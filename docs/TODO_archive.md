# TODO — archive of CLOSED items

Closed work moved out of `TODO.md` so the file that is read at the start of **every** session carries only live work. **Nothing here is a to-do.**

`TODO.md`'s `## Done` section keeps a one-line entry for each of these, so the *never redo a closed item without asking* rule still works by grepping there; this file holds the reasoning behind each one.

Items are verbatim as they were closed, newest-moved first in the order they appeared in `TODO.md`. Line numbers and "next up" markers inside them are historical — do not act on them.

---

- [x] **Possibly an `AGENTS.md` for the repo**, so tools other than Claude Code
  get the same instructions. Decide whether it is a pointer or symlink to
  `CLAUDE.md` or a separate file. A copy would drift, and `CLAUDE.md` changes
  weekly. Check what `cc-data-project-template` does and keep the two consistent.
  **CLOSED 2026-09-25 (S196), no file:** Peter's call. An agent from another tool finds `CLAUDE.md` by looking around the repo, the repo takes no outside contributions, and much of `CLAUDE.md` is Claude-Code-specific anyway. Revisit in `cc-data-project-template` if anywhere.

- [x] **SERVICES' HOVER STILL TEASES A CHART ITS PANEL DOES NOT OPEN** — CLOSED 2026-09-24 (S194): Peter picked `click to compare with service costs`; Ratio lost its fallback history panel and 44 Development hoods stopped falling through to it (`verify-hoodmode.js` sweep). **Was:** the same
  defect fixed on the revenue cuts 2026-08-16, left live because the replacement
  copy is Peter's call.** In Services (with the cost columns shipped) the hover
  plots the **assessment-share sparkline** and says **`click to pin`**, while the
  click opens the **cost-against-revenue panel** (`servicePanelFor`, 2026-08-10).
  Measured, not inferred: `hoodPanelLens()` is `!serviceLens() || state.hasRoadsLife`,
  so the teaser is appended there like anywhere else. ⚠️ **Predicate name
  corrected 2026-09-16 (S166) — it read `state.hasSvcCost` until 2026-09-05,
  when the retired roads+fire composite took that flag with it; the gate had to
  name a column the PUBLIC build actually shows. The DEFECT is unchanged and
  still live — `web/index.html`'s own comment above `tooltipFor` says so:
  *"SERVICES IS NOT YET EXCEPTED though it should be … the hover still plots
  history under a click that opens costs."*
  - ⚠️ **`docs/CONTROLS_MATRIX.md` asserted the OPPOSITE** ("the sparkline is
    not [offered in Services]") from 2026-08-10 until this was measured on
    2026-08-16. The cell is corrected; the point is that the claim sat unchecked
    for six days because nobody hovered a Services hood.
  - **The fix is one predicate** — the revenue branch in `tooltipFor` already
    demonstrates it; Services needs `servicePanelFor(p)` treated the same way.
  - **What is NOT decided is the invite's wording.** The revenue cuts say
    `click for the revenue mix`; Services would need its own line (`click for the
    cost breakdown`?), and naming a "cost" in one phrase brushes the locked rule
    that ⚠️ **there is no single cost number and there cannot be** — two bases,
    ~10.8× apart, deliberately not summed (`data/DATA.md` §13, `SPEC_services.md`).
    A hint that implies one total would be the same class of error as the chart.
  - Precedent + full reasoning: `docs/DECISIONS.md` 2026-08-16 (the sparkline
    row), `docs/SPEC_temporal.md` §2 (the amended row).


### `verify-services-panel.js` and `verify-ratio-denom.js` are red on the public build (FOUND 2026-09-24 S193)

Four checks fail on master as well as on branches: *"transit / bike / transitcost /
bikecost: the panel opens and is not empty — 0 rows"*. Those services are
full-only (`SERVICES[*].pub` false), so the public build has no rows to show. It
is the missing build gate `tools/profiling/README.md` convention 1 describes.
The script is not in CI, which is why nobody saw it. Fix: gate those four on
`FULL_BUILD` and print `PARTIAL`, the way `verify-transport-cost.js` does.

`verify-ratio-denom.js` has the same defect: *"ratio: picker shown"* fails on
the public build, where the denominator picker is full-only by design
(`ratioDenomShow` requires `FULL_BUILD`). It passes 42/42 on the full build.

**CLOSED 2026-09-24 (S194):** both scripts read `FULL_BUILD`. `verify-services-panel.js` skips §1–3 on a public URL (its §4 already covers the three public layers) and prints `PARTIAL`. `verify-ratio-denom.js` asserts the picker matches the build in both directions, skips the fire §4–9 on public, and prints `COMPLETE`/`PARTIAL`. The public run had been passing ~20 fire checks by JS-clicking the hidden picker. Falsified: ungating `ratioDenomShow` turns the public run red.
