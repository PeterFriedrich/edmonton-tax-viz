"""Rank the City's approved operating budget by branch, for the /full/ budget panel.

Source is Socrata ``da9s-v9j8`` ("Approved Operating Budget - Expenses") on
``data.edmonton.ca``. ⚠️ **This is the SAME publication as
``budget.edmonton.ca/api/operating_budget.csv`` already catalogued in DATA.md
§17, not a second source** — verified 2026-08-16 by identity: same 8 columns,
same 7,283 rows, same FY2017-FY2026 span, and two totals tie to the dollar
(FY2025 tax-supported $3,855,881,010; FY2026 Parks and Roads $307,325,053).
The only thing that changes is the host, and that is the point: ``data.edmonton.ca``
is the host the rest of the pipeline already talks to, so this needs no new
network path.

This is a **manual, reviewed input** (mill-rates / FIR-debt pattern — DATA.md
§11, §17): run it by hand when Council approves a budget or an adjustment,
eyeball the diff, commit. It is NOT part of the weekly refresh — the approved
budget moves once or twice a year, the assessment roll moves weekly, and
letting the two share a cadence would imply a freshness this data does not have.

⚠️ **Its vintage is the source's ``rowsUpdatedAt``, not the run date**, and it is
published in the output so the panel can date itself honestly.

What it publishes
-----------------
One ranked list of branches, split in two:

  ``services``   — branches that deliver a service, i.e. that spend money on
                   people and things (SERVICE_CATEGORIES below).
  ``other``      — branches that spend money on none of those: debt service,
                   pay-as-you-go capital, neighbourhood renewal, corporate
                   overhead, tax adjustments.

⚠️ **THE SPLIT IS DERIVED, NEVER A HARDCODED BRANCH LIST.** A branch is "other"
iff it has zero dollars in every service category. This matters because the
budget tree gets re-cut (DATA.md §17 records two re-cuts of the PROGRAM tree
inside Parks and Roads alone); a name list would silently misclassify the day a
branch is renamed, and this cannot. The classification is written into the
output precisely so a human diff catches membership drift.

Why the split exists: ``Capital Project Financing`` is the single largest line
in the tax-supported budget ($687.6M in FY2026), ahead of Police. A ranked list
that does not separate it tells the reader the City's biggest expense is debt
service, which is true of the ledger and misleading about the City.

Basis and its limits (all inherited from the source — DATA.md §17)
------------------------------------------------------------------
  - **Gross operating expense, and operating only.** No capital programme. The
    revenue side lives in a sibling dataset (``m84q-ghmu``) that this script
    does not read, so nothing here is net.
  - **Branch totals are net of intra-municipal recoveries**, which are negative
    lines. That is what makes them safe to rank and sum — internal cross-charges
    do not get counted twice — but it means a branch total is not the same as
    what that branch spends in the world.
  - **``Tax Supported`` only** by default. That is the correct denominator for a
    tax-funded comparison and matches ``city_budget_context.json`` (DATA.md §16);
    all-funds would add Utilities and Enterprise/CRL and understate every share.

Integrity rules (no silent data drops)
--------------------------------------
  - the branch totals must sum to the fund total queried independently —
    a mismatch of even a dollar HARD-FAILS;
  - every branch must classify, and both sides must be non-empty;
  - a branch whose total is negative HARD-FAILS (it would rank nonsensically);
  - the requested budget year must exist in the source.

Usage::

    python scripts/export_budget_ranked.py                 # latest year
    python scripts/export_budget_ranked.py --year 2025
    python scripts/export_budget_ranked.py --out /tmp/b.json
"""

import argparse
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

logger = logging.getLogger(__name__)

DATASET_ID = "da9s-v9j8"
DATASET_NAME = "Approved Operating Budget - Expenses"
HOST = "https://data.edmonton.ca"
RESOURCE_URL = f"{HOST}/resource/{DATASET_ID}.json"
METADATA_URL = f"{HOST}/api/views/{DATASET_ID}.json"

OUT_PATH = Path(__file__).resolve().parent.parent / "web" / "data" / "budget_ranked.json"

DEFAULT_FUND_TYPE = "Tax Supported"

# A branch that spends money on ANY of these is delivering a service. The test
# is deliberately about inputs (people, materials, contractors, fleet, space)
# rather than about the branch's name, so a rename cannot change the answer.
# Measured 2026-08-16 on FY2026: 43 branches qualify, 5 do not, and the 5 are
# exactly the financing/corporate ones.
SERVICE_CATEGORIES = frozenset({
    "Personnel",
    "Materials, Goods and Supplies",
    "External Services",
    "Fleet Services",
    "Utilities & Other Charges",
    "Intra-municipal Charges",
})

TIMEOUT = 60


