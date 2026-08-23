# SPEC — the break-even lens (Lab, proposal)

**Status: PROPOSAL. Nothing here is built.** Opened 2026-08-11 from Peter's
ask: *"we could actually hypothetically have pipelines to estimate for each type
of cost, then keep improving them… a setup that would let us attack each cost
category, and even issues in each hood, one at a time."*

**Read `docs/SPEC_services.md` and `data/city_unit_costs.json` first** — the cost
side already exists in pieces, and this proposes a frame to hold them, not a
restart.

---

## 0. THE ONE THING THAT DECIDES WHETHER THIS WORKS

A break-even number is `revenue − cost`. We model the revenue side at **$2,715M**
and, on the operating basis, the cost side at **$473M** — **15.5% of the City's
$3,055.2M operating-only budget** (§8 #1/#7, settled 2026-08-23: operating
basis, operating-only denominator — the $3,846M/12.3% figure this section
originally quoted used the full tax-supported budget, since superseded).

Computed today, the lens would say **every neighbourhood in Edmonton runs a
5.7× surplus.** That is not an uncertain answer. It is a **wrong answer in a
known direction**, and it would be wrong by roughly the same factor everywhere,
so it would look plausible and rank hoods in a defensible-looking order while
being false about every one of them.

⚠️ **So coverage is not a caveat on this lens. Coverage IS the lens.** The
headline is not "this hood nets +$8,000/acre"; it is *"of the $3.06B the City
spends operating this budget, we can place 31% of it geographically, and
against that 31% this hood nets +$8,000/acre."* Every design choice below
follows from that.

The good news is that this is the *shape of problem Peter described*: it
improves monotonically and category by category, and each increment is
independently checkable. The bad news is that **there is a long stretch where
the number exists and is not yet worth showing**, and the plan has to say who
decides when that ends.

---

## 1. What the number is

Per neighbourhood, per year, in the Lab only:

```
net_per_acre = revenue_per_acre − Σ (cost terms on ONE basis, status=shipped)
coverage     = Σ (control totals of those terms) ÷ tax-supported operating budget
```

**It is NOT** a cost-of-service study, and must never be called one — no
`COSA`, no "cost of service", in code, columns, filenames or UI copy. The same
rule the deviation lens ships under (`DECISIONS.md` 2026-08-11). This is a
**modelled net position against a stated fraction of city spending**.

Working name: **net position**. Alternatives: *modelled balance*, *pays-its-way
estimate*. Naming is Peter's (§8).

---

## 2. The cost register — the part that makes it incremental

One entry per cost category in a new `data/cost_register.json`, and **the
composite is computed from the register, never hand-assembled**. An entry
declares:

| field | why it exists |
|---|---|
| `basis` | `operating` \| `lifecycle`. **Load-bearing — see §3.** |
| `control_total` | the citywide dollars this category is allowed to distribute |
| `control_source` | the published line it comes from, with vintage |
| `driver` | the per-hood column the total is allocated by (`road_m_per_acre`, `fire_events_per_acre`, …) |
| `driver_justification` | one sentence on why that driver tracks this cost |
| `status` | `shipped` \| `stub` \| `unallocatable` \| `absent` |
| `confidence` | `sourced` \| `modelled` \| `assumed` — inherited from `city_unit_costs.json`'s existing discipline |

**Attacking one category = adding one entry and its allocation.** The composite,
the coverage meter and the guards all update themselves. That is the whole
architectural point, and it is the same move `SERVICES` already makes in
`web/index.html` and `LAB_EXPERIMENTS` makes for Lab views.

Allocation follows the pattern already proven twice (fire, transit): **take a
published citywide control total and distribute it by a per-hood driver, divided
by the pipeline's own citywide sum of that driver.** It is an *allocation*, not
a rate — `DECISIONS.md` 2026-08-03 makes that distinction and a test pins that
the terms sum back to the budget. Keep both properties.

### 2a. `unallocatable` is a first-class status, not a failure

Some spending has no defensible per-hood driver and probably never will —
governance, corporate services, debt servicing, much of social spending. **A
break-even that silently omits them is biased upward; one that pretends to
place them is fiction.**

Proposal: an explicit **unallocated residual** term, spread on a stated flat
basis (per acre, or per capita once dwelling counts are wired), **labelled as
smeared rather than modelled**, and reported separately in the readout:

```
this hood:  modelled −$4,120/acre   ·  smeared −$6,880/acre   ·  net −$11,000/acre
coverage:   modelled 31%  ·  smeared 54%  ·  unmodelled 15%
```

