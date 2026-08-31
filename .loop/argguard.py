#!/usr/bin/env python3
"""
argguard.py — détecte un argument effondré avant que l'outil ne conclue.

ZSH NE FAIT PAS DE WORD-SPLITTING. Une variable contenant
`--recu fichier.md` est passée comme UN SEUL argument, pas deux. L'outil
reçoit alors une valeur qui contient elle-même une option, et il rend un
verdict — refus, zéro, « rien à dispatcher » — qui décrit un appel
malformé, pas l'état du dépôt.

Trois occurrences le 30-31/08/2026, sur deux personnes différentes :
  · `$REG` valant `--registry /chemin` → argparse « unrecognized arguments »,
    un run de génération perdu ;
  · deux essais successifs de `check_prompt.py` où `--recu fichier.md`
    arrivait en positionnel → la garde semblait refuser tout.

Le piège est documenté dans les leçons du dépôt depuis des semaines et il
n'a empêché aucune des trois. C'est précisément la démonstration qu'une
leçon écrite ne protège pas : seul du code qui refuse le fait.

Usage dans un outil :
    from argguard import verifier_arguments
    verifier_arguments(args)      # après parse_args()
"""
import re
import sys

# Une valeur d'option qui contient elle-même une option : signature d'un
# argument effondré par l'absence de word-splitting.
EFFONDRE = re.compile(r'(^|\s)--?[A-Za-z]')


def verifier_arguments(args, code=4):
    """Refuse si une valeur d'argument contient elle-même une option.

    Rend un message qui dit explicitement que l'APPEL est en cause, pas
    ce que l'outil contrôle : un contrôle ambigu est pire qu'un contrôle
    absent, il produit de fausses certitudes dans les deux sens."""
    suspects = []
    for nom, val in vars(args).items():
        for v in (val if isinstance(val, (list, tuple)) else [val]):
            if isinstance(v, str) and ' ' in v and EFFONDRE.search(v):
                suspects.append((nom, v))
    if not suspects:
        return
    print("⚠️  APPEL MALFORMÉ — un argument contient lui-même une option :",
          file=sys.stderr)
    for nom, v in suspects:
        print(f"      --{nom.replace('_', '-')} = « {v} »", file=sys.stderr)
    print("\n    Cause probable : zsh ne fait PAS de word-splitting. Une\n"
          "    variable valant « --opt valeur » est passée comme UN seul\n"
          "    argument. Utiliser un tableau, ou brancher explicitement :\n"
          "        if [ -f \"$f\" ]; then outil --opt \"$f\"; else outil; fi\n"
          "\n    Ce n'est PAS un verdict sur le dépôt : rien n'a été "
          "contrôlé.", file=sys.stderr)
    sys.exit(code)
