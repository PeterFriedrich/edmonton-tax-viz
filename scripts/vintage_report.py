"""Monthly vintage & pin digest: what has silently gone stale and needs a human.

The project's automated guards all fire on the WEEKLY refresh, and all of them
are pass/fail gates on work already happening. Nothing tells Peter, unprompted,
that an upstream year has moved or a January pin is due — so the January roll
was discovered by noticing a banner, and the 2026 mill rates (published
2026-04-29) went unnoticed until someone thought to look on 2026-08-06.

This script answers "what needs my attention this month?" in one pass. It is
REPORT-ONLY: it never writes data, never gates the pipeline, and exits 0 even
when it finds action items — the caller (.github/workflows/vintage-digest.yml)
turns the output into a GitHub issue, whose notification is the actual email.

Philosophy borrowed from check_year_alignment.py: a network failure must not
manufacture an alarm. Any check that cannot reach its source reports UNKNOWN and
says so, rather than guessing in either direction.

Statuses:
  OK       nothing to do
  ACTION   a human needs to do something, and the digest says what
  UNKNOWN  could not be determined (network, shape change) — look by hand

Usage:
    python scripts/vintage_report.py              # markdown to stdout
    python scripts/vintage_report.py --json       # machine-readable
"""

import argparse
import datetime as dt
import json
import logging
import os
import re
import sys
from pathlib import Path

import requests

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

MILL_RATES = ROOT / "data" / "mill_rates.json"
STORMWATER_RATES = ROOT / "data" / "stormwater_rates.json"
TEMPORAL_ARCHIVE = ROOT / "data" / "temporal_archive.json"
STATUS_JSON = ROOT / "web" / "data" / "status.json"

ASSESSMENT_METADATA_URL = "https://data.edmonton.ca/api/views/q7d6-ambg.json"
MILL_RATES_URL = "https://data.edmonton.ca/resource/pwis-wc4c.json"

OK, ACTION, UNKNOWN = "OK", "ACTION", "UNKNOWN"


def _rates_years(path):
    return {int(y) for y in json.loads(path.read_text())["rates"]}


def _pins():
    """main.py is the single source of truth for every pinned year."""
    import main  # noqa: PLC0415 — heavy import, only when needed
    return main


def check_assessment_roll(timeout=60):
    """The roll year in Socrata metadata vs the ASSESSMENT_YEAR pin.

    This is the same comparison check_year_alignment.py gates CI on; repeated
    here because the digest's job is to say it BEFORE the banner appears.
    """
    pinned = _pins().ASSESSMENT_YEAR
    try:
        from scripts.check_year_alignment import parse_coverage_year  # noqa: PLC0415
        meta = requests.get(ASSESSMENT_METADATA_URL, timeout=timeout).json()
        detected = parse_coverage_year(meta)
    except Exception as exc:  # noqa: BLE001 — any failure is the same outcome
        return (UNKNOWN, "Assessment roll year",
                f"Could not read Socrata metadata ({exc}). Pin is {pinned}.")
    if detected == pinned:
        return (OK, "Assessment roll year",
                f"Roll is {detected}, pin is {pinned} — aligned.")
    return (ACTION, "Assessment roll year",
            f"**Roll has moved to {detected}, pin is still {pinned}.** The weekly "
            f"refresh is holding and the site is showing a banner. Work "
            f"`docs/RUNBOOK.md` §1 top to bottom.")


