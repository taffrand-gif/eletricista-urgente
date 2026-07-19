#!/usr/bin/env python3
"""
Action #4 prep — Transforme `<ul class="concelhos-grid">` des `distritos/*.html`
EU pour ajouter des `<a href="/concelhos/<slug>">` autour de chaque nom.

Mission : fixer le hub-and-spoke cassé (cause #2 du diagnostic EU 2026-07-18).
Les 6 pages `distritos/*.html` ont du contenu (5 KB chacune) mais zéro lien
vers les concellos qu'elles sont censées agréger. GoogleBot les classe en
UNKNOWN (4/6 districts).

Doctrine verrouillée :
  - Source de vérité = `data/concelhos.json` (slug + district + name).
  - Aucune URL inventée. Tout slug doit exister en `concelhos/`.
  - Aucune ligne `<li>` retirée — on wrappe le nom existant dans un `<a>`.
  - Si un nom ne matche aucun slug → WARN stderr, ligne inchangée (sécurité).
  - Mapping name → slug : match exact d'abord, fallback heuristique
    (lowercase, sans accents, tirets) si besoin.
  - Écriture IDEMPOTENTE : si déjà wrappé, ne touche pas.

Usage :
    # Dry-run (par défaut, n'écrit rien, montre les diffs)
    python3 tools/enrich-distritos-maillage.py

    # Appliquer (commit séparé)
    python3 tools/enrich-distritos-maillage.py --apply

Sortie : rapport JSON `_audit/AUDIT-DISTRITOS-MAILLAGE-2026-07-18.json`.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DISTRITOS_DIR = REPO_ROOT / "distritos"
CONCELHOS_JSON = REPO_ROOT / "data" / "concelhos.json"
AUDIT_OUT = REPO_ROOT / "_audit" / "AUDIT-DISTRITOS-MAILLAGE-2026-07-18.json"

# Districts officiels du site (cf. diagnostic §1.2 et §2.2)
DISTRITOS = ["braganca", "douro", "guarda", "tras-os-montes", "vila-real", "viseu"]


def slugify_pt(name: str) -> str:
    """Slug PT-PT conforme au canonique Vercel (extensionless, minuscules, tirets)."""
    text = unicodedata.normalize("NFKD", name)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower()
    # Remplacements manuels pour caractères spéciaux PT
    text = text.replace("ç", "c").replace("ã", "a").replace("õ", "o")
    text = text.replace("á", "a").replace("à", "a").replace("â", "a")
    text = text.replace("é", "e").replace("ê", "e")
    text = text.replace("í", "i")
    text = text.replace("ó", "o").replace("ô", "o")
    text = text.replace("ú", "u")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def load_slug_index() -> dict[str, dict[str, str]]:
    """Construit l'index name→slug (canonique) et slugify→slug pour fallback.

    Returns:
        dict avec deux clés :
          - ``by_name`` : {name canonique: slug} (cf. data/concelhos.json)
          - ``by_slugify`` : {slugify_pt(name): slug} (fallback heuristique)
          - ``by_alias`` : alias manuels (abréviations PT, sigles)
    """
    data = json.loads(CONCELHOS_JSON.read_text(encoding="utf-8"))
    by_name: dict[str, str] = {}
    by_slugify: dict[str, str] = {}
    for c in data:
        by_name[c["name"]] = c["slug"]
        sf = slugify_pt(c["name"])
        if sf and sf not in by_slugify:
            by_slugify[sf] = c["slug"]
    # Alias manuels — abréviations observées dans distritos/*.html.
    # Chaque entrée : alias (telle qu'écrite dans le <li>) → slug canonique.
    by_alias: dict[str, str] = {
        "S. João da Pesqueira": "sao-joao-da-pesqueira",
        "VN Foz Côa": "vila-nova-de-foz-coa",
        "São João da Pesqueira": "sao-joao-da-pesqueira",
        "Vila Nova de Foz Côa": "vila-nova-de-foz-coa",
    }
    # Fusion : by_alias est prioritaire sur les heuristiques car explicitement
    # validé par l'agent lors du diagnostic 2026-07-18.
    by_alias.update({k: v for k, v in by_alias.items() if k not in by_alias})
    return {"by_name": by_name, "by_slugify": by_slugify, "by_alias": by_alias}


def transform_li(html: str, index: dict[str, dict[str, str]]) -> tuple[str, list[str]]:
    """Ajoute `<a href>` autour des `<li>X</li>`. Retourne (html, warns)."""
    warns: list[str] = []
    by_name = index["by_name"]
    by_slugify = index["by_slugify"]
    by_alias = index.get("by_alias", {})

    def replace(match: re.Match) -> str:
        inner = match.group(1)
        # Si déjà wrappé → idempotent
        if "<a " in inner or "<a\n" in inner:
            return match.group(0)
        # Le nom dans <li> peut contenir des annotations type "(zona norte"
        # → on extrait le nom "officiel" en nettoyant
        # Stratégie : prendre jusqu'à la première "(" ou "," ou ";"
        cleaned = re.split(r"\s*[\(,;]", inner, maxsplit=1)[0].strip()
        if not cleaned:
            return match.group(0)
        # Entrées purement éditoriales (pas un vrai concelho) → skip sans warn
        editorial_skip = (
            "Todos os concelhos",
            "Trás-os-Montes",  # apparaît dans braganca.html par erreur éditoriale
        )
        if any(cleaned.startswith(s) for s in editorial_skip):
            return match.group(0)
        # Lookup alias → name canonique → slugify
        slug = by_alias.get(cleaned)
        if not slug:
            slug = by_name.get(cleaned)
        if not slug:
            slug = by_slugify.get(slugify_pt(cleaned))
        if not slug:
            warns.append(f"WARNING: nom non matché: '{cleaned}' (ligne {inner[:60]})")
            return match.group(0)
        return f'<li><a href="/concelhos/{slug}">{inner}</a></li>'

    return re.sub(r"<li>([^<]+)</li>", replace, html), warns


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Applique les modifications (par défaut : dry-run).",
    )
    args = parser.parse_args()

    if not CONCELHOS_JSON.exists():
        print(f"ERROR: {CONCELHOS_JSON} introuvable.", file=sys.stderr)
        return 1

    index = load_slug_index()
    report = {
        "ran_at": datetime.utcnow().isoformat() + "Z",
        "mode": "apply" if args.apply else "dry-run",
        "by_distrito": {},
        "summary": {
            "distritos_processed": 0,
            "total_li_before": 0,
            "total_li_after": 0,
            "total_warns": 0,
        },
    }

    for dist in DISTRITOS:
        path = DISTRITOS_DIR / f"{dist}.html"
        if not path.exists():
            report["by_distrito"][dist] = {"error": "file missing"}
            continue
        original = path.read_text(encoding="utf-8")
        # Localiser le bloc <ul class="concelhos-grid">...</ul>
        m = re.search(
            r'(<ul class="concelhos-grid">)([\s\S]*?)(</ul>)', original
        )
        if not m:
            report["by_distrito"][dist] = {"error": "concelhos-grid not found"}
            continue
        block = m.group(2)
        li_before = re.findall(r"<li>([^<]+)</li>", block)
        new_block, warns = transform_li(block, index)
        new_html = original.replace(m.group(0), m.group(1) + new_block + m.group(3))
        report["by_distrito"][dist] = {
            "li_count": len(li_before),
            "li_names_before": li_before,
            "warns": warns,
            "block_chars": len(block),
            "new_block_chars": len(new_block),
            "modified": new_block != block,
        }
        report["summary"]["distritos_processed"] += 1
        report["summary"]["total_li_before"] += len(li_before)
        report["summary"]["total_warns"] += len(warns)
        if new_block != block:
            li_after = re.findall(r"<a href=\"/concelhos/[^\"]+\"", new_block)
            report["summary"]["total_li_after"] += len(li_after)
        else:
            report["summary"]["total_li_after"] += len(li_before)

        if args.apply and new_block != block:
            path.write_text(new_html, encoding="utf-8")
            print(f"[APPLY] {dist}.html : {len(li_before)} <li> wrappées")
        elif not args.apply:
            print(f"[DRY ] {dist}.html : {len(li_before)} <li> à wrapper, {len(warns)} warns")
        if warns:
            for w in warns:
                print(f"   {w}", file=sys.stderr)

    AUDIT_OUT.parent.mkdir(parents=True, exist_ok=True)
    AUDIT_OUT.write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"\nRapport écrit dans {AUDIT_OUT}")
    print(
        f"Total : {report['summary']['total_li_before']} <li> détectées, "
        f"{report['summary']['total_li_after']} wrappées, "
        f"{report['summary']['total_warns']} warns."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
