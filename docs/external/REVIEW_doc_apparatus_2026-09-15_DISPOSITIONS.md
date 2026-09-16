# Dispositions — RUN 2026-09-16 (Session B, Fable 5.1)

**Session B of `docs/FABLE_AUDIT_doc_apparatus.md`.** One disposition per live row of
`REVIEW_doc_apparatus_2026-09-15.md` (line numbers are that file's), against the
premises as `_PREMISES.md` left them. Live rows named by Peter: **4, 5, 7, 8, 9** and
the two proposals recorded in `AUDIT_LEDGER.md` candidate 11. **Not disposed here, by
his call:** 1, 2, 6 (retrieval log's two-week clock restarted 2026-09-16 — re-run
`tools/retrieval_report.py` ~2026-09-30) and 3's `$50k` clamp. Measured on `master`
@ `43b324d`; retrieval log 0 days old, used for nothing.

| rec | disposition | what changed / the argument |
|---|---|---|
| **4** single rewritten handoff file (L92) | ✅ **DECIDED-NO** (Peter, 2026-09-16 — keep one file per session; `DECISIONS.md` that date) | Re-opened by A8 (memory carries lessons, 0 continuity fields) and P10 (the load is `TODO.md`). Measured: the 3 live handoffs are **one read** (`CLAUDE.md`: latest only), **12 KB = 4%** of the 292 KB loaded path; `TODO.md` is 89%. Handoffs are also **findings records**: 3 ledger rows (S48, S56, S99) and 12 docs cite one, and **6 of 8 such citations were dead** — the monthly archive move broke them and `check_doc_citations.py` never looked inside `session-summary/`. **EXECUTED alongside:** the 6 repointed, and the guard now fails on a dead `session-summary/…md` citation. |
| **5** split `DECISIONS.md` + test ID per decision (L93) | split: ✅ **DECIDED-NO** (Peter, 2026-09-16 — stays one log) · test-ID half: **EXECUTED** | `scripts/check_decisions_log.py` on the merge gate: a row dated ≥ 2026-09-17 names a test that exists (`test_x` / `verify-x.js` / `check_x.py`) or is tagged `[unverifiable]`; a cited test that does not exist fails on any row (0 today). Sample of the last 22 rows: 10 cite one, ~6 have a test and did not name it, ~6 are copy/process — so the gate asks a real question, not a tag-everything one. The §3 precondition for any split (8 values unique to this file) is **met**: all 8 now exist in ≥1 other file. |
| **7** append-then-prune quarterly (L97) | prune: **DECIDED-NO** · back-annotate: **EXECUTED** | A6 HOLDS: 13 rows announce a supersession of an earlier row, **4 originals were marked**. The `TODO.md` shape (`## Done` + archive) does not transfer — a closed task stops mattering, a superseded decision is still the referent of the row that superseded it. So: 12 originals now carry `PARTLY SUPERSEDED/AMENDED/REVERSED/RETRACTED <date>` in place, the header says so (item 4), and the same script fails a new announcement whose target is unmarked. A cadence became a write-time check. |
| **8** test-before-prose default (L98) | **EXECUTED** | Lives in three places that fire: `CLAUDE.md` Code Style (loaded every session), `DECISIONS.md` header item 4 (the file you are in when you write a row), and `tests.yml` (the gate). A7: 7.5% of rows are genuinely untestable; the tag covers them. |
| **9** ratio ceiling (L99) | ceiling: **DECIDED-NO** · measurement: **EXECUTED** | A2 FAILS — the number read 0.68 / 1.79 / 1.98 / 1.73 with no prose changing; `.gitattributes` now states the denominator once and `STACK.md` §8 says *sanity check, never tracked*. What A1/P10 say costs is the **loaded path**, which is denominator-free: `retrieval_report.py` now prints it (`292 KB — TODO.md 261 (89%), CLAUDE.md 12, latest handoff 12, MEMORY.md 7`). A number at the place it will be re-read, not a ceiling in a doc — Peter can put a ceiling on it there if it moves. |
| **P1** CI gate on new rows: char cap + test ID | cap: **DECIDED-NO** · test ID: **EXECUTED** (rec 5) | A 500-char cap rejects 227/280 rows and 99% of the last two months; the file is **not** in the loaded path; Peter blessed the log form 2026-09-09. The ledger's objection stands and is in the script's docstring: the gate checks a row NAMES a test that EXISTS, not that the test tests the decision, and the tag is self-applied. |
| **P2** eval harness: ablate a doc, judge scores the delta | as proposed: **DECIDED-NO** · oracle variant: ✅ **DECIDED-NO 2026-09-16 — not viable on this codebase, measured** | 3–5 scenarios × 2 runs cannot separate signal from nondeterminism by the review's own Khatri numbers (L47); a model judging whether a model got worse is the §0 loop; it inherits A4. **The oracle variant was authorised and then killed by its own feasibility check — see §P2 below.** In one line: the ablation has no arm B. `SPEC_temporal.md` §2 is not the sole carrier of its invariants, and no doc in this repo is the sole carrier of an invariant that a non-vacuous oracle scores. |

## Rec 4 — options (✅ **Peter chose A, 2026-09-16**)

| option | costs | loses | rec |
|---|---|---|---|
| **A** keep: one file per session, 3 live, monthly archive | ~12–16 KB written per session; archive grows ~2 MB per 100 sessions, out of the loaded path | nothing | **recommended** — the rec targets 4% of the load |
| **B** single rewritten `HANDOFF.md`, lean on auto-memory | memory must start carrying branch / stopping point / next steps (0 of 34 files do); a rewrite discipline | the per-session record that 15 docs and ledger rows cite as audit output; loaded bytes unchanged (still one read) | no |
| **C** per-session file, template split: STATE (§2/§4/§5) rewritten each time, LESSONS (§3) → memory | one template edit | nothing; the live file shrinks | acceptable |

## Rec 5 split — options (✅ **Peter chose A, 2026-09-16**)

| option | costs | loses | rec |
|---|---|---|---|
| **A** stays a log; the two write-time rules above enforce what the header promises | done | nothing; 0 tokens unless opened | **recommended** |
| **B** short ADR register of "irreversible why" + archived dump | hand-triage of 280 rows for "irreversible"; re-opens the 2026-09-09 header decision | one-place search; 13 supersession chains cross any cut | no |
| **C** date cut: rows older than 90 days → archive file | mechanical | the same chains, and the oldest rows are the shortest (May median 138 ch) — least mass for most breakage | no |

## P2 — the oracle-scored ablation, authorised 2026-09-16 and killed by its own feasibility check

Peter authorised the pilot (1 doc × 2 arms × 5 headless runs, scored by
`verify-temporal.js`, no model judge). **No runs were spent.** Two checks come
before the spend, and the second one ends it.

### 1. The oracle is sound — falsified, not assumed

Baseline green, then `temporalGeom`'s `pts` mutated to position x from the array
index instead of the year value (the exact violation §2 invariant 1 forbids):

```
const pts = ys.map((y, i) => [px(y), py(vals[i])]);          // year value
      ->   [pad + (w-2*pad) * (i/(ys.length-1)), py(vals[i])] // array index

FAIL  x is year-scaled: 2023->2026 is ~3x a one-year step  jump=21.2 step=21.2 ratio=1.00
FAIL  the band covers the missing years only               band=36.3 step=21.2
2 CHECK(S) FAILED
```

So `verify-temporal.js` **measures** the invariant rather than pinning a literal,
and it is not one of the "checks that cannot fail" class. Restored and confirmed
by grepping for the mutated literal (0 hits), not by the suite going green.

### 2. There is no arm B — the ablation removes the *weakest* carrier

The design assumes `SPEC_temporal.md` §2 is where an editing agent learns the
invariant. It is not. Measured on `master`:

| carrier of §2 invariant 1 ("x from the year value, never the array index") | |
|---|---|
| `web/index.html:4601–4620` | a **20-line banner directly above the chart code**, stating BOTH invariants — and stating them **more fully than §2 does** (it carries the 2,322-vs-2,448 correction that §2 lacks) |
| `web/index.html:4853`, `:5015` | two more in-file restatements, one on `devHistGeom` naming "§2 invariant 1" explicitly |
| `tools/profiling/verify-temporal.js:5–11` | the oracle's own header states both |
| `docs/ARCHITECTURE.md:967`, `TRANSITIONS.md:197`, `SPEC_development.md:553` | three further doc copies |

Invariant 2 is carried the same way (`UI.md:1335`, `index.html:4613`, the script
header, `TODO_archive.md:1381`). **Deleting `SPEC_temporal.md` leaves the agent
reading the rule at the edit site**, so both arms see it and the expected effect
is ~0 — and a null at n=5 would be uninterpretable, indistinguishable from
"docs don't help".

### 3. Re-targeting fails too, and the reason generalises

Searched for any invariant a doc carries **alone** and a non-vacuous oracle
scores. Three strata, none yields one. ⚠️ **The constant sweep is exhaustive (all
162 module constants, scripted); the behavioural sweep is NOT** — it went through
the 43 verify scripts' subject areas and their doc citations, not through all
1,174 checks one by one. A doc-only behavioural invariant could survive this
search. What is exhaustive is the carrier-density measurement, and that is what
the conclusion rests on.

- **UI (where the oracles are rich — 43 verify scripts, 1,174 checks):**
  `web/index.html` is **38% comment lines** (2,963 of 7,890), carrying **155 ⚠️
  warning markers** and **54 citations of the docs themselves**. The edit site is
  the primary carrier by construction, so a doc is always the *second* copy.
- **Pipeline (thin — `src/` + `main.py` are 14% comments):** of 162 module
  constants, the ones that are test-covered with a thin code comment
  (`SET_ASIDE_THRESHOLD`, `WEB_PRECISION`, `PERMIT_YEARS_LONG`, `GROUPS`,
  `SQ_M_PER_ACRE`) are guarded by **literal pins** — `assert
  SET_ASIDE_THRESHOLD == 0.90`. A pin fails on *any* change, including the edit
  under test, so it cannot score a silent mistake. `FINDINGS_vacuous_guards_r2.md`
  §250–251 already catalogues exactly these.
- **Genuinely doc-only rationale exists but has no oracle:** `M2_GROSS_PER_UNIT
  = 90.0` keeps its justification (the 70–120 m²/unit sweep, ±5% citywide, "NOT
  where the EPCOR gap comes from") only in `FINDINGS_utility_validation.md` §2.1
  — and **no test references it at all**.

**Conclusion.** The oracle-scored variant is not viable here, for a reason that is
a property of the codebase rather than of the experiment: **this project
co-locates rationale with code by convention** (`CLAUDE.md`: comments where the
why is non-obvious), so a doc is never the sole carrier of an executable
invariant. An ablation of a doc can therefore only ever measure ~0, and the
honest reading of that null is "the rule was still in front of the model", not
"the doc is worthless". ⚠️ **This also bounds what the doc apparatus can be
blamed for**: on executable invariants the docs are redundancy, not the channel.
The rows where docs ARE the sole carrier are the *non-executable* ones — settled
design, rejected alternatives, "do not rebuild it" — and by construction no
oracle scores those, which is what sent the original rec to a model judge and
into the §0 loop.

**Revisit if** the front end is ever split into modules (the `PROPOSAL_lens_registry.md`
route): comment density per file drops, and a doc could become a sole carrier.

### ⚠️ Conflict of interest — read this before accepting §3

`AUDIT_LEDGER.md` already warns that **Opus 5 authored the artifacts under review
and has an interest in finding the one instrument that would measure its own
output unworkable** — it counted four objections. **This is the fifth, written by
Opus 5, and it is the one that actually killed the instrument.** Discount
accordingly, and note what is and is not a judgement call:

- **Not judgement — quotes and counts, all re-runnable above.** That
  `index.html:4601–4620` states both invariants is a quotation, not a reading.
  38% / 2,963 / 155 / 54 / 162 constants are scripted counts. `assert
  SET_ASIDE_THRESHOLD == 0.90` is the test file's own line.
- **Judgement — the inference.** "The rule is at the edit site, therefore both
  arms see it, therefore the effect is ~0" assumes an editing agent reads the
  comment block above the function it edits. That is *likely* but **untested, and
  it is exactly the kind of claim this pilot existed to stop taking on faith.**
- **The cheap way to falsify me**, if Peter wants the instrument to survive its
  author's objection: run **arm B only**, n=3, ablating `SPEC_temporal.md` §2 and
  nothing else. If a doc-less agent breaks an invariant, §2 above is wrong and
  the pilot is back on — at ~30% of the authorised spend. **A green arm B does
  not confirm me**, it is consistent with both explanations; only a red one is
  decisive, and it is decisive *against* this disposition.

## Reproduce

```bash
.venv/bin/python scripts/check_decisions_log.py        # both rules, real file
.venv/bin/python scripts/check_doc_citations.py        # now fails on a dead session-summary/ pointer
.venv/bin/python tools/retrieval_report.py | sed -n 4p # the loaded-path line

# P2 §1 — the oracle is non-vacuous (mutate, expect 2 FAILs, restore)
cd web && ../.venv/bin/python -m http.server 8741 &   # confirm the serving root
node tools/profiling/verify-temporal.js http://localhost:8741/index.html

# P2 §3 — the carrier-density measurement
grep -c '⚠' web/index.html                            # in-file warnings
ls tests/test_*.py | wc -l
```
