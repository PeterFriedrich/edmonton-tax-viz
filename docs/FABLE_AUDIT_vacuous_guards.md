# AUDIT BRIEF — checks that cannot fail

**Read cold.** This is a reusable *instrument*, not a findings doc. The
2026-09-07 run's output is `docs/FINDINGS_vacuous_guards.md`; the coverage map
is `docs/AUDIT_LEDGER.md`.

**Sibling brief:** `docs/FABLE_AUDIT_proxy_guards.md` covers a check reading a
**stand-in** for the property. This one covers a check reading the **right**
property, in a condition, fixture or scope where it **cannot differ**. Both are
green guards that guard nothing; neither is found by running the suite.

---

## §0 — Why this class exists

Nine defects share one shape, and **every one was found by accident** — none by
looking for it.

| # | found | the check | why it could not fail |
|---|---|---|---|
| 1–5 | 2026-09-01 | five assertions | two placed where the value could not be wrong (one *already written* when the bug it should have caught shipped); three freshly written, including a literal `check(true, true)` |
| 6 | 2026-09-05 (S142) | `verify-transport-cost.js` "the two road bases stay distinct" | compared the operating column against the **roads+fire composite**, so the *fire* term supplied the entire gap — one rate wired into both road columns would have passed |
| 7 | 2026-09-05 (S142) | `test_transport_ops_roads_term_differs_from_lifecycle_roads_term` | the fixture set **both** road rates to `$2.0`; green since 2026-08-03 |
| 8 | 2026-09-07 (S144) | `check_cost_copy.py` | greps the **whole file** for the rate string, so a **code comment** satisfies it while the public blurb shows a retired rate |
| 9 | 2026-09-07 (S144) | the acre constant | `SQ_M_PER_ACRE` can be **halved** — doubling every published per-acre figure — with all 784 tests green, because the tests import the constant *from the module under test* |

**The shape:** the assertion names the right property, and the surrounding
context removes the property's ability to vary. The check is not wrong. It is
**unfalsifiable**, which looks identical to *true*.

**Why it is this project's signature failure:** every instance was green. A
check that goes red gets fixed the same day. A check that cannot go red produces
confident, sustained, silent wrongness — and this repo's entire verification
posture exists for silent-correctness failures.

---

## §1 — The hinge fact, confirm before descending

> **A green check is evidence about the system only if you have seen that check
> go red. Until then it is evidence about nothing.**

Three states collapse into one exit code, and the estate cannot tell them apart:

1. the check ran and the property held;
2. the check **did not run** (an early exit, a skipped branch, a script nothing
   invokes);
3. the check ran and **could not have failed**.

⚠️ **Corollary that decides scope: "N passed, 0 failed" is not a measurement.**
Before trusting any pass count, ask how many checks the script *has*. A run
that reports 3 passes from a 37-check script has told you almost nothing, and it
reports success exactly as loudly as a full run.

---

## §2 — Grounding order

1. `docs/AUDIT_LEDGER.md` — both tables; this class is never-audited item 3.
2. `docs/FINDINGS_vacuous_guards.md` — the prior run; re-verify its fixes still
   red when falsified rather than assuming they held.
3. `docs/FABLE_AUDIT_proxy_guards.md` §0 — the sibling class, so instances get
   filed under the right one.
4. `docs/DECISIONS.md` 2026-09-02 and 2026-09-05 (the `verify-*.js` pinning
   rule), and the memory `check-where-the-value-can-be-wrong`.
5. **Then measure. Do not audit from the docs** — the docs record the instances
   that were already found, which is the wrong sample.

⚠️ **Scope: the guard/test estate only** — `tools/profiling/verify-*.js`,
`tests/`, `scripts/check_*.py`, and the workflow wiring that runs them. **Not**
the lenses; they have their own briefs.

---

## §3 — The tiers, ranked by blast radius

**Rank by what a vacuity here would let through, not by how clever it is.**

| tier | estate | what a vacuity costs |
|---|---|---|
| **T1 — the merge gate** | `tests.yml`: pytest, `check_doc_citations`, `check_cost_copy` | a wrong number **on the public site**, shipped by `deploy.yml` minutes later |
| **T2 — the publish path** | `deploy.yml` | ⚠️ **runs no checks at all** — see §5 |
| **T3 — the weekly refresh** | `refresh.yml`: 6 `check_*.py`, `verify-smoke.js` ×2 builds | wrong **data** for up to a week |
| **T4 — the browser harness** | 42 `verify-*.js` | ⚠️ gates nothing today; costs false confidence, and it is the **only** browser verification that exists |
| **T5 — the unit suite** | 784 tests | the cheapest place to falsify (≈11 s), so a vacuity here is the least excusable |

---

## §4 — Per-tier questions

**Every tier, first:** *what would I break to make this red?* If you cannot name
the edit, the check has no defined failure mode and that is the finding.

- **T1/T3 guards.** Does a test exercise the **failure** path, not just the pass
  path? Does the guard's comparison have **locality** — does it constrain *where*
  the value appears, or would any occurrence anywhere in the file satisfy it?
- **T2 wiring.** Which workflow runs this check, on which trigger? A guard in no
  workflow is a guard that gates nothing (`grep` the workflows by filename —
  do not trust a comment that says it runs).
- **T4 scripts.** Does the script have an **early exit** that leaves its body
  unrun and still exits 0? Is the guard on that exit a **DATA** condition or a
  **BUILD** condition? ⚠️ Both builds share the same GeoJSON, so a data-gated
  guard never fires on the public build, where the UI difference actually lives.
- **T5 tests.** Does the test import its expected value **from the module under
  test**? Does the fixture make two supposedly-distinct values equal? Does a
  comparison have an extra term on one side that manufactures the difference?

---

## §5 — Discriminators that keep the finding list honest

- ⚠️ **A literal `true` is not automatically a finding.** `check(name, true)`
  inside an early-exit branch is *reporting* that a branch was taken. The
  finding is not the literal; it is whether the script then **exits 0 with its
  substance unrun**.
- ⚠️ **"No assert" is not automatically a finding.** A test whose body is a call
  with `# no raise` asserts that it does not raise, and reds if it does.
- **Falsify, do not reason.** Reintroduce the defect and confirm **that named
  check** reds. A falsification that reds via a *different* assertion, or reds
  nothing, is itself the finding.
- ⚠️ **Falsify your own instrument too.** A regex that classifies guards, a
  sweep that counts passes — if it cannot be shown to produce a negative, its
  count is not evidence. Report what you confirmed by inspection, not what the
  scanner totalled. (The 2026-09-07 run's guard classifier returned `?` for most
  entries; the count was dropped rather than published.)
- ⚠️ **`pgrep -f <name>` matches the watcher's own command line.** It bit this
  run's own tooling. See the memory `pgrep-watchers-match-themselves`.
- **Do not measure under load.** Concurrent runs manufacture failures on this
  4-core box; re-run any red **alone** before believing it
  (`run-verify-scripts-alone`).

---

## §6 — How to report

Per instance: **the check**, **the property it names**, **the reason it cannot
vary**, **the falsification you ran and what actually went red**, and **the
blast radius from §3**. Then the fix.

A tier with nothing found gets a line saying what you falsified and that it
red — a clean tier is a result, and an unexamined one must not read like it.
