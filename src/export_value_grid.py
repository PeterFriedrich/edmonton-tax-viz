"""Grid-cell web export for the Glass view's Urban3-style spikes.

Bins every assessed property (by its lat/long point) into a square grid in
EPSG:3400, sums assessed value — and municipal levy, when apply_tax_rates has
run upstream — per cell, and divides by TWO denominators:

**Ground acres** (always): the cell's own fixed area. Consistent with the
neighbourhood metrics (boundary acres, streets included) and immune to the
per-parcel ``lot_size`` field. Known cost: one lat/long per account means
large parcels needle (WEM — DATA.md §2).

**Lot acres** (when a ``lot_size`` column is present): the deeded parcel area
of the properties in the cell — the actual Urban3 land-productivity metric.
``lot_size`` is unreliable at multi-unit points (duplicated / apportioned /
null with no distinguishing flag — DATA.md §2), so it goes through the dedupe
heuristic validated in docs/FINDINGS_lot_dedupe.md:

  - per point, a repeated ``lot_size`` value counts ONCE when parcel-sized
    (>= ``SHARE_MAX_M2`` — duplication guard) and PER UNIT when share-sized
    (< ``SHARE_MAX_M2`` — identical apportioned shares are real land; a plain
    distinct-sum collapses 300-townhouse complexes to one share and
    manufactures the very needles this metric removes);
  - a point is INELIGIBLE when it has >1 unit and >50% null ``lot_size``
    (understated land -> fake $/lot-acre needles), or no usable value at all;
  - ineligible points are excluded from the lot-acre metric (dollars AND
    acres) and their count + value REPORTED — no silent drops;
  - ``check_lot_acre_bounds`` enforces the physical bound (per-hood deduped
    lot acres <= boundary acres) with a committed known-outlier list.

Output is a compact flat-JSON file (not GeoJSON — ~35k cells of identical
square geometry don't need per-feature geometry objects):

    {
      "cell_m": 100.0,
      "crs_note": "cells binned in EPSG:3400; corners reprojected to WGS84",
      "columns": ["lon", "lat", "value_per_acre", "revenue_per_acre",
                  "value_per_lot_acre", "revenue_per_lot_acre"],
      "cells": [[lon, lat, v, r, vl, rl], ...]   # lon/lat = cell SW corner
    }

``revenue_*`` columns are omitted on the Phase 1 value-only path and the
``*_per_lot_acre`` columns are omitted when ``lot_size`` is absent, mirroring
the graceful degradation everywhere else. Cells with no eligible lot acres
carry ``null`` in the lot-acre slots.
"""

import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd
from pyproj import Transformer

logger = logging.getLogger(__name__)

SQ_M_PER_ACRE = 4046.8564224

# Repeated lot_size values below this are per-unit apportioned shares (count
# each); at or above it they read as a parcel duplicated across units (count
# once). Results are insensitive to the exact cut from 500-2000 m² — see
# docs/FINDINGS_lot_dedupe.md §4.3.
SHARE_MAX_M2 = 1000.0

# Hoods allowed to exceed the physical bound in check_lot_acre_bounds.
# PEMBINA: 1.41x — a 619-unit manufactured-home point claiming 96 lot acres
# plus 137 Avenue lots whose deeded size extends past the hood boundary
# (docs/FINDINGS_lot_dedupe.md §4.4).
KNOWN_BOUND_OUTLIERS = ("PEMBINA",)

# WGS84 lat/long -> Alberta 10-TM Forest (the project CRS for anything
# metric); set explicitly, per project rule, before any area-based math.
_TO_ALBERTA = Transformer.from_crs(4326, 3400, always_xy=True)
_TO_WGS84 = Transformer.from_crs(3400, 4326, always_xy=True)


