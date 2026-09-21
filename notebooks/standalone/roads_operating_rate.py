# ---
# jupyter:
#   title: Where the $9.32 per road-metre per year comes from
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
# # Where the $9.32 per road-metre per year comes from
#
# **What this document is:** the full justification for the **operating** rate
# behind this project's roads cost lens — **$9.32 per road-metre per year** —
# re-derived from primary sources in front of you, including the parts that
# argue against it.
#
# **In one sentence:** the City of Edmonton's budget portal publishes a
# **$65,671,000** roadway-maintenance program and a reporter quoting a City
# supervisor puts road snow clearing at **$36.85M**; both are divided by the
# City's stated **~11,000 km** road inventory, giving **$5,970 + $3,350 =
# $9,320/km/yr = $9.32/m/yr**.
#
# **This is the companion to `roads_lifecycle_rate.py`, which defends the
# project's *other* road rate — $50/m/yr.** The two are different bases, not
# competing estimates, and §7 is about why they must never be summed or quoted
# as a ratio. Read that section before quoting either against the other.
#
# Three things in the opening sentence are choices or known defects rather than
# readings, and all three are pressed below:
#
# 1. ⚠️ **The unit is wrong, knowingly.** Both halves are dollars per
#    **lane**-kilometre and the pipeline multiplies them by **centreline**
#    metres. §3. This is the largest known error in the rate, it is
#    **disclosed on the map rather than corrected**, and it runs in the
#    direction of understatement — roughly **1.8×**.
# 2. **The two halves come from different publications of different years** —
#    FY2017 for maintenance, 2025 for snow — and the maintenance half ships
#    **unescalated**. §1, §5.
# 3. **The maintenance half was a different number until 2026-09-06**, when it
#    was re-scoped **4.65× upward** after this project was found rejecting the
#    old figure in one file while shipping it on a public map. §5.
#
# ## What this is not
#
# ⚠️ **OPERATING ONLY — this is annual upkeep and contains no capital.**
# Reconstruction is a separate and much larger budget. The map says so in the
# layer's own blurb and this rate is labelled a **floor** there. It is also a
# modelled uniform rate, not Edmonton's actual spend on any particular street.
# §8 states the limits in full.
#
# ## Reproducing
#
# ```
# pip install requests certifi pandas pypdf
# ```
#
# Every figure below is fetched live from a public URL at run time and checked
# against the transcription printed here. Nothing is read from this project's
# repository, and no API token is needed. Where a figure *cannot* be re-derived
# from public sources alone, it is labelled **[repo]** and cited rather than
# asserted.

# %%
import io
import re
import html as _html
from datetime import datetime, timezone

import certifi
import pandas as pd
import requests
from IPython.display import Markdown, display
from pypdf import PdfReader

FIRST_MEASURED = "2026-09-21"
RUN_AT = datetime.now(timezone.utc)

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124 Safari/537.36")

CHECKS = []


def check(ok, claim):
    """Record one invariant. The final cell raises if any came back False."""
    CHECKS.append((bool(ok), claim))
    return bool(ok)


def get(url, timeout=180):
    """Fetch a public URL.

    ⚠️ ``verify=certifi.where()`` is deliberate: some hosts this notebook was
    written on carry a CA bundle too old for edmonton.ca's chain, and the
    failure presents as an unreachable host rather than a certificate error.
    """
    r = requests.get(url, headers={"User-Agent": UA}, timeout=timeout,
                     verify=certifi.where())
    r.raise_for_status()
    return r


def visible_text(resp):
    """Strip markup so quotes can be matched against what a reader would see."""
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", resp.text, flags=re.S)
    return re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", " ", t)))


def pdf_pages(resp):
    return PdfReader(io.BytesIO(resp.content)).pages


def show(df):
    display(df.style.hide(axis="index") if hasattr(df, "style") else df)


display(Markdown(
    f"_First measured **{FIRST_MEASURED}**; this run executed "
    f"**{RUN_AT:%Y-%m-%d}** (UTC)._"))

