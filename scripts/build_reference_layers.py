#!/usr/bin/env python3
"""Build the Tier-1 geographic reference layers the web map draws for orientation.

The map has no basemap tiles — just a dark backdrop (web/index.html, "base
map") — so a first-time viewer has nothing to orient against before engaging
with the fiscal data. This writes the shapes that make Edmonton recognizable
at a glance:

  t="river"     the North Saskatchewan River water body, clipped to the extent
  t="highway"   the motorway/trunk network, clipped to the SAME extent so it
                runs off the edge of the view rather than stopping at the city
                limit (2026-08-03; replaces the hand-extracted t="henday")
  t="boundary"  one Polygon per neighbouring municipality (PLACES), per region
                (REGIONS: Edmonton's own legal limit plus the four counties it
                abuts), and for the industrial zone — all unfilled outlines
  t="place"     one Point per named thing, carrying the text to draw

⚠️ EVERY feature now carries `kind`, and `t="boundary"` features carry `name`
(2026-08-08). Before that, all 13 outlines shipped as a bare {"t":"boundary"}
and the front end could not tell Edmonton's own legal limit from Devon's town
outline — they drew in one colour because nothing distinguished them. `kind` is
the tier the map styles on, NOT a restatement of `t`:

  kind="city"    Edmonton's own limit. Its own stroke; deliberately NOT labelled
                 (the page title already says Edmonton, and a name in the middle
                 of the choropleth is clutter, not orientation).
  kind="region"  the four counties. Labelled since 2026-08-08 — see REGIONS.
  kind="place"   the neighbouring municipalities: outline + name.
  kind="zone"    Alberta's Industrial Heartland: outline + name.
  kind="econ"    the airport and Nisku: name only, no outline. See ECON below.

Purely cartographic: no metric, no colour semantics, no tooltip. All are
STATIC geography, so this is NOT part of the weekly refresh (same posture as
scripts/build_levy_catchments.py) — the output is committed and re-run only
when the reference geography itself changes. That also honours the rule that
the Alberta endpoints are queried once at build time, never at runtime.

Sources:
  river  — Alberta base_water_feature MapServer layer 72 ("Lake/River (20K)",
           the most detailed polygon tier). NAME='North Saskatchewan River'
           isolates it cleanly: 7 polygons province-wide, all genuinely the
           river, of which only the main channel reaches Edmonton. Verified
           2026-07-26.
  highways — OpenStreetMap via Overpass (ODbL; credited in Data & Methods).
           Two other sources were tried and rejected 2026-08-03: the City
           centreline feed carries the highways but only INSIDE the city limit,
           so they stop dead at the boundary; and Alberta's
           transportation/highways_public MapServer has ideal attributes but
           returns NULL GEOMETRY on every feature in every format. See the
           HIGHWAY_URL comment.
  boundaries — the same municipality query as the places below: the outline is
           the very polygon the label anchor is derived from, so a name and the
           shape it names cannot disagree.
  places — Alberta urban_and_rural_municipality MapServer. Each name is fetched
           from the sublayer matching its LEGAL STATUS, which is why there are
           three: Sherwood Park is not a town but an urban service area of
           Strathcona County, and Devon is a town where the other five are
           cities. Verified 2026-07-27.

CRS: geometry work happens in EPSG:3400 so simplify tolerances are honest
metres — the pipeline's working CRS. Output is WGS84, because that is what
deck.gl/MapLibre consume and what every other file in web/data/ already is.

Usage:
    python scripts/build_reference_layers.py
    python scripts/build_reference_layers.py --margin-m 5000
"""
from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

import geopandas as gpd
import pandas as pd
import requests
from shapely.geometry import LineString, MultiLineString, Point, box, shape
from shapely.ops import linemerge, unary_union

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[1]
BOUNDARIES = ROOT / "data/raw/neighbourhoods.geojson"
OUT = ROOT / "web/data/reference.geojson"

WORKING_EPSG = 3400  # metres; matches the rest of the pipeline
OUT_EPSG = 4326

RIVER_URL = (
    "https://geospatial.alberta.ca/titan/rest/services/environment"
    "/base_water_feature/MapServer/72/query"
)
RIVER_NAME = "North Saskatchewan River"

# How far past the city bounding box to keep the river. It should run clean OFF
# the edge of the view in both directions rather than stopping dead — the city
# sits ON a river that comes from and goes somewhere, and a river with two
# square ends just inside the frame reads as a lake.
#
# Sized against the default camera, not guessed: at HOME zoom 10.2 and latitude
# 53.5 the scale is ~79 m/px, so a 1440px viewport spans ~114 km flat (~57 km
# from centre) and the 52 degree pitch pushes the horizon much further. The city
# half-width is only ~15 km. 60 km clears the flat view with room for the
# pitched one and for moderate zoom-out; the whole file is still only ~54 kB.
MARGIN_M = 60000.0

