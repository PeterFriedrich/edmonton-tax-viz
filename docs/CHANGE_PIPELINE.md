# Change pipeline

The path every change takes in this repo, in order. **Read it before you open
your first PR of a session.** Each step says what to run and when to stop and
ask Peter. The rules themselves live in `CLAUDE.md` and the scripts named
here; this doc puts them in sequence and doesn't restate them.

Ported by hand from `cc-data-project-template` (master `5b48600`, 2026-10-19).
This repo is the template's source, so copier never runs here: a change to the
template's copy is ported by hand. **If you change a step here, check whether
the template's copy should change too, and tell `template`.**

## 1. Before the PR

1. **Plan first when the change is a new module, a data contract or output
   schema change, or a CI change** (`CLAUDE.md` §"Comments & Scope"). Send the
   plan to Peter and wait. Routine edits don't need one.
2. **Reproduce before you fix.** An open `TODO.md` item can be stale: re-measure
   its stated cause first.
3. **A decision that protects a number is a test first.** Write the guard,
   then the `docs/DECISIONS.md` row that cites it
   (`scripts/check_decisions_log.py` gates new rows).
4. **A number that rests on something unproven gets a row in
   `docs/ASSUMPTIONS.md`**, pointing at the evidence.
5. **Verify, and show the output.** Say what ran and what it returned, not that
   it passed.
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
   - One round per PR. Re-review only after a substantial fix.
8. **Commit each working unit** with a descriptive message.

## 2. The PR

1. **Branch fresh from `origin/master` for every PR.** Peter merges within
   minutes, and a branch whose PR merged is dead (`.githooks/pre-push` blocks
   pushing to it).
2. **Open the description with a `Code review:` line** (*trial*, with 1.7): the
   level, the finding count, and what happened to them ("medium, 3 findings: 2
   fixed, 1 intended"), or "skipped (docs only)".
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
2. **Before every push to an existing branch, check whether its PR merged**
   (`gh pr view --json state`). If it did, branch again from `origin/master`.
3. **After a merge, confirm the work landed**:
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
   - Roll back: `git revert` reaches the live site only through the next
     workflow run, and a refresh run re-downloads. There is no
     deploy-without-regenerate path (`docs/RUNBOOK.md` §4, known gap).
5. **An upstream data defect found on the way** goes in `docs/DATA_ISSUES.md`,
   with whether the publisher has been told.

## When to stop and ask

- A plan-first change (step 1.1).
- A finding you'd resolve as "intended" that changes a published number.
- Anything that would push to `master`, rewrite history, or delete data.
- A permission your session was denied. Take it to Peter; don't ask
  another session to do it.

## This project's fit

Answered 2026-10-19. Each row is `adopted` (plus the mechanism),
`later: <trigger>`, `no: <reason>` or `n/a`. A row held only by habit says so.

| Stage | Step | This project |
|---|---|---|
| Before the PR | Plan first for a new module, schema or CI change | adopted: `CLAUDE.md` §"Comments & Scope"; habit |
| | Reproduce before fixing | adopted: `CLAUDE.md` (TODO line) and memory; habit |
| | A decision that protects a number is a test first | adopted: `scripts/check_decisions_log.py` in `tests.yml` |
| | Unproven premises indexed in `docs/ASSUMPTIONS.md` | adopted: `tests/test_assumptions_index.py` in `tests.yml` covers the 03 sizing rows and unit costs; other rows are habit |
| | Verify, and show the output | adopted: pytest and guards in `tests.yml` too; the local Playwright scripts for `web/` are habit, and nothing names which to run |
| | Break each new or changed guard on purpose | adopted: habit (memories), no mechanism |
| | Review the diff with `/code-review` (trial) | trial: 2 of 3–5 PRs done (#760, #761) |
| | Commit each working unit | adopted: `CLAUDE.md`; habit |
| The PR | A fresh branch from `origin/master` per PR | adopted: `.githooks/pre-push` blocks a merged branch |
| | `Code review:` line in the description (trial) | trial: with 1.7 |
| | Sync note for claude.ai-synced files | adopted: `CLAUDE.md`; habit. The synced set differs from the template's (`REPORT_CLAIMS.md` in; `ARCHITECTURE.md`, `DATA.md` out) |
| | CI green, and `master` requires the `test` check | adopted: `master` requires `test` and `url-state` |
| | No timed PR check-ins | adopted: `CLAUDE.md`; habit |
| Merging | The owner merges | adopted, with an exception: docs-only PRs are self-merged (Peter's standing instruction) |
| | Pre-push hook enabled (`git config core.hooksPath .githooks`) | adopted: set in this clone; a fresh clone must set it by hand |
| | Work confirmed on `master` with `git merge-base` | adopted: habit; no mechanism (work has stranded 9×) |
| After the merge | Template changes pulled by `copier update` | n/a: this repo is the template's source; changes are ported by hand |
| | Publish, with a gate before it ships | adopted: `refresh.yml` guards + verified notebooks + `verify-smoke.js`; `deploy.yml` smoke check |
| | Seen before the public build | no: `/dev-build-full/` ships in the same deploy, so nothing is seen first; the pre-publish guards stand in for staging |
| | Watch and roll back | watch adopted (automated issues, failed-run email, `status.json`); roll back no: `git revert` only reaches the site through a run that re-downloads (`docs/RUNBOOK.md` §4) |
| | Upstream data defects logged in `docs/DATA_ISSUES.md` | adopted: `CLAUDE.md`; habit |
