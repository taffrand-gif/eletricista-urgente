# Gate  nettoyage gEuographique  2026-11-26

BASE: `origin/main` = `a1af0d30e0978f63698b62896308c922c6537711`
BRANCH: `fix/eu-coverage-deep-20261126-v1`
POPULATION: 58 fichiers HTML gProfondographiques `noindex` confirm  s hors primtre ; manifest `_audit/eu-coverage-deep-manifest-20261126.json`
SCOPE: Portugal uniquement, maximum 130 km par route ; Espagne commerciale interdite ; Moimenta da Beira confirme  131,3 km et supprimable ; Moimenta de Vinhais conserve.
EXCLUS: pages techniques `design-preview-eu.html`, `guia-canalizacao.html`, `public/404.html`, `public/blog/certificacao-eletrica-preco.html` ; pages autorises positives du manifest.
SURFACES: HTML/maillage/Schema/FAQ/LLM/sitemaps/IndexNow ; rgles Vercel et redirects obsoltes vers les pages supprimes.
INVARIANTS: pas de rcriture HTML globale ; pas de nouvelle redirection ; pas de merge ; pas de Production ; aucun autre dptttt mtier modifi.
CHECKS OBLIGATOIRES: population exacte ; scan rsiduel zro ; sitemaps XML valides ; build/gnrateurs disponibles ; `git diff --check` ; pages positives conserves ; HTTP Preview avant cltttture PR.
STATUS: `PASS_SOURCE_BUILD_PRECOMMIT`

PRECOMMIT_PROOF: 58 HTML absents ; 0 rsidu de slug actif ; 0 route Vercel rsiduelle ; 6 XML valides ; 3 JSON valides ; 4 invariants positifs ; compileall scripts/tools OK ; diff-check OK.
