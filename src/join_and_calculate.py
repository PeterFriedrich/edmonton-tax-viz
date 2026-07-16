import json
import logging
from pathlib import Path

import geopandas as gpd
import pandas as pd

logger = logging.getLogger(__name__)


# Zoning composition columns carried into the output when a zoning frame is
# supplied. set_aside_* drive the neutral-grey render; frac_residential/
# is_residential drive the residential-only lens; the full per-category
# fractions (sum to 1) drive the use-mix view — dominant use + tooltip
# composition are derived client-side, like the ratio metric.
ZONING_COLUMNS = [
    "set_aside_frac", "is_set_aside", "set_aside_reason",
    "frac_never", "frac_notyet", "frac_inst",
    "frac_residential", "frac_commercial", "frac_industrial",
    "frac_mixed", "frac_dc", "frac_other",
    "is_residential",
]

# Road-supply column carried from load_roads when a roads frame is supplied
# (services lens, SPEC_services.md). road_m_total = collector + local only;
# the per-class breakdown stays in load_roads. road_m_per_acre is computed
# HERE against boundary area_acres — the same denominator as value/revenue.
ROAD_COLUMNS = ["road_m_total"]

# Modeled stormwater column carried from load_stormwater when supplied
# (utility lens #1, SPEC_utilities.md — MODELED, not billed). The rate-
# independent lot/effective areas stay in load_stormwater; per-acre is
# computed HERE against boundary area_acres, same as everything else.
STORM_COLUMNS = ["storm_charge_annual"]

# Fire-demand column carried from load_fire when supplied (services lens #3,
# SPEC_services.md "Fire lens"): mean annual dispatched emergency events in
# the pinned window. Per-acre is computed HERE against boundary area_acres.
FIRE_COLUMNS = ["fire_events_per_year"]

# Transit-supply column carried from load_transit when supplied (services
# lens #4, SPEC_services.md "Transit lens"): mean-weekday SCHEDULED transit
# stop-events — a supply proxy from the GTFS schedule, never ridership. The
# per-mode bus/LRT breakdown stays in load_transit (the road-class pattern).
# Per-acre is computed HERE against boundary area_acres.
TRANSIT_COLUMNS = ["transit_dep_total"]

# Modeled water + sanitary columns carried from load_water when supplied
# (utility lens #2, SPEC_utilities.md — MODELED, not billed; residential
# scope only). Total AND fixed ride along so the client can show the
# connection-vs-consumption split; per-acre is computed HERE.
WATER_COLUMNS = ["water_charge_annual", "water_fixed_annual"]

# Modeled electricity/gas franchise columns carried from load_franchise when
# supplied (utility lens #3, SPEC_utilities.md — MODELED, not billed;
# residential scope; COLLINEAR with dwelling_count). Carried on the full frame
# for the totals + future display/analysis; deliberately NOT in SLIM_COLUMNS
# (no display layer yet) and no per-acre derived here for the same reason.
FRANCHISE_COLUMNS = [
    "dwelling_count", "elec_distribution_annual", "elec_laf_revenue",
    "gas_delivery_annual", "gas_franchise_revenue",
]


# New-residential-supply columns carried from load_permits when supplied
# (Development & Infill lens A, SPEC_development.md): Σ units_added on new-
# construction ∩ residential permits over the pinned window, and the permit
# count behind it. new_units_per_acre AND new_permits_per_acre are computed HERE
# against boundary area_acres — the same denominator as everything else. Both the
# total and the count ride into the slim file for the tooltip (like the water
# total/fixed pair); either per-acre metric can drive the choropleth (units is the
# default; the permit-count sub-metric surfaces project density — one big
# apartment is many units but one permit, many single houses are many permits).
PERMIT_COLUMNS = ["new_dwelling_units", "new_dwelling_permits"]

# Optional recent (3-year) window (SPEC_development.md "Lens A polish", window
# toggle 2026-07-13). When a second, shorter permit window is supplied it
# duplicates the four activity columns with a ``_3yr`` suffix so the web window
# toggle can switch 5yr <-> 3yr on the same map. The base (5yr) columns stay
# UNSUFFIXED for backward-compat with the live geojson and the existing web
# gates (``new_units_per_acre`` / ``new_permits_per_acre``).
PERMIT_COLUMNS_3YR = [f"{c}_3yr" for c in PERMIT_COLUMNS]


# Neighbourhood lot-acre denominator (the "value per developable acre" toggle,
# docs/FINDINGS_denominator_cardinality.md). Carried from build_hood_lot_acres;
# value_per_lot_acre / revenue_per_lot_acre are computed HERE against the deduped
# parcel acres (not boundary acres), and parcel_frac = lot acres / boundary acres
# ships alongside so the client can label + guard. This is an editorial
# alternative denominator, NOT a correction to the cardinality-robust default.
LOT_ACRE_COLUMNS = [
    "value_lot_eligible", "revenue_lot_eligible", "lot_acres_eligible", "far",
]

