#!/usr/bin/env python3
"""
measure.py — mesure une famille de violations, contrôle positif inclus.

RÈGLE APPLIQUÉE MÉCANIQUEMENT : tout compte sort avec un contrôle positif
produit par la MÊME exécution. Un zéro seul ne prouve rien — il peut être
une absence de violation ou un outil cassé, et rien ne les distingue.

Quatre faux négatifs silencieux ont été rencontrés le 30/08/2026, tous
rendant 0 sans la moindre erreur : `\\s` non interprété par `git grep -E`,
`(?:...)` inexistant en ERE POSIX, périmètre implicite, et `\\|` échappé
cassant un tableau. Cet outil refuse de rendre un compte dont le contrôle
positif est à zéro : dans ce cas, c'est la mesure qui est cassée, pas le
dépôt qui est sain.

Il signale enfin les ANGLES MORTS DE FORMAT : si un prédicat déclare un
périmètre, le motif est rejoué sans restriction et l'outil rend ce qui
matche ailleurs. Un gate téléphone qui ne lit que du HTML a laissé vivre
un numéro croisé dans un `.json` pendant des mois — son compte était juste
sur son périmètre, et son périmètre ne disait pas qu'il excluait des
formats. Un gate énonce ses FORMATS au même titre que son motif et son
périmètre.

Avec --ventiler, il sépare le compte en PRODUCTION et HORS PRODUCTION.
Ce n'est ni un tri par extension ni le périmètre servi de I6 : un `.md` de
`content/blog/` alimente la génération et compte, `server/` n'est pas servi
mais une affirmation fausse qui s'y trouve reste fausse, tandis que
`SEO_PLAN.md` et `_archive/` ne sont rien. Un motif qui matche sa propre
doctrine gonfle le compte et fait patcher la règle au lieu du contenu.

Usage:
    python3 measure.py --repo <chemin> --ref github/main \\
        --famille X-ORC \\
        --motif '[Oo]r[çc]amento[^<>.!?]{0,40}(gratuit|gr[áa]tis)' \\
        --controle-positif 'or[çc]amento' \\
        --arbre 'client/public/*.html' 'client/src/*' \\
        [--exclusion '(diagn[óo]stico|an[áa]lise)[^<>.!?]{0,30}gratuit']

    python3 measure.py --repo <chemin> --ref origin/main --lot familles.json
"""
import argparse
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from argguard import verifier_arguments

# Motifs ERE refusés en amont : ils rendent 0 sans erreur avec git grep -E.
PIEGES = [
    ('\\s', "`\\s` n'est pas interprété — écrire les espaces littéralement"),
    ('(?:', "`(?:...)` n'existe pas en ERE POSIX — utiliser `(...)`"),
    ('\\d', "`\\d` n'est pas interprété — utiliser `[0-9]`"),
    ('\\b', "`\\b` est peu fiable ici — préférer une classe explicite"),
    # Le plus vicieux des cinq : dans une classe, `\n` n'est pas un saut de
    # ligne, c'est le backslash ET la lettre `n`. `[^<>\n]` exclut donc
    # `<`, `>`, `\` et **n** — n'importe quel mot contenant un « n » casse
    # le motif. Vérifié : `orcamento personalizado gratuito` ne matche pas
    # `orcamento[^<>\n]{0,40}gratuit`. Sur CNR, 42 fichiers au lieu de 262.
    # Le compteur reste plausible, c'est ce qui rend l'erreur durable.
    ('\\n', "`\\n` dans un motif ERE = backslash + lettre `n`. Dans une "
            "classe `[^...\\n]`, cela EXCLUT la lettre n — tout mot qui en "
            "contient casse le motif. Retirer `\\n` de la classe"),
    ('\\t', "`\\t` n'est pas une tabulation en ERE — c'est backslash + t"),
    ('\\r', "`\\r` n'est pas un retour chariot en ERE"),
]

