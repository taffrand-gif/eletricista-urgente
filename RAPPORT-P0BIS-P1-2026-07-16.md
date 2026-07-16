# RAPPORT P0bis + P1 — 2026-07-16

## Résumé exécutif

Mission réversible (branches + draft PR, JAMAIS merge/deploy/301) exécutée par Hermes Agent sur le repo `~/work/Sites/eletricista-urgente` (uniquement ce repo).

**2 branches ouvertes, 2 draft PRs à valider par Philippe.**

- **Étape 1 — sitemap tiering** : exécutée. Commit `10e3bd109` sur branche `feat/p0-indexation-sitemap-canonical-robots` (PR #149).
- **Étape 2 — P1 hubs concelhos Variante A** : **GATE FAIL au sens SPEC §11.5**, batch suspendu, rapport ci-dessous. Générateur reproductible commité sur nouvelle branche `feat/p1-hubs-eletricista` (draft PR séparé).

---

## Étape 1 — Sitemap tiering (commit `10e3bd109`)

**Branche** : `feat/p0-indexation-sitemap-canonical-robots` (PR #149)
**DOd** : `grep -c '<loc>' public/sitemap-core.xml` = **80**.

### Modifs
- `public/sitemap-core.xml` créé : 80 URLs (1 racine + 1 pilier + 78 hubs `/eletricista-urgente-<slug>.html` réels)
- `public/sitemap-villages.xml` créé : squelette (0 URLs) + manifeste explicite documentant ce qui manque
- `public/sitemap.xml` : remplacé par mirror de `sitemap-core.xml` (compat GSC conservée, découvre 80 URLs au lieu de 1987 URLs dont 90% pointaient vers du vide)
- `public/robots.txt` : référence désormais les 2 sitemaps

### ÉCART PAR RAPPORT AU SPEC

Le SPEC § Étape 1 annonçait : « Remplacer sitemap.xml complet (~2000 URLs plat) par sitemap-core : 33 hubs concelhos/ + 6 distritos/ + pages money-kw existantes + piliers. Les ~1900 pages village restent crawlables via maillage interne mais HORS sitemap-core. »

**Inventaire disque réel** (état hérité de PR #148 + branches amont) :

| Catégorie | Disque | Cible SPEC |
|---|---:|---:|
| `concelhos/<slug>.html` | **0 / 33** | 33 |
| `distritos/<slug>.html` | **0 / 6** | 6 |
| Pages money-kw × city | **0** | plusieurs centaines |
| Villages `/eletricista-<slug>.html` | **0** | ~1900 (déjà mentionné par mission) |
| Hubs `/eletricista-urgente-<slug>.html` | **78** | — |

Le sitemap.xml actuel référençait déjà `/concelhos/<slug>` et `/distritos/<slug>` alors que **les fichiers correspondants n'existent pas sur disque**. Publier ces URLs dans sitemap-core aurait perpétué la désinformation GSC.

**Décision** : limiter `sitemap-core.xml` aux URLs dont le fichier HTML existe (78 hubs cidade + 2 piliers). Les autres catégories sont documentées dans `sitemap-villages.xml` (squelette avec manifeste). À chaque fois qu'une catégorie est matérialisée sur disque, elle pourra rejoindre `sitemap-core.xml` ou remplir `sitemap-villages.xml`.

**Preuve DoD** :
```
$ grep -c '<loc>' public/sitemap-core.xml
80
```

**Sitemap-plain.xml et sitemap-priority.xml (483 lignes chacun)** : non touchés.

### Note sur la 78 hubs cidade (pas de doublons accent cette fois)

Les URLs `/eletricista-urgente-<slug>` héritées (PR #148 self-ref) sont en ASCII-lowercase diacritics-strippés. Pas de doublons accent dans les fichiers disque. Le sitemap-core est donc **propre**, contrairement à l'ancien `sitemap.xml` qui avait 433 entrées diacritique-dupliquées pour ces 78 hubs.

---

## Étape 2 — P1 hubs concelhos Variante A : GATE FAIL, batch suspendu

**Branche créée** : `feat/p1-hubs-eletricista` (depuis `origin/main`)
**Aucun commit, aucun patch** sur les 33 pages `concelhos/<slug>.html`. Seuls les fichiers reproductibles (script + rapport) sont ajoutés.

### État du disque (détecté en arrivant sur la branche)

Les 33 pages `concelhos/<slug>.html` **existent** (générées par `scripts/gen_concelhos.py` PR #147). PR #147 a différencié le LEAD et les barrios, mais le reste du gabarit reste très templaté.

Mesure GATE (script dans `scripts/p1/measure_baseline_jaccard.py` à venir ; calcul inline ici) :

| Métrique | État actuel | Cible SPEC §10 |
|---|---:|---:|
| Jaccard pairwise médian (corps complet, 528 paires) | **0.921** | ≤ 0.35 |
| Jaccard p90 | **0.934** | ≤ 0.50 |
| Jaccard max | **0.958** | outliers ≤ 0.60 |
| Mots uniques / page | ~277 | 150-250 |
| Pages hub cibles | 33 | 33 |

Profil par section (Macedo ↔ Braganca) :

| Section | Jaccard |
|---|---:|
| Transparence tarifaire (H2) | **1.00** |
| Tabela de deslocação | **1.00** |
| Serviços urgentes | 0.95 |
| Como agimos | 0.95 |
| FAQ | 0.99 |
| Porquê choisir | 0.95 |
| Bairros servidos | **0.55** |

**5 sections sur 8 sont à 0.95-1.00.**

### Test d'injection Variante A seule (prototype Macedo)

Script `scripts/p1/gen_p1_hub_concelho.py` génère le bloc Variante A :
- 286 mots, 161 uniques
- Préséance `concelhos.json` ↔ `precos-zonas.json` : **NON tranchée** → `{{price_block}}` **BLOQUÉ** (absence explicite, conformément SPEC §1 + §11.4)
- Liens hub → 6 villages réels (texte + km, **pas de liens** car les pages village `/eletricista-<slug>.html` n'existent pas) + 1 pilier `/top-10-razoes-contratar-eletricista`
- canonical self-ref : déjà OK sur la page (PR #148)

Si on appliquait le patch sur 33 hubs (le texte injecté variant seulement par `concelho_name` et 6 villages), simulation :

- **Macedo ↔ Braganca** : 0.914 → **0.725** (baisse de 0.19, mais loin de la cible 0.35)
- Jaccard pairwise médian resterait **≈ 0.92** (les 5 sections non touchées dominent)

**Conclusion** : pour passer de 0.92 à 0.35, il faudrait **réécrire 4-5 sections sur 8 par concelho**, soit ~280 mots uniques par page à injecter. C'est un travail de **refonte de gabarit** (PR séparée, ~1000+ lignes spec), pas une Variante A.

### Décision conforme SPEC §11.5

> « Si fail → STOP, rapporte, ne batch pas. »

**STOP appliqué** :
- Aucun `concelhos/<slug>.html` patché
- Générateur `scripts/p1/gen_p1_hub_concelho.py` commité pour usage futur
- Rapport présent dans `RAPPORT-P0BIS-P1-2026-07-16.md`
- Draft PR ouvert pour traçabilité

### Préconisations pour la suite (à arbitrer par Philippe)

Trois voies possibles, par effort croissant :

**Option A — Refonte gabarit ciblée (recommandé pour atteindre Jaccard 0.35)**
1. Auditer le gabarit actuel pour identifier les 4 sections quasi-identiques
2. Réécrire les sections services/como agimos/FAQ/porquê choisir pour qu'elles varient **par des faits réels** :
   - Serviços : piocher dans une liste d'intents réels par zone (curto-circuito rural, falha energia serra, disjuntor dispara em idosos, etc.) — 1 phrase dédiée par hub
   - Como agimos : adapter à la `route_km` (et éventuellement météo / altitude connue) — 1 phrase dédiée par hub
   - FAQ : 2 questions contextualisées sur 5 (les 3 autres restent communes)
   - Porquê choisir : 2 bullets localisés sur 5

Effort estimé : ~1 PR de refonte avec gabarit révisé, puis re-exécution Variante A. Cible 0.35 atteignable.

**Option B — Accepter Jaccard 0.7+ et documenter**
Variante A ajoute les liens villages + pilier + price_block vide. Le Jaccard 0.72 est meilleur que rien (état 0.92) mais reste 2x la cible SPEC. Aucune garantie GEO.

**Option C — Abandon P1 Variante A**
Variante B (village NAP-minimal) reste plus prometteuse : la page village a ~50 champs nommés propres qui la différencieraient — mais conditionne la création effective des pages village (0 actuellement sur disque).

**Recommandation agent : Option A** car :
- seule qui aligne l'effort sur la cible SPEC documentée
- préserve l'investissement de PR #147 (lead déjà différencié)
- crée une base réutilisable pour P1.1 (intents, géo fine)

### Note prix

`{{price_block}}` reste **explicitement absent** du prototype injecté jusqu'à décision de préséance entre `data/concelhos.json` (zone/depuis/h2 réels pour 34 concelhos) et `precos-zonas.json` (zone normalisée). 16 discordances + 2 absences détectées dans le SPEC §1. Tant que Philippe n'a pas tranché, Variante A s'affiche sans chiffre monétaire (conformément à SPEC §11.4 « Refuser toute fusion de zones quand divergentes »).

---

## 2 draft PRs ouverts (NON MERGÉS)

1. **PR #149 suite — sitemap tiering (commit `10e3bd109`)**
   - Branche `feat/p0-indexation-sitemap-canonical-robots`
   - Diff : `+187 / -1989` (sitemap.xml drop + 2 nouveaux + robots.txt)
   - À reviewer et merger par Philippe (jamais auto-merge, AGENTS.md §7)

2. **PR nouveau — P1 prototype générateur + STOP rapport**
   - Branche `feat/p1-hubs-eletricista` depuis `origin/main`
   - Fichiers ajoutés : `scripts/p1/gen_p1_hub_concelho.py`, ce rapport, `LECONS.md`
   - Pas de modification sur `concelhos/<slug>.html` (gate fail)

---

## DoD / Evidence

| Étape | DoD | Preuve |
|---|---|---|
| E1 — sitemap-core | `grep -c '<loc>' public/sitemap-core.xml` | 80 (commit `10e3bd109`) |
| E1 — sitemap-villages | référence robots.txt + squelette documenté | `robots.txt` mis à jour, `sitemap-villages.xml` 19 lignes |
| E1 — non merge | pas de push force, branche, commit seul | `git log -1` commit local |
| E2 — prototype 1 page | Mots uniques 150-250 | 161 uniques sur 286 mots (`gen_p1_hub_concelho.py --dry-run`) |
| E2 — Jaccard vs autre hub | Jaccard cible ≤ 0.35 median | 0.92 (mesure baseline) — **FAIL GATE, pas de batch** |
| E2 — canonical self-ref | déjà OK sur les 33 pages | grep `<link rel="canonical"` concelhos/ (PR #148) |
| E2 — scanner univers HTML complet post-batch | N/A (pas de batch) | — |
| LECONS.md | 1 leçon re-grip post-batch | créé section « Sitemap tiering » |
| 2 draft PRs | sans merge | rapport ci-dessus + status branches |

---

## Fichiers du dépôt modifiés ou créés

**Branche PR #149 (`feat/p0-indexation-sitemap-canonical-robots`)** :
- M `public/robots.txt`
- A `public/sitemap-core.xml`
- A `public/sitemap-villages.xml`
- M `public/sitemap.xml` (mirror de core, pour compat GSC)

**Branche P1 (`feat/p1-hubs-eletricista`)** :
- A `scripts/p1/gen_p1_hub_concelho.py`
- A `RAPPORT-P0BIS-P1-2026-07-16.md` (ce document)
- A `LECONS.md` (créé)

Aucun autre fichier touché. Aucun merge. Aucun deploy. Aucun 301.
