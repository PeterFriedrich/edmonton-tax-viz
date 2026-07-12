"""New residential dwelling supply per neighbourhood (Development & Infill lens A).

Counts new dwelling units created per neighbourhood from issued building
permits (``24uj-dj8v``, General Building Permits), summed over a pinned window
of full calendar years. This is the permit-based answer to "where are new homes
actually being built now" — the direct signal that
``FINDINGS_growth_servicing.md`` could only proxy with median building-stock age.
Design + locked decisions: docs/SPEC_development.md "Lens A"; dataset facts
data/DATA.md §"Building Permits".

**Activity metric only — new CONSTRUCTION.** The numerator is ``units_added``
on permits whose ``work_type`` is a genuinely-new structure
(``NEW_WORK_TYPES``) and whose ``building_type`` is a residential dwelling
(``RESIDENTIAL_BUILDING_TYPES``). Suite conversions / add-suites codes
(``(07)``/``(08)``/``(09)``) DO add dwellings but are infill densification, not
new construction — they are deliberately OUT of this first cut and belong to the
Lens B infill story. Garages, decks, commercial building types are excluded.

**Explicit dictionaries, warn on unseen (DECISIONS 2026-06-29).** The permit
vocabulary carries many spelling variants of the same category (``Apartments
(310)`` vs ``Apartment (310)`` vs ``Apartment Condos (315)``; ``Row House
(330)`` vs ``Row Houses (330)``; ``Semi Detached House`` with no code) — so the
sets below are hand-enumerated from the live vocabulary (2026-07-12), never
prefix-matched on the ``(NNN)`` code. Any ``work_type`` / ``building_type`` value
NOT in the corresponding KNOWN set is logged loudly (it may be a new residential
variant we should count) but is treated as excluded, never silently swept in.

**Activity is not the money path.** An unmatched permit-side neighbourhood
contributes 0 activity (a visibly blank hood), not a silently wrong dollar
figure — so the name join is warn-not-fail (unlike the assessment money path's
CI guard, scripts/check_unmatched_names.py). The only known straggler after
NAME_CORRECTIONS is ``GLENORA, ROSSLYN`` (1 unit, 2026-07-12), immaterial.
"""

import logging
from pathlib import Path

import pandas as pd

from load_assessment import NAME_CORRECTIONS

logger = logging.getLogger(__name__)

# work_type values counted as NEW construction (live vocab 2026-07-12). Suite
# conversions ((07)/(08)/(09)), additions, alterations, demolitions etc. add no
# new standalone dwelling and are excluded — infill densification is Lens B.
NEW_WORK_TYPES = frozenset({
    "(01) New",
    "(01) Building - New",
    "(01) New House",
})

# Full work_type vocabulary observed 2026-07-12 — used ONLY to detect NEW,
# UNSEEN codes (which get a loud log line and are treated as excluded until
# reviewed). NEW_WORK_TYPES is a subset of this.
KNOWN_WORK_TYPES = NEW_WORK_TYPES | frozenset({
    "(02) Addition",
    "(03) Interior Alterations", "(03) Exterior Alterations", "(03) Deck Attached",
    "(04) Foundation", "(04) Footing & Foundation", "(04) Excavation",
    "(05) Structure", "(05) Structural Frame",
    "(07) Add Suites to Single Dwelling", "(08) Add Suites to Multi-Dwelling",
    "(09) Convert Non-Res to Residential", "(10) Convert Residential to Non-Res",
    "(11) Remove Suites", "(11) Remove Suite(s)",
    "(12) Move Building OnSite", "(12) Move Building on to Site", "(12) Move on Mobile Home",
    "(14) Hot Tub", "(14) Swimming Pool",
    "(15) Attached Garage/Carport",
    "(98) Move Building OFF Site", "(98) Move Building OffSite",
    "(99) Demolition",
})

# building_type values counted as a residential DWELLING (live vocab
# 2026-07-12), every spelling variant enumerated explicitly. Backyard House is a
# garden/secondary dwelling but IS a new dwelling unit when built new, so it
# counts. Mixed Use (522) is commercial-coded and ambiguous on residential unit
# count — excluded from this first cut (noted in SPEC_development.md).
RESIDENTIAL_BUILDING_TYPES = frozenset({
    # Single detached (110/115) + backyard/garden house
    "Single Detached House (110)", "Single House (110)",
    "Single Detached Condo (115)", "Backyard House (110)",
    # Semi-detached / duplex (210/215)
    "Semi-Detached House (210)", "Semi Detached House (210)", "Semi Detached House",
    "Semi-Detached Condo (215)", "Semi Detached Condo (215)",
    "Duplex (210)", "Duplex Condo (215)",
    # Row house / townhouse (330/335)
    "Row House (330)", "Row Houses (330)",
    "Row House Condo (335)", "Row House Condos (335)",
    # Apartment (310/315)
    "Apartments (310)", "Apartment (310)",
    "Apartment Condos (315)", "Apartment Condo (315)",
    # Mobile home
    "Mobile Home (130)",
})

