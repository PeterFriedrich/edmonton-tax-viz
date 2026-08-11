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
and, on the operating basis, the cost side at **$473M** — **12.3% of the City's
$3,846M tax-supported operating budget.**

Computed today, the lens would say **every neighbourhood in Edmonton runs a
5.7× surplus.** That is not an uncertain answer. It is a **wrong answer in a
known direction**, and it would be wrong by roughly the same factor everywhere,
so it would look plausible and rank hoods in a defensible-looking order while
being false about every one of them.

⚠️ **So coverage is not a caveat on this lens. Coverage IS the lens.** The
headline is not "this hood nets +$8,000/acre"; it is *"of the $3.85B the City
spends, we can place 31% of it geographically, and against that 31% this hood
nets +$8,000/acre."* Every design choice below follows from that.

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
Roads Services). Also: **edmonton.ca is unreachable from the Oracle box**, so
this is a laptop fetch or a CI-side fetch, like every other manual reviewed
input.

**Task 2 — order the register by control total, then build downward.** Expect
transit, police, fire and parks to dominate. Fire and transit already have
allocations; police is the largest category with *no driver in hand* and is
where the plan will first hit §2a.

**Task 3 — each category is its own unit of work**, with its own driver
justification, its own reconciliation test, and its own `AUDIT_LEDGER.md` row.
This is the "one at a time" property Peter asked for, and it is what keeps the
lens reviewable as it grows.

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

1. **Basis** — operating first (recommended, §3), lifecycle first, or both in
   parallel?
2. **Name** — "net position"? It must not imply a cost-of-service study.
3. **The publication gate** — at what modelled coverage is the number worth
   showing even to specialists? ⚠️ **Recommend deciding this NOW, before the
   number exists**, because deciding it afterwards means deciding it while
   looking at an answer you like.
4. **Unallocated residual** (§2a) — in from the start, or omit and accept a
   known upward bias until coverage is high?
5. **Revenue scope** (§5) — municipal levy only, or widen to the other
   tax-supported revenue that funds the same budget?
