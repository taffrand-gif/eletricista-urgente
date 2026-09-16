# FPP réfuté — scope-electric-on-plumbing em eletricista-braganca.html

**Tâche** : `t_938087ad` (pool-keeper signal 2026-09-14)
**Branche** : `fix/eu-braganca-scope-electric-fpp-t_938087ad`
**Base** : `origin/main@1b572563cfc`
**Date** : 2026-09-14

## Verdict

**FAUX POSITIF** — la violation `scope-electric-on-plumbing` n'existe ni en prod
publique, ni sur `origin/main`, ni sur la branche fraîche `fix/eu-braganca-scope-electric-fpp-t_938087ad`.

L'extrait signalé provient **uniquement** du patch DRAFT de la PR #384
(`fix/eu-gsc-gap-eletricista-braganca-t_35f59179`, commit `796ec75fc`),
qui a ajouté un bloc "Quando chamar um eletricista em Bragança" — liste technique
100% élec : disjuntor que dispara, curto-circuito, fuga de corrente,
tomadas quentes, cheiro a queimado, quadro elétrico, certificação DGEG.

## Cause du faux signal

Le détecteur regex matche la sous-chaîne **`fuga`** sans distinguer :

- `fuga de corrente` (terme technique élec — earth-leakage differential-trip diagnosis,
  scope élec strict, équipement Megger MFT1741+ + Fluke T6-1000)
- `fuga de água` (plomberie — réseau hydraulique sous pression)

**Collision lexicale récurrente** — même classe de FP que :

- `t_869cc997` (vilar-de-macada)
- `t_22dd3b18` (argozelo)
- `t_1c4ea453` (amarante)
- `t_44cdcde1` (cedovim)
- `t_df870168` (cambres)
- `t_24099f7e` (calculadora-de-preco)
- `t_bf6a4791` (santo-estevao)
- `t_7ec530ae` (cumieira)

## Preuves live — branche fraîche (origin/main)

### Extrait signalé — 0/5 occurrences

```
fuga de corrente         = 0
curto-circuito           = 0
Tomadas ou interruptores quentes = 0
Queda total de luz       = 0
Quando chamar um eletricista     = 0
```

### Termes plomberie (visible body) — 0/14

```
torneira, fossa, esgoto, autoclismo, chuveiro, esquentador, piscina,
entup, sumidouro, fuga de água, lavatório, sifão, ralo, vazamento → tous 0
```

Seule occurrence `canalizador` = JSON-LD `sameAs` (backlink cross-site conforme
Annexe A — `canalizador-norte-reparos.pt` / `canalizador-urgente.pt`).

### Doctrine §12 intacte

```
70 €/h       = 1
70€/h        = 2
Zona 3       = 1
Z3           = 1
932 321 892  = 8
orçamento por escrito = 5
TRIESP       = 2
DGEG         = 4
Fluke        = 3
Megger       = 1
```

### Preuve prod publique (curl https://eletricista-urgente.pt/eletricista-braganca.html)

```
fuga de corrente                  = 0
curto-circuito                    = 0
Tomadas ou interruptores quentes  = 0
```

→ La violation n'est **pas en production**.

## Audit R145 + R11 — branche fraîche

```
em 30 minutos, em 20 minutos, em 15 minutos, em 10 minutos  → 0/0/0/0
resposta em, resposta rápida, chegada em                    → 0/0/0
resposta prioritária, atendimento imediato, imediatamente   → 0/0/0
resposta confirmada por chamada                              → 0

trabalhos realizados, trabalhos recentes                    → 0/0
caso de, história de, obra em                               → 0/0/0
cliente satisfeito, testemunho de                           → 0/0
```

Aucun délai chiffré inventé (R145 ✓), aucune invention service/avis (R11 ✓).

## Décision retenue

- **Aucun correctif HTML requis** — la page `eletricista-braganca.html` sur
  `origin/main` est déjà conforme à PRICING.md, R11, R12, R145, R7 et Doctrine §12.
- **PR DRAFT ouverte** pour traçabilité gouvernance (R7 STOP merge).
- **Aucun merge auto** — gated R7, attente GO Filipe.

## Recommandation pool-keeper

Le détecteur `scope-electric-on-plumbing` devrait matcher **expressions complètes**
(`fuga de água` | `cano rebentado` | `cano entupido` | `torneira a pingar` |
`esgoto a transbordar` | `válvula de segurança` | etc.) plutôt que la sous-chaîne
`fuga` — sinon il continuera à flagger en FP toutes les pages élec qui mentionnent
`fuga de corrente` (terme R12 doctrine §12).

## Conformité R7 (zéro merge auto)

- PR DRAFT en attente GO Filipe explicite (gate AGENTS.md §14 cycle élec + R7).
- Aucun push direct sur main.
- Branche `fix/eu-braganca-scope-electric-fpp-t_938087ad` réutilisable par le pool-keeper
  si une autre occurrence du même FP est signalée sur cette page.