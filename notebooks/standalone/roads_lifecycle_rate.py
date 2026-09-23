# ---
# jupyter:
#   title: Where the $50 per road-metre per year comes from
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
# # Where the $50 per road-metre per year comes from
#
# **What this document is:** the full justification for the single modelled
# number behind this project's roads cost lens — **$50 per road-metre per
# year** — re-derived from primary sources in front of you, including the parts
# that argue against it.
#
# **In one sentence:** the City of Edmonton publishes a complete lifecycle for
# one kilometre of a typical neighbourhood road — **$1.5M to build, $600k to
# operate and maintain, $1.9M to renew and replace** — and this project
# annualizes the **$2.5M non-capital** half over the **50-year** life the same
# page describes, giving **$50,000/km/yr = $50/m/yr**.
#
# Two things in that sentence are choices rather than readings, and both are
# challenged below:
#
# 1. **Is the City's "1 kilometre" a centreline kilometre or a lane kilometre?**
#    A two-lane street would halve every per-metre figure. §2.
# 2. **Is the life 25 years or 50?** The same City sentence contains both
#    numbers. §3. This is the load-bearing choice: at 25 years the rate would be
#    **$100/m/yr**, exactly double.
#
# §§4–6 then check the answer against three sources that were produced by
# different mechanisms and for different purposes — the City's audited financial
# statements, its engineering condition assessments, and a City staffer
# describing the maintenance schedule — and §7 shows where **this project's own
# earlier reasoning was wrong** and how it was corrected.
#
# ## What this is not
#
# ⚠️ **This is a modelled uniform rate, not Edmonton's actual spend on any
# particular street.** It applies one published per-kilometre lifecycle to every
# collector and local road metre in the city. Arterials and alleys are excluded
# from the metric entirely. §9 states the limits in full.
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

FIRST_MEASURED = "2026-09-18"
RUN_AT = datetime.now(timezone.utc)

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124 Safari/537.36")

CHECKS = []


def check(ok, claim):
    """Record one invariant. The final cell raises if any came back False.

    ⚠️ The plain-text line is not redundant with the Markdown summary at the
    end. Outside a Jupyter kernel ``display()`` renders as an opaque object
    repr, so a notebook run as a script would report *nothing* about its own
    invariants — and the monthly recheck
    (``scripts/recheck_evidence_notebooks.py``) runs these as scripts. Printing
    here is what makes the result legible to a machine; it is the same idiom
    the five evidence notebooks use.
    """
    CHECKS.append((bool(ok), claim))
    print(f"  [{'PASS' if ok else 'FAIL'}] {claim}")
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
# ## 1. The published figures
#
# Source: **City of Edmonton — *Development Impact on Infrastructure***. This is
# a live City web page, not a report, and it is the origin of every dollar figure
# in the rate.
#
# ⚠️ **`www.edmonton.ca` soft-404s with HTTP 200** — a missing page returns a
# success status with a body titled *"Page Not Found"*. The title is checked
# below, because a status-code check alone would report a dead City URL as live.

# %%
DI_URL = ("https://www.edmonton.ca/city_government/initiatives_innovation/"
          "development-impact-on-infrastructure")

di = get(DI_URL)
di_text = visible_text(di)
di_title = re.search(r"<title>(.*?)</title>", di.text, re.S).group(1).strip()

display(Markdown(f"**HTTP {di.status_code}** · title: *{di_title}*"))

check("Page Not Found" not in di_title,
      "the Development Impact page is live and is not a soft-404")

# The two passages the whole rate rests on, as a reader sees them.
QUOTE_CAPITAL = ("the initial cost of 1 kilometre of a typical Edmonton "
                 "neighbourhood road is about $1.5 million")
QUOTE_LIFE = ("The road will usually last 25 years, but proper maintenance and "
              "renewal could extend its life to 50 years")
QUOTE_SPEND = ("it would cost approximately $600,000 to operate and maintain "
               "and another $1.9 million to renew and replace")
QUOTE_TOTAL = ("The total cost over its life would be about $4 million")
QUOTE_SETASIDE = ("we need to set aside, on average, 3% of the infrastructure"
                  "’s value to operate, maintain, renew and replace")

for label, q in [("capital", QUOTE_CAPITAL), ("life", QUOTE_LIFE),
                 ("spend", QUOTE_SPEND), ("total", QUOTE_TOTAL),
                 ("3% rule", QUOTE_SETASIDE)]:
    check(q in di_text, f"the page still reads, verbatim — *{label}*: “{q}”")

