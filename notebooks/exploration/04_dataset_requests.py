# ---
# jupyter:
#   title: What people ask Edmonton Open Data for, and what happens to it
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
# # What people ask Edmonton Open Data for, and what happens to it
#
# **Dataset:** *Dataset Requests* (`a9w6-s3na`) on `data.edmonton.ca`. It is
# refreshed daily and holds every request since automated intake began on
# 2016-01-26.
#
# **Two jobs:**
#
# 1. **Duplicate check (§6).** Before this project sends a data request, find
#    out whether someone has already asked for it and what the City answered.
# 2. **Landscape (§3–§5).** What people request over time, what gets published,
#    and what gets refused or left open.
#
# ⚠️ **Read §2 before quoting any count.** The table mixes two intake systems
# with different status vocabularies. In December 2023, 126 old requests that
# had never been decided were moved to the new tracker, and on the old system
# they were stamped `Rejected` or `Declined` as they went. A single-day bulk
# edit in August 2026 also reset `status_date` on 241 rows. Counted naively,
# the table double-counts requests, **overstates refusals by 2.6×**, and
# misdates decisions.
#
# ## Reproducing
#
# ```
# pip install pandas matplotlib certifi
# ```
#
# Public endpoint, no API token.

# %%
import json
import re
import ssl
import urllib.parse
import urllib.request
from datetime import datetime, timezone

import certifi
import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import Markdown, display

UA = "edmonton-tax-viz/dataset-requests (open-data landscape)"
SSL_CTX = ssl.create_default_context(cafile=certifi.where())
RUN_AT = datetime.now(timezone.utc)
REQUESTS = "a9w6-s3na"
LIMIT = 50000

pd.set_option("display.max_colwidth", 90, "display.width", 200)

CHECKS: list[tuple[bool, str]] = []


def check(ok: bool, claim: str) -> None:
    CHECKS.append((bool(ok), claim))
    print(f"  [{'PASS' if ok else 'FAIL'}] {claim}")


def soda(dataset: str, params: dict) -> list[dict]:
    url = (f"https://data.edmonton.ca/resource/{dataset}.json?"
           + urllib.parse.urlencode(params))
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, context=SSL_CTX, timeout=120) as r:
        return json.loads(r.read())


raw = pd.DataFrame(soda(REQUESTS, {"$limit": LIMIT}))
d = raw.copy()
for c in ["request_creation_date", "status_date", "dataset_published_date"]:
    d[c] = pd.to_datetime(d[c])
d["department"] = d["department"].fillna("(blank)")

display(Markdown(f"**Snapshot.** Executed against live data **{RUN_AT:%Y-%m-%d}** "
                 f"(UTC): **{len(d):,} requests**, created "
                 f"{d.request_creation_date.min():%Y-%m-%d} to "
                 f"{d.request_creation_date.max():%Y-%m-%d}. The source changes "
                 "daily, so re-execute before citing a figure."))
check(len(d) < LIMIT, f"one page holds the whole table ({len(d)} < {LIMIT}), so no rows were cut off")
check(d.request_number.is_unique, "request_number is unique")

# %% [markdown]
# ## 1. Two intake systems, two status vocabularies
#
# `request_number` gives away which system took the request:
#
# * **`ODRyy-nnn`**: the original intake, from 2016 until its last entry in
#   2024. Statuses are Title-case: `Completed`, `Rejected`, `Declined`,
#   `Cancelled`, `New`.
# * **Opaque ids such as `868…`**: the newer tracker, from October 2021 on.
#   Statuses are UPPER-case: `NEW`, `IN PROGRESS`, `PAUSED`, `CLOSED`.
#
# ⚠️ **The newer system has no way to say "refused" and no way to say
# "published".** Everything that ends goes to `CLOSED`. Old-system outcomes
# therefore can't be compared one-for-one with new-system outcomes, and
# `CLOSED` is shown below as its own bucket instead of being folded into
# "done".

