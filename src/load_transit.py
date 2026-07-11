"""Scheduled transit service per neighbourhood (services lens, fourth service).

Counts scheduled transit stop-events (departures) per neighbourhood on a
mean weekday from the ETS GTFS static feed, published as five Socrata
tables (stops / routes / trips / stop_times / calendar_dates). Design +
the two locked decisions: docs/SPEC_services.md "Transit lens"; dataset
facts DATA.md §9.

**Scheduled service, not usage.** ETS publishes no stop- or
neighbourhood-level ridership (probed 2026-07-11), so this is a supply
proxy counted from the published schedule — never present it as a
ridership, cost, or coverage claim. On-demand transit zones are not in the
GTFS and are invisible to this metric (documented limitation).

**Feed window semantics:** the feed is a snapshot of the CURRENT signup
only (e.g. the summer schedule — the seasonal service low). The metric
steps at signup boundaries under the weekly refresh; the window is logged
every load and the display carries the current-signup caveat. Like roads,
provenance is the download date, not a roll year.

Every scheduled stop-time row counts as one stop-event (the final stop of
a trip is arrival-only; counted anyway — the honest name is "scheduled
stop-events"). Weekday = Mon–Fri dates active in calendar_dates; the
per-service weekday-day count weights its trips, so no per-date loop is
needed.
"""

import json
import logging
from pathlib import Path

import geopandas as gpd
import pandas as pd

logger = logging.getLogger(__name__)

# GTFS route_type_descr -> mode group. Explicit, every value hand-assigned
# (the ZONE_CATEGORY philosophy); unknown values are KEPT in the total under
# "other" and logged loudly — they are presumably real scheduled service.
ROUTE_MODE = {
    "BUS": "bus",
    "TRAM, STREETCAR, LIGHT RAIL": "lrt",
}

# Working/projected CRS for the stop -> neighbourhood point-in-polygon; the
# boundary frame from load_boundaries is already in it.
PROJECTED_CRS = "EPSG:3400"

# LRT route_ids to DROP from the track-line context layer. HER is the High
# Level Bridge heritage streetcar (volunteer-run, seasonal) — NOT ETS LRT
# service, so it's absent from the GTFS TRAM/LIGHT-RAIL routes the metric
# counts. Drawing it would put track on the map the lens doesn't measure.
# Explicit exclude set (the ROUTE_MODE philosophy): surprises are logged.
EXCLUDED_LRT_ROUTE_IDS = {"HER"}


def _read_calendar(calendar_dates_csv: str | Path) -> tuple[pd.DataFrame, int]:
    """Active (service_id, date) pairs on weekdays + the weekday-date count.

    The ETS feed is calendar-dates-only: every active service day is an
    exception_type 1 row. Type-2 (removed) rows are honoured generically by
    subtracting matching pairs, and counted either way.
    """
    cal = pd.read_csv(calendar_dates_csv, dtype={"service_id": str})
    for needed in ("service_id", "date", "exception_type"):
        if needed not in cal.columns:
            raise ValueError(
                f"expected column {needed!r} not in {calendar_dates_csv} — "
                f"headers: {list(cal.columns)}"
            )
    when = pd.to_datetime(cal["date"], errors="coerce", format="mixed")
    unparsed = when.isna()
    if unparsed.any():
        logger.warning(
            "%d calendar_dates rows have unparseable dates — excluded",
            int(unparsed.sum()),
        )
    cal = cal.loc[~unparsed].copy()
    cal["date"] = when.loc[~unparsed].dt.normalize()

    exc = pd.to_numeric(cal["exception_type"], errors="coerce")
    added = cal.loc[exc == 1, ["service_id", "date"]]
    removed = cal.loc[exc == 2, ["service_id", "date"]]
    other = int((~exc.isin([1, 2])).sum())
    if other:
        logger.warning("%d calendar_dates rows with exception_type not in {1,2} — ignored", other)
    if len(removed):
        logger.info("calendar_dates: %d type-2 (removed) rows subtracted", len(removed))
        added = (
            added.merge(removed, on=["service_id", "date"], how="left", indicator=True)
            .query("_merge == 'left_only'")
            .drop(columns="_merge")
        )
    if added.empty:
        raise ValueError(f"no active service dates in {calendar_dates_csv} — wrong/empty feed")

    logger.info(
        "GTFS feed window: %s -> %s (%d active service-date pairs)",
        added["date"].min().date(), added["date"].max().date(), len(added),
    )

    weekday = added.loc[added["date"].dt.weekday < 5]
    n_weekday_dates = weekday["date"].nunique()
    if n_weekday_dates == 0:
        raise ValueError(
            f"calendar_dates in {calendar_dates_csv} contains no active WEEKDAY "
            f"dates — wrong/empty feed (the mean-weekday metric is undefined)"
        )
    logger.info("%d distinct weekday dates in the feed window", n_weekday_dates)

    per_service = (
        weekday.groupby("service_id", as_index=False)
        .size()
        .rename(columns={"size": "weekday_days"})
    )
    return per_service, n_weekday_dates


