# Premise evaluation — RUN 2026-09-16 (Session A, Fable 5.1)

**Session A of `docs/FABLE_AUDIT_doc_apparatus.md`.** Tests the *reasoning* of
`REVIEW_doc_apparatus_2026-09-15.md` (line numbers below are that file's); the sibling
`_CLAIMS.md` tests its arithmetic. **No dispositions here — that is Session B.**
Measured on `master` @ `8e92d07`. Every command below is re-runnable from the repo root.

## Grounding counts (§1 confirm-back, re-measured)

- `docs/*.md` **80** (22 named in `CLAUDE.md`; 83 with `docs/external/`); `session-summary/` **3** live + **102** archived.
- `DECISIONS.md` **430 KB, 280 rows** (corrected splitter; median Decision cell 1,259 ch, 28 rows one-sentence).
- Markdown **4,829 KB** (all tracked `.md`, `CODEMAP.md` excluded) ÷ hand-written code **2,440 KB** (`src` 332 + `tools` 816 + `tests` 507 + `web/index.html` 452 + `.github` 28 + `scripts`; vendor and `web/data` excluded) = **1.98:1**; 1.80:1 if `notebooks/` (237 KB) counts as code. Numerator: `docs/` 2,273, `session-summary/` 2,127 (98% archived), `TODO.md` 261, `data/` 158.
- **Loaded path per session** (what a session is told to read): `CLAUDE.md` 12 + `TODO.md` **261** + latest handoff 14 + `MEMORY.md` 7 = **294 KB, 89% of it `TODO.md`.**
- `tools/retrieval_report.py`: **8 calls, 2 sessions, 0 days** — used for nothing below. (Runs only under `.venv/bin/python`; system `python` is too old for its type hints.)

## Premise verdicts (§A1)

| # | verdict | what was measured |
|---|---|---|
| **A1** cost is spread across all artifacts | **FAILS** | An unread doc costs 0 tokens; the loaded path is 294 KB and 89% of it is `TODO.md`, which the review never names. Staleness (`git log -1` age per `docs/*.md`): median **13 d**, 16/80 > 60 d, 1 > 90 d (`SPEC_phase1.md`, 118 d) — and 9 of the 10 oldest are `FINDINGS_*` (A4's set). 0 of 80 docs have zero inbound links from other tracked `.md`. So the cost of the 58 unnamed docs is staleness concentrated in one cluster, not context mass. Recs #6 and #9 are argued from mass (L94, L99). |
| **A2** a md:code mass ratio is a meaningful signal | **FAILS** | The same repo reads 0.68 (review), 1.79 (`_CLAIMS`), 1.98/1.80 (this run) depending only on what the denominator admits — the number moved 3× without a byte of prose changing. 44% of the numerator is `session-summary/`, 98% of which is already out of the loaded path: mass does not separate loaded from unloaded, or agent-facing from public-facing. Review L27 warns of Goodhart; L99 sets a ratio ceiling. Self-undermining on its own terms. |
| **A3** ablation can measure a doc's value | **FAILS** | The proposed verifier is uncoupled from the target: **0 of 43** `tools/profiling/verify-*.js` read a doc (7 mention `docs/` in comments only); the only executables that open `docs/*.md` by path are `tools/codemap.py` (generated file), `tools/todo_archive.py`, and `scripts/check_doc_citations.py` (pointer *existence*). "Remove a doc, run Playwright" (L94) cannot go red. Scale: 160 sessions in 119 days (2026-05-20 → 09-16); L47's 120–200 tasks per single-doc ablation × 58 candidates is unreachable. What IS measurable: L47's process effects — the repeated-mistake tallies memory already keeps (`stranded 9×`, `7 instances now`) and rec #2's hit log. |
| **A4** the reader of these docs is the agent | **FAILS** | 27 `FINDINGS_*` + `DATA_ISSUES` + `EVIDENCE_NOTEBOOKS` = 29. Public inbound links: `README.md` → 3 FINDINGS + `DATA_ISSUES` + `METHODS` + 7 more; `web/` → `DATA_ISSUES` ×3, `METHODS`, `VERIFICATION`, 2 FINDINGS verdicts. **13 docs are reachable from public surfaces and the retrieval log shows 0 agent reads for all of them** — the log is not a prune signal for that set. ⚠️ The other direction: **22 of 27 FINDINGS have no public inbound link and 11 of 18 `DATA_ISSUES` rows are `NOT SENT`** — for those the outsider reader is intended, not evidenced. |
| **A5** this is a solo project | **HOLDS** | `gh`: 300/300 PRs and every non-bot issue by one author; 1 fork, 2 stars; repo PUBLIC, site live. No second human reads or writes the agent-facing docs (handoffs, `TODO.md`, `DECISIONS.md`); L103's threshold ("move to a team") is not met. The public-facing subset is A4's finding, not a counter to this one. |
| **A6** append-only leaves superseded text indistinguishable from current (L12) | ~~**FAILS as stated**~~ **→ HOLDS. CORRECTED 2026-09-16, same day, by the sweep this row said it had not run.** | ⚠️ **The original verdict was reached from three grepped examples (L148, L159, L327) and generalized. The sweep refutes it: of the 51 rows carrying supersede/reverse/reopen language, only 5 carry a `~~strike~~` — 6 in the whole 280-row file.** The mechanism is the opposite of what I claimed: the **new** row announces the supersession ("supersedes the same-day …" L151), and the **original is left unmarked**. Forward-only annotation, so a grep landing on a superseded original gets no signal — which is L12's hazard exactly, and P9 says it bites here. What survives of the original verdict: the audit-trail value is real (`FINDINGS_decisions_index_drift.md` §7 kept its own three wrong counts, 35 → 26 → 22, which is what made the parser defect diagnosable), so a prune that drops originals still deletes the referent of every "supersedes" row. **That makes the remedy question open — it does not make the premise false.** `TODO.md` 87 strikes and `AUDIT_LEDGER.md` 7 are a different file's practice and were never evidence for this one. |
| **A7** most decisions can become a test | **HOLDS — larger than the brief assumed** | Over 280 rows: **234 (83%)** carry a numeric literal/threshold, 240 (86%) a backticked code symbol, **21 (7.5%) neither** (the "unit of analysis" kind); **108 (38%) already cite a test/verify ID**, 132 (47%) mention a test or guard. The untestable boundary is ~7%, not half. |
| **A8** auto-memory now covers the cold-start need | **FAILS for continuity, HOLDS for lessons** | 34 memory files = 22 `feedback` + 10 `project` + 1 `reference`; **0** carry a branch, PR, stopping point or next step; the S160 handoff's §4 is 46 lines of exactly that. 32/34 memory files carry a date inline (none in frontmatter) — they inherit the staleness problem but visibly; one (`sklearn-scipy-in-venv`) exists solely to override a stale handoff note. L104's threshold (~10 sessions without cold-start pain) is untested; the retrieval log can test it once it has weeks. |
| **P9** (added) stale docs cause shipped mistakes *here* (L12) | **HOLDS** | 8 memory files record stale-artifact incidents; `CLAUDE.md` L7 records `TODO.md` lagging reality twice; `guards-must-measure-data-not-metadata` is a stale *string* that kept a guard green. This is the review's strongest premise in this repo and it cuts against any comfort taken from A6. |
| **P10** (added) `session-summary/` is "the single most disproportionate item" (L5) | **FAILS in the loaded path** | 3 live handoffs = **40 KB**; `TODO.md` = **261 KB** and is "read it first". `session-summary/` is 44% of repo markdown by mass but 98% archived. The loaded-path disproportion is `TODO.md`, which the review never mentions. |

Not a premise the review rests on: none of A1–A8 was found spurious; all eight are load-bearing for at least one recommendation.

⚠️ **Read the verdict column with this in mind.** Six of eight premises failed on
first pass, and **sorted by consequence, every premise whose failure protects an
artifact failed** (A1 the 58 unnamed docs, A2 the only metric constraining growth,
A3 the ability to measure at all, A4 the 29 FINDINGS, A6 append-only, A8 the
handoffs) while the two that held are the two that threaten nothing (A5 neutral,
A7 creates work). §A1 names this shape and this file reproduced it. **A6 was then
falsified by one command** — the sweep its own row admitted skipping. The two next
most exposed, flagged by the author against interest: **A2** is an argument, not a
measurement (the ratio moving with the denominator is a reason to *define* the
denominator, not to drop the metric), and **A4** leans on "0 agent reads" from a
log this file's own grounding section says is used for nothing.

## Recommendation survival (§A2 rule 2)

| rec | call |
|---|---|
| 1 retrieval logging | **ALREADY DONE** (hook live 2026-09-16; 0 days of data) |
| 2 doc hit log | **SURVIVES** (A3: it is the measurable process effect) |
| 3 golden coverage of published numbers | **SURVIVES** (executed 2026-09-15; L2, `2017` vintage row, `$50k` clamp open per brief §B1) |
| 4 single rewritten `HANDOFF.md` + lean on auto-memory | **RE-OPENED BY A8, P10** (auto-memory half; the loaded-path mass is `TODO.md`) |
| 5 split `DECISIONS.md` + cite a test ID per decision | ~~RE-OPENED BY A6~~ **SURVIVES** (A6 corrected to HOLDS; A7 strengthens the test-ID half — 38% of rows already cite one) |
| 6 ablate zero-read pointer docs | **RE-OPENED BY A1, A3, A4** |
| 7 append-then-prune quarterly | ~~RE-OPENED BY A6, P9~~ **SURVIVES** (A6 corrected to HOLDS; P9 says something must happen. The open half is prune-vs-back-annotate, which A6's audit-trail point bears on — Session B's call, not settled here) |
| 8 test-before-prose default | **SURVIVES** (A7) |
| 9 ratio ceiling | **RE-OPENED BY A2** |

## Reproduce (the non-obvious ones)

```bash
# A3: verifiers coupled to docs
grep -l 'docs/' tools/profiling/verify-*.js | wc -l   # 7 — all comments
grep -rnE "['\"]docs['\"]\s*/" tests/*.py scripts/*.py tools/*.py src/*.py   # 3 real openers
# A7: DECISIONS rows by testability (corrected splitter, see FINDINGS_decisions_index_drift.md §6)
# A8: memory files carrying state
grep -l -i 'next step\|stopping point\|branch:\|in flight' ~/.claude/projects/-home-opc-edmonton-tax-viz/memory/*.md | wc -l   # 0
# P10: loaded path
wc -c CLAUDE.md TODO.md session-summary/*.md
```
