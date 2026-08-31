#!/usr/bin/env python3
"""
derive_served.py — dérive la liste blanche des surfaces servies d'UN repo.

PRINCIPE : est servi ce qui modifie le contenu de `outputDirectory`.
Le reste ne l'est pas, quel que soit son emplacement.

Ce principe se décline en deux régimes, et le régime se lit dans
`vercel.json`, il ne se suppose pas :

  BUILD    outputDirectory pointe une sortie de build (`dist/public`).
           Sont servies les SOURCES qui alimentent cette sortie, plus la
           chaîne qui la fabrique (prebuild/build/postbuild). Pas le reste
           du dépôt.

  STATIQUE outputDirectory vaut `.` ou est absent : le dépôt EST la sortie.
           Sont servis tous les fichiers publiés, moins `.vercelignore`,
           moins les fichiers d'état du projet (voir ÉTAT_PROJET).

La chaîne de build est RÉSOLUE, pas devinée : on suit `prebuild`, `build`
et `postbuild` de package.json, on déréférence les `npm run X`, et on
relève les fichiers réellement invoqués (`node scripts/foo.mjs`). C'est
pourquoi `scripts/**` n'entre jamais en bloc : un script d'audit ou de
purge ne change rien tant que la chaîne ne l'exécute pas.

Usage:
    python3 derive_served.py --repo <chemin> --name <nom> [--out served.json]
"""
import argparse
import json
import os
import re
import sys

# Fichiers d'état du projet. En régime STATIQUE ils sont physiquement
# publiés (ils sont dans outputDirectory), mais ce ne sont pas du contenu :
# aucun visiteur ne les atteint par navigation. Les compter comme servis
# rendrait I6 inopérant précisément sur les dépôts où les PR no-op
# atterrissent — une PR ne touchant que SEO_PLAN.md passerait le garde-fou.
ETAT_PROJET = [
    r'^[^/]*\.md$',
    r'^_archive',
    r'^_audit/',
    r'^_reports/',
    r'^_indexing/',
    r'^_backlog/',
    r'^tests?/',
    r'^\.',
]

# Sources qui alimentent dist/public en régime BUILD.
BUILD_SOURCES = [
    (r'^client/public/', 'publicDir de vite, copié tel quel dans outDir'),
    (r'^client/src/', 'compilé dans outDir'),
    (r'^client/index\.html$', "point d'entrée vite"),
    (r'^public/', 'alimente client/public via la chaîne prebuild'),
    (r'^vite\.config\.ts$', 'définit root, outDir et le contenu de la sortie'),
    (r'^package\.json$', 'définit la chaîne prebuild/build/postbuild'),
]

SCRIPT_REF = re.compile(r'node\s+([\w./-]+\.(?:mjs|js|cjs|ts))')
NPM_RUN = re.compile(r'npm\s+run\s+([\w:-]+)')


def resolve_chain(scripts):
    """Déréférence prebuild/build/postbuild et rend les fichiers invoqués."""
    seen, files, queue = set(), [], ['prebuild', 'build', 'postbuild']
    while queue:
        name = queue.pop(0)
        if name in seen or name not in scripts:
            continue
        seen.add(name)
        cmd = scripts[name]
        queue.extend(NPM_RUN.findall(cmd))
        for f in SCRIPT_REF.findall(cmd):
            if f not in files:
                files.append(f)
    return files, sorted(seen)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--name', required=True)
    ap.add_argument('--out')
    args = ap.parse_args()

    def load(fn):
        p = os.path.join(args.repo, fn)
        try:
            with open(p, encoding='utf-8') as fh:
                return json.load(fh)
        except (OSError, ValueError):
            return {}

    vercel, pkg = load('vercel.json'), load('package.json')
    outdir = vercel.get('outputDirectory')
    scripts = pkg.get('scripts', {})

    regime = 'BUILD' if (outdir and outdir not in ('.', './')) else 'STATIQUE'
    served, notes = [], []

    if regime == 'BUILD':
        for pat, why in BUILD_SOURCES:
            served.append(pat)
            notes.append(f'{pat} — {why}')
        chain_files, chain_names = resolve_chain(scripts)
        for f in chain_files:
            served.append('^' + re.escape(f) + '$')
            notes.append(f'^{f}$ — invoqué par la chaîne {"/".join(chain_names)}')
        notes.append('server/** EXCLU — bundlé par esbuild vers dist/, '
                     'jamais publié : outputDirectory ne contient que '
                     'dist/public')
        notes.append('scripts/** EXCLU en bloc — seuls les scripts '
                     'effectivement invoqués sont retenus')
    else:
        # Le dépôt EST la sortie : tout est publié. On énumère donc ce qui
        # ne l'est PAS, au lieu d'énumérer ce qui l'est — sinon on oublie
        # les fichiers racine qui ne sont pas du HTML. Cas réel : la PR
        # #286 de CU ne touche que LECONS.md et og-image.png ; l'image est
        # bien servie, et une liste blanche en `*.html` l'aurait manquée.
        served.append(r'^.')
        notes.append('^. — le dépôt EST la sortie : tout est publié, '
                     "l'exclusion fait seule le tri")
        notes.append("fichiers d'état du projet EXCLUS bien que publiés — "
                     "voir ETAT_PROJET")

    if os.path.exists(os.path.join(args.repo, 'vercel.json')):
        served.append(r'^vercel\.json$')
        notes.append('^vercel.json$ — rewrites et headers changent ce qui '
                     'est servi')

    cfg = {
        'repo': args.name,
        'regime': regime,
        'outputDirectory': outdir,
        'servi': served,
        'jamais_servi': ETAT_PROJET if regime == 'STATIQUE' else [],
        'justification': notes,
    }
    out = args.out or f'{args.name}.served.json'
    with open(out, 'w', encoding='utf-8') as fh:
        json.dump(cfg, fh, ensure_ascii=False, indent=2)

    print(f"{args.name}: régime {regime}, outputDirectory={outdir!r}")
    for n in notes:
        print(f"  · {n}")
    print(f"  → {out}")
    return 0


def _toplevel_dirs(repo):
    """Répertoires racine publiés (hors état projet et hors ignorés)."""
    ignore = {'node_modules', '.git', 'dist', 'scripts', 'tools'}
    out = []
    for e in os.listdir(repo):
        if not os.path.isdir(os.path.join(repo, e)):
            continue
        if e in ignore or e.startswith('.') or e.startswith('_'):
            continue
        out.append(e)
    return out


if __name__ == '__main__':
    sys.exit(main())
