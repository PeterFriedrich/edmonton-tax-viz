# Findings — the test estate as one system (S247, 2026-11-15)

Peter's ask: *look at our entire test system. What are the overall patterns? Do
we have redundancies at different levels? Is the system well organized and
efficient?* Fable 5.2. Measured at `0c4dcdd`: counts and timings on the Oracle
box, mutations in a scratch git worktree, CI history through `gh api`. No code,
test or workflow was changed. §6 lists proposals; none is executed.

Earlier runs cover parts of this and are not repeated: vacuous guards
(`docs/FINDINGS_vacuous_guards.md`, `docs/FINDINGS_vacuous_guards_r2.md`), guard
channels (`docs/FINDINGS_guard_channels.md`), and the browser suite's runtime
(`docs/FINDINGS_verify_runtime.md`). This run looks at how the tiers fit
together.

## 0. The answer

- **Patterns.** Six tiers, each tied to one gate, and every asymmetry between
  them is explained in a comment where it lives. A guard is written after an
  incident, falsified when written, then gets its own tests and a test of its
  workflow wiring. Moving data is checked by band or derivation, not equality.
  Verify scripts are added, never refactored.
- **Redundancy.** Three of the four script steps on the merge gate repeat a
  check that pytest ran one step earlier (F3, proven by mutation). Everything
  else that looks duplicated is deliberate and recorded (§5).
- **Organization.** The workflows are well organized. `tests/` is not
  partitioned: it is one flat bucket that serves two gates with different
  questions, so the weekly data publish also runs every docs and process test
  (F2). Two recorded decisions say it must not.
- **Efficiency.** The gated tiers are cheap (pytest 18 s, merge gate 58 s,
  deploy 3 min, refresh 10 min). The browser sweep is the only expensive tier
  and it gates nothing; that was already known and stays open in `TODO.md`.
- **The ungated tier is red.** 8 of 44 verify scripts fail on the full build
  at `0c4dcdd`, two of them from copy merged two days ago (F5).
- **One defect.** A pytest test pins an exact count on a file the weekly bot
  rewrites. One neighbourhood crossing the $50k colour clamp turns the merge
  gate red for every PR and fails the next refresh, while the guard that owns
  that number is deliberately non-blocking (F1). It has not fired. The January
  roll is the likely trigger.

## 1. The map

| Tier | What | Size | Runs in | Blocks | Time |
|---|---|---|---|---|---|
| pytest | `tests/`, flat, no `conftest.py`, no markers | 66 files, 1,187 tests, 16,553 lines | `tests.yml` (PR, push), `refresh.yml` (weekly) | merge, weekly publish | 18 s here, 14 s on GitHub |
| Static guards | 4 `scripts/check_*.py` steps after pytest | 1,094 lines | `tests.yml` | merge | seconds |
| URL walk | `verify-url-state.js`, 7 shards, both builds | 1 script | `tests.yml`, PRs touching `web/` | merge | ~3 min |
| Data guards | 10 `scripts/check_*.py` steps around `main.py`, plus the raises inside `src/` | 2,811 lines | `refresh.yml` | weekly publish, or warn by issue | inside 10 min |
| Verified notebooks | `notebooks/verified/01`–`04` | 1,564 lines | `refresh.yml` | weekly publish | inside 10 min |
| Render smoke | `verify-smoke.js` (+ `verify-blurbs.js` on deploy) | 2 scripts | `deploy.yml`, `refresh.yml` | publish only | ~1 min |
| Browser suite | the other 41 `verify-*.js` | 44 scripts in all, 12,087 lines | a session, by hand | nothing | 39 min public, 44 min full |
| Monthly reports | `vintage_report.py` (16 checks), `recheck_evidence_notebooks.py` | 1,286 lines | their own workflows | nothing; files an issue | — |
| Hooks | `.githooks/pre-push`, `handoff_gap.py`, codemap regeneration | — | local | a push to a merged branch | — |

pytest by subject (sorted by file name, so the split is approximate):

| Subject | Files | Tests |
|---|---|---|
| Pipeline (`src/`, `main.py`) | 26 | 568 |
| Tests of the guard scripts | 17 | 382 |
| Build, fetch, tools | 6 | 95 |
| Front end read as text (ramps, tokens, labels) | 5 | 33 |
| Repo, docs and process state | 12 | 109 |

Test code is about the size of the code it tests: 30,200 lines of pytest,
verify scripts and notebooks against 31,000 lines of `src/`, `scripts/`,
`tools/`, `main.py` and `web/index.html`.

## 2. What each tier has caught on GitHub

All runs ever, read 2026-11-15.