def check_mill_rates(timeout=60):
    """Newest published rate year vs what mill_rates.json carries.

    Catches the case that prompted this script: the City publishing next year's
    rates months before the roll, with nothing watching the rate feed itself.
    """
    have = _rates_years(MILL_RATES)
    pinned = _pins().ASSESSMENT_YEAR
    if pinned not in have:
        return (ACTION, "Mill rates",
                f"**`mill_rates.json` has no {pinned} block** but that is the pinned "
                f"year — the pipeline cannot bill. Have: {sorted(have)}.")
    try:
        rows = requests.get(MILL_RATES_URL, params={"$limit": 2000}, timeout=timeout).json()
        published = {int(r["tax_year"]) for r in rows}
    except Exception as exc:  # noqa: BLE001
        return (UNKNOWN, "Mill rates",
                f"Could not read `pwis-wc4c` ({exc}). Local file has {sorted(have)}.")
    # Only the pinned year and NEWER matter. The file deliberately carries no
    # history (the source publishes 2014 onward; we bill one year at a time), so
    # comparing against the full published set reports a decade of false work.
    missing = {y for y in published if y >= pinned} - have
    if missing:
        return (ACTION, "Mill rates",
                f"**{sorted(missing)} published upstream but not in "
                f"`mill_rates.json`** (have {sorted(have)}). Pre-staging is safe — "
                f"rates are year-keyed, so an unpinned year is inert. "
                f"`docs/RUNBOOK.md` §1 step 2.")
    return (OK, "Mill rates",
            f"Nothing published for {pinned} or later is missing locally "
            f"(have {sorted(have)}; pinned year {pinned} present).")


def check_year_constants():
    """generate_status.py's DATA_YEAR/RATE_YEAR are SEPARATE from main.py's pin.

    RUNBOOK §1 step 6 warns that forgetting these makes status.json — and the
    site's vintage display — silently misreport the year. Nothing enforced it.
    """
    pinned = _pins().ASSESSMENT_YEAR
    try:
        from scripts.generate_status import DATA_YEAR, RATE_YEAR  # noqa: PLC0415
    except Exception as exc:  # noqa: BLE001
        return (UNKNOWN, "Year constants", f"Could not import generate_status ({exc}).")
    off = [f"{n}={v}" for n, v in (("DATA_YEAR", DATA_YEAR), ("RATE_YEAR", RATE_YEAR))
           if v != pinned]
    if off:
        return (ACTION, "Year constants",
                f"**{', '.join(off)} disagree with `ASSESSMENT_YEAR`={pinned}** — "
                f"the site would misreport its own vintage. `docs/RUNBOOK.md` §1 step 6.")
    return (OK, "Year constants", f"`DATA_YEAR`/`RATE_YEAR`/`ASSESSMENT_YEAR` all {pinned}.")


def check_stormwater():
    """Stormwater rates are year-keyed and must match the roll, same as mill rates."""
    pinned = _pins().ASSESSMENT_YEAR
    years = {int(y) for y in json.loads(STORMWATER_RATES.read_text())["years"]}
    if pinned in years:
        return (OK, "Stormwater rates", f"Covers pinned year {pinned} (has {sorted(years)}).")
    return (ACTION, "Stormwater rates",
            f"**No {pinned} entry** (has {sorted(years)}). `docs/RUNBOOK.md` §1 step 5.")


def check_window_pins(today=None):
    """FIRE_YEARS / PERMIT_YEARS / PERMIT_YEARS_RECENT vs the last FULL year.

    Pinned deliberately so a partial year is never averaged or summed in, which
    means they need a manual January bump. PERMIT_YEARS_LONG is derived from
    PERMIT_YEARS and needs no check.
    """
    m = _pins()
    today = today or dt.date.today()
    last_full = today.year - 1
    stale = [f"`{n}` ends {w[-1]}" for n, w in (
        ("FIRE_YEARS", m.FIRE_YEARS),
        ("PERMIT_YEARS", m.PERMIT_YEARS),
        ("PERMIT_YEARS_RECENT", m.PERMIT_YEARS_RECENT),
    ) if w[-1] < last_full]
    if not stale:
        return (OK, "Pinned activity windows", f"All end at {last_full}, the last full year.")
    return (ACTION, "Pinned activity windows",
            f"**{last_full} is complete but {'; '.join(stale)}.** Drop the oldest "
            f"year, add {last_full}, all three roll together. `docs/RUNBOOK.md` §1 "
            f"step 4. (The drift guard hard-errors on a stale pin, so this is a "
            f"heads-up, not a silent risk.)")


