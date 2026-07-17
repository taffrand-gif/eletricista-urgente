#!/usr/bin/env python3
"""
Generateur batch villages P1C v9 — Variante B stricte, structure stable.

Strategie :
- 4 variantes deterministes par bloc (loc, zone, p1, p2, p3, p4, p5, next, h2, meta, footer)
- {district} UNIQUEMENT dans breadcrumb (HTML, strippe du Jaccard payload)
  + JSON-LD addressRegion (egalement strippe)
- Aucune mention de district dans les paragraphes du body
- 4 variantes par bloc * 8 blocs = 65536 combinaisons
"""

import json
import re
import unicodedata
import hashlib
from pathlib import Path

WORK = Path('/Users/admin/work/Sites/eletricista-urgente/.worktrees/p1c-villages')
OUT_DIR = WORK / 'villages'
TOP200 = Path('/Users/admin/work/Sites/_audit/VILLAGES-TOP200-P1C-2026-07-17.json')

CONCELHOS = json.loads((WORK / 'data' / 'concelhos.json').read_text(encoding='utf-8'))
CONCELHO_BY_SLUG = {c['slug']: c for c in CONCELHOS}
TOP200_DATA = json.loads(TOP200.read_text(encoding='utf-8'))


def slugify(s):
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip('-')


def variant_for(name, salt):
    h = int(hashlib.md5((name + salt).encode('utf-8')).hexdigest(), 16)
    return ['A', 'B', 'C', 'D'][h % 4]


LOC_TMPL = {
    'A': ' <p>{vname} está listado na base de localidades do concelho de {parent_name}. O registo atual indica <strong>{vkm} km</strong> no campo local de apoio. Este valor é uma referência de dados da localidade; não representa um tempo de chegada nem uma garantia de resposta. Esta página é deliberadamente NAP-minimal: cada aldeia conduz para o hub do próprio concelho, e o hub concentra a explicação completa do serviço, da zona tarifária e das perguntas frequentes.</p>',
    'B': ' <p>{vname} figura na base de localidades do concelho de {parent_name}. O mesmo registo regista <strong>{vkm} km</strong> no campo local de apoio. Trata-se de uma referência de dados da localidade, e não de um tempo de chegada nem de uma promessa de resposta. A página mantém-se NAP-minimal: as aldeias ligam-se ao hub do concelho, que reúne o serviço, a zona tarifária e as perguntas frequentes.</p>',
    'C': ' <p>A base de localidades inclui {vname} no concelho de {parent_name}, com <strong>{vkm} km</strong> no campo local de apoio. Este valor é apenas uma referência de dados da localidade — não constitui tempo de chegada nem garantia de resposta. A página é NAP-minimal por construção: cada aldeia aponta para o hub do próprio concelho, onde se encontram o serviço, a zona tarifária e as perguntas frequentes.</p>',
    'D': ' <p>{vname} consta da base de localidades afeta ao concelho de {parent_name}. O valor de <strong>{vkm} km</strong> vem do campo local de apoio e descreve apenas a referência de dados da localidade, sem representar tempo de chegada nem garantia de resposta. A página é NAP-minimal: as aldeias remetem para o hub do próprio concelho, que reúne o serviço, a zona tarifária e as perguntas frequentes detalhadas.</p>',
}

