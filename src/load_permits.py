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

import json
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

# building_type values counted as INDUSTRIAL (SPEC_industrial.md A3) — the
# City's 400-series codes, enumerated by FULL STRING like the residential set
# (codes duplicate across unrelated types: Parkade shares (490) with
# Engineering; Mixed Use / Office Complex share (522)).
# Commercial (5xx) and institutional (6xx) stay out — this is the industrial
# permit-velocity cut, not a non-residential catch-all.
#
# ⚠️ **Two 400-series types were REMOVED 2026-08-18 because they are not
# industrial in this data**, found when the 100 m grid drew a $91.2M spike on
# DOWNTOWN (measured by `job_description`, 2009–2026):
#   Engineering (490)            95% parkades ($189.3M of $202.1M; $10.5M else)
#   Transportation Terminals (440)  100% LRT/transit ($326.1M LRT stations,
#                                   pedways, platforms + $33.4M parkade)
# ⚠️ **The full-string rule did not protect against this, and the comment above
# shows why we thought it would**: it assumed one physical thing carries one
# label, but the City files underground parkades under BOTH `Parkade (490)` and
# `Engineering (490)`. Excluding the obvious string left the same buildings in
# under the other one. **Enumerating by string only helps if the strings
# partition the things — check what is actually IN a category, not just that
# its name sounds right.**
# The kept types are clean: Warehouses (58% of the metric's dollars) and
# Manufacturing measure 0% parkade/LRT. 450 and 480 retain some LRT
# maintenance/utility facilities (30% / 24% of their own dollars) — those are
# genuine industrial operations and stay in; the 2026-08-18 decision names them.
INDUSTRIAL_BUILDING_TYPES = frozenset({
    "Animal and Plant Services (410)",
    "Manufacturing Buildings (430)",
    "Maintenance Buildings incl Hangars (450)",
    "Storage Buildings, Warehouses (460)",
    "Communication Buildings (470)",
    "Utility Buildings (480)",
})

# Removed from INDUSTRIAL above but still part of the KNOWN vocabulary — they
# are real building_type values, so they must not trip the warn-on-unseen guard.
NON_INDUSTRIAL_400_SERIES = frozenset({
    "Transportation Terminals (440)",
    "Engineering (490)",
})

