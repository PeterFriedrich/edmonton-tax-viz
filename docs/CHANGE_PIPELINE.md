# Change pipeline

The path every change takes in this repo, in order. **Read it before you open
your first PR of a session.** Each step says what to run and when to stop and
ask Peter. The rules themselves live in `CLAUDE.md` and the scripts named
here; this doc puts them in sequence and doesn't restate them.

**What it's for:** spend Peter's attention only where a person is needed
(plans, the stop-and-ask points, calls a guard can't make) and let guards and
review catch the rest. Saving review time is no saving if it comes back as
fixes after a merge, so that count is the guardrail (step 4.6). Weigh a step
you'd skip or a row you'd answer `no` against it.

Ported by hand from `cc-data-project-template` (master `a104a5f`, 2026-10-21;
first port `5b48600`, 2026-10-19). This repo is the template's source, so
copier never runs here: a change to the template's copy is ported by hand.
**If you change a step here, check whether the template's copy should change
too, and tell `template`.** Step status (which steps a mechanism enforces and
which hold by habit) is in §"This project's fit" below.

## 1. Before the PR

1. **Plan first when the change is a new module, a data contract or output
   schema change, or a CI change** (`CLAUDE.md` §"Comments & Scope"). Send the
   plan to Peter and wait. Routine edits don't need one.
   - **Offer an explainer in one line** when the plan touches a part of the
     code Peter hasn't worked in: a written explainer of that slice, or a page
     (an Artifact) that shows it visually. He asked to be reminded that this
     exists. Offer it; don't make it unasked.
2. **Reproduce before you fix.** An open `TODO.md` item can be stale: re-measure
   its stated cause first.
   - **Search `docs/DECISIONS.md` before changing a behaviour or a number**,
     for the file, function or term you're about to change (and
     `docs/COPY_DECISIONS.md` for reader-facing wording). Say what it found in
     the plan or the description, or "no decision found". Checking "when it
     feels settled" misses the case where it doesn't: `a13969e` reverted a
     change whose own fix says "it was decided, and I had not read the row".
3. **A decision that protects a number is a test first.** Write the guard,
   then the `docs/DECISIONS.md` row that cites it
   (`scripts/check_decisions_log.py` gates new rows).
4. **A number that rests on something unproven gets a row in
   `docs/ASSUMPTIONS.md`**, pointing at the evidence.
