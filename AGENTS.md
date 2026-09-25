# AGENTS.md — Norte-OS EU

## Autorité

Les règles centrales sont dans `../_governance/` : lire `00-AUTHORITY.md`, `10-SAFETY.md`, `20-BUSINESS-FACTS.json`, `30-CONTENT-DOCTRINE.md` et `40-RUNBOOKS.md` avant toute action. Le détail de migration de ce dépôt est dans `NORTE-GOVERNANCE.md`.

Les anciennes règles ont été archivées dans `../_governance/ARCHIVE/2026-09-25-legacy-rules/`. Elles sont historiques et ne font plus autorité.

## Périmètre

- Dépôt : `eletricista-urgente`
- Domaine : `eletricista-urgente.pt`
- Métier : électricité urgente
- Langue client : PT-PT

## Règles locales

Le statut public actif est : `Eletricista credenciado pela DGEG — Técnico Responsável de Instalações Elétricas, TRIESP n.º 90062. Execução em Baixa Tensão até 41,4 kVA.` Le niveau 4 RTA de 925 heures est une formation en cours, pas une qualification déjà obtenue. Le futur périmètre 30 kV / 250 kVA n’est pas actif.

Le wallbox est un service possible sous devis dans le périmètre applicable. Ne pas inventer d’avis, de chantiers, de clients, de délais garantis ou de prix.

Appliquer exclusivement le modèle tarifaire central : 70 €/h + 30 € en semaine 09:00–17:00 ; 100 €/h + 50 € la nuit, les week-ends et jours fériés. Aucune zone Z1–Z6 et aucun calcul tarifaire par distance.

Lire `SEO_PLAN.md` et `MARKETING.md` pour le contexte éditorial local. Consigner les actions dans l’historique prévu par le plan, sans dupliquer la doctrine centrale.

## Git et contrôle

Travailler sur une branche identifiée. Ne jamais réécrire l’historique ni forcer un push. Aucun merge ou déploiement sans validation explicite de Filipe. Après modification, contrôler les générateurs, les pages produites et les prix visibles.
