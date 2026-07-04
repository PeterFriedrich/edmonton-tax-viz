"""Loader for the Property Info dataset (``dkk9-cj3x`` — DATA.md §2).

Currently exposes only ``lot_size`` (the grid export's footprint-spreading
input); the diversity-analysis columns (``year_built`` etc.) can extend this
module when that work starts.
"""

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def load_lot_sizes(csv_path: str | Path) -> pd.DataFrame:
    """Load per-account lot sizes from the Property Info CSV.

    Returns a DataFrame with columns:
        account_number   int    join key to the assessment roll
        lot_size_m2      float  city-provided lot area, sq metres (NaN kept —
                                ~0.6% of rows; DATA.md §2)

    CAUTION (DATA.md §2): at multi-unit points ``lot_size`` is inconsistently
    duplicated / apportioned / null across units. It is safe as a per-row
    footprint hint (export_value_grid spreads each row's value over its own
    lot square) but NOT safe to sum across units as a land denominator.
    """
    df = pd.read_csv(
        csv_path, low_memory=False, usecols=["Account Number", "lot_size"]
    ).rename(columns={"Account Number": "account_number", "lot_size": "lot_size_m2"})
    df["lot_size_m2"] = pd.to_numeric(df["lot_size_m2"], errors="coerce")

    nulls = df["lot_size_m2"].isna().sum()
    logger.info(
        "Loaded %d lot sizes (%d null/non-numeric — kept as NaN)", len(df), nulls
    )
    return df
