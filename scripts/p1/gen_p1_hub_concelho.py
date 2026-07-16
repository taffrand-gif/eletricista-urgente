#!/usr/bin/env python3
"""SPEC P1 §6 Variante A — bloc de differenciation hub-concelho money
SPEC §5 contrat d'injection ; §9 NAP/service ; §11.1-5 gate.

Usage:
  python3 /tmp/eu_p1_render.py [--slug <concelho_slug>] [--apply]
  sans --apply : dry-run, imprime le bloc
  avec --apply : patche concelhos/<slug>.html en place du bloc Variante A
"""
import json, re, os, sys, argparse, unicodedata
from pathlib import Path

DOMAIN = 'https://eletricista-urgente.pt'
NAP_DISPLAY = '+351 932 321 892'
NAP_TEL = '+351****1892'
PILIER_DEFAULT = '/top-10-razoes-contratar-eletricista'  # URL propre existente

def norm(s):
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return s.lower()

def slugify_local(name):
    s = unicodedata.normalize('NFD', name)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = s.lower().replace(' ', '-').replace("'", '')
    s = re.sub(r'[^a-z0-9\-]', '', s)
    s = re.sub(r'-+', '-', s).strip('-')
    return s

def lookup_zone(village_name, precos):
    """SPEC §1/§11.4 : zone uniquement si lookup exact/normalisé unique sans ambiguïté."""
    # Exact match
    if village_name in precos:
        return precos[village_name]
    # Casefold
    cf = village_name.casefold()
    hits = [v for k,v in precos.items() if k.casefold()==cf]
    if len(hits)==1:
        return hits[0]
    if len(hits)>1:
        return None  # ambigu
    # Norm unique
    n = norm(village_name)
    hits = [v for k,v in precos.items() if norm(k)==n]
    if len(hits)==1:
        return hits[0]
    return None  # ambigu ou absent

# SPEC §1: « concelhos[].zone et precos-zonas zone discordent pour 16 noms » — donc on refuse la fusion silencieuse.
# On utilise uniquement precos-zonas pour la zone (plus restrictif). On N'AFFICHE PAS la zone concelhos.
# SPEC §6 « zone seulement si la source de zone est cohérente » → par coherence, on n'inclut pas la zone si elle n'est pas source unique.

def render_block(c, villages, precos_zonas):
    """Render le bloc Variante A pour un concelho donné."""
    # Service KV page = eletricista (CF EU whitelist §1)
    service_label = 'Eletricista urgente'
    service_kw = 'curto-circuito ou falha de energia'

    # 1) H2 answer-first
    h2 = f'{service_label} em {c["name"]}: informação clara antes do contacto'

    # 2) Phrase factuelle
    district = c['district']
    rkm_val = c.get('route_km')
    rkm_str = f'{rkm_val:g} km' if rkm_val is not None else None
    if rkm_str:
        phrase = (
            f'Para {service_kw} em {c["name"]}, a nossa equipa começa por esclarecer o problema, a zona aplicável e o que pode ser feito. '
            f'{c["name"]} pertence ao distrito de {district}. '
            f'A ficha rodoviária disponível regista {rkm_str} até ao ponto de referência operacional; este dado descreve a rota, não é uma promessa de tempo de resposta.'
        )
    else:
        phrase = (
            f'Para {service_kw} em {c["name"]}, a nossa equipa começa por esclarecer o problema, a zona aplicável e o que pode ser feito. '
            f'{c["name"]} pertence ao distrito de {district}. '
            f'A ficha rodoviária não está preenchida para este concelho no momento.'
        )

    # 3) Price block — BLOQUÉ (§1, §11.4 — préséance zones non tranchée)
    # SPEC §5 « price_block uniquement si resolver retourne une preuve; sinon absence explicite, jamais un montant de secours »
    price_block = '<!-- price_block BLOQUÉ : préséance concelhos.json vs precos-zonas.json non tranchée par P0bis. Affichage prix retiré en attendant décision. -->'

    # 4) Méthode/diagnostic — paragraphe neutre, sans chantier inventé (§11 R11)
    diagnostic = (
        'Explicamos o diagnóstico e o trabalho necessário antes de qualquer intervenção. '
        'Não publicamos moradas privadas, testemunhos, obras ou pontos comerciais que não estejam confirmados por uma fonte pública. '
        'Quando a informação local não existe na base, mantemos o texto factual e curto.'
    )

    # 5) Village count + intro para os villages
    village_count = len(villages)
    intro_villages = (
        f'O concelho reúne {village_count} localidades listadas na base atual. '
        f'Consulte as páginas de localidade diferenciadas quando existirem; cada uma conduz para este hub, sem criar uma combinação artificial entre serviço e todas as aldeias.'
    )

    # 6) CTA NAP
    cta = (
        f'Contacte-nos pelo {NAP_DISPLAY} para descrever os sintomas e receber orientação sobre o próximo passo. '
        f'A nossa equipa responde com linguagem simples, preço transparente e sem uma morada privada publicada.'
    )

    # 7) Liens hub → villages + pilier
    # SPEC §6 « 3-8 pages village réellement disponibles » — condition: link dest doit exister
    # On a 0 village page /eletricista-<slug>.html sur disque. Donc AUCUN village link !
    # SPEC §6 dit aussi « lier vers une page absente » est interdit
    # Solution: lister les 6 premiers villages SANS lien (texte + km), conformément aux bonnes pratiques (la table bairros existante), pas de lien mort
    villages_lines = []
    for v in villages[:6]:
        # sans lien — village page n'existe pas
        villages_lines.append(f' <li>{v["name"]} — {v["km"]} km (dados de base, sem página dedicada por enquanto)</li>')
    villages_html = '\n'.join(villages_lines) if villages_lines else ' <li>(sem localidades na base por enquanto)</li>'

    nav_html = f'''<nav aria-label="Villages servidos e pilier">
 <h3>Localidades próximas do centro operacional</h3>
 <p>Lista factual baseada em data/localidades.json. Sem moradas privadas, sem promesses de délai:</p>
 <ul>
{villages_html}
 </ul>
 <h3>Pilier recomendado</h3>
 <ul>
  <li><a href="{DOMAIN}{PILIER_DEFAULT}">Top 10 razões para contratar um eletricista — Nur Reparos</a></li>
 </ul>
</nav>'''

    # Compose block
    block = f'''<section class="p1-diferenciacao p1-hub-concelho" data-source="agentes.md §6 Variante A">
 <h2>{escape_html(h2)}</h2>
 <p>{escape_html(phrase)}</p>
 <div class="price-transparency">{price_block}</div>
 <p>{escape_html(diagnostic)}</p>
 <p>{escape_html(intro_villages)}</p>
 <p>{escape_html(cta)}</p>
 {nav_html}
</section>'''

    return block

