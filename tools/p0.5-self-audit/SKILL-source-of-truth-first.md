---
name: source-of-truth-first
description: Avant de CRÉER ou MODIFIER tout contenu avec prix/zone/distance/délai/tél, recharger la source unique (zonas-data.json + grille OSRM + doctrine R12). Jamais de valeur métier depuis ta mémoire de session. Trigger : "créer page localité", "page M3 datée", "nouveau service", "fichier preco-", "page zona-".
---

# source-of-truth-first — Recharger la source AVANT tout contenu neuf (S3, mission P0.5, 02/07/2026)

> **Pourquoi** : le défaut #3 de la baseline 02/07 est **la grille périmée sur
> contenu NEUF** — pages M3 Bragança créées avec **Z3/35€** alors que la grille
> OSRM corrigée (**Z2/25€**) existait le jour même.
>
> Cause : tu as utilisé ta **mémoire de session** (ce que tu savais avant) au lieu
> de **recharger la source unique** au moment de la création.

## Sources de vérité (OBLIGATOIRE de recharger AVANT création)

### 1. `~/work/Sites/norte-os-marketing/prototypes/zonas-data.json`
**Quoi** : mapping localité → zone (1..6), 914 entrées.
**Pourquoi recharger** : les communes changent de zone après audit OSRM.
**Commande** :
```bash
python3 -c "import json; z=json.load(open('$HOME/work/Sites/norte-os-marketing/prototypes/zonas-data.json')); print('Bragança →', z['Bragança'])"
```

### 2. Grille OSRM officielle (dans `PLAN_ACTION_CEO_*.md` et `AGENTS.md` §12)
```
Z1 = 15 €  (0-22 km)
Z2 = 25 €  (23-43 km)
Z3 = 35 €  (44-65 km)
Z4 = 45 €  (66-87 km)
Z5 = 55 €  (88-109 km)
Z6 = 65 €  (110-130 km)
```
**Pourquoi recharger** : peut être révisée après audit OSRM (leçon #298).
**Où lire** : `~/work/Sites/PLAN_ACTION_CEO_2026-07-02.md` §1 et chaque `AGENTS.md` §12.

### 3. Doctrine R12 (`AGENTS.md` §12 de chaque repo)
- 65 €/h canalização · 70 €/h eletricidade.
- +50% nuit/WE/feriado.
- Phrase obligatoire "orçamento por escrito antes de qualquer intervenção, sem surpresas".

### 4. Tarifs services (CNR/ENR, R12 verrouillée)
- CNR : orçamento por escrito em 48h, sem compromisso.
- ENR : orçamento por escrito em 48h, NAP 932 321 892.

### 5. NAP (Name Address Phone) par repo
- canalizador-urgente.pt : 928 484 451
- eletricista-urgente.pt : 932 321 892
- canalizador-norte-reparos.pt : 928 484 451
- eletricista-norte-reparos.pt : 932 321 892

## Procédure obligatoire AVANT de créer une page avec prix/zone

```
□ 1. Lire zonas-data.json pour la localité cible (recharger, pas mémoire).
□ 2. Vérifier la grille OSRM dans PLAN_ACTION_CEO (recharger).
□ 3. Vérifier la doctrine R12 dans AGENTS.md du repo cible.
□ 4. Composer la page avec UNIQUEMENT ces valeurs.
□ 5. AVANT commit : lancer self-audit-zones.py (S1) sur la page → KO doit être 0.
□ 6. Commit avec mention "créé depuis source-of-truth rechargée <date>".
```

## Anti-pattern (log en leçon #329-ter)

**Symptôme** : page M3 Bragança créée avec Z3/35€, alors que la source dit Z2/25€.

**Cause** : tu as copié le pattern d'une autre page (ex: Chaves Z4/45€) et tu as
adapté SANS relire la source pour Bragança.

**Prévention** : règle S3 ci-dessus. Recharger **avant** d'écrire la première
ligne de HTML.

## Cas particuliers à surveiller

- **Communes à la frontière entre 2 zones** : vérifier la valeur exacte dans
  zonas-data.json (ex: Vimioso = 3, pas 2).
- **Pages datées `-2026.html`** : ce sont les pages M3 (GEO). Elles doivent
  refléter la grille la plus à jour, pas la grille du brief initial.
- **Pages -es (espagnol)** : peuvent avoir une grille différente
  (le périmètre P0 exclut -es, mais vérifier si tu dois en créer).

## Lien avec les autres skills

- **S1 (self-audit-batch)** : applique le script APRÈS création pour confirmer
  que tu as bien utilisé la source (KO = 0).
- **S2 (definition-of-done-page)** : si la source dit zone X, tu dois patcher
  les 8 surfaces en X (pas juste le badge).
- **S4 (priority-gate)** : si la mission est "M3 nouvelles pages", c'est
  l'item #10 du PLAN (low priority tant que P0.5 n'est pas mergé).

## Mémoire de session vs source de vérité

| Type de donnée | Source de vérité | Risque si mémoire |
|---|---|---|
| Zone d'une localité | `zonas-data.json` | ÉLEVÉ (change après audit OSRM) |
| Tarif Z1..Z6 | `PLAN_ACTION_CEO` §1 + `AGENTS.md` §12 | MOYEN (rarement révisé) |
| Tarif horaire | `AGENTS.md` §12 | FAIBLE (R12 verrouillé) |
| NAP téléphone | `AGENTS.md` périmètre | FAIBLE |
| Horaires | `AGENTS.md` §12 | FAIBLE |

**Règle** : pour TOUT ce qui a une source externe (zones, prix, NAP), recharger
AVANT d'écrire. Pour les règles verrouillées R12, citer l'AGENTS.md du repo.