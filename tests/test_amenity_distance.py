import logging
import sys

import geopandas as gpd
import numpy as np
import pandas as pd
import pytest
from pyproj import Transformer
from shapely.geometry import LineString

sys.path.insert(0, "src")
from amenity_distance import build_road_graph, network_distance_m


_TO_WGS84 = Transformer.from_crs(3400, 4326, always_xy=True)
# An arbitrary origin inside the Alberta 10-TM Forest zone; tests lay out metres
# there and convert, so every expected distance below is in real metres.
X0, Y0 = 300_000.0, 5_930_000.0


def _ll(dx: float, dy: float) -> tuple[float, float]:
    """(lon, lat) for a point ``dx``/``dy`` metres from the test origin."""
    return _TO_WGS84.transform(X0 + dx, Y0 + dy)


# Real centrelines are densely vertexed — median edge 13 m, p90 76 m — and the
# graph snaps points to NODES, so test geometry has to be vertexed like the real
# thing or the snap dominates every expected distance.
VERTEX_STEP_M = 10.0


def _densify(offsets):
    out = [offsets[0]]
    for (x0, y0), (x1, y1) in zip(offsets[:-1], offsets[1:]):
        n = max(1, int(round(np.hypot(x1 - x0, y1 - y0) / VERTEX_STEP_M)))
        out += [(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n) for i in range(1, n + 1)]
    return out


def _line(*offsets, centerline_type="Road"):
    return {
        "centerline_type": centerline_type,
        "geometry": LineString([_ll(dx, dy) for dx, dy in _densify(offsets)]),
    }


def _roads(tmp_path, rows, name="roads.geojson"):
    path = tmp_path / name
    gpd.GeoDataFrame(rows, crs="EPSG:4326").to_file(path, driver="GeoJSON")
    return str(path)


def _points(*offsets):
    lonlat = [_ll(dx, dy) for dx, dy in offsets]
    return pd.DataFrame({
        "longitude": [p[0] for p in lonlat],
        "latitude": [p[1] for p in lonlat],
    })


# An L: 1000 m east along y=0, then 1000 m north at x=1000. A point at the
# corner is 1000 m from the origin by road but ~1000 m straight-line too; a
# point at the far end is 2000 m by road and ~1414 m straight-line — the gap
# this module exists to measure.
L_ROADS = [_line((0, 0), (1000, 0)), _line((1000, 0), (1000, 1000))]


def test_distance_follows_the_road_not_the_crow(tmp_path):
    graph = build_road_graph(_roads(tmp_path, L_ROADS))
    d = network_distance_m(graph, _points((1000, 1000)), _points((0, 0)), "test")
    assert d[0] == pytest.approx(2000, abs=2)


def test_both_snap_offsets_are_included(tmp_path):
    """A point 30 m off the road is 30 m from a point standing on it, not 0 m."""
    graph = build_road_graph(_roads(tmp_path, [_line((0, 0), (1000, 0))]))
    d = network_distance_m(graph, _points((500, 30)), _points((500, -20)), "test")
    assert d[0] == pytest.approx(50, abs=2)


def test_nearest_amenity_wins_including_its_own_offset(tmp_path):
    """The amenity closer ALONG THE ROAD can lose to one with a shorter total."""
    graph = build_road_graph(_roads(tmp_path, [_line((0, 0), (1000, 0))]))
    # Amenity A: at x=0 on the road. Amenity B: at x=600 but 400 m off it.
    # From x=800, A is 800 m; B is 200 m + 400 m = 600 m.
    d = network_distance_m(graph, _points((800, 0)), _points((0, 0), (600, 400)), "test")
    assert d[0] == pytest.approx(600, abs=3)


def test_railways_and_alleys_are_excluded_from_the_graph(tmp_path):
    """A rail line is not a walking shortcut — the correctness filter, not tidying."""
    rows = L_ROADS + [_line((0, 0), (1000, 1000), centerline_type="Railway")]
    graph = build_road_graph(_roads(tmp_path, rows))
    d = network_distance_m(graph, _points((1000, 1000)), _points((0, 0)), "test")
    assert d[0] == pytest.approx(2000, abs=2)  # 1414 if the railway routed


