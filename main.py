"""End-to-end pipeline entrypoint for the Edmonton value-per-acre analysis.

Wires the independently-runnable ``src/`` modules together in order and produces
both project outputs from a single command:

    Phase 1  static choropleth PNG   -> output/edmonton_value_per_acre.png
    Phase 2  slim web GeoJSON         -> web/data/neighbourhood_value_per_acre.geojson

This module is the single place that pins the canonical export parameters
(SETBACK_M, SIMPLIFY_TOLERANCE_M) in version-controlled code, rather than
leaving them in ad-hoc regen commands. See docs/PERFORMANCE.md for why those
values were chosen.

Usage:
    python main.py                      # run with the defaults below
    python main.py --skip-png           # web GeoJSON only (faster iteration)
    python main.py --assessment-csv ... # override any input/output path
"""

import argparse
import logging
import sys
from pathlib import Path

import geopandas as gpd

# The src/ modules are runnable in isolation and import each other by bare name,
# so put src/ on the path before importing them (matches the test suite + the
# regen snippet in session-summary).
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from load_assessment import load_assessment
from apply_tax_rates import apply_tax_rates
from aggregate_by_neighbourhood import aggregate_by_neighbourhood
from load_boundaries import load_boundaries
from load_zoning import load_zoning, export_zoning_web
from load_roads import load_roads, export_roads_web
from load_bike import load_bike, export_bike_web
from load_property_info import load_property_info
from load_stormwater import load_stormwater
from load_water import load_water
from load_franchise import load_franchise
from load_fire import load_fire_events, export_fire_stations_web
from load_transit import (
    load_transit,
    export_transit_stations_web,
    export_transit_lines_web,
)
from load_permits import load_permits, export_dev_grid
from join_and_calculate import join_and_calculate, export_geojson, load_unit_costs
from export_value_grid import export_value_grid, check_lot_acre_bounds, build_hood_lot_acres
from load_temporal import load_temporal, export_temporal_web
from revenue_by_zone import FRACTION_DECIMALS, revenue_by_zone
from plot_choropleth import plot_choropleth

logger = logging.getLogger(__name__)

