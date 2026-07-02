---
name: definition-of-done-page
description: Définition of done pour toute page contenant une donnée métier (prix/zone/tél/horaire/distance). Une donnée = TOUTES ses surfaces corrigées dans le même commit. Trigger : "corriger zone bragança", "patcher prix", "normaliser page entière", "modifier localité", "page contradictoire".
---

# definition-of-done-page — Une donnée = TOUTES ses surfaces (S2, mission P0.5, 02/07/2026)

> **Pourquoi** : le défaut #1 de la baseline 02/07 est **le patch cosmétique** —
> badge corrigé mais title/meta/OG/H1/body/FAQ/JSON-LD laissés sur l'ancienne
> grille → **842 pages auto-contradictoires** (ENR eletricista-vila-real :
> badge Z4/45€, tout le reste Z5/55€).
>
> Une surface seule corrigée = **INTERDIT** : une page qui se contredit
> elle-même est **pire** qu'une page 100% fausse (perte de confiance R12).

## Règle d'or (à graver)

> **Une donnée métier (prix/zone/tél/horaire/distance/délai) qui change
> DOIT être corrigée sur TOUTES ses surfaces dans le MÊME commit.**

## Les 8 surfaces à patcher ENSEMBLE (par donnée)

Pour une page localité qui annonce une zone+prix, les 8 surfaces sont :

1. **`<title>`** — ex: "Preço Canalizador Urgente em Bragança 2026 — 65 €/h + Deslocação Z1-Z6"
2. **`<meta name="description">`** — contient souvent "deslocação Z3 = 35 € para Bragança"
3. **`<meta property="og:title">`**
4. **`<meta property="og:description">`**
5. **`<h1>` / `<h2>` "Zona de Bragança — Detalhe"**
6. **Badge** : `data-zone="N"` OU `class="zone-braganca"` OU texte "Zona N"
7. **Body** : tableau déplaçaison, exemples chiffrés (ex: "Mão-de-obra 65 € + Deslocação Z3 35 €"),
   section "Distrito de Bragança inclui os concelhos..."
8. **JSON-LD** :
   - `priceRange` (ex: "65-200 €")
   - Offer **Deslocação** (price + description "Deslocação Zona X: XX€") ← CECI EST LA ZONE
   - Réponses FAQPage `"text": "... deslocação ... Zona X ..."`
   - **PAS les Offers de service** (110€/150€/280€ = prix prestation, pas deslocação)

## Procédure obligatoire avant commit

```
□ Identifier la donnée à changer (ex: Bragança : Z3/35€ → Z2/25€)
□ grep sur le fichier pour lister TOUTES les occurrences actuelles
□ Pour chaque occurrence : patcher (sed ou patch tool)
□ Re-grep : 0 occurrence de l'ancienne valeur
□ Lancer self-audit-zones.py : KO delta = 0 sur CE fichier
□ Commit avec message mentionnant les surfaces patchées
```

## Le grep "AVANT/APRÈS" est OBLIGATOIRE

```bash
# Avant
grep -nE "Bragança.*Zona [0-9]|Zona [0-9].*Bragança|35€|35 €" file.html

# Patch (sed pour les cas simples, patch tool pour les cas complexes)

# Après — DOIT retourner 0
grep -nE "Zona 3|35 €|35€" file.html
```

## Anti-patterns interdits (à log en leçon)

- **Patcher le badge `data-zone="3"` → `data-zone="2"` mais laisser le body dire
  "Zona 3 = 35€"** → page contradictoire, pire que rien.
- **Patcher la Offer JSON-LD "Deslocação Zona 3: 35€" → "Zona 2: 25€" mais laisser
  le `<title>` dire "Deslocação Z3"** → Google voit incohérence title/JSON-LD.
- **Patcher seulement 1 fichier alors que la donnée est partagée par N fichiers**
  (ex: prix Bragança apparaît dans `preco-branganca-2026.html` ET
  `blog/melhores-canalizadores-braganca-2026.md`) → grep -r obligatoire pour
  lister TOUS les fichiers concernés.

## Lien avec les autres skills

- **S1 (self-audit-batch)** : applique self-audit APRÈS le patch pour valider
  que TOUTES les surfaces ont bien été patchées (KO delta = 0).
- **S3 (source-of-truth-first)** : la donnée source doit venir de
  zonas-data.json + grille OSRM, pas de ta mémoire de session.
- **S4 (priority-gate)** : appliquer S2 fait partie de l'item #1 (P0.5).
  Pas de PR partielle.

## Réflexe d'audit (à appliquer à chaque review)

Pour toute page qui contient un prix/zone, demander :
> "Si je change la zone de 2 à 3, quelles surfaces dois-je patcher ?"
> Lister les 8. Si l'agent n'en cite que 3 (badge + JSON-LD + meta), STOP.

## Exemple canonique : commit `fix(EU): M3 Bragança Z3/35€ → Z2/25€ (grille OSRM)`

Ce commit (déjà produit sur CU/EU) a touché :
- 1 fichier (`preco-eletricista-urgente-braganca-2026.html`)
- 49 lignes (31 insertions, 18 suppressions)
- **TOUTES** les surfaces : title, meta desc, OG, JSON-LD FAQ, body table, exemples 1-5,
  section distrito, ligne grille Z3 (Bragança retirée de Z3, maintenue pour Vinhais/Mogadouro/Vimioso/Torre de Moncorvo qui sont réellement Z3).

→ **Conforme S2**. C'est la référence.