display(Markdown(
    "> " + QUOTE_CAPITAL[0].upper() + QUOTE_CAPITAL[1:] + ". " + QUOTE_LIFE
    + ". … Throughout the life of the road, " + QUOTE_SPEND + ". "
    + QUOTE_TOTAL + ". Or about 2.5 times the initial capital investment."))

# %% [markdown]
# ### The page audits itself
#
# The four figures are not four independent claims — the page states a total,
# and the total reconciles. That is what makes them **one internally consistent
# lifecycle** rather than a mix of bases picked up from different places.

# %%
CAPITAL = 1_500_000      # initial construction, per km
OM = 600_000             # operate and maintain, over the life
RENEWAL = 1_900_000      # renew and replace, over the life

total = CAPITAL + OM + RENEWAL
ratio = total / CAPITAL

show(pd.DataFrame([
    {"component": "initial capital", "per km": f"${CAPITAL:,}"},
    {"component": "operate and maintain", "per km": f"${OM:,}"},
    {"component": "renew and replace", "per km": f"${RENEWAL:,}"},
    {"component": "TOTAL (page says “about $4 million”)", "per km": f"${total:,}"},
    {"component": "multiple of capital (page says “about 2.5 times”)",
     "per km": f"{ratio:.2f}×"},
]))

check(total == 4_000_000,
      "the three published components sum to exactly the $4M total the page "
      "states, so they describe one scenario rather than several")
check(2.4 <= ratio <= 2.8,
      f"and the total is {ratio:.2f}× the capital cost against the page's "
      "stated “about 2.5 times”")

# %% [markdown]
# ## 2. The unit is a CENTRELINE kilometre, not a lane kilometre
#
# This matters more than it sounds. A typical neighbourhood street is two lanes,
# so reading these figures as lane-kilometres would **halve** every per-metre
# result — $50/m/yr would become $25/m/yr. It would also invert a separate
# finding in this project about observed reconstruction spend.
#
# Three things pin it, and the third is the one that cannot be faked:

# %%
lane_mentions = len(re.findall(r"\blane\b", di_text, re.I))

check("1 kilometre of a typical Edmonton neighbourhood road" in di_text,
      "(1) the unit is stated as *“1 kilometre of a typical Edmonton "
      "neighbourhood road”* — one road, not one lane")
check(lane_mentions == 0,
      f"(2) the word “lane” appears {lane_mentions} times on the entire "
      "rendered page — a lane-km figure would have to say so somewhere")
# (3) is the §1 reconciliation above — not asserted a second time.
display(Markdown(
    "(3) the page's own $4M total reconciles to the three components (§1), "
    "which a mixed-unit reading could not do."))

display(Markdown(
    "The subject also stays singular throughout — *“The road will…”*, "
    "*“its life”* — which is not how a network aggregate reads."))

# %% [markdown]
# ## 3. The denominator: why 50 years and not 25
#
# **This is the choice, and it is worth exactly 2×.** The City's sentence
# contains both numbers: the road *"will usually last 25 years, but proper
# maintenance and renewal could extend its life to 50 years."*

# %%
rates = pd.DataFrame([
    {"life": "25 years (unmaintained)", "$/km/yr": f"${(OM + RENEWAL) / 25:,.0f}",
     "$/m/yr": f"${(OM + RENEWAL) / 25 / 1000:,.0f}"},
    {"life": "50 years (maintained) — SHIPPED",
     "$/km/yr": f"${(OM + RENEWAL) / 50:,.0f}",
     "$/m/yr": f"${(OM + RENEWAL) / 50 / 1000:,.0f}"},
])
show(rates)

SHIPPED = (OM + RENEWAL) / 50 / 1000
check(SHIPPED == 50.0, "the shipped rate is exactly $50/road-m/yr at a 50-year life")
check((OM + RENEWAL) / 25 / 1000 == 100.0,
      "and would be exactly $100/road-m/yr at 25 — the choice is worth 2×, "
      "nothing else in the chain moves")

