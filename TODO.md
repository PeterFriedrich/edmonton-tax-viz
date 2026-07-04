# TODO — living backlog

This is the **authoritative list of what's left**, edited in place as items open
and close. It holds only **non-derivable** work: things not yet started, and open
decisions. For mechanical state (branch, commits, test count, what files exist),
check `git` / `pytest` directly — do not restate it here, it only goes stale.

Session summaries (`session-summary/`) are dated *narratives* of what happened and
why. This file owns *what's left*. When they disagree, this file wins.

_Last reconciled: 2026-07-02_

## Open work

- [ ] **Services lens — road supply (SPEC'd 2026-07-01, branch `feature/services-lens`).**
  Spec: `docs/SPEC_services.md`. V1 = `road_m_per_acre` (city-maintained
  **collector + local** centreline metres per boundary acre; per-class columns
  kept internally, arterials computed but excluded from the metric); V2 fast
  follow = revenue per road-metre. Locked: alleys OUT, arterials OUT (shared
  infrastructure), railway OUT, City-owned only.
  Build order:
  - [x] ~~Prerequisite commit: `$limit` count-vs-limit assertion in
    `scripts/download_data.py` + add roads source `9j8t-zm52`~~ — done
    2026-07-01 (closes the data-integrity §5 follow-on below); roads
    downloaded + verified (53,720 features, check passes).
  - [x] ~~`src/load_roads.py` + synthetic tests~~ — done 2026-07-01 (13 tests;
    real data: 3,644 km collector+local in metric, 0.28% unassigned).
  - [x] ~~Wire `join_and_calculate` (`ROAD_COLUMNS`) + `main.py` flags~~ — done
    2026-07-01 (+4 tests; GeoJSON regenerated, `road_m_per_acre` on all 406).
  - [x] ~~Skew check on `road_m_per_acre` → pick colour transform~~ — DECIDED
    2026-07-01: **linear** (raw skew −0.29; sqrt/log over-correct; FINDINGS §6.3).
    Clamp ≈ p97.5 = 53 m/acre.
  - [x] ~~Frontend: third metric in the Revenue/Value toggle~~ — done 2026-07-01
    (per-metric transforms, linear roads, button hides on pre-services data,
    headless-verified; set-aside grey kept per the v1 lean).
  - [x] ~~Docs: `DATA.md` §6, `ARCHITECTURE.md` module entry, status.json
    vintage~~ — done 2026-07-01. Resolution on vintage: **no roads year field**
    — the network is a live feed with no roll-year semantics; provenance =
    `last_checked` (recorded in SPEC_services + DATA.md §6).
  - [x] **Display pivot (2026-07-01): two-plane stackable architecture — COMPLETE
    2026-07-02** (SPEC_services.md "Display architecture — REVISED"; final control
    model = three discrete views **Money | Roads | Ratio**, UI.md "Services
    views"). Road prisms RETIRED; staging as executed:
    - [ ] (1) Roads ground layer:
      - [x] ~~pipeline: slim `web/data/roads.geojson` export (dissolved per
        hood × arterial/access, simplified 8 m, 5 dp)~~ — done 2026-07-02
        (`export_roads_web` in `src/load_roads.py`, wired into `main.py`;
        791 features, 2.3 MB, committed like the polygons file; +5 tests).
      - [x] ~~frontend: layers panel, lazy-loaded ground layer; arterials
        neutral, access roads coloured by hood `road_m_per_acre` (linear,
        clamp 53); remove Roads from metric toggle~~ — done 2026-07-02
        (headless-verified; details in UI.md "Roads ground layer").
    - [x] ~~(2) Prism transparency control (money plane overlays service
      plane)~~ — done 2026-07-02, landed with stage 1: opacity slider in the
      layers panel (prisms + roof edges) + 45% auto-nudge on first Roads
      enable — needed because the network is ~invisible under opaque prisms
      (only setback gaps show).
    - [x] ~~(3) Ratio view: revenue vs total services (revenue-per-road-metre
      is the single-service case — subsumes the old V2 item)~~ — done
      2026-07-02 as the **Ratio view** (Money | Roads | Ratio buttons;
      ghost prisms of $/road-metre over the neutral network; log colour
      FINDINGS §6.4; road-base floor 5 m/acre greys artifacts; UI.md
      "Services views"). "Total services" DEFINITION still deferred until
      a second service exists — reopen this staging list then.
  - [x] ~~Merge `feature/services-lens` → master via PR once Peter's eyeballed
    it~~ — done 2026-07-02: PR #8 merged, refresh workflow run green, live site
    verified serving the three views + roads.geojson.

- [ ] **Views & lenses follow-ons (Peter, 2026-07-02).** Three asks on top of the
  shipped Money | Roads | Ratio views:
  - [x] ~~**Residential-only lens in the Ratio view.**~~ — done 2026-07-03:
    non-residential kept hoods fade to the lens grey (height untouched), log
    colour anchors rescale to the residential kept subset (≤ $258 … $916+ vs
    $264 … $3,253 — FINDINGS §6.4 addendum), lens button disables in the Roads
    view (state persists). Headless-verified (`tools/profiling/verify-lens.js`
    + screenshot); UI.md updated. **PR #9 merged + deployed** (run 28646374983;
    deploy step needed one transient-error rerun); live site verified serving
    the new code.
  - [ ] **More service layers (water / drainage / transit / …).** Each needs its
    own SPEC_services section (dataset, filters, locked decisions), a
    per-hood supply column, and a slim web export. Decide the UI shape when
    the second service arrives: another view button doesn't scale — likely
    the Roads view generalizes to a "Services" view with per-service
    checkboxes (the original stackable idea returns, one level down). That's
    also the trigger to define "total services" and reopen the ratio's
    denominator (currently roads-only by construction).
  - [x] ~~**Use-mix view: surface each neighbourhood's zoning composition.**~~
    **SHIPPED 2026-07-03 — PR #10 merged + deployed** (run 28679596055, green
    first try); live site verified serving the Uses view + `zoning.geojson`
    (200, 1.17 MB). Shows what the land IS (res / com / ind / mixed / DC /
    institutional / reserve), not what it yields. **Decisions (Peter,
    2026-07-03):** nonres split 4 ways `com`/`ind`/`mix`/`dc` — DC its own
    category (24% of nonres area, bespoke bylaws, can't honestly fold
    elsewhere); a **fourth view button** Money | Roads | Ratio | Uses; real
    bylaw geometry (clipped to the 45 m hood setbacks) rather than
    dominant-colour hoods; tooltip = dominant use + stacked composition bar.
    Sub-items below record the build trail.
    - [x] ~~Pipeline prerequisite: split `ZONE_CATEGORY` + export the full
      composition~~ — done 2026-07-03: 39 nonres codes re-tagged (ambiguous
      names resolved from bylaw purpose statements — UW/HA/MMS → mix, BE →
      ind, MED/AED → com; DATA.md §5); unknown codes now default to `other`
      (not `nonres`); `ZONING_COLUMNS`/`SLIM_COLUMNS` extended with all 9
      fracs; GeoJSON regenerated (0.68 MB, fracs sum to 1 on all 406, 48
      set-aside / 226 residential unchanged; +4 tests, 135 green).
    - [x] ~~Frontend: "Uses" view~~ — built 2026-07-03: fourth view button,
      flat categorical fill by dominant use, validated 7-hue palette + two
      neutral greys (UI.md "Uses view" — colours computed through the dataviz
      validator, min all-pairs CVD 10.6 w/ gap+tooltip relief), data-driven
      legend rows, composition tooltip, lens disabled in-view, old-data
      guard. Headless-verified (`tools/profiling/verify-uses.js`, 0/406 fill
      mismatches; `verify-lens.js` regression green) + screenshot.
      (Superseded same day by the real-geometry render below; the
      dominant-colour path remains as the fallback.)
    - [x] ~~Tooltip mini stacked composition bar~~ — done 2026-07-03 (Peter's
      ask): 190×8 px flex bar in the category colours above the composition
      text; `.tip` max-width 300px so long compositions wrap.
    - [x] ~~Real zoning geometry IN the Uses view~~ (Peter's call — the
      dominant-colour render was "meh utility"; consciously reopened the
      "zoning polygon overlay" scope item for THIS view only) — done
      2026-07-03: `export_zoning_web` (citywide category dissolve, simplify
      10 m, grid-snap `set_precision` — plain rounding after the validity
      pass broke the browser tessellator; 8 features, 1.1 MB), wired into
      `main.py`; frontend lazy-loads it with dominant-colour fallback +
      hood-hover tooltips on top; legend now shows all 8 present categories.
      +4 tests (139 green); verify-uses.js + verify-lens.js green;
      screenshot eyeballed.
    - [ ] **NEXT after this ships — land-use diversity analysis (Peter,
      2026-07-03):** ANALYSIS_BACKLOG item 4 (normalized entropy over the
      composition shares → test revenue/acre vs mix and road-per-household vs
      mix, deconfounded by age/density/lot size). Build prerequisites in order:
      (1) `dkk9-cj3x` download step in `scripts/download_data.py` (+$limit
      guard) for `year_built`/`lot_size`; (2) residential-record count per hood
      (household proxy) — from the already-loaded assessment CSV; (3) the DC
      provision scrape (ANALYSIS_BACKLOG 3) before trusting the entropy index
      (DC = unknown use, not mixed use).
    NOTE: this is hood-level composition — it does NOT reopen the "full
    zoning polygon overlay" scope decision below; keep them decoupled.
    FINDING (for ANALYSIS_BACKLOG 1): the 8 dc-dominant hoods are the big-box
    power centres — South Edmonton Common, Terra Losa, Mill Woods Town Centre,
    Calgary Trail South, Summerlea, Place LaRue, McCauley, Strathcona Junction.

