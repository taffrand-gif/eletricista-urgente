#!/usr/bin/env bash
# Vercel ignoreCommand : skip deploy si diff doc-only (économie quota)
#
# Sortie:
#   exit 0 → Vercel CANCEL le deploy (skip)
#   exit 1 → Vercel CONTINUE le deploy normal
#
# Variables Vercel disponibles:
#   $VERCEL_GIT_PREVIOUS_SHA  (commit avant)
#   $VERCEL_GIT_COMMIT_SHA    (commit courant, déployé)
#   $VERCEL_GIT_REPO_OWNER, $VERCEL_GIT_REPO_NAME (si GitHub)
#
# Stratégie "fail-safe" : si git diff échoue, on EXIT 1 (= build normal).
# Ça évite de skip un deploy par bug du script.

set -u

# Cas 1: pas de previous SHA (1er commit d'une branche, force-push, etc.) → build
if [[ -z "${VERCEL_GIT_PREVIOUS_SHA:-}" ]] || [[ -z "${VERCEL_GIT_COMMIT_SHA:-}" ]]; then
  echo "[vercel-ignore] no git SHAs, build normal"
  exit 1
fi

# Cas 2: previous = current (commit identique, peut arriver en retry) → build
if [[ "$VERCEL_GIT_PREVIOUS_SHA" == "$VERCEL_GIT_COMMIT_SHA" ]]; then
  echo "[vercel-ignore] identical SHAs, build normal"
  exit 1
fi

# Récupérer la liste des fichiers modifiés
files=$(git diff --name-only "$VERCEL_GIT_PREVIOUS_SHA" "$VERCEL_GIT_COMMIT_SHA" 2>/dev/null)
diff_exit=$?
if [[ $diff_exit -ne 0 ]] || [[ -z "$files" ]]; then
  echo "[vercel-ignore] git diff failed or empty, build normal"
  exit 1
fi

# Vérifier que TOUS les fichiers modifiés sont doc-only
# Patterns doc-only autorisés:
#   *.md, *.markdown, *.txt (hors paths build)
#   *.json (mais pas package.json, tsconfig, vercel.json)
#   *.yml, *.yaml (GitHub Actions config, COURS, mais pas vercel.yml)
#   *.gitignore, *.gitattributes
#   LICENSE, CHANGELOG, README
#   SEO_PLAN.md, CLAUDE.md, AGENTS.md, .openclaw/**, docs/**
# Patterns interdits (build assets):
#   client/src/**, client/public/** (Vite sources)
#   src/**, public/** (Vite sources selon config)
#   package.json, package-lock.json (rebuild npm)
#   vercel.json, vite.config.*, tsconfig*.json
#   dist/**, build/**

DOC_ONLY=true
while IFS= read -r f; do
  case "$f" in
    # === DOCS AUTORISÉES ===
    *.md|*.markdown) continue ;;
    *.txt) continue ;;
    LICENSE|CHANGELOG|README*|CONTRIBUTING*) continue ;;
    .gitignore|.gitattributes) continue ;;
    .github/*.yml|.github/*.yaml|.github/workflows/*.yml|.github/workflows/*.yaml) continue ;;
    docs/**|docs/*) continue ;;
    .openclaw/**|.openclaw/*) continue ;;
    SEO_PLAN.md|CLAUDE.md|AGENTS.md|AGENTS_LOCAL.md) continue ;;
    # JSON safe (metadata, configs hors-build)
    *.json)
      case "$f" in
        package.json|package-lock.json|tsconfig*.json|vercel.json|vite.config.*) DOC_ONLY=false; break ;;
        client/package.json) DOC_ONLY=false; break ;;
        *) continue ;;
      esac
      ;;
    # YML safe (CI, pas config Vercel)
    *.yml|*.yaml)
      case "$f" in
        vercel.yml|.vercel.yml|vercel.yaml|.vercel.yaml) DOC_ONLY=false; break ;;
        *) continue ;;
      esac
      ;;
    # === TOUT LE RESTE = BUILD NÉCESSAIRE ===
    *)
      DOC_ONLY=false
      break
      ;;
  esac
done <<< "$files"

if [[ "$DOC_ONLY" == "true" ]]; then
  echo "[vercel-ignore] diff doc-only ($(echo "$files" | wc -l | tr -d ' ') files), CANCEL deploy"
  echo "[vercel-ignore] files: $(echo "$files" | tr '\n' ' ')"
  exit 0
else
  echo "[vercel-ignore] diff contains build files, build normal"
  exit 1
fi