def load_transit(
    stops_csv: str | Path,
    routes_csv: str | Path,
    trips_csv: str | Path,
    stop_times_csv: str | Path,
    calendar_dates_csv: str | Path,
    boundaries: gpd.GeoDataFrame,
) -> pd.DataFrame:
    """Mean-weekday scheduled stop-events per neighbourhood, by mode.

    Returns a DataFrame:
        neighbourhood_name  str
        transit_dep_bus     float  mean-weekday scheduled bus stop-events
        transit_dep_lrt     float  mean-weekday scheduled LRT stop-events
        transit_dep_total   float  all modes (bus + lrt + any unknown "other")

    A hood absent from the result has no served stops — join_and_calculate
    fills the true 0 (roads semantics). Stop-events at stops outside every
    boundary polygon (regional stops), at unknown stop_ids, or at stops with
    null coordinates form the reported "unassigned" bucket; the conservation
    check requires assigned + unassigned == citywide total.
    """
    per_service, n_weekday_dates = _read_calendar(calendar_dates_csv)

    # --- routes -> mode -------------------------------------------------------
    routes = pd.read_csv(routes_csv, dtype=str)
    for needed in ("route_id", "route_type_descr"):
        if needed not in routes.columns:
            raise ValueError(
                f"expected column {needed!r} not in {routes_csv} — headers: "
                f"{list(routes.columns)}"
            )
    descr = routes["route_type_descr"].astype("string").str.strip().str.upper()
    routes["mode"] = descr.map(ROUTE_MODE)
    unknown_types = sorted(descr[routes["mode"].isna()].dropna().unique())
    if unknown_types:
        logger.warning(
            "route_type_descr values not in ROUTE_MODE — KEPT in the total as "
            "'other' (presumed real service), review + add to ROUTE_MODE: %s",
            unknown_types,
        )
    routes["mode"] = routes["mode"].fillna("other")
    logger.info(
        "Routes by mode: %s",
        ", ".join(f"{m}: {n}" for m, n in routes["mode"].value_counts().items()),
    )

    # --- trips: trip -> (service, mode) ---------------------------------------
    trips = pd.read_csv(trips_csv, dtype=str)
    for needed in ("trip_id", "route_id", "service_id"):
        if needed not in trips.columns:
            raise ValueError(
                f"expected column {needed!r} not in {trips_csv} — headers: "
                f"{list(trips.columns)}"
            )
    trips = trips.merge(routes[["route_id", "mode"]], on="route_id", how="left")
    no_route = trips["mode"].isna()
    if no_route.any():
        logger.warning(
            "%d trips reference route_ids missing from routes — kept as 'other': %s",
            int(no_route.sum()),
            sorted(trips.loc[no_route, "route_id"].unique())[:10],
        )
        trips["mode"] = trips["mode"].fillna("other")

    # Weekday weight per service: active weekday days / all weekday dates.
    # Weekend-only services (or services absent from calendar_dates) weigh 0.
    trips = trips.merge(per_service, on="service_id", how="left")
    no_cal = trips["weekday_days"].isna()
    n_no_cal_services = trips.loc[no_cal, "service_id"].nunique()
    if n_no_cal_services:
        logger.info(
            "%d service_id(s) on %d trips have no active weekday dates "
            "(weekend-only or absent from calendar_dates) — weight 0",
            n_no_cal_services, int(no_cal.sum()),
        )
    trips["weekday_days"] = trips["weekday_days"].fillna(0)
    trips["weight"] = trips["weekday_days"] / n_weekday_dates

    # --- stop_times: count scheduled stop-events per (trip, stop) -------------
    stop_times = pd.read_csv(stop_times_csv, dtype=str)
    for needed in ("trip_id", "stop_id"):
        if needed not in stop_times.columns:
            raise ValueError(
                f"expected column {needed!r} not in {stop_times_csv} — headers: "
                f"{list(stop_times.columns)}"
            )
    n_events_raw = len(stop_times)
    per_trip_stop = (
        stop_times.groupby(["trip_id", "stop_id"], as_index=False)
        .size()
        .rename(columns={"size": "n_events"})
    )
    per_trip_stop = per_trip_stop.merge(
        trips[["trip_id", "mode", "weight"]], on="trip_id", how="left",
    )
    orphan = per_trip_stop["weight"].isna()
    if orphan.any():
        n_orphan_events = int(per_trip_stop.loc[orphan, "n_events"].sum())
        logger.warning(
            "%d stop-time rows reference trip_ids missing from trips — "
            "excluded (referential break, %d distinct trips)",
            n_orphan_events,
            per_trip_stop.loc[orphan, "trip_id"].nunique(),
        )
        per_trip_stop = per_trip_stop.loc[~orphan]

    # Mean-weekday events per (stop, mode): n_events × the trip's weekday weight.
    per_trip_stop["dep"] = per_trip_stop["n_events"] * per_trip_stop["weight"]
    per_stop = (
        per_trip_stop.groupby(["stop_id", "mode"], as_index=False)["dep"].sum()
    )
    citywide = float(per_stop["dep"].sum())
    logger.info(
        "Citywide mean-weekday scheduled stop-events: %.0f (%s) from %d "
        "stop-time rows over %d weekday dates",
        citywide,
        ", ".join(
            f"{m}: {v:,.0f}"
            for m, v in per_stop.groupby("mode")["dep"].sum().items()
        ),
        n_events_raw, n_weekday_dates,
    )

    # --- stops -> neighbourhood (point-in-polygon) ----------------------------
    stops = pd.read_csv(stops_csv, dtype=str)
    for needed in ("stop_id", "stop_lat", "stop_lon"):
        if needed not in stops.columns:
            raise ValueError(
                f"expected column {needed!r} not in {stops_csv} — headers: "
                f"{list(stops.columns)}"
            )
    lat = pd.to_numeric(stops["stop_lat"], errors="coerce")
    lon = pd.to_numeric(stops["stop_lon"], errors="coerce")
    bad_coord = lat.isna() | lon.isna()
    if bad_coord.any():
        logger.warning(
            "%d stop row(s) have null coordinates — their stop-events fall in "
            "the unassigned bucket", int(bad_coord.sum()),
        )
    stop_pts = gpd.GeoDataFrame(
        stops.loc[~bad_coord, ["stop_id"]],
        geometry=gpd.points_from_xy(lon[~bad_coord], lat[~bad_coord]),
        crs="EPSG:4326",
    ).to_crs(PROJECTED_CRS)

    hoods = boundaries[["neighbourhood_name", "geometry"]].to_crs(PROJECTED_CRS)
    stop_hood = gpd.sjoin(stop_pts, hoods, how="left", predicate="within")
    dupes = stop_hood.index.duplicated(keep="first")
    if dupes.any():
        logger.warning(
            "%d stop(s) matched multiple neighbourhood polygons (boundary-"
            "coincident points) — first match kept", int(dupes.sum()),
        )
        stop_hood = stop_hood.loc[~dupes]
    stop_hood = stop_hood[["stop_id", "neighbourhood_name"]]

    # --- assign events to hoods + conservation check --------------------------
    per_stop = per_stop.merge(stop_hood, on="stop_id", how="left")
    unassigned = per_stop["neighbourhood_name"].isna()
    unassigned_dep = float(per_stop.loc[unassigned, "dep"].sum())
    if unassigned.any():
        logger.info(
            "%d served stop(s) outside every neighbourhood polygon, unknown, "
            "or coordinate-less — %.0f mean-weekday stop-events (%.1f%% of "
            "citywide) in the unassigned bucket (regional stops expected)",
            int(unassigned.sum()), unassigned_dep,
            100 * unassigned_dep / citywide if citywide else 0.0,
        )

    assigned = per_stop.loc[~unassigned]
    total_check = float(assigned["dep"].sum()) + unassigned_dep
    if abs(total_check - citywide) > 1e-6 * max(citywide, 1.0):
        raise AssertionError(
            f"conservation check failed: assigned + unassigned = {total_check} "
            f"!= citywide {citywide}"
        )

    per_hood_mode = (
        assigned.groupby(["neighbourhood_name", "mode"])["dep"].sum().unstack(fill_value=0.0)
    )
    for mode in ("bus", "lrt"):
        if mode not in per_hood_mode.columns:
            per_hood_mode[mode] = 0.0
    out = pd.DataFrame({
        "neighbourhood_name": per_hood_mode.index,
        "transit_dep_bus": per_hood_mode["bus"].values,
        "transit_dep_lrt": per_hood_mode["lrt"].values,
        # total = every mode incl. any unknown "other" (kept, logged above)
        "transit_dep_total": per_hood_mode.sum(axis=1).values,
    })

    logger.info(
        "Transit supply: %d hoods, %.0f assigned mean-weekday stop-events "
        "(bus %.0f, LRT %.0f)",
        len(out), out["transit_dep_total"].sum(),
        out["transit_dep_bus"].sum(), out["transit_dep_lrt"].sum(),
    )
    return out


