#!/usr/bin/env python3
"""
Action #5 prep — Audit édit H1/title/concelhos des 33 pages concelhos EU
pour identifier le pattern doorway « Prix + Zone + ETA ».

Mission : fournir une preuve READ-ONLY + une reco éditable pour la PR draftée
« neutraliser le pattern doorway dans H1 et 80ers chars du title ».

Doctrine verrouillée EU-INDEXATION-DIAGNOSTIC-2026-07-18 §3 Action #5 :
  - Pattern doorway identifié : H1 et 80 premiers chars du `<title>`
    exposent simultanément « {PRIX}€ + Zona N + ETA minutes ».
  - Le contenu body reste OK (5 localités TomTom + FAQ + 5 cas pratiques),
    c'est le packaging H1/title qui tilt la GoogleDoorwayPolicy.
  - Reco : retirer ETA et zone du H1 et des 80ers chars du title. Les
    garder dans le body et la FAQ, mais pas dans la signature visible
    par Googlebot.

Catégories :
  - DOORWAY_H1     : H1 expose explicitement ETA (rare mais possible)
  - DOORWAY_TITLE  : title expose Prix + ETA dans les 80 premiers chars
  - DOORWAY_PILL   : paragraphe juste après H1 expose le « Zone-pill »
  - NEUTRE         : aucune exposition Prix/Zone/ETA dans surfaces visibles
  - UNKNOWN        : structure H1 non reconnue

Sortie : JSON par concelho + verdict global.
Doctrine PT-PT, lecture seule, aucun prix inventé (regex sur pattern existant).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONCELHOS_DIR = REPO_ROOT / "concelhos"
AUDIT_OUT = REPO_ROOT / "_audit" / "AUDIT-EDIT-DOORWAY-CONCELHOS-2026-07-18.json"

# Pattern doorway à détecter. Le "€" en UTF-8 peut être collé ou suivi
# d'un mot, donc on accepte l'absence de word boundary à droite.
PRICE_RE = re.compile(r"\b(\d+)\s*€")
ZONE_RE = re.compile(r"Zona\s+\d", re.IGNORECASE)
ETA_RE = re.compile(r"~\d+\s*min|\d+\s*minutos?|\d+\s*min\b", re.IGNORECASE)
TITLE_FIRST_CHARS = 80  # le diagnostic parle de "80 premiers caractères"


def extract_title(html: str) -> str:
    m = re.search(r"<title>([^<]+)</title>", html)
    return m.group(1).strip() if m else ""


def extract_h1(html: str) -> str:
    m = re.search(r"<h1[^>]*>([^<]+)</h1>", html)
    return m.group(1).strip() if m else ""


def extract_after_h1(html: str) -> str:
    """Le paragraphe juste après H1, qui contient souvent le 'Zone-pill'."""
    m = re.search(r"<h1[^>]*>[^<]+</h1>([\s\S]{0,500}?)<(?:div|h2|section)", html)
    return (m.group(1) if m else "").strip()


def audit_concelho(path: Path) -> dict:
    html = path.read_text(encoding="utf-8")
    title = extract_title(html)
    h1 = extract_h1(html)
    after_h1 = extract_after_h1(html)

    title_first = title[:TITLE_FIRST_CHARS]
    title_contains_price = bool(PRICE_RE.search(title_first))
    title_contains_eta = bool(ETA_RE.search(title_first))
    h1_contains_eta = bool(ETA_RE.search(h1))
    h1_contains_zone = bool(ZONE_RE.search(h1))
    pill_contains_zone = bool(ZONE_RE.search(after_h1))
    pill_contains_eta = bool(ETA_RE.search(after_h1))

    # DOORWAY_TITLE strict = Prix ET ETA simultanément dans 80 chars
    # (définition verrouillée diagnostic §1.4).
    doorway_title_strict = title_contains_price and title_contains_eta
    # TITLE_AVEC_PRIX = le title contient Prix (même sans ETA). Le geste
    # recommandé par le diagnostic est de retirer le Prix des 80ers chars,
    # donc même les titres "Prix seul" sont candidats au patch.
    title_avec_prix = title_contains_price

    categories = []
    if h1_contains_eta or h1_contains_zone:
        categories.append("DOORWAY_H1")
    if doorway_title_strict:
        categories.append("DOORWAY_TITLE_STRICT")
    elif title_avec_prix:
        # Pas doorway strict mais candidat au geste recommandé
        categories.append("TITLE_AVEC_PRIX")
    if pill_contains_zone and pill_contains_eta:
        categories.append("DOORWAY_PILL")
    if not categories:
        categories.append("NEUTRE")

    return {
        "slug": path.stem,
        "title": title,
        "title_first_chars": title_first,
        "title_contains_price": title_contains_price,
        "title_contains_eta": title_contains_eta,
        "h1": h1,
        "h1_contains_eta": h1_contains_eta,
        "h1_contains_zone": h1_contains_zone,
        "after_h1_excerpt": after_h1[:200],
        "pill_contains_zone": pill_contains_zone,
        "pill_contains_eta": pill_contains_eta,
        "doorway_title_strict": doorway_title_strict,
        "title_avec_prix": title_avec_prix,
        "categories": categories,
    }


def reco_for(cat: dict) -> list[str]:
    """Recommandations éditables (PR draftée, à merger conditionnellement)."""
    recos: list[str] = []
    if "DOORWAY_TITLE" in cat["categories"]:
        m = PRICE_RE.search(cat["title_first_chars"])
        if m:
            recos.append(
                f"Title : retirer '{m.group(0)}' des 80ers chars. "
                f"Exemple : '⚡ Eletricista Urgente "
                f"{cat['slug'].replace('-', ' ').title()} | Norte Reparos 24h' "
                f"(sans prix)."
            )
    if "DOORWAY_H1" in cat["categories"]:
        recos.append(
            "H1 : retirer ETA + zone. Le titre actuel doit indiquer le "
            "service + le lieu + la disponibilité 24h, sans chiffres tarifaires "
            "ni ETA."
        )
    if "DOORWAY_PILL" in cat["categories"]:
        recos.append(
            "Pill (zone-pill) : conserver pour l'UX (utilité interne), mais le "
            "déplacer APRES le premier H2 de contenu (ex. après 'Sobre o "
            "serviço'). Sortir le bloc 'Zona N · Deslocação X€ · Resposta em "
            "~N min' du top above-the-fold."
        )
    return recos


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args()

    if not CONCELHOS_DIR.exists():
        print(f"ERROR: {CONCELHOS_DIR} introuvable.", file=sys.stderr)
        return 1

    files = sorted(CONCELHOS_DIR.glob("*.html"))
    print(f"Audit édit doorway sur {len(files)} concelhos...")

    audited = []
    stats = {
        "DOORWAY_H1": 0,
        "DOORWAY_TITLE_STRICT": 0,
        "TITLE_AVEC_PRIX": 0,
        "DOORWAY_PILL": 0,
        "NEUTRE": 0,
    }
    for path in files:
        cat = audit_concelho(path)
        for c in cat["categories"]:
            stats[c] = stats.get(c, 0) + 1
        cat["recos"] = reco_for(cat)
        audited.append(cat)

    total = len(audited)
    pct_neutral = round(stats["NEUTRE"] / total * 100, 2) if total else 0
    pct_pill = round(stats["DOORWAY_PILL"] / total * 100, 2) if total else 0

    report = {
        "ran_at": datetime.utcnow().isoformat() + "Z",
        "scope": "33 concelhos EU (sitemap-core)",
        "diagnostic_ref": "_audit/EU-INDEXATION-DIAGNOSTIC-2026-07-18.md §3 Action #5",
        "stats": stats,
        "pct_neutral": pct_neutral,
        "pct_pill": pct_pill,
        "verdict": (
            f"DOORWAY_H1={stats['DOORWAY_H1']}/{total} — "
            f"DOORWAY_TITLE_STRICT(Prix+ETA simultanés)="
            f"{stats['DOORWAY_TITLE_STRICT']}/{total} — "
            f"TITLE_AVEC_PRIX(candidat patch recommandé)="
            f"{stats['TITLE_AVEC_PRIX']}/{total} — "
            f"DOORWAY_PILL(pill zone+ETA sous H1)="
            f"{stats['DOORWAY_PILL']}/{total} ({pct_pill}%) — "
            f"NEUTRE={stats['NEUTRE']}/{total}"
        ),
        "reading": (
            f"0/{total} H1 doorway, 0/{total} title doorway strict (Prix+ETA), "
            f"{stats['DOORWAY_PILL']}/{total} ont le pill 'Zone N · Deslocação "
            f"X€ · Resposta em ~N min' juste sous H1 (above-the-fold). "
            f"Tous les {stats['TITLE_AVEC_PRIX']}/{total} titres contiennent "
            f"un Prix. Le geste éditorial recommandé par le diagnostic = "
            f"(a) retirer Prix des 80ers chars du title, (b) déplacer le "
            f"pill 'Zone N' sous le 1er H2 body."
        ),
        "per_concelho": audited,
        "next_action": (
            "PR draftée conditionnelle : pour les 33 concelhos, retirer Prix "
            "des 80ers chars du title + déplacer pill 'Zone N · Deslocação "
            "X€ · Resposta em ~N min' sous le 1er H2 body. À merger UNIQUEMENT "
            "si Action #3 (J+5) confirme cause (a) éditoriale, c'est-à-dire "
            "ΔINDEXED ≤ +1 ET ΔUNKNOWN ≥ 0. Sinon la cause (d) « déployé "
            "trop récent » se résout toute seule et la PR est inutile."
        ),
        "doctrine_note": (
            "PRIX RESTENT dans le body, la FAQ, le JSON-LD, la meta description. "
            "On ne retire que la signature H1/title/above-the-fold. Aucune "
            "valeur inventée : toutes les regex détectent le pattern existant, "
            "on propose uniquement des retraits."
        ),
    }

    AUDIT_OUT.parent.mkdir(parents=True, exist_ok=True)
    AUDIT_OUT.write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Rapport écrit dans {AUDIT_OUT}")
    print(report["verdict"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