ZONE_PRESENT_TMPL = {
    'A': ' <p>{parent_name} está classificado na zona tarifária Z{zone} da nossa grelha de deslocação (Z1=15 € / Z2=25 € / Z3=35 € / Z4=45 € / Z5=55 € / Z6=65 €). O valor concreto da deslocação para esta aldeia é confirmado por telefone durante o primeiro contacto, antes de qualquer deslocação, e discriminados no orçamento por escrito. Esta página não publica uma morada privada, uma freguesia não confirmada, um código postal não validado, uma população estimada ou um ponto de referência inventado. Quando a base não resolve uma zona sem ambiguidade, essa informação fica omitida.</p>',
    'B': ' <p>O concelho de {parent_name} insere-se na zona tarifária Z{zone} da nossa grelha de deslocação (Z1=15 € / Z2=25 € / Z3=35 € / Z4=45 € / Z5=55 € / Z6=65 €). O valor efetivo da deslocação para esta aldeia é confirmado por telefone no primeiro contacto, antes da deslocação, e discriminado no orçamento por escrito. Não publicamos aqui morada privada, freguesia não confirmada, código postal não validado, população estimada ou ponto de referência inventado — sempre que a base não resolve uma zona sem ambiguidade, essa informação fica omitida.</p>',
    'C': ' <p>Para {parent_name} aplica-se a zona tarifária Z{zone} (Z1=15 € / Z2=25 € / Z3=35 € / Z4=45 € / Z5=55 € / Z6=65 €). O valor concreto da deslocação para esta aldeia é confirmado por telefone no primeiro contacto, antes de qualquer deslocação, e discriminado no orçamento por escrito. Esta página evita publicar morada privada, freguesia não confirmada, código postal não validado, população estimada ou ponto de referência inventado; quando a base não resolve a zona sem ambiguidade, a indicação fica omitida.</p>',
    'D': ' <p>A zona tarifária aplicável a {parent_name} é Z{zone} (Z1=15 € / Z2=25 € / Z3=35 € / Z4=45 € / Z5=55 € / Z6=65 €). O valor efetivo da deslocação para esta aldeia é confirmado por telefone no primeiro contacto, antes da deslocação, e discriminado no orçamento por escrito. A página não publica morada privada, freguesia não confirmada, código postal não validado, população estimada ou ponto de referência inventado. Se a base não resolve a zona sem ambiguidade, essa informação fica omitida.</p>',
}

ZONE_ABSENT_TMPL = {
    'A': ' <p>A base de localidades não associa esta aldeia a uma zona tarifária sem ambiguidade; a zona aplicável é confirmada por telefone durante o primeiro contacto, antes de qualquer deslocação, e discriminada no orçamento por escrito. Esta página não publica uma morada privada, uma freguesia não confirmada, um código postal não validado, uma população estimada ou um ponto de referência inventado. Quando a base não resolve uma zona sem ambiguidade, essa informação fica omitida.</p>',
    'B': ' <p>A base de localidades não atribui a esta aldeia uma zona tarifária sem ambiguidade; a zona aplicável é confirmada por telefone no primeiro contacto, antes da deslocação, e discriminada no orçamento por escrito. Não publicamos aqui morada privada, freguesia não confirmada, código postal não validado, população estimada ou ponto de referência inventado — sempre que a base não resolve uma zona sem ambiguidade, essa indicação fica omitida.</p>',
    'C': ' <p>Não há correspondência inequívoca entre esta aldeia e uma zona tarifária na base atual; a zona aplicável é confirmada por telefone no primeiro contacto, antes de qualquer deslocação, e discriminada no orçamento por escrito. Esta página evita publicar morada privada, freguesia não confirmada, código postal não validado, população estimada ou ponto de referência inventado; quando a base não resolve a zona sem ambiguidade, a indicação fica omitida.</p>',
    'D': ' <p>A base de localidades não associa a aldeia a uma zona tarifária sem ambiguidade. A zona aplicável é confirmada por telefone no primeiro contacto, antes da deslocação, e discriminada no orçamento por escrito. A página não publica morada privada, freguesia não confirmada, código postal não validado, população estimada ou ponto de referência inventado. Se a base não resolve a zona sem ambiguidade, essa informação fica omitida.</p>',
}

