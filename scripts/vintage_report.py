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
import csv
import datetime as dt
import hashlib
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
FIR_TAX_BASE = ROOT / "data" / "fir_tax_base.json"
STATUS_JSON = ROOT / "web" / "data" / "status.json"
CAPITAL_BUDGET = ROOT / "data" / "capital_budget.csv"
SERVED_GEOJSON = ROOT / "web" / "data" / "neighbourhood_value_per_acre.geojson"

ASSESSMENT_METADATA_URL = "https://data.edmonton.ca/api/views/q7d6-ambg.json"
MILL_RATES_URL = "https://data.edmonton.ca/resource/pwis-wc4c.json"
CAPITAL_BUDGET_URL = "https://budget.edmonton.ca/api/capital_budget.csv"

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
        from scripts.check_year_alignment import (  # noqa: PLC0415
            _load_rate_years,
            check_alignment,
            parse_coverage_year,
        )
        meta = requests.get(ASSESSMENT_METADATA_URL, timeout=timeout).json()
        detected = parse_coverage_year(meta)
    except Exception as exc:  # noqa: BLE001 — any failure is the same outcome
        return (UNKNOWN, "Assessment roll year",
                f"Could not read Socrata metadata ({exc}). Pin is {pinned}.")

    # ⚠️ ROUTED THROUGH check_alignment() RATHER THAN COMPARING HERE. This used
    # to test `detected == pinned` itself, which silently bypassed the
    # stale-metadata downgrade locked in on 2026-08-25 (`DECISIONS.md`): a
    # coverage year older than the calendar year means the STRING is untrusted,
    # not that the roll moved. With Edmonton's field reading 2025 through the
    # whole 2026 roll and our pin correctly at 2026, this check reported
    # "**Roll has moved to 2025, pin is still 2026**" and told Peter to work the
    # year-roll runbook for a roll already done — a false ⚠️ every month, in the
    # one channel that reaches a human. A digest that cries wolf monthly is how
    # the real alarm gets ignored.
    result, message = check_alignment(detected, pinned, _load_rate_years(MILL_RATES))
    if result == "aligned":
        return (OK, "Assessment roll year",
                f"Roll is {detected}, pin is {pinned} — aligned.")
    if result == "stale-metadata":
        return (UNKNOWN, "Assessment roll year",
                f"**Socrata's `Period of Coverage` says {detected} but it is "
                f"{dt.date.today().year} — the field is hand-maintained and is not "
                f"being kept current, so it says nothing about the roll.** Our pin "
                f"is {pinned}. The authority is `scripts/check_roll_year_against_fir.py`, "
                f"which measures parcels against Alberta FIR and gates the weekly "
                f"refresh; this digest cannot run it (it needs the raw roll, which "
                f"is not committed). Not an action unless that guard disagrees.")
    return (ACTION, "Assessment roll year",
            f"**Roll reads {detected}, pin is {pinned}.** {message} Work "
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


def check_temporal_archive_year():
    """Every ARCHIVED year must measure as the year it is filed under.

    ⚠️ THE SIBLING CHECK ABOVE WAS GREEN THROUGHOUT THE DEFECT THIS EXISTS TO
    CATCH, and the difference between them is the whole point.
    `check_temporal_archive` confirms the live year was CAPTURED; on 2026-07-28
    it was, so that check passed — but the capture was the 2026 roll filed under
    the label 2025, because the pin was stale and the guard validating it read
    Edmonton's own coverage string rather than measuring anything
    (`docs/DATA_ISSUES.md` issues 1-2). **Presence is not correctness.**

    Reuses scripts/check_temporal_archive_year.py rather than reimplementing it,
    so the digest and the standalone guard can never disagree about what a
    mislabelled year is. Reads only committed files (the archive + FIR), so
    unlike its neighbours it cannot fail on the network.
    """
    sys.path.insert(0, str(ROOT / "scripts"))
    from check_roll_year_against_fir import detect_year, filed_bases
    from check_temporal_archive_year import archived_residential_bases

    filed = filed_bases(FIR_TAX_BASE)
    ours = archived_residential_bases(TEMPORAL_ARCHIVE)
    if not ours:
        return (OK, "Archived years measure right", "The archive holds no years.")

    mismatched, inconclusive, unchecked, good = [], [], [], []
    for year in sorted(ours):
        if year not in filed:
            # Named, never counted as passing: an unverifiable year reading as
            # verified is the same failure shape being detected.
            unchecked.append(year)
            continue
        detected, _ = detect_year(ours[year], filed)
        if detected is None:
            inconclusive.append(year)
        elif detected != year:
            mismatched.append((year, detected))
        else:
            good.append(year)

    if mismatched:
        detail = "; ".join(f"**{f} measures as the {d} roll**" for f, d in mismatched)
        return (ACTION, "Archived years measure right",
                f"{detail}. The archive is FROZEN by design "
                f"(`src/load_temporal.write_archive`), so this needs a decision, "
                f"not a rewrite — `docs/DATA_ISSUES.md` §2 records how the last "
                f"one was resolved (the phantom entry was deleted, and the year "
                f"it claimed turned out to be unrecoverable). Run "
                f"`python scripts/check_temporal_archive_year.py` for the residuals.")
    if unchecked and not good:
        return (UNKNOWN, "Archived years measure right",
                f"**NOT CHECKED** — {_years(unchecked)} outside "
                f"`data/fir_tax_base.json`. Re-run `scripts/fetch_fir_tax_base.py`.")
    if inconclusive:
        return (UNKNOWN, "Archived years measure right",
                f"**INCONCLUSIVE** for {_years(inconclusive)} — no FIR year fits "
                f"within tolerance. Either FIR has not published that year yet, or "
                f"something other than the label is wrong.")

    # ⚠️ The COUNT is printed, not just a tick. After the 2026-08-27 deletion this
    # check ran against exactly ONE archived year, and a bare ✅ over a population
    # of 1 reads far stronger than the evidence is. It thickens by one each
    # January; until then the number is the caveat.
    note = f"{len(good)} archived year(s) measure as filed ({_years(good)})."
    if len(good) == 1:
        note += (" ⚠️ **One year is a thin population** — this goes green on a "
                 "single comparison and gains a year at each roll-forward.")
    if unchecked:
        note += (f" ⚠️ {_years(unchecked)} NOT CHECKED (outside "
                 f"`data/fir_tax_base.json`) and not counted above.")
    return (OK, "Archived years measure right", note)


def _years(ys):
    return ", ".join(str(y) for y in ys)


def _capital_fingerprint(text):
    """Row count, total approved, and an ORDER-INDEPENDENT hash of the CSV body.

    ⚠️ Sorted rather than hashed as raw bytes on purpose. The endpoint is
    byte-stable today (verified 2026-08-21, two fetches identical), but it is
    generated per request behind `Cache-Control: no-cache`, so a server-side
    regeneration could reorder rows without changing a single figure. Hashing
    the bytes would call that a budget change; hashing sorted rows does not.
    """
    rows = list(csv.reader(text.splitlines()))
    if not rows or rows[0][0] != "fiscal_year":
        raise ValueError(f"unexpected header {rows[0] if rows else '(empty)'!r}")
    body = rows[1:]
    total = sum(float(r[-1]) for r in body)
    digest = hashlib.sha256("\n".join(sorted(",".join(r) for r in body)).encode()).hexdigest()
    return len(body), total, digest


def check_capital_budget(timeout=60):
    """Has the capital budget moved since the copy committed in data/?

    ⚠️ There is NO freshness header to key off — `Last-Modified` merely echoes
    `Date` (unlike Socrata's `rowsUpdatedAt`), so the committed file IS the pin
    and the comparison is content-based. The budget is a four-year cycle moved
    by supplemental adjustments, so this is expected to stay green for months
    and then move in one step. `data/DATA.md` §19.
    """
    try:
        local = _capital_fingerprint(CAPITAL_BUDGET.read_text())
    except FileNotFoundError:
        return (UNKNOWN, "Capital budget",
                "No local copy at `data/capital_budget.csv` to compare against.")
    try:
        resp = requests.get(CAPITAL_BUDGET_URL, timeout=timeout)
        resp.raise_for_status()
        upstream = _capital_fingerprint(resp.text)
    except Exception as exc:  # noqa: BLE001 — unreachable is UNKNOWN, never ACTION
        return (UNKNOWN, "Capital budget",
                f"Could not reach or parse {CAPITAL_BUDGET_URL} ({exc}).")

    n_loc, tot_loc, dig_loc = local
    n_up, tot_up, dig_up = upstream
    if dig_loc == dig_up:
        return (OK, "Capital budget",
                f"Unchanged ({n_loc:,} rows, ${tot_loc:,.0f} approved).")
    return (ACTION, "Capital budget",
            f"**Upstream moved**: {n_loc:,} -> {n_up:,} rows, "
            f"${tot_loc:,.0f} -> ${tot_up:,.0f} approved "
            f"(delta {n_up - n_loc:+,} rows, ${tot_up - tot_loc:+,.0f}). "
            f"Re-fetch and commit — `docs/RUNBOOK.md` §1a.")


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


def check_unclassified_zoning():
    """Land the zoning map could not classify, off the SERVED file.

    `_categorize` defaults an unmatched code to `other` and only WARNS. In a
    weekly CI refresh a log line is effectively silent, so a new zoning-bylaw
    code would land unnoticed. This reports it instead of failing: the map draws
    the bucket as "Unclassified" grey, which is honest, so a new code is a
    go-look signal, not a reason to stop publishing (added 2026-08-31).
    """
    feats = json.loads(SERVED_GEOJSON.read_text())["features"]
    hoods = [(f["properties"].get("neighbourhood_name", "?"),
              f["properties"].get("frac_other") or 0.0) for f in feats]
    hit = sorted(((v, n) for n, v in hoods if v > 0), reverse=True)
    if not hit:
        return (OK, "Unclassified zoning",
                f"No unclassified land ({len(hoods):,} hoods, frac_other all 0).")
    worst = ", ".join(f"{n} {v:.1%}" for v, n in hit[:3])
    return (ACTION, "Unclassified zoning",
            f"**{len(hit)} of {len(hoods):,} hoods carry unclassified zoning** "
            f"(worst: {worst}). A zone code is missing from "
            f"`load_zoning.ZONE_CATEGORY` — grep the refresh log for `Unmatched "
            f"zone codes` to name it, then map it from the bylaw's purpose "
            f"statement (`data/DATA.md` §5). ⚠️ Do NOT fold it into a "
            f"non-residential total (`docs/DECISIONS.md` 2026-08-31).")


CHECKS = (
    check_assessment_roll,
    check_mill_rates,
    check_year_constants,
    check_stormwater,
    check_window_pins,
    check_temporal_archive,
    check_temporal_archive_year,
    check_capital_budget,
    check_unclassified_zoning,
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
