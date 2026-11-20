"""Tests for scripts/check_served_columns.py (the served-schema drop guard).

The failure this guard exists for is invisible by construction: every lens
self-gates on its own column, so a dropped one hides its own row and the publish
looks clean. The tests that matter are therefore the ones proving it TRIPS — a
guard that only ever passes would be indistinguishable from no guard at all,
which is the exact state this replaced.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from check_served_columns import (  # noqa: E402
    EXIT_DRIFT,
    EXIT_OK,
    column_presence,
    compare_to_baseline,
    empty_columns,
    grid_drift,
    main,
)

COLUMNS = ["neighbourhood_name", "revenue_per_acre", "bike_m_per_acre"]


def _feature(**props):
    return {"type": "Feature", "geometry": None, "properties": props}


def _geojson(features):
    return {"type": "FeatureCollection", "features": features}


def _full(n=3):
    return [_feature(neighbourhood_name=f"H{i}", revenue_per_acre=1.0, bike_m_per_acre=2.0)
            for i in range(n)]


def _write(tmp_path, features, baseline=COLUMNS):
    geo = tmp_path / "served.geojson"
    base = tmp_path / "baseline.json"
    geo.write_text(json.dumps(_geojson(features)))
    base.write_text(json.dumps({"columns": list(baseline)}))
    return geo, base


def _run(geo, base):
    # `--grid` with no paths: these tests are about the GeoJSON half, and the
    # default would read the real web/data grids.
    return main(["--geojson", str(geo), "--baseline", str(base), "--grid"])


# --- column_presence ---------------------------------------------------------

def test_column_presence_counts_key_presence_not_values():
    # A null is a legitimate "no value for this hood" (set-aside land), so it
    # must still count as the column being present — the distinction the whole
    # guard turns on.
    counts = column_presence([
        _feature(a=1.0, b=None),
        _feature(a=2.0, b=3.0),
    ])
    assert counts == {"a": 2, "b": 2}


def test_column_presence_counts_a_partially_written_column():
    counts = column_presence([_feature(a=1.0, b=1.0), _feature(a=2.0)])
    assert counts == {"a": 2, "b": 1}


# --- compare_to_baseline -----------------------------------------------------

def test_compare_clean_schema_has_nothing_in_any_bucket():
    counts = column_presence(_full())
    assert compare_to_baseline(counts, 3, COLUMNS) == ([], [], [])


def test_compare_flags_a_fully_dropped_column_as_missing():
    counts = column_presence([_feature(neighbourhood_name="H", revenue_per_acre=1.0)])
    missing, partial, added = compare_to_baseline(counts, 1, COLUMNS)
    assert missing == ["bike_m_per_acre"]
    assert partial == []


def test_compare_flags_a_half_written_column_as_partial_not_missing():
    features = _full(3)
    del features[0]["properties"]["bike_m_per_acre"]
    missing, partial, added = compare_to_baseline(column_presence(features), 3, COLUMNS)
    assert partial == ["bike_m_per_acre"]
    assert missing == []


def test_compare_reports_a_new_column_as_added():
    features = _full(2)
    for f in features:
        f["properties"]["brand_new"] = 1.0
    missing, partial, added = compare_to_baseline(column_presence(features), 2, COLUMNS)
    assert added == ["brand_new"]
    assert (missing, partial) == ([], [])


# --- main(), the exit codes CI actually reads --------------------------------

def test_main_passes_on_a_complete_schema(tmp_path):
    assert _run(*_write(tmp_path, _full())) == EXIT_OK


def test_main_fails_when_a_column_is_gone_from_every_feature(tmp_path):
    """⚠️ THE CASE verify-smoke.js CANNOT CATCH.

    B7 tolerates a fully-absent column on purpose (it cannot tell "dropped" from
    "not shipped yet" using only the served file). This guard has the committed
    baseline that makes the difference visible, so a full drop MUST be red here
    or it is red nowhere.
    """
    features = [_feature(neighbourhood_name=f"H{i}", revenue_per_acre=1.0) for i in range(3)]
    assert _run(*_write(tmp_path, features)) == EXIT_DRIFT


def test_main_fails_on_a_partially_written_column(tmp_path):
    features = _full(3)
    del features[1]["properties"]["bike_m_per_acre"]
    assert _run(*_write(tmp_path, features)) == EXIT_DRIFT


def test_main_does_not_fail_on_a_new_column(tmp_path):
    """Adding a metric must never block the weekly publish — the cry-wolf rule."""
    features = _full(2)
    for f in features:
        f["properties"]["brand_new"] = 1.0
    assert _run(*_write(tmp_path, features)) == EXIT_OK


def test_main_fails_when_the_served_file_is_absent(tmp_path):
    """Deliberately NOT a skip: no served file means nothing worth publishing."""
    base = tmp_path / "baseline.json"
    base.write_text(json.dumps({"columns": COLUMNS}))
    assert _run(tmp_path / "missing.geojson", base) == EXIT_DRIFT


def test_main_fails_on_an_empty_feature_collection(tmp_path):
    # Zero features makes every column vacuously "absent"; failing here stops
    # that reading an empty file as a clean schema.
    assert _run(*_write(tmp_path, [])) == EXIT_DRIFT


def test_write_baseline_round_trips_the_live_schema(tmp_path):
    geo, base = _write(tmp_path, _full(), baseline=["stale_column"])
    assert main(["--geojson", str(geo), "--baseline", str(base), "--grid",
                 "--write-baseline"]) == EXIT_OK
    assert json.loads(base.read_text())["columns"] == sorted(COLUMNS)
    assert _run(geo, base) == EXIT_OK


# --- the column that is PRESENT and EMPTY ------------------------------------
# docs/FINDINGS_vacuous_guards_r2.md R1. Presence is the wrong question one step
# further along: a failed join or a renamed upstream field writes the column and
# fills it with nulls, so `column_presence` reports every feature carrying it.
# Falsified against the real served file — res_revenue_per_acre nulled on all
# 406 features passed this guard AND verify-smoke.js on the public build, and a
# blank public lens would have published.

def test_a_column_null_on_every_feature_is_empty():
    features = _full(3)
    for f in features:
        f["properties"]["revenue_per_acre"] = None
    assert empty_columns(features, COLUMNS) == ["revenue_per_acre"]


def test_a_column_null_on_some_features_is_not_empty():
    """The cry-wolf direction, and the reason presence counts nulls as present:
    `far` is null on 16 of 406 hoods and the four *_per_lot_acre columns on the
    seven set-aside hoods. Those are legitimate 'no value here'."""
    features = _full(3)
    features[0]["properties"]["revenue_per_acre"] = None
    assert empty_columns(features, COLUMNS) == []


def test_an_absent_column_is_not_double_reported_as_empty():
    """A dropped column is MISSING, not EMPTY — one diagnosis per defect."""
    features = [_feature(neighbourhood_name=f"H{i}") for i in range(3)]
    assert "revenue_per_acre" not in empty_columns(features, COLUMNS)


def test_main_fails_when_a_column_is_null_on_every_feature(tmp_path):
    features = _full(3)
    for f in features:
        f["properties"]["revenue_per_acre"] = None
    assert _run(*_write(tmp_path, features)) == EXIT_DRIFT


def test_main_still_passes_when_a_column_is_null_on_only_some_features(tmp_path):
    # The opposite direction: without this, a guard that failed on ANY null
    # would pass the test above while reddening every real refresh.
    features = _full(3)
    features[0]["properties"]["revenue_per_acre"] = None
    assert _run(*_write(tmp_path, features)) == EXIT_OK


# --- the columnar grids (value_grid.json, value_grid_50.json) ----------------
# The failure: `exempt_frac_res` drops from a grid, the front end's per-cut
# accessor falls back to the TOTAL share, and the defect #803 fixed is back on a
# green publish.

GRID_COLS = ["lon", "lat", "exempt_frac", "exempt_frac_res"]


def _grid(columns=GRID_COLS):
    # One cell with a value in every column, one all-null cell (open land).
    return {"cell_m": 100, "columns": list(columns),
            "cells": [[0.5] * len(columns), [None] * len(columns)]}


def _write_with_grid(tmp_path, grid, grid_baseline=GRID_COLS):
    geo, base = _write(tmp_path, _full())
    pinned = {"columns": COLUMNS}
    if grid_baseline is not None:
        pinned["grid_columns"] = list(grid_baseline)
    base.write_text(json.dumps(pinned))
    g = tmp_path / "value_grid.json"
    g.write_text(json.dumps(grid))
    return geo, base, g


def _run_grid(geo, base, *grids):
    return main(["--geojson", str(geo), "--baseline", str(base), "--grid", *map(str, grids)])


def test_grid_drift_is_clean_on_a_complete_grid():
    d = grid_drift(_grid(), GRID_COLS)
    assert (d["missing"], d["empty"], d["ragged"], d["added"]) == ([], [], 0, [])


def test_grid_drift_flags_a_dropped_column():
    cols = [c for c in GRID_COLS if c != "exempt_frac_res"]
    assert grid_drift(_grid(cols), GRID_COLS)["missing"] == ["exempt_frac_res"]


def test_grid_drift_flags_a_column_null_in_every_cell():
    g = {"columns": GRID_COLS, "cells": [[1.0, 2.0, 0.3, None], [1.1, 2.1, None, None]]}
    assert grid_drift(g, GRID_COLS)["empty"] == ["exempt_frac_res"]


def test_grid_drift_counts_rows_shorter_than_the_columns():
    g = {"columns": GRID_COLS, "cells": [[0.5] * 4, [0.5] * 2]}
    assert grid_drift(g, GRID_COLS)["ragged"] == 1


def test_grid_drift_reports_an_unpinned_column_as_added():
    assert grid_drift(_grid(GRID_COLS + ["new_col"]), GRID_COLS)["added"] == ["new_col"]


def test_main_fails_on_a_ragged_grid(tmp_path):
    grid = {"columns": GRID_COLS, "cells": [[0.5] * 4, [0.5] * 2]}
    geo, base, g = _write_with_grid(tmp_path, grid)
    assert _run_grid(geo, base, g) == EXIT_DRIFT


def test_main_fails_when_the_grid_baseline_is_an_empty_list(tmp_path):
    geo, base, g = _write_with_grid(tmp_path, _grid(), grid_baseline=[])
    assert _run_grid(geo, base, g) == EXIT_DRIFT


def test_write_baseline_refuses_when_the_grids_share_no_columns(tmp_path):
    geo, base, g = _write_with_grid(tmp_path, {"cells": []})
    assert main(["--geojson", str(geo), "--baseline", str(base), "--grid", str(g),
                 "--write-baseline"]) == EXIT_DRIFT


def test_write_baseline_without_grids_keeps_the_existing_grid_pin(tmp_path):
    geo, base, _ = _write_with_grid(tmp_path, _grid())
    assert main(["--geojson", str(geo), "--baseline", str(base), "--grid",
                 "--write-baseline"]) == EXIT_OK
    assert json.loads(base.read_text())["grid_columns"] == GRID_COLS


def test_write_baseline_warns_for_every_column_it_unpins(tmp_path, caplog):
    geo, base, g = _write_with_grid(tmp_path, _grid(GRID_COLS[:3]))
    with caplog.at_level("WARNING"):
        main(["--geojson", str(geo), "--baseline", str(base), "--grid", str(g),
              "--write-baseline"])
    assert any("exempt_frac_res" in r.message and "UNPINNED" in r.message
               for r in caplog.records)


def test_main_passes_on_a_complete_grid(tmp_path):
    geo, base, g = _write_with_grid(tmp_path, _grid())
    assert _run_grid(geo, base, g) == EXIT_OK


def test_main_fails_when_a_grid_drops_the_per_cut_share(tmp_path):
    cols = [c for c in GRID_COLS if c != "exempt_frac_res"]
    geo, base, g = _write_with_grid(tmp_path, _grid(cols))
    assert _run_grid(geo, base, g) == EXIT_DRIFT


def test_main_fails_when_a_grid_column_is_null_in_every_cell(tmp_path):
    grid = {"columns": GRID_COLS, "cells": [[1.0, 2.0, 0.3, None]]}
    geo, base, g = _write_with_grid(tmp_path, grid)
    assert _run_grid(geo, base, g) == EXIT_DRIFT


def test_main_fails_when_the_grid_file_is_absent(tmp_path):
    geo, base, _ = _write_with_grid(tmp_path, _grid())
    assert _run_grid(geo, base, tmp_path / "missing_grid.json") == EXIT_DRIFT


def test_main_fails_when_grids_are_checked_but_no_grid_baseline_is_pinned(tmp_path):
    # Not a skip: deleting the key must not be a way to turn the check off.
    geo, base, g = _write_with_grid(tmp_path, _grid(), grid_baseline=None)
    assert _run_grid(geo, base, g) == EXIT_DRIFT


def test_write_baseline_pins_only_columns_every_grid_carries(tmp_path):
    geo, base, g = _write_with_grid(tmp_path, _grid())
    g2 = tmp_path / "value_grid_50.json"
    g2.write_text(json.dumps(_grid(GRID_COLS[:3])))
    assert main(["--geojson", str(geo), "--baseline", str(base), "--grid", str(g), str(g2),
                 "--write-baseline"]) == EXIT_OK
    assert json.loads(base.read_text())["grid_columns"] == sorted(GRID_COLS[:3])


def test_the_committed_baseline_pins_the_per_cut_grid_shares():
    pinned = json.loads((Path(__file__).resolve().parent.parent
                         / "data" / "expected_columns.json").read_text())
    assert {"exempt_frac_res", "exempt_frac_nonres"} <= set(pinned["grid_columns"])
