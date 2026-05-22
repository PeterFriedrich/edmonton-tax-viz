import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

EXEMPT_CLASS = "NONRES MUNICIPAL/RES EDUCATION"


def load_assessment(csv_path: str | Path) -> pd.DataFrame:
    """Load and clean the property assessment CSV.

    Returns a DataFrame with columns:
        neighbourhood_name  str    normalized (stripped, uppercased)
        assessed_value      float
        is_exempt           bool   True for NONRES MUNICIPAL/RES EDUCATION rows
    """
    df = pd.read_csv(csv_path, low_memory=False)

    df = df.rename(columns={
        "Neighbourhood": "neighbourhood_name",
        "Assessed Value": "assessed_value",
        "Assessment Class 1": "assessment_class_1",
    })

    df["neighbourhood_name"] = df["neighbourhood_name"].str.strip().str.upper()
    df["is_exempt"] = df["assessment_class_1"] == EXEMPT_CLASS

    exempt_count = df["is_exempt"].sum()
    if exempt_count:
        logger.info("Flagged %d tax-exempt rows (Assessment Class 1 == '%s')", exempt_count, EXEMPT_CLASS)

    zero_mask = df["assessed_value"] == 0
    null_mask = df["assessed_value"].isna()
    drop_mask = zero_mask | null_mask
    drop_count = drop_mask.sum()
    if drop_count:
        logger.info("Dropping %d rows with null or zero assessed_value", drop_count)
    df = df[~drop_mask].copy()

    df["assessed_value"] = df["assessed_value"].astype(float)

    return df[["neighbourhood_name", "assessed_value", "is_exempt"]]
