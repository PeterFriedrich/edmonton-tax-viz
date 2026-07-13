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


# --- merge key uniqueness (validate="m:1", FINDINGS NEW-1) -------------------
# safe_area is computed once and reused positionally across every merge, so a
# duplicate right-hand key would fan the join out and silently misalign every
# downstream division. validate="m:1" must raise loudly instead.


def test_duplicate_assessment_key_raises():
    with pytest.raises(pd.errors.MergeError):
        join_and_calculate(
            _assessment([
                {"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 1_000_000.0},
                {"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 2_000_000.0},
            ]),
            _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 100.0}]),
        )


def test_duplicate_roads_key_raises():
    with pytest.raises(pd.errors.MergeError):
        join_and_calculate(
            _assessment([{"neighbourhood_name": "GRIDTOWN", "total_assessed_value": 100.0}]),
            _boundaries([{"neighbourhood_name": "GRIDTOWN", "area_acres": 10.0}]),
            roads=_roads([
                {"neighbourhood_name": "GRIDTOWN", "road_m_total": 250.0},
                {"neighbourhood_name": "GRIDTOWN", "road_m_total": 400.0},
            ]),
        )


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


def test_export_keeps_storm_charge_per_acre_when_present(tmp_path):
    out = tmp_path / "slim.geojson"
    export_geojson(
        _result([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 1e6,
                  "area_acres": 100.0, "value_per_acre": 10_000.0,
                  "storm_charge_annual": 5000.0, "storm_charge_per_acre": 50.0}]),
        str(out),
    )
    written = gpd.read_file(out)
    assert "storm_charge_per_acre" in written.columns
    # the per-acre ratio ships; the raw total stays out of the slim file
    assert "storm_charge_annual" not in written.columns


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


def test_setback_shrinks_footprint(tmp_path):
    # 100m square, 20m setback -> 60x60 = 3600 m^2 (down from 10000).
    slim = export_geojson(
        _result([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 1e6,
                  "area_acres": 100.0, "value_per_acre": 10_000.0}]),
        str(tmp_path / "slim.geojson"),
        setback_m=20.0,
    )
    area_m2 = slim.to_crs("EPSG:3400").area.iloc[0]
    assert area_m2 == pytest.approx(3600, rel=0.02)


def test_setback_collapses_sliver_falls_back_and_logs(tmp_path, caplog):
    # A 5m-wide sliver cannot survive a 20m inward buffer -> keep original (area ~500).
    sliver = Polygon([(600_000, 5_931_000), (600_005, 5_931_000),
                      (600_005, 5_931_100), (600_000, 5_931_100)])
    gdf = gpd.GeoDataFrame(
        [{"neighbourhood_name": "SLIVER", "value_per_acre": 10_000.0}],
        geometry=[sliver], crs="EPSG:3400",
    )
    with caplog.at_level("WARNING", logger="join_and_calculate"):
        slim = export_geojson(gdf, str(tmp_path / "slim.geojson"), setback_m=20.0)
    assert "SLIVER" in caplog.text and "collapsed" in caplog.text
    assert slim.to_crs("EPSG:3400").area.iloc[0] == pytest.approx(500, rel=0.02)


# A 100m square carrying redundant collinear midpoints on every edge. Douglas-
# Peucker drops the midpoints (zero deviation) back to the four corners.
_SQUARE_WITH_MIDPOINTS_3400 = Polygon([
    (600_000, 5_931_000), (600_050, 5_931_000), (600_100, 5_931_000),
    (600_100, 5_931_050), (600_100, 5_931_100), (600_050, 5_931_100),
    (600_000, 5_931_100), (600_000, 5_931_050),
])


def _midpoint_result():
    return gpd.GeoDataFrame(
        [{"neighbourhood_name": "DOWNTOWN", "value_per_acre": 10_000.0}],
        geometry=[_SQUARE_WITH_MIDPOINTS_3400], crs="EPSG:3400",
    )


def test_simplify_reduces_vertices_and_logs(tmp_path, caplog):
    from join_and_calculate import _count_vertices

    before = _count_vertices(_SQUARE_WITH_MIDPOINTS_3400)
    with caplog.at_level("INFO", logger="join_and_calculate"):
        slim = export_geojson(
            _midpoint_result(), str(tmp_path / "slim.geojson"), simplify_tolerance_m=5.0,
        )
    after = _count_vertices(slim.geometry.iloc[0])
    assert after < before
    assert "Simplify" in caplog.text and "reduction" in caplog.text


