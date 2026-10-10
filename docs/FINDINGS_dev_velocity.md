# Findings — coding speed and ease: where a session's effort goes (2026-10-10, S225, Opus 5.5, `xhigh`)

First run of `docs/FABLE_AUDIT_dev_velocity.md` (audit queue item 20).
⚠️ **Same model family as the builder.** Opus 5 and 5.5 wrote most of the
process audited here, so a cross-model read is owed (memory
`measurements-that-favour-me`). §11 names the claims to aim it at.

## 0. Verdict

**There is no large process lever. Session time goes to producing the work
itself.** Of 64 working hours across 114 sessions (43 days, 457 merged PRs):

- model generation is 49%;
- running verify scripts is 15%;
- everything that could be called overhead is about 17% (git/gh calls, plus
  writing commit messages, PR bodies, handoffs and TODO/DECISIONS/ledger rows).

No overhead remedy measured here would recover more than ~3% of working time.

| Level | Verdict | One line |
|---|---|---|
| L0 where effort goes | **MEASURED** (CONDITIONAL on the instrument, §2) | Generation 49% of working time (31% of it thinking), verify runs 15%, ceremony ~17% (~5.7 min/session, ~1.5 min/PR). Reading docs is 12% of token cost but under 1% of tool time |
| L1 ceremony proportionate | **SOUND** | Every step with a count has catches: the pre-push hook 2, `handoff_gap` 2, `check_decisions_log` failed in 17 sessions. Batching the 54 small docs PRs would save ~2% |
| L2 what a session loads | **SOUND on size, WARN on accuracy** | Sessions read ~4.7k tokens of `TODO.md`, not 298 KB (1.6% of token cost). The real fixed cost is the always-loaded instructions (~14k tokens, 6.3%). **Five stale statements were in `CLAUDE.md`; fixed in this PR** |
| L3 merge friction | **SOUND** | 7 conflicts in 43 days. Append-anchor docs had 5, `CODEMAP.md` 1. The parallel-session trial caused 0 |
| L4 local web loop | **WARN → proposal** | 324 plumbing-only calls in 60 sessions. `pkill -f` killed its own shell 28× in 19 sessions, ≥18 of them after the memory note warning against it. `require('playwright')` failed 19× in 16 sessions. 4 scratch probes are committed on master |
| L5 one-file re-open trigger | **NOT FIRED — stopped** | The report session's 5 PRs touched no `web/index.html` |

What this changes:
- **Shipped in this PR (docs):** the stale `CLAUDE.md`, `STACK.md`,
  `EVIDENCE_NOTEBOOKS.md` and `TOKEN_EFFICIENCY.md` statements, and the
  tokens-per-byte rule.
- **Recorded in memory:** the `NODE_PATH` route that keeps probes out of the
  repo.
- **Proposed (§10):** a `verify.js --serve` wrapper; deleting the 4 stray
  probes; committing this run's instrument.

---

## 1. Hinge facts and baseline re-measure

Both hinge facts hold:
- 115 transcript files (one is this session), 289 MB, from 2026-08-28. Assistant
  records carry `message.usage` and `tool_use` blocks.
- The report session has its own directory (2 transcripts, 134 calls). It is
  **excluded** from every total below.

| Brief §1 figure | Brief | Re-measured 2026-10-10 | Note |
|---|---|---|---|
| Loaded path | 324 KB, `TODO.md` 89% | 323 KB, `TODO.md` 291 KB (89%) | ⚠️ this is *bytes a session is told to read*, not what it reads (§5) |
| `TODO.md` open boxes | 84 | 83 top-level, **117 including nested** | `STALENESS_LEDGER.md` counted nested (100 on 09-20), so the like-for-like change is +17 |
| `DECISIONS.md` | 562 KB "against a one-line contract" | 562 KB | ⚠️ **premise false.** The contract was rewritten 2026-09-09 by Peter: long rows are blessed (header, `FINDINGS_decisions_index_drift.md` §7). Only `CLAUDE.md` still described the old contract (§5d) |
| `index.html` | 8,849 lines | 8,849 | `CLAUDE.md` said ~7,345; fixed |
| PR throughput | 200 in 18 days | **457 merged PRs created since 2026-08-28** (43 days, 10.6/day) | 54% docs, 43% code, 2% data |
| Tool mix (one transcript in the brief) | 67 Bash, 2 Edit, 2 Read | 81.6% Bash, 8.3% Edit, 5.2% Read, 2.3% Write, of 12,610 calls | |

