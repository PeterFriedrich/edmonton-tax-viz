# Findings — Road figures CONSOLIDATION (the first run of `FABLE_AUDIT_road_figures.md`)

Run 2026-09-08 (S149, **Fable 5.1**, effort `high`). The brief is
`docs/FABLE_AUDIT_road_figures.md`; this is one run's output and the brief
holds no findings. Everything below was **measured in-session** from the
committed data, the raw feeds on this box, and two fresh pulls from
`budget.edmonton.ca` (operating and capital, both 200) — nothing is recalled
from an earlier session. Where a figure comes from outside the repo it says
so and says what class of source it is.

**The hinge fact confirmed (§1 of the brief):** `city_unit_costs.json` still
carries two bases on the same collector+local centreline metres —
`roadway_ops` **$9.32/m/yr** ($5,970 maintenance + $3,350 snow per km) and
`roadway_om_renewal` **$50/m/yr** ($12 O&M + $38 renewal) — 5.4× apart, with
`_two_bases` saying so. The brief is not stale.

**No rate, served column or served value changed in this run.** The brief
forbids proposing a replacement rate and none is proposed. Everything that
moves a reader's number is a **Peter's call** in §5.

---

## 0. The one-paragraph verdict

**L0 SOUND · L1 CONDITIONAL (it is a gap instrument, not a validation) ·
L2a SOUND · L2b UNSOUND for the operating basis (a unit-of-measure error,
direction known, ~1.8–2.2×) · L3 nothing reader-moving.** The round's one
finding that changes a published number is that **both halves of the operating
rate are dollars per LANE-kilometre being applied to CENTRELINE metres**: the
"~11,000 km" behind $5,970 and $3,350 is the City's snow-and-ice inventory,
which the City states in lane-km and which includes ~1,300 km of alleys, while
the City's own centreline feed — the file this project already reads — holds
**5,029 km of City-owned road centreline** (1,358 arterial / 926 collector /
2,740 local) plus 1,311 km of alleys. The brief predicted the denominator was
where the project gets it wrong; it was. The map does not move (a uniform
scalar cancels in `scaleT`) but the legend, the panel percentages and three
sentences of public copy do, by ~2×. Separately, the citywide near-match the
brief flagged ($182.7M vs $180.4M) is confirmed to be **two scope errors of
opposite sign** and is not evidence of anything; and the brief's "1.7×
disagreement between two City publications" was **our** error — the two
publications agree to 3% once the same population is compared.

---

## L0 — Is publishing a road cost still the right call? **SOUND**

**Tested:** whether the sharpest argument — *publish `road_m_per_acre` and put
the dollars in prose* — beats what ships. It does not, for two measured
reasons. (1) The two bases tell **different stories** that the physical metres
cannot: on the served file the operating basis puts roads at a **1.68% median
share of a hood's levy (2 hoods over 100%)** and the lifecycle basis at
**9.01% (9 hoods over 100%)**; a reader who only sees metres has no way to
know which of those the City is paying for. (2) The choropleth is invariant to
every error this run found — `scaleT` divides by the 97.5th percentile, so a
uniform scalar (the unit error, the vintage, the blend) leaves the map
pixel-identical. What a wrong rate corrupts is the **legend and the copy**, and
those are guarded (`check_cost_copy.py`) and cheap to change.

**Sharpest argument against, still standing:** the operating basis is
published under the label "per kilometre" while being per lane-kilometre (L2b),
so today the disclosure on screen is not merely a floor, it is a floor with an
unstated unit. L0 stays SOUND **because** L2b's fix is a unit decision and a
copy edit, not a retraction.

**What would change it:** a demonstration that readers act on the absolute
dollars rather than the ranking — nothing in the repo measures that.

---

## L1 — Does either basis reconcile against City money citywide? **CONDITIONAL**

**The level is the wrong instrument for corroboration and the right one for a
gap statement.** Every model figure here is an annual **requirement** (what it
costs to keep a metre of road over its life); every City figure is annual
**funding**. Agreement would not validate the rate and disagreement would not
refute it — the difference between them is the funding gap, which is exactly
what `roadway_renewal.citywide_scale` says the project could not compute. It
can now, and the numbers are below. CONDITIONAL on being read that way.

### Q1 — the $182.7M vs $180.4M near-match is a coincidence, decomposed

