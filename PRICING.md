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

## Prestations documentaires (électricité — DGEG)
- **Emissão de ficha eletrotécnica e termo de responsabilidade : a partir de 250 €**
  - **Un seul prix plancher couvrant les DEUX documents** (formulation Filipe : « ficha electrotec **et/ou** termos de responsabilidade »). Ne JAMAIS publier deux lignes distinctes : lu comme 250 € chacune, soit 500 € — faux et pénalisant.
  - Écrire « a partir de » : c'est un plancher, pas un tarif fixe. Aucune fourchette haute ne doit être inventée.
  - Distinct de la main-d'œuvre (70 €/h) et du déplacement par zone : prestation documentaire, pas une heure de travail.
  - Adossé à la credencial **DGEG TRIESP n.º 90062** (baixa tensão até 41,4 kVA). Sites **ÉLECTRICITÉ uniquement** — jamais sur les repos plomberie.
  - Source : Filipe, 2026-08-10 (donnée métier qu'il est seul à détenir, absente de toute source avant cette date).

## Majoration
- **+50 %** nuit / week-end / feriado — s'applique à la main-d'œuvre ET au déplacement.

## Règle de communication (doctrine) — V2 2026-08-11

Quatre engagements à publier (Filipe, 11/08) :

1. **Estimativa sem custo por telefone ou WhatsApp quando fotos/vídeo permitem chiffrer**.
2. **Orcamento por escrito antes de qualquer intervencao**.
3. **A deslocacao tem preco tabelado por zona (Z1-Z6)** — voir tableau ci-dessus.
4. **Confirmamos sempre consigo o trabalho e o preco antes de faturar seja o que for**.

### Formulation bannie (R-canon-2026-08-11)

- ❌ **JAMAIS** « orçamento gratuito » : la deslocacao est facturée, ce qui crée une fausse promesse.
- ❌ **JAMAIS** « visita gratuita » : la visite technique est couplée à la deslocacao facturée.
- ❌ **JAMAIS** « deslocacao gratuita » : la deslocacao a un prix tabelado par zone (Z1-Z6).
- ✅ La formulation correcte met l'accent sur **estimativa sem custo** (pas de frais pour chiffrer par téléphone/WhatsApp si photos/vidéo permettent) et sur l'**engagement écrit avant intervention**.

### Hors grille / cas variable

- Cas variable (ex : installation, wallbox, certificação DGEG) : **"sob orçamento"**, jamais une fourchette inventée.
- Bloc Transparence prix placé HAUT de page (grille + majoration + 4 engagements ci-dessus).

## NAP (public, jamais masquer)
- Canal : `+351 928 484 451` · Élec : `+351 932 321 892`.
- Machine : schema.telephone = E.164 `+351928484451` / `+351932321892` ; href = `tel:+351928484451`. JAMAIS de masque `****`.

## Source amont
Méthodologie zones : `ObsidianVault/NORTE-OS/Methodologie/ZONE-COUVERTURE-PT-130KM-2026-06-24.md` (OSRM, prime sur toute vieille grille). Data : `norte-os-marketing/prototypes/zonas-data.json`.
