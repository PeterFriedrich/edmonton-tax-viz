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


def test_share_coded_multi_unit_point_ineligible_and_reported(caplog):
    # The WESTMOUNT case, to scale: 3 records at one point whose lot_size values
    # are normalized ownership SHARES summing to 1.000, not m². Undetected this
    # made a 1 m² denominator and $3.48B/lot-acre — the tallest cell in the 50 m
    # grid, which anchors every other cell's height.
    df = _frame([
        {**A, "assessed_value": 469500.0, "lot_size": 0.505},
        {**A, "assessed_value": 185500.0, "lot_size": 0.218},
        {**A, "assessed_value": 204500.0, "lot_size": 0.277},
    ])
    with caplog.at_level("WARNING"):
        grid = build_value_grid(df, cell_m=50.0)
    assert "share-coded" in caplog.text
    assert pd.isna(grid.iloc[0]["value_per_lot_acre"])
    # ground acres are untouched — the dollars are real, only the lot area is not
    cell_acres = 50.0 * 50.0 / SQ_M_PER_ACRE
    assert grid.iloc[0]["value_per_acre"] == pytest.approx(859500.0 / cell_acres)


def test_single_record_tiny_lot_stays_eligible():
    # ⚠️ The floor is restricted to n > 1 ON PURPOSE. 381 real single-parcel
    # points hold genuinely tiny lots (median 8.4 m², median value $500 —
    # stalls, slivers) and produce unremarkable ratios. Widening the rule to
    # n == 1 would delete them for no gain.
    df = _frame([{**A, "assessed_value": 500.0, "lot_size": 8.4}])
    grid = build_value_grid(df, cell_m=50.0)
    lot_acres = 8.4 / SQ_M_PER_ACRE
    assert grid.iloc[0]["value_per_lot_acre"] == pytest.approx(500.0 / lot_acres)


def test_multi_unit_point_above_floor_stays_eligible():
    # A real multi-unit parcel just above the floor is kept — the rule must not
    # creep into ordinary small lots.
    df = _frame([
        {**A, "assessed_value": 100.0, "lot_size": 6.0},
        {**A, "assessed_value": 200.0, "lot_size": 6.0},
    ])
    grid = build_value_grid(df, cell_m=50.0)
    lot_acres = 12.0 / SQ_M_PER_ACRE  # repeated sub-SHARE_MAX value counts per unit
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


# --- stock-age column (load_property_info year_built) -----------------------


def test_median_year_built_per_cell():
    # Cell A: years 1950/1960/2000 -> median 1960. Cell B: single 2020.
    df = _frame([
        {**A, "assessed_value": 100.0, "year_built": 1950.0},
        {**A2, "assessed_value": 100.0, "year_built": 1960.0},
        {**A2, "assessed_value": 100.0, "year_built": 2000.0},
        {**B, "assessed_value": 400.0, "year_built": 2020.0},
    ])
    grid = build_value_grid(df, cell_m=100.0)
    assert sorted(grid["median_year_built"]) == pytest.approx([1960.0, 2020.0])


def test_year_built_median_skips_nulls_and_all_null_cell_is_nan():
    # Within a cell, null years are skipped (median over the known ones);
    # a cell with NO known year carries NaN — never 0 ("year 0" is not a
    # real zero the way $0 res levy is).
    df = _frame([
        {**A, "assessed_value": 100.0, "year_built": 1970.0},
        {**A2, "assessed_value": 100.0, "year_built": None},
        {**B, "assessed_value": 400.0, "year_built": None},
    ])
    grid = build_value_grid(df, cell_m=100.0)
    years = grid["median_year_built"]
    assert years.notna().sum() == 1
    assert years.dropna().iloc[0] == pytest.approx(1970.0)
    assert years.isna().sum() == 1


def test_year_built_median_robust_to_condo_repeats():
    # A multi-unit building repeats one year on every unit row (the DATA.md §2
    # duplication regimes) — the median of repeated identical values is that
    # value, so no dedupe machinery is needed for this column.
    df = _frame(
        [{**A, "assessed_value": 100.0, "year_built": 2005.0} for _ in range(50)]
        + [{**A2, "assessed_value": 100.0, "year_built": 1955.0}]
    )
    grid = build_value_grid(df, cell_m=100.0)
    assert grid.iloc[0]["median_year_built"] == pytest.approx(2005.0)


