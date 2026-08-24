# context.md — Loop State

> Écrit par le loop Cowork après chaque run. NE PAS ÉDITER MANUELLEMENT.

## Dernier run
- Date : 2026-08-24
- Tâche prévue : rang 1 — le prologue triplé d'`amarante`.
- Tâche réellement exécutée : **la tâche prévue, plus le rang 4** (famille `<section>` 6/5) sur les fichiers libres.
- **1 PR ouverte** :
  - **#316** — https://github.com/taffrand-gif/eletricista-urgente/pull/316 — branche `loop/2026-08-24-eu-structure2` — 4 commits, **3 fichiers de production** + `SEO_PLAN.md`
- ✅ **#315 a mergé** (les 6 blocs E-E-A-T et les 6 pages de district sont en production).

### 1. 🔴 La page `amarante` était NOINDEX en production
Le compteur `<html> 3/1` **sous-décrivait le défaut d'un ordre de grandeur**. Le fichier porte `<!DOCTYPE>`/`<html>`/`<head>` **trois fois** ; le parseur **ignore les 2ᵉ et 3ᵉ ouvertures et fusionne tous les `<meta>` dans un seul `<head>`**. Ce qui était servi :

```
<meta name="robots" content="index, follow">     ← 1er render
<meta name="robots" content="noindex,follow">    ← 2e render (périmé)
<meta name="robots" content="noindex,follow">    ← 3e render (périmé)
```

**Google retient la directive la plus restrictive : la money page était désindexée.** Elle servait aussi **trois `<title>`**.

**Témoin d'unanimité, deux niveaux** : (i) sur **2 398** fichiers HTML, `amarante` est le **seul** à porter plusieurs `<meta robots>` ; (ii) dans sa famille `eletricista-avaria-eletrica-*` (77 pages), **37/37** des pages qui déclarent `robots` écrivent exactement `index, follow`, **zéro `noindex`**.

**Méthode de retrait** : ne retirer que les balises dont la **clé** (`name`/`property`/`charset`/`rel`) est **déjà présente** dans le prologue conservé ; s'arrêter au premier `<script>`/`<style>` ou à la première clé inédite. Contrôle : **0 balise retirée sans équivalent conservé**. **Preuve finale** : le `<head>` reconstruit est **byte-identique (hors espaces) à celui du frère de gabarit `cambres`**, aux deux seules phrases propres à la page près.

### 2. La famille `<section>` 6/5 — la profondeur tranche là où le compteur ne dit rien
`alijo` (qui portait **aussi** le prologue dupliqué) et `penedono` : les deux `<section class="unique-urg-*">` étaient **imbriquées** au lieu d'être sœurs. Sur les **152** pages portant `unique-urg-*`, **147 les ouvrent à profondeur `section` = 1** ; **les 5 exceptions sont exactement les pages cassées.**

### 3. ⚠️ 🔴 Incident de méthode — un faux négatif SILENCIEUX du contrôle de réservation
`eletricista-aguas-vivas.html` et `eletricista-urgente-alfandega-da-fe.html` ont été **patchés puis restaurés**.

Cause : `gh pr view … > /tmp/eu_prfiles.txt` s'exécute sur le **host** ; le `grep` de contrôle avait été lancé depuis le **sandbox**, dont le `/tmp` est un autre système de fichiers. **Le grep n'a rien trouvé parce que le fichier n'existait pas — et il n'a produit aucune erreur.**

Recontrôlé depuis le host : `aguas-vivas` est pris par la **PR #308**, `alfandega-da-fe` par la **PR #311**. Restaurés via `git checkout -- <chemins nommés>` (jamais `-- .`), **avant tout commit**. **Périmètre final : 3 fichiers, pas 5.**

## ✅ Gate merge — aucun gate actif
Vérifié ce run : **aucune mention d'attente de merge**. Aucun gate réécrit. 4 PR étaient ouvertes ; la #316 a été ouverte quand même.

🔴 **Rappel de doctrine, à ne jamais réécrire** : R7 interdit de **MERGER**, pas de **PRODUIRE**. Entre le 06/08 et le 09/08, « Attente GO merge (R7) » a été relue chaque nuit comme un ordre d'arrêt → **4 runs sans production**. **Ne jamais réécrire un gate de ce type.**

## 🎯 FILE DE TÂCHES LOOP — état au 2026-08-24

