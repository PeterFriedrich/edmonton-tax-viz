import sys

import geopandas as gpd
import pandas as pd
import pytest
from shapely.geometry import Point, Polygon

sys.path.insert(0, "src")
from join_and_calculate import export_geojson, join_and_calculate


def _assessment(rows):
    return pd.DataFrame(rows)


def _boundaries(rows):
    return gpd.GeoDataFrame(
        rows,
        geometry=[Point(0, 0)] * len(rows),
        crs="EPSG:3400",
    )


def test_value_per_acre_calculated_correctly():
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 1_000_000.0}]),
        _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 100.0}]),
    )
    assert result.iloc[0]["value_per_acre"] == pytest.approx(10_000.0)


def test_left_join_keeps_all_boundary_rows():
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 1_000_000.0}]),
        _boundaries([
            {"neighbourhood_name": "DOWNTOWN", "area_acres": 100.0},
            {"neighbourhood_name": "OUTER", "area_acres": 200.0},
        ]),
    )
    assert len(result) == 2
    assert "OUTER" in result["neighbourhood_name"].values


def test_boundary_with_no_assessment_has_null_value_per_acre():
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 1_000_000.0}]),
        _boundaries([
            {"neighbourhood_name": "DOWNTOWN", "area_acres": 100.0},
            {"neighbourhood_name": "OUTER", "area_acres": 200.0},
        ]),
    )
    outer = result[result["neighbourhood_name"] == "OUTER"].iloc[0]
    assert pd.isna(outer["value_per_acre"])


def test_zero_area_does_not_crash():
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 1_000_000.0}]),
        _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 0.0}]),
    )
    assert pd.isna(result.iloc[0]["value_per_acre"])


def test_unmatched_assessment_flagged(caplog):
    with caplog.at_level("WARNING", logger="join_and_calculate"):
        join_and_calculate(
            _assessment([
                {"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 1_000_000.0},
                {"neighbourhood_name": "GHOST TOWN", "total_assessed_value": 500_000.0},
            ]),
            _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 100.0}]),
        )
    assert "GHOST TOWN" in caplog.text


def test_unmatched_boundary_flagged(caplog):
    with caplog.at_level("WARNING", logger="join_and_calculate"):
        join_and_calculate(
            _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 1_000_000.0}]),
            _boundaries([
                {"neighbourhood_name": "DOWNTOWN", "area_acres": 100.0},
                {"neighbourhood_name": "UNMAPPED", "area_acres": 50.0},
            ]),
        )
    assert "UNMAPPED" in caplog.text


def test_output_columns():
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 1_000_000.0}]),
        _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 100.0}]),
    )
    assert set(result.columns) == {
        "neighbourhood_name", "total_assessed_value", "area_acres", "value_per_acre", "geometry"
    }


# --- export_geojson ---------------------------------------------------------

# A small square near Edmonton, expressed in EPSG:3400 (the CRS the join result
# carries). Coordinates are realistic Alberta 10-TM eastings/northings.
_SQUARE_3400 = Polygon([(600_000, 5_931_000), (600_100, 5_931_000),
                        (600_100, 5_931_100), (600_000, 5_931_100)])


def _result(rows):
    return gpd.GeoDataFrame(
        rows,
        geometry=[_SQUARE_3400] * len(rows),
        crs="EPSG:3400",
    )


def test_export_writes_only_slim_columns(tmp_path):
    out = tmp_path / "slim.geojson"
    export_geojson(
        _result([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 1e6,
                  "area_acres": 100.0, "value_per_acre": 10_000.0}]),
        str(out),
    )
    written = gpd.read_file(out)
    assert set(written.columns) == {"neighbourhood_name", "value_per_acre", "geometry"}


def test_export_reprojects_to_wgs84(tmp_path):
    out = tmp_path / "slim.geojson"
    export_geojson(
        _result([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 1e6,
                  "area_acres": 100.0, "value_per_acre": 10_000.0}]),
        str(out),
    )
    written = gpd.read_file(out)
    assert written.crs.to_epsg() == 4326
    # Geometry should now be lon/lat near Edmonton, not 6-digit projected metres.
    minx, miny, maxx, maxy = written.total_bounds
    assert -115 < minx < -112 and 52 < miny < 55


def test_export_drops_null_value_rows_and_logs(tmp_path, caplog):
    out = tmp_path / "slim.geojson"
    with caplog.at_level("WARNING", logger="join_and_calculate"):
        slim = export_geojson(
            _result([
                {"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 1e6,
                 "area_acres": 100.0, "value_per_acre": 10_000.0},
                {"neighbourhood_name": "EMPTY", "total_assessed_value": None,
                 "area_acres": 0.0, "value_per_acre": float("nan")},
            ]),
            str(out),
        )
    assert "EMPTY" in caplog.text
    assert list(slim["neighbourhood_name"]) == ["DOWNTOWN"]
    assert len(gpd.read_file(out)) == 1


def test_export_raises_without_crs(tmp_path):
    gdf = gpd.GeoDataFrame(
        [{"neighbourhood_name": "DOWNTOWN", "value_per_acre": 10_000.0}],
        geometry=[_SQUARE_3400],
        crs=None,
    )
    with pytest.raises(ValueError, match="no CRS"):
        export_geojson(gdf, str(tmp_path / "x.geojson"))
