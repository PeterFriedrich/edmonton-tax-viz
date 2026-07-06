"""Download the raw open-data inputs the pipeline needs, into ``data/raw/``.

This is the CI/runner's "fetch" step (see docs/SPEC_deployment.md): a fresh
GitHub Actions VM has none of the raw inputs, so it must pull them before
``main.py`` can regenerate the map. Run locally the same way to refresh a
snapshot.

Seven inputs come from Edmonton's Socrata open-data portal:
  - assessment     q7d6-ambg  (Property Assessment Data, current year)  -> CSV
  - boundaries     65fr-66s6  (Neighbourhood Boundaries)                -> GeoJSON
  - zoning         fixa-tstc  (Zoning Bylaw Geographical Data)          -> GeoJSON
  - roads          9j8t-zm52  (Road Network centrelines)                -> GeoJSON
  - property_info  dkk9-cj3x  (Property Info: lot size / zoning /
                               year built, current year)                -> CSV
  - fire_events    7hsn-idqi  (Fire Response, current + historical)     -> CSV
  - fire_stations  b4y7-zhnz  (Fire Stations: 31 points)                -> CSV

Mill rates (pwis-wc4c) are NOT fetched here — they live in the committed
``data/mill_rates.json`` (see DATA.md); refreshing them for a new year is a
manual, reviewed step because the year must align with the assessment roll.

Every download is verified against truncation two ways (see
docs/FINDINGS_data_integrity_audit.md, the $limit truncation risk):
  1. GeoJSON sources carry an explicit ``limit`` (the URL's $limit): Socrata
     truncates silently at $limit, returning exactly that many features, so a
     post-download count >= limit fails the run. Works offline; catches OUR
     limit going stale as a dataset grows.
  2. All sources carry a ``count_url`` ($select=count(*)): the post-download
     record count must equal the live server count exactly. Catches
     truncation by any limit that isn't ours — historically SODA 2.0 capped
     $limit at 50,000 server-side (this endpoint demonstrably doesn't today:
     roads returned 53,720 in one request, 2026-07-01), and a platform cap
     could (re)appear without touching our config. The count fetch itself
     fails SOFT (warn + proceed — the guard must not add fragility, same
     principle as check_year_alignment); a count MISMATCH fails hard.

Usage:
    python scripts/download_data.py                 # fetch all inputs
    python scripts/download_data.py --only zoning   # fetch one (repeatable)
"""

import argparse
import csv
import json
import logging
import sys
from pathlib import Path

import requests

logger = logging.getLogger(__name__)

RAW = Path(__file__).resolve().parent.parent / "data" / "raw"

# Each input: the Socrata download URL + the local filename main.py expects.
# GeoJSON exports use the resource endpoint with an explicit $limit above the
# feature count (Socrata paginates at 1,000 by default and truncates silently).
# ``limit`` must match the URL's $limit — it drives the truncation check.
def _count_url(dataset_id: str) -> str:
    return f"https://data.edmonton.ca/resource/{dataset_id}.json?$select=count(*)"


SOURCES = {
    "assessment": {
        # Full-export endpoint, no $limit — only the server cross-check applies.
        "url": "https://data.edmonton.ca/api/views/q7d6-ambg/rows.csv?accessType=DOWNLOAD",
        "dest": RAW / "Property_Assessment_Data__Current_Calendar_Year_.csv",
        "count_url": _count_url("q7d6-ambg"),
    },
    "boundaries": {
        "url": "https://data.edmonton.ca/resource/65fr-66s6.geojson?$limit=500",
        "dest": RAW / "neighbourhoods.geojson",
        "limit": 500,  # 407 neighbourhoods as of 2026-07
        "count_url": _count_url("65fr-66s6"),
    },
    "zoning": {
        "url": "https://data.edmonton.ca/resource/fixa-tstc.geojson?$limit=20000",
        "dest": RAW / "zoning.geojson",
        "limit": 20000,  # 11,510 features as of 2026-06
        "count_url": _count_url("fixa-tstc"),
    },
    "roads": {
        "url": "https://data.edmonton.ca/resource/9j8t-zm52.geojson?$limit=100000",
        "dest": RAW / "roads.geojson",
        "limit": 100000,  # 53,720 centrelines as of 2026-07 (SPEC_services.md)
        "count_url": _count_url("9j8t-zm52"),
    },
    "property_info": {
        # Full-export endpoint, no $limit — only the server cross-check applies.
        # Lot size / zoning / year built per account (DATA.md §2); joins the
        # assessment roll on account number. 439,685 rows as of 2026-07.
        "url": "https://data.edmonton.ca/api/views/dkk9-cj3x/rows.csv?accessType=DOWNLOAD",
        "dest": RAW / "Property_Info__Current_Calendar_Year_.csv",
        "count_url": _count_url("dkk9-cj3x"),
    },
    "fire_events": {
        # Fire lens (SPEC_services.md "Fire lens"): dispatched events with the
        # neighbourhood pre-joined. Resource endpoint (snake_case API headers,
        # which load_fire keys on), all columns — the dataset grows ~65k/yr,
        # so the $limit has decades of headroom.
        "url": "https://data.edmonton.ca/resource/7hsn-idqi.csv?$limit=2000000",
        "dest": RAW / "fire_response.csv",
        "limit": 2000000,  # 947,781 events as of 2026-07 (2011–mid-2026)
        "count_url": _count_url("7hsn-idqi"),
    },
    "fire_stations": {
        # 31 station points — context dots in the Services view's fire layer.
        "url": "https://data.edmonton.ca/resource/b4y7-zhnz.csv?$limit=500",
        "dest": RAW / "fire_stations.csv",
        "limit": 500,  # 31 stations as of 2026-07
        "count_url": _count_url("b4y7-zhnz"),
    },
}