# %%
d["system"] = d.request_number.str.startswith("ODR").map({True: "ODR (old)", False: "tracker (new)"})
print(pd.crosstab(d.status, d.system, margins=True))
print()
print(d.groupby("system").request_creation_date.agg(["min", "max", "count"]))

OUTCOME = {
    "Completed": "Completed",
    "Rejected": "Refused", "Declined": "Refused",
    "CLOSED": "Closed (reason not given)",
    "NEW": "Open", "New": "Open", "IN PROGRESS": "Open", "PAUSED": "Open",
    "Cancelled": "Withdrawn",
}
d["outcome"] = d.status.map(OUTCOME)
unmapped = sorted(d.loc[d.outcome.isna(), "status"].unique())
check(not unmapped, f"every status maps to an outcome bucket (unmapped: {unmapped or 'none'})")
d["outcome"] = d.outcome.fillna("Unmapped")

# %% [markdown]
# ### `dataset_published_date` on a `CLOSED` row does not mean something was published
#
# Every `CLOSED` row has a `dataset_published_date`, including requests the
# City could not have fulfilled publicly. One example is below. On the new
# tracker the field is best read as "date closed".

# %%
closed = d[d.status == "CLOSED"]
check(closed.dataset_published_date.notna().all(),
      f"all {len(closed)} CLOSED rows carry a dataset_published_date")
ex = d[d.request_details.fillna("").str.contains("will not be publicly visible")]
print(ex[["request_number", "status", "dataset_published_date", "request_description", "request_details"]].to_string(index=False))

# %% [markdown]
# ## 2. Two artifacts that distort naive counts
#
# ### 2a. The December 2023 migration: "Rejected" here means "moved"
#
# On 2023-12-12 and 2023-12-13, old-system requests were re-entered in the new
# tracker under new ids and new creation dates. On the **same two days**, their
# old-system rows were set to `Rejected` or `Declined`. The pairs are matched
# by normalised title, restricted to old rows whose `status_date` falls on
# those two days.
#
# These were **not refusals**. The request carried on in the new tracker, and
# many are still open there. Most had been created years earlier with no
# status change since, so they had simply **never been decided**. Taking the
# old status at face value overstates refusals.
#
# The notebook handles the pairs as follows:
#
# * **Volume over time:** each pair is counted once, in the year the request
#   was first made. The new-tracker row is dropped.
# * **Outcome:** the old row takes its outcome from the new-tracker row, which
#   is where the request actually stands now. A `moved` flag records that it
#   was never decided on the old system.

# %%
norm = lambda s: re.sub(r"[^a-z0-9]", "", str(s).lower())
d["title_key"] = d.request_description.map(norm)
MIGRATION_DAYS = {"2023-12-12", "2023-12-13"}
on_migration_day = d.status_date.dt.strftime("%Y-%m-%d").isin(MIGRATION_DAYS)
created_on_migration_day = d.request_creation_date.dt.strftime("%Y-%m-%d").isin(MIGRATION_DAYS)

odr_stamped = d[(d.system == "ODR (old)") & on_migration_day]
new_side = d[(d.system == "tracker (new)") & created_on_migration_day]
pairs = odr_stamped.merge(new_side, on="title_key", suffixes=("_orig", ""))
check(pairs.request_number_orig.is_unique and pairs.request_number.is_unique,
      f"migration pairs match one-to-one by title ({len(pairs)} pairs)")

d["reintake"] = d.request_number.isin(pairs.request_number)
d["moved"] = d.request_number.isin(pairs.request_number_orig)
d.loc[d.moved, "outcome"] = d.loc[d.moved, "request_number"].map(
    pairs.set_index("request_number_orig").outcome)

