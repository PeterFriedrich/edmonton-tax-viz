# Fable Brief — Services COST Lens DECISION Audit

Read this in full before opening any code. This is the third decision brief in
the house pattern (`docs/FABLE_AUDIT_development_lens.md` §0 is the rule; read
that section first if you have not). It audits the **fundamental decisions**
behind the *dollar* side of the Services lens — every column that
`data/city_unit_costs.json` feeds — **top-down, highest level first**. Code
correctness is the bottom of the stack, not the point.

**Scope.** The levy-side cost family only: `svc_cost_per_acre`,
`cost_roads_life_per_acre`, `cost_roads_ops_per_acre`, `cost_transit_ops_per_acre`,
`cost_bike_ops_per_acre`, `transport_cost_ops_per_acre`, the Ratio view's
"Per service $" denominator, and the Services hood panel. **Out of scope:** the
physical supply/demand columns (`road_m_per_acre`, `fire_events_per_acre`,
`transit_dep_per_acre`, `bike_m_per_acre` — they carry no cost model and are the
ground the dollar columns stand on), and the EPCOR-modeled utility charges
(storm/water — a different money flow, `docs/SPEC_utilities.md`, validated in
`docs/FINDINGS_utility_validation.md`).

**Why this target now.** The cost side has had build-time verification, one
back-solve from served output (S114) and one input cross-check (S94) — and both
of the defects the project has found in its own published numbers were on this
side: a budget-pod figure ~5× low (S94), and a shipped rate contradicted 4.65× by
the City's own program while the same figure had been retired elsewhere in the
repo for a month (S139, `docs/FINDINGS_roadway_maintenance_rate.md`). An
unaudited surface with confirmed defects of that shape is where the next one is.

## 0. The one rule

**Evaluate the stack in order; when a level is UNSOUND, everything beneath it is
moot for that branch.** Verdicts are **SOUND / CONDITIONAL / UNSOUND**, each with
the single sharpest argument against and what evidence would change it. We are
not looking for reassurance — the authors believe the caveats carry the map;
your value is the argument they didn't make against themselves.

⚠️ **This stack FORKS at the second level.** Two kinds of dollar column exist
and they fail differently: **allocation terms** (a citywide budget ÷ a citywide
count × the hood's count — fire, transit) and **rate terms** (a published unit
cost × the hood's metres — roads, bike). Level 1 and Level 2 are siblings under
Level 0, not parent and child. An UNSOUND at Level 1 moots the *allocation*
branch's comparison and copy; it does **not** moot the rate branch.

## 1. Ground yourself first (in this order, then stop reading and start judging)

1. `docs/SPEC_services.md` — "Transportation lens" Stage 2, "Roads cost —
   lifecycle", and the fire/transit lens sections (the physical lenses the
   dollars scale).
2. `docs/SPEC_utilities.md` decision 3 — where the "total services" question
   was decided and the V2 composite was born.
3. `data/DATA.md` §13 (the unit-cost file), §16–§17 (the budget context and
   the portal that corrected it).
4. `data/city_unit_costs.json` — read the `_two_bases` field and every
   `caveat` / `*_mismatch` / `*_contradiction` block. The authors' own
   objections are already written down here; your job is to weigh them.
5. `docs/DECISIONS.md` — search `2026-07-10`, `2026-07-15`, `2026-07-16`,
   `2026-08-02`, `2026-08-03`, `2026-08-07`, `2026-08-10`, `2026-09-02`.
6. `docs/FINDINGS_roadway_maintenance_rate.md` and
   `docs/FINDINGS_nrp_reconstruction_cross_check.md` — the two findings that
   already call both road bases floors.
7. `docs/AUDIT_LEDGER.md` rows S94, S114, S134, S139 — what has been checked and
   how, so nothing is re-derived.

Then confirm one thing back before proceeding, with the code that proves it:
**every dollar column on the map is a physical column multiplied by ONE
citywide constant** — a rate, or a budget divided by the pipeline's own
citywide total. There is no observed per-neighbourhood spend anywhere in the
served file. (`src/join_and_calculate.py`: the `unit_costs` branches; the S114
back-solve recovering $50.0001/m and $3,142/event from served output is the
independent proof.) State that you've confirmed it — it is the hinge of Levels
1–3: a single-term dollar map has the *identical* spatial pattern as its
physical column, so only a **composite** can show anything new, and a
composite's pattern is whichever term has the larger variance.

