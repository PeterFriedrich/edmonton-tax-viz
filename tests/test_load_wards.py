import sys

import pandas as pd
import pytest

sys.path.insert(0, "src")
from load_wards import COMPOUND_WARD_VALUES, load_wards


def _csv(tmp_path, rows):
    """Write a minimal property-info CSV; extra columns prove usecols works."""
    path = tmp_path / "property_info.csv"
    pd.DataFrame(
        [{"Account Number": f"{i}", "Neighbourhood": h, "Ward": w, "lot_size": "300"}
         for i, (h, w) in enumerate(rows)]
    ).to_csv(path, index=False)
    return path


def test_one_row_per_neighbourhood(tmp_path):
    path = _csv(tmp_path, [
        ("BONNIE DOON", "Métis"), ("BONNIE DOON", "Métis"), ("DOWNTOWN", "O-day'min"),
    ])
    result = load_wards(path)
    assert len(result) == 2
    assert set(result["neighbourhood_name"]) == {"BONNIE DOON", "DOWNTOWN"}


def test_maps_hood_to_its_ward(tmp_path):
    path = _csv(tmp_path, [("BONNIE DOON", "Métis"), ("DOWNTOWN", "O-day'min")])
    result = load_wards(path).set_index("neighbourhood_name")["ward"]
    assert result["BONNIE DOON"] == "Métis"
    assert result["DOWNTOWN"] == "O-day'min"


def test_raises_when_a_neighbourhood_spans_two_wards(tmp_path):
    """The 1:1 relation is what makes a ward rollup a regroup, not a re-aggregation."""
    path = _csv(tmp_path, [("BONNIE DOON", "Métis"), ("BONNIE DOON", "papastew")])
    with pytest.raises(ValueError, match="span multiple wards"):
        load_wards(path)


def test_hood_with_no_ward_is_kept_as_na_not_dropped(tmp_path):
    path = _csv(tmp_path, [("BONNIE DOON", "Métis"), ("CHAPPELLE AREA", None)])
    result = load_wards(path)
    assert len(result) == 2, "a hood without a ward must not vanish from the lookup"
    assert result.set_index("neighbourhood_name")["ward"].isna()["CHAPPELLE AREA"]


def test_partial_ward_coverage_resolves_to_the_known_ward(tmp_path):
    """A hood with some blank rows still has exactly one ward, not zero."""
    path = _csv(tmp_path, [("BONNIE DOON", "Métis"), ("BONNIE DOON", None)])
    result = load_wards(path).set_index("neighbourhood_name")["ward"]
    assert result["BONNIE DOON"] == "Métis"


def test_compound_ward_value_is_preserved_verbatim(tmp_path):
    """Never split or guess — the source makes no per-parcel assignment."""
    compound = next(iter(COMPOUND_WARD_VALUES))
    path = _csv(tmp_path, [("GLENRIDDING RAVINE", compound)])
    result = load_wards(path).set_index("neighbourhood_name")["ward"]
    assert result["GLENRIDDING RAVINE"] == compound


def test_rows_without_a_neighbourhood_do_not_become_a_hood(tmp_path):
    path = _csv(tmp_path, [("BONNIE DOON", "Métis"), (None, "Métis")])
    result = load_wards(path)
    assert len(result) == 1
    assert result["neighbourhood_name"].notna().all()
