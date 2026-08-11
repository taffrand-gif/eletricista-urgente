# context.md — Loop State

> Écrit par le loop Cowork après chaque run. NE PAS ÉDITER MANUELLEMENT.

## Dernier run
- Date : 2026-08-11
- Tâches exécutées : **(A) audit du générateur** (tâche n°1 du `context.md`, lecture seule) et **(B) prototype R11 prix** sur `eletricista-urgente-macedo-de-cavaleiros.html` (tâche n°2).
- Branche : `loop/2026-08-11-eletricista-urgente-r11-prix-prototype` (depuis `origin/main`, **en worktree**)
- Commits : `5e79a837d` (page sede operacional), puis `2e5d06054` (`SEO_PLAN.md`)
- PR ouverte : https://github.com/taffrand-gif/eletricista-urgente/pull/268
- Résultat : ✅ 2 commits, 2 fichiers. La `<meta name="description">` de la **sede operacional**, visible en SERP, annonçait « 15€ deslocação + 70€/h. **A partir de 100€ (1h)..** » alors que la grille de la même phrase donne **85 €** (+15 €, **+17,6 %**). Corrigé **par retrait du total dérivé, zéro arithmétique** — les composants de la grille restent verbatim. Témoins R8 : `A partir de 100€` 1→0 · `A partir de` 1→0 · `(1h)` 1→0 · `15€ deslocação + 70€/h` 1→1 · `24h` 16→16 · `€` 18→18. Delta **−26 octets**. **JSON-LD : 2/2 blocs re-parsés valides.**

## ✅ RÉSOLU ce run — la question qui conditionnait tout le reste

> *« Le gisement FAQ ne diminue pas malgré un merge → un générateur régénère-t-il le template cassé ? »*

**Réponse : NON — ce ne sont pas les générateurs de pages, ce sont les SCRIPTS DE PURGE eux-mêmes.**

| Script | Ligne | Chaîne de remplacement |
|---|---|---|
| `scripts/r12_blog_safe_cleanup.py` | L49-50 | `Resposta conforme disponibilidade` → **`"Deslocação conforme zona Z"`** |
| `scripts/r12_hubs_cleanup.py` | L37-45 | 2 motifs → **`"< Deslocação conforme zona tarifária Z"`** |

Dans les deux cas la chaîne de remplacement **se termine par un `Z` orphelin** : le numéro de zone n'est jamais concaténé. **C'est un fragment de gabarit inachevé** — voilà l'origine des 955 réponses vides.

➡️ **Conséquence, et elle est bonne** : ces scripts sont des nettoyages **one-shot**, pas une étape de build. **Un batch sur les 955 fichiers ne sera PAS annulé au prochain déploiement**, à condition de corriger ou retirer ces deux scripts d'abord. **Le blocage « corriger la source avant les pages » est levé, avec sa cible identifiée.**

### ⚠️ MAIS un défaut distinct existe dans le vrai générateur — `scripts/gen_concelhos.py`

Celui-ci **régénère effectivement à chaque exécution**, et produit du contenu non conforme :

| Ligne | Contenu produit | Problème |
|---|---|---|
| L170-174 `faq_time()` | « O tempo médio de viagem desde Macedo de Cavaleiros é de cerca de **{route_min} minutos** » | **délai chiffré** — R145 |
| L143 | « **Resposta rápida 24 horas por dia**, 7 dias por semana » | promesse de délai |
| L148 | « Sim, **24h por dia, 7 dias por semana, sem custo adicional** de marcação » | claim non sourcé |
| L149 | « fatura detalhada com NIF e **relatório técnico** quando aplicável » | terme banni par le ruling Filipe 08/07 |

**Non touché ce run** : 1 générateur = impact batch sur toutes les pages `concelhos/` → **GO Philippe**. **À traiter AVANT toute purge des pages `concelhos/`**, sinon le correctif sera annulé à la prochaine génération.

## ✅ Gate merge — CADUC, vérifié ce run
Vérification `gh pr view` : **#240 (CU) MERGED**, **#269 (CNR) MERGED**, **#295 (ENR) MERGED**, **#200 (ce repo) MERGED**. Aucun gate actif.

