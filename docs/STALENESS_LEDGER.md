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

**Totals: 25 distinct items · 8 CORRECTED · 17 ACCURATE** (was 20 / 7 / 13
before pass 7).

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
   sampled** — still the most likely place for an untouched stale claim.
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
