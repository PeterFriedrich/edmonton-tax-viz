import json
import sys
from unittest.mock import patch

import geopandas as gpd
import pandas as pd
import pytest
from shapely.geometry import LineString, Polygon

sys.path.insert(0, "src")
from load_roads import CLASS_GROUP, _classify, export_roads_web, load_roads


def _square(x0, y0, size):
    return Polygon([(x0, y0), (x0 + size, y0), (x0 + size, y0 + size), (x0, y0 + size)])


def _boundaries(names, polys):
    """Neighbourhood boundaries already projected to EPSG:3400 (metres)."""
    return gpd.GeoDataFrame(
        {"neighbourhood_name": names, "geometry": polys},
        crs="EPSG:3400",
    )


def _roads(rows):
    """Road frame in EPSG:3400 metres so the loader's to_crs(3400) is a no-op.

    rows: list of (centerline_type, responsible_party, functional_class, geometry)
    """
    types, parties, classes, geoms = zip(*rows)
    return gpd.GeoDataFrame(
        {
            "centerline_type": list(types),
            "responsible_party_description": list(parties),
            "functional_class_code": list(classes),
            "geometry": list(geoms),
        },
        crs="EPSG:3400",
    )


def _run(boundaries, roads):
    with patch("load_roads.gpd.read_file", return_value=roads):
        return load_roads("dummy.geojson", boundaries)


CITY = "City of Edmonton"
LOCAL = "Local-Residential"
COLLECTOR = "Collector-Residential"
ARTERIAL = "Arterial-Class A (Primary Highway, Truck Route)"


# --- _classify -------------------------------------------------------------


def test_classify_exact_strings():
    groups = _classify(pd.Series([LOCAL, COLLECTOR, ARTERIAL, "Local-ParkWay"]))
    assert list(groups) == ["local", "collector", "arterial", "local"]


def test_classify_alley_residential_is_alley_group():
    assert list(_classify(pd.Series(["Alley-Residential"]))) == ["alley"]


def test_every_alley_prefixed_code_is_the_alley_group():
    """⚠️ The alleys-out decision is that FUNCTION governs, so every ``Alley-*``
    code must map to "alley" — NOT to the DEFAULT_GROUP fallback, which is
    "local" and would charge an alley as road.

    Pins the class dict rather than the feed (data/raw is gitignored and 62 MB).
    ``Alley-Commercial`` appeared upstream after the 2026-07-01 survey that
    recorded the enumeration as closed at 15 values, fell through the fallback,
    and was counted as local road until 2026-09-09 — this is that hole.

    ⚠️ THIS TEST CANNOT CATCH THE NEXT SUCH CODE, and must not be cited as
    drift protection. It iterates the keys that ARE here, so a missing key
    makes it vacuously true — verified: deleting ``Alley-Commercial`` leaves it
    GREEN and only ``test_alley_commercial_is_excluded_from_the_metric`` reds.
    What it does catch is an ``Alley-*`` key mapped to the wrong group.
    Detecting a NEW upstream code needs the feed's vocabulary compared to this
    dict in the monthly digest — the shape ``check_zoning_bylaw`` already uses
    for the zoning bylaw. Not built; see TODO.md.
    """
    alley_keys = [k for k in CLASS_GROUP if k.startswith("Alley-")]
    assert alley_keys, "no Alley-* codes in CLASS_GROUP at all"
    assert list(_classify(pd.Series(alley_keys))) == ["alley"] * len(alley_keys)


def test_alley_commercial_is_excluded_from_the_metric():
    """The regression itself, end to end: an Alley-Commercial row typed Road
    must not reach road_m_total. Fails by name if the key is removed."""
    hood = _boundaries(["ALPHA"], [_square(0, 0, 100)])
    roads = _roads(
        [
            ("Road", CITY, "Alley-Commercial", LineString([(0, 10), (100, 10)])),
            ("Road", CITY, LOCAL, LineString([(0, 20), (100, 20)])),
        ]
    )
    row = _run(hood, roads).iloc[0]
    assert row["road_m_total"] == pytest.approx(100)


