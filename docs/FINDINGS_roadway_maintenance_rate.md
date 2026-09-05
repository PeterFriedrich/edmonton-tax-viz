# Findings — the $1,285/km maintenance rate against the City's published roads-maintenance program

Captured 2026-09-05 (S139), while compiling a full inventory of the project's
road-cost numbers. **Both sources were fetched fresh from the Oracle box** —
`budget.edmonton.ca` and the Taproot article both return 200 (see §5).

**The question:** `SPEC_services.md` and `DATA.md` §13 have carried an OPEN item
since 2026-09-02 — the lifecycle O&M half (**$12/m/yr**) and the operating
maintenance rate (**$4.635/m/yr**) both claim to be annual non-capital spend on
neighbourhood roads and sit **2.6× apart**, with neither traced to what it
actually covers. This traces one of them.

**The answer: the gap is mostly an artifact of the maintenance half being far
narrower than the City's own roads-maintenance program.** The two sources do not
disagree about roads.

⚠️ **NOTHING WAS CHANGED.** No rate, no served column, no value. `roadway_ops`
still ships at $4.635/m/yr. The remedy is a judgement call (§4) and it is
Peter's.

## 1. The source says $1,285 is the same kind of number as the rejected $178

Fetched from the Taproot article (`roadway_ops.source.url`), the sentence in
full:

> *"It costs about **$178 per kilometre to replace, repair, and maintain**
> active pathways, and **$1,285 per kilometre to do the same for roads**."*

⚠️ **The two rates come from ONE sentence and carry ONE phrase.** That phrase —
*"replace, repair, and maintain"* — is exactly what a relayed brief used to
argue $178/km was an all-in bikeway lifecycle rate, and what this project
**rejected on arithmetic** on 2026-08-03
(`city_unit_costs.json` → `bikeway_ops.rejected_lifecycle_reading`).

**The repo reads $1,285 as operating-maintenance, and that reading is correct.**
But the rejection's own test applies to both numbers. Against the City's
3.33%/yr implied set-aside on $1,500,000/km of road capital:

| rate | as %/yr of its own asset value | vs the 3.33%/yr rule |
|---|---|---|
| $178/km bikeway (rejected) | 0.039% | **85× low** |
| **$1,285/km road (shipped)** | **0.086%** | **39× low** |

Neither can be a replace-and-repair rate. **For bikeways that finding blocked a
lens; for roads the same finding has never been drawn.**

## 2. The published program is 4.65× the rate

From `budget.edmonton.ca/api/operating_budget.csv` (§17 — the same publication
as Socrata `da9s-v9j8`, never cite them as corroborating each other):

**FY2017 `Roadway Maintenance` = $65,671,000.**

⚠️ **It is a SEPARATE PROGRAM from `Snow and Ice Control` ($63,709,000)**, so it
is maintenance-only — the right comparator in kind for a maintenance rate, with
no snow double-count. Composition (category is expense *type*, not service):

| category | FY2017 |
|---|---|
| Personnel | $50,786,000 |
| Fleet Services | $26,249,000 |
| Materials, Goods, and Supplies | $17,974,000 |
| External Services | $11,941,000 |
| Utilities & Other Charges | $1,442,000 |
| Transfer to Reserves | $450,000 |
| Intra-municipal Recoveries | −$14,904,000 |
| Intra-municipal Charges | −$28,267,000 |
| **total** | **$65,671,000** |

**$65,671,000 ÷ 11,000 km = $5,970/km — 4.65× the $1,285.**

(11,000 km is the article's own roads figure. It is the snow denominator; the
article states **no** denominator for $1,285 — see §3.)

## 3. What this does to the 2.6× gap

| maintenance half | + snow $3,350 | operating all-in | gap vs $12/m/yr lifecycle O&M |
|---|---|---|---|
| **$1,285** (as shipped) | | **$4.635/m/yr** | **2.59×** |
| $5,970 (published, FY2017) | | $9.32/m/yr | **1.29×** |
| $7,974 (escalated 1.336× to 2025) | | $11.32/m/yr | **1.06×** |

The escalation is the `Parks & Roads Services` branch's own FY2017→FY2025 growth
($244,856,000 → $327,064,221 = **1.3357×**), computed from the fetched CSV's own
rows (58 branch rows in FY2017, 42 in FY2025) — **not recalled**.

⚠️ **Its agreement with `DATA.md` §16's "~34% ($244.9M → $327.1M)" is NOT
corroboration.** §16 was itself derived from this same portal, so the two are one
source restated. **This is the same trap as the 3% set-aside cross-check demoted
2026-09-03** (`roadway_om_renewal.cross_check`) — do not count it twice.

⚠️ **ENDPOINT SENSITIVITY — FY2025 is the SERIES MAXIMUM**, and FY2026 is lower
($307,325,053). The escalated row above therefore uses the more favourable of the
two available endpoints. Both are disclosed:

