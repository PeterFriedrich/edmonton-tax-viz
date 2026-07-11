# Decisions Index

Append-only, one line per locked decision: when, what, the one-sentence why
(including what was rejected), and where the full reasoning lives. This file
**duplicates no rationale** — it exists so a contributor can find where a
decision is argued without reading every doc. When a decision locks, add a
line; when one is superseded, strike it (`~~...~~`) and add the successor —
don't delete history.

Status of anything still open lives in the owning SPEC doc, not here.

---

## Analysis unit & denominators

| When | Decision | Full reasoning |
|------|----------|----------------|
| 2026-05 (Phase 1) | **Neighbourhood, not parcel, as the unit** — parcel boundary polygons are licensed (ADP/AltaLIS), not open data; roll points + boundary polygons are. | `docs/PARCEL_LEVEL_OPPORTUNITIES.md`, `data/DATA.md` |
| 2026-05 (Phase 1) | **Boundary-polygon acres as the default denominator**, EPSG:3400 projected before any area calc — one consistent acre across every metric. | `docs/ARCHITECTURE.md` Key Decisions |
| 2026-05 (Phase 1) | **Condo records included as-is** — many units on one land record inflating $/acre reflects real density, not an error. | `docs/ARCHITECTURE.md` Key Decisions |
| 2026-07-05 | **Repeat-aware lot dedupe heuristic** for any lot-area sum (condo rows repeat the parent lot; majority-null multi-unit points are ineligible, excluded + reported). | `docs/FINDINGS_lot_dedupe.md` |
| 2026-07-08 | **Ground-acre stays the default; lot-acre ships as an editorial alternative** ("per developable acre" toggle, suppressed below 15% parcel land) — ground-acre is cardinality-robust, not Urban3 lineage. | `docs/FINDINGS_denominator_cardinality.md` |

## Revenue methodology

| When | Decision | Full reasoning |
|------|----------|----------------|
| 2026-06 | **Municipal-only tax**, not education requisition. | `docs/SPEC_revenue.md` |
| 2026-06 | **Keep both metrics** (assessed value/acre AND revenue/acre, web toggle) — the gap between them IS the class-differential mill rates; hiding one is less transparent. | `docs/SPEC_revenue.md` |
| 2026-06 | ~~Tax-exempt: flag via `is_exempt` + include~~ **Superseded 2026-06-29**: exempt institutional land is absent from the taxable roll entirely (the flag catches 3 parcels), so exempt-heavy hoods understate — recorded as a limitation, separation done by the zoning layer instead. | `docs/SPEC_revenue.md`, `docs/FINDINGS_exempt_institutional.md` |
| 2026-06-29 | **Set-aside = never-land + not-yet-land ≥ 0.90 of area** (zoning overlay; grey, off the colour scale) — the near-zero spike is undeveloped land, not exempt land. Zoning is a refreshed input so developing land graduates off the list automatically. | `docs/SPEC_revenue.md` update, `docs/FINDINGS_revenue_scale.md` |
| 2026-06-29 | **Explicit hand-assigned code→category dictionaries, never keyword/prefix heuristics** (zone codes; later road classes and runoff coefficients follow the same rule) — place-names like "Energy & Technology *Park*" break fuzzy matching. Unknown codes warn loudly. | `docs/FINDINGS_revenue_scale.md`, `src/load_zoning.py` |

## Services & utility lenses

