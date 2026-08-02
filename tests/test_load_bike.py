import json
import sys
from unittest.mock import patch

import geopandas as gpd
import pandas as pd
import pytest
from shapely.geometry import LineString, Polygon

sys.path.insert(0, "src")
from load_bike import (
    CLASSIFICATION_GROUP,
    _classify,
    export_bike_web,
    load_bike,
)


def _square(x0, y0, size):
    return Polygon([(x0, y0), (x0 + size, y0), (x0 + size, y0 + size), (x0, y0 + size)])


def _boundaries(names, polys):
    """Neighbourhood boundaries already projected to EPSG:3400 (metres)."""
    return gpd.GeoDataFrame(
        {"neighbourhood_name": names, "geometry": polys},
        crs="EPSG:3400",
    )


def _bike(rows):
    """Bike frame in EPSG:3400 metres so the loader's to_crs(3400) is a no-op.

    rows: list of (classification, route_coming_soon, type, geometry)
    """
    classes, soon, types, geoms = zip(*rows)
    return gpd.GeoDataFrame(
        {
            "classification": list(classes),
            "route_coming_soon": list(soon),
            "type": list(types),
            "geometry": list(geoms),
        },
        crs="EPSG:3400",
    )


def _run(boundaries, bike):
    with patch("load_bike.gpd.read_file", return_value=bike):
        return load_bike("dummy.geojson", boundaries)


PROTECTED = "Protected Bike Lane"
PATHWAY = "Shared Pathway"
SHARED_ROAD = "Shared Roadway - Lower Traffic"
WALKWAY = "Walkway / Breezeway"
ON, OFF = "ON ROAD", "OFF ROAD"


# --- _classify -------------------------------------------------------------


def test_classify_exact_strings():
    groups = _classify(pd.Series([PROTECTED, PATHWAY, SHARED_ROAD, WALKWAY]))
    assert list(groups) == ["dedicated", "dedicated", "shared_roadway", "pedestrian"]


def test_classify_unknown_defaults_to_excluded_and_warns(caplog):
    """The opposite default from load_roads: drift must not INFLATE supply."""
    with caplog.at_level("WARNING"):
        groups = _classify(pd.Series(["Jetpack Corridor"]))
    assert list(groups) == ["unclassified"]
    assert "Jetpack Corridor" in caplog.text


def test_classify_null_warns(caplog):
    with caplog.at_level("WARNING"):
        groups = _classify(pd.Series([None]))
    assert list(groups) == ["unclassified"]
    assert "<null>" in caplog.text


def test_every_live_classification_is_mapped():
    """The 12 values in the live feed, verified 2026-08-02 (DATA.md §15).

    A new value appearing upstream must fail here, not silently land in the
    excluded bucket — this is the list that has to be revisited.
    """
    live = {
        "Protected Bike Lane", "Painted Bike Lane", "Contra-Flow Bike Lane",
        "Local Street Bikeway", "Shared Pathway", "Shared Trail",
        "Shared Roadway - Higher Traffic", "Shared Roadway - Lower Traffic",
        "Bus / Bike / Taxi Lane", "Walkway / Breezeway", "Maintenance Access",
        "Unclassified",
    }
    assert live == set(CLASSIFICATION_GROUP)


# --- row filters -----------------------------------------------------------


def test_coming_soon_routes_are_excluded():
    """Planned infrastructure is not built infrastructure."""
    boundaries = _boundaries(["A"], [_square(0, 0, 100)])
    bike = _bike([
        (PROTECTED, False, ON, LineString([(10, 10), (10, 60)])),   # 50 m, built
        (PROTECTED, True, ON, LineString([(20, 10), (20, 90)])),    # 80 m, planned
    ])
    result = _run(boundaries, bike)
    assert result.loc[0, "bike_m_total"] == pytest.approx(50.0)


def test_shared_roadway_excluded_no_double_count_with_roads():
    """A bike designation on an existing street adds no asset — those metres
    are already in load_roads' road_m_total."""
    boundaries = _boundaries(["A"], [_square(0, 0, 100)])
    bike = _bike([
        (PROTECTED, False, ON, LineString([(10, 10), (10, 60)])),      # 50 m
        (SHARED_ROAD, False, ON, LineString([(20, 10), (20, 90)])),    # 80 m
        ("Bus / Bike / Taxi Lane", False, ON, LineString([(30, 10), (30, 90)])),
    ])
    result = _run(boundaries, bike)
    assert result.loc[0, "bike_m_total"] == pytest.approx(50.0)


def test_pedestrian_classes_excluded():
    boundaries = _boundaries(["A"], [_square(0, 0, 100)])
    bike = _bike([
        (PATHWAY, False, OFF, LineString([(10, 10), (10, 60)])),       # 50 m
        (WALKWAY, False, OFF, LineString([(20, 10), (20, 90)])),       # 80 m
        ("Maintenance Access", False, OFF, LineString([(30, 10), (30, 90)])),
    ])
    result = _run(boundaries, bike)
    assert result.loc[0, "bike_m_total"] == pytest.approx(50.0)