Also confirm the **public exposure** of each surface before judging severity
(`web/index.html`: `SERVICES[*].pub`, `SVC_COST_BASES[*].full`, the
`!FULL_BUILD` gates). At the time of writing: the public root carries roads
supply + the two roads cost rows + the Services panel's roads rows; the fire
composite, the Ratio view and the transit/bike cost rows are `/full/` only.

## 2. The decision stack

### Level 0 — Should modeled City DOLLARS be published per neighbourhood at all?
The physical lenses were designed to need *"no cost model or allocation
assumptions"* (SPEC_services "Why"). The dollar layer buys one thing they
cannot: comparability with the levy, which is also in dollars — and "revenue vs
cost" is the project's stated purpose.
- Every defect found on the cost side so far has been in the constants, not the
  geometry. Is a map coloured in dollars, under a "MODELED" label and a
  150-word blurb, read as spending regardless? (The S48 question about
  disclaimers as fig-leaves, asked again.)
- Is the honest alternative — physical quantities beside revenue, no dollars —
  actually worse for the reader, or just less satisfying?
- What would replace the model with observed money (the NRP publishes
  per-neighbourhood spend for some hoods — `FINDINGS_nrp_reconstruction_cross_check.md`)?

### Level 1 — The ALLOCATION terms: is `budget ÷ citywide count × hood count` a cost of serving the land?
`svc_cost_per_acre` = roads lifecycle + `fire_events_per_acre × (Fire Rescue
gross budget ÷ citywide kept events)`. `cost_transit_ops_per_acre` = ETS bus+LRT
gross ÷ citywide weekday stop-events × the hood's stop-events. Both carry the
caveat *"a mostly-fixed budget shared out, not a bill."*
- **Average vs marginal.** The caveat concedes the budget does not move with
  events. The map then colours land by exactly that motion. Measure it: what
  share of `svc_cost_per_acre`'s **variance** is the fire term? What does the
  composite's rank order correlate with — road metres, or fire events?
- **Consistency with the arterials decision.** Arterials were excluded because
  *"attributing their metres to the neighbourhood they happen to pass through
  would embed a city-wide quantity into a per-neighbourhood metric"*
  (DECISIONS 2026-07-01). A fire hall is *standing capacity* by the project's
  own description. Does the principle that excluded arterials admit fire?
- **Consistency with the 2026-08-03 transit decision.** The transport composite
  got NO UI row because *"a map coloured by the sum is a bus-service density
  map"* (transit 90.8% of the median). Apply the same test to
  `svc_cost_per_acre`, which has a UI row, a Ratio denominator and a panel row.
- **What the fire-dominated map actually shows.** Decompose the events of the
  hoods that top the composite by `event_description` (raw
  `data/raw/fire_response.csv`, `NOISE_GROUPS` filter, window years). If those
  hoods are the inner-city ones with shelters and supportive housing, and their
  events are predominantly medical, then the "revenue vs modeled service cost"
  ratio is a fiscal verdict on where vulnerable people live, not on a land-use
  pattern. Weigh that against the neutral-tone rule that excluded *alleys*.
- **Fire vs transit are not the same case.** Transit is a *supplied* service
  allocated by *supply* (ETS chooses the schedule; drivers and fuel scale with
  service-hours). Fire is standing capacity allocated by *demand*. Judge them
  separately.