# --- highways -------------------------------------------------------------
# OpenStreetMap via Overpass, NOT the City centreline feed and NOT Alberta's
# highways_public service. Both were tried (2026-08-03):
#   - the City feed carries the highways, but only inside the city limit, so
#     they stop dead at the boundary — the same "two square ends read as a
#     lake" failure MARGIN_M exists to prevent for the river;
#   - Alberta's transportation/highways_public MapServer has ideal attributes
#     (510 in-service segments with ROAD_NUMBER over this extent) but returns
#     NULL GEOMETRY on every feature, in geojson and Esri JSON, with and
#     without an envelope. It answers 200 with features and no shapes, so a
#     naive reader would emit an empty highway layer and call it success.
# Overpass is queried once at build time like the Alberta services; this script
# is not part of the weekly refresh. OSM data is ODbL — the credit line in
# web/index.html's Data & Methods names it.
HIGHWAY_URL = "https://overpass-api.de/api/interpreter"

# The public Overpass instance rejects anonymous clients with 406. Identify the
# project, as its usage policy asks.
OVERPASS_USER_AGENT = "edmonton-tax-viz/1.0 (reference-layer build script)"

# The two OSM classes that mean "highway" in the orientation sense: grade-
# separated freeways (motorway) and the major intercity routes (trunk).
# `primary` is deliberately OUT — it would add 1,591 ways and 1,786 km of
# in-city arterials, tripling the file to compete with the fiscal data on a map
# that has no basemap precisely so the data reads first.
HIGHWAY_CLASSES = ("motorway", "trunk")

# Coarser than the river: these are long, near-straight runs drawn 1-2 px wide.
HIGHWAY_SIMPLIFY_M = 30.0

# Floor for the welded highway network over the clip extent. Measured 999 km
# across 1,194 ways (2026-08-03: Hwy 16 337 km, Hwy 2 213 km, Hwy 216 156 km,
# Hwy 43 131 km, then 63/28/15/16A). Set well below that — enough slack for OSM
# edits, tight enough that losing a major route trips it.
HIGHWAY_MIN_KM = 700.0

# Cross-check on the replacement: the retired City-feed extraction yielded
# 149 km for the ring's two carriageways, and OSM's Highway 216 is 156 km.
# Agreement within ~5% is what justified dropping the hand-tuned extractor.
HIGHWAY_RING_REF_KM = 156.0

# Municipal outlines are background context at ~1 px; 100 m costs 169 vertices
# for the seven places (~3.6 kB) and nothing visible. The five REGIONS below are
# far larger shapes and cost ~35 kB at the same tolerance — still cheap for a
# static committed file, and 100 m is ~2 px at city zoom, so coarsening further
# would start to show on a border.
BOUNDARY_SIMPLIFY_M = 100.0

PLACE_URL = (
    "https://geospatial.alberta.ca/titan/rest/services/base"
    "/urban_and_rural_municipality/MapServer/{layer}/query"
)

# The neighbouring places named on the map, as a closed enumeration with the
# sublayer each one legally lives in — NOT a bbox sweep of every municipality
# near Edmonton. Which names belong on the map is a cartographic judgement
# (how populated should the frame feel?), so it is stated, not derived: a
# radius query would silently gain and lose names as the province edits
# boundaries, and the map's composition would drift with it.
#
# Three sublayers because Alberta models municipal STATUS, not size:
#   78 City               St. Albert, Spruce Grove, Fort Saskatchewan,
#                         Leduc, Beaumont (a city since 2019)
#   56 Town               Devon
#   66 Urban Service Area Sherwood Park — a hamlet-like urban service area of
#                         Strathcona County, so it is in NEITHER the City nor
#                         the Town layer. Looking for it there finds nothing.
# Note layer 66 also holds "Sherwood Park (Bremner)", a separate future-growth
# polygon ~10 km east; the exact-name match excludes it deliberately.
PLACES = (
    ("St. Albert", 78, "CITY_NAME"),
    ("Sherwood Park", 66, "USA_NAME"),
    ("Spruce Grove", 78, "CITY_NAME"),
    ("Fort Saskatchewan", 78, "CITY_NAME"),
    ("Leduc", 78, "CITY_NAME"),
    ("Beaumont", 78, "CITY_NAME"),
    ("Devon", 56, "TOWN_NAME"),
    # Added 2026-08-08 with the regional-narrative pass: the two incorporated
    # towns that were missing from the neighbour set. Both are Towns, so they
    # share Devon's sublayer.
    ("Morinville", 56, "TOWN_NAME"),
    ("Stony Plain", 56, "TOWN_NAME"),
)

