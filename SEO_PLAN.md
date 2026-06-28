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

**Statut** : ⏳ À FAIRE
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

---

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

**Dernière MAJ** : 2026-06-28 16h30 BST
**Prochaine action** : A1 (homepage complète selon Doctrine §12, 70€/h) — en attente GO Philippe
