import json
import sys

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, "src")
from export_value_grid import (
    SQ_M_PER_ACRE,
    build_hood_lot_acres,
    build_value_grid,
    check_lot_acre_bounds,
    export_value_grid,
)

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


# --- lot-acre denominator variant (docs/FINDINGS_lot_dedupe.md) -------------


def test_lot_acre_dedupes_duplicated_parcel():
    # Duplicated-parcel regime: every unit repeats a PARCEL-SIZED value
    # (>= SHARE_MAX_M2) — counted once.
    df = _frame([
        {**A, "assessed_value": 100.0, "lot_size": 5000.0},
        {**A, "assessed_value": 200.0, "lot_size": 5000.0},
    ])
    grid = build_value_grid(df, cell_m=100.0)
    lot_acres = 5000.0 / SQ_M_PER_ACRE
    assert grid.iloc[0]["value_per_lot_acre"] == pytest.approx(300.0 / lot_acres)


def test_lot_acre_sums_identical_small_shares():
    # Identical apportioned shares (< SHARE_MAX_M2) are real land per unit —
    # the townhouse-complex regime a plain distinct-sum collapses
    # (FINDINGS_lot_dedupe §4.3).
    df = _frame([
        {**A, "assessed_value": 100.0, "lot_size": 150.0},
        {**A, "assessed_value": 100.0, "lot_size": 150.0},
        {**A, "assessed_value": 100.0, "lot_size": 150.0},
    ])
    grid = build_value_grid(df, cell_m=100.0)
    lot_acres = 450.0 / SQ_M_PER_ACRE
    assert grid.iloc[0]["value_per_lot_acre"] == pytest.approx(300.0 / lot_acres)


def test_lot_acre_sums_apportioned_shares():
    # Apportioned regime: differing per-unit shares all count.
    df = _frame([
        {**A, "assessed_value": 100.0, "lot_size": 300.0},
        {**A, "assessed_value": 200.0, "lot_size": 200.0},
    ])
    grid = build_value_grid(df, cell_m=100.0)
    lot_acres = 500.0 / SQ_M_PER_ACRE
    assert grid.iloc[0]["value_per_lot_acre"] == pytest.approx(300.0 / lot_acres)


def test_lot_acre_sums_across_points_in_cell():
    # Two separate parcels in one cell: deduped per point, summed per cell.
    df = _frame([
        {**A, "assessed_value": 100.0, "lot_size": 400.0},
        {**A2, "assessed_value": 200.0, "lot_size": 600.0},
    ])
    grid = build_value_grid(df, cell_m=100.0)
    lot_acres = 1000.0 / SQ_M_PER_ACRE
    assert grid.iloc[0]["value_per_lot_acre"] == pytest.approx(300.0 / lot_acres)


def test_majority_null_point_ineligible_and_reported(caplog):
    # >1 unit and >50% null lot_size: excluded from the lot-acre numerator
    # AND denominator (understated land would fake a needle), reported.
    df = _frame([
        {**A, "assessed_value": 100.0, "lot_size": 250.0},
        {**A, "assessed_value": 200.0, "lot_size": None},
        {**A, "assessed_value": 300.0, "lot_size": None},
        {**B, "assessed_value": 50.0, "lot_size": 100.0},
    ])
    with caplog.at_level("WARNING"):
        grid = build_value_grid(df, cell_m=100.0)
    assert "lot-ineligible" in caplog.text
    cell_a = grid[grid["value_per_acre"] > grid["value_per_acre"].min()].iloc[0]
    assert pd.isna(cell_a["value_per_lot_acre"])  # no eligible acres in A's cell
    # ground-acre metric keeps the full dollars regardless
    cell_acres = 100.0 * 100.0 / SQ_M_PER_ACRE
    assert cell_a["value_per_acre"] == pytest.approx(600.0 / cell_acres)


def test_half_null_point_stays_eligible():
    # Exactly 50% null is NOT majority-null — the point stays in.
    df = _frame([
        {**A, "assessed_value": 100.0, "lot_size": 250.0},
        {**A, "assessed_value": 200.0, "lot_size": None},
    ])
    grid = build_value_grid(df, cell_m=100.0)
    lot_acres = 250.0 / SQ_M_PER_ACRE
    assert grid.iloc[0]["value_per_lot_acre"] == pytest.approx(300.0 / lot_acres)


def test_zero_lot_size_treated_as_null():
    df = _frame([
        {**A, "assessed_value": 100.0, "lot_size": 0.0},
    ])
    grid = build_value_grid(df, cell_m=100.0)
    assert pd.isna(grid.iloc[0]["value_per_lot_acre"])


