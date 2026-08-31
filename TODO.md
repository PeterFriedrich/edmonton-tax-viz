# TODO — living backlog

This is the **authoritative list of what's left**, edited in place as items open
and close. It holds only **non-derivable** work: things not yet started, and open
decisions. For mechanical state (branch, commits, test count, what files exist),
check `git` / `pytest` directly — do not restate it here, it only goes stale.

Session summaries (`session-summary/`) are dated *narratives* of what happened and
why. This file owns *what's left*. When they disagree, this file wins.

**Closed items live in `docs/TODO_archive.md`, not here** (moved 2026-07-30).
`## Open work` carries only live work; `## Done` keeps a one-line entry for every
closed item, so **the *never redo a closed item without asking* rule still works
by grepping `## Done`** — the reasoning is one hop away in the archive. This file
is read at the start of every session, so it should hold what is still true, not
the whole history. Keep it that way: when an item closes, move its body to the
archive and leave a `## Done` line.

_Last reconciled: 2026-07-31 (S80 — **the temporal + change lenses are PUBLIC**
(#121, merged + deployed) and **the verify suite is GREEN for the first time on
record: 26 scripts, 0 failures** (#122). Three things closed by *measurement
rather than building*: mobile chrome step 3 was not reproducible; the
45-grey-hoods "blocker" had shipped in S79; and all three verify failures were
stale TEST expectations, not app bugs. Also found and fixed a **data-loss bug in
`tools/todo_archive.py`** — it OVERWROTE the archive instead of appending, and
had destroyed 747 lines of S79 history before it was caught.)_

_Last reconciled: 2026-08-01 (S83 — the touch readout regression is closed: the
peek card now carries **each lens's full rows**, not just its headline, and
Money's readout is split so revenue facts stop printing under the Value map.
**Later the same day: phase 1 of those two numbers is BUILT** — `revenue_by_zone`
ships `revenue_share_city` + 10 `rev_frac_*` columns, and the zoning source
decision reversed on measurement (polygons, not the per-property field). **The
`▶` is now phase 2, the UI.** Original note: the `▶` moved to the two new
numbers Peter asked for (% of city revenue,
top 3 revenue by zone) — both need new columns, so they are proposed rather than
built, and the bottom-sheet decision is demoted (not closed) behind them.
**(That bottom-sheet decision is now CLOSED — refused 2026-08-04, no bottom
sheet; `docs/TODO_archive.md`.)**
Also removed a duplicated preamble block left in this file by the
`todo_archive.py` banner bug fixed in S82.)_

_Last reconciled: 2026-08-07 (S101 — reconciliation pass only, nothing built.
**The `## Done` line and archive entry for West Meadowlark still held the FIRST,
later-inverted answer** ("one new $247.8M parcel"), with no mention of the
renumbering or that the map had been understating the hood — so the settled
record disagreed with the open item that superseded it. Both corrected. Also
fixed a **live contradiction between two open items**: the DATA VINTAGE item
recommended `--geojson-out /tmp/x.geojson` as the safe local-run path while the
item directly above it exists to say that is wrong. And added the
roll-continuity-as-second-guard question, which existed only in a session
summary.)_

_Last reconciled: 2026-08-15 (S108 — **two stale BLOCKERS fell in one session,
and both had parked real work for days.** The open-data request's ASSET
paragraph was unverified because the Alberta manual "returned HTTP 520" — it was
transient, and reading it verified the claim *more strongly* than the draft dared
assert (a Tax Code separating `T` from `E`, a Tax Exemption Code mandatory for
every property *including taxable* ones, and Appendix G naming our exact hospital
and university parcels by MGA section). The break-even lens's first task was
recorded as needing a laptop because "edmonton.ca is unreachable from the Oracle
box" — true of `www.`, **false of `budget.edmonton.ca`**, which returns HTTP 200;
Task 2 then executed here in minutes. ⚠️ **A stale blocker is worse than a stale
bug: nobody reproduces it, because its whole claim is that trying is pointless.
Test the exact host, never the domain, and re-test 5xx before recording it as an
environmental fact.** Nothing was built this session — it was all measurement and
docs.)_

_Last reconciled: 2026-08-16 (S109 — **the session's lesson is that a threshold
which is right for words can be wrong for geometry.** The institutional band
selected hoods by ≥25% institutional SHARE and used that one number for both the
caveat and the outlined range. Share is relative, so it caught hoods where the
share is high and the dollars trivial: RIVER VALLEY CAMERON is 49% institutional
and moves **0 rank places and 0.02 of the colour ramp**. Split into two tiers —
share decides the words, movement on the lens's own ramp decides the geometry.
⚠️ **And the obvious version of "worst drop" was wrong**: SPRUCE AVENUE has the
city's second-largest dollar drop ($30,310/acre) and moves **12 rank places**,
while EDMONTON NORTHLANDS drops fewer dollars and swings **0.62** — measure on
the encoding the reader reads, never in the underlying units. ⚠️ **A second
lesson, from Peter catching it:** the translucent-prism change was justified by
measuring that translucency was UNUSED on Money, without checking whether it was
unused ON PURPOSE — `docs/UI.md` said "always opaque", and the known
depth-ordering quirk it flags was not tested until asked. **Measuring the current
state is not the same as checking the intent.**)_

_Last reconciled: 2026-08-18 (S111 — **three hover fixes, and each one's real
defect was worse than the report**. The revenue sparkline had not "come back":
`git log -S` shows one call site, never removed — 2026-08-01 gave the revenue
cuts a different panel and rewrote the invite's WORDING while leaving the chart,
so the teaser kept promising a chart the click no longer opened. The band prisms
were not merely unhoverable: unpickable geometry over a flattened, transparent
footprint fell through to **whoever stood behind it**, so the tooltip named the
WRONG hood — invisible to any flat overhead check, because at pitch 0 the
transparent footprint picks correctly. And the fix's own no-primacy refusal
(`autoHighlight: false`) silently removed hover CONFIRMATION: 0 pixels moved.
⚠️ **A principled refusal to draw something still has to be checked against the
affordance it removes.** Two new open items came out of it: Services' hover
teases a chart its panel does not open (same defect, blocked on invite copy),
and ratio/uses prisms still pick the hood behind them (blocked on an opacity
call). Also corrected `CONTROLS_MATRIX.md`, which had claimed for six days that
Services carries no sparkline — measured, it does.)_

## Open work



- [ ] **OUTREACH TRACKER — five data issues found, ZERO sent. Every one is
  Peter's call.** ⚠️ **`docs/DATA_ISSUES.md` "Status at a glance" is
  AUTHORITATIVE** — this is a one-line mirror so the count is visible from the
  file that gets read every session. If the two disagree, that file is right and
  this is stale.
  - Channel: **`opendata@edmonton.ca`** (portal footer, read 2026-08-25).
    Assessment & Taxation is the *escalation*, not the first stop.

  | # | issue | blocked on |
  |---|---|---|
  | 1 | `Period of Coverage` names the wrong year | **report text** — evidence is published |
  | 3 | `qi6a-xuwt` drops 2,448 accounts | **report text** — evidence is published; see the detailed item below |
  | 4 | no per-parcel exemption status | **nothing — the draft is written**, `docs/DRAFT_open_data_request_exemption_status.md` |
  | 5 | 3 of 5 school boards absent | **report text** — evidence is published 2026-08-29 |

  - ⚠️ **Every sendable issue now has published notebook evidence** (issue 5's
    landed 2026-08-29). **The only remaining blocker on all four is REPORT
    TEXT** — there is no measurement left to do.
  - **Issue 4 is the only one that could go today.** ⚠️ **Do not put the
    $125.4M figure in it** — that asserts an exemption status no public source
    states.
  - **1 and 3 are one email's work each** now that both pages are live and
    linkable; 1 is the cheapest of all five (a single field edit on their end)
    and has never had a draft.
  - **Issue 2 is not outreach** — it is ours, caused by issue 1, and needs a
    decision rather than a message (its own item below).
  - ⚠️ **Detailed context lives in the two long items further down** (the
    `qi6a-xuwt` bug report, and the open-data request). **Do not duplicate their
    content here** — this item exists to make "zero sent" impossible to miss,
    which is exactly how the `qi6a-xuwt` report went invisible for six days
    inside a closed parent.

- [ ] **ACTIVE — how many properties are silently absent from the published
  current roll? One case is proven; the population is a guess.** Full context:
  `docs/DATA_ISSUES.md` "Possible issues" §A. Promoted to active work
  2026-08-26.
  - **The proven case:** Misericordia Community Hospital, continuously assessed
    2012–2025 as `10095840` (~$200–260M, WEST MEADOWLARK PARK), renumbered to
    `11495573`, **absent from `q7d6-ambg` until 2026-08-03**. The map understated
    that neighbourhood by **~$250M** for the duration, and nothing flagged it.
  - **The unproven part:** `tools/audit_roll_continuity.py` (re-run 2026-08-30 vs
    historical 2024) finds **1,457 of 426,913 parcels — 0.34%, $1.07B** with no
    current match, by POSITION (all three identifiers churn, so none can match).
  - ⚠️ **THIS REPLACES 1,534 / $1.62B, re-measured 2026-08-30.** Of 1,578
    position-unmatched parcels, **121 ($592M — 35.6% of the value) are still on
    the roll under the same account number**, recentroided past the 5 m
    tolerance. **The three largest cases the backlog named for three weeks were
    never missing.** Detail + the do-not-widen-the-tolerance warning are on the
    long item further down; don't re-derive them here.
  - ⚠️ **Those 1,457 are candidates, NOT verdicts, and an upper bound.**
    Demolitions, subdivisions and consolidations are indistinguishable from a
    dropout from the outside. **The whole job is separating them** — that is what
    makes this unreportable today, not the measurement.
  - ⚠️ **Do NOT treat identifier churn as the defect.** Renumbering runs
    0.15%–0.37%/yr routinely; `data/DATA.md` states outright that a vanished
    account number is not by itself a finding. The defect is a property absent
    from the roll **while still being assessed**.
  - **Why it is worth the work:** it is the same dataset as `DATA_ISSUES.md` §1
    (the coverage-year mislabel), so a confirmed result could ride along in that
    report instead of needing its own. And it is a **live understatement of the
    map**, unlike every other row in that file.
  - **Done looks like:** a standalone notebook in the house pattern — live
    sources only, figures recomputed at run time, invariants asserted, rendered
    to `web/notebooks/` and added to that folder's hand-written `index.html`.
    ✅ The re-measure this used to ask for is **done (2026-08-30)** and the
    per-parcel baseline is committed at
    `data/roll_continuity_candidates_2026-08-30.csv`. ⚠️ **What is still missing
    is the transient/permanent split** — that needs one more observation diffed
    against that file, and it is the only thing that would make a notebook worth
    writing. A notebook on today's figures would publish an upper bound.

- [ ] **PETER'S CALL — the amenity bands are FIXED at 600 m / 800 m
  (`AMENITY_BANDS` in `web/index.html`).** Built and live behind the weekly
  refresh 2026-08-23; the filter works, the numbers in it are conventions.
  ⚠️ **The control is INFILL-ONLY as of 2026-08-26** — built in Glass, extended
  to Infill 2026-08-25, and the Glass copy removed on Peter's call
  (`DECISIONS.md` 2026-08-26). One place to change now, not two.
  - **What a change would cost:** the band value is repeated in each row's
    tooltip copy, so `AMENITY_BANDS` and the two `title=` strings move together
    (the code comment says so).
  - **Undecided:** whether the LRT band should follow the activity window
    picker — the 3yr kernel wants 800 m where the 5yr wants 600 m. A band that
    moves under the reader needs a reason better than symmetry.
  - **Not urgent.** 600 m is the TOD walkshed convention and 800 m the usual
    school-walk figure; both are defensible as they stand.
  - ⚠️ **Do NOT fold distance into the Infill score** without deliberately
    reopening `DECISIONS.md` 2026-08-22 — proximity is a desirability input, and
    a weighted term nothing can falsify is exactly what that decision refused.
    The Infill highlight grid is a filter overlay, not a step toward this.

- [ ] **PETER'S CALL — the road service life is 50 years and figures in public
  circulation use 25.** Both readings sit on the SAME City page we
  already cite (`city_unit_costs.json` → `roadway_om_renewal.source`,
  "Development Impact on Infrastructure"), which publishes the life as *"usually
  25, extended to 50 with proper maintenance"*. Your call 2026-07-15 took 50.
  - ⚠️ **This is a denominator choice, NOT a data discrepancy** — same $600,000/km
    O&M numerator either way. Do not "reconcile" it by changing the value.
  - **What the choice is worth:** the O&M half is **$12,000/km/yr** at 50 yr vs
    **$24,000/km/yr** at 25 — exactly 2×. The full lifecycle rate the site
    actually ships is **$50,000/km/yr**; at 25 yr it would be **$100,000/km/yr**
    (already recorded as `roadway_om_renewal.sensitivity`).
  - **Why 50 still looks right:** the independent cross-check — the same page's
    ~3%/yr set-aside rule on $1.5M/km ≈ **$45,000/km/yr** — corroborates the
    50-year $50,000, not the 25-year reading.
  - **The decision is only whether the methodology note should SAY SO.** Right now
    nothing in the UI or `DATA.md` explains why a reader who has met the 25-year
    figure elsewhere sees half of it here. Verified 2026-08-20 against served
    output, not config (least-squares back-solve on
    `neighbourhood_value_per_acre.geojson`: road $50.0001/m/yr, fire
    $3,142/event, 404 hoods).
  - ⚠️ **The secondary write-up that carries these figures is NOT a citable
    source and must not be named** in `DATA.md`, methodology notes, UI copy, or
    commits — it publishes them with no footnote. We cite the City page
    directly; that we independently hold the same numbers is a confidence
    signal, not a citation. An accompanying *"30% of road users are not
    Edmonton taxpayers"* claim is traceable to nothing in our reference list and
    must not be repeated even informally.

- [ ] **T8 FOLLOW-UPS — the three unchecked category sets were AUDITED 2026-08-30
  and none carries the 2026-08-18 defect.** Two follow-ups survive; the sweep
  itself is done (`docs/AUDIT_LEDGER.md` 2026-08-30, verdicts + measurements).
  - ✅ **`load_zoning` (area numerator, highest risk) — PASS.** `frac_other` and
    `rev_frac_other` are **0.0000 across all 406 hoods**: every zone code in the
    served `zoning.geojson` classifies, so nothing lands in the unmatched bucket.
  - ✅ **`load_water.HOUSEHOLD_CLASSES` — PASS.** Vocabulary fully enumerated;
    the only household-like class excluded is `FARMLAND` (512 parcels, 0.12%),
    consistent with the residential-only lock (2026-07-06) and logged out-of-scope.
  - ⚠️ **`load_temporal.COMMERCIAL_CLASSES` — WARN, and it is FORCED.** It tests
    `Assessment Class 1` only, but a parcel carries up to three classes: 1,094
    parcels / **$9.06B** have a class 2. Effect is bounded and nearly
    self-cancelling citywide (**−0.50%**, 22.10% vs 22.21% apportioned) but not
    per hood — **max 6.5 pp, 23 hoods >1 pp, 3 hoods >5 pp** (worst: EDMONTON
    SOUTH CENTRAL EAST −6.54, U OF A FARM +6.33). ⚠️ **Do NOT "fix" it by
    apportioning the live half:** `qi6a-xuwt` publishes `mill_class_1` only, no
    class 2/3, so the archive half CANNOT be apportioned and doing one side
    alone would break splice consistency — a worse error than the one it fixes.
    - ✅ **DOCUMENTED 2026-08-30** — `docs/SPEC_temporal.md` §3 carries the cut,
      the per-hood cost and why apportioning one half is worse than the error it
      removes; locked in `DECISIONS.md` the same day. **Nothing is open here —
      do not reopen it as a code change.**
  - ✅ **CLOSED 2026-08-31 — the `other`-in-`frac_nonres` contradiction is gone,
    resolved by DELETING the column.** Nothing consumed `frac_nonres` (it never
    reached the served GeoJSON), so the contradiction had no consumer, only a
    trap. ⚠️ **Measuring the exposure changed the fix:** the served path was
    already honest — `frac_other` renders as "Unclassified" grey. The real
    weakness was `_categorize` only **warning**, which a weekly CI refresh
    swallows; the monthly digest now reports it
    (`vintage_report.check_unclassified_zoning`) rather than failing the
    pipeline. `DECISIONS.md` 2026-08-31. **Nothing is open here.**
  - ⚠️ **METHOD, and it cost a wrong number in this very run:** a parcel-level
    cross-tab on `Property_Info.zoning` said `other` held **$36.8B**. It does
    not — that column's vocabulary is not the one the metric uses
    (`zoning.geojson`). **Audit the actual numerator, never a proxy for it.**
  - **Already settled, do not redo:** `RESIDENTIAL_BUILDING_TYPES` is CLEAR
    (its `units_added` numerator is self-checking — 8 of 25,146 permits carry 0
    units); `export_budget_ranked.py`'s `SERVICE_CATEGORIES` is hardened by
    derivation (`DECISIONS.md` 2026-08-16).
  - ⚠️ **Rank by NUMERATOR, not by how wrong the names look.** A count or
    value-sum over an enumerated category has no self-check — every member
    counts for its full weight whatever it is. A quantity numerator limits the
    damage on its own.
  - Full reasoning: `docs/DATA_INTEGRITY.md` T8, `docs/AUDIT_LEDGER.md`
    2026-08-18 and 2026-08-30, `docs/DECISIONS.md` 2026-08-18.

- [ ] **PETER'S CALL — should Industrial go PUBLIC now that it is grid-capable?**
  `docs/DECISIONS.md` 2026-07-23 tagged the Industrial `#devmetric` `/full/`-only
  with one stated reason: *it's choropleth-only, so in public it would leave the
  new 3-way Detail selector with dead options*. ⚠️ **That reason expired
  2026-08-18** — Industrial now has its own 100 m cells, so it would leave no
  dead option. The tag was NOT changed; it is simply now unargued.
  - **What it would cost:** one `BUILD`-flag guard removed (`web/index.html`,
    the `state.hasIndPermits && FULL_BUILD` branch in `syncDevControls`) plus
    the public build's verify expectations.
  - ⚠️ **The public build has no other dollar-valued layer whose numbers are a
    DECLARED ESTIMATE.** The blurb discloses it, but a public reader is likelier
    to read "construction value" as money actually spent than a specialist is —
    weigh that, not just the control-surface tidiness.
  - Full reasoning + measurements: `docs/SPEC_industrial.md` A3 amendment,
    `docs/DECISIONS.md` 2026-08-18 (three rows), `docs/CONTROLS_MATRIX.md` §7.

- [ ] **THE RATIO AND USES PRISMS STILL PICK THE HOOD BEHIND THEM — same defect
  as the band prisms (fixed 2026-08-17), but the fix needs a call on OPACITY
  first.** Measured at pitch 55 over the U of A: hovering up a `ratio-extrusion`
  ghost prism returns `hood-hover :: RIVER VALLEY VICTORIA` / `WÎHKWÊNTÔWIN` —
  the flat hood layer beneath, not the prism the cursor is on. Uses' optional
  residential prisms are the same shape of problem.
  - **Why it was not fixed with the bands:** both layers ride
    `state.prismOpacity` (ratio's default is the 5% *ghost*; the slider reaches
    0). ⚠️ **A pickable prism at opacity 0 hijacks hovers over what looks like
    empty air** — the Services comment already names this trap ("an opacity-0
    layer would still tessellate, draw, pick, and highlight").
  - **The question is Peter's:** should a ghost prism own the hover at all? On
    `ratio` the ROADS are the subject and the prisms are context, so picking the
    prism may be the wrong answer even when it works. Options: always pickable;
    pickable only above some opacity; leave as is.
  - The band fix needs none of this — those prisms have no opacity control and
    the hood beneath them is deliberately blank.
  - Precedent + measurements: `docs/SPEC_revenue.md` "The banded prism is its own
    hover target", `docs/DECISIONS.md` 2026-08-17.

- [ ] **SERVICES' HOVER STILL TEASES A CHART ITS PANEL DOES NOT OPEN — the same
  defect fixed on the revenue cuts 2026-08-16, left live because the replacement
  copy is Peter's call.** In Services (with the cost columns shipped) the hover
  plots the **assessment-share sparkline** and says **`click to pin`**, while the
  click opens the **cost-against-revenue panel** (`servicePanelFor`, 2026-08-10).
  Measured, not inferred: `hoodPanelLens()` is `!serviceLens() || state.hasSvcCost`,
  so the teaser is appended there like anywhere else.
  - ⚠️ **`docs/CONTROLS_MATRIX.md` asserted the OPPOSITE** ("the sparkline is
    not [offered in Services]") from 2026-08-10 until this was measured on
    2026-08-16. The cell is corrected; the point is that the claim sat unchecked
    for six days because nobody hovered a Services hood.
  - **The fix is one predicate** — the revenue branch in `tooltipFor` already
    demonstrates it; Services needs `servicePanelFor(p)` treated the same way.
  - **What is NOT decided is the invite's wording.** The revenue cuts say
    `click for the revenue mix`; Services would need its own line (`click for the
    cost breakdown`?), and naming a "cost" in one phrase brushes the locked rule
    that ⚠️ **there is no single cost number and there cannot be** — two bases,
    ~10.8× apart, deliberately not summed (`data/DATA.md` §13, `SPEC_services.md`).
    A hint that implies one total would be the same class of error as the chart.
  - Precedent + full reasoning: `docs/DECISIONS.md` 2026-08-16 (the sparkline
    row), `docs/SPEC_temporal.md` §2 (the amended row).

- [ ] **The citywide budget panel is EXPERIMENTAL and full-build-only — decide
  whether it stays, and on what terms.** Built 2026-08-16 (`#budget`,
  `scripts/export_budget_ranked.py`, `web/data/budget_ranked.json`,
  `verify-budget-panel.js`, 26 checks). It ranks the FY2026 approved operating
  budget by branch: 43 service branches, then 5 that deliver no service.
  - **Peter's call, three separable questions:** does it stay at all; does it
    leave `/full/`; and does it get a phone form. Today it is **desktop-only by
    decision** — a 400px readout in a ≤390px column, and the slot it borrows
    (`#millrates`) re-parents into `#title` on a phone, so a phone form is a
    design question, not a width tweak.
  - ⚠️ **It is NOT a lens and must not be made one** — citywide totals, no
    neighbourhood dimension, nothing to draw. `DECISIONS.md` 2026-08-16.
  - ⚠️ **Its data does NOT ride the weekly refresh** and must not be wired into
    it: an *approved* budget moves ~annually (`rowsUpdatedAt` 2026-06-05).
    Re-run the script by hand after a Council budget or adjustment. The panel
    prints the SOURCE vintage, so a stale file is visible rather than silent.
  - ⚠️ **`deploy.yml` excludes `web/data/**` from deploy triggers**, so a
    regenerated JSON alone will NOT deploy — it needs a `web/**` code commit to
    carry it, or a manual run.
  - **Companion available and not built:** `m84q-ghmu` ("Approved Operating
    Budget - Revenues", 1,414 rows, same 8 columns) is the "where the money
    comes from" side. `data/DATA.md` §17's *"there is no revenue side here"* is
    true of the expense feed only. ⚠️ Worth weighing against item ▶ below —
    the revenue split (tax-funded vs fee-funded) is close to what
    `SPEC_breakeven.md` §8.7 is choosing between.

- [ ] **`change` does not carry the institutional treatment.** The consequence
  tier shipped 2026-08-15 on Money's prism mode and the Lab; `glass` followed
  2026-08-19 (`inst_frac` + azure cell bands, `DECISIONS.md`), leaving `change`
  as the one Money mode where the same neighbourhood is outlined-and-uncertain
  on one mode of a view and confident on another.
  - ⚠️ **THIS ITEM SAID `glass` WAS "BLOCKED ON DATA" AND IT NEVER WAS** — the
    cell-level share was one `groupby` off a join `revenue_by_zone` was already
    doing and discarding. The claim sat here unchecked from 2026-08-15 to
    2026-08-19 and would have kept deferring the work. **Re-measure a stated
    blocker before believing it**; that is now twice this file has been wrong
    about one.
  - `change` is share-of-base movement over time, a different quantity again —
    it may need its own answer rather than this one. ⚠️ **Do not assume it is
    blocked either.** Check what the change columns are derived from first.
  - ⚠️ **Re-measure before building.** The 6-hood set is `revenue_per_acre` on
    today's refresh; it moves with the roll.
  - ⚠️ **`value_per_acre` is NOT a candidate and never will be** — exemption
    changes whether a levy is collected, not what a parcel is assessed at.
    Don't "finish the job" by adding a `value_frac_inst`.
  - Full reasoning, both thresholds and the colour measurement:
    `docs/SPEC_revenue.md` "The consequence tier"; `docs/DECISIONS.md`
    2026-08-15 (the second entry, which amends the 2026-08-12 band decision).

- [ ] **BUG REPORT to Edmonton Open Data — the `qi6a-xuwt` 2024/25 dropout.
  Gated on Peter reviewing the notebook by hand; everything else is done.**
  ⚠️ **Re-promoted 2026-08-06 from `docs/TODO_archive.md`, where it had been
  invisible since 2026-07-31** — it was a sub-item of the temporal-graph item,
  which closed and took this, still unchecked, into the archive with it. The
  archive's own header says *"Nothing here is a to-do"*, so nobody would have
  looked. `tools/todo_archive.py` now refuses to archive a closed parent with
  unchecked children (same date). Nothing about the finding changed while it sat
  there.
  - ▶▶ **THE ARTIFACT IS NOW RUN, RENDERED AND PUBLISHED (2026-08-26).**
    `notebooks/standalone/historical_2024_gap.py` / `.ipynb`, served at
    **`/notebooks/historical-2024-gap.html`**. It supersedes
    `notebooks/exploration/03_historical_roll_gap.ipynb` (still there, outputs
    still cleared — **do not send that one**). Standalone: live API only,
    imports nothing from `src/`, every figure computed at run time, 6/6
    invariants asserted, ~4 min cold. **Peter can now read the rendered page
    instead of driving a notebook**, which is what was declined in the form
    offered on 2026-08-07.
  - ⚠️ **FIGURES REFRESHED — re-measured live 2026-08-26, quote these.** The
    account counts are unchanged from 2026-07-28 (**2,448** cumulative, **188**
    neighbourhoods, Downtown **1,292**), which also proves the dataset has NOT
    been corrected. The **value and shares moved** because the control is the
    current roll and the roll rolled to 2026: **$3.008B** (was $2.93B) and
    Downtown **48.4%** of that value (was 53%). Take the figures off the page,
    not from this list.
  - **Two things the run added beyond the old notebook.** (1) All 14 years, both
    detectors, so "11 of 13 testable years are clean" is shown rather than
    asserted — and the self-audit/current-roll disagreement is **464×**, which
    is the single most useful sentence for the City. (2) The loss is
    **building-shaped**: 2,448 accounts at **272 addresses**, **29 of which lose
    every account**; largest are 309 and 261 units at 10310 / 10360 102 ST NW.
  - **Incidental second finding, in the same dataset**: one Downtown address is
    published under three spellings (`102 STREET` / `102 SSTREET` /
    `102 STSREET`), so that building loses **315**, not 309. Cheap for them to
    fix; cut it if it muddies the report.
  - ⚠️ **NEVER the earlier inferred "~8,000"** — that was read off row counts of
    different vintages and most of that gap is new construction.
  - **Cite dataset IDs + the SoQL, not prose:** `qi6a-xuwt` (Historical) and
    `q7d6-ambg` (Current Calendar Year). The notebook prints both. City data
    staff will want exact resource IDs.
  - ⚠️ **LEAVE THE CAUSE UNSTATED.** Describe the symptom — whole multi-unit
    buildings absent together, citywide — and let the City diagnose. No
    speculation about leasehold/condo handling or ETL join logic, however
    tempting the address clustering makes it.
  - **The shipped site is UNAFFECTED** (built from `q7d6-ambg`, the complete
    roll). This is a good-citizen report, not a fix we need. Full evidence:
    `data/DATA.md` §0, `docs/SPEC_temporal.md` §0.1, `docs/AUDIT_LEDGER.md`
    (2026-07-28 row).

- [ ] **The Services panel grouping was never checked on a phone.** Shipped
  2026-08-02 (PR #145). It added 2 group captions + 1 row, so the panel grew by
  3 lines of shared DOM — and `CONTROLS_MATRIX.md` records that grouping drives
  desktop AND mobile. Verified at 1280x800 and 1440x900 only.
  - ⚠️ **A SECOND, LARGER thing now needs the same check: the Services HOOD
    PANEL** (built 2026-08-10, `SPEC_services.md` "Hood panel"). It is up to 4
    bar rows + 2 basis captions + a 4-line note, and the bar row is a **3-column
    flex** (82px label / flexible track / 40px percentage) — the first control in
    this lens whose layout can be squeezed rather than merely stacked. Verified
    at 1400x900 only. ⚠️ Its narrow-width failure mode is **not overflow**: the
    track collapses toward zero width while the row still fits, so a width probe
    that only asks "does it overflow" will pass on a panel whose bars have
    stopped saying anything. Measure the TRACK, not the row.
  - ~~A probe at 390/360/320 px returned **all zeros**~~ — **the zeros were the
    probe's fault, resolved 2026-08-03.** `#optpanel` carries `.folded` by
    default at ≤640px, so its rows have no layout box; remove the class first
    and everything measures. (The item already recorded this cause for the
    S74 left-edge work — it just wasn't applied here.)
  - ✅ **NO OVERFLOW, measured 2026-08-03** at 390/360/320 px with
    `hasTouch`/`isMobile`, Services active, the pod **unfolded**, and the panel
    at its **worst case — 10 visible rows and 3 captions**, i.e. after Stage 2
    added a caption and three more rows:

    | width | `#controls` | `#services` h | clearance to `#botleft` |
    |---|---|---|---|
    | 390 | l=8 r=382 | 230 | 235px |
    | 360 | l=8 r=352 | 230 | 206px |
    | 320 | l=8 r=312 | 244 | 178px |

    Nothing clips left, nothing overflows right, nothing falls below the fold.
    Headless Chromium measures text **wider** than the real font stack (quirk
    y), so a no-clip result there errs safe.
  - **STILL NEEDS CONFIRMATION:** real device, actual touch interaction with the
    rows (the probe drives `.click()`, which bypasses `pointer-events` — the
    standing verify-script caveat), and the **folded default** state, which is
    what a phone user actually meets first.
  - Read `docs/MOBILE_USABILITY.md` first; keep the CONFIRMED /
    NEEDS-CONFIRMATION split honest.

- [ ] **▶ THE DENSITY/INCOME CONFOUND — it applies to a lens that is ALREADY
  LIVE, and we cannot currently measure it.** Opened 2026-08-11 from the
  break-even spec review (`docs/SPEC_breakeven.md` §9).
  - **The problem:** a revenue-per-acre gap between two hoods can be an **income
    gap wearing a density costume**. Edmonton's density gradient plausibly
    tracks its income gradient, and nothing in this pipeline separates them.
  - ⚠️ **It bites the deviation lens in `/full/` NOW**, not just future work —
    that lens is *entirely* a statement about who sits above and below the
    citywide average, which is the exact reading the confound corrupts.
  - **No income or demographic data is ingested**, so today this can only be
    disclaimed, not measured. Current mitigation is the standing one: purely
    descriptive framing, never a causal claim (*"infill pays for itself"* is the
    sentence to keep out).
  - [ ] **Peter's call: ingest an income variable to MEASURE it?** ⚠️ Not free
    of hazard — a map pairing neighbourhood income with fiscal performance
    invites exactly the editorial framing this project refuses. **Measuring the
    confound and publishing the variable are separate decisions**, and the
    second one should not ride in on the first.

- [ ] **▶ IS THE TRANSIT COST TERM ALLOCATED BY THE WRONG KIND OF DRIVER?**
  Opened 2026-08-11 (`docs/SPEC_breakeven.md` §2b-i). `cost_transit_ops_per_acre`
  distributes the ETS operating budget by **scheduled stop-events in each hood**
  — but a downtown stop's departures are consumed by people boarding from
  everywhere, so the driver is **network-shared being allocated as if it were
  site-bound**. Matters out of proportion: transit is **90.8% of
  `transport_cost_ops_per_acre`**.
  - ⚠️ **DO NOT "FIX" IT BY DELETING THE TERM.** Two things are already recorded
    against a hasty read: the figure is a **share, not a rate** (annual budget ÷
    mean-weekday count — meaningless as a unit, exact as an allocation), and the
    locked framing is **demand-allocation-of-a-fixed-budget**, defensible when
    published as such (`DECISIONS.md` 2026-08-03).
  - **The narrow question:** is *where service is supplied* an honest proxy for
    *who consumes it* at neighbourhood grain? Supply-side is all the data
    supports — **no stop-level ridership exists**, citywide-monthly only
    (`DECISIONS.md` 2026-07-11) — so the live options are relabel, move to the
    break-even residual while the Services lens keeps it as-is, or leave it and
    state the limit.
  - **Does not block the cost register.** Its own decision.

- [ ] **▶ BREAK-EVEN LENS — STILL NO CODE, BUT THE MEASUREMENT IS DONE.
  `docs/SPEC_breakeven.md`; FOUR decisions in its §8 now block all code (#2
  name, #4 residual, #5 revenue scope, #6 transit).** Opened
  2026-08-11 (Peter: pipelines per cost category, improved one at a time,
  composing into a per-hood break-even that stays in the Lab and might one day
  reach specialists). **§4 Tasks 1 and 2 executed 2026-08-13 (PR #208, merged) —
  §4a holds the result.**
  - ✅ **§8 #1 + #7 SETTLED 2026-08-23 (Peter): OPERATING basis, OPERATING-ONLY
    denominator.** Coverage reads **15.5% ($473M / $3,055.2M), not 12.3%** —
    the earlier $3,846M/12.3% figure used the full tax-supported budget and is
    superseded. `DECISIONS.md` 2026-08-23.
  - ⚠️ **THE NUMBER IS COMPUTABLE TODAY AND WOULD BE WRONG IN A KNOWN
    DIRECTION.** Revenue modelled $2,715M against $473M of cost on the
    operating basis — **15.5% of the City's $3,055.2M operating-only budget**
    — so the lens would report **every hood running a 5.7× surplus**,
    by roughly the same factor everywhere, which is exactly what makes it look
    plausible. **Coverage is therefore the product, not a caveat**, and must be
    computed and printed wherever the number is.
  - ✅ **TASK 1 + TASK 2 DONE 2026-08-13 — the register is measured and the head
    is SHORT.** FY2025 tax-supported (pinned to match `ASSESSMENT_YEAR` and to
    stay inside the 2018–2025 naming era): **$3,855.9M, 656 rows, 144 programs —
    and the top 25 programs are 76.5% of it.** Order: **Police $597.2M (15.5%)**,
    Transit `OPS/ETS - Bus and LRT` $449.1M, Tax-supported Debt Charges $221.0M,
    Fire `CS/FRS - Operations and Training` $208.2M, **Alley Renewal $174.4M**.
    Full table in `SPEC_breakeven.md` §4a. ⚠️ **Parks is NOT its own line** — it
    is bundled with roads inside `OPS/PARS - Infrastructure Operations`.
  - ⚠️ **▶ POLICE IS THE TOP LINE, HAS NO DRIVER, AND IS BIGGER THAN EVERYTHING
    CURRENTLY MODELLED PUT TOGETHER** ($597.2M vs $473M). **Do not reach it by
    working down the ranked list.** Allocating it by any spatial driver produces
    a per-neighbourhood policing-cost map, and **the driver choice would be doing
    the arguing** — a far more charged artifact than a roads-cost map. Its own
    decision, and an editorial one before it is a data one. ⚠️ **"Find better
    data" was checked 2026-08-23 and does not escape this** — EPS's crime
    dataset is real and joinable, but its publisher anonymizes locations
    specifically because per-area comparison is unreliable, so adopting it
    would import a documented bias rather than resolve the gap.
    `docs/ANALYSIS_BACKLOG.md` §14.
  - ✅ **§8.7 SETTLED 2026-08-23 (Peter): OPERATING-ONLY denominator,
    $3,055.2M — coverage reads 15.5%, not 12.3%.** Decided together with §8.1
    (basis) because the two can contradict each other made separately. The
    full-budget denominator would have been the §3 basis-mixing failure sitting
    **in the coverage ratio rather than the composite** — the worse location,
    because §6 puts coverage on screen wherever the number is. `DECISIONS.md`
    2026-08-23, `SPEC_breakeven.md` §0/§8.
    - ⚠️ **CAPITAL IS NOT A SYNONYM FOR UNALLOCATABLE — disclosure debt, not a
      closed question.** `Alley Renewal` **$174.4M** is per-neighbourhood
      infrastructure renewal on the **lifecycle** basis the roads term already
      uses — plausibly the most spatially-allocatable line in the whole budget,
      and a larger register entry than anything shipped except transit. **The
      genuinely hard part is the ~$400M of debt service**, not "capital". Must
      not silently drop out of the register once lifecycle-basis work exists.
  - ⚠️ **THE SILENT KILLER IS BASIS MIXING.** Lifecycle $50/road-m/yr vs
    operating $4.635 — same metres, 10.8× apart. The composite must HARD-ERROR
    across bases, not warn.
  - ⚠️ **The revenue half is not the solid half either** — $2,715M modelled vs
    $2,318M budgeted (17%), the ~$125.4M institutional question is open with
    unknown direction, and levy is not all the revenue funding that budget.
  - ~~Decide the publication gate before the number exists (§8.3).~~ **SETTLED
    2026-08-11** — no separate gate; the Lab is full-build-only and `beta`, so
    the requirement collapses into §6's *coverage renders wherever the number
    does*. ⚠️ **Do not re-open** (`SPEC_breakeven.md` §8.3).
  - ⚠️ **THE FETCH IS NOT LAPTOP-ONLY — that blocker was false and had parked
    this task since 2026-08-04.** `budget.edmonton.ca` returns **HTTP 200 from
    the Oracle box**; only `www.edmonton.ca` is blocked. Corrected in
    `data/DATA.md` §17 and `SPEC_breakeven.md` §4. The three real quirks still
    bite: program names do not survive two re-cuts, every figure is gross
    (`account_type` is `Expenses` only), portal and PDF differ (+1.31% on Parks
    and Roads; 0.26% on the tax-supported total).

- [ ] **THE LAB IS OPEN AS A CONTAINER — one experiment in it, and the only
  thing left is PETER'S CALL on whether it graduates.** The phone check closed
  2026-08-15 (eyes-on, PR #207). Built 2026-08-11 (`DECISIONS.md` ×2 same date;
  `verify-deviation.js`, **59 checks green** as of 2026-08-12). A full-build-only
  top-level `#views` button holding unfinished lenses, currently just the
  deviation lens ("vs peer average"), which re-centres the revenue map on its
  peer group's average **per developed acre** and extrudes the deficit half
  BELOW the ground plane.
  - ⚠️ **9 institutional hoods draw NO PRISM** (15 until 2026-08-15, when share
    stopped deciding the geometry) — replaced by two white outlines, one per
    scenario (levied / exempt), asserting no value. The outline colour is
    **achromatic by rule, not by taste**: amber shipped first and measured
    **ΔE 9.5 against the deficit orange under NORMAL vision** (hard floor 15),
    so the *unknown* hoods read as *below average*. Blue was rejected too — a
    cool hue leans toward the teal surplus pole. Verify pins `R === G === B`,
    not a hex. ⚠️ **The rule is local to this lens** — Money uses azure
    `#2ec4ff` against its near-white sequential peaks.
  - ⚠️ **`exempt` is NOT always the lower end** (EVERGREEN +$87, RIVER VALLEY
    CAMERON +$842); a first verify check assumed it was and was wrong, the code
    was right. **Since 2026-08-15 no inverted band is ever DRAWN, and that is
    structural**: inversion needs the hood to lose less than the average's
    $1,303/acre, so its span is under $1,303 against $21,470/$48,047 clamps —
    Δt < 0.061, never the 0.25 required. Both facts are asserted separately, so
    the inversion cannot quietly disappear from the data.
  - ⚠️ **Read both decisions before touching it.** The sub-lens it ships
    without (rate-adjusted revenue per acre) was refused *on measurement*, not
    on taste, and the numbers to re-supply if anyone asks again are recorded.
    The second decision is why an experiment must keep its own state.
  - **ADDING AN EXPERIMENT IS ONE LINE** in `LAB_EXPERIMENTS` plus its view
    (a branch in `buildViewLayers` / `primaryRow` / `viewTooltip` /
    `refreshLegend` and a `VIEWS` entry). The picker renders from the registry
    and reveals itself at 2+, so the second one costs no chrome work.
    ⚠️ **Give it its OWN state, never Money's** — that is the whole reason the
    container exists, and the failure it prevents is silent.
  - [x] **CHECKED ON A PHONE — Peter, 2026-08-12: "lab on phone is fine."**
    ⚠️ **This is an EYES-ON confirmation on a real device, which is the thing a
    probe could not give us** (the standing caveat: verify scripts drive
    `.click()` and bypass `pointer-events`). It is **not** a measurement — no
    width numbers were captured, so if the `#views` row or the title box grows
    again, this closure does not cover it. The untested axis was **WIDTH**: six
    buttons wrapping at `max-width: 640px`, "Lab" widened by its `beta` tag, and
    a title box that went **217 → 258 → 314px in one day** against Money's 176px.
    Desktop verified at 1440x900 / 1400x900 / 1366x768 / 1280x720 / 1024x768;
    worst `#botleft` clearance 215px at 1280x720, so vertical was never the
    worry. ⚠️ **Still live for the NEXT change:** Development's 442px blurb is
    what collides below 768px tall, so an addition to that blurb needs
    re-measuring rather than assuming, and remove `.folded` from `#optpanel`
    before measuring Options rows or every probe returns zeros (the trap this
    file records three times now).
  - [ ] **Peter's call: does the deviation lens ever leave the Lab? THE CASE
    FOR IT GOT STRONGER 2026-08-12 and the old reason to doubt it is GONE.**
    It was marked `beta` partly because it was rank-identical to the Money map.
    On the developed-acre denominator it is **not**: Spearman 0.900, 242 of 358
    hoods moving >10 rank places. It now carries information Money does not.
    ⚠️ **It also changed what it says** — 21% of hoods below average became
    **63%** — so the question is no longer "is this thin?" but "is this the
    headline?". Still no opinion recorded; `beta` and full-only until Peter
    calls it.

- [ ] **`verify-peek.js` IS FLAKY UNDER PARALLEL LOAD — reproduce before acting on a red.**
  Found 2026-08-12 running the 33-script sweep: it reported
  `touch: panel open via CARD -- another hood peeks, panel closes`. Re-run while
  the sweep was still competing for CPU it failed **differently**
  (`first tap PEEKS, panel stays shut`, `peek=null`); run three times on an idle
  box it passes **3/3 with zero failures**. Two distinct failure modes under load
  and none without it — the touch-interaction timings are the suspect, not the
  app. ⚠️ **Cost about an hour of diagnosis** (a worktree at the pre-change commit
  and a second server on :8778) before the load hypothesis was confirmed, so the
  cheap first move is to re-run it alone.
  - ⚠️ **The sweep HARNESS produced three separate wrong answers the same day**,
    and all three read as green or as a real failure: a grep pattern that matched
    neither of two crash signatures (reporting ~31 crashed scripts as PASSING);
    a `grep -c green` tail that discarded every RED line; and a URL-fallback that
    triggered on `expected string, got undefined` but not on `verify-smoke.js`'s
    `usage:` message, so that script silently ran without its URL and was scored
    RED with an empty reason. **Nearly every verify script REQUIRES a bare URL
    argument** — `verify-deviation.js` is the exception, it defaults its own.
  - Not a blocker, and not the two known-red scripts (`verify-nonres-revenue.js`,
    `verify-revenue-panel.js`), which are separate and still open above.

- [ ] **A TRUE BIKEWAY LIFECYCLE $/m/yr STILL DOES NOT EXIST** — the residue of
  Stage 2, which shipped 2026-08-03 on an **operating** basis instead. All three
  cost terms are maintenance + snow with **no capital replacement**, because the
  figure offered as a lifecycle rate was not one.
  - ⚠️ **Do not re-propose $178/km/yr.** It is an operating-maintenance line.
    Falsified four ways in `DECISIONS.md` 2026-08-03 and recorded in
    `city_unit_costs.json` → `bikeway_ops.rejected_lifecycle_reading`; the
    shortest version is that the same source puts snow clearing on the same
    network at **113× it**.
  - ✅ **THE CAPITAL HALF IS DONE (2026-08-04, on the laptop).** Bike Plan
    Implementation Guide §1.2 **Table 3** → **$452,065/km** blended
    (bands $365k–$790k by urban form), construction-only. Verified rather than
    relayed — every row's implied $/km sits inside its own stated band and the
    $190.8M City-borne subtotal reconciles. Recorded as `bikeway_capital` in
    `city_unit_costs.json`, **deliberately INERT** (nothing reads it; it is $/km
    of asset value, not a rate). **Do not re-hunt this source.**
  - ⚠️ **WHAT IS ACTUALLY BLOCKING: A SERVICE LIFE, AND EDMONTON PUBLISHES
    NONE.** Searched 2026-08-04 across the Development Impact page, both Bike
    Plan PDFs, the 2025 Infrastructure Report, the Infrastructure
    State-and-Condition / Inventory / Tools pages and the 2023 Capital Asset
    Management Audit. The Bike Plan's action **9.6.2(a) is to *"establish"* a
    bikeway asset-management program** — the City says outright it does not have
    one. **This is not a search that was done badly; it is a number that does
    not exist publicly.** Reopening it means a FOIP/direct-contact route, or
    Peter choosing a life by decision the way he chose 50 years for roads.
  - ⚠️ **Two shortcuts around the missing life are already closed off.** (a) The
    sidewalk page's *"amortized for 20 years"* is a **local-improvement levy
    term, not an asset life.** (b) The **~3% set-aside rule does not transfer**
    — at roads' implied 3.33%/yr the allowance is $15,069/km/yr, but measured
    `bikeway_ops` is **$20,278/km/yr, 1.35× the whole allowance** before any
    renewal. Both recorded in `bikeway_capital`.
  - **For scale, if it is ever derived:** across a 20–50 yr life the answer is
    **$29–43/m/yr, i.e. 0.6–0.9× roads' $50** — the result is insensitive to the
    life because the $20.278/m/yr ops floor dominates. Compare the rejected
    reading's **1/281×**. ⚠️ These are illustrative, **not a shipped number**.
  - **Only then** can a lifecycle bikeway term sit beside `svc_cost_per_acre`'s
    lifecycle roads term. Until then the two bases stay separated by the `_ops`
    suffix, and that separation is load-bearing (~10.8× on the same metres).

- [ ] **⚠️ `--geojson-out /tmp/x.geojson` DOES NOT MAKE A LOCAL `main.py` RUN
  SAFE — the DATA VINTAGE item below says it does, and that advice is wrong.**
  The flag redirects only the main GeoJSON. A full run on 2026-08-03 still wrote
  `roads.geojson`, `zoning.geojson`, `value_grid.json`, `dev_grid.json` and
  `temporal.json` into `web/data/` from 2026-07-06 raw data — the exact rollback
  that item exists to prevent. Caught by `git status` immediately after and
  restored from HEAD; **nothing was committed**.
  - **Fix:** give the auxiliary web exports their own out-dir, or one `--out-dir`
    they all honour. Until then the real mitigation is
    **`git checkout -- web/data/` after any local `main.py`**, and the DATA
    VINTAGE item below should say so instead of what it currently says.

- [ ] **DEFERRED TO A LAPTOP — the minimum colour transition on state swaps.**
  Peter, 2026-08-29: *"we may do this on the laptop so I can judge it on local
  host"* — it is a **taste call that needs a real screen**, not a headless one,
  and this box has no way to judge it (three font families, none of the CSS
  stack; screenshots are the only output and they cannot show motion).
  - **Rules are already locked — do not re-derive them.** `docs/TRANSITIONS.md`
    (rules, our controls, the engine's limits) and the `DECISIONS.md` 2026-08-29
    row. This item is the *build*, and only the smallest honest slice of it.
  - **Scope, ~15 lines, one function:** `transitions: { getFillColor: 250 }` on
    `metric-extrusion`, the same on `getColor` for `top-edges` (or the roof
    outlines snap colour while the prisms fade), and a guard computing the
    duration:
    - ramp / `#coloradj` changed with metric+denominator unchanged → 250
    - Revenue ⇄ Residential $ ⇄ Non-res $ → 250
    - **everything else → 0**, i.e. exactly today's hard cut
  - ⚠️ **The bare one-liner is WRONG and looks right** — without the guard it
    also fires on Revenue→**Value**, which `TRANSITIONS.md` §2 rules a
    cross-fade, not a tween.
  - ⚠️ **`prefers-reduced-motion` needs JS here** (`matchMedia`), forcing 0. The
    existing `web/styles.css` block covers CSS only; deck.gl transitions are not
    CSS and would ignore it.
  - **NO height, NO cross-fade, NO view swaps** — height cannot animate at all
    (`TRANSITIONS.md` §5) and cross-fading needs both layer stacks alive, which
    collides on `hood-hover`/`hood-labels`. Keeping to colour is what makes this
    ~15 lines instead of a render-path change.
  - **Cost is measured, and smaller than assumed: CI is UNAFFECTED.**
    `verify-smoke.js` is the only script `refresh.yml` runs and it never clicks
    a control. Exposure is 10 local scripts that click a ramp/metric button,
    concentrated in the 6 `shot-*` screenshot ones — they would need a settle
    wait.

- [ ] **RESIDUAL from the panel/blurb fix (2026-08-02): below ~768px tall,
  Development and Infill have no left column left to give.** The placement fix
  clears the blurb in all ten states at 1440x900 and clears `#botleft` too. At
  1366x768 and 1280x720 the two longest blurbs hit `TEMPORAL_MIN_H` and the
  panel reaches into `#botleft` — Development 2px/50px, Infill **76px/124px**.
  - **No placement rule can fix it, and that is measured, not assumed:** at
    1280x720 Infill's `#title` ends at 499 and `#botleft` starts at 535, so the
    column has **36px** free. The blurb is **479px of a 720px screen**.
  - **The only remaining lever is blurb length** — Development's title box is
    442px and Infill's 479px against a **~179px median** across the other eight
    states. That was an option when this was ruled on and was not the one taken;
    it is now the *only* one that helps here. **Content decision, so it needs
    Peter.**
  - Not obviously worth doing: 1440x900 is clean, and the failure mode is the
    panel overlapping bottom-anchored chrome rather than burying content.

- [ ] **⚠️ DATA VINTAGE: a local `python main.py` REGENERATES THE MAP FROM STALE
  RAW DATA — do not commit the result** (found 2026-08-01). `data/raw/` on the
  Oracle box is from **2026-07-06**; the committed `web/data/*.geojson` is built
  by the `refresh.yml` auto-refresh from data downloaded that day (last:
  **2026-07-27**). Regenerating locally and committing silently ROLLS THE SITE
  BACK — measured: **1,896 pre-existing values changed** across 406 features on a
  run that was only supposed to ADD columns.
  - **What to do instead:** commit pipeline code only and let the weekly refresh
    add the columns, or run `scripts/download_data.py` first if the data really
    should roll. ⚠️ **For local UI work, `--geojson-out /tmp/x.geojson` is NOT
    enough** — corrected 2026-08-07; this line used to recommend it on its own.
    The flag redirects only the main GeoJSON, and a full run still writes
    `roads.geojson`, `zoning.geojson`, `value_grid.json`, `dev_grid.json` and
    `temporal.json` into `web/data/` (measured 2026-08-03 — see the
    `--geojson-out` item above, which exists to say so). **The mitigation that
    actually works is `git checkout -- web/data/` after any local `main.py`.**
  - **Consequence to watch:** phase 2's UI columns are ABSENT from the served
    geojson until the next auto-refresh runs. The UI must degrade cleanly when
    they are missing (the house pattern), or the site breaks in the gap.

- [ ] **▶ `data/DATA.md` §1 "Tax-exempt flag" WAS FALSE — exempt institutional
  land IS on the taxable roll, ~$5.6B of it. CORRECTED 2026-08-07; only sub-item
  (3) is still open.** Opened 2026-08-07.
  The West Meadowlark investigation asked whether its hospital parcel was
  anomalous. **It is not** — and answering that exposed a much larger stale
  premise.
  - ⚠️ **SUPERSEDED FRAMING, 2026-08-07 (later the same day): "is it supposed to
    be taxable?" WAS THE WRONG QUESTION — it always was.** Misericordia has been
    continuously assessed **2012–2025** as account `10095840` (~$200–260M, always
    WEST MEADOWLARK PARK, always COMMERCIAL). It was **renumbered** to
    `11495573` and was simply **absent from the published current roll** during
    the changeover. ⚠️ **So the map UNDERSTATED West Meadowlark before 2026-08-03
    by ~$250M of assessed value / ~$6M/yr — the +130% was the CORRECTION, not
    the defect.** `$4.63M` was the wrong number; `$10.63M` is right. See
    `data/DATA.md` "Tax-exempt flag" and `tools/audit_roll_continuity.py`.
  - **`DATA.md` §1's "Tax-exempt flag" note used to say:** *"tax-exempt institutional land (Legislature, schools,
    hospitals, City property) is **absent from the taxable roll entirely**, not
    flagged or zeroed"*, listing `AJ/PU/UI/UF` as exempt-proxy zones. **Measured
    against the roll, that is wrong.** Every major hospital is on it and was
    already there in the Jul-6 snapshot:

    | account | site | assessed | zone |
    |---|---|---|---|
    | `11495590` | Royal Alexandra (10520 Kingsway) | $273,762,000 | UF |
    | `11495573` | **Misericordia (16940 87 Ave)** — **the ONLY one absent on Jul-6** | $247,780,500 | UF |
    | `11495606` | Grey Nuns (1100 Youville W) | $196,900,000 | UF |
    | `11495587` | Cross Cancer (11560 University) | $68,062,000 | AJ |
    | `11495614` / `11495565` / `9996778` | U of A campus | $577M / $438M / $431M | AJ |

  - **Full spatial join of the roll against `zoning.geojson`: 2,254 parcels on
    AJ/PU/UI/UF zoning carry $5,622,058,000 of assessed value, which our
    pipeline turns into ~$125.4M/yr of modelled levy — 4.6% of the $2.71B
    citywide served total.** Concentrated: UNIVERSITY OF ALBERTA alone is
    $45.5M/yr across 36 parcels, then SPRUCE AVENUE $9.1M, CENTRAL MCDOUGALL
    $8.5M, DOWNTOWN $7.5M.
  - ⚠️ **So West Meadowlark's $6.0M was never the story — it is 5% of a
    pre-existing exposure that has been in every published number all along.**
    The +130% simply moved one hood into a state ~40 others were already in.
  - ⚠️ **What is NOT established, and must not be asserted either way:** being on
    the assessment roll with an assessed value is **not** the same as being
    levied. This dataset publishes assessments and a `Tax Class`; it does not
    state exemption status, and Alberta assesses some exempt property. Our
    pipeline applies mill rates to every record on the roll. **The open question
    is whether that is the right thing to do for these 2,254 parcels** — not
    whether the data is corrupt.
  - ✅ **(1) `DATA.md` CORRECTED 2026-08-07** — the "Tax-exempt flag" note now
    carries the measured split (present: hospitals, U of A campus; absent: the
    Legislature, 0 rows at 10800 97 AVENUE NW) and the per-zone table. The old
    claim is quoted and marked retracted rather than deleted, and the Known
    Quirks bullet that repeated it is fixed.
  - ✅ **(2) THE TWO ARTIFACTS SURVIVE — re-run 2026-08-07, numbers UNCHANGED,
    and this is the useful part.** `tools/audit_exempt_institutional.py`
    *measures* the taxable footprint on institutional zoning and subtracts it,
    rather than assuming there is none — so land that IS taxed is counted as
    taxed and correctly excluded from `exempt_inst_acres`. **The method never
    used the false premise; only the docstring's motivating sentence did.** The
    fresh run reproduces every published figure exactly (U of A: 145 exempt acres
    of 253 institutional, ×2.0 lift, $15.2M/lot-acre, $2.242B on 47 accounts).
    Premise sentences corrected in both files; ⚠️ **both now say DO NOT "fix" the
    method on account of the retraction.** `ANALYSIS_BACKLOG.md` §7's conclusions
    ride on those same numbers and therefore also stand.
  - ⚠️ **(3) OPEN AND IT IS THE ONLY THING LEFT: should the revenue model treat
    AJ/PU/UI/UF differently at all?** We apply mill rates to every record on the
    roll, which produces the ~$125.4M/yr above. Whether the City actually levies
    those parcels is **not answerable from this dataset** — it publishes
    assessments and a `Tax Class`, not exemption status. ⚠️ **This is a
    public-number change and Peter's call, not a cleanup.** Needs an external
    source on exemption status before it is even decidable.
  - ✅ **(4) `docs/FINDINGS_revenue_scale.md` §4–5 RE-CHECKED AND CORRECTED
    2026-08-08 — and it was NOT "narrative, not a computation others cite".**
    This item said so, and ranked it lowest. ⚠️ **It was cited by a
    USER-FACING STRING that had been LIVE on the site**: the revenue-mix panel
    printed *"Tax-exempt land is not on the roll, so it is absent from every
    share above"*, with a code comment pointing at §4-5 as its authority. The
    retracted premise was **published**, not merely written down, and it
    **pointed the wrong way** — it promised an understatement where the model
    may be overstating. Fixed (PR #184, merged, **confirmed live in
    production**: new string present, old string returns 0 hits). §4's
    conclusion SURVIVED its own premise (measured, not assumed — same as
    `audit_exempt_institutional.py`) and both files now warn against "fixing"
    it; §5's direction was inverted. **The lesson worth keeping: "narrative"
    was the wrong triage — nothing had checked whether prose was quoted by
    code.**
  - ✅ **(5) HOW THE $125.4M/yr MUST BE DESCRIBED — locked 2026-08-08.** It is
    a **gross modelled** figure ("if every institutional/public-zoned parcel
    were fully taxable"), **never** "revenue lost" or "foregone". ⚠️ The
    direction of the error is **unknown, not merely unquantified**. Text in
    `data/DATA.md`; `DECISIONS.md` 2026-08-08.
  - ⚠️ **(6) GIPOT IS NOT A USABLE ANCHOR YET — three specific blockers.**
    Offered as the one hard reference point ("$15.7M for 2021-22") and **not
    written in**, because: (a) **the City publishes no dollar figure at all**,
    only a percentage history — the $15.7M is unsourced and secondary
    reporting says only "$15 million per year"; (b) **2021-22 sits inside the
    2020–2024 window when Alberta paid 50%**, so any receipt from it reads
    ~2× low as a tax equivalent (75% in 2019 and 2025, 100% from 2026); (c)
    **GIPOT covers Government of Alberta property** — that universities and
    hospitals fall outside it is *inference*, since the program page
    enumerates no exclusions. All three recorded in `data/DATA.md`. **Drop the
    number in once a primary source exists; do not publish it before.**

- [ ] **OPEN-DATA REQUEST (DRAFTED, NOT SENT): ask Edmonton to publish the
  taxable/exempt liability code on `q7d6-ambg`.** Opened 2026-08-08.
  `docs/DRAFT_open_data_request_exemption_status.md`. **This is the only route
  that resolves the AJ/UF/UI/PU question** — no public per-parcel exemption
  source exists, confirmed.
  - ▶ **SUPPORTING EVIDENCE IS NOW PUBLISHED (2026-08-26)** — a standalone
    notebook demonstrating *why* the request is necessary rather than asserting
    it: `notebooks/standalone/exemption_uncertainty.py` / `.ipynb`, served at
    **`/notebooks/exemption-uncertainty.html`**. It proves the identification
    failure by construction — two **disjoint** sets of apartment properties,
    60 and 68 of them, each reproducing the same $3.49B aggregate to 100.0000%.
    A sum does not determine its terms, so no amount of public data closes this.
    ⚠️ **Still do NOT put the $125.4M in the message** (unchanged); the page
    asserts nothing about any parcel and is safe to link.
  - ⚠️ **One claim in the brief it came from is FALSE and is corrected in the
    draft: Calgary does NOT publish exemption status as open data.** Verified
    against the live schema of Calgary's `4bsw-nn7w` — 22 fields, **no
    exempt/taxable flag**. Calgary discloses it on the **assessment notice**
    only (*"Tax exemption status is noted on your assessment notice"*, verified
    verbatim). Sending the stronger claim would be trivially checkable and
    wrong.
  - ✅ **THE ASSET / LIABILITY-CODE PARAGRAPH IS CONFIRMED — 2026-08-12, read in
    the primary source, and it came back STRONGER than the draft claimed.** The
    HTTP 520 was transient. *2025 Recording and Reporting Information for
    Assessment Audit and Equalized Assessment Manual*, **Ministerial Order No.
    MAG:016/25** (open.alberta.ca dataset `1718-1771`). The liability code's
    seven components include a **Tax Code** already separating `T` taxable from
    `E` *"assessable but exempt from taxation"*, and a **Tax Exemption Code**
    that is *"mandatory in ASSET"* for **every** property *including taxable
    ones* (`NAA`) — so there is no coverage gap to argue about. Appendix G names
    our parcels by statute: `MGA362(1)(d)` university boards of governors,
    `MGA362(1)(e)` hospital boards. Fallback paragraph retired; draft and
    `DECISIONS.md` updated. ⚠️ **It does NOT tell us what Edmonton coded for any
    parcel** — the $125.4M question is untouched, direction still unknown.
  - ✅ **SUBMISSION CHANNEL FOUND — `opendata@edmonton.ca`, 2026-08-25.** Read
    from the live portal itself (`https://data.edmonton.ca/`, the footer nav's
    "Contact Us" → `mailto:opendata@edmonton.ca`) — primary source, not
    inference. This is the right channel of the three that were listed: the ask
    is *publish a field on dataset `q7d6-ambg`*, which is a portal/dataset
    request, not a per-parcel assessment inquiry. **Assessment & Taxation Branch
    is the escalation if Open Data bounces it**, not the first stop.
    ⚠️ **Still NOT SENT — sending is Peter's call** (outward-facing, and it
    speaks for the project).
  - ⚠️ **THE "edmonton.ca IS UNREACHABLE FROM THE ORACLE BOX" BLOCKER WAS A
    MIS-DIAGNOSIS — RETRACTED 2026-08-25.** This bullet used to read: *"No
    submission channel is recorded in the repo, and `edmonton.ca` is
    **unreachable from the Oracle box** (`000` on 2026-08-12 …). Needs a machine
    that can reach `edmonton.ca`."* **The `000` was real; the cause was wrong,
    and the wrong cause made a client-side problem look like a hardware one for
    13 days.** Re-measured: DNS resolves (`35.190.75.248`), TCP connects, TLS
    negotiates, and the server presents a **valid** cert (`CN=*.edmonton.ca`,
    Entrust OV TLS Issuing RSA CA 2 → **Sectigo Public Server Authentication
    Root R46**). The failure is local: this box's `ca-certificates-2023.2.60`
    bundle (142 roots) **does not contain the Sectigo R46 root**, so curl
    reports the chain-embedded root as `self signed certificate in certificate
    chain`. Fetching with `certifi`'s bundle instead returns **200 / 61,938
    bytes**. `www.edmonton.ca` deep paths 404 (their URL structure moved) — a
    clean 404 is the host serving normally, not a block.
    - **Workaround for any HTTPS fetch from this box:**
      `ssl.create_default_context(cafile=certifi.where())` (or
      `curl --cacert "$(.venv/bin/python -c 'import certifi;print(certifi.where())')"`).
      Affects **any** host chaining to a post-2021 root, not just `edmonton.ca`.
    - ⚠️ **Lesson (the `todo-can-lag-executed-work` pattern, sharper form):** the
      symptom re-measured true and the blocker was *still* wrong. Re-measuring a
      stale blocker means re-deriving its **cause**, not just re-confirming its
      **symptom** — `000` is a client-side verdict, never evidence about the
      remote host.
  - **Keep separate from the `qi6a-xuwt` bug report** — that one asserts a
    defect, this one requests a field. **Do not put the $125.4M in the
    message**; it depends on the very question being asked.
  - ⚠️ **Do NOT hand-flag individual parcels as exempt meanwhile** (Peter,
    2026-08-08). No verified per-parcel source exists, and the worked examples
    circulated for exactly that purpose were **all wrong** — see the `## Done`
    line for the 2026-08-08 verification.

- [ ] **▶▶ AN EXTERNAL LEVY ANCHOR EXISTS AFTER ALL — Alberta FIR Schedule MR.**
  Opened 2026-08-25. ⚠️ **FIRST-PASS, NOT AUDITED — do not publish any number
  here until it is.**
  - ⚠️ **CORRECTION 2026-08-25, same day: this item first said "OUR MODEL READS
    +18.2% AGAINST IT" and that number was WRONG** — it compared our roll to FIR
    **2025** when the roll is **2026** (item above). It is quoted here rather
    than deleted because the error is instructive: an external anchor is only as
    good as the year you align it to, and the mismatch is what exposed the
    vintage drift. **Correct figures are below.**
  - ⚠️ **The premise "no City-given total exists to check against" is FALSE.**
    It was believed because `edmonton.ca` looked unreachable (that blocker is
    retracted above) — but the anchor was never on `edmonton.ca` at all. It is
    in the **same Alberta Municipal Affairs FIR workbooks
    `scripts/fetch_fir_debt.py` already downloads** for the debt lens
    (`data/DATA.md` §11). That script reads **one** sheet (`AA(1)-Debt`) of
    **51**. Three of the others are `MR(1)-Tax Levy`, `MR(2)-Assessment`,
    `MR(3)-Mill Rate`; `EA(1)-Assessment` is equalized assessment.
  - **Edmonton (code `0098`), financial year 2025, Schedule MR — filed by the
    City with the province:**

    | | taxable assessment | municipal levy |
    |---|---|---|
    | Residential | $148,128,818,480 | $1,129,541,492 |
    | Farmland | $59,062,724 | $450,377 |
    | Non-Residential (incl. linear) | $42,291,523,823 | $1,024,423,352 |
    | Machinery & Equipment | $768,976,453 | $0 |
    | Other (annexed, vacant, …) | $17,087,204,280 | $142,984,457 |
    | **TOTAL** | **$208,335,585,760** | **$2,297,399,678** |

  - ✅ **MR(2) IS THE TAXABLE BASE BY CONSTRUCTION — verified, not assumed.**
    `assessment × MR(3) rate` reproduces `MR(1)` levy to **±0.0000%** for
    Residential, Farmland and Non-Residential. ✅ **And MR(3)'s rates match
    `data/mill_rates.json` EXACTLY** (Residential `7.6254`, Non-Residential
    `24.2229`) — our rate inputs are independently confirmed correct.
  - ⚠️ **THE GAP, YEAR-ALIGNED (2026 roll vs FIR 2026, 2026 rates both sides).**
    Ours **$238,448,551,458 assessed / $2,784,219,936 levy**; FIR 2026
    **$224,199,394,806 / $2,509,075,991**. Gap **+$14.2B assessed (+6.4%)** and
    **+$275.1M levy (+11.0%)**. ⚠️ **Vintage WAS a large part of the
    explanation** — the same comparison mis-aligned to FIR 2025 read +14.5% /
    +18.2%, so **roughly half the apparent discrepancy was the wrong year**, not
    a modelling defect.
  - **Where the residual concentrates — and it is NOT residential.** Against FIR
    2026 by class: residential **+1.2%** (essentially matched), non-residential
    **+20.6% / +$9.08B**, "other residential" vs FIR's "Other" **+21%**.
    ⚠️ **This materially strengthens the institutional-exemption hypothesis**:
    the $5.6B of AJ/UF/UI/PU assessment is now **62% of the non-residential
    gap**, not the 19% of total that the mis-aligned comparison implied.
    ⚠️ **The per-class rows are still not 1:1** (FIR's 5 buckets vs our 4) —
    treat the residential fit as the reliable signal and the rest as a lead.
  - ⚠️ **THIS DOES NOT RESOLVE THE INSTITUTIONAL QUESTION — IT RESIZES IT.**
    Exempt institutional land is now the **leading** candidate for the
    non-residential residual (62% of it) rather than a minor one, but 38% of
    that gap is still unaccounted for. **The direction, however, is no longer
    unknown for the aggregate: we are OVER, not under.** (Per-parcel direction
    for any given institutional parcel is still unknown.)
  - **Candidates checked, and what they were worth:**
    - ❌ **Duplicate parcel records — RULED OUT.** 439,581 rows, 439,581 unique
      account numbers, **zero** duplicated accounts.
    - ❌ **Class-percentage apportionment — RULED OUT as a driver.** Slice
      percentages sum to 100 on all but **80** rows (min 85%); mean 99.9996%.
    - ✅ **Roll vintage — CONFIRMED, and it was about half of it** (item above).
    - ✅ **Bucket mapping — RESOLVED from FIR's own headers + implied rates.**
      `MR(2)` col [10] is *"Other (including annexed, vacant, total minimum
      tax, etc.)"*, **not** "Other Residential" — but its **implied rate
      `8.2872`** (levy ÷ assessment) sits within **1.0%** of our Other
      Residential `8.2064`, and cols [5]/[7] reproduce `7.7419`/`25.2216`
      exactly. Edmonton has no apartment slot in `MR`, so it files that
      sub-class under [10]. **The economic pairing was right; the label was
      not.** (Still inference, but rate-corroborated.)
    - ✅ **Machinery & Equipment — RESOLVED, and it is a non-issue for levy.**
      FIR assesses $759,582,941 at a **`0.0000` rate → $0 levy**. Edmonton
      levies no municipal tax on M&E, so it cannot contribute to the levy gap;
      it makes our *assessment* base look $759.6M **smaller**, not larger.
  - ✅ **WHERE THE NON-RESIDENTIAL GAP PHYSICALLY SITS — spatial join run
    2026-08-25, and one zone code closes most of it.** `gpd.sjoin` of all
    439,581 parcels against `zoning.geojson` (439,573 matched, 8 unplaced):

    | exempt-candidate zones | non-res assessed | share of the $9.08B gap |
    |---|---|---|
    | AJ/UF/UI/PU (the old proxy) | $5,199,452,500 | 57% |
    | **+ PS** | **$8,681,376,500** | **96%** |

    ⚠️ **`PS` is "Parks and Services" and was NEVER in the four-zone proxy** —
    991 parcels, $3.48B. The City's own `description` field names the set:
    `AJ` Alternative Jurisdiction, `UF` Urban Facilities, `UI` Urban
    Institution, `PU` Public Utility, `PS` Parks and Services. **96% of the
    non-residential gap coincides with public/institutional/parks zoning.**
    ⚠️ **Coincidence in a zone is NOT proof of exemption** — this is
    correlational, and `UF`/`PU` include privately-owned facilities
    (`data/DATA.md`). But it is a far tighter fit than anything before it.
  - ⚠️ **THE APARTMENT GAP IS A DIFFERENT ANIMAL AND THE ZONING PROXY IS BLIND
    TO IT.** Only **13%** ($515,535,000) of the $4.00B "Other Residential" gap
    sits on exempt-candidate zoning; the rest is on ordinary `RM`/`RS`/`DC2`
    residential zoning. **Consistent with use-based exemptions the zoning proxy
    structurally cannot see** — seniors' housing, non-profit and social housing
    are exempt by *use* under MGA 362, not by zone. **A zone-based method has
    hit its ceiling here; this bucket needs a different instrument.**
  - ⬜ **Still open:** whether the City apportions where we bill 100% of
    assessed value; the residential +1.2% / $1.90B residual; and the 4% of the
    non-res gap outside the five zones.

- [ ] **▶ WHO IS MISSING FROM THE CURRENT ROLL RIGHT NOW? — 1,457 parcels /
  $1.07B with no current-roll match.** Opened 2026-08-07 from
  `tools/audit_roll_continuity.py` (historical 2024 vs the live roll, matched by
  **position** within 5 m so renumbering / re-addressing / hood renames do not
  register). 168 of them are over $1M, totalling **$856M**. Largest: EDMONTON
  SOUTH CENTRAL `10884618` $38.4M, WOODCROFT `1012137` $37.7M, GRANVILLE
  `10501062` $33.8M.
  - ⚠️ **THESE FIGURES REPLACE 1,534 / $1.62B — AND SO DO THE EXAMPLES.**
    Re-measured 2026-08-30 (second observation, below). **The three parcels this
    item used to name as its largest cases — MILL WOODS TOWN CENTRE `9980213`
    $69.0M, YELLOWHEAD CORRIDOR WEST `10275721` $60.5M, SOUTHEAST INDUSTRIAL
    `9985679` $53.5M — were never missing.** All three sit on the current roll
    under their original account numbers. Do not cite them.
  - **The per-parcel list is now committed** —
    `data/roll_continuity_candidates_2026-08-30.csv` (1,578 rows, `acquitted`
    column). ⚠️ **Diff the next run against this file**, and pass `--out`; the
    reason this item stalled three times is that only the headline count ever
    survived a run.
  - **Why it matters:** every one of these is a potential Misericordia — a
    property still assessed but absent from the published current roll, whose
    neighbourhood is **understated on the live map** for as long as the gap
    lasts. That is a silent revenue-side error with no guard behind it before
    the fact (`check_revenue_deltas.py` only catches the *return*).
  - ⚠️ **CANDIDATES, NOT VERDICTS.** Demolitions, subdivisions and
    consolidations legitimately have no 1:1 successor and are in this list. The
    audit cannot tell those apart, and **one run cannot distinguish a transient
    renumber gap from a permanent removal** — that needs a second run later.
  - **Next step is cheap and decisive: RE-RUN IT and diff.** Anything that
    reappears was a transient gap (and its hood was understated meanwhile);
    anything still absent months later is a real removal. Nothing else about
    this item can be settled without that second observation.
  - ✅ **SECOND OBSERVATION DONE 2026-08-30** (first attempted 2026-08-09, when
    the roll had not moved). Roll republished: **439,634** rows against the
    439,631 baseline — **+3 net**, yet the candidate set moved by 44, so a tiny
    row delta hides real churn. ⚠️ **Do not use the row count to decide the
    answer can't have changed** — only to decide whether the source moved at all.
    - **What the diff CANNOT say:** nothing persisted the 2026-08-07 per-parcel
      list, so transient-vs-permanent is still unseparated. Fixed forward — the
      list is committed now.
  - ⚠️ **THE BIG FINDING IS A FALSE-POSITIVE CLASS, NOT THE DELTA.** Position
    matched 1,578 as unmatched; **121 of them ($592M — 35.6% of the value at
    risk) carry an account number still on the current roll.** They never left,
    they were recentroided past the 5 m tolerance. Verified against account
    reuse: 121/121 resolve to a plausible same-property current record (104
    identical hood, 17 boundary/rename churn like `CHAPPELLE` → `CHAPPELLE
    AREA`). The tool now runs an **acquittal pass**.
    - ⚠️ **DO NOT WIDEN `--tolerance-m` TO "FIX" THIS.** The acquitted moved a
      **median 58 m, max 559 m**; at 25 m only 30 of 121 come back, and a
      tolerance that wide starts matching the *neighbouring* parcel — trading a
      visible false positive for a silent false negative. The 5 m figure came
      from a **four-hospital sample** (0.6–1.6 m) that does not generalize to
      large commercial parcels.
    - **Why an identifier is allowed here** after `DECISIONS.md` 2026-08-07 said
      never to match on one: matching **on** an identifier creates false
      negatives (they all churn), but using one only to **acquit** can only
      remove false positives. The asymmetry is the licence.
  - ⚠️ **$1.07B IS STILL AN UPPER BOUND.** A parcel that both renumbered *and*
    recentroided past 5 m is a false positive the acquittal cannot see. Every one
    of the 1,457 has *some* current parcel within 427 m (median 36 m), so
    distance alone acquits no more of them.
  - **Running it again:**
    - **Readiness test before spending a run:** fetch the current roll and
      compare its row count to the baseline. Identical → the source has not
      moved and the answer cannot have changed.
    - ⚠️ **`--cache-dir` DEFAULTS TO `/tmp/roll_continuity` AND A WARM CACHE
      MAKES THE "RE-RUN" A REPLAY.** The first 2026-08-09 attempt reproduced
      1,534 / $1.62B off 45-hour-old files and read as a real null result. The
      tool now logs `CACHE HIT` at WARNING with the file's age — **but pass a
      fresh `--cache-dir` anyway.** A prescribed "just re-run it" that silently
      replays its own first answer is the third time this item's stated next
      step has not survived contact.
    - **Also measured, and not what the audit uses:** the local
      `data/raw/` snapshot was **439,685** rows (2026-07-06) against the API's
      **439,631** — the roll *shrank* by 54 accounts. Irrelevant to this tool,
      which fetches from Socrata directly, but it means a local
      `download_data.py` does **nothing** for this item. Do not repeat that.
  - ⚠️ **Do not report this upstream yet — and the second run STRENGTHENED that.**
    0.34% of parcels is within the range ordinary demolition/subdivision could
    explain, and we still have **no baseline for how much of it is normal** —
    unlike the `qi6a-xuwt` gap, which was measured against a control. A report
    sent on 2026-08-07's figures would have named three parcels that were on the
    roll the whole time.
  - **What would actually settle it, now that a baseline list exists:** diff the
    next observation against `data/roll_continuity_candidates_2026-08-30.csv`.
    A candidate that has reappeared was a transient gap (and its hood was
    understated meanwhile); one still absent months later is a real removal.
    That split is the reportable finding — the raw count never was.
  - ⚠️ **Do NOT "fix" this by dropping the parcels.** We apply published rates to
    the published roll; silently excluding records the City published is the
    exact silent-correctness failure the guards exist to prevent.
  - **Not an Open Data bug report.** Nothing here suggests the City's roll is
    wrong — the earlier framing assumed a defect and the evidence does not
    support one. Keep this separate from the `qi6a-xuwt` item.

- [ ] **PETER'S CALL: wire roll-continuity into `refresh.yml` as a SECOND
  guard?** Opened 2026-08-07 (S101 — it existed only in S100's session summary
  and would have evaporated on the next `/clear`).
  - **What it would catch that nothing else does:** `check_revenue_deltas.py`
    only fires when a missing property **returns** (the +130% correction).
    Nothing fires while a hood is understated, which is the whole window in
    which the map is wrong. A roll-continuity step would catch the *departure*.
  - **What changed in its favour:** the churn baseline now exists — accounts
    vanish at **0.15–0.37%/yr**, spiking to **0.91% (3,893 accounts)** in
    2023→24 — so this is a measured standing property of the data, not a hunch.
    That makes it more defensible than when it was first floated.
  - **What argues against:** it adds a **second issue-filing channel** on top of
    `revenue-delta`, and ⚠️ **the audit itself cannot separate a transient
    renumber gap from a permanent removal in one run** — so a CI version would
    file issues it cannot adjudicate. **Settle the 1,457-parcel item above
    first**; a diff against its committed baseline is what tells us the base
    rate. ⚠️ **The 2026-08-30 run sharpened this argument, not softened it:** a
    third of the value it reported was parcels that never left the roll, so a CI
    version wired up before the false-positive class was understood would have
    filed issues about parcels sitting on the roll the whole time.
  - If built, it must follow the existing guard's shape: **warn-not-fail, always
    exit 0, run BEFORE the commit step** or its baseline becomes the new data.

- [ ] **CARDINALITY GUARD — two small follow-ons (guard shipped 2026-07-28, PR #110).**
  `scripts/check_value_anchors.py` now pins the record-to-parcel *regime* in
  bands and runs in `refresh.yml` after regeneration. Both known bugs were
  re-verified as non-issues (see `AUDIT_LEDGER.md` 2026-07-28); this is
  maintenance, not a defect.
  - [x] **Tighten the bands — DONE 2026-08-05, but only FOUR of six.** See the
    `## Done` line; the split and its reasoning live in
    `data/expected_value_anchors.json`'s own `_why_two_widths` /
    `_ineligible_pair_is_drifting` fields.
  - [ ] **▶ WHY IS VALUE LEAVING THE LOT-ACRE DENOMINATOR? (NEW 2026-08-05, out
    of the band work.)** `ineligible_points` and `ineligible_value_frac` moved
    **monotonically upward on every independent data change** — 56 → 58 → 60 and
    0.00517 → 0.00575 → 0.00633 across 2026-08-01 / 08-03 / 08-04, no reversal.
    That is the **dangerous** direction by the guard's own `DANGER` map: growth
    means more assessed value silently dropping out of the lot-acre metric.
    - **This is the guard doing its job**, not a nuisance. `check_value_anchors`
      calls these points *"majority-null multi-unit"* — they leave the lot-acre
      numerator AND denominator while staying in ground-acre, so the two lenses
      quietly diverge as the count grows.
    - ⚠️ **`ineligible_value_frac` has used ~72% of its band** and would breach
      in roughly **2–3 more moves of the observed size**. Its band was left wide
      deliberately so that when it fires it fires on something real — **do not
      widen it further to buy silence, and do not tighten it to "finish" the
      band work.** A test pins both against exactly that.
    - **What would answer it:** which points became ineligible between two
      refreshes, and why — a new majority-null pattern in `Property_Info`, a
      condo/multi-unit regime change, or upstream nulls. ⚠️ **Needs two dated
      raw snapshots to diff**; `data/raw/` holds only the current pull, so this
      likely means capturing the next one or two refreshes before diffing.
    - ⚠️ **Only 3 independent observations exist** (the 2026-08-02 and 08-05
      runs committed `status.json` only, so their anchors re-measure unchanged
      input). Confirm the trend continues before treating the slope as real.
  - [ ] **Optional, Peter's call: lower `STALE_DAYS`.** Currently 14 against a
    weekly cron = one missed run tolerated, two consecutive misses warn. A
    drift failure is therefore viewer-silent for 14 days. If that is too long
    for a public audience, the knob is global (`web/index.html`) and should
    move for ALL failure types at once — deliberately NOT a per-guard banner
    (`DECISIONS.md` 2026-07-28).

- [ ] **GEOGRAPHIC REFERENCE LAYERS — TIERS 2 & 3 (Tier 1 shipped 2026-07-27).**
  Tier 1 (North Saskatchewan River + Anthony Henday ring road) is live and on by
  default; see `DECISIONS.md` 2026-07-27 (×2) and `data/DATA.md` §14. The render
  seam is proven: `buildLayers()` BRACKETS `buildViewLayers()` —
  `referenceUnderLayers()` (river, bottom) before it, `referenceOverLayers()`
  (ring road, top) after — one Display-menu toggle, `verify-reference-layer.js`.
  **Which end a new reference shape belongs at is a real question, not a
  default:** the river went underneath because the hood fabric already traces
  it (set-aside valley = a river-shaped seam), so painting over glitched; the
  ring road has no such seam and is invisible underneath. What's left:
  - [x] ~~**Tier 3b — the REGIONAL NAMES, beyond the seven towns.**~~ **DONE
    2026-08-08 (PR #187), live in production.** The four counties, the
    Industrial Heartland, Nisku and the airport are named; Morinville and Stony
    Plain joined the towns (16 names, 33 features). Edmonton's limit is drawn
    with its own stroke but **deliberately unnamed**. ⚠️ **This reversed the
    2026-07-27 "regions are unlabelled" decision** — see `DECISIONS.md`
    2026-08-08 and `DATA.md` §14 before re-opening it. ⚠️ **Tier 2 below
    inherits a hard-won constraint from it:** outlines are split into one layer
    per stroke with CONSTANT accessors, because a per-feature `getLineColor`
    builds a per-vertex attribute buffer and blew the verify's click timeout.
    Style a new Tier-2 shape by adding a layer, never by adding an accessor.
  - [ ] **Tier 2 — Edmonton internal reference.** District labels (West
    Edmonton, Mill Woods, Castle Downs, Terwillegar, Southeast) + Downtown and
    Old Strathcona/Whyte Ave; major arterials as thin unlabeled lines
    (Whitemud, Yellowhead, Gateway/Calgary Trail) from the existing road feed,
    same allowlist technique as the Henday. **Label collision is DECIDED
    (2026-07-27, Peter):** feed district labels into the existing
    `visibleLabels()` declutterer with districts winning priority — do NOT add
    a second, independent label layer, or "MILL WOODS" will stack on "MILL
    WOODS TOWN CENTRE". Districts have no dataset; coordinates are hardcoded
    and placement is a design call, not a data-fidelity one.
  - [x] ~~**Tier 3 — the NAMES half.**~~ **DONE 2026-07-27.** Seven regional
    place names ship on by default (St. Albert, Sherwood Park, Spruce Grove,
    Fort Saskatchewan, Leduc, Beaumont, Devon). Split out from the boundaries
    deliberately: the names needed no polygon fetch, and bundling them was what
    made Tier 3 look expensive. See `DECISIONS.md` 2026-07-27 (×2),
    `data/DATA.md` §14, `docs/UI.md`.
  - [x] ~~**Tier 3 — the BOUNDARIES half (still open).**~~ **DONE 2026-08-08 —
    and this item was ALREADY HALF-STALE when it was worked.** The neighbouring
    municipalities' outlines had shipped with the *names* half back on
    2026-07-27 (`reference-boundary`, seven polygons); what was genuinely
    missing was **Edmonton's own legal limit and the rural municipalities**,
    which this item never asked for. Both now ship as `REGIONS` in
    `scripts/build_reference_layers.py`: Edmonton + Strathcona / Sturgeon /
    Parkland / Leduc County, unlabelled, unfilled, under the data.
    ⚠️ **What it exposed is the durable part: the hood fabric is not the city.**
    Legal boundary **782.1 km²** vs **672.4 km²** of rendered hoods → **109.6
    km², 14.0% of Edmonton, has no neighbourhood at all** and had been reading
    as background. One-directional (0.0 km² of fabric outside the limit), so
    the map understates the city and never overstates it. **No metric moves**
    (all are per-hood), but a future *citywide-per-acre* figure must state which
    denominator it means. `DECISIONS.md` 2026-08-08, `data/DATA.md` §3 + §14.
    Original notes below, kept because the sublayer traps are still live:
    Alberta `urban_and_rural_municipality` MapServer, natively **EPSG:3400**.
    **Sublayer IDs confirmed:** Edmonton / St. Albert / Leduc are all in
    **78 (`City`, field `CITY_NAME`)**; **Strathcona County is in 104
    (`Specialized Municipality`, `SPMUN_NAME`) — NOT 114
    (`Municipal District and County`)**, which holds Leduc/Sturgeon/Parkland
    *County*. Ids 67/95/105 are group layers and return no fields. Note the
    names half needed a *third* sublayer, **66 `Urban Service Area`**, for
    Sherwood Park — the hamlet-like service area of Strathcona County, which is
    a different thing from the County polygon in 104.
  - [x] ~~**Which end of the stack do boundaries belong at?**~~ **ANSWERED
    2026-07-27 for the neighbours, and 2026-08-08 for the regions: UNDER the
    data, with the river.** The neighbours sit outside Edmonton where there is
    no hood fabric to hide them (measured: 0–0.7% of each outline overlaps the
    city), so underneath they are fully visible AND can never cut across a
    prism. ⚠️ **Edmonton's own limit is the one case that argument does NOT
    cover** — it is the only outline that runs *through* the fabric rather than
    outside it. Under the data is still right (an over-composed line would
    slice the prisms it crosses), but it means the limit is partly hidden where
    hoods meet it, and fully visible exactly along the 14% that has no hood —
    which is the read we want.
  - [ ] **Zoom-gating does not exist yet** — nothing in `index.html` gates on
    zoom today, so Tier 2/3 introduce the concept. Tier 1 deliberately renders
    at all zooms.
  - **Explicitly out of scope (decided 2026-07-27):** the Edmonton river
    valley/ravine overlay (`gis.edmonton.ca` Common_Layers 115). It is a
    regulatory development-setback polygon, not the river — drawing it near the
    water would read as "the river is this wide."

- [ ] **MOBILE USABILITY (NEW 2026-07-22 — full plan in
  `docs/MOBILE_USABILITY.md`; read it first).** Phone rendering is unstyled for
  small screens (zero `@media` queries today). **Confirmed problem:** the top
  third collides — title/blurb + all six control pods stack on top of each other
  at 390 px (screenshot-verified); wide pods clip off the left edge. Map render +
  bottom legend are fine; tap-to-inspect tooltips work on real devices. Separation
  seam is clean: render is shared (one WebGL canvas), but all chrome/layout is
  isolatable behind an `@media` block with zero desktop risk. Quick-pass order:
  (1) add the `@media (max-width:640px)` seam, (2) fix the top-third collision
  (collapse pods + shorten the blurb), (3) stop the left-edge clip, (4) re-render
  via `tools/profiling/shot-mobile.js` + real-device check. ~~NOT greenlit for the
  approach yet (single scroll column vs bottom-sheet/hamburger — decide at step 2).~~
  ✅ **APPROACH DECIDED 2026-08-04: the single scroll column, no bottom sheet and
  no hamburger** — steps 1-4 are all closed, so this quick-pass list is a record,
  not a queue (`docs/TODO_archive.md`).
  - [x] ~~**DECIDE FIRST: control regrouping**~~ — **DECIDED 2026-07-23** (8
    decisions, `CONTROLS_MATRIX.md` §7 + `DECISIONS.md` "Controls & lens grouping").
    All 7 §5 combos closed. Final shape: `#views` = 5 (Money · Services · Ratio ·
    Uses · Development); Glass → mode of Money; Infill + Industrial → full-only Dev
    extras; palette + Labels → an accessibility menu; stack reordered
    View→Variant→Presentation; "Residential only" → "Highlight residential"; Dev
    grid+spike → one 3-way Detail selector. `public|full` tags all resolved in the
    same pass (public = Money/Services/Ratio/Uses/Development-activity; `/full/`
    adds Infill + Industrial + deep data-detail). **Nothing built yet.**
  - [x] ~~**BUILD ONCE: implement the 8 regroup decisions in `web/index.html`.**~~
    **BUILT 2026-07-23 (branch `regroup-build-s65`, NOT yet on master).** One reflow:
    the top stack is now a `#controls` flex column (tier order via `order:`), Glass
    is a 2-way Money "Detail" toggle (internal view unchanged), Dev grid+spike is one
    3-way Detail selector (Neighbourhood / 100 m grid — activity / Stock age), Infill
    is a full-only Dev *mode* (`#devmode`), Industrial is a full-only `#devmetric`,
    palette + Labels moved into a "Display" accessibility popover, `Residential only`
    → `Highlight residential`. `BUILD` flag (`public|full`, `?build=public` override)
    gates the two full-only controls. Full verify-`*`.js suite green in **both**
    builds; verify + shot scripts updated to the new controls.
    - [x] ~~**⚠️ merge gate: two-build deploy plumbing**~~ — **RESOLVED 2026-07-23**
      (same branch): the emit now rewrites `DEFAULT_BUILD → public` for the root
      copy, so merging `regroup-build-s65` to master ships the *public* controls to
      the site root. **Branch is now safe to merge** (review + merge is Peter's call).
    - [ ] **THEN mobile CSS** (below) reflows the *final* grouping (inherits the flex
      column + Detail selectors — the structure-before-mobile payoff). *Partly done:*
      move-1 shipped 2026-07-24 (`@media` seam, collapsing title, bounded control
      column) and the `#views` **size** half of the "under-reads as primary" concern
      is fixed 2026-07-25. **Still open: the `#views` POSITION question** — it's
      still a thin strip at the very top. ⚠️ **It used to ride on the move-2 /
      bottom-sheet fork; that fork was REFUSED 2026-08-04**, so position now needs
      its own proposal if it is ever revisited (`MOBILE_USABILITY.md` §3).
    - [x] ~~**Regenerate `docs/LENS_INVENTORY.md`** from the rebuilt wiring.~~
      **DONE 2026-07-25.** Rewritten from the code (not patched): two-build table,
      4/5 views with Glass as Money's `#moneydetail` mode and Infill as
      Development's `#devmode` lens, the three different "doesn't apply here"
      behaviours (`#toggle` hides / `#lens` hides / `#coloradj` greys), per-view
      data gates, combination counts, and a code-anchor table. Every row of the
      matrix was **probed against the live site** in both builds, not inferred.
    - [x] ~~**`CONTROLS_MATRIX.md` §2–§5 still stale.**~~ **DONE 2026-07-25.**
      §1–§5 rewritten against the probed live behaviour: 4/5 views with the two
      internal modes named, the Options-fold structure (T2+T3 both live inside
      `#optpanel`, folded by default ≤640px), corrected §4 rows, and a §5 split
      into **still-open (numbered 1–7)** vs **resolved-by-the-regroup (original
      letters kept, because `DECISIONS.md` cites "§5.G"/"§5.A/B"/"§5.F")**.
      §7 reframed from "not yet on master" to merged & live.
    - [x] ~~**Two stale code comments in `web/index.html`**~~ — DONE 2026-07-26,
      folded into PR #96 rather than spending a deploy on a comment-only diff.
      All three siblings now agree that `devGridOfferable` excludes **only**
      Industrial. `CONTROLS_MATRIX.md` §6 closed out.
  - [x] ~~**Two-build deploy plumbing (`PLAN_public_release.md` §2a).**~~ **BUILT
    2026-07-23 (branch `regroup-build-s65`).** `scripts/build_site.py` fans `web/`
    into one Pages artifact: `_site/` = public root (whole tree, `DEFAULT_BUILD` →
    `public`) + `_site/full/` = specialist (`index.html` only, `<base href="../">`
    so its `./data`/`vendor` resolve to the ROOT's shared copies — no GeoJSON
    duplication — `DEFAULT_BUILD` `full`, + a fixed work-in-progress badge). Wired
    into BOTH `deploy.yml` (system `python3`, stdlib-only → stays the fast code path)
    and `refresh.yml` (before `upload-pages-artifact`, `path → _site`), factored once
    as the shared script. `tests/test_build_site.py` guards the emit + that the
    source `DEFAULT_BUILD` literal exists (a drift fails `refresh.yml`'s pytest gate
    before deploy). Verified locally: both URLs smoke-clean. **`/full/` is unlisted,
    NOT access-controlled** (repo is public → nothing secret; the WIP badge is the
    mitigation).
  - [ ] **Selective/partial data regen (DEFERRED — `SPEC_deployment.md`
    "Two deploy paths").** Teach the *data* run which datasets a change needs so
    even a refresh skips untouched sources. Signal exists (`rowsUpdatedAt` per
    dataset; roads static 2+ mo while permits/fire change daily) but needs
    raw-file caching across CI runs, and the weekly cron sits right on GitHub's
    7-day cache eviction. Real payoff on slow static layers (roads/zoning), real
    fragility — separate project, not started.

- [ ] **PARKED: Regional comparison lens (St. Albert / Strathcona; Phase 2,
  not November scope).** Spike complete (PR #69, `docs/SPIKE_regional_lens.md`
  — read it first). Feasible in principle but blocked on: (a) **St. Albert
  licensing** — the LandScape REST service is not a catalogued open dataset
  and its bulk-query-ability is likely incidental, not licensed; needs direct
  confirmation from the City before any raw-data use; (b) Strathcona
  multi-unit dedup rule unsolved; (c) output design undecided beyond
  "citywide aggregate chart is the safe/realistic scope". **Do not commit
  St. Albert per-parcel data to the public repo under any circumstances until
  (a) is resolved.** (Strathcona licensing is clean: OGL-Alberta via
  catalogued open-data hub datasets.)

- [ ] **INDUSTRIAL & NON-RESIDENTIAL LENS FAMILY (NEW 2026-07-18 — full plan in
  `docs/SPEC_industrial.md`; read it first).** Two tracks: A = non-res
  decomposition inside the existing hood/grid frame; B = citywide-aggregate
  regional context from Alberta Municipal Affairs sources (OGL-Alberta,
  established fetch pattern — extends `fetch_fir_debt.py`; NOT the parked
  per-parcel regional lens above, which stays parked untouched). Tone rule is
  stricter here — descriptive only, see the spec. Build order A1 → A3 → A2 →
  B2 → B1 → B3:
  - [x] ~~**A1 — Non-res $ cut (greenlit 2026-07-18)**~~ — **SHIPPED
    2026-07-18** (`feat/nonres-revenue-metric`): `nonres_levy` = the slices
    billed at the Non Residential rate (COMMERCIAL + MA DERELICT + DESIGNATED
    IND PROPERTIES via `NONRES_RATE_LABELS`; exempt is $0, farmland its own
    class; identity `levy == res + nonres + farmland` tested) → fourth Money
    metric "Non-res $" + Glass grid columns (appended last). Real data: 47.4%
    of citywide levy; clamp $50k (p97.5 ≈ $48.4k); 34% of cells nonres > 0.
    `verify-nonres-revenue.js` ALL PASS; DATA.md §4 + UI.md. Live on the next
    weekly refresh (column guard until then).
  - [x] ~~**A3 — Industrial permit velocity (greenlit 2026-07-18)**~~ —
    **SHIPPED 2026-07-18** (`feat/ind-permit-velocity`, stacked on A1):
    `INDUSTRIAL_BUILDING_TYPES` (400-series, full-string — Parkade 490 is NOT
    industrial) → `ind_permits` count → `ind_permits_per_acre` (+ `_3yr`).
    Third `#devmetric` option "Industrial" — Development-view choropleth only
    (Detail toggle hides; Infill resets it to a residential metric + hides the
    button). Real data: 283 permits / 117 hoods (5yr). `verify-ind-permits.js`
    ALL PASS; DATA.md §10 + SPEC_development + SPEC_industrial A3. Live on the
    next weekly refresh (column guard until then).
  - [ ] **A2 — Shovel-ready industrial land:** `stt5-pzaa` verified 2026-07-18
    (annual snapshots 2016–2023, `servicing` field, centroids); absorption
    computable from snapshot diffs; display undecided.
  - [ ] **A4 — Assessment-lag methods note:** Nov 29 2024 council memo
    attachment (Table 1, permit→assessment 3–5 yr lag) — edmonton.ca fetch,
    likely Peter/laptop.
  - [ ] **B2 — Regional non-res mill rates:** `2026_Tax_Rates.xlsx` on the FIR
    page (verified live) + yearly workbooks; 6 municipalities; reviewed JSON.
  - [ ] **B1 — Regional non-res assessment share:** FIR/SIR + equalized
    assessment XLSX (2024–26 verified on open.alberta.ca — NOT PDF-only);
    rebuild the published-share-series discrepancy from primary data.
  - [ ] **B3 — Industrial-areas context map:** illustrative; municipal
    boundary layer source to verify.

- [ ] **PUBLIC RELEASE PREP (NEW 2026-07-09 — scope + rationale in
  `docs/PLAN_public_release.md`; read it before working these).** An external
  prioritization memo was intaken and reconciled: its build list (WEM/condo fix,
  roads, set-aside, fire, stormwater) is **already shipped or closed** — see the
  plan's reconciliation table. What remains is presentation-layer credibility +
  ops hardening. Release scope locked: everything live stays in; transit/
  recreation/franchise-display stay out. *(AMENDED 2026-07-11, Peter: the
  transit lens is IN — built as the fourth service; see the service-layers
  item below. Recreation + franchise-display still out.)* Items, ranked:
  - [x] ~~P1.1 README refresh~~ — done 2026-07-09 (this PR): "Methodology
    (Planned)"/QGIS/AltaLIS-FOIP sections replaced with as-built.
  - [x] ~~**P1.2 In-app attribution/methods affordance**~~ — **DONE 2026-07-25**
    (PRs #94 + #95, both merged & live). Bottom-right `#about` pod above Display,
    labelled **`Data & Methods`**; the popover carries the City of Edmonton
    credit + Open Government Licence, the vintages, the modelled-not-billed
    caveat for revenue *and* the utility layers, and links to METHODS.md + the
    repo. **All years/dates come from `status.json`**, so the January year-roll
    can't strand a stale literal. `verify-about.js` (390/360/1440 overlap
    geometry, paint order, link resolution, a status.json-blocked run). It first
    shipped with the full credit AS the label; **reverted the same day** — 294px
    wide, it sat on the legend — and the collapsed-behind-a-button form turns out
    to be the map convention anyway (`UI.md` "What other maps actually do").
    Fixed three latent bugs on the way: `#botleft` swallowing pointer events, the
    z-index:1 paint-order collision, and `#legend` running under the right-hand
    column on phones. See `DECISIONS.md` 2026-07-25.
    - [x] ~~**Read the actual OGL – City of Edmonton text**~~ — DONE 2026-07-26
      (v1.0 July 2022, an adaptation of OGL–Canada 2.0). **Placement assumption
      confirmed: the licence says nothing about where attribution appears**, so
      the collapsed pod stands and the credit does NOT return to the map surface.
      But it caught two real gaps, both fixed the same day: (1) no link to the
      licence, which it asks for "where possible", and (2) the prescribed
      attribution sentence was paraphrased rather than verbatim. Added a
      non-endorsement line too (not required; the licence forbids implying
      official status). `docs/UI.md` "What other maps actually do",
      `DECISIONS.md` 2026-07-26. **P1.2 now has no open questions.**
  - [x] ~~P1.3 Public METHODS page~~ — done 2026-07-09 (PR #32 merged):
    `docs/METHODS.md` (metric definitions, denominators + guard, set-aside,
    WEM/condo worked examples, model formulas + validation ratios,
    limitations) + README Technical Docs link. P1.2 should link to it.
  - [x] ~~**P2.1 CI unmatched-set assertion**~~ — DONE 2026-07-11
    (`scripts/check_unmatched_names.py` + `data/expected_unmatched.json`, wired
    into `refresh.yml`; fails the build on a new money-path unmatched name). See
    the data-integrity audit §4 item below for scope detail.
  - [x] ~~**P2.2 Heartbeat PAT**~~ — DONE 2026-07-26, built as *two* halves
    because the PAT alone leaves the failure invisible when the PAT itself
    expires: (a) `refresh.yml` checks out with
    `${{ secrets.HEARTBEAT_TOKEN || github.token }}`, (b) the frontend ages
    `status.json`'s `last_checked` and raises the banner past `STALE_DAYS = 14`,
    (c) the commit step no longer swallows push failures green.
    `verify-staleness-banner.js`, `DECISIONS.md` 2026-07-26, `RUNBOOK.md` §3.
    - [ ] **Peter — one manual step left: create `HEARTBEAT_TOKEN`.** Fine-grained
      PAT, repo access `edmonton-tax-viz` only, Contents: Read and write, nothing
      else → repo Settings → Secrets and variables → Actions. Until it exists the
      workflow runs exactly as before (the fallback), so nothing is broken
      meanwhile — only the prevention half is dormant. Steps in `RUNBOOK.md` §3.
  - [x] ~~P2.3 Security/PII checklist pass~~ — done 2026-07-09 (Session 33,
    Fable audit): all boxes ticked/dated with evidence; scope updated to the
    Phase-2 static-site + CI surface. **Findings logged, not fixed** — see
    `docs/security-audit.md` "Findings — 2026-07-09" (S1–S6). Follow-ups:
    - [x] ~~**P2.3a Apply S1** (Medium): vendor maplibre-gl@4.7.1 + deck.gl@9.0.38~~
      DONE 2026-07-12 — vendored all three files into `web/vendor/`
      (`maplibre-gl-4.7.1.{js,css}`, `deck.gl-9.0.38.min.js`), `web/index.html`
      points at local copies (no CDN ref remains). Cross-verified vs jsdelivr,
      hashes in `web/vendor/README.md`; basemap is `sources:{}` so zero external
      runtime deps. verify-transit.js 24/24 against the vendored build. See
      security-audit.md S1 RESOLVED. (Branch `vendor/js-libs`, PR #40 merged.)
    - [x] **P2.3b Apply S3 + S4** (2026-07-12): S3 — added `esc()` helper and
      applied it to `neighbourhood_name` + `set_aside_reason` in `tooltipFor`
      (`web/index.html`); verify 24/24. S4 — SHA-pinned all four actions in
      `refresh.yml` (release version in trailing comment). Both → RESOLVED in
      `docs/security-audit.md`. Dependabot auto-bump left out (owner's call).
    - [x] **P2.3c S5 hygiene** (2026-07-12): bumped the 5 dev-freeze pins
      (tornado→6.5.7/bleach→6.4.0/soupsieve→2.8.4/jupyter_server→2.20.0/
      jupyterlab→4.5.9) + a 6th newer CVE found at fix time (mistune→3.3.0);
      `pip-audit -r requirements.txt` now clean. Added a **non-blocking**
      `pip-audit -r requirements-ci.txt` step to `refresh.yml`. → RESOLVED in
      `docs/security-audit.md` S5.
    - [ ] **P2.3d S2** — owner-only content decision, see security-audit.md S2.
  - [ ] **P2.5 Doc-drift fixes** (from the 2026-07-09 architecture
    reconciliation — six items listed in `docs/ARCHITECTURE.md` "Reconciliation
    notes"; no behavioural drift, docs lagging build only). Includes verifying
    the approximate Phase-1 dates in the new `docs/DECISIONS.md` index.
  - [ ] **P3 Decoteau/HHR/Riverview IIMP annotation** (= the existing item
    below; laptop-only) — the OIC-reconciliation credibility anchor; wanted
    before wider outreach, not gating a soft link.
  Platform question RESOLVED (Peter, 2026-07-09): **no new hosting, no new
  engineering** — release ships on the existing Pages deployment, nothing new
  gets built pre-release (plan §2).

- [ ] **Decoteau / Horse Hill / Riverview capital & debt annotation (NEW 2026-07-08).**
  A **citation/annotation layer, NOT a new spatial cost lens**, covering the three
  greenfield growth areas analyzed in the City's IIMP (Integrated Infrastructure
  Management Plan) — a 39-year capital pro forma (developer capital + muni/provincial
  capital + O&M + lifecycle renewal, amortized vs projected tax revenue). This is a
  **fundamentally different unit of analysis** than the citywide recurring-cost map
  (which deliberately excludes capital construction cost). Why now: IIMP is the closest
  existing precedent to the **OIC** (operating-impact-of-capital) accounting the City is
  introducing for the **2027–2030 zero-based budget cycle** — citing it well anchors the
  tool's credibility without rebuilding a citywide capital/debt model we have no data for.
  **Scope (locked — do NOT deviate without flagging):**
  - Click→panel annotation (no sidebar exists — interaction TBD) on **three
    specific named hoods only**, clearly labeled as a
    different methodology (multi-decade capital pro forma) from the revenue-per-acre /
    recurring-cost map.
  - **Do NOT** merge these figures into the citywide colour layer, the roads lens, the
    utilities lenses, or any recurring-cost calc; **do NOT** interpolate/extrapolate
    capital-debt cost to other hoods. Only these three growth areas have a published IIMP
    analysis — citywide capital-cost data at this fidelity doesn't exist.
  - Neutral/descriptive framing per project convention: state the IIMP's own projected
    figures + time horizon, don't editorialize.
  **Build:**
  1. Pin Decoteau, Horse Hill, Riverview boundaries in the existing hood boundary file.
  2. Attach a data **annotation (not a computed layer)**: developer capital, muni/provincial
     capital (~$369M piece), build-out horizon, revenue-vs-cost gap — all as stated in the
     source, with explicit citation + "as of" date.
  3. Surface as a click-through popup / footnote-style panel — **NOT** a toggle affecting
     the main colour ramp.
  **Sources — VERIFIED 2026-07-15 (laptop), research half DONE.**
  - **PRIMARY: Report CR_2705, "IIMP – Cumulative Impacts," March 22 2016** (+ 20-pg
    Attachment 1). **Every figure verified against the primary tables** — see
    `docs/FINDINGS_iimp_growth_areas.md`: developer $3.806B (Drainage $2.351B +
    Transportation $1.455B); City/Province $1.362B (full 8-line Table 3 breakdown
    confirmed); ~$1.4B 50-yr cumulative shortfall (**distinct** from the $1.362B
    capital — do NOT conflate, both ~$1.4B by coincidence); areas Decoteau 1,960 ha/
    74,565/39yr, Horse Hill 2,793 ha/70,038/36yr, Riverview 1,435 ha/50,422/30yr;
    combined pop 195,025. All **2016$, projections at build-out, "received for
    information"**. PDFs saved `data/raw/iimp/` (gitignored). doniveson.ca archive
    reachable from Oracle too, so the BUILD (D2) is not laptop-gated.
  - **Currency check done:** the 2016 IIMP is NOT superseded per-area — the new
    CIO/OIO framework (2027–2030 budget) is a citywide 10-yr capital outlook, not a
    per-growth-area pro forma. Cite 2016 IIMP, date-stamped. → build = ticket D2.
  - 2016 Global News coverage (already in project research) as secondary corroboration —
    primary report should supersede it for exact figures.
  - Off-site levy bylaw + capital financing policy — how the ~$369M muni/provincial piece
    was financed (debt vs levy vs grant); that's the "debt" component specifically.
  - City annual financial statements / debt management reports — actual debt-servicing
    cost + interest rates for the relevant financing period, IF we want real debt-service
    cost rather than just capital outlay.
  - Infrastructure committee **mid-2026 OIC presentation** (already in project context) —
    check whether it re-presents/updates the three areas' figures under the new OIC
    framework; if so, cite that instead of the 2016 analysis.
  **Non-goals:** no citywide capital-cost-per-hood dataset this pass; no blending into any
  recurring-cost lens.

- [ ] **GROWTH INFRASTRUCTURE FINANCING PANEL ("Debt Lens") — NEW 2026-07-14
  (brief: `docs/fable_brief_debt_lens.md`; scoped to these tickets same day).**
  From Peter's planning conversation; full research backing lives in claude.ai
  project knowledge (`Edmonton_Growth_Infrastructure_Financing__Feasibility...`),
  NOT in this repo — the brief is the authoritative in-repo doc. **Scope decision
  LOCKED (→ DECISIONS.md 2026-07-14): NO debt-per-parcel/neighbourhood map** —
  citywide debt isn't spatially attributable in public data. Two clearly-labelled
  components instead: (1) spatial growth-area financing transparency panel,
  (2) non-spatial citywide debt context. Framing = "financing transparency", NOT
  "debt attribution" — explicit in UI copy (load-bearing methodological claim).
  **Reachability probed 2026-07-14 (Oracle box):** doniveson.ca IIMP PDFs 200,
  open.alberta.ca FIR page 200 — D2/D5 data is Oracle-doable; only D0's bylaw
  map exhibit is edmonton.ca/laptop-gated.
  **⚠ INTERACTION PREREQ (all display tickets D1–D5-chart):** the app has **no
  sidebar** — there is no click→panel surface at all; interaction today is
  hover-tooltips only (S54 learning). Every "sidebar entry / extend the existing
  sidebar UI" phrasing below is aspirational shorthand from the brief, NOT an
  existing surface. **A new click→panel interaction must be designed and decided
  (Peter's call) before any D-series display work can start.** Read the phrasing
  below as "which content goes in that panel", not "add to a panel that exists".
  Tickets, build order:
  - [x] **D0 — catchment polygons BUILT 2026-07-15** (approximate, reviewable).
    `data/levy_catchments.geojson` (10 units) via
    `scripts/build_levy_catchments.py`; QA overlay + area validation confirm the
    footprints match Schedule A. Two flags for a future reviewer (editable
    `CATCHMENT_HOODS` dict): **Blatchford under-covers** (catchment > mapped
    hood) and **Riverview 1.65** (maybe drop `RIVER'S EDGE`). Full writeup:
    `docs/FINDINGS_offsite_levy_catchments.md`. Detail below ↓
  - [ ] **D0 detail — catchment polygon acquisition (RISK — source resolved
    2026-07-15; approach was Peter's call).** The 12 fire-hall off-site levy
    catchments (names/costs/rates tabled in the brief). Probed 2026-07-14:
    **NOT on data.edmonton.ca** (Socrata catalog: zero hits) **nor ArcGIS Hub**
    (every "off-site levy" layer there is Calgary's).
    **RESOLVED 2026-07-15 (laptop):** the ONLY published boundaries are a raster
    map exhibit — **Schedule A of Bylaw 19340** ("Fire Halls with Catchment
    Boundaries"), a JPEG in the bylaw PDF. **No GIS vector layer exists anywhere.**
    Bylaw text confirms boundaries are advisory ("subject to change… may adjust
    and refine over time"). Source artifacts saved to
    `data/raw/offsite_levy/` (bylaw PDF, ScheduleA JPEG, 2026 approved rates).
    Key enabling finding: Schedule A's catchment edges **follow the neighbourhood
    grid**, and all 12 catchments map to clusters of neighbourhoods we already
    hold in `neighbourhoods.geojson` (e.g. Blatchford→`BLATCHFORD AREA`,
    Walker→`WALKER`, Cumberland→`CUMBERLAND`, Big Lake→`ANTHONY HENDAY BIG LAKE`,
    Horse Hill→`ANTHONY HENDAY HORSE HILL` + the Horse Hill district). Three
    paths, decreasing effort / fidelity:
    1. **Trace/digitize** the raster (georeference + hand-trace 12 polygons) —
       highest fidelity, most manual; boundaries are advisory anyway.
    2. **Neighbourhood-union approximation** (RECOMMENDED) — build a
       neighbourhood→catchment assignment table by reading Schedule A, then
       dissolve. Reproducible from data we own, honest ("approximated to
       neighbourhood boundaries"), aligns with our neighbourhood-unit pipeline;
       error small because edges follow hood lines.
    3. **Table only** — per-catchment table + text list of member hoods, no map
       layer. Lowest effort, still honest, loses the spatial punch.
  - [ ] **D1 — levy performance mini-viz.** Cumulative levy collected vs the
    ~$26M single-facility cost, per catchment (simple bar/ratio — makes the gap
    immediate). Figures in the brief (2022–2024 annual reports; cumulative
    $3.83M end-2024, **zero halls levy-funded**). Use the 2024 **Table 6.1**
    figure ($3,033,592), footnote the exec-summary discrepancy ($3,259,866).
    Headline finding to make visually obvious: **Edmonton levies developers for
    fire halls ONLY** — no trunk roads/water/sanitary/storm levy (vs
    Calgary/St. Albert $170K–$270K/ha) — "1 of 5 essential services levied".
    Small manual dataset → reviewed JSON input (mill-rates pattern).
  - [ ] **D2 — IIMP financing split** (extends the Decoteau/HHR/Riverview
    annotation item above — primary source now located, Oracle-reachable). Add
    the developer-vs-City split to the Decoteau/HHR/Riverview click→panel content:
    developer $3.806B (drainage $2.351B + transportation $1.455B) vs
    City/Province $1.362B, net ~$1.4B 50-yr shortfall — 2016 projections,
    **label as projection, not actual**. **Needs the click→panel interaction
    decided first (see INTERACTION PREREQ above) — no sidebar exists yet.**
  - [ ] **D3 — Blatchford contrast case study.** 4th panel entry, same content
    pattern: the infill counter-example to the 3 greenfield areas —
    self-liquidating "debt recoverable" financing (Policy C597A), DESS
    district energy, $23.7M federal SREPs grant, own levy catchment
    ($32,813/ha, already in the D0/D1 table).
  - [ ] **D4 — sanitary trunk callout** (one-line panel text, NOT mapped —
    no clean basin boundaries confirmed): SSTC/EA charges paused May 2024;
    growth trunk sanitary currently funded from the accumulated ratepayer
    reserve, not active growth charges (figures in the brief).
  - [ ] **D5 — Component 2: citywide debt context chart (non-spatial).**
    Separate panel/chart, labelled "citywide, not neighbourhood-specific" —
    never a map layer. Headline 2025: $4.6B outstanding, 69% of the
    tax-supported debt-servicing limit (DMFP ≤18%/≤21% limits in the brief).
    - [x] **Data layer DONE 2026-07-14**: `scripts/fetch_fir_debt.py` →
      committed `data/fir_debt_series.json` — Edmonton + St. Albert +
      Strathcona County, **2003–2025** (a year further than the brief
      expected: the 2025 FIR is out, Edmonton total debt $4,592,150,000 =
      the brief's "$4.6B" headline, directly sourced). All four Schedule AA
      fields (debt + limits + servicing). Manual-reviewed-input pattern;
      anchor cross-checks + neighbour-band sanity; Strathcona-2013 $000s
      source quirk corrected + documented. DATA.md §11. +10 pytest (328).
      NB the FIR limit is the MGA regulation limit — Edmonton 2025 = 59.3%
      of it; the brief's "69%" is the DMFP servicing limit, a different
      denominator (quirk documented in §11).
    - [ ] **Display/chart** — undecided design (where does a non-map panel
      live in the UI?); Peter's call before building.
  - **Out of scope (locked in the brief):** any spatial allocation of the
    $4.6B; S&P rating detail / CCBF/MSI/LGFF; Local Improvement levies
    (genuinely parcel-level but not open data — future phase, needs
    FOIP/per-bylaw scraping).

- [ ] **Services lens — road supply (SPEC'd 2026-07-01, branch `feature/services-lens`).**
  Spec: `docs/SPEC_services.md`. V1 = `road_m_per_acre` (city-maintained
  **collector + local** centreline metres per boundary acre; per-class columns
  kept internally, arterials computed but excluded from the metric); V2 fast
  follow = revenue per road-metre. Locked: alleys OUT, arterials OUT (shared
  infrastructure), railway OUT, City-owned only.
  Build order:
  - [x] ~~Prerequisite commit: `$limit` count-vs-limit assertion in
    `scripts/download_data.py` + add roads source `9j8t-zm52`~~ — done
    2026-07-01 (closes the data-integrity §5 follow-on below); roads
    downloaded + verified (53,720 features, check passes).
  - [x] ~~`src/load_roads.py` + synthetic tests~~ — done 2026-07-01 (13 tests;
    real data: 3,644 km collector+local in metric, 0.28% unassigned).
  - [x] ~~Wire `join_and_calculate` (`ROAD_COLUMNS`) + `main.py` flags~~ — done
    2026-07-01 (+4 tests; GeoJSON regenerated, `road_m_per_acre` on all 406).
  - [x] ~~Skew check on `road_m_per_acre` → pick colour transform~~ — DECIDED
    2026-07-01: **linear** (raw skew −0.29; sqrt/log over-correct; FINDINGS §6.3).
    Clamp ≈ p97.5 = 53 m/acre.
  - [x] ~~Frontend: third metric in the Revenue/Value toggle~~ — done 2026-07-01
    (per-metric transforms, linear roads, button hides on pre-services data,
    headless-verified; set-aside grey kept per the v1 lean).
  - [x] ~~Docs: `DATA.md` §6, `ARCHITECTURE.md` module entry, status.json
    vintage~~ — done 2026-07-01. Resolution on vintage: **no roads year field**
    — the network is a live feed with no roll-year semantics; provenance =
    `last_checked` (recorded in SPEC_services + DATA.md §6).
  - [x] **Display pivot (2026-07-01): two-plane stackable architecture — COMPLETE
    2026-07-02** (SPEC_services.md "Display architecture — REVISED"; final control
    model = three discrete views **Money | Roads | Ratio**, UI.md "Services
    views"). Road prisms RETIRED; staging as executed:
    - [ ] (1) Roads ground layer:
      - [x] ~~pipeline: slim `web/data/roads.geojson` export (dissolved per
        hood × arterial/access, simplified 8 m, 5 dp)~~ — done 2026-07-02
        (`export_roads_web` in `src/load_roads.py`, wired into `main.py`;
        791 features, 2.3 MB, committed like the polygons file; +5 tests).
      - [x] ~~frontend: layers panel, lazy-loaded ground layer; arterials
        neutral, access roads coloured by hood `road_m_per_acre` (linear,
        clamp 53); remove Roads from metric toggle~~ — done 2026-07-02
        (headless-verified; details in UI.md "Services views").
    - [x] ~~(2) Prism transparency control (money plane overlays service
      plane)~~ — done 2026-07-02, landed with stage 1: opacity slider in the
      layers panel (prisms + roof edges) + 45% auto-nudge on first Roads
      enable — needed because the network is ~invisible under opaque prisms
      (only setback gaps show).
    - [x] ~~(3) Ratio view: revenue vs total services (revenue-per-road-metre
      is the single-service case — subsumes the old V2 item)~~ — done
      2026-07-02 as the **Ratio view** (Money | Roads | Ratio buttons;
      ghost prisms of $/road-metre over the neutral network; log colour
      FINDINGS §6.4; road-base floor 5 m/acre greys artifacts; UI.md
      "Services views"). "Total services" DEFINITION: DECIDED 2026-07-10 —
      stays per-service (denominator picker; SPEC_utilities decision 3);
      the V2 unit-cost composite is tracked under "More service layers".
  - [x] ~~Merge `feature/services-lens` → master via PR once Peter's eyeballed
    it~~ — done 2026-07-02: PR #8 merged, refresh workflow run green, live site
    verified serving the three views + roads.geojson.

- [ ] **DEVELOPMENT & INFILL LENS family (NEW 2026-07-12 — full plan in
  **⚠️ Stock age was WITHDRAWN from this lens 2026-07-27** (Peter: not
  working well as an option) — see `DECISIONS.md`. The UI and render path
  are gone and `verify-age-spikes.js` is deleted, but `median_year_built`
  still ships in `value_grid.json` and
  `FINDINGS_stock_age_spike_scaling.md` still holds the scaling work, so
  a different presentation would not start from zero. Anything below that
  assumes a 3-way Detail selector is stale.
  `docs/SPEC_development.md`).** Permit-based "where is building actually
  happening" lens family, the direct answer to what `FINDINGS_growth_servicing.md`
  could only proxy with median building-stock age. Data verified live 2026-07-12:
  General Building Permits `24uj-dj8v` (243k rows, 2009→now; has `units_added`,
  `work_type` new-vs-reno, `building_type`, `neighbourhood` UPPERCASE-matches-ours,
  lat/long, `construction_value`). Build one minimal cut of each lens to *see it*
  before designing the next. Three locked decisions (Peter, 2026-07-12) →
  DECISIONS.md: (1) activity = choropleth, (2) infill = suitability×activity
  mismatch shown both ways, (3) combined cost side = city service cost (not
  permit construction_value).
  - [x] **Lens A — Building Activity (choropleth), PHASE 1 / first cut. DONE
    2026-07-12** (`feat/dev-lens-a-building-activity`). `src/load_permits.py`
    (slim `$select` download, count cross-check hardened for the `count_1`
    alias) → new-construction `work_type` ∩ residential `building_type`
    (hand-enumerated dicts incl. every spelling variant, warn-on-unseen) → Σ
    `units_added` per hood → `join_and_calculate` column (`validate="m:1"`,
    warn-not-fail) → new **Development** web view (own view, NOT a city service;
    `new_units_per_acre`, 2021–2025 pinned, sqrt colour). **Set-aside override
    LOCKED = full override coloured** (empirically low-impact: 6 hoods/43 units;
    growth hoods sit below the 0.90 threshold — the S42 "headline tension" was
    overstated for current data). `NAME_CORRECTIONS` resolves CHAPPELLE AREA etc.
    (only GLENORA,ROSSLYN 1-unit straggler left). DATA.md §10 added; 308 pytest +
    `verify-development.js` 25/25 green; screenshot eyeballed. Live-data: 59,696
    units / 236 hoods, GARNEAU tops per-acre (dense infill).
    - [x] **Lens A polish — permit-count sub-metric** (2026-07-13): pipeline
      `new_permits_per_acre` column + web `#devmetric` units/permits picker
      (project density vs dwelling supply); ABBOTTSFIELD 248 units / 2 permits is
      the extreme case. 308 pytest + `verify-development.js` 31/31 green.
    - [x] **Lens A polish — window toggle** (2026-07-13): second pinned window
      `PERMIT_YEARS_RECENT` (3yr, 2023–2025) alongside the 5yr base →
      `_3yr`-suffixed columns + web `#devwindow` 5yr/3yr picker (both metrics),
      gated on the `_3yr` columns. 311 pytest + `verify-development.js` 40/40 green.
    - [x] **Lens A — long "Since 2009" window** (2026-07-21, from the inspiration
      lens = cumulative "homes added 2009–2023" density-in-the-core map): third
      `#devwindow` option (2009–2025), `PERMIT_YEARS_LONG` → `_long` columns for
      all three metrics. ANCHORED (2009 start pinned, end derived from
      `PERMIT_YEARS[-1]` → auto-extends on the January bump). ~160k units citywide
      vs 60k/39k. **First-class window** (2026-07-22): drives the choropleth AND
      its own 100 m detail-grid spikes (`units_long` cells) — the initial
      choropleth-only cut was reverted once the data showed early-year geocoding
      is fine (2009–2023 at 95–98%; the lag is the NEWEST permits, so the long
      grid is the best-covered of the three at 84%). DECISIONS + SPEC_development
      "Activity window" + DATA.md §9. 402 pytest + `verify-development.js` (+11
      long-window checks incl. the long detail grid) + age/ind regressions green;
      choropleth + spike-map screenshots eyeballed.
    - [x] **Lens A 100 m detail grid** (2026-07-15, Peter: "add them as a layer
      switch this time... may want to move the others to this style later"):
      layers-panel "Detail" toggle in the Development view swaps the choropleth
      for the Glass composition — neutral plane + 100 m geocoded-permit spikes
      (`load_permits.export_dev_grid` → `web/data/dev_grid.json`, 4,105 cells;
      permits `$select` now fetches lat/long). Linear height / sqrt colour,
      driven by the existing pickers; geocode-lag coverage (~21% of 5yr units
      not yet mapped) written into the JSON + disclosed in the blurb.
      DECISIONS 2026-07-15; SPEC_development "Lens A detail grid";
      verify-development 54/54; +6 pytest (334).
    - **Lens A polish (remaining):** the `occupancy_granted_date` completed-builds
      variant (DATA.md §10 — only populated residential ≥2022 / non-res ≥2024).
  - [ ] **Lens B — Suitability × Activity mismatch, PHASE 2.** Signed diverging
    metric `z(suitability) − z(activity)`: two views off one scale — suitable-
    but-quiet (opportunity) AND less-suitable-but-building (Peter's flip).
    - [x] **Suitability proxy LOCKED 2026-07-13 (Peter): built FAR** (`far` = Σ
      floor area ÷ deduped lot area/hood; low FAR = underused). Backend column
      DONE — `load_property_info` loads `gross_area`, `build_hood_lot_acres`
      emits `far`, `join_and_calculate` carries it into geojson + SLIM
      (unsuppressed by LOW_PARCEL_FRAC); +7 tests, 318 green. DECISIONS.md +
      SPEC_development Lens B + DATA.md §2.
    - [x] **Web `Infill` diverging view DONE 2026-07-13:** `z(suitability) −
      z(activity)` = `−(z(far)+z(activity))` computed live (responds to the
      units/permits × 5yr/3yr pickers); one dark-centred diverging plane (teal =
      suitable-but-quiet, orange = building-where-less-suitable), set-aside
      EXCLUDED from the z population (358 hoods kept). DECISIONS + SPEC_development.
    - [x] **Asymmetric residential opportunity gate DONE 2026-07-13:** a prototype
      showed the planned maturity gate (median `year_built`) DOESN'T fix the
      opportunity end — the pollution is structurally-low-FAR *non-residential*
      land (industrial/fringe, all decades), not new suburbs. Fix: non-residential
      hoods barred from the teal opportunity end (grey) but kept on orange/pressure
      + in the z population (keeps DOWNTOWN). Web-only, no new pipeline column
      (`infillOppSuppressed`). `verify-infill.js` 41/41. DECISIONS + SPEC_development.
    - [x] ~~**Lens B per-arm colour scaling (REOPENED 2026-07-14, handed to Fable).**
      S48 audit: the mismatch score is structurally asymmetric (suitability capped
      +0.97, activity unbounded) so the symmetric p95 clamp leaves the teal arm
      unable to saturate (0 teal vs 18 orange saturations) + median hood on the
      +0.5 verdict line. Fix (web-only): clamp each arm at its own p95 + verdict
      cut-points in `t` space. Brief: `docs/FABLE_infill_perarm_scaling.md`~~ —
      done 2026-07-14 (Fable): `clampPos`/`clampNeg` in `infillStats`, per-arm
      `infillT`, verdict cut at `t = ±0.4`; `verify-infill.js` 44/44; live on the
      next `refresh.yml` run.
    - [ ] **Lens B optional refinement (future, low priority):** one-sided
      opportunity/pressure choropleth toggles (the single diverging map already
      shows both). SPEC_development Lens B.
    - [ ] **Lens B fine-grain "Infill detail" (assessed 2026-07-14, not yet
      decided):** the z-mismatch SCORE doesn't survive 100 m grain (~88% of
      inhabited cells have zero 5yr activity — every quiet cell would read
      "opportunity"; set-aside/residential gates are hood-level constructs).
      The honest fine-grain version is the DECOMPOSED ingredients: a per-cell
      FAR texture (per-point `gross_area` + `_point_lot_stats` lot dedupe —
      `build_hood_lot_acres` keyed on cell instead of hood) under the Lens A
      permit spikes (now shipped), verdict stays hood-level. Middle path if a
      finer score is ever wanted: prototype 250–500 m cells first. Needs
      Peter's call before building.
  - [ ] **Lens C — Activity vs City Service Cost, PHASE 3 / future.** Where new
    building goes vs modeled city service columns (road/storm/water/fire per acre)
    or V2 unit-cost $/acre (laptop-gated). Two-ledger idiom of
    FINDINGS_growth_servicing made spatial. `construction_value` NOT used here.
    Depends on Lens A + V2 unit costs.

- [ ] **Views & lenses follow-ons (Peter, 2026-07-02).** Three asks on top of the
  shipped Money | Roads | Ratio views:
  - [x] ~~**Residential-only lens in the Ratio view.**~~ — done 2026-07-03:
    non-residential kept hoods fade to the lens grey (height untouched), log
    colour anchors rescale to the residential kept subset (≤ $258 … $916+ vs
    $264 … $3,253 — FINDINGS §6.4 addendum), lens button disables in the Roads
    view (state persists). Headless-verified (`tools/profiling/verify-lens.js`
    + screenshot); UI.md updated. **PR #9 merged + deployed** (run 28646374983;
    deploy step needed one transient-error rerun); live site verified serving
    the new code.
  - [ ] **More service layers (water / drainage / transit / …).** Each needs its
    own SPEC_services section (dataset, filters, locked decisions), a
    per-hood supply column, and a slim web export.
    - [x] ~~**Transit lens**~~ — BUILT 2026-07-11 (Peter's call, AMENDS the
      2026-07-09 release-scope lock that kept transit out): mean-weekday
      scheduled GTFS stop-events/acre (`transit_dep_per_acre`, sqrt colour
      FINDINGS §6.8), Services-view checkbox + 58 LRT-station/transit-centre
      dots, five new weekly GTFS downloads. SPEC_services "Transit lens",
      DATA.md §9. Scheduled supply, NOT ridership (none exists stop-level);
      current-signup seasonality is the standing caveat.
      - [x] ~~**LRT track lines** context layer~~ — added 2026-07-11: the
        operating network (Capital/Metro/Valley) as a `PathLayer` under the
        station dots (`rpjw-4jft` "LRT Routes" → `web/data/lrt_lines.json`,
        343 segs); the HER heritage streetcar is excluded (not ETS LRT
        service). Not part of the metric. DECISIONS.md 2026-07-11.
    - [x] ~~**Services-view UI generalization**~~ — **SHIPPED 2026-07-05:
      PR #14 merged + deployed + LIVE** (run 28767241818 — deploy step
      needed two transient-error reruns, "Deployment failed, try again
      later"; live verified serving the Services button + storm column on
      all 406 hoods; CI regenerated the geojson byte-identical). The Roads
      view is now a "Services" view with per-service checkboxes (Roads,
      Stormwater; Fire added 2026-07-06) and a "colour" radio choosing which checked
      service drives the ramp (others render neutral; defaults = the old
      Roads view exactly). Headless-verified
      (`tools/profiling/verify-services.js` + regressions green) +
      screenshots (`shot-services.js`) + Peter's on-device eyeball. Display
      detail: UI.md "Services views".
    - [x] ~~**"Total services" / Ratio-view denominator reopen**~~ — **DECIDED
      2026-07-10 (Peter) + V1 BUILT same day** (branch
      `feature/ratio-denominator-picker`): the ratio stays **PER-SERVICE** —
      a "Ratio denominator" picker (revenue per road metre | per fire
      event) in the Ratio view. Modeled EPCOR dollars (storm/water) are
      excluded from any levy ratio by the money-flow honesty rule (they'd
      compare unrelated flows / cancel if added to both sides) — so the
      "two dollar services" trigger resolved to per-service, not a $ sum.
      Fire floor 0.005 events/acre/yr + log colour: FINDINGS §6.7;
      SPEC_utilities decision 3 holds the full design; headless-verified
      (`verify-ratio-denom.js`, 27 checks) + regressions + screenshots.
      Also fixed in passing: `verify-labels.js` still clicked the retired
      "roads" view button (stale since the 2026-07-05 generalization).
      **PR #33 merged (`e0da845`) + deployed 2026-07-10** (refresh run
      29099791508 green → auto-refresh `e8f58b4`; github-pages deploy
      success; live-verified 27/27 vs the Pages URL).
    - [ ] **V2 — combined "modeled city service cost per acre".** One
      denominator = road metres × roadway O&M+renewal $/m/yr + fire events ×
      (Fire Rescue operating budget ÷ citywide dispatches). Labeled MODELED,
      "roads + fire only", never "total city cost". Design locked in
      SPEC_utilities decision 3.
      - [x] **Unit-cost source hunt DONE 2026-07-15 (laptop)** — the
        laptop-gated half. `data/city_unit_costs.json` (reviewed input,
        mill-rates pattern): **roadway $50/m/yr** (edmonton.ca Development
        Impact page: $600k O&M + $1.9M renewal per km ÷ 50-yr life; Peter's
        50-yr call; 3%-of-value cross-check ≈ $45) + **Fire Rescue 2026 gross
        operating budget $276.706M** (2026 Approved Operating Budget PDF; net
        $273.598M). Provenance + caveats in the JSON.
      - [x] ~~**Build the composite metric (Oracle-doable).**~~ — done
        2026-07-15: `load_unit_costs` + `unit_costs` arg in
        `join_and_calculate` → `svc_cost_per_acre` = road_m_per_acre ×
        $50/m/yr + fire_events_per_acre × (budget ÷ the fire frame's OWN
        citywide kept-event total, pre-join — unmatched fire hoods stay in
        the denominator). Requires BOTH roads + fire (warn+skip otherwise —
        a one-term composite would be mislabeled). In `SLIM_COLUMNS`, so
        the column ships with the next refresh run (code-only PR; the
        local raw snapshot is older than the live auto-refreshed data,
        so no regenerated GeoJSON was committed). +9 pytest (351).
        Real-data run verified: **$3,142/event** ($276.706M / 88,065 kept
        events/yr), composite on all 406 exported hoods, median
        $3,302/acre/yr (fire-dominated downtown ~$34k, road-dominated
        suburbs ~$3.4k — the allocation caveat is visible in the data).
      - [ ] **Display (UI) for the composite** — **DECIDED 2026-07-16
        (Peter): BOTH, staged** (Services checkbox first, then a Ratio-view
        coverage denominator). Carry the fixed-budget-allocation + "roads +
        fire only, never total city cost" caveats in copy.
        - [x] ~~**(a) Services-view checkbox**~~ — BUILT 2026-07-16
          (`feat/v2-svc-cost-display`): 6th per-service row "Service cost
          (roads+fire) — modeled $/acre" on the shared `svc-plane` (SERVICES
          `servicecost`, sqrt colour), blurb + legend + tooltip with both
          caveats, column-guarded (hides until the column ships on the next
          refresh). `verify-services.js` + `shot-services.js` extended;
          screenshot eyeballed (fire-heavy core bright, greenfield grey).
        - [x] ~~**(b) Ratio-view coverage denominator**~~ — BUILT 2026-07-16
          (`feat/v2-svc-cost-display`): 3rd "Ratio denominator" option "Per
          service $" = revenue ÷ modeled roads+fire cost (dimensionless).
          **Magnitude, not break-even (Peter): same log ramp, no 1.0
          marking; median ≈5.8× so blurb/tooltip own "not a sign the land
          pays its full way".** ×-format legend bounds, $230/acre floor,
          picker opens on hasFire||hasSvcCost, button column-guarded.
          verify-ratio-denom 38/38; screenshot eyeballed.
    - [x] ~~**Fire lens**~~ — **BUILT 2026-07-06** (design DECIDED 2026-07-05,
      Peter, all four recommendations: demand metric events/acre/yr as the
      Services ground plane + 31 station dots; all emergency responses minus
      operational noise, medical share a caveat NOT a filter; 2023–2025
      averaged, pinned `FIRE_YEARS`; built after the Services UI landed).
      As built (branch `claude/session-summary-review-vwweia`):
      `src/load_fire.py` (+21 tests) + `download_data.py` sources
      (`7hsn-idqi`, `b4y7-zhnz`) + `join_and_calculate` FIRE_COLUMNS →
      `fire_events_per_acre` in SLIM_COLUMNS + `main.py --skip-fire` +
      third Services checkbox (shared `svc-plane`, station dots,
      demand/medical caveats) + verify-services/shot-services extended.
      209 pytest green; headless-verified against a SYNTHETIC fire column.
      Dataset facts: DATA.md §7–8; spec: SPEC_services "Fire lens".
      **Remaining follow-ups (blocked on network access to
      data.edmonton.ca — the build session's VM policy denied it):**
      - [x] ~~First real-data run~~ — DONE 2026-07-06 (Session 18, Oracle
        server): `dispatch_datetime` resolved as the first exact candidate
        (186 of 948k unparseable); mix verified (MEDICAL 60%, 4,025 noise
        excluded, 88,065 kept events/yr / 408 fire hoods). Caught + fixed
        TWO real-data bugs: PR #17 (event_type_group carries CODES — filter
        on event_description) and PR #18 (`FIRE_NAME_CORRECTIONS`: fire CSV
        still says OLIVER for WÎHKWÊNTÔWIN, 1,476 events/yr displayed as 0;
        + 3 "AREA" collapses). Live-verified: plane + 31 dots + tooltip.
      - [x] ~~Colour transform check on real `fire_events_per_acre`~~ —
        DECIDED 2026-07-06: **sqrt** (raw skew +7.86, the project's worst;
        clamp/median 5.8×; linear crammed 59% of hoods into the ramp's
        bottom fifth; log undefined on the 5 zero hoods. FINDINGS §6.5).
      - [ ] **January task**: bump `FIRE_YEARS` (main.py) AND the
        2023–2025 wording in the fire blurb + legend (`web/index.html`).
    - [ ] **Utility cost lenses — SPEC'd 2026-07-05 (`docs/SPEC_utilities.md`);
      stormwater DECIDED first (Peter) and its v1 PIPELINE BUILT same day on
      `feature/stormwater-lens` (unmerged).** Five candidates in three
      fidelity tiers, from Peter's methods doc
      (`docs/utility_cost_estimation_lens_methods.md` — verified 2025/2026
      tariffs; rate numbers live there). All outputs MODELED, not billed.
      - [x] ~~Stormwater pipeline (Lens 1)~~ — built 2026-07-05:
        `src/load_stormwater.py` (bylaw A×I×R per point; `ZONE_RUNOFF`
        explicit dict; condo dedupe reused; fixa-tstc zone fallback) +
        year-keyed `data/stormwater_rates.json` + join/main wiring +
        19 tests (182 green). Real data: 287,103/287,163 points, citywide
        $240.4M/yr (2025 rate), ranking sanity passes (industrial top,
        river valley bottom). As-built numbers + caveats: SPEC_utilities
        Lens 1 (serviced-area assumption is the big one — EETP fringe = 5%
        of the total; AG runoff coded 0.1 with VERIFY flag).
      - [x] ~~**Display shape**~~ — DECIDED (Peter; SPEC decision 2) and
        **SHIPPED 2026-07-05 (PR #14, with the Services-view item above)**:
        per-hood ground-plane layer in the generalized Services view —
        linear colour, clamp p97.5 of non-set-aside hoods (≈ $2,700,
        runtime), set-asides grey, legend + blurb labeled MODELED /
        "modeled, not billed"; `storm_charge_per_acre` added to
        `SLIM_COLUMNS` (hood GeoJSON 0.7 MB, all 406 hoods carry it).
        Pipeline PR #13 merged first, as sequenced.
      - [x] ~~Water + sanitary (Lens 2)~~ — BUILT 2026-07-07 (Session 18,
        branch `feature/water-lens`; decisions locked with Peter
        2026-07-06: residential+multi-res scope, two columns, colour by
        TOTAL): `src/load_water.py` (per-connection model — roll points
        as connections, meter-size bands, inclining/declining blocks) +
        `data/water_rates.json` (Apr 2026 tariffs; `WATER_RATE_YEAR` pin)
        + join/main wiring + fourth Services checkbox (LINEAR colour,
        FINDINGS §6.6; tooltip fixed/total split). Real run: 268,489
        connections / 551,831 modeled households, citywide $588.1M/yr
        ($133.9M fixed). 229 tests green; headless-verified on real data.
        As-built numbers + caveats: SPEC_utilities "Lens 2 as built".
        Follow-ups: household count ~20% over census (floor-area→units
        assumption — [x] ~~sensitivity-check M2_GROSS_PER_UNIT~~ DONE
        2026-07-07: 70–120 m²/unit sweep moves households ±7% but citywide
        $ only ±5% — the assumption is NOT the source of the EPCOR gap;
        90 baseline stands. `tools/sensitivity_m2_per_unit.py` +
        FINDINGS_utility_validation §2.1); validation vs EPCOR revenue
        (below, now covers water too).
      - [x] ~~Validation pass vs EPCOR published revenue~~ — DONE
        2026-07-07 (Session 19), full numbers + sources in
        `docs/FINDINGS_utility_validation.md`. **Order-of-magnitude PASS
        both lenses.** Stormwater: $240.4M modeled vs $141.1M published
        2025F (1.70×), but residential slice is 1.11× and the excess is
        localized (notyet+never zones = $49.8M unbilled land; I=1.0 vs
        real DIF reductions on commercial). Water/sanitary: $588.1M vs
        ≈$467M published res+MR scope (≈1.26×); connection count 13%
        UNDER EPCOR's (268k vs 308k accounts) — excess is per-connection.
        [Refined 2026-07-07: the in-city water res+MR share was a flat ~70%
        guess; now derived to ~80% from EPCOR's by-class customer+consumption
        counts (EWS 2024 PBR Progress Report p.9, FINDINGS §2.2), tightening
        the ratio 1.33×→1.26×. The raw water revenue-by-class schedule stays
        unreachable (all edmonton.ca public-files paths dead, no Wayback), so
        ~80% is a blend estimate, not a read-off — but a well-anchored one.]
      - [x] ~~**Peter decision (bracket quantified, FINDINGS §3)**~~ —
        DECIDED 2026-07-07: report BOTH (all-parcels $240.4M AND excl
        notyet+never zones $190.5M). Shipped same day:
        `UNBILLED_CATEGORIES` in `src/load_stormwater.py` — log line +
        `.attrs` carry both totals; per-hood outputs unchanged
        (reporting, not modeling). 230 tests green; real-data verified.
      - [x] ~~Lenses 3–4 (electricity/gas franchise)~~ — BUILT 2026-07-07
        as **columns only, no display layer** (Peter's call: they're
        collinear with dwelling count — flat per-dwelling proxy makes every
        column `dwellings × constant`). `src/load_franchise.py` reuses
        `load_water.build_connections` (extracted shared helper → ONE
        551,831-dwelling model) + `data/franchise_rates.json` + join wiring
        (`FRANCHISE_COLUMNS`, out of SLIM) + `--skip-franchise`; 8 tests
        (238 total). Real run: **$162.6M/yr modeled City revenue** (elec LAF
        $36.9M + gas franchise $125.7M). Modeled LAF ~⅓ low vs published
        $8.33/mo (base schedule vs full distribution revenue — documented).
        As-built + validation: SPEC_utilities "Lens 3+4 as built" +
        FINDINGS_utility_validation §5. Follow-ups: (a) ~~validate vs City
        budget franchise line~~ **DONE 2026-07-07** — vs Note 24 of the 2024
        Financial Annual Report (audited): combined elec+gas modeled $162.6M
        vs actual $175.9M = **0.92×**, but two offsetting errors — gas 1.32×
        over (Rider T in the 35% base; excl → 1.00×), elec 0.46× under (LAF
        floor). FINDINGS §5.1; (b) commercial scope needs a consumption proxy;
        (c) display lens if ever wanted.
      - [ ] **DEFERRED (Peter, 2026-07-07 — revisit later): exclude
        transmission Rider T from the gas franchise base?** Validation §5.1
        found modeled gas franchise ($125.7M) exceeds the all-sector City
        actual ($95.2M) at 1.32×; dropping Rider T ($1.357/GJ) from the 35%
        base → $95.6M ≈ 1.00×. One-line change (`gas_rider_t_per_gj` already
        isolated in `franchise_rates.json`). NOT proven — residential-only
        matching an all-sector actual could be a compensating 115 GJ/dwelling
        overcount. Parked as-is with the Rider-T caveat documented; no model
        change for now.
      - [ ] Remaining SPEC open decisions: (3) modeled $ in the "total
        services" denominator (recommended: not yet); (4) franchise-fee
        revenue columns only with their lenses — SETTLED (columns only,
        built above).
  - [x] ~~**Use-mix view: surface each neighbourhood's zoning composition.**~~
    **SHIPPED 2026-07-03 — PR #10 merged + deployed** (run 28679596055, green
    first try); live site verified serving the Uses view + `zoning.geojson`
    (200, 1.17 MB). Shows what the land IS (res / com / ind / mixed / DC /
    institutional / reserve), not what it yields. **Decisions (Peter,
    2026-07-03):** nonres split 4 ways `com`/`ind`/`mix`/`dc` — DC its own
    category (24% of nonres area, bespoke bylaws, can't honestly fold
    elsewhere); a **fourth view button** Money | Roads | Ratio | Uses; real
    bylaw geometry (clipped to the 45 m hood setbacks) rather than
    dominant-colour hoods; tooltip = dominant use + stacked composition bar.
    Sub-items below record the build trail.
    - [x] ~~Pipeline prerequisite: split `ZONE_CATEGORY` + export the full
      composition~~ — done 2026-07-03: 39 nonres codes re-tagged (ambiguous
      names resolved from bylaw purpose statements — UW/HA/MMS → mix, BE →
      ind, MED/AED → com; DATA.md §5); unknown codes now default to `other`
      (not `nonres`); `ZONING_COLUMNS`/`SLIM_COLUMNS` extended with all 9
      fracs; GeoJSON regenerated (0.68 MB, fracs sum to 1 on all 406, 48
      set-aside / 226 residential unchanged; +4 tests, 135 green).
    - [x] ~~Frontend: "Uses" view~~ — built 2026-07-03: fourth view button,
      flat categorical fill by dominant use, validated 7-hue palette + two
      neutral greys (UI.md "Uses view" — colours computed through the dataviz
      validator, min all-pairs CVD 10.6 w/ gap+tooltip relief), data-driven
      legend rows, composition tooltip, lens disabled in-view, old-data
      guard. Headless-verified (`tools/profiling/verify-uses.js`, 0/406 fill
      mismatches; `verify-lens.js` regression green) + screenshot.
      (Superseded same day by the real-geometry render below; the
      dominant-colour path remains as the fallback.)
    - [x] ~~Tooltip mini stacked composition bar~~ — done 2026-07-03 (Peter's
      ask): 190×8 px flex bar in the category colours above the composition
      text; `.tip` max-width 300px so long compositions wrap.
    - [x] ~~**Residential prisms over the Uses fabric** (Peter's ask
      2026-07-10: "how much residential is in each neighbourhood
      specifically")~~ — built 2026-07-10: layers-panel checkbox (default
      off), translucent sand prisms with height = `frac_residential` on a
      fixed 0–100% linear scale, peak deliberately 2.5 km NOT the 8.2 km
      parity height (bounded share clusters 40–95% → full parity renders a
      solid wall; screenshot-verified before lowering). Zero-share hoods
      omitted (z-fight), opacity on the shared prism slider (Uses default
      35%), labels ride roofs, blurb honesty line, state persists.
      Client-side only — `frac_residential` already served. Headless-
      verified (`verify-uses-prisms.js`, 20 checks) + full regression
      suite green + screenshots. Display detail: UI.md "Uses view".
    - [x] ~~Real zoning geometry IN the Uses view~~ (Peter's call — the
      dominant-colour render was "meh utility"; consciously reopened the
      "zoning polygon overlay" scope item for THIS view only) — done
      2026-07-03: `export_zoning_web` (citywide category dissolve, simplify
      10 m, grid-snap `set_precision` — plain rounding after the validity
      pass broke the browser tessellator; 8 features, 1.1 MB), wired into
      `main.py`; frontend lazy-loads it with dominant-colour fallback +
      hood-hover tooltips on top; legend now shows all 8 present categories.
      +4 tests (139 green); verify-uses.js + verify-lens.js green;
      screenshot eyeballed.
    - [x] ~~**land-use diversity analysis (Peter, 2026-07-03)**~~ — DONE
      2026-07-07 (Sessions 22 + 24). ANALYSIS_BACKLOG item 4, see
      `docs/FINDINGS_land_use_diversity.md`. Result: revenue/acre vs diversity
      holds under controls (partial r +0.27, n=299) but is secondary to density;
      road-per-dwelling vs diversity is a **null**. Prerequisite DC provision
      scrape (ANALYSIS_BACKLOG item 3) also DONE end-to-end (crawl→extract→
      classify→QA→rollup): the 918 DC provisions are use-classified
      (`data/dc_inferred_use.csv`), rolled up per hood
      (`data/dc_use_by_hood.csv`), folded into the index, and 8 of the 14
      previously-dropped high-`frac_dc` hoods re-admitted — both verdicts
      unchanged. Open upgrades: formal regression + p-values (needs `scipy`);
      `notebooks/exploration/` scatter version (deferred).
    NOTE: this is hood-level composition — it does NOT reopen the "full
    zoning polygon overlay" scope decision below; keep them decoupled.
    FINDING (for ANALYSIS_BACKLOG 1): the 8 dc-dominant hoods are the big-box
    power centres — South Edmonton Common, Terra Losa, Mill Woods Town Centre,
    Calgary Trail South, Summerlea, Place LaRue, McCauley, Strathcona Junction.

- [ ] **Residential-only lens (Phase 2 view — needs a pipeline extension first).**
  Goal: a UI filter that fades non-residential/downtown prisms so councillors see a
  pure residential-to-residential comparison (mature infill vs. greenfield suburb) —
  no class-rate differential or Downtown outlier confounding the scale. The narrative
  "third lens" after sqrt-colour (orient) + linear-height (the Downtown reveal), which
  the current single view already fuses.
  **Backend done (2026-07-01, commit `02704b6`)** — only the frontend remains:
  - [x] Split `dev` → `res` / `nonres` in `ZONE_CATEGORY` (by each code's
    `description`; 28 housing codes → res, 39 commercial/industrial/mixed/DC → nonres).
  - [x] Emit `frac_residential` + `is_residential` (≥0.50 of zoned area) per hood.
    Validated on real data: 226 residential, 0 overlap with set-aside.
  - [x] Added to `ZONING_COLUMNS` + `SLIM_COLUMNS`; regenerated GeoJSON carries both.
  - [x] Frontend filter (`web/index.html`): "Residential only" toggle fades
    non-residential hoods translucent (fill α70 / roof-edge α45 — **visible but
    see-through**, Peter's call), residential hoods keep full colour. Off by
    default; preserves metric/palette state. *(Not visually verified — no headless
    browser; preview `cd web && python -m http.server 8777`.)*
  Note: `is_residential` is a display filter, orthogonal to `is_set_aside` (grey);
  a set-aside hood is not residential. Keep the two flags independent.

- [ ] **Colour scale for revenue/value — decide after exempt split.** Current hard
  clamp ($50k / $4M, ~p97) creates a visible saturated plateau that reads as a fake
  threshold. Once exempt is split, re-run the skew check on the status-defined
  taxable set: if it's ≈ log-normal (likely), use `log` for the taxable scale; `sqrt`
  is the fallback if it stays mixed. Height stays LINEAR (locked honesty choice).
  *Colour ramps in `web/index.html`:* 3 swappable ramps (Inferno / Glow /
  Cividis) + palette switcher. **Default = Inferno (picked 2026-07-01).** Cividis
  retained in the switcher as a liked alternative + the colourblind-friendly
  option (see Visual polish → colourblind (cividis) mode below).
  *Not yet built:* scale toggle (linear+clamp / sqrt / log) for visual comparison.

- [ ] **Deployment follow-ons (deferred, see `docs/SPEC_deployment.md`):**
  - [x] ~~Year-mismatch **guard**~~ — built 2026-07-01 (`scripts/check_year_alignment.py`
    + `refresh.yml` wiring): detects the roll year from Socrata metadata; on mismatch
    skips regen, keeps serving committed data, auto-sets the holding banner. See
    SPEC as-built notes + `docs/FINDINGS_data_integrity_audit.md` §3.
  - [ ] Auto-**fetch** matching `pwis-wc4c` rates for a newly detected year (the
    guard detects + holds; it doesn't self-heal). Recovery is manual: bump
    `ASSESSMENT_YEAR`, extend `mill_rates.json`, update `generate_status.py` years,
    `--clear-banner`.
  - [ ] Per-year archive filenames (`web/data/YYYY.geojson`, keep-not-overwrite) for
    the future UI year selector.
  - [x] ~~**Heartbeat watch:**~~ DONE 2026-07-26 — didn't wait for it to sleep;
    added the repo-scoped PAT (with fallback) *plus* a client-side staleness
    banner. Same item as P2.2 above; see there for the remaining manual step.
  - [ ] Optional tidy: delete merged branches on origin (`feature/phase2-web`,
    `feature/deployment`, `chore/node24-actions`, and the three audit-session
    branches from 2026-07-01: `docs/data-integrity-audit-brief`,
    `fix/name-corrections-audit`, `feature/year-alignment-guard`).

- [ ] **Data-integrity audit follow-ons** (first run 2026-07-01, **second run
  2026-07-11** — see `docs/FINDINGS_data_integrity_audit.md`; second run covered
  all post-07-01 modules: roads/storm/water/franchise/fire/transit/lot-acre/grid.
  **No blocking findings; published numbers confirmed trustworthy.**):
  - [x] ~~**CI unmatched-set assertion (audit §4 / second-run T3c):**~~ DONE
    2026-07-11 — `scripts/check_unmatched_names.py` asserts the live money-path
    unmatched set == committed baseline `data/expected_unmatched.json`
    (`assessment_not_in_boundaries` = {OLIVER}, `boundaries_not_in_assessment` =
    {LEWIS FARMS}); wired into `refresh.yml` as a hard gate after download, before
    regen. A NEW assessment name with no boundary (silent dollar loss) FAILS the
    build (exit 5) → no wrong-data deploy, last-good data keeps serving. New
    boundary holes / resolved names → exit-0 warnings (update the baseline). +8
    tests. **Scope = the money path only** (the join that drops dollars); the five
    service frames (zoning/roads/storm/fire/transit/water) default unmatched to
    0/NaN — less catastrophic, still `join_and_calculate`-warned — so extending
    the guard to them is a possible future add, not done here.
  - [x] ~~**`validate="m:1"` on the `join_and_calculate` merges (second-run
    NEW-1):**~~ DONE 2026-07-11 — added `validate="m:1"` to all nine merges
    (base assessment + zoning/roads/storm/fire/transit/water/franchise/lot-acre);
    pandas now raises `MergeError` if a duplicate right-key ever appears instead
    of silently misaligning every per-acre denominator via the positionally-reused
    `safe_area`. +2 tests (`test_duplicate_assessment_key_raises`,
    `test_duplicate_roads_key_raises`). Pipeline reruns clean on real data (all
    nine pass validation). 277 pytest green.
  - [x] ~~**Socrata `$limit` truncation check (audit §5)**~~ — built 2026-07-01
    on `feature/services-lens` (`check_not_truncated()` in
    `scripts/download_data.py`, fails at count >= limit; +6 tests; roads
    source added in the same commit).
  - [ ] (Optional, fidelity) map `MA DERELICT RESIDENTIAL` to the dedicated
    "Mature Area Derelict Residential" rate class instead of "Non Residential" —
    identical municipal rate today, differs if `rate_type` ever changes (audit T1).

- [ ] **Visual polish** (pre-existing, untouched):
  - [ ] top-cap edge colour `TOP_EDGE_COLOR=[40,95,120,215]` in `web/index.html`
    ("not happy yet")
  - [ ] deferred zoom-out (~10.2→~9.4) + proportional `ELEVATION_SCALE` bundle
  - [ ] light mode + colourblind (cividis) mode

- [ ] **(Optional) exploration notebook** — work `FINDINGS_assessment_classes.md`'s
  "to visualize" list (value vs levy share by class; split-class distribution;
  per-neighbourhood exempt share). Notebooks go in `notebooks/exploration/`; per
  global CLAUDE.md, use the Jupyter MCP server tools, not NotebookEdit.

- [ ] **STAGE 2 of the `web/index.html` split — the JS into ES modules (NOT
  started, and deliberately deferred).** Stage 1 (CSS → `web/styles.css`) shipped
  2026-07-29, PR #116; see `DECISIONS.md` that date for the full reasoning.
  Remaining: ~3,300 lines of JS in one block with **nine existing section
  banners** (tunables, services lens, uses view, services view, base map,
  development detail grid, infill lens, reference layers, money view) — the
  structure is already latent, it just isn't expressed as files. Native ESM
  (`<script type="module">` + relative imports) needs no bundler and works on
  Pages.
  - ⚠️ **Do NOT justify this on token savings — that was measured and is false.**
    See `docs/TOKEN_EFFICIENCY.md` "Files to watch". Justify it on navigability,
    grep precision and blast radius, or not at all.
  - ⚠️ **`DEFAULT_BUILD` must stay in `index.html`** — `scripts/build_site.py`
    regexes it there and hard-fails on anything but exactly one match. If the JS
    moves, that literal stays behind or `build_site.py` moves with it.
  - ⚠️ **11 verify scripts reference `index.html` directly** — that is where the
    risk lives, and why this is a separate stage.
  - **Gate: wait until stage 1 has actually helped** (the mobile-chrome work in
    `MOBILE_USABILITY.md` §3 is the first real test of it). Don't do stage 2
    speculatively.

## Done

Closed items moved out of `## Open work` live in **`docs/TODO_archive.md`** — one line each below, reasoning there.

- [x] **CLOSED 2026-08-30 — the 15 hardcoded activity-window labels now read from one constant, and drift fails the build.** (Audit F4; the `status.json` route was rejected on measurement.) — CLOSED 2026-08-30 · `docs/TODO_archive.md`

- [x] **CLOSED 2026-08-29 — the three verify failures are resolved, and one of them was NEVER a master failure.** — CLOSED 2026-08-29 · `docs/TODO_archive.md`



- [x] **✅ DONE 2026-08-28 — the archive can no longer freeze the wrong year.** — DONE 2026-08-28 · `docs/TODO_archive.md`
- [x] **✅ DONE 2026-08-28 — the merge gate exists.** — DONE 2026-08-28 · `docs/TODO_archive.md`
- [x] **✅ DONE 2026-08-27 — the temporal archive's mislabelled 2025 entry is deleted, and 2025 is accepted as unrecoverable.** — DONE 2026-08-27 · `docs/TODO_archive.md`

- **Wire `check_temporal_archive_year.py` into the monthly vintage digest** — DONE 2026-08-27 (PR #258). No workflow change needed: the digest already runs `vintage_report.py`, so it is a check function + a `CHECKS` entry. Also fixed a FALSE ALARM found while testing — `check_assessment_roll` bypassed the stale-metadata downgrade and would have said "roll has moved to 2025" every month from 2026-09-01. `docs/RUNBOOK.md` §0, `docs/TODO_archive.md`.


- [x] **▶▶ FIXED 2026-08-25 — THE MEASURED ROLL-YEAR GUARD EXISTED BUT RAN NOWHERE — `check_roll_year_against_fir.py` was not wired into any workflow; exit 3 now HOLDS** — 2026-08-25 · `docs/TODO_archive.md`
- [x] **▶▶▶ FIXED 2026-08-25 — THE LIVE ROLL IS THE 2026 ROLL AND WE BILLED IT AT 2025 MILL RATES — the year-alignment guard cannot see it, because it reads a** — 2026-08-25 · `docs/TODO_archive.md`
- [x] **▶▶ FIXED 2026-08-25 — THE MAP'S LEVIED/EXEMPT UNCERTAINTY BAND WAS TOO NARROW — `PS` ("Parks and Services") is categorised `never`, not `inst`, so $88** — 2026-08-25 · `docs/TODO_archive.md`



- [x] **`gross_area` MISSING and `gross_area` ZERO were the same number — `far` now emits `null`, not 0, where no floor area is recorded.** — DONE 2026-08-22 · `docs/TODO_archive.md`
- [x] **The Services lens has no hood panel — BUILT 2026-08-10. Revenue vs each service cost, grouped by basis, NO total (two no-sum rules).** — DONE 2026-08-10 · `docs/TODO_archive.md`
- [x] **Sweep the doc-to-doc citations — DONE 2026-08-09 (S104). ONE REAL DEFECT, and it was a locked decision built on a display artifact.** — DONE 2026-08-09 · `docs/TODO_archive.md`



- [x] **Doc-citation sweep of `src/`, `scripts/`, `tools/` — DONE 2026-08-09, no wrong number reached shipped data.** 216 sites / 51 files, ~20 with a falsifiable number, every one re-derived from `data/raw/`. Three comment-level defects: a **line-number citation that drifted** (`audit_exempt_institutional.py`'s "DATA.md line ~308" — right on 2026-07-09, now ~240 lines off), a **unit mislabel** (`load_temporal.py`'s "19 rows" is 19 *accounts*, 16 rows), and ⚠️ **S102's own follow-up note retracted** — it said `SPEC_temporal.md` §2 "was never updated", but `git log -S` shows the §2 banner and the comment flagging it landed in the SAME commit (`7e065ef`). — 2026-08-09 · `docs/TODO_archive.md`

- [x] **`WEST MEADOWLARK PARK`'s revenue MORE THAN DOUBLED in one auto-refresh — EXPLAINED 2026-08-07: a RENUMBERING GAP CLOSING, so the +130% was the CORRECTION, not the defect.** Misericordia was continuously assessed 2012–2025 and merely absent from the published current roll during a renumber; the map had been UNDERSTATING the hood by ~$250M assessed / ~$6M/yr. ⚠️ **Two earlier answers are WRONG and are recorded in commits** — *"one new $247.8M parcel arrived"* (true but shallow) and *"is a hospital supposed to be taxable?"* (the wrong question; it always was). Read the archive entry before citing either. — 2026-08-07 · `docs/TODO_archive.md`



- [x] **Tighten the cardinality-guard bands — DONE 2026-08-05, and the item's premise was half wrong, so only FOUR of the six moved.** The variance data turned out to exist in a place nobody had looked: **the guard logs every anchor value in CI**, harvested from the refresh runs' job logs. ⚠️ **Five runs but only THREE independent data changes** — the 2026-08-02 and 08-05 runs committed `status.json` only, so their readings re-measure unchanged input. **Four anchors were effectively frozen** (`dup_parcel_points` constant at 33, `lot_needle_ratio` 0.00%, `dedupe_effect_pct` 0.01%, `dup_parcel_value_frac` 0.11%) and were tightened **2×**, to ±25%. ⚠️ **The other two are not noisy, they are TRENDING** — `ineligible_points` 56→58→60 and `ineligible_value_frac` 0.00517→0.00575→0.00633, monotonic, in the guard's own **dangerous** direction — and were **left wide on purpose**: tightening them would red the weekly publish on the next real data change and read as a false alarm. ⚠️ **The item's prescribed mechanism could not express this** — `--write-baseline --tolerance` applies ONE global tolerance to every anchor, so the bands are now hand-set per anchor and that flag would flatten them; the baseline says so in `_bands_are_per_anchor`. **Not tightened further than ±25% because no observation across a January year-roll exists yet**, which is the event the guard was built for. Three new tests pin all of it, and the tightening test was **falsified against the old baseline first**. The drift became its own open item. — 2026-08-05 · `docs/TODO_archive.md`

- [x] **Publish the roads-maintenance correction — DONE 2026-08-05, verified against PRODUCTION.** `refresh.yml` dispatched by hand per RUNBOOK §3d (run `30966755798`, success). The live pod now prints roads at **$103M · 2.7%** with **no asterisk**, was $50.985M · 1.33% with one; `transit:roads` reads **4.6×**. `verify-about.js` against the public root: **ALL CHECKS PASSED** — all four shares recomputed independently from the published dollars, pod still fits at 900/800/768/720px. ⚠️ **The refresh committed `status.json` ONLY** (`8ca6e8f`), i.e. no source data changed on this run — which is what made it a clean publish of the manifest edit and nothing else. — 2026-08-05 · `docs/TODO_archive.md`

- [x] **Source the derived $14.135M roads-maintenance figure — CLOSED 2026-08-04, and the derived figure was ~5× TOO LOW, live on a public page.** Replaced with **$65,671,000**, the Open Budget portal's `Roadway Maintenance` program (FY2017). ⚠️ **The item said "the one soft number in that table"; it was a wrong one.** The derived value was `$1,285/km × ~11,000 km` — a narrow unit rate multiplied across the whole network; the published program implies **~$5,900/km**. Roads moves **1.33% → 2.67%** of the operating budget and transit:roads **9.2× → 4.6×**. ⚠️ **The error was in OUR derivation, not the Taproot source** — that source's *totals* reconcile: roads snow $36.85M + path snow $30.15M = **99.2%** of the portal's published `Snow and Ice Control` program, and **that contrast is what exposed the maintenance line**. **2017 is the only year Edmonton ever published a roads-only maintenance program** (re-cut in 2018 into a line that also covers sidewalks and pathways — using it would double-count this table's own rows — and again in 2026), so Peter chose clean scope over matching vintage. New **`DATA.md` §17** documents the portal, including its **two rename eras** and a **+1.31% portal-vs-PDF** gap. ⚠️ **Not yet on the live site** — budget figures ship only when `refresh.yml` reruns `generate_status.py`; see the open publish item. — 2026-08-04 · `docs/TODO_archive.md`

- [x] **Mobile chrome — the bottom-sheet question — CLOSED 2026-08-04, NO code change: the control column stays a stack.** The quick pass's last open piece was a *decision*, not a build item (steps 1-2 shipped `0089eba`; step 3 closed 2026-07-31 as not reproducible). ⚠️ **Re-measured before deciding, and the basis had moved.** The union method reproduced the default to the decimal (**27.9%**), but **Money unfolded is 47.9%, not the recorded 54.3%** — `#moneymode` left the Options panel on **2026-08-02, one day after that measurement**. ⚠️ **The ">half the screen" claim was attached to the wrong state**: the only >50% states are **Services 53.1%** and **Development 52.7%**, neither ever measured — the 08-01 pass took one view and generalised. ⚠️ **The public build cannot reach the worst state**: Services and Ratio are full-only since 2026-07-28, so **public `#views` is TWO buttons (Money · Development)**, correcting a doc line that claimed four. Worst public state is **52.3%** (Development unfolded + peek), rendered clean. Peter's call: the >50% states are transient and user-initiated, a bottom sheet is a **shared desktop+mobile DOM** refactor, and the default a phone user meets is 27.9% vs desktop 20.3%. ⚠️ **`#views` position loses its vehicle** — it was parked pending this fork. **Tenth time a stated basis did not survive re-measurement; the first where that CLOSED the item.** — 2026-08-04 · `docs/TODO_archive.md`

- [x] **The four Stage 2 cost columns shipped and `expected_columns.json` is re-pinned 62 → 66 — DONE 2026-08-04, on a manually dispatched refresh.** The weekly cron was 6 days out, so `refresh.yml` was dispatched by hand (run `30909649645`, success, commit `024ecc6`). All four `cost_*_ops_per_acre` columns are present on all **406** features and the composite sums exactly (`88.92 + 13820.65 + 129.59 = 14039.16`). ⚠️ **The pre-repin guard behaved exactly as the item predicted** — warned on all four as NEW, exit 0 — and that is also the path it took **in CI**. ⚠️ **The served-column guard has now RUN IN CI for the first time** (step *"Check served columns (guard after regenerating)"*, success), closing an item carried S89 → S91. Re-pin diff is a pure 4-line addition; the re-run is clean at 66. `status.json` carries `budget_context`, so both S90 features' data is live. Verified against **production**: `verify-transport-cost.js` **6 → 41 passed / 0 failed** against `/full/` (including the load-bearing two-bases check, roads ops **$89** vs svc **$7,527**), `verify-about.js` **ALL CHECKS PASSED** against the public root (all four shares recomputed independently from dollars, pod fits at 720px). — 2026-08-04 · `docs/TODO_archive.md`

- [x] **`verify-peek.js` was 71% of the suite's wall time — FIXED 2026-08-04, 437s → 94s, 27/27 still green.** ⚠️ **The item named the wrong loop.** `findTappableHoods` (which it blamed) is 46s of 408s — it exits at `n` hoods and never nears its worst case. The cost was the **empty-map-pixel scan: 346s, 85%**, blind-sweeping ~2,470 picks. ⚠️ **A pick costs ~137ms and neither `radius` nor `deviceScaleFactor` changes it** — deck re-renders the whole picking buffer on the CPU per call, so the only lever is *fewer picks*; the first burst also carries a one-off ~20s shader warm-up, which is what `targets`' residual 46s is (left alone, it is at the floor). ⚠️ **Its "coarsen the grid" lever is a measured trap**: step 25 still costs 30s and **step 40 finds nothing** and fails the check — only 17 of 4,400 grid points are clear. Fixed with its *other* lever: `metric-extrusion` is the only pickable layer, so the pixel is derived from projected geometry (9,236 vertices, 14ms) and confirmed with **one** pick instead of 2,474, landing on the same pixel. — 2026-08-04 · `docs/TODO_archive.md`

- [x] **The verify runner's own default was manufacturing quirk (mmm) — FIXED 2026-08-03.** `verify.js` hardcoded `--jobs 3`, but a **single** verify script draws **~275% CPU** on this 4-core box (headless Chromium on SwiftShader — software rasterisation and software deck.gl picking), so 3-up demanded ~8 cores from 4: `cpu_sum` 385–400%, load 8.2. Measured on three scripts: jobs=3 ~509s **2 failed**, jobs=2 ~505s **1 failed**, jobs=1 615s **all green** — parallelism was buying ~17% wall time for a suite whose red results had to be re-run alone to mean anything (three scripts went red on PR #148, which touched none of them). Default now `floor(cores / 3)` → 1 here, 2 on an 8-core; `--jobs N` still forces. ⚠️ `verify-temporal`'s hand-set 4000ms click timeout deliberately left alone — it passes at the new default, and raising it would treat the symptom of a fixed cause. Not a CI change (`refresh.yml` runs `verify-smoke.js` directly). — 2026-08-03 · `docs/DECISIONS.md`

- [x] **A dropped SERVICES column was invisible to every guard — FIXED 2026-08-03.** Two halves, because the item's own prescribed fix could not catch the failure it named: `verify-smoke.js` gains `B7` (all-or-nothing presence, columns derived from the **union** of `SERVICES[].plane.col` and `RATIO_DENOMS[].col` — Roads is a ground layer, so `road_m_per_acre` lives only in the latter) and `B8` (a services row is offered exactly when its column is present). ⚠️ **B7 provably CANNOT catch a full drop** — falsification F2 shows it passing green — because nothing derived from the served file alone can tell "dropped" from "not shipped yet". That needs memory, so `scripts/check_served_columns.py` + `data/expected_columns.json` (62 columns) hold a committed baseline and fail the refresh on a removal; a new column only warns. — 2026-08-03 · `docs/TODO_archive.md`, `docs/DECISIONS.md`

- [x] **A data refresh published with no check on the RENDER — FIXED 2026-08-02.** `verify-smoke.js` gates `refresh.yml` before `upload-pages-artifact`, so a red check leaves the live site on the previous good render. Invariant-only by design (a pinned value would cry wolf weekly — #139). ⚠️ The item's premise was wrong: `refresh.yml` **deploys itself**, so the gap was an *unchecked* deploy, not a missing one. Falsification found the check's own hole (a dropped column is *omitted*, not printed as NaN → `B6`); the inverse test caught it crying wolf on absent mill rates. — 2026-08-02 · `docs/TODO_archive.md`, `docs/DECISIONS.md`

- [x] **`styles.css` had no cache-busting, so a CSS-only deploy could render stale — FIXED 2026-08-02.** `scripts/build_site.py` stamps `styles.css?v=<8 hex of the file's content hash>` into both builds; content hash not commit sha, so an unrelated deploy keeps the cached copy. Drift fails the build loudly. ⚠️ Scope is stale-CSS-under-fresh-HTML only — a stale `index.html` carries the old query with it, so RUNBOOK §3c keeps its private-window step. — 2026-08-02 · `docs/TODO_archive.md`, `docs/DECISIONS.md`

- [x] **The pinned panel painted over the title blurb in five states — FIXED 2026-08-02.** `#temporal`'s `top: 210px` constant replaced by `syncTemporalPos`, which measures `#title` and `#botleft`; where clearing the blurb leaves no room the **panel** scrolls, not the blurb (`#title` is `.panel`, so pointer-events:none — a capped blurb could not be scrolled to). Two defects found by measuring the fix: content-box `max-height` overshot `#botleft` by 11px, and an absolute close button scrolled away. `verify-temporal.js` 43 → 67 checks, sweeping six states. — 2026-08-02 · `docs/TODO_archive.md`, `docs/DECISIONS.md`

- [x] **`verify-temporal.js` red since the 2026-08-01 refresh — DIAGNOSED AND FIXED 2026-08-02.** The data moved, the splice did not: 839 changed cells, **every one in 2025**, 2012–2023 bit-identical across all 406 hoods. The defect was in the script, which pinned the live year the pipeline guard deliberately refuses to band. Live-year assertions now derived from the loaded series; historical anchors stay pinned. 42 → 43 checks, green. — 2026-08-02 · `docs/TODO_archive.md`, `docs/DECISIONS.md`

- [x] **UI BUG: the Display popover and the Data & Methods pod overlap. FIXED 2026-08-02** — 2026-08-02 · `docs/TODO_archive.md`



- [x] **▶ REVENUE-LENS READOUT — phase 2 of 2: the UI. DONE 2026-08-01 (both halves).** — DONE 2026-08-01 · `docs/TODO_archive.md`



- [x] **UI BUG: the hover tooltip `div.tip` rendered on TOUCH, 127px off the right edge. CONFIRMED ON DEVICE and FIXED 2026-07-31.** — 2026-07-31 · `docs/TODO_archive.md`
- [x] **REVENUE-LENS READOUT phase 1 (pipeline) — BUILT 2026-08-01.** `src/revenue_by_zone.py` + 11 tests; ships `total_revenue`, `revenue_share_city` and 10 `rev_frac_*` columns. Zoning source reversed on measurement: the polygons, not `dkk9-cj3x`'s per-property field (null for 42% of Downtown's revenue). Phase 2 (the UI) closed later the same day. — 2026-08-01 · `docs/DECISIONS.md`, `data/DATA.md`
- [x] **`#hoodmode-btn` CONFIRMS instead of toggling off when the panel was opened by a peek card — RULED and BUILT 2026-08-01.** Peter: *"change button name and first press to mean yes, keep it open."* Three label states now (`popup` / `panel` / `panel ✓`); the tick marks the only one that earns one-tap pinning. — 2026-08-01 · `docs/DECISIONS.md`
- [x] **Should the change lens's card carry its `% of city base` endpoints? RULED 2026-08-01: LEAVE IT.** Peter's call; the panel is one tap away and special-casing would put wrapper content in the card for one view only. — 2026-08-01 · `docs/SPEC_temporal.md` §2
- [x] **REGRESSION from that fix: suppressing `.tip` left every lens with a ONE-LINE readout on touch. Reported by Peter and FIXED 2026-08-01** — the peek card now borrows `viewTooltip(info, false)`, so it carries the lens's full rows; Money's readout also split so revenue facts no longer print under the Value map. — 2026-08-01 · `docs/DECISIONS.md`, `docs/MOBILE_USABILITY.md` §2b



- [x] **PROMOTED the temporal + change lenses to the PUBLIC build — DONE 2026-07-31 (PR #121, merged `828bb5a`, deploy green, LIVE).** — DONE 2026-07-31 · `docs/TODO_archive.md`
- [x] **ALL THREE PRE-EXISTING VERIFY FAILURES ARE FIXED (2026-07-31). THE SUITE IS GREEN: 26 scripts, 0 failures.** — 2026-07-31 · `docs/TODO_archive.md`
- [x] **TOUCH: the history panel now takes TWO gestures (tap → peek card → tap the card), and the panel's × is doubled to 44px — DONE 2026-07-31.** Peter: *"the panel on mobile [should be] harder to activate"* + *"the x on the panel needs to be twice as big"*. Gated on `(hover: none)`, all touch paths idempotent (a tap can fire the handler twice). ⚠️ **Two claims here were REVISED the same day:** the gate is armed on EVERY tap (only `#hoodmode-btn` disarms it — committing the card was itself what set panel mode), and *"on touch the tooltip node never exists"* was true of deck's built-in `.deck-tooltip` but NOT of the app's own `.tip`, which did render on a finger. `verify-peek.js`, 25 checks — **the first script in the suite that drives a real pointer at the map.** — `docs/DECISIONS.md` 2026-07-31, `docs/SPEC_temporal.md` §2



- [x] **ASSESSMENT-OVER-TIME GRAPH PER NEIGHBOURHOOD** — COMPLETE 2026-07-29 · `docs/TODO_archive.md`
- [x] **TEMPORAL, ROUND 2 — "HOW MUCH HAS EACH HOOD CHANGED?" AS A MAP METRIC, WITH SELECTABLE WINDOWS (Peter, 2026-07-30).** — BUILT 2026-07-30 · `docs/TODO_archive.md`
- [x] **UI: the pinned panel and the hover popup must not both be up — add an explicit MODE toggle** — DONE 2026-07-30 · `docs/TODO_archive.md`
- [x] **NEEDS A PHONE, NOT A BOX: confirm the double-tap-zoom fix (PR #107).** — 2026-07-27 · `docs/TODO_archive.md`
- [x] **LABEL SWEEP IS BLIND TO DOM CHROME.** — DONE 2026-07-27 · `docs/TODO_archive.md`
- [x] **PUBLIC BUILD SHAPE** — LOCKED 2026-07-28 · `docs/TODO_archive.md`
- [x] **RIVER GEOMETRY IS UNTRIMMED AND UNCHECKED (audited 2026-07-27).** — CLOSED 2026-07-27 · `docs/TODO_archive.md`
- [x] **FLAKY TEST: `verify-uses-prisms.js` "money: control hidden again, state kept" (found 2026-07-27).** — CLOSED 2026-07-28 · `docs/TODO_archive.md`
- [x] **SMALL OPEN UI DECISIONS (2026-07-25).** — CLOSED 2026-07-26 · `docs/TODO_archive.md`
- [x] **Residential revenue metric ("Residential $", Peter 2026-07-16)** — SHIPPED 2026-07-16 · `docs/TODO_archive.md`
- [x] **Dev+Infill ROUND-2 delta audit** — EXECUTED 2026-07-16 · `docs/TODO_archive.md`
- [x] **PRIORITY — Lot-acre denominator TOGGLE on the neighbourhood (first) lens (NEW 2026-07-08, out of the cardinality audit below).** — BUILT 2026-07-08 · `docs/TODO_archive.md`
- [x] **PRE-LAUNCH AUDIT — record-to-parcel cardinality bug (WEM numerator + condo denominator) & lot-acre vs ground-acre methodology (NEW 2026-07-08).** — CLOSED 2026-07-09 · `docs/TODO_archive.md`
- [x] **Neighbourhood labels — finish + ship** — SHIPPED 2026-07-04 · `docs/TODO_archive.md`
- [x] **Ghost prisms over a neutral hood plane (Peter, 2026-07-03; design clarified 2026-07-04).** — SHIPPED 2026-07-05 · `docs/TODO_archive.md`
- [x] **PRIORITY — Lot-size denominator variant for the grid spikes** — SHIPPED 2026-07-05 · `docs/TODO_archive.md`
- [x] **SCOPE: composition numbers now; full zoning POLYGON layer in the viewer is a SEPARATE later product decision** — 2026-07-03 · `docs/TODO_archive.md`
- [x] **UI control hierarchy: separate "Color Adjustment" from lens controls.** — BUILT 2026-07-07 · `docs/TODO_archive.md`
- [x] **Deployment — LIVE (2026-07-01/02)** — 2026-07-01 · `docs/TODO_archive.md`


- [x] Revenue phase backend — per-property municipal levy + `revenue_per_acre`
  (committed `5912576`).
- [x] Web value↔revenue toggle, revenue default (committed `a0cf2a0`).
- [x] Push `feature/phase2-web` to origin.
- [x] **Low-coverage tail separated via the Zoning Bylaw layer (`fixa-tstc`)** —
  end-to-end land-use set-aside feature (2026-07-01). `src/load_zoning.py` (95 base
  codes → never/notyet/inst/dev, overlay → `set_aside_frac`/`is_set_aside`/
  `set_aside_reason`), wired through `join_and_calculate` + `main.py`; 48 hoods set
  aside at ≥0.90. Colour transform **DECIDED: sqrt** (FINDINGS §6.1 — log over-corrects
  to −4.19; the mixed 0.55–0.90 band stays on-scale by design). Frontend: sqrt colour
  + neutral-grey set-aside hoods. Methodology caveat recorded in FINDINGS §5 (zoning
  `UI`/`UF`/`AJ`/`PU` partially flags exempt-roll understatement). Refs:
  `docs/FINDINGS_revenue_scale.md` §§5–6.1, `scripts/investigate_skew.py`,
  `docs/SPEC_revenue.md` "Update 2026-06-29".
