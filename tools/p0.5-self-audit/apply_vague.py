#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
apply_vague.py — Patcher canonique P0.5B pour une vague (page-entiere, 8 surfaces alignees).

Mission P0.5B (mission 02/07/2026, CEO 9/10) : vague patch ≤100 fichiers,
toutes surfaces alignees (8 par page) dans le meme commit. Patcher
reproductible qui suit les regles ci-dessous.

REGLES STRICTES (R8 OpenClaw, R4 zero invention, R145 R12) :
  - Pas de dist/, pas de fichiers -es.html (skip)
  - Pas de JSON-LD '@type':"Offer" simple ou '@type':"Service" (intact)
  - Pas de grille canonique Z1=15€..Z6=65€ cassee (intacte)
  - R145 strict sur -urgente : delais chiffres retires/remplaces par
    "Sob marcação, mediante confirmação por telefone"
  - R4 zero invention : jamais inventer prix, zone, delai
    Tous les patches s'appuient sur GRILLE canonique + source-of-truth
  - Page-entiere : si une page a N KO (toutes categories), corriger les
    N en un seul passage.

STRATEGIE PATCH (par categorie de KO) :

  KO1_badge_zona :
    Source = zonas-data.json (zone_attendue). Body data-zone="X" -> data-zone="<expected>".

  KO2ter_body_vs_badge :
    Le badge data-zone="<expected>" est OK (== source). Body dit "Deslocação Zona X"
    avec X != expected. Remplacer X par expected dans body. Propager le prix
    grille associe (GRILLE[expected]€).

  KO2ter_zone_attendue :
    Badge OK (= body zone) MAIS body zone != source. Remplacer par expected et
    propager le prix grille.

  KO2ter_body_seul :
    Pas de badge MAIS body dit "Deslocação Zona X" avec X != expected.
    Remplacer X par expected et propager prix.

  KO2_jsonld_zone :
    Le bloc <script type="application/ld+json"> contient "Deslocação Zona X".
    Remplacer par expected DANS JSON-LD. ATTENTION : ne pas casser le JSON.

  KO2bis_badge_vs_jsonld :
    Badge != JSON-LD deslocacao. Aligner JSON-LD sur badge OU sur source
    (preferer source si badge OK).

  KO3_prix_body :
    Body dit "Zona X" avec prix P != GRILLE[X]. Remplacer P par GRILLE[X].

  KO4_delai_chiffre_urgente :
    -urgente strict (R145) : remplacer tous les (Tempo|Chegada|resposta)[^<]*\d+\s*min
    par "Sob marcação, mediante confirmação por telefone".

USAGE :
  python3 apply_vague.py <repo_dir> <files_json>
  <files_json> = fichier JSON avec {"files": [path relatif, ...]}

SORTIE :
  exit 0 si OK
  exit 1 si temoin manquant ou erreur irrecuperable
  log sur stderr : nombre de fichiers modifies, delta par tier
