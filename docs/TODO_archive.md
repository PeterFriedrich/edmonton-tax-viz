# TODO — archive of CLOSED items

Closed work moved out of `TODO.md` so the file that is read at the start of **every** session carries only live work. **Nothing here is a to-do.**

`TODO.md`'s `## Done` section keeps a one-line entry for each of these, so the *never redo a closed item without asking* rule still works by grepping there; this file holds the reasoning behind each one.

Items are verbatim as they were closed, newest-moved first in the order they appeared in `TODO.md`. Line numbers and "next up" markers inside them are historical — do not act on them.

---

- [x] **Manifest staleness guard — BUILT 2026-09-17 (S167), on Peter's yes.**
  The original item proposed ONE function; it shipped as TWO, because the digest
  renders one row per check and folding two sources into one cell prints two
  unrelated verdicts side by side.
  - **`check_budget_context`** — `city_budget_context.json` is hand-maintained
    and feeds published dollars on all 18 About-panel surfaces through
    `status.json`, and nothing recurring read it
    (`docs/FABLE_AUDIT_published_numbers.md` §3: *the world moves and the file
    does not, silently, forever*). Three parts: a newer published `Tax Supported`
    FY than the pod's `year`; the two pinned FY2017 program lines re-derived; the
    snow cross-check against the published program. **Fired ACTION on its first
    live run** — FY2026 $4,045,178,891 vs the pod's FY2025 $3,845,555,000.
  - **`check_mill_rate_values`** — the pinned year's rate VALUES against
    `pwis-wc4c`. ⚠️ `check_mill_rates` compares the SET OF YEARS only, so a rate
    **republished for a year we already hold passes it silently**. Green on the
    first run: all 15 2026 rates match exactly; Farmland municipal is carried
    locally with nothing published, as its own `_assumed` note says.
  - ⚠️ **Every pinned figure is a (program, year) PAIR, never a name followed
    across years.** `Roadway Maintenance` and `Snow and Ice Control` are FY2017
    ONLY; from FY2018 the latter is `OPS/PARS - Snow and Ice Control`
    (`data/DATA.md` §17's era trap). A name-only sum would read a rename as a cut.
  - ⚠️ **NOT a content fingerprint like `check_capital_budget`** — the file is
    approved but not frozen (FY2026 republished between 2026-09-05 and 09-15,
    7,283 → 7,294 rows, FY2025 byte-identical). Hashing it would call that a
    budget change.
  - ⚠️ **A newer FY is a PROMPT, NOT A DEFECT** — the FY2017 roads-only vintage
    is a decision (`docs/DECISIONS.md` 2026-08-04). The message says *re-confirm
    the vintage, do not bump the year alone*, and a test pins that wording.
  - **13 falsification tests; 6 mutations, each caught by the right test.**
    ⚠️ **The era-trap test was VACUOUS on first write** — its fixture used the
    RENAMED programs, so deleting the year pin changed nothing and it passed
    under the bug. Rewritten to republish the SAME name in a later year.
    (`check-where-the-value-can-be-wrong`, instance 8.)
  - `scripts/vintage_report.py`, `tests/test_vintage_report.py` (+20).

- [x] **Residential-only lens — SUPERSEDED, and the built version was REMOVED.**
  ⚠️ **Verified 2026-09-16: do NOT rebuild this.** Every sub-item below shipped,
  and the fade lens was then deleted 2026-07-26 as redundant with the Residential
  revenue cut (`DECISIONS.md`; `state.residential` and `#lens` are gone from
  `web/index.html` — 0 occurrences). The goal — a residential-to-residential
  comparison — is met by the Residential metric, not by fading prisms. Original:
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


- [x] **Colour scale for revenue/value — SUPERSEDED 2026-09-16.** The clamp
  question this item asks was decided that day: the ground-acre clamps STAY
  hand-set literals (the lot and grid scales already track a live p97.5), and
  the drift is guarded instead — `scripts/check_colour_clamps.py` fails the
  merge gate if the legend and the clamp disagree, and warns each refresh when
  the saturating share leaves 1–6%. ⚠️ **The "saturated plateau" this item calls
  a fake threshold was re-measured 2026-09-16 and is real and deliberate**: the
  tail is 5.1× the clamp (DOWNTOWN $256,564), so no clamp choice separates the
  top hoods. `DECISIONS.md` 2026-09-16. Original text:
  clamp ($50k / $4M, ~p97) creates a visible saturated plateau that reads as a fake
  threshold. Once exempt is split, re-run the skew check on the status-defined
  taxable set: if it's ≈ log-normal (likely), use `log` for the taxable scale; `sqrt`
  is the fallback if it stays mixed. Height stays LINEAR (locked honesty choice).
  *Colour ramps in `web/index.html`:* 3 swappable ramps (Inferno / Glow /
  Cividis) + palette switcher. **Default = Inferno (picked 2026-07-01).** Cividis
  retained in the switcher as a liked alternative + the colourblind-friendly
  option (see Visual polish → colourblind (cividis) mode below).
  *Not yet built:* scale toggle (linear+clamp / sqrt / log) for visual comparison.


- [x] **`$50k` revenue clamp — DECIDED AND GUARDED 2026-09-16 (S162).** Peter's
  call: it stays a **stability literal** (the lot and grid scales already track a
  live p97.5; the landing view must not). `scripts/check_colour_clamps.py` splits
  the two failures — legend-must-decode-to-clamp **fails the merge gate** (falsified:
  the clamp moved to $5,000 under a `$50k+` legend with all 923 pre-existing tests
  green), saturating-share-outside-1–6% **warns each refresh and files an issue**.
  The band contains today's 4.5% deliberately; it catches the next move.
  `DECISIONS.md` 2026-09-16, Findings §5.

- [x] **Services lens — road supply — SHIPPED (verified 2026-09-16:
  `road_m_per_acre` is served on all 406 hoods, the roads ground layer and
  Services view are live, and 13 `DECISIONS.md` rows cite `SPEC_services.md`).**
  Every sub-item below was already checked; the parent was not, and the branch
  `feature/services-lens` has long since merged and been deleted — which is how
  the digest's `TODO branch refs` check found it (`RUNBOOK.md` §0d).
  Original scope (SPEC'd 2026-07-01):
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
    - [x] (1) Roads ground layer — both children done 2026-07-02; box never
      ticked (verified 2026-09-16: `web/data/roads.geojson` is served):
      - [x] ~~pipeline: slim `web/data/roads.geojson` export (dissolved per
        hood × arterial/access, simplified 8 m, 5 dp)~~ — done 2026-07-02
        (`export_roads_web` in `src/load_roads.py`, wired into `main.py`;
        791 features, 2.3 MB, committed like the polygons file; +5 tests).
      - [x] ~~frontend: layers panel, lazy-loaded ground layer; arterials
        neutral, access roads coloured by hood `road_m_per_acre` (linear,
        clamp 53); remove Roads from metric toggle~~ — done 2026-07-02
        (headless-verified; details in UI.md "Services views").
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


- [x] **Nothing verifies the Services panel** (the T1 gap) — **CLOSED 2026-09-15,
  PR #398 then #399.** Written and merged RED against the broken build (7 checks
  failing), falsified both ways, green after the fix. `## Done`.

- [x] **Published numbers with no loud check — audit EXECUTED 2026-09-15 (S160,
  Fable 5.1).** `docs/FINDINGS_published_numbers.md`; ledger row. Instrument fixed
  first (Money view was never captured; public over-counted by 18 unreachable
  claims). Every manifest value still matches its source; **nothing recurring
  would say so if it stopped** — falsified: `year` 2025→2019 and a wrong 2026 mill
  rate propagated via `generate_status.py` both pass 892 tests + every merge-gate
  guard. Follow-ups below, **nothing built**.

- [x] **L1 + L3 of the three unguarded PUBLIC literals — CLOSED 2026-09-16 (S160),
  PR #406.** Two `check_cost_copy` CLAIMS rows now read `$600,000` / `$1,900,000`
  from `roadway_om_renewal.source`, and the Infill blurb renders `WIN_SHORT.permits`
  while `test_window_labels` matches **both** year spellings. Falsified six ways with
  a green control on both ends; rendered output checked on the public build. `## Done`.

- [x] **Retrieval logging — EXECUTED 2026-09-16 (S160).** `Read|Grep|Glob`
  `PostToolUse` hook in `.claude/settings.json` → `~/.claude/retrieval-log.jsonl`;
  read it with `python tools/retrieval_report.py`. Proven firing (a real Read logged
  with this session's id). ⚠️ **Harvest no earlier than ~2026-09-30** — the report
  refuses to be treated as evidence under 14 days. This is rec #1 of
  `docs/external/REVIEW_doc_apparatus_2026-09-15.md`.

- [x] **Doc-apparatus audit — EXECUTED 2026-09-16: Session A (S161) `_PREMISES.md`, Session B (S162) `_DISPOSITIONS.md`; recs 1/2/6 wait on the log (~2026-09-30), rec 3's `$50k` clamp and recs 4/5's restructuring are Peter's.**
  `docs/FABLE_AUDIT_doc_apparatus.md`, ledger candidate 11. ⚠️ **Scoped against the
  failure of the last attempt**: the review was digested to one sentence, 1 of 9
  recommendations carried, 314 lines of prose and zero checks shipped. §3's output
  constraint is the correction — disposition per row, a `TODO.md` park counts as NOT
  disposed, write-up capped by the code it changes. Recs 4/5/7/8/9 are answerable
  now; 1/2/6 wait on the log. ⚠️ **Cross-model does not fix this one** — Fable ran
  the failed attempt. ⚠️ **TWO SESSIONS (§0a): A evaluates the review's premises and
  STOPS at a handover; Peter names the live rows; B disposes them.** Running both at
  once is the model acting on its own evaluation unchecked.

- [x] **T2 — `#devwindow` is the only one of Development's three sibling pickers
  that does not reach the panel.** `#devmode` and `#devmetric` both do; every
  other readout follows all three. ⚠️ **Answer "is `renderDevHistory`
  deliberately all-time?" BEFORE touching the wiring** — if it is, the defect is
  copy (a `COPY_DECISIONS.md` row), and the cheap wiring fix would silently
  redefine a published number.
  - **CLOSED 2026-09-15 (S159, Fable 5.1).** It is deliberately all-time:
    `DECISIONS.md` 2026-09-14 makes the panel the whole per-year series and the
    windows aggregates over it; `devHistoryFor` reads only the metric key. The
    copy remainder is `COPY_DECISIONS.md` F4. `docs/FINDINGS_controls_state_space.md` T2.

- [x] **`tools/todo_archive.py` swallowed trailing non-item text — FIXED 2026-09-10 (S154).** An item now ends at the first unindented non-item line; runs no longer add blank lines; `tests/test_todo_archive.py` (4 tests, 3 red against the old tool by name). Replayed on the real 2026-09-10 case: 40 lines moved, heading and notes kept. Original item follows.
  - Found 2026-09-10 (S154) closing the send-back-brief item: it took the `_Last reconciled: 2026-09-01_` block, the `### General backlog` heading and its paragraph with it (66 lines for a 39-line item) — an item's span runs to the next `- [ ]`/`- [x]`, not to the next non-indented line. Reverted and moved by hand. **Until fixed, diff every run** (`git diff -U0 TODO.md | grep '^@@'`): CLAUDE.md points sessions at this tool for bulk closes.


- [x] **SENT — the follow-up brief went out (Peter confirmed 2026-09-10, S154; send date not recorded). Reply pending; the Q1 hold stays until Q1(a) answers.** Original item follows.
  - **PETER TO SEND — the follow-up brief is written and unsent.**
  `/home/opc/research/edmonton-tax-viz/road_cost/road_cost_sendback_brief.md` (**outside the repo**, same as the Q8
  addendum). Written 2026-09-03 (S136) for the next external research pass. It
  carries: **six corrections** to the last round (the 3% rule is not an
  independent cross-check; the year-late Taproot date; the composite-profile
  undercount; Table 8 exists; the adopted-vs-adjusted vintage trap; the endpoint
  was not a discovery), **six ranked questions**, the §4 NRP measurement, and a
  **§6 correcting the follow-up road-per-dwelling task** — three things already
  built, four wrong premises (including that this project has **no
  population-by-hood source at all**), and what measuring it actually showed.
  ✅ **REVISED 2026-09-09 (S150) — the brief is now current and ready to send as
  written; nothing further is needed from a model.** The retired $1,285 ran
  through **four** places, not the one the S149 handoff flagged, and all four
  are fixed: §1's holdings line, §1's derived-rate table (now $5,970 + $3,350 =
  **$9.32/road-m/yr**), §2.2's verification note, and Q1. **Q1 and Q2 swapped
  priority.** Q1 is now the **lane-km unit + the arterial ratio k**; Q2 is the
  old scope question ($600k and the FY2017 `Roadway Maintenance` program),
  carrying the warning that the size *and direction* of the $12-vs-$9.32 gap
  depend on Q1(a) — 1.29× on the shipped basis, **1.4–1.7× the other way** per
  centreline metre. Still six questions; Q3–Q6 untouched.
  ⚠️ **Q1(b) is the one that matters: `k` is the single free variable in a
  caveat now LIVE on the map** (*a floor unless arterials cost more than ~3.3×
  a collector/local lane-km*). ⚠️ **The brief now declares its own weak
  provenance** — both constants in that formula (arterials **35%** of road
  lane-km, and the **1.80**) come from ONE secondary relay of the City's 2020
  Infrastructure State & Condition figures **whose blog is 404** — and asks for
  that table from a primary source as a third retrieval. It also warns the
  reader that the source we derived from (Taproot 2025) says **"linear
  kilometres"**, which we believe is a relay error; establishing the unit from
  the City rather than a reporter is the job. **Three retrievals are asked for
  because they fail from this box:** the Taproot **2022-05-31** alley brief (we
  hold the date and quote but **no URL**, and it is half the cross-check),
  the Winter Roads FAQ (**403**), and the 2020 class lane-km table.
  - ⚠️ **The brief opens with a "what we already hold, do not re-derive"
    section.** The last round spent most of seven questions restating
    `city_unit_costs.json` in less detail; that section exists to stop it
    happening twice, and it is the part to keep current if the brief is reused.
  - ⚠️ **Grep before applying anything it returns** — relayed research invents
    file names and sources, and produced a year-late date in the last batch.

- [x] ✅ **DECIDED 2026-09-08 — STATE THE UNIT, DO NOT CONVERT: `roadway_ops` stays $9.32/m/yr and the basis publishes as a FLOOR** (Peter: *"let's choose the floor for now. We may link directly to an external analysis I'll do later"*). Both conversions declined — ×1.80 rests on a secondary 2020 relay now 404, ×2.19 charges alleys nothing, and rates here come from named City publications, not an audit's arithmetic. ⚠️ **The floor is now ARITHMETIC under a stated k** (net ≥ 1.06× for an arterial-to-local cost ratio k ≤ 3; flips only at k > 3.3), and the 5.4× lifecycle gap must not be read as a fact about a road metre (~2.5–3× per centreline metre). Three public copy sites say *per lane-kilometre*; served columns unchanged; `DECISIONS.md` 2026-09-08. Original item follows.
  - **PETER'S CALL — the operating road rate is DOLLARS PER LANE-KILOMETRE applied to CENTRELINE metres (S149 consolidation audit, `docs/FINDINGS_road_figures_consolidation.md` L2b).** The "~11,000 km" under both halves of `roadway_ops` ($5,970 maintenance + $3,350 snow) is the City's snow-and-ice inventory, which the City states in **lane-km** and which includes ~1,300 km of alleys; the City's own centreline feed (`data/raw/roads.geojson`, the file `load_roads` reads) holds **5,029 km of City road centreline** (1,358 arterial / 926 collector / 2,740 local) + 1,311 km alleys. Taproot's *"linear kilometres"* is the only source saying linear, and it is wrong. **Direction known: the shipped $9.32/m understates by 1.8–2.2× per centreline metre** (1.80 on the 2020 class lane-km ÷ feed centreline for collector+local; 2.19 on the feed's 5,029 km alone). The arterial-blend overstatement runs the other way but is bounded — 1.80 ÷ (0.65 + 0.35k) stays ≥ 1.06 for an arterial-to-local cost ratio k ≤ 3. ⚠️ **NOT a rate proposal** (the brief forbids one): it is a UNIT decision — convert per class, convert on City centreline, or keep the value and state the unit in `floor`/`denominator_mismatch` and the three public copy sites. **What moves on the served file if converted:** legend median $304 → $547–665/acre/yr, panel median roads-ops share of levy 1.68% → 3.0–3.7%, hoods over 100% 2 → 3–4, the copy's *"about five times higher"* → ~2.5–3× (`check_cost_copy.py` names every stale sentence). **The map does not move** — a uniform scalar cancels in `scaleT`. ⚠️ Also falls with it: the 2026-09-06 *"1.29× — the two sources do not disagree about roads"* clause, which compared $/lane-km to $/centreline-km (demoted in `DECISIONS.md` 2026-09-08; the re-scope decision itself stands on its other two reasons).


- [x] ✅ **DONE 2026-09-08 — the road-figure CONSOLIDATION brief RAN (S149, Fable 5.1): `docs/FINDINGS_road_figures_consolidation.md`; L0 SOUND · L1 CONDITIONAL · L2a SOUND · L2b UNSOUND (operating basis unit) · L3 nothing reader-moving.** The near-match ($182.7M vs $180.4M) decomposed into +$43.8M O&M on our side and ~+$90M non-road components on the City's; the "1.7× disagreement between two City publications" was OUR population/window error (NR Reserve draws 2023–26 = $720.0M = $180.0M/yr vs the levy's $174.386M/yr, within 3%); 3,654 vs 3,644 km is vintage (+10.2 km of greenfield network across 28 hoods since the 2026-08-04 served file). The one open call is the item above. Original item follows.
  - **PETER TO RUN — the road-figure CONSOLIDATION brief is written and unrun: `docs/FABLE_AUDIT_road_figures.md` (2026-09-08, S147).** ⚠️ **The gap it exists for: four audits have each moved a road number (S114, S134, S136, S139) and NOBODY HAS EVER RECONCILED THE WHOLE SET AGAINST ITSELF.** Three bodies of evidence have never been in the same room — what the repo ships, the two external research inventories (`/home/opc/`, written explicitly to sit beside the repo's own for hand-comparison), and the City's published money.
  - **L1 is the level that has never been examined, and it is cheap.** S136 ran the observed-money check **per neighbourhood**; the CITYWIDE aggregate is a different measurement. Computed 2026-09-08 as a **claim to reproduce, not a finding**: `$50/m × 3,654 km = $182.7M/yr` against the City's **$180.4M/yr** Neighbourhood Renewal line — **1.3% apart, and to be assumed a coincidence until it survives**, because the like-for-like is the renewal half alone (`$38/m = $138.9M`), which is 1.3× the *other* way, and NRP's numerator bundles alleys/sidewalks/lighting. ⚠️ **Two errors of opposite sign landing on a near-match is a pattern this project has been burned by.**
  - ⚠️ **Two City publications disagree 1.7× about the same programme:** `capital_budget.csv` service `Neighbourhoods` is **$716.5M over FY2023–2029 ≈ $102M/yr**, against the 2026 approved operating budget's **$174.386M/yr** transfer to capital. ⚠️ **Neither `$180.386M` nor `$174.386M` appears anywhere in the repo** (zero hits, confirmed 2026-09-08).
  - **Also open, all denominator-side — the level this project actually gets wrong:** the residential lane-km conflict (>4,000 vs ~9,000 vs the repo's 3,654 km CENTRELINE — ⚠️ different units, may be no conflict at all); the repo's own 3,654 vs 3,644 km, 10 km unreconciled; and the snow term's arterial-blended denominator, whose overstatement has never been sized.
  - ⚠️ **The research-side inventory is STALE on its own biggest item** — it calls the $5,970/km substitution a hypothesis the repo "floated". It shipped 2026-09-06; $1,285/km no longer ships anywhere. The brief's §4 lists all four already-closed items so the round does not re-litigate them.
  - ✅ **The Calgary report (`Calgary_Road_Infra_Cost`) was TRIAGED 2026-09-08 and is mostly moot** — Thurber, the geotechnical claim and the $2,000/lane-km comparator all refute things that **never entered this repo** (zero hits for `Thurber`). ⚠️ **Its value is its EDMONTON figures**: a $158.8M annual budget on ~13,000 km (→ $12,215/km) and a quoted $12,500–$17,000/km, neither in the repo, both secondary press with unstated scope. **Leads with a scope question, not a check** — but the project is chronically short of outside-in views of its own numbers.


- [x] ✅ **DONE 2026-09-05 — Peter chose RETIRE, and it shipped the same day.**
  `svc_cost_per_acre`, the "Service cost" Services row, the Ratio view's "Per
  service $" denominator and the panel's nested "Roads + fire" row are all gone
  (`DECISIONS.md` 2026-09-05). `fire_events_per_acre` untouched;
  `cost_roads_life_per_acre` is now the sole lifecycle road column and is pinned
  in `expected_columns.json`. ⚠️ **`SPEC_development.md` Lens C and
  `SPEC_breakeven.md` are unblocked but must now name their cost side** — the
  composite they referenced does not exist.
  - ⚠️ **Two defects surfaced during the removal, both fixed, both worth the
    pattern:** the Services **panel kept its own publish flag**, so the PUBLIC
    build printed modelled transit + bike cost while the row list hid them (it
    now reads the `pub` tag); and `verify-transport-cost.js`'s "the two road
    bases stay distinct" check **could not fail** — it compared against the
    composite, whose *fire* term supplied the entire gap, and the unit test's
    fixture had both road rates at $2.0. Both are the same shape as the
    S141/S142 lesson: **a check placed where the value cannot be wrong.**


- [x] ✅ **DONE 2026-09-06 — the wrong-base sentence is DELETED, not corrected**
  (findings §7.1). *"…works out to about two and a half times the $1,285 rate"*
  stated 2.6× against $1,285 where it holds only against the whole $4,635
  ($12,000/km lifecycle O&M is **9.3×** $1,285). Resolved by the re-scope below:
  with $1,285 gone the sentence had no subject, and *"treat this as the low end
  of a range"* went with it — that phrasing's premise was the 2.6× gap, now
  closed to 1.29×. The blurb now names the two real caveats instead (arterial
  blend; unescalated FY2017 vintage) and says which way each pushes.
  ⚠️ **`check_cost_copy.py` still cannot catch this class** — it checks literals,
  not arithmetic — but it *did* catch the two claims that moved with the rate.

- [x] ✅ **DONE 2026-09-07 — recorded as deliberate; the panel is UNCHANGED.**
  Peter's call. ⚠️ **Three parts of the audit's framing did not survive
  re-measurement, and they are why the panel stayed as it is:**
  (1) **there is no DECISIONS 2026-07-16 row** — the audit cited one; the lock
  lived only in `SPEC_utilities.md` 3(b) and `UI.md`, and is now **back-filled**
  into the index, because its absence is what let the 08-10 row build a 100%
  mark without referencing it;
  (2) **the lock's subject is retired** — it governed `revenue_per_acre ÷
  svc_cost_per_acre`, and neither survives in the front end;
  (3) ⚠️ **the two claims run in OPPOSITE directions.** The Ratio's 1.0 divided
  FULL tax by a PARTIAL cost side and read **≫1** (median ≈5.8×), so a 1.0 line
  asserted a break-even the numbers could not support; the panel divides **one
  service by the whole levy**, reads **≪1** (median 1.7% ops, ~9% lifecycle),
  and 100% is a well-defined local statement.
  **Harm re-measured, both builds: still none** — 9/2/9/12 hoods over 100%
  (life/ops/transit/bike), **all set-aside**, worst a golf course.
  **What was real and is fixed:** `renderServiceCost`'s comment claimed the
  panel answers *"whether this hood's levy covers each service"* — break-even
  language for a share-of-levy rendering. The comment overclaimed; the bars did
  not. ⚠️ **Re-open if a developed hood ever crosses 100%** — that is when the
  amber starts describing a neighbourhood instead of a golf course.
  `DECISIONS.md` 2026-09-07.

- [x] ✅ **DONE 2026-09-06 — the $1,285 split treatment is closed by RE-SCOPING**
  (the fourth call, open since S139). `roadway_ops` **$4.635 → $9.32/m/yr**,
  maintenance half **$1,285 → $5,970/km**, the served GeoJSON regenerated in the
  same PR. Detail in the item directly below and in `DECISIONS.md` 2026-09-06.

### Road cost estimation — the reconciliation is CLOSED; the remaining sub-items are not (OPEN 2026-09-02, RESOLVED 2026-09-06)


- [x] ✅ **DONE 2026-09-06 — RE-SCOPED. `roadway_ops` $4.635 → $9.32/m/yr,
  maintenance half $1,285 → $5,970/km (Peter's call).** The same $1,285/km had
  been **rejected in one place and retained in another**: `DATA.md` §16 retired
  `$1,285/km × ~11,000 km = $14.135M` as ~5× too low on 2026-08-04 (live on a
  public page at the time) while it kept shipping as the maintenance half of
  `roadway_ops`. Substituting the City's published FY2017 `Roadway Maintenance`
  program closes the **2.6×** lifecycle-vs-operating gap to **1.29×** — the two
  sources do not disagree about roads. Served GeoJSON regenerated in the same PR
  so the map and the copy never disagreed; the choropleth is **pixel-identical**
  (a uniform scalar cancels in `scaleT`). Median roads-ops share of levy
  **0.8% → 1.7%**; hoods over 100% on that row **1 → 2**, both set-aside.
  `docs/FINDINGS_roadway_maintenance_rate.md` §5, `DECISIONS.md` 2026-09-06.
  - ⚠️ **The basis is STILL A FLOOR, and the two known errors have OPPOSITE
    SIGNS.** The maintenance half now inherits the **arterial blend** that snow
    always carried (overstates), and the rate **mixes vintages** — FY2017
    maintenance against 2025 snow, deliberately unescalated (understates).
    **Neither is sized.** "Floor" is a judgement about which is larger, not an
    arithmetic bound — do not present it as one.
  - ⚠️ **What $1,285 measured is STILL UNKNOWN** and that is not a leftover
    chore: it was dropped because nothing supports reading it as total road
    maintenance, **not** because a better reading was found. No decomposition of
    the published program reproduces it (materials-only $1,634/km is closest,
    still 1.27× off). **Do not reintroduce it with an invented scope.**
  - ⚠️ **The $600,000/km side was never traced** and still has not been. Q1 of
    the send-back brief below is now **half** answered, not answered.

⚠️ **The sub-items below are UNAFFECTED and still open** — the 25-vs-50 service
life, the per-class differential, the snow denominator, and the NRP finding that
the lifecycle rate is itself a floor. **None of them was touched by the
re-scope**, which moved only the operating basis.

Seven sourcing questions were written up for a research pass (given to Peter
2026-09-02 to run externally). ⚠️ **THAT ROUND CAME BACK 2026-09-03 AND DID NOT
CLOSE THIS ITEM** — Q1 and Q4–Q7 re-derived what `city_unit_costs.json` already
documents, usually in less detail, and the 2.6× gap was restated rather than
traced. What it did produce was the Table 8 route, the composite-profile trap
(`data/DATA.md` §19) and the demotion of the 3% cross-check. **Question 2 below
was answered by data we already held, not by the research** — see the send-off
item at the end of this section. The two that would change the most:

1. **What does Edmonton's $600,000/km "operate and maintain" actually
   include** — snow? lighting? sweeping, signs, signals? — and what is in the
   narrower $1,285/km "maintenance" figure.
   ✅ **HALF-ANSWERED 2026-09-05** (`docs/FINDINGS_roadway_maintenance_rate.md`):
   the City's own FY2017 `Roadway Maintenance` program is **$5,970/km, 4.65× the
   $1,285**, so the $1,285 is far too narrow to be total road maintenance —
   which closes the 2.6× gap to **1.29×** (~1.1× vintage-corrected; 1.29× is the
   figure that needs no escalation assumption). ⚠️ **What
   $1,285 DOES measure is still unknown** — the source gives it no scope and no
   decomposition of the program reproduces it. The $600,000/km side is untouched.
   ⚠️ **ACTED ON 2026-09-06** — the $1,285 was not merely doubted, it was
   **replaced** by the $5,970 program figure (see the closed item at the top of
   this section). **Q1 is still worth asking**, but only its $600,000/km half:
   what $1,285 covered no longer affects anything shipped.
2. **Is there a better source class entirely?** A uniform per-km rate cannot
   tell a 1960s neighbourhood from a 2015 one, which is precisely the
   distinction a revenue-vs-cost map exists to show. If the **Neighbourhood
   Renewal Program** publishes actual per-neighbourhood spend, that replaces
   the model with observed money. ⚠️ **That would be a real rework** — the
   metric stops being `metres × rate` — though the row/legend/panel machinery
   survives it.

Also open: the 25-vs-50 year service life (halves or doubles the whole
lifecycle number, currently chosen on one parenthetical phrase); a published
per-class cost differential; the snow rate's denominator, which blends over
11,000 km **including priority-cleared arterials** while our numerator is
collector+local only.

**Adjusting a rate is cheap by construction** — one value in
`data/city_unit_costs.json`, two test assertions, and the next refresh
recomputes; `scripts/check_cost_copy.py` fails the build if the prose is not
updated with it. Do not let the open question block shipping.


- [x] ✅ **DONE 2026-09-07 — `check_cost_copy.py` now searches READER-VISIBLE PROSE, not the raw file** (Peter's call, proposed then made; `docs/FINDINGS_vacuous_guards.md` V1). ⚠️ **Reproduced first:** the roads blurb reverted to the retired `$1,285` plus one ordinary comment containing `$5,970` → **the guard reported all 7 rates OK**. It tested `expected in html` against the raw 7,300-line file with **no locality**, and `web/index.html` is heavily commented by house style. **This is the only thing tying the map's rates to its captions and it runs on the merge gate.**
  - **The fix is the haystack, not the match.** New `prose()` builds the search space from two sources, both DERIVED rather than enumerated so new copy is in scope automatically: (1) the HTML's visible text — `<script>` blocks, `<!-- -->` comments and tags removed, which carries the `#about-*` methods-pod paragraphs; (2) every line-anchored `blurb:` string literal, with `"a " + "b"` concatenation joined SEAMLESSLY (the lifecycle rate is written `"... $50 per metre " + "per year, ..."`, so a separator would hide it). Sources are newline-joined so no match can be manufactured across a seam. **Haystack is now 4% of the file** (16,912 of 432,532 chars).
  - ⚠️ **Comments are excluded BY CONSTRUCTION — nothing strips them from JS.** That was deliberate: the file has `//` inside 5 string literals and a regex literal containing BOTH quote characters (`.replace(/[&<>"']/g, ...)`), so a comment-stripping lexer would have to resolve regex-vs-division to stay honest. Not reading comments at all cannot get that wrong. The `blurb:` key is line-anchored because `// Uses blurb: ...` prose appears **three times** in the real file.
  - **Deliberate consequence, recorded in the docstring:** a rate quoted ONLY in a dynamic builder (`servicesBlurb()`, `changeBlurb()`, …) or in `temporal-note`'s `textContent` now FAILS. Safe direction — a red merge gate is visible, a green one was not. **The fix is to widen `prose()`, never to loosen the match.**
  - **`check_cost_copy` had NO test file; it has 13 now** (`tests/test_check_cost_copy.py`), led by the falsification verbatim. ⚠️ **Falsified against 4 mutations:** reverting to the raw-file haystack reds **6 tests by name**; a space between concatenated literals reds 2; dropping the line anchor reds 1; joining sources without a separator reds 1. A first test also asserts the fixture still produces the figures the others key on, so a claim rename cannot make them pass vacuously. **799 pass** (786 + 13).


- [x] **Four `verify-*.js` scripts were RED on master since 2026-09-02.** ✅ **FIXED S141 (2026-09-05) — the suite is 42/42 green, the first clean sweep since.** ⚠️ **One of the four was a REAL BUG, not a stale test:** `#budget` and `#budget-pod` were never added to `CHROME_IDS`, so place labels were free to draw over the budget panel in the full build — `verify-reference-layer.js` was written to catch exactly that and did; nothing ran it. The page was fixed, not the test. `verify-deviation.js`'s public `#views` expectation was re-stated by hand to `money,development,services` (a GATE assertion — publishing a lens SHOULD require a human edit; `ratio`/`uses` are still full-only, so the next edit adds exactly one name). `verify-glass-cell.js` and `verify-grid-loading.js` had cell counts **pinned to live data** (34671/93201, moved to 34662/93180 by the 2026-09-02 refresh) — now derived from the served files, plus a new `the two grids are genuinely different files` check so the derivation cannot make the count checks vacuous.


- [x] **Front-end fix-in-place PR — the two defects the S140 architecture audit measured, fixed without a split.** ✅ **DONE S141 (2026-09-05)** — banners + named `boot()` shipped as specified; the module flip was **withdrawn and replaced by `"use strict";`** because its premise was falsified (`DECISIONS.md` 2026-09-05 ×2, `docs/FINDINGS_frontend_architecture_verdict.md` §7 items 1 ⚠️CORRECTED and 4). Verified: 786 python tests, `check_doc_citations` + `check_cost_copy`, and **38 of 42 `verify-*.js` green run one at a time, no page exception in the sweep**. The two carry-overs below are unchanged and still open.


- [x] **CLOSED 2026-09-05 — STAGE 2 of the `web/index.html` split: WON'T DO. The file stays one file (Peter, S140, on the architecture brief's verdict); re-open triggers in `DECISIONS.md` 2026-09-05.** Original item head: STAGE 2 of the `web/index.html` split — the JS into ES modules (NOT started, and deliberately deferred). ⚠️ **PREP IS COMPLETE (S138,
  2026-09-04) AND THE SESSION IS BLOCKED ONLY ON ACCOUNT CREDIT** — both
  `claude-fable-5` and `claude-fable-5-1` return *"You've hit your monthly spend
  limit"* from this box. That is an account usage gate, **not** model entitlement
  and **not** a stale CLI. **Launch recipe, model and effort are settled in
  `docs/PLAN_frontend_refactor.md` §6 step 1 — use it verbatim** (launch ONCE on
  Opus with the guard flags, then `/model claude-fable-5-1` in-session; the flags
  are launch-time only). Instrument:
  **`docs/FABLE_AUDIT_frontend_architecture.md`.** Do not
  re-plan this item inline; the brief hands the call to a 7-level decision stack
  (Level 0 should the front end be hand-written at all → Level 6 code), and its
  §3 carries the measured facts so the session doesn't re-derive them. **Nothing
  below is decided until that runs.** Stage 1 (CSS → `web/styles.css`) shipped
  2026-07-29, PR #116; see `DECISIONS.md` that date for the full reasoning.
  Remaining, **re-measured 2026-09-04 (S136): ~6,750 lines of JS in one block
  with 19 section banners** — the structure is already latent, it just isn't
  expressed as files. Native ESM (`<script type="module">` + relative imports)
  needs no bundler and works on Pages.
  - ⚠️ **IT DOUBLED IN FIVE WEEKS.** This item was written 2026-07-29 against
    **3,305 lines / 9 banners**; the file is now **6,748 / 19**, and the whole
    page is 7,345 lines. **The trajectory is the argument, not the size** — and
    it is the one number here that came from measurement rather than taste.
    The five banners added since: change lens, deviation lens, the institutional
    band (×3 sections), temporal lens, the revenue panel, the budget panel.
  - ⚠️ **Do NOT justify this on token savings — that was measured and is false.**
    See `docs/TOKEN_EFFICIENCY.md` "Files to watch". Justify it on navigability,
    grep precision and blast radius, or not at all.
  - ⚠️ **`DEFAULT_BUILD` must stay in `index.html`** — `scripts/build_site.py`
    regexes it there and hard-fails on anything but exactly one match. If the JS
    moves, that literal stays behind or `build_site.py` moves with it.
  - ⚠️ **"11 verify scripts reference `index.html` directly" was WRONG, and it
    pointed the risk at the wrong half of the repo.** Measured 2026-09-04:
    **8 of 65** profiling scripts name it, **7 as a served URL**
    (`localhost:PORT/index.html`) — the page, not the source — so an ESM split
    leaves those working and the JS harness is **mostly not the risk**.
    ⚠️ **The eighth is the exception, and "every one is a URL" was wrong
    (re-measured 2026-09-04, S138): `tools/profiling/verify-staleness-banner.js`
    reads `web/index.html` OFF DISK** (`fs.readFileSync`, line 66) and regexes
    `const STALE_DAYS = (\d+);` out of the source — a literal declared at the
    `tunables` banner, **inside the `<script>` block that a stage-2 split
    moves**. It fails loudly (`process.exit(1)`, "not found"), not silently, but
    it is **the one JS-side file a split must carry**, and it is a second
    instance of the same pattern as `check_cost_copy.py` /
    `check_served_columns.py`: **a guard asserting on the text of the artifact
    rather than on the value.**
  - ⚠️ **THE REAL COUPLING IS THE PYTHON/CI SIDE — 11 non-doc files read the
    single file**: `build_site.py` (the `DEFAULT_BUILD` regex, above),
    `check_cost_copy.py` and `check_served_columns.py` (both scan the HTML for
    copy/column gating), `check_doc_citations.py`, `build_reference_layers.py`,
    `tools/codemap.py`, `tests/test_build_site.py`, `test_codemap.py`,
    `test_window_labels.py` (WINDOWS literals vs `main.py`), plus `refresh.yml`
    and `deploy.yml` path triggers. ⚠️ **`tools/codemap.py` is the sharp one** —
    it parses the banners out of this file to generate `docs/CODEMAP.md`, which
    a `PostToolUse` hook regenerates and `CLAUDE.md` names as the way to
    navigate. **Move the JS without moving codemap.py and the project's own
    navigation aid silently empties.**
  - **Gate: wait until stage 1 has actually helped** (the mobile-chrome work in
    `MOBILE_USABILITY.md` §3 is the first real test of it). Don't do stage 2
    speculatively. ⚠️ **The doubling arguably moots this gate** — the item was
    deferred when the file was half its current size. Re-read the gate before
    invoking it as a reason to defer again.


- [x] **CLOSED 2026-09-03 — WHY IS VALUE LEAVING THE LOT-ACRE DENOMINATOR? It
  isn't. The trend was ONE STEP WITH AN INVENTED MIDPOINT, and the number that
  kept it alive came from stale local data.**

  Opened 2026-08-05 out of the band work, on this premise: `ineligible_points`
  and `ineligible_value_frac` moved *"monotonically upward on every independent
  data change"* — 56 → 58 → 60 and 0.00517 → 0.00575 → 0.00633 across
  2026-08-01 / 08-03 / 08-04, no reversal — in the guard's own **dangerous**
  direction. The item flagged its own weakness and was right to: *"Only 3
  independent observations exist… Confirm the trend continues before treating
  the slope as real."* Nobody did, for four weeks, while it headlined two
  handoffs as *"the most likely thing to fail next."*

  **The confirming data existed the whole time.** Every `refresh.yml` run logs
  all six anchors against a fresh `download_data.py` pull, so
  `gh run view <id> --log | grep 'INFO:   '` over the run list is the entire
  series. Fourteen runs, harvested 2026-09-03:

  | date | `ineligible_points` | `ineligible_value_frac` |
  |---|---|---|
  | 08-01, 08-02, 08-03 05:17 | 56 | 0.00517178 |
  | 08-03 11:19, 08-04, 08-05 | 60 | 0.00632732 |
  | **08-10** | **56** | **0.00516634** |
  | 08-17, 08-19, 08-23, 08-24 | 57 | 0.00516946 |
  | 08-25 | 57 | 0.00515087 |
  | 08-31 | 57 | 0.00515159 |
  | 09-02 | 58 | 0.00515519 |

  ⚠️ **THE MIDDLE OBSERVATION WAS NEVER OBSERVED.** The `58 / 0.00575` matched
  no run. All five of its anchors were midpoints of the rows either side —
  `lot_needle_ratio` 12.82175 exactly between 12.822 and 12.8215, points 58
  exactly between 56 and 60. It had been sitting as a pinned row in
  `OBSERVED_IN_CI` in `tests/test_check_value_anchors.py` since 2026-08-05,
  where it was load-bearing: **it is what turned a single step into an apparent
  monotone three-point trend.** The 08-01→08-05 window holds **six** runs and
  only **two** distinct data states; the step fell between the 05:17 and 11:19
  runs of 08-03, which the harvest had collapsed into one "08-03".

  ⚠️ **And the step reverted on 08-10.** Since then the pair has moved ~0.3%
  across 8 independent pulls. `ineligible_value_frac` sits at **49.4% of its
  band** — dead centre — not the 72% its own note estimated nor the 83% the
  S133/S134 handoffs carried. There was never a breach coming.

  ⚠️ **Where 83% came from: a stale, MISMATCHED local `data/raw/`.** This box
  held `Property_Info__Current_Calendar_Year_.csv` dated 2026-07-06 beside a
  2026-08-09 assessment file. Against that pair the guard reads
  `ineligible_points` **85** / `ineligible_value_frac` 0.00646; CI, same code,
  same day, fresh pull, read **58** / 0.00515519. Majority-null `lot_size` is
  exactly what a stale property-info file paired with a newer roll distorts.

  ⚠️ **THAT PHANTOM HAD ALREADY COST SOMETHING.** The 2026-09-02 re-pin note
  claimed the reading *"had reached the band ceiling EXACTLY and would have
  fired on the next weekly publish on its own"* and widened `ineligible_points`
  28–84 → 42.5–127.5. It would not have fired — CI read 58, comfortably inside
  28–84. The ceiling moved 84 → 127.5, **halving the guard's sensitivity in its
  own declared dangerous direction to accommodate a number the published
  pipeline never produced.** (The floor move was harmless: below-band on a
  high-danger anchor is `benign`, warn-only, never reds the publish.)

  **What shipped**

  1. `ineligible_points` re-pinned to **29–87**, centre 58, the real 2026-09-02
     CI reading, same ±50%. `ineligible_value_frac` deliberately NOT re-pinned —
     it is already within 0.6% of its centre.
  2. `OBSERVED_IN_CI` replaced with the full verified series, interpolated row
     gone, distinct states labelled by the run that first produced them.
  3. `scripts/check_value_anchors.py` gains `report_raw_vintage()`: it logs each
     raw file's date, warns above `STALE_RAW_DAYS` (14, the site-wide
     convention) or `MISMATCHED_RAW_DAYS` (2, since both files come from one
     `download_data.py` run), and **refuses `--write-baseline`** on either
     condition (`--allow-stale-baseline` overrides). Reading stale anchors is
     merely misleading; *writing a band from them* is how this happened. Silent
     in CI, where the mtimes are the download times.
  4. New `test_every_band_is_centred_on_a_reading_ci_actually_produced` —
     **falsified against the 42.5–127.5 band first**, where it fails with
     *"centred on 85, outside every reading CI has logged (56-60)"*. Widths were
     already pinned; **provenance was not**, which is the whole gap.

  **Transferable rules.** ⚠️ *A trend needs three REAL observations — check that
  the middle one is one.* An interpolated point is indistinguishable from data
  once it is in a table, and it manufactures exactly the monotonicity that makes
  a trend look real. ⚠️ *A guard run on stale input is not a weaker reading, it
  is a different measurement* — and this project already had the harvest habit
  (`_why_two_widths` was built from CI logs) but reached for the local run
  anyway. ⚠️ *Pinning a band's width without pinning its centre guards the wrong
  half.* Same family as *a band fitted around a defect* (S133) and *an assertion
  placed where the value can't be wrong* (S133).

  Related: `_why_two_widths`'s *"5 runs, 3 independent data changes"* is also
  wrong — six runs, two states — so the ±25% given the four "frozen" anchors
  rested on two observations, not three. **Their bands need no change:** 8
  further CI states through 2026-09-02 keep `dedupe_effect_pct` in
  0.040806–0.0408324, `dup_parcel_value_frac` in 0.00309363–0.00309689 and
  `dup_parcel_points` flat at 33, all far inside ±25%. The claim was overstated;
  the conclusion happened to survive.

- [x] **CLOSED 2026-08-29 — the three verify failures are resolved, and one of
  them was NEVER a master failure.** Replaces the two items previously here
  (`verify-temporal.js` "fails on unmodified master", and the two "stale
  expectation" scripts). Reproduced before acting, per the standing rule.
  - **`verify-temporal.js` — NOT a defect, and the item's headline was wrong.**
    6/6 PASS on clean `master` on an idle box. Re-run under deliberate
    contention (12 concurrent chromiums) it FAILS **on the exact selectors the
    old item named**, both `Timeout 4000ms exceeded`. ⚠️ **This is the
    already-documented `run-verify-scripts-alone` condition, not a third
    broken script** — the 2026-08-16 "4 failures in 4 sequential runs" was
    measured on a box that was not actually idle. **The 4000ms budget was NOT
    raised**: nothing is wrong with it under the protocol the project already
    requires. Folded into the `verify-peek.js` flakiness item below, which is
    the same root cause.
  - **`verify-revenue-panel.js` — FIXED, and the old diagnosis was stale.** It
    listed 3 failures with one cause; there were **6 with two**, and the new
    three were the interesting ones. ⚠️ **`rev_frac_*` is NOT one partition —
    it is two overlapping dimensions.** `rev_frac_exempt` is a CROSS-CUTTING
    flag (an exempt institutional parcel counts in `rev_frac_inst` AND in
    `rev_frac_exempt`), so the test's ground truth of "every `rev_frac_*` > 0"
    summed to 1.054081 for DOWNTOWN — the excess being exactly its 0.054082
    exempt share. The app was right throughout: `REV_CATEGORIES` excludes
    exempt by construction and the panel note discloses it separately. Ground
    truth now excludes it, **and a new check asserts exempt IS cross-cutting**
    so the exclusion did not silently drop coverage. The other three were the
    known element-vs-visible count, fixed with the house `getClientRects()`
    idiom.
  - **`verify-nonres-revenue.js` — FIXED by DERIVING the tolerance, not
    widening it.** The old `1 + 1e-9` predated the 6-significant-figure export
    decision (`DECISIONS.md` 2026-08-09) and failed on 127 of 406 hoods. ⚠️
    **The invariant was checked against what the rounding can produce before
    any epsilon was touched**, which is what the old item demanded: measured
    across all 406 hoods, **every breach sits inside the half-ULP bound of the
    three rounded values and NONE exceeds it** (worst: WÎHKWÊNTÔWIN, excess
    0.4 against a bound of 0.6). So the decomposition is exact upstream. The
    test now computes that per-hood bound instead of carrying a magic number.
    **Falsified against injected breaches**: 0.5× the bound passes, 2× and 10×
    both fail — it discriminates at the rounding boundary rather than being
    loosened into uselessness.


- [x] **✅ DONE 2026-08-28 — the archive can no longer freeze the wrong year.**
  Built on Peter's *"do f1 and f3"*. `write_archive(..., confirmed=)` refuses to
  overwrite a confirmed entry with an unconfirmed capture; the caller MEASURES
  the capture (reusing `detect_year`, never a second comparison) instead of
  trusting the pin; `_year_confirmed` backfilled from the standalone guard's own
  verdict. ⚠️ **Deliberately NOT the proposed "skip on inconclusive"** — that
  would leave the archive empty through the months-long FIR lag and cost a year
  outright if Alberta ran late, reintroducing the original loss. The data is
  irreplaceable; only the label was ever wrong. Regression test falsified against
  the old logic (fails on the OVERWRITE, not the signature).
  Original item — audit F1, 2026-08-28;
  `docs/FINDINGS_proxy_guards.md` T1. **The 2026-08-27 fix deleted the bad
  entry; it did not close the door.**
  - **Reproduced, not inferred:** `write_archive`'s freeze protects *other*
    years — the **pinned** year's entry is reassigned every run (by design, so
    the live capture improves). Under a **stale pin** that writes the NEW roll
    over a CORRECT archived year, weekly and silently.
  - ⚠️ **The FIR guard cannot catch it**: `detect_year`'s candidate set is
    years **Alberta has filed**, and Alberta files months after Edmonton rolls.
    Simulated on Edmonton's own history — a next-year roll at **+2%/+4%**
    returns a confident **ALIGNED on the wrong year**; at **+6%/+8.3%/+12%**
    it returns inconclusive, which `refresh.yml` treats as **proceed**.
    **No revaluation rate protects the archive.**
  - **The missed distinction is REVERSIBILITY.** "Inconclusive → proceed" is
    right for regenerating `web/data` (recomputable) and wrong for the freeze
    (permanent). They share one gate.
  - **Proposed:** make `--write-archive` require a *positively confirmed* year
    and SKIP on inconclusive, leaving regeneration untouched. A skipped capture
    is recoverable next week; a wrong one never is. **Changes
    `check_temporal_years.py`'s contract — propose-first, hence not built.**


- [x] **✅ DONE 2026-08-28 — the merge gate exists.** `.github/workflows/tests.yml`
  runs `pytest` + `check_doc_citations.py` on `pull_request` and `push: master`;
  offline and secret-free, so it cannot flake on an upstream outage. ⚠️
  **`refresh.yml`'s own pytest step STAYS** — that one gates the weekly data
  publish, this one gates the change; a test pins both, because the tempting
  cleanup is to drop the "duplicate". ⚠️ **Branch protection is still OFF** —
  the gate reports, but nothing blocks a merge on it. That is a repo-settings
  change only Peter can make. Original item — audit F3, 2026-08-28. `pytest` appears in **exactly one place**:
  `refresh.yml`, a weekly cron. No `pull_request` workflow exists and `master`
  is **not protected** (API returns `Branch not protected`).
  - **`deploy.yml` publishes to the live site on every push with zero test
    execution**, and "746 passed" in a PR body attests to the author's laptop,
    not the merged state.
  - A failure introduced on a Tuesday surfaces the following **Monday as a held
    data refresh** — the symptom is a stale map, not a red check on the cause.
  - **Real mitigation, stated honestly:** the placement *inside* `refresh.yml`
    is correct (before download/regeneration), so a broken suite holds the data
    path rather than corrupting it. The gap is release-gate vs merge-gate.
  - **Proposed:** a `pull_request` + `push: master` workflow running
    `pytest tests/ -q` + `check_doc_citations.py` — both offline, ~11s, no
    secrets, no network. **Changes CI behaviour — propose-first, hence not
    built.**


- [x] **✅ DONE 2026-08-27 — the temporal archive's mislabelled 2025 entry is
  deleted, and 2025 is accepted as unrecoverable.** Found 2026-08-26, fixed
  2026-08-27; full write-up in `docs/DATA_ISSUES.md` §2 and `DECISIONS.md`
  2026-08-27. Deleted rather than relabelled — a correct `2026` entry already
  existed (342/406 hoods byte-identical, totals +0.0021% apart). ⚠️ **Deleting
  did NOT restore 2025**: it is in `HISTORICAL_DEFECT_YEARS`, so the year is
  OMITTED rather than falling back to the historical file, whose 2025 slice
  carries the same 2,448-account hole that got 2024 omitted. **Published series
  is now 2012–2023 + 2026.** Moved with it: the `expected_temporal_years.json`
  2025 anchor (removed, with an in-file re-pin prohibition), `CHG_WINDOW_LABEL`
  → `2012–2026`, the tooltip's hardcoded `(2024 n/a)` (now derived), and 9
  rescaled checks across `verify-temporal.js` / `verify-change.js` — all green.
  `check_temporal_archive_year.py` now exits **0**.
  - ⚠️ **STILL OPEN, split out below:** wiring that guard into a workflow. It
    was unwired only because it failed by design; that reason is now gone.


- [x] **▶▶ FIXED 2026-08-25 — THE MEASURED ROLL-YEAR GUARD EXISTED BUT RAN
  NOWHERE — `check_roll_year_against_fir.py` was not wired into any workflow.**
  Opened and closed 2026-08-25, immediately after the item below shipped it.
  - **The gap.** The item below replaced the blind metadata guard with one that
    measures parcels, and deliberately downgraded `check_year_alignment.py` so
    it can now return only `aligned`-on-current-metadata, `inconclusive`, or
    `hold`. But `refresh.yml` still invoked **only** `check_year_alignment.py`.
    Net effect: with the coverage string stale (which it is), CI had **no
    positive confirmation of the roll year at all** — the new detector ran only
    when a human remembered to type it. A guard that exists and never executes
    is documentation, not a guard.
  - **Fixed by** adding a `rollyear` step to `refresh.yml` immediately after the
    metadata guard (it must follow `Download source data` — it reads the
    downloaded roll), and giving the script the same `$GITHUB_OUTPUT` contract
    the metadata guard already had (`result` / `detected_year` / `pinned_year` /
    `banner`), so the workflow can gate on either identically.
  - **Exit 3 HOLDS** — skip regeneration, keep serving the last committed data,
    raise the banner (Peter's call, 2026-08-25). Reasoning: unlike the metadata
    string, this guard *measures*, so a mismatch is evidence rather than a
    guess, and it is the exact failure that billed a 2026 roll at 2025 rates for
    months. False-positive risk is low by construction — the script returns 4
    (inconclusive), never 3, unless another year fits within 5% **and** beats
    the runner-up by 3%.
  - ⚠️ **Both guards can hold, so all seven publish steps now gate on BOTH**
    (`steps.yearcheck… != 'hold' && steps.rollyear… != 'hold'`), and the banner
    step fires on either, preferring the FIR banner because it measured the
    parcels. `test_refresh_workflow_gates_every_publish_step_on_both_guards`
    parses `refresh.yml` and asserts the coverage holds — the failure it exists
    to catch is a future step copying a neighbour's `if:` and gating on only one.
  - ⚠️ **`PyYAML` had to be added to `requirements-ci.txt`.** That test parses
    the workflow; PyYAML was in `requirements.txt` only, so the test passed
    locally and would have errored at import inside the very `pytest` step that
    gates the refresh. `jupytext` pulls it in transitively, but a guard-shape
    test must not rest on a transitive dep.
  - **Verified:** 727 tests pass (713 + 14 new); the workflow parses and all
    eight gated steps carry both conditions.

- [x] **▶▶▶ FIXED 2026-08-25 — THE LIVE ROLL IS THE 2026 ROLL AND WE BILLED IT
  AT 2025 MILL RATES —
  the year-alignment guard cannot see it, because it reads a Socrata metadata
  STRING instead of the data.** Opened 2026-08-25, found by the FIR comparison
  below (which is how a wrong number got caught: my own first pass compared the
  roll to the wrong FIR year and reported +18.2%; see the correction there).
  - ⚠️ **THE EVIDENCE — residential is the tell.** Residential land is barely
    exempt anywhere, so our residential base should match the province's filed
    residential base closely. Ours is **$162,273,056,185**. Against FIR:

    | FIR year | filed residential base | ours reads |
    |---|---|---|
    | 2023 | $131,284,317,914 | +23.6% |
    | 2024 | $134,439,557,008 | +20.7% |
    | 2025 | $148,128,818,480 | +9.5% |
    | **2026** | **$160,372,669,990** | **+1.2%** |

    Monotonic, and 2026 fits to within noise. **The roll advanced and nothing
    noticed.**
  - **Corroborated three ways, independently:** (a) the dataset is literally
    named *Property Assessment Data (**Current Calendar Year**)* and it is
    August **2026**; (b) `data/mill_rates.json`'s 2026 block matches FIR 2026
    `MR(3)` **exactly** (Residential `7.7419`, Non-Residential `25.2216`) — the
    City published 2026 rates and we already hold them; (c) the residential fit
    above.
  - ⚠️ **WHY THE GUARD IS BLIND.** `scripts/check_year_alignment.py`
    `parse_coverage_year()` reads
    `metadata.custom_fields["Time Frame"]["Period of Coverage"]`, which still
    says `"2025-01-01 to 2025-12-31"` (`Date Updated: 2026-05-11`). **The City
    did not update that string when the roll rolled.** `vintage_report.py`
    reports "Roll is 2025, pin is 2025 — aligned" and the January year-roll
    checklist never fires. **A guard that trusts a publisher's free-text
    metadata field is not measuring the data** — this is the project's
    signature failure mode wearing a green checkmark.
  - ⚠️ **IMPACT ON EVERY PUBLISHED LEVY NUMBER.** `main.py ASSESSMENT_YEAR = 2025`
    feeds `apply_tax_rates(..., assessment_year)`, so the 2026 roll is billed at
    2025 rates: Residential `7.6254` vs `7.7419` (**−1.5%**), Non-Residential
    `24.2229` vs `25.2216` (**−4.0%**). Citywide our levy reads **$2,714,729,701**
    at 2025 rates vs **$2,784,219,936** at 2026 — the site **understates by
    ~$69.5M (2.5%)** from the rate year alone, on top of showing a 2026 roll
    labelled 2025.
  - ✅ **APPLIED 2026-08-25** (Peter: "yeah sure can you just do them?"):
    1. **Detector fixed FIRST**, so this cannot recur silently every January.
       New `scripts/check_roll_year_against_fir.py` measures the **parcels**:
       our residential base vs Edmonton's filed base (FIR `MR(2)`), exit 3 on
       mismatch. New `scripts/fetch_fir_tax_base.py` → committed
       `data/fir_tax_base.json` (manual/reviewed, the mill-rates pattern;
       `data/DATA.md` §21). `check_year_alignment.py` now returns INCONCLUSIVE
       — never "aligned" — when the coverage string is older than the calendar
       year, so a stale string can no longer read as agreement.
    2. **Re-pinned** `ASSESSMENT_YEAR` (`main.py`) and `DATA_YEAR`/`RATE_YEAR`
       (`generate_status.py`) to 2026. Verified against `docs/RUNBOOK.md` §1:
       mill rates 2026 pre-staged and complete for `DISPLAY_RATE_CLASSES`,
       stormwater has 2026, `WATER_RATE_YEAR`/`FRANCHISE_RATE_YEAR` already
       2026 and left alone.
    3. ⚠️ **Activity windows deliberately NOT bumped** — `FIRE_YEARS` /
       `PERMIT_YEARS` / `PERMIT_YEARS_RECENT` pin the last **COMPLETE** calendar
       year, which is still 2025 in Aug 2026. No deflator re-run needed either
       (no new permit year pulled in).
    4. **Temporal baseline re-pinned** (`--write-baseline`) after reading the
       guard first, per RUNBOOK step 8. 2025 correctly moved live→archive; the
       series is now 2012-2023, 2025-2026, live year 2026, no hard-fail.
    5. **Measured result:** citywide levy $2,714,729,701 → **$2,784,219,621**
       (+$69.5M, the rate year alone). Pipeline run end-to-end, `pytest` 713
       passed.
  - ⚠️ **NOT DONE — the banner.** `generate_status.py --clear-banner` (RUNBOOK
    step 10) was not run: no banner was ever raised, because the guard never
    detected the roll. Confirm none is showing after the next refresh deploy.


- [x] **▶▶ FIXED 2026-08-25 — THE MAP'S LEVIED/EXEMPT UNCERTAINTY BAND WAS TOO
  NARROW — `PS`
  ("Parks and Services") is categorised `never`, not `inst`, so $88M/yr of levy
  is missing from the exempt scenario.** Opened 2026-08-25, falls straight out
  of the zone decomposition above. ⚠️ **This one DOES reach the rendered map**
  (the FIR findings above are all docs-only so far).
  - **What the band is.** `web/index.html` renders a two-scenario uncertainty
    band per hood — a levied prism and an exempt prism
    (`inst-band-levied`/`inst-band-exempt`, `deviation-band-*`) — gated on
    `INST_UNCERTAIN_MIN = 0.25` against `rev_frac_inst`. Deliberately
    **achromatic**, because a band asserting no direction must not be tinted
    toward either pole. `GLASS_INST_MIN = 0.25` does the same for the 100 m
    grid via `inst_frac`.
  - ⚠️ **The defect.** `rev_frac_inst` comes from `load_zoning.ZONE_CATEGORY`,
    where **`PS` → `"never"`** while only `AJ`/`UF`/`UI`/`PU` → `"inst"`.
    Measured on the 2026 roll at 2026 rates:

    | | levy | share of citywide |
    |---|---|---|
    | AJ/UF/UI/PU — drives the band | $136,423,407 | 4.90% |
    | **PS — excluded from it** | **$88,038,783** | **3.16%** |

    **Treating PS as institutional would widen the band by 65%.**
  - ⚠️ **ONE MAPPING IS DOING TWO INCOMPATIBLE JOBS.** `ZONE_CATEGORY` answers
    both *"can this ever be developed?"* (where `PS` → `never` is **correct** —
    parks aren't infill) and *"might this be exempt?"* (where `PS` → `never` is
    **wrong** — parks are prime exempt candidates). A single category cannot
    express both. ⚠️ **Do not "fix" this by moving `PS` to `inst`** — that
    would break the development lens. It needs a second, independent
    exempt-candidate set.
  - **Hoods that would newly cross the 0.25 gate: 17 → 24 (+7).**

    | hood | today | with PS |
    |---|---|---|
    | MILL WOODS PARK | 0.000 | **1.000** |
    | MCQUEEN | 0.190 | 0.412 |
    | CALLINGWOOD NORTH | 0.000 | 0.373 |
    | ROYAL GARDENS | 0.000 | 0.318 |
    | HERITAGE VALLEY TOWN CENTRE | 0.030 | 0.310 |
    | WOODCROFT | 0.196 | 0.298 |
    | LEGER | 0.003 | 0.291 |

    ⚠️ **MILL WOODS PARK is the headline: its ENTIRE levy sits on `PS` zoning,
    and the map currently draws it as fully certain** — no band at all — when
    it may be the most exempt-exposed hood in the city.
  - ⚠️ **My 17 is an approximation of the code's 15** (`INST_UNCERTAIN_MIN`'s
    comment says *"15 hoods on Total; 2 on Residential"*). I counted every hood
    with levy; the map also applies `inDeviationPop(p)`, which I did not
    replicate, and the comment predates the 2026 roll. **Re-derive in-code
    before quoting either number.**
  - ✅ **APPLIED 2026-08-25, together with the roll-vintage fix above.**
    - New `load_zoning.EXEMPT_CANDIDATE_ZONES = ("AJ","UF","UI","PU","PS")`,
      **deliberately independent of `ZONE_CATEGORY`** — which keeps `PS` →
      `never`, so the development lens is untouched. Both sets carry comments
      saying why the other exists and warning against merging them.
    - `property_zone_categories` refactored onto a new `property_zone_codes`,
      so the exempt share reads the raw zone CODE off the **same single**
      440k-point join rather than adding a second one.
    - New per-hood `rev_frac_exempt` (NOT folded into the `rev_frac_*` family,
      which partitions levy and sums to 1.0 — this cuts across it). Grid's
      `inst_levy`/`inst_frac` renamed `exempt_levy`/`exempt_frac`; client's
      `instFrac`/`INST_UNCERTAIN_MIN`/`GLASS_INST_MIN` renamed to match, because
      a column named `inst_*` that includes parks is a lie.
    - **Measured on the real pipeline output, not a model:** hoods at/over the
      0.25 gate **17 → 24** citywide; **MILL WOODS PARK 0.000 → 1.000**. In the
      tooltip's deviation population the caveat tier is **15 → 21** (the six new
      ones all park-dominated) and the band-prism set is unchanged at 6.
    - **Verified:** `verify-glass-inst.js` 15/15, `verify-inst-caveat.js` 25/25
      (two hardcoded expectations updated with the reason recorded: the U of A
      range moved on 2026 RATES, the count on `PS`), `verify-amenity.js` 35/35,
      `pytest` 713 passed.
  - **Next:** re-derive independently before trusting it; decide whether the
    site should state a measured overstatement against a filed figure. ⚠️
    **This is a public-number question and Peter's call**, same as sub-item (3)
    above — but it now has an external reference point, which is exactly what
    that item said it lacked.


- [x] **Sweep the doc-to-doc citations — DONE 2026-08-09 (S104). ONE REAL
  DEFECT, and it was a locked decision built on a display artifact.** The
  mechanical half was already automated (`scripts/check_doc_citations.py`,
  S103); this ran the judgement half — whether the prose a citation points at
  still supports the claim — over the 168 doc-to-doc citation sites that carry a
  falsifiable figure, re-deriving from `data/raw/` rather than comparing texts.
  ⚠️ **RETRACTED: "14% of Edmonton has no neighbourhood polygon" (2026-08-08).**
  It read **672.4 km²** of drawn hood fabric against a **782.1 km²** city and
  called the **109.6 km²** difference annexed land carrying no neighbourhood, in
  `DATA.md` §3 + §14, `DECISIONS.md`, `build_reference_layers.py` and a
  `web/index.html` comment. Measured in `EPSG:3400`, the same 406 hoods cover
  **782.0 km² in the RAW boundary file** against a **782.4 km²** legal outline —
  agreeing to **1.4 km²**, inside that outline's own 100 m simplification noise.
  **The raw fabric tiles the city.** The 109.6 km² is `main.py`'s
  **`SETBACK_M = 45.0`** display buffer: **all 406 hoods lose area** (median
  **18.3%**, min 2.7%, max 65.9% — perimeter-proportional, the signature of a
  shrink, not of missing land), and `buffer(-45)` + `simplify(10)` reproduces
  the shipped **672.42 km²** to the decimal. **No wrong number reached the
  public page** — code comments and docs only. The 2026-08-08 decision to draw
  the limit **survives**; its stated evidence did not.
  ⚠️ **The generalisable lesson: a number read off a SHIPPED DISPLAY FILE is not
  a fact about the world.** `neighbourhood_value_per_acre.geojson` is
  post-setback, post-simplify geometry, and `join_and_calculate.py` already
  documented both as display-only — the doc that got it wrong never opened it.
  **Also fixed:** both outstanding guard warnings (`UI.md "Roads ground layer"`
  → `"Services views"`; the audit brief's `docs/SPEC` → `docs/SPEC_phase1.md`,
  a file that **never existed in history**), an overstatement in S103's own
  record (it called three cited files missing; **two have existed since
  2026-05-16** and the ledger's 2026-07-09 row records the brief being executed
  against one of them), a `FINDINGS_lot_dedupe.md` pointer, and an external
  "project knowledge" reference now marked as unverifiable-in-repo. Citation
  guard: **0 warnings, down from 5**. — 2026-08-09 · `docs/TODO_archive.md`
  **Verified correct and left alone** (re-derived, not compared): the `$50k` /
  `$4M` colour clamps still sit at **p97.0 / p97.5** on live data; roads
  `$264–$3,253` and fire `$7,092–$298,901` anchors; `rho +0.959` over all 406;
  the served grid's top three lot-acre cells **612.3 / 149.3 / 143.0** (exact);
  the whole Open-Budget corroboration table (**99.7% / 99.1% / 97.1%**, snow to
  **99.2%**, roads **4.6×**); the census anchor **459,859**. Two dated
  measurements have drifted with the weekly refresh and were left as dated:
  the stock-age grid (**34,675** cells → 34,671) and the 5yr geocode coverage
  (**47,125/59,697** → 47,052/59,687) — both still support their conclusions.
  Full result: `docs/AUDIT_LEDGER.md` 2026-08-09 (S104).


- [x] **`WEST MEADOWLARK PARK`'s revenue MORE THAN DOUBLED in one auto-refresh —
  EXPLAINED 2026-08-07: a RENUMBERING GAP CLOSING, so the +130% was the
  CORRECTION, not the defect.**
  `total_revenue` $4.63M → $10.63M (+130%). ⚠️ **`$4.63M` was the wrong number;
  `$10.63M` is right — the map had been UNDERSTATING this hood by ~$250M of
  assessed value / ~$6M/yr for as long as the gap lasted.**
  - ⚠️ **THE ANSWER MOVED THREE TIMES AND THE FIRST TWO ARE IN THE COMMIT
    HISTORY. Do not cite them.**
    1. *"One new $247.8M parcel arrived."* **True but shallow** — every figure
       below still holds, it just is not what happened.
    2. *"Is a hospital supposed to be taxable?"* **THE WRONG QUESTION.** It
       always was taxable and always was on the roll.
    3. ✅ **A RENUMBERING GAP.** Misericordia has been continuously assessed
       **2012–2025** as account **`10095840`** (~$200–260M, always WEST
       MEADOWLARK PARK, always COMMERCIAL). It was renumbered to `11495573` and
       was simply **absent from the published current roll** during the
       changeover. Nothing arrived; something came back.
  - **The pipeline did the right thing throughout.** Account **`11495573`, 16940
    87 AVENUE NW**, `tax_class = Non Residential`. Parcel count 1079 → 1080 and
    `$438,858,000 + $247,780,500 = $686,638,500` **exactly**. Implied rate
    **2.4223%** = **24.223 mills** = exactly the 2025 Non Residential municipal
    rate in `data/mill_rates.json` (24.2229). Value rose 56.5% while revenue rose
    129.7% purely because the parcel is taxed at 3.2× the residential rate.
  - **The other candidates are ruled out by measurement.** Not a hood
    reassignment — the largest value *drop* anywhere was QUEEN MARY PARK at
    ≈$6.6M, nothing lost $247M. Not `qi6a-xuwt` — that defect is accounts
    *missing* from the historical roll; this is one *arriving* in the current
    one. Not a code change — `git log f76fc7d..f464bdf` is the single data-bot
    commit.
  - ⚠️ **The item's own reproduce line was off by one refresh.** The jump landed
    at **`f464bdf`, the SECOND 2026-08-03 refresh**, not the 08-03 → 08-04
    boundary. Eleventh time a stated basis did not survive re-measurement.
  - ⚠️ **This is the event that exposed the guard hole, and that is one durable
    outcome.** The run was **green** — all five guards passed, no email, four
    days on the live map, found only by diffing git revisions for an unrelated
    reason. `scripts/check_revenue_deltas.py` now exists because of it, and
    **warn-not-fail turned out to be right for a reason only visible at the
    end**: the event it catches is a correction, so failing the publish on it
    would have been exactly backwards.
  - ⚠️ **The other durable outcome is the general lesson:** every identifier in
    the assessment data churns independently (account renumbered, address
    re-addressed, neighbourhood renamed), so a check built on any one of them
    reports churn as loss. `tools/audit_roll_continuity.py` matches by
    **position** because of this. See `docs/DECISIONS.md` 2026-08-07 (×2) and
    the session-summary for S100.
  - **The residual question is upstream and is its own open item** (whether the
    revenue model should treat `AJ/PU/UI/UF` differently at all — ~$125.4M/yr of
    modelled levy, Peter's call, not decidable from this dataset). ⚠️ Note that
    this is **no longer** framed as "was West Meadowlark's parcel anomalous" —
    it was not; it is 5% of a pre-existing exposure present in every published
    number all along. Revenue side only — `road_m_per_acre` changed in 0 of 406
    hoods, so no renewal figure moved.


- [x] **RE-PIN `data/expected_columns.json` ONCE the four Stage 2 columns ship
  — CLOSED 2026-08-04, 62 → 66.** (`cost_roads_ops_per_acre`,
  `cost_transit_ops_per_acre`, `cost_bike_ops_per_acre`,
  `transport_cost_ops_per_acre`.)
  - The item's gate was *"do NOT re-pin before the refresh carries them"*, and
    the weekly cron was 6 days out (Monday 2026-08-10). Peter chose to
    **dispatch `refresh.yml` by hand** instead of waiting — run
    `30909649645`, success, data commit `024ecc6`.
  - ⚠️ **The item's prediction held exactly, which is worth recording because
    the previous two closed items' predictions did NOT.** Against the freshly
    published GeoJSON the guard warned on all four columns as NEW and exited
    **0** — the correct interim state, not a problem. It took that same path in
    CI on the same run.
  - Verified before re-pinning: all four columns present on all **406**
    features, 66 columns total, and the composite sums exactly
    (`88.92 + 13820.65 + 129.59 = 14039.16`). Re-pin diff is a pure four-line
    addition — no column silently changed name or vanished. Clean re-run
    afterwards: *"all 66 baselined columns present on all 406 features"*.
  - ⚠️ **`python` on this box is the SYSTEM interpreter and cannot run this
    script** — `dict[str, int]` raises `TypeError: 'type' object is not
    subscriptable`. Use `.venv/bin/python`. The restoration procedures write
    bare `python` after a `source .venv/bin/activate` that is easy to skip.

- [x] **THE SERVED-COLUMN GUARD HAD NEVER RUN IN CI — CLOSED 2026-08-04 on the
  same run.** Carried S89 → S91 as a next-step, never as a `TODO.md` item.
  Step *"Check served columns (guard after regenerating)"* executed and
  reported success on run `30909649645`. It is no longer an untested code path
  in the weekly publish.
  - Also closed on that run: both S90 features' **data** finally shipped. The
    three transport cost rows and the budget-context pod had been correctly
    hidden since 2026-08-03 because those were code-only deploys.
  - Verified against **production**, not a local build:
    `verify-transport-cost.js` went **6 → 41 passed / 0 failed** against
    `/full/` — including the load-bearing two-bases assertion, roads operating
    **$89** vs lifecycle svc **$7,527** on the same metres — and
    `verify-about.js` returned **ALL CHECKS PASSED** against the public root,
    recomputing all four budget shares independently from the published dollars
    (12.2% / 1.3% / 0.79% / 0.15%) and fitting the pod at 720px tall.

- [x] **`verify-peek.js` WAS 71% OF THE SUITE'S WALL TIME — FIXED 2026-08-04,
  437s → 94s, all 27 checks still green.** The item was right that the script
  dominated the suite and right that the cost was software-GL picking. ⚠️ **It
  named the wrong loop, and both of its proposed levers were wrong** — which is
  why the first thing done was to re-measure rather than act on it.
  - **The item blamed `findTappableHoods` (the `targets` grid sweep). Measured
    2026-08-04, that sweep is 46s of 408s.** It exits as soon as it has `n`
    hoods, so it never approaches its 2,400-candidate worst case: **1 candidate
    / 9 picks** on desktop, **22 candidates / 57 picks** on touch. The real cost
    was the **empty-map-pixel scan** — **346s, 85% of the total** — a blind 7px
    sweep making **~2,470 picks** before it found a pixel that picks nothing.
  - ⚠️ **A PICK COSTS ~137ms AND NEITHER `radius` NOR `deviceScaleFactor`
    CHANGES THAT** (measured: r0 vs r6 identical; dsf3 vs dsf1 identical). The
    cost is deck **re-rendering the whole picking buffer** on the CPU under
    SwiftShader on *every* `pickObject` call, not the buffer readback. So the
    only lever that works is **making fewer picks**. Separately, the **first**
    pick burst in a context carries a **one-off ~20s** of shader warm-up, which
    is what `targets`' remaining 46s almost entirely is — it is already at the
    floor and was deliberately left alone.
  - ⚠️ **"Coarsen the grid" was measured and is a TRAP.** Step 7 → 25 still
    costs 30s, and **step 40 finds no empty pixel at all** and would fail the
    check. Empty pixels are genuinely scarce here: only **17 of the 4,400**
    points on the 7px grid are clear.
  - **The fix is the item's *other* lever, applied to the loop that actually
    cost the time: derive the pixel from geometry, pick only to confirm.**
    `metric-extrusion` is the **only pickable layer**, so "no hood polygon
    covers this pixel" and "`pickObject` returns nothing" are the same
    statement — and `boot()` has already flattened the map, so a prism's screen
    footprint is just its projected polygon. Project all 406 hoods' rings to
    screen (**9,236 vertices, 14ms**), ray-cast point-in-polygon with a bbox
    pre-filter, require an 8-point ring at 7px to be clear as well, then confirm
    the first candidate with **one** real pick. **2,474 picks → 1**, landing on
    the *same* pixel (382,425) the blind sweep found. Falls back to a 3px grid
    if the 7px one yields nothing, since geometry tests are free where picks are
    not. — 2026-08-04 · `tools/profiling/verify-peek.js`

- [x] **▶ THE HISTORY PANEL PAINTS OVER THE TITLE BLURB IN FIVE STATES.
  FIXED 2026-08-02** (`verify-temporal.js` **43 → 67 checks**). Measured on clean
  master 2026-08-01; **re-measured 2026-08-02 before anything was touched and
  found identical** — 46 / 46 / 158 / 252 / 289px — despite three PRs having
  landed on this area since. A rare case of a carried item whose numbers were
  *not* stale.
  - ⚠️ **Two things in the item WERE stale, and the re-measurement caught both.**
    Its title says *"the history panel"*, but two of the five states now show the
    **revenue-mix** panel, which did not exist when it was written — and the two
    modes are **different heights** (293 vs 308px), so a fix assuming one height
    is wrong in the other. And it asserted that moving the panel below the blurb
    "does not fit", generalising from Infill: it fits in **3 of the 5** (money's
    cuts with 172px spare, the change lens with 45px) and fails only in
    Development (by 26px) and Infill (by 100px).
  - **Ruled (Peter): track the measured title, and cap.** `syncTemporalPos`
    measures `#title` and `#botleft` and places the panel between them —
    `syncMillRates` + its `ResizeObserver` was the pattern, and observers now
    watch **both** boxes, since `#botleft`'s legend changes height per view.
  - ⚠️ **WHICH ELEMENT YIELDS REVERSED DURING IMPLEMENTATION, on a finding.**
    The ruling was *cap the blurb*; `#title` is `class="panel"` and `.panel` sets
    **`pointer-events: none`**, so a capped, scrollable blurb **cannot be
    scrolled to** — it would hide text with no way to reach it. Giving `#title p`
    pointer-events:auto would steal a ~360×380px region from map dragging, the
    failure `#botleft`'s own comment records having caused. `#temporal` is
    already pointer-events:auto, so the **panel** yields instead. Re-ruled by
    Peter on that evidence.
  - ⚠️ **TWO DEFECTS THE FIRST IMPLEMENTATION SHIPPED, BOTH FOUND BY MEASURING
    THE FIX RATHER THAN ASSUMING IT:**
    - `max-height` is **content-box** by default, so it excluded the 21px of
      vertical padding + border and the panel overshot `#botleft` by exactly
      that minus the gap — **11px, in every state that capped**, including two
      that did not even scroll. `#temporal` is `box-sizing: border-box` now
      (width 300 → 328 keeps the content box identical).
    - **An absolutely-positioned close button inside a scroll container scrolls
      away with the content.** The x *and* the hood name both left the box in
      Infill — the two things you need in order to use a scrolled panel. New
      `#temporal-body` wrapper holds the scrolling region.
  - **Result at 1440×900: all ten states clear both the blurb and `#botleft`.**
    Two scroll (Development −38px, Infill −112px). Below ~768px tall the two
    longest blurbs hit the min-height floor and reach into `#botleft` — left
    open in `TODO.md`, because at 1280×720 Infill's blurb is 479px of a 720px
    screen and the column has **36px** free, so no placement rule can fix it.
  - ⚠️ **The CHECK was the other half of the bug.** `panel clears the title`
    passed throughout, because it only ever ran on money/value — the same narrow
    case the original 210px sweep was written from. It now sweeps **six states**,
    and also asserts the name and the x survive a scroll. **Falsified both:**
    restoring the constant `top` fails exactly the five original states; moving
    the name back into the scrolling region fails the two that scroll.

- [x] **`verify-temporal.js` HAD BEEN RED SINCE THE 2026-08-01 AUTO-REFRESH, and
  nothing reported it. DIAGNOSED AND FIXED 2026-08-02** (42 → 43 checks, green).
  5 of 42 checks failed on clean master: Downtown's share read **3.28%** where
  the script pinned **3.30%**, with the commercial-base and current-value
  literals moved with it.
  - **The item asked: did the data move, or did the splice move? Answer: the
    data, and only its live year.** Diffing the served `temporal.json` at
    `ab8bac7` against `4466fbf` across all 406 hoods and all three series:
    **839 cells changed and every single one is in the 2025 column.**
    2012–2023 are **bit-identical**, the hood set is unchanged (nonzero counts
    404 / 406 / 402 both sides), and the shares still conserve to 100%
    (999,993 → 1,000,008 ppm). Citywide 2025 value rose 0.296%
    ($237.50B → $238.20B) while Downtown's own fell 0.32%, which is exactly why
    its share fell 3.2991% → 3.2788%. The archive half of the splice never moved.
  - ⚠️ **THE DEFECT WAS IN THE SCRIPT, AND IT CONTRADICTED A GUARD THAT WAS
    ALREADY RIGHT.** `scripts/check_temporal_years.py` ran on that refresh and
    **passed**; its docstring pre-registers this exact movement — *"The live
    year is NOT pinned to a band. It is a live snapshot that genuinely moves
    week to week … so a pinned band would cry wolf continuously."*
    `verify-temporal.js` pinned that same quantity to **equalities**. This was
    not a near-miss the guard failed to catch; it was cry-wolf by construction,
    and it would have gone red after essentially every roll update.
  - ⚠️ **The item's own premise was false and is corrected in place:** it claimed
    the temporal file "has no equivalent" of `check_value_anchors.py`. The guard
    exists and runs in `refresh.yml` before the status-manifest step. **Sixth
    time an open item's stated cause did not survive reproduction.**
  - **Fix: derive, don't band** (Peter's call over the standing *pin bands*
    rule). Live-year numbers are read from the loaded series via `temporalFor`
    and compared against the rendered strings; historical anchors (2012 5.09%,
    peak 5.55% in 2016) stay pinned tight, because those are what prove the
    archive half held. A band would still have needed a width guess and would
    still drift; deriving cannot cry wolf and additionally catches the panel
    rendering the wrong hood, series or index.
  - ⚠️ **Compare PARSED NUMBERS, never a string built with the page's own
    formatter** — that would have made S85's `fmtBig` bug invisible. Tolerance
    is one display ulp (0.006; both formatters carry two decimals).
  - **Falsified all three, per the standing rule:** an off-by-one live index
    (`length - 2`) fails 3 checks; the commercial slot rendering `share` instead
    of `commercial` fails 1; `fmtBig` dropping a decimal (**"$8B"** — the S85
    bug shape exactly) fails 1.
  - **Left open as a proposal:** a data-only refresh still triggers no deploy and
    runs no front-end check at all. The data side is guarded; the *render* is not.

- [x] **UI BUG: the Display popover and the Data & Methods pod overlap.
  FIXED 2026-08-02** (`#a11y-menu { bottom: calc(200% + 8px) }`;
  `verify-about.js` **44 → 50 checks**). Reported by Peter 2026-07-28.
  **Both the reported DIRECTION and the suspected CAUSE failed to survive
  reproduction — the fifth time an open item's stated cause proved wrong.**
  - **The direction was backwards.** The item said Display "covers" the
    Data & Methods button. Measured, it is the reverse: equal `z-index` falls
    back to DOM order and `#about` is later, so the **button paints over the
    menu**, truncating *"Landmarks & nearby pla⌷es"*. Found in a screenshot;
    the `elementFromPoint` probe agreed.
  - **The cause was not the z-index asymmetry.** It is that the two pods form a
    **stack** in one column (`#a11y` `bottom:40px`, `#about` `bottom:68px`,
    both buttons 26px tall) while `#a11y-menu` was anchored to its **own**
    button's top (`calc(100% + 6px)`), ignoring the sibling above it. Both
    offsets are fixed, so the ~23px collision was identical at 1440x900,
    390x844 and 360x780.
  - ⚠️ **THE SUSPECTED FIX WOULD HAVE BEEN WORSE THAN THE BUG.** The
    hypothesised `#a11y.open { z-index: 5 }` was **falsified by applying it**:
    it paints the menu over the button, and `verify-about.js` then **times
    out** because the *"Landmarks & nearby places"* label **intercepts pointer
    events** — the Data & Methods button becomes **unclickable**. A visual
    defect would have been traded for a dead control. (Caught only because
    `verify-about.js` uses a real `page.click()`; a JS `.click()` bypasses
    `pointer-events` and would have passed.)
  - ⚠️ **The new checks assert GEOMETRY (no overlap), not paint order.** A
    "menu is on top" assertion passes for the z-index version — the very
    outcome to reject. Only *they do not overlap at all* rejects both failures.
  - `calc(200% + 8px)` tracks the shared button styling (the pod's own height
    counted twice, plus the 2px inter-pod gap and the 6px the menu already
    wanted) instead of hardcoding 60px.


- [x] **▶ REVENUE-LENS READOUT — phase 2 of 2: the UI. DONE 2026-08-01 (both
  halves).** Phase 1 (the pipeline) shipped the columns earlier the same day.
  Peter: *"I actually want this in the popup panel, instead of the assessment
  graph, on the revenue lens. also can we have the current relevant mill rates in
  the top left on this lens?"*
  - **Decisions RULED by Peter:** top by **category**, not raw zone code; on
    Money/Revenue the panel shows the breakdown **instead of** the assessment
    graph, with history staying reachable via the Change-over-time lens;
    pipeline before UI.
  - [x] **(a) The panel. DONE 2026-08-01** (`renderRevenueMix`,
    `verify-revenue-panel.js`, **37 checks**). `#temporal` gained a MODE rather
    than a sibling — it already owned the three dismissals, the `CHROME_IDS`
    exemption, the phone bottom-sheet form, `#hoodmode` and the peek card's
    commit path. Three rulings taken at build time, all revising the brief:
    - **ALL non-zero categories, ranked — not top 3.** The panel has the room a
      tooltip doesn't, so the rows sum to 100% with no unstated remainder
      (Downtown's top 3 is only 90%).
    - **Shown on the Residential/Non-residential cuts too, with the denominator
      NAMED.** `rev_frac_*` are shares of the hood's TOTAL levy while those cuts
      colour one class of it — so panel and map divide by different things, and
      §6's rule applies: an unnamed denominator is how a correct number reads as
      wrong.
    - **The header keeps `total_revenue` + `revenue_share_city`.**
    - ⚠️ **The categories are `USE_CATEGORIES`' OWN**, column derived as
      `"rev_" + u.frac` rather than listed again — that is what stops the Uses
      lens's area shares and this panel's revenue shares drifting apart.
    - ⚠️ **Three surfaces advertise the panel and all three follow the lens**
      (`#peek-go`, `#temporal-hint`, the tooltip's invite). A pinned panel also
      re-renders on any lens change (`syncPinnedPanel`) — a revenue breakdown
      left under a value map is a silent-correctness failure.
    - ⚠️ **`fmtBig` could NOT be reused for the levy:** calibrated for
      assessment totals ($10M–$10B), it rounds megas whole and printed a
      $1,876,137 levy as **"$2M"** — a 7% error on a fiscal headline. `fmtLevy`
      keeps two decimals. Caught by reading the rendered output, not by a test.
    - `SPEC_temporal.md` §2 now opens with the warning that the panel is the
      history surface **only under Value**; `verify-temporal.js` selects Value
      on every page it opens.
  - [x] **(b) Mill rates. DONE 2026-08-01** (`#millrates`,
    `verify-millrates.js`, **54 checks**; PRs #131 / #132 / #133, **production
    verified in both builds**). Three things the brief got wrong, all found by
    measuring:
    - **"~500px of left column is free" was measured with the panel CLOSED.**
      `#temporal` owns that column: it is **308px** tall (its own CSS comment
      says ~265), leaving 211px of slack at 1440x900 but **79px at 1366x768** and
      **31px at 1280x720**. There is no room for pod *and* panel on a laptop, so
      **the pod yields while a hood is pinned** (Peter, after re-measurement,
      reversing his first call to push the panel down).
    - **"Top left is an open spot" is false on two of the three cuts** —
      residential and non-residential blurbs push `#title` to 256, not 196. The
      pod is positioned from the **measured** title box, never a constant.
      This is the same defect the panel has, unfixed — see the item above.
    - **"Relevant = follow the sub-metric" became: show all three, light the
      active ones** (Peter's ruling). Dropping rows would hide the 7.6254-vs-
      24.2229 differential, which is the fact the map rests on.
    - Rates ship in `status.json` as `municipal_rates`, derived from
      `data/mill_rates.json` — never typed into the page. `assumed` is data, so
      the Farmland caveat stops printing by itself when a real row is published.
    - **The PHONE FORM took two goes, and the second deleted the first.** Peter
      saw the desktop-only build (*"no rates show on mobile"*), described a
      standalone stack, then rejected it on sight: ***"i don't like the
      independent mill rates panel. folding it into the tax revenue blurb is
      fine."*** Final: `#millrates` is **re-parented into `#title`** below 640px,
      so the rates open and close with the description blurb and add nothing to
      the default render. Only the stacking (one rate per row) survives from the
      standalone version. ⚠️ **Every problem that version had to solve — an
      anchor clear of `#controls`, its own card background, the inherited
      panel-yield — was an artifact of it being a separate surface.**
      `MOBILE_USABILITY.md` §2 and `DECISIONS.md` have it.
    - ⚠️ **One bug shipped and was fixed inside the day:** the desktop yield
      `#temporal.open ~ #millrates` went out **ungated**, so switching the phone
      readout to **panel mode** blanked the rates with nothing contending (the
      panel is a bottom sheet there). The comment said "desktop-only in effect" —
      reasoning about the LAYOUT, not the SELECTOR. **A media gate was written,
      then falsified as redundant** (a child of `#title` is not `#temporal`'s
      sibling) and dropped. `verify-millrates.js` asserts the behaviour instead.
  - **Available columns** (shipped by phase 1): `total_revenue`,
    `revenue_share_city`, and `rev_frac_{never,notyet,inst,residential,
    commercial,industrial,mixed,dc,other,unzoned}`.
  - ⚠️ **`rev_frac_unzoned` is the honesty column** — 0.002% citywide today. If
    it ever grows, the top-3 is quietly describing less than the whole hood. Do
    not hide it; `src/revenue_by_zone.top_zones()` already excludes it from the
    ranking by default rather than letting it take a slot.


- [x] **UI BUG: the hover tooltip `div.tip` rendered on TOUCH, 127px off the
  right edge. CONFIRMED ON DEVICE and FIXED 2026-07-31.** `tooltipFor` now
  returns null under `noHover()`. Full reasoning in `DECISIONS.md` and
  `SPEC_temporal.md` §2; regression net in `verify-peek.js`.


- [x] **PROMOTED the temporal + change lenses to the PUBLIC build — DONE
  2026-07-31 (PR #121, merged `828bb5a`, deploy green, LIVE).** Peter: *"can we
  actually move those value change over time features to the public build"* →
  **both**. A **content-split tag change, not a re-opened lock**.
  - **Cost: three `FULL_BUILD` conjuncts.** No pipeline, no new columns, no
    build plumbing — `temporal.json` (42 kB gzipped) **already shipped to the
    public root** and the controls were **hidden, not stripped**. The **data**
    gate survives, which is the half that matters.
  - **The verify scripts caught the contract change** — five "the public build
    does NOT have this" assertions. Two made **stricter**: "panel opens" beats
    "cannot open" (a build that failed to load `temporal.json` SATISFIED the old
    absence check, so it could not tell *correctly withheld* from *silently
    broken*), and the change-window check now runs AFTER entering change mode
    (`#chgwindow` is hidden in Money/current in BOTH builds, so the old
    assertion passed for the wrong reason).
  - **A caveat must travel with the lens it qualifies** — new check that the
    public build STATES the 2024 omission.
  - **Verified in the BUILT tree**, not just `?build=public` on source.
  - ⚠️ **`#hoodmode` moved ABOVE `#coloradj`** (Peter), which also fixed
    `verify-coloradj.js`. **That commit was STRANDED** — #121 merged the
    previous commit only, in the gap between the PR-state check and the push
    landing; recovered by cherry-pick into #122. **Re-measuring on the new
    branch is what caught it.**


- [x] **ALL THREE PRE-EXISTING VERIFY FAILURES ARE FIXED (2026-07-31). THE
  SUITE IS GREEN: 26 scripts, 0 failures.** First found 2026-07-29 while
  verifying the CSS extraction (not caused by it), carried through S79 as "fix
  or waive". **All three were STALE TEST EXPECTATIONS, not app bugs** — the app
  was right every time, which is why nothing looked broken on screen.
  - [x] `verify-ind-permits.js` — **both failures were ONE root cause: the
    window suffix.** `state.devWindow` defaults to `"long"`, so the live columns
    are `ind_permits_per_acre_long` / `new_units_per_acre_long`, while the
    script hardcoded the BARE names. The colour check therefore recomputed p97.5
    over a *different distribution* and failed on a small delta
    (`want 148,39,97 got 140,37,97`) that read like ramp drift; the infill check
    listed only the bare names. Both now derive the column from the app's own
    `devCol()`/`DEV_COLS`, so **a future window cannot break them again**. Two
    checks ADDED to keep them honest once the column is app-supplied: the plane
    must be driven by an `ind_permits_per_acre*` column, and infill must never
    read an industrial one.
  - [x] `verify-glass-no-slider.js` — **the 100 m grid is Development's DEFAULT
    (`devGrid: true`), so entering the view lands on the grid, where the slider
    is CORRECT.** The script probed straight after switching view and called the
    result "the neighbourhood choropleth". True when the grid was opt-in, stale
    since. It now selects the choropleth EXPLICITLY rather than trusting the
    view default. (The suspected causes recorded here — the removed Glass slider
    and the moved `#coloradj` — were both wrong.)
  - [x] `verify-coloradj.js` — a THIRD failure, found 2026-07-31 and not
    previously listed. `#coloradj is the last child of #opt-body` and two
    re-checks, all reporting `layers > coloradj > hoodmode`. Confirmed
    pre-existing on master; cause dated to **S78 (#119)**, where `#hoodmode` was
    added to `#opt-body` *after* `#coloradj`. **Unnoticed because S79's gate ran
    3 of the 26 scripts** — the standing cost of a targeted gate. Fixed by
    Peter's call: `#hoodmode` moved ABOVE `#coloradj`, restoring the 2026-07-26
    intent that colour scaling reads last. No CSS `order:` on these pods, so
    markup order is visual order.
  - **Generalisable:** all three failed because a test restated a value the app
    owns (a column name, a default mode, a markup position) instead of reading
    it. ⚠️ **And all three were invisible on screen** — the standing rule is
    that a red verify script is evidence about the *test* as often as the app,
    so diagnose before "fixing" either.
  - **Full-suite baseline, 2026-07-31: 26 scripts / 0 failures.** Run it in
    batches (quirk t): `node tools/profiling/verify.js <url> <names...>`


- [x] ~~**ASSESSMENT-OVER-TIME GRAPH PER NEIGHBOURHOOD**~~ — **✅ COMPLETE
  2026-07-29, live in `/full/`. All four phases shipped; `SPEC_temporal.md` has
  nothing pending.** Read that spec before editing the lens: **§2** for the
  panel's design and the two silent-failure rendering invariants, **§0** before
  touching anything that reads the historical file. Regression net:
  `tools/profiling/verify-temporal.js` (38 checks). The sub-items below are kept
  as the record of how it was decided, not as work.
  Original ask (Peter, 2026-07-28): *"you mouse over and get a line graph of the
  assessment value over time, for that hood."* The data exists and the
  aggregate is cheap — see `data/DATA.md` §"Property Assessment Data
  (Historical)". Measured, not assumed:
  - **`qi6a-xuwt` "Property Assessment Data (Historical)" — 14 years, 2012–2025,
    5.5M rows**, and it carries `neighbourhood_name`, so it never has to be
    downloaded whole. One server-side `$group=neighbourhood_name,assessment_year`
    returns **5,577 rows / 443 hoods in ~3 s, 534 kB raw** — and that is verbose
    JSON; as array-of-arrays it is well under 100 kB before gzip, i.e. ~1% of the
    current 7.7 MB payload. **This is the cheapest new lens the project has ever
    had available.**
  - **The series is a real story, not decoration.** Downtown: $7.30B (2012) →
    **$10.28B peak (2016)** → **$7.09B (2025)** — down ~31% from peak — while its
    account count *rose* 8,716 → 10,307. A revenue-per-acre project that cannot
    show that is leaving its best material on the table.
  - [x] ~~**The home for it**~~ — **sparkline in the hover tooltip PLUS a
    click-to-pin panel.** Peter asked "can that go in the pop ups?" Mechanically
    yes: `tooltipFor` returns an HTML string and a 14-point sparkline is one
    inline `<svg><polyline>` — no library, no dependency. But hover **vanishes on
    mouse-out, cannot be studied, and does not exist on touch at all**, and the
    Money tooltip already carries 3–4 rows — so the sparkline is the teaser and
    the panel is the home. ⚠️ **Attribution, so nobody re-litigates it as
    settled-by-Peter: this was decided on the merits in `SPEC_temporal.md` §2,
    NOT asked.** The touch argument makes it close to forced, and it is cheap to
    reverse, but it is mine. Say so if it comes up.
  - [x] ~~**The pinned panel's DESIGN**~~ — **SETTLED 2026-07-29. Full table in
    `SPEC_temporal.md` §2.** Left column under the title (`top: 210px`, measured
    against a 176–179px title box, not estimated); dismisses three ways (×,
    Escape, a second click on the pinned hood); clicking **another** hood re-pins
    and an empty-map click is **inert**; the sparkline rides **every** view's
    tooltip via one wrapper; phone = a near-opaque bottom sheet. ⚠️ **Attribution:
    decided ON THE MERITS BY ME, not asked** (Peter's instruction was "just pick
    the panel design"). Cheap to reverse.
  - [x] ~~**Where it gets built**~~ — **`/full/` (specialist build), 2026-07-28,
    Peter: "we'd prototype this in full for now."** Natural home: it already
    carries the work-in-progress badge, so an unfinished lens is labelled as
    one. Gate it the established way (`|| !FULL_BUILD` beside the data guard);
    `CONTROLS_MATRIX.md` §2 notes the three places a lens leaks if it is ever
    promoted to public.
  - [x] ~~**Map the defect across all 14 years**~~ — **DONE 2026-07-28**,
    `tools/audit_historical_roll_gaps.py`, map in `output/historical_roll_gaps.json`.
    **Confined to 2024–2025; one dropout event, not systemic.** 2013–2023 clean
    (0–14 accounts/yr = 0.00%); 2024 = 2,322, 2025 = 131 incremental (~2,448
    cumulative). **2012–2023 usable, 2025 repairable via the current roll, 2024
    irreparable.** Full read-out: `docs/SPEC_temporal.md` §0.1.
  - [x] ~~**How to treat 2024**~~ — **OMITTED. Decided 2026-07-28 (Peter).** An
    honest gap in the line, reason stated on hover. **This reversed the balanced
    panel §0.2 originally recommended**: share-of-base is self-normalizing per
    year, so the metric needs each year's roll *complete*, not the account
    universe *constant* — a fixed panel would punch the same $2.93B hole into
    twelve clean years to rescue one broken one. Flag and uncertainty-band lose
    on display grain (invisible at sparkline size). Interpolation stays ruled
    out. Full reasoning: `SPEC_temporal.md` §0.2.
  - [x] ~~**Metric, denominator, per-acre**~~ — **ALL THREE DECIDED 2026-07-28
    (Peter); `SPEC_temporal.md` §7 is now empty and the rows live in §6.** The
    settled cut is **share of the TOTAL citywide base · assessed VALUE · TOTAL
    not per-acre**, the only combination needing no deflator, no area assumption
    and no mill-rate table. Value over revenue (reaches 2012 vs 2014, and skips
    the class-differential caveats); **commercial-base share appears as a
    labelled number in the pinned panel, not a second sparkline**.
  - [x] ~~**The splice + the guard**~~ — **DONE 2026-07-28. PHASE 0 IS CLOSED.**
    `src/load_temporal.py` (splice) + `scripts/check_temporal_years.py` (guard,
    wired into `refresh.yml` before the status-manifest step) + the year × hood ×
    class aggregate added to `download_data.py`. 33 new tests. Read
    `SPEC_temporal.md` §0.3–§0.4 and `ARCHITECTURE.md` before touching either.
  - [x] ~~**Archive the live year, or lose 2025**~~ — **DONE 2026-07-28.**
    `data/temporal_archive.json` (~74 kB/yr, committed), captured on every run
    by `check_temporal_years.py --write-archive`. Freeze rule: only the live
    year is ever written. The archive wins only for `HISTORICAL_DEFECT_YEARS` —
    using it for a clean year would mix vintages. `SPEC_temporal.md` §0.4.
  - [x] ~~**Phases 1, 2 and 4**~~ — **DONE 2026-07-28.** The hood × year module,
    the served file (`web/data/temporal.json`, 406 hoods × 13 years, **89.2 kB**
    of a 100 kB budget), and the guard. Wired into `main.py`.
  - [x] ~~**Phase 3: render it in `/full/`**~~ — **DONE 2026-07-29. THE LENS IS
    COMPLETE; all four phases are shipped.** Sparkline in the tooltip +
    `#temporal` click-to-pin panel; `#temporal` is in `CHROME_IDS`; gated
    `|| !FULL_BUILD` beside a defensive fetch. Regression net:
    **`tools/profiling/verify-temporal.js`, 38 checks.** ⚠️ **Two invariants that
    fail SILENTLY — read `SPEC_temporal.md` §2 before editing the chart:**
    x is scaled from the **year value** and the line is drawn as **runs split at
    every gap** (index positioning or one polyline would hide the 2024 hole, and
    neither is visible to the eye — the verify script *measures* the 2× ratio);
    and the **y axis is not zero-based**, so both endpoints are labelled (most
    hoods are under 1% of the base, so zero-basing flattens 406 series).
    The verify script also earned its keep on the way in: it caught a title
    overlap at the first `top` offset, and the `OLIVER`→`WÎHKWÊNTÔWIN` rename
    crashing its own hood lookup.
  - **Context — the 2024/2025 slices of `qi6a-xuwt` are PROVEN INCOMPLETE** (2026-07-28; evidence in `data/DATA.md` §0). For assessment year
    2025, same year, the current roll has **11,216 Downtown accounts / $7.81B**
    and the historical file has **10,307 / $7.09B** — a **909-account, ~$720M
    hole**, including two entire ICE District towers that are present in 2023,
    absent 2024–25, and present again in the current roll.
    - **This is not a curiosity, it changes the headline number.** The apparent
      Downtown collapse was $2.07B; the real one is **$1.35B**. Peak-to-2025 is
      **−24%, not −31%**. Roughly a third of the story was the hole.
    - **Build the guard first, the graph second.** Same idiom as
      `check_year_alignment.py` / `check_value_anchors.py`: reconcile each year's
      account count + total against a control, and refuse to publish a year that
      does not. **Likely shape: historical for 2012–2023, the current roll for
      the live year.**
    - [x] ~~**Quantify how far the defect reaches**~~ — **DONE 2026-07-28**, all
      14 years. Confined to 2024–2025, one dropout event; 2012–2023 clean.
      ~~"~8,000 accounts short citywide"~~ **was wrong** — inferred from row
      counts of different vintages, and most of that gap is new construction.
      The measured figure is **2,448**. See §0.1 of `SPEC_temporal.md`.
    - [ ] **BUG REPORT to Edmonton Open Data — worth doing (Peter, 2026-07-28),
      gated on Peter reviewing it by hand first.**
      - ⚠️ **THIS SUB-ITEM IS LIVE WORK AND WAS RE-PROMOTED TO `TODO.md` ON
        2026-08-06** — it rode its closed parent into the archive on 2026-07-31
        and was invisible for six days. **Track it in `TODO.md`, not here**;
        the copy below is kept only because this file is verbatim history.
        `tools/todo_archive.py` now refuses to archive a closed parent that
        still has unchecked children.
      Notebook written for exactly
      that: **`notebooks/exploration/03_historical_roll_gap.ipynb`** — hits the
      live API only, no local data, runs top to bottom, re-derives every claim.
      - ✅ **SCOPE NOW MEASURED (2026-07-28) — it is CITYWIDE, and the earlier
        "~8,000" was wrong.** That figure was inferred from row counts; most of
        the gap is new construction. Verified account-by-account: **2,448
        accounts / $2.93B / 188 neighbourhoods** existed in 2023 *and* exist in
        the current roll but are absent from historical 2025. Downtown holds
        1,292 (53%); Magrath Heights 430 (17% of the hood), Glenora 269 (15%).
        **Report the 2,448, never the 8,000.**
      - ✅ **Cite dataset IDs and query params, not prose.** `qi6a-xuwt`
        (Historical) and `q7d6-ambg` (Current Calendar Year); City data staff
        will want exact resource IDs + the SoQL used. The notebook prints both.
      - ⚠️ **LEAVE THE CAUSE UNSTATED.** Describe the symptom — whole multi-unit
        buildings absent together, citywide — and let the City diagnose. Do not
        speculate about leasehold/condo record handling or ETL join logic in the
        report, however tempting the address clustering makes it.
      - [x] ~~Whether the gap reaches years **before 2024**~~ — **SETTLED
        2026-07-28: it does not.** 2012–2023 are clean (0–14 accounts/yr).
        ⚠️ **The N−1/N+1 detector this item originally pointed at cannot answer
        the question** — it is blind to dropouts that never return, and reported
        **5** for 2024 against a true 2,321. The answer came from the
        current-roll control detector. `SPEC_temporal.md` §0.1 (not §4.1 — that
        section number no longer exists).
      - [ ] Still to do before filing: spot-check a few missing accounts against
        the City's public assessment lookup, so the report cites something a
        human can open.
      - **Strongest single exhibit: Stantec Tower** (10310 102 ST NW):
        Edmonton's tallest building, 309 accounts in the 2023 slice, **zero rows
        in 2024 and 2025**, and 310 accounts / $105.7M in the current roll.
  - [x] ~~**⚠️ NAME THE DENOMINATOR IN THE UI**~~ — **DECIDED 2026-07-28: the
    sparkline plots share of the TOTAL base; the pinned panel ALSO states the
    commercial-base share as a labelled number** (not a second line — two series
    is past what a 14-point sparkline carries). Downtown is **3.22% of the total
    base but 9.30% of the COMMERCIAL base** (2025); public reporting (CBC/council
    ~5.2%) quotes the second kind, so an incoming claim that those figures
    "match the project's" does **not** hold against total-value share, and
    publishing 3.22% beside an article saying 5.2% makes the project look wrong
    when it is not. Full table in `ANALYSIS_BACKLOG.md`. **Still binding on the
    build: recompute BOTH from the current roll before publishing.**
  - **RESOLVED 2026-07-28: the office-devaluation story survives, at ~2/3 the
    headline size.** Commercial fell **$6.32B → $4.85B (−23%) on a near-stable
    account count** (822 → 723) — the same buildings reassessed lower, confirmed
    against the roll we ship rather than the suspect historical file. Annotating
    2024 as a "discontinuity" is no longer the plan: it was mostly a data hole,
    so the fix is to **use good data**, not to annotate bad data.
  - **RESOLVED 2026-07-28: the 1,280 missing residential accounts are the
    defect, not an event.** Traced individually — 1,358 of 1,359 exist nowhere in
    the 2024 roll, exactly one moved (to OLIVER), only 2 return in 2025. Not a
    reclassification, not a boundary redraw, not condo-to-rental consolidation.
  - [ ] **Decide the metric: assessed value, or revenue.** Value is available
    2012–2025 directly. *Revenue* needs historical mill rates — we already have
    them (`pwis-wc4c`, "2014 onward"), so a revenue series is possible but starts
    **2014**, not 2012, and inherits every class-differential caveat.
  - [ ] **⚠️ NORMALIZE AGAINST THE CITYWIDE BASE — this is not a polish item, it
    decides whether the graph means anything (Peter asked "does inflation matter
    for people doing this?", 2026-07-28).** The answer is that **inflation is the
    *second*-order problem**. The first-order one: the **mill rate is a
    residual** — council sets a budget, rate = levy ÷ total assessed base — so a
    citywide revaluation is *fiscally neutral* (the rate absorbs it) and a hood's
    tax burden moves **only when its assessment moves differently from the city
    average**. A nominal per-hood series conflates those two. **CPI-deflating
    does not separate them** — it answers a purchasing-power question, not a
    tax-share one. The normalizer that does is the **citywide base itself**
    (share of base, or hood indexed to city): unit-free, no deflator, no vintage
    to maintain.
    - **This changes how the Downtown finding must be read** (see
      `ANALYSIS_BACKLOG.md`): −31% nominal is uninterpretable until set against
      what the citywide base did over the same years. Same query, minus the hood
      dimension.
    - **Where inflation genuinely does bite:** dollars-per-acre *levels* compared
      across years; and the services lens if it ever gets a time axis — revenue
      and modeled cost must share a year's dollars, and city input costs track a
      **Municipal Price Index**, not CPI (asphalt/equipment/wages). CPI on the
      cost side would be the wrong index, not merely imprecise.
    - **Trap:** assessed values embed **house-price** inflation, which has
      diverged sharply from CPI. Deflating asset prices with a consumer index
      reads rigorous and is apples/oranges.
    - **Vintage, affects axis labelling:** Alberta assessments are market value
      as of **July 1 of the preceding year** (MGA) — the 2025 column reflects
      mid-2024 conditions. **Stated from domain knowledge; confirm against
      Edmonton's own published wording before it reaches user-facing copy.**
  - [ ] **Per-acre or total?** The whole project is per-acre, but hood boundaries
    and the account count both move over 14 years (Downtown gained ~1,600
    accounts). A per-acre series divides by a *current* area — state whether that
    is honest before shipping it.
  - ⚠️ **Do not skip the year-alignment question.** `scripts/check_year_alignment.py`
    and the year-roll machinery exist because the current roll's year moves. A
    historical series that silently ends one year early each January is exactly
    the failure this project already guards against elsewhere.


- [x] ~~**TEMPORAL, ROUND 2 — "HOW MUCH HAS EACH HOOD CHANGED?" AS A MAP METRIC,
  WITH SELECTABLE WINDOWS (Peter, 2026-07-30).**~~ — **✅ BUILT 2026-07-30
  (S79), branch `change-metric-map`.** Money sub-mode `#moneymode` (Current /
  Change over time) + `#chgwindow` (Since 2012 / Since 2019), flat diverging
  choropleth, `/full/`-only, no pipeline work. **`verify-change.js`, 36 checks.**
  Full record in `SPEC_temporal.md` **§6b**; three rows in `DECISIONS.md`.
  ⚠️ **TWO OF THE BUILD NOTES BELOW WERE WRONG AND MEASUREMENT CAUGHT THEM** —
  read §6b before touching the metric:
  - **The rate had to become COMPOUND, not arithmetic.** `(last/first - 1)/years`
    is unbounded above (observed max **+2,076%/yr**) and gave the diverging ramp
    arms **108× apart**, so teal was owned by a few new subdivisions. Geometric:
    max +54%/yr, arms 6× apart.
  - **A SECOND degenerate endpoint existed.** The 45 no-baseline hoods were
    known; one hood *ends* at zero share and printed **`-100.00% / yr`**. Both
    ends are off-scale holes with distinct reasons now.
  - The years-elapsed trap flagged below was real and is avoided (13, not 12);
    it is `verify-change.js`'s first check, recomputed from the raw file.
  The sub-items below are kept as the record of how it was decided, not as work.
  Original ask: *"what I want is like, timelines
  options, for how much each hood has changed on average over time… and spike
  chloro map eventually. Like half the time going back, and all the way back in
  the dataset."* The shipped lens answers **one hood at a time**; this asks the
  same data for **all 406 at once**, which is where the fiscal story actually
  reads off the map.
  - **✅ NO PIPELINE WORK, NO NEW COLUMNS.** `web/data/temporal.json` (406 hoods
    × 13 years, already in the browser in `/full/`) has everything. Derive the
    change per hood **client-side** and join it onto `state.data.features` at
    load. Consequence: switching windows recomputes instantly with no refetch —
    and the whole family is **`/full/`-only**, like the lens it reads.
  - ⚠️ **A SPIKE MAP AND A SIGNED METRIC CONTRADICT EACH OTHER — this is the main
    design tension in the ask.** A prism cannot have negative height, and hoods
    moved **both** directions. **In-repo prior art settled this once already:**
    the Infill lens is a signed z-score and renders as a **flat plane with a
    dark-centred diverging ramp**, not spikes (`infillColorAt` / `INFILL_CENTER`
    / `INFILL_POS` / `INFILL_NEG` in `web/index.html` — symbols, not line
    numbers: those had already drifted 16 lines by the next day). Two honest
    options: (a) **choropleth only**, reusing `infillColorAt` — cheapest, and
    consistent with the one precedent; or (b) **height = |change|, colour =
    direction**, which is legitimate but has to be *said*, because a tall spike
    would then mean "moved a lot" in either direction. **Do not invent a third
    ramp, and do not force a sequential one** — the existing ramps are
    luminance-sequential by decision and cannot show a sign.
  - ⚠️ **THE 2024 GAP BITES AGAIN, IN A NEW PLACE — likely the feature's one
    silent bug.** "Average annual change" must divide by **years elapsed (13)**,
    never by **observed intervals (12)**. The gap means those differ, so dividing
    by intervals inflates every hood's annual rate by ~8%. Same class as
    index-vs-year positioning in the chart, so **make it the first verify check.**
  - **✅ THE GATE HAS BEEN RUN — `ANALYSIS_BACKLOG.md` §10, 2026-07-30. IT PARTLY
    FAILS, so read it before building anything here.** Prompted by Peter: *"I've
    already seen some graphs that have like, a peak in the middle. So straight
    average would be 0."* He is right, and the measurement turned up three things
    that outrank the hump. **Two recommendations this item previously carried were
    WRONG and are struck below.**
  - [x] ~~**DECISION 1 — which measure**~~ — **DECIDED 2026-07-30 (Peter):
    RELATIVE change, with the 45 undefined hoods rendered in the established
    off-scale grey and the reason stated.** Chosen over pp-with-a-sqrt-transform
    because that would rescale a metric which genuinely does not separate rather
    than fixing it — presentation papering over distribution, next door to the
    linear-elevation honesty choice. Cost accepted: **45 grey holes, and they are
    the new-growth areas** — visible absence rather than a wrong number. The
    measured basis is `ANALYSIS_BACKLOG.md` §10; the short version of the bind:
    - `last/first` **does not exist for 45 of 406 hoods (11%)** whose 2012 share
      is zero — Blatchford, Decoteau, Keswick, Glenridding Ravine, Graydon Hill,
      Rosenthal, Stillwater, the Anthony Henday segments. **Exactly the hoods a
      change map most needs to show.**
    - But percentage-point change, which *is* defined everywhere, **does not
      separate**: median hood **−0.032 pp** vs Downtown **−1.791 pp** (**56×**),
      and **15% of hoods move under 0.01 pp in thirteen years**. A pp choropleth
      is Downtown blazing over ~380 visually identical hoods.
    - **Rejected, for the record:** (b) pp with a sqrt/rank transform — see the
      reason above; and (c) relative from each hood's first non-zero year, which
      is defensible but silently puts a 3-year and a 13-year change on one ramp,
      **the comparability trap this project keeps meeting.**
    - [x] ~~⚠️ **Still to settle when it is built: what the 45 grey hoods say on
      hover.**~~ — **✅ DECIDED 2026-07-30, and the honest phrasing was the right
      one.** Hover reads `No 2012 baseline — held none of the assessment base
      that year`; the legend swatch says `No 2012 baseline — off-scale`. Both
      name the YEAR so the absence is checkable against the sparkline
      underneath, and `verify-change.js` asserts the string never contains "set
      aside". The window picker rewrites both to 2019 in the short window.
  - **DECISION 2 — endpoints, and the hump needs a SECOND NUMBER, not a different
    one.** ~~Recommend measuring whether endpoints and OLS slope disagree~~ —
    **measured: rho +0.959 over all 406**, so they are near-duplicates; **+0.719
    restricted to the 34 real humps**, which is Peter's point quantified. ⚠️ **And
    peak-drawdown does NOT fix it either — rho +0.919 against net change**, i.e.
    almost the same ranking. **So use endpoints (explainable, and no worse), and
    give a peaked hood its peak value + peak year as a second reading rather than
    hunting for a cleverer single number.** The panel already computes and shows
    exactly that (`peak share 5.55% in 2016`). Humps are **34 hoods (8%)**;
    71% of hoods are monotone and endpoint arithmetic describes them honestly.
  - **DECISION 3 — the windows. ✅ CONFIRMED WORTH HAVING.** Long (2012→2025) vs
    short (2019→2025): rho **+0.734**, and the sign **flips for 55 of 406 hoods
    (14%)** — so the two windows genuinely tell different stories for a seventh
    of the city, and the "timeline options" ask is not decorative. **Use the
    Development view's window-picker idiom (`#devwindow`: 3yr/5yr/long)** — direct
    in-repo precedent for exactly this control — rather than a free year picker.


- [x] ~~**UI: the pinned panel and the hover popup must not both be up — add an
  explicit MODE toggle**~~ — **✅ DONE 2026-07-30** (Peter: *"I don't want both the
  panel and pop up appearing at the same time… a button that will convert you to
  panel mode, or back to pop up mode"*). `#hoodmode` in `#opt-body` beside
  `#coloradj`, label-is-the-state (`Readout: popup` / `Readout: panel`), hidden
  until `temporal.json` loads so it can never offer a mode that does not exist.
  Regression net: **`tools/profiling/verify-hoodmode.js`, 31 checks.**
  - **Three gestures, three distinct effects — the layering is the design:** the
    **×** clears the pinned hood and stays in panel mode on its prompt; **Escape**
    and **the button** leave the mode. A click in **popup** mode enters panel mode
    *and* pins, which keeps the tooltip's own "click to pin" hint truthful.
  - ⚠️ **This CHANGED `verify-temporal.js`'s contract** and the script caught it:
    a second click on the pinned hood no longer *closes* the panel, it unpins and
    leaves the prompt. Two expectations were rewritten deliberately (and made
    stricter — inertness is now "state unchanged", not "stays closed").
  - **Popup mode** (default): the full hover tooltip, sparkline included.
    **Panel mode**: the tooltip reduced to the headline number + the panel.
    Clicking different hoods still works in panel mode — Peter accepted that it
    is harder.
  - [x] ~~**What happens to the readout in panel mode**~~ — **DECIDED (Peter,
    2026-07-30): the popup is NOT suppressed, it is REDUCED to just the primary
    metric.** *"reduce the popup to just the primary metric once you go panel."*
    So panel mode = a one-line hover (hood name + the view's headline number),
    with the panel carrying the history. Better than either option that was put
    to him: hovering stays useful while browsing hoods, and the objection was
    never "two surfaces at once", it was **two dense blocks competing**.
    - **The sparkline and the `click to pin` hint drop out entirely in panel
      mode** — the panel already draws the chart, so the teaser would duplicate
      it, and the hint is pointless once you are in the mode. Clean shape:
      `tooltipFor` = `viewTooltip` (reduced when in panel mode) **plus** the
      temporal block **only in popup mode**.
    - ⚠️ **DO NOT implement the reduction as "keep row 1".** It happens to be
      right for five of the six views — money, ratio, development, infill, and
      uses (whose primary is the dominant-use label, the mixbar and composition
      being the detail) — but **services is the exception**: its rows lead with
      `road_m_per_acre` whenever roads are present, *regardless of which service
      is driving the ramp*. A naive first-row rule would print road metres while
      the colour is driven by stormwater. **Services' primary is
      `state.svcDriver`'s number.**
    - The set-aside and no-data branches already return a single muted line, so
      they pass through the reduction unchanged.
  - [x] ~~**Where the button goes**~~ — `#opt-body` beside `#coloradj` (Tier 3:
    applies in every view, presentation not data), **not** the Display popover,
    which is accessibility. `CONTROLS_MATRIX.md` §3 updated: `#temporal` is no
    longer tier-less, `#hoodmode` is its control.
  - [x] ~~**The two smaller open ends**~~ — panel mode with nothing pinned shows
    a **prompt** ("Click a neighbourhood to see its assessment history"), because
    a button that appears to do nothing reads as broken; and the **× clears the
    pin only**, since the button that put you in the mode is the one that takes
    you out.


- [x] ~~**NEEDS A PHONE, NOT A BOX: confirm the double-tap-zoom fix (PR #107).**~~
  **CONFIRMED ON DEVICE 2026-07-27** — Peter, on a phone: *"double tap on phone
  no longer zooms in for the buttons, only the map."* Both halves of the design
  hold: the chrome no longer hijacks the gesture, and the map deliberately still
  does. Headless asserts the *mechanism* only (55/55 controls carry
  `touch-action: manipulation`, `#map` does not); the device check is what
  settled the *outcome*, per the tooltip precedent. See `DECISIONS.md`
  2026-07-27, `docs/MOBILE_USABILITY.md` §2b.
  - [ ] **Still open, one gesture:** nobody has actually **pinch-zoomed**. The
    fix deliberately avoids `user-scalable=no` (which would fail WCAG 1.4.4), so
    pinch should be unaffected — but that is reasoning, not a check. Fold it
    into the next phone session rather than making a trip for it.


- [x] ~~**LABEL SWEEP IS BLIND TO DOM CHROME.**~~ **DONE 2026-07-27.**
  `visibleLabels()` now culls labels landing under the HTML chrome, skipping
  them like the existing offscreen cull. Two calls worth knowing before
  touching it: `CHROME_IDS` omits `#layers`/`#coloradj` (borderless sections
  inside `#optpanel`, which is the box that actually paints) and *includes*
  `#title`/`#legend` (no background, but text-over-text is the reported case);
  and the chrome test is **unpadded**, unlike the label-vs-label sweep, because
  `LABEL_PAD` is inter-label breathing room and charging it against a panel
  edge cost DOWNTOWN on a phone. A verify check asserts `CHROME_IDS` covers
  every `.panel` in the document, so a future panel fails loudly. Measured cost
  none: readable-label counts identical (32/32 desktop, 25/25 at 390x844).
  See `DECISIONS.md` 2026-07-27, `docs/UI.md` "Labels dodge the chrome".
  - [ ] **Follow-on, unresolved:** on a phone the chrome covers ~45% of the
    screen, so labels are genuinely scarce there — the cull is correct but the
    underlying problem is that the panels are too big, which is
    `MOBILE_USABILITY.md`'s headline fix (collapse the blurb), not a label
    problem. Worth revisiting label density on mobile only after that lands.


- [x] ~~**PUBLIC BUILD SHAPE**~~ — **LOCKED 2026-07-28: two views, Money ·
  Development.** Peter: *"2 views is fine for release, lock it in."* The three
  provisional full-only tags (Uses, Services, Ratio) are settled, not pending.
  See `DECISIONS.md` 2026-07-28.
  - [ ] **Post-launch: return the pulled lenses ONE AT A TIME, each its own
    release** (Peter: *"we'll add the other stuff later, like one lense at a
    time"*). Not a batch un-pull. Each one needs its own decision, its own
    verification **in the public build**, and its own reason.
    - **Ungating is not just the `#views` line.** `CONTROLS_MATRIX.md` §2 names
      the three places a lens leaks: `tooltipFor`, the Data & Methods copy, the
      legend. Ratio in particular owns two Money-tooltip rows and Services owns
      the modelled-layers caveat + the road/fire/transit source credits.
    - Suggested order is **Ratio or Services first** — they share the roads
      fetch, so whichever lands first pays that cost and the second is nearly
      free. Uses is independent.


- [x] ~~**RIVER GEOMETRY IS UNTRIMMED AND UNCHECKED (audited 2026-07-27).**~~
  **CLOSED 2026-07-27 — NO ACTION.** The river is 95% of `reference.geojson`
  (2,316 verts, 50.7 kB) and `RIVER_SIMPLIFY_M = 25` is ~3× finer than a pixel
  at HOME zoom, with 104 islands = 35% of its vertex budget, 99 on the bare
  tails. Re-simplifying at 100 m would halve the file. The item was scoped as
  *one look decides it*, because there was never a performance argument (54 kB
  = 0.7% of a 7.7 MB payload) — only the visual question of whether the 52–95 m
  islands (~1 px) speckle the tails. **Peter looked on device: they do not.**
  With the only open question answered no, the trim buys nothing. Reopen only
  if speckle shows up at some zoom nobody has tried.


- [x] ~~**FLAKY TEST: `verify-uses-prisms.js` "money: control hidden again, state
  kept" (found 2026-07-27).**~~ **CLOSED 2026-07-28 — NO LONGER REPRODUCIBLE.**
  S71 measured it failing ~3 runs in 4; on 2026-07-28 the **unmodified master
  version passed 4/4**, and a scratch harness replaying the exact check at its
  own 1500 ms sample point passed **8/8**. Most likely already fixed by S73's
  PR #108, which repaired two "chrome read before it was final" ordering bugs in
  `applyView` — the same class that would make this check's `boxShown` /
  `sliderShown` conjuncts race. **Nobody proved that link**; the honest statement
  is only that it does not reproduce.
  - **The inherited diagnosis was wrong in a checkable way, and this is the
    reusable part.** It blamed `layerManager.layers` holding `uses-res-prisms`
    "for a beat" after a view switch. Measured: the managed list is stale only at
    **0 ms** (4 of 30 samples, all at delay 0); by **50 ms** it agrees with
    `props.layers`, and the check samples at **1500 ms**. So that mechanism is
    real but **cannot** explain a failure at the suite's sample point — and the
    check has four conjuncts, not just the layer one. A confident cause named in
    a handoff is still a hypothesis.
  - The probe was switched to `props.layers` anyway (2026-07-28) as **consistency,
    not a bugfix** — it was the only one of nine verify scripts reading deck's
    internal managed list, which also carries sublayers
    (`hood-labels-characters`, `…-polygons-fill`) and is genuinely stale at 0 ms.
    That makes it a latent trap if any delay in the suite is ever shortened.


- [x] ~~**SMALL OPEN UI DECISIONS (2026-07-25).**~~ **ALL THREE CLOSED 2026-07-26**
  (Peter decided; see `DECISIONS.md` 2026-07-26 for the reasoning on each).
  - [x] ~~Does `#coloradj` hide when it doesn't apply?~~ **Yes — built.** _Later
    the same day `#lens` was removed outright, which emptied that column for good:
    `#opt-pres` and `syncPresColumn` are gone and `#coloradj` moved to the BOTTOM
    of the Options panel (`CONTROLS_MATRIX.md` §5.1/§5.2)._
  - [x] ~~Should `#views` keep 14px on phones?~~ **No — stays 12.5px, one row.**
    Deliberate no-op, not an oversight: wrapping the primary control costs more
    than 1.5px buys, and 12.5px still out-ranks the 11.5px modifiers.
  - [x] ~~Center 2D: reframe vs flatten-in-place?~~ **Keeps reframing.** Deliberate
    no-op: the compass needle already does in-place north-up, and both Center
    buttons reframing preserves the only "put the camera back" recovery.


- [x] ~~**Residential revenue metric ("Residential $", Peter 2026-07-16)**~~ —
  **SHIPPED 2026-07-16.** The numerator decomposition Peter asked for (explicit
  residential tax dollars, vs the zoned-area fade lens): `res_levy`
  (RESIDENTIAL + OTHER RESIDENTIAL; MA DERELICT excluded → DECISIONS.md
  2026-07-16) → `res_revenue_per_acre` / `_per_lot_acre` → third Money metric
  + "N% of revenue is residential" tooltip line in all Money metrics.
  DATA.md §4 decomposition, UI.md "Residential revenue metric",
  `verify-res-revenue.js`. Follow-on:
  - [x] ~~**Glass grid file res columns**~~ — **SHIPPED 2026-07-17.**
    `export_value_grid.py` rolls `res_levy` into the 100 m cells
    (`res_revenue_per_acre` / `_per_lot_acre` appended to the payload);
    Glass renders real res cells instead of the hood-prism fallback. Size
    cost weighed: ~1.76 → ~2.1 MB raw (gzipped on Pages). DATA.md §4 "Glass
    grid variant", UI.md Glass bullet; columns reach live on the next weekly
    refresh (column guard until then).


- [x] ~~**Dev+Infill ROUND-2 delta audit**~~ — **EXECUTED 2026-07-16 (S56, same
  session the brief was written; this line was stale until 2026-07-17).**
  Dispositions in `session-summary/archive/2026-07-16.md` §2.D + `docs/AUDIT_LEDGER.md`:
  **0 DEGRADED**; D1+D2 CLOSED (L4→SOUND; denominator bias immaterial), D3
  numbers → recommend disclose-only, D6 SOUND (WATCH: orange clamp = p95 of a
  ~105-member arm). What's LEFT is the **post-audit copy PR** below.
  - [ ] **Post-audit copy PR (small, any model):** apply the D4 verdict-grammar
    copy ("Room to add, quiet lately" / "More building than room suggests" /
    "Activity ≈ room") + the three S56-proposed caveat texts (D2 denominator
    note, D5 z-compression + 0.50-cliff clauses, D3 suite-conversion
    disclosure) to `web/index.html` blurb/tooltip + `docs/SPEC_development.md`
    Lens B — pending Peter's picks on D4 grammar and the D3 fork
    (recommendation: disclose-only). Texts: `session-summary/archive/2026-07-16.md`
    §2.D.


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

## Cache-bust `styles.css` at build time — CLOSED 2026-08-02

Closed by stamping `styles.css?v=<content hash>` in `scripts/build_site.py`.
Full reasoning (why a content hash and not the commit sha, why a query and not
a hashed filename, and the limitation it does NOT cover) is the 2026-08-02 row
in `docs/DECISIONS.md`. Original item as it stood:

- [ ] **PROPOSE: cache-bust `styles.css` at build time.** Peter, 2026-08-01, on a
  phone after a successful deploy: *"i'm still not seeing the mill rates on
  mobile… i can see it when i open it in a private window on my phone. but it's
  refusing to show on normal safari."* The change was live and correct; his
  Safari held the old stylesheet. **This is new since 2026-07-29**, when
  `styles.css` was extracted out of `index.html` — a CSS-only change now ships in
  a separate file with its own cache lifetime, so a stale stylesheet renders
  against a fresh page and the feature looks half-deployed.
  - Both files serve `cache-control: max-age=600` with matching `last-modified`,
    so the intended window is 10 minutes; observed Safari behaviour was longer.
  - **Fix:** inject a version query on the `<link>` in `scripts/build_site.py`
    (content hash or commit sha). ⚠️ **Changes CI behaviour → propose, do not
    smuggle**, and ⚠️ that script's base-tag guard does a plain substring test
    over the whole source, which has already killed one deploy — anything near
    the `<head>` needs the guard re-run. Triage order: `RUNBOOK.md` §3c.
    *(The guard was scoped to the `<head>` slice on 2026-08-04, so the
    whole-source substring test described here no longer exists.)*

## A data-only refresh runs no front-end check — CLOSED 2026-08-02

Closed by `tools/profiling/verify-smoke.js`, gated into `refresh.yml` before
`upload-pages-artifact`. Full reasoning (why the existing suite was refused,
what the falsification and inverse tests found, and the two checks whose scope
is narrower than it looks) is the 2026-08-02 row in `docs/DECISIONS.md`.
⚠️ The item's premise that a refresh 'triggers no deploy' was FALSE — refresh.yml
deploys itself; the gap was an unchecked deploy, not a missing one. Original item:

- [ ] **PROPOSE: a data-only refresh runs no front-end check at all.** The
  narrow symptom is closed (see `## Done`, 2026-08-02) but the structural gap it
  exposed is not. `deploy.yml` is scoped to `web/**` minus `web/data/**`, so a
  refresh that rewrites `web/data/` triggers **no deploy**, and `refresh.yml`
  runs no verify script — a data change can therefore alter what the site
  renders with nothing on fire.
  - ⚠️ **Correcting this item's own former claim:** it used to say the temporal
    file "has no equivalent" of `check_value_anchors.py`. **False** —
    `scripts/check_temporal_years.py` exists, runs in `refresh.yml` before the
    status-manifest step, and **passed on the 2026-08-01 refresh**. The data
    side is guarded. What is unguarded is the *render*.
  - **Open question, not an obvious build:** the verify suite needs a browser
    and ~1 min/script, and the pipeline guards already cover data correctness —
    so a full suite on every refresh may cost more than it catches. A single
    smoke script over the panels that read refreshed data is the cheaper shape.
    ⚠️ **Changes CI behaviour → propose, do not smuggle.**

## `verify-smoke.js` guards the METRICS columns but not the SERVICES ones — CLOSED 2026-08-03

Closed by `verify-smoke.js` `B7`/`B8` **plus** `scripts/check_served_columns.py`
+ `data/expected_columns.json`. Full reasoning is the 2026-08-03 row in
`docs/DECISIONS.md`.

⚠️ **The item's prescribed fix does not catch the failure the item names**, and
that is the whole finding. It asked for *"present on every feature OR absent from
every feature, never partially"* — but a refresh that silently drops a service
column drops it from **all 406** features, which is "absent from every feature",
which that rule tolerates. Falsification F2 confirmed it: with `bike_m_per_acre`
deleted from every feature, B7 passes green. The tolerance is not removable
either — `bike_m_per_acre` was legitimately absent for exactly this reason
between the 2026-08-02 merge and the refresh that followed it, and failing on
absence would have redded the weekly publish over a column that was not supposed
to exist yet. Telling the two apart needs **memory of last week's schema**, which
no check derived from the served file can have; hence the committed baseline.

Two corrections to the item's own text, both found by reading the config:
`SERVICES` is **not** the whole list (Roads is a ground layer with no
`plane.col`, so `road_m_per_acre` appears only in `RATIO_DENOMS`), and the
service columns carry **no nulls at all** — set-aside is its own `is_set_aside`
flag, so the null-vs-undefined care B6 needs does not arise here, though the
check reads `undefined` anyway to keep the two families asking one question.

Original item:

- [ ] **`verify-smoke.js` GUARDS THE METRICS COLUMNS BUT NOT THE SERVICES ONES
  — a dropped service column is invisible by design.** Found 2026-08-02 while
  adding the bike lens. `B6` asserts every `METRICS` column is present on every
  feature, derived from the config; `B4` does the same for `USE_CATEGORIES`.
  **Nothing derives from `SERVICES`**, so the 7 service plane columns
  (`road_m_per_acre`, `bike_m_per_acre`, `transit_dep_per_acre`,
  `storm_charge_per_acre`, `water_charge_per_acre`, `fire_events_per_acre`,
  `svc_cost_per_acre`) are unguarded.
  - ⚠️ **The failure is SILENT BY CONSTRUCTION:** every services row
    self-gates on its own column, so a refresh that silently dropped one would
    simply hide the row. No error, no NaN, no banner — the exact "a dropped
    fact is this project's cardinal failure" case B6 exists for, on a surface
    that just grew from 6 rows to 7.
  - **Fix is cheap and mirrors B6:** derive the required column list from
    `SERVICES`' own `plane.col` values rather than listing them.
  - ⚠️ Must stay tolerant of legitimately-absent columns (an old data file, or
    a lens whose reviewed input has not landed) — the S87 cry-wolf lesson.
    Probably "present on every feature OR absent from every feature", never
    partially.

## Mobile chrome — the bottom-sheet question — CLOSED 2026-08-04 (no code change)

The last open piece of the mobile-chrome quick pass (`docs/MOBILE_USABILITY.md`
§3). Steps 1 and 2 shipped in `0089eba` and Peter confirmed the blurb collapse
on device; step 3 (the left-edge clip) closed 2026-07-31 as not reproducible.
What remained was **a decision, not a build item** — whether the flex control
column is enough on a phone or the controls should move into a bottom sheet /
hamburger.

⚠️ **The item was re-measured before being decided, and the basis had moved.**
The union coverage method reproduced the default state **to the decimal
(27.9%)**, so the deltas below are real movement and not method drift:

| state | recorded 2026-08-01 | measured 2026-08-04 |
|---|---|---|
| default (Money, folded) | 27.9% | **27.9%** ✅ |
| **Money UNFOLDED** | **54.3%** | **47.9%** ⬇ |
| Services unfolded *(full only)* | never measured | **53.1%** |
| Development unfolded | never measured | **52.7%** (public 44.7%) |
| Ratio / Uses unfolded *(full only)* | never measured | 37.4% / 31.6% |
| worst **public** state (Dev unfolded + peek) | never measured | **52.3%** |

⚠️ **THE ">HALF THE SCREEN" CLAIM WAS ATTACHED TO THE WRONG STATE.** The doc
named Money unfolded at 54.3%; it is now **47.9%, under half**, because
`#moneymode` left the Options panel for `#toggle` row 2 on **2026-08-02 — one
day after the measurement was taken**. The states that *are* over half
(Services, Development) had never been measured at all: the 08-01 pass took one
view and generalised from it.

⚠️ **A SECOND STALE LINE, FOUND ON THE WAY.** §3 claimed *"public `#views` is
now 4 buttons"*. It is **two — Money · Development**. Services and Ratio were
pulled to full-only on 2026-07-28 (`|| !FULL_BUILD`, the `applyView`
data-presence gate). This is load-bearing for the decision: **the public build
cannot reach the 53.1% state at all.**

**Peter's call: the column stays as-is.** The reasoning, recorded so it is not
re-opened on the old numbers:
- The >50% states are **transient and user-initiated** — reachable only by
  deliberately unfolding Options, and they fold away again. The **default**
  render, which is what a phone user meets first, is **27.9%** vs desktop's
  20.3% — about 7 points.
- The worst *public* state (52.3%) needs an unfold **and** a neighbourhood tap,
  and the peek card is the answer to that tap. Rendered and eyeballed: nothing
  clips, nothing overlaps, the middle ~40% of the map stays clear.
- A bottom sheet is a refactor of **shared desktop+mobile DOM**
  (`CONTROLS_MATRIX.md`: grouping drives both) — real desktop regression risk
  for a state the user can dismiss.

⚠️ **`#views` POSITION (the "too far from the map" hierarchy question) LOSES ITS
VEHICLE.** It had been parked pending "the move-2 fork", which this refuses. It
now needs its own proposal if it is ever revisited.

**Still genuinely open and NOT closed by this** (own item): the Services panel
grouping has never been touched on a **real phone** — the geometry is measured
clean at 390/360/320, but real-device touch and the **folded default** state are
unconfirmed, and the verify scripts drive `.click()`, which bypasses
`pointer-events`.

⚠️ **Tenth time a carried item's stated basis did not survive re-measurement —
and the first where re-measuring CLOSED the item instead of redirecting it.**

---

## Replace the derived $14.135M roads-maintenance figure — CLOSED 2026-08-04

**Closed by correcting it, not by confirming it.** The item read *"it is the one
soft number in that table; the other three are quoted directly"* and framed the
work as *"a single value swap plus dropping `derived_component`"*. The swap was
indeed a single value — but the figure being replaced was **about 5× too low**,
and it had been **live on a public page since the 2026-08-04 manual refresh**.

### The original figure and why it failed
`$1,285/km × ~11,000 km = $14,135,000`. Two inferences stacked: a narrow unit
rate from Taproot reporting, multiplied across the citywide network, with the
**snow-clearing** network reused as a maintenance denominator. Against the
City's own published program the implied rate is **~$5,900/km**, not $1,285/km.

⚠️ **The error was in the repo's derivation, not in the source.** Taproot's
*totals* hold up; only the rate×network product did not. That distinction is
what the cross-check below establishes, and it matters — the instinct on finding
a bad number is to distrust the source.

### What was found
`https://budget.edmonton.ca/api/operating_budget.csv` — the City's Open Budget
portal, **program-level, machine-readable, FY2017–FY2026**, 7,283 rows. Now
`DATA.md` **§17**. The Approved Operating Budget PDF stops at branch level
(`Parks and Roads Services`, FY2026 gross $303.361M) where roads are bundled
with parks — 6× the whole roads row, and unusable for this.

### The cross-check that exposed it
| | |
|---|---|
| Published `Snow and Ice Control` program, FY2025 | **$67,553,815** |
| Pod's roads snow $36.85M + path snow $30.15M | **$67,000,000** |
| | **99.2%** |

Same source, two numbers: the snow figures reconcile almost exactly, the
maintenance figure was out by 5×. **The asymmetry is the finding.**

### Why FY2017, a stale vintage
**It is the only year Edmonton ever published a roads-only maintenance
program** (`Roadway Maintenance`, **$65,671,000**; alongside `Snow and Ice
Control` $63,709,000 — a 1.03 ratio, where the pod's derived figure implied
0.38× its own snow, **4.9× apart**). The tree was **re-cut in 2018** into
`OPS/PARS - Infrastructure Maintenance`, which also covers sidewalks, pathways
and bridges — using it would **double-count against this table's own sidewalks
and bike-lane rows** — and **re-cut again in 2026** into `Mobility
Infrastructure Services`. Peter's call: **roads-only scope beats matching
vintage, documented rather than silently mixed**, the same call already made for
ETS 2025 vs fire 2026. Being 2017 dollars it is if anything a **lower bound** —
the branch grew ~34% ($244.9M → $327.1M) by 2025.

### Effect
Roads **$50.985M → $102.521M**, i.e. **1.33% → 2.67%** of the operating budget;
transit:roads **9.2× → 4.6×**. `derived_component` dropped, so the pod's public
asterisk is gone. Transit, bike and sidewalk rows unaffected.

⚠️ **Because nothing downstream pins a share, this was a one-value edit** — the
UI divides. That is the second time a number in this table has been corrected
after publication, and the standing argument for the no-pinned-ratios rule.

### Guarding it
`test_committed_budget_file_shares_are_what_we_claim` **failed on the change, as
designed**, and was updated with a warning that moving it is correct only
alongside a sourced value change. A new
`test_committed_budget_roads_maintenance_is_no_longer_derived` pins the value
and the absence of `derived_component` against a revert.

---

## Tighten the cardinality-guard bands — CLOSED 2026-08-05 (four of six)

**The item said "tighten the bands once there is variance data." The variance
data existed, and it said two different things about the six anchors.**

### Where the variance data was
Not in git, and not in the baseline file — **the guard prints every anchor value
in CI on every run**, and those logs are retrievable. Harvested from the
`refresh.yml` runs' job logs.

⚠️ **`gh run view --log` returns nothing even for a COMPLETED run here; the jobs
API works.** Quirk (qqqq) had recorded the in-progress half of this; the
completed half is new:
```bash
JOB=$(gh api repos/PeterFriedrich/edmonton-tax-viz/actions/runs/<id>/jobs -q '.jobs[0].id')
gh api "repos/PeterFriedrich/edmonton-tax-viz/actions/jobs/$JOB/logs"
```

⚠️ **Five runs, but only THREE independent observations.** The 2026-08-02 and
2026-08-05 runs committed `status.json` only, so their anchors re-measure
unchanged input. Checking *what each auto-refresh commit actually touched* is
what separates a real observation from a re-reading.

### What it showed
| anchor | observed spread | action |
|---|---|---|
| `dup_parcel_points` | 0.00% (constant 33) | tightened 2× |
| `lot_needle_ratio` | 0.00% | tightened 2× |
| `dedupe_effect_pct` | 0.01% | tightened 2× |
| `dup_parcel_value_frac` | 0.11% | tightened 2× |
| `ineligible_points` | 7.1% | ⚠️ **left wide** |
| `ineligible_value_frac` | 22.3% | ⚠️ **left wide** |

**The last two are not noisy — they are trending**, monotonically upward on
every independent data change, with no reversal:
```
ineligible_points      56 -> 58 -> 60
ineligible_value_frac  0.00517 -> 0.00575 -> 0.00633
```
That is the **dangerous** direction by the guard's own `DANGER` map. Tightening
them to observed spread would have red the weekly publish on the next real data
change and read as a false alarm rather than the regime signal the guard exists
to give. `ineligible_value_frac` has consumed ~72% of its band already.

### Two things the item got wrong
1. **Its prescribed mechanism cannot express the result.**
   `--write-baseline --tolerance` applies ONE global tolerance to every anchor.
   The bands are now hand-set per anchor — which needs **no code change**, since
   the comparator reads `min`/`max` per key and ignores `_`-prefixed notes — and
   that flag would silently flatten them back. Recorded in the baseline's own
   `_bands_are_per_anchor` field and pinned by a test.
2. **"Observed spread" is the wrong target anyway.** The guard exists mainly for
   the **January year-roll**, and **no observation across a year-roll exists** —
   it shipped 2026-07-28. Three weekly readings say nothing about reassessment,
   so ±25% buys a real 2× tightening while leaving room for the event the guard
   was built for. Going tighter is a decision for after the first January roll.

### Guarding it
Three tests, none of which existed before (nothing pinned the committed baseline
at all): every CI reading must stay in band; the drifting pair must stay wide;
the four tightened anchors must stay at ±25%. ⚠️ **The tightening test was
falsified against the old baseline first** — it fails there and passes here, so
it pins the change rather than merely describing it.

## Finish the doc-citation sweep: `src/`, `scripts/`, `tools/` — CLOSED 2026-08-09 (S103)

Opened 2026-08-08 by S102, which swept only `web/index.html` (40 sites, 14 docs)
and found a **wrong number live on the site**. The other three trees cite docs
too and had never been checked. Closed by sweeping them: **216 citation sites
across 51 files**, triaged to the ~20 that back a falsifiable number or a data
contract — the rest are bare "see `SPEC_x.md`" pointers with nothing to be wrong
about.

**Method (the part worth reusing):** every numeric claim re-derived from
`data/raw/` rather than compared against the doc text — point-in-polygon for the
containment counts, a chunked scan of the 363 MB fire feed, feature counts on
the road/bike GeoJSONs, groupby on the historical aggregate. Then
`git log -S '<figure>'` **paired with** `git show <commit>:data/DATA.md` to
separate a citation that *drifted* from one that was *never right* — S102 used
only the first half, and only the pairing distinguishes the two.

**Three defects, all comment-level; nothing wrong reached shipped data.**

1. ⚠️ **A line-number citation drifted.** `tools/audit_exempt_institutional.py`
   cited the institutional zone codes as *"DATA.md line ~308"*. `git show` at the
   authoring commit proves it was **right on 2026-07-09**; DATA.md has grown
   ~240 lines since, so line 308 now lands on `Total Gross Area`/FAR. Re-pointed
   at **§5 "Set-aside categories"**. The project already bans line-number
   citations for `CODEMAP.md`; this was the same failure one file over.
2. **A unit mislabel.** `src/load_temporal.py` justified `COMMERCIAL_CLASSES`
   with *"NONRES MUNICIPAL/RES EDUCATION is 19 rows across all 14 years"*. **19
   is the account count; rows are 16.** The locked decision is unaffected (still
   noise on single accounts) but the stated evidence was not what it claimed.
3. ⚠️ **S102's own follow-up note was FALSE and is retracted.** It recorded that
   `web/index.html` self-flags `SPEC_temporal.md` §2 as stale and *"the doc was
   never updated"*. `git log -S` shows §2's **READ FIRST banner and that very
   comment landed in the same commit, `7e065ef`** — the doc was updated the day
   the comment was written. The comment was **obsolete on arrival**, pointing
   readers at a §2 that already opens with the correction. Rewritten to send
   them to the banner.

**One imprecision, stage now stated.** `load_temporal.py`'s *"32 historical names
have no current boundary"* reproduces **only** at the shared-`NAME_CORRECTIONS`
stage while counting the `""` null bucket (3 null rows) as a name: 31 + 1. Raw
is **41**; after both correction layers, **25**. The nulls are *not* a silent
drop — `normalize_hood` does `fillna("")`, so they survive into the denominator
and get reported, which is what trap 2 requires.

**Verified correct and left alone** (re-derived, not compared): roads **53,720**
and bike **10,417** features (exact); fire noise `TRAINING/MAINTENANCE`
**18,144** / `COMMUNITY EVENT` **2,491** / `PRE-INCIDENT PLANNING` **515**
(exact); `ZONE_CATEGORY` **95** base codes; `gross_area` null/zero **6.19%**
(DATA.md's own 27,202 / ~6.2% exact); the historical aggregate at **14,842**
rows with the class dimension costing **9,265** ("~14,800" / "~9,300"); spatial
containment **945/946** and **100/103** (exact); **0** null coordinates in the
current roll; permit geocoding **94.8–98.0%** for 2009–2023 and **71.6%** for
2025; OLIVER's straggler at exactly **1 row / $500**; the census anchor
**459,859**; and every DATA.md section number cited (§2/§5/§10/§11/§13/§14/§15)
plus `SPEC_temporal` §0.1–§0.4.

**Two left deliberately unchanged.** `SPUR LINES` is a second unmatched name
($0, 1 row), so `load_assessment.py`'s *"the lone remaining unmatched name"* is
**correct only in scope** — the zero-value drop runs first, so SPUR LINES never
reaches that join — and it is documented in three places; the two texts
reconcile only if you know the ordering. And `load_stormwater.py`'s **$49.8M**
unbilled is a difference the cited doc never states (§3 gives $240.4M and
$190.5M, rounded difference **$49.9M**) — within rounding of the unrounded
inputs, but a derived figure with no source.

**Successor:** the `docs/` tree itself is still unswept, and docs cite each
other constantly. See `## Open work`.

## The Services lens has no hood panel — BUILT 2026-08-10

Closed 2026-08-10. The panel confronts revenue per acre with each service
cost, grouped by basis, with **no total** — forced by the two no-sum rules
(`DECISIONS.md` 2026-08-10, `docs/SPEC_services.md` "Hood panel").
`verify-peek.js`'s Services block was rewritten: the invariant is "a tap
produces a readout", not "a tap opens the card".

- [x] **The Services lens has no hood panel — build the service-specific one.**
  Opened 2026-08-06. Clicking a hood in Services now does nothing by design
  (`hoodPanelLens()`; `DECISIONS.md` 2026-08-06): the assessment-history panel
  was the wrong content there, so it was gated out, and Peter's stated intent is
  *"we'll probably have something service specific"*. Until that exists the lens
  is hover/card-only, which is a **complete** readout — this is a feature gap,
  not a defect, and nothing is currently broken by leaving it.
  - **What the panel would hold (undecided — this is the actual open question,
    not the plumbing):** the per-service rows already exist in the tooltip, so a
    panel that only repeats them earns nothing. The candidate that would justify
    it is the **cost-vs-revenue confrontation** the Ratio view gestures at —
    this hood's modelled service cost per acre beside its revenue per acre — but
    ⚠️ the cost terms carry incompatible bases (`DATA.md` §13: `roadway_om_renewal`
    lifecycle vs `roadway_ops` operating, ~10.8× apart, never to be summed or
    compared), so any such panel needs its basis named on screen or it becomes
    a headline number that is arithmetically true and descriptively false.
  - **The plumbing is already in place and is the cheap half:** flip
    `hoodPanelLens()` for services, give `#temporal` a third render mode beside
    `renderHistory` / `renderRevenueMix`, and point `#peek-go` / `#temporal-hint`
    at it — all three advertisements already follow the lens.
  - ⚠️ **Re-read the `verify-peek.js` Services block before touching any of
    this.** It encodes a regression that reached production (the card is the
    ONLY per-hood readout on touch); the checks there are what stop it
    recurring, and they must keep passing in whatever the panel becomes.

---

## `gross_area` null-vs-zero in `far` — CLOSED 2026-08-22

- [ ] **⚠️ `gross_area` MISSING AND `gross_area` ZERO ARE THE SAME NUMBER IN THE
  GRID PATH — a cell with no data emits `far = 0`, which reads as maximum infill
  opportunity.** Measured 2026-08-22: the field is null/zero on **6.25% of
  eligible rows**, `build_hood_lot_acres` / `_cell_lot_metrics` sum it with
  `NaN → 0`, and at 100 m grain **16.2% of cells land on `far == 0` with 100% of
  their own properties missing the field** (median). 3,964 in-scale cells tie at
  the identical maximum opportunity score.
  - **The fix:** emit `null` where no property in the unit has a usable
    `gross_area`, the way `median_year_built` already does for year (*"age has no
    meaningful zero"* — same argument, same file).
  - ⚠️ **The SHIPPED hood lens is NOT wrong today** — reproduce before "fixing"
    the live output. 69 in-scale hoods exceed 50% missing but **only 2 are
    residential**, so the asymmetric residential gate bars the rest from the teal
    end anyway. The defect is real; its blast radius at hood grain is 2 hoods,
    both with 3–4 eligible rows.
  - ⚠️ **The gate absorbing a DATA gap is undocumented behaviour** — `SPEC_development.md`
    Lens B justifies it purely as a land-use filter. Worth stating there, because
    it is precisely what the gate cannot do per-cell.
  - Prerequisite for any cell-grain FAR. Full measurements:
    `docs/FINDINGS_infill_granularity.md`; open work:
    `docs/ANALYSIS_BACKLOG.md` §12.

**Outcome:** fixed in `build_hood_lot_acres` (null and zero both masked, `min_count=1`), +3 tests. 16 of 410 hoods go null; 12 were already set-aside grey. EVERGREEN leaves the Infill scale and `SPEC_development.md` Lens B was amended — its teal was never a measurement. ⚠️ **PARTIAL coverage is still open** (MAPLE RIDGE, ~33% recorded, #2 on the teal arm): `docs/ANALYSIS_BACKLOG.md` §12. Full reasoning: `docs/DECISIONS.md` 2026-08-22, `docs/FINDINGS_infill_granularity.md` §6a.

---

- [ ] **Wire `check_temporal_archive_year.py` into the monthly vintage digest.**
  Unblocked 2026-08-27 — it exits 0 now, so gating no longer means holding the
  site over an open decision. `vintage-digest.yml` already holds `issues: write`
  and already opens `⚠️`-titled issues, and `DECISIONS.md` 2026-08-26 named it
  the honest home for a guard that cannot gate a publish but must not go quiet.
  ⚠️ **CI change → propose the plan first** (`CLAUDE.md` Comments & Scope).
  Rejected once already: warn-only inside a green run, which reaches nobody.

**Outcome (2026-08-27, PR #258):** wired, and **no CI change was needed** — the digest already runs `vintage_report.py` and already folds ⚠️ into the issue title, so it is a check function plus a `CHECKS` entry (membership IS the wiring, and a test pins it). Reuses `filed_bases()`/`detect_year()`/`archived_residential_bases()` so the digest and the standalone guard cannot disagree. Reads only committed files, so it cannot fail on the network. Two deliberate reporting choices: a year outside `fir_tax_base.json` is named NOT CHECKED and never counted as passing, and a green over ONE archived year carries its own thin-population caveat. ⚠️ **A false alarm was found in the same file and fixed**: `check_assessment_roll` compared the coverage string to our pin itself, bypassing `check_alignment()`'s 2026-08-25 stale-metadata downgrade, and would have reported "Roll has moved to 2025, pin is still 2026" every month starting 2026-09-01 — recorded as issue 1's THIRD consequence (`docs/DATA_ISSUES.md`, PR #259).

---

- [x] **CLOSED 2026-08-30 — the 15 hardcoded activity-window labels now read from
  one constant, and drift fails the build.** Audit F4, opened 2026-08-28.

  Original item:
  - `FIRE_YEARS` / `PERMIT_YEARS` / `PERMIT_YEARS_RECENT` are restated as
    literals across 15 user-facing sites in `web/index.html` (`DEV_WINDOW_LABEL`
    alone feeds 5 render sites). **All correct today** — only because the
    project is younger than one year-roll.
  - Step 4 bumps the pins and re-runs the deflator, and says the drift guard
    means a stale pin "can't be missed silently". **True of the pin, false of
    all 15 strings.**
  - ⚠️ **This is the `(2024 n/a)` defect (S122) at 15×**, with the same tell:
    correctly-derived copy sits beside it (the vintage footer reads
    `status.json`).
  - **Not a one-line fix:** `status.json` carries no activity window, so the
    browser cannot derive these. Closing it means `generate_status.py`
    publishing the three windows — an **output-schema change**, propose-first.
    ⚠️ **Do not ship the cheap partial alone** (a RUNBOOK line + a test pinning
    label against pin) without deciding: a half-fix that makes step 4 *look*
    complete is its own hazard.

**Outcome:** closed the other way round from what the item proposed. The
`status.json` route was **rejected on measurement, not cost** — the manifest is
fetched async and lands after first render (`web/index.html`, the STATUS_URL
fetch), so every label would still need a literal fallback and the fix would
have created **two** sources of truth rather than removing one.

Shipped instead: a single `WINDOWS` block in the tunables, `${WIN.<key>}` at
every JS site and `{{<key>}}` placeholders in the seven static tooltips,
substituted at parse time. `tests/test_window_labels.py` (4 tests) asserts
`WINDOWS` equals `main.py`'s pins, that both change windows end at
`ASSESSMENT_YEAR`, that no user-facing string spells a range out, and that every
placeholder names a real key. RUNBOOK §1 step 4 now names the second edit.

⚠️ **Scope grew by one lens on Peter's call**: `CHG_WINDOW_LABEL` /
`CHG_WINDOWS` (2012–2026 / 2019–2026) carry the same defect on a different pin
and were folded in. Their ends stay PINNED rather than read off `temporal.json`
— the 2026-08-27 phantom-year decision — and the comment saying so was kept and
amended rather than deleted.

⚠️ **The four remaining literals in the file are comments**, one describing an
unrelated ASTER window that happens to share a range; the guard strips comments
for that reason. The other three were reworded to stop restating years.

Verified: mutation (a stale pin and a reintroduced literal each fail the guard),
760 tests, and the live page — all six ranges render byte-identical to before,
no unsubstituted token, no page error. Full reasoning: `docs/DECISIONS.md`
2026-08-30.

## CLOSED 2026-09-01 — the 50 m grid as an ADDITIONAL OPTION (the scope correction)

**Resolved by:** a third `#moneydetail` button. Peter: *"let's do the 50m option,
keep 100m as default. Can 50m not just be a third option"*. Both answers the item
was blocked on came at once — **100 m is the default**, and the control is a
**third button**, not a separate cell-size row.

**How each design note landed** (all of them held; none needed re-deriving):
- Both files ship. `value_grid.json` went back to **100 m** and
  `value_grid_50.json` is new — the canonical unsuffixed path holds the DEFAULT.
- `gridData` became the ACTIVE grid over a per-resolution `gridStore`, and the
  fetch gate reads the **cell size**, not `!gridData`. The memo caches
  (`cellsFor`/`instFor`) hang off the parsed object, so one shared slot would
  have served 100 m memos against 50 m cells.
- **Infill PINS the default** rather than following the switch — the third-button
  shape made this the obvious answer, since Infill is not in that row. Its band
  percentages are resolution-dependent, so a Money control silently moving them
  would be a reading changing under a control that does not appear to touch it.
- `lot_needle_ratio` anchors on the **fine** file. The grid is read for exactly
  one anchor, and the 100 m grid demonstrably masks the defect that anchor
  exists to catch (12 vs 79 on identical data), so the ±50% re-pin stands.
- Button labels stayed `CELLS` pins (both name a fixed shipped resolution, so
  both are correct at parse time); prose describing the grid ON SCREEN reads
  `glassCellLabel()` off the loaded file.

⚠️ **The verify script's first version was vacuous** — it asserted the default
only after clicking the 100 m button, which SETS the value it was about to read,
so it passed with the default pinned to 50. Caught by falsification, not review.

Full reasoning: `docs/DECISIONS.md` 2026-09-01 (third row of that date).

### The item as it stood when it closed

- [ ] **⚠️ SCOPE CORRECTION — the 50 m grid was meant to be an ADDITIONAL
  OPTION, and shipped as a REPLACEMENT.** Opened 2026-09-01, immediately after
  PR #293 merged. Peter: *"i wanted it as an additional option, not literally
  just change it to 50."*
  - **What is live now:** Glass renders 50 m only; 100 m is gone from the
    served data and from the UI. `web/data/value_grid.json` IS the 50 m file.
  - **What was wanted:** both resolutions, user-switchable in the Glass view.
  - ⚠️ **Do NOT fix this by reverting #293.** Everything in it is wanted and
    most of it is resolution-independent — the `CELLS`/`{{token}}` label fix,
    `verify-tokens.js`, the `lot_needle_ratio` re-pin, `DATA_ISSUES.md` §E,
    the `GRID_CELL_M`/`DEV_GRID_CELL_M` split. **A revert would throw away a
    real data-defect find to undo a default.** Build the option on top.
  - Design notes already established, so this does not need re-deriving:
    - Both files must ship. 100 m is **1.05 MB** gzipped, 50 m is **2.74 MB**;
      each is lazy, so fetch only the one selected and the cost is per-choice,
      not additive. First load is untouched either way.
    - ⚠️ **The label mechanism already half-solves it.** `CELLS` pins the
      DEFAULT (known at parse time, which is the constraint that forced a pin —
      the grids are lazy, so a data-derived label is empty on first paint).
      Once a user switches, the label can read `cell_m` off the loaded file,
      because by then it HAS loaded. Pin the default, read the switch.
    - `gridData` is a single slot — it needs to key by cell size, or refetch.
      `ensureGridData()` fires for Glass **and** Infill; the amenity bands read
      `dist_lrt_m`/`dist_school_m` off whichever grid is loaded, and **those
      band percentages differ by resolution** (LRT 1.59%→1.43%, school
      37.81%→42.34%). Decide whether Infill follows the switch or pins one.
    - ⚠️ **`lot_needle_ratio` is calibrated for 50 m now** (±50%, one degenerate
      cell sets it). If 100 m becomes selectable again the guard still only
      measures the SERVED default — decide which file it anchors on.
  - Open question for Peter: **which resolution is the default**, and does the
    control live in `#moneydetail` (a third button beside Neighbourhood) or as
    a separate cell-size row that appears only in Glass? See
    `docs/CONTROLS_MATRIX.md` — grouping is shared DOM, so it drives mobile too.

## Monthly-digest check for `functional_class_code` vocabulary drift (closed 2026-09-09, S151)

- [ ] **DEFERRED, Peter 2026-09-09 (*"we'll do that next time"*) — NOTHING DETECTS
  A NEW `functional_class_code` UPSTREAM.** The road feed's enumeration was
  recorded as **closed at 15 values** (`data/DATA.md` §6, 2026-07-01) and it
  **grew**: `Alley-Commercial` appeared later, missed `CLASS_GROUP`, and
  `_classify`'s fail-open default (`DEFAULT_GROUP = "local"`) **charged 106 m of
  alley as local road** until 2026-09-09 (fixed, PR #378). ⚠️ **The fix does not
  close the hole — only that one instance of it.** `_classify` warns on an
  unmatched code, but into a log nobody reads; that warning had been firing on
  every pipeline run. And ⚠️ **`test_every_alley_prefixed_code_is_the_alley_group`
  must NOT be quoted as drift protection** — it iterates the keys that are
  present, so a MISSING key makes it vacuously true. **Measured, not assumed:**
  deleting `Alley-Commercial` leaves it GREEN and only
  `test_alley_commercial_is_excluded_from_the_metric` reds by name.
  **The shape to build:** compare the feed's `functional_class_code` vocabulary
  to `CLASS_GROUP` in the **monthly digest** — exactly what `check_zoning_bylaw`
  does for the zoning bylaw's zone codes (`scripts/vintage_report.py`, DECISIONS
  2026-09-08), including its two lessons: report **both directions** (a code that
  DISAPPEARS is half of what a rename looks like), and an **empty upstream
  vocabulary must return UNKNOWN, not ACTION**, or a renamed column conjures a
  bylaw replacement. ⚠️ **Not taken because it changes digest behaviour** —
  propose-first per `CLAUDE.md`. ⚠️ **Also open, and the more general question:**
  whether fail-open-to-`local` is right at all. It is deliberate (*"no silent
  data drops"* — an unknown code keeps its length in the metric), but it silently
  picks the **charged** side, and for an `Alley-*` code that was the wrong one.

## `_classify` fail-open-to-`local` (closed 2026-09-09, S151)

- [ ] **OPEN, and the more general question the digest check does NOT settle:
  should `_classify` fail open to `local` at all?** It is deliberate (*"no silent
  data drops"* — an unknown code keeps its length in the metric) but it silently
  picks the **CHARGED** side, and for an `Alley-*` code that was the wrong one
  (`Alley-Commercial`, 106 m, 2026-09-09). ⚠️ **`check_road_classes` makes the
  event VISIBLE within a month; it does not change which way the fallback errs
  in the meantime.** The alternatives are fail-closed (drop the length — a real
  silent drop) or a third `unknown` group carried out of `road_m_total` and
  reported. **A decision about which error to prefer, not a build task.**

### The pointer-style index files drifted off their own contracts (opened 2026-09-04 — CLOSED 2026-09-09, S152)

- [ ] **PETER'S CALL — trim `docs/DECISIONS.md`'s rows, or rewrite its header to
  describe what the file has become.** Full measurement:
  `docs/FINDINGS_decisions_index_drift.md`. ⚠️ **Do not start trimming before this
  is decided** — the two options point opposite ways and only one is reversible
  cheaply.
  - **The drift:** the header promises *"one line per locked decision… the
    one-sentence why… duplicates no rationale"*. One-line and the pointer column
    both hold (247 rows; only 3 lack a pointer). **The one-sentence rule is at 13%**
    (median 6 sentences, max 19), and the median row went **138 → 2,219 chars
    between 2026-05 and 2026-09** — 16×, with **no `DECISIONS.md` line reopening the
    format**. The Decision column is 88% of the 367 KB file.
  - ⚠️ **Duplication is real but PARAPHRASED, not verbatim** — median 8-gram overlap
    with the pointed-to doc is only **4%**, while **98.8% of distinctive facts are
    recoverable elsewhere in the repo**. That is why four months of review never
    caught it: there is no wording to match on.
  - ⚠️ **`docs/AUDIT_LEDGER.md` has the same drift** — median **1,941** chars/row,
    max 5,416, under a header that says *"Rules (mirror `DECISIONS.md`): … one-line
    verdict + pointer, never duplicate findings or rationale here."* **Fixing only
    `DECISIONS.md` treats the instance, not the cause.**
  - **If the answer is trim:** ~8 values live **only** in `DECISIONS.md` and must be
    rescued into their owning docs first — `0.06%` (L205), `$14,048.73/acre` +
    `$234,399` (L223), `258px`/`272px` (L226–227), `$161.3M` (L245),
    `$88,038,783/yr` (L258), `152/167/319 ms` (L287). A trim touches **12 of 247
    rows** destructively; the rest is safe.
  - **If the answer is rewrite the header:** the case is that four months of authors
    chose the long form every single time, which is evidence the file became a
    useful decision *log*.
  - ✅ **THE DECIDING QUESTION IS NOW MEASURED (2026-09-09, S152 — §7 of the
    findings), AND IT NAMES A THIRD OPTION.** Two of the longest rows were read
    against the doc they point at (L231 → `SPEC_revenue.md`, L284 → `UI.md`):
    **both fully recoverable, and the target doc RICHER than the row** — all three
    of L284's reasons in order, Peter's verbatim ask included. ⚠️ **A grep test
    would have answered this backwards** — *"SHARE decides the WORDS"* and
    *"inherits the right gating for free"* appear nowhere else, yet both arguments
    are present, paraphrased (§2 measured 4% n-gram overlap, so phrase-absence
    tests are vacuous here and this had to be READ).
  - ⚠️ **THE DEFECT IS THE POINTER COLUMN, NOT THE DECISION COLUMN.** **23 of 272
    rows carry no `.md` pointer**; exactly **one (`L196`) has no pointer column at
    all**; **18 are long**. Those are the only rows where a trim could destroy an
    argument, and `L153` (CSS extraction, code-only pointer) is told in
    `UI.md`/`STACK.md`/`TOKEN_EFFICIENCY.md` anyway — so **23 is an upper bound.**
  - ⚠️ **THE FIRST COUNTS I PUBLISHED HERE WERE WRONG AND SO WAS §1's.** Rows carry
    pipes **inside inline code** (`L62`/`L145`/`L146`/`L196`/`L261`), so a naive
    `split("|")` reads the wrong field as the pointer; three successive parses gave
    35, 26, 22 before the method was pinned. **The pointer is the LAST field.**
    §1's *"only 3 rows have an empty pointer"* was the same artifact — it named
    `L145`/`L146`/`L261`, **all of which have full pointers**, and could not see the
    one row that has none. ⚠️ **My `L146` example was backwards**: I offered it as
    an unpointed row whose reasoning I had *found* in `PLAN_public_release.md` —
    the row already pointed there. Corrected in `FINDINGS_decisions_index_drift.md`
    §7, and §6's reproduce script fixed. **§3's 1,295-facts/16-unique numbers were
    NOT re-derived and read the same columns — re-run before trusting the trim's
    blast radius.**
  - **▶ THIRD OPTION, and it is right under EITHER of the two above — PETER'S
    CALL:** complete the **pointer** column on those 23 rows, longest first.
    Append-only (which is what the header already claims the file is),
    non-destructive, reversible, and it is **the prerequisite a trim already
    needs** — after it the trim's blast radius is re-measurable and §3's ~8
    orphaned values are the only true rescues left.
  - ✅ **THE POINTER PASS IS DONE (2026-09-09, S152): all 272 rows carry a doc
    pointer, 0 remaining**, verified by `check_doc_citations.py` — every addition
    resolves, guard at its 2-warning baseline. **Nothing was trimmed and the header
    was not rewritten**; the trim-vs-bless call is still yours and is now cheap to
    act on either way. ⚠️ **8 of the 23 landed on a doc that never names the row's
    symbol** (`RIVER_COLOR` appears only in the generated `CODEMAP.md`) — placed on
    heading semantics instead, because per §7 the docs paraphrase and
    symbol-absence refutes nothing. Those 8 are the ones to re-read if a pointer
    ever looks wrong.
  - **▶ NEXT, IF YOU WANT THE TRIM:** re-run §3's uniqueness sweep with the
    corrected splitter (its 1,295-facts/16-unique numbers predate the fix), then
    rescue the ~8 values that live only here.
  - ⚠️ **Still open either way:** whether the long form should be *blessed*. The
    measurement says the long rows are **redundant**, not **harmful** — and §3's
    size-the-remedy rule applies to the header rewrite too. `DECISIONS.md` has
    also grown **367 KB → 412 KB since 2026-09-04**, so waiting is not free.
  - **Gate:** nothing is blocked on this. It costs money only when a doc-heavy
    session loads these files — which is what surfaced it.

---

## Closed sub-items lifted out of still-open parents — 2026-09-16 (S166)

These shipped. They were sitting inside parent items in `TODO.md` that are
**still open**, so `tools/todo_archive.py` could not move them — it operates on
top-level closed items only. Lifted by hand so the file every session reads
carries live work; the parents stay open in `TODO.md` with a pointer here.
Verbatim as they stood. **Nothing here is a to-do.**

### From: **THE LAB IS OPEN AS A CONTAINER — one experiment in it, and the only

- [x] **CHECKED ON A PHONE — Peter, 2026-08-12: "lab on phone is fine."**
  ⚠️ **This is an EYES-ON confirmation on a real device, which is the thing a
  probe could not give us** (the standing caveat: verify scripts drive
  `.click()` and bypass `pointer-events`). It is **not** a measurement — no
  width numbers were captured, so if the `#views` row or the title box grows
  again, this closure does not cover it. The untested axis was **WIDTH**: six
  buttons wrapping at `max-width: 640px`, "Lab" widened by its `beta` tag, and
  a title box that went **217 → 258 → 314px in one day** against Money's 176px.
  Desktop verified at 1440x900 / 1400x900 / 1366x768 / 1280x720 / 1024x768;
  worst `#botleft` clearance 215px at 1280x720, so vertical was never the
  worry. ⚠️ **Still live for the NEXT change:** Development's 442px blurb is
  what collides below 768px tall, so an addition to that blurb needs
  re-measuring rather than assuming, and remove `.folded` from `#optpanel`
  before measuring Options rows or every probe returns zeros (the trap this
  file records three times now).

### From: **CARDINALITY GUARD — two small follow-ons (guard shipped 2026-07-28, PR #110).**

- [x] **Tighten the bands — DONE 2026-08-05, but only FOUR of six.** See the
  `## Done` line; the split and its reasoning live in
  `data/expected_value_anchors.json`'s own `_why_two_widths` /
  `_ineligible_pair_was_NOT_drifting` fields.
- [x] **WHY IS VALUE LEAVING THE LOT-ACRE DENOMINATOR? — CLOSED 2026-09-03: it
  wasn't. The trend was one step with an invented midpoint.** See the `## Done`
  line.

### From: **GEOGRAPHIC REFERENCE LAYERS — TIERS 2 & 3 (Tier 1 shipped 2026-07-27).**

- [x] ~~**Tier 3b — the REGIONAL NAMES, beyond the seven towns.**~~ **DONE
  2026-08-08 (PR #187), live in production.** The four counties, the
  Industrial Heartland, Nisku and the airport are named; Morinville and Stony
  Plain joined the towns (16 names, 33 features). Edmonton's limit is drawn
  with its own stroke but **deliberately unnamed**. ⚠️ **This reversed the
  2026-07-27 "regions are unlabelled" decision** — see `DECISIONS.md`
  2026-08-08 and `DATA.md` §14 before re-opening it. ⚠️ **Tier 2 below
  inherits a hard-won constraint from it:** outlines are split into one layer
  per stroke with CONSTANT accessors, because a per-feature `getLineColor`
  builds a per-vertex attribute buffer and blew the verify's click timeout.
  Style a new Tier-2 shape by adding a layer, never by adding an accessor.
- [x] ~~**Tier 3 — the NAMES half.**~~ **DONE 2026-07-27.** Seven regional
  place names ship on by default (St. Albert, Sherwood Park, Spruce Grove,
  Fort Saskatchewan, Leduc, Beaumont, Devon). Split out from the boundaries
  deliberately: the names needed no polygon fetch, and bundling them was what
  made Tier 3 look expensive. See `DECISIONS.md` 2026-07-27 (×2),
  `data/DATA.md` §14, `docs/UI.md`.
- [x] ~~**Tier 3 — the BOUNDARIES half (still open).**~~ **DONE 2026-08-08 —
  and this item was ALREADY HALF-STALE when it was worked.** The neighbouring
  municipalities' outlines had shipped with the *names* half back on
  2026-07-27 (`reference-boundary`, seven polygons); what was genuinely
  missing was **Edmonton's own legal limit and the rural municipalities**,
  which this item never asked for. Both now ship as `REGIONS` in
  `scripts/build_reference_layers.py`: Edmonton + Strathcona / Sturgeon /
  Parkland / Leduc County, unlabelled, unfilled, under the data.
  ⚠️ **What it exposed is the durable part: the hood fabric is not the city.**
  Legal boundary **782.1 km²** vs **672.4 km²** of rendered hoods → **109.6
  km², 14.0% of Edmonton, has no neighbourhood at all** and had been reading
  as background. One-directional (0.0 km² of fabric outside the limit), so
  the map understates the city and never overstates it. **No metric moves**
  (all are per-hood), but a future *citywide-per-acre* figure must state which
  denominator it means. `DECISIONS.md` 2026-08-08, `data/DATA.md` §3 + §14.
  Original notes below, kept because the sublayer traps are still live:
  Alberta `urban_and_rural_municipality` MapServer, natively **EPSG:3400**.
  **Sublayer IDs confirmed:** Edmonton / St. Albert / Leduc are all in
  **78 (`City`, field `CITY_NAME`)**; **Strathcona County is in 104
  (`Specialized Municipality`, `SPMUN_NAME`) — NOT 114
  (`Municipal District and County`)**, which holds Leduc/Sturgeon/Parkland
  *County*. Ids 67/95/105 are group layers and return no fields. Note the
  names half needed a *third* sublayer, **66 `Urban Service Area`**, for
  Sherwood Park — the hamlet-like service area of Strathcona County, which is
  a different thing from the County polygon in 104.
- [x] ~~**Which end of the stack do boundaries belong at?**~~ **ANSWERED
  2026-07-27 for the neighbours, and 2026-08-08 for the regions: UNDER the
  data, with the river.** The neighbours sit outside Edmonton where there is
  no hood fabric to hide them (measured: 0–0.7% of each outline overlaps the
  city), so underneath they are fully visible AND can never cut across a
  prism. ⚠️ **Edmonton's own limit is the one case that argument does NOT
  cover** — it is the only outline that runs *through* the fabric rather than
  outside it. Under the data is still right (an over-composed line would
  slice the prisms it crosses), but it means the limit is partly hidden where
  hoods meet it, and fully visible exactly along the 14% that has no hood —
  which is the read we want.

### From: **MOBILE USABILITY (NEW 2026-07-22 — full plan in

- [x] ~~**DECIDE FIRST: control regrouping**~~ — **DECIDED 2026-07-23** (8
  decisions, `CONTROLS_MATRIX.md` §7 + `DECISIONS.md` "Controls & lens grouping").
  All 7 §5 combos closed. Final shape: `#views` = 5 (Money · Services · Ratio ·
  Uses · Development); Glass → mode of Money; Infill + Industrial → full-only Dev
  extras; palette + Labels → an accessibility menu; stack reordered
  View→Variant→Presentation; "Residential only" → "Highlight residential"; Dev
  grid+spike → one 3-way Detail selector. `public|full` tags all resolved in the
  same pass (public = Money/Services/Ratio/Uses/Development-activity; `/full/`
  adds Infill + Industrial + deep data-detail). **Nothing built yet.**
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

### From: **INDUSTRIAL & NON-RESIDENTIAL LENS FAMILY (NEW 2026-07-18 — full plan in

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

### From: **PUBLIC RELEASE PREP (NEW 2026-07-09 — scope + rationale in

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
  - [x] ~~**Peter — one manual step left: create `HEARTBEAT_TOKEN`.**~~ —
    **DONE. Verified 2026-09-16: `gh secret list` shows `HEARTBEAT_TOKEN`
    created 2026-08-31**, so `refresh.yml`'s `secrets.HEARTBEAT_TOKEN ||
    github.token` now takes the first branch and the prevention half is live,
    not dormant. ⚠️ A fine-grained PAT **expires** — if the weekly schedule
    goes quiet again, re-check this secret before anything else
    (`RUNBOOK.md` §3).

### From: **GROWTH INFRASTRUCTURE FINANCING PANEL ("Debt Lens") — NEW 2026-07-14

- [x] **D0 — catchment polygons BUILT 2026-07-15** (approximate, reviewable).
  `data/levy_catchments.geojson` (10 units) via
  `scripts/build_levy_catchments.py`; QA overlay + area validation confirm the
  footprints match Schedule A. Two flags for a future reviewer (editable
  `CATCHMENT_HOODS` dict): **Blatchford under-covers** (catchment > mapped
  hood) and **Riverview 1.65** (maybe drop `RIVER'S EDGE`). Full writeup:
  `docs/FINDINGS_offsite_levy_catchments.md`. Detail below ↓
- [x] **D0 detail — catchment polygon acquisition — DONE (verified 2026-09-16:
  `scripts/build_levy_catchments.py` exists, and
  `docs/FINDINGS_offsite_levy_catchments.md` records the resolution).** The 12 fire-hall off-site levy
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

### From: **DEVELOPMENT & INFILL LENS family (NEW 2026-07-12 — full plan in

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

### From: **Views & lenses follow-ons — its own three asks are all DONE (verified

- [x] ~~**Residential-only lens in the Ratio view.**~~ ⚠️ **BUILT 2026-07-03 and
  REMOVED 2026-07-26** (redundant with the Residential revenue cut); the cited
  `verify-lens.js` is deleted. Kept as the record of what happened, not as a
  description of the app. Done 2026-07-03:
  non-residential kept hoods fade to the lens grey (height untouched), log
  colour anchors rescale to the residential kept subset (≤ $258 … $916+ vs
  $264 … $3,253 — FINDINGS §6.4 addendum), lens button disables in the Roads
  view (state persists). Headless-verified (`tools/profiling/verify-lens.js`
  + screenshot); UI.md updated. **PR #9 merged + deployed** (run 28646374983;
  deploy step needed one transient-error rerun); live site verified serving
  the new code.
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

### From: **Deployment follow-ons (deferred, see `docs/SPEC_deployment.md`):**

- [x] ~~Year-mismatch **guard**~~ — built 2026-07-01 (`scripts/check_year_alignment.py`
  + `refresh.yml` wiring): detects the roll year from Socrata metadata; on mismatch
  skips regen, keeps serving committed data, auto-sets the holding banner. See
  SPEC as-built notes + `docs/FINDINGS_data_integrity_audit.md` §3.
- [x] ~~**Heartbeat watch:**~~ DONE 2026-07-26 — didn't wait for it to sleep;
  added the repo-scoped PAT (with fallback) *plus* a client-side staleness
  banner. Same item as P2.2 above; see there for the remaining manual step.
- [x] Optional tidy — DONE (verified 2026-09-16: all six already gone from
  origin): delete merged branches (`feature/phase2-web`,
  `feature/deployment`, `chore/node24-actions`, and the three audit-session
  branches from 2026-07-01: `docs/data-integrity-audit-brief`,
  `fix/name-corrections-audit`, `feature/year-alignment-guard`).

### From: **Data-integrity audit follow-ons** (first run 2026-07-01, **second run

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

### COLD-LOAD COST HAS NEVER BEEN MEASURED ON THE WIRE — CLOSED 2026-09-17 (measured; nothing to change)

- [x] **COLD-LOAD COST HAS NEVER BEEN MEASURED ON THE WIRE** (NEW 2026-08-07,
  out of the stack comparison in `docs/VIZ_STACK.md` — read §1 and §5 first).
  Every payload number in this project is an **on-disk** number. Pages gzips, so
  what a first-time visitor actually downloads is unknown, and no decision about
  payload should be made until it is.
  - ⚠️ **DO NOT re-file this as "we ship 16.1 MB".** That is the size of
    `web/data/`, not a page weight, and reading it as one is the specific error
    this item exists to stop. **Boot awaits exactly ONE file** —
    `neighbourhood_value_per_acre.geojson`, 1.04 MB on disk (re-measured
    2026-09-16; `web/data/` has since doubled to 16.1 MB while the boot payload
    got *smaller* — the 7.63 MB `value_grid_50.json` is lazy). Everything else is a
    memoized `??=` single-flight fetch gated on the view that needs it
    (`gridFetch`, `zoningFetch`, `roadsFetch`, `devGridFetch`, …).
  - ⚠️ **LAZY LOADING IS ALREADY DONE — do not "add" it.** It was proposed
    2026-08-07 after spotting the pattern on `map.kunicki.app/assessment/`
    (their `prop_details/<slug>.json`), then withdrawn on reading our own code:
    ours is the same idea applied more broadly, to bigger files. Recorded in
    `VIZ_STACK.md` §2 so it doesn't get re-proposed a third time.
  - **What is actually unmeasured, and the whole of this item:** gzipped wire
    size of (a) the 2.02 MB of vendored libraries — deck.gl 1.19 + maplibre 0.78
    + CSS 0.06 — and (b) the 1.04 MB boot GeoJSON. **The libraries are now nearly
    DOUBLE the boot geometry uncompressed** (they have not changed; the boot file
    shrank), which is not what anyone assumed; JS and GeoJSON don't
    gzip at the same ratio, so the ordering can flip on the wire and must be
    measured, not reasoned about.
  - **Only then is there a decision to make.** If boot geometry dominates, the
    lever is simplification / coordinate quantization of that one file. If the
    libraries dominate, there is no cheap lever — dropping deck.gl is refused on
    feature grounds (`VIZ_STACK.md` §3, §4B) and vendoring is refused on
    offline-verification grounds (§6). A measurement that changes nothing is
    still the correct outcome here.
  - **Not known to be a problem.** Nobody has reported the site as slow. This is
    "we have never looked", not "we found something".

**OUTCOME (2026-09-17, S168) — measured on the live site; the payload decision is
"no change", which the item itself names as a correct result.**

Method: headless Chromium against `https://peterfriedrich.github.io/edmonton-tax-viz/`,
zero interaction, cross-checked two ways (per-request `sizes().responseBodySize`
and the page's own `performance` `transferSize` — they agree to 0.02%). Full
table in `docs/PERFORMANCE.md` §"The cold visit, end to end".

- **Cold visit = 2.05 MiB gzipped over 12 requests**; critical path **948 KB**.
- **The ordering does NOT flip, it widens.** Libraries lead boot geometry 1.94×
  on disk and **3.13× on the wire** — GeoJSON gzips at 5.76×, minified JS at
  3.57×. Libraries are **62.5%** of the critical path. Per §5 axis 4's own rule
  that means **there is no cheap lever**, and trimming the boot GeoJSON attacks
  the smallest of the three terms.
- ⚠️ **THE ITEM'S PREMISE WAS STALE.** It asserted "every payload number in this
  project is an on-disk number" and the wire cost "unknown". False since
  **2026-08-10**: `PERFORMANCE.md` §Payload has carried per-file gzip figures,
  explicitly headed "Measured over the wire", and mine agree with it to ~2%. The
  genuinely open question was narrower — *does compression reorder the terms* —
  and that one was real. `todo-can-lag-executed-work`, again: the premise should
  have been re-checked before the measurement, not after.
- ⚠️ **MY FIRST RUN MANUFACTURED A FALSE HEADLINE AND IT FLATTERED ME.** Run 1
  reported `value_grid_50.json` (8.0 MB) fetched at boot — a dramatic "the lazy
  architecture is broken" finding. It was **my instrument**: calling Playwright's
  `response.body()` on the app's `HEAD` probe materialized a body that never
  crossed the wire. The real request is a **394-byte HEAD**, exactly as
  `index.html`'s own comment says ("the fine grid is never prefetched"). Caught
  by re-running with methods recorded. `measurements-that-favour-me` +
  `check-where-the-value-can-be-wrong`.

**Three side-findings, all corrected in place:**
1. **`VIZ_STACK.md` §1 listed `temporal.json`, `reference.geojson` and
   `dev_history.json` as toggle-driven. They are unconditional boot fetches** —
   three adjacent lines in `index.html`. `PERFORMANCE.md` had it right the whole
   time, so **the two docs contradicted each other for five weeks**;
   `dev_history.json` was counted as boot cost in neither.
2. **The app shell is a third budget nobody was accounting for.** `index.html`
   alone is **147 KB gzipped — 15.5% of the critical path and 77% of the boot
   GeoJSON**, which is the term every payload discussion compares against. It
   grows with every lens added.
3. **Pages serves gzip only — no brotli, no zstd** (probed per-encoding, and
   confirmed with a browser sending all four). Brotli would take another ~15–20%
   off the minified JS and is **not a lever we hold**.

⚠️ **Deliberately NOT built: a wire-size regression guard.** It needs network in
CI and is a new merge-gate behaviour, which `CLAUDE.md` says to propose first.
The numbers above are a snapshot and will drift with every data refresh — open
question for Peter, not something to slip in.

### RE-MEASURE the mobile coverage ceiling — CLOSED 2026-09-17 (re-probed; ceiling 53.5%)

- [x] **RE-MEASURE the mobile coverage ceiling — the 2026-08-04 figure is stale
  by construction.** `docs/MOBILE_USABILITY.md` measured "the public build
  cannot reach the worst state" and a **52.3%** public ceiling when public
  `#views` was TWO buttons. It is now **four** (Services returned 2026-09-02,
  Ratio 2026-09-11), so the Services-unfolded **53.1%** state is publicly
  reachable and the ceiling is simply unknown. Flagged in place 2026-09-11
  rather than re-derived, because the per-view percentages still stand and only
  reachability moved. **The work is one re-probe of the live public build**, not
  a re-measurement of every state. ⚠️ The bottom-sheet refusal that cites this
  ceiling did not rest on it alone, so this does not re-open that decision.

**OUTCOME (2026-09-17, S168) — re-probed; the public ceiling is 53.5%, and the
predicted mechanism was wrong.**

Live public build, 390×844, union method (2px grid, `CHROME_IDS` + `EXTRA_IDS`).
**Validated before use:** it reproduces three of `MOBILE_USABILITY.md`'s own
figures to the decimal — default **27.9%**, Money unfolded **47.9%**, Development
unfolded + peek **52.3%** — and two consecutive runs were byte-identical.

| public state | union |
|---|---|
| default (folded) | 27.9% |
| Ratio unfolded | 30.8% · + peek 35.9% |
| Services unfolded | 38.8% · + peek 42.2% |
| Development unfolded | 44.7% · + peek 52.3% |
| **Money unfolded** | 47.9% · **+ peek 53.5% ← ceiling** |

- ⚠️ **THE ITEM'S PREMISE WAS WRONG.** It expected Services returning public to
  carry its 53.1% in. **Public Services unfolded is 38.8%** — the public build's
  Services is roads-only, and 53.1% was a *full-build* panel (measured 62.7% on
  `/full/` today). The 53.1% state is still not publicly reachable.
- ⚠️ **THE CEILING ROSE VIA A STATE NOBODY HAD MEASURED, AND IT WAS ALREADY
  WRONG IN AUGUST.** The worst public state is **Money unfolded + peek**. The
  table lists Money unfolded (47.9%) and default + peek (34.5%) separately but
  never their combination, and all three affordances were public on 2026-08-04
  too — so **52.3% was an understatement when written, not drift.** That is the
  table's own rule ("name the state and name the view") failing on the table.
- ⚠️ **`Development UNFOLDED 52.7%` IS INTERNALLY IMPOSSIBLE.** A union cannot
  shrink when a rect is added, yet the next row has Development unfolded **+
  peek** at 52.3%. Re-measured: **44.7%** unfolded, 52.3% + peek — consistent,
  with the +peek figure reproducing exactly. 52.7% is wrong, not changed.
- **The full build is now 66.1% at its worst** (Services unfolded + peek; Money
  61.8%, Development 65.0%). **Not comparable** to the August full-build rows —
  `#budget-pod` did not exist then and is present in every full state now. Public
  does not carry the pod.
- **The bottom-sheet refusal is NOT re-opened**, as the item said it would not
  be: it never rested on the ceiling alone, and a transient 53.5% is the same
  order as the transient 52.3% it replaces.

⚠️ **A measurement trap worth keeping: my first two sweeps recorded "+ peek"
states in which no peek card ever opened.** The tap went to the map centre, which
the unfolded Options panel swallows in Money and Development; a later fix tapped
a *chrome-free* pixel and still missed, because that pixel was off the city
polygon. Both runs printed a confident, plausible ceiling (47.9%) built on a
state that did not exist. Fixed by scanning candidate pixels centre-out and
**asserting `#peek` is actually visible before recording the row**.

### Sliver-floor audit follow-on — the boundary-allocation RULE (OPEN 2026-09-22 S187)

From `docs/FINDINGS_sliver_floors.md` §1. Already done: the limitation is
recorded and sized (`data/DATA.md` roads Known Quirks, `SPEC_services.md`
annotated, DECISIONS 2026-09-22), the tooltip gate shipped (`verify-smoke.js`
§C11), and the two false comments were fixed. **Open: whether to apply an
explicit rule** for road that lies on a hood boundary, since today ~0.2 m of
digitizing noise picks the side. Options to cost: 50/50 split between the two
hoods (moves 25 published hoods > 5%), or keep as-is. ⚠️ Changes published
numbers and `ward_rollup.py`'s basis, so propose before building (CLAUDE.md).
Bike: same mechanism, 2.5 km.

**CLOSED 2026-09-22 (S188): equal split built** — Peter chose 50/50 after two external research replies (`/home/opc/research/edmonton-tax-viz/road_cost/boundary_road_*_2026-09-22.md`). `load_roads.split_boundary_pieces` (`BOUNDARY_TOL_M` = 2 m), applied to the roads metric, the roads web colour driver and bike. DECISIONS 2026-09-22 (S188 row) carries the measured sizes and tests.

### Dataset-requests notebook fixes (OPEN 2026-09-23 S190)

From `docs/FINDINGS_dataset_requests_notebook.md`. The page is public and states one false sentence. Nothing applied yet.

- [x] §5a prose: delete "Utilities & drainage is the only topic … more refusals than completions". Property also has more (11 vs 10) (§4).
- [x] Topic regexes: `\bbus` → `\bbus(?:es)?\b`, `tree` → `\btrees?\b`. Transit falls from 50 to 30 (§3).
- [x] Split the 2023-06-07 and 2023-09-19 backlog sweeps out of "Refused" (16 rows), drop `ODR19-269` "test", re-state the headline: ~61 decided refusals, ~3.3× (§2).
- [x] §5e: call the ~11% a floor; the date anchor is bulk for 57 of 152 CLOSED rows (§5). Decide `~d.moved` vs `~d.reintake`.
- [x] §6 Issue 4 prose: cite `ODR23-363` first; it was refused in 2023 and is the closest precedent (§6).
- [x] Re-render and re-inject the mobile CSS; update the index blurb if the headline changes.

**CLOSED 2026-09-23 (S190):** all five applied in one PR and re-rendered; 10 of 10 invariants. Decided refusals 61, naive overstatement 3.3×, Transit 50 → 30. The §5e `~d.moved` no-op was removed and the 53 re-intake rows kept on purpose: they are CLOSED requests like any other.