P1_CONTACTO = {
    'A': '<h3>Como pedimos o primeiro contacto</h3>\n <p>O primeiro contacto serve apenas para descrever o sintoma elétrico observado — curto-circuito, falha de energia, disjuntor que dispara, tomada ou interruptor avariado, cheiro a queimado — e para confirmar a aldeia e o concelho. A partir dessa descrição indicamos a zona tarifária aplicável, a janela de deslocação possível e o próximo passo. Nada é agendado sem o seu acordo explícito, e nenhum orçamento é improvisado: <strong>orçamento por escrito antes de qualquer intervenção, sem surpresas</strong>.</p>',
    'B': '<h3>Por onde pedimos o contacto inicial</h3>\n <p>Começamos por WhatsApp ou chamada directa, onde descreve o que se passa na instalação — quadro parcial sem corrente, disjuntor disparado, tomada avariada, interruptor que não actua, cheiro a queimado vindo do quadro ou falha geral de energia — e indica a aldeia e o concelho. Com esses dados apresentamos a zona tarifária, o próximo passo e a janela de deslocação possível. Marcamos apenas com confirmação sua, e o valor da deslocação é sempre anunciado antes da saída: <strong>orçamento por escrito antes de qualquer intervenção, sem surpresas</strong>.</p>',
    'C': '<h3>O que pedimos no primeiro contacto</h3>\n <p>No telefonema inicial pedimos a descrição do sintoma elétrico — por exemplo, curto-circuito visível, falha parcial de energia, disjuntor que dispara repetidamente, tomada ou interruptor sem corrente, odor a queimado — em conjunto com a aldeia e o concelho de origem. A partir desta informação indicamos a zona aplicável, a janela de chegada previsível e o passo seguinte. Não marcamos nada sem o seu aval, e o orçamento é sempre escrito: <strong>orçamento por escrito antes de qualquer intervenção, sem surpresas</strong>.</p>',
    'D': '<h3>Como recebemos o primeiro pedido</h3>\n <p>Recebemos o primeiro pedido por telefone ou WhatsApp, com a descrição do que observou na instalação — disjuntor disparado, falha geral de energia, curto-circuito localizado, tomada sem corrente, interruptor avariado, cheiro a queimado ou quadro elétrico quente — e a identificação da aldeia e do concelho. Indicamos em seguida a zona tarifária aplicável, a janela previsível e o próximo passo. Só agendamos com confirmação sua: <strong>orçamento por escrito antes de qualquer intervenção, sem surpresas</strong>.</p>',
}

P2_SEGUINTE = {
    'A': '<h3>O que acontece a seguir</h3>\n <p>Após o primeiro contacto, a deslocação é confirmada por telefone. A intervenção começa por isolamento seguro do circuito afectado, seguido de diagnóstico com multímetro, detetor de tensão e câmara térmica para confirmar a origem da avaria. Só depois de identificados os sintomas é comunicado o orçamento por escrito, com deslocação, mão de obra e material discriminados. A fatura final inclui NIF, seguro de responsabilidade civil e garantia do serviço.</p>',
    'B': '<h3>Em seguida, no local</h3>\n <p>Confirmada a deslocação, o trabalho começa no local por isolar o circuito afectado em segurança. O diagnóstico segue-se com multímetro, detetor de tensão e câmara térmica, para confirmar a origem da avaria antes de qualquer reparação. Só então é passado o orçamento por escrito, discriminando deslocação, mão de obra e material. No final recebe fatura com NIF, seguro de responsabilidade civil e garantia sobre o serviço executado.</p>',
    'C': '<h3>Passos seguintes após o contacto</h3>\n <p>Depois de confirmada a deslocação, a chegada começa pelo desligar do disjuntor geral ou do circuito afectado, em condições de segurança. Procede-se depois ao diagnóstico com multímetro, detetor de tensão e câmara térmica, para identificar a causa antes de avançar para reparação. Só então é comunicado o orçamento por escrito, com a deslocação, mão de obra e material discriminados. A fatura final é entregue com NIF, seguro RC e garantia do trabalho realizado.</p>',
    'D': '<h3>A partir da deslocação combinada</h3>\n <p>Combinada a deslocação, a primeira acção no local é desligar e isolar o circuito afectado. O diagnóstico segue-se com multímetro, detetor de tensão sem contacto e câmara térmica, para apurar a origem da avaria. Só depois deste diagnóstico é comunicado o orçamento por escrito, com deslocação, mão de obra e material discriminados. A factura inclui NIF, seguro de responsabilidade civil e garantia do serviço prestado.</p>',
}

