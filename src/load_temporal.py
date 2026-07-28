"""Neighbourhood assessment over time — the spliced hood x year table.

Phase 0 of docs/SPEC_temporal.md. Produces one row per (neighbourhood, year)
carrying assessed value, account count, and the two share-of-base metrics the
lens plots.

THE SPLICE, and why there is one
--------------------------------
Two sources, because neither alone is publishable:

  * ``qi6a-xuwt`` (Property Assessment Data - Historical) covers 2012-2025, but
    its **2024 and 2025 slices are missing 2,448 accounts worth $2.93B** across
    188 neighbourhoods (audited 2026-07-28; data/DATA.md section 0).
  * ``q7d6-ambg`` (the current roll) is complete and is what the shipped site is
    built from, but it is a single year with no history.

So: **history from the historical file, the live year from the current roll, and
any year that neither source covers completely is OMITTED** (decided 2026-07-28 --
interpolating a known hole is exactly the failure this project's guard culture
exists to prevent). Today that means 2012-2023 + 2025, with **2024 absent**. The
published year list is therefore **deliberately non-contiguous**; see
``publishable_years``, and do not "fix" the gap.

Two traps this module exists to handle
--------------------------------------
1. **Hood names are not stable across 14 years.** OLIVER carried ~12,000
   accounts from 2012 through 2024 and appears as WIHKWENTOWIN from 2025 -- a
   rename, not a collapse. Naively keyed by name, the series shows one
   neighbourhood dying and another appearing from nothing. 32 historical names
   have no current boundary at all.
2. **An unmatched name is not a dropped dollar.** The metric is *share of the
   citywide base*, so every row belongs in the DENOMINATOR whether or not it has
   a polygon to render. Unmatched hoods are counted, reported, and kept in the
   base; only the numerator is restricted to hoods that render. Dropping them
   from both would silently inflate every other hood's share.

Vintage caveat (real, and not fixable here)
-------------------------------------------
The current roll is a *live* snapshot of the live assessment year, while the
historical file is that year as published at the time. The current roll
therefore carries titles created since (~8,200 accounts as of 2026-07-28, mostly
new construction). The live year's account count is consequently not
vintage-comparable with the historical years' -- it is the same year measured
later. Value shares are far less sensitive to this than counts, which is another
reason the plotted metric is a share rather than a level.
"""

import json
import logging
from pathlib import Path

import pandas as pd

from src.load_assessment import NAME_CORRECTIONS

logger = logging.getLogger(__name__)

# First year in the historical file. 2012 is also the first year the audit could
# not test (no prior year to compare against) -- see SPEC_temporal.md section 0.1.
FIRST_YEAR = 2012

# Years PROVEN incomplete in the historical file (audited 2026-07-28, all 14
# years -- SPEC_temporal.md section 0.1). 2024 lost 2,322 accounts and 2025 a
# further 131; every other year is clean at 0.00%.
#
# NOT the same thing as the omitted years, and the difference is the subtle part.
# A defective year is publishable if and only if a complete source covers it, and
# the only such source is the current roll, which covers exactly ONE year: the
# live one. So 2025 is publishable *while it is the live year* and becomes
# unpublishable the moment the roll advances past it -- see publishable_years.
#
# The trap this exists to close: with a plain "omit 2024" rule, next January's
# roll-forward would make 2026 live, quietly drop 2025 back to the historical
# file, and re-acquire the defect on a year that renders fine today. Nothing else
# in the pipeline would notice.
HISTORICAL_DEFECT_YEARS = (2024, 2025)

# The "commercial base" denominator (SPEC_temporal.md section 6). Deliberately
# just COMMERCIAL: this is the series public reporting quotes, and the
# neighbouring classes are noise -- NONRES MUNICIPAL/RES EDUCATION is 19 rows
# across all 14 years and DESIGNATED IND PROPERTIES is 1, so their shares swing
# on single accounts. Explicit tuple rather than a "not residential" rule, same
# philosophy as ZONE_CATEGORY / ROUTE_MODE: every class hand-assigned.
COMMERCIAL_CLASSES = ("COMMERCIAL",)