def test_no_lot_column_omits_lot_metrics():
    df = _frame([{**A, "assessed_value": 100.0}])
    grid = build_value_grid(df)
    assert "value_per_lot_acre" not in grid.columns


def test_lot_revenue_uses_eligible_levy():
    df = _frame([
        {**A, "assessed_value": 100.0, "levy": 1.0, "lot_size": 500.0},
        {**B, "assessed_value": 400.0, "levy": 4.0, "lot_size": None},
    ])
    grid = build_value_grid(df, cell_m=100.0)
    lot_acres = 500.0 / SQ_M_PER_ACRE
    ok = grid[grid["value_per_lot_acre"].notna()].iloc[0]
    assert ok["revenue_per_lot_acre"] == pytest.approx(1.0 / lot_acres)


# --- residential-revenue subset (apply_tax_rates res_levy) ------------------


def test_res_revenue_grid_columns():
    # res_levy sums per cell like levy; a cell with no residential-class levy
    # reads a real 0, not null. Lot-acre variant uses the eligible subset.
    df = _frame([
        {**A, "assessed_value": 100.0, "levy": 1.0, "res_levy": 1.0, "lot_size": 500.0},
        {**A2, "assessed_value": 200.0, "levy": 2.0, "res_levy": 0.5, "lot_size": 500.0},
        {**B, "assessed_value": 400.0, "levy": 4.0, "res_levy": 0.0, "lot_size": 250.0},
    ])
    grid = build_value_grid(df, cell_m=100.0)
    cell_acres = 100.0 * 100.0 / SQ_M_PER_ACRE
    res = sorted(grid["res_revenue_per_acre"])
    assert res == pytest.approx(sorted([1.5 / cell_acres, 0.0]))
    cell_a = grid[grid["res_revenue_per_acre"] > 0].iloc[0]
    lot_acres = 1000.0 / SQ_M_PER_ACRE
    assert cell_a["res_revenue_per_lot_acre"] == pytest.approx(1.5 / lot_acres)


def test_res_revenue_lot_uses_eligible_subset():
    # The lot-acre res metric excludes ineligible points' dollars, exactly
    # like value/revenue; the ground-acre res metric keeps them.
    df = _frame([
        {**A, "assessed_value": 100.0, "levy": 1.0, "res_levy": 1.0, "lot_size": 500.0},
        {**B, "assessed_value": 400.0, "levy": 4.0, "res_levy": 4.0, "lot_size": None},
    ])
    grid = build_value_grid(df, cell_m=100.0)
    lot_acres = 500.0 / SQ_M_PER_ACRE
    ok = grid[grid["res_revenue_per_lot_acre"].notna()].iloc[0]
    assert ok["res_revenue_per_lot_acre"] == pytest.approx(1.0 / lot_acres)
    cell_acres = 100.0 * 100.0 / SQ_M_PER_ACRE
    bad = grid[grid["res_revenue_per_lot_acre"].isna()].iloc[0]
    assert bad["res_revenue_per_acre"] == pytest.approx(4.0 / cell_acres)


def test_no_res_levy_omits_res_columns():
    df = _frame([{**A, "assessed_value": 100.0, "levy": 1.0, "lot_size": 500.0}])
    grid = build_value_grid(df)
    assert "res_revenue_per_acre" not in grid.columns
    assert "res_revenue_per_lot_acre" not in grid.columns


def _bounds_frame(rows):
    return _frame([{**r, "neighbourhood_name": r.get("neighbourhood_name", "H1")} for r in rows])


def test_bound_check_passes_within_boundary():
    df = _bounds_frame([
        {**A, "assessed_value": 100.0, "lot_size": 2000.0},
    ])
    boundaries = pd.DataFrame([
        {"neighbourhood_name": "H1", "area_acres": 1.0},  # 2000 m2 ~ 0.49 ac
    ])
    ratios = check_lot_acre_bounds(df, boundaries)
    assert ratios.iloc[0]["ratio"] == pytest.approx(2000.0 / SQ_M_PER_ACRE, rel=1e-6)


def test_bound_check_raises_on_new_violation():
    df = _bounds_frame([
        {**A, "assessed_value": 100.0, "lot_size": 9000.0},  # ~2.2 ac in a 1 ac hood
    ])
    boundaries = pd.DataFrame([
        {"neighbourhood_name": "H1", "area_acres": 1.0},
    ])
    with pytest.raises(RuntimeError, match="H1"):
        check_lot_acre_bounds(df, boundaries)


