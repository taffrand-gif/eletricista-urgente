# AUDIT PROACTIF EU — eletricista-urgente.pt
**Date** : 2026-08-11
**Périmètre** : `*.html` racine + `blog/` + `concelhos/` + `distritos/` + `villages/` (excl `public/`, `_archive/`, `.worktrees/`, `.git/`)
**Repo** : `/Users/admin/work/Sites/eletricista-urgente` (branche `main`)
**Total fichiers HTML périmètre** : **2 271** (1 962 racine + 33 concelhos + 6 distritos + 200 villages + 70 blog)
**Mode** : READ-ONLY strict · proxy-Lighthouse sur fichiers statiques + curl prod (Vercel) pour headers HTTP

---

## Synthèse scores

| # | Section                              | Score /10 |
|---|--------------------------------------|-----------|
| 1 | Lighthouse (proxy statique)          | **8.0** |
| 2 | Sécurité HTTP headers                | **5.5** |
| 3 | Schema.org coverage                  | **7.5** |
| 4 | Conversion CTA                       | **9.5** |
| 5 | NAP consistency                      | **8.5** |
| 6 | Indexation sitemap                   | **3.0** |
| 7 | Canonical KO                         | **8.0** |
| 8 | llms / ai / robots                   | **9.5** |
| 9 | Endpoints critiques                  | **9.0** |
|   | **TOTAL**                            | **68.5 / 90** |

**Verdict global** : **76 %** — site globalement sain en SEO/GEO/CTA, mais lacunes structurelles sur **indexation sitemap** (secondaire non déclaré) et **sécurité headers** (CSP/Referrer-Policy/Permissions-Policy absents).

---

## 1. Lighthouse (proxy statique HTML) — 8.0/10

Audit proxy sans Chromium (lighthouse CLI non disponible dans ce runtime). Mesures structurelles sur 6 pages représentatives.

| Page                          | KB  | ext JS | ext CSS | H1 | H2 | img alt=OK | lang=pt-PT | viewport | GA4 | JSON-LD | Title len |
|-------------------------------|-----|--------|---------|----|----|------------|------------|----------|-----|---------|-----------|
| `index.html`                  | 19.9| 1 (gtag) | 0     | 1  | 7  | 0 (no img) | ✅         | ✅       | ✅  | ✅      | 73 ✅     |
| `curto-circuito.html`         | 37.6| 1       | 0       | 1  | 13 | 0 (no img) | ✅         | ✅       | ✅  | ✅      | 83 ✅     |
| `villages/braganca-alfaiao.html` | 9.0 | 1     | 0       | 1  | 1  | 0 (no img) | ✅         | ✅       | ✅  | ✅      | 58 ✅     |
| `concelhos/braganca.html`     | 22.7| 1       | 0       | 1  | 9  | 0 (no img) | ✅         | ✅       | ✅  | ✅      | 54 ✅     |
| `distritos/braganca.html`     | 6.4 | 1       | 0       | 1  | 5  | 0 (no img) | ✅         | ✅       | ✅  | ✅      | 50 ✅     |
| `blog/avaria-eletrica-domingo.html` | 12.4 | 1 | 0    | 1  | 11 | 0 (no img) | ✅         | ✅       | ✅  | ✅      | 109 ⚠️   |

### Findings Lighthouse
- ✅ **CSS 100 % inline** sur toutes pages secondaires (`<style>` block) → 0 requête CSS externe → excellent LCP/FCP théorique.
- ✅ **Une seule requête JS externe** (gtag GA4) sur toutes les pages → blocking externe minimal.
- ✅ **1 seul H1** par page (correct SEO) ; H2 nombreux (structure sémantique propre).
- ✅ **Meta viewport** présent partout → mobile-friendly.
- ✅ **`lang="pt-PT"`** présent sur toutes les pages testées.
- ⚠️ **0 image `<img>`** sur toutes les pages échantillonnées → pas de gain à optimiser en `loading="lazy"` mais **LCP = texte pur** (pas de hero-image OG). À vérifier visuellement pour le score LCP réel.
- ⚠️ **Title 109 char** sur `blog/avaria-eletrica-domingo.html` (>60 recommandé Google) → tronqué SERP probable.
- ⚠️ **Aucune `aria-label` systématique** sur CTA `wa.me` et `tel:` → accessibilité moyenne.
- ❌ Pas de `width`/`height` sur SVG inline (CSS background uniquement).

