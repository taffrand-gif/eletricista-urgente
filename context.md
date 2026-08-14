# context.md — Loop State

> Écrit par le loop Cowork après chaque run. NE PAS ÉDITER MANUELLEMENT.

## Dernier run
- Date : 2026-08-14
- Tâche exécutée : **tâche n°4 du `context.md` du 13/08 (« sans GO ») — inventaire par parsing de TOUTES les Questions du `FAQPage`**, puis prototype.
- Branche : `loop/2026-08-14-eletricista-urgente-inventaire-faq` (depuis `origin/main`, **en worktree**)
- Commits : 2 (`blog/avaria-eletrica-domingo.html`, + `SEO_PLAN.md`)
- PR ouverte : https://github.com/taffrand-gif/eletricista-urgente/pull/303
- Périmètre parsé : **2 396 fichiers HTML · 9 237 blocs `ld+json` · 4 218 `acceptedAnswer`** (`_archive/` exclu). **0 bloc non parsable.**
- Résultat : ✅ 1 fichier de production. **Et quatre résultats qui changent l'état du repo.**
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

## 🔴 Ventilation exhaustive des Questions — 4 résultats

### 1. 🟢 (b2) est CADUC — ne plus demander ce GO
`"name": "Trabalham Atendimento 24h/7d?"` → **0 occurrence**. Le nom est désormais `Trabalham 24h/7d?` sur **956** fichiers. Les 955 documentés le 13/08 **ont été refermés**. **Retirer (b2) du tableau des décisions.**

### 2. 🔴 (b1) était sous-estimé d'un facteur 1,8 — le prédicat était faux
Le prédicat suivi était la *valeur de réponse* `" conforme zona"`. Le prédicat correct est **la Question**.

`Quanto tempo demoram a chegar?` — **953 fichiers, 4 variantes** :

| Réponse | Fichiers | Statut |
|---|---:|---|
| `conforme zona` | **525** | seule variante documentée jusqu'ici |
| `min conforme zona. atendimento após contacto telefónico ao telefone.` | **418** | 🆕 **jamais documentée** |
| `min conforme zona. Atendemos 24h/7 dias, após contacto telefónico ao telefone.` | 6 | 🆕 |
| `min conforme zona. Atendimento 24h/7 dias, ligue 932 321 892 ao telefone.` | 4 | 🆕 |

La variante à 418 porte la même signature : préfixe **`min` orphelin** (le nombre a été consommé), `atendimento` en minuscule en milieu de phrase, `após contacto telefónico ao telefone` redondant.
➡️ **Cible réelle : la Question, 953 fichiers, retrait du couple Q/R, motif unique.**

### 3. 🔴 Un gisement prix jamais inventorié — `Quanto custa uma urgencia eletrica?` (955 fichiers, 6 variantes)

| Réponse | Fichiers | Statut |
|---|---:|---|
| `sob orçamento por escrito (1h) com deslocacao incluida. Suplemento fora de horas.` | **836** | 🔴 agrammatical, pourcentage perdu |
| `Mao de obra 70 EUR/hora mais deslocacao por zona (Z1-Z6, de 15 a 65 EUR). Majoracao +50%…` | 96 | ✅ conforme |
| `…antes da deslocação)EUR (1h)…` | 15 | 🔴 **artefact `)EUR`** |
| `sob orçamento (1h) com deslocacao incluida. Suplemento fora de horas.` | 6 | 🔴 |
| `70 €/h + deslocação (Z1: 15€ a Z6: 65€). Mínimo 1h. Acréscimo +50% fora de horas úteis.` | 1 | ✅ **source de vérité** |
| `Desde 135 EUR (1h) com deslocacao incluida. Suplemento fora de horas.` | 1 | 🔴 prix inventé |

**Conformes : 97 · Non conformes : 858.**
🔴 **L'artefact `)EUR` était réputé propre à CU (`por escritoEUR`, 698 fichiers). Il existe aussi ici.**

### 4. 🔴 Contradiction de prix EN PRODUCTION — `Trabalham ao fim de semana?`

