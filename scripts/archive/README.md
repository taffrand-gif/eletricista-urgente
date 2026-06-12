# Archive — scripts one-shot

Ce dossier contient des scripts utilisés **une seule fois** lors d'opérations
de maintenance (lots de correction SEO, suppressions en masse, etc.) et qui
ne sont plus exécutés en routine.

## Contenu

- `lot1-remove-fake-schema.py` — Lot 1, suppression des JSON-LD frauduleux
  (avis Google inventés, schémas Plumber/Electrician avec fausses données)
  sur les pages des 2 sites principaux. Exécuté en juin 2026.

- `lot1-skipped-files.log` — Log des fichiers skippés durant le Lot 1
  (JSON-LD déjà cassé en pré-existant, repris dans le Lot 7.5).

## Pourquoi archivés et non supprimés

- **Traçabilité** : si un pattern de JSON-LD frauduleux réapparaît, le
  script peut servir de référence / base pour un nouveau passage.
- **Audit** : démontrer ce qui a été nettoyé en cas de revue qualité.
- **Ne PAS re-exécuter** sans avoir relu le code : les IDs de pages et
  les patterns ont évolué.

## Maintenance future

Tout nouveau script one-shot doit être placé ici après utilisation,
nommé `lot{N}-{action}.{ext}` avec un log associé `lot{N}-skipped-files.log`
si applicable.