# Historical hood name -> current boundary name, applied ON TOP of the pipeline's
# shared NAME_CORRECTIONS. Every entry is a name that appears in the historical
# file and resolves to exactly one present-day boundary.
#
# OLIVER is a genuine municipal RENAME (to Wihkwentowin, effective in the 2025
# roll) and is the single most consequential entry here: without it a
# 12,000-account central neighbourhood reads as vanishing in 2025.
#
# The " AREA" entries are the same pattern as the shared NAME_CORRECTIONS'
# "CHAPPELLE AREA" -> "CHAPPELLE": a staging name used while land developed,
# later replaced by the settled neighbourhood name. Each was confirmed to match
# a current boundary exactly after the suffix; names that merely LOOK like the
# pattern but have no exact match (GLENRIDDING AREA, MEADOWS AREA, TERWILLEGAR
# AREA) are deliberately NOT guessed at -- they stay unmatched and reported.
TEMPORAL_NAME_CORRECTIONS = {
    "OLIVER":               "WÎHKWÊNTÔWIN",
    "KESWICK AREA":         "KESWICK",
    "MACTAGGART AREA":      "MACTAGGART",
    "MAGRATH HEIGHTS AREA": "MAGRATH HEIGHTS",
    "MCCONACHIE AREA":      "MCCONACHIE",
    "WINDERMERE AREA":      "WINDERMERE",
}

# Column order of the emitted table.
TEMPORAL_COLUMNS = [
    "neighbourhood_name", "year", "source",
    "n_accounts", "total_assessed_value",
    "commercial_n_accounts", "commercial_assessed_value",
    "share_of_total_base", "share_of_commercial_base",
    "matched_boundary",
]

# Web-file scaling. Both series ship as INTEGERS -- JSON floats cost roughly
# their digit count in bytes, and 406 hoods x 13 years x 3 series makes that the
# difference between fitting the budget and not (129 kB verbose vs 88 kB scaled).
#
# SHARE_SCALE: parts per million. The UI shows a share to 2 dp of a percent, i.e.
# 1e-4; ppm is 100x finer, so the worst rounding error is 0.00005 pp -- invisible.
#
# VALUE_UNIT: dollars per stored unit. $1k, chosen by measurement, NOT by taste.
# The obvious $0.1M is 10 kB smaller and puts the smallest hood ($57.5k) out by
# **74%**; $10k is still out by 7.7%. $1k holds the worst case to 0.87% and still
# lands inside the budget, so the tail of small hoods stays honest.
SHARE_SCALE = 1_000_000
VALUE_UNIT = 1_000


def publishable_years(live_year: int, defect_years=HISTORICAL_DEFECT_YEARS,
                      first_year=FIRST_YEAR, archived_years=()) -> tuple[int, ...]:
    """The year list the lens should publish, gaps and all.

    A year is publishable when a COMPLETE source covers it, in precedence order:
    the current roll (the live year), then the archive (a year captured while it
    WAS live), then the historical file when it is clean for that year. The result
    is deliberately non-contiguous -- a caller that wants an unbroken range is
    asking the wrong question (see the module docstring).

    Live 2025, nothing archived:  2012-2023 + 2025, with 2024 missing.
    Live 2026, 2025 archived:     2012-2023 + 2025 + 2026 -- 2025 survives the
                                  roll-forward because it was captured in time.
    Live 2026, nothing archived:  2012-2023 + 2026 -- 2025 is lost for good.
    """
    defect, archived = set(defect_years), set(archived_years)
    return tuple(
        y for y in range(first_year, live_year + 1)
        if y == live_year or y in archived or y not in defect
    )


def omitted_years(live_year: int, defect_years=HISTORICAL_DEFECT_YEARS,
                  first_year=FIRST_YEAR, archived_years=()) -> tuple[int, ...]:
    """The inverse of publishable_years, for reporting."""
    published = set(publishable_years(live_year, defect_years, first_year, archived_years))
    return tuple(y for y in range(first_year, live_year + 1) if y not in published)