# Full building_type vocabulary observed 2026-07-12 — the residential +
# industrial sets above UNION the remaining codes below. Anything absent from
# this union is UNSEEN: logged loudly, treated as excluded until reviewed (it
# could be a new residential variant that should be counted).
KNOWN_BUILDING_TYPES = RESIDENTIAL_BUILDING_TYPES | INDUSTRIAL_BUILDING_TYPES | \
        NON_INDUSTRIAL_400_SERIES | frozenset({
    "Carport (090)",
    "Clinics, Health Units (642)",
    "Convention Centres (536)", "Day Cares, Nursing Homes (650)",
    "Detached Deck (020)", "Detached Garage (010)", "Detached Greenhouse (030)",
    "Detached Misc. Structure (090)", "Detached Shed (040)",
    "Elementary Schools (620)", "Funeral Homes (590)",
    "Gazebo (090)", "Government Legislative/Admin (610)", "Greenhouse (030)",
    "Hoarding (910)", "Hospitals (640)", "Hotels (530)",
    "Indoor Recreational Buildings (560)", "Laboratory/Research Centres (580)",
    "Law Enforcement/Emergency Svcs. (612)", "Libraries/Museums/Art Galleries (630)",
    "Malls, Office/Retail (512)",
    "Mixed Use (522)", "Motels (532)",
    "Office Buildings (520)", "Office Complex (522)",
    "Other Accommodation (534)", "Other Accomodation (534)",
    "Outdoor Recreational Buildings (562)", "Parkade (490)", "Play Structure (090)",
    "Post-secondary Institutions (624)", "Religious Buildings (660)",
    "Restaurants and Bars (540)", "Retail and Shops (510)", "Retail - Motor Vehicle (570)",
    "Secondary Schools (622)", "Service Stations, Repair Garages (572)", "Shed (040)",
    "Temporary Structure (099)",
    "Temporary Structures (999)", "Theatre and Performing Arts Ctrs (550)",
    "Universities (626)",
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
        ind_permits           int    new-construction ∩ INDUSTRIAL permit count
                                     (SPEC_industrial.md A3 — count only;
                                     units_added is meaningless for industrial)

    A hood absent from the result had zero new residential AND industrial
    permits in the window; a hood with one kind but not the other carries a
    true 0 in the other column — join_and_calculate fills the true 0 for
    absent hoods (roads/fire semantics).
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
    is_ind = btype.isin(INDUSTRIAL_BUILDING_TYPES)

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

    # --- industrial permit velocity (SPEC_industrial.md A3) -----------------
    # Same new-construction work_type set, industrial building types, COUNT
    # only. Aggregated separately (the residential filter above excludes these
    # rows) and outer-merged: a hood with one kind of activity but not the
    # other carries a true 0 in the missing column.
    ind = in_window.loc[is_new & is_ind].copy()
    ind_hood = (
        ind["neighbourhood"].astype("string").str.strip().str.upper()
        .replace(PERMIT_NAME_CORRECTIONS)
    )
    ind_no_hood = ind_hood.isna() | (ind_hood == "")
    if ind_no_hood.any():
        logger.warning(
            "%d kept industrial permits have no neighbourhood — excluded",
            int(ind_no_hood.sum()),
        )
    ind = ind.loc[~ind_no_hood.values].copy()
    ind["neighbourhood_name"] = ind_hood.loc[~ind_no_hood].values
    ind_out = (
        ind.groupby("neighbourhood_name", as_index=False)
        .agg(ind_permits=("neighbourhood_name", "size"))
    )
    logger.info(
        "Kept %d new industrial permits across %d hoods (window %s)",
        int(ind_out["ind_permits"].sum()) if len(ind_out) else 0, len(ind_out), years,
    )
    out = out.merge(ind_out, on="neighbourhood_name", how="outer")
    for col in ("new_dwelling_units", "new_dwelling_permits", "ind_permits"):
        out[col] = out[col].fillna(0.0)

    logger.info(
        "New-supply activity: %d hoods, %.0f dwelling units citywide (window total)",
        len(out), out["new_dwelling_units"].sum(),
    )
    return out


DEFAULT_PRICE_INDEX = Path(__file__).resolve().parents[1] / "data" / \
    "construction_price_index.json"


def _load_deflators(path: str | Path | None) -> tuple[dict[int, float], int]:
    """Load the construction-price deflator table (year -> factor, base year).

    Produced by ``scripts/fetch_construction_price_index.py`` — a manual,
    reviewed input, deliberately NOT on the weekly refresh. Missing file is
    fatal: silently exporting nominal dollars is the failure this exists to
    prevent, and it would look identical on the map.
    """
    path = Path(path) if path else DEFAULT_PRICE_INDEX
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found — run scripts/fetch_construction_price_index.py. "
            f"The industrial grid's dollars are meaningless without it (a 2009 "
            f"permit is 1.72x understated against a 2025 one)."
        )
    payload = json.loads(path.read_text(encoding="utf-8"))
    try:
        deflators = {int(y): float(v) for y, v in payload["deflators"].items()}
        base_year = int(payload["base_year"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"{path} is not a deflator table ({exc})") from exc
    if deflators.get(base_year) != 1.0:
        raise ValueError(
            f"{path}: base year {base_year} has factor "
            f"{deflators.get(base_year)}, expected exactly 1.0 — the table was "
            f"rebased inconsistently"
        )
    return deflators, base_year


def export_dev_grid(
    permits_csv: str | Path,
    out_path: str | Path,
    years: tuple[int, ...],
    years_recent: tuple[int, ...] | None = None,
    years_long: tuple[int, ...] | None = None,
    cell_m: float = 100.0,
    price_index_path: str | Path | None = None,
) -> dict:
    """100 m grid of new construction — the Development view's detail layer.

    Bins GEOCODED new-construction permits into ``cell_m`` squares on the same
    EPSG:3400 grid as ``export_value_grid`` (Glass view), so the detail layers
    share cell geometry. Residential cells carry dwelling units and permit
    counts; industrial cells carry **deflated construction value** and a permit
    count. Emits compact flat JSON::

        { "cell_m": 100.0,
          "crs_note": "...",
          "columns": ["lon", "lat", "units", "permits", "ind_cv", "ind_n", ...],
          "cells": [[lon, lat, u, p, cv, n, ...], ...],  # lon/lat = cell SW corner
          "coverage": { "5yr": {"units": ..., "units_geocoded": ...,
                                "permits": ..., "permits_geocoded": ...,
                                "ind_permits": ..., "ind_permits_geocoded": ...,
                                "ind_value": ..., "ind_value_geocoded": ...,
                                "ind_permits_zero_value": ...},
                        "3yr": {...} } }

    **Why industrial is measured in dollars.** Industrial has no ``units_added``
    analogue, and permit COUNT alone does not form a surface at this resolution:
    measured 2026-08-18, 89% of 5yr industrial cells hold exactly one permit and
    the tallest holds ten, so a count-driven grid is a dot map wearing a density
    map's clothes. Declared construction value spreads those same cells over
    191x (5yr max/median), which is what makes the height carry information.
    Enlarging the cell does NOT fix the count problem — 100 m to 400 m is a 16x
    area increase that removes 19 of 184 cells (SPEC_industrial.md A3).

    ⚠️ **The dollars are a DECLARED ESTIMATE at permit application**, not audited
    spend and not investment: land is excluded, the permit fee is derived from
    the figure, and 78% of values end in ``000``. They are deflated to constant
    dollars here (``price_index_path``, default
    ``data/construction_price_index.json``) because nominal sums encode
    construction-cost inflation as development — an identical building permitted
    in 2009 would otherwise draw a spike 1.72x shorter than a 2025 one. A permit
    year with no deflator HARD-FAILS rather than passing through at nominal.

    ⚠️ **Zero-value industrial permits are counted, never dropped.** 13 of 1,314
    industrial permits are declared at exactly $0 (118 at <=$10k), which on a
    dollar-driven height would render as a zero-height cell — a building that
    silently vanishes from the map. ``ind_n`` ships alongside ``ind_cv`` so the
    client can floor those cells to a visible height; the count of them is
    reported per window in ``coverage``.

    The ``_3yr`` / ``_long`` columns appear only when ``years_recent`` /
    ``years_long`` are given (mirroring the hood columns' suffix convention).
    **Geocode coverage is reported, not silent**: permits without
    latitude/longitude — a geocoding lag concentrated in the NEWEST permits
    (DATA.md §10: 2009–2023 sit at 95–98% geocoded, 2025 at ~72%) — are excluded
    from the cells but counted in ``coverage`` so the web blurb can disclose the
    gap. The long window is therefore BETTER-geocoded on average than 3yr (which
    is dominated by the newest, laggiest years). Vocabulary
    drift warnings (unseen work/building types) are load_permits' job — the
    weekly pipeline runs both on the same file; this filter stays quiet.
    """
    from pyproj import Transformer

    out_path = Path(out_path)
    windows = {"5yr": tuple(sorted(years))}
    if years_recent:
        windows["3yr"] = tuple(sorted(years_recent))
    if years_long:
        windows["long"] = tuple(sorted(years_long))

    header = pd.read_csv(permits_csv, nrows=0)
    needed = set(REQUIRED_COLUMNS) | {"latitude", "longitude", "construction_value"}
    missing = sorted(needed - set(header.columns))
    if missing:
        raise ValueError(
            f"columns {missing} not in {permits_csv} — the permits CSV predates "
            f"the lat/long (2026-07-15) or construction_value (2026-08-18) "
            f"$select (scripts/download_data.py); re-download before exporting "
            f"the dev grid"
        )

    deflators, base_year = _load_deflators(price_index_path)

    df = pd.read_csv(permits_csv, usecols=sorted(needed), low_memory=False)
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["units_added"] = pd.to_numeric(df["units_added"], errors="coerce").fillna(0.0)
    df["construction_value"] = pd.to_numeric(
        df["construction_value"], errors="coerce").fillna(0.0)
    is_new = df["work_type"].astype("string").str.strip().isin(NEW_WORK_TYPES)
    btype = df["building_type"].astype("string").str.strip()
    is_res = btype.isin(RESIDENTIAL_BUILDING_TYPES)
    is_ind = btype.isin(INDUSTRIAL_BUILDING_TYPES)
    lat = pd.to_numeric(df["latitude"], errors="coerce")
    lon = pd.to_numeric(df["longitude"], errors="coerce")
    geocoded = lat.notna() & lon.notna()

    all_years = sorted({y for w in windows.values() for y in w})
    in_range = is_new & df["year"].isin(all_years)
    kept = df.loc[in_range & is_res].copy()
    kept_ind = df.loc[in_range & is_ind].copy()
    if not len(kept):
        raise ValueError(
            f"no new residential permits in {all_years} — wrong input or "
            f"vocabulary drift (load_permits would have warned)"
        )
    if not len(kept_ind):
        # NOT fatal, deliberately: industrial is the secondary metric, and
        # hard-failing here would withhold the whole grid — including the
        # residential cells — and silently hide the Detail toggle. The empty
        # columns still ship; `coverage[*].ind_permits == 0` is what the client
        # gates the Industrial option on, so it hides rather than drawing a
        # blank map.
        logger.warning(
            "No new industrial permits in %s — the industrial detail grid will "
            "be EMPTY. Expect ~285 in a 5yr window; check for building_type "
            "vocabulary drift (INDUSTRIAL_BUILDING_TYPES).", all_years,
        )

    # Deflate to constant dollars BEFORE any summing: a cell aggregates permits
    # from different years, so nominal addition would mix price levels inside a
    # single number. A missing year is fatal — see the docstring.
    missing_years = sorted({int(y) for y in kept_ind["year"].dropna().unique()}
                           - set(deflators))
    if missing_years:
        raise ValueError(
            f"no construction-price deflator for permit years {missing_years} "
            f"(have {min(deflators)}–{max(deflators)}). Re-run "
            f"scripts/fetch_construction_price_index.py; do NOT let those "
            f"permits through at nominal value."
        )
    kept_ind["cv_real"] = (kept_ind["construction_value"]
                           * kept_ind["year"].map(deflators).astype(float))

    coverage = {}
    for name, w in windows.items():
        in_w = kept["year"].isin(w)
        geo = in_w & geocoded.loc[kept.index]
        in_wi = kept_ind["year"].isin(w)
        geo_i = in_wi & geocoded.loc[kept_ind.index]
        coverage[name] = {
            "units": round(float(kept.loc[in_w, "units_added"].sum())),
            "units_geocoded": round(float(kept.loc[geo, "units_added"].sum())),
            "permits": int(in_w.sum()),
            "permits_geocoded": int(geo.sum()),
            "ind_permits": int(in_wi.sum()),
            "ind_permits_geocoded": int(geo_i.sum()),
            "ind_value": round(float(kept_ind.loc[in_wi, "cv_real"].sum())),
            "ind_value_geocoded": round(float(kept_ind.loc[geo_i, "cv_real"].sum())),
            # Declared at $0 — real permits the dollar height cannot show on its
            # own. The client floors them; this is how many it is flooring.
            "ind_permits_zero_value": int(
                (kept_ind.loc[geo_i, "construction_value"] <= 0).sum()),
        }
        logger.info(
            "Dev grid %s window: %d of %d permits geocoded (%.0f of %.0f units) "
            "— the gap is the recent-permit geocoding lag, disclosed in-app",
            name, coverage[name]["permits_geocoded"], coverage[name]["permits"],
            coverage[name]["units_geocoded"], coverage[name]["units"],
        )
        logger.info(
            "Dev grid %s industrial: %d of %d permits geocoded ($%.1fM of $%.1fM "
            "in %d dollars); %d geocoded permits declared $0",
            name, coverage[name]["ind_permits_geocoded"], coverage[name]["ind_permits"],
            coverage[name]["ind_value_geocoded"] / 1e6, coverage[name]["ind_value"] / 1e6,
            base_year, coverage[name]["ind_permits_zero_value"],
        )

    pts = kept.loc[geocoded.loc[kept.index]].copy()
    pts_ind = kept_ind.loc[geocoded.loc[kept_ind.index]].copy()
    # Same projection + floor-binning as export_value_grid, so a dev-grid cell
    # and a value-grid cell with equal corners are the SAME 100 m square.
    to_alberta = Transformer.from_crs(4326, 3400, always_xy=True)
    for frame in (pts, pts_ind):
        x, y = to_alberta.transform(frame["longitude"].values, frame["latitude"].values)
        frame["cx"] = (x // cell_m).astype(int)
        frame["cy"] = (y // cell_m).astype(int)

    per_cell, per_cell_ind = {}, {}
    for name, w in windows.items():
        g = (pts.loc[pts["year"].isin(w)]
             .groupby(["cx", "cy"])
             .agg(units=("units_added", "sum"), permits=("units_added", "size")))
        per_cell[name] = g[g["units"] + g["permits"] > 0]
        # Industrial keeps every cell with a PERMIT, including the $0 ones —
        # the count is what stops a zero-dollar building disappearing.
        gi = (pts_ind.loc[pts_ind["year"].isin(w)]
              .groupby(["cx", "cy"])
              .agg(ind_cv=("cv_real", "sum"), ind_n=("cv_real", "size")))
        per_cell_ind[name] = gi[gi["ind_n"] > 0]
    # A cell is emitted if ANY window has activity there, residential OR
    # industrial (long-only cells — active 2009–2020 but not in the 5yr window —
    # carry 0 in the shorter windows, which the client's `c[col] > 0` filter
    # drops when they're viewed).
    cells_idx = per_cell["5yr"].index.union(per_cell_ind["5yr"].index)
    for name in ("3yr", "long"):
        if name in per_cell:
            cells_idx = cells_idx.union(per_cell[name].index)
            cells_idx = cells_idx.union(per_cell_ind[name].index)

    to_wgs84 = Transformer.from_crs(3400, 4326, always_xy=True)
    SUFFIX = {"5yr": "", "3yr": "_3yr", "long": "_long"}
    columns = ["lon", "lat"]
    for name in windows:
        s = SUFFIX[name]
        columns += [f"units{s}", f"permits{s}", f"ind_cv{s}", f"ind_n{s}"]
    rows = []
    for cx, cy in cells_idx:
        lon_sw, lat_sw = to_wgs84.transform(cx * cell_m, cy * cell_m)
        row = [round(lon_sw, 6), round(lat_sw, 6)]
        for name in windows:
            if (cx, cy) in per_cell[name].index:
                rec = per_cell[name].loc[(cx, cy)]
                row += [round(float(rec["units"])), int(rec["permits"])]
            else:
                row += [0, 0]
            if (cx, cy) in per_cell_ind[name].index:
                rec = per_cell_ind[name].loc[(cx, cy)]
                row += [round(float(rec["ind_cv"])), int(rec["ind_n"])]
            else:
                row += [0, 0]
        rows.append(row)

    payload = {
        "cell_m": cell_m,
        "crs_note": "cells binned in EPSG:3400; SW corners reprojected to WGS84",
        # The blurb reads the basis from the FILE, so the disclosure cannot go
        # stale against the dollars it describes (the geocode-coverage idiom).
        "ind_value_note": {
            "basis": f"constant {base_year} dollars",
            "base_year": base_year,
            # Short enough to print in the blurb and still findable. The full
            # dimension detail (series, vector, units) lives in
            # data/construction_price_index.json, which is where provenance
            # belongs — the blurb already runs long.
            "deflator": "StatCan table 18-10-0289 (Edmonton, industrial)",
            "oldest_factor": round(max(deflators[y] for y in all_years
                                       if y in deflators), 3),
            "meaning": "declared estimate of construction work at permit "
                       "application — excludes land, not audited spend",
        },
        "columns": columns,
        "cells": rows,
        "coverage": coverage,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, separators=(",", ":"))

    stats = {"n_cells": len(rows), "cell_m": cell_m,
             "coverage": coverage, "bytes": out_path.stat().st_size}
    logger.info("Wrote %s: %d cells, %.2f MB",
                out_path.name, len(rows), stats["bytes"] / 1e6)
    return stats
