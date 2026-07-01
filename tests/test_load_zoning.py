import sys
from unittest.mock import patch

import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon

sys.path.insert(0, "src")
from load_zoning import SET_ASIDE_THRESHOLD, _categorize, load_zoning


def _square(x0, y0, size):
    return Polygon([(x0, y0), (x0 + size, y0), (x0 + size, y0 + size), (x0, y0 + size)])


def _boundaries(names, polys):
    """Neighbourhood boundaries already projected to EPSG:3400 (metres)."""
    return gpd.GeoDataFrame(
        {"neighbourhood_name": names, "geometry": polys},
        crs="EPSG:3400",
    )


def _zoning(codes, polys):
    """Zoning frame with geometry already in EPSG:3400 metres, so the loader's
    to_crs(3400) is a no-op and the synthetic coordinates drive the overlay."""
    return gpd.GeoDataFrame(
        {"zoning": codes, "geometry": polys},
        crs="EPSG:3400",
    )


def _run(boundaries, zoning):
    with patch("load_zoning.gpd.read_file", return_value=zoning):
        return load_zoning("dummy.geojson", boundaries)


# --- _categorize ---------------------------------------------------------------

def test_categorize_parses_first_token():
    cats = _categorize(pd.Series(["RM h16", "A", "FD"]))
    assert list(cats) == ["dev", "never", "notyet"]


def test_categorize_institutional_not_set_aside():
    # UI/UF/AJ/PU are their own category, distinct from set-aside.
    assert list(_categorize(pd.Series(["PU", "UI", "AJ", "UF"]))) == ["inst"] * 4


def test_categorize_unknown_defaults_to_dev_and_warns(caplog):
    with caplog.at_level("WARNING"):
        cats = _categorize(pd.Series(["ZZZ"]))
    assert list(cats) == ["dev"]
    assert "ZZZ" in caplog.text


def test_categorize_direct_control_is_dev():
    assert list(_categorize(pd.Series(["DC", "DC1", "DC2"]))) == ["dev"] * 3


# --- load_zoning ---------------------------------------------------------------

def test_fully_natural_hood_is_set_aside():
    hood = _boundaries(["RIVER VALLEY"], [_square(0, 0, 100)])
    zoning = _zoning(["A"], [_square(0, 0, 100)])
    result = _run(hood, zoning)
    row = result.iloc[0]
    assert row["set_aside_frac"] == 1.0
    assert bool(row["is_set_aside"]) is True
    assert row["set_aside_reason"] == "River Valley / Natural / Parks"


def test_fully_developed_hood_not_set_aside():
    hood = _boundaries(["DOWNTOWN"], [_square(0, 0, 100)])
    zoning = _zoning(["RSF"], [_square(0, 0, 100)])
    result = _run(hood, zoning)
    row = result.iloc[0]
    assert row["set_aside_frac"] == 0.0
    assert bool(row["is_set_aside"]) is False
    assert row["set_aside_reason"] == ""


def test_threshold_boundary():
    # 95% natural, 5% developed (full-height strips) → above 0.90 → set aside.
    hood = _boundaries(["MOSTLY_NATURAL"], [_square(0, 0, 100)])
    zoning = _zoning(
        ["NA", "RSF"],
        [Polygon([(0, 0), (95, 0), (95, 100), (0, 100)]),
         Polygon([(95, 0), (100, 0), (100, 100), (95, 100)])],
    )
    result = _run(hood, zoning)
    row = result.iloc[0]
    assert abs(row["set_aside_frac"] - 0.95) < 1e-6
    assert bool(row["is_set_aside"]) is True


def test_mixed_hood_below_threshold_stays_on_scale():
    # 50/50 natural/developed → below 0.90 → stays on scale.
    hood = _boundaries(["MIXED"], [_square(0, 0, 100)])
    zoning = _zoning(
        ["A", "RSF"],
        [Polygon([(0, 0), (50, 0), (50, 100), (0, 100)]),
         Polygon([(50, 0), (100, 0), (100, 100), (50, 100)])],
    )
    result = _run(hood, zoning)
    row = result.iloc[0]
    assert abs(row["set_aside_frac"] - 0.5) < 1e-6
    assert bool(row["is_set_aside"]) is False
    assert SET_ASIDE_THRESHOLD == 0.90


def test_notyet_counts_toward_set_aside():
    hood = _boundaries(["FRINGE"], [_square(0, 0, 100)])
    zoning = _zoning(["FD"], [_square(0, 0, 100)])
    result = _run(hood, zoning)
    row = result.iloc[0]
    assert row["frac_notyet"] == 1.0
    assert bool(row["is_set_aside"]) is True
    assert row["set_aside_reason"] == "Future / Rural / Reserve"


def test_institutional_stays_on_scale():
    hood = _boundaries(["CIVIC"], [_square(0, 0, 100)])
    zoning = _zoning(["PU"], [_square(0, 0, 100)])
    result = _run(hood, zoning)
    row = result.iloc[0]
    assert row["frac_inst"] == 1.0
    assert row["set_aside_frac"] == 0.0
    assert bool(row["is_set_aside"]) is False