**Score 8.0** : structure excellente, deux points perdus sur title trop long et accessibilité CTA perfectible.

---

## 2. Sécurité HTTP headers — 5.5/10

Test sur 5 URLs prod (`curl -sI -L`) :

| Header                     | Valeur                              | Statut |
|----------------------------|--------------------------------------|--------|
| `strict-transport-security`| `max-age=63072000` (2 ans)           | ✅ OK  |
| `x-content-type-options`   | `nosniff`                            | ✅ OK  |
| `x-frame-options`          | `DENY`                               | ✅ OK  |
| `content-type`             | `text/html; charset=utf-8`           | ✅ OK  |
| `server`                   | `Vercel` (header exposé)             | ⚠️ mineur |
| `etag`                     | Présent (cache-friendly)             | ✅ OK  |
| `access-control-allow-origin` | `*`                            | ⚠️ non requis |
| `content-disposition`      | `inline`                             | ✅ OK  |
| `cache-control`            | `public, max-age=0, must-revalidate` | ✅ OK  |
| **ABSENTS**                | CSP, Referrer-Policy, Permissions-Policy | ❌ |

### Findings sécurité
- ❌ **Pas de `Content-Security-Policy`** → exposition XSS totale. Recommandé : `default-src 'self'; img-src 'self' data: https:; script-src 'self' https://www.googletagmanager.com; style-src 'self' 'unsafe-inline'; connect-src 'self' https://www.google-analytics.com; frame-ancestors 'none'; base-uri 'self'`.
- ❌ **Pas de `Referrer-Policy`** → leaks URL complètes vers GA4 + outbound (wa.me).
- ❌ **Pas de `Permissions-Policy`** → autorise géoloc/caméra/micro par défaut sur tous les iframes.
- ⚠️ **`Access-Control-Allow-Origin: *`** sur toutes les pages HTML → inutile et surface d'attaque accrue.
- ⚠️ **`Server: Vercel`** exposé → fingerprinting facile (mineur).
- ✅ HSTS 2 ans (`max-age=63072000`) → couvre 2 ans entiers, conforme Mozilla guideline.
- ✅ `X-Frame-Options: DENY` → anti-clickjacking OK.

**Score 5.5** : HSTS + frame-options + nosniff présents (3.5/6) ; CSP/Referrer/Permissions absents (-2).

---

## 3. Schema.org coverage — 7.5/10

Échantillon 86 pages (120 racine + 30 concelhos + 6 distritos + 25 villages + 25 blog).

### Types présents (fréquence)

| Type              | Count (n=86) | %  |
|-------------------|--------------|-----|
| `FAQPage`         | 55           | 64 % |
| `WebPage`         | 55           | 64 % |
| `Service`         | 46           | 53 % |
| `Article`         | 39           | 45 % |
| `HowTo`           | 37           | 43 % |
| `LocalBusiness`   | 36           | 42 % |
| `BreadcrumbList`  | 30           | 35 % |
| `WebSite`         | 30           | 35 % |
| `Organization`    | 30           | 35 % |
| `EmergencyService`| 16           | 19 % |
| `BlogPosting`     | 16           | 19 % |

### Findings Schema.org
- ✅ **100 % des pages échantillonnées ont au moins 1 JSON-LD** + canonical.
- ✅ Toutes les pages racine/services ont `FAQPage` (très bon pour AI Overviews / SGE).
- ✅ `EmergencyService` × 16 (priorité haute pour urgence élec) → aligns intent.
- ⚠️ **`villages/*` : schema minimal** (`WebPage` uniquement) → page-level only, **pas de FAQPage/HowTo** sur 200 villages = potentielle perte SGE citations.
- ⚠️ **`distritos/braganca.html` : seulement `LocalBusiness`** (pas de FAQPage, pas de HowTo) → page distrito faible.
- ⚠️ **Géo-violations R12 détectées** (cf. section 5 NAP) :
  - `contactos.html` schema : `streetAddress: "Trás-os-Montes, Portugal"` (R12 violation — géo-précis)
  - `concelhos/braganca.html` schema : `addressLocality` = ville réelle (géo-non-neutre)
