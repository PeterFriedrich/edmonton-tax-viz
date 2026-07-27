"""Tests for scripts/build_reference_layers.py (Tier-1 orientation geometry).

The reference layers are static cartographic furniture, so the risk is not a
wrong number — it is a wrong SHAPE that nobody notices in a 15 kB file and
every viewer notices on the map. These tests exercise the two pieces of logic
that produced real defects during the build, on synthetic geometry (no network,
no real data):

  - the mainline/concurrency selection rules are a closed enumeration, and
  - spur pruning leaves a closed ring and removes anything with a loose end.
"""
import sys
from pathlib import Path

import pytest

gpd = pytest.importorskip("geopandas")
from shapely.geometry import LineString, MultiLineString  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import build_reference_layers as b  # noqa: E402


# --- selection rules -------------------------------------------------------

def test_mainline_allowlist_keeps_structures():
    """Bridges and overpasses ARE the mainline where it crosses something.

    Dropping them as "structures" would open a gap in the ring at every river
    crossing and cross-street flyover.
    """
    assert "Structure - Bridge" in b.HENDAY_MAINLINE_TYPES
    assert "Structure - Overpass" in b.HENDAY_MAINLINE_TYPES
    assert "Roadway (Standard)" in b.HENDAY_MAINLINE_TYPES


def test_mainline_allowlist_excludes_interchange_furniture():
    """Ramps and cutoffs are named for the highway they serve, but are not it."""
    for junk in ("Entrance Ramp", "Exit Ramp", "Right Turn Cutoff",
                 "Left Turn Cutoff", "Collector-Distributor", "Service Road"):
        assert junk not in b.HENDAY_MAINLINE_TYPES


def test_concurrency_is_north_south_only():
    """Hwy 216 shares Hwy 14's north/south carriageways, not its east/west ones.

    The ring runs north-south through the concurrency; HIGHWAY 14
    EASTBOUND/WESTBOUND is Highway 14 leaving the ring, and pulling it in grows
    a ~5 km spur. A "HIGHWAY 14" substring match would do exactly that.
    """
    assert b.HENDAY_CONCURRENT_NAMES == {"HIGHWAY 14 NORTHBOUND",
                                         "HIGHWAY 14 SOUTHBOUND"}
    assert not any("HIGHWAY 14" in p for p in b.HENDAY_PATTERNS)


def test_name_patterns_do_not_catch_lookalikes():
    """The two substrings must not match '216 STREET NW' or 'ANTHONY CRESCENT'."""
    for decoy in ("216 STREET NW", "ANTHONY CRESCENT SW"):
        assert not any(pat in decoy for pat in b.HENDAY_PATTERNS)


# --- topology --------------------------------------------------------------

def _square_ring():
    """A closed square, split into two arcs the way linemerge leaves them."""
    return [
        LineString([(0, 0), (0, 100), (100, 100)]),
        LineString([(100, 100), (100, 0), (0, 0)]),
    ]


def test_closed_ring_has_no_dangles():
    flags = b._dangling_flags(_square_ring(), b.RING_CLOSURE_TOLERANCE_M)
    assert flags == [False, False]


def test_open_ring_reports_dangles():
    """A hole in the ring shows up as a matched pair of loose ends.

    This is the shape of the Highway 14 defect: two arcs, ends far apart.
    """
    arcs = [
        LineString([(0, 0), (0, 100), (100, 100)]),
        LineString([(100, 100), (100, 0), (5000, 0)]),  # never returns
    ]
    assert b._dangling_flags(arcs, b.RING_CLOSURE_TOLERANCE_M) == [True, True]


def test_prune_spurs_drops_the_spur_and_keeps_the_ring():
    arcs = _square_ring() + [LineString([(100, 100), (900, 900)])]  # spur
    kept = b._prune_spurs(MultiLineString(arcs), b.RING_CLOSURE_TOLERANCE_M)
    assert len(kept) == 2
    assert not any(f for f in b._dangling_flags(kept, b.RING_CLOSURE_TOLERANCE_M))


def test_prune_spurs_iterates_to_remove_a_chain():
    """Removing one stub can expose the next — pruning must repeat, not run once."""
    arcs = _square_ring() + [
        LineString([(100, 100), (400, 400)]),   # stub off the ring
        LineString([(400, 400), (800, 800)]),   # stub off the stub
    ]
    kept = b._prune_spurs(MultiLineString(arcs), b.RING_CLOSURE_TOLERANCE_M)
    assert len(kept) == 2


def test_prune_spurs_refuses_to_empty_the_layer():
    """An all-spur input is a broken extract, not a silently empty ring road."""
    arcs = MultiLineString([LineString([(0, 0), (100, 100)])])
    with pytest.raises(RuntimeError, match="no closed ring"):
        b._prune_spurs(arcs, b.RING_CLOSURE_TOLERANCE_M)


def test_closure_tolerance_is_below_the_defect_scale():
    """The tolerance must not be loose enough to swallow a real break.

    The Highway 14 hole was 2.9 km; the tolerance is metres.
    """
    assert 0 < b.RING_CLOSURE_TOLERANCE_M < 500


# --- regional place labels -------------------------------------------------
#
# The places are an explicit list, not a query result, so the failure mode is
# not "wrong geometry" but "wrong list": a name that no longer resolves, or a
# name looked for in the wrong sublayer. Both would silently cost the map a
# label. These pin the enumeration itself; _fetch_places raising on an empty
# result is what covers the live service.

def test_places_are_a_closed_explicit_list():
    """Composition is a cartographic judgement, so it is stated, not derived.

    A bbox/radius sweep would gain and lose names as the province edits
    boundaries, and the map's composition would drift with it.
    """
    names = [name for name, _, _ in b.PLACES]
    assert len(names) == len(set(names)), "duplicate place name"
    assert "Edmonton" not in names, "the subject city must not label itself"


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
