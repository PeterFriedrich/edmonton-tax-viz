# Findings — should doc growth be instrumented? (2026-09-16, S166, Fable 5.1, read cold)

**Instrument:** `docs/FABLE_AUDIT_doc_growth.md` (written by Opus 5, S165, the
model that proposed the feature). Measured on `master` @ `d0fdf6e`. Every figure
below was re-derived from git with my own code (§7), not the brief's script. No
S165 handoff was read; `FINDINGS_guard_channels.md` was opened only at step 5 of
the brief's grounding order.

## 0. Verdict

| level | verdict | one line |
|---|---|---|
| **L0** — is repo-wide doc growth a problem here? | **FAILS → build nothing** | The growth is ~95% artefact classes that `CLAUDE.md` mandates or Peter commissioned, it scales with session count (~38 KB/session, 54 sessions in the window), it costs 0 tokens outside the loaded path by the project's own decided cost model, and **no `.md` file has ever been deleted in 176 days of history** — there is no decision a repo-mass number would change. A growth row on repo mass is rec 9's ratio ceiling with a different numerator, and rec 9 was DECIDED-NO on 2026-09-16. |
| L1–L4 | **moot** | Not descended. |

**What the hinge-fact re-measure changed:** the brief's §3 framing — *"the
measurement that exists is pointed at the 4 files that are not growing, and the
growth is in the ~200 files it does not look at"* — is **false**. The loaded
path grew **173 → 288 KB (+66%) in the same 30 days** the repo grew +69%. The
brief's *"292 → 295 KB, ~1%"* is a **one-session** delta set beside a
**30-day** repo figure. The existing instrument is pointed at the right thing,
the right thing is growing at the repo's rate, and what it lacks is not a new
metric but the reader the 2026-09-16 decision row already assumed (§3).

**Deliverable per brief §8:** this file, a ledger row, a `DECISIONS.md` row
closing the question. No digest row designed.

## 1. Hinge-fact checkpoint — every figure re-measured

Baseline `a204fe6` (2026-08-17, the last commit before today−30). `master` has
moved two merges since the brief was written (#445 the brief itself, #446 the
S165 handoff), which accounts for every difference below.

| claim | brief | measured | verdict |
|---|---|---|---|
| repo-wide `.md`, 30 d | 3,014 → 5,065 KB (+68%), 117 → 206 | **3,015 → 5,095 KB (+69%), 117 → 208** | ✅ (+30 KB = the two merges) |
| `docs/` + `TODO` + `CLAUDE` + `README` | 1,485 → 2,705 KB (+82%), 55 → 91 | **1,486 → 2,724 KB (+83%), 55 → 92** | ✅ |
| `session-summary/` | 1,393 → 2,181 KB (+57%), 56 → 109 | **1,394 → 2,191 KB (+57%), 56 → 110** | ✅ |
| biggest grower | `DECISIONS.md` +204 KB → 442 KB | **+205 KB, 237 → 442 KB** | ✅ |
| loaded path | 295 KB; `TODO.md` 264 KB = 89% | **295 KB; `TODO.md` 264 KB (89%)** | ✅ |
| loaded-path growth "this session" | 292 → 295 KB, "vs S164 handoff §6" | 292 is in `DECISIONS.md` 2026-09-16 (rec 9 row) and `_DISPOSITIONS.md`; **S164's handoff does not contain the number** | ⚠️ pointer wrong, figure right |

The numbers hold. **The framing around one of them does not** — see §2.

### 1a. What the brief did not measure, now measured

| quantity | value |
|---|---|
| 60-day baseline (`db1d7ac`, 2026-07-18) | **1,434 KB / 77 files** → +255% to today |
| 90-day baseline (`423da3d`, 2026-06-18) | **59 KB / 11 files** — the doc corpus is effectively 90 days old |
| absolute growth per 30 d | 60→30 d: +1,581 KB; 30 d→now: **+2,080 KB** (accelerating in bytes, decelerating in %) |
| sessions in the window | **54** handoffs dated ≥ 2026-08-17 → **~38 KB of `.md` per session**, of which the handoff itself is ~15 KB |
| `.md` files ever deleted | **0.** `git log -M --diff-filter=D -- '*.md'` is empty; the 2 root-level "deletions" (`ARCHITECTURE.md`, `SPEC_phase1.md`) and every `session-summary/` one are renames into `docs/` or `archive/` |
| loaded path, 30 d | **173 → 288 KB (+66%)** committed bytes (`CLAUDE.md` 9.0→13.5, `TODO.md` 149→264, newest handoff 15.8→9.9); +7 KB memory index = the 295 |
| `TODO.md` | **149 → 264 KB (+77%)**, 3,285 lines — longer than one default `Read` (2,000 lines) returns |
| `DECISIONS.md` rows | 184 → 292 (+108 in 30 d = **2.0 rows/session**); median row 1,107 → 1,467 ch |