# %% [markdown]
# ## 1. The two halves, and why they come from two publications
#
# ⚠️ **This rate's two halves have different sources and different vintages,
# and that is deliberate rather than an oversight.** The maintenance half was
# re-scoped onto the City's own published program in 2026-09-06 (§5) while the
# snow half kept the source it was built from. Both are stated here before
# either is defended.
#
# | half | figure | source | vintage |
# |---|---|---|---|
# | maintenance | $65,671,000 | Open Budget portal, `Roadway Maintenance` program | **FY2017** |
# | snow & ice | $36.85M | Taproot Edmonton, quoting a City supervisor | **2025** |
#
# ### 1a. The maintenance half — the City's own published program
#
# Source: **`budget.edmonton.ca/api/operating_budget.csv`**, the City's Open
# Budget portal. This is a machine-readable public API, so it is the strongest
# provenance in either roads notebook.
#
# ⚠️ **`Roadway Maintenance` is a SEPARATE PROGRAM from `Snow and Ice
# Control`**, which is what makes the two halves addable without double-count.
# The check below asserts that separation rather than assuming it.

# %%
BUDGET_URL = "https://budget.edmonton.ca/api/operating_budget.csv"
ob = pd.read_csv(io.BytesIO(get(BUDGET_URL).content))

roadway = ob[ob.program.astype(str).str.contains("Roadway Maintenance", na=False)]
snow_prog = ob[ob.program.astype(str).str.contains("Snow and Ice", na=False)]

rm_by_year = roadway.groupby("budget_year").budget.sum()
sn_by_year = snow_prog.groupby("budget_year").budget.sum()

MAINT_PROGRAM = 65_671_000

display(Markdown(
    f"**`Roadway Maintenance`** appears in **{len(rm_by_year)} budget year(s)**: "
    + ", ".join(f"FY{y} ${v:,.0f}" for y, v in rm_by_year.items())))

check(len(rm_by_year) == 1 and 2017 in rm_by_year.index,
      "the portal carries `Roadway Maintenance` for **FY2017 only** — the "
      "program was re-cut in 2018, which is why this half has no later vintage")
check(int(rm_by_year.loc[2017]) == MAINT_PROGRAM,
      f"FY2017 `Roadway Maintenance` = **${MAINT_PROGRAM:,}**, as transcribed")
check(2017 in sn_by_year.index and int(sn_by_year.loc[2017]) != MAINT_PROGRAM,
      f"`Snow and Ice Control` is a **separate program** (FY2017 "
      f"${sn_by_year.loc[2017]:,.0f}), so the maintenance half is "
      "maintenance-only and the two halves do not double-count")

# Composition — `category` is expense TYPE, not service.
comp = (roadway[roadway.budget_year == 2017].groupby("category").budget.sum()
        .sort_values(ascending=False))
show(comp.reset_index().assign(budget=lambda d: d.budget.map("${:,.0f}".format)))

check(abs(comp.sum() - MAINT_PROGRAM) < 1,
      "and the expense-type rows reconcile to the program total")

# %% [markdown]
# ⚠️ **The program name does not survive across the series, and that is why the
# maintenance half is stuck in 2017.** The portal re-cut it in 2018 into
# `Infrastructure Maintenance` — which also covers sidewalks, pathways and
# bridges — and again in 2026 into `Mobility Infrastructure Services`. **FY2017
# is the only year with a roads-only maintenance program**, so there is no
# later figure of the same scope to use. See `data/DATA.md` §17 for the
# portal's two rename eras.
#
# ### 1b. The snow half — a reporter quoting a City supervisor
#
# Source: **Taproot Edmonton, *"Why it costs so much more to clear snow from
# sidewalks, bike lanes than roads"*, Stephanie Swensrude, 2025-08-29**,
# quoting City infrastructure field operations supervisor Valerie Dacyk.
#
# ⚠️ **[SECONDARY]** — a news outlet quoting a named City staffer, not a City
# document. It must not be cited as City-published. §2 is the check that earns
# it a place anyway.

# %%
TAPROOT_URL = ("https://edmonton.taproot.news/briefs/2025/08/29/"
               "why-it-costs-so-much-more-to-clear-snow-from-sidewalks-"
               "bike-lanes-than-roads")
tap = visible_text(get(TAPROOT_URL))

QUOTE_SPLIT = ("The city spends about 55%, or $36.85 million, clearing roads "
               "across Edmonton and 45%, or $30.15 million, clearing anything "
               "else not classified as a road")
QUOTE_INVENTORY = ("11,000 linear kilometres of roads")
QUOTE_BUDGET = ("The annual snow and ice control budget is $67 million")

for label, q in [("the roads/paths split", QUOTE_SPLIT),
                 ("the inventory", QUOTE_INVENTORY),
                 ("the programme total", QUOTE_BUDGET)]:
    check(q in tap, f"the article still reads, verbatim — *{label}*: “{q}”")

