# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # The Money lens, end to end
#
# This is one of the two lenses the **public** build exposes (the other is
# Development). It answers: *how much assessed value, and how much municipal tax
# revenue, does each neighbourhood carry per acre?*
#
# ## How to read this notebook
#
# It imports the real `src/` modules and runs the same calls, in the same order,
# as `main.run()`. It does not reimplement the pipeline — if it drifts from
# production, that is a bug in this notebook, not a difference of opinion.
#
# Two rules govern everything below, and they exist because the previous
# walkthrough notebook rotted silently:
#
# * **No number is written by hand.** Every figure in the prose is interpolated
#   from the run you are reading. The data refreshes weekly, so any hand-typed
#   count is wrong within days.
# * **Invariants are asserted, values are not.** `dropped == 50` would be a
#   weekly false alarm. `aggregation preserves total assessed value` must hold
#   for any data, forever — so that is what gets pinned.
#
# Checks accumulate and are reported together at the end, so one failure does
# not hide the rest.

# %%
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

# Resolve the repo root. nbconvert executes with cwd set to the notebook's own
# directory — which is a build directory, not the repo — so the runner passes
# the root explicitly. The cwd search is the fallback for running interactively
# in Jupyter. (`__file__` is not available in a kernel, so it is no use here.)
def _find_root() -> Path:
    env = os.environ.get("EDMONTON_REPO_ROOT")
    if env:
        return Path(env).resolve()
    here = Path.cwd()
    for p in (here, *here.parents):
        if (p / "src" / "join_and_calculate.py").exists():
            return p
    raise RuntimeError(
        "cannot locate the repo root — set EDMONTON_REPO_ROOT or run from inside the repo"
    )


REPO_ROOT = _find_root()
sys.path.insert(0, str(REPO_ROOT))

# Input paths and the rate year come from main.py rather than being restated
# here. Restating them is exactly how a documentation notebook drifts from the
# pipeline it claims to document — it would keep passing while describing files
# production no longer reads. main.py is import-safe and puts src/ on the path.
import main  # noqa: E402

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(name)s: %(message)s")

CHECKS: list[tuple[bool, str, str]] = []


