#!/usr/bin/env python3
"""Générateur des pages concelho (eletricista-urgente).
Source unique = data/concelhos.json + data/localidades.json (dérivés d'AUTORITAIRE + TomTom).
Produit concelhos/{slug}.html pour chaque concelho indexable avec drive-time réel.

Règles dures appliquées:
- Cœur métier ÉLEC uniquement (0 plomberie, 0 DGEG, 0 solaire).
- NAP élec = +351 932 321 892 partout.
- Prix = CANAL (grille AUTORITAIRE), pas de +5€.
- Titres / meta / H1 uniques par concelho (data réelle).
- canonical self extensionless (cleanUrls).
- Drive-time = valeur réelle TomTom, jamais estimée.
Reproductible: relancer ce script régénère à l'identique.
"""
import json, os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(REPO, "data")
OUT = os.path.join(REPO, "concelhos")
BASE = "https://eletricista-urgente.pt"
TEL = "+351 932 321 892"
TEL_RAW = "932321892"
HUB = "Macedo de Cavaleiros"

def page(c, locs):
    name = c["name"]; slug = c["slug"]; district = c["district"]; zone = c["zone"]
    p = c["price"]; desloc = p["desloc"]; desde = p["desde"]; h2 = p["h2"]
    rkm = c["route_km"]; rmin = c["route_min"]; is_hub = c.get("hub")
    url = f"{BASE}/concelhos/{slug}"

    if is_hub:
        dist_line = f"Macedo de Cavaleiros é a nossa base de operações — resposta imediata em todo o concelho."
        title_km = ""
    else:
        dist_line = (f"A {rkm:.0f} km de {HUB} (tempo médio de viagem ~{rmin} min). "
                     f"Deslocamo-nos a todo o concelho de {name}.")
        title_km = ""

    # Localidades servidas (proximité réelle, TomTom). Peut être vide.
    if locs:
        items = "".join(f"<li>{l['name']}</li>" for l in locs)
        locs_block = f"""
 <h2>Localidades servidas na zona de {name}</h2>
 <p>Deslocamo-nos a {name} e às localidades em redor. Algumas das localidades que servimos nesta zona:</p>
 <ul class="aldeias-grid">
 {items}
 </ul>"""
    else:
        locs_block = ""

    schema = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": f"Norte Reparos — Eletricista Urgente {name}",
        "telephone": TEL,
        "priceRange": f"{desloc}€–{h2}€",
        "address": {"@type": "PostalAddress", "addressLocality": name,
                    "addressRegion": district, "addressCountry": "PT"},
        "areaServed": {"@type": "AdministrativeArea", "name": f"Concelho de {name}"},
        "openingHoursSpecification": {"@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
            "opens": "00:00", "closes": "23:59"},
    }
    schema_json = json.dumps(schema, ensure_ascii=False, indent=1)

    desc = (f"Eletricista urgente em {name} ({district}). Deslocação {desloc}€, "
            f"resposta 24h/7d. Quadros, avarias e curto-circuitos. Ligue {TEL}.")
    if not is_hub:
        desc = (f"Eletricista urgente em {name} ({district}), a ~{rmin} min de viagem. "
                f"Deslocação {desloc}€, 24h/7d. Ligue {TEL}.")

    return f"""<!DOCTYPE html>
<html lang="pt-PT">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>🚨 Eletricista Urgente {name} {desloc}€ | Norte Reparos</title>
 <meta name="description" content="{desc}">
 <link rel="canonical" href="{url}">
 <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
 <meta property="og:title" content="Eletricista Urgente no Concelho de {name}">
 <meta property="og:description" content="{desc}">
 <meta property="og:type" content="article">
 <meta property="og:url" content="{url}">
 <meta property="og:image" content="{BASE}/og-image.png">
 <meta property="og:image:width" content="1200">
 <meta property="og:image:height" content="630">
 <meta name="geo.placename" content="{name}, {district}">
 <meta name="theme-color" content="#FF6B35">
 <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
 <script type="application/ld+json">
{schema_json}
 </script>
 <style>
 body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; max-width: 800px; margin: 0 auto; padding: 2rem 1rem; line-height: 1.7; color: #333; }}
 h1 {{ color: #FF6B35; border-bottom: 3px solid #FF6B35; padding-bottom: .5rem; }}
 h2 {{ color: #FF6B35; margin-top: 2.5rem; }}
 .info-box {{ background: #f0f9ff; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #FF6B35; margin: 1.5rem 0; }}
 .aldeias-grid {{ columns: 3; column-gap: 1rem; padding-left: 1.2rem; }}
 .aldeias-grid li {{ break-inside: avoid; }}
 .cta {{ background: #FF6B35; color: white; padding: 2rem; border-radius: 8px; margin: 2rem 0; text-align: center; }}
 .cta a {{ color: white; font-weight: bold; }}
 </style>
</head>
<body role="document">
 <nav role="navigation" style="font-size:.85rem;color:#666;margin-bottom:1rem">
 <a href="/" style="color:#FF6B35;text-decoration:none">Início</a> »
 <a href="/distritos/{district_slug(district)}.html" style="color:#FF6B35;text-decoration:none">{district}</a> »
 Concelho de {name}
 </nav>

 <h1 role="heading" aria-level="1">Eletricista Urgente no Concelho de {name}</h1>

 <div class="info-box">
 <p><strong>Concelho:</strong> {name}</p>
 <p><strong>Distrito:</strong> {district}</p>
 <p><strong>Distância desde {HUB}:</strong> {dist_desc(c)}</p>
 <p><strong>Zona tarifária:</strong> Zona {zone} — deslocação {desloc}€ (já incluída no orçamento)</p>
 </div>

 <p>{dist_line}</p>

 <h2>Serviços de eletricista em {name}</h2>
 <ul>
 <li>Avarias elétricas urgentes e curto-circuitos</li>
 <li>Quadros elétricos e disjuntores que disparam</li>
 <li>Tomadas, interruptores e pontos de luz</li>
 <li>Iluminação interior e exterior (LED)</li>
 <li>Instalação e substituição de cabos e circuitos</li>
 <li>Resposta de urgência 24h/7d em todo o concelho</li>
 </ul>
{locs_block}

 <h2>Preços em {name}</h2>
 <div class="info-box">
 <p><strong>Deslocação (Zona {zone}):</strong> {desloc}€ — incluída no orçamento</p>
 <p><strong>Intervenção (1h):</strong> desde {desde}€</p>
 <p><strong>Intervenção (2h):</strong> {h2}€</p>
 <p style="font-size:.85rem;color:#666;margin-top:.8rem">Preço de deslocação fixo, comunicado antes da chegada. Orçamento gratuito e sem compromisso.</p>
 </div>

 <h2>Sobre a Norte Reparos</h2>
 <p>A Norte Reparos é uma equipa de eletricistas com base em {HUB}, ao serviço do concelho de {name} e de toda a região transmontana. Resposta rápida 24 horas por dia, 7 dias por semana, incluindo fins de semana e feriados. Fatura com NIF e garantia sobre os trabalhos realizados.</p>

 <h2>Perguntas frequentes — Eletricista em {name}</h2>
 <p><strong>Quanto tempo demoram a chegar a {name}?</strong><br>{faq_time(c)}</p>
 <p style="margin-top:1rem"><strong>Quanto custa a deslocação?</strong><br>A deslocação para a Zona {zone} é de {desloc}€ e está incluída no orçamento.</p>
 <p style="margin-top:1rem"><strong>Atendem de noite, fins de semana e feriados?</strong><br>Sim, 24h por dia, 7 dias por semana, sem custo adicional de marcação.</p>
 <p style="margin-top:1rem"><strong>Emitem fatura?</strong><br>Sim, fatura detalhada com NIF e relatório técnico quando aplicável.</p>

 <div class="cta">
 <h2 style="color:#fff">Precisa de eletricista em {name}?</h2>
 <p>📞 <a href="tel:{TEL_RAW}">{TEL}</a></p>
 <p>💬 <a href="https://wa.me/351{TEL_RAW}">WhatsApp</a></p>
 <p><a href="/zonas-deslocacao.html">Zonas de deslocação</a> · <a href="/calculadora-de-preco.html">Calculadora de preço</a></p>
 </div>
</body>
</html>
"""

