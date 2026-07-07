"""Modeled water + sanitary/wastewater charge per neighbourhood (utility lens #2).

Reconstructs the EPCOR residential water + wastewater-treatment + sanitary-
collection bill per CONNECTION from verified 2026 tariffs (Methods §A–B) and
the assessment roll, then aggregates to neighbourhoods. Design + locked
decisions: docs/SPEC_utilities.md Lens 2.

**Everything here is MODELED, not billed** — and Tier 2: unlike stormwater's
bylaw-native area formula, every component is per-connection/per-household,
so the per-acre map partly tracks household density (Methods §G pitfall; the
display must carry that caveat). Two outputs per hood keep the split honest:

    water_fixed_annual   per-connection daily charges × 365 — the
                         infrastructure-connection signal
    water_charge_annual  fixed + volumetric (consumption proxy × rates) —
                         the modeled total bill, the display's colour column

Scope — residential only (locked decision 2026-07-06): classes with a
verified consumption proxy. RESIDENTIAL and MA DERELICT RESIDENTIAL rows are
households; OTHER RESIDENTIAL rows are multi-res buildings. COMMERCIAL /
FARMLAND / everything else is excluded + counted (verified rates exist but
no consumption benchmark — no invented numbers).

The modeled assumptions, all explicit and tunable:
- **Connections**: household rows grouped by exact lat/long — one connection
  per point (a condo tower's units are individual roll records at one point,
  FINDINGS_lot_dedupe). Each OTHER RESIDENTIAL row is one building
  connection; its unit count is estimated from the property-info CSV's
  gross floor area (m², confirmed) at ``M2_GROSS_PER_UNIT``; null/zero
  floor areas are excluded + counted.
- **Meter size** is not public — assumed from the connection's unit count
  (``_meter_size_mm`` bands), using only the four sizes whose fixed charges
  are verified for BOTH water and sanitary (15/25/100/300 mm).
- **Consumption**: 14.3 m³/month/household (EPCOR's published 2025
  benchmark). Single-unit connections bill on the residential inclining
  block; multi-unit connections on the multi-res declining block.
"""

import json
import logging
from pathlib import Path

import pandas as pd

from load_assessment import NAME_CORRECTIONS

logger = logging.getLogger(__name__)

# Classes modeled as one household per roll record. MA DERELICT RESIDENTIAL
# stays in (a standing structure is a serviced connection); logged either way.
HOUSEHOLD_CLASSES = {"RESIDENTIAL", "MA DERELICT RESIDENTIAL"}
MULTIRES_CLASS = "OTHER RESIDENTIAL"

# EPCOR's published typical-household benchmark (14,300 L/month, 2025 —
# Methods §A). The volumetric proxy for every modeled household.
MONTHLY_M3_PER_HOUSEHOLD = 14.3

# Gross floor area per dwelling unit for OTHER RESIDENTIAL buildings (m² —
# includes corridors/common space, hence above typical suite area). Modeled
# assumption; the roll has no unit counts for purpose-built rentals.
M2_GROSS_PER_UNIT = 90.0


def _meter_size_mm(units: int) -> int:
    """Assumed meter size for a connection serving ``units`` dwellings.

    Bands use only the four sizes with fixed charges verified for both water
    and sanitary (rates JSON provenance). Modeled assumption, not data.
    """
    if units <= 1:
        return 15
    if units < 50:
        return 25
    if units < 300:
        return 100
    return 300


def load_water_rates(rates_json: str | Path, year: int) -> dict:
    """Return the rate entry for ``year``; hard-error on a missing year.

    Silently modeling one year's tariffs while claiming another is the
    mill-rate desync bug — the caller pins the rate year explicitly.
    """
    with open(rates_json, encoding="utf-8") as f:
        rates = json.load(f)
    entry = rates["years"].get(str(year))
    if entry is None:
        raise ValueError(
            f"no water rates for {year} in {rates_json} — "
            f"available: {sorted(rates['years'])}"
        )
    return entry


def _block_charge(monthly_m3: float, blocks: list) -> float:
    """Monthly volumetric charge across [upper_bound, rate] blocks.

    Bounds are cumulative m³; a null bound is open-ended (the last block).
    Works for both the residential inclining and multi-res declining shapes.
    """
    total, prev = 0.0, 0.0
    for bound, rate in blocks:
        if bound is None or monthly_m3 <= bound:
            return total + (monthly_m3 - prev) * rate
        total += (bound - prev) * rate
        prev = bound
    raise ValueError(f"block schedule has no open-ended final block: {blocks}")


def _connection_charges(units: pd.Series, rates: dict) -> pd.DataFrame:
    """Annual fixed + volumetric $ for connections serving ``units`` dwellings."""
    meter = units.map(_meter_size_mm).astype(str)
    fixed_daily = (
        meter.map(rates["water_fixed_daily"])
        + meter.map(rates["sanitary_fixed_daily"])
        + rates["wastewater_fixed_daily"]
    )
    monthly_m3 = units * MONTHLY_M3_PER_HOUSEHOLD
    flat = rates["wastewater_per_m3"] + rates["sanitary_per_m3"]
    vol_monthly = [
        _block_charge(
            m3,
            rates["water_blocks_residential"] if u == 1 else rates["water_blocks_multires"],
        ) + m3 * flat
        for u, m3 in zip(units, monthly_m3)
    ]
    return pd.DataFrame({
        "fixed_annual": 365.0 * fixed_daily.to_numpy(),
        "vol_annual": 12.0 * pd.Series(vol_monthly, index=units.index).to_numpy(),
    }, index=units.index)


