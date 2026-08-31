import json
import sys
from unittest.mock import patch

import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon

sys.path.insert(0, "src")
from load_zoning import (
    RESIDENTIAL_THRESHOLD,
    SET_ASIDE_THRESHOLD,
    _categorize,
    export_zoning_web,
    load_zoning,
)


def _square(x0, y0, size):
    return Polygon([(x0, y0), (x0 + size, y0), (x0 + size, y0 + size), (x0, y0 + size)])


def _boundaries(names, polys):
    """Neighbourhood boundaries already projected to EPSG:3400 (metres)."""
    return gpd.GeoDataFrame(
        {"neighbourhood_name": names, "geometry": polys},
        crs="EPSG:3400",
    )


def _zoning(codes, polys):
    """Zoning frame with geometry already in EPSG:3400 metres, so the loader's
    to_crs(3400) is a no-op and the synthetic coordinates drive the overlay."""
    return gpd.GeoDataFrame(
        {"zoning": codes, "geometry": polys},
        crs="EPSG:3400",
    )


def _run(boundaries, zoning):
    with patch("load_zoning.gpd.read_file", return_value=zoning):
        return load_zoning("dummy.geojson", boundaries)


# --- _categorize ---------------------------------------------------------------

def test_categorize_parses_first_token():
    cats = _categorize(pd.Series(["RM h16", "A", "FD"]))
    assert list(cats) == ["res", "never", "notyet"]


def test_categorize_splits_residential_from_nonresidential():
    # The old "dev" bucket is split: housing → res; the rest by use.
    assert list(_categorize(pd.Series(["RSF", "RM", "GRH"]))) == ["res"] * 3
    assert list(_categorize(pd.Series(["CN", "IM", "MU"]))) == ["com", "ind", "mix"]


def test_categorize_nonres_split_resolves_misleading_names():
    # Assigned from the bylaw purpose statement, not the name: UW "Urban
    # Warehouse" is a downtown mixed-use zone, BE "Business Employment" sits in
    # the bylaw's industrial part (DATA.md §5).
    assert list(_categorize(pd.Series(["UW", "HA", "MMS"]))) == ["mix"] * 3
    assert list(_categorize(pd.Series(["BE"]))) == ["ind"]
    assert list(_categorize(pd.Series(["MED", "AED"]))) == ["com"] * 2


def test_categorize_institutional_not_set_aside():
    # UI/UF/AJ/PU are their own category, distinct from set-aside.
    assert list(_categorize(pd.Series(["PU", "UI", "AJ", "UF"]))) == ["inst"] * 4


def test_categorize_unknown_defaults_to_other_and_warns(caplog):
    # Unknown codes stay on scale but are not claimed as any specific use.
    with caplog.at_level("WARNING"):
        cats = _categorize(pd.Series(["ZZZ"]))
    assert list(cats) == ["other"]
    assert "ZZZ" in caplog.text


def test_categorize_direct_control_is_own_category():
    # DC is bespoke per-site bylaws — stays on scale, claimed as no single use.
    assert list(_categorize(pd.Series(["DC", "DC1", "DC2"]))) == ["dc"] * 3


# --- load_zoning ---------------------------------------------------------------

def test_fully_natural_hood_is_set_aside():
    hood = _boundaries(["RIVER VALLEY"], [_square(0, 0, 100)])
    zoning = _zoning(["A"], [_square(0, 0, 100)])
    result = _run(hood, zoning)
    row = result.iloc[0]
    assert row["set_aside_frac"] == 1.0
    assert bool(row["is_set_aside"]) is True
    assert row["set_aside_reason"] == "River Valley / Natural / Parks"


def test_fully_developed_hood_not_set_aside():
    hood = _boundaries(["DOWNTOWN"], [_square(0, 0, 100)])
    zoning = _zoning(["RSF"], [_square(0, 0, 100)])
    result = _run(hood, zoning)
    row = result.iloc[0]
    assert row["set_aside_frac"] == 0.0
    assert bool(row["is_set_aside"]) is False
    assert row["set_aside_reason"] == ""


def test_threshold_boundary():
    # 95% natural, 5% developed (full-height strips) → above 0.90 → set aside.
    hood = _boundaries(["MOSTLY_NATURAL"], [_square(0, 0, 100)])
    zoning = _zoning(
        ["NA", "RSF"],
        [Polygon([(0, 0), (95, 0), (95, 100), (0, 100)]),
         Polygon([(95, 0), (100, 0), (100, 100), (95, 100)])],
    )
    result = _run(hood, zoning)
    row = result.iloc[0]
    assert abs(row["set_aside_frac"] - 0.95) < 1e-6
    assert bool(row["is_set_aside"]) is True


