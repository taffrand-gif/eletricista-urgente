#!/usr/bin/env python3
"""
dispatch.py — choisit le prochain chantier d'un run, par IDENTIFIANT STABLE.

Quatre invariants, dans l'ordre où ils ont été payés :

  I1  ADRESSAGE PAR ID. Le dispatch ne connaît pas les numéros de ligne.
      Un chantier sans ID n'est pas dispatchable — il est signalé, pas deviné.

  I2  LE DISPATCH N'ÉCRIT RIEN. Ni dans SEO_PLAN.md, ni ailleurs. Les traces
      vont dans JOURNAL.md, écrit par le run, jamais relu par le dispatch.

  I3  UN GATE BLOQUE LE MERGE, PAS LE RUN. Un « GO requis » lu dans un
      fichier d'état ne fait jamais renvoyer « rien à faire ». C'est la
      leçon R7 : du 06/08 au 09/08/2026, un gate relu comme ordre d'arrêt
      a coûté 4 nuits de production.

  I4  DÉDUP AVANT DISPATCH. Un chantier dont une PR est MERGED n'est pas
      redispatchable. C'est ce qui a manqué aux 8 runs no-op du
      2026-08-30 sur ENR, tous sur un chantier clos par la PR #398.

  I5  L'ÉTAT LU ET L'ÉTAT ÉCRIT NE SONT JAMAIS LE MÊME FICHIER.
      Le dispatch ne lit que le bloc entre les ancres CHANTIERS. Il ne lit
      pas context.md, qui est réécrit par chaque run : un fichier qu'on
      modifie ne peut pas servir de pointeur sur lui-même. context.md est
      un journal pour les humains, sans effet sur l'ordonnancement.
      Tout le reste découle de cette règle.

  I6  PAS DE PR SANS DIFF SERVI. Un run autonome n'ouvre de PR que si son
      diff touche au moins un fichier réellement servi. Sinon il ne pousse
      rien, consigne dans son journal et rend la main. Ne s'applique pas
      aux PR humaines ni aux PR d'outillage.

Sortie : un objet JSON sur stdout, ou un code de sortie non nul si aucun
chantier n'est dispatchable (ce qui est un résultat, pas une erreur).

Usage:
    python3 dispatch.py --plan SEO_PLAN.md --repo taffrand-gif/eletricista-norte-reparos
    python3 dispatch.py --plan SEO_PLAN.md --prs prs.json      # hors ligne
    python3 dispatch.py --plan SEO_PLAN.md --id B2 --prs prs.json
"""
import argparse
import json
import os
import re
import subprocess
import sys

BEGIN = '<!-- CHANTIERS:BEGIN -->'
END = '<!-- CHANTIERS:END -->'

# Formes acceptées : B1, C4, X001 (amorçage) et X-JSX, X-GEN (chantiers ad
# hoc nommés). Un ID reste court, majuscule et sans espace — c'est ce qui le
# rend citable dans un titre de PR sous la forme [ID:<X>].
ID_RE = re.compile(r'^[A-Z]{1,3}(?:\d{1,3})?(?:-[A-Z0-9]{1,10})?$')
# EN_COURS n'est PAS dispatchable : un autre agent travaille déjà dessus.
# Le dispatcher le saute et prend le suivant, plutôt que d'ouvrir une PR
# concurrente sur le même chantier — c'est ainsi que naissent les
# force-push croisés et les commits orphelins.
OPEN_STATUS = {'A_FAIRE'}
BUSY_STATUS = {'EN_COURS'}
PRIO_ORDER = {'HAUTE': 0, 'MOYENNE': 1, 'BASSE': 2, '': 3}


# I6 — surfaces servies. PAR REPO, jamais globale : une liste unique serait
# fausse pour deux dépôts sur quatre (CU et EU sont des statiques purs, sans
# server/ ni chaîne de prerender). La liste se dérive de vercel.json et de
# package.json — voir derive_served.py — et se charge ici.

# I5 — fichiers réécrits par les runs : jamais une source d'adressage.
FORBIDDEN_SOURCES = ('context.md',)


class Chantier(dict):
    @property
    def id(self):
        return self.get('ID', '').strip()


def load_served(cfg_path):
    with open(cfg_path, encoding='utf-8') as fh:
        cfg = json.load(fh)
    return (cfg,
            [re.compile(p) for p in cfg.get('servi', [])],
            [re.compile(p) for p in cfg.get('jamais_servi', [])])