# Economic geography, added 2026-08-08 — NOT municipalities, and that is the
# point of them: the airport and the Nisku industrial park are regional
# infrastructure sitting in LEDUC COUNTY, so Edmonton does not tax them. They
# are drawn as bare labels with no outline, which is both simpler and more
# honest than it looks:
#   Nisku is a HAMLET. Alberta publishes hamlets as points only (sublayer 7,
#     CULPT_NAME) — it has no legal polygon to draw, so a point is the whole
#     of what exists.
#   The airport HAS a polygon in OSM, but it is a ~28 km² shape 40 km south of
#     the city drawn at 1 px. Naming it locates it; tracing it does not, and an
#     outline in the municipal grey would read as one more jurisdiction.
# Fetched by IATA code rather than by name: `name` gets edited in OSM, `iata`
# does not.
NISKU = ("Nisku", 7, "CULPT_NAME")
AIRPORT_IATA = "YEG"
AIRPORT_LABEL = "Edmonton Int'l Airport"
# Where to look for it. Tight on purpose — a province-wide aerodrome query
# times out on the public Overpass instance (observed 504, 2026-08-08).
AIRPORT_BBOX = (53.24, -113.68, 53.36, -113.50)  # S, W, N, E

# Alberta's Industrial Heartland, as the province actually publishes it.
#
# ⚠️ THE SERVICE DOES NOT CARRY THE NAME. It is a single unnamed 590.7 km²
# MultiPolygon in a layer called `resource_designated_industrial_zone`, with no
# name field at all — so the identification is OURS and was made by measuring
# who it overlaps, not by reading a label off the source:
#   Sturgeon County 171.8 · Strathcona County 134.3 · EDMONTON 53.2 ·
#   Fort Saskatchewan 29.5 km², remainder ≈ Lamont County (not in this layer).
# That is exactly the Heartland's member set, and 590.7 km² matches the ~582 km²
# the association publishes. Recorded in data/DATA.md §14 so the inference is
# visible rather than implied by the label.
#
# ⚠️ **53.2 km² of it is inside Edmonton's own boundary**, so this is NOT a
# clean "regional infrastructure Edmonton doesn't tax" shape the way the airport
# and Nisku are. Do not narrate it as one.
ZONE_URL = (
    "https://geospatial.alberta.ca/titan/rest/services/boundaries"
    "/resource_designated_industrial_zone/MapServer/0/query"
)
ZONE_LABEL = "Industrial Heartland"
ZONE_MIN_KM2 = 400.0   # measured 590.7; trips loudly if the layer is repointed

# The city's own legal limit and the rural municipalities it abuts, where the
# EDGE is the payload rather than the small-polygon-plus-name of PLACES.
#
# ⚠️ **REGIONS ARE LABELLED AS OF 2026-08-08, REVERSING THE ORIGINAL DECISION.**
# This comment used to argue they should not be: "far too large to label
# sensibly at city zoom (Parkland County alone is 2,755 km², 3.5x Edmonton), and
# a county name is not what the outline is saying — the message is 'the city
# ends here, and there is more past it'." That reasoning holds for an
# ORIENTATION map and fails for a REGIONAL one (Peter, 2026-08-08): once the
# question is fiscal — who else levies here, and what does Edmonton not tax —
# an unnamed edge cannot answer it. See docs/DECISIONS.md 2026-08-08.
#
# ⚠️ The old objection was still half right, and the anchor is where it gets
# paid: a county CENTROID sits 27–58 km from Edmonton's centre and would put
# every name off-screen at the default camera. `_region_anchor` places the label
# on the county's visible strip near the city instead. Do not "simplify" it back
# to a centroid.
#
# Edmonton is in this list because the map has never drawn its own limit: what
# reads as the city edge is only where the neighbourhood polygons stop.
# Measured 2026-08-08 — the legal boundary is 782.1 km² against 672.4 km² of
# hood fabric, so 109.6 km² (14.0% of Edmonton) lies inside the city and is
# absent from the map: annexed and undeveloped land carrying no neighbourhood.
# Nothing is drawn OUTSIDE the legal limit (0.0 km²), so the fabric is strictly
# contained and the map understates the city's extent rather than overstating
# it. Drawing the limit is what makes that 14% visible as empty space instead of
# reading as background.
#
# Sublayers follow legal STATUS again, not size — and the trap is different from
# the PLACES one:
#   78  City                     Edmonton
#   104 Specialized Municipality Strathcona County — NOT 114. Alberta models
#                                specialized municipalities separately, so the
#                                obvious county layer does not contain it.
#   114 Municipal District/County Sturgeon, Parkland, Leduc County
# Note Leduc appears twice across the two lists and they are different polygons:
# the CITY of Leduc (PLACES, layer 78) sits inside LEDUC COUNTY (here, 114).
REGIONS = (
    ("Edmonton", 78, "CITY_NAME"),
    ("Strathcona County", 104, "SPMUN_NAME"),
    ("Sturgeon County", 114, "MD_NAME"),
    ("Parkland County", 114, "MD_NAME"),
    ("Leduc County", 114, "MD_NAME"),
)

