#!/usr/bin/env python3
"""Génère un sitemap.xml pour eletricista-urgente.pt — DISCOVERY FIX.

INCLUT (served 200, no noindex, qualité money/service) :
- home + pages pilier/info élec (precos, sobre, FAQ, etc.)
- /concelhos/{slug} (33 concelhos indexables real_tomtom)
- /distritos/{slug} (6 distritos)
- /blog/{slug} (25 articles blog élec)
- /eletricista-urgente-{aldeia} (256 villes, canonique sans acento)
- /eletricista-{service}-{aldeia} (539 pages : avaria, tomada, quadro,
  iluminacao-led, iluminacao-exterior, fuga-corrente, certificacao)

EXCLUT :
- aldeias doorway simples (eletricista-{aldeia}.html) — scaled content risk
- pages com <meta name="robots" content="noindex">
- pages pilier "canal" (glossario-canalizacao, guia-canalizacao, etc.)
- doublons aldeias (variantes acentuées dont l'équivalent sans acento existe)
- /404, /public/404
- politique cookies/privacidade, termos-condicoes (faible valeur SEO)

Format URL : extensionless (servi sans .html).
Site de référence : https://eletricista-urgente.pt
"""
import json
import os
import re
import unicodedata
import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BASE = "https://eletricista-urgente.pt"
TODAY = datetime.date.today().isoformat()

NOINDEX_RE = re.compile(r'<meta[^>]*robots[^>]*noindex', re.IGNORECASE)

# Services money élec (qualité, taille ~18-20K, no noindex)
SERVICE_PREFIXES = (
    "eletricista-avaria-eletrica-",
    "eletricista-tomada-interruptor-",
    "eletricista-quadro-eletrico-",
    "eletricista-iluminacao-led-",
    "eletricista-iluminacao-exterior-",
    "eletricista-fuga-corrente-",
    "eletricista-certificacao-eletrica-",
)

URGENTE_PREFIX = "eletricista-urgente-"

# Pages pilier/info élec (à inclure, ordre prioritaire)
PILIER_ELEC = (
    "/",
    "/precos",
    "/contactos",
    "/sobre",
    "/equipa",
    "/garantia",
    "/testemunhos",
    "/metodologia",
    "/perguntas-frequentes",
    "/recursos-gratuitos",
    "/imprensa",
    "/indice-a-z",
    "/calculadora-de-preco",
    "/comparacao",
    "/sinais-alerta-casa-antiga",
    "/como-poupar-eletricidade",
    "/top-10-razoes-contratar-eletricista",
    "/guia-eletricidade",
    "/glossario-eletricidade",
    "/zona-intervencao",
    "/zonas-deslocacao",
    "/mapa-do-site",
    "/trabalhar-conosco",
    # pages de prix par ville (pilier SEO)
    "/preco-eletricista-urgente-braganca-2026",
    "/preco-eletricista-urgente-chaves-2026",
    "/preco-eletricista-urgente-mirandela-2026",
    "/preco-eletricista-urgente-vila-real-2026",
)

# Pages exclues explicitement (canal/noindex/faible valeur/legacy 301)
EXCLUDE_PATHS = {
    "/politica-cookies",
    "/politica-privacidade",
    "/termos-condicoes",
    "/glossario-canalizacao",  # noindex + hors-périmètre
    "/guia-canalizacao",       # noindex + hors-périmètre
    "/top-10-fugas-mais-comuns",  # noindex + hors-périmètre
    "/top-10-razoes-contratar-canalizador",  # noindex + hors-périmètre
    "/404",
    # Legacy : page urgente avec slug cassé, redirige (301) vers la bonne
    "/eletricista-urgente-carrazeda-de-anciaes",
}

# Stems (sans extension) à exclure en plus des paths ci-dessus
EXCLUDE_STEMS = {
    "eletricista-urgente-carrazeda-de-anciaes",
}