SNOW_ROADS = 36_850_000
NETWORK_KM = 11_000

# %% [markdown]
# ### 1c. The arithmetic
#
# Both halves are divided by the same **~11,000 km** the article states. §3 is
# about what that number actually measures.

# %%
maint_per_km = MAINT_PROGRAM / NETWORK_KM
snow_per_km = SNOW_ROADS / NETWORK_KM
ops_per_km = round(maint_per_km) + round(snow_per_km)

show(pd.DataFrame([
    {"half": "roadway maintenance (FY2017)",
     "annual": f"${MAINT_PROGRAM:,}", "÷ 11,000 km": f"${maint_per_km:,.0f}/km"},
    {"half": "snow & ice, roads share (2025)",
     "annual": f"${SNOW_ROADS:,}", "÷ 11,000 km": f"${snow_per_km:,.0f}/km"},
    {"half": "OPERATING TOTAL — SHIPPED",
     "annual": "", "÷ 11,000 km": f"${ops_per_km:,}/km/yr = ${ops_per_km / 1000:.2f}/m/yr"},
]))

SHIPPED = ops_per_km / 1000
check(round(maint_per_km) == 5_970, "the maintenance half is **$5,970/km/yr**")
check(round(snow_per_km) == 3_350, "the snow half is **$3,350/km/yr**")
check(SHIPPED == 9.32,
      "and the shipped operating rate is exactly **$9.32/road-m/yr**")

# %% [markdown]
# ## 2. Why the secondary snow source is kept: its totals reconcile
#
# A reporter's figure normally could not carry a shipped number. This one does,
# because the article's **two shares sum to a programme total the City itself
# publishes** — and the City's number was not in the article for the reporter
# to fit to.
#
# ⚠️ **This is a genuine independent check, unlike the one demoted in the
# lifecycle notebook** (§3 there): the roads and paths figures come from the
# City staffer, and the programme total comes from the budget API. Two
# mechanisms, one answer.

# %%
SNOW_PATHS = 30_150_000
article_total = SNOW_ROADS + SNOW_PATHS
portal_2025 = float(sn_by_year.loc[2025])
agreement = article_total / portal_2025

display(Markdown(
    f"- article: roads **${SNOW_ROADS:,}** + paths **${SNOW_PATHS:,}** = "
    f"**${article_total:,}**\n"
    f"- portal `Snow and Ice Control`, FY2025: **${portal_2025:,.0f}**\n"
    f"- agreement: **{agreement * 100:.1f}%**"))

check(0.97 <= agreement <= 1.03,
      f"the article's two shares reconcile to the portal's published "
      f"`Snow and Ice Control` programme within **{abs(1 - agreement) * 100:.1f}%** — "
      "the check that earns a secondary source a shipped number")
check(abs(SNOW_ROADS / article_total - 0.55) < 0.01,
      "and the roads share is the 55% the article states, so the split is "
      "internally consistent too")

display(Markdown(
    "⚠️ **What this does NOT license.** The same article carries a "
    "**$1,285/km** roads maintenance figure that this project shipped for five "
    "weeks and then dropped (§5). Its totals reconciling does not make every "
    "line in it sound — **it makes the snow half checkable and left the "
    "maintenance line unsupported**, which is exactly the contrast that "
    "exposed the latter."))

# %% [markdown]
# ## 3. ⚠️ The unit is a LANE-kilometre, and the pipeline multiplies it by CENTRELINE metres
#
# **This is the largest known defect in the rate and it ships disclosed rather
# than corrected** (Peter's call, 2026-09-08 — `docs/DECISIONS.md`). Anyone
# quoting $9.32 needs this section.
#
# The `~11,000 km` denominator is the City's snow-and-ice inventory. If that is
# **lane**-km — length × number of lanes — then dividing by it produces dollars
# per lane-km, and the pipeline then multiplies that by **centreline** metres
# from the City's road-geometry feed. A two-lane street gets charged once
# instead of twice.
#
# ### 3a. The City contradicts itself in one document, twelve pages apart
#
# Source: **City of Edmonton, *Snow and Ice Control Annual Report, Winter
# 2023-24*** — a primary City PDF, fetched live below.

# %%
SIC_URL = ("https://www.edmonton.ca/sites/default/files/public-files/assets/"
           "PDF/Snow-Ice-Annual-Report_Winter2023-2024.pdf")
