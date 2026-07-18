#!/usr/bin/env python3
"""
Compare deux baselines d'indexation GSC (J0 vs J+5) et sort un rapport de delta.

Doctrine verrouillée (leçon #418 + EU-INDEXATION-DIAGNOSTIC-2026-07-18) :
  - Lecture seule.
  - Pas d'invention de seuils magiques : utilise les KPI cibles du diagnostic
    §5 (Cible J+5 et Cible J+12).
  - Aligne les URLs par chemin canonique (sans trailing slash, host lowercase).
  - Sortie Markdown + verdict global (cause d vs cause a vs cause b).

Usage :
    python3 tools/diff-index-baseline.py \
        --j0 _audit/raw/INDEX-STATUS-EU-2026-07-18.md \
        --j5 _audit/raw/INDEX-STATUS-EU-2026-07-23.md \
        --output _audit/INDEX-DELTA-EU-2026-07-18-vs-23.md

Notes :
  - Le script parse le format markdown produit par `index_status_sample.py`.
  - Aucun contact réseau.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

# KPI cibles du diagnostic §5 — verrouillés
KPI = {
    "indexed_j5_min": 18,        # baseline 12, cible J+5
    "indexed_j12_min": 27,       # cible J+12 (60 % de 45)
    "discovered_j5_max": 12,     # baseline 18, cible J+5
    "unknown_j5_max": 10,        # baseline 15, cible J+5
    "districts_indexed_j5_min": 4,  # 2/6 → 4/6
    "curto_falha_links_indexed_min": 5,  # ≥ 5/8 concelhos linkés curto+falha
}


def normalize_path(url: str) -> str:
    """Canonise le chemin pour aligner J0 et J+5."""
    parsed = urlparse(url)
    host = (parsed.netloc or "").lower()
    path = parsed.path or "/"
    if len(path) > 1 and path.endswith("/"):
        path = path[:-1]
    return f"{host}{path}"


def parse_baseline_md(path: Path) -> dict[str, str]:
    """Parse une baseline md et retourne {path: verdict}.

    Format verrouillé par `index_status_sample.py` (leçon #418) :
        | URL | Propriété GSC | **INDEXED** | lastCrawlTime | Canonical | coverageState |
        | URL | Propriété GSC | **DISCOVERED** | — | — | Discovered - currently not indexed |
        | URL | Propriété GSC | **NEUTRAL** | — | — | URL is unknown to Google |

    Le verdict est en colonne 2, dans `**XXX**`. On classifie NEUTRAL selon la
    colonne coverageState (colonne 5).
    """
    text = path.read_text(encoding="utf-8")
    out: dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) < 6:
            continue
        if not cells[0].startswith("http"):
            continue  # ligne d'en-tête ou de séparation
        url = cells[0]
        verdict_raw = cells[2].upper().replace("*", "").strip()
        coverage = cells[5].lower()
        if "INDEXED" in verdict_raw and "NOT" not in verdict_raw:
            verdict = "INDEXED"
        elif "DISCOVERED" in verdict_raw:
            verdict = "DISCOVERED"
        elif "NEUTRAL" in verdict_raw:
            if "unknown to google" in coverage:
                verdict = "UNKNOWN"
            elif "noindex" in coverage:
                verdict = "NOINDEX"
            elif "canonical tag" in coverage:
                verdict = "CANONICALIZED"
            else:
                verdict = "NEUTRAL_OTHER"
        elif "CRAWLED" in verdict_raw and "NOT" in verdict_raw:
            verdict = "CRAWLED_NOT_INDEXED"
        else:
            verdict = "UNKNOWN"
        out[normalize_path(url)] = verdict
    return out


def count_by_verdict(baseline: dict[str, str]) -> Counter:
    return Counter(baseline.values())


def classify_cause(indexed_delta: int, unknown_delta: int) -> str:
    """Règle de décision verrouillée §5."""
    if indexed_delta >= 6 and unknown_delta <= -3:
        return (
            "Cause (d) « déployé trop récent » CONFIRMÉE — basculer sur la cause "
            "(a) éditoriale (Action #5) en J+12."
        )
    if indexed_delta <= 1:
        return (
            "Cause (b) « hub-and-spoke cassé » à traiter en PRIORITÉ — "
            "merger la PR #4 (distritos hub-and-spoke)."
        )
    return (
        "Cause indéterminée — ré-mesurer à J+12 (30/07). Probable mix "
        "(d) délai + (a) édit. Action #5 PR à merger."
    )


def render_markdown(j0_path: Path, j5_path: Path, report: dict) -> str:
    lines = [
        f"# Delta indexation EU — {j0_path.stem} → {j5_path.stem}",
        "",
        f"> Généré par `tools/diff-index-baseline.py` (READ-ONLY) le "
        f"{datetime.utcnow().isoformat()}Z.",
        f"> Baseline J0 : `{j0_path}`",
        f"> Baseline J+5 : `{j5_path}`",
        "",
        "## Synthèse globale",
        "",
        "| Site | INDEXED J0 | INDEXED J+5 | Δ | DISCOVERED J0 | DISCOVERED J+5 | Δ | UNKNOWN J0 | UNKNOWN J+5 | Δ |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for site, data in report["by_site"].items():
        lines.append(
            f"| {site} | {data['indexed_j0']} | {data['indexed_j5']} | "
            f"{data['indexed_delta']:+d} | {data['discovered_j0']} | "
            f"{data['discovered_j5']} | {data['discovered_delta']:+d} | "
            f"{data['unknown_j0']} | {data['unknown_j5']} | "
            f"{data['unknown_delta']:+d} |"
        )
    lines.extend(
        [
            "",
            "## KPI cibles (verrouillés diagnostic §5)",
            "",
            f"- INDEXED cible J+5 = ≥ {KPI['indexed_j5_min']} (EU)",
            f"- DISCOVERED cible J+5 = ≤ {KPI['discovered_j5_max']} (EU)",
            f"- UNKNOWN cible J+5 = ≤ {KPI['unknown_j5_max']} (EU)",
            "",
            "## Verdict heuristique",
            "",
            f"**{report['verdict']}**",
            "",
            "## URLs pivot curto-circuito + falha-energia (8 concelhos linkés)",
            "",
            "| Concelho | J0 | J+5 | Δ |",
            "|---|---|---|---|",
        ]
    )
    for slug, statuses in report["curto_falha"].items():
        lines.append(
            f"| {slug} | {statuses['j0']} | {statuses['j5']} | {statuses['delta']} |"
        )
    lines.extend(
        [
            "",
            "## URLs pivot UNKNOWN J0 à surveiller",
            "",
            "| URL | J0 | J+5 | Δ |",
            "|---|---|---|---|",
        ]
    )
    for url, statuses in report["unknown_pivot"].items():
        lines.append(
            f"| {url} | {statuses['j0']} | {statuses['j5']} | {statuses['delta']} |"
        )
    lines.extend(["", "---", "", "*— fin delta —*", ""])
    return "\n".join(lines)


# 8 concelhos linkés par curto-circuito + falha-energia (cf. diagnostic §1.2)
CURTO_FALHA_CONCELHOS = [
    "alfandega-da-fe",
    "alijo",
    "braganca",
    "carrazeda-de-ansiaes",
    "chaves",
    "macedo-de-cavaleiros",
    "miranda-do-douro",
    "mirandela",
    "vila-real",  # noqa: extra du diagnostic
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--j0", required=True, help="Baseline J0 (md)")
    parser.add_argument("--j5", required=True, help="Baseline J+5 (md)")
    parser.add_argument(
        "--site",
        default="EU",
        choices=["EU", "CU", "CNR", "ENR"],
        help="Site à analyser (défaut EU).",
    )
    parser.add_argument("--output", required=True, help="Rapport delta (md)")
    args = parser.parse_args()

    j0_path = Path(args.j0)
    j5_path = Path(args.j5)
    if not j0_path.exists() or not j5_path.exists():
        print(
            f"ERROR: baseline introuvable ({j0_path} ou {j5_path}).",
            file=sys.stderr,
        )
        return 1

    j0 = parse_baseline_md(j0_path)
    j5 = parse_baseline_md(j5_path)

    counts_j0 = count_by_verdict(j0)
    counts_j5 = count_by_verdict(j5)

    indexed_delta = counts_j5.get("INDEXED", 0) - counts_j0.get("INDEXED", 0)
    discovered_delta = counts_j5.get("DISCOVERED", 0) - counts_j0.get("DISCOVERED", 0)
    unknown_delta = counts_j5.get("UNKNOWN", 0) - counts_j0.get("UNKNOWN", 0)

    site_data = {
        "indexed_j0": counts_j0.get("INDEXED", 0),
        "indexed_j5": counts_j5.get("INDEXED", 0),
        "indexed_delta": indexed_delta,
        "discovered_j0": counts_j0.get("DISCOVERED", 0),
        "discovered_j5": counts_j5.get("DISCOVERED", 0),
        "discovered_delta": discovered_delta,
        "unknown_j0": counts_j0.get("UNKNOWN", 0),
        "unknown_j5": counts_j5.get("UNKNOWN", 0),
        "unknown_delta": unknown_delta,
    }

    # URLs pivot curto+falha (8 concelhos)
    curto_falha = {}
    for slug in CURTO_FALHA_CONCELHOS:
        candidates = [k for k in j0 if slug in k]
        if candidates:
            path = candidates[0]
            curto_falha[slug] = {
                "j0": j0.get(path, "—"),
                "j5": j5.get(path, "—"),
                "delta": (
                    "→ INDEXED"
                    if j0.get(path) != "INDEXED" and j5.get(path) == "INDEXED"
                    else "stable"
                ),
            }

    # URLs UNKNOWN J0 à surveiller
    unknown_pivot = {}
    for path, verdict in j0.items():
        if verdict == "UNKNOWN":
            unknown_pivot[path] = {
                "j0": "UNKNOWN",
                "j5": j5.get(path, "—"),
                "delta": (
                    "→ INDEXED"
                    if j5.get(path) == "INDEXED"
                    else ("→ DISCOVERED" if j5.get(path) == "DISCOVERED" else "stable")
                ),
            }

    verdict = classify_cause(indexed_delta, unknown_delta)

    report = {
        "by_site": {args.site: site_data},
        "curto_falha": curto_falha,
        "unknown_pivot": unknown_pivot,
        "verdict": verdict,
    }

    md = render_markdown(j0_path, j5_path, report)
    Path(args.output).write_text(md, encoding="utf-8")
    print(f"Rapport delta écrit dans {args.output}")
    print(f"Verdict : {verdict}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