| Réponse | Fichiers | Statut |
|---|---:|---|
| `Sim, com majoração de +50% sobre mão de obra e deslocação, sempre discriminada no orçamento.` | **41** | ✅ conforme `PRICING` |
| `Sim, Atendimento 24h/7d, 7 dias por semana, incluindo feriados. **Sem custo extra de fim de semana.**` | **23** | 🔴 **claim faux** |

**Deux réponses opposées à la même Question, sur le même site. Aucune n'avait été inventoriée.** Les 23 sont tous des `blog/*.html`, **aucun n'a de jumelle `public/`** → gisement homogène et sûr.
## ✅ Gate merge — aucun gate actif
Vérifié ce run : aucune mention d'attente dans les 4 `context.md`. Aucun gate réécrit.

🔴 **Rappel de doctrine, à ne jamais réécrire** : R7 interdit de **MERGER**, pas de **PRODUIRE**. Entre le 06/08 et le 09/08, la mention « Attente GO merge (R7) » a été relue chaque nuit comme un ordre d'arrêt → **4 runs sans production**.

🆕 **Corollaire découvert ce run (sur CNR)** : le statut `MERGED` de l'API GitHub **n'est pas une preuve de présence en production** — la PR CNR #300, pourtant `MERGED`, a été annulée par une réécriture de `main`. ➡️ **Contrôle de fin de run : `git merge-base --is-ancestor <mergeCommit> <remote>/main`.** À passer aussi sur EU au prochain run.
## Prototype livré — `blog/avaria-eletrica-domingo.html`
Page la plus à enjeu du lot des 23 : **le dimanche est précisément le cas où la majoration s'applique**. Déclarée au `sitemap-extra.xml`. **Sans jumelle `public/`** → décidable sans rouvrir le blocage n°5.

Corrections, **toutes par transplant verbatim depuis la production de ce repo** (zéro invention, R4) :
1. `Quanto custa este serviço em 2026?` répondait `varia entre 80€ e 200€` — **fourchette inventée**, explicitement bannie (R12 : « jamais de fourchette inventée ; hors grille = *sob orçamento* ») → grille verbatim, **dans le JSON-LD ET dans le corps**.
2. `Trabalham ao fim de semana?` → variante majoritaire verbatim (41 fichiers), **JSON-LD ET corps**.
3. Bloc CTA : retrait de `· Sem custo extra de fim de semana` (même claim faux, **au-dessus de la ligne de flottaison**).
4. Retrait de la phrase `custa em média entre 80€ e 200€ … reparação de 1.000€ a 5.000€` (économie inventée de bout en bout).

Témoins R8 : `80€ e 200€` **3→0** · `Sem custo extra` **3→0** · `1.000€ a 5.000€` **1→0** · `preço médio em 2026` **2→0** · grille `70 €/h + deslocação…` **0→2** · `majoração de +50%…` **0→2** · `932 321 892` **2→2** (NAP intact).
⚠️ `24h/7d` **2→0** : les 2 occurrences étaient **à l'intérieur de la réponse remplacée**. La disponibilité reste affirmée par le « **Sim,** » de la réponse verbatim et par le `(24h)` du CTA. **Rien n'a été purgé au motif de `24h` — R145 l'autorise ici.**
Contrôle : **2/2 blocs JSON-LD re-parsés valides**, `FAQPage` **3 questions conservées**, **0 `acceptedAnswer.text` < 20 caractères**.
⚠️ **Non traité, à statuer** : la même page portait `Mais de 60% dos problemas graves que vemos no terreno` — **statistique non sourcée** (famille R11), laissée en place faute de source. Motif à inventorier.
## 🛑 DÉCISIONS REQUISES — tableau mis à jour au 2026-08-14