| Rang | Cible | Statut |
|---|---|---|
| — | `amarante` (prologue ×3, page noindex) · `alijo` · `penedono` | ✅ **traité ce run (#316)** |
| **1** | 🔴 **`public/blog/blog-problemas-eletricos-inverno.html` — `<h1>` 25/1** | ⏳ **libre, aucun GO. Le plus gros défaut restant du repo.** ℹ️ **Le MÊME fichier porte le même défaut sur ENR (`<h1>` ×26), mais y est pris par une PR ouverte.** Traiter ici d'abord ; rouvrir ENR dès libération. ⚠️ Passer d'abord le contrôle de bloc dupliqué : 25 `<h1>` = soit une duplication massive du corps, soit des `<h1>` employés en sous-titres — **deux défauts très différents**. |
| **2** | 🔴 **`eletricista-disjuntor-disparar-braganca.html` — `<h1>` multiples** | ⏳ **libre.** Même contrôle préalable que le rang 1. |
| **3** | 🛑 **Arbitrer les 2 `sameAs` contradictoires** des 5 pages `fuga-corrente` (+ `aguas-vivas`) | 🛑 **GO d'une ligne.** Le groupe A rattache des pages d'électricité à **deux sites de plomberie** et omet `eletricista-urgente.pt`. Correctif mécanique une fois le groupe de référence désigné. |
| **4** | **Les 3 pages restantes de la famille `<section>` 6/5** : `miranda-do-douro` et `alfandega-da-fe` (**PR #311**), `mirandela` (**PR #313**) | ⏸ **correctif identique à #316, prouvé, aucun GO.** Rouvrir dès merge. **Invariant à réappliquer : profondeur `section` = 1 pour `unique-urg-*` (147/152).** |
| **5** | **`eletricista-aguas-vivas.html`** — prologue dupliqué + `<style>` 2/3 + `<nav>` 2/3 + 3 doublons JSON-LD | ⏸ **pris par la PR #308.** Le correctif de prologue est **déjà écrit et prouvé** (#316) ; le `<style>`/`<nav>` 2/3 (fermetures en trop) est une **autre famille**. |
| **6** | **`contactos.html`** — ni DOCTYPE ni `<html lang>` | ⏸ **pris par une PR ouverte.** **Correctif déjà écrit et prouvé sur CU (#273, mergée)** : transplanter le prologue d'un jumeau, vérifier l'égalité byte-à-byte. Aucun GO. |
| **7** | **`comparacao.html`** — 3 doublons JSON-LD + `<main>` 1/0, `<section>` 1/0 | ⏸ **pris par une PR ouverte.** Méthode CU #271 dès libération. |
| **8** | **Le reste du sweep `LECONS.md`** | ⏳ sans GO. 771 lignes, 10 motifs couverts le 21/08. 💡 **Sur CU ce run, le sweep a sorti 27 nœuds JSON-LD non typés que rien d'autre ne voyait** — voir Apprentissages, **le contrôle `@type` est à passer ici aussi**. |
| **9** | **Corruption `repar`→`arranj` — 30 occurrences / 20 fichiers** | ⏳ **GO périmètre.** Les 5 `href` corrompus (`/arranjacao-avarias-eletricas`) **n'ont de cible sous aucune des deux formes** → liens morts antérieurs au batch, à traiter séparément. |
| **10** | **`Você` — 22 occurrences / 16 fichiers** | 🛑 corpus INTERDIT, GO requis. ℹ️ **Chercher les doublons d'abord.** |
| **11** | Statistiques non sourcées — commencer par la contradiction `30%` vs `40% dos incêndios domésticos` | ⏳ **2 + 5 fichiers, aucune décision d'offre : c'est une erreur factuelle.** Sans GO. |
| 12 | Chercher sur EU les défauts trouvés sur CU : `Fazem orçamento sem compromisso?` → `gratuito`, signature `<td>` + `&lt;`, **et les meta descriptions à phrase dupliquée** (10 trouvées sur CU) | ⏳ sans GO |
| 13 | **Si GO (b2′)** : les 221 fichiers restants de `Tempo de resposta?` | 🛑 **patch déjà écrit et en revue (PR #311)** |
| 14 | **Si GO (g)** : les 22 `Sem custo extra de fim de semana` | 🛑 GO. ℹ️ **Sur CU, les 76 occurrences de ce motif étaient TOUTES dans `_archive/`** — vérifier ici avant de dépenser l'arbitrage. |
| 15 | Arbitrer le doublon `public/` ↔ racine, conjointement avec CU | ⏸ |

## Tâche suivante recommandée
1. **Rang 1 — les `<h1>` ×25 de `blog-problemas-eletricos-inverno.html`.** Libre, aucun GO, plus gros défaut restant. **Contrôle de bloc dupliqué AVANT de patcher.**
2. **Rang 2 — `disjuntor-disparar-braganca`**, même famille, même contrôle préalable.
3. **Ajouter le contrôle `@type` au balayage structurel** et le repasser une fois à ce titre (voir Apprentissages — sur CU il a sorti 27 nœuds non typés dans du JSON parfaitement valide).
4. **Rang 11 — la contradiction `30%` vs `40%`** : erreur factuelle, 7 fichiers, aucun GO.
5. **Rangs 4, 5, 6, 7 dès merge** — tous les correctifs sont déjà écrits et prouvés.
6. **Poser en une ligne** le GO `sameAs` (rang 3).

## Apprentissages (self-improving)
- 🔴 **NOUVEAU — un compteur de balises peut sous-décrire le défaut d'un ordre de grandeur.** `<html> 3/1` sonne comme une coquetterie de validation ; la réalité était **une money page désindexée**. ➡️ **Quand un prologue de document est dupliqué, ne pas compter les balises : LISTER les `<meta robots>` et les `<title>` effectivement servis.** Le parseur fusionne, et c'est la fusion qui décide.
- 🔴 **NOUVEAU — le retrait d'un doublon devient prouvable quand on le fait par CLÉ, pas par bloc.** Ne retirer que les balises dont la clé est déjà présente, s'arrêter à la première clé inédite ou au premier `<script>` : le contrôle « **0 balise retirée sans équivalent conservé** » remplace le jugement. Et la vérification finale — `<head>` byte-identique au frère de gabarit — transforme la restauration en fait. **Ce prédicat est réutilisable sur tous les prologues dupliqués des 4 repos.**
- 🔴 **NOUVEAU — un `grep` qui ne trouve rien parce que son FICHIER D'ENTRÉE n'existe pas ne produit aucune erreur.** Le `/tmp` du sandbox n'est pas celui du host : le contrôle de réservation a rendu un faux négatif silencieux et **2 fichiers réservés ont été patchés** (rattrapé avant commit). ➡️ **Tout contrôle s'exécute là où vit son fichier d'entrée**, et **un contrôle qui rend 0 doit d'abord prouver que sa source est non vide** (`wc -l` sur l'entrée). **C'est le pendant exact de la leçon « un worktree n'est pas un dépôt git vu depuis le sandbox » : un résultat vide n'est pas un résultat tant que la source n'est pas prouvée.**
- 🔴 **NOUVEAU — restaurer un fichier patché à tort se fait sur des CHEMINS NOMMÉS**, jamais sur `.`, même dans un worktree dédié. R-WT ne se relâche pas parce que le répertoire est à nous.
- 🔴 **NOUVEAU (leçon CU de ce run) — validité JSON ≠ validité schema.org.** 27 nœuds y passaient `json.loads` en écrivant `"type"` au lieu de `"@type"` : JSON valide, donnée structurée nulle. ➡️ **Ajouter au balayage structurel : tout objet d'un bloc `ld+json` doit porter `@type`.** À passer sur EU.
- 🔴 **La profondeur d'imbrication est un invariant mesurable, et il tranche là où le compteur ne dit rien.** 147/152 pour `unique-urg-*` ici ; 279/279 pour `<div class="content">` sur ENR le même run. **Mesurer la profondeur aux points de repère, pas seulement les totaux.**
- 🔴 **Une balise ouvrante sans contenu ni fermeture, c'est un BLOC MANQUANT, pas une erreur de syntaxe.** Traiter tout `<tag> n/n-1` comme une alerte de **contenu manquant**, et regarder ce qu'il y a **entre** l'ouverture et la fermeture attendue.
- 🔴 **Quand un bloc est du gabarit, la POPULATION le prouve, et la transplantation devient exacte.** **Compter les variantes avant de transplanter. Une seule variante = restauration prouvable ; deux = arbitrage.**
- 🔴 **Certaines fermetures ne sont pas un choix : l'imbrication les impose.** **Distinguer « la seule complétion valide » de « la complétion la plus probable ». La première se pose, la seconde se consigne.**
- 🔴 **Le même fichier porte le même défaut sur deux repos** (`blog-problemas-eletricos-inverno.html`). ➡️ **Quand un défaut sort sur un repo, le chercher par NOM DE FICHIER sur les trois autres.**
- 🔴 **Le balayage structurel est productif sur les 4 repos.** ➡️ **Étape FIXE du loop, avant de dérouler la file** : équilibre des balises + **profondeur aux points de repère** + `<h1>` multiples + validité JSON-LD + **présence de `@type`** + doublons byte-à-byte + DOCTYPE + `<html lang>` + **unicité des `<meta robots>` et des `<title>`**.
- 🔴 **Le contrôle des PR ouvertes se fait AVANT de calculer le périmètre** — et **son résultat doit être vérifié**, cf. l'incident ci-dessus. **6ᵉ run consécutif qu'il évite un conflit.**
- 🔴 **Un doublon apparent peut n'être un doublon que sur un bloc.** **Hacher chaque bloc avant de conclure.**
- 🔴 **Un doublon byte-à-byte est le seul retrait qui se prouve sans arbitrage.** md5 identique → je retire ; md5 différent → je documente et je laisse. ℹ️ **Exception établie ce run** : un doublon **par clé de balise** se prouve aussi, parce que la clé identifie l'équivalent conservé.
- 🔴 **« Valeur non sourçable » se PROUVE en remontant la chaîne de définition.** Distinguer « aucune source » de « source pas encore cherchée ».
- 🔴 **Un défaut DÉJÀ RÉPARÉ qui revient est un générateur non corrigé** (leçon ENR #371) : `git log -S <motif>` avant de patcher.
- 🔴 **`_archive/` fausse tous les compteurs** (leçon CU) : l'exclure de tout compteur de conformité et le dire dans le rapport.
- **Ne pas sur-purger.** R4 se viole dans les deux sens : inventer **et** effacer ce qui est vrai.

## Edge cases détectés
- 🔴 **Le checkout partagé d'EU est SUR `main`.** `git worktree add … -B main` échoue (« 'main' is already used by worktree »). ➡️ **Créer le worktree de `context.md` en `--detach` sur `origin/main` et pousser `HEAD:main`.** Ne jamais tenter de récupérer la branche `main` du checkout partagé (R-WT).
- **Ce repo n'a QU'UN remote : `origin`.**
- 🔴 **Le `/tmp` du sandbox ≠ le `/tmp` du host.** Vaut pour les `--body-file` de PR **et pour tout fichier intermédiaire de contrôle**. Écrire sous `~/work/Sites/_worktrees/` (monté des deux côtés), et **supprimer le `PR_BODY.md` après le `gh pr create`**.
- **`gh` et les credentials Git n'existent QUE sur le host macOS.** Répartition : lecture / grep / parsing Python / **écriture de fichiers** → sandbox `mcp__workspace__bash` ; `git` en écriture / `gh` → `mcp__desktop-commander__start_process`.
- 🔴 **Un worktree n'est PAS un dépôt git vu depuis le sandbox** : `git show`/`diff`/`log` y rendent des **compteurs à zéro** trompeurs. ➡️ **Tout témoin se compte en Python sur le CONTENU des fichiers.**
- ⚠️ **Borner explicitement ce qu'on imprime** en balayant ~2 400 fichiers.
- 🔴 **`grep -P` n'existe pas sur macOS** ; **`grep -E` de macOS ne matche pas de façon fiable les accents** ; **`grep -c '***'` échoue en zsh**. **Pour tout motif accentué ou non trivial : Python.**
- 🔴 **Une f-string Python ne peut pas contenir de backslash dans son expression** — sortir les regex en constantes avant de les interpoler, ou utiliser `%`.
- 🔴 **`git commit -m` multiligne est fragile en zsh** → `printf … | git commit -F -`. **ASCII dans les messages de commit**, UTF-8 dans les fichiers. Corps de PR : `--body-file`, jamais `--body` inline.
- **Worktree obligatoire** (R-WT). **Jamais `reset --hard` / `checkout -- .` / `stash` / `clean`** sur le checkout partagé. Aucun `context.md` ne *prescrit* de `reset --hard`.

## Blocages connus
1. 🛑 **GO d'une ligne — les 2 `sameAs` contradictoires** des pages `fuga-corrente` : des pages d'électricité rattachées à deux sites de plomberie, `eletricista-urgente.pt` omis.
2. ⏸ **Rangs 4, 5, 6 et 7 pris par des PR ouvertes** — pas des blocages de fond, des attentes de merge. **Tous les correctifs sont déjà écrits et prouvés.** **Les rangs 1 et 2 sont libres : y aller.**
3. 🛑 **GO périmètre — corruption `repar`→`arranj`** : 30 occ / 20 fichiers ici, 523 sur les 4 repos.
4. 🛑 **`Você`** — corpus INTERDIT, GO requis. **Chercher les doublons d'abord.**
5. 🛑 **Batches en attente de GO** : 221 (`Tempo de resposta?`), 22 (`Sem custo extra de fim de semana` — **vérifier d'abord s'ils sont en production ou en archive**), 960, 842.
6. ⚠️ **La chaîne de génération de pages statiques reste non auditée.** Familles imputables sur les 4 repos : marqueurs `##style##`, corps de page dupliqués, JSON-LD tronqué écrasant un `<style>`, JSX non compilé, prologue absent (CU), mutation `@context` (ENR + CU), **et désormais prologue TRIPLÉ avec `robots` contradictoires (EU)**. **Sept familles, une chaîne. C'est le point de levier le plus élevé des 4 repos.**
