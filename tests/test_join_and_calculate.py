import json
import sys

import geopandas as gpd
import pandas as pd
import pytest
from shapely.geometry import Point, Polygon

sys.path.insert(0, "src")
from join_and_calculate import (
    SLIM_COLUMNS, WEB_PRECISION, export_geojson, join_and_calculate,
)


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


def test_export_rounds_served_precision(tmp_path):
    # This file is fetched at boot by every visitor, so its precision is a served
    # cost, not a formatting detail. Read the raw text: parsing back to float
    # would not show what actually went over the wire.
    out = tmp_path / "slim.geojson"
    export_geojson(
        _result([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 1e6,
                  "area_acres": 100.0,
                  "value_per_acre": 18556.499688325515}]),
        str(out),
    )
    payload = json.loads(out.read_text())
    props = payload["features"][0]["properties"]
    assert props["value_per_acre"] == 18556.5

    coords = payload["features"][0]["geometry"]["coordinates"][0]
    for lon, lat in coords:
        for v in (lon, lat):
            _, _, frac = repr(float(v)).partition(".")
            assert len(frac) <= 5, f"{v} exceeds {WEB_PRECISION} dp"


def test_export_returns_unrounded_frame(tmp_path):
    # Only the file is rounded. Callers computing from the return value (main.py
    # passes it on) must still see full precision.
    out = tmp_path / "slim.geojson"
    slim = export_geojson(
        _result([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 1e6,
                  "area_acres": 100.0,
                  "value_per_acre": 18556.499688325515}]),
        str(out),
    )
    assert slim["value_per_acre"].iloc[0] == 18556.499688325515


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


# --- the RETIRED roads+fire composite (DECISIONS.md 2026-09-05) ---------------
# svc_cost_per_acre allocated the Fire Rescue budget to land by dispatch count.
# The decision audit found it 88.6% fire-term variance — a dispatch-density map
# priced in dollars (docs/FINDINGS_services_cost_lens_verdict.md §3). It is gone;
# the roads half survives as cost_roads_life_per_acre. These tests exist so it
# cannot come back by accident.

# Small synthetic numbers: $2/road-metre lifecycle.
_UNIT_COSTS = {"road_dollars_per_m": 2.0}


def test_no_service_cost_composite_even_with_roads_and_fire():
    """The retired column must not reappear when both its old inputs are present.

    ⚠️ Asserted with roads AND fire supplied and unit costs loaded — the exact
    state that used to produce it. A test that only checked a fire-less run
    would pass under a resurrected composite.
    """
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "GRIDTOWN", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "GRIDTOWN", "area_acres": 10.0}]),
        roads=_roads([{"neighbourhood_name": "GRIDTOWN", "road_m_total": 250.0}]),
        fire=_fire([{"neighbourhood_name": "GRIDTOWN", "fire_events_per_year": 30.0}]),
        unit_costs=_UNIT_COSTS,
    )
    assert "svc_cost_per_acre" not in result.columns
    assert "svc_cost_per_acre" not in SLIM_COLUMNS
    # The roads half still ships, on its own rate and nothing else.
    assert result.iloc[0]["cost_roads_life_per_acre"] == pytest.approx(25.0 * 2.0)


def test_fire_lens_survives_the_composite_retirement():
    """fire_events_per_acre is the fire lens and was NOT retired with the cost."""
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "GRIDTOWN", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "GRIDTOWN", "area_acres": 10.0}]),
        fire=_fire([{"neighbourhood_name": "GRIDTOWN", "fire_events_per_year": 30.0}]),
    )
    assert result.iloc[0]["fire_events_per_acre"] == pytest.approx(3.0)
    assert "fire_events_per_acre" in SLIM_COLUMNS


def test_no_unit_costs_omits_the_roads_lifecycle_column():
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "GRIDTOWN", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "GRIDTOWN", "area_acres": 10.0}]),
        roads=_roads([{"neighbourhood_name": "GRIDTOWN", "road_m_total": 250.0}]),
        fire=_fire([{"neighbourhood_name": "GRIDTOWN", "fire_events_per_year": 30.0}]),
    )
    assert "cost_roads_life_per_acre" not in result.columns