Reproduced from the served file joined to full-resolution `load_boundaries()`
acres (406/406, **3,654.1 km**, 193,237 acres): lifecycle $50/m → **$182.7M/yr**
(the served `cost_roads_life_per_acre × area_acres` sums to the same $182.7M);
renewal half $38/m → **$138.9M/yr**; operating $9.32/m → $34.1M/yr.

The City's Neighbourhood Renewal line, from the fresh operating-portal pull:
**$174,386,000 in each of FY2023–FY2026**, booked as `Neighbourhood Renewal`
$158,106,000 + `Alley Renewal` $22,280,000 − `Less: Microsurfacing – City
Operations` $6,000,000. So the brief's **$180.386M gross / $174.386M to
capital / $6.0M microsurfacing** all reproduce from a primary source. (The line
ramped $134.4M → $166.6M over FY2017–22 and has been **flat** since 2023.)

| model figure | what is in it that NRP is not | NRP figure | what is in it that the model is not |
|---|---|---|---|
| $182.7M (both halves) | **$43.8M of O&M** — operating money, funded from `Parks & Roads Services`, never from the renewal levy | $174.4M capital | alleys ($22.3M explicit); sidewalks/curbs, lighting, landscaping, active transportation, traffic safety (**53%** of a typical project per the City's own CEA-2026 slide, Roads **47%**); arterial and collector renewals filed under the `Roads` service and drawn from the same reserve |

Like-for-like is the model's **roads-only renewal requirement $138.9M** against
NRP's **roads-only** spend, which is bracketed **$82.0M (47% of $174.4M, if
every dollar were a typical reconstruction) to $174.4M (if it were all
roads)**. The requirement sits inside the bracket: **order-of-magnitude
plausible, and that is all this level can say.** The two "errors" in the naive
comparison are +$43.8M on the model side and roughly +$90M on the City side —
they do not cancel, they merely land near each other.

⚠️ **One number NOT to quote as agreement:** the City reconstructed *"about 73
km of residential roads and alleys"* in 2024 (secondary press quoting the City),
and 3,654 km ÷ 50 yr = 73.1 km/yr. The populations differ (alleys inside the
73, arterial/collector renewals outside it, overlays and microsurfacing on
other kilometres), so this is arithmetic coincidence of the kind the brief
warns about, recorded here so nobody rediscovers it as evidence.

### Q2 — the "1.7× disagreement between two City publications" was ours

`capital_budget.csv` service `Neighbourhoods` = $716.5M over FY2023–2029 ÷ 7 =
$102M/yr — **wrong population and wrong window**. The programme is not a
*service*, it is a *fund*: the committed file's `fund == "Neighborhood Renewal
Reserve"` draws are

| | FY2023 | FY2024 | FY2025 | FY2026 | **2023–26** | 2027–29 tail |
|---|---|---|---|---|---|---|
| NR Reserve, all services | $183.0M | $188.6M | $250.0M | $98.3M | **$720.0M = $180.0M/yr** | $186.8M |

against the levy's **$174.386M/yr → $697.5M over the same four years**:
**within 3%.** The reserve funds $668.2M under `Neighbourhoods` and **$238.4M
under `Roads`** (Pleasantview and Killarney reconstructions, 132 Avenue, 86
Street, 95 Avenue, 97 Street, the Minor Renewal Program — NRP work filed under
another service); the `Neighbourhoods` service in turn draws $37.8M from Local
Improvements and $5.8M from the Cemetery Reserve. Dividing by seven counted the
carry-forward tail (`DATA.md` §19: 2027+ rows are carry-forwards) as three full
years. **Not independent** — the operating side is the reserve's inflow and the
capital side its outflow, both from the same portal — so the 3% agreement is an
accounting identity, not a validation. It does establish that both figures are
the same programme, correctly read.

### Q3 — should the NRP line be a committed reviewed input?

**The funded side is already committed** — it is the `fund` column of
`data/capital_budget.csv`, which the project has held since 2026-08-22 while
`roadway_renewal.citywide_scale` and the inventory §1.5 said *"this project has
no data on the funded side."* That sentence is false and should be corrected
(§5). The **operating** line ($180.386M / $174.386M) is not committed and need
not be: it is derivable from the operating portal in one `groupby` (§6), it
enters no copy, and `check_cost_copy.py` guards copy↔JSON only, so a committed
copy would be a drift surface with no guard. Record it in `DATA.md` §17 with
the reproduction; do not put it in `city_unit_costs.json`.

