"""Tests for scripts/check_year_alignment.py (the T2 year-alignment guard)."""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

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

def test_aligned():
    result, msg = check_alignment(2025, 2025, {"2025"})
    assert result == "aligned"


def test_roll_ahead_rates_missing_is_hold_with_holding_banner():
    result, msg = check_alignment(2026, 2025, {"2025"})
    assert result == "hold"
    assert "2025" in msg and "2026" in msg
    assert "aren't incorporated" in msg


def test_roll_ahead_rates_present_is_hold_pending_review():
    result, msg = check_alignment(2026, 2025, {"2025", "2026"})
    assert result == "hold"
    assert "pending review" in msg


def test_pin_matches_roll_but_rates_missing_is_hold():
    result, msg = check_alignment(2025, 2025, {"2024"})
    assert result == "hold"
    assert "missing from the rate table" in msg


def test_roll_behind_pin_is_hold():
    # A regression in the feed (or a wrong pin bump) must also hold.
    result, _ = check_alignment(2024, 2025, {"2025"})
    assert result == "hold"


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
    assert run_main(tmp_path, "2025-01-01 to 2025-12-31", 2025) == EXIT_ALIGNED


def test_main_mismatch_exit_3(tmp_path):
    assert run_main(tmp_path, "2026-01-01 to 2026-12-31", 2025) == EXIT_HOLD


def test_main_unreadable_metadata_exit_4(tmp_path):
    assert run_main(tmp_path, None, 2025) == EXIT_INCONCLUSIVE


def test_main_writes_github_output(tmp_path, monkeypatch):
    out = tmp_path / "gh_output"
    monkeypatch.setenv("GITHUB_OUTPUT", str(out))
    run_main(tmp_path, "2026-01-01 to 2026-12-31", 2025)
    text = out.read_text()
    assert "result=hold" in text
    assert "detected_year=2026" in text
    assert "pinned_year=2025" in text
    assert "banner=Showing 2025 data" in text
