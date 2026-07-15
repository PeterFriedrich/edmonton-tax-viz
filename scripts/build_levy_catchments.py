#!/usr/bin/env python3
"""Build approximate fire-hall off-site levy catchment polygons (debt lens D0).

The 12 fire-hall off-site levy catchments are published ONLY as a raster map
exhibit (Schedule A of Bylaw 19340) — no GIS vector layer exists anywhere. See
docs/FINDINGS_offsite_levy_catchments.md for the full source investigation.

This script APPROXIMATES each catchment as a union of existing City
neighbourhoods (data/raw/neighbourhoods.geojson), read off Schedule A against a
labelled render of the neighbourhood grid. It is a manual-reviewed input (like
scripts/fetch_fir_debt.py) — the assignment table below is meant to be edited by
a human, not auto-derived. It is NOT part of the weekly refresh.

Two catchment pairs cannot be separated by neighbourhood union because the far
greenfield grid is a single giant hood per corner — per the 2026-07-15 decision
they are MERGED to the grid:
  - EETP + Northeast EETP  -> "EETP"        (one 5,334 ha hood spans both)
  - Horse Hill + NE Horse Hill -> "Horse Hill" (rural hoods 2-3x the catchments)

Output: data/levy_catchments.geojson (WGS84), one feature per catchment unit,
carrying the brief's levy attributes + the computed union area + a QA ratio +
an explicit approximation flag. No silent drops: any assignment name not found
in the neighbourhood layer aborts the build.

Usage:
    python scripts/build_levy_catchments.py
    python scripts/build_levy_catchments.py --qa   # also write a QA overlay PNG
"""
from __future__ import annotations
import argparse
import json
import logging
import sys
from pathlib import Path

import geopandas as gpd
from shapely.ops import unary_union

log = logging.getLogger("build_levy_catchments")

# EPSG:3400 (Alberta 3TM 114) — project standard for area in metres.
AREA_CRS = 3400

# --- Brief attributes: 2026 Off-Site Levies Approved Rates (edmonton.ca).
# facility_cost = single fire-hall cost funded by the catchment ($).
# assessable_ha = the levy's assessable-area denominator (facility_cost / rate);
#   this is NET assessable land, always <= a gross neighbourhood-union area.
LEVY_TABLE = {
    "Wedgewood":            {"facility_cost": 26_143_915, "assessable_ha": 622,   "rate_per_ha": 42_032},
    "Blatchford":           {"facility_cost": 25_757_959, "assessable_ha": 785,   "rate_per_ha": 32_813},
    "Riverview":            {"facility_cost": 26_143_915, "assessable_ha": 838,   "rate_per_ha": 31_198},
    "Horse Hill":           {"facility_cost": 26_143_915, "assessable_ha": 905,   "rate_per_ha": 28_888},
    "Northeast Horse Hill": {"facility_cost": 26_143_915, "assessable_ha": 963,   "rate_per_ha": 27_148},
    "Mistatim Industrial":  {"facility_cost": 26_143_915, "assessable_ha": 1_102, "rate_per_ha": 23_724},
    "Southeast":            {"facility_cost": 26_143_915, "assessable_ha": 1_181, "rate_per_ha": 22_137},
    "Walker":               {"facility_cost": 24_043_915, "assessable_ha": 1_095, "rate_per_ha": 21_958},
    "Big Lake":             {"facility_cost": 26_143_915, "assessable_ha": 1_214, "rate_per_ha": 21_535},
    "EETP":                 {"facility_cost": 26_143_915, "assessable_ha": 1_268, "rate_per_ha": 20_618},
    "Cumberland":           {"facility_cost": 26_143_915, "assessable_ha": 1_338, "rate_per_ha": 19_540},
    "Northeast EETP":       {"facility_cost": 26_143_915, "assessable_ha": 2_040, "rate_per_ha": 12_816},
}

# Catchment pairs merged to the neighbourhood grid (see module docstring).
MERGE_GROUPS = {
    "EETP":       ["EETP", "Northeast EETP"],
    "Horse Hill": ["Horse Hill", "Northeast Horse Hill"],
}

# --- Assignment: catchment unit -> member neighbourhoods (name column).
# Read off Schedule A (data/raw/offsite_levy/ScheduleA_catchment_map.jpg) vs a
# labelled render of neighbourhoods.geojson, 2026-07-15. APPROXIMATE — edit here.
CATCHMENT_HOODS = {
    # -- developed-edge catchments: neighbourhood union is faithful --
    "Wedgewood":  ["WEDGEWOOD HEIGHTS", "ANTHONY HENDAY SOUTH WEST", "CAMERON HEIGHTS"],
    "Riverview":  ["RIVERVIEW AREA", "RIVER'S EDGE"],
    "Big Lake":   ["TRUMPETER AREA", "STARLING", "HAWKS RIDGE", "KINGLET GARDENS",
                   "PINTAIL LANDING", "ANTHONY HENDAY BIG LAKE"],
    "Walker":     ["WALKER", "CHARLESWORTH", "SUMMERSIDE", "MELTWATER"],
    "Southeast":  ["DECOTEAU", "ALCES"],
    "Mistatim Industrial": ["MISTATIM INDUSTRIAL", "ANTHONY HENDAY MISTATIM", "RAMPART INDUSTRIAL"],
    "Cumberland": ["GOODRIDGE CORNERS", "ANTHONY HENDAY CASTLEDOWNS", "ANTHONY HENDAY RAMPART",
                   "ALBANY", "RAPPERSWILL", "CANOSSA", "CUMBERLAND"],
    # -- under-coverage: catchment is larger than the only mapped hood (flag) --
    "Blatchford": ["BLATCHFORD AREA"],
    # -- merged to grid (grid too coarse to separate the component catchments) --
    "EETP":       ["EDMONTON ENERGY AND TECHNOLOGY PARK"],
    "Horse Hill": ["ANTHONY HENDAY HORSE HILL", "RURAL NORTH EAST HORSE HILL", "MARQUIS",
                   "RURAL NORTH EAST SOUTH STURGEON", "EVERGREEN", "QUARRY RIDGE"],
}

