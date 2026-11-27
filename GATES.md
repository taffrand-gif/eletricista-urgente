# GATES. EU coverage deletion 2026-11-25

BASE: origin/main
POPULATION: 17 HTML files explicitly authorized for deletion
SCOPE: confirmed Spain, Moimenta/Tavira/Viseu hors couverture, excluding Vila Verde da Raia (Chaves) and Vila Nova da Rainha (Macedo de Cavaleiros)
EXCLUDED: Chaves, ValpaMdos, reserved CNR PAA pages, all other files
INVARIANTS: no sitemap or generator edits in this deletion step; no production; no merge
CHECKS: exact manifest, git diff --check, deleted paths only, generators inspected before PR
STATUS: pending validation


---

# GATES — Pilote SEO/GEO EU avaria elétrica

## Périmètre

- Dépôt : `taffrand-gif/eletricista-urgente`
- Worktree : `/Users/admin/work/Sites/_worktrees/seo-pilot-eu-avaria-20261126`
- Branche : `seo/pilot-eu-avaria-20261126`
- Base : `origin/main` / `a1af0d30e0978f63698b62896308c922c6537711`
- Page témoin unique : `index.html` → `https://eletricista-urgente.pt/`
- Intention : avaria elétrica urgente, avec symptômes curto-circuito / disjuntor
- Hors périmètre : pages locales `eletricista-avaria-eletrica-*`, `curto-circuito.html`, pages `quadro/disjuntor`, articles de blog, générateurs de masse, production, merge et passage Ready.

## Arbitrage

La homepage est retenue parce qu’elle est la page canonique commerciale de l’intention générale : canonical `/`, H1 « avarias e curto-circuitos », CTA téléphone/WhatsApp, et entrée prioritaire du `sitemap.xml`. Les pages locales, spécialisées et informationnelles conservent leurs intentions propres.

## Invariants métier

- PT-PT uniquement.
- Téléphone EU : `+351 932 321 892`.
- Tarif jour : `70 €/h` + `30 €` de déplacement, jours ouvrables 09:00–18:00.
- Tarif nuit/week-end/jour férié : `100 €/h` + `50 €` de déplacement.
- Valeurs TTC, devis écrit avant intervention.
- Aucun prix par zone, aucune zone Z1–Z6.
- Équipements électriques autorisés : Fluke, FLIR E96/câmara térmica ; détecteur d’humidité seulement si pertinent. Aucun équipement plomberie ni capacité non prouvée.
- Statut autorisé : « Eletricista credenciado pela DGEG — Técnico Responsável de Instalações Elétricas, TRIESP n.º 90062. Execução em Baixa Tensão até 41,4 kVA. »
- Ficha/Termos : « a partir de 350 € TTC, sob orçamento conforme o caso » seulement si pertinent ; pas de prix dans JSON-LD.
- Pas de promesse de délai d’arrivée, avis, chantier, résultat, garantie ou assurance non sourcée.
- CTA `tel:` et WhatsApp doivent rester présents.

## Modifications attendues

1. Réponse directe citable en haut pour avaria elétrica / curto-circuito / disjuntor.
2. Symptômes et consigne de sécurité sans instruction risquée.
3. Équipement présenté par usage réel et uniquement autorisé.
4. Bloc DGEG/TR​​IESP conforme au wording central.
5. Suppression des formulations interdites repérées dans le témoin.
6. Aucun changement de sitemap attendu : l’URL `/` doit rester présente une seule fois.

## Contrôles reproductibles

- `git diff --check`
- Vérification déterministe title, canonical, H1 unique, téléphone, WhatsApp et URL canonique.
- Parsing de tous les blocs JSON-LD avec Python `json.loads`.
- Vérification des invariants tarifaires et absence des claims interdits dans `index.html`.
- Vérification sitemap : URL racine présente exactement une fois.
- Contrôle artefact statique : `index.html` lisible et balises essentielles fermées ; pas de build applicatif attendu (site HTML statique).
- `python3 ~/agents/done-gate/done-gate.py` si compatible avec ce lot.
- Preview/DOM/HTTP public : à exécuter si la Preview est accessible ; sinon statut explicitement `NON VÉRIFIÉ`.

## État initial

- Avant code : `PASS_SOURCE` sur la sélection de page et la base Git.
- Production : inchangée.
- Merge/Ready : interdits sans GO explicite nommé de Filipe.

## Statut final attendu

`PARTIEL / PASS_SOURCE` au minimum ; `PASS_BUILD` si les contrôles locaux passent ; Preview/DOM/Production listés séparément et jamais déduits d’un contrôle source.

FINI = [commande][population][commit][source][niveau][production][exceptions]
