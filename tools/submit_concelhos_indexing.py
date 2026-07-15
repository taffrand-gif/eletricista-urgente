#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""submit_concelhos_indexing.py — force-submit les 33 concelhos EU à Indexing API.

Tâche: t_8d3cbf2a — vague 1 différenciation EU.
Gate DoD: sortie Indexing API 200 collée pour les 30+ URLs concelhos.
Suit le patron canonique: ~/work/Sites/indexing-api-2026-07-11.py
"""
import json, os, sys, time
import urllib.request, urllib.error
from datetime import datetime, timezone
from pathlib import Path

from google.oauth2 import service_account
from google.auth.transport.requests import Request as GAuthRequest

KEY_PATH = os.path.expanduser("~/.hermes/gsc-indexing-key.json")
SCOPES = ["https://www.googleapis.com/auth/indexing"]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
EU = "https://eletricista-urgente.pt"
HERE = Path(__file__).resolve().parent.parent
LOG_JSON = HERE.parent.parent / "INDEXING-API-2026-07-15-EU-concelhos.json"
LOG_MD = HERE.parent.parent / "INDEXING-API-2026-07-15-EU-concelhos.md"


def get_creds():
    with open(KEY_PATH) as f:
        info = json.load(f)
    creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    creds.refresh(GAuthRequest())
    return creds


def post_url(creds, url):
    body = json.dumps({"url": url, "type": "URL_UPDATED"}).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {creds.token}",
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(ENDPOINT, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read().decode("utf-8")
            try:
                return r.status, json.loads(raw) if raw else {}
            except Exception:
                return r.status, {"raw": raw}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, {"raw": raw}
    except urllib.error.URLError as e:
        return -1, {"error": f"URLError: {e.reason}"}


def main():
    dry = "--dry" in sys.argv
    concelhos_dir = HERE / "concelhos"
    slugs = sorted(p.stem for p in concelhos_dir.glob("*.html"))
    urls = [f"{EU}/concelhos/{s}" for s in slugs]

    log = {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "dry_run": dry,
        "service_account": None,
        "n_targets": len(urls),
        "submissions": [],
        "errors": [],
        "stats": {"total": 0, "ok": 0, "fail": 0},
    }

    if not dry:
        try:
            creds = get_creds()
            log["service_account"] = json.load(open(KEY_PATH))["client_email"]
        except Exception as e:
            log["errors"].append(f"auth_failed: {e}")
            print(json.dumps(log, indent=2, ensure_ascii=False))
            return 1

    for i, url in enumerate(urls, 1):
        if dry:
            code, body = 200, {"urlNotificationMetadata": {"latestUpdate": {"url": url}}}
            time.sleep(0.02)
        else:
            code, body = post_url(creds, url)
            time.sleep(0.15)
        log["submissions"].append({"url": url, "status": code, "body": body})
        log["stats"]["total"] += 1
        if code == 200:
            log["stats"]["ok"] += 1
        else:
            log["stats"]["fail"] += 1
        if i % 5 == 0 or i == len(urls):
            print(f"  [{i}/{len(urls)}] {url}: {code}", flush=True)

    log["ended_at"] = datetime.now(timezone.utc).isoformat()
    with open(LOG_JSON, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)
    # markdown report
    md_lines = [
        f"# Indexing API EU concelhos — {log['started_at']}",
        f"",
        f"- **Total URLs**: {log['n_targets']}",
        f"- **OK (200)**: {log['stats']['ok']}",
        f"- **FAIL**: {log['stats']['fail']}",
        f"- **Service account**: `{log.get('service_account', '?')}`",
        f"- **Mode**: {'DRY-RUN' if dry else 'REAL'}",
        f"- **Started**: {log['started_at']}",
        f"- **Ended**: {log.get('ended_at', '')}",
        f"",
        "## Per-URL status",
        "",
    ]
    for s in log["submissions"]:
        body_str = json.dumps(s["body"])[:200] if s["body"] else ""
        md_lines.append(f"- `{s['status']}` — `{s['url']}`")
    md_lines.append("")
    md_lines.append(f"_Tâche Kanban: t_8d3cbf2a. PR draft #147._")
    with open(LOG_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"\nWROTE: {LOG_JSON}")
    print(f"WROTE: {LOG_MD}")
    print(f"STATS: {log['stats']}")
    return 0 if log["stats"]["fail"] == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
