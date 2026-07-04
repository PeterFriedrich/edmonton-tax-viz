import json
import sys

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, "src")
from export_value_grid import SQ_M_PER_ACRE, build_value_grid, export_value_grid

# Two points well inside Edmonton, far enough apart (~1.1 km) to always land
# in different 100 m cells; two more within ~10 m of the first to always share
# its cell. Synthetic values chosen for easy sums.
A = dict(latitude=53.5200, longitude=-113.5000)
A2 = dict(latitude=53.52005, longitude=-113.50005)
B = dict(latitude=53.5300, longitude=-113.5000)


def _frame(rows):
    return pd.DataFrame(rows)


def test_same_cell_sums_and_different_cells_split():
    df = _frame([
        {**A, "assessed_value": 100.0, "levy": 1.0},
        {**A2, "assessed_value": 200.0, "levy": 2.0},
        {**B, "assessed_value": 400.0, "levy": 4.0},
    ])
    grid = build_value_grid(df, cell_m=100.0)
    assert len(grid) == 2
    cell_acres = 100.0 * 100.0 / SQ_M_PER_ACRE
    vals = sorted(grid["value_per_acre"])
    assert vals == pytest.approx(sorted([300.0 / cell_acres, 400.0 / cell_acres]))
    revs = sorted(grid["revenue_per_acre"])
    assert revs == pytest.approx(sorted([3.0 / cell_acres, 4.0 / cell_acres]))


def test_conserves_totals():
    rng = np.random.default_rng(7)
    n = 500
    df = _frame({
        "latitude": 53.52 + rng.uniform(0, 0.05, n),
        "longitude": -113.50 + rng.uniform(0, 0.05, n),
        "assessed_value": rng.uniform(1e5, 1e6, n),
        "levy": rng.uniform(1e2, 1e4, n),
    })
    grid = build_value_grid(df, cell_m=100.0)
    cell_acres = 100.0 * 100.0 / SQ_M_PER_ACRE
    assert (grid["value_per_acre"] * cell_acres).sum() == pytest.approx(df["assessed_value"].sum())
    assert (grid["revenue_per_acre"] * cell_acres).sum() == pytest.approx(df["levy"].sum())


def test_value_only_path_omits_revenue():
    df = _frame([{**A, "assessed_value": 100.0}])
    grid = build_value_grid(df)
    assert "revenue_per_acre" not in grid.columns


def test_null_coordinates_excluded_not_crashed(caplog):
    df = _frame([
        {**A, "assessed_value": 100.0},
        {"latitude": None, "longitude": None, "assessed_value": 900.0},
    ])
    with caplog.at_level("WARNING"):
        grid = build_value_grid(df)
    assert len(grid) == 1
    assert "null coordinates" in caplog.text


def test_corner_is_wgs84_near_input():
    # The SW corner must land within one cell diagonal of the input point.
    df = _frame([{**A, "assessed_value": 100.0}])
    grid = build_value_grid(df, cell_m=100.0)
    assert grid.iloc[0]["lon"] == pytest.approx(A["longitude"], abs=0.01)
    assert grid.iloc[0]["lat"] == pytest.approx(A["latitude"], abs=0.01)


def test_large_lot_spreads_across_cells():
    # One property with a 300 m-square lot (9 ha) must occupy multiple cells,
    # not one needle — and still conserve its total exactly.
    df = _frame([{**A, "assessed_value": 9e6, "levy": 9e4, "lot_size_m2": 90_000.0}])
    grid = build_value_grid(df, cell_m=100.0)
    assert len(grid) >= 9  # a 300 m square covers at least a 3x3 cell block
    cell_acres = 100.0 * 100.0 / SQ_M_PER_ACRE
    assert (grid["value_per_acre"] * cell_acres).sum() == pytest.approx(9e6)
    assert (grid["revenue_per_acre"] * cell_acres).sum() == pytest.approx(9e4)
    # No single cell holds more than the footprint's per-cell share (a full
    # interior cell's worth) — the needle is gone.
    assert grid["value_per_acre"].max() <= (9e6 / 9 / cell_acres) * (1 + 1e-9)


def test_small_and_null_lots_stay_point_binned():
    df = _frame([
        {**A, "assessed_value": 100.0, "lot_size_m2": 500.0},   # typical lot
        {**B, "assessed_value": 200.0, "lot_size_m2": None},    # null lot
    ])
    grid = build_value_grid(df, cell_m=100.0)
    assert len(grid) == 2  # one cell each — no spreading


def test_spread_and_binned_mix_conserves():
    df = _frame([
        {**A, "assessed_value": 9e6, "levy": 9e4, "lot_size_m2": 90_000.0},
        {**B, "assessed_value": 100.0, "levy": 1.0, "lot_size_m2": 500.0},
    ])
    grid = build_value_grid(df, cell_m=100.0)
    cell_acres = 100.0 * 100.0 / SQ_M_PER_ACRE
    assert (grid["value_per_acre"] * cell_acres).sum() == pytest.approx(9e6 + 100.0)
    assert (grid["revenue_per_acre"] * cell_acres).sum() == pytest.approx(9e4 + 1.0)


def test_export_writes_compact_json(tmp_path):
    df = _frame([
        {**A, "assessed_value": 100.0, "levy": 1.0},
        {**B, "assessed_value": 400.0, "levy": 4.0},
    ])
    out = tmp_path / "value_grid.json"
    stats = export_value_grid(df, out, cell_m=100.0)
    payload = json.loads(out.read_text())
    assert payload["cell_m"] == 100.0
    assert payload["columns"] == ["lon", "lat", "value_per_acre", "revenue_per_acre"]
    assert len(payload["cells"]) == 2 == stats["n_cells"]
    for row in payload["cells"]:
        assert len(row) == 4
        assert isinstance(row[2], int) and isinstance(row[3], int)  # whole dollars
    assert stats["has_revenue"] is True
