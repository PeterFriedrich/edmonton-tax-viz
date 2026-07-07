"""Scrape Edmonton Direct Control (DC) provision bylaw pages.

ANALYSIS_BACKLOG.md item 3. The zoning GeoJSON's ``url`` field points at a
per-site bylaw page for each DC provision (dc1-19431, dc2-277, …); each page's
``<main>`` region carries a Purpose statement + permitted uses that
``load_zoning.py`` cannot infer from the DC code alone. This fetches the
distinct DC pages politely and caches the raw HTML to disk so downstream
extraction (tools/extract_dc_uses.py) and classification can run offline and
re-runs can diff against the cached corpus rather than re-crawling.

Polite + resumable: sequential, rate-limited, skips pages already cached, one
retry on failure. Cache + manifest live under data/raw/ (gitignored). Run from
the repo root:

    python scripts/scrape_dc_provisions.py            # full corpus (~938 pages)
    python scripts/scrape_dc_provisions.py --limit 5  # smoke test
"""
from __future__ import annotations

import argparse
import csv
import logging
import re
import time
from pathlib import Path

import geopandas as gpd
import requests

ZONING = "data/raw/zoning.geojson"
CACHE = Path("data/raw/dc_provisions")
MANIFEST = CACHE / "_manifest.csv"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")
DELAY_S = 0.8      # polite gap between requests (city Drupal app, not a bulk API)
TIMEOUT_S = 30
MIN_BYTES = 2000   # anything smaller is an error page, not a provision

log = logging.getLogger("scrape_dc")


def slug_for(url: str) -> str:
    """Last path segment -> safe filename stem (e.g. .../dc1-19431 -> dc1-19431)."""
    seg = url.rstrip("/").rsplit("/", 1)[-1]
    return re.sub(r"[^a-z0-9._-]", "_", seg.lower()) or "index"


def dc_urls() -> list[tuple[str, str]]:
    """Distinct (url, agreement_no) for every DC-coded zoning polygon."""
    g = gpd.read_file(ZONING)
    dc = g[g["zoning"].astype(str).str.upper().str.startswith("DC")]
    pairs = (dc[["url", "agreement_no"]]
             .dropna(subset=["url"])
             .drop_duplicates(subset=["url"])
             .itertuples(index=False, name=None))
    return sorted(pairs)


def fetch(session: requests.Session, url: str) -> bytes | None:
    for attempt in (1, 2):
        try:
            r = session.get(url, timeout=TIMEOUT_S)
            if r.status_code == 200 and len(r.content) >= MIN_BYTES:
                return r.content
            log.warning("  %s -> HTTP %d (%d bytes)", url, r.status_code, len(r.content))
        except requests.RequestException as e:
            log.warning("  %s -> %s (attempt %d)", url, e, attempt)
        if attempt == 1:
            time.sleep(2.0)
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None, help="fetch at most N (smoke test)")
    ap.add_argument("--delay", type=float, default=DELAY_S)
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    CACHE.mkdir(parents=True, exist_ok=True)
    targets = dc_urls()
    if args.limit:
        targets = targets[: args.limit]
    log.info("DC provisions to ensure cached: %d", len(targets))

    session = requests.Session()
    session.headers.update({"User-Agent": UA})

    rows, fetched, cached, failed = [], 0, 0, []
    for i, (url, agreement) in enumerate(targets, 1):
        stem = slug_for(url)
        path = CACHE / f"{stem}.html"
        if path.exists() and path.stat().st_size >= MIN_BYTES:
            cached += 1
            rows.append((url, agreement, stem, "cached", path.stat().st_size))
            continue
        content = fetch(session, url)
        if content is None:
            failed.append(url)
            rows.append((url, agreement, stem, "FAILED", 0))
        else:
            path.write_bytes(content)
            fetched += 1
            rows.append((url, agreement, stem, "fetched", len(content)))
            time.sleep(args.delay)
        if i % 50 == 0:
            log.info("  %d/%d  (fetched %d, cached %d, failed %d)",
                     i, len(targets), fetched, cached, len(failed))

    with open(MANIFEST, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["url", "agreement_no", "slug", "status", "bytes"])
        w.writerows(rows)

    log.info("done: %d fetched, %d already cached, %d failed", fetched, cached, len(failed))
    if failed:
        log.warning("FAILED (%d) — re-run to retry: %s", len(failed), failed[:10])


if __name__ == "__main__":
    main()
