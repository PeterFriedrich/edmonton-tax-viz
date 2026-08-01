"""Attribute each property's municipal levy to a zoning CATEGORY, per neighbourhood.

The Uses lens answers "what is this land zoned for" by AREA, from the zoning
polygons. This module answers "where does this neighbourhood's revenue come
from" over the *same* polygons, weighted by levy instead of area — so the two
are one map read two ways and cannot disagree about what a category means.

⚠️ WHY THE POLYGONS AND NOT THE PER-PROPERTY `zoning` FIELD. `dkk9-cj3x` carries
a `zoning` string per account, and using it directly is the obvious route. It is
also wrong here: the field is null for 35.7% of properties — **16.0% of citywide
revenue, and 42% of DOWNTOWN's** — because condo units carry no zoning. A
"top 3 zones" built on it would have shown a hole as Downtown's largest entry.
Every one of those Downtown properties has coordinates and falls inside a zoning
polygon (measured 2026-08-01: 11,022 / 11,022 filled), so the point-in-polygon
route is both more complete and the one that matches the Uses lens.

Inputs:  the assessment frame AFTER `apply_tax_rates` (needs `levy`,
         `neighbourhood_name`, `latitude`, `longitude`), plus the zoning
         GeoDataFrame from `load_zoning`'s source file.
Outputs: one row per neighbourhood, `rev_frac_*` per category summing to 1.0.

Does not: aggregate anything else, touch boundaries, or know about acres.
"""

from __future__ import annotations

import logging

import geopandas as gpd
import pandas as pd

from load_zoning import CATEGORIES, DEFAULT_CATEGORY, ZONE_CATEGORY

logger = logging.getLogger(__name__)

# The lat/lon in the assessment roll are WGS84. Stated, never inferred — an
# unset CRS is the silent failure mode this project's CRS rule exists to stop.
POINTS_CRS = "EPSG:4326"

# Revenue that landed in no zoning polygon at all. Its own bucket rather than a
# drop, so the fractions always sum to 1 and the gap is visible instead of
# quietly inflating every other category.
UNZONED = "unzoned"

# Mirrors load_zoning's export names so the revenue fractions read as siblings
# of the area fractions they sit beside in the output.
OUTPUT_NAMES = {
    "never": "rev_frac_never",
    "notyet": "rev_frac_notyet",
    "inst": "rev_frac_inst",
    "res": "rev_frac_residential",
    "com": "rev_frac_commercial",
    "ind": "rev_frac_industrial",
    "mix": "rev_frac_mixed",
    "dc": "rev_frac_dc",
    "other": "rev_frac_other",
    UNZONED: "rev_frac_unzoned",
}

REQUIRED_COLUMNS = ("neighbourhood_name", "levy", "latitude", "longitude")

# Fractions are rounded before export: 1e-6 is 0.0001% of a neighbourhood's
# levy, orders below anything the readout can show, and full float repr costs
# ~19 characters per value. Measured 2026-08-01 over 406 features x 12 columns:
# +33 kB gzipped unrounded vs +4 kB rounded. Rounding here rather than at export
# so the module's own output matches what ships.
FRACTION_DECIMALS = 6


def _categorize_codes(codes: pd.Series) -> pd.Series:
    """Map zoning codes to categories, flagging unknowns instead of dropping them.

    Deliberately a separate pass from `load_zoning._categorize`: that one takes
    the polygon frame's own column, this one takes the column AFTER a spatial
    join, where the null case means "matched no polygon" rather than "no zoning
    recorded". Same dict, so the two cannot drift on what a code means.
    """
    base = codes.astype("string").str.strip().str.split().str[0]
    category = base.map(ZONE_CATEGORY)

    unknown = category.isna() & base.notna() & (base != "")
    if unknown.any():
        logger.warning(
            "%d propert(ies) in %d unmatched zone code(s), defaulting to %r: %s",
            int(unknown.sum()),
            base[unknown].nunique(),
            DEFAULT_CATEGORY,
            sorted(base[unknown].dropna().unique()),
        )
        category = category.mask(unknown, DEFAULT_CATEGORY)

    return category


