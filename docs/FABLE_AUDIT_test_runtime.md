# AUDIT BRIEF — test & verify runtime, and the close-out sweep

**Read cold.** This is a reusable *instrument*, not a findings doc. Written
2026-10-02 (S212, Opus 5.5) by the session that built most of what it audits
(#637/#638, #642), so its claims about that work are self-graded. Fable if
credits exist; otherwise Opus 5.5 is the default (DECISIONS 2026-10-02), and the
findings must say the builder's model graded its own work.
Family: **(a) decision audit**, top-down. Two halves: **A** audits the speed-ups,
then **B** is the close-out sweep that ends the arc. Do A first, because a red
in A changes what B should close.

The arc: S205 asked "does the pre-merge verify need to take this long?" S206
measured it (`docs/FINDINGS_verify_runtime.md`: 82 min sweep, 31% teardown,
43% of the rest fixed sleeps). Since then:
- **#620:** the runner's `fast-teardown.js` preload (82 → 57.5 min).
- **#621, #622:** the harness reds and the probe renames.
- **#637 + #638:** `url-state` on web/ PRs, sharded 6 ways (8.5 → 4.0 min).
- **#642:** the public walk split by view, and a headless-shell-only install
  (→ 177 s run, slowest shard 148 s).

---

## §0 — Grounding order

1. `docs/FINDINGS_verify_runtime.md` §0, §3, §4 (what was measured, and why
   the sleeps were NOT swept).
2. `.github/workflows/tests.yml`: the header, then `url-state-changes`,
   `url-state-shard`, `url-state`. Then `tests/test_ci_workflows.py`.
3. `tools/profiling/verify.js` and `fast-teardown.js` (the runner and its preload).
4. `docs/DECISIONS.md` rows from 2026-09-29 on that name verify, url-state or
   shards. ⚠️ Read the bodies in full; don't `cut` or `head` them.
5. The "Verify runtime" section of `TODO.md`.

**Hinge facts. Confirm these first, and stop if one is false:**
- #642 is merged and on master: `git merge-base --is-ancestor <sha> origin/master`.
  If it is still open, audit the branch and say so.
- The box is unloaded: `top -bn1 | head -15`. No orphaned `node`, `python` or
  `http.server` (S206 lost 7 days of timings to one). Find them with `ss -ltnp`
  and `ps`, and never use `pkill -f`.

---

## A — Audit (highest level first; a red at one level makes the levels below it moot)

**L0. Is the right thing gated?** Pytest and four offline guards gate every
PR. `url-state` gates web/ PRs. `verify-smoke` and `verify-blurbs` gate the
publish. Nothing else browser-driven runs unasked.
- Is there a silent-failure class (DECISIONS, `FINDINGS_*`) that only an
  ungated `verify-*` would catch?
- `url-state` is **not a required check** (S211 §3), so a PR can merge red.
  Is "it emails Peter after the deploy" an adequate reader for it? This
  project's standing failure mode is a guard on a channel nobody reads.

**L1. Did the speed-ups keep coverage?** The claims to falsify:
- The shards partition each build's walk exactly. Re-derive the offered views
  per build from the live page (`--views-except=zzz` prints `walking:`), and
  compare the total round trips across shards with one unsharded run.
  S204 recorded public 31 / full 58; expect drift since then, but explain it.
- The change filter (`url-state-changes`) fires on everything the check
  depends on. S212 checked that `verify-url-state.js` requires only
  `playwright`; re-check that, and ask what else could change the served
  page without touching `web/` or `scripts/build_site.py`.
- `--only-shell`: S212 confirmed it from the job log only. Show that the
  headless shell and full Chrome render the walk's screens the same, or that
  the walk never compares pixels.
- The preload: confirm S206's "90/90 status and check counts unchanged" still
  holds on today's suite, not just on the S206 day.

**L2. Is any check slower than it needs to be, where the time is paid?** Only
two places pay wall time: the PR run (`url-state`, and `test` at about 1 min)
and the deploy. Rank them by time × how often they run. A local sweep is paid
only when someone chooses to run it.

**L3. Hygiene.** The runner's "0 checks" reporting, `verify-blurbs` reading red
on the full build, and any assertion-less `verify-*` still listed as `ok`.

**Instruments:**
- Mutate a shard's `flags` and confirm the partition test goes red.
- Use a temporary `--views` typo branch only if the test cannot show it.
- Commit before falsifying (memory `commit-before-falsifying`).

---

## B — Close-out sweep

1. **One full local sweep, alone, on an unloaded box.** Both builds,
   `node tools/profiling/verify.js <url> --jobs 1` (it loads the preload
   itself). Record per-build minutes, the reds and the check counts against
   S206's 38.2 + 43.7 min baseline and its 57.5 min post-preload figure.
   ⚠️ Run verify scripts alone (memory `run-verify-scripts-alone`); a red is
   real only if it reproduces when re-run alone.
2. **Close or rescope every open "Verify runtime" item in `TODO.md`**, with a
   number behind each decision:
   - Fixed sleeps: keep "per script, on promotion", or name the scripts worth
     converting now.
   - The "0 checks" reporting.
   - `verify-blurbs` on the full build.
   - Each closed item gets a `## Done` line (`python tools/todo_archive.py`).
3. **Append the closing numbers to `docs/FINDINGS_verify_runtime.md`** as a new
   section, without rewriting S206's.
4. **Add an `AUDIT_LEDGER.md` row** for the A half. Add a `DECISIONS.md` line
   only if something locks.
5. **Anything that changes CI or a `verify-*` script is proposed to Peter**,
   not merged by the session (memory `merge-docs-only-myself`).
