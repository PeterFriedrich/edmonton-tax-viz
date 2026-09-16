"""Tests for scripts/check_decisions_log.py (the decisions-log guard).

The load-bearing ones reconstruct what the guard was built against: a row that
announces "supersedes the 2026-07-29 row" while that row sits unmarked (the
file's practice on 2026-09-16 — 13 such rows, 4 marked), and a mark that the
first cut of the guard misread as an announcement pointing backwards.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from check_decisions_log import EXIT_FAIL, EXIT_OK, check, main, parse_rows  # noqa: E402

HEADER = "# Decisions Index\n\n| When | Decision | Full reasoning |\n|---|---|---|\n"


def _tree(tmp_path: Path, *rows: str) -> Path:
    (tmp_path / "docs").mkdir(parents=True)
    (tmp_path / "docs" / "DECISIONS.md").write_text(HEADER + "\n".join(rows) + "\n")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_real.py").write_text("def test_real_thing():\n    pass\n")
    (tmp_path / "tools" / "profiling").mkdir(parents=True)
    (tmp_path / "tools" / "profiling" / "verify-real.js").write_text("")
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "check_real.py").write_text("")
    return tmp_path


def _row(when: str, text: str) -> str:
    return f"| {when} | {text} | `docs/SPEC.md` |"


# --- check 1: a new row names a test or says it cannot ------------------------

def test_new_row_without_a_test_fails(tmp_path):
    failures = check(_tree(tmp_path, _row("2026-09-17", "**The clamp is $50k** — stability wins.")))
    assert len(failures) == 1 and "names no test" in failures[0]


def test_new_row_citing_a_real_test_passes(tmp_path):
    for cite in ("`test_real_thing`", "`verify-real.js`", "`check_real.py`", "`tests/test_real.py`"):
        root = _tree(tmp_path / cite.strip("`").replace("/", "_"),
                     _row("2026-09-17", f"**The clamp is $50k** — pinned by {cite}."))
        assert check(root) == [], cite


def test_new_row_tagged_unverifiable_passes(tmp_path):
    root = _tree(tmp_path, _row("2026-09-17", "**Neighbourhood is the unit** [unverifiable] — licensing."))
    assert check(root) == []


def test_old_row_without_a_test_is_grandfathered(tmp_path):
    assert check(_tree(tmp_path, _row("2026-07-13", "**Lens A window = 5yr**"))) == []


def test_dangling_test_id_fails_on_an_old_row_too(tmp_path):
    """The one S161 found by hand: a row naming a verify script deleted weeks earlier."""
    failures = check(_tree(tmp_path, _row("2026-07-25", "**Hides, not greys** — `verify-lens-visibility.js`.")))
    assert len(failures) == 1 and "verify-lens-visibility.js" in failures[0] and "does not exist" in failures[0]


# --- check 2: a superseded row is marked where it stands ----------------------

ORIGINAL = "**CSS extracted — stage 2 should wait until stage 1 proves it helps.**"
SUPERSEDER = "**`web/index.html` STAYS ONE FILE** — supersedes the deferral clause of the 2026-07-29 stage-1 row."


def test_unmarked_original_fails(tmp_path):
    """The file's practice on 2026-09-16: the new row announces, the original is left clean."""
    failures = check(_tree(tmp_path, _row("2026-07-29", ORIGINAL), _row("2026-09-05", SUPERSEDER)))
    assert len(failures) == 1
    assert "DECISIONS.md:6" in failures[0] and "2026-07-29 (L5)" in failures[0]
    assert "SUPERSEDED 2026-09-05" in failures[0]


def test_marked_original_passes(tmp_path):
    root = _tree(tmp_path,
                 _row("2026-07-29", "⚠️ **PARTLY SUPERSEDED 2026-09-05 — the deferral clause.** " + ORIGINAL),
                 _row("2026-09-05", SUPERSEDER))
    assert check(root) == []


def test_mark_naming_the_wrong_date_does_not_count(tmp_path):
    root = _tree(tmp_path,
                 _row("2026-07-29", "**SUPERSEDED 2026-08-01.** " + ORIGINAL),
                 _row("2026-09-05", SUPERSEDER))
    assert len(check(root)) == 1


def test_struck_original_passes(tmp_path):
    root = _tree(tmp_path, _row("2026-07-29", f"~~{ORIGINAL}~~"), _row("2026-09-05", SUPERSEDER))
    assert check(root) == []


def test_the_mark_is_not_itself_an_announcement(tmp_path):
    """First cut of the guard: 'PARTLY AMENDED 2026-08-15' read as a row announcing
    a supersession of 2026-08-15, which had no earlier row, and failed 9 marks it
    had just asked for."""
    root = _tree(tmp_path, _row("2026-08-12", "⚠️ **PARTLY AMENDED 2026-08-15 — see that row.** **The ≥25% floor.**"))
    assert check(root) == []


def test_row_above_form(tmp_path):
    root = _tree(tmp_path,
                 _row("2026-09-05", "**No JS toolchain in the publish path; `type=\"module\"` stays.**"),
                 _row("2026-09-05", "**Supersedes the `type=\"module\"` clause of the row above.**"))
    assert len(check(root)) == 1
    root = _tree(tmp_path / "ok",
                 _row("2026-09-05", "**PARTLY SUPERSEDED 2026-09-05 — see the next row.** **No JS toolchain.**"),
                 _row("2026-09-05", "**Supersedes the `type=\"module\"` clause of the row above.**"))
    assert check(root) == []


def test_same_day_form(tmp_path):
    root = _tree(tmp_path,
                 _row("2026-07-31", "**Gate on the way IN only.**"),
                 _row("2026-07-31", "**Armed on every tap** — reverses the clause locked earlier the same day."))
    assert len(check(root)) == 1


def test_when_it_happened_is_not_an_announcement(tmp_path):
    """'had already been retracted on 2026-08-11' describes a retraction, it does not make one."""
    root = _tree(tmp_path,
                 _row("2026-08-11", "**Negative extrusion renders.**"),
                 _row("2026-08-26", "**Prisms can be negative** — the claim had already been retracted on 2026-08-11."))
    assert check(root) == []


def test_announcing_a_date_with_no_row_fails(tmp_path):
    failures = check(_tree(tmp_path, _row("2026-09-05", "**X** — supersedes the 2026-01-01 row.")))
    assert len(failures) == 1 and "no earlier row" in failures[0]


# --- parsing + exit codes -----------------------------------------------------

def test_pipe_inside_inline_code_does_not_split_the_row():
    rows = parse_rows(HEADER + "| 2026-08-04 | **Mode flag `public\\|full`** | `docs/UI.md` |\n")
    assert len(rows) == 1 and "public\\|full" in rows[0].text


def test_month_only_dates_parse_as_undated_and_are_grandfathered(tmp_path):
    assert check(_tree(tmp_path, _row("2026-05 (Phase 1)", "**Neighbourhood as the unit.**"))) == []


def test_main_exit_codes(tmp_path, capsys):
    ok = _tree(tmp_path / "ok", _row("2026-07-13", "**Old row.**"))
    assert main(["--root", str(ok)]) == EXIT_OK
    bad = _tree(tmp_path / "bad", _row("2026-09-17", "**New row, no test.**"))
    assert main(["--root", str(bad)]) == EXIT_FAIL
    assert "FAIL" in capsys.readouterr().out
