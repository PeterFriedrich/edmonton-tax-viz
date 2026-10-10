# Findings — light mode and what it left behind (queue item 19)

**Run:** 2026-10-09, S221, Opus 5.5, `xhigh`. **Brief:** `docs/FABLE_AUDIT_light_mode.md`.
⚠️ **The builder's model family audited its own build.** A cross-model read is still
worth having, aimed first at L4 and L6 below.

**Build audited:** master `a8e948b`. It was built locally with `build_site.py`.
**Data:** the 2026-10-08 data in `web/data`.

**Instruments.** All of these are scratch scripts and none is kept. Each was run alone.
- **Light renders:**
  - every view and panel at 1440×900 and 390×844 (63 PNGs);
  - a second pass for the states the public build gates out.
- **Tooltip and panel probes:** the tooltip's computed style; the revenue-mix
  panel in both themes.
- **Theme-switch diff:** every inline `rgb()` before and after a switch, plus a
  detector for colours that belong to the other theme. The control is a run with
  no switch.
- **Contrast arithmetic:** reuses `tests/test_light_ramps.py`'s parser and maths.
  - **Control:** it reproduces S218's 14.5% / 8.9% / 7.3% exactly.
- **Three single-colour mutants:** each is run through `pytest` and the deploy's
  light `verify-smoke.js`, plus `verify-theme.js` for one of them.
- **Chromium auto-dark emulation:**
  - `--enable-features=WebContentsForceDark` with
    `--blink-settings=forceDarkModeEnabled=true`;
  - run on three builds: as shipped, with a meta tag, and with per-theme CSS.
- **Print path:** `page.pdf()` in both themes.
- **Width sweep:** 641–1024 px, run on master and on the pre-#698 build.

## §1 — The hinge: which gates render light

| Gate | Class | Runs in |
|---|---|---|
| `verify-theme.js` (sentinel probe, reader paths) | wiring | by hand only |
| `test_light_ramps.py`, `test_set_aside_colour.py`, `test_backdrop_grid.py` | arithmetic | pytest (CI) |
| `test_theme_tokens.py` (`test_light_inks_are_legible` …) | arithmetic, **over the backdrop only** | pytest (CI) |
| `verify-smoke.js <url> light` (A0 + the invariants) | loads light; checks no garbage and no exceptions | `deploy.yml`, both builds |
| Phase 4 screenshot review | render, by eye | once, S219: 5 desktop + 3 phone states |

**Confirmed: no gate renders light and looks at it.**
- The S219 review covered 8 states.
- It covered no hover tooltip.
- It covered no width between 641 and 1280 px.

The brief's negative also held: `verify-theme.js` runs in no workflow. That is the
documented norm for most of the verify tier, not a light-mode lapse. CI now runs 3 of
the 44 scripts: smoke, blurbs and url-state. F10 covers the stale doc that says
otherwise.

## §2 — Verdicts by level

| Level | Verdict | Sharpest argument against | What would change it |
|---|---|---|---|
| L0: should light mode exist | **SOUND** | The 2026-09-22 row named print as the only trigger, and print is still unserved (F8): the legend key prints blank. Light mode shipped for a different reason (readers asked), so this does not unseat it. | Evidence that readers do not use it |
| L1: how the theme is chosen | **SOUND**, one hole (F6) | No CI run ever loads the `<head>` script's OS branch: the smoke stores `light`. A browser's own forced dark repaints a stored-light page when the OS is dark (F6). | — |
| L2: the light ramps | **SOUND** | — | A view where light is worse than dark. None was found (table below). |
| L3: the 40 dependent colours | **CONDITIONAL** | They were measured against the map backdrop and the ramps. The ones that also render in HTML panels were never measured against a panel, and S219's mid-grey surfaces lowered them further (F5). | — |
| L4: chrome | **UNSOUND as claimed** | DECISIONS 2026-10-09 says every reading ink clears 4.5:1 on every surface. The hover tooltip never uses those surfaces and renders at 1.2:1 (F1). The token values themselves are sound. | — |
| L5: copy | **SOUND** | — | — |
| L6: the guards | **CONDITIONAL** | The guards are wiring checks plus arithmetic over stand-ins. F1 passed all of them, and so did a missing light value that does not crash (F4). | A gate that renders light and reads it |
| L7: S220 additions | grid and mask **SOUND**; Dark Reader lock **SOUND, partial** (F6); blurb box **regressed narrow widths** (F2) | — | — |

