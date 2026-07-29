# context.md — Loop State

> Écrit par le loop Cowork après chaque run. NE PAS ÉDITER MANUELLEMENT.

## Dernier run
- Date : 2026-07-29
- Tâche exécutée : **R145 — réponses FAQ vides laissées par la purge des délais** (violation détectée en lecture, traitée en priorité sur la tâche prévue conformément à R11/R12). La tâche recommandée au run précédent — soumission IndexNow — reste 🛑 gatée sur un GO infra de Philippe.
- Branche créée : `loop/2026-07-29-eletricista-urgente-faq-stub-prototype`
- PR ouverte : https://github.com/taffrand-gif/eletricista-urgente/pull/200
- Résultat : ✅ 2 commits, 2 fichiers (1 par commit, atomique). **PROTOTYPE SUR 1 SEULE PAGE** conformément à AGENTS.md §12. Témoins R8 : `demoram a chegar` 1→0, `conforme zona` 1→0, −130 octets, bloc `FAQPage` re-parsé après patch = **JSON valide** (2 questions restantes, réponses réelles). Attente GO merge + GO batch Philippe.

## 🛑 DÉCISION REQUISE — gisement de 955 fichiers
Une purge R145 antérieure a laissé des `acceptedAnswer` **cassées ou vides** dans le JSON-LD `FAQPage` de **~955 fichiers** (hors `_archive/`), sur la question « Quanto tempo demoram a chegar? ». 4 variantes :

| Occurrences | Valeur de `text` |
|---|---|
| 527 | `" conforme zona"` — vide : commence par une espace, sans sujet ni verbe |
| 418 | `" min conforme zona. atendimento após contacto telefónico ao telefone."` — unité « min » orpheline (nombre retiré), « ao telefone » redondant, minuscule initiale |
| 6 | `" min conforme zona. Atendemos 24h/7 dias, após contacto telefónico ao telefone."` |
| 4 | `" min conforme zona. Atendimento 24h/7 dias, ligue 932 321 892 ao telefone."` |

**Impact** : ~955 pages servent à Google un `FAQPage` dont une réponse est syntaxiquement vide ou incohérente → risque de perte d'éligibilité aux rich results FAQ.

**Pourquoi la réponse n'est pas réparable** : la question porte sur un **délai d'arrivée**. R145 interdit tout délai chiffré, R11 interdit d'inventer, et « resposta mediante confirmação por telefone » est explicitement BANNIE par R145. Aucune réponse honnête ET conforme n'existe → **retrait du couple Q/R** = seule issue. Le vide honnête > le faux (R11).

