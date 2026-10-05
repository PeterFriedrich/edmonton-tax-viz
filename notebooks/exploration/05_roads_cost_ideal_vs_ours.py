# ---
# jupyter:
#   title: Pricing Edmonton's neighbourhood roads, the ideal method against ours
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
# # Pricing Edmonton's neighbourhood roads: the ideal method, and where ours falls short
#
# The Services view prices each neighbourhood's roads two ways: a **lifecycle**
# cost ($50 per road-metre per year) and an **operating** cost ($9.32). This
# notebook starts from what an ideal calculation of that cost would need, and
# takes the parts one at a time: what the ideal needs, what the pipeline does,
# and what the difference does to the number.
#
# **What is recomputed and what is not.** Everything that can be derived from
# this repo is recomputed here, with the pipeline's own loaders: road length by
# class, the boundary split, the served cost columns, the reconstruction
# cross-check from the capital budget, and the per-dwelling figures. City
# figures that only exist in PDFs (the 2020 *Infrastructure State and
# Condition* Appendix A, the FY2023 financial statements' Schedule 1, the
# *Development Impact on Infrastructure* page) are transcribed as constants,
# with their source beside them. The operating budget is fetched live from
# `budget.edmonton.ca`.
#
# The argument behind each section lives in a `docs/FINDINGS_*.md` file, named
# in the section. This page recomputes the numbers; it does not re-argue them.
#
# ## Reproducing
#
# Run from inside the repo with the project's `.venv`. It reads `data/raw/`
# (roads, boundaries, the two roll CSVs) and the served
# `web/data/neighbourhood_value_per_acre.geojson`, so the figures move with the
# data. From this server, HTTPS needs `certifi`; the fetch below passes it.

# %%
import io
import json
import logging
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import certifi
import geopandas as gpd
import numpy as np
import pandas as pd
import requests
from IPython.display import Markdown, display
from scipy.stats import spearmanr


def _find_root() -> Path:
    env = os.environ.get("EDMONTON_REPO_ROOT")
    if env:
        return Path(env).resolve()
    here = Path.cwd()
    for p in (here, *here.parents):
        if (p / "src" / "join_and_calculate.py").exists():
            return p
    raise RuntimeError("cannot locate the repo root; set EDMONTON_REPO_ROOT or run inside the repo")


REPO_ROOT = _find_root()
sys.path.insert(0, str(REPO_ROOT))
import main  # noqa: E402  (import-safe; puts src/ on the path)

import load_roads as lr  # noqa: E402
from load_boundaries import load_boundaries  # noqa: E402

logging.basicConfig(stream=sys.stdout, level=logging.WARNING, format="%(name)s: %(message)s")

CHECKS: list[tuple[bool, str, str]] = []


def check(ok: bool, claim: str, detail: str = "") -> None:
    """Record whether a claim the report makes still holds on this data."""
    CHECKS.append((bool(ok), claim, detail))
    print(f"  [{'HOLDS' if ok else 'CHANGED'}] {claim}{'  — ' + detail if detail else ''}")


def md(text: str) -> None:
    # A pair of bare `$` reads as TeX math delimiters in the renderer.
    display(Markdown(text.replace("$", r"\$")))


def table(df: pd.DataFrame) -> None:
    # Hand-built rather than DataFrame.to_markdown, which needs `tabulate` (not in the venv).
    fmt = lambda v: f"{v:,.2f}".rstrip("0").rstrip(".") if isinstance(v, float) else str(v)  # noqa: E731
    lines = ["| " + " | ".join(map(str, df.columns)) + " |", "|" + "---|" * len(df.columns)]
    lines += ["| " + " | ".join(fmt(v) for v in row) + " |" for row in df.itertuples(index=False)]
    md("\n".join(lines))


served = pd.DataFrame([f["properties"] for f in json.loads(
    (REPO_ROOT / "web/data/neighbourhood_value_per_acre.geojson").read_text())["features"]])
status = json.loads((REPO_ROOT / "web/data/status.json").read_text())
unit_costs = json.loads(main.UNIT_COSTS_JSON.read_text())
roads_mtime = datetime.fromtimestamp(main.ROADS_GEOJSON.stat().st_mtime, timezone.utc)

print(f"served data generated:   {status.get('generated')}")
print(f"data/raw/roads.geojson:  {roads_mtime:%Y-%m-%d}")
print(f"executed:                {datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC}")