def check(ok: bool, claim: str, detail: str = "") -> None:
    """Record an invariant. Reported together at the end; never stops the run."""
    CHECKS.append((bool(ok), claim, detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {claim}{'  — ' + detail if detail else ''}")


ASSESSMENT_CSV = main.ASSESSMENT_CSV
BOUNDARIES = main.BOUNDARIES_GEOJSON
MILL_RATES = main.MILL_RATES_JSON
ASSESSMENT_YEAR = main.ASSESSMENT_YEAR

vintage = datetime.fromtimestamp(ASSESSMENT_CSV.stat().st_mtime, timezone.utc)
print(f"repo root:        {REPO_ROOT}")
print(f"assessment roll:  {ASSESSMENT_CSV.name}")
print(f"data vintage:     {vintage:%Y-%m-%d %H:%M UTC}  (file mtime)")
print(f"mill-rate year:   {ASSESSMENT_YEAR}  (from main.ASSESSMENT_YEAR)")
print(f"executed:         {datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC}")

# %% [markdown]
# ## Step 1 — Load the assessment roll
#
# One row per property. `load_assessment` normalises neighbourhood names so they
# will match the boundary file later, applies the documented name corrections,
# drops rows with null or zero assessed value, and *flags* tax-exempt rows
# without removing them.
#
# That last distinction is the one worth understanding: **exclusion is a policy
# choice, not a data-cleaning step.** Dropping a zero-value row is arithmetic
# hygiene — it cannot change a ratio. Removing exempt institutional land would
# change what the map claims, so the pipeline refuses to make that call
# silently. Watch the log lines below: the drop is reported as a drop, the flag
# as a flag.

# %%
from load_assessment import load_assessment  # noqa: E402

assessment = load_assessment(str(ASSESSMENT_CSV))
print(f"\nrows: {len(assessment):,}   columns: {assessment.shape[1]}")
assessment.head()

# %% [markdown]
# ## Step 2 — Apply the mill rates
#
# The municipal levy for a property is *not* one rate times one value. A parcel
# can be split across up to three assessment classes, each with its own
# percentage and its own rate:
#
# $$\text{levy} = \text{assessed value} \times \sum_{\text{slot}}
#   \frac{\text{pct}_{\text{slot}}}{100} \times
#   \frac{\text{rate}[\text{class}_{\text{slot}}]}{1000}$$
#
# `res_levy` and `nonres_levy` are *subsets* of `levy` — a split-class parcel
# contributes only its residential slice to `res_levy`. They do not sum to
# `levy`, because other rate classes (farmland, machinery) exist. That
# relationship is the invariant worth pinning.

# %%
from apply_tax_rates import apply_tax_rates  # noqa: E402

rates_file = json.loads(MILL_RATES.read_text())
published_years = sorted(rates_file["rates"].keys())
print(f"mill_rates.json publishes: {published_years}")
print(f"pipeline asks for:         {ASSESSMENT_YEAR}\n")

check(
    str(ASSESSMENT_YEAR) in rates_file["rates"],
    "the rate year main.py asks for exists in mill_rates.json",
    f"{ASSESSMENT_YEAR} in {published_years} — the January year-roll breaks this first",
)

assessment = apply_tax_rates(assessment, MILL_RATES, ASSESSMENT_YEAR)

levy_total = assessment["levy"].sum()
res_total = assessment["res_levy"].sum()
nonres_total = assessment["nonres_levy"].sum()

print(f"\ncitywide municipal levy: ${levy_total:,.0f}")
print(f"  residential slices:    ${res_total:,.0f}  ({res_total / levy_total:.1%})")
print(f"  non-residential:       ${nonres_total:,.0f}  ({nonres_total / levy_total:.1%})")
print(f"  other classes:         ${levy_total - res_total - nonres_total:,.0f}")

check(
    res_total + nonres_total <= levy_total * 1.0000001,
    "res + nonres levy never exceeds total levy",
    f"${res_total + nonres_total:,.0f} <= ${levy_total:,.0f}",
)
check(levy_total > 0, "citywide levy is positive")
check(
    (assessment["levy"] < 0).sum() == 0,
    "no property carries a negative levy",
)

# %% [markdown]
# ## Step 3 — Aggregate to neighbourhoods
#
# Collapse ~440k property rows to one row per neighbourhood. This is the step
# that makes the whole project a *neighbourhood* analysis rather than a parcel
# one — and it is why `docs/PARCEL_LEVEL_OPPORTUNITIES.md` exists as a separate
# backlog.
#
# Aggregation is a pure sum, so it must be **value-preserving**. If this
# invariant ever fails, a neighbourhood is being dropped or double-counted.

# %%
from aggregate_by_neighbourhood import aggregate_by_neighbourhood  # noqa: E402

aggregated = aggregate_by_neighbourhood(assessment)

value_before = assessment["assessed_value"].sum()
value_after = aggregated["total_assessed_value"].sum()
revenue_after = aggregated["total_revenue"].sum()

print(f"\nneighbourhoods: {len(aggregated):,}")
print(f"assessed value  before ${value_before:,.0f}  after ${value_after:,.0f}")

check(
    abs(value_before - value_after) < 1.0,
    "aggregation preserves total assessed value",
    f"delta ${abs(value_before - value_after):,.4f}",
)
check(
    abs(levy_total - revenue_after) < 1.0,
    "aggregation preserves total levy",
    f"delta ${abs(levy_total - revenue_after):,.4f}",
)
check(
    aggregated["neighbourhood_name"].is_unique,
    "one row per neighbourhood after aggregation",
)

aggregated.sort_values("total_assessed_value", ascending=False).head(10)

# %% [markdown]
# ## Step 4 — Citywide revenue share, computed *before* the boundary join
#
# `main.run()` computes each neighbourhood's share of citywide revenue here,
# against the full roll — deliberately, and the ordering is load-bearing.
#
# The boundary join in step 6 can drop a neighbourhood the roll knows about.
# Deriving the share *after* that join (or in the browser, by summing the served
# features) would renormalise over whatever survived — so a neighbourhood's
# "% of city revenue" would silently depend on **who else made it onto the
# map**. Computing it here means the denominator is the real city.

# %%
city_revenue = aggregated["total_revenue"].sum()
aggregated["pct_of_city_revenue"] = (aggregated["total_revenue"] / city_revenue * 100).round(4)

top = aggregated.nlargest(5, "pct_of_city_revenue")[["neighbourhood_name", "pct_of_city_revenue"]]
print(f"citywide revenue denominator: ${city_revenue:,.0f}")
print(f"shares sum to: {aggregated['pct_of_city_revenue'].sum():.2f}%\n")

check(
    abs(aggregated["pct_of_city_revenue"].sum() - 100.0) < 0.05,
    "revenue shares sum to 100% across the full roll",
    f"{aggregated['pct_of_city_revenue'].sum():.4f}%",
)
top

# %% [markdown]
# ## Step 5 — Neighbourhood boundaries and area
#
# `load_boundaries` returns geometry plus `area_acres`. The CRS is set
# explicitly before any area calculation — projecting after measuring would
# silently produce wrong acreages, which is why the project rule says to set it
# up front rather than trusting a file's declared CRS.

# %%
from load_boundaries import load_boundaries  # noqa: E402

boundaries = load_boundaries(str(BOUNDARIES))
print(f"boundaries: {len(boundaries):,}   CRS: {boundaries.crs}")
print(f"total area: {boundaries['area_acres'].sum():,.0f} acres")

check(boundaries.crs is not None, "boundaries carry an explicit CRS")
check(
    (boundaries["area_acres"] > 0).all(),
    "every boundary has positive area",
    "a zero would make value_per_acre infinite",
)
boundaries[["neighbourhood_name", "area_acres"]].head()

# %% [markdown]
# ## Step 6 — Join, and account for every unmatched name
#
# `join_and_calculate` left-joins boundaries → assessment and computes
# `value_per_acre` and `revenue_per_acre`. Every optional service layer is left
# at `None` here, so this is the Money lens alone; the cost lenses that `/full/`
# adds are a separate notebook.
#
# **No silent data drops** is the project's core rule, so the point of this step
# is not that the join succeeds — it is that anything unmatched is *named*. Watch
# for the warning about the known straggler documented in `data/DATA.md`.

# %%
from join_and_calculate import join_and_calculate  # noqa: E402

joined = join_and_calculate(aggregated, boundaries)

matched = joined["total_assessed_value"].notna().sum()
print(f"\nfeatures: {len(joined):,}   with assessment: {matched:,}")

roll_names = set(aggregated["neighbourhood_name"])
boundary_names = set(boundaries["neighbourhood_name"])
in_roll_only = sorted(roll_names - boundary_names)
in_boundary_only = sorted(boundary_names - roll_names)

print(f"\nin roll but not on the map ({len(in_roll_only)}): {in_roll_only}")
print(f"on the map but not in the roll ({len(in_boundary_only)}): {len(in_boundary_only)} names")

check(
    len(joined) == len(boundaries),
    "the join is boundary-preserving (left join, no row multiplication)",
    f"{len(joined):,} == {len(boundaries):,}",
)
check(
    joined["neighbourhood_name"].is_unique,
    "no boundary was duplicated by the join",
)
check(
    matched > len(joined) * 0.9,
    "over 90% of boundaries matched an assessment row",
    f"{matched:,}/{len(joined):,} = {matched / len(joined):.1%}",
)

# %% [markdown]
# ## Step 7 — The published metric, checked by hand
#
# `value_per_acre = total_assessed_value / area_acres`. Recomputing it
# independently for the top neighbourhoods is the cheapest possible guard
# against a units or denominator error — the failure mode this project
# actually has.

# %%
have = joined[joined["value_per_acre"].notna()].copy()
have["recomputed"] = have["total_assessed_value"] / have["area_acres"]
have["delta"] = (have["value_per_acre"] - have["recomputed"]).abs()

worst = have["delta"].max()
check(
    worst < 0.01,
    "value_per_acre equals total_assessed_value / area_acres for every feature",
    f"largest disagreement ${worst:.6f}",
)

if "revenue_per_acre" in have.columns:
    rev = have[have["revenue_per_acre"].notna()].copy()
    rev_delta = (rev["revenue_per_acre"] - rev["total_revenue"] / rev["area_acres"]).abs().max()
    check(
        rev_delta < 0.01,
        "revenue_per_acre equals total_revenue / area_acres for every feature",
        f"largest disagreement ${rev_delta:.6f}",
    )

cols = ["neighbourhood_name", "total_assessed_value", "area_acres", "value_per_acre"]
if "revenue_per_acre" in have.columns:
    cols.append("revenue_per_acre")
have.nlargest(10, "value_per_acre")[cols]

# %% [markdown]
# ## What this notebook does *not* cover
#
# Stated explicitly so its silence is never mistaken for a clean bill of health:
#
# * the **lot-acre denominator** (`lot_acres_eligible`, `parcel_frac`) and its
#   cardinality guard — the `ineligible_points` drift is an open investigation;
# * the **Development lens** (building permits) — the public build's other lens;
# * every **cost lens** that `/full/` adds: services, transport, temporal, ratio;
# * the **web export** itself — setback, simplification, and the served column
#   contract, which `scripts/check_served_columns.py` already guards.

# %%
failed = [c for c in CHECKS if not c[0]]
print(f"{len(CHECKS) - len(failed)}/{len(CHECKS)} invariants held\n")
for ok, claim, detail in CHECKS:
    print(f"  [{'PASS' if ok else 'FAIL'}] {claim}{'  — ' + detail if detail else ''}")

if failed:
    raise AssertionError(
        f"{len(failed)} invariant(s) failed:\n"
        + "\n".join(f"  - {claim} {detail}" for _, claim, detail in failed)
    )
print("\nAll invariants held.")