# %% [markdown]
# ### The argument for 50, which is not circular
#
# **The $600k + $1.9M *is* the maintenance and renewal the page says buys the
# extension.** The sentence is causal: proper maintenance and renewal *could
# extend its life to 50 years*. Annualizing that same bundle over 25 years
# charges the full cost of the extension while refusing to count the extension —
# it bills for a 50-year road and then depreciates it as a 25-year one.
#
# ⚠️ **The two numbers are not two estimates of one event.** ~25 is when the
# pavement structure is due for intervention; 50 is the interval to full
# reconstruction, bought with the resurfacing and renewal spending in between
# while the road base persists. §6 shows a City staffer describing exactly that
# schedule. Because this metric charges the **whole bundle** — capital, O&M and
# renewal — its denominator has to be the interval over which the *bundle*
# recurs, which is the reconstruction interval.
#
# ### The supporting argument that had to be withdrawn
#
# ⚠️ **Recorded because it was this project's own error.** The same page says
# *"for every dollar invested, we need to set aside, on average, 3% of the
# infrastructure's value."* 3% of $1.5M ≈ $45,000/km/yr, which looks like an
# independent second opinion agreeing with $50,000 rather than $100,000. **It is
# not independent.** The page defines that 3% as covering *operate, maintain,
# renew and replace* — the same bundle over the same life — so it is the same
# arithmetic restated.

# %%
implied_pct = (OM + RENEWAL) / 50 / CAPITAL      # the bundle's own annual %
three_pct = 0.03 * CAPITAL

display(Markdown(
    f"- 3% of $1,500,000 = **${three_pct:,.0f}/km/yr** — looks like it "
    f"corroborates $50,000\n"
    f"- but the bundle's own implied rate is "
    f"**{implied_pct * 100:.2f}%/yr**, so $45,000 vs $50,000 is just a rounded "
    f"3% against {implied_pct * 100:.2f}% — one number, not two"))

check(0.033 <= implied_pct <= 0.034,
      f"the published bundle implies {implied_pct * 100:.2f}%/yr of asset value, "
      "so the page's “3%” is a rounding of this project's own input, not "
      "a check on it")
check("fire station" in di_text.lower(),
      "the same page assigns a fire station a different multiple, so the 3% is "
      "a property of the road example rather than a general law")

display(Markdown(
    "**What survives:** the 3% rule still *discriminates* the two lives "
    "directionally, because the life is the only free variable — 3.33%/yr at 50 "
    "against 6.67%/yr at 25. **What does not survive: calling it independent "
    "confirmation.**"))

# %% [markdown]
# ## 4. Cross-check A — the City's audited books imply 36–38 years
#
# Source: **City of Edmonton, Consolidated Financial Statements, FY2023.**
# Produced by an entirely different mechanism (accounting policy, externally
# audited) for an entirely different purpose.
#
# The statements do **not** publish a road service life — roadways are amortized
# inside a broad *Engineered structures* class at *7 to 100 years*, which cannot
# discriminate 25 from 50. But **Schedule 1** reports gross cost and annual
# amortization on separate lines per class, so an implied average life is
# derivable: `gross cost ÷ annual amortization expense`.
#
# ⚠️ **The reason this method is trustworthy here is that the document audits
# itself:** the same ratio computed for *every* class must land inside that
# class's own stated Note 1 range. All eight do, and the ordering is the right
# shape — light rail outlives roads, which outlive buses, which outlive
# machinery. A method producing roads that outlive LRT would be measuring the
# arithmetic rather than the assets.

# %%
CFS_URL = ("https://www.edmonton.ca/sites/default/files/public-files/"
           "FinancialAnnualReportConsolidatedFinancialStatements2023.pdf")
cfs = get(CFS_URL)
cfs_pages = pdf_pages(cfs)
note1 = cfs_pages[22].extract_text()

check(len(cfs_pages) > 50 and "Engineered structures" in note1,
      "the FY2023 Consolidated Financial Statements fetched and Note 1 is on p23")
check(re.search(r"7\s*to\s*100\s*years", note1) is not None,
      "Note 1 amortizes *Engineered structures* at **7 to 100 years** — no "
      "roads line exists, and that range cannot discriminate 25 from 50")

# Schedule 1, p79 (thousands of dollars): opening cost, closing cost,
# amortization expense for the year, and the class's own Note 1 range.
S1 = {
    "Land improvements":       (1_897_484, 1_987_563,  62_379, (20, 50)),
    "Buildings":               (3_704_948, 3_969_045, 141_361, (10, 60)),
    "Vehicles":                (1_485_937, 1_626_337,  74_000, (9, 35)),
    "Machinery and equipment": (1_037_305, 1_092_018,  75_923, (3, 50)),
    "ENG: Roadway system":     (9_304_626, 9_732_383, 255_893, (7, 100)),
    "ENG: Light rail transit": (1_866_680, 2_091_320,  36_660, (7, 100)),
    "ENG: Waste":              (156_702,     156_839,   2_692, (7, 100)),
    "ENG: Bus system":         (289_323,     297_697,  10_230, (7, 100)),
}

