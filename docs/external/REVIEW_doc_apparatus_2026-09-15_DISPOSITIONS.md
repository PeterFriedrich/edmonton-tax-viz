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
| **P2** eval harness: ablate a doc, judge scores the delta | as proposed: **DECIDED-NO** · oracle variant **as specified**: ✅ **DECIDED-NO 2026-09-16** · **routing-ablation redesign: PETER-DECIDES** | 3–5 scenarios × 2 runs cannot separate signal from nondeterminism by the review's own Khatri numbers (L47); a model judging whether a model got worse is the §0 loop; it inherits A4. **The oracle variant was authorised, and its feasibility check killed the specified design and produced a working one — see §P2.** In one line: ablating `SPEC_temporal.md` §2 alone has no arm B, because `CLAUDE.md`'s Key Files entry for `SPEC_temporal.md` carries both invariants into every session; ablating the **routing layer** (that clause + §2's paragraph + the lens section banner) does have one, and both invariants are proven to redden the oracle. ⚠️ **§P2 was materially wrong on first write and was corrected by the Fable 5.1 review the same day** — three errors, all favouring its own conclusion. |

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

⚠️ **That falsifies invariant 1 only, and the first version of this section claimed
both** (Fable 5.1 review, 2026-09-16). Invariant 2 falsified separately — dropping
the low endpoint from `ylab` in `temporalChartSvg`:

```
const ylab = [[9, g.hi], [H - 1, g.lo]]  ->  [[9, g.hi]]

FAIL  both y endpoints are labelled (axis is not zero-based)  5.55% | 2012 | 2026 | no data
1 CHECK(S) FAILED
```

So `verify-temporal.js` **measures** both invariants rather than pinning literals,
and neither is in the "checks that cannot fail" class. Both mutations restored and
confirmed by grepping for the mutated literal (0 hits), not by the suite going green.

### 2. There is no arm B — the ablation removes the *weakest* carrier

The design assumes `SPEC_temporal.md` §2 is where an editing agent learns the
invariant. It is not. ⚠️ **The first version of this section got the reason wrong
in its own favour** — corrected by the Fable 5.1 review, 2026-09-16. Both the
mistake and the correction matter, so both are here.

**What was claimed:** a "20-line banner **directly above the chart code**" at
`web/index.html:4601–4620`. **False.** That banner heads the whole temporal-lens
section (`// --- temporal lens ---`, line 4597); `temporalGeom` is at **4855 —
253 lines below it**. An agent that greps the symbol and reads a window around it
never sees the banner. And `temporalGeom`'s own comment covers the run/gap
derivation but **says nothing about x coming from the year value**. So the
adjacent-carrier claim, which was the load-bearing one, does not hold.

**The actual decisive carrier, missed entirely on the first pass:**

| carrier | |
|---|---|
| **`CLAUDE.md`, Key Files → `SPEC_temporal.md`** | ⚠️ **states BOTH invariants verbatim** — *"x must be scaled from the year value, never the array index; the y axis is not zero-based, so both endpoints must stay labelled"* — in the project instructions **loaded into every session unconditionally** |
| `web/index.html:4597–4620` | the lens section banner: both invariants, more fully than §2 (it carries the 2,322-vs-2,448 correction §2 lacks) — but 253 lines from the function |
| `web/index.html:5015` | `devHistGeom` names "§2 invariant 1" explicitly — a *different* function, 160 lines below |
| `web/index.html:~4932` | `// Both y labels, always — see invariant 2 above` — in situ for invariant 2, but as a **pointer**, not a statement |
| `tools/profiling/verify-temporal.js:5–11` | the oracle's own header states both |
| `ARCHITECTURE.md:967`, `TRANSITIONS.md:197`, `SPEC_development.md:553`, `UI.md:1335`, `TODO_archive.md:1381` | five further doc copies |

**So the ablation has no arm B for a simpler and much harder reason than the one
first given:** deleting `SPEC_temporal.md` §2 leaves the rule in `CLAUDE.md`, which
is loaded every session no matter what the agent reads. Expected effect ~0, and a
null at n=5 uninterpretable — but because of the *project instructions*, not
because of an adjacent comment.

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

**Conclusion — narrowed 2026-09-16 after the Fable review.** What is established is
that **the pilot AS SPECIFIED cannot work**: ablating `SPEC_temporal.md` §2 alone
leaves both invariants in `CLAUDE.md`, loaded every session. The broader claim the
first version made — *"no doc in this repo is ever the sole carrier of an
executable invariant"* — is **overclaimed and withdrawn**. `CLAUDE.md` is itself a
doc, and for these two invariants it is very close to a sole *routing* carrier: it
is the only copy guaranteed to be in context before the agent chooses what to read.

**The redesign that IS viable, and that the first version wrongly foreclosed.**
The unit to ablate is the **routing layer**, not one SPEC section:

| | arm A | arm B |
|---|---|---|
| `CLAUDE.md`'s Key Files invariant clause | present | **removed** |
| `SPEC_temporal.md` §2 invariant paragraph | present | **removed** |
| `web/index.html:4597–4620` section banner | present | **removed** |
| all other code, comments and the oracle | untouched | untouched |
| task | a real edit to `temporalGeom` (e.g. *"the chart is cramped, widen the plot box"*) | same |
| score | `verify-temporal.js` | same |

**This has a real arm B**, which is exactly what the specified design lacked:
`temporalGeom`'s own comment does **not** state the x-scaling rule, so with the
three routing carriers gone an agent editing that function has nothing in front of
it saying x must come from the year value. Both invariants are now proven to
redden the oracle (§1), so a violation is scored rather than eyeballed.

⚠️ **It tests routing, not prose, and must be reported as that** — "did the reader
get pointed at the rule", not "was the SPEC well written". That is a narrower
question than rec P2 asked, but it is the one this codebase can actually answer,
and it is falsifiable.

**Also revisit if** the front end is split into modules (`PROPOSAL_lens_registry.md`):
per-file comment density drops and a doc could become a sole carrier outright.

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
- ⚠️ **THE FALSIFICATION PATH THIS SECTION FIRST OFFERED WAS ITSELF UNFALSIFIABLE,
  and that is the sharpest thing the Fable review found.** It proposed: *"run arm B
  only, n=3, ablating `SPEC_temporal.md` §2 and nothing else."* With that `CLAUDE.md`
  clause intact that arm **cannot go red** — the rule is in context regardless. A
  row arguing against checks that cannot fail shipped a check that cannot fail.
  Same family as `check-where-the-value-can-be-wrong`: **the instrument was wrong
  in the direction that protected the conclusion**, and that is the third time on
  this one page (the banner claim, the both-invariants claim, this).
- **The real falsification path is the redesign in §3** — ablate the routing layer
  (all three carriers), n=3, arm B only. That arm CAN go red. If it does, the
  instrument works and rec P2's oracle variant is back on at full scope. A green
  arm B is still not a confirmation: it is consistent with "the model knows this
  anyway", which no arrangement of this experiment separates.
- **Three of this page's errors were caught by a different model reading it**,
  not by its author re-reading it, and not by any guard. That is a data point
  about the review apparatus worth more than the disposition it corrected.

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
