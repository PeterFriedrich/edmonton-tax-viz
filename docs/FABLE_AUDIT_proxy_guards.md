# AUDIT BRIEF — proxy readings: checks and wiring that read a stand-in

**Read cold.** This is a reusable *instrument*, not a findings doc. One run's
output lives in `docs/FINDINGS_proxy_guards.md`; the coverage map is
`docs/AUDIT_LEDGER.md`.

---

## §0 — Why this class exists

Five defects in this repo share one shape. None was found by looking for it;
every one fell out of unrelated work.

| # | found | the reading | the stand-in | cost |
|---|---|---|---|---|
| 1 | 2026-08-25 (S119) | "the roll is year N" | Socrata's hand-typed `Period of Coverage` | levy understated **$69.5M / 2.5%**, every guard green for months |
| 2 | 2026-08-26 (S121) | "this archive entry is 2025" | the same pin, frozen at capture time | **the 2025 series is unrecoverable** |
| 3 | 2026-08-27 (S122) | "the roll moved" | the coverage string again, compared in a second place | a false ⚠️ every month, in the one channel that reaches a human |
| 4 | 2026-08-28 | "this change alters the site" | `deploy.yml`'s `web/**` path filter | a merged change silently never deployed |
| 5 | 2026-08-28 | "the tests pass" | a green run on the author's laptop | nothing measures the merged state |

**The shape:** a check, a gate or a piece of wiring asserts a property it never
measures, by reading something *correlated with* that property and easier to
reach. The stand-in is authoritative-looking — a publisher's field, a path
convention, a workflow comment, a literal that was true when typed — so the
reading looks like evidence.

**Why it is this project's signature failure and not a generic one:** every
instance was **green**. A proxy that goes red gets fixed the same day. A proxy
that agrees with reality until the day it doesn't produces confident, sustained,
silent wrongness, and this repo's whole verification posture is built for
silent-correctness failures.

---

## §1 — The hinge fact, confirm before descending

> **A check is only as good as its candidate set, and the candidate set is
> often controlled by the same party whose claim you are checking.**

Instance 2 is the proof and the warning. The remedy for instance 1 was to stop
reading Edmonton's metadata and **measure the parcels** against Alberta's FIR
filings — a genuinely independent source. But `detect_year` can only return a
year **FIR has already filed**. Alberta files months after Edmonton rolls. So
the measurement is blind in exactly the window the roll moves, and "we measure
it now" reads as a stronger guarantee than it is.

**Replacing a proxy with a measurement does not, by itself, close the class.**
Ask what the measurement's candidate set is and who controls it.

---

## §2 — Grounding order

1. `docs/AUDIT_LEDGER.md` — both tables. Prior rows for this class: 2026-08-28.
2. `docs/DATA_ISSUES.md` §1 (the upstream field behind instances 1–3).
3. `docs/DECISIONS.md` 2026-08-25 (the stale-metadata downgrade),
   2026-08-27 (×2), 2026-08-28 (×2).
4. `docs/SPEC_temporal.md` §0 — the freeze rule and why a lost year is lost.
5. Then measure. **Do not audit from the docs** — three of the five instances
   had a comment nearby asserting the correct behaviour.

---

## §3 — The tiers, ranked by blast radius

Work top-down. A proxy in tier 1 moots tidying one in tier 4.

**T1 — IRREVERSIBLE GATES.** A step whose output cannot be recomputed:
`write_archive`'s freeze, anything committed-and-never-rewritten, anything
published outward. ⚠️ **Reversibility, not correctness, is what sets the tier** —
the same wrong reading is a nuisance on a regenerable artifact and permanent
loss on a frozen one. Ask: *does this step share a gate with recomputable
steps?* If so, the gate was sized for the wrong one.

**T2 — PUBLISH GATES.** Guards that hold or release the weekly refresh. Ask of
each: does it measure the data, or read a claim about the data? What does it do
when it *cannot* tell — hold, or proceed? **"Inconclusive → proceed" is itself a
proxy** (absence of a detected problem standing in for absence of a problem),
and it is right for recomputable output and wrong for T1.

**T3 — WIRING.** Triggers, path filters, `if:` conditions, `CHECKS` membership.
Ask: is the trigger the *cause* (what changes the artifact) or a *correlate of
the cause* (what lives in a directory)? Does anything run this on the merged
state, or only on a schedule?

**T4 — DISPLAY.** User-facing copy asserting a vintage, a count, a range. Ask:
is this literal derived from the data, or was it true when typed? What
procedure would have to remember to update it, and does that procedure mention
it? ⚠️ **Check the neighbours** — instance 3 and the `(2024 n/a)` defect were
both six lines from correctly-derived copy.

**T5 — TESTS.** A test whose name claims coverage while its body checks
consistency. Ask: what does this test do when the thing it guards is *absent*
rather than *inconsistent*?

---

## §4 — Per-tier questions

For every candidate, answer in order and stop at the first failure:

1. **What property is asserted?** State it as a sentence with a truth value.
2. **What is actually read?** The literal expression.
3. **What would have to be true for (2) to establish (1)?** Name it.
4. **Who controls that?** If it is the publisher whose claim is under test, or
   a human who must remember, the reading is a proxy.
5. **When they diverge, which way does it fail?** Green-while-wrong is the only
   answer that matters; red-while-right is a nuisance.
6. **What is the reversibility of the thing gated?** Sets the tier.

## §5 — Discriminators that keep the finding list honest

Not every indirection is this class. Record cleared items — a sweep with no
negatives is not a sweep.

- **Machine-maintained ≠ hand-maintained.** Socrata's `rowsUpdatedAt` is
  emitted by the platform on write; `Period of Coverage` is prose someone
  types. The first is a reasonable stamp, the second is the defect. Do not pad
  the list by conflating them.
- **A stated proxy is not a hidden one.** `check_assessment_roll` reads the
  coverage string, says so, downgrades to ❓ and names the measuring guard as
  the authority. That is a proxy handled correctly.
- **Content hashing is the pattern that works.** `check_capital_budget`
  explicitly refuses `Last-Modified` and fingerprints the body instead. When
  proposing a fix, point at it rather than inventing a mechanism.
- **A literal is not automatically wrong.** `CHG_WINDOW_LABEL` is hardcoded
  *on purpose* (`DECISIONS.md` 2026-08-27) — a self-deriving label would have
  renamed the phantom year instead of exposing it. Deriving is not always the
  fix; ask what the literal is *for*.

## §6 — How to report

Per tier: **SOUND / CONDITIONAL / UNSOUND**, the sharpest argument against, and
what evidence would change it. A T1 or T2 UNSOUND moots the tiers below it —
report and stop descending.

⚠️ **Reproduce before reporting.** The T1 finding in the first run was
reproduced by calling `write_archive` twice on a temp file; asserting it from
the code would have been weaker and, on this project's record, roughly a coin
flip on being right about the cause.