def load_unit_costs(path: str | Path) -> dict[str, float]:
    """Load the MODELED service unit costs for the V2 composite (data/city_unit_costs.json).

    Manual, reviewed input (mill-rates pattern — SPEC_utilities decision 3,
    DATA.md §13). Returns the two numbers the composite needs:

        road_dollars_per_m   $/road-metre/yr (O&M + renewal, 50-yr life)
        fire_budget_annual   Fire Rescue gross operating budget, $/yr

    Validates loudly — a malformed hand edit must fail the pipeline, not
    silently zero a term of the composite.
    """
    with open(path) as f:
        data = json.load(f)
    try:
        road = data["roadway_om_renewal"]["value"]
        fire_budget = data["fire_response"]["operating_budget_gross_annual"]
    except KeyError as e:
        raise KeyError(f"{path} is missing required unit-cost field {e}") from e
    for name, val in (("roadway value", road), ("fire budget", fire_budget)):
        if not isinstance(val, (int, float)) or val <= 0:
            raise ValueError(f"{path}: {name} must be a positive number, got {val!r}")
    return {"road_dollars_per_m": float(road), "fire_budget_annual": float(fire_budget)}


# Below this parcel-land share the lot-acre denominator is near-zero and the
# ratio explodes (Mill Woods Golf Course 0% parcel -> x6960; the park/river-
# valley tail). Such hoods are suppressed to NaN (rendered n/a grey), not shown
# with a meaningless multiple. parcel_frac itself still ships for the tooltip.
# Hoods above 1.0 (lot acres > boundary acres) are a known lot_size artifact,
# already gated by export_value_grid.check_lot_acre_bounds' KNOWN_BOUND_OUTLIERS.
LOW_PARCEL_FRAC = 0.15


def _merge_permit_window(
    joined: gpd.GeoDataFrame,
    permits: pd.DataFrame,
    safe_area: pd.Series,
    suffix: str,
) -> tuple[gpd.GeoDataFrame, list[str]]:
    """Merge one new-supply permit-window aggregation onto the hood frame.

    Warn-not-fail on unmatched permit hoods (activity ≠ the money path — an
    unmatched hood is a visibly blank hood, not a silent dollar loss), fill the
    true 0 for hoods with no permits in the window, and compute the two per-acre
    activity metrics against boundary ``safe_area`` (the one project
    denominator). The base window uses ``suffix=""`` (the canonical column
    names); the recent window uses ``"_3yr"``. Returns the updated frame and the
    list of columns added (two totals + two per-acre), in output order.
    """
    units_col = f"new_dwelling_units{suffix}"
    permits_col = f"new_dwelling_permits{suffix}"
    upa_col = f"new_units_per_acre{suffix}"
    ppa_col = f"new_permits_per_acre{suffix}"

    boundary_names = set(joined["neighbourhood_name"])
    unmatched_permits = sorted(set(permits["neighbourhood_name"]) - boundary_names)
    if unmatched_permits:
        stranded = permits.set_index("neighbourhood_name").loc[
            unmatched_permits, "new_dwelling_units"
        ]
        logger.warning(
            "%d permit neighbourhood(s) with no boundary match (activity "
            "dropped, %.0f units%s) — warn-not-fail (activity ≠ money path):\n  %s",
            len(unmatched_permits), stranded.sum(),
            f", {suffix.lstrip('_')} window" if suffix else "",
            "\n  ".join(f"{n} ({stranded[n]:.0f}u)" for n in unmatched_permits),
        )

    frame = permits.rename(columns={
        "new_dwelling_units": units_col, "new_dwelling_permits": permits_col,
    })
    joined = joined.merge(
        frame[["neighbourhood_name", units_col, permits_col]],
        on="neighbourhood_name",
        how="left",
        validate="m:1",
    )

    no_permits = joined[units_col].isna()
    if no_permits.any():
        logger.info(
            "%d boundary neighbourhood(s) with no new residential permits in "
            "the %s window (default 0 units)", int(no_permits.sum()),
            suffix.lstrip("_") if suffix else "base",
        )
    # No new residential permits there in the window -> a true 0 units.
    joined[units_col] = joined[units_col].fillna(0.0)
    joined[permits_col] = joined[permits_col].fillna(0.0)
    joined[upa_col] = joined[units_col] / safe_area
    joined[ppa_col] = joined[permits_col] / safe_area
    return joined, [units_col, permits_col, upa_col, ppa_col]


