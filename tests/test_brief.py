"""Guards on the Claude web brief (`scripts/make_brief.py`, `docs/CLAUDE_WEB.md`).

The committed `docs/BRIEF.md` is what a claude.ai Project syncs. Unlike the
template, there is no staleness test here: `/handoff` regenerates it (why:
`scripts/make_brief.py` docstring). These pin what the generator keeps and
drops, each against a fixture repo, so a parser that quietly stops matching
fails here instead of producing a brief with an empty section.
"""
import importlib.util
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

_spec = importlib.util.spec_from_file_location("make_brief", REPO / "scripts" / "make_brief.py")
make_brief = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(make_brief)


def _fixture(root: Path) -> Path:
    (root / "docs").mkdir()
    (root / "CLAUDE.md").write_text(
        "# Claude Instructions\n\n## Project\nToy fiscal analysis.\n\n"
        "## Key Files\n- `TODO.md` — the backlog. Read it first.\n\n## Other\nx\n")
    (root / "TODO.md").write_text(
        "# TODO\n\n## Open work\n\n### Group one\n\n"
        "- [ ] **Open item.** First line\n  continues here.\n"
        "  - [ ] a nested child, not a top-level item\n"
        "- [x] **Closed but not yet archived.**\n\n## Done\n\n- [x] **Archived.**\n")
    (root / "docs" / "DECISIONS.md").write_text(
        "# Decisions\n\n| When | Decision | Full reasoning |\n|---|---|---|\n"
        "| 2026-09-01 | ~~**Old rule**~~ SUPERSEDED 2026-09-02 | `docs/X.md` |\n"
        "| 2026-09-02 | **New rule.** Long tail sentence. | `docs/X.md` |\n"
        "| 2026-09-03 | **Parked on St. Albert licensing.** Middle sentence. "
        "Rejected: scraping it anyway. | `docs/X.md` |\n"
        "| 2026-09-04 | **Keep the flag.** Why. The `x`-rejected clause stays. | `docs/X.md` |\n")
    (root / "docs" / "DATA_ISSUES.md").write_text(
        "# DATA_ISSUES\n\n| this file | where |\n|---|---|\n| a | b |\n\n"
        "## Status at a glance\n\n| # | issue | evidence | report text | status |\n"
        "|---|---|---|---|---|\n| 1 | wrong year | link | draft | **NOT SENT** |\n\n## 1. Detail\n")
    (root / "docs" / "SCOPE.md").write_text("# SCOPE\n\n## Out of scope\n\n- **Rasters.** No GIS.\n")
    (root / "requirements.txt").write_text("# comment\npandas==2.3.0\njupyterlab==4.0\n")
    (root / "requirements-ci.txt").write_text("# comment\npandas==2.3.0\n")
    return root


def test_brief_carries_each_source(tmp_path):
    brief = make_brief.build(_fixture(tmp_path))
    for expected in ("Toy fiscal analysis.", "**Rasters.** No GIS.", "pandas==2.3.0",
                     "**New rule.**", "**Open item.** First line continues here.",
                     "**Group one**", "`TODO.md` — the backlog", "CLAIM-CHECK"):
        assert expected in brief, expected


def test_brief_drops_dead_and_closed_rows(tmp_path):
    brief = make_brief.build(_fixture(tmp_path))
    for dropped in ("Old rule", "Closed but not yet archived", "Archived.",
                    "nested child", "Long tail sentence", "Middle sentence",
                    "jupyterlab", "`x`-rejected"):
        assert dropped not in brief, dropped


def test_decision_keeps_its_rejected_sentence_and_survives_st(tmp_path):
    """The two template bugs alberta-regional-viz found (2026-09-30): the summary
    was the first sentence only, so "Rejected:" clauses were lost, and the
    sentence split cut "St. Albert" to "St."."""
    brief = make_brief.build(_fixture(tmp_path))
    assert "**Parked on St. Albert licensing.** … Rejected: scraping it anyway." in brief


def test_data_issues_reads_the_status_table(tmp_path):
    brief = make_brief.build(_fixture(tmp_path))
    assert "- #1 wrong year — status: **NOT SENT**" in brief
    (tmp_path / "docs" / "DATA_ISSUES.md").write_text("# DATA_ISSUES\n")
    empty = make_brief.build(tmp_path).split("## Known upstream data defects")[1].split("##")[0]
    assert "no rows in the" in empty  # never reported as "no defects"


def test_check_goes_red_when_a_source_changes(tmp_path):
    """Falsification for the staleness guard: write the brief, edit a source,
    and `--check` must fail; rewrite, and it must pass again."""
    root = _fixture(tmp_path)
    args = ["--root", str(root)]
    assert make_brief.main(args + ["--check"]) == make_brief.EXIT_FAIL  # missing
    assert make_brief.main(args + ["--write"]) == make_brief.EXIT_OK
    assert make_brief.main(args + ["--check"]) == make_brief.EXIT_OK
    decisions = root / "docs" / "DECISIONS.md"
    decisions.write_text(decisions.read_text() + "| 2026-09-03 | **Newer rule.** | `docs/X.md` |\n")
    assert make_brief.main(args + ["--check"]) == make_brief.EXIT_FAIL
    assert make_brief.main(args + ["--write"]) == make_brief.EXIT_OK
    assert make_brief.main(args + ["--check"]) == make_brief.EXIT_OK
