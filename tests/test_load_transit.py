import json
import sys

import geopandas as gpd
import pandas as pd
import pytest
from shapely.geometry import Polygon

sys.path.insert(0, "src")
from load_transit import (
    export_transit_lines_web,
    export_transit_stations_web,
    load_transit,
)


# Two square hoods in lon/lat space; the loader projects both sides to
# EPSG:3400, so containment set up here in EPSG:4326 is preserved.
def _square(lon0, lat0, size=0.02):
    return Polygon([
        (lon0, lat0), (lon0 + size, lat0),
        (lon0 + size, lat0 + size), (lon0, lat0 + size),
    ])


BOUNDARIES = gpd.GeoDataFrame(
    {
        "neighbourhood_name": ["ALPHA", "BRAVO"],
        "geometry": [_square(-113.52, 53.50), _square(-113.48, 53.50)],
    },
    crs="EPSG:4326",
)

# Stops: s1/s2 inside ALPHA, s3 inside BRAVO, s4 far outside every hood
# (regional), st1 a location_type-1 station.
DEFAULT_STOPS = [
    {"stop_id": "s1", "stop_lat": 53.505, "stop_lon": -113.515, "location_type": 0, "stop_name": "First"},
    {"stop_id": "s2", "stop_lat": 53.506, "stop_lon": -113.514, "location_type": 0, "stop_name": "Second"},
    {"stop_id": "s3", "stop_lat": 53.505, "stop_lon": -113.475, "location_type": 0, "stop_name": "Third"},
    {"stop_id": "s4", "stop_lat": 53.900, "stop_lon": -113.900, "location_type": 0, "stop_name": "Regional"},
    {"stop_id": "st1", "stop_lat": 53.507, "stop_lon": -113.513, "location_type": 1, "stop_name": "Central Station"},
]

DEFAULT_ROUTES = [
    {"route_id": "rb", "route_type_descr": "Bus"},
    {"route_id": "rl", "route_type_descr": "Tram, Streetcar, Light rail"},
]

# Service "wk" is active both weekday dates (weight 1); "sat" only Saturday
# (weight 0). 2026-01-05 Mon, 2026-01-06 Tue, 2026-01-10 Sat.
DEFAULT_CALENDAR = [
    {"service_id": "wk", "date": "2026-01-05", "exception_type": 1},
    {"service_id": "wk", "date": "2026-01-06", "exception_type": 1},
    {"service_id": "wk", "date": "2026-01-10", "exception_type": 1},
    {"service_id": "sat", "date": "2026-01-10", "exception_type": 1},
]

DEFAULT_TRIPS = [
    {"trip_id": "t1", "route_id": "rb", "service_id": "wk"},
    {"trip_id": "t2", "route_id": "rl", "service_id": "wk"},
    {"trip_id": "t3", "route_id": "rb", "service_id": "sat"},
]

# t1 (bus, weekday) serves s1 + s2; t2 (LRT, weekday) serves s3;
# t3 (bus, Saturday-only) serves s1 — must contribute nothing.
DEFAULT_STOP_TIMES = [
    {"trip_id": "t1", "stop_id": "s1"},
    {"trip_id": "t1", "stop_id": "s2"},
    {"trip_id": "t2", "stop_id": "s3"},
    {"trip_id": "t3", "stop_id": "s1"},
]


def _write(tmp_path, name, rows):
    path = tmp_path / name
    pd.DataFrame(rows).to_csv(path, index=False)
    return path


def _run(
    tmp_path,
    stops=None,
    routes=None,
    trips=None,
    stop_times=None,
    calendar=None,
    boundaries=None,
):
    return load_transit(
        _write(tmp_path, "stops.csv", stops or DEFAULT_STOPS),
        _write(tmp_path, "routes.csv", routes or DEFAULT_ROUTES),
        _write(tmp_path, "trips.csv", trips or DEFAULT_TRIPS),
        _write(tmp_path, "stop_times.csv", stop_times or DEFAULT_STOP_TIMES),
        _write(tmp_path, "calendar.csv", calendar or DEFAULT_CALENDAR),
        BOUNDARIES if boundaries is None else boundaries,
    )


# --- load_transit ------------------------------------------------------------


def test_per_hood_mode_totals(tmp_path):
    out = _run(tmp_path).set_index("neighbourhood_name")
    # ALPHA: t1 at s1 + s2, weight 1 -> 2 bus events; BRAVO: t2 at s3 -> 1 LRT.
    assert out.loc["ALPHA", "transit_dep_bus"] == pytest.approx(2.0)
    assert out.loc["ALPHA", "transit_dep_lrt"] == pytest.approx(0.0)
    assert out.loc["ALPHA", "transit_dep_total"] == pytest.approx(2.0)
    assert out.loc["BRAVO", "transit_dep_lrt"] == pytest.approx(1.0)
    assert out.loc["BRAVO", "transit_dep_total"] == pytest.approx(1.0)


