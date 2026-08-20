# context.md — Loop State

> Écrit par le loop Cowork après chaque run. NE PAS ÉDITER MANUELLEMENT.

## Dernier run
- Date : 2026-08-20
- Tâche prévue : `context.md` du 19/08, **n°3** — « localiser les 2 blocs `ld+json` JSON-invalides ; il les compte, il ne les a pas encore nommés ».
- Tâche réellement exécutée : **la tâche prévue, plus la réparation — qui s'est révélée être un défaut de structure HTML, pas de JSON.**
- Branche (depuis `origin/main`, **en worktree**) : `loop/2026-08-20-eu-jsonld-invalide`
- Commits : 3 (2 fichiers de production, **1 par commit**, + `SEO_PLAN.md`)
- PR ouverte : **#312** — https://github.com/taffrand-gif/eletricista-urgente/pull/312
- **PR jumelle CU : #269** (même signature, trouvée le même soir)
- Résultat : ✅ 2 fichiers. **Deux pages servaient leur feuille de style à l'intérieur d'un bloc de données structurées.**

### Localisation
Parsing des **2 398 fichiers / 9 266 blocs `ld+json`** (`_archive/` exclu) : les 2 invalides sont **ligne 14** de `eletricista-fuga-corrente-cambres.html` et `eletricista-fuga-corrente-santa-marinha-do-zezere.html`, même erreur au même octet.

🔎 **Propagation cross-repo dans le run même** : la signature vient de CU, où le même défaut venait d'être trouvé le soir même (PR #269). Passée sur EU avant de clore le run → 2 fichiers de plus.

### Deux défauts par ligne, tous deux par suppression de fragment
**1.** `"@context":"https://***@type":"Service"` au lieu de `"@context":"https://schema.org","@type":"Service"` — la chaîne exacte `schema.org","` remplacée par `***`, JSON cassé dès le caractère 30. Cause racine : `LECONS.md` **leçon #407 (18/07)**, un filtre de sandbox mute `https://schema.org","@type":` dans les outputs.

**2. — le plus grave.** La ligne perdait aussi **son début et sa fin** :

| | ligne 14 |
|---|---|
| jumelle `cumieira` | `<meta property="og:type" content="website"><script …ld+json>{JSON}</script><style>` |
| cassé | `<script …ld+json>{JSON}` |

Le `<script type="application/ld+json">` restait **non fermé**, avalant **2 860** et **2 940 caractères sur 19 lignes** → **toute la feuille de style de la page partait dans un bloc de données structurées au lieu d'être appliquée.**

### Le défaut était exactement circonscrit avant tout patch
Ces 2 fichiers sont les **seuls des 77 pages `fuga-corrente` sans `og:type`**, et les **seuls des 2 398 fichiers du repo** dont le compte `<style>` est déficitaire.

- **Témoins R8** : `https://***` **2→0** · `og:type` **0→1 par fichier**. `git diff --numstat` : **1/1 sur chacun**.
- **Compteurs de balises après patch identiques à la jumelle `cumieira`** : ld+json 10 · `</script>` 13 · `<style>` 2 · `</style>` 3 · `og:type` 1.
- **Rescan complet : 2 398 fichiers, 9 268 blocs, 0 invalide.** Contrôle croisé exécuté **depuis le host** — c'est un filtre de sandbox qui produit ce défaut.
- Ligne recomposée **verbatim** sur le patron des jumelles de même génération (`cumieira`, `salzedas`, `valdigem`) → zéro invention (R4).
- Aucun chevauchement avec #311, #308, #307. Aucune jumelle `public/` → **blocage n°5 non concerné**.

## ✅ Gate merge — aucun gate actif
Vérifié ce run sur les 4 `context.md` : **aucune mention d'attente de merge**. Aucun gate réécrit.