# --- Default paths (override via CLI) --------------------------------------
ASSESSMENT_CSV = ROOT / "data/raw/Property_Assessment_Data__Current_Calendar_Year_.csv"
BOUNDARIES_GEOJSON = ROOT / "data/raw/neighbourhoods.geojson"
ZONING_GEOJSON = ROOT / "data/raw/zoning.geojson"
ROADS_GEOJSON = ROOT / "data/raw/roads.geojson"
BIKE_GEOJSON = ROOT / "data/raw/bike_routes.geojson"
PROPERTY_INFO_CSV = ROOT / "data/raw/Property_Info__Current_Calendar_Year_.csv"
FIRE_EVENTS_CSV = ROOT / "data/raw/fire_response.csv"
FIRE_STATIONS_CSV = ROOT / "data/raw/fire_stations.csv"
# Transit lens (SPEC_services.md "Transit lens"): the five GTFS tables are
# one logical input — load_transit needs all of them, so the lens keys its
# presence off the stops file and warns listing whichever are missing.
GTFS_STOPS_CSV = ROOT / "data/raw/gtfs_stops.csv"
GTFS_ROUTES_CSV = ROOT / "data/raw/gtfs_routes.csv"
GTFS_TRIPS_CSV = ROOT / "data/raw/gtfs_trips.csv"
GTFS_STOP_TIMES_CSV = ROOT / "data/raw/gtfs_stop_times.csv"
GTFS_CALENDAR_DATES_CSV = ROOT / "data/raw/gtfs_calendar_dates.csv"
# LRT track lines — a context layer under the transit lens (the station dots'
# companion), independent of the metric; exported when present.
LRT_ROUTES_GEOJSON = ROOT / "data/raw/lrt_routes.geojson"
PERMITS_CSV = ROOT / "data/raw/building_permits.csv"
# Temporal lens (SPEC_temporal.md): the year x hood x class SERVER-SIDE
# aggregate, ~14.8k rows — never the 5.5M-row raw dataset.
HISTORICAL_CSV = ROOT / "data/raw/assessment_historical_by_hood.csv"
MILL_RATES_JSON = ROOT / "data/mill_rates.json"
STORMWATER_RATES_JSON = ROOT / "data/stormwater_rates.json"
WATER_RATES_JSON = ROOT / "data/water_rates.json"
FRANCHISE_RATES_JSON = ROOT / "data/franchise_rates.json"
# V2 service-cost composite unit costs (SPEC_utilities decision 3) — manual,
# reviewed input like the mill rates: sourced by hand, committed, NOT part of
# the weekly refresh. Needs both the roads and fire lenses at join time.
UNIT_COSTS_JSON = ROOT / "data/city_unit_costs.json"
PNG_OUT = ROOT / "output/edmonton_value_per_acre.png"
GEOJSON_OUT = ROOT / "web/data/neighbourhood_value_per_acre.geojson"
ROADS_WEB_OUT = ROOT / "web/data/roads.geojson"
# Bike network context layer (SPEC_services.md "Transportation lens") — the
# LRT-lines pattern: geometry only, no metric (the hood plane carries it).
BIKE_WEB_OUT = ROOT / "web/data/bike_routes.json"
ZONING_WEB_OUT = ROOT / "web/data/zoning.geojson"
GRID_WEB_OUT = ROOT / "web/data/value_grid.json"
DEV_GRID_WEB_OUT = ROOT / "web/data/dev_grid.json"
FIRE_STATIONS_WEB_OUT = ROOT / "web/data/fire_stations.json"
TRANSIT_STATIONS_WEB_OUT = ROOT / "web/data/transit_stations.json"
TRANSIT_LINES_WEB_OUT = ROOT / "web/data/lrt_lines.json"
TEMPORAL_WEB_OUT = ROOT / "web/data/temporal.json"
# Committed, not under web/ — see src/load_temporal.write_archive.
TEMPORAL_ARCHIVE = ROOT / "data/temporal_archive.json"

# Assessment-year alignment: the local snapshot is 2025 data (the coverage year
# lives in Socrata metadata, not the rows — see DATA.md). Mill rates MUST match.
# A future re-download could roll the year; re-check metadata + bump this.
ASSESSMENT_YEAR = 2025

# Fire lens window: the last 3 FULL calendar years, averaged (locked decision
# 3, SPEC_services.md "Fire lens"). Pinned — an auto-rolling window could
# silently average in a partial year. Bump manually each January.
FIRE_YEARS = (2023, 2024, 2025)

# Development & Infill lens A window (SPEC_development.md, locked 2026-07-12):
# the last 5 FULL calendar years of building-permit activity, summed. Pinned —
# an auto-rolling window could silently sum in a partial year (fire-lens
# precedent). Bump manually each January (see docs/RUNBOOK.md year-roll).
PERMIT_YEARS = (2021, 2022, 2023, 2024, 2025)

# Recent (3-year) sub-window for the Development-view window toggle
# (SPEC_development.md "Lens A polish", 2026-07-13): the last 3 full years, a
# "current activity" cut alongside the 5-year base. Same pin/drift-guard rules;
# bump alongside PERMIT_YEARS each January. Kept as its own pinned tuple (not
# derived from PERMIT_YEARS) so the year-roll is explicit for both windows.
PERMIT_YEARS_RECENT = (2023, 2024, 2025)