print(f"old-system rows stamped on the migration days: {len(odr_stamped)}")
print(f"  ...of which paired with a new-tracker row:    {len(pairs)}")
print("\nOld-system stamp  ×  where the request stands now (new tracker):")
print(pd.crosstab(pairs.status_orig, pairs.status, margins=True))
print("\nOld-system creation year of the moved requests:")
print(pairs.request_creation_date_orig.dt.year.value_counts().sort_index().to_string())
check(len(pairs) >= 100, f"the Dec-2023 migration is still visible ({len(pairs)} pairs)")
check(len(odr_stamped) - len(pairs) <= 2,
      f"nearly every old row stamped on the migration days was moved "
      f"({len(pairs)} of {len(odr_stamped)}), so the stamp means 'moved', not 'refused'")
check(set(odr_stamped.status) <= {"Rejected", "Declined"},
      "every migration-day stamp is Rejected/Declined, the statuses a naive reading counts as refusals")

# %% [markdown]
# ### 2b. `status_date` is the date the row was last edited, not the date of the decision
#
# Large blocks of rows share a single `status_date`. That is a bulk edit, not
# hundreds of decisions made on one day. Durations such as "time to decision"
# computed from `status_date` are therefore unreliable on the new tracker, and
# this notebook doesn't compute them.

# %%
top_days = d.status_date.dt.date.value_counts().head(5)
print(top_days)
biggest = top_days.index[0]
print(f"\n{biggest}: statuses on the bulk-edit day")
print(d[d.status_date.dt.date == biggest].status.value_counts())
check(top_days.iloc[0] >= 100, f"a bulk status_date sweep is present ({top_days.iloc[0]} rows on {biggest})")

# %% [markdown]
# ## 3. Volume over time
#
# Requests by the year they were **first** made, each counted once (§2a).
# Colours show each request's current outcome. Moved requests show where they
# stand on the new tracker.

# %%
u = d[~d.reintake].copy()
u["year"] = u.request_creation_date.dt.year
ORDER = ["Completed", "Refused", "Closed (reason not given)", "Open", "Withdrawn"]
COLOURS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]  # dataviz reference palette, slots 1-5 in order
by_year = pd.crosstab(u.year, u.outcome).reindex(columns=ORDER, fill_value=0)
display(by_year.assign(total=by_year.sum(axis=1)))

fig, ax = plt.subplots(figsize=(9, 4.2))
bottom = pd.Series(0, index=by_year.index)
for col, colour in zip(ORDER, COLOURS):
    ax.bar(by_year.index, by_year[col], bottom=bottom, color=colour, label=col,
           width=0.72, edgecolor="#fcfcfb", linewidth=1.5)
    bottom += by_year[col]
ax.set_title("Dataset requests by year first made, coloured by current outcome", loc="left", fontsize=11)
ax.set_ylabel("requests")
ax.set_xticks(by_year.index)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", color="#e6e5e0", linewidth=0.8)
ax.set_axisbelow(True)
ax.legend(frameon=False, fontsize=8, ncol=5, loc="upper center", bbox_to_anchor=(0.5, -0.1))
this_year = RUN_AT.year
ax.annotate(f"{this_year}: part-year", (this_year, by_year.loc[this_year].sum() if this_year in by_year.index else 0),
            textcoords="offset points", xytext=(0, 6), ha="center", fontsize=8, color="#52514e")
plt.tight_layout()
plt.show()

# %% [markdown]
# **How to read it:**
#
# * 2016 was the intake's first year and is its busiest. Only 11 of its rows
#   are hackathon whiteboard captures (measured 2026-09-22), so hackathons
#   don't explain the peak.
# * Everything filed after the switch to the new tracker is either
#   `Closed (reason not given)` or still `Open`. The drop in blue and orange
#   after 2022 comes from the vocabulary change in §1. It is not a change in
#   how the City decides.
# * Green and yellow before 2021 are the moved requests: they were never
#   decided on the old system, and they now sit on the new tracker.

# %% [markdown]
# ## 4. What people request
#
# Topics are assigned by keyword over title and details. Each request goes to
# the **first** topic in the list below that matches, so every request is
# counted once. This is a transparent heuristic, not a classifier, and the
# patterns are printed so they can be argued with.

