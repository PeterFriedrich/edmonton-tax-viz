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
| **S7** | the same defect in NON-dollar units — **OPEN, one decision, four surfaces** | The 2026-09-19 sweep's remainder, measured over the served file: `fmtDev` **378** values across 9 metric×window combos (`0.00 new permits / acre` on a hood that HAS permits — reads as NO development), `fmtPct` **746** (temporal share 285 + commercial 441 + `revenue_share_city` 20), `fmtFar` **37** (`0.00 FAR`), and the three non-dollar service readouts `fmtFire` 10 / `fmtBike` 3 / `fmtTransit` 2 | **NOT a port of `<$1`** — each unit needs its own floor and its own string (`<0.01 permits / acre`? `<0.01 FAR`? and is `0.00 FAR` on a near-unbuilt hood actually *correct*?). ⚠️ **Decide the rule once and apply to all four**, which is what this file exists to enforce | **OPEN — Peter's call.** ⚠️ See the DATA note below: some of these inputs may be artefacts, not small numbers, and a floor would dignify them |

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

⚠️ **The other non-dollar surfaces are UNMEASURED and this result does not
transfer.** `fmtDev` 378, `fmtPct` 746, `fmtFar` 37, `fmtFire` 10,
`fmtTransit` 2 — fire and transit come from different pipelines that use the
same overlay pattern and may tell the same story, but nobody has checked.
**Ask the artefact-or-small question per surface before choosing any floor.**

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

## Related

- `docs/DECISIONS.md` — where a decided row goes once it locks (cite the id)
- `docs/CONTROLS_MATRIX.md` — the control/view state space these surfaces sit in
- `docs/UI.md` — the build log
- `scripts/check_cost_copy.py` — already guards the cost-rate figures in copy