This is what lets coverage honestly approach 100% without claiming spatial
knowledge we do not have — and it makes the *modelled* fraction the thing that
improves as categories land, which is the metric of progress for this project.

---

## 2b. ⚠️ RULE: every driver declares SITE-BOUND or NETWORK-SHARED

**A cost may only be distributed by a local count when the service is consumed
where it is supplied.** Register entries carry `driver_scope`:
`site_bound` | `network_shared`, and **only `site_bound` terms are allocated per
hood**. `network_shared` terms go to the §2a residual, or to a separate
citywide-shared layer — never to a local count.

The reasoning generalises a defect that shows up first in *functional
population*, the standard technique for splitting shared costs between
residential and non-residential. It assumes the service-consuming population is
bounded by the unit that pays. That is true of a municipality and **false of a
neighbourhood**: an office worker downtown consumes road, transit and water
infrastructure across every hood they transit, so charging their weight to the
destination hood overstates it and understates everywhere they came from.

⚠️ **But the fix is NOT "exclude the non-residential share."** That prescription
is over-broad, and applying it would corrupt terms that are already correct.
The distinction is not residential vs non-residential — it is whether the
driver is bound to the site:

| term | driver | scope | verdict |
|---|---|---|---|
| fire | dispatches at the address | `site_bound` | correct as-is — the fire *is* there |
| stormwater | impervious area | `site_bound` | correct as-is — physically bound |
| roads | local + collector metres in the hood | `site_bound` | correct as-is; **arterials already excluded as shared infrastructure** (`DECISIONS.md` 2026-07-01) — the same rule, found empirically before it was named |
| **transit** | **scheduled departures at stops in the hood** | **`network_shared`** | ⚠️ **fails the test — see below** |

The arterial exclusion is this rule discovered early and by instinct. Naming it
is what makes it apply to categories nobody has built yet.

### ⚠️ 2b-i. The rule's first casualty is a term ALREADY SHIPPING

`cost_transit_ops_per_acre` allocates the ETS operating budget by **scheduled
stop-events in each hood**. A downtown stop's departures are charged to
downtown, but they are consumed by people boarding from every hood in the city.
By the test above that driver is `network_shared`, and the term is currently
distributed as if it were site-bound.

This matters out of proportion to its size: transit is **90.8% of
`transport_cost_ops_per_acre`** (`DECISIONS.md` 2026-08-03).

⚠️ **Do NOT "fix" it by deleting the term.** Two things are already recorded
against a hasty read: the figure is a **share, not a rate** (an annual budget
over a mean-weekday count — meaningless as a unit, exact as an allocation), and
the locked framing is **demand-allocation-of-a-fixed-budget**, which is a
defensible thing to publish *as such*. The open question is narrower and should
be written down before it is answered: **is "where service is supplied" an
honest proxy for "who consumes it" at neighbourhood grain?** Supply-side
allocation is the only thing the data supports — no stop-level ridership exists
(citywide-monthly only, `DECISIONS.md` 2026-07-11) — so the realistic outcomes
are relabelling it, moving it to the residual for break-even purposes while it
stays as-is in the Services lens, or leaving it and stating the limit.

**Its own item in `TODO.md`. It does not block the register.**

---

## 3. ⚠️ ONE BASIS, AND THIS IS THE TRAP THAT WILL EAT THIS LENS

`svc_cost_per_acre` is **lifecycle** ($50/road-m/yr). `cost_roads_ops_per_acre`
is **operating** ($4.635/road-m/yr). **The same metres, ~10.8× apart.**
`city_unit_costs.json`'s own `_two_bases` field exists to keep them apart, and
`DECISIONS.md` 2026-08-02/03 refuses a single headline cost number precisely
because summing across bases is *arithmetically true and descriptively false*.

Rules:

1. **Every term in a composite declares a basis, and the composite refuses to
   compute across mixed bases.** Not a warning — a hard error. This is the one
   failure that produces a confident wrong number with no visible symptom.
2. **Two composites may exist** (`net_operating_per_acre`,
   `net_lifecycle_per_acre`) but they are never added, never averaged, and never
   shown as one number.
3. The control totals must be on the same basis as the driver rate. A lifecycle
   control total distributed by an operating driver is the same error wearing a
   hat.

**Recommendation: build the OPERATING basis first.** The City publishes an
operating budget with program-level detail (§4), it is the larger and better-
sourced universe, and the lifecycle basis currently rests on two unit costs and
a *missing bikeway service life* that this project already established Edmonton
does not publish (`TODO.md`).

---

## 4. Build order — attack by budget share, and the first task is measurement

⚠️ **We cannot currently rank the categories, and that is task one.** The
per-hood cost work so far grew from what was *measurable*, not from what is
*expensive*, so the register would start lopsided.

