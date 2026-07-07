# TODO — living backlog

This is the **authoritative list of what's left**, edited in place as items open
and close. It holds only **non-derivable** work: things not yet started, and open
decisions. For mechanical state (branch, commits, test count, what files exist),
check `git` / `pytest` directly — do not restate it here, it only goes stale.

Session summaries (`session-summary/`) are dated *narratives* of what happened and
why. This file owns *what's left*. When they disagree, this file wins.

_Last reconciled: 2026-07-06_

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
    per-hood supply column, and a slim web export.
    - [x] ~~**Services-view UI generalization**~~ — **SHIPPED 2026-07-05:
      PR #14 merged + deployed + LIVE** (run 28767241818 — deploy step
      needed two transient-error reruns, "Deployment failed, try again
      later"; live verified serving the Services button + storm column on
      all 406 hoods; CI regenerated the geojson byte-identical). The Roads
      view is now a "Services" view with per-service checkboxes (Roads,
      Stormwater; Fire added 2026-07-06) and a "colour" radio choosing which checked
      service drives the ramp (others render neutral; defaults = the old
      Roads view exactly). Headless-verified
      (`tools/profiling/verify-services.js` + regressions green) +
      screenshots (`shot-services.js`) + Peter's on-device eyeball. Display
      detail: UI.md "Services views". Defining "total services" and reopening the ratio's
      denominator (currently roads-only by construction) remains open —
      SPEC_utilities decision 3: keep it physical until at least two dollar
      services exist.
    - [x] ~~**Fire lens**~~ — **BUILT 2026-07-06** (design DECIDED 2026-07-05,
      Peter, all four recommendations: demand metric events/acre/yr as the
      Services ground plane + 31 station dots; all emergency responses minus
      operational noise, medical share a caveat NOT a filter; 2023–2025
      averaged, pinned `FIRE_YEARS`; built after the Services UI landed).
      As built (branch `claude/session-summary-review-vwweia`):
      `src/load_fire.py` (+21 tests) + `download_data.py` sources
      (`7hsn-idqi`, `b4y7-zhnz`) + `join_and_calculate` FIRE_COLUMNS →
      `fire_events_per_acre` in SLIM_COLUMNS + `main.py --skip-fire` +
      third Services checkbox (shared `svc-plane`, station dots,
      demand/medical caveats) + verify-services/shot-services extended.
      209 pytest green; headless-verified against a SYNTHETIC fire column.
      Dataset facts: DATA.md §7–8; spec: SPEC_services "Fire lens".
      **Remaining follow-ups (blocked on network access to
      data.edmonton.ca — the build session's VM policy denied it):**
      - [x] ~~First real-data run~~ — DONE 2026-07-06 (Session 18, Oracle
        server): `dispatch_datetime` resolved as the first exact candidate
        (186 of 948k unparseable); mix verified (MEDICAL 60%, 4,025 noise
        excluded, 88,065 kept events/yr / 408 fire hoods). Caught + fixed
        TWO real-data bugs: PR #17 (event_type_group carries CODES — filter
        on event_description) and PR #18 (`FIRE_NAME_CORRECTIONS`: fire CSV
        still says OLIVER for WÎHKWÊNTÔWIN, 1,476 events/yr displayed as 0;
        + 3 "AREA" collapses). Live-verified: plane + 31 dots + tooltip.
      - [x] ~~Colour transform check on real `fire_events_per_acre`~~ —
        DECIDED 2026-07-06: **sqrt** (raw skew +7.86, the project's worst;
        clamp/median 5.8×; linear crammed 59% of hoods into the ramp's
        bottom fifth; log undefined on the 5 zero hoods. FINDINGS §6.5).
      - [ ] **January task**: bump `FIRE_YEARS` (main.py) AND the
        2023–2025 wording in the fire blurb + legend (`web/index.html`).
    - [ ] **Utility cost lenses — SPEC'd 2026-07-05 (`docs/SPEC_utilities.md`);
      stormwater DECIDED first (Peter) and its v1 PIPELINE BUILT same day on
      `feature/stormwater-lens` (unmerged).** Five candidates in three
      fidelity tiers, from Peter's methods doc
      (`docs/utility_cost_estimation_lens_methods.md` — verified 2025/2026
      tariffs; rate numbers live there). All outputs MODELED, not billed.
      - [x] ~~Stormwater pipeline (Lens 1)~~ — built 2026-07-05:
        `src/load_stormwater.py` (bylaw A×I×R per point; `ZONE_RUNOFF`
        explicit dict; condo dedupe reused; fixa-tstc zone fallback) +
        year-keyed `data/stormwater_rates.json` + join/main wiring +
        19 tests (182 green). Real data: 287,103/287,163 points, citywide
        $240.4M/yr (2025 rate), ranking sanity passes (industrial top,
        river valley bottom). As-built numbers + caveats: SPEC_utilities
        Lens 1 (serviced-area assumption is the big one — EETP fringe = 5%
        of the total; AG runoff coded 0.1 with VERIFY flag).
      - [x] ~~**Display shape**~~ — DECIDED (Peter; SPEC decision 2) and
        **SHIPPED 2026-07-05 (PR #14, with the Services-view item above)**:
        per-hood ground-plane layer in the generalized Services view —
        linear colour, clamp p97.5 of non-set-aside hoods (≈ $2,700,
        runtime), set-asides grey, legend + blurb labeled MODELED /
        "modeled, not billed"; `storm_charge_per_acre` added to
        `SLIM_COLUMNS` (hood GeoJSON 0.7 MB, all 406 hoods carry it).
        Pipeline PR #13 merged first, as sequenced.
      - [x] ~~Water + sanitary (Lens 2)~~ — BUILT 2026-07-07 (Session 18,
        branch `feature/water-lens`; decisions locked with Peter
        2026-07-06: residential+multi-res scope, two columns, colour by
        TOTAL): `src/load_water.py` (per-connection model — roll points
        as connections, meter-size bands, inclining/declining blocks) +
        `data/water_rates.json` (Apr 2026 tariffs; `WATER_RATE_YEAR` pin)
        + join/main wiring + fourth Services checkbox (LINEAR colour,
        FINDINGS §6.6; tooltip fixed/total split). Real run: 268,489
        connections / 551,831 modeled households, citywide $588.1M/yr
        ($133.9M fixed). 229 tests green; headless-verified on real data.
        As-built numbers + caveats: SPEC_utilities "Lens 2 as built".
        Follow-ups: household count ~20% over census (floor-area→units
        assumption — sensitivity-check M2_GROSS_PER_UNIT); validation vs
        EPCOR revenue (below, now covers water too).
      - [x] ~~Validation pass vs EPCOR published revenue~~ — DONE
        2026-07-07 (Session 19), full numbers + sources in
        `docs/FINDINGS_utility_validation.md`. **Order-of-magnitude PASS
        both lenses.** Stormwater: $240.4M modeled vs $141.1M published
        2025F (1.70×), but residential slice is 1.11× and the excess is
        localized (notyet+never zones = $49.8M unbilled land; I=1.0 vs
        real DIF reductions on commercial). Water/sanitary: $588.1M vs
        ≈$440M published res+MR scope (≈1.33×); connection count 13%
        UNDER EPCOR's (268k vs 308k accounts) — excess is per-connection.
      - [x] ~~**Peter decision (bracket quantified, FINDINGS §3)**~~ —
        DECIDED 2026-07-07: report BOTH (all-parcels $240.4M AND excl
        notyet+never zones $190.5M). Shipped same day:
        `UNBILLED_CATEGORIES` in `src/load_stormwater.py` — log line +
        `.attrs` carry both totals; per-hood outputs unchanged
        (reporting, not modeling). 230 tests green; real-data verified.
      - [ ] Remaining SPEC open decisions: (3) modeled $ in the "total
        services" denominator (recommended: not yet); (4) franchise-fee
        revenue columns only with their lenses; Lenses 3–4 unbuilt.
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

- [x] ~~**Ghost prisms over a neutral hood plane (Peter, 2026-07-03; design
  clarified 2026-07-04).**~~ **SHIPPED 2026-07-05 — PR #12 merged + deployed**
  (run `28757734787`, green first try; live site serves the Glass view +
  `value_grid.json` with the lot-acre columns, 1.76 MB / 200). Full design
  trail below; the denominator story continues in the lot-size item after it.
  The Urban3-infographic composition: keep the
  extruded prisms but render them **transparent**, over a flat hood plane
  UNDERNEATH that is **one neutral colour — NOT metric-coloured** (Peter:
  "i don't actually want the color on the hood underneath"). The plane is
  mouseover geography, not a signal carrier; ALL metric signal stays in the
  prisms. Exception: **set-aside/holdout hoods get their own distinct colour**
  on the plane. Hover/tooltip lives on the hood plane, like the Uses-view
  pattern (hood layer under a display layer carries picking + highlight).
  DECIDED 2026-07-04: **its own (fifth) view button** — "directly cribbing
  the Urban3 style thing, just with our own interactive flavor" (Peter).
  V1 (hood-prism glass, built + verified on `feature/glass-view`) was then
  refined by Peter: the spikes should be **finer than the hood unit** — the
  Urban3 detail level. DECIDED 2026-07-04 (after the condo lot_size probe —
  see DATA.md §2): **100 m grid cells** (~35k, in Peter's "a tenth of 287k"
  range), height = **revenue in cell ÷ cell GROUND acres** (consistent with
  the hood metric's boundary-acre denominator; no condo/lot_size artifacts).
  Built on `feature/glass-view` (merged in PR #12): pipeline grid export +
  Glass view renders the cells over the neutral hood plane (pure point
  binning, 34,675 cells). Tests + verify-glass.js green; screenshots
  eyeballed.
  - [x] ~~**Confirm the set-aside artifacting is gone (Peter, on-device).**~~
    CONFIRMED 2026-07-05 — Peter eyeballed the local preview (reverted
    point-binned grid + the new denominator toggle): "looks fine". The
    rollback stands; no further diagnosis needed. Original context below.
    Peter saw "really bad artifacting, specifically in areas that are
    actually set asides" (2026-07-04) after the footprint-spreading round.
    DECIDED 2026-07-04: **spreading ROLLED BACK** (`70a5d54` reverted in
    `19c25fb`) rather than diagnosed — back to point binning. The
    artifacting is presumed caused by the spreading (synthetic footprint
    squares up to 1.2 km painting faint cells over river valley /
    set-aside land, plus tens of thousands of sub-1 m cells coplanar with
    the plane); needs Peter's eyeball on the reverted grid to confirm
    before ship.
  - [x] ~~**Large single-point lots needle the grid (known limitation,
    post-rollback).**~~ RESOLVED by the lot-acre denominator toggle
    (shipped in the same PR — see the lot-size item below); the needle
    remains visible in ground-acre mode by design (that metric honestly
    shows dollars-per-map-cell). Original context: One lat/long per
    account means WEM ($1.285B,
    43 ha) is a single $12.6M/acre spike — #1 citywide, 2× the top
    downtown tower; lots > 1 ha are 5,524 rows / ~18% of citywide value.
    **Chosen fix: the PRIORITY lot-size denominator variant below** (per
    parcel acre, the tower correctly beats WEM ~50×). The reverted
    footprint-spreading approach (spread value over a lot-area square
    centred on the point, `git show 70a5d54`) also de-needled WEM but
    caused the set-aside artifacting above; if ever revisited instead,
    fix the spillover first (clip spread cells to the parcel's hood
    polygon, cap the square side, floor displayed $/acre — REPORTED,
    not silent).

- [x] ~~**PRIORITY — Lot-size denominator variant for the grid spikes**~~
  **SHIPPED 2026-07-05 — PR #12** (with the Glass view above; deployed +
  live-verified). (Peter, 2026-07-04; prioritized after the WEM
  verification.) The true Urban3
  metric is revenue per PARCEL acre (`dkk9-cj3x` `lot_size`), not per
  ground acre. **Why it's now priority:** verified 2026-07-04 that the
  ground-acre grid ranks WEM (single account, $1.285B, 107-acre lot, one
  lat/long → one 2.47-acre cell → $12.6M levy/acre needle, #1 citywide)
  2× above the top downtown tower ($620M on 0.93 acres) — but per LOT
  acre the tower beats WEM ~50× ($612M vs $12M value/lot-acre). Point
  binning ÷ fixed cell area rewards "most dollars pinned to one point",
  not land productivity; the lot-acre denominator is the chosen fix
  (preferred over resurrecting the reverted footprint spreading).
  **PIPELINE BUILT + VALIDATED 2026-07-05** (`docs/FINDINGS_lot_dedupe.md`):
  - [x] ~~Dedupe heuristic~~ — REVISED same day after cell-level validation:
    the first-draft distinct-sum collapsed identically-apportioned townhouse
    complexes (KAMEYOSEK 309 units → 0.04 ac → fake $1.2B/lot-acre needles).
    Shipped rule = repeat-aware (`SHARE_MAX_M2 = 1000 m²`): repeated values
    < 1000 m² count per unit (real shares), ≥ 1000 m² count once (duplication
    guard); majority-null multi-unit points ineligible (56 points / $1.23B /
    0.52% of roll, excluded + REPORTED). Threshold insensitive 500–2000 m².
  - [x] ~~Wire into `export_value_grid`~~ — done: `load_property_info.py`
    (new), `account_number` in load_assessment, `*_per_lot_acre` columns in
    `value_grid.json` (1.8 MB, null where no eligible acres),
    `check_lot_acre_bounds` RAISES on new bound violations (PEMBINA the
    committed `KNOWN_BOUND_OUTLIERS`); `--skip-property-info` degrades to
    ground-acre only. 163 tests green (+23).
  - [x] ~~Validation vs ground-acre~~ — done (FINDINGS §6.5): top-10
    lot-acre cells all Downtown CBD; WEM $12.6M → $290k; tower cell #1 at
    $14.8M revenue/lot-acre; p97.5 $105k vs $144k ground.
  - [x] ~~**Frontend: denominator toggle in the Glass view**~~ (Peter,
    2026-07-05: "make it togglable, so i can view both") — built 2026-07-05:
    "Ground acres | Lot acres" in the layers panel (Glass-only; hidden on
    grid files without the lot columns), per-column scale anchors, null-lot
    cells DROPPED in lot mode (28), legend/blurb follow the denominator.
    verify-glass extended (denominator matrix green; lens+uses regressions
    green); shot-denom.js eyeballed — WEM needle collapses in lot mode.
    UI.md synced. Peter's on-device eyeball PASSED 2026-07-05 ("looks
    fine"); PR #12 merged + deployed same day (README view list rode in
    the PR).

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
