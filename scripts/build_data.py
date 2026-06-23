#!/usr/bin/env python3
# One-time builder: merge AUTORITAIRE (zones/prix CANAL) + TomTom (drive-time réel + coords)
# Emits in-repo snapshots: data/concelhos.json + data/localidades.json
# Rule: n'invente pas. Missing data -> flagged "a_completar", never fabricated.
import json, unicodedata, math, sys

TOMTOM = "/Users/admin/Claude/Projects/norte reparos/norte-reparos-couverture-130km-route.json"
OUT_DIR = "/Users/admin/projects/eletricista-urgente/data"

# Barème CANAL par zone (AUTORITAIRE) — deslocação, desde(1h), 2h
ZONE_PRICE = {
    1: {"desloc": 15, "desde": 80,  "h2": 145},
    2: {"desloc": 25, "desde": 90,  "h2": 155},
    3: {"desloc": 35, "desde": 100, "h2": 165},
    4: {"desloc": 45, "desde": 110, "h2": 175},
    5: {"desloc": 55, "desde": 120, "h2": 185},
    6: {"desloc": 65, "desde": 130, "h2": 195},
}

# 34 concelhos AUTORITAIRE: name, district, zone, grille_km. Moimenta = held.
# tomtom_name = override when TomTom file uses a variant spelling.
CONCELHOS = [
    ("Macedo de Cavaleiros", "Bragança",  1, 0,   True,  None),
    ("Mirandela",            "Bragança",  2, 27,  True,  None),
    ("Alfândega da Fé",      "Bragança",  2, 31,  True,  None),
    ("Vila Flor",            "Bragança",  2, 40,  True,  None),
    ("Bragança",             "Bragança",  3, 42,  True,  None),
    ("Valpaços",             "Vila Real", 4, 48,  True,  None),
    ("Mogadouro",            "Bragança",  3, 48,  True,  None),
    ("Vinhais",              "Bragança",  3, 49,  True,  None),
    ("Carrazeda de Ansiães", "Bragança",  2, 51,  True,  None),
    ("Torre de Moncorvo",    "Bragança",  3, 52,  True,  None),
    ("Murça",                "Vila Real", 4, 54,  True,  None),
    ("Vila Nova de Foz Côa", "Guarda",    4, 63,  True,  "Vila Nova de Foz Coa"),
    ("Vimioso",              "Bragança",  3, 64,  True,  None),
    ("Alijó",                "Vila Real", 5, 74,  True,  None),
    ("Chaves",               "Vila Real", 6, 75,  True,  None),
    ("São João da Pesqueira","Viseu",     4, 80,  True,  None),
    ("Sabrosa",              "Vila Real", 5, 82,  True,  None),
    ("Vila Real",            "Vila Real", 5, 86,  True,  None),
    ("Vila Pouca de Aguiar", "Vila Real", 6, 89,  True,  None),
    ("Miranda do Douro",     "Bragança",  4, 92,  True,  None),
    ("Freixo de Espada à Cinta","Bragança",3,94, True,  None),
    ("Penedono",             "Viseu",     6, 98,  True,  None),
    ("Peso da Régua",        "Vila Real", 5, 98,  True,  None),
    ("Boticas",              "Vila Real", 6, 99,  True,  None),
    ("Santa Marta de Penaguião","Vila Real",5,103,True, None),
    ("Tabuaço",              "Viseu",     5, 106, True,  None),
    ("Lamego",               "Viseu",     5, 111, True,  None),
    ("Armamar",              "Viseu",     5, 112, True,  None),
    ("Montalegre",           "Vila Real", 6, 113, True,  None),
    ("Mesão Frio",           "Vila Real", 5, 113, True,  None),
    ("Sernancelhe",          "Viseu",     6, 114, True,  None),
    ("Ribeira de Pena",      "Vila Real", 6, 120, True,  None),
    ("Mondim de Basto",      "Vila Real", 6, 129, True,  None),
    # Moimenta da Beira: TomTom "Moimenta" (village,78.8km) probable AUTRE Moimenta -> HELD
    ("Moimenta da Beira",    "Viseu",     6, None, False, None),
]

