#!/usr/bin/env python3
"""Generate the root sitemap from the HTML pages served by this static site.

Only root-level pages are considered.  Archive directories and partial/template
files are deliberately excluded.  The root and public mirrors stay identical.
"""
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape
import sys

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DOMAIN = "eletricista-urgente.pt"
EXCLUDED_NAMES = {"404.html"}
EXCLUDED_MARKERS = ("template", "partial")


def page_slugs():
    pages = []
    for path in ROOT.glob("*.html"):
        name = path.name.lower()
        if name in EXCLUDED_NAMES or any(marker in name for marker in EXCLUDED_MARKERS):
            continue
        pages.append(path)
    return sorted(pages, key=lambda path: (path.name != "index.html", path.name))


def build_xml(domain: str, pages: list[Path]) -> str:
    lastmod = date.today().isoformat()
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for page in pages:
        slug = "" if page.stem == "index" else page.stem
        loc = f"https://{domain}/{slug}"
        lines.append(f"<url><loc>{escape(loc)}</loc><lastmod>{lastmod}</lastmod></url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main() -> int:
    domain = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else DEFAULT_DOMAIN
    pages = page_slugs()
    xml = build_xml(domain, pages)
    targets = [ROOT / "sitemap.xml"]
    public = ROOT / "public"
    if public.is_dir():
        targets.append(public / "sitemap.xml")
    for target in targets:
        target.write_text(xml, encoding="utf-8")
    print(f"Generated {len(pages)} URLs for {domain}")
    for target in targets:
        print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