# HORS PRODUCTION — le périmètre d'un RECENSEMENT de violations.
#
# À ne pas confondre avec la liste blanche `served.json`, qui sert à I6.
# Les deux répondent à des questions différentes :
#   served.json      « cette PR change-t-elle ce qu'un visiteur reçoit ? »
#   hors production  « ce fichier contient-il une affirmation fausse ? »
# `server/reviewAutomation.ts` n'est pas servi — une PR qui ne toucherait
# que lui serait refusée par I6 — mais une garantie fausse qui y figure
# reste une garantie fausse dans le code. Elle compte au recensement.
#
# CRITÈRE : « un humain ou un modèle peut-il lire ce fichier comme une
# AFFIRMATION DE L'ENTREPRISE ? »  Un `.patch`, non — c'est un artefact
# d'outillage. Un `.json` servi en 200 et lu par ChatGPT, oui. Le tri
# n'est donc ni l'extension seule, ni « servi contre non servi » : un
# `.md` de `content/blog/` alimente la génération et compte, `server/`
# n'est pas servi mais une affirmation fausse qui s'y trouve reste
# fausse, tandis qu'un `.patch` sous `_prototype/` n'affirme rien.
HORS_PRODUCTION = [
    # Artefacts d'outillage — jamais du contenu, quel que soit l'endroit.
    r'\.(patch|diff|log)$',
    # COPIES SOUS UN NOM VOISIN. Le suffixe peut être décoré : la copie
    # périmée de `og-image.png` s'appelait `og-image.png.bak-57645` et
    # répondait 200 en servant les faux avis « 4.9 (127 reviews) » que la
    # PR d'à côté venait de retirer. Un motif ancré sur `\.bak$` ne la
    # voyait pas. Un fichier corrigé peut survivre sous un nom voisin.
    r'\.(bak|orig|rej|backup|old|save|tmp)([-._][A-Za-z0-9]+)*$',
    r'\.pre-fix', r'~$',
    r'(^|/)_archive', r'(^|/)_prototype', r'(^|/)_reports?/',
    r'(^|/)_audit/', r'(^|/)_backlog/', r'(^|/)_indexing/',
    # Doctrine racine : elle CITE la règle qu'on cherche.
    r'^[^/]+\.md$',
    r'^\.',
]


def charger_served(path):
    return [re.compile(p) for p in HORS_PRODUCTION]


def est_servi(chemin, served):
    return not any(r.search(chemin) for r in served)


def git_grep(repo, ref, motif, arbre, only_matching=False):
    cmd = ['git', '-C', repo, 'grep', '-o' if only_matching else '-l',
           '-E', motif, ref]
    if arbre:
        cmd += ['--'] + list(arbre)
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode not in (0, 1):
        return None, res.stderr.strip()
    lines = [l for l in res.stdout.splitlines() if l.strip()]
    return lines, None


# Fenêtre bornée `[^...]{0,N}` dont la classe n'exclut pas la ponctuation
# forte. Elle relie deux propositions sans rapport et FABRIQUE des
# violations : sur ENR, `[Oo]r[çc]amento[^<>]{0,40}gratuit` reliait
# « orçamento final no local. » à « Fornecemos diagnóstico gratuito » de la
# phrase SUIVANTE — laquelle relève de l'exclusion doctrinale. 207 fichiers
# comptés, 20 réels, 187 faux positifs.
#
# Symétrique exact de la substitution destructrice (règle 8) : une fenêtre
# trop permissive INVENTE des violations quand on compte, et DÉTRUIT du
# texte voisin quand on substitue. Même cause, deux dégâts opposés.
FENETRE = re.compile(r'\[\^([^\]]*)\]\{0,(\d+)\}')
PONCT_FORTE = '.!?'


