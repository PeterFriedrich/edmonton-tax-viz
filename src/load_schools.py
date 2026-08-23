"""School points for the grid's amenity-distance column (dist_school_m).

Two Socrata datasets, one per board — EPSB `996c-239n` and ECSD `gfxq-u8uu`
(DATA.md §12). They publish INCOMPATIBLE schemas for the same thing, so this
module's whole job is to harmonize them into one point set:

    school_name, board, latitude, longitude

**Only catchment schools count.** Both boards list city-wide and specialized
programs alongside neighbourhood schools — storefront Learning Stores, the
Glenrose Hospital school, Metro Continuing Ed, the Alberta School for the
Deaf, the four CCAC outreach centres. Nobody walks a child to those from the
next block, so including them would put a fake "school nearby" on downtown and
hospital cells. Membership is an EXPLICIT dict per board, never a keyword
heuristic (the ZONE_CATEGORY / ROUTE_MODE philosophy), and an unrecognized
category is KEPT and logged loudly — a new school type must not vanish
silently from the amenity set.

⚠️ **Coverage gap, by source not by choice:** these two boards are all the
open-data portal publishes. Private, charter, and francophone (Conseil
scolaire Centre-Nord) schools are ABSENT, so `dist_school_m` overstates the
distance for a block whose nearest school belongs to one of them. Documented
in DATA.md §12; do not present the column as "distance to the nearest school
in Edmonton".
"""

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

# EPSB `sch_type` -> is this a catchment school? Enumerated 2026-08-23 from the
# live dataset (225 rows): EL 125, EJ 38, JR 26, SR 16, SP 15, EJS 3, JS 2.
# SP is the only False, and its 15 members were read one by one rather than
# trusted by name — they are L. S. (Learning Store) at Blue Quill / Northgate /
# on Whyte / West Edm, Academy King Edward, Institut Serv Schs, Braemar,
# Tevie Miller Hrtg Sc, Glenrose Hospital, Metro Continuing Ed., Aspen Program,
# Rosecrest, L. Y. Cairns, AB School for Deaf, Transitions at the Y: city-wide
# and specialized programs, not neighbourhood catchments.
EPSB_TYPE_IS_CATCHMENT = {
    "EL": True,   # elementary
    "EJ": True,   # elementary + junior high
    "EJS": True,  # elementary + junior + senior
    "JR": True,   # junior high
    "JS": True,   # junior + senior high
    "SR": True,   # senior high
    "SP": False,  # city-wide / specialized program (see above)
}

# ECSD `grade_level` -> is this a catchment school? Enumerated 2026-08-23 from
# the live dataset (97 rows). Outreach's 4 members are the CCAC centres
# (City-Centre, Westmount, Mill Woods, Clareview) — Grade 9-12 outreach
# programs serving the whole city, the ECSD analogue of EPSB's Learning Stores.
ECSD_LEVEL_IS_CATCHMENT = {
    "Elementary": True,
    "Elementary, Junior": True,
    "Elementary, Junior, Senior": True,
    "Junior": True,
    "Junior, Senior": True,
    "Senior": True,
    "Outreach": False,
}

# Edmonton's envelope with room to spare. A lat/long swap or a degrees-vs-DMS
# change upstream lands every point outside this and fails the load — the kind
# of silent geography error a distance column would otherwise absorb into
# plausible-looking metres.
CITY_BBOX = (-114.2, 53.2, -113.0, 53.8)  # (min_lon, min_lat, max_lon, max_lat)


def _catchment_mask(
    values: pd.Series, mapping: dict[str, bool], board: str, field: str
) -> pd.Series:
    """Explicit category -> catchment lookup; unknown categories KEPT + logged."""
    known = values.isin(mapping)
    if not known.all():
        surprises = sorted(set(values[~known].dropna()))
        logger.warning(
            "%s: %d row(s) carry unrecognized %s value(s) %s — KEPT as catchment "
            "schools (no silent drops). Add them to the explicit map in "
            "load_schools if that is wrong.",
            board, int((~known).sum()), field, surprises,
        )
    return values.map(mapping).fillna(True).astype(bool)


