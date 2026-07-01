import logging

import geopandas as gpd
import pandas as pd

logger = logging.getLogger(__name__)


# Zoning composition columns carried into the output when a zoning frame is
# supplied. Kept small — the full per-category fractions stay in load_zoning.
ZONING_COLUMNS = ["set_aside_frac", "is_set_aside", "set_aside_reason"]


def join_and_calculate(
    assessment: pd.DataFrame,
    boundaries: gpd.GeoDataFrame,
    zoning: pd.DataFrame | None = None,
) -> gpd.GeoDataFrame:
    """Left join boundaries → assessment, flag unmatched rows, compute value_per_acre.

    Assessment names are expected to be corrected and aggregated already
    (NAME_CORRECTIONS is applied upstream in load_assessment.py). The three
    unresolved cases (OLIVER, HERITAGE VALLEY TOWN CENTRE AREA,
    LEWIS FARMS INDUSTRIAL) surface here as unmatched warnings.

    ``zoning`` (optional, from load_zoning.py) adds set_aside_frac / is_set_aside
    / set_aside_reason, merged on neighbourhood_name. Degrades gracefully when
    absent, like the revenue columns; boundaries with no zoning match default to
    is_set_aside=False (stays on scale) and are flagged.
    """
    agg = assessment

    boundary_names = set(boundaries["neighbourhood_name"])
    unmatched_assessment = sorted(set(agg["neighbourhood_name"]) - boundary_names)
    if unmatched_assessment:
        logger.warning(
            "%d assessment neighbourhood(s) with no boundary match (excluded from map):\n  %s",
            len(unmatched_assessment),
            "\n  ".join(unmatched_assessment),
        )

    joined = boundaries.merge(agg, on="neighbourhood_name", how="left")

    no_assessment = joined[joined["total_assessed_value"].isna()]
    if len(no_assessment):
        logger.warning(
            "%d boundary neighbourhood(s) with no assessment data:\n  %s",
            len(no_assessment),
            "\n  ".join(sorted(no_assessment["neighbourhood_name"])),
        )

    zero_area = joined["area_acres"] == 0
    if zero_area.any():
        logger.warning(
            "%d neighbourhood(s) with zero area_acres — value_per_acre will be NaN:\n  %s",
            zero_area.sum(),
            "\n  ".join(sorted(joined[zero_area]["neighbourhood_name"])),
        )

    safe_area = joined["area_acres"].replace(0, float("nan"))
    joined["value_per_acre"] = joined["total_assessed_value"] / safe_area

    logger.info(
        "Joined %d boundary neighbourhoods; %d with value_per_acre calculated",
        len(joined),
        joined["value_per_acre"].notna().sum(),
    )

    out_cols = ["neighbourhood_name", "total_assessed_value", "area_acres", "value_per_acre", "geometry"]

    # Revenue phase: when total_revenue is present (apply_tax_rates ran upstream),
    # add revenue_per_acre alongside value_per_acre — both metrics, web toggle.
    if "total_revenue" in joined.columns:
        joined["revenue_per_acre"] = joined["total_revenue"] / safe_area
        out_cols = [
            "neighbourhood_name", "total_assessed_value", "total_revenue",
            "area_acres", "value_per_acre", "revenue_per_acre", "geometry",
        ]

    # Zoning phase: merge land-use set-aside composition when supplied.
    if zoning is not None:
        boundary_names = set(joined["neighbourhood_name"])
        unmatched_zoning = sorted(set(zoning["neighbourhood_name"]) - boundary_names)
        if unmatched_zoning:
            logger.warning(
                "%d zoning neighbourhood(s) with no boundary match (dropped):\n  %s",
                len(unmatched_zoning),
                "\n  ".join(unmatched_zoning),
            )

        joined = joined.merge(
            zoning[["neighbourhood_name", *ZONING_COLUMNS]],
            on="neighbourhood_name",
            how="left",
        )

        no_zoning = joined[joined["set_aside_frac"].isna()]
        if len(no_zoning):
            logger.warning(
                "%d boundary neighbourhood(s) with no zoning overlay (default is_set_aside=False):\n  %s",
                len(no_zoning),
                "\n  ".join(sorted(no_zoning["neighbourhood_name"])),
            )
        # Boundaries without a zoning match stay on the scale, not set aside.
        joined["is_set_aside"] = joined["is_set_aside"].fillna(False).astype(bool)
        joined["set_aside_reason"] = joined["set_aside_reason"].fillna("")

        # Insert zoning columns before geometry.
        out_cols = [c for c in out_cols if c != "geometry"] + ZONING_COLUMNS + ["geometry"]

    return joined[out_cols]


# Columns the web client actually consumes. Everything else is dropped to keep
# the GeoJSON the browser downloads small. revenue_per_acre and the zoning
# set-aside columns are included only when present (their respective phases) —
# the value↔revenue toggle reads both metrics; is_set_aside/set_aside_reason
# drive the neutral-grey render + tooltip.
SLIM_COLUMNS = [
    "neighbourhood_name", "value_per_acre", "revenue_per_acre",
    "set_aside_frac", "is_set_aside", "set_aside_reason", "geometry",
]


# CRS used for the setback buffer — must be projected (metres), not degrees.
# Matches load_boundaries: NAD83 / Alberta 10-TM (Forest).
SETBACK_CRS = "EPSG:3400"


