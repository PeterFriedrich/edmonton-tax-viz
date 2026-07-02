"""Road supply layer: overlay Road Network centrelines on neighbourhood
boundaries to derive each neighbourhood's city-maintained road length by class.

See docs/SPEC_services.md (locked decisions), docs/ARCHITECTURE.md §load_roads,
and DATA.md. The shipped metric basis is collector + local ONLY:
  - alleys and railways are excluded at the row filter (centerline_type),
  - non-City segments are excluded (responsible_party),
  - arterials are computed but excluded from road_m_total (shared
    infrastructure — any development pattern entails them; SPEC_services.md).
Classification is an EXPLICIT class→group dict — never keyword/prefix
heuristics (same philosophy as load_zoning's ZONE_CATEGORY).
"""

import logging

import geopandas as gpd
import pandas as pd

logger = logging.getLogger(__name__)

# Row filters (SPEC_services.md, decisions locked 2026-07-01).
CENTERLINE_TYPE = "Road"  # drops Alley (12,088) + Railway (2,117) rows
RESPONSIBLE_PARTY = "City of Edmonton"  # drops provincial/private/rail/neighbours

# Warn when more than this share of filtered road length falls outside every
# neighbourhood polygon (conservation guard).
UNASSIGNED_WARN_FRAC = 0.05

# ---------------------------------------------------------------------------
# Explicit functional_class_code → class group dictionary.
#
# Exact full-string keys (the field is a closed enumeration; 14 values appear
# on City-owned Road rows, verified 2026-07-01). Groups:
#   arterial  — computed + reported, but EXCLUDED from road_m_total
#               (shared infrastructure; SPEC_services.md)
#   collector — in the metric
#   local     — in the metric. Includes Local-Private (73 City-responsible
#               rows — the ownership filter, not the name, governs) and
#               Local-ParkWay (river-valley parkways).
#   alley     — EXCLUDED entirely: 41 Road-type rows are functionally classed
#               Alley-Residential; the alleys-out decision governs by function.
# ---------------------------------------------------------------------------
CLASS_GROUP = {
    # --- arterial (excluded from the metric) -----------------------------------
    "Arterial-Class A (Primary Highway, Truck Route)": "arterial",
    "Arterial-Class B (Non-Primary Highway, Truck Route)": "arterial",
    "Arterial-Class C (Truck Route, Low speeds)": "arterial",
    "Arterial-Class D (Non-Truck Route, Low speeds)": "arterial",
    # --- collector --------------------------------------------------------------
    "Collector-Residential": "collector",
    "Collector-Industrial (Adjoining lots zoned > 50% Industrial)": "collector",
    "Collector-Commercial (Adjoining lots zoned > 50% Commercial)": "collector",
    # --- local --------------------------------------------------------------------
    "Local-Residential": "local",
    "Local-Residential (Enhanced)": "local",
    "Local-Industrial (Adjoining lots zoned > 50% Industrial)": "local",
    "Local-Commercial (Adjoining lots zoned > 50% Commercial)": "local",
    "Local-ParkWay": "local",
    "Local-Private": "local",
    # --- alley (excluded entirely) -----------------------------------------------
    "Alley-Residential": "alley",
}

# Groups carried as output columns (alley is dropped before the overlay).
GROUPS = ("arterial", "collector", "local")

# Groups that make up road_m_total (arterials are shared infrastructure).
METRIC_GROUPS = ("collector", "local")

# Unknown/null classes default here (conservative for a supply metric: the
# length STAYS IN road_m_total rather than silently vanishing). Flagged.
DEFAULT_GROUP = "local"


def _classify(class_series: pd.Series) -> pd.Series:
    """Map functional_class_code to a class group via the explicit dict.

    After the Road + City filters every row should carry a class (nulls in the
    raw feed are exactly the alley + railway rows — verified 2026-07-01), so a
    null or unmatched value here means upstream drift: warn loudly (no silent
    drops) and default to DEFAULT_GROUP so the length stays in the metric.
    """
    group = class_series.map(CLASS_GROUP)

    unmatched = group.isna()
    if unmatched.any():
        missing = sorted(class_series[unmatched].fillna("<null>").unique())
        logger.warning(
            "Unmatched functional_class_code values on %d rows (defaulting to %r "
            "— expected NONE after the Road/City filters; check for upstream "
            "drift): %s",
            int(unmatched.sum()),
            DEFAULT_GROUP,
            missing,
        )
        group = group.fillna(DEFAULT_GROUP)

    return group


