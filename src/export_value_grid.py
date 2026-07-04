"""Grid-cell web export for the Glass view's Urban3-style spikes.

Bins every assessed property (by its lat/long point) into a square grid in
EPSG:3400, sums assessed value — and municipal levy, when apply_tax_rates has
run upstream — per cell, and divides by the cell's GROUND area in acres.

The ground-acre denominator is a deliberate decision (2026-07-04): it is
consistent with the neighbourhood metrics (which divide by boundary acres,
streets included), and it avoids the per-parcel ``lot_size`` field entirely —
at multi-unit points that field is inconsistently duplicated / apportioned /
null (DATA.md §2), exactly where the tallest spikes are. A lot-acre variant
is a separate TODO.

Output is a compact flat-JSON file (not GeoJSON — ~35k cells of identical
square geometry don't need per-feature geometry objects):

    {
      "cell_m": 100.0,
      "crs_note": "cells binned in EPSG:3400; corners reprojected to WGS84",
      "columns": ["lon", "lat", "value_per_acre", "revenue_per_acre"],
      "cells": [[lon, lat, v, r], ...]     # lon/lat = cell SW corner
    }

``revenue_per_acre`` is omitted from ``columns`` (and each row) on the
Phase 1 value-only path, mirroring the graceful degradation everywhere else.
"""

import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd
from pyproj import Transformer

logger = logging.getLogger(__name__)

SQ_M_PER_ACRE = 4046.8564224

# WGS84 lat/long -> Alberta 10-TM Forest (the project CRS for anything
# metric); set explicitly, per project rule, before any area-based math.
_TO_ALBERTA = Transformer.from_crs(4326, 3400, always_xy=True)
_TO_WGS84 = Transformer.from_crs(3400, 4326, always_xy=True)


def build_value_grid(df: pd.DataFrame, cell_m: float = 100.0) -> pd.DataFrame:
    """Aggregate per-property values into square grid cells.

    Expects ``latitude``/``longitude``/``assessed_value`` (load_assessment
    contract) and optionally ``levy`` (apply_tax_rates). Returns a DataFrame
    with one row per occupied cell:

        lon, lat                float  cell SW corner, WGS84
        value_per_acre          float  sum(assessed_value) / cell ground acres
        revenue_per_acre        float  sum(levy) / cell ground acres — only
                                       when ``levy`` is present

    No silent drops: rows with null coordinates are counted and reported
    (0 in the current data — DATA.md §2), and the cell sums are checked to
    conserve the input totals exactly.
    """
    missing = df["latitude"].isna() | df["longitude"].isna()
    if missing.any():
        logger.warning("%d rows have null coordinates — excluded from the grid", missing.sum())
    pts = df.loc[~missing]

    x, y = _TO_ALBERTA.transform(pts["longitude"].to_numpy(), pts["latitude"].to_numpy())
    cells = pd.DataFrame({
        "ix": np.floor(np.asarray(x) / cell_m).astype(np.int64),
        "iy": np.floor(np.asarray(y) / cell_m).astype(np.int64),
        "assessed_value": pts["assessed_value"].to_numpy(),
    })
    agg_spec = {"assessed_value": "sum"}
    if "levy" in pts.columns:
        cells["levy"] = pts["levy"].to_numpy()
        agg_spec["levy"] = "sum"
    grid = cells.groupby(["ix", "iy"], as_index=False).agg(agg_spec)

    # Conservation guard: binning must not create or lose a dollar.
    if not np.isclose(grid["assessed_value"].sum(), pts["assessed_value"].sum()):
        raise RuntimeError("grid cell sums do not conserve total assessed value")

    cell_acres = (cell_m * cell_m) / SQ_M_PER_ACRE
    lon, lat = _TO_WGS84.transform(
        (grid["ix"] * cell_m).to_numpy(), (grid["iy"] * cell_m).to_numpy()
    )
    out = pd.DataFrame({
        "lon": lon,
        "lat": lat,
        "value_per_acre": grid["assessed_value"] / cell_acres,
    })
    if "levy" in agg_spec:
        out["revenue_per_acre"] = grid["levy"] / cell_acres

    logger.info(
        "Value grid: %d properties -> %d occupied %.0f m cells (%d rows without coordinates)",
        len(pts), len(out), cell_m, missing.sum(),
    )
    return out


def export_value_grid(
    df: pd.DataFrame, out_path: str | Path, cell_m: float = 100.0
) -> dict:
    """Write the grid to ``out_path`` as compact flat JSON; return summary stats.

    Per-acre dollar values are rounded to whole dollars and corners to 6 dp
    (~0.1 m) — display precision; all analysis stays upstream.
    """
    grid = build_value_grid(df, cell_m=cell_m)
    has_revenue = "revenue_per_acre" in grid.columns

    columns = ["lon", "lat", "value_per_acre"] + (["revenue_per_acre"] if has_revenue else [])
    rows = []
    for t in grid.itertuples(index=False):
        row = [round(t.lon, 6), round(t.lat, 6), round(t.value_per_acre)]
        if has_revenue:
            row.append(round(t.revenue_per_acre))
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
        "bytes": out_path.stat().st_size,
    }
    logger.info(
        "Wrote %s: %d cells, %.1f MB", out_path.name, stats["n_cells"], stats["bytes"] / 1e6
    )
    return stats
