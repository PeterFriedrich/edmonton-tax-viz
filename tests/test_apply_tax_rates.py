import json
import sys

import pandas as pd
import pytest

sys.path.insert(0, "src")
from apply_tax_rates import apply_tax_rates, load_mill_rates


# Minimal synthetic rate table — same shape as data/mill_rates.json. Round
# numbers so expected levies are easy to verify by hand.
RATES = {
    "rates": {
        "2025": {
            "Residential":       {"municipal": 10.0, "education": 2.0},
            "Other Residential": {"municipal": 20.0, "education": 2.0},
            "Non Residential":   {"municipal": 30.0, "education": 4.0},
            "Farmland":          {"municipal": 10.0},
        }
    }
}


@pytest.fixture
def rates_path(tmp_path):
    p = tmp_path / "mill_rates.json"
    p.write_text(json.dumps(RATES))
    return p


def _row(**kwargs) -> dict:
    base = {
        "neighbourhood_name": "DOWNTOWN",
        "assessed_value": 1_000_000.0,
        "is_exempt": False,
        "tax_class": "Residential",
        "assessment_class_1": "RESIDENTIAL", "assessment_class_pct_1": 100,
        "assessment_class_2": None, "assessment_class_pct_2": None,
        "assessment_class_3": None, "assessment_class_pct_3": None,
    }
    return {**base, **kwargs}


def test_single_class_levy(rates_path):
    # $1,000,000 × 100% × (10/1000) = $10,000
    df = pd.DataFrame([_row()])
    out = apply_tax_rates(df, rates_path, 2025)
    assert out["levy"].iloc[0] == pytest.approx(10_000.0)


def test_non_residential_uses_commercial_label(rates_path):
    # COMMERCIAL label bills under the Non Residential rate (the vocab bridge):
    # $1,000,000 × 100% × (30/1000) = $30,000
    df = pd.DataFrame([_row(
        tax_class="Non Residential",
        assessment_class_1="COMMERCIAL",
    )])
    out = apply_tax_rates(df, rates_path, 2025)
    assert out["levy"].iloc[0] == pytest.approx(30_000.0)


def test_split_class_apportionment(rates_path):
    # 73% COMMERCIAL (Non Res, 30) + 27% RESIDENTIAL (10), on $1,000,000:
    #   1e6 × 0.73 × 0.030  +  1e6 × 0.27 × 0.010 = 21,900 + 2,700 = 24,600
    df = pd.DataFrame([_row(
        tax_class="Non Residential",
        assessment_class_1="COMMERCIAL", assessment_class_pct_1=73,
        assessment_class_2="RESIDENTIAL", assessment_class_pct_2=27,
    )])
    out = apply_tax_rates(df, rates_path, 2025)
    assert out["levy"].iloc[0] == pytest.approx(24_600.0)


def test_exempt_label_is_zero_levy(rates_path):
    df = pd.DataFrame([_row(
        is_exempt=True,
        tax_class="Non Residential",
        assessment_class_1="NONRES MUNICIPAL/RES EDUCATION",
    )])
    out = apply_tax_rates(df, rates_path, 2025)
    assert out["levy"].iloc[0] == pytest.approx(0.0)


def test_ma_derelict_bills_as_non_residential(rates_path):
    # MA DERELICT RESIDENTIAL → Non Residential rate (30), per the Tax Class data.
    df = pd.DataFrame([_row(
        tax_class="Non Residential",
        assessment_class_1="MA DERELICT RESIDENTIAL",
    )])
    out = apply_tax_rates(df, rates_path, 2025)
    assert out["levy"].iloc[0] == pytest.approx(30_000.0)


def test_designated_industrial_bills_as_non_residential(rates_path):
    # DESIGNATED IND PROPERTIES (Designated Industrial Property; appeared in the
    # 2026 live feed) → Non Residential rate (30), matching its Tax Class field.
    df = pd.DataFrame([_row(
        tax_class="Non Residential",
        assessment_class_1="DESIGNATED IND PROPERTIES",
    )])
    out = apply_tax_rates(df, rates_path, 2025)
    assert out["levy"].iloc[0] == pytest.approx(30_000.0)


def test_unknown_label_raises(rates_path):
    df = pd.DataFrame([_row(assessment_class_1="SPACE ELEVATOR")])
    with pytest.raises(KeyError, match="Unmapped assessment class"):
        apply_tax_rates(df, rates_path, 2025)


