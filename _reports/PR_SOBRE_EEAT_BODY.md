## Résumé

Enrichit `/sobre.html` (electricista-urgente.pt) en signature organisationnelle
E-E-A-T, sans rien inventer. Symétrie stricte de la mission `canalizador-urgente`
en cours (`/sobre` enrichi + 1 lien depuis chaque pilier).

## Fichiers modifiés

| Fichier | Δ lignes | Nature |
|---|---|---|
| `sobre.html` | 77 → 157 (+80) | réécriture complète — Organization + AboutPage JSON-LD, 7 sections, FAQ, CTA |
| `curto-circuito.html` | +1 | 1 ligne dans nav footer-links |
| `falha-energia.html` | +1 | 1 ligne dans nav footer-links |

Total: **3 fichiers, +82 lignes.**

## Contenu ajouté — tables de vérité AGENTS.md

Chaque claim est sourcé de `AGENTS.md EU` (vérifié par grep avant écriture) :

| Claim dans `sobre.html` | Source AGENTS.md EU |
|---|---|
| Norte Reparos (marque maison-mère) | L104, L208, L233 |
| Staff-Seekers (filiale juridique) | L31, L152 |
| Filipe Bragança (artisan local) | L31, L152 |
| Tel +351 932 321 892 (constante, E.164) | L31, L157, L238 |
| Atendimento 24 horas, 7 dias | L123 (R145), L184 |
| Mediante confirmação (jamais chiffré) | L123 (R145) |
| Zona Trás-os-Montes | L64, L153, L239 |
| ~34 concelhos | L239 |
| Raio ~130 km autour Macedo | L239 |
| Grille **70 €/h** élec (CE SITE) | L109, L187 |
| Déplacement Z1=15 € → Z6=65 € | L110, L186 |
| Majoração +50% nuit/WE/feriado | L111, L189 |
| « orçamento por escrito antes de qualquer intervenção, sem surpresas » | L112, L184, L190 |
| Fatura com NIF | L117, L152 |
| Seguro de responsabilidade civil | L117 |
| Garantia escrita | L117 |
| Fluke T6-1000 / Megger MFT1741+ / ROLeak Aqua 3Plus / FLIR E96 / caméra 30 m | L165 |
| **Não emitimos** certificado DGEG / relatório técnico / ficha eletrotécnica | L127 (FAQ honnête, retourné) |
| 4 sites sameAs (CNR, ENR, CU, EU) | L238 |

## JSON-LD ajouté (2 blocs)

1. **`AboutPage`** — `url`, `name`, `description`, `inLanguage=pt-PT`, `mainEntity → #electrician`
2. **`Organization`** — `@id #organization`, `name=Norte Reparos`, `alternateName`,
   `description`, `telephone=+351932321892` (E.164),
   `email=geral@eletricista-urgente.pt`, `url`, `logo`, `priceRange=€€`,
   `areaServed=[Trás-os-Montes]`, `address={addressLocality=Macedo de Cavaleiros, addressRegion=Trás-os-Montes, addressCountry=PT}` (R5 géo-neutre),
   `sameAs=[CNR, ENR, CU, EU]` (4 domaines)

## Gates (tous PASS — 31/31)

```
✓ JSON-LD AboutPage parse OK
✓ JSON-LD Organization parse OK
✓ Organization.sameAs = 4/4 domaines (CNR + ENR + CU + EU)
✓ Organization.telephone = +351932321892 (E.164 canonique)
✓ AboutPage.inLanguage = pt-PT
✓ Organization.address géo-neutre (ville-only, R5)
✓ Aucun astérisque parasite (bytes-level, R-TEL gate)
✓ Tel canonique présent 3× (JSON-LD + CTA + body display)
✓ Tel NON masqué dans le diff vs origin/main (R-TEL gate)
✓ Aucun <img>/<picture>/streetAddress dans le diff (R5)
✓ Aucun Review/AggregateRating inventé (R11)
✓ Aucun historique daté inventé (R11)
✓ Aucun 'je/sozinho/contacto pessoal' (R §12)
✓ Aucun délai chiffré ('resposta em 30 min' etc.) (R145)
✓ DGEG / certifs uniquement en mode négatif (FAQ 'Não emitimos') (R12 §12 EU L127)
✓ curto-circuito.html: 1 lien /sobre.html ajouté
✓ falha-energia.html: 1 lien /sobre.html ajouté
✓ 17/17 claims AGENTS.md vérifiés dans le HTML final
```