# Long "since data start" window for the Development-view window toggle
# (SPEC_development.md "Lens A long window", 2026-07-21): the full permit record
# from PERMIT_START_YEAR through the last full year, an ANCHORED-cumulative
# window (start is fixed; only the end advances). This is the "density added
# over the era" view — the inspiration lens's 2009–2023 "homes added" snapshot.
# UNLIKE the 5yr/3yr windows, the START never slides, so the end is DERIVED from
# PERMIT_YEARS' last full year: the same manual January bump that rolls the two
# sliding windows extends this one automatically (no separate pin to forget).
# The partial-year safety still holds — PERMIT_YEARS never includes a partial
# year, so neither can this. Drives BOTH the hood choropleth (join_and_calculate
# `_long` columns) and the 100 m detail grid (export_dev_grid `_long` cells):
# early-year permit geocoding is EXCELLENT (2009–2023 at 95–98%; the lag is on
# the newest permits, 2025 ~72%), so the long-window grid is if anything better-
# geocoded than the 3yr grid (docs/DATA.md §9).
PERMIT_START_YEAR = 2009
PERMIT_YEARS_LONG = tuple(range(PERMIT_START_YEAR, PERMIT_YEARS[-1] + 1))

# Water lens tariff vintage. Unlike mill rates (which MUST match the roll
# year), the water model is a forward-looking modeled bill: the current
# verified tariff schedule applied to the current roll. 2026 = the Apr 1
# 2026 schedule (data/water_rates.json). Bump when new rates are verified;
# the legend/blurb year in web/index.html rides along.
WATER_RATE_YEAR = 2026

# Franchise lens (electricity/gas) tariff vintage — same forward-looking
# modeled-bill stance as the water lens (current verified tariffs on the
# current roll). 2026 = EDTI DAS-R (Jan 2025) + ATCO Gas North (Jan 2026)
# schedules in data/franchise_rates.json. Electricity/gas rates reset Jan 1.
FRANCHISE_RATE_YEAR = 2026

# --- Canonical web-export geometry parameters ------------------------------
# Display-only. value_per_acre is computed from true area upstream and is
# untouched by either of these. See docs/PERFORMANCE.md / docs/ARCHITECTURE.md.
SETBACK_M = 45.0             # inward buffer -> "city blocks" gaps between prisms
SIMPLIFY_TOLERANCE_M = 10.0  # Douglas-Peucker vertex cut (applied AFTER setback)
GRID_CELL_M = 100.0          # Glass-view spike grid (~35k occupied cells, 2026-07)


