"""Tests for scripts/check_year_alignment.py (the T2 year-alignment guard)."""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from datetime import date

from check_year_alignment import (
    EXIT_ALIGNED,
    EXIT_HOLD,
    EXIT_INCONCLUSIVE,
    check_alignment,
    main,
    parse_coverage_year,
)


def metadata_with_coverage(coverage: str) -> dict:
    return {"metadata": {"custom_fields": {"Time Frame": {"Period of Coverage": coverage}}}}


# --- parse_coverage_year -----------------------------------------------------

def test_parse_normal_coverage():
    assert parse_coverage_year(metadata_with_coverage("2025-01-01 to 2025-12-31")) == 2025


def test_parse_single_year_string():
    assert parse_coverage_year(metadata_with_coverage("2026")) == 2026


def test_parse_multi_year_coverage_raises():
    with pytest.raises(ValueError, match="multiple years"):
        parse_coverage_year(metadata_with_coverage("2025-01-01 to 2026-12-31"))


def test_parse_no_year_raises():
    with pytest.raises(ValueError, match="No year found"):
        parse_coverage_year(metadata_with_coverage("current calendar year"))


def test_parse_missing_field_raises():
    with pytest.raises(KeyError):
        parse_coverage_year({"metadata": {"custom_fields": {}}})


# --- check_alignment ---------------------------------------------------------
#
# ⚠️ These use YEAR-RELATIVE values, not literals. A coverage year in the PAST
# now means "Socrata's hand-maintained string is stale", which is exactly the
# 2026-08-25 defect; hard-coding 2025 made the suite assert the bug.

NOW = date.today().year


def test_aligned():
    result, msg = check_alignment(NOW, NOW, {str(NOW)})
    assert result == "aligned"


def test_past_coverage_year_is_stale_metadata_not_aligned():
    """The 2026-08-25 defect: Edmonton left the string on 2025 all through 2026.

    Pin and metadata agreed with each other while both were a year stale, so
    the guard reported "aligned" and the pipeline billed a 2026 roll at 2025
    rates. A coverage year older than the calendar year is now untrustworthy.
    """
    result, msg = check_alignment(NOW - 1, NOW - 1, {str(NOW - 1)})
    assert result == "stale-metadata"
    assert "check_roll_year_against_fir" in msg


def test_roll_ahead_rates_missing_is_hold_with_holding_banner():
    result, msg = check_alignment(NOW + 1, NOW, {str(NOW)})
    assert result == "hold"
    assert str(NOW) in msg and str(NOW + 1) in msg
    assert "aren't incorporated" in msg


def test_roll_ahead_rates_present_is_hold_pending_review():
    result, msg = check_alignment(NOW + 1, NOW, {str(NOW), str(NOW + 1)})
    assert result == "hold"
    assert "pending review" in msg


def test_pin_matches_roll_but_rates_missing_is_hold():
    result, msg = check_alignment(NOW, NOW, {str(NOW - 1)})
    assert result == "hold"
    assert "missing from the rate table" in msg


def test_roll_behind_pin_is_stale_metadata():
    # Roll reading BEHIND the pin now trips the stale-string branch first: a
    # past coverage year can no longer be evidence about the roll at all.
    result, _ = check_alignment(NOW - 1, NOW, {str(NOW)})
    assert result == "stale-metadata"


# --- main() exit codes (offline via --metadata-file; explicit --expected-year
# so the test never imports main.py / geopandas) -------------------------------

def run_main(tmp_path: Path, coverage: str | None, expected: int, rates_years=("2025",)) -> int:
    rates = tmp_path / "mill_rates.json"
    rates.write_text(json.dumps({"rates": {y: {} for y in rates_years}}))
    args = ["--expected-year", str(expected), "--rates-json", str(rates)]
    if coverage is not None:
        meta = tmp_path / "metadata.json"
        meta.write_text(json.dumps(metadata_with_coverage(coverage)))
        args += ["--metadata-file", str(meta)]
    else:
        args += ["--metadata-file", str(tmp_path / "does_not_exist.json")]
    return main(args)


def test_main_aligned_exit_0(tmp_path):
    assert run_main(tmp_path, f"{NOW}-01-01 to {NOW}-12-31", NOW,
                    rates_years=(str(NOW),)) == EXIT_ALIGNED


def test_main_mismatch_exit_3(tmp_path):
    assert run_main(tmp_path, f"{NOW + 1}-01-01 to {NOW + 1}-12-31", NOW,
                    rates_years=(str(NOW),)) == EXIT_HOLD


def test_main_stale_coverage_string_exit_4(tmp_path):
    """A past coverage year is inconclusive, NOT a hold — it must not raise a banner.

    We know nothing about the roll when the string is stale; holding would
    publish a guess. check_roll_year_against_fir.py is what can answer.
    """
    assert run_main(tmp_path, f"{NOW - 1}-01-01 to {NOW - 1}-12-31", NOW - 1,
                    rates_years=(str(NOW - 1),)) == EXIT_INCONCLUSIVE


def test_main_unreadable_metadata_exit_4(tmp_path):
    assert run_main(tmp_path, None, NOW) == EXIT_INCONCLUSIVE


def test_main_writes_github_output(tmp_path, monkeypatch):
    out = tmp_path / "gh_output"
    monkeypatch.setenv("GITHUB_OUTPUT", str(out))
    run_main(tmp_path, f"{NOW + 1}-01-01 to {NOW + 1}-12-31", NOW, rates_years=(str(NOW),))
    text = out.read_text()
    assert "result=hold" in text
    assert f"detected_year={NOW + 1}" in text
    assert f"pinned_year={NOW}" in text
    assert f"banner=Showing {NOW} data" in text
