"""Tests for scripts/build_levy_catchments.py (approx. off-site levy catchments).

The catchment polygons are a manual, reviewed approximation (union of
neighbourhoods read off Bylaw 19340 Schedule A). These tests pin the config
invariants (no double-assigned hood; every levy catchment mapped) and exercise
the dissolve/validation core on synthetic square geometries — no real data.
"""
import sys
from pathlib import Path

import pytest

gpd = pytest.importorskip("geopandas")
from shapely.geometry import Polygon  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import build_levy_catchments as b  # noqa: E402


def test_every_levy_catchment_is_mapped():
    """Each of the 12 brief catchments appears once, directly or via a merge."""
    covered = set()
    for unit in b.CATCHMENT_HOODS:
        covered.update(b.MERGE_GROUPS.get(unit, [unit]))
    assert covered == set(b.LEVY_TABLE), covered ^ set(b.LEVY_TABLE)


def test_no_hood_assigned_twice():
    used = [h for hs in b.CATCHMENT_HOODS.values() for h in hs]
    assert len(used) == len(set(used)), "a hood is assigned to >1 catchment"


def test_merged_attrs_sums_components():
    a = b.merged_attrs("EETP")  # EETP + Northeast EETP
    assert a["merged"] is True
    assert a["assessable_ha_brief"] == 1_268 + 2_040
    assert a["facility_cost_total"] == 26_143_915 * 2
    assert a["rate_per_ha_blended"] == round(a["facility_cost_total"] / a["assessable_ha_brief"])


def test_merged_attrs_single_is_not_merged():
    a = b.merged_attrs("Wedgewood")
    assert a["merged"] is False
    assert a["components"] == ["Wedgewood"]


def _hoods(names):
    """Unit squares (100 ha each in EPSG:3400 metres) stacked along x."""
    polys = [Polygon([(i * 1000, 0), (i * 1000 + 1000, 0),
                      (i * 1000 + 1000, 1000), (i * 1000, 1000)])
             for i in range(len(names))]
    return gpd.GeoDataFrame({"name": names}, geometry=polys, crs=b.AREA_CRS)


def test_build_missing_name_aborts(tmp_path, monkeypatch):
    monkeypatch.setattr(b, "CATCHMENT_HOODS", {"Wedgewood": ["NOPE"]})
    monkeypatch.setattr(b, "MERGE_GROUPS", {})
    hp = tmp_path / "h.geojson"
    _hoods(["REAL"]).to_file(hp, driver="GeoJSON")
    with pytest.raises(SystemExit, match="not in neighbourhood layer"):
        b.build(hp, tmp_path / "out.geojson")


def test_build_duplicate_hood_aborts(tmp_path, monkeypatch):
    monkeypatch.setattr(b, "CATCHMENT_HOODS", {"Wedgewood": ["A"], "Big Lake": ["A"]})
    monkeypatch.setattr(b, "MERGE_GROUPS", {})
    hp = tmp_path / "h.geojson"
    _hoods(["A"]).to_file(hp, driver="GeoJSON")
    with pytest.raises(SystemExit, match="assigned to >1 catchment"):
        b.build(hp, tmp_path / "out.geojson")


def test_build_dissolves_and_flags_ratio(tmp_path, monkeypatch):
    # Wedgewood assessable_ha_brief = 622; two 100 ha squares -> 200 ha union
    # -> ratio 0.32 -> under-covers flag. One catchment, no merges.
    monkeypatch.setattr(b, "CATCHMENT_HOODS", {"Wedgewood": ["A", "B"]})
    monkeypatch.setattr(b, "MERGE_GROUPS", {})
    hp = tmp_path / "h.geojson"
    _hoods(["A", "B"]).to_file(hp, driver="GeoJSON")
    out = tmp_path / "out.geojson"
    gdf = b.build(hp, out)
    assert out.exists()
    assert len(gdf) == 1
    row = gdf.iloc[0]
    assert row["n_hoods"] == 2
    assert round(row["union_ha"]) == 200
    assert "under-covers" in row["qa_flag"]
    assert gdf.crs.to_epsg() == 4326
