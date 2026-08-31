#!/usr/bin/env python3
"""
check_prompt.py — compare le prompt REÇU à la copie versionnée du dépôt.

Le prompt est le point unique de défaillance de la chaîne. Tout le reste —
outillage, registre, prédicats, listes blanches — vit dans les dépôts et
passe par une PR. Le prompt, lui, vit dans la configuration de la tâche
planifiée : hors de git, modifiable sans trace, sans revue.

Le 30/08/2026, après deux jours de corrections, il portait encore
l'adressage par numéro de ligne, `context.md` comme file de tâches et le
gate merge relu comme ordre d'arrêt. Réactiver la tâche en l'état annulait
tout le travail. Rien dans les dépôts ne l'aurait montré.

D'où cette garde, premier acte de chaque run : le prompt reçu doit
correspondre à `.loop/PROMPT.md`, versionné et gaté par PR comme le reste.
Une divergence n'est pas un avertissement, c'est un REFUS DE DÉMARRER.

La comparaison ignore uniquement les espaces de fin de ligne et les lignes
vides terminales. Elle n'ignore RIEN d'autre : une garde qui se satisfait
d'une correspondance partielle laisse passer le cas qu'elle couvre.

Usage:
    python3 check_prompt.py --recu prompt-recu.md [--ref .loop/PROMPT.md]
"""
import argparse
import difflib
import hashlib
import os
import sys


def normaliser(texte):
    lignes = [l.rstrip() for l in texte.replace('\r\n', '\n').split('\n')]
    while lignes and not lignes[-1]:
        lignes.pop()
    return lignes


def empreinte(lignes):
    return hashlib.sha256('\n'.join(lignes).encode('utf-8')).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--recu', required=True,
                    help='fichier contenant le prompt effectivement reçu')
    ap.add_argument('--ref', default=os.path.join('.loop', 'PROMPT.md'))
    ap.add_argument('--montrer-diff', action='store_true', default=True)
    args = ap.parse_args()

    for p in (args.recu, args.ref):
        if not os.path.exists(p):
            print(f"⛔ REFUS DE DÉMARRER — {p} introuvable.", file=sys.stderr)
            print("   Sans les deux versions, la comparaison n'a pas de sens "
                  "et l'absence ne vaut pas conformité.", file=sys.stderr)
            return 2

    recu = normaliser(open(args.recu, encoding='utf-8').read())
    ref = normaliser(open(args.ref, encoding='utf-8').read())
    h_recu, h_ref = empreinte(recu), empreinte(ref)

    print(f"prompt reçu     sha256 {h_recu[:16]}…  {len(recu)} lignes")
    print(f"copie versionnée sha256 {h_ref[:16]}…  {len(ref)} lignes")

    if h_recu == h_ref:
        print("\n✅ Prompt conforme à la copie versionnée — le run peut "
              "démarrer.")
        return 0

    print("\n⛔ REFUS DE DÉMARRER — le prompt reçu diverge de "
          f"{args.ref}.\n")
    diff = list(difflib.unified_diff(ref, recu, fromfile=args.ref,
                                     tofile='prompt reçu', lineterm='',
                                     n=1))
    ajouts = sum(1 for l in diff if l.startswith('+') and not l.startswith('+++'))
    retraits = sum(1 for l in diff if l.startswith('-') and not l.startswith('---'))
    print(f"   {retraits} ligne(s) retirée(s), {ajouts} ajoutée(s)\n")
    for l in diff[:60]:
        print('   ' + l)
    if len(diff) > 60:
        print(f"   … {len(diff) - 60} lignes de diff supplémentaires")

    print("\n   Deux causes possibles, à distinguer avant de conclure :")
    print("   · la configuration de la tâche a dérivé   -> la réaligner "
          "sur la copie versionnée")
    print("   · le prompt a été amélioré volontairement -> porter le "
          "changement dans .loop/PROMPT.md par une PR, pour qu'il soit revu")
    print("\n   Dans les deux cas : NE PAS EXÉCUTER LE RUN.")
    return 1


if __name__ == '__main__':
    sys.exit(main())
