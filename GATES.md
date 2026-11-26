# GATES. EU coverage deletion 2026-11-25

BASE: origin/main
POPULATION: 17 HTML files explicitly authorized for deletion
SCOPE: confirmed Spain, Moimenta/Tavira/Viseu hors couverture, excluding Vila Verde da Raia (Chaves) and Vila Nova da Rainha (Macedo de Cavaleiros)
EXCLUDED: Chaves, ValpaMdos, reserved CNR PAA pages, all other files
INVARIANTS: no sitemap or generator edits in this deletion step; no production; no merge
CHECKS: exact manifest, git diff --check, deleted paths only, generators inspected before PR
STATUS: pending validation


# GATES. EU SEO/GEO pilot 2026-11-26
BASE: origin/main
POPULATION: 1 HTML page (blog/tomada-nao-funciona.html)
SCOPE: freshness dateModified/date visible + removal of unsupported stock, coverage, and unvalidated price claims on the page witness
EXCLUDED: interruptor-nao-funciona.html, all locality pages, generators, sitemap, IndexNow, R145, production
INVARIANTS: PT-PT; EU phone +351 932 321 892; tel and WhatsApp CTA; central pricing 70 €/h + 30 € day / 100 €/h + 50 € night-weekend-holiday; no new geography or regulated claim
CHECKS: JSON-LD parse all blocks; exact price/CTA witnesses; forbidden-claim scan; git diff --check; changed paths only
ROLLBACK: git revert <commit>
STATUS: PARTIEL — PASS_SOURCE; Preview/HTTP/DOM/production non vérifiés tant que la PR reste Draft
