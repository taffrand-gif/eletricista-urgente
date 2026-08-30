#!/usr/bin/env python3
"""
verify_preview.py — porte de vérification du patch .md, sur URL de preview.

À lancer par Hermes sur l'URL de preview de chaque PR, AVANT merge. Le
patch ne se valide pas sur la confiance : la règle `vercel.json` n'a
d'effet qu'une fois déployée.

Les deux derniers contrôles sont POSITIFS et non négociables : sans eux,
un patch qui renverrait 404 sur tout passerait la porte. Un zéro sans
contrôle positif dans la même exécution ne vaut rien.

Sortie non nulle si un seul contrôle échoue.

Usage:
    python3 verify_preview.py https://<preview>.vercel.app
"""
import sys
import urllib.error
import urllib.request

# (chemin, statut attendu, rôle)
CONTROLES = [
    ('/PRICING.md',                     404, 'cible — doctrine/prix'),
    ('/blog/agua-amarela-torneira.md',  404, 'cible — doublon du HTML'),
    ('/blog/agua-quente-demora.md',     404, 'cible — orphelin, sans jumeau'),
    ('/robots.txt',                     200, 'CONTRÔLE POSITIF — .txt intact'),
    ('/llms-full.txt',                  200, 'CONTRÔLE POSITIF — .txt intact'),
    ('/blog/agua-amarela-torneira',     200, 'CONTRÔLE POSITIF — page HTML survit'),
]


def statut(url):
    req = urllib.request.Request(url, method='GET',
                                 headers={'User-Agent': 'norte-reparos-gate'})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:                      # noqa: BLE001
        return f'ERR {e}'


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    base = sys.argv[1].rstrip('/')
    print(f"Porte de vérification — {base}\n")

    echecs = []
    for path, attendu, role in CONTROLES:
        got = statut(base + path)
        ok = got == attendu
        if not ok:
            echecs.append((path, attendu, got))
        print(f"  {'OK  ' if ok else 'ÉCHEC'}  {str(got):>5}  "
              f"(attendu {attendu})  {path}\n         {role}")

    if any(p.endswith('.md') for p, *_ in echecs):
        print("\n⚠️  Une cible .md répond encore : la règle vercel.json n'a "
              "pas pris. Vérifier qu'elle est bien EN TÊTE des rewrites — "
              "placée après le catch-all /(.*), elle n'est jamais atteinte.")
    if any(not p.endswith('.md') for p, *_ in echecs):
        print("\n🔴 Un contrôle POSITIF a échoué : le patch casse du contenu "
              "servi. NE PAS MERGER.")

    if echecs:
        print(f"\n{len(echecs)} échec(s) — porte fermée.")
        return 1
    print(f"\n{len(CONTROLES)} contrôles verts, dont 3 positifs — "
          "porte ouverte.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
