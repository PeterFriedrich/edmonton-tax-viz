import json
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
import pytest
from shapely.geometry import Polygon

sys.path.insert(0, "tools")
from ward_rollup import build, summarise  # noqa: E402

RENEWAL_RATE = 38


def _fixture(tmp_path, hoods, wards=None, area_acres=10.0):
    """hoods: {name: (road_m_per_acre, total_revenue)}."""
    served = tmp_path / "served.geojson"
    served.write_text(json.dumps({"type": "FeatureCollection", "features": [
        {"type": "Feature", "geometry": None, "properties": {
            "neighbourhood_name": n, "road_m_per_acre": r, "total_revenue": v}}
        for n, (r, v) in hoods.items()
    ]}))

    costs = tmp_path / "costs.json"
    costs.write_text(json.dumps({"roadway_renewal": {"value": RENEWAL_RATE}}))

    info = tmp_path / "property_info.csv"
    wards = wards or {n: "Métis" for n in hoods}
    pd.DataFrame([{"Account Number": str(i), "Neighbourhood": n, "Ward": wards.get(n)}
                  for i, n in enumerate(hoods)]).to_csv(info, index=False)

    boundaries = tmp_path / "boundaries.geojson"
    gpd.GeoDataFrame(
        {"name": list(hoods), "geometry": [Polygon(
            [(0, 0), (0.01, 0), (0.01, 0.01), (0, 0.01)]) for _ in hoods]},
        crs="EPSG:4326",
    ).to_file(boundaries, driver="GeoJSON")

    return served, boundaries, info, costs


def _build(tmp_path, hoods, wards=None):
    paths = _fixture(tmp_path, hoods, wards)
    df, rate = build(*paths)
    return df, rate


def test_road_metres_rebuilt_from_per_acre_times_acres(tmp_path):
    """The served frame has no absolute metres; they must come back via acres."""
    df, _ = _build(tmp_path, {"BONNIE DOON": (100.0, 1_000.0)})
    row = df.iloc[0]
    assert row["road_m"] == pytest.approx(row["road_m_per_acre"] * row["area_acres"])


def test_renewal_is_metres_times_the_rate(tmp_path):
    df, rate = _build(tmp_path, {"BONNIE DOON": (100.0, 1_000.0)})
    assert rate == RENEWAL_RATE
    row = df.iloc[0]
    assert row["renewal_per_year"] == pytest.approx(row["road_m"] * RENEWAL_RATE)


def test_rate_is_read_from_the_file_not_hardcoded(tmp_path):
    paths = _fixture(tmp_path, {"BONNIE DOON": (100.0, 1_000.0)})
    served, boundaries, info, costs = paths
    costs.write_text(json.dumps({"roadway_renewal": {"value": 99}}))
    df, rate = build(served, boundaries, info, costs)
    assert rate == 99
    assert df.iloc[0]["renewal_per_year"] == pytest.approx(df.iloc[0]["road_m"] * 99)


def test_hoods_group_into_their_wards(tmp_path):
    df, _ = _build(
        tmp_path,
        {"BONNIE DOON": (100.0, 1_000.0), "OTTEWELL": (50.0, 500.0),
         "DOWNTOWN": (10.0, 9_000.0)},
        wards={"BONNIE DOON": "Métis", "OTTEWELL": "Métis", "DOWNTOWN": "O-day'min"},
    )
    table = summarise(df)
    assert table.loc["Métis", "hoods"] == 2
    assert table.loc["O-day'min", "hoods"] == 1


def test_no_hood_is_lost_in_the_rollup(tmp_path):
    """Every served hood lands in exactly one ward row — the double-count guard."""
    df, _ = _build(
        tmp_path,
        {"BONNIE DOON": (100.0, 1_000.0), "OTTEWELL": (50.0, 500.0),
         "CHAPPELLE AREA": (20.0, 200.0)},
        wards={"BONNIE DOON": "Métis", "OTTEWELL": "Métis", "CHAPPELLE AREA": None},
    )
    table = summarise(df)
    assert table["hoods"].sum() == len(df) == 3


def test_hood_without_a_ward_gets_its_own_row_not_dropped(tmp_path):
    df, _ = _build(
        tmp_path,
        {"BONNIE DOON": (100.0, 1_000.0), "CHAPPELLE AREA": (20.0, 200.0)},
        wards={"BONNIE DOON": "Métis", "CHAPPELLE AREA": None},
    )
    table = summarise(df)
    assert "(no ward in source)" in table.index
    assert table.loc["(no ward in source)", "hoods"] == 1


def test_renewal_totals_are_additive_across_wards(tmp_path):
    df, _ = _build(
        tmp_path,
        {"BONNIE DOON": (100.0, 1_000.0), "DOWNTOWN": (10.0, 9_000.0)},
        wards={"BONNIE DOON": "Métis", "DOWNTOWN": "O-day'min"},
    )
    table = summarise(df)
    assert table["renewal_per_year"].sum() == pytest.approx(
        df["renewal_per_year"].sum())


def test_served_hood_with_no_boundary_area_raises(tmp_path):
    """Silently costing zero metres would understate a ward — must fail loud."""
    served, boundaries, info, costs = _fixture(
        tmp_path, {"BONNIE DOON": (100.0, 1_000.0)})
    fc = json.loads(served.read_text())
    fc["features"].append({"type": "Feature", "geometry": None, "properties": {
        "neighbourhood_name": "GHOST HOOD", "road_m_per_acre": 5.0,
        "total_revenue": 1.0}})
    served.write_text(json.dumps(fc))
    with pytest.raises(ValueError, match="no boundary area"):
        build(served, boundaries, info, costs)