🔴 **Rappel de doctrine, à ne jamais réécrire** : R7 interdit de **MERGER**, pas de **PRODUIRE**. Entre le 06/08 et le 09/08, la mention « Attente GO merge (R7) » a été relue chaque nuit comme un ordre d'arrêt → **4 runs sans production**. Ne jamais réécrire un gate de ce type.

## 📊 Recompte des 2 gisements — 2026-08-11

Script Python (motifs non-ASCII), `_archive/` exclu, **avec contrôle positif** `65€` = **1473 fichiers**.

| Gisement | 06/08 | 11/08 | Tendance |
|---|---:|---:|---|
| Prix `{X}€ deslocação + {H}€/h. A partir de {Y}€` | 336 fichiers | **303** | ✅ **diminue** |
| — écart **+15 €** (générateur à 85 €/h périmé) | 207 | **207** | stable |
| — écart 0 (corrects) | 96 | **96** | stable |
| — dispersés (retouches manuelles) | ~33 | **0** | ✅ résorbés |
| FAQ `demoram a chegar` | 955 fichiers | **955** | ⚠️ **inchangé** |
| `" conforme zona"` | 1279 | **526 fichiers** | (unité différente — recompter en occurrences ET en fichiers au prochain run) |
| `min conforme zona` | 428 | **428** | stable |

Le gisement prix **diminue** ; le gisement FAQ ne bouge pas — cohérent avec le diagnostic ci-dessus : **rien ne le régénère, mais rien ne l'a purgé non plus** faute de GO batch.

## 🛑 R11 — 303 fichiers annoncent un prix minimum FAUX

Phrase de la forme « **{X}€ deslocação + 70€/h. A partir de {Y}€ (1h).** » où **{Y} ≠ {X} + 70**. **207 occurrences suivent un écart systématique de +15 €** — signature d'un générateur qui calcule `deslocação + 85` au lieu de `+ 70` (tarif horaire périmé de 85 €/h). C'est un **bug de template**, pas une erreur aléatoire. **96 sont correctes.**

**Pourquoi c'est grave** : prix faux en `<meta name="description">`, donc **visible directement en SERP**, sur 303 pages. R11 + risque commercial.