def test_no_year_built_column_omitted():
    df = _frame([{**A, "assessed_value": 100.0, "levy": 1.0}])
    grid = build_value_grid(df)
    assert "median_year_built" not in grid.columns


def test_export_year_column_appended_last(tmp_path):
    # median_year_built appends AFTER every existing column (stable prefix);
    # whole-year ints in the payload, null where the cell has no known year.
    df = _frame([
        {**A, "assessed_value": 100.0, "levy": 1000.0, "res_levy": 1000.0,
         "lot_size": 500.0, "year_built": 1975.0},
        {**B, "assessed_value": 400.0, "levy": 4000.0, "res_levy": 0.0,
         "lot_size": None, "year_built": None},
    ])
    out = tmp_path / "value_grid.json"
    stats = export_value_grid(df, out, cell_m=100.0)
    payload = json.loads(out.read_text())
    assert payload["columns"] == [
        "lon", "lat", "value_per_acre", "revenue_per_acre",
        "value_per_lot_acre", "revenue_per_lot_acre",
        "res_revenue_per_acre", "res_revenue_per_lot_acre",
        "median_year_built",
    ]
    assert stats["has_year"] is True
    assert stats["n_cells_without_year"] == 1
    years = sorted((r[8] for r in payload["cells"]), key=lambda v: (v is None, v))
    assert years[0] == 1975 and isinstance(years[0], int)
    assert years[1] is None


def test_export_year_without_lot_or_res(tmp_path):
    # year_built alone (older upstream): the column still ships, right after
    # the base columns.
    df = _frame([{**A, "assessed_value": 100.0, "year_built": 1990.0}])
    out = tmp_path / "value_grid.json"
    export_value_grid(df, out, cell_m=100.0)
    payload = json.loads(out.read_text())
    assert payload["columns"] == ["lon", "lat", "value_per_acre", "median_year_built"]
    assert payload["cells"][0][3] == 1990


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


def test_hood_lot_acres_far_is_nan_when_no_gross_area_recorded():
    # A hood whose eligible rows record NO floor area gets NaN, not 0.0 — absent
    # data and nothing-built are different claims, and far == 0 is the maximum
    # OPPORTUNITY end of the Infill scale, so a 0 here would read as a finding.
    df = _frame([
        {**A, "neighbourhood_name": "HOODX", "lot_size": SQ_M_PER_ACRE,
         "assessed_value": 1000.0, "gross_area": None},
        {**B, "neighbourhood_name": "HOODY", "lot_size": SQ_M_PER_ACRE,
         "assessed_value": 1000.0, "gross_area": 500.0},
    ])
    out = build_hood_lot_acres(df).set_index("neighbourhood_name")
    assert pd.isna(out.loc["HOODX", "far"])
    assert out.loc["HOODY", "far"] == pytest.approx(500.0 / SQ_M_PER_ACRE)


def test_hood_lot_acres_far_treats_zero_gross_area_as_missing():
    # ZERO is the other half of the same gap (DATA.md counts null AND zero as
    # "no floor area recorded"), so a hood of zeros is NaN too — not FAR 0.
    df = _frame([
        {**A, "neighbourhood_name": "HOODX", "lot_size": SQ_M_PER_ACRE,
         "assessed_value": 1000.0, "gross_area": 0.0},
    ])
    out = build_hood_lot_acres(df).set_index("neighbourhood_name")
    assert pd.isna(out.loc["HOODX", "far"])


def test_hood_lot_acres_far_ignores_zeros_but_keeps_real_floor_area():
    # A partially-recorded hood keeps a real FAR from the rows that HAVE one —
    # the zeros must not drag the numerator down, and must not null the hood.
    df = _frame([
        {**A, "neighbourhood_name": "HOODX", "lot_size": 5000.0,
         "assessed_value": 100.0, "gross_area": 0.0},
        {**A, "neighbourhood_name": "HOODX", "lot_size": 5000.0,
         "assessed_value": 200.0, "gross_area": 250.0},
    ])
    out = build_hood_lot_acres(df).set_index("neighbourhood_name")
    assert out.loc["HOODX", "far"] == pytest.approx(250.0 / 5000.0)


