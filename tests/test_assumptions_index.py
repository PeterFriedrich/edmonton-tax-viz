"""docs/ASSUMPTIONS.md must list every premise the two machine-readable sources
name, and every file path it cites must exist. An index that silently misses
a new row is the failure it exists to prevent."""

import ast
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / "docs" / "ASSUMPTIONS.md").read_text()
STATUSES = {"VERIFIED", "SUPPORTED", "UNVERIFIED", "ACCEPTED"}


def _table_rows():
    return [l for l in INDEX.splitlines() if re.match(r"\| [AB]\d+ \|", l)]


def test_every_03_sizing_row_is_indexed():
    src = (ROOT / "notebooks" / "verified" / "03_assumptions.py").read_text()
    calls = [n for n in ast.walk(ast.parse(src))
             if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "row"]
    assert calls, "03_assumptions.py no longer calls row(); this test is reading the wrong thing"
    rows = _table_rows()
    for c in calls:
        lens = c.args[0].value
        where = c.args[5].value
        assert any(f"| {lens} |" in r and where in r for r in rows), (
            f"03_assumptions row ({lens!r}, cited {where!r}) at line {c.lineno} "
            "has no row in docs/ASSUMPTIONS.md")


def test_every_unestablished_cost_rate_is_indexed():
    costs = json.loads((ROOT / "data" / "city_unit_costs.json").read_text())
    open_rates = [k for k, v in costs.items()
                  if isinstance(v, dict) and "source_denominator" in v
                  and v["source_denominator"]["confidence"] not in ("ESTABLISHED", "N/A")]
    for key in open_rates:
        assert f"`{key}`" in INDEX, f"{key} is not ESTABLISHED but has no row in docs/ASSUMPTIONS.md"


def test_every_row_has_a_known_status():
    rows = _table_rows()
    assert len(rows) >= 10
    for r in rows:
        cells = [c.strip() for c in r.strip("|").split("|")]
        assert STATUSES & set(cells), f"no valid status in: {r}"


def test_cited_paths_exist():
    paths = set(re.findall(r"`((?:src|data|notebooks|scripts|tests|tools)/[\w./-]+)`", INDEX))
    assert paths
    missing = sorted(p for p in paths if not (ROOT / p).exists())
    assert not missing, f"docs/ASSUMPTIONS.md cites missing paths: {missing}"
