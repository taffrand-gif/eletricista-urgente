# context.md — Loop State

> Écrit par le loop Cowork après chaque run. NE PAS ÉDITER MANUELLEMENT.

## Dernier run
- Date : 2026-08-25
- Tâche prévue : **rang 1 — le `<h1>` 25/1 de `public/blog/blog-problemas-eletricos-inverno.html`**. ✅ **Exécutée** — et **les deux hypothèses du 24/08 étaient fausses toutes les deux.**
- **1 PR ouverte** :
  - **#317** — https://github.com/taffrand-gif/eletricista-urgente/pull/317 — branche `loop/2026-08-25-eu-h1-duplique` — 2 commits, **1 fichier de production** + `SEO_PLAN.md`
- État de #316 (run du 24/08) : **toujours ouverte**. 4 PR ouvertes.

### 1. 🔴 Ce n'était ni un corps dupliqué ni des `<h1>` en sous-titres : c'est un document MARKDOWN publié sans conversion
Le fichier ne contient **qu'un seul `<h1>…</h1>` réel**. Les 24 autres `<h1>` sont **ouvrants et jamais fermés** :

```html
<p>#<h1>Introdução</p>
<p>##<h1>O Problema<br>Durante o inverno, muitas casas…</p>
```

Le convertisseur a laissé les marqueurs `#` / `##` **en texte** *et* émis un `<h1>` ouvrant pour chacun. **Les 23 `<h1>` non fermés imbriquaient tout le corps de l'article dans des éléments de titre.**

Prédicat `<p>#{1,6}<h1>` sur tout le dépôt : **23 occurrences / 1 seul fichier**. Défaut isolé, pas une famille.

### 2. 🔴 Le compteur pointait les `<h1>` ; en les lisant, on a trouvé pire
- **Le front-matter de l'auteur était servi en clair aux visiteurs**, en tête d'article : « **Meta Title:** … **Meta Description:** … **Palavras-chave:** … ». Retiré, **sans perte prouvée** : le `<head>` porte déjà son propre `<title>` et sa `<meta description>`, rédigés différemment.
- **10 séparateurs Markdown `<p>---</p>`** servis en clair. Retirés.
- 🔴 **Un lien Markdown brut servi en TEXTE** : `[WhatsApp](https://wa.me/351932321892…)` — **le CTA WhatsApp de l'article n'est pas cliquable.** Non réparé (voir rang 2).

**Rien de tout cela n'était compté par quoi que ce soit.**

### 3. La convention de remplacement a été MESURÉE
| Invariant sur les 35 articles de blog sains | Valeur |
|---|---|
| `<h2>` sous `<article>` | **297** |
| `<h3>` sous `<article>` | **330** |
| Pages de blog portant exactement **un** `<h1>` | **41 / 41** |

D'où `#` → `<h2>` et `##` → `<h3>`. Sans cette mesure, le niveau aurait été arbitraire.

### 4. Un nombre IMPAIR est un critère d'arrêt objectif
**56 `<strong>` non fermés** (le convertisseur écrit `<strong>texte<strong>`). La séquence relevée est de **63 ouvrants consécutifs — impair** : l'appariement n'est donc **pas mécaniquement déterminé**. Non patché : il faut une règle, pas un script.

## ✅ Gate merge — aucun gate actif
Vérifié ce run : **aucune mention d'attente de merge**. Aucun gate réécrit. 4 PR étaient ouvertes ; la #317 a été ouverte quand même.

🔴 **Rappel de doctrine, à ne jamais réécrire** : R7 interdit de **MERGER**, pas de **PRODUIRE**. Entre le 06/08 et le 09/08, « Attente GO merge (R7) » a été relue chaque nuit comme un ordre d'arrêt → **4 runs sans production**. **Ne jamais réécrire un gate de ce type.**

## 🎯 FILE DE TÂCHES LOOP — état au 2026-08-25

