#!/usr/bin/env python3
"""
Audit qualité sitemap-villages.xml — préparation Action #2 diagnostic EU 2026-07-18.

Mission : avant de déclarer `sitemap-villages.xml` dans robots.txt (PR draftée),
produire un état des lieux READ-ONLY de ce qu'il y a dedans.

Catégories identifiées :
  - V_STD     : /eletricista-<slug>             (village money page long-tail)
  - V_URGENTE : /eletricista-urgente-<slug>     (village variante préfixée "urgente")
  - INSTITUC  : /<page-racine>                  (pages éditoriales/institutionnelles)
  - POLLUTION : URLs hors-pattern (calculadora-de-preco, comparacao, etc.)

Pour chaque catégorie on compte et on note si la catégorie est cohérente avec un
sitemap "villages" ou si elle contamine le signal Googlebot.

Doctrine respectée : PT-PT, aucun prix inventé, lecture seule.
Zéro contact réseau dans la version par défaut (mode --curl-only à activer
séparément pour mesurer le %200).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

# Accepte caractères latins accentués (PT-PT) dans les slugs de villages.
V_STD_RE = re.compile(
    r"^https://eletricista-urgente\.pt/eletricista-[a-z0-9à-ÿ-]+$"
)
V_URGENTE_RE = re.compile(
    r"^https://eletricista-urgente\.pt/eletricista-urgente-[a-z0-9à-ÿ-]+$"
)
POLLUTION_KNOWN = {
    "calculadora-de-preco",
    "como-poupar-eletricidade",
    "comparacao",
    "design-preview-eu",
}


def categorize(url: str) -> str:
    """Classe une URL du sitemap en V_STD / V_URGENTE / INSTITUC / POLLUTION."""
    path = urlparse(url).path.lstrip("/")
    if path in POLLUTION_KNOWN:
        return "POLLUTION"
    if V_URGENTE_RE.match(url):
        return "V_URGENTE"
    if V_STD_RE.match(url):
        return "V_STD"
    return "INSTITUC"


def load_urls(sitemap_path: Path) -> list[str]:
    text = sitemap_path.read_text(encoding="utf-8")
    return re.findall(r"<loc>([^<]+)</loc>", text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sitemap",
        default="sitemap-villages.xml",
        help="Chemin du sitemap-villages.xml (par défaut racine).",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Sortie JSON (par défaut stdout).",
    )
    args = parser.parse_args()

    sitemap = Path(args.sitemap)
    if not sitemap.exists():
        print(f"ERROR: {sitemap} introuvable.", file=sys.stderr)
        return 1

    urls = load_urls(sitemap)
    counter: Counter[str] = Counter()
    pollution_urls: list[str] = []
    instituc_urls: list[str] = []
    v_urgente_urls: list[str] = []

    for url in urls:
        cat = categorize(url)
        counter[cat] += 1
        if cat == "POLLUTION":
            pollution_urls.append(url)
        elif cat == "INSTITUC":
            instituc_urls.append(url)
        elif cat == "V_URGENTE":
            v_urgente_urls.append(url)

    total = len(urls)
    pct = {k: round(v / total * 100, 2) for k, v in counter.items()}

    report = {
        "sitemap": str(sitemap),
        "total_urls": total,
        "by_category": dict(counter),
        "by_category_pct": pct,
        "pollution_urls": sorted(pollution_urls),
        "instituc_sample": sorted(instituc_urls)[:20],
        "v_urgente_count": counter["V_URGENTE"],
        "v_urgente_sample": sorted(v_urgente_urls)[:10],
        "verdict": {
            "ready_to_declare": counter["POLLUTION"] == 0
            and counter["INSTITUC"] == 0,
            "blocking_issues": (
                []
                if counter["POLLUTION"] == 0 and counter["INSTITUC"] == 0
                else (
                    [f"{counter['POLLUTION']} URLs POLLUTION à supprimer avant déclaration"]
                    + [
                        f"{counter['INSTITUC']} URLs institutionnelles hors-périmètre"
                        " (à déplacer vers sitemap.xml ou exclure)"
                    ]
                )
            ),
            "v_urgente_observation": (
                f"{counter['V_URGENTE']} URLs préfixées /eletricista-urgente-<slug>/ "
                "— vérifier si elles ont du contenu réel ou sont des stubs. "
                "Si stubs : exclure. Si contenu : OK mais clarifier dans sitemap."
            ),
        },
        "next_action": (
            "Nettoyer les URLs POLLUTION + INSTITUC du sitemap-villages.xml, "
            "puis PR draftée déclarant Sitemap: https://eletricista-urgente.pt/sitemap-villages.xml "
            "dans robots.txt."
        ),
        "ran_at": datetime.utcnow().isoformat() + "Z",
    }

    output = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
        print(f"Rapport écrit dans {args.output}")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