def verifier_fenetre(motif, seuil=8):
    alertes = []
    for classe, n in FENETRE.findall(motif):
        if int(n) < seuil:
            continue
        manquants = [c for c in PONCT_FORTE if c not in classe]
        if manquants:
            alertes.append(
                f"fenêtre `[^{classe}]{{0,{n}}}` n'exclut pas "
                f"{' '.join(repr(c) for c in manquants)} : elle peut "
                "traverser une frontière de phrase et relier deux "
                "propositions sans rapport. Écrire "
                f"`[^{classe}{''.join(manquants)}]{{0,{n}}}`, ou assumer "
                "explicitement avec --fenetre-sans-ponctuation")
    return alertes


def verifier_motif(motif, fenetre_libre=False):
    alertes = [msg for frag, msg in PIEGES if frag in motif]
    if not fenetre_libre:
        alertes += verifier_fenetre(motif)
    return alertes


def mesurer(repo, ref, fam, motif, controle, arbre, exclusion=None,
            served=None, fenetre_libre=False):
    out = {'famille': fam, 'ref': ref,
           'arbre': list(arbre) if arbre else ['(dépôt entier)']}

    alertes = (verifier_motif(motif, fenetre_libre)
               + verifier_motif(controle, fenetre_libre))
    if alertes:
        out['refus'] = 'motif suspect'
        out['alertes'] = alertes
        return out

    ctrl, err = git_grep(repo, ref, controle, arbre)
    if err:
        out['refus'] = f'git grep en erreur : {err}'
        return out
    if len(ctrl) == 0:
        out['refus'] = (
            f"contrôle positif « {controle} » à ZÉRO sur cet arbre. "
            "La mesure est cassée (motif, périmètre ou ref), pas le dépôt "
            "sain. Aucun compte n'est rendu.")
        return out
    out['controle_positif'] = {'motif': controle, 'fichiers': len(ctrl)}

    cible, err = git_grep(repo, ref, motif, arbre)
    if err:
        out['refus'] = f'git grep en erreur : {err}'
        return out
    occ, _ = git_grep(repo, ref, motif, arbre, only_matching=True)
    out['cible'] = {'motif': motif, 'fichiers': len(cible),
                    'occurrences': len(occ or [])}

    if served:
        chemins = [l.split(':', 1)[1] if ':' in l else l for l in cible]
        hors = [c for c in chemins if not est_servi(c, served)]
        servis = [c for c in chemins if est_servi(c, served)]
        md_servis = [c for c in servis if c.endswith('.md')]
        out['cible']['servis'] = len(servis)
        out['cible']['hors_production'] = len(hors)
        out['cible']['exemples_hors_production'] = sorted(hors)[:4]
        if md_servis:
            out['cible']['dont_md_servis'] = len(md_servis)
        if hors:
            out['cible']['avertissement'] = (
                f"{len(hors)} fichier(s) hors production comptés — ils ne "
                "sont rien, ni doctrine à préserver ni contenu à corriger. "
                "Le compte à retenir est celui des fichiers de PRODUCTION.")

    # TROISIÈME AXE — les FORMATS balayés.
    # Un gate qui ne lit que du HTML est aveugle à un numéro faux dans un
    # .json, et l'est silencieusement : son compte est juste sur son
    # périmètre, et son périmètre ne dit pas qu'il exclut des formats.
    # On rejoue donc le motif SANS restriction d'arbre et on rend ce qui
    # matche ailleurs, ventilé par extension.
    if arbre:
        partout, _ = git_grep(repo, ref, motif, [])
        if partout:
            vus = {l.split(':', 1)[1] if ':' in l else l for l in cible}
            tous = {l.split(':', 1)[1] if ':' in l else l for l in partout}
            dehors = [c for c in (tous - vus)
                      if not served or est_servi(c, served)]
            if dehors:
                exts = {}
                for c in dehors:
                    e = os.path.splitext(c)[1] or '(sans extension)'
                    exts[e] = exts.get(e, 0) + 1
                out['angle_mort_format'] = {
                    'fichiers': len(dehors),
                    'par_extension': dict(sorted(exts.items(),
                                                 key=lambda kv: -kv[1])),
                    'exemples': sorted(dehors)[:4],
                }

    if exclusion:
        exc, _ = git_grep(repo, ref, exclusion, arbre)
        out['exclusion'] = {'motif': exclusion,
                            'fichiers_non_violants': len(exc or [])}
    return out


