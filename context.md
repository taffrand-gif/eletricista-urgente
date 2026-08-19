# context.md — Loop State

> Écrit par le loop Cowork après chaque run. NE PAS ÉDITER MANUELLEMENT.

## Dernier run
- Date : 2026-08-19
- Tâches prévues : `context.md` du 14/08, **n°5** (« ventiler les Questions **restantes** — ~20 Questions de fréquence 35-52 non ventilées ») et **n°6** (« inventorier la statistique non sourcée `Mais de 60% dos problemas graves…` »).
- Tâches réellement exécutées : **les deux, plus une violation R145 traitée en priorité (R11/R12).**
- Branche (depuis `origin/main`, **en worktree**) : `loop/2026-08-19-eu-ventilation`
- Commits : 3 (`equipa.html` · le batch 43 fichiers · `SEO_PLAN.md`)
- PR ouverte : **#311** — https://github.com/taffrand-gif/eletricista-urgente/pull/311
- Résultat : ✅ **44 fichiers de production.** La ventilation a sorti **une promesse d'arrivée en 3 minutes, en production**.

### 🔴 `Tempo de resposta?` — 267 fichiers, 5 variantes
| Variante | Fichiers | Verdict |
|---|---:|---|
| `para emergências, 24h/7d incluindo fins de semana.` | **221** | artefact — commence par **`para` en minuscule**, le délai a été mangé |
| **`3 min para emergências, 24h/7d incluindo fins de semana.`** | **43** | 🔴 **promesse d'arrivée en 3 minutes** — R145. **CORRIGÉ CE RUN** |
| `24h/7d para emergências, incluindo fins de semana. Orçamento por escrito antes da deslocação.` | **1** | ✅ **conforme — source de vérité** |
| `24h/7d incluindo fins de semana — chegada conforme disponibilidade operacional.` | 1 | ✅ conforme |
| `Atendemos 24h/7 dias, após contacto telefónico para emergências, 24h/7d incluindo fins de semana.` | 1 | doublon `X … X` |