# Simplify tolerances (metres). Both layers are unlabelled background context
# drawn 1-2 px wide, so they can be far coarser than the road network's 20/40 m
# — at city zoom one pixel is ~50 m and none of this detail survives anyway.
RIVER_SIMPLIFY_M = 25.0

# Coordinate decimals (~1 m at Edmonton's latitude) — matches load_roads.
PRECISION = 5

# How wide a band around the city a county label may sit in (see _region_anchor).
# Much tighter than MARGIN_M: that one sizes the RIVER so it runs off the frame,
# this one keeps a name near the edge it belongs to. At 12 km every county gets
# an anchor in the band a viewer is looking at, without pushing Parkland's name
# 58 km west to its true centroid.
REGION_ANCHOR_MARGIN_M = 12000.0


def _fetch_river(bounds_4326: tuple[float, float, float, float]) -> gpd.GeoDataFrame:
    """Query the Alberta hydrography service for the river within `bounds_4326`.

    Asks the server for the intersecting subset rather than pulling the
    province-wide feature (2.6 MB) and clipping locally.
    """
    minx, miny, maxx, maxy = bounds_4326
    params = {
        "where": f"NAME='{RIVER_NAME}'",
        "geometry": f"{minx},{miny},{maxx},{maxy}",
        "geometryType": "esriGeometryEnvelope",
        "inSR": 4326,
        "spatialRel": "esriSpatialRelIntersects",
        "outFields": "NAME",
        "returnGeometry": "true",
        "f": "geojson",
    }
    logger.info("Fetching %s from the Alberta hydrography service…", RIVER_NAME)
    resp = requests.get(RIVER_URL, params=params, timeout=180)
    resp.raise_for_status()
    payload = resp.json()

    # ArcGIS reports query errors inside a 200 response — check explicitly
    # rather than letting an error object parse as an empty FeatureCollection.
    if "error" in payload:
        raise RuntimeError(f"ArcGIS query failed: {payload['error']}")
    feats = payload.get("features") or []
    if not feats:
        raise RuntimeError(
            f"No {RIVER_NAME!r} features returned for the Edmonton extent — "
            "the service schema or NAME value may have changed."
        )
    if payload.get("exceededTransferLimit"):
        raise RuntimeError(
            "Server truncated the river query (exceededTransferLimit) — the "
            "result would be a partial river drawn as if complete."
        )

    gdf = gpd.GeoDataFrame.from_features(feats, crs=f"EPSG:{OUT_EPSG}")
    logger.info("  %d river polygon(s) returned", len(gdf))
    return gdf.to_crs(epsg=WORKING_EPSG)


