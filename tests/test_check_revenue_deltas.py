"""Tests for scripts/check_revenue_deltas.py (the per-hood magnitude guard).

Two things need proving, and the second is the one that decides whether anyone
keeps the guard switched on:

  1. it TRIPS on the event it was built for — the real 2026-08-03 refresh, where
     WEST MEADOWLARK PARK went $4.63M -> $10.63M on a green run.
  2. it stays SILENT on the legitimate churn in the same file's history —
     especially ALCES (+12.7% but only +$501K), the case that forces the
     threshold to be a percentage AND a dollar amount rather than either alone.

A guard that fires on ordinary reassessment noise reds the weekly publish on
good data and gets turned off, so (2) is not a nicety.

⚠️ Everything here must ALSO confirm exit 0. This guard warns and never blocks;
a version of it that fails the publish would take the site's weekly refresh down
on a legitimate parcel completion.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from check_revenue_deltas import (  # noqa: E402
    EXIT_OK,
    MIN_ABS_DOLLARS,
    MIN_PCT,
    biggest_frac_shift,
    compare,
    main,
    render,
)


def _hood(name, revenue, **frac):
    props = {"neighbourhood_name": name, "total_revenue": revenue}
    props.update(frac)
    return {"type": "Feature", "geometry": None, "properties": props}


def _served(features):
    return {"type": "FeatureCollection", "features": features}


def _as_map(features):
    return {f["properties"]["neighbourhood_name"]: f["properties"] for f in features}


def _write(tmp_path, name, features):
    p = tmp_path / name
    p.write_text(json.dumps(_served(features)))
    return p


# --- the event the guard exists for -----------------------------------------


def test_trips_on_the_west_meadowlark_shape():
    """+130% and +$6.0M — both thresholds cleared, the real 2026-08-03 numbers."""
    before = _as_map([_hood("WEST MEADOWLARK PARK", 4_626_512.39)])
    after = _as_map([_hood("WEST MEADOWLARK PARK", 10_628_474.66)])
    flagged, appeared, disappeared = compare(before, after)
    assert [r["name"] for r in flagged] == ["WEST MEADOWLARK PARK"]
    assert round(flagged[0]["pct"], 1) == 129.7
    assert round(flagged[0]["delta"]) == 6_001_962
    assert not appeared and not disappeared


def test_reports_the_revenue_mix_fingerprint():
    """rev_frac_inst 0.059 -> 0.590 is what identified the cause in minutes."""
    before = _as_map([_hood("H", 4_626_512, rev_frac_inst=0.0589, rev_frac_residential=0.5667)])
    after = _as_map([_hood("H", 10_628_475, rev_frac_inst=0.5903, rev_frac_residential=0.2467)])
    flagged, _, _ = compare(before, after)
    key, old, new = flagged[0]["frac_shift"]
    assert key == "rev_frac_inst"
    assert round(old, 3) == 0.059 and round(new, 3) == 0.590
    assert "rev_frac_inst" in render(flagged, [], [], 1)


# --- the false positives that would get it switched off ---------------------


def test_silent_on_alces_big_percent_small_dollars():
    """+12.7% on +$501K — real 2026-07-27 churn in a small edge neighbourhood.

    This is the whole reason the dollar condition exists. A percentage-only
    guard fires here, on a legitimate handful of completed houses.
    """
    before = _as_map([_hood("ALCES", 3_947_000)])
    after = _as_map([_hood("ALCES", 4_448_317)])
    flagged, _, _ = compare(before, after)
    assert flagged == []


def test_silent_on_big_dollars_small_percent():
    """The other half: a huge hood drifting 1% is not an event."""
    before = _as_map([_hood("BIG", 300_000_000)])
    after = _as_map([_hood("BIG", 303_000_000)])   # +$3M but only +1%
    flagged, _, _ = compare(before, after)
    assert flagged == []


def test_both_conditions_are_required_not_either():
    """Pins the AND. Flipping it to OR passes the two tests above only by luck."""
    assert compare(_as_map([_hood("A", 100.0)]),
                   _as_map([_hood("A", 1_000_000.0)]))[0] == []      # % yes, $ no
    assert compare(_as_map([_hood("B", 1e9)]),
                   _as_map([_hood("B", 1e9 + 5e6)]))[0] == []        # $ yes, % no
    assert compare(_as_map([_hood("C", 5e6)]),
                   _as_map([_hood("C", 1.1e7)]))[0] != []            # both


# --- membership, and the arithmetic edges -----------------------------------


def test_appearing_and_disappearing_hoods_are_reported():
    before = _as_map([_hood("STAYS", 1.0), _hood("GONE", 1.0)])
    after = _as_map([_hood("STAYS", 1.0), _hood("NEW", 1.0)])
    flagged, appeared, disappeared = compare(before, after)
    assert appeared == ["NEW"] and disappeared == ["GONE"] and flagged == []


def test_zero_and_missing_baselines_do_not_divide_by_zero():
    before = _as_map([_hood("ZERO", 0.0), _hood("NULL", None), _hood("OK", 5e6)])
    after = _as_map([_hood("ZERO", 9e6), _hood("NULL", 9e6), _hood("OK", 1.1e7)])
    flagged, _, _ = compare(before, after)
    assert [r["name"] for r in flagged] == ["OK"]


def test_a_drop_is_flagged_too_not_just_a_rise():
    """Value LEAVING a hood is the same defect wearing the other sign."""
    before = _as_map([_hood("H", 10_628_475.0)])
    after = _as_map([_hood("H", 4_626_512.0)])
    flagged, _, _ = compare(before, after)
    assert flagged[0]["pct"] < 0 and flagged[0]["delta"] < 0


def test_uniform_scaling_reports_no_mix_shift():
    """No rev_frac_* move means a rate change, not a parcel event — say so."""
    before = _as_map([_hood("H", 5e6, rev_frac_inst=0.10, rev_frac_residential=0.90)])
    after = _as_map([_hood("H", 1.1e7, rev_frac_inst=0.10, rev_frac_residential=0.90)])
    flagged, _, _ = compare(before, after)
    assert "unchanged" in render(flagged, [], [], 1)


def test_biggest_frac_shift_ignores_non_frac_columns():
    shift = biggest_frac_shift(
        {"rev_frac_inst": 0.1, "revenue_per_acre": 1.0},
        {"rev_frac_inst": 0.2, "revenue_per_acre": 9999.0},
    )
    assert shift[0] == "rev_frac_inst"


# --- exit behaviour: this guard must never stop a publish -------------------


def test_exit_is_zero_even_when_flagged(tmp_path, caplog):
    before = _write(tmp_path, "before.geojson", [_hood("H", 4_626_512)])
    after = _write(tmp_path, "after.geojson", [_hood("H", 10_628_475)])
    report = tmp_path / "report.md"
    with caplog.at_level("WARNING"):
        code = main(["--before", str(before), "--after", str(after), "--report", str(report)])
    assert code == EXIT_OK
    assert "BIG REVENUE DELTA" in caplog.text
    assert "129.7" in report.read_text()


def test_exit_is_zero_when_clean(tmp_path):
    before = _write(tmp_path, "before.geojson", [_hood("H", 5_000_000)])
    after = _write(tmp_path, "after.geojson", [_hood("H", 5_010_000)])
    assert main(["--before", str(before), "--after", str(after)]) == EXIT_OK


def test_missing_served_file_is_not_an_error(tmp_path):
    """The steps above already fail hard on this; here it must stay quiet."""
    before = _write(tmp_path, "before.geojson", [_hood("H", 5e6)])
    assert main(["--before", str(before),
                 "--after", str(tmp_path / "nope.geojson")]) == EXIT_OK


def test_thresholds_are_the_measured_pair():
    """Pins the documented values so a casual 'tighten it' shows up in review."""
    assert (MIN_PCT, MIN_ABS_DOLLARS) == (10.0, 1_000_000.0)
