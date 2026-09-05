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

L'ENVELOPPE — le 02/09/2026, la garde a refusé quatre dépôts d'affilée
alors que le corps du prompt était identique au bit près. L'écart venait
de l'empaquetage : la tâche planifiée transporte le prompt sous forme de
fichier de skill, et préfixe un frontmatter YAML `name` + `description`.

Ce frontmatter n'est pas inerte : la `description` reçue portait
« Premier run : RAPPORT seul », c'est-à-dire une directive de fond. C'est
exactement le canal hors git contre lequel cette garde existe. L'ignorer
rendrait la garde verte en laissant le canal invisible.

D'où : le frontmatter est détaché du corps, AFFICHÉ en entier, et comparé
à `.loop/ENVELOPPE.md` — versionné et gaté par PR comme le reste. Une
clé hors de {name, description}, ou une valeur qui diverge du pin, est
un refus au même titre qu'une dérive du corps.

Codes de sortie — distincts à dessein, pour qu'un mauvais appel ne
ressemble pas à un refus de conformité :
    0  prompt conforme
    1  DIVERGENCE — refus de démarrer (corps OU enveloppe)
    3  un des deux fichiers est introuvable
    4  appel malformé (fichier passé en positionnel)

Usage:
    python3 check_prompt.py --recu prompt-recu.md [--ref .loop/PROMPT.md]
                            [--ref-enveloppe .loop/ENVELOPPE.md]
"""
import argparse
import difflib
import hashlib
import os
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from argguard import verifier_arguments


def normaliser(texte):
    lignes = [l.rstrip() for l in texte.replace('\r\n', '\n').split('\n')]
    while lignes and not lignes[-1]:
        lignes.pop()
    return lignes


def empreinte(lignes):
    return hashlib.sha256('\n'.join(lignes).encode('utf-8')).hexdigest()


# normaliser() absorbe TROIS choses, et il a fallu les distinguer avant d'en
# retirer une :
#   1. `\r\n` -> `\n`   — artefact de TRANSPORT. Une fin de ligne Windows ne
#      change pas ce que le prompt dit ; refuser dessus donnerait un rouge
#      permanent que personne ne peut réparer. CONSERVÉE.
#   2. `rstrip()` par ligne — retire les espaces de fin de CHAQUE ligne.
#   3. le retrait des lignes vides TERMINALES.
#
# Les points 2 et 3 masquent une mutilation du corps. Le 05/09/2026, un
# `update_scheduled_task` ne portant que `description` a re-sérialisé la
# configuration et mangé le newline final du corps (158 -> 157 lignes). La
# garde est restée VERTE : les deux côtés perdaient leur ligne vide terminale,
# donc plus rien ne les distinguait. C'est le troisième « vert pour la
# mauvaise raison » de la journée, après un `$?` capturé derrière un `| head`
# et un `rev-parse` fatal lu comme « travail hors main ».
#
# Un corps mutilé n'est pas le corps revu par PR. Un run qui s'arrête se
# répare en une commande ; un run parti sur un prompt silencieusement altéré,
# non. Le corps est donc désormais comparé OCTET À OCTET.
def normaliser_transport(texte):
    """La seule tolérance conservée pour le corps : CRLF -> LF."""
    return texte.replace('\r\n', '\n')


def corps_brut(texte):
    """Corps du prompt tel quel : ni rstrip, ni retrait de lignes vides
    terminales.

    Les lignes vides qui SUIVENT le délimiteur fermant du frontmatter sont
    seules retirées — elles appartiennent à la séparation entre l'enveloppe
    et le corps, pas au corps. C'est la même règle que detacher_enveloppe(),
    et elle porte sur le début, jamais sur la fin.
    """
    t = normaliser_transport(texte)
    lignes = t.split('\n')
    if lignes and lignes[0] == '---':
        for i in range(1, len(lignes)):
            if lignes[i] == '---':
                reste = lignes[i + 1:]
                while reste and not reste[0]:
                    reste.pop(0)
                return '\n'.join(reste)
    return t


def premier_ecart(a, b):
    """Position du premier octet qui diffère, et son voisinage lisible."""
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return i, repr(a[max(0, i - 20):i + 20]), repr(b[max(0, i - 20):i + 20])
    i = min(len(a), len(b))
    return i, repr(a[max(0, i - 20):]), repr(b[max(0, i - 20):])


CLES_EMPAQUETAGE = ('name', 'description')

# Le `description` du frontmatter est INJECTÉ dans le prompt au chargement
# du skill : c'est un canal d'instruction, pas une étiquette. Le 05/09/2026
# il annonçait « RAPPORT SEUL » alors que le corps autorisait déjà une PR
# sur ENR. La garde rendait vert parce qu'elle compare chaque couche à SA
# référence, jamais les deux couches entre elles — le vert portait sur la
# mauvaise question.
#
# Le périmètre vit dans le corps, seule couche revue par PR. Ce prédicat
# empêche la couche enveloppe de redevenir prescriptive. Il ne cherche PAS
# à comprendre la description : il constate la présence de mots par lesquels
# un périmètre s'énonce. C'est grossier, et c'est le but — une garde qui
# interprète du texte libre est une garde qu'on ne peut plus auditer.
TERMES_PRESCRIPTIFS = ('rapport', 'autoris', 'interdit')

# Nommer un dépôt dans la description, c'est déjà trancher un périmètre.
DEPOTS = ('canalizador-norte-reparos', 'eletricista-norte-reparos',
          'canalizador-urgente', 'eletricista-urgente')


def plier(texte):
    """Minuscules, accents retirés — pour que AUTORISÉES, autorisées et
    Autorise soient le même mot aux yeux du prédicat. Sans ce pliage, la
    forme même qui figurait dans PROMPT.md (« AUTORISÉES ») passerait."""
    return ''.join(c for c in unicodedata.normalize('NFD', texte.lower())
                   if unicodedata.category(c) != 'Mn')


def valeur_cle(enveloppe, cle):
    """Valeur d'une clé de premier niveau du frontmatter, ou None."""
    for ligne in enveloppe[1:-1]:
        if ligne.startswith(cle + ':'):
            return ligne.split(':', 1)[1].strip()
    return None