# QA ratio band: gross union area / brief assessable area. Gross >= assessable is
# expected, so >1 is normal; these bounds only flag likely mis-assignment.
RATIO_LO, RATIO_HI = 0.85, 1.5


def merged_attrs(unit: str) -> dict:
    """Brief attributes for a unit, summing component catchments if merged."""
    parts = MERGE_GROUPS.get(unit, [unit])
    cost = sum(LEVY_TABLE[p]["facility_cost"] for p in parts)
    ass = sum(LEVY_TABLE[p]["assessable_ha"] for p in parts)
    return {
        "components": parts,
        "facility_cost_total": cost,
        "assessable_ha_brief": ass,
        "rate_per_ha_blended": round(cost / ass),
        "merged": len(parts) > 1,
    }


def build(hoods_path: Path, out_path: Path) -> gpd.GeoDataFrame:
    hoods = gpd.read_file(hoods_path).to_crs(AREA_CRS)
    names = set(hoods["name"])

    # No silent drops: every assigned hood must exist.
    missing = {h for hs in CATCHMENT_HOODS.values() for h in hs if h not in names}
    if missing:
        raise SystemExit(f"ABORT: assignment names not in neighbourhood layer: {sorted(missing)}")

    used = [h for hs in CATCHMENT_HOODS.values() for h in hs]
    dupes = {h for h in used if used.count(h) > 1}
    if dupes:
        raise SystemExit(f"ABORT: hood assigned to >1 catchment: {sorted(dupes)}")

    records = []
    for unit, member_hoods in CATCHMENT_HOODS.items():
        sub = hoods[hoods["name"].isin(member_hoods)]
        geom = unary_union(sub.geometry.values)
        union_ha = geom.area / 1e4
        attrs = merged_attrs(unit)
        ratio = union_ha / attrs["assessable_ha_brief"]
        if ratio < RATIO_LO:
            flag = "under-covers (catchment larger than mapped hoods)"
        elif ratio > RATIO_HI:
            flag = "over-covers (gross hoods exceed assessable; rural/merged land)"
        else:
            flag = "ok"
        records.append({
            "catchment": unit,
            "merged": attrs["merged"],
            "components": ", ".join(attrs["components"]),
            "facility_cost": attrs["facility_cost_total"],
            "assessable_ha_brief": attrs["assessable_ha_brief"],
            "union_ha": round(union_ha, 1),
            "area_ratio": round(ratio, 2),
            "rate_per_ha": attrs["rate_per_ha_blended"],
            "n_hoods": len(member_hoods),
            "member_hoods": ", ".join(member_hoods),
            "qa_flag": flag,
            "approximation": "union of neighbourhoods; boundaries advisory (Bylaw 19340 Schedule A)",
            "geometry": geom,
        })

    gdf = gpd.GeoDataFrame(records, geometry="geometry", crs=AREA_CRS).to_crs(4326)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    gdf.to_file(out_path, driver="GeoJSON")

    log.info("Wrote %d catchment units -> %s", len(gdf), out_path)
    log.info("%-22s %8s %8s %6s  %s", "catchment", "assess", "union", "ratio", "flag")
    for r in records:
        log.info("%-22s %8d %8.0f %6.2f  %s", r["catchment"], r["assessable_ha_brief"],
                 r["union_ha"], r["area_ratio"], r["qa_flag"])

    # Coverage accounting (no silent drops): how many hoods went unused.
    log.info("Assigned %d of %d neighbourhoods to %d catchment units.",
             len(used), len(hoods), len(gdf))
    return gdf


def write_qa(gdf: gpd.GeoDataFrame, hoods_path: Path, png_path: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    hoods = gpd.read_file(hoods_path).to_crs(4326)
    fig, ax = plt.subplots(figsize=(13, 16))
    hoods.boundary.plot(ax=ax, color="#dddddd", linewidth=0.3)
    gdf.plot(ax=ax, column="catchment", cmap="tab20", edgecolor="black",
             linewidth=0.8, alpha=0.75, legend=True,
             legend_kwds={"loc": "lower left", "fontsize": 7})
    for _, r in gdf.iterrows():
        c = r.geometry.centroid
        ax.annotate(f"{r['catchment']}\n{r['area_ratio']}", (c.x, c.y),
                    fontsize=5, ha="center", va="center", weight="bold")
    ax.set_axis_off()
    ax.set_title("Approx. off-site levy catchments (neighbourhood union) — QA vs Schedule A")
    plt.tight_layout()
    plt.savefig(png_path, dpi=150, bbox_inches="tight")
    log.info("Wrote QA overlay -> %s", png_path)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--hoods", default="data/raw/neighbourhoods.geojson", type=Path)
    ap.add_argument("--out", default="data/levy_catchments.geojson", type=Path)
    ap.add_argument("--qa", action="store_true", help="also write a QA overlay PNG")
    ap.add_argument("--qa-out", default="data/levy_catchments_qa.png", type=Path)
    args = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    gdf = build(args.hoods, args.out)
    if args.qa:
        write_qa(gdf, args.hoods, args.qa_out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
