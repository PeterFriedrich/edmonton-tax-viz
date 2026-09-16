# Claims check — `REVIEW_doc_apparatus_2026-09-15.md`

⚠️ **Read this BEFORE acting on any number in that review.** The review is kept
**verbatim** (its evidentiary value is that it is unedited), so its factual claims
about this repo cannot be corrected in place. They are corrected here.

Measured **2026-09-16 (S160)** against `master` at `d3aee1f`. The review was written
**2026-09-15**, so one day of drift is expected and is not a criticism of it.

**Why this file exists:** the review's own §Q1 argues that *"an agent misled by stale
docs ships the mistake."* Importing a document full of unverified claims about the
repo, and instructing sessions to read it as grounding, is that hazard exactly. This
file is the mitigation. Re-measure before a run that turns on any of these numbers.

---

## Claims about THIS repo

| # | the review claims | measured 2026-09-16 | verdict |
|---|---|---|---|
| 1 | **markdown-to-code mass ratio ~`0.68:1`** (TL;DR; §Q1 gives *"4,736 KB vs 6,924 KB"*) | **`1.79:1`** — markdown **4,793 KB**, hand-written code **2,673 KB** | ❌ **WRONG, and wrong AGAINST the review's own case.** The 6,924 KB counts **2,001 KB of vendored libs** (`web/vendor/`) and **2,263 KB of exported notebook HTML** as code. Markdown does not approach parity — it **outweighs** hand-written code by 79%. ⚠️ **The figure came from this project** (S159 reported it to the reviewer), so the error is ours, not theirs |
| 2 | **`412 KB` append-only decision log** | `docs/DECISIONS.md` = **430 KB**, **279 rows** | ⚠️ **STALE, still growing.** +18 KB in the window where its growth was the finding |
| 3 | *"a per-session summary directory grown to **104 files**"*, *"**104** append-only summaries **in the loaded path**"* | **104 total: 3 top-level, 101 in `session-summary/archive/`** | ⚠️ **COUNT RIGHT, FRAMING WRONG.** `CLAUDE.md` says read only the latest and not to bulk-read the archive, so **3** are in the loaded path, not 104. Rec #4's *"archive the 104 out of the loaded path"* is **already done**; what remains is the narrower question of new-file-per-session vs one rewritten file |
| 4 | *"**~45** Playwright invariant checks"* | **43** `tools/profiling/verify-*.js`, **892** pytest | ✅ **HOLDS** |
| 5 | *"**~20** pointer docs"* | **22** entries in `CLAUDE.md`'s Key Files list | ✅ **HOLDS for the loaded set.** ⚠️ But `docs/` holds **80** `.md` files — **58 that `CLAUDE.md` never names**. The review did not have this number and it is the more interesting one for rec #6 |
| 6 | *"one-line-per-decision rule broke months ago; median row now **~2,200 chars**"* | `FINDINGS_decisions_index_drift.md`: median **138 → 2,219** chars, **13%** one-sentence compliance | ✅ **HOLDS** — independently measured here 2026-09-04, before the review |
| 7 | *"Ratio drift: **~2 doc lines changed per 1 code line**"* | **1.27:1** over 90 days; **1.80:1** over 30 days (vendored + exported HTML + generated `CODEMAP.md` excluded) | ⚠️ **DIRECTIONALLY RIGHT, OVERSTATED at 90d.** The 30-day figure is close to the claim, and is **rising** |
| 8 | *"Contract collapse is the clearest single tell"* applied to `DECISIONS.md` | Confirmed by `FINDINGS_decisions_index_drift.md` | ✅ **HOLDS.** ⚠️ **The S159 handoff scored this ❌** as *"already measured and deliberately blessed"* — that is not a refutation, it is a confirmation with a shrug, and **Peter's call on it is still open**. Do not reuse that dismissal |
| 9 | *"your golden/invariant test suite … is genuinely load-bearing"* | The 2026-09-15 published-numbers audit found the suite pins manifest inputs against **edits** (4 tests red by name) but **not** against staleness | ✅ **HOLDS, with a limit the review did not have** — `FINDINGS_published_numbers.md` §3 |
| 10 | *"one prevented-error anecdote"* (a decision record preventing a silent redefinition) | Real: `AUDIT_LEDGER.md` 2026-09-15 (S159) T2 — a wired-in "fix" would have silently re-scoped a published number | ✅ **HOLDS** |

## Claims about the outside world

| # | claim | status |
|---|---|---|
| 11 | METR RCT — 16 devs, 246 tasks, 19% slower / 20% perceived faster | ✅ **Checked S159**, matches independent knowledge |
| 12 | A `PostToolUse` hook can log every `Read`/`Grep` | ✅ **PROVEN HERE 2026-09-16** — the hook is live in `.claude/settings.json`, read with `tools/retrieval_report.py`. This is rec #1, executed |
| 13 | Claude Code auto-memory / `/memory` / Dreams duplicate the handoff need | ✅ **Partly confirmed** — auto-memory is live for this project (**34** memory files). Whether it *substitutes* for the handoff is rec #4's open question, not a settled fact |
| 14 | Chatlatanagulchai et al., arXiv:2511.12884 (2,303 context files; Flesch ~16.6; 67.4%) | — **NOT VERIFIED HERE.** No offline copy; the specific statistics are unchecked |
| 15 | Khatri arXiv:2607.27250; Gloaguen arXiv:2602.11988; the *"71% cut, nothing broke"* and *"delete your CLAUDE.md every 6 months"* reports | — **NOT VERIFIED HERE.** ⚠️ The review **self-caveats** all of these as unreviewed preprints or practitioner reports. Treat as directional; do not cite as evidence for a deletion |
| 16 | Documentation-debt cost figures (47% effort / 48% cost, Mendes 2016 / Stochel 2012) | — **NOT VERIFIED HERE**, and relayed second-hand through arXiv:2212.01479 in the review's own framing |

---

## What this changes about how to use the review

1. **Its central thesis survives, and #1 strengthens it.** The disproportion is real
   and **larger** than the review argued.
2. **Rec #4 is half-done already** (#3): the archive is out of the loaded path. Audit
   the remaining half, not the whole.
3. **Rec #6 has a bigger target than stated** (#5): 58 `docs/*.md` files are never
   named by `CLAUDE.md`. The retrieval log (#12) is what settles which are opened.
4. ⚠️ **Do not cite #14–#16 as grounds for deleting anything.** Unverified here, and
   self-caveated there. The measurements in this repo (#1, #2, #6, #7, and the
   retrieval log) are the evidence a deletion should rest on.
