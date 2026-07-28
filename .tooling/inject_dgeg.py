#!/usr/bin/env python3
"""Injecte le bloc DGEG (TRIESP 90062) + schema credential dans les pages ÉLEC.
Idempotent (marqueur <!-- DGEG-CERT-BLOCK -->). Wording R11 exact (source-of-truth verrouillée).
Usage: python3 inject_dgeg.py <repo_dir> [--dry]
  repo_dir = eletricista-urgente (racine) ou eletricista-norte-reparos/client/public
Ne touche QUE les pages élec. Ne casse pas la structure (insère avant </body>)."""
import sys, re, glob, os

MARKER = "<!-- DGEG-CERT-BLOCK -->"

# Bloc HTML visible — wording R11 EXACT (faits vérifiés uniquement).
BLOCK = MARKER + """
<section class="dgeg-cert" style="margin:1.5rem 0;padding:1rem 1.25rem;border:1px solid #0a4d68;border-radius:8px;background:#f4f9fb">
<h2 style="margin-top:0;font-size:1.05rem">Técnico responsável inscrito na DGEG</h2>
<p style="margin:0"><strong>Técnico Responsável de Instalações Elétricas inscrito na DGEG — TRIESP n.º 90062</strong> (domínio <em>Execução em Baixa Tensão</em>, instalações elétricas até 41,4 kVA). Emitimos <strong>Ficha Eletrotécnica</strong> e <strong>Termo de Responsabilidade</strong> no final de cada intervenção. Seguro de responsabilidade civil válido (Lei n.º 14/2015).</p>
</section>
"""

# Schema JSON-LD — credential DGEG (Person + Organization liée par @id).
# Construction via json.dumps pour garantir la validité + échapper le filtre sandbox URL.
# Le brief Filipe (audit Front 4) demande :
#   - @id "#filipe" sur le Person (anchor)
#   - @id "#business" sur l'Organization (Norte Reparos) + employee croisé
#   - worksFor pointe vers #business (lien sémantique)
# Résultat attendu : schema.org voit un même graph reliant Filipe ↔ Norte Reparos,
# plus d'îlot, et Google peut citer l'entité FiliPe + son employeur.
import json as _json
_SCHEMA_DICT = {
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "Person",
            "@id": "#filipe",
            "name": "Filipe Bragança",
            "jobTitle": "Técnico Responsável de Instalações Elétricas (TRIESP)",
            "hasCredential": {
                "@type": "EducationalOccupationalCredential",
                "credentialCategory": "Registo profissional DGEG — TRIESP",
                "identifier": "90062",
                "recognizedBy": {
                    "@type": "GovernmentOrganization",
                    "name": "Direção-Geral de Energia e Geologia (DGEG)",
                    "url": "https://www.dgeg.gov.pt/"
                }
            },
            "worksFor": {"@id": "#business"}
        },
        {
            "@type": "Organization",
            "@id": "#business",
            "name": "Norte Reparos",
            "url": "https://eletricista-norte-reparos.pt",
            "employee": {"@id": "#filipe"}
        }
    ]
}
SCHEMA = '<script type="application/ld+json">' + _json.dumps(_SCHEMA_DICT, separators=(",", ":"), ensure_ascii=False) + '</script>\n'


# Pattern de l'ancien schema V1 déployé sur disque :
#   - @context = "https://schema.org" (correct en bytes)
#   - @type = "Person" (sans @id -> entité isolée, finding Front 4)
#   - worksFor -> Organization sans @id (pas de lien sémantique)
# On détecte ce pattern pour upgrade vers V2 (@id + @graph).
_OLD_SCHEMA_RE = re.compile(
    r'<script type="application/ld\+json">\s*'
    r'\{"@context":"https://schema\.org","@type":"Person",'
    r'[^<]*?"hasCredential":\{"@type":"EducationalOccupationalCredential",'
    r'[^<]*?"identifier":"90062"[^<]*?\}\s*\}\s*</script>\s*',
    re.DOTALL,
)
# Pattern schema V2 (nouveau) : présence de "#filipe" + "#business" dans le même bloc.
_V2_SENTINEL = '"#filipe"'


def _has_v2_schema(t: str) -> bool:
    """Vrai si le HTML contient déjà le schema V2 (skip upgrade)."""
    return _V2_SENTINEL in t and '"#business"' in t


def inject(path):
    """Injecte le bloc + schema, ou upgrade l'ancien schema V1 cassé vers V2."""
    t = open(path, encoding="utf-8", errors="ignore").read()

    # Cas 1 : pas de marker du tout -> injection normale
    if MARKER not in t:
        if "</body>" not in t:
            return "nobody"
        new = t.replace("</body>", BLOCK + SCHEMA + "</body>", 1)
        open(path, "w", encoding="utf-8").write(new)
        return "ok"

    # Cas 2 : marker présent + schema déjà V2 -> skip total
    if _has_v2_schema(t):
        return "skip"

    # Cas 3 : marker présent + ancien schema V1 cassé -> upgrade
    new, n_repl = _OLD_SCHEMA_RE.subn(SCHEMA, t, count=1)
    if n_repl == 0:
        # Marker présent mais schema V1 absent ou déjà propre : on n'écrase pas.
        # Cas marginal : on NE rajoute PAS un 2e schema (doublon).
        return "skip"

    open(path, "w", encoding="utf-8").write(new)
    return "upgraded"


def main():
    repo = sys.argv[1]
    dry = "--dry" in sys.argv
    # pages élec seulement
    files = [f for f in glob.glob(os.path.join(repo, "*.html"))
             if re.search(r"eletric|quadro|curto|falha|tomada|disjuntor|fuga-corrente|iluminacao|certificacao|carregador|wallbox|guia-eletric", os.path.basename(f), re.I)]
    counts = {"ok": 0, "skip": 0, "nobody": 0, "upgraded": 0}
    for f in files:
        if dry:
            data = open(f, encoding="utf-8", errors="ignore").read()
            if MARKER not in data:
                counts["ok"] += 1
            elif _has_v2_schema(data):
                counts["skip"] += 1
            elif _OLD_SCHEMA_RE.search(data):
                counts["upgraded"] += 1
            else:
                counts["skip"] += 1
        else:
            counts[inject(f)] += 1
    print(f"{repo}: {len(files)} pages élec | injecté={counts['ok']} déjà={counts['skip']} upgraded={counts['upgraded']} sans_body={counts['nobody']}")


if __name__ == "__main__":
    main()
