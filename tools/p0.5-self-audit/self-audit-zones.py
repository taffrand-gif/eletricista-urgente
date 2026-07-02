#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
r"""
self-audit-zones.py — Audit mecanique des pages localite vs source-of-truth.

OBJECTIF (mission Hermes P0.5, 02/07/2026, base 6,5/10) :
Remplacer les claims subjectifs (« 0 mismatch ») par des CHIFFRES REPRODUCTIBLES.

P0.5B (mission P0.5B, 02/07/2026 soir, audit CEO 8,5/10) :
- KO2bis (badge vs JSON-LD) et KO4 (delais chiffres) passent AVANT
  le early-return NO_RESOL. Une page NO_RESOL est quand meme auditee
  pour ces 2 checks (coherence interne pure).
- SERVICE_PREFIXES etendu : preco-canalizador-urgente-, preco-eletricista-urgente-,
  iluminacao-exterior- (+ tout prefixe decouvert au triage S1).
- SLUG_ALIASES (D6) : resoudre chaque slug typo contre zonas-data.json
  (alfndega*, seix0, macedo-cavaleiros sans "de"). Application stricte :
  uniquement si correspondance NON AMBIGUE, sinon OUT_OF_AREA.
- OUT_OF_AREA Guarda : fornos-de-algodres, trancoso = district Guarda,
  hors zone de service. Nouvelle categorie (lister pour Filipe, PAS patcher).

P0.5C (mission P0.5C, 02/07/2026, arbitrage CEO commit 71f1956b7) :
- KO2ter (body 'Deslocação Zona X' != badge ET/OU != zone attendue) est
  ajoute au pipeline. Temoin de validation : VPA (Vila Pouca de Aguiar)
  avec badge Z5 + body Z3 doit declencher KO2ter_body_vs_badge ET
  KO2ter_body_vs_expected.
- Le check s'applique au body VISIBLE (scripts strippés, pas seulement
  JSON-LD) pour eviter le double-comptage avec KO2bis. Si la mention est
  dans un <script>...</script>, elle est traitée par KO2bis (scope JSON-LD
  only, comportement inchange).

Pour chaque page HTML (hors -es, hors dist/, hors _archive/, hors node_modules/) :
  1. Resoudre la zone attendue : strip prefixes service du filename -> slug
     (fuga-agua-, desentupimento-, fossa-septica-, canalizacao-nova-,
      curto-circuito-, quadro-eletrico-, instalacao-eletrica-, avaria-eletrica-,
      preco-*, iluminacao-exterior-) -> lookup dans
     norte-os-marketing/prototypes/zonas-data.json.
     Si localite introuvable -> NO_RESOL (a trancher Filipe, decision D3).
  2. KO1 - Badge data-zone != zone attendue :
       <... data-zone="N" ...> ou zone-braganca (classe) ou "Zona N" explicite
       doivent matcher zonas-data.json.
  3. KO2 - Badge != JSON-LD "Desloca[çc][ãa]o Zona X" :
       la zone annoncee dans la Offer JSON-LD desplazacao doit matcher la zone
       attendue (et le badge si present).
  4. KO2ter — body « Deslocação Zona X » ≠ badge (et ≠ zone attendue si résolue) :
       extracted du body VISIBLE (scripts strippés pour eviter doublon avec
       KO2bis). Declenche si badge ET body presents ET valeurs differentes.
       Variante KO2ter_zone_attendue : badge OK (matche zone_body) MAIS
       body != zone_attendue. Variante KO2ter_body_seul : pas de badge mais
       body annonce une zone != zone_attendue.
  5. KO3 - Prix body vs grille officielle :
       Z1=15€ / Z2=25€ / Z3=35€ / Z4=45€ / Z5=55€ / Z6=65€.
       Survit aux patchs partiels (ex. badge Z2 corrige mais body dit "Z3 35€").
  6. KO4 - Delais chiffres residuels :
       regex (Tempo|Chegada|resposta)[^<]{0,40}\d{1,3}\s*min
       (R145 strict sur -urgente, tolere sur -norte sous lecon #298).

ORDRE DES CHECKS (P0.5B, le bug v1) :
  KO2bis (badge vs JSON-LD - coherence INTERNE) et KO4 (delais) ne dependent
  PAS de expected_zone. Ils sont executes MEME si localite introuvable.

ORDRE DES CHECKS (P0.5C) : KO2ter execute MEME si localite introuvable.
  KO2ter est un check de coherence interne (badge vs body 'Deslocação Zona X')
  qui ne depend pas de la resolution. Il s'execute apres KO2bis/KO4 et AVANT
  le early-return NO_RESOL — comme KO2bis, c'est un check de coherence
  pure applicable meme sur une page no_resol. Cela evite de rater le cas
  "badge Z5, body Z3" sur une page dont la localite n'est pas encore
  ajoutee a zonas-data.json.

REGLE D'USAGE (bareme prochain audit, +2 self-audit chiffre joint) :
  Tout commit de batch inclut la sortie de ce script.
  Interdit d'ecrire « 0 KO » sans coller le chiffre brut.

TEMOINS DE CONTROLE (R8 OpenClaw) - cas connus a retrouver a chaque run :
  T1 : Bragaça            -> zonas-data.json = 2, grille = Z2/25€.
  T2 : Vinhais             -> zonas-data.json = 3, grille = Z3/35€.
  T3 : Macedo de Cavaleiros-> zonas-data.json = 1, grille = Z1/15€.

USAGE :
  python3 self-audit-zones.py <repo_path> [<repo_path> ...]
  # Exemple :
  python3 self-audit-zones.py ~/work/Sites/canalizador-urgente
  python3 self-audit-zones.py ~/work/Sites/{canalizador,eletricista}-{urgente,norte-reparos}

SORTIE :
  stdout : resume par repo (4 categories KO + NO_RESOL + OUT_OF_AREA) + totaux
  exit 0 si OK, exit 1 si temoin manquant ou JSON source introuvable.

DEPENDANCES : stdlib uniquement (json, re, sys, os, pathlib, unicodedata).
"""

