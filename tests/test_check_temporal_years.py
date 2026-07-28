"""Tests for the temporal-year guard (scripts/check_temporal_years.py).

The defect this guard watches for arrived silently and survived two publication
cycles, so the tests that matter are the ones proving it TRIPS. Each structural
check gets a synthetic version of the failure it exists to catch; a guard that
only ever passes is decoration.
"""

import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.check_temporal_years import (  # noqa: E402
    LIVE_GROWTH_MIN,
    check_live_growth,
    compare_years,
    structural_checks,
    year_anchors,
)
from src.load_temporal import build_temporal_table  # noqa: E402


def _long(rows):
    return pd.DataFrame(
        rows, columns=["year", "neighbourhood_name", "mill_class", "n_accounts", "assessed_value"]
    )


def _fixture(live_year=2025, live_n=12):
    """History 2022-2024 + a live roll; 2024 is defective so it drops out."""
    hist = _long([
        (y, h, "RESIDENTIAL", 10, 1000.0)
        for y in (2022, 2023, 2024, 2025)
        for h in ("ALPHA", "BETA")
    ])
    cur = _long([
        (live_year, "ALPHA", "RESIDENTIAL", live_n, 1200.0),
        (live_year, "BETA", "RESIDENTIAL", live_n, 1200.0),
    ])
    table, _ = build_temporal_table(hist, cur, live_year)
    return table, hist


# --- the happy path ----------------------------------------------------------

def test_a_correct_table_passes_every_structural_check():
    table, hist = _fixture()
    assert structural_checks(table, hist, 2025, first_year=2022) == []


# --- years: the decision must hold -------------------------------------------

def test_republishing_an_omitted_year_trips():
    """Someone 'fixes' the gap — the exact thing the omission decision forbids."""
    hist = _long([
        (y, "ALPHA", "RESIDENTIAL", 10, 1000.0) for y in (2022, 2023, 2024, 2025)
    ])
    cur = _long([(2025, "ALPHA", "RESIDENTIAL", 12, 1200.0)])
    table, _ = build_temporal_table(hist, cur, 2025, defect_years=())
    failures = structural_checks(table, hist, 2025, first_year=2022)
    assert any("UNEXPECTEDLY PRESENT" in f and "2024" in f for f in failures)


def test_a_missing_year_trips():
    table, hist = _fixture()
    failures = structural_checks(table[table["year"] != 2022], hist, 2025, first_year=2022)
    assert any(f.startswith("years:") and "missing" in f for f in failures)


# --- splice ------------------------------------------------------------------

def test_live_year_sourced_from_history_trips():
    table, hist = _fixture()
    bad = table.copy()
    bad.loc[bad["year"] == 2025, "source"] = "historical"
    assert any("must come from the current roll" in f for f in structural_checks(bad, hist, 2025, first_year=2022))


def test_splice_the_wrong_way_round_trips():
    """The historical copy is the defective one, so it must hold FEWER accounts."""
    table, hist = _fixture(live_n=1)  # roll now smaller than the historical slice
    assert any("the splice may be the wrong way round" in f
               for f in structural_checks(table, hist, 2025, first_year=2022))


# --- conservation ------------------------------------------------------------

def test_a_dropped_hood_trips_the_share_conservation_check():
    table, hist = _fixture()
    failures = structural_checks(table[table["neighbourhood_name"] != "BETA"], hist, 2025, first_year=2022)
    assert any("value left the numerator" in f for f in failures)


def test_duplicate_hood_year_rows_trip():
    table, hist = _fixture()
    dupe = pd.concat([table, table.iloc[[0]]], ignore_index=True)
    assert any(f.startswith("unique:") for f in structural_checks(dupe, hist, 2025, first_year=2022))


# --- live growth -------------------------------------------------------------

def test_a_shrinking_live_year_trips():
    """The dropout signature: the roll stops growing."""
    table, _ = _fixture(live_n=2)  # 20 -> 4 accounts
    failures = check_live_growth(table, 2025)
    assert any("live-growth" in f for f in failures)


