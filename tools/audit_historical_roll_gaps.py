#!/usr/bin/env python3
"""Map the completeness defect in Edmonton's Historical assessment roll.

`qi6a-xuwt` (Property Assessment Data — Historical) is missing properties in its
recent slices: whole multi-unit buildings absent from a year while present both
before and after. Proven for 2024/2025 on 2026-07-28 (`data/DATA.md` §0); this
tool establishes the extent across ALL 14 years, which is Phase 0 of
`docs/SPEC_temporal.md` — a hard gate on the temporal lens.

TWO DETECTORS, because neither alone is sufficient. Report the union.

  A. SELF-AUDIT — present in year N-1 AND N+1, absent from N. Buildings do not
     blink. Needs no external source, and catches properties later demolished.
     ** BLIND TO ANY DROPOUT THAT NEVER RETURNS. ** This bit us: the Stantec
     Tower accounts vanished in 2024 and stayed vanished, so the 2024 self-audit
     reported 5 defects when the true figure is 2,321. A run that reports ~0 for
     recent years has NOT shown them clean.

  B. CURRENT-ROLL CONTROL — present in year N-1 AND in the CURRENT roll
     (`q7d6-ambg`, independent and complete), absent from N. A property that
     existed before and still exists today cannot legitimately be missing in
     between. Catches persistent dropouts, which is the shape of this defect.
     Its own blind spot: properties demolished since are excluded, so a defect
     affecting one is invisible — which is why detector A is kept.

2012 is untestable by A (no prior year); B still applies from 2013 on.

Deliberately NOT diagnosed here: the cause. This reports the symptom only.

    python tools/audit_historical_roll_gaps.py
    python tools/audit_historical_roll_gaps.py --out output/roll_gaps.json
"""
from __future__ import annotations

import argparse
import collections
import json
import logging
import sys
import urllib.parse
import urllib.request
from pathlib import Path

HISTORICAL = "qi6a-xuwt"  # Property Assessment Data (Historical), 2012-2025
CURRENT = "q7d6-ambg"     # Property Assessment Data (Current Calendar Year)

FIRST_YEAR, LAST_YEAR = 2012, 2025
PAGE = 50_000  # Socrata's default page size is 1,000 -- always pass $limit
TIMEOUT = 300

log = logging.getLogger("roll_gaps")


def soda(dataset: str, **params) -> list[dict]:
    """One Socrata request. Keys are passed as $-prefixed SoQL parameters."""
    url = f"https://data.edmonton.ca/resource/{dataset}.json?" + urllib.parse.urlencode(
        {("$" + k): v for k, v in params.items()}
    )
    with urllib.request.urlopen(url, timeout=TIMEOUT) as resp:
        return json.load(resp)


def accounts(dataset: str, where: str | None = None, label: str = "") -> set[str]:
    """Every account_number matching `where`, paged.

    $order is required for stable offset paging -- without it Socrata may
    repeat or skip rows across pages and the set silently loses members.
    """
    out: set[str] = set()
    offset = 0
    while True:
        params = {"select": "account_number", "order": "account_number",
                  "limit": str(PAGE), "offset": str(offset)}
        if where:
            params["where"] = where
        rows = soda(dataset, **params)
        if not rows:
            break
        out.update(r["account_number"] for r in rows if r.get("account_number"))
        offset += PAGE
        if len(rows) < PAGE:
            break
    log.info("  %-22s %8d accounts", label, len(out))
    return out


def describe(account_ids: list[str]) -> list[dict]:
    """Look the given accounts up in the CURRENT roll, batched.

    The current roll is used deliberately: these accounts are missing from the
    historical year under test, so it is the source that can still say where
    they are and what they are worth today.
    """
    out: list[dict] = []
    for i in range(0, len(account_ids), 200):
        in_list = ",".join("'" + a + "'" for a in account_ids[i:i + 200])
        out += soda(
            CURRENT,
            select="account_number,neighbourhood,assessed_value,mill_class_1,house_number,street_name",
            where=f"account_number in({in_list})",
            limit=str(PAGE),
        )
    return out