def test_export_keeps_cost_roads_life_per_acre_when_present(tmp_path):
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 10.0}]),
        roads=_roads([{"neighbourhood_name": "DOWNTOWN", "road_m_total": 250.0}]),
        unit_costs=_UNIT_COSTS,
    )
    written = export_geojson(result, str(tmp_path / "out.geojson"))
    assert "cost_roads_life_per_acre" in written.columns
    assert "svc_cost_per_acre" not in written.columns


# --- load_unit_costs (data/city_unit_costs.json, the reviewed input) ----------

def test_load_unit_costs_reads_committed_file():
    from join_and_calculate import load_unit_costs

    costs = load_unit_costs("data/city_unit_costs.json")
    assert costs["road_dollars_per_m"] == 50.0
    # The fire budget is no longer read — the composite it fed is retired, and
    # the JSON block stays only as the fire lens's sourcing record.
    assert "fire_budget_annual" not in costs


def test_load_unit_costs_missing_field_raises(tmp_path):
    from join_and_calculate import load_unit_costs

    bad = tmp_path / "unit_costs.json"
    bad.write_text('{"fire_response": {"operating_budget_gross_annual": 276706000}}')
    with pytest.raises(KeyError, match="roadway_om_renewal"):
        load_unit_costs(bad)


def test_load_unit_costs_needs_only_the_roadway_rate(tmp_path):
    """A file carrying the roads rate alone is valid — fire is not required."""
    from join_and_calculate import load_unit_costs

    ok = tmp_path / "unit_costs.json"
    ok.write_text('{"roadway_om_renewal": {"value": 50}}')
    assert load_unit_costs(ok) == {"road_dollars_per_m": 50.0}


def test_load_unit_costs_nonpositive_value_raises(tmp_path):
    from join_and_calculate import load_unit_costs

    bad = tmp_path / "unit_costs.json"
    bad.write_text('{"roadway_om_renewal": {"value": 0}}')
    with pytest.raises(ValueError, match="positive"):
        load_unit_costs(bad)


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


# --- residential-revenue decomposition (res_levy → res_revenue_per_acre) -----
# The RESIDENTIAL + OTHER RESIDENTIAL class subset of the levy, same boundary
# denominator as revenue_per_acre. The share ships nowhere — the client derives
# it as res/revenue per acre (denominators cancel).


def test_res_revenue_per_acre_computed():
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN",
                      "total_assessed_value": 1_000_000.0,
                      "total_revenue": 10_000.0, "total_res_revenue": 4_000.0}]),
        _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 100.0}]),
    )
    row = result.iloc[0]
    assert row["res_revenue_per_acre"] == pytest.approx(40.0)   # 4k / 100
    assert row["revenue_per_acre"] == pytest.approx(100.0)      # subset < total


def test_res_revenue_absent_without_upstream_column():
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN",
                      "total_assessed_value": 1_000_000.0, "total_revenue": 10_000.0}]),
        _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 100.0}]),
    )
    assert "res_revenue_per_acre" not in result.columns


def test_res_revenue_lot_acre_variant_and_suppression():
    # The lot variant divides by deduped parcel acres and inherits the
    # LOW_PARCEL_FRAC suppression like the other per-lot-acre dollar ratios.
    result = join_and_calculate(
        _assessment([
            {"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 1_000_000.0,
             "total_revenue": 10_000.0, "total_res_revenue": 4_000.0},
            {"neighbourhood_name": "PARK", "total_assessed_value": 100_000.0,
             "total_revenue": 1_000.0, "total_res_revenue": 400.0},
        ]),
        _boundaries([
            {"neighbourhood_name": "DOWNTOWN", "area_acres": 100.0},
            {"neighbourhood_name": "PARK", "area_acres": 100.0},
        ]),
        lot_acres=_lot([
            {"neighbourhood_name": "DOWNTOWN", "lot_acres_eligible": 50.0,
             "value_lot_eligible": 900_000.0, "revenue_lot_eligible": 9_000.0,
             "res_revenue_lot_eligible": 3_600.0},
            {"neighbourhood_name": "PARK", "lot_acres_eligible": 5.0,  # 5% parcel
             "value_lot_eligible": 90_000.0, "revenue_lot_eligible": 900.0,
             "res_revenue_lot_eligible": 360.0},
        ]),
    )
    dt = result[result["neighbourhood_name"] == "DOWNTOWN"].iloc[0]
    assert dt["res_revenue_per_lot_acre"] == pytest.approx(72.0)  # 3.6k / 50
    park = result[result["neighbourhood_name"] == "PARK"].iloc[0]
    assert pd.isna(park["res_revenue_per_lot_acre"])  # suppressed (< 15%)


