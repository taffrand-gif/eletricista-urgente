#!/usr/bin/env python3
"""Non-régression : tools/enrich_concelhos.py ne doit réintroduire ni zones, ni priceRange, ni équipement/claims non confirmés, ni garantie chiffrée.
Génère dans un répertoire temporaire (aucune page du dépôt n'est modifiée), 2 passes identiques. Usage: python3 tools/test_enrich_concelhos_gate.py"""
import importlib.util, json, re, shutil, sys, tempfile
from pathlib import Path
REPO = Path(__file__).resolve().parent.parent
FORBID = {
 "zones/ancien prix": r"\bZ[1-6]\b|\+ ?50 ?%|(?<![\d.])(?:65|55|45|35|25|15) ?€|zona tarif|zonas-deslocacao",
 "TomTom/OSRM/route_km publics": r"(?i)tomtom|osrm|route_km",
 "ROLeak/Ridgid/plomberie": r"(?i)roleak|ridgid|desentup",
 "Megger/Analisador": r"(?i)megger|MFT ?1741|analisador de circuito",
 "Fluke modèle/spec": r"(?i)fluke[ \-]?(?:87v|1587|t6)|multímetro fluke|43 ?200",
 "priceRange": r"priceRange",
 "garantie chiffrée": r"(?i)garantia\s+(?:de\s+)?\d+\s*(?:anos?|meses)|\d+\s*anos? de garantia",
 "délai chiffré": r"(?i)~\s*\d+\s*min|minutos publicados|chegamos em",
 "gratuité": r"(?i)sem compromisso|gr[aá]tis|gratuit",
}
def run(tmp):
    spec = importlib.util.spec_from_file_location("enrich", REPO / "tools" / "enrich_concelhos.py"); m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    (tmp / "data").mkdir(); (tmp / "concelhos").mkdir()
    shutil.copy(REPO / "data" / "concelhos.json", tmp / "data"); shutil.copy(REPO / "data" / "localidades.json", tmp / "data")
    for f in (REPO / "concelhos").glob("*.html"): shutil.copy(f, tmp / "concelhos")
    m.ROOT = tmp; m.CONCELHOS_DIR = tmp / "concelhos"; m.DATA = tmp / "data" / "concelhos.json"; m.main()
    return {p.name: p.read_text(encoding="utf-8") for p in sorted((tmp / "concelhos").glob("*.html"))}
def main():
    with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
        p1 = run(Path(a)); p2 = run(Path(b)); bad = 0
        if p1 != p2: print("FAIL: 2e génération différente"); bad += 1
        for name, t in p1.items():
            for k, rx in FORBID.items():
                if re.search(rx, t): print(f"FAIL {name}: {k}"); bad += 1
            for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
                try: json.loads(blk)
                except Exception: print(f"FAIL {name}: JSON-LD invalide"); bad += 1
            if not all(x in t for x in ("70", "100")) or "tel:" not in t: print(f"FAIL {name}: grille/tel absents"); bad += 1
        print(f"{len(p1)} pages générées, {bad} échec(s)"); return 1 if bad else 0
if __name__ == "__main__": sys.exit(main())
