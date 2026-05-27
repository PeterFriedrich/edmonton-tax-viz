import sys

import geopandas as gpd
import pandas as pd
import pytest
from shapely.geometry import Point

sys.path.insert(0, "src")
from plot_choropleth import plot_choropleth


def _make_gdf(rows):
    return gpd.GeoDataFrame(
        rows,
        geometry=[Point(0, 0)] * len(rows),
        crs="EPSG:3400",
    )


def test_output_file_created(tmp_path):
    gdf = _make_gdf([
        {"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 1e9, "area_acres": 100.0, "value_per_acre": 1e7},
        {"neighbourhood_name": "OUTER", "total_assessed_value": 5e7, "area_acres": 500.0, "value_per_acre": 1e5},
    ])
    out = tmp_path / "map.png"
    plot_choropleth(gdf, str(out))
    assert out.exists()
    assert out.stat().st_size > 0


def test_null_value_per_acre_does_not_crash(tmp_path):
    gdf = _make_gdf([
        {"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 1e9, "area_acres": 100.0, "value_per_acre": 1e7},
        {"neighbourhood_name": "NO DATA", "total_assessed_value": None, "area_acres": 50.0, "value_per_acre": None},
    ])
    out = tmp_path / "map.png"
    plot_choropleth(gdf, str(out))
    assert out.exists()