---

## L2a — NUMERATOR: is every shipped rate still traceable to a live source? **SOUND**

Re-pulled and matched to the dollar: `Roadway Maintenance` FY2017
**$65,671,000** (the only year the program exists — 2018–25 is
`Infrastructure Maintenance` $49.7–56.9M, 2026 is `Mobility Infrastructure
Services` $76.9M); `Snow and Ice Control` FY2025 **$67,553,815** (FY2026
$71,247,971); `Parks & Roads Services` FY2017→25 **1.3357×**, →26 **1.2551×**.
The Taproot article is live and its snow totals still read $67M / $36.85M /
$30.15M. The Development Impact page returned **502 to the fetch tool today**
and `www.edmonton.ca` is unreachable from this box; its figures were last
confirmed live by the outside research (page `last-modified 2024-07-26`), so
the lifecycle numerator is traceable but **not re-verified in this run**.

The vintage call (ship FY2017 unescalated, quote the 1.29× FY2017-vs-FY2017
figure) is the right one *for the reason given* — branch growth is a proxy.
⚠️ **But the 1.29× "reconciliation" itself does not survive L2b**: it compared
$/lane-km to $/centreline-km. Per centreline km the operating rate is ~$16.8–
$20.4/m against the $12 lifecycle O&M half — the disagreement is real and runs
the **other way** (1.4–1.7×). The 2026-09-06 re-scope decision does not rest on
that clause (it rested on the §16-vs-§13 split and the set-aside test) and
stands; the clause is demoted the way the 3% cross-check was on 2026-09-03.

---

## L2b — DENOMINATOR **— UNSOUND for the operating basis**

### 1. The lane-km conflict resolves, and it resolves against the shipped rate

Every source that states a unit says the City's inventory is **lane-km**:
the City's own Winter Roads FAQ (*"more than 12,000 km of roadways … over 4,000
lane kms of residential roads"* — search-surfaced text; the page 403s the fetch
tool), the 2020 Infrastructure State & Condition figures relayed as
**arterial 3,500 / collector 1,763 / local 4,830 lane-km = 10,093** (secondary,
blog now 404), and Taproot's 2022 brief that the inventory grew *"21% … in
roadway lane kilometres"* mostly because *"alleyways added 1,250 to 1,300
kilometres"* when the 2021 policy started counting them. Taproot 2025 attaches
*"linear kilometres"* to its 11,000 — the only source to say linear, and the one
this project derived both halves from.

Measured from `data/raw/roads.geojson` in EPSG:3400 (53,854 segments, the same
feed `load_roads` reads):

| population | centreline km |
|---|---|
| everything in the feed (roads + alleys + railways, all owners) | 7,700 |
| `centerline_type == Road`, all owners | 5,685 (Province 495 — the ring road) |
| **City of Edmonton roads** | **5,029** — arterial 1,358 · collector 926 · local 2,740 · alley-classed 6 |
| City alleys (`centerline_type == Alley`) | **1,311** |

There is no reading of the City's centreline data under which 11,000 is linear
km: City roads plus alleys are **6,340 km**. Three independent checks agree on
the conversion: the City's alley addition (1,250–1,300 lane-km) equals the feed's
**1,311 alley centreline km** (alleys are one lane, so lane-km = centreline km);
the 2020 class figures give **2.58 / 1.90 / 1.76 lanes per centreline km**
(arterial / collector / local — divided arterials are drawn per carriageway,
locals are two lanes less one-ways); and Calgary, in the comparator report,
states **6,652 linear km / 18,239 lane-km** for a city of similar footprint.

**What it does to the shipped rate**, per centreline km of the roads the metric
counts (collector+local, alleys and arterials excluded):

| conversion | maintenance | snow | operating | vs shipped |
|---|---|---|---|---|
| shipped: $65.671M ÷ 11,000 · $36.85M ÷ 11,000 | $5,970 | $3,350 | **$9.32/m** | — |
| class lane-km ÷ centreline km, collector+local: 6,593 ÷ 3,666 = **1.80** | $10,750 | $6,030 | **$16.8/m** | **1.80×** |
| City road centreline, alleys carrying a pro-rata share: ÷ 5,029 × (10,100 ÷ 11,400) | $11,570 | $6,490 | $18.1/m | 1.94× |
| City road centreline, alleys carrying nothing: ÷ 5,029 | $13,060 | $7,330 | **$20.4/m** | **2.19×** |

