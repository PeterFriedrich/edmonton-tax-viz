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
from load_property_info import load_property_info
from load_stormwater import load_stormwater
from load_fire import load_fire_events, export_fire_stations_web
from join_and_calculate import join_and_calculate, export_geojson
from export_value_grid import export_value_grid, check_lot_acre_bounds
from plot_choropleth import plot_choropleth

logger = logging.getLogger(__name__)

# --- Default paths (override via CLI) --------------------------------------
ASSESSMENT_CSV = ROOT / "data/raw/Property_Assessment_Data__Current_Calendar_Year_.csv"
BOUNDARIES_GEOJSON = ROOT / "data/raw/neighbourhoods.geojson"
ZONING_GEOJSON = ROOT / "data/raw/zoning.geojson"
ROADS_GEOJSON = ROOT / "data/raw/roads.geojson"
PROPERTY_INFO_CSV = ROOT / "data/raw/Property_Info__Current_Calendar_Year_.csv"
FIRE_EVENTS_CSV = ROOT / "data/raw/fire_response.csv"
FIRE_STATIONS_CSV = ROOT / "data/raw/fire_stations.csv"
MILL_RATES_JSON = ROOT / "data/mill_rates.json"
STORMWATER_RATES_JSON = ROOT / "data/stormwater_rates.json"
PNG_OUT = ROOT / "output/edmonton_value_per_acre.png"
GEOJSON_OUT = ROOT / "web/data/neighbourhood_value_per_acre.geojson"
ROADS_WEB_OUT = ROOT / "web/data/roads.geojson"
ZONING_WEB_OUT = ROOT / "web/data/zoning.geojson"
GRID_WEB_OUT = ROOT / "web/data/value_grid.json"
FIRE_STATIONS_WEB_OUT = ROOT / "web/data/fire_stations.json"

# Assessment-year alignment: the local snapshot is 2025 data (the coverage year
# lives in Socrata metadata, not the rows — see DATA.md). Mill rates MUST match.
# A future re-download could roll the year; re-check metadata + bump this.
ASSESSMENT_YEAR = 2025

# Fire lens window: the last 3 FULL calendar years, averaged (locked decision
# 3, SPEC_services.md "Fire lens"). Pinned — an auto-rolling window could
# silently average in a partial year. Bump manually each January.
FIRE_YEARS = (2023, 2024, 2025)

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
    property_info_csv: Path | None = PROPERTY_INFO_CSV,
    stormwater_rates_json: Path | None = STORMWATER_RATES_JSON,
    fire_events_csv: Path | None = FIRE_EVENTS_CSV,
    fire_stations_csv: Path | None = FIRE_STATIONS_CSV,
    fire_years: tuple[int, ...] = FIRE_YEARS,
    setback_m: float = SETBACK_M,
    simplify_tolerance_m: float = SIMPLIFY_TOLERANCE_M,
) -> None:
    """Run the full pipeline. Pass png_out/geojson_out=None to skip that output."""
    assessment = apply_tax_rates(
        load_assessment(assessment_csv), mill_rates_json, assessment_year,
    )
    aggregated = aggregate_by_neighbourhood(assessment)
    boundaries = load_boundaries(str(boundaries_geojson))

    # Zoning is an optional refreshed input — degrade gracefully if the file is
    # absent (join_and_calculate omits the set-aside columns when zoning is None).
    zoning = None
    if zoning_geojson is not None and Path(zoning_geojson).exists():
        zoning = load_zoning(str(zoning_geojson), boundaries)
    elif zoning_geojson is not None:
        logger.warning("Zoning file not found (%s) — skipping set-aside layer", zoning_geojson)

    # Roads are the same kind of optional refreshed input (services lens,
    # SPEC_services.md) — omitting the file just omits the road columns.
    roads = None
    if roads_geojson is not None and Path(roads_geojson).exists():
        roads = load_roads(str(roads_geojson), boundaries)
    elif roads_geojson is not None:
        logger.warning("Roads file not found (%s) — skipping road-supply layer", roads_geojson)

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

    # Fire demand (services lens #3, SPEC_services.md "Fire lens") — same
    # optional-refreshed-input pattern; omitting the file omits the columns.
    fire = None
    if fire_events_csv is not None and Path(fire_events_csv).exists():
        fire = load_fire_events(fire_events_csv, fire_years)
    elif fire_events_csv is not None:
        logger.warning("Fire events file not found (%s) — skipping the fire lens", fire_events_csv)

    result = join_and_calculate(
        aggregated, boundaries, zoning=zoning, roads=roads, stormwater=stormwater,
        fire=fire,
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
        # Ground-layer zoning geometry for the Uses view (dissolved by
        # category, clipped to the same setback gaps as the prisms; display
        # only) — skipped with the zoning layer.
        if zoning is not None:
            export_zoning_web(
                str(zoning_geojson), boundaries, str(ZONING_WEB_OUT),
                setback_m=setback_m,
            )
        # Grid-cell spikes for the Glass view (Urban3-style detail). The
        # lot_size join adds the lot-acre denominator variant (deduped per
        # docs/FINDINGS_lot_dedupe.md); without the property-info file the
        # grid degrades to ground-acre only.
        grid_input = assessment
        if property_info_csv is not None and Path(property_info_csv).exists():
            grid_input = assessment.merge(
                load_property_info(property_info_csv), on="account_number", how="left",
            )
            check_lot_acre_bounds(grid_input, boundaries)
        elif property_info_csv is not None:
            logger.warning(
                "Property-info file not found (%s) — grid exports ground-acre only",
                property_info_csv,
            )
        export_value_grid(grid_input, GRID_WEB_OUT, cell_m=GRID_CELL_M)
        # Fire-station context dots for the Services view's fire layer —
        # rides with the fire lens (skipped with it).
        if fire is not None and fire_stations_csv is not None and Path(fire_stations_csv).exists():
            export_fire_stations_web(fire_stations_csv, FIRE_STATIONS_WEB_OUT)
        elif fire is not None and fire_stations_csv is not None:
            logger.warning(
                "Fire stations file not found (%s) — station dots not exported",
                fire_stations_csv,
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
    p.add_argument("--skip-property-info", action="store_true",
                   help="skip the lot_size join (grid exports ground-acre only; "
                        "also skips the stormwater lens, which needs the same file)")
    p.add_argument("--skip-stormwater", action="store_true",
                   help="skip the modeled stormwater lens (SPEC_utilities.md)")
    p.add_argument("--fire-events-csv", type=Path, default=FIRE_EVENTS_CSV)
    p.add_argument("--fire-stations-csv", type=Path, default=FIRE_STATIONS_CSV)
    p.add_argument("--skip-fire", action="store_true",
                   help="skip the fire demand lens (SPEC_services.md \"Fire lens\")")
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
        property_info_csv=None if args.skip_property_info else args.property_info_csv,
        stormwater_rates_json=None if args.skip_stormwater else STORMWATER_RATES_JSON,
        fire_events_csv=None if args.skip_fire else args.fire_events_csv,
        fire_stations_csv=None if args.skip_fire else args.fire_stations_csv,
        setback_m=args.setback_m,
        simplify_tolerance_m=args.simplify_tolerance_m,
    )


if __name__ == "__main__":
    main()
