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

Patch AUDIT-SITEMAP-TIERS-2026-07-30 (t_85288418) : <lastmod> calcule via
git log -1 %aI -- <file> (date honnete du dernier commit sur le fichier
serti) au lieu de TODAY = date.today(). 9/10 sitemaps Norte-OS etaient
a 0-1.5% honnete.

Usage :
  python3 scripts/build_sitemap_full.py
"""
import os
import subprocess
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


def git_lastmod(rel_path: str) -> str:
    """Renvoie la date du dernier commit (YYYY-MM-DD) pour le fichier
    `rel_path` (relatif a la racine du repo), ou TODAY si git echoue.
    Patch AUDIT-SITEMAP-TIERS-2026-07-30 §7.1.
    """
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%aI", "--", rel_path],
            cwd=ROOT, capture_output=True, text=True, timeout=5,
        ).stdout.strip()
        if not out:
            return TODAY
        return out[:10]
    except Exception:
        return TODAY


def list_html_slugs(directory):
    """Liste tous les .html (slug = filename sans .html)."""
    if not os.path.isdir(directory):
        return []
    return sorted(
        f[:-5] for f in os.listdir(directory)
        if f.endswith(".html") and os.path.isfile(os.path.join(directory, f))
    )


def build_sitemap_xml(urls_with_relpath):
    """`urls_with_relpath` = liste de (url, priority, relPath)."""
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for url, priority, rel_path in urls_with_relpath:
        lines.append(
            f'<url><loc>{url}</loc><lastmod>{git_lastmod(rel_path)}</lastmod>'
            f'<priority>{priority}</priority></url>'
        )
    lines.append('</urlset>')
    lines.append('')
    return '\n'.join(lines)


def main():
    # 1) Racine : TOUTES les .html (sans seuil)
    root_html = list_html_slugs(ROOT)

    # 2) /concelhos/
    concelhos_dir = os.path.join(ROOT, "concelhos")
    concelhos_html = list_html_slugs(concelhos_dir)

    # 3) /distritos/
    distritos_dir = os.path.join(ROOT, "distritos")
    distritos_html = list_html_slugs(distritos_dir)

    # Construction ordonnee avec relPath.
    entries = []

    # index.html en priorite 1.0
    if "index" in root_html:
        entries.append((f"{BASE_URL}/", "1.0", "index.html"))
        root_html_no_index = [s for s in root_html if s != "index"]
    else:
        root_html_no_index = root_html

    # Autres piliers racine : priorite 0.7
    for slug in sorted(root_html_no_index):
        entries.append((f"{BASE_URL}/{slug}", "0.7", f"{slug}.html"))

    # Concelhos : priorite 0.8
    for slug in concelhos_html:
        entries.append((f"{BASE_URL}/concelhos/{slug}", "0.8", f"concelhos/{slug}.html"))

    # Distritos : priorite 0.7
    for slug in distritos_html:
        entries.append((f"{BASE_URL}/distritos/{slug}", "0.7", f"distritos/{slug}.html"))

    # Stats
    print(f"=== SITEMAP COMPLET (P0 indexation) ===")
    print(f"  BASE_URL         : {BASE_URL}")
    print(f"  Pages racine     : {len(root_html)}")
    print(f"  Concelhos/       : {len(concelhos_html)}")
    print(f"  Distritos/       : {len(distritos_html)}")
    print(f"  TOTAL URLs       : {len(entries)}")

    # Generation XML
    xml = build_sitemap_xml(entries)

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
