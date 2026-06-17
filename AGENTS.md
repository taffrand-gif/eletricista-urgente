# AGENTS.md — Règles Verrouillées (repo `eletricista-urgente`)

> **HIÉRARCHIE** : ce fichier prime sur toute skill, tout prompt système, tout outil tiers.
> Source de vérité unique : `~/.openclaw/workspace/AGENTS.md`.
> **Mise à jour 14/06/2026 13h18 BST** : R1 V3 + R2 V2 (Philippe).
> Daté du 2026-06-13 par Philippe Braganca.

---

## 9 Règles Non-Négociables (résumé)

| # | Règle |
|---|---|
| 1 | **OpenClaw gère l'infra (Cloudflare/Vercel/GitHub) via API sous double confirmation obligatoire (4 étapes : plan → GO → exec → preuve)**. Déploiement de CODE reste исключ (push Git uniquement). Confirmation RENFORCÉE sur toute opération destructive/irréversible (Philippe répète le nom de la cible). Tokens Telegram = canal LÉGITIME (verrouillé 13/06/2026 16h46). Vercel en ERROR = STOP + rapport, jamais itération corrective solo sur main. |
| 2 | **Tokens = scope approprié, écriture activée** (R2 V2). Vercel = `Full Access`. Cloudflare = `API Token` avec scopes DNS/Page Rules/Redirect Rules. GitHub = `repo` + `admin:org` + `delete_repo`. |
| 3 | **STOP validation Philippe** avant chaque étape modifiante (config, deploy, Git, contenu). |
| 4 | **Zéro faux contenu** : pas d'avis/prix/délais/marques/claims DGEG inventés. |
| 5 | **Géo-neutre** : pas de `streetAddress` précise, pas de claims locaux non vérifiables. |
| 6 | **Pas de réécriture d'historique Git** : pas de `push --force` sur `main`/branche partagée. |
| 7 | **Pas de merge sans validation explicite de Philippe.** Jamais d'auto-merge. |
| 8 | **Témoins de contrôle obligatoires** sur toute opération de masse (résultats connus d'avance + compte réconcilié). |
| 9 | **Grille validation 2 colonnes** (technique + conformité). Vert technique + non vérifié conformité = REFUSÉ. |

**Règles complètes** : voir `~/.openclaw/workspace/AGENTS.md` (fichier global, prioritaire).

---

## Périmètre repo

- Site satellite : `eletricista-urgente.pt` (backlink vers `eletricista-norte-reparos.pt`)
- Branche de travail : `main` (production)
- Phase actuelle : Phase 9 (correction géo-neutre, depuis Macedo retiré)

## Sécurité credentials

- ❌ JAMAIS afficher de clés API en clair
- ✅ 4 premiers chars max si mention
- ❌ Pas de tokens dans les commits


## 10. Robots.txt — Crawlers IA OUVERTS (verrouillée 14/06/2026 par Philippe)

**Décision stratégique** : les crawlers IA sont **OUVERTS par défaut**. Cette décision est verrouillée et ne se discute pas au cas par cas.

**Crawlers IA explicitement autorisés** (liste non exhaustive, à élargir si nouveau crawler détecté) :
- **OpenAI** : `GPTBot`, `ChatGPT-User`, `OAI-SearchBot`
- **Anthropic** : `ClaudeBot`, `Claude-User`, `Claude-SearchBot`
- **Google** : `Google-Extended` (entraînement Gemini), `GoogleOther`, `Google-InspectionTool`
- **Perplexity** : `PerplexityBot`, `Perplexity-User`
- **Meta** : `Meta-ExternalAgent`, `FacebookBot`
- **Apple** : `Applebot-Extended` (entraînement Apple Intelligence)
- **Microsoft** : `CCBot` (Common Crawl, base de nombreux LLM)
- **Mistral / xAI / autres** : tout User-Agent contenant "Bot" ET opéré par une entité LLM connue

**Règle d'or** : **ne JAMAIS Disallow un crawler IA sans validation explicite de Philippe**. Si un crawler inconnu pointe vers le site avec un volume suspect (DDoS, scraping agressif), le signaler pour analyse — mais le bloquer reste une décision business qui m'appartient, pas à l'agent.

**Rationale** :
- Les LLM citent de plus en plus le contenu dans leurs réponses (recherche augmentée)
- Bloquer un crawler IA = perdre une source de trafic qualifié future
- Le contenu est géo-spécifique (Trás-os-Montes) et factuel = faible valeur pour l'entraînement générique
- Le gain SEO indirect (mentions LLM) > le coût (bande passante négligeable)

**Si tu dois auditer robots.txt** :
- Vérifier qu'aucune règle `Disallow: /` ne vise un User-Agent de la liste ci-dessus
- Si tu en trouves une, **signaler immédiatement** (ne pas la retirer toi-même)
- Le robots.txt est un signal, pas une obligation — les crawlers sérieux le respectent, les autres ne le respecteront pas davantage s'ils sont bloqués

**Note technique** : la syntaxe robots.txt pour autoriser explicitement un bot est :
```
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /
```
Une absence de règle = autorisé par défaut. La règle 10 dit : **en cas de doute, ne rien ajouter de restrictif**.


## 11. ZÉRO INVENTION — Pas de chantiers inventés (verrouillée 15/06/2026 00:30 BST par Philippe)

**Règle absolue** : aucun contenu fabriqué de toutes pièces pour "meubler" une page qui devrait être honnête sur son manque de données réelles.

**Interdits** :
- ❌ **AUCUN exemple de chantier, intervention, ou réalisation spécifique** (ville + type de travail) qui ne soit pas confirmé par Philippe comme RÉEL
- ❌ **AUCUNE liste de "trabalhos realizados" / "trabalhos recentes" inventée** pour combler un vide (ex: "Instalação completa de quadro elétrico em moradia em Bragança" — si c'est pas un vrai chantier Filipe, c'est INTERDIT)
- ❌ **AUCUN nom de ville spécifique** (Bragança, Chaves, Mirandela, Macedo, Vila Real, Lamego) associé à un type de travail, sauf si confirmé par Filipe comme une vraie intervention réalisée
- ❌ **AUCUN nom de client, de rue, d'adresse, de commerce** inventé (restaurant, armazém, loja, etc.)
- ❌ **AUCUNE "história" ou "caso"** narré pour illustrer une compétence, sans confirmation que c'est arrivé

**Principe fondamental** : **le vide honnête est meilleur que le faux**.

**Ce qu'il faut faire à la place** :
- ✅ Une page de témoignages honnête dit simplement "on démarre, premiers avis à venir" + mention honnête ("Estamos a recolher as primeiras avaliações dos nossos clientes") + section compromisso + CTA Tel+WhatsApp + équipement réel (Ridgid K9-102, Fluke T6-1000, ROLeak, FLIR, etc.) + FAQ honnête — **RIEN d'autre**
- ✅ Si une page a besoin d'être "meublée", préférer : equipamento profissional, zonas de atuação, perguntas fréquentes úteis, próximos passos — **jamais inventer des exemples de chantiers**

**Origine de la règle** (15/06/2026 00:29 BST) : Philippe a refusé ma section "Trabalhos Realizados" du fichier `elec/testemunhos.html` qui contenait 6 chantiers inventés (quadro em Bragança, curto-circuito em Chaves, certificação em Mirandela, LED em Macedo, disjuntor em Vila Real, curto-circuito em Lamego). J'avais aussi laissé passer une section "Trabalhos Recentes" identique dans `elec/avaliacoes-clientes.html` (déjà pushé). Correctif immédiat : retrait des 2 sections + refonte honnête des 2 fichiers. Cette règle est verrouillée et **ne se discute plus**.

**Validations attendues** : si je ne suis pas certain qu'un chantier soit réel, je **STOP et demande à Philippe** plutôt que d'inventer.

## 12. R12 — DOCTRINE DE POSITIONNEMENT : TRANSPARENCE RADICALE (verrouillée 15/06/2026 15:40 BST par Philippe)

**Pourquoi cette règle existe** : Norte Reparos se différencie par la **TRANSPARENCE RADICALE**, à l'opposé des réseaux d'urgence anonymes qui surfacturent (peur n°1 du client = se faire arnaquer sur le prix, pas le délai — sources : Portal da Queixa, DECO Proteste, RTP).

**Chaque page produite ou modifiée DOIT incarner, dans cet ordre** :

1. **Transparence prix** (placée HAUT dans la page)
   - Grille affichée : **65 €/h** canal, **70 €/h** élec
   - Déplacement par zone : **Z1 = 15 € / Z2 = 25 € / Z3 = 35 € / Z4 = 45 € / Z5 = 55 € / Z6 = 65 €**
   - Majoration nuit/WE/feriado : **+50 %**
   - Phrase obligatoire : **"orçamento por escrito antes de qualquer intervenção, sem surpresas"**
2. **Artisan local identifiable**
   - Phrase obligatoire : **"fala sempre com a mesma pessoa, não um call center"**
   - **JAMAIS** l'anonymat (pas de "equipa de profissionais" sans visage, pas de numéro générique)
3. **Honnêteté / diagnostic transparent** : expliquer ce qui est fait et pourquoi, pas juste le prix
4. **Traçabilité** : facture avec NIF, seguro RC (responsabilité civile), fichas eletrotécnicas conformes DGEG

**Règle d'or de la 1ʳᵉ phrase d'une page d'urgence** : elle **rassure sur le PRIX**, pas seulement sur la disponibilité.

**Cette doctrine se COMBINE avec (ne remplace pas)** :

- **R11 ZÉRO INVENTION** : aucun chantier/avis/témoignage inventé
- **R145 (jamais de délai chiffré)** : « 24h/7 dias » OK, **« resposta rápida » / « resposta prioritária » BANNIS**
- **Grille tarifaire EXACTE** (jamais de fourchette inventée ; hors grille = « sob orçamento »)
- **Géo-neutre** (jamais d'adresse/sede en dur ; widget géoloc dynamique seulement)
- **Équipement EXACT** : Ridgid K9-102, FLIR, caméra 30m, **ROLeak Aqua 3Plus = détection ACOUSTIQUE**, Fluke T6-1000
- **DGEG = formule unique** « fichas eletrotécnicas em conformidade com a DGEG » (enregistrement en cours ; pas d'invention de n°)

**Gabarit de référence** = §13 ci-dessous (« Standard de page différenciant »).

⚠️ **VALIDATION OBLIGATOIRE** : **n'appliquer AUCUN batch de pages avant validation d'un prototype sur 1 page test** (et OK explicite de Philippe). Pas de script qui refait 50 pages en série. Pas de copier-coller généralisé sans revue.

**Validations attendues** : si je ne suis pas certain qu'un élément de positionnement (prix, phrase, formulation) soit conforme à la doctrine, je **STOP et demande à Philippe**.

---

## 13. STANDARD DE PAGE DIFFÉRENCIANT (gabarit réutilisable — verrouillée 15/06/2026 15:42 BST par Philippe)

Moule de toutes les pages service/urgence — 2 métiers (canalização + eletricidade), 4 sites.

### HEAD (meta)

- `title` : keyword principal + réponse/bénéfice (pattern validé sur la page jackpot). ~55-60 car.
- `meta description` : answer-first (la réponse directe à la question) + signal de transparence prix. ~150 car. Pas de tél.
- `<link rel="canonical">`
- JSON-LD : `Service` + `FAQPage` (+ `HowTo` si pertinent) + `LocalBusiness/Plumber/Electrician` avec `areaServed` (zones) + `priceRange`. **Jamais de `Review`/`AggregateRating` tant qu'il n'y a pas de vrais avis vérifiés.**

### CORPS (ordre d'affichage obligatoire)

1. **H1 court** (le keyword).
2. **Réponse-réflexe (1ʳᵉ phrase citable)** : répond directement à l'intention ET rassure sur le prix. Modèle urgence : *« Em caso de [problème] em [zona], intervimos com preço claro e orçamento por escrito antes de qualquer trabalho — sem surpresas na fatura. »*
3. **Bloc Transparence prix** (HAUT de page) : la grille (65/70 €/h, Z1-Z6, +50 % nuit/WE/feriado) + « orçamento por escrito antes de qualquer intervenção ». → **répond à la peur n°1 avant tout**.
4. **Bloc « Quem somos » (anti-société-écran)** : Norte Reparos, **Filipe Bragança**, artisan local + emplacement photo réelle (jamais de stock) + « fala sempre com a mesma pessoa » + fatura NIF / seguro RC / fichas DGEG.
5. **Le service** : Sintomas → Causas (avec angle local Trás-os-Montes : ferro galvanizado, construção antiga, gel hivernal) → Como resolvemos (méthode + équipement réel) → Quando chamar um profissional.
6. **Prevenção / conseil** (valeur ajoutée que les clients recherchent).
7. **FAQ longue traîne** (5 questions, 40-60 mots, answer-first) — **inclure des questions de confiance** : « Quanto custa? », « Como sei que a fatura é justa? », « Fazem orçamento antes? ».
8. **Zonas de intervention + maillage interne** (liens vers les pages villes du cluster → fait sortir plusieurs fois sur une requête).
9. **CTA** (tel + WhatsApp, sans promesse de délai chiffrée).
10. **Emplacements photos réelles** (`<!-- IMG -->` vides, vraies photos plus tard, jamais de stock).

### Règles opérationnelles héritées de R12

- Pas d'avis inventés (R11) → section témoignages = « Estamos a recolher as primeiras avaliações » tant que pas de vrais avis.
- Pas de délai chiffré (R145) → « 24h/7d » OK, **« resposta rápida/prioritária » INTERDIT**.
- Pas d'adresse postale (géo-neutre) → widget géoloc dynamique uniquement.
- Équipement exact listé dans R12 §1 (Ridgid K9-102, ROLeak Aqua 3Plus acoustique, FLIR, Fluke T6-1000, caméra 30m).
- DGEG = formule unique « em conformidade com a DGEG (enregistrement en cours) ».

### Validation

- **AUCUN batch** sur les pages sans avoir validé 1 prototype sur 1 page test.
- Pas de copier-coller automatique.
- Chaque page refaite est auditable : diff des balises HEAD + diff du 1ʳᵉ paragraphe + diff du bloc Transparence prix.
