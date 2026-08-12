# context.md — Loop State

> Écrit par le loop Cowork après chaque run. NE PAS ÉDITER MANUELLEMENT.

## Dernier run
- Date : 2026-08-12
- Tâche exécutée : **tâche n°4 du `context.md` (« sans GO ») — prototype R11 prix sur une 2ᵉ page à fort trafic**, après la sede operacional (PR #268).
- Branche : `loop/2026-08-12-eletricista-urgente-r11-prix-braganca` (depuis `origin/main`, **en worktree**)
- Commits : `cab5137b8` (`eletricista-braganca.html`), puis le commit `SEO_PLAN.md`
- PR ouverte : https://github.com/taffrand-gif/eletricista-urgente/pull/277
- Résultat : ✅ 2 commits, 2 fichiers. La `<meta name="description">` de `eletricista-braganca.html`, **visible en SERP**, annonçait « 35€ deslocação + 70€/h. **A partir de 120€ (1h)..** » alors que la grille de la même phrase donne **105 €** (+15 €, **+14,3 %**). Corrigé **par retrait du total dérivé, zéro arithmétique**. Témoins R8 : `A partir de 120€` 1→0 · `(1h)` 1→0 · `..` 1→0 · `A partir de` 6→5 (les 5 restants = libellés légitimes des blocs prix) · `35€ deslocação + 70€/h` 1→1 · `24h` 6→6 · `+351 932 321 892` 6→6 · `€` 15→14. **JSON-LD : 2/2 blocs re-parsés valides**, 0 `acceptedAnswer` < 20 caractères.
- Page choisie **aussi pour ce qu'elle évite** : Bragança est la plus grande ville du district, la page est déclarée dans `sitemap.xml`, et elle **n'a pas de jumelle dans `public/`** — le prototype ne se mélange donc pas au blocage n°5 (doublon `public/` ↔ racine) resté en arbitrage.

## 🔑 CE RUN — la ventilation complète du gisement prix, et elle débloque la décision

Recompte en début de run (script Python, `_archive/` exclu, **contrôle positif `65€` = 2 337 fichiers**) : gisement prix **303 fichiers**, identique au 11/08 — **207 à écart, 96 exacts, 0 dispersé**.

| Zone | Deslocação | Total annoncé | Total correct | Écart | Occ. |
|---|---:|---:|---:|---:|---:|
| Z1 | 15 € | 100 € | 85 € | **+15** | 10 |
| Z2 | 25 € | 110 € | 95 € | **+15** | 31 |
| Z3 | 35 € | 120 € | 105 € | **+15** | 39 |
| Z4 | 45 € | 130 € | 115 € | **+15** | 26 |
| Z5 | 55 € | 140 € | 125 € | **+15** | 54 |
| Z6 | 65 € | 150 € | 135 € | **+15** | 47 |
| — | 5 zones | corrects | — | 0 | 96 |

➡️ **L'écart est rigoureusement +15 € sur les 6 zones, sans exception.** C'est la preuve mécanique d'un bug de template unique et non de saisies dispersées : **le batch sur les 301 fichiers restants est mécaniquement sûr** — un seul motif, un seul remplacement, aucun cas particulier. **Il ne manque que le GO.**

## ✅ Gate merge — aucun gate actif
Vérifié au run du 11/08 : #240 (CU), #269 (CNR), #295 (ENR), #200 (EU) **toutes MERGED**. Aucun gate réécrit ce run.

🔴 **Rappel de doctrine, à ne jamais réécrire** : R7 interdit de **MERGER**, pas de **PRODUIRE**. Entre le 06/08 et le 09/08, la mention « Attente GO merge (R7) » a été relue chaque nuit comme un ordre d'arrêt → **4 runs sans production**.

## ✅ Acquis du run du 11/08, toujours valides

**La source des 955 FAQ vides, ce ne sont pas les générateurs de pages — ce sont les scripts de purge eux-mêmes.**

| Script | Ligne | Chaîne de remplacement |
|---|---|---|
| `scripts/r12_blog_safe_cleanup.py` | L49-50 | **`"Deslocação conforme zona Z"`** |
| `scripts/r12_hubs_cleanup.py` | L37-45 | **`"< Deslocação conforme zona tarifária Z"`** |

Chaîne terminée par un **`Z` orphelin** : fragment de gabarit inachevé. Ces scripts sont **one-shot**, pas une étape de build → **un batch sur les 955 fichiers ne sera pas annulé au prochain déploiement**, à condition de corriger ou retirer ces deux scripts d'abord.

⚠️ **MAIS — nuance apportée par CU ce run** : sur `canalizador-urgente`, les scripts jumeaux portent la **même** chaîne défectueuse et pourtant `conforme zona Z` y a **0 occurrence en production** ; le défaut CU vient d'une 4ᵉ passe absente du repo. ➡️ **Avant le batch ici, vérifier que `conforme zona Z` existe bien en production sur EU** — le diagnostic n'est établi que si la chaîne du script s'y retrouve réellement.

### ⚠️ Défaut distinct dans le vrai générateur — `scripts/gen_concelhos.py`
Celui-ci **régénère à chaque exécution** : `faq_time()` L170-174 produit un **délai chiffré**, L143/L148 des claims « Resposta rápida 24 horas por dia » / « sem custo adicional », L149 « **relatório técnico** » (banni par le ruling Filipe 08/07). **À traiter AVANT toute purge des pages `concelhos/`** — GO requis.

## Tâche suivante recommandée
1. **Si GO batch prix** : les **301 fichiers restants**, par retrait, patron des PR #268 et #277 et de la PR #240 (CU, mergée). La ventilation ci-dessus lève le dernier doute méthodologique.
2. **Si GO** : corriger `scripts/r12_blog_safe_cleanup.py` L49-50 et `scripts/r12_hubs_cleanup.py` L37-45, **puis** batch FAQ sur les 955 fichiers — **après** avoir vérifié que `conforme zona Z` existe bien en production ici (contrôle nouveau, venu de CU).
3. **Si GO** : corriger `scripts/gen_concelhos.py` — **avant** toute purge des pages `concelhos/`.
4. **Sans GO** : prototype R11 prix sur une 3ᵉ page. Candidats sans jumelle `public/` et déclarés au sitemap : `eletricista-vila-real.html` (Z5, 140→125), `eletricista-mirandela.html` (Z2, 110→95), `eletricista-quadro-eletrico-braganca.html` (Z3, 120→105).

## Apprentissages (self-improving)
- 🔴 **NOUVEAU — un écart CONSTANT sur toutes les zones est un feu vert méthodologique, pas une curiosité.** Les 6 zones dérivent de **+15 € exactement**. Un défaut qui ne varie pas est un défaut à motif unique : le batch devient une substitution déterministe, sans arbitrage cas par cas. ➡️ **Avant de demander un GO batch, publier la ventilation complète du gisement — c'est elle qui rend la décision possible en un tap.** Quatre runs ont demandé ce GO sans jamais fournir ce tableau.
- 🔴 **NOUVEAU — choisir la page prototype aussi pour ce qu'elle ÉVITE.** `eletricista-braganca.html` n'a pas de jumelle `public/` : le prototype ne s'enchevêtre pas avec le blocage n°5 encore en arbitrage. Un prototype qui touche deux questions ouvertes à la fois n'est plus décidable en un tap.
- 🔴 **NOUVEAU (venu de CU) — un script cassé dans le repo n'est pas la preuve qu'il a produit le défaut.** Sur CU, la chaîne défectueuse des 3 scripts a **0 occurrence** en production. ➡️ **Vérifier que la chaîne du script existe réellement en production avant de conclure à la causalité** — y compris ici, avant le batch FAQ.
- 🔴 **NOUVEAU (venu de CU) — vérifier qu'une PR mergée a bien CLOS son gisement.** Sur CU, la PR #254 annonçait 14 fichiers, il en restait 34. **Un merge n'est pas une clôture.**
- 🔴 **Un gisement qui ne diminue pas n'implique pas forcément un générateur.** Ici la source était la chaîne de remplacement d'un script de purge, inachevée. ➡️ **La chaîne de remplacement d'un script de substitution doit être une phrase complète, testée sur un échantillon**, jamais un fragment de gabarit.
- 🔴 **Distinguer script one-shot et étape de build change complètement la décision.** Un one-shot cassé laisse un gisement **figé et sûr à purger** ; un générateur cassé **annule tout batch**. Les deux existent ici : `r12_*.py` (one-shot) et `gen_concelhos.py` (générateur). **Trier avant de demander un GO.**
- 🔴 **Un batch de conformité peut corrompre la RÈGLE qu'il applique** (leçon CU, `fb9dd2415`). **Tout batch doit exclure `AGENTS.md`, `SEO_PLAN.md`, `context.md`, `CLAUDE.md`.** ➡️ Vérifié : l'`AGENTS.md` d'EU n'est **pas** corrompu.
- **Le contrôle positif doit rester systématique** : `65€` = 2 337 fichiers ce run (1 473 le 11/08 — l'écart vient du périmètre de scan, `65 €` avec espace inclus).
- 🔴 **Tout grep à motif non-ASCII passe par un script Python**, jamais une boucle inline `zsh -c`.
- 🔴 **Vérifier qu'un gisement DIMINUE entre deux runs.** Prix 336 → 303 → 303 ✅ (stable, rien ne régénère) · FAQ 955 → 955 ⚠️.
- **Corriger un prix faux par RETRAIT du total, pas par recalcul.** Conserver les composants (grille source de vérité) et supprimer le total dérivé : zéro arithmétique, donc zéro invention (R4).
- ⚠️ **HEURISTIQUE FAUSSE À NE PAS RÉINTRODUIRE** — « ce site = 70 €/h, donc un `65€` ici est une erreur » est **FAUX**. `65 €` est la déslocation **Zone 6**, légitime sur les 4 sites. Distinction réelle : **70 €/h = main-d'œuvre électricité · 65 €/h = main-d'œuvre canalisation · 65 € = déplacement Z6**.
- **R145 autorise explicitement « 24h/7 dias »** (AGENTS.md L184). Ce qui est banni : les promesses de délai personnalisées. ⚠️ C'est **l'inverse** des sites `*-norte-reparos`. **Ne pas purger « 24h » ici.**
- **Quand une question FAQ porte sur un délai, retirer le couple Q/R plutôt que le réécrire.** Validé par le merge de la PR #200.
- **Toute purge de conformité doit re-parser le JSON-LD après coup** et vérifier que chaque `acceptedAnswer.text` fait > 20 caractères. ⚠️ Ne pas exiger « commence par une majuscule ».

## Edge cases détectés
- **Le `/tmp` du sandbox ≠ le `/tmp` du host.** Worktrees sous `~/work/Sites/_worktrees/`.
- **Les commandes `git` ne fonctionnent PAS depuis le sandbox dans un worktree** (le `.git` contient un chemin absolu host). Dans un worktree : grep/lecture au sandbox, **tout `git` via desktop-commander**.
- ⚠️ **Le sandbox ne peut pas supprimer les `.git/objects/*.lock`** (« Operation not permitted ») — `git fetch` émet des warnings d'unlink mais **réussit**.
- 🔴 **`set -e` + zsh : un glob sans correspondance fait AVORTER tout le script.** Utiliser `setopt null_glob`.
- **Worktree obligatoire** : copie de travail sale en permanence. **Jamais `reset --hard`/`stash`/`clean`** (R-WT).
- **Agents concurrents confirmés sur ce checkout.** Parade : `git branch --show-current` avant **chaque** commit, `git diff origin/main..HEAD --name-only` avant le push, `gh pr create --head <branche-explicite>`.
- Le sandbox n'a ni `gh` ni credentials Git → tout git/gh via `mcp__desktop-commander__start_process`. Il est **excellent** pour les scripts Python sur les milliers de fichiers HTML montés.
- L'outil `Edit` (chemin host) gère parfaitement les accents et les fichiers HTML sur une seule ligne — plus sûr que `sed` pour un patch chirurgical.
- `public/index.html` et `./index.html` **diffèrent** (même situation que `canalizador-urgente`). Canonicals identiques et corrects → pas d'urgence, mais doublon à arbitrer conjointement avec CU.
- Ce repo est un site **statique pur** : pas de `tsc`, vérification par grep + re-parsing JSON.
- `_archive/` contient de vieux fichiers avec violations — **NE PAS patcher**, l'exclure de tous les greps.

## Blocages connus
1. 🛑 **301 fichiers avec un prix minimum faux** (R11 actif, visible en SERP) = attente GO batch. **Prototypes ouverts : PR #268 (sede operacional) et PR #277 (Bragança).** La ventilation par zone ci-dessus lève le dernier doute méthodologique. **Le plus grave du repo.**
2. 🛑 **955 fichiers avec une réponse FAQ vide** = attente GO batch. Verrou technique levé, mais **vérifier d'abord que `conforme zona Z` existe bien en production ici** (contrôle nouveau venu de CU).
3. 🛑 **`scripts/gen_concelhos.py`** : délai chiffré + claims 24h + « relatório técnico ». Régénère à chaque exécution → à corriger **avant** toute purge des pages `concelhos/`.
4. **Doublon `public/` ↔ racine.** Même question ouverte sur CU — **un seul arbitrage débloque les 2 repos.**
