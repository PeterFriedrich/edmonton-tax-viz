# AUDIT BRIEF — is the doc apparatus load-bearing, or is it ceremony?

**Read cold.** This is a reusable *instrument*. Coverage map: `docs/AUDIT_LEDGER.md`
(candidate 11).

⚠️ **This brief exists because the last attempt at this question failed, and the
failure is instructive enough that §0 is not optional.**

---

## §0 — The failure this brief corrects

On 2026-09-15 Peter commissioned an outside review of this project's documentation
apparatus and put it in front of the model. **The review is
`docs/external/REVIEW_doc_apparatus_2026-09-15.md`** — 111 lines, 9 numbered
recommendations across 3 stages.

What happened to it:

1. **It was digested into one sentence.** `docs/FABLE_AUDIT_published_numbers.md`
   §0 says *"an outside review … landed on one line worth keeping"* and quotes
   *"prose about correctness is not a control on correctness."* **No path, no
   citation.** The path survived only in an S159 handoff (archivable) and a TODO
   line. A read-cold instrument that summarises its own evidence cannot be
   re-grounded by whoever runs it.
2. **One of nine recommendations was carried, and it was the comfortable one.**
   Rec #3 (*confirm every published number has a golden test*) says do more of
   what this project is already good at. The other eight ask it to stop doing
   something. The brief was written by the model whose output was under review.
3. **The result was 314 lines of markdown and zero executable checks** — against a
   review whose central claim is that this loop is the problem. ⚠️ **Cross-model
   execution did not save it:** Fable ran the audit and still produced prose.
   The constraint has to be structural, which is §3.

**Scoreboard when this brief was written: 0 of 9 recommendations implemented.**

---

## §1 — Ground yourself, in this order

1. **`docs/external/REVIEW_doc_apparatus_2026-09-15_CLAIMS.md` FIRST, then the
   review `docs/external/REVIEW_doc_apparatus_2026-09-15.md` IN FULL.**
   ⚠️ **The review is kept verbatim and SEVERAL OF ITS NUMBERS ARE WRONG** — the
   claims file measures every one. The headline `0.68:1` ratio is really **1.79:1**
   (vendored libs and exported notebook HTML were counted as code, an error this
   project fed the reviewer); the "104 summaries in the loaded path" are **3**, with
   101 already archived. Reading the review without the claims file is how those
   become ground truth — the review's own §Q1 is about exactly that hazard.
   ⚠️ Do not work from any summary of the review, including §0 above. Its
   Recommendations section is your target list.
   ⚠️ **Re-measure before relying on any figure**; the claims file is dated.
2. `docs/FINDINGS_decisions_index_drift.md` — this project already measured its own
   `DECISIONS.md` contract collapse (13% one-sentence compliance, median row
   138 → 2,219 chars). ⚠️ The review's diagnosis was **confirmed** here and then
   dismissed as *"already measured and deliberately blessed"*; Peter's call on it
   is still open. Do not repeat that move.
3. **`python tools/retrieval_report.py`** — the read-frequency table (rec #1, the
   only recommendation executed before this brief; hook in `.claude/settings.json`,
   raw log `~/.claude/retrieval-log.jsonl`). **It prints its own date range first and
   warns when it is too young.** Under ~2 weeks it cannot settle anything: say so and
   use it for nothing. ⚠️ A zero-read row is a prune *candidate*, never a verdict —
   the script's docstring says why.
4. `docs/AUDIT_LEDGER.md` — this file's own row, and the rows for the audits whose
   output volume is under review.

**Confirm one thing back before judging, with the measurement that proves it:**
the current counts of `docs/*.md`, `session-summary/` (top-level *and* archive),
`DECISIONS.md` bytes and rows, and the markdown-KB ÷ hand-written-code-KB ratio.
⚠️ **`measurements-that-favour-me` applies with full force here** — the last ratio
reported to Peter was **0.68:1 and the true figure was 1.61:1**, because vendored
libs and exported notebook HTML were counted as code. Decompose before reporting.

---

## §2 — The target list: all nine, no selection

The review's Recommendations section is the audit's scope. **You may not pick a
subset.** Every row gets a disposition; "not applicable" is a legitimate verdict
but must be argued from evidence, not from comfort.

They split by what they need, and the split is load-bearing:

