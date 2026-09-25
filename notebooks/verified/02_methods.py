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
# # Methods & definitions
#
# How the numbers on [the map](https://peterfriedrich.github.io/edmonton-tax-viz/)
# are made — written for a reader checking the work rather than building it.
#
# This page replaced a prose `docs/METHODS.md` that quoted figures by hand. By
# the time it was retired it was still quoting the **2025** mill rates after
# the pipeline had moved to 2026 — nothing noticed, because nothing re-read
# it. So this page follows the rule of the
# [Money lens notebook](01_money_lens.html): **no number below is typed by
# hand.** Each one is computed from the data the site is publishing this week,
# by the code in the cell above it. Constants (thresholds, rates) are read from
# the pipeline module that uses them, never restated.
#
# Where a claim rests on a one-off investigation rather than on data this page
# can recompute, it is cited to the `FINDINGS_*` document that holds it, with no
# number attached — see the last section for that list.

# %%
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from IPython.display import Markdown, display


# Same root resolution as 01_money_lens: nbconvert's cwd is the build dir, so the
# runner passes the root; the cwd search is for running interactively.
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
import main  # noqa: E402  (import-safe; puts src/ on the path)

# The pipeline's INFO lines are the Money lens notebook's subject, not this
# page's; warnings still surface.
logging.basicConfig(stream=sys.stdout, level=logging.WARNING, format="%(name)s: %(message)s")

CHECKS: list[tuple[bool, str, str]] = []


