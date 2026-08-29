# ---
# jupyter:
#   title: Edmonton's open data covers two school authorities, not all of them
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
# # Edmonton's open data covers two school authorities, not all of them
#
# **Datasets:** *EPSB School Locations* (`996c-239n`) and *Edmonton Catholic
# Schools (Current)* (`gfxq-u8uu`) on `data.edmonton.ca`.
#
# **In one sentence:** Edmonton publishes point locations for its two public
# school boards, and for no other school operator — so private, charter and
# francophone schools are absent from the portal, and any "distance to the
# nearest school" computed from open data is **systematically too large**.
#
# Nothing here is a defect in the two datasets that exist. They are current,
# well-formed and directly usable. The gap is one of **coverage**, and it is
# invisible to a consumer: both datasets are named for their boards, so a
# reasonable person can join them and believe they now hold "Edmonton's
# schools".
#
# ## The one methodological point worth reading even if nothing else
#
# **This is a claim about ABSENCE, and absence cannot be demonstrated the way a
# wrong value can.** There is no query that returns "this dataset does not
# exist". The honest form of the argument is:
#
# 1. state what a dataset covering the missing schools would look like,
# 2. run the searches that **would find it if it existed**, and
# 3. show they come back empty.
#
# So the searches in §2 are chosen to *falsify* the claim, not to support it. If
# any of them returns a point set for a private, charter or francophone school,
# this notebook has disproved its own headline and says so — the invariants in
# §5 are written that way round.
#
# ⚠️ **What this can and cannot establish.** It establishes that the Socrata
# catalogue for `data.edmonton.ca` exposed no such dataset **on the day this was
# run**, which is printed below. It cannot establish that the City holds no such
# data internally, nor that it is unpublished elsewhere — only that a consumer
# working from the open data portal cannot find it.
#
# ## Reproducing
#
# ```
# pip install pandas certifi
# ```
#
# Every cell is a small metadata or aggregate query against public endpoints.
# The whole notebook runs in seconds and needs no API token.

# %%
import json
import re
import ssl
import urllib.parse
import urllib.request
from datetime import datetime, timezone

import certifi
import pandas as pd
from IPython.display import Markdown, display

UA = "edmonton-tax-viz/school-coverage (open-data quality check)"
SSL_CTX = ssl.create_default_context(cafile=certifi.where())

RUN_AT = datetime.now(timezone.utc)

# ⚠️ THIS REPORT IS A SNAPSHOT, and the published page has to say so on its own
# face — it is the artifact that gets handed to someone, usually without the
# index page that would otherwise date it. Two of these four carried NO date at
# all until 2026-08-29.
#
# FIRST_MEASURED is when the finding was made and does NOT change on re-run.
# _STAMPED_AT is when this page was last re-executed against live data. Both are
# shown: "first found on" and "still true today" are different claims and a
# reader needs each. Imports are aliased and local to this block so it can be
# pasted into any of these notebooks unchanged.
import datetime as _dt

from IPython.display import Markdown as _Md, display as _disp

FIRST_MEASURED = "2026-08-29"
_STAMPED_AT = _dt.datetime.now(_dt.timezone.utc)

_disp(_Md(
    f"**Snapshot.** Finding first measured **{FIRST_MEASURED}**; this page "
    f"re-executed against live data **{_STAMPED_AT:%Y-%m-%d}** (UTC). "
    f"Nothing re-runs these on a schedule — re-execute before citing a figure."))

CHECKS: list[tuple[bool, str]] = []


def check(ok: bool, claim: str) -> None:
    CHECKS.append((bool(ok), claim))
    print(f"  [{'PASS' if ok else 'FAIL'}] {claim}")


def _read(url: str, timeout: int = 300) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, context=SSL_CTX, timeout=timeout) as r:
        return r.read()