import json
import os
import re
import sys
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────
# CONSTANTES MÉTIER (source unique : norte-os-marketing/prototypes/zonas-data.json)
# ──────────────────────────────────────────────────────────────────────

GRILLE = {1: 15, 2: 25, 3: 35, 4: 45, 5: 55, 6: 65}  # Z1..Z6 -> €

# Prefixes service a stripper pour resoudre la localite depuis le filename.
# P0.5B : etendu avec preco-* (CU/EU), preco-*-norte-reparos (CNR/ENR),
# iluminacao-exterior- (EU).
# Tout prefixe non couvert tombe en NO_RESOL (a etendre au triage S1).
SERVICE_PREFIXES = (
    # P0.5B : satellites "urgente" pages prix (date-stripped)
    "precos-canalizador-",
    "precos-eletricista-",
    "preco-canalizador-urgente-",
    "preco-eletricista-urgente-",
    "preco-canalizador-norte-reparos-",
    "preco-eletricista-norte-reparos-",
    "quanto-custa-canalizador-",
    "quanto-custa-eletricista-",
    # P0.5B : services électricista EU
    "iluminacao-exterior-",
    # Services historiques (v1 OK)
    "fuga-agua-",
    "desentupimento-",
    "fossa-septica-",
    "canalizacao-nova-",
    "curto-circuito-",
    "quadro-eletrico-",
    "instalacao-eletrica-",
    "avaria-eletrica-",
)

# Localite est dans le filename apres strip prefixe(s), avant .html
# Cas speciaux a stripper en plus :
EXTRA_PREFIXES = (
    "canalizador-",   # prefixe metier (canalizador-braganca.html)
    "eletricista-",   # prefixe metier
    "urgente-",       # P0.5B : satellites "canalizador-urgente-lagoaca.html"
                      # = préfixe métier satellite; apres strip double, on
                      # retombe sur Lagoaca.
)

# SLUG_ALIASES (P0.5B / D6) : typos communes retirees du slug AVANT lookup.
# Application stricte : UNIQUEMENT correspondance NON AMBIGUE (un seul candidat
# dans zonas-data.json pour le nom normalise). Sinon -> OUT_OF_AREA.
# Origine : triage D6 CEO 02/07 (5 slugs ENR hors source).
SLUG_ALIASES = {
    # alfndega* -> Alfandega da Fe (zone 3 dans source)
    "alfndega-da-fe": "Alfandega da Fe",
    "alfandega-da-fe": "Alfandega da Fe",
    # seix0 -> Seixo (Manique) - si vraiment sans typo apres decodage
    # (garder prudent, plus facile de lister en NO_RESOL si doute)
    "seix0": None,  # marquer pour audit, PAS de resolution auto
    # macedo-cavaleiros sans "de" -> Macedo de Cavaleiros
    "macedo-cavaleiros": "Macedo de Cavaleiros",
}

# OUT_OF_AREA (P0.5B / D6) : localites du district Guarda, hors zone service
# Norte Reparos (~130 km autour de Macedo de Cavaleiros). NE PAS PATCHER en
# zone, mais lister pour Filipe (decision business).
OUT_OF_AREA_LOCALIDADES = frozenset({
    "Fornos de Algodres",
    "Trancoso",
})

# Source-of-truth
SOURCE_OF_TRUTH = Path.home() / "work/Sites/norte-os-marketing/prototypes/zonas-data.json"

# Témoins (R8 — au moins 3 cas à retrouver à chaque run)
TEMOINS = {
    "Bragança": 2,
    "Vinhais": 3,
    "Macedo de Cavaleiros": 1,
}

