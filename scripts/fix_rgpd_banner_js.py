#!/usr/bin/env python3
"""Repare le bandeau RGPD inline casse (SyntaxError: Unexpected identifier 'flex').

Cause : le patcheur one-shot patch_rgpd_statique_v2.py (2026-08-29, commit 6c5b087ac #342)
a ecrit b.innerHTML="<div style="flex:1;..." avec des guillemets non echappes.
Correction = remplacement litteral de 2 lignes, identique au paquet LOT-RGPD valide le
2026-09-30 (commit 05dba592c, 114 fichiers). Idempotent : une page deja reparee est ignoree.
Ne touche ni texte visible, ni prix, ni CTA, ni canonical, ni robots, ni sitemap, ni JSON-LD.

Usage : python3 scripts/fix_rgpd_banner_js.py [--check] [racine]
  --check : n'ecrit rien ; code 1 s'il reste des pages cassees.
"""
import os, sys

BROKEN_INNER = '  b.innerHTML="<div style="flex:1;min-width:220px"><strong>Cookies e análise de utilização.</strong> Utilizamos cookies para analisar a utilização do site (Google Analytics) e melhorar o serviço. Pode aceitar ou recusar — a sua escolha é livre. <a href="/politica-cookies" style="color:#7dd3fc;text-decoration:underline;margin-left:4px">Política de cookies</a></div><div style="display:flex;gap:10px;flex-shrink:0"><button id=""+BANNER_ID+"-accept" type="button" style="background:#2193b0;color:#fff;border:0;padding:10px 18px;border-radius:6px;font-weight:700;cursor:pointer;font-size:14px">Aceitar</button><button id=""+BANNER_ID+"-reject" type="button" style="background:#2193b0;color:#fff;border:0;padding:10px 18px;border-radius:6px;font-weight:700;cursor:pointer;font-size:14px">Recusar</button></div>";'
FIXED_INNER = '  b.innerHTML="<div style=\\"flex:1;min-width:220px\\"><strong>Cookies e análise de utilização.</strong> Utilizamos cookies para analisar a utilização do site (Google Analytics) e melhorar o serviço. Pode aceitar ou recusar — a sua escolha é livre. <a href=\\"/politica-cookies\\" style=\\"color:#7dd3fc;text-decoration:underline;margin-left:4px\\">Política de cookies</a></div><div style=\\"display:flex;gap:10px;flex-shrink:0\\"><button id=\\"rgpd-banner-eu-accept\\" type=\\"button\\" style=\\"background:#2193b0;color:#fff;border:0;padding:10px 18px;border-radius:6px;font-weight:700;cursor:pointer;font-size:14px\\">Aceitar</button><button id=\\"rgpd-banner-eu-reject\\" type=\\"button\\" style=\\"background:#2193b0;color:#fff;border:0;padding:10px 18px;border-radius:6px;font-weight:700;cursor:pointer;font-size:14px\\">Recusar</button></div>";'
BROKEN_STYLE = '  b.style="position:fixed;bottom:0;left:0;right:0;z-index:9999;background:rgba(17,24,39,.97);color:#f3f4f6;padding:14px 18px;display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:center;font-size:14px;line-height:1.45";'
FIXED_STYLE = '  b.style="position:fixed;bottom:0;left:0;right:0;z-index:10000;background:rgba(17,24,39,.97);color:#f3f4f6;padding:14px 18px;display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:center;font-size:14px;line-height:1.45";'
SKIP_DIRS = {'.git', 'node_modules', '_archive', '_audit', '_prototype', '_reports', '_indexing', 'drizzle', 'content', 'client'}


def fix_bytes(raw):
    """Retourne (nouveau_contenu, modifie)."""
    bi, fi = BROKEN_INNER.encode('utf8'), FIXED_INNER.encode('utf8')
    if bi not in raw:
        return raw, False
    out = raw.replace(bi, fi, 1)
    out = out.replace(BROKEN_STYLE.encode('utf8'), FIXED_STYLE.encode('utf8'), 1)
    return out, True


def main(argv):
    check = '--check' in argv
    args = [a for a in argv if not a.startswith('--')]
    root = args[0] if args else '.'
    changed = broken = 0
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in SKIP_DIRS and not d.startswith('_archive')]
        for f in fn:
            if not f.endswith('.html'):
                continue
            p = os.path.join(dp, f)
            with open(p, 'rb') as fh:
                raw = fh.read()
            new, mod = fix_bytes(raw)
            if mod:
                broken += 1
                if not check:
                    with open(p, 'wb') as fh:
                        fh.write(new)
                    changed += 1
    print('pages cassees detectees: %d | reparees: %d' % (broken, changed))
    return 1 if (check and broken) else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
