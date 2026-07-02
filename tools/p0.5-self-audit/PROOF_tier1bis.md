AVANT tier-1-bis (re-run self-audit 02/07 22:50, Python 3.9 fix from __future__ import annotations):
  KO2ter_body_vs_badge : 173   (CU 32, CNR 27, EU 35, ENR 79)
  KO2ter_zone_attendue : 92    (CU 23, CNR 19, EU 23, ENR 27)
  Total KO2ter tier 1  : 265
  KO1_badge_zona       : 253
  KO2_jsonld_zone      : 323
  KO2bis               : 11
  KO3_prix_body        : 653
  KO4_delai            : 214
  KO2ter_body_seul     : 2693   (NO_RESOL, tier 3)
  html_total           : 13113

PATCHER P0.5C-tier1bis (apply_vague.py) :
  + RE_BODY_DESLOCACAO_ZONE_ONLY : 'Deslocação Zona N' sans prix requis (div.price-item)
  + RE_BODY_ZONE_BARE : 'Zona N' orphelin (FAQ, sous-titres)
  + Step 4 : align prix 'Zona N: P€' sur GRILLE[N]
  + Step 5 (KO1_coupling) : align data-zone sur target (ferme KO1+KO2ter couplés)
  + Bugfix : new = new_body écrasait badge patché → restauré

VAGUE tier-1-bis (4 repos, 2 passes) :
  Passe 1 (173 body_vs_badge + 92 zone_attendue) : 173/173 patches
  Passe 2 (73 KO2ter restants = KO1+KO2ter couplés) : 73/73 patches
  Total fichiers patchés : 246 (253 - 7 fichiers en double)

APRÈS tier-1-bis (re-run self-audit 02/07 23:XX) :
  KO2ter_body_vs_badge : 0     ✓
  KO2ter_zone_attendue : 0     ✓
  KO1_badge_zona       : 180   (-73 cascade)
  KO2_jsonld_zone      : 323
  KO2bis               : 11
  KO3_prix_body        : 653
  KO4_delai            : 214
  KO2ter_body_seul     : 2693

TEMOINS R8 (re-run après vague) :
  Vinhais Z3 (CU/CNR/EU/ENR)         : resolved, 0 KO
  Macedo de Cavaleiros Z1 (4 repos)  : resolved, 0 KO
  Bragança Z2 (CU canalizador/EU)    : resolved, KO1_badge_zona (KO1, tier 2 — hub page)