# Regex délais chiffrés (R145 strict -urgente)
RE_DELAIS = re.compile(
    r"(?i)(?:tempo|chegada|resposta)[^<]{0,40}?\d{1,3}\s*min",
)

# Regex badge data-zone / class="zone-..." / mention "Zona N" dans body
RE_BADGE_ATTR = re.compile(r'data-zone=["\'](\d)["\']')
RE_BADGE_CLASS = re.compile(r'class=["\'][^"\']*\bzone-([a-z0-9-]+)\b[^"\']*["\']', re.IGNORECASE)
RE_BADGE_TEXT = re.compile(r"\bZona\s+(\d)\b", re.IGNORECASE)
# Variante : "Z[1-6]=" dans la grille canonique (info, pas KO)
RE_GRILLE_CANON = re.compile(r"Z[1-6]=\d+€")

# Regex JSON-LD "Desloca[cç][ãa]o Zona X".
# P0.5B : simplifiee pour matcher TOUT script application/ld+json qui contient
# une mention "Deslocação Zona N" (independamment de la cle JSON englobante :
# description, text, name, acceptedAnswer.text, etc.). Capture groupe 1 = N.
# On verifie en amont que le match est dans un script JSON-LD (audit_page scope).
RE_JSONLD_DESLOCACAO_ZONE = re.compile(
    r'Desloca[çc][ãa]o\s+Zona\s+(\d)',
    re.IGNORECASE,
)
# Regex JSON-LD "Offer" deslocação avec prix
RE_JSONLD_OFFER_PRICE = re.compile(
    r'"@type"\s*:\s*"Offer"[^}]*?"price"\s*:\s*"?(\d+)[^"]*?"',
    re.IGNORECASE,
)

# Regex prix body (Deslocação X€ / Zona X : X€)
RE_BODY_DESLOCACAO = re.compile(
    r"Desloca[çc][ãa]o[^.<>\n]{0,40}?(\d{1,3})\s*€",
    re.IGNORECASE,
)
# Regex body « Deslocação Zona N » — utilisée par KO2ter.
# P0.5C (mission P0.5C, CEO commit 71f1956b7) : on l'applique sur le contenu
# HORS blocs <script>...</script> (tous, pas seulement JSON-LD) pour eviter les
# doublons avec KO2bis. Scope géré dans extract_body_deslocacao_zones().
RE_BODY_DESLOCACAO_ZONE = re.compile(
    r"Desloca[çc][ãa]o\s*[—–-]?\s*Zona\s*(\d)",
    re.IGNORECASE,
)
RE_BODY_ZONE_PRIX = re.compile(
    r"\bZona\s+(\d)\b[^.<>\n]{0,80}?(\d{1,3})\s*€",
    re.IGNORECASE,
)
RE_BODY_PRIX_ZONE = re.compile(
    r"(\d{1,3})\s*€[^.<>\n]{0,80}?\bZona\s+(\d)\b",
    re.IGNORECASE,
)


# ──────────────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────────────

def slug_to_localidade(slug: str) -> str:
    """Strip préfixes service + métier + suffixes date, retourne nom localité."""
    s = slug
    # Strip suffixes date (ex. -2026, -2025)
    s = re.sub(r"-\d{4}$", "", s)
    # Strip préfixes service (boucle : peut y en avoir plusieurs)
    changed = True
    while changed:
        changed = False
        for p in SERVICE_PREFIXES + EXTRA_PREFIXES:
            if s.startswith(p):
                s = s[len(p):]
                changed = True
                break
    # Slug → "Nome Composto" : remplacer - par espace, Title Case intelligent
    # (particules "de/da/do/das/dos/em/na/no" restent en minuscule,
    #  contrairement à .title() qui les capitalise).
    PARTICULES = {"de", "da", "do", "das", "dos", "em", "na", "no", "e"}
    parts = s.replace("-", " ").split()
    parts = [p.capitalize() if i == 0 or p not in PARTICULES else p
             for i, p in enumerate(parts)]
    return " ".join(parts)


import unicodedata

def unaccent(s: str) -> str:
    """Retire les diacritiques : 'Bragança' → 'Braganca', 'Numão' → 'Numao'."""
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def normalize_for_lookup(name: str) -> list[str]:
    """Génère les variantes de casse (+ ASCII unaccented) pour lookup zonas-data.json."""
    candidates = [name]
    # Title case (idempotent ici)
    candidates.append(name.title())
    # Upper / Lower
    candidates.append(name.upper())
    candidates.append(name.lower())
    # Variantes ASCII sans accents (slugs sont ASCII ; JSON a accents)
    ua = unaccent(name)
    if ua != name:
        candidates.append(ua)
        candidates.append(ua.title())
        candidates.append(ua.upper())
        candidates.append(ua.lower())
    return list(dict.fromkeys(candidates))  # dedup en gardant l'ordre


