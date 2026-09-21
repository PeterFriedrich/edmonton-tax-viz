# STALENESS LEDGER — which `TODO.md` items have been re-verified, when, and what came back

One row per **item checked** by the `TODO.md` staleness audit. `CLAUDE.md`'s
rule is that an *open* item can be stale — "reproduce the symptom and re-measure
the stated cause before acting on it" — and a hand sample of 15 items untouched
>60 days found **7 stale (47%)** (`DECISIONS.md` 2026-09-16). This file is the
coverage map for that work.

⚠️ **Why this is NOT in `TODO.md`.** Two reasons, both measured:

1. **The loaded path.** `TODO.md` is ~89% of what every session reads, and the
   audit's own progress notes had grown to **11.6 KB in a single line** —
   S166 recorded that its four progress notes added back over half the space the
   relocation had just freed. *"If this resumes, record progress somewhere that
   is not the loaded path, or the audit pays for itself in the currency it is
   trying to save."* This file is that somewhere; it is **not** session reading.
2. ⚠️ **A dated tag inside an item corrupts the cohort metric it is measured
   by.** The cohort is defined below as *the newest date in the item body* — so
   writing "checked 2026-09-20" into an item **moves it out of its own cohort**.
   Pass 5 hit exactly this: it annotated 3 items with that day's date and the
   band it was working shrank from 12 to 8 underneath it. Keeping the record
   **external** is what makes the metric stable.

## Definitions — none of these were written down before 2026-09-20, and all three were ambiguous

| term | definition | value on 2026-09-20 |
|---|---|---|
| **unit** | one checkbox at any depth inside the `## Open work` span | — |
| **denominator** | open boxes (`- [ ]`) in that span | **100** (65 top-level + 35 nested) |
| **cohort** | **the NEWEST date appearing in the item body** = when anyone last touched it | >60 d: **5** · 30–60 d: **13** |
| *(rejected)* | oldest date in the body = when it was opened | >60 d: 25 · 30–60 d: 29 |
| **undated** | items carrying no `YYYY-MM-DD` at all — **invisible to either metric** | **21** |

⚠️ **"18 of 103" was never a coverage figure** and should not be quoted. `103`
was wrong (the file has held **100** open boxes at both S169 and today, 65 of
them top-level), and the numerator was a running tally kept in prose with no
per-item record, so it could not detect a re-check. **The 21 undated items are a
new finding of 2026-09-20** — a fifth of the backlog cannot be placed in any
cohort, and no pass has ever selected from them.

⚠️ **The unit was never fixed either.** Of the 20 items below, **16 are real
checkboxes and 4 are claims living inside another item's body** (marked
`sub-claim`). That is why pass 3 reported "3 more" while naming four things.
**Count boxes; record a sub-claim under its parent box.**

## Checked items

Identified by quoted text, **never by line number** — those drift.