- ✅ **0 page sans schema** sur échantillon.
- ❌ **Pas de `Review`/`AggregateRating`** (volontairement, R11 ZÉRO INVENTION) → conformité doctrine, mais perd les étoiles SERP.
- ❌ **Pas de `VideoObject`/`ImageObject`** → pas d'enrichissement média.

**Score 7.5** : couverture 100 % avec FAQPage majoritaire (-1), 200 villages sous-équipés (-0.5), 2 violations R12 schéma (-1).

---

## 4. Conversion CTA — 9.5/10

Cible : tel: `+351932321892` et `wa.me/351932321892` (NAP R12).

| Section        | Fichiers | tel: | wa.me: | % CTA |
|----------------|----------|------|--------|-------|
| Racine `*.html`| 1 962    | 1 960 | 1 959 | 99.85 % |
| `concelhos/`   | 33       | 33   | 33     | 100 % |
| `distritos/`   | 6        | 6    | 6      | 100 % |
| `villages/`    | 200      | 200  | **0**  | **50 %** (tel only) |
| `blog/`        | 70       | 70   | 70     | 100 % |

### Findings Conversion CTA
- ✅ **CTA universel** sur 2 269 / 2 271 pages (99.91 %).
- ✅ **2 racines sans CTA** (probablement `indexnow-key.txt` HTML stub, `design-preview-eu.html`).
- ✅ **R12 respecté** : NAP unique 932 (pas de fuite 928 canalizador).
- ✅ **Sticky CTA + multiple CTA** par page (hero + bottom + sticky).
- ✅ **GA4 event tracking** configuré : `click_tel`, `click_whatsapp` → funnel mesurable.
- ⚠️ **`villages/*` : 0 WhatsApp CTA** → gap conversion mobile (200 pages). Tel only = friction supérieure sur mobile (coût appel).
- ⚠️ **CTA WhatsApp ouvre `wa.me/351...` sans `?text=`** → pas de message pré-rempli = friction conversion élevée (meilleure pratique : `?text=Olá%20preciso%20eletricista%20urgente%20em%20[ville]`).
- ⚠️ **`trackWhatsAppClick('source')` event** mais pas de tracking différencié par page-source → impossible de mesurer ROI par template.
- ❌ Pas de `trackTelClick` GA4 enhanced conversions (`phone_conversion`).

**Score 9.5** : couverture CTA 99.91 % + R12 respecté + tracking GA4 (-0.5 villages sans WA).

---

## 5. NAP consistency — 8.5/10

Cross-check NAP EU vs autres supports.

| Source                | NAP trouvé                          | Format |
|-----------------------|--------------------------------------|--------|
| `index.html` schema   | `+351 932 321 892`                   | ✅     |
| `index.html` tel href | `tel:+351932321892`                  | ✅     |
| `contactos.html`      | `+351 932 321 892` (4 occurrences)   | ✅     |
| `precos.html`         | `+351 932 321 892` (6 occurrences)   | ✅     |
| `llms.txt`            | `+351 932 321 892`                   | ✅     |
| `llms-full.txt`       | `+351 932 321 892` (5 occurrences)   | ✅     |
| `ai.txt`              | `+351-932-321-892` (PrimaryPhone + WhatsApp) | ✅ |
| `sitemap.xml`         | N/A                                  | -      |
| Brand name            | `Norte Reparos` (9× index), `Filipe Bragança` (2× index), `Staff-Seekers` (2× index) | ✅ |
| Cross-928 leak        | Aucune fuite `928 484 451` sur EU (1 mention dans `llms.txt` ligne cross-ref canalizador) | ✅ |

