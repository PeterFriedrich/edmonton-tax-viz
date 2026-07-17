"""Load the property-info CSV (dkk9-cj3x) for the lot-size join.

Slim by design: the pipeline needs three columns from this dataset, all keyed
by ``account_number`` for the join to the assessment roll (100% coverage,
verified 2026-07-04):
  - ``lot_size`` — parcel area in m², city-supplied (DATA.md §2).
  - ``gross_area`` — building floor area in m² (source ``Total Gross Area``);
    the numerator of the Development Lens B built floor-area ratio (FAR =
    Σ floor area / Σ deduped lot area, the "underused / room to add"
    suitability proxy — docs/SPEC_development.md Lens B). ~6% null/zero.
  - ``year_built`` — construction year; feeds the Development view's
    stock-age spikes (median year built per 100 m cell,
    ``export_value_grid``). ~4.8% null; 1881–2026 and junk-free in the
    current data (probed 2026-07-17), with a plausibility window here so
    future junk nulls out loudly instead of skewing a cell median.
Other columns stay out until something needs them (ANALYSIS_BACKLOG 4).

``lot_size`` semantics are inconsistent at multi-unit points (duplicated /
apportioned / null — DATA.md §2); this module does NOT resolve that. It only
normalizes the fields (numeric, non-positive → null) and reports null counts.
The dedupe heuristic lives with its consumer in ``export_value_grid.py``
(docs/FINDINGS_lot_dedupe.md); ``gross_area`` is summed per unit there (each
condo unit carries its own floor area — no dedupe on the numerator).
"""

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

# Plausibility window for year_built: outside it the value is junk (a typo'd
# roll entry), not a building — nulled and counted, never silently kept.
# Edmonton's oldest surviving stock is 1880s; the top allows next-year
# completions on a current-year roll.
YEAR_BUILT_MIN = 1850
YEAR_BUILT_MAX = 2100


def load_property_info(csv_path: str | Path) -> pd.DataFrame:
    """Load account → lot size + floor area + year built from the property-info CSV.

    Returns a DataFrame with columns:
        account_number   int
        lot_size         float  parcel area in m²; NaN where null or <= 0
        gross_area       float  building floor area in m²; NaN where null or <= 0
        year_built       float  construction year; NaN where null or implausible
                                (outside [YEAR_BUILT_MIN, YEAR_BUILT_MAX])

    No silent drops: null/non-positive/implausible values are kept as NaN and
    counted.
    """
    df = pd.read_csv(
        csv_path,
        usecols=["Account Number", "lot_size", "Total Gross Area", "year_built"],
        low_memory=False,
    )
    df = df.rename(columns={
        "Account Number": "account_number", "Total Gross Area": "gross_area",
    })

    for col in ("lot_size", "gross_area"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].where(df[col] > 0)

    df["year_built"] = pd.to_numeric(df["year_built"], errors="coerce")
    implausible = df["year_built"].notna() & ~df["year_built"].between(
        YEAR_BUILT_MIN, YEAR_BUILT_MAX
    )
    if implausible.any():
        logger.warning(
            "%d year_built values outside [%d, %d] nulled (examples: %s)",
            implausible.sum(), YEAR_BUILT_MIN, YEAR_BUILT_MAX,
            df.loc[implausible, "year_built"].head(5).tolist(),
        )
    df["year_built"] = df["year_built"].where(~implausible)

    dupes = df["account_number"].duplicated().sum()
    if dupes:
        raise ValueError(
            f"{dupes} duplicated account numbers in {csv_path} — "
            "the account->lot_size join key is no longer unique"
        )

    logger.info(
        "Loaded %d property-info rows: %d null lot_size, %d null gross_area, "
        "%d null year_built",
        len(df), df["lot_size"].isna().sum(), df["gross_area"].isna().sum(),
        df["year_built"].isna().sum(),
    )
    return df
