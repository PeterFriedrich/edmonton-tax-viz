import json
import sys

import pandas as pd
import pytest

sys.path.insert(0, "src")
from load_franchise import (
    _per_dwelling_charges,
    load_franchise,
    load_franchise_rates,
)

YEAR = 2026

# The verified schedule (Methods §D–E), mirrored from data/franchise_rates.json.
RATES = {
    "effective_electricity": "2025-01-01",
    "effective_gas": "2026-01-01",
    "elec_customer_daily": 0.69953,
    "elec_energy_per_kwh": 0.01712,
    "elec_kwh_per_dwelling_year": 7200.0,
    "elec_laf_fraction": 0.1765,
    "gas_fixed_daily": 0.997,
    "gas_variable_per_gj": 1.049,
    "gas_rider_t_per_gj": 1.357,
    "gas_rider_l_per_gj": 0.091,
    "gas_gj_per_dwelling_year": 115.0,
    "gas_franchise_fraction": 0.35,
}

# Hand-computed per-dwelling annual figures at this schedule.
ELEC_DIST = 365 * 0.69953 + 7200 * 0.01712
LAF = 0.1765 * ELEC_DIST
GAS_DELIV = 365 * 0.997 + 115 * (1.049 + 1.357 + 0.091)
GAS_FR = 0.35 * GAS_DELIV


def _write_rates(tmp_path):
    p = tmp_path / "franchise_rates.json"
    p.write_text(json.dumps({"years": {"2026": RATES}}))
    return p


def _assessment_row(account=1, cls="RESIDENTIAL", hood="ALPHA", lat=53.5, lon=-113.5):
    return {
        "Account Number": account,
        "Assessment Class 1": cls,
        "Neighbourhood": hood,
        "Latitude": lat,
        "Longitude": lon,
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
    return load_franchise(
        _write_assessment(tmp_path, assessment_rows),
        _write_info(tmp_path, list(info_rows)),
        _write_rates(tmp_path),
        YEAR,
    )


# --- rate loading / helpers ---------------------------------------------------

def test_missing_year_raises(tmp_path):
    with pytest.raises(ValueError, match="no franchise rates for 2024"):
        load_franchise_rates(_write_rates(tmp_path), 2024)


def test_per_dwelling_charges_match_hand_computation():
    pd_charges = _per_dwelling_charges(RATES)
    assert pd_charges["elec_distribution_annual"] == pytest.approx(ELEC_DIST)
    assert pd_charges["elec_laf_revenue"] == pytest.approx(LAF)
    assert pd_charges["gas_delivery_annual"] == pytest.approx(GAS_DELIV)
    assert pd_charges["gas_franchise_revenue"] == pytest.approx(GAS_FR)


# --- end-to-end ---------------------------------------------------------------

def test_single_dwelling_columns(tmp_path):
    out = _run(tmp_path, [_assessment_row()])
    assert list(out["neighbourhood_name"]) == ["ALPHA"]
    row = out.iloc[0]
    assert row["dwelling_count"] == pytest.approx(1.0)
    assert row["elec_laf_revenue"] == pytest.approx(LAF)
    assert row["gas_franchise_revenue"] == pytest.approx(GAS_FR)


def test_revenue_is_linear_in_dwellings(tmp_path):
    # Three separate single-family points in one hood -> 3 dwellings, 3x revenue.
    rows = [
        _assessment_row(account=1, lat=53.5),
        _assessment_row(account=2, lat=53.6),
        _assessment_row(account=3, lat=53.7),
    ]
    out = _run(tmp_path, rows)
    row = out.iloc[0]
    assert row["dwelling_count"] == pytest.approx(3.0)
    assert row["elec_laf_revenue"] == pytest.approx(3 * LAF)
    assert row["gas_franchise_revenue"] == pytest.approx(3 * GAS_FR)


def test_condo_point_counts_units_not_connections(tmp_path):
    # Two records at the SAME point = 2 dwellings (2 meters), unlike water's
    # one shared connection. Franchise bills per dwelling.
    rows = [_assessment_row(account=1), _assessment_row(account=2)]
    out = _run(tmp_path, rows)
    assert out.iloc[0]["dwelling_count"] == pytest.approx(2.0)
    assert out.iloc[0]["elec_laf_revenue"] == pytest.approx(2 * LAF)


def test_multires_units_from_floor_area(tmp_path):
    # OTHER RESIDENTIAL building, 900 m2 / 90 = 10 estimated dwellings.
    rows = [_assessment_row(cls="OTHER RESIDENTIAL", hood="BETA")]
    info = [{"Account Number": 1, "Total Gross Area": 900.0}]
    out = _run(tmp_path, rows, info)
    assert out.iloc[0]["dwelling_count"] == pytest.approx(10.0)
    assert out.iloc[0]["gas_franchise_revenue"] == pytest.approx(10 * GAS_FR)


def test_commercial_excluded(tmp_path):
    # No residential rows -> build_connections raises (shared with water).
    with pytest.raises(ValueError, match="no residential connections"):
        _run(tmp_path, [_assessment_row(cls="COMMERCIAL")])


def test_name_correction_applied(tmp_path):
    rows = [_assessment_row(hood="  place la rue "),
            _assessment_row(account=2, hood="PLACE LARUE", lat=53.9)]
    out = _run(tmp_path, rows)
    assert list(out["neighbourhood_name"]) == ["PLACE LARUE"]
    assert out.iloc[0]["dwelling_count"] == pytest.approx(2.0)