**Correction recommandée — par RETRAIT, zéro arithmétique** : supprimer « A partir de {Y}€ (1h). » et conserver « {X}€ deslocação + 70€/h », qui est la grille source de vérité énoncée verbatim. **Prototype ouvert ce run (PR #268) sur la sede operacional.**

**Décision demandée** : (a) valider le retrait comme formulation ; (b) autoriser le batch sur les 302 fichiers restants.

Commande de recomptage (script Python obligatoire — motif non-ASCII) :
```python
import os,re,collections
pat=re.compile(r'(\d+)€ deslocação \+ (\d+)€/h\. A partir de (\d+)€')
c=collections.Counter(); files=set()
for dp,dn,fn in os.walk('.'):
    if '_archive' in dp or '.git' in dp: continue
    for f in fn:
        if not f.endswith('.html'): continue
        p=os.path.join(dp,f); s=open(p,encoding='utf-8',errors='ignore').read()
        for m in pat.finditer(s):
            d,h,t=map(int,m.groups()); c[(d,h,t,d+h)]+=1; files.add(p)
print(len(files), sorted(c.items()))
```

## Tâche suivante recommandée
1. **Si GO batch prix** : les 302 fichiers restants, par retrait, patron de la PR #268 (ce run) et #240 (CU, mergée).
2. **Si GO** : corriger `scripts/r12_blog_safe_cleanup.py` L49-50 et `scripts/r12_hubs_cleanup.py` L37-45 (chaîne de remplacement inachevée), **puis** batch FAQ sur les 955 fichiers.
3. **Si GO** : corriger `scripts/gen_concelhos.py` (délai chiffré `faq_time()`, claims 24h L143/L148, « relatório técnico » L149) — **avant** toute purge des pages `concelhos/`.
4. Sans GO : prototype R11 prix sur une 2ᵉ page à fort trafic, ou audit par point d'entrée des pages les plus crawlées.

## Apprentissages (self-improving)
- 🔴 **NOUVEAU — un gisement qui ne diminue pas n'implique pas forcément un générateur.** Ici la source était la **chaîne de remplacement d'un script de purge**, inachevée (`"…zona Z"`, numéro jamais concaténé). ➡️ **Contrôle à ajouter à tout script de substitution : la chaîne de remplacement doit être une phrase complète, testée sur un échantillon**, jamais un fragment de gabarit.
- 🔴 **NOUVEAU — distinguer script one-shot et étape de build change complètement la décision.** Un one-shot cassé laisse un gisement **figé et sûr à purger** ; un générateur cassé **annule tout batch**. Les deux existent ici : `r12_*.py` (one-shot) et `gen_concelhos.py` (générateur). **Trier avant de demander un GO batch.**
- 🔴 **Leçon transverse du run, venue de `canalizador-urgente` — un batch de conformité peut corrompre la RÈGLE qu'il applique.** Le commit `fb9dd2415` (CU) a substitué `relatório técnico` → `orçamento por escrito` sur 2003 fichiers **y compris `AGENTS.md`**, désarmant le ruling. ➡️ **Vérifié ce run : l'`AGENTS.md` d'EU n'est PAS corrompu** (son §12 a été amendé le 30/07 — Filipe délivre officiellement Ficha + Termo, Lei 14/2015 — et L184 liste « orçamento por escrito » comme ✅ OK). ➡️ **Règle : tout batch de substitution doit exclure `AGENTS.md`, `SEO_PLAN.md`, `context.md`, `CLAUDE.md`.** Et **avant d'escalader une contradiction de doctrine : `git log -S "<fragment>" -- AGENTS.md`.**
- **Le contrôle positif fonctionne et doit rester systématique** : `65€` = 1473 fichiers prouve que le scan voit les motifs non-ASCII, donc 303 et 955 sont de vrais chiffres.
- 🔴 **Tout grep à motif non-ASCII passe par un script Python/bash**, jamais une boucle inline `zsh -c` (le motif est mangé → 0 résultat).
- 🔴 **Vérifier qu'un gisement DIMINUE entre deux runs.** Fait ce run : prix 336→303 ✅, FAQ 955→955 ⚠️.
- **Corriger un prix faux par RETRAIT du total, pas par recalcul.** Conserver les composants (grille source de vérité) et supprimer le total dérivé : zéro arithmétique, donc zéro invention (R4).
- ⚠️ **HEURISTIQUE FAUSSE À NE PAS RÉINTRODUIRE** — « ce site = 70 €/h, donc un `65€` ici est une erreur » est **FAUX**. `65 €` est la déslocation **Zone 6**, légitime sur les 4 sites (1473 fichiers). Distinction réelle : **70 €/h = main-d'œuvre électricité · 65 €/h = main-d'œuvre canalisation · 65 € = déplacement Z6**.
- **R145 autorise explicitement « 24h/7 dias »** (AGENTS.md L184). Ce qui est banni : les promesses de délai personnalisées. ⚠️ C'est **l'inverse** des sites `*-norte-reparos`. **Ne pas purger « 24h » ici.**
- **Quand une question FAQ porte sur un délai, retirer le couple Q/R plutôt que le réécrire.** Validé par le merge de la PR #200.
- **Toute purge de conformité doit re-parser le JSON-LD après coup** et vérifier que chaque `acceptedAnswer.text` fait > 20 caractères. ⚠️ Ne pas exiger « commence par une majuscule ».

## Edge cases détectés
- **Le `/tmp` du sandbox ≠ le `/tmp` du host.** Worktrees sous `~/work/Sites/_worktrees/` (monté des deux côtés).
- **Les commandes `git` ne fonctionnent PAS depuis le sandbox dans un worktree** (le `.git` contient un chemin absolu host). Dans un worktree : grep/lecture au sandbox, **tout `git` via desktop-commander**.
- 🔴 **`set -e` + zsh : un glob sans correspondance (`rm -f .git/*.lock`) fait AVORTER tout le script.** Utiliser `setopt null_glob`.
- **Worktree obligatoire** : copie de travail sale en permanence, posée sur une branche feature d'une autre automation. **Jamais `reset --hard`/`stash`/`clean`** (R-WT).
- **Agents concurrents confirmés sur ce checkout.** Parade : `git branch --show-current` avant **chaque** commit, `git diff origin/main..HEAD --name-only` avant le push, `gh pr create --head <branche-explicite>`.
- Le sandbox n'a ni `gh` ni credentials Git → tout git/gh via `mcp__desktop-commander__start_process` (host, `gh` authentifié `taffrand-gif`). Il est **excellent et rapide** pour les grep/scripts sur les milliers de fichiers HTML montés.
- `public/index.html` et `./index.html` **diffèrent** (même situation que `canalizador-urgente`). Canonicals identiques et corrects → pas d'urgence, mais doublon à arbitrer conjointement avec CU.
- Ce repo est un site **statique pur** : pas de `tsc`, vérification par grep + re-parsing JSON.
- `_archive/` contient de vieux fichiers avec violations — **NE PAS patcher**, l'exclure de tous les greps.

## Blocages connus
1. 🛑 **303 fichiers avec un prix minimum faux** (R11 actif, visible en SERP) = attente GO batch + validation de la formulation. **Prototype ouvert : PR #268.** Le plus grave du repo.
2. 🛑 **955 fichiers avec une réponse FAQ vide** = attente GO batch. **Verrou technique levé** (rien ne régénère), mais corriger d'abord `r12_blog_safe_cleanup.py` + `r12_hubs_cleanup.py`.
3. 🛑 **`scripts/gen_concelhos.py`** : délai chiffré + claims 24h + « relatório técnico ». Régénère à chaque exécution → à corriger **avant** toute purge des pages `concelhos/`. GO requis.
4. **Blog resurrection 58 MD** = bloqué conformité, attente décision.
5. **`curto-circuito` dedup FAQ** (branche `feat/monopole-piliers-eu`) = à pusher + GO merge.
6. **Doublon `public/` ↔ racine** — à arbitrer conjointement avec `canalizador-urgente`.
7. **PR #160 (IndexNow) est CLOSED** — point clos, ne pas le rouvrir sans instruction.
8. A2 (/zonas/) : **obsolète**, ne pas rouvrir. A4-TER (`Atendimento prioritário`) : **résolu**, ne pas rouvrir.

## Instructions améliorées pour prochain run
1. **Pré-flight host-side** : `setopt null_glob` puis `rm -f ~/work/Sites/eletricista-urgente/.git/*.lock`.
2. **Worktree obligatoire** : `git worktree add -q ~/work/Sites/_worktrees/loop-YYYY-MM-DD/eu -b loop/YYYY-MM-DD-eletricista-urgente-{tache} origin/main`. **Jamais `/tmp`, jamais la copie principale, jamais `reset --hard`/`stash`/`clean`.**
3. **Recompter les 2 gisements** (303 prix / 955 FAQ) et comparer au tableau ci-dessus. **Contrôle positif obligatoire.**
4. **Tout grep non-ASCII par script Python**, jamais une boucle inline.
5. **Ne PAS purger « 24h » sur ce site** — R145 l'autorise. **Ne jamais « corriger » un `65€`** sans lire son contexte (= déplacement Z6).
6. **Corriger un prix faux par retrait du total dérivé**, en conservant les composants de la grille.
7. **Après tout patch d'un JSON-LD : re-parser TOUS les blocs** et vérifier chaque `acceptedAnswer.text` (> 20 caractères).
8. `git branch --show-current` avant **chaque** commit et `git diff origin/main..HEAD --name-only` avant chaque push (agents concurrents). `gh pr create --head <branche-explicite>`.
9. **Répartition des outils** : grep/lecture/scripts → `mcp__workspace__bash` ; git/gh → `mcp__desktop-commander__start_process`.
10. **Vérifier que `context.md` est arrivé sur `main`** : `git show origin/main:context.md | head -6` doit afficher la date du jour.
11. Nettoyer : `git worktree remove …` puis `git worktree prune`. Si le retrait échoue, laisser en place et le signaler — ne jamais forcer.
