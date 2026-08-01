import logging
import sys

import geopandas as gpd
import pandas as pd
import pytest
from shapely.geometry import Polygon

sys.path.insert(0, "src")
from revenue_by_zone import (
    OUTPUT_NAMES,
    UNZONED,
    revenue_by_zone,
    top_zones,
)

# Two adjacent unit squares in WGS84 degrees. Small and far from any real
# neighbourhood, so nothing here depends on Edmonton's actual geography.
LEFT = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
RIGHT = Polygon([(1, 0), (2, 0), (2, 1), (1, 1)])


def _zoning(codes=("RSF", "IM"), polys=(LEFT, RIGHT)):
    return gpd.GeoDataFrame({"zoning": list(codes), "geometry": list(polys)}, crs="EPSG:4326")


def _assessment(rows):
    """rows: (hood, levy, lon, lat)"""
    return pd.DataFrame(
        {
            "neighbourhood_name": [r[0] for r in rows],
            "levy": [r[1] for r in rows],
            "longitude": [r[2] for r in rows],
            "latitude": [r[3] for r in rows],
        }
    )


def _row(result, hood):
    return result.set_index("neighbourhood_name").loc[hood]


def test_splits_revenue_by_the_polygon_each_property_falls_in():
    # 75 in the residential square, 25 in the industrial one.
    a = _assessment([("A", 75.0, 0.5, 0.5), ("A", 25.0, 1.5, 0.5)])
    r = _row(revenue_by_zone(a, _zoning()), "A")
    assert r["rev_frac_residential"] == pytest.approx(0.75)
    assert r["rev_frac_industrial"] == pytest.approx(0.25)
    assert r["rev_zone_matched_frac"] == pytest.approx(1.0)


def test_weights_by_levy_not_by_property_count():
    """The whole point of the module: one big account outweighs many small ones."""
    a = _assessment(
        [("A", 900.0, 0.5, 0.5)] + [("A", 10.0, 1.5, 0.5) for _ in range(10)]
    )
    r = _row(revenue_by_zone(a, _zoning()), "A")
    # 10 of 11 properties are industrial, but 90% of the money is residential.
    assert r["rev_frac_residential"] == pytest.approx(0.9)
    assert r["rev_frac_industrial"] == pytest.approx(0.1)


def test_fractions_sum_to_one_per_neighbourhood():
    a = _assessment(
        [("A", 10.0, 0.5, 0.5), ("A", 30.0, 1.5, 0.5), ("B", 5.0, 0.5, 0.5)]
    )
    result = revenue_by_zone(a, _zoning())
    frac_cols = [c for c in result.columns if c.startswith("rev_frac_")]
    assert result[frac_cols].sum(axis=1).round(9).eq(1.0).all()


def test_revenue_outside_every_polygon_is_bucketed_not_dropped():
    """A silent drop here would inflate every other category's share."""
    a = _assessment([("A", 50.0, 0.5, 0.5), ("A", 50.0, 99.0, 99.0)])
    r = _row(revenue_by_zone(a, _zoning()), "A")
    assert r[OUTPUT_NAMES[UNZONED]] == pytest.approx(0.5)
    assert r["rev_frac_residential"] == pytest.approx(0.5)
    assert r["rev_zone_matched_frac"] == pytest.approx(0.5)


def test_properties_without_coordinates_stay_in_the_denominator():
    """They cannot be placed, but their levy is still the hood's revenue."""
    a = _assessment([("A", 50.0, 0.5, 0.5), ("A", 50.0, None, None)])
    r = _row(revenue_by_zone(a, _zoning()), "A")
    assert r["rev_frac_residential"] == pytest.approx(0.5)
    assert r[OUTPUT_NAMES[UNZONED]] == pytest.approx(0.5)


def test_a_boundary_straddling_point_is_counted_once():
    """sjoin emits a row per matched polygon; double counting would break the sum."""
    a = _assessment([("A", 100.0, 1.0, 0.5)])   # exactly on the shared edge
    result = revenue_by_zone(a, _zoning())
    frac_cols = [c for c in result.columns if c.startswith("rev_frac_")]
    assert result[frac_cols].sum(axis=1).round(9).eq(1.0).all()


def test_zero_levy_neighbourhood_is_nan_not_zero():
    """"No revenue to apportion" must be distinguishable from "0% from every use"."""
    a = _assessment([("A", 0.0, 0.5, 0.5)])
    r = _row(revenue_by_zone(a, _zoning()), "A")
    assert pd.isna(r["rev_frac_residential"])


def test_unknown_zone_code_is_flagged_and_defaults_to_other(caplog):
    z = _zoning(codes=("ZZZQ", "IM"))
    a = _assessment([("A", 100.0, 0.5, 0.5)])
    with caplog.at_level(logging.WARNING):
        r = _row(revenue_by_zone(a, z), "A")
    assert r["rev_frac_other"] == pytest.approx(1.0)
    assert "ZZZQ" in caplog.text


def test_missing_levy_column_raises_rather_than_guessing():
    a = _assessment([("A", 1.0, 0.5, 0.5)]).drop(columns=["levy"])
    with pytest.raises(KeyError, match="apply_tax_rates"):
        revenue_by_zone(a, _zoning())


def test_top_zones_orders_by_share_and_omits_empty_categories():
    a = _assessment(
        [("A", 60.0, 0.5, 0.5), ("A", 40.0, 1.5, 0.5)]
    )
    r = _row(revenue_by_zone(a, _zoning()), "A")
    top = top_zones(r)
    assert top == [("res", pytest.approx(0.6)), ("ind", pytest.approx(0.4))]
    assert len(top) == 2          # not padded to 3 with zero-share entries


def test_top_zones_excludes_unzoned_by_default():
    """The gap is a data caveat, not a land use — it must not occupy a slot."""
    a = _assessment([("A", 90.0, 99.0, 99.0), ("A", 10.0, 0.5, 0.5)])
    r = _row(revenue_by_zone(a, _zoning()), "A")
    assert top_zones(r) == [("res", pytest.approx(0.1))]
    assert top_zones(r, include_unzoned=True)[0][0] == UNZONED
