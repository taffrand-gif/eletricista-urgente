# SMKO eu — eletricista-aguas-vivas — 2026-09-24 (re-test post tâche t_7b290488)

**Tâche** : t_7b290488
**URL** : https://eletricista-urgente.pt/eletricista-aguas-vivas
**Source signalement** : scan local « wrong-phone » 2026-09-24
**Extrait fourni** : `ign:center;background:#0a4d68;color:#fff"><h2 style="color:#fff">Eletricista em Águas Vivas?</h2><a class="cta" href="tel:+351****1892">…`

## Verdict

**KO wrong-phone RÉFUTÉ — aucun écart NAP, fichier conforme, aucun commit requis.**

## Vérification contenu (téléphone — point nommé par la preuve live)

### Salve exhaustive des numéros 9 chiffres dans le fichier

| Pattern | Occurrences |
|---------|-------------|
| `+351 932 321 892` (NAP élec, E.164 lisible) | 12 |
| `932 321 892` (forme courte) | 1 |
| `+351****1892` (href `tel:` masqué, cf. PRICING.md §NAP) | 7 |
| `+351-932 321 892` (JSON-LD Schema.org) | 2 |
| **`928 …` (NAP canal — à NE PAS mettre sur EU)** | **0** |
| **Toute autre séquence 9 chiffres** | **0** |

**Total : 22 occurrences, 100 % sur le NAP élec 932 321 892. Aucune trace de 928 ou d'un numéro tiers.**

### Comparaison local ↔ live (Vercel edge)

| Source | SHA256 | Taille | ETag Vercel |
|--------|--------|--------|-------------|
| `eletricista-aguas-vivas.html` local | `cb4efa019bbb8497303e445229a301fbbfcd550f1e2e9564bd3968c94d95f2ae` | 30 378 octets | n/a |
| `https://eletricista-urgente.pt/eletricista-aguas-vivas` (curl 2026-09-24 23:30 BST) | `cb4efa019bbb8497303e445229a301fbbfcd550f1e2e9564bd3968c94d95f2ae` | 30 378 octets | `b2b43040a919e8bc9528a18ef2a20d4d` |
| `https://eletricista-urgente.pt/eletricista-aguas-vivas` (audit SMKO 2026-09-15, 10 probes) | (identique) | 30 378 octets | `b2b43040…` (stable) |

**Match parfait local = live, ETag stable depuis 14/09 20:47 UTC.** Aucun déploiement divergent, aucun drift NAP.

### Vérification de l'extrait cité dans la preuve live

L'extrait fourni commence par `ign:center;background:#0a4d68;color:#fff` et contient `<a class="cta" href="tel:+351****1892">`. Recherche exhaustive dans le fichier :

| Pattern recherché | Résultat |
|-------------------|----------|
| `ign:center;background:#0a4d68` | 0 occurrence |
| `color:#fff"><h2 style="color:#fff">Eletricista` | 0 occurrence (les `<h2 style="color:#fff">` n'existent pas ; le seul `color:#fff` après `0a4d68` est sur `<aside class="doctrine-transparence">` qui n'a pas de `tel:`) |
| `class="cta" href="tel:+351****1892"` | 0 occurrence (les `class="cta"` ont `tel:+351****1892` sur **quelques** lignes, mais sans le préfixe `ign:center` ni le H2 « Eletricista em Águas Vivas » associé) |

**L'extrait est un composite reconstitué** (concaténation de fragments de bouts de lignes différents) qui ne correspond à aucun endroit du fichier réel. Le scan local a vraisemblablement lu des caractères sur plusieurs lignes voisines et assemblé un faux match — pas un vrai défaut du fichier servi.

### Vérification NAP-cohérence (Doctrine R12 + PRICING.md)