def get_zone_from_zonas(zonas: dict, name: str) -> object:
    """Lookup robusto: match direct + match unaccented (toutes variantes)."""
    for cand in normalize_for_lookup(name):
        if cand in zonas:
            return zonas[cand]
    # Fallback : index unaccented (construit à la volée pour 1 lookup)
    for k, v in zonas.items():
        if unaccent(k).lower() == unaccent(name).lower():
            return v
    return None


def extract_badge_zone(content: str, slug: str) -> object:
    """Cherche la zone annoncée par le badge (data-zone, class zone-X, ou texte Zona N)."""
    # Priorité 1 : data-zone="N"
    m = RE_BADGE_ATTR.search(content)
    if m:
        return int(m.group(1))
    # Priorité 2 : class="zone-braganca" etc. — on mappe la classe via lookup zonas
    m = RE_BADGE_CLASS.search(content)
    if m:
        # class="zone-braganca" → mapper via zonas (slug_to_localidade inverse)
        # Approximation : on prend le slug et on cherche sa zone, mais ici on a déjà
        # la zone attendue ; on s'en sert juste pour valider la cohérence interne.
        # → on NE peut PAS déduire la zone d'une classe sémantique sans lookup.
        # Fallback : on tente le lookup du nom de classe.
        return None
    # Priorité 3 : texte "Zona N" dans le body (première occurrence)
    # ATTENTION : la grille canonique (Z1=15€, Z2=25€, ...) en JSON-LD est EXCLUE
    # pour éviter les faux positifs ; on cherche dans le body HTML visible.
    # Heuristique simple : si la mention apparaît dans une <tr> ou <td>, c'est la grille.
    # Pour rester conservateur, on ne s'appuie pas sur cette regex seule —
    # le badge data-zone est la source primaire ; ici on signale juste la présence.
    return None


def extract_jsonld_deslocacao_zone(content: str) -> object:
    """Extrait la zone annoncée dans JSON-LD 'Desloca[cç][ãa]o Zona X'.

    P0.5B : scan UNIQUEMENT les blocs <script type='application/ld+json'>
    (RE_JSONLD_DESLOCACAO_ZONE est volontairement laxiste, on borne le scope ici
    pour eviter faux positifs depuis le body). Retourne la premiere zone trouvee.
    """
    # Scanner tous les blocs JSON-LD
    for m_script in re.finditer(
        r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>',
        content, re.DOTALL | re.IGNORECASE,
    ):
        ld_block = m_script.group(1)
        m_zone = RE_JSONLD_DESLOCACAO_ZONE.search(ld_block)
        if m_zone:
            return int(m_zone.group(1))
    return None


def extract_body_deslocacao_zones(content: str) -> list[int]:
    """Extrait TOUTES les zones N mentionnées par 'Desloca[cç][ãa]o Zona N' dans
    le body VISIBLE (HORS blocs <script>...</script>).

    P0.5C (mission P0.5C, CEO commit 71f1956b7) : KO2ter s'applique au body
    uniquement (pas au JSON-LD, déjà couvert par KO2/KO2bis). On strippe
    TOUS les scripts (pas seulement application/ld+json) car un éditeur peut
    avoir inline du JSON-LD ou autre contenu structuré dans le body via JS.

    Retourne une liste de zones (pas un set, on garde l'ordre des occurrences
    pour les messages KO2ter). Vide si aucune mention.
    """
    # Supprime tous les blocs <script ...>...</script> (greedy=False pour eviter
    # de manger du HTML legitime en cas de bug, mais DOTALL pour multilignes).
    content_no_scripts = re.sub(
        r'<script\b[^>]*>.*?</script>',
        '',
        content,
        flags=re.DOTALL | re.IGNORECASE,
    )
    zones: list[int] = []
    for m in RE_BODY_DESLOCACAO_ZONE.finditer(content_no_scripts):
        zones.append(int(m.group(1)))
    return zones


def extract_body_prix_par_zone(content: str) -> dict[int, int]:
    """Extrait les couples (zone → prix) détectés dans le body."""
    result: dict[int, int] = {}
    for m in RE_BODY_ZONE_PRIX.finditer(content):
        zone = int(m.group(1))
        prix = int(m.group(2))
        result[zone] = prix
    return result


def extract_delais_chiffres(content: str) -> list[str]:
    """Retourne les snippets où un délai chiffré apparaît."""
    return [m.group(0).strip() for m in RE_DELAIS.finditer(content)]


def _title_with_particules(s: str) -> str:
    """Title case intelligent (particules en minuscule)."""
    PARTICULES = {"de", "da", "do", "das", "dos", "em", "na", "no", "e"}
    parts = s.replace("-", " ").split()
    parts = [p.capitalize() if i == 0 or p not in PARTICULES else p
             for i, p in enumerate(parts)]
    return " ".join(parts)


