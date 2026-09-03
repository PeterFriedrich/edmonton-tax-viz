"""Tests for the value-anchor cardinality guard (scripts/check_value_anchors.py).

The guard exists to notice a *regime* change in the record-to-parcel data, so
the tests that matter are the ones proving it TRIPS: a synthetic
duplicated-parcel regime (the condo bug arriving for real) and a synthetic
needle (the WEM bug arriving for real) must both push their anchor out of band
in the dangerous direction. A guard that only ever passes is decoration.
"""

import json
import os
import sys
from datetime import datetime, timedelta, timezone
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
    report_raw_vintage,
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


# --- the COMMITTED baseline itself -------------------------------------------
# Nothing above pins data/expected_value_anchors.json; these do. Every value is
# a reading scripts/check_value_anchors.py logged in CI against a FRESH
# download_data.py pull -- the only readings that gate a publish.
#
# ⚠️ RE-HARVESTED 2026-09-03, AND THE OLD TABLE HAD AN INTERPOLATED ROW. Its
# "2026-08-03" entry (56/58/60 -> the 58; 0.00517/0.00575/0.00633 -> the
# 0.00575) matched NO run: all five of its values were midpoints of the rows
# either side, lot_needle_ratio 12.82175 exactly. The 08-01..08-05 window has
# six runs and only TWO distinct data states -- 08-03 had two runs, one in each
# state, and the step between them happened between 05:17 and 11:19 that day.
# That invented middle point is what turned a SINGLE STEP into an apparent
# monotone three-point trend, which then drove the _ineligible_pair note, a
# TODO item, and a band re-pin. A trend needs three real observations.
#
# Each key below is the FIRST run of a distinct state; runs listed after it read
# identically. Harvested with `gh run view <id> --log | grep 'INFO:   '`.
OBSERVED_IN_CI = {
    # 08-01, 08-02, 08-03 05:17
    "2026-08-01": {"dedupe_effect_pct": 0.0408139, "dup_parcel_points": 33,
                   "dup_parcel_value_frac": 0.00309689, "ineligible_points": 56,
                   "ineligible_value_frac": 0.00517178, "lot_needle_ratio": 12.822},
    # 08-03 11:19, 08-04, 08-05 -- the excursion, and it reverted by 08-10
    "2026-08-03T11:19": {"dedupe_effect_pct": 0.0408168, "dup_parcel_points": 33,
                   "dup_parcel_value_frac": 0.00309363, "ineligible_points": 60,
                   "ineligible_value_frac": 0.00632732, "lot_needle_ratio": 12.8215},
    "2026-08-10": {"dedupe_effect_pct": 0.040806, "dup_parcel_points": 33,
                   "dup_parcel_value_frac": 0.00309363, "ineligible_points": 56,
                   "ineligible_value_frac": 0.00516634, "lot_needle_ratio": 12.8217},
    # 08-17, 08-19, 08-23, 08-24
    "2026-08-17": {"dedupe_effect_pct": 0.040825, "dup_parcel_points": 33,
                   "dup_parcel_value_frac": 0.00309435, "ineligible_points": 57,
                   "ineligible_value_frac": 0.00516946, "lot_needle_ratio": 12.8208},
    "2026-08-25": {"dedupe_effect_pct": 0.0408245, "dup_parcel_points": 33,
                   "dup_parcel_value_frac": 0.00309429, "ineligible_points": 57,
                   "ineligible_value_frac": 0.00515087, "lot_needle_ratio": 12.8209},
    "2026-08-31": {"dedupe_effect_pct": 0.0408324, "dup_parcel_points": 33,
                   "dup_parcel_value_frac": 0.00309473, "ineligible_points": 57,
                   "ineligible_value_frac": 0.00515159, "lot_needle_ratio": 12.8202},
    # 09-02: first run on the 50 m grid + MULTI_UNIT_MIN_LOT_M2, hence the needle
    "2026-09-02": {"dedupe_effect_pct": 0.0408324, "dup_parcel_points": 33,
                   "dup_parcel_value_frac": 0.00309473, "ineligible_points": 58,
                   "ineligible_value_frac": 0.00515519, "lot_needle_ratio": 13.9252},
}