## 2. L0 — is doc growth a problem in this repo? FAILS

### 2a. The commissioned-vs-drift split (the brief's "single most important unmeasured quantity")

The 30-day delta is 2,080 KB: **1,406 KB in 94 new files, 721 KB in files that
grew, −47 KB removed.**

The 94 new files by class:

| class | files | KB | commissioned by |
|---|---|---|---|
| handoffs (57 = 54 archived + 3 live) | 57 | 845 | `CLAUDE.md` *"always run `/handoff`"*; **re-decided KEEP 2026-09-16** (rec 4, Peter) |
| `FINDINGS_*` | 15 | 256 | audit output — every one has an `AUDIT_LEDGER.md` row Peter commissioned |
| `FABLE_AUDIT_*` briefs | 10 | 128 | the skill's own Step 3(a) rule (*"write the brief as a standalone file"*) |
| `docs/external/` | 4 | 61 | the outside review Peter brought in + its two response docs |
| other `docs/` | 7 | 107 | see below |
| `PROPOSAL_*` | 1 | 9 | |

The 7 "other" files, checked at their creating commit: `DATA_ISSUES.md`
(the register `CLAUDE.md` now requires), `EVIDENCE_NOTEBOOKS.md`, `STACK.md`,
`TRANSITIONS.md`, `COPY_DECISIONS.md`, `PLAN_frontend_refactor.md`,
`VIZ_STACK.md` — each landed in its own reviewed PR, each is named in
`CLAUDE.md`'s Key Files or in a ledger row. **That is 107 KB (5%) as the upper
bound on "unprompted".** The other 95% is the project's own process running at
54 sessions per month.

The 721 KB of growth in existing files: `DECISIONS.md` +205 (mandated per
decision; long form blessed 2026-09-09 and re-blessed 2026-09-16), `TODO.md` +
`TODO_archive.md` +199 (the backlog and its archive — archiving happened, 83 KB
of it, and `TODO.md` still grew 116), `AUDIT_LEDGER.md` +97 (one row per audit),
`DATA.md` +39, `RUNBOOK.md` +23, `UI.md` +22.

**So the honest split is roughly 95 / 5, and the 95 is not drift — it is the
rate at which a process Peter runs and has just re-affirmed produces bytes.**
A growth number would report *"you ran 54 sessions"*.

### 2b. The cost model is already decided, and it says these bytes cost nothing

Three rows dated 2026-09-16 (read in full, not grepped):

- rec 9 row: *"The markdown:code mass ratio is a sanity check, never a tracked
  metric or a ceiling; what is tracked is the LOADED PATH in bytes."*
- rec 4 row: `session-summary/` archive is *"out of the loaded path"*; the 3
  live files are 4% of it.
- rec 5 row: `DECISIONS.md` *"is not in any session's loaded path, so its 430 KB
  costs 0 tokens unless opened."*

And `_PREMISES.md` A1 FAILS: *"an unread doc costs 0 tokens."* A repo-mass
growth row re-opens A1 under a new name. The brief's §5 L0 second candidate
("it is not") is not one candidate among three — **it is the project's recorded
position**, and nothing measured here contradicts it.

### 2c. What decision would a growth number change? History says none

- **Zero deletions in 176 days** (§1a). The only mass that has ever left a
  file is a rename into an archive — which is the *good* hygiene the brief's L3
  warns a growth instrument would misreport.
- Every artefact class that grew was **re-decided KEEP on 2026-09-16**, with
  the review's own numbers on the table (rec 4, 5, 7-prune, 9, P1-cap all
  DECIDED-NO).