def load_water(
    assessment_csv: str | Path,
    property_info_csv: str | Path,
    rates_json: str | Path,
    year: int,
) -> pd.DataFrame:
    """Model the annual residential water + sanitary charge per neighbourhood.

    Returns a DataFrame keyed by ``neighbourhood_name``:
        water_fixed_annual   float  modeled per-connection fixed charges, $/yr
        water_charge_annual  float  fixed + volumetric total, $/yr
    """
    rates = load_water_rates(rates_json, year)

    df = pd.read_csv(
        assessment_csv,
        usecols=["Account Number", "Assessment Class 1", "Neighbourhood",
                 "Latitude", "Longitude"],
        low_memory=False,
    ).rename(columns={
        "Account Number": "account_number",
        "Assessment Class 1": "assessment_class",
        "Neighbourhood": "neighbourhood_name",
        "Latitude": "latitude",
        "Longitude": "longitude",
    })
    df["neighbourhood_name"] = (
        df["neighbourhood_name"].astype("string").str.strip().str.upper()
        .replace(NAME_CORRECTIONS)
    )

    is_household = df["assessment_class"].isin(HOUSEHOLD_CLASSES)
    is_multires = df["assessment_class"] == MULTIRES_CLASS
    out_of_scope = df.loc[~is_household & ~is_multires, "assessment_class"]
    logger.info(
        "Water model scope (residential only — locked 2026-07-06): %d household "
        "rows + %d multi-res buildings; %d rows out of scope (no consumption "
        "proxy):\n  %s",
        int(is_household.sum()), int(is_multires.sum()), len(out_of_scope),
        "\n  ".join(f"{c}: {n:,}" for c, n in out_of_scope.value_counts().items()),
    )

    # --- household connections: one per exact roll point --------------------
    hh = df.loc[is_household]
    no_coords = hh["latitude"].isna() | hh["longitude"].isna()
    if no_coords.any():
        logger.warning(
            "%d household rows have null coordinates — excluded (cannot be "
            "grouped into a connection)", int(no_coords.sum()),
        )
    hh = hh.loc[~no_coords]
    conns = (
        hh.groupby(["latitude", "longitude"], sort=False)
        .agg(units=("account_number", "size"),
             neighbourhood_name=("neighbourhood_name", "first"))
        .reset_index(drop=True)
    )

    # --- multi-res buildings: one connection each, units from floor area ----
    mr = df.loc[is_multires, ["account_number", "neighbourhood_name"]]
    if len(mr):
        info = pd.read_csv(
            property_info_csv,
            usecols=["Account Number", "Total Gross Area"],
            low_memory=False,
        ).rename(columns={"Account Number": "account_number",
                          "Total Gross Area": "gross_m2"})
        info["gross_m2"] = pd.to_numeric(info["gross_m2"], errors="coerce")
        mr = mr.merge(info, on="account_number", how="left")
        no_area = mr["gross_m2"].isna() | (mr["gross_m2"] <= 0)
        if no_area.any():
            logger.warning(
                "%d of %d multi-res buildings have null/zero gross floor area — "
                "excluded (their households are uncounted; the hood totals "
                "understate accordingly)", int(no_area.sum()), len(mr),
            )
        mr = mr.loc[~no_area].copy()
        mr["units"] = (mr["gross_m2"] / M2_GROSS_PER_UNIT).round().clip(lower=1).astype(int)
        conns = pd.concat(
            [conns, mr[["units", "neighbourhood_name"]]], ignore_index=True,
        )

    if not len(conns):
        raise ValueError("no water connections modeled — inputs are wrong")

    charges = _connection_charges(conns["units"], rates)
    conns = pd.concat([conns, charges], axis=1)

    out = (
        conns.groupby("neighbourhood_name", as_index=False)
        .agg(water_fixed_annual=("fixed_annual", "sum"),
             water_vol_annual=("vol_annual", "sum"))
    )
    out["water_charge_annual"] = out["water_fixed_annual"] + out["water_vol_annual"]
    out = out.drop(columns=["water_vol_annual"])

    meter_mix = conns["units"].map(_meter_size_mm).value_counts().sort_index()
    logger.info(
        "Water model (year %d rates): %d connections / %d modeled households "
        "-> %d hoods, citywide $%.1fM/yr ($%.1fM fixed + $%.1fM volumetric). "
        "Meter mix (assumed): %s",
        year, len(conns), int(conns["units"].sum()), len(out),
        out["water_charge_annual"].sum() / 1e6,
        out["water_fixed_annual"].sum() / 1e6,
        (out["water_charge_annual"] - out["water_fixed_annual"]).sum() / 1e6,
        ", ".join(f"{m}mm: {n:,}" for m, n in meter_mix.items()),
    )
    return out
