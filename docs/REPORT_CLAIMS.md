# Report claims — what the written report may state, and where each claim is proven

**What this is.** The report itself is a Google Doc in Peter's Drive, edited by
Peter. Claude Code and Claude web read the doc and check it against this file.
**This file is the source of truth for claims; the doc is the source of truth
for wording.** Locked 2026-10-03 (`DECISIONS.md`).

**What this is not.** No report prose lives here, not even drafts. A row is one
summarized technical point plus the place that proves it. If a row needs a
paragraph, the paragraph belongs in the `FINDINGS_*` doc it points to.

## Rules

1. **Every row points at its proof**: a verified notebook section, a
   `FINDINGS_*` section, a `DECISIONS.md` date or a test. A claim with no
   resolvable pointer does not go in, and the report should not state it.
2. **Weekly-live figures get a pointer, not a number.** The verified notebooks
   recompute them every Monday. Freezing one here is how `docs/METHODS.md` went
   stale (it was still quoting 2025 mill rates after the pipeline moved to 2026).
   Fixed constants and one-off measurements may carry the number, with the date
   or data vintage it was measured on.
3. **Withdrawn claims stay, as rows.** A report is most likely to repeat
   something that was once said and later disproven.
4. **Status vocabulary:**

| status | meaning |
|---|---|
| **confirmed** | measured or checked; the report may state it as written |
| **caveated** | true, but only with the caveat in the row |
| **contested** | two sources in this repo disagree; don't use it until resolved |
| **withdrawn** | was claimed, is wrong; the report must not state it |

5. **A fact-check pass** over the doc flags every claim that has no row here,
   or that contradicts a row. Unmatched claims are reported, not silently
   accepted. That is the report-side form of "no silent data drops".

---

## Method

| id | claim | status | proof | live? |
|---|---|---|---|---|
| M1 | The metric is **municipal** levy per acre. The provincial education levy is excluded: the project measures the City's fiscal capacity, not a household's tax burden. | confirmed | `notebooks/verified/02_methods.py` §1 | rule |
| M2 | Per account, levy = Σ over tax classes of assessed value × class % × municipal mill rate (`pwis-wc4c`), summed by neighbourhood. | confirmed | `02_methods.py` §1 | rule |
| M3 | The gap between the value view and the revenue view is exactly the class-differential mill rates (non-residential is taxed a multiple of residential per dollar). | confirmed | `02_methods.py` §1 | **live** — cite the multiple from the page, never from here |
| M4 | Two denominators. **Ground acres** (boundary polygon, includes roads and parks) is the default because it never reads a lot-size field. **Lot acres** is the one comparable to Urban3's method. The ground-acre default is this project's addition, not borrowed methodology. | confirmed | `02_methods.py` §1; `FINDINGS_denominator_cardinality.md` | rule |
| M5 | The lot-acre view drops **roads and unparcelled land** (river valley, water). It does **not** drop parks or big lots: parks on the roll are counted, and a neighbourhood of big lots reads *lower* per lot acre. | confirmed | `FINDINGS_blurb_claims.md` §2 (F3) | rule |
| M6 | Neighbourhoods whose titled lots cover too little of the boundary are greyed in lot-acre mode, not shown. | confirmed | `02_methods.py` §1 | **live** count |
| M7 | Condominiums use a repeat-aware lot rule instead of being excluded. Points the rule cannot read are excluded from the lot-acre view and reported; their dollars stay in the ground-acre view. | confirmed | `02_methods.py` §2; `FINDINGS_lot_dedupe.md` | **live** counts |
| M8 | Set-aside neighbourhoods (mostly river valley, parks, or future-development reserve by zoning) render grey and are not ranked. Their revenue is real and stays in the totals. | confirmed | `02_methods.py` §3; `FINDINGS_revenue_scale.md` | **live** count |
| M9 | Prism height is always linear. Colour ramps may use square-root or log transforms, and the app can switch them off. | confirmed | `02_methods.py` §6; `FINDINGS_revenue_scale.md` §6 | rule |
| M10 | The 100 m grid (Glass) is pure point binning: one coordinate per account, no interpolation. A property larger than a cell puts all its dollars in one cell. | caveated — the lot-acre toggle is the counterweight | `02_methods.py` §4; `03_assumptions.py` (Glass row) | **live** size |
| M11 | "Assessed value" is land **plus buildings**. It is not "land value", which is a different term of art. | confirmed | `FINDINGS_blurb_claims.md` §2 (F6) | rule |

## Exempt and institutional land

| id | claim | status | proof | live? |
|---|---|---|---|---|
| E1 | Edmonton publishes **no per-parcel exemption status**, so no map built from open data can say which institutional dollars are real. | confirmed | `DATA_ISSUES.md` issue 4; `notebooks/standalone/exemption_uncertainty.py` | evidence, re-checked monthly |
| E2 | The error runs **both ways**. Some exempt land is on the roll with a computed levy (hospitals, the U of A campus; 2,254 parcels on UI/UF/AJ/PU zoning carry $5.6B), which may **overstate** revenue. Some is genuinely absent (e.g. the Legislature), which **understates** it. | caveated | `FINDINGS_exempt_institutional.md` (premise corrected 2026-08-07); `03_assumptions.py` (Money rows) | parcel count as of 2026-08-07; share is **live** |
| E3 | ⚠️ "Exempt institutions are **absent from the roll**, not listed at zero" — the blanket form. | **contested** — the 2026-08-07 correction says it is false, but `02_methods.py` §3 and §8 item 1 still publish it weekly. Don't use until the methods page is fixed. | `FINDINGS_exempt_institutional.md`; `data/DATA.md` "Tax-exempt flag" | — |
| E4 | Share of **non-residential** levy sitting on exempt-candidate zoning, citywide: **16.4%** (spatial zoning, raw data of 2026-09-03). | confirmed | `FINDINGS_blurb_claims.md` §6 | as-of; **live** version in `03_assumptions.py` |
| E5 | The neighbourhood bands and tooltip caveats gate on the exempt share of **total** levy, so on the Non-residential cut 144 of the 165 neighbourhoods with ≥25% exempt-candidate non-res levy get no band. | caveated — known display gap, fix proposed (TODO F1+F2) | `FINDINGS_blurb_claims.md` §6 | as-of 2026-09-28 |

