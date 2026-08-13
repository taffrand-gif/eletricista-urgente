# context.md — Loop State

> Écrit par le loop Cowork après chaque run. NE PAS ÉDITER MANUELLEMENT.

## Dernier run
- Date : 2026-08-13
- Tâche exécutée : **tâche n°4 du `context.md` (« sans GO »)**, réorientée : le gisement prix ayant été refermé, le run a porté sur le **gisement FAQ** — audit par parsing + prototype sur une page.
- Branche : `loop/2026-08-13-eletricista-urgente-faq-vide-prototype-braganca` (depuis `origin/main`, **en worktree**)
- Commits : `af04ccabd` (`garantia.html`), puis le commit `SEO_PLAN.md`
- PR ouverte : https://github.com/taffrand-gif/eletricista-urgente/pull/284 — **mergeable ✅**
- Résultat : ✅ 1 fichier de production. **Et deux constats qui changent l'état du repo.**

## ✅ BLOCAGE n°1 CLOS — le gisement prix n'existe plus
La PR **#281** (« recalc derived totals — remove +15€ artefact + publish "Mínimo faturado" »), **mergée le 13/08**, a refermé le gisement des 301 fichiers. Vérification de cohérence sur les **303 occurrences** appariées `deslocação + 70€/h → A partir de` :

| Zone | Deslocação | Total annoncé | Attendu | Écart | Occ. |
|---|---:|---:|---:|---:|---:|
| Z1 | 15 € | 85 € | 85 € | **0** ✅ | 10 |
| Z2 | 25 € | 95 € | 95 € | **0** ✅ | 36 |
| Z3 | 35 € | 105 € | 105 € | **0** ✅ | 58 |
| Z4 | 45 € | 115 € | 115 € | **0** ✅ | 42 |
| Z5 | 55 € | 125 € | 125 € | **0** ✅ | 82 |
| Z6 | 65 € | 135 € | 135 € | **0** ✅ | 75 |

➡️ **L'écart de +15 € est nul sur les 6 zones. Le « plus grave du repo » est réglé.** Les prototypes PR #268 et PR #277 ont servi leur but : la ventilation par zone a rendu la décision possible, le batch a été autorisé et exécuté correctement. **Patron à réutiliser sur CU.**

## 🔴 Le diagnostic « les scripts `r12_*.py` ont produit les FAQ vides » est RÉFUTÉ
Contrôle demandé par le `context.md` du 12/08 (nuance venue de CU) : **`conforme zona Z` = 0 occurrence en production sur EU.**
➡️ Même conclusion que sur CU : **la chaîne défectueuse des scripts versionnés n'a jamais atteint la production.** Le défaut vient d'une passe absente du repo.
➡️ **Conséquence : corriger `scripts/r12_blog_safe_cleanup.py` et `scripts/r12_hubs_cleanup.py` n'est PAS un prérequis du batch FAQ.** C'est une hygiène séparée. **Le blocage n°2 perd sa condition suspensive technique.**

## 🔴 Le chiffre « 955 FAQ vides » comptait DEUX gisements différents
Parsing exhaustif de tous les blocs `application/ld+json` (`_archive/` exclu) : **0 bloc non parsable**, **4 219 `acceptedAnswer`** au total.

| Gisement | Fichiers | Nature |
|---|---:|---|
| `acceptedAnswer.text` == `" conforme zona"` | **526** | réponse vide — Question « Quanto tempo demoram a chegar? », **une seule valeur exacte, zéro variante** |
| `"name": "Trabalham Atendimento 24h/7d?"` | **955** | 🆕 **artefact dans le NOM DE LA QUESTION**, jamais documenté |

➡️ **Le « 955 » suivi run après run n'était pas le nombre de FAQ vides.** Les réponses vides sont **526**. Les 955 sont un **second gisement, distinct** : la substitution `24h` → `Atendimento 24h/7d` a été appliquée à une question qui portait **déjà** `24h/7d`, produisant « Trabalham **Atendimento 24h/7d**? » — agrammatical, **et affiché en rich snippet**.
➡️ **Ceci explique le « 955 → 955 » noté comme suspect le 12/08 : le compteur suivait le mauvais gisement.**
➡️ **La cible (b1) est donc parfaitement propre : 526 fichiers, une seule valeur exacte, zéro faux positif, zéro variante à traiter à part.**