def test_mixed_hood_below_threshold_stays_on_scale():
    # 50/50 natural/developed → below 0.90 → stays on scale.
    hood = _boundaries(["MIXED"], [_square(0, 0, 100)])
    zoning = _zoning(
        ["A", "RSF"],
        [Polygon([(0, 0), (50, 0), (50, 100), (0, 100)]),
         Polygon([(50, 0), (100, 0), (100, 100), (50, 100)])],
    )
    result = _run(hood, zoning)
    row = result.iloc[0]
    assert abs(row["set_aside_frac"] - 0.5) < 1e-6
    assert bool(row["is_set_aside"]) is False
    assert SET_ASIDE_THRESHOLD == 0.90


def test_notyet_counts_toward_set_aside():
    hood = _boundaries(["FRINGE"], [_square(0, 0, 100)])
    zoning = _zoning(["FD"], [_square(0, 0, 100)])
    result = _run(hood, zoning)
    row = result.iloc[0]
    assert row["frac_notyet"] == 1.0
    assert bool(row["is_set_aside"]) is True
    assert row["set_aside_reason"] == "Future / Rural / Reserve"


def test_institutional_stays_on_scale():
    hood = _boundaries(["CIVIC"], [_square(0, 0, 100)])
    zoning = _zoning(["PU"], [_square(0, 0, 100)])
    result = _run(hood, zoning)
    row = result.iloc[0]
    assert row["frac_inst"] == 1.0
    assert row["set_aside_frac"] == 0.0
    assert bool(row["is_set_aside"]) is False


# --- residential-only lens -----------------------------------------------------

def test_fully_residential_hood_flagged():
    hood = _boundaries(["SUBURB"], [_square(0, 0, 100)])
    zoning = _zoning(["RSF"], [_square(0, 0, 100)])
    result = _run(hood, zoning)
    row = result.iloc[0]
    assert row["frac_residential"] == 1.0
    assert bool(row["is_residential"]) is True


def test_commercial_hood_not_residential():
    hood = _boundaries(["STRIP"], [_square(0, 0, 100)])
    zoning = _zoning(["CN"], [_square(0, 0, 100)])
    result = _run(hood, zoning)
    row = result.iloc[0]
    assert row["frac_commercial"] == 1.0
    assert row["frac_residential"] == 0.0
    assert bool(row["is_residential"]) is False


def test_unclassified_land_is_not_folded_into_a_nonres_total():
    """An unmatched code lands in `frac_other` and stays visible as its own share.

    `frac_nonres` (com+ind+mix+dc+other) was removed 2026-08-31: it was the one
    place `other` got asserted as a non-residential use, contradicting
    `DEFAULT_CATEGORY`'s own comment, and nothing consumed it. This pins both
    halves — the column is gone, and the unclassified share is still reported.
    """
    hood = _boundaries(["ODDBALL"], [_square(0, 0, 100)])
    zoning = _zoning(["ZZZ"], [_square(0, 0, 100)])  # not in ZONE_CATEGORY
    result = _run(hood, zoning)
    row = result.iloc[0]
    assert row["frac_other"] == 1.0
    assert "frac_nonres" not in result.columns
    assert row["frac_commercial"] == 0.0
    assert row["frac_residential"] == 0.0


# --- use-mix composition ---------------------------------------------------------

def test_composition_fractions_sum_to_one():
    # Four quarters: residential / commercial / industrial / direct control.
    hood = _boundaries(["QUARTERS"], [_square(0, 0, 100)])
    zoning = _zoning(
        ["RSF", "CN", "IM", "DC2"],
        [_square(0, 0, 50), _square(50, 0, 50), _square(0, 50, 50), _square(50, 50, 50)],
    )
    result = _run(hood, zoning)
    row = result.iloc[0]
    for col in ("frac_residential", "frac_commercial", "frac_industrial", "frac_dc"):
        assert abs(row[col] - 0.25) < 1e-6
    frac_cols = [
        "frac_never", "frac_notyet", "frac_inst", "frac_residential",
        "frac_commercial", "frac_industrial", "frac_mixed", "frac_dc", "frac_other",
    ]
    assert abs(sum(row[c] for c in frac_cols) - 1.0) < 1e-6


def test_mixed_use_hood_composition():
    # 60% mixed-use zoning, 40% housing → mix-dominant but still nonres-minority.
    hood = _boundaries(["TOD"], [_square(0, 0, 100)])
    zoning = _zoning(
        ["MU", "RSF"],
        [Polygon([(0, 0), (60, 0), (60, 100), (0, 100)]),
         Polygon([(60, 0), (100, 0), (100, 100), (60, 100)])],
    )
    result = _run(hood, zoning)
    row = result.iloc[0]
    assert abs(row["frac_mixed"] - 0.6) < 1e-6
    assert abs(row["frac_residential"] - 0.4) < 1e-6
    assert row["frac_commercial"] == 0.0
    assert bool(row["is_residential"]) is False