def controler_description(enveloppe):
    """La description ne doit énoncer aucun périmètre. Rend True si elle est
    acceptable, False si c'est un refus."""
    description = valeur_cle(enveloppe, 'description')
    if description is None:
        return True
    plie = plier(description)
    trouves = ([t for t in TERMES_PRESCRIPTIFS if t in plie]
               + [d for d in DEPOTS if d in plie])
    if not trouves:
        return True
    print("⛔ REFUS DE DÉMARRER — la `description` de l'enveloppe énonce un "
          "périmètre :")
    print("   " + ', '.join(trouves))
    print("   Cette description est injectée dans le prompt au chargement : "
          "c'est une")
    print("   instruction. Le périmètre appartient au corps, seule couche "
          "revue par PR.")
    print("   Deux couches qui portent la même décision finissent par en "
          "porter deux.")
    return False



def detacher_enveloppe(lignes):
    """Sépare un frontmatter YAML de tête du corps du prompt.

    Rend (enveloppe, corps). `enveloppe` vaut None si le texte n'en porte
    pas — auquel cas `corps` est rendu inchangé.

    Les lignes vides qui suivent le délimiteur fermant sont retirées du
    corps : elles appartiennent à la séparation, pas au prompt. C'est la
    SEULE tolérance ajoutée, et elle ne masque rien puisque l'enveloppe
    détachée est affichée et comparée séparément.
    """
    if not lignes or lignes[0] != '---':
        return None, lignes
    for i in range(1, len(lignes)):
        if lignes[i] == '---':
            corps = lignes[i + 1:]
            while corps and not corps[0]:
                corps.pop(0)
            return lignes[:i + 1], corps
    # Délimiteur ouvrant sans fermant : ce n'est pas une enveloppe, c'est
    # du corps. Ne rien détacher plutôt que deviner.
    return None, lignes


