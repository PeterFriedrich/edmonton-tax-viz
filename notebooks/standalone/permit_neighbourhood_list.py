# ---
# jupyter:
#   title: Edmonton's building permits put several neighbourhoods in a one-neighbourhood field
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
# # Edmonton's building permits put several neighbourhoods in a one-neighbourhood field
#
# **Dataset:** *General Building Permits* (`24uj-dj8v`) on `data.edmonton.ca`.
#
# **In one sentence:** on a small number of rows, `neighbourhood` holds a
# **comma-joined list** of names — `OLIVER, WÎHKWÊNTÔWIN`,
# `RITCHIE, RITCHIE`, `HOLLICK-KENYON, BRINTNELL, MILLER, BRINTNELL` — and the
# companion id field `neighbourhood_numberr` is comma-joined in exactly the same
# way, so a consumer joining either field to the neighbourhood boundary file
# loses those rows with no signal that anything was dropped.
#
# The row count is small. The consequence is not evenly spread: because the
# affected rows cluster in a few neighbourhoods and skew to older years, a
# per-neighbourhood total can be wrong by a large fraction for a *specific*
# neighbourhood while the citywide total barely moves.
#
# ## Three different things are mixed into one field
#
# The list-valued rows do not all mean the same thing, and this is the part that
# matters most for anyone deciding how to fix it:
#
# 1. **A rename carrying both the old and new name** — `OLIVER, WÎHKWÊNTÔWIN`,
#    the 2024 municipal rename. One neighbourhood, two labels.
# 2. **The same neighbourhood written twice** — `RITCHIE, RITCHIE`. Pure
#    duplication, carrying no information at all.
# 3. **A permit genuinely spanning two or more neighbourhoods** —
#    `CANOSSA, NORWESTER INDUSTRIAL`. This is real information, in a field with
#    no room to express it.
#
# Only the third case actually needs a list. The first two are artifacts.
#
# ## The useful finding: the id column already separates the three
#
# `neighbourhood_numberr` looks at first like the same defect twice over — it is
# comma-joined on precisely the same rows. But it is **strictly more informative
# than the name**, because the numeric ids can be checked against the published
# boundary file (`65fr-66s6`), and retired ids are absent from it. That gives a
# mechanical rule where name-matching could only guess:
#
# | pattern in `neighbourhood_numberr` | what it means |
# |---|---|
# | the same id repeated (`5642, 5642`) | duplication |
# | one retired id + one live id (`1150, 1151`) | a rename |
# | two or more **live** ids (`3080, 4350`) | a genuine multi-neighbourhood permit |
#
# §3 applies that rule to every affected row. It classifies **all** of them —
# no row is left ambiguous — which a name-based reading cannot do.
#
# ⚠️ **What this means for the fix:** "publish a numeric id" is not the ask,
# because the id is already published. The ask is that the existing id be
# **single-valued**, with the genuine multi-neighbourhood case given somewhere
# to go.
#
# ## Reproducing
#
# ```
# pip install pandas certifi
# ```
#
# Every cell is a metadata or aggregate query against public endpoints. No API
# token is needed.

# %%
import json
import ssl
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone

import certifi
import pandas as pd
from IPython.display import Markdown, display

UA = "edmonton-tax-viz/permit-neighbourhood-list (open-data quality check)"
SSL_CTX = ssl.create_default_context(cafile=certifi.where())

RUN_AT = datetime.now(timezone.utc)

# ⚠️ THIS REPORT IS A SNAPSHOT, and the published page has to say so on its own
# face — it is the artifact that gets handed to someone, usually without the
# index page that would otherwise date it.
#
# FIRST_MEASURED is when the finding was made and does NOT change on re-run.
# ⚠️ It is 2026-09-14, the date the list-valued field was first measured, NOT
# the date this notebook was written (2026-09-17). The notebook publishes an
# existing finding; the id-based classification in §3 is new on the later date
# and is dated in place there. _STAMPED_AT is when this page was last
# re-executed against live data.
import datetime as _dt

from IPython.display import Markdown as _Md, display as _disp

FIRST_MEASURED = "2026-09-14"
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