**L2, measured.** These are shares under 3:1 against what the colour sits on, flat
colour.

| View | Dark `current` | Light `current` | Light `cividis` |
|---|---|---|---|
| Landing hoods vs backdrop (control) | 14.5% | 8.9% | 7.3% |
| Services roads vs backdrop, by length | 21.7% | 19.1% | 16.5% |
| Development 100 m cells vs plane | 95.1% | 80.6% | 70.4% |

Light is no worse than dark in any measured view.
- The Development row is a flat-colour proxy for lit, extruded spikes. Read it as a
  comparison between themes, not as a defect.
- At first sight the Services screenshot looked worse in light. The table says
  otherwise.

**L5.** Checked:
- No public blurb says "bright" in light.
- The sub-pages (`verified/`, `notebooks/`) carry no "brighter" or "darker" in
  their visible text.
- Colour names (teal, orange, azure, grey) mean the same in both themes.

One stale string, F12, predates light mode.

## §3 — Findings, most severe first

**F1 — The hover tooltip is illegible in light mode. HIGH; public.**
- **What happens:** deck.gl writes its default tooltip style inline:
  `background-color: rgb(41,50,60); color: rgb(160,167,180); padding: 10px`.
  Inline style beats `.tip { background: var(--read-bg); color: var(--ink-tip) }`.
  The project's tooltip surface has therefore never applied, in either theme,
  since the rule landed on 2026-06-25.
- **In dark it passed by accident:** the theme's light inks happen to read on
  deck's slate. The name is 9.1:1, the muted lines 6.6:1, the value 5.4:1.
- **In light:** the name (`--accent-ink` `#8a5a00`) is **2.2:1**. The muted lines
  (`--ink-2-bright` `#3c3c4c`) are **1.2:1**: "61% of revenue is residential",
  "51.9 road m / acre" and "click for the revenue mix" all vanish. The intended
  pairing, `--ink-tip` on `--read-bg`, would be 14.6:1.
- **Reach:** hover is the desktop readout in every view ("Readout: popup").
- **Why every gate missed it:** `test_light_inks_are_legible` checks
  `--ink-tip`/`--read-bg`, a token pair the tooltip does not render with (a proxy
  guard). `verify-theme` checks layer colours, not DOM. The S219 review had no
  tooltip in it.
- **Fix:** have every `viewTooltip` return also pass deck a `style` that
  overrides the defaults, for example
  `style: { backgroundColor: "var(--read-bg)", color: "var(--ink-tip)", padding: "6px 9px" }`.
  Or use `!important` on `.tip`.
  - **Then add a render check:** hover a hood in light and assert the tooltip's
    computed background is not `rgb(41, 50, 60)`.

**F2 — From 641 to ~930 px wide, the top-left column covers the view buttons; #698 widened the band. MEDIUM; public.**

The top-left column is the title box, the search and `?` buttons, and the mill rates.

Measured rects (light, 800 px high):

| Width | Master: overlaps | Pre-#698: overlaps |
|---|---|---|
| 641 | title, mill rates, search, `?` × views / toggle / Options | same |
| 720 | same | title × views and Options; search, `?` × views |
| 800 | **title × views, title and mill rates × Options**, search, `?` × views | search, `?` × views |
| 900 | **`?` × views** | none |
| 1024 | none | none |

- **On screen at 800 px:** the title box sits over the Money and Development
  buttons.
- **Who hits it:** portrait tablets (768–834) and small laptop windows. No
  layout exists between the phone block (≤640) and full desktop.
- **Old, then extended:** the collision below ~860 px predates S220. #698 moved
  its top edge up by about 40 px and made the box opaque over the buttons.
- **Fix:** a layout decision (where the column goes between 641 and ~1000), so
  Peter's call.

**F3 — On phones, the "Beta build" badge covers the legend's last line and the bottom sheet's last lines. MEDIUM; public; pre-existing; both themes.**
- **What it is:** `build_site.py` injects `#wip-badge` with `position:fixed;
  left:50%; bottom:10px; z-index:9999`. Its comment says bottom-centre "keeps
  clear of the legend (bottom-left)".
- **At 390 px:** the badge covers the legend's set-aside or arterial line in
  every view, and the last two lines of the revenue-mix sheet.
- **Confirmed in a dark render too.** It also shows at 800 px desktop.
- ⚠️ This box has no web fonts, and text measures 15–20% wide here. A real phone
  wraps less, but the badge and the legend's last line share the same bottom band
  either way.
