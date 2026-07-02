---
name: self-audit-batch
description: Audit mécanique des pages localité vs source-of-truth (zonas-data.json + grille OSRM Z1=15€..Z6=65€). À utiliser AVANT tout commit de batch touchant prix/zone/distance. Trigger : "audite les zones", "vérifie les badges data-zone", "combien de KO sur ce repo", "passe self-audit sur CNR/CU/EU/ENR", "compare page à la grille officielle".
---

# self-audit-batch — Audit mécanique (S1, mission P0.5, 02/07/2026)

> **Pourquoi** : remplacer les claims subjectifs (« 0 mismatch », « propre ») par des
> **chiffres reproductibles**. Le barème prochain audit donne +2 si la sortie du script
> est jointe au commit de batch. Interdit d'écrire « 0 KO » sans coller le chiffre.

## Le script

**Localisation** : `~/.openclaw/workspace/scripts/self-audit-zones.py`

**Source unique de vérité** :
- `~/work/Sites/norte-os-marketing/prototypes/zonas-data.json` (914 localités, Z1-Z6)
- Grille OSRM : `Z1=15€ / Z2=25€ / Z3=35€ / Z4=45€ / Z5=55€ / Z6=65€`

**Ce qu'il vérifie (4 catégories de KO)** :
- **KO1** : `data-zone="N"` ≠ zonas-data.json (slug strip préfixes service)
- **KO2** : JSON-LD `"Deslocação Zona X"` ≠ attendu
- **KO2bis** : badge ≠ JSON-LD (page contradictoire interne)
- **KO3** : prix body (mention "Zona N ... XX€") ≠ grille officielle
- **KO4** : délais chiffrés `(?i)(tempo|chegada|resposta)[^<]{0,40}\d{1,3} min` (R145 strict sur `-urgente`, info sur `-norte`)

**Témoins (R8 OpenClaw)** : Bragança=Z2/25€ · Vinhais=Z3/35€ · Macedo CV=Z1/15€.

## Usage

```bash
# Un repo
python3 ~/.openclaw/workspace/scripts/self-audit-zones.py ~/work/Sites/canalizador-urgente

# Les 4 repos
python3 ~/.openclaw/workspace/scripts/self-audit-zones.py \
  ~/work/Sites/canalizador-urgente \
  ~/work/Sites/eletricista-urgente \
  ~/work/Sites/canalizador-norte-reparos \
  ~/work/Sites/eletricista-norte-reparos
```

Sortie : par repo (HTML total · patched · no_resol · KO1 · KO2 · KO2bis · KO3 · KO4) + témoins.

## Règles d'engagement

1. **AVANT tout commit de batch touchant prix/zone/distance** :
   - Lancer le script sur le(s) repo(s) concerné(s).
   - Coller la sortie dans le message de commit (format compact).
2. **Le commit DOIT afficher le delta KO** :
   - Avant patch : N KO (catégorie par catégorie)
   - Après patch : M KO (delta = N - M)
   - Si delta = 0 et N > 0 → le patch est cosmétique (warning skill S2).
3. **Interdit d'écrire "0 KO" ou "clean" sans chiffre brut**.
4. **Témoins** : si l'un des 3 témoins (Bragança/Vinhais/Macedo CV) n'est pas
   conforme dans la sortie, **STOP** — la grille a peut-être changé, mettre à jour
   la constante TEMOINS dans le script.
5. **NO_RESOL ≠ OK** : NO_RESOL = localité non trouvée dans zonas-data.json
   (décision D3 Filipe pendante). Ne JAMAIS classer une page NO_RESOL comme "patched".

## Étalonnage baseline 02/07 (validé par CEO audit)

| Repo | KO1 attendu | KO1 mesuré |
|---|---|---|
| CU | 16 | 16 ✓ |
| EU | 29 | 29 ✓ |
| CNR | 58 | 58 ✓ |
| ENR | 71 | 71 ✓ |
| **TOTAL** | **174** | **174** |

Le script matche la baseline CEO. Tout écart > 5% = investigation immédiate
(la grille a changé ou un batch non documenté a eu lieu).

## Périmètre exclu

- Pages `-es.html` (version espagnole — décision antérieure P0).
- `dist/`, `build/`, `node_modules/`, `_archive/`, `.hermes/`, `.git/`.

## Limites connues (V1 — à étendre si besoin)

- Préfixes service gérés : `fuga-agua-`, `desentupimento-`, `fossa-septica-`,
  `canalizacao-nova-`, `curto-circuito-`, `quadro-eletrico-`, `instalacao-eletrica-`,
  `avaria-eletrica-`, `canalizador-`, `eletricista-`.
- **Non gérés V1** : `esquentador-`, `autoclismo-`, `torneira-`, `pressao-agua-`,
  `urgente-` (quand séparé du préfixe métier), `paco-` (vs `paço`). Ces pages
  tombent en NO_RESOL et sont à étendre dans une V2 si la mission l'exige.
- KO2 (JSON-LD strict "Deslocação Zona X" en description) est plus restrictif
  que l'audit CEO qui regarde aussi les autres champs JSON-LD.

## Lien avec les autres skills (S2-S5)

- **S2 (definition-of-done-page)** : si KO post-patch > 0 sur les surfaces patchées
  → violation de S2.
- **S3 (source-of-truth-first)** : si tu utilises des prix/zone depuis ta mémoire
  de session au lieu de zonas-data.json, S1 te le dira via KO élevé.
- **S4 (priority-gate)** : tu ne dois PAS sauter l'item #1 du PLAN_ACTION_CEO pour
  exécuter un audit self-audit en parallèle sans GO.
- **S5 (clean-tree)** : tu ne dois PAS lancer self-audit sur un tree sale.