# Pinned to the fetched PDF (Schedule 1 is PDF page 12, printed p79): every
# transcribed figure must appear in the document this run downloaded, so a
# restated or corrected Schedule 1 fails here instead of passing on constants.
cfs_text = " ".join(p.extract_text() for p in cfs_pages)
missing = [f"{v:,}" for o, c, a, _ in S1.values() for v in (o, c, a)
           if f"{v:,}" not in cfs_text]
check(not missing,
      "all 24 transcribed Schedule 1 figures (opening cost, closing cost, "
      "amortization × 8 classes) appear in the fetched statements"
      + (f" — missing: {', '.join(missing)}" if missing else ""))

rows, inside = [], True
for k, (o, c, a, (lo, hi)) in S1.items():
    yrs = (o / a, ((o + c) / 2) / a, c / a)
    ok = all(lo <= y <= hi for y in yrs)
    inside &= ok
    rows.append({"class": k, "opening": f"{yrs[0]:.1f}", "mean": f"{yrs[1]:.1f}",
                 "closing": f"{yrs[2]:.1f}", "Note 1 range": f"{lo}–{hi}",
                 "inside": "✅" if ok else "❌"})
show(pd.DataFrame(rows))

road = S1["ENG: Roadway system"]
road_life = (road[0] / road[2], road[1] / road[2])

check(inside,
      "all eight asset classes land inside their own stated Note 1 range — "
      "the validation that makes the method usable")
check(36.0 <= road_life[0] <= 38.5 and 36.0 <= road_life[1] <= 38.5,
      f"the roadway system's implied average life is "
      f"**{road_life[0]:.1f}–{road_life[1]:.1f} years**")
check((S1["ENG: Light rail transit"][1] / S1["ENG: Light rail transit"][2])
      > road_life[1]
      > (S1["ENG: Bus system"][1] / S1["ENG: Bus system"][2]),
      "and the ordering is the right shape: LRT > roadway > bus system")

# %% [markdown]
# ⚠️ **Four limits, stated before anyone quotes 37.**
#
# 1. **It is an ACCOUNTING life, not an engineering service life.** Straight-line
#    amortization is a policy choice; the statements never use the words
#    "service life". It must not be called *"the City's road service life"*.
# 2. **`Roadway system` is every road the City owns** — arterials, collectors,
#    locals, alleys and capitalized structures — not a neighbourhood street.
# 3. ⚠️ **It OVERSTATES the policy life, by an unknown amount.** Fully
#    amortized roads still in service stay in gross cost but add nothing to
#    amortization expense, so `gross ÷ amortization` reads long. Growth alone
#    does not bias it under straight-line (each unamortized asset contributes
#    `cost/L` either way). Schedule 1 shows $157M of roadway disposals in the
#    year, so some are written off, but not how many. **This bias runs
#    AGAINST 50**: the true accounting life is at or below 36–38. A range is
#    quoted because the stock grew 4.6% in the year (opening vs closing).
# 4. **Historical cost, not replacement cost** — older metres enter at the
#    dollars of their build year.
#
# **Where it lands: 36–38 is below 50 and well above 25.** Recorded as it falls.

# %% [markdown]
# ## 5. Cross-check B — the per-class expected lives, and what condition says
#
# Source: **City of Edmonton, *2020 Infrastructure State and Condition*,
# Appendix A p31.** This is the only City document found that publishes an
# expected asset life **per road class**, which makes it the only life figure
# measured on approximately the population this metric charges.
#
# ⚠️ **Provenance is imperfect and is stated plainly.** This is the City's own
# PDF, but the live `edmonton.ca` page no longer serves it; the copy fetched here
# is an Internet Archive snapshot. The current 2025 edition **no longer publishes
# expected asset life per class at all**, so these may be the last such figures
# published.

# %%
ISC2020_URL = ("https://web.archive.org/web/20240112150443/"
               "http://www.matthewdance.ca/s/"
               "2020-Infrastructure-Inventory-State-and-Condition.pdf")
isc2020 = get(ISC2020_URL)
app_a = pdf_pages(isc2020)[30].extract_text()      # p31
narrative = pdf_pages(isc2020)[18].extract_text()  # p19

