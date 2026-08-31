#!/usr/bin/env python3
"""
split_plan.py — sépare SEO_PLAN.md en deux fichiers aux rôles disjoints.

    SEO_PLAN.md  = SOURCE D'ADRESSAGE. Lue par le dispatch. N'est jamais
                   écrite par un run.
    JOURNAL.md   = TRACE. Écrite par les runs. N'est jamais lue par le
                   dispatch.

Motif : tant que les deux rôles cohabitent dans un seul fichier, chaque
trace écrite décale l'adressage et fabrique le no-op suivant (boucle des
8 runs du 2026-08-30 sur ENR).

Non destructif : n'écrit que dans --outdir, ne touche jamais au dépôt.
Idempotent : rejouable sur la même entrée sans dérive.

Usage:
    python3 split_plan.py --in SEO_PLAN.md --outdir out/ [--report]
"""
import argparse
import os
import re
import sys

# --- Classification des sections -------------------------------------------
# LISTE BLANCHE, jamais liste noire.
#
# Seul est adressable ce qui se trouve entre les ancres CHANTIERS. Le reste
# du fichier est au mieux de la documentation de référence, au pire de la
# trace — mais jamais de l'adressage, quels que soient son titre, sa date
# ou sa position.
#
# Conséquence sur le découpage : une section inconnue part au JOURNAL. Une
# liste noire obligeait à reconnaître chaque forme de trace, et toute
# section mal titrée retombait dans l'adressage — le problème rentrait par
# la porte de service. Ici l'oubli coûte une section à reclasser à la main,
# pas une réouverture de la faille.

DOC_PATTERNS = [
    r'^#\s',                                  # titre de premier niveau
    r'ROADMAP',
    r'STRATÉGIE MONOPOLE',
    r'VISION',
    r'ÉTAT ACTUEL',
    r'TODO DÉTAILLÉE',
    r'RÈGLES DU PROJET',
    r'RÈGLES DE COORDINATION',
    r'NOTES pour les futures IA',
    r'P0 — Prix/zones OSRM',
    r'<préambule>',
]
DOC_RE = [re.compile(p) for p in DOC_PATTERNS]

HEADING_RE = re.compile(r'^(#{1,6})\s+(.*)$')


def is_doc(title_line):
    """Section de documentation à conserver dans SEO_PLAN.md.

    Conserver n'est pas rendre adressable : l'adressage vient exclusivement
    des ancres CHANTIERS."""
    return any(rx.search(title_line) for rx in DOC_RE)


def split_sections(lines):
    """Découpe en sections de niveau <= 2 (## et #)."""
    idx = []
    for i, line in enumerate(lines):
        m = HEADING_RE.match(line)
        if m and len(m.group(1)) <= 2:
            idx.append(i)
    if not idx:
        return [(0, len(lines), lines[0] if lines else '')]
    sections = []
    # Préambule éventuel avant le premier titre
    if idx[0] > 0:
        sections.append((0, idx[0], '<préambule>'))
    for n, start in enumerate(idx):
        end = idx[n + 1] if n + 1 < len(idx) else len(lines)
        sections.append((start, end, lines[start].rstrip('\n')))
    return sections


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--in', dest='infile', required=True)
    ap.add_argument('--outdir', required=True)
    ap.add_argument('--report', action='store_true')
    args = ap.parse_args()

    with open(args.infile, encoding='utf-8') as fh:
        lines = fh.readlines()

    sections = split_sections(lines)
    plan, journal, report = [], [], []

    for start, end, title in sections:
        body = lines[start:end]
        doc = is_doc(title)
        (plan if doc else journal).extend(body)
        report.append((
            'DOC    ' if doc else 'JOURNAL',
            start + 1, end - start, title[:88]
        ))

    os.makedirs(args.outdir, exist_ok=True)

    plan_hdr = [
        "<!-- SOURCE D'ADRESSAGE.\n",
        "     Le dispatch ne lit QUE le bloc entre les ancres\n",
        "     CHANTIERS:BEGIN / CHANTIERS:END. Tout le reste de ce fichier\n",
        "     est de la documentation : lisible, non adressable, sans effet\n",
        "     sur l'ordonnancement — quels que soient son titre, sa date ou\n",
        "     sa position.\n",
        "     N'y écrire aucune trace de run : les traces vont dans\n",
        "     JOURNAL.md. L'état lu et l'état écrit ne sont jamais le même\n",
        "     fichier. -->\n\n",
    ]
    jrnl_hdr = [
        "<!-- JOURNAL — trace append-only des runs.\n",
        "     Jamais lu par le dispatch. Écrire en TÊTE ou en QUEUE est ici\n",
        "     sans conséquence : aucun pointeur ne vise ce fichier. -->\n\n",
    ]

    with open(os.path.join(args.outdir, 'SEO_PLAN.md'), 'w', encoding='utf-8') as fh:
        fh.writelines(plan_hdr + plan)
    with open(os.path.join(args.outdir, 'JOURNAL.md'), 'w', encoding='utf-8') as fh:
        fh.writelines(jrnl_hdr + journal)

    if args.report:
        print(f"{'CLASSE':8s} {'L.DÉB':>6s} {'LIGNES':>7s}  TITRE")
        for cls, ln, n, title in report:
            print(f"{cls:8s} {ln:6d} {n:7d}  {title}")
        print()

    print(f"entrée      : {len(lines)} lignes")
    print(f"SEO_PLAN.md : {len(plan)} lignes  (adressage)")
    print(f"JOURNAL.md  : {len(journal)} lignes  (trace)")
    if len(plan) + len(journal) != len(lines):
        print("ERREUR: perte de lignes au découpage", file=sys.stderr)
        return 1
    print("contrôle    : 0 ligne perdue")
    return 0


if __name__ == '__main__':
    sys.exit(main())
