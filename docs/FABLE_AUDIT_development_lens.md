# Fable 5 Brief — Development Lens (A + B) DECISION Audit

Read this in full before opening any code. This is **not** the security/architecture
brief — that is `docs/FABLE_AUDIT_BRIEF.md`, a separate session. This one asks you
to audit the **fundamental decisions** behind the Development lens family (Lens A —
Building Activity, and Lens B — the `Infill` suitability×activity view), **top-down,
highest level first**. Code correctness is the *bottom* of the stack, not the point.

This session uses Fable 5 usage that counts against plan limits at a higher rate than
Opus — don't spend it re-deriving context that is already written down. The reasoning
is in the repo; your job is to *challenge* it, not reconstruct it.

## 0. The one rule that makes this audit different

**Evaluate the decision stack in order, and when a level is unsound, say so and treat
everything beneath it as moot.** Do not spend the session on a z-score edge case if
you've concluded the neighbourhood is the wrong unit of analysis, or that "suitability"
should not be published at all. Each level below is a load-bearing assumption for the
ones under it. For each level, return a one-word verdict — **SOUND**,
**CONDITIONAL** (sound only if a stated caveat holds), or **UNSOUND** — the single
sharpest argument against it, and what evidence would change your verdict. If a level
is UNSOUND, still note (briefly) whether the levels beneath it would be salvageable
under a different top-level choice.

We are not looking for reassurance. Assume the authors are capable and motivated to
believe their own lens works; your value is the argument they didn't make against
themselves. A finding that kills a level is worth more than ten that polish one.

## 1. Ground yourself first (in this order, then stop reading and start judging)

1. `docs/SPEC_development.md` — the whole decision record for both lenses. Read it all.
2. `docs/DECISIONS.md` — the locked one-liners (search `2026-07-12`, `2026-07-13`).
3. `FINDINGS_growth_servicing.md` — the median-age proxy this lens family was built to
   *replace*; its self-stated limitation is the reason Lens A exists.
4. `docs/PARCEL_LEVEL_OPPORTUNITIES.md` — what was deliberately set aside because we
   aggregate to neighbourhood (directly relevant to Level 1 below).
5. `data/DATA.md` §"Building Permits" and §2 (property_info / `far`, `gross_area`).

Then confirm one thing back before proceeding, with the file that proves it:
**every quantity in this lens is aggregated to the ~406-neighbourhood unit before the
reader sees it.** Nothing is shown per-parcel. State that you've confirmed it — it is
the hinge of Level 1.

## 2. The decision stack to audit (highest level first)

### Level 0 — Should this lens family exist, and be *published* as civic data?
The lens makes two claims to the public: (A) "here is where building is happening,"
and (B) "here is where building *should* be happening (suitable) but isn't, and where
it's happening in *less* suitable places." (A) is descriptive; (B) is a normative
judgment about neighbourhoods rendered as a map.
- Is a permit-derived "suitability" verdict a responsible thing to publish about named
  neighbourhoods? The blurb frames the whole view as "relative and exploratory — not a
  target or a recommendation." **Is that disclaimer load-bearing and honest, or a
  fig-leaf over a map that will be read as a recommendation regardless?**
- Does (B) answer a real question, or does it manufacture a "mismatch" that is an
  artifact of how the two ingredients were constructed?

### Level 1 — The unit of analysis: the neighbourhood.
Infill and "room to add" are inherently **parcel-level** phenomena, aggregated here to
~406 neighbourhoods.
- Ecological fallacy / Simpson's paradox: a hood can read "underused, quiet" in
  aggregate while being fully built-out except for one park, one floodplain, or one
  rail yard. Does aggregation create opportunity signals that don't exist on any actual
  parcel? (`docs/PARCEL_LEVEL_OPPORTUNITIES.md` shows the authors know this; judge
  whether the shipped lens over-claims despite it.)
- Is the neighbourhood boundary a defensible denominator for *any* per-acre density
  claim when boundaries include undevelopable land (river valley, ravines, ROWs)?

### Level 2 — Lens A: is issued-permit activity a valid measure of "where building is"?
`new_units_per_acre` = Σ `units_added` (new-construction `work_type` ∩ residential
`building_type`) ÷ boundary acres, over a pinned window (5yr 2021–2025 / 3yr
2023–2025). Also a permits-per-acre sub-metric. See SPEC_development Lens A + `src/load_permits.py`.
- **Event choice:** issued permits, not completions/occupancy. Permits can lapse, get
  cancelled, or precede build by years. Is "issued" the right proxy for "building is
  happening"? (The `occupancy_granted_date` variant was rejected as incomplete — judge
  that.)
- **Filter bias:** residential-only, explicit hand-mapped dictionaries for `work_type`
  and `building_type`, ~60k null-`work_type` rows dropped-and-reported. Does the
  dictionary approach systematically miss or mis-bucket real dwelling activity? Is
  dropping nulls neutral, or does it bias toward well-coded (recent, larger) permits?
- **Normalization:** units per *boundary* acre. A hood that is 70% ravine looks far
  denser per developable acre than per boundary acre. Is the denominator honest?
- **Window:** pinned 5yr/3yr, drift-guarded. Defensible, or arbitrary framing that
  could be cherry-picked?

