#!/usr/bin/env python3
"""
patch_ga4_t_e145af0d.py — Patch GA4 tracking sur les 4 sites CNR/ENR/CU/EU.

Injecte (ou upgradge) le tag GA4 + helpers click_tel/click_whatsapp dans le <head>
de chaque fichier HTML qui ne l'a pas sous la forme standardisée.

Idempotent :
  - Marker absent                                → injecte le bloc standard après <head>
  - Marker présent, bloc PARTIAL (config seul)   → remplace par le bloc standard
  - Marker présent, bloc COMPLET (avec helpers)  → skip

Détection du bloc COMPLET = contient le marker ET `send_page_view` ET `click_tel`
Détection du bloc PARTIAL = contient le marker SANS `send_page_view`
                            (typiquement : `gtag('config', 'X-XXXXX');` seul)

Témoins : rapport avant/après + sample de 3 fichiers inspectés.

Usage :
  python3 patch_ga4_t_e145af0d.py --site CNR --root <worktree-path>
  python3 patch_ga4_t_e145af0d.py --site ENR --root <worktree-path>
  python3 patch_ga4_t_e145af0d.py --site CU --root <worktree-path>
  python3 patch_ga4_t_e145af0d.py --site EU --root <worktree-path>

Auteur : Hermes (kanban t_e145af0d, run 04-05/08/2026)
Doctrine : R8 témoins obligatoires, R3 STOP validation (jamais push/merge auto).
"""
import argparse
import re
import sys
from pathlib import Path

# (site, property_id, tag_marker)
# default_excludes : chemins RELATIFS À LA RACINE DU WORKTREE à NE JAMAIS scanner.
# Logique :
#   - CNR/ENR : `client/index.html` = React shell avec helpers (`trackPhoneClick`)
#     appelés par le code React → NE PAS toucher (sinon on casse les events).
#     `client/public/index.html` = artefact non servi à la racine (Vite sert
#     `dist/public/index.html` depuis `client/index.html`). Pas dans le path
#     critique ; exclu par prudence.
#   - CU/EU : pas de React, structure statique pure. Tous les .html sont candidats
#     y compris `public/index.html` (page d'accueil historique qui était bare).
DEFAULT_EXCLUDES_PER_SITE = {
    "CNR": ["client/index.html", "client/public/index.html"],
    "ENR": ["client/index.html", "client/public/index.html"],
    "CU": [],
    "EU": [],
}

SITES = {
    "CNR": {
        "property_id": "G-VWSWFQB71H",
        "site_label": "canalizador-norte-reparos.pt",
        "marker": "G-VWSWFQB71H",
    },
    "ENR": {
        "property_id": "G-P0521CSGHY",
        "site_label": "eletricista-norte-reparos.pt",
        "marker": "G-P0521CSGHY",
    },
    "CU": {
        "property_id": "G-65XLQV88LM",
        "site_label": "canalizador-urgente.pt",
        "marker": "G-65XLQV88LM",
    },
    "EU": {
        "property_id": "G-ZWNCKFYGRK",
        "site_label": "eletricista-urgente.pt",
        "marker": "G-ZWNCKFYGRK",
    },
}


def build_block(site: str) -> str:
    """Bloc GA4 standard à injecter juste après <head>."""
    cfg = SITES[site]
    pid = cfg["property_id"]
    return (
        f'<!-- GA4 — {cfg["site_label"]} {pid} (injecté 2026-08-04, mission t_e145af0d) -->\n'
        f'<script async src="https://www.googletagmanager.com/gtag/js?id={pid}"></script>\n'
        f'<script>\n'
        f'window.dataLayer = window.dataLayer || [];\n'
        f'function gtag(){{dataLayer.push(arguments);}}\n'
        f'gtag(\'js\', new Date());\n'
        f'gtag(\'config\', \'{pid}\', {{\'send_page_view\': true, \'anonymize_ip\': true, \'cookie_flags\': \'SameSite=None;Secure\'}});\n'
        f'window.trackTelClick = function(phone) {{ gtag(\'event\', \'click_tel\', {{\'event_category\': \'conversion\', \'event_label\': phone, \'value\': 1}}); }};\n'
        f'window.trackWhatsAppClick = function(source) {{ gtag(\'event\', \'click_whatsapp\', {{\'event_category\': \'conversion\', \'event_label\': source, \'value\': 1}}); }};\n'
        f'</script>\n'
    )


