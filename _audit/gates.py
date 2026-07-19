#!/usr/bin/env python3
"""
Gates:
1) count liens ajoutés vs count villages
2) tel masqué 0 (constante 932321892 si besoin — jamais copier le vrai en clair)
3) claims 0 — aucun "garantimos"/"X anos experiência"/etc.
"""
import re
import os
from pathlib import Path
from collections import defaultdict

ROOT = Path('/tmp/eu-hub-villages')

# Gate 1 — count
new_links_per_hub = {}
for f in sorted((ROOT / 'concelhos').glob('*.html')):
    content = f.read_text(encoding='utf-8', errors='ignore')
    if 'Aldeias e freguesias servidas' not in content:
        continue
    # extract the section: from h2 to next h2/section
    m = re.search(r'<h2[^>]*>Aldeias e freguesias servidas</h2>(.*?)<h2|<section', content, re.DOTALL)
    if not m:
        print(f'WARN: section introuvable dans {f.name}')
        continue
    section = m.group(1)
    # count <a href="/villages/..."> anchors
    links = re.findall(r'<a href="/villages/([^"]+)"', section)
    new_links_per_hub[f.stem] = links

total_links = sum(len(v) for v in new_links_per_hub.values())
all_linked_villages = set()
for vs in new_links_per_hub.values():
    all_linked_villages.update(vs)

# Compare to filesystem villages
fs_villages = sorted(p.stem for p in (ROOT / 'villages').glob('*.html'))
fs_set = set(fs_villages)

missing_in_fs = all_linked_villages - fs_set
missing_in_links = fs_set - all_linked_villages

print(f'=== GATE 1: count ===')
print(f'fichiers villages/ sur disque : {len(fs_villages)}')
print(f'liens villages ajoutés        : {total_links}')
print(f'unique villages liés           : {len(all_linked_villages)}')
print(f'match                          : {len(fs_villages) == total_links}')
print(f'orphelins (liés mais pas FS)  : {len(missing_in_fs)}')
print(f'manquants (FS mais pas liés)   : {len(missing_in_links)}')

if missing_in_fs:
    for v in sorted(missing_in_fs):
        print(f'  ⚠ lié mais pas de fichier: {v}')
if missing_in_links:
    for v in sorted(missing_in_links):
        print(f'  ⚠ FS mais pas lié: {v}')

print()
print(f'=== Distribution par hub ===')
for c, vs in sorted(new_links_per_hub.items()):
    print(f'  {c:<28} {len(vs):>3}')

# Gate 2 — tel masqué 0
print()
print(f'=== GATE 2: tel masqué ===')
# tel masqué = href="tel:+351····NNNN"
masked_pattern = re.compile(r'tel:\+351\*{4}\d{4}')
unmasked_pattern = re.compile(r'tel:\+351\s*\d{3}\s*\d{3}\s*\d{3}')  # full E.164 visible
masked_count = 0
unmasked_count = 0
for f in (ROOT / 'concelhos').glob('*.html'):
    content = f.read_text(encoding='utf-8', errors='ignore')
    masked_count += len(masked_pattern.findall(content))
    unmasked_count += len(unmasked_pattern.findall(content))
print(f'tel:+351····NNNN (masked) : {masked_count} (attendu ≥ 1 par hub)')
print(f'tel:+351 932 321 892 (unmasked, interdit) : {unmasked_count}')

# Gate 3 — claims 0
print()
print(f'=== GATE 3: claims ===')
# Patterns interdits (depuis le brief et la doctrine R12/R145/M17)
forbidden_patterns = [
    (r'\b(garantimos|garantimos\s+atendimento|garantimos\s+que|garantimos\s+resposta)\b', 'garantimos'),
    (r'\b(mais de \d+\s*anos?)\b', 'mais de X anos'),
    (r'\b(empresa registada|empresa com mais)\b', 'empresa registada'),
    (r'\b(equipa de \d+|equipa com \d+)\b', 'equipa numerica'),
    (r'\b(disponibilidade imediata|resposta imediata|chegamos em \d+ min)\b', 'promessas immediates'),
    (r'\b(atendimento(?: imediato)?(?: em| dentro de)? \d+\s*min)', 'promesse minutes'),
]
total_claims = 0
# restrict search to newly-injected section
for f, vs in new_links_per_hub.items():
    content = (ROOT / 'concelhos' / f'{f}.html').read_text(encoding='utf-8', errors='ignore')
    m = re.search(r'<h2[^>]*>Aldeias e freguesias servidas</h2>.*?(?=<h2|<section)', content, re.DOTALL)
    if not m:
        continue
    section = m.group(0)
    for pat, label in forbidden_patterns:
        matches = re.findall(pat, section, re.IGNORECASE)
        if matches:
            print(f'  ⚠ {f}: {label} ({len(matches)})')
            total_claims += len(matches)
print(f'claims interdits (sections injectées) : {total_claims}')
