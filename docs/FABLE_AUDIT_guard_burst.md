# Fable audit brief — THE GUARD BURST: everything shipped since the last audit's baseline

**Target:** the 14 PRs merged between `43b324d` (the master S162's audit measured
against) and `adc5e49`. **Written by Opus 5 in under two days**, apart from S162's
own Session B. **3,088 insertions / 488 deletions across 34 files**, of which the
load-bearing part is **four new guard scripts and ~950 lines of tests for them**.

**Read cold. Do not read S162's or S163's handoff before forming your own view of
§L0 and §L1** — both are Opus 5 arguing that this machinery was worth building.

---

## 0. Why this target, and why you

⚠️ **The precedent is 24 hours old and it is the reason Peter asked for this.**
In S163 Opus 5 ran a feasibility check on an experiment that would have measured
its own output, concluded "not viable", and shipped a verdict containing **three
errors, every one favouring that conclusion** — a comment block called "directly
above the chart code" that is **253 lines** away; a decisive carrier
(`CLAUDE.md`'s own Key Files entry) missed **while it sat in context**; and "both
checks proven to measure" written having falsified one. **The offered
falsification path could not go red.** `AUDIT_LEDGER.md` had flagged that exact
conflict of interest *before* the session, and Opus 5 **quoted the warning into
its own row and made the errors anyway.** Fable 5.1 caught all three in one pass.

So the standing question for this brief is not "is the code correct". It is:
**this burst built machinery whose whole purpose is to catch silent mistakes, and
it was built fast by a model that had just demonstrated it cannot audit itself.**

## 1. What shipped (inventory — verify it, don't trust it)

| PR | what | risk class |
|---|---|---|
| #421 | `scripts/check_colour_clamps.py` (282 lines) + 226 test lines — legend-string/`colorClamp` agreement on `tests.yml`; saturating-share drift WARNS on `refresh.yml` | new guard, two channels |
| #427 | `scripts/handoff_gap.py` (162) + 241 test lines — `PreCompact`/`SessionEnd` hooks name unrecorded work | new guard, **hook-only, not CI** |
| #420 | `scripts/check_decisions_log.py` (210) + 152 test lines — on `tests.yml` | new guard, **see joint A** |
| #423 | `tests/test_loaded_path.py` (64) — fails on a 4th live handoff and on archiving the wrong end | new invariant |
| #426 | `check_todo_branch_refs`, the vintage digest's 13th check (+112 in `vintage_report.py`) | new check on a monthly channel |
| #420 | `check_doc_citations.py` +14 — now fails on a dead `session-summary/…md` citation | extension of an existing guard |
| #425/#428/#430/#432 | `TODO.md` staleness passes | judgement, not machinery |
| #431/#432 | the P2 disposition and its correction | **audited already, by Fable — do not redo** |

## 2. Levels — highest first, and a failure at a level MOOTS the ones below it

Per `docs/FABLE_AUDIT_development_lens.md`'s rule and Peter's standing
preference: **frame on the fundamental decision, not on code nits.** If L0 fails,
say so and stop — do not produce a line-level review of machinery that should not
exist.

### L0 — Should this machinery exist at all?

**Four guards in two days on a single-person project.** The doc-apparatus review
that S162 was disposing asked whether this project's *documentation* had outgrown
its usefulness. ⚠️ **Ask whether the answer was to build more apparatus one level
down.** Each guard is permanent maintenance and a permanent CI second. Concretely:

- What defect class does each guard catch that was **actually occurring**? (#421
  has an answer — the 2026-09-15 audit found the clamps would pass with the
  legend wrong. Check whether the others do.)
- `CLAUDE.md` says *"No abstractions for a single use case — inline until there
  are 3+ call sites"* and *"Make the smallest change that satisfies the request."*
  **Do these four pass their own project's rule?**
- The project's own stated failure mode is **a working guard on a channel nobody
  reads**. Four new signals landed. Count the readers.

### L1 — Does each guard actually fire? (falsify, do not read)

**Red-then-green each one.** `docs/FABLE_AUDIT_vacuous_guards.md` and
`FINDINGS_vacuous_guards_r2.md` define the class; this burst has never been swept
for it. For each: break the thing it protects, confirm red, restore, confirm
green. ⚠️ **Commit before mutating** (`commit-before-falsifying`) — a `git
checkout --` in a mutation loop has wiped an uncommitted fix here before.

Known-good precedent to imitate: S163 falsified `verify-temporal.js` both ways
(index positioning → `ratio=1.00`; dropped `ylab` endpoint → endpoint check red).
**That is the standard of evidence.** "The tests pass" is not.

### L2 — Does the signal reach a reader?

For each guard: which channel, and **who reads that channel unprompted?**
`CLAUDE.md`'s Session Management section is explicit that GitHub issues reach
Peter and only Peter, and that a session sees them solely by going to look.

### L3 — Does the record match what shipped?

`DECISIONS.md` gained several rows in this window, one marked `PARTLY AMENDED`
and two `SUPERSEDED`, all same-day. The `AUDIT_LEDGER.md` P2 row was rewritten
three times in one day. **Check the chains resolve and that no row claims a
disposition the code does not have.**

### L4 — Code level

Only if L0–L3 hold. Normal review of the four scripts and their tests.

## 3. Pre-verified joints — start here, these are measured, not guesses

**A. ⚠️ `check_decisions_log`'s central rule has NEVER FIRED ON A REAL ROW.**
`CUTOFF = date(2026, 9, 17)` (`scripts/check_decisions_log.py:52`) — **tomorrow**
as this brief is written. Rows dated ≥ that: **0**. Every row the burst itself
wrote is dated 2026-09-16 and therefore **exempt from the gate it shipped**. The
17 unit tests exercise it with synthetic dates. **So the guard is green because
nothing has reached it yet, which is indistinguishable from green because it
works.** Verify what happens on the first real row; check the cutoff is not
silently permanent.

**B. `handoff_gap.py` is silent on a docs-only session, by design — and S163 was
one.** It excludes `docs/`, or it fires after almost every commit. S163 landed
**3 PRs and it said nothing.** ⚠️ It also had a **vacuous first write**: the
fallback used `capture_output=`/`text=` (Python 3.7+) against this box's 3.6.8
`python3`, and the `TypeError` was swallowed by a deliberate fail-silent handler
— **printing nothing, for ever, while looking healthy.** Two tests now pin it.
**Re-check both the exclusion's cost and that the 3.6.8 path still works.**

**C. `check_colour_clamps`' band contains today's value on purpose.** S162 argues
this is not vacuity — 4.5% is the share Peter accepted, so a band excluding it
would red the gate to force a decision already made. ⚠️ **That argument is exactly
the shape a vacuous guard's defence takes.** It is Opus 5's argument about Opus
5's guard. Test whether the band can go red in both directions on real data, not
only in the fixtures.

**D. `test_loaded_path.py` is an invariant with no script and no CI step** — it
rides pytest. Confirm it fails on a 4th live handoff *and* on archiving the wrong
end (the count test alone passes that second case, which is the stated reason
both exist).

**E. `check_todo_branch_refs` excluded `docs/` from its branch pattern after 64
false positives.** Check the exclusion does not also hide true positives.

## 4. Out of scope

- **The P2 disposition (#431/#432).** Already audited cross-model, by you. The
  three errors are recorded and corrected; do not re-litigate.
- Anything before `43b324d`.
- The `$50k` clamp value itself — Peter decided it 2026-09-16; the *guard* is in
  scope, the *literal* is not.

## 5. Deliverable

`docs/external/` or a `FINDINGS_*.md`, plus **an `AUDIT_LEDGER.md` row** (the
ledger is the coverage map; a run that does not add a row did not happen). If L0
fails, the deliverable is that verdict and its argument — **not** a line-level
review performed anyway.

⚠️ **Report what you could NOT check, and say plainly where you are agreeing with
Opus 5 rather than having verified.** The failure this brief exists to catch is
agreement that looks like verification.