def _fetch_highways(bounds_4326: tuple[float, float, float, float]) -> gpd.GeoDataFrame:
    """Query Overpass for motorway/trunk ways within `bounds_4326`.

    Returns the ways in WORKING_EPSG with their `ref` (road number, e.g. "216")
    for reporting only — the emitted layer carries no per-feature attributes,
    the same posture as the river.
    """
    minx, miny, maxx, maxy = bounds_4326
    classes = "|".join(HIGHWAY_CLASSES)
    query = (
        f"[out:json][timeout:180];"
        f'(way["highway"~"^({classes})$"]'
        f"({miny:.4f},{minx:.4f},{maxy:.4f},{maxx:.4f}););"
        f"out geom;"
    )
    logger.info("Fetching %s ways from Overpass…", "/".join(HIGHWAY_CLASSES))
    # Form-encoded `data=`, with a named User-Agent: a raw body or an anonymous
    # client gets 406 Not Acceptable from the public instance.
    resp = requests.post(
        HIGHWAY_URL,
        data={"data": query},
        headers={"User-Agent": OVERPASS_USER_AGENT},
        timeout=300,
    )
    resp.raise_for_status()
    payload = resp.json()

    elements = payload.get("elements") or []
    if not elements:
        raise RuntimeError(
            "Overpass returned no highway ways for the Edmonton extent — the "
            "query or the tagging may have changed. An empty highway layer "
            "would look like a successful build."
        )

    rows, refs, skipped = [], [], 0
    for el in elements:
        geom = el.get("geometry")
        # `out geom` omits geometry for ways the server could not resolve.
        # Count them rather than letting them vanish (no silent drops).
        if not geom or len(geom) < 2:
            skipped += 1
            continue
        rows.append(LineString([(p["lon"], p["lat"]) for p in geom]))
        refs.append((el.get("tags") or {}).get("ref"))
    if skipped:
        logger.warning("Overpass returned %d way(s) without usable geometry", skipped)
    if not rows:
        raise RuntimeError("Every Overpass way lacked geometry — nothing to draw.")

    gdf = gpd.GeoDataFrame(
        {"ref": refs}, geometry=rows, crs=f"EPSG:{OUT_EPSG}"
    ).to_crs(epsg=WORKING_EPSG)
    by_ref = (gdf.assign(km=gdf.geometry.length / 1000)
                 .groupby("ref", dropna=False)["km"].sum().sort_values(ascending=False))
    logger.info(
        "Highways: %d ways, %.1f km; top routes %s",
        len(gdf), by_ref.sum(),
        ", ".join(f"{r if isinstance(r, str) else 'unnumbered'} {k:.0f}km"
                  for r, k in by_ref.head(5).items()),
    )

    # The retired City-feed extractor produced 149 km for the ring. If OSM's
    # 216 has drifted far from that, the replacement is no longer the same road
    # and the discrepancy should be looked at, not averaged away.
    ring_km = float(by_ref.get("216", 0.0))
    if abs(ring_km - HIGHWAY_RING_REF_KM) > 0.25 * HIGHWAY_RING_REF_KM:
        logger.warning(
            "Highway 216 is %.1f km, vs the %.0f km the retired City-feed "
            "extraction measured — check the ring is intact.",
            ring_km, HIGHWAY_RING_REF_KM,
        )
    return gdf


def _largest_polygon(name: str, layer: int, field: str):
    """The largest polygon of one municipality, in WORKING_EPSG.

    Shared by PLACES and REGIONS: both ask this service the same way and differ
    only in what they do with the shape afterwards.
    """
    resp = requests.get(
        PLACE_URL.format(layer=layer),
        params={
            # Doubling is the SQL escape for a literal quote. None of the
            # current names contain one; this keeps that from becoming a
            # silent failure if a "St. Paul'"-style name is ever added.
            "where": f"{field}='{name.replace(chr(39), chr(39) * 2)}'",
            "outFields": field,
            "returnGeometry": "true",
            "outSR": OUT_EPSG,
            "f": "geojson",
        },
        timeout=180,
    )
    resp.raise_for_status()
    payload = resp.json()
    if "error" in payload:
        raise RuntimeError(f"ArcGIS query failed for {name!r}: {payload['error']}")
    feats = payload.get("features") or []
    if not feats:
        raise RuntimeError(
            f"No geometry returned for {name!r} in sublayer {layer} "
            f"({field}) — the name or its municipal status may have changed. "
            "A shape that silently vanishes leaves a hole in the map's "
            "orientation with nothing to signal it."
        )
    geom = gpd.GeoSeries(
        [shape(f["geometry"]) for f in feats], crs=f"EPSG:{OUT_EPSG}"
    ).to_crs(epsg=WORKING_EPSG).union_all()
    return max(getattr(geom, "geoms", [geom]), key=lambda p: p.area)


def _fetch_point(name: str, layer: int, field: str):
    """One named POINT from the Alberta municipality service, in WORKING_EPSG.

    The point-layer sibling of `_largest_polygon`, for the entries that have no
    polygon to take a centroid from — Alberta publishes hamlets as points.
    """
    resp = requests.get(
        PLACE_URL.format(layer=layer),
        params={
            "where": f"{field}='{name.replace(chr(39), chr(39) * 2)}'",
            "outFields": field,
            "returnGeometry": "true",
            "outSR": OUT_EPSG,
            "f": "geojson",
        },
        timeout=180,
    )
    resp.raise_for_status()
    payload = resp.json()
    if "error" in payload:
        raise RuntimeError(f"ArcGIS query failed for {name!r}: {payload['error']}")
    feats = payload.get("features") or []
    if not feats:
        raise RuntimeError(
            f"No point returned for {name!r} in sublayer {layer} ({field}) — "
            "the name or its status may have changed."
        )
    return (
        gpd.GeoSeries([shape(feats[0]["geometry"])], crs=f"EPSG:{OUT_EPSG}")
        .to_crs(epsg=WORKING_EPSG).iloc[0]
    )