def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def slugify(s):
    s = strip_accents(s).lower()
    out = []
    for ch in s:
        if ch.isalnum(): out.append(ch)
        elif ch in ' -_': out.append('-')
    slug = ''.join(out)
    while '--' in slug: slug = slug.replace('--','-')
    return slug.strip('-')

def norm(s):
    return strip_accents(s).lower().strip()

def haversine(a, b):
    (la1, lo1), (la2, lo2) = a, b
    R=6371.0
    p1,p2=math.radians(la1),math.radians(la2)
    dp=math.radians(la2-la1); dl=math.radians(lo2-lo1)
    h=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*R*math.asin(math.sqrt(h))

def main():
    tt = json.load(open(TOMTOM))
    by_norm = {}
    for x in tt:
        by_norm.setdefault(norm(x['name']), x)

    concelhos = []
    seats = {}  # slug -> (lat,lon)
    for name, district, zone, grille_km, indexable, ttname in CONCELHOS:
        slug = slugify(name)
        rec = {
            "name": name, "slug": slug, "district": district, "zone": zone,
            "grille_km": grille_km, "price": ZONE_PRICE[zone],
            "indexable": indexable,
        }
        key = norm(ttname) if ttname else norm(name)
        tt_e = by_norm.get(key)
        if tt_e and tt_e.get('route_km') is not None and tt_e.get('route_min'):
            rec["route_km"] = tt_e["route_km"]
            rec["route_min"] = tt_e["route_min"]
            rec["lat"] = tt_e["lat"]; rec["lon"] = tt_e["lon"]
            seats[slug] = (tt_e["lat"], tt_e["lon"])
            rec["drive_time_status"] = "real_tomtom"
        else:
            rec["route_km"] = None; rec["route_min"] = None
            rec["drive_time_status"] = "a_completar"
        # Macedo hub: 0km origin, route_min plancher -> mark hub
        if slug == "macedo-de-cavaleiros":
            rec["hub"] = True
        concelhos.append(rec)

    # Assign TomTom localities (non-seat) to nearest indexable concelho seat
    seat_items = [(s, c) for s, c in seats.items()]
    localidades = {s: [] for s in seats}
    concelho_norm_names = {norm(c["name"]) for c in concelhos}
    for x in tt:
        t = x.get("type")
        if t == "city":  # skip seats / cities
            continue
        if norm(x["name"]) in concelho_norm_names:
            continue
        lat, lon = x.get("lat"), x.get("lon")
        if lat is None or lon is None:
            continue
        best=None; bestd=1e9
        for s,(sl,so) in seats.items():
            d=haversine((lat,lon),(sl,so))
            if d<bestd: bestd=d; best=s
        if best is not None and bestd <= 25:  # within 25km of a seat = "na zona"
            localidades[best].append({"name": x["name"], "km": round(bestd,1)})
    # sort each list by proximity, cap 30
    for s in localidades:
        localidades[s].sort(key=lambda r: r["km"])
        localidades[s] = localidades[s][:30]

    import os
    os.makedirs(OUT_DIR, exist_ok=True)
    json.dump(concelhos, open(OUT_DIR+"/concelhos.json","w"), ensure_ascii=False, indent=2)
    json.dump(localidades, open(OUT_DIR+"/localidades.json","w"), ensure_ascii=False, indent=2)

    idx=[c for c in concelhos if c["indexable"] and c["drive_time_status"]=="real_tomtom"]
    held=[c for c in concelhos if not c["indexable"] or c["drive_time_status"]!="real_tomtom"]
    print(f"concelhos total: {len(concelhos)}")
    print(f"indexables avec drive-time réel: {len(idx)}")
    print(f"held/a_completar: {[(c['name'],c['drive_time_status'],c['indexable']) for c in held]}")
    print(f"localidades assignées (total): {sum(len(v) for v in localidades.values())}")
    print("sample localidades braganca:", [l['name'] for l in localidades.get('braganca',[])[:8]])

if __name__=="__main__":
    main()
