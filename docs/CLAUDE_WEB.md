# CLAUDE_WEB — giving a Claude web chat the project, and getting rows back

**Read when:** starting a research chat in claude.ai about this project, or
setting up its claude.ai Project.

Claude web sees only what it is given. The brief, `scripts/make_brief.py`, is
built from `CLAUDE.md`, `docs/SCOPE.md`, `docs/DECISIONS.md`, `TODO.md`,
`docs/DATA_ISSUES.md` and `requirements-ci.txt`, so the "my situation" block
is never re-typed by hand. It ends with a required reply format whose tables
map onto `TODO.md` / `DECISIONS.md` rows.

Ported by hand from `cc-data-project-template` (copier never runs on this repo).
Differences from the template, each deliberate (2026-09-30):

- **No merge-gate staleness test; `/handoff` regenerates the brief.** TODO.md
  and DECISIONS.md change in most PRs here, so a gate would put a `BRIEF.md`
  diff in nearly every PR. Master's copy is at most one session stale.
- **The synced set is the brief and the specs only** — not `ARCHITECTURE.md`
  (84 KB) or `data/DATA.md` (165 KB). With them the set is ~620 KB and the
  Project falls back to retrieval.
- The generator reads this repo's shapes: `requirements-ci.txt` for the stack,
  DATA_ISSUES's "Status at a glance" table, and each decision row's first
  sentence **plus its first rejected-alternative sentence**.

## Sync the brief into a claude.ai Project

1. The brief is committed as `docs/BRIEF.md`; `/handoff` re-runs
   `.venv/bin/python scripts/make_brief.py --write` and commits it with the
   handoff. `--check` exits 6 if it is stale.
2. In claude.ai, use a **private** Project (the GitHub integration is not
   offered on a shared one) and add the repo from GitHub. Select the
   **synced set** below. Add `CLAUDE.md` or `TODO.md` in full only if the
   project's capacity allows — the brief already summarises both.
3. ⚠️ **The sync is manual.** claude.ai fetches the files when you press
   **Sync now**, not on push. A green merge gate means the *repo's* files are
   current, not the Project's copy. Press Sync before each research chat.

### The synced set

The brief is a generated summary; it does not carry the spec itself. The spec
docs sync as they are — they are the real thing, not a summary:

- `docs/BRIEF.md` — generated, always
- `docs/SPEC_*.md` — each one (nine as of 2026-09-30, ~277 KB)
- `docs/REPORT_CLAIMS.md` — the claims register for the written report
  (added 2026-10-03; see "Report rounds" below)

In git pathspec form (the handoff skill uses this exact list):
`docs/BRIEF.md 'docs/SPEC_*.md' docs/REPORT_CLAIMS.md`. To sync another file, add it in four places
together: here, the handoff skill's command (`.claude/skills/handoff/SKILL.md`
§"Claude web sync check"), the `CLAUDE.md` line for this doc, and the claude.ai
Project.

### Knowing when to press Sync

Claude web has no hooks, so the reminder comes from the Claude Code side, at
the two points the owner already reads:

- **A PR that changes a synced file opens its description with**
  "**After merge: press Sync in the claude.ai Project.**" claude.ai reads
  master, so merge is the moment it goes stale.
- **`/handoff` checks** whether a synced file changed on master since the
  previous handoff, and if so makes that the first Next Step.

The integration reads file contents only — no history, PRs or issues. A
research chat that needs one of those gets it pasted.

## Before each research round

- Update `docs/SCOPE.md` if an idea was turned down since the last round.
- Keep the brief's reply-format section in the prompt (it is in the brief;
  if the prompt is written separately, say "end with the brief's reply format").
- File the reply outside the repo first (on the owner's server,
  `/home/opc/research/<repo>/`), then triage its
  tables into `TODO.md` / `docs/DECISIONS.md` by hand. A parser for them
  (`ingest_reply.py`) is deferred until three rounds have used the format —
  `docs/FINDINGS_harvest.md` §"D (spec sheet): recommendation".

## Report rounds

The written report is a Google Doc in Peter's Drive. Peter owns its prose.
Claude web (through claude.ai's Google Drive integration) and Claude Code
(through its Drive connector, which acts as Peter) read it and check it
against `docs/REPORT_CLAIMS.md`. No report text is copied into the repo.

- **Changes to the doc are proposals**, as comments or a clearly marked block
  Peter accepts. Never rewrite his prose wholesale. Don't route edits through
  the server session's `gdocs.py`: it writes whole tabs as a service account.
- **Press Sync before a report round**, so Claude web checks against the
  current register.
- **Reply format for a report round** — one table, one row per claim found in
  the doc:

  | doc passage (short quote) | register row | verdict | note |
  |---|---|---|---|

  Verdict is one of `matches`, `contradicts`, `withdrawn` (the doc states an
  X-row claim), `contested` (the row's status is contested) or `no row`. A
  `no row` claim is reported, never silently accepted: either it gets a row
  with a proof pointer, or it comes out of the report.
- File the reply in `/home/opc/research/edmonton-tax-viz/` as for any round,
  then triage: register rows into `docs/REPORT_CLAIMS.md`, doc fixes into
  comments on the doc.
