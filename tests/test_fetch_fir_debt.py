"""Tests for scripts/fetch_fir_debt.py (FIR debt series extraction).

openpyxl/xlrd are dev-only deps (the fetch is a manual, reviewed step — not
part of the weekly refresh), so the whole module skips on CI where only
requirements-ci.txt is installed. The extraction core (_extract_rows) is
exercised on plain row tuples; no real workbook needed.
"""

import sys
from pathlib import Path

import pytest

pytest.importorskip("openpyxl")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import fetch_fir_debt as f  # noqa: E402

HDR = ("YEAR", "STATUS", "CODE", "MUNICIPALITY", "Debt Limit", "Total Debt",
       "Debt Service Limit", "Total Debt Service Costs")


def rows(*munis):
    """A minimal debt schedule: title row, header, then municipality rows."""
    return [("Schedule AA", None, None, None, None, None, None, None), HDR, *munis]


def edmonton(year=2024, debt=4_368_432_000):
    return (str(year), "City", "0098", "EDMONTON", 7_224_698_000, debt,
            1_264_322_000, 413_580_000)


def st_albert(year=2024):
    return (str(year), "City", "0292", "ST. ALBERT", 373_354_000, 97_628_505,
            62_226_000, 12_986_300)


def strathcona(year=2024, scale=1):
    return (str(year), "Specialized Municipality", "0302", "STRATHCONA COUNTY",
            707_454_437 // scale, 111_912_965 // scale, 117_909_073 // scale,
            13_959_975 // scale)


def test_extracts_all_three_municipalities():
    got = f._extract_rows(rows(edmonton(), st_albert(), strathcona()), 2024, "t")
    assert set(got) == {"0098", "0292", "0302"}
    assert got["0098"]["total_debt"] == 4_368_432_000
    assert got["0292"]["debt_limit"] == 373_354_000
    assert set(f.FIELDS) <= set(got["0302"])


def test_missing_municipality_hard_fails():
    with pytest.raises(SystemExit, match="STRATHCONA"):
        f._extract_rows(rows(edmonton(), st_albert()), 2024, "t")


def test_missing_column_hard_fails():
    bad_hdr = tuple(h if h != "Total Debt" else "Renamed" for h in HDR)
    with pytest.raises(SystemExit, match="Total Debt"):
        f._extract_rows([bad_hdr, edmonton()], 2024, "t")


def test_no_header_hard_fails():
    with pytest.raises(SystemExit, match="header"):
        f._extract_rows([("just", "noise")], 2024, "t")


def test_non_numeric_value_hard_fails():
    row = ("2024", "City", "0098", "EDMONTON", "n/a", 1, 1, 1)
    with pytest.raises(SystemExit, match="non-numeric"):
        f._extract_rows([HDR, row], 2024, "t")


def test_known_unit_correction_applied_and_recorded():
    got = f._extract_rows(rows(edmonton(2013), st_albert(2013),
                               strathcona(2013, scale=1000)), 2013, "t")
    assert got["0302"]["unit_corrected"] == 1000
    # back on the real-dollar scale (integer division in the fixture is <$1000 off)
    assert abs(got["0302"]["total_debt"] - 111_912_965) < 1000
    # other municipalities untouched
    assert "unit_corrected" not in got["0098"]


def test_legacy_xls_float_code_normalized():
    row = (2003.0, "City", "98.0", "EDMONTON", 2_125_774_000.0, 370_914_000.0,
           372_010_000.0, 63_961_000.0)
    got = f._extract_rows([HDR, row, st_albert(2003), strathcona(2003)], 2003, "t")
    assert got["0098"]["total_debt"] == 370_914_000


def _series_of(vals_by_year):
    years = {y: {fld: v for fld in f.FIELDS} for y, v in vals_by_year.items()}
    return {name: {"code": code, "years": years}
            for code, name in f.MUNICIPALITIES.items()}


def test_neighbour_sanity_catches_unit_slip():
    series = _series_of({2012: 470_000_000, 2013: 485_000, 2014: 500_000_000})
    with pytest.raises(SystemExit, match="sanity"):
        f.sanity_check_neighbours(series)


def test_neighbour_sanity_passes_smooth_series():
    series = _series_of({2012: 470_000_000, 2013: 485_000_000, 2014: 500_000_000})
    f.sanity_check_neighbours(series)  # no raise


def test_anchor_mismatch_fails_unless_allowed(caplog):
    series = _series_of({2022: 1, 2025: 2})
    with pytest.raises(SystemExit, match="anchor"):
        f.check_anchors(series, allow_drift=False)
    f.check_anchors(series, allow_drift=True)  # warns, no raise
    assert "anchor" in caplog.text
