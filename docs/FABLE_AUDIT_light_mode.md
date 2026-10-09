# AUDIT BRIEF — light mode, and what it left behind

**Read cold.** This is a reusable *instrument*, not a findings doc. It was written
2026-10-09 (S221, Opus 5.5) by the session family that built light mode
(S217–S220). The coverage map is `docs/AUDIT_LEDGER.md`, queue item 19. **Run 1:**
2026-10-09 (S221, Opus 5.5, same family) → `docs/FINDINGS_light_mode.md`. M5 there is moot (deck.gl 9 needs
WebGL2), and §1's negative held but its corroborating doc was stale.

⚠️ **Conflict of interest, stated first.** The builder wrote this brief. Every
light-mode gate was designed and falsified by the same model that built the
thing it guards. A cross-model run (Fable, or any model not Opus 5.5) is the
better read. Memory `measurements-that-favour-me` applies: decompose every number
that says the work is fine before you believe it.

**Scope.** All seven light-mode phases (S217–S220) plus the four S220
additions that ride on the theme: the backdrop grid, the city mask, the Dark
Reader lock and the desktop blurb box. Then the second half, which is the
reason for the run: **what the build never looked at** (§4).

**Out of scope, already tracked:** the `verify-millrates` 360 px overlap (red on
master, TODO), the phone title clip at 390 px (S220 handoff §4.4), the grid's
zoom subdivision (TODO), and the ramp-middle compression and cividis/set-aside
collision in DARK mode (`FINDINGS_colour_claims.md`, Peter's call). Mention them
only if light mode makes one worse.

---

## §0 — Ground first, in this order, then stop reading and judge

1. `docs/DECISIONS.md`: every row from 2026-09-21 to 2026-10-09 that mentions
   light, theme, ramp, grid, mask, Dark Reader or the blurb box. ⚠️ **Read the
   whole row, never a truncated `grep`.** Two earlier runs published a finding
   that a row's tail had already settled (`edmonton-audit` skill, Step 3).
2. `docs/UI.md` → `### Light mode` (build plan + phase 1–7 status), `### Blurb box (S220)`,
   `### Backdrop grid (S220)`.
3. `docs/COPY_DECISIONS.md` row B9.
4. `/home/opc/research/edmonton-tax-viz/light_mode_theme_verification_2026-09-21.md`:
   the external research and the 19-backdrop sweep the 2026-09-22 row rests on.
5. The guards, as code: `tools/profiling/verify-theme.js`, `verify-smoke.js` (A0, A9),
   `tests/test_theme_tokens.py`, `test_light_ramps.py`, `test_set_aside_colour.py`,
   `test_backdrop_grid.py`, `test_dark_reader_is_locked_out`,
   `test_the_smoke_gate_covers_both_builds`.
6. `web/index.html`: look symbols up in `docs/CODEMAP.md` first. Start with `themed`, `tc`,
   `activeRamp`, `applyTheme`, `syncThemeChrome`, `applyPalette`, `paintBackdrop`,
   `refreshLegend`, `setBlurb`, the `<head>` theme script, and the `#theme` listeners.

## §1 — The hinge fact, confirm before descending

> **Most light-mode gates check WIRING, not LEGIBILITY.** `verify-theme.js` swaps
> in a *sentinel* theme and asserts that no dark colour is still drawn. It
> proves every colour is routed through `tc()`. It cannot say whether the real
> light map reads well. Legibility was argued from stop arithmetic
> (`test_light_ramps.py`, `test_set_aside_colour.py`, `test_theme_tokens.py`) and
> from one screenshot review (phase 4: 5 desktop states + 3 phone states).

Confirm or break this before descending. Steps:

1. List every gate above.
2. Mark each one as **wiring** (is the colour routed?), **arithmetic** (do the
   numbers clear a threshold?), or **render** (did a real light page get looked
   at?).
3. Then list the views and panels that **no render-class gate and no human
   review has ever shown in light**. The views: money, ratio, change, glass,
   uses, infill, development, services with each layer, temporal, the budget,
   the Services panel, peek, guide, Sources, about.

That list is the run's map. If it is empty, §2's L6 is SOUND and §4 shrinks.

⚠️ **Claimed at write time, NOT verified: `verify-theme.js` runs in no workflow.**
`grep -rln verify-theme tests .github scripts tools` returned only the script
itself. That is the confident-negative shape. All four reversals in this ledger
had that shape (`edmonton-audit` Step 4). **Find a reader before you believe it.**
Also check whether it runs in a hook, or is named in a RUNBOOK step. If it truly
has no reader, the wiring guard is hand-run only, and every future colour edit
can ship a dark value into light.

## §2 — The decision stack (highest level first; an UNSOUND level moots everything under it)

For each level give a verdict of SOUND / CONDITIONAL / UNSOUND, the single
sharpest argument against it, and the evidence that would change the verdict.

**L0 — Should a light mode exist?** It was reopened 2026-10-08 because "readers
want it". The 2026-09-22 row had held it, and named print/export as the only
trigger. Arguments to test:
- Is the reader demand recorded anywhere? Compare its weight to the standing
  cost: every future map colour now needs two measured values and a light
  render.
- The original trigger was print, and nothing prints. There is no `@media print`
  in `styles.css` or `index.html`.

**L1 — How the theme is chosen.** The page follows the OS, a stored choice in the
Display pod beats it, the theme stays out of the share hash, and automation is
pinned to dark unless a choice is stored. Arguments to test:
- The same share link renders opposite encodings for two readers: "brighter =
  more" in dark, "darker = more" in light. Is a screenshot quoted under the
  wrong theme a real misreading risk, given that the legend travels with it?
- The webdriver pin means no automated run is ever an *OS-light* reader. The
  only exception is `verify-theme.js`'s unset-`webdriver` path. Does anything
  in CI exercise the `<head>` script's OS branch at all?

**L2 — The light ramps.** Reversed inferno capped at purple, reversed cividis,
light = low, on `#f7f7f4`. Lightness direction is inverted between themes;
hue order is not. Arguments to test:
- Is "dark = more in light, bright = more in dark" one encoding or two?
- 8.9% / 7.3% of hoods sit under 3:1 on the landing view. Re-derive that figure
  on today's data. Then check the other metrics, not just the landing one: the
  Non-residential middle ΔE of 3.5 was the only off-landing number taken.

**L3 — The 40 dependent colours.** These were measured, not mirrored.
- Re-derive the constrained ones in UI.md's phase 3 table from the shipped
  values.
- The arterial grey is noted as closest to cividis's middle. Measure it in
  light.
- The roof edge is still marked "provisional". Is it a decision or a
  leftover?

**L4 — Chrome.** Mid-grey surfaces, `--accent-ink`, and inks at ≥4.5:1, measured
on a pod composited over the backdrop. Arguments to test:
- Those ratios assume the pod sits over the BACKDROP. Pods sit over prisms. In
  light mode the prisms run down to purple `(87,16,110)`. Does a translucent pod
  (α.92) over a purple tower still give its dim inks 4.5:1? This is the same
  failure the blurb box fixed for bare text.

**L5 — Copy.** `setBlurb` swaps brighter → darker, and the guide card carries
`.more-word`. Arguments to test:
- Grep every reader-facing string for colour words: bright, dark, black, white,
  grey, glow, light, pale. Each one is a claim about a colour that may now
  differ by theme.
- Check strings OUTSIDE `setBlurb`: tooltips, the Sources and about text,
  legend captions, the Services panel, and the notebooks.

**L6 — The guards.** For each gate, ask what it can see, and use §1's three
classes. Then test whether it is wired to anything that runs (§1's caveat).
Falsify the `verify-theme` exemption list (`UNDRAWN`): can one of its three
named exemptions hide a real miss?

**L7 — The S220 additions.**
- **Grid:** is the ΔE band right on all three dark backdrops and on the light
  one?
- **Mask:** is it correct in every view, and at the city edge in 3D with pitch?
- **Dark Reader lock:** the tag covers ONE extension in ONE mode. See M1.
- **Blurb box:** it is 400 px on desktop. Measure it at 641–800 px widths,
  where the column meets the control stack.

## §3 — Method notes

- Build, serve and run as in the latest handoff's Restoration Procedure. Run
  verify scripts ALONE (memory `run-verify-scripts-alone`).
- `verify-theme` takes the site ROOT URL and runs about 6 min.
- To render light from automation, store `theme=light` before first paint, as
  `verify-smoke.js <url> light` does.
- SwiftShader renders on the CPU. Never report an absolute timing. Use on/off
  A/Bs on one page.
- This box has no web fonts (memory `oracle-box-has-no-web-fonts`). Text widths
  read 15–20% long, so blurb-box overflow findings need a font-width caveat or
  a check on a real browser.
- A finding about a colour needs the shipped value. Read it from the page with
  `page.evaluate(() => tc(X))` or from the layer attributes, never from the
  docs table.

## §4 — What the build may have missed (hypotheses, NOT findings)

Each item below was noticed while writing this brief and **none has been
reproduced**. Reproduce the symptom and measure the cause before reporting
anything (memory `todo-can-lag-executed-work`). Rank by public reach.

- **M1 — No `color-scheme` is declared anywhere.** There is no
  `<meta name="color-scheme">` and no CSS `color-scheme`. Two effects to test:
  - Native controls (the `#search` input, scrollbars in reading panels,
    checkboxes) render in the UA's default scheme. They may stay light in dark
    mode, or the reverse.
  - Browsers with forced dark (Chrome Android's "Auto Dark Mode for Web
    Contents", Samsung Internet's dark mode, Edge's force-dark) are not stopped
    by `darkreader-lock`. Without a `color-scheme` that says the page handles
    dark, they may recolour the light chrome over the WebGL map. That is the
    exact symptom the S220 lock fixed for one extension. Check each browser's
    documented opt-out before proposing a fix (memory
    `verify-relayed-external-advice`).
- **M2 — Panels that are open during a theme switch.** `applyTheme` rebuilds the
  layers, the backdrop and the legend. HTML panels that bake `tc()` colours into
  markup at render time may keep the old theme's colours until they next
  re-render: the revenue mix (~line 5625), the Uses breakdown (~6399), and the
  Services rows. Open each one, switch the theme, and read its inline
  `background:rgb(...)`. `verify-theme` checks only the legend's set-aside
  swatch (its line ~225).
- **M3 — Glow is not restored.** Entering light rewrites `state.ramp` from
  `glow` to `current`. Switching back to dark leaves the reader on Inferno. Is
  that intended (DECISIONS 2026-10-09 says only "moves a Glow reader to
  Inferno")? Check also what a stored dark choice does on the next load.
- **M4 — The linked sub-pages are light-only.** `web/verified/*.html` and
  `web/notebooks/*.html` have no `prefers-color-scheme` handling, with a
  `#ffffc0` / `#fcfcfb` background. A dark-mode reader who follows the methods
  link from the about text lands on a white page. Is that a decision, a miss,
  or not worth a change?
- **M5 — The browser floor.** The `#theme` boot path calls
  `matchMedia(...).addEventListener("change", ...)`. Older Safari (before 14)
  had only `addListener`. A throw there skips the boot lines after it, the
  label and reference listeners and `ensureReference()`. Find the project's
  stated browser floor (`docs/STACK.md`) before calling this a defect.
- **M6 — Doc drift the build left behind.**
  - `index.html`'s guide comment says the seen flag is "the app's only
    localStorage use". The theme now uses it too.
  - `docs/UI.md` → Light mode still opens with "factor the colour tunables into
    a named theme object (`THEMES.dark` / `THEMES.light`)". The phase 1 row
    REJECTED that, and the build plan's phase 1 line still names it.
  - Sweep for any others.
- **M7 — Reader-facing colour names.** Legend and blurb text that names a
  colour ("grey = set aside", "azure outline", "white" hover) may be wrong in
  one theme. This overlaps L5. Report it once.

## §5 — Reporting discipline

- Findings go in `docs/FINDINGS_light_mode.md`. One verdict line per level, then
  §4's M-items as CONFIRMED / NOT REPRODUCED / DECISION-NEEDED.
- Peter's design calls (L0, L2, M3, M4) are **reported for decision, not
  fixed**.
- ⚠️ The findings doc ends with a non-empty `What this run got wrong` section.
  This brief already carries one candidate, §1's "no CI reader" negative.
- Close the loop as the `edmonton-audit` skill's Step 5 says:
  - a ledger row in Executed audits;
  - Findings-register rows;
  - TODO items for each CONFIRMED or DECISION-NEEDED;
  - this brief's header updated with the run's output pointer.
