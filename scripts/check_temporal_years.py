"""Temporal-year guard: refuse to publish an assessment year that fails its control.

Phase 0's exit gate (docs/SPEC_temporal.md section 0.3). The temporal lens splices
two sources -- the historical file for 2012-2023, the current roll for the live
year -- because the historical file's 2024 and 2025 slices are missing 2,448
accounts worth $2.93B (audited 2026-07-28). This guard exists because that defect
arrived SILENTLY: the roll simply had fewer rows one year, and nothing downstream
noticed for two publication cycles.

Two classes of check, deliberately separated.

STRUCTURAL (always run, no baseline needed -- these are invariants)
  * ``years``       the published set is exactly ``publishable_years(live_year)``.
                    Asserts the 2024 gap is PRESENT: the omission is a decision,
                    so a contiguous series means someone "fixed" the gap and
                    republished a year we know is incomplete. Also catches the
                    January trap -- once the roll advances past 2025 that year is
                    no longer repairable and must drop out (see load_temporal).
  * ``unique``      no duplicate (hood, year) rows.
  * ``shares``      each year's shares sum to 1.0 -- the conservation check. A
                    hood silently dropped from the numerator shows up here.
  * ``splice``      the live year's rows all come from the current roll, every
                    other year from the historical file, and the live year's
                    account count EXCEEDS the historical file's own copy of it.
                    That last one is the direct control on the splice: the
                    historical copy is the defective one, so if it ever holds
                    more accounts than the roll, the splice is backwards.

ANCHORED (needs data/expected_temporal_years.json)
  Per-year citywide account count and assessed value, in bands.

  Historical years are an ARCHIVE -- 2012-2023 are settled and should not move at
  all. They get a tight band, and a DROP is the dangerous direction, because
  losing accounts from a settled year is precisely the 2024 signature. Growth
  warns and asks for a re-pin (the check_unmatched_names policy).

  The live year is NOT pinned to a band. It is a live snapshot that genuinely
  moves week to week -- 347 Downtown accounts moved between 2026-07-06 and
  2026-07-28 -- and reassessment moves every dollar each January, so a pinned
  band would cry wolf continuously. It is checked structurally instead (``splice``
  above) and against year-over-year growth.

Why not the account-level control here: the exact detector (present in N-1 and in
the current roll, absent from N) needs the 5.5M-row account-level pull and takes
~20 minutes. That is ``tools/audit_historical_roll_gaps.py``, which stays the
instrument of record; re-run it when this guard fires. This guard is the cheap
weekly sentry over the same failure mode.

Outcomes (exit codes; 2 is argparse's):
  0  ok    -- every check passed, or inputs absent (skip).
  5  drift -- a structural invariant broke, or an anchor moved dangerously. FAIL.

Must run BEFORE the status-manifest step in refresh.yml, or a failure bumps the
heartbeat and goes invisible (docs/DECISIONS.md 2026-07-28).

Usage:
    python scripts/check_temporal_years.py
    python scripts/check_temporal_years.py --write-baseline   # re-pin after an understood move
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.load_assessment import load_assessment  # noqa: E402
from src.load_temporal import (  # noqa: E402
    FIRST_YEAR,
    build_temporal_table,
    current_roll_aggregate,
    load_archive,
    load_historical_aggregate,
    publishable_years,
    write_archive,
)

logger = logging.getLogger(__name__)

DEFAULT_HISTORICAL_CSV = ROOT / "data" / "raw" / "assessment_historical_by_hood.csv"
DEFAULT_ASSESSMENT_CSV = ROOT / "data" / "raw" / "Property_Assessment_Data__Current_Calendar_Year_.csv"
DEFAULT_BASELINE = ROOT / "data" / "expected_temporal_years.json"
DEFAULT_ARCHIVE = ROOT / "data" / "temporal_archive.json"

EXIT_OK = 0
EXIT_DRIFT = 5

# Shares are floats summed over ~430 hoods; this is generous for accumulated
# error and far tighter than any real dropped hood.
SHARE_TOLERANCE = 1e-6

# Year-over-year citywide account growth for the live year, as a fraction of the
# previous published year. Measured over 2013-2025: +0.28% (the defect year) to
# +3.71%, and the published series skips 2024 so the live step can span two
# years. The floor is the load-bearing side -- a live year that does not GROW is
# the signature this guard exists for -- and it sits just below the observed
# minimum. The ceiling is loose on purpose: unexpected growth is not a defect.
LIVE_GROWTH_MIN = -0.005
LIVE_GROWTH_MAX = 0.25

# Tight, because a settled historical year should not move at all. Non-zero only
# so a supplementary correction upstream does not red the build over rounding.
HISTORICAL_TOLERANCE = 0.005


def structural_checks(
    table: pd.DataFrame, historical: pd.DataFrame, live_year: int,
    first_year: int = FIRST_YEAR, archived_years=(),
) -> list[str]:
    """Invariants that hold regardless of any baseline. Returns a list of failures."""
    failures = []

    expected = publishable_years(live_year, first_year=first_year, archived_years=archived_years)
    actual = tuple(int(y) for y in sorted(table["year"].unique()))
    if actual != expected:
        missing, extra = set(expected) - set(actual), set(actual) - set(expected)
        detail = []
        if missing:
            detail.append(f"missing {sorted(missing)}")
        if extra:
            detail.append(
                f"UNEXPECTEDLY PRESENT {sorted(extra)} — these years are omitted by "
                f"decision because no complete source covers them; publishing one "
                f"means a known-incomplete year reached the series"
            )
        failures.append(f"years: {'; '.join(detail)} (expected {list(expected)}, got {list(actual)})")

    dupes = table.duplicated(subset=["neighbourhood_name", "year"]).sum()
    if dupes:
        failures.append(f"unique: {dupes} duplicate (hood, year) row(s)")

    for year, grp in table.groupby("year"):
        total = grp["share_of_total_base"].sum()
        if abs(total - 1.0) > SHARE_TOLERANCE:
            failures.append(
                f"shares: {year} shares sum to {total:.9f}, not 1.0 — value left the numerator"
            )

    # The splice, checked from both ends.
    live_rows = table[table["year"] == live_year]
    if live_rows.empty:
        failures.append(f"splice: no rows for the live year {live_year}")
    elif set(live_rows["source"].unique()) != {"current_roll"}:
        failures.append(
            f"splice: live year {live_year} carries source(s) "
            f"{sorted(live_rows['source'].unique())} — it must come from the current roll"
        )
    past = table[table["year"] != live_year]
    if not past.empty and not set(past["source"].unique()) <= {"historical", "archive"}:
        failures.append(
            f"splice: non-live years carry source(s) {sorted(past['source'].unique())}"
        )
    # An archived year must be served FROM the archive. If one falls back to the
    # historical file the capture was lost, which is the January trap arriving.
    for year in sorted(set(archived_years)):
        rows = table[table["year"] == year]
        if not rows.empty and set(rows["source"].unique()) != {"archive"}:
            failures.append(
                f"archive: {year} is archived but is being served from "
                f"{sorted(rows['source'].unique())} — the captured copy is not being used, "
                f"so a defective historical slice may have replaced it"
            )

    hist_live = historical[historical["year"] == live_year]
    if not hist_live.empty and not live_rows.empty:
        roll_n = int(live_rows["n_accounts"].sum())
        hist_n = int(hist_live["n_accounts"].sum())
        if roll_n <= hist_n:
            failures.append(
                f"splice: the current roll holds {roll_n:,} accounts for {live_year} but the "
                f"historical file holds {hist_n:,}. The historical copy is the DEFECTIVE one, "
                f"so it should hold fewer — the splice may be the wrong way round, or the "
                f"upstream defect has been fixed (verify with tools/audit_historical_roll_gaps.py)"
            )

    return failures


def year_anchors(table: pd.DataFrame) -> dict[str, dict[str, float]]:
    """Citywide account count and assessed value per year — what the baseline pins."""
    agg = table.groupby("year").agg(
        n_accounts=("n_accounts", "sum"),
        total_assessed_value=("total_assessed_value", "sum"),
    )
    return {
        str(int(year)): {
            "n_accounts": float(row["n_accounts"]),
            "total_assessed_value": float(row["total_assessed_value"]),
        }
        for year, row in agg.iterrows()
    }


def compare_years(
    live: dict[str, dict[str, float]], baseline: dict, live_year: int
) -> tuple[str, list[str], list[str]]:
    """Compare per-year anchors to the committed bands.

    Returns ``(result, dangerous, benign)``. A settled historical year LOSING
    accounts or value is the dangerous direction; gaining warns only.
    """
    dangerous, benign = [], []
    pinned = baseline.get("years", {})
    for year, vals in sorted(live.items()):
        if int(year) == live_year:
            continue  # not pinned — see the module docstring
        band = pinned.get(year)
        if band is None:
            benign.append(f"{year}: not pinned — add it with --write-baseline")
            continue
        for metric, value in vals.items():
            lo, hi = float(band[metric]["min"]), float(band[metric]["max"])
            if value < lo:
                dangerous.append(
                    f"{year}.{metric}: {value:,.0f} below band {lo:,.0f}-{hi:,.0f} "
                    f"— a settled year LOST {(1 - value / lo) * 100:.2f}% or more"
                )
            elif value > hi:
                benign.append(
                    f"{year}.{metric}: {value:,.0f} above band {lo:,.0f}-{hi:,.0f} (grew)"
                )
    return ("drift" if dangerous else "ok"), dangerous, benign


def check_live_growth(table: pd.DataFrame, live_year: int) -> list[str]:
    """The live year must grow against the previous PUBLISHED year, not shrink."""
    years = sorted(int(y) for y in table["year"].unique())
    prior = [y for y in years if y < live_year]
    if not prior:
        return []
    prev = prior[-1]
    by_year = table.groupby("year")["n_accounts"].sum()
    a, b = float(by_year[prev]), float(by_year[live_year])
    if a <= 0:
        return []
    growth = (b - a) / a
    if not (LIVE_GROWTH_MIN <= growth <= LIVE_GROWTH_MAX):
        return [
            f"live-growth: {prev} -> {live_year} accounts moved {growth * 100:+.2f}% "
            f"({a:,.0f} -> {b:,.0f}), outside {LIVE_GROWTH_MIN * 100:+.1f}%.."
            f"{LIVE_GROWTH_MAX * 100:+.1f}%. A live year that does not grow is the "
            f"dropout signature — check tools/audit_historical_roll_gaps.py"
        ]
    logger.info(
        "  live-growth              %+.2f%% (%d -> %d accounts, %d -> %d)",
        growth * 100, prev, live_year, int(a), int(b),
    )
    return []


def _write_github_output(**kv: object) -> None:
    out = os.environ.get("GITHUB_OUTPUT")
    if not out:
        return
    with open(out, "a") as f:
        for k, v in kv.items():
            f.write(f"{k}={v}\n")


def _band(value: float, tol: float) -> dict[str, float]:
    span = abs(value) * tol
    return {"min": round(max(0.0, value - span), 2), "max": round(value + span, 2)}


def _capture_measures_as(current: pd.DataFrame, live_year: int) -> bool:
    """Does THIS capture measure as ``live_year``, or does it only inherit the pin?

    Guards `write_archive`'s one irreversible act. Measures the frame about to be
    written -- not the CSV, not a pin, not Socrata's coverage string -- against
    Alberta's FIR filings, and reuses `check_roll_year_against_fir`'s own
    `detect_year` rather than comparing here, so this and the standalone guard
    can never disagree about what a mislabelled year is (the S122 lesson: a
    duplicated comparison is a bypassed decision).

    ⚠️ FALSE MEANS UNPROVEN, NOT WRONG, and during the annual FIR lag it is the
    ordinary answer -- Alberta files months after Edmonton rolls, so a correctly
    pinned January capture is unprovable until the filing lands. That is why an
    unconfirmed capture is still written; see `write_archive`.
    """
    try:
        sys.path.insert(0, str(ROOT / "scripts"))
        from check_roll_year_against_fir import (  # noqa: PLC0415
            FIR_TAX_BASE,
            detect_year,
            filed_bases,
        )
        from check_temporal_archive_year import RESIDENTIAL_CLASS  # noqa: PLC0415

        if not FIR_TAX_BASE.exists():
            logger.warning("Archive year UNPROVEN: no %s to measure against.", FIR_TAX_BASE)
            return False
        live = current[current["year"] == live_year]
        ours = float(live[live["mill_class"] == RESIDENTIAL_CLASS]["assessed_value"].sum())
        detected, residuals = detect_year(ours, filed_bases(FIR_TAX_BASE))
    except Exception as exc:  # noqa: BLE001 — unprovable for any reason is the same answer
        logger.warning("Archive year UNPROVEN: could not measure it (%s).", exc)
        return False

    if detected == live_year:
        logger.info("Archive year CONFIRMED: the capture measures as %d "
                    "(residual %+.2f%%).", live_year, residuals[live_year] * 100)
        return True
    if detected is None:
        logger.warning(
            "Archive year UNPROVEN: no FIR year fits the capture within tolerance "
            "(residuals %s). Expected during the FIR lag; the capture is still "
            "written, but it cannot overwrite a confirmed year.",
            {y: f"{r:+.2%}" for y, r in sorted(residuals.items())},
        )
        return False
    logger.error(
        "Archive year MEASURES AS %d BUT THE PIN SAYS %d. The roll has almost "
        "certainly moved past the pin -- bump ASSESSMENT_YEAR (docs/RUNBOOK.md "
        "section 1). Residuals %s.",
        detected, live_year, {y: f"{r:+.2%}" for y, r in sorted(residuals.items())},
    )
    return False


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--historical-csv", type=Path, default=DEFAULT_HISTORICAL_CSV)
    p.add_argument("--assessment-csv", type=Path, default=DEFAULT_ASSESSMENT_CSV)
    p.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE)
    p.add_argument(
        "--live-year", type=int, default=None,
        help="assessment year of the current roll (default: main.ASSESSMENT_YEAR)",
    )
    p.add_argument("--archive", type=Path, default=DEFAULT_ARCHIVE)
    p.add_argument("--write-baseline", action="store_true")
    p.add_argument(
        "--write-archive", action="store_true",
        help="capture the live year into the archive (previously-archived years "
             "are frozen). ⚠️ CI OWNS THIS — running it locally re-captures from "
             "whatever roll snapshot is in data/raw/, so a stale local CSV "
             "COMMITS A DOWNGRADED ARCHIVE. Check `git diff` before staging.",
    )
    p.add_argument(
        "--tolerance", type=float, default=HISTORICAL_TOLERANCE,
        help=f"band half-width for historical years (default {HISTORICAL_TOLERANCE})",
    )
    p.add_argument("--log-level", default="INFO")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(
        stream=sys.stdout,
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(levelname)s: %(message)s",
    )

    # Missing inputs SKIP rather than fail — the same policy as
    # check_value_anchors: the pipeline degrades deliberately when an input is
    # absent, and a guard must not invent a hard failure the pipeline avoided.
    for path, what in ((args.historical_csv, "historical aggregate"),
                       (args.assessment_csv, "assessment CSV")):
        if not path.exists():
            logger.warning(
                "SKIPPING temporal-year guard — %s not found (%s). Fetch it with "
                "scripts/download_data.py --only assessment_historical.", what, path,
            )
            _write_github_output(result="skipped")
            return EXIT_OK

    live_year = args.live_year
    if live_year is None:
        import main as pipeline  # noqa: PLC0415 — only to read the pinned year
        live_year = pipeline.ASSESSMENT_YEAR

    historical = load_historical_aggregate(args.historical_csv)
    current = current_roll_aggregate(load_assessment(args.assessment_csv), live_year)

    if args.write_archive:
        write_archive(args.archive, current, live_year,
                      confirmed=_capture_measures_as(current, live_year))

    archive = load_archive(args.archive)
    table, stats = build_temporal_table(historical, current, live_year, archive=archive)

    live = year_anchors(table)

    if args.write_baseline:
        payload = {
            "_note": (
                "Per-year citywide anchors for the temporal lens "
                "(scripts/check_temporal_years.py). Historical years are an archive and "
                "should not move; the LIVE year is deliberately absent from this file "
                "because it is a live snapshot that moves weekly. See "
                "docs/SPEC_temporal.md section 0.3."
            ),
            "live_year_when_pinned": live_year,
            "years": {
                y: {k: _band(v, args.tolerance) for k, v in vals.items()}
                for y, vals in live.items() if int(y) != live_year
            },
        }
        args.baseline.write_text(json.dumps(payload, indent=2) + "\n")
        logger.info(
            "Wrote baseline %s: %d historical year(s) pinned at +/-%.1f%% "
            "(live year %d deliberately unpinned)",
            args.baseline, len(payload["years"]), args.tolerance * 100, live_year,
        )
        return EXIT_OK

    failures = structural_checks(
        table, historical, live_year, archived_years=stats["archived_years"]
    )
    failures += check_live_growth(table, live_year)

    if args.baseline.exists():
        baseline = json.loads(args.baseline.read_text())
        result, dangerous, benign = compare_years(live, baseline, live_year)
        failures += dangerous
        for msg in benign:
            logger.warning("  %s", msg)
    else:
        logger.warning(
            "  no baseline at %s — structural checks only. Create it with "
            "--write-baseline.", args.baseline,
        )

    if failures:
        logger.error(
            "TEMPORAL-YEAR DRIFT — %d check(s) failed:\n%s\n"
            "Do NOT re-pin the baseline until the cause is understood. The published "
            "year set and the 2024 omission are DECISIONS (docs/DECISIONS.md "
            "2026-07-28), not defaults; re-run tools/audit_historical_roll_gaps.py "
            "before changing either.",
            len(failures), "\n".join(f"  - {f}" for f in failures),
        )
        _write_github_output(result="drift", failures=str(len(failures)))
        return EXIT_DRIFT

    logger.info(
        "Temporal-year guard OK: %d year(s) %s, %d hoods, live year %d from the current roll"
        "%s.",
        len(stats["years"]), list(stats["years"]), stats["hoods"], live_year,
        f", {len(stats['archived_years'])} from the archive {list(stats['archived_years'])}"
        if stats["archived_years"] else "",
    )
    _write_github_output(result="ok")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
