# TODO — living backlog

This is the **authoritative list of what's left**, edited in place as items open
and close. It holds only **non-derivable** work: things not yet started, and open
decisions. For mechanical state (branch, commits, test count, what files exist),
check `git` / `pytest` directly — do not restate it here, it only goes stale.

Session summaries (`session-summary/`) are dated *narratives* of what happened and
why. This file owns *what's left*. When they disagree, this file wins.

_Last reconciled: 2026-07-09_

## Open work

- [ ] **PUBLIC RELEASE PREP (NEW 2026-07-09 — scope + rationale in
  `docs/PLAN_public_release.md`; read it before working these).** An external
  prioritization memo was intaken and reconciled: its build list (WEM/condo fix,
  roads, set-aside, fire, stormwater) is **already shipped or closed** — see the
  plan's reconciliation table. What remains is presentation-layer credibility +
  ops hardening. Release scope locked: everything live stays in; transit/
  recreation/franchise-display stay out. *(AMENDED 2026-07-11, Peter: the
  transit lens is IN — built as the fourth service; see the service-layers
  item below. Recreation + franchise-display still out.)* Items, ranked:
  - [x] ~~P1.1 README refresh~~ — done 2026-07-09 (this PR): "Methodology
    (Planned)"/QGIS/AltaLIS-FOIP sections replaced with as-built.
  - [ ] **P1.2 In-app attribution/methods affordance** — the live map has NO
    link to repo, data sources, or methodology. Small footer/info control:
    data source + assessment year, modeled-not-billed pointer, methods link.
  - [x] ~~P1.3 Public METHODS page~~ — done 2026-07-09 (PR #32 merged):
    `docs/METHODS.md` (metric definitions, denominators + guard, set-aside,
    WEM/condo worked examples, model formulas + validation ratios,
    limitations) + README Technical Docs link. P1.2 should link to it.
  - [x] ~~**P2.1 CI unmatched-set assertion**~~ — DONE 2026-07-11
    (`scripts/check_unmatched_names.py` + `data/expected_unmatched.json`, wired
    into `refresh.yml`; fails the build on a new money-path unmatched name). See
    the data-integrity audit §4 item below for scope detail.
  - [ ] **P2.2 Heartbeat PAT** (= the deployment follow-on below, bumped from
    "watch" to "do": 60-day Action auto-disable means silently stale public data).
  - [x] ~~P2.3 Security/PII checklist pass~~ — done 2026-07-09 (Session 33,
    Fable audit): all boxes ticked/dated with evidence; scope updated to the
    Phase-2 static-site + CI surface. **Findings logged, not fixed** — see
    `docs/security-audit.md` "Findings — 2026-07-09" (S1–S6). Follow-ups:
    - [ ] **P2.3a Apply S1** (Medium): vendor maplibre-gl@4.7.1 + deck.gl@9.0.38
      into `web/vendor/` (or add SRI hashes) — `web/index.html:8-10`, no
      `integrity=` today. Biggest risk-per-effort item.
    - [ ] **P2.3b Apply S3 + S4** (Low, ~10 lines each): entity-escape helper
      for the data-derived strings in `tooltipFor` (`web/index.html:1349`);
      SHA-pin the four actions in `refresh.yml`.
    - [ ] **P2.3c S5 hygiene**: bump the 5 dev-freeze pins (tornado/bleach/
      soupsieve/jupyter-server/jupyterlab — fix versions in the findings) next
      env touch; add a `pip-audit -r requirements-ci.txt` step to `refresh.yml`.
    - [ ] **P2.3d S2** — owner-only content decision, see security-audit.md S2.
  - [ ] **P2.5 Doc-drift fixes** (from the 2026-07-09 architecture
    reconciliation — six items listed in `docs/ARCHITECTURE.md` "Reconciliation
    notes"; no behavioural drift, docs lagging build only). Includes verifying
    the approximate Phase-1 dates in the new `docs/DECISIONS.md` index.
  - [ ] **P3 Decoteau/HHR/Riverview IIMP annotation** (= the existing item
    below; laptop-only) — the OIC-reconciliation credibility anchor; wanted
    before wider outreach, not gating a soft link.
  Platform question RESOLVED (Peter, 2026-07-09): **no new hosting, no new
  engineering** — release ships on the existing Pages deployment, nothing new
  gets built pre-release (plan §2).

- [x] ~~**PRIORITY — Lot-acre denominator TOGGLE on the neighbourhood (first) lens
  (NEW 2026-07-08, out of the cardinality audit below).**~~ **BUILT 2026-07-08**
  (branch `feature/hood-lot-acre-toggle`): `export_value_grid.build_hood_lot_acres`
  (per-hood dedupe rollup reusing `_point_lot_stats`/`SHARE_MAX_M2`) →
  `join_and_calculate` `lot_acres=` param computes `value_per_lot_acre` /
  `revenue_per_lot_acre` + `parcel_frac`, with a `LOW_PARCEL_FRAC = 0.15` guard
  (7 hoods suppressed on 2025 data — 6 set-aside + MAPLE RIDGE 1.6%); `main.py`
  builds it from the shared `grid_input`; columns in `SLIM_COLUMNS`. Frontend:
  the Glass `#denom` control mirrored onto the Money view (shared `state.denom`,
  `moneyScale()` with runtime p97.5 clamp + height parity, `lotBlurb`/legend/
  tooltip follow). +9 pytest (247), headless-verified
  (`verify-money-denom.js`, all PASS) + screenshots. Real numbers match the
  findings: U of A ×2.0, Rossdale ×2.8, Riverdale ×2.5. **SHIPPED 2026-07-09 —
  PR #23 merged + deployed** (refresh run 28987792808, green; roads download
  fixed by PR #24's 900s timeout + retry same run). Auto-refresh commit `bb224da`
  verified data-only: 0 geometry changes (the Session-27 additive graft matched
  CI-canonical geometry exactly), only `parcel_frac`×233 + `storm_charge`×3 value
  drift from the fresh roll. Original brief kept below for reference.
  <details><summary>original item</summary>
   The audit found the first
  lens has NO bug to fix, but a parcel/lot-acre denominator is worth OFFERING: it
  systematically boosts park/river-valley hoods (median ×2.47 $/acre for the 51 hoods
  <55% parcel land; Rossdale ×2.8, Riverdale ×2.4) — the Urban3-analogous "value per
  *developable* acre" view. 35 of 406 hoods move >50 ranks (Spearman 0.959). Build:
  mirror the Glass view's "Ground acres | Lot acres" toggle on the neighbourhood
  choropleth — add `value_per_lot_acre` / `revenue_per_lot_acre` hood columns
  (aggregate deduped `lot_size` per hood via the shipped `SHARE_MAX_M2` /
  `_point_lot_stats` heuristic in `export_value_grid.py`; reuse `load_property_info`),
  a per-column scale anchor, and a **low-parcel-fraction guard** (suppress hoods
  below ~15% parcel to an "n/a" grey — else near-zero-parcel hoods explode, e.g. Mill
  Woods Golf Course ×6960; plus the `KNOWN_BOUND_OUTLIERS` >100% tail, Pembina).
  Frame honestly: ground-acre = cardinality-robust default, lot-acre = Urban3-analogous.
  Full numbers + rationale: `docs/FINDINGS_denominator_cardinality.md`.
  **Validation/guard fixtures (worked in the findings doc, 2026-07-08):** University
  of Alberta = a guard-PASS case (50% parcel, $7.6M→$15.2M/ac = ×2.0, exempt
  campus/hospital land off-roll) — a new *exempt-institutional* rise category beyond
  the park/river-valley examples; pair it with Mill Woods Golf Course (0% parcel,
  ×6960) as the guard-FAIL case when regression-testing the ~15% floor. NB the toggle
  makes U of A's revenue intensity honest but can't show its exempt-land service
  free-riding — that's the services lens, not this one.
  </details>

- [x] ~~**PRE-LAUNCH AUDIT — record-to-parcel cardinality bug (WEM numerator + condo
  denominator) & lot-acre vs ground-acre methodology (NEW 2026-07-08).**~~ **CLOSED
  2026-07-09** (Q1/Q2/Q5 answered 2026-07-08; Q6/Q7 methodology-note cleanup done
  2026-07-09 — see below). Part of a
  broader sweep to check the main lenses before this goes public/live officially.
  **Q1/Q2/Q5 ANSWERED 2026-07-08** — `docs/FINDINGS_denominator_cardinality.md`
  (`tools/audit_cardinality_denominators.py`): the **first lens is immune to both bugs,
  structurally and empirically** (numerator sums the real per-account roll and never
  joins parcel geometry; denominator is boundary area and never reads lot_size). WEM is
  a SINGLE $1.285B account (a grid needle, not a numerator double-count — the brief's
  premise was inverted). Condo denominator inflation is 0.1% citywide / +12% worst hood
  and the `SHARE_MAX_M2` dedupe already handles it. Ground-acre = 74% parcel land
  citywide (~26% roads/parks/ROW); it is NOT Urban3 lineage (Q6 — Urban3's denominator
  is closer to lot-acre). The lot-acre neighbourhood lens that fell out is now the
  PRIORITY item above. **Q6 + Q7 DONE 2026-07-09 — the methodology-note cleanup:**
  swept the docs (README, SPEC_revenue, ARCHITECTURE, UI, FINDINGS_lot_dedupe,
  DATA_INTEGRITY, web tooltips) and found NO doc actually asserted "ground-acre =
  Urban3/gross-area" — every Urban3 mention already pinned the lineage to *parcel/
  lot*-acre. Added a positive not-Urban3-lineage note to `ARCHITECTURE.md`'s
  ground-acre bullet (so the distinction survives outside the findings doc) + the
  condo-exclusion-as-industry-norm paragraph to `FINDINGS_lot_dedupe.md` §1. Q3 (single
  join-integrity fix) is effectively moot for the first lens — there is no bug to fix; the
  grid already carries the only dedupe needed. Sweep the docs (`FINDINGS_lot_dedupe.md`,
  `DATA_INTEGRITY.md`, README/UI methodology blurbs) for stale Urban3-lineage claims.
  **Original brief for reference —** two
  known distortions share ONE root cause — a **record-to-parcel cardinality mismatch**
  (multiple assessment records → one parcel geometry) — but push in OPPOSITE directions,
  so they do NOT cancel in aggregate and summing-before-dividing at the hood level does
  NOT protect against either (corruption is upstream, in the raw components):
  1. **WEM**: many assessment records join one parcel → inflates the revenue *numerator*,
     denominator unchanged.
  2. **Condos**: shared lot area duplicated across unit records → inflates the area
     *denominator*.
  Overlaps existing machinery: the lot-acre denominator work (PR #12,
  `docs/FINDINGS_lot_dedupe.md`) already ships a repeat-aware `SHARE_MAX_M2` dedupe +
  `*_per_lot_acre` columns and verified WEM as a single-account needle — this audit is
  the systematic pre-launch confirmation + the ground-acre methodology cleanup, not a
  from-scratch dig. **Anchor docs:** `FINDINGS_lot_dedupe.md`, `DATA_INTEGRITY.md`,
  `DATA.md` §2 (condo/lot_size quirks); consider driving with the `edmonton-audit` skill.
  **Questions to answer in code/data (numbers, not yes/no):**
  1. **Quantify WEM's numerator inflation.** Count assessment records per underlying WEM
     parcel geometry; compute the hood's revenue/acre with duplicate-join revenue
     collapsed to one record/parcel vs the current summed total. Report the % distortion.
  2. **Quantify condo denominator inflation.** Confirm whether unit-level records each
     carry the FULL shared lot area (vs a prorated per-unit share); find the hoods with
     the highest condo-titled-unit concentration; compute the % area overcount there
     under current logic vs a corrected (dedup/prorated) area.
  3. **Confirm the root cause is shared** — both bugs = multiple records → one geometry —
     and scope a SINGLE join-integrity fix covering both, not two patches.
  4. **Test ground-acre as a partial mitigation.** Confirm ground-acre (boundary-polygon
     hood area) is structurally immune to the condo bug (never touches parcel/unit
     records), and confirm it does NOT fix the WEM numerator bug (revenue is still summed
     from assessment records regardless of denominator).
  5. **Characterize what ground-acre actually measures.** Does the hood boundary area
     include non-parcel land (roads, alleys, parks, ROW) alongside parcel land? If so,
     quantify the ground-acre vs summed-lot-acre gap on a sample of hoods, so the methods
     note can state precisely what ground-acre includes that lot-acre excludes.
  6. **Correct any "Urban3-standard / gross land area" claim for ground-acre.** Web
     research indicates Urban3 computes value/acre as total *parcel* value ÷ total
     *parcel* area — i.e. their denominator is closer to this project's **lot-acre**, NOT
     a boundary-derived gross area. No evidence Urban3 uses a gross/boundary denominator.
     Fix any doc language implying ground-acre has Urban3 lineage: ground-acre is an
     **independent addition here, justified on cardinality-robustness grounds**, not
     methodological continuity with Urban3.
  7. **Document condo handling as an industry-wide open problem**, not just an internal
     bug: independent Urban3-method replications (e.g. the Bloomington-Normal Strong Towns
     GIS group) reportedly EXCLUDED condo parcels entirely rather than solve the ownership
     complexity. This project's dedupe (if it ships as the fix) is a genuine improvement
     over exclusion — useful methods-note context.
  **Deliverable:** a short written finding per question (with numbers) — likely a FINDINGS
  doc; recommended scope for the single join-integrity fix (WEM + condos); and methods-note
  language distinguishing **lot-acre (Urban3-analogous)** from **ground-acre (this
  project's own robustness-motivated addition)**, incl. what land ground-acre includes
  that lot-acre excludes.

- [ ] **Decoteau / Horse Hill / Riverview capital & debt annotation (NEW 2026-07-08).**
  A **citation/annotation layer, NOT a new spatial cost lens**, covering the three
  greenfield growth areas analyzed in the City's IIMP (Integrated Infrastructure
  Management Plan) — a 39-year capital pro forma (developer capital + muni/provincial
  capital + O&M + lifecycle renewal, amortized vs projected tax revenue). This is a
  **fundamentally different unit of analysis** than the citywide recurring-cost map
  (which deliberately excludes capital construction cost). Why now: IIMP is the closest
  existing precedent to the **OIC** (operating-impact-of-capital) accounting the City is
  introducing for the **2027–2030 zero-based budget cycle** — citing it well anchors the
  tool's credibility without rebuilding a citywide capital/debt model we have no data for.
  **Scope (locked — do NOT deviate without flagging):**
  - Sidebar/annotation on **three specific named hoods only**, clearly labeled as a
    different methodology (multi-decade capital pro forma) from the revenue-per-acre /
    recurring-cost map.
  - **Do NOT** merge these figures into the citywide colour layer, the roads lens, the
    utilities lenses, or any recurring-cost calc; **do NOT** interpolate/extrapolate
    capital-debt cost to other hoods. Only these three growth areas have a published IIMP
    analysis — citywide capital-cost data at this fidelity doesn't exist.
  - Neutral/descriptive framing per project convention: state the IIMP's own projected
    figures + time horizon, don't editorialize.
  **Build:**
  1. Pin Decoteau, Horse Hill, Riverview boundaries in the existing hood boundary file.
  2. Attach a data **annotation (not a computed layer)**: developer capital, muni/provincial
     capital (~$369M piece), build-out horizon, revenue-vs-cost gap — all as stated in the
     source, with explicit citation + "as of" date.
  3. Surface as a click-through popup / footnote-style panel — **NOT** a toggle affecting
     the main colour ramp.
  **Sources to hunt (primary supersedes secondhand):**
  - **PRIMARY: the actual IIMP / "Fiscal Impacts of Growth" report** for Decoteau/Horse
    Hill/Riverview — referenced secondhand via a Gemini research summary in project files;
    we don't yet have the primary City doc. Search council agenda/report archives
    (edmonton.ca, eScribe/insite) for "IIMP", "Fiscal Impacts of Growth", "Decoteau ASP",
    "Growth Related Analysis". (edmonton.ca is Oracle-box-unreachable — laptop-only, per
    the Session-21 blocker.)
  - 2016 Global News coverage (already in project research) as secondary corroboration —
    primary report should supersede it for exact figures.
  - Off-site levy bylaw + capital financing policy — how the ~$369M muni/provincial piece
    was financed (debt vs levy vs grant); that's the "debt" component specifically.
  - City annual financial statements / debt management reports — actual debt-servicing
    cost + interest rates for the relevant financing period, IF we want real debt-service
    cost rather than just capital outlay.
  - Infrastructure committee **mid-2026 OIC presentation** (already in project context) —
    check whether it re-presents/updates the three areas' figures under the new OIC
    framework; if so, cite that instead of the 2016 analysis.
  **Non-goals:** no citywide capital-cost-per-hood dataset this pass; no blending into any
  recurring-cost lens.

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
      "Services views"). "Total services" DEFINITION: DECIDED 2026-07-10 —
      stays per-service (denominator picker; SPEC_utilities decision 3);
      the V2 unit-cost composite is tracked under "More service layers".
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
    - [x] ~~**Transit lens**~~ — BUILT 2026-07-11 (Peter's call, AMENDS the
      2026-07-09 release-scope lock that kept transit out): mean-weekday
      scheduled GTFS stop-events/acre (`transit_dep_per_acre`, sqrt colour
      FINDINGS §6.8), Services-view checkbox + 58 LRT-station/transit-centre
      dots, five new weekly GTFS downloads. SPEC_services "Transit lens",
      DATA.md §9. Scheduled supply, NOT ridership (none exists stop-level);
      current-signup seasonality is the standing caveat.
      - [x] ~~**LRT track lines** context layer~~ — added 2026-07-11: the
        operating network (Capital/Metro/Valley) as a `PathLayer` under the
        station dots (`rpjw-4jft` "LRT Routes" → `web/data/lrt_lines.json`,
        343 segs); the HER heritage streetcar is excluded (not ETS LRT
        service). Not part of the metric. DECISIONS.md 2026-07-11.
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
      detail: UI.md "Services views".
    - [x] ~~**"Total services" / Ratio-view denominator reopen**~~ — **DECIDED
      2026-07-10 (Peter) + V1 BUILT same day** (branch
      `feature/ratio-denominator-picker`): the ratio stays **PER-SERVICE** —
      a "Ratio denominator" picker (revenue per road metre | per fire
      event) in the Ratio view. Modeled EPCOR dollars (storm/water) are
      excluded from any levy ratio by the money-flow honesty rule (they'd
      compare unrelated flows / cancel if added to both sides) — so the
      "two dollar services" trigger resolved to per-service, not a $ sum.
      Fire floor 0.005 events/acre/yr + log colour: FINDINGS §6.7;
      SPEC_utilities decision 3 holds the full design; headless-verified
      (`verify-ratio-denom.js`, 27 checks) + regressions + screenshots.
      Also fixed in passing: `verify-labels.js` still clicked the retired
      "roads" view button (stale since the 2026-07-05 generalization).
      **PR #33 merged (`e0da845`) + deployed 2026-07-10** (refresh run
      29099791508 green → auto-refresh `e8f58b4`; github-pages deploy
      success; live-verified 27/27 vs the Pages URL).
    - [ ] **V2 — combined "modeled city service cost per acre" (LAPTOP-GATED:
      budget source hunt).** One denominator = road metres × published
      roadway O&M+renewal $/m/yr + fire events × (Fire Rescue operating
      budget ÷ citywide dispatches). Needs the two unit costs from City
      budget documents (edmonton.ca unreachable from the Oracle box — same
      bucket as the IIMP hunt); they become a manual reviewed input
      (`city_unit_costs.json`, mill-rates pattern), labeled MODELED and
      "roads + fire only", never "total city cost". Design already locked
      in SPEC_utilities decision 3.
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
        assumption — [x] ~~sensitivity-check M2_GROSS_PER_UNIT~~ DONE
        2026-07-07: 70–120 m²/unit sweep moves households ±7% but citywide
        $ only ±5% — the assumption is NOT the source of the EPCOR gap;
        90 baseline stands. `tools/sensitivity_m2_per_unit.py` +
        FINDINGS_utility_validation §2.1); validation vs EPCOR revenue
        (below, now covers water too).
      - [x] ~~Validation pass vs EPCOR published revenue~~ — DONE
        2026-07-07 (Session 19), full numbers + sources in
        `docs/FINDINGS_utility_validation.md`. **Order-of-magnitude PASS
        both lenses.** Stormwater: $240.4M modeled vs $141.1M published
        2025F (1.70×), but residential slice is 1.11× and the excess is
        localized (notyet+never zones = $49.8M unbilled land; I=1.0 vs
        real DIF reductions on commercial). Water/sanitary: $588.1M vs
        ≈$467M published res+MR scope (≈1.26×); connection count 13%
        UNDER EPCOR's (268k vs 308k accounts) — excess is per-connection.
        [Refined 2026-07-07: the in-city water res+MR share was a flat ~70%
        guess; now derived to ~80% from EPCOR's by-class customer+consumption
        counts (EWS 2024 PBR Progress Report p.9, FINDINGS §2.2), tightening
        the ratio 1.33×→1.26×. The raw water revenue-by-class schedule stays
        unreachable (all edmonton.ca public-files paths dead, no Wayback), so
        ~80% is a blend estimate, not a read-off — but a well-anchored one.]
      - [x] ~~**Peter decision (bracket quantified, FINDINGS §3)**~~ —
        DECIDED 2026-07-07: report BOTH (all-parcels $240.4M AND excl
        notyet+never zones $190.5M). Shipped same day:
        `UNBILLED_CATEGORIES` in `src/load_stormwater.py` — log line +
        `.attrs` carry both totals; per-hood outputs unchanged
        (reporting, not modeling). 230 tests green; real-data verified.
      - [x] ~~Lenses 3–4 (electricity/gas franchise)~~ — BUILT 2026-07-07
        as **columns only, no display layer** (Peter's call: they're
        collinear with dwelling count — flat per-dwelling proxy makes every
        column `dwellings × constant`). `src/load_franchise.py` reuses
        `load_water.build_connections` (extracted shared helper → ONE
        551,831-dwelling model) + `data/franchise_rates.json` + join wiring
        (`FRANCHISE_COLUMNS`, out of SLIM) + `--skip-franchise`; 8 tests
        (238 total). Real run: **$162.6M/yr modeled City revenue** (elec LAF
        $36.9M + gas franchise $125.7M). Modeled LAF ~⅓ low vs published
        $8.33/mo (base schedule vs full distribution revenue — documented).
        As-built + validation: SPEC_utilities "Lens 3+4 as built" +
        FINDINGS_utility_validation §5. Follow-ups: (a) ~~validate vs City
        budget franchise line~~ **DONE 2026-07-07** — vs Note 24 of the 2024
        Financial Annual Report (audited): combined elec+gas modeled $162.6M
        vs actual $175.9M = **0.92×**, but two offsetting errors — gas 1.32×
        over (Rider T in the 35% base; excl → 1.00×), elec 0.46× under (LAF
        floor). FINDINGS §5.1; (b) commercial scope needs a consumption proxy;
        (c) display lens if ever wanted.
      - [ ] **DEFERRED (Peter, 2026-07-07 — revisit later): exclude
        transmission Rider T from the gas franchise base?** Validation §5.1
        found modeled gas franchise ($125.7M) exceeds the all-sector City
        actual ($95.2M) at 1.32×; dropping Rider T ($1.357/GJ) from the 35%
        base → $95.6M ≈ 1.00×. One-line change (`gas_rider_t_per_gj` already
        isolated in `franchise_rates.json`). NOT proven — residential-only
        matching an all-sector actual could be a compensating 115 GJ/dwelling
        overcount. Parked as-is with the Rider-T caveat documented; no model
        change for now.
      - [ ] Remaining SPEC open decisions: (3) modeled $ in the "total
        services" denominator (recommended: not yet); (4) franchise-fee
        revenue columns only with their lenses — SETTLED (columns only,
        built above).
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
    - [x] ~~**Residential prisms over the Uses fabric** (Peter's ask
      2026-07-10: "how much residential is in each neighbourhood
      specifically")~~ — built 2026-07-10: layers-panel checkbox (default
      off), translucent sand prisms with height = `frac_residential` on a
      fixed 0–100% linear scale, peak deliberately 2.5 km NOT the 8.2 km
      parity height (bounded share clusters 40–95% → full parity renders a
      solid wall; screenshot-verified before lowering). Zero-share hoods
      omitted (z-fight), opacity on the shared prism slider (Uses default
      35%), labels ride roofs, blurb honesty line, state persists.
      Client-side only — `frac_residential` already served. Headless-
      verified (`verify-uses-prisms.js`, 20 checks) + full regression
      suite green + screenshots. Display detail: UI.md "Uses view".
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
    - [x] ~~**land-use diversity analysis (Peter, 2026-07-03)**~~ — DONE
      2026-07-07 (Sessions 22 + 24). ANALYSIS_BACKLOG item 4, see
      `docs/FINDINGS_land_use_diversity.md`. Result: revenue/acre vs diversity
      holds under controls (partial r +0.27, n=299) but is secondary to density;
      road-per-dwelling vs diversity is a **null**. Prerequisite DC provision
      scrape (ANALYSIS_BACKLOG item 3) also DONE end-to-end (crawl→extract→
      classify→QA→rollup): the 918 DC provisions are use-classified
      (`data/dc_inferred_use.csv`), rolled up per hood
      (`data/dc_use_by_hood.csv`), folded into the index, and 8 of the 14
      previously-dropped high-`frac_dc` hoods re-admitted — both verdicts
      unchanged. Open upgrades: formal regression + p-values (needs `scipy`);
      `notebooks/exploration/` scatter version (deferred).
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

