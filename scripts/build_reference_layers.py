#!/usr/bin/env python3
"""Build the Tier-1 geographic reference layers the web map draws for orientation.

The map has no basemap tiles — just a dark backdrop (web/index.html, "base
map") — so a first-time viewer has nothing to orient against before engaging
with the fiscal data. This writes the two shapes that make Edmonton
recognizable at a glance:

  t="river"   the North Saskatchewan River water body, clipped to the map extent
  t="henday"  Anthony Henday Drive (Highway 216), the ring road
  t="place"   one Point per neighbouring municipality, carrying its name

Purely cartographic: no metric, no colour semantics, no tooltip. Both are
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
  henday — the EXISTING data/raw/roads.geojson. No new source: the Henday is
           in the City's centreline feed as 518 `Province of Alberta` rows.
           load_roads filters those out (it measures City-maintained road
           supply), which is why the ring never appears on the services map.
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
from shapely.geometry import MultiLineString, Point, box, shape
from shapely.ops import linemerge, unary_union

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[1]
BOUNDARIES = ROOT / "data/raw/neighbourhoods.geojson"
ROADS = ROOT / "data/raw/roads.geojson"
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

# Anthony Henday Drive carries two names in the centreline feed: the road name
# on most of the ring, and its provincial designation on the north-east leg.
# Matched as full substrings, deliberately: a bare "216" also hits
# "216 STREET NW", and a bare "ANTHONY" hits "ANTHONY CRESCENT SW".
HENDAY_PATTERNS = ("ANTHONY HENDAY", "HIGHWAY 216")

# CONCURRENCY. Name-matching alone leaves a 2.9 km hole in the east leg — 73
# screen pixels at the default zoom, which reads as a broken ring rather than
# as missing data. The road is there; for that stretch Highway 216 runs
# concurrent with Highway 14, and the feed labels the shared carriageway for
# Highway 14 only. (Confirmed by probing the hole: every sample point sits
# 1-35 m from a HIGHWAY 14 centreline.)
#
# Only the north/southbound carriageways are the concurrency — the ring runs
# north-south here. HIGHWAY 14 EASTBOUND/WESTBOUND is Highway 14 genuinely
# heading east away from the ring, and including it would grow a 5 km spur.
# Hence exact full names, not a "HIGHWAY 14" substring.
HENDAY_CONCURRENT_NAMES = frozenset({
    "HIGHWAY 14 NORTHBOUND",
    "HIGHWAY 14 SOUTHBOUND",
})

# Mainline-only, as an EXPLICIT segment-type allowlist (the load_roads
# philosophy: a closed enumeration, never a keyword/prefix heuristic).
#
# Name-matching alone pulls 275.7 km across 590 segments — every entrance and
# exit ramp, right-turn cutoff and collector-distributor lane is *named* for
# the highway it serves. Drawn thin at city zoom that renders as a tangle of
# spurs at each interchange rather than a ring. The three types below are
# 149.2 km, which is the ~75 km ring times its two carriageways.
#
# The two Structure types are IN, not out: they are the mainline where it
# bridges the river or flies over a cross street. Dropping them would open a
# gap in the ring at every crossing.
HENDAY_MAINLINE_TYPES = frozenset({
    "Roadway (Standard)",     # 144.9 km — the ring itself
    "Structure - Overpass",   #   2.8 km — mainline over a cross street
    "Structure - Bridge",     #   1.5 km — mainline over the river
})

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

# Simplify tolerances (metres). Both layers are unlabelled background context
# drawn 1-2 px wide, so they can be far coarser than the road network's 20/40 m
# — at city zoom one pixel is ~50 m and none of this detail survives anyway.
RIVER_SIMPLIFY_M = 25.0
HENDAY_SIMPLIFY_M = 30.0

# Coordinate decimals (~1 m at Edmonton's latitude) — matches load_roads.
PRECISION = 5

# The mainline extract is ~149 km: a ~75 km ring drawn as two carriageways.
# Warn well below that — enough slack for a feed revision, tight enough that a
# missing leg of the ring (~30 km) trips it.
HENDAY_MIN_KM = 120.0

# Welded endpoints closer than this count as the same node (the feed's
# coordinates are sub-metre, so this is slack for the simplify pass).
RING_CLOSURE_TOLERANCE_M = 50.0


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


def _fetch_places() -> gpd.GeoDataFrame:
    """One label anchor per entry in PLACES, from the Alberta municipality service.

    The anchor is the centroid of the place's largest polygon — the same rule
    labelAnchors() uses for neighbourhoods in web/index.html, so a regional
    name and a hood name are positioned by one convention rather than two.
    Falls back to a representative point for any shape whose centroid lands
    outside it (a crescent-shaped boundary would otherwise label the hole).
    """
    logger.info("Fetching %d regional place anchors…", len(PLACES))
    names, points = [], []
    for name, layer, field in PLACES:
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
                "A place that silently vanishes leaves a hole in the map's "
                "orientation with nothing to signal it."
            )

        geom = gpd.GeoSeries(
            [shape(f["geometry"]) for f in feats], crs=f"EPSG:{OUT_EPSG}"
        ).to_crs(epsg=WORKING_EPSG).union_all()
        biggest = max(getattr(geom, "geoms", [geom]), key=lambda p: p.area)
        anchor = biggest.centroid
        if not biggest.contains(anchor):
            anchor = biggest.representative_point()
        logger.info(
            "  %-20s %5.1f km² from sublayer %d", name, biggest.area / 1e6, layer
        )
        names.append(name)
        points.append(anchor)

    return gpd.GeoDataFrame(
        {"name": names}, geometry=points, crs=f"EPSG:{WORKING_EPSG}"
    )


def _load_henday(roads_path: Path) -> gpd.GeoDataFrame:
    """Extract the Anthony Henday / Highway 216 centrelines from the road feed."""
    logger.info("Reading the road centreline feed (%s)…", roads_path.name)
    roads = gpd.read_file(roads_path)
    if roads.crs is None:
        logger.warning("Roads CRS missing — assuming EPSG:4326")
        roads = roads.set_crs(epsg=4326)

    name = roads["street_name_full"].fillna("")
    match = pd.Series(False, index=roads.index)
    for pat in HENDAY_PATTERNS:
        hits = name.str.contains(pat, case=False, regex=False)
        logger.info("  %-22s %d segments", pat, int(hits.sum()))
        match |= hits
    concurrent = name.isin(HENDAY_CONCURRENT_NAMES)
    logger.info("  %-22s %d segments (Hwy 216/14 concurrency)",
                "HIGHWAY 14 N/S", int(concurrent.sum()))
    match |= concurrent

    named = roads.loc[match & (roads["centerline_type"] == "Road")]
    if named.empty:
        raise RuntimeError(
            "No Anthony Henday segments matched — street_name_full values may "
            "have changed in the road feed."
        )

    seg_type = named["road_segment_type_description"].fillna("(null)")
    henday = named.loc[seg_type.isin(HENDAY_MAINLINE_TYPES)]
    if henday.empty:
        raise RuntimeError(
            "Henday name-match found rows but none carry a mainline segment "
            f"type. Types present: {sorted(seg_type.unique())}"
        )

    # No silent drops: say what the allowlist removed and what it kept.
    excluded = seg_type[~seg_type.isin(HENDAY_MAINLINE_TYPES)].value_counts()
    logger.info(
        "  mainline allowlist kept %d of %d named segments; excluded %s",
        len(henday), len(named), dict(excluded),
    )
    unknown = set(seg_type.unique()) - HENDAY_MAINLINE_TYPES - set(excluded.index)
    if unknown:
        logger.warning("  unrecognised segment types (dropped): %s", sorted(unknown))

    return henday.to_crs(epsg=WORKING_EPSG)


def _weld(geoms) -> "gpd.base.BaseGeometry":
    """Dissolve segments into as few continuous lines as possible."""
    merged = unary_union(list(geoms))
    if merged.geom_type == "MultiLineString":
        merged = linemerge(merged)
    return merged


def _dangling_flags(parts, tol: float) -> list[bool]:
    """Per-arc: does either end touch no other arc's end?"""
    ends = []
    for part in parts:
        coords = list(part.coords)
        ends.extend([Point(coords[0]), Point(coords[-1])])
    out = []
    for i in range(len(parts)):
        loose = False
        for slot in (2 * i, 2 * i + 1):
            e = ends[slot]
            if not any(e.distance(o) <= tol
                       for j, o in enumerate(ends) if j != slot):
                loose = True
        out.append(loose)
    return out


