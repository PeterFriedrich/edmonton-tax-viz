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
import sys
from pathlib import Path

import pytest

gpd = pytest.importorskip("geopandas")
from shapely.geometry import LineString, MultiLineString  # noqa: E402

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