def _point_lot_stats(pts: pd.DataFrame) -> pd.DataFrame:
    """Deduped lot area + eligibility per exact lat/long point.

    Implements the FINDINGS_lot_dedupe heuristic (repeat-aware dedupe):
    within a point, a repeated lot_size value < SHARE_MAX_M2 counts once per
    unit (apportioned shares), >= SHARE_MAX_M2 counts once total (duplicated
    parcel). Returns one row per point: ``latitude``/``longitude``,
    ``lot_m2``, ``n``/``n_null``, and ``eligible``.
    """
    lot = pts["lot_size"].where(pts["lot_size"] > 0)
    per_point = (
        pts.assign(_lot=lot)
        .groupby(["latitude", "longitude"], sort=False)
        .agg(n=("_lot", "size"), n_null=("_lot", lambda s: s.isna().sum()))
        .reset_index()
    )

    # One row per (point, distinct lot value) with its repeat count k.
    vc = (
        pts.assign(_lot=lot)
        .dropna(subset=["_lot"])
        .groupby(["latitude", "longitude", "_lot"], sort=False)
        .size()
        .rename("k")
        .reset_index()
    )
    vc["contrib"] = vc["_lot"] * np.where(vc["_lot"] < SHARE_MAX_M2, vc["k"], 1)
    lot_m2 = vc.groupby(["latitude", "longitude"], sort=False)["contrib"].sum()

    per_point = per_point.merge(
        lot_m2.rename("lot_m2").reset_index(), on=["latitude", "longitude"], how="left"
    )
    per_point["lot_m2"] = per_point["lot_m2"].fillna(0.0)
    majority_null = (per_point["n"] > 1) & (per_point["n_null"] * 2 > per_point["n"])
    per_point["eligible"] = ~majority_null & (per_point["lot_m2"] > 0)
    return per_point


def build_value_grid(df: pd.DataFrame, cell_m: float = 100.0) -> pd.DataFrame:
    """Aggregate per-property values into square grid cells.

    Expects ``latitude``/``longitude``/``assessed_value`` (load_assessment
    contract) and optionally ``levy`` (apply_tax_rates) and ``lot_size``
    (load_property_info, merged upstream). Returns a DataFrame with one row
    per occupied cell:

        lon, lat                float  cell SW corner, WGS84
        value_per_acre          float  sum(assessed_value) / cell ground acres
        revenue_per_acre        float  sum(levy) / cell ground acres — only
                                       when ``levy`` is present
        value_per_lot_acre      float  eligible value / deduped lot acres —
                                       only when ``lot_size`` is present;
                                       NaN where the cell has no eligible
                                       lot acres
        revenue_per_lot_acre    float  same, from ``levy``

    No silent drops: rows with null coordinates are counted and reported
    (0 in the current data — DATA.md §2), lot-ineligible points are counted
    and reported with their value, and the cell sums are checked to conserve
    the input totals exactly.
    """
    missing = df["latitude"].isna() | df["longitude"].isna()
    if missing.any():
        logger.warning("%d rows have null coordinates — excluded from the grid", missing.sum())
    pts = df.loc[~missing]

    x, y = _TO_ALBERTA.transform(pts["longitude"].to_numpy(), pts["latitude"].to_numpy())
    ix = np.floor(np.asarray(x) / cell_m).astype(np.int64)
    iy = np.floor(np.asarray(y) / cell_m).astype(np.int64)
    cells = pd.DataFrame({
        "ix": ix,
        "iy": iy,
        "assessed_value": pts["assessed_value"].to_numpy(),
    })
    agg_spec = {"assessed_value": "sum"}
    has_levy = "levy" in pts.columns
    if has_levy:
        cells["levy"] = pts["levy"].to_numpy()
        agg_spec["levy"] = "sum"
    grid = cells.groupby(["ix", "iy"], as_index=False).agg(agg_spec)

    # Conservation guard: binning must not create or lose a dollar.
    if not np.isclose(grid["assessed_value"].sum(), pts["assessed_value"].sum()):
        raise RuntimeError("grid cell sums do not conserve total assessed value")

    if "lot_size" in pts.columns:
        grid = grid.merge(
            _cell_lot_metrics(pts, cells, has_levy), on=["ix", "iy"], how="left"
        )

    cell_acres = (cell_m * cell_m) / SQ_M_PER_ACRE
    lon, lat = _TO_WGS84.transform(
        (grid["ix"] * cell_m).to_numpy(), (grid["iy"] * cell_m).to_numpy()
    )
    out = pd.DataFrame({
        "lon": lon,
        "lat": lat,
        "value_per_acre": grid["assessed_value"] / cell_acres,
    })
    if has_levy:
        out["revenue_per_acre"] = grid["levy"] / cell_acres
    if "lot_acres" in grid.columns:
        out["value_per_lot_acre"] = grid["value_eligible"] / grid["lot_acres"]
        if has_levy:
            out["revenue_per_lot_acre"] = grid["levy_eligible"] / grid["lot_acres"]

    logger.info(
        "Value grid: %d properties -> %d occupied %.0f m cells (%d rows without coordinates)",
        len(pts), len(out), cell_m, missing.sum(),
    )
    return out