def join_and_calculate(
    assessment: pd.DataFrame,
    boundaries: gpd.GeoDataFrame,
    zoning: pd.DataFrame | None = None,
    roads: pd.DataFrame | None = None,
    stormwater: pd.DataFrame | None = None,
    fire: pd.DataFrame | None = None,
    transit: pd.DataFrame | None = None,
    water: pd.DataFrame | None = None,
    franchise: pd.DataFrame | None = None,
    permits: pd.DataFrame | None = None,
    permits_recent: pd.DataFrame | None = None,
    lot_acres: pd.DataFrame | None = None,
    unit_costs: dict[str, float] | None = None,
) -> gpd.GeoDataFrame:
    """Left join boundaries → assessment, flag unmatched rows, compute value_per_acre.

    Assessment names are expected to be corrected and aggregated already
    (NAME_CORRECTIONS is applied upstream in load_assessment.py). The one
    expected unmatched case — the OLIVER straggler row, deliberately left
    unmapped (DATA.md "Name Matching") — surfaces here as a warning.

    ``zoning`` (optional, from load_zoning.py) adds the ZONING_COLUMNS — the
    set-aside flags, the residential-lens flag, and the full land-use
    composition fractions (use-mix view) — merged on neighbourhood_name.
    Degrades gracefully when absent, like the revenue columns; boundaries with
    no zoning match default to is_set_aside=False (stays on scale) and
    is_residential=False (frac_* left NaN), and are flagged.

    ``roads`` (optional, from load_roads.py) adds road_m_total and computes
    road_m_per_acre against boundary area_acres (SPEC_services.md). Boundaries
    with no roads overlay default to 0 — genuinely zero city-maintained
    collector/local road, unlike the zoning NaNs — and are flagged.

    ``stormwater`` (optional, from load_stormwater.py) adds the MODELED
    storm_charge_annual and computes storm_charge_per_acre against boundary
    area_acres (SPEC_utilities.md Lens 1). Boundaries with no modeled points
    default to $0 (roads semantics: no roll parcels there means no modeled
    charge) — with the shared caveat that the roll omits exempt institutional
    land, so hood totals understate where exempt land dominates.

    ``fire`` (optional, from load_fire.py) adds fire_events_per_year and
    computes fire_events_per_acre against boundary area_acres
    (SPEC_services.md "Fire lens"). Boundaries with no events default to a
    true 0/yr (roads semantics: no dispatched emergency events recorded
    there in the window) — and are flagged.

    ``transit`` (optional, from load_transit.py) adds transit_dep_total —
    mean-weekday SCHEDULED stop-events, a supply proxy, not ridership — and
    computes transit_dep_per_acre against boundary area_acres
    (SPEC_services.md "Transit lens"). Boundaries with no served stops
    default to a true 0 (roads semantics) — and are flagged.

    ``water`` (optional, from load_water.py) adds the MODELED residential
    water + sanitary columns (WATER_COLUMNS) and computes
    water_charge_per_acre / water_fixed_per_acre against boundary area_acres
    (SPEC_utilities.md Lens 2). Boundaries with no modeled connections
    default to $0 (stormwater semantics; commercial-only hoods are genuinely
    out of the residential scope) — and are flagged.

    ``franchise`` (optional, from load_franchise.py) adds the MODELED
    electricity/gas franchise columns (FRANCHISE_COLUMNS) — City-revenue
    lines plus the collinear dwelling_count (SPEC_utilities.md Lens 3).
    Carried on the full frame only (no per-acre, no SLIM — no display layer
    yet). Boundaries with no modeled dwellings default to 0 (water semantics)
    — and are flagged.

    ``unit_costs`` (optional, from load_unit_costs — data/city_unit_costs.json,
    the manual reviewed input) adds the V2 MODELED composite
    svc_cost_per_acre = road_m_per_acre × $/road-metre/yr
    + fire_events_per_acre × (fire budget ÷ the pipeline's own citywide
    kept-event total) (SPEC_utilities decision 3). Roads + fire ONLY — never
    "total city cost" — and the fire term is a demand ALLOCATION of a mostly-
    fixed budget, not a marginal cost; both caveats belong in any display copy.
    Requires BOTH the roads and fire frames: with either missing the composite
    would be a mislabeled one-term metric, so it is skipped with a warning.

    ``lot_acres`` (optional, from export_value_grid.build_hood_lot_acres) adds
    the neighbourhood lot-acre denominator toggle: value_per_lot_acre /
    revenue_per_lot_acre (eligible dollars / deduped parcel acres) plus
    parcel_frac (parcel land / boundary land). Hoods below LOW_PARCEL_FRAC
    parcel land are suppressed to NaN (n/a grey) so the near-zero-denominator
    tail doesn't explode; parcel_frac still ships for the tooltip. An editorial
    alternative denominator (docs/FINDINGS_denominator_cardinality.md), NOT a
    fix — the ground-acre metric stays the cardinality-robust default.
    """
    agg = assessment

    boundary_names = set(boundaries["neighbourhood_name"])
    unmatched_assessment = sorted(set(agg["neighbourhood_name"]) - boundary_names)
    if unmatched_assessment:
        logger.warning(
            "%d assessment neighbourhood(s) with no boundary match (excluded from map):\n  %s",
            len(unmatched_assessment),
            "\n  ".join(unmatched_assessment),
        )

    # validate="m:1": the right frame (aggregated assessment) must be unique per
    # neighbourhood_name. safe_area is computed once below and reused positionally
    # across every subsequent merge; a duplicate right key would fan the left join
    # out, shift the RangeIndex, and silently divide every downstream hood by the
    # wrong area. pandas raises loudly here instead (docs/FINDINGS_data_integrity_audit.md NEW-1).
    joined = boundaries.merge(agg, on="neighbourhood_name", how="left", validate="m:1")

    no_assessment = joined[joined["total_assessed_value"].isna()]
    if len(no_assessment):
        logger.warning(
            "%d boundary neighbourhood(s) with no assessment data:\n  %s",
            len(no_assessment),
            "\n  ".join(sorted(no_assessment["neighbourhood_name"])),
        )

    zero_area = joined["area_acres"] == 0
    if zero_area.any():
        logger.warning(
            "%d neighbourhood(s) with zero area_acres — value_per_acre will be NaN:\n  %s",
            zero_area.sum(),
            "\n  ".join(sorted(joined[zero_area]["neighbourhood_name"])),
        )

    safe_area = joined["area_acres"].replace(0, float("nan"))
    joined["value_per_acre"] = joined["total_assessed_value"] / safe_area

    logger.info(
        "Joined %d boundary neighbourhoods; %d with value_per_acre calculated",
        len(joined),
        joined["value_per_acre"].notna().sum(),
    )

    out_cols = ["neighbourhood_name", "total_assessed_value", "area_acres", "value_per_acre", "geometry"]

    # Revenue phase: when total_revenue is present (apply_tax_rates ran upstream),
    # add revenue_per_acre alongside value_per_acre — both metrics, web toggle.
    if "total_revenue" in joined.columns:
        joined["revenue_per_acre"] = joined["total_revenue"] / safe_area
        out_cols = [
            "neighbourhood_name", "total_assessed_value", "total_revenue",
            "area_acres", "value_per_acre", "revenue_per_acre", "geometry",
        ]

    # Zoning phase: merge land-use set-aside composition when supplied.
    if zoning is not None:
        boundary_names = set(joined["neighbourhood_name"])
        unmatched_zoning = sorted(set(zoning["neighbourhood_name"]) - boundary_names)
        if unmatched_zoning:
            logger.warning(
                "%d zoning neighbourhood(s) with no boundary match (dropped):\n  %s",
                len(unmatched_zoning),
                "\n  ".join(unmatched_zoning),
            )

        joined = joined.merge(
            zoning[["neighbourhood_name", *ZONING_COLUMNS]],
            on="neighbourhood_name",
            how="left",
            validate="m:1",
        )

        no_zoning = joined[joined["set_aside_frac"].isna()]
        if len(no_zoning):
            logger.warning(
                "%d boundary neighbourhood(s) with no zoning overlay (default is_set_aside=False):\n  %s",
                len(no_zoning),
                "\n  ".join(sorted(no_zoning["neighbourhood_name"])),
            )
        # Boundaries without a zoning match stay on the scale, not set aside,
        # and are not claimed residential (frac_* left NaN, like set_aside_frac).
        joined["is_set_aside"] = joined["is_set_aside"].fillna(False).astype(bool)
        joined["set_aside_reason"] = joined["set_aside_reason"].fillna("")
        joined["is_residential"] = joined["is_residential"].fillna(False).astype(bool)

        # Insert zoning columns before geometry.
        out_cols = [c for c in out_cols if c != "geometry"] + ZONING_COLUMNS + ["geometry"]

    # Services lens: merge road supply when supplied (SPEC_services.md).
    if roads is not None:
        boundary_names = set(joined["neighbourhood_name"])
        unmatched_roads = sorted(set(roads["neighbourhood_name"]) - boundary_names)
        if unmatched_roads:
            logger.warning(
                "%d roads neighbourhood(s) with no boundary match (dropped):\n  %s",
                len(unmatched_roads),
                "\n  ".join(unmatched_roads),
            )

        joined = joined.merge(
            roads[["neighbourhood_name", *ROAD_COLUMNS]],
            on="neighbourhood_name",
            how="left",
            validate="m:1",
        )

        no_roads = joined["road_m_total"].isna()
        if no_roads.any():
            logger.warning(
                "%d boundary neighbourhood(s) with no roads overlay (default 0 m):\n  %s",
                int(no_roads.sum()),
                "\n  ".join(sorted(joined.loc[no_roads, "neighbourhood_name"])),
            )
        # No overlay means genuinely zero city collector/local road there.
        joined["road_m_total"] = joined["road_m_total"].fillna(0.0)
        joined["road_m_per_acre"] = joined["road_m_total"] / safe_area

        out_cols = (
            [c for c in out_cols if c != "geometry"]
            + ROAD_COLUMNS + ["road_m_per_acre"] + ["geometry"]
        )

    # Utility lens #1: merge the modeled stormwater charge when supplied
    # (SPEC_utilities.md — modeled, not billed).
    if stormwater is not None:
        boundary_names = set(joined["neighbourhood_name"])
        unmatched_storm = sorted(set(stormwater["neighbourhood_name"]) - boundary_names)
        if unmatched_storm:
            logger.warning(
                "%d stormwater neighbourhood(s) with no boundary match (dropped):\n  %s",
                len(unmatched_storm),
                "\n  ".join(unmatched_storm),
            )

        joined = joined.merge(
            stormwater[["neighbourhood_name", *STORM_COLUMNS]],
            on="neighbourhood_name",
            how="left",
            validate="m:1",
        )

        no_storm = joined["storm_charge_annual"].isna()
        if no_storm.any():
            logger.warning(
                "%d boundary neighbourhood(s) with no modeled stormwater points (default $0):\n  %s",
                int(no_storm.sum()),
                "\n  ".join(sorted(joined.loc[no_storm, "neighbourhood_name"])),
            )
        # No roll parcels modeled there -> modeled $0 (exempt-land caveat above).
        joined["storm_charge_annual"] = joined["storm_charge_annual"].fillna(0.0)
        joined["storm_charge_per_acre"] = joined["storm_charge_annual"] / safe_area

        out_cols = (
            [c for c in out_cols if c != "geometry"]
            + STORM_COLUMNS + ["storm_charge_per_acre"] + ["geometry"]
        )

    # Services lens #3: merge fire demand when supplied (SPEC_services.md
    # "Fire lens" — dispatched emergency events, a demand count, not a
    # coverage or response-time claim).
    if fire is not None:
        boundary_names = set(joined["neighbourhood_name"])
        unmatched_fire = sorted(set(fire["neighbourhood_name"]) - boundary_names)
        if unmatched_fire:
            logger.warning(
                "%d fire neighbourhood(s) with no boundary match (dropped):\n  %s",
                len(unmatched_fire),
                "\n  ".join(unmatched_fire),
            )

        joined = joined.merge(
            fire[["neighbourhood_name", *FIRE_COLUMNS]],
            on="neighbourhood_name",
            how="left",
            validate="m:1",
        )

        no_fire = joined["fire_events_per_year"].isna()
        if no_fire.any():
            logger.warning(
                "%d boundary neighbourhood(s) with no fire events in the window (default 0/yr):\n  %s",
                int(no_fire.sum()),
                "\n  ".join(sorted(joined.loc[no_fire, "neighbourhood_name"])),
            )
        # No kept events there in the window -> a true 0 events/yr.
        joined["fire_events_per_year"] = joined["fire_events_per_year"].fillna(0.0)
        joined["fire_events_per_acre"] = joined["fire_events_per_year"] / safe_area

        out_cols = (
            [c for c in out_cols if c != "geometry"]
            + FIRE_COLUMNS + ["fire_events_per_acre"] + ["geometry"]
        )

    # V2 composite: modeled city service cost per acre (SPEC_utilities
    # decision 3 — MODELED, roads + fire only, never "total city cost").
    # Needs both the road and fire per-acre columns computed above; the fire
    # per-event cost divides the budget by the LOADER's citywide kept-event
    # total (the fire frame sum, pre-join) so the unit cost's denominator
    # matches the fire_events_per_acre numerator exactly — unmatched fire
    # hoods still consumed budget, so they stay in the denominator.
    if unit_costs is not None:
        if roads is None or fire is None:
            logger.warning(
                "Unit costs supplied but %s frame missing — svc_cost_per_acre "
                "needs BOTH (roads + fire only would be mislabeled); composite skipped",
                "roads" if roads is None else "fire",
            )
        else:
            citywide_events = float(fire["fire_events_per_year"].sum())
            if citywide_events <= 0:
                raise ValueError(
                    "Citywide kept fire events per year is not positive "
                    f"({citywide_events}) — cannot derive a per-event cost"
                )
            fire_cost_per_event = unit_costs["fire_budget_annual"] / citywide_events
            joined["svc_cost_per_acre"] = (
                joined["road_m_per_acre"] * unit_costs["road_dollars_per_m"]
                + joined["fire_events_per_acre"] * fire_cost_per_event
            )
            logger.info(
                "V2 service-cost composite: $%.2f/road-m/yr + $%.0f/fire-event "
                "($%.0f budget / %.0f kept events/yr) -> svc_cost_per_acre on %d hoods "
                "(MODELED, roads + fire only)",
                unit_costs["road_dollars_per_m"], fire_cost_per_event,
                unit_costs["fire_budget_annual"], citywide_events,
                int(joined["svc_cost_per_acre"].notna().sum()),
            )
            out_cols = (
                [c for c in out_cols if c != "geometry"]
                + ["svc_cost_per_acre"] + ["geometry"]
            )

    # Services lens #4: merge scheduled transit supply when supplied
    # (SPEC_services.md "Transit lens" — scheduled stop-events from the GTFS
    # feed, a supply proxy, never a ridership or coverage claim).
    if transit is not None:
        boundary_names = set(joined["neighbourhood_name"])
        unmatched_transit = sorted(set(transit["neighbourhood_name"]) - boundary_names)
        if unmatched_transit:
            logger.warning(
                "%d transit neighbourhood(s) with no boundary match (dropped):\n  %s",
                len(unmatched_transit),
                "\n  ".join(unmatched_transit),
            )

        joined = joined.merge(
            transit[["neighbourhood_name", *TRANSIT_COLUMNS]],
            on="neighbourhood_name",
            how="left",
            validate="m:1",
        )

        no_transit = joined["transit_dep_total"].isna()
        if no_transit.any():
            logger.warning(
                "%d boundary neighbourhood(s) with no served transit stops (default 0):\n  %s",
                int(no_transit.sum()),
                "\n  ".join(sorted(joined.loc[no_transit, "neighbourhood_name"])),
            )
        # No served stops there -> a true 0 scheduled stop-events.
        joined["transit_dep_total"] = joined["transit_dep_total"].fillna(0.0)
        joined["transit_dep_per_acre"] = joined["transit_dep_total"] / safe_area

        out_cols = (
            [c for c in out_cols if c != "geometry"]
            + TRANSIT_COLUMNS + ["transit_dep_per_acre"] + ["geometry"]
        )

    # Utility lens #2: merge the modeled water + sanitary charge when
    # supplied (SPEC_utilities.md Lens 2 — modeled, not billed; residential
    # scope only).
    if water is not None:
        boundary_names = set(joined["neighbourhood_name"])
        unmatched_water = sorted(set(water["neighbourhood_name"]) - boundary_names)
        if unmatched_water:
            logger.warning(
                "%d water neighbourhood(s) with no boundary match (dropped):\n  %s",
                len(unmatched_water),
                "\n  ".join(unmatched_water),
            )

        joined = joined.merge(
            water[["neighbourhood_name", *WATER_COLUMNS]],
            on="neighbourhood_name",
            how="left",
            validate="m:1",
        )

        no_water = joined["water_charge_annual"].isna()
        if no_water.any():
            logger.warning(
                "%d boundary neighbourhood(s) with no modeled water connections "
                "(default $0):\n  %s",
                int(no_water.sum()),
                "\n  ".join(sorted(joined.loc[no_water, "neighbourhood_name"])),
            )
        # No residential roll records there -> modeled $0 (residential scope).
        for col in WATER_COLUMNS:
            joined[col] = joined[col].fillna(0.0)
        joined["water_charge_per_acre"] = joined["water_charge_annual"] / safe_area
        joined["water_fixed_per_acre"] = joined["water_fixed_annual"] / safe_area

        out_cols = (
            [c for c in out_cols if c != "geometry"]
            + WATER_COLUMNS + ["water_charge_per_acre", "water_fixed_per_acre"]
            + ["geometry"]
        )

    # Utility lens #3: merge the modeled electricity/gas franchise columns when
    # supplied (SPEC_utilities.md Lens 3 — modeled, not billed; residential
    # scope; collinear with dwelling_count, so no map layer — see the module).
    if franchise is not None:
        boundary_names = set(joined["neighbourhood_name"])
        unmatched_fr = sorted(set(franchise["neighbourhood_name"]) - boundary_names)
        if unmatched_fr:
            logger.warning(
                "%d franchise neighbourhood(s) with no boundary match (dropped):\n  %s",
                len(unmatched_fr),
                "\n  ".join(unmatched_fr),
            )

        joined = joined.merge(
            franchise[["neighbourhood_name", *FRANCHISE_COLUMNS]],
            on="neighbourhood_name",
            how="left",
            validate="m:1",
        )

        no_fr = joined["dwelling_count"].isna()
        if no_fr.any():
            logger.warning(
                "%d boundary neighbourhood(s) with no modeled dwellings "
                "(default 0):\n  %s",
                int(no_fr.sum()),
                "\n  ".join(sorted(joined.loc[no_fr, "neighbourhood_name"])),
            )
        # No residential roll records there -> modeled 0 (residential scope).
        for col in FRANCHISE_COLUMNS:
            joined[col] = joined[col].fillna(0.0)

        out_cols = (
            [c for c in out_cols if c != "geometry"]
            + FRANCHISE_COLUMNS + ["geometry"]
        )

    # Development & Infill lens A: merge new-residential-supply activity when
    # supplied (SPEC_development.md "Lens A" — new dwelling units from issued
    # building permits over the pinned window, an activity count, NOT a revenue
    # or cost claim). Unlike the money path this is warn-not-fail on the join.
    if permits is not None:
        joined, base_cols = _merge_permit_window(joined, permits, safe_area, "")
        added = list(base_cols)
        # Optional recent (3-year) window for the web window toggle — same merge,
        # suffixed columns (SPEC_development.md "Lens A polish", 2026-07-13).
        if permits_recent is not None:
            joined, recent_cols = _merge_permit_window(
                joined, permits_recent, safe_area, "_3yr"
            )
            added += recent_cols

        out_cols = (
            [c for c in out_cols if c != "geometry"] + added + ["geometry"]
        )

    # Neighbourhood lot-acre denominator toggle (the "value per developable
    # acre" view, docs/FINDINGS_denominator_cardinality.md). Merge the eligible
    # dollars + deduped parcel acres, divide, and guard the low-parcel tail.
    if lot_acres is not None:
        boundary_names = set(joined["neighbourhood_name"])
        unmatched_lot = sorted(set(lot_acres["neighbourhood_name"]) - boundary_names)
        if unmatched_lot:
            logger.warning(
                "%d lot-acre neighbourhood(s) with no boundary match (dropped):\n  %s",
                len(unmatched_lot),
                "\n  ".join(unmatched_lot),
            )

        merge_cols = ["neighbourhood_name"] + [
            c for c in LOT_ACRE_COLUMNS if c in lot_acres.columns
        ]
        joined = joined.merge(
            lot_acres[merge_cols], on="neighbourhood_name", how="left", validate="m:1"
        )

        # parcel_frac ships regardless (tooltip); the per-lot-acre ratios divide
        # by deduped parcel acres, not boundary acres.
        joined["parcel_frac"] = joined["lot_acres_eligible"] / safe_area
        safe_lot = joined["lot_acres_eligible"].replace(0, float("nan"))
        joined["value_per_lot_acre"] = joined["value_lot_eligible"] / safe_lot
        added = ["value_per_lot_acre"]
        if "revenue_lot_eligible" in joined.columns:
            joined["revenue_per_lot_acre"] = joined["revenue_lot_eligible"] / safe_lot
            added.append("revenue_per_lot_acre")
        added.append("parcel_frac")

        # Guard: hoods below the parcel-fraction floor (incl. NaN — no eligible
        # parcels at all) get NaN per-lot-acre values so the client renders them
        # n/a grey rather than an exploded multiple. parcel_frac is left intact.
        suppress = ~(joined["parcel_frac"] >= LOW_PARCEL_FRAC)
        n_sup = int(suppress.sum())
        if n_sup:
            logger.info(
                "Lot-acre lens: %d hood(s) below %.0f%% parcel land suppressed to "
                "n/a (near-zero denominator would explode):\n  %s",
                n_sup, LOW_PARCEL_FRAC * 100,
                "\n  ".join(sorted(joined.loc[suppress, "neighbourhood_name"])),
            )
        ratio_cols = [c for c in added if c != "parcel_frac"]
        joined.loc[suppress, ratio_cols] = float("nan")

        # far (Development Lens B suitability proxy) rides along UNSUPPRESSED:
        # it is a built floor-area density ratio, not a per-lot-acre dollar
        # figure, so the LOW_PARCEL_FRAC denominator guard does not apply. The
        # web view owns the low-FAR park/greenfield exclusion (SPEC_development
        # Lens B). NaN only where a hood has no eligible parcels at all.
        if "far" in joined.columns:
            added.append("far")

        out_cols = [c for c in out_cols if c != "geometry"] + added + ["geometry"]

    return joined[out_cols]


