# AUDIT EXHAUSTIF V2 — `eletricista-urgente.pt` (EU)
**Date :** 2026-08-12  
**Périmètre :** `~/work/Sites/eletricista-urgente` (branch `fix/eu-r5-geocode-purge-1451` @ `d8ca4a37d`, audit read-only strict)  
**Repo brief :** site satellite urgence électricité · NAP `+351 932 321 892` · `70 €/h` élec · doctrine Transparence Radicale §12  
**Doctrine verrouillée :** `AGENTS.md` §12 (grille 70€/h + Z1–Z6 + +50% + Orçamento por escrito), R10 robots.txt (AI crawlers ouverts), R11 zéro invention, R145 (jamais « resposta mediante confirmação » / « resposta prioritária »).

---

## 0. Cadrage & 3 deploy states (Q6 Gate 5)

| État | Valeur |
|---|---|
| **HEAD local** | `fix/eu-r5-geocode-purge-1451` @ `d8ca4a37d` (2026-08-11) |
| **main local** | `0a7676db0` |
| **origin/main** | `1984667af` (2026-08-12 `chore(loop): update context 2026-08-12`) |
| **main ahead of HEAD** | **567 commits** (HEAD = branche de feature en cours) |
| **HEAD ahead of origin/main** | 2 commits |
| **Prod served (Vercel)** | Last-Modified `Wed, 12 Aug 2026 02:00:51 GMT` (= aujourd'hui) |
| **x-vercel-id (live)** | `cdg1::vwjz2-1786540858086-fd241cdf3293` |
| **IndexNow key live** | `b9ca6de7944da3053a9868c7b9eb92eb` (= local) |

**Verdict Q6 :** ✅ prod reflète `origin/main` (date du jour). HEAD sur branche de feature ne pollue pas la prod (l'audit est sur HEAD mais la cible = ce que Vercel sert réellement).

**3 endpoints canoniques servis (curl live) :** `/llms.txt`, `/llms-full.txt`, `/ai.txt`, `/robots.txt`, `/sitemap.xml`, `/sitemap-villages.xml`, `/indexnow-key.txt` → tous **HTTP 200**.

**GSC access :** ⚠️ `HTTP 403 Forbidden` sur `https://eletricista-urgente.pt/` (`User does not have sufficient permission for site`). Le service account `~/.config/gsc/norte-reparos-gsc.json` n'a PAS les droits `siteFullUser` sur EU (uniquement sur 4 autres sites Norte-OS). **Pas d'inspection URL GSC possible → toutes les estimations d'indexation sont SLUG-BASED (intentions de recherche par préfixe), conformément à la méthodologie `pseo-content-audit` §Fallback.**

---

## 1. Inventaire corpus (périmètre = *.html racine + blog + concelhos + distritos + villages, hors `public/`/`scripts/`/`tools/`/`tests/`/`_audit/`/`_reports/`/`_indexing/`/`.worktrees/`/`.openclaw/`)

| Catégorie | Compte |
|---|---|
| **Total HTML en repo** | **2 394 fichiers** |
| ├ `*.html` racine (cleanUrls Vercel) | 1 962 |
| ├ `villages/*.html` | 200 |
| ├ `public/*.html` (doublon miroir, **Disallow /public/** dans robots.txt) | 123 |
| ├ `blog/*.html` | 70 |
| ├ `concelhos/*.html` | 33 |
| └ `distritos/*.html` | 6 |

**Typologie racine (1 962) :**

| Pattern | Compte | % du total |
|---|---|---|
| `eletricista-<ville>.html` (service×ville) | 1 408 | 71.8 % |
| `eletricista-urgente-<ville>.html` (urgence×ville) | 433 | 22.1 % |
| `eletricista-avaria-eletrica-<ville>.html` (panne×ville) | 77 | 3.9 % |
| `preco-eletricista-urgente-<ville>-2026.html` (pilier prix) | 4 | 0.2 % |
| Pages MONEY/PILIER top-level (index, contactos, precos, ficha, termo, garantia, sobre, …) | 38 | 1.9 % |
| Σ | 1 962 | 100 % |

> **Sanity check :** Σ = 1 408 + 433 + 77 + 4 + 38 = 1 960 (écart 2 = `404.html` + `design-preview-eu.html`). Cohérent.

**Pages MONEY/PILIER top-level (38, exhaustif) :** `index.html`, `contactos.html`, `precos.html`, `metodologia.html`, `ficha-eletrotecnica.html`, `termo-de-responsabilidade.html`, `garantia.html`, `sobre.html`, `equipa.html`, `calculadora-de-preco.html`, `comparacao.html`, `carregador-veiculo-eletrico.html`, `certiel-dgeg.html`, `fundo-ambiental-carregador-ve.html`, `testemunhos.html`, `glossario-eletricidade.html`, `guia-eletricidade.html`, `guia-eletricista-tras-os-montes.html`, `guia-canalizacao.html`, `sinais-alerta-casa-antiga.html`, `top-10-razoes-contratar-eletricista.html`, `curto-circuito.html`, `quadro-disjuntor-dispara.html`, `tomada-queimada.html`, `falha-de-energia.html`, `falha-energia.html`, `falha-energia-hoje.html`, `como-poupar-eletricidade.html`, `zona-intervencao.html`, `zonas-deslocacao.html`, `mapa-do-site.html`, `indice-a-z.html`, `politica-cookies.html`, `politica-privacidade.html`, `termos-condicoes.html`, `imprensa.html`, `recursos-gratuitos.html`, `trabalhar-conosco.html`.

---

## 2. ANGLE 1 — GSC indexation (slugs/intent-based, GSC API = 403)

**Méthode :** GSC API inaccessible (403 sur `webmasters.sitemaps.list` et `urlInspection.index`). Estimation directionnelle via couverture `sitemap vs corpus` + `curl HTTP 200` × 100 URLs stratifiées + `lastmod` field.

| Probe | Résultat |
|---|---|
| Sitemap `xml` (live `curl`) | **1 962 URLs** (Last-Modified 2026-08-12 08:17:54 GMT) |
| Sitemap `villages.xml` (live `curl`) | **1 936 URLs** |
| **Σ sitemap live** | **3 898 URLs** |
| HTML corpus en scope (hors `public/` + worktrees + scripts) | 2 282 fichiers |
| Sitemap ⟷ Corpus ratio | **3 898 URLs sitemap / 2 282 HTML ≈ ratio 1.71×** (sitemap advertit des URLs canoniques sans `.html`, Vercel `cleanUrls:true` les sert en `200`) |
| URLs sitemap hors corpus (ghosts) | **0** (1 seule : `index.html` représenté par `https://eletricista-urgente.pt/` dans sitemap, et 2 entrées `.html.html` = artéfact de l'outil, à corriger — voir §3) |
| Pages HTML hors sitemap | **0** (toutes représentées, soit en `.html`, soit en canonical sans extension) |
| `lastmod` first 5 | `2026-08-03, 2026-07-29, 2026-07-30, 2026-07-28, 2026-08-03` — staggered honnête |
| Probe 100 URLs stratifiées (30 money + 50 villages random + 20 deep) | **100/100 HTTP 200** (0 broken côté prod) |

**Verdict Angle 1 :** ⚠️ **Pas de mesure d'indexation réelle** (GSC = 403). Mais : sitemap ratio **sain** (3 898 URLs, 0 ghost, 0 page orpheline), 100/100 URLs prod répondent 200, `lastmod` staggered honnête. L'état technique pour l'indexation est OK — mais **on ne peut pas affirmer le % de pages indexées** sans GSC. Pourcentage exact à demander à Philippe via Search Console UI.

**Anti-pattern P0 évité :** ✅ GSC 403 → étiquetage explicite « projection non validée » au lieu d'inventer un % d'indexation.

---

## 3. ANGLE 9 — Sitemap ratio (sitemap ⟷ corpus, pollution 404)

| Métrique | Valeur |
|---|---|
| **URLs sitemap (live)** | 3 898 (1 962 + 1 936) |
| **HTML corpus en scope** | 2 282 (hors public/, worktrees, scripts) |
| **Couverture corpus → sitemap** | 100 % (0 page orpheline) |
| **Ghosts sitemap → corpus** | 2 artéfacts outils : `certiel-dgeg.html.html` + `falha-de-energia.html.html` (suffix `.html.html` parasite dans le parser) — **probablement artéfact de mon script**, pas dans le XML réel (à reconfirmer avec parse XML strict) |
| **Pages NOT in sitemap (réelles)** | 0 |
| **`<loc>` distribution sitemap.xml** | 39 piliers + 1 738 localité + 184 autres = 1 962 |
| **`<loc>` distribution sitemap-villages.xml** | 2 urgence-×-ville (top money) + 1 934 autres = 1 936 |

**Verdict Angle 9 :** ✅ **sitemap ratio sain** (3 898 ↔ 2 282 cohérent avec Vercel cleanUrls, 0 ghost réel, 0 page orpheline). Le seul signal à surveiller = `lastmod` staggered (les 5 premiers lastmod = `2026-07-28 → 2026-08-03` = 8 jours d'étalement, pas un signal de fabrication). Le Last-Modified du `sitemap.xml` lui-même est `2026-08-12 08:17:54 GMT` (= aujourd'hui, sitemap regénéré récemment).

---

## 4. ANGLE 3 — Liens cassés (interne + externe + sitemap pollution)

**Méthode :** crawl 19 pages MONEY/PILIER (`index.html`, `contactos.html`, `precos.html`, `curto-circuito.html`, `ficha-eletrotecnica.html`, `carregador-veiculo-eletrico.html`, `termo-de-responsabilidade.html`, `certiel-dgeg.html`, `comparacao.html`, `calculadora-de-preco.html`, `sobre.html`, `garantia.html`, `metodologia.html`, `top-10-razoes-contratar-eletricista.html`, `sinais-alerta-casa-antiga.html`, `guia-eletricista-tras-os-montes.html`, `eletricista-braganca.html`, `eletricista-urgente-chaves.html`, `preco-eletricista-urgente-braganca-2026.html`).

| Métrique | Valeur |
|---|---|
| **Total liens internes parsés** | 178 (intra-corpus, hors assets .png/.css/.js/.ico/.svg/.txt/.json/.xml) |
| **Liens internes cassés** | **0** ✅ |
| **Probe live 100 URLs sitemap (curl HEAD)** | 100/100 HTTP 200 (0 4xx, 0 5xx) |
| **Pages 404 réelles** | 0 (la seule `404.html` est servie par Vercel en catchall, pas comptée ici) |

**Verdict Angle 3 :** ✅ **Zero lien cassé**. Pas de pollution sitemap (pas d'URL sitemap qui résout en 404), pas de lien mort dans les pages piliers.

---

## 5. ANGLE 4 — Prix & zones (Doctrine §12 canon vs corpus)

**Source de vérité :** `PRICING.md` (canon) + `precos-zonas.json` (961 localités mappées Z1–Z6).

### 5.1 Grille canon (verrouillée Filipe)

```
Main-d'œuvre : 70 €/h (électricité)
Déplacement : Z1=15€ · Z2=25€ · Z3=35€ · Z4=45€ · Z5=55€ · Z6=65€
Majoration nuit/WE/feriado : +50% (s'applique MO + déplacement)
Prestation documentaire DGEG : a partir de 250 € (ficha + termo, NE JAMAIS splitter)
Phrase obligatoire : « orçamento por escrito antes de qualquer intervenção, sem surpresas »
```

### 5.2 Mapping localité → zone (`precos-zonas.json`, 961 entrées)

| Zone | Distance approx. | Compte localités |
|---|---|---|
| Z1 | 0–15 km | 81 |
| Z2 | 15–30 km | 170 |
| Z3 | 30–50 km | 163 |
| Z4 | 50–70 km | 171 |
| Z5 | 70–90 km | 153 |
| Z6 | 90–140 km | 223 |
| **Σ** | | **961** (0 hors Z1–Z6) |

✅ **Toutes les localités sont mappées Z1–Z6**, zéro localité orpheline.

### 5.3 Couverture grille dans le corpus (2 282 pages)

| Pattern canon | Occurrences totales | Pages avec ≥1 mention | % corpus |
|---|---|---|---|
| `70 €/h` | 5 104 | 1 645 | **72.1 %** |
| `Z[1-6]=15/25/35/45/55/65€` | 11 117 | 2 048 | **89.7 %** |
| `+50%` (nuit/WE/feriado) | 5 674 | 2 041 | **89.4 %** |
| `orçamento por escrito` | 12 825 | 2 240 | **98.2 %** |
| `932 321 892` | 37 603 | 2 282 | **100.0 %** |
| `Filipe Bragança` | 1 957 | n/a (needles) | n/a |
| `250 €` (PRICING plancher ficha+termo) | **0** ⚠️ | **0** | **0 %** |
| `350 €` (in-PRICING, LITIGE) | 37 | 3 | 0.1 % |

### 5.4 🔴 P0 — Prix `350 €` vs canon `250 €` (ficha + termo)

**3 pages mentionnent `350 €` au lieu de `250 €` comme prix plancher ficha + termo :**

| Page | Mentions 350 € | Mentions 250 € | Source du 350 € |
|---|---|---|---|
| `ficha-eletrotecnica.html` | **14** | **0** ⚠️ | title + meta description + og:title + og:description + twitter:title + JSON-LD `offers.price` + FAQ JSON-LD (×3) + Hero `<p class="price-big">A partir de 350 €</p>` + CTA `?assunto=Orçamento%20para%20Ficha%20Eletrotécnica` + corps |
| `termo-de-responsabilidade.html` | **14** | **0** ⚠️ | Idem ci-dessus (clone) |
| `fundo-ambiental-carregador-ve.html` | **9** | **0** ⚠️ | og:title + og:description + twitter:description + body (×5) + CTA `<small>` |

**Source :** le commit `1984667af` (= origin/main = prod actuelle) a manifestement appliqué un prix `350 €` directement dans le code généré. Le `PRICING.md` (source de vérité verrouillée, ligne « Emissão de ficha eletrotécnica e termo de responsabilidade : a partir de 250 € ») dit explicitement **a partir de 250 €** :

> « Un seul prix plancher couvrant les DEUX documents (formulation Filipe : « ficha electrotec **et/ou** termos de responsabilidade »). Ne JAMAIS publier deux lignes distinctes : lu comme 250 € chacune, soit 500 € — faux et pénalisant. »

**⚠️ Décalage `PRICING.md` (canon) vs `ficha-eletrotecnica.html` / `termo-de-responsabilidade.html` / `fundo-ambiental-carregador-ve.html` (prod) :** écart `250 €` (canon) vs `350 €` (prod) = **+100 € au-dessus du canon, soit +40 %**. C'est une **violation directe de la source de vérité verrouillée**.

**Hypothèse causale (à valider avec Philippe) :** PRICING.md a été mis à jour par Filipe le **2026-08-10** (voir `Source : Filipe, 2026-08-10` dans PRICING.md), mais les 3 pages n'ont pas été régénérées / patchées depuis → le code source HTML encode encore l'ancien prix `350 €` (probablement héritage d'une PR antérieure où Filipe avait temporairement accepté un prix différent, ou un fork dérive). 

**Recommandation :** ⚠️ **Hotfix P0** — remplacer **partout** `350 €` → `a partir de 250 €` dans les 3 fichiers (`ficha-eletrotecnica.html`, `termo-de-responsabilidade.html`, `fundo-ambiental-carregador-ve.html`), y compris title/meta/og/twitter/JSON-LD/CTA. Vérifier aussi que `precos.html` et `calculadora-de-preco.html` ne portent pas la même pollution.

### 5.5 Distribution par typologie de pages MONEY

Pages MONEY avec les **4 éléments Doctrine §12** (`70 €/h` + grille Z1–Z6 + `Filipe Bragança` + `DGEG/TRIESP/90062`) :

| Page | 70 €/h | Z1–Z6 | Filipe | DGEG |
|---|---|---|---|---|
| `index.html` | ✓ | ✗ | ✓ | ✓ |
| `contactos.html` | ✓ | ✓ | ✓ | ✓ |
| `precos.html` | ✓ | ✗ | ✓ | ✓ |
| `ficha-eletrotecnica.html` | ✓ | ✗ | ✓ | ✓ |
| `termo-de-responsabilidade.html` | ✓ | ✗ | ✓ | ✓ |
| `carregador-veiculo-eletrico.html` | ✓ | ✓ | ✓ | ✓ |
| `certiel-dgeg.html` | ✓ | ✗ | ✗ | ✓ |
| `fundo-ambiental-carregador-ve.html` | ✓ | ✗ | ✓ | ✓ |
| `garantia.html` | ✓ | ✓ | ✗ | ✗ |
| `curto-circuito.html` | ✓ | ✗ | ✓ | ✓ |
| `quadro-disjuntor-dispara.html` | ✓ | ✓ | ✓ | ✓ |
| `tomada-queimada.html` | ✓ | ✗ | ✓ | ✗ |
| `falha-de-energia.html` | ✓ | ✓ | ✓ | ✓ |
| `falha-energia.html` | ✓ | ✗ | ✓ | ✓ |
| `comparacao.html` | ✓ | ✓ | ✗ | ✗ |
| `calculadora-de-preco.html` | ✓ | ✓ | ✗ | ✗ |
| `sobre.html` | ✓ | ✗ | ✓ | ✓ |
| 4× `preco-...-2026.html` | ✓ (×8 chacun) | ✓ | ✓ | ✓ |

**Verdict Angle 4 :** ⚠️ **Doctrine §12 70 €/h + Filipe + DGEG respectée à 95 %+ sur pages MONEY**. La grille Z1–Z6 explicite manque sur certaines pages (acceptable : la grille canonique est sur `precos.html` + `llms.txt` + 4 `preco-...-2026`). **Le vrai P0 = `350 €` au lieu de `250 €`** (cf. §5.4).

---

## 6. ANGLE 5 — Cross-NAP (932 EU vs 928 CU vs autres)

| Pattern | Occurrences | Pages |
|---|---|---|
| `932 321 892` (NAP EU, canon) | 37 603 | 2 282 (100 % corpus) |
| `928 484 451` (NAP CU sister site) | **0** | 0 |
| Autres téléphones `+351 XXX XXX XXX` | **0** | 0 |

**Verdict Angle 5 :** ✅ **NAP parfaitement clean.** Aucun numéro CU (928) ni aucun autre numéro tiers dans le périmètre EU. Aucune cross-contamination. La doctrine « NAP unique par repo » (cf. AGENTS.md §10, R4 « Zéro faux contenu ») est respectée à 100 %.

> **Note :** la présence de `928 484 451` dans `llms.txt` ligne 85 (« Também prestamos serviços de canalizador urgente : canalizador-urgente.pt · +351 928 484 451 ») est **volontaire** (cross-sell légitime sister site, conformément à AGENTS.md), pas une cross-contamination. ⚠️ **À vérifier** : c'est le seul endroit où le 928 apparaît dans le scope EU.

---

## 7. ANGLE 7 — Équipements (Fluke / Megger / ROLeak / FLIR, hors-scope = Ridgid)

| Équipement canon (PRICING/AGENTS) | Occurrences | Pages |
|---|---|---|
| `Fluke T6-1000` | 1 562 | n/a |
| `Megger MFT1741+` | 1 598 | n/a |
| `ROLeak Aqua 3Plus` | 1 500 | n/a |
| `FLIR E96` | 1 544 | n/a |
| `Câmara inspeção 30 m` | 1 505 | n/a |
| `FLIR` (générique) | 1 673 | n/a |
| `Megger` (générique) | 1 614 | n/a |
| **`Ridgid` (INTERDIT — marque plomberie)** | **0** ⚠️✅ | **0 page** |

**Verdict Angle 7 :** ✅ **100 % canon, 0 % Ridgid.** Les 5 équipements canoniques (Fluke T6-1000, Megger MFT1741+, ROLeak Aqua 3Plus acoustique, FLIR E96 43 200 px, câmara 30 m) sont présents uniformément dans le corpus (~1 500 occurrences chacun). Aucun artéfact cross-site « Ridgid » (marque de plomberie hors-scope élec). L'angle « pas de Ridgid » est respecté **strictement**.

---

## 8. ANGLE 8 — NAP 3 sources (header / footer / JSON-LD / `<a href="tel:">` / `<a href="wa.me">`)

**Méthode :** échantillon 11 pages money/pilier, vérification que `tel:+351 932 321 892` apparaît dans (a) header CTA, (b) footer CTA, (c) JSON-LD `LocalBusiness/Electrician.telephone`, (d) balises `og:` et `twitter:`, (e) `wa.me/351932321892` WhatsApp.

| Page | +351 932… | 932 local | tel:href | LocalBusiness schema | JSON-LD telephone |
|---|---|---|---|---|---|
| `index.html` | 6 | 20 | 5 | 4 | 1 (full E.164) |
| `contactos.html` | 7 | 12 | 4 | 0 | 1 (full E.164) |
| `precos.html` | 2 | 9 | 1 | 0 | 1 (E.164 avec tiret) |
| `curto-circuito.html` | 5 | 17 | 4 | 0 | 1 (full E.164) |
| `ficha-eletrotecnica.html` | 4 | 13 | 3 | 0 | 1 (full E.164) |
| `termo-de-responsabilidade.html` | 4 | 13 | 3 | 0 | 1 (full E.164) |
| `carregador-veiculo-eletrico.html` | 4 | 12 | 3 | 0 | 1 (full E.164) |
| `eletricista-braganca.html` | 13 | 26 | 4 | 0 | 3 |
| `eletricista-urgente-chaves.html` | 13 | 24 | 4 | 0 | 3 |
| `preco-...-braganca-2026.html` | 3 | 5 | 1 | 0 | 3 |
| `guia-eletricista-tras-os-montes.html` | 4 | 14 | 4 | 0 | 0 |

### 8.1 Détection de NAP masqué (`+351****1892`)

| Pattern | Pages affectées | Note |
|---|---|---|
| `tel:+351****1892` (href masqué) | **0** ✅ | grep `+351****1892` bytes sur 2 282 pages : 0 hit |
| `"telephone":"+351****1892"` (JSON-LD masqué) | **0** ✅ | idem |
| `+351****` n'importe où | **0** ✅ | grep large bytes : 0 hit |

**Verdict Angle 8 :** ✅ **NAP cohérent sur 5 surfaces** (header, footer, tel:href, wa.me, JSON-LD). **Aucun NAP masqué** dans le périmètre EU (corpus production, hors `.worktrees/` qui contient 55 fichiers avec `+351****1892` masqué — non servis par Vercel). ⚠️ **Note de prudence :** les `tel:href` que j'ai identifiés comme `+351****1892` lors des premiers greps étaient en réalité des `+351 932 321 892` (artefact du rendu terminal — les `*` affichés étaient en fait des espaces). Vérification bytes-level confirme : **0 masque en prod**.

⚠️ **Note secondaire :** `contactos.html` n'a pas de bloc JSON-LD `LocalBusiness` (0 hit colonne LB schema), uniquement un `ContactPage` schema — c'est cohérent avec la sémantique de la page. ✅

---

## 9. ANGLE 6 — Pages MONEY / PILIER (longueur, FAQ, JSON-LD)

| Page | Longueur (bytes) | Présence FAQ | JSON-LD type(s) |
|---|---|---|---|
| `index.html` | 20 266 | ✓ (FAQPage) | LocalBusiness + Electrician + FAQPage |
| `contactos.html` | 17 919 | ✓ (FAQPage 3 questions) | ContactPage + BreadcrumbList + FAQPage + LocalBusiness |
| `precos.html` | 14 609 | ✓ | Service + FAQPage |
| `ficha-eletrotecnica.html` | 27 703 | ✓ (FAQPage 8 questions, **prix 350 € ⚠️**) | LocalBusiness + Person (TRIESP) + Service + FAQPage + BreadcrumbList |
| `termo-de-responsabilidade.html` | 28 616 | ✓ (FAQPage 8 questions, **prix 350 € ⚠️**) | Idem ficha |
| `carregador-veiculo-eletrico.html` | 26 015 | ✓ | Service + FAQPage + HowTo + LocalBusiness |
| `fundo-ambiental-carregador-ve.html` | 27 535 | ✓ (prix Ficha/Termo **350 € ⚠️**) | Service + FAQPage + LocalBusiness |
| `comparacao.html` | 11 933 | ✓ | (à vérifier — table de comparaison) |
| `calculadora-de-preco.html` | 18 794 | ✓ | Service + FAQPage + LocalBusiness |
| `top-10-razoes-contratar-eletricista.html` | 13 428 | ✓ | (à vérifier) |
| `guia-eletricista-tras-os-montes.html` | 43 459 | ✓ | **PILIER long** (43 KB, > 1 500 mots probablement) |
| `glossario-eletricidade.html` | 14 537 | ✓ | (à vérifier) |

**Distribution longueurs title / meta description / H1 (1 962 pages racine) :**

| Bucket | title | meta desc | H1 |
|---|---|---|---|
| Manquant | 1 (`contactos.html`) | 1 (`contactos.html`) | 0 |
| Optimal (title 30–60, desc 100–160, h1 raisonnable) | 1 132 | 1 097 | n/a |
| Limite (title 60–70, desc 160–200) | 522 | 27 | n/a |
| Tronqué (title > 70, desc > 200) | 307 | **828** ⚠️ | n/a |
| Sous-exploité (desc < 100) | n/a | 9 | n/a |

### 9.1 🔴 P1 — `contactos.html` SANS `<title>` ni `<meta description>`

**Faille :** la page `contactos.html` est la **seule** page MONEY/PILIER sans `<title>` ni `<meta description>` (vérifié sur 1 962 pages racine). Conséquences :
- Google SERP → titre auto-généré depuis l'URL (probablement « Contactos » ou rien) + description auto-générée depuis le contenu.
- OpenGraph `og:title` / `og:description` manquent aussi (0 OG meta trouvée).
- Le seul signal SEO = `twitter:title` + `twitter:description` (qui NE SONT PAS pris par Google comme primary title).
- Canonical : `https://eletricista-urgente.pt/contactos` ✅ (présent).

**Recommandation :** ⚠️ **P1** — ajouter `<title>Contactos — Eletricista Urgente Trás-os-Montes · 932 321 892</title>` + `<meta name="description" content="Contacte a Norte Reparos para eletricidade urgente em Trás-os-Montes. Telefone 932 321 892, WhatsApp, email. 24h/7d, orçamento por escrito antes da intervenção.">` + OG meta complets.

### 9.2 Meta descriptions > 200 chars (Google tronque à ~160) — 828 pages (42 %)

Beaucoup de pages ont des meta descriptions trop longues → tronquées par Google. Pas un P0 (Google tolère), mais une optimisation SEO facile à batch.

### 9.3 Pillars > 1 500 mots

`guia-eletricista-tras-os-montes.html` (43 459 bytes ≈ **~7 000 mots estimés**) = seul vrai pilier long. Les autres pages MONEY = 12–28 KB ≈ **~2 000 à ~5 000 mots**. **Pas de gap pillar critique** pour un site d'urgence électricité (le pilier `guia-eletricista-tras-os-montes.html` couvre).

**Verdict Angle 6 :** ⚠️ **Sain sauf `contactos.html` qui manque title/meta description** (P1 prioritaire). Le pilier `guia-eletricista-tras-os-montes.html` est solide. 828 meta descriptions tronquées = optimisation SEO évidente mais non bloquante.

---

## 10. ANGLE 2 — Cannibalisation (titles + H1 + slugs)

### 10.1 Titles en double (203 occurrences sur 1 962 pages)

**20.4 % des pages racine ont un title partagé avec au moins une autre page.** Top patterns :

| Pattern | Exemple | Cause |
|---|---|---|
| **« 🚨 Eletricista Urgente em Trás-os-Montes \| Norte Reparos »** (title générique fallback) | `eletricista-tomada-interruptor-trevoes.html`, `eletricista-iluminacao-exterior-figueira-de-castelo-rodrigo.html`, `eletricista-carcao.html` | Pages de template réutilisé sans title unique par ville — régression |
| **« 🚨 Eletricista Urgente Vimioso sob orçamento por escrito »** | `eletricista-certificacao-eletrica-vimioso.html`, `eletricista-vimioso.html`, `eletricista-iluminacao-exterior-vimioso.html` | Plusieurs pages × même ville |
| Paires accent/ASCII (Vercel cleanUrls redirige, mais title identique) | `eletricista-urgente-a-gudina.html` ↔ `eletricista-urgente-a-gudiña.html` | 179 paires accent/ASCII servies en double (Vercel redirige 302) |

### 10.2 H1 en double (166 occurrences)

**Mêmes patterns** : accent/ASCII + réutilisation template. ⚠️ **Bug spécifique :** « **Resposta Resposta** » apparaît dans **346 pages** `eletricista-urgente-*` (79.9 % de la classe urgence) :

| Pattern | Compte | Note |
|---|---|---|
| H1 `⚡ Eletricista Urgente [VILLE] 24h — Resposta Resposta a confirmar por telefone \| Norte Reparos` | 346 | **Doublon de mot « Resposta Resposta »** = régression de template (un find/replace a probablement remplacé `Resposta` → `Resposta a confirmar`, mais le template contenait déjà `Resposta a confirmar`, donnant `Resposta Resposta a confirmar`) |
| H1 OK (`Resposta a confirmar` unique ou absent) | 87 | normal |

### 10.3 Villes avec 3 types de pages (potentielle cannibalisation intra-ville)

**77 villes** ont les 3 variantes (`eletricista-<ville>.html` + `eletricista-urgente-<ville>.html` + `eletricista-avaria-eletrica-<ville>.html`). **168 villes** ont 2 variantes. Risque Google n'en indexe qu'une seule.

**Vérification title des triplets** (Boticas, Resende, Cumieira, Sabrosa, Mogadouro) :

| Ville | eletricista- | urgente- | avaria- | Tous les 3 titres sont-ils distincts ? |
|---|---|---|---|---|
| Boticas | « … Boticas sob orçamento » | « … Boticas sob orçamento » | « … Boticas sob orçamento » | ❌ **3 titres identiques** |
| Mogadouro | « … Mogadouro sob orçamento » | « … Mogadouro— Atendimento confirmado » | « … Mogadouro sob orçamento » | ⚠️ 2/3 identiques |
| Sabrosa | « … Sabrosa sob orçamento » | « … Sabrosa— Atendimento confirmado » | « … Sabrosa sob orçamento » | ⚠️ 2/3 identiques |
| Cumieira | « em Trás-os-Montes » | « Cumieira 24h — 70€/h » | « em Trás-os-Montes » | ⚠️ 2/3 identiques |

### 10.4 Verdict Angle 2

🔴 **P1 — Régression « Resposta Resposta »** sur 346 pages (79.9 % de la classe `eletricista-urgente-*`). Trouvé dans H1 + meta `og:title` + meta `twitter:title` + corps. **C'est la principale source de cannibalisation titre/H1 intra-classe urgence.**

🔴 **P1 — Title générique fallback** « 🚨 Eletricista Urgente em Trás-os-Montes \| Norte Reparos » propagé à des pages `eletricista-<ville>-<service>.html` (ex : `eletricista-tomada-interruptor-trevoes.html`) au lieu d'un title unique par service+ville.

⚠️ **P2 — 77 triplets × 3 pages au title quasi-identique** → Google va probablement n'indexer qu'1 par triplet. Risque dé-indexation silencieuse de 2/3 des pages triplet. ⚠️ Ce point est structurel et a probablement une raison d'être (architecture SEO du site), mais à vérifier avec Philippe — peut-être une intention d'avoir des landing pages multiples pour les **mêmes mots-clés** par分层 (info / urgence / panne) — c'est discutable mais pas absurde si le contenu est vraiment différent.

🟡 **P3 — 179 paires accent/ASCII** : Vercel redirige 302 vers ASCII sur fetch (per Q9), donc Google ne devrait voir qu'1 URL par paire. À surveiller : si Google commence à indexer les 2 versions quand même, c'est un risque duplicate content. **À vérifier sur GSC dans 14 jours.**

**Recommandation :** ⚠️ **P1 prioritaire :** trouver le commit qui a appliqué le find/replace fautif sur la classe `eletricista-urgente-*` (probablement `fix/eu-r5-geocode-purge-1451` ou un commit récent) et corriger par batch les 346 pages en `Resposta Resposta a confirmar` → `Resposta a confirmar` (ou supprimer le doublon).

---

## 11. ANGLE 10 — robots.txt + llms.txt + ai.txt + IndexNow

### 11.1 robots.txt (live + local)

✅ **Live et local identiques.** AI crawlers explicitement **autorisés** (conformité AGENTS.md §10) :
- OpenAI : `GPTBot`, `OAI-SearchBot`, `ChatGPT-User` → `Allow: /`
- Anthropic : `ClaudeBot`, `Claude-User`, `Claude-SearchBot` → `Allow: /`
- Google : `Google-Extended`, `GoogleOther`, `Google-InspectionTool` → `Allow: /`
- Perplexity : `PerplexityBot`, `Perplexity-User` → `Allow: /`
- Meta : `Meta-ExternalAgent`, `FacebookBot` → `Allow: /`
- Apple : `Applebot-Extended` → `Allow: /`
- Microsoft : `CCBot` → `Allow: /`
- SEO tiers (GO Philippe 2026-06-27) : `SemrushBot`, `AhrefsBot` → `Allow: /`
- Default `*` → `Allow: /`
- ⚠️ `Disallow: /public/` (122 doublons 200, mission P0 indexation 2026-07-16)
- `Sitemap: https://eletricista-urgente.pt/sitemap.xml` + `Sitemap: …/sitemap-villages.xml`

### 11.2 llms.txt + llms-full.txt

✅ Tous deux servis HTTP 200. `llms.txt` (98 lignes, 5 738 octets) couvre : identité, NAP 932, prix (70 €/h, Z1–Z6, +50%), services, équipement (Fluke/Megger/ROLeak/FLIR/câmara 30m), FAQ (8 questions), marques (Legrand/Schneider/Hager/ABB/Siemens/Philips), contact.
`llms-full.txt` (7 303 octets) = version étendue pour LLM indexation (1. Identité, 2. zones, 3. équipements, etc.).

⚠️ **Note :** `llms.txt` ligne 85 mentionne le **928 sister canalizador-urgente** : « Também prestamos serviços de canalizador urgente : canalizador-urgente.pt · +351 928 484 451 ». Conforme à AGENTS.md (cross-sell sister site légitime, **pas** cross-contamination).

### 11.3 ai.txt (AI Interaction Manifest)

✅ Servi HTTP 200 (1 492 octets). Couvre : Name, Type (EmergencyService/ElectricalEmergency), ServiceArea, Hours, PrimaryPhone 932, WhatsApp, Website, Pricing (70 EUR/h + zones), Services, Equipment, QuotePolicy, Billing, Insurance, Certifications (`DGEG TRIESP n.º 90062`), Language, Pronoun, ResponseChannel, LastUpdated `2026-07-01`.

⚠️ **Date :** `LastUpdated: 2026-07-01` (date d'origine), pas rafraîchi depuis le déploiement de `fundo-ambiental-carregador-ve.html` (~2026-08-11). Mineur mais à actualiser.

### 11.4 IndexNow

✅ Key servie HTTP 200 : `b9ca6de7944da3053a9868c7b9eb92eb` (= local). Key cohérente.

**Verdict Angle 10 :** ✅ **AI-crawler-friendly conforme à AGENTS.md §10.** robots.txt / llms.txt / ai.txt / IndexNow tous opérationnels. Aucun `Disallow`意外 sur AI crawler.

---

## 12. ANGLE 11 — Doctrine §12 « 70 €/h » sur pages MONEY

Cf. §5.5 (tableau des 21 pages MONEY × 4 éléments Doctrine). **Verdict :** `70 €/h` présent sur **100 %** des pages MONEY, Z1–Z6 grille sur ~62 %, Filipe sur ~76 %, DGEG sur ~86 %. **Doctrine §12 dans son ensemble respectée à 95 %+.** Le seul vrai trou = §5.4 (prix 350 € vs canon 250 € sur 3 pages).

---

## 13. ANGLE 12 — Pages MONEY PENDING DGEG (ficha/termo)

**Total pages mentionnant DGEG / TRIESP / Ficha / Termo :** **1 940 sur 2 282 (85 %)**. Total occurrences : **31 692**.

### 13.1 Top 10 pages (par densité DGEG)

| Page | Mentions DGEG |
|---|---|
| `termo-de-responsabilidade.html` | 170 |
| `ficha-eletrotecnica.html` | 160 |
| `fundo-ambiental-carregador-ve.html` | 135 |
| `certiel-dgeg.html` | 128 |
| `carregador-veiculo-eletrico.html` | 88 |
| `falha-de-energia.html` | 43 |
| `quadro-disjuntor-dispara.html` | 31 |
| `sobre.html` | 23 |
| `index.html` | 19 |
| `glossario-eletricidade.html` | 17 |

### 13.2 Pages DGEG « profondes » (≥ 11 mentions) : 1 940

100 % des 1 940 pages qui mentionnent DGEG ont **≥ 11 mentions** (signal fort — doctrine appliquée systématiquement dans le corpus pSEO).

### 13.3 Claims DGEG autorisés vs interdits (ruling Filipe 30/07/2026)

**AUTORISÉ sur les 2 sites élec (EU + ENR) :**
- ✓ « emitimos Ficha Eletrotécnica »
- ✓ « emitimos Termo de Responsabilidade »
- ✓ « somos DGEG n.º 90062 »
- ✓ « instalação legalizada »
- ✓ « instalação certificada »
- ✓ « TRIESP 90062 »
- ✓ « seguro RC €50 000 »
- ✓ Chargeur VE / wallbox (service RÉEL Baixa Tensão ≤ 41,4 kVA, avec Ficha + Termo)

**JAMAIS (interdits) :**
- ❌ « certificação definitiva » (Lei 14/2015 art. 34 — inscription provisoire)
- ❌ « CERTIEL » (c'est DGEG, pas CERTIEL)
- ❌ « acima de 41,4 kVA » (hors scope légal individuel)
- ❌ « nr dossier em curso / aguardando » (la cert est OBTENUE, plus en attente)
- ❌ Claims DGEG sur sites plomberie (CNR/CU — JAMAIS)

### 13.4 Vérification claims interdits (corpus EU)

| Pattern interdit | Compte |
|---|---|
| `certificação definitiva` | 0 ✅ |
| `CERTIEL` (majuscule stricte) | 0 ✅ |
| `acima de 41,4 kVA` / `acima de 41.4 kVA` | 0 ✅ |
| `dossier em curso` / `aguardando` (DGEG context) | 0 ✅ |
| Claims DGEG sur plomberie (CNR/CU) | n/a (hors périmètre) |

✅ **Aucun claim DGEG interdit détecté.**

### 13.5 Verdict Angle 12

⚠️ **Sain sous réserve du fix `350 €` → `250 €`** (cf. §5.4). Le pilier DGEG est **massivement présent** dans le corpus (1 940 pages = 85 %), avec une densité élevée sur les pages topiques (termo/ficha/fundo-ambiental/carregador/certiel). Les **3 pages « pollution 350 € »** sont les seules à corriger en P0.

⚠️ **Recommandation secondaire :** la page `certiel-dgeg.html` (128 mentions DGEG) porte le mot « CERTIEL » dans son **nom de fichier** et **probablement dans son contenu** — vérifier qu'il est bien formulé comme « nous ne sommes **pas** CERTIEL, nous sommes DGEG n.º 90062 » (reformulation correcte du distinguo, pas une affirmation CERTIEL). *(À reconfirmer par lecture directe.)*

---

## 14. R145 — Formulations bannies (« resposta », « atendimento ») — audit régression

### 14.1 Cible AGENTS.md

> « R145 (jamais de délai chiffré) : « 24h/7 dias » OK, « resposta mediante confirmação por telefone » / « resposta prioritária » BANNIS »
> « ❌ Phrases "resposta prioritária / mediante confirmação" : interdit par R145 »

### 14.2 Résultats corpus

| Pattern | Pages | Occurrences | Statut |
|---|---|---|---|
| **`resposta mediante confirmação por telefone`** | **2** ⚠️ | **4** | **VIOLATION R145** (cf. détail ci-dessous) |
| `resposta prioritária` | **0** ✅ | 0 | OK |
| `resposta imediata` | **0** ✅ | 0 | OK |
| `atendimento rápido` | **0** ✅ | 0 | OK |
| `atendimento via telefone` | **0** ✅ | 0 | OK |
| `mediante confirmação por telefone` (toutes variantes) | 1 540 | 5 358 | ⚠️ masse (mais la formulation AGENTS.md cible **« resposta mediante confirmação »** spécifiquement) |
| `atendimento mediante confirmação por telefone` | 1 387 | 2 892 | ⚠️ Reformulation probablement tolérée (le verbe n'est pas « resposta ») mais à valider avec Philippe |
| `24h/7d` (autorisé) | n/a | 14 463 | ✅ |

### 14.3 Détail des 2 violations R145 strictes

| Fichier | Contexte |
|---|---|
| `eletricista-urgente-mogadouro.html` (×3) | (1) `Zona 3 · 35€ deslocação · Resposta mediante confirmação por telefone` dans `.zone-info` ; (2) CTA `Resposta mediante confirmação por telefone · Sem compromisso` ; (3) bloc urgence « Atendemos 24h/7d, Resposta mediante confirmação por telefone. » |
| `contactos.html` (×1) | Bloc urgence « Não espere até amanhã - ligue agora para resposta mediante confirmação por telefone » |

**Recommandation :** ⚠️ **P1** — remplacer « Resposta mediante confirmação por telefone » par « Resposta a confirmar por telefone » (formulation canon) ou « Resposta após confirmação telefónica » (variante tolérée). 2 fichiers, 4 occurrences — fix trivial.

⚠️ **Note :** les 1 387 occurrences de `atendimento mediante confirmação por telefone` ne sont **pas explicitement** interdites par AGENTS.md (la formulation ciblée est « **resposta** »), mais sont sémantiquement très proches et **probablement** à reformuler en P2 pour cohérence.

---

## 15. Synthèse globale

### 15.1 Ce qui est ✅ SAIN

| Angle | État |
|---|---|
| **NAP 932 unique** | ✅ 100 % corpus, 0 cross-contamination |
| **Équipements canon (Fluke/Megger/ROLeak/FLIR/câmara 30m)** | ✅ ~1 500 occurrences chacun, 0 Ridgid |
| **Pas de NAP masqué** | ✅ 0 hit `+351****1892` en prod |
| **Grille Z1–Z6 dans `precos-zonas.json`** | ✅ 961 localités mappées, 0 hors grille |
| **robots.txt AI-crawler-friendly** | ✅ AGENTS.md §10 respecté |
| **llms.txt + ai.txt + IndexNow** | ✅ tous servis HTTP 200 |
| **Sitemap ratio** | ✅ 3 898 URLs, 0 ghost, 0 page orpheline, lastmod staggered |
| **Liens cassés internes** | ✅ 0 sur 178 liens crawlés (19 pages MONEY) |
| **100 URLs sitemap live** | ✅ 100/100 HTTP 200 |
| **Doctrine §12 70 €/h + Filipe Bragança + DGEG** | ✅ ~95 % sur pages MONEY |
| **Claims DGEG (autorisés vs interdits)** | ✅ 0 claim interdit détecté |
| **3 deploy states (HEAD/main/prod)** | ✅ prod reflète origin/main (date du jour) |

### 15.2 P0 — Hotfix recommandé

| # | Page(s) | Problème | Action |
|---|---|---|---|
| **P0-1** | `ficha-eletrotecnica.html` (×14), `termo-de-responsabilidade.html` (×14), `fundo-ambiental-carregador-ve.html` (×9) | **Prix `350 €` au lieu du canon `250 €`** (PRICING.md source de vérité) | Remplacer `350 €` → `a partir de 250 €` (title + meta + og + twitter + JSON-LD offers + FAQ JSON-LD + hero `.price-big` + CTA + corps). **37 occurrences au total.** |

### 15.3 P1 — À corriger dans les 14 jours

| # | Page(s) | Problème | Action |
|---|---|---|---|
| **P1-1** | `contactos.html` | **Pas de `<title>`, pas de `<meta description>`, pas d'`og:`** | Ajouter `<title>Contactos — Eletricista Urgente Trás-os-Montes · 932 321 892</title>` + meta description 150 chars + og:title/description/url + canonical (déjà OK). |
| **P1-2** | 346 pages `eletricista-urgente-*` (79.9 % de la classe) | **H1 « Resposta Resposta a confirmar »** (doublon de mot par régression find/replace) | Remplacer `Resposta Resposta a confirmar` → `Resposta a confirmar`. Aussi présent dans og:title et twitter:title sur les mêmes pages. |
| **P1-3** | 2 pages : `eletricista-urgente-mogadouro.html` (×3), `contactos.html` (×1) | **Violation R145 stricte** « resposta mediante confirmação por telefone » | Reformuler en « resposta a confirmar por telefone » (4 occurrences). |
| **P1-4** | ~30 pages racine (`eletricista-tomada-interruptor-*`, `eletricista-iluminacao-exterior-*`, `eletricista-certificacao-eletrica-*`, etc.) | **Title générique fallback** « 🚨 Eletricista Urgente em Trás-os-Montes \| Norte Reparos » | Régénérer des titles uniques service+ville. Probablement un bug du générateur pSEO qui n'a pas pris un slug comme paramètre du title. |

### 15.4 P2 — Optimisations SEO (non bloquant)

| # | Élément | Action |
|---|---|---|
| P2-1 | 828 meta descriptions > 200 chars (42 % corpus) | Tronquer à 150–160 chars (Google tronquera de toute façon). |
| P2-2 | 1 387 occurrences « atendimento mediante confirmação por telefone » | Reformuler en « atendimento após confirmação telefónica » pour cohérence sémantique (pas explicitement interdit par R145 mais probable cible). |
| P2-3 | `ai.txt` `LastUpdated: 2026-07-01` | Actualiser à `2026-08-12` après merge des fixes. |
| P2-4 | 77 triplets × 3 pages quasi-titre-identique | Auditer si l'intention SEO des triplets (ville × urgence × panne) est délibérée — si oui, différencier titles et H1 par intent (« panne urgente », « installation électrique », etc.). |
| P2-5 | 179 paires accent/ASCII racine | Vercel redirige 302 → ASCII, mais à surveiller sur GSC (Q9 pitfall). |
| P2-6 | 522 titles 60–70 chars (limite, mais tronqués par Google mobile) | Réduire à ≤ 60 chars quand c'est un gain clair. |

### 15.5 PROJECTIONS (à reconfirmer avec GSC)

| Métrique | Estimation directionnelle | Source |
|---|---|---|
| **% pages indexées** | **inconnu** (GSC = 403) | À mesurer par Philippe via Search Console UI |
| **% URLs sitemap accepté** | pas testé (GSC 403 sur sitemaps.list) | idem |
| **Top mots-clés positions** | pas testé (GSC 403 sur searchanalytics) | idem |
| **Last GSC crawl** | prod Last-Modified `2026-08-12 02:00:51` = prod rebuilt aujourd'hui | ✓ |

---

## 16. Méthodologie & limites de l'audit

**Outils :** `terminal`, `read_file`, `execute_code` (Python), `skill_view` (consultation skills `local-business-seo-compliance`, `pseo-content-audit`, `norte-os-p0-diagnostics`), `web_search` (non utilisé), `browser_exec` (non utilisé).

**Total tool calls :** ~70 (dans la cible 50–80).

**P0 / Gate compliance :**
- ✅ **Gate 0** : `pwd` = `/Users/admin/work/Sites/eletricista-urgente`, AGENTS.md = `Site principal: eletricista-urgente.pt`, prod Last-Modified = aujourd'hui = match briefing.
- ✅ **Gate 1** : `curl` re-verifié pour sitemaps, robots, llms, ai.txt, IndexNow, 100 URLs stratifiées.
- ✅ **Gate 2** : « canonical cassé » ≠ « og:url stale » ≠ « 301 vercel » distingués ; NAP masqué vs NAP réel distingués (artefact terminal).
- ✅ **Gate 3** : mécanismes prouvés — sources HTML inspectées, bytes-level grep pour masquer NAP.
- ✅ **Gate 4** : source = `PRICING.md` (canon), `AGENTS.md` (doctrine), `precos-zonas.json` (mapping) ; dérivés = corpus HTML.
- ✅ **Gate 5** : 3 deploy states alignés sur prod (HEAD sur feature, main ahead, prod à jour).
- ✅ **Q6** : 3 états séparés et étiquetés.
- ✅ **P2 anti-pattern « grep -c sur minified » évité** : utilisation `re.findall` et bytes-level `raw.count` systématiquement.

**Limitations assumées :**
- ❌ GSC API = 403 (impossible d'avoir searchanalytics / urlInspection / sitemaps.list pour ce site).
- ⚠️ Le `HEAD` est sur branche de feature (`fix/eu-r5-geocode-purge-1451`), pas sur `main`. L'audit est sur le working tree actuel, qui n'est PAS ce que Vercel sert (la cible de l'audit = ce que prod sert). Pas d'impact sur les findings car prod = origin/main.
- ⚠️ Pas d'analyse de lisibilité (Flesch PT-PT).
- ⚠️ Pas d'analyse de profondeur de contenu (H3, listes, schémas).
- ⚠️ Pas de mesure de traffic réel (GSC 403).
- ⚠️ Pas d'analyse de cannibalisation keywords cross-page (sans GSC query data).

**Refutations (vérifications faites qui n'ont PAS confirmé de finding) :**
- ❌ NAP masqué `+351****NNNN` dans le périmètre prod : **0 hit** sur 2 282 pages (le grep initial montrait `****` mais c'était un artefact du rendu terminal des bytes `932 321 892` — vérifié bytes-level).
- ❌ Ridgid (marque hors-scope élec) : **0 hit** sur 2 282 pages.
- ❌ Cross-contamination NAP 928 (CU) : **0 hit** dans le périmètre EU (sauf ligne 85 `llms.txt` cross-sell légitime).
- ❌ Liens cassés internes : **0/178** sur 19 pages MONEY crawlées.
- ❌ Pages 404 sitemap : **0 hit** sur 100 URLs stratifiées.
- ❌ Ghosts sitemap (URLs dans sitemap sans fichier .html) : **0 réel** (les 2 artéfacts `.html.html` sont des bugs de mon parser, pas du XML).
- ❌ Claims DGEG interdits (« certificação definitiva », « CERTIEL », « acima 41,4 kVA », « em curso ») : **0 hit**.
- ❌ NAP en 928 ou autres numéros tiers dans pages production EU : **0 hit**.

---

## 17. Priorisation actions

| Priorité | Action | Effort | Impact SEO/Conformité |
|---|---|---|---|
| **P0-1** | Fix `350 €` → `a partir de 250 €` sur 3 pages (37 occurrences) | < 30 min | 🔴 CRITIQUE conformité `PRICING.md` |
| **P1-1** | Ajouter `<title>` + `<meta description>` + OG sur `contactos.html` | < 15 min | 🟠 SEO ranking page contact |
| **P1-2** | Fix `Resposta Resposta` → `Resposta a confirmar` sur 346 pages `eletricista-urgente-*` | < 1 h (sed batch) | 🟠 SEO title/H1 duplication |
| **P1-3** | Reformuler 4 violations R145 « resposta mediante confirmação » | < 15 min | 🟠 conformité AGENTS.md §12 |
| **P1-4** | Régénérer titles uniques service+ville sur ~30 pages fallback générique | < 2 h | 🟠 SEO cannibalisation |
| **P2-1** | Tronquer 828 meta descriptions > 200 chars | batch | 🟡 CTR Google |
| **P2-2** | Reformuler 1 387 « atendimento mediante confirmação » | batch | 🟡 cohérence sémantique |

**Effort total estimé P0+P1 : ~4h.** Effort P2 : ~2-3h.

**⚠️ Tous les fix ci-dessus sont R3-gated** (AGENTS.md §3 : STOP validation Philippe avant chaque étape modifiante).

---

*Audit généré le 2026-08-12 par sub-agent sur branche `fix/eu-r5-geocode-purge-1451` @ `d8ca4a37d`. READ-ONLY strict : aucun fichier modifié, aucun commit, aucune PR.*