def load_archive(path: str | Path) -> pd.DataFrame:
    """Read the committed archive of previously-live years into the long shape.

    Returns an empty frame (correct columns) when the file is absent, so the
    archive is optional everywhere and its absence is never an error.
    """
    cols = ["year", "neighbourhood_name", "mill_class", "n_accounts", "assessed_value"]
    path = Path(path)
    if not path.exists():
        return pd.DataFrame(columns=cols)
    payload = json.loads(path.read_text())
    rows = [
        (int(year), hood, cls, int(n), float(v))
        for year, hoods in payload.get("years", {}).items()
        for hood, classes in hoods.items()
        for cls, (n, v) in classes.items()
    ]
    return pd.DataFrame(rows, columns=cols)


def write_archive(path: str | Path, current: pd.DataFrame, live_year: int) -> dict:
    """Capture the live year into the archive. Returns a summary dict.

    THE FREEZE RULE, and it is the whole safety story: only the LIVE year is ever
    written. A year already archived is never rewritten, because once the roll
    advances past it we no longer hold a complete source for it -- any rewrite
    could only be a downgrade, and a silent one.

    Called every pipeline run, so the live year's entry tracks the roll while it
    is still live (each run captures a slightly more complete snapshot) and then
    freezes by itself when the roll moves on. Nobody has to remember to do this
    in January, which is the point -- a step that must be performed exactly once,
    at a date months away, is a step that does not happen.
    """
    path = Path(path)
    payload = json.loads(path.read_text()) if path.exists() else {}
    years = payload.setdefault("years", {})

    frozen = sorted(int(y) for y in years if int(y) != live_year)
    live = current[current["year"] == live_year]
    if live.empty:
        raise ValueError(f"nothing to archive: the frame carries no rows for {live_year}")

    entry: dict[str, dict[str, list]] = {}
    for row in live.itertuples():
        entry.setdefault(row.neighbourhood_name, {})[row.mill_class] = [
            int(row.n_accounts), round(float(row.assessed_value), 2)
        ]
    years[str(live_year)] = entry

    payload["_note"] = (
        "Assessment years captured from the CURRENT ROLL while each was the live "
        "year. The roll covers exactly one year, so a year not captured here "
        "before the roll advances is unrecoverable. Years other than the live one "
        "are FROZEN and must never be rewritten -- see src/load_temporal."
        "write_archive. Generated; do not hand-edit."
    )
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=1, sort_keys=True) + "\n")

    summary = {
        "archived_year": live_year,
        "hoods": len(entry),
        "frozen_years": tuple(frozen),
        "bytes": path.stat().st_size,
    }
    logger.info(
        "Archived %d (%d hoods) -> %s; %d frozen year(s) left untouched %s",
        live_year, len(entry), path.name, len(frozen), list(frozen),
    )
    return summary


def normalize_hood(names: pd.Series) -> pd.Series:
    """Strip + uppercase + both correction layers, in the pipeline's usual order.

    Corrections are applied BEFORE any aggregation, for the same reason
    load_assessment does it: correcting after the sum collapses two summed rows
    onto one boundary and duplicates it.
    """
    out = names.fillna("").str.strip().str.upper()
    return out.replace(NAME_CORRECTIONS).replace(TEMPORAL_NAME_CORRECTIONS)