def test_export_keeps_res_revenue_columns_when_present(tmp_path):
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN",
                      "total_assessed_value": 1_000_000.0,
                      "total_revenue": 10_000.0, "total_res_revenue": 4_000.0}]),
        _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 100.0}]),
        lot_acres=_lot([
            {"neighbourhood_name": "DOWNTOWN", "lot_acres_eligible": 50.0,
             "value_lot_eligible": 900_000.0, "revenue_lot_eligible": 9_000.0,
             "res_revenue_lot_eligible": 3_600.0},
        ]),
    )
    written = export_geojson(result, str(tmp_path / "out.geojson"))
    assert "res_revenue_per_acre" in written.columns
    assert "res_revenue_per_lot_acre" in written.columns
    # the raw total stays out of the slim file, like every other total
    assert "total_res_revenue" not in written.columns
    assert "res_revenue_lot_eligible" not in written.columns


# --- FAR (Development Lens B suitability proxy) ------------------------------

def test_far_passes_through_unsuppressed():
    # far rides through the lot-acre merge and is NOT subject to the
    # LOW_PARCEL_FRAC suppression that NaNs the per-lot-acre dollar ratios: PARK
    # is below the 15% parcel floor (value_per_lot_acre suppressed) but keeps
    # its far (a density ratio, independent of the denominator guard).
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
             "value_lot_eligible": 900_000.0, "far": 2.5},
            {"neighbourhood_name": "PARK", "lot_acres_eligible": 5.0,  # 5% parcel
             "value_lot_eligible": 90_000.0, "far": 0.02},
        ]),
    )
    dt = result[result["neighbourhood_name"] == "DOWNTOWN"].iloc[0]
    park = result[result["neighbourhood_name"] == "PARK"].iloc[0]
    assert dt["far"] == pytest.approx(2.5)
    assert park["far"] == pytest.approx(0.02)         # NOT suppressed
    assert pd.isna(park["value_per_lot_acre"])        # dollar ratio IS suppressed


def test_far_absent_when_not_in_lot_acres():
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 1_000_000.0}]),
        _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 100.0}]),
        lot_acres=_lot([
            {"neighbourhood_name": "DOWNTOWN", "lot_acres_eligible": 50.0,
             "value_lot_eligible": 900_000.0},
        ]),
    )
    assert "far" not in result.columns


def test_export_keeps_far_when_present(tmp_path):
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 1_000_000.0}]),
        _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 100.0}]),
        lot_acres=_lot([
            {"neighbourhood_name": "DOWNTOWN", "lot_acres_eligible": 50.0,
             "value_lot_eligible": 900_000.0, "far": 1.8},
        ]),
    )
    written = export_geojson(result, str(tmp_path / "out.geojson"))
    assert "far" in written.columns
    assert written.iloc[0]["far"] == pytest.approx(1.8)


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


