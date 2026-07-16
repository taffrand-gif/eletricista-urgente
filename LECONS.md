# LECONS.md — eletricista-urgente · Phil-Hermes

> Mémoire locale du repo eletricista-urgente (satellite urgence ⚡).
> Source de vérité globale : `~/.openclaw/workspace/AGENTS.md`.
> Format : 1 leçon = (date, contexte, takeaway actionnable, source).

---

## Leçon #P0bis-2026-07-16-01 — Sitemap-EMPTY trahirait GSC

**Contexte** : mission P0bis « Remplacer sitemap.xml complet par sitemap-core : 33 hubs concelhos/ + 6 distritos/ + pages money-kw + piliers ». État disque hérité : 0 page `concelhos/` (malgré la PR #147 qui les prétend générées), 0 `distritos/`, 0 money-kw, 0 village page. Seul `sitemap.xml` les référençait toutes.

**Takeaway** : ne JAMAIS publier un sitemap.xml contenant des URLs dont le fichier HTML n'existe pas. Le sitemap est un signal GSC : publier 90% d'URLs cassées détruit la confiance de Google, plus lentement qu'un 404 massif mais plus sûrement (CRAWLED_NOT_INDEXED qui se propage aux rares pages valides).

**Action canon** :
1. Avant tout sitemap, lister les fichiers HTML présents sur disque (`ls public/ | grep .html | wc -l`)
2. Pour chaque URL candidate, vérifier qu'un fichier existe (`os.path.exists` + NFD-normalisation pour diacritiques)
3. Si cible manquante, **retarder** la publication dans `sitemap-core.xml` ou documenter dans `sitemap-villages.xml` (squelette + manifeste explicite)
4. Le pattern « sitemap-vide mais honnête + manifeste » est toujours préférable à « sitemap-plein mais mensonger »

**Source** : PR #149 `/RAPPORT-P0BIS-P1-2026-07-16.md` § Étape 1.

---

## Leçon #P0bis-2026-07-16-02 — Jaccard 0.92 vs cible 0.35 = STOP obligatoire

**Contexte** : mission P0bis+ « Variante A — bloc de differenciation hub-concelho money » sur 33 pages. SPEC §10 fixe cible Jaccard pairwise médian ≤ 0.35 ; §11.5 dit « si fail → STOP, rapporte, ne batch pas ». Mesure baseline = **0.92**, soit 2.6x la cible.

**Takeaway** : un générateur automatique qui se contente d'injecter un bloc Variant A templatée (variant seulement `concelho_name` + 6 villages) **n'atteint pas** la cible Jaccard. La cause structurelle = 5 sections sur 8 du gabarit actuel sont à 0.95-1.00 de Jaccard ; Variante A ne touche que la section ajoutée.

**Action canon** :
1. **TOUJOURS mesurer le Jaccard sur le corps complet** avant batch
2. Si Jaccard médian > cible : STOP, écrire un rapport détaillé (sections responsables + effort estimé), ne PAS batcher
3. Pour atteindre Jaccard 0.35 sur ces hubs, prévoir un rewriter de gabarit (refonte 4-5 sections par hub) qui n'est pas une Variante A
4. `price_block` BLOQUÉ tant que préséance zones non tranchée — absence explicite sans chiffre de secours (SPEC §11.4)

**Source** : PR `/RAPPORT-P0BIS-P1-2026-07-16.md` § Étape 2.

---

## Leçon #P0bis-2026-07-16-03 — Convention URL `/concelhos/` ≠ racine `public/concelhos/`

**Contexte** : en arrivant sur la branche PR #149, j'ai d'abord cherché `public/concelhos/*.html` (racine `public/`) — pas trouvé. Conclusion erronée « 0 page concelhos/ ». En fait les pages sont à la racine du repo : `concelhos/<slug>.html`. Le `vercel.json` n'a pas de rewrite `/concelhos/(.*)` mais le site sert la racine (`outputDirectory: "."`) donc `/concelhos/<slug>` → `concelhos/<slug>.html` servi tel quel.

**Takeaway** : avant tout audit sitemap/url, faire un `ls`large de la racine du repo et de `public/`. Le path URL n'implique pas un sous-dossier de `public/`. `vercel.json` peut servir `.` entier.

**Action canon** :
1. Audit disque sur **deux niveaux** : `ls -la` à la racine du repo ET `ls public/`
2. Lire `vercel.json` pour comprendre `outputDirectory` et `rewrites`
3. Les pages satellites existent souvent à la racine, pas dans `public/`

**Source** : Session mission P0bis 2026-07-16 (5 min de recherche évitée si appliqué).

---

## Cross-références

- Variante A non exécutée : voir `RAPPORT-P0BIS-P1-2026-07-16.md` § Étape 2 + 3 options présentées à Philippe
- Sitemap tiering PR #149 : commit `10e3bd109`
- Spec source : `~/work/Sites/_audit/SPEC-DIFFERENCIATION-P1-2026-07-16.md`
- Skill transversal : `local-business-seo-compliance` (R0 + ref `r0-canonical-selfref.md`)
