#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Générateur de liste {files:[...]} pour KO3 + KO4 sur un repo.

Réutilise les fonctions du script d'audit canonique
(self-audit-zones.py — body_for_ko3 patch déjà appliqué par Philippe)
pour garantir qu'on détecte exactement les mêmes KO3/KO4.

Sortie : stdout JSON {"files": [relpaths], "counts": {ko3, ko4, total}}.
Exit 0.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path("/Users/admin/work/Sites/eletricista-urgente").resolve()
SELF_AUDIT = REPO / "tools/p0.5-self-audit/self-audit-zones.py"
SOURCE_OF_TRUTH = Path.home() / "work/Sites/norte-os-marketing/prototypes/zonas-data.json"

# Importer dynamiquement le script d'audit comme module
import importlib.util
spec = importlib.util.spec_from_file_location("saud", str(SELF_AUDIT))
saud = importlib.util.module_from_spec(spec)
spec.loader.exec_module(saud)

# Constantes
GRILLE = {1: 15, 2: 25, 3: 35, 4: 45, 5: 55, 6: 65}

# Mêmes excludes que self-audit-zones.py
EXCLUDE_DIRS = {"dist", "node_modules", "_archive", ".git", ".hermes", "__pycache__"}


def is_excluded(path: Path) -> bool:
    parts = set(path.parts)
    if parts & EXCLUDE_DIRS:
        return True
    if path.name.endswith("-es.html"):
        return True
    return False


def detect_ko3_or_ko4(path: Path, content: str, zonas: dict) -> tuple[bool, bool]:
    """Retourne (has_ko3, has_ko4) selon la logique canonique."""
    # KO3 : body_prix avec script JSON-LD strippé (body_for_ko3)
    body_for_ko3 = re.sub(
        r'<script\b[^>]*>.*?</script>', '', content,
        flags=re.DOTALL | re.IGNORECASE,
    )
    body_prix = saud.extract_body_prix_par_zone(body_for_ko3)
    slug = path.stem
    loc = saud.slug_to_localidade(slug)
    expected_zone = saud.get_zone_from_zonas(zonas, loc)

    has_ko3 = False
    for zone_annoncee, prix_annonce in body_prix.items():
        # Aligné sur audit canonique : KO3 uniquement si zone_annoncee == expected_zone
        # (les cas zone != expected sont comptés en KO2ter par l'audit canonique).
        if zone_annoncee == expected_zone:
            if prix_annonce != GRILLE[zone_annoncee]:
                has_ko3 = True
                break

    # KO4 : délais chiffres, R145 strict sur -urgente
    has_ko4 = False
    if "urgente" in str(path):
        delais = saud.extract_delais_chiffres(content)
        if delais:
            has_ko4 = True

    return has_ko3, has_ko4


def main() -> int:
    zonas = json.loads(SOURCE_OF_TRUTH.read_text(encoding="utf-8"))

    files = []
    counts = {"ko3": 0, "ko4": 0, "total": 0}

    for path in sorted(REPO.rglob("*.html")):
        if is_excluded(path):
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        has_ko3, has_ko4 = detect_ko3_or_ko4(path, content, zonas)
        if has_ko3 or has_ko4:
            rel = str(path.relative_to(REPO))
            files.append(rel)
            counts["total"] += 1
            if has_ko3:
                counts["ko3"] += 1
            if has_ko4:
                counts["ko4"] += 1

    out = {"files": files, "counts": counts, "repo": REPO.name}
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())