sic = pdf_pages(get(SIC_URL))
p4 = re.sub(r"\s+", " ", sic[3].extract_text())
p16 = re.sub(r"\s+", " ", sic[15].extract_text())

QUOTE_P4 = ("The City maintains more than 12,000 linear km of roadways and "
            "500 km of active pathways")
QUOTE_P16 = ("Distances are represented in lane kilometres (lane km), which is "
             "a function of the length of the street or bike route multiplied "
             "by the number of lanes")

check(QUOTE_P4 in p4, f"**p4** says: “{QUOTE_P4}”")
check(QUOTE_P16 in p16, f"**p16** says: “{QUOTE_P16}”")

display(Markdown(
    "> **p4:** *“…more than 12,000 **linear km** of roadways…”*\n>\n"
    "> **p16:** *“Distances are represented in **lane kilometres** (lane km), "
    "which is a function of the length of the street or bike route multiplied "
    "by the number of lanes…”*\n\n"
    "**The unit cannot be settled from the City's wording, because the City's "
    "own wording disagrees with itself.** Filed as `docs/DATA_ISSUES.md` "
    "issue **G** — ⚠️ **not yet reported to the City.**"))

# %% [markdown]
# ### 3b. Magnitude settles what wording cannot
#
# The City publishes its road centreline geometry as an open dataset — the same
# feed this project's pipeline reads. **[repo]**, measured in EPSG:3400 from
# `data/raw/roads.geojson` (53,854 segments); the derivation is in
# `docs/FINDINGS_road_figures_consolidation.md` §L2b and `data/DATA.md` §6.

# %%
# [repo] — centreline km measured from the City's own feed.
CENTRELINE = {
    "everything in the feed (roads + alleys + railways, all owners)": 7_700,
    "centerline_type == Road, all owners": 5_685,
    "City of Edmonton roads": 5_029,
    "City alleys": 1_311,
}
show(pd.DataFrame([{"population": k, "centreline km": f"{v:,}"}
                   for k, v in CENTRELINE.items()]))

city_roads_and_alleys = CENTRELINE["City of Edmonton roads"] + CENTRELINE["City alleys"]

display(Markdown(
    f"**City roads + alleys = {city_roads_and_alleys:,} centreline km.** The "
    f"City's stated inventory is **11,000–12,000**. There is no reading of the "
    f"centreline data under which those are the same number — a linear reading "
    f"is **{(1 - city_roads_and_alleys / NETWORK_KM) * 100:.0f}% low**."))

check(city_roads_and_alleys < 0.7 * NETWORK_KM,
      f"the City's own centreline feed holds {city_roads_and_alleys:,} km of "
      f"roads + alleys against a stated ~{NETWORK_KM:,} — the inventory "
      "**cannot** be centreline km **[repo]**")

# %% [markdown]
# ⚠️ **Three corroborations and one warning about them**, all from
# `FINDINGS_road_figures_consolidation.md` §L2b:
#
# 1. The City's 2021 policy change added **1,250–1,300 lane-km of alleys** to
#    the inventory; the feed holds **1,311 alley centreline km**. Alleys are one
#    lane, so the two units coincide there. ⚠️ **This is NOT a unit check** — it
#    shows the inventory *includes* alleys, nothing more. It was corrected from
#    a stronger claim on 2026-09-10.
# 2. Relayed 2020 class figures give **2.58 / 1.90 / 1.76** lanes per centreline
#    km (arterial / collector / local). ⚠️ **[SECONDARY, and the blog is now
#    404]** — no primary source has been found for the class split.
# 3. Calgary publishes **6,652 linear km / 18,239 lane-km** for a similar
#    footprint, so a ~2× multiple is what a road network reads.
#
# **What carries the finding is the magnitude argument plus the p16 definition.**
# The other supports are weaker than they first appeared and are recorded at
# their true strength.
#
# ### 3c. What it does to the rate, and which end of the range is real

