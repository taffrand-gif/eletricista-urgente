#!/usr/bin/env python3
"""
Inject 'Aldeias e freguesias servidas' section into concelhos/*.html.

Doctrine:
- Each concelhos/<slug>.html lists ITS villages/<concelho>-*.html existing on main.
- Source-of-truth: filesystem (villages/ folder) — déduit par préfixe slug.
- Renfort SOT: data/localidades.json (noms canoniques avec accents).
- Renfort title: villages/<slug>.html <title> (Eletricista Urgente <Name> ...).
- Ancres = nom du village (clean). Liens = /villages/<slug>.
- Aucune invention : si village existe sur disque, on le liste ; sinon on l'ignore.
- 21 concelhos sans villages publiés ne sont pas touchés.
"""
import os
import re
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path('/tmp/eu-hub-villages')

# ---------- 1. Build village → concelho mapping (filesystem prefix)
villages = sorted(p.stem for p in (ROOT / 'villages').glob('*.html'))
concelhos_slugs = sorted(p.stem for p in (ROOT / 'concelhos').glob('*.html'))

# group by longest-matching prefix
groups = defaultdict(list)
for v in villages:
    matches = [c for c in concelhos_slugs if v == c or v.startswith(c + '-')]
    if not matches:
        raise SystemExit(f'Village orphelin: {v}')
    c = max(matches, key=len)
    groups[c].append(v)

# ---------- 2. Build canonical name lookup
with open(ROOT / 'data' / 'localidades.json') as f:
    sot = json.load(f)

# Title parsing
def title_name(slug):
    f = ROOT / 'villages' / f'{slug}.html'
    if not f.exists():
        return None
    content = f.read_text(encoding='utf-8', errors='ignore')
    m = re.search(r'<title>([^<]+)</title>', content)
    if not m:
        return None
    m2 = re.match(r'Eletricista Urgente (.+?) \(([^)]+)\)', m.group(1))
    if not m2:
        return None
    return m2.group(1)


def village_name(concelho, village_slug):
    """Return canonical village name with accents/uppercase as in SOT or title."""
    suffix = village_slug[len(concelho) + 1:] if village_slug.startswith(concelho + '-') else village_slug
    # 1) SOT
    sot_names = {x['name'].lower().replace(' ', '-'): x['name'] for x in sot.get(concelho, [])}
    if suffix in sot_names:
        return sot_names[suffix]
    # 2) title
    tn = title_name(village_slug)
    if tn:
        return tn
    # 3) Fallback: title case from slug (should not happen)
    return suffix.replace('-', ' ').title()


# ---------- 3. Build the HTML block
def build_section(concelho, village_slugs):
    parts = []
    parts.append('\n<h2 role="heading" aria-level="2">Aldeias e freguesias servidas</h2>')
    parts.append(f'<p>A nossa equipa cobre {len(village_slugs)} aldeias e freguesias do concelho de {concelho_name(concelho)} com página dedicada. Cada aldeia mantém o NAP-minimal (zona tarifária, deslocação confirmada por telefone) e conduz a este hub para o serviço completo:</p>')
    parts.append('<p>')
    links = []
    for v in sorted(village_slugs):
        name = village_name(concelho, v)
        links.append(f'<a href="/villages/{v}">{name}</a>')
    parts.append(', '.join(links) + '.')
    parts.append('</p>')
    return '\n'.join(parts) + '\n'


def concelho_name(slug):
    """Return the display name of a concelho (capitalised, from SOT or title-case from slug)."""
    for c in sot.get(slug, []) if False else []:
        return c.get('name')
    # Lookup concelhos.json
    with open(ROOT / 'data' / 'concelhos.json') as f:
        cs = json.load(f)
    for c in cs:
        if c.get('slug') == slug:
            return c['name']
    return slug.replace('-', ' ').title()


# ---------- 4. Inject after the "Bairros servidos" table
def inject(path, section_html):
    content = path.read_text(encoding='utf-8', errors='ignore')
    if 'Aldeias e freguesias servidas' in content:
        return False, 'already_present'
    # Find "Bairros servidos" h2
    m = re.search(r'<h2[^>]*>Bairros servidos no concelho de [^<]+</h2>.*?</table>', content, re.DOTALL)
    if not m:
        return False, 'no_bairros_table'
    insert_at = m.end()
    # Insert section with blank line separation
    new_content = content[:insert_at] + '\n' + section_html + content[insert_at:]
    path.write_text(new_content, encoding='utf-8')
    return True, 'ok'


def main():
    touched = 0
    skipped = 0
    report = []
    for c in sorted(concelhos_slugs):
        vs = groups.get(c, [])
        path = ROOT / 'concelhos' / f'{c}.html'
        if not vs:
            skipped += 1
            report.append((c, 0, 'no_villages', path))
            continue
        section = build_section(c, vs)
        ok, status = inject(path, section)
        if ok:
            touched += 1
        report.append((c, len(vs), status, path))
    print(f'touched: {touched}, skipped_no_villages: {skipped}')
    print(f'total villages linked: {sum(len(v) for v in groups.values())}')
    for c, n, st, p in report:
        print(f'  {c:<32} {n:>3} {st}')


if __name__ == '__main__':
    main()
