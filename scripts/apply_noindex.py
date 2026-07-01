#!/usr/bin/env python3
"""Applique noindex aux pages NON indexables (eletricista-urgente).

Politique (décisions verrouillées + GO Filipe):
- Toutes les pages-aldeia doorway racine `eletricista-*.html`  -> noindex,follow
- Pages hors cœur métier (solaire / VE / DGEG)                 -> noindex,follow (PAS supprimées)
Le set indexable canonique = concelhos/{slug}.html (généré) + pages cœur légitimes.

Idempotent: relancer ne change rien de plus.
"""
import glob, os, re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FORBIDDEN = [  # hors cœur métier — noindex, conservés (gate compliance séparé)
    "calculadora-roi-solar.html",
    "como-instalar-painel-solar.html",
    "painel-solar-vale-pena.html",
    "como-carregar-carro-eletrico-casa.html",
    # G2 (2026-06-23) — contamination cœur métier encore indexable.
    # Plomberie sur site ÉLEC (cross-craft, viole NAP/cœur strict):
    "guia-canalizacao.html",
    "glossario-canalizacao.html",
    "top-10-fugas-mais-comuns.html",
    "top-10-razoes-contratar-canalizador.html",
    # Solaire / VE (hors cœur, même politique que les 5 ci-dessus):
    "blog/painel-solar-avariado.html",
    "blog/avaria-carregador-carro.html",
    "public/blog/bateria-solar-vale-pena.html",
    "public/blog/carregador-carro-eletrico-garagem.html",
    "public/blog/carregador-carro-eletrico-problema.html",
    "public/blog/carregador-carro-eletrico-solar.html",
    "public/blog/como-escolher-painel-solar-casa.html",
]

ROBOTS_RE = re.compile(r"<meta\s+name=(['\"])robots\1\s+content=(['\"])(.*?)\2\s*/?>", re.I)

def to_noindex(html):
    """Force every robots meta to noindex,follow. Inject one if none present."""
    found = [False]
    def repl(m):
        found[0] = True
        q = m.group(2)
        return f"<meta name=\"robots\" content={q}noindex, follow{q}>"
    new = ROBOTS_RE.sub(repl, html)
    if not found[0]:
        # inject right after <head>
        new = re.sub(r"(<head[^>]*>)", r'\1\n <meta name="robots" content="noindex, follow">',
                     new, count=1, flags=re.I)
    return new

def main():
    os.chdir(REPO)
    targets = set(glob.glob("eletricista-*.html"))   # aldeia doorways racine
    for f in FORBIDDEN:
        if os.path.exists(f):
            targets.add(f)
    changed = 0
    for f in sorted(targets):
        html = open(f, encoding="utf-8").read()
        new = to_noindex(html)
        if new != html:
            open(f, "w", encoding="utf-8").write(new)
            changed += 1
    print(f"cibles: {len(targets)}  modifiées: {changed}")
    # sanity: aucune cible ne doit rester 'index' (hors noindex)
    still_index = []
    for f in sorted(targets):
        html = open(f, encoding="utf-8").read()
        for m in ROBOTS_RE.finditer(html):
            if "noindex" not in m.group(3).lower():
                still_index.append(f); break
    print(f"cibles restées indexables (doit=0): {len(still_index)} {still_index[:5]}")

if __name__ == "__main__":
    main()
