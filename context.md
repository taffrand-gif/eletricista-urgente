# context.md — Loop State

> Écrit par le loop Cowork après chaque run. NE PAS ÉDITER MANUELLEMENT.

## Dernier run
- Date : 2026-06-29
- Tâche exécutée : B2 — Correction doublon public/index.html (canonical cassé + R12 violations)
- Branche créée : `loop/2026-06-29-eletricista-urgente-b2-doublon-homepage`
- PR ouverte : https://github.com/taffrand-gif/eletricista-urgente/pull/64
- Résultat : ✅ 1 commit, 1 fichier modifié. PR ouverte, attente merge Philippe.

## Tâche suivante recommandée
- Tâche : A2 — 8 pages /zonas/ prioritaires (eletricista-urgente-{braganca,vila-real,mirandela,chaves,...}.html)
- Priorité : CRITIQUE (selon SEO_PLAN)
- Note : Vérifier dans HISTORIQUE si Philippe a donné GO avant de commencer A2

## Apprentissages (self-improving)
- Pattern public/index.html doublon identique à canalizador-urgente → fix identique (cp index.html public/index.html)
- Ce site = 70€/h (PAS 65€/h) — NE PAS confondre avec les 3 autres sites
- A1 ✅ FAIT depuis 29/06 (PR #33+#35+#36) — SEO_PLAN.md déjà à jour pour A1

## Edge cases détectés
- Tarif spécifique : 70€/h pour eletricista-urgente (vs 65€/h sur les 3 autres sites)
- grep R8 : utiliser "70 €" (avec espace) — le site écrit "70 €/h" avec espace

## Blocages connus
- A2 (/zonas/) : vérifier GO Philippe avant exécution (8h d'effort, création de 8 fichiers)

## Instructions améliorées pour prochain run
1. Vérifier GO Philippe pour A2 dans HISTORIQUE SEO_PLAN.md avant de commencer
2. Pour A2 : créer 8 fichiers HTML statiques dans racine repo avec contenu Doctrine §12 (70€/h, Z1-Z6, équipement Fluke/Megger/FLIR, FAQ urgence, NAP 932 321 892)
3. ATTENTION : tarif = 70€/h sur ce site (pas 65€/h)
4. Si lock file git : `mcp__desktop-commander__start_process` avec `rm -f ~/work/Sites/eletricista-urgente/.git/*.lock && git ...`