def test_weekend_only_service_weighs_zero(tmp_path):
    # t3 (Saturday-only) serves s1; removing it must not change ALPHA.
    with_t3 = _run(tmp_path).set_index("neighbourhood_name")
    without = _run(
        tmp_path, stop_times=[r for r in DEFAULT_STOP_TIMES if r["trip_id"] != "t3"],
    ).set_index("neighbourhood_name")
    assert with_t3.loc["ALPHA", "transit_dep_total"] == pytest.approx(
        without.loc["ALPHA", "transit_dep_total"]
    )


def test_partial_weekday_service_weighted(tmp_path):
    # A service active on 1 of the 2 weekday dates contributes 0.5 per event.
    calendar = DEFAULT_CALENDAR + [
        {"service_id": "half", "date": "2026-01-05", "exception_type": 1},
    ]
    trips = DEFAULT_TRIPS + [{"trip_id": "t4", "route_id": "rb", "service_id": "half"}]
    stop_times = DEFAULT_STOP_TIMES + [{"trip_id": "t4", "stop_id": "s1"}]
    out = _run(
        tmp_path, calendar=calendar, trips=trips, stop_times=stop_times,
    ).set_index("neighbourhood_name")
    assert out.loc["ALPHA", "transit_dep_bus"] == pytest.approx(2.5)


def test_stop_outside_every_hood_is_unassigned(tmp_path, caplog):
    # t1 also serves the regional stop s4 — reported, not assigned anywhere.
    stop_times = DEFAULT_STOP_TIMES + [{"trip_id": "t1", "stop_id": "s4"}]
    with caplog.at_level("INFO"):
        out = _run(tmp_path, stop_times=stop_times).set_index("neighbourhood_name")
    assert out["transit_dep_total"].sum() == pytest.approx(3.0)
    assert "unassigned" in caplog.text


def test_unknown_stop_id_is_unassigned_not_crash(tmp_path, caplog):
    stop_times = DEFAULT_STOP_TIMES + [{"trip_id": "t1", "stop_id": "s9"}]
    with caplog.at_level("INFO"):
        out = _run(tmp_path, stop_times=stop_times).set_index("neighbourhood_name")
    assert out["transit_dep_total"].sum() == pytest.approx(3.0)
    assert "unassigned" in caplog.text


def test_orphan_stop_times_excluded_and_warned(tmp_path, caplog):
    # A stop_times row referencing a trip_id absent from trips.
    stop_times = DEFAULT_STOP_TIMES + [{"trip_id": "t9", "stop_id": "s1"}]
    with caplog.at_level("WARNING"):
        out = _run(tmp_path, stop_times=stop_times).set_index("neighbourhood_name")
    assert out.loc["ALPHA", "transit_dep_bus"] == pytest.approx(2.0)
    assert "trip_ids missing from trips" in caplog.text


def test_unknown_route_type_kept_as_other(tmp_path, caplog):
    routes = DEFAULT_ROUTES + [{"route_id": "rg", "route_type_descr": "Gondola"}]
    trips = DEFAULT_TRIPS + [{"trip_id": "t5", "route_id": "rg", "service_id": "wk"}]
    stop_times = DEFAULT_STOP_TIMES + [{"trip_id": "t5", "stop_id": "s1"}]
    with caplog.at_level("WARNING"):
        out = _run(
            tmp_path, routes=routes, trips=trips, stop_times=stop_times,
        ).set_index("neighbourhood_name")
    # In the total, NOT in bus or lrt.
    assert out.loc["ALPHA", "transit_dep_total"] == pytest.approx(3.0)
    assert out.loc["ALPHA", "transit_dep_bus"] == pytest.approx(2.0)
    assert "GONDOLA" in caplog.text


def test_calendar_type2_removal_subtracts(tmp_path):
    # Remove wk's Tuesday -> weight drops to 1/2 (1 of 2 weekday dates...
    # Tuesday itself stays a weekday date via another service).
    calendar = DEFAULT_CALENDAR + [
        {"service_id": "wk", "date": "2026-01-06", "exception_type": 2},
        {"service_id": "other", "date": "2026-01-06", "exception_type": 1},
    ]
    out = _run(tmp_path, calendar=calendar).set_index("neighbourhood_name")
    assert out.loc["ALPHA", "transit_dep_bus"] == pytest.approx(1.0)


def test_no_weekday_dates_hard_errors(tmp_path):
    calendar = [{"service_id": "sat", "date": "2026-01-10", "exception_type": 1}]
    with pytest.raises(ValueError, match="WEEKDAY"):
        _run(tmp_path, calendar=calendar)


def test_empty_calendar_hard_errors(tmp_path):
    calendar = [{"service_id": "wk", "date": "not-a-date", "exception_type": 1}]
    with pytest.raises(ValueError):
        _run(tmp_path, calendar=calendar)


