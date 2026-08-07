"""Neighbourhood -> city ward lookup, from the property-info roll.

Ward is an **attribute column on the property-info CSV**, not a boundary layer:
there is no polygon to ingest and no spatial join to run. Each parcel carries
its ward name, and every neighbourhood sits in exactly one ward, so the lookup
is a groupby — see ``load_wards`` for the invariant that enforces this.

Names are the post-2021 redistricting set (``Metis``, ``O-day'min``,
``papastew``, ``pihesiwin``, ...), which is why this cannot be joined to any
pre-2021 ward geography.
"""

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

# Not a ward. A single hood (GLENRIDDING RAVINE) carries two ward names in one
# comma-joined string upstream. It is kept verbatim rather than split or
# guessed -- splitting would invent a parcel-to-ward assignment the source does
# not make -- but it must never be presented as a ward, so it is named here and
# reported by load_wards.
COMPOUND_WARD_VALUES = {"pihêsiwin, Ipiihkoohkanipiaohtsi"}


def load_wards(csv_path: str | Path) -> pd.DataFrame:
    """Load the neighbourhood -> ward lookup from the property-info CSV.

    Returns a DataFrame with one row per neighbourhood:

        neighbourhood_name  str  ALL CAPS, as in the assessment/boundary data
        ward                str  ward name; NaN where the source has none

    ⚠️ **Raises if any neighbourhood spans more than one ward.** The 1:1
    relation is what makes a ward rollup a regroup of neighbourhood-level
    results rather than a re-aggregation from parcels; if it ever breaks, every
    ward figure downstream becomes a double count and the caller must be told
    rather than silently handed a mode.

    No silent drops: neighbourhoods whose ward is absent upstream are returned
    with a NaN ward and counted, and compound values are reported.
    """
    df = pd.read_csv(
        csv_path,
        usecols=["Neighbourhood", "Ward"],
        dtype=str,
        low_memory=False,
    )

    missing_hood = df["Neighbourhood"].isna().sum()
    if missing_hood:
        logger.warning(
            "%d property-info rows have no neighbourhood — no ward can be "
            "derived for them", missing_hood,
        )
    df = df.dropna(subset=["Neighbourhood"])

    wards_per_hood = df.groupby("Neighbourhood")["Ward"].agg(
        lambda s: sorted(s.dropna().unique())
    )

    split = {h: w for h, w in wards_per_hood.items() if len(w) > 1}
    if split:
        raise ValueError(
            f"{len(split)} neighbourhood(s) span multiple wards, so a ward "
            f"rollup would double-count them: {split} — the 1:1 "
            "neighbourhood->ward assumption in load_wards no longer holds"
        )

    out = pd.DataFrame({
        "neighbourhood_name": wards_per_hood.index,
        "ward": [w[0] if w else pd.NA for w in wards_per_hood],
    }).reset_index(drop=True)

    no_ward = sorted(out.loc[out["ward"].isna(), "neighbourhood_name"])
    if no_ward:
        logger.warning(
            "%d neighbourhood(s) have no ward in the source and are excluded "
            "from any ward rollup: %s", len(no_ward), no_ward,
        )

    compound = sorted(out.loc[out["ward"].isin(COMPOUND_WARD_VALUES),
                              "neighbourhood_name"])
    if compound:
        logger.warning(
            "%d neighbourhood(s) carry a compound ward value that is NOT a "
            "single ward and must not be reported as one: %s",
            len(compound), compound,
        )

    # Counted excluding COMPOUND_WARD_VALUES: including them would report 13
    # wards for a 12-ward city.
    real_wards = out.loc[~out["ward"].isin(COMPOUND_WARD_VALUES), "ward"]
    logger.info(
        "Loaded ward lookup: %d neighbourhoods, %d wards, %d without a ward, "
        "%d compound", len(out), real_wards.dropna().nunique(), len(no_ward),
        len(compound),
    )
    return out
