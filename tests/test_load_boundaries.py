import sys
from unittest.mock import patch

import geopandas as gpd
import pytest
from shapely.geometry import MultiPolygon, Polygon

sys.path.insert(0, "src")
from load_boundaries import SQ_M_PER_ACRE, load_boundaries


def _make_gdf(names, polys, crs="EPSG:4326"):
    return gpd.GeoDataFrame(
        {"name": names, "geometry": polys},
        crs=crs,
    )


def _small_square(lon, lat, size=0.01):
    return MultiPolygon([Polygon([
        (lon, lat), (lon + size, lat),
        (lon + size, lat + size), (lon, lat + size),
    ])])


def test_reprojects_to_3400():
    gdf_in = _make_gdf(["DOWNTOWN"], [_small_square(-113.5, 53.5)])
    with patch("load_boundaries.gpd.read_file", return_value=gdf_in):
        result = load_boundaries("dummy.geojson")
    assert result.crs.to_epsg() == 3400


def test_area_acres_positive():
    gdf_in = _make_gdf(["DOWNTOWN"], [_small_square(-113.5, 53.5)])
    with patch("load_boundaries.gpd.read_file", return_value=gdf_in):
        result = load_boundaries("dummy.geojson")
    assert result.iloc[0]["area_acres"] > 0


def test_area_acres_not_in_degrees():
    # A 0.01-degree square near Edmonton is roughly 60–80 hectares (~150–200 acres).
    # If we forgot to reproject, area would be ~0.0001 (degrees squared).
    gdf_in = _make_gdf(["DOWNTOWN"], [_small_square(-113.5, 53.5)])
    with patch("load_boundaries.gpd.read_file", return_value=gdf_in):
        result = load_boundaries("dummy.geojson")
    assert result.iloc[0]["area_acres"] > 1.0


def test_normalizes_neighbourhood_name():
    gdf_in = _make_gdf(["  west end  ", "Downtown"], [
        _small_square(-113.6, 53.5),
        _small_square(-113.5, 53.5),
    ])
    with patch("load_boundaries.gpd.read_file", return_value=gdf_in):
        result = load_boundaries("dummy.geojson")
    assert list(result["neighbourhood_name"]) == ["WEST END", "DOWNTOWN"]


def test_output_columns():
    gdf_in = _make_gdf(["DOWNTOWN"], [_small_square(-113.5, 53.5)])
    with patch("load_boundaries.gpd.read_file", return_value=gdf_in):
        result = load_boundaries("dummy.geojson")
    assert set(result.columns) == {"neighbourhood_name", "geometry", "area_acres"}


def test_sq_m_per_acre_is_the_international_acre():
    """Pin the constant itself, as a LITERAL.

    ⚠️ Found 2026-09-07 by mutation (docs/FINDINGS_vacuous_guards.md V2):
    SQ_M_PER_ACRE could be HALVED — doubling every published per-acre figure,
    the project's headline metric — with all 784 tests green. Nothing pinned it.

    ⚠️ The literal is the point. tests/test_export_value_grid.py imports
    SQ_M_PER_ACRE from the module under test and computes its expected values
    with it, so ~40 assertions there move WITH the constant and cannot catch it
    changing. A test that derives the expectation from the value under test
    checks that the value equals itself. tests/test_load_roads.py already does
    this correctly by hardcoding 4046.8564224.
    """
    assert SQ_M_PER_ACRE == 4046.8564224