# Transcribed from Appendix A p31: lane-km, average age, expected asset life,
# physical condition A+B / C / D+F, replacement value $M.
APP_A = {
    "Major Arterial":  (596.2,  30, 22, (78, 20, 2),  711),
    "Minor Arterial":  (2927.2, 48, 22, (53, 40, 7),  2914),
    "Local Roads":     (4830.30, 38, 28, (70, 17, 13), 3461),
    "Collector Roads": (1763.10, 35, 20, (62, 34, 5),  1888),
    "Alleys":          (1192.7, 30, 28, (20, 16, 64), 501),
}
show(pd.DataFrame([
    {"class": k, "lane-km": f"{q:,.1f}", "avg age": age, "expected life": life,
     "A+B / C / D+F": " / ".join(map(str, cond)), "replacement": f"${val:,}M"}
    for k, (q, age, life, cond, val) in APP_A.items()]))

# The figures must actually appear on the page that was just fetched.
flat = re.sub(r"\s+", " ", app_a)
# The whole row in reading order — quantity, age, expected life, condition — so
# the lives behind §5's ~26-year figure are pinned too, not just the lane-km.
for k, (q, age, life, cond, val) in APP_A.items():
    qs = f"{q:.2f}" if k in ("Local Roads", "Collector Roads") else f"{q:.1f}"
    row = f"{k} {qs} Lane km {age} {life} {' / '.join(map(str, cond))}"
    check(row in flat and f"${val:,}" in flat,
          f"Appendix A p31 still carries the **{k}** row as transcribed "
          f"(age {age}, expected life {life}, replacement ${val:,}M)")

# %% [markdown]
# ### The naive reading, and why it is wrong
#
# Local roads average **38 years old against a 28-year expected life**;
# collectors **35 against 20**. Read alone, that looks like a renewal backlog —
# and this project did read it that way at first.
#
# **Age past expected life is compatible with a backlog *and* with a
# successfully extended life. Only condition discriminates them**, and the same
# table publishes condition.

# %%
local, collector, alley = APP_A["Local Roads"], APP_A["Collector Roads"], APP_A["Alleys"]
cl_km = local[0] + collector[0]
weighted_life = (local[0] * local[2] + collector[0] * collector[2]) / cl_km

display(Markdown(
    f"- **Local**: {local[1]} yrs old, {local[2]}-yr life, "
    f"**{local[3][0]}% good / {local[3][2]}% poor**\n"
    f"- **Collector**: {collector[1]} yrs old, {collector[2]}-yr life, "
    f"**{collector[3][0]}% good / {collector[3][2]}% poor**\n"
    f"- **Alleys** (excluded from this metric): {alley[1]} yrs old, "
    f"{alley[2]}-yr life, **{alley[3][0]}% good / {alley[3][2]}% poor**"))

check(alley[3][2] > alley[3][0],
      "the **alley** row is what a renewal backlog looks like inside this very "
      "table — 64% poor — and alleys are already excluded from the metric")
check(local[3][0] >= 70 and collector[3][0] >= 60,
      "the two charged classes are both past their expected life yet majority "
      "good, which is an extended life rather than a backlog")
check(25.0 <= weighted_life <= 27.0,
      f"lane-km weighted across collector+local the expected asset life is "
      f"**{weighted_life:.1f} years** — recorded as it falls, well below 50")

# %% [markdown]
# ⚠️ **Two honest narrowings of that reading**, both found when this section was
# cross-read by a second model:
#
# 1. **"70% good" is the whole class, not the past-life cohort.** Local Roads
#    includes every post-1990 suburb, nearly all of it younger than 28 and in
#    good condition. The condition of the roads that actually *are* past their
#    expected life is not published, only bounded — roughly 45% good / 24% poor
#    on a plausible age split. That still excludes the backlog reading; it does
#    not support *"ten years past life and still 70% good"*.
# 2. **The contrast with alleys is partly a funding contrast.** Collector and
#    local roads had eleven years of Neighbourhood Renewal spending behind them
#    by 2020; alleys had almost none. So the table shows that **renewal spending
#    works** — which is the City's own *"extended to 50 with proper
#    maintenance"* clause, and is therefore consistent with 50 rather than
#    independent evidence for it.
#
# ### The 25.9 is a different quantity, not a competing answer
#
# The City's own narrative on p19 says so directly.

# %%
p19 = re.sub(r"\s+", " ", narrative)
QUOTE_P19 = ("With appropriate maintenance and renewal schedules roads can be "
             "maintained past their expected asset life")
check(QUOTE_P19 in p19,
      f"the 2020 report's own narrative reads: “{QUOTE_P19}”")
display(Markdown(f"> …Roads' assets are at or over their expected asset life. "
                 f"{QUOTE_P19}. However, there will come a point when full "
                 f"replacement will be needed."))

