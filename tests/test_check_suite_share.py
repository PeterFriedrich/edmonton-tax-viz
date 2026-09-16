"""Fixture coverage for the suite-share guard.

The guard itself runs in the refresh workflow, because it re-derives from
``data/raw/building_permits.csv`` and that file is gitignored. These tests are
what keeps its LOGIC covered in CI: they build a tiny permits frame whose share
is known by construction, so a regression in the arithmetic or the copy match
fails here rather than waiting for a weekly refresh.

⚠️ The fixture's share is deliberately **not** the shipped 0.9%. A fixture that
happens to agree with production passes when the guard is comparing the wrong
two things — the failure this project keeps catching (`check-where-the-value-
can-be-wrong`). 3 suite units against 97 new units is 3.0%, which no real
window produces.
"""
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, "scripts")
from check_suite_share import main, stated_share, suite_share  # noqa: E402

YEARS = (2021, 2022)

# 3 suite units / 100 new units -> 3.0%, a value production never shows.
ROWS = [
    ("(01) New", 2021, 60),
    ("(01) New House", 2022, 40),
    ("(07) Add Suites to Single Dwelling", 2021, 1),
    ("(08) Add Suites to Multi-Dwelling", 2022, 1),
    ("(09) Convert Non-Res to Residential", 2022, 1),
    # Out of window on both sides: must not reach either half of the ratio.
    ("(01) New", 2019, 500),
    ("(09) Convert Non-Res to Residential", 2019, 500),
    # In window but neither new nor a suite conversion: excluded from both.
    ("(99) Demolition", 2021, 7),
]


@pytest.fixture
def permits():
    return pd.DataFrame(ROWS, columns=["work_type", "year", "units_added"])


def _page(text):
    return f"<html><body><p>{text}</p></body></html>"


def test_share_is_suite_units_over_new_units_in_window(permits):
    share, suite_units, lens_a, rows = suite_share(permits, YEARS)
    assert (suite_units, lens_a, rows) == (3, 100, 3)
    assert share == pytest.approx(3.0)


def test_out_of_window_rows_reach_neither_half(permits):
    """The 2019 rows are 500 units on each side — a leak would be unmissable."""
    share, _, lens_a, _ = suite_share(permits, YEARS)
    assert lens_a == 100, "Lens A denominator picked up an out-of-window row"
    assert share == pytest.approx(3.0)


def test_non_new_non_suite_rows_are_excluded(permits):
    """Demolition is in-window and must not inflate the denominator."""
    _, _, lens_a, _ = suite_share(permits, YEARS)
    assert lens_a == 100


def test_renamed_work_type_fails_rather_than_shrinking_the_share(permits):
    """A vocabulary rename must not silently drop a code from the numerator.

    This is the direction that matters: an unrecognised (09) spelling would
    quietly shrink the disclosed share, making the exclusion look MORE
    defensible than it is.
    """
    permits.loc[permits["work_type"].str.startswith("(09)"), "work_type"] = "(09) Convert NonRes"
    with pytest.raises(SystemExit, match="vocabulary"):
        suite_share(permits, YEARS)


def test_zero_denominator_refuses_to_divide(permits):
    with pytest.raises(SystemExit, match="Lens A numerator is zero"):
        suite_share(permits, (1999,))


def test_stated_share_reads_the_copy():
    assert stated_share(_page("conversions (~0.9% of units 2021-25) are excluded")) == 0.9
    assert stated_share(_page("no disclosure here")) is None


def test_stated_share_ignores_comments():
    """The haystack is reader-visible text — the V1 vacuous-guard lesson.

    A comment carrying the right number must not satisfy the guard while the
    visible copy says something else.
    """
    page = "<html><body><!-- ~0.9% of units --><p>nothing visible</p></body></html>"
    assert stated_share(page) is None


def _run(tmp_path, permits, copy_text):
    html = tmp_path / "index.html"
    html.write_text(_page(copy_text))
    csv = tmp_path / "permits.csv"
    permits.to_csv(csv, index=False)
    return main(["--html", str(html), "--permits", str(csv),
                 "--years", *[str(y) for y in YEARS]])


def test_matching_copy_passes(tmp_path, permits):
    assert _run(tmp_path, permits, "conversions (~3.0% of units) are excluded") == 0


def test_drifted_copy_fails(tmp_path, permits):
    assert _run(tmp_path, permits, "conversions (~0.9% of units) are excluded") == 5


def test_removed_disclosure_fails(tmp_path, permits):
    assert _run(tmp_path, permits, "new construction only.") == 5


def test_missing_input_fails_rather_than_passing_quietly(tmp_path, permits):
    """⚠️ The vacuous direction. Absent data must never read as 'ok'."""
    html = tmp_path / "index.html"
    html.write_text(_page("conversions (~3.0% of units) are excluded"))
    assert main(["--html", str(html), "--permits", str(tmp_path / "nope.csv")]) == 4