# %% [markdown]
# ## The ideal calculation
#
# The question: what does it cost the City, per year, to keep the roads that
# serve each neighbourhood? Annual, so it can sit beside the municipal tax the
# neighbourhood pays; per acre, so neighbourhoods of different sizes compare.
# With unlimited data the calculation would have eight parts:
#
# 1. **An inventory of every segment** the City maintains: class, length,
#    width or lane count, surface, age, condition.
# 2. **A rule for which roads belong to a neighbourhood**: every road the City
#    pays for, with shared roads such as arterials divided by who uses them.
# 3. **An allocation of each segment** to the land it serves, ideally the
#    parcels that front it.
# 4. **A lifecycle cost per segment**: the treatments its class gets, what
#    each costs, and when each falls due given its condition.
# 5. **A service life** measured as the interval at which that class is
#    actually reconstructed under that treatment schedule.
# 6. **An operating cost per segment**: actual annual maintenance and snow
#    clearing, by class, in current dollars.
# 7. **One dollar-year and one basis**, so every cost is counted once.
# 8. **A check against real money**: citywide totals that reconcile to the
#    City's roads spending, and per-neighbourhood figures that match observed
#    spending where the City has rebuilt.
#
# Sections 1 to 8 below take these in order; section 9 is what the result can
# and cannot show on a map.

# %% [markdown]
# ## 1. The inventory: centreline length, without width, age or condition
#
# **Ideal:** every segment with its width, age and condition. **Ours:** the
# City's centreline feed (`9j8t-zm52`), which gives each segment's length and
# functional class and nothing else. The City publishes age and condition
# only as class totals, in its *Infrastructure State and Condition* reports.
# (`docs/FINDINGS_road_figures_consolidation.md` L2b,
# `docs/FINDINGS_road_class_inventory.md`)

# %%
raw = gpd.read_file(main.ROADS_GEOJSON).to_crs(epsg=3400)
raw["km"] = raw.geometry.length / 1000

city_road = raw[(raw["centerline_type"] == lr.CENTERLINE_TYPE)
                & (raw["responsible_party_description"] == lr.RESPONSIBLE_PARTY)].copy()
city_road["group"] = city_road["functional_class_code"].map(lr.CLASS_GROUP).fillna(lr.DEFAULT_GROUP)
by_class = city_road.groupby("group")["km"].sum()
alley_km = raw.loc[raw["centerline_type"] == "Alley", "km"].sum()
city_road_km = by_class.drop("alley", errors="ignore").sum()

table(pd.DataFrame({
    "population": ["City road: arterial", "City road: collector", "City road: local",
                   "City road: alley-classed", "City road: unknown class", "**City road, all classes**",
                   "Alleys (centreline type Alley)"],
    "centreline km": [by_class.get(g, 0.0) for g in ("arterial", "collector", "local", "alley", "unknown")]
                     + [city_road_km, alley_km],
}).round(1))

# %% [markdown]
# **What the feed cannot say.** Nothing in it distinguishes a wide collector
# from a narrow local street, or a 1960s road in poor shape from a new one. The
# only class-level cost signal is the City's 2020 Appendix A, transcribed here
# (p31; obtained via the Internet Archive, `FINDINGS_road_class_inventory.md`
# §0).

# %%
# City of Edmonton, 2020 Infrastructure State and Condition, Appendix A, p31.
# lane_km, average age, expected asset life (yrs), condition (A+B, C, D+F %), replacement value ($M)
APP_A = pd.DataFrame([
    ("Major Arterial",  596.2,   30, 22, (78, 20, 2),  711),
    ("Minor Arterial",  2927.2,  48, 22, (53, 40, 7),  2914),
    ("Local Roads",     4830.30, 38, 28, (70, 17, 13), 3461),
    ("Collector Roads", 1763.10, 35, 20, (62, 34, 5),  1888),
    ("Alleys",          1192.7,  30, 28, (20, 16, 64), 501),
], columns=["class", "lane_km", "avg_age", "life", "condition", "value_m"]).set_index("class")

per_lane_km = APP_A["value_m"] / APP_A["lane_km"]
coll_premium = per_lane_km["Collector Roads"] / per_lane_km["Local Roads"]
coll_value_share = APP_A.loc["Collector Roads", "value_m"] / APP_A.loc[["Collector Roads", "Local Roads"], "value_m"].sum()

md(f"""
- A collector lane-km carries **{coll_premium:.2f}×** the replacement value of a
  local one (${per_lane_km['Collector Roads']:.3f}M vs ${per_lane_km['Local Roads']:.3f}M).
- Collectors are **{coll_value_share:.0%}** of the City's collector + local
  replacement value. Their share of the length *this project charges* is in
  section 2.
- **Effect:** one rate per metre understates collector-heavy neighbourhoods.
  The lifecycle rate's own config calls it "a mild lower bound for the
  collector share".
""")
check(1.45 <= coll_premium <= 1.55, "a collector lane-km is ~1.49× a local one in replacement value",
      f"{coll_premium:.3f}×")

# %% [markdown]
# ## 2. Which roads count: collector and local only
#
# **Ideal:** every road the City pays for, arterials shared by use. **Ours:**
# City-maintained collector and local road only. Arterials are excluded as
# citywide infrastructure, alleys by the alleys-out decision, and private roads
# carry no City centreline (`docs/SPEC_services.md`, `DECISIONS.md`
# 2026-07-01). This runs the pipeline's own `load_roads`, observing its clip
# and its boundary split.