def test_bound_check_allows_known_outlier():
    df = _bounds_frame([
        {**A, "assessed_value": 100.0, "lot_size": 9000.0, "neighbourhood_name": "PEMBINA"},
    ])
    boundaries = pd.DataFrame([
        {"neighbourhood_name": "PEMBINA", "area_acres": 1.0},
    ])
    ratios = check_lot_acre_bounds(df, boundaries)  # must not raise
    assert ratios.iloc[0]["ratio"] > 1.0


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
    assert stats["has_lot"] is False


def test_export_lot_columns_and_nulls(tmp_path):
    df = _frame([
        {**A, "assessed_value": 100.0, "levy": 1.0, "lot_size": 500.0},
        {**B, "assessed_value": 400.0, "levy": 4.0, "lot_size": None},  # no eligible acres
    ])
    out = tmp_path / "value_grid.json"
    stats = export_value_grid(df, out, cell_m=100.0)
    payload = json.loads(out.read_text())
    assert payload["columns"] == [
        "lon", "lat", "value_per_acre", "revenue_per_acre",
        "value_per_lot_acre", "revenue_per_lot_acre",
    ]
    rows = {tuple(r[:2]): r for r in payload["cells"]}
    lot_vals = sorted((r[4] for r in payload["cells"]), key=lambda v: (v is None, v))
    assert None in lot_vals  # B's cell has no eligible lot acres -> null slots
    lot_acres = 500.0 / SQ_M_PER_ACRE
    assert round(100.0 / lot_acres) in lot_vals
    assert stats["has_lot"] is True
    assert stats["n_cells_without_lot"] == 1


def test_export_res_columns_appended(tmp_path):
    # res columns append AFTER the existing six (stable prefix, old files
    # diffable); lot slot null where the cell has no eligible lot acres.
    df = _frame([
        {**A, "assessed_value": 100.0, "levy": 1000.0, "res_levy": 1000.0, "lot_size": 500.0},
        {**B, "assessed_value": 400.0, "levy": 4000.0, "res_levy": 0.0, "lot_size": None},
    ])
    out = tmp_path / "value_grid.json"
    stats = export_value_grid(df, out, cell_m=100.0)
    payload = json.loads(out.read_text())
    assert payload["columns"] == [
        "lon", "lat", "value_per_acre", "revenue_per_acre",
        "value_per_lot_acre", "revenue_per_lot_acre",
        "res_revenue_per_acre", "res_revenue_per_lot_acre",
    ]
    assert stats["has_res"] is True
    lot_acres = 500.0 / SQ_M_PER_ACRE
    res_rows = sorted(payload["cells"], key=lambda r: r[6])
    assert res_rows[0][6] == 0 and res_rows[0][7] is None   # B: no res, no lot
    assert res_rows[1][6] > 0
    assert res_rows[1][7] == round(1000.0 / lot_acres)


def test_export_res_without_lot(tmp_path):
    # res_levy present but no lot_size: only the ground-acre res column ships.
    df = _frame([{**A, "assessed_value": 100.0, "levy": 1.0, "res_levy": 1.0}])
    out = tmp_path / "value_grid.json"
    export_value_grid(df, out, cell_m=100.0)
    payload = json.loads(out.read_text())
    assert payload["columns"] == [
        "lon", "lat", "value_per_acre", "revenue_per_acre", "res_revenue_per_acre",
    ]
    assert len(payload["cells"][0]) == 5


# --- build_hood_lot_acres (neighbourhood lot-acre denominator) --------------

def test_hood_lot_acres_basic_rollup():
    # HoodX: one point, 1-acre lot, $1000 / $10 levy. HoodY: one point, 2-acre
    # lot, $500 / $5. Deduped lot acres and eligible dollars roll up per hood.
    df = _frame([
        {**A, "neighbourhood_name": "HOODX", "lot_size": SQ_M_PER_ACRE,
         "assessed_value": 1000.0, "levy": 10.0},
        {**B, "neighbourhood_name": "HOODY", "lot_size": 2 * SQ_M_PER_ACRE,
         "assessed_value": 500.0, "levy": 5.0},
    ])
    out = build_hood_lot_acres(df).set_index("neighbourhood_name")
    assert out.loc["HOODX", "lot_acres_eligible"] == pytest.approx(1.0)
    assert out.loc["HOODX", "value_lot_eligible"] == pytest.approx(1000.0)
    assert out.loc["HOODX", "revenue_lot_eligible"] == pytest.approx(10.0)
    assert out.loc["HOODY", "lot_acres_eligible"] == pytest.approx(2.0)
    assert out.loc["HOODY", "value_lot_eligible"] == pytest.approx(500.0)