- [x] ~~**Neighbourhood labels — finish + ship**~~ — SHIPPED 2026-07-04
  (PR #11 merged, deployed run `28712502638` — one transient Pages failure,
  fixed by `gh run rerun --failed` — live-verified). Final styling: 15 px /
  weight 800, 128 px SDF atlas (`radius: 24`, `smoothing: 0.08`) for
  city-zoom sharpness; Peter approved on-device. 27 labels at city zoom /
  64 at zoom 12.2. See UI.md "Neighbourhood labels" for the
  CollisionFilterExtension and glyph-scale gotchas.

- [ ] **Ghost prisms over a neutral hood plane (Peter, 2026-07-03; design
  clarified 2026-07-04).** The Urban3-infographic composition: keep the
  extruded prisms but render them **transparent**, over a flat hood plane
  UNDERNEATH that is **one neutral colour — NOT metric-coloured** (Peter:
  "i don't actually want the color on the hood underneath"). The plane is
  mouseover geography, not a signal carrier; ALL metric signal stays in the
  prisms. Exception: **set-aside/holdout hoods get their own distinct colour**
  on the plane. Hover/tooltip lives on the hood plane, like the Uses-view
  pattern (hood layer under a display layer carries picking + highlight).
  No new data — hood polygons + all metrics already in the served GeoJSON
  (display-only build). Still open at build time: which metrics get it
  (money / ratio / both); fifth view button vs a "flat"/composition toggle
  on existing views (overlaps the "control hierarchy" item below); prism
  opacity default (the existing opacity slider may already cover it); the
  two plane colours (neutral + set-aside — the current set-aside grey may
  serve as one of them); whether the road network stays underneath as
  ground context like Ratio.

