#!/usr/bin/env bash
# Action #3 — Re-mesure indexation EU J+5 (23/07) — RUN SEC
# ----------------------------------------------------------------------------
# Mission : reproduire la baseline J0 (18/07, 95 inspections) pour mesurer
# l'effet du deploy curto-circuito + falha-energia (17/07) et le delta post
# force-resubmit (Action #1).
#
# Doctrine verrouillée EU-INDEXATION-DIAGNOSTIC-2026-07-18 :
#   - même seed (42), même limite (45 EU + 50 CU), même script.
#   - quota Inspection API J0 = 95/2000 (4.75 %), cible J+5 ≤ 200 cumulé.
#   - toute la chaîne est dans gsc-venv (sinon ImportError).
#
# PRÉREQUIS : venv gsc-venv actif + clé ~/.hermes/gsc-key.json + READ-ONLY.
#
# CECI EST UNE PRÉPARATION : le script peut être lancé tel quel le 23/07
# sans rien merger ni toucher main. Sortie = 2 fichiers md + 1 rapport delta.
#
# Usage :
#   /Users/admin/work/Sites/gsc-venv/bin/bash tools/run-j5-remeasure.sh
# ----------------------------------------------------------------------------
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SITES_ROOT="/Users/admin/work/Sites"
GSC="${SITES_ROOT}/gsc-venv/bin/python"
AUDIT="${SITES_ROOT}/_audit/tools/index_status_sample.py"
RAW="${SITES_ROOT}/_audit/raw"
DIFF="${ROOT}/tools/diff-index-baseline.py"
DATE="$(date -u +%Y-%m-%d)"

mkdir -p "${RAW}"

if [[ ! -x "${GSC}" ]]; then
  echo "ERROR: gsc-venv introuvable à ${GSC}. Active le venv avant." >&2
  exit 1
fi
if [[ ! -f "${AUDIT}" ]]; then
  echo "ERROR: index_status_sample.py introuvable à ${AUDIT}." >&2
  exit 1
fi

echo "=== Action #3 — Re-mesure J+5 EU/CU — ${DATE} ==="
echo ""

# 1) Re-run baseline EU (45 URLs, seed 42, sitemap.xml core)
echo "[1/4] Re-run EU sitemap core (45 URLs)..."
"${GSC}" "${AUDIT}" \
  --site EU --limit 45 --sample random_seed42 \
  --output "${RAW}/INDEX-STATUS-EU-${DATE}.md"

# 2) Re-run baseline CU (50 URLs, seed 42, sitemap.xml core)
echo "[2/4] Re-run CU sitemap core (50 URLs)..."
"${GSC}" "${AUDIT}" \
  --site CU --limit 50 --sample random_seed42 \
  --output "${RAW}/INDEX-STATUS-CU-${DATE}.md"

# 3) Delta EU J0 vs J+5
echo "[3/4] Delta EU J0 vs J+5..."
"${GSC}" "${DIFF}" \
  --j0 "${RAW}/INDEX-STATUS-EU-2026-07-18.md" \
  --j5 "${RAW}/INDEX-STATUS-EU-${DATE}.md" \
  --site EU \
  --output "${ROOT}/_audit/INDEX-DELTA-EU-2026-07-18-vs-${DATE}.md"

# 4) Delta CU J0 vs J+5
echo "[4/4] Delta CU J0 vs J+5..."
"${GSC}" "${DIFF}" \
  --j0 "${RAW}/INDEX-STATUS-CU-2026-07-18.md" \
  --j5 "${RAW}/INDEX-STATUS-CU-${DATE}.md" \
  --site CU \
  --output "${ROOT}/_audit/INDEX-DELTA-CU-2026-07-18-vs-${DATE}.md"

echo ""
echo "=== Terminé. Artefacts : ==="
echo "  ${RAW}/INDEX-STATUS-EU-${DATE}.md"
echo "  ${RAW}/INDEX-STATUS-CU-${DATE}.md"
echo "  ${ROOT}/_audit/INDEX-DELTA-EU-2026-07-18-vs-${DATE}.md"
echo "  ${ROOT}/_audit/INDEX-DELTA-CU-2026-07-18-vs-${DATE}.md"
echo ""
echo "Lecture des deltas : ouvrir les 2 fichiers *_vs_${DATE}.md"
echo "Verdict heuristique automatique (diff-index-baseline.py) :"
echo "  Cause (d) confirmé = INDEXED Δ ≥ +6 ET UNKNOWN Δ ≤ -3"
echo "  Cause (b) priorité = INDEXED Δ ≤ +1 → merger PR #4 distritos"
echo "  Sinon → mix (d)+(a) → préparer Action #5 PR édit H1"