# Columns the web client actually consumes. Everything else is dropped to keep
# the GeoJSON the browser downloads small. revenue_per_acre and the zoning
# columns are included only when present (their respective phases) — the
# value↔revenue toggle reads both metrics; is_set_aside/set_aside_reason drive
# the neutral-grey render + tooltip; is_residential drives the residential lens;
# the frac_* composition (sums to 1) drives the use-mix view (dominant use is
# derived client-side); road_m_per_acre, storm_charge_per_acre,
# fire_events_per_acre, and the water_* pair are the Services-view metrics
# (SPEC_services.md, SPEC_utilities.md — ratios only, totals stay out of the
# slim file like total_assessed_value does; the storm and water figures are
# MODELED, not billed — water additionally residential-scope only, with the
# fixed column shipping alongside the total so the client can show the
# connection-vs-consumption split — the fire figure is dispatched-event
# DEMAND, not coverage, and the transit figure is SCHEDULED service supply,
# not ridership; the client must label all of them as such). svc_cost_per_acre
# is the V2 composite — MODELED road $ + allocated fire $, roads + fire only,
# never "total city cost" (SPEC_utilities decision 3; no display layer yet —
# placement is an open call). new_units_per_acre
# and new_permits_per_acre (+ the total/permit-count pair for the tooltip) are the
# Development lens A activity metrics — new dwelling units / new permits from
# issued permits, a change/flow signal, NOT revenue or cost (SPEC_development.md).
SLIM_COLUMNS = [
    "neighbourhood_name", "value_per_acre", "revenue_per_acre",
    "set_aside_frac", "is_set_aside", "set_aside_reason",
    "frac_never", "frac_notyet", "frac_inst",
    "frac_residential", "frac_commercial", "frac_industrial",
    "frac_mixed", "frac_dc", "frac_other",
    "is_residential", "road_m_per_acre", "storm_charge_per_acre",
    "fire_events_per_acre", "transit_dep_per_acre",
    "water_charge_per_acre", "water_fixed_per_acre",
    "svc_cost_per_acre",
    "new_units_per_acre", "new_permits_per_acre",
    "new_dwelling_units", "new_dwelling_permits",
    "new_units_per_acre_3yr", "new_permits_per_acre_3yr",
    "new_dwelling_units_3yr", "new_dwelling_permits_3yr",
    "value_per_lot_acre", "revenue_per_lot_acre", "parcel_frac",
    "far",
    "geometry",
]