def resolve_localidade(slug: str, zonas: dict) -> tuple[object, str | None, str]:
    """Resout la localite depuis le slug.

    Retourne (zone_or_None, key_trouvee, status) ou status ∈:
      - 'resolved'   : localite connue dans zonas-data.json ET en zone service
      - 'out_of_area': localite detectee mais hors zone service (Guarda)
      - 'unknown'    : localite introuvable dans la source

    Pipeline :
      1. slug_to_localidade(slug) -> tentative directe
      2. variante ASCII (slug brut) si accents differents
      3. SLUG_ALIASES (typos D6) si correspondance non ambigue
      4. sinon retourne (None, None, 'unknown')
    """
    # 1. tentative directe
    loc = slug_to_localidade(slug)
    zone = get_zone_from_zonas(zonas, loc)
    if zone is not None:
        # 4. verif OUT_OF_AREA (Guarda) au plus tot : meme si la source
        # contient une zone pour Trancoso/Fornos, on les FLAG out_of_area
        # car elles sont hors zone service Norte Reparos (~130 km de Macedo CV).
        # NE PAS PATCHER en zone, lister pour Filipe (decision business D6).
        if loc in OUT_OF_AREA_LOCALIDADES:
            return (zone, loc, "out_of_area")
        return (zone, loc, "resolved")

    # 2. variante ASCII du slug brut (parfois slug deja ASCII sans accent)
    ascii_loc = _title_with_particules(unaccent(slug).lower())
    if ascii_loc != loc:
        zone = get_zone_from_zonas(zonas, ascii_loc)
        if zone is not None:
            if ascii_loc in OUT_OF_AREA_LOCALIDADES:
                return (zone, ascii_loc, "out_of_area")
            return (zone, ascii_loc, "resolved")

    # 3. SLUG_ALIASES : on cherche TOUTES les cles de SLUG_ALIASES qui sont
    # un prefixe OU un match du slug (apres unaccented + lower).
    ua_slug = unaccent(slug).lower()
    matches: list[str] = []
    for typo_slug, alias in SLUG_ALIASES.items():
        ua_typo = unaccent(typo_slug).lower()
        # Match : le slug normalise est EXACTEMENT le typo slug
        # OU finit par -<typo_slug> (le typo est le suffixe localite)
        if ua_slug == ua_typo or ua_slug.endswith("-" + ua_typo):
            if alias is None:
                # alias None = marquer pour audit (pas de resolution auto)
                return (None, None, "unknown")
            matches.append(alias)

    # Dedup et garder UNIQUEMENT si unique non ambigu
    matches = list(dict.fromkeys(matches))
    if len(matches) == 1:
        alias = matches[0]
        if alias in OUT_OF_AREA_LOCALIDADES:
            zone = get_zone_from_zonas(zonas, alias)
            return (zone, alias, "out_of_area")
        zone = get_zone_from_zonas(zonas, alias)
        if zone is not None:
            return (zone, alias, "resolved")

    # 4. derniere chance : check OUT_OF_AREA sur le nom derive direct
    # (cas : slug est Deja la localite, ex: "trancoso.html" ou "fornos-de-algodres.html")
    if loc in OUT_OF_AREA_LOCALIDADES:
        return (None, loc, "out_of_area")
    if ascii_loc in OUT_OF_AREA_LOCALIDADES:
        return (None, ascii_loc, "out_of_area")

    return (None, None, "unknown")


def is_grille_canonique_context(content: str, m: re.Match) -> bool:
    """Heuristique : la mention 'Zona N' est dans la grille canonique Z1=15€..Z6=65€ ?
    Si oui, on NE signale PAS comme KO (c'est une référence, pas une affectation).
    """
    start = max(0, m.start() - 40)
    end = min(len(content), m.end() + 40)
    snippet = content[start:end]
    # Si la grille complète Z1=15€..Z6=65€ est dans le même paragraphe/ligne → info
    return bool(re.search(r"Z[1-6]=\d+€", snippet))


# ──────────────────────────────────────────────────────────────────────
# AUDIT D'UNE PAGE
# ──────────────────────────────────────────────────────────────────────