# %%
class _Capture(logging.Handler):
    def __init__(self):
        super().__init__(logging.INFO)
        self.records = []

    def emit(self, record):
        self.records.append(record)


cap = _Capture()
lr.logger.addHandler(cap)
lr.logger.setLevel(logging.INFO)
lr.logger.propagate = False

SPLIT_INPUT: list[gpd.GeoDataFrame] = []
_split = lr.split_boundary_pieces


def _observed_split(pieces, boundaries, label, tol=lr.BOUNDARY_TOL_M):
    SPLIT_INPUT.append(pieces.copy())
    return _split(pieces, boundaries, label, tol)


lr.split_boundary_pieces = _observed_split
try:
    boundaries = load_boundaries(str(main.BOUNDARIES_GEOJSON))
    roads = lr.load_roads(str(main.ROADS_GEOJSON), boundaries)
finally:
    lr.split_boundary_pieces = _split
    lr.logger.removeHandler(cap)
    lr.logger.propagate = True

cons = [r for r in cap.records if str(r.msg).startswith("Road length conservation")][0]
km_in, km_assigned, km_outside, pct_outside = cons.args

metric_km = roads["road_m_total"].sum() / 1000
collector_km = roads["road_m_collector"].sum() / 1000
local_km = roads["road_m_local"].sum() / 1000
arterial_km = roads["road_m_arterial"].sum() / 1000
art_lane_share = APP_A.loc[["Major Arterial", "Minor Arterial"], "lane_km"].sum() / \
    APP_A.loc[["Major Arterial", "Minor Arterial", "Local Roads", "Collector Roads"], "lane_km"].sum()

md(f"""
- **Charged (the metric):** {metric_km:,.1f} km, of which collector
  {collector_km:,.1f} km (**{collector_km / metric_km:.0%}** of the length,
  against {coll_value_share:.0%} of the replacement value) and local {local_km:,.1f} km.
- **Arterials, excluded:** {arterial_km:,.1f} km of centreline inside
  neighbourhoods; **{art_lane_share:.1%}** of the City's road lane-km (Appendix A).
- **Alleys, excluded:** {alley_km:,.0f} km. In Appendix A they are the class in
  the worst condition: **{APP_A.loc['Alleys', 'condition'][2]}%** poor against
  {APP_A.loc['Local Roads', 'condition'][2]}% for local roads.
- **Unknown class, held out:** {roads['road_m_unknown'].sum() / 1000:,.3f} km.
""")

# %% [markdown]
# **Private roads.** A neighbourhood served by private internal roads has
# dwellings and almost no City road. Per acre that reads as merely low; per
# dwelling it divides by almost nothing (`docs/FINDINGS_road_per_dwelling.md`
# §1). Dwellings come from the pipeline's own dwelling model.

# %%
from load_water import build_connections  # noqa: E402

conn = build_connections(str(main.ASSESSMENT_CSV), str(main.PROPERTY_INFO_CSV))
dwellings = conn.groupby("neighbourhood_name")["units"].sum().rename("dwellings")

hood = (boundaries[["neighbourhood_name", "area_acres"]]
        .merge(roads[["neighbourhood_name", "road_m_total", "road_m_collector", "road_m_local"]],
               on="neighbourhood_name", how="left")
        .fillna({"road_m_total": 0.0, "road_m_collector": 0.0, "road_m_local": 0.0})
        .merge(served, on="neighbourhood_name", how="inner")
        .merge(dwellings, left_on="neighbourhood_name", right_index=True, how="left")
        .fillna({"dwellings": 0}))
hood["is_set_aside"] = hood["is_set_aside"].fillna(False).astype(bool)
hood["road_m_per_dwelling"] = hood["road_m_total"] / hood["dwellings"].where(hood["dwellings"] > 0)

res = hood[hood["is_residential"].fillna(False).astype(bool) & ~hood["is_set_aside"] & (hood["dwellings"] >= 100)]
private = res[res["road_m_per_dwelling"] < 1.0].sort_values("road_m_per_dwelling")
table(private[["neighbourhood_name", "dwellings", "road_m_total", "road_m_per_dwelling"]]
      .rename(columns={"road_m_total": "City road m", "road_m_per_dwelling": "m per dwelling"}).round(2))
check(len(private) >= 3, "a few residential neighbourhoods have dwellings and almost no City road",
      f"{len(private)} under 1 m per dwelling")

# %% [markdown]
# **Effect:** the lens prices the local network a neighbourhood is built
# around, not the City's road bill. That is a deliberate scope; the citywide
# total is not Edmonton's road cost.
#
# ## 3. Assigning road to neighbourhoods: overlay and an equal split
#
# **Ideal:** each segment's cost goes to the parcels that front it. **Ours:**
# centrelines are clipped to boundary polygons, pieces under a metre dropped,
# and a road lying on a boundary shared by k neighbourhoods is split 1/k to
# each (since 2026-09-22; `DECISIONS.md`, `docs/FINDINGS_roads_end_to_end.md`
# §1).

