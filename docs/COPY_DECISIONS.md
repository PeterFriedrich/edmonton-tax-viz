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

---

## Group N — one quantity, four names

Municipal property tax appears under four different nouns depending on the surface.
A reader moving between the map and a panel has no way to know it is the same
number. **Decide the noun once (N1) and the rest follow.**

| id | surface | on screen now | proposal | status |
|---|---|---|---|---|
| **N1** | `#title`, Money view | `Edmonton: Tax Revenue per Acre` | `Edmonton: City Taxes per Acre` — "tax revenue" does not say *whose* tax, which is the whole reason education is excluded | open |
| **N2** | `#legend-label` | `Revenue per acre` | `City tax per acre` — "revenue" reads as business income to a general audience | open |
| **N3** | `renderRevenueMix` headline | `$1.89M municipal levy` | `$1.89M in city property tax`. ⚠️ This is a hood **total**, not per-acre — keep it distinct from N4 so the two panels don't look like one measure | open |
| **N4** | `renderServiceCost` headline | `$18,721 municipal levy / acre / yr` | `City property tax collected here` / `$18,721 per acre each year`. **The line Peter flagged as eye-glazing** (S157): an accounting noun plus a rate nobody holds intuitively | open |
| **N5** | `#loading-blurb` | `Municipal property-tax revenue per acre, by neighbourhood.` | `What each neighbourhood pays the City in property tax, per acre.` First thing anyone reads; currently the most jargon-dense sentence on the site | open |
| **N6** | `#revcut`, `#labcut`, `#ratio-denom` ×2 | `the full municipal levy the land generates` ×2 · `the levy-funded network…` · `levy-funded demand` | Follow N1–N5; `levy-funded` → `tax-funded`. Low-visibility, but it is where a confused reader goes — the worst place to repeat the confusing word | open |

---

## Group C — true, but stated where nobody reads it

Three facts are load-bearing for interpreting every number on the map. All three
are documented; none appear at the point of reading.

| id | fact | where it lives now | proposal | status |
|---|---|---|---|---|
| **C1** | Education tax is excluded | `#mill-note`, inside Data & Methods | Put it on the panel headline: *"City portion only — school taxes go to the province."* A resident comparing this to their own bill finds it ~24% short (2.4366 mills residential) with no way to know why | open |
| **C2** | Nothing anchors "per acre" | nowhere | `≈ 5.3 average houses' worth of city tax per acre`. Median hood $18,060/acre ÷ $3,431 (a $450k house at 7.6254 mills). **Computable per hood — do not hardcode** | open |
| **C3** | Roads are one service among many | `renderServiceCost` note | Say it in the headline, not the note. Without it, "Roads 5.1%" invites the reader to conclude the other 94.9% is surplus | open |

---

## Group J — jargon inherited from the source data

From the assessment roll and the City's own documents. Correct, and not English.
Each is a separate call — some are worth *teaching*, some worth replacing.

| id | term | on screen now | proposal | status |
|---|---|---|---|---|
| **J1** | mill rate | `…applying Edmonton's class-differential mill rates.` | Teach it once: *"different rates by property type — non-residential pays 3.2× the residential rate"*. The 3.2× (24.2229 vs 7.6254) is the interesting fact the jargon hides | open |
| **J2** | set-aside | `Set aside / insufficient road base` (legend) | `River valley, parks & undeveloped`. Project-internal term that reached the legend; 55 occurrences in the file | open |
| **J3** | assessment base | `0.08% of Edmonton's total assessment base` | `share of everything Edmonton taxes`. ⚠️ Live on the **public** site | open |
| **J4** | lifecycle / operating **basis** | `lifecycle basis — upkeep plus eventual rebuilding…` | Drop "basis": `To run and eventually rebuild` / `To run it this year`. The explanatory clauses are already good; only the head noun is accountancy | open |

---

## Group S — consistency, no judgement required

| id | issue | current | proposal | status |
|---|---|---|---|---|
| **S1** | `modelled` vs `modeled` | 17 each, dead even | Canadian `modelled` throughout — the project is otherwise strictly Canadian (`neighbourhood` 129 / `neighborhood` 0) | open |
| **S2** | two labels, one layer | `Roads cost — lifecycle` (picker) vs `lifecycle basis → Roads` (panel) | One label, chosen with J4. Part of why the panel reads as unrelated to the map | open |

---

## Group F — framing that changes the conclusion

Wording downstream of a layout or logic decision. These alter what a reader
*concludes*, not just how comfortably they read.

### F1 — the Services panel ignores the service picker — **direction chosen, not built**

`renderServiceCost` renders the same block for all ten layers. Select Fire, Water,
Transit or Bike, click a hood, and the panel reports **road costs**. Verified by
driving all ten layers and diffing the rendered panel: byte-identical every time.

**Chosen (Peter, S157): "selected layer + its cost twin"** — the panel follows the
picker and shows the selected layer's value, its rank, and its cost twin where one
exists. ⚠️ 4 of 10 layers (storm, fire, water, transit-supply) have **no** cost
twin, so the panel shape must degrade cleanly rather than render an empty group.

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