def _fetch_airport() -> Point:
    """The airport's centre from OSM, by IATA code, as a bare label anchor.

    `out center;` rather than `out geom;` on purpose: the aerodrome is an OSM
    RELATION, so a real outline would mean assembling its member ways, and the
    outline is not wanted anyway (see the ECON note above). The centre is the
    whole payload.
    """
    south, west, north, east = AIRPORT_BBOX
    query = (
        f"[out:json][timeout:90];"
        f'(way["aeroway"="aerodrome"]["iata"="{AIRPORT_IATA}"]'
        f"({south},{west},{north},{east});"
        f'relation["aeroway"="aerodrome"]["iata"="{AIRPORT_IATA}"]'
        f"({south},{west},{north},{east}););"
        f"out tags center;"
    )
    logger.info("Fetching %s from Overpass…", AIRPORT_IATA)
    resp = requests.post(
        HIGHWAY_URL,
        data={"data": query},
        headers={"User-Agent": OVERPASS_USER_AGENT},
        timeout=300,
    )
    resp.raise_for_status()
    for el in resp.json().get("elements") or []:
        centre = el.get("center") or {}
        if "lat" in centre and "lon" in centre:
            return (
                gpd.GeoSeries(
                    [Point(centre["lon"], centre["lat"])], crs=f"EPSG:{OUT_EPSG}"
                ).to_crs(epsg=WORKING_EPSG).iloc[0]
            )
    raise RuntimeError(
        f"Overpass returned no aerodrome with iata={AIRPORT_IATA} in the "
        "airport bbox. A missing label would look like a successful build."
    )


def _fetch_zone():
    """Alberta's Industrial Heartland outline, in WORKING_EPSG.

    One unnamed feature in the whole layer, so `where=1=1` IS the query. The
    area check is the guard: this service carries no name to assert against, so
    size is the only handle on "did the layer get repointed at something else".
    """
    resp = requests.get(
        ZONE_URL,
        params={"where": "1=1", "returnGeometry": "true",
                "outSR": OUT_EPSG, "f": "geojson"},
        timeout=180,
    )
    resp.raise_for_status()
    payload = resp.json()
    if "error" in payload:
        raise RuntimeError(f"ArcGIS query failed for the industrial zone: {payload['error']}")
    feats = payload.get("features") or []
    if not feats:
        raise RuntimeError("The designated-industrial-zone layer returned nothing.")
    geom = gpd.GeoSeries(
        [shape(f["geometry"]) for f in feats], crs=f"EPSG:{OUT_EPSG}"
    ).to_crs(epsg=WORKING_EPSG).union_all()
    km2 = geom.area / 1e6
    if km2 < ZONE_MIN_KM2:
        raise RuntimeError(
            f"The designated industrial zone came back as {km2:.1f} km², under "
            f"the {ZONE_MIN_KM2:.0f} km² floor (measured 590.7). The layer may "
            "no longer be the shape we identified as the Heartland."
        )
    logger.info("  %-20s %6.0f km²", ZONE_LABEL, km2)
    return geom.simplify(BOUNDARY_SIMPLIFY_M, preserve_topology=True)


def _region_anchor(region, anchor_box):
    """Where a county's name goes: on the strip of it nearest the city.

    ⚠️ NOT the centroid — that is the whole reason this function exists. The
    county centroids sit 27-58 km from Edmonton's centre (Parkland's is 58 km
    west), so centroid labels land off the edge of the default camera and the
    names simply never appear. Clipping to a band around the city first puts the
    label on the part a viewer is actually looking at.

    Falls back to the region's own representative point if the clip is empty —
    a region that does not reach the band at all still gets a label rather than
    silently losing one.
    """
    visible = region.intersection(anchor_box)
    if visible.is_empty:
        return region.representative_point()
    biggest = max(getattr(visible, "geoms", [visible]), key=lambda p: p.area)
    return biggest.representative_point()


def _fetch_regions() -> list:
    """One unlabelled outline per entry in REGIONS.

    NOT clipped to the view extent, unlike the river and the highways. Those are
    clipped because they are open shapes that would otherwise stop dead in the
    middle of the frame. A municipality is a closed ring, and clipping one would
    replace its far side with a straight run along the clip box that draws as if
    it were a real border. Parkland County is the only one that leaves the
    extent (66.7% inside, measured 2026-08-08); letting it run off the edge is
    the same effect MARGIN_M buys for the river.
    """
    logger.info("Fetching %d regional outlines…", len(REGIONS))
    out = []
    for name, layer, field in REGIONS:
        biggest = _largest_polygon(name, layer, field)
        logger.info(
            "  %-20s %6.0f km² from sublayer %d", name, biggest.area / 1e6, layer
        )
        out.append((name, biggest.simplify(BOUNDARY_SIMPLIFY_M, preserve_topology=True)))
    return out