# %%
md(f"""
- **Into the clip:** {km_in:,.1f} km of City road; **{km_outside:,.1f} km
  ({pct_outside:.2f}%)** lies outside every neighbourhood.
""")
check(pct_outside < 1.0, "under 1% of City road falls outside every neighbourhood", f"{pct_outside:.2f}%")

# Which pieces were split, and between whom. This repeats split_boundary_pieces'
# own sharer test on the pieces it was handed, so the shares can be re-weighted.
pieces = SPLIT_INPUT[0].reset_index(drop=True)
rings = gpd.GeoDataFrame({"sharer": boundaries["neighbourhood_name"].values},
                         geometry=boundaries.geometry.boundary.buffer(lr.BOUNDARY_TOL_M).values,
                         crs=boundaries.crs)
hits = gpd.sjoin(pieces[["neighbourhood_name", "geometry"]], rings, predicate="within")[["neighbourhood_name", "sharer"]]
own = hits.index[hits["neighbourhood_name"] == hits["sharer"]].unique()
hits = hits.loc[hits.index.isin(own), ["sharer"]]
k = hits.groupby(level=0).size()
shared = hits.loc[hits.index.isin(k.index[k >= 2])].copy()
shared["piece_m"] = pieces.loc[shared.index, "piece_m"].values
shared["k"] = k.loc[shared.index].values

aside = served.set_index("neighbourhood_name")
shared["sharer_aside"] = shared["sharer"].map(aside["is_set_aside"]).fillna(False).astype(bool)
shared["sharer_reason"] = shared["sharer"].map(aside["set_aside_reason"])
split_km = shared.groupby(level=0)["piece_m"].first().sum() / 1000
md(f"**Split:** {shared.index.nunique():,} pieces, {split_km:,.1f} km of metric road on a shared boundary.")
print("set-aside reasons among sharers:", shared.loc[shared["sharer_aside"], "sharer_reason"].value_counts().to_dict())

# %%
# Road between a published neighbourhood and a set-aside one.
mixed = shared.groupby(level=0).agg(any_aside=("sharer_aside", "any"), all_aside=("sharer_aside", "all"),
                                     piece_m=("piece_m", "first"))
mixed_km = mixed.loc[mixed["any_aside"] & ~mixed["all_aside"], "piece_m"].sum() / 1000

# Variant: a river-valley or park neighbour takes no share; the rest is split
# among the remaining sharers.
RIVER_PARK = {r for r in shared["sharer_reason"].dropna().unique()
              if re.search(r"river|valley|park", str(r), re.I)}
shared["excluded"] = shared["sharer_reason"].isin(RIVER_PARK)
keep_n = shared.groupby(level=0)["excluded"].transform(lambda s: (~s).sum())
shared["share_now"] = shared["piece_m"] / shared["k"]
shared["share_variant"] = np.where(keep_n == 0, shared["share_now"],
                                   np.where(shared["excluded"], 0.0, shared["piece_m"] / keep_n.clip(lower=1)))
delta = shared.groupby("sharer")[["share_now", "share_variant"]].sum()
delta["d_m"] = delta["share_variant"] - delta["share_now"]
cmp = hood.set_index("neighbourhood_name")[["road_m_total", "is_set_aside"]].join(delta["d_m"]).fillna({"d_m": 0.0})
cmp = cmp[~cmp["is_set_aside"] & (cmp["road_m_total"] > 0)]
cmp["change"] = cmp["d_m"] / cmp["road_m_total"]
moved = cmp[cmp["change"].abs() > 1e-9]
big = cmp[cmp["change"].abs() > 0.05].sort_values("change", ascending=False)

md(f"""
- **{mixed_km:,.1f} km** of road lies between a published neighbourhood and a
  set-aside one, and the equal split gives the set-aside side its share.
- If a river-valley or park neighbour ({', '.join(sorted(map(str, RIVER_PARK))) or 'none found'})
  took no share, **{len(moved)}** published neighbourhoods would move,
  **{len(big)}** of them by more than 5%; {delta['d_m'].clip(lower=0).sum() / 1000:,.1f} km returns
  to the developed side.
""")
table(big.reset_index()[["neighbourhood_name", "road_m_total", "change"]]
      .assign(change=lambda d: d["change"].map("{:+.1%}".format)).round(0).head(10))
check(len(big) <= 10, "the river-valley variant moves only a handful of neighbourhoods by over 5%", f"{len(big)}")

# %% [markdown]
# **Effect:** the split is right between two developed neighbourhoods and wrong
# where the other side fronts nothing. This is an open decision (`TODO.md`,
# roads end-to-end follow-ons). A true frontage rule would need parcels.
#
# ## 4. The lifecycle cost: one published figure for every road
#
# **Ideal:** a treatment schedule and cost per class, applied to each segment's
# condition. **Ours:** one figure for "1 kilometre of a typical Edmonton
# neighbourhood road" from the City's *Development Impact on Infrastructure*
# page, spread over 50 years. The page's unit is centreline km, read directly
# on 2026-09-17 (`DECISIONS.md`).