def test_industrial_permits_per_acre_computed():
    # ind_permits (SPEC_industrial A3) rides the permit merge into
    # ind_permits_per_acre; a hood without it fills a true 0.
    result = join_and_calculate(
        _assessment([
            {"neighbourhood_name": "INDPARK", "total_assessed_value": 100.0},
            {"neighbourhood_name": "HOUSING", "total_assessed_value": 100.0},
        ]),
        _boundaries([
            {"neighbourhood_name": "INDPARK", "area_acres": 10.0},
            {"neighbourhood_name": "HOUSING", "area_acres": 10.0},
        ]),
        permits=_permits([
            {"neighbourhood_name": "INDPARK", "new_dwelling_units": 0.0,
             "new_dwelling_permits": 0, "ind_permits": 5},
            {"neighbourhood_name": "HOUSING", "new_dwelling_units": 30.0,
             "new_dwelling_permits": 12, "ind_permits": 0},
        ]),
    )
    ind = result.set_index("neighbourhood_name")
    assert ind.loc["INDPARK", "ind_permits"] == pytest.approx(5.0)
    assert ind.loc["INDPARK", "ind_permits_per_acre"] == pytest.approx(0.5)
    assert ind.loc["HOUSING", "ind_permits_per_acre"] == pytest.approx(0.0)


def test_industrial_permits_absent_when_column_missing():
    # A permit frame from before A3 (no ind_permits) omits the columns entirely.
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "GROWTOWN", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "GROWTOWN", "area_acres": 10.0}]),
        permits=_permits([
            {"neighbourhood_name": "GROWTOWN",
             "new_dwelling_units": 50.0, "new_dwelling_permits": 20},
        ]),
    )
    assert "ind_permits_per_acre" not in result.columns
    assert "ind_permits" not in result.columns


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


def test_permits_long_window_adds_suffixed_columns():
    # The optional long "since 2009" window duplicates the four activity columns
    # with a _long suffix, alongside (independent of) the base + 3yr windows.
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
        permits_long=_permits([
            {"neighbourhood_name": "GROWTOWN",
             "new_dwelling_units": 160.0, "new_dwelling_permits": 64},
        ]),
    )
    row = result.iloc[0]
    # base + recent windows untouched by the long window
    assert row["new_units_per_acre"] == pytest.approx(5.0)
    assert row["new_units_per_acre_3yr"] == pytest.approx(3.0)
    # long window, suffixed
    assert row["new_dwelling_units_long"] == pytest.approx(160.0)
    assert row["new_dwelling_permits_long"] == 64
    assert row["new_units_per_acre_long"] == pytest.approx(16.0)
    assert row["new_permits_per_acre_long"] == pytest.approx(6.4)  # 64 / 10


def test_permits_long_defaults_zero_and_omitted_when_absent():
    # A hood with no long-window permits gets a true 0; omitting permits_long
    # entirely omits every _long column (older data files / callers).
    with_long = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 100.0}]),
        _boundaries([
            {"neighbourhood_name": "DOWNTOWN", "area_acres": 10.0},
            {"neighbourhood_name": "QUIET", "area_acres": 20.0},
        ]),
        permits=_permits([
            {"neighbourhood_name": "DOWNTOWN",
             "new_dwelling_units": 10.0, "new_dwelling_permits": 4},
        ]),
        permits_long=_permits([
            {"neighbourhood_name": "DOWNTOWN",
             "new_dwelling_units": 40.0, "new_dwelling_permits": 16},
        ]),
    )
    quiet = with_long[with_long["neighbourhood_name"] == "QUIET"].iloc[0]
    assert quiet["new_dwelling_units_long"] == 0.0
    assert quiet["new_units_per_acre_long"] == 0.0

    without_long = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 10.0}]),
        permits=_permits([
            {"neighbourhood_name": "DOWNTOWN",
             "new_dwelling_units": 10.0, "new_dwelling_permits": 4},
        ]),
    )
    assert "new_units_per_acre_long" not in without_long.columns
    assert "new_dwelling_units_long" not in without_long.columns
    assert "new_units_per_acre" in without_long.columns  # base still present


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


# --- non-residential decomposition (nonres_levy → nonres_revenue_per_acre) ---
# The non-res-rate subset (COMMERCIAL + MA DERELICT + DESIGNATED IND slices,
# SPEC_industrial.md A1), same conventions as the residential block above.


def test_nonres_revenue_per_acre_computed():
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN",
                      "total_assessed_value": 1_000_000.0,
                      "total_revenue": 10_000.0, "total_nonres_revenue": 6_000.0}]),
        _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 100.0}]),
    )
    row = result.iloc[0]
    assert row["nonres_revenue_per_acre"] == pytest.approx(60.0)  # 6k / 100
    assert row["revenue_per_acre"] == pytest.approx(100.0)        # subset < total


