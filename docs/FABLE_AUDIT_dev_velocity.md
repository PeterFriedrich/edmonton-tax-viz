# AUDIT BRIEF — coding speed and ease (where a session's effort goes)

**Read cold.** This is a reusable *instrument*, not a findings doc. Written
2026-10-10 (S224, Opus 5.5) at Peter's request: "what things could help coding
ease and speed". ⚠️ **The builder's model wrote most of the process this audits**
(the handoff hooks, the pre-push hook, the ledger and DECISIONS conventions, the
guard scripts), so a same-model run grades its own work. Opus 5.5 is the default
(DECISIONS 2026-10-02); memory `measurements-that-favour-me` says to get the
findings read by a different model.

Family: **(a) decision audit, top-down.** A red at one level makes the levels
below it moot. Output: a new findings doc in `docs/` (`FINDINGS_dev_velocity`), plus a row in
`docs/AUDIT_LEDGER.md`.

---

## §0 — Grounding order

1. This brief, in full.
2. `docs/TOKEN_EFFICIENCY.md`, then `docs/FINDINGS_doc_growth.md` §3 and
   `docs/STALENESS_LEDGER.md` (what the S166 doc-growth run already settled).
3. `docs/AUDIT_LEDGER.md` rows S160–S166 (the doc apparatus, the guard burst and
   doc growth) and S213 (test and verify runtime). Don't re-run those questions;
   cite them.
4. `docs/DECISIONS.md` 2026-09-05 (two rows: `web/index.html` stays one file,
   with its re-open triggers). Read the bodies in full.