# %%
life = unit_costs["roadway_om_renewal"]
pub = life["source"]["published_figures_per_km_neighbourhood_road"]
OM, RENEW, CAPITAL, LIFE = pub["operate_and_maintain"], pub["renew_and_replace"], pub["initial_capital"], 50
rate_life = (OM + RENEW) / LIFE / 1000
md(f"""
- Operate and maintain **${OM:,.0f}** + renew and replace **${RENEW:,.0f}** per km,
  over {LIFE} years = **${rate_life:.2f}** per metre per year
  (${OM / LIFE / 1000:.0f} upkeep, ${RENEW / LIFE / 1000:.0f} renewal).
- The page's **${CAPITAL:,.0f}** initial construction is not in the rate.
- Shipped value in `city_unit_costs.json`: **${life['value']}**.
""")
check(abs(rate_life - life["value"]) < 1e-9, "the shipped lifecycle rate is the page's two figures over 50 years",
      f"${rate_life:.2f}")

# %% [markdown]
# **Against observed money.** The capital budget lists Neighbourhood Renewal
# profiles by neighbourhood. Dividing a profile's approved total by the
# collector + local metres in its neighbourhood(s) gives an observed
# reconstruction cost per metre (`docs/FINDINGS_nrp_reconstruction_cross_check.md`;
# the matching and the $8M floor are that document's).

# %%
cap_budget = pd.read_csv(REPO_ROOT / "data/capital_budget.csv")
nrp = cap_budget[cap_budget["service"] == "Neighbourhoods"]
road_m = dict(zip(roads["neighbourhood_name"], roads["road_m_total"]))
hoods = set(road_m)


def match(profile: str) -> list[str]:
    up = re.sub(r"^(NRP|NARP)[/A-Z]*\s+RECON\s*-\s*", "", profile.upper())
    for pat in (r"\b(NEIGHBOURHOOD|NEIGHBORHOOD|NBHD)S?\b", r"\b(AND\s+)?ALLEY(S)?\b",
                r"\b(RECONSTRUCTION|RENEWAL|REVITALIZATION|RECON)\b"):
        up = re.sub(pat, "", up)
    found = [h for h in hoods if re.search(r"(?<![A-Z])" + re.escape(h) + r"(?![A-Z])", up)]
    return sorted(h for h in found if not any(h != o and h in o for o in found))


rows = []
for profile, amount in nrp.groupby("profile")["approved"].sum().items():
    m = match(profile)
    if not m or amount < 8e6:
        continue
    metres = sum(road_m[h] for h in m)
    alley_only = "ALLEY" in profile.upper() and "NEIGHBO" not in profile.upper()
    rows.append(dict(profile=profile, scope="alley only" if alley_only else "full",
                     approved=amount, road_m=metres, per_m=amount / metres, hoods=", ".join(m)))
nrp_df = pd.DataFrame(rows)
full = nrp_df[nrp_df["scope"] == "full"]
alley_only = nrp_df[nrp_df["scope"] == "alley only"]
agg_full = full["approved"].sum() / full["road_m"].sum()
agg_alley = alley_only["approved"].sum() / alley_only["road_m"].sum()
published_per_m = RENEW / 1000

table(full.sort_values("per_m")[["hoods", "approved", "road_m", "per_m"]].round(0))
md(f"""
- **{len(full)}** full reconstructions: **${agg_full:,.0f}** per metre in aggregate,
  median **${full['per_m'].median():,.0f}**: **{agg_full / published_per_m:.2f}×** the published
  ${published_per_m:,.0f}. {int((full['per_m'] > published_per_m).sum())} exceed it,
  {int((full['per_m'] > 2 * published_per_m).sum())} exceed twice it.
- Alley-only profiles run ${agg_alley:,.0f} per metre of road; taking that out of the
  full figure still leaves **{(agg_full - agg_alley) / published_per_m:.2f}×**.
- Coverage: {len(set(', '.join(nrp_df['hoods']).split(', ')))} neighbourhoods of {len(served)}.
""")
check(agg_full / published_per_m > 1.3, "observed reconstruction runs well above the published renewal figure",
      f"{agg_full / published_per_m:.2f}×")

# %% [markdown]
# **Effect:** the lifecycle rate is a floor. The cross-check cannot become a
# rate: the budgets also pay for sidewalks, lighting and drainage, and the
# neighbourhoods were chosen because they were due.
#
# ## 5. The service life: 50 years, and why it holds
#
# **Ideal:** the interval at which a neighbourhood road is actually
# reconstructed under the maintenance assumed. **Ours:** 50, from the same page
# ("usually 25, extended to 50 with proper maintenance"). The other City
# figures measure different events (`docs/FINDINGS_roadway_implied_life.md`,
# `docs/FINDINGS_road_class_inventory.md` §4, `docs/FINDINGS_road_life_crossread.md`).