def test_simplify_preserves_value_per_acre(tmp_path):
    # Display-only: the value column must pass through untouched by simplification.
    slim = export_geojson(
        _midpoint_result(), str(tmp_path / "slim.geojson"), simplify_tolerance_m=5.0,
    )
    assert slim["value_per_acre"].iloc[0] == 10_000.0


def test_simplify_and_setback_compose(tmp_path):
    # Both display transforms applied together (setback then simplify): a 20m
    # setback on the 100m square -> 60x60 = 3600 m^2, simplify leaves area intact.
    slim = export_geojson(
        _midpoint_result(), str(tmp_path / "slim.geojson"),
        simplify_tolerance_m=5.0, setback_m=20.0,
    )
    area_m2 = slim.to_crs("EPSG:3400").area.iloc[0]
    assert area_m2 == pytest.approx(3600, rel=0.02)


# Full land-use composition ZONING_COLUMNS expects (use-mix view). Tests set
# only what they assert on; the rest default to 0.0.
_FRAC_DEFAULTS = {
    "frac_never": 0.0, "frac_notyet": 0.0, "frac_inst": 0.0,
    "frac_residential": 0.0, "frac_commercial": 0.0, "frac_industrial": 0.0,
    "frac_mixed": 0.0, "frac_dc": 0.0, "frac_other": 0.0,
}


def _zoning(rows):
    return pd.DataFrame([{**_FRAC_DEFAULTS, **row} for row in rows])


def test_zoning_merge_adds_set_aside_columns():
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "RIVER VALLEY", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "RIVER VALLEY", "area_acres": 10.0}]),
        zoning=_zoning([{
            "neighbourhood_name": "RIVER VALLEY", "set_aside_frac": 0.98,
            "is_set_aside": True, "set_aside_reason": "River Valley / Natural / Parks",
            "frac_never": 0.98, "frac_residential": 0.0, "is_residential": False,
        }]),
    )
    row = result.iloc[0]
    assert set([
        "set_aside_frac", "is_set_aside", "set_aside_reason",
        "frac_residential", "is_residential",
    ]).issubset(result.columns)
    assert bool(row["is_set_aside"]) is True
    assert row["set_aside_reason"] == "River Valley / Natural / Parks"
    assert bool(row["is_residential"]) is False


def test_zoning_merge_carries_composition_fractions():
    # The use-mix view needs the full composition in the output (and thus the
    # GeoJSON) — dominant use is derived client-side from these.
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "TOD", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "TOD", "area_acres": 10.0}]),
        zoning=_zoning([{
            "neighbourhood_name": "TOD", "set_aside_frac": 0.0,
            "is_set_aside": False, "set_aside_reason": "",
            "frac_residential": 0.4, "frac_mixed": 0.3, "frac_commercial": 0.2,
            "frac_dc": 0.1, "is_residential": False,
        }]),
    )
    row = result.iloc[0]
    assert row["frac_mixed"] == pytest.approx(0.3)
    assert row["frac_commercial"] == pytest.approx(0.2)
    assert row["frac_dc"] == pytest.approx(0.1)
    assert row["frac_industrial"] == 0.0
    assert row["frac_other"] == 0.0


def test_no_zoning_arg_omits_set_aside_columns():
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 10.0}]),
    )
    assert "is_set_aside" not in result.columns


def test_boundary_without_zoning_match_defaults_false(caplog):
    with caplog.at_level("WARNING"):
        result = join_and_calculate(
            _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 100.0}]),
            _boundaries([
                {"neighbourhood_name": "DOWNTOWN", "area_acres": 10.0},
                {"neighbourhood_name": "OUTER", "area_acres": 20.0},
            ]),
            zoning=_zoning([{
                "neighbourhood_name": "DOWNTOWN", "set_aside_frac": 0.1,
                "is_set_aside": False, "set_aside_reason": "",
                "frac_residential": 0.7, "is_residential": True,
            }]),
        )
    downtown = result[result["neighbourhood_name"] == "DOWNTOWN"].iloc[0]
    outer = result[result["neighbourhood_name"] == "OUTER"].iloc[0]
    assert bool(downtown["is_residential"]) is True
    assert bool(outer["is_set_aside"]) is False
    assert outer["set_aside_reason"] == ""
    # Boundary with no zoning overlay defaults is_residential=False too.
    assert bool(outer["is_residential"]) is False
    assert "no zoning overlay" in caplog.text