def test_residential_threshold_boundary():
    # 60% residential, 40% commercial → above 0.50 → residential.
    hood = _boundaries(["MOSTLY_HOMES"], [_square(0, 0, 100)])
    zoning = _zoning(
        ["RSF", "CN"],
        [Polygon([(0, 0), (60, 0), (60, 100), (0, 100)]),
         Polygon([(60, 0), (100, 0), (100, 100), (60, 100)])],
    )
    result = _run(hood, zoning)
    row = result.iloc[0]
    assert abs(row["frac_residential"] - 0.6) < 1e-6
    assert bool(row["is_residential"]) is True
    assert RESIDENTIAL_THRESHOLD == 0.50


def test_set_aside_hood_is_not_residential():
    # Orthogonality: a set-aside hood cannot clear the residential threshold.
    hood = _boundaries(["RIVER VALLEY"], [_square(0, 0, 100)])
    zoning = _zoning(
        ["A", "RSF"],
        [Polygon([(0, 0), (95, 0), (95, 100), (0, 100)]),
         Polygon([(95, 0), (100, 0), (100, 100), (95, 100)])],
    )
    result = _run(hood, zoning)
    row = result.iloc[0]
    assert bool(row["is_set_aside"]) is True
    assert bool(row["is_residential"]) is False

# --- export_zoning_web (Uses-view ground layer) ----------------------------------

def _run_export(zoning, tmp_path, boundaries=None, **kwargs):
    # Default: one big hood covering the synthetic zoning, setback off, so
    # category tests aren't about the clip.
    if boundaries is None:
        boundaries = _boundaries(["ALL"], [_square(-100, -100, 800)])
        kwargs.setdefault("setback_m", 0.0)
    out = tmp_path / "zoning.geojson"
    with patch("load_zoning.gpd.read_file", return_value=zoning):
        n = export_zoning_web("dummy.geojson", boundaries, str(out), **kwargs)
    return n, json.loads(out.read_text())


def test_export_dissolves_by_category(tmp_path):
    # Two residential squares + one commercial -> one feature per category.
    zoning = _zoning(
        ["RSF", "RM", "CN"],
        [_square(0, 0, 100), _square(100, 0, 100), _square(300, 0, 100)],
    )
    n, fc = _run_export(zoning, tmp_path)
    assert n == 2
    cats = sorted(f["properties"]["u"] for f in fc["features"])
    assert cats == ["com", "res"]


def test_export_clips_setback_gaps_between_hoods(tmp_path):
    # One residential sheet across two adjacent hoods; a 10 m setback must
    # remove the 20 m strip around their shared boundary (x=200) from the
    # display geometry.
    zoning = _zoning(["RSF"], [_square(0, 0, 400)])
    hoods = _boundaries(["WEST", "EAST"], [_square(0, 0, 200), _square(200, 0, 200)])
    _, fc = _run_export(zoning, tmp_path, boundaries=hoods, setback_m=10.0,
                        simplify_tolerance_m=0.0)
    import shapely.geometry as sg
    geom = sg.shape(fc["features"][0]["geometry"])
    # Points either side of the gap survive; the boundary strip does not.
    # (The export writes EPSG:4326 — probe via the projected frame instead.)
    from pyproj import Transformer
    t = Transformer.from_crs("EPSG:3400", "EPSG:4326", always_xy=True)
    inside = sg.Point(t.transform(100, 100))
    gap = sg.Point(t.transform(200, 100))
    assert geom.contains(inside)
    assert not geom.contains(gap)


def test_export_carries_only_the_category_prop(tmp_path):
    zoning = _zoning(["A"], [_square(0, 0, 100)])
    _, fc = _run_export(zoning, tmp_path)
    assert list(fc["features"][0]["properties"]) == ["u"]
    assert fc["features"][0]["properties"]["u"] == "never"


def test_export_rounds_coordinates(tmp_path):
    zoning = _zoning(["RSF"], [_square(0, 0, 100)])
    _, fc = _run_export(zoning, tmp_path, precision=3)

    def flat(c):
        return sum((flat(x) for x in c), []) if isinstance(c, list) else [c]

    for v in flat(fc["features"][0]["geometry"]["coordinates"]):
        assert round(v, 3) == v


def test_export_unknown_code_lands_in_other(tmp_path):
    zoning = _zoning(["ZZZ"], [_square(0, 0, 100)])
    _, fc = _run_export(zoning, tmp_path)
    assert fc["features"][0]["properties"]["u"] == "other"
