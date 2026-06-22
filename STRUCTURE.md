# STRUCTURE — `eletricista-urgente` (eletricista-urgente.pt)

> Site **statique HTML** (satellite SEO du principal `eletricista-norte-reparos.pt`). Pas de build, pas de framework : fichiers `.html` servis tels quels par Vercel. Jumeau statique de `canalizador-urgente`.
> Doc = ce qui EXISTE et est prouvé sur disque (2026-06-22). Pas un idéal.
> ⚠️ **`AGENTS.md` prime sur ce fichier** (9 règles verrouillées Filipe). Lire AGENTS.md avant toute action.
> **PROD** : domaine `eletricista-urgente.pt`. Remote GitHub = source de vérité. Déploiement = **push Git**.

---

## 1. Nature du repo

Pas de `package.json`, pas de bundler. ~1900 pages `.html` autonomes + assets, servies en statique par Vercel avec `cleanUrls`. Pages **générées** par substitution de placeholders (§3).

## 2. Arborescence réelle

```
eletricista-urgente/
├── eletricista-<slug>.html   ~1900 pages-villes À PLAT à la racine (1 fichier = 1 ville)
├── calculadora-de-preco.html  contactos.html  comparacao.html …   pages outils/hub
├── blog/            articles .html (~27+)
├── concelhos/       14 pages hub par concelho
├── distritos/       6 pages hub par district
├── public/          assets
├── scripts/         génération + maintenance (scripts/archive/ = ponctuels passés)
├── dist/            ⚠️ artefact de build COMMITÉ (voir §6)
├── vercel.json      cleanUrls, redirects, rewrite → .html (§5)
├── sitemap.xml  robots.txt  llms.txt  ai.txt
├── AGENTS.md        ⚠️ règles verrouillées (prioritaires)
└── .gitignore       .vercel, __pycache__, *.pyc/pyo, .DS_Store, *.log
```

**3A — pages-villes à plat, on NE réorganise PAS.** Réorganiser casserait ~1900 URLs + redirects + sitemap. Routing = `cleanUrls` (§5), pas l'arborescence.

## 3. Génération des pages-villes (template à placeholders)

Mécanisme = **substitution de placeholders** dans un template HTML vers `eletricista-<slug>.html`. Placeholders du même schéma R13 :
`{{CIDADE}}` `{{ZONA}}` `{{SLUG}}` `{{DESLOCACAO}}` `{{PRECO_DESDE}}` `{{PRECO_DESDE_NUM}}` `{{MAILLAGE}}` `{{LOCAL_BUSINESS_TYPE}}`

🔴 **Template source non localisé pour ce repo.** Les masters R13 connus (`~/.openclaw/workspace/REVUE_MISSION_18039_2026-06-15/`) ne contiennent QUE des masters `canal` (`master-canal-R13.html`, GOLDEN canalizador). **Aucun master R13 électricien n'a été trouvé.** La source de génération de ce site est donc soit une adaptation non versionnée du master canal, soit perdue. À clarifier/recréer (voir §6).

### Ajouter une ville (procédure, sous réserve §6)
1. Partir d'une page-ville existante saine de ce repo (`eletricista-<slug>.html`) comme référence locale, à défaut d'un master élec.
2. Adapter le contenu pour la nouvelle ville (`{{CIDADE}}`/`{{SLUG}}`/`{{ZONA}}`/prix/maillage), périmètre électricité.
3. Écrire `eletricista-<slug>.html` à la racine (`slug` = minuscules, sans accent, tirets).
4. Ajouter au `sitemap.xml` + maillage interne.
5. `git add` ciblé + commit + push.

⚠️ Génération de masse = **R8 (témoins de contrôle)** d'AGENTS.md : compte attendu + réconcilié.

## 4. blog / concelhos / distritos

Pages `.html` statiques : hubs par concelho/district (maillage interne) + articles dans `blog/`. Servies directement.

## 5. Routing & déploiement (Vercel statique)

`vercel.json` :
- `cleanUrls: true`, `trailingSlash: false` → URLs sans extension.
- `rewrites`: `{"source":"/(.*)","destination":"/$1.html"}` → URL propre → fichier `.html`.
- `redirects` (26) : normalisations `/public/...` → 301, etc. Toute page ajoutée/retirée = vérifier redirects + sitemap.
- `headers` : cache/sécurité.

**Déploiement** = `git push` sur la branche prod (règle R1 AGENTS.md, jamais d'API/CLI Vercel pour publier). Vercel en ERROR = STOP + rapport.

## 6. Pièges & divergences connus (signalés, NON corrigés — décision Filipe)

- 🔴 **Pas de master R13 électricien retrouvé** (§3) : site non reproductible depuis un template dédié. À recréer/rapatrier dans le repo (`_templates/`).
- ⚠️ **`dist/` est commité** dans le repo (artefact de build statique). Devrait être ignoré (`.gitignore` n'exclut PAS `dist/` ici, contrairement à l'attendu). À retirer du suivi git après vérif.
- ⚠️ **Contenu hors cœur de métier** : des pages du repo sortent du périmètre électricité. À examiner/nettoyer (décision Filipe) — non listées ici, non touchées.

## 7. Hors périmètre

- Site React principal : `eletricista-norte-reparos` (`STRUCTURE.md` dédié).
- `microsites`, `fabric` : hors de ce repo.