### Level 3 — Lens B suitability proxy: inverse FAR.
`far` = Σ gross floor area (`Total Gross Area`) ÷ deduped lot area per hood; **low FAR
= "underused = suitable."** ~6.2% of parcels null `gross_area`. Rejected alternatives:
median `year_built`, value/lot-acre (no land/improvement split exists), zoning
headroom. See SPEC_development Lens B, `build_hood_lot_acres` (`src/export_value_grid.py`).
- **The core inversion:** does low built floor-area ratio actually mean "room to add
  housing"? A park, a cemetery, a rail yard, a floodplain, and a surface parking lot
  all have near-zero FAR and zero room for *residential* infill. Is "underused"
  conflated with "not-a-building"?
- Is FAR conflated with **land use** rather than opportunity? (Industrial land is
  structurally low-FAR — this is exactly what forced the Level-5 gate below. Judge
  whether the proxy is salvageable or whether the gate is treating a symptom.)
- Is the deduped-lot / summed-floor-area construction (`FINDINGS_lot_dedupe.md`)
  actually measuring FAR, or something subtly different at multi-unit points?

### Level 4 — The mismatch metric: `z(suitability) − z(activity)`.
Computed live in the browser as `−(z(far) + z(activity))`, both terms standardised over
the same included population, clamped symmetrically at p95 of `|score|`, rendered on a
diverging teal↔orange ramp. See `web/index.html` (search `infillScore`, `infillStats`).
- Is standardising **two heterogeneous quantities** (a dimensionless ratio and a
  per-acre count, both right-skewed) to z-scores and *subtracting* them a legitimate
  operation, or does it impose a false commensurability? What does "one z-unit of FAR
  minus one z-unit of activity" *mean*?
- The metric is **entirely population-relative** — a hood's colour changes if the set
  of included hoods changes. Is that an acceptable property for a published map?
- Does the diverging +/− framing impose a false symmetry between "opportunity" and
  "pressure" — two things that are not opposite ends of one axis?
- Is p95 symmetric clamp defensible, or does it let a few extremes set the whole scale?

### Level 5 — The exclusions, and the asymmetric residential gate (newest decision).
Set-aside hoods are excluded (grey). **New (2026-07-13):** an *asymmetric residential
gate* — a non-residential hood is barred from the **opportunity (teal)** end (positive
score → off-scale grey) but **kept on the pressure (orange) end and in the z-scoring
population.** Rationale + rejected alternative (a median-`year_built` "maturity gate")
are in SPEC_development Lens B and DECISIONS 2026-07-13. A prototype showed the maturity
gate doesn't work because the opportunity pollution is structurally-low-FAR
non-residential land (industrial/fringe, all decades), not new suburbs.
- **Is the asymmetric gate principled, or an ad-hoc patch to make the map look right?**
  It hides a hood on one arm of a diverging scale but not the other, based on land use.
  Defensible design, or an admission that the Level-3/4 metric is measuring the wrong
  thing for a third of the city?
- Keeping non-residential hoods **in the z-population** while hiding them on one arm:
  does that distort the z-scores of the residential hoods that ARE shown? (i.e. the
  mean/std the visible teal colours are measured against includes hoods the reader
  never sees.)
- Grey now means **three** different things (set-aside, no-data, non-residential-
  suppressed). Is that legible, or does one sentinel colour overload the reader?
- Is `is_residential` (a boolean derived upstream) the right cut, and is barring the
  *opportunity* end but not the *pressure* end internally consistent?

### Level 6 — Communication honesty.
Blurb, legend labels, tooltip copy in `web/index.html` (`VIEWS.infill`, `refreshLegend`,
`tooltipFor`).
- Could a reasonable reader take a teal hood as "the city says build here"? Is the
  gap between what the data supports and what the map implies acceptable?
- Do legend/tooltip disclose the population-relative nature, the exclusions, and the
  gross_area/permit coverage gaps?

### Level 7 — Code correctness (only after the above).
Now, and only now: does the code faithfully implement the decisions above? Point to
`src/load_permits.py`, `src/export_value_grid.py::build_hood_lot_acres`,
`src/join_and_calculate.py`, and the `Infill` block + gate in `web/index.html`. The
two verify scripts (`tools/profiling/verify-development.js`, `verify-infill.js`) and
`tests/` encode the intended behaviour — check the tests test the *right* thing, not
just that the code does what the test says.

## 3. Reporting discipline

- Before any finding, point to the file/line/decision it challenges. If you cannot
  verify something this session, say so — do not flag it as confirmed.
- **Do not narrate your reasoning process into the output.** Report the verdict, the
  argument, and the evidence — not a transcript of how you got there. (This also avoids
  tripping Fable's reasoning-extraction classifier, which can silently reroute the
  session to Opus mid-task.)
- No subagents — single session.
- Do **not** edit `docs/SPEC_development.md` or `docs/DECISIONS.md`; those are the
  record of what was decided. Log findings; propose changes; don't make them. If a
  decision should be reopened, say which DECISIONS line and why.
- Pause and ask only for a judgment call the project owner alone can make (e.g. "should
  suitability be published at all"). Don't end on a vague "let me know."

## 4. Before this session ends

Run `/handoff`. The handoff must include:
- A verdict line per level (0–7): SOUND / CONDITIONAL / UNSOUND + the one sharpest argument.
- The highest level you found UNSOUND, if any, and what it moots beneath it.
- Any decision you recommend reopening, by DECISIONS.md date/line.
- Anything flagged but not verifiable this session, so it isn't lost.