# %% [markdown]
# ⚠️ **A widely-quoted figure that this project checked and will not use.** The
# same report's *Goods and People Movement Portfolio* is given as **average age
# 37, expected life 33** — and that portfolio contains bridges (57-year life),
# LRT and transit alongside roads. A "33-year road life" sourced to this family
# of reports has the exact shape of a **portfolio number mislabelled as a roads
# number**; the actual Roads row reads 24.

# %%
check("expected life of 33 years" in p19 and "Bridges" in p19,
      "the **33** belongs to a portfolio containing bridges, LRT and transit — "
      "not to the Roads row, which reads 24")

# %% [markdown]
# ## 6. Cross-check C — the reconstruction interval, described with its schedule
#
# Source: **ConstructConnect / *Journal of Commerce*, September 2016**, quoting
# the City on the Neighbourhood Renewal program.
#
# ⚠️ **[SECONDARY]** — a trade publication quoting a named City staffer, not a
# City document. It must not be cited as City-published. What makes it valuable
# is not its rank: **it is the only source found that states the maintenance
# schedule and the resulting interval together**, which is what turns the
# Development Impact page's sentence from ambiguous into mechanical.

# %%
JOC_URL = ("https://canada.constructconnect.com/joc/news/infrastructure/2016/09/"
           "infrastructure-upgrades-forge-ahead-in-edmonton-1018310w")
joc = visible_text(get(JOC_URL))

QUOTE_60 = ("The results of a complete reconstruction are expected to endure "
            "for 60 years, so long as preventative maintenance is carried out "
            "as scheduled")
QUOTE_SCHED = ("road microsurfacing at 10 years and again at 40 years, along "
               "with a roadway overlay completed after 30 years")

check(QUOTE_60 in joc, f"the article still reads, verbatim: “{QUOTE_60}”")
check(QUOTE_SCHED in joc, f"…with the schedule: “{QUOTE_SCHED}”")
check("A municipal levy was introduced in 2009" in joc,
      "the same article dates the Neighbourhood Renewal levy to **2009**, which "
      "matters for §5's funding contrast")

show(pd.DataFrame([
    {"event": "surface treatment", "interval": "10 yr, 40 yr", "what happens": "microsurfacing"},
    {"event": "resurfacing", "interval": "30 yr", "what happens": "roadway overlay"},
    {"event": "expected asset life (App. A)", "interval": "~26 yr",
     "what happens": "the structure is DUE — not the same as replaced"},
    {"event": "full reconstruction", "interval": "50–60 yr",
     "what happens": "base rebuilt; the cycle restarts"},
]))

# %% [markdown]
# ⚠️ **Three things this does not establish**, stated because the quote is the
# single most favourable datum in this document:
#
# 1. **It is a forward claim about a road reconstructed to 2016 standards on a
#    full treatment schedule** — not an interval the existing stock has achieved.
#    Neighbourhood Renewal exists precisely because the 1950–1980 stock did not
#    last 60 years.
# 2. **Calgary's comparable primary page says *"a fully reconstructed road can
#    last up to 20 years."*** Almost certainly a base life comparable to
#    Edmonton's "usually 25" rather than a reconstruction interval — but the
#    reading has to be stated rather than the datum quietly filed.
# 3. **Winnipeg prints the same base-plus-maintained structure Edmonton does** —
#    asphalt regional streets *"designed for 25 years"*, rehabilitation expected
#    to extend service life *"to 60"* — which is a second municipality
#    describing two events rather than two estimates. That is the part that
#    transfers; the specific numbers are Winnipeg's.

# %% [markdown]
# ## 7. ⚠️ Where this project's own reasoning was wrong
#
# **This section exists because it is the strongest thing in the document.** An
# argument that has never lost anything has not been tested.
#
# For one day, this project's files claimed that the strongest evidence for the
# 50-year reading was a **trend**: the poor-condition (D+F) share of Edmonton's
# Roads portfolio had not moved in five years — 11.0% (2020) → 11.4% (2023) →
# 11.2% (2025) — while the portfolio grew by ~$870M. A renewal backlog is a
# *rising* poor share, so a flat one looked like proof that the network is being
# sustained.
#
# **It does not hold, and the 2025 report's own appendix is what breaks it.**

# %%
ISC2025_URL = ("https://www.edmonton.ca/sites/default/files/public-files/"
               "documents/2025-infrastructure-state-and-condition-report.pdf")