def test_unreachable_point_is_null_not_a_large_number(tmp_path):
    """A sentinel distance would read downstream as a real 'far away'."""
    rows = L_ROADS + [_line((50_000, 50_000), (51_000, 50_000))]  # a separate island
    graph = build_road_graph(_roads(tmp_path, rows))
    d = network_distance_m(graph, _points((0, 0), (50_500, 50_000)), _points((0, 0)), "test")
    assert d[0] == pytest.approx(0, abs=2)
    assert np.isnan(d[1])


def test_never_shorter_than_straight_line(tmp_path):
    """The invariant that caught nothing on 439,245 real properties — keep it."""
    graph = build_road_graph(_roads(tmp_path, L_ROADS))
    pts = _points((0, 0), (500, 0), (1000, 500), (1000, 1000), (250, 400))
    amenity = _points((0, 0))
    d = network_distance_m(graph, pts, amenity, "test")
    to_alberta = Transformer.from_crs(4326, 3400, always_xy=True)
    px, py = to_alberta.transform(pts["longitude"].to_numpy(), pts["latitude"].to_numpy())
    straight = np.hypot(np.asarray(px) - X0, np.asarray(py) - Y0)
    assert np.all(d >= straight - 1.0)


def test_duplicate_geometry_does_not_double_the_weight(tmp_path):
    """Parallel edges SUM in a coo->csr conversion; a doubled weight lengthens routes."""
    rows = [_line((0, 0), (1000, 0)), _line((0, 0), (1000, 0))]
    graph = build_road_graph(_roads(tmp_path, rows))
    d = network_distance_m(graph, _points((1000, 0)), _points((0, 0)), "test")
    assert d[0] == pytest.approx(1000, abs=2)


def test_missing_centerline_type_raises(tmp_path):
    path = tmp_path / "no_type.geojson"
    gpd.GeoDataFrame(
        [{"geometry": LineString([_ll(0, 0), _ll(100, 0)])}], crs="EPSG:4326"
    ).to_file(path, driver="GeoJSON")
    with pytest.raises(ValueError, match="centerline_type"):
        build_road_graph(str(path))


def test_no_walkable_rows_raises(tmp_path):
    rows = [_line((0, 0), (1000, 0), centerline_type="Railway")]
    with pytest.raises(ValueError, match="no .* centrelines"):
        build_road_graph(_roads(tmp_path, rows))


def test_empty_amenity_set_raises(tmp_path):
    graph = build_road_graph(_roads(tmp_path, L_ROADS))
    with pytest.raises(ValueError, match="no amenity points"):
        network_distance_m(graph, _points((0, 0)), _points(), "test")


def test_far_snap_is_reported_not_dropped(tmp_path, caplog):
    graph = build_road_graph(_roads(tmp_path, [_line((0, 0), (1000, 0))]))
    with caplog.at_level(logging.WARNING):
        d = network_distance_m(graph, _points((500, 900)), _points((500, 0)), "test")
    assert d[0] == pytest.approx(900, abs=2)
    assert "from any road" in caplog.text


def test_snapping_to_a_node_overstates_never_understates(tmp_path):
    """The one approximation in the module, pinned in the SAFE direction.

    Points snap to the nearest graph NODE, not to the nearest point on the
    nearest edge, so a point beside the middle of a long edge walks to that
    edge's endpoint. Measured on 20,000 real properties (2026-08-23): median
    3.5 m of excess, p90 35 m, p99 67 m, 0.19% over 100 m. It always ADDS
    distance, so a "within 600 m" filter under-claims proximity rather than
    manufacturing it — the same direction of safety as taking the cell median
    over the cell minimum.
    """
    # One 400 m edge with no interior vertices: the worst case, not the normal one.
    path = tmp_path / "sparse.geojson"
    gpd.GeoDataFrame(
        [{"centerline_type": "Road", "geometry": LineString([_ll(0, 0), _ll(400, 0)])}],
        crs="EPSG:4326",
    ).to_file(path, driver="GeoJSON")
    graph = build_road_graph(str(path))
    # x=250 is nearer the x=400 node than the x=0 one, so the walk goes the
    # wrong way down the edge and back: 400 m + the offset, not the ~250 m truth.
    d = network_distance_m(graph, _points((250, 10)), _points((0, 0)), "test")
    assert d[0] == pytest.approx(400 + np.hypot(150, 10), abs=2)
    assert d[0] > np.hypot(250, 10)