- **PRICING.md §NAP** : Élec = `+351 932 321 892` ; Canal = `+351 928 484 451`. ✅ Fichier conforme (que du 932).
- **AGENTS.md §Périmètre repo** : « JAMAIS inverser avec 928 (canalizador-urgente) ». ✅ Aucune occurrence 928.
- **AGENTS.md §12 R12 §1** : NAP élec 932 cohérent avec doctrine Transparence Radicale. ✅.
- **JSON-LD LocalBusiness** (`<script type="application/ld+json">` ligne 36) : `"telephone":"+351 932 321 892"` ✅.
- **OpenGraph `og:title`** (ligne 32) : « Eletricista Águas Vivas — 30€ | +351 932 321 892 » ✅ (NAP OK ; le « 30€ » est un autre sujet, hors-porte de cette tâche wrong-phone).
- **Schema.org BreadcrumbList + FAQPage + Service + LocalBusiness** (lignes 65, 71) : `telephone` toujours 932. ✅.

### Vérification absence contamination plomberie

Recherche des termes typiques d'un template-bleed plomberie (cf. tâche t_e6bfd650 corticos, fix e24f1cb00) :

| Pattern | Occurrences |
|---------|-------------|
| `Fuga ativa` / `Inundação` / `Cano rebentado` / `Esgoto a transbordar` / `Válvula de segurança` | 0 / 0 / 0 / 0 / 0 |
| `feche a torneira geral` / `feche o contador` | 0 / 0 |
| `torneira` (hors équipement ROLeak) | 0 |
| `aquecimento` (sens plomberie) | 0 |
| `canalização` / `canalizador` (hors JSON-LD `sameAs`) | 0 (les `sameAs` pointent vers les sites irmãos, légitime) |

**Aucune contamination plomberie.** La seule occurrence de « fugas » est dans la mention de l'équipement `ROLeak Aqua 3Plus` (légitime, c'est un outil élec de détection acoustique, listé en AGENTS.md §12 R12 §1).

## État repo

- working tree : aucun changement sur `eletricista-aguas-vivas.html` ; rapport `_audit/SMKO-eu-2026-09-24-aguas-vivas.md` seul ajouté, non staged
- commit : aucun
- `eletricista-aguas-vivas.html` : non touché (30378 octets, 162 lignes, sha256 `cb4efa01…`)
- `sitemap.xml` : non touché

## Diagnostic

Même classe de signal que t_c6432a28 (cnr/salzedas), t_ac479308 (cnr/marialva), t_1662f744 (cu/alvendre), t_c0beada0 (eu/amendoeira), t_4fa3d40f (cu/almendra), t_9ce7c4c5-mezquita-cu : **faux positif scan local**. Le détecteur a vraisemblablement concaténé des fragments de plusieurs lignes pour fabriquer un faux match « wrong-phone » qui n'existe pas dans le fichier réel ni dans la version servie.

À noter que la page a 2 défauts **secondaires** sans rapport avec le téléphone :
1. **Doublons `<head>`** (lignes 32 + 34) — défaut de structure HTML, pré-existant.
2. **« Zona 3 » + « Zona 4 »** affichées en parallèle (lignes 97/100 et 98/101) — incohérence interne mineure, hors-porte de cette tâche wrong-phone.

Aucune action recommandée pour cette tâche. Conformément à R7, **STOP validation Filipe avant toute autre intervention** sur ce fichier (les défauts 1+2 ci-dessus peuvent être corrigés dans un batch séparé avec GO explicite, suivant la doctrine « AUCUN batch sans prototype 1 page test » de AGENTS.md §12).

## Leçon (série en cours)

8e KO signalisé réfuté en 9 jours (14/09 → 24/09) sur les 4 sites eu/cu/cnr. Le scan « wrong-phone » local a un taux de faux positifs élevé quand l'extrait cité est un composite multi-lignes. Avant tout patch wrong-phone, **toujours** :
1. Vérifier `sha256` local = live (curl + etag)
2. Compter toutes les occurrences des NAP 928/932 (un seul des deux doit dominer selon le site)
3. Vérifier que l'extrait cité existe tel quel dans le fichier (chercher chaque fragment séparément)
4. Si les 3 checks passent → réfutation, rapport `_audit/`, PR draft consignation, **pas de patch**.
