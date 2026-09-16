# Brief — should doc growth be instrumented, and if so how? (read cold)

**For: Fable 5.1, fresh session. Written by Opus 5, 2026-09-16 (S165).**

⚠️ **Read §0 and §1 before anything else. §1 is a conflict-of-interest
declaration, and it is load-bearing: every number in this brief was produced by
the model that is proposing the feature the numbers justify.**

---

## 0. What you are being asked

Peter's question, in his words: *"did we at least have more automation for like,
telling if docs throughout the repo might be bloating too much over time? Cuz
that seems to be our main manual evaluation."*

The answer to the factual half is **no** (§3). The open question — yours — is
whether that absence is a **defect worth fixing** or a **decision already taken
and still correct**.

**Evaluate top-down, L0 → L4 (§5). A failure at a level moots everything below
it.** If L0 fails, say so and stop; do not design a better digest row under a
verdict that nothing should be built.

⚠️ **"Build nothing" is a first-class outcome here and costs you nothing to
return.** The proposal originates with a model that had just spent a session
generating the prose the proposal would measure. Treat the recommendation as
the thing under audit, not as the premise.

---

## 1. ⚠️ Conflict of interest — three layers, stated before the evidence

1. **Opus 5 proposed the feature** (a monthly digest row for doc growth),
   unprompted, at the end of a session in which it had itself added **+824
   lines, 98% prose** across 5 PRs.
2. **Opus 5 produced every number** below, including the one that makes the case.
3. **Opus 5 wrote this brief**, choosing which numbers appear in it.

`measurements-that-favour-me` (memory) says: *decompose any number supporting my
own output before reporting it; get a different model to read it.* That is what
this brief is for. **One instance already surfaced in the writing of it** — see
§2's ⚠️, where the first figure quoted was the more alarming subset.

Relevant, and pulled forward so you do not have to find it: **in this same
session Opus 5 published three claims that were reversed** — an audit HIGH that
was settled ground, the post-mortem for that HIGH (also false, also
self-flattering), and a "the prune recurs" reversal that was n=1.
`docs/FINDINGS_guard_channels.md` §4 lists all four with who caught each: **one
by the run, two by Peter, one by Fable.** A fourth self-serving claim from the
same session is the prior you should hold.

---

## 2. ⚠️ HINGE-FACT CHECKPOINT — re-measure before you evaluate

**Do this first, from git, without reusing the script in §7.** If your numbers
disagree with these, the disagreement is the finding and the rest of the brief
is void.

| claim | figure as reported | how to falsify |
|---|---|---|
| repo-wide `.md` mass, 30 d | **3,014 → 5,065 KB (+68%)**, 117 → 206 files | `git ls-tree -r -l <rev> -- .` at `master` and at `a204fe6` (2026-08-17), sum `.md` blobs |
| `docs/` + `TODO.md` + `CLAUDE.md` + `README.md` | **1,485 → 2,705 KB (+82%)**, 55 → 91 files | same, restricted to those paths |
| `session-summary/` | **1,393 → 2,181 KB (+57%)**, 56 → 109 files | same, that path |
| biggest single grower | **`DECISIONS.md` +204 KB → 442 KB** | `git ls-tree -l` that one path at both revs |
| loaded path (what a session reads) | **295 KB; `TODO.md` 264 KB = 89%** | `python tools/retrieval_report.py`, first block |
| loaded-path growth this session | **292 → 295 KB** | ditto, vs S164 handoff §6 |

⚠️ **The +82% figure was the one first quoted to Peter, and it is the subset
that excludes `session-summary/` — the file class the external review called
"the single most disproportionate item."** The honest repo-wide number is +68%.
The error direction is the tell: **the louder number reached him first.** Decide
for yourself whether the rest of the brief is shaped the same way.

**Known defects in the measurement, volunteered:**