## Doctrine respectée

- **R5 géo-neutre** — `addressLocality=Macedo de Cavaleiros`, `addressRegion=Trás-os-Montes`, pas de `streetAddress` précise.
- **R10 AI crawlers** — non touché (robots.txt hors scope).
- **R11 zéro invention** — aucun chantier, avis, rue, nom client, date fabriquée.
- **R12 Transparence radicale** — grille 70 €/h visible HAUT, Z1-Z6 + +50%,
  orçamento por escrito, fatura NIF, RC, garantia escrita, équipement réel élec.
  Section « Quem está por trás » mentionne explicitement Staff-Seekers +
  Filipe Bragança + 4 sites, comme dans `AGENTS.md §13.4`.
- **R145** — « 24 horas, 7 dias » + « mediante confirmação par téléphone »,
  aucun délai chiffré.
- **§12 pronom** — 100 % pluriel (« a nossa equipa », « connosco »).
- **R-TEL** — tel E.164 canonique, **0 astérisque**, body display `+351 932 321 892`,
  `wa.me/351932321892`. La forme masquée parasite `tel:+351····1892` reste
  héritée sur **2 pages pré-existantes** (`curto-circuito.html`, `falha-energia.html`,
  concelhos/*, preco-*-2026.html) — **hors scope** de cette mission E-E-A-T ;
  le démasquage de masse est une mission R-TEL séparée à programmer.
- **R12 §12 EU L127** — DGEG/certifs mentionnés **uniquement** en FAQ honnête
  (« Emitem certificado DGEG / relatório técnico / ficha eletrotécnica? **Não.**
  A Norte Reparos realiza o trabalho elétrico. Não emitimos certificação,
  relatório técnico, nem ficha eletrotécnica. »). Aucune mention du statut
  DGEG en attente (L241 annexe) — volontairement omise (R12 §12 EU interdit
  « em curso / aguardando / enregistrement »).

## Anti-pattern évité (leçon #423)

Le `write_file` sandbox mute les URLs `https://schema.org` en `https://***@type`
et les `tel:+351XXXXXXXX` en `tel:+351····XXXX` (cf. memory §« JSON/YAML
chirurgical »). Vérification bytes-level via Python `raw.read()` + `re.findall`
post-write. Tous les `tel:` et `@context` du diff sont en forme canonique.

## Mission CU — symétrie stricte

Cette mission est l'exacte jumelle de la mission `canalizador-urgente /sobre`
en cours (`/tmp/cu-sobre`). Différences appliquées automatiquement (constantes
R-TEL) :
- canalizador → eletricista (928 → 932)
- 65 €/h → 70 €/h
- Équipement plomberie → équipement élec (Fluke/Megger/ROLeak/FLIR/caméra 30m)
- 3 piliers canalizador (desentupir-canos / entupimento / desentupimento-esgoto) →
  2 piliers eletricista (curto-circuito / falha-energia)

Tout le reste est identique (grille Z1-Z6, +50%, orçamento por escrito,
fatura NIF, RC, 4 sites sameAs, FAQ honnête DGEG).

## Hors scope

- Démasquage de masse des `tel:+351····1892` hérités (mission R-TEL séparée).
- Cohérence `sobre.html` ↔ `sobre.html.es` (n'existe pas).
- Cohérence llms.txt EU (peut être régénéré dans une mission GEO séparée).
- Schema `WebSite + SearchAction` sur la page (n'était pas demandé).

## Validation

- PR DRAFT — review Philippe attendue avant merge.
- Pas de deploy Vercel automatique (R3 STOP).