def tag_state(content: str, marker: str) -> str:
    """Renvoie :
      - 'none'    : pas de marker GA4
      - 'partial' : marker présent mais sans `send_page_view` (config nue)
      - 'complete': marker présent avec `send_page_view` ET `click_tel` (helpers)
                    → déjà conforme, skip
    """
    if marker not in content:
        return "none"
    if "send_page_view" in content and "click_tel" in content:
        return "complete"
    return "partial"


def find_head_insertion_point(content: str):
    """Trouve l'index (juste après le token `<head...>`) où insérer notre bloc.

    Variantes reconnues : `<head>\\n`, `<head>\\r\\n`, `<head>`, `<head >\\n`, `<head >`.
    Renvoie l'index de fin du token (après `>` ou après le `\\n`) ou None si pas trouvé.
    """
    variants = [
        "<head>\n",
        "<head>\r\n",
        "<head>",
        "<head >\n",
        "<head >",
    ]
    for v in variants:
        idx = content.find(v)
        if idx != -1:
            return idx + len(v)
    return None


# Regex qui matche un éventuel bloc gtag préexistant, qu'on retire pour le remplacer
# par notre bloc standard. Couvre :
#   <!-- GA4 ... --> (commentaire éventuel)
#   <script async src="...googletagmanager.com/gtag/js?id=X"></script>
#   <script> ... </script>    (jusqu'au prochain </script>)
# On utilise une heuristique large mais bornée pour ne pas casser le HTML autour.
LEGACY_TAG_RE = re.compile(
    r'(?:<!--[^>]*?GA4[^>]*?-->\s*)?'
    r'<script\s+async\s+src=["\']https://www\.googletagmanager\.com/gtag/js\?id=[^"\']+["\']>\s*</script>\s*'
    r'<script[^>]*>(?:(?!</script>).)*?gtag\(\s*[\'"]config[\'"][^)]*\)[^<]*?</script>',
    re.IGNORECASE | re.DOTALL,
)


def patch_file(path: Path, site: str) -> tuple[bool, str]:
    """Patch un fichier HTML. Renvoie (modifié, raison)."""
    cfg = SITES[site]
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            content = path.read_text(encoding="latin-1")
        except Exception as e:
            return False, f"read-encoding: {e}"
    except Exception as e:
        return False, f"read: {e}"

    state = tag_state(content, cfg["marker"])
    if state == "complete":
        return False, "already-complete"

    insertion_idx = find_head_insertion_point(content)
    if insertion_idx is None:
        return False, "no-<head>"

    new_block = build_block(site)

    if state == "partial":
        # Tenter de retirer l'ancien bloc gtag (s'il existe encore sous une forme
        # identifiable) pour ne pas avoir 2x <head>-block concurrents.
        new_content, n_subs = LEGACY_TAG_RE.subn(new_block, content, count=1)
        if n_subs == 0:
            # Fallback: pas de match legacy regex → on retire la ligne `gtag('config', ...)` seule
            legacy_config_re = re.compile(
                r"<script>\s*window\.dataLayer[^<]*gtag\([^<]*?\)\s*;</script>",
                re.IGNORECASE | re.DOTALL,
            )
            new_content, n_subs2 = legacy_config_re.subn(new_block, content, count=1)
            if n_subs2 == 0:
                # Ultime fallback : on insère après <head>, en acceptant la duplication
                # (rare: le tag était dans une forme très atypique).
                new_content = content[:insertion_idx] + new_block + content[insertion_idx:]
                print(f"  WARN partial-no-match: {path} — duplication possible", file=sys.stderr)
    else:
        # state == "none" : insertion pure après <head>
        new_content = content[:insertion_idx] + new_block + content[insertion_idx:]

    try:
        path.write_text(new_content, encoding="utf-8")
    except Exception as e:
        return False, f"write: {e}"

    return True, f"injected ({state}→complete)"


