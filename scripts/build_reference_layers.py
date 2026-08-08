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
  t="boundary"  one Polygon per neighbouring municipality (PLACES) AND per
                region (REGIONS: Edmonton's own legal limit plus the four
                counties it abuts), all drawn as unfilled outlines
  t="place"     one Point per neighbouring municipality, carrying its name

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
)

# Outlines drawn WITHOUT a label, unlike PLACES above — two different jobs:
#   PLACES  a named town, where the point and the outline describe the same
#           small polygon and the NAME is the payload.
#   REGIONS the city's own legal limit and the rural municipalities it abuts,
#           where the EDGE is the payload. These are far too large to label
#           sensibly at city zoom (Parkland County alone is 2,755 km², 3.5x
#           Edmonton), and a county name is not what the outline is saying —
#           the message is "the city ends here, and there is more past it".
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
    outlines = []
    for name, layer, field in REGIONS:
        biggest = _largest_polygon(name, layer, field)
        logger.info(
            "  %-20s %6.0f km² from sublayer %d", name, biggest.area / 1e6, layer
        )
        outlines.append(biggest.simplify(BOUNDARY_SIMPLIFY_M, preserve_topology=True))
    return outlines


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

    # --- places: a named point AND an outline per neighbouring municipality --
    places = _fetch_places()
    # --- regions: Edmonton's own limit + the counties it abuts, unlabelled ----
    # Emitted as the same t="boundary" kind: identical treatment on the map (a
    # faint unfilled line under the data), so splitting the type would buy a
    # second render path for one colour they already share.
    outlines = list(places["outline"]) + _fetch_regions()

    out_gdf = gpd.GeoDataFrame(
        {
            "t": (["river", "highway"] + ["boundary"] * len(outlines)
                  + ["place"] * len(places)),
            # Only places carry a name. Boundaries are deliberately unlabelled:
            # the place point already sits inside its own outline, so naming
            # both would print every regional name twice.
            "name": ([None, None] + [None] * len(outlines) + list(places["name"])),
        },
        geometry=[river_geom, highway_geom] + outlines + list(places.geometry),
        crs=f"EPSG:{WORKING_EPSG}",
    ).to_crs(epsg=OUT_EPSG)

    features = []
    for row in out_gdf.itertuples():
        geom = row.geometry.__geo_interface__
        props = {"t": row.t}
        # isinstance, not `is not None`: pandas coerces the unnamed features'
        # Nones (river, highway, every boundary) to float nan in this mixed
        # column, and nan passes an `is not None` test — which would emit a
        # bare NaN token that is invalid JSON and fails JSON.parse in the
        # browser for the whole file.
        if isinstance(row.name, str):
            props["name"] = row.name
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