- [x] ~~**UI control hierarchy: separate "Color Adjustment" from lens controls.**~~
  **BUILT 2026-07-07** (`web/index.html`, `#coloradj` panel at the top of the right-hand
  stack, above the lens controls; UI.md "Colour Adjustment toggle" bullet is the as-built).
  - [x] ~~sqrt as a runtime toggle~~ — `state.colorAdjust` (default **on**) gates the
    money/glass sqrt in `scaleT`; off = linear+clamp (true magnitude). Legend follows via
    `legendGradient`→`scaleT`; the money/glass blurb colour clause swaps via
    `withColourClause` (honesty). Height stays LINEAR either way. **Scope = `scaleT`
    consumers (money + glass) only** — greys out (disabled) in services/ratio/uses, which
    use their own transforms (`svcT`, `ratioT`).
  - [x] ~~Self-describing state label~~ — `#coloradj-state`: On → "colour spread across
    distribution", Off → "colour shows true magnitude".
  - **Not visually verified in a browser** (no headless browser on the laptop) — awaits
    Peter's on-device eyeball. JS syntax `node --check` green.
  - Deferred follow-on (if Peter wants it): a single GLOBAL "sqrt colour" switch that also
    drives fire's sqrt (services) — currently fire/ratio transforms are independent.

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

