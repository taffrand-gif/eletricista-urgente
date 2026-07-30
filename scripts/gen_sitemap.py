#!/usr/bin/env python3
"""Génère un sitemap.xml PROPRE (eletricista-urgente).

Contenu = home + les concelhos indexables (drive-time réel) UNIQUEMENT.
Les ~1879 pages-aldeia doorway sont noindex et volontairement EXCLUES.
URLs extensionless (cleanUrls=true). Reproductible depuis data/concelhos.json.

⚠️ Ne JAMAIS remettre les 2000 doorways ici (risque scaled-content abuse).

Patch AUDIT-SITEMAP-TIERS-2026-07-30 (t_85288418) : <lastmod> calcule via
git log -1 %aI -- <file> au lieu de TODAY = date.today(). 9/10 sitemaps
Norte-OS etaient a 0-1.5% honnete.
"""
import json, os, datetime, subprocess

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://eletricista-urgente.pt"
TODAY = datetime.date.today().isoformat()


def git_lastmod(rel_path: str) -> str:
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%aI", "--", rel_path],
            cwd=REPO, capture_output=True, text=True, timeout=5,
        ).stdout.strip()
        if not out:
            return TODAY
        return out[:10]
    except Exception:
        return TODAY


def main():
    concelhos = json.load(open(os.path.join(REPO, "data", "concelhos.json")))
    entries = [(f"{BASE}/", "1.0", "index.html")]
    for c in concelhos:
        if c.get("indexable") and c.get("drive_time_status") == "real_tomtom":
            slug = c["slug"]
            entries.append((f"{BASE}/concelhos/{slug}", "0.8", f"concelhos/{slug}.html"))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, pr, rel in entries:
        lines.append(f"<url><loc>{loc}</loc><lastmod>{git_lastmod(rel)}</lastmod><priority>{pr}</priority></url>")
    lines.append("</urlset>")
    out = "\n".join(lines) + "\n"
    open(os.path.join(REPO, "sitemap.xml"), "w", encoding="utf-8").write(out)
    print(f"sitemap.xml écrit: {len(entries)} URLs (1 home + {len(entries)-1} concelhos)")


if __name__ == "__main__":
    main()
