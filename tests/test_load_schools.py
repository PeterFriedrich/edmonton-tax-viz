import logging
import sys

import pandas as pd
import pytest

sys.path.insert(0, "src")
from load_schools import load_schools


EPSB_ROWS = [
    {"school_nam": "Allendale", "sch_type": "EL", "latitude": 53.501, "longitude": -113.503},
    {"school_nam": "Steele Heights", "sch_type": "JR", "latitude": 53.608, "longitude": -113.431},
    # A city-wide program: excluded, and the exclusion is the point of the module.
    {"school_nam": "Metro Continuing Ed.", "sch_type": "SP", "latitude": 53.510, "longitude": -113.520},
]

ECSD_ROWS = [
    {"school_name": "St. Joseph", "grade_level": "Senior", "latitude": 53.553, "longitude": -113.509},
    {"school_name": "CCAC-Westmount", "grade_level": "Outreach", "latitude": 53.567, "longitude": -113.540},
]


def _write(tmp_path, epsb=None, ecsd=None):
    a = tmp_path / "public.csv"
    b = tmp_path / "catholic.csv"
    pd.DataFrame(EPSB_ROWS if epsb is None else epsb).to_csv(a, index=False)
    pd.DataFrame(ECSD_ROWS if ecsd is None else ecsd).to_csv(b, index=False)
    return a, b


def test_harmonizes_both_boards_and_drops_city_wide_programs(tmp_path):
    schools = load_schools(*_write(tmp_path))
    assert list(schools.columns) == ["school_name", "board", "latitude", "longitude"]
    assert set(schools["school_name"]) == {"Allendale", "Steele Heights", "St. Joseph"}
    assert schools["board"].value_counts().to_dict() == {"EPSB": 2, "ECSD": 1}


def test_unknown_category_is_kept_not_dropped(tmp_path, caplog):
    """A new school type must not vanish from the amenity set (no silent drops)."""
    epsb = EPSB_ROWS + [
        {"school_nam": "Brand New", "sch_type": "XX", "latitude": 53.55, "longitude": -113.49}
    ]
    with caplog.at_level(logging.WARNING):
        schools = load_schools(*_write(tmp_path, epsb=epsb))
    assert "Brand New" in set(schools["school_name"])
    assert "XX" in caplog.text


def test_null_coordinates_are_dropped_and_reported(tmp_path, caplog):
    epsb = EPSB_ROWS + [
        {"school_nam": "No Location", "sch_type": "EL", "latitude": None, "longitude": None}
    ]
    with caplog.at_level(logging.WARNING):
        schools = load_schools(*_write(tmp_path, epsb=epsb))
    assert "No Location" not in set(schools["school_name"])
    assert "null coordinates" in caplog.text


def test_swapped_lat_long_raises(tmp_path):
    """The failure a distance column would otherwise absorb into plausible metres."""
    epsb = [{"school_nam": "Swapped", "sch_type": "EL", "latitude": -113.5, "longitude": 53.5}]
    with pytest.raises(ValueError, match="outside the Edmonton bbox"):
        load_schools(*_write(tmp_path, epsb=epsb))


def test_missing_column_raises_with_headers(tmp_path):
    epsb = [{"school_nam": "Wrong Schema", "latitude": 53.5, "longitude": -113.5}]
    with pytest.raises(ValueError, match="sch_type"):
        load_schools(*_write(tmp_path, epsb=epsb))


def test_all_excluded_raises(tmp_path):
    with pytest.raises(ValueError, match="no catchment schools"):
        load_schools(*_write(
            tmp_path,
            epsb=[{"school_nam": "L. S. on Whyte", "sch_type": "SP",
                   "latitude": 53.517, "longitude": -113.51}],
            ecsd=[{"school_name": "CCAC-Clareview", "grade_level": "Outreach",
                   "latitude": 53.601, "longitude": -113.41}],
        ))
