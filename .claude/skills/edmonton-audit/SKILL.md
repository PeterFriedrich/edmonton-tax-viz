---
name: edmonton-audit
description: >
  Focused audit skill for the Edmonton revenue-per-acre fiscal analysis project.
  Use this whenever the user asks to audit, review, check, or QA the pipeline,
  a lens, or project files. Picks ONE audit target per run; grounds in
  docs/AUDIT_LEDGER.md before scoping and adds a ledger row after executing.
  Triggers on: "audit my code", "check the pipeline", "review my project",
  "what should I look at", "is this right", or any QA/review request in the
  context of this project.
---

# Edmonton Revenue-Per-Acre Audit Skill

## Purpose

This project is a public civic analysis — methodology errors will be scrutinized.
The goal of each audit run is a **single, deep, actionable verdict** on one
target. Do not attempt a broad sweep; pick one focus, go deep, produce clear
verdicts + specific fixes. One target per run — a focused single-target audit
is more useful than a shallow pass over everything.

## The audit ecosystem (know the pieces before you start)

- **`docs/AUDIT_LEDGER.md`** — the coverage map: one row per *executed* audit
  run, plus a ranked never-audited inventory. **Read it FIRST when scoping;
  add a row when your audit executes.** This skill and the ledger are two
  halves of one loop.
- **Briefs** (`docs/FABLE_AUDIT_*.md`, `docs/DATA_INTEGRITY.md`) — reusable
  read-cold *instruments*. A brief is written once and can be re-run; it holds
  the grounding order and the questions, never the findings.
- **Findings** (`docs/FINDINGS_*.md`, or handoff sections for smaller runs) —
  one run's *output*. Never duplicated into the ledger (one-line verdict +
  pointer only).
- **`docs/DECISIONS.md`** — if an audit locks or reopens a decision, append a
  one-liner there too.

## How to run an audit

### Step 1 — Ground before scoping (non-negotiable)

1. Read `docs/AUDIT_LEDGER.md` — both tables.
2. Cross-check the latest 2–3 session summaries in `session-summary/`.
   **TODO.md can lag executed work** — a backlog item that "smells like an
   audit" may have already run and only be recorded in a handoff (this nearly
   caused a full re-run once). If the ledger and TODO disagree, the ledger +
   summaries win; reconcile TODO in your PR.
3. Remember ledger verdicts are **point-in-time**: a target audited before a
   relevant change is fair game to re-audit — say so explicitly ("re-run,
   prior row YYYY-MM-DD, delta since: …").

### Step 2 — Pick ONE target

- If the user named a target, use it.
- Otherwise take the top of the ledger's "Never audited" ranked list, or —
  for correctness work — the `docs/DATA_INTEGRITY.md` joint ranking (T1–T7).
- Tell the user which target you picked and why before going deep.

### Step 3 — Choose the audit family

**(a) Decision audit** (lenses, metrics, published claims — the default for
anything user-facing): audit the **fundamental decisions top-down, highest
level first**, not the code. The house pattern is
`docs/FABLE_AUDIT_development_lens.md` — read its §0 before writing anything.
Its load-bearing rules:

- Build the target's **decision stack** (L0 "should this be published at all"
  → … → Ln "is the code right") and evaluate in order. **When a level is
  unsound, everything beneath it is moot** — don't polish a z-score edge case
  under a broken unit-of-analysis choice.
- Per-level verdicts: **SOUND / CONDITIONAL** (sound only if a stated caveat
  holds) **/ UNSOUND**, plus the single sharpest argument against the level
  and what evidence would change the verdict.
- Not looking for reassurance: assume the authors believe their own lens;
  the value is the argument they didn't make against themselves. One finding
  that kills a level beats ten that polish one.
- Ground in the repo's written reasoning (SPEC, DECISIONS.md, prior
  FINDINGS) and *challenge* it — don't re-derive it.
- For a substantial new target, **write the brief as a standalone
  `docs/FABLE_AUDIT_<target>.md`** (read-cold: grounding order, a
  confirm-the-hinge-fact checkpoint, the stack, per-level questions) so the
  instrument outlives the run and round-2 deltas can reuse it.

**(b) Correctness audit** (silent-wrong-numbers risk): use
`docs/DATA_INTEGRITY.md` as the map; verdicts are **PASS / FAIL / WARN** per
target. The classic checklists (CRS, silent drops, methodology) are in the
appendix below.

### Step 4 — Deliver verdicts

Decision audits: one verdict line per level, sharpest counter-argument,
evidence-that-would-change-it. Correctness audits:

```
## Audit: [Target]
**Verdict:** PASS / FAIL / WARN
**Finding:** [One paragraph. Quote the actual line if there's a bug. Don't hedge.]
**Fix (if needed):** [Concrete change; if PASS, what you confirmed and why.]
```

### Step 5 — Close the loop (this is what makes the run count)

1. **Add a row to `docs/AUDIT_LEDGER.md`**: date, target/scope, instrument,
   output pointer, one-line verdict, outstanding items. Follow the existing
   rows' style.
2. Write findings where they belong: a `FINDINGS_*.md` for big runs, the
   session handoff §2 for delta/smaller runs — the ledger row just points.
3. Reconcile `TODO.md` (tick executed items, add follow-up items for
   CONDITIONAL/WARN outcomes) and append to `DECISIONS.md` if a decision
   locked or reopened.
4. Update the ledger's "Never audited" list if your run covered (or
   surfaced) an inventory item.
5. Ship as a PR like any other docs change (`git pull` master before cutting
   the branch — ledger/DECISIONS/TODO tails are append-conflict magnets).

## Escalation

A FAIL on CRS, silent drops, or anything that makes published numbers wrong is
**blocking** — stop auditing other targets in the same run; the numbers can't
be trusted until it's fixed. An UNSOUND on a top decision level moots the rest
of that stack: report it and stop descending. WARN/CONDITIONAL/architecture
issues: list them, let the user decide order.

---

## Appendix — correctness checklists (family b)

### CRS correctness
The most dangerous silent failure. `.to_crs()` must be explicit before any
`.area` call; target is **EPSG:3400** (NAD83 / Alberta 10-TM Forest) end to
end. EPSG:4326 areas are degrees² — wrong numbers, no error. Flag
**EPSG:26911** (UTM 11N) as an inconsistency: valid metric CRS, but Edmonton
sits at Zone 11's eastern edge and it breaks pipeline consistency.

### Silent data drops
Spec requires unmatched records flagged, never silently dropped. Check: names
normalized before joins; explicit unmatched-row check after; counts + examples
logged; before/after record counts visible so drift shows.

### Module independence
Each `src/` module runnable standalone: own/argued paths, no top-level state
imports from sibling modules, existence checks on upstream outputs, traceable
raw → joined → calculated → output flow.

### Methodology
Value per acre = summed (not averaged) assessed value ÷ acres, units checked
(1 km² = 247.105 acres); exclusions (farmland, exempt, DERELICT) documented
and intentional; denominator source (polygon area vs dataset field) stated.

### DATA.md currency
Column names, row counts, name quirks, join match rates, exclusions — all
matching reality. A stale DATA.md means knowledge is leaking between sessions;
flag it.
