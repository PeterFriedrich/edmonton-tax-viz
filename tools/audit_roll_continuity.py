"""Audit: which properties have FALLEN OUT of the current assessment roll?

The current roll (``q7d6-ambg``) is a snapshot, and a property can vanish from it
while still existing and still being assessed. Misericordia Community Hospital
did exactly that: continuously on the roll since 2012 as account ``10095840``
(~$200-260M, always WEST MEADOWLARK PARK), it was renumbered to ``11495573`` and
was **absent from the published current roll** until 2026-08-03, when it
reappeared and that neighbourhood's revenue jumped +130%. The map understated
the hood for as long as the gap lasted.

⚠️ THE HARD PART IS THAT EVERY IDENTIFIER IN THESE DATASETS CHURNS, so a
continuity check built on any one of them measures churn and calls it loss:

  * ``account_number`` — renumbered. All four major hospitals moved into a new
    ``114955xx`` block; their old numbers are gone from the current roll and
    their new ones appear in NO year of the historical roll.
  * address — re-addressed. ``WESTMOUNT SHOPPING CENTRE NW`` no longer exists as
    a street name at all.
  * ``neighbourhood`` — renamed. OLIVER -> WÎHKWÊNTÔWIN moved 12,237 parcels, and
    a per-hood value comparison reads that as **-100%**.

⚠️ **Renumbering is ROUTINE, not an anomaly** — measured year-over-year in the
historical roll, accounts vanish at 0.15%-0.37% per year (2023->2024 spikes to
0.91%, 3,893 accounts). So this audit cannot treat a vanished account number as
a finding; it has to look past the identifier entirely.

WHAT IS STABLE IS POSITION. Across the hospital renumbering the coordinates moved
by **under two metres** (Royal Alexandra 1.3m, Grey Nuns 1.6m, Misericordia 0.7m,
Cross Cancer 0.6m). So this matches historical parcels to current ones
**spatially**, and is immune to all three churn mechanisms by construction.

(``legal_description`` — plan/block/lot — would be a better key still, and is
genuinely immutable. It exists ONLY in the historical roll, not in ``q7d6-ambg``,
so it cannot join the two. Noted so nobody re-derives that dead end.)

⚠️ WHAT THIS PRODUCES IS CANDIDATES, NOT VERDICTS. A demolished parcel, a
subdivision, or a consolidation legitimately has no 1:1 successor and will be
flagged. A single run also cannot distinguish a transient renumber gap from a
permanent removal — that needs two runs separated in time. Read the output as
"these are worth a look", the same contract as ``check_revenue_deltas.py``.

Reproduce:  .venv/bin/python tools/audit_roll_continuity.py
            .venv/bin/python tools/audit_roll_continuity.py --year 2023 --tolerance-m 10
"""

import argparse
import json
import logging
import pathlib
import sys

import geopandas as gpd
import pandas as pd
import requests

logger = logging.getLogger(__name__)

HISTORICAL = "https://data.edmonton.ca/resource/qi6a-xuwt.json"
CURRENT = "https://data.edmonton.ca/resource/q7d6-ambg.json"

# Same projected CRS the pipeline uses for all distance/area math (src/*.py).
METRIC_CRS = "EPSG:3400"

# Default comparison year: the most recent COMPLETE historical slice. 2025 is
# excluded on purpose — SPEC_temporal.md §0 documents that slice as proven
# incomplete, and comparing against it would manufacture dropouts.
DEFAULT_YEAR = 2024

PAGE = 50_000


def fetch(url: str, select: str, where: str | None = None,
          cache_dir: pathlib.Path | None = None, tag: str = "") -> pd.DataFrame:
    """Page a Socrata resource. Cached on disk — these are 400k-row pulls."""
    if cache_dir:
        cached = cache_dir / f"{tag}.json"
        if cached.exists():
            return pd.DataFrame(json.loads(cached.read_text()))
    rows: list[dict] = []
    offset = 0
    while True:
        params = {"$select": select, "$limit": PAGE, "$offset": offset}
        if where:
            params["$where"] = where
        batch = requests.get(url, params=params, timeout=300).json()
        rows += batch
        offset += len(batch)
        logger.info("  %s: %d rows", tag or url, offset)
        if len(batch) < PAGE:
            break
    if cache_dir:
        (cache_dir / f"{tag}.json").write_text(json.dumps(rows))
    return pd.DataFrame(rows)


def to_points(df: pd.DataFrame) -> gpd.GeoDataFrame:
    """Drop rows without coordinates and project to the metric CRS.

    No silent drops: the caller logs how many rows had no position, because a
    parcel with no coordinate cannot be matched and would otherwise read as a
    dropout it is not.
    """
    df = df.copy()
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df["assessed_value"] = pd.to_numeric(df["assessed_value"], errors="coerce")
    located = df.dropna(subset=["latitude", "longitude"])
    gdf = gpd.GeoDataFrame(
        located,
        geometry=gpd.points_from_xy(located["longitude"], located["latitude"]),
        crs="EPSG:4326",
    )
    return gdf.to_crs(METRIC_CRS)


