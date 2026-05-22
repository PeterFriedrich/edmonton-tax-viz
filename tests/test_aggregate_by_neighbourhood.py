import sys

import pandas as pd

sys.path.insert(0, "src")
from aggregate_by_neighbourhood import aggregate_by_neighbourhood


def _make_df(rows: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(rows)


def test_sums_values_by_neighbourhood():
    df = _make_df([
        {"neighbourhood_name": "DOWNTOWN", "assessed_value": 100.0, "is_exempt": False},
        {"neighbourhood_name": "DOWNTOWN", "assessed_value": 200.0, "is_exempt": False},
        {"neighbourhood_name": "WEST END", "assessed_value": 50.0, "is_exempt": False},
    ])
    result = aggregate_by_neighbourhood(df)
    downtown = result[result["neighbourhood_name"] == "DOWNTOWN"].iloc[0]
    assert downtown["total_assessed_value"] == 300.0


def test_one_row_per_neighbourhood():
    df = _make_df([
        {"neighbourhood_name": "DOWNTOWN", "assessed_value": 100.0, "is_exempt": False},
        {"neighbourhood_name": "DOWNTOWN", "assessed_value": 200.0, "is_exempt": False},
        {"neighbourhood_name": "WEST END", "assessed_value": 50.0, "is_exempt": False},
    ])
    result = aggregate_by_neighbourhood(df)
    assert len(result) == 2
    assert result["neighbourhood_name"].nunique() == 2


def test_output_columns():
    df = _make_df([
        {"neighbourhood_name": "DOWNTOWN", "assessed_value": 100.0, "is_exempt": False},
    ])
    result = aggregate_by_neighbourhood(df)
    assert set(result.columns) == {"neighbourhood_name", "total_assessed_value"}


def test_single_neighbourhood():
    df = _make_df([
        {"neighbourhood_name": "ABBOTTSFIELD", "assessed_value": 165000.0, "is_exempt": False},
    ])
    result = aggregate_by_neighbourhood(df)
    assert len(result) == 1
    assert result.iloc[0]["total_assessed_value"] == 165000.0
