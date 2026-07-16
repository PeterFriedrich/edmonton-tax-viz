# Fable 5 Brief — Development & Infill Lenses, ROUND-2 Delta Audit

Read this in full before opening any code. This is **not a re-run** of
`docs/FABLE_AUDIT_development_lens.md` — that audit EXECUTED in S48
(2026-07-13; handoff in `session-summary/archive/2026-07-13.md`, "SESSION 48"):
**6× CONDITIONAL, 2× SOUND (L2 permits, L7 code), 0× UNSOUND**, one decision
reopened and since fixed. Its verdicts are recorded; do not re-derive them.
Your job is the **delta**: (a) verify the fix that was shipped in response,
(b) audit what changed in these lenses since S48 that no audit has seen, and
(c) **disposition every outstanding CONDITIONAL's condition** — met, still
open, or unmeetable.

This session uses Fable usage that counts against plan limits at a higher rate
than Opus — don't spend it reconstructing context that is already written down.

## 0. The one rule (adapted for a round-2)

S48's rule was top-down-moot. Round-2's rule is **disposition, not
re-litigation**: each item below carries its S48 verdict and its stated
condition. For each, return exactly one of:
- **CLOSED** — the condition is now met (say what met it, with file/line);
- **STILL OPEN** — say precisely what is missing and the smallest action that
  would close it;
- **DEGRADED** — the condition cannot be met, or new evidence breaks it; the
  S48 verdict falls to UNSOUND and you say what that moots.

Do not reopen a level whose verdict was SOUND unless the post-S48 changes
touched it (D6 tells you which did). A finding that degrades a level is worth
more than ten that polish one — but a false degradation wastes an owner
decision; check the S48 numbers before contradicting them.

## 1. Ground yourself first (in this order, then stop reading and start judging)

1. `session-summary/archive/2026-07-13.md` — the S48 handoff ("SESSION 48"
   block, verdict lines L0–L7 + the empirical numbers). This is the baseline.
2. `docs/FABLE_AUDIT_development_lens.md` — the original brief (for what each
   level means; do NOT re-execute it).
3. `docs/DECISIONS.md` — the 2026-07-13 Infill line, the 2026-07-14 REOPENED
   line, and the 2026-07-14 per-arm close (`t = ±0.4`).
4. `docs/FABLE_infill_perarm_scaling.md` + `session-summary/2026-07-14.md`
   (S49/S50) — the fix implementation record.
5. `docs/SPEC_development.md` Lens B — the "⚠️ REOPENED" block and its close.

Then confirm one thing back before proceeding, with the file/line that proves
it: **the shipped Infill view now clamps each arm at its own p95**
(`web/index.html` `infillStats` — `clampPos`/`clampNeg`, ~line 1350) **and the
tooltip verdict branches on clamped `t`, not raw score.** That is the hinge of
D1; if it is not true on current master, stop and report before anything else.

## 2. The delta stack (work in this order)

### D1 — Verify the L4 fix holds on CURRENT data (was L4: CONDITIONAL→fix shipped).
S48's numbers were computed on the 2026-07-13 geojson; the fix's acceptance
numbers (clampPos ≈ 1.49, clampNeg ≈ 4.34, teal saturations 0→2, orange 18→6,
median t ≈ 0.29 vs cut ±0.4) on 2026-07-14 data. The weekly refresh has run
since. **Independently recompute** — from the live
`web/data/neighbourhood_value_per_acre.geojson`, not the app's own functions —
per-arm p95s, saturation counts per arm, and the median-t-to-cut gap, for BOTH
window variants (units×5yr and units×3yr; the toggle re-scores the population).
- Does the teal endpoint stay reachable on refreshed data, or was 2026-07-14
  a lucky vintage?
- Is the ±0.4 cut still clear of the median on both windows, or has the
  coin-flip S48 flagged crept back?
- Verdict: CLOSED flips L4 to SOUND; a regression here is DEGRADED and moots
  D4/D5 polish until re-fixed.

### D2 — The L1 flip test (was L1: CONDITIONAL; test proposed, never run).
S48's sharpest unresolved argument: **FAR and activity use different
denominators** (FAR ÷ deduped private lot acres — parks/ravines absent from
the roll don't dilute it; activity ÷ boundary acres — ravines fully dilute
it), so a half-ravine hood is biased teal by boundary geometry alone, and
z-scoring hides the unit mismatch. The proposed test: **recompute the activity
term per `lot_acres_eligible`** (column already in the slim geojson) and
compare — Spearman rank correlation of the resulting scores, top/bottom-15
overlap on each arm, and which specific hoods change verdict band at
`t = ±0.4`. High parcel-land hoods should barely move; the interesting set is
hoods below ~50% `parcel_frac`.
- If ranks are stable: CLOSED with the evidence documented (propose where —
  SPEC_development Lens B caveats).