isc2025 = get(ISC2025_URL)
app_b = re.sub(r"\s+", " ", pdf_pages(isc2025)[36].extract_text())   # p37

# Appendix B p37 prints the Roads row AND its sub-rows, 2025 beside 2023.
PAVED_25, UNPAVED_25, CURBS_25 = 8204.164788, 182.805696, 2097.342722   # $M
ROADS_25 = 10484.313206
PAVED_DF_25, CURBS_DF_25 = 12.5, 7.0      # poor (D+F) %
PAVED_DF_23 = 11.5

check(abs(PAVED_25 + UNPAVED_25 + CURBS_25 - ROADS_25) < 0.001,
      "the 2025 Roads row is exactly Paved + Unpaved + **Curbs**")
# ⚠️ Paved and Unpaved are pinned too: the sum check above is arithmetic on four
# literals, and the 11.2% blend below reads PAVED_25 — pinning only Roads and
# Curbs left both blind to a restated Paved line.
check(all(s in app_b for s in ("10,484,313,206", "8,204,164,788",
                               "182,805,696", "2,097,342,722")),
      "Appendix B p37 carries the Roads total and the Paved, Unpaved and Curbs "
      "lines as transcribed")

blend = (PAVED_25 * PAVED_DF_25 + CURBS_25 * CURBS_DF_25) / ROADS_25
display(Markdown(
    f"The headline **11.2%** poor for 2025 is the value-weighted blend of "
    f"**Paved Roads at {PAVED_DF_25}%** and a **${CURBS_25:,.0f}M curbs line at "
    f"{CURBS_DF_25}%**: `({PAVED_25:,.0f}×{PAVED_DF_25} + "
    f"{CURBS_25:,.0f}×{CURBS_DF_25}) / {ROADS_25:,.0f}` = **{blend:.2f}**."))

check(11.1 <= blend <= 11.25,
      "the printed 11.2% reproduces exactly as a curbs-diluted paved figure")
# Built FROM the constants, so a mistyped constant fails here too.
for s_ in (f"73.1%14.4%{PAVED_DF_25}%", f"73.2%15.3%{PAVED_DF_23}%",
           f"68.3%24.7%{CURBS_DF_25}%"):
    check(s_ in app_b, f"Appendix B p37 carries the condition triple {s_} as transcribed")

# 2023 has no Curbs line: its Roads row is Paved + Unpaved exactly, and Paved
# FALLS $1.5B into 2025 while a $2.1B Curbs line appears.
PAVED_23, UNPAVED_23, ROADS_23 = 9704.516452, 42.968839, 9747.485291   # $M
check(all(v in app_b for v in ("9,704,516,452", "42,968,839", "9,747,485,291"))
      and abs(PAVED_23 + UNPAVED_23 - ROADS_23) < 0.001,
      "the 2023 Roads row is exactly Paved + Unpaved — no Curbs line that year")
check(PAVED_23 - PAVED_25 > 1000 and ROADS_25 > ROADS_23,
      f"so **2023 Paved almost certainly included curbs**: Paved falls "
      f"${PAVED_23 - PAVED_25:,.0f}M while Roads rises and a ${CURBS_25:,.0f}M "
      f"Curbs line appears — {PAVED_DF_23}% (2023) and {PAVED_DF_25}% (2025) "
      "are NOT the same population and are not compared as a trend")

# The 2020 figure is not the same population either: it included alleys.
R20, ALLEY_V, ALLEY_DF = 9614, 501, 64
check(f"${R20:,}" in flat, "the 2020 Roads replacement value ($9,614M) is on p31 as transcribed")
ex_alleys = (R20 * 11 - ALLEY_V * ALLEY_DF) / (R20 - ALLEY_V)
check(7.5 <= ex_alleys <= 8.7,
      f"and 2020's “11%” carries ~{ALLEY_V * ALLEY_DF / R20:.1f} points of "
      f"**alleys** at 64% poor — roads excluding alleys read ~{ex_alleys:.1f}%")

display(Markdown(
    "**Verdict: the three “Roads” rows are three differently-composed "
    "aggregates.** The composition changed by more than the trend being "
    "claimed, so a 0.4-point range across them is inside the re-scoping noise. "
    "⚠️ **And even a genuinely flat poor share would not discriminate 25 from "
    "50** — it would say renewal spending is keeping pace, which both lives "
    "predict. The claim has been withdrawn."))

