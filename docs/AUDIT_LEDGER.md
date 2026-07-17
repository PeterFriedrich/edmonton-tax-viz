# AUDIT LEDGER — what has been audited, when, and what came back

One row per **executed audit run**. This is the coverage map the audit docs
don't give individually: briefs (`DATA_INTEGRITY.md`, `FABLE_AUDIT_*.md`) are
reusable *instruments*, findings docs record *one run's output*, and the
`edmonton-audit` skill deliberately picks ONE target per session — so nothing
else says what has and hasn't been looked at. This does.

Rules (mirror `DECISIONS.md`): add a row when an audit **executes** (not when
a brief is written); one-line verdict + pointer, never duplicate findings or
rationale here; verdicts are **point-in-time** — a row says the target was
audited *as of that date*, not that it's still clean after later changes.
Audits are framed top-down, fundamental decisions first (the
`FABLE_AUDIT_development_lens.md` §0 rule is the house pattern).

## Executed audits

| Date | Target / scope | Instrument | Output | Verdict (one line) | Outstanding |
|---|---|---|---|---|---|
| 2026-07-01 | **Data integrity, full pass** — class→rate mapping, roll/rate vintage, join drops, aggregation grain, completeness (ranked targets T1–T7) | `docs/DATA_INTEGRITY.md` | `docs/FINDINGS_data_integrity_audit.md` | 5 bugs: Heritage Valley ~1/250th value (blocking), Lewis Farms $106M hole, no roll-year/rate guard, CI unmatched-set warning-only, latent Socrata `$limit` truncation; T1 class→rate CONFIRMED-correct | None — all five fixed & re-verified in later sessions (guard: `scripts/check_year_alignment.py`; CI assertion: `scripts/check_unmatched_names.py`; see TODO "Done") |
| 2026-07-08→09 | **Pre-launch cardinality & denominator methodology** — WEM numerator, condo denominator, ground- vs lot-acre lineage | brief inline in TODO (now its Done section) + `tools/audit_cardinality_denominators.py` | `docs/FINDINGS_denominator_cardinality.md` | First lens **immune to both bugs** structurally & empirically; WEM is one $1.285B account (premise inverted); condo inflation 0.1% citywide, dedupe already handles it; ground-acre is NOT Urban3 lineage (doc sweep clean) | None — CLOSED 2026-07-09; lot-acre lens it spawned has since shipped |
| 2026-07-09 | **Security + architecture reconciliation** (whole repo; static-Pages / build-time-Python split confirmed) | `docs/FABLE_AUDIT_BRIEF.md` | `docs/security-audit.md` "Findings — 2026-07-09" (S1–S6) | 1 Medium (CDN scripts w/o SRI) + 4 Low + 1 Informational; S1/S3/S4/S5 RESOLVED 2026-07-12 (vendored libs, `esc()` helper, SHA-pinned actions, CVE bumps) | **S2 open** — scrubbed-content-in-history, owner-only call (TODO P2.3d); S6 informational/accepted |
| 2026-07-13 (S48) | **Development + Infill lens DECISION stack** (L0 publishability → L7 code), top-down-moot rule | `docs/FABLE_AUDIT_development_lens.md` | S48 handoff: `session-summary/archive/2026-07-13.md` (verdict lines L0–L7) | **6× CONDITIONAL, 2× SOUND (L2 permits, L7 code), 0× UNSOUND**; one decision REOPENED (Infill single-scale saturation) → fixed 2026-07-14 (per-arm p95 clamp, `t = ±0.4`; DECISIONS.md) | Its 6 CONDITIONALs → dispositioned by the Round-2 delta row below |
| 2026-07-16 (S56) | **Dev+Infill ROUND-2 delta** — dispositions S48's CONDITIONALs + audits post-S48 changes (per-arm impl, window toggle, dev-grid) | `docs/FABLE_AUDIT_devinfill_round2.md` | S56 handoff: `session-summary/2026-07-16.md` §2.D (disposition lines D1–D6 + proposed caveat texts) | **0 DEGRADED.** D1 CLOSED (L4→SOUND, per-arm fix holds on refreshed data), D2 CLOSED (denominator bias immaterial: Spearman ρ 0.9965, 5 band-edge flips only), D3 evidence delivered → recommend disclose-only (suites = 0.9% of Lens A units, zero hoods flip teal), D6 SOUND (WATCH: orange clamp = p95 of a ~105-member arm) | D4 grammar + D5(i)/(ii) doc debt → the post-audit **copy PR** (proposed texts in the S56 handoff §2.D, pending Peter's D4-grammar / D3-fork picks) |

## Never audited (candidates, roughly ranked)

Surfaces no audit run has covered. Listing here is inventory, not commitment.

1. **Services/cost lens decision stack** (roads, fire, stormwater, transit —
   `docs/SPEC_services.md`): the cost side has had build-time verification and
   the S55 svc_cost honesty guard, but never a top-down decision audit like
   S48 gave the development lenses. Biggest unaudited public claim surface.
2. **Residential-revenue metric + Glass grid columns** (shipped 2026-07-16/17,
   post-S48): pipeline verified green at build; the *decisions* (class
   composition, MA DERELICT exclusion, real-zero convention) unaudited. The
   Round-2 brief's D6 covers the dev-grid, not these.
3. **Debt lens data series** (`data/fir_debt_series.json`): anchor
   cross-checks were done at build (S~53); no independent pass. Lens itself
   still unbuilt (interaction prereq), so low urgency.
4. **Refresh workflow end-to-end failure modes** (`refresh.yml` +
   `docs/RUNBOOK.md`): the security pass covered its supply chain; the
   *operational* logic (HOLD paths, banner states, January year-roll) has a
   runbook but no adversarial audit.
5. **Data-integrity RE-RUN** on current data: the 2026-07-01 pass predates the
   lot-acre columns, res_levy decomposition, value/res grids, and services
   join — `docs/DATA_INTEGRITY.md` §joints may itself need updating first.