def cles_enveloppe(enveloppe):
    """Clés YAML de premier niveau du frontmatter, dans l'ordre rencontré."""
    cles = []
    for ligne in enveloppe[1:-1]:
        if ligne.startswith((' ', '\t', '-')) or ':' not in ligne:
            continue
        cles.append(ligne.split(':', 1)[0].strip())
    return cles


def controler_enveloppe(enveloppe, chemin_ref):
    """Affiche l'enveloppe reçue et décide si elle autorise le démarrage.

    Rend True si le run peut continuer, False si c'est un refus.
    """
    print("\n📦 ENVELOPPE D'EMPAQUETAGE reçue hors git — "
          "reproduite ici en entier :\n")
    for ligne in enveloppe:
        print('   │ ' + ligne)
    print()

    inattendues = [c for c in cles_enveloppe(enveloppe)
                   if c not in CLES_EMPAQUETAGE]
    if inattendues:
        print("⛔ REFUS DE DÉMARRER — l'enveloppe porte une ou des clés hors "
              "de l'empaquetage attendu :")
        print("   " + ', '.join(inattendues))
        print(f"   Attendu : {', '.join(CLES_EMPAQUETAGE)} et rien d'autre.")
        print("   Une clé supplémentaire est une instruction qui n'est passée "
              "par aucune revue.")
        return False

    if not controler_description(enveloppe):
        return False

    if not os.path.exists(chemin_ref):
        print(f"⛔ REFUS DE DÉMARRER — {chemin_ref} est absent : rien ne "
              "permet de dire\n"
              "   que cette enveloppe a été revue.")
        print("   Le contenu à épingler par PR, tel que reçu, est reproduit "
              "ci-dessus.")
        return False

    ref = normaliser(open(chemin_ref, encoding='utf-8').read())
    if enveloppe != ref:
        print(f"⛔ REFUS DE DÉMARRER — l'enveloppe diverge de {chemin_ref}.\n")
        for l in difflib.unified_diff(ref, enveloppe, fromfile=chemin_ref,
                                      tofile='enveloppe reçue', lineterm='',
                                      n=1):
            print('   ' + l)
        print("\n   La `description` de ce frontmatter porte du texte "
              "directif. Une divergence")
        print("   est donc un changement d'instruction, pas une variation "
              "cosmétique : la porter")
        print(f"   dans {chemin_ref} par une PR, ou réaligner "
              "l'empaquetage.")
        return False

    print(f"✅ Enveloppe conforme à {chemin_ref}.")
    return True


