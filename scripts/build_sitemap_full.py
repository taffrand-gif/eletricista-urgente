#!/usr/bin/env python3
"""
Génère les sitemaps EU depuis la population métier curatée.

La population unique vient de ``scripts/gen_sitemap_discovery.py`` :
pages piliers, concelhos, distritos, blog et pages money indexables.
Ce wrapper ne découvre jamais tous les HTML du dépôt ; il ajoute seulement
les ``lastmod`` Git honnêtes et écrit les deux miroirs sitemap.

Format URL : https://<domain>/<slug> (sans .html, conforme canonical self-ref)

La sortie doit rester alignée sur la population discovery, sans réintroduire
les previews, pages techniques ou doorways non sélectionnés.

Patch AUDIT-SITEMAP-TIERS-2026-07-30 (t_85288418) : <lastmod> calcule via
git log -1 %aI -- <file> (date honnete du dernier commit sur le fichier
serti) au lieu de TODAY = date.today(). 9/10 sitemaps Norte-OS etaient
a 0-1.5% honnete.

Usage :
  python3 scripts/build_sitemap_full.py https://eletricista-urgente.pt
"""
import os
import subprocess
import sys

from gen_sitemap_discovery import build_sitemap as build_curated_population

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# EU domain is explicit; argv[1] remains an override for local verification.
if len(sys.argv) > 1:
    BASE_URL = sys.argv[1].rstrip("/")
else:
    BASE_URL = "https://eletricista-urgente.pt"


def git_lastmod(rel_path: str) -> str:
    """Renvoie la date du dernier commit (YYYY-MM-DD) pour le fichier
    `rel_path` (relatif a la racine du repo).
    Patch AUDIT-SITEMAP-TIERS-2026-07-30 §7.1.
    """
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%aI", "--", rel_path],
            cwd=ROOT, capture_output=True, text=True, timeout=5,
        ).stdout.strip()
        if not out:
            raise RuntimeError(f"No Git author date for {rel_path}")
        return out[:10]
    except Exception as exc:
        raise RuntimeError(f"Cannot determine Git lastmod for {rel_path}") from exc


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


def resolve_page(path: str):
    """Resolve a curated URL path to its served HTML source file."""
    if path == "/":
        return "index.html"
    rel = path.lstrip("/")
    candidate = os.path.join(ROOT, f"{rel}.html")
    if not os.path.isfile(candidate):
        raise FileNotFoundError(f"Curated URL has no matching HTML: {path} -> {candidate}")
    return os.path.relpath(candidate, ROOT)


def main():
    # Source unique de population : discovery métier curaté et testé.
    entries = []
    for path, priority in build_curated_population():
        entries.append((f"{BASE_URL}{path}", priority, resolve_page(path)))

    # Stats
    print(f"=== SITEMAP COMPLET (P0 indexation) ===")
    print(f"  BASE_URL         : {BASE_URL}")
    print("  Population       : gen_sitemap_discovery.py")
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