| # | Cible (PRÉDICAT explicite) | Fichiers | Traitement | Verrou restant |
|---|---|---:|---|---|
| ~~(b2)~~ | ~~`"name" == "Trabalham Atendimento 24h/7d?"`~~ | ~~955~~ **0** | — | ✅ **CADUC — retiré** |
| **(b1′)** | Question `name == "Quanto tempo demoram a chegar?"` | **953** | retrait du couple Q/R (prototype PR #284) | **aucun** — motif unique, 4 variantes de la même famille |
| **(f)** 🆕 | Question `name == "Quanto custa uma urgencia eletrica?"`, réponse ∉ {2 variantes conformes} | **858** | substitution par la grille verbatim | **aucun** |
| **(g)** 🆕 | `Sem custo extra de fim de semana` | **23** | substitution par la variante majoritaire (41 fichiers) | **aucun** — prototype PR #303 |
| (c) | `scripts/gen_concelhos.py` | 1 | délai chiffré (`faq_time()` L170-174) + claims 24h (L143/L148) + « relatório técnico » (L149) | **régénère à chaque exécution** → corriger **avant** toute purge de `concelhos/` |

⚠️ Rappel appliqué à ces batchs : **exclure explicitement `AGENTS.md`, `SEO_PLAN.md`, `context.md`, `CLAUDE.md`** (leçon CU `fb9dd2415`).
## Tâche suivante recommandée
1. **Si GO (g)** : 23 fichiers, substitution déterministe, prototype déjà en revue (PR #303). **Le plus petit et le plus grave** — une contradiction de prix en production.
2. **Si GO (b1′)** : 953 fichiers, retrait du couple Q/R. **Puis re-parser le `FAQPage` de chaque fichier** (`acceptedAnswer.text` > 20 car.) — c'est le contrôle manquant qui a créé le gisement.
3. **Si GO (f)** : 858 fichiers, substitution par la grille verbatim.
4. **Si GO (c)** : corriger `scripts/gen_concelhos.py` **avant** toute purge des pages `concelhos/`.
5. **Sans GO** : ventiler les Questions **restantes** — ce run a caractérisé les 4 plus fréquentes (956 · 955 · 953 · 64) ; il reste ~20 Questions de fréquence 35-52 non ventilées, dont `A altitude obriga a medidas especiais?` (**40 variantes pour 40 fichiers** — à vérifier : soit du contenu légitimement localisé, soit du bruit).
6. **Sans GO** : inventorier la statistique non sourcée `Mais de 60% dos problemas graves…` (famille R11), repérée sur la page prototype.
7. **Sans GO** : arbitrer le blocage n°5 (doublon `public/` ↔ racine), conjointement avec CU.
## Apprentissages (self-improving)
- 🔴 **NOUVEAU — le prédicat d'un gisement doit être la QUESTION, pas la valeur de réponse.** Suivre `" conforme zona"` donnait 526 ; suivre la Question donne **953**. **C'est la deuxième fois que ce repo se trompe de prédicat** (après le « 955 » du 13/08). ➡️ **Méthode désormais obligatoire : ventiler chaque Question par variante de réponse, puis cibler la Question.** Le tableau §DÉCISIONS porte maintenant le prédicat explicite de chaque cible.
- 🔴 **NOUVEAU — deux réponses CONTRADICTOIRES à la même Question peuvent coexister en production sans qu'aucun compteur ne s'en aperçoive.** 41 pages disent `+50%`, 23 disent `Sem custo extra de fim de semana`. ➡️ **Nouveau contrôle : pour chaque Question dont le nombre de variantes > 1, vérifier que les variantes ne se contredisent pas.**
- 🔴 **NOUVEAU — un défaut documenté sur un repo doit être recherché sur les 3 autres dans le run qui suit.** L'artefact `)EUR` était réputé propre à CU (698 fichiers) ; il existe aussi ici (15). Il n'a été trouvé que parce que ce run a **ventilé** au lieu de grepper des motifs déjà connus.
- 🔴 **NOUVEAU — une fourchette de prix est bannie même quand elle a l'air prudente.** `varia entre 80€ e 200€` (26 fichiers) coche « jamais de fourchette inventée » de R12. ➡️ **Motif à inventorier : `varia entre X€ e Y€` / `custa em média entre`.**
- 🔴 **NOUVEAU — une PR mergée peut DISPARAÎTRE de `main`** (constaté sur CNR, PR #300). ➡️ **Contrôle de fin de run : `git merge-base --is-ancestor <mergeCommit> <remote>/main`.**
- 🟢 **Le parsing exhaustif du repo tient en quelques secondes au sandbox** (2 396 fichiers, 9 237 blocs). **Il n'y a aucune raison de continuer à grepper des motifs connus : ventiler coûte le même temps et trouve ce qu'on ne cherchait pas.**
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
