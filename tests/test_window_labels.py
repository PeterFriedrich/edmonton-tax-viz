"""Guard: web/index.html's WINDOWS block agrees with main.py's year pins.

Audit F4 (2026-08-28): the activity windows are pinned in `main.py` and bumped
BY HAND each January (docs/RUNBOOK.md §1 step 4) so a partial year is never
averaged or summed in. The bump rolled the numbers; ~15 user-facing labels in
`web/index.html` restated the same ranges as literals and did not roll with
them. Nothing caught it — the drift guards in `load_fire`/`load_permits` and
`vintage_report.check_window_pins` all watch the PIN, not the copy.

The fix put every label behind one `WINDOWS` block. These tests are the half of
it that makes drift loud: `WINDOWS` must equal the pins, and no user-facing
string may go back to spelling a range out.

**On halting the weekly refresh.** `pytest` is refresh.yml's guard step, so a
red test stops the data pipeline — `tests/test_codemap.py` argues at length why
a docs artifact must never do that. This one is different in the way that
matters: nothing the refresh does can turn it red. Both sides are hand-edited
constants, so it can only fail inside a PR where someone bumped `main.py` and
not the labels — which is precisely the state that must not reach the site.
"""
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

INDEX = ROOT / "web/index.html"


def _cells_block():
    """Parse the `CELLS = { ... }` object literal into {key: metres}."""
    src = INDEX.read_text(encoding="utf-8")
    m = re.search(r"const CELLS = \{(.*?)\n    \};", src, re.S)
    assert m, "CELLS block not found in web/index.html — did it get renamed?"
    pairs = re.findall(r"(\w+):\s*(\d+),", m.group(1))
    assert pairs, "CELLS block parsed but held no entries"
    return {k: int(v) for k, v in pairs}


def _windows_block():
    """Parse the `WINDOWS = { ... }` object literal into {key: (start, end)}."""
    src = INDEX.read_text(encoding="utf-8")
    m = re.search(r"const WINDOWS = \{(.*?)\n    \};", src, re.S)
    assert m, "WINDOWS block not found in web/index.html — did it get renamed?"
    pairs = re.findall(r"(\w+):\s*\[(\d{4}),\s*(\d{4})\]", m.group(1))
    assert pairs, "WINDOWS block parsed but held no [start, end] entries"
    return {k: (int(a), int(b)) for k, a, b in pairs}


@pytest.fixture(scope="module")
def windows():
    return _windows_block()


@pytest.fixture(scope="module")
def cells():
    return _cells_block()


@pytest.fixture(scope="module")
def pins():
    import main  # heavy import, and only this module needs it

    from src.load_temporal import FIRST_YEAR

    return main, FIRST_YEAR


def test_permit_and_fire_windows_match_main_pins(windows, pins):
    main, _ = pins
    expected = {
        "fire": (main.FIRE_YEARS[0], main.FIRE_YEARS[-1]),
        "permits": (main.PERMIT_YEARS[0], main.PERMIT_YEARS[-1]),
        "permitsRecent": (main.PERMIT_YEARS_RECENT[0], main.PERMIT_YEARS_RECENT[-1]),
        "permitsLong": (main.PERMIT_YEARS_LONG[0], main.PERMIT_YEARS_LONG[-1]),
    }
    got = {k: windows[k] for k in expected}
    assert got == expected, (
        "web/index.html WINDOWS disagrees with main.py's pins. Bump the WINDOWS "
        "block to match (docs/RUNBOOK.md §1 step 4) — every year range on the "
        f"page reads from it.\n  main.py: {expected}\n  index.html: {got}"
    )


def test_change_windows_end_at_the_assessment_year(windows, pins):
    """Both change windows end at the roll the map is showing; long starts at
    the first year of the assessment history."""
    main, first_year = pins
    assert windows["chgLong"] == (first_year, main.ASSESSMENT_YEAR)
    assert windows["chgShort"][1] == main.ASSESSMENT_YEAR
    assert first_year < windows["chgShort"][0] < main.ASSESSMENT_YEAR


