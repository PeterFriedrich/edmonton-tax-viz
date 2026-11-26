# AUDIT BRIEF: which automatic checks protect the Money path, and which steps nothing protects

Written 2026-11-26 (S263, Opus 5.5) at Peter's request. Scoped, not run. A
read-cold instrument: a session that has never seen this repo should be able to
run it from this file.

**Peter's question:** of all the tests, guards, notebooks and CI steps, which
are load-bearing? If a Money-path step went wrong, which checks would go red,
and is there any step that nothing would catch?

**Why now:** the release rests on a human verification chain, C1–C10, kept out of
the repo in `/home/opc/research/edmonton-tax-viz/human_verification/`
(`make_checks_page_draft.py` names the steps). That chain checks the numbers
against City sources, not the automatic checks. This run covers the other half:
for each Money step (C2–C6, plus C8 for the published file), what the machine
already guarantees. Peter's hand checks then go where the machine is weakest.

## §0. Grounding order

1. `docs/FINDINGS_test_estate.md` §1–§3: the six tiers, what each blocks and
   what each has caught. Don't redo it. This run adds the per-step axis it
   doesn't have.
2. `docs/FINDINGS_published_numbers.md` T1b: 9 mutations of committed inputs.
   **A wrong 2026 mill rate and `year` 2025→2019 both passed 892 tests and every
   guard.** Re-run those two first. If they still pass, that is C3's answer
   already.
3. `docs/FINDINGS_vacuous_guards_r2.md` R4: the constants mutation sweep (58 of
   75 moved with the suite green, most triaged as not findings). Don't re-mutate
   constants R4 already triaged. Cite it.
4. `docs/VERIFICATION.md` and `notebooks/verified/01_money_lens.py`: the
   Money notebook's invariants. It runs inside `refresh.yml` and gates the publish.
5. `.github/workflows/refresh.yml`, `tests.yml`, `deploy.yml`: which step runs,
   in which order, and whether it **fails** or **warns** (opens an issue). Read
   the comments; the fail-or-warn choice is decided per guard.
6. `docs/DECISIONS.md`: read the full rows for any guard you are about to call
   weak. "Non-blocking by decision" is not a finding.

**Hinge-fact checkpoint (stop if it fails):** confirm the Money call order in
`main.py` `run()` is still `load_assessment` → `apply_tax_rates` →
`aggregate_by_neighbourhood` → `load_boundaries` → `join_and_calculate` →
`export_geojson`, with `load_property_info` / `build_hood_lot_acres` feeding the
lot-acre denominator. If the order has changed, rebuild the step list in §1
before mutating anything.

## §1. The steps and the mutations

One row per mutation. Each mutation is the **smallest plausible real bug** at
that step: one a refactor or an upstream change could actually produce, not
sabotage. Confirm each site in the code before using it; the sites below are
leads, not line numbers.

