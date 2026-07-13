# P0 Résurrection blog urgente — Rapport de gate

Date : 2026-07-13
Tâche Kanban : `t_8bd2beb1`
Repo : `eletricista-urgente`
Branche isolée : `feat/eu-blog-md-resurrection`

## Verdict

**BLOQUÉ — 0 page publiée.**

Le brief affirmait que les 58 sources Markdown étaient « R12-OK ». Le dry-run exhaustif du renderer réfute ce point : **58/58 sources sont refusées** par au moins une règle d’`AGENTS.md`. Les convertir mécaniquement rendrait publiques 58 pages non conformes.

Conséquence volontaire :

- HTML générés depuis les 58 sources : **0**
- Sitemap modifié : **non**
- Push / PR / merge / déploiement : **aucun**
- Curl live 200 : **non applicable**, puisque la publication a été bloquée avant effet prod

## Inventaire structurel

```json
{
  "md_count": 58,
  "existing_html_targets": 0,
  "source_location": "blog/",
  "served_html_locations": {
    "blog": 25,
    "public/blog": 42
  }
}
```

Le repo statique sert directement la racine (`vercel.json: outputDirectory="."`, `cleanUrls=true`). Pour ce corpus, la cible correcte après validation serait donc `blog/<slug>.html`; aucun miroir `client/public/blog` n’existe.

## Renderer livré sur la branche

`scripts/render-blog-md.js` :

- parse le frontmatter et le Markdown sans dépendance npm ;
- impose un H1 cohérent avec le title ;
- impose une réponse directe de 40 à 60 mots ;
- rend tableaux, listes, liens, emphase et code ;
- injecte le tarif canonique **70 €/h**, Z1–Z6, +50 %, la phrase d’orçamento et le bloc anti-call-center ;
- ajoute CTA téléphone/WhatsApp sticky ;
- ajoute `EmergencyService`, `Service`, `FAQPage`, `BlogPosting`, et `HowTo` quand des étapes sont détectées ;
- ajoute un bloc E-E-A-T honnête, vide de tout chantier inventé ;
- refuse atomiquement tout corpus qui contient une violation : aucune écriture partielle ;
- limite un batch à 95 sources (R15).

Tests : `tests/test-render-blog-md.js` + deux fixtures.

## Preuve tests

Commande :

```bash
node --check scripts/render-blog-md.js
node --check tests/test-render-blog-md.js
node tests/test-render-blog-md.js
```

Sortie :

```text
render-blog-md tests: PASS
```

Le test couvre : rendu HTML, réponse 40–60 mots, prix/NAP, JSON-LD parseable, HowTo, FAQ, Markdown, dry-run, rejet atomique d’une source non conforme et rejet d’un title/H1 hors métier.

## Gate exhaustif des 58 sources

Commande :

```bash
node scripts/render-blog-md.js --source blog --out-dir blog --dry-run
```

Sortie synthétique :

```text
CONFORMITY BLOCK: 58/58 source(s) refusée(s)
exit code: 2
```

Nombre de fichiers affectés par catégorie (une source peut apparaître dans plusieurs catégories) :

| Catégorie | Fichiers |
|---|---:|
| Prix/fourchette non sourcé | 52 |
| Délai de réponse chiffré | 34 |
| Pronom client interdit | 31 |
| Document/certification émis | 30 |
| Statistique terrain non sourcée | 20 |
| Promesse R145 | 20 |
| Ancienneté/volume non vérifié | 18 |
| Contenu plomberie hors métier | 8 |
| Témoignage ou exemple inventé | 5 |
| NAP plomberie/placeholder téléphone | 3 |
| Service interdit | 2 |
| PT-BR | 1 |

Exemples bloquants constatés :

- `blog/canalizador-braganca-guia-completo.md`, `canalizador-macedo-cavaleiros-sede-operacional.md`, `canalizador-mirandela-solucoes-locais.md` : plomberie + NAP **928 484 451** dans le repo électricité ;
- `blog/eletricista-24-horas-guia-completo.md` : délais chiffrés, exemples prétendument réels, faux témoignages, prix divergents et claims de performance ;
- `blog/certificacao-eletrica-obrigatoria-quando-como.md` et `blog/preco-certificacao-certiel-2026.md` : émission de certificat/fiches/documents contraire au ruling Filipe du 08/07 ;
- `blog/tomada-faisca-perigo.md` : « Dados de 500+ Intervenções », pourcentages terrain, délais et document émis non sourcés ;
- `blog/alarme-incendio-obrigatorio.md` : PT-BR, prix et ancienneté non vérifiés.

## Grille technique + conformité

| Technique | Conformité |
|---|---|
| ✅ Renderer syntaxiquement valide | ❌ 58/58 sources refusées |
| ✅ Tests automatisés PASS | ❌ Prototype réel du corpus non validable sans réécriture |
| ✅ Structure source/serveur identifiée | ✅ Aucune page non conforme créée |
| ✅ Écriture atomique et dry-run | ✅ Aucun sitemap/deploy touché |

Verdict global selon R9 : **REFUSÉ** tant que la colonne conformité n’est pas verte.

## Décision requise

Deux voies honnêtes :

1. **Réécriture éditoriale conforme** : choisir un article pilote réel, le nettoyer intégralement depuis les sources de vérité, faire valider son diff, puis traiter le reste en lots ≤95 avec le gate ;
2. **Abandon de ce corpus** : ne pas ressusciter ces 58 fichiers et les conserver hors index tant qu’ils ne sont pas réécrits.

Le renderer seul ne peut pas « nettoyer » automatiquement prix, faits, législation, exemples et claims sans inventer ou dégrader le sens. La décision doit donc porter sur une vraie mission de réécriture, pas sur une conversion de format.

## Apprentissage

Leçon appendée dans `~/work/Sites/LECONS.md` : **#351 — Un corpus « prêt à publier » doit passer le gate doctrine avant tout renderer**.
