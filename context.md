# context.md — Loop State

> Écrit par le loop Cowork après chaque run. NE PAS ÉDITER MANUELLEMENT.

## Dernier run
- Date : 2026-08-23
- Tâche prévue : rang 2 — contrôler `comparacao.html`. **Toujours pris par une PR ouverte**, comme le rang 3.
- Tâche réellement exécutée : **un balayage structurel systématique de tout le dépôt** (2 398 fichiers HTML), méthode transposée d'ENR et CU le même run. Il a sorti **deux familles homogènes de 6 fichiers**, dont l'une avait perdu du contenu réel.
- **1 PR ouverte** :
  - **#315** — https://github.com/taffrand-gif/eletricista-urgente/pull/315 — branche `loop/2026-08-23-eu-structure` — 13 commits, **12 fichiers de production** + `SEO_PLAN.md`

### 1. 🔴 Six articles de blog avaient PERDU leur bloc E-E-A-T entier (PR #315)
`public/blog/{aquecedor-eletrico-barulho-causa, cabo-eletrico-quente-perigo, casa-toda-sem-luz-o-que-fazer, cheiro-ozono-casa-eletricidade, cheiro-plastico-queimado-tomada, cheiro-queimado-casa-eletricidade}.html`

Les six se terminaient par `…</div></article><section class="eeat" …>` suivi **immédiatement** de `</body></html>` : **balise ouverte, contenu absent, jamais fermée**, `</main>` perdu avec. Témoins `<main>` **1/0**, `<section>` **1/0**.

🔴 **Ce n'est pas un défaut de validation.** Le bloc E-E-A-T **ne s'affichait pas du tout**, et avec lui **5 liens internes par page** vers `/sobre.html`, `/equipa.html`, `/garantia.html`, `/metodologia.html`, `/imprensa.html` — **30 liens de maillage E-E-A-T disparus**, sur les pages mêmes qui doivent porter le signal d'expertise. **Aucun audit de maillage ne le voyait : les liens n'étaient pas cassés, ils n'existaient plus.**

**Preuve d'unanimité** : sur les 42 pages de `public/blog/` portant cette section, balise ouvrante identique **42/42**, contenu byte-identique **36/36** (une seule variante md5, 1 265 octets). C'est du gabarit. Contenu transplanté **verbatim** ; **preuve après patch : bloc reconstruit byte-identique au donneur sur les 6**. L'ordre `</section></main></body>` est **imposé par l'imbrication**, pas choisi.