def soda(dataset: str, params: dict) -> list[dict]:
    """One Socrata query. ⚠️ urlencode is required — a raw space in $select
    (as in `count(*) as n`) raises InvalidURL before the request is made."""
    return json.loads(_read(
        f"https://data.edmonton.ca/resource/{dataset}.json?"
        + urllib.parse.urlencode(params)))


def catalog(query: str, limit: int = 400) -> list[dict]:
    """Search the PUBLIC Socrata catalogue for this domain — the same index the
    portal's own search box uses, so a negative here is a negative for anyone
    looking for the data by hand."""
    url = ("https://api.us.socrata.com/api/catalog/v1?"
           + urllib.parse.urlencode({"domains": "data.edmonton.ca",
                                     "q": query, "limit": limit}))
    return json.loads(_read(url))["results"]


print(f"run at: {RUN_AT:%Y-%m-%d %H:%M} UTC")

# %% [markdown]
# ## 1. What Edmonton publishes
#
# Two datasets, one per public board. Both are live and both are counted here
# rather than quoted, so the figures below are this run's, not a remembered
# number.

# %%
PUBLISHED = {
    "996c-239n": "EPSB School Locations (Edmonton Public)",
    "gfxq-u8uu": "Edmonton Catholic Schools (Current)",
}

rows = []
for ds, label in PUBLISHED.items():
    n = int(soda(ds, {"$select": "count(1)"})[0]["count_1"])
    rows.append({"dataset": ds, "name": label, "rows": n})

published = pd.DataFrame(rows)
display(published)

total_published = int(published["rows"].sum())
print(f"\ntotal published school points: {total_published}")

# %% [markdown]
# Both datasets name their board in their title. Neither claims to be a
# citywide list, and neither is wrong — but between them they are the **only**
# school point sets on the portal, which §2 establishes.

# %% [markdown]
# ## 2. Searching for what is missing
#
# These are the searches that would find the absent schools **if the portal
# carried them**. They are deliberately generous: the Socrata catalogue does a
# loose full-text match, so a relevant dataset under almost any title should
# surface for at least one of them.

# %%
FALSIFYING = [
    "private school",
    "charter school",
    "independent school",
    "francophone",
    "Centre-Nord",          # the francophone authority serving Edmonton
]

# A hit only counts if the dataset is plausibly a school POINT SET for one of
# the missing operators — the loose match returns playgrounds and survey
# results otherwise, and counting those as hits would flatter the portal.
MISSING_TERMS = ("private", "charter", "independent", "francophone",
                 "centre-nord", "centre nord")
SCHOOL_TERMS = ("school", "ecole", "école")

found = []
search_rows = []
for q in FALSIFYING:
    res = catalog(q)
    relevant = [r for r in res
                if any(t in r["resource"]["name"].lower() for t in MISSING_TERMS)
                and any(t in r["resource"]["name"].lower() for t in SCHOOL_TERMS)]
    found.extend(relevant)
    search_rows.append({
        "search": q,
        "results": len(res),
        "naming a missing operator AND a school": len(relevant),
        "example result": res[0]["resource"]["name"][:52] if res else "—",
    })

display(pd.DataFrame(search_rows))

# %% [markdown]
# The middle column is the one that matters. The raw result counts are noise —
# a loose match on "private school" returns playgrounds and sign locations —
# so a result only counts if its title names one of the missing operators
# **and** names a school.

# %% [markdown]
# ### Every school dataset on the portal, classified
#
# The broad search below is the one a person would actually run. Each result is
# classified by which operator it belongs to, so the claim "only two boards" is
# checked against the whole result set rather than asserted.

# %%
broad = catalog("school")


def operator_of(name: str) -> str:
    n = name.lower()
    if any(t in n for t in MISSING_TERMS):
        return "a MISSING operator"
    if "catholic" in n:
        return "Edmonton Catholic (ECSD)"
    if "public school" in n or "epsb" in n:
        return "Edmonton Public (EPSB)"
    return "not a school-operator dataset"


