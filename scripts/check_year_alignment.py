"""Year-alignment guard: verify the assessment roll year still matches the pin.

The single unguarded silent-integrity risk found by the data-integrity audit
(docs/FINDINGS_data_integrity_audit.md §3): the assessment feed (`q7d6-ambg`,
"Current Calendar Year") carries NO year column — the roll vintage lives only in
Socrata metadata. When Edmonton rolls the feed to a new year, an unguarded
weekly refresh would keep applying the pinned mill rates to the new roll:
every revenue number wrong, nothing crashing.

This script runs in CI between download and regeneration (refresh.yml) and
compares three things:
  1. the roll year in the live Socrata metadata
     (``custom_fields."Time Frame"."Period of Coverage"`` — see DATA.md §1),
  2. the pinned ``ASSESSMENT_YEAR`` (main.py — the single source of truth),
  3. the years present in ``data/mill_rates.json``.

Outcomes (exit codes chosen for the workflow to branch on; 2 is argparse's):
  0  aligned      — metadata year == pin, and the pin has published rates.
                    Proceed with regeneration.
  3  hold         — metadata year != pin (or the pin has no rates). Per
                    SPEC_deployment "Year alignment": do NOT regenerate a
                    mismatched-year map. Keep serving the last committed data,
                    set the maintenance banner, alert. Graceful, not a crash.
  4  inconclusive — metadata could not be fetched/parsed. Proceed as aligned
                    (the guard must not add fragility the pipeline never had),
                    but warn.

When ``GITHUB_OUTPUT`` is set (CI), writes ``result=``, ``detected_year=``,
``pinned_year=`` and ``banner=`` for the workflow steps to branch on.

Usage:
    python scripts/check_year_alignment.py                      # live metadata
    python scripts/check_year_alignment.py --metadata-file m.json --expected-year 2025
"""

import argparse
import json
import logging
import os
import re
import sys
from datetime import date
from pathlib import Path

import requests

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent
MILL_RATES_JSON = ROOT / "data" / "mill_rates.json"

# Socrata dataset metadata for the assessment feed (q7d6-ambg).
METADATA_URL = "https://data.edmonton.ca/api/views/q7d6-ambg.json"

EXIT_ALIGNED = 0
EXIT_HOLD = 3
EXIT_INCONCLUSIVE = 4


def parse_coverage_year(metadata: dict) -> int:
    """Extract the roll year from Socrata metadata's Period of Coverage.

    The field reads like ``"2025-01-01 to 2025-12-31"``. The START year is the
    roll year. If start and end years ever differ, that's a new metadata shape —
    raise rather than guess (the caller treats parse failures as inconclusive).
    """
    coverage = metadata["metadata"]["custom_fields"]["Time Frame"]["Period of Coverage"]
    years = re.findall(r"\b(20\d{2})\b", coverage)
    if not years:
        raise ValueError(f"No year found in Period of Coverage: {coverage!r}")
    if len(set(years)) > 1:
        raise ValueError(f"Period of Coverage spans multiple years: {coverage!r}")
    return int(years[0])


def check_alignment(detected: int, pinned: int, rate_years: set[str]) -> tuple[str, str]:
    """Compare detected roll year vs the pin vs available rates.

    Returns ``(result, message)`` where result is ``"aligned"`` or ``"hold"``.
    On hold, message is the visitor-facing banner text (SPEC_deployment
    "Year alignment" holding-window wording).
    """
    # ⚠️ `detected` comes from Socrata's hand-maintained "Period of Coverage"
    # string, and Edmonton left it reading 2025 for the whole 2026 roll — so
    # "detected == pinned" agreed with itself while both were a year stale and
    # the pipeline billed a 2026 roll at 2025 rates (TODO.md 2026-08-25). A
    # coverage year older than the current calendar year now means the string
    # is untrustworthy, NOT that the roll is aligned. The authoritative check
    # measures the parcels: scripts/check_roll_year_against_fir.py.
    if detected < date.today().year:
        return "stale-metadata", (
            f"Socrata reports the roll as {detected} but it is {date.today().year} — "
            f"'Period of Coverage' is not maintained and cannot be trusted. "
            f"Run scripts/check_roll_year_against_fir.py, which measures the roll."
        )

    if detected == pinned and str(pinned) in rate_years:
        return "aligned", f"Assessment roll {detected} matches pinned rates {pinned}."

    if detected == pinned:
        # Pin matches the roll but mill_rates.json lost/never had that year —
        # a config error, not a roll. Still a hold: can't compute revenue.
        return "hold", (
            f"Map data is temporarily not refreshing: {pinned} mill rates are "
            f"missing from the rate table. The current map remains correct."
        )

    if str(detected) in rate_years:
        return "hold", (
            f"Showing {pinned} data — the {detected} assessment roll is published "
            f"and {detected} rates are available; the update is pending review. "
            f"The map will refresh once it lands."
        )
    return "hold", (
        f"Showing {pinned} data — the {detected} assessment roll is published but "
        f"Edmonton's {detected} municipal tax rates aren't incorporated yet. "
        f"The map updates automatically once they are."
    )