## 2. The instrument

The scripts are kept outside the repo, at
`/home/opc/research/edmonton-tax-viz/dev_velocity_instrument/` (proposal 3 in
§10 is to commit them).

**Parsing.** One API response is written as **several JSONL records that
repeat the same `usage`**. In a 40-file sample, 2,612 of 4,456 message ids were
split this way. Usage is therefore deduplicated by `message.id`; summing per
record would inflate tokens ~1.8× (8,223 records for 4,456 ids). Sidechains are excluded. A tool result is
matched to its `tool_use` by id.

**Cost unit, IET (input-equivalent tokens).** Opus list-price ratios: input 1,
cache write 2.0 (1 h) or 1.25 (5 m), cache read 0.1, output 5. A tool result of
*t* tokens is charged *t* × (2 + 0.1 × the API calls after it in the session),
because it is written once and re-read on every later turn. This is a
quota/cost proxy, not time.

**Tokens per character, calibrated rather than assumed.** I paired consecutive
API calls where the first issued exactly one tool call with a result over
6,000 chars. Context growth minus output tokens gives the result's token count:

| Content | Pairs | Chars per token, p25 / median / p75 |
|---|---|---|
| Markdown | 121 | 2.27 / **2.38** / 2.50 |
| Code | 47 | 2.36 / **2.49** / 2.58 |

⚠️ `TOKEN_EFFICIENCY.md`'s *"tokens ≈ bytes ÷ 4"* **understates this repo by
~1.7×**. `TODO.md` is ~124k tokens, not ~75k. The rule has been corrected in
this PR.

**Time.**
- Tool time is the span from the `tool_use` record to its `tool_result`.
  `AskUserQuestion` (10.1 h waiting on Peter) and spans over 30 min are
  excluded.
- Model time is the span from the last user or tool-result record to each
  assistant record.
- A fit across 110 sessions gives **model time = 12.2 ms per output token,
  with ~0 per call** (R² 0.95). Generation time is therefore output-bound.
- Usage reports `thinking_tokens` = **31% of output tokens**.

**Buckets.** Bash commands are bucketed by the program each shell segment
runs, not by the tool name:
- heredoc bodies are lifted out first, and quoted strings containing
  metacharacters are masked;
- a compound command gets several tags, and its cost is split equally across
  them;
- edits to `TODO.md`, `DECISIONS.md`, `AUDIT_LEDGER.md`, `session-summary/`,
  `CODEMAP.md`, `BRIEF.md` or `STALENESS_LEDGER.md` count as **ceremony**,
  per the brief.

**Spot check: 20 random calls per bucket.** The first classifier was wrong (§12):
- ~3 of 20 "verifying" calls were correct;
- 0 of 20 "other" calls belonged there.

After the rewrite, the second sample of 20 per bucket gave:

| Bucket | Correct of 20 |
|---|---|
| ceremony | 20 |
| reading_code | ~20 |
| reading_docs | ~18 |
| data | ~19 |
| verifying | ~17 |
| editing | ~17 |

"other" is now 2% of calls: loops, binary greps, `jupytext`.

**Known biases:**
- Equal splitting gives an edit-then-verify command half the verify time, so
  the "editing" tool time is inflated.
- Output is attributed by the visible characters of each tool input; JSON
  escaping inflates this by a few percent.