def test_missing_column_hard_errors(tmp_path):
    stops = [{"stop_id": "s1", "stop_lat": 53.505}]  # no stop_lon
    with pytest.raises(ValueError, match="stop_lon"):
        _run(tmp_path, stops=stops)


def test_null_stop_coordinates_reported(tmp_path, caplog):
    stops = DEFAULT_STOPS + [
        {"stop_id": "s5", "stop_lat": None, "stop_lon": None, "location_type": 0, "stop_name": "NoCoord"},
    ]
    stop_times = DEFAULT_STOP_TIMES + [{"trip_id": "t1", "stop_id": "s5"}]
    with caplog.at_level("WARNING"):
        out = _run(tmp_path, stops=stops, stop_times=stop_times)
    assert out["transit_dep_total"].sum() == pytest.approx(3.0)
    assert "null coordinates" in caplog.text


# --- export_transit_stations_web ----------------------------------------------


def test_station_export_writes_type1_only(tmp_path):
    stops_csv = _write(tmp_path, "stops.csv", DEFAULT_STOPS)
    out_path = tmp_path / "web" / "transit_stations.json"
    n = export_transit_stations_web(stops_csv, out_path)
    assert n == 1
    data = json.loads(out_path.read_text(encoding="utf-8"))
    assert data == {"stations": [[-113.513, 53.507, "Central Station"]]}


def test_station_export_drops_null_coords(tmp_path, caplog):
    stops = DEFAULT_STOPS + [
        {"stop_id": "st2", "stop_lat": None, "stop_lon": None, "location_type": 1, "stop_name": "Ghost"},
    ]
    stops_csv = _write(tmp_path, "stops.csv", stops)
    with caplog.at_level("WARNING"):
        n = export_transit_stations_web(stops_csv, tmp_path / "out.json")
    assert n == 1
    assert "null coordinates" in caplog.text


def test_station_export_errors_when_no_stations(tmp_path):
    stops = [r for r in DEFAULT_STOPS if r["location_type"] != 1]
    stops_csv = _write(tmp_path, "stops.csv", stops)
    with pytest.raises(ValueError, match="location_type"):
        export_transit_stations_web(stops_csv, tmp_path / "out.json")


# --- export_transit_lines_web -------------------------------------------------


def _route_feature(route_id, name, coords):
    return {
        "type": "Feature",
        "properties": {"lrt_route_id": route_id, "lrt_route_name": name},
        "geometry": {"type": "MultiLineString", "coordinates": coords},
    }


def _write_routes(tmp_path, features):
    path = tmp_path / "lrt_routes.geojson"
    path.write_text(json.dumps({"type": "FeatureCollection", "features": features}))
    return path


def test_lines_export_flattens_multiline_and_rounds(tmp_path):
    feats = [
        _route_feature("021R", "Capital Line",
                       [[[-113.512345678, 53.501234], [-113.51, 53.50]],
                        [[-113.50, 53.49], [-113.49, 53.48]]]),
    ]
    out_path = tmp_path / "web" / "lrt_lines.json"
    n = export_transit_lines_web(_write_routes(tmp_path, feats), out_path)
    assert n == 2  # one path per MultiLineString segment
    data = json.loads(out_path.read_text(encoding="utf-8"))
    assert data["lines"][0][0] == [-113.51235, 53.50123]  # rounded to 5 dp


def test_lines_export_drops_heritage_streetcar(tmp_path):
    feats = [
        _route_feature("021R", "Capital Line", [[[-113.5, 53.5], [-113.4, 53.4]]]),
        _route_feature("HER", None, [[[-113.54, 53.53], [-113.53, 53.52]]]),
    ]
    n = export_transit_lines_web(_write_routes(tmp_path, feats), tmp_path / "out.json")
    assert n == 1  # HER excluded


def test_lines_export_skips_degenerate_single_point_paths(tmp_path):
    feats = [
        _route_feature("021R", "Capital Line",
                       [[[-113.5, 53.5]], [[-113.5, 53.5], [-113.4, 53.4]]]),
    ]
    n = export_transit_lines_web(_write_routes(tmp_path, feats), tmp_path / "out.json")
    assert n == 1  # the 1-point segment is dropped


def test_lines_export_errors_when_all_excluded(tmp_path):
    feats = [_route_feature("HER", None, [[[-113.54, 53.53], [-113.53, 53.52]]])]
    with pytest.raises(ValueError, match="drawable"):
        export_transit_lines_web(_write_routes(tmp_path, feats), tmp_path / "out.json")


def test_lines_export_errors_on_empty_file(tmp_path):
    with pytest.raises(ValueError, match="no features"):
        export_transit_lines_web(_write_routes(tmp_path, []), tmp_path / "out.json")