- If hoods flip verdict bands: STILL OPEN or DEGRADED — say whether the fix is
  switching the denominator (pipeline change) or disclosing the bias (copy
  change), and which you'd recommend.

### D3 — The L6 suite-conversion disclosure (was L6: CONDITIONAL; Peter's fork, undecided).
`(07) Add Suites to Single Dwelling` / `(08) Add Suites to Multi-Dwelling` /
`(09) Convert Non-Res to Residential` are in `KNOWN_WORK_TYPES` but outside
`NEW_WORK_TYPES` (`src/load_permits.py:48-63`) — deliberate for Lens A
("units added by new construction"), but Lens B's activity term IS the Lens A
column, so a hood densifying via secondary suites reads "quiet" → teal on the
very lens meant to surface infill. **Quantify it**: in-window (07)/(08)/(09)
row and `units_added` counts from `data/raw/building_permits.csv`, and which
hoods carry them. Then give Peter decision-grade evidence for the fork:
(i) disclose in the Infill blurb only, (ii) add suite units to Lens B's
activity term (NOT Lens A's), or (iii) immaterial — document and close.
Recommend one, with the numbers.

### D4 — Verdict grammar in t-space (was L0: CONDITIONAL; residual owner call).
The tooltip still pronounces per-hood verdicts ("Suitable but quiet — infill
opportunity") — S50 moved the *cut-points* to t-space but did not soften the
*grammar*. Read the current strings (`web/index.html`, tooltip verdict branch
near `infillT`). Is the recommendation-grammar risk S48 flagged still live now
that the thresholds are principled? Propose exact replacement copy if so —
this is a copy PR, not a design PR. The residual "is being cited as
build-here advice an acceptable failure mode" remains Peter's call; frame it,
don't decide it.

### D5 — The L5 documentation debt (was L5: CONDITIONAL — defensible but undocumented).
Three specific gaps S48 named: (i) keeping 132 teal-barred non-res hoods in
the z-population compresses visible-teal contrast ~2× (far std 0.249 vs 0.120
res-only) — defensible (ranks stable 14/15) but written down nowhere;
(ii) the `frac_residential ≥ 0.50` cliff (`src/load_zoning.py:26`) is
invisible to readers; (iii) grey carries 3 meanings (set-aside / no-data /
non-res-suppressed). Check whether ANY of this reached reader-facing or
maintainer-facing text since (UI.md, SPEC, blurb). For each: CLOSED / STILL
OPEN + the one-paragraph text you'd add and where it goes.

### D6 — Post-S48 changes no audit has seen (new material — brief top-down pass).
Apply S48's stack-thinking (decision before code) to what shipped after the
audit snapshot, but keep it proportionate — these are follow-on decisions, not
new lens families:
- **The per-arm implementation itself** (`infillStats`/`infillT`,
  `web/index.html` ~1334-1380): p95-of-arm on small-n arms (the positive arm
  had ~253 members, the negative ~105 — is p95 of 105 stable release-to-
  release?), the `|| 1` degenerate-arm fallback, cache invalidation across the
  window toggle.
- **The 5yr/3yr window toggle** (DECISIONS 2026-07-13): both windows re-score
  the same population — is the toggle disclosed as a re-scoring (colours
  change meaning), or could a reader think it's a filter?
- **The Development-view 100 m detail grid** (`dev_grid.json`): does the
  parcel-ish resolution undercut the L1 aggregation defence ("we only publish
  at hood level"), or is it exempt because it shows raw activity, not
  suitability verdicts?
Verdict per item: SOUND / CONDITIONAL / UNSOUND, one sharpest argument each.

## 3. Reporting discipline

- Before any finding, point to the file/line/decision it challenges; if you
  cannot verify something this session, say so — do not flag it as confirmed.
- **Do not narrate your reasoning process into the output.** Verdict, argument,
  evidence. (Also avoids the reasoning-extraction reroute to Opus.)
- No subagents — single session.
- Do **not** edit `docs/SPEC_development.md` or `docs/DECISIONS.md`; log
  findings, propose changes. D2/D3/D4/D5 may each end in a *proposed* text or
  code change — write the proposal into the handoff, not the repo.
- Empirical work happens on the LIVE geojson + raw permits CSV via small
  python snippets (`.venv/bin/python`); never `Read` the raw files
  (`docs/TOKEN_EFFICIENCY.md`).
- Pause and ask only for a judgment call the owner alone can make (the D3 fork
  qualifies if the numbers are material). Don't end on a vague "let me know."

## 4. Before this session ends

Run `/handoff`. The handoff must include:
- A disposition line per item D1–D6: CLOSED / STILL OPEN / DEGRADED (+ the
  S48 level it descends from) and the one-line evidence.
- Any DEGRADED item: which S48 verdict falls, what it moots, and the smallest
  re-fix.
- The D3 numbers and your recommended fork option, framed for Peter.
- Anything flagged but not verifiable this session, so it isn't lost.