# %%
TOPICS = [
    ("Transit", r"\bets\b|transit|\bbus|lrt|gtfs|arc card|ridership|\btrain"),
    ("Property, assessment & tax", r"assess|parcel|propert|\btax|\blot\b|lot size|title"),
    ("Planning, permits & zoning", r"permit|zoning|land use|development|bylaw \d|\barp\b|rezon|licen[cs]e"),
    ("Roads, traffic & mobility", r"road|traffic|collision|speed|parking|snow|sidewalk|bike|cycl|pathway|pedestrian|intersection|radar|scooter|micromobility|bridge|pedway"),
    ("Utilities & drainage", r"drain|sewer|water|epcor|\bgas\b|power|electric|utilit"),
    ("Public safety", r"crime|police|fire|911|emergenc|bylaw enforcement|complain"),
    ("Parks, trees & environment", r"\bpark|tree|green|waste|garbage|trash|recycl|climate|emission|river|ravine|natural area|cemeter|washroom|picnic|graffiti|ashtray|flood"),
    ("Recreation, library & community", r"recreation|library|leisure|community|arena|pool|school|playground"),
    ("People & census", r"census|population|demograph|income|housing|homeless|senior"),
    ("Budget & spending", r"budget|spend|\bcost|expend|revenue|contract|procure|salar|financial statement|expense|severance|capital project|renewal invest|funding|earnings"),
    ("Council, elections & administration", r"council|election|\bward|voting|candidate|meeting|motion|agenda|lobby|foip|\b311\b|job|rfp|disclosure"),
    ("Base maps & imagery", r"lidar|orthophoto|imagery|elevation|\bdem\b|postal code|neighbou?rhood (?:dataset|boundar)|manhole|historic resource"),
]


def topic_of(text: str) -> str:
    t = text.lower()
    for name, pat in TOPICS:
        if re.search(pat, t):
            return name
    return "Other / unclassified"


u["text"] = u.request_description.fillna("") + " " + u.request_details.fillna("")
u["topic"] = u.text.map(topic_of)
u["era"] = pd.cut(u.year, [2015, 2019, 2022, 2100], labels=["2016–19", "2020–22", "2023–now"])
tt = pd.crosstab(u.topic, u.era, margins=True, margins_name="all").sort_values("all", ascending=False)
display(tt)
print(f"unclassified: {(u.topic == 'Other / unclassified').mean():.0%} of requests")

# %% [markdown]
# ## 5. What gets through, what gets refused, what never gets decided
#
# ### 5a. Old system, by the year a request was first made
#
# The old system is the only one that records an explicit outcome. Each old
# request lands in one of four groups:
#
# * **Completed**
# * **Refused**: `Rejected` or `Declined`, excluding the migration stamps
# * **Never decided**: moved to the new tracker in December 2023
# * **Withdrawn / still open**

# %%
old = u[u.system == "ODR (old)"].copy()
old["fate"] = "Withdrawn / still open"
old.loc[old.status == "Completed", "fate"] = "Completed"
old.loc[old.outcome == "Refused", "fate"] = "Refused"
old.loc[old.moved, "fate"] = "Never decided (moved)"
FATES = ["Completed", "Refused", "Never decided (moved)", "Withdrawn / still open"]
fy = pd.crosstab(old.year, old.fate).reindex(columns=FATES, fill_value=0)
fy["completed share"] = (fy.Completed / fy[FATES].sum(axis=1)).round(2)
display(fy)
tot = old.fate.value_counts()
print(f"old system overall: {tot.get('Completed', 0)} completed, {tot.get('Refused', 0)} refused, "
      f"{tot.get('Never decided (moved)', 0)} never decided, of {len(old)}")
