# RAPPORT — Mission legacy-blog-r12 — eletricista-urgente

> **Branche** : `fix/legacy-blog-r12` (basée sur `origin/main` @ `3581bee2e`)
> **Mission** : nettoyer les violations R11/R12/R145 dans `blog/*.html` pré-13/07
> **Statut** : PR DRAFT — PAS de merge (R7)

## 1. Périmètre inventorié

- **70 fichiers HTML** dans `blog/`
- Date de création des fichiers : majoritairement antérieurs au 13/07/2026 (pré-R11/R12 verrouillage)
- Aucun de ces fichiers ne contient la formule R12 obligatoire `fala sempre com a mesma pessoa, não um call center` (grep F1 = 0)

## 2. Détection des violations par grep

| ID | Pattern | Nb fichiers | Sévérité |
|---|---|---|---|
| F1 | `mesma pessoa` (R12 obligatoire) | 0 | — (manquant dans 100% du blog) |
| F2 | `em [0-9]+ min\b` (R145 strict) | 0 | — (délais courts absents) |
| F3 | `garantimos` (claims invents) | 0 | — |
| F4 | `mediante confirmação` (R145 bannis) | 6 | **HAUTE** — R145 violation stricte |
| F5 | `Resposta rápida 24h/7d` (claim délai soft) | 23 | **HAUTE** — R145 violation |
| F6 | `Resposta a confirmar` (claim délai vague) | 24 | **HAUTE** — R145 violation |
| F7 | `Atendimento prioritário` (claim délai soft) | 13 | MOYENNE — claim délai fabricated |
| F8 | `Sob marcação, mediante confirmação` (combo titre/H1) | 2 | **HAUTE** — combo titre/H1 R145 |

**Note importante** : les `em X minutos` détectés (25 fichiers) sont des **estimations techniques DIY** ("Deixe a lâmpada arrefecer 5 minutos", "Substituição 30 minutos") — c'est de la **pédagogie technique**, PAS des claims de délai de service Norte Reparos. R145 vise les claims commerciaux du type "resposta em 30 min". Les estimations DIY sont **conservées**.

## 3. Classification récupérable / irrécupérable

### A. Irrécupérable — à supprimer (1 fichier)

| Fichier | Lignes | Violations |
|---|---|---|
| `blog/eletricista-urgente-braganca-24h-premium.html` | 85 | Corruption sémantique majeure générée par IA |

**Violations observées** :
- Phrases cassées : « Ligue mediante confirmação por telefonemente: 932 321 892 »
- Phrases pétées : « Chegamos Atendemos 24h/7 dias, mediante confirmação por telefone »
- Phrases cassées : « Diagnóstico profissional com equipamento Fluke Atendemos 24h/7 dias, mediante confirmação por telefone »
- 6× « Resposta a confirmar/imediata/rápida »
- 3× « mediante confirmação »
- « Tempo de resposta: Resposta a confirmar por telefone » (claim délai soft)
- « 150-300€ » (fourchette prix hors grille R12)
- « certificação elétrica válida » (claim AGENTS.md §11 violation)
- « Chegamos em Rápida » (phrase cassée)

**Verdict** : structure entièrement pétée — patch chirurgical impossible (chaque phrase demande une réécriture complète du fichier). **À supprimer** (PR draft, PAS de suppression effective tant que GO Philippe non obtenu).

### B. Patch mécanique léger (2 fichiers)

| Fichier | Patch |
|---|---|
| `blog/avaria-eletrica-domingo.html` | Strip "Sob marcação, mediante confirmação por telefone" du titre/H1/og:title/JSON-LD ; remplacer FAQ/body Resposta |
| `blog/candeeiro-caiu-curto.html` | idem |

### C. Patch mécanique standard (24 fichiers)

Tous les fichiers de la liste `Resposta rápida 24h/7d` + `Resposta a confirmar` :

