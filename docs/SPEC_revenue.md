# Scope: True Revenue Per Acre (next phase)

**Status: BUILT 2026-06-28.** The pipeline now computes per-property municipal
levy (`src/apply_tax_rates.py`) and emits `revenue_per_acre` alongside
`value_per_acre` in the served GeoJSON. Total 2025 municipal levy ≈ $2.67 B;
class reweighting confirmed (Residential 68.5% of value / 46.2% of levy;
Non Residential 21.7% / 46.4%). Web map value↔revenue toggle: DONE (commit
`a0cf2a0`). This doc captures the methodology that turned the *assessed-value*-per-acre
metric into a *tax-revenue*-per-acre metric.

**Update 2026-06-29:** the colour-scale work exposed that the "flag exempt-heavy
neighbourhoods" plan was built on a false premise (exempt land is absent from the
roll, not low). Superseded by a land-use set-aside via the zoning layer — see the
dated section below and `docs/FINDINGS_revenue_scale.md`.

## Why

The project is titled "Revenue Per Acre" but currently computes
`value_per_acre = total_assessed_value / area_acres` — **assessed value, not
revenue**. No mill rate is applied (see `join_and_calculate.py`). Assessed value
is a *proxy* for revenue and a biased one: Edmonton's non-residential mill rate
is higher than residential, so value-per-acre understates the revenue pull of
commercial/industrial land relative to housing. True revenue/acre applies the
per-class tax rate.

## Methodology check — RESOLVED 2026-06-28

Confirmed how comparable projects define the metric (web research, sources below):

- **Strong Towns** (canonical how-to): primary metric is **assessed value per
  acre**, explicitly does *not* apply mill rates; tax liability is offered only
  as a secondary analysis.
- **Urban3 / Joe Minicozzi** (originators of the 3D value-per-acre map — our
  closest analog): **taxable assessed value per acre**.
- Some derivative practitioners apply the rate → revenue/acre
  (`(assessed value × tax rate) / acres`), but this is the minority/stricter form.

**So the current metric (assessed value/acre) IS the common convention — it
matches Urban3 directly. A rename alone would be legitimate.**

**The deciding insight:** applying a *uniform* city-wide rate is just scaling
every parcel by the same constant → an identical-looking map, only the legend
units change. The map only changes shape if **rates differ by class**. Edmonton's
do, substantially (see external data below: non-res ≈ 2–3× residential). So the
real payoff of the revenue phase is capturing the **class differential**, which
re-ranks neighbourhoods (commercial/industrial rises relative to residential) —
a genuinely new signal, not a unit change.

**Decision: build the real computation, keep BOTH metrics as a toggle.** Keep
assessed value/acre (the Urban3 convention, comparable to every other VPA map)
*and* add revenue/acre using class-differential municipal mill rates. The gap
between the two maps reflects the effect of Edmonton's class-differential mill
rates. This also resolves the exempt question (below): Urban3/Strong Towns
use *taxable* value, so exempt parcels shouldn't inflate either metric — exclude/
separate under value, $0 under revenue (the two treatments converge).

Sources:
- Strong Towns, "Value Per Acre Analysis: A How-To For Beginners" —
  https://www.strongtowns.org/journal/2018-10-19-value-per-acre-analysis-a-how-to-for-beginners
- Urban3 methodology (taxable value per acre, 3D) — https://www.urbanthree.com/
- Urban Prosperity Network, value-per-acre how-to (the apply-the-rate variant) —
  https://urbanprosperity.net/how-to-calculate-and-visualize-value-per-acre-in-your-city

## Data we already have

The raw assessment CSV (`Property_Assessment_Data__Current_Calendar_Year_.csv`)
**already carries the class fields** — they're currently dropped in
`load_assessment.py` (values per `DATA.md`):

- `Tax Class` — clean 4-value field: **Residential, Non Residential, Other
  Residential, Farmland**. This maps directly to the City's published mill-rate
  classes — **use it as the rate join key** (cleaner than `Assessment Class 1`,
  which has messier values like COMMERCIAL / MA DERELICT RESIDENTIAL).
- `Assessment Class 1/2/3` + `Assessment Class % 1/2/3` — per-class apportionment
  for split-class parcels.

So split-class parcels can be handled correctly from existing data. Note the
exempt proxy already in use: `Assessment Class 1 == 'NONRES MUNICIPAL/RES
EDUCATION'` (3 rows, flagged `is_exempt` on load) — see exempt decision below.

## Data we still need (external)

- **Edmonton municipal mill rates by tax class, assessment year 2025 — FETCHED
  2026-06-28, stored in `data/mill_rates.json`.** Source: Edmonton Open Data
  dataset `pwis-wc4c` ("Property and Education Tax Rates (2014 onward)"). 2025
  municipal rates per $1,000: Residential **7.6254**, Other Residential
  **8.3116**, Non Residential **24.2229**, Farmland **7.6254** (assumed =
  Residential; no 2025 Farmland row — see DATA.md). Non-res ≈ 3.2× residential,
  confirming the class differential.
  - The earlier search figures were wrong and are now superseded: 0.0076648 was
    the **2024** residential rate; the "21 mills" non-res was stale (true 2025
    municipal non-res is 24.2229). Provenance + the education rates (unused) are
    in `data/mill_rates.json`; full source detail in `DATA.md` §4.