5. **Verify, and show the output.** Say what ran and what it returned, not that
   it passed. Run them after your last edit, and on the built output when
   something is served: a check from before the final edit verified a
   different file (PR #117's deploy failed that way).
   - Every PR: `.venv/bin/python -m pytest -q` and every `scripts/check_*.py`
     that `tests.yml` runs.
   - A `web/` PR also: build (`scripts/build_site.py`), serve it, and run the
     `tools/profiling/verify-*.js` scripts for the area touched, **one at a
     time** (concurrent runs manufacture failures on the Oracle box). After any
     control-chrome or CSS change, `verify-controls-clickable.js`. For a visual
     change, the `render-compare` skill. Recipe: `docs/REMOTE_VM.md` and the
     latest handoff's Restoration Procedure. No list maps an area to its
     scripts; pick from `docs/UI.md`, which names the script that verified each
     feature.
   - Passing tests are not the result in a data project. **A change that moves
     a published number shows the old and new value and why it moved.** Build
     both sides from one raw data pull, or a data refresh is blamed on the
     code change. Show totals and the largest movers, not every row: a
     citywide total can move 0.2% while one neighbourhood moves 130%.
   - Published here: the served files in `web/data/`, numbers in the page copy
     (`web/index.html`, `data/city_budget_context.json`,
     `data/city_unit_costs.json`), and report figures (`docs/REPORT_CLAIMS.md`).
     `scripts/check_revenue_deltas.py` and `scripts/check_value_anchors.py`
     print the served-data movers; nothing prints the copy or report figures.
6. **Break each new or changed guard on purpose.** Commit first, then revert
   the fix or mutate the check, confirm its test goes red, then restore it. A
   test that passes either way guards nothing.
7. **Review the diff** (*trial*, from 2026-10-19, for 3–5 code PRs; the
   template's TODO J decides whether it becomes the rule). Run `/code-review`
   on a diff that touches code, at the level below. Fix or resolve each finding
   with a reason. Docs-only diffs skip this step.
   - `medium`: a change to a published number, a data contract, `src/` or
     `web/`.
   - `low`: tooling, guards, tests.
   - `ultra`: only when Peter starts it; it is billed.
   - One round per PR. Re-review only after a substantial fix, and only on
     the new diff.
   - **Fix the class, not the line.** When you fix a finding, search for the
     same pattern elsewhere (another hand-kept copy of a list, the same
     unchecked call) and fix every instance, or say why one stays. Note it on
     the `Code review:` line ("fixed, 2 more instances by grep").
   - **A real finding this diff didn't introduce is pre-existing.** Don't fix
     it in this PR (the smallest-change rule); open a `TODO.md` item, or a
     `docs/DATA_ISSUES.md` / `docs/ASSUMPTIONS.md` row if it is about data.
   - **Security review on risky paths.** Run `/security-review` too when the
     diff touches `.github/workflows/`, `scripts/build_site.py` or another
     deploy step, a secret or token; adds a data file to this public repo; or
     renders outside data (City names and labels from the feeds) as HTML in
     `web/index.html`. Note it on the same `Code review:` line ("security: 0
     findings"). Other diffs skip it.
8. **A kind of finding seen twice is fixed at the source**, not by hand a
   third time. When `/code-review` or an audit flags the same kind of problem
   on a second PR, fix it at the source in that PR, or tell Peter why not.
   - Prefer a guard or hook. A `CLAUDE.md` line is for when no mechanism fits:
     a written rule twice failed to stop pushes to merged branches, and only
     `.githooks/pre-push` did. Say which you chose and why.
   - Twice can be a coincidence. Before proposing a guard, say how often this
     kind of problem actually occurs.
9. **Commit each working unit** with a descriptive message.

## 2. The PR

1. **Branch fresh from `origin/master` for every PR.** Peter merges within
   minutes, and a branch whose PR merged is dead (`.githooks/pre-push` blocks
   pushing to it).
2. **A code PR's description opens with these lines**, after the Sync note if
   2.3 applies. A docs-only PR skips them (Peter, 2026-10-21: terse bodies for
   docs and editorial changes).
   - `Risk:` the tier, set by the paths the diff touches, not by judgment: the
     highest tier any path reaches, and that path ("high (`src/load_roads.py`)").
     - **high:** `.github/workflows/`, `scripts/build_site.py`, `src/` (every
       module feeds a served number), a served column or file shape, the
       committed inputs in `data/*.json`;
     - **medium:** `web/`, other `scripts/`, `tools/`, `notebooks/`, tests
       that change;
     - **low:** tests only added.
   - `Code review:` (*trial*, with 1.7) the level, the finding count, and what
     happened to them ("medium, 4 findings: 2 fixed, 1 intended, 1
     pre-existing, now a TODO item").
   - `Tested:` what ran and what it returned (step 1.5), and old → new for any
     published number that moved. Then "not covered: …", naming what no test
     or guard checked ("not covered: the served page; only the JSON was
     checked"), or "not covered: nothing known".
   - `Undo:` "revert", or "revert, then …" when a revert alone leaves
     something behind: served data that only a refresh run rebuilds
     (`docs/RUNBOOK.md` §4), a deploy or auto-commit a workflow already made,
     a claude.ai Project to re-sync.
   - `Cause:` a bug fix only: the cause in one line, apart from the symptom,
     then the step that should have caught it: "missed by: step 1.5", or
     "missed by: none (found by <audit>)" when no step was meant to. Don't
     guess a step: 10 of the 19 fixes before 2026-10-20 were found by an audit
     that no step stands in for.

   What the `Risk:` tier asks:
   - **low:** merge on green.
   - **medium:** as usual.
   - **high:** `/code-review` (and `/security-review` where 1.7's paths say)
     has run, the description names the files or hunks to read, and Peter
     reads the diff before merging. Offer the step 1.1 explainer for the slice
     the diff changes.

   The tier is a label only: Peter still merges every code PR (step 3.1).
   Self-merge of low-tier PRs is the template's trial (TODO M); not adopted
   here.
3. **A PR that changes a claude.ai-synced file** (`docs/BRIEF.md`,
   `docs/SPEC_*.md`, `docs/REPORT_CLAIMS.md` here; the list is in
   `docs/CLAUDE_WEB.md` §"The synced set") opens with "After merge: press Sync
   in the claude.ai Project."
4. **CI must be green**: `tests.yml` runs pytest and the guards, plus the
   URL-state Playwright shards on `web/` PRs. `master` requires the `test` and
   `url-state` checks. Don't merge around a red check; fix it.
5. **Push proactively; don't watch the PR on a timer.** No `/loop`,
   `ScheduleWakeup` or trigger to re-check it. Check it at your next real turn.

## 3. Merging

1. **Peter merges code PRs** (`src/`, `web/`, `scripts/`, `tools/`, `tests/`,
   `notebooks/`, `.github/`). Docs-only PRs, handoffs included, are
   self-merged with `gh pr merge --merge`, by his standing instruction.
2. **A push after Peter has looked says so.** If you push to a PR he has
   already looked at or approved, comment on the PR before he merges: "new
   commit since you looked: <what it changes>". His look covered the commit
   he saw, not this one.
3. **Before every push to an existing branch, check whether its PR merged**
   (`gh pr view --json state`). If it did, branch again from `origin/master`.
4. **After a merge, confirm the work landed**:
   `git merge-base --is-ancestor <sha> origin/master`. A merged PR is
   necessary, not sufficient.

## 4. After the merge

1. **Template changes**: n/a here (see the top of this doc).
2. **Publish.** Two paths, both to GitHub Pages:
   - `refresh.yml`, weekly (Monday 08:00 UTC) and by hand: tests, download,
     the pre-regeneration guards (unmatched names, year alignment, roll year
     vs FIR), regeneration, the post-regeneration guards (value anchors,
     served columns, colour clamps, revenue deltas, temporal years), the
     verified notebooks (`notebooks/verified/`, `docs/VERIFICATION.md`), then
     `verify-smoke.js` on both builds. Any red stops the deploy.
   - `deploy.yml`, on a push to `master` touching `web/**` (not `web/data/**`):
     builds and runs `verify-smoke.js` before upload.
   `verify-smoke.js` checks invariants only, never a data value.
3. **Staging**: none. The specialist build (`/dev-build-full/`) ships in the
   same deploy as the public root; it is a second audience, not a preview.
4. **Watch and roll back.**
   - Watch: automated GitHub issues (vintage digest, big revenue delta,
     colour-clamp drift, evidence recheck; titles in `CLAUDE.md`
     §"Session Management"), GitHub's failed-run email for the scheduled
     refresh, and `web/data/status.json` (vintage, generated date, banner).
     Read open issues at session start: `gh issue list --state open`. Triage:
     `docs/RUNBOOK.md`.
   - **A warning that only reaches a log is not detection.** Make it fail, or
     file an issue. Failed runs and deploys here were fixed in 15 to 30
     minutes, but `Alley-Commercial` was billed as local road for about 70
     days while its warning printed on every run to a log nobody read.
   - **A scheduled job fails quietly unless it is built not to**: an empty
     read is a failure, not a quiet week (a count check passes 0 == 0, so
     also fail below a floor); record a run as done only after its output
     landed; something outside the job notices a job that never ran (GitHub
     disables a scheduled Action after 60 days without repo activity).
   - Roll back: `git revert` reaches the live site only through the next
     workflow run, and a refresh run re-downloads. There is no
     deploy-without-regenerate path (`docs/RUNBOOK.md` §4, known gap).
5. **An upstream data defect found on the way** goes in `docs/DATA_ISSUES.md`,
   with whether the publisher has been told.
6. **Count fixes after a merge**: how this repo would notice that a lighter
   step (a skipped review, a looser guard) is costing more fixes later. A fix
   to a recently merged change, or a wrong published number found after it
   shipped, is the cost that review time was meant to save. No count runs yet;
   the `Cause:` lines (step 2.2) make it greppable
   (`git log --grep 'missed by'`).

## When to stop and ask

- A plan-first change (step 1.1).
- A finding you'd resolve as "intended" that changes a published number.
- Anything that would push to `master`, rewrite history, or delete data.
- A permission your session was denied. Take it to Peter; don't ask
  another session to do it.

## This project's fit

Answered 2026-10-19; rows from the 2026-10-21 port answered then. Each row is
`adopted` (plus the mechanism), `later: <trigger>`, `no: <reason>` or `n/a`. A
row held only by habit says so.

| Stage | Step | This project |
|---|---|---|
| Before the PR | Plan first for a new module, schema or CI change | adopted: `CLAUDE.md` §"Comments & Scope"; habit |
| | Offer an explainer for an unfamiliar slice | adopted: habit |
| | Reproduce before fixing | adopted: `CLAUDE.md` (TODO line) and memory; habit |
| | Search `DECISIONS.md` before changing a behaviour or number | adopted: `CLAUDE.md` (DECISIONS line); habit |
| | A decision that protects a number is a test first | adopted: `scripts/check_decisions_log.py` in `tests.yml` |
| | Unproven premises indexed in `docs/ASSUMPTIONS.md` | adopted: `tests/test_assumptions_index.py` in `tests.yml` covers the 03 sizing rows and unit costs; other rows are habit |
| | Verify, and show the output | adopted: pytest and guards in `tests.yml` too; the local Playwright scripts for `web/` are habit, and nothing names which to run |
| | A moved published number shown old → new, with why | adopted: served data by `check_revenue_deltas.py` / `check_value_anchors.py`; copy and report figures by habit |
| | Break each new or changed guard on purpose | adopted: habit (memories), no mechanism |
| | Review the diff with `/code-review` (trial) | trial: 2 of 3–5 PRs done (#760, #761) |
| | Fix the class, not the line | adopted with the trial: habit |
| | Pre-existing findings go to `TODO.md` or a ledger, not this PR | adopted: habit |
| | `/security-review` on this repo's risky paths (list them) | adopted: step 1.7 lists them; habit |
| | A kind of finding seen twice is fixed at the source | adopted: habit |
| | Commit each working unit | adopted: `CLAUDE.md`; habit |
| The PR | A fresh branch from `origin/master` per PR | adopted: `.githooks/pre-push` blocks a merged branch |
| | `Code review:` line in the description (trial) | trial: with 1.7 |
| | The description carries `Tested:` and `Undo:` | adopted for code PRs (Peter, 2026-10-21); docs PRs skip; habit |
| | A bug-fix PR names its cause | adopted for code PRs (`Cause:` … `missed by:`); habit |
| | `Risk:` tier set by this repo's path list (list them) | adopted as a label (step 2.2 lists the paths); self-merge by tier no: Peter merges code PRs |
| | Sync note for claude.ai-synced files | adopted: `CLAUDE.md`; habit. The synced set differs from the template's (`REPORT_CLAIMS.md` in; `ARCHITECTURE.md`, `DATA.md` out) |
| | CI green, and `master` requires the `test` check | adopted: `master` requires `test` and `url-state` |
| | No timed PR check-ins | adopted: `CLAUDE.md`; habit |
| Merging | The owner merges | adopted, with an exception: docs-only PRs are self-merged (Peter's standing instruction) |
| | A push after the owner looked is announced on the PR | adopted: habit |
| | Pre-push hook enabled (`git config core.hooksPath .githooks`) | adopted: set in this clone; a fresh clone must set it by hand |
| | Work confirmed on `master` with `git merge-base` | adopted: habit; no mechanism (work has stranded 9×) |
| After the merge | Template changes pulled by `copier update` | n/a: this repo is the template's source; changes are ported by hand |
| | Fit-table guard (`scripts/check_fit_table.py`) | no: it protects a `copier update` merge, which never runs here (Peter, 2026-10-21) |
| | Publish, with a gate before it ships | adopted: `refresh.yml` guards + verified notebooks + `verify-smoke.js`; `deploy.yml` smoke check |
| | Seen before the public build | no: `/dev-build-full/` ships in the same deploy, so nothing is seen first; the pre-publish guards stand in for staging |
| | Watch and roll back | watch adopted (automated issues, failed-run email, `status.json`); roll back no: `git revert` only reaches the site through a run that re-downloads (`docs/RUNBOOK.md` §4) |
| | Upstream data defects logged in `docs/DATA_ISSUES.md` | adopted: `CLAUDE.md`; habit |
| | Fixes after a merge are counted (the guardrail) | later: when the `/code-review` trial reports; `Cause:` lines make it greppable |
