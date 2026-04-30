#!/usr/bin/env python3
"""
snapshot.py — Pre-bake all live API endpoints into static JSON files.

Usage:
    # Against local skills server (default)
    python scripts/snapshot.py

    # Against a specific skills API URL
    SKILLS_API_URL=https://mobius-skills-xxx-uc.a.run.app python scripts/snapshot.py

Output: public/data/snapshot/*.json
Each file is named after the endpoint slug so apiFetch() can load it in static mode.

Run this before every release to update the snapshot.
"""

import json
import sys
import os
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError
from urllib.parse import urlencode

SKILLS_API = os.environ.get("SKILLS_API_URL", "http://localhost:8011")
OUT_DIR = Path(__file__).resolve().parent.parent / "public" / "data" / "snapshot"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Endpoints to snapshot ──────────────────────────────────────────────────────
# Each entry: (slug, method, path, params_or_body)
#   slug      → filename: public/data/snapshot/{slug}.json
#   method    → GET or POST
#   path      → relative to SKILLS_API
#   params    → dict (GET query params) or body (POST JSON)
ENDPOINTS = [
    # Fact-pack: key scopes the app requests
    ("fact-pack__bhpf__all",      "GET", "/story/fact-pack", {"scope": "bhpf"}),
    ("fact-pack__fbha__all",      "GET", "/story/fact-pack", {"scope": "fbha"}),
    ("fact-pack__all_cmhc__all",  "GET", "/story/fact-pack", {"scope": "all_cmhc"}),
    # lookalike / fqhc / community_bh scopes not yet supported by API — skip for now

    # Widgets
    ("widget__rate-codes",        "GET", "/story/widget/rate-codes",        {"top": "10"}),
    ("widget__service-line-share","GET", "/story/widget/service-line-share", {}),
    ("widget__org-ranking",       "GET", "/story/widget/org-ranking",        {"top": "15"}),
]


def fetch(method, path, params=None):
    url = f"{SKILLS_API}{path}"
    if method == "GET" and params:
        url = f"{url}?{urlencode(params)}"
    req = Request(url, method=method)
    req.add_header("Accept", "application/json")
    if method == "POST" and params:
        body = json.dumps(params).encode()
        req.add_header("Content-Type", "application/json")
        req.data = body
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def main():
    ok, failed = 0, []
    for slug, method, path, params in ENDPOINTS:
        out_path = OUT_DIR / f"{slug}.json"
        print(f"  {method:4s} {path}  {'?' + urlencode(params) if params else ''}", end="  ")
        try:
            data = fetch(method, path, params)
            out_path.write_text(json.dumps(data, indent=2, default=str))
            print(f"→ {out_path.name} ({out_path.stat().st_size // 1024}KB)")
            ok += 1
        except URLError as e:
            print(f"FAILED: {e}")
            failed.append(slug)
        except Exception as e:
            print(f"ERROR: {e}")
            failed.append(slug)

    # Write a manifest so the browser knows what's available
    manifest = {
        "generated": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        "skills_api": SKILLS_API,
        "snapshots": [e[0] for e in ENDPOINTS if e[0] not in failed],
        "failed": failed,
    }
    (OUT_DIR / "_manifest.json").write_text(json.dumps(manifest, indent=2))

    print(f"\n✓ {ok}/{len(ENDPOINTS)} endpoints snapshotted → {OUT_DIR}")
    if failed:
        print(f"✗ Failed: {', '.join(failed)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