| Workflow | Runs | Failures | What failed |
|---|---|---|---|
| `tests.yml` | 1,154 | **0** | nothing, in either job (28 of the last 1,000 were cancelled) |
| `deploy.yml` | 203 | 1 | the build step, 2026-07-30, before the smoke gate existed |
| `refresh.yml` | 77 | 10 | `main.py` raise ×2, pytest ×2, commit/push ×2, deploy ×1, startup or infrastructure ×3 |
| `vintage-digest.yml` | 4 | 0 | one ⚠️ digest, 2026-11-01: zoning code `RTCC` unknown |
| `evidence-recheck.yml` | 2 | 0 | both green |

Step-level data exists for the 55 refresh runs since 2026-07-18:

- **No `check_*` step, no verified-notebook step and no smoke step has failed.**
  Every non-success is a `skipped` behind an earlier failure.
- The two issue-filing steps have never run (revenue delta 25 of 25 skipped,
  clamp drift 12 of 12). The year-mismatch holding step has never run (53 of
  53). Six issues have ever been filed, all monthly reports.
- The two real upstream changes were caught by raises inside the pipeline:
  `no active service dates in gtfs_calendar_dates.csv` (2026-10-05) and
  `Unmapped assessment class label(s): ['DERELICT RESIDENTIAL']` (2026-10-19).
- The two pytest failures (2026-08-23) were a missing `scipy` in CI.

**Not measured:** reds on a session's own machine before a push. That is where
pytest is run most, and nothing records it. A merge gate with no red in 1,154
runs is consistent with sessions chaining the tests to the commit; it is not
evidence that the tests find nothing.

The findings register in `docs/AUDIT_LEDGER.md` gives the other half. Of 215
audit findings, 57 were visible on the public site, so they passed every tier.
By class: `render` 19, `claim` 19, `input` 4, `method` 4, `pipeline` 2. The
estate is densest on pipeline arithmetic and on the guards themselves (950 of
1,187 tests) and thinnest on copy and rendered state, which is also the tier
that gates nothing. The register has said this since 2026-09-26; the CI history
agrees with it.

## 3. Verdicts, top down

| Level | Question | Verdict |
|---|---|---|
| L0 | Is this much checking warranted? | **SOUND.** Public numbers, and the project's failures are silent ones. Sharpest objection: the tiers that run automatically have blocked two bad publishes in four months, both from `src/` raises that predate most of the estate. |
| L1 | Are the tiers split by the right question (the change, the data, the render)? | **SOUND** in the workflows. Each step sits in the workflow whose question it answers, and the fail-or-warn choice is recorded per guard. |
| L2 | Does each check live in one tier? | **CONDITIONAL.** pytest is one bucket for two gates (F2), and one test contradicts its guard's non-blocking decision (F1). |
| L3 | Is anything checked twice by accident? | **WARN.** Three merge-gate steps (F3). |
| L4 | Can a reader find their way around? | **WARN.** The two documents that describe the estate are stale (F4). |

## 4. Findings

### F1. A pytest equality on bot-written data turns a non-blocking drift guard into a blocking one

`tests/test_check_colour_clamps.py::test_the_real_file_is_in_band_today` reads
the committed `web/data/neighbourhood_value_per_acre.geojson` and asserts
`saturating == 16 and 4.0 < share < 5.0`, then that the share is inside the
1–6% band.

`DECISIONS.md` 2026-09-16 (colour clamps) says the saturating share *"WARNS each
refresh, files an issue, never blocks"*, and the same file's
`test_drift_never_changes_the_exit_code` pins that for the script.

**Mutation M5:** in the worktree, the highest live neighbourhood under the
clamp ($48,097 per acre) was moved to $50,001. That is 17 of 358, 4.7%, inside
the band.

- `check_colour_clamps.py` exits 0 and flags nothing. Correct.
- `check_colour_clamps.py --legend-only` exits 0. Correct.
- pytest: **1 failed**, `test_the_real_file_is_in_band_today`.

What follows on GitHub, from the wiring (not run there):

1. The refresh that moves the count commits and deploys normally. Its push
   uses the admin token, which bypasses the required check (`docs/RUNBOOK.md`,
   weekly-workflow triage).
2. The `tests.yml` push run on that commit is red, and so is every open PR.
3. The next refresh fails at its pytest step, before the download.

**Base rate.** Across the last 30 bot commits the count moved twice, 13 → 12 on
2026-08-03 and 12 → 16 on 2026-08-25, both before the test was written on
2026-09-16. It has been 16 on all twelve refreshes since. The nearest
neighbourhood is 3.8% under the clamp. Rates and assessments change at the
January roll, and `docs/RUNBOOK.md` does not mention this test.

