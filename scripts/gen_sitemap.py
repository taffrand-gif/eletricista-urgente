#!/usr/bin/env python3
"""Génère un sitemap.xml PROPRE (eletricista-urgente).

Contenu = home + les concelhos indexables (drive-time réel) UNIQUEMENT.
Les ~1879 pages-aldeia doorway sont noindex et volontairement EXCLUES.
URLs extensionless (cleanUrls=true). Reproductible depuis data/concelhos.json.

⚠️ Ne JAMAIS remettre les 2000 doorways ici (risque scaled-content abuse).
"""
import json, os, datetime

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://eletricista-urgente.pt"
TODAY = datetime.date.today().isoformat()

def main():
    concelhos = json.load(open(os.path.join(REPO, "data", "concelhos.json")))
    urls = [(f"{BASE}/", "1.0")]
    for c in concelhos:
        if c.get("indexable") and c.get("drive_time_status") == "real_tomtom":
            urls.append((f"{BASE}/concelhos/{c['slug']}", "0.8"))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, pr in urls:
        lines.append(f"<url><loc>{loc}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>")
    lines.append("</urlset>")
    out = "\n".join(lines) + "\n"
    open(os.path.join(REPO, "sitemap.xml"), "w", encoding="utf-8").write(out)
    print(f"sitemap.xml écrit: {len(urls)} URLs (1 home + {len(urls)-1} concelhos)")

if __name__ == "__main__":
    main()
