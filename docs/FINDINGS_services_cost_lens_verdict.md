# FINDINGS — Services COST lens decision audit

**Run 2026-09-05 (S142) against `docs/FABLE_AUDIT_services_cost_lens.md`.**
Output of that brief: one verdict per level, the sharpest argument, the
evidence that would change it. **Nothing served was edited** — no column, no
rate, no copy. Every remedy below is Peter's call and is listed in `TODO.md`.

Every number here was measured this session from the served
`web/data/neighbourhood_value_per_acre.geojson` (406 hoods, refreshed
2026-09-02) or from `data/raw/fire_response.csv` with `load_fire`'s own
`NOISE_GROUPS` filter over 2023–2025, using the commands in §8. Nothing is
recalled from a doc.

---

## 0. The hinge fact, confirmed

**Every dollar column is a physical column × one citywide constant.**
`src/join_and_calculate.py`: `cost_roads_life_per_acre = road_m_per_acre × 50`;
`cost_roads_ops_per_acre = road_m_per_acre × 4.635`; the fire term is
`fire_events_per_acre × (276,706,000 ÷ citywide kept events)`; transit is the
same shape over stop-events. From the served file the implied fire rate is
**$3,142.08/event** — the figure S114's least-squares back-solve recovered.

Consequence: a single-term dollar map has *exactly* the spatial pattern of its
physical column (Spearman 1.0). Only a composite can show anything new, and a
composite's pattern belongs to whichever term has the larger variance.

**Public exposure, confirmed** (`SERVICES[*].pub`, `SVC_COST_BASES[*].full`,
the `!FULL_BUILD` gates): the **public root** carries roads supply, "Roads cost"
(operating), "Roads cost — lifecycle", and the Services panel's two roads rows.
The **fire composite** (`servicecost` row, the Ratio view's "Per service $", the
panel's "Roads + fire (incl. above)" row) and the transit/bike cost rows are
**`/full/` only** — an unlisted but public URL.

## 1. Verdicts

| level | verdict | one line |
|---|---|---|
| **0** publish modeled dollars at all? | **CONDITIONAL** | Buys comparability with the levy, which is the project's purpose — on condition the constants are defensible; every defect found so far has been a constant |
| **1a** fire allocation as a cost | **UNSOUND** | 88.6% of the composite's variance is a fixed budget shared out by dispatch count; the map is a fire-dispatch density map priced in dollars, and the dispatches are 61–78% medical in the hoods it singles out |
| **1b** transit allocation as a cost | **CONDITIONAL** | Same arithmetic, different case: a supplied service allocated by supply; honest as "share of the ETS budget for service scheduled here", which is what the blurb says |
| **2** one citywide rate × metres | **CONDITIONAL** | Honest as "what a road of this length would cost if the published unit costs held" — but the $1,285 split treatment is an UNSOUND *state* inside it, and the public blurb's own arithmetic compares against the wrong base |
| **3** comparison to the levy | **CONDITIONAL** (roads) / **moot** (fire composite) | The 2026-08-10 panel presents break-even (100% saturation, amber over) that the 2026-07-16 lock forbade the ratio view — an unrecorded amendment; on the public roads rows only set-aside hoods cross 100%, so it is harmless there today |
| **4** communication | **CONDITIONAL** | One arithmetic misstatement in public copy; the strongest known fact against the operating rate (4.65×) is absent from its caption |
| **5** code | **SOUND** | Bases pinned apart by test; fire divisor pre-join; served output back-solves to the file's constants; the copy guard does what it claims and no more |

**Highest level UNSOUND: 1a.** It moots, for the fire composite only: the
`servicecost` Services row (sqrt colour), the "Per service $" Ratio denominator
(its $230 floor and log ramp), and the panel's nested "Roads + fire (incl.
above)" row with its "of which" copy. All of that is `/full/`-only. **The rate
branch (Level 2 onward) is not mooted** — it is a sibling, not a child.

---

## 2. Level 0 — modeled dollars: CONDITIONAL

**Sharpest argument against.** The physical lenses were designed to need *"no
cost model or allocation assumptions"* and none of them has ever been found
wrong. The dollar layer has: the budget pod ~5× low (S94), a shipped rate
contradicted 4.65× by the City's own program (S139), a relayed "lifecycle" rate
that was an operating line (2026-08-03), and two bases 10.8× apart on the same
metres that need layout, caption and a CI guard to keep readers from adding
them. The constants are where this project's errors live, and a map coloured in
dollars is read as spending whatever the label says.

