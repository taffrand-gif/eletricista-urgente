# context.md — Loop State

> Écrit par le loop Cowork après chaque run. NE PAS ÉDITER MANUELLEMENT.

## Dernier run
- Date : 2026-08-21
- Tâches prévues : **n°1** (passer les signatures de `LECONS.md` sur tout le repo) et **n°2** (contrôler l'équilibre des balises sur tout le repo).
- Tâches réellement exécutées : **les deux**. Elles ont livré une **cause racine** et un **défaut de rendu sur une money page**.
- **PR ouverte : #313** — https://github.com/taffrand-gif/eletricista-urgente/pull/313 — branche `loop/2026-08-21-eu-signatures-lecons` — 6 commits, 5 fichiers.

### Le sweep croisé que `LECONS.md` demandait depuis le 04/08 n'avait jamais été fait
`LECONS.md` porte, depuis le 04/08 : *« **TODO post-merge** : grep croisé des 4 sites pour les 11 chaînes signature sur TOUS les fichiers. Si positif : ouvrir un ticket par site. »*
**Toutes les signatures visées étaient encore en production 17 jours plus tard.**

| Signature | CNR | ENR | CU | EU |
|---|---:|---:|---:|---:|
| NAP parasite `tel:+351****` | 5 / 4f | 18 / 5f | 11 / 4f | **3 / 2f** |
| JSON-LD `https://***` | – | 3 / 1f | 5 / 1f | 1 / 1f |
| pt-br `Você` (corpus INTERDIT) | 40 / 35f | 103 / 96f | 19 / 14f | 22 / 16f |
| chaînes françaises interdites | 2 | 6 | 3 | – |

### 🔴 Cause racine : le NAP parasite est écrit en dur dans le GÉNÉRATEUR DE HUBS
`LECONS.md` traitait le parasite comme un **résidu** à nettoyer page par page. C'en n'était pas un.
**`scripts/p1/gen_p1_hub_concelho.py` L15 : `NAP_TEL = '+351****1892'`.** Chaque hub concelho généré recevait un `href="tel:"` **mort**. C'est pourquoi le défaut revenait après chaque nettoyage. **Le générateur est corrigé — premier commit de la PR.** (Symétrique sur CU : `tools/enrich_cu_desentup.py` L42.)
Valeur `+351932321892` reprise **verbatim** d'`AGENTS.md` L31 (`**NAP** : **+351 932 321 892**`), conformément à #142 (ne jamais recopier depuis un HTML/TSX).

### 🔴 Second défaut : `##style##` — la feuille de style de `contactos.html` n'était jamais ouverte
`contactos.html` L2 portait le marqueur de gabarit `##style##` **à la place de `<style>`** : la feuille de style n'était jamais ouverte, **tout le CSS était servi comme texte visible en haut de la page Contactos**, et le `</style>` de L36 fermait un bloc inexistant. Marqueur résiduel `##endstyle##` (L35) également retiré. Même marqueur sur `calculadora-de-preco.html`.
**Témoin : `<style>`/`</style>` 1/2 → 2/2.**

- **Témoins R8** : `+351****` (hors docs/`_audit`) **4 occ / 3 f → 0** · `##style##`+`##endstyle##` **3 occ / 2 f → 0**.
- Aucun fichier pris par une PR ouverte (contrôle sur les 145 fichiers des PR ouvertes avant patch).

### ⚠️ La PR #312 du 20/08 n'a pas clos sa famille
`eletricista-fuga-corrente-cambres.html`, qu'elle avait réparé, présente **toujours** un déséquilibre `<style>` 2/3, et **5 pages sœurs identiques n'avaient pas été relevées**. Le contrôle de balises de ce run les sort toutes.

## ✅ Gate merge — aucun gate actif
Vérifié ce run : **aucune mention d'attente de merge** dans les 4 `context.md`. Aucun gate réécrit.

🔴 **Rappel de doctrine, à ne jamais réécrire** : R7 interdit de **MERGER**, pas de **PRODUIRE**. Une PR en attente ne gèle pas le repo. Entre le 06/08 et le 09/08, la mention « Attente GO merge (R7) » a été relue chaque nuit comme un ordre d'arrêt → **4 runs sans production**. **Ne jamais réécrire un gate de ce type.**

## 🎯 FILE DE TÂCHES LOOP — état au 2026-08-21

| Rang | Cible | Statut |
|---|---|---|
| — | générateur de hubs · 3 pages `tel:` · `##style##` ×2 | ✅ **traités ce run (#313)** |
| **1** | **7 pages à `<style>` déséquilibré + `BreadcrumbList` JSON-LD DUPLIQUÉ** | ⏳ **PROCHAINE TÂCHE, sans GO.** `eletricista-aguas-vivas.html` et les 6 `eletricista-fuga-corrente-*` (`santa-marinha-do-zezere`, `cambres`, `salzedas`, `valdigem`, `cumieira`). Un `</style>` orphelin sépare **deux copies du même bloc JSON-LD**. Décider quel bloc fait foi, puis retirer le doublon **et** le `</style>` orphelin. |
| **2** | **Les autres signatures de `LECONS.md` jamais grepées** | ⏳ sans GO. Le sweep de ce run a couvert 10 motifs et livré une cause racine ; `LECONS.md` (771 lignes) en contient d'autres. **Meilleur rapport effort/résultat, 2 runs de suite.** |
| **3** | **Corruption `repar`→`arranj` — 30 occurrences / 20 fichiers sur EU** | ⏳ **GO périmètre.** Voir §Blocages n°1. Sur EU les 5 `href` corrompus (`/arranjacao-avarias-eletricas`) **n'ont de cible sous aucune des deux formes** → liens morts antérieurs au batch, à traiter séparément. |
| **4** | **`Você` — 22 occurrences / 16 fichiers** | 🛑 corpus INTERDIT, GO requis (184 sur les 4 repos) |
| **5** | Statistiques non sourcées (h) — commencer par la contradiction `30%` vs `40% dos incêndios domésticos` | ⏳ **2 + 5 fichiers, aucune décision d'offre : c'est une erreur factuelle.** Sans GO. |
| **6** | Chercher sur EU les défauts trouvés sur CU : `Fazem orçamento sem compromisso?` → `gratuito` et la signature `<td>` + `&lt;` | ⏳ sans GO |
| **7** | **Si GO (b2′)** : les 221 fichiers restants de `Tempo de resposta?` | 🛑 **le patch est déjà écrit et en revue (PR #311)** |
| 8 | **Si GO (g)** : les 22 `Sem custo extra de fim de semana` | 🛑 GO |
| 9 | Arbitrer le doublon `public/` ↔ racine, conjointement avec CU | ⏸ |

## Tâche suivante recommandée
1. **Rang 1 — les 7 pages à JSON-LD dupliqué.** Le contrôle de balises les a toutes sorties, le motif de nom est net, aucun GO. **Et cela clôt vraiment la famille que #312 avait ouverte.**
2. **Rang 2 — continuer le sweep `LECONS.md`.** Deux runs de suite, c'est ce qui a produit le plus par unité d'effort.
3. **Rang 5 — la contradiction `30%` vs `40% dos incêndios domésticos`** : erreur factuelle, 7 fichiers, aucun GO.
4. **Rang 6** — sans GO.
5. **Rappel d'une ligne** : les batches 221 / 22 / 960 / 842 restent en attente de GO périmètre.

## Apprentissages (self-improving)
- 🔴 **NOUVEAU — un « TODO post-merge » écrit dans `LECONS.md` n'est exécuté par personne.** Celui-ci datait du 04/08 ; **toutes** les signatures qu'il visait étaient encore en production. ➡️ **Le passage des signatures de `LECONS.md` doit être une étape FIXE du loop, pas une recommandation.**
- 🔴 **NOUVEAU — quand un défaut RÉCIDIVE, la page n'est pas le bon niveau de correction : chercher le GÉNÉRATEUR.** Le NAP parasite avait été nettoyé au moins 5 fois page par page ; il était écrit en dur dans deux scripts Python. ➡️ **Avant de nettoyer une occurrence en série, grepper le motif dans `tools/`, `scripts/` et la chaîne de build.**
- 🔴 **NOUVEAU — une PR qui répare un fichier ne répare pas sa famille.** La #312 a corrigé 2 pages `fuga-corrente` ; 6 sœurs portaient le même défaut, **dont celle qu'elle avait touchée**. ➡️ **Après tout correctif sur une page générée, repasser le contrôle sur l'ensemble du motif de nom** et le consigner comme témoin.
- 🔴 **NOUVEAU — un marqueur de gabarit non substitué ne ressemble pas à une violation et n'apparaît dans aucun compteur.** `##style##` passe tous les audits de conformité, tous les linters JSON-LD, tous les greps de doctrine — et casse le rendu d'une money page. ➡️ **Contrôle à ajouter en fin de run** : `grep -rIoE '##[a-zA-Z_]{3,}##'` et, plus généralement, les délimiteurs non résolus (`{{…}}`, `%%…%%`, `__…__`, `${…}`).
- 🔴 **NOUVEAU — le contrôle de balises trouve mieux que le parseur JSON, confirmé 2 runs de suite.** Le 20/08 c'est le compteur `<style>` qui avait révélé le `<script>` non fermé ; ce soir c'est lui qui sort le `</style>` orphelin ET le JSON-LD dupliqué de 7 pages. **Le garder comme passe systématique.**
- 🔴 **NOUVEAU — la signature d'une corruption de batch, c'est le MOT INEXISTANT.** `grep -rIoE '[[:alpha:]]*<lemme>[[:alpha:]]*' | sort | uniq -c` sort les formes légitimes puis, juste en dessous, les non-mots. Une commande, 523 corruptions révélées sur 4 repos.
- 🔴 **Vérifier les PR ouvertes AVANT de patcher** : `gh pr view <n> --json files --jq '.files[].path'`. 3ᵉ run consécutif où ce contrôle évite un conflit.
- 🔴 **Un fix de conformité sur 1 site n'élimine PAS la contamination sur les sites symétriques.** Confirmé encore ce run : les deux générateurs fautifs étaient le miroir l'un de l'autre.
- 🔴 **Le compteur R12 sur-compte** : R145 **autorise** `24h/7 dias`. Requalifier avant de patcher.
- **Ne pas sur-purger.** R4 se viole dans les deux sens.

## Edge cases détectés
- **`gh` et les credentials Git n'existent QUE sur le host macOS.** Sandbox : `git fetch` OK, **`git push` impossible**. **Répartition** : lecture / grep / parsing Python / **écriture de fichiers** → sandbox ; `git` en écriture / `gh` → `mcp__desktop-commander__start_process`.
- **Le `/tmp` du sandbox ≠ le `/tmp` du host.** Worktrees sous `~/work/Sites/_worktrees/loop-YYYY-MM-DD/`.
- 🔴 **Le filtre sandbox qui mute `https://schema.org` à l'affichage est COSMÉTIQUE** — le disque conserve la bonne valeur. **Mais `https://***` réellement présent sur disque est un vrai défaut.** Distinguer en relisant les octets, pas la sortie du terminal.
- 🔴 **L'anchor d'insertion sur les concelhos EU est `</script>\n <style>`** (avec espace), contrairement à `</script>\n\n<style>` ailleurs — vérifier la convention locale avant de patcher.
- 🔴 **`grep -P` n'existe pas sur macOS** ; **zsh ne fait pas de word-splitting**. Pour tout motif non trivial : **Python**.
- 🔴 **`git commit -m` multiligne est fragile en zsh** → `git commit -F -`. Corps de PR : `--body-file`.
- **Worktree obligatoire** (R-WT). **Jamais `reset --hard` / `checkout -- .` / `stash` / `clean`** sur le checkout partagé.

## Blocages connus
1. 🛑 **GO périmètre — corruption `repar`→`arranj` sans limite de mot** : **523 occurrences / 258 fichiers** sur les 4 repos (EU 30/20). Formes : `parranjar` 221 (`preparar`), `arranjacao` 113 (`reparacao`), `parranjo` 96 (`preparação`), `parranjada/o/os/as` 41, `parranjou` 14. La partie « liens » est livrée sur CNR (#323) et ENR (#363). Le blocage porte sur `Parranjo`→`Preparação` : restauration *probable* mais **pas prouvable par un fichier sur disque** → hors R4 sans arbitrage. **Un GO d'une ligne débloque les 523.**
2. 🛑 **`Você` — 184 occurrences / 161 fichiers sur les 4 repos** (EU 22/16). Corpus INTERDIT `LECONS.md`. GO requis.
3. 🛑 **Batches en attente de GO** : 221 (`Tempo de resposta?`, patch déjà écrit en PR #311) · 22 (`Sem custo extra de fim de semana`) · 960 · 842.
4. ⚠️ **`/arranjacao-avarias-eletricas` — 5 occurrences, aucune cible sous aucune des deux formes.** Lien mort **antérieur** au batch : à traiter comme lien mort, pas comme corruption.
5. ⚠️ **7 pages à `BreadcrumbList` dupliqué** — voir rang 1.
6. ⚠️ **La cause racine du batch `repar`→`arranj` n'est pas identifiée.** **Retrouver le script pour s'assurer qu'il n'est pas rejoué.**