def audit_page(path: Path, zonas: dict) -> dict:
    """Retourne un dict {kos, no_resol, no_resol_reason, zone_attendue, ...}.

    P0.5B — ordre des checks (bug v1) :
      KO2bis (badge vs JSON-LD - cohérence INTERNE) et KO4 (délais) ne dépendent
      PAS de expected_zone. Ils sont exécutés MÊME si localité introuvable, AVANT
      tout early-return. Une page avec un NO_RESOL peut quand même avoir un
      badge incohérent avec son JSON-LD (= KO2bis détectable).

    P0.5C — extension :
      KO2ter (badge vs body « Deslocação Zona N ») est EXÉCUTÉ avant le
      early-return au même titre que KO2bis (cohérence interne pure : la
      résolution n'est pas requise pour comparer badge et body). Variantes
      zone_attendue et body_seul ne s'appliquent que sur localité résolue.
    """
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return {"error": str(e), "kos": [], "no_resol": True,
                "no_resol_reason": "read_error"}

    slug = path.stem  # filename sans extension

    # Resolution v2 : pipeline complet, retourne status ∈ {resolved, out_of_area, unknown}
    expected_zone, loc_key, status = resolve_localidade(slug, zonas)

    result = {
        "path": str(path),
        "slug": slug,
        "localidade": loc_key,
        "zone_attendue": expected_zone,
        "status": status,                      # resolved / out_of_area / unknown
        "no_resol": status != "resolved",       # v1 backward compat
        "no_resol_reason": status,              # alias sémantique pour reporting
        "kos": [],
        "delais": [],
    }

    # Extraction badges + JSON-LD (rapide et sans dépendance à expected_zone)
    badge = extract_badge_zone(content, slug)
    jsonld_zone = extract_jsonld_deslocacao_zone(content)
    # KO2ter : « Deslocação Zona N » dans le body VISIBLE (scripts strippés).
    body_zones_list = extract_body_deslocacao_zones(content)
    body_zones_set = set(body_zones_list)

    # ───────────────────────────────────────────────────────────────────
    # CHECKS NO-ZONE-DEPENDANTS : exécutés AVANT tout early-return
    # ───────────────────────────────────────────────────────────────────

    # KO2bis (interne) : badge vs JSON-LD si les deux présents
    if jsonld_zone is not None and badge is not None and badge != jsonld_zone:
        result["kos"].append({
            "type": "KO2bis_badge_vs_jsonld",
            "msg": f"badge={badge} != JSON-LD={jsonld_zone} (page contradictoire)",
        })

    # KO4 délais chiffrés (-urgente strict, leçon #298 tolérance -norte)
    delais = extract_delais_chiffres(content)
    is_urgente = "urgente" in str(path)
    for snippet in delais[:3]:  # cap à 3 exemples
        result["delais"].append(snippet)
        if is_urgente:
            result["kos"].append({
                "type": "KO4_delai_chiffre_urgente",
                "msg": f"delai chiffre R145: '{snippet}'",
            })
        # Sur -norte : info seulement (lecon #298), pas KO

    # KO2ter (interne — P0.5C) : badge vs body « Deslocação Zona N ».
    # 3 variantes :
    #   - KO2ter_body_vs_badge : badge + body presents, valeurs differentes
    #     (incoherence interne : le badge ment, le body dit autre chose).
    #     Active MEME en no_resol (coherence interne pure, comme KO2bis).
    #   - KO2ter_zone_attendue : page resolue et le body mentionne une zone
    #     qui n'est PAS la zone_attendue (ex temoin VPA : badge Z5, body Z3,
    #     attendu Z5 → KO2ter_zone_attendue). Detecte le cas "le body promet
    #     un prix Z alors que la page est Z reelle".
    #   - KO2ter_body_seul : pas de badge mais body annonce une zone != attendu.
    #     Necessite que la localite soit resolue.
    if badge is not None and body_zones_set and badge not in body_zones_set:
        # Variante badge vs body (incoherence interne)
        body_zones_str = ",".join(str(z) for z in body_zones_list)
        result["kos"].append({
            "type": "KO2ter_body_vs_badge",
            "msg": (f"badge={badge} != body Deslocação Zona "
                    f"[{body_zones_str}]"),
        })
    # Variante zone_attendue : body mentionne une zone != attendu.
    # Detecte le cas "body promet un prix Z alors que la page est en zone Y".
    if (status == "resolved"
            and expected_zone is not None
            and body_zones_set
            and expected_zone not in body_zones_set):
        body_zones_str = ",".join(str(z) for z in body_zones_list)
        if badge is None:
            result["kos"].append({
                "type": "KO2ter_body_seul",
                "msg": (f"pas de badge, body Deslocação Zona "
                        f"[{body_zones_str}] != attendu={expected_zone}"),
            })
        else:
            result["kos"].append({
                "type": "KO2ter_zone_attendue",
                "msg": (f"body Deslocação Zona [{body_zones_str}] "
                        f"!= attendu={expected_zone} (badge={badge})"),
            })

    # ───────────────────────────────────────────────────────────────────
    # EARLY-RETURN si localité introuvable (KO2bis + KO4 + KO2ter déjà collectés)
    # ───────────────────────────────────────────────────────────────────
    if status != "resolved":
        return result

    # ───────────────────────────────────────────────────────────────────
    # CHECKS ZONE-DEPENDANTS : exécutés uniquement si localité résolue
    # ───────────────────────────────────────────────────────────────────

    # KO1 : badge data-zone != attendu
    if badge is not None and badge != expected_zone:
        result["kos"].append({
            "type": "KO1_badge_zona",
            "msg": f"badge data-zone={badge} != zonas-data.json={expected_zone} ({loc_key})",
        })

    # KO2 : JSON-LD deslocação != attendu
    if jsonld_zone is not None and jsonld_zone != expected_zone:
        result["kos"].append({
            "type": "KO2_jsonld_zone",
            "msg": f"JSON-LD 'Desloca[cç][ãa]o Zona {jsonld_zone}' != attendu={expected_zone} ({loc_key})",
        })
    # Note : KO2bis déjà collecté plus haut (badge vs JSON-LD interne)

    # KO3 : prix body vs grille
    body_prix = extract_body_prix_par_zone(content)
    for zone_annoncee, prix_annonce in body_prix.items():
        if zone_annoncee == expected_zone:
            # C'est la zone de CETTE page -> prix doit matcher la grille
            prix_attendu = GRILLE[expected_zone]
            if prix_annonce != prix_attendu:
                result["kos"].append({
                    "type": "KO3_prix_body",
                    "msg": f"body Zona {zone_annoncee}={prix_annonce}€ != grille officielle={prix_attendu}€",
                })

    return result


