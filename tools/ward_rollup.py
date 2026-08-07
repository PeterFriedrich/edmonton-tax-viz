"""Roll the served neighbourhood metrics up to city wards.

Reports, per ward, the modelled ANNUAL CAPITAL-RENEWAL REQUIREMENT for
collector+local roads beside the municipal property-tax revenue raised there.

⚠️ Three framing rules, all load-bearing:

1. **Requirement, not gap.** This is what renewing the roads costs per year, not
   the unfunded shortfall. A gap is requirement minus what is already funded and
   this project has no data on the funded side. Do not present the output beside
   a published citywide infrastructure-gap figure as if they were the same
   quantity.
2. **Partial network.** ``road_m_per_acre`` is collector+local only — arterials
   are excluded from the metric — so every kilometre and dollar here understates
   the real road network.
3. **Renewal only.** ``roadway_renewal`` is the $38/m/yr capital-renewal half of
   the $50/m/yr lifecycle rate. It is NOT the whole lifecycle cost and must
   never be summed with ``roadway_om_renewal`` (city_unit_costs.json
   ``_two_bases``).

Revenue is the MUNICIPAL levy only (education is provincial and excluded
upstream in apply_tax_rates), which is the right basis for a municipal levy
question.

Usage:
    python tools/ward_rollup.py
    python tools/ward_rollup.py --ward Métis
"""

import argparse
import json
import logging
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from load_boundaries import load_boundaries  # noqa: E402
from load_wards import load_wards  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SERVED = ROOT / "web/data/neighbourhood_value_per_acre.geojson"
BOUNDARIES = ROOT / "data/raw/neighbourhoods.geojson"
PROPERTY_INFO = ROOT / "data/raw/Property_Info__Current_Calendar_Year_.csv"
UNIT_COSTS = ROOT / "data/city_unit_costs.json"

log = logging.getLogger("ward_rollup")


def build(served_path, boundaries_path, property_info_path, unit_costs_path):
    """Join served metrics -> boundary acres -> ward, and cost the road metres."""
    with open(served_path, encoding="utf-8") as f:
        served = pd.DataFrame([
            feat["properties"] for feat in json.load(f)["features"]
        ])[["neighbourhood_name", "road_m_per_acre", "total_revenue"]]

    with open(unit_costs_path, encoding="utf-8") as f:
        renewal_rate = json.load(f)["roadway_renewal"]["value"]

    acres = load_boundaries(boundaries_path)[["neighbourhood_name", "area_acres"]]
    wards = load_wards(property_info_path)

    df = served.merge(acres, on="neighbourhood_name", how="left")
    missing_area = df.loc[df["area_acres"].isna(), "neighbourhood_name"].tolist()
    if missing_area:
        raise ValueError(
            f"{len(missing_area)} served neighbourhood(s) have no boundary area, "
            f"so their road metres cannot be costed: {missing_area}"
        )

    df = df.merge(wards, on="neighbourhood_name", how="left")

    # road_m_per_acre is served; the absolute metres are not, so rebuild them
    # against the same boundary acres the metric was divided by.
    df["road_m"] = df["road_m_per_acre"] * df["area_acres"]
    df["renewal_per_year"] = df["road_m"] * renewal_rate
    return df, renewal_rate


def summarise(df):
    """One row per ward; hoods with no ward are kept as an explicit row."""
    grouped = df.copy()
    grouped["ward"] = grouped["ward"].fillna("(no ward in source)")
    out = grouped.groupby("ward").agg(
        hoods=("neighbourhood_name", "size"),
        acres=("area_acres", "sum"),
        road_km=("road_m", lambda s: s.sum() / 1000),
        renewal_per_year=("renewal_per_year", "sum"),
        municipal_revenue=("total_revenue", "sum"),
    )
    out["renewal_pct_of_revenue"] = (
        out["renewal_per_year"] / out["municipal_revenue"] * 100
    )
    return out.sort_values("renewal_per_year", ascending=False)


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--ward", help="report a single ward (exact name, e.g. Métis)")
    ap.add_argument("--served", type=Path, default=SERVED)
    ap.add_argument("--boundaries", type=Path, default=BOUNDARIES)
    ap.add_argument("--property-info", type=Path, default=PROPERTY_INFO)
    ap.add_argument("--unit-costs", type=Path, default=UNIT_COSTS)
    ap.add_argument("--out", type=Path, help="also write the table as CSV")
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s",
                        stream=sys.stdout)

    df, rate = build(args.served, args.boundaries, args.property_info,
                     args.unit_costs)
    table = summarise(df)

    unassigned = int(df["ward"].isna().sum())
    print(f"\nModelled annual road CAPITAL-RENEWAL REQUIREMENT at ${rate}/road-m/yr")
    print("collector+local only (arterials excluded) — a PARTIAL network")
    print("revenue is the MUNICIPAL levy only\n")

    show = table.copy()
    show["acres"] = show["acres"].round(0).astype(int)
    show["road_km"] = show["road_km"].round(0).astype(int)
    show["renewal_$M/yr"] = (show.pop("renewal_per_year") / 1e6).round(1)
    show["revenue_$M/yr"] = (show.pop("municipal_revenue") / 1e6).round(1)
    show["renewal_%_of_rev"] = show.pop("renewal_pct_of_revenue").round(1)

    if args.ward:
        if args.ward not in table.index:
            raise SystemExit(
                f"no ward named {args.ward!r}; available: {sorted(table.index)}"
            )
        show = show.loc[[args.ward]]
        hoods = df.loc[df["ward"] == args.ward, "neighbourhood_name"]
        print(show.to_string())
        print(f"\n{len(hoods)} neighbourhoods: {', '.join(sorted(hoods))}")
    else:
        print(show.to_string())
        totals = table.sum(numeric_only=True)
        print(f"\nCITYWIDE  {totals['road_km']:,.0f} km  "
              f"${totals['renewal_per_year']/1e6:,.1f}M/yr renewal  "
              f"${totals['municipal_revenue']/1e6:,.1f}M/yr municipal revenue  "
              f"({totals['renewal_per_year']/totals['municipal_revenue']*100:.1f}%)")

    if unassigned:
        log.warning(
            "%d served neighbourhood(s) have no ward and are reported in their "
            "own row, not distributed: %s", unassigned,
            sorted(df.loc[df["ward"].isna(), "neighbourhood_name"]),
        )

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        table.to_csv(args.out)
        log.info("wrote %s", args.out)


if __name__ == "__main__":
    main()