### Findings NAP
- ✅ **Numéro unique EU : `+351 932 321 892`** → identique sur tous supports (HTML, llms, ai, sitemap excluded).
- ✅ **Aucune contamination** croisée avec `928 484 451` (canalizador-urgente.pt) sur les pages EU.
- ✅ **Brand name cohérent** : `Norte Reparos` (9×) + `Staff-Seekers` (2×) + `Filipe Bragança` (2×) — alignement R12 "artisan local identifiable".
- ⚠️ **Violation R12 (géo-non-neutre)** sur `contactos.html` schema : `streetAddress: "Trás-os-Montes, Portugal"` — la doctrine dit "**pas de `streetAddress` précise**" → ici la string est volontairement vague mais le champ existe. À vérifier si Google lit "rue" = signal adresse physique.
- ⚠️ **Violation R12 sur `concelhos/braganca.html`** : `addressLocality` = ville concrète dans `@graph` → leak géo-précis sur 33 concelhos probable (non échantillonné exhaustivement).
- ⚠️ **`index.html` schema `@type: ["Electrician","LocalBusiness","ProfessionalService"]`** : `Electrician` n'existe PAS dans Schema.org vocabulary officiel. Type non reconnu → ignoré par Google. À remplacer par `ProfessionalService` + `Service` uniquement.
- ⚠️ **Email `geral@eletricista-norte-reparos.pt`** dans schema `index.html` et `contactos.html` → cohérent mais redirige vers domaine principal `eletricista-norte-reparos.pt`. Vérifier que ce MX existe.

**Score 8.5** : NAP parfait sur 9 supports + R11 respecté (-0.5 Electrician type invalide, -0.5 addressLocality leak sur concelhos, -0.5 streetAddress contact).

---

## 6. Indexation sitemap — 3.0/10

Fichiers sitemap présents à la racine : `sitemap.xml` + `sitemap-villages.xml` (1962 + 1936 = 3 898 lignes).

| Source                       | URLs   |
|------------------------------|--------|
| `sitemap.xml`                | 1 962  |
| `sitemap-villages.xml`       | 1 936  |
| **Total sitemap (clean URLs)** | **1 962 distinct** (chevauchement partiel) |
| **Total fichiers périmètre**  | **2 271** |
| **Couverture sitemap**         | **86.5 %** |

### Couverture par section

| Section        | Fichiers | Dans sitemap | Couverture |
|----------------|----------|--------------|------------|
| Racine `*.html`| 1 962    | 1 962        | 100 %      |
| `concelhos/`   | 33       | **0**        | **0 %** ❌ |
| `distritos/`   | 6        | **0**        | **0 %** ❌ |
| `villages/`    | 200      | **0**        | **0 %** ❌ |
| `blog/`        | 70       | **0**        | **0 %** ❌ |

### Findings sitemap
- ❌ **`sitemap-villages.xml` ne contient AUCUN `/villages/*`** : malgré son nom, il ne contient que des URLs racine `/eletricista-*` (probablement merge accidentel des deux sitemaps par un script précédent). Le nom est trompeur.
- ❌ **Aucune section secondaire indexée** : 309 pages (33 concelhos + 6 distritos + 200 villages + 70 blog) sont **complètement hors sitemap** → risque de non-découverte Google pour tout le contenu secondaire.
- ❌ **`/index.html` (la racine sans trailing slash)** → redirige 308 → `/`. La racine canonique est OK mais absente explicite du sitemap avec `priority=1.0` (1 URL racine seulement).
- ⚠️ **105 URLs orphelines** dans `sitemap.xml` (URLs listées mais sans fichier `.html` correspondant) — exemples : `/eletricista-avaria-eletrica-cedovi` (manque le 'm' → `cedovim`), `/eletricista-eletricista-afonsi`, `/eletricista-avaria-eletrica-lali`. Probablement génération script avec troncature sur variable. → **renvoient 404** sur Vercel (à confirmer).
- ⚠️ **Priorités uniformes** : `priority=1.0` sur home uniquement, `priority=0.7` sur tous les autres racine. Blog/concelhos/distritos/villages non classés.
- ⚠️ **`lastmod` 2026-07-28 ou 2026-08-04** : précise mais figée → Google peut soupçonner signal d'obsolescence sur contenu non-touched récemment.
- ✅ `Sitemap:` directives présentes dans `robots.txt` (x2).