def district_slug(d):
    import unicodedata
    s=''.join(c for c in unicodedata.normalize('NFD',d) if unicodedata.category(c)!='Mn').lower()
    return s.replace(' ','-')

def dist_desc(c):
    if c.get("hub"): return "0 km (base de operações)"
    return f"{c['route_km']:.0f} km por estrada (~{c['route_min']} min)"

def faq_time(c):
    if c.get("hub"):
        return "Macedo de Cavaleiros é a nossa base — chegamos no menor tempo possível, com prioridade a emergências."
    return (f"O tempo médio de viagem desde {HUB} é de cerca de {c['route_min']} minutos "
            f"({c['route_km']:.0f} km). Para emergências, damos prioridade máxima.")

def main():
    concelhos = json.load(open(os.path.join(DATA,"concelhos.json")))
    localidades = json.load(open(os.path.join(DATA,"localidades.json")))
    os.makedirs(OUT, exist_ok=True)
    written = []; skipped = []
    for c in concelhos:
        if not c.get("indexable") or c.get("drive_time_status") != "real_tomtom":
            skipped.append((c["name"], c.get("drive_time_status")))
            continue
        html = page(c, localidades.get(c["slug"], []))
        with open(os.path.join(OUT, c["slug"]+".html"), "w") as f:
            f.write(html)
        written.append(c["slug"])
    print(f"écrites: {len(written)}")
    print(f"skipped (held/a_completar): {skipped}")
    return written

if __name__ == "__main__":
    main()
