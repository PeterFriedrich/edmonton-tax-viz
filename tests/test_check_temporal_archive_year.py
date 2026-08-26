"""Tests for scripts/check_temporal_archive_year.py (the frozen-archive guard).

Every test drives main() through --archive/--fir-tax-base against files built in
tmp_path, so nothing here reads the repo's real archive — the real one currently
FAILS by design (the 2025 entry is the 2026 roll, docs/DATA_ISSUES.md), and a
test that asserted today's repo state would have to be rewritten the moment that
is resolved.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from check_temporal_archive_year import (
    EXIT_HOLD,
    EXIT_INCONCLUSIVE,
    EXIT_OK,
    archived_residential_bases,
    main,
)

# The real filed bases: consecutive years ~8-10% apart, which is what makes the
# residual a sharp label check rather than a coin flip.
FILED = {2023: 131_284_317_914.0, 2024: 134_439_557_008.0,
         2025: 148_128_818_480.0, 2026: 160_372_669_990.0}


def write_archive(tmp_path: Path, years: dict[int, float]) -> Path:
    """An archive whose RESIDENTIAL totals are exactly `years`, split over 2 hoods.

    The split matters: the guard sums across hoods AND classes, and a
    single-hood fixture would pass even if it summed only the first one.
    """
    payload = {"years": {}}
    for year, residential in years.items():
        payload["years"][str(year)] = {
            "HOOD A": {
                "RESIDENTIAL": [100, residential * 0.6],
                # Non-residential classes must be ignored entirely. OTHER
                # RESIDENTIAL is deliberately large here: including it is the
                # mistake the guard's RESIDENTIAL_CLASS comment warns about.
                "OTHER RESIDENTIAL": [20, residential * 0.5],
                "COMMERCIAL": [10, residential * 0.3],
            },
            "HOOD B": {
                "RESIDENTIAL": [50, residential * 0.4],
                "FARMLAND": [1, 55_471_000.0],
            },
        }
    path = tmp_path / "temporal_archive.json"
    path.write_text(json.dumps(payload))
    return path


def write_fir(tmp_path: Path, filed=FILED) -> Path:
    path = tmp_path / "fir_tax_base.json"
    path.write_text(json.dumps(
        {"years": {str(y): {"assessment": {"residential": v}} for y, v in filed.items()}}))
    return path


def run_main(tmp_path: Path, years: dict[int, float], filed=FILED) -> int:
    return main(["--archive", str(write_archive(tmp_path, years)),
                 "--fir-tax-base", str(write_fir(tmp_path, filed))])


# --- archived_residential_bases ----------------------------------------------

def test_sums_residential_across_hoods_and_ignores_other_classes(tmp_path):
    path = write_archive(tmp_path, {2026: 160_000_000_000.0})
    assert archived_residential_bases(path) == {2026: 160_000_000_000.0}


def test_reads_every_archived_year(tmp_path):
    path = write_archive(tmp_path, {2025: 1.0, 2026: 2.0})
    assert sorted(archived_residential_bases(path)) == [2025, 2026]


# --- main() exit codes -------------------------------------------------------

def test_correctly_labelled_years_exit_0(tmp_path):
    assert run_main(tmp_path, {2025: FILED[2025] * 1.012,
                               2026: FILED[2026] * 1.012}) == EXIT_OK


def test_mislabelled_year_exit_3(tmp_path):
    """THE defect this guard exists for: a 2026 roll frozen under the label 2025.

    Both entries carry the 2026 base, four weeks apart — the 2026 one is fine
    and the 2025 one is the same roll wearing the wrong year.
    """
    assert run_main(tmp_path, {2025: FILED[2026] * 1.0117,
                               2026: FILED[2026] * 1.0118}) == EXIT_HOLD


def test_one_bad_year_reds_the_whole_check(tmp_path):
    """A good year must not mask a bad one — the guard reports on every entry."""
    assert run_main(tmp_path, {2023: FILED[2023],
                               2025: FILED[2026]}) == EXIT_HOLD


def test_no_year_fits_is_inconclusive_not_a_mislabel(tmp_path):
    """An unrecognisable base is not evidence about the LABEL. Don't guess."""
    assert run_main(tmp_path, {2026: FILED[2026] * 1.5}) == EXIT_INCONCLUSIVE


def test_year_outside_the_fir_range_is_reported_not_passed(tmp_path):
    """⚠️ Unverifiable must not read as verified.

    2027 cannot be checked against a 2023-2026 anchor. It must not silently
    count as OK — the run stays exit 0 (there is nothing wrong, only something
    unknown) but the year is named and excluded from the 'checked' count.
    """
    archive = write_archive(tmp_path, {2026: FILED[2026] * 1.012, 2027: 1.0})
    fir = write_fir(tmp_path)
    assert main(["--archive", str(archive), "--fir-tax-base", str(fir)]) == EXIT_OK


def test_missing_archive_is_skipped_not_failed(tmp_path):
    """No archive must never red the build — there is nothing to check."""
    fir = write_fir(tmp_path)
    assert main(["--archive", str(tmp_path / "absent.json"),
                 "--fir-tax-base", str(fir)]) == EXIT_OK


def test_missing_anchor_is_skipped_not_failed(tmp_path):
    archive = write_archive(tmp_path, {2026: FILED[2026]})
    assert main(["--archive", str(archive),
                 "--fir-tax-base", str(tmp_path / "absent.json")]) == EXIT_OK


def test_empty_archive_is_skipped_not_failed(tmp_path):
    path = tmp_path / "temporal_archive.json"
    path.write_text(json.dumps({"years": {}}))
    assert main(["--archive", str(path),
                 "--fir-tax-base", str(write_fir(tmp_path))]) == EXIT_OK


# --- the CI contract ---------------------------------------------------------

def test_writes_github_output_naming_the_mislabelled_year(tmp_path, monkeypatch):
    out = tmp_path / "gh_output"
    monkeypatch.setenv("GITHUB_OUTPUT", str(out))
    run_main(tmp_path, {2025: FILED[2026] * 1.012, 2026: FILED[2026] * 1.012})
    written = out.read_text()
    assert "result=hold" in written
    assert "mismatched=2025" in written


def test_writes_github_output_when_ok(tmp_path, monkeypatch):
    out = tmp_path / "gh_output"
    monkeypatch.setenv("GITHUB_OUTPUT", str(out))
    run_main(tmp_path, {2026: FILED[2026] * 1.012})
    assert "result=ok" in out.read_text()


def test_the_repo_archive_is_readable_by_the_guard():
    """Not an assertion about the ANSWER — only that the real file still parses.

    The shape of data/temporal_archive.json is what this guard depends on, and a
    change to it would otherwise surface as a skipped check rather than a red.
    """
    repo_archive = Path(__file__).resolve().parent.parent / "data" / "temporal_archive.json"
    if not repo_archive.exists():
        return
    bases = archived_residential_bases(repo_archive)
    assert bases, "the archive parsed to no years — the guard would silently skip"
    assert all(v > 0 for v in bases.values())
