# 📄 SEO_PLAN.md — Mémoire vivante du projet

> **Fichier de coordination multi-IA / multi-agents / multi-harnais**
> Toute IA travaillant sur ce repo DOIT lire ce fichier avant toute action.
> Toute modification du projet DOIT être consignée ici.

**Propriétaire** : Philippe Braganca (Filipe)
**Site** : https://eletricista-urgente.pt
**Repo** : `taffrand-gif/eletricista-urgente` (working copy locale : `~/work/Sites/eletricista-urgente/`)
**Branche prod** : `main` | **Branche dev** : `seo-2026-q3` (à créer)
**NAP** : +351 932 321 892 | Norte Reparos | Trás-os-Montes
**Doctrine site** : **Transparence Radicale** (AGENTS.md §12)
**AGENTS.md** : verrouillé 28/06/2026 — copie adaptée de `canalizador-urgente/AGENTS.md` avec focus élec

---

## 🎯 VISION — Ce qu'on veut devenir

**Objectif business** : être la **référence dépannage électricité d'urgence** sur Trás-os-Montes via SEO + GEO pur.

**Périmètre site** : URGENCE uniquement (curto-circuito, sem luz, cheiro queimado, disjuntor dispara). PAS d'installation (c'est `eletricista-norte-reparos.pt`).

**Promesse homepage** : "Sem luz? Curto-circuito? 70€/h, deslocação Z1-Z6, orçamento por escrito antes da intervenção. Ligue agora."

**Cible SEO** :
- Top 5 Google sur "eletricista urgente Bragança" / "curto-circuito urgente"
- Cité par Google AI Overview sur "preço eletricista urgente"
- Appels nuit/WE/feriado captés

**Cible business** : 20-50 appels/mois d'urgence.

---

## 📊 ÉTAT ACTUEL (au 28/06/2026)

### Forces SEO/GEO (à PROTÉGER)
- ✅ 2062 fichiers HTML
- ✅ **Schema.org Electrician complet** (NAP, areaServed 12 villes, openingHoursSpecification 24/7)
- ✅ Robots.txt : 15+ crawlers IA ouverts
- ✅ Sitemap.xml présent
- ✅ NAP cohérent : 932 321 892
- ✅ Doctrine Transparence Radicale verrouillée

### Faiblesses SEO/GEO CRITIQUES (PRIORITÉ 1)
- 🔴 Homepage **squelettique** : 16-39 éléments
- 🔴 Manque : grille de prix **70€/h** + Z1-Z6 — ⚠️ **CE SITE = 70€/h, PAS 65**
- 🔴 Manque : "fala sempre com a mesma pessoa, não um call center"
- 🔴 Manque : section équipement réel (Fluke, Megger, FLIR)
- 🔴 Manque : FAQ honnête
- 🔴 Manque : schema.org FAQPage
- 🔴 Pages /zonas/ = 0
- 🟠 Pas de différenciation d'intention vs `eletricista-norte-reparos.pt`

### Doctrine Transparence Radicale (R12) — 10 sections
1. Transparence prix : **70€/h élec**, Z1-Z6, +50% nuit/WE/feriado
2. "orçamento por escrito antes de qualquer intervenção, sem surpresas"
3. "fala sempre com a mesma pessoa, não um call center"
4. Diagnostic transparent
5. Traçabilité : NIF, seguro RC, fichas eletrotécnicas
6. Équipement EXACT : Fluke T6-1000, Megger MFT1741+, ROLeak, FLIR E96
7. Marques : Schneider, Legrand
8. FAQ honnête
9. Zones d'intervention
10. CTA Tel + WhatsApp

### Interdits
- ❌ Pas de chantiers inventés (R4 + R11)
- ❌ Pas d'avis/témoignages inventés
- ❌ Pas de délais chiffrés
- ❌ Pas d'adresse précise (R5)
- ❌ Pas de mention "instalação, projeto, remodelação"
- ❌ Pas de `git push --force` (R6)
- ❌ Pas d'auto-merge (R7)
- ❌ **Pas de 65€/h ici** (c'est 70€/h pour l'élec)

---

## 🗺️ ROADMAP — 3 phases

### 🟥 PHASE A — Refondre ce site selon Doctrine (S1-S2) ← **PRIORITÉ 1**
Voir TODO DÉTAILLÉE ci-dessous

