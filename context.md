# context.md — Loop State

> Écrit par le loop Cowork après chaque run. NE PAS ÉDITER MANUELLEMENT.

## Dernier run
- Date : 2026-07-18
- Tâche exécutée : IndexNow J1 — régénération `eletricista-urgente-indexnow-urls.txt` (liste stale depuis 03/07, homepage manquante + 185 URLs sitemap manquantes + 25 URLs blog obsolètes retirées)
- Branche créée : `loop/2026-07-18-eu-indexnow-urls-v2` (branche `loop/2026-07-18-eu-indexnow-urls-refresh` initiale ABANDONNÉE — contaminée par un commit tiers concurrent, voir Apprentissages)
- PR ouverte : https://github.com/taffrand-gif/eletricista-urgente/pull/160 (PR #159 fermée, contaminée, voir plus bas)
- Résultat : ✅ 2 commits, 2 fichiers modifiés (`eletricista-urgente-indexnow-urls.txt` + `SEO_PLAN.md`). PR #160 ouverte, attente merge Philippe. Soumission API réelle à `api.indexnow.org` **NON faite** (hors scope — action infra, GO Philippe requis, AGENTS.md Règle 1).

## Tâche suivante recommandée
- Tâche : soumission effective à `api.indexnow.org` (host=eletricista-urgente.pt, key=`b9ca6de7944da3053a9868c7b9eb92eb`, urlList=`eletricista-urgente-indexnow-urls.txt` 1989 URLs) — **après GO explicite Philippe** (AGENTS.md Règle 1, double confirmation infra/API)
- Priorité : moyenne (prep déjà faite, juste l'appel API à valider)
- Autre piste si GO IndexNow pas donné : A4-TER dette (76 "Atendimento prioritário" + 1 défaut alij.html + claims §11, ~80 fichiers) mentionnée SEO_PLAN.md ligne "Prochaine action" — Philippe doit décider safe-drop vs PR dédiée
- Statut blog resurrection (58 MD) : 🛑 BLOQUÉ conformité (SEO_PLAN 2026-07-13) — attente décision Philippe (autoriser réécriture éditoriale sourcée ou annuler)
- Statut curto-circuito dedup FAQ (SEO_PLAN 2026-07-17, branche `feat/monopole-piliers-eu`) : 🟡 à pusher + attendre GO merge (non touché par ce run, hors scope)

## Apprentissages (self-improving)
- **⚠️ CONCURRENCE CONFIRMÉE sur ce repo** : pendant ce run (2026-07-18), un autre processus/agent (tâche identifiée "QW-P0.1.2", commit `e6d468e29` "harmoniser llms.txt bornes km avec SOT TomTom") a opéré sur le MÊME checkout local `~/work/Sites/eletricista-urgente` en parallèle, checkoutant d'autres branches entre mes commandes et poussant un commit sur ma branche `loop/2026-07-18-eu-indexnow-urls-refresh`. Récupéré SANS `push --force` (R6) : cherry-pick de mes 2 commits propres vers une nouvelle branche `loop/2026-07-18-eu-indexnow-urls-v2`, nouveau PR #160, PR #159 fermé (commenté, pas supprimé — le commit tiers reste intact et accessible).
- **Prochain run DOIT** : vérifier `git branch --show-current` juste avant CHAQUE commit/push (pas seulement en début de run) pour détecter une collision de branche. Utiliser systématiquement `gh pr create --head <branche-explicite>` (pas de dépendance au HEAD courant). Si une branche `loop/*` contient un fichier ou commit non attendu (`git diff origin/main..HEAD --name-only` doit lister UNIQUEMENT les fichiers du run), repartir d'une branche propre par cherry-pick plutôt que force-push.
- La note SEO_PLAN.md "❌ Pas de fichier indexnow-key.txt ni indexnow-urls.txt à la racine EU" (section ÉTAT POST-FOURNÉE 17/07) était **fausse/obsolète** : `indexnow-key.txt` + fichier de vérification existent et sont trackés depuis le 03/07 (commit `9142d3067`, mission M10). Corrigé dans SEO_PLAN HISTORIQUE 2026-07-18.
- `eletricista-urgente-indexnow-urls.txt` n'est pas régénéré automatiquement quand `sitemap-villages.xml` grossit (ex. batch P1C 200 villages du 17/07 → +118 URLs non reflétées). Prévoir un script de régénération automatique ou refaire ce contrôle à chaque gros batch de pages avant toute soumission IndexNow.
- Ce site = 70€/h (PAS 65€/h) — NE PAS confondre avec les 3 autres sites. Grille Z1-Z6 vérifiée cohérente dans `llms.txt` avant contamination (0–15/15–30/30–50/50–70/70–90/90–140 km selon le commit tiers `e6d468e29`, à valider — pas mon périmètre ce run).
- docs/seo-plan-update (branche visible au début du run) = déjà mergée dans main via PR #158 (même contenu, squash) → rien à faire, confirmé par comparaison `git log origin/main..origin/docs/seo-plan-update`.

## Edge cases détectés
- Tarif spécifique : 70€/h pour eletricista-urgente (vs 65€/h sur les 3 autres sites) — non touché ce run
- Concurrence multi-agent sur le même checkout local (voir Apprentissages) — risque à surveiller sur les prochains runs

## Blocages connus
- Soumission API IndexNow réelle : attente GO Philippe (fichier prêt, PR #160)
- Blog resurrection 58 MD : 🛑 BLOQUÉ conformité, attente décision Philippe (autoriser réécriture sourcée ou annuler)
- A2 (/zonas/ 8 pages, ancien blocage 30/06) : probablement obsolète (33 hubs concelhos + 200 villages P1C déjà livrés depuis, cf SEO_PLAN état 17/07) — à re-vérifier au prochain run avant de le considérer encore actif
- curto-circuito dedup FAQ (branche `feat/monopole-piliers-eu`) : 🟡 à pusher + GO merge, non traité ce run (hors scope de la tâche IndexNow)

## Instructions améliorées pour prochain run
1. **Vérifier `git branch --show-current` avant CHAQUE commit/push**, pas seulement au début — ce repo semble partagé avec d'autres processus concurrents en temps réel.
2. Toujours utiliser `gh pr create --head <branche-explicite>` plutôt que compter sur le HEAD courant.
3. Après tout push, faire `git diff origin/main..<branche>--name-only` pour vérifier qu'aucun fichier hors scope ne s'est glissé dans la branche avant d'ouvrir le PR.
4. Trust HISTORIQUE > TODO/ÉTAT sections dans SEO_PLAN.md, mais vérifier aussi contre la réalité du repo (`git ls-files`, `wc -l`) — au moins une note d'état (indexnow-key.txt) s'est révélée fausse.
5. Tarif = 70€/h sur ce site (pas 65€/h).
6. Si lock file git : desktop-commander `rm -f .git/*.lock` host-side.