def test_classify_unknown_goes_to_its_own_group_not_the_charged_one(caplog):
    """⚠️ The fallback used to be "local", and "local" is not a neutral holding
    pen — it is the CHARGED side of road_m_total. `Alley-Commercial` is the
    proof: an Alley-* code must leave the metric entirely, and the old default
    billed it as road. Asserting `!= "local"` as well as `== "unknown"` because
    the group NAME is cosmetic and the exclusion is the contract."""
    with caplog.at_level("WARNING"):
        groups = _classify(pd.Series(["Hyperloop-Class Z"]))
    assert list(groups) == ["unknown"]
    assert "local" not in list(groups)
    assert "Hyperloop-Class Z" in caplog.text


def test_classify_null_goes_to_the_unknown_group(caplog):
    with caplog.at_level("WARNING"):
        groups = _classify(pd.Series([None]))
    assert list(groups) == ["unknown"]
    assert "<null>" in caplog.text


def test_the_unknown_group_is_not_in_the_metric():
    """The whole decision, as one assertion on the constants."""
    from load_roads import DEFAULT_GROUP, GROUPS, METRIC_GROUPS
    assert DEFAULT_GROUP not in METRIC_GROUPS
    assert DEFAULT_GROUP in GROUPS  # carried, not discarded


def test_an_unmappable_code_is_held_out_of_the_metric(caplog):
    """⚠️ The direction that inverted on 2026-09-09. Under the old fallback this
    row was CHARGED — road_m_total would read 200. It is now held out."""
    hood = _boundaries(["ALPHA"], [_square(0, 0, 100)])
    roads = _roads(
        [
            ("Road", CITY, "Hyperloop-Class Z", LineString([(0, 10), (100, 10)])),
            ("Road", CITY, LOCAL, LineString([(0, 20), (100, 20)])),
        ]
    )
    with caplog.at_level("WARNING"):
        row = _run(hood, roads).iloc[0]
    assert row["road_m_total"] == pytest.approx(100)
    assert row["road_m_local"] == pytest.approx(100)
    assert "Hyperloop-Class Z" in caplog.text


def test_an_unmappable_code_is_CARRIED_not_dropped():
    """⚠️ The other half, and the one a "just exclude it" fix would fail. Holding
    the length out of the metric must not delete it — a silent data drop is the
    failure this project forbids, and the length is how anyone sizes the defect
    before deciding what the code is."""
    hood = _boundaries(["ALPHA"], [_square(0, 0, 100)])
    roads = _roads(
        [
            ("Road", CITY, "Hyperloop-Class Z", LineString([(0, 10), (100, 10)])),
            ("Road", CITY, LOCAL, LineString([(0, 20), (100, 20)])),
        ]
    )
    row = _run(hood, roads).iloc[0]
    assert row["road_m_unknown"] == pytest.approx(100)


def test_road_m_unknown_is_zero_on_a_clean_feed():
    """It is a defect gauge: non-zero means upstream drift, so the normal
    reading must be 0.0 and not merely absent."""
    hood = _boundaries(["ALPHA"], [_square(0, 0, 100)])
    roads = _roads([("Road", CITY, LOCAL, LineString([(0, 10), (100, 10)]))])
    assert _run(hood, roads).iloc[0]["road_m_unknown"] == 0.0


# --- load_roads ------------------------------------------------------------


def test_lengths_summed_per_hood_and_class():
    hood = _boundaries(["ALPHA"], [_square(0, 0, 100)])
    roads = _roads(
        [
            ("Road", CITY, LOCAL, LineString([(0, 10), (100, 10)])),  # 100 m local
            ("Road", CITY, LOCAL, LineString([(0, 20), (50, 20)])),  # 50 m local
            ("Road", CITY, COLLECTOR, LineString([(0, 30), (100, 30)])),  # 100 m coll
        ]
    )
    result = _run(hood, roads)
    row = result.iloc[0]
    assert row["road_m_local"] == pytest.approx(150)
    assert row["road_m_collector"] == pytest.approx(100)
    assert row["road_m_total"] == pytest.approx(250)


