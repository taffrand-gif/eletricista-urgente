# context.md — Loop State

> Écrit par le loop Cowork après chaque run. NE PAS ÉDITER MANUELLEMENT.

## Dernier run
- Date : 2026-08-22
- Tâche prévue : rang 1 de la file du 21/08 — `</style>` orphelin + `BreadcrumbList` JSON-LD dupliqué.
- Tâche réellement exécutée : **la tâche prévue**, avec le contrôle passé sur **la famille entière (79 fichiers)** et non sur les 6 pages annoncées.
- **1 PR ouverte** :
  - **#314** — https://github.com/taffrand-gif/eletricista-urgente/pull/314 — branche `loop/2026-08-22-eu-jsonld-duplique` — 6 commits, 5 fichiers de production + `SEO_PLAN.md`

### 1. Les 5 pages à `</style>` orphelin + `BreadcrumbList` dupliqué (PR #314)
Structure identique sur les 5 : un **`</style>` sans ouverture** sépare **deux groupes de 4 blocs JSON-LD** (`BreadcrumbList`, `FAQPage`, `Service`, `LocalBusiness`).

🔎 **Le doublon n'est que PARTIEL — le `context.md` du 21/08 le décrivait comme total.** Seul le `BreadcrumbList` du second groupe est un doublon **byte-à-byte** du premier (même md5). **Les 3 autres paires DIVERGENT.** Supprimer « le second groupe » en bloc, ce que la formulation précédente suggérait, aurait détruit 3 blocs porteurs de données différentes.

Retiré : le `</style>` orphelin + le seul `BreadcrumbList` md5-identique. Conservé : les 8 autres blocs.

- **Témoins R8, identiques sur les 5** (avant mesuré sur `origin/main` intact) : `<style>` **2/3 → 2/2** · blocs JSON-LD **10 → 9** · doublons md5 **1 → 0** · JSON invalides **0 → 0** · `<script>` 12/12, `<div>` 15/15, `<html>`/`<head>`/`<body>` 1/1 **inchangés**. Volume : −392 à −424 octets par fichier.

### 2. La famille entière contrôlée — et le compteur du 21/08 est confirmé exact
Contrôle passé sur les **78 `eletricista-fuga-corrente-*` + `eletricista-aguas-vivas.html`** (leçon « une PR qui répare un fichier ne répare pas sa famille »). Résultat : **6 anormales sur 79**, exactement celles annoncées. **La famille est close.**