naive = old.status.isin(["Rejected", "Declined"]).sum()
print(f"a naive count of Rejected+Declined gives {naive} refusals; "
      f"the real figure is {tot.get('Refused', 0)} ({naive / max(tot.get('Refused', 1), 1):.1f}× overstated)")

# %% [markdown]
# **How to read it:** after 2016 the City rarely says no outright. What
# changed was how many requests **never got an answer**. From 2017 on, more
# requests ended up in "never decided" than in "refused" in every year. The
# completed share falls from roughly 0.4–0.5 in 2016–2018 to about one in
# eight in 2022–2023. 2021 is the exception, and it has only 16 requests.
#
# Real refusals are concentrated in **utilities**: gas and power mapping, and
# infrastructure owned by EPCOR or other outside parties. Utilities & drainage
# is the only topic in §5b with more refusals than completions. Base maps &
# imagery has too few requests to say.

# %% [markdown]
# ### 5b. By topic, old system
#
# Topics use the same keyword heuristic as §4. Counts per topic are small, so
# read the table for its broad shape, not for rank order.

# %%
bt = pd.crosstab(old.topic, old.fate).reindex(columns=FATES, fill_value=0)
bt["n"] = bt[FATES].sum(axis=1)
bt["completed share"] = (bt.Completed / bt.n).round(2)
display(bt.sort_values("n", ascending=False))

# %% [markdown]
# ### 5b′. The genuine refusals
#
# These are old-system `Rejected` or `Declined` rows that the migration didn't
# stamp, most recent first. The table records no reason for any refusal, so
# only the titles are available.

# %%
real_refusals = old[old.fate == "Refused"].sort_values("request_creation_date", ascending=False)
print(real_refusals[["request_number", "status", "request_creation_date", "request_description"]]
      .assign(request_creation_date=lambda t: t.request_creation_date.dt.date).head(30).to_string(index=False))

# %% [markdown]
# ### 5c. The open backlog
#
# Requests still `NEW`, `IN PROGRESS` or `PAUSED`, aged from the **original**
# request date. A moved request is counted once and dated back to its
# old-system original.

# %%
orig_date = pairs.set_index("request_number").request_creation_date_orig
d["first_asked"] = d.request_number.map(orig_date).fillna(d.request_creation_date)
openq = d[(d.outcome == "Open") & ~d.moved].copy()
openq["age_years"] = ((pd.Timestamp(RUN_AT.date()) - openq.first_asked.dt.tz_localize(None)).dt.days / 365.25).round(1)
print(f"{len(openq)} open requests; median age {openq.age_years.median()} years; "
      f"{(openq.age_years >= 5).sum()} first asked five or more years ago")
print(openq.status.value_counts().to_string())
print("\nOldest ten:")
print(openq.sort_values("first_asked")[["request_number", "status", "first_asked", "request_description"]]
      .head(10).assign(first_asked=lambda t: t.first_asked.dt.date).to_string(index=False))

# %% [markdown]
# ### 5d. Asked again and again
#
# Titles that appear more than once after the re-intake is removed, meaning
# different people asked for the same thing. Titles are grouped loosely, by a
# keyword such as "parcel", because requesters word the same ask differently.
# A cluster here is demand the City has seen repeatedly.

# %%
CLUSTERS = {
    "parcel / lot polygons": r"parcel|lot (?:line|polygon|boundar)",
    "property assessment extra fields / history": r"assess",
    "zoning": r"zoning",
    "transit ridership / ARC": r"ridership|arc card",
    "crime": r"crime",
    "snow": r"snow",
    "trees": r"tree",
}
rows = []
for name, pat in CLUSTERS.items():
    hit = u[u.request_description.fillna("").str.lower().str.contains(pat)]
    rows.append((name, len(hit), hit.year.min(), hit.year.max(),
                 ", ".join(f"{k} {v}" for k, v in hit.outcome.value_counts().items())))
display(pd.DataFrame(rows, columns=["cluster (title match)", "requests", "first", "last", "outcomes"])
        .sort_values("requests", ascending=False))

