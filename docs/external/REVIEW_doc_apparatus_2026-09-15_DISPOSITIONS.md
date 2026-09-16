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
| **4** single rewritten `HANDOFF.md` (L92) | **PETER-DECIDES** — table below | Re-opened by A8 (memory carries lessons, 0 continuity fields) and P10 (the load is `TODO.md`). Measured: the 3 live handoffs are **one read** (`CLAUDE.md`: latest only), **12 KB = 4%** of the 292 KB loaded path; `TODO.md` is 89%. Handoffs are also **findings records**: 3 ledger rows (S48, S56, S99) and 12 docs cite one, and **6 of 8 such citations were dead** — the monthly archive move broke them and `check_doc_citations.py` never looked inside `session-summary/`. **EXECUTED alongside:** the 6 repointed, and the guard now fails on a dead `session-summary/…md` citation. |
| **5** split `DECISIONS.md` + test ID per decision (L93) | split: **PETER-DECIDES** — table below · test-ID half: **EXECUTED** | `scripts/check_decisions_log.py` on the merge gate: a row dated ≥ 2026-09-17 names a test that exists (`test_x` / `verify-x.js` / `check_x.py`) or is tagged `[unverifiable]`; a cited test that does not exist fails on any row (0 today). Sample of the last 22 rows: 10 cite one, ~6 have a test and did not name it, ~6 are copy/process — so the gate asks a real question, not a tag-everything one. The §3 precondition for any split (8 values unique to this file) is **met**: all 8 now exist in ≥1 other file. |
| **7** append-then-prune quarterly (L97) | prune: **DECIDED-NO** · back-annotate: **EXECUTED** | A6 HOLDS: 13 rows announce a supersession of an earlier row, **4 originals were marked**. The `TODO.md` shape (`## Done` + archive) does not transfer — a closed task stops mattering, a superseded decision is still the referent of the row that superseded it. So: 12 originals now carry `PARTLY SUPERSEDED/AMENDED/REVERSED/RETRACTED <date>` in place, the header says so (item 4), and the same script fails a new announcement whose target is unmarked. A cadence became a write-time check. |
| **8** test-before-prose default (L98) | **EXECUTED** | Lives in three places that fire: `CLAUDE.md` Code Style (loaded every session), `DECISIONS.md` header item 4 (the file you are in when you write a row), and `tests.yml` (the gate). A7: 7.5% of rows are genuinely untestable; the tag covers them. |
| **9** ratio ceiling (L99) | ceiling: **DECIDED-NO** · measurement: **EXECUTED** | A2 FAILS — the number read 0.68 / 1.79 / 1.98 / 1.73 with no prose changing; `.gitattributes` now states the denominator once and `STACK.md` §8 says *sanity check, never tracked*. What A1/P10 say costs is the **loaded path**, which is denominator-free: `retrieval_report.py` now prints it (`292 KB — TODO.md 261 (89%), CLAUDE.md 12, latest handoff 12, MEMORY.md 7`). A number at the place it will be re-read, not a ceiling in a doc — Peter can put a ceiling on it there if it moves. |
| **P1** CI gate on new rows: char cap + test ID | cap: **DECIDED-NO** · test ID: **EXECUTED** (rec 5) | A 500-char cap rejects 227/280 rows and 99% of the last two months; the file is **not** in the loaded path; Peter blessed the log form 2026-09-09. The ledger's objection stands and is in the script's docstring: the gate checks a row NAMES a test that EXISTS, not that the test tests the decision, and the tag is self-applied. |
| **P2** eval harness: ablate a doc, judge scores the delta | as proposed: **DECIDED-NO** · oracle variant: **MEASUREMENT-PENDING** | 3–5 scenarios × 2 runs cannot separate signal from nondeterminism by the review's own Khatri numbers (L47); a model judging whether a model got worse is the §0 loop; it inherits A4. **The variant that needs no judge:** for a doc that warns about an executable invariant (`SPEC_temporal.md` §2 ↔ `verify-temporal.js`), run a headless task with and without the doc in a worktree and score with the existing verify script. Detects a large effect at ~5 runs per arm. Exists when Peter authorises the spend — a pilot is 1 doc × 2 arms × 5 runs. |

## Rec 4 — options (Peter's call)

| option | costs | loses | rec |
|---|---|---|---|
| **A** keep: one file per session, 3 live, monthly archive | ~12–16 KB written per session; archive grows ~2 MB per 100 sessions, out of the loaded path | nothing | **recommended** — the rec targets 4% of the load |
| **B** single rewritten `HANDOFF.md`, lean on auto-memory | memory must start carrying branch / stopping point / next steps (0 of 34 files do); a rewrite discipline | the per-session record that 15 docs and ledger rows cite as audit output; loaded bytes unchanged (still one read) | no |
| **C** per-session file, template split: STATE (§2/§4/§5) rewritten each time, LESSONS (§3) → memory | one template edit | nothing; the live file shrinks | acceptable |

## Rec 5 split — options (Peter's call)

| option | costs | loses | rec |
|---|---|---|---|
| **A** stays a log; the two write-time rules above enforce what the header promises | done | nothing; 0 tokens unless opened | **recommended** |
| **B** short ADR register of "irreversible why" + archived dump | hand-triage of 280 rows for "irreversible"; re-opens the 2026-09-09 header decision | one-place search; 13 supersession chains cross any cut | no |
| **C** date cut: rows older than 90 days → archive file | mechanical | the same chains, and the oldest rows are the shortest (May median 138 ch) — least mass for most breakage | no |

## Reproduce

```bash
.venv/bin/python scripts/check_decisions_log.py        # both rules, real file
.venv/bin/python scripts/check_doc_citations.py        # now fails on a dead session-summary/ pointer
.venv/bin/python tools/retrieval_report.py | sed -n 4p # the loaded-path line
```