def check_temporal_archive():
    """The archive must capture the live year BEFORE the roll moves past it.

    refresh.yml captures it automatically every run; this only confirms the
    capture happened, because a year missed in time is unrecoverable (the
    current roll covers exactly one year).
    """
    pinned = _pins().ASSESSMENT_YEAR
    years = {int(y) for y in json.loads(TEMPORAL_ARCHIVE.read_text())["years"]}
    if pinned in years:
        return (OK, "Temporal archive", f"Live year {pinned} captured (has {sorted(years)}).")
    return (ACTION, "Temporal archive",
            f"**Live year {pinned} NOT captured** (has {sorted(years)}). The weekly "
            f"refresh should do this automatically — if it has run since the roll, "
            f"something is wrong. A year missed before the roll is unrecoverable "
            f"(`docs/SPEC_temporal.md` §0).")


def check_banner():
    """A banner left up after its cause is fixed is a live-site correctness issue."""
    banner = json.loads(STATUS_JSON.read_text()).get("banner")
    if not banner:
        return (OK, "Site banner", "No banner showing.")
    return (ACTION, "Site banner",
            f"**A banner is live:** {banner!r} — if its cause is resolved, clear it "
            f"(`python scripts/generate_status.py --clear-banner`, commit, push). "
            f"Banners are preserved across runs by design and will NOT clear "
            f"themselves. `docs/RUNBOOK.md` §1 step 10.")


CHECKS = (
    check_assessment_roll,
    check_mill_rates,
    check_year_constants,
    check_stormwater,
    check_window_pins,
    check_temporal_archive,
    check_banner,
)


def run_all():
    results = []
    for fn in CHECKS:
        try:
            results.append(fn())
        except Exception as exc:  # noqa: BLE001 — one broken check must not kill the digest
            results.append((UNKNOWN, fn.__name__, f"Check raised: {exc!r}"))
    return results


def render(results, today=None):
    today = today or dt.date.today()
    actions = [r for r in results if r[0] == ACTION]
    unknowns = [r for r in results if r[0] == UNKNOWN]

    if actions:
        head = f"**{len(actions)} item(s) need attention.**"
    elif unknowns:
        head = f"Nothing needs attention, but {len(unknowns)} check(s) were inconclusive."
    else:
        head = "**Nothing needs attention.** Every vintage and pin is current."

    icon = {OK: "✅", ACTION: "⚠️", UNKNOWN: "❓"}
    lines = [
        f"Vintage & pin digest — {today.isoformat()}",
        "",
        head,
        "",
        "| | Check | Detail |",
        "|---|---|---|",
    ]
    for status, name, detail in sorted(results, key=lambda r: (r[0] != ACTION, r[0] != UNKNOWN)):
        lines.append(f"| {icon[status]} | **{name}** | {detail} |")
    lines += [
        "",
        "---",
        "*Generated monthly by `.github/workflows/vintage-digest.yml` "
        "(`scripts/vintage_report.py`). Report-only — it changes nothing. "
        "Close this issue once you've acted, or immediately if it's all green.*",
    ]
    return "\n".join(lines), len(actions)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--json", action="store_true", help="machine-readable output")
    p.add_argument("--log-level", default="WARNING")
    args = p.parse_args(argv)
    logging.basicConfig(stream=sys.stderr, level=getattr(logging, args.log_level.upper()))

    results = run_all()
    if args.json:
        print(json.dumps([{"status": s, "check": n, "detail": d} for s, n, d in results], indent=2))
        return 0

    body, n_actions = render(results)
    print(body)

    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        today = dt.date.today().isoformat()
        flag = "⚠️ " if n_actions else "✅ "
        with open(out, "a") as f:
            f.write(f"action_count={n_actions}\n")
            f.write(f"title={flag}Vintage & pin digest — {today}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
