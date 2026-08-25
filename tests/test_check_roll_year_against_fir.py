"""Tests for scripts/check_roll_year_against_fir.py (the measured roll-year guard).

Every test drives main() through --assessment-csv/--fir-tax-base/--expected-year
so nothing here imports main.py or geopandas, and detect_year is exercised
directly for the boundary cases.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from check_roll_year_against_fir import (
    EXIT_HOLD,
    EXIT_INCONCLUSIVE,
    EXIT_OK,
    MAX_PLAUSIBLE_RESIDUAL,
    MIN_SEPARATION,
    detect_year,
    main,
)

# The real shape: consecutive filed years sit ~8-10% apart, which is what makes
# the residual a sharp year detector rather than a coin flip.
FILED = {2023: 131_284_317_914.0, 2024: 134_439_557_008.0,
         2025: 148_128_818_480.0, 2026: 160_372_669_990.0}


# --- detect_year -------------------------------------------------------------

def test_detects_the_year_it_sits_closest_to():
    """The real 2026 measurement: +1.2% against 2026, ~10% against its neighbour."""
    detected, residuals = detect_year(162_273_056_185.0, FILED)
    assert detected == 2026
    assert 0.011 < residuals[2026] < 0.013
    assert residuals[2025] > 0.09


def test_exact_match_detects_that_year():
    assert detect_year(FILED[2025], FILED)[0] == 2025


def test_no_year_within_tolerance_is_inconclusive():
    """A base far above every filed year means something other than the year is wrong."""
    assert detect_year(FILED[2026] * 1.5, FILED)[0] is None


def test_too_close_to_call_is_inconclusive():
    """Sitting midway between two filed years must not pick one."""
    midpoint = (FILED[2025] + FILED[2026]) / 2
    assert detect_year(midpoint, FILED)[0] is None


def test_separation_floor_is_what_rejects_the_midpoint():
    """Guard the constants themselves: a midpoint fit is inside MAX_PLAUSIBLE_RESIDUAL
    only because MIN_SEPARATION rejects it, so loosening either changes behaviour."""
    midpoint = (FILED[2025] + FILED[2026]) / 2
    _, residuals = detect_year(midpoint, FILED)
    best, runner_up = sorted(abs(r) for r in residuals.values())[:2]
    assert best < MAX_PLAUSIBLE_RESIDUAL          # tolerance alone would accept it
    assert runner_up - best < MIN_SEPARATION      # separation is what rejects it


# --- main() exit codes -------------------------------------------------------

def run_main(tmp_path: Path, ours: float, expected: int, filed=FILED) -> int:
    csv = tmp_path / "roll.csv"
    csv.write_text("placeholder\n")   # existence is all main() checks before measuring
    anchor = tmp_path / "fir_tax_base.json"
    anchor.write_text(json.dumps(
        {"years": {str(y): {"assessment": {"residential": v}} for y, v in filed.items()}}))

    import check_roll_year_against_fir as mod
    orig = mod.our_residential_base
    mod.our_residential_base = lambda csv_path=None: ours
    try:
        return main(["--expected-year", str(expected),
                     "--assessment-csv", str(csv), "--fir-tax-base", str(anchor)])
    finally:
        mod.our_residential_base = orig


def test_main_aligned_exit_0(tmp_path):
    assert run_main(tmp_path, FILED[2026] * 1.012, 2026) == EXIT_OK


def test_main_mismatch_exit_3(tmp_path):
    """The S119 failure itself: the roll measures 2026 while the pin still says 2025."""
    assert run_main(tmp_path, FILED[2026] * 1.012, 2025) == EXIT_HOLD


def test_main_no_fit_exit_4(tmp_path):
    assert run_main(tmp_path, FILED[2026] * 1.5, 2026) == EXIT_INCONCLUSIVE


def test_main_missing_roll_is_skipped_not_failed(tmp_path):
    """No local roll must never red the build — there is nothing to measure."""
    anchor = tmp_path / "fir_tax_base.json"
    anchor.write_text(json.dumps({"years": {}}))
    assert main(["--expected-year", "2026",
                 "--assessment-csv", str(tmp_path / "absent.csv"),
                 "--fir-tax-base", str(anchor)]) == EXIT_OK


def test_main_missing_anchor_is_skipped_not_failed(tmp_path):
    csv = tmp_path / "roll.csv"
    csv.write_text("placeholder\n")
    assert main(["--expected-year", "2026", "--assessment-csv", str(csv),
                 "--fir-tax-base", str(tmp_path / "absent.json")]) == EXIT_OK


# --- the CI contract refresh.yml gates on ------------------------------------

def test_main_writes_github_output_on_hold(tmp_path, monkeypatch):
    out = tmp_path / "gh_output"
    monkeypatch.setenv("GITHUB_OUTPUT", str(out))
    run_main(tmp_path, FILED[2026] * 1.012, 2025)
    text = out.read_text()
    assert "result=hold" in text
    assert "detected_year=2026" in text
    assert "pinned_year=2025" in text
    assert "banner=Showing 2025 data" in text


def test_hold_banner_is_single_line(tmp_path, monkeypatch):
    """$GITHUB_OUTPUT is line-delimited — a newline in the banner would truncate it."""
    out = tmp_path / "gh_output"
    monkeypatch.setenv("GITHUB_OUTPUT", str(out))
    run_main(tmp_path, FILED[2026] * 1.012, 2025)
    banner = [ln for ln in out.read_text().splitlines() if ln.startswith("banner=")]
    assert len(banner) == 1
    assert banner[0].endswith("are incorporated.")


def test_refresh_workflow_gates_every_publish_step_on_both_guards():
    """Wiring a guard in is only half of it — the gate has to cover every step.

    Two guards can hold, so a step gated on just one of them regenerates and
    publishes during the other's hold. That is precisely the silent-correctness
    shape this project keeps getting bitten by, and it is easy to reintroduce by
    copying a neighbouring step's `if:` when adding one.
    """
    import yaml
    workflow = yaml.safe_load(
        (Path(__file__).resolve().parents[1] / ".github/workflows/refresh.yml").read_text())
    conditions = [s["if"] for s in workflow["jobs"]["build"]["steps"]
                  if "if" in s and "yearcheck" in s["if"]]
    assert conditions, "no step gates on the year guard — the gate vanished"
    for cond in conditions:
        assert "rollyear" in cond, f"step gates on yearcheck but not rollyear: {cond!r}"


def test_main_writes_github_output_when_ok(tmp_path, monkeypatch):
    out = tmp_path / "gh_output"
    monkeypatch.setenv("GITHUB_OUTPUT", str(out))
    run_main(tmp_path, FILED[2026] * 1.012, 2026)
    text = out.read_text()
    assert "result=ok" in text
    assert "banner=" not in text      # nothing to show a visitor on a good run
