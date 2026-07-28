"""Download the raw open-data inputs the pipeline needs, into ``data/raw/``.

This is the CI/runner's "fetch" step (see docs/SPEC_deployment.md): a fresh
GitHub Actions VM has none of the raw inputs, so it must pull them before
``main.py`` can regenerate the map. Run locally the same way to refresh a
snapshot.

Twelve inputs come from Edmonton's Socrata open-data portal:
  - assessment     q7d6-ambg  (Property Assessment Data, current year)  -> CSV
  - boundaries     65fr-66s6  (Neighbourhood Boundaries)                -> GeoJSON
  - zoning         fixa-tstc  (Zoning Bylaw Geographical Data)          -> GeoJSON
  - roads          9j8t-zm52  (Road Network centrelines)                -> GeoJSON
  - property_info  dkk9-cj3x  (Property Info: lot size / zoning /
                               year built, current year)                -> CSV
  - fire_events    7hsn-idqi  (Fire Response, current + historical)     -> CSV
  - fire_stations  b4y7-zhnz  (Fire Stations: 31 points)                -> CSV
  - gtfs_stops     4vt2-8zrq  (ETS GTFS: stops)                         -> CSV
  - gtfs_routes    d577-xky7  (ETS GTFS: routes)                        -> CSV
  - gtfs_trips     ctwr-tvrd  (ETS GTFS: trips, slim $select)           -> CSV
  - gtfs_stop_times greh-g7ac (ETS GTFS: stop times, slim $select)      -> CSV
  - gtfs_calendar_dates f2sy-bth7 (ETS GTFS: calendar dates)            -> CSV
  - permits        24uj-dj8v  (General Building Permits, slim $select)   -> CSV

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
import time
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
        # Socrata generates this ~54k-feature GeoJSON server-side before sending
        # the first byte; the default 300s read timeout has failed on the tail
        # (run 28976864116, 2026-07-08). Give the slow endpoint real headroom.
        "timeout": 900,
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
    # Transit lens (SPEC_services.md "Transit lens"): the ETS GTFS static
    # feed, published as individual Socrata tables (the zip bundle is an
    # href-only page). Trips and stop_times use $select to fetch only the
    # keyed columns — trips otherwise carries a per-trip geometry_line that
    # dominates the file, and stop_times is 1.7M rows. $select does not
    # change the row count, so both truncation guards still apply.
    "gtfs_stops": {
        "url": "https://data.edmonton.ca/resource/4vt2-8zrq.csv?$limit=20000",
        "dest": RAW / "gtfs_stops.csv",
        "limit": 20000,  # 6,882 stops as of 2026-07
        "count_url": _count_url("4vt2-8zrq"),
    },
    "gtfs_routes": {
        "url": "https://data.edmonton.ca/resource/d577-xky7.csv?$limit=2000",
        "dest": RAW / "gtfs_routes.csv",
        "limit": 2000,  # 238 routes as of 2026-07
        "count_url": _count_url("d577-xky7"),
    },
    "gtfs_trips": {
        "url": (
            "https://data.edmonton.ca/resource/ctwr-tvrd.csv"
            "?$select=trip_id,route_id,service_id&$limit=300000"
        ),
        "dest": RAW / "gtfs_trips.csv",
        "limit": 300000,  # 56,812 trips as of 2026-07
        "count_url": _count_url("ctwr-tvrd"),
    },
    "gtfs_stop_times": {
        "url": (
            "https://data.edmonton.ca/resource/greh-g7ac.csv"
            "?$select=trip_id,stop_id&$limit=5000000"
        ),
        "dest": RAW / "gtfs_stop_times.csv",
        "limit": 5000000,  # 1,744,051 stop-time rows as of 2026-07
        "count_url": _count_url("greh-g7ac"),
        # Big table; give the server generation time headroom like roads.
        "timeout": 900,
    },
    "gtfs_calendar_dates": {
        "url": "https://data.edmonton.ca/resource/f2sy-bth7.csv?$limit=50000",
        "dest": RAW / "gtfs_calendar_dates.csv",
        "limit": 50000,  # 9,248 (service_id, date) rows as of 2026-07
        "count_url": _count_url("f2sy-bth7"),
    },
    "permits": {
        # Development & Infill lens A (docs/SPEC_development.md): issued
        # building permits, one row per permit. Slim $select — we need only
        # the filter/join/numerator columns, not the 34-column full schema
        # (construction_value, geometry_point, etc.). $select does NOT change
        # the row count, so both truncation guards still apply. UPPERCASE
        # `neighbourhood` matches our neighbourhood_name format.
        # latitude/longitude (added 2026-07-15) feed the 100 m dev-grid
        # detail layer (load_permits.export_dev_grid); recent permits lag
        # geocoding — nulls are reported, never silently dropped (DATA.md §10).
        "url": (
            "https://data.edmonton.ca/resource/24uj-dj8v.csv"
            "?$select=year,issue_date,work_type,building_type,units_added,"
            "neighbourhood,latitude,longitude"
            "&$limit=1000000"
        ),
        "dest": RAW / "building_permits.csv",
        "limit": 1000000,  # 243,371 permits as of 2026-07-12 (2009→present)
        "count_url": _count_url("24uj-dj8v"),
    },
    "assessment_historical": {
        # Temporal lens (docs/SPEC_temporal.md): assessed value per
        # neighbourhood per year, 2012-present. The raw dataset is 5.5M rows, so
        # this fetches the SERVER-SIDE AGGREGATE instead -- ~14,800 rows keyed
        # (year, hood, mill class), which is the whole reason this lens is cheap.
        # The class dimension is what makes the commercial-base denominator
        # available (SPEC_temporal.md section 6); it costs ~9,300 extra rows.
        #
        # $order is not optional decoration: Socrata's paging is undefined
        # without it, and a grouped query is exactly where a silently reordered
        # page would lose members.
        "url": (
            "https://data.edmonton.ca/resource/qi6a-xuwt.csv"
            "?$select=assessment_year,neighbourhood_name,mill_class_1,"
            "count(*) as n_accounts,sum(assessed_value) as total_assessed_value"
            "&$group=assessment_year,neighbourhood_name,mill_class_1"
            "&$order=assessment_year,neighbourhood_name,mill_class_1"
            "&$limit=200000"
        ),
        "dest": RAW / "assessment_historical_by_hood.csv",
        "limit": 200000,  # 14,842 groups as of 2026-07-28
        # The generic count(*) cross-check compares ROW counts, which is
        # meaningless for an aggregate (14,842 groups vs 5.5M rows). This
        # stronger check replaces it: every source row lands in exactly one
        # group, so the n_accounts column must sum to the dataset's live row
        # count. That catches a dropped GROUP, which a row count never would.
        "sum_column": "n_accounts",
        "count_url": _count_url("qi6a-xuwt"),
    },
    "lrt_routes": {
        # LRT track lines — a context layer under the transit lens (the LRT
        # station dots' companion), NOT part of the stop-events metric. Four
        # named route multilines; the loader drops the HER heritage streetcar
        # (not ETS LRT service, absent from the GTFS we count). GeoJSON.
        "url": "https://data.edmonton.ca/resource/rpjw-4jft.geojson?$limit=500",
        "dest": RAW / "lrt_routes.geojson",
        "limit": 500,  # 4 routes as of 2026-07
        "count_url": _count_url("rpjw-4jft"),
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


def csv_column_sum(path: Path, column: str) -> int:
    """Sum an integer column across a CSV — the aggregate sources' row-conservation check.

    For a ``$group`` download the file's row count is the number of GROUPS, so it
    can never equal the dataset's count(*). What must hold instead is that every
    source row landed in exactly one group: the per-group counts sum to the live
    row count. That is a strictly stronger check than the row comparison it
    replaces — it also catches a whole group going missing.
    """
    with open(path, newline="", encoding="utf-8") as f:
        rows = csv.DictReader(f)
        if column not in (rows.fieldnames or []):
            raise RuntimeError(
                f"{path.name}: no '{column}' column to sum (has {rows.fieldnames}) "
                "— the $select in SOURCES and this source's 'sum_column' disagree."
            )
        return sum(int(float(r[column])) for r in rows if r[column])


def server_count(count_url: str, timeout: int = 30) -> int | None:
    """The dataset's live row count via $select=count(*).

    Fails SOFT: any error (network, schema) returns None — the cross-check is
    skipped with a warning rather than making the download step more fragile.
    """
    try:
        r = requests.get(count_url, timeout=timeout)
        r.raise_for_status()
        # count(*) returns one row with one column, but Socrata aliases it
        # inconsistently across datasets ("count" on roads, "count_1" on the
        # permits dataset 24uj-dj8v). Read the sole value rather than keying on
        # a fixed name, so the cross-check works everywhere.
        return int(next(iter(r.json()[0].values())))
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
        # Aggregate sources compare a SUM of per-group counts, not the row count
        # (see csv_column_sum); everything else compares rows directly.
        if "sum_column" in src:
            got, unit = csv_column_sum(src["dest"], src["sum_column"]), \
                f"source rows across {n} groups"
        else:
            got, unit = n, "records"
        if expected is None:
            logger.warning("%s: server count unavailable — local count %d unverified", name, n)
        elif got != expected:
            raise RuntimeError(
                f"{name}: downloaded {got} {unit} but the server reports {expected} "
                f"— incomplete download (server-side limit or interrupted export)."
            )
        else:
            logger.info("%s: %d %s == server count(*) — complete", name, got, unit)


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


def download_with_retry(
    url: str, dest: Path, timeout: int = 300, attempts: int = 3, backoff: int = 10
) -> int:
    """``download`` with retry-on-failure, for transient portal blips.

    The read timeout (server generation time) is handled by ``timeout``; this
    wrapper covers *transient* failures — dropped connections, a one-off slow
    tail — by re-attempting with linear backoff. A persistently slow endpoint
    should get a larger ``timeout`` (see the roads source), not more attempts.
    """
    last: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            return download(url, dest, timeout=timeout)
        except Exception as exc:  # noqa: BLE001 — retry any download failure
            last = exc
            if attempt < attempts:
                wait = backoff * attempt
                logger.warning(
                    "download attempt %d/%d failed (%s) — retrying in %ds",
                    attempt, attempts, exc, wait,
                )
                time.sleep(wait)
    assert last is not None  # loop ran >= 1 time
    raise last


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
            download_with_retry(src["url"], src["dest"], timeout=src.get("timeout", 300))
            verify_download(name, src)
        except Exception as exc:  # noqa: BLE001 — report every input, don't stop at the first
            logger.error("FAILED to download %s: %s", name, exc)
            failures.append(name)
    if failures:
        raise SystemExit(f"Download failed for: {', '.join(failures)}")
    logger.info("All downloads complete (%d input(s)).", len(wanted))


if __name__ == "__main__":
    main()
