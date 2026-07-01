# TODO — living backlog

This is the **authoritative list of what's left**, edited in place as items open
and close. It holds only **non-derivable** work: things not yet started, and open
decisions. For mechanical state (branch, commits, test count, what files exist),
check `git` / `pytest` directly — do not restate it here, it only goes stale.

Session summaries (`session-summary/`) are dated *narratives* of what happened and
why. This file owns *what's left*. When they disagree, this file wins.

_Last reconciled: 2026-07-01_

## Open work

- [ ] **Separate the low-coverage tail — PREREQUISITE for the colour scale.**
  The revenue distribution is a **mixture**: a roughly log-normal taxable core
  (log-skew −0.22 with the tail removed) + a near-zero spike of ≈57 neighbourhoods.
  Mixed, `log` over-corrects (left skew −2.16); the transform can't be chosen until
  the spike is split out — **by category, not by a revenue threshold** (thresholding
  is the arbitrary-cap sin).
  **CORRECTION (2026-06-29):** the spike is NOT exempt land. `is_exempt` flags only
  3 parcels citywide; exempt_share = 0.00 across all 57; tax-exempt institutional
  land (Legislature/schools/etc.) is **absent from the taxable roll entirely**, not
  flagged or zeroed. The spike is **low taxable coverage** — undeveloped/natural
  land (20× "RIVER VALLEY", golf courses, ring-road margins, energy parks,
  undeveloped town centres; 55/57 have <200 parcels). So the separator is
  coverage/land-use, not exempt share.
  **APPROACH (decided 2026-06-29): the Zoning Bylaw layer (`fixa-tstc`).** Boundary
  file has no type field (cols: number/name/descriptive_name/ward/district/desc/geom).
  Instead use Edmonton's zoning polygons (11,510; codes + descriptions) spatially
  overlaid on neighbourhood boundaries → land-use **composition %** per neighbourhood.
  Principled, area-based, non-arbitrary. Buckets split THREE ways (the policy story):
  - **Never taxable** — `A` River Valley, `NA` Natural Areas, `PS`/`PSN` Parks → set aside.
  - **Not yet** — `FD` Future Urban Development (+ fringe `AG`/`RR`) → "fiscal potential", flag separately.
  - **Genuine underperformer** — developed-zoned but low value/acre → STAYS on the scale
    (zoning = what's *allowed*, not *built*; underdeveloped residential is the fiscal story).
  - **Institutional/other-jurisdiction** — `UI`/`UF`/`AJ`/`PU` → proxy for where the
    exempt-roll understatement lives (recovers the "undetectable" caveat, partially).
  *Methodological framing (for the doc):* neighbourhood-level aggregation REQUIRES
  explicit categorization of non-developable land that parcel-level (Urban3) handles
  implicitly. It's compensation for our unit choice, not feature creep.
  - [ ] Methodology caveat to record: revenue/acre **understates** neighbourhoods
    holding large exempt institutions; zoning (UI/UF/AJ) now lets us *flag* where,
    though zoning ≠ tax status (proxy only).

  **LOCKED 2026-06-29** (in specs — SPEC_revenue Update, ARCHITECTURE, DATA §5,
  SPEC_deployment, UI): set-aside = **never + not-yet** at **≥0.90**; mixed (0.5–0.9)
  + developed STAY on scale; set-aside renders **neutral grey**, excluded from the
  scale fit; **zoning is a refreshed input** (auto-graduates developing land).
  Validated in scratch: tail median set-aside 0.99 vs developed 0.11; 48 set aside,
  24 mixed kept; ZERO genuine underperformers in the tail.
  **BUILD:**
  - [x] `src/load_zoning.py` — explicit `code→category` dict (all 95 base codes;
    never/notyet/inst/dev), reproject 3400, `buffer(0)` clean, overlay →
    `set_aside_frac`/`is_set_aside`/`set_aside_reason` per neighbourhood. + 10 synthetic
    tests. *(2026-07-01: `DC`/`DC1`/`DC2` → developed; unknown codes warn + default dev.
    Validated on real data: 48 set aside, zero unmatched codes.)*
  - [x] Wire into `join_and_calculate` (optional `zoning=` arg, graceful when absent) +
    `main.py` (`--zoning-geojson`/`--skip-zoning`); regenerated web GeoJSON now carries
    `set_aside_frac`/`is_set_aside`/`set_aside_reason` (48 set-aside features). Raw
    `zoning.geojson` stays gitignored + re-pulled each cycle (like the other raw inputs).
  - [x] Re-run skew on the set-aside-excluded set → pick colour transform.
    **DECIDED: sqrt** — taxable core is NOT log-normal at the 0.90 threshold (log
    over-corrects to −4.19; the mixed 0.55–0.90 band stays on-scale by design and
    drags the left log-tail). Recorded in FINDINGS_revenue_scale §6.1; reproduce via
    `scripts/investigate_skew.py`.
  - [x] Frontend (`web/index.html`): colour now **sqrt**-scaled (`scaleT`);
    set-aside hoods render neutral grey off the ramp (`SET_ASIDE_COLOR`, excluded
    from the scale), legend gradient resampled under sqrt + a set-aside swatch,
    tooltip shows the set-aside reason + %, blurbs note the transform. *(Not yet
    eyeballed in a browser — no headless render here; preview via
    `cd web && python -m http.server 8777`.)*
  - Zoning GeoJSON re-downloaded 2026-07-01 to `data/raw/zoning.geojson` (9.2 MB,
    gitignored) — ready to use, no re-download needed. Validated numbers to reproduce:
    tail median set-aside 0.99 vs developed 0.11; ~48 set aside, ~24 mixed kept.

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
  **Blocked on the zoning layer**, which today lumps residential + commercial +
  industrial + mixed into one `dev` bucket (`src/load_zoning.py`) and exports only
  `set_aside_frac`/`is_set_aside`/`set_aside_reason` (the per-category fracs are
  computed but dropped). To unblock:
  - [ ] Split `dev` → `residential` vs `non-residential` in `ZONE_CATEGORY` (data
    supports it — descriptions distinguish "…Residential"; standard RSF/RM/RS/RSM/RL/
    HDR/RMU + the special-area row-housing/apartment codes are residential).
  - [ ] Emit `frac_residential` + `is_residential` (dominant, e.g. ≥0.50) per hood.
  - [ ] Add them to `ZONING_COLUMNS` + `SLIM_COLUMNS` so they reach the GeoJSON.
  - [ ] Frontend filter: make non-residential prisms transparent/dimmed on toggle.
  Note: `is_residential` is a display filter, orthogonal to `is_set_aside` (grey);
  a set-aside hood is not residential. Keep the two flags independent.

- [ ] **Colour scale for revenue/value — decide after exempt split.** Current hard
  clamp ($50k / $4M, ~p97) creates a visible saturated plateau that reads as a fake
  threshold. Once exempt is split, re-run the skew check on the status-defined
  taxable set: if it's ≈ log-normal (likely), use `log` for the taxable scale; `sqrt`
  is the fallback if it stays mixed. Height stays LINEAR (locked honesty choice).
  *In progress, uncommitted in `web/index.html`:* 3 swappable colour ramps
  (Inferno / Glow / Cividis) + palette switcher — done, awaiting Peter's pick.
  *Not yet built:* scale toggle (linear+clamp / sqrt / log) for visual comparison.

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
