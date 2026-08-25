"""Detect the assessment roll's year FROM THE DATA, and check it against the pin.

⚠️ WHY THIS EXISTS. ``check_year_alignment.py`` decides the roll year by parsing
Socrata's ``Period of Coverage`` metadata string. Edmonton left that string
reading ``"2025-01-01 to 2025-12-31"`` for the whole 2026 roll, so on 2026-08-25
every guard was green while the pipeline billed a **2026 roll at 2025 mill
rates** — understating citywide levy by ~$69.5M. A guard that reads a
publisher's free-text field is not measuring the data (TODO.md, 2026-08-25).

THE DETECTOR. Residential land is barely exempt anywhere, so our residential
taxable base should sit within a couple of percent of what Edmonton FILED with
Alberta (FIR Schedule ``MR(2)``, ``data/fir_tax_base.json``). Consecutive years
are ~10% apart, so the residual is sharp:

    our residential base $162,273,056,185 vs the filed base
        2023  +23.6%      2025   +9.5%
        2024  +20.7%      2026   +1.2%   <- the roll

The best-fitting year is the roll year. This reads the parcels, so no metadata
claim can hide a roll that moved.

⚠️ It does NOT verify the whole model — only which YEAR the roll is. The
residual against the correct year is expected to be small but non-zero
(exemptions we bill, apportionment we don't model); that is a separate open
question, not this check's business.

Exit codes:  0 ok / skipped   3 year mismatch (the hold state)   4 inconclusive

When ``GITHUB_OUTPUT`` is set (CI), writes ``result=``, ``detected_year=``,
``pinned_year=`` and ``banner=`` for the workflow steps to branch on — the same
contract as ``check_year_alignment.py``, so refresh.yml can gate on either.

Usage:
    .venv/bin/python scripts/check_roll_year_against_fir.py
    .venv/bin/python scripts/check_roll_year_against_fir.py --expected-year 2026
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

logger = logging.getLogger(__name__)

FIR_TAX_BASE = ROOT / "data" / "fir_tax_base.json"
ASSESSMENT_CSV = ROOT / "data" / "raw" / "Property_Assessment_Data__Current_Calendar_Year_.csv"

# Our residential base may exceed the filed one (we bill some property the City
# exempts) but should never fall far below it, and a correct year is an order of
# magnitude closer than its neighbours. A best fit worse than this means
# something other than a year shift is wrong — report inconclusive, don't guess.
MAX_PLAUSIBLE_RESIDUAL = 0.05   # 5%
MIN_SEPARATION = 0.03           # best fit must beat the runner-up by this much

EXIT_OK = 0
EXIT_HOLD = 3
EXIT_INCONCLUSIVE = 4


def _write_github_output(**kv: object) -> None:
    """Expose results to the workflow when running under GitHub Actions."""
    out = os.environ.get("GITHUB_OUTPUT")
    if not out:
        return
    with open(out, "a") as f:
        for k, v in kv.items():
            f.write(f"{k}={v}\n")


def our_residential_base(csv_path: Path = ASSESSMENT_CSV) -> float:
    """Percentage-apportioned RESIDENTIAL assessment across all class slices."""
    from apply_tax_rates import CLASS_SLOTS  # noqa: PLC0415 — heavy import
    from load_assessment import load_assessment  # noqa: PLC0415

    df = load_assessment(str(csv_path))
    total = 0.0
    for label_col, pct_col in CLASS_SLOTS:
        slice_ = df[df[label_col] == "RESIDENTIAL"]
        total += float((slice_["assessed_value"] * slice_[pct_col].fillna(0) / 100).sum())
    return total


def filed_bases(path: Path = FIR_TAX_BASE) -> dict[int, float]:
    data = json.loads(path.read_text())
    return {
        int(y): rec["assessment"]["residential"]
        for y, rec in data["years"].items()
        if rec["assessment"].get("residential")
    }


def detect_year(ours: float, filed: dict[int, float]) -> tuple[int | None, dict[int, float]]:
    """Return (best-fit year or None, {year: signed residual})."""
    residuals = {y: ours / base - 1 for y, base in filed.items()}
    ranked = sorted(residuals, key=lambda y: abs(residuals[y]))
    best = ranked[0]
    if abs(residuals[best]) > MAX_PLAUSIBLE_RESIDUAL:
        return None, residuals
    if len(ranked) > 1 and abs(residuals[ranked[1]]) - abs(residuals[best]) < MIN_SEPARATION:
        return None, residuals
    return best, residuals


def main(argv=None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--expected-year", type=int,
                   help="override the pin (default: main.py ASSESSMENT_YEAR)")
    p.add_argument("--assessment-csv", type=Path, default=ASSESSMENT_CSV)
    p.add_argument("--fir-tax-base", type=Path, default=FIR_TAX_BASE)
    args = p.parse_args(argv)

    if not args.assessment_csv.exists():
        logger.info("SKIPPED: no local roll at %s (nothing to measure)", args.assessment_csv)
        _write_github_output(result="skipped")
        return EXIT_OK
    if not args.fir_tax_base.exists():
        logger.warning("SKIPPED: no %s — run scripts/fetch_fir_tax_base.py",
                       args.fir_tax_base)
        _write_github_output(result="skipped")
        return EXIT_OK

    pinned = args.expected_year
    if pinned is None:
        import main as pipeline  # noqa: PLC0415 — heavy import, only when needed
        pinned = pipeline.ASSESSMENT_YEAR

    filed = filed_bases(args.fir_tax_base)
    ours = our_residential_base(args.assessment_csv)
    detected, residuals = detect_year(ours, filed)

    logger.info("our residential taxable base: $%s", f"{ours:,.0f}")
    for year in sorted(residuals):
        mark = " <-- best fit" if year == detected else ""
        logger.info("  vs FIR %d: $%s  %+.1f%%%s",
                    year, f"{filed[year]:,.0f}", 100 * residuals[year], mark)

    if detected is None:
        logger.warning(
            "INCONCLUSIVE — no year fits within %.0f%% with %.0f%% separation. "
            "Either the roll moved beyond data/fir_tax_base.json (re-run "
            "scripts/fetch_fir_tax_base.py) or something other than the year is wrong.",
            100 * MAX_PLAUSIBLE_RESIDUAL, 100 * MIN_SEPARATION)
        _write_github_output(result="inconclusive", pinned_year=pinned)
        return EXIT_INCONCLUSIVE

    if detected != pinned:
        logger.error(
            "YEAR MISMATCH — the roll measures as %d but ASSESSMENT_YEAR is %d. "
            "The pipeline is billing a %d roll at %d mill rates. "
            "Work docs/RUNBOOK.md §1 (the January year roll).",
            detected, pinned, detected, pinned)
        # Visitor-facing wording, same contract as check_year_alignment.py's
        # holding banner. It does NOT promise the detected year's rates exist —
        # this guard measures the roll, and says nothing about the rate table.
        banner = (
            f"Showing {pinned} data — the assessment roll now measures as "
            f"{detected}. The map updates automatically once {detected} "
            f"municipal tax rates are incorporated."
        )
        _write_github_output(result="hold", detected_year=detected,
                             pinned_year=pinned, banner=banner)
        return EXIT_HOLD

    logger.info("Roll-year guard OK: roll measures as %d, pin is %d — aligned "
                "(residual %+.1f%%).", detected, pinned, 100 * residuals[detected])
    _write_github_output(result="ok", detected_year=detected, pinned_year=pinned)
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