⚠️ **`eletricista-aguas-vivas.html` EXCLUE : prise par une PR ouverte** (contrôle sur les 149 fichiers des PR #313, #311, #308, #307). Elle porte le même défaut en pire — **3 blocs dupliqués** au lieu d'1. À reprendre après merge.

### 3. 🛑 Découverte — deux `sameAs` CONTRADICTOIRES servis simultanément aux crawlers
Sur les 5 pages, les paires conservées divergent, et pas cosmétiquement :
```
LocalBusiness.sameAs
  groupe A : ["canalizador-norte-reparos.pt", "eletricista-norte-reparos.pt", "canalizador-urgente.pt"]
  groupe B : ["eletricista-norte-reparos.pt", "eletricista-urgente.pt"]
```
Le **groupe A rattache une page d'électricité à deux sites de PLOMBERIE** et omet `eletricista-urgente.pt`, c'est-à-dire le site sur lequel la page se trouve. Le groupe B paraît correct — mais « paraît » n'est pas une source. `Service.provider.sameAs` porte la même contradiction, et `FAQPage` diverge sur le texte des réponses.
**Choisir lequel fait foi est un arbitrage, pas un correctif** : les deux blocs sont syntaxiquement valides et aucun document verrouillé ne tranche. Non touché (R4). **Un GO d'une ligne — « le groupe qui suit l'orphelin fait foi » — clôt les 5 pages, et probablement `aguas-vivas` avec.**

## ✅ Gate merge — aucun gate actif
Vérifié ce run : **aucune mention d'attente de merge** dans les 4 `context.md`. Aucun gate réécrit.

🔴 **Rappel de doctrine, à ne jamais réécrire** : R7 interdit de **MERGER**, pas de **PRODUIRE**. Une PR en attente ne gèle pas le repo. Entre le 06/08 et le 09/08, la mention « Attente GO merge (R7) » a été relue chaque nuit comme un ordre d'arrêt → **4 runs sans production**. **Ne jamais réécrire un gate de ce type.**
ℹ️ Confirmation de terrain ce run : **la PR #271 de CU a été mergée dans l'heure suivant son ouverture.** Produire n'attend rien.

## 🎯 FILE DE TÂCHES LOOP — état au 2026-08-22

| Rang | Cible | Statut |
|---|---|---|
| — | 5 pages `fuga-corrente` : `</style>` orphelin + `BreadcrumbList` dupliqué | ✅ **traité ce run (#314)** — famille de 79 close |
| **1** | 🛑 **Arbitrer les 2 `sameAs` contradictoires** des 5 pages (+ `aguas-vivas`) | 🛑 **GO d'une ligne.** Le groupe A rattache des pages d'électricité à des sites de plomberie. Le correctif est mécanique une fois le groupe de référence désigné. |
| **2** | **`comparacao.html` — contrôler s'il porte des copies multiples du corps de page** | ⏳ **PROCHAINE TÂCHE SANS GO.** CU en avait **2** (corrigé, PR #271 mergée), ENR en a **3**, CNR **0**. **EU est le dernier angle mort de la famille.** ⚠️ Le fichier est **pris par une PR ouverte** — contrôler avant. Méthode CU #271 : hacher les copies, prouver l'absence de perte, supprimer la périmée. |
| **3** | **`eletricista-aguas-vivas.html`** — même défaut que les 5, **3 blocs dupliqués** | ⏸ **pris par une PR ouverte.** Reprendre dès son merge, méthode #314. |
| **4** | **Le reste du sweep `LECONS.md`** | ⏳ sans GO. `LECONS.md` fait 771 lignes ; le sweep du 21/08 en a couvert 10 motifs. |
| **5** | **Corruption `repar`→`arranj` — 30 occurrences / 20 fichiers sur EU** | ⏳ **GO périmètre.** Voir §Blocages n°1. Les 5 `href` corrompus (`/arranjacao-avarias-eletricas`) **n'ont de cible sous aucune des deux formes** → liens morts antérieurs au batch, à traiter séparément. |
| **6** | **`Você` — 22 occurrences / 16 fichiers** | 🛑 corpus INTERDIT, GO requis. ℹ️ **Chercher les doublons d'abord** : sur CU, 4 occurrences sont tombées ce run **sans consommer le GO**, parce qu'elles vivaient dans un bloc mort. |
| **7** | Statistiques non sourcées (h) — commencer par la contradiction `30%` vs `40% dos incêndios domésticos` | ⏳ **2 + 5 fichiers, aucune décision d'offre : c'est une erreur factuelle.** Sans GO. |
| **8** | Chercher sur EU les défauts trouvés sur CU : `Fazem orçamento sem compromisso?` → `gratuito` et la signature `<td>` + `&lt;` | ⏳ sans GO |
| **9** | **Si GO (b2′)** : les 221 fichiers restants de `Tempo de resposta?` | 🛑 **le patch est déjà écrit et en revue (PR #311)** |
| 10 | **Si GO (g)** : les 22 `Sem custo extra de fim de semana` | 🛑 GO |
| 11 | Arbitrer le doublon `public/` ↔ racine, conjointement avec CU | ⏸ |

## Tâche suivante recommandée
1. **Rang 2 — `comparacao.html`.** C'est le dernier angle mort d'une famille dont 3 repos sur 4 sont déjà mesurés, la méthode est validée et le résultat est prouvable. Contrôler la PR qui le prend avant de patcher.
2. **Rang 7 — la contradiction `30%` vs `40% dos incêndios domésticos`** : erreur factuelle, 7 fichiers, aucun GO.
3. **Rang 4 — continuer le sweep `LECONS.md`.**
4. **Rang 8** — sans GO.
5. **Rappel d'une ligne** : les batches 221 / 22 / 960 / 842 restent en attente de GO périmètre.

## Apprentissages (self-improving)
- 🔴 **NOUVEAU — un doublon apparent peut n'être un doublon que sur un bloc.** 4 blocs répétés, **1 seul identique**. Supprimer « le second groupe » aurait détruit 3 blocs de données différentes, dont un `sameAs` distinct. ➡️ **Hacher chaque bloc avant de conclure à une duplication**, jamais se fier à la répétition des `@type`.
- 🔴 **NOUVEAU — un doublon byte-à-byte est le seul retrait qui se prouve sans arbitrage.** C'est la ligne de partage utile entre corriger et escalader : **md5 identique → je retire ; md5 différent → je documente et je laisse.**
- 🔴 **NOUVEAU — passer le contrôle sur la famille entière coûte une commande et ferme le sujet.** 79 fichiers scannés, 6 anormaux, périmètre clos **et compteur du `context.md` vérifié** — au lieu de patcher 6 noms sur parole et de rouvrir le sujet au prochain run.
- 🔴 **NOUVEAU — le `</style>` orphelin était le MARQUEUR, pas le défaut.** Il signalait une frontière de concaténation : deux rendus du même gabarit collés bout à bout. Le vrai défaut est le **générateur qui concatène sans vérifier**. ➡️ **Même famille que le NAP parasite du 21/08 et que les copies multiples de `comparacao.html` (CU 2, ENR 3) trouvées ce run. Trois défauts de duplication distincts en deux runs : la chaîne de génération de pages statiques mérite un audit dédié.**
- 🔴 **NOUVEAU — un compteur de balises ÉQUILIBRÉ peut signaler une duplication, pas une santé** (leçon CU de ce run). `<header>` 2/2 et `<h1>` 2/2 étaient dupliqués, pas sains. ➡️ **Compter les balises uniques par document (`<h1>`, `<header>`, `<main>`), pas seulement leur équilibre.**
- 🔴 **Une PR qui répare un fichier ne répare pas sa famille.** Confirmé : la #312 avait corrigé 2 pages `fuga-corrente` ; **6 sœurs portaient le même défaut, dont celle qu'elle avait touchée**. Ce run les a toutes sorties et closes.
- 🔴 **Le contrôle de balises trouve mieux que le parseur JSON**, 3 runs de suite. **Le garder comme passe systématique** — et l'accompagner du **grep des délimiteurs non résolus**, qui trouve ce que lui manque (sur CNR et ENR ce run, des fichiers **équilibrés 2/2** portaient un marqueur `##endstyle##`).
- 🔴 **Un titre de PR ne dit pas ce que la PR couvre.** Sur ENR ce run, la #348 intitulée « supprime les promesses de délai (R145) » prend en fait `comparacao.html`. **4ᵉ run consécutif** que `gh pr view <n> --json files` évite un conflit.
- 🔴 **La signature d'une corruption de batch, c'est le MOT INEXISTANT.**
- 🔴 **Quand un défaut RÉCIDIVE, chercher le GÉNÉRATEUR, pas la page.**
- 🔴 **Un fix de conformité sur 1 site n'élimine PAS la contamination sur les sites symétriques.**
- 🔴 **Le compteur R12 sur-compte** : R145 **autorise** `24h/7 dias`.
- **Ne pas sur-purger.** R4 se viole dans les deux sens.

## Edge cases détectés
- **`gh` et les credentials Git n'existent QUE sur le host macOS.** Sandbox : `git fetch` OK, **`git push` impossible**. **Répartition** : lecture / grep / parsing Python / **écriture de fichiers** → sandbox ; `git` en écriture / `gh` → `mcp__desktop-commander__start_process`.
- **Le `/tmp` du sandbox ≠ le `/tmp` du host.** Worktrees sous `~/work/Sites/_worktrees/loop-YYYY-MM-DD/`.
- 🔴 **NOUVEAU — un worktree n'est PAS un dépôt git vu depuis le sandbox** : son `.git` est un fichier pointant vers un chemin macOS. `git show`/`git diff`/`git log` y **échouent** depuis `mcp__workspace__bash`, et un `python3` qui lit leur stdout renvoie des compteurs **à zéro** qui ressemblent à un résultat. ➡️ **Tout « avant » mesuré par git se prend depuis le host.**
- 🔴 **NOUVEAU — `main` peut avancer PENDANT le run** (la #271 de CU a été mergée entre l'ouverture de la PR et la mise à jour du `context.md`). Le `git push` de l'étape 6 est alors rejeté en non-fast-forward. ➡️ **`git fetch` puis `git rebase <remote>/main` sur le commit de contexte — jamais `--force` (R6).** Vérifier d'abord que `context.md` n'a pas bougé de son côté.
- 🔴 **L'anchor d'insertion sur les concelhos EU est `</script>\n <style>`** (avec espace), contrairement à `</script>\n\n<style>` ailleurs — vérifier la convention locale avant de patcher.
- 🔴 **Le filtre sandbox qui mute `https://schema.org` à l'affichage est COSMÉTIQUE** — le disque conserve la bonne valeur. **Mais `https://***` réellement présent sur disque est un vrai défaut.**
- 🔴 **`grep -P` n'existe pas sur macOS** ; **zsh ne fait pas de word-splitting**. Pour tout motif non trivial : **Python**.
- 🔴 **`git commit -m` multiligne est fragile en zsh** → `git commit -F -`. Corps de PR : `--body-file`.
- **Worktree obligatoire** (R-WT). **Jamais `reset --hard` / `checkout -- .` / `stash` / `clean`** sur le checkout partagé. Vérifié ce run : checkout partagé sur `main` avec **1380 fichiers non commités** — non touché.

## Blocages connus
1. 🛑 **NOUVEAU — arbitrage `sameAs` sur les 5 pages `fuga-corrente` (+ `aguas-vivas`)** : deux blocs `LocalBusiness`/`Service` contradictoires servis simultanément, l'un rattachant des pages d'électricité à des sites de plomberie. **GO d'une ligne.**
2. 🛑 **GO périmètre — corruption `repar`→`arranj` sans limite de mot** : **523 occurrences / 258 fichiers** sur les 4 repos (EU 30/20). La partie « liens » est livrée sur CNR (#323) et ENR (#363). Le blocage porte sur `Parranjo`→`Preparação` : restauration *probable* mais **pas prouvable par un fichier sur disque** → hors R4 sans arbitrage. **Un GO d'une ligne débloque les 523.**
3. 🛑 **`Você` — ~180 occurrences / ~157 fichiers sur les 4 repos** (EU 22/16). Corpus INTERDIT `LECONS.md`. GO requis. ℹ️ **Chercher les doublons avant de dépenser l'arbitrage.**
4. 🛑 **Batches en attente de GO** : 221 (`Tempo de resposta?`, patch déjà écrit en PR #311) · 22 (`Sem custo extra de fim de semana`) · 960 · 842.
5. ⏸ **`eletricista-aguas-vivas.html` et `comparacao.html`** — bloqués par des **PR ouvertes**, pas par un arbitrage.
6. ⚠️ **`/arranjacao-avarias-eletricas` — 5 occurrences, aucune cible sous aucune des deux formes.** Lien mort **antérieur** au batch.
7. ⚠️ **La cause racine du batch `repar`→`arranj` n'est pas identifiée**, et **celle des duplications de corps de page non plus**. **Audit dédié de la chaîne de génération de pages statiques recommandé.**
