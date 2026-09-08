# Fable Brief — Road Figures CONSOLIDATION

Read this in full before opening any code or any number. This is the sixth
decision brief in the house pattern (`docs/FABLE_AUDIT_development_lens.md` §0
is the rule; read that section first if you have not).

⚠️ **This one is shaped differently from the other five, and the difference is
the point.** The others audit a decision stack that lives entirely inside the
repo. This one audits a stack that has **three separate bodies of evidence that
have never been put in the same room**: what the repo ships, what the external
research docs hold, and what the City's own published money says. Four audits
have each touched a slice of the road figures (S114, S134, S136, S139) and each
one moved a number — but **nobody has ever reconciled the whole set against
itself.** That is this brief.

**Scope.** Every road-cost figure this project holds, on both bases, plus their
denominators and the City sources behind them. **Out of scope:** the fire and
transit allocation terms (audited S142, `docs/FINDINGS_services_cost_lens_verdict.md`;
the composite that carried them is retired), the EPCOR-modelled utility charges,
and anything on the revenue side.

**Explicitly NOT in scope: re-deriving a new rate.** If the reconciliation says a
shipped rate is wrong, say so and say by how much — do not propose a replacement
number. Every replacement this project has taken has come from a named City
publication after a scoped question, never from an audit's arithmetic.

---

## §0 — The one rule, and the fork below it

**Evaluate the stack in order; when a level is UNSOUND, everything beneath it is
moot for that branch.** Verdicts are **SOUND / CONDITIONAL / UNSOUND**, each with
the single sharpest argument against and what evidence would change it. We are
not looking for reassurance — the authors believe the caveats carry the map;
your value is the argument they did not make against themselves.

⚠️ **The stack forks at Level 2 into NUMERATOR and DENOMINATOR**, and the
project's history says the denominator is where it has actually been wrong.
The $1,285/km defect (S139) was a numerator error and it was caught. The 14%
"unmapped land" retraction (S104) and the snow-blend bias (S134 Q5) were both
denominator errors, and both survived longer.

---

## §1 — The hinge fact, confirm before descending

**Two road cost bases ship in the same served GeoJSON and they differ by 5.4×.**

| column | basis | rate | what it claims |
|---|---|---|---|
| `cost_roads_ops_per_acre` | operating | **$9.32/m/yr** | annual operating spend |
| `cost_roads_life_per_acre` | lifecycle | **$50/m/yr** | whole-of-life O&M + renewal, annualized |

Both apply to the **same** collector+local centreline metres. Confirm this from
`data/city_unit_costs.json` (`_two_bases`, `roadway_ops`, `roadway_om_renewal`)
before going further — if the file no longer says this, the brief is stale and
you should say so first.

⚠️ **The 5.4× is not a defect on its face** — the two measure different things
and `_two_bases` says so at length. The question this brief asks is one level
up: **after four audits, does either basis reconcile against City money at the
citywide aggregate, and do they still disagree by an amount the two-bases
framing can carry?**

---

## §2 — Grounding order (read these, then stop reading and start judging)

1. `data/city_unit_costs.json` — `_two_bases`, and every `caveat` /
   `*_mismatch` / `*_contradiction` / `floor` block. **The authors' own
   objections are already written down here; your job is to weigh them, not to
   rediscover them.**
2. `docs/FINDINGS_roadway_maintenance_rate.md` — why the operating rate moved
   $4.635 → $9.32/m/yr, and why it is still called a FLOOR.
3. `docs/FINDINGS_nrp_reconstruction_cross_check.md` — the only observed-money
   check ever run on the lifecycle side; it **did not corroborate**.
4. `data/DATA.md` §13 (unit costs), §16–§17 (budget context and the portal),
   §19 (road supply).
5. `docs/DECISIONS.md` — `2026-07-01` (the denominator), `2026-07-15`,
   `2026-08-02`, `2026-08-03`, `2026-08-07`, `2026-09-02`, `2026-09-03`,
   `2026-09-05`, `2026-09-06`.
6. `docs/AUDIT_LEDGER.md` rows **S114, S134, S136, S139** — what has already
   been checked, and with what result.
