"""Tests for scripts/build_reference_layers.py (Tier-1 orientation geometry).

The reference layers are static cartographic furniture, so the risk is not a
wrong number — it is a wrong SHAPE that nobody notices in a 15 kB file and
every viewer notices on the map. These tests exercise the logic that produced real defects during the build, on
synthetic geometry (no network, no real data):

  - the highway query asks for a closed set of OSM classes and reports, rather
    than silently drops, ways the server returns without geometry, and
  - the place list is a closed enumeration queried in the sublayer matching
    each place's legal status.

⚠️ The Anthony Henday extraction this file used to test at length (mainline
allowlists, Highway 14 concurrency, spur pruning, ring closure) was RETIRED
2026-08-03 along with its tests: the highway layer now comes from OSM, which
needs none of it. The ring-closure invariant did not survive either — the new
layer is deliberately many open-ended corridors running off the clip edge.
What replaced it is a rendered-geometry assertion in
tools/profiling/verify-reference-layer.js: the highways must extend past the
city on all four sides.
"""
import json
import sys
from pathlib import Path

import pytest

gpd = pytest.importorskip("geopandas")
from shapely.geometry import LineString, MultiLineString, shape  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import build_reference_layers as b  # noqa: E402


# --- highway query --------------------------------------------------------

def test_highway_classes_are_a_closed_pair():
    """motorway + trunk only.

    `primary` is excluded on purpose: it would add ~1,786 km of in-city
    arterials to a map that has no basemap precisely so the data reads first.
    """
    assert b.HIGHWAY_CLASSES == ("motorway", "trunk")


def test_highway_query_uses_the_class_list_not_a_literal(monkeypatch):
    """A hardcoded regex would drift from HIGHWAY_CLASSES silently."""
    captured = {}

    class _Resp:
        def raise_for_status(self): pass
        def json(self): return {"elements": [
            {"tags": {"ref": "216"}, "geometry": [{"lon": -113.5, "lat": 53.5},
                                                  {"lon": -113.4, "lat": 53.6}]}]}

    def fake_post(url, data=None, headers=None, timeout=None):
        captured["query"] = data["data"]
        captured["ua"] = (headers or {}).get("User-Agent")
        return _Resp()

    monkeypatch.setattr(b.requests, "post", fake_post)
    b._fetch_highways((-114.0, 53.0, -113.0, 54.0))
    for cls in b.HIGHWAY_CLASSES:
        assert cls in captured["query"]
    # The public instance answers 406 without one.
    assert captured["ua"]


def test_ways_without_geometry_are_reported_not_silently_dropped(monkeypatch, caplog):
    """`out geom` omits geometry for ways the server cannot resolve."""
    class _Resp:
        def raise_for_status(self): pass
        def json(self): return {"elements": [
            {"tags": {"ref": "2"}, "geometry": [{"lon": -113.5, "lat": 53.5},
                                                {"lon": -113.4, "lat": 53.6}]},
            {"tags": {"ref": "16"}},                       # no geometry at all
            {"tags": {"ref": "16"}, "geometry": [{"lon": -113.5, "lat": 53.5}]},
        ]}

    monkeypatch.setattr(b.requests, "post", lambda *a, **k: _Resp())
    with caplog.at_level("WARNING"):
        out = b._fetch_highways((-114.0, 53.0, -113.0, 54.0))
    assert len(out) == 1
    assert "without usable geometry" in caplog.text


def test_empty_highway_response_raises_rather_than_drawing_nothing(monkeypatch):
    """An empty highway layer would look exactly like a successful build.

    This is not hypothetical: Alberta's highways_public MapServer answers 200
    with 510 features and NULL geometry on every one of them.
    """
    class _Resp:
        def raise_for_status(self): pass
        def json(self): return {"elements": []}

    monkeypatch.setattr(b.requests, "post", lambda *a, **k: _Resp())
    with pytest.raises(RuntimeError, match="no highway ways"):
        b._fetch_highways((-114.0, 53.0, -113.0, 54.0))