# %%
conversions = pd.DataFrame([
    {"conversion": "shipped — ÷ 11,000, unit unexamined",
     "ratio": "—", "operating $/m": "$9.32", "standing": "what ships"},
    {"conversion": "collector+local lane-km ÷ centreline km (6,593 ÷ 3,666)",
     "ratio": "1.80×", "operating $/m": "$16.8",
     "standing": "**BEST ESTIMATE** — matched, and the population charged"},
    {"conversion": "City road centreline, alleys pro-rata",
     "ratio": "1.94×", "operating $/m": "$18.1", "standing": "interior"},
    {"conversion": "÷ 5,029 City road centreline, alleys charged nothing",
     "ratio": "2.19×", "operating $/m": "$20.4",
     "standing": "**UPPER BOUND** — mismatched populations, not a multiplicity"},
])
show(conversions)

display(Markdown(
    "⚠️ **The ends of that range do not have equal standing, and a fourth "
    "ratio — 1.73 — entered outside circulation as “inside the range” when it "
    "is BELOW it.** 1.73 divides the whole inventory by roads + alleys; alleys "
    "are one lane, so it is diluted downward and is a lower bound. Only "
    "**1.80** is a lane-multiplicity measured on the population the metric "
    "actually charges.\n\n"
    "**Direction: the shipped rate UNDERSTATES by roughly 1.8×.** Both halves "
    "share the denominator, so both move together.\n\n"
    "⚠️ **The shipped rate is $/lane-km applied to centreline metres, and it "
    "is DISCLOSED on the map rather than corrected** (`DECISIONS.md` "
    "2026-09-08). That sentence carries no ✅ below **on purpose** — it is a "
    "statement about what this project decided, and nothing in a notebook of "
    "live source fetches can verify it. The invariant above it is the one that "
    "does real work: it measures the City's own centreline feed against the "
    "City's own stated inventory."))

# %% [markdown]
# ### 3d. Why it was disclosed rather than converted
#
# Peter's call, 2026-09-08: *"let's choose the floor for now."* Three reasons,
# and the third is a rule rather than a judgement:
#
# 1. The **×1.80** conversion rests on a class split whose only source is a
#    secondary relay that now 404s.
# 2. The **×2.19** conversion charges alleys nothing, which is not a
#    lane-multiplicity at all.
# 3. ⚠️ **No replacement rate comes out of an audit's own arithmetic.** A number
#    on a public map should trace to a publication, not to this project's
#    correction of one.
#
# So the value stayed at $9.32 and **three copy sites on the map were changed to
# say “per lane-kilometre”** — `web/index.html` lines near `:531`, `:1159` and
# `:5395`. `scripts/check_cost_copy.py` ties that copy to
# `data/city_unit_costs.json` and runs **on the merge gate**, so the disclosure
# cannot drift away from the number.

# %% [markdown]
# ## 4. What the rate is multiplied by
#
# **[repo]** — this section describes this project's pipeline, not a City
# publication. Source: `src/load_roads.py`; decisions in
# `docs/SPEC_services.md`.
#
# The rate is applied to `road_m_per_acre`, which counts **collector and local
# centreline metres only**:
#
# | excluded | how | why |
# |---|---|---|
# | **alleys** | `CENTERLINE_TYPE = "Road"` drops 12,088 rows; 41 more are caught by *functional class* | shared rear infrastructure; function governs, not the row label |
# | **railways** | same row filter, 2,117 rows | not roads |
# | **non-City roads** | `RESPONSIBLE_PARTY = "City of Edmonton"` | the provincial ring road is not a City cost |
# | **arterials** | 4 `Arterial-Class A–D` codes, excluded from `METRIC_GROUPS` | shared infrastructure serving the whole city, not the abutting neighbourhood |
#
# ⚠️ **Two consequences that must travel with any citywide total built from
# this rate:**
#
# 1. **It is a PARTIAL NETWORK by construction.** Arterials and alleys are out,
#    so every citywide figure understates the network.
# 2. ⚠️ **The arterial exclusion cuts the OTHER WAY from §3** — see §6.
#
# ⚠️ **Unknown or null functional classes land in their own group** rather than
# defaulting to `local`. Until 2026-09-09 they were charged as local, which is
# the kind of silent default this project's data-handling rules exist to
# prevent.

# %% [markdown]
# ## 5. ⚠️ Where this project's own reasoning was wrong
#
# **This section exists because it is the strongest thing in the document.** An
# argument that has never lost anything has not been tested.
#
# **Until 2026-09-06 the maintenance half was $1,285/km, and the rate was
# $4.635/m/yr.** That figure came from the same Taproot article as the snow
# half: *"It costs about $178 per kilometre to replace, repair, and maintain
# active pathways, and **$1,285 per kilometre to do the same for roads**."*