# %% [markdown]
# ### 5e. New tracker: did a `CLOSED` request produce a dataset?
#
# The new tracker's `CLOSED` doesn't say whether anything was published
# (§1). The catalogue can help. For each closed request, this looks for a
# portal asset **created within 45 days** of the close date whose name shares
# at least two content words with the request title.
#
# ⚠️ **This check misses a lot.** Many fulfilled requests extend an existing
# dataset instead of creating a new one, and requesters' titles don't match
# the City's dataset names. The same check is run on old-system `Completed`
# rows, whose outcome is known, to measure how much it misses. That catch rate
# is used to scale the `CLOSED` figure into a rough estimate.

# %%
cat_rows, off = [], 0
while True:
    page = json.loads(urllib.request.urlopen(urllib.request.Request(
        "https://api.us.socrata.com/api/catalog/v1?" + urllib.parse.urlencode(
            {"domains": "data.edmonton.ca", "limit": 1000, "offset": off}),
        headers={"User-Agent": UA}), context=SSL_CTX, timeout=120).read())["results"]
    cat_rows += [{"name": r["resource"]["name"], "created": r["resource"]["createdAt"]} for r in page]
    off += 1000
    if len(page) < 1000:
        break
cat = pd.DataFrame(cat_rows)
cat["created"] = pd.to_datetime(cat.created).dt.tz_localize(None)
STOP = set("the of and a in to for data dataset edmonton city by on with from all at or is be "
           "map maps list request information open current".split())
words = lambda s: {w for w in re.findall(r"[a-z]{3,}", str(s).lower()) if w not in STOP}
cat["words"] = cat.name.map(words)
print(f"catalogue: {len(cat):,} assets")


def catalogue_match(row):
    near = cat[(cat.created - row.dataset_published_date).abs() <= pd.Timedelta(days=45)]
    rw = words(row.request_description)
    best = max(((len(rw & cw), n) for n, cw in zip(near.name, near.words)), default=(0, None))
    return best[1] if best[0] >= 2 else None


res = {}
for label, rows in [("old Completed (known published)", d[(d.status == "Completed") & d.dataset_published_date.notna()]),
                    ("new CLOSED (unknown)", d[(d.status == "CLOSED") & ~d.moved])]:
    m = rows.apply(catalogue_match, axis=1)
    res[label] = (len(rows), m.notna().sum())
    if label.startswith("new"):
        closed_hits = rows.assign(match=m)[m.notna()][["request_number", "request_description", "match"]]
recall = res["old Completed (known published)"][1] / res["old Completed (known published)"][0]
n_closed, h_closed = res["new CLOSED (unknown)"]
for k, (n, h) in res.items():
    print(f"{k:34} {h:3} of {n:3} matched")
print(f"\ncatch rate on known-published requests: {recall:.0%}")
print(f"rough estimate of CLOSED requests that produced a new asset: {h_closed / recall:.0f} of {n_closed} "
      f"(~{h_closed / recall / n_closed:.0%})")
print(closed_hits.to_string(index=False))

# %% [markdown]
# **How to read it:** on the known-published old `Completed` requests, the
# check catches only a minority. It catches a much smaller share of new
# `CLOSED` requests. Even after scaling for what the check misses, most
# `CLOSED` requests don't appear to have produced a new catalogue asset.
# Some may have been answered by pointing to an existing dataset, which
# nothing here can see. **Treat the estimate as an order of magnitude**, and
# read the matched titles rather than the percentage.

# %% [markdown]
# ## 6. Duplicate check: has anyone already asked for what we are about to ask?
#
# Each project ask is searched against title and details, including the
# re-intake rows, so no answer is missed. The asks come from
# `docs/DATA_ISSUES.md`. Two are **dataset requests** (issues 4 and 5). The
# rest are **defect reports** about datasets that already exist, which would
# not normally go through this channel. They are searched anyway, to catch
# anyone who reported the same problem as a request.
#
# ⚠️ **No hits means no match for these patterns on the run date.** Read the
# near-misses before concluding that nobody asked.