def export_transit_stations_web(stops_csv: str | Path, out_path: str | Path) -> int:
    """Write the station context dots for the web map's transit layer.

    GTFS ``location_type == 1`` rows (LRT stations + transit centres) as a
    tiny committed JSON — ``{"stations": [[lon, lat, label], ...]}`` — the
    fire-station pattern, lazy-loaded by the Services view. Returns the
    station count. Null-coordinate rows dropped + reported, never silently.
    """
    stops = pd.read_csv(stops_csv, dtype=str)
    for needed in ("stop_lat", "stop_lon", "location_type"):
        if needed not in stops.columns:
            raise ValueError(
                f"expected column {needed!r} not in {stops_csv} — headers: "
                f"{list(stops.columns)}"
            )
    loc_type = pd.to_numeric(stops["location_type"], errors="coerce")
    st = stops.loc[loc_type == 1].copy()
    if st.empty:
        raise ValueError(f"no location_type==1 stations in {stops_csv}")

    lat = pd.to_numeric(st["stop_lat"], errors="coerce")
    lon = pd.to_numeric(st["stop_lon"], errors="coerce")
    bad = lat.isna() | lon.isna()
    if bad.any():
        logger.warning("%d station row(s) have null coordinates — dropped", int(bad.sum()))

    labels = (
        st["stop_name"].fillna("") if "stop_name" in st.columns
        else pd.Series("", index=st.index)
    )
    stations = [
        [round(float(x), 5), round(float(y), 5), str(lbl)]
        for x, y, lbl, b in zip(lon, lat, labels, bad)
        if not b
    ]
    if not stations:
        raise ValueError(f"no stations with coordinates in {stops_csv}")

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"stations": stations}, f, separators=(",", ":"), ensure_ascii=False)
    logger.info("Wrote %d transit stations to %s", len(stations), out_path)
    return len(stations)