- [x] ~~**SCOPE: composition numbers now; full zoning POLYGON layer in the viewer is a
  SEPARATE later product decision**~~ — RESOLVED 2026-07-03: Peter opted in for the
  Uses view (PR #10) — the real bylaw geometry renders there, category-dissolved and
  clipped to the hood setbacks. The metric views (Money/Roads/Ratio) stay
  overlay-free; any zoning overlay ON those views would be a new decision.

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

- [x] **Deployment — LIVE (2026-07-01/02)** at
  https://peterfriedrich.github.io/edmonton-tax-viz/ (merged to master, PRs #1–3).
  Scheduled GitHub Action (`.github/workflows/refresh.yml`, weekly Mon 08:00 UTC +
  dispatch) downloads all inputs → `main.py` → `status.json` heartbeat →
  commit-if-changed → deploy Pages. `scripts/download_data.py` (all three inputs),
  `scripts/generate_status.py`, frontend banner, `requirements-ci.txt`. Pages enabled
  `build_type: workflow`; first run + node24-bump run both green in production.
  Decisions settled: rerun+git-diff / weekly / `GITHUB_TOKEN`. See `docs/SPEC_deployment.md`.
  **Deferred follow-ons still open (below).**

- [ ] **Deployment follow-ons (deferred, see `docs/SPEC_deployment.md`):**
  - [x] ~~Year-mismatch **guard**~~ — built 2026-07-01 (`scripts/check_year_alignment.py`
    + `refresh.yml` wiring): detects the roll year from Socrata metadata; on mismatch
    skips regen, keeps serving committed data, auto-sets the holding banner. See
    SPEC as-built notes + `docs/FINDINGS_data_integrity_audit.md` §3.
  - [ ] Auto-**fetch** matching `pwis-wc4c` rates for a newly detected year (the
    guard detects + holds; it doesn't self-heal). Recovery is manual: bump
    `ASSESSMENT_YEAR`, extend `mill_rates.json`, update `generate_status.py` years,
    `--clear-banner`.
  - [ ] Per-year archive filenames (`web/data/YYYY.geojson`, keep-not-overwrite) for
    the future UI year selector.
  - [ ] **Heartbeat watch:** if the schedule auto-disables after 60 days idle, add a
    repo-scoped PAT for the heartbeat commit (SPEC "Staying awake").
  - [ ] Optional tidy: delete merged branches on origin (`feature/phase2-web`,
    `feature/deployment`, `chore/node24-actions`, and the three audit-session
    branches from 2026-07-01: `docs/data-integrity-audit-brief`,
    `fix/name-corrections-audit`, `feature/year-alignment-guard`).

- [ ] **Data-integrity audit follow-ons** (found 2026-07-01, see
  `docs/FINDINGS_data_integrity_audit.md` §4–5; findings 1–3 fixed + deployed):
  - [ ] **CI unmatched-set assertion (audit §4):** commit the expected unmatched
    list (now just the OLIVER straggler) and fail the CI build when the live
    unmatched set differs — converts name-drift from warn-silent to fail-loud.
  - [x] ~~**Socrata `$limit` truncation check (audit §5)**~~ — built 2026-07-01
    on `feature/services-lens` (`check_not_truncated()` in
    `scripts/download_data.py`, fails at count >= limit; +6 tests; roads
    source added in the same commit).
  - [ ] (Optional, fidelity) map `MA DERELICT RESIDENTIAL` to the dedicated
    "Mature Area Derelict Residential" rate class instead of "Non Residential" —
    identical municipal rate today, differs if `rate_type` ever changes (audit T1).

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
