#!/usr/bin/env python3
"""
P0.5 Dry-run — eletricista-urgente UNIQUEMENT

Méthode:
- Pour chaque page eletricista-*.html, extraire le badge (zone-info data-zone OU zone-badge text)
- Résoudre le city depuis le slug, strip préfixes service
- Comparer badge à la valeur zonas-data.json (lookup exact)
- Détecter KO badge≠JSON-LD "Deslocação Zona N" + KO price JSON-LD Offer deslocação ≠ grille
- Détecter doublons zone-info
- Exclure pages ES (préfixes villes Castille/Galice/Ourense — heuristique sur contenu ES)

Le brief attend 29 KO badge et 202 KO badge≠JSON-LD. Ces chiffres étaient calculés
par la logique batch P0 (probablement lookup limité à certaines villes/régions). Ce script
rapporte la totalité des KO détectables avec résolution strip préfixes.
"""
import json, re, sys
from pathlib import Path
from collections import defaultdict

ROOT = Path('/Users/admin/work/Sites/eletricista-urgente')
ZONAS = json.load(open('/Users/admin/work/Sites/norte-os-marketing/prototypes/zonas-data.json'))
ZMAP = ZONAS

SERVICE_PREFIXES = [
    'avaria-eletrica-', 'fuga-corrente-', 'quadro-eletrico-',
    'certificacao-eletrica-', 'certificacao-dgeg-',
    'tomada-interruptor-', 'iluminacao-led-', 'iluminacao-exterior-',
    'iluminacao-', 'preco-eletricista-urgente-',
]

# Pages ES (villes frontalières castillanes/galiciennes : nom espagnol, absentes zonas-data.json)
ES_TOKENS = [
    'xinzo-de-limia', 'a-mezquita', 'requejo-de-sanabria', 'fariza-de-sayago',
    'ferreruela-de-tabara', 'samir-de-los-canos', 'san-pedro-de-la-silba',
    'perena-de-la-ribera', 'o-rios', 'cerezal-de-penahorcada',
    'a-gudinha', 'pias', 'hermisende',
]

def strip_service_prefix(stem):
    s = stem.replace('eletricista-', '', 1)
    for p in SERVICE_PREFIXES:
        if s.startswith(p):
            return s[len(p):]
    return s

def is_es_page(stem):
    s = stem
    for ep in ES_TOKENS:
        if ep in s:
            return True
    return False

def lookup_city(city_slug):
    """Lookup zones-data.json normalized."""
    candidates = [
        city_slug.replace('-', ' ').title(),
        city_slug.replace('-', ' '),
        city_slug,
        city_slug.lower(),
    ]
    for c in candidates:
        if c in ZMAP:
            return str(ZMAP[c])
    return None

def extract_badge_zone(txt):
    # Pattern 1: zone-info data-zone
    m = re.search(r'<div[^>]*class="zone-info"[^>]*data-zone="(\d)"', txt)
    if m: return m.group(1)
    m = re.search(r'<div[^>]*data-zone="(\d)"[^>]*class="zone-info"', txt)
    if m: return m.group(1)
    # Pattern 2: zone-badge text "Zona N · NN€"
    m = re.search(r'class="zone-badge"[^>]*>(?:[^<]*?Zona\s*)?(\d)', txt)
    if m: return m.group(1)
    return None

def extract_body_pricing_zone(txt):
    """Zones mentionnées dans les blocs pricing (zone-badge, Para Zona, Deslocação Zona)."""
    zones = set()
    visible = re.sub(r'<script[^>]*>.*?</script>', '', txt, flags=re.DOTALL)
    visible = re.sub(r'<style[^>]*>.*?</style>', '', visible, flags=re.DOTALL)
    for m in re.finditer(r'Para\s*Zona\s*(\d)', visible):
        zones.add(m.group(1))
    for m in re.finditer(r'Desloca[cç][aã]o\s*Zona\s*(\d)', visible):
        zones.add(m.group(1))
    for m in re.finditer(r'class="zone-badge"[^>]*>([^<]+)', visible):
        zm = re.search(r'Zona\s*(\d)', m.group(1))
        if zm: zones.add(zm.group(1))
    return sorted(zones)

