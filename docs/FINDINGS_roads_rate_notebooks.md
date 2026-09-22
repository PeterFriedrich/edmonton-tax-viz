# FINDINGS — the two roads justification notebooks, audited

**Run:** 2026-09-22, S187, **Opus 5.5**, effort `high`. `docs/AUDIT_LEDGER.md`
S173–S186 backlog item #2. ⚠️ **Same model family as the author (Opus 5), who
also shipped both rates.** This run is a different model, not an independent
one.
**Target:** `notebooks/standalone/roads_lifecycle_rate.py` (#474, defends
$50/road-m/yr) and `roads_operating_rate.py` (#509, defends $9.32/road-m/yr).
Both are **unpublished**, pending Peter's call (`docs/EVIDENCE_NOTEBOOKS.md`).
Both **postdate** the S172 cross-read (#473), so neither had been read by a
second model.
**Grounding read first:** DECISIONS 2026-09-03 (3% demoted), 2026-09-06
(re-scope), 2026-09-08 ×2 (1.29× demoted; lane-km stated not converted),
2026-09-17 ×4 (centreline unit, CFS implied life, App A, per-class life);
`DATA.md` §16; `FINDINGS_roadway_maintenance_rate.md` §2.
**Method:** ran both notebooks live. Separately re-fetched the three PDFs and
the budget CSV, and matched every hardcoded transcription against the fetched
text. Traced both cost columns through `web/index.html` and
`src/join_and_calculate.py`.

## Verdicts

| # | Level | Verdict |
|---|---|---|
| L0 | Fit to publish as a defence of a shipped number? | **CONDITIONAL, both** — no shipped number is wrong; three claims need downgrading first (§1, §3, §4) |
| **Lifecycle $50** | | |
| L1 | Source figures ($1.5M / $600k / $1.9M, 25 vs 50) | **SOUND** — all 5 quotes verbatim live, page reconciles to its own $4M |
| L2 | Centreline, not lane, km | **SOUND** |
| L3 | 50-year denominator | **CONDITIONAL**, as the notebook itself says; one omitted bias, and it runs *against* 50 (§2) |
| L4 | §7 "paved poor share rose 11.5 → 12.5" | **WRONG** — the same unlike-for-like composition error §7 diagnoses (§3) |
| **Operating $9.32** | | |
| L5 | Maintenance half ($65.671M FY2017) | **SOUND**; its "separate program" invariant is vacuous, and better evidence exists (§4b) |
| L6 | Snow half: §2's "genuine independent check" | **OVERCLAIMED** — it verifies the $67M total, not the 55% share that ships (§4a) |
| L7 | Lane-km unit, "floor", arterial *k* | **Decided 2026-09-08 — not re-opened**; the floor is conditional on *k* ≤ 3.3, which the notebook states |
| **Both** | | |
| L8 | The two bases are never summed on a served surface | **PASS** |
| L9 | Invariants as an instrument | **WARN** — the header claims every figure is checked against its source; 16 of the lifecycle notebook's 40 are arithmetic on constants (§5) |
| L10 | Transcriptions vs the fetched PDFs | **PASS** — every value checked matches (§5) |

## §1 — Both notebooks run green

40/40 and 22/22 invariants pass against live sources today. Every quoted
sentence (Development Impact page, Journal of Commerce, Taproot, Snow & Ice
report p4/p16, ISC 2020 p19) is present verbatim.

## §2 — L3: the audited-books cross-check has an unstated bias, and it runs against 50

`roads_lifecycle_rate.py` §4 derives the roadway system's implied life as
`gross cost ÷ annual amortization` = **36.4–38.0 years**. It lists four limits.
The third, *"exact only for a stock in steady state; the stock grew 4.6%"*, names
the wrong mechanism. Under straight-line amortization, growth alone doesn't bias
the ratio: each not-yet-amortized asset contributes `cost/L` either way.
**The bias that does exist, and goes unnamed, is fully amortized roads still in
service at gross cost.** They add to the numerator and contribute nothing to
amortization, so the ratio **overstates** the policy life. Schedule 1 shows
$157M of roadway disposals in the year, so some are written off, but the scale
is unknown.

**Direction:** the true accounting life is ≤ 36–38, further below the shipped
50. The notebook already records 36–38 "as it falls" and calls the 50 an
argument, not a measurement, so no verdict flips. But this is the one omitted
limit found, and it cuts against the author's position.
**Fix:** replace limit 3's mechanism with this one.

## §3 — L4: §7's "paved rose 11.5 → 12.5" compares a curbs-inclusive 2023 with a curbs-exclusive 2025

§7 correctly withdraws the "flat poor share" trend claim because the three
"Roads" rows are *differently composed aggregates*. Its own invariant then makes
that mistake: `PAVED_DF_25 - PAVED_DF_23 >= 0.5`, *"the paved sub-row … moves 11.5
→ 12.5, a rise, not a flat line"*.

ISC 2025 Appendix B p37, read from the fetched PDF:

| row | 2025 value | 2025 D+F | 2023 value | 2023 D+F |
|---|---|---|---|---|
| Roads | $10,484.3M | 11.2% | $9,747.5M | 11.4% |
| Paved Roads | **$8,204.2M** | 12.5% | **$9,704.5M** | 11.5% |
| Unpaved | $182.8M | — | $43.0M | — |
| Curbs | **$2,097.3M** | 7.0% | **not reported** | — |

2023 Roads = Paved + Unpaved exactly. Paved *falls* $1.5B while total Roads
*rises* $0.74B and a $2.1B Curbs line appears. **Curbs were almost certainly
inside 2023 Paved.** If they sat at a similar ~7% poor, 2023 paved without
curbs was ~12.6–12.7%, roughly flat against 2025's 12.5%, not a rise.

**Direction:** the correction is mildly *favourable* to 50 (no rising backlog).
The section's conclusion, that the trend doesn't discriminate 25 from 50, still
survives. What is wrong is only the invariant, and it would publish the exact
error the section exists to warn about.
**Fix:** drop the invariant, or restate it as "not comparable, since 2023 Paved
includes curbs".

## §4 — the operating notebook

### 4a — L6: the snow reconciliation checks the total, not the number that ships

§2 says the snow source earns its place because *"the article's two shares sum to
a programme total the City itself publishes … a genuine independent check,
unlike the one demoted in the lifecycle notebook … Two mechanisms, one answer."*
`DATA.md` §16 says the same: *"THE SNOW FIGURES ARE INDEPENDENTLY CORROBORATED."*

**$36.85M = 0.55 × $67M and $30.15M = 0.45 × $67M, both exactly.** The article
applies a percentage split to a rounded programme total, so the shares summing
to the total is arithmetic. The companion invariant *"the roads share is the 55%
the article states"* is the article agreeing with itself. What the portal check
actually establishes is that **the reporter's $67M matches the City's FY2025
$67,553,815 (99.2%)**, which is worth having. **The 55% roads share, the one
input that reaches the rate, rests on the staffer alone.** This is the same shape
as the 3% set-aside demoted on 2026-09-03: a check that verifies the part that
was never in doubt.

**Materiality:** each 5 points of share moves the snow half by $305/km, about
$0.31/m (3.3% of the rate). Nothing suggests 55% is wrong. The claim is
overstated; the number isn't known to be wrong.
**Fix:** reword §2 and `DATA.md` §16 to "the programme total is corroborated; the
roads/paths split is the staffer's", and keep the snow half as SECONDARY on the
split.

### 4b — L5: the "separate program" invariant proves nothing; the budget has better evidence

`check(... int(sn_by_year.loc[2017]) != MAINT_PROGRAM, "…a separate program … the
two halves do not double-count")`. Two programmes having different totals says
nothing about overlap. The fetched CSV has something much closer to evidence:

| FY2017 | Roadway Maintenance | Snow and Ice Control |
|---|---|---|
| Personnel | $50,786,000 | **none** |
| Intra-municipal Charges | **−$28,267,000** | **+$29,312,000** |

Snow & Ice employs no staff of its own and is charged ~$29M in. Roadway
Maintenance charges ~$28M out. That is the signature of maintenance crews' snow
time being moved across, which would make the net $65.671M snow-free. ⚠️ **This
suggests the separation; it doesn't prove it.** The two figures differ by $1.0M,
and charges can flow to other programmes. Untraced.
**Fix:** replace the vacuous check with this mirror, stated at its true strength.

## §5 — L9/L10: what the invariants actually verify

The lifecycle notebook's header says *"Every figure below is fetched live … and
checked against the transcription printed here."* Of its 40 invariants:

- **24 read the fetched source**: quotes, page titles, "lane" count, Note 1
  range, App A row presence, the 2025 Roads/Curbs strings, the live budget draw.
- **16 are arithmetic on hardcoded constants.** They include the whole Schedule 1
  table (8 classes × 3 figures) behind the 36.4–38.0 headline, App A's expected
  lives and average ages (the ~25.9-year figure), and the 2025 paved/curbs poor
  shares. One (`total == 4_000_000`) is asserted twice.

**No transcription error turned up:** I matched all 24 Schedule 1 values (PDF
page 12, printed p79), every App A life, age and condition value, and every App B
share against the fetched text. The weakness is in the instrument. The monthly
recheck (`scripts/recheck_evidence_notebooks.py`) counts all 40 as invariants, but
for these tables it cannot detect the source changing under the transcription.
That is the S144 vacuous-guard class, and it feeds S173–S186 backlog item #4.
**Fix:** assert each constant appears in the fetched page text, as §5 already
does for App A lane-km. That is cheap, and the values are on known pages.

The operating notebook is similar but smaller: $5,970, $3,350, $9.32, the 55%
share, the [repo] centreline table, 0.086%, *k* = 3 and 3.0× are constants or
arithmetic.

## §6 — L8 and smaller items

- **L8 PASS.** No served surface sums `cost_roads_life_per_acre` and
  `cost_roads_ops_per_acre`. The Services panel groups rows by basis
  (`SVC_COST_BASES`), and `transport_cost_ops_per_acre` is operating-only.
- **Stale "~5.4×"**: `web/index.html` (two comments) and
  `src/join_and_calculate.py` still describe the bases as "~5.4x apart", the
  figure operating §7 says is a unit artifact (~3.0× on one unit). Comments only,
  not reader-facing.
- **"40-year" vs 50**: `data/city_unit_costs.json` `roadway_ops.caveat` says
  capital reconstruction runs on a *"40-year full-reconstruction cycle"*. The
  lifecycle basis uses 50, and nothing in either notebook supports 40. Not served.

## What this run got wrong

- **I nearly reported Schedule 1 as unsourced.** The notebook cites "p79", and
  the fetched PDF has 58 pages, so my first extraction indexed past the end. The
  values are on PDF page 12. "p79" is the printed page label. Caught by searching
  for the values rather than trusting the page number.
- **§3's "curbs were inside 2023 Paved" is an inference from value arithmetic**
  (2023 Roads = Paved + Unpaved exactly; paved −$1.5B while curbs +$2.1B appear),
  not from anything the report says. The ~12.6–12.7% ex-curbs estimate further
  assumes 2023 curbs sat near 2025's 7% poor.
- **§4b's intra-municipal mirror is suggestive and untraced.** −$28.27M and
  +$29.31M are not equal, and I didn't follow either charge to its counterparty.
- **Several verdicts favour the numbers I was auditing, and the author shares my
  model family.** §3's correction and §4b's evidence both *support* the shipped
  rates. The two findings that cut against them (§2's bias, §4a's overclaim) are
  about provenance, not magnitude. A different model family should read §2 and
  §4a before either is acted on.