7. **The four documents OUTSIDE the repo** — all `.md` files in `/home/opc/`,
   named without the extension below so `check_doc_citations.py` does not read
   them as broken repo citations. They are deliberately not committed, so they
   cannot drift against `city_unit_costs.json`; **if a number there disagrees
   with the JSON, the JSON wins**:
   - `road_cost_numbers_inventory` — the repo-side inventory (S139).
   - `Road_Cost_Numbers_Research_Docs_Inventory` — the research-side
     inventory, written to sit beside it for hand-comparison.
   - `Reconciling_Edmonton_Road_Infrastructure_Cost_Figures` — the source
     research, updated 2026-09-05.
   - `Calgary_Road_Infra_Cost` — the comparator report. ⚠️ **Triaged
     2026-09-08 and mostly moot** (see §5); read its Q7 table and its two
     *Edmonton* figures, skip the rest.

---

## §3 — The levels

### L0 — Is publishing a road cost still the right call at all?

Every basis this project has is now explicitly a **floor**, and no two City
sources agree within 1.7× on the same program. The map colours land by these
numbers. The prior on this level is that L0 is SOUND (the disclosure is on
screen, both bases are named, the caveats ship) — **but it has never been
stated as a decision and tested**, and the S142 audit retired a whole column
one level down without this level ever being asked.

The sharpest argument against, which you should try to beat: *a reader cannot
act on a number whose own file calls it a floor and whose two bases differ 5.4×,
so the honest publication is the physical supply (`road_m_per_acre`) with the
dollars in prose.*

### L1 — Does each basis reconcile against City money at the CITYWIDE aggregate?

⚠️ **This level has never been examined.** S136 ran the observed-money check
**per neighbourhood**; the citywide version is a different measurement and a
cheaper one.

The arithmetic below was run 2026-09-08 while triaging the Calgary report. **It
is a claim to reproduce, not a finding** — re-derive every term:

```
lifecycle  $50/m/yr × 3,654 km collector+local = $182.7M/yr
renewal half only, $38/m/yr × 3,654 km         = $138.9M/yr
operating  $9.32/m/yr × 3,654 km               =  $34.1M/yr

City Neighbourhood Renewal line, 2026 approved operating budget
                                               = $180.4M/yr
      ($174.386M transferred to capital + $6.0M microsurfacing operating)

capital_budget.csv, service `Neighbourhoods`, FY2023–2029
                    $716.5M over 7 years      ≈ $102M/yr
```

Three questions, in order:

1. ⚠️ **$182.7M vs $180.4M is 1.3% apart, and you should assume that is a
   coincidence until it survives.** The like-for-like comparison is the
   **renewal half alone** ($138.9M) against a capital renewal programme, and
   that is 1.3× the *other* way. NRP's numerator also bundles alleys,
   sidewalks, lighting and drainage — the bias
   `FINDINGS_nrp_reconstruction_cross_check.md` already documents. **Two errors
   of opposite sign landing on a near-match is a pattern this project has been
   burned by.** Which comparison is the honest one?
2. **$102M/yr (capital budget) vs $174.386M/yr (operating budget transfer) is a
   1.7× disagreement between two City publications about the same programme.**
   Is it a scope difference, a vintage difference, or is one of them wrong? This
   bears directly on question 3 below.
3. **Neither $180.386M nor $174.386M appears anywhere in the repo** (zero hits,
   confirmed 2026-09-08). Should the annual NRP line be a committed reviewed
   input beside the capital budget, or does adding it create a second drift
   surface that `check_cost_copy.py` would not guard?

### L2a — NUMERATOR: is every shipped rate still traceable to a live source?

The operating rate's maintenance half moved to a published FY2017 programme
figure with a **branch-level growth proxy** applied for vintage. `DATA.md` §16
and the `roadway_ops` block both record that this is a proxy, not a deflator.
Is the vintage correction still the right call, and is the FY2017-vs-FY2017
fallback (1.29×) the one that should be quoted?

### L2b — DENOMINATOR: the level this project actually gets wrong

Three unresolved denominator questions, all live:

1. **The residential lane-km conflict.** A City FAQ says *">4,000 lane-km"*
   residential; a councillor page says *"~9,000 lane-km (~75% of network)"*.
   The repo computes **3,654 km collector+local CENTRELINE**. ⚠️ **Different
   units — lane-km vs linear km — so this may be no conflict at all**, and the
   research inventory §6 flags exactly that possibility without resolving it.
   Resolve it, in one direction or the other.
2. **The repo cites both 3,654 km and 3,644 km** in different places — a 10 km
   / 0.27% discrepancy nobody has reconciled.
