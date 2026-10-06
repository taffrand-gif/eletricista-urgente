#!/usr/bin/env python3
"""Charge /call-tracking.js sur les pages village EU qui n'ont que les anciens helpers inline.

Contexte : ces pages definissent window.trackTelClick / trackWhatsAppClick (click_tel,
click_whatsapp) mais aucun element ne les appelle, et /call-tracking.js (phone_click,
whatsapp_click, un seul ecouteur delegue) n'y est pas charge. Le lot A v4 (commit 51d4a28d8,
valide le 2026-09-30) a ajoute la meme balise sur 115 pages hors villages ; les villages
etaient exclus (decision V1 en attente). Insertion identique : une ligne avant </head>.

Ne modifie rien d'autre. call-tracking.js neutralise lui-meme les anciens helpers : un seul
evenement par clic. Idempotent. Ignore concelhos/ et blog/ (autres paquets).

Usage : python3 scripts/add_call_tracking_villages.py [--check] [racine | fichier.html ...]
"""
import os, sys

TAG = b'<script src="/call-tracking.js" defer></script>\n'
SKIP_DIRS = {'.git', 'node_modules', '_archive', '_audit', '_prototype', '_reports', '_indexing',
             'drizzle', 'content', 'client', 'concelhos', 'blog'}


def fix_bytes(raw):
    """Retourne (nouveau_contenu, modifie)."""
    if b'call-tracking.js' in raw or b'window.trackTelClick' not in raw:
        return raw, False
    if raw.count(b'</head>') != 1:
        return raw, False
    i = raw.index(b'</head>')
    # </head> en debut de ligne : balise sur sa propre ligne ; sinon insertion inline (diff minimal)
    tag = TAG if raw[i - 1:i] == b'\n' else TAG.rstrip(b'\n')
    return raw[:i] + tag + raw[i:], True


def iter_files(args):
    explicit = [a for a in args if a.endswith('.html')]
    if explicit:
        yield from explicit
        return
    root = args[0] if args else '.'
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in SKIP_DIRS and not d.startswith('_archive')]
        for f in fn:
            if f.endswith('.html'):
                yield os.path.join(dp, f)


def main(argv):
    check = '--check' in argv
    args = [a for a in argv if not a.startswith('--')]
    todo = changed = 0
    for p in iter_files(args):
        with open(p, 'rb') as fh:
            raw = fh.read()
        new, mod = fix_bytes(raw)
        if mod:
            todo += 1
            if not check:
                with open(p, 'wb') as fh:
                    fh.write(new)
                changed += 1
    print('pages sans mesure detectees: %d | modifiees: %d' % (todo, changed))
    return 1 if (check and todo) else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