def served(paths, ok_re, ko_re):
    """Chemins qui modifient le contenu de outputDirectory.

    `jamais_servi` l'emporte : en régime statique, SEO_PLAN.md est
    physiquement publié mais n'est pas du contenu. Sans cette exclusion,
    une PR ne touchant que SEO_PLAN.md passerait I6 — exactement le cas
    des PR no-op qu'on cherche à refuser."""
    return [p for p in paths
            if any(rx.search(p) for rx in ok_re)
            and not any(rx.search(p) for rx in ko_re)]


def check_diff(paths, cfg_path):
    """I6 — un run autonome peut-il ouvrir une PR avec ce diff ?"""
    cfg, ok_re, ko_re = load_served(cfg_path)
    hits = served(paths, ok_re, ko_re)
    return {
        'repo': cfg.get('repo'),
        'regime': cfg.get('regime'),
        'fichiers_du_diff': len(paths),
        'fichiers_servis': hits,
        'pr_autorisee': bool(hits),
        'motif': (f'{len(hits)} fichier(s) servi(s)' if hits else
                  'aucun fichier servi — ne pas pousser, consigner au '
                  'journal et rendre la main (I6)'),
    }


def parse_registry(path):
    """Lit le registre entre marqueurs. Les marqueurs sont des ancres, pas
    des positions : insérer du texte ailleurs dans le fichier ne déplace
    rien du point de vue du dispatch."""
    base = os.path.basename(path).lower()
    if any(base.endswith(f) for f in FORBIDDEN_SOURCES):
        sys.exit(f"ERREUR: {os.path.basename(path)} est réécrit par les runs "
                 "et ne peut pas servir de source d'adressage (I5).")
    with open(path, encoding='utf-8') as fh:
        text = fh.read()
    if BEGIN not in text or END not in text:
        sys.exit(f"ERREUR: marqueurs {BEGIN} / {END} absents de {path}. "
                 "Le registre de chantiers est obligatoire (I1).")
    block = text.split(BEGIN, 1)[1].split(END, 1)[0]
    rows = [ln.strip() for ln in block.splitlines()
            if ln.strip().startswith('|')]
    rows = [r for r in rows if not re.match(r'^\|[\s:|-]+\|$', r)]
    if not rows:
        return []
    header = split_cells(rows[0])
    out, ignorees = [], []
    for row in rows[1:]:
        cells = split_cells(row)
        if len(cells) != len(header):
            # Un chantier ne disparaît JAMAIS en silence : une ligne mal
            # formée est signalée, pas ignorée. C'est ce garde-fou qui a
            # révélé que les `\|` échappés d'un prédicat cassaient le
            # découpage et faisaient sauter deux chantiers du registre.
            ignorees.append((row[:60], len(cells), len(header)))
            continue
        out.append(Chantier(zip(header, cells)))
    if ignorees:
        for r, got, want in ignorees:
            print(f"ERREUR: ligne de registre illisible ({got} colonnes, "
                  f"{want} attendues) : {r}…", file=sys.stderr)
        sys.exit("Registre invalide — corriger avant tout dispatch.")
    return out


def split_cells(row):
    """Découpe une ligne de tableau markdown sur les `|` NON échappés.

    Un prédicat contient souvent des alternatives regex `a\\|b` : les
    couper comme des séparateurs de colonne décale toute la ligne."""
    cells, cur, prev = [], '', ''
    for ch in row.strip().strip('|'):
        if ch == '|' and prev != '\\':
            cells.append(cur.strip())
            cur = ''
        else:
            cur += ch
        prev = ch
    cells.append(cur.strip())
    return cells


def merged_ids(repo=None, prs_file=None):
    """Ensemble des ID de chantier cités par une PR MERGED.

    Convention : le titre ou le corps d'une PR porte le token [ID:<X>].
    Un chantier ainsi cité est clos et n'est plus dispatchable (I4)."""
    if prs_file:
        with open(prs_file, encoding='utf-8') as fh:
            prs = json.load(fh)
    elif repo:
        res = subprocess.run(
            ['gh', 'pr', 'list', '--repo', repo, '--state', 'all',
             '--limit', '200', '--json', 'number,state,title,body'],
            capture_output=True, text=True, check=True)
        prs = json.loads(res.stdout)
    else:
        return {}, set()
    closed, merged_nums = {}, set()
    for pr in prs:
        if pr.get('state') != 'MERGED':
            continue
        merged_nums.add(pr.get('number'))
        blob = f"{pr.get('title', '')}\n{pr.get('body') or ''}"
        for cid in re.findall(r'\[ID:([A-Z0-9-]+)\]', blob):
            closed.setdefault(cid, []).append(pr.get('number'))
    return closed, merged_nums