def test_nonres_revenue_absent_without_upstream_column():
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN",
                      "total_assessed_value": 1_000_000.0, "total_revenue": 10_000.0}]),
        _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 100.0}]),
    )
    assert "nonres_revenue_per_acre" not in result.columns


def test_nonres_revenue_lot_acre_variant_and_suppression():
    result = join_and_calculate(
        _assessment([
            {"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 1_000_000.0,
             "total_revenue": 10_000.0, "total_nonres_revenue": 6_000.0},
            {"neighbourhood_name": "PARK", "total_assessed_value": 100_000.0,
             "total_revenue": 1_000.0, "total_nonres_revenue": 600.0},
        ]),
        _boundaries([
            {"neighbourhood_name": "DOWNTOWN", "area_acres": 100.0},
            {"neighbourhood_name": "PARK", "area_acres": 100.0},
        ]),
        lot_acres=_lot([
            {"neighbourhood_name": "DOWNTOWN", "lot_acres_eligible": 50.0,
             "value_lot_eligible": 900_000.0, "revenue_lot_eligible": 9_000.0,
             "nonres_revenue_lot_eligible": 5_400.0},
            {"neighbourhood_name": "PARK", "lot_acres_eligible": 5.0,  # 5% parcel
             "value_lot_eligible": 90_000.0, "revenue_lot_eligible": 900.0,
             "nonres_revenue_lot_eligible": 540.0},
        ]),
    )
    dt = result[result["neighbourhood_name"] == "DOWNTOWN"].iloc[0]
    assert dt["nonres_revenue_per_lot_acre"] == pytest.approx(108.0)  # 5.4k / 50
    park = result[result["neighbourhood_name"] == "PARK"].iloc[0]
    assert pd.isna(park["nonres_revenue_per_lot_acre"])  # suppressed (< 15%)


def test_export_keeps_nonres_revenue_columns_when_present(tmp_path):
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN",
                      "total_assessed_value": 1_000_000.0,
                      "total_revenue": 10_000.0, "total_nonres_revenue": 6_000.0}]),
        _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 100.0}]),
        lot_acres=_lot([
            {"neighbourhood_name": "DOWNTOWN", "lot_acres_eligible": 50.0,
             "value_lot_eligible": 900_000.0, "revenue_lot_eligible": 9_000.0,
             "nonres_revenue_lot_eligible": 5_400.0},
        ]),
    )
    written = export_geojson(result, str(tmp_path / "out.geojson"))
    assert "nonres_revenue_per_acre" in written.columns
    assert "nonres_revenue_per_lot_acre" in written.columns
    # the raw total stays out of the slim file, like every other total
    assert "total_nonres_revenue" not in written.columns
    assert "nonres_revenue_lot_eligible" not in written.columns


# --- Transportation lens Stage 2: the OPERATING-basis cost composite ----------
# cost_roads_ops_per_acre = road_m_per_acre × $/road-m/yr (maintenance + snow)
# cost_bike_ops_per_acre  = bike_m_per_acre × $/bike-m/yr (maintenance + snow)
# cost_transit_ops_per_acre = transit_dep_per_acre × (ETS budget ÷ the transit
#   frame's OWN citywide stop-event total)
# transport_cost_ops_per_acre = the three, ALL-OR-NOTHING.
#
# ⚠️ OPERATING basis — no capital replacement. cost_roads_ops_per_acre is NOT
# cost_roads_life_per_acre (same metres, different basis).

def _bike(rows):
    return pd.DataFrame(rows)


# $2/road-m ops, $8/bike-m ops, $400 ETS budget over 40 citywide stop-events.
# ⚠️ The lifecycle and operating road rates MUST DIFFER here. They were both
# $2.0/m until 2026-09-05, which made the "the two bases must not coincide" test
# below unable to fail for the reason it names: it compared the operating column
# against the roads+fire composite, and the FIRE term supplied the whole gap. A
# single rate wired into both columns would have passed. 10x mirrors the real
# $50 vs $4.635.
_TRANSPORT_COSTS = {
    **_UNIT_COSTS,
    "road_dollars_per_m": 20.0,
    "road_ops_dollars_per_m": 2.0,
    "bike_ops_dollars_per_m": 8.0,
    "transit_budget_annual": 400.0,
}