def test_hood_lot_acres_omits_far_without_gross_area():
    # Backward-compat: no gross_area column -> no far column emitted.
    df = _frame([
        {**A, "neighbourhood_name": "HOODX", "lot_size": SQ_M_PER_ACRE,
         "assessed_value": 1000.0},
    ])
    out = build_hood_lot_acres(df)
    assert "far" not in out.columns


# --- non-residential subset (apply_tax_rates nonres_levy) -------------------


def test_nonres_revenue_grid_columns():
    # nonres_levy sums per cell like res_levy; a cell with property but no
    # non-res-rate levy reads a real 0, not null. Lot variant: eligible subset.
    df = _frame([
        {**A, "assessed_value": 100.0, "levy": 3.0, "nonres_levy": 2.0, "lot_size": 500.0},
        {**A2, "assessed_value": 200.0, "levy": 1.0, "nonres_levy": 0.5, "lot_size": 500.0},
        {**B, "assessed_value": 400.0, "levy": 4.0, "nonres_levy": 0.0, "lot_size": 250.0},
    ])
    grid = build_value_grid(df, cell_m=100.0)
    cell_acres = 100.0 * 100.0 / SQ_M_PER_ACRE
    vals = sorted(grid["nonres_revenue_per_acre"])
    assert vals == pytest.approx(sorted([2.5 / cell_acres, 0.0]))
    cell_a = grid[grid["nonres_revenue_per_acre"] > 0].iloc[0]
    lot_acres = 1000.0 / SQ_M_PER_ACRE
    assert cell_a["nonres_revenue_per_lot_acre"] == pytest.approx(2.5 / lot_acres)


def test_no_nonres_levy_omits_nonres_columns():
    df = _frame([{**A, "assessed_value": 100.0, "levy": 1.0, "lot_size": 500.0}])
    grid = build_value_grid(df)
    assert "nonres_revenue_per_acre" not in grid.columns
    assert "nonres_revenue_per_lot_acre" not in grid.columns


def test_export_nonres_columns_appended_last(tmp_path):
    # nonres columns append at the very END — after median_year_built — so the
    # existing nine slots keep their positions (stable prefix). Levy values
    # >= 1000: whole-$ rounding on a ~2.47-acre cell zeroes tiny values.
    df = _frame([
        {**A, "assessed_value": 100.0, "levy": 3000.0, "res_levy": 1000.0,
         "nonres_levy": 2000.0, "lot_size": 500.0, "year_built": 1975.0},
        {**B, "assessed_value": 400.0, "levy": 4000.0, "res_levy": 4000.0,
         "nonres_levy": 0.0, "lot_size": None, "year_built": None},
    ])
    out = tmp_path / "value_grid.json"
    stats = export_value_grid(df, out, cell_m=100.0)
    payload = json.loads(out.read_text())
    assert payload["columns"] == [
        "lon", "lat", "value_per_acre", "revenue_per_acre",
        "value_per_lot_acre", "revenue_per_lot_acre",
        "res_revenue_per_acre", "res_revenue_per_lot_acre",
        "median_year_built",
        "nonres_revenue_per_acre", "nonres_revenue_per_lot_acre",
    ]
    assert stats["has_nonres"] is True
    lot_acres = 500.0 / SQ_M_PER_ACRE
    rows = sorted(payload["cells"], key=lambda r: r[9])
    assert rows[0][9] == 0 and rows[0][10] is None   # B: real $0 nonres, no lot
    assert rows[1][9] == round(2000.0 / (100.0 * 100.0 / SQ_M_PER_ACRE))
    assert rows[1][10] == round(2000.0 / lot_acres)


def test_export_nonres_without_lot(tmp_path):
    # nonres_levy present but no lot_size: only the ground-acre column ships.
    df = _frame([{**A, "assessed_value": 100.0, "levy": 1000.0, "nonres_levy": 1000.0}])
    out = tmp_path / "value_grid.json"
    export_value_grid(df, out, cell_m=100.0)
    payload = json.loads(out.read_text())
    assert payload["columns"] == [
        "lon", "lat", "value_per_acre", "revenue_per_acre", "nonres_revenue_per_acre",
    ]
    assert len(payload["cells"][0]) == 5


