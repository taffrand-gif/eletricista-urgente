#!/usr/bin/env python3
"""
Génère sitemap.xml (et public/sitemap.xml) pour eletricista-urgente.pt.

CU a déjà un build_sitemap.py, EU n'en avait pas. Crée ce script par
parité (leçon t_2029e47b) pour pouvoir régénérer le sitemap EU à la demande.

Cible : inclure les pages money/service SERVIE et INDEXABLES :
- 33 piliers info (sans noindex, sans _archive)
- 433 urgentes money (≥18KB = top villes avec contenu)
- aldeia simples money (≥18KB)
- service money (tomada-interruptor, curto-circuito, etc.)
- 33 concelhos/
- 6 distritos/
- blog/ (html)

Exclut :
- Pages <18KB (boilerplates courts)
- _archive/*
- diacritique doublons md5

Format URL : https://eletricista-urgente.pt/<slug> (sans .html, conforme canonical)
"""
import os, re, hashlib, sys
from collections import defaultdict
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_URL = 'https://eletricista-urgente.pt'
TODAY = date.today().isoformat()
SIZE_THRESHOLD = 18000

# Pages EU explicitement noindex (à exclure du sitemap)
NOINDEX_PAGES = set()  # EU n'a pas de noindex dans ce scope (à enrichir si besoin)

# Prefixes service EU (money-tier)
SERVICE_PREFIXES = (
    'autoclismo-', 'tomada-interruptor-', 'curto-circuito-', 'quadro-eletrico-',
    'fuga-agua-', 'fossa-septica-', 'esquentador-', 'canalizacao-nova-',
    'iluminacao-', 'avarias-eletricas-', 'instalacao-eletrica-',
)


def has_diacritics(s):
    return bool(re.search(r'[áéíóúàâêôãõçÁÉÍÓÚÀÂÊÔÃÕÇ]', s))


def collect_html_files(directory):
    out = []
    for f in os.listdir(directory):
        full = os.path.join(directory, f)
        if os.path.isfile(full) and f.endswith('.html'):
            out.append(f)
    return out


def dedup_md5(files, root_dir):
    md5_groups = defaultdict(list)
    for f in files:
        full = os.path.join(root_dir, f)
        with open(full, 'rb') as fp:
            data = fp.read()
        h = hashlib.md5(data).hexdigest()
        md5_groups[h].append(f)
    keep = set()
    for h, lst in md5_groups.items():
        sorted_lst = sorted(lst, key=lambda x: (has_diacritics(x), x))
        keep.add(sorted_lst[0])
    return keep


def categorize(unique_files, root_dir):
    """Catégorise les fichiers .html racine EU."""
    pillars = set()
    urgentes = set()
    services = set()
    aldeia = set()  # aldeia simples (villages)
    noindex = set()
    for f in unique_files:
        if f in NOINDEX_PAGES:
            noindex.add(f)
            continue
        if not f.startswith('eletricista-'):
            pillars.add(f)
            continue
        if f == 'index.html':
            pillars.add(f)
            continue
        if f.startswith('eletricista-urgente-'):
            urgentes.add(f)
            continue
        is_service = False
        for sp in SERVICE_PREFIXES:
            if f.startswith(f'eletricista-{sp}'):
                services.add(f)
                is_service = True
                break
        if is_service:
            continue
        aldeia.add(f)
    return pillars, urgentes, services, aldeia, noindex


def file_to_url(f):
    slug = f[:-5]
    return f'{BASE_URL}/{slug}'


def build_sitemap_xml(urls_with_priority):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for url, priority in urls_with_priority:
        lines.append(f'<url><loc>{url}</loc><lastmod>{TODAY}</lastmod><priority>{priority}</priority></url>')
    lines.append('</urlset>')
    lines.append('')
    return '\n'.join(lines)


def main():
    root_files = collect_html_files(ROOT)
    unique_root = dedup_md5(root_files, ROOT)
    pillars, urgentes_all, services_all, aldeia_all, noindex = categorize(unique_root, ROOT)

    def by_size(file_set):
        return {f for f in file_set if os.path.getsize(os.path.join(ROOT, f)) >= SIZE_THRESHOLD}

    urgentes_money = by_size(urgentes_all)
    services_money = by_size(services_all)
    aldeia_money = by_size(aldeia_all)

    concelhos_dir = os.path.join(ROOT, 'concelhos')
    distritos_dir = os.path.join(ROOT, 'distritos')
    blog_dir = os.path.join(ROOT, 'blog')

    concelhos = sorted(os.listdir(concelhos_dir)) if os.path.isdir(concelhos_dir) else []
    distritos = sorted(os.listdir(distritos_dir)) if os.path.isdir(distritos_dir) else []
    blog_html = sorted([f for f in os.listdir(blog_dir) if f.endswith('.html')]) if os.path.isdir(blog_dir) else []

    urls = []

    for f in sorted(pillars):
        url = file_to_url(f) if f != 'index.html' else f'{BASE_URL}/'
        priority = '1.0' if f == 'index.html' else '0.7'
        urls.append((url, priority))

    for f in concelhos:
        slug = f[:-5]
        urls.append((f'{BASE_URL}/concelhos/{slug}', '0.8'))

    for f in distritos:
        slug = f[:-5]
        urls.append((f'{BASE_URL}/distritos/{slug}', '0.7'))

    for f in blog_html:
        slug = f[:-5]
        urls.append((f'{BASE_URL}/blog/{slug}', '0.6'))

    for f in sorted(urgentes_money):
        urls.append((file_to_url(f), '0.9'))

    for f in sorted(services_money):
        urls.append((file_to_url(f), '0.8'))

    for f in sorted(aldeia_money):
        urls.append((file_to_url(f), '0.7'))

    print(f"=== INVENTAIRE FINAL ===")
    print(f"  Piliers info        : {len(pillars)}")
    print(f"  Urgentes money      : {len(urgentes_money)} (sur {len(urgentes_all)} total)")
    print(f"  Service money       : {len(services_money)} (sur {len(services_all)} total)")
    print(f"  Concelhos           : {len(concelhos)}")
    print(f"  Distritos           : {len(distritos)}")
    print(f"  Blog (html)         : {len(blog_html)}")
    print(f"  Aldeia money        : {len(aldeia_money)} (sur {len(aldeia_all)} total simples)")
    print(f"  TOTAL URLs sitemap  : {len(urls)}")
    print(f"  Exclus aldeia <18KB : {len(aldeia_all) - len(aldeia_money)} (boilerplates courts)")

    xml = build_sitemap_xml(urls)

    out_paths = [
        os.path.join(ROOT, 'sitemap.xml'),
        os.path.join(ROOT, 'public', 'sitemap.xml'),
    ]
    for p in out_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w', encoding='utf-8') as fp:
            fp.write(xml)
        print(f"  Written: {p}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