**Direction: the shipped operating rate UNDERSTATES by 1.8–2.2×.** Both halves
share the denominator, so both move together. Units named on every row per the
brief's rule; the 1.80 row is the class-specific one and the conservative one.

#### ⚠️ The endpoints of that range do NOT have equal standing (added 2026-09-09, S150)

A correction factor here is a **lane-multiplicity**: lane-km ÷ centreline km
**on one population**. Only the 1.80 row is that, on the population the metric
actually charges. Stating this because a fourth ratio, **1.73**, entered
circulation externally as *"inside the range"* — it is **below** it, and the
reason is structural, not arithmetic:

| ratio | construction | what it is |
|---|---|---|
| **1.73** | 11,000 ÷ 6,335 (roads **+ alleys**, both sides) | matched, but the **whole inventory** — **alleys are one lane**, so it is diluted downward. A **LOWER** bound, never interior. |
| **1.80** | 6,593 ÷ 3,666 (collector+local, both sides) | matched **and** the right population. **The best estimate.** |
| 2.01 | 10,093 ÷ 5,024 (all roads, both sides) | matched, but includes arterials, which are wider (2.58). |
| **2.19** | 11,000 ÷ 5,024 (numerator **incl.** alleys, denominator **excl.**) | **not a lane-multiplicity at all** — mismatched populations. An **UPPER** bound by construction, which is the same thing as *"charges alleys nothing"*. |

So **$16.8/m is a best estimate and $20.4/m is a bound**, and the range should
not be quoted as though its two ends were alternative measurements.

⚠️ **A cross-check that falls out of this, and it strengthens the unit finding
independently of the alley argument.** The 2020 class figures are roads-only and
total **10,093 lane-km**; add the feed's **1,311 km of alleys** (one lane, so
lane-km = centreline km) and the inventory is **11,404 lane-km** — within
**3.7%** of the City's *"~11,000"*. On a centreline reading the same total is
6,335 km, which is **42% low**. Two independent sources agree the City's figure
is lane-km. Separately, all roads come to **2.01 lanes per centreline km** —
i.e. essentially two — which is what a road network should read and is a
sanity check that the relayed 2020 split is internally sensible.

### 2. The 3,654 vs 3,644 km — resolved, vintage, and it falsifies a recorded claim

`tools/ward_rollup.py` derives metres exactly as S136 did (served
`road_m_per_acre` × `load_boundaries()` acres), so the method is identical. The
served file at `024ecc6` (2026-08-04, the vintage the 2026-08-07 figure was
read from) gives **3,643.9 km**; today's gives **3,654.1 km**. **28 hoods
changed, +10.22 km net**, almost all greenfield (Crossroads +2.6 km, Edgemont
+2.0, Meltwater +1.3, Marquis +0.7, Aster +0.7) — the weekly roads refresh
adding built network. So `roadway_renewal.citywide_scale`'s dated "~3,644 km
(2026-08-07)" was right on its date, and **`DECISIONS.md` 2026-08-07's
reasoning that "the renewal side is provably refresh-invariant, so a rerun would
reproduce $138.5M exactly" is wrong in kind** — it was measured across one
refresh in which the roads feed did not change. Over a month the renewal
requirement moved +$0.39M/yr (0.28%). The decision it supported (ward_rollup
reads the committed served file) still holds — the drift is small and
monotone — but for a different reason than recorded.

### 3. The snow arterial blend — sized, with the assumption stated

Arterials are **35%** of road lane-km (3,500 of 10,093). If an arterial lane-km
costs *k* times a collector/local lane-km to clear, the blended rate overstates
the collector+local term by **1 ÷ (0.65 + 0.35k)**: *k*=1 → 1.00, *k*=2 → 0.74,
*k*=3 → 0.59, *k*=5 → 0.42. Nothing published gives *k*; the City's Procedure
C409K puts arterials at bare pavement fastest and residential at a 5 cm
snowpack in 10–14 days, so *k* > 1 with certainty. **Combined with §1, the net
factor on the shipped operating rate is 1.80 × (0.65 + 0.35k)⁻¹ — still ≥ 1.06×
at k=3, and it takes k > 3.3 to flip the sign.** So `roadway_ops.floor`'s
"a judgement about which error is larger, not an arithmetic bound" can now be
an arithmetic bound under a stated *k*. The same shape applies to the
maintenance half (arterials are more heavily maintained), with no *k* published
for it either.