def _prune_spurs(geom, tol: float = RING_CLOSURE_TOLERANCE_M):
    """Drop arcs with a loose end — the Henday is a ring, so it has none.

    Bringing in the Highway 14 concurrency closes the hole in the east leg but
    overshoots it: the shared carriageways continue ~1.7 km and ~1.3 km south
    past the junction, where Highway 14 turns east and leaves the ring. Those
    stubs would render as two lines trailing off the ring into nothing.

    Pruning by TOPOLOGY rather than by a coordinate cutoff or a length
    threshold: "part of the ring" is exactly "both ends meet another arc", so
    the rule states the intent and cannot drift if the feed's segmentation
    changes. Iterated, because removing one stub can expose the next.
    """
    parts = list(getattr(geom, "geoms", [geom]))
    while True:
        flags = _dangling_flags(parts, tol)
        if not any(flags):
            return parts
        kept = [p for p, loose in zip(parts, flags) if not loose]
        dropped = [p for p, loose in zip(parts, flags) if loose]
        # No silent drops: name what came off and how long it was.
        logger.info(
            "  pruned %d spur arc(s) with loose ends: %s",
            len(dropped), [f"{p.length:.0f} m" for p in dropped],
        )
        if not kept:
            raise RuntimeError(
                "Pruning removed every arc — the extract has no closed ring."
            )
        parts = kept


