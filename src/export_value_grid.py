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


def _spread_large_lots(
    x: np.ndarray, y: np.ndarray, side: np.ndarray, values: np.ndarray, cell_m: float
) -> pd.DataFrame:
    """Distribute each row's values over the cells its lot square overlaps.

    Each row is modelled as a square of the lot's area centred on its point
    (we have no parcel polygons — DATA.md §2); every overlapped cell receives
    ``value × overlap_area / lot_area``. The fractions of a square across a
    grid sum to exactly 1, so conservation is preserved by construction.
    """
    ixs, iys, out = [], [], []
    for i in range(len(x)):
        half = side[i] / 2.0
        x0, x1 = x[i] - half, x[i] + half
        y0, y1 = y[i] - half, y[i] + half
        for ix in range(int(np.floor(x0 / cell_m)), int(np.floor(x1 / cell_m)) + 1):
            ox = min(x1, (ix + 1) * cell_m) - max(x0, ix * cell_m)
            if ox <= 0:
                continue
            for iy in range(int(np.floor(y0 / cell_m)), int(np.floor(y1 / cell_m)) + 1):
                oy = min(y1, (iy + 1) * cell_m) - max(y0, iy * cell_m)
                if oy <= 0:
                    continue
                ixs.append(ix)
                iys.append(iy)
                out.append(values[i] * (ox * oy) / (side[i] * side[i]))
    frame = pd.DataFrame(np.asarray(out), columns=[f"c{j}" for j in range(values.shape[1])])
    frame.insert(0, "ix", ixs)
    frame.insert(1, "iy", iys)
    return frame


def build_value_grid(df: pd.DataFrame, cell_m: float = 100.0) -> pd.DataFrame:
    """Aggregate per-property values into square grid cells.

    Expects ``latitude``/``longitude``/``assessed_value`` (load_assessment
    contract), optionally ``levy`` (apply_tax_rates) and ``lot_size_m2``
    (load_property_info). Returns a DataFrame with one row per occupied cell:

        lon, lat                float  cell SW corner, WGS84
        value_per_acre          float  sum(assessed_value) / cell ground acres
        revenue_per_acre        float  sum(levy) / cell ground acres — only
                                       when ``levy`` is present

    Properties whose lot is LARGER than one cell (``lot_size_m2 > cell_m²``)
    are spread over the cells their footprint covers — modelled as a square
    of the lot's area centred on the point — instead of dropping their whole
    value into the single cell holding the point. Without this, a large
    parcel reads as a false needle: West Edmonton Mall is $1.3B on a 43 ha
    lot behind ONE lat/long; citywide, lots over 1 ha carry ~18% of all
    assessed value. Rows with small or null lot sizes bin by point — which
    also keeps the inconsistent multi-unit ``lot_size`` values (DATA.md §2)
    from mattering: each row only ever spreads over its OWN lot square.

    No silent drops: rows with null coordinates are counted and reported
    (0 in the current data — DATA.md §2), and the cell sums are checked to
    conserve the input totals exactly.
    """
    missing = df["latitude"].isna() | df["longitude"].isna()
    if missing.any():
        logger.warning("%d rows have null coordinates — excluded from the grid", missing.sum())
    pts = df.loc[~missing]

    x, y = _TO_ALBERTA.transform(pts["longitude"].to_numpy(), pts["latitude"].to_numpy())
    x, y = np.asarray(x), np.asarray(y)

    value_cols = ["assessed_value"] + (["levy"] if "levy" in pts.columns else [])
    values = pts[value_cols].to_numpy(dtype=float)

    if "lot_size_m2" in pts.columns:
        lot = pd.to_numeric(pts["lot_size_m2"], errors="coerce").to_numpy(dtype=float)
        big = np.nan_to_num(lot) > cell_m * cell_m
    else:
        big = np.zeros(len(pts), dtype=bool)

    # Point-binned rows (small/unknown lots): value lands in the point's cell.
    binned = pd.DataFrame({
        "ix": np.floor(x[~big] / cell_m).astype(np.int64),
        "iy": np.floor(y[~big] / cell_m).astype(np.int64),
    })
    for j, c in enumerate(value_cols):
        binned[f"c{j}"] = values[~big, j]

    # Large lots: spread over the footprint square.
    parts = [binned]
    if big.any():
        logger.info(
            "Spreading %d large-lot propert(ies) (> %.0f m² footprint) across their cells",
            big.sum(), cell_m * cell_m,
        )
        parts.append(_spread_large_lots(x[big], y[big], np.sqrt(lot[big]), values[big], cell_m))

    cells = pd.concat(parts, ignore_index=True)
    grid = cells.groupby(["ix", "iy"], as_index=False).sum()
    grid = grid.rename(columns={f"c{j}": c for j, c in enumerate(value_cols)})

    # Conservation guard: binning/spreading must not create or lose a dollar.
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
    if "levy" in value_cols:
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
