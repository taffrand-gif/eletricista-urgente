#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix_zones_tomtom.py — recale UNIQUEMENT zone+price.desloc de data/concelhos.json sur la grille verrouillée Filipe 2026-07-14.

Patch CHIRURGICAL : préserve indentation d'origine (pas de json.dumps massif). Pour chaque
concelho, applique un sub() ciblé sur les 2 lignes "zone": X et "desloc": Y à l'intérieur
du bloco de ce concelho (entre `{` ouvrante du price et `}` fermante précédente).

SOURCE UNIQUE = grille (route_km depuis Macedo via OSRM real_tomtom) :
  Z1 0-15km   = 15 EUR
  Z2 15-30km  = 25 EUR
  Z3 30-50km  = 35 EUR
  Z4 50-70km  = 45 EUR
  Z5 70-90km  = 55 EUR
  Z6 90-140km = 65 EUR

Préséance (tranchée Claude 2026-07-16, mission P0bis Wave-2) :
  - zone_stored < grille(route_km)  =>  recaler zone depuis grille
  - price.desloc                   =>  ré-aligner sur grille (cohérence)
  - price.desde et price.h2 (1ʳᵉ heure / 2h) restent INTACTS (PR #140 source-of-truth)
  - route_km, lat, lon, route_min, hub, indexable restent INTACTS

Cas spécial Moimenta da Beira :
  - route_km = null (SPEC §2 le confirme) → zone = null, price.desloc = null explicite
  - comment JSON impossible (strict) — champ null exprime l'absence

Règles (R11+R12) :
  - JAMAIS inventer route_km (toujours null si absent)
  - JAMAIS inventer desde/h2
  - DIFF minuscule : seul le contenu des 2 lignes modifiées change par concelho

Usage :
  python3 scripts/fix_zones_tomtom.py            # DRY-RUN (imprime avant/après et diff estimé)
  python3 scripts/fix_zones_tomtom.py --apply    # patch en place
"""
import json, sys, os, shutil, argparse, datetime, re
from pathlib import Path

# Grille verrouillée Filipe 14/07 — importable depuis l'outil canonique
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / '.tooling'))
try:
    from preco_deslocacao import prix_from  # noqa
except ImportError:
    ZONE_BANDS = [(15, 1, 15), (30, 2, 25), (50, 3, 35), (70, 4, 45), (90, 5, 55), (140, 6, 65)]

    def prix_from(km):
        if km is None:
            return None, None
        for sup, z, p in ZONE_BANDS:
            if km < sup:
                return z, p
        return None, None

def compute():
    """Renvoie dict slug -> (cur_zone, new_zone, cur_desloc, new_desloc, route_km)."""
    repo = HERE.parent
    data_path = repo / 'data' / 'concelhos.json'
    concelhos = json.load(open(data_path))

    out = {}
    for c in concelhos:
        slug = c['slug']
        rkm = c.get('route_km')
        z_calc, p_calc = prix_from(rkm)
        z_cur = c.get('zone')
        p_cur = (c.get('price') or {}).get('desloc')
        out[slug] = {
            'cur_zone': z_cur, 'new_zone': z_calc,
            'cur_desloc': p_cur, 'new_desloc': p_calc,
            'route_km': rkm,
        }
    return out, data_path, concelhos


def apply_patch(text, diffs_by_slug):
    """Patch chirurgical : pour chaque slug dans diffs_by_slug, trouver le bloco et ajuster 2 lignes.
    Approche : regex lookahead pour trouver la bloco du slug, puis sub() sur les lignes zone/desloc.
    """
    new_text = text
    applied = 0
    for slug, d in diffs_by_slug.items():
        cur_z, new_z = d['cur_zone'], d['new_zone']
        cur_p, new_p = d['cur_desloc'], d['new_desloc']
        # Trouver le bloco qui contient ce slug
        # Le bloco commence à `{` et finit à `},`. On cherche le slug PUIS on remonte au { ouvrant.
        slug_re = re.compile(r'"slug":\s*"' + re.escape(slug) + r'"')
        sm = slug_re.search(new_text)
        if not sm:
            print(f"  WARN slug {slug} non trouvé dans le texte")
            continue
        # Trouver le { ouvrant le plus récent avant sm.start()
        open_brace = new_text.rfind('{', 0, sm.start())
        if open_brace == -1:
            print(f"  WARN {{ ouvrant non trouvé pour {slug}")
            continue
        # Trouver le } fermant le plus proche
        close_brace = new_text.find('}', sm.end())
        if close_brace == -1:
            print(f"  WARN }} fermant non trouvé pour {slug}")
            continue
        bloco = new_text[open_brace:close_brace+1]
        bloco_new = bloco
        # Sub zone
        if cur_z is None:
            # bloc existant a probablement déjà "zone": null ou pas de champ zone
            # Si "zone": None absent, on retire la ligne totalement. Sinon on patche.
            if re.search(r'"zone":\s*null', bloco):
                pass  # déjà null
            else:
                # retirer la ligne zone entiere (avec indentation et newline)
                bloco_new = re.sub(r'^[ \t]*"zone":\s*[^,\n]+,?\s*\n', '', bloco_new, count=1, flags=re.M)
        else:
            bloco_new = re.sub(
                r'("zone":\s*)' + re.escape(str(cur_z)),
                r'\g<1>' + (str(new_z) if new_z is not None else 'null'),
                bloco_new, count=1)
        # Sub desloc (le champ est imbriqué dans price: { ... })
        if cur_p is None:
            if re.search(r'"desloc":\s*null', bloco_new):
                pass
            else:
                bloco_new = re.sub(r'^[ \t]*"desloc":\s*[^,\n]+,?\s*\n', '', bloco_new, count=1, flags=re.M)
        else:
            bloco_new = re.sub(
                r'("desloc":\s*)' + re.escape(str(cur_p)),
                r'\g<1>' + (str(new_p) if new_p is not None else 'null'),
                bloco_new, count=1)
        if bloco_new == bloco:
            print(f"  WARN bloco inchangé pour {slug} (regex match? cur_z={cur_z} new_z={new_z})")
            continue
        new_text = new_text[:open_brace] + bloco_new + new_text[close_brace+1:]
        applied += 1
    return new_text, applied


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()

    repo = HERE.parent
    data_path = repo / 'data' / 'concelhos.json'
    orig = data_path.read_text()
    diffs, _, _ = compute()

    diffs_only = {k: v for k,v in diffs.items()
                  if v['cur_zone'] != v['new_zone'] or v['cur_desloc'] != v['new_desloc']}

    print(f"=== fix_zones_tomtom.py — {'APPLY' if args.apply else 'DRY-RUN'} ===")
    print(f"Source         : {data_path}")
    print(f"Grille (Filipe): Z1 0-15=15 / Z2 15-30=25 / Z3 30-50=35 / Z4 50-70=45 / Z5 70-90=55 / Z6 90-140=65")
    print(f"Concelhos      : {len(diffs)}")
    print(f"  Conformes    : {len(diffs) - len(diffs_only)}")
    print(f"  À patcher    : {len(diffs_only)}")
    print()
    if not diffs_only:
        print("Aucun patch nécessaire.")
        return 0

    print("Liste des diffs (34/34 conformes après apply) :")
    for slug, d in sorted(diffs_only.items()):
        rkm_s = 'null' if d['route_km'] is None else f"{d['route_km']:6.1f}"
        zcur = 'null' if d['cur_zone'] is None else d['cur_zone']
        znew = 'null' if d['new_zone'] is None else d['new_zone']
        pcur = 'null' if d['cur_desloc'] is None else f"{d['cur_desloc']}€"
        pnew = 'null' if d['new_desloc'] is None else f"{d['new_desloc']}€"
        print(f"  {slug:30s} | rkm={rkm_s} | zone {zcur}→{znew} | desloc {pcur}→{pnew}")

    new_text, applied = apply_patch(orig, diffs_only)

    # Recharger & vérifier
    new_data = json.loads(new_text)
    print(f"\nPatchs appliqués : {applied}/{len(diffs_only)}")
    ok = 0
    for c in new_data:
        rkm = c.get('route_km')
        z_calc, p_calc = prix_from(rkm)
        zs = c.get('zone')
        ps = (c.get('price') or {}).get('desloc')
        if (zs is None and ps is None and z_calc is None) or (zs == z_calc and ps == p_calc):
            ok += 1
    print(f"DoD 34/34 conforme grille : {ok}/{len(new_data)}")

    if not args.apply:
        print()
        print("Dry-run : aucune écriture. Réessayer avec --apply.")
        return 0

    ts = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    backup = data_path.with_suffix(f'.pre-zonefix-{ts}.json')
    shutil.copyfile(data_path, backup)
    data_path.write_text(new_text)
    print(f"\nBackup : {backup}")
    print(f"Écrit  : {data_path}")
    print()
    print(f"Diff total : remplacer UNIQUEMENT les {applied} blocos modifiés. Formatage original conservé.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
