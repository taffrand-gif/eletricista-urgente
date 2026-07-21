#!/usr/bin/env python3
"""
GEO-NEUTRALISATION V2 — applique les 4 règles du CEO sur tous les .html d'un repo.

Règles (ordonnées: plus spécifique d'abord):
  R1. (Raio de )?<N> km de Macedo[s]?[ de Cavaleiros]?
        → "cobertura em toda a região de Trás-os-Montes"
  R2. sede em Macedo[ de Cavaleiros]? | base em Macedo[ de Cavaleiros]?
        → "sede na região de Trás-os-Montes"  / "base na região de Trás-os-Montes"
  R3. desde Macedo[ de Cavaleiros]?  (inclut "a vinda desde Macedo...")
        → "na região de Trás-os-Montes"
  R4. a vinda desde Macedo de Cavaleiros
        → "a vinda na região de Trás-os-Montes"  (réécriture naturelle)

NB: "em Macedo de Cavaleiros" FACTUEL localité → INTACT.
"""

import re
import sys
from pathlib import Path

# 4 patterns compilés — du plus spécifique au plus générique (imperatif)
RX_KM = re.compile(
    r'(\bRaio de\s+)?(\d+)\s*km\s+de\s+Macedo(?:\s+de\s+Cavaleiros)?\b',
    re.IGNORECASE,
)
RX_SEDE_BASE = re.compile(
    r'\b(sede|base)\s+em\s+Macedo(?:\s+de\s+Cavaleiros)?\b',
    re.IGNORECASE,
)
RX_DESDE = re.compile(
    r'\bdesde\s+Macedo(?:\s+de\s+Cavaleiros)?\b',
    re.IGNORECASE,
)
# Variante explicite "a vinda desde Macedo de Cavaleiros" (CEO demande un wording)
RX_A_VINDA = re.compile(
    r'\ba\s+vinda\s+desde\s+Macedo(?:\s+de\s+Cavaleiros)?\b',
    re.IGNORECASE,
)


def transform(text: str) -> tuple[str, int]:
    """Applique les 4 règles dans l'ordre, retourne (texte, nb_total_subs)."""
    total = 0

    # R1: distance en km depuis Macedo (avec ou sans "Raio de", ou "a N km de")
    text, n = RX_KM.subn("cobertura em toda a região de Trás-os-Montes", text)
    total += n

    # R2: sede/base em Macedo (avant desde, pour éviter collision)
    def r2_sub(m: re.Match) -> str:
        word = m.group(1).lower()
        return f"{word} na região de Trás-os-Montes"
    text, n = RX_SEDE_BASE.subn(r2_sub, text)
    total += n

    # R3-bis (phrase entière "a vinda desde Macedo"): wording naturel
    def r3b_sub(m: re.Match) -> str:
        return "a deslocação na região de Trás-os-Montes"
    text, n = RX_A_VINDA.subn(r3b_sub, text)
    total += n

    # R3: depuis Macedo (reste) → "na região de Trás-os-Montes"
    text, n = RX_DESDE.subn("na região de Trás-os-Montes", text)
    total += n

    return text, total


def main(repo_root: str) -> int:
    root = Path(repo_root).resolve()
    files_processed = 0
    files_modified = 0
    total_subs = 0

    for p in sorted(root.rglob("*.html")):
        # Skip build artifacts / Vercel output si besoin
        rel = p.relative_to(root)
        if "/node_modules/" in str(rel) or "/.git/" in str(rel):
            continue
        files_processed += 1
        try:
            original = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        new, n = transform(original)
        if n > 0:
            p.write_text(new, encoding="utf-8")
            files_modified += 1
            total_subs += n

    print(f"FILES_PROCESSED={files_processed}")
    print(f"FILES_MODIFIED={files_modified}")
    print(f"TOTAL_SUBS={total_subs}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