def escape_html(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--slug', default='macedo-de-cavaleiros')
    parser.add_argument('--apply', action='store_true', help='Apply the patch on disk')
    parser.add_argument('--all', action='store_true', help='Apply to all 33 concelhos')
    args = parser.parse_args()

    concelhos = json.load(open('data/concelhos.json'))
    localidades = json.load(open('data/localidades.json'))
    precos = json.load(open('precos-zonas.json'))

    slugs_to_apply = []
    if args.all:
        slugs_to_apply = [c['slug'] for c in concelhos]
    elif args.slug:
        slugs_to_apply = [args.slug]
    else:
        slugs_to_apply = ['macedo-de-cavaleiros']

    summary = {}
    for slug in slugs_to_apply:
        c = next((c for c in concelhos if c['slug']==slug), None)
        if not c:
            print(f"  SKIP {slug}: not in concelhos.json")
            continue
        villages = localidades.get(slug, [])
        block = render_block(c, villages, precos)

        # Word count (rough)
        text = re.sub(r'<[^>]+>', ' ', block)
        text = re.sub(r'\s+', ' ', text).strip()
        words = re.findall(r'\b[a-zà-ÿA-Z0-9]+\b', text)
        unique_words = set(w.lower() for w in words)

        target = f'concelhos/{slug}.html'
        if not os.path.exists(target):
            print(f"  SKIP {slug}: no {target} on disk")
            continue

        if not args.apply:
            print(f"\n=== DRY-RUN {slug} ({len(words)} words, {len(unique_words)} uniques) ===")
            print(block[:800] + ('...' if len(block)>800 else ''))
            continue

        # Apply: inject block before <footer or <div class="cta"> finale
        with open(target) as f:
            html = f.read()
        # Find insertion point: just before <footer> tag
        m = re.search(r'\n(<footer[\s>])', html)
        if not m:
            # fallback: before <div class="cta"> (just before </body>)
            m = re.search(r'(<div class="cta">)', html)
        if not m:
            print(f"  ABORT {slug}: no insertion anchor found")
            continue
        insertion_pos = m.start()
        before = html[:insertion_pos]
        after = html[insertion_pos:]
        new_html = before.rstrip() + '\n\n' + block + '\n\n' + after

        with open(target, 'w') as f:
            f.write(new_html)
        print(f"  APPLIED {slug}: {len(words)} words / {len(unique_words)} uniques")
        summary[slug] = (len(words), len(unique_words))

    if args.apply and summary:
        print(f"\nSummary patches: {len(summary)} pages patched")

if __name__ == '__main__':
    main()