**Décision demandée à Philippe** : (a) valider le pattern du prototype (PR #200), (b) autoriser ou non le batch sur les ~954 fichiers restants. Le loop ne le fera pas sans GO explicite (AGENTS.md §12 : pas de script qui refait 50 pages en série).

## Tâche suivante recommandée
- **Si GO batch reçu sur PR #200** : appliquer le même retrait aux ~954 fichiers restants. ⚠️ Traiter les 4 variantes séparément (motifs distincts) et re-parser le `FAQPage` de chaque fichier après patch pour garantir un JSON valide — c'est le contrôle qui a validé le prototype.
- **Sinon** : vérifier le même défaut sur `canalizador-urgente` (même généalogie de purge R145) — audit lecture seule, pas de patch sans GO.
- Autres pistes, toutes 🛑 gatées : soumission IndexNow réelle (PR #160), blog resurrection 58 MD, curto-circuito dedup FAQ (branche `feat/monopole-piliers-eu`, à pusher).

## Audit de conformité effectué ce run (lecture seule, `origin/main`, `_archive/` exclu)
Motifs verrouillés AGENTS.md — **0 occurrence sur chacun** : `resposta prioritária`, `mediante confirmação`, `emitimos`, `certificação`, `instalações certificadas`, `trabalho profissional`, `DGEG`, `aggregateRating`, `+351-` (NAP au tiret).
➡️ La dette **A4-TER** signalée au run du 18/07 (« 76 × *Atendimento prioritário* + claims §11, ~80 fichiers ») est **RÉSOLUE** : 0 occurrence de `prioritári` sur tout le repo hors `_archive/`. Ne pas la rouvrir.

## Apprentissages (self-improving)
- ⚠️ **HEURISTIQUE FAUSSE À SUPPRIMER** — les notes antérieures disaient « ce site = 70€/h, donc un `65€` ici est une erreur ». **C'est FAUX et dangereux.** `65€` est le **tarif de déslocation de la Zone 6**, parfaitement légitime sur les 4 sites (1489 fichiers en contiennent ici). `calculadora-de-preco.html` énonce d'ailleurs correctement les deux : « mão-de-obra (canalização 65€/h, eletricidade 70€/h) » — cette page sert les 2 métiers. **Ne jamais “corriger” un `65€` sans lire son contexte.** La distinction réelle est : 70 €/h = **main-d'œuvre électricité**, 65 €/h = **main-d'œuvre canalisation**, 65 € = **déplacement Z6**.
- ⚠️ **PIÈGE DE TOOLING MAJEUR** : passer un motif contenant `€` ou des guillemets imbriqués à `git grep -F` via une boucle inline `zsh -c` **mange le motif et renvoie 0 résultat** — faux négatif silencieux. Un premier audit de ce run a conclu « 0 fichier avec 65€ » alors que la réalité est **1489**. **Toujours écrire un script (`bash x.sh` / `python3 x.py`) pour tout grep à motif non-ASCII**, jamais une boucle inline.
- **Méthode fiable pour auditer ce repo statique volumineux** : `git archive origin/main | tar -x -C /tmp/scan` puis grep local. Évite à la fois les pathspecs `git grep` capricieux et la copie de travail sale.
- R145 **autorise explicitement « 24h/7 dias »** (AGENTS.md L123/L163). Ce qui est banni, ce sont les promesses de délai personnalisées (« resposta prioritária », « mediante confirmação por telefone »). ⚠️ C'est **l'inverse** des sites `*-norte-reparos` (installation), où « 24h » est une violation R12 par cannibalisation d'intent. **La même chaîne est violation sur 2 sites et conforme sur les 2 autres.**
- Les purges automatiques de conformité (comme celle qui a créé ce gisement) **doivent re-valider le JSON-LD après coup** : retirer une sous-chaîne d'un `acceptedAnswer` produit du JSON syntaxiquement valide mais sémantiquement vide, ce qu'aucun linter ne détecte. Contrôle à ajouter à tout futur batch : re-parser chaque bloc `FAQPage` et vérifier que chaque `text` fait > 20 caractères et commence par une majuscule.

## Edge cases détectés
- **Worktree obligatoire sur ce repo** : copie de travail sale en permanence (`LECONS.md`, `public/robots.txt`, `public/sitemap.xml`, `robots.txt`, `sitemap-villages.xml` modifiés) et posée sur `fix/sitemap-refresh`. Pattern fiable appliqué ce run : `git worktree add -q /tmp/eu-wt -b <branche> origin/main`, travailler là, `git worktree remove` à la fin.
- **Agents concurrents confirmés sur ce checkout** (documenté 18/07, contamination de la branche `loop/2026-07-18-...-refresh` par un commit tiers). Parade appliquée ce run : `git branch --show-current` vérifié avant **chaque** commit, `git diff origin/main..HEAD --name-only` avant le push, `gh pr create --head <branche-explicite>`. Aucune collision constatée.
- `public/index.html` et `./index.html` **diffèrent** (même situation que sur `canalizador-urgente`). Canonicals identiques et corrects des deux côtés (`https://eletricista-urgente.pt/`) donc pas d'urgence, mais le doublon reste à arbitrer — voir le `context.md` de `canalizador-urgente` §1 pour l'analyse complète (99 fichiers, `vercel.json` sans `outputDirectory`).
- Le sandbox `mcp__workspace__bash` n'a ni `gh` ni credentials Git → tout git/gh passe par `mcp__desktop-commander__start_process` (host macOS, `gh` authentifié `taffrand-gif`).
- Ce repo est un site **statique pur** : pas de `npx tsc` possible, la vérification post-patch se fait par grep + re-parsing JSON.

## Blocages connus
1. **Batch FAQ ~954 fichiers** = 🛑 attente validation du prototype PR #200 + GO batch (AGENTS.md §12).
2. **Soumission API IndexNow** (PR #160) = 🛑 attente GO infra Philippe (AGENTS.md Règle 1).
3. **Blog resurrection 58 MD** = 🛑 bloqué conformité, attente décision Philippe.
4. **curto-circuito dedup FAQ** (branche `feat/monopole-piliers-eu`) = 🟡 à pusher + GO merge, non traité.
5. **Doublon `public/` ↔ racine** — à arbitrer conjointement avec `canalizador-urgente`.
6. A2 (/zonas/ 8 pages, blocage du 30/06) : **considéré obsolète** — 33 hubs concelhos + 200 villages P1C livrés depuis.

## Instructions améliorées pour prochain run
1. **Ne jamais “corriger” un `65€` sur ce site** sans lire son contexte : c'est le déplacement Z6, légitime. (Heuristique inverse notée dans d'anciens runs = fausse.)
2. **Tout grep à motif non-ASCII (`€`, accents, guillemets imbriqués) doit passer par un script**, jamais par une boucle inline — sinon faux négatifs silencieux.
3. **Travailler en `git worktree`** (`git worktree add -q /tmp/eu-wt -b <branche> origin/main`), jamais en `git checkout` dans `~/work/Sites/eletricista-urgente`.
4. **Vérifier `git branch --show-current` avant CHAQUE commit** et `git diff origin/main..HEAD --name-only` avant chaque push (agents concurrents).
5. Utiliser `gh pr create --head <branche-explicite>`, jamais le HEAD courant.
6. **Ne PAS purger « 24h » sur ce site** — R145 l'autorise explicitement.
7. Ne pas rouvrir A4-TER (`Atendimento prioritário`) : 0 occurrence, résolu.
8. Tout futur batch de conformité doit **re-parser le JSON-LD après patch** et vérifier que chaque `acceptedAnswer.text` est non vide — c'est précisément ce contrôle manquant qui a produit le gisement de 955 fichiers.