# %%
OUR_ASKS = [
    ("Issue 4: taxable/exempt status per assessment account",
     r"exempt|non-?taxable|tax code|tax status|liabilit"),
    ("Issue 5: school locations for private / charter / francophone operators",
     r"private school|charter|francophone|independent school|school (?:site|location)"),
    ("Issue 1: q7d6-ambg 'Period of Coverage' year",
     r"q7d6|period of coverage|current calendar year"),
    ("Issue 3: historical assessment roll (qi6a-xuwt) gaps",
     r"qi6a|historical (?:property )?assess"),
    ("Issue 6: permits' neighbourhood field (24uj-dj8v)",
     r"24uj|building permit.*neighbourhood|general building permit"),
    ("Issue 7: stt5-pzaa frozen",
     r"stt5"),
    ("Context: other asks for more assessment fields",
     r"assessment (?:data|variables|dataset)|additional fields|lot (?:size|width)"),
]
text_all = (d.request_description.fillna("") + " " + d.request_details.fillna("")).str.lower()
summary = []
for label, pat in OUR_ASKS:
    hit = d[text_all.str.contains(pat, regex=True)]
    summary.append((label, len(hit)))
    display(Markdown(f"#### {label}\n`{pat}`: **{len(hit)} hit(s)**"))
    if len(hit):
        display(hit.sort_values("request_creation_date")
                [["request_number", "request_creation_date", "status", "department", "request_description"]]
                .assign(request_creation_date=lambda t: t.request_creation_date.dt.date)
                .reset_index(drop=True))

# %% [markdown]
# ### What the hits mean for each ask
#
# (Written against the run of 2026-09-22. Re-read the tables above when
# re-executing.)
#
# * **Issue 4 (exemption status):** nobody has requested it. The request
#   would be new. The context block lists other requests for more assessment
#   fields. They run from 2016 to 2026, and most were never decided or were
#   closed without a stated reason. `868ev4dbu`, which asks for a list of assessment
#   variables, is still `NEW`. A draft could cite this record, and should be
#   ready for a similar answer.
# * **Issue 5 (schools):** every earlier request was for **school-site
#   polygons** for the two public boards. `ODR19-241` (public schools) was
#   Completed. The Catholic request (`ODR19-263`) was never decided on the old
#   system. It was moved in December 2023 and is now `CLOSED` as `8686qh58b`. Nobody has asked for
#   private, charter or francophone operators. The request would be new, and
#   those precedents are worth citing.
# * **Issue 6 (permits):** nobody has reported the defect. One related ask,
#   **adding the assessment account number to the General Building Permit
#   dataset** (`ODR20-301`, never decided, moved as `8686qhh84`, still `NEW`),
#   would give permits a clean join key. It is worth mentioning alongside the
#   defect report.
# * **Issues 1, 3 and 7:** nobody has reported these defects. The hits only
#   share wording: the dataset's own title contains "Current Calendar Year",
#   and the historical-assessment requests ask for years **before 2012**, not
#   for accounts missing from 2012 onward. That was expected, because defect
#   reports go to `opendata@edmonton.ca`, not to the request form.

# %%
display(pd.DataFrame(summary, columns=["ask", "hits"]))

# %% [markdown]
# ## Invariants
#
# These guard the notebook's own readings of the data: the re-intake, the
# bulk-edit date, and the status mapping. If one fails, the upstream table has
# changed shape and the prose above is stale.

# %%
passed = sum(1 for ok, _ in CHECKS if ok)
display(Markdown(f"### {passed} of {len(CHECKS)} invariants passed"))
for ok, claim in CHECKS:
    print(f"  [{'PASS' if ok else 'FAIL'}] {claim}")
if passed != len(CHECKS):
    raise AssertionError(f"{len(CHECKS) - passed} invariant(s) failed — see above")