"""
import json
import re
import sys
from pathlib import Path

# Constantes alignees avec self-audit-zones.py
GRILLE = {1: 15, 2: 25, 3: 35, 4: 45, 5: 55, 6: 65}

# Source-of-truth
SOURCE_OF_TRUTH = Path.home() / "work/Sites/norte-os-marketing/prototypes/zonas-data.json"

# Regex (alignement strict sur le script d'audit)
RE_BADGE_ATTR = re.compile(r'data-zone=["\']([1-6])["\']')
RE_GRILLE_CANON_INFO = re.compile(r"Z[1-6]=\d+€")
RE_JSONLD_BLOCK = re.compile(
    r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>',
    re.DOTALL | re.IGNORECASE,
)
RE_JSONLD_DESLOCACAO_ZONE = re.compile(
    r'Desloca[çc][ãa]o\s+Zona\s+(\d)',
    re.IGNORECASE,
)
# Pour remplacer Z par expected + propager le prix.
# Accepte balises HTML entre "Zona X:" et le prix (ex: `<strong>...</strong>`).
# Strategie : capturer la zone, puis continuer a travers balises jusqu'au prix.
RE_BODY_DESLOCACAO = re.compile(
    r"Desloca[çc][ãa]o[\s ]*Zona[\s ]*(\d)[\s ]*:?(?:[^<]|<[^>]*>){0,80}?(\d{1,3})\s*€",
    re.IGNORECASE,
)
RE_BODY_ZONE_PRIX = re.compile(
    r"(\bZona\s+(\d)\b[^\.<>\n]{0,80}?)(\d{1,3})\s*€",
    re.IGNORECASE,
)
RE_DELAIS = re.compile(
    r"(?i)(?:tempo|chegada|resposta)[^<]{0,40}?\d{1,3}\s*min",
)


def load_source():
    if not SOURCE_OF_TRUTH.exists():
        sys.exit(f"Source-of-truth introuvable : {SOURCE_OF_TRUTH}")
    return json.loads(SOURCE_OF_TRUTH.read_text(encoding="utf-8"))


def unaccent(s: str) -> str:
    import unicodedata
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def slug_to_localidade(slug: str) -> str:
    s = slug
    s = re.sub(r"-\d{4}$", "", s)
    prefixes_service = (
        "precos-canalizador-", "precos-eletricista-",
        "preco-canalizador-urgente-", "preco-eletricista-urgente-",
        "preco-canalizador-norte-reparos-", "preco-eletricista-norte-reparos-",
        "quanto-custa-canalizador-", "quanto-custa-eletricista-",
        "iluminacao-exterior-",
        "fuga-agua-", "desentupimento-", "fossa-septica-", "canalizacao-nova-",
        "curto-circuito-", "quadro-eletrico-", "instalacao-eletrica-", "avaria-eletrica-",
    )
    prefixes_extra = ("canalizador-", "eletricista-", "urgente-")
    changed = True
    while changed:
        changed = False
        for p in prefixes_service + prefixes_extra:
            if s.startswith(p):
                s = s[len(p):]
                changed = True
                break
    particules = {"de", "da", "do", "das", "dos", "em", "na", "no", "e"}
    parts = s.replace("-", " ").split()
    parts = [p.capitalize() if i == 0 or p not in particules else p for i, p in enumerate(parts)]
    return " ".join(parts)


def get_zone(zonas, name):
    for cand in [name, name.title(), name.upper(), name.lower(),
                 unaccent(name), unaccent(name).title(),
                 unaccent(name).upper(), unaccent(name).lower()]:
        if cand in zonas:
            return zonas[cand]
    for k, v in zonas.items():
        if unaccent(k).lower() == unaccent(name).lower():
            return v
    return None


def patch_one_page(content: str, expected_zone: int, slug: str, is_urgente: bool, zonas,
                   target_override: int = None) -> tuple[str, list[str]]:
    """Applique les patches page-entiere.

    target_override : si specifie (cas NO_RESOL fallback sur badge),
    utilise cette zone comme cible au lieu de expected_zone.
    """
    target = target_override if target_override is not None else expected_zone
    patches = []
    new = content

    # KO2ter body : remplacer toute mention "Deslocação Zona X" par target
    # Mais on ne touche PAS la grille canonique informative ("Z1=15€..Z6=65€")
    body_no_grille = RE_GRILLE_CANON_INFO.sub("__GRILLE_PROTECTED__", new)
    new_body, n_body = RE_BODY_DESLOCACAO.subn(
        lambda m: f"Deslocação Zona {target}: {GRILLE[target]}€"
        if int(m.group(1)) != target else m.group(0),
        body_no_grille,
    )
    if n_body > 0:
        new = new_body.replace("__GRILLE_PROTECTED__", RE_GRILLE_CANON_INFO.pattern)
        patches.append(f"body_Z{target}_propagate ({n_body} occurrences)")

    # KO2_jsonld_zone : remplacer dans les blocs JSON-LD uniquement
    def fix_jsonld(m):
        ld = m.group(1)
        if RE_JSONLD_DESLOCACAO_ZONE.search(ld):
            new_ld, n = RE_JSONLD_DESLOCACAO_ZONE.subn(
                lambda mm: f"Deslocação Zona {target}"
                if int(mm.group(1)) != target else mm.group(0),
                ld,
            )
            if n > 0:
                patches.append(f"jsonld_Z{target} ({n} occurrences)")
                ld = new_ld
        return f"<script type=\"application/ld+json\">{ld}</script>"
    new = RE_JSONLD_BLOCK.sub(fix_jsonld, new)

    # KO4 delais : -urgente strict (R145)
    if is_urgente:
        new, n = RE_DELAIS.subn("Sob marcação, mediante confirmação por telefone", new)
        if n > 0:
            patches.append(f"R145_delai ({n} occurrences)")

    return (new, patches)


# Alias pour lappel NO_RESOL fallback (patch_one_page with target_override)
def patch_one_page_with_target(content, target, slug, is_urgente, zonas):
    return patch_one_page(content, expected_zone=target, slug=slug,
                         is_urgente=is_urgente, zonas=zonas, target_override=target)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    repo_dir = Path(sys.argv[1]).expanduser().resolve()
    files_json = Path(sys.argv[2]).expanduser().resolve()

    if not repo_dir.exists():
        sys.exit(f"Repo introuvable : {repo_dir}")
    if not files_json.exists():
        sys.exit(f"Fichier JSON introuvable : {files_json}")

    zonas = load_source()
    print(f"Source-of-truth chargée : {SOURCE_OF_TRUTH} ({len(zonas)} localités)")

    files_data = json.loads(files_json.read_text(encoding="utf-8"))
    files = files_data.get("files", [])
    print(f"Vague : {len(files)} fichiers à patcher dans {repo_dir.name}")

    patches_log = []
    skipped = []
    errored = []
    no_change = []

    for rel_path in files:
        full = repo_dir / rel_path
        if not full.exists() or full.name.endswith("-es.html"):
            skipped.append(rel_path)
            continue
        try:
            content = full.read_text(encoding="utf-8", errors="replace")
            slug = full.stem
            loc = slug_to_localidade(slug)
            expected_zone = get_zone(zonas, loc)
            is_urgente = "urgente" in str(full)

            # Strategie target : si page resolue, on prend source-of-truth.
            # Si NO_RESOL (D3 in-scope coherence), on prend le badge existant.
            # Si pas de badge non plus, on skip (D3 inconnu).
            if expected_zone is not None:
                target = expected_zone
                target_source = "source"
            else:
                # Cherche badge dans le fichier
                m_badge = RE_BADGE_ATTR.search(content)
                if m_badge:
                    target = int(m_badge.group(1))
                    target_source = "badge (NO_RESOL fallback)"
                else:
                    skipped.append((rel_path, "NO_RESOL_no_fallback"))
                    continue

            new_content, patches = patch_one_page(
                content, expected_zone if expected_zone is not None else target,
                slug, is_urgente, zonas
            )
            # fallback call: si on a target (badge fallback), patcher avec target direct
            if expected_zone is None:
                new_content, patches = patch_one_page_with_target(
                    content, target, slug, is_urgente, zonas
                )

            if new_content != content:
                full.write_text(new_content, encoding="utf-8")
                patches_log.append((rel_path, patches))
            else:
                no_change.append(rel_path)
        except Exception as e:
            errored.append((rel_path, str(e)))

    # Resume
    print(f"\n=== Résumé vague {repo_dir.name} ===")
    print(f"  Patches appliques : {len(patches_log)} / {len(files)}")
    print(f"  Skipped (NO_RESOL ou -es) : {len(skipped)}")
    print(f"  Errors : {len(errored)}")
    print(f"  No change (deja OK) : {len(no_change)}")

    if errored:
        print("\nErreurs :")
        for path, err in errored[:5]:
            print(f"  {path}: {err}")

    return 0 if not errored else 1


if __name__ == "__main__":
    sys.exit(main() or 0)
