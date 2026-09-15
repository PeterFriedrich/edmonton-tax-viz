# AUDIT BRIEF — published numbers with no loud check

**Read cold.** This is a reusable *instrument*, not a findings doc. The coverage
map is `docs/AUDIT_LEDGER.md` (candidate 10). Scoping measurement taken
2026-09-15 (S159) with `tools/profiling/audit-published-numbers.js`.

**Fourth sibling of a swept family, and it inverts them.**
`docs/FABLE_AUDIT_proxy_guards.md` is a check reading a **stand-in** for the
property; `docs/FABLE_AUDIT_vacuous_guards.md` is a check reading the right
property where it **cannot differ**; `docs/FABLE_AUDIT_controls_state_space.md`
is a control next to a readout it does not reach. All three audit a thing that
exists and is wrong. **This one audits an absence**: a number a reader can see,
quote and act on, with nothing that fails when it goes wrong.

---

## §0 — Why this class exists

**Fresh evidence, which is this list's stated criterion.**

S159 (2026-09-15) closed F1 — the Services panel had reported road costs under
Fire, Water, Transit and Bike for weeks. ⚠️ **It had been confirmed by three
separate sessions and fixed by none.** What closed it was not another paragraph:
it was `verify-services-panel.js`, written red and merged red. In the same
session an outside review of this project's documentation apparatus landed on one
line worth keeping:

> *Prose about correctness is not a control on correctness — executable checks
> are.*

⚠️ **That review's specific accusations about this repo were checked and two did
not survive** (`docs/DECISIONS.md` 2026-09-15 and the S159 handoff record which).
The line above did. This brief is the part that survived, turned into work.

⚠️ **The project's standing failure mode is the same shape one level up**: a
working guard on a channel nobody reads (`_classify` warned for ~70 days into a
log). A number with no guard at all is that failure with the guard removed.

---

## §1 — The hinge: "unguarded" means three different things

> ⚠️ **Do not rank by the raw unguarded count. Rank by HOW THE NUMBER CAN GO
> WRONG**, which differs by where it comes from. The scoping run's 63 uncovered
> claims are not 63 defects, and treating them as one list produces a worthless
> report.

| kind | where it comes from | how it goes wrong | what a guard would have to do |
|---|---|---|---|
| **Computed** | a served column, formatted at render (`$256,564 / acre`, `14%`, a rank) | the pipeline computes it wrong, or the column vanishes | already partly covered: `check_served_columns.py` (schema), `check_value_anchors.py` (cardinality), 892 pytest, 43 verify scripts |
| **Manifest** | `status.json`, written from a **hand-maintained** JSON (`city_budget_context.json`, `city_unit_costs.json`, `mill_rates.json`) | the world moves and the file does not — **silently, forever** | nothing recurring exists. This is the gap |
| **Literal** | typed into a blurb in `web/index.html` | the pipeline changes and the sentence does not | `check_cost_copy.py` covers **7 rates**; everything else is unguarded |

⚠️ **A computed number being "unguarded by a copy check" is not a finding** — it
is the wrong guard for that kind. Say so and move on. The audit's value is in the
manifest and literal rows.

---

## §2 — ⚠️ FALSIFY THE INSTRUMENT FIRST

The scoping run's **first** extractor was a regex over `web/index.html` and it
was wrong in two ways that both produced confident output:

1. It counted **code comments as reader-facing copy** — `colorClamp: 30_000, //
   hand-set from the ramp` was reported as a published claim.
2. Blurbs are `+`-concatenated across source lines, so a per-line match **split
   numbers from their sentences** and undercounted coverage (it scored 4 of 23
   covered where the guard actually names 7).

`audit-published-numbers.js` therefore reads the **RENDERED** page — it drives
every view and all ten service layers and scrapes the blurb, panel note, panel
readout, legend and About panel. ⚠️ **That is the only way to enumerate what a
reader can see**, and it is the same DRAWN-vs-source rule that caught the frozen
label sweep (`DECISIONS.md` 2026-07-27).

⚠️ **AMENDED 2026-09-15 (S160, first execution — `FINDINGS_published_numbers.md`
§1): the shipped v1 had three MORE defects than this section listed, and the
run fixed them before trusting the inventory.** (1) It looped `Object.keys(VIEWS)`,
which has no `money` key — **the landing view and its four metrics were never
captured**, so "6 views" below was 8 `VIEWS` entries and no Money. (2) It drove
views and services by JS, which works on the public build for controls that
build hides — **18 of the public claims were unreachable by a public reader**;
surfaces now carry `reachable`. (3) `$50k` tokenised as `$50` and merged with the
About panel's "$50 per metre". Corrected inventory: **77 claims on `/full/`, 58
reachable on public** (23 surfaces; 14 reachable on public).

⚠️ **Its remaining known limits, which the audit must close, not inherit:**
- **It captures one hood (DOWNTOWN) and one viewport** (`--hoods A,B` now takes
  more; a second hood added 27 claims in S160, all computed panel readouts). A
  claim that only renders on a phone is invisible to it. **The `moneydetail` grid
  legends, the `denom` lot-acre variant, tooltips and the peek card are not
  captured.**
- **It does not read the README, the Data & Methods long copy, or the four
  evidence notebooks** — all reader-facing, all carrying numbers.
- **Bare small integers are excluded by design** ("31 fire stations" is prose).
  ⚠️ That exclusion is a judgement call and may be hiding a real claim.
- It cannot tell *computed* from *literal* on its own. §1's split was done by
  hand and **is the part most likely to be wrong**.

---

## §3 — The scoping measurement (full build, 2026-09-15, 1440×900)