- **Fix:** move the badge on narrow screens, or shrink it. Then correct the
  comment.

**F4 — A colour with no light value ships when its `undefined` does not crash. MEDIUM; latent; guard-blind.**

One mutant per colour, each declared `themed(dark)` with no light value:

| Mutant | pytest (1132) | deploy light smoke | how it was caught |
|---|---|---|---|
| `RIVER_COLOR` (constant accessor) | pass | **FAIL A4** | deck console error |
| `ARTERIAL_COLOR` (`.slice` in the legend) | pass | **FAIL A8** | page exception |
| `HOVER_COLOR` (`highlightColor` prop) | pass | **pass** | — |
| `HOVER_COLOR`, `verify-theme.js` (hand-run) | — | **112/112 pass** | — |

- **The catch is incidental:** the first two fail only because `undefined`
  crashes something. The third ships an undefined hover colour in light (deck
  falls back to its own default; not inspected) with every gate green, the
  hand-run `verify-theme` included. Its colour checks run under a sentinel
  theme, which tests routing, not the `light` values.
- **Fix:** make `themed()` throw when `light` is missing. Every such colour then
  crashes at load, and the light and dark smoke both go red. A pytest that every
  `themed(` call has two array arguments would catch it before merge.

**F5 — The revenue-mix greys almost vanish on the light reading panel. LOW–MEDIUM; public.**

Swatch and bar against `--read-bg` composited over the backdrop:

| Swatch | Dark | Light | How common |
|---|---|---|---|
| "Outside any zone" (`UNZONED_COLOR`) | 2.1:1 | **1.3:1** | at most 1.3% of any hood's tax |
| "Future / rural" (= set-aside) | 3.7:1 | **1.7:1** | 41 hoods hold ≥10% of their tax here; one holds 100% |
| Residential | — | 2.5:1 | — |
| Industrial | — | 2.6:1 | — |

- **Confirmed on render:** Anthony Henday Mistatim and Edmonton South Central,
  both themes.
- The text labels still carry the meaning.
- **Never checked:** `UNZONED_COLOR` is in `verify-theme`'s `UNDRAWN` exemption
  ("HTML panel only"), and in no phase-3 table.
- **Fix:** a design call. Options: a 1 px `--border-strong` outline on swatches
  and bar segments, or panel-specific light values. The set-aside value is tied
  to the map, so it can't move alone.

**F6 — A browser's forced dark repaints the light chrome. LOW; public.**

> **FIXED 2026-10-09 (S222).** `color-scheme` declared per theme in `styles.css`; the forced-dark emulation no longer repaints the stored-light chrome.
- **The setup (Chromium auto-dark, emulated):** OS dark, reader stored Light.
  Nothing declares `color-scheme`.
- **The result:** Chromium darkens the title box and inverts its ink, while the
  WebGL map stays light. That is the symptom S220 fixed for Dark Reader.
- **Two fixes stop it, both verified under OS dark:**
  - `<meta name="color-scheme" content="dark light">`;
  - per-theme CSS: `:root[data-theme="light"] { color-scheme: only light }` and
    `:root[data-theme="dark"] { color-scheme: only dark }`.
- The CSS form is better, because it also keeps native controls and scrollbars
  in the page's theme.
- Neither fix helps with OS light plus a forced flag. Chrome ties its real auto
  dark to the OS dark theme, so that case is an artifact of the emulation flag.