def test_arterial_carried_but_excluded_from_total():
    hood = _boundaries(["ALPHA"], [_square(0, 0, 100)])
    roads = _roads(
        [
            ("Road", CITY, ARTERIAL, LineString([(0, 10), (100, 10)])),
            ("Road", CITY, LOCAL, LineString([(0, 20), (100, 20)])),
        ]
    )
    row = _run(hood, roads).iloc[0]
    assert row["road_m_arterial"] == pytest.approx(100)
    assert row["road_m_total"] == pytest.approx(100)  # local only


def test_non_road_and_non_city_rows_filtered_out():
    hood = _boundaries(["ALPHA"], [_square(0, 0, 100)])
    roads = _roads(
        [
            ("Alley", CITY, None, LineString([(0, 10), (100, 10)])),
            ("Railway", "Canadian National Railway", None, LineString([(0, 20), (100, 20)])),
            ("Road", "Province of Alberta", ARTERIAL, LineString([(0, 30), (100, 30)])),
            ("Road", CITY, LOCAL, LineString([(0, 40), (100, 40)])),
        ]
    )
    row = _run(hood, roads).iloc[0]
    assert row["road_m_total"] == pytest.approx(100)  # only the city road
    assert row["road_m_arterial"] == 0.0  # provincial arterial dropped


def test_functionally_alley_road_rows_excluded():
    """Road-type rows classed Alley-Residential are excluded per the alleys-out
    decision (function governs). 41 such rows in the real data."""
    hood = _boundaries(["ALPHA"], [_square(0, 0, 100)])
    roads = _roads(
        [
            ("Road", CITY, "Alley-Residential", LineString([(0, 10), (100, 10)])),
            ("Road", CITY, LOCAL, LineString([(0, 20), (100, 20)])),
        ]
    )
    row = _run(hood, roads).iloc[0]
    assert row["road_m_total"] == pytest.approx(100)
    assert "road_m_alley" not in row.index


def test_segment_split_across_two_hoods():
    """A road crossing a boundary contributes its clipped length to each side —
    conserved, not duplicated."""
    hoods = _boundaries(
        ["WEST", "EAST"], [_square(0, 0, 100), _square(100, 0, 100)]
    )
    roads = _roads(
        [("Road", CITY, LOCAL, LineString([(0, 50), (200, 50)]))]  # 200 m spanning both
    )
    result = _run(hoods, roads).set_index("neighbourhood_name")
    assert result.loc["WEST", "road_m_total"] == pytest.approx(100)
    assert result.loc["EAST", "road_m_total"] == pytest.approx(100)


def test_segment_outside_all_hoods_reported_not_counted(caplog):
    hood = _boundaries(["ALPHA"], [_square(0, 0, 100)])
    roads = _roads(
        [
            ("Road", CITY, LOCAL, LineString([(0, 10), (100, 10)])),  # inside
            ("Road", CITY, LOCAL, LineString([(0, 500), (100, 500)])),  # outside
        ]
    )
    with caplog.at_level("INFO"):
        result = _run(hood, roads)
    assert result.iloc[0]["road_m_total"] == pytest.approx(100)
    assert "outside all boundaries" in caplog.text


def test_boundaries_must_be_projected():
    hood = _boundaries(["ALPHA"], [_square(0, 0, 100)]).to_crs(epsg=4326)
    roads = _roads([("Road", CITY, LOCAL, LineString([(0, 10), (100, 10)]))])
    with pytest.raises(ValueError, match="EPSG:3400"):
        _run(hood, roads)