def run(
    assessment_csv: Path,
    boundaries_geojson: Path,
    png_out: Path | None,
    geojson_out: Path | None,
    mill_rates_json: Path = MILL_RATES_JSON,
    assessment_year: int = ASSESSMENT_YEAR,
    zoning_geojson: Path | None = ZONING_GEOJSON,
    roads_geojson: Path | None = ROADS_GEOJSON,
    bike_geojson: Path | None = BIKE_GEOJSON,
    property_info_csv: Path | None = PROPERTY_INFO_CSV,
    stormwater_rates_json: Path | None = STORMWATER_RATES_JSON,
    water_rates_json: Path | None = WATER_RATES_JSON,
    water_rate_year: int = WATER_RATE_YEAR,
    franchise_rates_json: Path | None = FRANCHISE_RATES_JSON,
    franchise_rate_year: int = FRANCHISE_RATE_YEAR,
    fire_events_csv: Path | None = FIRE_EVENTS_CSV,
    fire_stations_csv: Path | None = FIRE_STATIONS_CSV,
    fire_years: tuple[int, ...] = FIRE_YEARS,
    unit_costs_json: Path | None = UNIT_COSTS_JSON,
    permits_csv: Path | None = PERMITS_CSV,
    historical_csv: Path | None = HISTORICAL_CSV,
    permit_years: tuple[int, ...] = PERMIT_YEARS,
    permit_years_recent: tuple[int, ...] = PERMIT_YEARS_RECENT,
    permit_years_long: tuple[int, ...] = PERMIT_YEARS_LONG,
    gtfs_stops_csv: Path | None = GTFS_STOPS_CSV,
    gtfs_routes_csv: Path | None = GTFS_ROUTES_CSV,
    gtfs_trips_csv: Path | None = GTFS_TRIPS_CSV,
    gtfs_stop_times_csv: Path | None = GTFS_STOP_TIMES_CSV,
    gtfs_calendar_dates_csv: Path | None = GTFS_CALENDAR_DATES_CSV,
    lrt_routes_geojson: Path | None = LRT_ROUTES_GEOJSON,
    setback_m: float = SETBACK_M,
    simplify_tolerance_m: float = SIMPLIFY_TOLERANCE_M,
) -> None:
    """Run the full pipeline. Pass png_out/geojson_out=None to skip that output."""
    assessment = apply_tax_rates(
        load_assessment(assessment_csv), mill_rates_json, assessment_year,
    )
    aggregated = aggregate_by_neighbourhood(assessment)

    # Share of the CITYWIDE levy, computed here against the full roll — before
    # the boundary join, which can drop a neighbourhood the roll knows about.
    # Deriving it downstream (or in the browser, by summing the served features)
    # would renormalise over whatever survived, so a hood's "% of city revenue"
    # would silently depend on who else made it onto the map.
    if "total_revenue" in aggregated.columns:
        city_revenue = aggregated["total_revenue"].sum()
        # Rounded for the same reason as the zone fractions (revenue_by_zone
        # FRACTION_DECIMALS): 1e-6 here is 0.0001% of the citywide levy.
        aggregated["revenue_share_city"] = (
            aggregated["total_revenue"] / city_revenue
        ).round(FRACTION_DECIMALS)
        logger.info(
            "Citywide municipal levy $%.0f over %d neighbourhood(s); "
            "largest share %.2f%% (%s)",
            city_revenue,
            len(aggregated),
            100 * aggregated["revenue_share_city"].max(),
            aggregated.loc[aggregated["revenue_share_city"].idxmax(), "neighbourhood_name"],
        )

    boundaries = load_boundaries(str(boundaries_geojson))

    # Zoning is an optional refreshed input — degrade gracefully if the file is
    # absent (join_and_calculate omits the set-aside columns when zoning is None).
    zoning = None
    if zoning_geojson is not None and Path(zoning_geojson).exists():
        zoning = load_zoning(str(zoning_geojson), boundaries)
        # Revenue by zoning category, over the SAME polygons the Uses lens
        # colours by area — one map read two ways, so the two lenses cannot
        # disagree about what "commercial" means. Needs the levy, so it is
        # skipped on the value-only path along with everything else revenue.
        if "levy" in assessment.columns:
            aggregated = aggregated.merge(
                revenue_by_zone(assessment, gpd.read_file(str(zoning_geojson))),
                on="neighbourhood_name",
                how="left",
            )
    elif zoning_geojson is not None:
        logger.warning("Zoning file not found (%s) — skipping set-aside layer", zoning_geojson)

    # Roads are the same kind of optional refreshed input (services lens,
    # SPEC_services.md) — omitting the file just omits the road columns.
    roads = None
    if roads_geojson is not None and Path(roads_geojson).exists():
        roads = load_roads(str(roads_geojson), boundaries)
    elif roads_geojson is not None:
        logger.warning("Roads file not found (%s) — skipping road-supply layer", roads_geojson)

    # Bike routes, same optional shape (SPEC_services.md "Transportation lens").
    bike = None
    if bike_geojson is not None and Path(bike_geojson).exists():
        bike = load_bike(str(bike_geojson), boundaries)
    elif bike_geojson is not None:
        logger.warning("Bike routes file not found (%s) — skipping bike-supply layer", bike_geojson)

    # Stormwater (utility lens #1, SPEC_utilities.md — MODELED, not billed)
    # rides on inputs the pipeline already has: the property-info CSV and the
    # zoning GeoJSON (zone-null fallback). Skipped when either the rates file
    # or the property-info file is absent; the rate year is pinned to the
    # assessment year, same rule as mill rates.
    stormwater = None
    if (
        stormwater_rates_json is not None
        and property_info_csv is not None
        and Path(property_info_csv).exists()
    ):
        stormwater = load_stormwater(
            property_info_csv, stormwater_rates_json, assessment_year,
            zoning_geojson=zoning_geojson,
        )
    elif stormwater_rates_json is not None:
        logger.warning(
            "Property-info file not found (%s) — skipping the stormwater lens",
            property_info_csv,
        )

    # Water + sanitary (utility lens #2, SPEC_utilities.md — MODELED, not
    # billed; residential scope only) rides on the assessment + property-info
    # CSVs the pipeline already has. The tariff vintage is pinned separately
    # from the roll year (WATER_RATE_YEAR above).
    water = None
    if (
        water_rates_json is not None
        and property_info_csv is not None
        and Path(property_info_csv).exists()
    ):
        water = load_water(
            assessment_csv, property_info_csv, water_rates_json, water_rate_year,
        )
    elif water_rates_json is not None:
        logger.warning(
            "Property-info file not found (%s) — skipping the water lens",
            property_info_csv,
        )

    # Electricity/gas franchise revenue (utility lens #3, SPEC_utilities.md
    # Lens 3 — MODELED City-revenue columns; residential scope; collinear with
    # dwelling count, so columns only, no display layer). Shares the water
    # lens's dwelling model, so it needs the same two CSVs.
    franchise = None
    if (
        franchise_rates_json is not None
        and property_info_csv is not None
        and Path(property_info_csv).exists()
    ):
        franchise = load_franchise(
            assessment_csv, property_info_csv, franchise_rates_json,
            franchise_rate_year,
        )
    elif franchise_rates_json is not None:
        logger.warning(
            "Property-info file not found (%s) — skipping the franchise lens",
            property_info_csv,
        )

    # Fire demand (services lens #3, SPEC_services.md "Fire lens") — same
    # optional-refreshed-input pattern; omitting the file omits the columns.
    fire = None
    if fire_events_csv is not None and Path(fire_events_csv).exists():
        fire = load_fire_events(fire_events_csv, fire_years)
    elif fire_events_csv is not None:
        logger.warning("Fire events file not found (%s) — skipping the fire lens", fire_events_csv)

    # V2 service-cost composite (SPEC_utilities decision 3): load the reviewed
    # unit-cost input when present. join_and_calculate owns the roads+fire-
    # both-required guard (it skips with a warning if either lens is off).
    unit_costs = None
    if unit_costs_json is not None and Path(unit_costs_json).exists():
        unit_costs = load_unit_costs(unit_costs_json)
    elif unit_costs_json is not None:
        logger.warning(
            "Unit-costs file not found (%s) — skipping the V2 service-cost composite",
            unit_costs_json,
        )

    # Scheduled transit supply (services lens #4, SPEC_services.md "Transit
    # lens") — five GTFS tables forming ONE logical input; the lens runs only
    # when all five are present (missing ones listed), same optional-
    # refreshed-input pattern as the other services.
    transit = None
    gtfs_paths = (
        gtfs_stops_csv, gtfs_routes_csv, gtfs_trips_csv,
        gtfs_stop_times_csv, gtfs_calendar_dates_csv,
    )
    if all(p is not None for p in gtfs_paths):
        missing = [str(p) for p in gtfs_paths if not Path(p).exists()]
        if not missing:
            transit = load_transit(
                gtfs_stops_csv, gtfs_routes_csv, gtfs_trips_csv,
                gtfs_stop_times_csv, gtfs_calendar_dates_csv, boundaries,
            )
        else:
            logger.warning(
                "GTFS file(s) not found — skipping the transit lens: %s",
                ", ".join(missing),
            )

    # New residential supply (Development & Infill lens A, SPEC_development.md)
    # — same optional-refreshed-input pattern; omitting the file omits the
    # activity columns.
    permits = None
    permits_recent = None
    permits_long = None
    if permits_csv is not None and Path(permits_csv).exists():
        permits = load_permits(permits_csv, permit_years)
        # Second aggregation over the shorter window feeds the web window toggle
        # (5yr base <-> 3yr recent). Same loader, different pinned window.
        permits_recent = load_permits(permits_csv, permit_years_recent)
        # Third aggregation over the anchored "since 2009" window — the "density
        # added over the era" cut for the window toggle. Same loader, longest
        # pinned window (main.py PERMIT_YEARS_LONG).
        permits_long = load_permits(permits_csv, permit_years_long)
    elif permits_csv is not None:
        logger.warning(
            "Building-permits file not found (%s) — skipping the development lens",
            permits_csv,
        )

    # Lot-size join (property-info CSV) feeds TWO consumers: the neighbourhood
    # lot-acre denominator toggle (hood rollup, joined below) and the Glass-view
    # grid (export block). Merge once here so both share it; without the file
    # both degrade to ground-acre only. check_lot_acre_bounds validates the
    # per-hood deduped acres before either uses them.
    lot_acres_hood = None
    grid_input = assessment
    if property_info_csv is not None and Path(property_info_csv).exists():
        grid_input = assessment.merge(
            load_property_info(property_info_csv), on="account_number", how="left",
        )
        check_lot_acre_bounds(grid_input, boundaries)
        lot_acres_hood = build_hood_lot_acres(grid_input)
    elif property_info_csv is not None:
        logger.warning(
            "Property-info file not found (%s) — no lot-acre denominator "
            "(grid + neighbourhood lens ground-acre only)",
            property_info_csv,
        )

    result = join_and_calculate(
        aggregated, boundaries, zoning=zoning, roads=roads, bike=bike, stormwater=stormwater,
        fire=fire, transit=transit, water=water, franchise=franchise,
        permits=permits, permits_recent=permits_recent, permits_long=permits_long,
        lot_acres=lot_acres_hood,
        unit_costs=unit_costs,
    )

    if png_out is not None:
        png_out.parent.mkdir(parents=True, exist_ok=True)
        plot_choropleth(result, str(png_out))

    if geojson_out is not None:
        geojson_out.parent.mkdir(parents=True, exist_ok=True)
        export_geojson(
            result,
            str(geojson_out),
            setback_m=setback_m,
            simplify_tolerance_m=simplify_tolerance_m,
        )
        # Ground-layer road geometry rides with the web export (services lens
        # display architecture, SPEC_services.md) — skipped with the roads layer.
        if roads is not None:
            export_roads_web(str(roads_geojson), boundaries, str(ROADS_WEB_OUT))
        # Bike network context layer — skipped with the bike layer.
        if bike is not None:
            export_bike_web(str(bike_geojson), boundaries, str(BIKE_WEB_OUT))
        # Ground-layer zoning geometry for the Uses view (dissolved by
        # category, clipped to the same setback gaps as the prisms; display
        # only) — skipped with the zoning layer.
        if zoning is not None:
            export_zoning_web(
                str(zoning_geojson), boundaries, str(ZONING_WEB_OUT),
                setback_m=setback_m,
            )
        # Grid-cell spikes for the Glass view (Urban3-style detail). Reuses the
        # grid_input (assessment + lot_size) built above; the lot-acre variant
        # is deduped per docs/FINDINGS_lot_dedupe.md, and without the
        # property-info file grid_input is the bare assessment (ground-acre only).
        export_value_grid(grid_input, GRID_WEB_OUT, cell_m=GRID_CELL_M)
        # Per-neighbourhood assessment over time (docs/SPEC_temporal.md). A side
        # branch: it never enters the hood join, it just writes its own compact
        # file. Needs the historical aggregate, which download_data.py fetches;
        # without it the lens is simply absent, like every other optional input.
        if historical_csv is not None and Path(historical_csv).exists():
            temporal, temporal_stats = load_temporal(
                historical_csv, assessment, assessment_year,
                boundary_names=set(boundaries["neighbourhood_name"]),
                archive_path=TEMPORAL_ARCHIVE,
            )
            export_temporal_web(temporal, TEMPORAL_WEB_OUT)
        else:
            logger.warning(
                "Temporal lens skipped — %s not found (download_data.py --only "
                "assessment_historical)", historical_csv,
            )
        # 100 m new-units grid for the Development view's detail toggle —
        # rides with the permits lens (skipped with it). Needs the lat/long
        # columns (download_data $select, 2026-07-15); an older CSV degrades
        # to a warning so a stale snapshot can't fail the whole pipeline.
        if permits is not None:
            try:
                export_dev_grid(
                    permits_csv, DEV_GRID_WEB_OUT,
                    permit_years, permit_years_recent, permit_years_long,
                    cell_m=GRID_CELL_M,
                )
            except ValueError as e:
                logger.warning("Dev grid not exported: %s", e)
        # Fire-station context dots for the Services view's fire layer —
        # rides with the fire lens (skipped with it).
        if fire is not None and fire_stations_csv is not None and Path(fire_stations_csv).exists():
            export_fire_stations_web(fire_stations_csv, FIRE_STATIONS_WEB_OUT)
        elif fire is not None and fire_stations_csv is not None:
            logger.warning(
                "Fire stations file not found (%s) — station dots not exported",
                fire_stations_csv,
            )
        # Transit-station context dots (LRT stations + transit centres) for
        # the Services view's transit layer — rides with the transit lens.
        if transit is not None:
            export_transit_stations_web(gtfs_stops_csv, TRANSIT_STATIONS_WEB_OUT)
        # LRT track lines — companion context layer, exported when the LRT
        # routes file is present (independent of the GTFS metric inputs).
        if transit is not None and lrt_routes_geojson is not None and Path(lrt_routes_geojson).exists():
            export_transit_lines_web(lrt_routes_geojson, TRANSIT_LINES_WEB_OUT)
        elif transit is not None and lrt_routes_geojson is not None:
            logger.warning(
                "LRT routes file not found (%s) — track lines not exported",
                lrt_routes_geojson,
            )

    logger.info("Pipeline complete.")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--assessment-csv", type=Path, default=ASSESSMENT_CSV)
    p.add_argument("--boundaries-geojson", type=Path, default=BOUNDARIES_GEOJSON)
    p.add_argument("--zoning-geojson", type=Path, default=ZONING_GEOJSON)
    p.add_argument("--roads-geojson", type=Path, default=ROADS_GEOJSON)
    p.add_argument("--property-info-csv", type=Path, default=PROPERTY_INFO_CSV)
    p.add_argument("--mill-rates-json", type=Path, default=MILL_RATES_JSON)
    p.add_argument("--assessment-year", type=int, default=ASSESSMENT_YEAR)
    p.add_argument("--png-out", type=Path, default=PNG_OUT)
    p.add_argument("--geojson-out", type=Path, default=GEOJSON_OUT)
    p.add_argument("--setback-m", type=float, default=SETBACK_M)
    p.add_argument("--simplify-tolerance-m", type=float, default=SIMPLIFY_TOLERANCE_M)
    p.add_argument("--skip-png", action="store_true", help="skip the Phase 1 PNG")
    p.add_argument("--skip-geojson", action="store_true", help="skip the Phase 2 web GeoJSON")
    p.add_argument("--skip-zoning", action="store_true", help="skip the land-use set-aside layer")
    p.add_argument("--skip-roads", action="store_true", help="skip the road-supply layer")
    p.add_argument("--bike-geojson", type=Path, default=BIKE_GEOJSON)
    p.add_argument("--skip-bike", action="store_true", help="skip the bike-supply layer")
    p.add_argument("--skip-property-info", action="store_true",
                   help="skip the lot_size join (grid exports ground-acre only; "
                        "also skips the stormwater lens, which needs the same file)")
    p.add_argument("--skip-stormwater", action="store_true",
                   help="skip the modeled stormwater lens (SPEC_utilities.md)")
    p.add_argument("--skip-water", action="store_true",
                   help="skip the modeled water + sanitary lens (SPEC_utilities.md Lens 2)")
    p.add_argument("--skip-franchise", action="store_true",
                   help="skip the modeled electricity/gas franchise lens (SPEC_utilities.md Lens 3)")
    p.add_argument("--fire-events-csv", type=Path, default=FIRE_EVENTS_CSV)
    p.add_argument("--fire-stations-csv", type=Path, default=FIRE_STATIONS_CSV)
    p.add_argument("--skip-fire", action="store_true",
                   help="skip the fire demand lens (SPEC_services.md \"Fire lens\")")
    p.add_argument("--unit-costs-json", type=Path, default=UNIT_COSTS_JSON)
    p.add_argument("--skip-service-cost", action="store_true",
                   help="skip the V2 modeled service-cost composite (SPEC_utilities decision 3)")
    p.add_argument("--gtfs-stops-csv", type=Path, default=GTFS_STOPS_CSV)
    p.add_argument("--gtfs-routes-csv", type=Path, default=GTFS_ROUTES_CSV)
    p.add_argument("--gtfs-trips-csv", type=Path, default=GTFS_TRIPS_CSV)
    p.add_argument("--gtfs-stop-times-csv", type=Path, default=GTFS_STOP_TIMES_CSV)
    p.add_argument("--gtfs-calendar-dates-csv", type=Path, default=GTFS_CALENDAR_DATES_CSV)
    p.add_argument("--lrt-routes-geojson", type=Path, default=LRT_ROUTES_GEOJSON)
    p.add_argument("--skip-transit", action="store_true",
                   help="skip the scheduled-transit supply lens (SPEC_services.md \"Transit lens\")")
    p.add_argument("--permits-csv", type=Path, default=PERMITS_CSV)
    p.add_argument("--historical-csv", type=Path, default=HISTORICAL_CSV)
    p.add_argument("--skip-permits", action="store_true",
                   help="skip the development/infill activity lens (SPEC_development.md \"Lens A\")")
    p.add_argument("--log-level", default="INFO", help="logging level (default INFO)")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    logging.basicConfig(
        stream=sys.stdout,
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(levelname)s: %(message)s",
    )
    run(
        assessment_csv=args.assessment_csv,
        boundaries_geojson=args.boundaries_geojson,
        png_out=None if args.skip_png else args.png_out,
        geojson_out=None if args.skip_geojson else args.geojson_out,
        mill_rates_json=args.mill_rates_json,
        assessment_year=args.assessment_year,
        zoning_geojson=None if args.skip_zoning else args.zoning_geojson,
        roads_geojson=None if args.skip_roads else args.roads_geojson,
        bike_geojson=None if args.skip_bike else args.bike_geojson,
        property_info_csv=None if args.skip_property_info else args.property_info_csv,
        stormwater_rates_json=None if args.skip_stormwater else STORMWATER_RATES_JSON,
        water_rates_json=None if args.skip_water else WATER_RATES_JSON,
        franchise_rates_json=None if args.skip_franchise else FRANCHISE_RATES_JSON,
        fire_events_csv=None if args.skip_fire else args.fire_events_csv,
        fire_stations_csv=None if args.skip_fire else args.fire_stations_csv,
        unit_costs_json=None if args.skip_service_cost else args.unit_costs_json,
        gtfs_stops_csv=None if args.skip_transit else args.gtfs_stops_csv,
        gtfs_routes_csv=None if args.skip_transit else args.gtfs_routes_csv,
        gtfs_trips_csv=None if args.skip_transit else args.gtfs_trips_csv,
        gtfs_stop_times_csv=None if args.skip_transit else args.gtfs_stop_times_csv,
        gtfs_calendar_dates_csv=None if args.skip_transit else args.gtfs_calendar_dates_csv,
        lrt_routes_geojson=None if args.skip_transit else args.lrt_routes_geojson,
        permits_csv=None if args.skip_permits else args.permits_csv,
        historical_csv=args.historical_csv,
        setback_m=args.setback_m,
        simplify_tolerance_m=args.simplify_tolerance_m,
    )


if __name__ == "__main__":
    main()