- **Selection effect, unquantified.** The 30-day window straddles a burst of
  audit work **Peter commissioned** (S140–S165: the services-cost lens, the
  doc-apparatus review, the guard burst, two vacuous-guard runs). Some fraction
  of +68% is requested work landing, not drift. **Nobody has separated the two,
  and the split decides L0.** A defensible attempt: classify the 89 new files
  by whether a `TODO.md` item or a Peter instruction preceded them.
- **Baseline rev is arbitrary** — `a204fe6` is an auto-refresh commit, chosen
  only as "last commit before today−30". A different window may tell a different
  story; 60 and 90 days were **not** checked.
- **Bytes are not the cost.** Nothing here measures tokens *read*. A 442 KB file
  nothing opens costs a session nothing.

---

## 3. What exists today (verified 2026-09-16, re-verify anyway)

| | |
|---|---|
| `tools/retrieval_report.py` | **Invoked by nothing.** No workflow, no test, no digest. Manual only. |
| what it sizes | **4 files** — `CLAUDE.md`, `TODO.md`, newest handoff, and the auto-memory index (outside the repo). One `stat()` of the working tree. |
| history stored | **None.** Two runs give two snapshots and no delta. |
| its read log | `~/.claude/retrieval-log.jsonl` — **outside the repo**, uncommitted, machine-local, and **0 days old** (clock restarted 2026-09-16). |
| the 13 digest checks | All upstream-data vintage + banner + branch-refs. **No size or growth row.** |
| rec 9 (a ratio ceiling) | **DECIDED-NO**, 2026-09-16 — *"a number at the place it will be re-read, not a ceiling in a doc."* |

**So the measurement that exists is pointed at the 4 files that are not growing,
and the growth is in the ~200 files it does not look at.** That framing is Opus
5's and is exactly the kind of tidy inversion that should be checked, not
adopted.

---

## 4. Grounding order (read in this order, then challenge)

1. `docs/external/REVIEW_doc_apparatus_2026-09-15.md` — the external review that
   started this. Title: *"Is Your Documentation Load-Bearing, or Is the Agent
   Building Cargo-Cult Scaffolding for Itself?"*
2. `docs/external/REVIEW_doc_apparatus_2026-09-15_PREMISES.md` — Session A's
   corrections to it. **Several of the review's premises FAIL.** A3 in
   particular: ablation is uncoupled from the target here.
3. `docs/external/REVIEW_doc_apparatus_2026-09-15_DISPOSITIONS.md` — what Peter
   actually decided. **Recs 4, 5, 7(prune), 9(ceiling), P1(cap), P2 are all
   DECIDED-NO.** Read *why* before proposing anything adjacent.
4. `docs/DECISIONS.md` 2026-09-16 rows — ⚠️ **read the row BODIES, do not grep
   and truncate.** That exact failure produced two of this session's reversals
   (`FINDINGS_guard_channels.md` §0a).
5. `docs/FINDINGS_guard_channels.md` §4 — the four errors, and the shape they
   share: **every one was a confident negative.**
6. `tools/retrieval_report.py` — the whole file; it is short.

---

## 5. The decision stack — evaluate in order, stop at the first failure

### L0 — Is doc growth a PROBLEM in this repo at all?

The level everything rests on. Candidate answers, all defensible:

- **It is a problem.** +68% in 30 days; the review's named worst offender
  (`DECISIONS.md`) grew fastest *after* being named; nothing would have surfaced
  it without Peter asking.
- **It is not.** The growth is commissioned audit output landing. Docs outside
  the loaded path cost **zero tokens** per session. The project's real cost
  metric — the loaded path — moved **292 → 295 KB**, ~1%.
- **It is the wrong problem.** The charge against a doc is **staleness**, not
  size, and this session produced live evidence: `RUNBOOK.md` §2 carried advice
  that was wrong-and-repeating for months, and `VIZ_STACK.md` sat 40 days with
  drifted numbers. **Neither has anything to do with growth rate.**

