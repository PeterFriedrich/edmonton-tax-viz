import json
import sys

import geopandas as gpd
import pandas as pd
import pytest
from shapely.geometry import box

sys.path.insert(0, "src")
from load_stormwater import (
    ZONE_RUNOFF,
    load_stormwater,
    load_stormwater_rate,
    runoff_coefficient,
)
from load_zoning import ZONE_CATEGORY

# 2026 rate annualized: $0.00327/m2/day * 365
RATE_2026 = 0.00327 * 365


def _write_rates(tmp_path):
    p = tmp_path / "stormwater_rates.json"
    p.write_text(json.dumps({
        "intensity_default": 1.0,
        "years": {
            "2025": {"rate": 0.09275, "per": "m2_month", "effective": "2025-04-01"},
            "2026": {"rate": 0.00327, "per": "m2_day", "effective": "2026-04-01"},
        },
    }))
    return p


def _write_csv(tmp_path, rows):
    # Real header casing: zoning/lot_size lowercase, the rest Title Case
    # (DATA.md §2). Extra column proves the loader slims by usecols.
    df = pd.DataFrame(rows)
    df["Ward"] = "W"
    p = tmp_path / "property_info.csv"
    df.to_csv(p, index=False)
    return p


def _row(lat=53.5, lon=-113.5, zone="RS", lot=400.0, hood="ALPHA"):
    return {
        "zoning": zone, "lot_size": lot,
        "Latitude": lat, "Longitude": lon, "Neighbourhood": hood,
    }


# --- runoff_coefficient ------------------------------------------------------

def test_fixed_coefficient():
    assert runoff_coefficient("CB", 10_000) == 0.75
    assert runoff_coefficient("A", 10_000) == 0.2


def test_residential_split_direction():
    # Smaller residential lot -> HIGHER coverage -> higher R.
    assert runoff_coefficient("RS", 400) == 0.55
    assert runoff_coefficient("RS", 450) == 0.50
    assert runoff_coefficient("RSM", 400) == 0.60
    assert runoff_coefficient("RSM", 600) == 0.55


def test_dc_split_direction_reverses():
    # DC reverses: larger site -> higher R.
    assert runoff_coefficient("DC2", 500) == 0.55
    assert runoff_coefficient("DC2", 700) == 0.60


def test_unknown_zone_is_none():
    assert runoff_coefficient("NOPE", 500) is None


def test_every_zone_category_code_has_runoff():
    # The spatial fallback resolves against fixa-tstc, whose full code
    # vocabulary is ZONE_CATEGORY — every code must carry an R assignment
    # so fallback-resolved points never dead-end on an unassigned zone.
    missing = [c for c in ZONE_CATEGORY if c not in ZONE_RUNOFF]
    assert missing == []


# --- load_stormwater_rate ----------------------------------------------------

def test_rate_annualization(tmp_path):
    p = _write_rates(tmp_path)
    daily, i = load_stormwater_rate(p, 2026)
    assert daily == pytest.approx(RATE_2026)
    monthly, _ = load_stormwater_rate(p, 2025)
    assert monthly == pytest.approx(0.09275 * 12)
    assert i == 1.0


def test_missing_year_raises(tmp_path):
    p = _write_rates(tmp_path)
    with pytest.raises(ValueError, match="2030"):
        load_stormwater_rate(p, 2030)


# --- load_stormwater end-to-end -----------------------------------------------

def test_single_family_charge(tmp_path):
    csv = _write_csv(tmp_path, [_row(zone="RS", lot=400.0)])
    out = load_stormwater(csv, _write_rates(tmp_path), 2026)
    assert list(out["neighbourhood_name"]) == ["ALPHA"]
    assert out["storm_lot_m2"].iloc[0] == 400.0
    assert out["storm_effective_m2"].iloc[0] == pytest.approx(400 * 0.55)
    assert out["storm_charge_annual"].iloc[0] == pytest.approx(400 * 0.55 * RATE_2026)


def test_condo_shares_count_per_unit(tmp_path):
    # Repeated share-sized lot_size values are per-unit apportionment: 3 x 30 m2.
    csv = _write_csv(tmp_path, [_row(zone="RM", lot=30.0)] * 3)
    out = load_stormwater(csv, _write_rates(tmp_path), 2026)
    assert out["storm_lot_m2"].iloc[0] == pytest.approx(90.0)
    assert out["storm_effective_m2"].iloc[0] == pytest.approx(90.0 * 0.60)