def _transport_kwargs():
    return {
        "roads": _roads([{"neighbourhood_name": "GRIDTOWN", "road_m_total": 250.0}]),
        "bike": _bike([{"neighbourhood_name": "GRIDTOWN", "bike_m_total": 100.0}]),
        "transit": _transit([{"neighbourhood_name": "GRIDTOWN",
                              "transit_dep_total": 40.0}]),
        "fire": _fire([{"neighbourhood_name": "GRIDTOWN",
                        "fire_events_per_year": 30.0}]),
    }


def test_transport_ops_terms_and_composite():
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "GRIDTOWN", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "GRIDTOWN", "area_acres": 10.0}]),
        unit_costs=_TRANSPORT_COSTS,
        **_transport_kwargs(),
    )
    row = result.iloc[0]
    # 25 road-m/acre × $2 = 50 ; 10 bike-m/acre × $8 = 80
    assert row["cost_roads_ops_per_acre"] == pytest.approx(50.0)
    assert row["cost_bike_ops_per_acre"] == pytest.approx(80.0)
    # $400 / 40 citywide stop-events = $10 ; 4 dep/acre × $10 = 40
    assert row["cost_transit_ops_per_acre"] == pytest.approx(40.0)
    assert row["transport_cost_ops_per_acre"] == pytest.approx(170.0)


def test_transport_ops_roads_term_differs_from_lifecycle_roads_term():
    """The two road terms are different bases and must not coincide.

    Guards the _ops suffix's whole reason for existing: cost_roads_life_per_acre
    uses the $50/m lifecycle rate, cost_roads_ops_per_acre the $4.635/m
    operating rate. If a future edit ever wires one rate into both, this fails.
    """
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "GRIDTOWN", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "GRIDTOWN", "area_acres": 10.0}]),
        unit_costs=_TRANSPORT_COSTS,
        **_transport_kwargs(),
    )
    row = result.iloc[0]
    roads_lifecycle = 25.0 * _TRANSPORT_COSTS["road_dollars_per_m"]   # $50
    assert row["cost_roads_ops_per_acre"] == pytest.approx(25.0 * 2.0)
    assert row["cost_roads_life_per_acre"] == pytest.approx(roads_lifecycle)
    # ⚠️ The two are ~10.8x apart on the SAME metres. Pin the gap, not just the
    # values: a single rate wired into both would still satisfy each line above
    # if the constants were also edited together.
    assert row["cost_roads_life_per_acre"] > 3 * row["cost_roads_ops_per_acre"]


def test_roads_lifecycle_is_the_supply_column_times_the_published_rate():
    """cost_roads_life_per_acre is road_m_per_acre x the lifecycle rate, exactly.

    It used to be pinned against the roads+fire composite as its component; with
    that composite retired the standalone column IS the lifecycle figure, so the
    thing to pin is its derivation from the supply column.
    """
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "GRIDTOWN", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "GRIDTOWN", "area_acres": 10.0}]),
        unit_costs=_TRANSPORT_COSTS,
        **_transport_kwargs(),
    )
    row = result.iloc[0]
    assert row["cost_roads_life_per_acre"] == pytest.approx(
        row["road_m_per_acre"] * _TRANSPORT_COSTS["road_dollars_per_m"]
    )


def test_roads_lifecycle_ships_without_fire_data():
    """The lifecycle column must survive a run with no fire frame.

    It has never depended on fire; this pins that it still does not, now that the
    branch it used to sit beside is gone.
    """
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "GRIDTOWN", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "GRIDTOWN", "area_acres": 10.0}]),
        roads=_roads([{"neighbourhood_name": "GRIDTOWN", "road_m_total": 250.0}]),
        unit_costs=_TRANSPORT_COSTS,
    )
    row = result.iloc[0]
    assert row["cost_roads_life_per_acre"] == pytest.approx(
        25.0 * _TRANSPORT_COSTS["road_dollars_per_m"]
    )


