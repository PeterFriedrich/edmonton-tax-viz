import sys
from unittest.mock import patch

import geopandas as gpd
import pandas as pd
import pytest
from shapely.geometry import LineString, Polygon

sys.path.insert(0, "src")
from load_roads import _classify, load_roads


def _square(x0, y0, size):
    return Polygon([(x0, y0), (x0 + size, y0), (x0 + size, y0 + size), (x0, y0 + size)])


def _boundaries(names, polys):
    """Neighbourhood boundaries already projected to EPSG:3400 (metres)."""
    return gpd.GeoDataFrame(
        {"neighbourhood_name": names, "geometry": polys},
        crs="EPSG:3400",
    )


def _roads(rows):
    """Road frame in EPSG:3400 metres so the loader's to_crs(3400) is a no-op.

    rows: list of (centerline_type, responsible_party, functional_class, geometry)
    """
    types, parties, classes, geoms = zip(*rows)
    return gpd.GeoDataFrame(
        {
            "centerline_type": list(types),
            "responsible_party_description": list(parties),
            "functional_class_code": list(classes),
            "geometry": list(geoms),
        },
        crs="EPSG:3400",
    )


def _run(boundaries, roads):
    with patch("load_roads.gpd.read_file", return_value=roads):
        return load_roads("dummy.geojson", boundaries)


CITY = "City of Edmonton"
LOCAL = "Local-Residential"
COLLECTOR = "Collector-Residential"
ARTERIAL = "Arterial-Class A (Primary Highway, Truck Route)"


# --- _classify -------------------------------------------------------------


def test_classify_exact_strings():
    groups = _classify(pd.Series([LOCAL, COLLECTOR, ARTERIAL, "Local-ParkWay"]))
    assert list(groups) == ["local", "collector", "arterial", "local"]


def test_classify_alley_residential_is_alley_group():
    assert list(_classify(pd.Series(["Alley-Residential"]))) == ["alley"]


def test_classify_unknown_defaults_to_local_and_warns(caplog):
    with caplog.at_level("WARNING"):
        groups = _classify(pd.Series(["Hyperloop-Class Z"]))
    assert list(groups) == ["local"]
    assert "Hyperloop-Class Z" in caplog.text


def test_classify_null_warns(caplog):
    with caplog.at_level("WARNING"):
        groups = _classify(pd.Series([None]))
    assert list(groups) == ["local"]
    assert "<null>" in caplog.text


# --- load_roads ------------------------------------------------------------


def test_lengths_summed_per_hood_and_class():
    hood = _boundaries(["ALPHA"], [_square(0, 0, 100)])
    roads = _roads(
        [
            ("Road", CITY, LOCAL, LineString([(0, 10), (100, 10)])),  # 100 m local
            ("Road", CITY, LOCAL, LineString([(0, 20), (50, 20)])),  # 50 m local
            ("Road", CITY, COLLECTOR, LineString([(0, 30), (100, 30)])),  # 100 m coll
        ]
    )
    result = _run(hood, roads)
    row = result.iloc[0]
    assert row["road_m_local"] == pytest.approx(150)
    assert row["road_m_collector"] == pytest.approx(100)
    assert row["road_m_total"] == pytest.approx(250)


def test_arterial_carried_but_excluded_from_total():
    hood = _boundaries(["ALPHA"], [_square(0, 0, 100)])
    roads = _roads(
        [
            ("Road", CITY, ARTERIAL, LineString([(0, 10), (100, 10)])),
            ("Road", CITY, LOCAL, LineString([(0, 20), (100, 20)])),
        ]
    )
    row = _run(hood, roads).iloc[0]
    assert row["road_m_arterial"] == pytest.approx(100)
    assert row["road_m_total"] == pytest.approx(100)  # local only


def test_non_road_and_non_city_rows_filtered_out():
    hood = _boundaries(["ALPHA"], [_square(0, 0, 100)])
    roads = _roads(
        [
            ("Alley", CITY, None, LineString([(0, 10), (100, 10)])),
            ("Railway", "Canadian National Railway", None, LineString([(0, 20), (100, 20)])),
            ("Road", "Province of Alberta", ARTERIAL, LineString([(0, 30), (100, 30)])),
            ("Road", CITY, LOCAL, LineString([(0, 40), (100, 40)])),
        ]
    )
    row = _run(hood, roads).iloc[0]
    assert row["road_m_total"] == pytest.approx(100)  # only the city road
    assert row["road_m_arterial"] == 0.0  # provincial arterial dropped


def test_functionally_alley_road_rows_excluded():
    """Road-type rows classed Alley-Residential are excluded per the alleys-out
    decision (function governs). 41 such rows in the real data."""
    hood = _boundaries(["ALPHA"], [_square(0, 0, 100)])
    roads = _roads(
        [
            ("Road", CITY, "Alley-Residential", LineString([(0, 10), (100, 10)])),
            ("Road", CITY, LOCAL, LineString([(0, 20), (100, 20)])),
        ]
    )
    row = _run(hood, roads).iloc[0]
    assert row["road_m_total"] == pytest.approx(100)
    assert "road_m_alley" not in row.index


def test_segment_split_across_two_hoods():
    """A road crossing a boundary contributes its clipped length to each side —
    conserved, not duplicated."""
    hoods = _boundaries(
        ["WEST", "EAST"], [_square(0, 0, 100), _square(100, 0, 100)]
    )
    roads = _roads(
        [("Road", CITY, LOCAL, LineString([(0, 50), (200, 50)]))]  # 200 m spanning both
    )
    result = _run(hoods, roads).set_index("neighbourhood_name")
    assert result.loc["WEST", "road_m_total"] == pytest.approx(100)
    assert result.loc["EAST", "road_m_total"] == pytest.approx(100)


def test_segment_outside_all_hoods_reported_not_counted(caplog):
    hood = _boundaries(["ALPHA"], [_square(0, 0, 100)])
    roads = _roads(
        [
            ("Road", CITY, LOCAL, LineString([(0, 10), (100, 10)])),  # inside
            ("Road", CITY, LOCAL, LineString([(0, 500), (100, 500)])),  # outside
        ]
    )
    with caplog.at_level("INFO"):
        result = _run(hood, roads)
    assert result.iloc[0]["road_m_total"] == pytest.approx(100)
    assert "outside all boundaries" in caplog.text


def test_boundaries_must_be_projected():
    hood = _boundaries(["ALPHA"], [_square(0, 0, 100)]).to_crs(epsg=4326)
    roads = _roads([("Road", CITY, LOCAL, LineString([(0, 10), (100, 10)]))])
    with pytest.raises(ValueError, match="EPSG:3400"):
        _run(hood, roads)


def test_hood_with_no_roads_absent_from_result():
    """Like load_zoning, hoods with zero overlay simply don't appear — the
    downstream merge defaults them (join_and_calculate's concern)."""
    hoods = _boundaries(
        ["HASROADS", "EMPTY"], [_square(0, 0, 100), _square(1000, 0, 100)]
    )
    roads = _roads([("Road", CITY, LOCAL, LineString([(0, 10), (100, 10)]))])
    result = _run(hoods, roads)
    assert list(result["neighbourhood_name"]) == ["HASROADS"]


def test_empty_geometry_dropped():
    hood = _boundaries(["ALPHA"], [_square(0, 0, 100)])
    roads = _roads(
        [
            ("Road", CITY, LOCAL, LineString([(0, 10), (100, 10)])),
            ("Road", CITY, LOCAL, None),
        ]
    )
    row = _run(hood, roads).iloc[0]
    assert row["road_m_total"] == pytest.approx(100)