### 2. Six pages de district n'étaient jamais fermées
`distritos/{braganca, douro, guarda, tras-os-montes, vila-real, viseu}.html` se terminaient par `…</p>` puis **directement** `</html>`. Témoins `<body>` **1/0**, `<div>` **2/1** (l'`info-box` est fermée, la `cta` non). Le bloc CTA — **téléphone et WhatsApp** — est le dernier élément de la page. Complétion **déterminée par l'imbrication** : `</div>` puis `</body>`, aucune autre séquence n'est bien formée.

### 3. Bilan du balayage : 23 fichiers à problème sur 2 398
**17 libres, 12 traités.** Un seul fichier du dépôt est sans DOCTYPE et sans `<html lang>` : `contactos.html` — **pris par une PR ouverte**, et c'est **exactement** le défaut corrigé sur CU par la PR #273.

## ✅ Gate merge — aucun gate actif
Vérifié ce run : **aucune mention d'attente de merge**. Aucun gate réécrit. 4 PR étaient ouvertes ; la #315 a été ouverte quand même.

🔴 **Rappel de doctrine, à ne jamais réécrire** : R7 interdit de **MERGER**, pas de **PRODUIRE**. Entre le 06/08 et le 09/08, « Attente GO merge (R7) » a été relue chaque nuit comme un ordre d'arrêt → **4 runs sans production**. **Ne jamais réécrire un gate de ce type.**

## 🎯 FILE DE TÂCHES LOOP — état au 2026-08-23

| Rang | Cible | Statut |
|---|---|---|
| — | 6 blogs à bloc E-E-A-T absent + 6 `distritos/` non fermés | ✅ **traité ce run (#315)** |
| **1** | 🔴 **`eletricista-avaria-eletrica-amarante.html` — le prologue de document est TRIPLÉ** (`<html>` **3/1**, `<head>` **3/1**) | ⏳ **libre, aucun GO.** Trois ouvertures de document dans un seul fichier : à lire avant de trancher (concaténation de 3 rendus ? deux prologues parasites ?). **Le plus gros défaut structurel libre du repo.** |
| **2** | 🔴 **`public/blog/blog-problemas-eletricos-inverno.html` — `<h1>` 25/1** | ⏳ **libre.** ℹ️ **Le MÊME fichier porte le même défaut sur ENR (`<h1>` ×26)** — fichier jumeau, défaut jumeau. **Traiter les deux dans le même run.** |
| **3** | 🛑 **Arbitrer les 2 `sameAs` contradictoires** des 5 pages `fuga-corrente` (+ `aguas-vivas`) | 🛑 **GO d'une ligne.** Le groupe A rattache des pages d'électricité à **deux sites de plomberie** et omet `eletricista-urgente.pt`. Correctif mécanique une fois le groupe de référence désigné. |
| **4** | **`eletricista-urgente-alijo.html`** (`<html>` 2/1, `<head>` 2/1, `<section>` 6/5) et **`eletricista-urgente-penedono.html`** (`<section>` 6/5) | ⏳ **libres.** Même famille `<section>` 6/5 que 3 pages **prises par des PR** (`miranda-do-douro`, `mirandela`, `alfandega-da-fe`) → traiter les 2 libres, rouvrir les 3 après merge. |
| **5** | **`eletricista-disjuntor-disparar-braganca.html`** — `<h1>` multiples | ⏳ libre |
| **6** | **`comparacao.html`** — 3 doublons JSON-LD + `<main>` 1/0, `<section>` 1/0 | ⏸ **pris par une PR ouverte.** CU en avait 2 copies (corrigé, #271 mergée), ENR 3. Méthode CU #271 dès libération. |
| **7** | **`eletricista-aguas-vivas.html`** — 3 doublons JSON-LD, `<style>` 2/3 | ⏸ **pris par une PR ouverte.** Méthode #314. |
| **8** | **`contactos.html`** — ni DOCTYPE ni `<html lang>` | ⏸ **pris par une PR ouverte.** **Correctif déjà écrit et prouvé sur CU (#273)** : transplanter le prologue d'un jumeau, vérifier l'égalité byte-à-byte. Aucun GO. |
| **9** | **Le reste du sweep `LECONS.md`** | ⏳ sans GO. 771 lignes, 10 motifs couverts le 21/08. |
| **10** | **Corruption `repar`→`arranj` — 30 occurrences / 20 fichiers sur EU** | ⏳ **GO périmètre.** Les 5 `href` corrompus (`/arranjacao-avarias-eletricas`) **n'ont de cible sous aucune des deux formes** → liens morts antérieurs au batch, à traiter séparément. |
| **11** | **`Você` — 22 occurrences / 16 fichiers** | 🛑 corpus INTERDIT, GO requis. ℹ️ **Chercher les doublons d'abord.** |
| **12** | Statistiques non sourcées — commencer par la contradiction `30%` vs `40% dos incêndios domésticos` | ⏳ **2 + 5 fichiers, aucune décision d'offre : c'est une erreur factuelle.** Sans GO. |
| 13 | Chercher sur EU les défauts trouvés sur CU : `Fazem orçamento sem compromisso?` → `gratuito`, signature `<td>` + `&lt;` | ⏳ sans GO |
| 14 | **Si GO (b2′)** : les 221 fichiers restants de `Tempo de resposta?` | 🛑 **patch déjà écrit et en revue (PR #311)** |
| 15 | **Si GO (g)** : les 22 `Sem custo extra de fim de semana` | 🛑 GO |
| 16 | Arbitrer le doublon `public/` ↔ racine, conjointement avec CU | ⏸ |

## Tâche suivante recommandée
1. **Rang 1 — le prologue triplé d'`amarante`.** Libre, aucun GO, et c'est le défaut structurel le plus grave qui reste.
2. **Rang 2 — les `<h1>` ×25**, **en binôme avec ENR** : même fichier, même défaut, un seul run pour les deux.
3. **Rang 4 — `alijo` et `penedono`**, la famille `<section>` 6/5.
4. **Rang 12 — la contradiction `30%` vs `40%`** : erreur factuelle, 7 fichiers, aucun GO.
5. **Rang 8 dès libération** — le correctif est déjà écrit et prouvé sur CU (#273).
6. **Rappel d'une ligne** : les batches 221 / 22 / 960 / 842 restent en attente de GO périmètre, et le `sameAs` attend un GO d'une ligne.

## Apprentissages (self-improving)
- 🔴 **NOUVEAU — une balise ouvrante sans contenu ni fermeture, c'est un BLOC MANQUANT, pas une erreur de syntaxe.** Le compteur disait `<section> 1/0` ; la réalité était que **le bloc E-E-A-T entier et ses 5 liens internes avaient disparu de 6 pages**. Aucun audit de maillage ne le voyait — **les liens n'étaient pas cassés, ils n'existaient plus**. ➡️ **Traiter tout `<tag> n/n-1` comme une alerte de contenu manquant, et regarder ce qu'il y a ENTRE l'ouverture et la fermeture attendue. Ici : rien.**
- 🔴 **NOUVEAU — quand un bloc est du gabarit, la POPULATION le prouve, et la transplantation devient exacte.** 42/42 pour la balise ouvrante, 36/36 pour le contenu, une seule variante md5 : ce n'est plus « un jumeau plausible », c'est **le** contenu. ➡️ **Compter les variantes avant de transplanter. Une seule variante = restauration prouvable ; deux = arbitrage.**
- 🔴 **NOUVEAU — certaines fermetures ne sont pas un choix : l'imbrication les impose.** Sur `distritos/`, `<div>` et `<body>` ouverts, `</html>` déjà là, **rien entre les deux** → `</div></body>` est la seule séquence bien formée. À l'inverse, sur `vimioso` (CU) trois invariants de jumeaux convergeaient et le point de fermeture restait **indéterminé**. ➡️ **Distinguer « la seule complétion valide » de « la complétion la plus probable ». La première se pose, la seconde se consigne.**
- 🔴 **NOUVEAU — le même fichier porte le même défaut sur deux repos** (`blog-problemas-eletricos-inverno.html` : `<h1>` ×25 ici, ×26 sur ENR). ➡️ **Quand un défaut sort sur un repo, le chercher par NOM DE FICHIER sur les trois autres.** Une commande, rendement doublé.
- 🔴 **NOUVEAU — le balayage structurel est productif sur les 4 repos** : CNR 13 pages à CTA morts, ENR 3 pages au corps avalé, CU la seule page en mode quirks, EU 12 fichiers dont 6 blocs de contenu disparus. ➡️ **En faire une ÉTAPE FIXE du loop, avant de dérouler la file de tâches.** Équilibre des balises + `<h1>` multiples + validité JSON-LD + doublons byte-à-byte + DOCTYPE + `<html lang>`.
- 🔴 **NOUVEAU (leçon CNR de ce run) — « valeur non sourçable » se PROUVE en remontant la chaîne de définition.** Un rang y est resté bloqué un run entier pour un motif faux. **Distinguer « aucune source » de « source pas encore cherchée ».**
- 🔴 **Un doublon apparent peut n'être un doublon que sur un bloc.** 4 blocs répétés, **1 seul identique**. ➡️ **Hacher chaque bloc avant de conclure**, jamais se fier à la répétition des `@type`.
- 🔴 **Un doublon byte-à-byte est le seul retrait qui se prouve sans arbitrage.** **md5 identique → je retire ; md5 différent → je documente et je laisse.**
- 🔴 **Passer le contrôle sur la famille entière coûte une commande et ferme le sujet.**
- 🔴 **Le `</style>` orphelin était le MARQUEUR, pas le défaut** : une frontière de concaténation. ⚠️ **La chaîne de génération a maintenant produit SIX familles de défauts distinctes sur les 4 repos** : marqueurs `##style##`, corps de page dupliqués, JSON-LD tronqué écrasant un `<style>` (ENR), JSX non compilé (CNR), prologue de document absent (CU) ou triplé (EU, rang 1), bloc de contenu ouvert puis abandonné (EU). **Un audit du générateur rapporterait plus que la somme des correctifs.**
- 🔴 **Un compteur de balises ÉQUILIBRÉ peut signaler une duplication, pas une santé.** Compter les balises **uniques** par document (`<h1>`, `<header>`, `<main>`), pas seulement leur équilibre.
- 🔴 **Une PR qui répare un fichier ne répare pas sa famille.**
- 🔴 **Le contrôle de balises trouve mieux que le parseur JSON**, 4 runs de suite. **Passe systématique**, accompagnée du **grep des délimiteurs non résolus** qui trouve ce qui lui manque.
- 🔴 **Un titre de PR ne dit pas ce que la PR couvre.** **5ᵉ run consécutif** que `gh pr view <n> --json files` évite un conflit.
- 🔴 **La signature d'une corruption de batch, c'est le MOT INEXISTANT.**
- 🔴 **Quand un défaut RÉCIDIVE, chercher le GÉNÉRATEUR, pas la page.**
- 🔴 **Un fix de conformité sur 1 site n'élimine PAS la contamination sur les sites symétriques.**
- 🔴 **Le compteur R12 sur-compte** : R145 **autorise** `24h/7 dias`.
- **Ne pas sur-purger.** R4 se viole dans les deux sens.

## Edge cases détectés
- **`gh` et les credentials Git n'existent QUE sur le host macOS.** Sandbox : `git fetch` OK, **`git push` impossible**. ⚠️ **Depuis le sandbox, `git fetch` sur EU affiche `gh auth git-credential store: not found` — c'est bénin** (dépôt public, le fetch aboutit), mais **ne pas le confondre avec un échec**. **Répartition** : lecture / grep / parsing Python / **écriture de fichiers** → sandbox ; `git` en écriture / `gh` → `mcp__desktop-commander__start_process`.
- **Le `/tmp` du sandbox ≠ le `/tmp` du host.** Worktrees **et** `--body-file` de PR sous `~/work/Sites/_worktrees/`.
- 🔴 **Un worktree n'est PAS un dépôt git vu depuis le sandbox** : `git show`/`diff`/`log` y rendent des **compteurs à zéro** trompeurs. ➡️ **Tout témoin se compte en Python sur le CONTENU des fichiers.**
- 🔴 **`main` peut avancer PENDANT le run** (la #271 de CU a été mergée entre l'ouverture de la PR et la mise à jour du `context.md`). Le `git push` de l'étape 6 est alors rejeté en non-fast-forward. ➡️ **`git fetch` puis `git rebase <remote>/main` sur le commit de contexte — jamais `--force` (R6).**
- 🔴 **L'anchor d'insertion sur les concelhos EU est `</script>\n <style>`** (avec espace), contrairement à `</script>\n\n<style>` ailleurs — vérifier la convention locale avant de patcher.
- 🔴 **Le filtre sandbox qui mute `https://schema.org` à l'affichage est COSMÉTIQUE** — mais `https://***` réellement sur disque est un vrai défaut.
- ⚠️ **Un script Python qui accumule des exemples peut faire exploser la sortie** (196 000 caractères sur ENR ce run, résultat tronqué et inutilisable). **Borner explicitement ce qu'on imprime** en balayant des milliers de fichiers.
- 🔴 **`grep -P` n'existe pas sur macOS** ; **zsh ne fait pas de word-splitting**. Pour tout motif non trivial : **Python**.
- 🔴 **`git commit -m` multiligne est fragile en zsh** → `git commit -F -`. Corps de PR : `--body-file`.
- **Worktree obligatoire** (R-WT). **Jamais `reset --hard` / `checkout -- .` / `stash` / `clean`** sur le checkout partagé. Vérifié ce run : checkout partagé sur `main` avec plus de 1 300 fichiers non commités — **non touché**.

## Blocages connus
1. 🛑 **Arbitrage `sameAs` sur les 5 pages `fuga-corrente` (+ `aguas-vivas`)** : deux blocs `LocalBusiness`/`Service` contradictoires servis simultanément, l'un rattachant des pages d'électricité à des sites de plomberie. **GO d'une ligne.** Inchangé ce run.
2. ⏸ **`comparacao.html`, `eletricista-aguas-vivas.html`, `contactos.html` et 3 pages `<section>` 6/5** — bloqués par des **PR ouvertes**, pas par un arbitrage. Pour `contactos.html`, **le correctif est déjà écrit et prouvé sur CU (#273)**.
3. 🛑 **GO périmètre — corruption `repar`→`arranj` sans limite de mot** : **523 occurrences / 258 fichiers** sur les 4 repos (EU 30/20). La partie « liens » est livrée sur CNR (#323) et ENR (#363). Le blocage porte sur `Parranjo`→`Preparação`. **Un GO d'une ligne débloque les 523.**
4. 🛑 **`Você` — ~180 occurrences / ~157 fichiers sur les 4 repos** (EU 22/16). Corpus INTERDIT `LECONS.md`. GO requis.
5. 🛑 **Batches en attente de GO** : 221 (`Tempo de resposta?`, patch déjà écrit en PR #311) · 22 (`Sem custo extra de fim de semana`) · 960 · 842.
6. ⚠️ **`/arranjacao-avarias-eletricas` — 5 occurrences, aucune cible sous aucune des deux formes.** Lien mort **antérieur** au batch.
7. ⚠️ **Aucune des SIX familles de défauts de génération n'a de cause racine identifiée.** **La chaîne de génération de pages statiques mérite un audit dédié — c'est le point de levier le plus élevé des 4 repos.**
