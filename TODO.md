# TODO — living backlog

This is the **authoritative list of what's left**, edited in place as items open
and close. It holds only **non-derivable** work: things not yet started, and open
decisions. For mechanical state (branch, commits, test count, what files exist),
check `git` / `pytest` directly — do not restate it here, it only goes stale.

Session summaries (`session-summary/`) are dated *narratives* of what happened and
why. This file owns *what's left*. When they disagree, this file wins.

_Last reconciled: 2026-07-01_

## Open work

- [ ] **SCOPE: composition numbers now; full zoning POLYGON layer in the viewer is a
  SEPARATE later product decision** — it changes the viz from "revenue/acre" to
  "revenue/acre + land-use overlay" (clarity-vs-complexity call for a public audience).
  Do NOT couple them.

- [ ] **Residential-only lens (Phase 2 view — needs a pipeline extension first).**
  Goal: a UI filter that fades non-residential/downtown prisms so councillors see a
  pure residential-to-residential comparison (mature infill vs. greenfield suburb) —
  no class-rate differential or Downtown outlier confounding the scale. The narrative
  "third lens" after sqrt-colour (orient) + linear-height (the Downtown reveal), which
  the current single view already fuses.
  **Backend done (2026-07-01, commit `02704b6`)** — only the frontend remains:
  - [x] Split `dev` → `res` / `nonres` in `ZONE_CATEGORY` (by each code's
    `description`; 28 housing codes → res, 39 commercial/industrial/mixed/DC → nonres).
  - [x] Emit `frac_residential` + `is_residential` (≥0.50 of zoned area) per hood.
    Validated on real data: 226 residential, 0 overlap with set-aside.
  - [x] Added to `ZONING_COLUMNS` + `SLIM_COLUMNS`; regenerated GeoJSON carries both.
  - [x] Frontend filter (`web/index.html`): "Residential only" toggle fades
    non-residential hoods translucent (fill α70 / roof-edge α45 — **visible but
    see-through**, Peter's call), residential hoods keep full colour. Off by
    default; preserves metric/palette state. *(Not visually verified — no headless
    browser; preview `cd web && python -m http.server 8777`.)*
  Note: `is_residential` is a display filter, orthogonal to `is_set_aside` (grey);
  a set-aside hood is not residential. Keep the two flags independent.

- [ ] **Colour scale for revenue/value — decide after exempt split.** Current hard
  clamp ($50k / $4M, ~p97) creates a visible saturated plateau that reads as a fake
  threshold. Once exempt is split, re-run the skew check on the status-defined
  taxable set: if it's ≈ log-normal (likely), use `log` for the taxable scale; `sqrt`
  is the fallback if it stays mixed. Height stays LINEAR (locked honesty choice).
  *Colour ramps in `web/index.html`:* 3 swappable ramps (Inferno / Glow /
  Cividis) + palette switcher. **Default = Inferno (picked 2026-07-01).** Cividis
  retained in the switcher as a liked alternative + the colourblind-friendly
  option (see Visual polish → colourblind (cividis) mode below).
  *Not yet built:* scale toggle (linear+clamp / sqrt / log) for visual comparison.

- [ ] **UI control hierarchy: separate "Color Adjustment" from lens controls.**
  Two distinct categories, visually grouped apart so the distinction reads without
  explanation:
  - **Color Adjustment** (the sqrt scaling) sits *above*, as an on/off toggle — it's
    about *how* colour is rendered, not *what* you're looking at. Label honestly as
    "Color Adjustment (sqrt scaling)" — no implication either mode is the "correct"
    one; someone who never clicks it still sees a valid map.
    - [ ] Make sqrt a runtime toggle (currently hardcoded on via `scaleT`): Off =
      linear+clamp (true magnitude), On = sqrt (spread across the distribution).
      Legend gradient already recomputes per-transform (`legendGradient`), so wire it
      to the toggle. Height stays LINEAR either way (locked).
    - [ ] Self-describing state label that changes with the toggle:
      Off → "Off — colour shows true magnitude";
      On → "On — colour spread across distribution".
  - **Lens controls** below — metric (Revenue/Value), palette (Inferno/Cividis…),
    eventually the residential filter. These are about *what* you're looking at.
  Pairs with the scale-toggle line above (this is its UI design); folds the residential
  filter in as a lens once built.

- [ ] **Deployment** (per `docs/SPEC_deployment.md`): `.github/workflows/*.yml`
  (scheduled Action), `web/data/status.json` + maintenance banner, per-year archive
  filenames. Three open decisions, with leans:
  - [ ] change-detection — lean: rerun + git-diff
  - [ ] cron cadence — lean: weekly
  - [ ] heartbeat auth — lean: start with `GITHUB_TOKEN`

- [ ] **Visual polish** (pre-existing, untouched):
  - [ ] top-cap edge colour `TOP_EDGE_COLOR=[40,95,120,215]` in `web/index.html`
    ("not happy yet")
  - [ ] deferred zoom-out (~10.2→~9.4) + proportional `ELEVATION_SCALE` bundle
  - [ ] light mode + colourblind (cividis) mode

- [ ] **(Optional) exploration notebook** — work `FINDINGS_assessment_classes.md`'s
  "to visualize" list (value vs levy share by class; split-class distribution;
  per-neighbourhood exempt share). Notebooks go in `notebooks/exploration/`; per
  global CLAUDE.md, use the Jupyter MCP server tools, not NotebookEdit.

## Done

- [x] Revenue phase backend — per-property municipal levy + `revenue_per_acre`
  (committed `5912576`).
- [x] Web value↔revenue toggle, revenue default (committed `a0cf2a0`).
- [x] Push `feature/phase2-web` to origin.
- [x] **Low-coverage tail separated via the Zoning Bylaw layer (`fixa-tstc`)** —
  end-to-end land-use set-aside feature (2026-07-01). `src/load_zoning.py` (95 base
  codes → never/notyet/inst/dev, overlay → `set_aside_frac`/`is_set_aside`/
  `set_aside_reason`), wired through `join_and_calculate` + `main.py`; 48 hoods set
  aside at ≥0.90. Colour transform **DECIDED: sqrt** (FINDINGS §6.1 — log over-corrects
  to −4.19; the mixed 0.55–0.90 band stays on-scale by design). Frontend: sqrt colour
  + neutral-grey set-aside hoods. Methodology caveat recorded in FINDINGS §5 (zoning
  `UI`/`UF`/`AJ`/`PU` partially flags exempt-roll understatement). Refs:
  `docs/FINDINGS_revenue_scale.md` §§5–6.1, `scripts/investigate_skew.py`,
  `docs/SPEC_revenue.md` "Update 2026-06-29".