def test_all_ways_lacking_geometry_raises(monkeypatch):
    class _Resp:
        def raise_for_status(self): pass
        def json(self): return {"elements": [{"tags": {}}, {"tags": {}}]}

    monkeypatch.setattr(b.requests, "post", lambda *a, **k: _Resp())
    with pytest.raises(RuntimeError, match="lacked geometry"):
        b._fetch_highways((-114.0, 53.0, -113.0, 54.0))


def test_places_are_a_closed_explicit_list():
    """Composition is a cartographic judgement, so it is stated, not derived.

    A bbox/radius sweep would gain and lose names as the province edits
    boundaries, and the map's composition would drift with it.
    """
    names = [name for name, _, _ in b.PLACES]
    assert len(names) == len(set(names)), "duplicate place name"
    assert "Edmonton" not in names, "the subject city must not label itself"


def test_regions_are_unlabelled_and_include_the_subject_city():
    """REGIONS is the mirror image of PLACES: the edge is the payload, not a name.

    Edmonton belongs here and NOT in PLACES — the map had never drawn its own
    legal limit, so what read as the city edge was only where the neighbourhood
    polygons stop. Nothing in REGIONS may be labelled: these shapes are far too
    large to name sensibly at city zoom.
    """
    names = [name for name, _, _ in b.REGIONS]
    assert len(names) == len(set(names)), "duplicate region name"
    assert "Edmonton" in names, "the city's own legal limit is the point of REGIONS"
    assert not set(names) & {n for n, _, _ in b.PLACES}, (
        "a name in both lists would draw two outlines and label one of them"
    )


def test_strathcona_county_is_a_specialized_municipality():
    """The REGIONS equivalent of the Sherwood Park trap.

    Alberta models specialized municipalities in their own sublayer, so
    Strathcona County is NOT in 114 with the other counties. Looking for it
    there — the obvious place — returns nothing.
    """
    entry = next(e for e in b.REGIONS if e[0] == "Strathcona County")
    assert entry[1] == 104 and entry[2] == "SPMUN_NAME"


def test_each_region_is_queried_in_a_sublayer_that_matches_its_field():
    expected = {78: "CITY_NAME", 104: "SPMUN_NAME", 114: "MD_NAME"}
    for name, layer, field in b.REGIONS:
        assert expected[layer] == field, f"{name}: layer {layer} does not carry {field}"


def test_leduc_the_city_and_leduc_county_are_different_shapes():
    """Both lists carry a 'Leduc'-ish entry and they are not the same polygon —
    the CITY of Leduc sits INSIDE Leduc County. Querying one where the other is
    expected returns a shape of the wrong scale with no error."""
    city = next(e for e in b.PLACES if e[0] == "Leduc")
    county = next(e for e in b.REGIONS if e[0] == "Leduc County")
    assert (city[1], city[2]) == (78, "CITY_NAME")
    assert (county[1], county[2]) == (114, "MD_NAME")


def test_sherwood_park_is_an_urban_service_area():
    """The one that breaks a naive implementation.

    Sherwood Park is not a town or a city — it is an urban service area of
    Strathcona County, so it lives in neither the City (78) nor the Town (56)
    sublayer. Looking for it in the obvious place finds nothing at all.
    """
    entry = next(e for e in b.PLACES if e[0] == "Sherwood Park")
    assert entry[1] == 66 and entry[2] == "USA_NAME"


def test_each_place_is_queried_in_a_sublayer_that_matches_its_field():
    """Layer id and field name travel together; a mismatch returns no features."""
    expected = {78: "CITY_NAME", 56: "TOWN_NAME", 66: "USA_NAME"}
    for name, layer, field in b.PLACES:
        assert expected[layer] == field, f"{name}: layer {layer} does not carry {field}"