def _committed_baseline():
    return json.loads((ROOT / "data" / "expected_value_anchors.json").read_text())


def test_committed_bands_accept_every_reading_the_guard_has_logged():
    """The bands were tightened 2026-08-05; no past CI reading may fall outside.

    A band that rejects a value the pipeline has already produced is a band that
    would have failed the weekly publish retroactively.
    """
    base = _committed_baseline()
    for date, live in OBSERVED_IN_CI.items():
        result, detail = compare_to_baseline(live, base)
        assert result == "ok", f"{date} would fail: {detail}"


def test_every_band_is_centred_on_a_reading_ci_actually_produced():
    """⚠️ The test that would have caught the 2026-09-02 re-pin.

    Nothing pinned a band's CENTRE, only its width -- so ineligible_points was
    re-centred on 85, a number read from a stale local data/raw/ that CI never
    produced (it read 58 the same day), and the ceiling went 84 -> 127.5 in the
    guard's own dangerous direction. Widths were guarded; provenance was not.

    Re-pinning stays easy and stays honest: move a centre, and add the CI run
    that justifies it to OBSERVED_IN_CI in the same commit.
    """
    base = _committed_baseline()
    observed = {k: [r[k] for r in OBSERVED_IN_CI.values()] for k in DANGER}
    for key, values in observed.items():
        b = base[key]
        centre = (b["min"] + b["max"]) / 2
        lo, hi = min(values), max(values)
        # Bands are written rounded to 6 dp, so a hair of slack at the edges.
        assert lo * (1 - 1e-3) <= centre <= hi * (1 + 1e-3), (
            f"{key} band is centred on {centre:g}, outside every reading CI has "
            f"logged ({lo:g}-{hi:g}). Either the centre came from data the "
            f"pipeline never saw, or the run that justifies it is missing from "
            f"OBSERVED_IN_CI."
        )


def test_the_ineligible_pair_was_left_wide_on_purpose():
    """⚠️ Pins the deliberate asymmetry, so 'finishing the job' fails here.

    ⚠️ The ORIGINAL reason is dead: the pair was thought to be drifting upward
    monotonically (56->58->60; 0.00517->0.00575->0.00633), and that was
    falsified 2026-09-03 -- it reverted on 2026-08-10 and has been flat since.
    The ±50% still stands on the OTHER reason, which never depended on the
    trend: ±25% is earned by flatness across a JANUARY YEAR-ROLL and no such
    observation exists yet (_why_only_25_percent).

    ⚠️ Pins the WIDTH, not the endpoints. Endpoints move on every legitimate
    re-pin -- 2026-09-02 re-centred ineligible_points on 85, 2026-09-03 put it
    back on 58 when that 85 turned out to be stale local data. ±50% is the
    invariant.
    """
    base = _committed_baseline()
    for key in ("ineligible_points", "ineligible_value_frac"):
        b = base[key]
        centre = (b["min"] + b["max"]) / 2
        half_width = (b["max"] - b["min"]) / 2 / centre
        assert half_width == pytest.approx(0.50, abs=0.01), (
            f"{key} half-width is {half_width:.3f}, expected 0.50 -- see "
            "_ineligible_pair_was_NOT_drifting in the baseline before re-tightening it"
        )


def test_lot_needle_was_widened_when_one_cell_started_setting_it():
    """⚠️ Pins the 2026-09-01 re-pin, so re-tightening fails here.

    Was one of the four +/-25% frozen anchors. The 50 m Glass grid moved it
    12 -> 79 -- resolution, not data: halving the cell stopped diluting three
    WESTMOUNT condo records whose lot_size holds ownership shares rather than
    m². Its value is now set by ONE degenerate record, so the flatness that
    earned the +/-25% no longer describes it, and tightening would red the
    weekly publish on a single upstream edit. Revisit only after the sub-1 m²
    lot_size defect is fixed (docs/DATA_ISSUES.md §E).
    """
    base = _committed_baseline()
    b = base["lot_needle_ratio"]
    centre = (b["min"] + b["max"]) / 2
    half_width = (b["max"] - b["min"]) / 2 / centre
    assert half_width == pytest.approx(0.50, abs=0.01), (
        f"lot_needle_ratio half-width is {half_width:.3f}, expected 0.50 -- see "
        "_lot_needle_is_now_one_cell in the baseline before re-tightening it"
    )