def test_roads_lifecycle_and_operating_stay_on_separate_bases():
    """The two roads cost columns are the same metres on incompatible bases.

    ⚠️ The expected ratio is DERIVED from the rates, never hardcoded: the whole
    point of keeping the rates in city_unit_costs.json is that improving one is
    a single-value edit, and a test pinning a literal 10.8 would red the build
    on exactly the edit we want to stay cheap.
    """
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "GRIDTOWN", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "GRIDTOWN", "area_acres": 10.0}]),
        unit_costs=_TRANSPORT_COSTS,
        **_transport_kwargs(),
    )
    row = result.iloc[0]
    expected = (_TRANSPORT_COSTS["road_dollars_per_m"]
                / _TRANSPORT_COSTS["road_ops_dollars_per_m"])
    assert (row["cost_roads_life_per_acre"]
            / row["cost_roads_ops_per_acre"]) == pytest.approx(expected)


def test_transit_ops_is_a_share_allocation_summing_to_the_budget():
    """⚠️ The per-departure figure is a SHARE, not a rate.

    transit_dep_total is a MEAN-WEEKDAY count while the budget is ANNUAL, so
    the intermediate unit is meaningless alone — but the terms must sum back to
    exactly the budget. Pins the identity against a future "unit fix" that
    scales by ~250 weekdays.
    """
    acres = {"GRIDTOWN": 10.0, "RIVERBEND": 40.0}
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": n, "total_assessed_value": 100.0}
                     for n in acres]),
        _boundaries([{"neighbourhood_name": n, "area_acres": a}
                     for n, a in acres.items()]),
        roads=_roads([{"neighbourhood_name": n, "road_m_total": 0.0} for n in acres]),
        bike=_bike([{"neighbourhood_name": n, "bike_m_total": 0.0} for n in acres]),
        transit=_transit([
            {"neighbourhood_name": "GRIDTOWN", "transit_dep_total": 30.0},
            {"neighbourhood_name": "RIVERBEND", "transit_dep_total": 10.0},
        ]),
        fire=_fire([{"neighbourhood_name": "GRIDTOWN", "fire_events_per_year": 30.0}]),
        unit_costs=_TRANSPORT_COSTS,
    )
    total_dollars = float(
        (result["cost_transit_ops_per_acre"]
         * result["neighbourhood_name"].map(acres)).sum()
    )
    assert total_dollars == pytest.approx(_TRANSPORT_COSTS["transit_budget_annual"])


def test_transit_ops_denominator_includes_unmatched_hoods():
    # Same rule as fire: a hood with no boundary match still consumed budget,
    # so it stays in the citywide denominator and shrinks the matched share.
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "GRIDTOWN", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "GRIDTOWN", "area_acres": 10.0}]),
        roads=_roads([{"neighbourhood_name": "GRIDTOWN", "road_m_total": 0.0}]),
        bike=_bike([{"neighbourhood_name": "GRIDTOWN", "bike_m_total": 0.0}]),
        transit=_transit([
            {"neighbourhood_name": "GRIDTOWN", "transit_dep_total": 40.0},
            {"neighbourhood_name": "NOWHERE", "transit_dep_total": 40.0},
        ]),
        fire=_fire([{"neighbourhood_name": "GRIDTOWN", "fire_events_per_year": 30.0}]),
        unit_costs=_TRANSPORT_COSTS,
    )
    # $400 / 80 = $5/dep ; 4 dep/acre × $5 = 20 (half of the matched-only case)
    assert result.iloc[0]["cost_transit_ops_per_acre"] == pytest.approx(20.0)