**Task 1 — ingest the Open Budget portal.**
`https://budget.edmonton.ca/api/operating_budget.csv` (`data/DATA.md` §17):
7,283 rows, FY2017–FY2026, program-level, machine-readable, tax-supported.
It is the only public source with sub-branch detail. Produces the ranked list
of *what actually costs money*, and the denominator for coverage.

⚠️ Three quirks are already documented and all three bite here: **program names
do not survive two re-cuts** (2017 / 2018–2025 / 2026 — never `groupby(program)`
across eras), **every figure is gross** (`account_type` is `Expenses` only, no
revenue side), and **the portal and the PDF do not tie** (+1.31% on Parks and
Roads Services).

✅ **CORRECTED 2026-08-13: this is NOT a laptop-only fetch.** This section used to
say *"edmonton.ca is unreachable from the Oracle box, so this is a laptop fetch
or a CI-side fetch"*. **`budget.edmonton.ca` is a different host from
`www.edmonton.ca` and it resolves fine from the Oracle box** — measured
2026-08-13, `HTTP 200`, 1,037,656 bytes, 7,283 rows, against `www.edmonton.ca`'s
connection failure (`000`) in the same sweep. `data.edmonton.ca`, `alberta.ca`
and `open.alberta.ca` also resolve. **Task 1 is executable here and has been
executed — see §4a.** ⚠️ The §13 blanket claim *"edmonton.ca is unreachable"* is
true only of `www.`; do not re-derive a blocker from it without testing the
specific host.

**Task 1b — ⚠️ A DWELLING-OR-POPULATION COUNT PER HOOD DOES NOT EXIST, AND
SEVERAL OBVIOUS ALLOCATIONS NEED ONE.** Checked, not assumed: nothing in `src/`
or the served GeoJSON carries population or employment. `new_dwelling_units` is
a **flow from permits, not a stock**; "employment" appears only as a *zoning
category label*; and the dwelling model the water and franchise lenses share is
internal — never emitted per neighbourhood.

So any per-capita or per-household allocation — including the residential half
of a functional-population split (§2b) and the §2a residual if it is smeared
per capita rather than per acre — is **blocked on an input we have not
ingested**. ⚠️ Note this also means the method §2b rules *out* (per-hood
employment) is not available either, so nothing is lost by the rule today; the
cost is entirely on the allocations we would want to add.

Cheapest route first: the water/franchise dwelling model already exists and
could be emitted as a column, which needs no new source and inherits its
documented assumptions. Census population is the alternative and is a new
ingest with its own boundary-matching problem (census tracts are not
neighbourhoods).

**Task 2 — order the register by control total, then build downward.** Expect
transit, police, fire and parks to dominate. Fire and transit already have
allocations; police is the largest category with *no driver in hand* and is
where the plan will first hit §2a.

**Task 3 — each category is its own unit of work**, with its own driver
justification, its own reconciliation test, and its own `AUDIT_LEDGER.md` row.
This is the "one at a time" property Peter asked for, and it is what keeps the
lens reviewable as it grows.

---

## 4a. Task 2 EXECUTED — the register, measured (2026-08-13)

**Pinned to FY2025** to match `ASSESSMENT_YEAR = 2025` on the revenue side, and
to sit inside the 2018–2025 program-naming era rather than straddling the 2026
re-cut. `fund_type == 'Tax Supported'`. **Total $3,855.9M across 656 rows and
144 programs** (the $3,846M quoted in §0 is the PDF; the 0.26% gap is the same
portal-vs-PDF seam as the +1.31% above — **do not present them as one series**).

**144 programs, but the head is short: the top 25 are 76.5% of the budget.** The
register is tractable. Top 12:

| $M | % | cum | program | branch |
|---|---|---|---|---|
| 597.2 | 15.5% | 15.5% | Police Service | Police Service |
| 449.1 | 11.6% | 27.1% | OPS/ETS - Bus and LRT | Edmonton Transit Service |
| 221.0 | 5.7% | 32.9% | Tax-supported Debt Charges | Capital Project Financing |
| 208.2 | 5.4% | 38.3% | CS/FRS - Operations and Training | Fire Rescue Services |
| 174.4 | 4.5% | 42.8% | Alley Renewal | Neighbourhood Renewal |
| 142.9 | 3.7% | 46.5% | Pay As You Go Funding | Capital Project Financing |
| 134.0 | 3.5% | 50.0% | CS/CRC - Facility Operations | Community Recreation |
| 128.2 | 3.3% | 53.3% | OPS/PARS - Infrastructure Operations | Parks and Roads |
| 91.7 | 2.4% | 55.7% | BAC/EXP - Explore Edmonton | Explore Edmonton |
| 80.6 | 2.1% | 57.8% | CS/SD - Affordable Housing and Homelessness | Social Development |
| 74.6 | 1.9% | 59.7% | OPS/FFS - Facility Maintenance Services | Fleet and Facility |
| 73.2 | 1.9% | 61.6% | BAC/LIB - Edmonton Public Library | Public Library |

