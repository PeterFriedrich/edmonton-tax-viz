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
# # The main assumptions, and how big each one is
#
# [Methods & definitions](02_methods.html) says how each number on
# [the map](https://peterfriedrich.github.io/edmonton-tax-viz/) is built and
# lists its known limitations. This page **sizes** them: for each assumption a
# public lens makes, how much of the levy, land, homes or records it touches
# this week.
#
# The same rules as the other two pages apply. **No number below is typed by
# hand**: each is recomputed from this week's data. The table is **sorted by
# the computed size**, so its order can change from week to week. The checks at
# the end assert that each size could be computed and that two measures of the
# same thing agree. They never fail because a size moved.
#
# ⚠️ The sizes are not on one scale. "30% of recent homes" and "8% of the
# levy" have different denominators. The ranking tells you what to read first,
# not which assumption matters more.

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


# Same root resolution as 01/02: nbconvert's cwd is the build dir, so the runner
# passes the root; the cwd search is for running interactively.
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

logging.basicConfig(stream=sys.stdout, level=logging.WARNING, format="%(name)s: %(message)s")

CHECKS: list[tuple[bool, str, str]] = []
ROWS: list[dict] = []


def check(ok: bool, claim: str, detail: str = "") -> None:
    """Record an invariant. Reported together at the end; never stops the run."""
    CHECKS.append((bool(ok), claim, detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {claim}{'  — ' + detail if detail else ''}")


def row(lens: str, assumption: str, share: float, of_what: str, direction: str, where: str) -> None:
    ROWS.append(dict(lens=lens, assumption=assumption, share=float(share),
                     of_what=of_what, direction=direction, where=where))
    print(f"  {share:6.1%}  {lens}: {assumption}")


def md(text: str) -> None:
    # A pair of bare `$` reads as TeX math delimiters in the renderer.
    display(Markdown(text.replace("$", r"\$")))


WEB_DATA = REPO_ROOT / "web" / "data"
served = pd.DataFrame([f["properties"] for f in json.loads(
    (WEB_DATA / "neighbourhood_value_per_acre.geojson").read_text())["features"]])
status = json.loads((WEB_DATA / "status.json").read_text())
dev = json.loads((WEB_DATA / "dev_grid.json").read_text())
temporal = json.loads((WEB_DATA / "temporal.json").read_text())

print(f"roll year / rate year: {status.get('data_year')} / {status.get('rate_year')}")
print(f"served data generated: {status.get('generated')}")
print(f"executed:              {datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC}")

# %% [markdown]
# ## Loading the roll once
#
# The levy-based rows need the per-property roll, the zone code each property
# falls in (the same point-in-polygon join the pipeline makes), and the
# roll's own property-information fields. These are the pipeline's loaders,
# not re-implementations.

# %%
import geopandas as gpd  # noqa: E402
from load_assessment import load_assessment  # noqa: E402
from apply_tax_rates import apply_tax_rates  # noqa: E402
from revenue_by_zone import property_zone_codes  # noqa: E402
from load_zoning import EXEMPT_CANDIDATE_ZONES  # noqa: E402

roll = apply_tax_rates(load_assessment(str(main.ASSESSMENT_CSV)),
                       main.MILL_RATES_JSON, main.ASSESSMENT_YEAR)
roll["zone"] = property_zone_codes(roll, gpd.read_file(str(main.ZONING_GEOJSON)))
info = (pd.read_csv(main.PROPERTY_INFO_CSV, usecols=["Account Number", "zoning", "lot_size"])
          .rename(columns={"Account Number": "account_number", "zoning": "roll_zoning"})
          .drop_duplicates("account_number"))
roll = roll.merge(info, on="account_number", how="left")
LEVY, NONRES = roll["levy"].sum(), roll["nonres_levy"].sum()
print(f"properties: {len(roll):,}   levy ${LEVY / 1e9:,.2f}B   non-res ${NONRES / 1e9:,.2f}B")

# %% [markdown]
# ## Money and Glass
#
# **Exempt-candidate land is counted as billed.** The roll computes a levy for
# parcels on zoning where many properties are tax-exempt (`AJ`, `UF`, `UI`,
# `PU`, `PS`). Edmonton publishes no per-parcel exemption status, so the map
# cannot tell which of those dollars are real. Where they aren't, the figure
# is overstated. The map bands the hoods where this is large
# (`docs/FINDINGS_exempt_institutional.md`,
# `docs/FINDINGS_blurb_claims.md` §6).

# %%
cand = roll["zone"].isin(EXEMPT_CANDIDATE_ZONES)
exempt_total = roll.loc[cand, "levy"].sum() / LEVY
exempt_nonres = roll.loc[cand, "nonres_levy"].sum() / NONRES
row("Money (non-residential)", "levy on exempt-candidate zoning is counted as paid",
    exempt_nonres, "of non-residential levy", "may overstate",
    "FINDINGS_blurb_claims.md §6")
row("Money (total)", "levy on exempt-candidate zoning is counted as paid",
    exempt_total, "of total levy", "may overstate", "FINDINGS_exempt_institutional.md")

served_exempt = (served["rev_frac_exempt"].fillna(0) * served["total_revenue"].fillna(0)).sum() \
    / served["total_revenue"].sum()
check(abs(served_exempt - exempt_total) < 0.005,
      "the served per-hood exempt share rebuilds the citywide share recomputed from the roll",
      f"served {served_exempt:.2%} vs roll {exempt_total:.2%}")

# %% [markdown]
# **Zone shares come from the bylaw map, not the roll's own zoning field.**
# The roll carries a `zoning` field, but it is blank on a large share of
# parcels, and those parcels sit disproportionately on institutional zones.
# Reading it would halve the exempt-candidate share above. The pipeline places
# every property in a bylaw polygon instead. This row sizes what the roll field
# would have missed. It is not a bias on the map.

# %%
blank = roll["roll_zoning"].isna()
row("Money / Glass", "zone shares use the bylaw map; the roll's own zoning field is blank here",
    roll.loc[blank, "nonres_levy"].sum() / NONRES, "of non-residential levy",
    "none on the map (instrument choice)", "FINDINGS_blurb_claims.md §6")

# %% [markdown]
# **The lot-acre denominator counts only parcelled land.** Roads and
# unparcelled valley drop out of it, so a hood reads higher per lot acre
# than per acre. The size is the unparcelled share of the median
# neighbourhood's land.

# %%
pf = served.loc[~served["is_set_aside"].fillna(False).astype(bool), "parcel_frac"].dropna()
row("Money (lot acres)", "the lot-acre denominator leaves out roads and unparcelled land",
    1 - pf.clip(upper=1).median(), "of the median hood's land", "raises per-lot-acre figures",
    "Methods §1")

# %% [markdown]
# **Set-aside neighbourhoods are grey, off the scale.** Their revenue is real,
# but they are not ranked (Methods §3).

# %%
aside = served["is_set_aside"].fillna(False).astype(bool)
row("Money", f"{int(aside.sum())} set-aside neighbourhoods are greyed, not ranked",
    served.loc[aside, "total_revenue"].sum() / served["total_revenue"].sum(),
    "of total levy", "none (excluded from the scale, not the totals)", "FINDINGS_revenue_scale.md")

# %% [markdown]
# **Glass pins each account to one point.** A property bigger than a grid cell
# puts all its dollars in one cell. The lot-acre toggle is the counterweight.

# %%
cell_m2 = main.GRID_CELL_M ** 2
big = roll["lot_size"] > cell_m2
row("Glass", f"one point per account; the lot is bigger than a {main.GRID_CELL_M:.0f} m cell",
    roll.loc[big, "levy"].sum() / LEVY, "of total levy", "concentrates dollars in one cell",
    "Methods §4")

# %% [markdown]
# **Split-class percentages are billed as stated.** A few properties' class
# percentages do not sum to 100. The pipeline bills them as written rather than
# inventing where the missing share belongs.

# %%
pct = sum(pd.to_numeric(roll[f"assessment_class_pct_{i}"], errors="coerce").fillna(0) for i in (1, 2, 3))
off = (pct - 100).abs() > 0.01
row("Money", f"{int(off.sum())} properties' class percentages don't sum to 100",
    roll.loc[off, "levy"].sum() / LEVY, "of total levy", "either way, billed as stated",
    "src/apply_tax_rates.py")

# %% [markdown]
# ## Development
#
# **The grid shows only permits with a location.** The neighbourhood view counts
# every permit. The grid can place only the geocoded ones. The gap is mostly
# recent permits not yet geocoded, plus older apartment permits that never were,
# so the grid under-places dense growth (`docs/FINDINGS_blurb_claims.md` F4).

# %%
cols = dev["columns"]
for window, suffix, label in (("3yr", "_3yr", "3 years"), ("5yr", "", "5 years"),
                              ("long", "_long", "since 2009")):
    cov = dev["coverage"][window]
    i = cols.index("units" + suffix)
    check(sum(c[i] for c in dev["cells"]) == cov["units_geocoded"],
          f"grid cells hold exactly the geocoded units ({label})", f"{cov['units_geocoded']:,}")
    row("Development (grid)", f"homes permitted in the last {label} with no location are off the grid"
        if window != "long" else "homes permitted since 2009 with no location are off the grid",
        1 - cov["units_geocoded"] / cov["units"], f"of new homes ({label})",
        "grid under-places them; the neighbourhood view counts them", "FINDINGS_blurb_claims.md F4")

# %% [markdown]
# ## Change over time
#
# **Two roll years are omitted.** The historical file's 2024 and 2025 slices are
# proven incomplete, so the published series skips them
# (`docs/SPEC_temporal.md` §0).

# %%
years = temporal["years"]
span = max(years) - min(years) + 1
missing = sorted(set(range(min(years), max(years) + 1)) - set(years))
check(not set(map(int, temporal.get("defect_accounts", []))) & set(years),
      "no year with a defective slice is published", f"omitted: {missing}")
row("Change over time", f"roll years {', '.join(map(str, missing))} are omitted",
    len(missing) / span, f"of the {min(years)}–{max(years)} years", "changes span the gap",
    "SPEC_temporal.md §0")

# %% [markdown]
# ## Roads
#
# **Arterials are left out of road metres.** Every kind of development shares
# them, so they are not charged to the neighbourhood they cross.

# %%
from load_boundaries import load_boundaries  # noqa: E402
from load_roads import load_roads  # noqa: E402

roads = load_roads(str(main.ROADS_GEOJSON), load_boundaries(str(main.BOUNDARIES_GEOJSON)))
art = roads["road_m_arterial"].sum()
row("Roads", "arterial roads are left out of road metres",
    art / (art + roads["road_m_total"].sum()), "of classified centreline length",
    "lowers road metres where arterials run", "DECISIONS.md 2026-07-01")

# %% [markdown]
# ## The table, largest first

# %%
t = pd.DataFrame(ROWS).sort_values("share", ascending=False)
check(t["share"].between(0, 1).all() and t["share"].notna().all(),
      "every size computed and lies in [0, 1]", f"{len(t)} rows")
md("| size | of what | lens | assumption | effect | argued in |\n|---|---|---|---|---|---|\n" + "\n".join(
    f"| **{r.share:.1%}** | {r.of_what} | {r.lens} | {r.assumption} | {r.direction} | `{r.where}` |"
    for r in t.itertuples()))

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
