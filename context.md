# context.md — Loop State

> Écrit par le loop Cowork après chaque run. NE PAS ÉDITER MANUELLEMENT.

## Dernier run
- Date : 2026-06-30
- Tâche exécutée : R4 — FAQ schema calculadora-de-preco.html (prix + tel NAP)
- Branche créée : `loop/2026-06-30-eletricista-urgente-faq-schema-r4`
- PR ouverte : https://github.com/taffrand-gif/eletricista-urgente/pull/65
- Résultat : ✅ 2 commits, 1 fichier modifié. PR ouverte, attente merge Philippe.

## Tâche suivante recommandée
- Tâche : A2 — 8 pages /zonas/ prioritaires (eletricista-urgente-{braganca,vila-real,mirandela,chaves,...}.html)
- Priorité : CRITIQUE (selon SEO_PLAN)
- Statut : 🛑 STOP — attente GO explicite Philippe (ne pas créer sans validation)

## Apprentissages (self-improving)
- Pattern identique à canalizador-urgente : calculadora-de-preco.html avait "Desde 135 EUR" + "+351-" — même bug copié-collé entre les 2 sites urgents (corrigé PR #68 CU + PR #65 EU en même run)
- Ce site = 70€/h (PAS 65€/h) — NE PAS confondre avec les 3 autres sites
- grep R8 : utiliser "70 €" (avec espace) sur ce site
- A2 /zonas/ STOP attente Philippe — ne pas démarrer sans GO écrit dans HISTORIQUE

## Edge cases détectés
- Tarif spécifique : 70€/h pour eletricista-urgente (vs 65€/h sur les 3 autres sites)
- calculadora zones décalées vs AGENTS.md (possible intentionnel pour urgence vs normal) — ne pas toucher logique JS sans GO Philippe

## Blocages connus
- A2 (/zonas/ 8 pages) = 🛑 STOP attente GO Philippe

## Instructions améliorées pour prochain run
1. En DÉBUT de loop : grep "Desde [0-9]\|+351-\|Suplemento [0-9]" sur calculadora-de-preco.html des 4 sites (pattern récurrent R4)
2. Si GO A2 reçu : créer 8 fichiers HTML statiques avec Doctrine §12 (70€/h, Z1-Z6, Fluke/Megger/FLIR, FAQ urgence, NAP 932 321 892)
3. ATTENTION : tarif = 70€/h sur ce site (pas 65€/h)
4. Si lock file git : desktop-commander rm host-side
5. SITE COMPLET pour tâches autonomes — prochaine tâche = A2 sur GO Philippe