## 3. L0 — where the effort goes

### 3a. Working time: 63.9 h over 114 sessions (mean 34 min/session)

| Component | Hours | Share | How measured |
|---|---|---|---|
| Model generation | 31.0 | **48.5%** | output-bound (§2): thinking ≈ 9.6 h, visible ≈ 21.4 h |
| — of which ceremony prose (commit/PR text, handoffs, TODO/DECISIONS/ledger rows) | ~6.2 | ~9.7% | 29.1% of visible output chars (§3b) |
| — of which other docs (findings, briefs, specs, `UI.md`…) | ~3.4 | ~5.3% | 15.9% |
| — of which code (web, tests and verify scripts, other code and scratch) | ~4.2 | ~6.5% | 19.5% |
| — of which prose to Peter | ~3.5 | ~5.5% | 16.5% |
| Tool: verifying (pytest, `verify-*.js`, build, serve) | 9.4 | **14.8%** | |
| Tool: ceremony (git, gh, guards, archive) | 4.6 | 7.2% | CI waits total only 1.1 h |
| Tool: reading code | 3.8 | 6.0% | |
| Tool: editing | 3.3 | 5.2% | inflated by compound edit + verify commands |
| Tool: waiting (`sleep`/`until` loops) | 2.6 | 4.1% | |
| Tool: everything else | 9.2 | 14.4% | reading output, data, fs, env, analysis… |
| **Ceremony, all in** | **~10.8** | **~17%** | 5.7 min/session; ~1.5 min per merged PR |

**Reading docs is 0.5 h of tool time.** Reads are cheap in time and dear in
tokens (§3c).

### 3b. What the model writes (13.66M visible output chars)

| Destination | Share |
|---|---|
| Docs edits (non-ceremony `.md`) | 15.9% |
| **Commit messages and PR text** | **11.5%** |
| **Handoffs** | **9.0%** |
| Code and scratch scripts | 8.8% |
| Tests and verify scripts | 6.8% |
| Web | 3.9% |
| `TODO.md` / `DECISIONS.md` / ledger / other ceremony | 2.6 / 2.3 / 1.0 / 2.8% |
| Commands for data, verify, reading and analysis | ~17% |
| **Prose to Peter** | 16.5% |

Measured from git:
- PR body: median 829 chars, p90 2,626;
- commit message: median 569;
- handoff: median 12.4k chars, so ~1 min of generation per session.

### 3c. Token cost (324M IET)

| Component | Share |
|---|---|
| Tool results carried in context | **27.2%**: reading docs 11.7, reading code 7.8, data 1.9, ceremony 1.6, other 4.2 |
| Base context (first-call prompt carried) | 18.4% |
| Output | 14.6% |
| Cache rewrites after a miss | 10.8%: 140 events, **107 after more than 60 min idle** (Peter away), not a process cost |
| Residual: assistant turns carried, harness reminders, attachments | ~29% |

**Per file:** no single file dominates.

| File | Share of all IET (carried reads) | Sessions | Largest single read |
|---|---|---|---|
| `web/index.html` | **3.2%** | 77 | 11.9k tok |
| `TODO.md` | 1.6% | 97 | 10.7k tok |
| `DECISIONS.md` | 1.2% | 87 | 12.2k tok |
| `AUDIT_LEDGER.md` | 1.2% | 54 | 25.0k tok |
| `styles.css`, `DATA.md`, `CONTROLS_MATRIX.md`, … | under 0.3% each | | |

### 3d. Session-start cost

- First-call context: median **44k tokens** (50k this week).
- First non-ceremony edit: after median **15 API calls**, with **~28k tokens
  read** first. Context there: median 74k.
- **10% of a session's IET is spent before its first edit.**

Pre-edit reads per session that does them:

