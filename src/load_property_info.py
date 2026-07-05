"""Load the property-info CSV (dkk9-cj3x) for the lot-size join.

Slim by design: the only column the pipeline needs from this dataset today is
``lot_size`` (parcel area in m², city-supplied — DATA.md §2), keyed by
``account_number`` for the join to the assessment roll (100% coverage,
verified 2026-07-04). ``year_built`` etc. stay out until the diversity
analysis needs them (ANALYSIS_BACKLOG 4).

``lot_size`` semantics are inconsistent at multi-unit points (duplicated /
apportioned / null — DATA.md §2); this module does NOT resolve that. It only
normalizes the field (numeric, non-positive → null) and reports null counts.
The dedupe heuristic lives with its consumer in ``export_value_grid.py``
(docs/FINDINGS_lot_dedupe.md).
"""

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def load_property_info(csv_path: str | Path) -> pd.DataFrame:
    """Load account → lot size from the property-info CSV.

    Returns a DataFrame with columns:
        account_number   int
        lot_size         float  parcel area in m²; NaN where null or <= 0

    No silent drops: null/non-positive lot sizes are kept as NaN and counted.
    """
    df = pd.read_csv(
        csv_path, usecols=["Account Number", "lot_size"], low_memory=False,
    )
    df = df.rename(columns={"Account Number": "account_number"})

    df["lot_size"] = pd.to_numeric(df["lot_size"], errors="coerce")
    nonpositive = (df["lot_size"] <= 0).sum()
    df["lot_size"] = df["lot_size"].where(df["lot_size"] > 0)

    dupes = df["account_number"].duplicated().sum()
    if dupes:
        raise ValueError(
            f"{dupes} duplicated account numbers in {csv_path} — "
            "the account->lot_size join key is no longer unique"
        )

    logger.info(
        "Loaded %d property-info rows: %d null lot_size (%d of those non-positive)",
        len(df), df["lot_size"].isna().sum(), nonpositive,
    )
    return df
