---
name: priority-gate
description: La file d'action vit dans ~/work/Sites/PLAN_ACTION_CEO_<DATE>.md (le plus récent). Prendre l'item #1 NON FINI. Saut = uniquement GO explicite Filipe, cité dans le commit. "Fini" = self-audit à ZÉRO, pas déclaration. Trigger : "quelle mission maintenant", "ordre des tâches", "next step", "sauter P0.5", "faire M3 avant P0.5".
---

# priority-gate — File CEO d'abord (S4, mission P0.5, 02/07/2026)

> **Pourquoi** : le défaut #4 de la baseline 02/07 est **la file de priorités
> ignorée** — item M3 (rang #10) exécuté AVANT P0.5 (rang #1) sans GO.
>
> Tu optimises "tâche déclarée faite" au lieu de "état final conforme à la file".

## La source unique

**Fichier** : `~/work/Sites/PLAN_ACTION_CEO_<DATE>.md` (le plus récent).
- 02/07 : `~/work/Sites/PLAN_ACTION_CEO_2026-07-02.md`
- À chaque nouveau plan CEO, le précédent est archivé (vérifier dans `_audit/`).

## Structure de la file (sections 1-4 du plan)

1. **§1 Verdict travail Hermes** — état du dernier batch.
2. **§2 Décisions Filipe (D1-D5)** — blocantes, à demander.
3. **§3 File d'action priorisée ROI** — la file elle-même (items #1 à #N).
4. **§4 KPI de contrôle** — comment re-mesurer après exécution.

## Règle d'or

> **Toujours prendre l'item #1 NON FINI de la §3.**
> Sauter un item = uniquement avec **GO explicite Filipe cité dans le commit**.

## Définition de "fini" (la seule qui compte)

> **Un item est "fini" quand `self-audit-zones.py` retourne 0 KO sur son périmètre.**

PAS quand :
- ❌ Le commit est créé (commit ≠ état final).
- ❌ Le PR est draft (draft ≠ mergé ≠ en prod).
- ❌ "J'ai l'impression que c'est propre" (impression ≠ mesure).

## Quand tu DOIS demander GO à Filipe

1. **Saut d'item** : tu veux faire #5 alors que #1 n'est pas fini → STOP, GO.
2. **Décision D1-D5** pendante : tu ne sais pas trancher → STOP, GO (cite Dx).
3. **NO_RESOL > 50 pages** : tu ne peux pas patcher en lot → STOP, GO stratégie
   (fallback concelho vs prune vs autre).
4. **Conflit avec règle verrouillée R1-R12** : tu détectes une contradiction →
   STOP, signale.

## Format de citation GO dans le commit

```
fix(CNR): P0.5 normalisation page entière vague 1 (16 fichiers)

GO Filipe (Telegram 02/07 16h12) : "GO vague 1 sur CNR, max 16 fichiers,
patch sur toutes surfaces ensemble". Saut de l'item #10 (M3 GEO) car P0.5
item #1 = priorité ROI. Cf. MISSION_HERMES_P0.5_2026-07-02.md.

[Sortie self-audit-zones.py]
Avant : 211 KO badge≠JSON-LD + 4 JSON-LD prix faux
Après : 0 KO sur les 16 fichiers patchés
```

## Lien avec les autres skills

- **S1 (self-audit-batch)** : la mesure "fini" = 0 KO au script.
- **S2 (definition-of-done-page)** : si tu fais un item de la file, applique S2
  sur les surfaces patchées.
- **S3 (source-of-truth-first)** : si l'item implique création de contenu neuf,
  recharge la source.
- **S5 (clean-tree)** : tu ne commences PAS un item de la file sur un tree sale.

## Réflexe à avoir en début de session

```
1. cd ~/work/Sites/
2. cat PLAN_ACTION_CEO_*.md | head -100   # lire §3 file
3. Identifier item #1 NON FINI
4. self-audit-zones.py sur le périmètre → confirmer KO > 0
5. Si oui : c'est ton item. Si non : l'item est fini → passer au #2.
6. Lancer la mission avec sortie self-audit jointe au commit final.
```

## Pièges classiques

- **"M3 c'est plus visible, je le fais en premier"** : NON. ROI ≠ visibilité.
  P0.5 ferme la conformité, M3=l'offensif. Conformité AVANT offensif.
- **"Le PR est draft, c'est comme mergé"** : NON. Draft = 0 ROI utilisateur.
- **"J'ai fait 90% de P0.5, je passe à P0.3"** : NON. 90% ≠ 100% ≠ 0 KO.
  Finir P0.5 d'abord.
- **"Filipe a dit 'fais ce que tu penses être bien'"** : ce n'est PAS un GO
  pour sauter un item. Demander explicitement.

## File actuelle (snapshot 02/07 15h45)

```
#1 P0.5 normalisation PAGE ENTIÈRE (4 repos, ~3h)
#2 P0.5c doublons CNR (CNR seul, ~1h)
#3 Merge 4 PRs P0/P0.5 (post-vérif, ~30min)
#4 P0.3 purge faux avis GoogleReviews (CNR+ENR, ~1h) — risque légal
#5 P0.1 fin purge body (4 repos, ~2h30)
#6 D1 purge "Chegada ~min" CNR + D2 purge "mediante confirmação"
#7 M1 maillage hub↔localité (CNR/ENR d'abord)
#8 P0.2/M2 différenciation intent norte vs urgente
#9 P6.3 pilote keywords Bragança
#10 M3 GEO pages datées
#11 P5 backlinks blancs (continu)
```

→ **item #1 = P0.5 normalisation page entière**. C'est TON item par défaut.