| File | Tokens per session | Sessions |
|---|---|---|
| the handoff | 5.5k | 96 |
| `index.html` slices | 5.5k | 50 |
| `TODO.md` | 4.2k | **57 of 105** |
| `AUDIT_LEDGER.md` | 10.6k | 24 |
| `DECISIONS.md` | 3.8k | 36 |

### 3e. Per shipped change

- PRs per session: median 4.
- **Ceremony calls ≈ 11.9 per session + 5.8 per PR** (OLS over 98 sessions).
- Of the 439 PRs mapped to a session, 105 are handoff PRs.
- 135 are other docs PRs, of which **54 have under 40 changed lines**.

### 3f. Rework

- **2.1%** of tool calls error. Verify commands error most, at 4.8%.
- **30 of 457 PRs (7%)** are titled as corrections, reversals or withdrawals.
  Most correct audit claims or docs, not code.

## 4. L1 — is the per-change ceremony proportionate? SOUND

**Catches against firings.** These counts come from transcript tool results,
not from memory.

| Step | Firings | Catches | Verdict |
|---|---|---|---|
| `.githooks/pre-push` | 547 pushes in 103 sessions | **2** real `BLOCKED` (`docs/fable-brief-inline-grounding`, `fix/loaded-path-grep`); 3 more matches were sessions reading the hook's source | keep: ~1 s per push |
| `merge-base --is-ancestor` | 344 calls in 100 sessions | **≤4 candidates** (handoffs reported "NOT on master" while their PR showed MERGED); not verified one by one | keep: rides inside other git calls |
| `check_decisions_log.py` | 250 runs in 52 sessions | `FAIL` printed in 32 runs across **17 sessions** (a row with no test citation or `[unverifiable]`, or an unmarked supersession) | keep: enforcing the convention is its purpose |
| `handoff_gap.py` SessionStart | 115 sessions | **2** messages (09-17, 09-22), both naming real unrecorded commits; silent otherwise | keep: zero cost when silent |

**Remedies the brief asked to test:**
- **Batch docs-only edits into the next code PR.** The 54 docs PRs under 40
  lines × ~5.8 ceremony calls × ~15 s ≈ **1.3 h over 43 days (~2%)**. Batching
  also delays landing, and delayed landing is where strands come from. **Not
  worth it.**
- **Let handoff PRs carry the TODO edits.** 50% of PRs touch `TODO.md`. Moving
  those edits saves no ceremony calls: the PR exists anyway.
- **Drop steps with zero catches.** None has zero.
- **Not in the brief, measured:** a PR body that restates a single-commit
  message. PR bodies total 513k chars ≈ 0.24M tokens ≈ **50 min (~1.3%)**.
  `gh pr create --fill` would save most of it. Small, optional; it is
  Peter's channel.

**Sharpest counter-argument.** This measures the *model's* ceremony cost.
Peter's is invisible here: reviewing and merging ~10 PRs a day, and 46
`AskUserQuestion` waits totalling 10.1 h (~13 min each). If his time per PR is
a minute, it matches the model's. **Evidence that would change the verdict:**
Peter's own estimate of time per PR. That is the one input this audit cannot
measure.

## 5. L2 — what does a session load, and does it need it?

### 5a. `TODO.md`: SOUND on cost

- **Composition (298 KB):**
  - open-item text 209 KB (70%), across 117 open boxes at ~1.8 KB each;
  - `## Done` one-liners 38.5 KB (13%);
  - closed sub-items inside open parents 23 KB (8%, relocatable, P10);
  - prose 27 KB.

  Regrowth from 238 KB is mostly **more open work, written longer**.
- **Cost:**
  - sessions read ~4.7k tokens of it (max single read 10.7k, never whole);
  - only 57 of 105 sessions open it before their first edit;
  - total **1.6% of IET**.

S166's open question, *"whether a session pays all 264 KB"*, is answered:
**no**. The loaded-path figure overstates what a session reads by ~25×.

### 5b. `DECISIONS.md`: SOUND, premise false