def export_geojson(
    result: gpd.GeoDataFrame,
    output_path: str,
    crs: str = "EPSG:4326",
    setback_m: float = 0.0,
    simplify_tolerance_m: float = 0.0,
) -> gpd.GeoDataFrame:
    """Write a slim GeoJSON of the join result for the Phase 2 web map.

    Keeps only the columns the deck.gl layer needs (SLIM_COLUMNS) and reprojects
    to ``crs`` (default EPSG:4326 — MapLibre/deck.gl expect lon/lat geometry; the
    join result is in projected EPSG:3400 for area math). Rows with no
    value_per_acre cannot be rendered (null elevation), so they are dropped — but
    the count is logged, never silently discarded.

    ``setback_m`` (metres, default 0 = off) shrinks each polygon inward by a
    negative buffer so the extruded columns don't touch — a purely cosmetic
    "city blocks" look. Thin sliver neighbourhoods can collapse to empty/invalid
    under the buffer; those fall back to their original footprint, count logged.

    ``simplify_tolerance_m`` (metres, default 0 = off) runs a topology-preserving
    Douglas-Peucker simplification to cut vertex count — the dominant render-cost
    lever on the iGPU baseline audience (see docs/PERFORMANCE.md). Applied AFTER
    the setback so the final pass also collapses the rounded-corner vertices the
    negative buffer adds, keeping the served file small (the extra export-time
    cost of buffering full-resolution geometry is a once-a-year non-issue).

    Both ``simplify_tolerance_m`` and ``setback_m`` are DISPLAY geometry only;
    value_per_acre is computed from the true area upstream and is untouched.
    Neither silently drops or alters a row without logging it.

    Returns the slim GeoDataFrame that was written.
    """
    slim = result[[c for c in SLIM_COLUMNS if c in result.columns]]

    missing = slim["value_per_acre"].isna()
    if missing.any():
        logger.warning(
            "Dropping %d neighbourhood(s) with no value_per_acre from GeoJSON export:\n  %s",
            missing.sum(),
            "\n  ".join(sorted(slim[missing]["neighbourhood_name"])),
        )
    slim = slim[~missing]

    if slim.crs is None:
        raise ValueError("result GeoDataFrame has no CRS set; cannot reproject for export")

    if setback_m:
        slim = _apply_setback(slim, setback_m)

    if simplify_tolerance_m:
        slim = _apply_simplify(slim, simplify_tolerance_m)

    slim = slim.to_crs(crs)

    slim.to_file(output_path, driver="GeoJSON")
    logger.info(
        "Wrote slim GeoJSON (%d features, %s, simplify=%sm, setback=%sm) to %s",
        len(slim), crs, simplify_tolerance_m, setback_m, output_path,
    )

    return slim


def _apply_setback(slim: gpd.GeoDataFrame, setback_m: float) -> gpd.GeoDataFrame:
    """Shrink each polygon inward by ``setback_m`` metres (display-only).

    Buffers in a projected metric CRS, then restores the original geometry for
    any shape that collapses to empty/invalid, logging which ones.
    """
    metric = slim.to_crs(SETBACK_CRS)
    shrunk = metric.geometry.buffer(-setback_m)

    collapsed = shrunk.is_empty | ~shrunk.is_valid
    if collapsed.any():
        logger.warning(
            "Setback (%sm) collapsed %d sliver neighbourhood(s); kept original footprint:\n  %s",
            setback_m,
            int(collapsed.sum()),
            "\n  ".join(sorted(metric.loc[collapsed, "neighbourhood_name"])),
        )

    metric = metric.set_geometry(shrunk.where(~collapsed, metric.geometry))
    return metric


def _count_vertices(geom) -> int:
    """Total coordinate count of a (Multi)Polygon, exterior + interiors."""
    if geom is None or geom.is_empty:
        return 0
    if geom.geom_type == "Polygon":
        return len(geom.exterior.coords) + sum(len(r.coords) for r in geom.interiors)
    if geom.geom_type == "MultiPolygon":
        return sum(_count_vertices(p) for p in geom.geoms)
    return len(geom.coords)


def _apply_simplify(slim: gpd.GeoDataFrame, tolerance_m: float) -> gpd.GeoDataFrame:
    """Reduce vertex count via Douglas-Peucker in a projected metric CRS (display-only).

    Topology-preserving so polygons stay valid (no new self-intersections) and no
    shape is removed. Logs the vertex reduction; any shape that still lands
    empty/invalid falls back to its original geometry (no silent changes).
    """
    metric = slim.to_crs(SETBACK_CRS)
    before = int(metric.geometry.apply(_count_vertices).sum())

    simplified = metric.geometry.simplify(tolerance_m, preserve_topology=True)

    collapsed = simplified.is_empty | ~simplified.is_valid
    if collapsed.any():
        logger.warning(
            "Simplify (%sm) produced %d empty/invalid geometry(ies); kept original:\n  %s",
            tolerance_m,
            int(collapsed.sum()),
            "\n  ".join(sorted(metric.loc[collapsed, "neighbourhood_name"])),
        )
    simplified = simplified.where(~collapsed, metric.geometry)

    metric = metric.set_geometry(simplified)
    after = int(metric.geometry.apply(_count_vertices).sum())
    logger.info(
        "Simplify (%sm tolerance): %d -> %d vertices (%.0f%% reduction)",
        tolerance_m, before, after, 100 * (1 - after / before) if before else 0.0,
    )
    return metric