def main():
    ap = argparse.ArgumentParser(
        description="Compare le prompt reçu à .loop/PROMPT.md. "
                    "Divergence = refus de démarrer.")
    # Volontairement NON required : sinon argparse échoue avant d'atteindre
    # le diagnostic ci-dessous, et rend un message générique là où l'appelant
    # a besoin de savoir que son appel — et non le prompt — est en cause.
    ap.add_argument('--recu',
                    help='fichier contenant le prompt effectivement reçu')
    ap.add_argument('--ref', default=os.path.join('.loop', 'PROMPT.md'),
                    help='copie versionnée (défaut : .loop/PROMPT.md)')
    ap.add_argument('--ref-enveloppe',
                    default=os.path.join('.loop', 'ENVELOPPE.md'),
                    help='frontmatter d\'empaquetage épinglé '
                         '(défaut : .loop/ENVELOPPE.md)')
    # Attrape l'appel positionnel au lieu de le laisser mourir en
    # « unrecognized arguments ». Une invocation fausse rendait le MÊME
    # code de sortie qu'un refus légitime : le testeur voyait une garde
    # qui refuse tout, c'est-à-dire une garde qui semble cassée. Un outil
    # de contrôle doit rendre son propre mauvais usage évident.
    ap.add_argument('positionnel', nargs='?', help=argparse.SUPPRESS)
    args = ap.parse_args()
    verifier_arguments(args)

    if args.positionnel and not args.recu:
        print(f"⚠️  APPEL MALFORMÉ — « {args.positionnel} » a été passé en "
              "positionnel.\n"
              "    Ce n'est PAS un refus de conformité : la garde n'a rien "
              "comparé.\n"
              f"    Utiliser : check_prompt.py --recu {args.positionnel}",
              file=sys.stderr)
        return 4
    if not args.recu:
        print("⚠️  APPEL MALFORMÉ — --recu est obligatoire.\n"
              "    Ce n'est PAS un refus de conformité : la garde n'a rien "
              "comparé.\n"
              "    Utiliser : check_prompt.py --recu <prompt-reçu.md>",
              file=sys.stderr)
        return 4

    for p in (args.recu, args.ref):
        if not os.path.exists(p):
            print(f"⛔ REFUS DE DÉMARRER — {p} introuvable.", file=sys.stderr)
            print("   Sans les deux versions, la comparaison n'a pas de sens "
                  "et l'absence ne vaut pas conformité.", file=sys.stderr)
            return 3

    brut_recu = open(args.recu, encoding='utf-8').read()
    brut_ref = open(args.ref, encoding='utf-8').read()
    recu = normaliser(brut_recu)
    ref = normaliser(brut_ref)
    corps_recu = corps_brut(brut_recu)
    corps_ref = normaliser_transport(brut_ref)

    # L'enveloppe est détachée AVANT la comparaison du corps, mais son
    # contrôle est un refus à part entière : une enveloppe non revue
    # arrête le run même quand le corps est conforme.
    enveloppe, recu = detacher_enveloppe(recu)
    h_recu, h_ref = empreinte(recu), empreinte(ref)

    print(f"prompt reçu     sha256 {h_recu[:16]}…  {len(recu)} lignes"
          + ("  (corps, enveloppe détachée)" if enveloppe else ""))
    print(f"copie versionnée sha256 {h_ref[:16]}…  {len(ref)} lignes")

    enveloppe_ok = True
    if enveloppe:
        enveloppe_ok = controler_enveloppe(enveloppe, args.ref_enveloppe)

    if h_recu == h_ref and corps_recu != corps_ref:
        pos, vu_ref, vu_recu = premier_ecart(corps_ref, corps_recu)
        print("\n⛔ REFUS DE DÉMARRER — le corps est identique LIGNE À LIGNE "
              "mais pas OCTET À OCTET.\n")
        print(f"   {args.ref} : {len(corps_ref)} octets")
        print(f"   prompt reçu : {len(corps_recu)} octets")
        print(f"   premier écart à l'octet {pos}")
        print(f"     attendu : {vu_ref}")
        print(f"     reçu    : {vu_recu}\n")
        print("   Un corps rogné n'est pas le corps revu par PR, même si le "
              "texte semble le même.")
        print("   Cause connue : une mise à jour de la tâche planifiée qui ne "
              "porte QUE `description`")
        print("   re-sérialise la configuration et mange le newline final du "
              "corps.\n")
        print("   ➡️  Renvoyer le champ `prompt` EN ENTIER, jamais la seule "
              "`description`.")
        return 1

    if h_recu == h_ref:
        if not enveloppe_ok:
            print("\n   Le CORPS du prompt, lui, est conforme : l'écart porte "
                  "uniquement sur\n"
                  "   l'enveloppe. NE PAS EXÉCUTER LE RUN pour autant.")
            return 1
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
    # Le diff est illisible sans son sens de lecture. Un opérateur qui
    # recopie le mauvais côté dans la tâche planifiée reproduit ce refus
    # mot pour mot — et le second essai ressemble alors à une garde
    # cassée plutôt qu'à une erreur de manipulation. Un outil de contrôle
    # doit nommer son propre remède.
    print(f"   SENS DE LECTURE — les lignes « - » sont {args.ref}, "
          "la copie versionnée :")
    print("   c'est CE côté qu'il faut recopier dans la tâche planifiée.")
    print("   Les lignes « + » sont le prompt reçu, c'est-à-dire le texte "
          "encore envoyé.\n")
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