def test_hood_with_no_roads_absent_from_result():
    """Like load_zoning, hoods with zero overlay simply don't appear — the
    downstream merge defaults them (join_and_calculate's concern)."""
    hoods = _boundaries(
        ["HASROADS", "EMPTY"], [_square(0, 0, 100), _square(1000, 0, 100)]
    )
    roads = _roads([("Road", CITY, LOCAL, LineString([(0, 10), (100, 10)]))])
    result = _run(hoods, roads)
    assert list(result["neighbourhood_name"]) == ["HASROADS"]


def test_empty_geometry_dropped():
    hood = _boundaries(["ALPHA"], [_square(0, 0, 100)])
    roads = _roads(
        [
            ("Road", CITY, LOCAL, LineString([(0, 10), (100, 10)])),
            ("Road", CITY, LOCAL, None),
        ]
    )
    row = _run(hood, roads).iloc[0]
    assert row["road_m_total"] == pytest.approx(100)


# --- export_roads_web --------------------------------------------------------


def _boundaries_with_acres(names, polys):
    """Web-export boundaries also carry area_acres (the metric denominator)."""
    gdf = _boundaries(names, polys)
    gdf["area_acres"] = gdf.geometry.area / 4046.8564224
    return gdf


def _export(boundaries, roads, out_path):
    with patch("load_roads.gpd.read_file", return_value=roads):
        return export_roads_web("dummy.geojson", boundaries, str(out_path))


def _read_fc(out_path):
    fc = json.loads(out_path.read_text())
    assert fc["type"] == "FeatureCollection"
    return fc


def test_export_dissolves_to_one_feature_per_hood_and_type(tmp_path):
    hood = _boundaries_with_acres(["ALPHA"], [_square(0, 0, 100)])
    roads = _roads(
        [
            ("Road", CITY, LOCAL, LineString([(0, 10), (100, 10)])),
            ("Road", CITY, LOCAL, LineString([(0, 20), (100, 20)])),
            ("Road", CITY, COLLECTOR, LineString([(0, 30), (100, 30)])),
            ("Road", CITY, ARTERIAL, LineString([(0, 40), (100, 40)])),
        ]
    )
    out = tmp_path / "roads.geojson"
    n = _export(hood, roads, out)
    fc = _read_fc(out)
    # 3 local/collector segments dissolve into ONE access feature + 1 arterial.
    assert n == len(fc["features"]) == 2
    types = sorted(f["properties"]["t"] for f in fc["features"])
    assert types == ["access", "arterial"]


def test_export_v_on_access_only_arterial_null(tmp_path):
    hood = _boundaries_with_acres(["ALPHA"], [_square(0, 0, 100)])
    roads = _roads(
        [
            ("Road", CITY, LOCAL, LineString([(0, 10), (100, 10)])),
            ("Road", CITY, ARTERIAL, LineString([(0, 40), (100, 40)])),
        ]
    )
    out = tmp_path / "roads.geojson"
    _export(hood, roads, out)
    props = {f["properties"]["t"]: f["properties"] for f in _read_fc(out)["features"]}
    acres = (100 * 100) / 4046.8564224
    assert props["access"]["v"] == pytest.approx(100 / acres, abs=0.05)  # rounded 0.1
    assert props["arterial"]["v"] is None


def test_export_arterials_dissolve_citywide(tmp_path):
    """Arterials carry no metric, so the export doesn't clip them per hood:
    ONE citywide feature (n null), re-welded across the boundary crossing."""
    hoods = _boundaries_with_acres(
        ["WEST", "EAST"], [_square(0, 0, 100), _square(100, 0, 100)]
    )
    roads = _roads(
        [
            ("Road", CITY, ARTERIAL, LineString([(0, 50), (200, 50)])),  # spans both
            ("Road", CITY, LOCAL, LineString([(0, 10), (100, 10)])),
        ]
    )
    out = tmp_path / "roads.geojson"
    _export(hoods, roads, out)
    art = [f for f in _read_fc(out)["features"] if f["properties"]["t"] == "arterial"]
    assert len(art) == 1
    assert art[0]["properties"]["n"] is None
    g = art[0]["geometry"]
    n_parts = 1 if g["type"] == "LineString" else len(g["coordinates"])
    assert n_parts == 1  # the per-hood clip cut is welded back together


