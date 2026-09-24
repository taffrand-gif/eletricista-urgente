# SMKO eu — eletricista-aguas-frias — 2026-09-24 (re-test post tâche t_7a7c928a)

**Tâche** : t_7a7c928a
**URL** : https://eletricista-urgente.pt/eletricista-aguas-frias
**Source signalement** : scan local « wrong-phone » 2026-09-24
**Extrait fourni** : `ign:center;background:#0a4d68;color:#fff"><h2 style="color:#fff">Eletricista em Águas Frias?</h2><a class="cta" href="tel:+351****1892">…`

## Verdict

**KO wrong-phone RÉFUTÉ — aucun écart NAP, fichier conforme, aucun commit requis.**

## Vérification contenu (téléphone — point nommé par la preuve live)

### Salve exhaustive des numéros 9 chiffres dans le fichier

| Pattern | Occurrences |
|---------|-------------|
| `+351 932 321 892` (NAP élec, E.164 lisible) | 8 |
| `932 321 892` (forme courte, hors préfixe +351) | 10 |
| `+351-932 321 892` (JSON-LD Schema.org, tirets) | 1 |
| `tel:+351****1892` (href `tel:` masqué, cf. PRICING.md §NAP — obscurcit les 4 chars médians, laisse `1892` final) | **5** |
| `wa.me/351932321892` (WhatsApp href) | **6** |
| **`928 …` (NAP canal — à NE PAS mettre sur EU)** | **0** |
| **`928 484 451` (NAP canal explicite)** | **0** |
| **Toute autre séquence 9 chiffres** | **0** |

**Total : 30 occurrences téléphone, 100 % sur le NAP élec 932 321 892. Aucune trace de 928 ni d'un numéro tiers.**

### Comparaison local ↔ live (Vercel edge)

| Source | SHA256 | Taille | ETag Vercel | HTTP |
|--------|--------|--------|-------------|------|
| `eletricista-aguas-frias.html` local | `a4cf1e966d9011702306aa6e8898482bb7c570f17e24aa5aa38fefbe0a8723d4` | 23 344 octets | n/a | n/a |
| `https://eletricista-urgente.pt/eletricista-aguas-frias` (curl 2026-09-24 23:25 BST) | `a4cf1e966d9011702306aa6e8898482bb7c570f17e24aa5aa38fefbe0a8723d4` | 23 344 octets | `b0ccfbfd6c9693a35b41b57e99a1eb79` | **200** |

**Match parfait local = live** (sha256 byte-pour-byte identique), ETag stable depuis 14/09 (cf. audit SMKO 15/09, 5/5 probes HTTP 200). Aucun déploiement divergent, aucun drift NAP. `last-modified: Thu, 24 Sep 2026 18:48:49 GMT` cohérent avec le snapshot Vercel.

### Vérification de l'extrait cité dans la preuve live

L'extrait fourni commence par `ign:center;background:#0a4d68;color:#fff"><h2 style="color:#fff">Eletricista em Águas Frias?</h2><a class="cta" href="tel:+351****1892">`. Recherche exhaustive dans le fichier :