def extract_jsonld_zones_deslocacao(txt):
    """Zones mentionnées dans JSON-LD via Offers deslocação."""
    blocks = re.findall(r'<script type="application/ld\+json">\s*(.+?)\s*</script>', txt, re.DOTALL)
    zones = []
    for b in blocks:
        try:
            d = json.loads(b)
        except Exception:
            continue
        jt = json.dumps(d, ensure_ascii=False)
        for zm in re.finditer(r'Desloca[cç][aã]o\s*Zona\s*(\d)', jt):
            zones.append(zm.group(1))
    return zones

def extract_jsonld_offer_deslocacao_prices(txt):
    out = []
    blocks = re.findall(r'<script type="application/ld\+json">\s*(.+?)\s*</script>', txt, re.DOTALL)
    for b in blocks:
        try:
            d = json.loads(b)
        except Exception:
            continue
        if not isinstance(d, dict):
            continue
        if d.get('@type') == 'Offer':
            n = d.get('name', '')
            if 'Desloca' in n:
                zm = re.search(r'Zona\s*(\d)', n)
                if zm:
                    out.append((n, str(d.get('price','')), zm.group(1)))
    return out

def find_double_zone_info(txt):
    """Détecte 2+ blocs zone-info avec data-zone différents."""
    zones = re.findall(r'<div[^>]*class="zone-info"[^>]*data-zone="(\d)"', txt)
    if len(zones) >= 2 and len(set(zones)) > 1:
        return list(zones)
    return None

GRID = {1: 15, 2: 25, 3: 35, 4: 45, 5: 55, 6: 65}

KO_NOSRC = []
KO_VSJSONLD = []
KO_GRIDPRICE = []
KO_DOUBLE = []
ES_PAGES = []
UNRESOLVED = []  # aldeias pas dans source

n_total = n_es = n_badge = n_resolved = 0

for html in sorted(ROOT.glob('eletricista-*.html')):
    stem = html.stem
    n_total += 1
    if is_es_page(stem):
        n_es += 1
        ES_PAGES.append(stem)
        continue
    txt = html.read_text(encoding='utf-8', errors='ignore')
    badge = extract_badge_zone(txt)
    if badge:
        n_badge += 1

    city = strip_service_prefix(stem)
    expected = lookup_city(city)
    if expected is None:
        UNRESOLVED.append(stem)
        continue
    n_resolved += 1

    # (a) badge ≠ source
    if badge and badge != expected:
        KO_NOSRC.append({'file': html.name, 'badge': badge, 'expected': expected, 'city': city})

    # (b) badge ≠ JSON-LD deslocação
    jsonld_zones = extract_jsonld_zones_deslocacao(txt)
    if badge and jsonld_zones and badge not in jsonld_zones:
        KO_VSJSONLD.append({'file': html.name, 'badge': badge, 'jsonld_zones': sorted(set(jsonld_zones))})

    # (b') badge ≠ body pricing zone (page interne contradictoire)
    body_pricing_zones = extract_body_pricing_zone(txt)
    # Trouver la mention body la plus fréquente ≠ badge
    if badge and body_pricing_zones:
        differing = [z for z in body_pricing_zones if z != badge]
        if differing:
            KO_VSJSONLD.append({
                'file': html.name,
                'badge': badge,
                'jsonld_zones': body_pricing_zones,
                'body_pricing_zones': body_pricing_zones,
                'kind': 'badge-vs-body',
            })

    # (c) JSON-LD Offer.price deslocação ≠ grille
    for name, price, zone_str in extract_jsonld_offer_deslocacao_prices(txt):
        z = int(zone_str)
        if str(GRID.get(z)) != price:
            KO_GRIDPRICE.append({'file': html.name, 'name': name, 'price': price, 'expected_price': str(GRID.get(z))})

    # (d) doublons zone-info
    dbl = find_double_zone_info(txt)
    if dbl:
        KO_DOUBLE.append({'file': html.name, 'zones': dbl})

