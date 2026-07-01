#!/usr/bin/env python3
"""R12 Blog Safe Cleanup EU — patch UNIQUEMENT les zones safe:
- <title>...</title>
- <meta ... />
- <script type="application/ld+json">...</script>

PAS LE BODY <p>, <li>, <h2>, <a href>
"""
import re, json
from pathlib import Path

ROOT = Path("/Users/admin/work/Sites/eletricista-urgente")
TARGETS = []
TARGETS += list((ROOT / "blog").glob("*.html"))
TARGETS += list((ROOT / "public" / "blog").glob("*.html"))

# Patterns (identiques à PR #93 + #94 EU hubs)
PATTERNS = [
    # Variantes longues
    (r"Atendemos 24h/7 dias, mediante confirmação por telefone — ligue 932 321 892, garantimos atenção mediante confirmação por telefone",
     "Atendemos 24h/7d, ligue 932 321 892 (orçamento por escrito em poucos minutos)"),
    (r"Atendimento mediante confirmação por telefone — ligue 932 321 892, garantimos atendimento mediante confirmação por telefone",
     "Atendimento — ligue 932 321 892, damos orçamento por escrito após auscultação por telefone"),
    (r"Resposta mediante confirmação por telefone — ligue 932 321 892, garantimos atendimento mediante confirmação por telefone",
     "Diagnóstico por telefone em poucos minutos, ligue 932 321 892"),
    (r"o atendimento é mediante confirmação por telefone — ligue 932 321 892, garantimos atendimento mediante confirmação por telefone",
     "o atendimento começa por orçamento escrito — ligue 932 321 892"),
    # Motifs courts
    (r"Atendemos 24h/7 dias, mediante confirmação por telefone",
     "Atendemos 24h/7d"),
    (r"Atendimento mediante confirmação por telefone/7d, 7 dias por semana\. Para emergências, atendemos sempre\.",
     "Atendimento 24h/7d, 7 dias por semana. Para emergências, atendemos sempre."),
    (r"Atendimento mediante confirmação por telefone/7d",
     "Atendimento 24h/7d"),
    (r"Atendimento mediante confirmação por telefone, sem surpresas",
     "Atendimento 24h/7d, sem surpresas"),
    (r"Atendimento mediante confirmação por telefone\. orçamento por escrito",
     "Atendimento. orçamento por escrito"),
    (r"Atendimento mediante confirmação por telefone",
     "Atendimento — ligue 932 321 892"),
    (r"atendimento é mediante confirmação por telefone",
     "atendimento é por telefone"),
    (r"atendimento mediante confirmação por telefone",
     "orçamento por escrito após auscultação por telefone"),
    (r"Resposta a confirmar por telefone",
     "Diagnóstico por telefone em poucos minutos"),
    (r"Resposta mediante confirmação por telefone",
     "Diagnóstico por telefone em poucos minutos"),
    (r"Resposta conforme disponibilidade",
     "Deslocação conforme zona Z"),
    (r"Ligue mediante confirmação por telefonemente",
     "Ligue imediatamente"),
    (r"© 2024(.*?Norte Reparos)", r"© 2026\1"),
    (r"© 2024", "© 2026"),
    (r"地下室", "cave"),
    # FALLBACK GÉNÉRIQUE (en DERNIER)
    (r"mediante confirmação por telefone",
     "orçamento por escrito por telefone"),
]


def main():
    stats = {"files_scanned": 0, "files_modified": 0, "total_replacements": 0}
    targets = list(set(TARGETS))
    print(f"Total targets: {len(targets)}")
    for p in sorted(targets):
        stats["files_scanned"] += 1
        content = p.read_text(encoding="utf-8")
        original = content

        # 1. patch <title>...</title>
        content = re.sub(r"<title[^>]*>.*?</title>",
                         lambda m: __apply(m.group(0)),
                         content, flags=re.DOTALL)
        # 2. patch <meta ... />
        content = re.sub(r"<meta[^>]+>", lambda m: __apply(m.group(0)), content)
        # 3. patch JSON-LD scripts
        content = re.sub(
            r'<script[^>]*type\s*=\s*"application/ld\+json"[^>]*>.*?</script>',
            lambda m: __apply(m.group(0)), content, flags=re.DOTALL)

        if content != original:
            p.write_text(content, encoding="utf-8")
            stats["files_modified"] += 1
            stats["total_replacements"] += sum(
                content.count(re.findall(r"mediante confirmação por telefone|Resposta conforme disponibilidade|Resposta a confirmar por telefone", original)[0] if re.findall(...) else "") for _ in [1]
            ) if False else 0
            # Approximation: just count
            n_before = len(re.findall(r"mediante confirmação por telefone|Resposta conforme disponibilidade|Resposta a confirmar por telefone", original))
            n_after = len(re.findall(r"mediante confirmação por telefone|Resposta conforme disponibilidade|Resposta a confirmar por telefone", content))
            stats["total_replacements"] += max(0, n_before - n_after)

    print(json.dumps(stats, indent=2, ensure_ascii=False))


def __apply(zone):
    for pat, repl in PATTERNS:
        zone = re.sub(pat, repl, zone)
    return zone


if __name__ == "__main__":
    main()