# --- roads merge (services lens, SPEC_services.md) ---------------------------

def _roads(rows):
    return pd.DataFrame(rows)


def test_roads_merge_adds_road_columns_and_per_acre():
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "GRIDTOWN", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "GRIDTOWN", "area_acres": 10.0}]),
        roads=_roads([{"neighbourhood_name": "GRIDTOWN", "road_m_total": 250.0}]),
    )
    row = result.iloc[0]
    assert row["road_m_total"] == pytest.approx(250.0)
    assert row["road_m_per_acre"] == pytest.approx(25.0)


def test_no_roads_arg_omits_road_columns():
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 10.0}]),
    )
    assert "road_m_total" not in result.columns
    assert "road_m_per_acre" not in result.columns


def test_boundary_without_roads_match_defaults_zero(caplog):
    with caplog.at_level("WARNING"):
        result = join_and_calculate(
            _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 100.0}]),
            _boundaries([
                {"neighbourhood_name": "DOWNTOWN", "area_acres": 10.0},
                {"neighbourhood_name": "ROADLESS", "area_acres": 20.0},
            ]),
            roads=_roads([{"neighbourhood_name": "DOWNTOWN", "road_m_total": 100.0}]),
        )
    roadless = result[result["neighbourhood_name"] == "ROADLESS"].iloc[0]
    assert roadless["road_m_total"] == 0.0
    assert roadless["road_m_per_acre"] == 0.0
    assert "no roads overlay" in caplog.text


def test_roads_and_zoning_merges_compose():
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "GRIDTOWN", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "GRIDTOWN", "area_acres": 10.0}]),
        zoning=_zoning([{
            "neighbourhood_name": "GRIDTOWN", "set_aside_frac": 0.1,
            "is_set_aside": False, "set_aside_reason": "",
            "frac_residential": 0.8, "is_residential": True,
        }]),
        roads=_roads([{"neighbourhood_name": "GRIDTOWN", "road_m_total": 250.0}]),
    )
    row = result.iloc[0]
    assert bool(row["is_residential"]) is True
    assert row["road_m_per_acre"] == pytest.approx(25.0)


# --- stormwater merge (utility lens #1, SPEC_utilities.md) --------------------

def _stormwater(rows):
    return pd.DataFrame(rows)


def test_stormwater_merge_adds_columns_and_per_acre():
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "GRIDTOWN", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "GRIDTOWN", "area_acres": 10.0}]),
        stormwater=_stormwater([
            {"neighbourhood_name": "GRIDTOWN", "storm_charge_annual": 5000.0},
        ]),
    )
    row = result.iloc[0]
    assert row["storm_charge_annual"] == pytest.approx(5000.0)
    assert row["storm_charge_per_acre"] == pytest.approx(500.0)


def test_no_stormwater_arg_omits_storm_columns():
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 10.0}]),
    )
    assert "storm_charge_annual" not in result.columns
    assert "storm_charge_per_acre" not in result.columns


def test_boundary_without_stormwater_match_defaults_zero(caplog):
    with caplog.at_level("WARNING"):
        result = join_and_calculate(
            _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 100.0}]),
            _boundaries([
                {"neighbourhood_name": "DOWNTOWN", "area_acres": 10.0},
                {"neighbourhood_name": "PARKLAND", "area_acres": 20.0},
            ]),
            stormwater=_stormwater([
                {"neighbourhood_name": "DOWNTOWN", "storm_charge_annual": 5000.0},
            ]),
        )
    parkland = result[result["neighbourhood_name"] == "PARKLAND"].iloc[0]
    assert parkland["storm_charge_annual"] == 0.0
    assert parkland["storm_charge_per_acre"] == 0.0
    assert "no modeled stormwater points" in caplog.text


# --- fire merge (services lens #3, SPEC_services.md "Fire lens") --------------

def _fire(rows):
    return pd.DataFrame(rows)


def test_fire_merge_adds_columns_and_per_acre():
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "GRIDTOWN", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "GRIDTOWN", "area_acres": 10.0}]),
        fire=_fire([
            {"neighbourhood_name": "GRIDTOWN", "fire_events_per_year": 30.0},
        ]),
    )
    row = result.iloc[0]
    assert row["fire_events_per_year"] == pytest.approx(30.0)
    assert row["fire_events_per_acre"] == pytest.approx(3.0)


