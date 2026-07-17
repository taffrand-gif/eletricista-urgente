#!/usr/bin/env python3
"""
Genere sitemap.xml COMPLET pour le site (mode P0 indexation).

Inclusions :
- TOUTES les .html racine (sans seuil de taille, sans dedup md5) -> slug = filename sans .html
- /concelhos/ -> slug = filename sans .html
- /distritos/ -> slug = filename sans .html
- (Blog: exclu volontairement, court-terme; ne pas generer de bruit pour Google)

Format URL : https://<domain>/<slug> (sans .html, conforme canonical self-ref)

Mode P0 (mission 2026-07-16) : on liste TOUT, pas de seuil, pas de dedup md5.
L'objectif est de prouver a Google que chaque page racine a une URL dans le sitemap,
peu importe sa taille. Le seuillage par taille etait une heuristique de l'ancien
script (build_sitemap.py) ; on la supprime pour ce tour.

Usage :
  python3 scripts/build_sitemap_full.py
"""
import os
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Allow override via env or argv[1]
if len(sys.argv) > 1:
    BASE_URL = sys.argv[1].rstrip("/")
else:
    # Default: infer from repo path
    if "canalizador-urgente" in ROOT:
        BASE_URL = "https://canalizador-urgente.pt"
    elif "eletricista-urgente" in ROOT:
        BASE_URL = "https://eletricista-urgente.pt"
    else:
        raise SystemExit("Cannot infer BASE_URL, pass as argv[1]")

TODAY = date.today().isoformat()


def list_html_slugs(directory):
    """Liste tous les .html (slug = filename sans .html)."""
    if not os.path.isdir(directory):
        return []
    return sorted(
        f[:-5] for f in os.listdir(directory)
        if f.endswith(".html") and os.path.isfile(os.path.join(directory, f))
    )


def build_sitemap_xml(urls_with_priority):
    """Genere le XML sitemap.0.9 formate avec lastmod et priority."""
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for url, priority in urls_with_priority:
        lines.append(f'<url><loc>{url}</loc><lastmod>{TODAY}</lastmod><priority>{priority}</priority></url>')
    lines.append('</urlset>')
    lines.append('')
    return '\n'.join(lines)


def main():
    # 1) Racine : TOUTES les .html (sans seuil)
    root_html = list_html_slugs(ROOT)

    # 2) /concelhos/
    concelhos_html = list_html_slugs(os.path.join(ROOT, "concelhos"))

    # 3) /distritos/
    distritos_html = list_html_slugs(os.path.join(ROOT, "distritos"))

    # Construction ordonnee
    urls = []

    # index.html en priorite 1.0
    if "index" in root_html:
        urls.append((f"{BASE_URL}/", "1.0"))
        root_html_no_index = [s for s in root_html if s != "index"]
    else:
        root_html_no_index = root_html

    # Autres piliers racine : priorite 0.7
    # On ne distingue PAS piliers vs money ici : on liste tout
    for slug in sorted(root_html_no_index):
        urls.append((f"{BASE_URL}/{slug}", "0.7"))

    # Concelhos : priorite 0.8
    for slug in concelhos_html:
        urls.append((f"{BASE_URL}/concelhos/{slug}", "0.8"))

    # Distritos : priorite 0.7
    for slug in distritos_html:
        urls.append((f"{BASE_URL}/distritos/{slug}", "0.7"))

    # Stats
    print(f"=== SITEMAP COMPLET (P0 indexation {TODAY}) ===")
    print(f"  BASE_URL         : {BASE_URL}")
    print(f"  Pages racine     : {len(root_html)}")
    print(f"  Concelhos/       : {len(concelhos_html)}")
    print(f"  Distritos/       : {len(distritos_html)}")
    print(f"  TOTAL URLs       : {len(urls)}")

    # Generation XML
    xml = build_sitemap_xml(urls)

    # Ecriture : sitemap.xml racine + public/sitemap.xml
    out_paths = [
        os.path.join(ROOT, "sitemap.xml"),
        os.path.join(ROOT, "public", "sitemap.xml"),
    ]
    for p in out_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as fp:
            fp.write(xml)
        print(f"  Written: {p}")

    return 0


if __name__ == "__main__":
    sys.exit(main())