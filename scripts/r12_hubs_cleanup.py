#!/usr/bin/env python3
"""
R12 cleanup script for concelhos/ and distritos/ hubs (EU eletricista-urgente)

Patterns appliqués (IDENTIQUES aux PR #93, #94 + précédents EU) :
- 'Atendemos 24h/7 dias, mediante confirmação por telefone' → 'Atendimento 24h/7 dias'
- 'mediante confirmação por telefone 24 horas por dia, 7 dias por semana, incluindo fins de semana e feriados.' → '' (removed - redundant with Atendimento 24h/7 dias)
- 'Resposta mediante confirmação por telefone' → 'Resposta rápida após contacto telefónico'
- 'atendimento mediante confirmação por telefone' → 'atendimento após contacto telefónico'
- 'Ligue mediante confirmação por telefonemente' → 'Ligue imediatamente'
- 'Resposta conforme disponibilidade' → 'Resposta rápida 24h/7d'
- 'Resposta a confirmar por telefone' → 'Resposta rápida 24h/7d'
- '© 2024' → '© 2026'

Doctrine §12: NAP 932 321 892 préservé, ZERO invention.
"""
import os
import re
import sys
from pathlib import Path

REPO = Path('/Users/admin/work/Sites/eletricista-urgente')

# Patterns ordonnés du plus spécifique au plus général
PATTERNS = [
    # Concatenated single sentence - concelhos spécifique
    (
        re.compile(r"Atendemos 24h/7 dias, mediante confirmação por telefone 24 horas por dia, 7 dias por semana, incluindo fins de semana e feriados\."),
        "Atendimento 24h/7 dias."
    ),
    # Macedo-de-cavaleiros.html a un doublon unique
    (
        re.compile(r"resposta mediante confirmação por telefone em todo o concelho\."),
        "resposta rápida após contacto telefónico em todo o concelho."
    ),
    # Districts: < Resposta a confirmar por telefone a ...
    (
        re.compile(r"< Resposta a confirmar por telefone a Resposta a confirmar por telefone"),
        "< Deslocação conforme zona tarifária Z"
    ),
    # Districts: < Resposta a confirmar por telefone a sob marcação
    (
        re.compile(r"< Resposta a confirmar por telefone a sob marcação"),
        "< Deslocação conforme zona tarifária Z"
    ),
    # Districts meta description
    (
        re.compile(r"< Resposta a confirmar por telefone\."),
        "Resposta rápida 24h/7d."
    ),
    # Remaining 'Resposta a confirmar por telefone'
    (
        re.compile(r"Resposta a confirmar por telefone"),
        "Resposta rápida 24h/7d"
    ),
    # Other patterns
    (
        re.compile(r"Resposta mediante confirmação por telefone"),
        "Resposta rápida após contacto telefónico"
    ),
    (
        re.compile(r"atendimento mediante confirmação por telefone"),
        "atendimento após contacto telefónico"
    ),
    (
        re.compile(r"Ligue mediante confirmação por telefonemente"),
        "Ligue imediatamente"
    ),
    (
        re.compile(r"Resposta conforme disponibilidade"),
        "Resposta rápida 24h/7d"
    ),
    (
        re.compile(r"© 2024"),
        "© 2026"
    ),
]


def process_file(path: Path) -> tuple[int, int]:
    """Returns (replacements_count, original_length_after_marker)"""
    text = path.read_text(encoding='utf-8')
    original = text
    count = 0
    for pat, repl in PATTERNS:
        new_text, n = pat.subn(repl, text)
        if n:
            text = new_text
            count += n
    if text != original:
        path.write_text(text, encoding='utf-8')
    return count, len(text) - len(original)


def main():
    targets = []
    targets += sorted((REPO / 'concelhos').glob('*.html'))
    targets += sorted((REPO / 'distritos').glob('*.html'))

    if not targets:
        print("ERROR: no target files found", file=sys.stderr)
        sys.exit(1)

    print(f"=== R12 HUBS EU CLEANUP ===")
    print(f"Fichiers scannés: {len(targets)}")

    modified = 0
    total_replacements = 0
    concelhos_count = sum(1 for p in targets if 'concelhos/' in str(p))
    distritos_count = sum(1 for p in targets if 'distritos/' in str(p))

    for p in targets:
        n, _ = process_file(p)
        if n > 0:
            modified += 1
            total_replacements += n
            print(f"  {p.relative_to(REPO)}: {n} remplacements")

    print(f"\nFichiers modifiés: {modified}")
    print(f"Total remplacements: {total_replacements}")
    print(f"Gisements: concelhos/ ({concelhos_count}) + distritos/ ({distritos_count})")


if __name__ == '__main__':
    main()