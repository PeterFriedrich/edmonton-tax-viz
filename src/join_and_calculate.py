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

# Bike-supply column carried from load_bike when a bike frame is supplied
# (services lens, SPEC_services.md "Transportation lens"). bike_m_total =
# DEDICATED cycling assets only — shared roadways are excluded there precisely
# because those metres are already in road_m_total above. The on/off-road split
# stays in load_bike; bike_m_per_acre is computed HERE against boundary
# area_acres, the same denominator as everything else.
BIKE_COLUMNS = ["bike_m_total"]

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

# Revenue-lens readout (2026-08-01): a hood's share of the CITYWIDE levy, and
# where that levy comes from by zoning category. Both are produced upstream by
# OPTIONAL steps (revenue_share_city in main.py, rev_frac_* by revenue_by_zone,
# which needs the zoning file), so they are carried only when present — the
# value-only and no-zoning paths must keep working.
REVENUE_READOUT_COLUMNS = [
    "revenue_share_city",
    "rev_frac_never", "rev_frac_notyet", "rev_frac_inst",
    "rev_frac_residential", "rev_frac_commercial", "rev_frac_industrial",
    "rev_frac_mixed", "rev_frac_dc", "rev_frac_other", "rev_frac_unzoned",
    # Cuts ACROSS the family above rather than joining it — the rev_frac_*
    # partition sums to 1.0 and this asks a different question of the same
    # dollars (load_zoning.EXEMPT_CANDIDATE_ZONES).
    "rev_frac_exempt",
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

# Optional long "since 2009" window (SPEC_development.md "Lens A long window",
# 2026-07-21) — the anchored-cumulative "density added over the era" cut for the
# web window toggle. Same duplication idiom as the 3yr window, `_long` suffix.
PERMIT_COLUMNS_LONG = [f"{c}_long" for c in PERMIT_COLUMNS]


# Neighbourhood lot-acre denominator (the "value per developable acre" toggle,
# docs/FINDINGS_denominator_cardinality.md). Carried from build_hood_lot_acres;
# value_per_lot_acre / revenue_per_lot_acre are computed HERE against the deduped
# parcel acres (not boundary acres), and parcel_frac = lot acres / boundary acres
# ships alongside so the client can label + guard. This is an editorial
# alternative denominator, NOT a correction to the cardinality-robust default.
LOT_ACRE_COLUMNS = [
    "value_lot_eligible", "revenue_lot_eligible", "res_revenue_lot_eligible",
    "nonres_revenue_lot_eligible",
    "lot_acres_eligible", "far",
]

def load_unit_costs(path: str | Path) -> dict[str, float]:
    """Load the MODELED service unit costs for the V2 composite (data/city_unit_costs.json).

    Manual, reviewed input (mill-rates pattern — SPEC_utilities decision 3,
    DATA.md §13). Returns the two numbers the composite needs:

        road_dollars_per_m   $/road-metre/yr (O&M + renewal, 50-yr life)
        fire_budget_annual   Fire Rescue gross operating budget, $/yr

    plus, when present, the OPERATING-basis transportation trio:

        road_ops_dollars_per_m   $/road-metre/yr    (maintenance + snow, NO capital)
        bike_ops_dollars_per_m   $/bikeway-metre/yr (maintenance + snow, NO capital)
        transit_budget_annual    ETS bus+LRT gross operating budget, $/yr

    ⚠️ The two road numbers are DIFFERENT BASES, not a duplicate — $50/m/yr
    lifecycle vs $4.635/m/yr operating, ~10.8x apart on the same metres. They
    feed different columns and must never be summed (city_unit_costs.json
    "_two_bases"). The operating trio is OPTIONAL: absent keys simply omit the
    transportation composite, so the file stays valid mid-sourcing.

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
    costs = {"road_dollars_per_m": float(road), "fire_budget_annual": float(fire_budget)}

    for out_key, block, field in (
        ("road_ops_dollars_per_m", "roadway_ops", "value"),
        ("bike_ops_dollars_per_m", "bikeway_ops", "value"),
        ("transit_budget_annual", "transit_ets", "operating_budget_gross_annual"),
    ):
        if block in data:
            # Present-but-malformed is a hand-edit error, not an absent key —
            # fail rather than silently dropping a term of the composite.
            try:
                costs[out_key] = float(data[block][field])
            except (KeyError, TypeError, ValueError) as e:
                raise ValueError(
                    f"{path}: {block}.{field} is missing or not a number ({e})"
                ) from e

    for name, val in (("roadway value", road), ("fire budget", fire_budget)):
        if not isinstance(val, (int, float)) or val <= 0:
            raise ValueError(f"{path}: {name} must be a positive number, got {val!r}")
    for key in ("road_ops_dollars_per_m", "bike_ops_dollars_per_m",
                "transit_budget_annual"):
        if key in costs and costs[key] <= 0:
            raise ValueError(f"{path}: {key} must be positive, got {costs[key]!r}")
    return costs


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
    names); the recent window uses ``"_3yr"``. When the permit frame carries
    ``ind_permits`` (the industrial permit-velocity count, SPEC_industrial.md
    A3 — older frames don't), it merges + fills + divides the same way into
    ``ind_permits{suffix}`` / ``ind_permits_per_acre{suffix}``. Returns the
    updated frame and the list of columns added, in output order.
    """
    units_col = f"new_dwelling_units{suffix}"
    permits_col = f"new_dwelling_permits{suffix}"
    upa_col = f"new_units_per_acre{suffix}"
    ppa_col = f"new_permits_per_acre{suffix}"
    has_ind = "ind_permits" in permits.columns
    ind_col = f"ind_permits{suffix}"
    ipa_col = f"ind_permits_per_acre{suffix}"

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
        "ind_permits": ind_col,
    })
    merge_cols = ["neighbourhood_name", units_col, permits_col]
    if has_ind:
        merge_cols.append(ind_col)
    joined = joined.merge(
        frame[merge_cols],
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
    added = [units_col, permits_col, upa_col, ppa_col]
    if has_ind:
        joined[ind_col] = joined[ind_col].fillna(0.0)
        joined[ipa_col] = joined[ind_col] / safe_area
        added += [ind_col, ipa_col]
    return joined, added


def join_and_calculate(
    assessment: pd.DataFrame,
    boundaries: gpd.GeoDataFrame,
    zoning: pd.DataFrame | None = None,
    roads: pd.DataFrame | None = None,
    bike: pd.DataFrame | None = None,
    stormwater: pd.DataFrame | None = None,
    fire: pd.DataFrame | None = None,
    transit: pd.DataFrame | None = None,
    water: pd.DataFrame | None = None,
    franchise: pd.DataFrame | None = None,
    permits: pd.DataFrame | None = None,
    permits_recent: pd.DataFrame | None = None,
    permits_long: pd.DataFrame | None = None,
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

    ``bike`` (optional, from load_bike.py) adds bike_m_total and computes
    bike_m_per_acre the same way (SPEC_services.md "Transportation lens").
    DEDICATED cycling assets only — shared roadways are excluded upstream
    because their metres are already in road_m_total, so the two supply
    columns are disjoint and may be read together. Boundaries with no
    dedicated route default to a true 0.

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
        # Revenue-lens readout columns, carried only if the caller computed them
        # (revenue_share_city in main.py, rev_frac_* from revenue_by_zone) —
        # both are optional upstream steps, so this must not require them.
        carried = [c for c in REVENUE_READOUT_COLUMNS if c in joined.columns]
        if carried:
            out_cols = [c for c in out_cols if c != "geometry"] + carried + ["geometry"]

    # Residential-revenue decomposition (res_levy from apply_tax_rates):
    # the residential-class subset of revenue_per_acre, same denominator.
    # The client derives the residential SHARE as res/revenue per acre
    # (denominators cancel), so no share column ships.
    if "total_res_revenue" in joined.columns:
        joined["res_revenue_per_acre"] = joined["total_res_revenue"] / safe_area
        out_cols = [c for c in out_cols if c != "geometry"] + [
            "total_res_revenue", "res_revenue_per_acre", "geometry",
        ]

    # Non-residential decomposition (nonres_levy from apply_tax_rates): the
    # non-res-rate subset of revenue_per_acre, same denominator + share-derived-
    # client-side conventions as the residential block above.
    if "total_nonres_revenue" in joined.columns:
        joined["nonres_revenue_per_acre"] = joined["total_nonres_revenue"] / safe_area
        out_cols = [c for c in out_cols if c != "geometry"] + [
            "total_nonres_revenue", "nonres_revenue_per_acre", "geometry",
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

    # Services lens: dedicated cycling supply (SPEC_services.md "Transportation
    # lens"). Same shape as roads — an unmatched bike hood is a reported drop,
    # and a boundary with no overlay is a true zero (no dedicated bike route
    # there), not missing data.
    if bike is not None:
        boundary_names = set(joined["neighbourhood_name"])
        unmatched_bike = sorted(set(bike["neighbourhood_name"]) - boundary_names)
        if unmatched_bike:
            logger.warning(
                "%d bike neighbourhood(s) with no boundary match (dropped):\n  %s",
                len(unmatched_bike),
                "\n  ".join(unmatched_bike),
            )

        joined = joined.merge(
            bike[["neighbourhood_name", *BIKE_COLUMNS]],
            on="neighbourhood_name",
            how="left",
            validate="m:1",
        )

        no_bike = joined["bike_m_total"].isna()
        if no_bike.any():
            logger.info(
                "%d boundary neighbourhood(s) with no dedicated bike route (default 0 m)",
                int(no_bike.sum()),
            )
        joined["bike_m_total"] = joined["bike_m_total"].fillna(0.0)
        joined["bike_m_per_acre"] = joined["bike_m_total"] / safe_area

        out_cols = (
            [c for c in out_cols if c != "geometry"]
            + BIKE_COLUMNS + ["bike_m_per_acre"] + ["geometry"]
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

    # Roads-only LIFECYCLE cost (SPEC_services.md "Roads cost — lifecycle").
    # The same $50/m/yr rate and the same metres as the roads term inside
    # svc_cost_per_acre — this simply publishes that term on its own, so a
    # roads-only lens can show a lifecycle figure without dragging fire in.
    #
    # ⚠️ NESTED, NOT ADDITIVE: cost_roads_life_per_acre is a COMPONENT of
    # svc_cost_per_acre (which is this + the allocated fire term). Never sum the
    # two — that double-counts roads. Contrast cost_roads_ops_per_acre, which is
    # the same metres on the OPERATING basis, ~10.8x smaller and never summable
    # with either (city_unit_costs.json "_two_bases").
    #
    # Deliberately in its OWN guard rather than inside the roads-and-fire branch
    # below: it needs only roads, so a run without fire data still publishes it
    # instead of silently dropping the one cost column a roads lens can show.
    if unit_costs is not None and roads is not None:
        joined["cost_roads_life_per_acre"] = (
            joined["road_m_per_acre"] * unit_costs["road_dollars_per_m"]
        )
        logger.info(
            "Roads LIFECYCLE cost: $%.2f/road-m/yr -> cost_roads_life_per_acre "
            "on %d hoods (MODELED, collector+local only, no capital-vs-ops mixing)",
            unit_costs["road_dollars_per_m"],
            int(joined["cost_roads_life_per_acre"].notna().sum()),
        )
        out_cols = (
            [c for c in out_cols if c != "geometry"]
            + ["cost_roads_life_per_acre"] + ["geometry"]
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

    # Transportation lens Stage 2: the OPERATING-basis cost terms
    # (SPEC_services.md "Transportation lens"). Runs HERE, after the transit
    # merge, because transit_dep_per_acre does not exist at the svc_cost_per_acre
    # block above.
    #
    # ⚠️ OPERATING basis: maintenance + snow clearing, NO capital replacement.
    # The roads term here is NOT the roads term inside svc_cost_per_acre — same
    # metres, $4.635/m/yr vs $50/m/yr lifecycle, ~10.8x apart. That is why every
    # column below carries _ops. Never sum the two (city_unit_costs "_two_bases").
    if unit_costs is not None:
        transport_terms: dict[str, pd.Series] = {}
        if roads is not None and "road_ops_dollars_per_m" in unit_costs:
            transport_terms["cost_roads_ops_per_acre"] = (
                joined["road_m_per_acre"] * unit_costs["road_ops_dollars_per_m"]
            )
        if bike is not None and "bike_ops_dollars_per_m" in unit_costs:
            transport_terms["cost_bike_ops_per_acre"] = (
                joined["bike_m_per_acre"] * unit_costs["bike_ops_dollars_per_m"]
            )
        if transit is not None and "transit_budget_annual" in unit_costs:
            # Denominator is the transit frame's OWN citywide total (pre-join),
            # so numerator and denominator describe the same population — the
            # fire pattern exactly. Unmatched hoods still consumed budget.
            citywide_dep = float(transit["transit_dep_total"].sum())
            if citywide_dep <= 0:
                raise ValueError(
                    "Citywide scheduled stop-events is not positive "
                    f"({citywide_dep}) — cannot derive a per-departure cost"
                )
            # ⚠️ THIS IS A SHARE ALLOCATION, NOT A RATE. transit_dep_total is a
            # MEAN-WEEKDAY count and the budget is ANNUAL, so this intermediate
            # ("annual dollars per mean-weekday stop-event") is meaningless on its
            # own — but hood_dep/citywide_dep is a valid share, and the terms
            # sum back to the budget. Do NOT "fix" the units by scaling to ~250
            # weekdays: that would multiply every hood's cost by 250.
            transit_cost_per_dep = unit_costs["transit_budget_annual"] / citywide_dep
            transport_terms["cost_transit_ops_per_acre"] = (
                joined["transit_dep_per_acre"] * transit_cost_per_dep
            )

        for col, series in transport_terms.items():
            joined[col] = series
        added_transport = list(transport_terms)

        # All-or-nothing across the three terms: a two-term metric labelled
        # "transportation" would be mislabeled (same rule svc_cost_per_acre uses).
        wanted = {"cost_roads_ops_per_acre", "cost_bike_ops_per_acre",
                  "cost_transit_ops_per_acre"}
        missing = sorted(wanted - set(transport_terms))
        if not missing:
            joined["transport_cost_ops_per_acre"] = (
                joined["cost_roads_ops_per_acre"]
                + joined["cost_bike_ops_per_acre"]
                + joined["cost_transit_ops_per_acre"]
            )
            added_transport.append("transport_cost_ops_per_acre")
            logger.info(
                "Transportation OPERATING composite: $%.3f/road-m/yr + "
                "$%.3f/bike-m/yr + $%.2f/weekday-departure ($%.0f ETS bus+LRT "
                "budget / %.0f citywide stop-events) -> transport_cost_ops_per_acre "
                "on %d hoods (MODELED, ops only — no capital)",
                unit_costs["road_ops_dollars_per_m"],
                unit_costs["bike_ops_dollars_per_m"],
                transit_cost_per_dep, unit_costs["transit_budget_annual"],
                citywide_dep,
                int(joined["transport_cost_ops_per_acre"].notna().sum()),
            )
        elif transport_terms:
            logger.warning(
                "Transportation OPERATING composite SKIPPED — missing term(s): %s. "
                "The per-term columns that ARE available still ship (%s); only the "
                "labelled composite is withheld.",
                ", ".join(missing), ", ".join(added_transport) or "none",
            )

        if added_transport:
            out_cols = (
                [c for c in out_cols if c != "geometry"]
                + added_transport + ["geometry"]
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
        # Optional long "since 2009" window — same merge, `_long`-suffixed columns
        # (SPEC_development.md "Lens A long window", 2026-07-21).
        if permits_long is not None:
            joined, long_cols = _merge_permit_window(
                joined, permits_long, safe_area, "_long"
            )
            added += long_cols

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
        if "res_revenue_lot_eligible" in joined.columns:
            joined["res_revenue_per_lot_acre"] = (
                joined["res_revenue_lot_eligible"] / safe_lot
            )
            added.append("res_revenue_per_lot_acre")
        if "nonres_revenue_lot_eligible" in joined.columns:
            joined["nonres_revenue_per_lot_acre"] = (
                joined["nonres_revenue_lot_eligible"] / safe_lot
            )
            added.append("nonres_revenue_per_lot_acre")
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
# placement is an open call). The cost_*_ops_per_acre trio and
# transport_cost_ops_per_acre are the Transportation lens Stage 2 composite on a
# strictly OPERATING basis (maintenance + snow, NO capital replacement) —
# ⚠️ cost_roads_ops_per_acre and the roads term inside svc_cost_per_acre are the
# SAME METRES ON DIFFERENT BASES, ~10.8x apart; the client must never sum or
# compare them, which is what the _ops suffix exists to signal.
# cost_roads_life_per_acre publishes that lifecycle roads term on its own, so a
# roads-only lens can show it without fire. ⚠️ It is NESTED INSIDE
# svc_cost_per_acre (never sum the two — double-counts roads) and is the SAME
# METRES as cost_roads_ops_per_acre on the other basis (never sum those either). new_units_per_acre
# and new_permits_per_acre (+ the total/permit-count pair for the tooltip) are the
# Development lens A activity metrics — new dwelling units / new permits from
# issued permits, a change/flow signal, NOT revenue or cost (SPEC_development.md).
# ind_permits_per_acre (+ ind_permits count) is the industrial permit-velocity
# cut — new-construction 400-series building_type permits per acre, count only
# (units_added is meaningless for industrial), same windows (SPEC_industrial.md A3).
# res_revenue_per_acre / res_revenue_per_lot_acre are the residential-revenue
# decomposition: the RESIDENTIAL + OTHER RESIDENTIAL class subset of the levy
# (a subset of revenue_per_acre, never all of what the land pays — the client
# must say so); the residential SHARE is derived client-side as res/revenue
# per acre (same denominator cancels), so no share column ships.
# nonres_revenue_per_acre / nonres_revenue_per_lot_acre are the complement by
# rate class (COMMERCIAL + MA DERELICT + DESIGNATED IND PROPERTIES slices —
# SPEC_industrial.md A1), same conventions.
SLIM_COLUMNS = [
    "neighbourhood_name", "value_per_acre", "revenue_per_acre",
    "res_revenue_per_acre", "res_revenue_per_lot_acre",
    "nonres_revenue_per_acre", "nonres_revenue_per_lot_acre",
    "set_aside_frac", "is_set_aside", "set_aside_reason",
    "frac_never", "frac_notyet", "frac_inst",
    "frac_residential", "frac_commercial", "frac_industrial",
    "frac_mixed", "frac_dc", "frac_other",
    "is_residential", "road_m_per_acre", "bike_m_per_acre",
    "storm_charge_per_acre",
    "fire_events_per_acre", "transit_dep_per_acre",
    "water_charge_per_acre", "water_fixed_per_acre",
    "svc_cost_per_acre", "cost_roads_life_per_acre",
    "cost_roads_ops_per_acre", "cost_bike_ops_per_acre",
    "cost_transit_ops_per_acre", "transport_cost_ops_per_acre",
    "new_units_per_acre", "new_permits_per_acre",
    "new_dwelling_units", "new_dwelling_permits",
    "new_units_per_acre_3yr", "new_permits_per_acre_3yr",
    "new_dwelling_units_3yr", "new_dwelling_permits_3yr",
    "new_units_per_acre_long", "new_permits_per_acre_long",
    "new_dwelling_units_long", "new_dwelling_permits_long",
    "ind_permits_per_acre", "ind_permits",
    "ind_permits_per_acre_3yr", "ind_permits_3yr",
    "ind_permits_per_acre_long", "ind_permits_long",
    "value_per_lot_acre", "revenue_per_lot_acre", "parcel_frac",
    "far",
    # Revenue-lens readout (2026-08-01): the absolute levy, its share of the
    # CITYWIDE levy (computed in main.py against the full roll, NOT renormalised
    # over whatever survives the boundary join), and where that revenue comes
    # from by zoning category — the Uses lens's own polygons weighted by levy
    # instead of by area. `rev_frac_unzoned` rides along rather than being
    # hidden: it is ~0.002% citywide today and must not be able to grow silently.
    "total_revenue", "revenue_share_city",
    "rev_frac_never", "rev_frac_notyet", "rev_frac_inst",
    "rev_frac_residential", "rev_frac_commercial", "rev_frac_industrial",
    "rev_frac_mixed", "rev_frac_dc", "rev_frac_other", "rev_frac_unzoned",
    # Cuts ACROSS the family above rather than joining it — the rev_frac_*
    # partition sums to 1.0 and this asks a different question of the same
    # dollars (load_zoning.EXEMPT_CANDIDATE_ZONES).
    "rev_frac_exempt",
    "geometry",
]


# CRS used for the setback buffer — must be projected (metres), not degrees.
# Matches load_boundaries: NAD83 / Alberta 10-TM (Forest).
SETBACK_CRS = "EPSG:3400"

# Served precision. This file is fetched at BOOT, before the map can draw data,
# by every visitor whatever lens they use — so its size is the one cost that
# grows with the number of lenses (each adds per-hood columns here). GDAL
# defaults to 15 digits on both, which was half the gzipped payload.
#
# 5 dp matches WEB_PRECISION in load_roads/load_bike and the load_zoning default
# — ~1 m at Edmonton's latitude, on geometry already simplified to 10 m and
# buffered inward 45 m.
WEB_PRECISION = 5
# Significant figures, not decimal places: scale-invariant, so dollars-per-acre
# keep ~1 dp and fractions keep 6 without a per-column table. 6 is above two
# floors that 3 would break — the 0.01 mix-shift comparison in
# check_revenue_deltas, and figures re-derived in the audit record.
WEB_SIGNIFICANT_FIGURES = 6


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

    # Rounding happens at WRITE time, so the returned frame stays full-precision
    # for any caller that computes from it.
    slim.to_file(
        output_path, driver="GeoJSON",
        COORDINATE_PRECISION=WEB_PRECISION,
        SIGNIFICANT_FIGURES=WEB_SIGNIFICANT_FIGURES,
    )
    logger.info(
        "Wrote slim GeoJSON (%d features, %s, simplify=%sm, setback=%sm, "
        "%sdp/%ssf) to %s",
        len(slim), crs, simplify_tolerance_m, setback_m,
        WEB_PRECISION, WEB_SIGNIFICANT_FIGURES, output_path,
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