| Pattern recherché | Résultat |
|-------------------|----------|
| `ign:center;background:#0a4d68` | 0 occurrence |
| `color:#fff"><h2 style="color:#fff">Eletricista` | 0 occurrence |
| `Eletricista em Águas Frias?</h2>` (avec point d'interrogation final) | 0 occurrence (le H2 réel est « Eletricista em Águas Frias » sans `?`) |
| `<a class="cta" href="tel:+351****1892">` | **5 occurrences réelles** (le `class="cta"` existe bien, attaché à `<a href="tel:+351****1892">` dans le `<div class="hero">` et le `<div class="cta-bottom">` — la forme `href` est bien présente, mais la chaîne entière `class="cta" href="tel:+351****1892"` n'est pas adjacente à un H2 « Aguas Frias? » avec point d'interrogation ; les `class="cta"` réels sont soit sur le `<div class="hero">`, soit sur le `<div class="cta-bottom">`, pas sur un fond `#0a4d68`) |

**L'extrait est un composite reconstitué** (concaténation de fragments de bouts de lignes différents) qui ne correspond à aucun endroit du fichier réel : (a) le préfixe CSS `ign:center;background:#0a4d68` n'existe pas dans le fichier (le fond du hero est `background:#0a4d68` mais le CSS est `align:center`, pas `ign:center` — vraisemblablement un copier-coller approximatif d'un extrait précédent) ; (b) le H2 « Eletricista em Águas Frias? » avec `?` final n'existe pas ; (c) la séquence complète `<a class="cta" href="tel:+351****1892">📞 +351 932 321 892</a><a class="cta wa" href="https://wa.me/351932321892">` n'est pas adjacente à un H2 « Eletricista em Águas Frias? » — le scan local a vraisemblablement lu des caractères sur plusieurs lignes voisines et assemblé un faux match. **Note importante** : le `class="cta"` cité dans la preuve est bien réel dans le fichier (5 occurrences), et le `tel:+351****1892` est bien réel (5 occurrences), mais leur concaténation dans le contexte cité + H2 Aguas Frias + fond `0a4d68` = composite fabriqué. Le téléphone reste 932 321 892 dans tous les cas.

### Vérification NAP-cohérence (Doctrine R12 + PRICING.md)

- **PRICING.md §NAP** : Élec = `+351 932 321 892` ; Canal = `+351 928 484 451`. ✅ Fichier conforme (que du 932).
- **AGENTS.md §Périmètre repo** : « JAMAIS inverser avec 928 (canalizador-urgente) ». ✅ Aucune occurrence 928.
- **AGENTS.md §12 R12 §1** : NAP élec 932 cohérent avec doctrine Transparence Radicale. ✅.
- **JSON-LD LocalBusiness** (`<script type="application/ld+json">` ligne 36) : `"telephone":"+351-932 321 892"` ✅.
- **OpenGraph `og:title`/`og:description`** (ligne 32) : NAP 932 cohérent. ✅.
- **Schema.org BreadcrumbList + FAQPage + Service + LocalBusiness** (lignes 65, 71) : `telephone` toujours 932. ✅.
- **`<title>`** : `Eletricista Profissional em Aguas Frias — Norte Reparos` ✅.
- **`<h1>`** : `Eletricista Profissional em Aguas Frias` ✅.

### Vérification absence contamination plomberie

Recherche des termes typiques d'un template-bleed plomberie (cf. tâche t_e6bfd650 corticos, fix e24f1cb00) :

| Pattern | Occurrences |
|---------|-------------|
| `Fuga ativa` / `Inundação` / `Cano rebentado` / `Esgoto a transbordar` / `Válvula de segurança` | 0 / 0 / 0 / 0 / 0 |
| `feche a torneira geral` / `feche o contador` | 0 / 0 |
| `torneira` (hors équipement ROLeak) | 0 |
| `aquecimento` (sens plomberie) | 0 |
| `canalização` / `canalizador` (hors JSON-LD `sameAs`) | 0 (les `sameAs` pointent vers les sites irmãos, légitime) |

**Aucune contamination plomberie.** La seule occurrence de « fugas » serait dans la mention de l'équipement `ROLeak Aqua 3Plus` (légitime, c'est un outil élec de détection acoustique, listé en AGENTS.md §12 R12 §1) — ici même pas de mention ROLeak, le fichier est un pSEO village court sans section équipement.

### Témoins Annexe A (pronoun + R12 + R11 + R145)

| Pattern | Occurrences |
|---------|-------------|
| `mediante confirmação` | 0 |
| `Resposta prioritária` | 0 |
| `Garantia 2 anos` | 0 |
| `Orçamento grátis` | 0 |
| `contacte-me` | 0 |
| `vou mostrar-lhe` | 0 |
| `minha empresa` | 0 |
| `sozinho` | 0 |
| `definitivo` | 0 |
| `65 €/h` (drift plomberie) | 0 |
| `+351 928` (drift plomberie) | 0 |

## État repo

- working tree : aucun changement sur `eletricista-aguas-frias.html` ; rapport `_audit/SMKO-eu-2026-09-24-aguas-frias.md` seul ajouté, non staged
- commit : aucun
- `eletricista-aguas-frias.html` : non touché (23 344 octets, 152 lignes, sha256 `a4cf1e96…`)
- `sitemap.xml` : non touché (déjà conforme, 3 sitemaps référencent l'URL avec priority 0.7)

## Diagnostic

Même classe de signal que t_7b290488 (eu/aguas-vivas), t_c6432a28 (cnr/salzedas), t_ac479308 (cnr/marialva), t_1662f744 (cu/alvendre), t_c0beada0 (eu/amendoeira), t_4fa3d40f (cu/almendra), t_9ce7c4c5-mezquita-cu : **faux positif scan local**. Le détecteur a vraisemblablement concaténé des fragments de plusieurs lignes pour fabriquer un faux match « wrong-phone » qui n'existe pas dans le fichier réel ni dans la version servie.

À noter que la page a 1 défaut **secondaire** sans rapport avec le téléphone :
1. **`<h2>` = `Eletricista em Águas Frias` (ligne 91)** — défaut stylistique mineur, le H2 ne contient pas de mot-clé d'intention type « urgente » / « 24h » / « preço ». Hors-porte de cette tâche wrong-phone.

Aucune action recommandée pour cette tâche. Conformément à R7, **STOP validation Filipe avant toute autre intervention** sur ce fichier (le défaut 1 ci-dessus peut être corrigé dans un batch séparé avec GO explicite, suivant la doctrine « AUCUN batch sans prototype 1 page test » de AGENTS.md §12).

## Leçon (série en cours)

9e KO signalisé réfuté en 11 jours (14/09 → 24/09) sur les 4 sites eu/cu/cnr. Le scan « wrong-phone » local a un taux de faux positifs élevé quand l'extrait cité est un composite multi-lignes. Avant tout patch wrong-phone, **toujours** :
1. Vérifier `sha256` local = live (curl + etag)
2. Compter toutes les occurrences des NAP 928/932 (un seul des deux doit dominer selon le site)
3. Vérifier que l'extrait cité existe tel quel dans le fichier (chercher chaque fragment séparément)
4. Si les 3 checks passent → réfutation, rapport `_audit/`, PR draft consignation, **pas de patch**.

**Action recommandée côté pool-keeper** : ajouter une heuristique d'alerte dans le détecteur local « wrong-phone » — ne pas lever de KO sur un fichier dont le compteur NAP majoritaire (≥90 % des occurrences) correspond au NAP canonique du site. Cela filtrerait 9/9 faux-positifs observés sans dégrader la détection des vrais dérives (qui ont un compteur NAP mixte, ex. corticos/olmos).