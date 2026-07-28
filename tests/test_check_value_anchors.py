"""Tests for the value-anchor cardinality guard (scripts/check_value_anchors.py).

The guard exists to notice a *regime* change in the record-to-parcel data, so
the tests that matter are the ones proving it TRIPS: a synthetic
duplicated-parcel regime (the condo bug arriving for real) and a synthetic
needle (the WEM bug arriving for real) must both push their anchor out of band
in the dangerous direction. A guard that only ever passes is decoration.
"""

import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

from check_value_anchors import (  # noqa: E402
    DANGER,
    compare_to_baseline,
    compute_anchors,
    compute_needle_ratio,
)


def _frame(rows):
    """rows: (lat, lon, value, lot_size) — lot_size None for null."""
    return pd.DataFrame(rows, columns=["latitude", "longitude", "assessed_value", "lot_size"])


# --- compute_anchors: the duplicated-parcel regime (the primary canary) -------

def test_clean_data_has_no_duplicated_parcel_regime():
    # Distinct single-account parcels: nothing repeats, so the dedupe branch
    # the guard watches is doing no work.
    df = _frame([(1.0, 1.0, 100.0, 500.0), (2.0, 2.0, 200.0, 5000.0)])
    a = compute_anchors(df)
    assert a["dup_parcel_points"] == 0
    assert a["dup_parcel_value_frac"] == 0
    assert a["dedupe_effect_pct"] == 0


def test_apportioned_shares_are_not_counted_as_duplication():
    # Four townhouse units each carrying an identical 200 m2 share: legitimate
    # per-unit land (< SHARE_MAX_M2), NOT a duplicated parcel. This is the
    # FINDINGS_lot_dedupe 4.3 townhouse case the rule was revised for.
    df = _frame([(1.0, 1.0, 50.0, 200.0)] * 4)
    a = compute_anchors(df)
    assert a["dup_parcel_points"] == 0
    assert a["dedupe_effect_pct"] == 0


def test_duplicated_parcel_regime_is_detected():
    # Four condo units each carrying the WHOLE 5000 m2 lot — the actual Bug 2
    # shape. One point flagged, and raw summing overcounts area 4x.
    df = _frame([(1.0, 1.0, 50.0, 5000.0)] * 4)
    a = compute_anchors(df)
    assert a["dup_parcel_points"] == 1
    assert a["dup_parcel_value_frac"] == pytest.approx(1.0)
    # raw 20000 m2 vs deduped 5000 m2 = 300% overcount
    assert a["dedupe_effect_pct"] == pytest.approx(300.0)


def test_majority_null_point_counted_ineligible():
    # 3 of 4 units null -> point drops out of the lot-acre metric entirely.
    df = _frame([
        (1.0, 1.0, 25.0, 400.0), (1.0, 1.0, 25.0, None),
        (1.0, 1.0, 25.0, None), (1.0, 1.0, 25.0, None),
    ])
    a = compute_anchors(df)
    assert a["ineligible_points"] == 1
    assert a["ineligible_value_frac"] == pytest.approx(1.0)


def test_zero_lot_size_treated_as_null_not_as_area():
    df = _frame([(1.0, 1.0, 10.0, 0.0), (2.0, 2.0, 10.0, 800.0)])
    a = compute_anchors(df)
    # The zero-lot point has no usable value -> ineligible, not a 0 m2 parcel.
    assert a["ineligible_points"] == 1


# --- compute_needle_ratio: cell grain, from the exported artifact -------------

def _grid(values):
    return {"columns": ["lon", "lat", "value_per_lot_acre"],
            "cells": [[0.0, 0.0, v] for v in values]}


def test_needle_ratio_is_near_one_for_a_flat_distribution():
    assert compute_needle_ratio(_grid([100.0] * 1000)) == pytest.approx(1.0)


def test_needle_ratio_spikes_when_one_cell_towers():
    # 999 ordinary cells and one 100x needle — the failure mode itself.
    ratio = compute_needle_ratio(_grid([100.0] * 999 + [10_000.0]))
    assert ratio > 50


def test_needle_ratio_ignores_null_cells():
    grid = {"columns": ["lon", "lat", "value_per_lot_acre"],
            "cells": [[0.0, 0.0, None], [0.0, 0.0, 100.0], [0.0, 0.0, 200.0]]}
    # Nulls must be filtered BEFORE the sort — leaving them in raises TypeError
    # on None-vs-float in py3, so reaching a number at all proves the filter.
    assert compute_needle_ratio(grid) == pytest.approx(1.0, rel=0.01)


def test_needle_ratio_raises_when_no_cells_carry_the_column():
    with pytest.raises(ValueError, match="no non-null"):
        compute_needle_ratio(_grid([None, None]))


# --- compare_to_baseline: direction-aware banding -----------------------------

BASE = {k: {"min": 1.0, "max": 10.0} for k in DANGER}


def test_in_band_is_ok():
    result, detail = compare_to_baseline({"ineligible_points": 5.0}, BASE)
    assert result == "ok"
    assert detail["ineligible_points"]["status"] == "ok"


def test_above_band_on_a_high_danger_anchor_fails():
    result, detail = compare_to_baseline({"ineligible_points": 50.0}, BASE)
    assert result == "drift"
    assert detail["ineligible_points"]["status"] == "drift"


def test_below_band_on_a_high_danger_anchor_is_benign_not_a_failure():
    # Fewer excluded points is good news: warn and ask for a re-pin, never red
    # the weekly refresh (the check_unmatched_names policy).
    result, detail = compare_to_baseline({"ineligible_points": 0.0}, BASE)
    assert result == "ok"
    assert detail["ineligible_points"]["status"] == "benign"


def test_anchor_with_no_declared_direction_never_hard_fails():
    # An anchor absent from DANGER has no "bad" side, so neither edge reds the
    # build. The coverage test below is what stops one being added by mistake.
    for value in (0.1, 99.0):
        result, detail = compare_to_baseline(
            {"undeclared": value}, {"undeclared": {"min": 1.0, "max": 10.0}}
        )
        assert detail["undeclared"]["status"] == "benign"
        assert result == "ok"


def test_unpinned_anchor_is_reported_not_silently_ignored():
    result, detail = compare_to_baseline({"brand_new_anchor": 3.0}, {})
    assert detail["brand_new_anchor"]["status"] == "unpinned"
    assert result == "ok"


def test_every_anchor_the_guard_computes_has_a_declared_danger_direction():
    # Guards against adding an anchor and forgetting to say which way is bad —
    # it would then be pinned but could never fail.
    df = _frame([(1.0, 1.0, 10.0, 500.0)])
    computed = set(compute_anchors(df)) | {"lot_needle_ratio"}
    assert computed == set(DANGER)