| endpoint | growth | maintenance | operating all-in | gap vs $12 |
|---|---|---|---|---|
| **FY2025** (used above; §16's year) | 1.3357× | $7,974/km | $11.32/m/yr | **1.06×** |
| FY2026 | 1.2551× | $7,493/km | $10.84/m/yr | **1.11×** |

**The conclusion is robust to the choice — both land near 1.1×** — but the
uncorrected FY2017 comparison (**1.29×**) is the one that needs no escalation
assumption at all, and is the safer figure to quote.

**The open item's premise — that two sources irreconcilably disagree about the
cost of maintaining a road — does not survive.** Substituting the published
program for the narrow rate closes 2.59× to 1.29×, and correcting the 2017
vintage closes it to ~1.1×.

## 4. ⚠️ Why this is NOT a licence to substitute $5,970

Three things block a straight swap, and the first two are structural:

1. **The arterial blend cuts the wrong way.** $5,970/km is a citywide average
   over ~11,000 km **including arterials**, which cost more per km to maintain
   than locals. Applied to the collector+local metres in `road_m_per_acre` it
   would **overstate** — the identical mismatch `roadway_ops.denominator_mismatch`
   already flags for the $3,350 snow blend. Restricted to local roads the true
   rate is lower, which **re-widens** the gap against $12.
2. **The comparison mixes populations either way.** $12/m/yr derives from a
   figure the City states for a *neighbourhood* road; $1,285 and $5,970 are both
   citywide blends. ⚠️ **That mismatch was inside the original 2.6× too** —
   neither number is clean, and the reconciliation in §3 is therefore
   directional, not exact.
3. **Vintage.** FY2017 is the only year with a roads-only maintenance program
   (§17: re-cut in 2018 into `Infrastructure Maintenance`, which also covers
   sidewalks, pathways and bridges, and again in 2026 into
   `Mobility Infrastructure Services`). The 1.336× escalation is *branch*-level
   growth applied to a *program* figure — a proxy, not a deflator.

⚠️ **WHAT $1,285 ACTUALLY MEASURES IS STILL UNKNOWN.** The article gives it no
denominator and no scope, and **no clean decomposition of the published program
reproduces it** — materials-only ($17,974,000 ÷ 11,000 km = $1,634/km) is the
closest and is still 1.27× off. Do not invent a scope for it.

## 5. The decision this leaves open (PETER'S CALL)

⚠️ **The same $1,285 figure was REJECTED in one place and RETAINED in another.**
`DATA.md` §16 retired `$1,285/km × ~11,000 km = $14.135M` as **~5× too low** on
2026-08-04 — and it had been live on a public page. The same $1,285/km remains
the maintenance half of the shipped `roadway_ops` rate. **That split treatment
should not stand**, whichever way it resolves:

- **Re-scope the operating rate** using the published program, with an explicit
  arterial-blend caveat matching the one snow already carries. Changes a served
  column (`cost_roads_ops_per_acre`) and every blurb quoting $4.635 — a data
  contract change, so it needs a proposal first.
- **Keep the value and document the contradiction** — record that the
  maintenance half is a narrow line the City's own program contradicts by 4.65×,
  and that the operating basis is therefore a **floor**, the way
  `roadway_om_renewal` is now documented as a floor on the lifecycle side.

Note the symmetry if it helps the call: **both bases are now known to be floors,
for independent reasons** — lifecycle by the NRP reconstruction cross-check
(`FINDINGS_nrp_reconstruction_cross_check.md`), operating by this.

## 6. Reproduction

Both hosts are reachable from the Oracle box. ⚠️ Use `certifi` — this box's CA
bundle is stale and pre-2021 roots fail (`DATA.md` §13's blanket "edmonton.ca is
unreachable" is true only of `www.`; `budget.edmonton.ca` returns 200).

```python
import urllib.request, ssl, certifi, pandas as pd
ctx = ssl.create_default_context(cafile=certifi.where())

url = "https://budget.edmonton.ca/api/operating_budget.csv"
with urllib.request.urlopen(url, context=ctx, timeout=90) as r:
    open('/tmp/opbudget.csv', 'wb').write(r.read())      # expect 1,037,656 bytes

d = pd.read_csv('/tmp/opbudget.csv')
r = d[d.program.astype(str).str.contains('Roadway Maintenance', na=False)]
print(r.groupby('budget_year')['budget'].sum())          # expect FY2017 $65,671,000 only
print(r[r.budget_year == 2017].groupby('category')['budget'].sum())

NET, SNOW = 11000.0, 3350
prog = 65_671_000
print(f"{prog/NET:,.0f}/km  = {prog/NET/1285:.2f}x the shipped $1,285")
print(f"operating all-in -> ${(prog/NET + SNOW)/1000:.2f}/m/yr  vs $12.00 lifecycle O&M")

b = d[d.branch.astype(str).str.contains('Parks', na=False)].groupby('budget_year')['budget'].sum()
print(b)                                                  # ⚠️ FY2025 is the series MAX
print(f"2017->2025: {b.loc[2025]/b.loc[2017]:.4f}x")      # expect 1.3357
print(f"2017->2026: {b.loc[2026]/b.loc[2017]:.4f}x")      # expect 1.2551 (endpoint sensitivity)
```

⚠️ **Derive the growth from these rows; do not recall it.** It coincides with
`DATA.md` §16's "~34%", and **that is one source restated, not two agreeing.**

The article sentence in §1 is at `roadway_ops.source.url`; fetch it with a
`User-Agent` header set.

## 7. Corrected in passing

`bikeway_ops.rejected_lifecycle_reading` stated $178/km was *"~0.09%/yr, ~33×
low"* against the 3% rule. That was computed against an implied ~$200,000/km
asset value — **written 2026-08-03, the day BEFORE `bikeway_capital`
($452,065/km) was sourced (2026-08-04)**, and never updated to it. On the
sourced figure $178/km is **0.039%/yr, 85× low**. ⚠️ **The rejection is
strengthened, not weakened** — only the stated multiple was stale. Fixed in
`city_unit_costs.json` in the same commit as this file.