| needs | rows | why |
|---|---|---|
| **MEASUREMENT** (read-logs, ablation) | 1, 2, 6 | The review's own Stage 1 is *instrument before you cut*, and its caveats say why: METR's perception-vs-reality gap means self-assessment is unreliable. ⚠️ **Rec #1 was executed 2026-09-16.** Until the log has weeks in it, these rows are `MEASUREMENT-PENDING` and that is the correct answer — not a stall |
| **DECISION** (shape questions) | 4, 5, 7, 8, 9 | Answerable cold, today. Whether per-session handoffs become one rewritten file; whether `DECISIONS.md` splits and cites test IDs; the prune cadence; test-before-prose as a default; a ratio ceiling. **This is where the audit earns its run** |
| **EXECUTION** (already scoped) | 3 | Audited 2026-09-15 (`docs/FINDINGS_published_numbers.md`) and left **three public literals and one drifted clamp unguarded, written down instead of fixed**. Rec #3 is not closed by that findings doc |

⚠️ **Rec #4 and #5 are decisions only Peter can make** — they delete or restructure
his records. Your job is the argument and the measurement, put sharply enough that
he can decide. Do not "implement" them.

---

## §2a — ⚠️ TEST THE PREMISES, NOT JUST THE NUMBERS

The `_CLAIMS.md` file checks the review's **arithmetic** about this repo. Nobody has
checked its **reasoning**. ⚠️ **A recommendation whose premise is false is not
disposed by executing it** — and the premises below are the ones that, if wrong,
change what the right answer is. Test each; **say which way it went**, because
several of these could come back *strengthening* the review.

