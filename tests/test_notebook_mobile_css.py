"""Every published evidence notebook must be readable on a phone.

nbconvert's lab template lays the input area out as `display: table-cell` with
`overflow: hidden` and puts nothing scrollable inside it. A code line wider than
the viewport is therefore **clipped, not scrolled** — no horizontal scroll
affordance exists to find, on touch or anywhere else. Measured 2026-09-20 at
390px: **54 of 54 code cells across all five published reports** lost up to
561px of every line. At 1280px none were clipped, which is why it survived —
the defect is invisible at the width the reports were rendered and reviewed at.

These reports are the public evidence for `docs/DATA_ISSUES.md`, linked from the
README and meant to be handed to someone. Half a code line is not evidence.

`tools/inject_notebook_mobile_css.py` adds the wrap rule. This test is the part
that survives a re-render: the HTML is a generated artifact, so the next person
to run nbconvert over a notebook gets the stock template back and would ship the
clipping again with nothing to notice it.
"""

import pathlib

import pytest

NOTEBOOK_DIR = pathlib.Path(__file__).resolve().parents[1] / "web" / "notebooks"
MARKER = "mobile-code-wrap"

REPORTS = sorted(p for p in NOTEBOOK_DIR.glob("*.html") if p.name != "index.html")


def test_reports_exist():
    """Guard the guard: an empty glob would make every test below vacuous."""
    assert len(REPORTS) >= 5, f"expected the five published reports, found {REPORTS}"


@pytest.mark.parametrize("report", REPORTS, ids=lambda p: p.name)
def test_code_cells_wrap(report: pathlib.Path):
    html = report.read_text(encoding="utf-8")
    assert MARKER in html, (
        f"{report.name} is missing the mobile-wrap block — code cells will be "
        f"clipped on narrow screens. Run: "
        f"python tools/inject_notebook_mobile_css.py"
    )
    # The rule, not just the comment: a marker with an empty block would pass
    # the check above while shipping the defect.
    block = html.split(MARKER, 1)[1].split("/mobile-code-wrap", 1)[0]
    assert "white-space: pre-wrap" in block, (
        f"{report.name} carries the marker but not the wrap rule"
    )


@pytest.mark.parametrize("report", REPORTS, ids=lambda p: p.name)
def test_output_tables_scroll(report: pathlib.Path):
    """Wide dataframes must be reachable too — the same defect, one level up.

    `.jp-OutputArea-child` is `display: table; overflow: hidden`, so a dataframe
    wider than the column loses its right-hand columns. Missed on the first
    pass because the check was written against `.jp-OutputArea-output` and its
    children, where the clipping cannot appear.

    ⚠️ The template LOOKS like it handles this: `.jp-RenderedHTMLCommon` carries
    `overflow-x: auto`. It is `display: table-row`, where overflow is inert —
    so the declaration scrolls nothing. Tables scroll rather than wrap, because
    wrapping a dataframe destroys what it is showing.
    """
    html = report.read_text(encoding="utf-8")
    block = html.split(MARKER, 1)[1].split("/mobile-code-wrap", 1)[0]
    assert ".jp-RenderedHTMLCommon table" in block, (
        f"{report.name} has no table rule — a wide dataframe will be clipped"
    )
    assert "overflow-x: auto" in block, (
        f"{report.name} carries the table selector but nothing that scrolls"
    )
