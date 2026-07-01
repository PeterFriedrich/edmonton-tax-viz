"""Compute per-property municipal tax levy from class apportionment + mill rates.

Independently runnable processing step (project rule). Bridges the two class
vocabularies in the assessment file (see docs/FINDINGS_assessment_classes.md):
the split-class label columns use ``COMMERCIAL`` etc., while ``mill_rates.json``
is keyed by the clean ``Tax Class`` vocabulary. Rates are loaded from the JSON
config keyed by year + class — never hardcoded.

Levy formula (per property, summed over its up-to-3 class slices):

    levy = assessed_value × Σ_slot  (pct_slot / 100) × (rate[class_slot] / 1000)

Exempt slices (``NONRES MUNICIPAL/RES EDUCATION``) carry no rate → contribute
$0, so exempt-only parcels compute to a $0 levy naturally.
"""

import json
import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

# Sentinel label flagged tax-exempt on load; carries no mill rate ($0 levy).
EXEMPT_LABEL = "NONRES MUNICIPAL/RES EDUCATION"

# Assessment Class N label → mill-rate-table class key (the Tax Class vocabulary
# used in mill_rates.json). None = exempt → $0. This map is exhaustive for the
# current snapshot; an unmapped label that appears is a hard error (below) so a
# future re-download introducing a new class can't be silently billed at $0.
ASSESSMENT_CLASS_TO_RATE_CLASS = {
    "RESIDENTIAL": "Residential",
    "COMMERCIAL": "Non Residential",
    "OTHER RESIDENTIAL": "Other Residential",
    "FARMLAND": "Farmland",
    "MA DERELICT RESIDENTIAL": "Non Residential",
    EXEMPT_LABEL: None,
}

# (label column, percentage column) for each of the up-to-3 class slices.
CLASS_SLOTS = [
    ("assessment_class_1", "assessment_class_pct_1"),
    ("assessment_class_2", "assessment_class_pct_2"),
    ("assessment_class_3", "assessment_class_pct_3"),
]


def load_mill_rates(rates_path: str | Path, year: int | str, rate_type: str = "municipal") -> dict[str, float]:
    """Return ``{rate_class: rate_per_1000}`` for ``year`` from mill_rates.json.

    Only classes that publish ``rate_type`` are included (e.g. 2025 Farmland has
    municipal but no education rate).
    """
    with open(rates_path) as f:
        data = json.load(f)
    year = str(year)
    if year not in data["rates"]:
        raise KeyError(f"No mill rates for year {year} in {rates_path} (have: {sorted(data['rates'])})")
    return {cls: vals[rate_type] for cls, vals in data["rates"][year].items() if rate_type in vals}


def _build_label_rate_lookup(df: pd.DataFrame, rates: dict[str, float], year: str) -> dict[str, float]:
    """Map every assessment-class label PRESENT in the data to its rate per $1,000.

    Validates up front: an unmapped label, or a mapped rate-class missing from the
    year's published rates, raises rather than billing silently at $0.
    """
    present: set[str] = set()
    for cls_col, _ in CLASS_SLOTS:
        present |= set(df[cls_col].dropna().unique())

    unknown = present - set(ASSESSMENT_CLASS_TO_RATE_CLASS)
    if unknown:
        raise KeyError(
            f"Unmapped assessment class label(s): {sorted(unknown)} — "
            "update ASSESSMENT_CLASS_TO_RATE_CLASS in apply_tax_rates.py"
        )

    lookup: dict[str, float] = {}
    for label in present:
        rate_class = ASSESSMENT_CLASS_TO_RATE_CLASS[label]
        if rate_class is None:
            lookup[label] = 0.0  # exempt
        elif rate_class not in rates:
            raise KeyError(f"Rate class {rate_class!r} (from label {label!r}) missing from {year} mill rates")
        else:
            lookup[label] = rates[rate_class]
    return lookup


def apply_tax_rates(
    df: pd.DataFrame,
    rates_path: str | Path,
    year: int | str,
    rate_type: str = "municipal",
) -> pd.DataFrame:
    """Add a per-property ``levy`` column (municipal tax) to the assessment frame.

    Expects the class columns carried through by load_assessment.py
    (``tax_class``, ``assessment_class_1/2/3``, ``assessment_class_pct_1/2/3``).
    Returns a copy with ``levy`` (float, dollars) appended.
    """
    rates = load_mill_rates(rates_path, year, rate_type)
    label_rate = _build_label_rate_lookup(df, rates, str(year))

    df = df.copy()
    levy = pd.Series(0.0, index=df.index)
    pct_total = pd.Series(0.0, index=df.index)

    for cls_col, pct_col in CLASS_SLOTS:
        slot_rate = df[cls_col].map(label_rate).fillna(0.0)  # NaN label (empty slot) → 0
        pct = pd.to_numeric(df[pct_col], errors="coerce").fillna(0.0)
        levy += df["assessed_value"] * (pct / 100.0) * (slot_rate / 1000.0)
        pct_total += pct

    # Source rounding leaves a few rows whose class %s sum to <100. Bill as-stated
    # (do NOT normalize — that would invent which class the missing % belongs to);
    # flag rather than silently adjust.
    off = (pct_total - 100.0).abs() > 0.01
    if off.any():
        logger.warning(
            "%d propert(ies) with class %% not summing to 100 — billed as-stated, not normalized",
            int(off.sum()),
        )

    df["levy"] = levy
    logger.info(
        "Computed %s levy for %d properties (year %s); total $%s",
        rate_type, len(df), year, f"{float(levy.sum()):,.0f}",
    )
    return df