PERMITS = "24uj-dj8v"
BOUNDARIES = "65fr-66s6"

print(f"run at: {RUN_AT:%Y-%m-%d %H:%M} UTC")

# %% [markdown]
# ## 1. The field, and how often it holds a list
#
# Counted live rather than quoted, so the figures below are this run's.

# %%
total_rows = int(soda(PERMITS, {"$select": "count(1)"})[0]["count_1"])
list_rows = int(soda(PERMITS, {"$select": "count(1)",
                               "$where": "neighbourhood like '%,%'"})[0]["count_1"])

display(Markdown(
    f"- rows in *General Building Permits*: **{total_rows:,}**\n"
    f"- rows whose `neighbourhood` contains a comma: **{list_rows:,}** "
    f"(**{list_rows / total_rows * 100:.2f}%**)"))

# %% [markdown]
# A fraction of a percent — which is exactly why it survives unnoticed. The
# next cell shows what the affected rows look like.

# %%
sample = soda(PERMITS, {
    "$select": "neighbourhood,neighbourhood_numberr,year,units_added",
    "$where": "neighbourhood like '%,%'", "$limit": 8, "$order": "year"})
display(pd.DataFrame(sample))

# %% [markdown]
# ⚠️ **Note the second column.** `neighbourhood_numberr` — the numeric
# companion — is comma-joined on the same rows, in the same order. A consumer
# who switches to the id field to avoid the name problem inherits it unchanged.
#
# ⚠️ Incidentally, that field name carries a **typo**: `numberr`, with a
# doubled final `r`. Harmless, but it is the kind of thing that is cheap to fix
# while the field is being looked at, and impossible for a consumer to work
# around without hard-coding the misspelling.

# %% [markdown]
# ## 2. Every other neighbourhood-bearing dataset is single-valued
#
# This is what makes the permits dataset an outlier rather than a convention:
# the same City publishes a clean single neighbourhood key elsewhere.

# %%
others = []
for ds, label, col in [
    ("q7d6-ambg", "Property Assessment (Current Calendar Year)", "neighbourhood"),
    (BOUNDARIES, "Neighbourhood Boundaries", "name"),
]:
    n = int(soda(ds, {"$select": "count(1)",
                      "$where": f"{col} like '%,%'"})[0]["count_1"])
    others.append({"dataset": ds, "name": label,
                   "rows with a comma in the neighbourhood field": n})
display(pd.DataFrame(others))

# %% [markdown]
# ## 3. Classifying every affected row by what its ids mean
#
# The rule from the header, applied to all of them. A neighbourhood id is
# **live** if it appears in the published boundary file, and **retired**
# otherwise.

# %%
live_ids = {r["neighbourhood_number"] for r in
            soda(BOUNDARIES, {"$select": "neighbourhood_number", "$limit": 500})}
print(f"live neighbourhood ids in {BOUNDARIES}: {len(live_ids)}")

rows, offset = [], 0
while True:
    batch = soda(PERMITS, {
        "$select": "neighbourhood,neighbourhood_numberr,year,units_added",
        "$where": "neighbourhood like '%,%'", "$limit": 1000, "$offset": offset})
    rows += batch
    offset += 1000
    if len(batch) < 1000:
        break
print(f"affected rows fetched: {len(rows)}")


def classify(raw_ids: str) -> str:
    ids = [x.strip() for x in raw_ids.split(",")]
    if len(set(ids)) == 1:
        return "duplication (same id repeated)"
    live = [i for i in set(ids) if i in live_ids]
    if len(live) == 1:
        return "rename (one retired id + one live)"
    if not live:
        return "all ids retired"
    return "genuine straddle (2+ live ids)"


missing_ids = sum(1 for r in rows if not r.get("neighbourhood_numberr"))
counts, units, names = Counter(), Counter(), defaultdict(set)
for r in rows:
    if not r.get("neighbourhood_numberr"):
        continue
    k = classify(r["neighbourhood_numberr"])
    counts[k] += 1
    units[k] += float(r.get("units_added") or 0)
    names[k].add(r["neighbourhood"])

