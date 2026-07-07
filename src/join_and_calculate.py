import logging

import geopandas as gpd
import pandas as pd

logger = logging.getLogger(__name__)


# Zoning composition columns carried into the output when a zoning frame is
# supplied. set_aside_* drive the neutral-grey render; frac_residential/
# is_residential drive the residential-only lens; the full per-category
# fractions (sum to 1) drive the use-mix view — dominant use + tooltip
# composition are derived client-side, like the ratio metric.
ZONING_COLUMNS = [
    "set_aside_frac", "is_set_aside", "set_aside_reason",
    "frac_never", "frac_notyet", "frac_inst",
    "frac_residential", "frac_commercial", "frac_industrial",
    "frac_mixed", "frac_dc", "frac_other",
    "is_residential",
]

# Road-supply column carried from load_roads when a roads frame is supplied
# (services lens, SPEC_services.md). road_m_total = collector + local only;
# the per-class breakdown stays in load_roads. road_m_per_acre is computed
# HERE against boundary area_acres — the same denominator as value/revenue.
ROAD_COLUMNS = ["road_m_total"]

# Modeled stormwater column carried from load_stormwater when supplied
# (utility lens #1, SPEC_utilities.md — MODELED, not billed). The rate-
# independent lot/effective areas stay in load_stormwater; per-acre is
# computed HERE against boundary area_acres, same as everything else.
STORM_COLUMNS = ["storm_charge_annual"]

# Fire-demand column carried from load_fire when supplied (services lens #3,
# SPEC_services.md "Fire lens"): mean annual dispatched emergency events in
# the pinned window. Per-acre is computed HERE against boundary area_acres.
FIRE_COLUMNS = ["fire_events_per_year"]

# Modeled water + sanitary columns carried from load_water when supplied
# (utility lens #2, SPEC_utilities.md — MODELED, not billed; residential
# scope only). Total AND fixed ride along so the client can show the
# connection-vs-consumption split; per-acre is computed HERE.
WATER_COLUMNS = ["water_charge_annual", "water_fixed_annual"]