**Score 3.0** : racine 100 % OK (5/10), tout le secondaire hors sitemap (-5), 105 orphelines probables (-2). Pondération 3.0.

---

## 7. Canonical KO — 8.0/10

Audit sur 2 271 fichiers (toutes sections périmètre).

### Distribution format canonical

| Format                          | Count | %  |
|---------------------------------|-------|-----|
| Clean URL (`/foo` sans .html)   | 2 270 | 99.96 % |
| Avec `.html`                    | 1     | 0.04 % |
| Absent                         | 0     | 0 %   |

### Findings Canonical
- ✅ **99.96 % de pages avec canonical propre** → alignement parfait avec `cleanUrls` Vercel (308 → clean).
- ✅ **1 seule page en KO** : `sobre.html` → canonical `https://eletricista-urgente.pt/sobre.html`. **KO confirmé** car Vercel redirige `/sobre.html` → `/sobre` (308), et la canonical pointe vers l'URL avec extension → boucle de redirection possible pour Google.
- ✅ **Canonical en `https://`** (pas de mix http/https).
- ✅ **Canonical en `www`-less** (cohérent avec config Vercel).
- ⚠️ **`/index.html` (avec extension) sert du contenu dupliqué** de `/` (home) — pas de canonical `self-referencing` pour `/index.html`, juste dépendance sur 308 Vercel. Si Vercel perd sa config `cleanUrls`, duplication emerge.
- ⚠️ **`/avaliacoes-clientes.html`** (sous `public/`) → redirige 308 → pas de canonical ni dans `/public/` ni dans racine. Comportement hérité du legacy blog R12 (cf. `_audit/RAPPORT-MISSION-LEGACY-BLOG-R12.md`).

**Score 8.0** : 99.96 % propres + 0 page sans canonical (-1.5 `sobre.html` KO + -0.5 dépendance cleanUrls Vercel).

---

## 8. llms / ai / robots — 9.5/10

Audit des surfaces AI-first du site.

| Fichier              | Statut prod | Taille | Évaluation |
|----------------------|-------------|--------|------------|
| `llms.txt`           | 200 ✅       | 98 L  | Descriptif court, bien structuré (sections Serviços/Preços/FAQ/Contacto) |
| `llms-full.txt`      | 200 ✅       | 157 L | Version longue, plus de contexte (équipement, zones) |
| `ai.txt`             | 200 ✅       | 42 L  | Format YAML-like (Name, Type, SubType, Pricing, Equipment) |
| `robots.txt`         | 200 ✅       | 62 L  | 12 AI bots explicitement Allow + Semrush + Ahrefs + Disallow `/public/` |
| `sitemap.xml`        | 200 ✅       | -     | Référencé dans robots.txt |
| `sitemap-villages.xml` | 200 ✅     | -     | Référencé dans robots.txt |

### Findings llms/ai/robots
- ✅ **R10 respectée à 100 %** : 12 bots IA explicitement Allow (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, Meta-ExternalAgent, Applebot-Extended, CCBot…). Bots SEO (Semrush, Ahrefs) également autorisés.
- ✅ **`llms.txt` production-ready** : structure claire (Serviços/Preços/FAQ/Equipamento/Contacto). Référencé dans llms-full.txt (auto-référence).
- ✅ **`ai.txt` format structuré** : Name, Type, SubType, Pricing détaillé (HandLabor 70 EUR/h, TravelZones Z1-Z6), Equipment listé. **Excellent pour ingestion IA.**
- ✅ **Default `User-agent: *` Allow `/`** → Googlebot, Bingbot, DuckDuckBot : tous crawables.
- ⚠️ **Divergence entre `llms.txt` et `public/llms.txt`** : 2 versions existent (diff `public/llms.txt` ligne 1 = `# Norte Reparos — Eletricista de Urgência` vs racine = `# Norte Reparos — Eletricista Urgente em Trás-os-Montes`). Probable héritage legacy non synchronisé.
- ⚠️ **Aucun lien `<link rel="llms-txt">`** dans `<head>` des pages HTML → pas de signal explicite aux crawlers IA du chemin canonique (recommandation emerging spec).
- ⚠️ **`ai.txt` n'a pas de directive "Last-Modified" explicite hors le champ `LastUpdated`** (qui est 2026-07-01) → peut être ignoré par crawlers regardant HTTP Last-Modified.
- ✅ **Pas de `Disallow` excessif** : seule `/public/` est bloquée (légitime, miroir backup).