**§4 Task 2's prediction was right on three of four.** Transit, police and fire
do dominate, and **police is the largest line in the budget with no driver in
hand** — it is bigger than everything the pipeline currently models put together
($597.2M vs $473M). **Parks does not appear as its own top line**; it is inside
`OPS/PARS - Infrastructure Operations`, bundled with roads, which is the §17
bundling problem in a different place.

⚠️ **Police is also where the register meets its hardest editorial problem, not
just its hardest data problem.** Allocating $597.2M by any spatial driver
produces a per-neighbourhood policing-cost map. That is a far more charged
artifact than a roads-cost map, and **the driver choice would be doing the
arguing.** Flagging it here so the decision is taken deliberately rather than
arrived at by working down a ranked list.

⚠️ **"Find better data" was checked and does not escape this.** EPS's crime
dataset is real, live-queryable (Esri FeatureServer, not the "OGC API - Records"
a relayed claim asserted — corrected), and joinable by point-in-polygon like
schools/LRT — but the publisher anonymizes locations specifically because
per-area comparison is unreliable, which imports a documented bias rather than
resolving one. `docs/ANALYSIS_BACKLOG.md` §14. Population/dwelling surfacing
(Task 1b, above) remains the cheaper unblock if police is to be reached at all.

### ⚠️ THE FINDING THAT CHANGES §0: 20.8% OF THE DENOMINATOR IS NOT OPERATING SPEND

**$800.7M of the $3,855.9M "tax-supported operating budget" is capital
financing** — debt charges, pay-as-you-go, reserve transfers and renewal:

| $M | line |
|---|---|
| 221.0 | Tax-supported Debt Charges |
| 174.4 | Neighbourhood Renewal / Alley Renewal |
| 142.9 | Pay As You Go Funding |
| 57.1 | Valley Line LRT dedicated funding |
| 51.5 | External Debt Charges |
| 44.4 | SLRT Debt Charges |
| 38.4 | Valley Line LRT Debt Charges |
| 70.9 | 9 smaller lines (reserve transfers, Downtown Arena, local improvements) |

⚠️ **So §1's `coverage` formula divides an operating-basis numerator by a
denominator that is 20.8% capital — the §3 basis-mixing failure, hiding in the
coverage ratio itself rather than in the composite.** It is the more dangerous
location of the two, because §6 requires coverage to render wherever the number
does: a mixed-basis denominator would be **published on the face of the lens**.

Operating-only, the denominator is **$3,055.2M**, and the current cost side
covers **15.5%, not 12.3%**. Neither number is wrong; they answer different
questions, and the lens must state which one it is answering. **New decision,
§8.7.**

⚠️ **But capital financing is NOT uniformly unallocatable, and the build order
should not treat it as a block to skip.** `Alley Renewal` at **$174.4M** is
plausibly the single most spatially-allocatable line in the entire budget — it
is per-neighbourhood infrastructure renewal, on the **lifecycle** basis the
roads term already uses, and it would be a larger register entry than anything
currently shipped except transit. **Debt charges (~$400M) are the genuinely hard
part**, being service on capital already built; renewal is not.

---

## 5. ⚠️ The revenue side is not settled either

Do not treat `revenue_per_acre` as the solid half.

- Our modelled levy is **$2,715M** against the City's budgeted **$2,318M** —
  **17% apart.** A break-even that divides a 17%-high revenue figure by a
  partial cost figure compounds two errors in the same direction.
- **~$125.4M/yr of that revenue is the open institutional question**
  (`TODO.md`): we apply mill rates to every record on the roll, including
  AJ/PU/UI/UF parcels whose exemption status is not public. Direction of the
  error is **unknown, not merely unquantified** (`DECISIONS.md` 2026-08-08).
- Municipal levy is **not all the City's revenue** — user fees, grants, EPCOR
  dividend and franchise fees fund the same budget. A net position against
  *levy only* charges hoods for services partly paid another way. Either widen
  the revenue side or state the scope in the readout; **do not leave it
  implicit.**

**A break-even is only as sound as its weaker half, and today that is the cost
side by a wide margin — but not by as much as it looks.**

---

## 6. Guards (the shape the repo already uses)