## Roads (cost side)

| id | claim | status | proof | live? |
|---|---|---|---|---|
| R1 | Road metres are City-maintained **collector and local** centreline per acre. Arterials are excluded as shared citywide infrastructure; alleys and provincial highways are out. | confirmed | `02_methods.py` §5; `DECISIONS.md` 2026-07-01 | rule; arterial share **live** in `03_assumptions.py` |
| R2 | Two cost bases price those metres: **lifecycle $50** and **operating $9.32** per road-metre per year. They are never summed or compared on a served surface. | confirmed | `FINDINGS_roads_rate_notebooks.md` (L8); `02_methods.py` §5 | constants in `data/city_unit_costs.json` |
| R3 | $50/m = ($600,000 + $1,900,000) per centreline km over a 50-year life. The source figures are quoted verbatim from the City's *Development Impact on Infrastructure* page. | confirmed | `notebooks/standalone/roads_lifecycle_rate.py`; `FINDINGS_roads_rate_notebooks.md` (L1, L2) | fixed |
| R4 | The **50-year** life is an argument, not a measurement. The audited books imply 36–38 years, and the one unaccounted bias pushes the true figure lower still. | caveated | `FINDINGS_roads_rate_notebooks.md` §2 | fixed |
| R5 | $9.32/m = roadway maintenance ($5,970 per **lane**-km, FY2017 budget) + snow clearing ($3,350). The lane-km unit is disclosed, not converted, by decision. | caveated | `roads_operating_rate.py`; `DECISIONS.md` 2026-09-08 | fixed |
| R6 | The snow **programme total** is corroborated ($67M reported vs the City's FY2025 $67.55M). The **55% roads share** that reaches the rate rests on one secondary source. Each 5 points of share moves the rate about 3%. | caveated | `FINDINGS_roads_rate_notebooks.md` §4 | fixed |

## Change over time

| id | claim | status | proof | live? |
|---|---|---|---|---|
| T1 | The published series is roll years **2012–2023 plus 2026**. 2024 and 2025 are omitted on purpose: the 2024 slice is proven incomplete, and the real 2025 roll is unrecoverable. The gap is two years wide and deliberate. | confirmed | `SPEC_temporal.md` §0; `DATA_ISSUES.md` issue 3 | fixed until a publisher fix |

## Development

| id | claim | status | proof | live? |
|---|---|---|---|---|
| D1 | The grid shows only geocoded permits; the neighbourhood view counts all of them. Over the since-2009 window about half the off-grid units come from 2009–2020 permits — a **permanent** gap concentrated in older apartment permits, not only a geocoding lag. | caveated | `FINDINGS_blurb_claims.md` §2 (F4); `03_assumptions.py` (Development rows) | **live** shares |
| D2 | The neighbourhoods at the top of the growth scale are mostly **greenfield subdivisions**, not infill. | confirmed | `FINDINGS_blurb_claims.md` §2 (F5) | as-of 2026-09-26 |

## Upstream data

| id | claim | status | proof | live? |
|---|---|---|---|---|
| U1 | Six issues with Edmonton open data are documented (issues 1 and 3–7; issue 2 was this project's own and is fixed). Five have a published evidence notebook; issue 7 (`stt5-pzaa`) has none yet. As of 2026-10-03 **none has been reported to its publisher**. | confirmed | `DATA_ISSUES.md` "Status at a glance" | send status changes by hand |

---

## Withdrawn — the report must not say these

| id | claim as once made | why withdrawn | proof |
|---|---|---|---|
| X1 | "The paved roads poor share rose from 11.5% to 12.5%." | 2023 *Paved* almost certainly included curbs and 2025's does not; ex-curbs the share is roughly flat. Not a trend. | `FINDINGS_roads_rate_notebooks.md` §3 |
| X2 | "The snow figures are independently corroborated." | Only the programme total is; the 55% split that ships is not (R6). | `FINDINGS_roads_rate_notebooks.md` §4 |
| X3 | "The two road cost bases are ~5.4× apart." | A unit artifact (lane-km vs centreline km); about 3.0× on one unit. | `FINDINGS_roads_rate_notebooks.md` §6 |
| X4 | "9% of non-residential levy is on exempt-candidate zoning." | An artifact of blank roll zoning; the figure is 16.4% (E4). | `FINDINGS_blurb_claims.md` §6 |
| X5 | "The lot-acre view stops parks, river valley and big lots diluting the figure." | Wrong for parks and backwards for big lots (M5). | `FINDINGS_blurb_claims.md` §2 (F3) |
| X6 | "Dense-infill areas top the growth scale." | The top is greenfield (D2). | `FINDINGS_blurb_claims.md` §2 (F5) |
| X7 | "Exempt institutional land is absent from the roll entirely." | False as a blanket claim (E2, E3). | `FINDINGS_exempt_institutional.md` |
