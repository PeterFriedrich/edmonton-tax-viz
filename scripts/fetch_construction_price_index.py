"""Fetch the Edmonton industrial building construction price index (the deflator).

The Development lens's industrial detail grid (docs/SPEC_industrial.md A3) draws
cell height from ``construction_value`` — the permit's *declared estimate of
construction work*. Summing that nominally across a 17-year window encodes
construction-cost inflation as if it were development: on this very series an
identical building permitted in 2009 draws a spike **1.72x shorter** than one
permitted in 2025. This script produces the deflator that removes it.

Source: Statistics Canada table **18-10-0289-01**, "Building construction price
indexes, by type of building and division", quarterly:

    https://www150.statcan.gc.ca/n1/tbl/csv/18100289-eng.zip

The one series we want (verified live 2026-08-18):

    GEO              Edmonton, Alberta
    Type of building Industrial buildings [62211]
    Division         Division composite
    UOM              Index, 2023=100
    VECTOR           v1617916332
    coverage         1981-Q1 -> 2026-Q2 (2009-2025 all four quarters)

**Two predecessor tables are ARCHIVED and must not be used**: 18-10-0135 ends
2022-Q2 and 18-10-0276 ends 2024-Q2. Both still download fine and still answer
queries -- they simply stop, so a stale pin would silently deflate recent years
by an out-of-date index. If this script's table goes archived too, the WDS
``getCubeMetadata`` endpoint reports ``archiveStatusEn``; the successor is
findable via ``getAllCubesListLite``.

This is a **manual, reviewed input** (mill-rates / FIR-debt pattern, DATA.md
sections 11 and 16): run it by hand when a year completes (~annually), eyeball
the diff on ``data/construction_price_index.json``, commit. It is NOT part of
the weekly refresh workflow -- a price index that silently moved would restate
every historical spike on the map at once.

Integrity rules (no silent data drops):
  - the dimension filter is by FULL STRING, and an empty result HARD-FAILS --
    that is how a StatCan dimension rename surfaces loudly instead of yielding
    an empty deflator table;
  - a year inside the emitted range missing any of its four quarters
    HARD-FAILS; the trailing partial year is EXCLUDED, not averaged (a
    two-quarter mean is not an annual index);
  - the base year must be complete, since every factor divides by it;
  - the emitted range must cover every year the permit windows can reach
    (PERMIT_START_YEAR..base), so a permit can never miss a deflator and get
    silently passed through at nominal value.

Usage:
    python scripts/fetch_construction_price_index.py
    python scripts/fetch_construction_price_index.py --base-year 2025
    python scripts/fetch_construction_price_index.py --keep-download  # debug
"""

from __future__ import annotations

import argparse
import io
import json
import logging
import sys
import urllib.request
import zipfile
from datetime import date
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

TABLE_ID = "18100289"
SOURCE_URL = f"https://www150.statcan.gc.ca/n1/tbl/csv/{TABLE_ID}-eng.zip"
CUBE_METADATA_URL = "https://www150.statcan.gc.ca/t1/wds/rest/getCubeMetadata"

# Full-string dimension filter — a rename must fail loudly, not silently match
# a neighbouring series (the load_permits building-type idiom).
SERIES = {
    "GEO": "Edmonton, Alberta",
    "Type of building": "Industrial buildings [62211]",
    "Division": "Division composite",
}
EXPECTED_VECTOR = "v1617916332"

# The permit windows in main.py start here; the deflator must reach back at
# least this far or a 2009 permit would silently ride at nominal value.
FIRST_YEAR = 2009
DEFAULT_BASE_YEAR = 2025

OUT_PATH = Path(__file__).resolve().parents[1] / "data" / "construction_price_index.json"


def _archive_status() -> str | None:
    """Report the cube's archive status, or None if the check can't run.

    Fails SOFT (the download itself is the real check) but a WARNING here is
    the early signal that this table has gone the way of 18-10-0135/0276.
    """
    try:
        req = urllib.request.Request(
            CUBE_METADATA_URL,
            data=json.dumps([{"productId": int(TABLE_ID)}]).encode(),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=30) as fh:
            obj = json.load(fh)[0].get("object", {})
        status = obj.get("archiveStatusEn")
        if status and "no longer being updated" in status:
            logger.warning(
                "StatCan table %s is ARCHIVED (%s), ending %s — find its successor "
                "via getAllCubesListLite before trusting this deflator",
                TABLE_ID, status.strip(), obj.get("cubeEndDate"),
            )
        return f"{status} (cube ends {obj.get('cubeEndDate')})" if status else \
            f"active (cube ends {obj.get('cubeEndDate')})"
    except Exception as exc:  # noqa: BLE001 — provenance nicety, never a blocker
        logger.warning("cube metadata check skipped (%s)", exc)
        return None