# %%
# FY2023 Consolidated Financial Statements, Schedule 1 (printed p79), $000.
S1_ROADWAY = dict(opening=9_304_626, closing=9_732_383, amortization=255_893)
implied = [S1_ROADWAY["opening"] / S1_ROADWAY["amortization"], S1_ROADWAY["closing"] / S1_ROADWAY["amortization"]]

cl = APP_A.loc[["Local Roads", "Collector Roads"]]
life_lane_km = (cl["lane_km"] * cl["life"]).sum() / cl["lane_km"].sum()
life_our_len = (local_km * cl.loc["Local Roads", "life"] + collector_km * cl.loc["Collector Roads", "life"]) / metric_km
life_by_cost = cl["value_m"].sum() / (cl["value_m"] / cl["life"]).sum()

table(pd.DataFrame([
    ("Expected asset life, collector + local, lane-km weighted", f"{life_lane_km:.1f}", "2020 ISC Appendix A", "when the structure is due for intervention"),
    ("  same, weighted by our charged length", f"{life_our_len:.1f}", "Appendix A × this run", ""),
    ("  same, weighted by replacement cost", f"{life_by_cost:.1f}", "Appendix A", "the right weighting for a $/m/yr charge"),
    ("Implied accounting life, all City roads", f"{implied[0]:.1f}–{implied[1]:.1f}", "FY2023 statements, Schedule 1", "amortization policy, incl. arterials and alleys"),
    ("Life with proper maintenance (used)", "50", "Development Impact page", "neighbourhood road"),
    ("Reconstruction with a treatment schedule", "60", "City staff via Journal of Commerce, 2016 (secondary)", "a forecast for a road rebuilt to 2016 standards"),
], columns=["figure", "years", "source", "what it measures"]))

md(f"""
**Why 50 holds:** the page's renewal cost (${RENEW / 1e6:.1f}M) exceeds its
original build (${CAPITAL / 1e6:.1f}M), which only fits a lifecycle that
includes a replacement-scale event. Spreading that bundle over 25 years charges
for the extension while denying it happens. **What it is worth:** at 25 years
the rate would be **${(OM + RENEW) / 25 / 1000:.0f}** per metre per year.
""")
check(life_by_cost < life_our_len < 28, "every reweighting of the expected life lands in 24–28, cost-weighted lowest",
      f"{life_by_cost:.1f} < {life_our_len:.1f} < 28")

# %% [markdown]
# ## 6. The operating cost: four known errors, mostly pointing low
#
# **Ideal:** actual annual maintenance and snow spend on these roads, by class,
# in current dollars. **Ours:** two citywide figures each divided by "about
# 11,000 km" (`docs/FINDINGS_roadway_maintenance_rate.md`,
# `docs/FINDINGS_road_figures_consolidation.md` L2b). The budget figures are
# fetched live.

# %%
ops = unit_costs["roadway_ops"]
try:
    r = requests.get("https://budget.edmonton.ca/api/operating_budget.csv", timeout=120, verify=certifi.where())
    r.raise_for_status()
    opb = pd.read_csv(io.StringIO(r.text))
    BUDGET_LIVE = True
except requests.RequestException as e:
    opb, BUDGET_LIVE = None, False
    md(f"**Could not fetch the operating budget ({type(e).__name__}); the figures below fall back to the transcribed ones.**")

INVENTORY_KM = 11_000
SNOW_TOTAL, SNOW_ROADS_SHARE = 67_000_000, 0.55   # Taproot; the share is the staffer's
if BUDGET_LIVE:
    maint_2017 = opb.loc[opb["program"].astype(str).str.contains("Roadway Maintenance") & (opb["budget_year"] == 2017), "budget"].sum()
    # Renamed "OPS/PARS - Snow and Ice Control" from 2018, so match on the stem.
    snow_2025 = opb.loc[opb["program"].astype(str).str.contains("Snow and Ice Control")
                        & (opb["budget_year"] == 2025), "budget"].sum()
    branch = opb[opb["branch"].astype(str).str.contains("Parks")].groupby("budget_year")["budget"].sum()
    growth = (branch.loc[2026] / branch.loc[2017], branch.loc[2025] / branch.loc[2017])
else:
    maint_2017, snow_2025, growth = 65_671_000, 67_553_815, (1.2551, 1.3357)