🔴 **Rappel de doctrine, à ne jamais réécrire** : R7 interdit de **MERGER**, pas de **PRODUIRE**. Entre le 06/08 et le 09/08, la mention « Attente GO merge (R7) » a été relue chaque nuit comme un ordre d'arrêt → **4 runs sans production**.

## 🛑 GISEMENTS CHIFFRÉS — DÉCISIONS REQUISES (prédicat = **Question** + variante)

Aucun n'a été touché ce run. Inventaire inchangé depuis le 19/08.

| # | Cible | Fichiers | Traitement |
|---|---|---:|---|
| **(b2′)** | **Q `Tempo de resposta?` → variante `para emergências…` (minuscule)** | **221** | ✅ **MEILLEUR CANDIDAT POUR UN GO** — **exactement le même patch que la PR #311**, dont le rendu est déjà visible sur 43 fichiers |
| (g) | `Sem custo extra de fim de semana` (contredit la majoration +50 %) | **22** | substitution déterministe — **le plus petit et le plus grave après (b2′)** |
| (b1′) | Q `Quanto tempo demoram a chegar?` | **960** | retrait du couple Q/R + re-parse du `FAQPage` |
| (f) | Q `Quanto custa uma urgencia eletrica?` → `sob orçamento por escrito (1h)…` | **842** | substitution par la grille verbatim |
| (h) | Statistiques non sourcées `N% dos/das` | **~60** | sourcer publiquement ou retirer |
| (c) | `)EUR` | 15 | corriger `scripts/gen_concelhos.py` **avant** toute purge des pages `concelhos/` |

## Tâche suivante recommandée
1. **Passer les signatures de corruption de `LECONS.md` sur TOUT le repo.** Le motif de la leçon #407 a sorti 2 pages en 4 secondes de parsing. **`LECONS.md` en contient d'autres qui n'ont jamais été grepées.** Aucun GO nécessaire, meilleur rapport effort/résultat identifié à ce jour.
2. **Contrôler l'équilibre des balises sur tout le repo**, pas seulement le JSON-LD : le défaut de ce run était un `<script>` non fermé, et c'est le compteur `<style>` qui l'a révélé — pas le parseur JSON. Passe générique : comparer, par génération de page, les comptes `<script>` / `</script>` / `<style>` / `</style>`.
3. **Si GO (b2′)** : les 221 fichiers restants de `Tempo de resposta?`. **Le patch est déjà écrit et en revue (PR #311).**
4. **Si GO (g)** : les 22 `Sem custo extra de fim de semana`.
5. **Sans GO** — traiter les statistiques (h) : commencer par la contradiction `30%` vs `40% dos incêndios domésticos`, **2 + 5 fichiers**, aucune décision d'offre en jeu (c'est une erreur factuelle).
6. **Sans GO** — chercher sur EU les défauts trouvés sur CU : `Fazem orçamento sem compromisso?` → `gratuito` (38 sur CU) et la signature `<td>` + `&lt; `.
7. **Sans GO** — arbitrer le blocage n°5 (doublon `public/` ↔ racine), conjointement avec CU.