# Full building_type vocabulary observed 2026-07-12 — the residential set above
# UNION the non-residential codes below. Anything absent from this union is
# UNSEEN: logged loudly, treated as excluded until reviewed (it could be a new
# residential variant that should be counted).
KNOWN_BUILDING_TYPES = RESIDENTIAL_BUILDING_TYPES | frozenset({
    "Animal and Plant Services (410)", "Carport (090)",
    "Clinics, Health Units (642)", "Communication Buildings (470)",
    "Convention Centres (536)", "Day Cares, Nursing Homes (650)",
    "Detached Deck (020)", "Detached Garage (010)", "Detached Greenhouse (030)",
    "Detached Misc. Structure (090)", "Detached Shed (040)",
    "Elementary Schools (620)", "Engineering (490)", "Funeral Homes (590)",
    "Gazebo (090)", "Government Legislative/Admin (610)", "Greenhouse (030)",
    "Hoarding (910)", "Hospitals (640)", "Hotels (530)",
    "Indoor Recreational Buildings (560)", "Laboratory/Research Centres (580)",
    "Law Enforcement/Emergency Svcs. (612)", "Libraries/Museums/Art Galleries (630)",
    "Maintenance Buildings incl Hangars (450)", "Malls, Office/Retail (512)",
    "Manufacturing Buildings (430)", "Mixed Use (522)", "Motels (532)",
    "Office Buildings (520)", "Office Complex (522)",
    "Other Accommodation (534)", "Other Accomodation (534)",
    "Outdoor Recreational Buildings (562)", "Parkade (490)", "Play Structure (090)",
    "Post-secondary Institutions (624)", "Religious Buildings (660)",
    "Restaurants and Bars (540)", "Retail and Shops (510)", "Retail - Motor Vehicle (570)",
    "Secondary Schools (622)", "Service Stations, Repair Garages (572)", "Shed (040)",
    "Storage Buildings, Warehouses (460)", "Temporary Structure (099)",
    "Temporary Structures (999)", "Theatre and Performing Arts Ctrs (550)",
    "Transportation Terminals (440)", "Universities (626)", "Utility Buildings (480)",
})

# Permit-CSV hood names → boundary names. The permit `neighbourhood` is already
# UPPERCASE and matches our format; the shared NAME_CORRECTIONS (CHAPPELLE AREA →
# CHAPPELLE, etc.) resolves every AREA-suffix greenfield hood that carries
# activity. No permit-local additions are needed as of 2026-07-12 — kept as a
# named layer (fire-lens pattern) so a future straggler has an obvious home.
PERMIT_NAME_CORRECTIONS = {**NAME_CORRECTIONS}

REQUIRED_COLUMNS = ("year", "work_type", "building_type", "units_added", "neighbourhood")