- **DECIDED: municipal mill rate only** (not municipal + education/provincial).
  Reason: this project models *City* fiscal sustainability, not total tax burden
  on residents. The education levy is set provincially and flows to schools, not
  city infrastructure, so including it would muddy what we are measuring.

## Computation

Per property, summing over its (up to 3) classes:

```
levy = Σ_class  assessed_value × (class_% / 100) × (mill_rate[class] / 1000)
```

Then aggregate `levy` by neighbourhood → `total_revenue`, and
`revenue_per_acre = total_revenue / area_acres`.

## Code changes

- **`load_assessment.py`** — stop dropping `Assessment Class N` + `% N` (and/or
  `Tax Class`); carry them through.
- **New module `src/apply_tax_rates.py`** (independently runnable, per project
  rule) — map class → mill rate, compute per-property `levy`, handling
  split-class apportionment. Mill rates from a small config/data file keyed by
  year + class (with source + year recorded), not hardcoded.
- **`aggregate_by_neighbourhood.py`** — sum `levy` → `total_revenue` (keep
  `total_assessed_value` too if we want both layers).
- **`join_and_calculate.py`** — add `revenue_per_acre`; decide whether it
  replaces `value_per_acre` or sits alongside it (a toggle in the web map could
  show value vs revenue).
- **Tests** for the new module: rate mapping, split-class apportionment, and the
  exempt → $0 case below.
- **Rename** docs/titles once revenue is real (or drop the rename if we decide
  assessed value is the chosen metric — see "Verify first").

## Methodology decisions to settle

