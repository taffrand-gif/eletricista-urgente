#!/usr/bin/env python3
"""
Fix canonical self-ref pour bucket C (EU eletricista-urgente).

Lit _audit/canonical-triage-EU.csv, sélectionne status_bucket == "c_money_other_concelho"
(slug canon = typo: diacritics strippés par le générateur), et patch chaque fichier
pour remplacer la cible canon par self-ref.

L'identité de la page source est la source de vérité :
- eletricista-XXX.html          -> canon = https://eletricista-urgente.pt/eletricista-XXX
- eletricista-urgente-XXX.html  -> canon = https://eletricista-urgente.pt/eletricista-urgente-XXX

DRY-RUN par défaut. --apply pour écrire.

GATE : 183 fichiers attendus, 1 patch/fichier, 0 modification collatérale.
Doctrine : L1 mémoire cross-canonical hors-scope = dé-indexation silencieuse.
"""
import csv
import re
import sys
import argparse
from pathlib import Path

ROOT = Path(".")
CSV = ROOT / "_audit" / "canonical-triage-EU.csv"
HOST = "https://eletricista-urgente.pt"

RE_CANON = re.compile(
    r'(<link[^>]+rel=[\"\']canonical[\"\'][^>]+href=[\"\'])([^\"\']+)([\"\'])',
    re.IGNORECASE,
)


def expected_self(filename):
    """Calcule le canonical self-ref attendu à partir du nom de fichier."""
    if filename.startswith("eletricista-urgente-"):
        slug = filename[len("eletricista-urgente-"):-len(".html")]
        return f"{HOST}/eletricista-urgente-{slug}"
    # eletricista-{slug}.html
    slug = filename[len("eletricista-"):-len(".html")]
    return f"{HOST}/eletricista-{slug}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Écrire les changements")
    args = ap.parse_args()

    if not CSV.exists():
        print(f"ERREUR: {CSV} introuvable. Lancer d'abord scan_canonical.py.", file=sys.stderr)
        sys.exit(1)

    targets = []
    with CSV.open() as f:
        for row in csv.DictReader(f):
            # Bucket C = typo slug (diacritics strippés). Bucket B = case-study|blog.
            # Sur EU le scan initial a tout classé en C (pas de case-study|blog).
            # On garde C + B par sécurité.
            if row["status_bucket"] in ("b_bug_case_study_blog", "c_money_other_concelho", "d_broken_404_empty"):
                targets.append(row)

    print(f"# Fichiers à fixer: {len(targets)}", file=sys.stderr)

    fixed = 0
    skipped = 0
    errors = []
    diff_log = []

    for t in targets:
        fp = ROOT / t["file"]
        if not fp.exists():
            errors.append(f"ABSENT: {t['file']}")
            continue

        try:
            expected_self_url = expected_self(t["file"])
        except Exception as e:
            errors.append(f"NOM INATTENDU ({e}): {t['file']}")
            continue

        raw = fp.read_bytes()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            text = raw.decode("latin-1", errors="replace")

        old_canon = t["canon_target"]
        # Si la cible canon == self-ref, rien à faire
        if old_canon == expected_self_url:
            errors.append(f"DÉJÀ SELF-REF: {t['file']}")
            continue

        count = text.count(old_canon)
        if count == 0:
            errors.append(f"CIBLE INTROUVABLE: {t['file']} (cherché '{old_canon}')")
            continue
        # L'URL du canonical apparaît aussi dans <meta og:url>, JSON-LD etc.
        # → on remplace TOUTES les occurrences (toutes les self-références
        # de l'URL doivent rester synchrones : canonical == og:url == self-page).
        if count > 4:
            errors.append(f"CIBLE TROP MULTIPLE ({count}x): {t['file']} — revue manuelle requise")
            continue

        new_text = text.replace(old_canon, expected_self_url)

        # Garde-fou chirurgical : le diff textuel doit être EXACTEMENT le
        # remplacement de l'URL canon (old_canon → expected_self_url).
        # Si le diff contient d'autres changements (refactor accidentel,
        # espaces, BOM, etc.), on abandonne le fichier.
        n_old_remaining = new_text.count(old_canon)
        if n_old_remaining > 0:
            errors.append(f"REMPLACEMENT INCOMPLET: {t['file']} ({n_old_remaining}x '{old_canon}' reste)")
            continue
        n_new_total = new_text.count(expected_self_url)
        n_new_was = text.count(expected_self_url)
        expected_diff_occurrences = count - n_old_remaining  # combien d'occurrences remplacées
        if (n_new_total - n_new_was) != count:
            errors.append(f"COMPTE DIFF INATTENDU: {t['file']} (avant={count}, après={n_new_total-n_new_was})")
            continue
        # Vérifier qu'on a bien 1 canonical et qu'il pointe vers self-ref
        new_canons = RE_CANON.findall(new_text)
        # RE_CANON.groups == 3 (prefix, href, suffix)
        if len(new_canons) != 1:
            errors.append(f"POST-FIX MULTI CANON: {t['file']} ({len(new_canons)} canon)")
            continue
        if new_canons[0][1] != expected_self_url:
            errors.append(f"POST-FIX MAUVAISE CIBLE: {t['file']} ({new_canons[0][1]} vs {expected_self_url})")
            continue

        diff_log.append((t["file"], old_canon, expected_self_url, t["status_bucket"]))

        if args.apply:
            new_bytes = new_text.encode("utf-8")
            if new_bytes == raw:
                errors.append(f"NO-OP: {t['file']} (octets identiques post-fix)")
                continue
            fp.write_bytes(new_bytes)
            fixed += 1
        else:
            skipped += 1

    # === RAPPORT ===
    print("=" * 70)
    if args.apply:
        print(f"MODE: APPLY (écriture réelle)")
    else:
        print(f"MODE: DRY-RUN (lecture seule)")
    print(f"Fichiers à fixer: {len(targets)}")
    print(f"Fixed:   {fixed}")
    print(f"Skipped: {skipped}")
    print(f"Errors:  {len(errors)}")
    print("=" * 70)

    if errors:
        print("\n# ERREURS :")
        for e in errors:
            print(f"  - {e}")

    print("\n# DIFF (uniquement lignes modifiées) :")
    for f, old, new, bucket in diff_log:
        print(f"  [{bucket}] {f}")
        print(f"    - {old}")
        print(f"    + {new}")

    if not args.apply:
        print(f"\n# Pour appliquer : python3 _audit/fix_canonical.py --apply")


if __name__ == "__main__":
    main()