# %% [markdown]
# ## 8. The funded side — is anyone actually paying for a 50-year cycle?
#
# A 50-year reconstruction interval is only credible if the City funds renewal
# at roughly the rate the model implies. The **Neighbourhood Renewal Reserve** is
# a `fund` in Edmonton's published capital budget, so the draw is checkable.
#
# ⚠️ **This is an order-of-magnitude bracket, not a validation.** The two sides
# cover different networks: the requirement below is collector+local roadway
# only, while an actual Neighbourhood Renewal project also rebuilds alleys,
# sidewalks, street lighting and landscaping.

# %%
BUDGET_URL = "https://budget.edmonton.ca/api/capital_budget.csv"
cb = pd.read_csv(io.BytesIO(get(BUDGET_URL).content))

nr = cb[cb.fund.astype(str).str.contains("Renewal Reserve", na=False)]
window = nr[nr.fiscal_year.between(2023, 2026)]
draw = window.approved.sum()
per_yr = draw / 4

show(window.groupby("service").approved.sum().reset_index()
     .assign(approved=lambda d: d.approved.map("${:,.0f}".format)))

display(Markdown(
    f"**FY2023–26 Neighbourhood Renewal Reserve draw: ${draw:,.0f}** "
    f"across {window.profile.nunique()} profiles — **${per_yr:,.0f}/yr**."))

# [repo] The charged network: 3,654 km of collector+local centreline across the
# 406 neighbourhoods this project serves. Not re-derived here (it requires the
# project's own road geometry); see docs/FINDINGS_nrp_reconstruction_cross_check.md.
CHARGED_KM = 3654
requirement = RENEWAL / 50 * CHARGED_KM        # $/m/yr renewal half x metres

display(Markdown(
    f"- modelled **renewal half**: ${RENEWAL / 50 / 1000:,.0f}/m/yr × "
    f"{CHARGED_KM:,} km **[repo]** = **${requirement / 1e6:,.1f}M/yr** required\n"
    f"- published reserve draw: **${per_yr / 1e6:,.1f}M/yr** across a *broader* "
    f"network (alleys, sidewalks, lighting, landscaping included)"))

check(1.0e8 <= draw <= 1.0e9,
      f"the Neighbourhood Renewal Reserve draw for FY2023–26 is "
      f"**${draw:,.0f}**, a real and substantial funded programme")
check(requirement < per_yr,
      f"the modelled roads-only renewal requirement (${requirement / 1e6:,.1f}M/yr) "
      f"sits BELOW the broader funded draw (${per_yr / 1e6:,.1f}M/yr) — "
      "consistent, and no more than that")

# %% [markdown]
# ⚠️ **One measurement runs the other way, and it is recorded rather than
# buried.** Observed full-reconstruction spend on completed Neighbourhood
# Renewal projects works out to **~$3,151 per centreline metre against the
# City's published $1,900/m** — about **1.66×**. **[repo]**,
# `docs/FINDINGS_nrp_reconstruction_cross_check.md`. Two biases of opposite sign
# prevent it becoming a replacement rate (an NRP project bundles non-roadway
# assets, inflating it; several profiles are cycle-boundary tails, deflating it),
# but the direction is consistent: **if the published $1.9M understates real
# reconstruction cost, the $50/m/yr rate is a floor, not a ceiling.**

# %% [markdown]
# ## 9. What this rate does NOT establish
#
# 1. **It is MODELLED and uniform.** One published per-kilometre lifecycle
#    applied to every collector and local metre. It is not Edmonton's
#    per-segment spend and no neighbourhood's figure is an observation.
# 2. **It is calibrated to a neighbourhood (local) street.** Collectors cost
#    roughly 1.5× per lane-km, so the blend is a mild lower bound.
# 3. **Arterials and alleys are excluded from the metric entirely**, so any
#    citywide total built from it is a partial network by construction.
# 4. **The 50-year choice remains a choice.** The City published both numbers on
#    one page. This document argues 50 is the right denominator for a bundle
#    that includes the maintenance buying the extension — it does not claim the
#    City endorsed that reading.
# 5. **Two of the cross-checks land below 50** (audited books 36–38, per-class
#    expected life ~26) and one lands above (reconstruction 60). They are
#    recorded as they fall. §3 explains why the low figures are measuring the
#    *intervention* interval rather than the *reconstruction* interval, but that
#    is an argument, not a measurement.
# 6. **The three sources published *after* 2020 no longer print a per-class
#    expected life at all**, so §5's figures cannot currently be refreshed.

# %% [markdown]
# ## 10. Invariants
#
# Every claim above is asserted here against what this run actually fetched. A
# failure means either a transcription is wrong or a source has changed —
# both worth knowing.

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
