"""Modeled electricity + gas franchise-fee revenue per neighbourhood (utility lens #3).

Reconstructs, per residential dwelling, the EDTI electricity distribution charge
and the ATCO Gas North delivery charge from verified tariffs (Methods SD-SE),
then applies the two City-of-Edmonton franchise-fee percentages (electricity
Local Access Fee 17.65%; gas Rider A 35%) to get the CITY-revenue lines. Design
+ locked decisions: docs/SPEC_utilities.md Lens 3.

**Everything here is MODELED, not billed** — and Tier 3, with a caveat sharper
than the other lenses:

    COLLINEAR WITH DWELLING COUNT. The consumption proxy is FLAT per dwelling
    (7,200 kWh/yr, 115 GJ/yr), so every per-hood column is just
    ``dwellings_in_hood x a constant``. As a map these would re-plot dwelling
    density and nothing more (SPEC_utilities Tier-3 caveat). Their genuine value
    is the citywide DOLLAR TOTALS — real City revenue keyed to utility activity,
    comparable to the tax levy — and the per-hood revenue ATTRIBUTION. The
    distinct spatial signal (commercial load, which pays different DAS schedules
    at far higher consumption) is OUT OF SCOPE: no commercial consumption proxy,
    same reason water excluded it. ``dwelling_count`` ships as its own column so
    the collinearity is explicit, not buried inside a dollar figure.

    MODELED LAF RUNS ~1/3 LOW vs the City's published per-customer franchise fee
    (~$8.33/mo = ~$100/yr, 2026): the fee is levied on EDTI's FULL distribution
    revenue (riders/pass-throughs), not just the base customer+energy schedule
    modeled here. A known, documented underestimate (rates JSON provenance);
    the per-hood shape is unaffected. Validation: FINDINGS_utility_validation.

Scope — residential only, and the SAME dwelling model as the water lens: the
connection/dedupe machinery lives in ``load_water.build_connections`` and is
shared, so the two lenses cannot silently disagree on the household count
(551,831 at present). Each dwelling is billed as its own electricity + gas meter
(unlike water, where a building shares one connection) — the SPEC's per-dwelling
proxy stance for Lens 3.
"""

import json
import logging
from pathlib import Path

import pandas as pd

from load_water import build_connections

logger = logging.getLogger(__name__)

# City's published average residential electricity franchise fee, for the
# per-dwelling sanity check only (Methods SD: ~$7.94/mo 2025 -> ~$8.33/mo 2026).
# The model is expected to fall UNDER this (base schedule vs full dist. revenue).
PUBLISHED_LAF_MONTHLY_2026 = 8.33


def load_franchise_rates(rates_json: str | Path, year: int) -> dict:
    """Return the rate entry for ``year``; hard-error on a missing year.

    Same pin-the-year contract as load_water_rates — silently modeling one
    year's tariffs while claiming another is the mill-rate desync bug.
    """
    with open(rates_json, encoding="utf-8") as f:
        rates = json.load(f)
    entry = rates["years"].get(str(year))
    if entry is None:
        raise ValueError(
            f"no franchise rates for {year} in {rates_json} — "
            f"available: {sorted(rates['years'])}"
        )
    return entry


def _per_dwelling_charges(rates: dict) -> dict:
    """Flat annual $ per dwelling — the four modeled quantities.

    Constant across every dwelling (the proxy is flat), so the per-hood
    columns are these times the hood's dwelling count. Returned explicitly so
    the sanity-check log and the tests can see the per-dwelling figures.
    """
    elec_distribution = (
        365.0 * rates["elec_customer_daily"]
        + rates["elec_kwh_per_dwelling_year"] * rates["elec_energy_per_kwh"]
    )
    gas_delivery = (
        365.0 * rates["gas_fixed_daily"]
        + rates["gas_gj_per_dwelling_year"]
        * (rates["gas_variable_per_gj"] + rates["gas_rider_t_per_gj"]
           + rates["gas_rider_l_per_gj"])
    )
    return {
        "elec_distribution_annual": elec_distribution,
        "elec_laf_revenue": rates["elec_laf_fraction"] * elec_distribution,
        "gas_delivery_annual": gas_delivery,
        "gas_franchise_revenue": rates["gas_franchise_fraction"] * gas_delivery,
    }


def load_franchise(
    assessment_csv: str | Path,
    property_info_csv: str | Path,
    rates_json: str | Path,
    year: int,
) -> pd.DataFrame:
    """Model annual electricity/gas franchise-fee revenue per neighbourhood.

    Returns a DataFrame keyed by ``neighbourhood_name``:
        dwelling_count            float  modeled residential dwellings (shared
                                         with the water lens; the collinear driver)
        elec_distribution_annual  float  modeled EDTI distribution charge, $/yr
        elec_laf_revenue          float  17.65% Local Access Fee (CITY revenue), $/yr
        gas_delivery_annual       float  modeled ATCO Gas North delivery charge, $/yr
        gas_franchise_revenue     float  35% Rider A franchise fee (CITY revenue), $/yr
    """
    rates = load_franchise_rates(rates_json, year)
    conns = build_connections(assessment_csv, property_info_csv)
    per_dwelling = _per_dwelling_charges(rates)

    dwellings = (
        conns.groupby("neighbourhood_name", as_index=False)["units"]
        .sum()
        .rename(columns={"units": "dwelling_count"})
    )
    dwellings["dwelling_count"] = dwellings["dwelling_count"].astype(float)
    for col, per in per_dwelling.items():
        dwellings[col] = dwellings["dwelling_count"] * per

    total_dwellings = dwellings["dwelling_count"].sum()
    laf_total = dwellings["elec_laf_revenue"].sum()
    gas_fr_total = dwellings["gas_franchise_revenue"].sum()
    modeled_laf_monthly = per_dwelling["elec_laf_revenue"] / 12.0
    logger.info(
        "Franchise model (year %d rates, residential scope — COLLINEAR with "
        "dwelling count, MODELED not billed): %d dwellings -> %d hoods. "
        "CITY revenue: electricity LAF (17.65%%) $%.1fM/yr, gas franchise "
        "(35%%) $%.1fM/yr, combined $%.1fM/yr. Modeled elec distribution "
        "$%.1fM/yr, gas delivery $%.1fM/yr. Per-dwelling LAF $%.2f/mo modeled "
        "vs $%.2f/mo City-published (base schedule underestimates full "
        "distribution revenue — see rates JSON).",
        year, int(total_dwellings), len(dwellings),
        laf_total / 1e6, gas_fr_total / 1e6, (laf_total + gas_fr_total) / 1e6,
        dwellings["elec_distribution_annual"].sum() / 1e6,
        dwellings["gas_delivery_annual"].sum() / 1e6,
        modeled_laf_monthly, PUBLISHED_LAF_MONTHLY_2026,
    )
    return dwellings