# %%
QUOTE_1285 = ("It costs about $178 per kilometre to replace, repair, and "
              "maintain active pathways, and $1,285 per kilometre to do the "
              "same for roads")
check(QUOTE_1285 in tap,
      f"the article still carries the retired figure, verbatim: “{QUOTE_1285}”")

OLD_MAINT, OLD_RATE = 1_285, 4.635
display(Markdown(
    f"- old: ${OLD_MAINT:,}/km + ${round(snow_per_km):,}/km = "
    f"**${OLD_RATE}/m/yr**\n"
    f"- now: ${round(maint_per_km):,}/km + ${round(snow_per_km):,}/km = "
    f"**${SHIPPED}/m/yr** — a **{SHIPPED / OLD_RATE:.3f}×** move"))

check(abs(round(maint_per_km) / OLD_MAINT - 4.65) < 0.02,
      f"the City's published program is **{round(maint_per_km) / OLD_MAINT:.2f}×** "
      f"the article's ${OLD_MAINT:,}/km line")

# %% [markdown]
# ### What actually forced the change — and it was not new evidence
#
# ⚠️ **This project was rejecting $1,285 in one file while shipping it on a
# public map layer.** `data/DATA.md` §16 had retired `$1,285/km × ~11,000 km =
# $14.135M` as **~5× too low** on 2026-08-04 — and the same $1,285 remained the
# maintenance half of a served column. **The split treatment is what tipped the
# call**, not a better reading of the figure.
#
# A second test the repo had already applied elsewhere pointed the same way.
# The City's own set-aside rule implies **~3.33%/yr** of asset value for a road
# (`roads_lifecycle_rate.py` §3); against $1,500,000/km of road capital:

# %%
ROAD_CAPITAL = 1_500_000      # [repo] — City's Development Impact page, see the lifecycle notebook
setaside = pd.DataFrame([
    {"rate": "$178/km bikeway — REJECTED 2026-08-03",
     "%/yr of asset value": f"{178 / 452_065 * 100:.3f}%", "verdict": "85× low"},
    {"rate": "$1,285/km road — shipped anyway, until 2026-09-06",
     "%/yr of asset value": f"{OLD_MAINT / ROAD_CAPITAL * 100:.3f}%",
     "verdict": "**39× low**"},
])
show(setaside)

check(OLD_MAINT / ROAD_CAPITAL < 0.001,
      f"$1,285/km is **{OLD_MAINT / ROAD_CAPITAL * 100:.3f}%/yr** of road asset "
      "value against the City's own ~3.33% set-aside rule — the identical test "
      "that had already blocked a bikeway rate, never applied to roads")

display(Markdown(
    "⚠️ **WHAT $1,285 ACTUALLY MEASURES IS STILL UNKNOWN.** The article gives "
    "it no denominator and no scope, and no clean decomposition of the "
    "published program reproduces it — materials-only "
    f"(${17_974_000 / NETWORK_KM:,.0f}/km) is the closest and is still 1.27× "
    "off. **It was dropped for lack of support, not replaced by a better "
    "reading of it.** Do not invent a scope for it.\n\n"
    "Full record: `docs/FINDINGS_roadway_maintenance_rate.md`."))

# %% [markdown]
# ### ⚠️ A reconciliation this project published, then demoted
#
# When the re-scope was argued, it was supported by the observation that
# substituting $5,970 closed the gap against the lifecycle O&M half ($12/m/yr)
# from **2.59× to 1.29×**. **That clause does not survive §3** — it compared
# dollars per *lane*-km to dollars per *centreline*-km. Corrected for the unit,
# the operating rate is ~$16.8–20.4/m against $12, so the disagreement is real
# and runs the **other way** (1.4–1.7×).
#
# **The 2026-09-06 decision does not rest on that clause and still stands**; the
# clause is demoted the way the 3% cross-check was on 2026-09-03. Recorded
# because a demoted support that stays in circulation is how a wrong number
# gets quoted confidently.

# %% [markdown]
# ## 6. The error that runs the other way — the arterial blend
#
# §3 says the rate understates by ~1.8×. **This section is the offsetting
# error, and it is not the same size.**
#
# Both halves are **citywide blends that include arterials**. Arterials are
# priority-cleared and more heavily maintained, and cost more per km than
# locals — but the rate is applied only to collector and local metres (§4). So
# the blend **overstates** the local-road term.