## Apprentissages (self-improving)
- 🔴 **NOUVEAU — un bloc `ld+json` invalide peut cacher un défaut de STRUCTURE HTML bien plus grave que lui.** Le parseur disait « JSON invalide » ; la cause réelle était un `<script>` non fermé avalant 19 lignes de feuille de style. ➡️ **Quand un bloc `ld+json` est invalide, comparer les COMPTEURS DE BALISES du fichier à ceux d'une jumelle de même génération AVANT de conclure que c'est un problème de JSON.**
- 🔴 **NOUVEAU — le fichier de référence d'un transplant doit être de la MÊME GÉNÉRATION.** Les 77 pages `fuga-corrente` se répartissent en 3 générations (2, 6 et 10 blocs `ld+json`). **Prendre la première jumelle venue aurait donné un patron faux.** ➡️ **Avant tout transplant, grouper les fichiers par signature structurelle et ne transplanter qu'à l'intérieur d'un groupe.**
- 🔴 **NOUVEAU — un piège d'OUTIL documenté doit être cherché dans les fichiers COMMITÉS, pas seulement évité au moment d'écrire.** `LECONS.md` décrit le filtre `schema.org","` → `***` depuis le **18/07** ; son motif n'avait jamais été passé sur le repo. ➡️ **Toute leçon décrivant une signature de corruption vaut une passe sur tout le repo au run suivant.**
- 🟢 **NOUVEAU — la propagation cross-repo peut se faire DANS LE RUN MÊME, pas au run suivant.** Signature trouvée sur CU à 1 h, passée sur EU à 1 h 20, 2 fichiers de plus. ➡️ **Quand un run trouve une signature de corruption, la passer sur les 3 autres repos avant de clore le run.**
- 🔴 **Quand le défaut vient d'un filtre de SANDBOX, la vérification doit sortir du sandbox.**
- 🔴 **Une variante MINORITAIRE peut être la plus grave.** `3 min` ne pesait que 43 fichiers sur 267, mais c'était la seule à promettre un délai chiffré. ➡️ **Ventiler par fréquence, puis trier par GRAVITÉ — pas par volume.**
- 🔴 **Le même défaut existe sous des libellés de Question différents.** `Tempo de resposta?` (267) et `Quanto tempo demoram a chegar?` (960) sont la même famille ; `Qual é o tempo de chegada?` (51) porte déjà la **réponse conforme**. ➡️ **Regrouper par THÈME avant de compter ; la réponse conforme d'une Question est la source verbatim de ses sœurs.**
- 🔴 **Une statistique non sourcée est un gisement au même titre qu'un prix.** ~60 fichiers, **deux chiffres du repo se contredisent**. ➡️ `grep -oE '[0-9]{1,3}% (dos|das|de)'` à l'audit récurrent des 4 repos.
- 🔴 **Deux réponses CONTRADICTOIRES à la même Question peuvent coexister en production** ; corollaire venu de CU : **deux Questions DIFFÉRENTES d'un même thème peuvent aussi se contredire.**
- 🔴 **Une fourchette de prix est bannie même quand elle a l'air prudente** (`varia entre 80€ e 200€`, 26 fichiers).
- 🟢 **Le parsing exhaustif tient en quelques secondes au sandbox** (2 398 fichiers, 9 266 blocs). **Aucune raison de continuer à grepper des motifs connus : ventiler coûte le même temps et trouve ce qu'on ne cherchait pas.** Vérifié une 4ᵉ fois.
- 🔴 **Une PR mergée peut DISPARAÎTRE de `main`** (constaté sur CNR, PR #300). Contrôle : chercher `(#N)` dans `git log --oneline` — `merge-base --is-ancestor` est **faux sur un merge en squash**.
- 🔴 **Une PR ouverte peut *perpétuer* un défaut sans l'avoir introduit** (leçon CU : #268 réécrit la ligne corrompue et garde le bug). **La bonne question n'est pas « quelles PR touchent ce fichier ? » mais « que fait cette PR de la ligne en cause ? ».**
- 🔴 **Le contrôle « la chaîne du script existe-t-elle en production ? » a invalidé 2 diagnostics sur 2.** À passer avant d'attribuer un défaut à un script versionné.
- 🔴 **Distinguer script one-shot et étape de build change complètement la décision.** `r12_*.py` (one-shot) vs `gen_concelhos.py` (générateur — **annule tout batch tant qu'il n'est pas corrigé**).
- 🔴 **Publier la ventilation complète est ce qui débloque une décision.** Patron validé : **ventiler → prototyper → demander le GO en un tap.**
- 🔴 **Choisir la page prototype aussi pour ce qu'elle ÉVITE** (pas de jumelle `public/`).
- **Toute purge de conformité doit re-parser le JSON-LD après coup.** ⚠️ Ne pas exiger « commence par une majuscule ».
- ⚠️ **HEURISTIQUE FAUSSE À NE PAS RÉINTRODUIRE** — « ce site = 70 €/h, donc un `65€` ici est une erreur » est **FAUX**. Distinction réelle : **70 €/h = main-d'œuvre électricité · 65 €/h = main-d'œuvre canalisation · 65 € = déplacement Z6**.
- **R145 autorise explicitement « 24h/7 dias »** (`AGENTS.md` L184). Ce qui est banni : les promesses de délai. ⚠️ **L'inverse des sites `*-norte-reparos`. Ne pas purger « 24h » ici.**
- **Quand une question FAQ porte sur un délai, retirer le couple Q/R plutôt que le réécrire** — sauf si une variante conforme de la MÊME Question existe déjà en production, auquel cas la transplanter verbatim.
- `_archive/` contient de vieux fichiers avec violations — **NE PAS patcher**, l'exclure de tous les greps.

## Edge cases détectés
- **`gh` et les credentials Git n'existent QUE sur le host macOS.** Sandbox = lecture / grep / parsing Python / **écriture de fichiers** ; `git` en écriture / `gh` → `mcp__desktop-commander__start_process`. **C'est la répartition la plus efficace.** ⚠️ **Mais pas pour tout** : quand le contenu en jeu est celui que le filtre de sandbox mute (`schema.org","`), le contrôle final doit être rejoué depuis le host.
- **Le `/tmp` du sandbox ≠ le `/tmp` du host.** Worktrees sous `~/work/Sites/_worktrees/loop-YYYY-MM-DD/` — lisibles **et inscriptibles** depuis le sandbox.
- **Les commandes `git` ne fonctionnent PAS depuis le sandbox dans un worktree** (chemin absolu host dans `.git`). **L'écriture de fichiers, si.**
- 🔴 **`gh pr diff <n>` peut dépasser 65 k caractères** → `gh pr view <n> --json files --jq '.files[].path'`, puis `comm -12` contre `git diff --name-only`. **Mais pour savoir ce qu'une PR fait d'une LIGNE précise, `gh pr diff` filtré par `awk` reste le seul moyen.**
- 🔴 **zsh ne fait PAS de word-splitting** ; **`grep -P` n'existe pas sur macOS** → Python pour tout motif non trivial ; **`set -e` + glob vide fait avorter le script** (`setopt null_glob`) ; **`git commit -m` multiligne est fragile** → `git commit -F -` + heredoc `<<'MSG'`.
- 🔴 **R6 interdit `--force`, donc une PR déjà ouverte se met à jour par MERGE de `main`, jamais par rebase.**
- **Worktree obligatoire** (R-WT) : copie de travail sale en permanence. **Jamais `reset --hard` / `checkout -- .` / `stash` / `clean`.** Vérifié ce run : le checkout partagé était sur `main` avec des **centaines de fichiers modifiés** par une autre automation — **non touché**. Cette mention est bien une **interdiction**, pas une prescription — rien à corriger.

## Blocages connus
1. 🛑 **(b2′) 221 fichiers** — attente GO. **Le patch existe déjà (PR #311).**
2. 🛑 **(b1′) 960 fichiers** — attente GO.
3. 🛑 **(f) 842 fichiers** — attente GO.
4. 🛑 **(h) ~60 fichiers de statistiques non sourcées** — sourcer ou retirer, décision requise.
5. ⚠️ **Doublon `public/` ↔ racine** — arbitrage conjoint avec CU.
6. ⚠️ **`scripts/gen_concelhos.py`** — générateur suspecté pour `)EUR` : **le corriger AVANT toute purge des pages `concelhos/`**, sinon le batch sera annulé au prochain build.
7. ✅ **REFERMÉ — les 2 blocs `ld+json` invalides.** Nommés et réparés ce run (PR #312). Rescan : 0 invalide sur 9 268 blocs.
