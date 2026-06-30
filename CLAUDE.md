# CLAUDE.md — Configuration Claude Code (Norte-OS)

> Lu par Claude Code dans VSCode. **Ne duplique pas la doctrine** : voir `./AGENTS.md`.
> Daté du 2026-06-28 par Philippe Braganca.

## Site
- **Domaine** : eletricista-urgente.pt
- **NAP** : +351 932 321 892 | Norte Reparos | Trás-os-Montes
- **Métier** : électricité (⚡) — site satellite de `eletricista-norte-reparos.pt`
- **Doctrine** : **Transparence Radicale** (PAS Doctrine A+ — voir `./AGENTS.md` §12)
- **État au 28/06/2026** : 🔴 EN ATTENTE REFONTE (~25k violations héritées)
- **Stack** : statique Vite + HTML/CSS
- **Déploiement** : `git push` → Vercel auto

## Commandes & outils Atlas
- `git fetch && git status` AVANT toute modif (#154)
- Pas de `npm run test`/`lint`/`build` standard — sites statiques
- Slash commands : `/goal` (boucle audit), `/loop`, `/review`

## Workflow patch (rappel court — ⚠️ DIFFÉRENT des sites `-norte-reparos`)
1. **Lire `./AGENTS.md` §11-14** EN ENTIER (Doctrine Transparence Radicale + zéro invention + gabarit + boucle)
2. **STOP validation Philippe OBLIGATOIRE** pour tout batch (cf. §12) — *AUCUN batch de pages avant prototype 1 page validé*
3. Témoin grep décomposé AVANT (motifs R12 §12 : délais chiffrés inventés, anonymat réseau, "resposta prioritária")
4. Patch 1 fichier à la fois (R15 : max 95 fichiers/commit, justifié)
5. Témoin grep APRÈS + commit référencé leçon
6. Push SANS `--force` (R6)

## Doctrine complète
➡️ `./AGENTS.md` (Doctrine Transparence Radicale, NAP 932, R11-R14 — gabarit page + boucle élec)

## Patterns R12 à supprimer (DIFFÉRENTS des `-norte-reparos`)
- ❌ Délais chiffrés inventés : "resposta em 30min", "chegamos em X minutos", "tempo médio"
- ❌ Anonymat réseau : "nossa equipa de profissionais" sans visage, "central de atendimento"
- ❌ Phrases "resposta prioritária / mediante confirmação" (R145)
- ✅ OK : "24h/7 dias" (disponibilité), "orçamento por escrito antes de qualquer intervenção"

## Plan stratégique SEO/GEO
➡️ `./SEO_PLAN.md` (vision, état actuel, TODO par phase, historique — priorité 🔴 refonte)

## 🧠 Mémoire / Leçons (durable, cross-sites)
➡️ `~/work/Sites/LECONS.md` — registre **append-only** des leçons méthode (survit aux `context.md` écrasés). **Lire AVANT d'agir**, **ajouter** après chaque erreur corrigée ou découverte, **ne jamais écraser**.
➡️ `~/work/Sites/HERMES_MISSIONS_2026Q3.md` (missions cross-sites) · `~/work/Sites/MONOPOLE_SEO_2026Q3.md` (stratégie).

**OBLIGATOIRE** : toute IA / agent / harnais travaillant sur ce repo DOIT :
1. **Lire `AGENTS.md` EN ENTIER** (§11 + §12 + §13 + §14 = ZÉRO INVENTION + Transparence Radicale + gabarit + boucle élec)
2. **Lire `SEO_PLAN.md` EN ENTIER** (tâche A1 = refonte homepage 70€/h = PRIORITÉ 1)
2-bis. **Lire `MARKETING.md`** (couche offensive : persona, value equation, construction de hooks — complète AGENTS.md, ne le remplace pas)
3. **Consigner toute action** dans la section `🔄 HISTORIQUE` du `SEO_PLAN.md`
4. **Suivre l'ordre strict** : A1 (homepage) → A2 (8 pages /zonas/) → B1 (différenciation) → C (backlinks)
5. **Tarif = 70€/h** (PAS 65 qui est pour la canalisation) — vérifier à chaque modif
6. **JAMAIS merger dans `main`** sans STOP validation Philippe

## Pas touche
- ❌ Pas de duplication de règles ici
- ❌ Pas de duplication du plan dans `SEO_PLAN.md`
- ❌ Pas de batch sans GO Philippe + prototype 1 page
- ❌ Pas de copier-coller automatique (R12 §validation)
| ❌ Pas d'invention de chantiers/témoignages (R11)
| ❌ Pas de mention "65€/h" ici (c'est 70€/h pour l'élec)

---

## Identité Norte Reparos (transversale — ajoutée 30/06/2026)

> Bloc d'identité partagé entre les 4 sites. À ne PAS dupliquer dans les pages client ; sert uniquement au contexte IA.

- **Maison-mère** : Norte Reparos (Portugal) — présentée comme une PME professionnelle multi-sites
- **Sites actifs** : `canalizador-norte-reparos.pt` (928 484 451) · `canalizador-urgente.pt` (928 484 451) · `eletricista-norte-reparos.pt` (932 321 892) · `eletricista-urgente.pt` (932 321 892)
- **Zone** : Trás-os-Montes, ~34 concelhos, rayon ~130 km autour de Macedo de Cavaleiros
- **Stack transversale** : React + Vite · GitHub (org `taffrand-gif`) · Vercel · Cloudflare DNS · n8n · Obsidian (vault `NORTE-OS`) · GA4 · Google Search Console · Google Ads · Meta Ads · TomTom · WhatsApp · ElevenLabs + Twilio (agent vocal, conçu, pas encore construit)
- **Certification élec** : DGEG `1757/2026/DIEN` en attente · co-signature LDE Mirandela en attendant
- **Langue** : interne FR informel · tout contenu client **PT-PT uniquement** (jamais PT-BR)
- **Positionnement site** : parler « a nossa equipa / os nossos técnicos / contacte-nous / garantimos ». **JAMAIS « je suis seul / entreprise individuelle / contacto pessoal »** sur les pages visibles client — règle absolue, verrouillée par Philippe 30/06/2026
- **Pronom** : **« nous » toujours, « je » jamais** côté rédaction client. Interdits : *« je suis », « je fais », « mon entreprise », « sozinho »*. À utiliser : *« nous sommes », « notre équipe », « nous faisons », « a nossa equipa », « fazemos »*. Vérifié à chaque livraison.

> **Note de compatibilité** : ce bloc ne remplace ni `AGENTS.md` (verrouillé, prime) ni `SEO_PLAN.md`. Si contradiction, `AGENTS.md` l'emporte.
