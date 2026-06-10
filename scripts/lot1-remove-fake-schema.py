#!/usr/bin/env python3
"""
scripts/lot1-remove-fake-schema.py
=================================

Lot 1 Phase 8 — Purge du schema.org mensonger injecte par Norte-Reparos-Bot
entre fevrier et juin 2026 (commits #49, #58, #68 notamment).

Pourquoi ce script existe
--------------------------
Le bot a injecte dans les HTML statiques des patterns schema.org non conformes
aux Google guidelines, ce qui expose les sites a une penalite manuelle :

  - "aggregateRating" avec 4.9/127 reviews : AUCUN avis Google reel n'existe
    (cf. MEMORY.md).  Faux social proof = violation schema.org + risque
    action manuelle Google.
  - "VideoObject" sur 237 HowTo : les VideoObject referencent des videos qui
    n'existent pas (commit #49 "Add VideoObject schema to 237 HowTo pages
    (placeholders for future video content)" - les placeholders ne doivent
    PAS etre presentes tant que les videos n'existent pas).
  - "SoftwareApplication" et "VirtualLocation" : pollution schema, jamais
    legitime pour un service de plomberie/electricite local.

Strategie
---------
On supprime uniquement la SOUS-PROPRIETE incriminee dans le bloc JSON-LD
(parent preserve : LocalBusiness, Service, FAQPage, etc. restent intacts).

On utilise un compteur d'accolades pour matcher l'objet complet, ce qui
permet de gerer correctement les objets JSON imbriques.

Comportement Option C (valide par Philippe 2026-06-10) :
  - Patche les fichiers ou le JSON-LD est valide et contient les patterns.
  - Pour les fichiers ou le JSON-LD est deja casse en pre-existant
    (commit bot anterieur qui a casse la structure), le script SKIP le
    fichier, LOGUE un warning dans scripts/lot1-skipped-files.log, et
    le laisse tel quel.  Pas de regression (le fichier etait deja casse).
  - Le contenu de skipped-files.log est reporte dans le commit message
    pour traçabilite.

Usage
-----
  python3 scripts/lot1-remove-fake-schema.py [--dry-run] [--root PATH]

  --dry-run   : simule sans ecrire
  --root PATH : racine a scanner (defaut: repertoire courant)

Le script est idempotent : le repasser ne devrait rien modifier.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# Les 4 patterns a supprimer (proprietes JSON-LD mensongeres)
TARGET_PROPS = [
    "aggregateRating",   # 4.9/127 reviews fantomes
    "VideoObject",       # videos qui n'existent pas
    "SoftwareApplication",  # pollution schema
    "VirtualLocation",   # pollution schema
]

# Regex pour trouver un bloc JSON-LD complet
RE_JSONLD_BLOCK = re.compile(
    r'(<script[^>]*application/ld\+json[^>]*>)(.*?)(</script>)',
    re.DOTALL,
)

# Regex pour reperer le debut d'une sous-propriete (accolade ouvrante apres :)
RE_SUBPROP_START = re.compile(r'[,]\s*"([^"]+)"\s*:\s*\{')


def remove_subprop(json_text: str, prop_name: str) -> tuple[str, int]:
    """
    Supprime toutes les occurrences de ,"PROP":{...} dans le texte JSON,
    ou { "PROP": ..., ... } quand PROP est utilise comme cle racine d'un objet
    (typiquement pour VideoObject, SoftwareApplication, VirtualLocation qui
    sont des @type a part entiere et non des sous-proprietes).

    Gere l'imbrication des accolades via compteur.
    Renvoie (nouveau_texte, nb_suppressions).
    """
    count = 0
    result_parts = []
    i = 0

    # Pattern strict : on cherche "PROP":{ avec le PROP exact, precede de :
    #   - une virgule + espaces (sous-propriete d'un objet)
    #   - un { ouvrant + espaces (cle racine d'un objet)
    # Mais PAS precede directement d'un caractere alphanumerique ou d'un "
    # (ce qui eviterait les faux positifs sur des sous-chaines comme
    # isVideoObjectEnabled, etc.)
    pattern = re.compile(
        r'(?:[,{]\s*)"' + re.escape(prop_name) + r'"\s*:\s*\{'
    )

    while i < len(json_text):
        m = pattern.search(json_text, i)
        if not m:
            result_parts.append(json_text[i:])
            break

        # m.end() - 1 = position du { ouvrant
        brace_start = m.end() - 1
        depth = 0
        j = brace_start
        while j < len(json_text):
            ch = json_text[j]
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    break
            j += 1

        if j >= len(json_text) or depth != 0:
            # Accolades non equilibrees, on laisse le fichier (sera loggue ailleurs)
            result_parts.append(json_text[i:])
            break

        # Determiner ou commencer la suppression :
        # - Si precede d'une virgule : supprimer depuis la virgule
        # - Si precede d'un { ouvrant (cle racine) : supprimer depuis le { ouvrant
        if json_text[m.start()] == ',':
            delete_start = m.start()  # inclure la virgule
        else:
            delete_start = m.start()  # c'est le { ouvrant

        # Supprimer de delete_start jusqu'a j+1 (apres l'accolade fermante)
        result_parts.append(json_text[i:delete_start])
        count += 1
        i = j + 1

    return ''.join(result_parts), count


def remove_standalone_jsonld_block(content: str, target_type: str) -> tuple[str, int]:
    """
    Supprime un bloc <script type="application/ld+json"> ENTIER quand son
    @type racine est target_type (ex: VideoObject, SoftwareApplication).

    Cible le cas ou le bot a cree un script JSON-LD dedie a un type frauduleux
    (typiquement VideoObject pour des videos qui n'existent pas).

    Renvoie (nouveau_contenu, nb_blocs_supprimes).
    """
    count = 0
    blocks = list(RE_JSONLD_BLOCK.finditer(content))
    result = []
    last_end = 0

    for m in blocks:
        # Ajouter tout ce qui est entre le dernier match et celui-ci
        result.append(content[last_end:m.start()])
        body = m.group(2)

        # Verifier si le @type racine (premier rencontre) est target_type
        # Le pattern cherche : "type_cible" dans les premieres cles
        # On matche "type_cible" comme @type racine
        # Format typique : {"@context":"...","@type":"VideoObject",...}
        # On cherche : ,"@type":"VideoObject" ou {"@type":"VideoObject"
        root_type_match = re.search(
            r'["\']?@type["\']?\s*:\s*["\']' + re.escape(target_type) + r'["\']',
            body,
        )

        if root_type_match:
            # Supprimer ce bloc entier
            count += 1
            last_end = m.end()
        else:
            # Garder le bloc tel quel
            result.append(content[m.start():m.end()])
            last_end = m.end()

    # Ajouter le reste du contenu
    result.append(content[last_end:])
    return ''.join(result), count


def is_jsonld_valid(content: str) -> bool:
    """Verifie que tous les blocs JSON-LD du contenu sont des JSON valides."""
    blocks = RE_JSONLD_BLOCK.findall(content)
    for _open, body, _close in blocks:
        try:
            json.loads(body)
        except json.JSONDecodeError:
            return False
    return True


def patch_file(filepath: Path, dry_run: bool = False) -> dict:
    """
    Patche un fichier HTML pour supprimer les 4 patterns de schema mensonger.

    Retourne un dict avec :
      - status: 'patched' | 'skipped_invalid_json' | 'unchanged' | 'error'
      - removed: dict {prop: count} des suppressions effectuees
      - reason: explication si skipped
    """
    result = {
        'file': str(filepath),
        'status': 'unchanged',
        'removed': {},
        'reason': None,
    }

    try:
        original = filepath.read_text(encoding='utf-8')
    except Exception as e:
        result['status'] = 'error'
        result['reason'] = f'Read error: {e}'
        return result

    # Verifier que tous les JSON-LD sont valides en pre-condition
    if not is_jsonld_valid(original):
        result['status'] = 'skipped_invalid_json'
        result['reason'] = 'JSON-LD blocks already invalid (pre-existing bot bug, not caused by this script)'
        return result

    # Appliquer les suppressions en sequence :
    # 1) D'abord les sous-proprietes (aggregateRating, etc.)
    # 2) Puis les blocs JSON-LD dedies ou @type racine = cible
    new_content = original
    for prop in TARGET_PROPS:
        new_content, n = remove_subprop(new_content, prop)
        if n > 0:
            result['removed'][prop] = n

    # Pour VideoObject, SoftwareApplication, VirtualLocation : aussi
    # supprimer les scripts JSON-LD dedies (quand le @type racine est la cible)
    for target_type in ['VideoObject', 'SoftwareApplication', 'VirtualLocation']:
        new_content, n = remove_standalone_jsonld_block(new_content, target_type)
        if n > 0:
            result['removed'][f'standalone_{target_type}'] = n

    if not result['removed']:
        # Rien a supprimer (ou pas concerne)
        return result

    # Verifier que le contenu patche est toujours du JSON valide
    if not is_jsonld_valid(new_content):
        result['status'] = 'error'
        result['reason'] = 'Patch would produce invalid JSON, aborting'
        return result

    # Verifier qu'aucun des 4 patterns ne subsiste
    for prop in TARGET_PROPS:
        if prop in new_content:
            result['status'] = 'error'
            result['reason'] = f'Pattern "{prop}" still present after patch'
            return result

    if not dry_run:
        filepath.write_text(new_content, encoding='utf-8')
    result['status'] = 'patched'
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Lot 1 Phase 8 - Purge du schema.org mensonger (Bot commits #49, #58, #68)"
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Simule le patch sans rien ecrire sur disque',
    )
    parser.add_argument(
        '--root', type=Path, default=Path('.'),
        help='Racine a scanner (defaut: repertoire courant)',
    )
    args = parser.parse_args()

    root = args.root.resolve()

    # Trouver tous les fichiers HTML a scanner
    html_files = sorted(root.rglob('*.html'))
    # Exclure node_modules et .git par securite
    html_files = [
        f for f in html_files
        if 'node_modules' not in f.parts
        and '.git' not in f.parts
    ]

    print(f"[Lot 1] Scan de {len(html_files)} fichiers HTML sous {root}")
    print(f"[Lot 1] Mode: {'DRY-RUN (lecture seule)' if args.dry_run else 'ECRITURE REELLE'}")
    print()

    stats = {
        'patched': 0,
        'skipped_invalid_json': 0,
        'unchanged': 0,
        'error': 0,
        'removed_total': {p: 0 for p in TARGET_PROPS},
        'removed_total_standalone': {
            'VideoObject': 0,
            'SoftwareApplication': 0,
            'VirtualLocation': 0,
        },
        'skipped_files': [],
        'error_files': [],
    }

    for f in html_files:
        r = patch_file(f, dry_run=args.dry_run)
        if r['status'] == 'patched':
            stats['patched'] += 1
            for prop, n in r['removed'].items():
                if prop.startswith('standalone_'):
                    # Bloc JSON-LD dedie supprime
                    target = prop.replace('standalone_', '')
                    stats['removed_total_standalone'][target] += n
                else:
                    stats['removed_total'][prop] += n
        elif r['status'] == 'skipped_invalid_json':
            stats['skipped_invalid_json'] += 1
            stats['skipped_files'].append(r['file'])
        elif r['status'] == 'unchanged':
            stats['unchanged'] += 1
        else:  # error
            stats['error'] += 1
            stats['error_files'].append((r['file'], r['reason']))

    # Rapport
    print("=" * 70)
    print("RAPPORT LOT 1 — PURGE SCHEMA FRAUD")
    print("=" * 70)
    print(f"Fichiers patchés:        {stats['patched']}")
    print(f"Fichiers inchangés:      {stats['unchanged']}")
    print(f"Fichiers skippés (JSON cassé): {stats['skipped_invalid_json']}")
    print(f"Erreurs:                 {stats['error']}")
    print()
    print("Suppressions par pattern (sous-proprietes):")
    for prop, n in stats['removed_total'].items():
        print(f"  {prop:25s} : {n:6d}")
    print()
    print("Suppressions de blocs JSON-LD dedies (root @type):")
    for prop, n in stats['removed_total_standalone'].items():
        if n > 0:
            print(f"  {prop:25s} : {n:6d} scripts supprimes")
    print()

    if stats['skipped_files']:
        print(f"Fichiers skippés (à traiter en backlog) : {len(stats['skipped_files'])}")
        for f in stats['skipped_files'][:20]:
            print(f"  - {f}")
        if len(stats['skipped_files']) > 20:
            print(f"  ... et {len(stats['skipped_files']) - 20} autres")
        print()

        # Ecrire le log pour le commit message
        log_path = root / 'scripts' / 'lot1-skipped-files.log'
        log_path.parent.mkdir(exist_ok=True)
        with open(log_path, 'w', encoding='utf-8') as lf:
            lf.write(f"# Lot 1 — fichiers skippés (JSON-LD déjà cassé en pré-existant)\n")
            lf.write(f"# Généré le {datetime.now(timezone.utc).isoformat()}\n")
            lf.write(f"# Total: {len(stats['skipped_files'])} fichiers\n\n")
            for f in stats['skipped_files']:
                lf.write(f"{f}\n")
        print(f"Log écrit: {log_path}")
        print()

    if stats['error_files']:
        print(f"ERREURS : {len(stats['error_files'])}")
        for f, reason in stats['error_files'][:10]:
            print(f"  - {f}: {reason}")
        sys.exit(1)

    print("=" * 70)
    if args.dry_run:
        print("DRY-RUN terminé. Aucune modification ecrite.")
    else:
        print("PATCH terminé.")
    print("=" * 70)


if __name__ == '__main__':
    main()
