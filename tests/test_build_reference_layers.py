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
