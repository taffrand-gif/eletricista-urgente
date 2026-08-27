# context.md — Loop State

> Écrit par le loop Cowork après chaque run. NE PAS ÉDITER MANUELLEMENT.

## Dernier run
- Date : 2026-08-27
- Tâches exécutées : **rang 2(b)** (CTA WhatsApp Markdown servi en texte) ✅ · **rang 4** (3 pages `<section>` 6/5) ✅ · **une seconde anomalie découverte sur `mirandela`** ✅
- Verdict livré : **rang 10** (re-mesure `gratuit` élargie) ✅
- **1 PR ouverte** :
  - **#336** — https://github.com/taffrand-gif/eletricista-urgente/pull/336 — branche `loop/2026-08-27-eu-cta-whatsapp-mort` — 5 commits, **4 fichiers de production** + `SEO_PLAN.md`
- Branche partie de `origin/main` = `bc0a124c9`.

### 🟢 ÉVÉNEMENT MAJEUR DU RUN — le stock de PR est vide
`gh pr list --state open` rend **0 PR ouverte sur les 4 repos**. Sur EU, #308 / #311 / #313 / #317 ont mergé. Les rangs 4, 5, 6 et 7 étaient **bloqués mécaniquement** par ce stock : **ils sont libres**.

### 1. Rang 2(b) — un CTA de money page qui n'était pas un lien
`[WhatsApp](https://wa.me/351932321892?text=…)` était servi tel quel au visiteur dans `public/blog/blog-problemas-eletricos-inverno.html`. Résidu du convertisseur Markdown traité par #317.

⚠️ **Le compteur brut était majoritairement composé de faux positifs légitimes** : prédicat « lien Markdown dans un fichier NON-`.md` » = **7 occurrences / 2 fichiers**, dont **6 dans `llms.txt`** — où le Markdown est **le format attendu** (spécification llms.txt). **Défaut réel : 1.**

Transformation `[X](U)` → `<a href="U">X</a>` : libellé et URL viennent **verbatim de la chaîne cassée elle-même**.

### 2. Rang 4 — invariant mesuré, pas choisi
| Invariant : profondeur `<section>` avant un `<section class="unique-urg-*">` | Valeur |
|---|---:|
| = 0 (sain) | **154** |
| ≠ 0 (cassé) | **3** — exactement les 3 fichiers visés |

Correctif identique à #316 (mergée) : insertion de `</section>`. Après patch : **157/157**.

### 3. 🔴 SECONDE ANOMALIE, famille différente, même fichier
Après réparation du `<section>`, `eletricista-urgente-mirandela.html` restait à `<div>` **−1**. Diagnostic par **diff de la séquence des balises `<div>`** contre un jumeau sain : **une seule différence sur 96 éléments** — un `<div class="wrap">` manquant en 5ᵉ position.

| Sur les **77** pages `eletricista-urgente-*` au motif de fin `</div></div></div><div class="cta-bottom">` | |
|---|---:|
| portant `</p></div><div class="wrap">` | **76** |
| ne le portant pas | **1 — mirandela** |
| déséquilibrées | **1 — mirandela, et elle seule** |

Après correction, la séquence de balises `<div>` de mirandela est **identique élément par élément** à celle de `-miranda-do-douro` (96 = 96).

### 4. 🔴 RANG 10 LIVRÉ — l'extrapolation depuis CNR est infirmée une SECONDE fois
**Périmètre énoncé** : tout le dépôt hors `_archive*`, hors `_audit/ _backlog/ docs/`, hors les 6 `.md` de doctrine racine, **`blog/*.md` INCLUS** = **2 542 fichiers**. Fenêtre de **60 caractères**.

| Repo | `orçamento`↔`gratuit` | Fichiers | Type |
|---|---:|---:|---|
| CNR | 4 701 | 2 037 | installation |
| ENR | 3 700 | 1 678 | installation |
| **EU** | **181** | **144** | **urgence** |
| CU | 110 | 100 | urgence |

