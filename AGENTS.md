# AGENTS.md — Norte-OS EU

## Autorité

La doctrine unique est `../_governance/` (`~/work/Sites/_governance/`). Lire `00-AUTHORITY.md` (carte des sujets, acteurs, règle d'autonomie) avant toute action, puis le fichier canonique du sujet traité. Ce fichier est une adaptation locale : il ne porte aucun fait métier. En cas d'écart, `_governance` l'emporte.

Les anciennes règles sont archivées dans `../_governance/ARCHIVE/2026-09-25-legacy-rules/` : historiques, non normatives. Les fichiers `MISSION_HERMES_*` et les rapports datés de ce dépôt sont historiques : Hermes, OpenClaw et MiniMax sont retirés de Norte.

## Périmètre

- Dépôt : `eletricista-urgente`
- Domaine : `eletricista-urgente.pt`
- Métier : électricité urgente
- Langue client : PT-PT
- Acteurs : Manus, Cue, Claude (rôles dans `00-AUTHORITY.md`)

## Règles locales

- Faits métier (tarifs, horaires, zones, téléphones, services, garanties, assurance, statut réglementaire) : uniquement depuis `../_governance/20-BUSINESS-FACTS.json`, jamais recopiés dans ce dépôt. Un fait absent n'existe pas : le demander à Filipe.
- Site électricité (`site_scope.EU`) : le statut public est `professional_status.public_wording_pt_pt`, repris mot pour mot ; une formation en cours n'est jamais présentée comme une qualification obtenue ; wallbox uniquement dans les conditions de `site_scope` et `services`. Aucun contenu, numéro, couleur ou équipement du métier plomberie (`10-SAFETY.md`).
- Ne pas inventer d'avis, de chantiers, de clients, de délais garantis ou de prix. Aucune zone Z1–Z6 et aucun calcul tarifaire par distance.
- Contexte éditorial local : `SEO_PLAN.md` et `MARKETING.md`, sans dupliquer la doctrine centrale.

## Git, preuve et publication

Suivre `../_governance/40-RUNBOOKS.md` : déclaration dans `../_coordination/REGISTRE.md`, un lot = une branche = un worktree en chemin absolu = une PR, ni réécriture d'historique ni force-push, statuts de preuve du done-gate. Merge, production et rollback : GO nommé de Filipe (dépôt + numéro de PR). Après modification, contrôler les générateurs, les pages produites et les prix visibles.