def test_devon_is_a_town_not_a_city():
    """Devon is the only non-city in the list; grouping it with the rest
    silently drops it."""
    assert next(e for e in b.PLACES if e[0] == "Devon")[1] == 56


def test_place_query_matches_on_equality_not_a_pattern(monkeypatch):
    """Sublayer 66 also holds 'Sherwood Park (Bremner)', a future-growth polygon
    ~10 km east. A LIKE/prefix query would pull it in and drag the anchor off
    the real town, so the WHERE clause must be an equality test.
    """
    seen = []

    class _Resp:
        status_code = 200
        def raise_for_status(self): pass
        def json(self):
            return {"features": [{
                "type": "Feature", "properties": {},
                "geometry": {"type": "Polygon",
                             "coordinates": [[[-113.3, 53.5], [-113.2, 53.5],
                                              [-113.2, 53.6], [-113.3, 53.6],
                                              [-113.3, 53.5]]]}}]}

    def _fake_get(url, params=None, timeout=None):
        seen.append(params["where"])
        return _Resp()

    monkeypatch.setattr(b.requests, "get", _fake_get)
    out = b._fetch_places()

    assert len(out) == len(b.PLACES), "one anchor per listed place"
    assert list(out["name"]) == [name for name, _, _ in b.PLACES]
    for where in seen:
        assert "LIKE" not in where.upper(), f"pattern match would over-select: {where}"
        assert "=" in where and where.endswith("'")
    assert "USA_NAME='Sherwood Park'" in seen


def test_missing_place_raises_rather_than_silently_dropping(monkeypatch):
    """A renamed or re-designated place must fail the build loudly.

    Returning nothing would leave a hole in the map's orientation with nothing
    to signal it — the same no-silent-drops rule the road extract follows.
    """
    class _Empty:
        def raise_for_status(self): pass
        def json(self): return {"features": []}

    monkeypatch.setattr(b.requests, "get", lambda *a, **k: _Empty())
    with pytest.raises(RuntimeError, match="No geometry returned"):
        b._fetch_places()


# --- the CRS path ---------------------------------------------------------
#
# ⚠️ S147 audit run 2, R4(4): `WORKING_EPSG` could be mutated with the suite
# green, so this script's CRS path was simply untested. RE-MEASURED 2026-09-08
# before building, and the finding as written is HALF STALE — which changes what
# is worth testing:
#
#   WORKING_EPSG = 999999  ->  3 tests already fail, but INCIDENTALLY: they
#                              exercise the highway path, `.to_crs` raises
#                              CRSError, and they crash. No assertion is about
#                              the CRS, and a crash is not a measurement.
#   WORKING_EPSG = 4326    ->  843 GREEN, and this is the dangerous one. 4326
#                              exists, so nothing raises; the whole module's
#                              tolerances are METRES (MARGIN_M, RIVER_SIMPLIFY_M,
#                              HIGHWAY_SIMPLIFY_M, BOUNDARY_SIMPLIFY_M) and they
#                              silently become DEGREES. Everything still writes.
#
# So the hole is a VALID-but-wrong CRS, not a nonexistent one — silent
# correctness, the failure mode this project keeps finding.


def test_the_working_crs_is_projected_and_measured_in_metres():
    """The property every tolerance in this module depends on, asserted by NAME.

    ⚠️ The module is written in metres throughout — `MARGIN_M` (60 km),
    `RIVER_SIMPLIFY_M` (25 m), `HIGHWAY_SIMPLIFY_M` (30 m), `BOUNDARY_SIMPLIFY_M`
    (100 m), `HIGHWAY_MIN_KM`. A geographic CRS makes all five degrees, and a
    25-DEGREE simplify tolerance is ~2,800 km: the river becomes a straight line
    and the file still writes.
    """
    from pyproj import CRS

    crs = CRS.from_epsg(b.WORKING_EPSG)
    assert crs.is_projected, (
        f"EPSG:{b.WORKING_EPSG} is geographic — every *_M tolerance in this "
        "module silently becomes degrees"
    )
    units = {ax.unit_name for ax in crs.axis_info}
    assert units == {"metre"}, f"EPSG:{b.WORKING_EPSG} measures in {units}, not metres"