def test_hood_lot_acres_dedupes_duplicated_parcel():
    # Two condo units at ONE point sharing a duplicated 5000 m² lot (>= SHARE_MAX
    # -> counted once), each separately assessed: land counts once, dollars sum.
    df = _frame([
        {**A, "neighbourhood_name": "HOODX", "lot_size": 5000.0, "assessed_value": 100.0},
        {**A, "neighbourhood_name": "HOODX", "lot_size": 5000.0, "assessed_value": 200.0},
    ])
    out = build_hood_lot_acres(df).set_index("neighbourhood_name")
    assert out.loc["HOODX", "lot_acres_eligible"] == pytest.approx(5000.0 / SQ_M_PER_ACRE)
    assert out.loc["HOODX", "value_lot_eligible"] == pytest.approx(300.0)
    assert "revenue_lot_eligible" not in out.columns  # no levy passed


def test_hood_lot_acres_res_revenue_variant():
    # res_levy (the residential-class subset) rolls up alongside levy into
    # res_revenue_lot_eligible; absent when res_levy isn't passed (test above).
    df = _frame([
        {**A, "neighbourhood_name": "HOODX", "lot_size": SQ_M_PER_ACRE,
         "assessed_value": 1000.0, "levy": 10.0, "res_levy": 4.0},
        {**B, "neighbourhood_name": "HOODX", "lot_size": SQ_M_PER_ACRE,
         "assessed_value": 500.0, "levy": 5.0, "res_levy": 0.0},
    ])
    out = build_hood_lot_acres(df).set_index("neighbourhood_name")
    assert out.loc["HOODX", "revenue_lot_eligible"] == pytest.approx(15.0)
    assert out.loc["HOODX", "res_revenue_lot_eligible"] == pytest.approx(4.0)


def test_hood_lot_acres_excludes_ineligible_points():
    # A majority-null multi-unit point is ineligible: excluded from BOTH the
    # denominator and the numerator (its value must not inflate value/lot-acre).
    df = _frame([
        {**A, "neighbourhood_name": "HOODX", "lot_size": SQ_M_PER_ACRE, "assessed_value": 100.0},
        {**B, "neighbourhood_name": "HOODX", "lot_size": None, "assessed_value": 900.0},
        {**B, "neighbourhood_name": "HOODX", "lot_size": None, "assessed_value": 900.0},
        {**B, "neighbourhood_name": "HOODX", "lot_size": 300.0, "assessed_value": 900.0},
    ])
    out = build_hood_lot_acres(df).set_index("neighbourhood_name")
    # Only point A (1 acre, $100) is eligible; the majority-null B point drops.
    assert out.loc["HOODX", "lot_acres_eligible"] == pytest.approx(1.0)
    assert out.loc["HOODX", "value_lot_eligible"] == pytest.approx(100.0)


# --- FAR (Development Lens B built floor-area ratio) ------------------------

def test_hood_lot_acres_far_basic():
    # One point, 1-acre lot, 2000 m² of floor area -> FAR = 2000 / 4046.86 m².
    df = _frame([
        {**A, "neighbourhood_name": "HOODX", "lot_size": SQ_M_PER_ACRE,
         "assessed_value": 1000.0, "gross_area": 2000.0},
    ])
    out = build_hood_lot_acres(df).set_index("neighbourhood_name")
    assert out.loc["HOODX", "far"] == pytest.approx(2000.0 / SQ_M_PER_ACRE)


def test_hood_lot_acres_far_sums_floor_area_over_deduped_land():
    # Two condo units at ONE point: land is a duplicated 5000 m² parcel (counted
    # ONCE), but each unit carries its own floor area (summed) -> FAR uses the
    # per-unit floor-area sum over the deduped land.
    df = _frame([
        {**A, "neighbourhood_name": "HOODX", "lot_size": 5000.0,
         "assessed_value": 100.0, "gross_area": 120.0},
        {**A, "neighbourhood_name": "HOODX", "lot_size": 5000.0,
         "assessed_value": 200.0, "gross_area": 130.0},
    ])
    out = build_hood_lot_acres(df).set_index("neighbourhood_name")
    assert out.loc["HOODX", "far"] == pytest.approx((120.0 + 130.0) / 5000.0)


def test_hood_lot_acres_omits_far_without_gross_area():
    # Backward-compat: no gross_area column -> no far column emitted.
    df = _frame([
        {**A, "neighbourhood_name": "HOODX", "lot_size": SQ_M_PER_ACRE,
         "assessed_value": 1000.0},
    ])
    out = build_hood_lot_acres(df)
    assert "far" not in out.columns