def _fetch_places() -> gpd.GeoDataFrame:
    """One label anchor per entry in PLACES, from the Alberta municipality service.

    The anchor is the centroid of the place's largest polygon — the same rule
    labelAnchors() uses for neighbourhoods in web/index.html, so a regional
    name and a hood name are positioned by one convention rather than two.
    Falls back to a representative point for any shape whose centroid lands
    outside it (a crescent-shaped boundary would otherwise label the hole).
    """
    logger.info("Fetching %d regional place anchors…", len(PLACES))
    names, points, outlines = [], [], []
    for name, layer, field in PLACES:
        biggest = _largest_polygon(name, layer, field)
        anchor = biggest.centroid
        if not biggest.contains(anchor):
            anchor = biggest.representative_point()
        logger.info(
            "  %-20s %5.1f km² from sublayer %d", name, biggest.area / 1e6, layer
        )
        names.append(name)
        points.append(anchor)
        # The same largest polygon the anchor came from, kept as the drawn
        # outline — so the label and the shape it names can never disagree.
        outlines.append(biggest.simplify(BOUNDARY_SIMPLIFY_M, preserve_topology=True))

    return gpd.GeoDataFrame(
        {"name": names, "outline": outlines},
        geometry=points, crs=f"EPSG:{WORKING_EPSG}",
    )


def _weld(geoms) -> "gpd.base.BaseGeometry":
    """Dissolve segments into as few continuous lines as possible."""
    merged = unary_union(list(geoms))
    if merged.geom_type == "MultiLineString":
        merged = linemerge(merged)
    return merged


def _round_coords(obj, precision: int):
    if isinstance(obj, (list, tuple)):
        if obj and isinstance(obj[0], float):
            return [round(c, precision) for c in obj]
        return [_round_coords(o, precision) for o in obj]
    return obj


