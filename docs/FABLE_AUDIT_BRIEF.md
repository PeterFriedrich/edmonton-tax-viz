# Fable 5 Session Brief — Property Tax Viz Audit

Read this in full before touching any code. This session uses Fable 5 usage that
counts against plan limits at a higher rate than Opus — don't spend it re-deriving
context that's already written down in the repo.

## 0. Ground yourself first (do this before anything else)

Read, in order: `CLAUDE.md`, `docs/SPEC_phase1.md`, `docs/ARCHITECTURE.md`,
`docs/security-audit.md`, `CONTRIBUTING.md`.

Then confirm one specific thing and state it back before proceeding:
**Where does the Python actually execute?** GitHub Pages only serves static
files — it cannot run a Python process. Check whether "backend" here means:
- (a) Python runs at build time (CI, local script, GitHub Action) to produce
  static data files that the deployed site then serves as-is, or
- (b) Python runs as a live service elsewhere (separate host, serverless
  function, etc.) that the static frontend calls over the network.

These have almost entirely different attack surfaces. Say which one this repo
actually is, with the file/workflow that proves it, before starting the audit.
If it's ambiguous, say so explicitly rather than assuming.

## 1. Scope for this session

Two tasks, in order:

1. **Security audit pass** — full read of the repo against `docs/security-audit.md`'s
   existing checklist. Update that file with findings; don't create a parallel doc.
2. **Architecture reconciliation** — check `docs/ARCHITECTURE.md` (living doc)
   against what's actually implemented. Flag drift; don't silently fix it.

Out of scope this session: refactoring, style cleanup, new features. If you find
something that clearly needs fixing, log it as a finding with a suggested fix —
don't make the change. `docs/SPEC_phase1.md` is frozen; don't propose edits to it, only
note if reality has diverged from it.

## 2. What actually matters for this repo

Given the static-frontend / Python-processing split, prioritize:

- **If (a) build-time**: are there any credentials, API keys, or internal-only
  fields in the generated static output? Anything committed to the repo or
  shipped to the deployed site that shouldn't be public (this is a public repo
  with a public site — assume everything in the output is world-readable).
- **If (b) live service**: CORS configuration, auth on any endpoint, rate
  limiting, what happens if the static frontend's expected request shape is
  bypassed and the endpoint is hit directly.
- **Either way**: data integrity of the property tax source data — is
  provenance documented, is there validation on ingest, could a bad source
  file silently corrupt what gets published as fact about people's tax bills.
  This is public-facing civic data; wrong numbers are a real-world harm, not
  just a bug.
- Anything in `.claude/`, CLAUDE.md, or committed config that leaks paths,
  tokens, or internal infrastructure details inappropriate for a public repo
  with expected contributors/forks.

## 3. Reporting discipline

- Before writing any finding, point to the actual file/line/output that
  supports it. If something can't be verified this session, say so explicitly
  rather than flagging it as confirmed.
- Don't narrate your own reasoning process into the output — report findings
  and evidence, not a transcript of how you thought about them. (This also
  avoids tripping Fable's reasoning-extraction classifier, which can silently
  reroute the session to Opus 4.8 mid-task.)
- No subagents are in use in this workflow — do this as a single session.
- Pause and ask only for things that are genuinely irreversible or need a
  judgment call only the project owner can make. Don't end a turn on a vague
  "let me know if you'd like me to continue."

## 4. Before this session ends

Run `/handoff` per the existing skill. The handoff should include, specifically:
- The build-time-vs-live-service answer from step 0, with evidence
- Every finding added to `docs/security-audit.md`, by severity
- Every drift item added to `docs/ARCHITECTURE.md` (or a note that none was found)
- Anything flagged but not verifiable this session, so it isn't lost