def join_and_calculate(
    assessment: pd.DataFrame,
    boundaries: gpd.GeoDataFrame,
    zoning: pd.DataFrame | None = None,
    roads: pd.DataFrame | None = None,
    stormwater: pd.DataFrame | None = None,
    fire: pd.DataFrame | None = None,
    water: pd.DataFrame | None = None,
) -> gpd.GeoDataFrame:
    """Left join boundaries → assessment, flag unmatched rows, compute value_per_acre.

    Assessment names are expected to be corrected and aggregated already
    (NAME_CORRECTIONS is applied upstream in load_assessment.py). The one
    expected unmatched case — the OLIVER straggler row, deliberately left
    unmapped (DATA.md "Name Matching") — surfaces here as a warning.

    ``zoning`` (optional, from load_zoning.py) adds the ZONING_COLUMNS — the
    set-aside flags, the residential-lens flag, and the full land-use
    composition fractions (use-mix view) — merged on neighbourhood_name.
    Degrades gracefully when absent, like the revenue columns; boundaries with
    no zoning match default to is_set_aside=False (stays on scale) and
    is_residential=False (frac_* left NaN), and are flagged.

    ``roads`` (optional, from load_roads.py) adds road_m_total and computes
    road_m_per_acre against boundary area_acres (SPEC_services.md). Boundaries
    with no roads overlay default to 0 — genuinely zero city-maintained
    collector/local road, unlike the zoning NaNs — and are flagged.

    ``stormwater`` (optional, from load_stormwater.py) adds the MODELED
    storm_charge_annual and computes storm_charge_per_acre against boundary
    area_acres (SPEC_utilities.md Lens 1). Boundaries with no modeled points
    default to $0 (roads semantics: no roll parcels there means no modeled
    charge) — with the shared caveat that the roll omits exempt institutional
    land, so hood totals understate where exempt land dominates.

    ``fire`` (optional, from load_fire.py) adds fire_events_per_year and
    computes fire_events_per_acre against boundary area_acres
    (SPEC_services.md "Fire lens"). Boundaries with no events default to a
    true 0/yr (roads semantics: no dispatched emergency events recorded
    there in the window) — and are flagged.

    ``water`` (optional, from load_water.py) adds the MODELED residential
    water + sanitary columns (WATER_COLUMNS) and computes
    water_charge_per_acre / water_fixed_per_acre against boundary area_acres
    (SPEC_utilities.md Lens 2). Boundaries with no modeled connections
    default to $0 (stormwater semantics; commercial-only hoods are genuinely
    out of the residential scope) — and are flagged.
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
        # Boundaries without a zoning match stay on the scale, not set aside,
        # and are not claimed residential (frac_* left NaN, like set_aside_frac).
        joined["is_set_aside"] = joined["is_set_aside"].fillna(False).astype(bool)
        joined["set_aside_reason"] = joined["set_aside_reason"].fillna("")
        joined["is_residential"] = joined["is_residential"].fillna(False).astype(bool)

        # Insert zoning columns before geometry.
        out_cols = [c for c in out_cols if c != "geometry"] + ZONING_COLUMNS + ["geometry"]

    # Services lens: merge road supply when supplied (SPEC_services.md).
    if roads is not None:
        boundary_names = set(joined["neighbourhood_name"])
        unmatched_roads = sorted(set(roads["neighbourhood_name"]) - boundary_names)
        if unmatched_roads:
            logger.warning(
                "%d roads neighbourhood(s) with no boundary match (dropped):\n  %s",
                len(unmatched_roads),
                "\n  ".join(unmatched_roads),
            )

        joined = joined.merge(
            roads[["neighbourhood_name", *ROAD_COLUMNS]],
            on="neighbourhood_name",
            how="left",
        )

        no_roads = joined["road_m_total"].isna()
        if no_roads.any():
            logger.warning(
                "%d boundary neighbourhood(s) with no roads overlay (default 0 m):\n  %s",
                int(no_roads.sum()),
                "\n  ".join(sorted(joined.loc[no_roads, "neighbourhood_name"])),
            )
        # No overlay means genuinely zero city collector/local road there.
        joined["road_m_total"] = joined["road_m_total"].fillna(0.0)
        joined["road_m_per_acre"] = joined["road_m_total"] / safe_area

        out_cols = (
            [c for c in out_cols if c != "geometry"]
            + ROAD_COLUMNS + ["road_m_per_acre"] + ["geometry"]
        )

    # Utility lens #1: merge the modeled stormwater charge when supplied
    # (SPEC_utilities.md — modeled, not billed).
    if stormwater is not None:
        boundary_names = set(joined["neighbourhood_name"])
        unmatched_storm = sorted(set(stormwater["neighbourhood_name"]) - boundary_names)
        if unmatched_storm:
            logger.warning(
                "%d stormwater neighbourhood(s) with no boundary match (dropped):\n  %s",
                len(unmatched_storm),
                "\n  ".join(unmatched_storm),
            )

        joined = joined.merge(
            stormwater[["neighbourhood_name", *STORM_COLUMNS]],
            on="neighbourhood_name",
            how="left",
        )

        no_storm = joined["storm_charge_annual"].isna()
        if no_storm.any():
            logger.warning(
                "%d boundary neighbourhood(s) with no modeled stormwater points (default $0):\n  %s",
                int(no_storm.sum()),
                "\n  ".join(sorted(joined.loc[no_storm, "neighbourhood_name"])),
            )
        # No roll parcels modeled there -> modeled $0 (exempt-land caveat above).
        joined["storm_charge_annual"] = joined["storm_charge_annual"].fillna(0.0)
        joined["storm_charge_per_acre"] = joined["storm_charge_annual"] / safe_area

        out_cols = (
            [c for c in out_cols if c != "geometry"]
            + STORM_COLUMNS + ["storm_charge_per_acre"] + ["geometry"]
        )

    # Services lens #3: merge fire demand when supplied (SPEC_services.md
    # "Fire lens" — dispatched emergency events, a demand count, not a
    # coverage or response-time claim).
    if fire is not None:
        boundary_names = set(joined["neighbourhood_name"])
        unmatched_fire = sorted(set(fire["neighbourhood_name"]) - boundary_names)
        if unmatched_fire:
            logger.warning(
                "%d fire neighbourhood(s) with no boundary match (dropped):\n  %s",
                len(unmatched_fire),
                "\n  ".join(unmatched_fire),
            )

        joined = joined.merge(
            fire[["neighbourhood_name", *FIRE_COLUMNS]],
            on="neighbourhood_name",
            how="left",
        )

        no_fire = joined["fire_events_per_year"].isna()
        if no_fire.any():
            logger.warning(
                "%d boundary neighbourhood(s) with no fire events in the window (default 0/yr):\n  %s",
                int(no_fire.sum()),
                "\n  ".join(sorted(joined.loc[no_fire, "neighbourhood_name"])),
            )
        # No kept events there in the window -> a true 0 events/yr.
        joined["fire_events_per_year"] = joined["fire_events_per_year"].fillna(0.0)
        joined["fire_events_per_acre"] = joined["fire_events_per_year"] / safe_area

        out_cols = (
            [c for c in out_cols if c != "geometry"]
            + FIRE_COLUMNS + ["fire_events_per_acre"] + ["geometry"]
        )

    # Utility lens #2: merge the modeled water + sanitary charge when
    # supplied (SPEC_utilities.md Lens 2 — modeled, not billed; residential
    # scope only).
    if water is not None:
        boundary_names = set(joined["neighbourhood_name"])
        unmatched_water = sorted(set(water["neighbourhood_name"]) - boundary_names)
        if unmatched_water:
            logger.warning(
                "%d water neighbourhood(s) with no boundary match (dropped):\n  %s",
                len(unmatched_water),
                "\n  ".join(unmatched_water),
            )

        joined = joined.merge(
            water[["neighbourhood_name", *WATER_COLUMNS]],
            on="neighbourhood_name",
            how="left",
        )

        no_water = joined["water_charge_annual"].isna()
        if no_water.any():
            logger.warning(
                "%d boundary neighbourhood(s) with no modeled water connections "
                "(default $0):\n  %s",
                int(no_water.sum()),
                "\n  ".join(sorted(joined.loc[no_water, "neighbourhood_name"])),
            )
        # No residential roll records there -> modeled $0 (residential scope).
        for col in WATER_COLUMNS:
            joined[col] = joined[col].fillna(0.0)
        joined["water_charge_per_acre"] = joined["water_charge_annual"] / safe_area
        joined["water_fixed_per_acre"] = joined["water_fixed_annual"] / safe_area

        out_cols = (
            [c for c in out_cols if c != "geometry"]
            + WATER_COLUMNS + ["water_charge_per_acre", "water_fixed_per_acre"]
            + ["geometry"]
        )

    return joined[out_cols]


# Columns the web client actually consumes. Everything else is dropped to keep
# the GeoJSON the browser downloads small. revenue_per_acre and the zoning
# columns are included only when present (their respective phases) — the
# value↔revenue toggle reads both metrics; is_set_aside/set_aside_reason drive
# the neutral-grey render + tooltip; is_residential drives the residential lens;
# the frac_* composition (sums to 1) drives the use-mix view (dominant use is
# derived client-side); road_m_per_acre, storm_charge_per_acre,
# fire_events_per_acre, and the water_* pair are the Services-view metrics
# (SPEC_services.md, SPEC_utilities.md — ratios only, totals stay out of the
# slim file like total_assessed_value does; the storm and water figures are
# MODELED, not billed — water additionally residential-scope only, with the
# fixed column shipping alongside the total so the client can show the
# connection-vs-consumption split — and the fire figure is dispatched-event
# DEMAND, not coverage; the client must label all of them as such).
SLIM_COLUMNS = [
    "neighbourhood_name", "value_per_acre", "revenue_per_acre",
    "set_aside_frac", "is_set_aside", "set_aside_reason",
    "frac_never", "frac_notyet", "frac_inst",
    "frac_residential", "frac_commercial", "frac_industrial",
    "frac_mixed", "frac_dc", "frac_other",
    "is_residential", "road_m_per_acre", "storm_charge_per_acre",
    "fire_events_per_acre", "water_charge_per_acre", "water_fixed_per_acre",
    "geometry",
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