def test_hood_lot_acres_nonres_revenue_variant():
    # nonres_levy rolls up alongside levy into nonres_revenue_lot_eligible;
    # absent when nonres_levy isn't passed (dedupe test above has no levy).
    df = _frame([
        {**A, "neighbourhood_name": "HOODX", "lot_size": SQ_M_PER_ACRE,
         "assessed_value": 1000.0, "levy": 10.0, "nonres_levy": 6.0},
        {**B, "neighbourhood_name": "HOODX", "lot_size": SQ_M_PER_ACRE,
         "assessed_value": 500.0, "levy": 5.0, "nonres_levy": 0.0},
    ])
    out = build_hood_lot_acres(df).set_index("neighbourhood_name")
    assert out.loc["HOODX", "revenue_lot_eligible"] == pytest.approx(15.0)
    assert out.loc["HOODX", "nonres_revenue_lot_eligible"] == pytest.approx(6.0)


def test_exempt_frac_is_share_of_cell_levy():
    # Two properties in one cell, one on institutionally-zoned land: the cell's
    # exempt_frac is the LEVY share, not the property count share.
    df = _frame([
        {**A, "assessed_value": 100.0, "levy": 1000.0, "exempt_levy": 750.0},
        {**A2, "assessed_value": 200.0, "levy": 3000.0, "exempt_levy": 0.0},
        {**B, "assessed_value": 400.0, "levy": 5000.0, "exempt_levy": 5000.0},
    ])
    grid = build_value_grid(df, cell_m=100.0).sort_values("exempt_frac")
    assert list(grid["exempt_frac"]) == pytest.approx([750.0 / 4000.0, 1.0])


def test_exempt_frac_is_nan_when_cell_has_no_levy():
    # A wholly exempt cell has no revenue to apportion. NaN, not 0.0 —
    # "nothing to apportion" is not "0% institutional" (revenue_by_zone's
    # $0-neighbourhood rule, applied per cell).
    df = _frame([
        {**A, "assessed_value": 100.0, "levy": 0.0, "exempt_levy": 0.0},
        {**B, "assessed_value": 400.0, "levy": 2000.0, "exempt_levy": 1000.0},
    ])
    grid = build_value_grid(df, cell_m=100.0)
    fracs = dict(zip(grid["revenue_per_acre"] > 0, grid["exempt_frac"]))
    assert np.isnan(fracs[False])
    assert fracs[True] == pytest.approx(0.5)


def test_no_inst_levy_omits_inst_frac():
    df = _frame([{**A, "assessed_value": 100.0, "levy": 1000.0}])
    grid = build_value_grid(df, cell_m=100.0)
    assert "exempt_frac" not in grid.columns


def test_exempt_frac_needs_levy_to_be_a_share_of():
    # exempt_levy without levy: no denominator, so no column rather than a
    # fraction of assessed value (a different quantity entirely).
    df = _frame([{**A, "assessed_value": 100.0, "exempt_levy": 50.0}])
    grid = build_value_grid(df, cell_m=100.0)
    assert "exempt_frac" not in grid.columns


def test_export_exempt_frac_appended_last(tmp_path):
    # exempt_frac appends after the nonres pair, keeping every existing slot.
    df = _frame([
        {**A, "assessed_value": 100.0, "levy": 3000.0, "res_levy": 1000.0,
         "nonres_levy": 2000.0, "lot_size": 500.0, "year_built": 1975.0,
         "exempt_levy": 3000.0},
        {**B, "assessed_value": 400.0, "levy": 4000.0, "res_levy": 4000.0,
         "nonres_levy": 0.0, "lot_size": None, "year_built": None,
         "exempt_levy": 0.0},
    ])
    out = tmp_path / "value_grid.json"
    stats = export_value_grid(df, out, cell_m=100.0)
    payload = json.loads(out.read_text())
    assert payload["columns"][-1] == "exempt_frac"
    assert payload["columns"][:11] == [
        "lon", "lat", "value_per_acre", "revenue_per_acre",
        "value_per_lot_acre", "revenue_per_lot_acre",
        "res_revenue_per_acre", "res_revenue_per_lot_acre",
        "median_year_built",
        "nonres_revenue_per_acre", "nonres_revenue_per_lot_acre",
    ]
    assert stats["has_exempt"] is True
    rows = sorted(payload["cells"], key=lambda r: r[11])
    assert rows[0][11] == 0.0 and rows[1][11] == 1.0


