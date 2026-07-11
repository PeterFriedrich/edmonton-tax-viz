"""Tests for scripts/check_unmatched_names.py (the money-path name-drift guard)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from check_unmatched_names import (
    EXIT_DRIFT,
    EXIT_OK,
    compare_to_baseline,
    compute_unmatched,
    main,
)


# --- compute_unmatched -------------------------------------------------------

def test_compute_unmatched_both_directions():
    live = compute_unmatched(
        assessment_names={"DOWNTOWN", "OLIVER"},
        boundary_names={"DOWNTOWN", "LEWIS FARMS"},
    )
    assert live["assessment_not_in_boundaries"] == {"OLIVER"}
    assert live["boundaries_not_in_assessment"] == {"LEWIS FARMS"}


def test_compute_unmatched_perfect_match_is_empty():
    live = compute_unmatched({"A", "B"}, {"A", "B"})
    assert live["assessment_not_in_boundaries"] == set()
    assert live["boundaries_not_in_assessment"] == set()


# --- compare_to_baseline -----------------------------------------------------

BASELINE = {
    "assessment_not_in_boundaries": {"OLIVER"},
    "boundaries_not_in_assessment": {"LEWIS FARMS"},
}


def test_exact_baseline_is_ok():
    result, detail = compare_to_baseline(BASELINE, BASELINE)
    assert result == "ok"
    assert detail["assessment_not_in_boundaries"]["added"] == set()


def test_new_assessment_name_is_drift():
    # A neighbourhood's dollars newly falling off the map — the dangerous case.
    live = {
        "assessment_not_in_boundaries": {"OLIVER", "GHOSTVILLE"},
        "boundaries_not_in_assessment": {"LEWIS FARMS"},
    }
    result, detail = compare_to_baseline(live, BASELINE)
    assert result == "drift"
    assert detail["assessment_not_in_boundaries"]["added"] == {"GHOSTVILLE"}


def test_new_boundary_hole_is_not_drift():
    # A boundary newly lacking assessment shows n/a grey, not wrong money → warn, not fail.
    live = {
        "assessment_not_in_boundaries": {"OLIVER"},
        "boundaries_not_in_assessment": {"LEWIS FARMS", "EMPTY MEADOWS"},
    }
    result, detail = compare_to_baseline(live, BASELINE)
    assert result == "ok"
    assert detail["boundaries_not_in_assessment"]["added"] == {"EMPTY MEADOWS"}


def test_resolved_name_is_not_drift():
    # OLIVER got mapped upstream: baseline is now stale but this is benign.
    live = {
        "assessment_not_in_boundaries": set(),
        "boundaries_not_in_assessment": {"LEWIS FARMS"},
    }
    result, detail = compare_to_baseline(live, BASELINE)
    assert result == "ok"
    assert detail["assessment_not_in_boundaries"]["removed"] == {"OLIVER"}


# --- main (end to end with tiny fixtures) ------------------------------------

def _write_baseline(path: Path, assess: dict, bound: dict) -> None:
    import json
    path.write_text(json.dumps({
        "assessment_not_in_boundaries": assess,
        "boundaries_not_in_assessment": bound,
    }))


def _write_assessment_csv(path: Path, rows: list[tuple[str, float]]) -> None:
    header = (
        "Account Number,Neighbourhood,Assessed Value,Tax Class,"
        "Assessment Class 1,Assessment Class 2,Assessment Class 3,"
        "Assessment Class % 1,Assessment Class % 2,Assessment Class % 3,"
        "Latitude,Longitude"
    )
    lines = [header]
    for i, (name, value) in enumerate(rows):
        lines.append(f"{i},{name},{value:.0f},RESIDENTIAL,RESIDENTIAL,,,100,,,53.5,-113.5")
    path.write_text("\n".join(lines) + "\n")


def _write_boundaries_geojson(path: Path, names: list[str]) -> None:
    import geopandas as gpd
    from shapely.geometry import Polygon
    sq = Polygon([(-113.5, 53.5), (-113.4, 53.5), (-113.4, 53.6), (-113.5, 53.6)])
    gpd.GeoDataFrame(
        {"name": names},
        geometry=[sq] * len(names),
        crs="EPSG:4326",
    ).to_file(path, driver="GeoJSON")


def test_main_ok_on_matching_baseline(tmp_path):
    csv = tmp_path / "a.csv"
    gj = tmp_path / "b.geojson"
    base = tmp_path / "base.json"
    _write_assessment_csv(csv, [("DOWNTOWN", 1_000_000), ("OLIVER", 500)])
    _write_boundaries_geojson(gj, ["DOWNTOWN", "LEWIS FARMS"])
    _write_baseline(base, {"OLIVER": "straggler"}, {"LEWIS FARMS": "hole"})

    code = main(["--assessment-csv", str(csv), "--boundaries-geojson", str(gj),
                 "--baseline", str(base)])
    assert code == EXIT_OK


def test_main_drift_on_new_unmatched_assessment_name(tmp_path):
    csv = tmp_path / "a.csv"
    gj = tmp_path / "b.geojson"
    base = tmp_path / "base.json"
    # GHOSTVILLE has assessed value but no boundary — dollars silently dropped.
    _write_assessment_csv(csv, [("DOWNTOWN", 1_000_000), ("GHOSTVILLE", 750_000)])
    _write_boundaries_geojson(gj, ["DOWNTOWN", "LEWIS FARMS"])
    _write_baseline(base, {}, {"LEWIS FARMS": "hole"})

    code = main(["--assessment-csv", str(csv), "--boundaries-geojson", str(gj),
                 "--baseline", str(base)])
    assert code == EXIT_DRIFT