- Salvage: is the fire *demand* lens (`fire_events_per_acre`, already shipped)
  the honest thing, with the dollar term retired? If a fire *cost* is wanted,
  what allocation matches a capacity service (station catchments — noting that
  DATA.md §12's levy catchments are 12 greenfield polygons, not station
  coverage, and §8's stations are points only)?

### Level 2 — The RATE terms: one citywide published unit cost × collector+local metres
`cost_roads_life_per_acre` ($50/m/yr, `roadway_om_renewal`),
`cost_roads_ops_per_acre` ($4.635/m/yr, `roadway_ops`), `cost_bike_ops_per_acre`
($20.278/m/yr).
- **A uniform rate makes the dollar map a re-labelled metres map** (Spearman
  1.0 by construction). What does the dollar layer add beyond the panel's
  level-vs-levy comparison? Is the *map colour* carrying any information the
  roads-supply layer does not?
- **The $1,285/km split treatment** (S139): retired as ~5× low in DATA.md §16,
  shipping as the maintenance half of `roadway_ops` in §13, on the public root.
  Is "documented as a floor" a sound *state*, or a contradiction the repo is
  carrying knowingly? Check the roads-ops blurb's own arithmetic against the
  figures it names.
- **Basis choice as a free variable**: the 25-vs-50-year life doubles or halves
  the lifecycle rate; `_two_bases` puts the same metres 10.8× apart. Is
  publishing *both* bases (with "never sum" scaffolding in layout, caption and
  a guard) sound, or does it delegate a decision to the reader that the authors
  could not make?
- **Numerator/denominator mismatches recorded but not absorbed** (snow blend
  includes arterials; rate calibrated to local roads applied to collectors;
  bike snow denominator is not bikeways). Are they directional and small, or do
  any of them flip a rank?
- Evidence that would change the verdict: per-neighbourhood observed spend (the
  NRP), or a per-class published rate.

### Level 3 — The comparison to the levy: Ratio view "Per service $" and the Services panel
Ratio: `revenue_per_acre ÷ svc_cost_per_acre`, log colour, $230 floor, framed as
**magnitude not break-even** (DECISIONS 2026-07-16: *"never 'pays its way'"*, no
1.0 marking). Panel (2026-08-10): each cost as a **fraction of this hood's
levy**, bar saturating at 100%, over-100% painted amber, grouped by basis, "There
is no total."
- Two locks, one question: does a bar that saturates at 100% and turns amber
  above it *present* break-even, whatever the ratio view's copy says? Read the
  `renderServiceCost` comment on what question the panel answers. If the 2026-08-10
  decision amended 2026-07-16 without saying so, name it.
- Which hoods actually cross 100% on each row, and are they set-aside (greyed
  elsewhere) or developed land?
- Numerator scope: the municipal levy funds the whole City; the denominator is
  one or two services. Is "% of levy" an honest share (roads *would need* 9% of
  this hood's levy) or an invitation to add?
- (Allocation branch: moot if Level 1 is UNSOUND — say so and stop.)

### Level 4 — Communication honesty
Blurbs (`SERVICES.roadscost/roadslife/transitcost/bikecost/servicecost`),
`RATIO_DENOMS.servicecost`, the panel note, `#about` sources.
- Does each blurb state the *strongest known fact against its own number*? The
  roads-ops blurb says "low end of a range"; the City's own program says 4.65×.
- Check every stated ratio's arithmetic against the figures it names.
  `scripts/check_cost_copy.py` checks literals, not arithmetic — it cannot catch
  a correct number compared against the wrong base.
- Is a row labelled "Service cost" honest when most of its variance is one
  allocation?

### Level 5 — Code correctness (only after the above)
`join_and_calculate.load_unit_costs` + the `unit_costs` branches; the
all-or-nothing rules; the pre-join fire divisor; `_two_bases` test;
`check_cost_copy.py`; `verify-services.js`, `verify-transport-cost.js`,
`verify-ratio-denom.js`. Check the tests test the *right* thing.

## 3. Reporting discipline

One verdict line per level (and per branch at Levels 1–2), the sharpest
counter-argument, the evidence that would change it, and — where UNSOUND — what
beneath it is mooted and whether it is salvageable under a different top-level
choice. Every number quoted must be measured in-session from the **served**
file or the raw inputs with the command shown, not recalled from a doc. Do not
edit `web/index.html`, `data/city_unit_costs.json` or any served column: the
remedies are Peter's calls, and at least one of them is a data-contract change
that needs a proposal first. Write findings to `docs/FINDINGS_services_cost_lens_verdict.md`;
add the ledger row; put every Peter's-call in `TODO.md`.