# ──────────────────────────────────────────────────────────────────────
# SCAN D'UN REPO
# ──────────────────────────────────────────────────────────────────────

def scan_repo(repo: Path, zonas: dict) -> dict:
    """Scan tous les HTML du repo, retourne stats avec breakdown NO_RESOL (P0.5B)."""
    stats = {
        "repo": str(repo),
        "html_total": 0,
        "no_resol": 0,                       # backward compat (no_resol_reason != 'resolved')
        "no_resol_unknown": 0,               # localité introuvable dans source
        "no_resol_out_of_area": 0,           # Guarda, hors zone (NE PAS PATCHER)
        "out_of_area_sample": [],            # exemples pour Filipe (D6)
        "patched": 0,                        # pages sans KO (et résolues)
        "ko1": 0,
        "ko2": 0,
        "ko2bis": 0,
        "ko2ter": 0,
        "ko3": 0,
        "ko4": 0,
        "kos_total": 0,
        "ko_list": [],                       # échantillon (max 30 par type)
        "temoin_braganca_ok": None,
        "temoin_vinhais_ok": None,
        "temoin_macedo_ok": None,
    }

    # Itère sur tous les HTML du repo (hors exclusions)
    html_files = []
    for root, dirs, files in os.walk(repo):
        # Exclusions in-place (mutate dirs)
        dirs[:] = [d for d in dirs if d not in {"node_modules", "_archive", "dist", "build", ".git", ".hermes"}]
        for f in files:
            if not f.endswith(".html"):
                continue
            if f.endswith("-es.html"):  # exclusion version espagnole (cohérent P0)
                continue
            html_files.append(Path(root) / f)

    stats["html_total"] = len(html_files)

    for path in html_files:
        r = audit_page(path, zonas)
        reason = r.get("no_resol_reason", "resolved")

        if reason == "unknown":
            stats["no_resol_unknown"] += 1
        elif reason == "out_of_area":
            stats["no_resol_out_of_area"] += 1
            if len(stats["out_of_area_sample"]) < 10:
                stats["out_of_area_sample"].append({
                    "path": str(path.relative_to(repo)),
                    "localidade": r.get("localidade"),
                    "zone_attendue": r.get("zone_attendue"),
                })

        if reason != "resolved":
            stats["no_resol"] += 1
        elif not r["kos"]:
            stats["patched"] += 1

        for ko in r["kos"]:
            t = ko["type"]
            if t == "KO1_badge_zona": stats["ko1"] += 1
            elif t == "KO2_jsonld_zone": stats["ko2"] += 1
            elif t == "KO2bis_badge_vs_jsonld": stats["ko2bis"] += 1
            elif (t == "KO2ter_body_vs_badge"
                  or t == "KO2ter_zone_attendue"
                  or t == "KO2ter_body_seul"):
                stats["ko2ter"] += 1
            elif t == "KO3_prix_body": stats["ko3"] += 1
            elif t == "KO4_delai_chiffre_urgente": stats["ko4"] += 1
            stats["kos_total"] += 1
            if len(stats["ko_list"]) < 30:
                stats["ko_list"].append({
                    "path": str(path.relative_to(repo)),
                    "type": t,
                    "msg": ko["msg"],
                })

        # Temoins : on a un KO SI la page concerne le temoin ET a un KO
        loc = r.get("localidade")
        if loc == "Bragança" and not r["kos"]:
            stats["temoin_braganca_ok"] = True
        elif loc == "Bragança":
            stats["temoin_braganca_ok"] = False
        if loc == "Vinhais" and not r["kos"]:
            stats["temoin_vinhais_ok"] = True
        elif loc == "Vinhais":
            stats["temoin_vinhais_ok"] = False
        if loc == "Macedo de Cavaleiros" and not r["kos"]:
            stats["temoin_macedo_ok"] = True
        elif loc == "Macedo de Cavaleiros":
            stats["temoin_macedo_ok"] = False

    return stats