def load_historical_aggregate(csv_path: str | Path) -> pd.DataFrame:
    """Read the pre-aggregated historical extract into the internal long shape.

    The file is the year x hood x class aggregate written by
    ``scripts/download_data.py`` (~14,800 rows), NOT the 5.5M-row raw dataset --
    the whole dataset never has to be downloaded, which is what makes this lens
    cheap (SPEC_temporal.md section 3).
    """
    df = pd.read_csv(csv_path)
    missing = {"assessment_year", "neighbourhood_name", "mill_class_1",
               "n_accounts", "total_assessed_value"} - set(df.columns)
    if missing:
        raise ValueError(
            f"{Path(csv_path).name}: missing expected column(s) {sorted(missing)}. "
            "Re-fetch with scripts/download_data.py --only assessment_historical."
        )
    return pd.DataFrame({
        "year": df["assessment_year"].astype(int),
        "neighbourhood_name": normalize_hood(df["neighbourhood_name"]),
        "mill_class": df["mill_class_1"].fillna("").str.strip().str.upper(),
        "n_accounts": df["n_accounts"].astype(int),
        "assessed_value": df["total_assessed_value"].astype(float),
    })


def current_roll_aggregate(assessment: pd.DataFrame, year: int) -> pd.DataFrame:
    """Aggregate the per-property current roll into the same long shape.

    ``assessment`` is the frame from ``load_assessment.load_assessment`` -- its
    hood names already carry NAME_CORRECTIONS, but not the temporal layer, so it
    is re-normalized here (both correction maps are idempotent on already-clean
    names).
    """
    df = pd.DataFrame({
        "year": year,
        "neighbourhood_name": normalize_hood(assessment["neighbourhood_name"]),
        "mill_class": assessment["assessment_class_1"].fillna("").str.strip().str.upper(),
        "assessed_value": assessment["assessed_value"].astype(float),
    })
    return (
        df.groupby(["year", "neighbourhood_name", "mill_class"], as_index=False)
          .agg(n_accounts=("assessed_value", "size"), assessed_value=("assessed_value", "sum"))
    )


def _collapse_classes(long: pd.DataFrame) -> pd.DataFrame:
    """Class-grained long form -> one row per (hood, year), with a commercial cut."""
    is_com = long["mill_class"].isin(COMMERCIAL_CLASSES)
    base = (
        long.groupby(["neighbourhood_name", "year"], as_index=False)
            .agg(n_accounts=("n_accounts", "sum"), total_assessed_value=("assessed_value", "sum"))
    )
    com = (
        long[is_com].groupby(["neighbourhood_name", "year"], as_index=False)
            .agg(commercial_n_accounts=("n_accounts", "sum"),
                 commercial_assessed_value=("assessed_value", "sum"))
    )
    out = base.merge(com, on=["neighbourhood_name", "year"], how="left")
    out["commercial_n_accounts"] = out["commercial_n_accounts"].fillna(0).astype(int)
    out["commercial_assessed_value"] = out["commercial_assessed_value"].fillna(0.0)
    return out