def _get(url: str, params: dict | None = None):
    r = requests.get(url, params=params, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


def source_vintage() -> dict:
    """The dataset's own last-updated stamp, so the panel dates itself honestly."""
    meta = _get(METADATA_URL)
    stamp = meta.get("rowsUpdatedAt")
    return {
        "dataset_id": DATASET_ID,
        "dataset_name": meta.get("name", DATASET_NAME),
        "host": HOST,
        "rows_updated_at": (
            datetime.fromtimestamp(stamp, timezone.utc).strftime("%Y-%m-%d")
            if stamp else None
        ),
        "retrieved": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    }


def available_years() -> list[int]:
    rows = _get(RESOURCE_URL, {"$select": "budget_year", "$group": "budget_year",
                               "$order": "budget_year"})
    return [int(r["budget_year"]) for r in rows]


def branch_categories(year: int, fund_type: str) -> dict[str, dict[str, float]]:
    """``{branch: {category: dollars}}`` for one year and fund."""
    rows = _get(RESOURCE_URL, {
        "$select": "branch,category,sum(budget) as amount",
        "$where": f"budget_year={year} AND fund_type='{fund_type}'",
        "$group": "branch,category",
        "$limit": "50000",
    })
    out: dict[str, dict[str, float]] = {}
    for r in rows:
        out.setdefault(r["branch"], {})[r["category"]] = float(r["amount"])
    return out


def fund_total(year: int, fund_type: str) -> float:
    """Queried independently of the branch breakdown so it can cross-check it."""
    rows = _get(RESOURCE_URL, {
        "$select": "sum(budget) as amount",
        "$where": f"budget_year={year} AND fund_type='{fund_type}'",
    })
    return float(rows[0]["amount"])


def delivers_a_service(categories: dict[str, float]) -> bool:
    return bool(set(categories) & SERVICE_CATEGORIES)


def build(year: int, fund_type: str = DEFAULT_FUND_TYPE) -> dict:
    years = available_years()
    if year not in years:
        raise SystemExit(
            f"budget_year {year} is not in {DATASET_ID}; available: {years}"
        )

    by_branch = branch_categories(year, fund_type)
    if not by_branch:
        raise SystemExit(f"no rows for {year} / {fund_type!r}")

    services, other = [], []
    for branch, cats in by_branch.items():
        total = sum(cats.values())
        # A negative branch total would sort below zero and read as a rebate;
        # the source has none today and we want to hear about it if that changes.
        if total < 0:
            raise SystemExit(
                f"branch {branch!r} totals {total:,.0f} — negative branch totals "
                "are not rankable; inspect the source before publishing"
            )
        row = {"branch": branch, "budget": round(total, 2)}
        (services if delivers_a_service(cats) else other).append(row)

    if not services or not other:
        raise SystemExit(
            f"classification collapsed: {len(services)} service / {len(other)} other "
            "branches. The category vocabulary has probably been re-cut — check "
            "SERVICE_CATEGORIES against the source before publishing."
        )

    services.sort(key=lambda r: -r["budget"])
    other.sort(key=lambda r: -r["budget"])

    services_total = sum(r["budget"] for r in services)
    other_total = sum(r["budget"] for r in other)
    published = fund_total(year, fund_type)
    # Independently queried, so this catches a dropped branch, a paging cutoff,
    # or a classification that lost rows. Cent-level tolerance only.
    if abs((services_total + other_total) - published) > 0.01:
        raise SystemExit(
            f"branch totals {services_total + other_total:,.2f} do not reconcile "
            f"with the published {fund_type} total {published:,.2f} for {year}"
        )

    return {
        "_purpose": (
            "Ranked branch-level operating budget for the /full/ budget panel. "
            "Citywide totals, NOT wired to the spatial pipeline — this answers "
            "'what does the City spend the most on', not 'what does this "
            "neighbourhood cost'. Nothing here is imported by src/ or main.py."
        ),
        "_basis": (
            "Gross OPERATING expense, operating only — no capital programme, and "
            "no revenue offset, so no line here is a net cost. Branch totals are "
            "net of intra-municipal recoveries (negative lines), which is what "
            "makes them safe to sum without double-counting internal charges."
        ),
        "_split": (
            "'services' are branches that spend on people/materials/contractors/"
            "fleet/space; 'other' are branches that spend on none of those - debt "
            "service, pay-as-you-go capital, renewal, corporate overhead, tax "
            "adjustments. DERIVED from the category mix, never a branch-name list, "
            "so a re-cut of the budget tree cannot silently misclassify."
        ),
        "source": source_vintage(),
        "budget_year": year,
        "fund_type": fund_type,
        "total": round(published, 2),
        "services_total": round(services_total, 2),
        "other_total": round(other_total, 2),
        "services": services,
        "other": other,
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--year", type=int, default=None,
                   help="budget year (default: the latest the source publishes)")
    p.add_argument("--fund-type", default=DEFAULT_FUND_TYPE)
    p.add_argument("--out", type=Path, default=OUT_PATH)
    args = p.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    year = args.year if args.year is not None else max(available_years())
    payload = build(year, args.fund_type)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n")

    logger.info(
        "%s FY%d %s: %d service branches (%.1f%%), %d other (%.1f%%), total $%.1fB -> %s",
        DATASET_ID, year, args.fund_type,
        len(payload["services"]), 100 * payload["services_total"] / payload["total"],
        len(payload["other"]), 100 * payload["other_total"] / payload["total"],
        payload["total"] / 1e9, args.out,
    )
    logger.info("source vintage: %s", payload["source"]["rows_updated_at"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
