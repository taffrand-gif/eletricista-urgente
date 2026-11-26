

## Résultat mécanique final

- Done-gate v3.14 exécuté le 2026-11-26 sur `792b27254fb1de26cec55a4a5d5dff8a8fa8e92b`.
- `PASS_SOURCE=VERT` ; 2 fichiers du lot, 2 occurrences base → HEAD, invariants couverts, aucun prix ajouté.
- Résidu hors lot mesuré : 1 658 occurrences / 537 fichiers, déclaré via `--expect 1658` en mode pilote.
- Contrôle Preview public : déploiement Vercel `dpl_FWZnzroekapx4wAVCQvbRdjJnK2F`, `READY`, URL `https://eletricista-urgente-eu14465uq-filipes-projects-4b992c3d.vercel.app/`, SHA `13063b4fc2ecf058e2629669b95a06789d7c6b67`.
- `PASS_PREVIEW` homepage : DOM indépendant via navigateur connecté, `readyState=complete`, H1 unique, title présent, canonical `https://eletricista-urgente.pt/`, téléphone `932 321 892`, tarifs `70 €/h + 30 €` et `100 €/h + 50 €`, 8 CTA `tel:`/WhatsApp visibles, aucun chevauchement, 3 blocs JSON-LD valides, bandeau RGPD visible avec boutons `Aceitar`/`Recusar`.
- Contrôle source/Preview : les marqueurs attendus du commit `13063b4fc` sont présents dans le rendu public ; source locale `index.html` : 26 533 octets, SHA-256 `b6040df5c9fb538d0ce43784e7c2e8b8b5341adafb97826ae2cadc2d8fcac3aa`, 1 H1, 3 blocs JSON-LD, 12 occurrences du téléphone, 4 liens WhatsApp, consentement `rgpd-consent-eu-v1`.
- Smoke public : `/robots.txt`, `/llms-full.txt` et `/aumento-de-potencia` récupérés avec contenu ; les 7 cibles supprimées ne renvoient aucun contenu extractible via la sonde web, mais leur code HTTP exact reste `NON VÉRIFIÉ` car le terminal local était bloqué par la politique DNS et l’outil web ne restitue pas le code des erreurs sans contenu.
- Artefact, régénération et Production : `NON VÉRIFIÉS`.
- Statut gate : `PARTIEL — PASS_SOURCE + PASS_PREVIEW homepage ; HTTP exact des cibles négatives, régénération et Production NON VÉRIFIÉS`, sans exception. PR maintenue Draft, sans Ready, merge ni déploiement Production.
- Manifest run : `/Users/admin/agents/done-gate/runs/20261126-234020-792b2725.json`.