def profile(rows: list[dict]) -> dict:
    """Summarise a defect set: value, hoods, classes, address clustering."""
    value = sum(float(r.get("assessed_value") or 0) for r in rows)
    hoods = collections.Counter(r.get("neighbourhood") or "(blank)" for r in rows)
    classes = collections.Counter(r.get("mill_class_1") or "(none)" for r in rows)
    addrs = collections.Counter(
        f"{r.get('house_number') or '?'} {r.get('street_name') or '?'}" for r in rows
    )
    # Buildings, not scattered units: how much sits at repeat addresses?
    clustered = sum(n for a, n in addrs.items() if n >= 10 and not a.startswith("?"))
    return {
        "resolved_in_current_roll": len(rows),
        "current_assessed_value": value,
        "neighbourhoods": len(hoods),
        "top_neighbourhoods": hoods.most_common(8),
        "by_class": classes.most_common(),
        "top_addresses": [(a, n) for a, n in addrs.most_common(8)],
        "share_at_addresses_with_10plus": (clustered / len(rows)) if rows else 0.0,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=Path("output/historical_roll_gaps.json"))
    ap.add_argument("--no-profile", action="store_true",
                    help="counts only; skip the current-roll lookups (much faster)")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s",
                        stream=sys.stdout)

    years = list(range(FIRST_YEAR, LAST_YEAR + 1))
    log.info("Fetching account sets (sliding window; each year fetched once)")

    results: dict[str, dict] = {}
    window: dict[int, set[str]] = {}

    def load(y: int) -> None:
        if y not in window:
            window[y] = accounts(HISTORICAL, f"assessment_year='{y}'", f"historical {y}")

    # The independent control, fetched once and held for every year's detector B.
    current = accounts(CURRENT, None, "CURRENT roll")

    for year in years[1:]:
        for y in (year - 1, year, year + 1):
            if y <= LAST_YEAR:
                load(y)

        # A: self-audit. Unavailable for the last year (no N+1 exists).
        self_audit: set[str] = set()
        if year < LAST_YEAR:
            self_audit = (window[year - 1] & window[year + 1]) - window[year]
        # B: current-roll control. Available for every year from 2013.
        control = (window[year - 1] & current) - window[year]

        union = sorted(self_audit | control)
        results[str(year)] = {
            "roll_size": len(window[year]),
            "self_audit": len(self_audit),
            "self_audit_available": year < LAST_YEAR,
            "current_roll_control": len(control),
            "defect_accounts": len(union),
            "ids": union,
        }
        log.info("  %d: roll %d  self-audit %-6d control %-6d UNION %d",
                 year, len(window[year]), len(self_audit), len(control), len(union))
        window.pop(year - 2, None)

    results[str(FIRST_YEAR)] = {"test": "untestable (no prior year)",
                                "roll_size": None, "defect_accounts": None, "ids": []}

    # --- profile each year's defect set against the current roll
    if not args.no_profile:
        log.info("\nProfiling defect sets against the current roll")
        for year, res in sorted(results.items()):
            if res["ids"]:
                res["profile"] = profile(describe(res["ids"]))
                log.info("  %s: %d resolved, $%.2fB, %d hoods", year,
                         res["profile"]["resolved_in_current_roll"],
                         res["profile"]["current_assessed_value"] / 1e9,
                         res["profile"]["neighbourhoods"])

    # --- report
    log.info("\n%s", "=" * 66)
    log.info("DEFECT MAP -- accounts missing from a year they should be in")
    log.info("%s", "=" * 66)
    log.info("%6s %10s %8s %8s %8s %7s   %s", "year", "roll", "self", "control",
             "union", "rate", "note")
    for year in years:
        r = results[str(year)]
        n = r["defect_accounts"]
        if n is None:
            log.info("%6d %10s %8s %8s %8s %7s   %s", year, "-", "-", "-", "-", "-", r["test"])
            continue
        rate = f"{100 * n / r['roll_size']:.2f}%" if r["roll_size"] else "-"
        note = ""
        if r.get("profile"):
            note = (f"${r['profile']['current_assessed_value']/1e9:.2f}B, "
                    f"{r['profile']['neighbourhoods']} hoods")
        sa = str(r["self_audit"]) if r["self_audit_available"] else "n/a"
        log.info("%6d %10d %8s %8d %8d %7s   %s", year, r["roll_size"], sa,
                 r["current_roll_control"], n, rate, note)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(results, indent=2))
    log.info("\nwrote %s", args.out)

    worst = max((y for y in years if results[str(y)]["defect_accounts"]),
                key=lambda y: results[str(y)]["defect_accounts"], default=None)
    if worst:
        log.info("worst year: %d (%d accounts)", worst, results[str(worst)]["defect_accounts"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