def _cell_lot_metrics(pts: pd.DataFrame, cells: pd.DataFrame, has_levy: bool) -> pd.DataFrame:
    """Per-cell lot acres + eligible dollar sums (FINDINGS_lot_dedupe heuristic).

    ``cells`` carries the already-computed ix/iy for each row of ``pts``
    (positionally aligned).
    """
    per_point = _point_lot_stats(pts)
    ineligible = per_point[~per_point["eligible"]]

    rows = pd.DataFrame({
        "latitude": pts["latitude"].to_numpy(),
        "longitude": pts["longitude"].to_numpy(),
        "assessed_value": pts["assessed_value"].to_numpy(),
        "ix": cells["ix"].to_numpy(),
        "iy": cells["iy"].to_numpy(),
    })
    if has_levy:
        rows["levy"] = pts["levy"].to_numpy()
    rows = rows.merge(per_point, on=["latitude", "longitude"], how="left")

    if len(ineligible):
        dropped_value = rows.loc[~rows["eligible"], "assessed_value"].sum()
        logger.warning(
            "Lot-acre metric: %d points (%d rows, $%.0fM assessed) are "
            "lot-ineligible (majority-null or no usable lot_size) — excluded "
            "from the lot-acre denominator AND numerator, kept in ground-acre",
            len(ineligible), (~rows["eligible"]).sum(), dropped_value / 1e6,
        )

    elig = rows[rows["eligible"]].copy()
    # A multi-unit point's deduped lot_m2 is a POINT-level quantity — count it
    # once per point, not once per row.
    point_lots = elig.drop_duplicates(["latitude", "longitude"])
    lot_by_cell = point_lots.groupby(["ix", "iy"])["lot_m2"].sum() / SQ_M_PER_ACRE

    agg = {"assessed_value": "sum"}
    if has_levy:
        agg["levy"] = "sum"
    dollars = elig.groupby(["ix", "iy"]).agg(agg)

    out = dollars.join(lot_by_cell.rename("lot_acres")).reset_index()
    out = out.rename(columns={"assessed_value": "value_eligible", "levy": "levy_eligible"})
    return out