---

## L3 — the leftovers (nothing here moves a shipped number)

- **$11,510.8M vs ~$11.56B.** The live API today totals **$11,510,831,000 —
  byte-identical to the committed 2026-08-21 file**, two months after the June
  2026 adjustment the $11.56B is attributed to. Either the portal has not
  absorbed it or the press figure is a different scope; the council report was
  not retrieved. Unresolved, not reader-moving, and `check_capital_budget` will
  flag the day the API moves.
- **$965.2M** never entered this repo (one TODO mention). Same disposition as
  the $500K/$2.5M/$17.5M figures: a refutation of a number we do not hold is
  not a finding here.
- **The four service-life figures** the research inventory §9 could not
  identify are named in `TODO.md`: **60-yr** (City staffer via JOC 2016),
  **Alberta Transportation 20-yr** design life (provincial highways), **Calgary
  "up to 20 years"** (full reconstruction), **Winnipeg 25-yr** (asphalt
  *regional* streets). The inventory's three plus Winnipeg. All still unverified
  and deferred (Peter, 2026-09-03); none is the same asset class as a
  neighbourhood road, which is why verifying them would not settle 25-vs-50.

---

## 4. Already-closed items the round did not re-open

The $5,970 substitution (shipped 2026-09-06), the demoted 3% cross-check, the
retired composite and the never-held per-neighbourhood figures were treated as
closed per the brief's §4. The Calgary report was read for its Q7 table and its
two Edmonton figures only: JOC's *"$158.8-million annual budget"* on *"13,000
kilometres"* is the **Neighbourhood Renewal levy** (CBC calls it *"a $159
million a year program"* the same season) over the City's **lane-km**
inventory — i.e. **$12.2k per lane-km of capital renewal**, and Calgary's
*"$12,500–$17,000"* is the same family. Neither is an operating figure, and
neither contradicts anything here; they are consistent with the L2b unit
finding (13,000 is a lane-km number).

---

## 5. What is proposed (all Peter's calls; ranked by whether a reader's number moves)

1. ✅ **DECIDED 2026-09-08 — STATE IT, DO NOT CONVERT.** Peter: *"let's choose the floor for now. We may link directly to an external analysis I'll do later."* The value stays $9.32/m/yr, the three copy sites say **per lane-kilometre**, and `roadway_ops.floor` becomes arithmetic under a stated k (net ≥ 1.06× for k ≤ 3). Both conversions below were declined: ×1.80 rests on a secondary relay now 404, ×2.19 charges alleys nothing, and the brief's own rule is that no replacement rate comes from an audit's arithmetic. `DECISIONS.md` 2026-09-08. **The finding as put:** the operating rate's unit. `roadway_ops` is $/lane-km applied to
   centreline metres. Options are a per-class lanes-per-centreline conversion
   (1.80 on the 2020 lane-km figures — secondary, internally consistent), a
   City-centreline conversion (5,029 km, primary, alleys unallocated), or
   keeping the value and stating the unit in `floor`, `denominator_mismatch`
   and the three public copy sites. On the served file the first two move the
   legend median **$304 → $547–665/acre/yr**, the panel's median roads-ops
   share of levy **1.68% → 3.0–3.7%**, hoods over 100% **2 → 3–4**, and the
   copy's *"about five times higher"* → **~2.5–3×** — `check_cost_copy.py`
   will name every stale sentence. The map does not change. **Not proposed as
   a rate**; proposed as a unit decision.
2. **Demote the "1.29× — the two sources do not disagree about roads" clause**
   in `DECISIONS.md` 2026-09-06, `DATA.md` §13 and
   `roadway_ops.rescoped_2026_09_06` (3). The decision stands; the support
   clause was computed across units.
3. **Correct `roadway_renewal.citywide_scale`** ("no data on the funded side")
   — the funded side is `capital_budget.csv`'s `fund` column, $180.0M/yr over
   2023–26, and the requirement it can now be set against is $138.9M/yr — with
   the caveat that both sides are partial networks in different directions.
4. **Amend `DECISIONS.md` 2026-08-07** — refresh-invariance falsified; the
   decision keeps, the reason changes.
5. **`DATA_ISSUES.md`** — the operating portal books FY2025's entire
   $174,386,000 to program `Alley Renewal` while FY2023/24/26 split it three
   ways; a labelling defect at the publisher. Not reportable until it has an
   artifact; recorded as a candidate.