Class `guard-noisy`, latent. The out-of-band case is blocked by the same test,
which the decision also says only warns.

### F2. `refresh.yml` runs all of `tests/`, so repo and docs state gates the data publish

`refresh.yml`'s first guard is `python -m pytest tests/ -q`. There is no marker,
directory or naming rule in `tests/` to select by purpose, so that step runs
the 109 repo, docs and process tests and every test that reads the live repo
(18 files do).

Two recorded decisions say this should not happen:

- `DECISIONS.md` 2026-07-30 (CODEMAP): *"a doc artifact must never be able to
  halt the data pipeline, and `pytest` is `refresh.yml`'s guard-before-
  regenerating step."*
- `DECISIONS.md` 2026-08-09 (doc citations): the check *"runs as a TEST, not a
  `refresh.yml` step, deliberately … a docs typo must not red a good weekly
  data refresh."* `docs/ARCHITECTURE.md` "Testing" repeats it.

The second is wrong as wired. Being a test is what puts it in the refresh.
**Mutation M1:** a line-number citation appended to `docs/STACK.md` fails
`test_live_repo_citations_all_resolve`, and with it the command `refresh.yml`
runs.

**Base rate: zero.** The required check keeps `master` green, and no refresh
pytest step has failed for a docs or process reason in 55 runs. Three routes
around the required check exist: the bot's own push (F1), an admin merge
(`enforce_admins: false`), and two PRs that are each green and red together
(`strict: false`; for example both sessions adding a handoff, which trips
`test_at_most_three_handoffs_at_top_level`). None has happened.

Class `process`, latent, low. The recorded intent and the wiring disagree, and
the missing partition in `tests/` is the reason.

### F3. Three of the four merge-gate script steps repeat a pytest test

`tests.yml` job `test` runs pytest, then four scripts. Control: 1,187 green and
all four scripts exit 0. Each mutation was made alone and reverted.

| Mutation | Script step | pytest |
|---|---|---|
| M1 line-number citation in `docs/STACK.md` | `check_doc_citations.py` exit 5 | red, `test_live_repo_citations_all_resolve` |
| M2 `colorClamp: 50_000` → `5_000` | `check_colour_clamps.py --legend-only` exit 7 | red, 3 tests in `test_check_colour_clamps.py` |
| M3 `"maintenance": 5970` → `5971` | `check_cost_copy.py` exit 5 | red, `test_the_shipped_copy_matches_the_shipped_rates` |
| M4 undecorated `DECISIONS.md` row | `check_decisions_log.py` exit 6 | **green** |

Only `check_decisions_log.py` is carried by its step. The other three steps
cannot go red unless pytest already has. The cost is a few seconds. The real
cost is that two idioms for "run this guard on the live repo" coexist, and the
pytest one is what leaks repo state into the refresh (F2).

Class `process`, harmless.

### F4. The documents that describe the estate are stale

- `docs/STACK.md` §5: "53 test files, 1,013 tests, ~14 s" and "`verify-*`
  (43)". Measured: 66, 1,187, 18 s, 44. Corrected in this PR.
- `docs/ARCHITECTURE.md` "Testing": the `tests/` tree lists 5 files, and "What
  to test per module" covers the five Phase-1 modules. Not corrected here.
- `tools/profiling/README.md` is titled "Web map profiling harness". The verify
  suite, `shot-*` and `probe-*` share that directory (45, 20 and 6 tracked
  scripts).

Class `claim`, not public.

### F5. The ungated tier is red on master, and nothing noticed

The full sweep at `0c4dcdd` (both builds, `--jobs 1`): **4 of 44 scripts red on
the public build, 8 of 44 on the full build.** Each red was re-run alone on an
idle box and all eight reproduced.

| Script | Build | Failing check | Known cause |
|---|---|---|---|
| `verify-nonres-revenue.js` | both | blurb carries "not all of what the land pays" | #808 (merged 2026-11-13) reworded `blurbNote` |
| `verify-about.js` | both | no year literal in the pod markup (found 2026) | #808's "reported for 2026" in the About paragraph |
| `verify-transit.js` | full | 58 stations loaded (n=59) | a pinned count on GTFS data; not traced |
| `verify-guide.js` | full | names in the card are the buttons on screen | pre-existing, recorded S246 |
| `verify-peek.js` | both | 5 touch checks: the tap lands on a different hood | not traced |
| `verify-theme.js` | both | themed colour `88,90,102` drawn in no state | not traced |
| `verify-center2d.js` | full | Center 2D engaged: gold fill | not traced |
| `verify-temporal.js` | full | `#revcut` residential button not clickable | not traced |