5. The auto-memory index (this project's memory directory). Many entries are workarounds for the local
   web loop, which makes them L4 evidence.

**Hinge facts. Confirm these first, and stop if one is false:**
- The transcripts exist: `ls ~/.claude/projects/-home-opc-edmonton-tax-viz/*.jsonl`
  (114 files from 2026-08-29 to S224, ~288 MB). Each assistant record carries
  `message.usage`, plus `tool_use` blocks with the tool name and input. ⚠️
  **Never `Read` one raw.** Parse them with `python3.12`.
- The report session (`~/edmonton-tax-viz-report`) has its own transcript
  directory. Keep its sessions out of this session's totals, or label them.

---

## §1 — Baseline measured 2026-10-10 (re-measure; don't trust these)

| Figure | Value | Command |
|---|---|---|
| Loaded path | **324 KB**, of which `TODO.md` is 291 KB (89%) | `.venv/bin/python tools/retrieval_report.py \| grep '^Loaded path'` |
| `TODO.md` | **298 KB**, 84 open boxes. S166 cut it to 238 KB | `wc -c TODO.md`; `grep -c '^- \[ \]' TODO.md` |
| `docs/DECISIONS.md` | **562 KB**, though `CLAUDE.md` says "one line + pointer" | `wc -c` |
| `web/index.html` | **8,849 lines**. `CLAUDE.md` still says ~7,345 | `wc -l` |
| PR throughput | **200 merged PRs in 18 days** (~11/day) | `gh pr list --state merged --limit 200` |
| Merge latency | code PRs median **0.1 h** (p90 2.8 h); docs median ~0 | same, `mergedAt − createdAt` |
| CI `Tests` | median **61 s** | `gh run list --workflow Tests` |
| `TODO.md` churn | **294 of 685** non-merge commits since 2026-08-11 touch it | `git log --no-merges -- TODO.md` |
| `docs/CODEMAP.md` churn | **86** commits; a generated file, committed | same |
| Merge-master-into-branch commits | 8 since 2026-08-11 (two on 2026-10-10: #706 on CODEMAP, #711 on TODO/TODO_archive) | `git log --merges \| grep 'into '` |

What these already rule out: **Peter's merge latency and CI time are not the
bottleneck.** Don't spend the audit on them.

---

## A — Audit (highest level first)

**L0. Where does a session's effort actually go?** Everything below is a guess
until this is measured.
- Parse the transcripts. Per session, sum input, output and cache tokens, and
  count tool calls. Bucket every tool call:
  - **reading docs:** `Read`, or `cat`/`sed -n`/`grep` on `docs/`, `TODO.md` or
    `session-summary/`;
  - **reading code:** the same, on `src/`, `web/`, `scripts/`, `tools/` or `tests/`;
  - **editing:** `Edit`, `Write`, or a heredoc or `sed -i` writing a file;
  - **verifying:** `pytest`, `verify-*.js`, `build_site.py`, `http.server`;
  - **ceremony:** `git`, `gh`, `merge-base`, the handoff skill, edits to
    `TODO.md`/`AUDIT_LEDGER.md`/`DECISIONS.md`/`session-summary/`;
  - **data:** fetches, notebooks, `main.py`.
- ⚠️ **Most tool calls are `Bash` (auto mode)**, so bucket on the command text,
  not the tool name. A spot check on one transcript found 67 Bash, 2 Edit and
  2 Read calls. Print 20 random calls per bucket to check that the classifier is
  right, before trusting any share.
- Report the shares, and the **session-start cost** (tokens before the first
  edit) as its own number.
- ⚠️ A bucket's size is not its waste. Verifying is this project's defence
  (`CLAUDE.md` "Comments & Scope"). The question is cost per *change shipped*,
  not which bucket is biggest.

**L1. Is the per-change ceremony proportionate?** A one-line docs fix and a
data-contract change go through the same PR, TODO, ledger, DECISIONS,
merge-base and handoff steps.
- From L0, measure ceremony tokens per merged PR, split docs vs code.
- Which steps have caught something? For the pre-push hook, the merge-base
  check and `check_decisions_log.py`, count catches against firings (memory:
  stranded 9×; the hook was added afterwards). A step with catches stays.
- Candidate remedies to *test*, not assume: batch docs-only edits into the next
  code PR; let handoff PRs carry the TODO edits; drop steps with zero catches.

**L2. What does a session load, and does it need it?**
- `TODO.md` grew back from 238 KB to 298 KB in 24 days. Is the growth open
  work, or closed and long-form text that `tools/todo_archive.py` didn't lift?
  Measure the bytes in open vs closed sub-items.
- `DECISIONS.md` is 562 KB against a one-line-per-row contract. How many rows
  exceed, say, 400 characters? Is it ever read whole? (It is not in the loaded
  path.)
- `CLAUDE.md` names ~20 "read before X" docs. From L0, which are actually
  opened, and how often does an opened one change what the session did?
- Stale figures in the loaded path (the 7,345 line count) cost a re-check every
  session. List them.

**L3. Merge friction.**
- `docs/CODEMAP.md` is generated by a `PostToolUse` hook and committed, so every
  pair of parallel `web/` PRs conflicts on it. Options: a `.gitattributes` merge
  driver that regenerates it, generate it in CI only, or stop committing it.
  Check what reads it (sessions, `tools/codemap.py` tests) before choosing.
- `TODO.md` and `docs/TODO_archive.md`: two PRs that each close an item append
  at the same anchor and conflict every time. Is a different anchor, or one file
  per closed item, cheaper?
- The parallel-session trial (`CLAUDE.md` "Parallel sessions") predicted small
  conflicts in `TODO.md` and `session-summary/`. Count the real ones since
  2026-10-02.

**L4. The local web loop: build, serve, verify.** These are memory entries
that describe a footgun, each paid for at least once:
- a stale `http.server` answering from another directory
  (`confirm-the-server-you-measure`);
- `pkill -f` killing its own shell (`pgrep-watchers-match-themselves`, which
  happened again in S223);
- verify runs that must run alone (`run-verify-scripts-alone`);
- teardown cost (`oracle-server-headless-verify`) and missing fonts
  (`oracle-box-has-no-web-fonts`);
- probe scripts that must live in `tools/profiling/` to `require('playwright')`.

  Is one wrapper (build → serve on a free port → confirm the root's md5 → run
  one verify → kill by pid) cheaper than everyone re-reading five memories? Count
  how many sessions in L0 hit one of these. ⚠️ **Measure the base rate before
  proposing it** (memory `measurements-that-favour-me`, S175).

**L5. Code navigation in `web/index.html`.** One file is **locked**
(DECISIONS 2026-09-05). Only check its three re-open triggers: "a second
concurrent author; a regression traced to cross-section scope interference; or
that registry refactor".
- ⚠️ **The parallel-session trial may be the first trigger.** Has
  `edmonton-tax-viz-report` committed to `web/index.html` since 2026-10-02?
  (`git log --since=2026-10-02 -- web/index.html`, matched to the report
  session's branches.) If not, the trigger has not fired; say so and stop.
- Otherwise, measure from L0 only: how many tokens go to finding code in
  `index.html` (CODEMAP lookups, slice reads)?

---

## Out of scope

- Verify runtime and sharding: audited in S213 (`FABLE_AUDIT_test_runtime.md`).
  Re-open only if L0 shows verifying has grown since.
- Whether the doc apparatus is load-bearing: settled in S160–S162. L2 asks about
  **size and reads**, not whether the docs should exist.
- One file vs modules: locked, except for L5's trigger check.

## Output rules

- Every remedy needs a measured cost from L0, and a base rate for the failure it
  prevents. A named footgun without a count is not a finding.
- Anything that changes CI, a guard, or a data contract is **propose-first**
  (`CLAUDE.md` "Comments & Scope"). Write it as a proposal in the findings doc,
  not a PR.
- Docs-only fixes (a stale figure in `CLAUDE.md`) may ship in the same session.
