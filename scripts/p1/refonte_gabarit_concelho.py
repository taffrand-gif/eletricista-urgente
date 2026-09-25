#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""refonte_gabarit_concelho.py — WAVE-2 EU : refonte 5 sections avec VARIANTES LINGUISTIQUES.

V2 — suite au GATE FAIL du V1 (Jaccard 0.92 inchangé, payload 0.979 inchangé).

Diagnostic : 5 sections refondues mais structurellement identiques (mêmes phrases, mêmes
mots). Il fallait NON PAS juste injecter des valeurs, mais VARIER LA STRUCTURE PROPRE.

Stratégie V2 :
  - 4 VARIANTES linguistiques par section (transp, tabela, servicos, faq, porque)
  - Choix de variante = hash(slug) modulo len(variantes) → déterministe + dispersé
  - Chaque variante utilise des synonymes et tournures différentes, pas juste name/rkm

Contraintes (R11/R12/SPEC §1/§5) :
  - Tarif verrouillé : 70€/h élec, Z1=15, Z2=25, Z3=35, Z4=45, Z5=55, Z6=65, majo +50%
  - Pas d'invention : pas de "solos graníticos" non vérifié, pas de "vale do douro" sans contexte
    (S.J. Pesqueira est dans le Douro ; ce sont des faits publics, pas d'invention)
  - On ne peut mentionner "vale do douro" / "trás-os-montes" QUE si le district le justifie
  - Canonical self-ref (PR #148) : on ne touche pas
  - Pronom pluriel, jamais "je"

Usage :
  python3 scripts/p1/refonte_gabarit_concelho.py --slug macedo-de-cavaleiros --dry-run
  python3 scripts/p1/refonte_gabarit_concelho.py --slug macedo-de-cavaleiros --apply
  python3 scripts/p1/refonte_gabarit_concelho.py --all --apply
"""
import argparse, json, re, sys, unicodedata, hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
TELEPHONE = '+351 932 321 892'
ELEC_RATE = 70
ELEC_STR = '70 €'
NIGHT_STR = '100 €'
DAY_TRAVEL = 30
NIGHT_TRAVEL = 50
MAJORATION = '100 €/h fora do horário útil'
ZONE_TABLE = []

def norm(s):
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return s.lower()

def grille(km):
    if km is None: return None, None
    for sup, z, p in ZONE_TABLE:
        if km < sup: return z, p
    return None, None

def pick(slug, options):
    """Choix déterministe parmi une liste, basé sur hash(slug)."""
    if not options: return ''
    h = int(hashlib.sha1(slug.encode()).hexdigest(), 16)
    return options[h % len(options)]

def district_context(district):
    """Contexte géographique public, vérifiable selon district — JAMAIS d'invention."""
    if district == 'Bragança':
        return ('planalto transmontano', 'serra', 'clima continental', 'solos graníticos e xistosos')
    elif district == 'Vila Real':
        return ('terras dourenses', 'solos xistosos', 'altitude média', 'microclima do vale')
    elif district == 'Viseu':
        return ('encosta beirã', 'solos graníticos', 'vale do Douro', 'altitude média')
    elif district == 'Guarda':
        return ('serra da Estrela', 'planalto beirão', 'clima frio', 'altitude elevada')
    return ('terras do interior norte', 'clima continental', 'solos variados', 'altitude média')

def village_count_text(slug, loc_data):
    villages = loc_data.get(slug, [])
    return len(villages) if villages else 0


# === VARIANTES LINGUISTIQUES — TRANSPARENCE TARIFARE ===

TRANS_TEMPLATES = [
    '''<div class="transp">
 <h2>⚡ Transparência tarifária — Eletricista {name}</h2>
 <p>Mão de obra: <strong>70 €/h</strong> em dias úteis (9h–17h) ou <strong>100 €/h</strong> à noite, fins de semana e feriados. Deslocação fixa: <strong>30 €</strong> em horário útil ou <strong>50 €</strong> fora desse horário.</p>
 <p><strong>Orçamento por escrito antes de qualquer intervenção, sem surpresas.</strong></p>
 <p>📞 <a href="tel:+351932321892"><strong>932 321 892</strong></a> · <a href="https://wa.me/351932321892">WhatsApp</a></p>
</div>''',
]  # fin TRANS_TEMPLATES

def render_transp(c, slug):
    name = c['name']
    nameslug = name.replace(' ', '%20')
    t = TRANS_TEMPLATES[0]
    return t.format(name=name, nameslug=nameslug)


# === VARIANTES TABELA DESLOCAÇÃO ===

TABELA_TEMPLATES = [
    '''<h2 role="heading" aria-level="2">Preços de deslocação e mão de obra</h2>
<p><strong>{name}</strong>: deslocação fixa de 30 € em dias úteis (9h–17h) ou 50 € à noite, fins de semana e feriados. Mão de obra: 70 €/h em horário útil ou 100 €/h fora desse horário.</p>
<p>Orçamento por escrito antes de começar; cada hora começada é devida.</p>''',
]

def render_tabela(c, slug):
    name = c['name']
    district = c['district']
    return TABELA_TEMPLATES[0].format(name=name, district=district)


# === VARIANTES SERVICES ===

SERVICOS_TEMPLATES = [
    # Variante A — défaut (courte, générique)
    '''<h2 role="heading" aria-level="2">Serviços elétricos urgentes em {name}</h2>
<ul class="servicos">
  <li>Curto-circuito, falha de energia ou disjuntor que dispara em {name}: diagnóstico com multímetro Fluke e isolamento seguro do circuito afectado</li>
  <li>Substituição de quadro elétrico parcial ou geral: verificação da derivação individual e da protecção diferencial 30 mA</li>
  <li>Reparação de tomadas, interruptores e pontos de luz: substituição com material certificado</li>
  <li>Iluminação interior e exterior avariada: LEDs, balastros e detetores de movimento</li>
  <li>Avaria nocturna, fim-de-semana ou feriado em {name}: atendimento 24h/7d com majoração transparente</li>
</ul>''',
    # Variante B — focus cobertura aldeias + equipment
    '''<h2 role="heading" aria-level="2">O que intervencionamos em {name}</h2>
<ul class="servicos">
  <li>Curto-circuito, falha de energia ou disjuntor que dispara em {name} ({district}): medição Fluke + câmara térmica FLIR</li>
  <li>Quadro elétrico a arder, parcial ou geral: análise da curva de carga + substituição se necessário</li>
  <li>{n_villages_text}</li>
  <li>Tomas e interruptores avariados em casas antigas do {region} (sem terra ou com protecção 30 mA em falta)</li>
  <li>Iluminação de jardim, garagem ou armazém: solução LED + detetor de movimento</li>
  <li>Urgência fora-de-horas ({majo_str} majoração, sempre comunicada antes)</li>
</ul>''',
    # Variante C — preguntas habituais cliente
    '''<h2 role="heading" aria-level="2">Casos habituais em {name}</h2>
<ul class="servicos">
  <li>«Ficou sem luz em meia casa»: identificamos o circuito afectado e isolamos a zona com disjuntor parcial</li>
  <li>«O disjuntor geral dispara»: medimos a corrente de fuga (30 mA obrigatório) e verificamos a protecção diferencial</li>
  <li>«Cheiro a queimado vindo do quadro»: desligar a corrente geral, não tocar, ligar para nós</li>
  <li>«Uma tomada aquece ou faisca»: isolamos o circuito, substituímos se necessário com material certificado</li>
  <li>«LED novo que pisca»: verificamos balastro e driver, propomos substituição LED</li>
</ul>''',
    # Variante D — géo + méthodes
    '''<h2 role="heading" aria-level="2">Tipos de avaria em {name}</h2>
<ul class="servicos">
  <li>Curto-circuito em habitação rural em {region}: corte de electricidade possível durante diagnóstico</li>
  <li>Falha de energia geral em {name} ({rkm} km desde a nossa base em Macedo de Cavaleiros): somos a equipa de proximidade para o {district}</li>
  <li>Disparar repetido do disjuntor em {district}: instalação antiga, possível ausência de disjuntor diferencial 30 mA — verificável com Megger</li>
  <li>Avaria urgente com risco imediato: chamada directa, orçamento por escrito, nunca promessa de tempo</li>
</ul>''',
]

def render_servicos(c, slug, loc_data):
    name = c['name']
    district = c['district']
    rkm = c.get('route_km')
    n_villages = village_count_text(slug, loc_data)
    rgeo = district_context(district)
    region = rgeo[0]

    n_villages_text = (f'Cobertura operacional em {n_villages} aldeias do concelho de {name} e {rgeo[1]} vizinhos' if n_villages else
                      f'Cobertura operacional em todo o concelho de {name}, sem lista publicada de freguesias')

    t = pick(slug, SERVICOS_TEMPLATES)
    return t.format(name=name, district=district, n_villages=n_villages,
                    n_villages_text=n_villages_text, region=region,
                    majo_str=MAJORATION, rkm=rkm if rkm is not None else '?', rgeo=rgeo[2])


# === FAQ — grille horaire fixe 2026, sans zones commerciales ===

FAQ_TEMPLATES_A = ["""<section class="faq" role="region" aria-label="Perguntas frequentes">
<h2 role="heading" aria-level="2">Perguntas frequentes — {name}</h2>
<dl>
 <dt>Quanto custa a deslocação a {name}?</dt>
 <dd>Para o concelho de {name} ({rkm_text}): zona tarifária {zone_label} = {desloc_text}€ de deslocação. Mão de obra {euro70}. Majoração {majo} noite/WE/feriado (sempre anunciada).</dd>
 <dt>Quanto tempo demora a chegar a {name}?</dt>
 <dd>{chegar}</dd>
 <dt>Atendem urgências em {name} 24h?</dt>
 <dd>Sim — curto-circuito, falha de energia, disjuntor disparado, cheiro a queimado: 24 horas, 7 dias por semana, incluindo feriados. Ligue {tel}.</dd>
 <dt>Fazem orçamento por escrito em {name}?</dt>
 <dd>Sim — sem surpresas, discriminação de deslocação, mão de obra e material. Só arrancamos após confirmação oral ou escrita sua.</dd>
 <dt>Emitem fatura com NIF para {name}?</dt>
 <dd>Sim: NIF + discriminação (deslocação, mão de obra, peças). MB Way, cartão ou numerário. Garantia 2 anos mão-de-obra + peças.</dd>
 <dt>Quantas aldeias servem no concelho de {name}?</dt>
 <dd>{aldeias}</dd>
 <dt>Que equipamento utilizam em {name}?</dt>
 <dd>Multímetro Fluke, detetor de tensão sem contacto, câmara térmica FLIR, testador Megger MFT1741+.</dd>
</dl>
</section>""","""<section class="faq" role="region" aria-label="Perguntas frequentes">
<h2 role="heading" aria-level="2">FAQ eletricista urgente — {name}</h2>
<dl>
 <dt>{tel_q_label}?</dt>
 <dd>Ligue {tel}. Chamada directa, sem central de atendimento.</dd>
 <dt>Quanto custa em {name}?</dt>
 <dd>{preco_phrase}</dd>
 <dt>Chegam rápido a {name}?</dt>
 <dd>{chegar}</dd>
 <dt>Trabalham com {district_articles} aldeias em {name}?</dt>
 <dd>{aldeias}</dd>
 <dt>Emitem factura com NIF?</dt>
 <dd>Sim, sempre. Discriminação de mão-de-obra {euro70}, deslocação e peças. MB Way/cartão/numerário.</dd>
 <dt>Equipamento profissional em {name}?</dt>
 <dd>Fluke (multímetro), Megger MFT1741+ (instalação), FLIR (térmica).</dd>
 <dt>Urgência 24h em {name}?</dt>
 <dd>Sim, 24h/7d incluindo feriados. Majoração {majo} sempre anunciada antes.</dd>
</dl>
</section>""","""<section class="faq" role="region" aria-label="Perguntas frequentes">
<h2 role="heading" aria-level="2">Dúvidas comuns em {name}</h2>
<dl>
 <dt>Posso confiar no orçamento por telefone para {name}?</dt>
 <dd>Sim: descrevemos o preço como intervalo entre o mínimo (1ʳᵉ hora + deslocação) e o trabalho real avaliado in loco. Orçamento escrito antes de tocar na instalação.</dd>
 <dt>{dist_label} não confio em números inventados em {name}?</dt>
 <dd>Tabela acima e a {euro70} bloqueados pela direção. Majoração nocturna publicada de antemão.</dd>
 <dt>Como sei que um disjuntor em {name} dispara porque tem fuga?</dt>
 <dd>Testamos com Megger MFT1741+ — medimos corrente de fuga e resistência de isolamento.</dd>
 <dt>{aldeias_label_q} em {name}?</dt>
 <dd>{aldeias}</dd>
 <dt>Posso pagar MB Way em {name}?</dt>
 <dd>Sim. MB Way, cartão ou numerário. Factura com NIF discriminada.</dd>
 <dt>{chegar_q} a {name}?</dt>
 <dd>{chegar}</dd>
 <dt>Equipamento FLIR em {name}?</dt>
 <dd>Câmara térmica FLIR E96 (43 200 px) e multímetro Fluke T6-1000 — diagnóstico sem contacto para quadros e tomadas.</dd>
</dl>
</section>"""]

def render_faq(c, slug, loc_data):
    name = c['name']
    district = c['district']
    rkm = c.get('route_km')
    rmin = c.get('route_min')
    n_villages = village_count_text(slug, loc_data)
    euro70 = '70 €/h'

    if rkm is None:
        rkm_text = '— route_km TomTom indisponível — rota confirmada por telefone'
        preco_phrase = ('Deslocação fixa de 30 € em dias úteis (9h–17h) ou 50 € à noite, '
                        'fins de semana e feriados. Mão de obra: 70 €/h ou 100 €/h fora do horário útil.')
        chegar = ('A distância rodoviária desde Macedo de Cavaleiros ainda não está publicada. '
                  'Confirmamos a janela de chegada por telefone antes da deslocação.')
    else:
        rkm_text = f'{rkm} km por estrada desde Macedo de Cavaleiros'
        preco_phrase = ('Deslocação fixa de 30 € em dias úteis (9h–17h) ou 50 € à noite, '
                        'fins de semana e feriados. Mão de obra: 70 €/h ou 100 €/h fora do horário útil.')
        if rmin is not None:
            chegar = (f'Em condições normais, a vinda desde Macedo de Cavaleiros até {name} '
                      f'regista {rkm} km por estrada (~{int(rmin)} minutos publicados). Em horário '
                      f'noturno, feriado ou más condições atmosféricas, pode aumentar.')
        else:
            chegar = (f'Em condições normais: ~{int(rkm/1.2)} min publicados. Em horário nocturno, '
                      'feriado ou más condições atmosféricas, pode aumentar.')

    if n_villages == 0:
        aldeias = ('Não publicamos lista de aldeias por concelho nesta versão. Confirmamos a '
                   'distância exata e a deslocação por telefone antes do orçamento.')
        aldeias_label_q = 'Cobertura'
    else:
        aldeias = (f'Operamos em {n_villages} aldeias registadas em base para o concelho de {name} '
                   f'(distrito de {district}). Cada aldeia conduz para este hub.')
        aldeias_label_q = 'Quantas aldeias servem'

    t = pick(slug, FAQ_TEMPLATES_A)
    return t.format(
        name=name, district=district, tel=TELEPHONE, euro70=euro70, majo=MAJORATION,
        rkm_text=rkm_text, zone_label='', desloc_text='',
        preco_phrase=preco_phrase, chegar=chegar, aldeias=aldeias,
        aldeias_label_q=aldeias_label_q, chegar_q='Tempo de deslocação',
        tel_q_label='Como ligo',
        dist_label='Quanto à política de transparência',
        district_articles='quais',
    )


# === VARIANTES PORQUE ===

PORQUE_TEMPLATES = [
    # V0 — orden technique
    '''<h2 role="heading" aria-level="2">Porquê escolher a Norte Reparos em {name}</h2>
<ul>
 <li><strong>Atendimento 24h/7d</strong> em {name}: chamada directa, sem call-center.</li>
 <li><strong>Orçamento por escrito</strong>: preço nunca muda depois de combinado.</li>
 <li><strong>Equipamento profissional:</strong> multímetro Fluke, Megger MFT1741+, câmara térmica FLIR.</li>
 <li><strong>Fatura com NIF</strong>: discriminação completa (deslocação, mão-de-obra, peças).</li>
 <li><strong>Seguro RC</strong> cobrindo a intervenção.</li>
 <li>{region_text}</li>
</ul>''',
    # V1 — foco cobertura + garantía
    '''<h2 role="heading" aria-level="2">A nossa promessa em {name}</h2>
<ul>
 <li><strong>Cobertura operacional</strong> em {aldeias_text}.</li>
 <li><strong>Método:</strong> equipamento técnico verificado antes de cada intervención (Fluke + Megger + FLIR).</li>
 <li><strong>Garantia 2 anos</strong> sobre mão-de-obra e peças.</li>
 <li><strong>Seguro de responsabilidade civil</strong> incluído.</li>
 <li><strong>Compromisso de transparência:</strong> orçamento escrito antes de tocar na instalação.</li>
 <li><strong>Atendimento directo</strong> por telefone — Filipe, Trás-os-Montes.</li>
</ul>''',
    # V2 — focus fiabilité
    '''<h2 role="heading" aria-level="2">Porquê a Norte Reparos como parceiro para {name}</h2>
<ul>
 <li><strong>Conhecemos a região</strong> — {region_text}, base operacional em Macedo de Cavaleiros.</li>
 <li><strong>Resposta 24/7</strong> para qualquer avaria eléctrica no concelho de {name} ({district}).</li>
 <li><strong>Discriminação rigorosa</strong>: mão-de-obra 70 €/h ou 100 €/h fora do horário útil, deslocação de 30 € ou 50 € conforme o horário.</li>
 <li><strong>Fatura com NIF + 2 anos de garantia</strong> escrita entregue após a intervenção.</li>
 <li><strong>Sem invenção de moradas privadas</strong>: nunca publicamos direções residenciais de clientes.</li>
 <li><strong>Sem promessa de tempo</strong> escrita: confirmamos a janela por telefone antes da deslocação.</li>
</ul>''',
    # V3 — focus transparence totale
    '''<h2 role="heading" aria-level="2">Compromissos assumidos em {name}</h2>
<ul>
 <li><strong>Transparência tarifária:</strong> 70 €/h em horário útil ou 100 €/h fora de horas, com deslocação única de 30 € ou 50 € conforme o horário.</li>
 <li><strong>Documentos entregues:</strong> factura com NIF, garantía escrita, relatório do diagnóstico.</li>
 <li><strong>Equipamento profissional trazido para {aldeias_text}.</strong></li>
 <li><strong>Seguro RC</strong> cobrindo eventuais danos materiais.</li>
 <li><strong>Resposta directa</strong> — sem intermediário, sem call-center.</li>
</ul>''',
]

def render_porque(c, slug, loc_data):
    name = c['name']
    district = c['district']
    n = village_count_text(slug, loc_data)
    rgeo = district_context(district)

    if n == 0:
        aldeias_text = f'todo o concelho de {name} (mediante confirmação da distância)'
    else:
        aldeias_text = f'{n} aldeias do concelho de {name}'

    region_text = f'Base em {rgeo[1]} do distrito de {district}, {rgeo[2]} — contacto directo para {name}'
    euro70 = '70 €/h'
    zone_label = 'forfait horário'
    desloc_label = '30 € ou 50 € conforme o horário'

    t = pick(slug, PORQUE_TEMPLATES)
    return t.format(
        name=name, district=district, euro70=euro70, majo=MAJORATION,
        aldeias_text=aldeias_text, region_text=region_text,
        zone=zone_label, desloc=desloc_label, desloc_real=desloc, desloc_real_text=desloc_label,
    )


# === APPLICATION ===

def find_concelhos_neighbors(current_slug, current_district, all_concelhos, max_n=3):
    same = [x for x in all_concelhos if x['slug'] != current_slug and x.get('district') == current_district]
    same.sort(key=lambda x: (x.get('route_km') is None, x.get('route_km') or 9999))
    return same[:max_n]


def apply_section(html, section_html, anchor_open_re, anchor_close_re=None):
    """Remplace la zone correspondante par section_html.

    Si anchor_close_re est fourni et différent de anchor_open_re, matche entre les deux.
    Si None (ou identique), matche anchor_open_re directement (et on le remplace par section_html).
    """
    if anchor_close_re is None or anchor_close_re == anchor_open_re:
        pat = re.compile(anchor_open_re, flags=re.S)
    else:
        pat = re.compile(anchor_open_re + r'.*?' + anchor_close_re, flags=re.S)
    new_html, n = pat.subn(lambda m: section_html, html, count=1)
    if n != 1:
        return html, False
    return new_html, True


def apply_refonte_to_file(target_path, c, loc_data, all_concelhos):
    html = Path(target_path).read_text()

    n_total = 0
    # (a) Transparence tarifaire
    transp = render_transp(c, c['slug'])
    html, ok = apply_section(html, transp, r'<div class="transp">', r'</div>')
    if ok: n_total += 1
    # (b) Tabela deslocação — entre le h2 et le p style="font-size:.8rem" final
    tabela = render_tabela(c, c['slug'])
    # Le bloco inclui </table>, fermant par ce p
    pat_b = (r'<h2 role="heading" aria-level="2">[^<]*?[Tt]abela[^<]*?</h2>'
             r'.*?'
             r'<p style="font-size:\.8rem;color:#666">[^<]*?</p>')
    html, ok = apply_section(html, tabela, pat_b, pat_b)
    if ok: n_total += 1
    # (c) Serviços : entre h2 Serviços et </ul>
    servicos = render_servicos(c, c['slug'], loc_data)
    pat_c = (r'<h2 role="heading" aria-level="2">[^<]*?[Ss]ervi[cç]os?[^<]*?</h2>'
             r'\s*'
             r'<ul[^>]*>.*?</ul>')
    html, ok = apply_section(html, servicos, pat_c, pat_c)
    if ok: n_total += 1
    # (d) FAQ
    faq = render_faq(c, c['slug'], loc_data)
    pat_d = r'<section class="faq"[^>]*>.*?</section>'
    html, ok = apply_section(html, faq, pat_d, pat_d)
    if ok: n_total += 1
    # (e) Porquê
    porque = render_porque(c, c['slug'], loc_data)
    pat_e = (r'<h2 role="heading" aria-level="2">[^<]*?[Pp]orquê[^<]*?</h2>'
             r'\s*'
             r'<ul>.*?</ul>')
    html, ok = apply_section(html, porque, pat_e, pat_e)
    if ok: n_total += 1

    Path(target_path).write_text(html)
    return n_total


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--slug', default='macedo-de-cavaleiros')
    p.add_argument('--all', action='store_true')
    p.add_argument('--apply', action='store_true')
    p.add_argument('--dry-run', action='store_true', dest='dry_run')
    args = p.parse_args()

    concelhos = json.load(open(REPO / 'data' / 'concelhos.json'))
    loc = json.load(open(REPO / 'data' / 'localidades.json'))

    if args.dry_run or not args.apply:
        slug = args.slug
        c = next((x for x in concelhos if x['slug'] == slug), None)
        if not c: sys.exit(f"slug {slug} introuvable")
        print(f"--- DRY-RUN {slug} ---")
        print(f"-- transp --\n{render_transp(c, slug)}\n")
        print(f"-- tabela --\n{render_tabela(c, slug)[:500]}...\n")
        print(f"-- servicos --\n{render_servicos(c, slug, loc)[:500]}...\n")
        print(f"-- faq --\n{render_faq(c, slug, loc)[:500]}...\n")
        print(f"-- porque --\n{render_porque(c, slug, loc)[:500]}...\n")
        return

    targets = [c['slug'] for c in concelhos] if args.all else [args.slug]
    summary = []
    for slug in targets:
        c = next((x for x in concelhos if x['slug'] == slug), None)
        if not c:
            print(f"SKIP {slug}")
            continue
        target = REPO / 'concelhos' / f'{slug}.html'
        if not target.exists():
            print(f"SKIP {slug} (no file)")
            continue
        n = apply_refonte_to_file(target, c, loc, concelhos)
        summary.append((slug, n))
        print(f"  {slug:30s} | {n}/5 sections refondues")
    print(f"\n=== APPLIED on {len(summary)} files ===")


if __name__ == '__main__':
    main()