def test_export_exempt_frac_serialises_null_not_zero(tmp_path):
    # The no-levy cell must reach the browser as null; 0.0 would claim the
    # cell was measured and found non-institutional.
    df = _frame([
        {**A, "assessed_value": 100.0, "levy": 0.0, "exempt_levy": 0.0},
        {**B, "assessed_value": 400.0, "levy": 4000.0, "exempt_levy": 1000.0},
    ])
    out = tmp_path / "value_grid.json"
    export_value_grid(df, out, cell_m=100.0)
    payload = json.loads(out.read_text())
    i = payload["columns"].index("exempt_frac")
    assert sorted(r[i] for r in payload["cells"] if r[i] is not None) == [0.25]
    assert sum(1 for r in payload["cells"] if r[i] is None) == 1


# --- amenity distance columns (amenity_distance, attached upstream) ----------

def test_distance_columns_take_the_cell_median_not_the_minimum():
    """One corner property near a station must not make the whole cell read as served."""
    df = _frame([
        {**A, "assessed_value": 100.0, "dist_lrt_m": 100.0, "dist_school_m": 200.0},
        {**A2, "assessed_value": 100.0, "dist_lrt_m": 900.0, "dist_school_m": 400.0},
        {**B, "assessed_value": 100.0, "dist_lrt_m": 5000.0, "dist_school_m": 800.0},
    ])
    grid = build_value_grid(df, cell_m=100.0).sort_values("dist_lrt_m").reset_index(drop=True)
    assert grid.loc[0, "dist_lrt_m"] == pytest.approx(500.0)  # median of 100/900
    assert grid.loc[0, "dist_school_m"] == pytest.approx(300.0)
    assert grid.loc[1, "dist_lrt_m"] == pytest.approx(5000.0)


def test_distance_median_skips_nulls_and_all_null_cell_is_nan():
    df = _frame([
        {**A, "assessed_value": 100.0, "dist_lrt_m": 400.0},
        {**A2, "assessed_value": 100.0, "dist_lrt_m": None},
        {**B, "assessed_value": 100.0, "dist_lrt_m": None},
    ])
    grid = build_value_grid(df, cell_m=100.0)
    dists = sorted(grid["dist_lrt_m"], key=lambda v: (pd.isna(v), v))
    assert dists[0] == pytest.approx(400.0)
    assert pd.isna(dists[1])


def test_no_distance_columns_omitted():
    grid = build_value_grid(_frame([{**A, "assessed_value": 100.0}]))
    assert "dist_lrt_m" not in grid.columns
    assert "dist_school_m" not in grid.columns


def test_one_distance_column_ships_without_the_other():
    """Graceful degradation: no GTFS feed still leaves the school column usable."""
    df = _frame([{**A, "assessed_value": 100.0, "dist_school_m": 250.0}])
    grid = build_value_grid(df)
    assert "dist_school_m" in grid.columns
    assert "dist_lrt_m" not in grid.columns


def test_export_distance_columns_appended_last(tmp_path):
    df = _frame([
        {**A, "assessed_value": 100.0, "dist_lrt_m": 612.4, "dist_school_m": 250.0},
        {**B, "assessed_value": 400.0, "dist_lrt_m": None, "dist_school_m": 900.0},
    ])
    out = tmp_path / "value_grid.json"
    stats = export_value_grid(df, out, cell_m=100.0)
    payload = json.loads(out.read_text())
    assert payload["columns"] == [
        "lon", "lat", "value_per_acre", "dist_lrt_m", "dist_school_m",
    ]
    assert stats["dist_columns"] == ["dist_lrt_m", "dist_school_m"]
    assert stats["n_cells_without_dist_lrt_m"] == 1
    lrt = sorted((r[3] for r in payload["cells"]), key=lambda v: (v is None, v))
    # Whole metres — the graph snaps at 0.1 m and the source is centrelines.
    assert lrt[0] == 612 and isinstance(lrt[0], int)
    # Unreachable is null, NOT a large sentinel a filter would read as "far".
    assert lrt[1] is None