| When | Decision | Full reasoning |
|------|----------|----------------|
| 2026-07-01 | **Roads metric = City-maintained collector + local centreline metres only** — arterials computed but excluded (shared infrastructure), alleys/railway excluded at the row filter. | `docs/SPEC_services.md` |
| 2026-07-05 | **Stormwater = the Bylaw 20865 charge modeled from open data** (A × I × R, I = 1.0, SIAP credits out of scope) — always labeled MODELED, never billed-accuracy. | `docs/SPEC_utilities.md` Lens 1 |
| 2026-07-05 | **Fire = demand only** (dispatches/acre/yr): no on-scene-arrival timestamp exists in the data, so a response-time/coverage claim is NOT buildable — don't oversell. Medical ~57% share is a caveat, not a filter; window pinned to last 3 full years (auto-rolling could dilute with a partial year). | `docs/SPEC_services.md` "Fire lens" (all four locked decisions) |
| 2026-07-06 | **Water lens: residential scope only; tariff vintage pinned independently of the roll year** (a forward-looking modeled bill, unlike mill rates which must match the roll). | `docs/SPEC_utilities.md` Lens 2 |
| 2026-07-07 | **Franchise lens: columns only, no display layer** — modeled electricity/gas revenue is collinear with dwelling count, so a map of it would just be a dwelling map; value is citywide totals + per-hood attribution. Shares ONE dwelling model with the water lens. | `docs/SPEC_utilities.md` Lens 3 |
| 2026-07-02/03 | **Ratio metric (revenue per road metre) is derived client-side in the browser** — the acres cancel, so no pipeline stage computes it; scale anchors computed at page load so they track refreshes. | `docs/ARCHITECTURE.md` data flow, FINDINGS §6.4 |
| 2026-07-10 | **"Total services" stays PER-SERVICE (Ratio-view denominator picker: road metre \| fire event)** — modeled EPCOR dollars (storm/water) never sit under the levy (money-flow honesty); a combined denominator waits on published city unit costs (V2, rejected for now as a new cost model without sources in hand). | `docs/SPEC_utilities.md` decision 3, `docs/FINDINGS_revenue_scale.md` §6.7 |
| 2026-07-11 | **Transit = scheduled supply only (mean-weekday GTFS stop-events/acre; bus + LRT combined, per-mode internal)** — no stop-level ridership exists (citywide-monthly only), so never present as usage; on-demand zones absent from GTFS (limitation); full lens incl. web display, AMENDING the 2026-07-09 release-scope lock that kept transit out (Peter's call). | `docs/SPEC_services.md` "Transit lens" (both locked decisions) |
| 2026-07-11 | **LRT track lines added as a transit context layer (Capital/Metro/Valley); HER heritage streetcar EXCLUDED** — the track lines match the measured ETS LRT service only; the volunteer-run High Level Bridge streetcar is not in the GTFS routes we count, so drawing it would show unmeasured track. Context layer, not part of the metric. | `docs/SPEC_services.md` "Transit lens" Display; DATA.md §9 |

## Display honesty

| When | Decision | Full reasoning |
|------|----------|----------------|
| 2026-06-25 | **Linear elevation, no power curve** — a super-linear transform exaggerates (2× reads ~4× at k=2), unacceptable for scrutinised civic numbers; "Downtown's spike IS the story". Spike emphasis remains OPEN, held. | `docs/ARCHITECTURE.md` Phase 2 visual tuning |
| 2026-06-25 | **Display-geometry-only transforms: 45 m setback then 10 m simplify, in that order** — order cuts the served file 4× (9,229 vs 38,607 vertices); all metrics computed from true full-resolution area upstream, so display geometry can never change a number. | `docs/ARCHITECTURE.md`, `docs/PERFORMANCE.md` |
| Phase 2 design | **MapLibre + deck.gl directly, not Kepler.gl** (a UI wrapper — less control); **extruded real neighbourhood polygons, not H3 hexes** (the shapes mean something to Edmonton readers); **no basemap v1**. | `docs/ARCHITECTURE.md` Phase 2 design decisions |

## Deployment & operations

| When | Decision | Full reasoning |
|------|----------|----------------|
| 2026-06-28 | **Push, not pull; static, not served** — a weekly GitHub Action regenerates committed data and deploys static Pages; no server, no database, no runtime backend. Data changes ~annually; traffic is a CDN problem, not a compute problem. | `docs/SPEC_deployment.md` (incl. the rejected dedicated-server alternative) |
| 2026-07-01 | **Git is the change detector; `status.json` is heartbeat + provenance + banner** — re-run on schedule, commit only if output changed, publish the vintage. | `docs/SPEC_deployment.md` "Decisions settled" |
| 2026-07-01 | **Mill rates are a manual, reviewed input — never auto-fetched**; a roll-year/rate mismatch puts CI in a HOLD (keep serving committed data + banner), never a regenerate. | `docs/SPEC_deployment.md` "Year alignment", `scripts/check_year_alignment.py` |
| 2026-07-06 | **Year pins are manual** (`ASSESSMENT_YEAR`, `FIRE_YEARS` in `main.py`) — anything auto-rolling can go wrong silently; see the RUNBOOK's January checklist. | `main.py` comments, `docs/RUNBOOK.md` |
| 2026-07-09 | **Public release ships on the existing Pages site — no new hosting or engineering** pre-release. | `docs/PLAN_public_release.md` |
