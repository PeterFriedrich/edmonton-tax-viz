"""Bike supply layer: overlay Bike Routes on neighbourhood boundaries to derive
each neighbourhood's length of dedicated cycling infrastructure.

See docs/SPEC_services.md ("Transportation lens"), docs/ARCHITECTURE.md
§load_bike, and DATA.md §15. The shipped metric basis is DEDICATED cycling
assets only:
  - routes flagged ``route_coming_soon`` are excluded (planned, not built),
  - shared roadways are excluded — a "bike route" designation painted on an
    existing street is not new infrastructure, and those metres are ALREADY
    counted in load_roads' road_m_total (double-count guard),
  - walkways/breezeways and maintenance access are excluded (pedestrian and
    operational, not cycling assets).
Classification is an EXPLICIT class→group dict — never keyword/prefix
heuristics (same philosophy as load_roads' CLASS_GROUP and load_zoning's
ZONE_CATEGORY).
"""

import json
import logging
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import MultiLineString
from shapely.ops import linemerge, unary_union

logger = logging.getLogger(__name__)

# Warn when more than this share of filtered bike length falls outside every
# neighbourhood polygon (conservation guard) — the load_roads threshold.
UNASSIGNED_WARN_FRAC = 0.05

# ---------------------------------------------------------------------------
# Explicit classification → group dictionary.
#
# Exact full-string keys (the field is a closed enumeration; all 12 values
# below appear in the live feed, verified 2026-08-02). Groups:
#   dedicated      — in the metric: purpose-built cycling infrastructure,
#                    on-street lanes and off-road paths alike
#   shared_roadway — EXCLUDED: an existing street signed/marked as a bike
#                    route. No new asset, and load_roads already counts these
#                    metres in road_m_total — including them would double-count
#                    the road network against itself
#   pedestrian     — EXCLUDED: walkways, breezeways and maintenance access are
#                    not cycling assets
#   unclassified   — EXCLUDED: the feed's own "don't know" bucket (every row
#                    carrying it is also route_coming_soon, verified 2026-08-02)
# ---------------------------------------------------------------------------
CLASSIFICATION_GROUP = {
    # --- dedicated (in the metric) ---------------------------------------------
    "Protected Bike Lane": "dedicated",
    "Painted Bike Lane": "dedicated",
    "Contra-Flow Bike Lane": "dedicated",
    "Local Street Bikeway": "dedicated",
    "Shared Pathway": "dedicated",
    "Shared Trail": "dedicated",
    # --- shared roadway (excluded — already in road_m_total) --------------------
    "Shared Roadway - Higher Traffic": "shared_roadway",
    "Shared Roadway - Lower Traffic": "shared_roadway",
    "Bus / Bike / Taxi Lane": "shared_roadway",
    # --- pedestrian / operational (excluded) ------------------------------------
    "Walkway / Breezeway": "pedestrian",
    "Maintenance Access": "pedestrian",
    # --- the feed's own unknown bucket (excluded) -------------------------------
    "Unclassified": "unclassified",
}

# Groups carried through the overlay for reporting; only METRIC_GROUPS count.
GROUPS = ("dedicated", "shared_roadway", "pedestrian", "unclassified")

# The metric basis.
METRIC_GROUPS = ("dedicated",)

# Unknown/null classifications default here — EXCLUDED, which is the OPPOSITE
# of load_roads' DEFAULT_GROUP="local". Roads defaults *into* the metric because
# an unclassified City road is still a road the City maintains. Here the metric
# is a narrow subset of a feed that is mostly NOT bike infrastructure (walkways
# and shared roadways outnumber dedicated assets), so an unrecognised value is
# far more likely to be another non-asset than a new lane type: defaulting in
# would let upstream drift silently INFLATE the supply metric. Flagged loudly
# either way — the warning is the actual guard, the default is just which
# direction the error runs.
DEFAULT_GROUP = "unclassified"

# The feed's on/off-road split, kept as internal columns (the load_roads
# class-split and load_transit per-mode pattern: reported internally, combined
# in the published metric).
TYPE_ONROAD = "ON ROAD"
TYPE_OFFROAD = "OFF ROAD"