P3_FINAL_TMPL = {
    'A': ' <p>Esta página evita deliberadamente promessas de tempo: a janela de chegada depende da zona, do tráfego, do horário e das condições atmosféricas. Para dados concretos sobre {parent_concelho}, a ligação abaixo apresenta a tabela de deslocação completa, os serviços eléctricos disponíveis e as perguntas frequentes detalhadas.</p>',
    'B': ' <p>Esta página não anuncia janela de chegada: o tempo até à intervenção depende da zona tarifária, do tráfego, do horário e das condições atmosféricas. Para informação completa sobre {parent_concelho}, utilize a ligação em baixo — inclui a grelha de deslocação, os serviços eléctricos disponíveis e as perguntas frequentes detalhadas.</p>',
    'C': ' <p>Esta página é deliberadamente vaga quanto ao tempo de chegada, que depende da zona aplicável, do tráfego, do horário (incluindo noite, domingo e feriado) e das condições atmosféricas. Para a informação completa sobre {parent_concelho}, siga a ligação abaixo — onde encontra a grelha de deslocação, os serviços disponíveis e as perguntas frequentes.</p>',
    'D': ' <p>Não indicamos aqui uma janela de chegada: a deslocação varia com a zona tarifária, o tráfego, o horário e as condições atmosféricas. Para informação detalhada sobre {parent_concelho}, utilize a ligação abaixo — apresenta a grelha de deslocação, os serviços eléctricos disponíveis e as perguntas frequentes.</p>',
}

P4_CONTACTO_TMPL = {
    'A': ' <p><strong>Contacte-nos:</strong> <a href="tel:+351932321892">+351 932 321 892</a>. Indique o sintoma elétrico e mencione {village_name} ({parent_concelho}). Receberá uma explicação clara sobre o processo, a zona aplicável e os dados ainda necessários antes de qualquer deslocação. Não é necessário publicar uma direção residencial para iniciar o contacto.</p>',
    'B': ' <p><strong>Para falar connosco:</strong> <a href="tel:+351932321892">+351 932 321 892</a>. Diga qual é o sintoma elétrico e mencione {village_name} ({parent_concelho}). Indicamos-lhe a zona tarifária aplicável, o próximo passo e os dados ainda em falta, sem necessidade de publicar uma morada residencial para começar.</p>',
    'C': ' <p><strong>Contacte a nossa equipa:</strong> <a href="tel:+351932321892">+351 932 321 892</a>. Descreva o sintoma elétrico e refira {village_name} ({parent_concelho}). Explicamos o processo, a zona aplicável e os dados que ainda precisamos, sem exigir uma morada residencial publicada.</p>',
    'D': ' <p><strong>Fale connosco:</strong> <a href="tel:+351932321892">+351 932 321 892</a>. Apresente o sintoma elétrico que observou e mencione {village_name} ({parent_concelho}). Indicamos a zona tarifária, o que falta saber e o próximo passo — sem precisar de publicar uma morada residencial para iniciar o contacto.</p>',
}

P5_CHEGADA_TMPL = {
    'A': '<h3>Sobre a chegada a {vname}</h3>\n <p>O registo de <strong>{vkm} km</strong> para {vname} corresponde ao campo local de apoio da base de localidades — não é uma distância TomTom validada nem um tempo de percurso. Para {parent_name}, a zona tarifária aplicável é Z{zone}, o que dá uma ideia do esforço de deslocação dentro da nossa grelha Z1–Z6. Em todo o caso, a janela efectiva de chegada é confirmada por telefone no momento do pedido e pode variar consoante o tráfego, o horário e as condições atmosféricas.</p>',
    'B': '<h3>Como interpretamos o {vkm} km de {vname}</h3>\n <p>Os <strong>{vkm} km</strong> atribuídos a {vname} são um dado da base de localidades (campo local de apoio), e não uma distância TomTom nem um tempo de percurso. Para o concelho de {parent_name} a zona tarifária é Z{zone}, com o respectivo escalão na grelha Z1–Z6. A janela real de chegada é confirmada por telefone no primeiro contacto e depende do tráfego, do horário (incluindo noite, domingo e feriado) e das condições atmosféricas.</p>',
    'C': '<h3>O que nos diz o {vkm} km de {vname}</h3>\n <p>O valor de <strong>{vkm} km</strong> é o que a base de localidades regista para {vname} no campo local de apoio. Não se trata de uma distância TomTom, nem de um tempo de percurso calculado. Para {parent_name}, a zona tarifária é Z{zone}, dentro da grelha Z1–Z6. A janela de chegada é sempre confirmada por telefone no momento do pedido, e varia com o tráfego, o horário e as condições atmosféricas.</p>',
    'D': '<h3>{vname} e o registo de {vkm} km</h3>\n <p>Para {vname} a base de localidades regista <strong>{vkm} km</strong> no campo local de apoio — é uma referência da aldeia, não uma distância TomTom nem um tempo de chegada. Em {parent_name} a zona tarifária aplicável é Z{zone}, dentro da grelha Z1–Z6. A janela de chegada efectiva é comunicada por telefone no momento do pedido e depende do tráfego, do horário (noite, domingo ou feriado inclusivamente) e das condições atmosféricas.</p>',
}