def rendre(r):
    print(f"\n── {r['famille']}  ({r['ref']})")
    print(f"   arbre : {' '.join(r['arbre'])}")
    if 'refus' in r:
        print(f"   ⛔ REFUS — {r['refus']}")
        for a in r.get('alertes', []):
            print(f"      · {a}")
        return False
    c = r['controle_positif']
    print(f"   contrôle positif : {c['fichiers']:>6} fichiers   « {c['motif']} »")
    t = r['cible']
    print(f"   CIBLE            : {t['fichiers']:>6} fichiers   "
          f"{t['occurrences']} occurrences")
    if 'servis' in t:
        print(f"   PRODUCTION       : {t['servis']:>6} fichiers"
              + (f"   (dont {t['dont_md_servis']} .md de génération)"
                 if 'dont_md_servis' in t else ""))
        print(f"   hors production  : {t['hors_production']:>6} fichiers  "
              f"{', '.join(x.split('/')[-1] for x in t.get('exemples_hors_production', []))}")
    if 'avertissement' in t:
        print(f"   ⚠️  {t['avertissement']}")
    if 'angle_mort_format' in r:
        a = r['angle_mort_format']
        fmts = ' · '.join(f"{k} ×{v}" for k, v in a['par_extension'].items())
        print(f"   ⚠️  ANGLE MORT DE FORMAT : {a['fichiers']} fichier(s) de "
              f"production matchent HORS du périmètre déclaré")
        print(f"       {fmts}")
        for x in a['exemples']:
            print(f"       · {x}")
    if 'exclusion' in r:
        e = r['exclusion']
        print(f"   exclusion        : {e['fichiers_non_violants']:>6} fichiers "
              f"non violants « {e['motif']} »")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--ref', default='origin/main')
    ap.add_argument('--famille')
    ap.add_argument('--motif')
    ap.add_argument('--controle-positif', dest='controle')
    ap.add_argument('--arbre', nargs='*', default=[])
    ap.add_argument('--exclusion')
    ap.add_argument('--lot', help='JSON : liste de familles à mesurer')
    ap.add_argument('--fenetre-sans-ponctuation', dest='fenetre_libre',
                    action='store_true',
                    help='assume une fenêtre qui peut traverser une phrase')
    ap.add_argument('--ventiler', action='store_true',
                    help='ventile le compte en production / hors production')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()
    verifier_arguments(args)

    served = charger_served(True) if args.ventiler else None
    familles = []
    if args.lot:
        with open(args.lot, encoding='utf-8') as fh:
            familles = json.load(fh)
    else:
        if not (args.famille and args.motif and args.controle):
            ap.error('--famille, --motif et --controle-positif sont requis '
                     '(ou --lot). Le contrôle positif n\'est pas optionnel.')
        familles = [{'famille': args.famille, 'motif': args.motif,
                     'controle': args.controle, 'arbre': args.arbre,
                     'exclusion': args.exclusion}]

    resultats, ok = [], True
    for f in familles:
        r = mesurer(args.repo, args.ref, f['famille'], f['motif'],
                    f['controle'], f.get('arbre') or [], f.get('exclusion'),
                    served, args.fenetre_libre)
        resultats.append(r)
        if not args.json:
            ok = rendre(r) and ok

    if args.json:
        print(json.dumps(resultats, ensure_ascii=False, indent=2))
    else:
        refus = [r['famille'] for r in resultats if 'refus' in r]
        print(f"\n{len(resultats) - len(refus)}/{len(resultats)} famille(s) "
              f"mesurée(s)" + (f" — REFUS : {', '.join(refus)}" if refus else ""))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