def build(
    boundaries_path: Path = BOUNDARIES,
    out_path: Path = OUT,
    margin_m: float = MARGIN_M,
    precision: int = PRECISION,
) -> int:
    """Write web/data/reference.geojson. Returns the feature count."""
    hoods = gpd.read_file(boundaries_path).to_crs(epsg=WORKING_EPSG)
    minx, miny, maxx, maxy = hoods.total_bounds
    clip_box = box(minx - margin_m, miny - margin_m, maxx + margin_m, maxy + margin_m)
    clip_4326 = (
        gpd.GeoSeries([clip_box], crs=f"EPSG:{WORKING_EPSG}")
        .to_crs(epsg=OUT_EPSG).total_bounds
    )
    logger.info(
        "Clip extent: city bbox + %.0f m margin (%.4f,%.4f,%.4f,%.4f WGS84)",
        margin_m, *clip_4326,
    )

    # --- river: clip to the view extent, then dissolve to one feature --------
    river = _fetch_river(tuple(clip_4326))
    river_geom = unary_union(list(river.geometry)).intersection(clip_box)
    if river_geom.is_empty:
        raise RuntimeError("River geometry is empty after clipping to the city extent.")
    river_geom = river_geom.simplify(RIVER_SIMPLIFY_M, preserve_topology=True)
    logger.info(
        "River: %.1f km² within the extent, %d part(s) after clip+simplify",
        river_geom.area / 1e6,
        len(getattr(river_geom, "geoms", [river_geom])),
    )

    # --- highways: clip to the same extent as the river, weld, simplify ------
    # Clipped to clip_box, not just the query bbox, so the highways END WHERE
    # THE RIVER ENDS. Both run off the edge of the view rather than stopping at
    # the city limit — the whole point of using OSM over the City feed.
    highways = _fetch_highways(tuple(clip_4326))
    raw_km = highways.geometry.length.sum() / 1000
    clipped = highways.geometry.intersection(clip_box)
    clipped = clipped[~clipped.is_empty & clipped.notna()]
    welded = _weld(clipped).simplify(HIGHWAY_SIMPLIFY_M, preserve_topology=True)
    highway_geom = (
        welded if welded.geom_type == "MultiLineString" else MultiLineString([welded])
    )
    highway_km = highway_geom.length / 1000
    logger.info(
        "Highways: %.1f km raw -> %.1f km welded in %d part(s) after clip+simplify",
        raw_km, highway_km, len(highway_geom.geoms),
    )
    if highway_km < HIGHWAY_MIN_KM:
        logger.warning(
            "Welded highway length %.1f km is below the %.0f km floor — a major "
            "route may be missing.",
            highway_km, HIGHWAY_MIN_KM,
        )

    # --- the named things ----------------------------------------------------
    # Assembled as (t, kind, name, geometry) rows so every feature declares its
    # own tier. Before 2026-08-08 the outlines were emitted as one anonymous
    # block and the map could not tell them apart — see the schema note in the
    # module docstring.
    places = _fetch_places()
    regions = _fetch_regions()
    zone = _fetch_zone()

    anchor_box = box(minx - REGION_ANCHOR_MARGIN_M, miny - REGION_ANCHOR_MARGIN_M,
                     maxx + REGION_ANCHOR_MARGIN_M, maxy + REGION_ANCHOR_MARGIN_M)

    # km² rides along on every label anchor that names a shape. ⚠️ This is not
    # decoration: the front end's declutter sweep sorts by (priority, area), and
    # every reference label used to carry area 0 — so same-tier names tied and
    # fell out IN FILE ORDER, which is how 5 of 7 places silently vanished at
    # z=7 (the note beside PLACE_MIN_SIZE in web/index.html). Adding nine more
    # names would have made an arbitrary rule arbitrary more often. Points with
    # no shape (econ) legitimately have none.
    rows: list[tuple[str, str, str | None, float | None, object]] = [
        ("river", "river", None, None, river_geom),
        ("highway", "highway", None, None, highway_geom),
    ]

    for name, outline in zip(places["name"], places["outline"]):
        rows.append(("boundary", "place", name, None, outline))
    for point, name, outline in zip(places.geometry, places["name"], places["outline"]):
        rows.append(("place", "place", name, outline.area / 1e6, point))

    for name, outline in regions:
        # Edmonton is the one region drawn but not named: the page title says
        # Edmonton already, and a label at the centre would sit on top of the
        # choropleth it exists to frame. Its EDGE is the payload — 14% of the
        # city has no neighbourhood polygon, and this is the line that shows it.
        is_city = name == "Edmonton"
        rows.append(("boundary", "city" if is_city else "region", name, None, outline))
        if not is_city:
            rows.append(("place", "region", name, outline.area / 1e6,
                         _region_anchor(outline, anchor_box)))

    rows.append(("boundary", "zone", ZONE_LABEL, None, zone))
    rows.append(("place", "zone", ZONE_LABEL, zone.area / 1e6,
                 _region_anchor(zone, anchor_box)))

    # Label-only, no outline (see the ECON note above).
    rows.append(("place", "econ", NISKU[0], None, _fetch_point(*NISKU)))
    rows.append(("place", "econ", AIRPORT_LABEL, None, _fetch_airport()))

    out_gdf = gpd.GeoDataFrame(
        {"t": [r[0] for r in rows],
         "kind": [r[1] for r in rows],
         "nm": [r[2] for r in rows],
         "km2": [r[3] for r in rows]},
        geometry=[r[4] for r in rows],
        crs=f"EPSG:{WORKING_EPSG}",
    ).to_crs(epsg=OUT_EPSG)

    features = []
    for row in out_gdf.itertuples():
        geom = row.geometry.__geo_interface__
        props = {"t": row.t, "kind": row.kind}
        if row.km2 == row.km2 and row.km2 is not None:   # nan-safe
            props["km2"] = round(float(row.km2), 1)
        # `nm`, not `name`: itertuples exposes the row INDEX as `.name`, so a
        # column actually called `name` is shadowed and every label silently
        # becomes an integer. Also isinstance rather than `is not None` —
        # pandas coerces the unnamed features' Nones to float nan in this mixed
        # column, and nan passes an `is not None` test, which would emit a bare
        # NaN token: invalid JSON, and JSON.parse then drops the WHOLE file.
        if isinstance(row.nm, str):
            props["name"] = row.nm
        features.append({
            "type": "Feature",
            "properties": props,
            "geometry": {
                "type": geom["type"],
                "coordinates": _round_coords(geom["coordinates"], precision),
            },
        })

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(
        {"type": "FeatureCollection", "features": features}, separators=(",", ":")
    ))
    logger.info(
        "Wrote %d reference features (%.0f kB, %sdp) to %s",
        len(features), out_path.stat().st_size / 1e3, precision, out_path,
    )
    return len(features)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--boundaries", type=Path, default=BOUNDARIES)
    p.add_argument("--out", type=Path, default=OUT)
    p.add_argument("--margin-m", type=float, default=MARGIN_M,
                   help="how far past the city bbox to keep the river")
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    build(args.boundaries, args.out, args.margin_m)


if __name__ == "__main__":
    main()
