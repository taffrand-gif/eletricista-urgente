#!/usr/bin/env python3
"""Compatibility entry point for the controlled EU sitemap generator.

The old implementation discovered every root HTML file and could reintroduce
technical, preview or doorway surfaces. Keep this command available for old
runbooks, but route it through ``build_sitemap_full.py`` so every entry point
uses the same curated discovery population and honest Git ``lastmod`` values.
"""
from __future__ import annotations

from build_sitemap_full import main


if __name__ == "__main__":
    raise SystemExit(main())