Les 43 corrigés par **transplant verbatim de la variante conforme de la MÊME Question** (`eletricista-avaria-eletrica-braganca.html`) → zéro invention (R4). `24h/7d` conservé (R145 l'autorise ici).
**Commit groupé assumé** : motif unique, 1 occurrence par fichier, 43 diffs d'une ligne, témoins connus d'avance.

### `equipa.html` — prix inventé `Desde 135 EUR`
Sur les **6 variantes** de `Quanto custa uma urgencia eletrica?` (962 fichiers), celle-ci n'existait **qu'à 1 exemplaire**. `PRICING.md` fixe **70 €/h + deslocação Z1-Z6**, jamais 135 €. Transplant verbatim de la variante conforme (`calculadora-de-preco.html`).

### Témoins R8 (repo entier, `_archive/` exclu)
`3 min para emergências` **43→0** · `24h/7d para emergências, incluindo` **1→44** · `24h/7d` **10 195→10 195** (contrôle positif) · `Desde 135 EUR` **1→0** · `70 €/h + deslocação` (equipa) **0→1** · `65€` (equipa) **2→2**.
Structure : **89/89 blocs JSON-LD** des fichiers touchés valides · **0** `acceptedAnswer.text` < 20 car. · `git diff --numstat` = **44/44** (1 pour 1).
Périmètre : **aucun chevauchement avec #307 et #308** (vérifié par `comm`). Aucun fichier touché n'a de jumelle `public/` → **blocage n°5 non concerné**.

### Ventilation — 2 398 fichiers, **9 266 blocs `ld+json`**, **2 JSON invalides**, **774 Questions distinctes**
Questions restantes ventilées, verdicts :
- ✅ `Qual é o tempo de chegada?` (51) — « **Não comunicamos tempo absoluto de chegada.** O que se garante é orçamento por escrito antes da deslocação. » **C'est la formulation de référence du repo pour toute question de délai.**
- ✅ `Há deslocação grátis?` (41, 5 variantes) — « Não há desconto de deslocação », cohérent Z1-Z6.
- ✅ `A altitude obriga a medidas especiais?` (40 fichiers / **40 variantes**) — **question tranchée : contenu légitimement localisé** (altitude réelle + jours de gel par commune), **pas du bruit**. Confirmé à l'identique sur CU (45/45).
- ✅ `Trabalham com materiais próprios?` (52) · `Emitem orçamento para seguro?` (51) · `E durante a noite?` (50) · `Qual é a tarifa de mão de obra?` (49) · `Fazem seguro RC?` (46) · `Como é o pagamento?` (45) · `Como é feito o orçamento?` (42) · `Posso pedir só o diagnóstico?` (40) · `Há majorações automáticas?` (35) — **toutes conformes, 1 variante chacune.**
- ⚠️ `Emitem fatura com NIF?` (48, 3 variantes) · `Atendem 24h/7d?` (43, 3 variantes) · `Atendimento quando?` (46, 2 variantes) — variantes mineures, non contradictoires.

### Inventaire des statistiques non sourcées (tâche n°6) — famille R11, **jamais mesurée**
| Statistique | Fichiers |
|---|---:|
| `Mais de 60% dos problemas graves que vemos no terreno…` | **23** |
| `…35% dos casos) — juntas, borrachas, vedantes` | **23** |
| `30% dos incêndios domésticos` | 5 |
| `95% das placas domésticas (até 7,4 kW)` | 2 |
| `80% dos problemas` · `40% dos incêndios domésticos` | 2 + 2 |
| `95% dos curtos-circuitos` · `90% dos problemas` · `80% dos falsos alarmes` · `80% das vezes causa piscar` | 1 chacun |

**~60 fichiers.** Aucune n'est sourcée, et **deux se contredisent** (`30%` vs `40% dos incêndios domésticos`).

## ✅ Gate merge — aucun gate actif
Vérifié ce run sur les 4 `context.md` : **aucune mention d'attente de merge**. Aucun gate réécrit.

🔴 **Rappel de doctrine, à ne jamais réécrire** : R7 interdit de **MERGER**, pas de **PRODUIRE**. Entre le 06/08 et le 09/08, la mention « Attente GO merge (R7) » a été relue chaque nuit comme un ordre d'arrêt → **4 runs sans production**.

## 🛑 GISEMENTS CHIFFRÉS — DÉCISIONS REQUISES (prédicat = **Question** + variante)

| # | Cible | Fichiers | Traitement |
|---|---|---:|---|
| **(b2′)** | **Q `Tempo de resposta?` → variante `para emergências…` (minuscule)** | **221** | ✅ **MEILLEUR CANDIDAT POUR UN GO** — **exactement le même patch que la PR #311**, dont le rendu est déjà visible sur 43 fichiers |
| (g) | `Sem custo extra de fim de semana` (contredit la majoration +50 %) | **22** | substitution déterministe — **le plus petit et le plus grave après (b2′)** |
| (b1′) | Q `Quanto tempo demoram a chegar?` | **960** | retrait du couple Q/R + re-parse du `FAQPage` |
| (f) | Q `Quanto custa uma urgencia eletrica?` → `sob orçamento por escrito (1h)…` | **842** | substitution par la grille verbatim |
| **(h)** | **Statistiques non sourcées `N% dos/das` — NOUVEAU** | **~60** | sourcer publiquement ou retirer |
| (c) | `)EUR` | 15 | corriger `scripts/gen_concelhos.py` **avant** toute purge des pages `concelhos/` |

## Tâche suivante recommandée
1. **Si GO (b2′)** : les 221 fichiers restants de `Tempo de resposta?`. **Le patch est déjà écrit et en revue.**
2. **Si GO (g)** : les 22 `Sem custo extra de fim de semana`.
3. **Sans GO — localiser les 2 blocs `ld+json` JSON-INVALIDES** relevés par le parseur. Il les compte, il ne les a pas encore nommés.
4. **Sans GO** — traiter les statistiques (h) : commencer par la contradiction `30%` vs `40% dos incêndios domésticos`, **2 + 5 fichiers**, aucune décision d'offre en jeu (c'est une erreur factuelle).
5. **Sans GO** — le doublon `X … X` de `Tempo de resposta?` (1 fichier) et les 2 variantes hybrides d'`Emitem fatura com NIF?`.
6. **Sans GO** — chercher sur EU les défauts trouvés sur CU ce run : `Fazem orçamento sem compromisso?` → `gratuito` (38 sur CU) et la signature `<td>` + `&lt; `.
7. **Sans GO** — arbitrer le blocage n°5 (doublon `public/` ↔ racine), conjointement avec CU.

