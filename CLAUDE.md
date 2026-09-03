# Claude Instructions

## Project
Edmonton revenue-per-acre fiscal analysis. Python-only, no GIS software.

## Key Files
- `TODO.md` — living backlog and **the source of truth for progress**. Read it first to know what to work on; update it in place as items open/close. Session summaries narrate *what happened*; TODO.md owns *what's left*. Never redo a closed item without asking — its `## Done` section lists every closed item in one line each. Conversely, an *open* item can be stale — reproduce the symptom and re-measure the stated cause before acting on it (it has lagged reality twice). **When an item closes, move its body to `docs/TODO_archive.md` and leave a `## Done` line** (`python tools/todo_archive.py` does it in bulk) — this file is read every session, so it must hold live work, not history.
- `docs/SPEC_phase1.md` — what we're building and why
- `docs/DECISIONS.md` — append-only index of locked decisions: one line + pointer to the doc holding the full reasoning. **Add a line whenever a decision locks; never duplicate rationale into it.** Check it before re-opening anything that feels "already settled".
- `docs/RUNBOOK.md` — live-site operations: the monthly vintage digest (§0), January year-roll checklist, weekly-workflow failure triage. **Read when the refresh workflow fails, the site shows a banner, or a `⚠️ Vintage & pin digest` (§0) or `⚠️ Big revenue delta` (§0b) issue lands.**
- `docs/SPEC_services.md` — services lens (cost side; roads first): metric, filters, locked decisions, build order
- `docs/SPEC_temporal.md` — temporal lens (assessment over time, per neighbourhood) — **COMPLETE and live in `/full/`**. **Read §0 before touching anything that reads the historical assessment file: its 2024/2025 slices are PROVEN incomplete, **2024 AND 2025 are both omitted by decision** (2025 joined them 2026-08-27 — the archive entry that was covering it turned out to be the 2026 roll mislabelled, and the real 2025 is unrecoverable), so the published list is **2012–2023 + 2026** and the gap is deliberately NON-CONTIGUOUS and TWO YEARS WIDE — don't "fix" it.** **Read §2 before editing the chart or the panel:** two rendering invariants fail silently there (x must be scaled from the year value, never the array index; the y axis is not zero-based, so both endpoints must stay labelled).
- `docs/ARCHITECTURE.md` — module interfaces, data flow, testing approach. **Read before writing any module.**
- `docs/STACK.md` — one-page inventory of what the project is built out of: pinned versions, the two requirements files and why they differ, the frameworkless front end, the four CI workflows, and §9's list of what this project deliberately does NOT use. **Read when onboarding, adding a dependency, or before proposing a tool/framework.**
- `data/DATA.md` — data source details, column names, known quirks. **Read before touching any data files. Update if you discover anything new.**
- `docs/TOKEN_EFFICIENCY.md` — context/token hygiene (what NOT to read raw, session-summary archiving, how to navigate the big front-end file). **Read before bulk-reading data or summaries.**
- `docs/CODEMAP.md` — **generated** symbol index for `web/index.html` (~7,345 lines): every top-level symbol with its line range + purpose, plus every element id. **Look a symbol up here before scanning the file, and read one large slice rather than many small windows** (the S79 cost lesson). **Regenerates automatically** — a `PostToolUse` hook re-runs `tools/codemap.py` whenever `Edit`/`Write` touches `web/index.html`, so it is always fresh; run it by hand only if you edit that file outside the tools. Never cite its line numbers — they drift.
- `docs/ANALYSIS_BACKLOG.md` — analytical questions/investigations to run later (auto + by-hand). Distinct from TODO.md (build work) and FINDINGS_*.md (conclusions).
- `docs/PARCEL_LEVEL_OPPORTUNITIES.md` — future work gated on parcel-level data (finer than the neighbourhood unit); the set-aside machinery exists because we aggregate to neighbourhood.
- `docs/MOBILE_USABILITY.md` — mobile/phone usability work: the desktop↔mobile separation seam (`@media` block; render is shared, chrome is isolatable), confirmed vs unconfirmed problems, quick-pass plan. **Read before touching layout/CSS for small screens; keep the CONFIRMED/NEEDS-CONFIRMATION split honest.**
- `docs/CONTROLS_MATRIX.md` — current-state snapshot of every view × control combination (what shows when, what gates what, the three control tiers) + flagged "weird combos" that are unpack/regroup candidates. **Read before regrouping controls or adding a view/sub-metric; grouping is shared DOM so it drives desktop AND mobile. `docs/UI.md` is the build log; this is the state space.**
- `docs/DATA_INTEGRITY.md` — standalone audit brief for checking the numbers are *right* (silent-correctness, not crashes). Point a model here for a full data-integrity pass: system map + ranked, pre-verified joints. Complements the `edmonton-audit` skill (which goes deep on ONE target).
- `docs/AUDIT_LEDGER.md` — coverage map of executed audit runs: what's been audited, when, verdicts, what never has. **Add a row when an audit executes; check it before scoping a new audit.**
- `docs/DATA_ISSUES.md` — register of defects in data we DON'T control (Edmonton Open Data, FIR, GTFS): evidence, what it breaks here, and **whether the publisher has been told**. **Add a row whenever an upstream defect is confirmed, and update the status when a report is actually sent** — "the artifact exists" is not sent, and a finding that never leaves the repo is the standing failure mode here. Distinct from `data/DATA.md` (what a source *is*).
- `docs/EVIDENCE_NOTEBOOKS.md` — inventory of the **standalone evidence notebooks** backing `DATA_ISSUES.md`: what each claims, which datasets it stands on (**both directions** — per report, and per source), invariants, and published URL. **Read before adding a report or touching one's data sources**; `q7d6-ambg` is a single point of failure for all four and nothing re-runs them on a schedule. Records why the duplicated helper block is deliberate. Distinct from `docs/VERIFICATION.md` (`notebooks/verified/`, which gate the weekly publish).
- `docs/REMOTE_VM.md` — **read FIRST in a Claude Code web/remote VM session** (repo at `/home/user/...`, no conda, empty `data/raw/`): network-policy constraints + fix, environment setup, headless-verify workarounds.
- `session-summary/` — session handoff notes. Read the latest before starting work; older ones live in `session-summary/archive/` (don't bulk-read them).

## Token Efficiency
- **Never `Read` raw `.geojson`/`.csv` data files** — the zoning GeoJSON alone is ~2.3M tokens. Inspect via a small python/geopandas summary instead. See `docs/TOKEN_EFFICIENCY.md`.
- Read only the **latest** session summary; keep the 3 most recent at top level, archive older.

## Session Management
- Always run `/handoff` before `/clear` — never wipe context without a written record in `session-summary/`
- Commit after each working unit with a descriptive message, rather than batching a session into one commit
- **Pushing is normal — push proactively after committing, in every environment (including the Oracle box). Don't wait for a "push it" confirmation.** This is standing authorization; it overrides the harness default of pushing only when asked. (Committing still follows the usual flow; this is specifically about not holding pushes.)
- **Remote/cloud VM sessions (Claude Code on the web): commit + push proactively — don't wait for Peter's push command.** The container is ephemeral and gets reclaimed on inactivity; unpushed work is LOST when that happens. Rules:
  - Push to the session's designated branch at every natural checkpoint (module + tests green, docs updated, feature milestone) — small pushed commits beat one perfect unpushed one.
  - If usage/budget feels like it might run out, or a long task is only partly done: STOP, write the handoff (state, stopping point, next steps), commit, push. A half-done feature safely on origin is recoverable; a finished one in a dead container is not.
  - Peter may be away — never hold work hostage waiting for a "push it" confirmation in these environments. (This overrides the usual only-push-when-asked default.)
  - Environment quirks (network policy, setup, headless verify): `docs/REMOTE_VM.md`.
- **⚠️ Peter merges PRs MID-SESSION, often within minutes. Re-check before EVERY push to an existing branch — not once per session.** Commits pushed to a branch after its PR merged land on a dead branch: they reach origin, the branch looks up to date, and they are **not on master**. This has stranded work 7+ times, twice in one session. Checking once at the start does not help — the danger is every push *after* the merge.
  - Enforced by a `pre-push` hook (`.githooks/pre-push`) that blocks a push to a branch whose PR is `MERGED`. **A fresh clone must enable it: `git config core.hooksPath .githooks`** (hooks are not cloned). It fails OPEN — no `gh`, no auth, no network, no PR — so it can never be the reason work goes unsaved. Escape hatch: `git push --no-verify`.
  - The hook cannot catch everything. After any merge, confirm the work actually landed: `git merge-base --is-ancestor <sha> origin/master`. A merged PR is necessary, not sufficient.

## Code Style
- Keep processing steps as separate, independently runnable modules in `src/`
- No silent data drops — flag unmatched or missing records explicitly
- Always set CRS explicitly before any area calculation

## Comments & Scope
- Comments only where the *why* is non-obvious. Don't narrate what the code plainly does.
- Make the **smallest change that satisfies the request**. Don't refactor, rename, or reformat code you weren't asked to touch. No new files unless required.
- No abstractions for a single use case — inline until there are 3+ call sites. (This is about speculative helpers. The `src/` module split above is a deliberate architecture choice, not an abstraction to collapse.)
- Deleting obsolete code is valid and **preferred** over leaving it behind.
- **Propose the plan first** for: a new module, a change to a data contract or output schema, or anything that changes CI behaviour. Routine edits don't need a proposal — just make them.
- These are scope rules, not verification rules. They do **not** relax `no silent data drops`, the guard scripts, or reproducing a bug before fixing it — this project's failures are silent-correctness failures, and that discipline is why they get caught.

## Deployment Horizon
- Configurable paths over hardcoded ones
- Structured output over print statements for logging
- Clean module boundaries so rendering can be swapped out later