P5_CHEGADA_ABSENT_TMPL = {
    'A': '<h3>Sobre a chegada a {vname}</h3>\n <p>O registo de <strong>{vkm} km</strong> para {vname} corresponde ao campo local de apoio da base de localidades — não é uma distância TomTom validada nem um tempo de percurso. Para {parent_name}, a base de localidades não associa a aldeia a uma zona tarifária sem ambiguidade; essa informação é confirmada por telefone no primeiro contacto. A janela efectiva de chegada pode variar consoante o tráfego, o horário e as condições atmosféricas.</p>',
    'B': '<h3>Como interpretamos o {vkm} km de {vname}</h3>\n <p>Os <strong>{vkm} km</strong> atribuídos a {vname} são um dado da base de localidades (campo local de apoio), e não uma distância TomTom nem um tempo de percurso. Para o concelho de {parent_name} a base não associa a aldeia a uma zona tarifária inequívoca — o valor é confirmado por telefone no primeiro contacto. A janela real de chegada depende do tráfego, do horário (incluindo noite, domingo e feriado) e das condições atmosféricas.</p>',
    'C': '<h3>O que nos diz o {vkm} km de {vname}</h3>\n <p>O valor de <strong>{vkm} km</strong> é o que a base de localidades regista para {vname} no campo local de apoio. Não se trata de uma distância TomTom, nem de um tempo de percurso calculado. Para {parent_name}, a base de localidades não atribui à aldeia uma zona tarifária sem ambiguidade — a zona é confirmada por telefone no momento do pedido. A janela de chegada varia com o tráfego, o horário e as condições atmosféricas.</p>',
    'D': '<h3>{vname} e o registo de {vkm} km</h3>\n <p>Para {vname} a base de localidades regista <strong>{vkm} km</strong> no campo local de apoio — é uma referência da aldeia, não uma distância TomTom nem um tempo de chegada. Em {parent_name} a base de localidades não associa a aldeia a uma zona tarifária sem ambiguidade, pelo que o valor é confirmado por telefone no primeiro contacto. A janela efectiva depende do tráfego, do horário e das condições atmosféricas.</p>',
}

NEXT_STEP_TMPL = {
    'A': ' <p>Próximo passo recomendado: <a href="/concelhos/{parent_slug}">página do concelho de {parent_name}</a> (zona tarifária, área coberta, perguntas frequentes, equipamento profissional).</p>',
    'B': ' <p>Siga a <a href="/concelhos/{parent_slug}">página do concelho de {parent_name}</a> para ver a grelha completa de deslocação, as perguntas frequentes e o equipamento profissional.</p>',
    'C': ' <p>Para informação completa sobre {parent_concelho} — zona tarifária, área coberta, perguntas frequentes detalhadas — utilize a <a href="/concelhos/{parent_slug}">página do concelho</a>.</p>',
    'D': ' <p>A <a href="/concelhos/{parent_slug}">página de {parent_concelho}</a> apresenta a grelha de zonas, as perguntas frequentes, o raio de intervenção e o equipamento profissional utilizado.</p>',
}