## Apprentissages (self-improving)
- 🔴 **NOUVEAU — une variante MINORITAIRE peut être la plus grave.** `3 min` ne pesait que **43 fichiers sur 267** pour sa Question, mais c'était la seule à promettre un délai chiffré. ➡️ **Ventiler par fréquence, puis trier par GRAVITÉ — pas par volume.** Un tri par volume l'aurait laissée en production indéfiniment.
- 🔴 **NOUVEAU — le même défaut existe sous des libellés de Question différents.** `Tempo de resposta?` (267) et `Quanto tempo demoram a chegar?` (960) sont **la même famille**, et `Qual é o tempo de chegada?` (51) porte déjà la **réponse conforme**. ➡️ **Regrouper les Questions par THÈME avant de compter ; la réponse conforme d'une Question est la source verbatim de ses sœurs.**
- 🔴 **NOUVEAU — une statistique non sourcée est un gisement au même titre qu'un prix.** ~60 fichiers, jamais mesurés parce qu'aucun contrôle ne cherchait le motif `N% dos/das`. **Deux chiffres du repo se contredisent.** ➡️ **Ajouter `grep -oE '[0-9]{1,3}% (dos|das|de)'` à l'audit récurrent des 4 repos.**
- 🔴 **NOUVEAU — un défaut documenté sur un repo doit être recherché sur les 3 autres DANS LE RUN QUI SUIT, et ça marche dans les deux sens.** CU a hérité de la question `altitude` (tranchée ici), EU hérite du prédicat `gratuit` et de la signature `<td>` de CU.
- 🔴 **Le prédicat d'un gisement doit être la QUESTION, pas la valeur de réponse.** Démontré deux fois sur ce repo.
- 🔴 **Deux réponses CONTRADICTOIRES à la même Question peuvent coexister en production** sans qu'aucun compteur ne s'en aperçoive. **Nouveau corollaire (venu de CU) : deux Questions DIFFÉRENTES d'un même thème peuvent aussi se contredire.**
- 🔴 **Une fourchette de prix est bannie même quand elle a l'air prudente** (`varia entre 80€ e 200€`, 26 fichiers).
- 🟢 **Le parsing exhaustif tient en quelques secondes au sandbox** (2 398 fichiers, 9 266 blocs). **Il n'y a aucune raison de continuer à grepper des motifs connus : ventiler coûte le même temps et trouve ce qu'on ne cherchait pas.** Vérifié une 3ᵉ fois.
- 🔴 **Une PR mergée peut DISPARAÎTRE de `main`** (constaté sur CNR, PR #300). ➡️ **Contrôle de fin de run : `git merge-base --is-ancestor <mergeCommit> <remote>/main`.**
- 🔴 **Le contrôle « la chaîne du script existe-t-elle en production ? » a invalidé 2 diagnostics sur 2.** À passer avant d'attribuer un défaut à un script versionné.
- 🔴 **Distinguer script one-shot et étape de build change complètement la décision.** `r12_*.py` (one-shot, sans effet en prod) vs `gen_concelhos.py` (générateur — **annule tout batch tant qu'il n'est pas corrigé**).
- 🔴 **Publier la ventilation complète est ce qui débloque une décision.** Patron validé : **ventiler → prototyper → demander le GO en un tap.**
- 🔴 **Choisir la page prototype aussi pour ce qu'elle ÉVITE** (pas de jumelle `public/`).
- **Toute purge de conformité doit re-parser le JSON-LD après coup.** ⚠️ Ne pas exiger « commence par une majuscule ».
- ⚠️ **HEURISTIQUE FAUSSE À NE PAS RÉINTRODUIRE** — « ce site = 70 €/h, donc un `65€` ici est une erreur » est **FAUX**. Distinction réelle : **70 €/h = main-d'œuvre électricité · 65 €/h = main-d'œuvre canalisation · 65 € = déplacement Z6**.
- **R145 autorise explicitement « 24h/7 dias »** (`AGENTS.md` L184). Ce qui est banni : les promesses de délai. ⚠️ **L'inverse des sites `*-norte-reparos`. Ne pas purger « 24h » ici.**
- **Quand une question FAQ porte sur un délai, retirer le couple Q/R plutôt que le réécrire** — sauf si une variante conforme de la MÊME Question existe déjà en production, auquel cas la transplanter verbatim (fait ce run).
- `_archive/` contient de vieux fichiers avec violations — **NE PAS patcher**, l'exclure de tous les greps.

## Edge cases détectés
- **`gh` et les credentials Git n'existent QUE sur le host macOS.** Sandbox = lecture / grep / parsing Python / **écriture de fichiers** — la substitution de masse sur 43 fichiers a été faite en Python au sandbox, puis committée depuis le host. **C'est la répartition la plus efficace.**
- **Le `/tmp` du sandbox ≠ le `/tmp` du host.** Worktrees sous `~/work/Sites/_worktrees/loop-YYYY-MM-DD/` — lisibles **et inscriptibles** depuis le sandbox.
- **Les commandes `git` ne fonctionnent PAS depuis le sandbox dans un worktree** (chemin absolu host dans `.git`). **L'écriture de fichiers, si.**
- 🔴 **`gh pr diff <n>` peut dépasser la limite de sortie de l'outil** (65 k caractères). Préférer `gh pr view <n> --json files --jq '.files[].path'`, puis `comm -12` contre `git diff --name-only` pour détecter un chevauchement.
- 🔴 **zsh ne fait PAS de word-splitting** — `set -- $var` dans une boucle échoue silencieusement.
- 🔴 **`grep -P` n'existe pas sur macOS.** Python pour tout motif non trivial. **Tout grep à motif non-ASCII passe par un script Python**, jamais une boucle inline `zsh -c`.
- 🔴 **`git commit -m` multiligne avec backticks/parenthèses est fragile en zsh.** `git commit -F -` + heredoc `<<'MSG'`.
- 🔴 **`set -e` + zsh : un glob sans correspondance fait AVORTER tout le script.** `setopt null_glob`.
- 🔴 **R6 interdit `--force`, donc une PR déjà ouverte se met à jour par MERGE de `main`, jamais par rebase.**
- **Worktree obligatoire** (R-WT) : copie de travail sale en permanence. **Jamais `reset --hard` / `stash` / `clean`.** Vérifié ce run : cette mention est bien une **interdiction**, pas une prescription — rien à corriger.

## Blocages connus
1. 🛑 **(b2′) 221 fichiers** — attente GO. **Le patch existe déjà (PR #311).**
2. 🛑 **(b1′) 960 fichiers** — attente GO.
3. 🛑 **(f) 842 fichiers** — attente GO.
4. 🛑 **(h) ~60 fichiers de statistiques non sourcées** — sourcer ou retirer, décision requise.
5. ⚠️ **Doublon `public/` ↔ racine** — arbitrage conjoint avec CU.
6. ⚠️ **`scripts/gen_concelhos.py`** — générateur suspecté pour `)EUR` : **le corriger AVANT toute purge des pages `concelhos/`**, sinon le batch sera annulé au prochain build.
7. ⚠️ **2 blocs `ld+json` JSON-invalides** — comptés, pas encore nommés.