def test_export_drops_short_access_slivers(tmp_path):
    """Access parts shorter than WEB_MIN_PART_M are clip slivers — dropped
    from the DISPLAY file only (v still counts their full-resolution length)."""
    hood = _boundaries_with_acres(["ALPHA"], [_square(0, 0, 100)])
    roads = _roads(
        [
            ("Road", CITY, LOCAL, LineString([(0, 10), (100, 10)])),  # kept
            ("Road", CITY, LOCAL, LineString([(0, 90), (5, 90)])),    # 5 m sliver
        ]
    )
    out = tmp_path / "roads.geojson"
    _export(hood, roads, out)
    (feat,) = _read_fc(out)["features"]
    g = feat["geometry"]
    n_parts = 1 if g["type"] == "LineString" else len(g["coordinates"])
    assert n_parts == 1  # sliver gone from display geometry
    acres = (100 * 100) / 4046.8564224
    assert feat["properties"]["v"] == pytest.approx(105 / acres, abs=0.05)  # metric keeps it


def test_export_props_and_geometry_shape(tmp_path):
    hoods = _boundaries_with_acres(
        ["WEST", "EAST"], [_square(0, 0, 100), _square(100, 0, 100)]
    )
    roads = _roads(
        [("Road", CITY, LOCAL, LineString([(0, 50), (200, 50)]))]  # spans both hoods
    )
    out = tmp_path / "roads.geojson"
    _export(hoods, roads, out)
    fc = _read_fc(out)
    assert sorted(f["properties"]["n"] for f in fc["features"]) == ["EAST", "WEST"]
    for f in fc["features"]:
        assert set(f["properties"]) == {"n", "t", "v"}
        assert f["geometry"]["type"] in ("LineString", "MultiLineString")


def test_export_coordinates_rounded_and_wgs84(tmp_path):
    hood = _boundaries_with_acres(["ALPHA"], [_square(0, 0, 100)])
    roads = _roads([("Road", CITY, LOCAL, LineString([(0, 10), (100, 10)]))])
    out = tmp_path / "roads.geojson"
    _export(hood, roads, out)

    def _flat(coords):
        if coords and isinstance(coords[0], float):
            yield coords
        else:
            for c in coords:
                yield from _flat(c)

    for f in _read_fc(out)["features"]:
        for lon, lat in _flat(f["geometry"]["coordinates"]):
            # Reprojected to lon/lat degrees — metre-scale values (0..200
            # here) would blow these ranges, so this catches a skipped to_crs.
            assert -180 <= lon <= 180 and -90 <= lat <= 90
            assert round(lon, 5) == lon and round(lat, 5) == lat


def test_export_welds_contiguous_segments(tmp_path):
    """Two touching collinear segments dissolve into ONE merged path, not a
    2-part MultiLineString — linemerge runs before simplify so short raw
    segments become long simplifiable lines (browser tessellation cost)."""
    hood = _boundaries_with_acres(["ALPHA"], [_square(0, 0, 100)])
    roads = _roads(
        [
            ("Road", CITY, LOCAL, LineString([(0, 10), (50, 10)])),
            ("Road", CITY, LOCAL, LineString([(50, 10), (100, 10)])),
        ]
    )
    out = tmp_path / "roads.geojson"
    _export(hood, roads, out)
    (feat,) = _read_fc(out)["features"]
    g = feat["geometry"]
    n_parts = 1 if g["type"] == "LineString" else len(g["coordinates"])
    assert n_parts == 1


