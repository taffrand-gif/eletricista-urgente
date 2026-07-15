# PRICING — Source de vérité prix Norte Reparos
> Verrouillé Filipe · À copier dans CHAQUE repo (`PRICING.md`) avec `precos-zonas.json`.
> JAMAIS inventer un prix/zone/délai. Tout chiffre € vient d'ici ou de `precos-zonas.json`.

## Main-d'œuvre (par heure)
- **Canalização (plomberie) : 65 €/h**
- **Eletricidade : 70 €/h**

## Déplacement — par ZONE (par localité, pas par concelho)
Zone = **distance ROUTE réelle** (km/temps de conduite via OSRM) depuis Macedo de Cavaleiros (sede operacional). ⚠️ **PAS à vol d'oiseau** — c'est la distance routière effective. Z1 = plus proche → Z6 = plus loin (~130 km route max).

| Zone | Déplacement |
|------|-------------|
| Z1 | 15 € |
| Z2 | 25 € |
| Z3 | 35 € |
| Z4 | 45 € |
| Z5 | 55 € |
| Z6 | 65 € |

**Mapping localité → zone** = `precos-zonas.json` (960 localités, dans ce repo). Lookup obligatoire, jamais deviner.
Exemple : `Freixo de Espada à Cinta` = Z5 = 55 €.

## Majoration
- **+50 %** nuit / week-end / feriado — s'applique à la main-d'œuvre ET au déplacement.

## Règle de communication (doctrine)
- Toujours : **"orçamento por escrito antes de qualquer intervenção, sem surpresas na fatura"**.
- Hors grille / cas variable (ex : installation, wallbox N/A) : **"sob orçamento"**, jamais une fourchette inventée.
- Bloc Transparence prix placé HAUT de page (grille + majoration + phrase orçamento).

## NAP (public, jamais masquer)
- Canal : `+351 928 484 451` · Élec : `+351 932 321 892`.
- Machine : schema.telephone = E.164 `+351928484451` / `+351932321892` ; href = `tel:+351928484451`. JAMAIS de masque `****`.

## Source amont
Méthodologie zones : `ObsidianVault/NORTE-OS/Methodologie/ZONE-COUVERTURE-PT-130KM-2026-06-24.md` (OSRM, prime sur toute vieille grille). Data : `norte-os-marketing/prototypes/zonas-data.json`.
