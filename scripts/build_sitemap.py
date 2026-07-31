#!/usr/bin/env python3
"""Regenerate the curated EU village sitemap with honest ``lastmod`` values.

The 1,936 URLs in ``sitemap-villages.xml`` are a deliberately curated
inventory.  Keep that inventory as the source of truth: this script updates
only the XML metadata and never discovers or invents new doorway URLs.

For every root HTML file, ``lastmod`` is the author date of its latest Git
commit (``git log -1 --format=%aI -- <file>``).  A missing Git date is an
error, rather than a fallback to today's date, because a build date is not a
page modification date.

Usage::

    python3 scripts/build_sitemap.py
    python3 scripts/build_sitemap.py --output /tmp/eu-sitemap.xml
    python3 scripts/build_sitemap.py --domain eletricista-urgente.pt

The default command writes only ``sitemap-villages.xml``.  In particular, it
does not touch ``public/sitemap*.xml`` or the core ``sitemap.xml``.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DOMAIN = "eletricista-urgente.pt"
DEFAULT_SOURCE = ROOT / "sitemap-villages.xml"

LOC_RE = re.compile(r"<loc>([^<]+)</loc>")
PRIORITY_RE = re.compile(r"<priority>([^<]+)</priority>")
LASTMOD_RE = re.compile(r"<lastmod>([^<]+)</lastmod>")


def source_entries(source: Path, domain: str) -> list[tuple[str, str, Path]]:
    """Read the curated URL inventory and resolve each URL to root HTML."""
    text = source.read_text(encoding="utf-8")
    locs = LOC_RE.findall(text)
    priorities = PRIORITY_RE.findall(text)
    if len(locs) != len(priorities):
        raise ValueError(
            f"{source}: {len(locs)} <loc> entries but {len(priorities)} priorities"
        )
    expected_prefix = f"https://{domain}/"
    entries: list[tuple[str, str, Path]] = []
    for loc, priority in zip(locs, priorities):
        if not loc.startswith(expected_prefix):
            raise ValueError(f"unexpected URL outside {domain}: {loc}")
        slug = loc[len(expected_prefix) :]
        if not slug or "/" in slug or slug.startswith("."):
            raise ValueError(f"expected a root extensionless URL, got: {loc}")
        page = ROOT / f"{slug}.html"
        if not page.is_file():
            raise FileNotFoundError(f"URL has no matching root HTML: {loc} ({page})")
        entries.append((loc, priority, page))
    if len(entries) != 1936:
        raise ValueError(f"expected curated EU inventory of 1936 URLs, got {len(entries)}")
    return entries


def git_lastmod(page: Path) -> str:
    """Return the committed author date for ``page``; never use today's date."""
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


def build_xml(entries: list[tuple[str, str, Path]], lastmods: dict[Path, str]) -> str:
    """Build sitemap XML without changing the curated URL or priority set."""
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc, priority, page in entries:
        lines.append(
            f"<url><loc>{escape(loc)}</loc>"
            f"<lastmod>{lastmods[page]}</lastmod>"
            f"<priority>{escape(priority)}</priority></url>"
        )
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--domain", default=DEFAULT_DOMAIN)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_SOURCE)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    source = args.source if args.source.is_absolute() else ROOT / args.source
    output = args.output if args.output.is_absolute() else ROOT / args.output
    entries = source_entries(source, args.domain.rstrip("/"))
    lastmods = {page: git_lastmod(page) for _, _, page in entries}
    output.write_text(build_xml(entries, lastmods), encoding="utf-8")
    print(f"Generated {len(entries)} URLs for {args.domain.rstrip('/')}")
    print(f"Written: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