# %%
ARTERIAL_SHARE = 0.35        # 3,500 of 10,093 lane-km [repo, secondary relay]
rows = []
for k in (1, 2, 3, 5):
    blend_factor = 1 / (0.65 + 0.35 * k)
    rows.append({"if an arterial costs k× a local": f"k = {k}",
                 "blend overstates by": f"{blend_factor:.2f}×",
                 "net with §3's 1.80×": f"{1.80 * blend_factor:.2f}×"})
show(pd.DataFrame(rows))

net_k3 = 1.80 / (0.65 + 0.35 * 3)
check(net_k3 >= 1.0,
      f"at k=3 the two errors still net to **{net_k3:.2f}×** understatement — "
      "it takes k > 3.3 to flip the sign")

display(Markdown(
    "⚠️ **Nothing published gives *k*.** The City's Procedure C409K puts "
    "arterials at bare pavement fastest and residential at a 5 cm snowpack in "
    "10–14 days, so *k* > 1 with certainty — but its size is unmeasured. "
    "**This is why the rate is called a floor**: under a stated *k* ≤ 3.3 the "
    "net direction is understatement, which makes “floor” an arithmetic claim "
    "rather than a judgement about which error is larger."))

# %% [markdown]
# ## 7. ⚠️ This is NOT the lifecycle rate, and the gap between them is partly an artifact
#
# **The single most likely way to misuse this number.** The project ships two
# road-cost bases and they are different questions, not competing answers:
#
# | basis | rate | column | covers |
# |---|---|---|---|
# | **operating** (this document) | **$9.32/m/yr** | `cost_roads_ops_per_acre` | upkeep only |
# | **lifecycle** (`roads_lifecycle_rate.py`) | **$50/m/yr** | `cost_roads_life_per_acre` | upkeep + rebuild |
#
# ⚠️ **NEVER SUM THEM** — the lifecycle basis already contains an O&M term
# ($12/m/yr of its $50). ⚠️ **AND DO NOT QUOTE THE 5.4× GAP AS A FACT ABOUT A
# ROAD METRE.**

# %%
display(Markdown(
    f"- raw ratio as shipped: **${50 / SHIPPED:.1f}×**\n"
    f"- but the operating rate is $/lane-km (§3) and the lifecycle rate is "
    f"$/**centreline**-km (established 2026-09-17)\n"
    f"- on a common centreline basis: 50 ÷ (9.32 × 1.80) = "
    f"**{50 / (SHIPPED * 1.80):.1f}×**"))

check(2.0 <= 50 / (SHIPPED * 1.80) <= 3.5,
      f"put on one unit the real gap is **~{50 / (SHIPPED * 1.80):.1f}×**, not "
      f"the **{50 / SHIPPED:.1f}×** the two shipped numbers appear to show — "
      "the difference is a unit artifact")

# %% [markdown]
# ## 8. What this rate does NOT establish
#
# 1. ⚠️ **The unit is known to be wrong.** $/lane-km applied to centreline
#    metres, understating ~1.8×. Disclosed on the map, not corrected. §3.
# 2. **OPERATING ONLY.** No capital. Reconstruction is a separate and much
#    larger budget, and this is therefore **not what a road costs over its
#    life**. The map's own blurb says exactly that.
# 3. **Two vintages, unescalated.** FY2017 maintenance against a 2025 snow
#    half. The City's own branch-level growth would put the maintenance half
#    1.24–1.34× higher (§9), and branch growth applied to a program figure is a
#    proxy, not a deflator — which is why it is not applied.
# 4. **Mixed populations.** Both halves are citywide blends including
#    arterials, applied to collector+local metres. §6.
# 5. **MODELLED and uniform.** No neighbourhood's figure is an observation of
#    that neighbourhood's spend.
# 6. **A partial network.** Arterials and alleys excluded, so any citywide
#    total understates. §4.
# 7. **The snow half is SECONDARY** — a reporter quoting a City staffer. §2
#    earns it a place; it does not make it City-published.
# 8. ⚠️ **What the retired $1,285/km measured is still unknown.** §5.

# %% [markdown]
# ## 9. The vintage question, measured rather than asserted
#
# The maintenance half ships in **2017 dollars**. How much does that matter?
# The `Parks & Roads Services` branch's own growth is the available proxy —
# computed from the fetched CSV, **not recalled**.
#
# ⚠️ **Its agreement with `data/DATA.md` §16's "~34%" is NOT corroboration** —
# §16 was derived from this same portal, so the two are one source restated.
# Same trap as the 3% set-aside cross-check demoted 2026-09-03.

