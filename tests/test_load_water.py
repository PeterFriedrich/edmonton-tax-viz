import json
import sys

import pandas as pd
import pytest

sys.path.insert(0, "src")
from load_water import (
    MONTHLY_M3_PER_HOUSEHOLD,
    _block_charge,
    _meter_size_mm,
    load_water,
    load_water_rates,
)

YEAR = 2026

# The verified 2026 schedule (Methods §A–B), mirrored from data/water_rates.json.
RATES = {
    "effective": "2026-04-01",
    "water_fixed_daily": {"15": 0.5359, "25": 1.3401, "100": 13.3996, "300": 90.4715},
    "sanitary_fixed_daily": {"15": 0.3625, "25": 1.0150, "100": 10.3248, "300": 77.3296},
    "wastewater_fixed_daily": 0.2269,
    "water_blocks_residential": [[10.0, 2.5258], [35.0, 2.7593], [None, 3.4873]],
    "water_blocks_multires": [[100.0, 2.3842], [1000.0, 1.9949], [None, 1.6484]],
    "wastewater_per_m3": 1.302,
    "sanitary_per_m3": 1.27331,
}

# Hand-computed single-family annual bill at the 2026 schedule:
# fixed = 365 * (0.5359 + 0.3625 + 0.2269)
# vol   = 12 * (10*2.5258 + 4.3*2.7593 + 14.3*(1.302 + 1.27331))
SF_FIXED = 365 * (0.5359 + 0.3625 + 0.2269)
SF_VOL = 12 * (10 * 2.5258 + 4.3 * 2.7593 + 14.3 * (1.302 + 1.27331))


def _write_rates(tmp_path):
    p = tmp_path / "water_rates.json"
    p.write_text(json.dumps({"years": {"2026": RATES}}))
    return p


def _assessment_row(account=1, cls="RESIDENTIAL", hood="ALPHA", lat=53.5, lon=-113.5):
    return {
        "Account Number": account,
        "Assessment Class 1": cls,
        "Neighbourhood": hood,
        "Latitude": lat,
        "Longitude": lon,
        # extra column proves the loader slims by usecols
        "Assessed Value": 100000,
    }


def _write_assessment(tmp_path, rows):
    p = tmp_path / "assessment.csv"
    pd.DataFrame(rows).to_csv(p, index=False)
    return p


def _write_info(tmp_path, rows):
    df = pd.DataFrame(rows if rows else [{"Account Number": 0, "Total Gross Area": None}])
    df["Ward"] = "W"
    p = tmp_path / "property_info.csv"
    df.to_csv(p, index=False)
    return p


def _run(tmp_path, assessment_rows, info_rows=()):
    return load_water(
        _write_assessment(tmp_path, assessment_rows),
        _write_info(tmp_path, list(info_rows)),
        _write_rates(tmp_path),
        YEAR,
    )


# --- rate loading / helpers ---------------------------------------------------

def test_missing_year_raises(tmp_path):
    with pytest.raises(ValueError, match="no water rates for 2024"):
        load_water_rates(_write_rates(tmp_path), 2024)


def test_meter_size_bands():
    assert [_meter_size_mm(u) for u in (1, 2, 49, 50, 299, 300, 1279)] == \
        [15, 25, 25, 100, 100, 300, 300]


def test_block_charge_inclining():
    # 14.3 m³ on the residential schedule: 10 @ first block + 4.3 @ second.
    expected = 10 * 2.5258 + 4.3 * 2.7593
    assert _block_charge(14.3, RATES["water_blocks_residential"]) == pytest.approx(expected)


def test_block_charge_declining_spans_blocks():
    # 20 units * 14.3 = 286 m³/month: 100 @ block 1, 186 @ block 2.
    expected = 100 * 2.3842 + 186 * 1.9949
    assert _block_charge(20 * 14.3, RATES["water_blocks_multires"]) == pytest.approx(expected)


def test_block_charge_requires_open_ended_block():
    with pytest.raises(ValueError, match="open-ended"):
        _block_charge(50.0, [[10.0, 1.0]])


# --- load_water ----------------------------------------------------------------