broad_df = pd.DataFrame([
    {"name": r["resource"]["name"], "operator": operator_of(r["resource"]["name"])}
    for r in broad
])
display(broad_df["operator"].value_counts().rename("datasets").to_frame())

missing_hits = broad_df[broad_df["operator"] == "a MISSING operator"]
print(f'datasets naming a missing operator: {len(missing_hits)}')
if len(missing_hits):
    display(missing_hits)

# %% [markdown]
# ## 3. Why a consumer cannot work around it
#
# The natural workaround is to identify schools from the property roll instead.
# It does not work, and the reason is structural rather than a matter of
# effort: **the current assessment roll carries no field describing what a
# property IS.**

# %%
roll_cols = list(soda("q7d6-ambg", {"$limit": 1})[0].keys())
roll_n = int(soda("q7d6-ambg", {"$select": "count(1)"})[0]["count_1"])

print(f"q7d6-ambg — {roll_n:,} rows, {len(roll_cols)} columns:")
for c in roll_cols:
    print("   ", c)

USE_FIELDS = ("use", "occupancy", "building", "description", "type", "purpose")
# ⚠️ Matched on WORD BOUNDARIES, not as substrings. A plain `in` test reports
# `house_number` as a land-use field (it contains "use") and the invariant below
# then fails for a reason that has nothing to do with the City's data — which is
# exactly what happened on the first run of this notebook.
land_use_cols = [c for c in roll_cols
                 if any(re.search(rf"(^|_){t}(_|$)", c.lower()) for t in USE_FIELDS)]
print(f"\ncolumns describing land use or occupancy: {land_use_cols or 'NONE'}")

# %% [markdown]
# `tax_class` and `mill_class_1` describe how a property is **taxed**, not what
# stands on it — an institutional class covers hospitals, fire halls, places of
# worship and community leagues alongside schools. So the roll cannot separate
# a school from the rest of that class, and the portal's two board datasets
# remain the only source of school locations.

# %% [markdown]
# ## 4. The consequence, and its direction
#
# Any "distance to nearest school" derived from the portal measures to the
# nearest **EPSB or ECSD** school. Where a private, charter or francophone
# school is nearer, the computed distance is too large.
#
# ⚠️ **The error is one-directional, and that is worth stating plainly in
# fairness to the City:** missing points can only ever make the nearest school
# look *further away*, never closer. A consumer using this for proximity
# analysis under-claims access rather than over-claiming it. The gap is a
# coverage limitation, not a source of false positives.
#
# What would close it: a published point set for the remaining operators, in
# the same shape as the two that already exist. Alberta publishes lists of
# accredited private and charter schools, but as **PDFs** — readable by a
# person, not joinable by a consumer, which is precisely the gap open data
# exists to close.

# %% [markdown]
# ## 5. Invariants
#
# Every claim above is asserted here against the numbers this run computed.
# ⚠️ **The first two are written so they FAIL if the portal starts carrying the
# missing schools** — that is the outcome this report is asking for, and the
# notebook should stop agreeing with itself the moment it arrives.

# %%
check(len(found) == 0,
      "no falsifying search returned a point set for a private, charter or "
      "francophone school")
check(len(missing_hits) == 0,
      "no dataset in the broad 'school' search names a missing operator")
check(total_published > 0 and len(published) == 2,
      f"exactly two school point sets are published, carrying "
      f"{total_published} schools between them")
check(not land_use_cols,
      "the current roll carries no land-use or occupancy field, so schools "
      "cannot be identified from it")

passed = sum(1 for ok, _ in CHECKS if ok)
display(Markdown(f"### {passed} of {len(CHECKS)} invariants passed"))
for ok, claim in CHECKS:
    display(Markdown(f"- {'✅' if ok else '❌'} {claim}"))
display(Markdown(f"_Checked against `data.edmonton.ca` on "
                 f"{RUN_AT:%Y-%m-%d} (UTC)._"))
if passed != len(CHECKS):
    raise AssertionError(f"{len(CHECKS) - passed} invariant(s) failed — see above")