| ID | C step | Step | Mutation (lead) |
|---|---|---|---|
| M1 | C2 | roll year | the pipeline reads last year's roll file (swap in a prior-year file with the same schema) |
| M2 | C2 | roll completeness | drop the top 1% of accounts by value from the raw roll (the #818 shape: an account leaves silently) |
| M3 | C3 | rates | one 2026 municipal mill rate wrong in `data/mill_rates.json` by 10% (re-run of published-numbers T1b) |
| M4 | C3 | rate year | `load_mill_rates` picks the prior year's rates |
| M5 | C4 | class mapping | swap two rate classes in `ASSESSMENT_CLASS_TO_RATE_CLASS` (e.g. a non-residential label mapped to residential) |
| M6 | C4 | class splits | use class 1 at 100% and ignore `assessment_class_pct_2/3` |
| M7 | C4 | exempt | exempt accounts taxed at a non-zero rate |
| M8 | C5 | aggregation | `aggregate_by_neighbourhood` drops rows whose hood name fails to normalise (silent drop) |
| M9 | C5 | join | the hood join duplicates rows (a many-to-one turned many-to-many) |
| M10 | C6 | denominator | ground acres used where lot acres are meant, or the reverse |
| M11 | C6 | CRS | area taken before the `to_crs(3400)` (degrees²) |
| M12 | C6 | unit | the m²→acre factor off by a small amount (e.g. 4,046.86 → 4,000) |
| M13 | C6 | set-aside | the set-aside threshold compares the wrong side (`>` ↔ `<`) |
| M14 | C8 | export | `export_geojson` rounds or renames a served money column |

Add a mutation if reading the code shows a likelier bug at a step. Drop one only
with a stated reason.

## §2. Protocol

- Work in a scratch **git worktree** off `origin/master`, never the main checkout.
  Commit the clean tree first (memory: commit before falsifying). After each
  mutation, `git checkout -- <path>`, clear `__pycache__`, and print the loaded
  value to show the mutant is gone (memory: same-length sed leaves stale .pyc).
- **Control run first:** every tier green on the unmutated tree. A tier red in
  the control can't be read for any mutation.
- For each mutation, run every tier that would see it, in the order CI runs them:
  1. pytest (`tests/`), the merge gate's four script steps;
  2. `main.py` on the real data in `data/raw/`, then the `refresh.yml` data
     guards in order, each recorded as **fail / warn / green / not reached**;
  3. `notebooks/verified/01_money_lens.py`;
  4. `build_site.py` + `verify-smoke.js` (public and full). Run browser checks
     **alone** (no concurrent Chromium; check `/proc/loadavg`).
- `df -h /` before the first pipeline run. Pipeline outputs go in the worktree,
  and the worktree is removed at the end.
- Record **which check went red and its message**, not only red/green. A red with
  an unrelated message (a crash downstream) is a "caught by accident" row, not
  coverage.
- A mutation that no tier catches is the key result. Before reporting it,
  re-check that the mutant was actually loaded and changed a served value
  (diff the served file against the control). A mutation that changes nothing
  served is not a gap.

## §3. Questions, highest level first

- **L0.** Is "mutate one step, see what goes red" the right measure of
  load-bearing here? Sharpest objection: real bugs here have come from upstream
  data (`DERELICT RESIDENTIAL`, GTFS dates), not code edits. If so, M1/M2-type
  data mutations should count for more than code ones; say so in the verdict.
- **L1.** Per C step: is at least one **blocking** check red for every mutation?
  SOUND / CONDITIONAL / UNSOUND per step.
- **L2.** Single points of failure: a check that is the **only** blocking red for
  some mutation. These are load-bearing. List them by name, with which mutations
  they alone catch.
- **L3.** Redundancy: mutations caught by 3+ blocking checks. Not a defect;
  `FINDINGS_test_estate.md` §5 records deliberate duplication. Report the count
  and leave it.
- **L4.** Channel: for warn-only catches, does the warning reach a reader (an
  issue, not a log)? Cross-check against `docs/FINDINGS_guard_channels.md`.

## §4. Outputs (two files plus the loop)

1. **`docs/FINDINGS_money_path_checks.md`**: the matrix (mutations × checks,
   each cell fail / warn / green / not reached, with the red message), the L0–L4
   verdicts, and a non-empty **What this run got wrong** section.
2. **`docs/MONEY_PATH_CHECKS.md`**: the **human-readable checklist**. For
   someone who doesn't read code (Peter, a reviewer, a volunteer). One section per
   C step (C2–C6, C8), each with:
   - *What could go wrong*, in one plain sentence per mutation.
   - *Stops the publish:* the checks that block, named in plain words (e.g. "the
     weekly Money notebook's 'aggregation can't lose value' check"), each with its
     file in brackets.
   - *Only warns:* checks that open an issue but don't block.
   - *Nothing catches this:* stated plainly. Your hand check C*n* is the only line.
   - *How to re-check:* the one command that reproduces the row.
   - A dated "last measured at `<sha>`" line at the top. The file is a snapshot,
     re-measured by re-running this brief, never updated by hand.
   No check is called load-bearing in the checklist without a matrix row behind it.
3. Close the loop: a row in `docs/AUDIT_LEDGER.md` (executed audits plus one
   register row per finding), `TODO.md` follow-ons for each gap, and a
   `DECISIONS.md` row only if a decision locks. Gaps found are **reported, not
   fixed** in this run: a new guard is a code PR for Peter.

## §5. Model and scope

Opus 5.5 by default; a different model is optional for a second read, not
blocking (memory: audit model default). The brief's author is the same model
that wrote many of these checks, so a result that says "the checks are fine" gets
the harder look, not the easier one.

Out of scope: lenses other than Money (Roads has its own notebook and audit;
Development, Services beyond roads, Ratio, Uses, Glass and Temporal are not
covered by this run and the checklist says so); whether the numbers are correct
against the City (that is C1–C10); the browser suite beyond `verify-smoke.js`
(it gates nothing).