def build_temporal_table(
    historical: pd.DataFrame,
    current: pd.DataFrame,
    live_year: int,
    boundary_names=None,
    defect_years=HISTORICAL_DEFECT_YEARS,
    archive: pd.DataFrame | None = None,
) -> tuple[pd.DataFrame, dict]:
    """Splice the two sources into the hood x year table. Returns (table, stats).

    ``historical`` / ``current`` are the long frames from the two loaders above.
    ``boundary_names`` is the set of renderable hood names (from
    ``load_boundaries``); when given, rows outside it are flagged
    ``matched_boundary=False`` -- kept in the denominator, excluded from nothing
    else. See the module docstring on why they are not dropped.

    The live year is taken from the CURRENT ROLL and the historical file's own
    copy of that year is discarded, because the historical copy is the incomplete
    one. That discard is the splice.
    """
    # Re-normalize both inputs. The loaders already did this, so it is a no-op on
    # the pipeline path -- but the hood-rename merge is the one invariant that
    # fails SILENTLY when it is skipped (OLIVER and WÎHKWÊNTÔWIN would survive as
    # two half-length series), so it is enforced here rather than assumed of the
    # caller. Both correction maps are idempotent.
    historical = historical.assign(neighbourhood_name=normalize_hood(historical["neighbourhood_name"]))
    current = current.assign(neighbourhood_name=normalize_hood(current["neighbourhood_name"]))
    if archive is None or archive.empty:
        archive = pd.DataFrame(columns=historical.columns)
    else:
        archive = archive.assign(neighbourhood_name=normalize_hood(archive["neighbourhood_name"]))

    # Source precedence: the roll owns the live year; the archive owns any
    # previously-live year it captured THAT THE HISTORICAL FILE GETS WRONG; the
    # historical file supplies the rest. Archived years are subtracted from the
    # historical set rather than merged, so a defective slice cannot dilute a
    # captured one.
    #
    # The archive deliberately does NOT win for a year the historical file covers
    # correctly, even though a capture exists. The two sources have different
    # vintages -- the roll carries titles created after publication (~8,200
    # accounts today) -- so preferring a capture for a clean year would make that
    # one year measured-later than its neighbours and put a step in the series
    # that is an artifact of sourcing, not of Edmonton. Captures are taken for
    # EVERY live year regardless, because which years turn out defective is not
    # knowable in advance; that is the whole lesson of this dataset.
    archived = {
        int(y) for y in archive["year"].unique()
        if int(y) != live_year and int(y) in set(defect_years)
    }
    keep_years = set(publishable_years(live_year, defect_years, archived_years=archived))
    hist_years = keep_years - {live_year} - archived
    hist = historical[historical["year"].isin(hist_years)]
    arch = archive[archive["year"].isin(archived)]

    cur = current[current["year"] == live_year]
    if cur.empty:
        raise ValueError(
            f"current roll frame carries no rows for live_year={live_year} "
            f"(has {sorted(current['year'].unique())}). The live year cannot be spliced."
        )

    parts = [
        _collapse_classes(hist).assign(source="historical"),
        _collapse_classes(cur).assign(source="current_roll"),
    ]
    if not arch.empty:
        parts.append(_collapse_classes(arch).assign(source="archive"))
    table = pd.concat(parts, ignore_index=True)

    # Citywide base per year = EVERY row of that year, matched or not.
    totals = table.groupby("year").agg(
        base=("total_assessed_value", "sum"),
        com_base=("commercial_assessed_value", "sum"),
    )
    table["share_of_total_base"] = (
        table["total_assessed_value"] / table["year"].map(totals["base"])
    )
    com_base = table["year"].map(totals["com_base"])
    table["share_of_commercial_base"] = (
        table["commercial_assessed_value"] / com_base
    ).where(com_base > 0)

    if boundary_names is None:
        table["matched_boundary"] = True
    else:
        table["matched_boundary"] = table["neighbourhood_name"].isin(set(boundary_names))

    table = table.sort_values(["neighbourhood_name", "year"]).reset_index(drop=True)

    unmatched = table[~table["matched_boundary"]]
    stats = {
        "years": tuple(int(y) for y in sorted(table["year"].unique())),
        "omitted_years": omitted_years(live_year, defect_years, archived_years=archived),
        "archived_years": tuple(sorted(archived)),
        "live_year": live_year,
        "hoods": int(table["neighbourhood_name"].nunique()),
        "rows": len(table),
        "unmatched_hoods": sorted(unmatched["neighbourhood_name"].unique()),
        "unmatched_value_frac": (
            float(unmatched["total_assessed_value"].sum() / table["total_assessed_value"].sum())
            if len(table) else 0.0
        ),
    }

    # No silent drops: an unmatched name is a hood that will not render, and the
    # reader deserves to know how much of the base is behind that.
    if stats["unmatched_hoods"]:
        logger.warning(
            "%d historical hood name(s) have no current boundary and will not render "
            "(kept in the citywide base; %.2f%% of all hood-years' value): %s",
            len(stats["unmatched_hoods"]), stats["unmatched_value_frac"] * 100,
            ", ".join(stats["unmatched_hoods"][:8])
            + ("..." if len(stats["unmatched_hoods"]) > 8 else ""),
        )
    logger.info(
        "Temporal table: %d rows, %d hoods, years %s (omitted %s; %d from the current roll)",
        stats["rows"], stats["hoods"], _year_summary(stats["years"]),
        ", ".join(str(y) for y in stats["omitted_years"]) or "none",
        int((table["source"] == "current_roll").sum()),
    )
    return table[TEMPORAL_COLUMNS], stats


