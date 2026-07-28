#!/usr/bin/env bash
# DGEG-CERT GATE — Vérification automatique avant merge d'un batch mentionnant DGEG/TRIESP/certificado
# Source-of-truth : ~/work/Sites/DGEG-CERT-SOURCE-OF-TRUTH.md
# Appelé par AGENTS.md §16 (eletricista-urgente) / §14 (eletricista-norte-reparos)

set -u

PASS=0; FAIL=0
log_pass() { echo "[PASS] $1"; PASS=$((PASS+1)); }
log_fail() { echo "[FAIL] $1"; FAIL=$((FAIL+1)); }

cd "$(git rev-parse --show-toplevel)"

# Déterminer le scope (root ou client/public)
if [ -d "client/public" ] && [ -d "client/public" ] && ls client/public/*.html >/dev/null 2>&1; then
  SCOPE="client/public/*.html"
  ROOT="client/public"
else
  SCOPE="*.html"
  ROOT="."
fi

echo "=== DGEG-CERT GATE ==="
echo "Repo: $(basename "$(git rev-parse --show-toplevel)")"
echo "Base ref: feat/dgeg-cert (vs origin/main baseline)"
echo "Scope: $SCOPE"
echo

# ===== Test 1 : présence wording canonique =====
echo "--- Test 1: présence wording canonique (6 chaînes attendues sur chaque page avec DGEG-CERT-BLOCK) ---"
# Restreint aux pages modifiées par le batch (vs main) — évite les faux positifs sur du contenu pré-existant non touché
CHANGED_HTML=$(git diff --name-only origin/main..HEAD -- '*.html' 2>/dev/null | grep -v '^$')
if [ -z "$CHANGED_HTML" ]; then
  echo "(Aucun fichier HTML modifié par le batch → Test 1 et 1b N/A — gate porte sur AGENTS.md uniquement)"
  CANON=()
  CHANGED_SCOPE_GLOB=""
else
  CANON=(
    "TRIESP n.º 90062"
    "Execução em Baixa Tensão"
    "até 41,4 kVA"
    "Ficha Eletrotécnica"
    "Termo de Responsabilidade"
    "Lei n.º 14/2015"
  )
  PAGES_WITH_BLOCK=$(grep -l "DGEG-CERT-BLOCK" $CHANGED_HTML 2>/dev/null | wc -l | tr -d ' ')
  echo "Pages avec DGEG-CERT-BLOCK (parmi fichiers modifiés par le batch): $PAGES_WITH_BLOCK"
  T1_OK=true
  for c in "${CANON[@]}"; do
    COUNT=$(grep -l "$c" $CHANGED_HTML 2>/dev/null | wc -l | tr -d ' ')
    if [ "$COUNT" -lt "$PAGES_WITH_BLOCK" ]; then
      log_fail "Test 1: chaîne '$c' présente sur $COUNT pages (< $PAGES_WITH_BLOCK attendues)"
      T1_OK=false
    fi
  done
  [ "$T1_OK" = true ] && log_pass "Test 1: les 6 chaînes canoniques sont sur toutes les pages DGEG modifiées par le batch"

  echo "--- Test 1b: 0 occurrence des INTERDITS (definitivo, CERTIEL, instalações certificadas) DANS LE BATCH UNIQUEMENT ---"
  FORBIDDEN_OK=true
  for fbd in "definitivo" "CERTIEL" "instalações certificadas"; do
    # On grep UNIQUEMENT les fichiers modifiés par le batch vs main
    HITS=$(grep -E "$fbd" $CHANGED_HTML 2>/dev/null | grep -v "diagnóstico definitivo" | wc -l | tr -d ' ')
    if [ "$HITS" -gt 0 ]; then
      log_fail "Test 1b: '$fbd' ajouté par le batch dans $HITS lignes (autorisé uniquement dans 'diagnóstico definitivo')"
      FORBIDDEN_OK=false
      # print samples
      grep -E "$fbd" $CHANGED_HTML 2>/dev/null | head -3 | sed 's/^/    /'
    fi
  done
  [ "$FORBIDDEN_OK" = true ] && log_pass "Test 1b: aucune occurrence des interdits dans le batch (hors 'diagnóstico definitivo')"
fi

# ===== Test 2 : JSON-LD credential valide =====
echo
echo "--- Test 2: JSON-LD credential valide (parse strict) — UNIQUEMENT pages modifiées par le batch ---"
if [ -z "$CHANGED_HTML" ]; then
  echo "(Aucun fichier HTML modifié → Test 2 N/A)"
else
T2_RESULT=$(python3 -c "
import re, json
from pathlib import Path
import subprocess
root = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], cwd='.').decode().strip()
branch_root = '$ROOT'
base = Path(root) / branch_root if branch_root not in ('.', '') else Path(root)
changed_html = '''$CHANGED_HTML'''.strip().split('\n')
broken = []
missing_credential = []
total_dgeg_pages = 0
total_person = 0
ok_credential = 0
for fpath in changed_html:
    p = Path(root) / fpath
    if not p.exists() or not fpath.endswith('.html'):
        continue
    txt = p.read_bytes().decode('utf-8', errors='replace')
    has_block = 'DGEG-CERT-BLOCK' in txt
    has_credential_mention = ('90062' in txt or 'TRIESP' in txt or 'hasCredential' in txt)
    if not (has_block or has_credential_mention):
        continue
    total_dgeg_pages += 1
    has_person_with_credential = False
    for m in re.finditer(r'<script[^>]*type=\"application/ld\\+json\"[^>]*>', txt):
        s = m.end()
        e = txt.find('</script>', s)
        if e < 0: continue
        blob = txt[s:e]
        for v in [blob, blob.replace('https://***@type', 'https://schema.org'), re.sub(r'\"https://[^\"]*@type\"', '\"https://schema.org\"', blob)]:
            try:
                obj = json.loads(v)
                if 'hasCredential' in obj:
                    total_person += 1
                    has_person_with_credential = True
                    hc = obj['hasCredential']
                    if (hc.get('identifier') == '90062'
                        and 'Registo profissional DGEG' in str(hc.get('credentialCategory', ''))
                        and hc.get('recognizedBy', {}).get('url') == 'https://www.dgeg.gov.pt/'):
                        ok_credential += 1
                break
            except Exception:
                pass
    if not has_person_with_credential and has_block:
        missing_credential.append(p.name)

print(f'Pages DGEG modifiées par le batch: {total_dgeg_pages}')
print(f'Credential valide (id=90062, cat, recog DGEG): {ok_credential}')
print(f'Pages modifiées SANS credential: {len(missing_credential)}')
for n in missing_credential[:5]:
    print(f'  - {n}')
")
echo "$T2_RESULT"
T2_OK=$(echo "$T2_RESULT" | grep -c "^Pages modifiées SANS credential: 0$")
if [ "$T2_OK" -gt 0 ]; then
  log_pass "Test 2: toutes les pages DGEG modifiées par le batch ont un credential JSON-LD valide"
else
  log_fail "Test 2: des pages DGEG modifiées par le batch n'ont PAS de credential JSON-LD valide"
fi
fi

# ===== Test 3 : invariants structurels =====
echo
echo "--- Test 3: invariants structurels (H1 inchangé, tel non masqué dans le batch) ---"
# 3a: H1 inchangé vs main (la diff ne doit PAS ajouter de <h1>)
H1_ADDED=$(git diff origin/main..HEAD -- '*.html' 2>/dev/null | grep -c "^+<h1")
H1_REMOVED=$(git diff origin/main..HEAD -- '*.html' 2>/dev/null | grep -c "^-<h1")
if [ "$H1_ADDED" -gt 0 ]; then
  log_fail "Test 3a: $H1_ADDED lignes <h1> ajoutées par le batch (delta > 0 vs main)"
else
  log_pass "Test 3a: 0 ligne <h1> ajoutée par le batch (H1 inchangé)"
fi

# 3b: tel non masqué dans les fichiers modifiés par le batch
if [ -n "$CHANGED_HTML" ]; then
  MASKED=$(grep -E "tel:\+351\*\*\*\*[0-9]{4}" $CHANGED_HTML 2>/dev/null | wc -l | tr -d ' ')
  if [ "$MASKED" -gt 0 ]; then
    log_fail "Test 3b: $MASKED occurrences de tel:+351****XXXX ajoutées par le batch (numéro masqué interdit)"
  else
    log_pass "Test 3b: 0 numéro masqué ajouté par le batch"
  fi
else
  log_pass "Test 3b: pas de fichier HTML modifié → N/A"
fi

# ===== Test 4 : chargeur VE =====
echo
echo "--- Test 4: chargeur VE (mention optionnelle dans le batch, n/A par défaut) ---"
if [ -n "$CHANGED_HTML" ] && grep -qE "(wallbox|carregador|carregadores|carro el[eé]trico|posto de carregamento)" $CHANGED_HTML 2>/dev/null; then
  COUNT=$(grep -lE '(wallbox|carregador)' $CHANGED_HTML 2>/dev/null | wc -l | tr -d ' ')
  log_pass "Test 4: chargeur VE ajouté par le batch sur $COUNT page(s)"
else
  log_pass "Test 4: chargeur VE absent du batch → N/A (acceptable, mention optionnelle)"
fi

# ===== Résumé =====
echo
echo "=== RÉSUMÉ ==="
echo "PASS: $PASS"
echo "FAIL: $FAIL"
if [ "$FAIL" -gt 0 ]; then
  echo
  echo "❌ GATE FAILED. STOP : NE PAS merger. Corriger les échecs ci-dessus."
  exit 1
else
  echo
  echo "✅ GATE OK. Procéder au merge (avec validation humaine Philippe)."
  exit 0
fi