def test_no_fire_arg_omits_fire_columns():
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 10.0}]),
    )
    assert "fire_events_per_year" not in result.columns
    assert "fire_events_per_acre" not in result.columns


def test_boundary_without_fire_match_defaults_zero(caplog):
    with caplog.at_level("WARNING"):
        result = join_and_calculate(
            _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 100.0}]),
            _boundaries([
                {"neighbourhood_name": "DOWNTOWN", "area_acres": 10.0},
                {"neighbourhood_name": "PARKLAND", "area_acres": 20.0},
            ]),
            fire=_fire([
                {"neighbourhood_name": "DOWNTOWN", "fire_events_per_year": 30.0},
            ]),
        )
    parkland = result[result["neighbourhood_name"] == "PARKLAND"].iloc[0]
    assert parkland["fire_events_per_year"] == 0.0
    assert parkland["fire_events_per_acre"] == 0.0
    assert "no fire events in the window" in caplog.text


def test_unmatched_fire_hood_flagged(caplog):
    with caplog.at_level("WARNING"):
        join_and_calculate(
            _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 100.0}]),
            _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 10.0}]),
            fire=_fire([
                {"neighbourhood_name": "DOWNTOWN", "fire_events_per_year": 30.0},
                {"neighbourhood_name": "NOWHERE", "fire_events_per_year": 5.0},
            ]),
        )
    assert "NOWHERE" in caplog.text


def test_export_keeps_fire_events_per_acre_when_present(tmp_path):
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 10.0}]),
        fire=_fire([
            {"neighbourhood_name": "DOWNTOWN", "fire_events_per_year": 30.0},
        ]),
    )
    written = export_geojson(result, str(tmp_path / "out.geojson"))
    assert "fire_events_per_acre" in written.columns
    # the raw total stays out of the slim file, like every other total
    assert "fire_events_per_year" not in written.columns


# --- transit merge (services lens #4, SPEC_services.md "Transit lens") --------

def _transit(rows):
    return pd.DataFrame(rows)


def test_transit_merge_adds_columns_and_per_acre():
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "GRIDTOWN", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "GRIDTOWN", "area_acres": 10.0}]),
        transit=_transit([
            {"neighbourhood_name": "GRIDTOWN", "transit_dep_total": 500.0},
        ]),
    )
    row = result.iloc[0]
    assert row["transit_dep_total"] == pytest.approx(500.0)
    assert row["transit_dep_per_acre"] == pytest.approx(50.0)


def test_no_transit_arg_omits_transit_columns():
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 10.0}]),
    )
    assert "transit_dep_total" not in result.columns
    assert "transit_dep_per_acre" not in result.columns


def test_boundary_without_transit_match_defaults_zero(caplog):
    with caplog.at_level("WARNING"):
        result = join_and_calculate(
            _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 100.0}]),
            _boundaries([
                {"neighbourhood_name": "DOWNTOWN", "area_acres": 10.0},
                {"neighbourhood_name": "PARKLAND", "area_acres": 20.0},
            ]),
            transit=_transit([
                {"neighbourhood_name": "DOWNTOWN", "transit_dep_total": 500.0},
            ]),
        )
    parkland = result[result["neighbourhood_name"] == "PARKLAND"].iloc[0]
    assert parkland["transit_dep_total"] == 0.0
    assert parkland["transit_dep_per_acre"] == 0.0
    assert "no served transit stops" in caplog.text


def test_unmatched_transit_hood_flagged(caplog):
    with caplog.at_level("WARNING"):
        join_and_calculate(
            _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 100.0}]),
            _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 10.0}]),
            transit=_transit([
                {"neighbourhood_name": "DOWNTOWN", "transit_dep_total": 500.0},
                {"neighbourhood_name": "NOWHERE", "transit_dep_total": 5.0},
            ]),
        )
    assert "NOWHERE" in caplog.text


def test_export_keeps_transit_dep_per_acre_when_present(tmp_path):
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 10.0}]),
        transit=_transit([
            {"neighbourhood_name": "DOWNTOWN", "transit_dep_total": 500.0},
        ]),
    )
    written = export_geojson(result, str(tmp_path / "out.geojson"))
    assert "transit_dep_per_acre" in written.columns
    # the raw total stays out of the slim file, like every other total
    assert "transit_dep_total" not in written.columns


