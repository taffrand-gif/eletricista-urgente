#!/usr/bin/env python3
"""
verify_preview.py — porte de vérification, sur URL de preview.

À lancer sur la preview de chaque PR, AVANT merge : la règle `vercel.json`
n'a d'effet qu'une fois déployée.

LES CONTRÔLES POSITIFS SONT PAR REPO. Une page de contrôle codée en dur
pour un site n'existe pas sur les autres : `/blog/agua-amarela-torneira`
est une page de CU, et la tester sur EU rend 404 sur un patch pourtant
conforme. **Un contrôle positif qui échoue parce qu'il vise la mauvaise
page est un faux négatif de plus** — exactement ce que cette porte est
censée empêcher. Chaque site fournit donc ses propres pages, et l'outil
refuse de tourner si le repo n'est pas décrit.

Sortie non nulle si un seul contrôle échoue.

Usage:
    python3 verify_preview.py <url-preview> --repo eletricista-urgente
    python3 verify_preview.py <url-preview> --repo <nom> \\
        --positifs /page-qui-existe /autre --cibles /PRICING.md
"""
import argparse
import sys
import urllib.error
import urllib.request

# Cibles communes : doivent répondre 404 après le patch.
CIBLES_COMMUNES = ['/PRICING.md', '/SEO_PLAN.md', '/context.md']

# Contrôles positifs PAR REPO — doivent répondre 200. Une page de contenu
# réelle du site, plus les .txt qui restent volontairement servis.
REPOS = {
    'canalizador-urgente': {
        'positifs': ['/robots.txt', '/llms-full.txt',
                     '/blog/agua-amarela-torneira'],
        'cibles': ['/blog/agua-amarela-torneira.md',
                   '/blog/agua-quente-demora.md',
                   '/data/concelhos.json.bak-pre-zones-fix-2026-07-16'],
    },
    'eletricista-urgente': {
        'positifs': ['/robots.txt', '/llms-full.txt',
                     '/aumento-de-potencia'],
        'cibles': ['/blog/alarme-incendio-obrigatorio.md',
                   '/blog/cabo-eletrico-danificado-reparar.md',
                   '/og-image.png.bak-57645',
                   '/robots.txt.backup-2026-06-27'],
    },
    'eletricista-norte-reparos': {
        'positifs': ['/robots.txt', '/llms-full.txt', '/'],
        'cibles': ['/og-image.png.bak-57645'],
    },
    'canalizador-norte-reparos': {
        'positifs': ['/robots.txt', '/llms-full.txt', '/'],
        # Les 3 sitemaps de sauvegarde totalisent 8349 URLs crawlables sur
        # le dépôt dont le goulot est l'indexation.
        'cibles': ['/sitemap-dynamic.xml.bak-2026-08-12',
                   '/sitemap-plain.xml.bak-2026-08-12',
                   '/sitemap-priority.xml.bak-2026-08-12',
                   '/sitemap.xml.bak-2-4bis'],
    },
}


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
    ap = argparse.ArgumentParser()
    ap.add_argument('url')
    ap.add_argument('--repo', required=True)
    ap.add_argument('--positifs', nargs='*')
    ap.add_argument('--cibles', nargs='*')
    args = ap.parse_args()

    cfg = REPOS.get(args.repo)
    if cfg is None and not (args.positifs and args.cibles is not None):
        sys.exit(
            f"ERREUR: repo « {args.repo} » inconnu. Ajouter son entrée dans "
            "REPOS, ou passer --positifs et --cibles. Réutiliser les pages "
            "d'un autre site produirait un faux négatif.")
    cfg = cfg or {}
    positifs = args.positifs if args.positifs is not None else cfg['positifs']
    cibles = (args.cibles if args.cibles is not None
              else CIBLES_COMMUNES + cfg.get('cibles', []))

    if not positifs:
        sys.exit("ERREUR: aucun contrôle positif. Une porte sans contrôle "
                 "positif laisse passer un patch qui casse tout.")

    base = args.url.rstrip('/')
    print(f"Porte de vérification — {base}  ({args.repo})\n")

    echecs_cible, echecs_positif = [], []
    for path in cibles:
        got = statut(base + path)
        ok = got == 404
        if not ok:
            echecs_cible.append((path, got))
        print(f"  {'OK  ' if ok else 'ÉCHEC'}  {str(got):>5}  (attendu 404)  "
              f"{path}")
    print()
    for path in positifs:
        got = statut(base + path)
        ok = got == 200
        if not ok:
            echecs_positif.append((path, got))
        print(f"  {'OK  ' if ok else 'ÉCHEC'}  {str(got):>5}  (attendu 200)  "
              f"{path}   ← CONTRÔLE POSITIF")

    if echecs_cible:
        print("\n⚠️  Une cible répond encore : la règle vercel.json n'a pas "
              "pris. Vérifier qu'elle est EN TÊTE des rewrites — après le "
              "catch-all /(.*), elle n'est jamais atteinte.")
    if echecs_positif:
        print("\n🔴 Un contrôle POSITIF a échoué. Deux causes possibles, à "
              "distinguer avant de conclure :\n"
              "   · le patch casse du contenu servi        -> NE PAS MERGER\n"
              "   · la page de contrôle n'existe pas ici   -> corriger "
              "REPOS['" + args.repo + "'], le patch n'est pas en cause")

    n = len(cibles) + len(positifs)
    e = len(echecs_cible) + len(echecs_positif)
    print(f"\n{n - e}/{n} contrôles verts, dont {len(positifs)} positifs — "
          f"porte {'ouverte' if e == 0 else 'fermée'}.")
    return 1 if e else 0


if __name__ == '__main__':
    sys.exit(main())