def check(ok: bool, claim: str, detail: str = "") -> None:
    """Record an invariant. Reported together at the end; never stops the run."""
    CHECKS.append((bool(ok), claim, detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {claim}{'  — ' + detail if detail else ''}")


def md(text: str) -> None:
    # The notebook renderer reads a pair of bare `$` as TeX math delimiters,
    # which swallows the text between two dollar amounts.
    display(Markdown(text.replace("$", r"\$")))


WEB_DATA = REPO_ROOT / "web" / "data"
features = json.loads((WEB_DATA / "neighbourhood_value_per_acre.geojson").read_text())["features"]
served = pd.DataFrame([f["properties"] for f in features])
status = json.loads((WEB_DATA / "status.json").read_text())
grid = json.loads((WEB_DATA / "value_grid.json").read_text())
grid_df = pd.DataFrame(grid["cells"], columns=grid["columns"])

print(f"served neighbourhoods: {len(served):,}")
print(f"roll year / rate year: {status.get('data_year')} / {status.get('rate_year')}")
print(f"served data generated: {status.get('generated')}")
print(f"executed:              {datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC}")

# %% [markdown]
# ## 1. The core metric: municipal revenue (or assessed value) per acre
#
# **Numerator.** Every account on the City's assessment roll (open dataset
# `q7d6-ambg`) carries an assessed value and up to three tax classes, each with
# a percentage of the value. Per account:
#
# ```
# levy = Σ over classes  assessed_value × (class % / 100) × (mill rate / 1000)
# ```
#
# using the City's published **municipal** mill rates (`pwis-wc4c`). The
# provincial education levy is excluded: the project measures the City's fiscal
# capacity, not a household's tax burden. Accounts sum by neighbourhood, and the
# map's toggle shows either this revenue or raw assessed value (the
# [Urban3](https://www.urbanthree.com/)/Strong Towns convention).

# %%
from apply_tax_rates import apply_tax_rates  # noqa: E402
from load_assessment import load_assessment  # noqa: E402

YEAR = main.ASSESSMENT_YEAR
rates = json.loads(main.MILL_RATES_JSON.read_text())["rates"][str(YEAR)]
assessment = apply_tax_rates(load_assessment(str(main.ASSESSMENT_CSV)), main.MILL_RATES_JSON, YEAR)
levy_total = assessment["levy"].sum()
res_rate = rates["Residential"]["municipal"]
nonres_rate = rates["Non Residential"]["municipal"]

md(f"""
For **{YEAR}** the rates are Residential **{res_rate}**, Other Residential
**{rates['Other Residential']['municipal']}** and Non Residential
**{nonres_rate}** per $1,000. Applied to **{len(assessment):,}** accounts, that
gives a citywide municipal levy of **${levy_total / 1e9:,.2f}B**.

The gap between the value view and the revenue view is exactly Edmonton's
class-differential rates: non-residential property is taxed
**{nonres_rate / res_rate:.1f}×** residential per dollar of value.
(`docs/SPEC_revenue.md`)
""")

# %% [markdown]
# **Denominator — two, on purpose.** A toggle offers:
#
# - **Ground acres** (the default): the neighbourhood boundary polygon's area
#   (`65fr-66s6`), which includes roads, parks and rights-of-way. It is the
#   default because it is *structurally immune* to parcel-record
#   inconsistencies — it never reads a lot-size field.
# - **Lot acres**: the deduplicated area of titled lots (`dkk9-cj3x`
#   `lot_size`), the denominator closest to Urban3's own method — revenue per
#   acre of private land. Neighbourhoods where titled lots cover too little of
#   the boundary are greyed out rather than shown, because a near-zero
#   denominator explodes the ratio.
#
# Urban3's published method divides by *parcel* acres, so lot-acre mode is the
# comparable one; the ground-acre default is this project's own
# robustness-motivated addition, not borrowed methodology.
# (`docs/FINDINGS_denominator_cardinality.md`)

# %%
from export_value_grid import (  # noqa: E402
    KNOWN_BOUND_OUTLIERS, MULTI_UNIT_MIN_LOT_M2, SHARE_MAX_M2, SQ_M_PER_ACRE,
    _point_lot_stats,
)
from join_and_calculate import LOW_PARCEL_FRAC  # noqa: E402
from load_boundaries import load_boundaries  # noqa: E402
from load_property_info import load_property_info  # noqa: E402

boundaries = load_boundaries(str(main.BOUNDARIES_GEOJSON))
ground_acres = boundaries.set_index("neighbourhood_name")["area_acres"]
served["ground_acres"] = served["neighbourhood_name"].map(ground_acres)

check(
    served["ground_acres"].notna().all(),
    "every served neighbourhood has a boundary area",
    f"{served['ground_acres'].isna().sum()} without",
)

# A hood's lot-acre figure is shown only at or above the parcel-coverage floor.
suppressed = served["value_per_lot_acre"].isna()
below_floor = ~(served["parcel_frac"] >= LOW_PARCEL_FRAC)
check(
    not (~suppressed & below_floor).any(),
    "no lot-acre figure is served below the parcel-coverage floor",
    f"{int((~suppressed & below_floor).sum())} served below {LOW_PARCEL_FRAC:.0%}",
)

md(f"""
The map covers **{len(served):,}** neighbourhoods and
**{served['ground_acres'].sum():,.0f}** ground acres. The lot-acre floor is
**{LOW_PARCEL_FRAC:.0%}**: this week **{int(below_floor.sum())}**
neighbourhoods have titled lots covering less than that share of their boundary,
and are greyed out in lot-acre mode.
""")

# %% [markdown]
# ## 2. The two hard cases, worked openly
#
# Anyone spot-checking this map lands on the same two places we audited first,
# so here is what the data does there.
#
# **One huge account.** The roll's single largest account is pinned to one
# coordinate. At the neighbourhood level it is simply summed once with its
# neighbours — no distortion. On the 100 m grid (the Glass view) one point ÷ one
# cell makes it a very tall needle under ground acres, which is why the grid
# carries the same lot-acre toggle: dollars per map cell and dollars per acre of
# land are both visible.

# %%
biggest = assessment.nlargest(1, "assessed_value").iloc[0]
hood = biggest["neighbourhood_name"]
hood_value = assessment.loc[assessment["neighbourhood_name"] == hood, "assessed_value"].sum()

# The account's own cell: grid lon/lat are cell centres, so the nearest centre
# (with longitude shrunk by cos(latitude)) is the cell it was binned into.
coslat = np.cos(np.radians(biggest["latitude"]))
dist = np.hypot((grid_df["lon"] - biggest["longitude"]) * coslat, grid_df["lat"] - biggest["latitude"])
its_cell = grid_df.loc[dist.idxmin()]
ground_rank = int((grid_df["revenue_per_acre"] > its_cell["revenue_per_acre"]).sum()) + 1
lot_rank = int((grid_df["revenue_per_lot_acre"] > its_cell["revenue_per_lot_acre"]).sum()) + 1
top_lot = grid_df.nlargest(1, "revenue_per_lot_acre").iloc[0]

md(f"""
This week the largest account is **${biggest['assessed_value'] / 1e9:,.2f}B** in
**{hood.title()}**, where it is **{biggest['assessed_value'] / hood_value:.0%}**
of the neighbourhood's assessed value.

On the grid, its cell carries **${its_cell['revenue_per_acre']:,.0f}** of levy
per ground acre — number **{ground_rank:,}** of {len(grid_df):,} cells. Per acre
of lot it carries **${its_cell['revenue_per_lot_acre']:,.0f}** and ranks
**{lot_rank:,}**, because its lot is large; the top lot-acre cell carries
**${top_lot['revenue_per_lot_acre']:,.0f}**, about
**{top_lot['revenue_per_lot_acre'] / its_cell['revenue_per_lot_acre']:,.0f}×**
more. The two rankings disagree by design — the toggle exists so both readings
can be seen.
""")
grid_df.nlargest(5, "revenue_per_acre")[["lat", "lon", "revenue_per_acre", "revenue_per_lot_acre"]]

# %% [markdown]
# **Condominiums.** Many taxable units share one lot, and the open data's
# `lot_size` field encodes that inconsistently — sometimes the whole parcel
# duplicated onto every unit, sometimes real per-unit shares, sometimes null.
# Independent Urban3-style replications have typically *excluded* condos
# entirely, deleting dense high-value land from their maps. This project applies
# a repeat-aware rule instead, at each property point:
#
# - a repeated lot size **under** the share threshold counts once per unit
#   (genuine apportioned shares — the townhouse regime);
# - a repeated lot size **at or above** it counts once (a duplicated parcel);
# - a point whose units are mostly null, or whose total is too small to be an
#   area at all, is **excluded** from the lot-acre view and reported — never
#   silently dropped. Its dollars stay in the ground-acre view.
#
# (`docs/FINDINGS_lot_dedupe.md`, which also holds the threshold-sensitivity
# test.)

# %%
lots = assessment.merge(load_property_info(main.PROPERTY_INFO_CSV), on="account_number", how="left")
pts = lots.loc[lots["latitude"].notna() & lots["longitude"].notna()]
per_point = _point_lot_stats(pts[["latitude", "longitude", "lot_size"]])

rows = pts.merge(per_point[["latitude", "longitude", "eligible"]], on=["latitude", "longitude"], how="left")
# A point the classifier never saw is a silent drop; the two sums below would
# still add to the roll, so this is the check, not their total.
check(
    rows["eligible"].notna().all(),
    "every located account's point is classified as in the lot-acre view or excluded",
    f"{int(rows['eligible'].isna().sum())} unclassified",
)
eligible = rows["eligible"].fillna(False).astype(bool)
inelig_value = rows.loc[~eligible, "assessed_value"].sum()
elig_value = rows.loc[eligible, "assessed_value"].sum()
roll_value = pts["assessed_value"].sum()

multi = per_point["n"] > 1
n_inelig = int((~per_point["eligible"]).sum())
elig_acres = per_point.loc[per_point["eligible"], "lot_m2"].sum() / SQ_M_PER_ACRE

md(f"""
The share threshold is **{SHARE_MAX_M2:,.0f} m²**, and a multi-unit point
totalling under **{MULTI_UNIT_MIN_LOT_M2:,.0f} m²** is treated as share-coded
rather than an area. This week the roll has **{len(per_point):,}** distinct
property points, **{int(multi.sum()):,}** of them multi-unit. **{n_inelig:,}**
points are excluded from the lot-acre view, carrying
**${inelig_value / 1e9:,.2f}B** — **{inelig_value / roll_value:.2%}** of located
assessed value.

The eligible lots total **{elig_acres:,.0f}** acres, which is
**{elig_acres / served['ground_acres'].sum():.0%}** of the ground acres above;
the rest is roads, parks, rights-of-way and land with no usable lot record.

A pipeline check asserts each neighbourhood's deduplicated lot acres fit inside
its boundary. Known, documented exceptions:
**{', '.join(o.title() for o in KNOWN_BOUND_OUTLIERS) or 'none'}**.
""")

# %% [markdown]
# The neighbourhood-level metric is structurally immune to both cases: its
# numerator never joins parcel geometry and its denominator never reads
# `lot_size`. (`docs/FINDINGS_denominator_cardinality.md`)
#
# ## 3. Grey neighbourhoods: the set-aside layer
#
# Some neighbourhoods render neutral grey instead of low-red: those where most
# of the land is zoned river valley, natural area or parks ("never taxable"), or
# future-development and agricultural reserve ("not yet"), found by overlaying
# the Zoning Bylaw geometry (`fixa-tstc`) on the boundaries. Painting them as
# "low revenue" would be true arithmetic but a false story; grey says *this
# land is not on the taxable roll by design*. The rule keys off zoning, so as
# fringe land is rezoned and develops it rejoins the colour scale on a later
# refresh. (`docs/FINDINGS_revenue_scale.md`)

# %%
from load_zoning import SET_ASIDE_THRESHOLD  # noqa: E402

set_aside = served["is_set_aside"].fillna(False).astype(bool)
check(
    set_aside.equals(served["set_aside_frac"].fillna(0) >= SET_ASIDE_THRESHOLD),
    "the grey flag is exactly the set-aside share at or above the threshold",
    f"{int(set_aside.sum())} flagged",
)
md(f"""
The threshold is **{SET_ASIDE_THRESHOLD:.0%}** of the land. This week
**{int(set_aside.sum())}** of **{len(served):,}** neighbourhoods are grey.
""")

# %% [markdown]
# **Standing caveat:** tax-exempt institutions (universities, hospitals, crown
# land) are *absent from the assessment roll*, not listed at zero — so revenue
# per acre genuinely understates neighbourhoods holding them, and no flag in the
# roll can mark it. The effect is measured instead: institutional-proxy zoning
# carrying no taxable account, per neighbourhood, with the University of Alberta
# area as the worked example (`docs/FINDINGS_exempt_institutional.md`).
#
# ## 4. The Glass view (100 m grid)
#
# Sub-neighbourhood detail: each account's dollars are binned into square
# cells, and prism height is dollars in the cell ÷ cell acres, with the same
# ground/lot-acre toggle as above. It is pure point binning — no interpolation,
# no spreading — so a cell shows exactly the accounts pinned inside it.

# %%
md(f"""
The cells are **{grid['cell_m']:,.0f} m** on a side; **{len(grid_df):,}** of
them hold at least one account this week.
""")

# %% [markdown]
# ## 5. The cost side (Services view)
#
# Revenue alone is half the fiscal story. Each service layer is a *supply* or a
# *modelled cost* per acre; none of them changes the revenue numbers. Layers
# marked *in development* are built and described here but are not on the
# public map yet.
#
# - **Roads** — metres of City-maintained **collector and local** road
#   centreline per acre (`9j8t-zm52`). Arterials are computed but excluded: they
#   are shared citywide infrastructure that happens to run along neighbourhood
#   edges. Alleys and provincial highways are out. This is the strongest cost
#   lens methodologically — road length drives recurring surface-infrastructure
#   cost, and it is measured, not modelled. Two **road cost** layers price those
#   metres on two bases that must never be added or compared: *lifecycle*
#   (upkeep plus eventual rebuilding, annualized) and *operating* (upkeep and
#   snow clearing only, from the last roads-only budget the City published).
# - The **Ratio view** divides revenue by road metres (and, *in development*,
#   by fire events). Only those two appear because only they are services the property
#   tax levy funds — the modelled EPCOR charges below are paid by utility
#   ratepayers, and dividing tax revenue by them would compare unrelated money
#   flows. (`docs/SPEC_services.md`, `docs/SPEC_utilities.md`)
# - **Fire rescue (demand)**, *in development* — emergency response events per acre per year,
#   averaged over a pinned window of full calendar years (`7hsn-idqi`), with the
#   station locations plotted. This is *service demand*, not response-time
#   performance; medical calls are the majority of events (a documented caveat,
#   not a filter). Training and similar operational events are excluded.
# - **Stormwater (modelled)**, *in development* — EPCOR's own bylaw formula (area × intensity ×
#   runoff coefficient) applied to every roll parcel.
# - **Water + sanitary (modelled)**, *in development* — a per-connection model: meter-size fixed
#   charges plus block volumetric rates.
# - **Electricity/gas franchise fees** — modelled as data columns but *not*
#   mapped: a flat per-dwelling proxy makes every map of them a dwelling-density
#   map. Listed here for honesty about what was tried and why it isn't shown.
#
# Each modelled dollar figure is labelled **modelled, not billed** in the app,
# and each model was validated against published EPCOR or audited City figures
# before shipping (`docs/FINDINGS_utility_validation.md`).

# %%
from load_roads import METRIC_GROUPS  # noqa: E402

from join_and_calculate import load_unit_costs  # noqa: E402

unit_costs = load_unit_costs(main.UNIT_COSTS_JSON)
n_stations = len(json.loads((WEB_DATA / "fire_stations.json").read_text())["stations"])


def citywide(col: str) -> float:
    return (served[col] * served["ground_acres"]).sum()


road_km = citywide("road_m_per_acre") / 1000
check(road_km > 0, "the served road metric covers a positive length", f"{road_km:,.0f} km")

md(f"""
This week, in figures:

| layer | citywide |
|---|---|
| road centreline in the metric ({' + '.join(METRIC_GROUPS)}) | **{road_km:,.0f} km** |
| lifecycle road rate | **${unit_costs['road_dollars_per_m']:,.2f}** per road metre per year |
| operating road rate | **${unit_costs['road_ops_dollars_per_m']:,.2f}** per road metre per year |
| fire events (in development) | **{citywide('fire_events_per_acre'):,.0f}** per year, window **{min(main.FIRE_YEARS)}–{max(main.FIRE_YEARS)}**, **{n_stations}** stations |
| stormwater, modelled (in development) | **${citywide('storm_charge_per_acre') / 1e6:,.1f}M** per year |
| water + sanitary, modelled (in development) | **${citywide('water_charge_per_acre') / 1e6:,.1f}M** per year |
""")

# %% [markdown]
# ## 6. Display honesty rules
#
# - **Prism height is always linear.** No transform ever exaggerates height.
# - Colour ramps may use a square-root (or, where noted, log) transform to
#   spread a skewed distribution across the palette, and the app has a toggle
#   to turn that off and see true-magnitude colour. Every transform choice is
#   recorded with its skew test in `docs/FINDINGS_revenue_scale.md` §6.
# - No silent data drops anywhere in the pipeline: unmatched, excluded or
#   suppressed records are counted and logged, and validation checks fail the
#   build rather than degrade it.
#
# ## 7. Data sources
#
# All open data; no desktop GIS software; Python only.
#
# | Input | Edmonton Open Data ID | Notes |
# |---|---|---|
# | Property assessments | `q7d6-ambg` | the current roll, live weekly feed |
# | Property information (lot sizes) | `dkk9-cj3x` | joins to assessments by account |
# | Neighbourhood boundaries | `65fr-66s6` | |
# | Tax rates | `pwis-wc4c` | municipal mill rates by class |
# | Zoning Bylaw geometry | `fixa-tstc` | land-use categories, set-aside layer |
# | Road network | `9j8t-zm52` | centreline segments |
# | Fire response events / stations | `7hsn-idqi` / `b4y7-zhnz` | |
# | Utility tariffs | EPCOR bylaw schedules | year-pinned JSON in `data/` |
#
# A weekly GitHub Action re-downloads everything, re-runs the pipeline, runs
# this page and the Money lens notebook, and redeploys — with guards that hold
# the last good data (and show a banner) if the assessment year rolls over or a
# download is truncated. (`docs/SPEC_deployment.md`)

# %%
md(f"""
This week's vintages, from the site's own manifest: roll **{status.get('data_year')}**,
rates **{status.get('rate_year')}**, zoning **{status.get('zoning_year')}**;
data last checked **{status.get('last_checked')}**.
""")

# %% [markdown]
# ## 8. Known limitations
#
# 1. **Exempt institutional land is invisible to the roll** (§3) — the biggest
#    structural understatement, measured but not correctable.
# 2. **One coordinate per account** — a large property's dollars pin to a
#    single point on the grid; the lot-acre denominator is the counterweight.
# 3. **Lot sizes are City-supplied, not clipped to neighbourhood boundaries** —
#    the known bound violations (§2) are reported, not hidden.
# 4. **Utility figures are models** with stated assumptions and published
#    validation ratios; they are order-of-magnitude tools, not bills.
# 5. **Neighbourhood aggregation** smooths variation within a neighbourhood;
#    the 100 m grid is the partial remedy, parcel-level analysis the future one
#    (`docs/PARCEL_LEVEL_OPPORTUNITIES.md`).
#
# ## What this page cites rather than recomputes
#
# These rest on one-off investigations, so they are cited without a number
# rather than quoted from a run that no longer exists:
#
# - the lot-dedupe threshold's insensitivity range — `docs/FINDINGS_lot_dedupe.md`;
# - the count of neighbourhoods with substantial untaxed institutional land —
#   `docs/FINDINGS_exempt_institutional.md`;
# - the utility models' validation ratios against EPCOR's published revenue —
#   `docs/FINDINGS_utility_validation.md`;
# - the colour-clamp percentiles and skew tests — `docs/FINDINGS_revenue_scale.md`.

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
