"""Check every year in the temporal archive against the year it is FILED UNDER.

⚠️ WHY THIS EXISTS. ``src/load_temporal.write_archive`` captures the live
assessment roll under whatever year ``main.ASSESSMENT_YEAR`` says, and the
entry then FREEZES — by design, because once the roll advances we no longer
hold a complete source for that year. That freeze is only a safety feature if
the label was right when it was written.

On **2026-07-28** it was not. Edmonton's Socrata ``Period of Coverage`` string
still read ``"2025-01-01 to 2025-12-31"`` while the roll had already advanced to
2026, ``check_year_alignment.py`` compared our pin against that string and
called them aligned, and the archive froze the **2026 roll under the label
2025**. Both entries then measure the same roll four weeks apart:

    archive "2025" RESIDENTIAL $162,255,323,500  -> best FIR fit 2026 (+1.17%)
    archive  2026  RESIDENTIAL $162,264,409,000  -> best FIR fit 2026 (+1.18%)

The true 2025 is 8.3% lower (FIR 2025 residential $148.1B; the historical table
totals $220.07B against the archive's $238.39B). See ``docs/DATA_ISSUES.md``.

``check_roll_year_against_fir.py`` now prevents a repeat — ``refresh.yml`` gates
``python main.py`` on it, so the archive can no longer be written under a stale
pin. This check covers the other half: **the entries already frozen**, which
that guard never looks at and which the freeze rule forbids rewriting.

THE DETECTOR is the same one, one level down. The archive stores per hood x
mill class, and its ``RESIDENTIAL`` total is the same quantity
``check_roll_year_against_fir.our_residential_base()`` computes from the
parcels — within 0.01% on the live year. So each archived year should best-fit
ITS OWN year in Alberta FIR Schedule MR(2); consecutive years are ~10% apart,
so a mislabel is unmissable.

⚠️ It checks the LABEL, not the contents. An archived year that fits its own
FIR year is the right roll; whether that roll is internally complete is a
different question (``scripts/check_temporal_years.py`` owns the anchors).

⚠️ A year outside ``data/fir_tax_base.json``'s range is UNCHECKABLE, not
passing — it is reported as skipped and named, because a silent pass on an
unverifiable year is exactly the shape of failure this file exists to catch.

Exit codes:  0 ok / skipped   3 a year is filed under the wrong label
             4 inconclusive (no year fits, or two fit equally well)

Usage:
    .venv/bin/python scripts/check_temporal_archive_year.py
    .venv/bin/python scripts/check_temporal_archive_year.py --archive path.json
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
sys.path.insert(0, str(ROOT / "scripts"))

from check_roll_year_against_fir import (  # noqa: E402
    EXIT_HOLD,
    EXIT_INCONCLUSIVE,
    EXIT_OK,
    detect_year,
    filed_bases,
)

logger = logging.getLogger(__name__)

FIR_TAX_BASE = ROOT / "data" / "fir_tax_base.json"
TEMPORAL_ARCHIVE = ROOT / "data" / "temporal_archive.json"

# The archive's mill-class key whose total is comparable to FIR's filed
# residential base. ⚠️ NOT "OTHER RESIDENTIAL" as well: adding it overshoots the
# filed base by ~15% and would make every year look inconclusive. Measured, not
# assumed — RESIDENTIAL alone reproduces the parcel-level guard to 0.01%.
RESIDENTIAL_CLASS = "RESIDENTIAL"


def _write_github_output(**kv: object) -> None:
    """Expose results to the workflow when running under GitHub Actions."""
    out = os.environ.get("GITHUB_OUTPUT")
    if not out:
        return
    with open(out, "a") as f:
        for k, v in kv.items():
            f.write(f"{k}={v}\n")


def archived_residential_bases(path: Path = TEMPORAL_ARCHIVE) -> dict[int, float]:
    """{year: RESIDENTIAL assessment} for every year in the archive."""
    payload = json.loads(Path(path).read_text())
    out: dict[int, float] = {}
    for year, hoods in payload.get("years", {}).items():
        out[int(year)] = sum(
            value
            for classes in hoods.values()
            for cls, (_count, value) in classes.items()
            if cls == RESIDENTIAL_CLASS
        )
    return out


def main(argv=None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--archive", type=Path, default=TEMPORAL_ARCHIVE)
    p.add_argument("--fir-tax-base", type=Path, default=FIR_TAX_BASE)
    args = p.parse_args(argv)

    if not args.archive.exists():
        logger.info("SKIPPED: no archive at %s (nothing to check)", args.archive)
        _write_github_output(result="skipped")
        return EXIT_OK
    if not args.fir_tax_base.exists():
        logger.warning("SKIPPED: no %s — run scripts/fetch_fir_tax_base.py",
                       args.fir_tax_base)
        _write_github_output(result="skipped")
        return EXIT_OK

    filed = filed_bases(args.fir_tax_base)
    ours = archived_residential_bases(args.archive)
    if not ours:
        logger.info("SKIPPED: the archive holds no years")
        _write_github_output(result="skipped")
        return EXIT_OK

    mismatched: list[tuple[int, int]] = []
    inconclusive: list[int] = []
    unchecked: list[int] = []

    for year in sorted(ours):
        base = ours[year]
        if year not in filed:
            unchecked.append(year)
            logger.warning(
                "  archive %d: $%s — NOT CHECKED, %d is outside "
                "data/fir_tax_base.json (%d–%d). Re-run scripts/fetch_fir_tax_base.py.",
                year, f"{base:,.0f}", year, min(filed), max(filed))
            continue
        detected, residuals = detect_year(base, filed)
        detail = "  ".join(
            f"{y}:{100 * residuals[y]:+.1f}%" for y in sorted(residuals))
        if detected is None:
            inconclusive.append(year)
            logger.warning("  archive %d: $%s — INCONCLUSIVE (%s)",
                           year, f"{base:,.0f}", detail)
        elif detected != year:
            mismatched.append((year, detected))
            logger.error("  archive %d: $%s — MEASURES AS %d (%s)",
                         year, f"{base:,.0f}", detected, detail)
        else:
            logger.info("  archive %d: $%s — ok, measures as %d (%+.1f%%)",
                        year, f"{base:,.0f}", detected, 100 * residuals[detected])

    _write_github_output(
        result=("hold" if mismatched else "inconclusive" if inconclusive else "ok"),
        checked=len(ours) - len(unchecked),
        mismatched=",".join(str(y) for y, _ in mismatched),
    )

    if mismatched:
        for filed_as, measures_as in mismatched:
            logger.error(
                "ARCHIVE YEAR MISLABELLED — the entry filed as %d measures as the "
                "%d roll. The archive is frozen by design "
                "(src/load_temporal.write_archive), so this needs a decision, not "
                "a rewrite: see docs/DATA_ISSUES.md.", filed_as, measures_as)
        return EXIT_HOLD
    if inconclusive:
        logger.warning(
            "INCONCLUSIVE for %s — no FIR year fits within tolerance. Either the "
            "archive holds a year FIR has not published yet, or something other "
            "than the label is wrong.",
            ", ".join(str(y) for y in inconclusive))
        return EXIT_INCONCLUSIVE

    logger.info("Archive-year guard OK: %d of %d archived year(s) measure as the "
                "year they are filed under.", len(ours) - len(unchecked), len(ours))
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