# CRS used for the setback buffer — must be projected (metres), not degrees.
# Matches load_boundaries: NAD83 / Alberta 10-TM (Forest).
SETBACK_CRS = "EPSG:3400"


def export_geojson(
    result: gpd.GeoDataFrame,
    output_path: str,
    crs: str = "EPSG:4326",
    setback_m: float = 0.0,
    simplify_tolerance_m: float = 0.0,
) -> gpd.GeoDataFrame:
    """Write a slim GeoJSON of the join result for the Phase 2 web map.

    Keeps only the columns the deck.gl layer needs (SLIM_COLUMNS) and reprojects
    to ``crs`` (default EPSG:4326 — MapLibre/deck.gl expect lon/lat geometry; the
    join result is in projected EPSG:3400 for area math). Rows with no
    value_per_acre cannot be rendered (null elevation), so they are dropped — but
    the count is logged, never silently discarded.

    ``setback_m`` (metres, default 0 = off) shrinks each polygon inward by a
    negative buffer so the extruded columns don't touch — a purely cosmetic
    "city blocks" look. Thin sliver neighbourhoods can collapse to empty/invalid
    under the buffer; those fall back to their original footprint, count logged.

    ``simplify_tolerance_m`` (metres, default 0 = off) runs a topology-preserving
    Douglas-Peucker simplification to cut vertex count — the dominant render-cost
    lever on the iGPU baseline audience (see docs/PERFORMANCE.md). Applied AFTER
    the setback so the final pass also collapses the rounded-corner vertices the
    negative buffer adds, keeping the served file small (the extra export-time
    cost of buffering full-resolution geometry is a once-a-year non-issue).

    Both ``simplify_tolerance_m`` and ``setback_m`` are DISPLAY geometry only;
    value_per_acre is computed from the true area upstream and is untouched.
    Neither silently drops or alters a row without logging it.

    Returns the slim GeoDataFrame that was written.
    """
    slim = result[[c for c in SLIM_COLUMNS if c in result.columns]]

    missing = slim["value_per_acre"].isna()
    if missing.any():
        logger.warning(
            "Dropping %d neighbourhood(s) with no value_per_acre from GeoJSON export:\n  %s",
            missing.sum(),
            "\n  ".join(sorted(slim[missing]["neighbourhood_name"])),
        )
    slim = slim[~missing]

    if slim.crs is None:
        raise ValueError("result GeoDataFrame has no CRS set; cannot reproject for export")

    if setback_m:
        slim = _apply_setback(slim, setback_m)

    if simplify_tolerance_m:
        slim = _apply_simplify(slim, simplify_tolerance_m)

    slim = slim.to_crs(crs)

    slim.to_file(output_path, driver="GeoJSON")
    logger.info(
        "Wrote slim GeoJSON (%d features, %s, simplify=%sm, setback=%sm) to %s",
        len(slim), crs, simplify_tolerance_m, setback_m, output_path,
    )

    return slim