# --- water merge (utility lens #2 — MODELED, residential scope) ---------------

def _water(rows):
    return pd.DataFrame(rows)


def test_water_merge_adds_columns_and_per_acre():
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "GRIDTOWN", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "GRIDTOWN", "area_acres": 10.0}]),
        water=_water([
            {"neighbourhood_name": "GRIDTOWN",
             "water_charge_annual": 1000.0, "water_fixed_annual": 400.0},
        ]),
    )
    row = result.iloc[0]
    assert row["water_charge_per_acre"] == pytest.approx(100.0)
    assert row["water_fixed_per_acre"] == pytest.approx(40.0)


def test_no_water_arg_omits_water_columns():
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 10.0}]),
    )
    assert "water_charge_per_acre" not in result.columns
    assert "water_fixed_per_acre" not in result.columns


def test_boundary_without_water_match_defaults_zero(caplog):
    with caplog.at_level("WARNING"):
        result = join_and_calculate(
            _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 100.0}]),
            _boundaries([
                {"neighbourhood_name": "DOWNTOWN", "area_acres": 10.0},
                {"neighbourhood_name": "PARKLAND", "area_acres": 20.0},
            ]),
            water=_water([
                {"neighbourhood_name": "DOWNTOWN",
                 "water_charge_annual": 1000.0, "water_fixed_annual": 400.0},
            ]),
        )
    parkland = result[result["neighbourhood_name"] == "PARKLAND"].iloc[0]
    assert parkland["water_charge_per_acre"] == 0.0
    assert parkland["water_fixed_per_acre"] == 0.0
    assert "no modeled water connections" in caplog.text


def test_export_keeps_water_per_acre_when_present(tmp_path):
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 10.0}]),
        water=_water([
            {"neighbourhood_name": "DOWNTOWN",
             "water_charge_annual": 1000.0, "water_fixed_annual": 400.0},
        ]),
    )
    written = export_geojson(result, str(tmp_path / "out.geojson"))
    assert "water_charge_per_acre" in written.columns
    assert "water_fixed_per_acre" in written.columns
    # the raw totals stay out of the slim file, like every other total
    assert "water_charge_annual" not in written.columns


# --- neighbourhood lot-acre denominator toggle ------------------------------

def _lot(rows):
    return pd.DataFrame(rows)


def test_lot_acre_columns_computed():
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 1_000_000.0}]),
        _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 100.0}]),
        lot_acres=_lot([
            {"neighbourhood_name": "DOWNTOWN", "lot_acres_eligible": 50.0,
             "value_lot_eligible": 900_000.0},
        ]),
    )
    row = result.iloc[0]
    assert row["parcel_frac"] == pytest.approx(0.5)          # 50 / 100
    assert row["value_per_lot_acre"] == pytest.approx(18_000.0)  # 900k / 50
    assert "revenue_per_lot_acre" not in result.columns      # no revenue path


def test_lot_acre_revenue_variant():
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN",
                      "total_assessed_value": 1_000_000.0, "total_revenue": 10_000.0}]),
        _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 100.0}]),
        lot_acres=_lot([
            {"neighbourhood_name": "DOWNTOWN", "lot_acres_eligible": 50.0,
             "value_lot_eligible": 900_000.0, "revenue_lot_eligible": 9_000.0},
        ]),
    )
    assert result.iloc[0]["revenue_per_lot_acre"] == pytest.approx(180.0)  # 9k / 50