| Rang | Cible | Statut |
|---|---|---|
| — | `blog-problemas-eletricos-inverno.html` — 23 titres Markdown + front-matter fuité + 10 `---` | ✅ **traité ce run (#317)** |
| **1** | 🔴 **`eletricista-disjuntor-disparar-braganca.html` — `<h1>` multiples** | ⏳ **libre, aucun GO.** ⚠️ **LIRE LES OCCURRENCES AVANT DE FORMER UNE HYPOTHÈSE** : sur `blog-problemas-eletricos-inverno` ce run, les deux hypothèses formées depuis le compteur étaient fausses. Vérifier d'abord si le prédicat `<p>#{1,6}<h1>` s'y applique (il rendait 23/1 fichier au moment du run, donc **non**) — c'est donc **une autre cause**. |
| **2** | 🔴 **NOUVEAU — les 3 artefacts restants du convertisseur sur `blog-problemas-eletricos-inverno.html`** | ⏳ **libre.** (a) **56 `<strong>` non fermés** — 63 ouvrants consécutifs, **nombre impair**, appariement non mécanique → **règle requise** ; (b) 🔴 **le lien Markdown `[WhatsApp](…)` servi en texte : CTA mort** — même nature que le JSX brut de CNR ; (c) `<li>` 35/10 hors `<ul>`. **(b) est le plus rentable : un CTA WhatsApp mort sur une money page de blog.** |
| **3** | 🛑 **Arbitrer les 2 `sameAs` contradictoires** des 5 pages `fuga-corrente` (+ `aguas-vivas`) | 🛑 **GO d'une ligne.** Le groupe A rattache des pages d'électricité à **deux sites de plomberie** et omet `eletricista-urgente.pt`. Correctif mécanique une fois le groupe de référence désigné. |
| **4** | **Les 3 pages restantes de la famille `<section>` 6/5** : `miranda-do-douro` + `alfandega-da-fe` (**PR #311**), `mirandela` (**PR #313**) | ⏸ **correctif identique à #316, prouvé, aucun GO.** **Invariant à réappliquer : profondeur `section` = 1 pour `unique-urg-*` (147/152).** |
| **5** | **`eletricista-aguas-vivas.html`** — prologue dupliqué + `<style>` 2/3 + `<nav>` 2/3 + 3 doublons JSON-LD | ⏸ **pris par la PR #308.** Correctif de prologue **déjà écrit et prouvé** (#316). |
| **6** | **`contactos.html`** — ni DOCTYPE ni `<html lang>` | ⏸ **pris par une PR ouverte.** **Correctif prouvé sur CU (#273, mergée)** : transplanter le prologue d'un jumeau, vérifier l'égalité byte-à-byte. |
| **7** | **`comparacao.html`** — 3 doublons JSON-LD + `<main>` 1/0, `<section>` 1/0 | ⏸ **pris par une PR ouverte.** Méthode CU #271 dès libération. |
| **8** | **Ajouter le contrôle `@type` au balayage structurel et le passer ici** | ⏳ sans GO. **Sur CU il a sorti 27 nœuds JSON-LD non typés dans du JSON parfaitement valide** — validité JSON ≠ validité schema.org. **Jamais encore passé sur EU.** |
| **9** | 🔴 **NOUVEAU — chercher ici les défauts sortis sur CU le 25/08** | ⏳ sans GO. (a) **meta descriptions à segment >25 c répété** — prédicat corrigé : « plus long **sous-segment** répété », pas « phrase égale » (le prédicat par phrase rend un **faux 0**) ; (b) 🔴 **pages en double par accent** — sur CU : **179 paires, 186 URLs `noindex` listées dans les sitemaps, 7 concelhos sans aucune page indexable.** **EU a la même chaîne de génération.** |
| **10** | 🔴 **NOUVEAU — remesurer `gratuit` avec PÉRIMÈTRE ET MOTIF ÉLARGIS** | ⏳ **Sur CNR le 25/08, le même prédicat est passé de « ~27 restantes » à 3822 occ / 1723 fichiers.** Une seule commande Python. |
| **11** | **Corruption `repar`→`arranj` — 30 occ / 20 fichiers** | ⏳ **GO périmètre.** Les 5 `href` corrompus (`/arranjacao-avarias-eletricas`) **n'ont de cible sous aucune des deux formes** → liens morts antérieurs au batch, à traiter séparément. |
| **12** | **`Você` — 22 occ / 16 fichiers** | 🛑 corpus INTERDIT, GO requis. ℹ️ **Chercher les doublons d'abord.** |
| **13** | Statistiques non sourcées — commencer par `30%` vs `40% dos incêndios domésticos` | ⏳ **2 + 5 fichiers, aucune décision d'offre : c'est une ERREUR FACTUELLE.** Sans GO. |
| 14 | **Si GO** : les 221 fichiers de `Tempo de resposta?` | 🛑 patch déjà écrit et en revue (PR #311) |
| 15 | **Si GO** : les 22 `Sem custo extra de fim de semana` | 🛑 ℹ️ **Sur CU, les 76 occurrences de ce motif étaient TOUTES dans `_archive/`** — vérifier ici avant de dépenser l'arbitrage. |
| 16 | Arbitrer le doublon `public/` ↔ racine, conjointement avec CU | ⏸ **lié au rang 9(b)** — c'est probablement le même dossier. |

## Tâche suivante recommandée
1. **Rang 2(b) — le lien Markdown `[WhatsApp](…)` servi en texte.** Un CTA mort sur une page de blog. Correctif d'une ligne, aucun GO. **Le meilleur rapport effort/valeur du repo.**
2. **Rang 9 — chercher ici les deux défauts sortis sur CU le 25/08**, en priorité les **pages en double par accent** : sur CU, 179 paires et **7 concelhos hors index**. Même générateur → forte probabilité.
3. **Rang 1 — `disjuntor-disparar-braganca`.** ⚠️ **Lire les occurrences avant de former une hypothèse.**
4. **Rang 10 — remesurer `gratuit`** (périmètre + motif élargis). Une commande, potentiellement deux ordres de grandeur.
5. **Rang 8 — ajouter `@type` au balayage structurel.**
6. **Poser en une ligne** le GO `sameAs` (rang 3).

## Apprentissages (self-improving)
- 🔴 **NOUVEAU — un compteur de balises ne dit pas QUEL défaut il compte, et les hypothèses formées à partir de lui sont souvent toutes fausses.** « `<h1>` 25/1 » avait produit deux hypothèses plausibles (corps dupliqué / `<h1>` en sous-titres) ; la réalité était une troisième chose invisible depuis le compteur : **du Markdown non converti**. ➡️ **LIRE les occurrences avant de former une hypothèse sur leur cause.** Coût : une commande qui imprime leur contexte.
- 🔴 **NOUVEAU — le pire défaut d'une page n'est pas toujours celui qu'on comptait.** En lisant les `<h1>`, on a trouvé le **front-matter de l'auteur servi aux visiteurs** et un **CTA WhatsApp non cliquable**, que rien ne comptait. **Le compteur ouvre la porte, il ne décrit pas la pièce.**
- 🔴 **NOUVEAU — la convention de remplacement se MESURE sur les pages saines, elle ne se choisit pas.** `#`→`<h2>`, `##`→`<h3>` s'appuient sur 297 `<h2>` / 330 `<h3>` relevés dans 35 articles sains et sur « 41/41 des pages saines portent exactement un `<h1>` ».
- 🔴 **NOUVEAU — une parité IMPAIRE prouve qu'un appariement n'est pas mécanique.** 63 `<strong>` ouvrants consécutifs ne peuvent pas former des paires bien définies. **Le nombre impair est en soi un critère d'arrêt objectif, pas une prudence.**
- 🔴 **NOUVEAU — un retrait de texte visible peut être PROUVÉ sans perte** quand l'information retirée est déjà portée ailleurs dans le même fichier (ici `<title>` et `<meta description>` du `<head>`). **C'est la seule façon de retirer du texte visible sans violer R4.**
- 🔴 **Un compteur de balises peut sous-décrire le défaut d'un ordre de grandeur.** `<html> 3/1` = **une money page désindexée**. **Quand un prologue est dupliqué, LISTER les `<meta robots>` et les `<title>` effectivement servis** : le parseur fusionne, et c'est la fusion qui décide.
- 🔴 **Le retrait d'un doublon devient prouvable quand on le fait par CLÉ, pas par bloc.** Ne retirer que les balises dont la clé est déjà présente ; contrôle « **0 balise retirée sans équivalent conservé** ». **Réutilisable sur tous les prologues dupliqués des 4 repos.**
- 🔴 **Un `grep` qui ne trouve rien parce que son FICHIER D'ENTRÉE n'existe pas ne produit aucune erreur.** ➡️ **Tout contrôle s'exécute là où vit son fichier d'entrée**, et **un contrôle qui rend 0 doit prouver que sa source est non vide**. ℹ️ **Confirmé une deuxième fois sur CU le 25/08** : un prédicat « deux phrases égales » y a rendu **0 sur 2453 pages** alors que la famille comptait 11 pages — **c'était le prédicat qui était faux.** ➡️ **Quand un contrôle rend 0 sur une famille qu'un run antérieur a comptée NON VIDE, c'est le CONTRÔLE qui est en cause.**
- 🔴 **Restaurer un fichier patché à tort se fait sur des CHEMINS NOMMÉS**, jamais sur `.`, même dans un worktree dédié.
- 🔴 **Validité JSON ≠ validité schema.org.** **Ajouter au balayage structurel : tout objet d'un bloc `ld+json` doit porter `@type`.**
- 🔴 **La profondeur d'imbrication est un invariant mesurable, et il tranche là où le compteur ne dit rien.** 147/152 ici ; **2843/2843 sur ENR le 25/08**. **Mesurer la profondeur aux points de repère, pas seulement les totaux.**
- 🔴 **Une balise ouvrante sans contenu ni fermeture, c'est un BLOC MANQUANT, pas une erreur de syntaxe.**
- 🔴 **Quand un bloc est du gabarit, la POPULATION le prouve.** **Compter les variantes avant de transplanter.** ℹ️ **Corollaire ENR du 25/08 : un donneur UNIQUE reste un fait mesuré si sa FORME est unique.**
- 🔴 **Le même fichier porte le même défaut sur deux repos** (`blog-problemas-eletricos-inverno.html`, ici et sur ENR). ➡️ **Quand un défaut sort sur un repo, le chercher par NOM DE FICHIER sur les trois autres.** ⚠️ Sur ENR le fichier est **pris par une PR ouverte** — rouvrir dès libération, le correctif est désormais écrit et prouvé (#317).
- 🔴 **Le balayage structurel est productif sur les 4 repos.** ➡️ **Étape FIXE du loop** : équilibre des balises + **profondeur aux points de repère** + `<h1>` multiples + validité JSON-LD + **présence de `@type`** + doublons byte-à-byte + DOCTYPE + `<html lang>` + **unicité des `<meta robots>` et des `<title>`** + **marqueurs de langage source non convertis (`#`, `---`, `[x](y)`, `${…}`)**.
- 🔴 **Le contrôle des PR ouvertes se fait AVANT de calculer le périmètre** — et **son résultat doit être vérifié**. **7ᵉ run consécutif qu'il évite un conflit.**
- 🔴 **Un doublon byte-à-byte est le seul retrait qui se prouve sans arbitrage** — exception : le doublon **par clé de balise**.
- 🔴 **« Valeur non sourçable » se PROUVE en remontant la chaîne de définition.**
- 🔴 **Un défaut DÉJÀ RÉPARÉ qui revient est un générateur non corrigé** : `git log -S <motif>` avant de patcher.
- 🔴 **`_archive/` fausse tous les compteurs** — et **exclure `_archive-*` aussi**, pas seulement `_archive/`.
- 🔴 **Un compteur de violation vaut ce que vaut son PÉRIMÈTRE, et le périmètre est presque toujours IMPLICITE** (leçon CNR du 25/08 : 27 annoncées → 3822 réelles). **Ne jamais écrire « il en reste N » sans écrire sur quel arbre et avec quel motif.**
- **Ne pas sur-purger.** R4 se viole dans les deux sens.

## Edge cases détectés
- 🔴 **Le checkout partagé d'EU est SUR `main`.** `git worktree add … -B main` échoue (« 'main' is already used by worktree »). ➡️ **Créer le worktree de `context.md` en `--detach` sur `origin/main` et pousser `HEAD:main`.** Ne jamais tenter de récupérer la branche `main` du checkout partagé (R-WT).
- **Ce repo n'a QU'UN remote : `origin`.** (CNR est le seul des 4 à avoir `github` **et** `origin`.)
- ⚠️ **L'ancre du HISTORIQUE diffère d'un repo à l'autre, et ce repo en a DEUX** : `## 🔄 HISTORIQUE P0 (batch 04/07/2026)…` (L216) et `## 🔄 HISTORIQUE` (L249, **la bonne**). **Insérer sur une correspondance EXACTE de ligne, jamais sur un `in` de sous-chaîne.**
- 🔴 **Le `/tmp` du sandbox ≠ le `/tmp` du host.** Vaut pour les `--body-file` **et pour tout fichier intermédiaire de contrôle**. Écrire sous `~/work/Sites/_worktrees/` ou `~/work/Sites/_loop-<date>/`, **hors du worktree**.
- **`gh` et les credentials Git n'existent QUE sur le host macOS.** Reconfirmé le 25/08 : `git push --dry-run` depuis le sandbox → `could not read Username for 'https://github.com'`. Répartition : lecture / grep / parsing Python / **écriture de fichiers** → sandbox ; `git` en écriture / `gh` → host.
- 🔴 **Un worktree n'est PAS un dépôt git vu depuis le sandbox** : `git show`/`diff`/`log` y rendent des **compteurs à zéro** trompeurs. **Tout témoin se compte en Python sur le CONTENU des fichiers.**
- ⚠️ **Borner explicitement ce qu'on imprime** en balayant ~2 400 fichiers.
- 🔴 **`grep -P` n'existe pas sur macOS** ; **`grep -E` de macOS ne matche pas de façon fiable les accents** ; **`grep -c '***'` échoue en zsh**. **Pour tout motif accentué ou non trivial : Python.**
- 🔴 **Une f-string Python ne peut pas contenir de backslash dans son expression** — sortir les regex en constantes, ou utiliser `%`.
- 🔴 **`git commit -m` multiligne est fragile en zsh** → `printf … | git commit -F -`. **ASCII dans les messages de commit**, UTF-8 dans les fichiers. Corps de PR : `--body-file`, jamais `--body` inline.
- **Worktree obligatoire** (R-WT). **Jamais `reset --hard` / `checkout -- .` / `stash` / `clean`** sur le checkout partagé. Aucun `context.md` ne *prescrit* de `reset --hard`.

## Blocages connus
1. 🛑 **GO d'une ligne — les 2 `sameAs` contradictoires** des pages `fuga-corrente` : des pages d'électricité rattachées à deux sites de plomberie, `eletricista-urgente.pt` omis.
2. ⏸ **Rangs 4, 5, 6 et 7 pris par des PR ouvertes** — attentes de merge, pas blocages de fond. **Tous les correctifs sont écrits et prouvés. Les rangs 1, 2, 8, 9, 10 et 13 sont LIBRES.**
3. 🛑 **GO périmètre — corruption `repar`→`arranj`** : 30 occ / 20 fichiers ici, 523 sur les 4 repos.
4. 🛑 **`Você`** — corpus INTERDIT, GO requis. **Chercher les doublons d'abord.**
5. 🛑 **Batches en attente de GO** : 221 (`Tempo de resposta?`), 22 (`Sem custo extra de fim de semana` — **vérifier d'abord archive vs production**), 960, 842.
6. ⚠️ **La chaîne de génération de pages statiques reste non auditée. Le dossier ne cesse de grossir.** Familles imputables sur les 4 repos : marqueurs `##style##` · corps de page dupliqués · JSON-LD tronqué écrasant un `<style>` · JSX non compilé (CNR) · prologue absent (CU) · mutation `@context` (ENR + CU) · prologue **triplé** avec `robots` contradictoires (EU) · `"type"` au lieu de `"@type"` (CU) · perte du `<div>` ouvrant du bloc de liens internes (ENR) · double génération accentuée / non accentuée (CU, 179 paires) · **et désormais Markdown publié sans conversion (EU)**. **ONZE familles, une chaîne.** **C'est le point de levier le plus élevé des 4 repos, et de loin. Corriger le générateur vaut mieux que N patchs.**
