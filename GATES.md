# GATES. EU coverage deletion 2026-11-25

BASE: origin/main
POPULATION: 17 HTML files explicitly authorized for deletion
SCOPE: confirmed Spain, Moimenta/Tavira/Viseu hors couverture, excluding Vila Verde da Raia (Chaves) and Vila Nova da Rainha (Macedo de Cavaleiros)
EXCLUDED: Chaves, ValpaMdos, reserved CNR PAA pages, all other files
INVARIANTS: no sitemap or generator edits in this deletion step; no production; no merge
CHECKS: exact manifest, git diff --check, deleted paths only, generators inspected before PR
STATUS: pending validation

## Intégration SEO/GEO/AEO 2026-11-27
BASE_EFFECTIVE: 8b71a5afb
OBJECTIF: conserver la population géographique prouvée et appliquer la présentation neutre du prototype EU.
POPULATION_SUPPLÉMENTAIRE: 1 fichier source du commit 7b92af3e3, plus ce gate.
INVARIANTS: Chaves et Vila Nova da Rainha conservées ; DGEG/TRIESP uniquement EU et exacts ; aucune adresse privée ni promesse non sourcée ; téléphone/WhatsApp conservés.
SOURCE: _governance/20-BUSINESS-FACTS.json ; index.html ; sitemaps/routes du commit de base.
PREUVES: manifest exact, scan des fichiers présents, JSON-LD parseable, canonical, CTA, sitemap/XML, git diff --check, régénération contrôlée.
STATUT: PARTIEL — intégration non rejouée ; aucun merge, Ready ou Production.

## STOP générateur EU — 2026-11-27
- Commande : `python3 scripts/build_sitemap_full.py https://eletricista-urgente.pt`
- Résultat source : 1 896 HTML racine + 33 concelhos + 5 distritos = 1 934 URLs.
- Sitemap curaté de base : 903 URLs.
- Comparaison mécanique : 1 874 ajouts, 843 retraits ; exemple d’ajout non arbitré : `/blog` et `/design-preview-eu` ; les retraits sont principalement les URLs blog curatées de base.
- Décision : sortie brute restaurée et non commitée ; aucun sitemap ne doit être remplacé sans arbitrage de la population et contrôle des routes.
- Statut : BLOCKED sur régénération EU ; intégration SEO/GEO/AEO reste PARTIELLE ; merge/Production interdits dans ce lot.
