"""Tests for scripts/check_permit_names.py (the permit-name drift issue guard)."""

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import check_permit_names as cpn  # noqa: E402

BOUNDARIES = {"CHAPPELLE", "ALLARD", "HERITAGE VALLEY AREA"}


def _permits(*rows):
    return pd.DataFrame(
        rows, columns=["neighbourhood_name", "new_dwelling_units", "new_dwelling_permits", "ind_permits"]
    )


def test_unmatched_is_names_without_a_boundary():
    out = cpn.unmatched_permits(
        _permits(("CHAPPELLE", 10, 2, 0), ("ALLARD, HERITAGE VALLEY AREA", 18, 3, 0)), BOUNDARIES
    )
    assert list(out["neighbourhood_name"]) == ["ALLARD, HERITAGE VALLEY AREA"]


def test_compare_splits_added_and_removed():
    added, removed = cpn.compare_to_baseline({"A", "NEW"}, {"A", "GONE"})
    assert added == {"NEW"}
    assert removed == {"GONE"}


def _run(tmp_path, monkeypatch, permits, baseline_names):
    baseline = tmp_path / "expected.json"
    baseline.write_text(json.dumps({cpn.BASELINE_KEY: {n: "reason" for n in baseline_names}}))
    monkeypatch.setattr(cpn, "_load_live", lambda *_: (permits, BOUNDARIES))
    gho = tmp_path / "gho"
    monkeypatch.setenv("GITHUB_OUTPUT", str(gho))
    report = tmp_path / "r.md"
    rc = cpn.main(["--baseline", str(baseline), "--report", str(report)])
    return rc, gho.read_text(), report


def test_respelled_name_is_flagged_and_reported(tmp_path, monkeypatch):
    # The 2026-11-10 shape: a straddler already in the baseline, plus the City's
    # respelling of a corrected name that no key matches.
    permits = _permits(
        ("CHAPPELLE", 6848, 900, 0),
        ("ALLARD, HERITAGE VALLEY AREA", 18, 3, 0),
        ("CHAPPELLE, HERITAGE VALLEY AREA", 28, 8, 0),
    )
    rc, gho, report = _run(tmp_path, monkeypatch, permits, {"ALLARD, HERITAGE VALLEY AREA"})
    assert rc == 0  # never blocks the publish
    assert "flagged=1" in gho
    assert "CHAPPELLE, HERITAGE VALLEY AREA" in gho
    body = report.read_text()
    assert "| `CHAPPELLE, HERITAGE VALLEY AREA` | 28 | 8 | 0 |" in body
    assert "ALLARD" not in body


def test_baseline_names_only_is_quiet(tmp_path, monkeypatch):
    permits = _permits(("CHAPPELLE", 10, 2, 0), ("ALLARD, HERITAGE VALLEY AREA", 18, 3, 0))
    rc, gho, report = _run(tmp_path, monkeypatch, permits, {"ALLARD, HERITAGE VALLEY AREA"})
    assert rc == 0
    assert gho == "flagged=0\n"
    assert not report.exists()


def test_name_leaving_the_set_does_not_flag(tmp_path, monkeypatch):
    permits = _permits(("CHAPPELLE", 10, 2, 0))
    rc, gho, _ = _run(tmp_path, monkeypatch, permits, {"ALLARD, HERITAGE VALLEY AREA"})
    assert rc == 0
    assert gho == "flagged=0\n"


def test_title_has_no_shell_metacharacters_from_markup(tmp_path, monkeypatch):
    # The title reaches a shell in refresh.yml; markdown backticks there would execute.
    permits = _permits(("THE UPLANDS, RIVER'S EDGE", 5, 1, 0))
    _, gho, _ = _run(tmp_path, monkeypatch, permits, set())
    title = next(line for line in gho.splitlines() if line.startswith("title="))
    assert "`" not in title


def test_committed_baseline_entries_are_reasoned_comma_lists():
    # Invariant, not a count: RUNBOOK §0f adds entries. A non-list name here would
    # be a single hood the map is missing, which belongs in a correction instead.
    names = json.loads((ROOT / "data" / "expected_unmatched.json").read_text())[cpn.BASELINE_KEY]
    assert names
    assert all("," in n and reason.strip() for n, reason in names.items())


def test_names_output_is_pipe_joined_for_the_dedup_loop(tmp_path, monkeypatch):
    # refresh.yml splits `names` on "|" and dedups each against open issue titles.
    permits = _permits(("EKOTA, SUMMERSIDE", 5, 1, 0), ("SATOO, SUMMERSIDE", 3, 1, 0))
    _, gho, _ = _run(tmp_path, monkeypatch, permits, set())
    assert "names=EKOTA, SUMMERSIDE|SATOO, SUMMERSIDE" in gho


def test_a_crash_reports_could_not_run_and_never_the_all_clear(tmp_path, monkeypatch):
    # In a year hold main.py is skipped, so a raise here would be the run's only failure.
    def boom(*_):
        raise ValueError("permits CSV missing required columns: ['neighbourhood']")
    baseline = tmp_path / "expected.json"
    baseline.write_text(json.dumps({cpn.BASELINE_KEY: {}}))
    monkeypatch.setattr(cpn, "_load_live", boom)
    gho = tmp_path / "gho"
    monkeypatch.setenv("GITHUB_OUTPUT", str(gho))
    report = tmp_path / "r.md"
    rc = cpn.main(["--baseline", str(baseline), "--report", str(report)])
    assert rc == 0
    out = gho.read_text()
    assert "flagged=error" in out and "flagged=0" not in out
    assert f"title={cpn.ERROR_TITLE}" in out
    assert "UNCHECKED" in report.read_text()