def _classify(class_series: pd.Series) -> pd.Series:
    """Map ``classification`` to a group via the explicit dict.

    Every live row carries one of the 12 known values, so a null or unmatched
    value here means upstream drift: warn loudly (no silent drops) and default
    to DEFAULT_GROUP, which keeps the length OUT of the metric — see the
    DEFAULT_GROUP comment for why this direction.
    """
    group = class_series.map(CLASSIFICATION_GROUP)

    unmatched = group.isna()
    if unmatched.any():
        missing = sorted(class_series[unmatched].fillna("<null>").unique())
        logger.warning(
            "Unmatched bike-route classification on %d rows (defaulting to %r, "
            "i.e. EXCLUDED from the metric — expected NONE; check for upstream "
            "drift, and add any genuinely new cycling asset type to "
            "CLASSIFICATION_GROUP): %s",
            int(unmatched.sum()),
            DEFAULT_GROUP,
            missing,
        )
        group = group.fillna(DEFAULT_GROUP)

    return group


def _clean_geometry(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Drop empty/missing and non-line geometries (routes must be lines)."""
    before = len(gdf)
    gdf = gdf[gdf.geometry.notna() & ~gdf.geometry.is_empty]
    gdf = gdf[gdf.geometry.geom_type.isin(["LineString", "MultiLineString"])]
    dropped = before - len(gdf)
    if dropped:
        logger.info("Dropped %d empty/non-line bike features after cleaning", dropped)
    return gdf


def _prepare_segments(bike_path: str, boundaries: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Shared front half: load → filter → classify → clip to neighbourhoods.

    Returns the clipped segments as a GeoDataFrame with ``neighbourhood_name``,
    ``group``, ``onroad`` (bool), ``piece_m`` and line geometry in EPSG:3400.
    Used by both load_bike (aggregation) and export_bike_web (the context-layer
    geometry the browser renders).
    """
    bike = gpd.read_file(bike_path)
    logger.info("Loaded %d bike-route features (input CRS: %s)", len(bike), bike.crs)

    for needed in ("classification", "route_coming_soon", "type"):
        if needed not in bike.columns:
            raise ValueError(
                f"expected column {needed!r} not in {bike_path} — columns: "
                f"{sorted(bike.columns)}"
            )

    # Row filter: planned routes are not built infrastructure (no silent drops
    # — report what this removes).
    coming_soon = bike["route_coming_soon"].astype(bool)
    logger.info(
        "Filter route_coming_soon == False: keeping %d, dropping %d (planned, not built)",
        int((~coming_soon).sum()), int(coming_soon.sum()),
    )
    bike = bike[~coming_soon].copy()

    if bike.crs is None:
        logger.warning("Bike routes CRS missing — assuming EPSG:4326")
        bike = bike.set_crs(epsg=4326)
    bike = bike.to_crs(epsg=3400)

    bike = _clean_geometry(bike)
    bike["group"] = _classify(bike["classification"])
    bike["onroad"] = bike["type"] == TYPE_ONROAD

    # Report every excluded group's length explicitly before dropping it.
    for group in GROUPS:
        if group in METRIC_GROUPS:
            continue
        is_group = bike["group"] == group
        if is_group.any():
            logger.info(
                "Excluding %d %r bike rows (%.1f km) per SPEC_services.md",
                int(is_group.sum()), group,
                bike.loc[is_group].geometry.length.sum() / 1000,
            )
    bike = bike[bike["group"].isin(METRIC_GROUPS)]

    bike = bike[["group", "onroad", "geometry"]]

    if boundaries.crs is None or boundaries.crs.to_epsg() != 3400:
        raise ValueError(
            f"boundaries must be projected to EPSG:3400 before overlay (got {boundaries.crs})"
        )

    total_before = bike.geometry.length.sum()

    overlay = gpd.overlay(
        bike,
        boundaries[["neighbourhood_name", "geometry"]],
        how="intersection",
        keep_geom_type=True,
    )
    overlay["piece_m"] = overlay.geometry.length

    # Conservation guard: clipped pieces must account for (nearly) all kept
    # length; the remainder lies outside every neighbourhood polygon.
    total_after = overlay["piece_m"].sum()
    unassigned = total_before - total_after
    unassigned_frac = unassigned / total_before if total_before else 0.0
    log = logger.warning if unassigned_frac > UNASSIGNED_WARN_FRAC else logger.info
    log(
        "Bike length conservation: %.1f km in, %.1f km assigned to neighbourhoods, "
        "%.1f km (%.2f%%) outside all boundaries",
        total_before / 1000, total_after / 1000, unassigned / 1000, 100 * unassigned_frac,
    )
    return overlay


def load_bike(bike_path: str, boundaries: gpd.GeoDataFrame) -> pd.DataFrame:
    """Overlay bike routes on boundaries → per-neighbourhood dedicated metres.

    Parameters
    ----------
    bike_path : str
        Path to the Bike Routes GeoJSON (`vd4b-a4iv`).
    boundaries : gpd.GeoDataFrame
        Output of load_boundaries — MUST carry projected geometry (EPSG:3400)
        and a `neighbourhood_name` column.

    Returns
    -------
    pd.DataFrame keyed by `neighbourhood_name` with columns:
        bike_m_onroad   — internal split (dedicated on-street lanes)
        bike_m_offroad  — internal split (dedicated paths and trails)
        bike_m_total    — the metric basis; bike_m_per_acre is computed
                          downstream in join_and_calculate against boundary
                          acres
    """
    overlay = _prepare_segments(bike_path, boundaries)

    by_type = (
        overlay.groupby(["neighbourhood_name", "onroad"])["piece_m"]
        .sum()
        .unstack(fill_value=0.0)
    )
    for flag in (True, False):
        if flag not in by_type.columns:
            by_type[flag] = 0.0

    result = pd.DataFrame(
        {
            "bike_m_onroad": by_type[True],
            "bike_m_offroad": by_type[False],
        }
    )
    result["bike_m_total"] = result["bike_m_onroad"] + result["bike_m_offroad"]
    result = result.reset_index()

    logger.info(
        "Bike overlay: %d neighbourhoods; %.1f km dedicated in the metric "
        "(%.1f km on-street, %.1f km off-road path/trail)",
        len(result),
        result["bike_m_total"].sum() / 1000,
        result["bike_m_onroad"].sum() / 1000,
        result["bike_m_offroad"].sum() / 1000,
    )
    return result


# Web-export display tunables (display geometry ONLY — every published metric
# comes from the full-resolution overlay in load_bike). The bike network is a
# CONTEXT layer: it carries no per-feature value, so it dissolves citywide the
# way load_roads' arterials do rather than per neighbourhood.
WEB_SIMPLIFY_M = 20.0   # the network is thin line-work; keep bends legible
WEB_MIN_PART_M = 20.0   # parts shorter than this are boundary-clip slivers
WEB_PRECISION = 5       # ~1 m at Edmonton's latitude


def export_bike_web(
    bike_path: str,
    boundaries: gpd.GeoDataFrame,
    out_path: str,
    simplify_m: float = WEB_SIMPLIFY_M,
    min_part_m: float = WEB_MIN_PART_M,
    precision: int = WEB_PRECISION,
) -> int:
    """Write the bike-network context layer the web map's Services view draws.

    ``{"lines": [[[lon, lat], ...], ...]}`` — the LRT-track-lines pattern
    (load_transit.export_transit_lines_web), lazy-loaded by the Services view
    and drawn as a PathLayer.

    CONTEXT ONLY, carrying no metric: the colour lives on the hood plane
    (``bike_m_per_acre``), so this file needs no per-feature properties and the
    whole dedicated network dissolves into one welded, simplified set of paths.
    Display geometry only — all metrics come from the full-resolution overlay in
    load_bike. Returns the number of path segments written.
    """
    overlay = _prepare_segments(bike_path, boundaries)

    # Weld contiguous parts end-to-end before simplifying: the raw parts are
    # short, so simplify has no interior vertices to drop until they are merged.
    # unary_union first — the overlay mixes LineString and MultiLineString, and
    # linemerge rejects a list containing multi-part geometries (the load_roads
    # arterial-dissolve pattern).
    welded = unary_union(overlay.geometry.values)
    if welded.geom_type == "MultiLineString":
        welded = linemerge(welded)
    parts = list(welded.geoms) if welded.geom_type == "MultiLineString" else [welded]

    # Drop clip slivers — display-only thinning, reported not silent.
    length_before = sum(p.length for p in parts)
    kept = [p for p in parts if p.length >= min_part_m]
    logger.info(
        "Bike web export thinning: dropped %d parts < %.0f m totalling %.1f km "
        "(display only; metrics unaffected)",
        len(parts) - len(kept), min_part_m,
        (length_before - sum(p.length for p in kept)) / 1000,
    )

    simplified = MultiLineString(kept).simplify(simplify_m, preserve_topology=True)
    geo = gpd.GeoSeries([simplified], crs=overlay.crs).to_crs(epsg=4326).iloc[0]
    segments = list(geo.geoms) if geo.geom_type == "MultiLineString" else [geo]

    lines = [
        [[round(x, precision), round(y, precision)] for x, y in seg.coords]
        for seg in segments
    ]

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        json.dump({"lines": lines}, f, separators=(",", ":"))
    logger.info(
        "Wrote bike context layer: %d path segments (%.2f MB, simplify=%sm, "
        "min part=%sm, %sdp) to %s",
        len(lines), out.stat().st_size / 1e6, simplify_m, min_part_m, precision, out_path,
    )
    return len(lines)