def test_duplicated_parcel_counts_once(tmp_path):
    # Repeated parcel-sized values are duplication: 2 units x 2000 m2 -> 2000.
    csv = _write_csv(tmp_path, [_row(zone="RM", lot=2000.0)] * 2)
    out = load_stormwater(csv, _write_rates(tmp_path), 2026)
    assert out["storm_lot_m2"].iloc[0] == pytest.approx(2000.0)
    # 2000 m2 >= 450 -> the mid-res split's upper branch.
    assert out["storm_effective_m2"].iloc[0] == pytest.approx(2000.0 * 0.55)


def test_majority_null_point_excluded(tmp_path, caplog):
    rows = [_row(zone="RM", lot=None), _row(zone="RM", lot=None),
            _row(zone="RM", lot=30.0)]
    csv = _write_csv(tmp_path, rows)
    with caplog.at_level("WARNING"):
        out = load_stormwater(csv, _write_rates(tmp_path), 2026)
    assert len(out) == 0
    assert "excludes" in caplog.text


def test_unknown_zone_excluded_and_reported(tmp_path, caplog):
    csv = _write_csv(tmp_path, [
        _row(zone="ZZTOP", lot=500.0),
        _row(lat=53.6, zone="RS", lot=400.0),
    ])
    with caplog.at_level("WARNING"):
        out = load_stormwater(csv, _write_rates(tmp_path), 2026)
    assert out["storm_lot_m2"].sum() == 400.0
    assert "ZZTOP" in caplog.text


def test_zone_suffix_stripped_and_modal_fill(tmp_path):
    # "RM h16" parses to base code RM, and a zone-less unit at the same point
    # inherits the point's modal zone. Two share-sized repeats -> 2 x 30 m2.
    rows = [_row(zone="RM h16", lot=30.0), _row(zone=None, lot=30.0)]
    csv = _write_csv(tmp_path, rows)
    out = load_stormwater(csv, _write_rates(tmp_path), 2026)
    assert out["storm_lot_m2"].iloc[0] == pytest.approx(60.0)
    assert out["storm_effective_m2"].iloc[0] == pytest.approx(60.0 * 0.60)


def test_spatial_fallback_resolves_zone(tmp_path):
    # No zoning column value anywhere; the fixa-tstc polygon supplies it.
    csv = _write_csv(tmp_path, [_row(zone=None, lot=500.0)])
    zones = gpd.GeoDataFrame(
        {"zoning": ["RS h16"]},
        geometry=[box(-113.51, 53.49, -113.49, 53.51)],
        crs="EPSG:4326",
    )
    zpath = tmp_path / "zoning.geojson"
    zones.to_file(zpath, driver="GeoJSON")
    out = load_stormwater(csv, _write_rates(tmp_path), 2026, zoning_geojson=zpath)
    assert out["storm_effective_m2"].iloc[0] == pytest.approx(500 * 0.50)


def test_no_fallback_file_excludes_and_reports(tmp_path, caplog):
    csv = _write_csv(tmp_path, [_row(zone=None, lot=500.0)])
    with caplog.at_level("WARNING"):
        out = load_stormwater(csv, _write_rates(tmp_path), 2026,
                              zoning_geojson=tmp_path / "missing.geojson")
    assert len(out) == 0
    assert "fallback" in caplog.text


def test_hood_aggregation_and_name_corrections(tmp_path):
    rows = [
        _row(lat=53.50, hood="PLACE LA RUE"),          # NAME_CORRECTIONS target
        _row(lat=53.51, hood="  place larue "),         # normalization target
        _row(lat=53.60, hood="BETA"),
    ]
    csv = _write_csv(tmp_path, rows)
    out = load_stormwater(csv, _write_rates(tmp_path), 2026)
    assert sorted(out["neighbourhood_name"]) == ["BETA", "PLACE LARUE"]
    larue = out[out["neighbourhood_name"] == "PLACE LARUE"]
    assert larue["storm_lot_m2"].iloc[0] == pytest.approx(800.0)