**Why it holds anyway.** Revenue per acre is in dollars; the only way to put
cost beside it on one axis is dollars. The roads rate terms are published City
figures, the derivation is one line, and the blurbs say what the number is and
is not in plain words. That is a defensible model *for roads*. The condition is
that each constant survives challenge — which is exactly what Levels 1 and 2
test, and the fire constant does not.

**Evidence that would change it.** Observed per-neighbourhood spend. The NRP
publishes it for ~24 hoods (`FINDINGS_nrp_reconstruction_cross_check.md`); if
that coverage grows, the model is replaced by money, not improved.

## 3. Level 1a — the fire allocation: UNSOUND as a cost

**What the composite is.** Variance decomposition of `svc_cost_per_acre`
across 406 hoods: **fire term 88.6%, roads term 3.4%** (the rest covariance).
Spearman with `fire_events_per_acre` **0.956**; with `road_m_per_acre` 0.776;
Pearson with fire 0.984. Fire is a median **49.5%** of the dollar level (p10
26%, p90 82%) but nearly all of the *pattern*. The Services row labelled
"Service cost" is a fire-dispatch map.

**What it does to named neighbourhoods.** MCCAULEY: 370 acres, **6,606
dispatches/yr** (17.87/acre), so the composite assigns it **$57,990/acre/yr** —
**$20.8M/yr, 7.5% of the entire Fire Rescue budget**, to one neighbourhood. Its
"Per service $" coverage is **0.5×**; ELMWOOD PARK 0.8×. Those are the only two
developed hoods the ratio puts below 1× (the other 20 are set-aside river
valley/Henday strips). The four hoods that top the composite — MCCAULEY,
DOWNTOWN, BOYLE STREET, CENTRAL MCDOUGALL — receive **19.9% of every kept fire
dispatch in the city** and **22.9% of the medical ones** (13.9% of structure
fires). Their event mix: MCCAULEY **78% medical**, ELMWOOD PARK 78%, DOWNTOWN
66%, CENTRAL MCDOUGALL 65%, BOYLE STREET 63%; citywide **60.6%** (up from the
~57% the docs record). 48 of 408 named hoods generate half of all dispatches.

So the "Revenue vs Modeled Service Cost" ratio identifies the inner-city hoods
with shelters, supportive housing and the highest concentration of medical
emergencies as the land that "doesn't cover its cost." That is a fiscal
verdict on where vulnerable people live, rendered as a land-use map — and the
project's neutral-tone rule excluded *alleys* for embedding far less
interpretation than this.

**Three arguments the authors did not make against themselves.**

1. **Average cost presented as marginal.** The caveat on every surface says the
   budget is *"mostly-fixed … standing capacity … a hood with 2× the events
   does not cost the City 2×"*. The map colours land by exactly that 2×. A
   caveat that contradicts the colour ramp it sits under is not carrying the
   map; 88.6% of the variance says the ramp wins.
2. **The arterials principle, inverted.** Arterials are excluded because
   *"attributing their metres to the neighbourhood they happen to pass through
   would embed a city-wide quantity into a per-neighbourhood metric"*
   (DECISIONS 2026-07-01). Fire halls are the project's own definition of
   shared standing capacity. The same principle excluded one and admitted the
   other.
3. **The 2026-08-03 test, not applied to its own precedent.** The transport
   composite got *no UI row* because *"a map coloured by the sum is a
   bus-service density map"* — transit is 90.8% of the median and **97.6% of
   its variance** (Spearman 0.995). `svc_cost_per_acre` is 88.6% fire variance
   and has a row, a Ratio denominator and a panel row. Same defect, opposite
   treatment, one month apart.

**Salvage.** Fire *demand* (`fire_events_per_acre`) is honest, already
shipped, and the right lens: it says what it measures. The dollar term should
not sit in a column called *cost*. If a fire **cost** per acre is wanted, the
allocation that matches a capacity service is by **coverage** (station
catchment area), not by dispatches — and no such layer exists as open data:
DATA.md §12's levy catchments are 12 greenfield polygons, §8's stations are
points only; a Voronoi over the 31 stations would be an approximation to
label as one.

**Evidence that would change the verdict.** A Fire Rescue cost-driver study
showing operating cost scaling with call volume rather than station count; or
per-station budgets. Neither is published.