### 🟧 PHASE B — Différencier les 4 homepages (S3)
- B1. Homepage distincte de `eletricista-norte-reparos.pt` par l'intention

### 🟨 PHASE C — Backlinks externes (continu S5+)

---

## 📋 TODO DÉTAILLÉE pour ce repo

### 🟥 A1 — Homepage complète selon Doctrine §12 (S1) ← **CRITIQUE**

**Statut** : ✅ FAIT (PR #33+#35+#36, 29/06/2026)
**Priorité** : CRITIQUE
**Effort** : ~4h

**Branche** : `seo-2026-q3` (à créer depuis `main`)

**Sections à créer (ordre imposé)** :
1. H1 unique : "⚡ Eletricista Urgente 24h — Trás-os-Montes"
2. Bloc prix HAUT : **70€/h** + grille Z1-Z6 + +50%
3. "Quem somos" : "Fala sempre com a mesma pessoa"
4. Équipement : Fluke T6-1000, Megger MFT1741+, ROLeak, FLIR E96
5. Services : Curto-circuito, sem luz, cheiro queimado
6. FAQ honnête
7. Zones
8. Témoignages honnête
9. CTA : Tel +351 932 321 892
10. Schema.org FAQPage

**Règles** : R3 (STOP), R4 (zéro invention), R5 (géo-neutre), R8 (témoin), R9 (grille), R11, R12

**Témoin R8** :
```bash
wc -l index.html
grep -c "70€" index.html  # doit être ≥ 1
grep -c "Fluke" index.html
grep -c "Megger" index.html
grep -c "schema.org" index.html
```

### 🟥 A2 — 8 pages /zonas/ prioritaires (S2)
**8 fichiers** : `eletricista-urgente-{braganca,vila-real,mirandela,chaves,miranda-do-douro,mogadouro,vinhais,lamego}.html`
**Structure** : ton urgence + prix 70€/h + FAQ locales + schema.org FAQPage
**Effort** : ~8h

---

## 🛡️ RÈGLES DU PROJET

- R1-R9 : voir AGENTS.md
- R10 : robots.txt IA ouvertes
- R11 : ZÉRO INVENTION
- R12 : DOCTRINE TRANSPARENCE RADICALE
- Branche dev : `seo-2026-q3` (à créer)
- Branche prod : `main` — JAMAIS toucher sans STOP
- Doctrine : Transparence Radicale (PAS A+)
- **Tarif : 70€/h** (PAS 65)
- NAP : 932 321 892

---

## 🔄 HISTORIQUE

> **Format OBLIGATOIRE** : `| DATE | AGENT | TÂCHE | ACTION | JUSTIFICATION | RÉSULTAT | STATUT |`

| Date | Agent | Tâche | Action | Justification | Résultat | Statut |
|---|---|---|---|---|---|---|
| 2026-06-28 | claude-minimax-m3 | création | Création SEO_PLAN.md | Mémoire vivante 4 sites | Fichier créé, 251 lignes | ✅ Fait |
| 2026-06-28 | claude-minimax-m3 | phase-2 | Lecture homepage + schema.org Electrician | Audit lecture seule (R3) | Schema.org complet (12 villes, 24/7) | ✅ Fait |
| 2026-06-28 | claude-minimax-m3 | phase-3 | Création 4 SEO_PLAN.md | Mémoire par projet | 4 fichiers créés | ✅ Fait |
| 2026-06-28 | claude-minimax-m3 | coordination | Patch AGENTS.md + CLAUDE.md (× 4) | Rendre SEO_PLAN.md découvrable | Triangle complet | ✅ Fait |
| 2026-06-28 | claude-minimax-m3 | audit | NAP uniformisé | Cohérence cross-fichiers | "Norte Reparos \| Trás-os-Montes" sur 4 sites | ✅ Fait |
| 2026-06-28 | claude-minimax-m3 | refonte | ⚠️ PRIORITÉ 1 = A1 refonte homepage **70€/h** | Doctrine §12 NON exécutée | Tâche verrouillée, branche `seo-2026-q3` désignée | 🛑 STOP - attente Philippe |
| 2026-06-28 | claude-minimax-m3 | restore | Réécriture complète (recovery) | Patch replace_all a détruit la structure | Fichier restauré à partir de la version saine de canalizador | ✅ Fait |
| 2026-06-29 | Hermes | R11 anos/fundada | Patch "12+ anos", "+10 anos", "15 anos", "Fundada em 2014" → "experiência em serviço técnico" / "Serviço estabelecido em Trás-os-Montes" | R11 (zéro invention) — 1992 occurrences virées sur 1823 fichiers | Témoin AVANT=3617+, APRÈS=0 | ✅ Fait |
| 2026-06-29 | Hermes | R11 fourchettes service | Patch ~70 fourchettes SERVICE (80-200€, 50-150€, 150-500€, 250-350€, 1000-2000€, 7000-15000€, etc.) → "sob orçamento" | R11 (zéro invention) — fourchettes déplacement (15-65€) CONSERVÉES, fourchettes économie (250-400€/ano) CONSERVÉES | Témoin AVANT=528, APRÈS=0 | ✅ Fait |
| 2026-06-29 | Hermes | R11 formulaires annexes | Patch "mais de X anos de atividade", "mais de uma década", "X anos de experiência no setor/em canalização" | R11 (zéro invention) — 213 occurrences virées sur 204 fichiers | Témoin AVANT=213, APRÈS=0 | ✅ Fait |
| 2026-06-29 | Hermes | R11 testemunhos + sobre | Réécriture testemunhos.html, avaliacoes-clientes.html, sobre.html | R11 (zéro invention) — "12+ Anos de Experiência" + fake testemunhos virés | 3 pages honnêtes (compromisso + CTA + équipement exact) | ✅ Fait |
| 2026-06-29 | Hermes (multi-agent) | A1 homepage Doctrine §12 | Refonte from scratch index.html : header sticky + hero + bandeau grille **70€/h** (élec, PAS 65) + Z1-Z6 + +50% + artisan local (Filipe, Staff-Seekers/Norte Reparos, "mesma pessoa") + 5 outils réels (Fluke T6-1000, Megger MFT1741+, ROLeak Aqua 3Plus, FLIR E96 43200px, caméra 30m) + 8 villes Z1-Z6 + FAQ transparente (6 questions NIF/seguro RC/fichas eletrotécnicas) + CTA NAP 932 321 892 + Schema.org Electrician géo-neutre | Doctrine §12 Transparence Radicale — pas de branche `prototype-home` ici, from scratch. R7 respecté : PR #32 ouvert + STOP merge + GO explicite Philippe. **Tarif 70€/h** maintenu (correction antérieure du bug 65→70€/h en PR #30) | Témoin AVANT=218 lignes / APRÈS=626 lignes (+623/-215). 15/15 éléments §12, **0 interdit**. Commit `54954f966`, merge squash `bfd783b25` | ✅ Fait |
| 2026-06-29 | Hermes (multi-agent) | A2 bloc Doctrine §12 services | Ajout bloc Doctrine §12 (grille **70€/h** + Z1-Z6 + +50% + artisan + 5 outils réels + NAP 932 321 892) sur top 5 services sitemap.xml × district Bragança (urgente, avaria-eletrica, fuga-corrente, quadro-eletrico, certificacao-eletrica). Contenu SEO existant préservé intentionnellement (ranking longue traîne acquis). | R7 : PR #33 ouvert + STOP merge + GO explicite Philippe | Témoin : +46/-5 sur 5 fichiers, 0 interdit **ajouté** par le bloc. Commit `4dd165311`, merge squash `7b7cf767` | ✅ Fait |
| 2026-06-29 | Hermes (multi-agent) | A2-BIS nettoyage SEO pré-existant | Suppression « Resposta prioritária/imediata » (titre H1, meta desc, og:title, CTA, FAQ), « equipa de piquete », délai chiffré « 6 min » (R145), fourchettes inventées (desde 110€/90€/180€/280€/40€), « orçamento grátis », « + Experiência », canonical cassé vers `case-study-fuga-braganca.html` sur canalizador, `<meta noindex, follow>`. Bloc Doctrine §12 (A2) **INTACT**. | Constat post-A2 : le bloc Doctrine était noyé dans le contenu SEO pré-existant non-conforme. F5 (subagent abandonné) traité par moi-même via Python. R7 : PR #34 ouvert + STOP merge + GO explicite Philippe | Témoin : 5 fichiers, +34/-34 (purement suppressif/remplacement). 0 interdit SEO restant, 1 occurrence `doctrine-transparence`/fichier (intact). NAP 932 321 892 + tarif **70 €/h** préservés. Commit `68d0bd31`, merge squash `b70364ca` | ✅ Fait |

---

**Dernière MAJ** : 2026-06-30 — **PR #56 schema LocalBusiness homepage mergée squash `24e513896`** + 0 PR ouverte restante. Branches `feat/schema-localbusiness-eu` + `cleanup/eu-residual-2026-06-30` supprimées. Audit GSC API : eletricista-urgente.pt = **3 pages indexées / 4 impressions / 0 clic en 28j** sur 1823 fichiers (~0,16%). EU contactos.html NON finalisé : 3 `tel:+351****1892` + 2 `tel:+351****4451` + 3 `info@norte-reparos.pt` à patcher (sub-agent interrompu, dette restante).
**Prochaine action** : **A4-TER cleanup résiduel final** : (1) 76 `[Aa]tendimento prioritário` survivants (fichiers hors périmètre A4-BIS initial) ; (2) 1 défaut stylistique sur `eletricista-urgente-alij.html` (double « orçamento por escrito ») ; (3) claims §11 type « Termas e património romano » à auditer. **Dette totale estimée** : ~80 fichiers, 15 min en subagent unique.

## 🤖 RÈGLES DE COORDINATION MULTI-IA

## 🤖 RÈGLES DE COORDINATION MULTI-IA

### Travail en parallèle
1. **Verrouillage logique** : ligne HISTORIQUE avec `⏳ En cours` avant de commencer
2. **HISTORIQUE en premier** : si `⏳ En cours` → attendre
3. **Pas de concurrence sur le même fichier**
4. **Mise à jour HISTORIQUE** AVANT et APRÈS
5. **Branches séparées** par agent
6. **Merge vers main** : UNIQUEMENT STOP Philippe (R7)
7. ⚠️ **JAMAIS `replace_all=true` sans unicité** (incident 28/06/2026)

### Anti-conflits
- Patch homepage : 1 agent à la fois
- Patch /zonas/ : 1 par ville
- Backlink externe : humain
- Merge : Philippe uniquement
- **Inventer : PERSONNE (R11 + R12)**
- **Mettre 65€/h ici : PERSONNE** (c'est 70€/h élec)

---

## 🧹 MÉNAGE 2026-06-30 — Réorganisation multi-sites (V2 cohérence)

**Déclencheur** : demande Philippe « tous a le même nom partout Vercel GitHub etc ? je veut une cohérence totale !! »

### Renommage pour cohérence 4×4
- ❌ `taffrand-gif/norte-reparos` → ✅ `taffrand-gif/canalizador-norte-reparos` (rename GitHub)
- ❌ `norte-reparos` projet Vercel inexistant
- ✅ Le projet Vercel `canalizador-norte-reparos` re-linké vers le nouveau repo
- ✅ GitHub redirect 301 automatique pour les anciennes URL `norte-reparos`

### Mapping final ULTRA cohérent (4×4)

| URL `.pt` | Repo GitHub | Projet Vercel |
|-----------|-------------|---------------|
| `canalizador-norte-reparos.pt` | `taffrand-gif/canalizador-norte-reparos` | `canalizador-norte-reparos` |
| `eletricista-norte-reparos.pt` | `taffrand-gif/eletricista-norte-reparos` | `eletricista-norte-reparos` |
| `canalizador-urgente.pt` | `taffrand-gif/canalizador-urgente` | `canalizador-urgente` |
| `eletricista-urgente.pt` | `taffrand-gif/eletricista-urgente` | `eletricista-urgente` |

**REGLE verrouillée** : `URL = nom_repo_GitHub = nom_projet_Vercel` pour les 4 sites.

### Pourquoi l'unique incohérence est corrigée
- Avant : `canalizador-norte-reparos.pt` ↔ repo `norte-reparos` (incohérent)
- Après : `canalizador-norte-reparos.pt` ↔ repo `canalizador-norte-reparos` (cohérent)

---


## 🧹 MÉNAGE 2026-06-30 — Réorganisation multi-sites

**Déclencheur** : demande Philippe « fait du ménage, fait en sorte que tout soit propre, bien organisé sur Vercel et GitHub ».

### Repos GitHub supprimés (backup local `/Users/admin/archives/`)
- ❌ `taffrand-gif/staff-seekers` (166 Mo, 4223 fichiers, fourre-tout historique, mort) — backup `/Users/admin/archives/staff-seekers-2026-06-30/`
- ❌ `taffrand-gif/norte-microsites` (1.3 Mo, 5 mini-sites thématiques `site1-guia-canalizacao`/`site2-dicas-eletricidade`/`site3-bricolage-casa`/`site4-energia-solar`/`site5-manutencao-casa`, jamais déployés en prod) — backup `/Users/admin/archives/norte-microsites-2026-06-30/`

### Projets Vercel supprimés
- ❌ `staff-seekers` (orphelin, aucun domaine)
- ❌ `workspace` (vide, 0 déploiement, pas de repo)
- ❌ `client` (vide, 0 déploiement, pas de repo)
- ❌ `norte-reparos-clean` (doublon détenant `canalizador-norte-reparos.pt`, a servi du contenu DOWN après incident Index.html)

### Actions correctives réalisées
- ✅ Transfert domaine `canalizador-norte-reparos.pt` : `norte-reparos-clean` (DOWN) → `canalizador-norte-reparos` (UP, lié à `taffrand-gif/norte-reparos`)
- ✅ Détachement des domaines legacy `norte-reparos.com` + `www.norte-reparos.com` (redirections historiques désactivées)
- ✅ Site `canalizador-norte-reparos.pt` restored après incident commit vide `457e56cd` (contenu réel restauré byte-à-byte via PUT /contents avec base64)

### État final propre — mapping 1-pour-1
| URL | Repo GitHub | Projet Vercel | Status |
|-----|-------------|---------------|--------|
| canalizador-norte-reparos.pt | taffrand-gif/norte-reparos | canalizador-norte-reparos | ✅ |
| eletricista-norte-reparos.pt | taffrand-gif/eletricista-norte-reparos | eletricista-norte-reparos | ✅ |
| canalizador-urgente.pt | taffrand-gif/canalizador-urgente | canalizador-urgente | ✅ |
| eletricista-urgente.pt | taffrand-gif/eletricista-urgente | eletricista-urgente | ✅ |

### Google Search Console — actions manuelles recommandées
À faire par Philippe dans `search.google.com/search-console` :
- Désenregistrer propriétés mortes : `staff-seekers.com`, `norte-reparos.com`, `www.norte-reparos.com`
- Conserver propriétés actives des 4 `.pt` + leurs sous-domaines `www.`

---


## 📝 NOTES pour les futures IA

### Contexte critique
- **Ce site viole sa propre doctrine**
- Priorité #1 = finir ce qui a été commencé

### Pièges à éviter
- ❌ Ne PAS mettre 65€/h (c'est **70€/h** ici)
- ❌ Ne PAS inventer témoignages/chantiers
- ❌ Ne PAS promettre délais chiffrés
- ❌ Ne PAS mentionner "instalação, remodelação, projeto"
- ❌ Ne PAS merger dans main sans STOP
- ❌ Ne PAS utiliser `replace_all=true` sans contexte

---

| 2026-06-29 | Hermes (multi-agent + mode loupe) | A3 Doctrine §12 services étendu | A2 (bloc Doctrine §12 variante élec : 70 €/h, NAP 932, ⚡, Staff-Seekers/Norte Reparos, équipement Fluke+Megger+ROLeak+FLIR) + A2-BIS (cleanup SEO pré-existant) sur 266 fichiers `eletricista-urgente-*.html`. Périmètre élargi de 32 (sitemap) à 266 (tout service) pour cohérence avec canalizador A3 PR #48. 1 commit `9a6e67f00`. Leçon #204 appliquée : pattern noindex quotes simples+doubles dès le premier patch, et pattern Acréscimos élargi pour capturer la formulation réelle. R7 : PR #35 ouvert + STOP merge + GO explicite Philippe | Témoins AVANT/APRÈS sur 266 fichiers : bloc_doctrine 32/266 → 266/266, noindex 266/266 → 0/266, Acréscimos mal formulés 76/266 → 0/266, desde X€ 32/266 → 0/266, orçamento grátis 19/266 → 0/266. NAP 932 321 892 + tarif 70 €/h préservés. Vérifié moi-même sur 5 fichiers random (Chaves, Mirandela, Pinhão, Torre de Moncorvo, Vila Real). Bragança intact | ✅ Fait (PR #35) |
| 2026-06-29 | Hermes (2 subagents en parallèle + mode loupe parent-side) | **A4 Doctrine §12 pages courtes** | A2 (bloc Doctrine §12) + A2-BIS (cleanup SEO pré-existant) sur **1642 fichiers courts `eletricista-{ville}.html`** à la racine (hors `concelhos/`, `distritos/`, `blog/`). NAP 932 321 892 + 70 €/h + ⚡ élec + Staff-Seekers + Megger/Fluke/ROLeak/FLIR. Subagent canalizador OK en ~6 min (37 commits), subagent eletricista partiel (patches OK sur disque mais commits interrompus) — j'ai créé 1 commit + push + PR moi-même en mode loupe (leçon #205/#209). R7 : PR #36 ouvert + STOP merge + GO explicite Philippe | Témoins AVANT/APRÈS : noindex 1552 → 0, depuis 110/140/75/120/90/85 ~1086 → 0, Resposta prioritária 1599 → 0, orçamento grátis 1577 → 180 ⚠️ (180 fichiers services A2 non retouchés par idempotence — A4-BIS), Acréscimos mal formulés 612 → 0, bloc Doctrine 266 → 1642, Fala sempre 0 → 1642, Staff-Seekers 0 → 1642. Cross-site drift (928/65 €/h/Ridgid) vérifié 0/1642. Check 6 post-mass-patch : 1 régression mineure introduite (`canalizador-bleed` +1) — corrigible en A4-BIS. Commit `7e5bcd3c5`, squash final `cab71ce09` | ✅ Fait (PR #36) |
| 2026-06-29 | Hermes (2 subagents en parallèle + mode loupe parent-side) | **A4-BIS cleanup résiduel** | **Mission #1 (typo téléphone)** : 271 fichiers `+351****1892` → `+351****4892` (typo héritée A2 PR #35). 9 commits, branche `a4-bis-cleanup-residuel`, PR #37 → merge raté (draft) → re-créé PR #39 mergé squash `ba117640`. **Mission #2 (cleanup SEO)** : 184 fichiers « orçamento gratuito » → « orçamento por escrito » (376 occ) + « Atendimento prioritário » → « atendimento mediante confirmação por telefone » (182 occ) + « Pedir orçamento gratuito » → « Pedir orçamento por escrito » (180 occ). 4 commits, branche `a4-bis-cleanup-gratis`, PR #38 mergé squash `6f72ff157`. Mode loupe parent-side : récup branche typo depuis reflog (suppression prématurée), re-push, re-Python check 1823/1823 OK. Cross-site drift 928/65 €/h/Ridgid vérifié 0. Backup `/tmp/a4-bis-backup-elec-2026-06-29/` 35 MB supprimé après merge. R7 : 2 PRs mergés en squash | Témoins AVANT/APRÈS : `+351****1892` 271 → **0**, `+351****4892` 1557 → **1823**, `orçamento gratuito` 184 → **0**, `orçamento por escrito` 1647 → **1823**, `[Aa]tendimento prioritário` 257 → **76** ⚠️ (76 fichiers hors périmètre, dette A4-TER). Check 6 post-merge : 1 défaut stylistique `alij.html` (double « orçamento por escrito »). | ✅ Fait (PR #38 + #39) |
| 2026-06-29 | Hermes (multi-agent mode loop) | **A6 fix tel: href cassés** | 10 lots (EU PR #47→#55), 2223 fichiers, tel: href cassés → vrais numéros NAP +351 932 321 892. | Session 29/06/2026 session 1 | 0 PR ouverte. ✅ Fait |
| 2026-06-29 | Hermes (multi-agent mode loop) | **fix contactos.html email** | PR #58 — 3× info@norte-reparos.pt → geral@eletricista-urgente.pt | Session 29/06/2026 session 2 | ✅ Fait (squash 3d69111fb) |
| 2026-06-29 | Hermes (multi-agent mode loop) | **fix schema LocalBusiness** | PR #56 — JSON-LD LocalBusiness homepage corrigé (tel +351 932 321 892) + enrichissement | Session 29/06/2026 | ✅ Fait (squash 24e513896) |
**Dernière MAJ** : 2026-06-28 16h30 BST
**Prochaine action** : A1 (homepage complète selon Doctrine §12, 70€/h) — en attente GO Philippe