def export_transit_lines_web(lrt_routes_geojson: str | Path, out_path: str | Path) -> int:
    """Write the LRT track lines for the web map's transit layer.

    A context layer (the LRT-station dots' companion), NOT part of the
    stop-events metric. Reads the "LRT Routes" GeoJSON (four route
    multilines), drops the HER heritage streetcar (``EXCLUDED_LRT_ROUTE_IDS``
    — not ETS LRT service), and flattens each remaining route's
    MultiLineString into individual paths. Writes a tiny committed JSON —
    ``{"lines": [[[lon, lat], ...], ...]}`` — the station-dots pattern, lazy-
    loaded by the Services view. Returns the path (segment) count.
    """
    with open(lrt_routes_geojson, encoding="utf-8") as f:
        fc = json.load(f)
    feats = fc.get("features", [])
    if not feats:
        raise ValueError(f"no features in {lrt_routes_geojson} — wrong/empty file")

    lines: list[list[list[float]]] = []
    kept, dropped = [], []
    for feat in feats:
        props = feat.get("properties") or {}
        rid = props.get("lrt_route_id")
        name = props.get("lrt_route_name") or rid
        if rid in EXCLUDED_LRT_ROUTE_IDS:
            dropped.append(name or rid)
            continue
        geom = feat.get("geometry") or {}
        gtype = geom.get("type")
        coords = geom.get("coordinates") or []
        # MultiLineString -> list of paths; LineString -> single path.
        parts = coords if gtype == "MultiLineString" else [coords]
        if gtype not in ("MultiLineString", "LineString"):
            logger.warning("LRT route %s has unexpected geometry %s — skipped", name, gtype)
            continue
        n_before = len(lines)
        for part in parts:
            path = [[round(float(x), 5), round(float(y), 5)] for x, y in part]
            if len(path) >= 2:
                lines.append(path)
        kept.append(f"{name} ({len(lines) - n_before} segs)")

    if not lines:
        raise ValueError(f"no drawable LRT track segments in {lrt_routes_geojson}")

    logger.info(
        "LRT track lines: kept %s; dropped %s",
        ", ".join(kept), ", ".join(dropped) or "none",
    )

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"lines": lines}, f, separators=(",", ":"), ensure_ascii=False)
    logger.info("Wrote %d LRT track segments to %s", len(lines), out_path)
    return len(lines)