summary = pd.DataFrame([
    {"what the row actually is": k, "rows": counts[k],
     "units_added": int(units[k]), "distinct name strings": len(names[k])}
    for k, _ in counts.most_common()])
display(summary)
print(f"\nrows carrying no id at all: {missing_ids}")

# %% [markdown]
# **Every affected row classifies, and none is left ambiguous.** That is the
# argument for the id field: the name alone cannot tell `RITCHIE, RITCHIE`
# (duplication) from `CANOSSA, NORWESTER INDUSTRIAL` (a real straddle) without
# a human knowing which pairs are renames.

# %%
for k in counts:
    display(Markdown(f"**{k}** — e.g. "
                     + ", ".join(f"`{n}`" for n in sorted(names[k])[:3])))

# %% [markdown]
# ## 4. Why a small row count is not a small problem
#
# The affected rows are not spread evenly. They concentrate by neighbourhood,
# so a citywide total absorbs the loss while a specific neighbourhood's total
# does not.

# %%
per_name = Counter()
per_units = Counter()
for r in rows:
    per_units[r["neighbourhood"]] += float(r.get("units_added") or 0)
    per_name[r["neighbourhood"]] += 1
top = pd.DataFrame(
    [{"neighbourhood field value": n, "rows": per_name[n],
      "units_added": int(per_units[n])}
     for n, _ in per_units.most_common(8)])
display(top)

display(Markdown(
    f"Total `units_added` sitting on list-valued rows: "
    f"**{int(sum(per_units.values())):,}**. A consumer joining on either the "
    f"name or the id drops all of it."))

# %% [markdown]
# ⚠️ **In fairness to the City:** the dataset is otherwise well-formed, the
# affected share is small, and the id field — once single-valued — would make
# this dataset *easier* to join than most, not harder. Two of the three causes
# are artifacts that carry no information, so fixing them loses nothing.
#
# ## What would close it
#
# 1. **Make `neighbourhood_numberr` single-valued**, and the name field with
#    it. For the duplication and rename cases this is unambiguous — the
#    classification in §3 is mechanical and needs no judgement.
# 2. **Give the genuine multi-neighbourhood permit somewhere to go**: either one
#    row per neighbourhood, or a separate `additional_neighbourhoods` field.
#    That is the only case that needs a schema decision.
# 3. Optionally, **fix the `numberr` typo** while the field is in hand.

# %% [markdown]
# ## 5. Invariants
#
# Every claim above is asserted here against the numbers this run computed.
# ⚠️ **The first three are written so they FAIL once the City makes the field
# single-valued** — the outcome this report is asking for. A report that keeps
# agreeing with itself after being acted on is one nobody notices has worked.
# Do not "fix" them into passing; mark the report RESOLVED instead.

# %%
check(list_rows > 0,
      f"`neighbourhood` still holds comma-joined lists on {list_rows} rows")
check(all(r.get("neighbourhood_numberr") and "," in r["neighbourhood_numberr"]
          for r in rows),
      "`neighbourhood_numberr` is comma-joined on every one of those rows too, "
      "so the id field is not a workaround")
check(counts["duplication (same id repeated)"] > 0
      and counts["rename (one retired id + one live)"] > 0
      and counts["genuine straddle (2+ live ids)"] > 0,
      "all three causes are present, so this cannot be fixed by one rule alone")
check(missing_ids == 0,
      "every affected row carries an id, so the id-based classification covers "
      "the whole defect rather than a subset")
check(all(r["rows with a comma in the neighbourhood field"] == 0
          for r in others),
      "no other neighbourhood-bearing dataset checked here holds a list, so "
      "this is an outlier rather than a City-wide convention")

passed = sum(1 for ok, _ in CHECKS if ok)
display(Markdown(f"### {passed} of {len(CHECKS)} invariants passed"))
for ok, claim in CHECKS:
    display(Markdown(f"- {'✅' if ok else '❌'} {claim}"))
display(Markdown(f"_Checked against `data.edmonton.ca` on "
                 f"{RUN_AT:%Y-%m-%d} (UTC)._"))
if passed != len(CHECKS):
    raise AssertionError(f"{len(CHECKS) - passed} invariant(s) failed — see above")
