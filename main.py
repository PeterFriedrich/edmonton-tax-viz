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
from aggregate_by_neighbourhood import aggregate_by_neighbourhood
from load_boundaries import load_boundaries
from join_and_calculate import join_and_calculate, export_geojson
from plot_choropleth import plot_choropleth

logger = logging.getLogger(__name__)

# --- Default paths (override via CLI) --------------------------------------
ASSESSMENT_CSV = ROOT / "data/raw/Property_Assessment_Data__Current_Calendar_Year_.csv"
BOUNDARIES_GEOJSON = ROOT / "data/raw/neighbourhoods.geojson"
PNG_OUT = ROOT / "output/edmonton_value_per_acre.png"
GEOJSON_OUT = ROOT / "web/data/neighbourhood_value_per_acre.geojson"

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
    setback_m: float = SETBACK_M,
    simplify_tolerance_m: float = SIMPLIFY_TOLERANCE_M,
) -> None:
    """Run the full pipeline. Pass png_out/geojson_out=None to skip that output."""
    aggregated = aggregate_by_neighbourhood(load_assessment(assessment_csv))
    boundaries = load_boundaries(str(boundaries_geojson))
    result = join_and_calculate(aggregated, boundaries)

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
    p.add_argument("--png-out", type=Path, default=PNG_OUT)
    p.add_argument("--geojson-out", type=Path, default=GEOJSON_OUT)
    p.add_argument("--setback-m", type=float, default=SETBACK_M)
    p.add_argument("--simplify-tolerance-m", type=float, default=SIMPLIFY_TOLERANCE_M)
    p.add_argument("--skip-png", action="store_true", help="skip the Phase 1 PNG")
    p.add_argument("--skip-geojson", action="store_true", help="skip the Phase 2 web GeoJSON")
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
        setback_m=args.setback_m,
        simplify_tolerance_m=args.simplify_tolerance_m,
    )


if __name__ == "__main__":
    main()
