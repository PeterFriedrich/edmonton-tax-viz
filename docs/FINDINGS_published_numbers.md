# Findings — published numbers with no loud check (run 2026-09-15, S160, Fable 5.1)

Instrument: `docs/FABLE_AUDIT_published_numbers.md` +
`tools/profiling/audit-published-numbers.js`. Ledger row: 2026-09-15 (S160). The
brief and its scoping run were Opus 5 (S159, the same day it built F1); this is
the first execution and the first cross-model read of it.

**The brief's hinge holds — the raw "63 unguarded" is not a defect list — but its
own scoping measurement was wrong in three ways that all pointed the same
direction, and the instrument had to be fixed before the inventory meant
anything (§1).** On the corrected inventory: **the manifest inputs still match
their source (T1a), nothing recurring would tell anyone if they stopped (T1b —
falsified: a wrong mill rate, propagated consistently, passes 892 tests and every
merge-gate guard), and three public-reachable literals have no guard at all (T2),
one of them sitting in the blind spot of the guard built for exactly its shape.**
One hand-set colour clamp has drifted below its stated percentile (T3). The
surfaces the instrument does not reach are enumerated, not audited (T4).

⚠️ **Nothing was built.** Every remedy below is a proposal; the one that changes
the monthly digest (§2.3) needs Peter's yes by the project's own rule.

---

## §0 — Method, as run

```
build_site.py --src web --out $SCR/_site
audit-published-numbers.js  /full/index.html            (v1, as shipped: 18 surfaces, 74 claims)
audit-published-numbers.js  /index.html                 (v1: 18 surfaces, 73 claims)
  → instrument fixed (§1) →
audit-published-numbers.js  /full/index.html --hoods DOWNTOWN,GLENORA   (46 surfaces, 101 claims)
audit-published-numbers.js  /full/index.html            (23 surfaces, 77 claims)
audit-published-numbers.js  /index.html                 (23 captured, 14 reachable; 76 / 58 claims)
```

Server restarted before every Playwright run; runs one at a time. Fresh fetch of
`budget.edmonton.ca/api/operating_budget.csv` (200, 1,036,937 bytes, 7,294 rows)
diffed against the 2026-09-05 copy still on disk (`/tmp/opbudget.csv`, 1,037,656
bytes, 7,283 rows). Nine mutations of committed inputs and copy, each against the
full suite (`892 passed` control) and the three merge-gate guards, each restored
with `git checkout` and the tree confirmed clean.

---

## §1 — Falsify the instrument first (brief §2) — three defects, all fixed

The brief said *"re-read §2 and decide whether the instrument's limits invalidate
the inventory before using it"*. They did, and two of the three were not in §2.

| # | defect | effect on the scoping numbers | fix |
|---|---|---|---|
| I1 | **The landing view was never captured.** The loop was `Object.keys(VIEWS)`, and `VIEWS` has no `money` key — Money is the default state, not an entry. The most-seen surface on the site (title, blurb, legend, four metric variants) contributed **zero** of the 74 | The brief's "6 views" was 8 `VIEWS` keys, none of them Money. The `$50k+` / `$30k+` / `$4M+` legend clamps — hand-set literals — were absent from the inventory | Money captured first as `view:money`, then each `METRICS` key as `metric:<key>` |
| I2 | **The public inventory counted surfaces a public reader cannot reach.** Views and services were driven by JS (`applyView`, `applyService`), which works on the public build for controls that build *hides* — the memory-file lesson that verify scripts bypass pointer-events, one instrument over. The public run reported 18 surfaces and 73 claims; the public page shows **4 views and 3 services** | **18 of 76 public claims are unreachable** (`$436.6 million`, `$20,100`, `$178`, `$35,200`, the storm/water/fire legends …). Brief §5 step 4 — *"a claim can be full-only (rank lower) or public (rank higher)"* — could not be applied to the v1 output | Every surface carries `reachable` (the button/row leading to it is visible); rows carry a `reachable` count. Glass/change/infill inherit their parent button, an approximation |
| I3 | **`$50k` tokenised as `$50`** — `k` was not in the regex's suffix set, so the money legend's clamp merged with the About panel's *"$50 per metre per year"* and the row read `n=19` | One row conflated a literal rate (guarded) with a hand-set clamp (not guarded, §4) | `k` added; `$50` now 24 (all About), `$50k` 3, `$30k` 1 |

