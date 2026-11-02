"""The register's live rows and the notebooks that source them stay in step.

`docs/REPORT_CLAIMS.md` gives a weekly-live figure a pointer, not a number; the
number reaches the report through `web/verified/REPORT_FIGURES.md`, which the
weekly run writes from each verified notebook's `REPORT_IDS`. These tests read
both sides statically, so a live row with no source fails at merge time rather
than on the next Monday run. The notebooks' own end-of-run check catches a
declared id that the run did not emit.
"""

import ast
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTER = ROOT / "docs" / "REPORT_CLAIMS.md"
NOTEBOOKS = sorted((ROOT / "notebooks" / "verified").glob("*.py"))


def _live_ids():
    ids = set()
    for line in REGISTER.read_text().splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and re.fullmatch(r"[A-Z]+\d+", cells[0]) and "**live**" in cells[-1]:
            ids.add(cells[0])
    return ids


def _declared():
    out = {}
    for nb in NOTEBOOKS:
        for node in ast.parse(nb.read_text()).body:
            if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "REPORT_IDS" for t in node.targets
            ):
                out[nb.stem] = set(ast.literal_eval(node.value))
    return out


def test_the_register_has_live_rows():
    # Guards the parser: a format change that matched nothing would pass the rest.
    assert len(_live_ids()) >= 5


def test_every_live_row_is_declared_by_exactly_one_notebook():
    declared = _declared()
    for rid in sorted(_live_ids()):
        pages = [stem for stem, ids in declared.items() if rid in ids]
        assert len(pages) == 1, (
            f"{rid} is marked **live** in REPORT_CLAIMS.md but is declared by {pages or 'no notebook'}; "
            f"add it to one verified notebook's REPORT_IDS with a figure() call, or re-tag the row as-of"
        )


def test_every_declared_id_is_a_live_row():
    live = _live_ids()
    for stem, ids in _declared().items():
        assert ids <= live, f"{stem} declares {sorted(ids - live)}, which the register does not mark **live**"


def test_every_declared_id_has_a_figure_call():
    for stem, ids in _declared().items():
        src = (ROOT / "notebooks" / "verified" / f"{stem}.py").read_text()
        missing = sorted(i for i in ids if f'figure("{i}"' not in src)
        assert not missing, f"{stem} declares {missing} but never calls figure() for them"


def _load_runner():
    import importlib.util

    sys.path.insert(0, str(ROOT / "tools"))
    spec = importlib.util.spec_from_file_location(
        "run_verified_notebooks", ROOT / "tools" / "run_verified_notebooks.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_render_orders_by_id_and_consumes_the_json(tmp_path):
    (tmp_path / "02_methods.figures.json").write_text(json.dumps(
        {"M10": [["size", "4.0%"]], "M3": [["multiple", "2.9×"]]}))
    (tmp_path / "04_roads_lens.figures.json").write_text(json.dumps(
        {"R9": [["outside", "0.31%"]], "D1": [["a", "21%"], ["b", "52%"]]}))
    md = _load_runner().render_report_figures(
        tmp_path, {"data_year": 2026, "rate_year": 2026, "generated": "2026-11-02"},
        "abc1234", "2026-11-02")
    rows = [l.split("|")[1].strip() for l in md.splitlines() if re.match(r"\| [A-Z]+\d+ ", l)]
    assert rows == ["D1", "D1", "M3", "M10", "R9"]
    assert "`abc1234`" in md and "Roll year 2026" in md
    assert not list(tmp_path.glob("*.figures.json"))
