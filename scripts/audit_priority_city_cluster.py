#!/usr/bin/env python3
"""Audit mécanique du cluster ville prioritaire EU.

Vérifie les 9 pages `eletricista-urgente-<ville>` promues dans le sitemap core :
fichier, sitemap, canonical self-ref, absence de noindex, liens depuis le hub
concelho, lien téléphonique cliquable visible tôt, FAQPage + Person JSON-LD.

Exit 0 = conforme ; exit 1 = au moins un défaut.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://eletricista-urgente.pt"
PHONE_HREF = "tel:+351932321892"
CITIES = {
    "braganca": "Bragança",
    "chaves": "Chaves",
    "vila-real": "Vila Real",
    "mirandela": "Mirandela",
    "macedo-de-cavaleiros": "Macedo de Cavaleiros",
    "miranda-do-douro": "Miranda do Douro",
    "mogadouro": "Mogadouro",
    "vinhais": "Vinhais",
    "lamego": "Lamego",
}
CORE_EXPECTED = {
    "concelhos": 33,
    "distritos": 6,
    "priority_cities": len(CITIES),
    "total": 56,
}
KNOWN_CORE_NONSELF = {
    # Dette préexistante hors scope de la mission ville ; le script la rend visible
    # sans masquer les invariants stricts des 9 nouvelles cibles prioritaires.
    f"{BASE}/sobre": f"{BASE}/sobre.html",
}

CANONICAL_RE = re.compile(
    r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', re.I
)
NOINDEX_RE = re.compile(
    r'<meta[^>]+(?:name=["\']robots["\'][^>]+content=["\'][^"\']*noindex|'
    r'content=["\'][^"\']*noindex[^>]+name=["\']robots["\'])',
    re.I,
)
JSONLD_RE = re.compile(
    r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.I | re.S,
)
LOC_RE = re.compile(r"<loc>([^<]+)</loc>")


def schema_types(value: object) -> set[str]:
    types: set[str] = set()

    def walk(node: object) -> None:
        if isinstance(node, dict):
            node_type = node.get("@type")
            if isinstance(node_type, str):
                types.add(node_type)
            elif isinstance(node_type, list):
                types.update(item for item in node_type if isinstance(item, str))
            for child in node.values():
                walk(child)
        elif isinstance(node, list):
            for child in node:
                walk(child)

    walk(value)
    return types


def main() -> int:
    sitemap_path = ROOT / "sitemap.xml"
    sitemap_urls = LOC_RE.findall(sitemap_path.read_text(encoding="utf-8"))
    sitemap_url_set = set(sitemap_urls)
    failures: list[str] = []
    core_counts = {
        "concelhos": sum(f"{BASE}/concelhos/" in url for url in sitemap_urls),
        "distritos": sum(f"{BASE}/distritos/" in url for url in sitemap_urls),
        "priority_cities": sum(
            url.startswith(f"{BASE}/eletricista-urgente-") for url in sitemap_urls
        ),
        "total": len(sitemap_urls),
    }
    for metric, expected in CORE_EXPECTED.items():
        if core_counts[metric] != expected:
            failures.append(
                f"sitemap core: {metric}={core_counts[metric]} (attendu {expected})"
            )
    if len(sitemap_urls) != len(sitemap_url_set):
        failures.append("sitemap core: URLs dupliquées")

    core_known_debt: list[dict[str, str | None]] = []
    for debt_url, expected_canonical in KNOWN_CORE_NONSELF.items():
        debt_path = ROOT / f"{debt_url.removeprefix(BASE).lstrip('/')}.html"
        debt_content = debt_path.read_text(encoding="utf-8", errors="ignore")
        debt_match = CANONICAL_RE.search(debt_content)
        actual_canonical = debt_match.group(1) if debt_match else None
        core_known_debt.append(
            {
                "url": debt_url,
                "expected_canonical": expected_canonical,
                "actual_canonical": actual_canonical,
            }
        )
        if actual_canonical != expected_canonical:
            failures.append(
                f"dette core connue a changé: {debt_url} canonical={actual_canonical}"
            )

    rows: list[dict[str, object]] = []

    for slug, city in CITIES.items():
        page_path = ROOT / f"eletricista-urgente-{slug}.html"
        hub_path = ROOT / "concelhos" / f"{slug}.html"
        url = f"{BASE}/eletricista-urgente-{slug}"
        row: dict[str, object] = {"city": city, "url": url}

        if not page_path.exists():
            failures.append(f"{city}: fichier page absent")
            rows.append(row)
            continue
        if not hub_path.exists():
            failures.append(f"{city}: hub concelho absent")
            rows.append(row)
            continue

        page = page_path.read_text(encoding="utf-8", errors="ignore")
        hub = hub_path.read_text(encoding="utf-8", errors="ignore")
        canonical_match = CANONICAL_RE.search(page)
        canonical = canonical_match.group(1).rstrip("/") if canonical_match else None
        page_head = page.split("</head>", 1)[0]
        body_prefix = page.split("<body", 1)[-1][:7000]

        schemas: set[str] = set()
        invalid_jsonld = 0
        for raw in JSONLD_RE.findall(page):
            try:
                schemas.update(schema_types(json.loads(raw)))
            except json.JSONDecodeError:
                invalid_jsonld += 1

        checks = {
            "sitemap": url in sitemap_url_set,
            "canonical_self": canonical == url,
            "indexable_meta": NOINDEX_RE.search(page_head) is None,
            "hub_link": bool(
                re.search(
                    rf'href=["\'](?:{re.escape(BASE)})?/eletricista-urgente-{re.escape(slug)}(?:\.html)?["\']',
                    hub,
                    re.I,
                )
            ),
            "phone_above_fold": PHONE_HREF in body_prefix,
            "faq_schema": "FAQPage" in schemas,
            "person_schema": "Person" in schemas,
            "jsonld_valid": invalid_jsonld == 0,
        }
        row.update(checks)
        rows.append(row)
        for check, ok in checks.items():
            if not ok:
                failures.append(f"{city}: {check}=KO")

    print(
        json.dumps(
            {
                "sitemap_core": core_counts,
                "core_known_debt": core_known_debt,
                "pages": rows,
                "failures": failures,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