def test_pct_not_summing_to_100_is_flagged_and_billed_as_stated(rates_path, caplog):
    # 90% RESIDENTIAL only (source rounding gap). Billed as-stated: 90% of $10k.
    df = pd.DataFrame([_row(assessment_class_pct_1=90)])
    with caplog.at_level("WARNING"):
        out = apply_tax_rates(df, rates_path, 2025)
    assert out["levy"].iloc[0] == pytest.approx(9_000.0)
    assert any("not summing to 100" in r.message for r in caplog.records)


def test_missing_year_raises(rates_path):
    df = pd.DataFrame([_row()])
    with pytest.raises(KeyError, match="No mill rates for year 1999"):
        apply_tax_rates(df, rates_path, 1999)


def test_load_mill_rates_filters_by_rate_type(rates_path):
    rates = load_mill_rates(rates_path, 2025, "municipal")
    assert rates["Non Residential"] == 30.0
    # Farmland has no education rate → excluded from the education lookup.
    edu = load_mill_rates(rates_path, 2025, "education")
    assert "Farmland" not in edu
    assert edu["Residential"] == 2.0


def test_does_not_mutate_input(rates_path):
    df = pd.DataFrame([_row()])
    apply_tax_rates(df, rates_path, 2025)
    assert "levy" not in df.columns
    assert "res_levy" not in df.columns


# --- res_levy: the residential-revenue decomposition -------------------------
# res_levy = the subset of levy billed on RESIDENTIAL + OTHER RESIDENTIAL
# slices. MA DERELICT RESIDENTIAL is excluded (billed at the punitive Non
# Residential rate — those are non-residential-rate dollars).


def test_res_levy_equals_levy_for_pure_residential(rates_path):
    df = pd.DataFrame([_row()])
    out = apply_tax_rates(df, rates_path, 2025)
    assert out["res_levy"].iloc[0] == pytest.approx(10_000.0)
    assert out["res_levy"].iloc[0] == out["levy"].iloc[0]


def test_res_levy_includes_other_residential(rates_path):
    # OTHER RESIDENTIAL (4+ unit apartments) is housing: counts as residential.
    # $1,000,000 × 100% × (20/1000) = $20,000
    df = pd.DataFrame([_row(
        tax_class="Other Residential",
        assessment_class_1="OTHER RESIDENTIAL",
    )])
    out = apply_tax_rates(df, rates_path, 2025)
    assert out["res_levy"].iloc[0] == pytest.approx(20_000.0)


def test_res_levy_zero_for_commercial(rates_path):
    df = pd.DataFrame([_row(
        tax_class="Non Residential",
        assessment_class_1="COMMERCIAL",
    )])
    out = apply_tax_rates(df, rates_path, 2025)
    assert out["levy"].iloc[0] == pytest.approx(30_000.0)
    assert out["res_levy"].iloc[0] == pytest.approx(0.0)


def test_res_levy_takes_only_residential_slice_of_split_class(rates_path):
    # 73% COMMERCIAL + 27% RESIDENTIAL: res_levy = 1e6 × 0.27 × 0.010 = 2,700
    # (levy = 24,600 — see test_split_class_apportionment).
    df = pd.DataFrame([_row(
        tax_class="Non Residential",
        assessment_class_1="COMMERCIAL", assessment_class_pct_1=73,
        assessment_class_2="RESIDENTIAL", assessment_class_pct_2=27,
    )])
    out = apply_tax_rates(df, rates_path, 2025)
    assert out["res_levy"].iloc[0] == pytest.approx(2_700.0)


def test_res_levy_excludes_ma_derelict_residential(rates_path):
    # Billed at the Non Residential rate on purpose — NOT residential dollars.
    df = pd.DataFrame([_row(
        tax_class="Non Residential",
        assessment_class_1="MA DERELICT RESIDENTIAL",
    )])
    out = apply_tax_rates(df, rates_path, 2025)
    assert out["levy"].iloc[0] == pytest.approx(30_000.0)
    assert out["res_levy"].iloc[0] == pytest.approx(0.0)


def test_res_levy_zero_for_exempt(rates_path):
    df = pd.DataFrame([_row(
        is_exempt=True,
        tax_class="Non Residential",
        assessment_class_1="NONRES MUNICIPAL/RES EDUCATION",
    )])
    out = apply_tax_rates(df, rates_path, 2025)
    assert out["res_levy"].iloc[0] == pytest.approx(0.0)
