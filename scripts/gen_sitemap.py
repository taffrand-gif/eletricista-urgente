#!/usr/bin/env python3
"""Generate the sitemap from root HTML pages served by this static site.

EU is deployed from the repository root (``vercel.json`` has
``outputDirectory: "."``).  Discovering only curated concelhos left most
served pages out of the sitemap, so the root HTML inventory is the source of
truth, matching the working generator used by canalizador-urgente.

URLs are extensionless because Vercel ``cleanUrls`` is enabled.  ``lastmod``
is the latest Git author date for each page, never the build date.
"""
from __future__ import annotations

import subprocess
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "eletricista-urgente.pt"


def page_slugs() -> list[Path]:
    """Return every root HTML page in stable order, with the homepage first."""
    return sorted(ROOT.glob("*.html"), key=lambda path: (path.name != "index.html", path.name))


def git_lastmod(page: Path) -> str:
    """Return the committed author date for a page."""
    relative = page.relative_to(ROOT).as_posix()
    result = subprocess.run(
        ["git", "log", "-1", "--format=%aI", "--", relative],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
    )
    value = result.stdout.strip()
    if result.returncode != 0 or not value:
        detail = result.stderr.strip() or "no commit found"
        raise RuntimeError(f"cannot determine Git lastmod for {relative}: {detail}")
    try:
        date.fromisoformat(value[:10])
    except ValueError as exc:
        raise RuntimeError(f"invalid Git author date for {relative}: {value}") from exc
    return value[:10]


def build_xml(pages: list[Path]) -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for page in pages:
        slug = "" if page.stem == "index" else page.stem
        loc = f"https://{DOMAIN}/{slug}"
        priority = "1.0" if page.name == "index.html" else "0.7"
        lines.append(
            f"<url><loc>{escape(loc)}</loc><lastmod>{git_lastmod(page)}</lastmod>"
            f"<priority>{priority}</priority></url>"
        )
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main() -> int:
    pages = page_slugs()
    output = ROOT / "sitemap.xml"
    output.write_text(build_xml(pages), encoding="utf-8")
    print(f"sitemap.xml written: {len(pages)} root URLs")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