def test_tightened_anchors_are_actually_tighter_than_the_old_uniform_band():
    """The three still-frozen anchors must stay at +/-25%, not drift back to
    +/-50%.

    ``--write-baseline`` applies ONE global --tolerance to every anchor and
    would silently flatten the split this file now encodes. ⚠️
    ``lot_needle_ratio`` was a fourth member until 2026-09-01 -- see the test
    above for why it left, and do not add it back without re-measuring.
    """
    base = _committed_baseline()
    for key in ("dup_parcel_points", "dup_parcel_value_frac",
                "dedupe_effect_pct"):
        b = base[key]
        centre = (b["min"] + b["max"]) / 2
        half_width = (b["max"] - b["min"]) / 2 / centre
        assert half_width == pytest.approx(0.25, abs=0.01), (
            f"{key} half-width is {half_width:.3f}, expected 0.25"
        )


# --- report_raw_vintage: the stale-local-data trap ----------------------------
#
# ⚠️ Falsified against the real 2026-09-02 incident: a 2026-07-06 property-info
# file beside a 2026-08-09 assessment file read ineligible_points 85 where CI,
# same code and same day, read 58. Nothing in the guard's output said so.

def _aged(tmp_path, name, days_old, now):
    p = tmp_path / name
    p.write_text("x")
    when = (now - timedelta(days=days_old)).timestamp()
    os.utime(p, (when, when))
    return p


def test_fresh_matched_raw_produces_no_warning(tmp_path):
    now = datetime(2026, 9, 3, tzinfo=timezone.utc)
    paths = {"assessment": _aged(tmp_path, "a.csv", 1, now),
             "property-info": _aged(tmp_path, "p.csv", 1, now)}
    assert report_raw_vintage(paths, now=now) == []


def test_stale_raw_is_reported(tmp_path):
    now = datetime(2026, 9, 3, tzinfo=timezone.utc)
    paths = {"assessment": _aged(tmp_path, "a.csv", 40, now),
             "property-info": _aged(tmp_path, "p.csv", 40, now)}
    warnings = report_raw_vintage(paths, now=now)
    assert any("STALE" in w for w in warnings)


def test_the_actual_2026_09_02_snapshot_is_flagged_both_ways(tmp_path):
    """The exact pair that produced the phantom 85 must trip both checks."""
    now = datetime(2026, 9, 2, tzinfo=timezone.utc)
    paths = {  # 2026-08-09 assessment, 2026-07-06 property-info
        "assessment": _aged(tmp_path, "a.csv", 24, now),
        "property-info": _aged(tmp_path, "p.csv", 58, now),
    }
    warnings = report_raw_vintage(paths, now=now)
    assert any("STALE" in w for w in warnings)
    assert any("MISMATCHED" in w for w in warnings)


def test_a_fresh_but_mismatched_pair_is_still_flagged(tmp_path):
    """⚠️ The dangerous case the staleness check alone MISSES.

    A fresh roll joined to a property-info file from an earlier pull is exactly
    what distorts the ineligible_* anchors, and both files can be recent.
    """
    now = datetime(2026, 9, 3, tzinfo=timezone.utc)
    paths = {"assessment": _aged(tmp_path, "a.csv", 0, now),
             "property-info": _aged(tmp_path, "p.csv", 9, now)}
    warnings = report_raw_vintage(paths, now=now)
    assert not any("STALE" in w for w in warnings)
    assert any("MISMATCHED" in w for w in warnings)