def _round_coords(obj, precision: int):
    if isinstance(obj, (list, tuple)):
        if obj and isinstance(obj[0], float):
            return [round(c, precision) for c in obj]
        return [_round_coords(o, precision) for o in obj]
    return obj


def build(
    boundaries_path: Path = BOUNDARIES,
    roads_path: Path = ROADS,
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

    # --- henday: weld the carriageways, then simplify ------------------------
    henday = _load_henday(roads_path)
    raw_km = henday.geometry.length.sum() / 1000
    welded = _weld(henday.geometry).simplify(
        HENDAY_SIMPLIFY_M, preserve_topology=True
    )
    henday_geom = MultiLineString(_prune_spurs(welded))
    parts = len(henday_geom.geoms)
    welded_km = henday_geom.length / 1000
    logger.info(
        "Henday: %d segments, %.1f km raw -> %.1f km welded in %d part(s)",
        len(henday), raw_km, welded_km, parts,
    )
    # Both carriageways are kept: the ring is a divided highway, and picking one
    # direction leaves gaps where the feed names a segment without a direction.
    # At 1 px the two lines coincide; they only separate when zoomed well in.
    if welded_km < HENDAY_MIN_KM:
        logger.warning(
            "Henday welded length %.1f km is below the %.0f km floor — the "
            "extract may be missing a leg of the ring.",
            welded_km, HENDAY_MIN_KM,
        )

    # _prune_spurs guarantees no loose ends; assert it rather than trust it,
    # since a silent break here is exactly the defect that is hard to see in a
    # 15 kB file and obvious to a viewer on the map.
    if any(_dangling_flags(list(henday_geom.geoms), RING_CLOSURE_TOLERANCE_M)):
        raise RuntimeError("Henday ring still has loose ends after pruning.")
    logger.info("Henday ring closure: no loose ends across %d arc(s)", parts)

    # --- places: one named point per neighbouring municipality --------------
    places = _fetch_places()

    out_gdf = gpd.GeoDataFrame(
        {
            "t": ["river", "henday"] + ["place"] * len(places),
            # Only places carry a name; river/henday are unlabelled shapes.
            "name": [None, None] + list(places["name"]),
        },
        geometry=[river_geom, henday_geom] + list(places.geometry),
        crs=f"EPSG:{WORKING_EPSG}",
    ).to_crs(epsg=OUT_EPSG)

    features = []
    for row in out_gdf.itertuples():
        geom = row.geometry.__geo_interface__
        props = {"t": row.t}
        # isinstance, not `is not None`: pandas coerces the river/henday Nones
        # to float nan in this mixed column, and nan passes an `is not None`
        # test — which would emit a bare NaN token that is invalid JSON and
        # fails JSON.parse in the browser for the whole file.
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
    p.add_argument("--roads", type=Path, default=ROADS)
    p.add_argument("--out", type=Path, default=OUT)
    p.add_argument("--margin-m", type=float, default=MARGIN_M,
                   help="how far past the city bbox to keep the river")
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    build(args.boundaries, args.roads, args.out, args.margin_m)


if __name__ == "__main__":
    main()