- Read in 88 of 115 sessions, ~3.8k tokens per session, max 12.2k, never whole.
- The "one-line contract" the brief measured against was replaced on
  2026-09-09 (Peter's call). Nothing to do except §5d's `CLAUDE.md` line.

### 5c. The always-loaded instructions: the real fixed cost

| File | Tokens | Share of all IET |
|---|---|---|
| project `CLAUDE.md` (16.8 KB, 10.8 KB on 08-30) | 7.0k | **3.2%** |
| the auto-memory index | 4.2k | 1.9% |
| server `CLAUDE.md` | 2.5k | 1.2% |

**Each 1k tokens of always-loaded text costs ~0.46% of all session tokens**,
so trimming 2k tokens ≈ 1%. That is a quota lever, not a speed lever: cached
prefill is fast.

**`CLAUDE.md`'s 28 "read before X" docs.** Sessions that opened each with a
read verb:

| Opened in | Docs |
|---|---|
| 92 of 115 | `TODO.md` |
| 88 | `DECISIONS.md` |
| 52 | `AUDIT_LEDGER.md` |
| 44 | `DATA.md` |
| 27 | `CODEMAP.md` |
| 3 or fewer | `DATA_INTEGRITY`, `REMOTE_VM`, `CLAUDE_WEB`, `SCOPE`, `BRIEF` |
| 0 | `PARCEL_LEVEL_OPPORTUNITIES` |

`REPORT_CLAIMS` shows 0 in the main session, but it belongs to the report
session.

A rarely opened pointer is not dead weight: `REMOTE_VM` is only needed on a
cloud VM. The cost sits in the long bullets: the session-start issue list is
1.7 KB, 10% of the file. **No trim recommended without Peter**, because the
long bullets carry ⚠️ lessons.

⚠️ **Out of the project's control, and larger.** The first-call context went
from 23k (08-28) to 50k (this week).
- The project's `CLAUDE.md` grew +6 KB (+2.5k tokens). The auto-memory index's history
  isn't recorded.
- Most of the rest is harness and account:
  - skill listing: 6.7k → 19.0k chars (+5k tokens);
  - deferred-tool names: 1.8k → 7.4k chars (+2.3k);
  - the remainder (system prompt, tool schemas) was not measured directly.

That is `server`'s and Peter's to weigh. Reported, not recommended.

### 5d. Stale statements in the loaded path: five, all fixed in this PR

| `CLAUDE.md` said | Measured | Fixed to |
|---|---|---|
| `index.html` "~7,345 lines" | 8,849 | the line count is dropped; `wc -l` is the source |
| `DECISIONS.md` "one line + pointer … never duplicate rationale" | header rewritten 2026-09-09: rows may paraphrase, every row carries a doc pointer | the current contract |
| the `STACK.md` line: four CI workflows | five: `evidence-recheck.yml` since 2026-09-21 | five |
| evidence notebooks: "`q7d6-ambg` … all four and nothing re-runs them on a schedule" | five reports, re-run monthly since 2026-09-21 | five, monthly |
| the `COPY_DECISIONS.md` line: 21 rows | 34 item ids | count dropped |

The same staleness, fixed at its source:
- `STACK.md` §7 omitted `evidence-recheck.yml` entirely;
- `EVIDENCE_NOTEBOOKS.md`'s dependency table said "all four" while its
  following paragraph said five, and claimed nothing runs them on a schedule;
- `TOKEN_EFFICIENCY.md` carried the ÷4 rule and the 7,345 count.

## 6. L3 — merge friction: SOUND

**Conflicts since 2026-08-28**, from `CONFLICT (` lines in tool results:
**7 events**.

| File | Conflicts |
|---|---|
| `DECISIONS.md` | 3 |
| `TODO.md` | 1 |
| `TODO.md` + `TODO_archive.md` | 1 |
| `CODEMAP.md` | 1 |
| `UI.md` | 1 |

- Git has 8 merge-master-into-branch commits in the same window.
- **The parallel-session trial caused 0**: no conflict involved a report-session
  branch.
- 7 of the 8 merges fall on 10-06 to 10-10, when the main session had several
  `web/` PRs open at once.

**`CODEMAP.md`.**
- Opened by read verb in 27 sessions; its whole value is being looked up.
- 1 conflict in 43 days, resolved by the one-liner S224 recorded
  (`tools/codemap.py && git add`).
- A merge driver, CI-only generation, or not committing it is **not justified
  at this base rate**.

**Append-anchor conflicts (5 of 7).**
- `merge=union` for `DECISIONS.md` and `TODO_archive.md` was considered. It
  would resolve these locally.
- But it silently keeps both sides of any in-place edit, and this project's
  failures are silent ones. **Not recommended at ~1 event per 9 days.**

## 7. L4 — the local web loop: WARN, wrapper proposed

60 of 114 sessions ran `verify-*`, probe or shot scripts:
- 604 script runs and 258 builds;
- **324 plumbing-only calls**: start `http.server`, find the port, check the
  root, kill. Median 4 per web session, p75 7, max 24.

At ~15–18 s per call that is **~1.5 h, ~2.5% of working time**.

| Footgun (memory) | Events | Sessions | Did the memory note stop it? |
|---|---|---|---|
| `pkill -f` kills its own shell, exit 144 (`pgrep-watchers-match-themselves`, written 2026-08-30) | **28**; 24 had `pkill -f` in the same command | 19 | **No.** ≥18 events after the note, the latest today |
| `require('playwright')` fails outside `tools/profiling/` | **19** | 16 | No note covered it as a rule. **Side effect: 4 scratch probes are committed on master** (`_dbg.js` 0f52b6d, `s223-probe{,2,3}.js` f289f81, ridden in by `git add -A`) |
| Stale server answering (`confirm-the-server-you-measure`) | 1 explicit `Address already in use` | 1 | undetectable by text when it succeeds silently, so a floor |
| Bash call ran into the 10-minute cap | 23 | 17 | 3.8 h; 19 of them asked for a timeout above the 600 s maximum. `TOKEN_EFFICIENCY.md` rule 7 already says to background long runs |

**Base rate against cost.**
- Each exit-144 or require failure costs ~1–2 calls, ~50–90 calls in total:
  cheap one at a time, but recurring every 2–3 days.
- **The memory route has failed for `pkill -f`. A mechanism does not depend on
  being remembered.**
- **The `require` fix is free and verified this session:**
  `NODE_PATH=/home/opc/edmonton-tax-viz/tools/profiling/node_modules node <scratchpad>/probe.js`
  resolves Playwright, so probes never need to be written into the repo.
  Recorded in the `oracle-server-headless-verify` memory.

## 8. L5 — the one-file re-open trigger: NOT FIRED

The report session's PRs since 2026-10-02 are #654, #656, #658, #659 and #670.
**None touches `web/index.html`**; #656's only `web/` file is a generated
notebook page under `web/notebooks/`. None of the 24 `index.html` commits
since 2026-10-02 is on a report-session branch. The "second concurrent author" trigger has not fired; per the
brief, stop. (DECISIONS 2026-09-05, bodies read in full.)

## 9. Levers outside the project's process, measured, not recommended

- **Thinking: ~9.6 h, ~15% of working time.** It is set by the effort level,
  and it is where the reasoning happens: the same defence argument as
  verifying. Peter's call.
- **Harness base context** doubled (§5c).
- **Waiting on Peter: 10.1 h** of `AskUserQuestion`.

## 10. Proposals: propose-first, none built

Ranked by measured saving:

1. **`verify.js --serve <root>`** (tools change; Peter decides):
   - start `http.server` from that root on a free port;
   - confirm by md5 that the served `index.html` matches the file on disk;
   - run the named scripts serially;
   - kill the server by its child pid.

   This removes most of the 324 plumbing calls (~2.5% of working time) and the
   main reason anyone types `pkill -f`. An alternative or complement is a
   `PreToolUse` hook rejecting `pkill -f`; that is a guard change.
2. **Delete the 4 stray probes** (`tools/profiling/_dbg.js`,
   `s223-probe.js`, `s223-probe2.js`, `s223-probe3.js`). Nothing references
   them.
3. **Commit this run's instrument** as `tools/transcript_effort.py`, with a test
   pinning the classifier cases that failed in §12. Re-running this brief
   without it means rebuilding the most expensive part (~40% of this run).
   It is a new module, so Peter decides.
4. Optional, Peter's channel: `gh pr create --fill` for single-commit PRs (~1%).

## 11. Conflict of interest, and what a cross-model read should check

The same model family built the hooks, guards and handoff process and measured
them here. The verdict ("no big lever, keep every step") is the shape that
favours the builder.

Aim the cross-model read at:
- **(a) the bucket classifier.** Re-sample 20 per bucket.
- **(b) "ceremony ≈ 17%".** It rests on attributing ~29% of visible output to
  ceremony and on output-bound model time. A per-message attribution of
  thinking would change it.
- **(c) the catches table.** The `merge-base` "≤4" was never verified one by
  one.
- **(d) §4's counter-argument.** Peter's own time per PR is the uncounted term.

## 12. What this run got wrong

1. **The first classifier was wrong for most "verifying" calls.** It matched
   file *names* (`verify-x.js`, `test_x.py`, `check_x.py`) that were being read
   or edited, not run: about 3 of 20 sampled were real verify runs. Caught by
   the spot check before any share was reported. The rewrite classifies each
   shell segment by its program.
2. **Every "other" sample (20 of 20) was a misfiled grep.** Splitting on `|`
   cut `grep "a\|b" FILE` apart, so the file path landed in a segment that
   looked like no program. Fixed by masking quoted strings before splitting.
3. **The token estimate started at chars ÷ 3.5**, my own prior and the same
   class of error as `TOKEN_EFFICIENCY.md`'s ÷4. Calibrated to ÷2.4 and every
   token figure was re-run. Uncalibrated, all token costs would have read ~30%
   low.
4. **The conflict count briefly included this run's own output.** A tool result
   echoing an old `CONFLICT … CODEMAP.md` line was counted as a new conflict on
   this branch. The class being audited showed up in the instrument. Excluded.
5. **The first count of `CLAUDE.md` doc opens (94 of 115 for `DECISIONS.md`)
   counted mentions.** `git add docs/DECISIONS.md` scored as an open. Recounted
   with read verbs only: 88.
6. **The handoff-span figure (2.0 min) comes from a biased subset.** Only 50 of
   114 sessions invoke `/handoff` through the Skill tool; the rest type it as a
   slash command. Not used in any verdict; §3b's ~1 min per handoff comes from
   output size instead.

## 13. Reproduce

```bash
I=/home/opc/research/edmonton-tax-viz/dev_velocity_instrument
python3.12 $I/parse_transcripts.py ~/.claude/projects/-home-opc-edmonton-tax-viz <outdir> main   # sessions_main.csv, calls_main.csv
python3.12 $I/decompose.py      # output share, cache-miss rewrites, attachment sizes
python3.12 $I/timing.py         # working-time split (run from <outdir>; writes timing_sessions.csv)
python3.12 $I/catches.py        # guard firings/catches, footgun events
gh pr list --state merged --limit 500 --json number,createdAt,mergedAt,headRefName,additions,deletions,files,title
```

The calibration, per-file reads, CLAUDE.md-opens and PR-mapping steps were
inline `pandas` cells over those CSVs. §2 and §3 state each one's rule.
⚠️ The live transcript grows while it is parsed, so this session's own counts
shift between runs (12,616 → 12,664 API calls).