🔴 **Le clivage sépare les deux sites d'INSTALLATION (~4 000 occ. chacun) des deux sites d'URGENCE (~150 chacun) — facteur ~30. Ce ne sont pas les mêmes chaînes de génération.**

Autres mesures : `Atendimento 24h` **2 439 / 1 293** · `gratuit*` toutes formes **227 / 160** · `Você` **42 / 22** (dont **18 en `.md`**) · corruption `*Parranj*` **25 / 16** (dont **8 en `.md`**) · `raio de 100 km` **5 / 5** · `30/40 % dos incêndios` **17 / 4**.
⚠️ **40 des 56 `.md` ont un jumeau `.html`** : sources de génération ⇒ occurrences **latentes**, pas closes.

## ✅ Gate merge — aucun gate actif
Aucune mention d'attente de merge dans le `context.md` lu ce run. Aucun gate réécrit. 0 PR ouverte ; la #336 a été ouverte.

🔴 **Rappel de doctrine, à ne jamais réécrire** : R7 interdit de **MERGER**, pas de **PRODUIRE**. Entre le 06/08 et le 09/08, « Attente GO merge (R7) » a été relue chaque nuit comme un ordre d'arrêt → **4 runs sans production**. **Ne jamais réécrire un gate de ce type.**

## 🎯 FILE DE TÂCHES LOOP — état au 2026-08-27

