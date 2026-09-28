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
# # The Roads lens, end to end
#
# The Services view on [the map](https://peterfriedrich.github.io/edmonton-tax-viz/)
# shows **road metres per acre**: the length of City-maintained collector and
# local road in each neighbourhood, divided by its area. It then prices those
# metres two ways, as a lifecycle cost and as an operating cost. This page
# re-runs that chain on this week's data, from the City's road centrelines to
# the figures the site is about to serve, and checks that each step agrees
# with the next.
#
# The same rules as [the Money lens page](01_money_lens.html) apply. **No
# number below is typed by hand.** The checks assert things that must hold for
# any data, not values. The one exception is the citywide length band, which
# is explained where it is checked.

# %%
import json
import logging
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from IPython.display import Markdown, display


# Same root resolution as 01–03: nbconvert's cwd is the build dir, so the runner
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


def check(ok: bool, claim: str, detail: str = "") -> None:
    """Record an invariant. Reported together at the end; never stops the run."""
    CHECKS.append((bool(ok), claim, detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {claim}{'  — ' + detail if detail else ''}")


def md(text: str) -> None:
    # A pair of bare `$` reads as TeX math delimiters in the renderer.
    display(Markdown(text.replace("$", r"\$")))


SERVED_PATH = REPO_ROOT / "web" / "data" / "neighbourhood_value_per_acre.geojson"


def served_frame(text: str) -> pd.DataFrame:
    return pd.DataFrame([f["properties"] for f in json.loads(text)["features"]])


served = served_frame(SERVED_PATH.read_text())
status = json.loads((REPO_ROOT / "web" / "data" / "status.json").read_text())
print(f"served data generated: {status.get('generated')}")
print(f"executed:              {datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC}")

# %% [markdown]
# ## 1. Centrelines to road metres per neighbourhood
#
# `load_roads` keeps City-maintained road centrelines, drops alleys, and
# classifies each line. It clips the lines to neighbourhood boundaries and
# drops clipping crumbs under a metre. Road drawn along a boundary shared by
# two or more neighbourhoods is split equally between them. Only collector and
# local road counts. Arterials are shared by the whole city and are left out
# (`docs/SPEC_services.md`).
#
# This runs the pipeline's own function. Two steps inside it are observed
# rather than re-implemented: the clip's own length accounting, read from the
# log record it writes, and the boundary split, wrapped to see what goes in
# and what comes out.

# %%
import load_roads as lr  # noqa: E402
from load_boundaries import load_boundaries  # noqa: E402
from join_and_calculate import load_unit_costs  # noqa: E402


class _Capture(logging.Handler):
    def __init__(self):
        super().__init__(logging.INFO)
        self.records: list[logging.LogRecord] = []

    def emit(self, record):
        self.records.append(record)


cap = _Capture()
lr.logger.addHandler(cap)
lr.logger.setLevel(logging.INFO)
lr.logger.propagate = False  # keep the INFO chatter out of the page

SPLITS: list[tuple[float, float, set]] = []
_split = lr.split_boundary_pieces


def _observed_split(pieces, boundaries, label, tol=lr.BOUNDARY_TOL_M):
    out = _split(pieces, boundaries, label, tol)
    SPLITS.append((float(pieces["piece_m"].sum()), float(out["piece_m"].sum()),
                   set(out["neighbourhood_name"])))
    return out


lr.split_boundary_pieces = _observed_split
try:
    boundaries = load_boundaries(str(main.BOUNDARIES_GEOJSON))
    roads = lr.load_roads(str(main.ROADS_GEOJSON), boundaries)
finally:
    lr.split_boundary_pieces = _split
    lr.logger.removeHandler(cap)
    lr.logger.propagate = True

cons = [r for r in cap.records if str(r.msg).startswith("Road length conservation")]
check(len(cons) == 1, "the clip reported its length accounting exactly once", f"{len(cons)} record(s)")
km_in, km_assigned, km_outside, pct_outside = cons[0].args if cons else (np.nan,) * 4

metric_km = roads["road_m_total"].sum() / 1000
unknown_km = roads["road_m_unknown"].sum() / 1000
md(f"""
- **{km_in:,.1f} km** of City road (alleys out) went into the clip.
- **{km_assigned:,.1f} km** landed inside a neighbourhood and **{km_outside:,.1f} km
  ({pct_outside:.2f}%)** lies outside every boundary.
- Of what landed, **{metric_km:,.1f} km** is collector and local road: the metric.
  **{roads['road_m_arterial'].sum() / 1000:,.1f} km** is arterial, kept out of it.
- **{unknown_km:,.3f} km** carries a road class the pipeline does not recognise.
  It is held out of the metric rather than guessed at.
""")

# %% [markdown]
# **The clip cannot create road.** The boundary polygons touch and in two
# places overlap slightly, so a line on a shared edge could land in both. The
# pipeline's own warning only fires when road goes *missing*; a double count
# would make that warning look healthier. So this checks the other direction.
#
# **Almost all road lands in a neighbourhood.** What falls outside is road
# beyond the mapped neighbourhoods, and 1% is several times what it has been.
# A larger share means the boundaries or the feed moved.

# %%
check(km_assigned <= km_in + 1e-6, "clipping to neighbourhoods adds no road length",
      f"{km_assigned:,.3f} km out of {km_in:,.3f} km in")
check(pct_outside < 1.0, "less than 1% of City road lies outside every neighbourhood",
      f"{pct_outside:.2f}%")

# %% [markdown]
# **The boundary split conserves length.** A shared piece is replaced by k
# equal parts, one per neighbourhood whose edge it runs along, so the total
# before and after must match to rounding, and every neighbourhood it hands
# road to must be one from the boundary file.

# %%
check(len(SPLITS) == 1, "load_roads split the boundary pieces exactly once", f"{len(SPLITS)} call(s)")
m_in, m_out, names_out = SPLITS[0] if SPLITS else (np.nan, np.nan, set())
check(abs(m_in - m_out) < 1e-3, "the boundary split conserves metric road length",
      f"{m_in / 1000:,.4f} km in, {m_out / 1000:,.4f} km out")
unknown_sharers = names_out - set(boundaries["neighbourhood_name"])
check(not unknown_sharers, "every neighbourhood the split hands road to is a real neighbourhood",
      f"{len(unknown_sharers)} unknown")
check(abs(metric_km * 1000 - m_out) < 1e-3, "the per-neighbourhood totals add up to what the split produced",
      f"{metric_km:,.4f} km")

# %% [markdown]
# **The citywide total sits in a plausible band.** This is the one value
# check on the page. Edmonton's collector and local network grows by about a
# percent a year, and it measured 3,655 km on 2026-09-28. The band is wide
# enough for years of growth. Outside it, the feed has lost or duplicated a
# large share of the network, and a per-neighbourhood check could not tell.

# %%
BAND_KM = (3_200, 4_400)
check(BAND_KM[0] <= metric_km <= BAND_KM[1],
      f"citywide collector + local road is within {BAND_KM[0]:,}–{BAND_KM[1]:,} km",
      f"{metric_km:,.1f} km")

# %% [markdown]
# ## 2. Road metres to road metres per acre
#
# `join_and_calculate` divides each neighbourhood's road metres by its
# boundary area in acres. A neighbourhood with no collector or local road gets
# 0, not a blank. This rebuilds that division from step 1 and compares it with
# the served file, neighbourhood by neighbourhood.

# %%
rebuilt = (boundaries[["neighbourhood_name", "area_acres"]]
           .merge(roads[["neighbourhood_name", "road_m_total"]], on="neighbourhood_name", how="left")
           .fillna({"road_m_total": 0.0}))
rebuilt["rebuilt"] = rebuilt["road_m_total"] / rebuilt["area_acres"]
cmp = served[["neighbourhood_name", "road_m_per_acre"]].merge(
    rebuilt, on="neighbourhood_name", how="outer", indicator=True)

only_served = cmp.loc[cmp["_merge"] == "left_only", "neighbourhood_name"].tolist()
only_boundary = sorted(cmp.loc[cmp["_merge"] == "right_only", "neighbourhood_name"])
check(not only_served, "every served neighbourhood is in the boundary file", f"{len(only_served)} not")
check(served["road_m_per_acre"].notna().all(), "every served neighbourhood has a road figure",
      f"{int(served['road_m_per_acre'].isna().sum())} blank")

both = cmp[cmp["_merge"] == "both"]
err = (both["road_m_per_acre"] - both["rebuilt"]).abs()
check(err.max() < 1e-3, "served road metres per acre equals the rebuild, every neighbourhood",
      f"{len(both)} neighbourhoods, max difference {err.max():.2e}")
if only_boundary:
    print(f"in the boundary file but not served (no assessment data; data/DATA.md): {', '.join(only_boundary)}")

# %% [markdown]
# ## 3. The map's colour matches the panel's number
#
# The road network on the map is a separate, much smaller file
# (`roads.geojson`). Each neighbourhood's roads carry a value `v` that drives
# their colour. It is computed from the same pieces with the same boundary
# split, but without the one-metre crumb floor and rounded to one decimal.
# The code bounds that difference at 0.1 m/acre. Without the split it
# disagreed by up to 20%, so a split that drifts out of step shows up here.

# %%
web = pd.DataFrame([f["properties"] for f in json.loads(
    (REPO_ROOT / "web" / "data" / "roads.geojson").read_text())["features"]])
acc = web[web["t"] == "access"].merge(served[["neighbourhood_name", "road_m_per_acre"]],
                                     left_on="n", right_on="neighbourhood_name", how="left")
verr = (acc["v"] - acc["road_m_per_acre"]).abs()
# A boundary with no assessment data (DATA.md: LEWIS FARMS) is not served, but
# the road layer is clipped to every boundary, so its roads are still drawn.
drawn_unserved = sorted(acc.loc[acc["road_m_per_acre"].isna(), "n"])
check(set(drawn_unserved) <= set(only_boundary),
      "every coloured neighbourhood on the map is served, or is a boundary the site does not serve",
      f"drawn but not served: {', '.join(drawn_unserved) or 'none'}")
check(verr.max() <= 0.15, "the map's colour value matches served road metres per acre within 0.15",
      f"{len(acc)} neighbourhoods drawn, max difference {verr.max():.3f}")

# %% [markdown]
# ## 4. Road metres per acre to dollars per acre
#
# The panel prices the same metres on two bases that must never be added
# together (`data/city_unit_costs.json`, "_two_bases"): a lifecycle rate
# (operate, maintain and renew over a 50-year life) and an operating rate
# (maintenance and snow clearing only). Each served cost column should be the
# served length times the configured rate, with rounding the only difference.

# %%
rates = load_unit_costs(main.UNIT_COSTS_JSON)
md(f"Configured rates this run: lifecycle **${rates['road_dollars_per_m']:,.2f}** and "
   f"operating **${rates['road_ops_dollars_per_m']:,.2f}** per road-metre per year.")
for col, key, label in (("cost_roads_life_per_acre", "road_dollars_per_m", "lifecycle"),
                        ("cost_roads_ops_per_acre", "road_ops_dollars_per_m", "operating")):
    want = served["road_m_per_acre"] * rates[key]
    rel = ((served[col] - want).abs() / want.where(want > 0)).max()
    zero_ok = (served.loc[want == 0, col] == 0).all()
    check(rel < 1e-4 and zero_ok, f"served {label} cost per acre = road metres per acre × the configured rate",
          f"max relative difference {rel:.1e}")

# %% [markdown]
# ## 5. What moved since the last published run
#
# Nothing else reads road figures between weekly refreshes. Before this page,
# a boundary redraw or a feed defect that moved road length would have
# published with no signal. The table compares this run with the last
# committed one. **It never fails the page**: roads get built. It is here so
# the moves are seen.

# %%
try:
    prev = served_frame(subprocess.run(
        ["git", "show", "HEAD:web/data/neighbourhood_value_per_acre.geojson"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True).stdout)
except (subprocess.CalledProcessError, OSError, ValueError, KeyError) as e:
    prev = None
    md(f"No previous run to compare with ({type(e).__name__}).")

if prev is not None:
    d = served[["neighbourhood_name", "road_m_per_acre"]].merge(
        prev[["neighbourhood_name", "road_m_per_acre"]], on="neighbourhood_name",
        how="outer", suffixes=("", "_prev"))
    d["change"] = (d["road_m_per_acre"] - d["road_m_per_acre_prev"]) / d["road_m_per_acre_prev"]
    moved = d[d["change"].abs() > 0.05].sort_values("change", key=abs, ascending=False)
    new_or_gone = d[d["road_m_per_acre"].isna() | d["road_m_per_acre_prev"].isna()]
    md(f"**{int((d['change'].abs() > 0.01).sum())}** neighbourhoods moved by more than 1% and "
       f"**{len(moved)}** by more than 5%. "
       f"**{len(new_or_gone)}** appear in only one of the two runs.")
    if len(moved):
        md("| neighbourhood | last run | this run | change |\n|---|---|---|---|\n" + "\n".join(
            f"| {r.neighbourhood_name} | {r.road_m_per_acre_prev:.2f} | {r.road_m_per_acre:.2f} | {r.change:+.1%} |"
            for r in moved.head(15).itertuples()))

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