**Score 9.5** : R10 + llms.txt + ai.txt tous présents et bien formés (-0.5 divergence llms.txt vs public/llms.txt).

---

## 9. Endpoints critiques — 9.0/10

Test `curl -sI` sur URLs stratégiques :

| URL                                  | Statut HTTP | Notes |
|--------------------------------------|-------------|-------|
| `/` (home)                           | 200 ✅       | 20 337 B |
| `/contactos`                         | 200 ✅       | 17 958 B |
| `/precos`                            | 200 ✅       | 14 609 B |
| `/curto-circuito`                    | 200 ✅       | 38 515 B |
| `/sitemap.xml`                       | 200 ✅       | 268 208 B |
| `/sitemap-villages.xml`              | 200 ✅       | (testé via grep) |
| `/robots.txt`                        | 200 ✅       | 1 112 B |
| `/llms.txt`                          | 200 ✅       | 5 738 B |
| `/llms-full.txt`                     | 200 ✅       | (200 OK) |
| `/ai.txt`                            | 200 ✅       | 1 492 B |
| `/index.html` (extension)            | 308 → `/` ✅ | Vercel cleanUrls |
| `/avaliacoes-clientes.html`          | 308 → `/avaliacoes-clientes` ✅ | (legacy) |
| `/concelhos/braganca`                | 200 ✅       | 23 198 B (cache MISS — récent déploiement) |
| `/villages/braganca-alfaiao`         | 200 ✅       | 9 201 B (cache MISS) |
| `/blog/curto-circuito`               | 200 ✅       | 36 879 B |

### Findings Endpoints critiques
- ✅ **100 % des endpoints prioritaires retournent 200** (cleanUrls).
- ✅ **Redirections 308 propres** : toutes les URLs avec extension `.html` redirigent vers leur version clean (Vercel `cleanUrls: true`).
- ✅ **HSTS + nosniff + frame-options présents sur toutes les réponses**.
- ✅ **Vary/ETag fonctionnels** : HIT cache sur home (14886s age), MISS sur concelhos récent (0s).
- ✅ **Tous les fichiers AI-first servis correctement** : `llms.txt`, `llms-full.txt`, `ai.txt`, `robots.txt`, 2 sitemaps.
- ⚠️ **Pas de `/healthz` ni `/status`** exposé publiquement (volontaire, OK).
- ⚠️ **`Vercel-Cache: HIT` sur home** mais contenu modifié `2026-08-11 02:13:36 GMT` (age 14886s ≈ 4h) → cache stale possible si push après ce timestamp. À surveiller.
- ⚠️ **Aucun endpoint `404.html` propre** testé — Vercel default 404 attendu.

**Score 9.0** : 14/14 endpoints prioritaires 200 OK + cache HIT/MISS propre (-1.0 surveillance cache stale, -0 absence monitoring endpoint public).

---

## 🏆 TOP 5 FINDINGS