3. **The snow term's denominator still blends arterials** (~11,000 km citywide)
   while being applied to collector+local metres — a documented overstatement
   whose size has never been measured. The Calgary report shows Calgary's own
   snow budget IS priority-split, which is a method existence proof, not a
   number we can borrow.

### L3 — The leftovers, ranked last because they touch no shipped number

- The **$11,510.8M vs ~$11.56B** capital-budget gap (~$50M, cause not
  determined). The June 2026 council report was inaccessible when this was
  raised.
- The **$965.2M** maintenance figure's provenance — bracketed by
  $798.6M–$1,171.2M so plausible, never traced to a table.
- The **four unverified service-life figures**. ⚠️ Establish first *which four
  the repo means* — the research inventory §9 explicitly does not know, and
  lists three.

---

## §4 — Already closed. Do not re-open these.

⚠️ **The research-side inventory's own "where to focus" list is stale on its
biggest item**, and re-litigating it would waste the round:

- ✅ **The $5,970/km substitution SHIPPED 2026-09-06** (`DECISIONS.md`). The
  inventory calls it a hypothesis the repo "floated". It is not floated; the
  operating rate is $9.32/m/yr and **$1,285/km no longer ships anywhere**.
- ✅ **The 3%/yr set-aside cross-check is DEMOTED** (2026-09-03) — it restates
  the same page's own numbers and is not independent. Do not use it as
  corroboration for anything.
- ✅ **`svc_cost_per_acre` is RETIRED** (2026-09-05) with its Services row, its
  Ratio denominator and its panel row. Any finding about the roads+fire
  composite is moot.
- ✅ **The $500K / $2.5M / $17.5M per-neighbourhood figures never entered this
  repo** (zero hits for `microsurfac`). Their refutation is correct and moot
  here — same disposition as S134.

---

## §5 — Discriminators that keep the finding list honest

- ⚠️ **A refutation of something that never entered the repo is NOT a finding.**
  This is the single most common way a road-cost round has wasted itself (S134:
  most of a 7-question report re-derived what the repo already documented). Grep
  before you write it up.
- ⚠️ **A figure read off a SHIPPED file is not a fact about the world.**
  `neighbourhood_value_per_acre.geojson` is post-setback (`SETBACK_M = 45.0`),
  post-simplify DISPLAY geometry. Reading area off it understates by ~16% and
  overstates every $/m accordingly — it produced a retracted 14%-of-the-city
  claim (S104) and a wrong first run in S136. **Derive area from
  `data/raw/neighbourhoods.geojson` in EPSG:3400.**
- ⚠️ **Agreement between two figures that trace to the same pull is not
  corroboration.** The 1.336× growth multiplier matches a figure already in
  `DATA.md` §16 — both from the same CSV. Same category as the demoted 3% rule.
  **State the independence of every cross-check you claim.**
- ⚠️ **Two biases of opposite sign can manufacture a match.** Say which
  direction each error runs and roughly how big, or do not quote the agreement.
- ⚠️ **Lane-km, linear km and centreline km are three different denominators**
  and the sources mix them freely. Name the unit on every $/km you write.
- **The Calgary report's value is its EDMONTON figures**, not its Calgary ones:
  JOC quotes *"Edmonton… approximately 13,000 kilometres and a $158.8-million
  annual budget"* (→ $12,215/km), and Calgary's own Pavement Quality report
  quotes Edmonton/Montreal at *"$12,500–$17,000 per year"* per km. Both are
  secondary press, both have unstated scope (probably capital paving), and
  **neither is in the repo.** Treat as leads with a named scope question, not as
  a check — but this project has been chronically short of outside-in views of
  its own numbers.
- **Do not propose a replacement rate.** See the scope note at the top.

---

## §6 — How to report

Per level: the **verdict** (SOUND / CONDITIONAL / UNSOUND), the **single
sharpest argument against**, and **what evidence would change it**. For a
numeric finding, also: the **two figures**, the **scope and unit of each**, the
**direction and rough size of every bias you know about**, and whether the
comparison is **independent** or shares a source.

A level examined and found sound gets a line saying what you tested and that it
held — a clean level is a result, and an unexamined one must not read like one.

⚠️ **Rank by whether a reader's number moves.** The map colours land by these
figures; a finding that changes a caveat's wording and a finding that changes
`$50/m` are not the same size, and the report should not present them as if
they were.