def _coords(df: pd.DataFrame, source: str) -> pd.DataFrame:
    """Numeric lat/long with null and out-of-bbox rows reported, never dropped silently."""
    lat = pd.to_numeric(df["latitude"], errors="coerce")
    lon = pd.to_numeric(df["longitude"], errors="coerce")
    bad = lat.isna() | lon.isna()
    if bad.any():
        logger.warning("%s: %d row(s) have null coordinates — dropped", source, int(bad.sum()))
    min_lon, min_lat, max_lon, max_lat = CITY_BBOX
    outside = ~bad & ~(lon.between(min_lon, max_lon) & lat.between(min_lat, max_lat))
    if outside.any():
        raise ValueError(
            f"{source}: {int(outside.sum())} school(s) fall outside the Edmonton "
            f"bbox {CITY_BBOX} — e.g. ({lat[outside].iloc[0]}, {lon[outside].iloc[0]}). "
            "A swapped lat/long or a changed coordinate format, not a real school."
        )
    out = df.loc[~bad].copy()
    out["latitude"] = lat.loc[~bad]
    out["longitude"] = lon.loc[~bad]
    return out


def load_schools(public_csv: str | Path, catholic_csv: str | Path) -> pd.DataFrame:
    """Catchment schools from both boards as one point set.

    Returns ``school_name, board, latitude, longitude`` — one row per school,
    city-wide/specialized programs excluded (and counted in the log). Raises if
    either file is missing a keyed column or if any point falls outside the city.
    """
    epsb = pd.read_csv(public_csv, dtype=str)
    for needed in ("school_nam", "sch_type", "latitude", "longitude"):
        if needed not in epsb.columns:
            raise ValueError(
                f"expected column {needed!r} not in {public_csv} — headers: {list(epsb.columns)}"
            )
    epsb = _coords(epsb, "EPSB")
    epsb_keep = _catchment_mask(epsb["sch_type"], EPSB_TYPE_IS_CATCHMENT, "EPSB", "sch_type")

    ecsd = pd.read_csv(catholic_csv, dtype=str)
    for needed in ("school_name", "grade_level", "latitude", "longitude"):
        if needed not in ecsd.columns:
            raise ValueError(
                f"expected column {needed!r} not in {catholic_csv} — headers: {list(ecsd.columns)}"
            )
    ecsd = _coords(ecsd, "ECSD")
    ecsd_keep = _catchment_mask(ecsd["grade_level"], ECSD_LEVEL_IS_CATCHMENT, "ECSD", "grade_level")

    frames = [
        pd.DataFrame({
            "school_name": epsb.loc[epsb_keep, "school_nam"].astype(str),
            "board": "EPSB",
            "latitude": epsb.loc[epsb_keep, "latitude"],
            "longitude": epsb.loc[epsb_keep, "longitude"],
        }),
        pd.DataFrame({
            "school_name": ecsd.loc[ecsd_keep, "school_name"].astype(str),
            "board": "ECSD",
            "latitude": ecsd.loc[ecsd_keep, "latitude"],
            "longitude": ecsd.loc[ecsd_keep, "longitude"],
        }),
    ]
    schools = pd.concat(frames, ignore_index=True)
    if schools.empty:
        raise ValueError(
            f"no catchment schools left from {public_csv} + {catholic_csv} — "
            "every row was excluded or unusable."
        )
    logger.info(
        "Schools: %d catchment points (EPSB %d of %d, ECSD %d of %d); "
        "%d city-wide/specialized program(s) excluded",
        len(schools), int(epsb_keep.sum()), len(epsb),
        int(ecsd_keep.sum()), len(ecsd),
        int((~epsb_keep).sum() + (~ecsd_keep).sum()),
    )
    return schools