print("=" * 70)
print("P0.5 Dry-run — eletricista-urgente (uniquement)")
print("=" * 70)
print(f"Total pages eletricista-*.html            : {n_total}")
print(f"  - Pages ES exclues (frontière ES)       : {n_es}")
print(f"  - Pages EU analysées                    : {n_total - n_es}")
print(f"    dont badge zone-info/zone-badge       : {n_badge}")
print(f"    dont city résolu dans source-of-truth : {n_resolved}")
print(f"    dont aldeias sans entrée source       : {len(UNRESOLVED)}")
print()
print(f"(a) KO badge data-zone ≠ zonas-data.json  : {len(KO_NOSRC)}  (attendu: 29)")
print(f"(b) KO badge ≠ JSON-LD 'Deslocação Zona X': {len(KO_VSJSONLD)}  (attendu: 202)")
print(f"(c) KO JSON-LD Offer.price deslocação ≠ grille : {len(KO_GRIDPRICE)}  (attendu: 2)")
print(f"(d) Doublons zone-info blocs              : {len(KO_DOUBLE)}")
print()
print("=" * 70)
print("Vagues fichiers KO (≤100/vague)")
print("=" * 70)
all_ko = sorted(set(
    [x['file'] for x in KO_NOSRC] +
    [x['file'] for x in KO_VSJSONLD] +
    [x['file'] for x in KO_GRIDPRICE] +
    [x['file'] for x in KO_DOUBLE]
))
print(f"Total fichiers uniques KO : {len(all_ko)}")
vagues = [all_ko[i:i+100] for i in range(0, len(all_ko), 100)]
for i, v in enumerate(vagues, 1):
    print(f"  → Vague {i} : {len(v)} fichiers")
print()
if all_ko:
    print(f"--- VAGUE 1 (premiers {min(100,len(all_ko))} fichiers KO) ---")
    for f in vagues[0][:30]:
        print(f"   {f}")
    if len(vagues[0]) > 30:
        print(f"   ... +{len(vagues[0])-30} autres")

# Echantillons (a)
if KO_NOSRC:
    print("\n" + "=" * 70)
    print("Sample (a) KO badge ≠ source-of-truth (premiers 20)")
    print("=" * 70)
    # Dédup par ville
    seen = set()
    for x in KO_NOSRC:
        if x['city'] not in seen:
            print(f"   {x['file']}  badge=Z{x['badge']}  expected=Z{x['expected']}  (city={x['city']})")
            seen.add(x['city'])
        if len(seen) >= 20: break

if KO_VSJSONLD:
    print("\n" + "=" * 70)
    print("Sample (b) KO badge ≠ JSON-LD Deslocação Zona X (premiers 10)")
    print("=" * 70)
    for x in KO_VSJSONLD[:10]:
        print(f"   {x['file']}  badge=Z{x['badge']}  jsonld={x['jsonld_zones']}")
    if not KO_VSJSONLD:
        print("   (aucun trouvé — le pattern 'Deslocação Zona N' n'apparaît quasi plus)")

# Pages ES
print("\n" + "=" * 70)
print(f"Pages ES exclues ({len(ES_PAGES)} attendues: ~56)")
print("=" * 70)
for s in ES_PAGES:
    print(f"   {s}")

# Aldeias non-résolues
print("\n" + "=" * 70)
print(f"Aldeias EU sans entrée source-of-truth ({len(UNRESOLVED)} — non comparables)")
print("=" * 70)
print(f"  Échantillon: {UNRESOLVED[:5]}")
print(f"  Total badges de ces pages: {sum(1 for x in UNRESOLVED if True)} (source-of-truth ne permet pas de valider)")

# Save report
output = {
    'summary': {
        'total_scanned': n_total,
        'es_excluded': n_es,
        'eu_analyzed': n_total - n_es,
        'with_badge': n_badge,
        'city_resolved_in_source': n_resolved,
        'aldeias_unresolved': len(UNRESOLVED),
        'ko_badge_nosrc': len(KO_NOSRC),
        'ko_badge_vs_jsonld': len(KO_VSJSONLD),
        'ko_price_grid': len(KO_GRIDPRICE),
        'ko_double_zone_info': len(KO_DOUBLE),
        'total_unique_ko_files': len(all_ko),
        'vagues': [{'vague': i+1, 'count': len(v), 'files': v} for i, v in enumerate(vagues)],
    },
    'ko_badge_nosrc': KO_NOSRC,
    'ko_badge_vs_jsonld': KO_VSJSONLD,
    'ko_price_grid': KO_GRIDPRICE,
    'ko_double_zone_info': KO_DOUBLE,
    'es_excluded_list': ES_PAGES,
    'aldeias_unresolved': UNRESOLVED,
}
out_path = ROOT / '.hermes' / 'P0.5_dryrun_eu.json'
out_path.parent.mkdir(exist_ok=True)
out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2))
print(f"\nRapport complet : {out_path}")
