"""Tests for scripts/check_doc_citations.py (the doc-citation drift guard).

⚠️ The load-bearing test here is ``test_catches_the_s103_line_number_bug``: it
reconstructs the ACTUAL bug the guard exists to prevent (S103's
``DATA.md line ~308``, correct on 2026-07-09 and ~240 lines off by 2026-08-09)
and asserts the guard fails on it. A guard that has never been shown to fail is
not evidence of anything.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from check_doc_citations import (  # noqa: E402
    EXIT_DRIFT,
    EXIT_OK,
    check_citations,
    doc_sections,
    main,
)


def _tree(tmp_path: Path, cited: str) -> Path:
    """A minimal repo: one doc with numbered sections, one module citing it."""
    (tmp_path / "data").mkdir(exist_ok=True)
    (tmp_path / "data" / "DATA.md").write_text(
        "# Data Sources\n\n"
        "## 2. Property Info Dataset\n\nLot size and zoning.\n\n"
        "## 5. Zoning Bylaw Geographical Data\n\n"
        "- **Set-aside categories:** never = River Valley; Institutional\n"
        "  (`UI`,`UF`,`AJ`,`PU`) is a proxy for exempt-roll understatement.\n"
    )
    (tmp_path / "src").mkdir(exist_ok=True)
    (tmp_path / "src" / "mod.py").write_text(f"# Institutional codes ({cited}).\nX = 1\n")
    return tmp_path


# --- the bug this guard exists to prevent ------------------------------------

def test_catches_the_s103_line_number_bug(tmp_path):
    """A line-number citation FAILS even when the line still exists in the doc."""
    failures, _ = check_citations(_tree(tmp_path, "DATA.md line ~308"))
    assert len(failures) == 1
    assert "LINE NUMBER" in failures[0]
    assert "src/mod.py:1" in failures[0]


def test_the_corrected_form_passes(tmp_path):
    """The fix S103 actually applied — cite the section, not the line."""
    failures, _ = check_citations(_tree(tmp_path, 'DATA.md §5, "Set-aside categories"'))
    assert failures == []


def test_line_number_banned_regardless_of_doc_length(tmp_path):
    """Not validated against the doc — banned. It drifts silently and plausibly."""
    root = _tree(tmp_path, "DATA.md line 3")  # line 3 exists and is real content
    failures, _ = check_citations(root)
    assert len(failures) == 1
    assert "LINE NUMBER" in failures[0]


# --- section resolution ------------------------------------------------------

def test_catches_a_section_that_does_not_exist(tmp_path):
    failures, _ = check_citations(_tree(tmp_path, "DATA.md §9"))
    assert len(failures) == 1
    assert "§9" in failures[0] and "no such section" in failures[0]


def test_accepts_a_subsection_of_a_real_section(tmp_path):
    """``§0.1`` resolves when the doc numbers its subsections that way."""
    root = _tree(tmp_path, "DATA.md §2")
    (root / "data" / "DATA.md").write_text("# D\n\n### 2.1 A subsection\n")
    failures, _ = check_citations(root)
    assert failures == []


def test_doc_sections_parses_the_projects_heading_forms():
    tmp = Path(__file__).parent / "_sections_probe.md"
    tmp.write_text(
        "## 5. Zoning\n### 0.1 The defect map\n## 6b. Round 2\n## Name Matching\n"
    )
    try:
        assert doc_sections(tmp) == {"5", "0.1", "6b"}
    finally:
        tmp.unlink()


# --- the false positives that shaped the parser -------------------------------

def test_a_phase_is_not_a_section(tmp_path):
    """``ARCHITECTURE.md Phase 2 notes`` is a project milestone, not a heading."""
    root = _tree(tmp_path, "DATA.md Phase 2 notes")
    failures, _ = check_citations(root)
    assert failures == []


def test_short_doc_names_need_the_md_suffix(tmp_path):
    """``UI`` is an Urban Institution zone code long before it is UI.md."""
    root = _tree(tmp_path, "x")
    (root / "docs").mkdir()
    (root / "docs" / "UI.md").write_text("# UI\n\n## 1. Layout\n")
    (root / "src" / "mod.py").write_text('# zoning `UI` "university/hospital" split\nX = 1\n')
    _, warnings = check_citations(root)
    assert warnings == []


def test_a_quoted_citation_is_a_mention_not_a_use(tmp_path):
    """Prose ABOUT the banned form (as in the audit ledger) must not fail."""
    root = _tree(tmp_path, "x")
    (root / "src" / "mod.py").write_text(
        '# The comment said "DATA.md line ~308", which drifted 240 lines.\nX = 1\n'
    )
    failures, _ = check_citations(root)
    assert failures == []


# --- warnings (never fail the build) -----------------------------------------

def test_missing_doc_warns_but_does_not_fail(tmp_path):
    root = _tree(tmp_path, "x")
    (root / "src" / "mod.py").write_text("# Read SPEC_nothing.md first.\nX = 1\n")
    failures, warnings = check_citations(root)
    assert failures == []
    assert any("does not exist" in w for w in warnings)


def test_quoted_title_absent_from_doc_warns(tmp_path):
    failures, warnings = check_citations(_tree(tmp_path, 'DATA.md "Fire lens"'))
    assert failures == []
    assert any("Fire lens" in w for w in warnings)


# --- the live repo -----------------------------------------------------------

def test_live_repo_citations_all_resolve():
    """The real check: every citation in this repo resolves right now."""
    failures, _ = check_citations()
    assert failures == [], "\n".join(failures)


def test_main_exit_codes(tmp_path):
    assert main(["--root", str(_tree(tmp_path, "DATA.md §5"))]) == EXIT_OK
    assert main(["--root", str(_tree(tmp_path, "DATA.md line ~308"))]) == EXIT_DRIFT