- The review named `DECISIONS.md` as the worst offender on 09-15; the brief says
  it then *"grew fastest after being named."* Measured: +24 KB in the 7 days
  before (09-08→09-15), +22 KB in the 1 day after — **but that day was six
  sessions Peter commissioned on that very review**, which wrote 13 decision
  rows. Per session the rate did not move. Being named produced work, not drift.

Nobody would delete a doc because a table said +69%, because nobody has deleted
one at +255% over 60 days, and the one person who could has just chosen not to
with the numbers in front of him. **L0 fails. Build nothing.**

### 2d. Sharpest counter-argument, and what would change the verdict

**Counter:** "Growth ∝ sessions" is exactly what a ratchet looks like from
inside — the process *is* the drift. 2 `DECISIONS.md` rows per session with
median length up 33% in 30 days, and 15 KB of handoff per session, are rates
that were never chosen; they emerged. A monthly row would at least make the
rate visible to the person who could change the process.

**Why it does not flip L0:** the rate *was* put in front of that person, twice
this week — the review's 412 KB / 104 files, and Session B's `292 KB, 89%
TODO.md` — and he chose the long form both times. A digest row that says
*"+2 MB, 54 sessions"* every month reports a decision already taken. Under
`CLAUDE.md`'s own green-digest rule it becomes the row that is always fine.

**Evidence that would change it:** (a) any doc deletion or consolidation
decision in the next 60 days that a growth figure would have triggered earlier;
(b) the 2026-09-30 read-frequency run showing a large never-read set **that
survives the Bash-read caveat** — then growth of the *unread* subset becomes
meaningful; (c) the loaded path crossing whatever ceiling Peter puts on it
(§3) — which is a loaded-path question, not a growth-instrumentation one.

## 3. The finding the checkpoint surfaced — the loaded path is growing at the repo's rate, and its decided metric has a printer and no reader

This is outside the brief's stack (L0 is about repo-wide growth) and is
reported because the hinge-fact re-measure produced it.

- Loaded path **173 → 288 KB in 30 days (+66%)**; **`TODO.md` 149 → 264 KB
  (+77%)**, 3,285 lines. `CLAUDE.md` says *"Read it first"*; a default `Read`
  returns 2,000 lines, so a session either pages or reads 61% of it.
- The 2026-09-16 rec 9 row says the loaded path *"is what is tracked … `tools/retrieval_report.py` prints it; no ceiling is set … Peter can put a ceiling on it there if it moves."*
- **It has moved +66% in 30 days, and nothing runs `retrieval_report.py`.**
  Verified by finding the readers, not by failing to find them: its only
  invokers are three handoff next-step lines saying *"~2026-09-30: run it"*
  (S163, S164, S165) — a dated manual reader for a one-shot measurement, which
  is fine for the read-log question it was parked for, and is not "tracking".
- The remedy already exists and is already open: `_PREMISES.md`'s P10 note —
  *"the real exposure is the 100 unchecked boxes, and nothing has audited
  them"*; the 46 KB of closed sub-items inside open parents is *relocatable*.
  ⚠️ **P10 has no `TODO.md` item** — it lives only in `_PREMISES.md` and the
  ledger's S162 row (*"its 100 open boxes are unaudited"*). Added below.

**Not recommended here:** a loaded-path digest row. That is L2 of a different
stack, and the brief's rule is not to design under a failed L0. The number is
already in the one place the project decided it belongs; whether it needs a
scheduled reader is a question to put to Peter with the 2026-09-30 run, when
`retrieval_report.py` will be opened anyway. What *is* actionable now is the
P10 item, which is a `TODO.md` shape problem, not an instrumentation one.

## 4. Prior art — what others do (brief §6: "nobody looked")

One search, four sources, all pointing the same way: the convention is a **line
cap on the always-loaded agent context file** (~60–200 lines, some
teams enforcing it in CI), justified by instruction-following limits, not by
repo mass. Nobody found tracks repo-wide markdown growth, and nobody tracks a
backlog file — this project's loaded-path outlier. That is the project's own
posture (rec 9: loaded path, not ratio) and against the proposal.
`CLAUDE.md` here is 65 lines / 13.5 KB — inside every cited cap by lines,
dense by bytes.