def _apply_setback(slim: gpd.GeoDataFrame, setback_m: float) -> gpd.GeoDataFrame:
    """Shrink each polygon inward by ``setback_m`` metres (display-only).

    Buffers in a projected metric CRS, then restores the original geometry for
    any shape that collapses to empty/invalid, logging which ones.
    """
    metric = slim.to_crs(SETBACK_CRS)
    shrunk = metric.geometry.buffer(-setback_m)

    collapsed = shrunk.is_empty | ~shrunk.is_valid
    if collapsed.any():
        logger.warning(
            "Setback (%sm) collapsed %d sliver neighbourhood(s); kept original footprint:\n  %s",
            setback_m,
            int(collapsed.sum()),
            "\n  ".join(sorted(metric.loc[collapsed, "neighbourhood_name"])),
        )

    metric = metric.set_geometry(shrunk.where(~collapsed, metric.geometry))
    return metric


def _count_vertices(geom) -> int:
    """Total coordinate count of a (Multi)Polygon, exterior + interiors."""
    if geom is None or geom.is_empty:
        return 0
    if geom.geom_type == "Polygon":
        return len(geom.exterior.coords) + sum(len(r.coords) for r in geom.interiors)
    if geom.geom_type == "MultiPolygon":
        return sum(_count_vertices(p) for p in geom.geoms)
    return len(geom.coords)


