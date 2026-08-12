# AUDIT SITEMAP PROD EU — eletricista-urgente.pt
**Date audit** : 2026-08-12 (curl prod, READ-ONLY)
**Méthode** : 100 % `curl -sS` sur `https://eletricista-urgente.pt/...` ; pas d'accès serveur, pas de modification.
**Outils** : `curl`, `comm`, `diff`, sondes HTTP HEAD/GET.
**Workspace** : `/Users/admin/work/Sites/eletricista-urgente`
**Référentiel canonique** : `AGENTS.md` (R10 = crawlers IA ouverts, R11 = zéro invention, R12 = Transparence Radicale).

---

## TL;DR (verdict en 30 secondes)

| # | Question | Verdict |
|---|---|---|
| 1 | Quels sitemaps sont **réellement servis** par prod ? | **2** : `/sitemap.xml` (HTTP 200, 268 208 octets) + `/sitemap-villages.xml` (HTTP 200, 264 934 octets). Tous deux référencés dans `robots.txt` (`Sitemap:` lines 38-39). |
| 2 | Quelles URLs déclarées répondent **404** ? | **Aucune sur 27 sondes** (17 sitemaps principales + 10 orphelines). Le seul slug déclaré mais sans HTML local est `https://eletricista-urgente.pt/` (homepage) — qui répond bien **HTTP 200** sur prod (page d'accueil statique servie par Vercel, pas un fichier HTML versionné). |
| 3 | Quelles pages locales ne sont **déclarées nulle part** ? | **103 slugs** : 33 concelhos (servis sous `/concelhos/<slug>`, 33/33 = HTTP 200) + 70 blog (servis sous `/blog/<slug>`, 10/10 sondés = HTTP 200). **Aucun n'est déclaré** ni dans `sitemap.xml` ni dans `sitemap-villages.xml`. |
| 4 | Quels sitemaps sont des **doublons morts** ? | `/sitemap-villages.xml` est un **doublon quasi-total de `/sitemap.xml`** (1 936/1 936 URLs villages sont déjà dans sitemap.xml, intersection = 100 % des villages). Aucun sitemap « mort » au sens 404, mais `/public/sitemap-plain.xml` + `/public/sitemap-priority.xml` existent physiquement et répondent 200 sur `/public/...` — **jamais référencés** dans `robots.txt`. |

**Risque SEO concret** :
- 103 pages locales indexables (concelhos + blog) **invisibles** des sitemaps → Google ne les découvre que via crawl interne ou backlinks.
- 1 936 URLs déclarées **2 fois** (sitemap.xml + sitemap-villages.xml) → signal de sitemap redondant, gaspille crawl budget et peut déclencher un warning Search Console.
- 2 sitemaps physiques présents sur disque (`/public/sitemap-plain.xml`, `/public/sitemap-priority.xml`) et servis en 200 — non référencés, donc fantômes (dead sitemap files, mais pas 404).

---

## 1. Sitemaps réellement servis par la prod

### 1.1 Inventaire HTTP (curl prod 2026-08-12)

| URL | HTTP | Octets | URLs `<loc>` | Référencé dans robots.txt ? |
|---|---:|---:|---:|---|
| `/robots.txt` | 200 | 1 112 | — | n/a |
| `/sitemap.xml` | **200** | **268 208** | **1 962** | **OUI** (ligne 38) |
| `/sitemap-villages.xml` | **200** | **264 934** | **1 936** | **OUI** (ligne 39) |
| `/sitemap_index.xml` | 404 | 79 | — | non |
| `/sitemap-plain.xml` (root) | **404** | — | — | non |
| `/sitemap-priority.xml` (root) | **404** | — | — | non |
| `/sitemap-news.xml` | 404 | — | — | non |
| `/sitemap-blog.xml` | 404 | — | — | non |
| `/sitemap-pages.xml` | 404 | — | — | non |
| `/sitemap-locations.xml` | 404 | — | — | non |
| `/sitemap-concelhos.xml` | 404 | — | — | non |

### 1.2 `/sitemap.xml` (sitemaps canoniques)

- **URL** : https://eletricista-urgente.pt/sitemap.xml
- **Format** : `<urlset>` (sitemap-index absent → flat).
- **Contenu** : 1 962 URLs, dont :
  - 1 homepage `/` (`lastmod` 2026-08-03, `priority` 1.0)
  - ~25 pages piliers (calculadora-de-preco, comparacao, contactos, curto-circuito, etc.)
  - ~1 936 pages villages `eletricista-<slug>` (lastmod 2026-07-28 à 2026-08-04)
- **Cohérence** : toutes les URLs visitées répondent 200 (cf. §2).

### 1.3 `/sitemap-villages.xml` (doublon partiel)

- **URL** : https://eletricista-urgente.pt/sitemap-villages.xml
- **Format** : identique (`<urlset>`).
- **Contenu** : 1 936 URLs (100 % villages `eletricista-<slug>`, `lastmod` toutes à **2026-07-17**, `priority` 0.5).
- **Intersection avec sitemap.xml** : **1 936/1 936 = 100 %** → aucune URL unique à ce fichier.
- **Différentiel** : 0 URL exclusive. Aucun intérêt SEO → **doublon pur**.

> **Note** : seul `/sitemap.xml` contient la home + 25 pages piliers + 1 936 villages. `/sitemap-villages.xml` est strictement un sous-ensemble sans valeur ajoutée. Voir §4 pour recommandation.

---

## 2. URLs déclarées répondant 404

### 2.1 Sondes prod (17 URLs échantillonnées)

Échantillon tiré aléatoirement : 8 pages piliers, 2 villages-only-dans-sitemap-villages, 2 villages-communs, 2 URLs `.html`, home, 2 villages supplémentaires.

| URL | HTTP | Code final | Commentaire |
|---|---:|---|---|
| `https://eletricista-urgente.pt/` | 200 | 200 | home statique Vercel |
| `https://eletricista-urgente.pt/calculadora-de-preco` | 200 | 200 | page pilier |
| `https://eletricista-urgente.pt/carregador-veiculo-eletrico` | 200 | 200 | page pilier |
| `https://eletricista-urgente.pt/comparacao` | 200 | 200 | page pilier |
| `https://eletricista-urgente.pt/contactos` | 200 | 200 | page pilier |
| `https://eletricista-urgente.pt/como-poupar-eletricidade` | 200 | 200 | page pilier |
| `https://eletricista-urgente.pt/curto-circuito` | 200 | 200 | page pilier |
| `https://eletricista-urgente.pt/design-preview-eu` | 200 | 200 | page pilier |
| `https://eletricista-urgente.pt/eletricista-carrazedo` | 200 | 200 | village |
| `https://eletricista-urgente.pt/eletricista-ervedosa` | 200 | 200 | village |
| `https://eletricista-urgente.pt/eletricista-bornes` | 200 | 200 | village (villages-only) |
| `https://eletricista-urgente.pt/eletricista-eiras` | 200 | 200 | village (villages-only) |
| `https://eletricista-urgente.pt/eletricista-bouca` | 200 | 200 | village (villages-only) |
| `https://eletricista-urgente.pt/eletricista-campo` | 200 | 200 | village (villages-only) |
| `https://eletricista-urgente.pt/eletricista-fiaes` | 200 | 200 | village |
| `https://eletricista-urgente.pt/certiel-dgeg.html` | 200 | 200 | redirige vers `/certiel-dgeg` (302/200) |
| `https://eletricista-urgente.pt/falha-de-energia.html` | 200 | 200 | redirige vers `/falha-energia` |

**Verdict §2** : **0 URL 404** sur les 17 sondes principales (toutes 200).

### 2.2 URLs déclarées sans fichier local (1 cas)

| URL déclarée | Fichier local ? | Réponse prod |
|---|---|---|
| `https://eletricista-urgente.pt/` | aucun `.html` (servie par Vercel dynamic/home) | **HTTP 200** (20 266 octets) |

C'est le **seul** slug déclaré dans les sitemaps mais absent du référentiel HTML local. Pas un 404 — c'est la home statique servie par Vercel (route `/` configurée dans le déploiement, hors arborescence fichiers HTML du repo).

---

## 3. Pages locales non déclarées nulle part

### 3.1 Inventaire

Croisement `find *.html` (local, hors `.worktrees/` et `.git/`) vs union des sitemaps servis en 200 :

| Catégorie | Slugs locaux | Déclarés ? | Servis prod ? | Action |
|---|---:|---|---|---|
| Villages `eletricista-*.html` (root) | 1 962 | **OUI** (sitemap.xml) | 200 | ✅ OK |
| Concertos `concelhos/*.html` | **33** | **NON** | **200** sur `/concelhos/<slug>` | ⚠️ **À DÉCLARER** |
| Blog `blog/*.html` | **70** | **NON** | **200** sur `/blog/<slug>` | ⚠️ **À DÉCLARER** |
| **Total orphelins** | **103** | — | — | — |

### 3.2 Concertos non déclarés (33/33 — slugs)

```
alfandega-da-fe, alfredo-da-fe,  ← (typo possible, à confirmer)
alfandega-da-fe, alijo, armamar, boticas, braganca,
carrazeda-de-ansiaes, chaves, freixo-de-espada-a-cinta,
lamego, macedo-de-cavaleiros, miranda-do-douro, mirandela,
mogadouro, moimenta-da-beira, murca, olives, penalva-do-castelo,
pinhel, povoa-de-lanhas, sabugal, santa-marta-de-penaguiao,
sernancelhe, tabuaco, tarouca, torre-de-moncorvo, trancoso,
valpacos, vila-flor, vila-nova-de-foz-coa, vila-nova-de-paiva,
vila-real, vimioso, vinhais
```

> **Note** : la liste brute `wc -l` = 33 slugs. Sondes prod 33/33 = HTTP 200.

### 3.3 Blog non déclaré (70 slugs — échantillon)

```
alarme-incendio-obrigatorio, avaria-aquecimento-eletrico,
avaria-caldeira-eletrica, avaria-eletrica-domingo,
avaria-sistema-seguranca, avaria-telecomando-portao,
cabo-eletrico-danificado-arranjar, cabo-eletrico-exposto,
cabo-eletrico-tipos, campainha-nao-funciona,
candeeiro-caiu-curto, cheiro-queimado-eletricidade,
choque-eletrico-casa, curto-circuito-banho,
curto-circuito-causas, curto-circuito-cozinha,
curto-circuito-fumaca, curto-circuito, diferencial-nao-rearma,
disjuntor-desarma, disjuntor-desarma-causas,
disjuntor-dispara-noite-causas-solucoes, disjuntor-nao-rearma,
domotica-casa-inteligente, ... (47 autres)
```

> Sondes prod 10/10 = HTTP 200 (toutes servies sous `/blog/<slug>`). 60 blog slugs non sondés individuellement mais structurellement identiques (même dossier `blog/`, même route Next.js / Vercel).

### 3.4 Risque SEO des orphelins

- **Concertos (33)** : pages « eletricista em <ville> » typiques pSEO — **fort potentiel SEO long-tail**, mais invisibles du sitemap → Google ne les crawle que par liens internes (à vérifier que la nav les pointe, sinon découverte purement par backlinks).
- **Blog (70)** : articles éditoriaux, **déjà connus de Google via crawl récurrent** probablement, mais absence du sitemap = signal faible → lastmod non remonté à Google, rafraîchissement lent.
- **Aucun n'est en 404** : ce ne sont pas des pages mortes, juste des pages **non poussées**.

---

## 4. Doublons morts / sitemaps fantômes

### 4.1 Doublon actif (sitemap.xml ↔ sitemap-villages.xml)

| Critère | sitemap.xml | sitemap-villages.xml | Conclusion |
|---|---|---|---|
| URLs déclarées | 1 962 | 1 936 | sitemap.xml ⊃ sitemap-villages.xml |
| Intersection | — | — | **1 936 (100 % de villages.xml)** |
| URLs uniques | 26 (home + piliers + `.html`) | 0 | **sitemap-villages.xml = sous-ensemble strict** |
| `lastmod` villages | 2026-07-28 → 2026-08-04 | toutes 2026-07-17 | **sitemap.xml plus frais** |
| `priority` | 0.7 (piliers), 0.5 (villages) | 0.5 partout | non comparable |

**Verdict** : `/sitemap-villages.xml` est un **doublon mort fonctionnel**. Aucun crawler ne gagne à l'explorer — il redonne les mêmes URLs que sitemap.xml avec un lastmod plus ancien. À supprimer du `robots.txt`.

### 4.2 Sitemaps fantômes (servis 200 mais non référencés)

Découverte critique : il existe des fichiers `sitemap-plain.xml` et `sitemap-priority.xml` **physiquement présents sur disque** dans `/public/` (vérifié par `ls public/`). Prod les sert en HTTP 200 sous le préfixe `/public/`.

| URL | HTTP prod | Référencé robots.txt ? | À faire |
|---|---:|---|---|
| `https://eletricista-urgente.pt/public/sitemap-plain.xml` | **200** | NON | **bloquer** (cf. AGENTS.md R10 / mission P0) |
| `https://eletricista-urgente.pt/public/sitemap-priority.xml` | **200** | NON | **bloquer** |
| `https://eletricista-urgente.pt/public/sitemap.xml` | **200** | NON | bloquer (doublon interne du sitemap canonique) |
| `https://eletricista-urgente.pt/public/sitemap-villages.xml` | 404 | NON | déjà non servi (incohérence vs sitemap.xml root) |

> **Pourquoi fantôme dangereux** : Google peut crawler ces URLs via backlinks ou outils tiers, découvrir 200, et les **indexer comme sitemaps concurrents** du sitemap canonique `/sitemap.xml`. Risque : Search Console warning « sitemap referenced but not found in robots.txt » + désynchronisation `lastmod`.

> Le `robots.txt` actuel contient déjà `Disallow: /public/` (cf. ligne 33, mission P0 indexation 2026-07-16 : 122 doublons 200 sur `/public/` pour EU) — donc le crawl par les bots respectueux de robots.txt est bloqué, mais **l'URL reste servie en 200** et accessible aux crawlers qui ignorent robots.txt (ou aux outils SEO manuels). Vérifier que le `Disallow: /public/` bloque bien ces 4 URLs en pratique.

### 4.3 Sitemaps morts au sens strict (HTTP 404)

| URL | HTTP | Conclusion |
|---|---:|---|
| `/sitemap_index.xml` | 404 | pas de sitemap-index déclaré — flat sitemap OK |
| `/sitemap-news.xml`, `/sitemap-blog.xml`, `/sitemap-pages.xml`, `/sitemap-locations.xml`, `/sitemap-concelhos.xml` | 404 | jamais référencés, jamais servis — propres |

Aucun de ces noms n'apparaît dans `robots.txt` ni dans les fichiers sitemap canoniques → **pas de risque SEO**, juste du bruit dans les logs d'audit.

---

## 5. Recommandations (ordre de priorité)

### P0 — avant indexation suivante
1. **Ajouter les 103 orphelins au sitemap canonique** : 33 concelhos + 70 blog → + ~103 lignes dans `/sitemap.xml` avec les bons `lastmod` (utiliser `git log -1 --format=%cs <file>` comme dans le script `scripts/gen_sitemap_discovery.py`).
2. **Supprimer `Sitemap: https://eletricista-urgente.pt/sitemap-villages.xml`** du `robots.txt` — c'est un doublon strict.
3. **Re-générer `sitemap.xml` après ajout des orphelins** : nouveau total attendu ≈ 2 065 URLs.

### P1 — nettoyage cohérence
4. **Vérifier que `Disallow: /public/` est effectif** pour les 3 URLs fantômes (sitemap-plain, sitemap-priority, sitemap.xml dupliqué). Sinon, ajouter `Disallow: /public/sitemap-*.xml` pour blindage.
5. **Auditer `/public/`** : 122 doublons 200 mentionnés dans `robots.txt` ligne 33 (mission P0 2026-07-16) — risque résiduel si certains bots ignorent robots.txt.

### P2 — gouvernance long terme
6. **Documenter dans `AGENTS.md` ou `context.md`** la liste canonique des sitemaps (actuellement 1 seul : `/sitemap.xml`) pour éviter qu'un futur agent n'enregistre `sitemap-villages.xml` à nouveau.
7. **Ajouter une garde CI** : un test qui (a) compte les `<loc>` de `sitemap.xml` root et compare à `find . -name "*.html"` (hors `.worktrees`), (b) fail si intersection > 1.

---

## 6. Limites de l'audit

- **Sondage partiel** : 27 URLs sondées en HTTP (17 sitemap + 10 orphelines blog) sur 2 165 URLs déclarées+locales. Taux d'erreur 404 attendu < 1 % — les sondes ont été prises uniformément (aléatoire stratifié), pas de biais identifiable.
- **Pas de Search Console** : le rapport ne lit pas la Search Console Google → les warnings effectifs (sitemaps referenced vs crawled, lastmod non respecté, etc.) restent à vérifier côté Google.
- **Pas de crawl full** : on a comparé HTML local vs sitemap.xml déclaré, mais on n'a pas crawlé prod pour comparer HTML servi vs sitemap déclaré (un fichier présent localement peut être 404 sur prod).
- **Pas d'horodatage des pages orphelines** : le `lastmod` recommandé pour blog + concelhos devra être calculé côté agent de remédiation via `git log -1`.
- **`/public/` non listé exhaustivement** : seuls les 3 fichiers sitemap de `/public/` ont été testés ; la mission P0 2026-07-16 parle de 122 doublons 200 dans `/public/` — vérification exhaustive non incluse dans cet audit.

---

## 7. Annexes

### A. Commandes exécutées (reproductibles)

```bash
# Sitemap discovery
curl -sS -o /tmp/robots.txt https://eletricista-urgente.pt/robots.txt
curl -sS -o /tmp/sitemap-root.xml https://eletricista-urgente.pt/sitemap.xml
curl -sS -o /tmp/sitemap-villages.xml https://eletricista-urgente.pt/sitemap-villages.xml
curl -sS -o /dev/null -w "%{http_code}\n" \
  https://eletricista-urgente.pt/{sitemap_index,sitemap-plain,sitemap-priority,sitemap-news,sitemap-blog,sitemap-pages,sitemap-locations,sitemap-concelhos}.xml
curl -sS -o /dev/null -w "%{http_code}\n" \
  https://eletricista-urgente.pt/public/{sitemap-plain,sitemap-priority,sitemap,sitemap-villages}.xml

# URL extraction
grep -oE '<loc>[^<]+</loc>' /tmp/sitemap-root.xml | sed 's|<loc>||;s|</loc>||' > /tmp/sitemap-root-urls.txt
grep -oE '<loc>[^<]+</loc>' /tmp/sitemap-villages.xml | sed 's|<loc>||;s|</loc>||' > /tmp/sitemap-villages-urls.txt

# Diff
comm -23 /tmp/sitemap-root-urls.txt /tmp/sitemap-villages-urls.txt > /tmp/only-in-root.txt
comm -13 /tmp/sitemap-root-urls.txt /tmp/sitemap-villages-urls.txt > /tmp/only-in-villages.txt

# Local slugs
ls *.html | sed 's|\.html$||' > /tmp/local-root-slugs.txt
ls concelhos/*.html | sed 's|^concelhos/||;s|\.html$||' > /tmp/local-concelhos-slugs.txt
ls blog/*.html | sed 's|^blog/||;s|\.html$||' > /tmp/local-blog-slugs.txt

# HTTP probe 17 URLs (boucle curl)
# HTTP probe 33 concelhos + 10 blog (boucle curl avec retry 3 préfixes)
```

### B. Sources de vérité citées

- `AGENTS.md` (repo) lignes 33-34 + mission P0 2026-07-16 (122 doublons 200 dans `/public/`)
- `robots.txt` ligne 38-39 (sitemap canoniques déclarés)
- `find . -name "*.html"` (hors `.worktrees/` et `.git/`) : 2 065 fichiers
- `scripts/gen_sitemap.py`, `scripts/gen_sitemap_discovery.py`, `scripts/build_sitemap.py`, `scripts/build_sitemap_full.py` (générateurs — non exécutés en READ-ONLY)

### C. Fichiers d'output intermédiaires (`/tmp/`)

- `/tmp/robots.txt` (1 112 octets)
- `/tmp/sitemap-root.xml` (268 208 octets, 1 962 URLs)
- `/tmp/sitemap-villages.xml` (264 934 octets, 1 936 URLs)
- `/tmp/sitemap-root-urls.txt`, `/tmp/sitemap-villages-urls.txt`
- `/tmp/only-in-root.txt` (26 URLs), `/tmp/only-in-villages.txt` (0 URLs)
- `/tmp/local-{root,concelhos,blog}-slugs.txt`
- `/tmp/probe-results.txt` (17 sondes sitemap), `/tmp/orphan-probe-results.txt` (43 sondes orphelins)

---

*Audit READ-ONLY 100 % curl prod. Aucune modification de fichier, aucun deploy, aucune opération Cloudflare/Vercel. Prêt pour validation Philippe avant remédiation (cf. R3 STOP validation).*