def test_no_user_facing_string_spells_a_window_out(windows):
    """Every current range must appear only in WINDOWS itself.

    Comments are stripped first: they are allowed to mention a year (one
    describes an unrelated ASTER window that happens to share a range), and a
    stale comment is not the defect F4 is about. Anything surviving the strip is
    markup or a JS string — i.e. something a reader can see.
    """
    lines = INDEX.read_text(encoding="utf-8").splitlines()
    in_windows = False
    offenders = []
    for n, line in enumerate(lines, 1):
        if "const WINDOWS = {" in line:
            in_windows = True
        if in_windows:
            if line.strip() == "};":
                in_windows = False
            continue
        if line.lstrip().startswith("//"):
            continue
        code = re.sub(r"\s+//.*$", "", line)
        for key, (a, b) in windows.items():
            if f"{a}–{b}" in code:
                offenders.append(f"  line {n}: {key} ({a}–{b}) — {line.strip()[:90]}")
    assert not offenders, (
        "A year range is spelled out instead of read from WINDOWS. Use "
        "`${WIN.<key>}` in JS, or a {{<key>}} placeholder in static markup:\n"
        + "\n".join(offenders)
    )


def test_cell_sizes_match_main_pins(cells, pins):
    """The grid edges are pinned in main.py and restated as labels, which is
    exactly F4's shape. The Glass grid halved to 50 m on 2026-09-01; the
    Development grid did not, so they are two independent pins."""
    main, _ = pins
    expected = {
        "cellGlass": int(main.GRID_CELL_M),
        "cellDev": int(main.DEV_GRID_CELL_M),
    }
    got = {k: cells[k] for k in expected}
    assert got == expected, (
        "web/index.html CELLS disagrees with main.py. Every 'N m' on the page "
        f"reads from it.\n  main.py: {expected}\n  index.html: {got}"
    )


def test_no_user_facing_string_spells_a_cell_size_out(cells):
    """The failure this catches is silent and was live: a 50 m grid rendering
    under labels that still read '100 m'. Comments are stripped, same as the
    window check — a comment may legitimately narrate a past resolution."""
    lines = INDEX.read_text(encoding="utf-8").splitlines()
    sizes = set(cells.values())
    in_cells = False
    in_html_comment = False
    offenders = []
    for n, line in enumerate(lines, 1):
        if "const CELLS = {" in line:
            in_cells = True
        if in_cells:
            if line.strip() == "};":
                in_cells = False
            continue
        # HTML comment blocks are comments too — one of them narrates the 100 m
        # measurements this grid replaced, which is history, not a live label.
        if in_html_comment:
            if "-->" in line:
                in_html_comment = False
            continue
        if "<!--" in line and "-->" not in line:
            in_html_comment = True
            continue
        if line.lstrip().startswith("//"):
            continue
        code = re.sub(r"\s+//.*$", "", line)
        for size in sizes:
            if re.search(rf"\b{size} m\b(?! grid file)", code):
                offenders.append(f"  line {n}: {line.strip()[:90]}")
                break
    assert not offenders, (
        "A grid cell size is spelled out instead of read from CELLS. Use "
        "`${CELL.<key>}` in JS, or a {{<key>}} placeholder in static markup:\n"
        + "\n".join(offenders)
    )


def test_every_placeholder_names_a_real_token(windows, cells):
    """An unknown {{token}} survives substitution and reaches the screen.

    Two substitution targets: `title` attributes, and the text of elements
    marked `data-tok` (button labels, which are visible text rather than a
    tooltip). A token anywhere else is never substituted, which the second
    half checks.
    """
    src = INDEX.read_text(encoding="utf-8")
    known = set(windows) | set(cells)
    tokens = {t for attr in re.findall(r'title="([^"]*)"', src)
              for t in re.findall(r"\{\{(\w+)\}\}", attr)}
    tokens |= {t for ln in src.splitlines() if "data-tok" in ln
               for t in re.findall(r"\{\{(\w+)\}\}", ln)}
    assert tokens, "no {{token}} placeholders found — did the markup stop using them?"
    unknown = tokens - known
    assert not unknown, f"placeholders with no WINDOWS or CELLS key: {sorted(unknown)}"

    stray = [f"  line {n}: {ln.strip()[:90]}"
             for n, ln in enumerate(src.splitlines(), 1)
             if re.search(r"\{\{\w+\}\}", ln) and not ln.lstrip().startswith("//")
             and 'title="' not in ln and "data-tok" not in ln]
    assert not stray, (
        "a {{token}} outside a title attribute or a data-tok element is never "
        "substituted and reaches the screen raw:\n" + "\n".join(stray)
    )