def revenue_by_zone(
    assessment: pd.DataFrame,
    zoning: gpd.GeoDataFrame,
    *,
    zoning_column: str = "zoning",
) -> pd.DataFrame:
    """Return per-neighbourhood revenue shares by zoning category.

    ``assessment`` must already carry ``levy`` (run ``apply_tax_rates`` first).
    Returns ``neighbourhood_name`` plus one ``rev_frac_*`` column per category,
    each row summing to 1.0, and ``rev_zone_matched_frac`` — the share of the
    neighbourhood's levy that landed in a real polygon.
    """
    missing = [c for c in REQUIRED_COLUMNS if c not in assessment.columns]
    if missing:
        raise KeyError(
            f"revenue_by_zone needs {missing} — run apply_tax_rates first "
            f"(have: {sorted(assessment.columns)})"
        )
    if zoning_column not in zoning.columns:
        raise KeyError(f"zoning frame has no {zoning_column!r} column")

    df = assessment[list(REQUIRED_COLUMNS)].copy()

    no_coords = df["latitude"].isna() | df["longitude"].isna()
    if no_coords.any():
        # Not a drop: they keep their levy and fall into UNZONED below, so the
        # neighbourhood's denominator stays its true total.
        logger.warning(
            "%d propert(ies) carrying $%.0f of levy have no coordinates and "
            "cannot be placed in a zone",
            int(no_coords.sum()),
            df.loc[no_coords, "levy"].sum(),
        )

    placed = df.loc[~no_coords]
    points = gpd.GeoDataFrame(
        placed,
        geometry=gpd.points_from_xy(placed["longitude"], placed["latitude"]),
        crs=POINTS_CRS,
    )
    # Explicit, both sides, every time — even when they already agree.
    zones = zoning[[zoning_column, "geometry"]].to_crs(POINTS_CRS)

    joined = gpd.sjoin(points, zones, how="left", predicate="within")

    # A point exactly on a shared boundary matches BOTH polygons and sjoin emits
    # a row per match, which would double-count its levy. Keep the first and say
    # how often it happened rather than silently deduping.
    duplicated = joined.index.duplicated(keep="first")
    if duplicated.any():
        logger.info(
            "%d propert(ies) fell on a zone boundary and matched >1 polygon; "
            "kept the first match",
            int(duplicated.sum()),
        )
        joined = joined[~duplicated]

    category = _categorize_codes(joined[zoning_column])
    unmatched = category.isna()
    if unmatched.any():
        logger.warning(
            "%d propert(ies) carrying $%.0f of levy fell in NO zoning polygon "
            "(bucketed as %r)",
            int(unmatched.sum()),
            joined.loc[unmatched, "levy"].sum(),
            UNZONED,
        )
    joined["category"] = category.fillna(UNZONED)

    # Properties with no coordinates rejoin here so the denominator is the
    # neighbourhood's FULL levy, not just its placeable share.
    stranded = df.loc[no_coords].assign(category=UNZONED)
    tall = pd.concat(
        [joined[["neighbourhood_name", "levy", "category"]], stranded[["neighbourhood_name", "levy", "category"]]],
        ignore_index=True,
    )

    by_cat = (
        tall.groupby(["neighbourhood_name", "category"])["levy"]
        .sum()
        .unstack(fill_value=0.0)
    )
    order = [*CATEGORIES, UNZONED]
    for cat in order:
        if cat not in by_cat.columns:
            by_cat[cat] = 0.0

    totals = by_cat[order].sum(axis=1)
    # A neighbourhood whose whole roll is exempt has a $0 denominator. NaN, not
    # 0.0 — "no revenue to apportion" is not "0% from every category", and the
    # front end must be able to tell them apart.
    zero = totals == 0
    if zero.any():
        logger.warning(
            "%d neighbourhood(s) have $0 total levy; their shares are NaN: %s",
            int(zero.sum()),
            sorted(totals.index[zero]),
        )
    fracs = by_cat[order].div(totals.where(~zero), axis=0)

    result = fracs.rename(columns=OUTPUT_NAMES).round(FRACTION_DECIMALS)
    result["rev_zone_matched_frac"] = 1.0 - result[OUTPUT_NAMES[UNZONED]]
    return result.reset_index()


def top_zones(row: pd.Series, n: int = 3, *, include_unzoned: bool = False) -> list[tuple[str, float]]:
    """The n largest revenue categories for one neighbourhood row, largest first.

    Zero-share categories are omitted — a neighbourhood with two land uses should
    report two, not two plus a padding entry at 0%.
    """
    names = {v: k for k, v in OUTPUT_NAMES.items()}
    shares = {
        names[col]: row[col]
        for col in OUTPUT_NAMES.values()
        if col in row.index and pd.notna(row[col]) and row[col] > 0
        and (include_unzoned or col != OUTPUT_NAMES[UNZONED])
    }
    return sorted(shares.items(), key=lambda kv: -kv[1])[:n]