def test_single_family_bill(tmp_path):
    out = _run(tmp_path, [_assessment_row()])
    assert list(out["neighbourhood_name"]) == ["ALPHA"]
    assert out["water_fixed_annual"].iloc[0] == pytest.approx(SF_FIXED)
    assert out["water_charge_annual"].iloc[0] == pytest.approx(SF_FIXED + SF_VOL)


def test_condo_units_share_one_connection(tmp_path):
    # Three RESIDENTIAL records at one point = ONE connection: 25mm meter,
    # multi-res declining block on 3 * 14.3 m³.
    rows = [_assessment_row(account=i) for i in (1, 2, 3)]
    out = _run(tmp_path, rows)
    fixed = 365 * (1.3401 + 1.0150 + 0.2269)
    m3 = 3 * MONTHLY_M3_PER_HOUSEHOLD
    vol = 12 * (m3 * 2.3842 + m3 * (1.302 + 1.27331))
    assert out["water_fixed_annual"].iloc[0] == pytest.approx(fixed)
    assert out["water_charge_annual"].iloc[0] == pytest.approx(fixed + vol)


def test_multires_units_from_floor_area(tmp_path):
    # 900 m² gross at 90 m²/unit -> 10 units, 25mm; 143 m³/month spans the
    # first declining-block boundary (100 @ block 1 + 43 @ block 2).
    rows = [_assessment_row(account=7, cls="OTHER RESIDENTIAL")]
    out = _run(tmp_path, rows, [{"Account Number": 7, "Total Gross Area": 900.0}])
    fixed = 365 * (1.3401 + 1.0150 + 0.2269)
    m3 = 10 * MONTHLY_M3_PER_HOUSEHOLD
    vol = 12 * (100 * 2.3842 + (m3 - 100) * 1.9949 + m3 * (1.302 + 1.27331))
    assert out["water_charge_annual"].iloc[0] == pytest.approx(fixed + vol)


def test_multires_null_area_excluded_and_reported(tmp_path, caplog):
    rows = [_assessment_row(),
            _assessment_row(account=7, cls="OTHER RESIDENTIAL", lat=53.6)]
    with caplog.at_level("WARNING"):
        out = _run(tmp_path, rows, [{"Account Number": 7, "Total Gross Area": None}])
    assert "1 of 1 multi-res buildings have null/zero gross floor area" in caplog.text
    # Only the single-family connection remains.
    assert out["water_charge_annual"].iloc[0] == pytest.approx(SF_FIXED + SF_VOL)


def test_out_of_scope_classes_excluded_and_counted(tmp_path, caplog):
    rows = [_assessment_row(),
            _assessment_row(account=2, cls="COMMERCIAL", lat=53.7),
            _assessment_row(account=3, cls="FARMLAND", lat=53.8)]
    with caplog.at_level("INFO"):
        out = _run(tmp_path, rows)
    assert "2 rows out of scope" in caplog.text
    assert out["water_charge_annual"].iloc[0] == pytest.approx(SF_FIXED + SF_VOL)


def test_derelict_residential_is_a_household(tmp_path):
    out = _run(tmp_path, [_assessment_row(cls="MA DERELICT RESIDENTIAL")])
    assert out["water_charge_annual"].iloc[0] == pytest.approx(SF_FIXED + SF_VOL)


def test_null_coords_excluded_and_reported(tmp_path, caplog):
    rows = [_assessment_row(),
            _assessment_row(account=2, lat=None, lon=None)]
    with caplog.at_level("WARNING"):
        out = _run(tmp_path, rows)
    assert "1 household rows have null coordinates" in caplog.text
    assert out["water_charge_annual"].iloc[0] == pytest.approx(SF_FIXED + SF_VOL)


def test_hood_normalized_and_corrected(tmp_path):
    # strip + uppercase + NAME_CORRECTIONS (PLACE LA RUE -> PLACE LARUE).
    rows = [_assessment_row(hood="  place la rue "),
            _assessment_row(account=2, hood="PLACE LARUE", lat=53.9)]
    out = _run(tmp_path, rows)
    assert list(out["neighbourhood_name"]) == ["PLACE LARUE"]
    assert out["water_charge_annual"].iloc[0] == pytest.approx(2 * (SF_FIXED + SF_VOL))


def test_no_connections_raises(tmp_path):
    with pytest.raises(ValueError, match="no water connections"):
        _run(tmp_path, [_assessment_row(cls="COMMERCIAL")])