def norm_ascii(s: str) -> str:
    """Normalise un nom de fichier : NFKD -> ASCII lower."""
    return unicodedata.normalize("NFKD", s).encode("ASCII", "ignore").decode().lower()


def has_accent(s: str) -> bool:
    """Détecte tout caractère non-ASCII (accents portugais + espagnols)."""
    return any(ord(c) > 127 for c in s)


def is_indexable(filepath: Path) -> bool:
    """Vérifie qu'une page .html n'a pas de meta robots noindex."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
        if NOINDEX_RE.search(content[:8000]):  # HEAD only
            return False
        return True
    except Exception:
        return False


def collect_concelhos():
    """33 concelhos indexables real_tomtom."""
    data = json.loads((REPO / "data" / "concelhos.json").read_text(encoding="utf-8"))
    return [
        c["slug"] for c in data
        if c.get("indexable") and c.get("drive_time_status") == "real_tomtom"
    ]


def collect_distritos():
    """6 pages distritos/."""
    out = []
    dist_dir = REPO / "distritos"
    if dist_dir.exists():
        for f in sorted(dist_dir.glob("*.html")):
            if is_indexable(f):
                out.append(f.stem)
    return out


def collect_blog():
    """Articles blog élec — seulement les .html (les .md ne sont pas servis en page)."""
    out = []
    blog_dir = REPO / "blog"
    if blog_dir.exists():
        for f in sorted(blog_dir.glob("*.html")):
            if is_indexable(f):
                out.append(f.stem)
    return out


def collect_money_pages():
    """Pages dinheiro : urgentes + services × ville (canonique, sans acento).

    Exclut les doublons (variantes accentuées dont l'équivalent sans acento existe).
    """
    out = {"urgente": [], "service": []}

    # Étape 1 : scanner tous les fichiers .html racine
    candidates_urgente = []
    candidates_service = []
    for f in REPO.glob("*.html"):
        name = f.name
        if name.startswith(URGENTE_PREFIX):
            candidates_urgente.append(f)
        elif any(name.startswith(p) for p in SERVICE_PREFIXES):
            candidates_service.append(f)

    # Étape 2 : construire un index "sans acento" pour dédupliquer
    # Map : norm_ascii(name) -> Path (priorité à la version sans accent)
    def best_canonical(paths):
        """Pour un groupe de fichiers au slug normalisé équivalent :
        garde la version de plus grande taille (gold > thin).
        Si plusieurs à égalité de taille, garder la version sans accent."""
        if not paths:
            return []
        sem = [p for p in paths if not has_accent(p.name)]
        com = [p for p in paths if has_accent(p.name)]
        # Trier par taille décroissante, sans accent优先 si égalité
        sem_sorted = sorted(sem, key=lambda p: (-p.stat().st_size, p.name))
        com_sorted = sorted(com, key=lambda p: (-p.stat().st_size, p.name))
        if sem_sorted:
            return [sem_sorted[0]]
        return [com_sorted[0]]

    # Urgentes : dédoublonner
    by_norm_urgente = {}
    for p in candidates_urgente:
        by_norm_urgente.setdefault(norm_ascii(p.name), []).append(p)
    for norm, paths in by_norm_urgente.items():
        for p in best_canonical(paths):
            if is_indexable(p):
                out["urgente"].append(p.stem)

    # Services : dédoublonner
    by_norm_service = {}
    for p in candidates_service:
        by_norm_service.setdefault(norm_ascii(p.name), []).append(p)
    for norm, paths in by_norm_service.items():
        for p in best_canonical(paths):
            if is_indexable(p):
                out["service"].append(p.stem)

    # Trier alphabétiquement
    out["urgente"].sort()
    out["service"].sort()
    return out


def url_path(stem_or_path):
    """Convertit un stem en chemin URL (avec /initial si pas préfixé /)."""
    s = str(stem_or_path)
    if s.startswith("/"):
        return s
    return "/" + s


def build_sitemap():
    """Construit la liste d'URLs à inclure dans le sitemap."""
    urls = []  # (path, priority)

    # 1. Home (priority 1.0)
    urls.append(("/", "1.0"))

    # 2. Pages pilier/info élec
    for path in PILIER_ELEC:
        if path in EXCLUDE_PATHS:
            continue
        urls.append((path, "0.7"))

    # 3. Concelhos (priority 0.8 — page pilier géo)
    for slug in collect_concelhos():
        urls.append((f"/concelhos/{slug}", "0.8"))

    # 4. Distritos (priority 0.6 — SEO régional)
    for slug in collect_distritos():
        urls.append((f"/distritos/{slug}", "0.6"))

    # 5. Blog (priority 0.6 — articles longue traîne)
    for slug in collect_blog():
        urls.append((f"/blog/{slug}", "0.6"))

    # 6. Pages money : urgentes + services (priority 0.85)
    money = collect_money_pages()
    for stem in money["urgente"]:
        if stem in EXCLUDE_STEMS:
            continue
        urls.append((f"/{stem}", "0.85"))
    for stem in money["service"]:
        if stem in EXCLUDE_STEMS:
            continue
        urls.append((f"/{stem}", "0.8"))

    # Dédupliquer en gardant la priority la plus haute
    by_path = {}
    for path, pr in urls:
        if path not in by_path or float(pr) > float(by_path[path]):
            by_path[path] = pr

    # Trier : home en premier, puis par priorité décroissante, puis alphabétique
    def sort_key(item):
        path, pr = item
        pr_f = float(pr)
        # home toujours en premier
        if path == "/":
            return (0, "")
        return (1 - pr_f, path)

    return sorted(by_path.items(), key=sort_key)


def write_sitemap(paths_with_priority):
    """Écrit le fichier sitemap.xml au format extensionless.

    Écrit dans les DEUX emplacements (root + public/) : sur Vercel la racine
    est servie par défaut, public/ était historiquement mirroré ; on couvre
    les deux sans dépendre d'un curl prod inaccessible depuis ce worker.
    """
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path, pr in paths_with_priority:
        loc = f"{BASE}{path}"
        lines.append(f"<url><loc>{loc}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>")
    lines.append("</urlset>")
    out = "\n".join(lines) + "\n"

    targets = [REPO / "sitemap.xml"]
    public_dir = REPO / "public"
    if public_dir.exists():
        targets.append(public_dir / "sitemap.xml")

    for t in targets:
        t.write_text(out, encoding="utf-8")
    return targets, len(paths_with_priority)


def main():
    items = build_sitemap()
    targets, count = write_sitemap(items)
    out_path = targets[0]

    # Stats
    by_priority = {}
    for path, pr in items:
        by_priority.setdefault(pr, []).append(path)
    print(f"sitemap.xml écrit: {count} URLs ({', '.join(str(t) for t in targets)})")
    for pr in sorted(by_priority.keys(), key=float, reverse=True):
        print(f"  priority={pr}: {len(by_priority[pr])} URLs")
    # Échantillon par catégorie
    pilier_count = sum(1 for p, _ in items if p in PILIER_ELEC)
    concelhos_count = sum(1 for p, _ in items if p.startswith("/concelhos/"))
    distritos_count = sum(1 for p, _ in items if p.startswith("/distritos/"))
    blog_count = sum(1 for p, _ in items if p.startswith("/blog/"))
    urgente_count = sum(1 for p, _ in items if p.startswith("/eletricista-urgente-"))
    service_count = sum(
        1 for p, _ in items
        if any(p.startswith("/" + s) for s in SERVICE_PREFIXES)
    )
    print()
    print(f"Détail par type :")
    print(f"  Pilier/info:  {pilier_count}")
    print(f"  Concelhos:    {concelhos_count}")
    print(f"  Distritos:    {distritos_count}")
    print(f"  Blog:         {blog_count}")
    print(f"  Urgente:      {urgente_count}")
    print(f"  Service × ville: {service_count}")


if __name__ == "__main__":
    main()
