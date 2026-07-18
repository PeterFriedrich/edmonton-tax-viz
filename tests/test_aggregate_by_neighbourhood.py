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


def test_levy_sums_into_total_revenue():
    df = _make_df([
        {"neighbourhood_name": "DOWNTOWN", "assessed_value": 100.0, "levy": 10.0, "is_exempt": False},
        {"neighbourhood_name": "DOWNTOWN", "assessed_value": 200.0, "levy": 30.0, "is_exempt": False},
    ])
    result = aggregate_by_neighbourhood(df)
    assert result.iloc[0]["total_revenue"] == 40.0


def test_res_levy_sums_into_total_res_revenue():
    # res_levy (the residential-class subset) aggregates alongside levy.
    df = _make_df([
        {"neighbourhood_name": "DOWNTOWN", "assessed_value": 100.0,
         "levy": 10.0, "res_levy": 10.0, "is_exempt": False},
        {"neighbourhood_name": "DOWNTOWN", "assessed_value": 200.0,
         "levy": 30.0, "res_levy": 0.0, "is_exempt": False},
    ])
    result = aggregate_by_neighbourhood(df)
    downtown = result.iloc[0]
    assert downtown["total_revenue"] == 40.0
    assert downtown["total_res_revenue"] == 10.0


def test_no_res_levy_no_total_res_revenue():
    # Without res_levy upstream the column stays absent (value-only path safe).
    df = _make_df([
        {"neighbourhood_name": "DOWNTOWN", "assessed_value": 100.0, "levy": 10.0, "is_exempt": False},
    ])
    result = aggregate_by_neighbourhood(df)
    assert "total_res_revenue" not in result.columns


def test_nonres_levy_sums_into_total_nonres_revenue():
    # nonres_levy (the non-res-rate subset) aggregates alongside levy/res_levy.
    df = _make_df([
        {"neighbourhood_name": "DOWNTOWN", "assessed_value": 100.0,
         "levy": 10.0, "nonres_levy": 0.0, "is_exempt": False},
        {"neighbourhood_name": "DOWNTOWN", "assessed_value": 200.0,
         "levy": 30.0, "nonres_levy": 30.0, "is_exempt": False},
    ])
    result = aggregate_by_neighbourhood(df)
    downtown = result.iloc[0]
    assert downtown["total_revenue"] == 40.0
    assert downtown["total_nonres_revenue"] == 30.0


def test_no_nonres_levy_no_total_nonres_revenue():
    df = _make_df([
        {"neighbourhood_name": "DOWNTOWN", "assessed_value": 100.0, "levy": 10.0, "is_exempt": False},
    ])
    result = aggregate_by_neighbourhood(df)
    assert "total_nonres_revenue" not in result.columns