Corrected inventory, one hood (DOWNTOWN), 1440×900:

| build | surfaces | reachable | distinct claims | reachable claims |
|---|---|---|---|---|
| `/full/` | 23 | 23 | **77** | 77 |
| public | 23 | **14** | 76 | **58** |

Adding a second hood (GLENORA) adds 27 claims and **every one is a panel readout**
— computed numbers, §2 kind 1. The brief's "one hood" limit therefore costs the
inventory nothing that matters to this audit; it would matter to a
*correctness* audit.

**Limits that remain, stated so nobody inherits them silently:** the
`moneydetail` grid legends (100 m / 50 m) and the `denom` lot-acre variant are not
captured; tooltips and the peek card are not captured; one viewport; bare small
integers still excluded; README and notebooks not read (§5).

---

## §2 — The sort (brief §1), reported because it is the judgement everything rests on

Mechanical first cut on the 77 full-build claims: value string present in
`web/index.html` source → *literal*; About-panel-only and absent from source →
*manifest*; else *computed*. Then corrected by hand, because the mechanical cut
misfiles both ways: a panel readout that happens to equal a string in the source
(`0.1%`, `0.5%`, `4.5%`, `14%`) is computed, and a year that appears everywhere
(`2025`, `2026`) is manifest on the About panel and prose in a blurb.

| kind | count | what a guard would have to do | verdict |
|---|---|---|---|
| **computed** | ~55 | pipeline + schema + verify | ✅ **not this audit's business** — `check_served_columns` (schema, now with the all-null bucket), `check_value_anchors`, 892 pytest, 43 verify scripts. Being "unguarded by a copy check" is the wrong guard for this kind, as the brief says |
| **manifest** | 12 | catch the world moving | §3 — the gap, confirmed and measured |
| **literal** | 10 | tie the sentence to the number it restates | §4 — 7 of 10 covered by `check_cost_copy`; **3 uncovered, all public-reachable** |

The manifest 12: the About panel's nine (`$3.8B`, `$469M`, `12.2%`, `$103M`,
`2.7%`, `$30.4M`, `0.79%`, `$5.9M`, `0.15%`) from `city_budget_context.json`; the
three vintage years (`2026` data, `2026` rates, `2024` zoning) from
`generate_status.py`'s pins; and the three mill rates in the pod from
`mill_rates.json`.

