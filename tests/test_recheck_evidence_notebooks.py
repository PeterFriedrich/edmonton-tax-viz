"""The evidence recheck must tell three outcomes apart, not two.

⚠️ The fixtures below differ ONLY in the condition under test. A notebook that
holds, one that flips an invariant, and one that cannot reach its sources all
print the same kind of output and differ only in how they exit — which is
exactly the distinction the script exists to make, and the one a naive
``returncode != 0`` check would collapse.
"""
import sys

import pytest

from scripts import recheck_evidence_notebooks as rc


HOLDS = """
print("  [PASS] the defect is still present upstream")
print("  [PASS] and the row count still matches")
"""

FLIPS = """
print("  [PASS] the defect is still present upstream")
print("  [FAIL] the missing set is non-empty")
raise AssertionError("1 invariant(s) failed — see above")
"""

# No [PASS] lines at all: the run died before any invariant could fire.
UNREACHABLE = """
import sys
print("Traceback (most recent call last):", file=sys.stderr)
print("requests.exceptions.ConnectionError: [Errno -2] Name or service not known",
      file=sys.stderr)
sys.exit(1)
"""

# ⚠️ The nastiest case: exits 0 having verified nothing.
SILENT = "pass\n"


@pytest.fixture
def notebooks(tmp_path, monkeypatch):
    """Write a fixture notebook AND put it on the roster.

    ⚠️ Registering the stem is not incidental. `--only` filters the roster
    rather than naming arbitrary files, so a fixture that is written but not
    registered makes `main()` return an EMPTY result set — and a test asserting
    over that list passes without ever exercising anything. One test here did
    exactly that before this fixture registered its stems.
    """
    monkeypatch.setattr(rc, "STANDALONE", tmp_path)
    monkeypatch.setattr(rc, "REPO", tmp_path)
    monkeypatch.setattr(rc, "EVIDENCE", ())
    monkeypatch.setattr(rc, "JUSTIFICATION", ())

    def write(stem, body):
        (tmp_path / f"{stem}.py").write_text(body)
        monkeypatch.setattr(rc, "EVIDENCE", rc.EVIDENCE + (stem,))

    return write


def test_a_holding_notebook_passes_and_counts_its_invariants(notebooks):
    notebooks("holds", HOLDS)
    status, detail = rc.run_one("holds")
    assert status == rc.PASS
    assert "2 invariant(s) held" in detail


def test_a_flipped_invariant_reports_MOVED_and_names_it(notebooks):
    notebooks("flips", FLIPS)
    status, detail = rc.run_one("flips")
    assert status == rc.MOVED
    # The failing claim must reach the issue body — "1 failed" is not actionable.
    assert "the missing set is non-empty" in detail


def test_an_unreachable_source_is_UNCHECKABLE_not_MOVED(notebooks):
    """The distinction this repo has got wrong before, in the other direction.

    A guard that could not read its baseline once reported like a guard that
    read it and found nothing. Both exit non-zero; only one is a measurement.
    """
    notebooks("unreachable", UNREACHABLE)
    status, detail = rc.run_one("unreachable")
    assert status == rc.UNCHECKABLE
    assert status != rc.MOVED
    assert "ConnectionError" in detail or "no invariant verdict" in detail


def test_a_notebook_that_verifies_nothing_does_not_pass(notebooks):
    """Exit 0 is not evidence. It is the absence of evidence."""
    notebooks("silent", SILENT)
    status, detail = rc.run_one("silent")
    assert status == rc.UNCHECKABLE
    assert "recorded no invariants" in detail


def test_a_missing_notebook_is_UNCHECKABLE(notebooks):
    status, detail = rc.run_one("never_written")
    assert status == rc.UNCHECKABLE
    assert "does not exist" in detail


def test_render_puts_uncheckable_above_moved_above_pass():
    results = [
        ("evidence", "c", rc.PASS, "8 invariant(s) held"),
        ("evidence", "a", rc.MOVED, "**1 of 9 flipped** — [FAIL] x"),
        ("justification", "b", rc.UNCHECKABLE, "timed out"),
    ]
    body, n_moved, n_unchecked = rc.render(results)
    assert n_moved == 1 and n_unchecked == 1
    assert body.index("`b`") < body.index("`a`") < body.index("`c`")


def test_render_never_calls_an_uncheckable_run_healthy():
    """A run that verified nothing must not read as a clean bill of health."""
    results = [("evidence", "a", rc.UNCHECKABLE, "timed out")]
    body, _, n_unchecked = rc.render(results)
    assert n_unchecked == 1
    assert "COULD NOT BE CHECKED" in body
    assert "Everything still holds" not in body


def test_all_green_says_so_plainly():
    results = [("evidence", "a", rc.PASS, "4 invariant(s) held")]
    body, n_moved, n_unchecked = rc.render(results)
    assert (n_moved, n_unchecked) == (0, 0)
    assert "Everything still holds" in body


def test_every_listed_notebook_exists():
    """The roster must not drift away from the directory it names."""
    import pathlib
    standalone = pathlib.Path(__file__).resolve().parent.parent / "notebooks" / "standalone"
    for stem in rc.EVIDENCE + rc.JUSTIFICATION:
        assert (standalone / f"{stem}.py").exists(), f"{stem} is listed but absent"


def test_the_two_species_are_disjoint():
    assert not set(rc.EVIDENCE) & set(rc.JUSTIFICATION)


def test_json_output_is_machine_readable(notebooks, capsys):
    notebooks("holds", HOLDS)
    rc.main(["--json", "--only", "holds", "--python", sys.executable])
    import json
    rows = json.loads(capsys.readouterr().out)
    # ⚠️ Assert the list is NON-EMPTY first. Without this the test passes on a
    # run that selected nothing, which is how it was first written.
    assert len(rows) == 1
    assert {"species", "notebook", "status", "detail"} <= rows[0].keys()
    assert rows[0]["notebook"] == "holds" and rows[0]["status"] == rc.PASS


def test_a_relative_interpreter_path_still_finds_the_interpreter(notebooks, capsys):
    """Notebooks run with cwd set to their own directory.

    A relative `--python` (the way this repo is normally driven:
    `.venv/bin/python`) would otherwise resolve against that directory and
    raise FileNotFoundError before a single notebook ran — reported as a crash
    rather than as a result.
    """
    import os
    notebooks("holds", HOLDS)
    rel = os.path.relpath(sys.executable, os.getcwd())
    rc.main(["--json", "--only", "holds", "--python", rel])
    import json
    rows = json.loads(capsys.readouterr().out)
    assert rows and rows[0]["status"] == rc.PASS