maint_km = maint_2017 / INVENTORY_KM
snow_km = SNOW_TOTAL * SNOW_ROADS_SHARE / INVENTORY_KM
rate_ops = (maint_km + snow_km) / 1000
md(f"""
- Maintenance: FY2017 *Roadway Maintenance* **${maint_2017:,.0f}** ÷ {INVENTORY_KM:,} = **${maint_km:,.0f}** per km.
- Snow: {SNOW_ROADS_SHARE:.0%} of ${SNOW_TOTAL / 1e6:.0f}M ÷ {INVENTORY_KM:,} = **${snow_km:,.0f}** per km.
  The City's FY2025 *Snow and Ice Control* budget is ${snow_2025:,.0f}, so the total is confirmed; the split is not.
- Together **${rate_ops:.2f}** per metre per year; shipped **${ops['value']}**.
""")
check(abs(round(rate_ops, 2) - ops["value"]) < 0.01, "the shipped operating rate is the two citywide figures over 11,000 km",
      f"${rate_ops:.2f}")
check(abs(snow_2025 / SNOW_TOTAL - 1) < 0.02, "the reported $67M snow total matches the City's FY2025 budget",
      f"${snow_2025:,.0f}")

# %%
app_a_inventory = APP_A["lane_km"].sum()
lane_factor = APP_A.loc[["Local Roads", "Collector Roads"], "lane_km"].sum() / metric_km
upper_factor = INVENTORY_KM / city_road_km
ks = [1, 2, 3, 5]
net = {kk: lane_factor / (0.65 + 0.35 * kk) for kk in ks}
k_flip = (lane_factor - 0.65) / 0.35

table(pd.DataFrame([
    ("11,000 km is lane-km incl. alleys (Appendix A totals "
     f"{app_a_inventory:,.1f}), applied to centreline metres",
     "understates", f"{lane_factor:.2f}× best estimate (collector + local lane-km ÷ our km); {upper_factor:.2f}× bound"),
    ("Both halves average in arterials, cleared first and maintained more heavily",
     "overstates", "1 ÷ (0.65 + 0.35k) for an arterial/local cost ratio k; unpublished"),
    ("Maintenance in 2017 dollars, snow in 2025",
     "understates", f"Parks and Roads Services grew {growth[0]:.2f}–{growth[1]:.2f}× since 2017"),
    ("55% roads share of snow rests on one news source", "unknown", "each 5 points moves the rate ~3%"),
], columns=["error", "direction", "size"]))

table(pd.DataFrame({"k (arterial ÷ local cost)": ks, "net factor on the shipped rate": [round(net[kk], 2) for kk in ks]}))
md(f"""
The unit error and the arterial blend combine: the rate stays too low unless
arterials cost more than **{k_flip:.1f}×** a local lane-km to maintain and
clear. On 2026-09-08 the project chose to state the lane-km unit rather than
convert it, and to publish the operating rate as a floor (`DECISIONS.md`).
""")
check(net[3] > 1.0, "the operating rate is still a floor at k = 3", f"{net[3]:.2f}×")

# %% [markdown]
# ## 7. Dollar years, and two bases that must not be added
#
# **Ideal:** one basis, one dollar-year. **Ours:** lifecycle and operating,
# side by side and never summed, because both contain upkeep. Their vintages
# differ (a page last modified in 2024; budgets from 2017 and 2025).

# %%
ratio = life["value"] / ops["value"]
md(f"""
- Median per acre per year across served neighbourhoods: lifecycle
  **${served['cost_roads_life_per_acre'].median():,.0f}**, operating
  **${served['cost_roads_ops_per_acre'].median():,.0f}**.
- The two rates are **{ratio:.1f}×** apart; on one unit (operating × {lane_factor:.2f})
  **{life['value'] / (ops['value'] * lane_factor):.1f}×**.
""")

# %% [markdown]
# ## 8. Checking against real money: only order of magnitude
#
# **Ideal:** the model's totals reconcile to City spending. **Ours:** the
# renewal half set against the City's Neighbourhood Renewal funding
# (`docs/FINDINGS_road_figures_consolidation.md` L1).

# %%
renewal_req = RENEW / LIFE / 1000 * metric_km * 1000
nr_fund = cap_budget[(cap_budget["fund"] == "Neighborhood Renewal Reserve") & cap_budget["fiscal_year"].between(2023, 2026)]
nr_per_year = nr_fund["approved"].sum() / 4
if BUDGET_LIVE:
    nr_levy = opb[(opb["branch"] == "Neighbourhood Renewal")].groupby("budget_year")["budget"].sum()
    levy = nr_levy.loc[2026] if 2026 in nr_levy.index else nr_levy.iloc[-1]
else:
    levy = 174_386_000
ROADS_SHARE_OF_PROJECT = 0.47   # City CEA-2026 slide: roads 47% of a typical project
md(f"""
- Renewal requirement: ${RENEW / LIFE / 1000:.0f}/m × {metric_km:,.0f} km = **${renewal_req / 1e6:,.1f}M** a year.
- Funded: Neighbourhood Renewal levy **${levy / 1e6:,.1f}M** a year (operating budget);
  reserve draws in the capital budget **${nr_per_year / 1e6:,.1f}M** a year over 2023–26.
- The levy also pays for alleys, sidewalks, lighting and landscaping, so its
  roads-only part lies between **${levy * ROADS_SHARE_OF_PROJECT / 1e6:,.0f}M** and **${levy / 1e6:,.0f}M**.
- Not agreement: {metric_km:,.0f} km ÷ 50 = {metric_km / 50:.0f} km a year, close to the
  ~73 km of residential roads *and alleys* rebuilt in 2024. Different roads.
""")
check(levy * ROADS_SHARE_OF_PROJECT <= renewal_req <= levy, "the renewal requirement sits inside the funded bracket",
      f"${renewal_req / 1e6:,.1f}M")