| Rang | Cible | Statut |
|---|---|---|
| — | CTA WhatsApp Markdown · 3 `<section>` 6/5 · `<div class="wrap">` de mirandela | ✅ **traités ce run (#336)** |
| — | Rang 10 — re-mesure `gratuit` élargie | ✅ **livré ce run** — 181 / 144, clivage installation/urgence identifié |
| **1** | 🟢 **`comparacao.html` — `<section>` +1, + 3 doublons JSON-LD, `<main>` 1/0** | 🟢 **LIBÉRÉ, aucun GO.** **Dernier déséquilibre `<section>` du dépôt.** Méthode CU #271 pour les doublons (**md5 par bloc**). ⚠️ Le `<section>` +1 se traite d'abord par le **diff de séquence** contre un jumeau sain — méthode validée ce run sur mirandela. |
| **2** | 🟢 **`eletricista-aguas-vivas.html`** — prologue dupliqué + `<style>` 2/3 + `<nav>` 2/3 + 3 doublons JSON-LD | 🟢 **LIBÉRÉ** (#308 mergée). Correctif de prologue **déjà écrit et prouvé** (#316) : retrait **par clé de balise**, contrôle « 0 balise retirée sans équivalent conservé ». |
| **3** | 🟢 **`contactos.html`** — ni DOCTYPE ni `<html lang>` | 🟢 **LIBÉRÉ.** **Correctif prouvé sur CU (#273, mergée)** : transplanter le prologue d'un jumeau, vérifier l'égalité byte-à-byte. |
| **4** | 🔴 **`eletricista-disjuntor-disparar-braganca.html` — `<h1>` multiples** | ⏳ **libre, aucun GO.** ⚠️ **LIRE LES OCCURRENCES AVANT DE FORMER UNE HYPOTHÈSE** : sur `blog-problemas-eletricos-inverno`, les deux hypothèses formées depuis le compteur étaient **fausses toutes les deux**. Le prédicat `<p>#{1,6}<h1>` ne rendait qu'un seul fichier ⇒ **c'est une autre cause**. |
| **5** | 🛑 **Les 56 `<strong>` non fermés** de `blog-problemas-eletricos-inverno.html` | 🛑 **63 ouvrants consécutifs, nombre IMPAIR** ⇒ appariement **non mécaniquement déterminé**. **Il faut une RÈGLE, pas un script.** *(Le `<li>` 35/10 hors `<ul>` du même fichier reste également ouvert.)* |
| **6** | 🛑 **Arbitrer les 2 `sameAs` contradictoires** des 5 pages `fuga-corrente` (+ `aguas-vivas`) | 🛑 **GO d'une ligne.** Le groupe A rattache des pages d'électricité à **deux sites de plomberie** et omet `eletricista-urgente.pt`. Correctif mécanique une fois le groupe de référence désigné. |
| **7** | 🟢 **`orçamento`↔`gratuit` — 181 occ. / 144 fichiers** | 🟢 **AUCUN GO — le volume ne le justifie pas.** Correctif prouvé et mergé sur CNR (#327) : `Orçamento gratuito` → `Orçamento por escrito`. **Bonne tâche de run de nuit.** ⚠️ Ventiler par famille avant de patcher. |
| **8** | **Ajouter le contrôle `@type` au balayage structurel et le passer ici** | ⏳ sans GO. **Sur CU il a sorti 27 nœuds JSON-LD non typés dans du JSON parfaitement valide** — validité JSON ≠ validité schema.org. **Jamais encore passé sur EU.** |
| **9** | 🔴 **Chercher ici les défauts sortis sur CU** | ⏳ sans GO. (a) **meta descriptions à sous-segment >25 c répété** — prédicat correct : « plus long **sous-segment** répété », pas « phrase égale » (le prédicat par phrase rend un **faux 0**) ; (b) 🔴 **pages en double par accent** — sur CU : **179 paires, 186 URLs `noindex` listées dans les sitemaps, 7 concelhos sans aucune page indexable**. ⚠️ **Mais le rang 10 vient de montrer que CU et EU n'ont PAS la même chaîne de génération que CNR/ENR — vérifier, ne pas extrapoler.** |
| **10** | **`Atendimento 24h` — 2 439 occ. / 1 293 fichiers** | 🛑 **GO périmètre.** ⚠️ **Requalifier d'abord** : R145 **autorise** `24h/7 dias`. Une part importante de ce compteur est probablement conforme. |
| **11** | **Statistiques non sourcées — `30%` vs `40% dos incêndios domésticos`, 17 occ. / 4 fichiers** | 🟢 **AUCUN GO : ce n'est pas une décision d'offre, c'est une ERREUR FACTUELLE** (deux chiffres contradictoires en production). Petit lot. |
| **12** | **`Você` — 42 occ. / 22 fichiers** (dont **18 en `.md`**) | 🛑 corpus INTERDIT, GO requis. ℹ️ **24 seulement sont dans du HTML servi** ; les 18 autres sont **latentes en source**. **Deux verdicts distincts.** |
| **13** | **Corruption `*Parranj*` — 25 occ. / 16 fichiers** (dont **8 en `.md`**) | ⏳ **GO périmètre.** Les 5 `href` corrompus (`/arranjacao-avarias-eletricas`) **n'ont de cible sous aucune des deux formes** → liens morts antérieurs au batch, **à traiter séparément**. |
| 14 | **Si GO** : les 221 fichiers de `Tempo de resposta?` | 🛑 patch déjà écrit |
| 15 | **Si GO** : les 22 `Sem custo extra de fim de semana` | 🛑 ℹ️ **Sur CU, les 76 occurrences de ce motif étaient TOUTES dans `_archive/`** — vérifier ici avant de dépenser l'arbitrage. |
| 16 | Arbitrer le doublon `public/` ↔ racine, conjointement avec CU | ⏸ **lié au rang 9(b)** |

## Tâche suivante recommandée
1. 🟢 **Rang 1 — `comparacao.html`** : dernier déséquilibre `<section>` du dépôt, **libéré ce run**. Employer le **diff de séquence contre un jumeau sain** (méthode validée ce run) plutôt qu'un compteur.
2. 🟢 **Rangs 2 et 3 — `eletricista-aguas-vivas.html` et `contactos.html`** : deux correctifs **déjà écrits et prouvés** (#316 et CU #273), libérés par les merges. Aucun GO.
3. 🟢 **Rang 11 — les statistiques contradictoires `30%` / `40% dos incêndios`** : 4 fichiers, erreur factuelle, aucun GO.
4. **Rang 4 — `disjuntor-disparar-braganca`.** ⚠️ **Lire les occurrences avant de former une hypothèse.**
5. **Rang 8 — ajouter `@type` au balayage structurel.**
6. **Poser en une ligne** le GO `sameAs` (rang 6) et la RÈGLE d'appariement des `<strong>` (rang 5).

## Apprentissages (self-improving)
- 🔴 **NOUVEAU — un compteur brut peut être majoritairement composé de faux positifs LÉGITIMES.** 7 liens Markdown détectés hors `.md`, **6 dans `llms.txt` où le Markdown est le format attendu**. Sans requalification, le run « corrigeait » un fichier parfaitement sain. ➡️ **Avant de patcher un format, vérifier que le fichier n'a pas ce format pour vocation.**
- 🔴 **NOUVEAU — le DIFF DE SÉQUENCE de balises localise un défaut là où le compteur n'en dit que l'existence.** « `div` −1 » ne se répare pas ; « il manque `<div class="wrap">` en 5ᵉ position, et 76 pages sur 77 l'ont » se répare **et se prouve**. Coût : une commande `difflib` contre un jumeau sain. ➡️ **À ajouter au balayage structurel comme outil de diagnostic standard.**
- 🔴 **NOUVEAU — l'égalité de SÉQUENCE avec un jumeau sain est un témoin plus fort que l'équilibre à 0.** Deux fichiers peuvent être tous deux équilibrés et structurés différemment. **L'égalité élément par élément ne laisse pas de place au doute.**
- 🔴 **NOUVEAU — une extrapolation inter-repos est une hypothèse, pas un résultat, et elle coûte une commande à tester.** Deux mesures indépendantes (CU puis EU) infirment celle de CNR, et révèlent au passage **un clivage structurel installation / urgence** que personne n'avait formulé. ➡️ **Ne jamais demander un GO sur un volume extrapolé.**
- 🔴 **NOUVEAU — un blocage « mécanique » n'est pas un arbitrage : il se re-teste à chaque run.** Quatre rangs d'EU attendaient un **merge**, pas un GO. ➡️ **Toujours écrire, à côté d'un blocage, PAR QUOI il tombe.**
- 🔴 **Un fichier peut porter DEUX défauts de familles différentes — et le second n'apparaît qu'APRÈS la réparation du premier.** mirandela : `<section>` +1 *et* `<div>` −1. **Dérouler la pile jusqu'au bout.**
- 🔴 **Un compteur de balises ne dit pas QUEL défaut il compte, et les hypothèses formées à partir de lui sont souvent toutes fausses.** ➡️ **LIRE les occurrences avant de former une hypothèse sur leur cause.**
- 🔴 **Le pire défaut d'une page n'est pas toujours celui qu'on comptait.** **Le compteur ouvre la porte, il ne décrit pas la pièce.**
- 🔴 **La convention de remplacement se MESURE sur les pages saines, elle ne se choisit pas.**
- 🔴 **Une parité IMPAIRE prouve qu'un appariement n'est pas mécanique.** **Le nombre impair est en soi un critère d'arrêt objectif.** (Rang 5.)
- 🔴 **Un retrait de texte visible peut être PROUVÉ sans perte** quand l'information retirée est déjà portée ailleurs dans le même fichier.
- 🔴 **Une correction purement structurelle doit le PROUVER** : l'égalité **stricte et bilatérale** des ensembles de mots avant/après. Ce run : identiques sur les 4 fichiers.
- 🔴 **Le retrait d'un doublon devient prouvable quand on le fait par CLÉ, pas par bloc.** Contrôle « 0 balise retirée sans équivalent conservé ».
- 🔴 **Un `grep` qui ne trouve rien parce que son FICHIER D'ENTRÉE n'existe pas ne produit aucune erreur.** **Un contrôle qui rend 0 doit prouver que sa source est non vide.** ⚠️ Variante subtile rencontrée sur CU ce run : le contrôle était juste, **c'est le PÉRIMÈTRE qui rendait 0** (les `.md` avaient été exclus).
- 🔴 **Le choix d'exclure les `.md` d'un périmètre n'est pas neutre.** Sur CNR/ENR ce sont des documents de doctrine qui *citent* les règles (faux positifs) ; **ici, 40 des 56 `.md` ont un jumeau `.html`** : ce sont des **sources de génération**. **Écrire le périmètre ET justifier chaque exclusion, repo par repo.**
- 🔴 **« Zéro dans le HTML servi » ne veut pas dire « clos ».** Une occurrence vivant dans une source de génération est **latente** : elle reviendra au build. **Distinguer purge de production et hygiène de source.**
- 🔴 **Validité JSON ≠ validité schema.org.** **Ajouter au balayage structurel : tout objet d'un bloc `ld+json` doit porter `@type`.**
- 🔴 **La profondeur d'imbrication est un invariant mesurable, et il tranche là où le compteur ne dit rien.** 154/157 ici ; 147/152 le 24/08 ; 2843/2843 sur ENR.
- 🔴 **Quand un bloc est du gabarit, la POPULATION le prouve.** **Compter les variantes avant de transplanter.** Ce run : 76 donneurs, 1 seule forme.
- 🔴 **Le même fichier porte le même défaut sur deux repos** (`blog-problemas-eletricos-inverno.html`, ici et sur ENR). ➡️ **Quand un défaut sort sur un repo, le chercher par NOM DE FICHIER sur les trois autres.**
- 🔴 **Le balayage structurel est productif sur les 4 repos.** ➡️ **Étape FIXE du loop** : équilibre des balises + **profondeur aux points de repère** + **diff de séquence contre un jumeau sain** + `<h1>` multiples + validité JSON-LD + **présence de `@type`** + doublons byte-à-byte + DOCTYPE + `<html lang>` + **unicité des `<meta robots>` et des `<title>`** + **marqueurs de langage source non convertis (`#`, `---`, `[x](y)`, `${…}`)**.
- 🔴 **Le contrôle des PR ouvertes se fait AVANT de calculer le périmètre.** ⚠️ **Un titre de PR ne dit pas ce qu'elle couvre** — lire le **diff**.
- 🔴 **« Valeur non sourçable » se PROUVE en remontant la chaîne de définition.**
- 🔴 **Un défaut DÉJÀ RÉPARÉ qui revient est un générateur non corrigé** : `git log -S <motif>` avant de patcher.
- 🔴 **`_archive/` fausse tous les compteurs** — et **exclure `_archive-*` aussi**, pas seulement `_archive/`.
- 🔴 **Un compteur de violation vaut ce que vaut son PÉRIMÈTRE, et le périmètre est presque toujours IMPLICITE.** **Ne jamais écrire « il en reste N » sans écrire sur quel arbre, avec quel motif et avec quelle fenêtre.**
- **Ne pas sur-purger.** R4 se viole dans les deux sens.

## Edge cases détectés
- 🔴 **Le checkout partagé d'EU est SUR `main`.** `git worktree add … -B main` échoue (« 'main' is already used by worktree »). ➡️ **Créer le worktree de `context.md` en `--detach` sur `origin/main` et pousser `HEAD:main`.** ✅ Appliqué ce run. Ne jamais tenter de récupérer la branche `main` du checkout partagé (R-WT).
- **Ce repo n'a QU'UN remote : `origin`.** (CNR est le seul des 4 à avoir `github` **et** `origin`.)
- ⚠️ **L'ancre du HISTORIQUE diffère d'un repo à l'autre, et ce repo en a DEUX** : `## 🔄 HISTORIQUE P0 (batch 04/07/2026)…` (L216) et **`## 🔄 HISTORIQUE` (L249, la bonne)**. **Insérer sur une ÉGALITÉ EXACTE de ligne (`assert`), jamais sur un `in` de sous-chaîne.**
- 🔴 **Le `/tmp` du sandbox ≠ le `/tmp` du host.** Vaut pour les `--body-file` **et pour tout fichier intermédiaire de contrôle**. Écrire sous `~/work/Sites/_worktrees/` ou `~/work/Sites/_loop-<date>/`, **hors du worktree**.
- **`gh` et les credentials Git n'existent QUE sur le host macOS.** Reconfirmé ce run : `git push --dry-run` depuis le sandbox → `could not read Username for 'https://github.com'`, et `gh` est absent du `PATH` du sandbox. **Répartition** : lecture / `git fetch` / grep / parsing Python / **écriture de fichiers** → sandbox ; `git` en écriture / `gh` → **host**. Le montage étant partagé, un `git fetch` lancé depuis le sandbox met bien à jour le vrai `.git`. ⚠️ Il émet alors un avertissement `gh auth git-credential store: … not found` — **bénin, le fetch réussit**.
- 🔴 **Un worktree n'est PAS un dépôt git vu depuis le sandbox** : `git show`/`diff`/`log` y rendent des **compteurs à zéro** trompeurs. **Tout témoin se compte en Python sur le CONTENU des fichiers.** ✅ En revanche `git show HEAD:<path>` **dans le worktree depuis le HOST** fonctionne — c'est le canal du contrôle de blob post-commit.
- ⚠️ **Borner explicitement ce qu'on imprime** en balayant ~2 400 fichiers.
- 🔴 **`grep -P` n'existe pas sur macOS** ; **`grep -E` de macOS ne matche pas de façon fiable les accents** ; **`grep -c '***'` échoue en zsh**. **Pour tout motif accentué ou non trivial : Python.**
- 🔴 **`git commit -m` multiligne est fragile en zsh** → `printf … | git commit -F -`. **ASCII dans les messages de commit, UTF-8 dans les fichiers.** Corps de PR : `--body-file`, jamais `--body` inline.
- **Worktree obligatoire** (R-WT). **Jamais `reset --hard` / `checkout -- .` / `stash` / `clean`** sur le checkout partagé. Aucun `context.md` ne *prescrit* de `reset --hard`.

## Blocages connus
1. 🛑 **RANG 5 — les 56 `<strong>` non fermés**, 63 ouvrants consécutifs, **nombre impair**. **Tombe par : une RÈGLE d'appariement, pas un script.**
2. 🛑 **RANG 6 — les 2 `sameAs` contradictoires** des pages `fuga-corrente`. **Tombe par : un GO d'une ligne** désignant le groupe de référence.
3. 🛑 **RANG 10 — `Atendimento 24h`, 2 439 occ.** ⚠️ **À requalifier avant de demander le GO** : R145 autorise `24h/7 dias`.
4. 🛑 **RANG 12 — `Você`, 42 occ.** dont **18 latentes en source**. **Deux verdicts distincts à rendre.**
5. 🛑 **RANG 13 — corruption `*Parranj*`, 25 occ.** ⚠️ Les 5 `href` corrompus n'ont de cible sous **aucune** des deux formes ⇒ liens morts **antérieurs** au batch, **à traiter séparément**.
6. ✅ **RÉSOLU — le stock de PR ouvertes.** 4 → **0**. Quatre rangs libérés d'un coup. **Ce n'était pas un blocage de fond, c'était une attente.**
7. 🔴 **La cause racine reste inconnue** pour le Markdown non converti, pour les prologues dupliqués et pour les `<section>`/`<div>` amputés. **Trois défauts issus de la même chaîne de génération.** ⚠️ **Mais le rang 10 vient d'établir que EU/CU et CNR/ENR n'ont PAS la même chaîne** (facteur ~30 sur le même prédicat) : **il y a au moins DEUX générateurs à auditer, pas un.** ➡️ **C'est le seul chantier qui change l'ordre de grandeur du backlog.**