def test_the_output_crs_is_the_lon_lat_the_front_end_reads():
    """deck.gl/MapLibre consume WGS84, and every other file in web/data/ is it."""
    from pyproj import CRS

    assert b.OUT_EPSG == 4326
    assert CRS.from_epsg(b.OUT_EPSG).is_geographic
    assert b.WORKING_EPSG != b.OUT_EPSG, "geometry work and output must not share a CRS"


# Edmonton, generously bounded. Wide enough that the 60 km clip margin and the
# neighbouring counties all sit inside it; tight enough that degrees-as-metres
# (or metres-as-degrees) lands far outside.
_EDM_LON = (-114.5, -112.5)
_EDM_LAT = (52.8, 54.5)


def _synthetic(monkeypatch, tmp_path):
    """Stub every network fetch with geometry built in 4326 and reprojected to
    ``WORKING_EPSG`` — the same last step the real fetchers take.

    ⚠️ That last step is the whole point. A stub that hard-coded metre
    coordinates would keep handing `build()` honest metres no matter what
    `WORKING_EPSG` says, and the test would pass under the bug — the failure
    this project has now hit seven times. Reprojecting for real means a
    geographic working CRS reaches `build()` as degrees, exactly as it would in
    production.
    """
    from shapely.geometry import Point, Polygon

    def to_working(geom):
        return gpd.GeoSeries([geom], crs="EPSG:4326").to_crs(epsg=b.WORKING_EPSG).iloc[0]

    # The "city": a ~0.4 x 0.25 degree block over Edmonton.
    hoods = gpd.GeoDataFrame(
        {"name": ["A"]},
        geometry=[Polygon([(-113.7, 53.4), (-113.3, 53.4),
                           (-113.3, 53.65), (-113.7, 53.65)])],
        crs="EPSG:4326",
    )
    boundaries = tmp_path / "hoods.geojson"
    hoods.to_file(boundaries, driver="GeoJSON")

    # A river across the city, wide enough to survive a 25 m simplify and to
    # have an area worth comparing.
    river_4326 = Polygon([(-113.9, 53.50), (-113.1, 53.56),
                          (-113.1, 53.58), (-113.9, 53.52)])
    monkeypatch.setattr(b, "_fetch_river", lambda bounds: gpd.GeoDataFrame(
        geometry=[to_working(river_4326)], crs=f"EPSG:{b.WORKING_EPSG}"))

    # Two long corridors, so the welded length clears nothing in particular but
    # exercises the same clip/weld/simplify path as the real layer.
    hwys = [LineString([(-114.2, 53.3), (-112.8, 53.75)]),
            LineString([(-113.5, 53.1), (-113.5, 53.9)])]
    monkeypatch.setattr(b, "_fetch_highways", lambda bounds: gpd.GeoDataFrame(
        {"ref": ["216", "2"]},
        geometry=[to_working(g) for g in hwys], crs=f"EPSG:{b.WORKING_EPSG}"))

    town = Polygon([(-113.0, 53.5), (-112.9, 53.5), (-112.9, 53.6), (-113.0, 53.6)])
    monkeypatch.setattr(b, "_fetch_places", lambda: gpd.GeoDataFrame(
        {"name": ["Townly"], "outline": [to_working(town)]},
        geometry=[to_working(Point(-112.95, 53.55))], crs=f"EPSG:{b.WORKING_EPSG}"))

    county = Polygon([(-114.0, 53.2), (-113.0, 53.2), (-113.0, 53.9), (-114.0, 53.9)])
    monkeypatch.setattr(b, "_fetch_regions", lambda: [
        ("Edmonton", to_working(hoods.geometry.iloc[0])),
        ("Some County", to_working(county)),
    ])
    zone = Polygon([(-113.2, 53.7), (-113.0, 53.7), (-113.0, 53.8), (-113.2, 53.8)])
    monkeypatch.setattr(b, "_fetch_zone", lambda: to_working(zone))
    monkeypatch.setattr(b, "_fetch_point",
                        lambda *a: to_working(Point(-113.5, 53.32)))
    monkeypatch.setattr(b, "_fetch_airport",
                        lambda: to_working(Point(-113.58, 53.31)))
    return boundaries, river_4326


