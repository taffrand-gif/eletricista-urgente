#!/usr/bin/env python3
"""Audit the EU P0 116-page pilot for legacy fixed travel fees and tariffs.

Scans each page as raw HTML, body-visible text, head metadata, text-bearing
attributes, and JSON-LD strings. With --base-url, the same layers are scanned
from public responses. The manifest is restricted to the approved pilot.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import csv
import html
import json
import re
import sys
import unicodedata
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "tests" / "fixtures" / "eu-p0-116-pages.csv"
PILOT_SIZE = 116

# The legacy amounts are old travel/exit fees. The amount may come before or
# after the fee term, with spaces, punctuation, plural nouns, or a currency word.
_OLD_NUMBER = r"(?:15|25|35|45|55|65)(?:[.,]0{1,2})?"
_CURRENCY = r"(?:€|eur(?:o|os)?)"
_OLD_MONEY = rf"{_OLD_NUMBER}\s*{_CURRENCY}"
_OLD_RANGE = rf"{_OLD_NUMBER}\s*(?:{_CURRENCY}\s*)?(?:[-–—]|\s+(?:a|ate)\s+)\s*{_OLD_NUMBER}\s*{_CURRENCY}"
_OLD_AMOUNT_OR_RANGE = rf"(?:{_OLD_RANGE}|{_OLD_MONEY})"
_OLD_START_TOTAL = r"(?:85|95|105|115|125|135)(?:[.,]0{1,2})?"
_LEGACY_START_TOTAL = re.compile(
    rf"\b(?:a\s+partir\s+de|desde)\s*{_OLD_START_TOTAL}\s*{_CURRENCY}(?=\s|$|[.,;:!?)])",
    re.IGNORECASE,
)
_LEGACY_ZONE = re.compile(
    r"\b(?:Z\s*[1-6](?:\s*(?:[-–—]|to|a)\s*(?:Z\s*)?[1-6])?|"
    r"Zona\s*[1-6](?:\s*(?:[-–—]|a)\s*(?:Zona\s*)?[1-6])?)\b",
    re.IGNORECASE,
)
_LEGACY_ZONE_ATTRIBUTE = re.compile(
    r"\bdata-zone\s*=\s*(?:&quot;|[\"'])?\s*[1-6]\s*(?:&quot;|[\"'])?",
    re.IGNORECASE,
)
_FEE_TERM = (
    r"(?:deslocac(?:ao|oes)"
    r"|taxas?\s+(?:de\s+)?saida"
    r"|custos?\s+(?:de\s+)?(?:deslocac(?:ao|oes)|saida)"
    r"|valores?\s+(?:de\s+)?(?:deslocac(?:ao|oes)|saida)"
    r"|precos?\s+(?:de\s+)?(?:deslocac(?:ao|oes)|saida)"
    r"|tarifas?\s+(?:de\s+)?(?:deslocac(?:ao|oes)|saida)"
    r"|despesas?\s+(?:de\s+)?deslocac(?:ao|oes)"
    r"|saidas?)"
)
_LEGACY_FEE_PATTERNS = (
    re.compile(
        rf"(?<!\d){_OLD_AMOUNT_OR_RANGE}(?!\w)\s*(?:(?:de|da|do|para|por)\s+)?{_FEE_TERM}\b",
        re.IGNORECASE,
    ),
    re.compile(
        rf"\b{_FEE_TERM}\b\s*(?:[:=\-–—]\s*)?(?:(?:de|da|do|para|por)\s+)?{_OLD_AMOUNT_OR_RANGE}(?!\w)",
        re.IGNORECASE,
    ),
)
_RULES: tuple[tuple[str, tuple[re.Pattern[str], ...]], ...] = (
    ("legacy_travel_fee", _LEGACY_FEE_PATTERNS),
    ("legacy_starting_total", (_LEGACY_START_TOTAL,)),
    ("legacy_zone_token", (_LEGACY_ZONE,)),
    ("legacy_zone_attribute", (_LEGACY_ZONE_ATTRIBUTE,)),
    (
        "legacy_surcharge",
        (
            re.compile(r"\+\s*(?:30\s*[-–—]\s*)?50\s*%", re.IGNORECASE),
            re.compile(r"\b(?:mais|acrescimo|majoracao|sobretaxa|adicional)\s+(?:de\s+)?(?:30\s*[-–—]\s*)?50\s*%(?!\w)", re.IGNORECASE),
        ),
    ),
    (
        "legacy_hours",
        (
            re.compile(r"\b0?9(?:\s*h|:00)\s*[-–—]\s*17(?:\s*h|:00)?\b", re.IGNORECASE),
            re.compile(r"\b0?8(?:\s*h|:00)\s*[-–—]\s*18(?:\s*h|:00)?\b", re.IGNORECASE),
        ),
    ),
)


@dataclass(frozen=True)
class Finding:
    route: str
    source: str
    layer: str
    rule: str
    match: str
    context: str


@dataclass(frozen=True)
class PageResult:
    route: str
    source: str
    status: int | None
    final_url: str | None
    findings: tuple[Finding, ...]
    error: str | None = None


def normalize(text: str) -> str:
    """Decode HTML entities, normalize Unicode/spacing, and fold accents."""
    text = html.unescape(text).replace("\u00a0", " ").replace("\u202f", " ")
    text = unicodedata.normalize("NFKD", text)
    text = "".join(char for char in text if not unicodedata.combining(char))
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\u20ac", "€")
    return re.sub(r"\s+", " ", text).strip()


class _HtmlLayers(HTMLParser):
    """Extract body text, metadata, text attributes, and JSON-LD separately."""

    _IGNORED = {"head", "script", "style", "noscript", "template"}
    _TEXT_ATTRIBUTES = {"alt", "title", "aria-label", "aria-description"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.visible_parts: list[str] = []
        self.metadata_parts: list[str] = []
        self.attribute_parts: list[str] = []
        self.jsonld_blocks: list[str] = []
        self._ignored_stack: list[str] = []
        self._script_jsonld = False
        self._script_parts: list[str] = []
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attrs_map = {key.lower(): (value or "") for key, value in attrs}
        if tag == "meta" and attrs_map.get("content"):
            self.metadata_parts.append(attrs_map["content"])
        for key, value in attrs_map.items():
            if key in self._TEXT_ATTRIBUTES and value:
                self.attribute_parts.append(value)
            if key == "data-zone" and value:
                self.attribute_parts.append(f"data-zone={value}")
        if tag == "title":
            self._in_title = True
        if tag == "script":
            self._script_jsonld = attrs_map.get("type", "").lower().split(";", 1)[0].strip() == "application/ld+json"
            self._script_parts = []
            self._ignored_stack.append(tag)
        elif tag in self._IGNORED:
            self._ignored_stack.append(tag)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self._in_title = False
        if tag == "script" and self._ignored_stack and self._ignored_stack[-1] == "script":
            if self._script_jsonld:
                self.jsonld_blocks.append("".join(self._script_parts))
            self._script_parts = []
            self._script_jsonld = False
            self._ignored_stack.pop()
        elif tag in self._IGNORED and self._ignored_stack and self._ignored_stack[-1] == tag:
            self._ignored_stack.pop()

    def handle_data(self, data: str) -> None:
        if self._ignored_stack:
            if self._ignored_stack[-1] == "script" and self._script_jsonld:
                self._script_parts.append(data)
            elif self._in_title:
                self.metadata_parts.append(data)
            return
        if self._in_title:
            self.metadata_parts.append(data)
        else:
            self.visible_parts.append(data)


def _json_strings(value: object) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from _json_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _json_strings(child)


def extract_layers(raw_html: str) -> tuple[str, list[str], str, str]:
    parser = _HtmlLayers()
    parser.feed(raw_html)
    parser.close()
    # Join text nodes split by inline tags, then collapse whitespace before matching.
    visible = normalize(" ".join(parser.visible_parts))
    metadata = " ".join(parser.metadata_parts)
    attributes = " ".join(parser.attribute_parts)
    jsonld_strings: list[str] = []
    for block in parser.jsonld_blocks:
        try:
            parsed = json.loads(block)
        except (json.JSONDecodeError, TypeError):
            # Keep the block searchable even if the page has unrelated malformed JSON-LD.
            jsonld_strings.append(block)
        else:
            jsonld_strings.extend(_json_strings(parsed))
    return visible, jsonld_strings, metadata, attributes


def scan_text(route: str, source: str, layer: str, text: str) -> list[Finding]:
    normalized = normalize(text)
    findings: list[Finding] = []
    seen: set[tuple[str, int, int]] = set()
    for rule, patterns in _RULES:
        for pattern in patterns:
            for match in pattern.finditer(normalized):
                key = (rule, match.start(), match.end())
                if key in seen:
                    continue
                seen.add(key)
                start, end = match.span()
                findings.append(
                    Finding(
                        route=route,
                        source=source,
                        layer=layer,
                        rule=rule,
                        match=match.group(0),
                        context=normalized[max(0, start - 70) : min(len(normalized), end + 90)],
                    )
                )
    return findings


def scan_html(route: str, source: str, raw_html: str) -> list[Finding]:
    """Scan raw HTML plus body-visible text, metadata, attributes, and JSON-LD."""
    findings = scan_text(route, source, "raw_html", raw_html)
    visible, jsonld_strings, metadata, attributes = extract_layers(raw_html)
    findings.extend(scan_text(route, source, "visible_text", visible))
    findings.extend(scan_text(route, source, "metadata", metadata))
    findings.extend(scan_text(route, source, "html_attribute", attributes))
    for block in jsonld_strings:
        findings.extend(scan_text(route, source, "jsonld", block))
    return findings


def load_manifest(path: Path, expected_count: int = PILOT_SIZE) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or not {"route", "source"}.issubset(rows[0]):
        raise ValueError("manifest must contain route,source columns")
    if expected_count is not None and len(rows) != expected_count:
        raise ValueError(f"expected {expected_count} manifest pages, found {len(rows)}")
    routes = [row["route"] for row in rows]
    sources = [row["source"] for row in rows]
    if len(set(routes)) != len(routes) or len(set(sources)) != len(sources):
        raise ValueError("manifest routes and source files must be unique")
    return rows


def _scan_remote_page(base_url: str, row: dict[str, str], timeout: int) -> PageResult:
    url = urljoin(base_url.rstrip("/") + "/", row["route"].lstrip("/"))
    request = Request(url, headers={"User-Agent": "EU-P0-Tariff-Audit/1.0"})
    try:
        with urlopen(request, timeout=timeout) as response:
            status = response.status
            body = response.read().decode("utf-8", errors="replace")
            final_url = response.geturl()
    except HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        status = error.code
        final_url = error.geturl()
    except (URLError, TimeoutError, OSError) as error:
        return PageResult(row["route"], row["source"], None, None, (), str(error))
    findings = scan_html(row["route"], row["source"], body)
    if status != 200:
        findings.append(Finding(row["route"], row["source"], "http", "http_status", str(status), final_url))
    return PageResult(row["route"], row["source"], status, final_url, tuple(findings))


def scan_manifest_local(root: Path, rows: list[dict[str, str]]) -> list[PageResult]:
    results: list[PageResult] = []
    for row in rows:
        path = (root / row["source"]).resolve()
        if root.resolve() not in path.parents:
            results.append(PageResult(row["route"], row["source"], None, None, (), "source path escapes root"))
            continue
        try:
            raw = path.read_text(encoding="utf-8", errors="replace")
        except OSError as error:
            results.append(PageResult(row["route"], row["source"], None, None, (), str(error)))
            continue
        results.append(PageResult(row["route"], row["source"], 200, None, tuple(scan_html(row["route"], row["source"], raw))))
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="local source root (default: repository root)")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST, help="CSV with route,source columns")
    parser.add_argument("--base-url", help="scan live public pages at this deployment origin instead of local files")
    parser.add_argument("--timeout", type=int, default=20, help="per-page HTTP timeout when --base-url is set")
    parser.add_argument("--workers", type=int, default=8, help="parallel HTTP workers when --base-url is set")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args(argv)
    try:
        rows = load_manifest(args.manifest)
    except (OSError, ValueError) as error:
        print(f"MANIFEST ERROR: {error}", file=sys.stderr)
        return 2

    if args.base_url:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
            results = list(pool.map(lambda row: _scan_remote_page(args.base_url, row, args.timeout), rows))
    else:
        results = scan_manifest_local(args.root, rows)

    findings = [finding for result in results for finding in result.findings]
    errors = [result for result in results if result.error]
    if args.json:
        payload = {
            "manifest_pages": len(rows),
            "scanned_pages": sum(result.status == 200 for result in results),
            "errors": [asdict(result) | {"findings": [asdict(f) for f in result.findings]} for result in errors],
            "findings": [asdict(finding) for finding in findings],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        by_layer: dict[str, int] = {}
        by_rule: dict[str, int] = {}
        for finding in findings:
            by_layer[finding.layer] = by_layer.get(finding.layer, 0) + 1
            by_rule[finding.rule] = by_rule.get(finding.rule, 0) + 1
        print(f"PILOT={len(rows)} HTTP_OR_FILE_OK={sum(result.status == 200 for result in results)} ERRORS={len(errors)} FINDINGS={len(findings)}")
        print("BY_LAYER=" + json.dumps(by_layer, sort_keys=True))
        print("BY_RULE=" + json.dumps(by_rule, sort_keys=True))
        for result in errors:
            print(f"ERROR {result.route} [{result.source}]: {result.error}")
        for finding in findings:
            print(f"{finding.route} [{finding.source}] {finding.layer}/{finding.rule}: {finding.context}")

    return 1 if findings or errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