```
blog/avaria-aquecimento-eletrico.html
blog/avaria-caldeira-eletrica.html
blog/avaria-eletrica-domingo.html       (catégorie B + C)
blog/avaria-sistema-seguranca.html
blog/avaria-telecomando-portao.html
blog/cabo-eletrico-exposto.html
blog/candeeiro-caiu-curto.html          (catégorie B + C)
blog/cheiro-queimado-eletricidade.html
blog/choque-eletrico-casa.html
blog/curto-circuito-banho.html
blog/curto-circuito-cozinha.html
blog/curto-circuito-fumaca.html
blog/diferencial-nao-rearma.html
blog/disjuntor-nao-rearma.html
blog/disjuntor-dispara-noite-causas-solucoes.html
blog/eletricista-urgente-braganca-24h-premium.html   (irrécupérable — voir A)
blog/iluminacao-fundiu-totalmente.html
blog/interruptor-a-faiscar.html
blog/quadro-eletrico-a-chamas.html
blog/queda-tensao-repetida.html
blog/sem-energia-noite.html
blog/sem-luz-casa-toda.html
blog/sem-luz-parcial-urgencia.html
blog/tomada-queimada-urgente.html
blog/tomadas-derretidas.html
```

**Note** : `disjuntor-dispara-noite-causas-solucoes.html` n'a pas le pattern FAQ strict, mais contient "mediante confirmação por telefone" dans la FAQ JSON-LD et dans `<p>` body. Patch mécanique à étendre.

### D. Pas de violation R12/R11/R145 identifiée (45 fichiers)

Les 45 autres fichiers de blog ne contiennent aucune des violations R12/R11/R145 strictes. Leurs "em X minutos" sont des estimations DIY légitimes. Non touchés.

## 4. Mapping des patches canoniques (R12/R145-compliant)

| Avant (violation) | Après (R12 OK) |
|---|---|
| `Sob marcação, mediante confirmação por telefone` (titre/h1/og) | `Diagnóstico e orçamento por escrito antes de qualquer intervenção` |
| `Sob marcação, mediante confirmação por telefone` (JSON-LD headline) | `Diagnóstico e orçamento por escrito antes de qualquer intervenção` |
| `mediante confirmação por telefone` (général) | `mediante contacto telefónico e orçamento prévio por escrito` |
| `Resposta rápida 24h/7d` (FAQ JSON-LD) | `Serviço 24h/7d, com deslocação Z1–Z6 e majoração +50% noite/WE/feriado` |
| `Resposta a confirmar por telefone` (body) | `Orçamento prévio por escrito, sem surpresas` |
| `Resposta após confirmação por telefone` (meta) | `Resposta após contacto telefónico` |
| `resposta após confirmação por telefone` (meta description) | `orçamento por escrito antes de qualquer intervenção` |
| `resposta urgente Resposta rápida 24h/7d` (meta description cassée) | `orçamento prévio e deslocação Z1–Z6` |
| `Atendimento prioritário` (claim délai) | `Atendimento personalizado` |
| `Resposta imediata` (claim délai) | `Contacto imediato` |
| `Resposta rápida` (claim délai soft) | `Resposta pela mesma pessoa` |
| `Chegada Rápida` / `Chegamos Atendimento prioritário` / `Chegamos em Rápida` | `Diagnóstico no local` |

## 5. Preuves DoD (grep avant/après)

Voir `_audit/legacy-blog-r12-grep-evidence.txt` (généré à la fin).

## 6. Suite — PR draft

- Branche : `fix/legacy-blog-r12`
- Fichiers modifiés : 24 fichiers de catégorie B+C (patchs mécaniques) — **PAS** le fichier irrécupérable (suppression séparée, attente GO)
- Commit message : `fix(eu,blog): R12/R145 — strip 'mediante confirmação' + Resposta a confirmar/rápida/imediata (24 fichiers)`
- PR draft : ne pas merger, attendre GO Philippe (R3 + R7)