- **Municipal-only vs total tax — DECIDED: municipal-only** (reason under "Data
  we still need").
- **Tax-exempt properties — treatment under revenue (most consequential
  decision).** Currently flagged + included (correct for an *assessed value*
  analysis). Under a *revenue* framing they generate **$0**. Key constraint: our
  denominator is the **neighbourhood boundary polygon area** (from
  `load_boundaries`), NOT a sum of taxable parcel areas — so "exclude exempt land
  from the denominator" (the Urban3 parcel-level move) is **not available**
  without parcel-area data we don't have (the AltaLIS gap). So the practical +
  honest choice is **$0 in the numerator, full boundary area in the
  denominator**: exempt-heavy neighbourhoods (downtown government parcels, the
  Legislature) will legitimately read **LOW** on revenue/acre. That is a true
  city-fiscal fact but visually surprising, so **flag those neighbourhoods**
  (we already detect `is_exempt`) rather than let them silently read as
  unproductive. **SUPERSEDED 2026-06-29 (see Update below):** `is_exempt` catches
  only 3 parcels — exempt institutional land is *absent from the taxable roll
  entirely*, so it cannot be flagged this way, and the near-zero neighbourhoods are
  **low-coverage natural/undeveloped land** (river valley, ravines, ring-road
  margins), not exempt. Separation is now by the zoning land-use layer.
- **Year alignment — RESOLVED: 2025.** The assessment dataset (Socrata
  `q7d6-ambg`) is a live weekly feed; its coverage year lives in the dataset
  *metadata* ("effective 2025-01-01 to 2025-12-31"), not in the rows. Our local
  snapshot (downloaded 2026-05-16) is 2025 data. Mill rates MUST be the **2025**
  bylaw. A future re-download could roll to a new year — re-check the metadata.
  See `DATA.md`.
- **Keep both metrics — DECIDED: yes.** Show assessed-value/acre and
  revenue/acre side by side (web toggle); the gap between them reflects the
  class-differential mill rates. Keeping both is also more transparent than
  picking one and hiding the other (supports the neutral-tone goal).

## Update 2026-06-29: colour scale + land-use set-aside

Full empirical detail in `docs/FINDINGS_revenue_scale.md`; decisions summarized here.

**Problem.** The web map's colour clamp ($50k revenue / $4M value, ~p97) saturates
the top ~2.5% to one peak colour — a hard plateau that reads as a meaningful
threshold but is only a display device. Driven by severe right skew (revenue spans
5.2 orders of magnitude; median would sit at 7% of a linear-to-max ramp).

**The distribution is a two-population mixture** — a roughly log-normal taxable core
plus a near-zero spike of ~57 neighbourhoods. The spike is **NOT exempt land**
(that proxy is near-empty; exempt institutions are absent from the roll). It is
**low-coverage natural/undeveloped land**, confirmed by zoning composition.

**Separator — DECIDED: the Zoning Bylaw layer (`fixa-tstc`).** Spatially overlay
zoning polygons on neighbourhood boundaries → land-use composition % per
neighbourhood (`src/load_zoning.py`, see ARCHITECTURE.md + DATA.md §5). Set aside a
neighbourhood when its **never + not-yet** share ≥ **0.90**:
- **never** = River Valley / Natural Areas / Parks (permanent non-taxable land);
- **not-yet** = Future Development + agricultural/rural fringe + industrial reserve.
- Mixed cases (50–90%) and all developed land **stay on the scale** (zoning = what's
  *allowed*, not *built*; underdeveloped-but-developed land is the fiscal story).

**Why not-yet is included and still scales:** set-aside keys off *zoning*, not
revenue. As fringe land develops the city rezones it, so it drops below 0.90 and
**auto-rejoins the scale** next refresh — self-maintaining, no threshold to re-tune.
This requires **zoning to be a refreshed pipeline input** (year-aligned, vintage
recorded — see SPEC_deployment.md).

**Visual — DECIDED:** set-aside neighbourhoods render in a **neutral grey**
(distinct from the ramp, not red/low) and are **excluded from the colour-scale fit**.
The full zoning-polygon overlay layer is a SEPARATE later product decision (not coupled).

**Colour transform — DEFERRED to after the set-aside lands.** Re-run the skew test
on the set-aside-excluded taxable set: if ≈ log-normal (likely), use **log** for
colour; **sqrt** is the fallback. **Height stays LINEAR** (the standing honesty
choice) regardless.

**Permanent caveat — ⚠️ CORRECTED 2026-08-15, this used to point the wrong way.**
It read *"revenue/acre understates any neighbourhood holding large exempt
institutions (absent from the roll)"*. Measured, the premise is false: the U of A
campus and the hospitals **are** on the roll (2,254 parcels on `AJ`/`UF`/`UI`/`PU`,
$5.62B assessed) and this pipeline levies all of them, so if the City in fact
exempts some we **overstate** those hoods. The roll publishes assessments and a
Tax Class, not exemption status, so **the direction is unknown**
(`FINDINGS_revenue_scale.md` §4–5, `DECISIONS.md` 2026-08-08). Zoning
(`UI`/`UF`/`AJ`/`PU`) still lets us flag *where*, though zoning ≠ tax status.

## The institutional caveat on the Money tooltip (2026-08-15)

The Lab's deviation lens bands a ≥25%-institutional hood into a range and draws
no prism. The default Money view kept a solid, confident prism — so the same
neighbourhood said two different things depending on which lens you were in, and
the confident version was the public one.

**Measured on `revenue_per_acre`:** 15 of 358 live hoods cross `INST_UNCERTAIN_MIN`
— the *same 15* the Lab bands. Four sit in the top 11:

| rank | hood | levied | if exempt | rank then |
|---:|---|---:|---:|---:|
| 2 | University of Alberta | $171,670 | $17,522 | **206** |
| 6 | Spruce Avenue | $72,898 | $42,588 | 18 |
| 7 | Central McDougall | $66,673 | $38,038 | 27 |
| 11 | Tawa | $51,472 | $21,949 | 138 |
| 92 | Edmonton Northlands | $26,849 | $675 | 354 |

Citywide, **$131.2M of the $2,714.7M levy (4.8%)** sits on institutionally-zoned
land and **71% of it falls inside those 15 hoods** — so flagging 15 of 358
localizes nearly the whole question rather than smearing doubt across the map.
The headline claim survives untouched: Downtown (#1, 5% institutional),
Summerlea, Wîhkwêntôwin, Garneau and Boyle Street are all clean.

**DECIDED — the tooltip says it; the prism does not change.** Two muted rows on
the ≥25% hoods, gated on `isRevenue(state.metric)`. The prism stays solid and
coloured.

- ⚠️ **Not under Value**, and *not* for the road rows' reason. Exemption changes
  whether a levy is collected, not what a parcel is assessed at — Alberta
  assesses exempt property too — so `value_per_acre` is not uncertain in this way
  and a caveat there would claim a doubt the data does not carry. (This is also
  why there is no `value_frac_inst` to build one from.)
- ⚠️ **"Zoned" is load-bearing in the copy.** The row above it is an assessment
  **class** share and this is a **zoning** share; they do not partition the same
  thing, and without the word they read as contradictory — EVERGREEN is 89%
  residential and 41% institutional, summing to 130%.
- Both surfaces read `INST_UNCERTAIN_MIN` itself rather than a copied 0.25, so
  the Lab and the map can never disagree about which hoods are uncertain;
  `verify-inst-caveat.js` pins set-equality, not a hard-coded list.
- The revenue-mix panel behind the click already carried this caveat in its
  footer note — the tooltip was the one silent surface.

**NOT decided — should the prisms go hollow on Money too?** That is the Lab's
full treatment on the default view, and it costs the colour of 4 of the top 11
(a hole in the central core, since Money's top-down choropleth read is primary).
It also reaches only one of Money's three modes: grid cells carry no
institutional share, so `glass` and `change` could not follow. Open in `TODO.md`.

## Cross-refs

- Current metric definition: `ARCHITECTURE.md` (join_and_calculate) + `DATA.md`.
- Tax-exempt current handling: `ARCHITECTURE.md` Key Decisions table.
- Colour scale + two-population finding: `docs/FINDINGS_revenue_scale.md`.
- Zoning land-use layer: `DATA.md` §5, `ARCHITECTURE.md` (`load_zoning.py`).