def cited_merged(ch, merged_nums):
    """PR citées dans la colonne PR du registre et déjà mergées.

    Voie de dédup qui fonctionne sur l'historique existant, où les PR ne
    portent pas encore le token [ID:<X>]."""
    nums = {int(n) for n in re.findall(r'#(\d+)', ch.get('PR', ''))}
    return nums & merged_nums


def noop_streak(journal_path, cid, window=3):
    """Compte les no-op consécutifs récents sur un même ID.

    Garde-fou terminal : si le dispatch a déjà proposé ce chantier et que
    les runs n'y ont rien trouvé, le redispatcher une fois de plus produit
    exactement la boucle du 2026-08-30."""
    if not journal_path:
        return 0
    try:
        with open(journal_path, encoding='utf-8') as fh:
            lines = fh.readlines()
    except OSError:
        return 0
    streak = 0
    for ln in lines:
        if f'[ID:{cid}]' not in ln:
            continue
        if 'NO-OP' in ln.upper():
            streak += 1
            if streak >= window:
                return streak
        else:
            break
    return streak


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--plan')
    ap.add_argument('--served', metavar='SERVED.JSON',
                    help='liste blanche du repo, produite par '
                         'derive_served.py')
    ap.add_argument('--check-diff', metavar='FICHIER',
                    help='I6 — fichier listant les chemins du diff (un par '
                         'ligne). Répond si un run autonome peut ouvrir une '
                         'PR. Sortie 4 si non.')
    ap.add_argument('--journal')
    ap.add_argument('--repo')
    ap.add_argument('--prs')
    ap.add_argument('--id', help='forcer un chantier précis (par ID)')
    ap.add_argument('--noop-window', type=int, default=3)
    args = ap.parse_args()

    if args.check_diff:
        if not args.served:
            ap.error('--check-diff exige --served (liste blanche du repo)')
        with open(args.check_diff, encoding='utf-8') as fh:
            paths = [ln.strip() for ln in fh if ln.strip()]
        verdict = check_diff(paths, args.served)
        print(json.dumps(verdict, ensure_ascii=False, indent=2))
        return 0 if verdict['pr_autorisee'] else 4

    if not args.plan:
        ap.error('--plan est requis (ou --check-diff)')

    chantiers = parse_registry(args.plan)
    closed, merged_nums = merged_ids(args.repo, args.prs)

    verdicts = []
    eligible = []

    for ch in chantiers:
        cid, why = ch.id, None
        if not cid or not ID_RE.match(cid):
            why = 'SANS_ID — non dispatchable, ID à créer (I1)'
        elif ch.get('Statut', '').upper() in BUSY_STATUS:
            why = 'EN_COURS — pris par un autre agent, on passe au suivant'
        elif ch.get('Statut', '').upper() not in OPEN_STATUS:
            why = f"statut={ch.get('Statut')}"
        elif cid in closed:
            why = f"clos par PR MERGED {closed[cid]} (I4)"
        elif cited_merged(ch, merged_nums):
            why = (f"colonne PR = {sorted(cited_merged(ch, merged_nums))} "
                   "déjà MERGED (I4)")
        else:
            streak = noop_streak(args.journal, cid, args.noop_window)
            if streak >= args.noop_window:
                why = (f'{streak} no-op consécutifs — chantier probablement '
                       'déjà produit, exige un arbitrage humain (I4)')
            else:
                eligible.append(ch)
        verdicts.append({'id': cid or '(vide)',
                         'chantier': ch.get('Chantier', '')[:60],
                         'dispatchable': why is None,
                         'motif': why or 'éligible'})

    # I3 — un gate n'exclut jamais du dispatch, il annote.
    for ch in eligible:
        if ch.get('Gate', '').strip() not in ('', '—', '-'):
            ch['_avertissement'] = (
                f"gate « {ch['Gate']} » : bloque le MERGE, pas ce run (I3)")

    if args.id:
        eligible = [c for c in eligible if c.id == args.id]
        if not eligible:
            print(json.dumps({'dispatch': None,
                              'motif': f'{args.id} non dispatchable',
                              'verdicts': verdicts},
                             ensure_ascii=False, indent=2))
            return 2

    eligible.sort(key=lambda c: PRIO_ORDER.get(c.get('Prio', '').upper(), 3))

    out = {
        'dispatch': eligible[0] if eligible else None,
        'nb_eligibles': len(eligible),
        'verdicts': verdicts,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if eligible else 3


if __name__ == '__main__':
    sys.exit(main())