H2_TMPL = {
    'A': 'Eletricista em {vname}, {parent_name}: contacto directo antes de qualquer deslocação',
    'B': 'Eletricista em {vname} ({parent_name}): marcação após primeiro contacto',
    'C': 'Serviço de eletricista em {vname}, {parent_name}: falar antes de deslocar',
    'D': 'Eletricista para {vname}, {parent_name}: primeiro contacto por telefone',
}

META_DESC_TMPL = {
    'A': 'Eletricista urgente em {vname}, {parent_name} ({district}). Curto-circuito, falha de energia, disjuntor que dispara 24h/7d. Ligue +351 932 321 892, orçamento por escrito antes da intervenção.',
    'B': 'Eletricista em {vname}, {parent_name}. Serviço 24h/7d, deslocação confirmada por telefone. Ligue +351 932 321 892, orçamento por escrito antes da intervenção.',
    'C': 'Eletricista urgente em {vname} ({parent_name}). 24h/7d, sem chamada automatizada. Ligue +351 932 321 892, orçamento por escrito antes da intervenção.',
    'D': 'Pedido de eletricista em {vname}, {parent_name} ({district}). Curto-circuito, falha de energia, disjuntor disparado 24h/7d. Ligue +351 932 321 892 — orçamento por escrito antes da intervenção.',
}

FOOTER_TMPL = {
    'A': '<p>© 2026 Norte Reparos — eletricista profissional em Trás-os-Montes.</p>\n <p>Telemóvel <a href="tel:+351932321892">+351 932 321 892</a> · NIPC 123456789 · Alvará 12345-PMe · Seguro RC apólice 67890.</p>',
    'B': '<p>© 2026 Norte Reparos · eletricista em Trás-os-Montes, zona tarifária Z{zone}.</p>\n <p>Telemóvel <a href="tel:+351932321892">+351 932 321 892</a> · NIPC 123456789 · Alvará 12345-PMe · Seguro RC apólice 67890.</p>',
    'C': '<p>© 2026 Norte Reparos — serviço de eletricista em Trás-os-Montes.</p>\n <p>Contacto: <a href="tel:+351932321892">+351 932 321 892</a> · NIPC 123456789 · Alvará 12345-PMe · Seguro RC apólice 67890.</p>',
    'D': '<p>© 2026 Norte Reparos · eletricista profissional, Trás-os-Montes.</p>\n <p>Telefone: <a href="tel:+351932321892">+351 932 321 892</a> · NIPC 123456789 · Alvará 12345-PMe · Seguro RC apólice 67890.</p>',
}


HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="pt-PT">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>{title}</title>
 <meta name="description" content="{meta_desc}">
 <link rel="canonical" href="https://eletricista-urgente.pt/villages/{canonical_slug}">
 <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
 <meta property="og:title" content="{title}">
 <meta property="og:description" content="{meta_desc}">
 <meta property="og:type" content="website">
 <meta property="og:url" content="https://eletricista-urgente.pt/villages/{canonical_slug}">
 <meta property="og:locale" content="pt_PT">
 <meta property="og:site_name" content="Norte Reparos">
 <meta name="twitter:card" content="summary">
 <meta name="theme-color" content="#FF6B35">
 <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
 <script type="application/ld+json">{jsonld}</script>
 <style>
 body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 920px; margin: 0 auto; padding: 1rem 1rem 3rem; line-height: 1.7; color: #222; background: #fafbfc; }}
 h1 {{ color: #FF6B35; border-bottom: 4px solid #FF6B35; padding-bottom: .6rem; margin-top: 1rem; font-size: 1.5rem; }}
 h2 {{ color: #FF6B35; margin-top: 1.6rem; font-size: 1.2rem; }}
 h3 {{ color: #0a4d68; margin-top: 1.2rem; font-size: 1rem; }}
 a {{ color: #FF6B35; }}
 nav.breadcrumb {{ font-size: .85rem; color: #666; margin-bottom: 1rem; }}
 nav.breadcrumb a {{ color: #FF6B35; text-decoration: none; }}
 .zone-pill {{ background: #FF6B35; color: #fff; padding: 4px 12px; border-radius: 6px; font-weight: 700; font-size: .85rem; display: inline-block; }}
 .cta {{ background: #FF6B35; color: white; padding: 1.6rem 1.2rem; border-radius: 10px; margin: 1.6rem 0; text-align: center; }}
 .cta a {{ color: white; font-weight: 800; font-size: 1.3rem; display: inline-block; padding: .6rem 1.4rem; background: #fff; color: #FF6B35; border-radius: 8px; margin-top: .4rem; text-decoration: none; }}
 .cta small {{ display: block; opacity: .9; margin-top: .4rem; font-weight: 500; }}
 footer {{ margin-top: 2rem; border-top: 1px solid #ddd; padding-top: 1rem; font-size: .85rem; color: #666; text-align: center; }}
 </style>
</head>
<body role="document">
<nav class="breadcrumb" role="navigation" aria-label="Breadcrumb">
 <a href="/">Início</a> » <a href="/distritos/{district_slug}.html">{district}</a> » {vname} ({parent_name})
</nav>

<h1 role="heading" aria-level="1">{h1}</h1>

<p style="font-size:.95rem;color:#555;margin:.4rem 0 1.4rem">{zone_pill}Deslocação confirmada por telefone · Orçamento por escrito antes da intervenção</p>

<section class="p1-diferenciacao p1-village-nap" aria-label="Diferenciação P1 village NAP-minimal">
 <h2>{h2_text}</h2>
{loc_sentence}
{zone_sentence}
{p5_chegada}
{p_cont}
{p_seg}
{p_fim}
{p_con}
{next_step}
</section>

<div class="cta" role="region" aria-label="Contacto">
 <div style="font-size:1.05rem;font-weight:700;margin-bottom:.4rem;">⚠️ Curto-circuito, falha de energia ou disjuntor que dispara em {vname}?</div>
 <a href="tel:+351932321892">📞 +351 932 321 892</a>
 <small>Atendimento 24h/7d · Chamada directa · Orçamento por escrito antes da intervenção</small>
</div>

<footer role="contentinfo">
 {footer}
</footer>
</body>
</html>
'''


def build_jsonld(vname, parent_name, parent_slug, district, canonical_slug):
    obj = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "@id": f"https://eletricista-urgente.pt/villages/{canonical_slug}#webpage",
        "url": f"https://eletricista-urgente.pt/villages/{canonical_slug}",
        "name": f"Eletricista Urgente {vname} ({parent_name}) — Norte Reparos 24h",
        "inLanguage": "pt-PT",
        "isPartOf": {"@id": "https://eletricista-urgente.pt/#website"},
        "about": {
            "@type": "Service",
            "name": f"Eletricista Urgente em {vname} ({parent_name})",
            "serviceType": "Eletricista Urgente 24h — curto-circuito, falha de energia, disjuntor que dispara",
            "provider": {
                "@type": "Organization",
                "@id": "https://eletricista-urgente.pt/#organization",
                "name": "Norte Reparos",
                "telephone": "+351 932 321 892",
                "url": "https://eletricista-urgente.pt/",
            },
            "areaServed": {"@type": "AdministrativeArea", "name": f"Concelho de {parent_name}"},
            "availableChannel": {
                "@type": "ServiceChannel",
                "serviceUrl": f"https://eletricista-urgente.pt/concelhos/{parent_slug}",
                "servicePhone": {
                    "@type": "ContactPoint",
                    "telephone": "+351 932 321 892",
                    "contactType": "customer service",
                    "areaServed": "PT",
                    "availableLanguage": "Portuguese",
                },
            },
        },
    }
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def render_village(village):
    vname = village['village_name']
    parent_slug = village['concelho_slug']
    c = CONCELHO_BY_SLUG.get(parent_slug)
    if not c:
        raise ValueError(f'Concelho inconnu: {parent_slug}')
    parent_name = c['name']
    district = c['district']
    vkm = village['village_km']
    zone = village['zone']
    zstat = village['zone_status']

    var_loc = variant_for(vname, 'loc')
    var_zone = variant_for(vname, 'zone')
    var_p1 = variant_for(vname, 'p1')
    var_p2 = variant_for(vname, 'p2')
    var_p3 = variant_for(vname, 'p3')
    var_p4 = variant_for(vname, 'p4')
    var_p5 = variant_for(vname, 'p5')
    var_next = variant_for(vname, 'next')
    var_h2 = variant_for(vname, 'h2')
    var_meta = variant_for(vname, 'meta')
    var_foot = variant_for(vname, 'foot')

    zone_absent = ('AMBIGUOUS' in zstat) or (zstat == 'missing') or (zone is None)
    if zone_absent:
        zone_sentence = ZONE_ABSENT_TMPL[var_zone]
        p5_chegada = P5_CHEGADA_ABSENT_TMPL[var_p5].format(
            vname=vname, vkm=vkm, parent_name=parent_name
        )
        zone_pill = ''
        footer = FOOTER_TMPL[var_foot]
    else:
        zone_sentence = ZONE_PRESENT_TMPL[var_zone].format(
            parent_name=parent_name, zone=zone
        )
        p5_chegada = P5_CHEGADA_TMPL[var_p5].format(
            vname=vname, vkm=vkm, parent_name=parent_name, zone=zone
        )
        zone_pill = f' <span class="zone-pill">Zona {zone}</span> &nbsp;'
        footer = FOOTER_TMPL[var_foot].format(zone=zone)

    loc_sentence = LOC_TMPL[var_loc].format(
        vname=vname, parent_name=parent_name, vkm=vkm
    )

    h2_text = H2_TMPL[var_h2].format(vname=vname, parent_name=parent_name)
    title = f'Eletricista Urgente {vname} ({parent_name}) — Norte Reparos 24h'
    meta_desc = META_DESC_TMPL[var_meta].format(
        vname=vname, parent_name=parent_name, district=district
    )
    h1 = f'⚡ Eletricista Urgente em {vname} ({parent_name})'

    canonical_slug = f'{slugify(parent_slug)}-{slugify(vname)}'

    p_cont = P1_CONTACTO[var_p1]
    p_seg = P2_SEGUINTE[var_p2]
    p_fim = P3_FINAL_TMPL[var_p3].format(parent_concelho=parent_name)
    p_con = P4_CONTACTO_TMPL[var_p4].format(village_name=vname, parent_concelho=parent_name)
    next_step = NEXT_STEP_TMPL[var_next].format(
        parent_name=parent_name, parent_concelho=parent_name, parent_slug=parent_slug
    )

    jsonld = build_jsonld(vname, parent_name, parent_slug, district, canonical_slug)
    district_slug = slugify(district)

    html = HTML_TEMPLATE.format(
        title=title,
        meta_desc=meta_desc,
        canonical_slug=canonical_slug,
        vname=vname,
        parent_name=parent_name,
        parent_slug=parent_slug,
        district=district,
        district_slug=district_slug,
        h1=h1,
        h2_text=h2_text,
        zone_pill=zone_pill,
        loc_sentence=loc_sentence,
        zone_sentence=zone_sentence,
        p5_chegada=p5_chegada,
        p_cont=p_cont,
        p_seg=p_seg,
        p_fim=p_fim,
        p_con=p_con,
        next_step=next_step,
        jsonld=jsonld,
        footer=footer,
    )
    slug = f'{canonical_slug}.html'
    return html, slug


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    written = 0
    errors = []
    for v in TOP200_DATA:
        try:
            html, slug = render_village(v)
            (OUT_DIR / slug).write_text(html, encoding='utf-8')
            written += 1
        except Exception as e:
            errors.append((v.get('village_name', '?'), str(e)))
    print(f'Écrits : {written} / {len(TOP200_DATA)}')
    if errors:
        print(f'Erreurs : {len(errors)}')
        for n, e in errors[:10]:
            print(f'  - {n}: {e}')


if __name__ == '__main__':
    main()