@pytest.mark.parametrize("missing", ["roads", "bike", "transit"])
def test_transport_composite_is_all_or_nothing(caplog, missing):
    kwargs = _transport_kwargs()
    kwargs[missing] = None
    with caplog.at_level("WARNING"):
        result = join_and_calculate(
            _assessment([{"neighbourhood_name": "GRIDTOWN",
                          "total_assessed_value": 100.0}]),
            _boundaries([{"neighbourhood_name": "GRIDTOWN", "area_acres": 10.0}]),
            unit_costs=_TRANSPORT_COSTS,
            **kwargs,
        )
    assert "transport_cost_ops_per_acre" not in result.columns
    assert f"cost_{missing}_ops_per_acre" not in result.columns
    assert "composite SKIPPED" in caplog.text
    # the surviving per-term columns still ship (disjoint by design)
    for other in {"roads", "bike", "transit"} - {missing}:
        assert f"cost_{other}_ops_per_acre" in result.columns


@pytest.mark.parametrize("key", ["road_ops_dollars_per_m", "bike_ops_dollars_per_m",
                                 "transit_budget_annual"])
def test_transport_composite_omitted_when_a_unit_cost_key_is_absent(key):
    costs = {k: v for k, v in _TRANSPORT_COSTS.items() if k != key}
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "GRIDTOWN", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "GRIDTOWN", "area_acres": 10.0}]),
        unit_costs=costs,
        **_transport_kwargs(),
    )
    assert "transport_cost_ops_per_acre" not in result.columns
    # the lifecycle column is unaffected by the operating trio being incomplete
    assert "cost_roads_life_per_acre" in result.columns


def test_transport_ops_columns_survive_the_slim_export(tmp_path):
    result = join_and_calculate(
        _assessment([{"neighbourhood_name": "DOWNTOWN", "total_assessed_value": 100.0}]),
        _boundaries([{"neighbourhood_name": "DOWNTOWN", "area_acres": 10.0}]),
        unit_costs=_TRANSPORT_COSTS,
        **{**_transport_kwargs(),
           "roads": _roads([{"neighbourhood_name": "DOWNTOWN", "road_m_total": 250.0}]),
           "bike": _bike([{"neighbourhood_name": "DOWNTOWN", "bike_m_total": 100.0}]),
           "transit": _transit([{"neighbourhood_name": "DOWNTOWN",
                                 "transit_dep_total": 40.0}]),
           "fire": _fire([{"neighbourhood_name": "DOWNTOWN",
                           "fire_events_per_year": 30.0}])},
    )
    written = export_geojson(result, str(tmp_path / "out.geojson"))
    for col in ("cost_roads_ops_per_acre", "cost_bike_ops_per_acre",
                "cost_transit_ops_per_acre", "transport_cost_ops_per_acre"):
        assert col in written.columns


def test_load_unit_costs_reads_the_committed_operating_trio():
    from join_and_calculate import load_unit_costs

    costs = load_unit_costs("data/city_unit_costs.json")
    assert costs["road_ops_dollars_per_m"] == pytest.approx(4.635)
    assert costs["bike_ops_dollars_per_m"] == pytest.approx(20.278)
    assert costs["transit_budget_annual"] == 436_605_000.0
    # ⚠️ the two road bases must stay distinct in the committed file
    assert costs["road_dollars_per_m"] != costs["road_ops_dollars_per_m"]


def test_load_unit_costs_operating_trio_is_optional(tmp_path):
    from join_and_calculate import load_unit_costs

    minimal = tmp_path / "unit_costs.json"
    minimal.write_text(
        '{"roadway_om_renewal": {"value": 50},'
        ' "fire_response": {"operating_budget_gross_annual": 276706000}}'
    )
    costs = load_unit_costs(minimal)
    assert "road_ops_dollars_per_m" not in costs


def test_load_unit_costs_malformed_operating_block_raises(tmp_path):
    """Present-but-broken is a hand-edit error — must fail, not silently skip."""
    from join_and_calculate import load_unit_costs

    bad = tmp_path / "unit_costs.json"
    bad.write_text(
        '{"roadway_om_renewal": {"value": 50},'
        ' "fire_response": {"operating_budget_gross_annual": 276706000},'
        ' "bikeway_ops": {"units": "dollars per metre"}}'
    )
    with pytest.raises(ValueError, match="bikeway_ops"):
        load_unit_costs(bad)