def test_export_v_matches_load_roads_metric(tmp_path):
    """The colour driver v must equal road_m_total / area_acres — the same
    number join_and_calculate publishes as road_m_per_acre."""
    hood = _boundaries_with_acres(["ALPHA"], [_square(0, 0, 200)])
    roads = _roads(
        [
            ("Road", CITY, LOCAL, LineString([(0, 10), (200, 10)])),
            ("Road", CITY, COLLECTOR, LineString([(0, 30), (150, 30)])),
            ("Road", CITY, ARTERIAL, LineString([(0, 50), (200, 50)])),
        ]
    )
    metric = _run(hood, roads).iloc[0]
    expected = metric["road_m_total"] / hood["area_acres"].iloc[0]

    out = tmp_path / "roads.geojson"
    _export(hood, roads, out)
    access = [f for f in _read_fc(out)["features"] if f["properties"]["t"] == "access"]
    assert access[0]["properties"]["v"] == pytest.approx(expected, abs=0.05)


def test_export_holds_unclassified_length_out_of_the_access_layer(tmp_path, caplog):
    """⚠️ The metric and the map must agree. `access_m` IS road_m_total's basis,
    so drawing unmapped length in the access layer would assert on the map
    exactly what load_roads declines to assert — and the access feature's `v`
    is that length per acre, so it would move the COLOUR too."""
    hood = _boundaries_with_acres(["ALPHA"], [_square(0, 0, 100)])
    roads = _roads(
        [
            ("Road", CITY, LOCAL, LineString([(0, 10), (100, 10)])),
            ("Road", CITY, "Hyperloop-Class Z", LineString([(0, 20), (100, 20)])),
        ]
    )
    out = tmp_path / "roads.geojson"
    with caplog.at_level("WARNING"):
        _export(hood, roads, out)
    fc = _read_fc(out)
    access = [f for f in fc["features"] if f["properties"]["t"] == "access"]
    assert len(access) == 1
    acres = hood["area_acres"].iloc[0]
    assert access[0]["properties"]["v"] == pytest.approx(100 / acres, rel=1e-3)


def test_export_reports_the_length_it_holds_out_rather_than_dropping_it_silently(
    tmp_path, caplog
):
    """⚠️ The silent path this guards. `unknown` is not in the `t` map, so left
    alone it becomes a NaN `t`, and BOTH selections below (`== "access"`,
    `== "arterial"`) exclude a NaN — the length would leave the map with no
    warning anywhere. The exclusion is explicit and logged for that reason."""
    hood = _boundaries_with_acres(["ALPHA"], [_square(0, 0, 100)])
    roads = _roads(
        [
            ("Road", CITY, LOCAL, LineString([(0, 10), (100, 10)])),
            ("Road", CITY, "Hyperloop-Class Z", LineString([(0, 20), (100, 20)])),
        ]
    )
    with caplog.at_level("WARNING"):
        _export(hood, roads, tmp_path / "roads.geojson")
    assert "held out of the access layer" in caplog.text
    assert "0.100 km" in caplog.text


def test_export_is_unchanged_when_every_code_maps(tmp_path, caplog):
    """The OK direction: no warning, and the access geometry is whole. Without
    this, an exclusion hard-wired to fire would pass every test above."""
    hood = _boundaries_with_acres(["ALPHA"], [_square(0, 0, 100)])
    roads = _roads(
        [
            ("Road", CITY, LOCAL, LineString([(0, 10), (100, 10)])),
            ("Road", CITY, COLLECTOR, LineString([(0, 20), (100, 20)])),
        ]
    )
    out = tmp_path / "roads.geojson"
    with caplog.at_level("WARNING"):
        _export(hood, roads, out)
    assert "held out of the access layer" not in caplog.text
    access = [f for f in _read_fc(out)["features"] if f["properties"]["t"] == "access"]
    acres = hood["area_acres"].iloc[0]
    assert access[0]["properties"]["v"] == pytest.approx(200 / acres, rel=1e-3)