Two of the reds were caused by a merged PR two days old, and the copy is
deliberate, so the scripts are what is stale. This is the open TODO item ("The
42 `verify-*.js` scripts gate NOTHING") happening again: its own text records
four scripts that stayed red for three days. Runtime: 39 min public, 44 min
full.

Class `guard-blind`, not public (the site is right; the checks are stale or
unexplained).

### Not findings

- **The browser suite gates nothing** (41 of 44 scripts). Open in `TODO.md`
  ("The 42 `verify-*.js` scripts gate NOTHING", Tiers 2 and 3). Not re-filed.
- **Fixed sleeps in the verify scripts.** 307 `waitForTimeout` calls, at least
  538 s per build if each ran once. Found and closed on purpose in
  `docs/FINDINGS_verify_runtime.md` §3 and §7: convert a script when it earns a
  gate.
- **No shared harness across the 44 scripts.** Each carries its own launch,
  boot and `check()`. This follows `DECISIONS.md` 2026-07-30 (the runner wraps
  the scripts instead of editing them). It is the price of that decision, and
  it comes due if Tier 2 or 3 is taken.
- **Sweep runtime** (39 and 44 min) matches `docs/FINDINGS_verify_runtime.md` after fast-teardown.

## 5. Deliberate duplication — leave it

- pytest in both `tests.yml` and `refresh.yml` (`DECISIONS.md` 2026-08-28;
  pinned by `tests/test_ci_workflows.py`).
- `verify-smoke.js` in both `deploy.yml` and `refresh.yml`; light mode and
  `verify-blurbs.js` in `deploy.yml` only (`DECISIONS.md` 2026-09-08, and the
  comments in both workflows).
- The assessment year checked by five guards (`check_year_alignment.py`,
  `check_roll_year_against_fir.py`, `check_temporal_years.py`,
  `check_temporal_archive_year.py`, `vintage_report.py`). Each reads a
  different source; the metadata-only version stayed green through the 2026
  roll.
- Pinned literals in verify scripts on the code path against invariants only in
  smoke on the data path (`docs/ARCHITECTURE.md` "Testing").

## 6. Proposals (Peter's call; none executed)

1. **F1, before the January roll.** In `test_the_real_file_is_in_band_today`,
   drop the two equalities and the band assertion and keep "the real files
   parse and yield the four money metrics". Convention followed:
   `test_the_repo_archive_is_readable_by_the_guard` ("not an assertion about
   the ANSWER") and `DECISIONS.md` 2026-07-28 ("bands, never equalities"). A
   test edit, so a code PR.
2. **F2 and F3, one decision.** Either:
   - (a) correct the 2026-08-09 row and `docs/ARCHITECTURE.md` to say a red
     `master` holds the refresh whatever the cause, and leave the wiring; or
   - (b) give `tests/` a partition (a marker or a `tests/repo/` directory) and
     have `refresh.yml` skip it, which is a CI change.

   Recommendation: (a). The base rate is zero in 55 runs, a red `master` is
   loud, and the last good site keeps serving. For new guards, run live-repo
   checks as a step and keep pytest to fixtures.
3. **F3 alone.** Leave the three duplicate steps. Removing them saves seconds
   and edits a gate that has pinned wiring tests.
4. **F4.** Replace the stale tree in `docs/ARCHITECTURE.md` "Testing" with a
   pointer to §1 here, when that section is next edited.

## 7. What this run got wrong

1. **I ran pytest during the verify sweep.** Five full runs and the mutation
   runs shared the box with it, against the standing rule. The sweep's timings
   are therefore not clean. Every red in F5 was re-run alone on an idle box
   before it was counted, and all eight reproduced.
2. **My first test classifier matched almost nothing.** It looked for
   `from src.x import`, which these tests do not use. The split in §1 is by
   file name and is approximate at the edges.
3. **I nearly wrote "no guard has ever fired".** The 2026-11-01 digest flagged
   `RTCC`, and step data covers 55 of the 77 refresh runs, not all of them. The
   claim in §2 is scoped to that.
4. **I carried F2 as a risk before I had its base rate.** It is zero. The
   finding that survives is that two decisions describe a wiring that does not
   exist.
5. **I counted 17 stray PNGs in `tools/profiling/` as clutter.** None is
   tracked.
6. **I drafted "no shared harness" and "fixed sleeps" as findings** before
   reading the 2026-07-30 runner row and `docs/FINDINGS_verify_runtime.md` §3,
   which decide both.
7. **Same model family as the builder**, and F3's "harmless" is my reading of
   my own kind of work. The mutations are reproducible from §4.
