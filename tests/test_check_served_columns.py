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
    return main(["--geojson", str(geo), "--baseline", str(base)])


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
    assert main(["--geojson", str(geo), "--baseline", str(base), "--write-baseline"]) == EXIT_OK
    assert json.loads(base.read_text())["columns"] == sorted(COLUMNS)
    assert _run(geo, base) == EXIT_OK