def load_permits(
    permits_csv: str | Path,
    years: tuple[int, ...],
) -> pd.DataFrame:
    """New residential dwelling supply per neighbourhood over a pinned window.

    ``years`` is the pinned window of FULL calendar years (main.py
    PERMIT_YEARS). Returns a DataFrame:
        neighbourhood_name    str    normalized + PERMIT_NAME_CORRECTIONS applied
        new_dwelling_units    float  Σ units_added, new-construction ∩ residential
        new_dwelling_permits  int    permit count behind that sum

    A hood absent from the result had zero new residential dwellings in the
    window — join_and_calculate fills the true 0 (roads/fire semantics).
    """
    if not years:
        raise ValueError("years window is empty")
    years = tuple(sorted(years))

    header = pd.read_csv(permits_csv, nrows=0)
    for needed in REQUIRED_COLUMNS:
        if needed not in header.columns:
            raise ValueError(
                f"expected column {needed!r} not in {permits_csv} — headers: "
                f"{list(header.columns)}. The Socrata $select in "
                f"scripts/download_data.py may have drifted."
            )

    df = pd.read_csv(permits_csv, usecols=list(REQUIRED_COLUMNS), low_memory=False)
    n_total = len(df)

    # --- year window --------------------------------------------------------
    year = pd.to_numeric(df["year"], errors="coerce")
    bad_year = year.isna()
    if bad_year.any():
        logger.warning(
            "%d of %d permit rows have an unparseable year — excluded",
            int(bad_year.sum()), n_total,
        )
    df = df.loc[~bad_year].copy()
    df["year"] = year.loc[~bad_year].astype(int)

    # Drift guard: a pinned window year with zero rows means the PERMIT_YEARS
    # pin is stale or the dataset changed (mirrors the fire-lens guard).
    per_year_all = df["year"].value_counts()
    for y in years:
        if per_year_all.get(y, 0) == 0:
            raise ValueError(
                f"window year {y} has ZERO permits in {permits_csv} — the "
                f"PERMIT_YEARS pin is wrong or the dataset drifted (years "
                f"present: {sorted(per_year_all.index)[:3]}…"
                f"{sorted(per_year_all.index)[-3:]})"
            )
    in_window = df[df["year"].isin(years)].copy()
    logger.info(
        "Permits in window %s: %d of %d rows (%s)",
        years, len(in_window), n_total,
        ", ".join(f"{y}: {int((in_window['year'] == y).sum()):,}" for y in years),
    )

    # --- work_type filter (new construction) --------------------------------
    work = in_window["work_type"].astype("string").str.strip()
    null_work = work.isna() | (work == "")
    if null_work.any():
        logger.info(
            "%d in-window permits have a null/blank work_type — excluded "
            "(cannot confirm new construction)", int(null_work.sum()),
        )
    unseen_work = sorted(set(work[~null_work].unique()) - KNOWN_WORK_TYPES)
    if unseen_work:
        logger.warning(
            "work_type values not in KNOWN_WORK_TYPES — EXCLUDED as non-new "
            "until reviewed (add to load_permits.py if any is new construction): %s",
            unseen_work,
        )
    is_new = work.isin(NEW_WORK_TYPES)

    # --- building_type filter (residential dwelling) ------------------------
    btype = in_window["building_type"].astype("string").str.strip()
    null_btype = btype.isna() | (btype == "")
    if null_btype.any():
        logger.info(
            "%d in-window permits have a null/blank building_type — excluded",
            int(null_btype.sum()),
        )
    unseen_btype = sorted(set(btype[~null_btype].unique()) - KNOWN_BUILDING_TYPES)
    if unseen_btype:
        logger.warning(
            "building_type values not in KNOWN_BUILDING_TYPES — EXCLUDED as "
            "non-residential until reviewed (add to load_permits.py if any is a "
            "dwelling): %s", unseen_btype,
        )
    is_res = btype.isin(RESIDENTIAL_BUILDING_TYPES)

    kept = in_window.loc[is_new & is_res].copy()
    if not len(kept):
        raise ValueError(
            "no new residential permits in the window after filtering — inputs "
            "are wrong or the vocabulary drifted"
        )

    # --- units_added numerator ----------------------------------------------
    units = pd.to_numeric(kept["units_added"], errors="coerce")
    bad_units = units.isna()
    if bad_units.any():
        logger.warning(
            "%d kept permits have a non-numeric units_added — treated as 0 units",
            int(bad_units.sum()),
        )
    kept["units_added"] = units.fillna(0.0)
    logger.info(
        "Kept %d new residential permits, %.0f new dwelling units (window %s)",
        len(kept), kept["units_added"].sum(), years,
    )

    # --- hood normalization + aggregation -----------------------------------
    hood = (
        kept["neighbourhood"].astype("string").str.strip().str.upper()
        .replace(PERMIT_NAME_CORRECTIONS)
    )
    no_hood = hood.isna() | (hood == "")
    if no_hood.any():
        logger.warning(
            "%d kept permits have no neighbourhood — excluded (%.0f units lost)",
            int(no_hood.sum()), kept.loc[no_hood.values, "units_added"].sum(),
        )
    kept = kept.loc[~no_hood.values].copy()
    kept["neighbourhood_name"] = hood.loc[~no_hood].values

    out = (
        kept.groupby("neighbourhood_name", as_index=False)
        .agg(
            new_dwelling_units=("units_added", "sum"),
            new_dwelling_permits=("units_added", "size"),
        )
    )
    logger.info(
        "New-supply activity: %d hoods, %.0f dwelling units citywide (window total)",
        len(out), out["new_dwelling_units"].sum(),
    )
    return out
