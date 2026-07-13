import sys

import pandas as pd
import pytest

sys.path.insert(0, "src")
from load_property_info import load_property_info


def _write_csv(tmp_path, rows):
    # Real header has many more columns; include an extra one to prove the
    # loader slims by usecols rather than assuming the exact schema. Every row
    # carries "Total Gross Area" (a required usecol) unless the test overrides it.
    df = pd.DataFrame([{"Total Gross Area": 100.0, **r} for r in rows])
    p = tmp_path / "property_info.csv"
    df.to_csv(p, index=False)
    return p


def test_loads_and_renames(tmp_path):
    p = _write_csv(tmp_path, [
        {"Account Number": 1, "lot_size": 335.0, "Total Gross Area": 112.0, "zoning": "RSF"},
        {"Account Number": 2, "lot_size": 1000.5, "Total Gross Area": 250.0, "zoning": "RSF"},
    ])
    df = load_property_info(p)
    assert set(df.columns) == {"account_number", "lot_size", "gross_area"}
    assert df.loc[df.account_number == 1, "lot_size"].iloc[0] == 335.0
    assert df.loc[df.account_number == 1, "gross_area"].iloc[0] == 112.0


def test_nonpositive_and_null_become_nan(tmp_path):
    p = _write_csv(tmp_path, [
        {"Account Number": 1, "lot_size": 0.0, "zoning": ""},
        {"Account Number": 2, "lot_size": -5.0, "zoning": ""},
        {"Account Number": 3, "lot_size": None, "zoning": ""},
        {"Account Number": 4, "lot_size": 200.0, "zoning": ""},
    ])
    df = load_property_info(p)
    assert df["lot_size"].isna().sum() == 3
    assert df["lot_size"].notna().sum() == 1


def test_gross_area_nonpositive_and_null_become_nan(tmp_path):
    p = _write_csv(tmp_path, [
        {"Account Number": 1, "lot_size": 335.0, "Total Gross Area": 0.0},
        {"Account Number": 2, "lot_size": 335.0, "Total Gross Area": -3.0},
        {"Account Number": 3, "lot_size": 335.0, "Total Gross Area": None},
        {"Account Number": 4, "lot_size": 335.0, "Total Gross Area": 112.0},
    ])
    df = load_property_info(p)
    assert df["gross_area"].isna().sum() == 3
    assert df.loc[df.account_number == 4, "gross_area"].iloc[0] == 112.0


def test_duplicate_accounts_raise(tmp_path):
    p = _write_csv(tmp_path, [
        {"Account Number": 1, "lot_size": 335.0, "zoning": ""},
        {"Account Number": 1, "lot_size": 400.0, "zoning": ""},
    ])
    with pytest.raises(ValueError, match="duplicated account"):
        load_property_info(p)