| # | pass · date | item | verdict | what came back |
|---|---|---|---|---|
| 1 | 1 · 2026-09-16 | `MOBILE USABILITY` | **CORRECTED** | *"zero `@media` queries today"* — `styles.css` has **6**, and `MOBILE_USABILITY.md` documents the 640px seam plus a CONFIRMED 390×844 pass |
| 2 | 1 · 2026-09-16 | `OUTREACH TRACKER` | **CORRECTED** | said *"five data issues"*; the register had grown. **Re-corrected 2026-09-20** — see below |
| 3 | 1 · 2026-09-16 | `▶ BREAK-EVEN LENS — STILL NO CODE` | ACCURATE | only comments denying it exist |
| 4 | 1 · 2026-09-16 | `A TRUE BIKEWAY LIFECYCLE $/m/yr STILL DOES NOT EXIST` | ACCURATE | the JSON's own `_status` agrees |
| 5 | 1 · 2026-09-16 | Services hover teases a chart its panel won't open — *sub-claim* | ACCURATE | `index.html`'s own comment confirms the defect; only the predicate NAME was stale (`hasSvcCost` → `hasRoadsLife`), fixed |
| 6 | 1 · 2026-09-16 | `THE RATIO AND USES PRISMS STILL PICK THE HOOD BEHIND THEM` | ACCURATE | `pickable: false` on both layers |
| 7 | 1 · 2026-09-16 | `Zoom-gating does not exist yet` | ACCURATE | ⚠️ **near-miss** — `placeSize()`/`PLACE_MIN_ZOOM` scale labels with zoom, but no show/hide GATE exists, so the item stands |
| 8 | 2 · 2026-09-16 | per-year archive filenames — *sub-claim* | **CORRECTED** | the archive already EXISTS (`data/temporal_archive.json`, `SPEC_temporal.md` ✅ 2026-07-28); only the year selector is open. ⚠️ **near-miss** — nearly called DEAD, but the lens is per-neighbourhood by design so the selector genuinely does not exist |
| 9 | 2 · 2026-09-16 | `Auto-fetch matching pwis-wc4c rates` | ACCURATE | `download_data.py` still does not fetch rates; the digest only CHECKS them |
| 10 | 2 · 2026-09-16 | `P2.3d S2` | ACCURATE | `docs/security-audit.md` exists |
| 11 | 2 · 2026-09-16 | P2.5 doc-drift — *sub-claim* | ACCURATE | `ARCHITECTURE.md` *"drift flagged, NOT fixed"* still stands |
| 12 | 2 · 2026-09-16 | `MA DERELICT RESIDENTIAL` | ACCURATE | `apply_tax_rates.py:37` maps it exactly as described |
| 13 | 3 · 2026-09-17 | `A2 — Shovel-ready industrial land` | **CORRECTED** | its INPUT was 19 months stale. ✅ **CLOSED 2026-09-20 (S179)** — `stt5-pzaa` is DEFECTIVE, filed as `DATA_ISSUES.md` §7 |
| 14 | 3 · 2026-09-17 | `Visual polish` | ACCURATE | all four claims re-checked against the tree |
| 15 | 3 · 2026-09-17 | `Utility cost lenses` | ACCURATE | already carried accurate 2026-09-16 corrections |
| 16 | 3 · 2026-09-17 | `PUBLIC RELEASE PREP` | ACCURATE | same |
| 17 | 5 · 2026-09-17 | `⚠️ DATA VINTAGE` | **CORRECTED** | two dates ~2 months stale (`data/raw/` is 2026-09-03 not 07-06; last auto-refresh 2026-09-14 not 07-27). Hazard live, gap 11 days not three weeks. ⚠️ **its 1,896-values blast radius was NOT re-derived** |
| 18 | 5 · 2026-09-17 | `⚠️ --geojson-out /tmp/x.geojson DOES NOT…` | **CORRECTED** | code claim re-verified, but the TITLE accused another item of advice it stopped giving on 2026-08-07; struck |
| 19 | 5 · 2026-09-17 | `verify-peek.js IS FLAKY UNDER PARALLEL LOAD` | ACCURATE | 3/3 green run alone, 38 checks |
| 20 | 6 · 2026-09-17 | Services hood-panel track narrow-width prediction — *sub-claim* | **CORRECTED** | **FALSIFIED by measurement** — the track is 210px at 390px against a 164px desktop control, i.e. WIDEST on a phone. The real limit is the VALUE, not the viewport |
| 21 | 7 · 2026-09-20 | `T3 — #revcut does not reach the panel` | ACCURATE | `revenueMix = p => REV_CATEGORIES.filter(…)` takes only `p` and reads no cut; the headline reads `p.total_revenue` / `p.revenue_share_city`, neither cut-aware; `#revcut` only calls `applyMetric`. **Both quoted figures reproduce exactly** — DOWNTOWN `$146.40M` and `5.26%` |
| 22 | 7 · 2026-09-20 | Retrieval logging (struck title, open box) | ACCURATE **+ material caveat** | The hook is live and working — 157 entries across 20 sessions since 2026-09-16. ⚠️ **But its matcher is `Read\|Grep\|Glob`, so a doc opened with `sed`/`grep`/`cat` in Bash is INVISIBLE**: three Bash file-reads produced **0** log entries, falsified directly. See the warning below |
| 23 | 7 · 2026-09-20 | `B2 — Regional non-res mill rates` | ACCURATE | `2026_tax_rates.xlsx` still on the FIR dataset page 64 days after *"verified live"* (filename is lowercase; the item's `2026_Tax_Rates.xlsx` is a casing slip, not a dead link) |
| 24 | 7 · 2026-09-20 | `B1 — Regional non-res assessment share` | ACCURATE | the equalized-assessment page carries exactly the **2024 / 2025 / 2026** XLSX workbooks claimed, still XLSX and not PDF-only |
| 25 | 7 · 2026-09-20 | `A4 — Assessment-lag methods note` | **CORRECTED** | its stated blocker *"likely Peter/laptop"* is **FALSIFIED** — `www.edmonton.ca` and `pub-edmonton.escribemeetings.com` both return **200** from the Oracle box. The memo itself is still unfetched; nothing stops a session here from doing it |
| 26 | 8 · 2026-09-21 | `Selective/partial data regen (DEFERRED)` | **CORRECTED** | ⚠️ **its stated payoff is FALSIFIED.** *"roads static 2+ mo while permits/fire change daily"* — row-level `max(:updated_at)` puts **Road Network at 2026-09-19** and zoning at 2026-09-14 against permits at 2026-09-19: same cadence, not static. The genuinely static sources are **GTFS (93–153 d)** and **school locations (139–151 d)**, which are small, so the optimization is worth less than the item claims |
| 27 | 8 · 2026-09-21 | `B3 — Industrial-areas context map` | **CORRECTED** | its blocker *"municipal boundary layer source to verify"* was **resolved 2026-08-03** — `reference.geojson` ships 15 `t="boundary"` outlines including the four counties **and Industrial Heartland**. Six weeks stale; only the map is left |
| 28 | 8 · 2026-09-21 | `D4 — sanitary trunk callout` | ACCURATE **+ material caveat** | the SSTC/EA pause is still in force, but the City states it lasts *"for the duration of the… Transformation project… expected to be completed by **Quarter 1 2027**"*. ⚠️ The item's word *"currently"* has an expiry ~2 quarters out, which a shipped panel line would outlive silently |
| 29 | 8 · 2026-09-21 | `D1 — levy performance mini-viz` | ACCURATE | the off-site levy page still lists **2022/2023/2024** annual reports and no 2025 one, so *"cumulative $3.83M end-2024"* is still the newest published figure; `$3,033,592` / `$3,259,866` / `$32,813` all reconcile to `fable_brief_debt_lens.md` |
| 30 | 8 · 2026-09-21 | `D3 — Blatchford contrast case study` | ACCURATE | `$32,813/ha` is in the D0/D1 table exactly as claimed (`fable_brief_debt_lens.md:31`, `:84`) |
| 31 | 8 · 2026-09-21 | `Lens B optional refinement` | ACCURATE | ⚠️ **near-miss** — the lens itself SHIPS (`#devmode` *Infill opportunity*, `z(suitability) − z(activity)`), which is precisely the item's premise that *"the single diverging map already shows both"*; the one-sided toggles it proposes still do not exist |
| 32 | 8 · 2026-09-21 | `Lens C — Activity vs City Service Cost` | ACCURATE | ⚠️ **near-miss** — `construction_value` IS used, in `load_permits.py`, but the item says *"NOT used **here**"* and Lens C is not built. Check the claim, not the string |
| 33 | 8 · 2026-09-21 | `Peter's call: ingest an income variable` | ACCURATE | no income variable anywhere in `src/`, `data/DATA.md` or `web/index.html`; still an undecided call, not a lapsed one |
| 34 | 8 · 2026-09-21 | `Display/chart — undecided design` | ACCURATE | no non-map panel exists; unchanged |

**Totals: 34 distinct items · 10 CORRECTED · 24 ACCURATE** (was 25 / 8 / 17
before pass 8).

⚠️ **PASS 8'S FINDING IS THAT A DEFERRED ITEM'S *JUSTIFICATION* GOES STALE
FASTER THAN ITS *CLAIM*.** Both corrections (rows 26, 27) were items nobody was
about to act on, and in both the thing that had rotted was the sentence saying
**why** it was worth doing or what stopped it — the roads-are-static premise,
the missing boundary source. Neither item's headline was wrong. **A deferred
item is read for its blocker, so a stale blocker is the expensive half**; this
is the same shape as row 25 (`A4`), where the blocker was also the wrong part.

⚠️ **Decomposed per rule 5, and it cuts against the audit:** pass 8's 2-of-9
yield is the *lowest* of any date-defined cohort, and neither correction changes
what gets built next. The undated pool was predicted to be *"the most likely
place for an untouched stale claim"* — **9 items in, it was not.** Two of the
nine (rows 31, 32) were near-misses in the audit's own favour: reading the topic
rather than the claim would have scored both as CORRECTED and made the pass look
twice as productive.

⚠️ **PASS 7'S BIGGEST FINDING IS ABOUT A MEASUREMENT WE ARE ABOUT TO ACT ON.**
The retrieval log (row 22) exists to answer *"is the doc apparatus
load-bearing?"* by showing which docs are never opened, with the decision rule
*"a doc never opened before an action is a prune candidate."* **It only observes
the `Read`, `Grep` and `Glob` tools.** Everything read through Bash — `sed -n`,
`grep`, `cat`, `head` — leaves no trace, and that is how much of this repo's
prose actually gets read: **this very session logged 8 `Read` entries while
touching several times that many files.** So the ~2026-09-30 readout will
systematically **undercount**, and the undercount is **biased toward exactly the
docs that get consulted in passing** — which is the prune rule pointed at
actively-used docs. ⚠️ **Do not prune anything on that table without first
either widening the matcher to include Bash or discounting the result.**
This is `check-where-the-value-can-be-wrong` in an instrument, again.
⚠️ **This is 20, where the prose running tally said 19** — pass 3 counted 3 and
named 4 (rows 13–16). Treat the reconstruction as authoritative and the old
tally as superseded; **35% corrected is well under the 47% the hand sample
suggested**, but both samples were shape-picked, so neither is a rate.

## Pass 4 was not an item pass

**2026-09-17 (S166) — external-dataset sweep.** Every Socrata id named in
`src/`, `scripts/`, `tools/`, `main.py`, `TODO.md` open work, `data/DATA.md` and
`docs/DATA_ISSUES.md`: 117 candidates → **26 real datasets**, asked when their
ROWS last moved. ✅ **Every ingested dataset was current.** Two outliers, neither
new work at the time: `stt5-pzaa` (now `DATA_ISSUES.md` §7) and `urjq-fvmq`,
which `DATA.md` §9 already documents as an href-only landing page.

⚠️ **The sweep was VACUOUS on its first run and printed a confident table
anyway** — it sliced `TODO.md` with `txt.index("## Open work")`, but the
preamble *talks about* `## Done`, so the slice was **39 characters**. The tell
was `stt5-pzaa` missing from a table built to find things like `stt5-pzaa`.
**Anchor on heading LINES and assert the slice is >50 KB** — the check used in
this file's own tooling. Same trap `CLAUDE.md` documents for `todo_archive.py`.

**This question is CLOSED — re-run the sweep, do not re-read the items.**

## What each pass selected, and what that means for the next one

| pass | cohort it drew from | yield |
|---|---|---|
| 1 | items asserting a **negative about the code** (shape-picked, not a date cohort) | 2 of 7 |
| 2–3 | >60 d | 2 of 9 |
| 4 | external datasets (not items) | pipeline clean |
| 5–6 | 30–60 d | 3 of 4 |
| 7 | **undated** (never sampled before) | 1 of 5 |
| 8 | **undated**, the remainder | 2 of 9 |

⚠️ **The yield changes SHAPE, not just rate.** Passes 1–2 found claims overtaken
by our own work — findable by reading. Pass 3 found an **external input that
went quiet**, which reading cannot find, only calling the source can. Passes 5–6
found **stale numbers inside items whose claims are still true**: a recent item
is likelier to be right-but-mismeasured than wrong, so **re-measure its figures
rather than re-litigating its premise.**

## Rules for the next pass

1. **Record every checked item here, ACCURATE ones included.** Pass 3's rule —
   don't annotate accurate items, to avoid growing the file — made an accurate
   item indistinguishable from an unchecked one, so later passes re-checked
   them: `THE RATIO AND USES PRISMS` and `A TRUE BIKEWAY LIFECYCLE` were both
   verified in pass 1 and both reappeared in pass 6's cohort of 8. **The file
   this protects is `TODO.md`, and this is not that file** — the reason for the
   old rule does not apply here.
2. **Never write a bare "checked, still fine" annotation into `TODO.md`.** It
   moves the item out of its own cohort for no informational gain (see the
   header). ⚠️ **A CORRECTION is different and belongs in the item** — the item's
   content genuinely changed, so it genuinely was touched. The rule bans
   no-op annotations on ACCURATE items, not real edits.
3. **Check the specific claim, not the topic.** Three near-misses so far (rows
   7, 8, and the pass-3 archive item) were all the same shape: the topic had
   moved on, the specific claim had not.
4. ⚠️ **The undated pool is the standing target, and it is SMALLER than it
   looks.** Of the 21 undated open items, **6 were already checked in passes
   1–3** (`P2.3d S2`, `pwis-wc4c`, `MA DERELICT`, `Visual polish` + its two
   children) — they simply carry no date, which is *why* they looked unsampled.
   **This file caught that on its first use; without it pass 7 would have
   re-checked all six.** Pass 7 took 5 of the remaining 15, leaving **10 never
   sampled**. ⚠️ **Pass 8 drained that pool (9 items — one of the 10 had since
   been dated by a correction) and the prediction was WRONG: 2 of 9, the lowest
   yield of any cohort.** The undated pool is now **exhausted, not promising**.
   The next pass has no obvious cohort left; pick by shape (pass 1's method,
   the best-yielding one) or re-run the external-dataset sweep, which is the
   only check that finds inputs going quiet.
5. ⚠️ **Decompose any number that flatters this audit before recording it.**
   Every instrument defect found so far — the vacuous slice, the double-counted
   spans, the 5 dropped open boxes, the shrinking band, "18 of 103" — inflated
   the appearance of progress. None inflated the appearance of failure.

## Cross-refs

- `TODO.md` → the audit's open item (one short box; this file holds the record)
- `docs/FINDINGS_doc_growth.md` §3 — the measurement that opened the work
- `docs/DECISIONS.md` 2026-09-16 — the 47% hand sample
- `docs/AUDIT_LEDGER.md` — executed audits of the *pipeline*; this file is the
  backlog's own staleness, a different thing