- **Basis-mixing → hard error** (§3). The one silent killer.
- **Reconciliation test per category**: Σ per-hood dollars == the control total,
  to the cent. The existing transit test is the template.
- **Coverage is computed, never pinned**, and printed everywhere the number is.
  The `renderBudgetContext` lesson (`DECISIONS.md` 2026-08-03): a pinned share
  is precisely the artefact that failed there — publish values, derive ratios.
- **Coverage regression check**: coverage must not fall between refreshes
  without a matching register change. A category quietly dropping out would
  raise every hood's net position.
- **`verify-breakeven.js`**: the number never renders without its coverage;
  never named COSA; the modelled/smeared split is visible.

---

## 7. Where it lives

The Lab (`LAB_EXPERIMENTS`), full build only, from the first commit to whenever
Peter says otherwise. Adding it is one registry line plus its view branches.

It should be the **second** Lab experiment, and it is worth noting it makes the
first one better: the deviation lens is the same map with the cost side set to
zero, so the two read as a progression — *here is revenue density against the
city average; here is what happens when we start subtracting what we can
actually place.*

---

## 8. Decisions needed before any code

1. ~~**Basis** — operating first (recommended, §3), lifecycle first, or both in
   parallel?~~ **SETTLED 2026-08-23 (Peter): operating first.** Larger,
   better-sourced universe (656 rows / 144 programs / $3,855.9M, already
   ingested, §4a); lifecycle rests on two unit costs and a missing bikeway
   service life Edmonton doesn't publish.
2. **Name** — "net position"? It must not imply a cost-of-service study.
3. ~~**The publication gate** — at what modelled coverage is the number worth
   showing?~~ **SETTLED 2026-08-11 (Peter): there is no separate gate.** The
   Lab is full-build-only and `beta`-marked — *"the specialist lens is literally
   built for this"* — so the audience is already the one that can read caveats.
   The gate collapses into a requirement §6 already carries: **coverage must
   render wherever the number does.** Dropping that is what would make it
   dishonest, not the coverage level.
4. **Unallocated residual** (§2a) — in from the start, or omit and accept a
   known upward bias until coverage is high? If in: smeared **per acre** (works
   today) or **per capita** (blocked on Task 1b)?
5. **Revenue scope** (§5) — municipal levy only, or widen to the other
   tax-supported revenue that funds the same budget?
6. **Transit** (§2b-i) — relabel, move to the residual for break-even while the
   Services lens keeps it, or leave it and state the limit?
7. ~~**⚠️ NEW 2026-08-13 — the COVERAGE DENOMINATOR (§4a).** Is coverage measured
   against the full **$3,855.9M** tax-supported budget, or the **$3,055.2M**
   operating-only remainder after capital financing?~~ **SETTLED 2026-08-23
   (Peter): operating-only, $3,055.2M — coverage reads 15.5%, not 12.3%.**
   Decided together with #1: an operating numerator over the full,
   20.8%-capital budget is the exact basis-mixing §3 forbids, just hiding in
   the coverage ratio instead of the composite — the one place the composite's
   hard error would not catch it. Operating-only is also the higher, more
   flattering number, so there was no correctness-vs-optics tradeoff to make.
   ⚠️ **Disclosure debt this creates:** the lens must state the $800.7M capital
   exclusion explicitly (never silently fold it in), and `Alley Renewal`
   ($174.4M of that $800.7M) is allocatable lifecycle spend, not unallocatable
   — do not let "excluded from the denominator" quietly become "excluded from
   the register" when lifecycle-basis work eventually attacks it.

---

## 9. ⚠️ A confound that applies to the lenses ALREADY SHIPPING

Raised in review of this spec, and it is not confined to it: **a revenue-per-acre
gap between two neighbourhoods can be an income gap wearing a density costume.**
Edmonton's density gradient plausibly tracks its income gradient, so "denser
land pays more per acre" and "wealthier land pays more per acre" are not
separated by anything in this pipeline.

⚠️ **This bites the deviation lens that is live in `/full/` today**, whose whole
framing is who sits above and below the citywide average — precisely the reading
that a density/income confound would corrupt.

**We cannot currently test it: no income or demographic data is ingested.** So
the honest position is the one the project already takes elsewhere — descriptive
framing only, and never a causal claim like *"infill pays for itself"* — plus a
`TODO.md` item to decide whether an income variable is worth ingesting to
measure the confound rather than merely disclaim it. ⚠️ Ingesting one is not
free of hazard: a map that pairs neighbourhood income with fiscal performance
invites exactly the editorial framing this project refuses. **Measuring the
confound and publishing the variable are different decisions.**
