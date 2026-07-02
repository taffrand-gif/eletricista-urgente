---
name: clean-tree
description: Hook début+fin de mission : git status --porcelain sur les 4 repos. Non-vide en début → committer/reverter d'abord. Non-vide en fin → mission pas finie. Trigger : "git status", "uncommitted changes", "SEO_PLAN.md sale", "avant mission", "fin de mission", "vérifier tree".
---

# clean-tree — Tree propre début ET fin (S5, mission P0.5, 02/07/2026)

> **Pourquoi** : le défaut #5 de la baseline 02/07 est **dirty tree** —
> SEO_PLAN.md non commité sur les 4 repos. Cause : pas de hook début/fin
> de mission pour vérifier que les fichiers de coordination (SEO_PLAN.md,
> MISSION_*.md) sont committés.
>
> Conséquence : ton travail de la veille est "perdu" tant que pas commité,
> et le prochain agent qui ouvre le repo voit un état incohérent.

## Hook début de mission

**AVANT** de commencer tout travail (avant même `cd` dans un repo) :

```bash
for repo in ~/work/Sites/canalizador-urgente \
            ~/work/Sites/eletricista-urgente \
            ~/work/Sites/canalizador-norte-reparos \
            ~/work/Sites/eletricista-norte-reparos; do
  echo "=== $repo ==="
  cd "$repo" || continue
  if [ -n "$(git status --porcelain)" ]; then
    echo "⚠ TREE SALE — lister les fichiers et committer/reverter"
    git status --short
    # 2 options :
    #   (a) git add -A && git commit -m "docs: WIP session <date>"  (garder)
    #   (b) git checkout -- .                                       (perdre)
    # Choisir selon contexte : si SEO_PLAN.md ou MISSION_*.md → (a) garder.
  else
    echo "✓ tree clean"
  fi
done
```

**Règle** : tree sale en début → STOP, ne PAS commencer la mission tant que
non committé/reverté. Une mission sur tree sale = invalidation garantie
des résultats (les fichiers que tu patches ne sont peut-être pas ceux du HEAD).

## Hook fin de mission

**AVANT** de considérer la mission comme "finie" :

```bash
for repo in ~/work/Sites/canalizador-urgente \
            ~/work/Sites/eletricista-urgente \
            ~/work/Sites/canalizador-norte-reparos \
            ~/work/Sites/eletricista-norte-reparos; do
  echo "=== $repo ==="
  cd "$repo" || continue
  if [ -n "$(git status --porcelain)" ]; then
    echo "⚠ TREE SALE — fichiers non commités :"
    git status --short
    # 2 options :
    #   (a) commit avec le contexte (preferred pour SEO_PLAN, MISSION)
    #   (b) revert si c'est un test scratch (git checkout -- .)
  fi
done
```

**Règle** : tree sale en fin = **la mission N'EST PAS finie**, même si
self-audit-zones.py retourne 0 KO. Tu dois committer le SEO_PLAN.md
mis à jour + les éventuels scratch.

## Fichiers typiquement en cause

| Fichier | Action |
|---|---|
| `SEO_PLAN.md` | Commit obligatoire (mémoire vivante, doit être HEAD) |
| `MISSION_HERMES_*.md` | Commit obligatoire (référence pour la mission) |
| `.hermes/` | Commit si config agent, sinon vérifier `.gitignore` |
| `_reports/`, `_prototype/` | Commit si livrable, sinon revert |
| `*.html.tmp`, `*.bak` | **Toujours revert** (scratch) |

## Cas spéciaux

- **Branche de travail** : `fix/prix-zones-osrm` (P0/P0.5). Si tree sale sur
  cette branche, commit + push même si PR est draft. Sinon le travail est
  local et non reviewable.
- **Working copy stale** (`norte-reparos/` à l'ancienne) : NE PAS toucher,
  c'est une copie à abandonner (cf. `AGENTS.md` §périmètre).
- **Branche `main`** : JAMAIS de dirty tree en fin de session sur main
  (la prod est en direct).

## Lien avec les autres skills

- **S1 (self-audit-batch)** : self-audit ne mesure que les fichiers commités.
  Si tree sale, self-audit voit l'ancien état.
- **S2 (definition-of-done-page)** : un patch partiel commité mais d'autres
  fichiers touched = sale, donc invalide S2.
- **S4 (priority-gate)** : tu commences l'item #1 sur tree clean, tu termines
  sur tree clean (le commit de l'item fait partie de "fini").

## Commande rapide (alias suggéré)

```bash
# À mettre dans ~/.zshrc ou ~/.bashrc
alias nr-clean="for r in ~/work/Sites/canalizador-urgente ~/work/Sites/eletricista-urgente ~/work/Sites/canalizador-norte-reparos ~/work/Sites/eletricista-norte-reparos; do echo \"=== \$r ===\"; cd \"\$r\" && (git status --short || echo 'tree clean'); done"
```

→ Tu tapes `nr-clean` au début et à la fin de chaque session.