Items 2–5 are executed in the same PR as this file (docs only, no served
change); item 1 is not.

---

## 6. Reproduction

⚠️ Redirect long outputs to a file. `www.edmonton.ca` is unreachable from this
box; `budget.edmonton.ca` needs `certifi`.

```python
# --- the network by class (EPSG:3400 before any length) ---------------------
import sys; sys.path.insert(0, '.'); sys.path.insert(0, 'src')
import geopandas as gpd, pandas as pd
from src.load_roads import CLASS_GROUP
r = gpd.read_file('data/raw/roads.geojson').to_crs(3400); r['km'] = r.length / 1000
print(r.groupby('centerline_type').km.sum())                      # Road 5,685 · Alley 1,311 · Railway 704
city = r[(r.centerline_type == 'Road') & (r.responsible_party_description == 'City of Edmonton')].copy()
city['group'] = city.functional_class_code.map(CLASS_GROUP)
print(city.groupby('group').km.sum())                             # arterial 1,358 · collector 926 · local 2,740

# --- 3,654 km today, 3,644 km on the 2026-08-04 served file -------------------
from src.load_boundaries import load_boundaries
b = load_boundaries('data/raw/neighbourhoods.geojson')[['neighbourhood_name', 'area_acres']]
def km(path):
    g = gpd.read_file(path); g['NAME'] = g.neighbourhood_name.str.upper()
    m = g.merge(b, left_on='NAME', right_on='neighbourhood_name'); assert len(m) == 406
    return (m.road_m_per_acre * m.area_acres).sum() / 1000
print(km('web/data/neighbourhood_value_per_acre.geojson'))        # 3654.1
# git show 024ecc6:web/data/neighbourhood_value_per_acre.geojson > /tmp/served_0807.geojson
print(km('/tmp/served_0807.geojson'))                              # 3643.9

# --- the two City publications, same population -----------------------------
c = pd.read_csv('data/capital_budget.csv')
nrr = c[c.fund == 'Neighborhood Renewal Reserve']
print(nrr.groupby('fiscal_year').approved.sum())                   # 2023-26 sum 719,953,000
print(nrr.groupby('service').approved.sum())                       # Neighbourhoods 668.2M · Roads 238.4M

import urllib.request, ssl, certifi
ctx = ssl.create_default_context(cafile=certifi.where())
with urllib.request.urlopen('https://budget.edmonton.ca/api/operating_budget.csv', context=ctx, timeout=120) as f:
    open('/tmp/opbudget.csv', 'wb').write(f.read())                # 1,037,656 bytes
d = pd.read_csv('/tmp/opbudget.csv')
nr = d[d.branch == 'Neighbourhood Renewal']
print(nr.groupby(['budget_year', 'program']).budget.sum())         # 2023/24/26: 158,106,000 + 22,280,000 − 6,000,000; 2025: one row 'Alley Renewal' 174,386,000

# --- what a unit correction moves on the served file (nothing changed) ------
import numpy as np
g = gpd.read_file('web/data/neighbourhood_value_per_acre.geojson')
m = g[(g.revenue_per_acre > 0) & g.cost_roads_ops_per_acre.notna()]
for k in (1, 1.80, 2.19):
    s = m.cost_roads_ops_per_acre * k / m.revenue_per_acre * 100
    print(k, round(np.median(s), 2), int((s > 100).sum()))          # 1.68%/2 · 3.02%/3 · 3.68%/4
```

## 7. This run's own errors and limits

- The first pass over `capital_budget.csv` grouped on a regex that also matched
  `Community Revitalization Levy` rows, producing a fund table with Recreation
  & Culture and Economic Development under "renewal"; caught on the exact
  `fund ==` filter before anything was written. **Match on the value, not a
  substring.**
- Three City pages (Winter Roads FAQ, the Snow & Ice annual report, the
  Development Impact page) and the CEA slide deck could not be fetched (403/502).
  The FAQ wording is search-surfaced, not fetched; the 2020 class lane-km are a
  secondary relay the run could not re-open. The unit finding does not depend on
  either — the feed's 5,029 km and the alley cross-check carry it — but the
  **1.80 factor does**, which is why 2.19 (primary, feed-only) is also given.
- No *k* exists for the arterial blend; §L2b.3 is a bound under a stated
  assumption, not a measurement.