# %%
branch = (ob[ob.branch.astype(str).str.contains("Parks", na=False)]
          .groupby("budget_year").budget.sum())
g25 = branch.loc[2025] / branch.loc[2017]
g26 = branch.loc[2026] / branch.loc[2017]

show(pd.DataFrame([
    {"endpoint": f"FY2025 (the series maximum — ${branch.loc[2025]:,.0f})",
     "growth": f"{g25:.4f}×",
     "maintenance would be": f"${round(maint_per_km) * g25:,.0f}/km",
     "operating all-in": f"${(round(maint_per_km) * g25 + round(snow_per_km)) / 1000:.2f}/m"},
    {"endpoint": f"FY2026 (${branch.loc[2026]:,.0f})",
     "growth": f"{g26:.4f}×",
     "maintenance would be": f"${round(maint_per_km) * g26:,.0f}/km",
     "operating all-in": f"${(round(maint_per_km) * g26 + round(snow_per_km)) / 1000:.2f}/m"},
]))

check(1.2 <= g26 <= g25 <= 1.4,
      f"escalating on branch growth would raise the rate to "
      f"${(round(maint_per_km) * g26 + round(snow_per_km)) / 1000:.2f}–"
      f"${(round(maint_per_km) * g25 + round(snow_per_km)) / 1000:.2f}/m — "
      "another reason the shipped number is a floor")
check(branch.loc[2025] == branch.max(),
      "⚠️ **FY2025 is the series MAXIMUM**, so the higher escalation uses the "
      "more favourable of the two available endpoints — stated rather than "
      "quietly chosen")

display(Markdown(
    f"⚠️ **This figure MOVED between runs, which is what the invariants are "
    f"for.** `docs/FINDINGS_roadway_maintenance_rate.md` recorded FY2026 as "
    f"**$307,325,053 (1.2551×)** on 2026-09-05; this run reads "
    f"**${branch.loc[2026]:,.0f} ({g26:.4f}×)**. The portal revised it. "
    f"**Nothing shipped changes** — the rate is unescalated FY2017 — but a "
    f"document that pinned the escalated figure would now be wrong."))

# %% [markdown]
# ## 10. Where the rest of this lives
#
# This document is deliberately not self-contained. The pointers:
#
# | what | where |
# |---|---|
# | the shipped rate and every caveat on it | `data/city_unit_costs.json` → `roadway_ops` |
# | the re-scope decision and its evidence | `docs/FINDINGS_roadway_maintenance_rate.md` |
# | the lane-km finding, in full | `docs/FINDINGS_road_figures_consolidation.md` §L2b |
# | the City's self-contradiction on the unit | `docs/DATA_ISSUES.md` issue **G** — ⚠️ **unreported** |
# | the network definition | `src/load_roads.py`; `docs/SPEC_services.md` |
# | the budget portal's rename eras | `data/DATA.md` §17 |
# | the **other** road rate | `notebooks/standalone/roads_lifecycle_rate.py` |
# | the copy guard tying map text to this JSON | `scripts/check_cost_copy.py` (merge gate) |
# | the locked decisions | `docs/DECISIONS.md` 2026-09-06, 2026-09-08, 2026-09-17 |

# %% [markdown]
# ## 11. Invariants
#
# Every claim above is asserted here against what this run actually fetched. A
# failure means either a transcription is wrong or a source has changed —
# both worth knowing.
#
# ⚠️ **This is a justification notebook, not a defect report.** Its invariants
# are meant to keep **passing**: a failure means a source moved under a number
# this project ships. That is the opposite of the reports in
# `docs/EVIDENCE_NOTEBOOKS.md`, whose invariants are written to fail when a
# publisher fixes something.

# %%
passed = sum(1 for ok, _ in CHECKS if ok)
display(Markdown(f"### {passed} of {len(CHECKS)} invariants passed"))
for ok, claim in CHECKS:
    display(Markdown(f"- {'✅' if ok else '❌'} {claim}"))
display(Markdown(
    f"_First measured **{FIRST_MEASURED}**; re-executed **{RUN_AT:%Y-%m-%d}** "
    f"(UTC) against live public sources._"))
if passed != len(CHECKS):
    raise AssertionError(f"{len(CHECKS) - passed} invariant(s) failed — see above")
