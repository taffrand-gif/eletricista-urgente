# GATES.md — EU coverage cleanup 2026-11-25

BASE: 0dd88ef1ef2e56a5defb7417220da1d3d59734d7
HEAD: affd26436f485312d954b1288acd4036a807779a
FILES_SHA256: 898ec8534ef90481e4fd64b43c65d08cf8165919877ec45b5ab28caaecfbf365
POPULATION: 3 commercial HTML pages currently indexable or without a noindex directive (2 Spain, 1 Viseu)
BRANCH: cleanup/eu-coverage-cleanup-20261125

## Objectif mesurable (1 ligne)
Neutraliser uniquement les 3 pages EU prouvées hors périmètre, sans toucher à Vila Nova da Rainha ambiguë ni aux pages Chaves/Valpaços.

## Source active (preuve chemin:ligne — sinon « À REVOIR — SOURCE ACTIVE NON PROUVÉE »)
Pages HTML statiques servies depuis la racine du dptttt ; gnrateur actif `scripts/gen_sitemap.py:225-303` crit `sitemap.xml` (et `public/sitemap.xml` si prsent) ; source mtier

## Gate
- Motif exact : pages commerciales EU ciblées avec robots absent ou `index,follow` pour Espagne ou Viseu.
- Attendu (résiduel) : les 3 pages ciblées portent `noindex,follow`; aucune page Chaves/Valpaços modifiée; Vila Nova da Rainha reste inchangée.
- Témoins positifs : une page Espagne, une page Viseu, une page locale valide Chaves/Valpaços non touchée.
- Témoin négatif légitime (ne doit pas bouger) : pages Chaves, Valpaços, Moimenta déjà neutralisée, contenus installation/urgence, prix, téléphone, WhatsApp, CTA et JSON-LD métier.
- Invariants protégés (title, H1, meta, canonical, robots, JSON-LD, tel, WhatsApp, CTA, GA4, Consent Mode, RGPD, liens, prix, séparation métiers) — exceptions autorisées : aucune.
- Régénération : aucune source génératrice EU identifiée pour ces sorties statiques ; prouver par `git grep` avant le gate. Si une source active est découverte, STOP_SOURCE_INCONNUE.

## Chaîne de preuve visée
source → généré → build → HTTP → production (autorisée ? non)

## STOP autorisés (/loop continue sinon)
valeur métier manquante · conflit de PR · changement de base · population instable · rate limit · preview inaccessible · résultat non déterministe · périmètre dépassé

## Commande de clôture
À compléter avec le manifeste réel : `python3 ~/agents/done-gate/done-gate.py --repo /Users/admin/work/Sites/_worktrees/eu-coverage-cleanup-20261125 --base 0dd88ef1ef2e56a5defb7417220da1d3d59734d --ref HEAD --gates GATES.md`.