def _clean_geometry(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Drop empty/missing and non-line geometries (centrelines must be lines)."""
    before = len(gdf)
    gdf = gdf[gdf.geometry.notna() & ~gdf.geometry.is_empty]
    gdf = gdf[gdf.geometry.geom_type.isin(["LineString", "MultiLineString"])]
    dropped = before - len(gdf)
    if dropped:
        logger.info("Dropped %d empty/non-line road features after cleaning", dropped)
    return gdf


def load_roads(roads_path: str, boundaries: gpd.GeoDataFrame) -> pd.DataFrame:
    """Overlay road centrelines on boundaries → per-neighbourhood road metres.

    Parameters
    ----------
    roads_path : str
        Path to the Road Network GeoJSON (`9j8t-zm52`).
    boundaries : gpd.GeoDataFrame
        Output of load_boundaries — MUST carry projected geometry (EPSG:3400)
        and a `neighbourhood_name` column.

    Returns
    -------
    pd.DataFrame keyed by `neighbourhood_name` with columns:
        road_m_arterial  — internal only; NEVER part of the metric
        road_m_collector
        road_m_local
        road_m_total     — collector + local (the metric basis;
                           road_m_per_acre is computed downstream in
                           join_and_calculate against boundary acres)
    """
    roads = gpd.read_file(roads_path)
    logger.info("Loaded %d centreline features (input CRS: %s)", len(roads), roads.crs)

    # Row filters (no silent drops — report what each one removes).
    is_road = roads["centerline_type"] == CENTERLINE_TYPE
    logger.info(
        "Filter centerline_type == %r: keeping %d, dropping %d (alleys/railways)",
        CENTERLINE_TYPE, int(is_road.sum()), int((~is_road).sum()),
    )
    roads = roads[is_road]

    is_city = roads["responsible_party_description"] == RESPONSIBLE_PARTY
    logger.info(
        "Filter responsible_party == %r: keeping %d, dropping %d (non-City)",
        RESPONSIBLE_PARTY, int(is_city.sum()), int((~is_city).sum()),
    )
    roads = roads[is_city].copy()

    if roads.crs is None:
        logger.warning("Roads CRS missing — assuming EPSG:4326")
        roads = roads.set_crs(epsg=4326)
    roads = roads.to_crs(epsg=3400)

    roads = _clean_geometry(roads)
    roads["group"] = _classify(roads["functional_class_code"])

    # Functionally-alley Road rows are excluded per the alleys-out decision —
    # explicitly, with the discarded length reported.
    is_alley = roads["group"] == "alley"
    if is_alley.any():
        logger.info(
            "Excluding %d functionally-alley road rows (%.1f km) per SPEC_services.md",
            int(is_alley.sum()),
            roads.loc[is_alley].geometry.length.sum() / 1000,
        )
        roads = roads[~is_alley]

    # Keep only what the overlay needs.
    roads = roads[["group", "geometry"]]

    if boundaries.crs is None or boundaries.crs.to_epsg() != 3400:
        raise ValueError(
            f"boundaries must be projected to EPSG:3400 before overlay (got {boundaries.crs})"
        )

    total_before = roads.geometry.length.sum()

    overlay = gpd.overlay(
        roads,
        boundaries[["neighbourhood_name", "geometry"]],
        how="intersection",
        keep_geom_type=True,
    )
    overlay["piece_m"] = overlay.geometry.length

    # Conservation guard: clipped pieces must account for (nearly) all filtered
    # length; the remainder lies outside every neighbourhood polygon.
    total_after = overlay["piece_m"].sum()
    unassigned = total_before - total_after
    unassigned_frac = unassigned / total_before if total_before else 0.0
    log = logger.warning if unassigned_frac > UNASSIGNED_WARN_FRAC else logger.info
    log(
        "Road length conservation: %.1f km in, %.1f km assigned to neighbourhoods, "
        "%.1f km (%.2f%%) outside all boundaries",
        total_before / 1000, total_after / 1000, unassigned / 1000, 100 * unassigned_frac,
    )

    by_group = (
        overlay.groupby(["neighbourhood_name", "group"])["piece_m"]
        .sum()
        .unstack(fill_value=0.0)
    )
    for group in GROUPS:
        if group not in by_group.columns:
            by_group[group] = 0.0

    result = pd.DataFrame(
        {
            "road_m_arterial": by_group["arterial"],
            "road_m_collector": by_group["collector"],
            "road_m_local": by_group["local"],
        }
    )
    result["road_m_total"] = sum(result[f"road_m_{g}"] for g in METRIC_GROUPS)
    result = result.reset_index()

    logger.info(
        "Road overlay: %d neighbourhoods; %.1f km collector+local in the metric, "
        "%.1f km arterial carried internally",
        len(result),
        result["road_m_total"].sum() / 1000,
        result["road_m_arterial"].sum() / 1000,
    )
    return result