def test_lot_acre_low_parcel_frac_suppressed(caplog):
    with caplog.at_level("INFO"):
        result = join_and_calculate(
            _assessment([
                {"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 1_000_000.0},
                {"neighbourhood_name": "PARK", "total_assessed_value": 100_000.0},
            ]),
            _boundaries([
                {"neighbourhood_name": "DOWNTOWN", "area_acres": 100.0},
                {"neighbourhood_name": "PARK", "area_acres": 100.0},
            ]),
            lot_acres=_lot([
                {"neighbourhood_name": "DOWNTOWN", "lot_acres_eligible": 50.0,
                 "value_lot_eligible": 900_000.0},
                {"neighbourhood_name": "PARK", "lot_acres_eligible": 5.0,   # 5% parcel
                 "value_lot_eligible": 90_000.0},
            ]),
        )
    park = result[result["neighbourhood_name"] == "PARK"].iloc[0]
    assert pd.isna(park["value_per_lot_acre"])           # suppressed (< 15%)
    assert park["parcel_frac"] == pytest.approx(0.05)    # but parcel_frac still ships
    assert "below 15% parcel land suppressed" in caplog.text
    dt = result[result["neighbourhood_name"] == "DOWNTOWN"].iloc[0]
    assert dt["value_per_lot_acre"] == pytest.approx(18_000.0)  # unaffected


def test_lot_acre_no_eligible_parcels_suppressed():
    # A hood with no eligible parcels (no lot_acres row) -> NaN parcel_frac ->
    # suppressed (the guard covers NaN, not just < floor).
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 1_000_000.0}]),
        _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 100.0}]),
        lot_acres=_lot([  # DOWNTOWN absent -> no eligible parcels
            {"neighbourhood_name": "OTHER", "lot_acres_eligible": 10.0,
             "value_lot_eligible": 50.0},
        ]),
    )
    assert pd.isna(result.iloc[0]["value_per_lot_acre"])
    assert pd.isna(result.iloc[0]["parcel_frac"])


def test_lot_acre_columns_absent_by_default():
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 1_000_000.0}]),
        _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 100.0}]),
    )
    assert "value_per_lot_acre" not in result.columns
    assert "parcel_frac" not in result.columns


def test_export_keeps_lot_acre_columns_when_present(tmp_path):
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 1_000_000.0}]),
        _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 100.0}]),
        lot_acres=_lot([
            {"neighbourhood_name": "DOWNTOWN", "lot_acres_eligible": 50.0,
             "value_lot_eligible": 900_000.0},
        ]),
    )
    written = export_geojson(result, str(tmp_path / "out.geojson"))
    assert "value_per_lot_acre" in written.columns
    assert "parcel_frac" in written.columns
    assert "lot_acres_eligible" not in written.columns  # raw total stays out of slim


# --- permits (Development & Infill lens A) -----------------------------------

def _permits(rows):
    return pd.DataFrame(rows)


def test_permits_merge_adds_columns_and_per_acre():
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "GROWTOWN", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "GROWTOWN", "area_acres": 10.0}]),
        permits=_permits([
            {"neighbourhood_name": "GROWTOWN",
             "new_dwelling_units": 50.0, "new_dwelling_permits": 20},
        ]),
    )
    row = result.iloc[0]
    assert row["new_dwelling_units"] == pytest.approx(50.0)
    assert row["new_dwelling_permits"] == 20
    assert row["new_units_per_acre"] == pytest.approx(5.0)
    assert row["new_permits_per_acre"] == pytest.approx(2.0)  # 20 permits / 10 acres


def test_no_permits_arg_omits_columns():
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 10.0}]),
    )
    assert "new_units_per_acre" not in result.columns
    assert "new_permits_per_acre" not in result.columns
    assert "new_dwelling_units" not in result.columns


def test_boundary_without_permits_defaults_zero(caplog):
    with caplog.at_level("INFO"):
        result = join_and_calculate(
            _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 100.0}]),
            _boundaries([
                {"neighbourhood_name": "DOWNTOWN", "area_acres": 10.0},
                {"neighbourhood_name": "QUIET", "area_acres": 20.0},
            ]),
            permits=_permits([
                {"neighbourhood_name": "DOWNTOWN",
                 "new_dwelling_units": 10.0, "new_dwelling_permits": 4},
            ]),
        )
    quiet = result[result["neighbourhood_name"] == "QUIET"].iloc[0]
    assert quiet["new_dwelling_units"] == 0.0
    assert quiet["new_units_per_acre"] == 0.0
    assert quiet["new_permits_per_acre"] == 0.0
    assert "no new residential permits" in caplog.text


def test_unmatched_permit_hood_warns_not_fails(caplog):
    # A permit hood with no boundary match is dropped with a warning (activity,
    # not money) — the join must NOT raise.
    with caplog.at_level("WARNING"):
        result = join_and_calculate(
            _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 100.0}]),
            _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 10.0}]),
            permits=_permits([
                {"neighbourhood_name": "DOWNTOWN",
                 "new_dwelling_units": 10.0, "new_dwelling_permits": 4},
                {"neighbourhood_name": "GHOSTVILLE",
                 "new_dwelling_units": 7.0, "new_dwelling_permits": 3},
            ]),
        )
    assert "GHOSTVILLE" not in set(result["neighbourhood_name"])
    assert "no boundary match" in caplog.text
    assert "warn-not-fail" in caplog.text