def fetch_index(base_year: int = DEFAULT_BASE_YEAR,
                keep_download: Path | None = None) -> dict:
    """Download, filter to the one series, and build the annual deflator table."""
    status = _archive_status()

    logger.info("Downloading StatCan %s (~4 MB zip)…", TABLE_ID)
    with urllib.request.urlopen(SOURCE_URL, timeout=300) as fh:
        blob = fh.read()
    if keep_download:
        Path(keep_download).write_bytes(blob)

    with zipfile.ZipFile(io.BytesIO(blob)) as zf:
        name = f"{TABLE_ID}.csv"
        if name not in zf.namelist():
            raise ValueError(
                f"{name} not in the downloaded zip ({zf.namelist()}) — StatCan "
                f"changed the bulk-CSV layout"
            )
        with zf.open(name) as csv_fh:
            df = pd.read_csv(
                csv_fh, low_memory=False,
                usecols=["REF_DATE", "GEO", "Type of building", "Division",
                         "UOM", "VECTOR", "VALUE"],
            )

    mask = pd.Series(True, index=df.index)
    for col, want in SERIES.items():
        if col not in df.columns:
            raise ValueError(
                f"dimension column {col!r} is gone from table {TABLE_ID} "
                f"(have {sorted(df.columns)}) — StatCan restructured the table"
            )
        mask &= df[col].astype("string").str.strip() == want
    series = df.loc[mask].copy()
    if not len(series):
        raise ValueError(
            f"no rows match {SERIES} in table {TABLE_ID} — a dimension VALUE was "
            f"renamed. Inspect the live values before editing SERIES; do not "
            f"loosen the match to the nearest label."
        )

    vectors = sorted(series["VECTOR"].dropna().astype(str).unique())
    if vectors != [EXPECTED_VECTOR]:
        # Not fatal: StatCan can re-issue a vector. But it must be recorded,
        # because a changed vector is how a *different* series slips in.
        logger.warning(
            "vector drift: expected %s, got %s — verify this is still the "
            "Edmonton industrial composite before committing",
            EXPECTED_VECTOR, vectors,
        )
    uom = sorted(series["UOM"].dropna().astype(str).unique())
    if len(uom) != 1:
        raise ValueError(f"series carries mixed units {uom} — cannot build a deflator")

    series["year"] = series["REF_DATE"].astype(str).str[:4].astype(int)
    series["VALUE"] = pd.to_numeric(series["VALUE"], errors="coerce")
    series = series.dropna(subset=["VALUE"])

    per_year = series.groupby("year")["VALUE"].agg(quarters="size", index="mean")

    # A partial trailing year is EXCLUDED, not averaged — a two-quarter mean is
    # not an annual index, and it would quietly bias the newest year.
    partial = per_year.index[per_year["quarters"] < 4].tolist()
    complete = per_year[per_year["quarters"] == 4]
    dropped_partial = [y for y in partial if y >= FIRST_YEAR]

    if base_year not in complete.index:
        raise ValueError(
            f"base year {base_year} is not complete in table {TABLE_ID} "
            f"(quarters present: {int(per_year['quarters'].get(base_year, 0))}). "
            f"Every factor divides by it, so pick a complete year with "
            f"--base-year (latest complete: {int(complete.index.max())})."
        )

    wanted = range(FIRST_YEAR, base_year + 1)
    missing = [y for y in wanted if y not in complete.index]
    if missing:
        raise ValueError(
            f"years {missing} have no complete index in table {TABLE_ID}; the "
            f"permit windows reach back to {FIRST_YEAR}, so a permit in those "
            f"years would have no deflator"
        )

    base_index = float(complete.loc[base_year, "index"])
    emitted = complete.loc[[y for y in wanted]]
    deflators = {
        str(int(y)): round(base_index / float(row["index"]), 6)
        for y, row in emitted.iterrows()
    }
    index_values = {
        str(int(y)): round(float(row["index"]), 4) for y, row in emitted.iterrows()
    }

    spread = max(deflators.values()) / min(deflators.values())
    logger.info(
        "Deflator built: %d years (%d–%d), base %d, %s. Oldest factor %.3fx — "
        "the nominal-dollar distortion this removes.",
        len(deflators), FIRST_YEAR, base_year, base_year, uom[0],
        max(deflators.values()),
    )
    if spread < 1.05:
        logger.warning(
            "deflator spread is only %.3fx across %d–%d — implausibly flat for a "
            "construction price index; check the series before committing",
            spread, FIRST_YEAR, base_year,
        )

    return {
        "source": {
            "dataset": "Statistics Canada, Building construction price indexes, "
                       "by type of building and division (quarterly)",
            "table_id": "18-10-0289-01",
            "url": SOURCE_URL,
            "series": SERIES,
            "vector": vectors[0] if vectors else None,
            "units": uom[0],
            "cube_status": status,
            "retrieved": date.today().isoformat(),
        },
        "notes": [
            "Multiply a NOMINAL construction value by deflators[<permit year>] to "
            f"express it in {base_year} dollars.",
            "Annual figures are the mean of the four published quarters. A "
            "trailing partial year is excluded, not averaged"
            + (f" (excluded here: {dropped_partial})." if dropped_partial else "."),
            "Industrial buildings, Edmonton CMA — chosen to match the permits "
            "being deflated (400-series building_type). It is NOT the all-"
            "non-residential index and must not be reused for other lenses "
            "without checking the type of building.",
            "Predecessor tables 18-10-0135 (ends 2022-Q2) and 18-10-0276 (ends "
            "2024-Q2) are ARCHIVED. They still download and still answer, so a "
            "stale pin fails silently rather than loudly — re-run this script "
            "rather than reusing an old extract.",
            "Manual, reviewed input: NOT part of the weekly refresh. A price "
            "index that moved silently would restate every historical spike on "
            "the map at once.",
        ],
        "base_year": base_year,
        "first_year": FIRST_YEAR,
        "index": index_values,
        "deflators": deflators,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--base-year", type=int, default=DEFAULT_BASE_YEAR,
                    help=f"express dollars in this year (default {DEFAULT_BASE_YEAR})")
    ap.add_argument("--out", type=Path, default=OUT_PATH)
    ap.add_argument("--keep-download", type=Path, default=None,
                    help="also write the raw zip here (debugging)")
    args = ap.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    payload = fetch_index(base_year=args.base_year, keep_download=args.keep_download)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n")

    d = payload["deflators"]
    logger.info("Wrote %s", args.out)
    logger.info("  %s -> %.3fx | %s -> %.3fx | base %s -> 1.000x",
                payload["first_year"], d[str(payload["first_year"])],
                payload["base_year"] - 4, d[str(payload["base_year"] - 4)],
                payload["base_year"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