- [ ] **Data-integrity audit follow-ons** (first run 2026-07-01, **second run
  2026-07-11** — see `docs/FINDINGS_data_integrity_audit.md`; second run covered
  all post-07-01 modules: roads/storm/water/franchise/fire/transit/lot-acre/grid.
  **No blocking findings; published numbers confirmed trustworthy.**):
  - [x] ~~**CI unmatched-set assertion (audit §4 / second-run T3c):**~~ DONE
    2026-07-11 — `scripts/check_unmatched_names.py` asserts the live money-path
    unmatched set == committed baseline `data/expected_unmatched.json`
    (`assessment_not_in_boundaries` = {OLIVER}, `boundaries_not_in_assessment` =
    {LEWIS FARMS}); wired into `refresh.yml` as a hard gate after download, before
    regen. A NEW assessment name with no boundary (silent dollar loss) FAILS the
    build (exit 5) → no wrong-data deploy, last-good data keeps serving. New
    boundary holes / resolved names → exit-0 warnings (update the baseline). +8
    tests. **Scope = the money path only** (the join that drops dollars); the five
    service frames (zoning/roads/storm/fire/transit/water) default unmatched to
    0/NaN — less catastrophic, still `join_and_calculate`-warned — so extending
    the guard to them is a possible future add, not done here.
  - [x] ~~**`validate="m:1"` on the `join_and_calculate` merges (second-run
    NEW-1):**~~ DONE 2026-07-11 — added `validate="m:1"` to all nine merges
    (base assessment + zoning/roads/storm/fire/transit/water/franchise/lot-acre);
    pandas now raises `MergeError` if a duplicate right-key ever appears instead
    of silently misaligning every per-acre denominator via the positionally-reused
    `safe_area`. +2 tests (`test_duplicate_assessment_key_raises`,
    `test_duplicate_roads_key_raises`). Pipeline reruns clean on real data (all
    nine pass validation). 277 pytest green.
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