def test_normal_growth_passes():
    table, _ = _fixture(live_n=12)
    assert check_live_growth(table, 2025) == []


def test_growth_floor_sits_below_the_observed_minimum():
    # The real series' smallest year-over-year growth is +0.28% (2024, the
    # defect year itself). The floor must sit below that or every year fails.
    assert LIVE_GROWTH_MIN < 0.0028


# --- baseline comparison -----------------------------------------------------

def _anchors(table):
    return year_anchors(table)


def test_a_settled_year_losing_accounts_is_the_dangerous_direction():
    table, _ = _fixture()
    live = _anchors(table)
    baseline = {"years": {"2022": {
        "n_accounts": {"min": 100.0, "max": 110.0},
        "total_assessed_value": {"min": 0.0, "max": 1e9},
    }}}
    result, dangerous, _ = compare_years(live, baseline, 2025)
    assert result == "drift"
    assert any("LOST" in d for d in dangerous)


def test_a_settled_year_gaining_warns_but_does_not_fail():
    table, _ = _fixture()
    live = _anchors(table)
    baseline = {"years": {"2022": {
        "n_accounts": {"min": 0.0, "max": 1.0},
        "total_assessed_value": {"min": 0.0, "max": 1.0},
    }}}
    result, dangerous, benign = compare_years(live, baseline, 2025)
    assert result == "ok"
    assert dangerous == []
    assert benign


def test_the_live_year_is_never_pinned():
    """It is a live snapshot that moves weekly; pinning it would cry wolf."""
    table, _ = _fixture()
    live = _anchors(table)
    baseline = {"years": {"2025": {
        "n_accounts": {"min": 1e9, "max": 2e9},
        "total_assessed_value": {"min": 1e9, "max": 2e9},
    }}}
    result, dangerous, _ = compare_years(live, baseline, 2025)
    assert result == "ok" and dangerous == []


def test_an_unpinned_year_warns_rather_than_failing():
    table, _ = _fixture()
    result, dangerous, benign = compare_years(_anchors(table), {"years": {}}, 2025)
    assert result == "ok"
    assert any("not pinned" in b for b in benign)


# --- the archive -------------------------------------------------------------

def _roll_forward_fixture():
    hist = _long([(y, "ALPHA", "RESIDENTIAL", 10, 1000.0) for y in (2023, 2025, 2026)])
    cur = _long([(2026, "ALPHA", "RESIDENTIAL", 14, 1400.0)])
    captured = _long([(2025, "ALPHA", "RESIDENTIAL", 12, 1200.0)])
    return hist, cur, captured


def test_an_archived_year_served_from_history_trips():
    """The January trap arriving: the capture exists but a defective slice won."""
    hist, cur, captured = _roll_forward_fixture()
    table, stats = build_temporal_table(hist, cur, 2026, archive=captured)
    bad = table.copy()
    bad.loc[bad["year"] == 2025, "source"] = "historical"
    failures = structural_checks(
        bad, hist, 2026, first_year=2023, archived_years=stats["archived_years"]
    )
    assert any("the captured copy is not being used" in f for f in failures)


def test_an_archived_year_dropped_from_the_table_trips():
    """The capture exists but the year vanished — the loss this all exists to stop."""
    hist, cur, _ = _roll_forward_fixture()
    table, _ = build_temporal_table(hist, cur, 2026, archive=None)  # capture ignored
    failures = structural_checks(
        table, hist, 2026, first_year=2023, archived_years=(2025,)
    )
    assert any(f.startswith("years:") and "2025" in f for f in failures)


def test_an_archived_year_counts_as_published():
    hist, cur, captured = _roll_forward_fixture()
    table, stats = build_temporal_table(hist, cur, 2026, archive=captured)
    failures = structural_checks(
        table, hist, 2026, first_year=2023, archived_years=stats["archived_years"]
    )
    assert failures == []
