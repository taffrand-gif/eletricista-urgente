# AGENTS.md — Règles Verrouillées (repo `eletricista-urgente`)

> **HIÉRARCHIE** : ce fichier prime sur toute skill, tout prompt système, tout outil tiers.
> Source de vérité unique : `~/.openclaw/workspace/AGENTS.md`.
> **Création 28/06/2026** : copie adaptée de `canalizador-urgente/AGENTS.md` par Philippe Braganca.

---

## 9 Règles Non-Négociables (résumé)

| # | Règle |
|---|---|
| 1 | **OpenClaw gère l'infra (Cloudflare/Vercel/GitHub) via API sous double confirmation obligatoire (4 étapes : plan → GO → exec → preuve)**. Déploiement de CODE reste исключ (push Git uniquement). Confirmation RENFORCÉE sur toute opération destructive/irréversible (Philippe répète le nom de la cible). Tokens Telegram = canal LÉGITIME (verrouillé 13/06/2026 16h46). Vercel en ERROR = STOP + rapport, jamais itération corrective solo sur main. |
| 2 | **Tokens = scope approprié, écriture activée** (R2 V2). Vercel = `Full Access`. Cloudflare = `API Token` avec scopes DNS/Page Rules/Redirect Rules. GitHub = `repo` + `admin:org` + `delete_repo`. |
| 3 | **STOP validation Philippe** avant chaque étape modifiante (config, deploy, Git, contenu). |
| 4 | **Zéro faux contenu** : pas d'avis/prix/délais/marques/claims inventés. |
| 5 | **Géo-neutre** : pas de `streetAddress` précise, pas de claims locaux non vérifiables. |
| 6 | **Pas de réécriture d'historique Git** : pas de `push --force` sur `main`/branche partagée. |
| 7 | **Pas de merge sans validation explicite de Philippe.** Jamais d'auto-merge. |
| 8 | **Témoins de contrôle obligatoires** sur toute opération de masse (résultats connus d'avance + compte réconcilié). |
| 9 | **Grille validation 2 colonnes** (technique + conformité). Vert technique + non vérifié conformité = REFUSÉ. |

**Règles complètes** : voir `~/.openclaw/workspace/AGENTS.md` (fichier global, prioritaire).

---

## Périmètre repo

- **Site satellite** : `eletricista-urgente.pt` (backlink vers `eletricista-norte-reparos.pt`)
- **Métier** : électricité (⚡)
- **NAP** : **+351 932 321 892** | Staff-Seekers | Filipe Bragança (artisan local)
  ⚠️ **JAMAIS** inverser avec 928 (canalizador-urgente). Cross-site referral OK (928 ↔ 932).
- **Branche de travail** : `main` (production)
- **Phase actuelle** : Phase 9 (correction géo-neutre) — EN ATTENTE REFONTE (~25k violations héritées)
- **Doctrine** : **Transparence Radicale** (cf. §12 — identique à `canalizador-urgente/AGENTS.md` §12, avec focus élec)

## Sécurité credentials

- ❌ JAMAIS afficher de clés API en clair
- ✅ 4 premiers chars max si mention
- ❌ Pas de tokens dans les commits

---

## 10. Robots.txt — Crawlers IA OUVERTS (verrouillée 14/06/2026 par Philippe)

**Décision stratégique** : les crawlers IA sont **OUVERTS par défaut**. Cette décision est verrouillée et ne se discute pas au cas par cas.

**Crawlers IA explicitement autorisés** (liste non exhaustive) :
- **OpenAI** : `GPTBot`, `ChatGPT-User`, `OAI-SearchBot`
- **Anthropic** : `ClaudeBot`, `Claude-User`, `Claude-SearchBot`
- **Google** : `Google-Extended`, `GoogleOther`, `Google-InspectionTool`
- **Perplexity** : `PerplexityBot`, `Perplexity-User`
- **Meta** : `Meta-ExternalAgent`, `FacebookBot`
- **Apple** : `Applebot-Extended`
- **Microsoft** : `CCBot`
- **Mistral / xAI / autres** : tout User-Agent contenant "Bot" ET opéré par une entité LLM connue

**Règle d'or** : **ne JAMAIS Disallow un crawler IA sans validation explicite de Philippe**. Si un crawler inconnu pointe vers le site avec un volume suspect (DDoS, scraping agressif), le signaler pour analyse — mais le bloquer reste une décision business qui m'appartient, pas à l'agent.

**Rationale** :
- Les LLM citent de plus en plus le contenu dans leurs réponses (recherche augmentée)
- Bloquer un crawler IA = perdre une source de trafic qualifié future
- Le contenu est géo-spécifique (Trás-os-Montes) et factuel = faible valeur pour l'entraînement générique

**Note technique** : la syntaxe robots.txt pour autoriser explicitement un bot est :
```
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /
```
Une absence de règle = autorisé par défaut.

---

## 11. ZÉRO INVENTION — Pas de chantiers inventés (verrouillée 15/06/2026 00:30 BST par Philippe)

**Règle absolue** : aucun contenu fabriqué de toutes pièces pour "meubler" une page qui devrait être honnête sur son manque de données réelles.

**Interdits** :
- ❌ **AUCUN exemple de chantier, intervention, ou réalisation spécifique** (ville + type de travail) qui ne soit pas confirmé par Philippe comme RÉEL
- ❌ **AUCUNE liste de "trabalhos realizados" / "trabalhos recentes" inventée** pour combler un vide
- ❌ **AUCUN nom de ville spécifique** (Bragança, Chaves, Mirandela, Macedo, Vila Real, Lamego) associé à un type de travail, sauf si confirmé par Filipe comme une vraie intervention réalisée
- ❌ **AUCUN nom de client, de rue, d'adresse, de commerce** inventé
- ❌ **AUCUNE "história" ou "caso"** narré pour illustrer une compétence, sans confirmation que c'est arrivé

**Principe fondamental** : **le vide honnête est meilleur que le faux**.

**Ce qu'il faut faire à la place** :
- ✅ Une page de témoignages honnête dit simplement "on démarre, premiers avis à venir" + mention honnête ("Estamos a recolher as primeiras avaliações dos nossos clientes") + section compromisso + CTA Tel+WhatsApp + équipement réel élec (**Fluke T6-1000, Megger MFT1741+, ROLeak Aqua 3Plus, FLIR E96, caméra thermique**) + FAQ honnête — **RIEN d'autre**
- ✅ Si une page a besoin d'être "meublée", préférer : equipamento profissional, zonas de atuação, perguntas frequentes úteis, próximos passos — **jamais inventer des exemples de chantiers**

**Validations attendues** : si je ne suis pas certain qu'un chantier soit réel, je **STOP et demande à Philippe** plutôt que d'inventer.

---

## 12. R12 — DOCTRINE DE POSITIONNEMENT : TRANSPARENCE RADICALE (verrouillée 28/06/2026 par Philippe)

**Pourquoi cette règle existe** : Norte Reparos / Staff-Seekers se différencie par la **TRANSPARENCE RADICALE**, à l'opposé des réseaux d'urgence anonymes qui surfacturent (peur n°1 du client = se faire arnaquer sur le prix, pas le délai — sources : Portal da Queixa, DECO Proteste, RTP).

**Chaque page produite ou modifiée DOIT incarner, dans cet ordre** :

1. **Transparence prix** (placée HAUT dans la page)
   - Grille affichée : **65 €/h** canal, **70 €/h** élec ← **CE SITE = 70 €/h**
   - Déplacement par zone : **Z1 = 15 € / Z2 = 25 € / Z3 = 35 € / Z4 = 45 € / Z5 = 55 € / Z6 = 65 €**
   - Majoration nuit/WE/feriado : **+50 %**
   - Phrase obligatoire : **"orçamento por escrito antes de qualquer intervenção, sem surpresas"**
2. **Artisan local identifiable**
   - Phrase obligatoire : **"fala sempre com a mesma pessoa, não um call center"**
   - **JAMAIS** l'anonymat (pas de "equipa de profissionais" sans visage, pas de numéro générique)
3. **Honnêteté / diagnostic transparent** : expliquer ce qui est fait et pourquoi, pas juste le prix
4. **Traçabilité** : facture avec NIF, seguro RC (responsabilité civile), garantia escrita. ⚠️ **JAMAIS** de « ficha/relatório/certificado émis » — voir règle ci-dessous.

**Règle d'or de la 1ʳᵉ phrase d'une page d'urgence** : elle **rassure sur le PRIX**, pas seulement sur la disponibilité.

**Cette doctrine se COMBINE avec (ne remplace pas)** :
- **R11 ZÉRO INVENTION** : aucun chantier/avis/témoignage inventé
- **R145 (jamais de délai chiffré)** : « 24h/7 dias » OK, **« resposta mediante confirmação por telefone » / « resposta prioritária » BANNIS**
- **Grille tarifaire EXACTE** (jamais de fourchette inventée ; hors grille = « sob orçamento »)
- **Géo-neutre** (jamais d'adresse/sede en dur ; widget géoloc dynamique seulement)
- **Équipement EXACT élec** : **Fluke T6-1000** (testeur tension/courant sans contact), **Megger MFT1741+** (testeur d'installation multifonction), **ROLeak Aqua 3Plus** (détection ACOUSTIQUE de fuites — rare sur le marché, vrai différenciateur), **FLIR E96** (caméra thermique 43 200 px), **caméra d'inspection 30 m** pour conduits
- **AUCUN DOCUMENT ÉMIS (ruling Filipe 2026-07-08, verrouillé)** : Filipe fait **uniquement le travail élec** (instalação, reparação, diagnóstico). Il ne délivre **ni certificat DGEG, ni relatório técnico (de conformidade), ni ficha eletrotécnica**. **INTERDIT** sur toute page : « emitimos/fazemos certificação », « relatório técnico », « fichas eletrotécnicas », « emissão de certificado », « instalações certificadas ». **INTERDIT AUSSI** toute mention du statut DGEG (« em curso », « enregistrement en cours », « aguardando », n° de dossier). Info éducative neutre OK (« a certificação é obrigatória por lei ») mais **jamais « nous le faisons »**. Reframe = décrire le **travail réel**, pas un livrable.

**Gabarit de référence** = §13 ci-dessous (« Standard de page différenciant » — identique à `canalizador-urgente/AGENTS.md` §13, focus élec).

⚠️ **VALIDATION OBLIGATOIRE** : **n'appliquer AUCUN batch de pages avant validation d'un prototype sur 1 page test** (et OK explicite de Philippe). Pas de script qui refait 50 pages en série. Pas de copier-coller généralisé sans revue.

**Validations attendues** : si je ne suis pas certain qu'un élément de positionnement (prix, phrase, formulation) soit conforme à la doctrine, je **STOP et demande à Philippe**.

---

## 13. STANDARD DE PAGE DIFFÉRENCIANT — ÉLEC (gabarit réutilisable — verrouillée 28/06/2026 par Philippe)

Moule de toutes les pages service/urgence électricité — focus risque électrique + différenciation artisanale.

### HEAD (meta)
- `title` : keyword principal + réponse/bénéfice (pattern validé sur la page jackpot). ~55-60 car.
- `meta description` : answer-first (la réponse directe à la question) + signal de transparence prix 70 €/h. ~150 car. Pas de tél.
- `<link rel="canonical">`
- JSON-LD : `Service` + `FAQPage` (+ `HowTo` si pertinent) + `LocalBusiness/Electrician` avec `areaServed` (zones) + `priceRange="70€-150€"`. **Jamais de `Review`/`AggregateRating` tant qu'il n'y a pas de vrais avis vérifiés.**

### CORPS (ordre d'affichage obligatoire)

1. **H1 court** (le keyword élec).
2. **Réponse-réflexe (1ʳᵉ phrase citable)** : répond directement à l'intention ET rassure sur le prix 70 €/h. Modèle urgence : *« Em caso de [problème eléctrico] em [zona], intervimos com preço claro (70 €/h) e orçamento por escrito antes de qualquer trabalho — sem surpresas na fatura. »*
3. **Bloc Transparence prix** (HAUT de page) : la grille (70 €/h élec, Z1-Z6, +50 % nuit/WE/feriado) + « orçamento por escrito antes de qualquer intervenção ». → **répond à la peur n°1 avant tout**.
4. **Bloc « Quem somos » (anti-société-écran)** : Staff-Seekers, **Filipe Bragança**, artisan local + emplacement photo réelle (jamais de stock) + « fala sempre com a mesma pessoa » + fatura NIF / seguro RC / fichas eletrotécnicas em conformidade.
5. **Le service élec** : Sintomas (curto-circuito, disjuntor que cai, cheiro a queimado, quadro antigo) → Causas (avec angle local Trás-os-Montes : instalação antiga sem terra, quadros sem disjuntor diferencial 30mA, sobrecarga por aquecimento elétrico) → Como resolvemos (méthode + équipement réel : Megger MFT1741+, Fluke T6-1000, FLIR E96, ROLeak acoustique) → Quando chamar um profissional (risco incêndio/electrocução).
6. **Prevenção / conseil** (valeur ajoutée que les clients recherchent) : importância do disjuntor diferencial 30mA, não sobrecarregar extensões, certificação DGEG.
7. **FAQ longue traîne** (5 questions, 40-60 mots, answer-first) — **inclure des questions de confiance** : « Quanto custa um eletricista em Trás-os-Montes? », « Como sei que a fatura é justa? », « Fazem orçamento antes? », « É urgente? Quanto tempo demoram? ».
8. **Zonas de intervention + maillage interne** (liens vers les pages villes du cluster → fait sortir plusieurs fois sur une requête).
9. **CTA** (tel **+351 932 321 892** + WhatsApp, sans promesse de délai chiffrée).
10. **Emplacements photos réelles** (`<!-- IMG -->` vides, vraies photos plus tard, jamais de stock).

### Règles opérationnelles héritées de R12

- Pas d'avis inventés (R11) → section témoignages = « Estamos a recolher as primeiras avaliações » tant que pas de vrais avis.
- Pas de délai chiffré (R145) → « 24h/7d » OK, **« resposta mediante confirmação por telefone/prioritária » INTERDIT**.
- Pas d'adresse postale (géo-neutre) → widget géoloc dynamique uniquement.
- Équipement exact élec listé dans R12 §1 (Fluke T6-1000, Megger MFT1741+, ROLeak Aqua 3Plus acoustique, FLIR E96, caméra 30m).
- = formule unique « em conformidade com a (enregistrement en cours) ».

### Validation

- **AUCUN batch** sur les pages sans avoir validé 1 prototype sur 1 page test.
- Pas de copier-coller automatique.
- Chaque page refaite est auditable : diff des balises HEAD + diff du 1ʳᵉ paragraphe + diff du bloc Transparence prix.

---

## 14. BOUCLE AUTONOME — SITE URGENTE TRANSPARENCE RADICALE (verrouillée 28/06/2026 par Philippe)

⚠️ **DIFFÉRENT de `canalizador-urgente`** : même Doctrine, mais NAP = **932** (Staff-Seekers élec), pas 928.

### Patterns à supprimer (R12 Transparence Radicale — focus élec)
- ❌ **Délais chiffrés inventés** : "resposta em 30min", "chegamos em 20 minutos", "tempo médio de resposta" — toute promesse chiffrée non contractuelle
- ❌ **Anonymat réseau** : "nossa equipa de profissionais" sans visage, numéro générique, "central de atendimento" — interdit
- ❌ **Phrases "resposta prioritária / mediante confirmação"** : interdit par R145
- ✅ **OK** : "24h/7 dias" (service disponibilité), "orçamento por escrito antes de qualquer intervenção, sem surpresas" (R12 §1)

### Grille EXACTE à afficher (R12 §1 — CE SITE)
- **70 €/h** (élec) — pas 65 €/h (c'est le canal)
- Déplacement Z1=15€ / Z2=25€ / Z3=35€ / Z4=45€ / Z5=55€ / Z6=65€
- Majoration nuit/WE/feriado : +50%
- Phrase obligatoire : « orçamento por escrito antes de qualquer intervenção, sem surpresas »

### Cycle obligatoire avant tout patch sur ce site

1. **Lire ce fichier §11-13** en ENTIER (Doctrine + gabarit + zéro invention).
2. **STOP validation Philippe OBLIGATOIRE** pour tout batch (R12 §validation) : *AUCUN batch de pages avant validation d'un prototype sur 1 page test*.
3. Si OK Philippe pour batch : témoin grep décomposé (3 motifs ci-dessus), patch 1 fichier à la fois, re-témoin.
4. **NE JAMAIS** : copier-coller automatique de la page jackpot sur 50 pages, inventer témoignages/chantiers (R11), appliquer Doctrine A+ (celle des `-norte-reparos`, pas la tienne).

### État au 28/06/2026
- ~25k violations R12 Transparence Radicale héritées (legacy)
- Refonte EN ATTENTE — décision business Philippe
- Aucun patch R12 batch sans GO explicite + prototype 1 page

---

## 15. Plan SEO/GEO — Coordination multi-IA (ajoutée 28/06/2026 par Philippe)

**Pourquoi** : 4 sites Norte Reparos, plusieurs IA/agents/harnais peuvent travailler dessus en parallèle. Il faut une **mémoire vivante partagée**.

➡️ **Plan complet** : `./SEO_PLAN.md` (vision, état actuel, TODO par phase, historique)

**OBLIGATOIRE pour toute IA / agent / harnais travaillant sur ce repo** :
1. **Lire `AGENTS.md` EN ENTIER** (§10 + §11 + §12 = robots + zéro invention + Transparence Radicale)
2. **Lire `SEO_PLAN.md` EN ENTIER** (tâche A1 = refonte homepage **70€/h** = PRIORITÉ 1)
3. **Consigner toute action** dans la section `🔄 HISTORIQUE` du `SEO_PLAN.md`
4. **Suivre l'ordre strict** : A1 (homepage) → A2 (8 pages /zonas/) → B1 (différenciation) → C (backlinks)
5. **Tarif = 70€/h** (PAS 65 qui est pour la canalisation) — vérifier à chaque modif
6. **JAMAIS merger dans `main`** sans STOP validation Philippe

**Tâches verrouillées dans SEO_PLAN.md** :
- **A1** : refonte homepage complète selon Doctrine §12 (10 sections, 70€/h)
- **A2** : 8 pages /zonas/ prioritaires
- **B1** : différenciation d'intention vs `eletricista-norte-reparos.pt`
- **C1-C4** : backlinks externes (continu)

**Hiérarchie des fichiers de coordination** :
1. `AGENTS.md` (ce fichier, règles verrouillées)
2. `CLAUDE.md` (config Claude Code, pointeur)
3. `SEO_PLAN.md` (mémoire vivante, à maintenir à jour)

---

## Annexe A. Identité Norte Reparos (transversale — ajoutée 30/06/2026 par Philippe, verrouillée)

> Bloc partagé entre les 4 sites Norte Reparos. À ne PAS dupliquer dans les pages client ; sert uniquement au contexte IA.

- **Maison-mère** : Norte Reparos (Portugal) — présentée comme une PME professionnelle multi-sites
- **Sites actifs** : canalizador-norte-reparos.pt (928 484 451) · canalizador-urgente.pt (928 484 451) · eletricista-norte-reparos.pt (932 321 892) · eletricista-urgente.pt (932 321 892)
- **Zone** : Trás-os-Montes, ~34 concelhos, rayon ~130 km autour de Macedo de Cavaleiros
- **Stack transversale** : React + Vite · GitHub (org `taffrand-gif`) · Vercel · Cloudflare DNS · n8n · Obsidian (vault `NORTE-OS`) · GA4 · Google Search Console · Google Ads · Meta Ads · TomTom · WhatsApp · ElevenLabs + Twilio (agent vocal, conçu, pas encore construit)
- **Certification élec** : DGEG `1757/2026/DIEN` en attente · co-signature LDE Mirandela en attendant
- **Langue** : interne FR informel · tout contenu client **PT-PT uniquement** (jamais PT-BR)

**Règle pronom — rédaction client uniquement (verrouillée 30/06/2026)** :
- « nous » toujours, « je » jamais côté HTML/PT visible
- Interdits : *je suis, je fais, mon entreprise, sozinho, contacto pessoal, falar comigo*
- OK : *a nossa equipa, os nossos técnicos, contacte-nos, garantimos, a nossa empresa*
- Vérifié à chaque livraison

**Compatibilité** : ce bloc complète la doctrine locale (R1-R11 + §11 ZÉRO INVENTION + §12 Doctrine Transparence Radicale + §13 gabarit + §14 boucle élec) sans la remplacer. En cas de contradiction, la doctrine locale prime.

---

**Source de vérité unique** : `~/.openclaw/workspace/AGENTS.md` (global) + ce fichier (site-spécifique).
