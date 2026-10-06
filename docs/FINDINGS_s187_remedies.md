# Findings — remedies from the S187–S191 audits, non-roads half (queue item 13)

**Run:** 2026-10-05, S215, Opus 5.5, `xhigh`. ⚠️ Same model family as the
remedies' author.
**Target:** `docs/AUDIT_LEDGER.md` queue item 13's open half: #543 (readout
floors, `FINDINGS_readout_floors.md` fixes 1–4), #544 (residential share
`>99%`, COPY_DECISIONS S10), #547 + #551 (evidence recheck F1–F8). The roads
half (#535, #548) ran 2026-09-28 (S202).
**Question:** did each remedy land as specified, does it hold on the data served
now (CI refresh 2026-09-28), and can its guard fail on a defect other than the
one it was written for?
**Instrument:**
- Served geojson.
- Two mutants of a fresh `build_site.py` tree:
  - **M1**: #543's ratio fix reverted, `money0` → `"$" + Math.round(…)` in
    `viewTooltip`'s band;
  - **M2**: the same open-coding moved to the Services **panel**
    (`renderServiceCost`'s cost row).
- `verify-smoke.js` on the full build for the control and each mutant, run
  alone.
- A headless render of M2's panel.
- `scripts/recheck_evidence_notebooks.py`, cold, all 7 notebooks, then
  `--only` the one that did not run.

## Verdicts

| Remedy | Verdict | Evidence |
|---|---|---|
| #544 `fmtResShare` `>99%` | **SOUND** | 6 hoods sit in [0.995, 1) and print `>99%`. No hood is exactly 1.0, so `100%` never prints. ANTHONY HENDAY HORSE HILL (nonres 0.0, share 0.9966) is correct at `>99%`: the remainder is farmland/other, not non-residential. Values are served to 6 significant figures, so the 0.995 boundary is not at risk. |
| #543 fix 2 (`fmtBike` floor) | **SOUND, and it arrived in time** | S188 predicted KING EDWARD PARK would reach 0.0046 m/acre at the 09-28 refresh. It did (0.00460044 served) and renders `<0.01`, not `0.00`. |
| #543 fixes 1, 3, 4 (smoke `.html`, ratio sites, zero-token sweep) | **SOUND for tooltips; BLIND for panels — F1** | Control: green. **M1 → red**: `C-ratio / fire: … UNIVERSITY OF ALBERTA FARM: $0` (full build; the public road denominator stays green because that hood's band does not render there). **M2 → green**, while rendering a public `$0` (below). |
| #547 / #551 evidence recheck | **SOUND, live** | The 5 evidence notebooks hold 9 + 6 + 12 + 5 + 5 = 37; `roads_operating_rate` 22. `roads_lifecycle_rate` came back **❓ data shape** (`EmptyDataError`: `budget.edmonton.ca/api/capital_budget.csv` answered 200 with an empty body). Re-run alone: **45 held**, so the source was transient. The ❓ did what #547 F2 built it for: it named the kind and did not fold into ✅. Total 104, matching #551's count. |

## F1 — the zero-token sweep reads tooltips only; the pinned panels are ungated

`verify-smoke.js` §C renders `viewTooltip` for every hood and flags a
zero-looking token that survives re-rendering with true zeros set to NaN. That
check is good: it caught M1 by name. But the pinned panels — `renderServiceCost`,
`renderRatioCost`, `renderRevenueMix`, `renderDevHistory` — are separate render
sites with their own formatting. The only panel either CI gate opens is B5's: the
assessment-history chart for the first hood, whose plotted points it counts. No
gate reads a panel's text.

**M2, measured:** the public Services panel, roads-cost driver, ANTHONY HENDAY
ENERGY PARK (operating cost $0.436/acre/yr) renders

> Roads | **$0 / acre / yr** | 398th highest of 406 neighbourhoods

and the full-build smoke run reports every C check PASS. HERITAGE VALLEY AREA
($0.450) is the second public hood below $0.50. Today the panel calls `money0`,
so there is **no live defect**. The gap is that the sweep built to catch
open-coded sites (`FINDINGS_readout_floors.md` §4) cannot see this class of
site. The panels are where #580 just added ranked dollars, and where the next
open-coded formatter is most likely to appear.

**Class:** `guard-blind`. **Reach:** latent.
**✅ Built 2026-10-05 (S216):** checks `C-<state>: no zero-looking panel figure
over a nonzero value` and `… no NaN/undefined in any hood's panel`. Renderers are
called directly per hood (every offered Services driver), not via `openTemporal`;
cost +3 s per build (13–14 s → 16–17 s, measured alone). M2 (Services), an
open-coded Ratio bar and an open-coded city-share line each fail only their own
panel check, on both builds.
**Remedy (CI-adjacent → Peter):** extend §C to call `openTemporal(name)` per
hood under each view, and run the same NaN-substitution zero-token scan on
`#temporal-read`. The cost is one more render per hood per view. Measure that
before deciding; the refresh gate's runtime is watched
(`FINDINGS_verify_runtime.md`).

## Observations

- **O1 — a transient empty 200 will produce a ❓ in the 10-15 issue if it
  recurs.** The harness has no retry. A ❓ is louder than a ⚠️ by design, so one
  flaky fetch reads like a dead source. A single retry of ❓ notebooks before
  reporting would cut that noise. A retry cannot turn a real ⚠️ into ✅, because
  it runs only on notebooks that verified nothing. CI behaviour, so it is
  Peter's.
- **O2 — two empty upstream bodies on one day.** `f2sy-bth7` reloaded with 0
  rows (`DATA_ISSUES.md` §8) and budget.edmonton.ca answered once with an empty
  CSV. For the digest's capital-budget check, an empty body raises → UNKNOWN
  (correct), but a **header-only** body fingerprints as 0 rows → **ACTION
  "Upstream moved: 1,884 → 0 rows"** (`vintage_report._capital_fingerprint`,
  tested directly). That is a loud false alarm, not a silent one. Input to queue
  item 18.

## What this run got wrong

- **I read the recheck's first ❓ as a broken source** and went looking for a
  moved URL. The endpoint served 272 KB when probed, and the notebook passed
  alone. Had I written it up from the first run, it would have been a false
  "source dead" finding. That is the noise O1 describes, and the harness's own
  ❓ text warns against exactly that reading.
- **My first draft of F1 said "nothing in either CI gate opens" a panel.**
  `verify-smoke.js` B5 calls `openTemporal` on one hood, to count the history
  chart's points. The true statement is narrower: no gate reads a panel's
  **text**. That was a confident negative, and grepping for the reader found it.
- **I ran the mutants on the full build only.** Under M1 the road-denominator
  `C-ratio` stayed green there too, and that is the only ratio denominator the
  public build has. So the public build's own smoke run would not catch M1. The
  full-build run in the same CI step does.