def _coords(obj):
    if isinstance(obj, (int, float)):
        return
    if len(obj) == 2 and all(isinstance(v, (int, float)) for v in obj):
        yield obj
        return
    for part in obj:
        yield from _coords(part)


def test_build_writes_lon_lat_over_edmonton(monkeypatch, tmp_path):
    """End to end through the real CRS path, no network: read -> WORKING ->
    clip and simplify in metres -> assemble -> OUT -> write."""
    boundaries, _ = _synthetic(monkeypatch, tmp_path)
    out = tmp_path / "reference.geojson"
    n = b.build(boundaries_path=boundaries, out_path=out)

    assert n > 0
    payload = json.loads(out.read_text())
    pts = [p for f in payload["features"] for p in _coords(f["geometry"]["coordinates"])]
    assert pts
    for lon, lat in pts:
        assert _EDM_LON[0] <= lon <= _EDM_LON[1], f"lon {lon} is not over Edmonton"
        assert _EDM_LAT[0] <= lat <= _EDM_LAT[1], f"lat {lat} is not over Edmonton"


def test_build_simplifies_in_metres_not_degrees(monkeypatch, tmp_path):
    """⚠️ THE ASSERTION THAT CATCHES A VALID-BUT-WRONG WORKING CRS.

    The lon/lat check above does NOT: with `WORKING_EPSG = 4326` the final
    `to_crs(4326)` is a no-op, so the coordinates come out as lon/lat anyway and
    that test passes under the bug. What does not survive is the SHAPE — a 25 m
    river tolerance read as 25 degrees flattens the polygon.

    So this measures the river's area back in the working CRS's metres and
    requires it to survive the round trip.
    """
    boundaries, river_4326 = _synthetic(monkeypatch, tmp_path)
    out = tmp_path / "reference.geojson"
    b.build(boundaries_path=boundaries, out_path=out)

    payload = json.loads(out.read_text())
    river = next(f for f in payload["features"] if f["properties"]["t"] == "river")
    got = gpd.GeoSeries([shape(river["geometry"])], crs="EPSG:4326").to_crs(epsg=3400)
    want = gpd.GeoSeries([river_4326], crs="EPSG:4326").to_crs(epsg=3400)

    # The river is clipped to the city bbox + 60 km margin, which contains it
    # whole here, and simplified by 25 m — so area moves by well under 1%.
    assert got.area.iloc[0] == pytest.approx(want.area.iloc[0], rel=0.01), (
        "the river's area did not survive build() — a simplify tolerance was "
        "not in metres"
    )


def test_the_working_crs_is_the_one_the_rest_of_the_pipeline_uses():
    """The property tests above pass on ANY metre-based CRS — measured: EPSG:3776
    (NAD83 / Alberta 3TM 114 W) leaves all 847 green, because it is projected, in
    metres, and covers Edmonton, so the tolerances stay honest and the output is
    still correct lon/lat.

    That is a consistency pin, not a correctness one, and it is stated as such:
    this layer is drawn over data built in EPSG:3400 (`src/load_roads.py`,
    `src/amenity_distance.py`, `src/load_stormwater.py` and others all hardcode
    it — there is no single constant to import, which is why this reads as a
    literal).
    """
    assert b.WORKING_EPSG == 3400, (
        "the reference layers would be built in a different projection from the "
        "data they are drawn over; correct only if the whole pipeline moved"
    )