def _year_summary(years) -> str:
    """"2012-2023, 2025" -- so the deliberate gap is visible in the log line."""
    years = sorted(years)
    if not years:
        return "none"
    runs, start, prev = [], years[0], years[0]
    for y in years[1:]:
        if y != prev + 1:
            runs.append((start, prev))
            start = y
        prev = y
    runs.append((start, prev))
    return ", ".join(str(a) if a == b else f"{a}-{b}" for a, b in runs)


def load_temporal(
    historical_csv: str | Path,
    assessment: pd.DataFrame,
    live_year: int,
    boundary_names=None,
    archive_path: str | Path | None = None,
) -> tuple[pd.DataFrame, dict]:
    """Convenience entry point: every loader + the splice, in one call."""
    return build_temporal_table(
        load_historical_aggregate(historical_csv),
        current_roll_aggregate(assessment, live_year),
        live_year,
        boundary_names=boundary_names,
        archive=load_archive(archive_path) if archive_path else None,
    )


def export_temporal_web(table: pd.DataFrame, out_path: str | Path) -> dict:
    """Write the lens's compact web file. Returns a stats dict.

    Shape (SPEC_temporal.md phase 2 -- arrays, not verbose objects)::

        {"years": [2012, ..., 2023, 2025],
         "share_scale": 1000000, "value_unit": 1000,
         "hoods": {"DOWNTOWN": [[share...], [value...], [commercial share...]]}}

    One array per series, index-aligned to ``years`` -- so the sparkline reads a
    hood's whole series without walking objects, and the deliberate 2024 gap is
    carried by the ``years`` array rather than by nulls the renderer would have
    to special-case. **The gap is real: consecutive entries are not necessarily
    consecutive years, so plot against the year values, never the index.**

    ONLY HOODS THAT RENDER ARE WRITTEN. Unmatched names have no polygon to hover,
    but they were already counted in the citywide base upstream, so the shares
    here remain shares of the whole city -- they simply do not sum to 1 across
    the file. That is correct and deliberate; see build_temporal_table.

    A hood with no commercial assessment gets 0, not null: the commercial share
    of a hood with no commercial property IS zero, and null would force the
    reader to distinguish "none" from "missing" where no such distinction exists.
    """
    rendered = table[table["matched_boundary"]]
    years = [int(y) for y in sorted(rendered["year"].unique())]

    hoods: dict[str, list[list[int]]] = {}
    for name, grp in rendered.groupby("neighbourhood_name"):
        grp = grp.sort_values("year")
        if len(grp) != len(years):
            # A hood missing a year would silently shift its whole series left
            # against the shared year axis. Pad explicitly instead.
            grp = grp.set_index("year").reindex(years).reset_index()
        hoods[str(name)] = [
            [_scaled(v, SHARE_SCALE) for v in grp["share_of_total_base"]],
            [_scaled(v, 1.0 / VALUE_UNIT) for v in grp["total_assessed_value"]],
            [_scaled(v, SHARE_SCALE) for v in grp["share_of_commercial_base"]],
        ]

    payload = {
        "years": years,
        "share_scale": SHARE_SCALE,
        "value_unit": VALUE_UNIT,
        "hoods": hoods,
    }
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    out_path.write_text(text + "\n")

    stats = {"hoods": len(hoods), "years": tuple(years), "bytes": len(text) + 1}
    logger.info(
        "Wrote %s: %d hoods x %d years, %.1f kB (%s)",
        out_path.name, len(hoods), len(years), stats["bytes"] / 1024,
        _year_summary(years),
    )
    return stats


def _scaled(value, scale: float) -> int:
    """Scale to an integer; NaN -> 0. See export_temporal_web on why 0, not null."""
    if value is None or value != value:
        return 0
    return int(round(float(value) * scale))
