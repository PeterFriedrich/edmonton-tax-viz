import io
import sys

import pandas as pd
import pytest

sys.path.insert(0, "src")
from load_assessment import load_assessment
from aggregate_by_neighbourhood import aggregate_by_neighbourhood


def _write_csv(rows: list[dict]) -> str:
    df = pd.DataFrame(rows)
    return df.to_csv(index=False)


def _base_row(**kwargs) -> dict:
    defaults = {
        "Account Number": 1,
        "Suite": None,
        "House Number": 100,
        "Street Name": "Main St",
        "Neighbourhood ID": 1,
        "Neighbourhood": "DOWNTOWN",
        "Ward": "A",
        "Assessed Value": 500000,
        "Tax Class": "Residential",
        "Garage": "N",
        "Assessment Class 1": "RESIDENTIAL",
        "Assessment Class 2": None,
        "Assessment Class 3": None,
        "Assessment Class % 1": 100,
        "Assessment Class % 2": None,
        "Assessment Class % 3": None,
        "Latitude": 53.5,
        "Longitude": -113.5,
        "Point Location": "POINT (-113.5 53.5)",
    }
    return {**defaults, **kwargs}


def test_normalizes_neighbourhood_name(tmp_path):
    csv = tmp_path / "assess.csv"
    csv.write_text(_write_csv([
        _base_row(Neighbourhood="  downtown  "),
        _base_row(Neighbourhood="West End"),
    ]))
    df = load_assessment(csv)
    assert list(df["neighbourhood_name"]) == ["DOWNTOWN", "WEST END"]


def test_drops_zero_assessed_value(tmp_path):
    csv = tmp_path / "assess.csv"
    csv.write_text(_write_csv([
        _base_row(**{"Assessed Value": 0}),
        _base_row(**{"Assessed Value": 100000}),
    ]))
    df = load_assessment(csv)
    assert len(df) == 1
    assert df.iloc[0]["assessed_value"] == 100000.0


def test_drops_null_assessed_value(tmp_path):
    csv = tmp_path / "assess.csv"
    csv.write_text(_write_csv([
        _base_row(**{"Assessed Value": None}),
        _base_row(**{"Assessed Value": 200000}),
    ]))
    df = load_assessment(csv)
    assert len(df) == 1


def test_flags_exempt_rows_not_dropped(tmp_path):
    csv = tmp_path / "assess.csv"
    csv.write_text(_write_csv([
        _base_row(**{"Assessment Class 1": "NONRES MUNICIPAL/RES EDUCATION"}),
        _base_row(**{"Assessment Class 1": "RESIDENTIAL"}),
    ]))
    df = load_assessment(csv)
    assert len(df) == 2
    assert df[df["is_exempt"]].shape[0] == 1
    assert df[~df["is_exempt"]].shape[0] == 1


def test_applies_name_correction(tmp_path):
    csv = tmp_path / "assess.csv"
    csv.write_text(_write_csv([_base_row(Neighbourhood="Chappelle Area")]))
    df = load_assessment(csv)
    assert df.iloc[0]["neighbourhood_name"] == "CHAPPELLE"


def test_corrected_names_aggregate_together(tmp_path):
    # Regression: "CHAPPELLE AREA" and "CHAPPELLE" must collapse to one summed
    # row. Correcting after aggregation would leave two rows and duplicate the
    # boundary at the join. Corrections run before aggregation to prevent this.
    csv = tmp_path / "assess.csv"
    csv.write_text(_write_csv([
        _base_row(Neighbourhood="Chappelle Area", **{"Assessed Value": 300000}),
        _base_row(Neighbourhood="Chappelle", **{"Assessed Value": 200000}),
    ]))
    agg = aggregate_by_neighbourhood(load_assessment(csv))
    chappelle = agg[agg["neighbourhood_name"] == "CHAPPELLE"]
    assert len(chappelle) == 1
    assert chappelle.iloc[0]["total_assessed_value"] == pytest.approx(500000.0)


def test_output_columns(tmp_path):
    csv = tmp_path / "assess.csv"
    csv.write_text(_write_csv([_base_row()]))
    df = load_assessment(csv)
    assert set(df.columns) == {
        "account_number", "neighbourhood_name", "assessed_value", "is_exempt", "tax_class",
        "assessment_class_1", "assessment_class_2", "assessment_class_3",
        "assessment_class_pct_1", "assessment_class_pct_2", "assessment_class_pct_3",
        "latitude", "longitude",
    }


def test_carries_class_columns_through(tmp_path):
    # Revenue phase: the split-class label + percentage columns must survive load
    # (they feed apply_tax_rates). Split-class row → class 1 and 2 populated.
    csv = tmp_path / "assess.csv"
    csv.write_text(_write_csv([_base_row(**{
        "Tax Class": "Non Residential",
        "Assessment Class 1": "COMMERCIAL", "Assessment Class % 1": 73,
        "Assessment Class 2": "RESIDENTIAL", "Assessment Class % 2": 27,
    })]))
    row = load_assessment(csv).iloc[0]
    assert row["tax_class"] == "Non Residential"
    assert row["assessment_class_1"] == "COMMERCIAL"
    assert row["assessment_class_pct_1"] == 73
    assert row["assessment_class_2"] == "RESIDENTIAL"
    assert row["assessment_class_pct_2"] == 27


def test_assessed_value_is_float(tmp_path):
    csv = tmp_path / "assess.csv"
    csv.write_text(_write_csv([_base_row()]))
    df = load_assessment(csv)
    assert df["assessed_value"].dtype == float