## 4. Level 1b — the transit allocation: CONDITIONAL

Same arithmetic (budget ÷ citywide stop-events × hood stop-events;
`transport_cost_ops_per_acre` is 97.6% transit variance). The difference is
what is being allocated: ETS *chooses* to schedule service at those stops, and
drivers, fuel and vehicle-hours scale with that schedule. It is a supply
allocated by supply. The blurb says *"shares out a mostly-fixed budget by where
the service runs"* and *"scheduled service, not ridership"* — that is the
number's actual meaning, stated. **Condition:** it stays a per-term row (the
2026-08-03 no-composite decision holds) and is never called a cost *of the
land*. `/full/`-only today.

## 5. Level 2 — the rate terms: CONDITIONAL

**Sharpest argument against.** A uniform rate makes every roads dollar map a
re-labelled road-metres map (Spearman 1.0 by construction). The colour carries
no information the public roads-supply layer does not; the only new content is
the *level* against the levy, which lives in the panel, not the map. And a rate
that cannot tell a 1960s street from a 2015 one is uninformative for the exact
question a revenue-vs-cost map asks — the TODO already says so.

**Why it holds anyway.** The lifecycle blurb states precisely what the number
is: *"what a road of this length would cost per year if the published unit
costs held everywhere"*, not actual spend, not a funding gap. Two independent
cross-checks (NRP reconstruction; the City's own maintenance program) both say
the two bases are **floors**, in the same direction — the model understates,
which is the safe side for a cost claim. Publishing both bases with the
"never sum" scaffolding is unusual but it is the honest response to the City
publishing figures on two bases.

**The UNSOUND state inside it.** The same $1,285/km is retired as ~5× low in
DATA.md §16 and shipping as the maintenance half of `cost_roads_ops_per_acre`
on the **public root**. S139 wrote this up; the resolution has been Peter's open
call since. This audit adds nothing to the evidence and one thing to the
framing: whichever way it resolves, the *state* — one repo, one number,
retired and shipped — is not one a public methodology can carry, and "documented
as a floor" resolves the number without resolving the contradiction.

**Evidence that would change it.** A per-class published rate; NRP observed
spend across enough hoods to replace `metres × rate`.

## 6. Level 3 — the comparison to the levy: CONDITIONAL (roads), moot (fire)

**The unrecorded amendment.** DECISIONS 2026-07-16 locked the Ratio view as
*"MAGNITUDE, not break-even … the SAME log ramp, NO 1.0 marking … never 'pays
its way'"*. DECISIONS 2026-08-10 built the Services panel with each cost as a
fraction of the hood's levy, **the bar saturating at 100% and turning amber
above it**, and `renderServiceCost`'s own comment says *"the question the panel
answers is whether this hood's levy covers each service."* That is a break-even
presentation. The 08-10 row records the no-total rule at length and does not
mention that it reverses 07-16's framing. The two locks are in tension and the
later one should say so.

**Measured harm today: none on the public root.** Rows where roads lifecycle
exceeds the levy: **9, all set-aside** (river valley strips, MILL WOODS GOLF
COURSE at 55×). Roads operating exceeds the levy in 1 (set-aside). The amber
fires only where the hood is already greyed everywhere else. For the fire
composite the two developed hoods over 100% are MCCAULEY (217%) and ELMWOOD
PARK (118%) — moot under Level 1a.

**"% of levy" for roads is an honest share**, not an invitation to add: the
municipal levy funds roads, and the bar says what fraction of this hood's levy
its roads *would need* at the published rate. Coverage on the fire composite
reads median **5.36×** today (p10 1.8×, p90 15.0×); `SPEC_utilities.md` records
≈5.8× from July data — the blurb wisely quotes no median.

## 7. Level 4 — communication: CONDITIONAL

1. **Arithmetic against the wrong base, public copy.** The "Roads cost"
   (operating) blurb: *"the City separately publishes a lifecycle maintenance
   figure that works out to about two and a half times the $1,285 rate"*. The
   lifecycle O&M figure is $600,000/km ÷ 50 yr = **$12,000/km/yr**. Against
   **$1,285/km** that is **9.3×**; the 2.6× is against the *whole* operating
   rate, **$4,635/km** (maintenance + snow). The sentence names $1,285 and
   states the ratio for $4,635. A reader doing the multiplication gets
   $3,200/km for a City figure that is $12,000/km. `scripts/check_cost_copy.py`
   cannot catch this — it checks literals, not arithmetic, and says so.
2. **The strongest known fact is missing from the caption.** The same blurb
   calls the rate *"the low end of a range"*. The City's own FY2017 `Roadway
   Maintenance` program is **4.65×** the maintenance half (S139). "Low end of a
   range" undersells a known 4.65× contradiction on a public layer.
3. **"Service cost"** as a row label for a column that is 88.6% fire variance
   — moot with 1a, recorded so the label is not reused.
4. The medical share drifted (57% → 60.6% over 2023–25); the copy says "most",
   which stays true. No change needed.

## 8. Level 5 — code: SOUND

`load_unit_costs` validates loudly; `svc_cost_per_acre` is all-or-nothing and
`cost_roads_life_per_acre` sits in its own guard so a fire-less run keeps the
roads column; the fire divisor is the pre-join citywide sum, so numerator and
denominator match; `_two_bases` is pinned apart by test; the served output
back-solves to the file's constants (S114, re-confirmed: $3,142.08/event). The
copy guard checks the thing it says it checks.

### Reproduction

```python
import json, numpy as np
from scipy.stats import spearmanr
P = [f["properties"] for f in json.load(open("web/data/neighbourhood_value_per_acre.geojson"))["features"]]
a = lambda c: np.array([p.get(c) if p.get(c) is not None else np.nan for p in P], float)
s, life, fe, rm, r = a("svc_cost_per_acre"), a("cost_roads_life_per_acre"), a("fire_events_per_acre"), a("road_m_per_acre"), a("revenue_per_acre")
fire = s - life
print(np.nanvar(fire)/np.nanvar(s), np.nanvar(life)/np.nanvar(s))          # 0.886, 0.034
m = ~np.isnan(s)
print(spearmanr(s[m], fe[m])[0], spearmanr(s[m], rm[m])[0])              # 0.956, 0.776
print(np.nanmedian(fire/fe))                                             # 3142.08
print(np.nanmedian(r[m]/s[m]))                                           # 5.36
```

```python
import pandas as pd, sys; sys.path.insert(0, "src"); from load_fire import NOISE_GROUPS
d = pd.read_csv("data/raw/fire_response.csv", usecols=["dispatch_year","event_description","neighbourhood_name"], dtype=str)
d = d[d.dispatch_year.isin(["2023","2024","2025"])]
desc = d.event_description.str.strip().str.upper()
d, desc = d[desc.notna() & ~desc.isin(NOISE_GROUPS) & d.neighbourhood_name.notna()], desc[desc.notna() & ~desc.isin(NOISE_GROUPS) & d.neighbourhood_name.notna()]
hood = d.neighbourhood_name.str.strip().str.upper()
print((desc == "MEDICAL").mean())                                        # 0.606
top4 = hood.isin(["MCCAULEY","DOWNTOWN","BOYLE STREET","CENTRAL MCDOUGALL"])
print(top4.mean(), ((desc=="MEDICAL")&top4).sum()/(desc=="MEDICAL").sum()) # 0.199, 0.229
print((desc[hood=="MCCAULEY"]=="MEDICAL").mean(), (hood=="MCCAULEY").sum()/3) # 0.78, 6606
```

## 9. What this leaves for Peter (all in `TODO.md`)

1. **The fire term's place in a column called cost** (Level 1a). Options, in
   the order the evidence favours: retire `svc_cost_per_acre`, the
   `servicecost` row, the "Per service $" denominator and the panel's nested
   row, keeping `fire_events_per_acre` as the fire lens; or reframe them as a
   *budget-share* surface that is never called cost and never sits under the
   levy; or keep as-is and accept that the caveat does not carry the map.
   `/full/`-only, so no public-root urgency — but `SPEC_development.md` Lens C
   and `SPEC_breakeven.md` both plan to build on this column, and should not
   until this is decided.
2. **The $1,285 split treatment** (Level 2) — already open since S139; this
   audit only adds that the state itself is the problem.
3. **The operating blurb's 2.5×-vs-$1,285 sentence** (Level 4.1) — a copy fix,
   but it touches `web/index.html` copy that `check_cost_copy.py` guards, and
   what it should say depends on item 2.
4. **Record the 07-16 / 08-10 tension** (Level 3) — one DECISIONS line saying
   the panel deliberately shows share-of-levy with a 100% mark, or change the
   panel. No measured harm on public rows today.