def test_export_keeps_permit_columns_when_present(tmp_path):
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 1_000_000.0}]),
        _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 100.0}]),
        permits=_permits([
            {"neighbourhood_name": "DOWNTOWN",
             "new_dwelling_units": 200.0, "new_dwelling_permits": 80},
        ]),
    )
    written = export_geojson(result, str(tmp_path / "out.geojson"))
    assert "new_units_per_acre" in written.columns
    assert "new_permits_per_acre" in written.columns
    assert "new_dwelling_units" in written.columns  # total kept for the tooltip
    assert "new_dwelling_permits" in written.columns


def test_permits_recent_window_adds_suffixed_columns():
    # The optional recent (3-year) window duplicates the four activity columns
    # with a _3yr suffix; the base (5yr) columns are untouched and unsuffixed.
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "GROWTOWN", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "GROWTOWN", "area_acres": 10.0}]),
        permits=_permits([
            {"neighbourhood_name": "GROWTOWN",
             "new_dwelling_units": 50.0, "new_dwelling_permits": 20},
        ]),
        permits_recent=_permits([
            {"neighbourhood_name": "GROWTOWN",
             "new_dwelling_units": 30.0, "new_dwelling_permits": 12},
        ]),
    )
    row = result.iloc[0]
    # base window unchanged
    assert row["new_units_per_acre"] == pytest.approx(5.0)
    assert row["new_permits_per_acre"] == pytest.approx(2.0)
    # recent window, suffixed
    assert row["new_dwelling_units_3yr"] == pytest.approx(30.0)
    assert row["new_dwelling_permits_3yr"] == 12
    assert row["new_units_per_acre_3yr"] == pytest.approx(3.0)
    assert row["new_permits_per_acre_3yr"] == pytest.approx(1.2)  # 12 / 10


def test_permits_recent_defaults_zero_and_omitted_when_absent():
    # A hood with no recent-window permits gets a true 0 in the _3yr columns;
    # omitting permits_recent entirely omits every _3yr column (older data files).
    with_recent = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 100.0}]),
        _boundaries([
            {"neighbourhood_name": "DOWNTOWN", "area_acres": 10.0},
            {"neighbourhood_name": "QUIET", "area_acres": 20.0},
        ]),
        permits=_permits([
            {"neighbourhood_name": "DOWNTOWN",
             "new_dwelling_units": 10.0, "new_dwelling_permits": 4},
        ]),
        permits_recent=_permits([
            {"neighbourhood_name": "DOWNTOWN",
             "new_dwelling_units": 6.0, "new_dwelling_permits": 3},
        ]),
    )
    quiet = with_recent[with_recent["neighbourhood_name"] == "QUIET"].iloc[0]
    assert quiet["new_dwelling_units_3yr"] == 0.0
    assert quiet["new_units_per_acre_3yr"] == 0.0
    assert quiet["new_permits_per_acre_3yr"] == 0.0

    without_recent = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 10.0}]),
        permits=_permits([
            {"neighbourhood_name": "DOWNTOWN",
             "new_dwelling_units": 10.0, "new_dwelling_permits": 4},
        ]),
    )
    assert "new_units_per_acre_3yr" not in without_recent.columns
    assert "new_dwelling_units_3yr" not in without_recent.columns
    assert "new_units_per_acre" in without_recent.columns  # base still present


def test_export_keeps_3yr_columns_when_present(tmp_path):
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 1_000_000.0}]),
        _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 100.0}]),
        permits=_permits([
            {"neighbourhood_name": "DOWNTOWN",
             "new_dwelling_units": 200.0, "new_dwelling_permits": 80},
        ]),
        permits_recent=_permits([
            {"neighbourhood_name": "DOWNTOWN",
             "new_dwelling_units": 120.0, "new_dwelling_permits": 50},
        ]),
    )
    written = export_geojson(result, str(tmp_path / "out.geojson"))
    assert "new_units_per_acre_3yr" in written.columns
    assert "new_permits_per_acre_3yr" in written.columns
    assert "new_dwelling_units_3yr" in written.columns
    assert "new_dwelling_permits_3yr" in written.columns