**Ask: what decision would a growth number change?** If the honest answer is
"none — nobody would delete a doc because a table said +82%", L0 fails and the
proposal is telemetry for its own sake — which is the review's own Goodhart
warning turned on the remedy.

### L1 — If it is a problem, is GROWTH the right proxy?

⚠️ **The strongest challenge in this brief, and Opus 5 has no answer to it.**

**Recs 1/2/6 are already parked awaiting `tools/retrieval_report.py` at
~2026-09-30** — the read-frequency measurement. That answers *"is this doc ever
opened"*, which is a strictly better question than *"did this doc get bigger"*.

So: **does a growth row earn its place before the read data lands, or does it
pre-empt a better instrument that is 14 days out?** A defensible verdict is
*"wait for 2026-09-30 and decide then"*, which costs nothing and is not what the
proposing model suggested.

Also weigh: growth, staleness, read-frequency, and per-session token cost are
four different metrics. Rank them by *what action each would trigger*.

### L2 — If growth is worth watching, is the monthly digest the right CHANNEL?

For: it already runs, already files an issue, already reaches Peter, and
CLAUDE.md names "a working guard on a channel nobody reads" as the standing
failure mode. Against: **a green row that says "+3 KB" every month for a year is
the exact thing CLAUDE.md's green-digest rule warns about** — a row that always
reads fine is how the next real one gets skimmed. A guard that cannot plausibly
go red is a guard with no reader by another route.

**Ask: what threshold would make this row ACTION rather than informational, and
can it be justified from data rather than chosen?** If no defensible threshold
exists, that is an argument for a report you run when curious — which is
`retrieval_report.py`, i.e. build nothing.

### L3 — Is `git ls-tree` at two revs the right INSTRUMENT?

Window choice, baseline choice, and the commissioned-vs-drift split from §2.
Also: what does it do about a **deliberate archive move** (`TODO.md` →
`TODO_archive.md`), which is *good* hygiene that registers as growth in one file
and shrinkage in another? An instrument that flags correct behaviour is worse
than none.

### L4 — Only if L0–L3 hold: the implementation

Thresholds, top-N, what prints, where it lives, what test guards it
(`CLAUDE.md`: a decision that protects a number is a test first). **Do not
descend here unless the levels above hold.**

---

## 6. What was NOT checked

- **60- and 90-day windows.** Only 30.
- **The commissioned-vs-drift split.** The single most important unmeasured
  quantity in this brief.
- **Whether any doc is actually read.** The log is 0 days old.
- **Whether other projects instrument this.** `check-convention-before-locking-design`
  (memory) says Peter asks *"what do others do?"* — nobody looked. Prior art on
  doc-growth telemetry in agent repos is unexamined and should be.
- **Deletion pressure.** Nobody measured whether any doc has *ever* been deleted
  here, which bears directly on whether a growth signal could change anything.

---

## 7. Reproduce

```bash
cd /home/opc/edmonton-tax-viz && git checkout master && git pull
.venv/bin/python tools/retrieval_report.py          # loaded path + reads
git rev-list -1 --before 2026-08-17 master          # the 30d baseline (a204fe6)
```

Per-path mass at a rev — **write your own; do not reuse Opus 5's**:

```bash
git ls-tree -r -l <rev> -- . | awk '$2=="blob" && $4 ~ /\.md$/ {s+=$3; n++} END {print s/1024" KB", n" files"}'
```

⚠️ Run verify scripts **alone** on this 4-core box, and `git ls-tree -l` reports
**committed** sizes — the working tree may differ.

---

## 8. Deliverable

Per the `edmonton-audit` skill: verdict line per level, sharpest
counter-argument, evidence-that-would-change-it; a row in `docs/AUDIT_LEDGER.md`;
findings in a new `docs/FINDINGS_doc_growth` markdown file. ⚠️ **Step 4 now requires a non-empty
"What this run got wrong" section** — added this session, and S165 is the reason.

**If L0 or L1 fails, the deliverable is that finding and a `DECISIONS.md` row
closing the question. Do not design the row anyway.**