def test_missing_required_column_raises():
    boundaries = _boundaries(["A"], [_square(0, 0, 100)])
    bike = _bike([(PROTECTED, False, ON, LineString([(10, 10), (10, 60)]))])
    bike = bike.drop(columns=["classification"])
    with pytest.raises(ValueError, match="classification"):
        _run(boundaries, bike)


# --- aggregation -----------------------------------------------------------


def test_onroad_offroad_split_sums_to_total():
    boundaries = _boundaries(["A"], [_square(0, 0, 100)])
    bike = _bike([
        (PROTECTED, False, ON, LineString([(10, 10), (10, 60)])),    # 50 m on
        (PATHWAY, False, OFF, LineString([(20, 10), (20, 40)])),     # 30 m off
    ])
    result = _run(boundaries, bike)
    assert result.loc[0, "bike_m_onroad"] == pytest.approx(50.0)
    assert result.loc[0, "bike_m_offroad"] == pytest.approx(30.0)
    assert result.loc[0, "bike_m_total"] == pytest.approx(80.0)


def test_lengths_split_across_neighbourhoods_at_the_boundary():
    boundaries = _boundaries(
        ["A", "B"], [_square(0, 0, 100), _square(100, 0, 100)]
    )
    # One 200 m path crossing the shared edge at x=100, 100 m each side.
    bike = _bike([(PATHWAY, False, OFF, LineString([(0, 50), (200, 50)]))])
    result = _run(boundaries, bike).set_index("neighbourhood_name")
    assert result.loc["A", "bike_m_total"] == pytest.approx(100.0)
    assert result.loc["B", "bike_m_total"] == pytest.approx(100.0)


def test_only_onroad_still_reports_zero_offroad():
    """The unstack must not drop the absent half of the split."""
    boundaries = _boundaries(["A"], [_square(0, 0, 100)])
    bike = _bike([(PROTECTED, False, ON, LineString([(10, 10), (10, 60)]))])
    result = _run(boundaries, bike)
    assert result.loc[0, "bike_m_offroad"] == pytest.approx(0.0)
    assert result.loc[0, "bike_m_total"] == pytest.approx(50.0)


def test_unprojected_boundaries_raise():
    boundaries = gpd.GeoDataFrame(
        {"neighbourhood_name": ["A"], "geometry": [_square(0, 0, 1)]},
        crs="EPSG:4326",
    )
    bike = _bike([(PROTECTED, False, ON, LineString([(0, 0), (0, 1)]))])
    with pytest.raises(ValueError, match="EPSG:3400"):
        _run(boundaries, bike)


def test_length_outside_boundaries_is_reported(caplog):
    """Conservation guard: what falls outside every polygon must be logged."""
    boundaries = _boundaries(["A"], [_square(0, 0, 100)])
    # 50 m inside, 100 m beyond the eastern edge.
    bike = _bike([(PATHWAY, False, OFF, LineString([(50, 50), (200, 50)]))])
    with caplog.at_level("INFO"):
        result = _run(boundaries, bike)
    assert result.loc[0, "bike_m_total"] == pytest.approx(50.0)
    assert "conservation" in caplog.text


# --- export_bike_web -------------------------------------------------------


def test_export_bike_web_writes_lines(tmp_path):
    boundaries = _boundaries(["A"], [_square(0, 0, 1000)])
    bike = _bike([
        (PATHWAY, False, OFF, LineString([(100, 100), (100, 900)])),
        (SHARED_ROAD, False, ON, LineString([(200, 100), (200, 900)])),
    ])
    out = tmp_path / "bike_routes.json"
    with patch("load_bike.gpd.read_file", return_value=bike):
        n = export_bike_web("dummy.geojson", boundaries, str(out))

    payload = json.loads(out.read_text())
    assert list(payload) == ["lines"]
    assert n == len(payload["lines"]) >= 1
    # The excluded shared roadway must not reach the context layer either.
    assert n == 1
    # Coordinates come back in lon/lat, not the projected metres.
    lon, lat = payload["lines"][0][0]
    assert -180 <= lon <= 180 and -90 <= lat <= 90


def test_export_bike_web_drops_clip_slivers(tmp_path):
    boundaries = _boundaries(["A"], [_square(0, 0, 1000)])
    bike = _bike([
        (PATHWAY, False, OFF, LineString([(100, 100), (100, 900)])),
        (PATHWAY, False, OFF, LineString([(500, 500), (500, 505)])),  # 5 m sliver
    ])
    out = tmp_path / "bike_routes.json"
    with patch("load_bike.gpd.read_file", return_value=bike):
        n = export_bike_web("dummy.geojson", boundaries, str(out), min_part_m=20.0)
    assert n == 1