def _load_rate_years(rates_path: Path) -> set[str]:
    with open(rates_path) as f:
        return set(json.load(f)["rates"])


def _resolve_pinned_year() -> int:
    """Default pin = main.py's ASSESSMENT_YEAR (the single source of truth)."""
    sys.path.insert(0, str(ROOT))
    from main import ASSESSMENT_YEAR  # noqa: PLC0415 — heavy import, only when needed
    return ASSESSMENT_YEAR


def _write_github_output(**kv: object) -> None:
    """Expose results to the workflow when running under GitHub Actions."""
    out = os.environ.get("GITHUB_OUTPUT")
    if not out:
        return
    with open(out, "a") as f:
        for k, v in kv.items():
            f.write(f"{k}={v}\n")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--metadata-url", default=METADATA_URL)
    p.add_argument("--metadata-file", type=Path, help="read metadata from a local JSON file instead of fetching")
    p.add_argument("--expected-year", type=int, help="override the pin (default: main.py ASSESSMENT_YEAR)")
    p.add_argument("--rates-json", type=Path, default=MILL_RATES_JSON)
    p.add_argument("--timeout", type=int, default=60)
    p.add_argument("--log-level", default="INFO")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(
        stream=sys.stdout,
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(levelname)s: %(message)s",
    )

    pinned = args.expected_year if args.expected_year is not None else _resolve_pinned_year()
    rate_years = _load_rate_years(args.rates_json)

    try:
        if args.metadata_file:
            metadata = json.loads(args.metadata_file.read_text())
        else:
            r = requests.get(args.metadata_url, timeout=args.timeout)
            r.raise_for_status()
            metadata = r.json()
        detected = parse_coverage_year(metadata)
    except Exception as exc:  # noqa: BLE001 — any fetch/parse failure is the same outcome
        logger.warning("Year-alignment check INCONCLUSIVE (%s) — proceeding as aligned", exc)
        _write_github_output(result="inconclusive", pinned_year=pinned)
        return EXIT_INCONCLUSIVE

    result, message = check_alignment(detected, pinned, rate_years)
    if result == "stale-metadata":
        # Deliberately INCONCLUSIVE, not HOLD: the metadata is untrustworthy, so
        # we know nothing about the roll — and a hold would raise a banner on a
        # guess. check_roll_year_against_fir.py is the one that can answer.
        logger.warning("Year-alignment check INCONCLUSIVE — %s", message)
        _write_github_output(result="inconclusive", detected_year=detected, pinned_year=pinned)
        return EXIT_INCONCLUSIVE

    if result == "aligned":
        logger.info("Year alignment OK: %s", message)
        _write_github_output(result="aligned", detected_year=detected, pinned_year=pinned)
        return EXIT_ALIGNED

    logger.error(
        "YEAR MISMATCH (detected roll %s vs pinned %s; rates for: %s) — HOLD: "
        "do not regenerate; keep serving committed data; banner: %s",
        detected, pinned, sorted(rate_years), message,
    )
    _write_github_output(result="hold", detected_year=detected, pinned_year=pinned, banner=message)
    return EXIT_HOLD


if __name__ == "__main__":
    sys.exit(main())