def main():
    parser = argparse.ArgumentParser(description="Patch GA4 sur HTML statiques.")
    parser.add_argument("--site", required=True, choices=list(SITES.keys()))
    parser.add_argument("--root", required=True, type=Path,
                        help="Racine du repo (worktree)")
    parser.add_argument("--include-dirs", nargs="*", default=None,
                        help="Sous-dossiers à scanner (défaut: racine + blog + public + dist/public + villages + concelhos + distritos + tuto + faq + urgencias)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Ne pas écrire, juste compter")
    parser.add_argument("--verbose", action="store_true",
                        help="Log des fichiers partiels détectés et autres infos")
    parser.add_argument("--exclude-paths", nargs="*", default=None,
                        help="Chemins relatifs à exclure (ex: 'client/index.html')")
    args = parser.parse_args()

    root: Path = args.root.resolve()
    if not root.exists():
        print(f"❌ Racine absente : {root}", file=sys.stderr)
        sys.exit(2)

    # Exclusions par site (React shells pour CNR/ENR, vide pour CU/EU).
    default_exclude_paths = set(DEFAULT_EXCLUDES_PER_SITE.get(args.site, []))
    exclude_paths = set(default_exclude_paths)
    if args.exclude_paths:
        exclude_paths.update(args.exclude_paths)
    exclude_paths_resolved = {(root / p).resolve() for p in exclude_paths}

    EXCLUDE_DIRS = {
        ".git", ".worktrees", ".hermes-worktrees", ".tooling", ".openclaw",
        "node_modules", "dist", ".vercel", "_audit", "_archive",
        "_archive-p1-fix-2026-07-16", "_archive-p1-prototype-2026-07-16",
        "_archive-wave2-refonte-2026-07-16",
        "scripts/logs", "scripts/archive",
        "_indexing",
    }

    include_dirs = args.include_dirs or [".", "blog", "public", "dist/public",
                                         "villages", "concelhos", "distritos",
                                         "tuto", "faq", "urgencias", "admin"]

    candidates = set()
    for inc in include_dirs:
        base = root / inc if inc != "." else root
        if not base.exists():
            continue
        for path in base.rglob("*.html"):
            rel_parts = path.relative_to(root).parts
            if any(part in EXCLUDE_DIRS for part in rel_parts):
                continue
            resolved = path.resolve()
            if resolved in exclude_paths_resolved:
                continue
            candidates.add(resolved)

    scanned = 0
    excluded_paths_count = 0
    modified = 0
    modified_from_none = 0
    modified_from_partial = 0
    skipped_complete = 0
    errors = 0
    error_reasons: dict[str, int] = {}
    sample_modified = []
    sample_partial_upgraded = []
    sample_skipped = []
    sample_excluded = []

    for path in sorted(candidates):
        scanned += 1
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            errors += 1
            error_reasons[f"read:{type(e).__name__}"] = error_reasons.get(f"read:{type(e).__name__}", 0) + 1
            continue

        state = tag_state(content, SITES[args.site]["marker"])
        if state == "complete":
            skipped_complete += 1
            if len(sample_skipped) < 3:
                sample_skipped.append(str(path.relative_to(root)))
            continue

        if args.dry_run:
            modified += 1
            if state == "partial":
                modified_from_partial += 1
            else:
                modified_from_none += 1
            continue

        was_modified, reason = patch_file(path, args.site)
        if was_modified:
            modified += 1
            if state == "partial":
                modified_from_partial += 1
                if len(sample_partial_upgraded) < 3:
                    sample_partial_upgraded.append(str(path.relative_to(root)))
                if args.verbose:
                    print(f"  upgraded (partial→complete): {path.relative_to(root)}", file=sys.stderr)
            else:
                modified_from_none += 1
                if len(sample_modified) < 3:
                    sample_modified.append(str(path.relative_to(root)))
        else:
            errors += 1
            error_reasons[reason] = error_reasons.get(reason, 0) + 1
            if args.verbose:
                print(f"  ERR ({reason}): {path.relative_to(root)}", file=sys.stderr)

    print(f"=== Témoin patch GA4 — site {args.site} ===")
    print(f"Racine : {root}")
    print(f"Scanned : {scanned}")
    print(f"Modified : {modified}")
    print(f"  ├─ from none (insertion) : {modified_from_none}")
    print(f"  └─ from partial (upgrade) : {modified_from_partial}")
    print(f"Skipped (déjà complet) : {skipped_complete}")
    print(f"Errors : {errors}")
    if error_reasons:
        print(f"  Raisons d'erreur : {error_reasons}")
    print(f"Sample 3 modifiés (none→complete) : {sample_modified}")
    print(f"Sample 3 modifiés (partial→complete) : {sample_partial_upgraded}")
    print(f"Sample 3 skipped (déjà complets) : {sample_skipped}")
    print(f"Excluded paths (jamais scannés) : {len(exclude_paths)} → {sorted(exclude_paths)}")
    print()
    if not args.dry_run:
        print("✅ Patch appliqué. NE PAS push (R3 STOP validation Philippe).")


if __name__ == "__main__":
    main()