def check_lot_acre_bounds(
    df: pd.DataFrame,
    boundaries: pd.DataFrame,
    known_outliers: tuple[str, ...] = KNOWN_BOUND_OUTLIERS,
) -> pd.DataFrame:
    """Physical-bound validation: per-hood deduped lot acres <= boundary acres.

    ``df`` needs ``neighbourhood_name``/``latitude``/``longitude``/``lot_size``;
    ``boundaries`` needs ``neighbourhood_name``/``area_acres`` (load_boundaries
    contract). Raises RuntimeError on any violation NOT in ``known_outliers``
    (a new violation means the dedupe heuristic broke or the data regime
    changed — docs/FINDINGS_lot_dedupe.md §4.1). Returns the per-hood ratio
    frame for inspection.
    """
    pts = df.loc[df["latitude"].notna() & df["longitude"].notna()]
    per_point = _point_lot_stats(pts)
    hood_of_point = (
        pts.groupby(["latitude", "longitude"], sort=False)["neighbourhood_name"].first()
    )
    per_point = per_point.merge(
        hood_of_point.rename("neighbourhood_name").reset_index(),
        on=["latitude", "longitude"],
    )
    hood_lot = (
        per_point.loc[per_point["eligible"]]
        .groupby("neighbourhood_name")["lot_m2"].sum() / SQ_M_PER_ACRE
    )
    ratios = (
        boundaries[["neighbourhood_name", "area_acres"]]
        .merge(hood_lot.rename("lot_acres"), on="neighbourhood_name", how="inner")
    )
    ratios["ratio"] = ratios["lot_acres"] / ratios["area_acres"]

    over = ratios[ratios["ratio"] > 1.0]
    new = over[~over["neighbourhood_name"].isin(known_outliers)]
    logger.info(
        "Lot-acre bound check: %d hoods, median ratio %.2f, %d over 1.0 (%d known)",
        len(ratios), ratios["ratio"].median(), len(over), len(over) - len(new),
    )
    if len(new):
        detail = ", ".join(
            f"{r.neighbourhood_name}={r.ratio:.2f}" for r in new.itertuples()
        )
        raise RuntimeError(
            f"lot-acre bound violated in {len(new)} hood(s) not on the "
            f"known-outlier list: {detail} — the lot_size dedupe heuristic "
            "no longer holds (docs/FINDINGS_lot_dedupe.md)"
        )
    return ratios


def export_value_grid(
    df: pd.DataFrame, out_path: str | Path, cell_m: float = 100.0
) -> dict:
    """Write the grid to ``out_path`` as compact flat JSON; return summary stats.

    Per-acre dollar values are rounded to whole dollars and corners to 6 dp
    (~0.1 m) — display precision; all analysis stays upstream. Lot-acre slots
    are ``null`` where the cell has no eligible lot acres.
    """
    grid = build_value_grid(df, cell_m=cell_m)
    has_revenue = "revenue_per_acre" in grid.columns
    has_lot = "value_per_lot_acre" in grid.columns

    columns = ["lon", "lat", "value_per_acre"]
    if has_revenue:
        columns.append("revenue_per_acre")
    if has_lot:
        columns.append("value_per_lot_acre")
        if has_revenue:
            columns.append("revenue_per_lot_acre")

    def _dollars(v) -> int | None:
        return None if pd.isna(v) else round(v)

    rows = []
    for t in grid.itertuples(index=False):
        row = [round(t.lon, 6), round(t.lat, 6), round(t.value_per_acre)]
        if has_revenue:
            row.append(round(t.revenue_per_acre))
        if has_lot:
            row.append(_dollars(t.value_per_lot_acre))
            if has_revenue:
                row.append(_dollars(t.revenue_per_lot_acre))
        rows.append(row)

    payload = {
        "cell_m": cell_m,
        "crs_note": "cells binned in EPSG:3400; SW corners reprojected to WGS84",
        "columns": columns,
        "cells": rows,
    }
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, separators=(",", ":"))

    stats = {
        "n_cells": len(rows),
        "cell_m": cell_m,
        "has_revenue": has_revenue,
        "has_lot": has_lot,
        "bytes": out_path.stat().st_size,
    }
    if has_lot:
        stats["n_cells_without_lot"] = int(grid["value_per_lot_acre"].isna().sum())
    logger.info(
        "Wrote %s: %d cells, %.1f MB", out_path.name, stats["n_cells"], stats["bytes"] / 1e6
    )
    return stats
