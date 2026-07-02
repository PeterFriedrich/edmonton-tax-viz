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
from load_zoning import load_zoning
from load_roads import load_roads
from join_and_calculate import join_and_calculate, export_geojson
from plot_choropleth import plot_choropleth

logger = logging.getLogger(__name__)

# --- Default paths (override via CLI) --------------------------------------
ASSESSMENT_CSV = ROOT / "data/raw/Property_Assessment_Data__Current_Calendar_Year_.csv"
BOUNDARIES_GEOJSON = ROOT / "data/raw/neighbourhoods.geojson"
ZONING_GEOJSON = ROOT / "data/raw/zoning.geojson"
ROADS_GEOJSON = ROOT / "data/raw/roads.geojson"
MILL_RATES_JSON = ROOT / "data/mill_rates.json"
PNG_OUT = ROOT / "output/edmonton_value_per_acre.png"
GEOJSON_OUT = ROOT / "web/data/neighbourhood_value_per_acre.geojson"

# Assessment-year alignment: the local snapshot is 2025 data (the coverage year
# lives in Socrata metadata, not the rows — see DATA.md). Mill rates MUST match.
# A future re-download could roll the year; re-check metadata + bump this.
ASSESSMENT_YEAR = 2025

# --- Canonical web-export geometry parameters ------------------------------
# Display-only. value_per_acre is computed from true area upstream and is
# untouched by either of these. See docs/PERFORMANCE.md / docs/ARCHITECTURE.md.
SETBACK_M = 45.0             # inward buffer -> "city blocks" gaps between prisms
SIMPLIFY_TOLERANCE_M = 10.0  # Douglas-Peucker vertex cut (applied AFTER setback)


def run(
    assessment_csv: Path,
    boundaries_geojson: Path,
    png_out: Path | None,
    geojson_out: Path | None,
    mill_rates_json: Path = MILL_RATES_JSON,
    assessment_year: int = ASSESSMENT_YEAR,
    zoning_geojson: Path | None = ZONING_GEOJSON,
    roads_geojson: Path | None = ROADS_GEOJSON,
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

    result = join_and_calculate(aggregated, boundaries, zoning=zoning, roads=roads)

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

    logger.info("Pipeline complete.")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--assessment-csv", type=Path, default=ASSESSMENT_CSV)
    p.add_argument("--boundaries-geojson", type=Path, default=BOUNDARIES_GEOJSON)
    p.add_argument("--zoning-geojson", type=Path, default=ZONING_GEOJSON)
    p.add_argument("--roads-geojson", type=Path, default=ROADS_GEOJSON)
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
        setback_m=args.setback_m,
        simplify_tolerance_m=args.simplify_tolerance_m,
    )


if __name__ == "__main__":
    main()