Sources: [fullsend #299 — CI enforcement for CLAUDE.md size](https://github.com/fullsend-ai/fullsend/issues/299) ·
[rulestack — three postures for CLAUDE.md](https://dev.to/rulestack/documentation-audit-or-commit-gate-three-postures-for-claudemd-and-agentsmd-and-where-each-5892) ·
[Addy Osmani — Audit your agent files](https://addyo.substack.com/p/audit-your-agent-files) ·
[Solmaz — stop agents littering Markdown](https://solmaz.io/agent-doc-workflow).
The search summary's specific percentages were not verified and are not relied on.

## 5. Conflict of interest — applied

The brief warned that *"the louder number reached him first"* and asked me to
decide whether the rest was shaped the same way. Result: **the numbers were
not shaped; the framing was, in one place, and in the direction that favoured
the proposal** — §3's "the 4 files are not growing" inversion, built from a
one-session loaded-path delta beside a 30-day repo delta. The brief itself
flagged that framing as *"should be checked, not adopted"*, and it fails the
check. Everything else (the COI declaration, the volunteered defects, the L1
concession) held up and made this run shorter.

## 6. What this run got wrong

1. **My first script could not run and I nearly reported the brief's numbers
   instead.** System `python3` is 3.6.8 (`capture_output=` TypeError — the
   exact trap `DECISIONS.md` 2026-09-16 records for `handoff_gap.py`, which I
   had not yet read). Re-ran under `.venv`. Had I fallen back to the brief's
   `awk` one-liner, the checkpoint would have re-derived the author's figures
   with the author's code, which is what §2 forbids.
2. **My deletion sweep first said "3 deleted" in the window.** Those were
   `s108/s109/s110` moved to `archive/` — my own script lacked rename
   detection, i.e. it made exactly the L3 error the brief predicts an
   instrument would make. The corrected figure is 0, and a script that
   reported 3 would have reported archive hygiene as loss.
3. **"Nothing runs `retrieval_report.py`" is a confident negative** — the
   shape all four S165 reversals took. Verified by finding the readers (three
   dated handoff lines) rather than by an empty grep; the grep also matched a
   comment in `handoff_gap.py`, which is not an invoker. Reported as *"has
   readers on a date, is not tracked"*, not as *"nobody reads it"*.
4. **§3 is scope creep by the brief's own rule.** L0 failed; the brief says
   stop. I reported the loaded-path growth anyway because the checkpoint
   produced it and it contradicts a sentence in the brief. Kept, but marked as
   outside the stack and carrying no design.
5. **Not checked:** whether a session actually *pays* 264 KB of `TODO.md`
   (the read log shows 6 reads over 2 sessions, consistent with paging; bytes
   are still not tokens read). The 5% "unprompted" bound is by file, not by
   section — unprompted *sections* inside mandated files (a handoff's §3
   lessons, a DECISIONS row's third ⚠️) are not separable by this method and
   could be larger.

## 7. Reproduce

```bash
cd /home/opc/edmonton-tax-viz && git checkout master && git pull
git rev-list -1 --before 2026-08-17 master      # a204fe6
git rev-list -1 --before 2026-07-18 master      # db1d7ac (60 d)
git rev-list -1 --before 2026-06-18 master      # 423da3d (90 d)
# per-path .md bytes at a rev — python, not the brief's awk:
.venv/bin/python - <<'EOF'
import subprocess
def blobs(rev):
    out = subprocess.run(["git","ls-tree","-r","-l",rev],stdout=subprocess.PIPE,universal_newlines=True).stdout
    return {l.split("\t",1)[1]: int(l.split()[3]) for l in out.splitlines() if l.split()[1]=="blob" and l.endswith(".md")}
for rev in ("master","a204fe6","db1d7ac","423da3d"):
    b = blobs(rev); print(rev, sum(b.values())//1024, "KB", len(b), "files")
EOF
git log -M --diff-filter=D --name-only --format= -- '*.md' | grep -c .   # 0 — no .md ever deleted
git ls-tree -r --name-only master -- session-summary | grep -cE '2026-0(8-(1[7-9]|2[0-9]|3[01])|9-)'   # 54 sessions in window
.venv/bin/python tools/retrieval_report.py | sed -n 4p   # the loaded-path line
grep -rl retrieval_report .github/ scripts/ tests/      # handoff_gap.py comment only
```