def feature_count(path: Path) -> int:
    """Number of features in a GeoJSON FeatureCollection on disk."""
    with open(path, encoding="utf-8") as f:
        return len(json.load(f)["features"])


def csv_record_count(path: Path) -> int:
    """Number of data records in a CSV (excluding the header row).

    Uses the csv reader, not line counting — quoted fields may legally contain
    newlines (they don't in today's assessment export, but this stays correct
    if that changes).
    """
    with open(path, newline="", encoding="utf-8") as f:
        return max(0, sum(1 for _ in csv.reader(f)) - 1)


def local_count(path: Path) -> int:
    """Record count of a downloaded file, by format."""
    if path.suffix == ".geojson":
        return feature_count(path)
    return csv_record_count(path)


def server_count(count_url: str, timeout: int = 30) -> int | None:
    """The dataset's live row count via $select=count(*).

    Fails SOFT: any error (network, schema) returns None — the cross-check is
    skipped with a warning rather than making the download step more fragile.
    """
    try:
        r = requests.get(count_url, timeout=timeout)
        r.raise_for_status()
        return int(r.json()[0]["count"])
    except Exception as exc:  # noqa: BLE001 — deliberate soft-fail, see docstring
        logger.warning("count(*) fetch failed (%s) — skipping cross-check", exc)
        return None


def check_not_truncated(name: str, count: int, limit: int) -> None:
    """Fail loudly if a GeoJSON download hit its Socrata $limit.

    Socrata returns exactly ``limit`` features when the dataset outgrows it —
    a silently incomplete file, not an error.
    """
    if count >= limit:
        raise RuntimeError(
            f"{name}: {count} features == $limit={limit} — download almost certainly "
            f"truncated. Raise the $limit (and this source's 'limit') in SOURCES."
        )
    logger.info("%s: %d features (< $limit=%d, not truncated)", name, count, limit)


def verify_download(name: str, src: dict) -> None:
    """Post-download integrity checks: our-$limit check, then server count(*).

    A server-count MISMATCH raises (that IS truncation/incompleteness, whoever's
    limit caused it); an UNAVAILABLE server count only warns (soft-fail).
    """
    n = local_count(src["dest"])
    if "limit" in src:
        check_not_truncated(name, n, src["limit"])
    if "count_url" in src:
        expected = server_count(src["count_url"])
        if expected is None:
            logger.warning("%s: server count unavailable — local count %d unverified", name, n)
        elif n != expected:
            raise RuntimeError(
                f"{name}: downloaded {n} records but the server reports {expected} "
                f"— incomplete download (server-side limit or interrupted export)."
            )
        else:
            logger.info("%s: %d records == server count(*) — complete", name, n)


def download(url: str, dest: Path, timeout: int = 300) -> int:
    """Stream ``url`` to ``dest``, returning bytes written. Raises on HTTP error."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    logger.info("Downloading %s -> %s", url, dest.name)
    written = 0
    with requests.get(url, stream=True, timeout=timeout) as r:
        r.raise_for_status()
        # Write to a temp sibling first so a mid-stream failure can't leave a
        # truncated file where main.py would read it as complete.
        tmp = dest.with_suffix(dest.suffix + ".part")
        with open(tmp, "wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 16):
                if chunk:
                    written += len(chunk)
                    f.write(chunk)
        tmp.replace(dest)
    logger.info("Wrote %s (%.1f MB)", dest.name, written / 1e6)
    return written


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument(
        "--only",
        action="append",
        choices=sorted(SOURCES),
        help="download only this input (repeatable); default is all of them",
    )
    p.add_argument("--log-level", default="INFO")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    logging.basicConfig(
        stream=sys.stdout,
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(levelname)s: %(message)s",
    )
    wanted = args.only or list(SOURCES)
    failures = []
    for name in wanted:
        src = SOURCES[name]
        try:
            download(src["url"], src["dest"])
            verify_download(name, src)
        except Exception as exc:  # noqa: BLE001 — report every input, don't stop at the first
            logger.error("FAILED to download %s: %s", name, exc)
            failures.append(name)
    if failures:
        raise SystemExit(f"Download failed for: {', '.join(failures)}")
    logger.info("All downloads complete (%d input(s)).", len(wanted))


if __name__ == "__main__":
    main()