# %% [markdown]
# **Effect:** nothing in the model is confirmed against money more precisely
# than an order of magnitude, and the one per-neighbourhood check (section 4)
# says it is low.
#
# ## 9. What the map can and cannot show
#
# **Ideal:** cost that varies with class, age and condition. **Ours:** one rate
# times metres, so the cost map is the road-length map, and every rate error
# above moves the legend and panel shares, never the colours
# (`docs/FINDINGS_services_cost_lens_verdict.md` §5,
# `docs/FINDINGS_road_per_dwelling.md`).

# %%
m = served.dropna(subset=["cost_roads_life_per_acre", "road_m_per_acre"])
rho = spearmanr(m["cost_roads_life_per_acre"], m["road_m_per_acre"])[0]

r2 = res[res["road_m_per_dwelling"] >= 1.0].copy()
r2["dw_per_acre"] = r2["dwellings"] / r2["area_acres"]
rpa = r2["road_m_total"] / r2["area_acres"]
r_density = np.corrcoef(np.log10(r2["road_m_per_dwelling"]), np.log10(r2["dw_per_acre"]))[0, 1]
r_rpa = np.corrcoef(np.log10(rpa), np.log10(r2["dw_per_acre"]))[0, 1]

lv = served[(served["revenue_per_acre"] > 0) & served["cost_roads_ops_per_acre"].notna()]
share_ops = (lv["cost_roads_ops_per_acre"] / lv["revenue_per_acre"]).median()
share_life = (lv["cost_roads_life_per_acre"] / lv["revenue_per_acre"]).median()

md(f"""
- Rank correlation of the lifecycle cost map with road metres per acre: **{rho:.3f}**.
- Across {len(r2)} residential neighbourhoods, road metres per acre run
  {rpa.min():.0f}–{rpa.max():.0f} (**{rpa.max() / rpa.min():.1f}×**, median {rpa.median():.0f}),
  and are unrelated to density (r = {r_rpa:+.2f} on logs).
- Per dwelling instead: density explains **{r_density ** 2:.0%}** of the variation
  (r = {r_density:+.3f}), so a per-dwelling map would mostly redraw the density map.
- At the published rates the median neighbourhood's roads would take
  **{share_ops:.1%}** of its municipal tax on the operating basis and
  **{share_life:.1%}** on the lifecycle basis.
""")
check(rho > 0.999, "the cost map has exactly the pattern of road length", f"ρ = {rho:.4f}")

# %% [markdown]
# ## All the gaps at once

# %%
table(pd.DataFrame([
    ("Inventory", "every segment, width, age, condition", "centreline length and class",
     f"collector-heavy areas understated (collector {coll_premium:.2f}× per lane-km); no age or condition signal"),
    ("Which roads", "all City roads, arterials by use", f"collector + local, {metric_km:,.0f} km",
     "prices the local network, not the City's road bill"),
    ("Allocation", "frontage or use", "overlay, equal split on shared edges",
     f"{mixed_km:.1f} km beside set-aside land half lost; {len(big)} neighbourhoods off by >5%"),
    ("Lifecycle cost", "per class and condition", f"one figure, ${(OM + RENEW) / 1e6:.1f}M per km",
     f"low: observed reconstruction {agg_full / published_per_m:.2f}× the published renewal"),
    ("Service life", "observed reconstruction interval", "50 years",
     f"defensible; 25 years would make the rate ${(OM + RENEW) / 25 / 1000:.0f}"),
    ("Operating cost", "actual spend by class, current dollars", "citywide 2017 and 2025 averages per lane-km",
     f"low by ≥{net[3]:.2f}× (k ≤ 3), {lane_factor:.2f}× on the unit alone"),
    ("Basis and dollar year", "one basis, one year", "two bases, three vintages", "two numbers a reader must not add"),
    ("Check against money", "reconciles citywide and per neighbourhood",
     "order of magnitude citywide; NRP neighbourhoods", "consistent with a floor"),
], columns=["part", "ideal", "ours", "effect on the cost shown"]))

# %%
held = sum(ok for ok, _, _ in CHECKS)
print(f"{held}/{len(CHECKS)} of the report's claims hold on this data\n")
for ok, claim, detail in CHECKS:
    print(f"  [{'HOLDS' if ok else 'CHANGED'}] {claim}{'  — ' + detail if detail else ''}")
