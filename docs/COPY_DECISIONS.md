# Reader-facing copy decisions

Opened 2026-09-14 (S157). **A working list, not a spec** — each row is a decision
that has not been made. Decide a row, then apply it to *every* surface it names in
one pass: the failure mode this file exists to prevent is fixing the wording in one
panel and leaving the other three saying something else.

Every item has an id (`N1`, `J2`, …) so a `DECISIONS.md` row can cite the item
instead of restating the wording.

**Measured against the built site on 2026-09-14**, not estimated:

- **9** reader-facing `levy` strings (4 control tooltips, 2 panel headlines, 2 panel notes, the mill-pod note)
- **17 / 17** dead-even split on `modelled` / `modeled`; `neighbourhood` 129 / `neighborhood` 0
- Services panel verified **byte-identical across all ten service layers** (driven by probe, panel diffed)
- `revenue_per_acre` across 406 hoods: p05 $197 · p25 $12,994 · **p50 $18,060** · p75 $25,936 · p95 $41,674

Status column: `open` · `decided` · `applied`. Add the date when it moves.

⚠️ **10 rows APPLIED 2026-09-18 (S172), in one pass** — N1–N6, C1, C3, J4, S2
(Peter's call; `DECISIONS.md` 2026-09-18). **The noun is `city tax` / `city
property tax`**, and "municipal levy" is gone from every reader-facing surface
(2 mentions survive in HTML comments only). ⚠️ **Nine verify scripts asserted on
the old strings and were updated with the copy** — `verify-peek`,
`verify-revenue-panel` (**4 occurrences, and the 4th was missed on the first
pass and caught by the guard**), `verify-glass-cell`, `verify-res-revenue`,
`verify-nonres-revenue`, `verify-services-public`. That is the cost of this
file's own one-pass rule, and it is the reason the rule exists.

⚠️ **S2 was applied to the PANEL only, and the first attempt was wrong.**
Renaming the *picker* to the same verb phrase made the panel print the sentence
twice — once as the layer head, once as the group head. The picker names the
**layer** (`Roads cost — lifecycle`); the group head says what the bar
**measures** (`To run and eventually rebuild`). Different jobs, different words.
Caught by rendering the panel, not by any guard.

⚠️ **Still open: C2** (anchor "per acre" in houses) and **S1** (`modelled` vs
`modeled` — now VISIBLE in the Services panel's reading line, which prints
`modeled road lifecycle cost`), plus **F4**. **A new row is owed for
`fmtSvcRatio`**, which prints a literal `0.0%` for 24 nonzero rows — it reads as
*free* rather than *small*, and the same defect was already fixed once in the
revenue panel (`<0.1%`, guarded by `verify-revenue-panel.js`).

---

## Group N — one quantity, four names

Municipal property tax appears under four different nouns depending on the surface.
A reader moving between the map and a panel has no way to know it is the same
number. **Decide the noun once (N1) and the rest follow.**

| id | surface | on screen now | proposal | status |
|---|---|---|---|---|
| **N1** | `#title`, Money view | `Edmonton: Tax Revenue per Acre` | `Edmonton: City Taxes per Acre` — "tax revenue" does not say *whose* tax, which is the whole reason education is excluded | **applied 2026-09-18** |
| **N2** | `#legend-label` | `Revenue per acre` | `City tax per acre` — "revenue" reads as business income to a general audience | **applied 2026-09-18** |
| **N3** | `renderRevenueMix` headline | `$1.89M municipal levy` | `$1.89M in city property tax`. ⚠️ This is a hood **total**, not per-acre — keep it distinct from N4 so the two panels don't look like one measure | **applied 2026-09-18** |
| **N4** | `renderServiceCost` headline | `$18,721 municipal levy / acre / yr` | `City property tax collected here` / `$18,721 per acre each year`. **The line Peter flagged as eye-glazing** (S157): an accounting noun plus a rate nobody holds intuitively | **applied 2026-09-18** |
| **N5** | `#loading-blurb` | `Municipal property-tax revenue per acre, by neighbourhood.` | `What each neighbourhood pays the City in property tax, per acre.` First thing anyone reads; currently the most jargon-dense sentence on the site | **applied 2026-09-18** |
| **N6** | `#revcut`, `#labcut`, `#ratio-denom` ×2 | `the full municipal levy the land generates` ×2 · `the levy-funded network…` · `levy-funded demand` | Follow N1–N5; `levy-funded` → `tax-funded`. Low-visibility, but it is where a confused reader goes — the worst place to repeat the confusing word | **applied 2026-09-18** |

---

## Group C — true, but stated where nobody reads it

Three facts are load-bearing for interpreting every number on the map. All three
are documented; none appear at the point of reading.

| id | fact | where it lives now | proposal | status |
|---|---|---|---|---|
| **C1** | Education tax is excluded | `#mill-note`, inside Data & Methods | Put it on the panel headline: *"City portion only — school taxes go to the province."* A resident comparing this to their own bill finds it ~24% short (2.4366 mills residential) with no way to know why | **applied 2026-09-18** |
| **C2** | Nothing anchors "per acre" | nowhere | `≈ 5.3 average houses' worth of city tax per acre`. Median hood $18,060/acre ÷ $3,431 (a $450k house at 7.6254 mills). **Computable per hood — do not hardcode** | open |
| **C3** | Roads are one service among many | `renderServiceCost` note | Say it in the headline, not the note. Without it, "Roads 5.1%" invites the reader to conclude the other 94.9% is surplus | **applied 2026-09-18** |

---

## Group J — jargon inherited from the source data

From the assessment roll and the City's own documents. Correct, and not English.
Each is a separate call — some are worth *teaching*, some worth replacing.

| id | term | on screen now | proposal | status |
|---|---|---|---|---|
| **J1** | mill rate | `…applying Edmonton's class-differential mill rates.` | Teach it once: *"different rates by property type — non-residential pays 3.2× the residential rate"*. The 3.2× (24.2229 vs 7.6254) is the interesting fact the jargon hides | open |
| **J2** | set-aside | `Set aside / insufficient road base` (legend) | `River valley, parks & undeveloped`. Project-internal term that reached the legend; 55 occurrences in the file | open |
| **J3** | assessment base | `0.08% of Edmonton's total assessment base` | `share of everything Edmonton taxes`. ⚠️ Live on the **public** site | open |
| **J4** | lifecycle / operating **basis** | `lifecycle basis — upkeep plus eventual rebuilding…` | Drop "basis": `To run and eventually rebuild` / `To run it this year`. The explanatory clauses are already good; only the head noun is accountancy | **applied 2026-09-18** |

---

## Group S — consistency, no judgement required

| id | issue | current | proposal | status |
|---|---|---|---|---|
| **S1** | `modelled` vs `modeled` | 17 each, dead even | Canadian `modelled` throughout — the project is otherwise strictly Canadian (`neighbourhood` 129 / `neighborhood` 0) | **applied 2026-09-18** — 17 occurrences on 16 lines (`grep -c` counts LINES; one tooltip carries it twice). All reader-facing; no element id moved (`about-modelled` was already Canadian). |
| **S2** | two labels, one layer | `Roads cost — lifecycle` (picker) vs `lifecycle basis → Roads` (panel) | One label, chosen with J4. Part of why the panel reads as unrelated to the map | **applied 2026-09-18** |
| **S3** | a nonzero cost printed as `0.0%` | `fmtSvcRatio` `toFixed(1)` below 10%, so **24 nonzero rows** rendered `0.0%` — 17 of them bikeway, the smallest a real cost four orders below the levy. **Reads as FREE, not as small.** | Floor at `<0.1%`, the fix `fmtMix` already carries one panel over. ⚠️ **`f > 0` is load-bearing** — 135 rows are EXACTLY zero and must keep saying `0.0%` | **applied 2026-09-18**, guarded by `verify-services-panel.js` §3c (3 checks, both mutations caught) |
| **S5** | a nonzero dollar amount printed as `$0` | S3's defect class, **swept for the first time 2026-09-19**. Seven dollar formatters rounded through `Math.round`, so **21 nonzero values** rendered `$0` — bikeway ops (6), roads ops (4), residential revenue (3), roads lifecycle (2), stormwater (1) and the lot-acre variants; smallest $0.0000008/acre. Same FREE-not-small misreading as S3, in dollars | Shared `money0` helper floors at `<$1` AT the rounding boundary. ⚠️ **`v > 0` is load-bearing** — a true zero must keep printing `$0` | **applied 2026-09-19**, guarded by `verify-smoke.js` §C9 (both directions, both mutations caught: 21 nonzero / 352 true zeros, distinguishable) + `verify-services-panel.js` §3d (non-vacuity) |
| **S6** | `fmtMix` called a true zero `<0.1%` | The inverse of S3, found by the same sweep. `fmtMix` lacked the `v > 0` guard `fmtSvcRatio` carries; correct only because `revenueMix` filters `> 0` before calling — **a formatter depending on its caller for correctness** | Add `v > 0 &&`, matching `fmtSvcRatio` | **applied 2026-09-19** |
| **S7** | the same defect in NON-dollar units | The 2026-09-19 sweep's remainder, measured over the served file: `fmtDev` **378** values across 9 metric×window combos (`0.00 new permits / acre` on a hood that HAS permits — reads as NO development), `fmtPct` **746** (temporal share 285 + commercial 441 + `revenue_share_city` 20), `fmtFar` **37** (`0.00 FAR`), and the three non-dollar service readouts `fmtFire` 10 / `fmtBike` 3 / `fmtTransit` 2 | **NOT a port of `<$1`**, and after measuring, **not one rule either** — the five surfaces are different cases (see the DATA note). Per unit: name the count where one exists, floor where the unit has no numerator to name, and leave `fmtFar` alone because `0.00 FAR` is *correct* | **DECIDED + applied 2026-09-20** (Peter, per-unit). `fmtDev` names its count in Infill; `fmtFire`/`fmtTransit`/`fmtPct` floor at `<0.01`; `fmtFar` and `fmtBike` closed as needing nothing. Guards: `verify-smoke.js` §C10 (3 checks) + `verify-infill.js` (2) + `verify-services-panel.js` §3e (non-vacuity) |
| **S8** | the same defect on TWO SURFACES THE S7 SWEEP NEVER LOOKED AT | S7 enumerated the formatters; these two are **open-coded at the use site**, so a sweep of `fmt*` could not see them. `road_m_per_acre` rendered `.toFixed(1)` at **four** separate call sites, and the residential revenue share was an inline `Math.round(100 * res / rev)` inside `viewTooltip`. Measured over the served file 2026-09-21: **19** hoods with residents paying tax rendered `0% of revenue is residential` (smallest SOUTH EDMONTON COMMON at 4.3e-07, largest that rounded away ELLERSLIE INDUSTRIAL at 0.40%), and **3** rendered `0.0 road m / acre` | Peter's rule, 2026-09-21: *"I don't want to hide activity from people, just say its super small."* Floors at `<1%` and `<0.1`, both keeping the `v > 0` guard. ⚠️ **The road three split into two different answers** — two were boundary-tangency crumbs and were deleted upstream (`MIN_PIECE_M`), one is a real 26.5 m stub and gets the floor. **Deleting a real road and floating a crumb are opposite errors and the surface cannot tell them apart**, which is why the fix is split across the two layers | **applied 2026-09-21**, guarded by `verify-smoke.js` §C10 (extended; its zero boundary is now a parameter, since these round to one decimal and to a whole percent) — falsified four ways, each count reproducing the pre-fix measurement |
| **S10** | `fmtResShare` said `100%` for mixed hoods | The top end of S8's fix, found by the S188 readout audit (`FINDINGS_readout_floors.md` §2): `Math.round` printed `100% of revenue is residential` for six hoods carrying 0.1–0.45% non-residential revenue (CRYSTALLINA NERA WEST … QUESNELL HEIGHTS); **0 hoods are exactly 100%**. S8's `0%` misreading mirrored: *nothing else is here* | `>99%` for `[0.995, 1)`; ⚠️ `frac < 1` is load-bearing, since a true all-residential hood must keep `100%` | **decided + applied 2026-09-23** (Peter: *">99%"*), guarded by `verify-smoke.js` §C10 (`res_share_top`) |
| **S9** | ⚠️ **`fmtFar` was re-proposed 2026-09-21 and REVERTED — it is DECIDED, not open** | S7 closed it as correct-not-floored on 2026-09-20 with the measurement behind it. A session working the S8 surfaces re-measured the same **37** values, did not read the row, and reported them to Peter as a new finding; he approved a floor against a framing that did not say it was already settled | **Leave `fmtFar` alone.** FAR is floor area over deduped LOT area, so a near-unbuilt hood genuinely has FAR ≈ 0 and `0.00` hides nobody — the unit is a density ratio, not a count of activity. That is what separates it from S8's share row | **closed 2026-09-20, re-closed 2026-09-21.** The use site and §C10 both carry the reason now, so the next re-proposal meets it before Peter does |

✅ **S7's data question is ANSWERED (2026-09-20), and it removed the bike
surface from this row rather than giving it a floor.** The question was whether
the smallest values — `bike_m_per_acre` = 3.8e-08 (38 **nanometres** of bike
route per acre), `cost_bike_ops_per_acre` = 7.8e-07 — were small numbers or
artefacts, because a display floor would render an artefact as `<0.01` and
dignify a value that belongs at zero.

**They were artefacts, and the instinct to fix it upstream was right.**
Measured over the live feed: 3.8e-08 is the **minimum** of the distribution,
not a typical value (median 7.07, max 42.2 — the metric itself is healthy).
Beacon Heights' entire bike network was **one overlay piece of 0.000011 m**, a
boundary-tangency crumb from `gpd.overlay`. ⚠️ **The map already drew no bike
line there** — the display path thins slivers at `WEB_MIN_PART_M`, the metric
path did not — so the tooltip and the map were telling a reader different
things. Fixed upstream by `MIN_PIECE_M = 1.0` in `src/load_bike.py`
(`DECISIONS.md` 2026-09-20; `test_sliver_piece_is_excluded_from_the_metric`).

**`fmtBike` drops from 3 values to 0** — the three sub-threshold values were
exactly the three sliver neighbourhoods, so bike needs no floor and no
`<0.01 m / acre` string. ⏳ Live from the next weekly refresh; the served file
still carries the three until then.

✅ **ALL FIVE ARE NOW MEASURED (2026-09-20), and BIKE WAS THE ONLY ARTEFACT.**
Every count above reproduced exactly against the served file (hash-matched to
`peterfriedrich.github.io` before measuring). The artefact-or-small question was
asked per surface, and the answers differ enough that **S7's original "decide
the rule once and apply to all four" framing did not survive** — a single
`<0.01` rule would have put a floor on FAR, where `0.00` is not a defect.

| surface | values | what is behind the `0.00` | verdict |
|---|---|---|---|
| `fmtBike` | 3 | an 11 µm overlay crumb | **ARTEFACT** — fixed upstream (`MIN_PIECE_M`), surface gone |
| `fmtDev` | 378 | **an INTEGER count ≥ 1 in every single row** (max 10 permits) | real; worst misread of the five |
| `fmtFire` | 10 | 0.31–15.4 dispatched events/yr | real, small |
| `fmtTransit` | 2 | 0.95 and 5.5 stop-events/weekday | real, small |
| `fmtFar` | 37 | 17.7–31,200 m² of floor area | real, and `0.00` is **correct** |
| `fmtPct` | 746 | 1 quantum of `share_scale` (1e-6) | at the **file's** precision floor |

⚠️ **`fmtDev`'s 378 are not uniformly harmful, and that narrowed the fix.** The
**Development** view already prints the raw count on the next line, so the rate
self-corrects there. Only the **Infill** view rendered `fmtDev` naked beside
`fmtFar`. So the fix is to **name the count** — the numerator is already in the
served file — and `fmtDev` needs no floor string and no new data.

⚠️ **`fmtFar` is CORRECT, not floored.** FAR = Σ floor area / Σ **deduped lot
area**, so the tiny values are huge, near-unbuilt polygons: ring-road corridors,
river-valley parkland, a 49 km² industrial park. The smallest implied floor area
is **17.7 m²** of real building. A hood that is essentially unbuilt genuinely
has FAR ≈ 0 and should say so. **A first pass divided by GROUND acres instead
and got 0.01 m² — physically impossible, and it looked exactly like the bike
story. The error ran toward the conclusion being reached for.** Check the
denominator before calling a ratio an artefact.

⚠️ **`fmtPct`'s floor belongs to the export, not the data.** `temporal.json`
stores shares as integers in units of 1/`share_scale` = 1e-6, so the smallest
nonzero value **is one quantum** — the file cannot resolve below `<0.01%`, which
is why the floor is the honest reading and a third decimal would be invented
precision. ❓ **UNRESOLVED:** 238 exact zeros in `share` (287 in `commercial`)
cannot be distinguished from values quantised down to zero. Greenfield hoods
with no assessment in 2012 are genuinely 0, so this is probably benign — but it
is not *shown* to be, and it cannot be settled from the served file.

⚠️ **`fmtBike` keeps NO floor, deliberately.** Post-`MIN_PIECE_M` the three
sliver hoods are exact zeros, so nothing renders `0.00`. A surviving 1 m route
in a very large hood *could* still land under 0.005 m/acre — today none does
(base rate 0), so no guard was added on the strength of a mechanism alone.
Re-measure if the bike tail reappears rather than pre-emptively flooring it.

---

## Group F — framing that changes the conclusion

Wording downstream of a layout or logic decision. These alter what a reader
*concludes*, not just how comfortably they read.

### F1 — the Services panel ignored the service picker — ✅ **APPLIED 2026-09-15** (PR #399)

`renderServiceCost` rendered the same block for all ten layers: select Fire, Water,
Transit or Bike, click a hood, and the panel reported **road costs**.

**Built as: the panel follows `state.svcDriver`** — the colour-driving service, not
the checkbox set, because Services is ten checkboxes plus a driver radio and "the
picker" was ambiguous (Peter, 2026-09-15). It shows the driver's value and rank,
then the cost bars for that service family. ⚠️ **3 layers have no cost twin, not
the 4 first recorded** — storm, fire, water; transit-supply pairs with
`transitcost`. Those three state the scope in their own terms instead of rendering
an empty group. Gated by `tools/profiling/verify-services-panel.js`, merged RED
first (#398). Full reasoning and the two corrections: `DECISIONS.md` 2026-09-15.

### F2 — the gold over-100% bar — ⚠️ **LOCKED AGAINST, do not re-derive**

`.svcrow em.over` saturates the bar at 100% and turns it gold when a modelled cost
exceeds the hood's levy.

⚠️ **`DECISIONS.md` 2026-07-16** (back-filled 2026-09-07): cost-vs-revenue is framed
as **MAGNITUDE, not break-even** — the same log ramp as roads/fire, **no 1.0
marking, never "pays its way"**. The gold threshold reintroduces exactly that
verdict at a different location.

The reasoning still holds, and the current data strengthens it: the numerator is the
**whole** municipal levy and the denominator is **one** service, so revenue ÷
lifecycle road cost has **median 10.9×** and only **2.2%** of hoods fall below 1.0×
(400 hoods). Proposal: drop the gold state, keep magnitude framing.

### F3 — the Ratio panel shows assessment history

`syncPinnedPanel` falls through to `temporalFor`, so the Ratio lens's pinned panel
reads `2026: 0.08% of Edmonton's total assessment base · $192M assessed`. The lens
that **is** about revenue-versus-service is the one lens whose panel says nothing
about it.

Proposal: show the ratio's own components — revenue, road base, and the citywide
median for comparison.

⚠️ **A road-cost *denominator* is NOT the fix.** Both cost columns are exact
constant multiples of road metres — **$50.000000/m** and **$9.320000/m**, stdev
< 0.0001 across 400 hoods — so `revenue ÷ road cost` is `revenue ÷ road metre ÷ 50`.
It would duplicate the existing (and public-default) road-metre map at different
units. A `Per service $` denominator also already existed and was **retired
2026-09-05** with its composite column.

### F4 — the Development history panel's summary line ignores the window picker

`#devwindow` (3 yr / 5 yr / Since 2009) reaches every readout except the pinned
panel (`docs/FINDINGS_controls_state_space.md` T2). **The wiring is right by
decision**: `DECISIONS.md` 2026-09-14 makes the panel the *whole* per-year series
(2009–2025, one column per year), and the three windows are aggregates over it —
so the chart deliberately does not re-scope. `devHistoryFor` reads the metric key
and nothing else.

What is left is one line of copy. `renderDevHistory` writes
`peak N in YYYY · N in the last 5 years · active in N of 17 years` under every
window — under **3 yr** the map is 2023–2025 and the panel volunteers a five-year
figure; under **Since 2009** the "last 5 years" is a second window the reader did
not pick. Options: (a) make that clause follow the picker (`N in 2023–2025`), (b)
drop it — the chart already shows the recent bars, (c) leave it, since the panel
names its own range in the headline. ⚠️ **Not a wiring fix** — re-scoping the
chart to the window would silently redefine the published number.

---

## Group B — the public title blurbs (inventory, 2026-09-23 S193)

The `#title-p` sentence under each view's title, **public build only** (TODO
"Public blurb cleanup"). **This is the inventory; no blurb has been reworded.**
Measured 2026-09-23 with a click-through script, since replaced by
`tools/profiling/verify-blurbs.js`. Its `--dump out.json` writes every public
state's text, length and rendered height in about 30 seconds. Re-run it after a
rewrite to re-measure.

**66 states, 11 base texts.** Most variation is appended clauses, not separate
blurbs: the colour clause (`withColourClause`), the azure-cells sentence
(Glass, Ratio), the Services "renders neutral" clause, and the Development
window phrase + grid addendum. The two road-cost states include the clause
*"The roads layer renders neutral…"*, because Roads stays checked by default.

| base text (source) | public states | chars | panel px |
|---|---|---|---|
| Money, Total/Res/Non-res/Value, ground (`METRICS[*].blurb`) | 4 × colour | 291–412 | 176–236 |
| Money, same four, lot (`METRICS[*].lotBlurb`) | 4 × colour | 421–452 | 214–254 |
| Money grid, ground (`GLASS_BLURBS.ground`) | 2 cell sizes × 4 metrics × colour | 357–514 | 198–273 |
| Money grid, lot (`GLASS_BLURBS.lot`) | same | 424–581 | 236–311 |
| Change over time (`changeBlurb`) | 2 windows | 880 | 423 |
| Development, neighbourhood (`devChoroplethBlurb`) | 2 metrics × 3 windows | 584–627 | 311 |
| Development, 100 m grid (`devBlurb`) | same | 906–951 | 442 |
| Services: Roads (`SERVICES.roads.blurb`) | 1 | 307 | 157 |
| Services: Roads cost (`SERVICES.roadscost.blurb`) | 1 | **1,087** | **495** |
| Services: Roads cost — lifecycle (`SERVICES.roadslife.blurb`) | 1 | **1,085** | **495** |
| Ratio (`RATIO_DENOMS.roads.blurb` + `ratioInstBlurb`) | 1 | 561 | 292 |

⚠️ **The two road-cost blurbs are the longest on the public site.** The TODO
assumed Development was the longest. The Services picker is a public control, so
these count.

### Defects found by the inventory — no judgement needed

| id | defect | status |
|---|---|---|
| **B1** | **The Development blurb says "dwelling units" in Permits mode.** The neighbourhood blurb is byte-identical for Dwelling units and Permits in all three windows. The grid addendum switches to "new permits per cell" but its coverage clause still says "~N% of the window's **units**". ⚠️ **The figure was also computed from units**: on the long window it showed ~16% missing where permits are ~8%. | **applied 2026-09-24**, guarded by `verify-development.js` (2 checks, both fail on the pre-fix file) |
| **B2** | **S1 missed capital `Modeled`.** It survives in the public Roads-cost-lifecycle blurb (*"Modeled, and in several ways"*) and in two public checkbox tooltips (Roads cost, Roads cost — lifecycle), plus full-only strings (water, storm, transit cost, two panel labels). S1's count was case-sensitive. | **applied 2026-09-24**: 12 strings; the one left is an all-caps code comment |

### Decisions the cleanup needs, per blurb

| id | question | where it bites | status |
|---|---|---|---|
| **B3** | **Height wording in 2D.** Since #552 the map is flat in top-down, so every height claim is false there. Options: (a) say it conditionally (the blurb follows the camera, like `withColourClause` follows the toggle), (b) move height into the legend, or (c) drop it. | Money ×8 (*"Height and colour show…", "Height is linear"*), grid ×2, Change (*"Teal rises… orange sinks below the plane"*, *"⚠️ Height is a RATE"*), Development grid (*"height is linear in new homes"*), Ratio (*"Ghost prisms… Height is linear"*). Services has none. || **decided 2026-09-24** (Peter): (a) for Money and Change, where height is the main encoding, so the sentence follows the camera the way `withColourClause` follows the toggle; (c) for the *"Height is linear"* asides, which are dropped |
| **B4** | **The noun.** N1–N5 set `city tax`. The title says *"City Taxes per Acre"* and every revenue blurb under it says *"municipal property-tax revenue"*, as does Ratio. The N-group was applied to the title and legend, not to `#title-p`. Follow N1; this is not reopening it. | Money Total/Res/Non-res ×2 denominators, Ratio | open |
| **B5** | **A length budget.** There isn't one. On a 768 px screen the panel runs from 157 px (Roads) to 495 px (road costs). A target (for example ≤ 400 chars, with the rest moved to the tooltip or Data & Methods) would decide most of the rewrite. | road costs, Change, Development grid | **decided 2026-09-24** (Peter): **≤ 400 characters** per blurb state; the caveats that don't fit move to the tooltip or Data & Methods. The worst case a visitor meets by default is Development (949 characters on entry) |
| **B6** | **The grid blurbs never name the metric**: *"The active metric in 100 m grid cells…"*. The title does, so this is a placeholder that shipped. | Money grid, 16 states | **applied in BG1** (in PR) |
| **B7** | **Register.** Change uses `⚠️` and ALL-CAPS (*RATE*, *NOT*). The Development long window reads *"(2009–2025) — the density added over the era — new houses…"*, two dash clauses in a row. | Change, Development | **decided 2026-09-24**: drop both; applied to Development (BD1) and Change (BC1) |
| **B8** | **A writing rule for every blurb** (Peter, 2026-09-24): *"paragraph breaks first… and bold for the very first important term/target in the lens"*. **P1** says what the lens shows, with the measured thing bolded where it first appears, and that is the only bold. **P2** says how to read it: colour, height, grey. **P3** holds caveats and mode-specific additions, and is left out when there is nothing to say. B5's 400 characters count across all paragraphs. Markup: a blank line starts a paragraph and `**x**` bolds x. `setBlurb()` builds the nodes without innerHTML. | **decided 2026-09-24**; renderer shipped. Guarded by `verify-blurbs.js` (1–3 paragraphs, exactly one bold term in P1, ≤ 400 characters, and no height claim in 2D) over every public state. A lens not yet rewritten prints as `OPEN`, not as a failure |


### Draft rewrites (B8 format, ≤ 400 characters)

**BD1 — Development** (status: **applied 2026-09-24**, Peter's edits: grid P2 reads *"counts new homes permitted there"*, or *"new permits issued there"* in Permits mode; guarded by `verify-blurbs.js`). Twelve states: 2 metrics × 3 windows × neighbourhood/grid. `{w}` is the window's year range; `{n}` is `homes` or `permits`; `{pct}` is read from `dev_grid.json` coverage for the active metric, and P3 is omitted when it is 0. The longest state is 388 characters; the default (units, since 2009, grid) is 380, down from 949.

| part | text |
|---|---|
| P1, units | `**New homes per acre**, {w}: dwelling units in issued building permits — houses, semis, row houses and apartments. Where the city is growing, not what it pays.` |
| P1, permits | `**New residential permits per acre**, {w}: one permit per building, so a house and an apartment block each count once. Where the city is growing, not what it pays.` |
| P2, neighbourhood | `Brighter neighbourhoods added more. Colour is square-root scaled, so a few dense-infill areas don't wash out the rest.` |
| P2, grid | `Each 100 m cell counts new homes permitted there` (Permits: `new permits issued there`) `— brighter is more. Colour is square-root scaled.` |
| P3, neighbourhood | `Undeveloped greenfield land is coloured here, not greyed: it is where much new building lands.` |
| P3, grid | `~{pct}% of the {n} aren't on the grid yet (the newest permits lag geocoding); they still count in the neighbourhood view.` |

**Dropped, and where each piece still lives:**
- *"counted where construction was permitted"*: it is implied by "issued building permits".
- *"a neighbourhood's set-aside status still shows on hover"*: the hover still shows it.
- *"the density added over the era"*: the long-window aside (B7).
- *"height is linear in new homes per cell"*: B3 (c).
- *"Unlike the other lenses"*: the Development button's tooltip already says greenfield land is shown in full colour.

**BC1 — Change over time** (status: **in PR, awaiting Peter's merge**). Four states: 2 windows × camera. `{w}` is the window's years and `{y0}` its first year. 393 characters in 3D and 394 in 2D, down from 880. It also applies B3 (a) and B7 (no `⚠️`, no ALL-CAPS).

| part | text |
|---|---|
| P1 | `How fast each neighbourhood's **share of Edmonton's assessed value** changed, {w}, against its own starting share.` |
| P2, 3D | `Teal rises where it gained, orange sinks where it lost. It is a rate, not dollars: the tallest are small new subdivisions. Grey = no {y0} value to start from.` |
| P2, 2D | `Teal gained share, orange lost it; stronger is faster. It is a rate, not dollars: the strongest are small new subdivisions. Grey = no {y0} value to start from.` |
| P3 | `A neighbourhood can lose share while its value rises, if the rest of the city rose faster. Click one for its history.` |

**Dropped:**
- *"so a small hood doubling reads as strongly as a large one doubling"*: the P2 "tallest are small new subdivisions" sentence carries the consequence.
- *"Colour saturates at each arm's 95th percentile"*: the legend's job.
- *"these are the new-growth areas, NOT set-aside land"*: the legend swatch and the hover already say "No {y0} baseline", and `verify-change.js` guards that neither says set-aside.
- *"assessment base"* → *"assessed value"*: J3's direction, applied to this blurb only.

The camera flip re-renders the blurb through `currentBlurb()` (from `syncMode`), before `buildLayers`, because the label sweep measures the title block.

**BM1 — Money, neighbourhood prisms** (status: **in PR, awaiting Peter's merge**). 32 states: 4 metrics × 2 denominators × colour toggle × camera. P1 is the metric's own (`METRICS[*].blurb` / `.lotBlurb`). P2 is built by `moneyBlurb()`, following the camera (B3) and the colour toggle (`withColourClause`). P3 is `blurbNote`, on the two split cuts only. The landing state goes from 348 to about 230 characters, and the longest state is under 375.

| part | text |
|---|---|
| P1, Total | `**City property tax per acre**: what each neighbourhood's properties pay the City, divided by its land area.` (lot: `…per lot acre**: … divided by the parcel land they own, so parks, river valley and big lots don't dilute it.`) |
| P1, Residential | `**Residential city tax per acre**: what houses, condos and apartment buildings pay the City, divided by the neighbourhood's land area.` |
| P1, Non-residential | `**Non-residential city tax per acre**: what commercial and industrial property pays the City, divided by the neighbourhood's land area.` |
| P1, Value | `**Assessed value per acre**: the total assessed value of each neighbourhood's property, divided by its land area. What the land is worth, not what it pays.` |
| P2 | `Taller, brighter` (2D: `Brighter`) `neighbourhoods are higher per acre; colour is square-root scaled to show the low end. Grey = set-aside land (river valley, parks, undeveloped), off the scale.` (lot: `Grey = set-aside land, or too little parcel land to measure.`) |
| P3, split cuts | `A subset of Revenue, not all of what the land pays.` (the honesty line `verify-res-revenue` / `verify-nonres-revenue` guard) |

**Dropped:**
- *"applying Edmonton's class-differential mill rates"* (J1): the mill-rate pod directly below the blurb prints the rates under every revenue cut.
- *"School tax is not included"* was drafted in, then cut: the same pod says *"City tax only; education excluded"* (C1).
- *"commercial and industrial dollars are excluded here"* / *"residential dollars are excluded"*: P1 already names the class.
- *"(city lot sizes, deduplicated at multi-unit points)"*: methodology. ⚠️ It now appears on no public surface; say if it belongs in Data & Methods.
- *"Height is linear"*: B3 (c).

**BG1 — Money, grid detail (100 m / 50 m)** (status: **in PR, awaiting Peter's merge**). 64 states: 2 cell sizes × 4 metrics × 2 denominators × colour × camera. It names the metric (B6) from `METRICS[*].legendLabel`. The longest state (Non-residential, lot acres, linear colour, 3D, azure cells showing) is 391 characters, down from 581.

| part | text |
|---|---|
| P1, ground | `**{legend label} in {cell} m grid cells**: property points binned to squares.` |
| P1, lot | `**{legend label, per lot acre} in {cell} m grid cells**, over the parcel acres each cell's properties own.` |
| P2 | `Taller, brighter spikes` (2D: `Brighter cells`) `are higher; colour is square-root scaled to show the low end. Hover the plane for neighbourhood numbers. Grey = set-aside land.` |
| P3, revenue cuts with azure cells | `{n} azure cells are mostly institutional land, where the roll doesn't say if tax is levied: only the solid part is certain.` |

**Dropped:**
- *"each cell's total divided by its ground acres"*: "per acre" in the bold term says it.
- *"(city lot sizes, deduplicated at multi-unit points; cells with no usable lot size are omitted)"*: methodology, the same open question as in BM1.
- *"The spikes are translucent so it reads through"*: the reader can see that.
- *"Height is linear"*: B3 (c).

Already open elsewhere and on the public default blurb: **J1** (*"class-differential
mill rates"*) and **J2** (*"set-aside"*, in every public blurb except Services: Roads).

---

## Related

- `docs/DECISIONS.md` — where a decided row goes once it locks (cite the id)
- `docs/CONTROLS_MATRIX.md` — the control/view state space these surfaces sit in
- `docs/UI.md` — the build log
- `scripts/check_cost_copy.py` — already guards the cost-rate figures in copy
