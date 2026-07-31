# TODO — living backlog

This is the **authoritative list of what's left**, edited in place as items open
and close. It holds only **non-derivable** work: things not yet started, and open
decisions. For mechanical state (branch, commits, test count, what files exist),
check `git` / `pytest` directly — do not restate it here, it only goes stale.

Session summaries (`session-summary/`) are dated *narratives* of what happened and
why. This file owns *what's left*. When they disagree, this file wins.

**Closed items live in `docs/TODO_archive.md`, not here** (moved 2026-07-30).
`## Open work` carries only live work; `## Done` keeps a one-line entry for every
closed item, so **the *never redo a closed item without asking* rule still works
by grepping `## Done`** — the reasoning is one hop away in the archive. This file
is read at the start of every session, so it should hold what is still true, not
the whole history. Keep it that way: when an item closes, move its body to the
archive and leave a `## Done` line.

_Last reconciled: 2026-07-31 (S80 — **the temporal + change lenses are PUBLIC**
(#121, merged + deployed) and **the verify suite is GREEN for the first time on
record: 26 scripts, 0 failures** (#122). Three things closed by *measurement
rather than building*: mobile chrome step 3 was not reproducible; the
45-grey-hoods "blocker" had shipped in S79; and all three verify failures were
stale TEST expectations, not app bugs. Also found and fixed a **data-loss bug in
`tools/todo_archive.py`** — it OVERWROTE the archive instead of appending, and
had destroyed 747 lines of S79 history before it was caught. **The `▶` moves to
the bottom-sheet decision** — the last open piece of the mobile work, and
Peter's call, not a build item.)_

## Open work` carries only live work; `## Done` keeps a one-line entry for every
closed item, so **the *never redo a closed item without asking* rule still works
by grepping `## Done`** — the reasoning is one hop away in the archive. This file
is read at the start of every session, so it should hold what is still true, not
the whole history. Keep it that way: when an item closes, move its body to the
archive and leave a `## Done` line.

_Last reconciled: 2026-07-31 (S80 — **mobile chrome step 3 CLOSED as NOT
REPRODUCIBLE, no code change.** Carried as the `▶` since S74 and never started;
re-measuring found the symptom already gone, in both builds and every view. The
**third** time an open item's stated cause proved stale — reproduce before
building. **The `▶` moves to promoting the temporal + change lenses to the
public build** (Peter's call this session). Prior S79 state still current: the
change map is live (#120); the two pre-existing verify failures are
re-reproduced with values confirmed, only the triage decision left.)_

## Open work


- [ ] **UI BUG: the Display popover paints OVER the Data & Methods pod
  (Peter, 2026-07-28).** Bottom-right: opening **Display** covers the
  **Data & Methods** button sitting above it.
  - **Suspected cause — UNVERIFIED, reproduce before fixing.** `#about.open`
    gets a `z-index: 5` bump (`web/index.html:250`); `#a11y` has **no
    equivalent `.open` rule** and stays at the base `z-index: 1` — so when the
    Display menu opens it has no way to win the stacking contest, and equal
    z-index falls back to DOM order. An asymmetry that looks like an oversight
    when `#about` was added. **But that is a hypothesis from reading the CSS,
    not a reproduction** — confirm the actual overlap first.
  - Both pods are `right: 22px`, `#a11y` at `bottom: 40px` and `#about` at
    `bottom: 68px`, and opening either closes the other (`web/index.html:243`),
    so the overlap is the open Display menu over the *closed* About button.
  - `verify-about.js` already asserts paint order at 390/360/1440
    (`topmost=about-menu`) — extend it to the Display menu rather than writing
    a new script.

- [ ] **Mobile chrome — and it is NOT the blurb collapse, that already shipped**
  (commit `0089eba`, "mobile chrome move 1"). Confirmed good on device by Peter
  2026-07-28. **Read `docs/MOBILE_USABILITY.md` §3 before starting.** **Steps
  1, 2 and 3 are now all done** — step 3 closed 2026-07-31 as not reproducible
  (see below). What actually remains is one **decision**, not a build item:
  - [x] **Step 3 — the left-edge clip. CLOSED 2026-07-31 AS NOT REPRODUCIBLE —
    no code change.** The S74 symptom (`#controls`/`#coloradj` at left **−51**,
    `#toggle` at **−10**) does **not** occur on current master. Re-measured at
    390×844 with `hasTouch`/`isMobile`, in **both builds**, across **every
    visible view**, with the Options pod **unfolded** — nothing renders at
    negative left and nothing overflows right:

    | | left | right |
    |---|---|---|
    | `#controls` | 8 | 382 |
    | `#views` | 22 | 382 |
    | `#toggle` | 103 | 382 |
    | `#coloradj` / `#layers` / `#moneymode` / `#chgwindow` | 177 | 371 |

    Two things had to be got right to measure it at all, both worth keeping:
    **(1)** `#optpanel` is `.folded` by default at ≤640px, so the pod's rows
    have **no layout box** and report `0,0` — the folded state cannot show the
    clip, and a naive pass reads as "fixed" for the wrong reason. Unfold first.
    **(2)** The public build keeps full-only controls in the DOM but **hidden**,
    so selecting by presence hangs Playwright's `click()`; filter on visibility.
    Headless Chromium also measures text **wider** than the real font stack
    (quirk y), so a no-clip result there errs safe.
    ⚠️ **`tools/profiling/shot-mobile.js`'s id list is STALE** — no `moneymode`
    /`chgwindow`, and its comment still claims 5 public views. Fix before
    trusting it for the next mobile pass.
  - [ ] **▶ The open question inside step 2 — bottom sheet or not.** Whether the
    control column is fine as a stack or wants a bottom sheet / hamburger.
    **Decide against the CURRENT render**, now that the blurb is collapsed: the
    old reasoning was written when the blurb still ate the top third. Peter's
    call, not a build item.
  - Context that makes this the priority: chrome covers **45.1%** of a 390x844
    screen vs 27.3% at 1440x900 (measured S73). Label scarcity on phones is a
    *panel-size* problem, not a cull problem.

- [ ] **CARDINALITY GUARD — two small follow-ons (guard shipped 2026-07-28, PR #110).**
  `scripts/check_value_anchors.py` now pins the record-to-parcel *regime* in
  bands and runs in `refresh.yml` after regeneration. Both known bugs were
  re-verified as non-issues (see `AUDIT_LEDGER.md` 2026-07-28); this is
  maintenance, not a defect.
  - [ ] **Tighten the bands once there is variance data.** They are +/-50%
    off a SINGLE snapshot — a guess biased toward not crying wolf. After a few
    weekly refreshes, re-pin against observed spread with
    `--write-baseline --tolerance`.
  - [ ] **Optional, Peter's call: lower `STALE_DAYS`.** Currently 14 against a
    weekly cron = one missed run tolerated, two consecutive misses warn. A
    drift failure is therefore viewer-silent for 14 days. If that is too long
    for a public audience, the knob is global (`web/index.html`) and should
    move for ALL failure types at once — deliberately NOT a per-guard banner
    (`DECISIONS.md` 2026-07-28).

- [ ] **GEOGRAPHIC REFERENCE LAYERS — TIERS 2 & 3 (Tier 1 shipped 2026-07-27).**
  Tier 1 (North Saskatchewan River + Anthony Henday ring road) is live and on by
  default; see `DECISIONS.md` 2026-07-27 (×2) and `data/DATA.md` §14. The render
  seam is proven: `buildLayers()` BRACKETS `buildViewLayers()` —
  `referenceUnderLayers()` (river, bottom) before it, `referenceOverLayers()`
  (ring road, top) after — one Display-menu toggle, `verify-reference-layer.js`.
  **Which end a new reference shape belongs at is a real question, not a
  default:** the river went underneath because the hood fabric already traces
  it (set-aside valley = a river-shaped seam), so painting over glitched; the
  ring road has no such seam and is invisible underneath. What's left:
  - [ ] **Tier 2 — Edmonton internal reference.** District labels (West
    Edmonton, Mill Woods, Castle Downs, Terwillegar, Southeast) + Downtown and
    Old Strathcona/Whyte Ave; major arterials as thin unlabeled lines
    (Whitemud, Yellowhead, Gateway/Calgary Trail) from the existing road feed,
    same allowlist technique as the Henday. **Label collision is DECIDED
    (2026-07-27, Peter):** feed district labels into the existing
    `visibleLabels()` declutterer with districts winning priority — do NOT add
    a second, independent label layer, or "MILL WOODS" will stack on "MILL
    WOODS TOWN CENTRE". Districts have no dataset; coordinates are hardcoded
    and placement is a design call, not a data-fidelity one.
  - [x] ~~**Tier 3 — the NAMES half.**~~ **DONE 2026-07-27.** Seven regional
    place names ship on by default (St. Albert, Sherwood Park, Spruce Grove,
    Fort Saskatchewan, Leduc, Beaumont, Devon). Split out from the boundaries
    deliberately: the names needed no polygon fetch, and bundling them was what
    made Tier 3 look expensive. See `DECISIONS.md` 2026-07-27 (×2),
    `data/DATA.md` §14, `docs/UI.md`.
  - [ ] **Tier 3 — the BOUNDARIES half (still open).** Thin grey outline, no
    fill, for St. Albert / Strathcona County / Leduc. Now a standalone call on
    its own merits: the orientation payoff was mostly the names, so this is
    worth doing only if the *shape* of the neighbours adds something. Alberta
    `urban_and_rural_municipality` MapServer, natively **EPSG:3400**.
    **Sublayer IDs confirmed:** Edmonton / St. Albert / Leduc are all in
    **78 (`City`, field `CITY_NAME`)**; **Strathcona County is in 104
    (`Specialized Municipality`, `SPMUN_NAME`) — NOT 114
    (`Municipal District and County`)**, which holds Leduc/Sturgeon/Parkland
    *County*. Ids 67/95/105 are group layers and return no fields. Note the
    names half needed a *third* sublayer, **66 `Urban Service Area`**, for
    Sherwood Park — the hamlet-like service area of Strathcona County, which is
    a different thing from the County polygon in 104.
  - [ ] **Which end of the stack do boundaries belong at?** Same real question
    Tier 1 answered per-feature. Unlike the river there is no seam in the hood
    fabric to show through, and unlike the ring road they sit entirely
    *outside* the city where nothing occludes them — so both arguments that
    settled Tier 1 are silent here. Measure before assuming.
  - [ ] **Zoom-gating does not exist yet** — nothing in `index.html` gates on
    zoom today, so Tier 2/3 introduce the concept. Tier 1 deliberately renders
    at all zooms.
  - **Explicitly out of scope (decided 2026-07-27):** the Edmonton river
    valley/ravine overlay (`gis.edmonton.ca` Common_Layers 115). It is a
    regulatory development-setback polygon, not the river — drawing it near the
    water would read as "the river is this wide."

- [ ] **MOBILE USABILITY (NEW 2026-07-22 — full plan in
  `docs/MOBILE_USABILITY.md`; read it first).** Phone rendering is unstyled for
  small screens (zero `@media` queries today). **Confirmed problem:** the top
  third collides — title/blurb + all six control pods stack on top of each other
  at 390 px (screenshot-verified); wide pods clip off the left edge. Map render +
  bottom legend are fine; tap-to-inspect tooltips work on real devices. Separation
  seam is clean: render is shared (one WebGL canvas), but all chrome/layout is
  isolatable behind an `@media` block with zero desktop risk. Quick-pass order:
  (1) add the `@media (max-width:640px)` seam, (2) fix the top-third collision
  (collapse pods + shorten the blurb), (3) stop the left-edge clip, (4) re-render
  via `tools/profiling/shot-mobile.js` + real-device check. NOT greenlit for the
  approach yet (single scroll column vs bottom-sheet/hamburger — decide at step 2).
  - [x] ~~**DECIDE FIRST: control regrouping**~~ — **DECIDED 2026-07-23** (8
    decisions, `CONTROLS_MATRIX.md` §7 + `DECISIONS.md` "Controls & lens grouping").
    All 7 §5 combos closed. Final shape: `#views` = 5 (Money · Services · Ratio ·
    Uses · Development); Glass → mode of Money; Infill + Industrial → full-only Dev
    extras; palette + Labels → an accessibility menu; stack reordered
    View→Variant→Presentation; "Residential only" → "Highlight residential"; Dev
    grid+spike → one 3-way Detail selector. `public|full` tags all resolved in the
    same pass (public = Money/Services/Ratio/Uses/Development-activity; `/full/`
    adds Infill + Industrial + deep data-detail). **Nothing built yet.**
  - [x] ~~**BUILD ONCE: implement the 8 regroup decisions in `web/index.html`.**~~
    **BUILT 2026-07-23 (branch `regroup-build-s65`, NOT yet on master).** One reflow:
    the top stack is now a `#controls` flex column (tier order via `order:`), Glass
    is a 2-way Money "Detail" toggle (internal view unchanged), Dev grid+spike is one
    3-way Detail selector (Neighbourhood / 100 m grid — activity / Stock age), Infill
    is a full-only Dev *mode* (`#devmode`), Industrial is a full-only `#devmetric`,
    palette + Labels moved into a "Display" accessibility popover, `Residential only`
    → `Highlight residential`. `BUILD` flag (`public|full`, `?build=public` override)
    gates the two full-only controls. Full verify-`*`.js suite green in **both**
    builds; verify + shot scripts updated to the new controls.
    - [x] ~~**⚠️ merge gate: two-build deploy plumbing**~~ — **RESOLVED 2026-07-23**
      (same branch): the emit now rewrites `DEFAULT_BUILD → public` for the root
      copy, so merging `regroup-build-s65` to master ships the *public* controls to
      the site root. **Branch is now safe to merge** (review + merge is Peter's call).
    - [ ] **THEN mobile CSS** (below) reflows the *final* grouping (inherits the flex
      column + Detail selectors — the structure-before-mobile payoff). *Partly done:*
      move-1 shipped 2026-07-24 (`@media` seam, collapsing title, bounded control
      column) and the `#views` **size** half of the "under-reads as primary" concern
      is fixed 2026-07-25. **Still open: the `#views` POSITION question** — it's
      still a thin strip at the very top; that's the move-2 / bottom-sheet fork
      (`MOBILE_USABILITY.md` §3 + the top-bar note). Decide against the live render.
    - [x] ~~**Regenerate `docs/LENS_INVENTORY.md`** from the rebuilt wiring.~~
      **DONE 2026-07-25.** Rewritten from the code (not patched): two-build table,
      4/5 views with Glass as Money's `#moneydetail` mode and Infill as
      Development's `#devmode` lens, the three different "doesn't apply here"
      behaviours (`#toggle` hides / `#lens` hides / `#coloradj` greys), per-view
      data gates, combination counts, and a code-anchor table. Every row of the
      matrix was **probed against the live site** in both builds, not inferred.
    - [x] ~~**`CONTROLS_MATRIX.md` §2–§5 still stale.**~~ **DONE 2026-07-25.**
      §1–§5 rewritten against the probed live behaviour: 4/5 views with the two
      internal modes named, the Options-fold structure (T2+T3 both live inside
      `#optpanel`, folded by default ≤640px), corrected §4 rows, and a §5 split
      into **still-open (numbered 1–7)** vs **resolved-by-the-regroup (original
      letters kept, because `DECISIONS.md` cites "§5.G"/"§5.A/B"/"§5.F")**.
      §7 reframed from "not yet on master" to merged & live.
    - [x] ~~**Two stale code comments in `web/index.html`**~~ — DONE 2026-07-26,
      folded into PR #96 rather than spending a deploy on a comment-only diff.
      All three siblings now agree that `devGridOfferable` excludes **only**
      Industrial. `CONTROLS_MATRIX.md` §6 closed out.
  - [x] ~~**Two-build deploy plumbing (`PLAN_public_release.md` §2a).**~~ **BUILT
    2026-07-23 (branch `regroup-build-s65`).** `scripts/build_site.py` fans `web/`
    into one Pages artifact: `_site/` = public root (whole tree, `DEFAULT_BUILD` →
    `public`) + `_site/full/` = specialist (`index.html` only, `<base href="../">`
    so its `./data`/`vendor` resolve to the ROOT's shared copies — no GeoJSON
    duplication — `DEFAULT_BUILD` `full`, + a fixed work-in-progress badge). Wired
    into BOTH `deploy.yml` (system `python3`, stdlib-only → stays the fast code path)
    and `refresh.yml` (before `upload-pages-artifact`, `path → _site`), factored once
    as the shared script. `tests/test_build_site.py` guards the emit + that the
    source `DEFAULT_BUILD` literal exists (a drift fails `refresh.yml`'s pytest gate
    before deploy). Verified locally: both URLs smoke-clean. **`/full/` is unlisted,
    NOT access-controlled** (repo is public → nothing secret; the WIP badge is the
    mitigation).
  - [ ] **Selective/partial data regen (DEFERRED — `SPEC_deployment.md`
    "Two deploy paths").** Teach the *data* run which datasets a change needs so
    even a refresh skips untouched sources. Signal exists (`rowsUpdatedAt` per
    dataset; roads static 2+ mo while permits/fire change daily) but needs
    raw-file caching across CI runs, and the weekly cron sits right on GitHub's
    7-day cache eviction. Real payoff on slow static layers (roads/zoning), real
    fragility — separate project, not started.

- [ ] **PARKED: Regional comparison lens (St. Albert / Strathcona; Phase 2,
  not November scope).** Spike complete (PR #69, `docs/SPIKE_regional_lens.md`
  — read it first). Feasible in principle but blocked on: (a) **St. Albert
  licensing** — the LandScape REST service is not a catalogued open dataset
  and its bulk-query-ability is likely incidental, not licensed; needs direct
  confirmation from the City before any raw-data use; (b) Strathcona
  multi-unit dedup rule unsolved; (c) output design undecided beyond
  "citywide aggregate chart is the safe/realistic scope". **Do not commit
  St. Albert per-parcel data to the public repo under any circumstances until
  (a) is resolved.** (Strathcona licensing is clean: OGL-Alberta via
  catalogued open-data hub datasets.)

- [ ] **INDUSTRIAL & NON-RESIDENTIAL LENS FAMILY (NEW 2026-07-18 — full plan in
  `docs/SPEC_industrial.md`; read it first).** Two tracks: A = non-res
  decomposition inside the existing hood/grid frame; B = citywide-aggregate
  regional context from Alberta Municipal Affairs sources (OGL-Alberta,
  established fetch pattern — extends `fetch_fir_debt.py`; NOT the parked
  per-parcel regional lens above, which stays parked untouched). Tone rule is
  stricter here — descriptive only, see the spec. Build order A1 → A3 → A2 →
  B2 → B1 → B3:
  - [x] ~~**A1 — Non-res $ cut (greenlit 2026-07-18)**~~ — **SHIPPED
    2026-07-18** (`feat/nonres-revenue-metric`): `nonres_levy` = the slices
    billed at the Non Residential rate (COMMERCIAL + MA DERELICT + DESIGNATED
    IND PROPERTIES via `NONRES_RATE_LABELS`; exempt is $0, farmland its own
    class; identity `levy == res + nonres + farmland` tested) → fourth Money
    metric "Non-res $" + Glass grid columns (appended last). Real data: 47.4%
    of citywide levy; clamp $50k (p97.5 ≈ $48.4k); 34% of cells nonres > 0.
    `verify-nonres-revenue.js` ALL PASS; DATA.md §4 + UI.md. Live on the next
    weekly refresh (column guard until then).
  - [x] ~~**A3 — Industrial permit velocity (greenlit 2026-07-18)**~~ —
    **SHIPPED 2026-07-18** (`feat/ind-permit-velocity`, stacked on A1):
    `INDUSTRIAL_BUILDING_TYPES` (400-series, full-string — Parkade 490 is NOT
    industrial) → `ind_permits` count → `ind_permits_per_acre` (+ `_3yr`).
    Third `#devmetric` option "Industrial" — Development-view choropleth only
    (Detail toggle hides; Infill resets it to a residential metric + hides the
    button). Real data: 283 permits / 117 hoods (5yr). `verify-ind-permits.js`
    ALL PASS; DATA.md §10 + SPEC_development + SPEC_industrial A3. Live on the
    next weekly refresh (column guard until then).
  - [ ] **A2 — Shovel-ready industrial land:** `stt5-pzaa` verified 2026-07-18
    (annual snapshots 2016–2023, `servicing` field, centroids); absorption
    computable from snapshot diffs; display undecided.
  - [ ] **A4 — Assessment-lag methods note:** Nov 29 2024 council memo
    attachment (Table 1, permit→assessment 3–5 yr lag) — edmonton.ca fetch,
    likely Peter/laptop.
  - [ ] **B2 — Regional non-res mill rates:** `2026_Tax_Rates.xlsx` on the FIR
    page (verified live) + yearly workbooks; 6 municipalities; reviewed JSON.
  - [ ] **B1 — Regional non-res assessment share:** FIR/SIR + equalized
    assessment XLSX (2024–26 verified on open.alberta.ca — NOT PDF-only);
    rebuild the published-share-series discrepancy from primary data.
  - [ ] **B3 — Industrial-areas context map:** illustrative; municipal
    boundary layer source to verify.

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
  - [x] ~~**P1.2 In-app attribution/methods affordance**~~ — **DONE 2026-07-25**
    (PRs #94 + #95, both merged & live). Bottom-right `#about` pod above Display,
    labelled **`Data & Methods`**; the popover carries the City of Edmonton
    credit + Open Government Licence, the vintages, the modelled-not-billed
    caveat for revenue *and* the utility layers, and links to METHODS.md + the
    repo. **All years/dates come from `status.json`**, so the January year-roll
    can't strand a stale literal. `verify-about.js` (390/360/1440 overlap
    geometry, paint order, link resolution, a status.json-blocked run). It first
    shipped with the full credit AS the label; **reverted the same day** — 294px
    wide, it sat on the legend — and the collapsed-behind-a-button form turns out
    to be the map convention anyway (`UI.md` "What other maps actually do").
    Fixed three latent bugs on the way: `#botleft` swallowing pointer events, the
    z-index:1 paint-order collision, and `#legend` running under the right-hand
    column on phones. See `DECISIONS.md` 2026-07-25.
    - [x] ~~**Read the actual OGL – City of Edmonton text**~~ — DONE 2026-07-26
      (v1.0 July 2022, an adaptation of OGL–Canada 2.0). **Placement assumption
      confirmed: the licence says nothing about where attribution appears**, so
      the collapsed pod stands and the credit does NOT return to the map surface.
      But it caught two real gaps, both fixed the same day: (1) no link to the
      licence, which it asks for "where possible", and (2) the prescribed
      attribution sentence was paraphrased rather than verbatim. Added a
      non-endorsement line too (not required; the licence forbids implying
      official status). `docs/UI.md` "What other maps actually do",
      `DECISIONS.md` 2026-07-26. **P1.2 now has no open questions.**
  - [x] ~~P1.3 Public METHODS page~~ — done 2026-07-09 (PR #32 merged):
    `docs/METHODS.md` (metric definitions, denominators + guard, set-aside,
    WEM/condo worked examples, model formulas + validation ratios,
    limitations) + README Technical Docs link. P1.2 should link to it.
  - [x] ~~**P2.1 CI unmatched-set assertion**~~ — DONE 2026-07-11
    (`scripts/check_unmatched_names.py` + `data/expected_unmatched.json`, wired
    into `refresh.yml`; fails the build on a new money-path unmatched name). See
    the data-integrity audit §4 item below for scope detail.
  - [x] ~~**P2.2 Heartbeat PAT**~~ — DONE 2026-07-26, built as *two* halves
    because the PAT alone leaves the failure invisible when the PAT itself
    expires: (a) `refresh.yml` checks out with
    `${{ secrets.HEARTBEAT_TOKEN || github.token }}`, (b) the frontend ages
    `status.json`'s `last_checked` and raises the banner past `STALE_DAYS = 14`,
    (c) the commit step no longer swallows push failures green.
    `verify-staleness-banner.js`, `DECISIONS.md` 2026-07-26, `RUNBOOK.md` §3.
    - [ ] **Peter — one manual step left: create `HEARTBEAT_TOKEN`.** Fine-grained
      PAT, repo access `edmonton-tax-viz` only, Contents: Read and write, nothing
      else → repo Settings → Secrets and variables → Actions. Until it exists the
      workflow runs exactly as before (the fallback), so nothing is broken
      meanwhile — only the prevention half is dormant. Steps in `RUNBOOK.md` §3.
  - [x] ~~P2.3 Security/PII checklist pass~~ — done 2026-07-09 (Session 33,
    Fable audit): all boxes ticked/dated with evidence; scope updated to the
    Phase-2 static-site + CI surface. **Findings logged, not fixed** — see
    `docs/security-audit.md` "Findings — 2026-07-09" (S1–S6). Follow-ups:
    - [x] ~~**P2.3a Apply S1** (Medium): vendor maplibre-gl@4.7.1 + deck.gl@9.0.38~~
      DONE 2026-07-12 — vendored all three files into `web/vendor/`
      (`maplibre-gl-4.7.1.{js,css}`, `deck.gl-9.0.38.min.js`), `web/index.html`
      points at local copies (no CDN ref remains). Cross-verified vs jsdelivr,
      hashes in `web/vendor/README.md`; basemap is `sources:{}` so zero external
      runtime deps. verify-transit.js 24/24 against the vendored build. See
      security-audit.md S1 RESOLVED. (Branch `vendor/js-libs`, PR #40 merged.)
    - [x] **P2.3b Apply S3 + S4** (2026-07-12): S3 — added `esc()` helper and
      applied it to `neighbourhood_name` + `set_aside_reason` in `tooltipFor`
      (`web/index.html`); verify 24/24. S4 — SHA-pinned all four actions in
      `refresh.yml` (release version in trailing comment). Both → RESOLVED in
      `docs/security-audit.md`. Dependabot auto-bump left out (owner's call).
    - [x] **P2.3c S5 hygiene** (2026-07-12): bumped the 5 dev-freeze pins
      (tornado→6.5.7/bleach→6.4.0/soupsieve→2.8.4/jupyter_server→2.20.0/
      jupyterlab→4.5.9) + a 6th newer CVE found at fix time (mistune→3.3.0);
      `pip-audit -r requirements.txt` now clean. Added a **non-blocking**
      `pip-audit -r requirements-ci.txt` step to `refresh.yml`. → RESOLVED in
      `docs/security-audit.md` S5.
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
  - Click→panel annotation (no sidebar exists — interaction TBD) on **three
    specific named hoods only**, clearly labeled as a
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
  **Sources — VERIFIED 2026-07-15 (laptop), research half DONE.**
  - **PRIMARY: Report CR_2705, "IIMP – Cumulative Impacts," March 22 2016** (+ 20-pg
    Attachment 1). **Every figure verified against the primary tables** — see
    `docs/FINDINGS_iimp_growth_areas.md`: developer $3.806B (Drainage $2.351B +
    Transportation $1.455B); City/Province $1.362B (full 8-line Table 3 breakdown
    confirmed); ~$1.4B 50-yr cumulative shortfall (**distinct** from the $1.362B
    capital — do NOT conflate, both ~$1.4B by coincidence); areas Decoteau 1,960 ha/
    74,565/39yr, Horse Hill 2,793 ha/70,038/36yr, Riverview 1,435 ha/50,422/30yr;
    combined pop 195,025. All **2016$, projections at build-out, "received for
    information"**. PDFs saved `data/raw/iimp/` (gitignored). doniveson.ca archive
    reachable from Oracle too, so the BUILD (D2) is not laptop-gated.
  - **Currency check done:** the 2016 IIMP is NOT superseded per-area — the new
    CIO/OIO framework (2027–2030 budget) is a citywide 10-yr capital outlook, not a
    per-growth-area pro forma. Cite 2016 IIMP, date-stamped. → build = ticket D2.
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

- [ ] **GROWTH INFRASTRUCTURE FINANCING PANEL ("Debt Lens") — NEW 2026-07-14
  (brief: `docs/fable_brief_debt_lens.md`; scoped to these tickets same day).**
  From Peter's planning conversation; full research backing lives in claude.ai
  project knowledge (`Edmonton_Growth_Infrastructure_Financing__Feasibility...`),
  NOT in this repo — the brief is the authoritative in-repo doc. **Scope decision
  LOCKED (→ DECISIONS.md 2026-07-14): NO debt-per-parcel/neighbourhood map** —
  citywide debt isn't spatially attributable in public data. Two clearly-labelled
  components instead: (1) spatial growth-area financing transparency panel,
  (2) non-spatial citywide debt context. Framing = "financing transparency", NOT
  "debt attribution" — explicit in UI copy (load-bearing methodological claim).
  **Reachability probed 2026-07-14 (Oracle box):** doniveson.ca IIMP PDFs 200,
  open.alberta.ca FIR page 200 — D2/D5 data is Oracle-doable; only D0's bylaw
  map exhibit is edmonton.ca/laptop-gated.
  **⚠ INTERACTION PREREQ (all display tickets D1–D5-chart):** the app has **no
  sidebar** — there is no click→panel surface at all; interaction today is
  hover-tooltips only (S54 learning). Every "sidebar entry / extend the existing
  sidebar UI" phrasing below is aspirational shorthand from the brief, NOT an
  existing surface. **A new click→panel interaction must be designed and decided
  (Peter's call) before any D-series display work can start.** Read the phrasing
  below as "which content goes in that panel", not "add to a panel that exists".
  Tickets, build order:
  - [x] **D0 — catchment polygons BUILT 2026-07-15** (approximate, reviewable).
    `data/levy_catchments.geojson` (10 units) via
    `scripts/build_levy_catchments.py`; QA overlay + area validation confirm the
    footprints match Schedule A. Two flags for a future reviewer (editable
    `CATCHMENT_HOODS` dict): **Blatchford under-covers** (catchment > mapped
    hood) and **Riverview 1.65** (maybe drop `RIVER'S EDGE`). Full writeup:
    `docs/FINDINGS_offsite_levy_catchments.md`. Detail below ↓
  - [ ] **D0 detail — catchment polygon acquisition (RISK — source resolved
    2026-07-15; approach was Peter's call).** The 12 fire-hall off-site levy
    catchments (names/costs/rates tabled in the brief). Probed 2026-07-14:
    **NOT on data.edmonton.ca** (Socrata catalog: zero hits) **nor ArcGIS Hub**
    (every "off-site levy" layer there is Calgary's).
    **RESOLVED 2026-07-15 (laptop):** the ONLY published boundaries are a raster
    map exhibit — **Schedule A of Bylaw 19340** ("Fire Halls with Catchment
    Boundaries"), a JPEG in the bylaw PDF. **No GIS vector layer exists anywhere.**
    Bylaw text confirms boundaries are advisory ("subject to change… may adjust
    and refine over time"). Source artifacts saved to
    `data/raw/offsite_levy/` (bylaw PDF, ScheduleA JPEG, 2026 approved rates).
    Key enabling finding: Schedule A's catchment edges **follow the neighbourhood
    grid**, and all 12 catchments map to clusters of neighbourhoods we already
    hold in `neighbourhoods.geojson` (e.g. Blatchford→`BLATCHFORD AREA`,
    Walker→`WALKER`, Cumberland→`CUMBERLAND`, Big Lake→`ANTHONY HENDAY BIG LAKE`,
    Horse Hill→`ANTHONY HENDAY HORSE HILL` + the Horse Hill district). Three
    paths, decreasing effort / fidelity:
    1. **Trace/digitize** the raster (georeference + hand-trace 12 polygons) —
       highest fidelity, most manual; boundaries are advisory anyway.
    2. **Neighbourhood-union approximation** (RECOMMENDED) — build a
       neighbourhood→catchment assignment table by reading Schedule A, then
       dissolve. Reproducible from data we own, honest ("approximated to
       neighbourhood boundaries"), aligns with our neighbourhood-unit pipeline;
       error small because edges follow hood lines.
    3. **Table only** — per-catchment table + text list of member hoods, no map
       layer. Lowest effort, still honest, loses the spatial punch.
  - [ ] **D1 — levy performance mini-viz.** Cumulative levy collected vs the
    ~$26M single-facility cost, per catchment (simple bar/ratio — makes the gap
    immediate). Figures in the brief (2022–2024 annual reports; cumulative
    $3.83M end-2024, **zero halls levy-funded**). Use the 2024 **Table 6.1**
    figure ($3,033,592), footnote the exec-summary discrepancy ($3,259,866).
    Headline finding to make visually obvious: **Edmonton levies developers for
    fire halls ONLY** — no trunk roads/water/sanitary/storm levy (vs
    Calgary/St. Albert $170K–$270K/ha) — "1 of 5 essential services levied".
    Small manual dataset → reviewed JSON input (mill-rates pattern).
  - [ ] **D2 — IIMP financing split** (extends the Decoteau/HHR/Riverview
    annotation item above — primary source now located, Oracle-reachable). Add
    the developer-vs-City split to the Decoteau/HHR/Riverview click→panel content:
    developer $3.806B (drainage $2.351B + transportation $1.455B) vs
    City/Province $1.362B, net ~$1.4B 50-yr shortfall — 2016 projections,
    **label as projection, not actual**. **Needs the click→panel interaction
    decided first (see INTERACTION PREREQ above) — no sidebar exists yet.**
  - [ ] **D3 — Blatchford contrast case study.** 4th panel entry, same content
    pattern: the infill counter-example to the 3 greenfield areas —
    self-liquidating "debt recoverable" financing (Policy C597A), DESS
    district energy, $23.7M federal SREPs grant, own levy catchment
    ($32,813/ha, already in the D0/D1 table).
  - [ ] **D4 — sanitary trunk callout** (one-line panel text, NOT mapped —
    no clean basin boundaries confirmed): SSTC/EA charges paused May 2024;
    growth trunk sanitary currently funded from the accumulated ratepayer
    reserve, not active growth charges (figures in the brief).
  - [ ] **D5 — Component 2: citywide debt context chart (non-spatial).**
    Separate panel/chart, labelled "citywide, not neighbourhood-specific" —
    never a map layer. Headline 2025: $4.6B outstanding, 69% of the
    tax-supported debt-servicing limit (DMFP ≤18%/≤21% limits in the brief).
    - [x] **Data layer DONE 2026-07-14**: `scripts/fetch_fir_debt.py` →
      committed `data/fir_debt_series.json` — Edmonton + St. Albert +
      Strathcona County, **2003–2025** (a year further than the brief
      expected: the 2025 FIR is out, Edmonton total debt $4,592,150,000 =
      the brief's "$4.6B" headline, directly sourced). All four Schedule AA
      fields (debt + limits + servicing). Manual-reviewed-input pattern;
      anchor cross-checks + neighbour-band sanity; Strathcona-2013 $000s
      source quirk corrected + documented. DATA.md §11. +10 pytest (328).
      NB the FIR limit is the MGA regulation limit — Edmonton 2025 = 59.3%
      of it; the brief's "69%" is the DMFP servicing limit, a different
      denominator (quirk documented in §11).
    - [ ] **Display/chart** — undecided design (where does a non-map panel
      live in the UI?); Peter's call before building.
  - **Out of scope (locked in the brief):** any spatial allocation of the
    $4.6B; S&P rating detail / CCBF/MSI/LGFF; Local Improvement levies
    (genuinely parcel-level but not open data — future phase, needs
    FOIP/per-bylaw scraping).

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

- [ ] **DEVELOPMENT & INFILL LENS family (NEW 2026-07-12 — full plan in
  **⚠️ Stock age was WITHDRAWN from this lens 2026-07-27** (Peter: not
  working well as an option) — see `DECISIONS.md`. The UI and render path
  are gone and `verify-age-spikes.js` is deleted, but `median_year_built`
  still ships in `value_grid.json` and
  `FINDINGS_stock_age_spike_scaling.md` still holds the scaling work, so
  a different presentation would not start from zero. Anything below that
  assumes a 3-way Detail selector is stale.
  `docs/SPEC_development.md`).** Permit-based "where is building actually
  happening" lens family, the direct answer to what `FINDINGS_growth_servicing.md`
  could only proxy with median building-stock age. Data verified live 2026-07-12:
  General Building Permits `24uj-dj8v` (243k rows, 2009→now; has `units_added`,
  `work_type` new-vs-reno, `building_type`, `neighbourhood` UPPERCASE-matches-ours,
  lat/long, `construction_value`). Build one minimal cut of each lens to *see it*
  before designing the next. Three locked decisions (Peter, 2026-07-12) →
  DECISIONS.md: (1) activity = choropleth, (2) infill = suitability×activity
  mismatch shown both ways, (3) combined cost side = city service cost (not
  permit construction_value).
  - [x] **Lens A — Building Activity (choropleth), PHASE 1 / first cut. DONE
    2026-07-12** (`feat/dev-lens-a-building-activity`). `src/load_permits.py`
    (slim `$select` download, count cross-check hardened for the `count_1`
    alias) → new-construction `work_type` ∩ residential `building_type`
    (hand-enumerated dicts incl. every spelling variant, warn-on-unseen) → Σ
    `units_added` per hood → `join_and_calculate` column (`validate="m:1"`,
    warn-not-fail) → new **Development** web view (own view, NOT a city service;
    `new_units_per_acre`, 2021–2025 pinned, sqrt colour). **Set-aside override
    LOCKED = full override coloured** (empirically low-impact: 6 hoods/43 units;
    growth hoods sit below the 0.90 threshold — the S42 "headline tension" was
    overstated for current data). `NAME_CORRECTIONS` resolves CHAPPELLE AREA etc.
    (only GLENORA,ROSSLYN 1-unit straggler left). DATA.md §10 added; 308 pytest +
    `verify-development.js` 25/25 green; screenshot eyeballed. Live-data: 59,696
    units / 236 hoods, GARNEAU tops per-acre (dense infill).
    - [x] **Lens A polish — permit-count sub-metric** (2026-07-13): pipeline
      `new_permits_per_acre` column + web `#devmetric` units/permits picker
      (project density vs dwelling supply); ABBOTTSFIELD 248 units / 2 permits is
      the extreme case. 308 pytest + `verify-development.js` 31/31 green.
    - [x] **Lens A polish — window toggle** (2026-07-13): second pinned window
      `PERMIT_YEARS_RECENT` (3yr, 2023–2025) alongside the 5yr base →
      `_3yr`-suffixed columns + web `#devwindow` 5yr/3yr picker (both metrics),
      gated on the `_3yr` columns. 311 pytest + `verify-development.js` 40/40 green.
    - [x] **Lens A — long "Since 2009" window** (2026-07-21, from the inspiration
      lens = cumulative "homes added 2009–2023" density-in-the-core map): third
      `#devwindow` option (2009–2025), `PERMIT_YEARS_LONG` → `_long` columns for
      all three metrics. ANCHORED (2009 start pinned, end derived from
      `PERMIT_YEARS[-1]` → auto-extends on the January bump). ~160k units citywide
      vs 60k/39k. **First-class window** (2026-07-22): drives the choropleth AND
      its own 100 m detail-grid spikes (`units_long` cells) — the initial
      choropleth-only cut was reverted once the data showed early-year geocoding
      is fine (2009–2023 at 95–98%; the lag is the NEWEST permits, so the long
      grid is the best-covered of the three at 84%). DECISIONS + SPEC_development
      "Activity window" + DATA.md §9. 402 pytest + `verify-development.js` (+11
      long-window checks incl. the long detail grid) + age/ind regressions green;
      choropleth + spike-map screenshots eyeballed.
    - [x] **Lens A 100 m detail grid** (2026-07-15, Peter: "add them as a layer
      switch this time... may want to move the others to this style later"):
      layers-panel "Detail" toggle in the Development view swaps the choropleth
      for the Glass composition — neutral plane + 100 m geocoded-permit spikes
      (`load_permits.export_dev_grid` → `web/data/dev_grid.json`, 4,105 cells;
      permits `$select` now fetches lat/long). Linear height / sqrt colour,
      driven by the existing pickers; geocode-lag coverage (~21% of 5yr units
      not yet mapped) written into the JSON + disclosed in the blurb.
      DECISIONS 2026-07-15; SPEC_development "Lens A detail grid";
      verify-development 54/54; +6 pytest (334).
    - **Lens A polish (remaining):** the `occupancy_granted_date` completed-builds
      variant (DATA.md §10 — only populated residential ≥2022 / non-res ≥2024).
  - [ ] **Lens B — Suitability × Activity mismatch, PHASE 2.** Signed diverging
    metric `z(suitability) − z(activity)`: two views off one scale — suitable-
    but-quiet (opportunity) AND less-suitable-but-building (Peter's flip).
    - [x] **Suitability proxy LOCKED 2026-07-13 (Peter): built FAR** (`far` = Σ
      floor area ÷ deduped lot area/hood; low FAR = underused). Backend column
      DONE — `load_property_info` loads `gross_area`, `build_hood_lot_acres`
      emits `far`, `join_and_calculate` carries it into geojson + SLIM
      (unsuppressed by LOW_PARCEL_FRAC); +7 tests, 318 green. DECISIONS.md +
      SPEC_development Lens B + DATA.md §2.
    - [x] **Web `Infill` diverging view DONE 2026-07-13:** `z(suitability) −
      z(activity)` = `−(z(far)+z(activity))` computed live (responds to the
      units/permits × 5yr/3yr pickers); one dark-centred diverging plane (teal =
      suitable-but-quiet, orange = building-where-less-suitable), set-aside
      EXCLUDED from the z population (358 hoods kept). DECISIONS + SPEC_development.
    - [x] **Asymmetric residential opportunity gate DONE 2026-07-13:** a prototype
      showed the planned maturity gate (median `year_built`) DOESN'T fix the
      opportunity end — the pollution is structurally-low-FAR *non-residential*
      land (industrial/fringe, all decades), not new suburbs. Fix: non-residential
      hoods barred from the teal opportunity end (grey) but kept on orange/pressure
      + in the z population (keeps DOWNTOWN). Web-only, no new pipeline column
      (`infillOppSuppressed`). `verify-infill.js` 41/41. DECISIONS + SPEC_development.
    - [x] ~~**Lens B per-arm colour scaling (REOPENED 2026-07-14, handed to Fable).**
      S48 audit: the mismatch score is structurally asymmetric (suitability capped
      +0.97, activity unbounded) so the symmetric p95 clamp leaves the teal arm
      unable to saturate (0 teal vs 18 orange saturations) + median hood on the
      +0.5 verdict line. Fix (web-only): clamp each arm at its own p95 + verdict
      cut-points in `t` space. Brief: `docs/FABLE_infill_perarm_scaling.md`~~ —
      done 2026-07-14 (Fable): `clampPos`/`clampNeg` in `infillStats`, per-arm
      `infillT`, verdict cut at `t = ±0.4`; `verify-infill.js` 44/44; live on the
      next `refresh.yml` run.
    - [ ] **Lens B optional refinement (future, low priority):** one-sided
      opportunity/pressure choropleth toggles (the single diverging map already
      shows both). SPEC_development Lens B.
    - [ ] **Lens B fine-grain "Infill detail" (assessed 2026-07-14, not yet
      decided):** the z-mismatch SCORE doesn't survive 100 m grain (~88% of
      inhabited cells have zero 5yr activity — every quiet cell would read
      "opportunity"; set-aside/residential gates are hood-level constructs).
      The honest fine-grain version is the DECOMPOSED ingredients: a per-cell
      FAR texture (per-point `gross_area` + `_point_lot_stats` lot dedupe —
      `build_hood_lot_acres` keyed on cell instead of hood) under the Lens A
      permit spikes (now shipped), verdict stays hood-level. Middle path if a
      finer score is ever wanted: prototype 250–500 m cells first. Needs
      Peter's call before building.
  - [ ] **Lens C — Activity vs City Service Cost, PHASE 3 / future.** Where new
    building goes vs modeled city service columns (road/storm/water/fire per acre)
    or V2 unit-cost $/acre (laptop-gated). Two-ledger idiom of
    FINDINGS_growth_servicing made spatial. `construction_value` NOT used here.
    Depends on Lens A + V2 unit costs.

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
    - [ ] **V2 — combined "modeled city service cost per acre".** One
      denominator = road metres × roadway O&M+renewal $/m/yr + fire events ×
      (Fire Rescue operating budget ÷ citywide dispatches). Labeled MODELED,
      "roads + fire only", never "total city cost". Design locked in
      SPEC_utilities decision 3.
      - [x] **Unit-cost source hunt DONE 2026-07-15 (laptop)** — the
        laptop-gated half. `data/city_unit_costs.json` (reviewed input,
        mill-rates pattern): **roadway $50/m/yr** (edmonton.ca Development
        Impact page: $600k O&M + $1.9M renewal per km ÷ 50-yr life; Peter's
        50-yr call; 3%-of-value cross-check ≈ $45) + **Fire Rescue 2026 gross
        operating budget $276.706M** (2026 Approved Operating Budget PDF; net
        $273.598M). Provenance + caveats in the JSON.
      - [x] ~~**Build the composite metric (Oracle-doable).**~~ — done
        2026-07-15: `load_unit_costs` + `unit_costs` arg in
        `join_and_calculate` → `svc_cost_per_acre` = road_m_per_acre ×
        $50/m/yr + fire_events_per_acre × (budget ÷ the fire frame's OWN
        citywide kept-event total, pre-join — unmatched fire hoods stay in
        the denominator). Requires BOTH roads + fire (warn+skip otherwise —
        a one-term composite would be mislabeled). In `SLIM_COLUMNS`, so
        the column ships with the next refresh run (code-only PR; the
        local raw snapshot is older than the live auto-refreshed data,
        so no regenerated GeoJSON was committed). +9 pytest (351).
        Real-data run verified: **$3,142/event** ($276.706M / 88,065 kept
        events/yr), composite on all 406 exported hoods, median
        $3,302/acre/yr (fire-dominated downtown ~$34k, road-dominated
        suburbs ~$3.4k — the allocation caveat is visible in the data).
      - [ ] **Display (UI) for the composite** — **DECIDED 2026-07-16
        (Peter): BOTH, staged** (Services checkbox first, then a Ratio-view
        coverage denominator). Carry the fixed-budget-allocation + "roads +
        fire only, never total city cost" caveats in copy.
        - [x] ~~**(a) Services-view checkbox**~~ — BUILT 2026-07-16
          (`feat/v2-svc-cost-display`): 6th per-service row "Service cost
          (roads+fire) — modeled $/acre" on the shared `svc-plane` (SERVICES
          `servicecost`, sqrt colour), blurb + legend + tooltip with both
          caveats, column-guarded (hides until the column ships on the next
          refresh). `verify-services.js` + `shot-services.js` extended;
          screenshot eyeballed (fire-heavy core bright, greenfield grey).
        - [x] ~~**(b) Ratio-view coverage denominator**~~ — BUILT 2026-07-16
          (`feat/v2-svc-cost-display`): 3rd "Ratio denominator" option "Per
          service $" = revenue ÷ modeled roads+fire cost (dimensionless).
          **Magnitude, not break-even (Peter): same log ramp, no 1.0
          marking; median ≈5.8× so blurb/tooltip own "not a sign the land
          pays its full way".** ×-format legend bounds, $230/acre floor,
          picker opens on hasFire||hasSvcCost, button column-guarded.
          verify-ratio-denom 38/38; screenshot eyeballed.
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
  - [x] ~~**Heartbeat watch:**~~ DONE 2026-07-26 — didn't wait for it to sleep;
    added the repo-scoped PAT (with fallback) *plus* a client-side staleness
    banner. Same item as P2.2 above; see there for the remaining manual step.
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

- [ ] **STAGE 2 of the `web/index.html` split — the JS into ES modules (NOT
  started, and deliberately deferred).** Stage 1 (CSS → `web/styles.css`) shipped
  2026-07-29, PR #116; see `DECISIONS.md` that date for the full reasoning.
  Remaining: ~3,300 lines of JS in one block with **nine existing section
  banners** (tunables, services lens, uses view, services view, base map,
  development detail grid, infill lens, reference layers, money view) — the
  structure is already latent, it just isn't expressed as files. Native ESM
  (`<script type="module">` + relative imports) needs no bundler and works on
  Pages.
  - ⚠️ **Do NOT justify this on token savings — that was measured and is false.**
    See `docs/TOKEN_EFFICIENCY.md` "Files to watch". Justify it on navigability,
    grep precision and blast radius, or not at all.
  - ⚠️ **`DEFAULT_BUILD` must stay in `index.html`** — `scripts/build_site.py`
    regexes it there and hard-fails on anything but exactly one match. If the JS
    moves, that literal stays behind or `build_site.py` moves with it.
  - ⚠️ **11 verify scripts reference `index.html` directly** — that is where the
    risk lives, and why this is a separate stage.
  - **Gate: wait until stage 1 has actually helped** (the mobile-chrome work in
    `MOBILE_USABILITY.md` §3 is the first real test of it). Don't do stage 2
    speculatively.

## Done

Closed items moved out of `## Open work` on 2026-07-30 live in **`docs/TODO_archive.md`** — one line each below, reasoning there.

- [x] **PROMOTED the temporal + change lenses to the PUBLIC build — DONE 2026-07-31 (PR #121, merged `828bb5a`, deploy green, LIVE).** — DONE 2026-07-31 · `docs/TODO_archive.md`
- [x] **ALL THREE PRE-EXISTING VERIFY FAILURES ARE FIXED (2026-07-31). THE SUITE IS GREEN: 26 scripts, 0 failures.** — 2026-07-31 · `docs/TODO_archive.md`


Closed items moved out of `## Open work` on 2026-07-30 live in **`docs/TODO_archive.md`** — one line each below, reasoning there.

- [x] **ASSESSMENT-OVER-TIME GRAPH PER NEIGHBOURHOOD** — COMPLETE 2026-07-29 · `docs/TODO_archive.md`
- [x] **TEMPORAL, ROUND 2 — "HOW MUCH HAS EACH HOOD CHANGED?" AS A MAP METRIC, WITH SELECTABLE WINDOWS (Peter, 2026-07-30).** — BUILT 2026-07-30 · `docs/TODO_archive.md`
- [x] **UI: the pinned panel and the hover popup must not both be up — add an explicit MODE toggle** — DONE 2026-07-30 · `docs/TODO_archive.md`
- [x] **NEEDS A PHONE, NOT A BOX: confirm the double-tap-zoom fix (PR #107).** — 2026-07-27 · `docs/TODO_archive.md`
- [x] **LABEL SWEEP IS BLIND TO DOM CHROME.** — DONE 2026-07-27 · `docs/TODO_archive.md`
- [x] **PUBLIC BUILD SHAPE** — LOCKED 2026-07-28 · `docs/TODO_archive.md`
- [x] **RIVER GEOMETRY IS UNTRIMMED AND UNCHECKED (audited 2026-07-27).** — CLOSED 2026-07-27 · `docs/TODO_archive.md`
- [x] **FLAKY TEST: `verify-uses-prisms.js` "money: control hidden again, state kept" (found 2026-07-27).** — CLOSED 2026-07-28 · `docs/TODO_archive.md`
- [x] **SMALL OPEN UI DECISIONS (2026-07-25).** — CLOSED 2026-07-26 · `docs/TODO_archive.md`
- [x] **Residential revenue metric ("Residential $", Peter 2026-07-16)** — SHIPPED 2026-07-16 · `docs/TODO_archive.md`
- [x] **Dev+Infill ROUND-2 delta audit** — EXECUTED 2026-07-16 · `docs/TODO_archive.md`
- [x] **PRIORITY — Lot-acre denominator TOGGLE on the neighbourhood (first) lens (NEW 2026-07-08, out of the cardinality audit below).** — BUILT 2026-07-08 · `docs/TODO_archive.md`
- [x] **PRE-LAUNCH AUDIT — record-to-parcel cardinality bug (WEM numerator + condo denominator) & lot-acre vs ground-acre methodology (NEW 2026-07-08).** — CLOSED 2026-07-09 · `docs/TODO_archive.md`
- [x] **Neighbourhood labels — finish + ship** — SHIPPED 2026-07-04 · `docs/TODO_archive.md`
- [x] **Ghost prisms over a neutral hood plane (Peter, 2026-07-03; design clarified 2026-07-04).** — SHIPPED 2026-07-05 · `docs/TODO_archive.md`
- [x] **PRIORITY — Lot-size denominator variant for the grid spikes** — SHIPPED 2026-07-05 · `docs/TODO_archive.md`
- [x] **SCOPE: composition numbers now; full zoning POLYGON layer in the viewer is a SEPARATE later product decision** — 2026-07-03 · `docs/TODO_archive.md`
- [x] **UI control hierarchy: separate "Color Adjustment" from lens controls.** — BUILT 2026-07-07 · `docs/TODO_archive.md`
- [x] **Deployment — LIVE (2026-07-01/02)** — 2026-07-01 · `docs/TODO_archive.md`


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