- **Samsung Internet's documented rule:** it applies the developer's alternate
  styles "if they exist", otherwise "its own transformations (Force Dark)"
  ([Samsung, 2020-12-15](https://developer.samsung.com/samsunginternet/blog/en-us/2020/12/15/dark-mode-in-samsung-internet)).
  Untested here.
- **Chrome's documented opt-out** is `color-scheme: only light`
  ([Chrome, Auto Dark Theme](https://developer.chrome.com/blog/auto-dark-theme)).

**F7 — An open revenue-mix panel keeps the other theme's greys after a switch. LOW; public.**

> **FIXED 2026-10-09 (S222).** `applyTheme` re-renders the pinned panel via `syncPinnedPanel()`.
- `applyTheme` repaints layers, backdrop and legend, but not `#temporal`.
- With a Future/rural or unzoned share showing, switching theme leaves those
  swatches at the other theme's value until the panel is re-opened. Measured
  both directions; the no-switch control shows 0.
- **Fix:** re-render the open panel in `applyTheme`.

**F8 — Print loses the legend key in both themes. LOW; public; pre-existing.**

> **FIXED 2026-10-09 (S222).** `print-color-adjust: exact` on the legend bar and swatches; the key prints in a `page.pdf()`.
- With the browsers' default "no background graphics", the gradient bar and the
  set-aside swatch print blank. The map still prints.
- A dark print also puts light ink on white chrome.
- This is the use case the 2026-09-22 row named as light mode's trigger.
- **Fix:** `@media print` with `print-color-adjust: exact` on the legend bar and
  swatches.

**F9 — Glow → light → dark leaves the reader on Inferno. LOW; decision.**
- `applyTheme` rewrites `state.ramp`.
- The 2026-10-09 row says only "Glow maps to Inferno" in light; it does not say
  what happens on the way back.
- Peter's call whether the choice should be restored.

**F10 — Docs left stale by the build. LOW; claim.**

> **FIXED 2026-10-09 (S222).** items 1–4 corrected; item 5 (the badge comment) waits on F3.
1. `docs/ARCHITECTURE.md` testing table: it says "42 scripts" and "only
   `verify-smoke.js` is wired into a workflow". The truth is 44 scripts, with
   smoke, blurbs and url-state in CI.
2. `docs/UI.md` → Light mode still opens by recommending a `THEMES.dark/light`
   object, and the build plan's phase 1 row names it. The phase 1 decision
   rejected that.
3. `web/index.html`, the `#title-p` comment: "nothing rewrites it on load".
   `syncThemeChrome()` rewrites it at every boot. No reader sees the static
   text, because the loading overlay covers it until then.
4. `web/index.html`, the guide comment: "the app's only localStorage use".
   The theme uses it too.
5. `scripts/build_site.py`, the badge comment (F3).

**F11 — The ink-contrast test composites over the backdrop only. LOW; guard-blind.**
- Over the darkest light prisms, `--accent-ink` falls to:
  - 4.4:1 on a reading panel;
  - 4.3:1 over cividis navy;
  - 3.9:1 on a pod.
- These are marginal, and F1's surface is the larger case of the same blind spot.
- **Observation, not a finding:** dark pods at α.7 over a yellow tower drop
  `--ink-2` to 2.8:1. That predates light mode, and the dark render did not put a
  pod over a tower.

**F12 — The Landmarks toggle says "plain grey landmarks". LOW; public; claim; pre-existing.**

> **FIXED 2026-10-09 (S222).** the tooltip now says "plain landmarks".
- The river has drawn blue in both themes since it changed from `(26,34,48)`.
  The string was written 2026-07-27 against that old colour.

**Not defects:**
- **M5:** older Safari's `MediaQueryList.addListener`. Moot, because the vendored
  deck.gl 9.0 needs WebGL2 (Safari 15+).
- **M4:** the light-only `verified/` and `notebooks/` pages. These are documents
  opened in a new tab, so a decision, not a miss. Recommend leaving them.
- **Arterial grey vs backdrop with alpha:** 2.26:1 light, 2.58:1 dark. It is
  recessive by design in both themes.

## §4 — What this run got wrong

1. **My first M2 pass said "0 stale everywhere", and it was void.** The probe
   hood was Downtown, whose revenue mix holds only categories that are
   theme-invariant. The cell could not differ. That is
   `check-where-the-value-can-be-wrong` again. Re-run with a hood carrying
   Future/rural and unzoned, M2 confirmed. Caught before reporting.
2. **Three renders silently showed Money.** Infill, Uses and the budget are gated
   out of the public build, and the hash or click was dropped. The page did what
   it was told; my state list was wrong. Caught by printing `state.view` per
   shot.
3. **I first leaned on ARCHITECTURE.md to confirm §1's negative, and that
   sentence was itself stale** (F10.1). The negative held only because I
   grepped the workflows.
4. **I read the Services screenshot as "light's low end vanishes".** Measured,
   light is better than dark (19.1% vs 21.7%). One theme's picture is not a
   comparison.
5. **The contrast probe dropped the arterial's alpha.** It reported 2.96:1; the
   real value is 2.26:1.
6. **The brief's M5 should not have been listed.** One look at `web/vendor/` moots
   it.

## §5 — Out of scope, still open

These are the items the brief excluded: the 360 px rates/sheet overlap, the phone
title clip, the grid's zoom subdivision, and the dark ramp-middle compression and
collision.