## ✅ Gate merge — aucun gate actif
Vérifié ce run : aucune mention d'attente dans les 4 `context.md`. **CNR #300 a été mergée pendant le run** ; #284 (ici), #334 (ENR) et #260 (CU) sont ouvertes et **toutes mergeables**.

🔴 **Rappel de doctrine, à ne jamais réécrire** : R7 interdit de **MERGER**, pas de **PRODUIRE**. Entre le 06/08 et le 09/08, la mention « Attente GO merge (R7) » a été relue chaque nuit comme un ordre d'arrêt → **4 runs sans production**.

## Prototype livré — `garantia.html`
Page de confiance, **déclarée au sitemap**, **sans jumelle `public/`** — le prototype ne s'enchevêtre pas avec le blocage n°5 (doublon `public/` ↔ racine). Même critère de choix que la PR #277.
1. **Q « Quanto tempo demoram a chegar? »** → réponse `" conforme zona"` (14 car.) → **retrait du couple Q/R** (question de délai, patron validé par le merge de la PR #200).
2. **Question « Trabalham Atendimento 24h/7d? » → « Trabalham 24h/7d? »** — restauration **verbatim** depuis le jumeau `canalizador-urgente` (`contactos.html`, même Question, non affectée).
- ⚠️ **La réponse n'est pas touchée : R145 autorise explicitement « 24h/7 dias » sur ce repo** (`AGENTS.md` L184). Rien n'est sur-purgé.
- Témoins R8 (avant → après) : ` conforme zona` **1→0** · `Quanto tempo demoram a chegar` **1→0** · `Trabalham Atendimento 24h/7d` **1→0** · `Trabalham 24h/7d` **0→1** · `24h` **2→2** et `Curto-circuitos` **1→1** (contrôles positifs).
- Contrôle post-purge : **4/4 blocs JSON-LD re-parsés valides**, 2 questions, **0 `acceptedAnswer.text` ≤ 20 caractères**.
- ⚠️ **Note de sélection** : `eletricista-braganca.html` (prototype de la PR #277) **n'est PAS dans le gisement** — son ` conforme zona` est dans une phrase légitime (« 15-35€ deslocação conforme zona »). **Ne pas le re-flaguer.**

## 🛑 DÉCISIONS REQUISES — chiffres corrigés

| # | Cible | Fichiers | Traitement | Verrou restant |
|---|---|---:|---|---|
| **(b1)** | `acceptedAnswer.text` == `" conforme zona"` | **526** | retrait du couple Q/R (prototype PR #284) | **aucun** — valeur unique, 0 variante |
| **(b2)** | `"name": "Trabalham Atendimento 24h/7d?"` | **955** | → `"Trabalham 24h/7d?"` (verbatim CU) | **aucun** — substitution déterministe |
| (c) | `scripts/gen_concelhos.py` | 1 | délai chiffré (`faq_time()` L170-174) + claims 24h (L143/L148) + « relatório técnico » (L149, banni ruling Filipe 08/07) | **régénère à chaque exécution** → à corriger **avant** toute purge de `concelhos/` |

⚠️ Rappel appliqué à ces batchs : **exclure explicitement `AGENTS.md`, `SEO_PLAN.md`, `context.md`, `CLAUDE.md`** (leçon CU `fb9dd2415`).

## Tâche suivante recommandée
1. **Si GO (b1)** : les 526 fichiers, retrait du couple Q/R, patron de la PR #284. **Puis re-parser le `FAQPage` de chaque fichier** (`acceptedAnswer.text` > 20 caractères) — c'est le contrôle manquant qui a créé le gisement.
2. **Si GO (b2)** : les 955 fichiers, substitution déterministe sur le `name`. **Ajouter au contrôle post-purge une vérification du `name`** : pas de double marqueur, pas de mot introduit deux fois.
3. **Si GO (c)** : corriger `scripts/gen_concelhos.py` — **avant** toute purge des pages `concelhos/`.
4. **Sans GO** : inventorier par parsing les **autres** Questions du `FAQPage`. Ce run n'a caractérisé que « Quanto tempo demoram a chegar? » et « Trabalham … 24h/7d? » sur 4 219 `acceptedAnswer`. **Le reste n'a jamais été inventorié.** Commencer par « Quanto custa uma urgencia eletrica? ».
5. **Sans GO** : arbitrer le blocage n°5 (doublon `public/` ↔ racine), conjointement avec CU.

## Apprentissages (self-improving)
- 🔴 **NOUVEAU — un compteur de gisement doit être défini par un PRÉDICAT, pas par un nombre.** « 955 FAQ vides » était suivi depuis des runs sans que personne ne re-dérive ce que 955 comptait. Le prédicat réel donne **526**, et 955 est **un autre défaut**. ➡️ **Écrire le prédicat exact à côté du chiffre dans `context.md`**, sinon le chiffre survit à sa définition.
- 🔴 **NOUVEAU — un gisement stable entre deux runs n'est pas rassurant : c'est un signal de mesure figée.** Le « 955 → 955 » avait été noté ⚠️ le 12/08 sans être creusé. Il était stable **parce qu'il mesurait autre chose**.
- 🔴 **NOUVEAU — les artefacts de purge se logent aussi dans les NOMS de questions, pas seulement dans les réponses.** Tous les contrôles écrits jusqu'ici portaient sur `acceptedAnswer.text` (> 20 caractères). ➡️ **Ajouter un contrôle sur `name`** : pas de double marqueur, pas de mot introduit deux fois.
- 🔴 **NOUVEAU — le contrôle « la chaîne du script existe-t-elle en production ? » a maintenant invalidé 2 diagnostics sur 2** (CU le 12/08, EU ce run). Il coûte une commande. ➡️ **À passer systématiquement avant d'attribuer un défaut à un script versionné.**
- 🔴 **NOUVEAU — publier la ventilation complète est ce qui débloque une décision, et ça a MARCHÉ.** Le tableau par zone du 12/08 a permis le GO, et le batch #281 a refermé le blocage n°1. **Quatre runs avaient demandé ce GO sans fournir le tableau.** ➡️ **Le patron est validé : ventiler → prototyper → demander le GO en un tap. À réappliquer sur CU (batch 815).**
- 🔴 **NOUVEAU (pattern des 4 repos ce run) — les violations les plus graves sont dans le JSON-LD**, et les compteurs de composants ne les voient pas. Vérifié sur CNR, ENR, CU et EU le même run.
- 🔴 **Choisir la page prototype aussi pour ce qu'elle ÉVITE.** `garantia.html` (comme `eletricista-braganca.html` avant elle) n'a pas de jumelle `public/` : le prototype ne s'enchevêtre pas avec le blocage n°5. **Un prototype qui touche deux questions ouvertes à la fois n'est plus décidable en un tap.**
- 🔴 **Un écart CONSTANT sur toutes les zones est un feu vert méthodologique.** Un défaut qui ne varie pas est un défaut à motif unique : le batch devient une substitution déterministe.
- 🔴 **Distinguer script one-shot et étape de build change complètement la décision.** Un one-shot cassé laisse un gisement **figé et sûr à purger** ; un générateur cassé **annule tout batch**. Les deux existent ici : `r12_*.py` (one-shot, et sans effet en prod) et `gen_concelhos.py` (générateur).
- **Le contrôle positif doit rester systématique.**
- 🔴 **Tout grep à motif non-ASCII passe par un script Python**, jamais une boucle inline `zsh -c`.
- **Corriger un prix faux par RETRAIT du total, pas par recalcul.**
- ⚠️ **HEURISTIQUE FAUSSE À NE PAS RÉINTRODUIRE** — « ce site = 70 €/h, donc un `65€` ici est une erreur » est **FAUX**. Distinction réelle : **70 €/h = main-d'œuvre électricité · 65 €/h = main-d'œuvre canalisation · 65 € = déplacement Z6**.
- **R145 autorise explicitement « 24h/7 dias »** (`AGENTS.md` L184). Ce qui est banni : les promesses de délai personnalisées. ⚠️ C'est **l'inverse** des sites `*-norte-reparos`. **Ne pas purger « 24h » ici.**
- **Quand une question FAQ porte sur un délai, retirer le couple Q/R plutôt que le réécrire.** Validé par le merge de la PR #200, réappliqué ce run sur ENR, CU et EU.
- **Toute purge de conformité doit re-parser le JSON-LD après coup.** ⚠️ Ne pas exiger « commence par une majuscule ».
- `_archive/` contient de vieux fichiers avec violations — **NE PAS patcher**, l'exclure de tous les greps.

## Edge cases détectés
- **Worktree obligatoire** : copie de travail sale en permanence. **Jamais `reset --hard`/`stash`/`clean`** (R-WT). Vérifié ce run : cette mention est bien une **interdiction**, pas une prescription — rien à corriger.
- **Le `/tmp` du sandbox ≠ le `/tmp` du host.** Worktrees sous `~/work/Sites/_worktrees/loop-YYYY-MM-DD/` — **lisibles depuis le sandbox**, ce qui permet de parser les 2 300+ fichiers HTML en quelques secondes. **Répartition la plus efficace : parsing Python au sandbox, `git`/`gh` au host.**
- **Les commandes `git` ne fonctionnent PAS depuis le sandbox dans un worktree** (le `.git` contient un chemin absolu host).
- 🔴 **`grep -P` n'existe pas sur macOS** — un `grep -P` dans une chaîne `&&` fait **échouer silencieusement tout le reste de la commande**. **Utiliser Python pour tout motif non trivial.**
- 🔴 **`git commit -m` multiligne avec backticks/parenthèses est fragile en zsh.** Utiliser `git commit -F -` avec un heredoc `<<'MSG'`.
- 🔴 **`set -e` + zsh : un glob sans correspondance fait AVORTER tout le script.** Utiliser `setopt null_glob`.
- 🔴 **R6 interdit `--force`, donc une PR déjà ouverte se met à jour par MERGE de `main`, jamais par rebase.**
- ⚠️ **Le sandbox ne peut pas supprimer les `.git/objects/*.lock`** — `git fetch` émet des warnings d'unlink mais **réussit**.
- **Agents concurrents confirmés sur ce checkout.** Parade : `git branch --show-current` avant **chaque** commit, `git diff <remote>/main...HEAD --name-only` avant le push, `gh pr create --head <branche-explicite>`.
- Le sandbox n'a ni `gh` ni credentials Git → tout git/gh via `mcp__desktop-commander__start_process`.
- L'outil `Edit`/`Write` (chemin host) gère parfaitement les accents et les fichiers HTML sur une seule ligne — plus sûr que `sed`.
- `public/index.html` et `./index.html` **diffèrent** (même situation que CU). Canonicals identiques et corrects → pas d'urgence, mais doublon à arbitrer conjointement avec CU.
- Ce repo est un site **statique pur** : pas de `tsc`, vérification par grep + re-parsing JSON.
- Corps de PR long : fichier + `gh pr create --body-file`, jamais `--body` inline.

## Blocages connus
1. ✅ **~~301 fichiers avec un prix minimum faux~~ — CLOS le 13/08 par la PR #281.** Vérifié : écart nul sur les 6 zones.
2. 🛑 **526 fichiers avec une réponse FAQ vide** = attente GO batch. **Plus aucun verrou technique** : la causalité « scripts » est réfutée, la cible est unique et sans faux positif.
3. 🛑 **955 fichiers avec un nom de question agrammatical** (`Trabalham Atendimento 24h/7d?`) = attente GO batch. Substitution déterministe, source verbatim sur CU.
4. 🛑 **`scripts/gen_concelhos.py`** : délai chiffré + claims 24h + « relatório técnico ». **Régénère à chaque exécution** → à corriger **avant** toute purge des pages `concelhos/`.
5. 🛑 **Doublon `public/` ↔ racine** — à arbitrer conjointement avec CU.