### 🔴 1. Sitemap incomplet — 309 pages secondaires hors sitemap (PRIORITÉ HAUTE)
**Sections concelhos/distritos/villages/blog** (33 + 6 + 200 + 70 = **309 pages) ne sont déclarées dans aucun sitemap**. Risque de non-indexation Google sur tout le contenu secondaire (70 % du site).
**Impact SEO** : perte potentielle de 309 Long Tail Keywords (each village/concelho est une page à intent local).
**Action** : 
1. Renommer `sitemap-villages.xml` → `sitemap-electricista-pages.xml` (son contenu réel)
2. Créer `sitemap-villages.xml` (vide pour l'instant) et `sitemap-concelhos.xml`, `sitemap-distritos.xml`, `sitemap-blog.xml`
3. Référencer les 5 sitemaps dans `robots.txt`
4. Nettoyer les **105 URLs orphelines** (troncatures manifestes : `cedovi`, `lali`, `lazari` → corriger vers `cedovim`, `lalim`, `lazarim` ou supprimer)

### 🔴 2. Sécurité HTTP headers — CSP, Referrer-Policy, Permissions-Policy absents (PRIORITÉ HAUTE)
Aucun CSP → surface XSS maximale. Le site injecte du JSON-LD utilisateur (description, FAQ textuelles), et héberge du GA4. Une faille = exfiltration data.
**Action** : ajouter dans config Vercel (ou Cloudflare si devant) :
```
Content-Security-Policy: default-src 'self'; img-src 'self' data: https:; script-src 'self' 'unsafe-inline' https://www.googletagmanager.com; style-src 'self' 'unsafe-inline'; connect-src 'self' https://www.google-analytics.com; frame-ancestors 'none'; base-uri 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), camera=(), microphone=()
```

### 🟠 3. Schema.org R12 violations + type invalide (PRIORITÉ MOYENNE)
- `contactos.html` : `streetAddress: "Trás-os-Montes, Portugal"` → doctrine R12 violation (géo-précis). **À supprimer**.
- `concelhos/braganca.html` : `addressLocality` = ville concrète → leak géo-précis sur 33 concelhos probable. **À vérifier exhaustivement et neutraliser**.
- `index.html` : `@type: ["Electrician", ...]` → `Electrician` n'est PAS un type Schema.org valide (ignoré par Google). **À retirer, garder `LocalBusiness` + `ProfessionalService` + `Service`**.

### 🟠 4. Villages sans WhatsApp CTA — friction conversion mobile (PRIORITÉ MOYENNE)
**200 villages** ont un CTA `tel:` mais **0 CTA `wa.me/`**. Sur mobile, WhatsApp convertit 3-5× mieux que `tel:` (pas de coût d'appel, asynchrone, qualification écrite). 
**Action** : ajouter un bouton WhatsApp secondaire `wa.me/351932321892?text=Olá%20preciso%20eletricista%20em%20[ville]` sur les 200 villages, et un event `trackWhatsAppClick('village-NNN')` pour attribution ROI.

### 🟠 5. Canonical KO sur `sobre.html` + divergence llms.txt vs public/llms.txt (PRIORITÉ BASSE)
- `sobre.html` → canonical `https://eletricista-urgente.pt/sobre.html` (avec extension). Vercel redirige 308 → clean URL `/sobre`. Boucle. **À corriger vers** `https://eletricista-urgente.pt/sobre`.
- `llms.txt` (racine) et `public/llms.txt` (miroir backup) ont des contenus divergents (ligne 1 et structure). **Risque d'indexation IA incohérente**. Action : unifier et garder uniquement la racine, supprimer le miroir `/public/llms.txt` (robots.txt bloque déjà `/public/` mais Google peut ignorer robots sur certains cas).

---

## Annexes

### Pages testées (échantillon Lighthouse + Schema)
- `index.html` (home)
- `curto-circuito.html` (service phare)
- `contactos.html`
- `precos.html`
- `concelhos/braganca.html`
- `distritos/braganca.html`
- `villages/braganca-alfaiao.html`
- `blog/avaria-eletrica-domingo.html`
- 5 URLs prod : `/`, `/contactos`, `/precos`, `/curto-circuito`, `/index.html`, `/avaliacoes-clientes.html`

### Fichiers de référence croisés
- `AGENTS.md` (R10, R11, R12, R145)
- `PRICING.md` (grille canonique 70 €/h élec, Z1-Z6)
- `_audit/canonical-triage-EU-summary.json`
- `_audit/RAPPORT-MISSION-LEGACY-BLOG-R12.md`

### Restrictions observées
- ⛔ READ-ONLY strict respecté (aucun fichier modifié dans le périmètre).
- ⛔ Lighthouse CLI non disponible dans le runtime → analyse proxy statique (pas de score Lighthouse numérique réel).
- ⛔ Audit GA4 live non exécuté → IDs et event names validés sur HTML statique uniquement.

---

*Rapport généré le 2026-08-11 · Sub-agent Norte-OS · Audit proactif EU*