The literal 10: `$50 per metre per year` (About), `$5,970`, `$3,350`, `$178`,
`$20,100`, `$436.6 million` and *"five times"* — the seven `check_cost_copy`
rows — plus `$600,000`, `$1,900,000` (roadslife blurb), `~0.9% of units 2021–25`
(infill blurb). `2015` (*"a 1960s street and a 2015 one"*) and `2017` (*"the
City's 2017 maintenance figure"*) are prose vintages, excluded; the second is
noted in §4 as a cheap future row.

---

## §3 — T1: the hand-maintained manifest inputs

### T1a — are the values still what the source says? ✅ YES, every one

Fresh portal pull, 2026-09-15, recomputed rather than compared to §16's text:

| committed figure | file | source now | agreement |
|---|---|---|---|
| total operating **$3,845,555,000** (FY2025) | `city_budget_context.json` | FY2025 tax-supported **$3,855,881,010** | 99.7%, unchanged since S94 |
| roads maintenance **$65,671,000** | same | FY2017 `Roadway Maintenance` **$65,671,000** | exact |
| roads + paths snow **$67.0M** | same | FY2025 `OPS/PARS - Snow and Ice Control` **$67,553,815** | 99.2%, unchanged |
| transit incl. DATS **$468,571,000** | same | FY2025 `Edmonton Transit Service` branch **$482,556,115** | 97.1% — a source difference (ETS Plan vs portal), documented in §17 as not-to-be-fixed |
| fire gross **$276,706,000** (2026) | `city_unit_costs.json` | FY2026 `Fire Rescue Services` **$279,264,932** | 99.1% — and **moot**: `fire_response` has been read by nothing since 2026-09-05 |
| mill rates 2026 | `mill_rates.json` | not re-fetched (`vintage_report.check_mill_rates` reads `pwis-wc4c` monthly for the *year*) | — |

⚠️ **And the source moved while nobody was looking.** Between 2026-09-05 and
2026-09-15 the portal republished **FY2026**: 501 rows added, 490 removed, the
FY2026 tax-supported total **$4,044,711,032 → $4,045,178,891**, ETS +$2.5M,
Parks and Roads −$3.0M, Police +$3.5M. FY2025 is byte-identical. None of this
touches a committed value — every committed figure is FY2025 or FY2017 — but it
is the T1 mechanism demonstrated on a ten-day window: *the world moves and the
file does not, silently*. Three docs (`DATA.md` §17 ×3, `SPEC_breakeven.md`,
`DECISIONS.md` 2026-08-16) now carry a stale row count of 7,283; §17 corrected
here, the rest left as dated.

### T1b — would anyone know? ❌ NO for the world moving; ✅ YES for a hand edit

The brief's sentence *"nothing recurring can go red if they drift"* is **half
right, and the half it gets wrong matters for what to build**:

| mutation | what it models | result |
|---|---|---|
| M1 total ×10 | a hand slip | ❌ red by name: `test_budget_context_publishes_values_and_total` |
| M2 transit ÷10 | a hand slip | ❌ red by name: `test_committed_budget_file_components_reconcile` (and the shares pin would follow) |
| **M3 `year` 2025 → 2019** | **the label drifting from the values** | ✅ **892 passed, all guards green.** The About panel would print *"Share of the City's $3.8B 2019 operating budget"* |
| M4 2026 Residential 7.7419 → 8.7419 | a wrong rate, `status.json` not regenerated | ❌ red by name: `test_committed_status_matches_the_rate_source` |
| **M4′ same + `generate_status.py` re-run** | **a wrong rate, propagated consistently — what a refresh does** | ✅ **892 passed; `check_year_alignment` exit 4 (identical to clean — the known Socrata-metadata inconclusive), `check_cost_copy` 0, `check_doc_citations` 0** |
| M5 `roadway_ops.maintenance` 5970 → 5907 | a rate edit the copy did not follow | ❌ `check_cost_copy` exit 5 + `test_the_shipped_copy_matches_the_shipped_rates` |
| M6 transit gross 436.6M → 463.6M | same | ❌ same two |

So the files are pinned against **edits** (four of the five pins red by name —
the S159 brief under-credited `test_generate_status.py`, which pins the total,
the component sums *and* the four shares to two decimals). They are not pinned
against **staleness**: M3 is the label saying 2019 over 2025 dollars, and M4′ is
the refresh path — the rate is wrong, `status.json` agrees with it, the pod
prints it, and every check that runs at the merge gate is green.

**Downstream, one detector exists for M4′ and it is coarse.** A +13% residential
rate moves `total_revenue` by ≥10% in any hood over ~77% residential, and
`check_revenue_deltas.py` (weekly, files a GitHub issue — a channel with a
reader) flags a hood at **≥10% AND ≥$1M**. So a gross rate error surfaces one
week later as a wall of ⚠️ *Big revenue delta* issues; a transposition
(7.7419 → 7.4719, −3.5%) does not. Nothing at all detects a stale
`city_budget_context.json`: its consumers are the pod and `test_generate_status`,
and neither reads the City.

### What the cheapest guard is (brief T1 (b)) — modelled on the precedent the brief names

`vintage_report.check_mill_rates` is the shape: monthly, fetches the source,
compares *what is published* to *what the file carries*, reports to the digest
that files an issue. `city_budget_context.json` has no sibling. Proposed, **not
built** (it adds a `CHECKS` member and therefore changes what the digest says —
a CI-behaviour change under the project's proposal rule):

- **`check_budget_context()`**: fetch `operating_budget.csv` (already proven
  reachable from CI's network path — `budget.edmonton.ca`, §17); compute the
  newest `budget_year` with `Tax Supported` rows; compare to
  `total_operating_budget.year`. **ACTION** when a newer FY exists (today: FY2026
  at $4.045B vs the pod's 2025 at $3.8B — a year stale, labelled honestly, and
  nobody was told). Then re-derive the two figures the portal *can* check —
  `Roadway Maintenance` FY2017 and `Snow and Ice Control` for the pinned year —
  and ACTION on any change. Transit and sidewalks come from other publications
  and stay unchecked; say so in the digest line rather than pretend.
- The `mill_rates.json` *value* side is a second, separate gap: `check_mill_rates`
  compares years only. `pwis-wc4c` carries the rates; comparing the pinned
  year's five class rates to the file is one more loop in the same function.

Not proposed: a fetch in `tests.yml`. The merge gate must not depend on a City
server being up.

---

## §4 — T2: literals beyond `check_cost_copy`'s seven

### The seven hold, cross-model ✅

`FINDINGS_vacuous_guards.md` V1's fix (the guard reads reader-visible prose, not
the file) re-confirmed by falsification from the copy side: blurb `$5,970` →
`$5,907` with the JSON unchanged → **exit 5**; then the correct `$5,970` planted
in a code comment beside `SERVICES` → **still exit 5**. And from the file side
(M5, M6 above). The guard cannot be satisfied by a comment and it goes red in
both directions.

### Three literals with no guard — ⚠️ all three public-reachable

| # | literal | surface | falsification | why it matters |
|---|---|---|---|---|
| **L1** | `$600,000` / `$1,900,000` (*"to operate and maintain … to renew and replace"*) | `roadslife` blurb, **public** | JSON `operate_and_maintain` 600000 → 650000: **892 passed, `check_cost_copy` 0**. Copy `$600,000` → `$650,000`: **`check_cost_copy` 0, 22 passed** | These are the two City figures `roadway_om_renewal.value` is *derived from* (`$2.5M / 50 yr`). They live in the JSON as `source.published_figures_per_km_neighbourhood_road` — numeric fields, so a `CLAIMS` row is a two-line addition. The rate's unit is already flagged unconfirmed (`⚠️_unit_unconfirmed_2026_09_09`); if it is corrected, the derivation changes and this sentence will not |
| **L2** | `~0.9% of units 2021–25` | `infill` blurb, **public** (Development button) | `0.9%` → `9.0%`: **892 passed** | A *measured* figure — S56's D3 disclosure (suites = 0.9% of Lens A units, 2026-07-16) — typed into copy and never recomputed. The permits feed refreshes weekly; the number is two months and one year-roll old and nothing re-derives it |
| **L3** | the `2021–25` in the same sentence | same | `2021–25` → `2020–25`: **`test_window_labels` 6 passed** | ⚠️ **This is the F4 shape, inside F4's own blind spot.** `test_no_user_facing_string_spells_a_window_out` matches `f"{a}–{b}"` with four-digit years (`2021–2025`); the blurb abbreviates the end year. When `PERMIT_YEARS` rolls in January 2027 this label will not, and the guard built on 2026-08-28 to make exactly that loud will stay green |

Cheap future row, not a defect: `2017` in *"the City's 2017 maintenance figure"*
(`roadscost` blurb, public) restates a vintage the JSON records only in prose
(`rescoped_2026_09_06`); a `vintage` field plus a `CLAIMS` row would tie it.

---

## §5 — T3: formatting that can misstate — one drifted clamp, sweep not completed

The brief's two precedents (`fmtSvcRatio`'s `<0.1%`, the revenue panel's two
decimals) are guarded by verify scripts. The hand-set colour clamps are the
literal kind hiding in the computed column: `colorClamp` is typed in, the legend
prints it, and its comment claims a percentile. Re-derived from the served file
(358 non-set-aside hoods):

| metric | clamp | p97.5 today | clamp ÷ p97.5 | hoods saturating |
|---|---|---|---|---|
| `revenue_per_acre` | **$50,000** | **$57,412** (p97 $52,261) | **0.871** | **16 (4.5%)** |
| `res_revenue_per_acre` | $30,000 | $28,924 | 1.037 | 7 |
| `nonres_revenue_per_acre` | $50,000 | $50,216 | 0.996 | 10 |
| `value_per_acre` | $4,000,000 | $4,028,947 | 0.993 | 10 |

S104 (2026-08-09) recorded the `$50k` clamp *"still at p97.0"*; it is now below
p97 and saturates 4.5% of hoods against a 2.5% design. `verify-res-revenue.js`
and `verify-smoke.js` pin the legend **strings** (`$30k+`, `$4M+`), so a guard
exists and it is the presence kind — it would pass with the clamp at $5,000.
Whether 0.871 is a defect is a design call (the clamp is deliberately a literal
so the colour scale is stable across refreshes — `DECISIONS.md` should say which
wins, stability or percentile); what this audit establishes is that **nothing
measures it** and the S104 statement is already stale.

`fmt*` functions were **not** swept beyond this; T3 is reported partial.

---

## §6 — T4: surfaces the instrument does not reach — enumerated, not audited

Same regex, applied to the source text with tags stripped:

| surface | distinct numeric claims | guard |
|---|---|---|
| `README.md` | 21 | none recurring (`check_doc_citations` checks pointers, not figures) |
| `web/notebooks/historical-2024-gap.html` | 55 | re-run by hand only (`EVIDENCE_NOTEBOOKS.md`) |
| `web/notebooks/exemption-uncertainty.html` | 47 | same |
| `web/notebooks/roll-year-metadata.html` | 24 | same |
| `web/notebooks/school-coverage-gap.html` | 2 | same |
| `web/verified/01_money_lens.html` | 18 | **regenerated every refresh** — computed, covered |

Plus: tooltips and the peek card; the grid legends; any phone-only readout.
**No coverage claim is made for any of these.**

---

## §7 — What the brief got wrong, and what it got right

Wrong: the surface count ("6 views"; Money missing), the public exposure (18
unreachable claims counted), the `$50` row, and *"nothing recurring can go red"*
(four pins do, for edits). **Right, and the reason to keep the brief:** the
three-way sort, the ranking of manifest above literal, the out-of-scope line
(*whether the numbers are correct*), and the instruction to fix the instrument
before believing it — which is where this run spent its first hour and found
its first three defects.

The brief's §2 and §3 are amended in place to the corrected numbers; §0–§1 and
§4–§5 stand.

## §8 — This run's own errors

1. The first M4 read *"892 passed"* and was **wrong** — the mutation had not
   been verified as applied before the suite ran (the same heredoc block had
   just failed on M3's assertion, and the two results were read together).
   Re-run with `git diff` shown and the test named: red. Recorded because a
   green read off an unverified mutation is the exact failure
   `commit-before-falsifying` describes.
2. `cd tools/profiling` persisted across tool calls twice and made a probe run
   against paths that did not exist (`sed: can't read web/index.html`); the
   probe reported exit 0 because the *guard* never ran. Re-run from the root.
3. The public reachability of `glass` / `change` / `infill` is inherited from
   their parent button, not measured from their own toggles — an approximation
   stated in the instrument.