def unmatched(historical: gpd.GeoDataFrame, current: gpd.GeoDataFrame,
              tolerance_m: float) -> gpd.GeoDataFrame:
    """Historical parcels with no current-roll parcel within ``tolerance_m``.

    ``sjoin_nearest`` rather than an exact join: the coordinates drift by up to
    ~2m across a renumbering, so an equality match on rounded lat/lon would
    report every renumbered parcel as missing — the exact false positive this
    audit exists to avoid.
    """
    joined = gpd.sjoin_nearest(
        historical, current[["geometry"]], how="left",
        max_distance=tolerance_m, distance_col="_dist",
    )
    joined = joined[~joined.index.duplicated(keep="first")]
    return joined[joined["index_right"].isna()].drop(columns=["index_right", "_dist"])


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--year", type=int, default=DEFAULT_YEAR,
                   help=f"historical assessment year to compare (default {DEFAULT_YEAR})")
    p.add_argument("--tolerance-m", type=float, default=5.0,
                   help="a historical parcel counts as present if a current parcel "
                        "is within this many metres (default 5)")
    p.add_argument("--min-value", type=float, default=0.0,
                   help="only report parcels assessed above this (default 0 = all)")
    p.add_argument("--top", type=int, default=25)
    p.add_argument("--cache-dir", type=pathlib.Path, default=pathlib.Path("/tmp/roll_continuity"))
    p.add_argument("--log-level", default="INFO")
    args = p.parse_args(argv)
    logging.basicConfig(stream=sys.stdout, level=getattr(logging, args.log_level.upper()),
                        format="%(levelname)s: %(message)s")
    args.cache_dir.mkdir(parents=True, exist_ok=True)

    if args.year >= 2025:
        logger.warning(
            "Year %d: the 2025 historical slice is PROVEN INCOMPLETE "
            "(SPEC_temporal.md §0). Dropouts found against it are not trustworthy.",
            args.year,
        )

    hist_raw = fetch(HISTORICAL,
                     "account_number,house_number,street_name,neighbourhood_name,"
                     "assessed_value,latitude,longitude",
                     f"assessment_year='{args.year}'", args.cache_dir, f"hist{args.year}")
    cur_raw = fetch(CURRENT, "account_number,assessed_value,latitude,longitude",
                    None, args.cache_dir, "current")

    hist, cur = to_points(hist_raw), to_points(cur_raw)
    logger.info("historical %d: %d rows, %d with coordinates (%d unlocatable)",
                args.year, len(hist_raw), len(hist), len(hist_raw) - len(hist))
    logger.info("current roll: %d rows, %d with coordinates (%d unlocatable)",
                len(cur_raw), len(cur), len(cur_raw) - len(cur))

    gone = unmatched(hist, cur, args.tolerance_m)
    if args.min_value:
        gone = gone[gone["assessed_value"] >= args.min_value]

    total_val = hist["assessed_value"].sum()
    gone_val = gone["assessed_value"].sum()
    print(f"\n=== ROLL CONTINUITY: historical {args.year} vs the live current roll ===")
    print(f"matched within {args.tolerance_m:.0f} m; position-based, so renumbering, "
          f"re-addressing and hood renames do NOT register")
    print(f"\n  historical {args.year}:  {len(hist):>7,} located parcels  ${total_val:>16,.0f}")
    print(f"  no current match:  {len(gone):>7,} parcels ({len(gone)/len(hist)*100:.2f}%)"
          f"  ${gone_val:>16,.0f} ({gone_val/total_val*100:.2f}%)")

    if gone.empty:
        print("\n  Nothing unmatched. The current roll covers every located historical parcel.")
        return 0

    print(f"\n--- largest unmatched parcels (top {args.top}) ---")
    cols = ["account_number", "house_number", "street_name", "neighbourhood_name", "assessed_value"]
    top = gone.nlargest(args.top, "assessed_value")[cols]
    print(top.to_string(index=False, formatters={"assessed_value": lambda v: f"${v:,.0f}"}))

    print("\n--- by neighbourhood, by value at risk ---")
    by_hood = (gone.groupby("neighbourhood_name")["assessed_value"]
               .agg(parcels="size", value="sum").nlargest(15, "value"))
    for hood, row in by_hood.iterrows():
        print(f"  {str(hood):32s} {int(row.parcels):>6,} parcels  ${row.value:>15,.0f}")

    print("\n⚠️ CANDIDATES, NOT VERDICTS. Demolitions, subdivisions and "
          "consolidations legitimately have no 1:1 successor and appear here. A "
          "single run cannot tell a transient renumber gap from a permanent "
          "removal — re-run later and compare.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