def _apply_simplify(slim: gpd.GeoDataFrame, tolerance_m: float) -> gpd.GeoDataFrame:
    """Reduce vertex count via Douglas-Peucker in a projected metric CRS (display-only).

    Topology-preserving so polygons stay valid (no new self-intersections) and no
    shape is removed. Logs the vertex reduction; any shape that still lands
    empty/invalid falls back to its original geometry (no silent changes).
    """
    metric = slim.to_crs(SETBACK_CRS)
    before = int(metric.geometry.apply(_count_vertices).sum())

    simplified = metric.geometry.simplify(tolerance_m, preserve_topology=True)

    collapsed = simplified.is_empty | ~simplified.is_valid
    if collapsed.any():
        logger.warning(
            "Simplify (%sm) produced %d empty/invalid geometry(ies); kept original:\n  %s",
            tolerance_m,
            int(collapsed.sum()),
            "\n  ".join(sorted(metric.loc[collapsed, "neighbourhood_name"])),
        )
    simplified = simplified.where(~collapsed, metric.geometry)

    metric = metric.set_geometry(simplified)
    after = int(metric.geometry.apply(_count_vertices).sum())
    logger.info(
        "Simplify (%sm tolerance): %d -> %d vertices (%.0f%% reduction)",
        tolerance_m, before, after, 100 * (1 - after / before) if before else 0.0,
    )
    return metric