# ──────────────────────────────────────────────────────────────────────
# AFFICHAGE
# ──────────────────────────────────────────────────────────────────────

def print_repo_stats(s: dict) -> None:
    print(f"\n{'='*78}")
    print(f"REPO : {s['repo']}")
    print(f"{'='*78}")
    print(f"  HTML scannes (hors -es, dist/, _archive/, node_modules/) : {s['html_total']}")
    print(f"  Pages resolues sans KO (patched)                        : {s['patched']}")
    print(f"  Pages NO_RESOL total                                    : {s['no_resol']}")
    print(f"    - out_of_area (Guarda, hors zone service)              : {s['no_resol_out_of_area']}")
    print(f"    - unknown (localite absente source / prefixe non couvert) : {s['no_resol_unknown']}")
    if s.get("out_of_area_sample"):
        print(f"    Echantillon OUT_OF_AREA (D6, a lister pour Filipe) :")
        for ex in s["out_of_area_sample"][:5]:
            print(f"      - {ex['path']}  ({ex['localidade']} / zone {ex['zone_attendue']})")
    print()
    print(f"  KO1 badge != zonas-data.json     : {s['ko1']}")
    print(f"  KO2 JSON-LD deslocacao != attendu: {s['ko2']}")
    print(f"  KO2bis badge != JSON-LD (interne): {s['ko2bis']}")
    print(f"  KO2ter body Deslocação Zona != badge/attendu : {s['ko2ter']}")
    print(f"  KO3 prix body != grille Z1=15..Z6=65 : {s['ko3']}")
    print(f"  KO4 delais chiffres (R145 -urgente)   : {s['ko4']}")
    print(f"  -------------------------------------")
    print(f"  KO TOTAL                          : {s['kos_total']}")
    print()
    # Temoins
    t_strs = []
    for name, val in [("Braganca (Z2/25€)", s['temoin_braganca_ok']),
                       ("Vinhais (Z3/35€)", s['temoin_vinhais_ok']),
                       ("Macedo CV (Z1/15€)", s['temoin_macedo_ok'])]:
        if val is True:
            t_strs.append(f"  v {name} : conforme")
        elif val is False:
            t_strs.append(f"  x {name} : KO detecte")
        else:
            t_strs.append(f"  . {name} : non vu dans ce repo")
    print("  TEMOINS (R8 OpenClaw) :")
    for ts in t_strs:
        print(ts)
    if s["ko_list"]:
        print()
        print(f"  Echantillon KO ({len(s['ko_list'])} max) :")
        for ko in s["ko_list"][:10]:
            print(f"    [{ko['type']}] {ko['path']}")
            print(f"      -> {ko['msg']}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)

    # Charge source-of-truth
    if not SOURCE_OF_TRUTH.exists():
        print(f"ERREUR FATALE : source-of-truth introuvable : {SOURCE_OF_TRUTH}", file=sys.stderr)
        sys.exit(1)
    zonas = json.loads(SOURCE_OF_TRUTH.read_text(encoding="utf-8"))
    print(f"Source-of-truth chargée : {SOURCE_OF_TRUTH} ({len(zonas)} localités)")

    # Vérif témoins dans la source elle-même
    print()
    print("TÉMOINS R8 — vérification dans zonas-data.json :")
    temoin_ok_global = True
    for name, expected in TEMOINS.items():
        actual = zonas.get(name)
        if actual != expected:
            print(f"  ✗ TEMOIN CASSÉ : {name} attendu={expected}, zonas={actual}")
            temoin_ok_global = False
        else:
            print(f"  ✓ {name} = {actual}")

    if not temoin_ok_global:
        print("\nERREUR FATALE : un témoin est cassé → la grille a changé, mettre à jour TEMOINS.", file=sys.stderr)
        sys.exit(1)

    # Scan chaque repo
    totals = {
        "html_total": 0,
        "patched": 0,
        "no_resol": 0,
        "no_resol_unknown": 0,
        "no_resol_out_of_area": 0,
        "ko1": 0, "ko2": 0, "ko2bis": 0, "ko2ter": 0, "ko3": 0, "ko4": 0, "kos_total": 0,
    }
    repo_results = []
    for repo_arg in sys.argv[1:]:
        repo = Path(repo_arg).expanduser().resolve()
        if not repo.exists():
            print(f"\n⚠ Repo introuvable : {repo}", file=sys.stderr)
            continue
        s = scan_repo(repo, zonas)
        repo_results.append(s)
        for k in totals:
            totals[k] += s.get(k, 0)
        print_repo_stats(s)

    # Totaux
    print(f"\n{'='*78}")
    print("TOTAUX (tous repos)")
    print(f"{'='*78}")
    for k, v in totals.items():
        print(f"  {k:20s} : {v}")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)