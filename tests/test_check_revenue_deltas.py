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
import re
import subprocess
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


# --- the baseline itself: a fault must not read as "first publish" -----------
#
# ⚠️ Until 2026-09-08 `load_committed` returned None on ANY non-zero `git show`,
# so a bad --rev, a missing git, or a non-checkout all took the same exit path as
# a genuine first publish: exit 0, flagged=0, "nothing to compare against" — the
# guard reporting an all-clear over 406 neighbourhoods it never looked at.
# Both directions are pinned below, because the cheap way to pass the first test
# is to call everything a fault and cry wolf on every real first publish.


def _repo(tmp_path, monkeypatch, committed=True):
    """A real git checkout with the served file in it, as `ROOT` for the module.

    A real repo, not a stubbed subprocess: what is under test IS the git
    invocation and how its failures are classified, so stubbing it would assert
    the stub. Only the location moves.
    """
    import check_revenue_deltas as mod

    run = lambda *a: subprocess.run(  # noqa: E731
        ["git", *a], cwd=tmp_path, check=True, capture_output=True
    )
    run("init", "-q", "-b", "main")
    run("config", "user.email", "t@example.invalid")
    run("config", "user.name", "t")
    (tmp_path / "web" / "data").mkdir(parents=True)
    served = tmp_path / "web" / "data" / "neighbourhood_value_per_acre.geojson"
    served.write_text(json.dumps(_served([_hood("H", 5_000_000)])))
    (tmp_path / "README").write_text("x\n")
    run("add", "README" if not committed else ".")
    run("commit", "-qm", "baseline")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    return served


def _outputs(tmp_path, monkeypatch):
    out = tmp_path / "gh_output"
    out.write_text("")
    monkeypatch.setenv("GITHUB_OUTPUT", str(out))
    return lambda: dict(
        line.split("=", 1) for line in out.read_text().splitlines() if "=" in line
    )


def test_a_rev_that_does_not_resolve_is_a_fault_not_a_first_publish(
    tmp_path, monkeypatch, caplog
):
    served = _repo(tmp_path, monkeypatch)
    read = _outputs(tmp_path, monkeypatch)
    report = tmp_path / "r.md"
    with caplog.at_level("INFO"):
        code = main(["--geojson", str(served), "--rev", "deadbeef",
                     "--report", str(report)])

    assert code == EXIT_OK, "the direction policy holds: a fault never blocks"
    assert "could not read its baseline" in caplog.text
    assert "first publish" not in caplog.text
    assert "Revenue-delta guard OK" not in caplog.text, (
        "the all-clear must never be printed over neighbourhoods that were "
        "not compared"
    )
    assert read()["flagged"] != "0"
    assert "uncompared" in report.read_text().lower()


def test_a_genuinely_uncommitted_served_file_is_still_a_clean_skip(
    tmp_path, monkeypatch, caplog
):
    """The cry-wolf direction. Real repo, real HEAD, file simply not in it."""
    served = _repo(tmp_path, monkeypatch, committed=False)
    read = _outputs(tmp_path, monkeypatch)
    with caplog.at_level("INFO"):
        code = main(["--geojson", str(served)])

    assert code == EXIT_OK
    assert "first publish" in caplog.text
    assert "could not read its baseline" not in caplog.text
    assert read()["flagged"] == "0"


def test_a_baseline_outside_the_repo_faults_instead_of_raising(
    tmp_path, monkeypatch, caplog
):
    """`relative_to` used to raise ValueError here — a traceback and a NON-ZERO
    exit out of the one guard that must never stop a publish."""
    _repo(tmp_path, monkeypatch)
    read = _outputs(tmp_path, monkeypatch)
    stray = tmp_path.parent / "stray_served.geojson"
    stray.write_text(json.dumps(_served([_hood("H", 5_000_000)])))
    with caplog.at_level("INFO"):
        code = main(["--geojson", str(stray)])

    assert code == EXIT_OK
    assert read()["flagged"] != "0"
    assert "--before" in caplog.text, "say how to compare a file outside the repo"


def test_a_corrupt_committed_baseline_is_a_fault(tmp_path, monkeypatch, caplog):
    import check_revenue_deltas as mod

    served = _repo(tmp_path, monkeypatch)
    read = _outputs(tmp_path, monkeypatch)
    monkeypatch.setattr(
        mod, "_git",
        lambda *a: subprocess.CompletedProcess(a, 0, stdout="{not json", stderr=""),
    )
    with caplog.at_level("INFO"):
        code = main(["--geojson", str(served)])

    assert code == EXIT_OK
    assert read()["flagged"] != "0"
    assert "first publish" not in caplog.text


def test_the_fault_signal_actually_fires_the_issue_step(tmp_path, monkeypatch):
    """The value is only useful if refresh.yml's condition accepts it.

    `flagged` is a COUNT on the delta path and the literal `fault` here, and the
    step is gated on a string comparison — so pin the emitted value against the
    committed workflow rather than against a remembered condition. (S147 R2: the
    detector passing says nothing about the wiring.)
    """
    served = _repo(tmp_path, monkeypatch)
    read = _outputs(tmp_path, monkeypatch)
    main(["--geojson", str(served), "--rev", "deadbeef"])
    emitted = read()["flagged"]

    workflow = (
        Path(__file__).resolve().parent.parent
        / ".github" / "workflows" / "refresh.yml"
    ).read_text()
    step = workflow[workflow.index("Report a big revenue delta as an issue"):]
    condition = step[step.index("if:"): step.index("\n", step.index("if:"))]
    assert "revdelta.outputs.flagged" in condition
    for excluded in re.findall(r"!=\s*'([^']*)'", condition):
        assert emitted != excluded, (
            f"flagged={emitted!r} is excluded by refresh.yml's condition "
            f"{condition.strip()!r} — the fault would file no issue"
        )