18 surfaces captured (6 views + 10 service layers + panel states). **74 distinct
numeric claims visible to a reader; 11 named by any guard; 63 not.**
⚠️ **Superseded by the S160 run (§2 amendment above): 77 / 58-reachable-on-public
with the Money view included.** The manifest rows and their ranking below are
unchanged by the correction; the two "nothing recurring can go red" sentences
are **half wrong** — `test_generate_status.py` pins the total, the component
sums and the four shares against a hand *edit*; what nothing catches is the
*world moving* (`year` 2025→2019 passes everything). Findings §3.

The highest-exposure rows, and they are all **manifest**:

| claim | on | source |
|---|---|---|
| `$3.8B`, `$469M`, `12.2%`, `$103M`, `2.7%`, `$30.4M`, `0.79%`, `$5.9M`, `0.15%` | **all 18 surfaces** (About panel) | `status.json` ← `data/city_budget_context.json` |

⚠️ **These are the most-published numbers on the site** — the About panel is
reachable from every view — and they are **hand-maintained**. `AUDIT_LEDGER.md`
2026-08-05 (S94) checked the four manual reviewed inputs against an independent
published source **once**. `export_budget_ranked.py` and `generate_status.py`
touch the file, but both are **producers, not checks**: nothing fails if the
values drift from what the City now publishes.

---

## §4 — Ranked targets (highest level first; a moot level moots what is under it)

### T1 — the hand-maintained manifest inputs, which nothing re-checks

`city_budget_context.json`, `city_unit_costs.json`, `mill_rates.json`. Audited
once each, published on every surface, and **structurally incapable of going red**
when the City republishes. Ask in this order: (a) is the value still what the
source says? (b) **is there a check that would have caught the drift**, and if
not, what is the cheapest one — a vintage assertion, a fetch-and-compare, a
digest line? ⚠️ **The `mill_rates.json` precedent is the model** — its Farmland
caveat is driven by an `assumed` list so it *stops printing by itself* the year a
real row is published (`DECISIONS.md` 2026-08-01). That is a guard built into the
data. Look for where else that shape applies.

### T2 — literals in blurbs beyond `check_cost_copy.py`'s seven rates

The guard covers the road/transit/bike unit costs. Not covered: the fire-cost
illustration figures, the bikeway `$178` / `$20,100` rates, the LRT band
distances, the coverage percentages. ⚠️ **`check_cost_copy.py` is itself a
known-weak guard** — `FINDINGS_vacuous_guards.md` V1 showed it can be satisfied by
a code comment, and it was fixed; **re-confirm the fix holds before trusting its
7** (that is a cross-model re-check of a prior finding, which is this brief's
cheapest real win).

### T3 — computed numbers whose *formatting* can lie

Not whether the value is right — whether the rendering can misstate it. Precedent
in-repo: `fmtSvcRatio` prints `<0.1%` rather than `0.0%` precisely so a category
that earned a row cannot claim to contribute nothing, and the revenue panel keeps
2 decimals because `fmtBig` would print `$1,876,137` as `$2M`. **Those are guarded
by verify scripts today. Sweep for the ones that are not.**

### T4 — surfaces the instrument does not reach

README, Data & Methods long copy, the four evidence notebooks, phone-only
readouts, and any claim that renders only for a hood other than DOWNTOWN.
⚠️ **Enumerate these before concluding anything about coverage** — a clean report
over an incomplete surface list is the failure this project keeps finding.

---

## §5 — Method

```bash
.venv/bin/python scripts/build_site.py --src web --out $SCR/_site
# ⚠️ restart the server before EVERY Playwright run — it wedges and then serves
# empty responses while still answering
cd tools/profiling            # ⚠️ required: playwright resolves from the SCRIPT dir
node audit-published-numbers.js http://localhost:8947/full/index.html > claims.json
node audit-published-numbers.js http://localhost:8947/index.html      # public
```

1. **Re-read §2 and decide whether the instrument's limits invalidate the
   inventory** before using it. Extend it or work by hand — do not inherit it.
2. Sort every claim into §1's three kinds. **Report the sort**, because it is the
   judgement the rest rests on.
3. For each **manifest** and **literal** claim: does a check exist that would go
   red if the number became wrong? Falsify by name — change the value and confirm
   something fails. ⚠️ **A guard that stays green under a deliberately wrong value
   is the finding**, and it is the same falsification `FINDINGS_vacuous_guards.md`
   used.
4. ⚠️ **Run both builds.** A claim can be full-only (rank lower) or public (rank
   higher).
5. Add an `AUDIT_LEDGER.md` row when the audit **executes**, with a pointer to its
   findings doc.

⚠️ **Out of scope, so nobody writes it:** *whether the numbers are correct.* That
is `docs/DATA_INTEGRITY.md`'s question and several ledger rows have answered parts
of it. This brief asks only whether a wrong value would be **caught**, which is a
falsifiable question about the guard estate.

⚠️ **THE SCOPING RUN AND §1's TAXONOMY WERE WRITTEN BY THE MODEL THAT BUILT F1
AND ITS VERIFY SCRIPT THE SAME DAY (Opus 5, S159), AND IT IS GRADING ITS OWN
COVERAGE. Reject the definitions if they are wrong.** Specifically: "published
number" here means *visible to a reader on a served surface*, and "covered" means
*named by a guard script*. Both are narrow. A number in a tooltip nobody hovers,
or covered by a pytest rather than a `check_*.py`, is sorted wrongly by those
definitions — and the S158→S159 pattern is that the instrument is the first thing
to find broken.