⚠️ **This section is not a licence to reject the review.** The measured finding so
far is that its thesis is **understated** (`_CLAIMS.md` #1). A run that contests
every premise and executes nothing has found the comfortable answer, and should
distrust itself accordingly.

| # | premise the review rests on | why it is worth testing here |
|---|---|---|
| **A1** | *Cost is spread across all the artifacts.* | An unread doc costs **zero tokens**. `CLAUDE.md` loads 22 pointers; `docs/` holds **80** files. So the real cost of the other 58 is **staleness risk**, not context bloat — a different problem with a different remedy. ⚠️ Recs #6 and #9 are argued from mass; if the cost is staleness, **pruning and dating are not the same move** |
| **A2** | *A markdown-to-code mass ratio is a meaningful signal (rec #9).* | ⚠️ **The review warns about Goodhart's Law and then proposes a ratio target.** A ratio says nothing about whether any given doc earns its place, and a ceiling is gameable by writing longer code. Is rec #9 self-undermining on the review's own terms? |
| **A3** | *Ablation can measure a doc's value (recs #2, #6).* | ⚠️ **The review's own cited study cuts against it**: Khatri found *"injection strategy does not measurably move correctness"* and concluded context files are *"behavior steering, not capability injection"* — and the review adds that detecting a ~10pp effect needs **120–200 tasks**. If correctness cannot move, **ablation-by-correctness cannot detect value**, and rec #6 may be unrunnable at this project's scale. What *would* be measurable — process effects, wall-clock, repeated mistakes? |
| **A4** | *The reader of these docs is the agent.* | ⚠️ **The sharpest one, and it is the blind spot of the instrument I built.** `tools/retrieval_report.py` measures **agent** reads only. But ~29 of `docs/` are `FINDINGS_*`, `DATA_ISSUES.md` and `EVIDENCE_NOTEBOOKS.md`, whose intended reader is a **skeptical outsider checking a public civic claim** — a journalist, a councillor, Edmonton Open Data. A zero-read row for one of those means *the agent never opened it*, **not** that it has no reader. Pruning on that signal would delete the artifacts the public release exists for |
| **A5** | *This is a solo project, so the apparatus is disproportionate.* | The review's own thresholds say the calculus shifts with an audience. `docs/PLAN_public_release.md` is active work. Does "solo" still describe a **published** civic analysis whose methodology is meant to be independently checkable? |
| **A6** | *Append-only is an anti-pattern; prune superseded entries (recs #5, #7).* | ⚠️ **This repo's error-catching has repeatedly depended on the superseded text still being there** — `AUDIT_LEDGER.md`'s S103→S104 amendment chain caught an **overstated correction**, which a prune would have erased along with the original. Is the audit trail a cost of append-only, or its point? What survives a prune that keeps corrections but drops originals? |
| **A7** | *Most decisions can become a test (rec #8).* | *"Why the neighbourhood is the unit of analysis"* is not testable; *"the road rate is $50/m/yr"* is. Where is the boundary, and what fraction of `DECISIONS.md` falls each side? ⚠️ Rec #8 is only as good as that fraction — and the review's own §Q3 concedes *"capture the why"* is durable |
| **A8** | *Auto-memory now covers the cold-start need (rec #4).* | Testable here, today: **34** auto-memory files exist for this project. Read them against the 3 live handoffs. What does each carry that the other does not? The review's own threshold is *"if auto-memory demonstrably carries continuity across the next ~10 sessions."* ⚠️ Memory files are also **undated assertions**, which is the staleness problem the review raises about docs — do they inherit it? |

**How to report a premise test:** one line per row — `HOLDS`, `FAILS`, or `UNTESTABLE
HERE` — plus what you measured. ⚠️ **A premise that FAILS re-opens the recommendation
built on it**, and that re-opening is a finding, not a dodge.

---

## §3 — ⚠️ THE OUTPUT CONSTRAINT (this is the part that makes the audit different)

The last run failed by producing a document. These rules forbid that shape:

0. **§2a's premise tests come first**, and a row whose premise `FAILS` is disposed
   against the *corrected* premise, not the review's. Report the premise verdicts
   even where they change nothing.
1. **Disposition per row, one of four words:** `EXECUTED` (the change is in the
   working tree), `DECIDED-NO` (argued and rejected, with the argument),
   `MEASUREMENT-PENDING` (named, with the measurement that would settle it and when
   it will exist), or `PETER-DECIDES` (§2 says recs 4 and 5 delete or restructure
   his records; you cannot execute those).
   ⚠️ **`PETER-DECIDES` is not an escape hatch, and its FORM is fixed**: a table of
   **2–4 concrete options**, each with what it costs, what it loses, and your
   recommendation — not an essay, and never a row you simply declined to think
   about. If you can dispose a row yourself, you must.
2. ⚠️ **A row parked in the backlog for a later session counts as NOT DISPOSED.** That is the
   move this project keeps making — F1 was confirmed by three sessions and fixed by
   none, and the 2026-09-15 audit added four more such rows on the day it was told
   this was the failure mode.
3. **The findings write-up may not exceed the lines of code and config it changes**,
   counting a `PETER-DECIDES` option table as if it were the code it proposes.
   Count before you write. If the honest answer is that nothing should change, the
   write-up is a paragraph, not a document — and *that is a valid outcome*, reported
   as such.
4. **Prefer editing an existing doc to creating one.** A new `FINDINGS_*.md` for an
   audit about doc volume needs an argument.

---

## §4 — Per-row questions worth asking (not a substitute for reading §1.1)

- **#4 (session-summary):** 3 live + 101 archived. The archive is already out of the
  mandatory path, which is half the review's remedy — so the live question is
  narrower than the review frames it: *does writing a NEW file per session beat
  rewriting ONE?* The retrieval log answers whether the 3 live ones are even opened.
- **#5 (DECISIONS.md):** 430 KB, 279 rows, growing. `FINDINGS_decisions_index_drift.md`
  found 98.8% of distinctive facts recoverable elsewhere but 12 rows carrying ~8
  unique values. ⚠️ **Those must be rescued into their owning docs before any trim** —
  that precondition is already recorded and is the thing a keen pruner will skip.
  The sharper half of the rec is *cite a test ID per decision that protects a
  published number*: that converts prose to an enforced constraint and is checkable.
- **#7 (prune cadence):** the repo has `tools/todo_archive.py` and a `## Done` rule
  for TODO. Does the same shape transfer, or does an append-only *decision* log
  differ in kind from an append-only *task* list?
- **#8 (test-before-prose default):** where would this live so it actually fires —
  `CLAUDE.md`, the audit skill, a PR checklist? A rule nobody reads at the moment of
  writing is the same defect one level up (`_classify` warned for ~70 days).
- **#9 (ratio ceiling):** a ceiling needs a numerator, a denominator and a place it
  is measured. Is it a guard, a digest line, or a number in a doc — and if the last,
  does that not fail rec #8 on its own terms?

---

## §5 — Out of scope, so nobody writes it

- **Whether the project's *analysis* is correct.** Different audit family entirely.
- **`data/DATA.md` and `docs/DATA_ISSUES.md`.** The review calls these load-bearing
  and non-inferable, and this brief accepts that. Do not propose pruning them.
- **The verify/test estate.** The review calls it the crown jewel and *under*-invested.
  Proposals that shrink it are out of scope; proposals that grow it are rec #8.

⚠️ **Conflict of interest, stated plainly:** every session that has touched this
question — including the one that wrote this brief — is the author of the artifacts
under review, and has an obvious interest in concluding they are load-bearing. The
retrieval log exists because the review says judgement here cannot be trusted.
**Weight the log over any argument in this file, including this one.**
