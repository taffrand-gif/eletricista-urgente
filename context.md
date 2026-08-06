# context.md — Loop State

> Écrit par le loop Cowork après chaque run. NE PAS ÉDITER MANUELLEMENT.

## Dernier run
- Date : 2026-08-06
- Tâche exécutée : **AUCUNE modification de code sur ce repo.** Le run a été interrompu (limite d'usage) après la phase d'audit, avant l'ouverture de la PR prototype. **Rien n'a été poussé, aucune branche orpheline laissée.** L'audit ci-dessous est complet, chiffré et directement actionnable : le prochain run peut ouvrir la PR sans refaire le travail.
- Les 3 autres sites ont été traités ce run : PR **#269** (canalizador-norte-reparos), PR **#295** (eletricista-norte-reparos), PR **#240** (canalizador-urgente).

## 🛑 DÉCOUVERTE MAJEURE — R11 : 336 fichiers annoncent un prix minimum FAUX

**C'est la trouvaille la plus importante du run, sur les 4 repos.**

336 fichiers (hors `_archive/`) publient une phrase de la forme :

> « **{X}€ deslocação + 70€/h. A partir de {Y}€ (1h).** »

…où **{Y} ≠ {X} + 70** dans la majorité des cas. Le prix minimum annoncé **contredit la grille énoncée dans la même phrase**, et `PRICING-CANONIQUE.md` (70 €/h électricité · Z1=15 € … Z6=65 €).

| deslocação | €/h | annoncé | réel (d+h) | écart | occurrences |
|---:|---:|---:|---:|---:|---:|
| 15 | 70 | 80 | 85 | **−5** | 1 |
| 15 | 70 | **100** | 85 | **+15** | 10 |
| 25 | 70 | 90 | 95 | −5 | 1 |
| 25 | 70 | 95 | 95 | 0 ✅ | 5 |
| 25 | 70 | **110** | 95 | **+15** | 31 |
| 35 | 70 | 90 | 105 | −15 | 2 |
| 35 | 70 | 100 | 105 | −5 | 3 |
| 35 | 70 | 105 | 105 | 0 ✅ | 19 |
| 35 | 70 | 110 | 105 | +5 | 1 |
| 35 | 70 | **120** | 105 | **+15** | 39 |
| 45 | 70 | 90 | 115 | −25 | 1 |
| 45 | 70 | 100 | 115 | −15 | 2 |
| 45 | 70 | 110 | 115 | −5 | 2 |
| 45 | 70 | 115 | 115 | 0 ✅ | 16 |
| 45 | 70 | **130** | 115 | **+15** | 26 |
| 55 | 70 | 110 | 125 | −15 | 1 |
| 55 | 70 | 120 | 125 | −5 | 3 |
| 55 | 70 | 125 | 125 | 0 ✅ | 28 |
| 55 | 70 | 130 | 125 | +5 | 2 |
| 55 | 70 | **140** | 125 | **+15** | 54 |
| 65 | 70 | 100 | 135 | −35 | 1 |
| 65 | 70 | 110 | 135 | −25 | 1 |
| 65 | 70 | 120 | 135 | −15 | 6 |
| 65 | 70 | 130 | 135 | −5 | 6 |
| 65 | 70 | 135 | 135 | 0 ✅ | 28 |
| 65 | 70 | **150** | 135 | **+15** | 47 |

**Lecture** :
- **207 occurrences suivent un écart systématique de +15 €** — signature d'un générateur qui calcule `deslocação + 85` au lieu de `deslocação + 70`, probablement un **tarif horaire périmé de 85 €/h**. C'est un bug de template, pas une erreur aléatoire.
- **96 occurrences sont correctes** (écart 0).
- Le reste (~33) est dispersé, sans logique — vraisemblablement des retouches manuelles.
- ⚠️ **Page la plus exposée : `eletricista-urgente-macedo-de-cavaleiros.html`** — la **sede operacional**, Z1. Elle annonce « A partir de **100€** » là où la grille donne **85 €** : **+17,6 % de surestimation sur la page phare**.

**Pourquoi c'est grave** : c'est un prix faux servi en production, en `<meta name="description">` donc **visible directement en SERP**, sur 336 pages. Risque R11 (invention) + risque commercial (annonce supérieure au tarif réel = perte de clics ; annonce inférieure = litige).

**Pourquoi le loop ne l'a pas corrigé** : 336 fichiers = batch, gaté par AGENTS.md §12 (« pas de script qui refait 50 pages en série » ; prototype 1 page + GO explicite requis).

**Correction recommandée — par RETRAIT, zéro arithmétique** : supprimer le segment « **A partir de {Y}€ (1h).** » et conserver « {X}€ deslocação + 70€/h », qui est la grille source de vérité énoncée verbatim. Aucun montant à recalculer → zéro invention (R4). C'est exactement le patron appliqué le même jour sur `canalizador-urgente` (PR #240, défaut jumeau `Desde 130`).

**Décision demandée à Philippe** : (a) valider le retrait comme formulation, ou fournir la phrase de remplacement souhaitée ; (b) autoriser le batch sur les 336 fichiers. Sinon, ordonner un prototype 1 page d'abord (`eletricista-urgente-macedo-de-cavaleiros.html` est la cible désignée).

**Commande de recomptage** (script Python obligatoire — motif non-ASCII, cf. §Apprentissages) :
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

## 🛑 Gisement FAQ vide — **955 fichiers**, NON RÉSORBÉ

- ✅ **PR #200 est MERGÉE** — le pattern de retrait du couple Q/R est donc **validé par Philippe**. Le prototype `calculadora-de-preco.html` est propre (`demoram a chegar` → 0).
- ⚠️ **MAIS le gisement mesure toujours 955 fichiers** au 06/08, contre « ~955 » au 29/07 — **il ne diminue pas**. La correction d'une page a été compensée. **Hypothèse à vérifier en priorité : un générateur de pages continue à produire le template cassé.** Si c'est le cas, tout batch sur les 955 fichiers sera annulé au prochain build : **il faut corriger la source avant les pages.**
- Pistes de source à inspecter : `scripts/normalize-blog-md.js`, `scripts/r12_blog_safe_cleanup.py`, `scripts/r12_hubs_cleanup.py` (les 3 contiennent la chaîne `conforme zona`), plus `tools/enrich_concelhos.py` et `tools/enrich-distritos-maillage.py`.
- Compteurs au 06/08 : `demoram a chegar` **955** fichiers · `" conforme zona"` **1279** · `min conforme zona` **428**.
- **Décision demandée** : (a) autoriser le batch sur les 955 fichiers, **et** (b) autoriser d'abord la correction du générateur qui les régénère.

## ✅ Propagation vérifiée ce run (audit croisé 4 repos)
- Le gisement FAQ vide **existe aussi sur `canalizador-urgente`** : **816 fichiers** (809 en `" conforme zona"`). C'était la vérification demandée par le run du 29/07 — **faite, positive**. Prototype ouvert côté CU : PR #240.
- Le défaut de prix minimum existe sur les **2 sites urgence** : `Desde 130` / `130 EUR` sur **73 fichiers** côté CU, et le gisement de 336 fichiers décrit ci-dessus côté EU. **Même famille de bug, deux repos.**
- Artefacts dans les `name` de questions (`"Trabalham Atendimento — ligue 932 321 892/7d?"`) : **0 sur EU**, présent sur CU. Pas de propagation dans ce sens.

## Tâche suivante recommandée
1. **Vérifier si un générateur régénère le template FAQ cassé** (voir ci-dessus) — c'est la question qui conditionne tout le reste. Audit lecture seule, faisable sans GO.
2. **Prototype R11 prix minimum** sur `eletricista-urgente-macedo-de-cavaleiros.html` (sede operacional, Z1, écart +15 €) : retirer « A partir de 100€ (1h). », conserver « 15€ deslocação + 70€/h ». 1 fichier = 1 PR, patron déjà validé par la PR #240 sur CU.
3. Si GO batch : (a) les 336 fichiers prix, (b) les 955 fichiers FAQ — dans cet ordre, un prix faux étant plus grave qu'une réponse vide.
4. Pistes toujours 🛑 gatées : soumission IndexNow (PR #160 **CLOSED**, à rouvrir si besoin), blog resurrection 58 MD, `curto-circuito` dedup FAQ (branche `feat/monopole-piliers-eu`, à pusher).

## Apprentissages (self-improving)
- 🔴 **NOUVEAU — ne jamais faire confiance à un audit « 0 occurrence » sans CONTRÔLE POSITIF.** Avant de conclure qu'un motif est absent, greper un motif **dont on sait qu'il est présent** pour prouver que la commande fonctionne. Appliqué ce run (`65€` → 1473 fichiers, `70 EUR/h` → 99) : c'est ce qui a permis d'affirmer que `Desde 130` → 0 sur EU est un **vrai** zéro, et non un faux négatif.
- 🔴 **Le piège du grep non-ASCII s'est REPRODUIT sur un autre repo.** La leçon (« passer un motif contenant `€` à `git grep -F` via une boucle inline `zsh -c` mange le motif et renvoie 0 résultat ») était consignée **ici** le 29/07 — et le **même jour**, l'audit de `canalizador-urgente` concluait `130 EUR` → 0 occurrence alors que la réalité est **66 fichiers**. ➡️ **Méta-règle : une leçon de tooling vaut pour les 4 repos et doit être copiée dans les 4 `context.md` le jour où elle est apprise.** Appliqué ce run.
- 🔴 **Vérifier qu'un gisement DIMINUE entre deux runs.** Le gisement FAQ est à 955 fichiers le 29/07 **et** le 06/08 malgré une correction mergée. Un gisement qui ne bouge pas malgré un correctif = **il y a une source qui le régénère**. Contrôle à ajouter systématiquement : recompter le gisement en début de run et comparer au chiffre du `context.md`.
- **Corriger la source avant les pages.** Un batch sur 955 fichiers générés est annulé au prochain build. Chercher le générateur AVANT de demander un GO batch.
- ⚠️ **HEURISTIQUE FAUSSE À NE PAS RÉINTRODUIRE** — « ce site = 70€/h, donc un `65€` ici est une erreur » est **FAUX**. `65 €` est le tarif de **déslocation Zone 6**, légitime sur les 4 sites (1473 fichiers ici). Distinction réelle : **70 €/h = main-d'œuvre électricité · 65 €/h = main-d'œuvre canalisation · 65 € = déplacement Z6**. Ne jamais « corriger » un `65€` sans lire son contexte.
- **R145 autorise explicitement « 24h/7 dias »** (AGENTS.md L123/L163). Ce qui est banni, ce sont les promesses de délai personnalisées (« resposta prioritária », « mediante confirmação por telefone »). ⚠️ C'est **l'inverse** des sites `*-norte-reparos` où « 24h » est une violation R12 par cannibalisation d'intent. **La même chaîne est violation sur 2 sites et conforme sur les 2 autres.**
- **Quand une question FAQ porte sur un délai, retirer le couple Q/R plutôt que le réécrire** : R145 interdit le délai chiffré, R11 interdit d'inventer, « mediante confirmação » est banni → aucune réponse honnête ET conforme n'existe. Le vide honnête > le faux. **Validé par le merge de la PR #200.**
- **Corriger un prix faux par RETRAIT du total, pas par recalcul.** Conserver les composants (grille source de vérité) et supprimer le total dérivé : zéro arithmétique, donc zéro invention (R4). Patron appliqué sur CU (PR #240), à reprendre ici.
- **Toute purge de conformité doit re-parser le JSON-LD après coup** et vérifier que chaque `acceptedAnswer.text` fait > 20 caractères. ⚠️ Ne pas ajouter « commence par une majuscule » comme critère **bloquant** : une réponse légitime peut commencer par un chiffre (« 70 €/h + deslocação… »).
- **Méthode fiable pour auditer ce repo volumineux** : `git archive origin/main | tar -x -C /tmp/scan` puis grep local, **ou** worktree sous `~/work/Sites/` + grep via le sandbox (plus rapide).

## Edge cases détectés
- 🔴 **NOUVEAU — le `/tmp` du sandbox et le `/tmp` du host sont DEUX systèmes de fichiers distincts.** Un worktree créé dans `/tmp` via desktop-commander est **invisible** au sandbox. Les worktrees doivent être créés **sous `~/work/Sites/`** (monté des deux côtés). Convention adoptée : `~/work/Sites/_worktrees/loop-YYYY-MM-DD/{cnr,enr,cu,eu}`.
- 🔴 **NOUVEAU — les commandes `git` ne fonctionnent PAS depuis le sandbox dans un worktree** : le fichier `.git` d'un worktree contient un chemin **absolu host** qui ne résout pas côté sandbox → `fatal: not a git repository`. Dans un worktree : grep/lecture au sandbox, **tout `git` via desktop-commander**.
- **Worktree obligatoire sur ce repo** : copie de travail sale en permanence (7 fichiers au 06/08) et posée sur `fix/eu-conform-falha-energia-scope-r145-t_0dd0259b`.
- **Agents concurrents confirmés sur ce checkout.** Parade : `git branch --show-current` avant **chaque** commit, `git diff origin/main..HEAD --name-only` avant le push, `gh pr create --head <branche-explicite>`.
- Le sandbox `mcp__workspace__bash` n'a ni `gh` ni credentials Git → tout git/gh passe par `mcp__desktop-commander__start_process` (host macOS, `gh` authentifié `taffrand-gif`, scopes `repo`+`workflow`). Le sandbox est en revanche **excellent et rapide** pour les grep/scripts sur les milliers de fichiers HTML montés.
- `public/index.html` et `./index.html` **diffèrent** (même situation que `canalizador-urgente`). Canonicals identiques et corrects des deux côtés → pas d'urgence, mais le doublon reste à arbitrer conjointement avec CU.
- Ce repo est un site **statique pur** : pas de `tsc` possible, vérification post-patch par grep + re-parsing JSON.
- `_archive/` contient de vieux fichiers avec violations — **NE PAS patcher**, et l'exclure de tous les greps.

## Blocages connus
1. 🛑 **336 fichiers avec un prix minimum faux** (R11 actif, visible en SERP) = attente GO batch + validation de la formulation. **Le plus grave du repo.**
2. 🛑 **955 fichiers avec une réponse FAQ vide** = attente GO batch. Pattern validé (PR #200 mergée) mais **le gisement ne diminue pas** → vérifier le générateur d'abord.
3. **Blog resurrection 58 MD** = bloqué conformité, attente décision Philippe.
4. **`curto-circuito` dedup FAQ** (branche `feat/monopole-piliers-eu`) = à pusher + GO merge, non traité.
5. **Doublon `public/` ↔ racine** — à arbitrer conjointement avec `canalizador-urgente`.
6. **PR #160 (IndexNow) est CLOSED** — point clos, ne pas le rouvrir sans instruction.
7. 🔴 **Le goulot est le merge, pas la production.** **27 PR ouvertes** sur ce repo au 06/08 — le plus embouteillé des 4 (**60 au total** : CNR 8, ENR 21, CU 5, EU 27). L'écrasante majorité vient des automations de conformité, pas du loop. **À arbitrer : session de merge groupée, ou ralentissement des automations.**
8. A2 (/zonas/ 8 pages, blocage du 30/06) : **obsolète** — 33 hubs concelhos + 200 villages P1C livrés depuis. Ne pas rouvrir.
9. A4-TER (`Atendimento prioritário`) : **résolu**, 0 occurrence. Ne pas rouvrir.

## Instructions améliorées pour prochain run
1. 🔴 **Pré-flight** : `rm -f ~/work/Sites/eletricista-urgente/.git/*.lock` (zsh dit « no matches found » s'il n'y en a pas — normal).
2. 🔴 **Travailler en worktree sous `~/work/Sites/`** : `git worktree add -q ~/work/Sites/_worktrees/loop-YYYY-MM-DD/eu -b loop/YYYY-MM-DD-eletricista-urgente-{tache} origin/main`. Jamais `/tmp`, jamais la copie principale.
3. 🔴 **Recompter les 2 gisements en début de run** (336 prix / 955 FAQ) et **comparer aux chiffres ci-dessus**. S'ils n'ont pas bougé malgré un merge, chercher le générateur.
4. 🔴 **Tout grep à motif non-ASCII (`€`, accents, guillemets) passe par un script Python/bash**, jamais une boucle inline `zsh -c`. Et **toujours un contrôle positif** avant de conclure « 0 occurrence ».
5. **Ne PAS purger « 24h » sur ce site** — R145 l'autorise explicitement.
6. **Ne jamais « corriger » un `65€`** sans lire son contexte (= déplacement Z6, légitime).
7. Tâche suivante : audit du générateur (lecture seule, sans GO), puis prototype R11 prix sur `eletricista-urgente-macedo-de-cavaleiros.html`.
8. **Corriger un prix faux par retrait du total dérivé**, en conservant les composants de la grille — zéro arithmétique, zéro invention.
9. **Après tout patch d'un JSON-LD : re-parser TOUS les blocs `application/ld+json`** du fichier et vérifier chaque `acceptedAnswer.text` (> 20 caractères, non vide).
10. `git branch --show-current` avant **chaque** commit et `git diff origin/main..HEAD --name-only` avant chaque push (agents concurrents). `gh pr create --head <branche-explicite>`.
11. **Répartition des outils** : grep/lecture/scripts → `mcp__workspace__bash` ; git/gh → `mcp__desktop-commander__start_process`.
12. PR : `cat > /tmp/pr-xxx.md <<'EOF'` + `gh pr create --body-file`.
13. 🔴 **Vérifier que `context.md` est bien arrivé sur `main`** en fin de run : `git show origin/main:context.md | head -6` doit afficher la date du jour. Le run du 05/08 sur `eletricista-norte-reparos` avait sauté cette étape et perdu ses apprentissages.
14. Nettoyer : `git worktree remove ~/work/Sites/_worktrees/loop-YYYY-MM-DD/eu` puis `git worktree prune`.
