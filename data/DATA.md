# Data Sources

Reference for raw input files. Update this file when you discover column name quirks, encoding issues, or anything unexpected. Do not rely on memory — write it down here.

**Socrata download completeness (applies to every source below):** Socrata
truncates silently at `$limit` — it returns exactly that many rows with no
error. Historically SODA 2.0 also imposed a **server-side 50,000-row cap** on
`$limit`; Edmonton's endpoints demonstrably don't today (the road network
returned 53,720 features in one request, 2026-07-01), but a platform cap could
(re)appear without touching our config. `scripts/download_data.py` therefore
verifies every download two ways: post-download count vs. **our** declared
`$limit` (fails at count >= limit), and vs. the **live server count** via
`$select=count(*)` (mismatch fails hard; an unreachable count endpoint only
warns — the guard must not add fragility). Verified against all four sources
2026-07-01.

---

## 0. Property Assessment Data (Historical) — CATALOGUED 2026-07-28, NOT YET USED

**Not in `download_data.py` and not in `data/raw/`.** Catalogued because the
shape was measured live and it unblocks the per-neighbourhood assessment-over-
time graph (`TODO.md`). Numbers below are from the API on 2026-07-28.

> ### 🛑 THE RECENT SLICES ARE INCOMPLETE — DO NOT USE 2024/2025 AS-IS
>
> **Proven 2026-07-28 against the current roll (§1), same assessment year:**
>
> | Downtown, assessment year 2025 | accounts | value |
> |---|---|---|
> | **`q7d6-ambg` current roll (what we ship)** | **11,216** | **$7.81B** |
> | `qi6a-xuwt` historical, 2025 slice | 10,307 | $7.09B |
> | **missing from historical** | **909** | **~$720M** |
>
> Two entire ICE District towers are absent from the historical dataset's 2024
> **and** 2025 slices while present in the current roll:
> **10310 102 STREET NW** (Stantec Tower — 309 accounts / $144.5M in the 2023
> historical slice, **gone** in 2024–25, but **310 accounts / $105.7M in the
> current roll**) and **10360 102 STREET NW** (261 accounts / $206.0M → gone →
> **261 / $202.1M in the current roll**). Buildings that appear in 2023, vanish
> in 2024–25, and reappear in the current roll were not demolished.
>
> **SCOPE — CITYWIDE, measured account-by-account 2026-07-28.** An earlier
> "~8,000 accounts citywide" figure was **inferred from row counts and was
> misleading** — most of that gap is new construction, not defect. The honest
> decomposition of the 7,929-account net gap:
>
> | | accounts | what it is |
> |---|---|---|
> | in current roll, **absent from historical 2025, and not in 2023 either** | 8,171 | almost certainly new titles/construction — a snapshot-vintage difference, benign |
> | in historical 2025 but not the current roll | ~2,690 | demolitions/consolidations between snapshots, benign |
> | **in historical 2023 AND in the current roll, but ABSENT from historical 2025** | **2,448** | **the genuine defect — a property that existed then and exists now cannot legitimately be missing in between** |
>
> **The 2,448 carry $2.93B of current assessed value and span 188
> neighbourhoods** — so this is citywide, not a Downtown curiosity, though
> Downtown holds **1,292 of them (53%)**. Next worst: MAGRATH HEIGHTS 430,
> GLENORA 269, WÎHKWÊNTÔWIN 124. By class: 2,056 residential, 373 commercial.
>
> **They cluster at individual multi-unit addresses — whole buildings vanish
> together**, and not only downtown towers: 10310 102 ST NW (310), 10360 102 ST
> NW (261), **7463 MAY COMMON NW (162, Magrath Heights)**, 10155 116 ST NW (123,
> Wîhkwêntôwin), 14105 WEST BLOCK DRIVE NW (60, Glenora). *Stated as a symptom
> only — the cause is not ours to diagnose.*
>
> **Practical effect per hood:** Magrath Heights is missing 17% of its accounts
> and Glenora 15%, so the 2025 slice is unusable at hood level well beyond
> Downtown.
>
> **Mechanism of the disappearance, measured:** 1,359 Downtown accounts present
> in the 2023 slice are absent from the 2024 slice. Traced individually across
> the whole 2024 roll — **1,358 of 1,359 do not exist anywhere in it**; exactly
> one moved (to OLIVER). They did not change neighbourhood, were not recoded into
> another hood, and only 2 reappear in 2025.
>
> **EXTENT — MAPPED 2026-07-28** (`tools/audit_historical_roll_gaps.py`, all 14
> years): **the defect is confined to 2024–2025.** 2013–2023 show 0–14 defect
> accounts per year against rolls of 346k–426k (0.00%); 2024 shows **2,322** and
> 2025 a further **131** incremental, ~2,448 cumulative. **One event, two
> slices** — not systemic decay. So **2012–2023 are usable**, 2025 is repairable
> by splicing the current roll, and **2024 is the only irreparable year**.
>
> ⚠️ **The obvious detector does not work here.** "Present in N−1 and N+1, absent
> from N" is blind to a dropout that never returns — it reported **5** for 2024
> where the truth is 2,321. Any check of this dataset must also test against the
> **current roll**, which is independent and complete.
>
> **Before ANY series ships:** validate each historical year against a control,
> and treat recent years as suspect until they reconcile with the current roll.
> Same guard idiom as `check_year_alignment.py` / `check_value_anchors.py`.
> **Splice: historical for 2012–2023, the current roll for the live year.**
> **2024 has no such fix** — there is no current-roll equivalent for it.
>
> ✅ **BOTH ARE BUILT (2026-07-28):** the splice is `src/load_temporal.py` and the
> guard is `scripts/check_temporal_years.py` (wired into `refresh.yml` before the
> status-manifest step). **This dataset is no longer "not yet used" — but note
> what IS used: `scripts/download_data.py --only assessment_historical` fetches a
> ~14,800-row SERVER-SIDE AGGREGATE** (`$group` by year × hood × mill class) into
> `data/raw/assessment_historical_by_hood.csv`, never the 5.5M raw rows.
>
> ⚠️ **The generic truncation check does not apply to an aggregate.** A `$group`
> download's row count is the number of GROUPS, so it can never equal the
> dataset's `count(*)`. The source declares `sum_column: n_accounts` instead and
> `download_data.verify_download` checks that the per-group counts **sum** to the
> live row count (5,501,958 as of 2026-07-28) — strictly stronger, since it also
> catches a whole group vanishing.
>
> ⚠️ **2025 IS ONLY REPAIRABLE WHILE IT IS THE LIVE YEAR.** The current roll
> covers exactly one year. When the roll advances to 2026, 2025 loses its only
> complete source and **drops out of the published series** — `publishable_years`
> handles this, and the guard fails if it is ever republished from the historical
> file. Preserving 2025's repaired numbers past that point needs an archived
> artifact that does not exist yet (`TODO.md`).
>
> **Do not silently smooth this.** A 909-account hole in the headline
> neighbourhood produced an apparent $2.07B collapse where the real decline is
> $1.35B — see `docs/ANALYSIS_BACKLOG.md`.

**Reportable evidence for the defect:** `notebooks/standalone/historical_2024_gap.py`
re-measures it live from the portal (no repo dependency) and is the artifact to
send with a data-quality report — it runs both detectors, shows the missing
accounts cluster into whole buildings, and lists account numbers Edmonton can
check by hand.

**Source:** Edmonton Open Data — dataset ID `qi6a-xuwt` ("Property Assessment
Data (Historical)")
**Coverage:** **14 years, 2012–2025**, 5,501,958 rows total (337k in 2012 rising
to 432k in 2025 — the roll grows with the city).
**Columns:** same shape as the current roll (§1) — `account_number`,
`assessment_year`, `neighbourhood_name`, `assessed_value`, `mill_class_1`,
`tax_class_pct_1`, `lot_size`, `zoning`, `year_built`, `latitude`/`longitude`,
`point_location`.

**⚠️ Do NOT download this whole dataset — aggregate server-side.** It carries
`neighbourhood_name`, so Socrata can do the grouping:

```
https://data.edmonton.ca/resource/qi6a-xuwt.json
  ?$select=neighbourhood_name,assessment_year,sum(assessed_value) as total,count(1) as n
  &$group=neighbourhood_name,assessment_year
  &$limit=50000
```

**Measured:** 5,577 rows / **443 neighbourhoods** in **~3 s, 534 kB** of verbose
JSON. Re-shaped as array-of-arrays that is well under 100 kB before gzip.
Note `$limit=50000` is required — the default page size is 1,000, and 443×14
would silently truncate. (See §head for the historical 50,000-row server cap.)

**Known quirks:**
- **443 hoods here vs the current roll's count** — expect names that have since
  been renamed, merged, or annexed. Any join to the neighbourhood boundary file
  MUST go through the same normalization + `check_unmatched_names.py` policy as
  everything else; no silent drops.
- Some rows carry a null/blank `neighbourhood_name` (filtered in the count
  above) — they are not free to ignore, they need the same explicit flagging.
- **`mill_class_1` alone does not reconstruct revenue** — the current pipeline
  uses the full class/percentage split. Historical *rates* live in `pwis-wc4c`
  (§"Property and Education Tax Rates"), which starts **2014**, so a revenue
  series cannot reach back to 2012 even though value does.

---

## 1. Property Assessment Data

**File:** `data/raw/Property_Assessment_Data__Current_Calendar_Year_.csv` *(filename as delivered by the API)*
**Download:** `scripts/download_data.py`
**Source:** [Edmonton Open Data](https://data.edmonton.ca/City-Administration/Property-Assessment-Data-Current-Calendar-Year-/q7d6-ambg) — dataset ID `q7d6-ambg`
**API URL:** `https://data.edmonton.ca/api/views/q7d6-ambg/rows.csv?accessType=DOWNLOAD`
**Format:** CSV, 439,769 rows. **Live feed, updated weekly** (Socrata
`Update Frequency: Weekly`); the assessment *year* rolls annually.
**Assessment year:** **2025** — i.e. effective 2025-01-01 to 2025-12-31. The year
is **not a column in the rows**; it lives only in the dataset metadata
(`https://data.edmonton.ca/api/views/q7d6-ambg.json` → description /
`custom_fields.Time Frame.Period of Coverage`). Our local snapshot was downloaded
2026-05-16 and is 2025 data. **Re-check the metadata after any re-download** — a
later pull can roll to a new year, which would silently desync from any
year-matched mill rates (see `docs/SPEC_revenue.md`). **This re-check is now
automated in CI** (`scripts/check_year_alignment.py`, added 2026-07-01): every
scheduled refresh compares the metadata year against the pinned
`ASSESSMENT_YEAR` and holds (skip regen + banner) on mismatch.
**Re-download 2026-07-02** (deployment dry-run + first CI run): metadata still
effective **2025** (intra-year edits only, no year roll), so 2025 rates stay
aligned. That pull also surfaced a new `Assessment Class 1` label
`DESIGNATED IND PROPERTIES` (1 row) — mapped to Non Residential; see
`docs/FINDINGS_assessment_classes.md`.
**Licence:** Open Government Licence – City of Edmonton

### Columns (confirmed 2026-05-22)

| Column | Type | Notes |
|--------|------|-------|
| `Account Number` | int64 | Unique property identifier |
| `Suite` | float64 | Mixed types — use `low_memory=False` on load |
| `House Number` | int64 | |
| `Street Name` | str | |
| `Neighbourhood ID` | int64 | Numeric neighbourhood key |
| `Neighbourhood` | str | Normalize (strip + uppercase) for joining |
| `Ward` | str | |
| `Assessed Value` | int64 | Main metric — 46 zero-value rows, 0 nulls (confirmed) |
| `Tax Class` | str | Values: Residential, Non Residential, Other Residential, Farmland |
| `Garage` | str | |
| `Assessment Class 1` | str | See values below — no explicit "exempt" flag |
| `Assessment Class 2` | float64 | |
| `Assessment Class 3` | float64 | |
| `Assessment Class % 1` | int64 | |
| `Assessment Class % 2` | float64 | |
| `Assessment Class % 3` | float64 | |
| `Latitude` | float64 | |
| `Longitude` | float64 | |
| `Point Location` | str | |

**Assessment Class 1 values:** RESIDENTIAL (411,563), COMMERCIAL (23,054), OTHER RESIDENTIAL (4,356), FARMLAND (509), MA DERELICT RESIDENTIAL (284), NONRES MUNICIPAL/RES EDUCATION (3)

**Tax-exempt flag:** No explicit exempt boolean. Best proxy is `Assessment Class 1 == 'NONRES MUNICIPAL/RES EDUCATION'` (3 rows). Flag these on load as `is_exempt`. So `is_exempt` cannot identify exempt-heavy neighbourhoods.

⚠️ **CORRECTED 2026-08-07 — institutional land is NOT uniformly absent from this roll, and the previous version of this line said it was.** It read: *"tax-exempt institutional land (Legislature, schools, hospitals, City property) is **absent from the taxable roll entirely**, not flagged or zeroed"* (noted 2026-06-29). Measured against the roll, that is **half right and half wrong**, and the wrong half is load-bearing:

- **Present.** Every major hospital is on the roll, and was before the Jul-6 snapshot: Royal Alexandra `11495590` $273.8M, Misericordia `11495573` $247.8M, Grey Nuns `11495606` $196.9M, Cross Cancer `11495587` $68.1M. The U of A campus is on it too — `11495614` $577.1M, `11495565` $437.7M, `9996778` $430.8M.
- **Absent.** The Alberta Legislature is genuinely not there (0 rows at 10800 97 AVENUE NW; no `LEGISLATURE` neighbourhood), so the original observation was true of provincial Crown land and got generalised.

**Sized by spatial join of all 439,685 parcels against `zoning.geojson`** (2026-08-07; 8 parcels matched no polygon). Parcels sitting on the four exempt-proxy zones:

| zone | | parcels | assessed | modelled levy |
|---|---|---|---|---|
| `AJ` | Alternative Jurisdiction | 340 | $2,599,819,500 | $60.3M/yr |
| `UF` | Urban Facilities | 768 | $1,951,061,000 | $41.4M/yr |
| `UI` | Urban Institution | 39 | $690,542,500 | $15.7M/yr |
| `PU` | Public Utility | 1,107 | $380,635,000 | $8.0M/yr |
| | **total** | **2,254** | **$5,622,058,000** | **$125.4M/yr — 4.6% of the $2.71B citywide served total** |

⚠️ **What this does NOT establish.** Being on the assessment roll with an assessed value is **not** the same as being levied: this dataset publishes assessments and a `Tax Class`, it does not publish exemption status, and Alberta assesses some exempt property. The pipeline applies mill rates to every record here, so **whether that is correct for these 2,254 parcels is an open question** (`TODO.md`), not a settled defect. ⚠️ **Zoning is also not ownership** — `UF` and `PU` include privately-owned facilities.

⚠️ **HOW THE $125.4M/yr MUST BE DESCRIBED, whenever it is quoted (locked 2026-08-08).** It is a **gross modelled figure, not a revenue loss and not a foregone-revenue estimate**:

> **Gross modelled tax if every institutional/public-zoned parcel were fully taxable.** Alberta law exempts many of these properties (hospitals, universities, government land); the actual taxable share is not publicly known.

The failure mode this guards against is quoting it as "$125.4M the City doesn't collect", which asserts an exemption status **no public source states** and which our own data cannot support either way. ⚠️ **The direction of the error is unknown, not merely unquantified** — if the City levies these parcels the modelled figure is right, and if it exempts them the model *overstates* the hoods holding them. `docs/FINDINGS_revenue_scale.md` §5 states this and used to state the reverse.

**The one nearby external reference point, and its limits.** Alberta's **Grants in Place of Taxes (GIPOT)** program pays municipalities for **Government of Alberta** property, which is exempt from municipal taxation; the federal PILT equivalent covers correctional, RCMP and military property. ⚠️ **Three cautions before this is used as an anchor for the figure above:**
- ⚠️ **No dollar amount is verified.** The City's own GIPOT page publishes **no figure at all** — only the percentage history. A "$15.7M for 2021-22" figure has been circulated to this project; secondary reporting puts Edmonton's GIPOT "at $15 million per year", consistent in magnitude but **not a confirmation of that number, that year, or that scope**. Do not publish it until a primary source is in hand.
- ⚠️ **Any 2020–2024 receipt is a HALF payment.** Alberta cut GIPOT to **75% of the calculated amount in 2019, then 50% for 2020–2024**, restored to 75% in 2025 and **100% in 2026**. So a 2021-22 receipt is roughly **half** the assessed-tax equivalent, and reading it as one understates by ~2×.
- ⚠️ **Coverage is narrower than the four zones.** GIPOT is a Government of Alberta program; **universities, hospitals and non-profits are not the Government of Alberta** and appear to fall outside it — but the program page does not enumerate exclusions, so *that* is inference, not a sourced statement. GIPOT therefore cannot net off the $125.4M even if the dollar figure were confirmed.

Sources checked 2026-08-08: [City of Edmonton — Grants in Lieu of Taxes](https://www.edmonton.ca/residential_neighbourhoods/property_tax_assessment/tax_exemptions_relief/grants-in-lieu-taxes), [Alberta — Grants in Place of Taxes program](https://www.alberta.ca/grants-in-place-of-taxes-program).

⚠️ **AND ABSENCE FROM THIS ROLL IS OFTEN TRANSIENT, NOT STRUCTURAL** (established 2026-08-07, and it is why the "absent entirely" claim above looked true). **Every identifier in these datasets churns:**

| identifier | churns how | worked example |
|---|---|---|
| `Account Number` | **renumbered** | all four major hospitals moved into a new `114955xx` block at the 2025 roll; the old numbers vanish from the current roll and the new ones appear in **no year** of `qi6a-xuwt` |
| address | **re-addressed** | `WESTMOUNT SHOPPING CENTRE NW` no longer exists as a street name |
| `Neighbourhood` | **renamed** | OLIVER → WÎHKWÊNTÔWIN moved 12,237 parcels; a per-hood value comparison reads that as **−100%** |

**A property can therefore be missing from the published current roll while still existing and still being assessed.** Misericordia Community Hospital was continuously assessed 2012–2025 as account `10095840` (~$200–260M, always WEST MEADOWLARK PARK), was renumbered to `11495573`, and was **absent from `q7d6-ambg` until 2026-08-03** — during which the map understated that neighbourhood by ~$250M of assessed value. ⚠️ **The two datasets disagree about account numbers for the SAME assessment year 2025** (historical still says `10095840`, current says `11495573`), so **cross-dataset account-number joins are unreliable for renumbered parcels.**

⚠️ **Renumbering is ROUTINE.** Year-over-year in the historical roll, accounts vanish at **0.15%–0.37%/yr** (2023→2024 spikes to **0.91%, 3,893 accounts**). A vanished account number is not by itself a finding.

**Position is stable enough to MATCH, but not to CONVICT.** `tools/audit_roll_continuity.py` matches parcels by position, independently of all three churning identifiers; re-run 2026-08-30 against historical 2024, **1,457 of 426,913 parcels (0.34%) had no current match, $1.07B assessed** (supersedes 1,534 / $1.62B from 2026-08-07). ⚠️ **The "coordinates move under 2 m" figure is a four-hospital sample and does NOT generalize**: 121 parcels the position match called missing are on the current roll under the same account number, having moved a median **58 m** (max 559 m). The tool now acquits those by `account_number` — an identifier may **acquit** here even though it must never **match**, because acquitting can only remove false positives. ⚠️ Those 1,457 remain candidates, not verdicts, and an upper bound — demolitions, subdivisions and consolidations legitimately have no 1:1 successor. (`legal_description` — plan/block/lot — would be a better key and is immutable, but exists **only** in the historical roll, so it cannot join the two.)

⚠️ **Two artifacts rest on the retracted claim and are UNVERIFIED against this correction:** `docs/FINDINGS_exempt_institutional.md` and `tools/audit_exempt_institutional.py` proxy exempt land as *polygon acres − taxable lot acres*, which under-counts by exactly the parcels above; `docs/ANALYSIS_BACKLOG.md` §7 (closed 2026-07-09) rests on the same premise. The direction of the original concern still holds — revenue/acre understates neighbourhoods holding large exempt institutions — but its **magnitude is not what those documents state**. See also `docs/FINDINGS_revenue_scale.md` §4–5, written under the old premise.

### Known Quirks

- Condo units: multiple rows share one land parcel — this is expected and correct for this analysis
- `Suite` column has mixed types — always load with `low_memory=False`
- 46 rows have `Assessed Value == 0` — drop and flag count on load
- No explicit tax-exempt column; proxy is `Assessment Class 1 == 'NONRES MUNICIPAL/RES EDUCATION'`, which is near-empty (3 rows). ⚠️ **This bullet used to add "because exempt institutional land is absent from the roll" — that reason is RETRACTED, see the Tax-exempt flag note above.** The proxy is near-empty regardless, but hospitals and the U of A campus *are* on the roll and $5.6B of assessed value sits on exempt-proxy zoning. The near-zero-revenue tail is **low-coverage** land (river valley / undeveloped), not exempt. See `docs/FINDINGS_revenue_scale.md`.
- Assessment year is metadata-only, not in the rows (year = 2025; see Format note above) — pin it against the mill-rate year for the revenue phase

---

## 2. Property Info Dataset (Lot Size, Zoning, Year Built)

**Source:** Edmonton Open Data — dataset ID `dkk9-cj3x` ("Property Info - Current Calendar Year")
**API URL:** `https://data.edmonton.ca/resource/dkk9-cj3x.json`
**Format:** SODA JSON API (no bulk CSV download confirmed; query via API)
**Rows:** 439,769 (confirmed 2026-05-27 — closely matches assessment CSV row count)
**Licence:** Open Government Licence – City of Edmonton

**Reference implementation:** `scripts/edmonton_property_api_stuff.py` — Python equivalents of the JS query functions from the open-property app (github.com/[author]/open-property), reverse-engineered to understand how lot_size is sourced.

### Columns (confirmed 2026-05-27)

| Column | Type | Notes |
|--------|------|-------|
| `account_number` | str | Join key to assessment dataset (`q7d6-ambg`) |
| `house_number` | str | |
| `street_name` | str | |
| `legal_description` | str | |
| `zoning` | str | e.g. `RSF` — nullable |
| `lot_size` | str (numeric) | Pre-computed by city; **not geometry-derived**. Units: sq metres (confirmed — sample value 335 m² is a typical residential lot). 2,728 nulls (~0.6%). |
| `total_gross_area` | str | Building floor area |
| `year_built` | str | Nullable. **Loaded since 2026-07-17** (Development stock-age spikes): 418,368 of 439,685 rows (95.2%), range 1881–2026, zero non-numeric junk; every row with a year also has coordinates. Loader nulls values outside [1850, 2100] (plausibility window, `load_property_info.YEAR_BUILT_MIN/MAX`). |
| `garage` | str | |
| `neighbourhood_id` | str | Numeric key |
| `neighbourhood` | str | ALL CAPS — consistent with assessment data |
| `ward` | str | |
| `latitude` | str | |
| `longitude` | str | |
| `point_location` | GeoJSON Point | Single coordinate per property — **no parcel polygon** |

### Key Findings

- **`lot_size` is a city-provided field, not computed** — Edmonton supplies it directly via the API. No geometry math needed.
- **No parcel polygon geometry** — only a centroid point. Edmonton transferred parcel GIS data to AltaLIS in 2021; it's no longer freely available. Polygon boundaries require the neighbourhood boundary file (dataset `65fr-66s6`).
- **`lot_size` units are sq metres** — divide by 4046.86 to get acres. (~0.6% null — minor, flag on load)
- **`Total Gross Area` units are sq metres too** (confirmed 2026-07-07: the
  RESIDENTIAL-class median is 112.7 — a ~1,200 sq ft house). The water lens
  (`src/load_water.py`) uses it to estimate multi-res unit counts (90 m²
  gross/unit assumption); 1,018 of 4,353 OTHER RESIDENTIAL rows have
  null/zero values — those buildings drop from the water model, counted.
- **`Total Gross Area` is now loaded by `load_property_info` (as `gross_area`)
  for the Development Lens B FAR** (2026-07-13) — the built floor-area ratio
  suitability proxy: `far` = Σ `gross_area` (per unit, over eligible points) ÷
  deduped lot area per hood, computed in `build_hood_lot_acres` on the same
  dedupe as the lot-acre denominator. 27,202 rows (~6.2%) have null/zero
  `gross_area` (flagged on load). ⚠️ **A hood whose eligible rows record NO floor
  area gets `far = null`, NOT 0** (changed 2026-08-22): null and zero both mean
  "not recorded", and `far == 0` is the maximum-OPPORTUNITY end of the Infill
  scale, so summing the gap to 0 turned absent data into a finding. **16 of 410
  hoods** are null on the current snapshot — 12 already set-aside grey, 4 newly
  off the scale, of which one (EVERGREEN, 4 eligible rows) is residential.
  Sanity: FAR
  ranges DOWNTOWN 3.37 / WÎHKWÊNTÔWIN 1.89 / GARNEAU 1.53 (densest) down to ≈0
  at River Valley / Anthony Henday greenfield edges. Low FAR = underused. Ships
  in the neighbourhood geojson (`far`, SLIM). See `docs/SPEC_development.md`
  Lens B for the proxy decision + the low-FAR park/greenfield caveat.
- **Condo `lot_size` semantics are INCONSISTENT (confirmed 2026-07-04)** — at the
  3,002 lat/long points holding multiple units, `lot_size` is sometimes the parcel
  size duplicated on every unit (summing overcounts the land), sometimes per-unit
  apportioned shares (summing is correct), and sometimes null/zero (one 1,059-unit
  building has nulls on 1,051 of them). No flag distinguishes the regimes. This is
  why the Glass view's grid export divides by cell GROUND acres, not lot acres
  (`src/export_value_grid.py`). **Dedupe heuristic built + validated
  2026-07-05** — repeat-aware: repeated values < 1000 m² are per-unit shares
  (count each; a plain distinct-sum collapses townhouse complexes and fakes
  needles), ≥ 1000 m² are duplicated parcels (count once); majority-null
  multi-unit points ineligible (56 points / 0.52% of roll, reported); per-hood
  bound test passes 405/406 (PEMBINA the known outlier, enforced by
  `check_lot_acre_bounds`). Full numbers: `docs/FINDINGS_lot_dedupe.md`.
- **One lat/long per account concentrates large parcels onto a single point
  (quantified 2026-07-04)** — the coordinate is a centroid regardless of lot
  size, so any point-binned density map needles big lots: West Edmonton Mall
  is one account ($1.285B assessed, 433,592 m² lot) behind one point — in the
  100 m Glass grid that's the #1 cell citywide at $12.6M levy/acre, 2× the top
  downtown tower ($620M on 3,754 m²), even though per LOT acre the tower beats
  WEM ~50× ($612M vs $12M value/lot-acre). Citywide, lots > 1 ha are 5,524
  rows carrying ~18% of the $237.5B roll. The lot-acre denominator variant
  (TODO.md, PRIORITY) is the chosen correction.
- **Downloaded via `scripts/download_data.py --only property_info`** (added
  2026-07-04): full-CSV export endpoint, server count(*) cross-check; lands at
  `data/raw/Property_Info__Current_Calendar_Year_.csv`. Join to the assessment
  roll on `Account Number`: 100% coverage (439,685 rows both sides, 2026-07-04).
- **`zoning` column probed 2026-07-05 (for the stormwater lens,
  `docs/SPEC_utilities.md`):** null on 157,030 rows (35.71%); 78 distinct base
  codes (first token) among the rest, and they are **current Bylaw 20001
  vocabulary** (RS 146,567 / RSF 98,606 dominant — no legacy RF1-style codes in
  the top ranks). 98.2% of non-null rows use base codes that appear directly in
  EPCOR's runoff-coefficient table; the remainder are special-area codes (GLDF,
  PLD, SLD, BRH, …) needing explicit hand assignments. 282,655 rows (64.3%)
  have both non-null `zoning` and positive `lot_size`. Zone-null fallback:
  point-in-polygon against `fixa-tstc` (§5). Follow-ups from the build run:
  - The null `zoning` rows are almost all condo units at points where another
    row carries the zone: per POINT, only 4,509 of 287,163 lack any zone, and
    the `fixa-tstc` fallback resolves 4,508 of those (1 unresolved citywide).
  - **Three legacy old-bylaw codes linger** (1 point each): `US`, `CSC`, `RSL`
    — Bylaw 12800 vocabulary that never appears in `fixa-tstc`. Excluded +
    reported by `load_stormwater` (`ZONE_RUNOFF` covers current codes only).
  - **`Neighbourhood` contains two non-boundary names:** the known `OLIVER`
    straggler (1 row, zero lot) and `SPUR LINES` (1 row, 62.5 ha of IM-zoned
    rail-spur land, no boundary polygon) — both dropped + flagged at the
    stormwater join, immaterial by count.

### Architecture Decision — Phase 1

For Phase 1 (neighbourhood-level choropleth), two approaches are viable:

| Approach | How | Tradeoff |
|----------|-----|----------|
| **A — Boundary join** | Sum `assessed_value` by neighbourhood → join to boundary polygons → divide by polygon area | Requires `load_boundaries.py` + area calc; clean for mapping |
| **B — Parcel lot_size** | Join `dkk9-cj3x` to `q7d6-ambg` on `account_number` → sum `assessed_value` / sum `lot_size` by neighbourhood | Bypasses boundary file; condo duplication needs investigation first |

**Current plan: Approach A** (boundary join) — boundary file already downloaded, simpler data flow, no condo ambiguity. Revisit Approach B for Phase 2 if parcel-level detail is needed.

---

## 3. Neighbourhood Boundaries

**File:** `data/raw/neighbourhoods.geojson`
**Source:** [Edmonton Open Data](https://data.edmonton.ca/resource/65fr-66s6.geojson) — dataset ID `65fr-66s6` ("City of Edmonton Neighbourhoods")
**Download URL:** `https://data.edmonton.ca/resource/65fr-66s6.geojson?$limit=50000`
**Download:** `scripts/download_data.py` (fetches this alongside assessment + zoning; uses `$limit=500`, which covers all 407)
**Format:** GeoJSON, 2.9 MB
**Features:** 407 neighbourhoods
**Geometry type:** MultiPolygon (all features)
**CRS:** EPSG:4326 (WGS84) — reproject to EPSG:3400 before area calculation
**Licence:** Open Government Licence – City of Edmonton

### Columns (confirmed 2026-05-27)

| Column | Type | Notes |
|--------|------|-------|
| `neighbourhood_number` | str | Numeric neighbourhood key |
| `name` | str | ALL CAPS — use as `neighbourhood_name` join key |
| `descriptive_name` | str | Human-readable name (may differ from `name`) |
| `civic_ward_name` | str | Ward name |
| `district` | str | District name |
| `effective_start_date` | str | |
| `effective_end_date` | str | |
| `description` | str | |
| `geometry` | MultiPolygon | Boundary polygon |

### Known Quirks

- `name` is already ALL CAPS — matches our `neighbourhood_name` normalization convention
- 407 boundary features. Join outcome (after the 2026-07-01 audit corrections): 1 assessment neighbourhood with no boundary match (the immaterial `OLIVER` straggler, $500 — deliberately unmapped) and 1 boundary neighbourhood with no assessment data (`LEWIS FARMS`) → 406 of 407 boundaries rendered. See "Name Matching" below; flagged in `join_and_calculate.py`.
- ⚠️ **THIS FILE DOES TILE THE CITY — the earlier "14% has no neighbourhood" reading was a DISPLAY ARTIFACT, corrected 2026-08-09.** Measured in `EPSG:3400`: the 406 rendered hoods cover **782.0 km²** in this raw file (all 407 = **782.11**), against a legal boundary polygon of **782.38 km²**. They agree to **1.4 km²** — the raw fabric tiles Edmonton. What the 2026-08-08 note measured as a "109.6 km² gap" was `main.py`'s **`SETBACK_M = 45.0`** inward display buffer: **all 406** hoods shrink (median **18.3%**, min 2.7%, max 65.9%), and `buffer(-45)` + `simplify(10)` reproduces the shipped file's **672.42 km²** exactly. See §14.

### Served precision of `neighbourhood_value_per_acre.geojson` (2026-08-09)

⚠️ **The served file is rounded to 5 dp of coordinate and 6 significant figures
of attribute** (`WEB_PRECISION` / `WEB_SIGNIFICANT_FIGURES` in
`join_and_calculate.py`, applied as GDAL `COORDINATE_PRECISION` /
`SIGNIFICANT_FIGURES` at write time). **This is a served-payload decision, not a
computation change**: `export_geojson` returns the full-precision frame, and every
number is computed at full precision upstream.

Why it is a data-contract fact and not a formatting detail: **this file is fetched
at boot, before the map can draw data, by every visitor whatever lens they use** —
it is the one payload whose size grows with the number of lenses, because each
lens adds per-hood columns here. At 66 columns the attributes had already grown
larger than the geometry (176 KB vs 138 KB gzipped). GDAL's 15-digit default was
**half the gzipped payload**: 340 KB → 166 KB.

⚠️ **Anything reading this file for ANALYSIS now sees 6 significant figures** —
`tools/ward_rollup.py`, `ml_feature_importance.py`, `audit_outlier_tails.py` and
four others do. Six figures is far past what any of them need, but a *figure about
the world* should still come from `data/raw/`, for the reason §14 records.

---

## 4. Property and Education Tax Rates (revenue phase)

**File:** `data/mill_rates.json` *(curated extract — see provenance inside)*
**Source:** [Edmonton Open Data](https://data.edmonton.ca/resource/pwis-wc4c.json) — dataset ID `pwis-wc4c` ("Property and Education Tax Rates (2014 onward)")
**Format:** Socrata JSON/SODA API (live; updated annually — 2026 rates published 2026-04-29, and **PRE-STAGED in `mill_rates.json` since 2026-08-06**, inert until `ASSESSMENT_YEAR` rolls)
**Units:** amount per **$1,000** of assessed value (mills); also published per-dollar
**Licence:** Open Government Licence – City of Edmonton

Columns: `tax_year`, `tax_rate_type` (Municipal / Education / Education Requisition Allowance), `assessment_class`, `amount_per_1_000_of_assessed_value`, `amount_per_dollar_of_assessed_value`.

**2025 Municipal rates (per $1,000)** — the year matching our assessment snapshot:

| Tax Class | Municipal mill rate |
|-----------|---------------------|
| Residential | 7.6254 |
| Other Residential | 8.3116 |
| Non Residential | 24.2229 |
| Farmland | 7.6254 *(assumed = Residential — see quirks)* |

Non-residential is ~3.2× residential — this class differential is the basis of the revenue phase (`docs/SPEC_revenue.md`).

### Known Quirks

- **Join on assessment `Tax Class`** (clean 4-value field). Rate-table class names use spaces (`Non Residential`); some historical years use a hyphenated `Non-Residential` — normalize on load.
- **No 2025 Farmland rate published.** The source dropped a separate Farmland class in 2025. Municipal Farmland == Municipal Residential in every year 2014–2024, so `mill_rates.json` sets 2025 Farmland municipal = Residential (7.6254) as a **flagged assumption**, not authoritative. Low impact (509 farmland parcels).
  - ⚠️ **That assumption is now ON SCREEN** (2026-08-01): the mill-rate pod prints "Farmland rate assumed" beside the rates. It is driven by the **`_assumed` key in this file**, which `generate_status.py` turns into a list in `status.json` — so **adding a real 2025+ Farmland row with no `_assumed` key silently and correctly retires the caveat**. Do not delete the key to "clean up"; deleting it claims the rate was published.
- ⚠️ **This file now feeds the FRONT END, not just the pipeline** (2026-08-01). `generate_status.py` copies the current year's municipal rates into `web/data/status.json` as `municipal_rates`, which the mill-rate pod renders. Rates are never typed into `web/index.html`. Consequence for the January roll: adding a year here is still the single edit, but the committed `status.json` only picks it up when the refresh runs — `tests/test_generate_status.py` asserts the committed manifest matches what the generator would write, so a drift fails the suite rather than shipping stale rates.
- Rate-type label changed over time: older years (2014–2018) use `Municipal Tax Rate` / `Education Tax Rate`; 2019+ use `Municipal` / `Education`. Only 2019+ form is needed for 2025.
- `Mature Area Derelict Residential` and `Transitional Residential` exist as rate classes but not as assessment `Tax Class` values — unused by the Tax-Class join.
- **Two class vocabularies in the assessment CSV.** `Tax Class` (col 9) is the clean 4-value field used for the join. The `Assessment Class 1/2/3` (+ `% 1/2/3`) columns describe split-class parcels using *different* labels (`COMMERCIAL` = `Non Residential`, plus `MA DERELICT RESIDENTIAL` → Non Residential, `NONRES MUNICIPAL/RES EDUCATION` → exempt). `map(Assessment Class 1)` equals `Tax Class` in 100% of rows, so only the 2nd/3rd slices add information; split-class is rare (~0.25% of rows). Full label→rate-class map, counts, and the unified levy formula: `docs/FINDINGS_assessment_classes.md`.

### Residential-revenue decomposition (added 2026-07-16)

`apply_tax_rates.py` also emits **`res_levy`** — the subset of each parcel's levy
billed on **`RESIDENTIAL` + `OTHER RESIDENTIAL`** class slices (all housing:
houses/condos <4 units *and* 4+ unit apartment buildings; split-class parcels
contribute only their residential slice). **`MA DERELICT RESIDENTIAL` is
excluded** — the city deliberately bills it at the punitive Non Residential
rate, so its dollars are non-residential-rate dollars. Flows: `res_levy` →
`total_res_revenue` (aggregate) → **`res_revenue_per_acre`** /
**`res_revenue_per_lot_acre`** (slim GeoJSON; the lot variant inherits the
LOW_PARCEL_FRAC suppression). No share column ships — the client derives the
residential share as `res_revenue_per_acre / revenue_per_acre` (identical
denominators cancel). Real-data anchors (2025 roll): residential-class =
**52.6% of the citywide levy**; hood median share ~75%, DOWNTOWN ~16%; ground
p97.5 ≈ $28.5k/acre (web clamp $30k). Distinct from `is_residential`
(§ Residential split below), which is a *zoned-area* display flag, not dollars.

⚠️ **Every grid column described below ships at BOTH resolutions**
(2026-09-01): `value_grid.json` at 100 m (the served default) and
`value_grid_50.json` at 50 m, exported from the same frame by the same call,
so the schemas are identical by construction and the levy reconciles across
both ($2.7842B each). Raw sizes quoted in these subsections are the **100 m**
file's; the 50 m one is ~2.7x larger. ⚠️ Cell-grain STATISTICS quoted anywhere
in this file are resolution-dependent — re-measure rather than carrying a
percentage between the two.

**Glass grid variant (added 2026-07-17):** `export_value_grid.py` rolls the
same `res_levy` into the grid cells — payload columns
**`res_revenue_per_acre`** / **`res_revenue_per_lot_acre`** appended after the
existing six (`value_grid.json` ~1.76 → ~2.1 MB raw; Pages gzips). A cell with
assessed property but no residential-class levy reads a **real 0**, not null
(distinct from "no cell" = no property); lot slots stay null where no eligible
lot acres, exactly like value/revenue. ~79% of cells have res > 0; res ≤ rev
per cell (±$1 whole-dollar rounding). Older files lack the columns and the
Glass Residential $ metric falls back to hood prisms (web column guard).

### Non-residential decomposition (added 2026-07-18 — SPEC_industrial.md A1)

`apply_tax_rates.py` also emits **`nonres_levy`** — the subset of each parcel's
levy billed **at the Non Residential rate**: `COMMERCIAL` + `MA DERELICT
RESIDENTIAL` + `DESIGNATED IND PROPERTIES` slices (`NONRES_RATE_LABELS`,
derived from the label→rate-class map so a future non-res label can't be
missed). The complement of `res_levy` by rate class; farmland (its own rate
class, 509 parcels) is the only slice in neither subset, so the identity
**`levy == res_levy + nonres_levy + farmland slices`** holds exactly (tested).
Flows mirror res: `nonres_levy` → `total_nonres_revenue` →
**`nonres_revenue_per_acre`** / **`nonres_revenue_per_lot_acre`** (slim
GeoJSON, LOW_PARCEL_FRAC suppression inherited) and into the grid cells
(payload columns appended LAST, after `median_year_built`; real-0/null
conventions identical to res; `value_grid.json` ~2.28 → ~2.50 MB raw). NOTE
there is **no industrial-vs-commercial split in the roll** — `COMMERCIAL`
covers all non-res (§ 2) — so this is the honest class-complete cut; an
industrial-only cut would need a zoning join. Real-data anchors (2025 roll):
non-res-rate = **47.4% of the citywide levy** ($1.281B of $2.704B; farmland
residual ~$532K); 34% of grid cells have nonres > 0; hood ground p97.5 ≈
$48.4k/acre (web clamp $50k). Web: fourth Money metric ("Non-res $"),
column-guarded like Residential $.

**Stock-age grid column (added 2026-07-17):** `export_value_grid.py` also
rolls `year_built` (property-info, § 2) into **`median_year_built`** per 100 m
cell — appended LAST in the payload columns; whole-year ints. Median over
ROWS (unit-weighted), which makes the multi-unit duplication regimes moot: a
tower repeating one year on every unit row medians to that year, no dedupe
machinery. A cell where **no property has a known year carries `null`, never
0** — age has no meaningful zero ("year 0" would be a lie; contrast
`res_levy`'s real $0). Consumed by the **Development view's Spikes picker**
("Year built" — height + colour linear in year, recency bright), NOT by
Glass; it rides in this file because the age layer needs the whole-roll cell
population, which `dev_grid.json` (permit cells only) doesn't have. Older
files lack the column and the picker stays hidden.

**Institutional-share grid column (added 2026-08-19):** `export_value_grid.py`
also rolls **`inst_frac`** — the share of a cell's levy sitting on
**institutionally-zoned** land — appended LAST in the payload columns. Source
is `revenue_by_zone`'s per-property zoning category, which used to be an
internal step and is now `property_zone_categories`; `main.py` computes it
**once** and attaches `inst_levy` to the assessment frame, so the hood
`rev_frac_inst` and the cell `inst_frac` come from the SAME point-in-polygon
pass and cannot drift. ⚠️ **A SHARE, not a per-acre column, and there is
deliberately no `_lot` sibling** — which land is institutional is a fact about
the land, so the one fraction serves both denominators, exactly as
`rev_frac_inst` already does at hood level. A cell with **no levy to
apportion carries `null`, never 0** (same rule as `res_levy`'s real-$0
contrast: "nothing to apportion" is not "0% institutional"). Rounded to 4
decimals — a display gate, not an accounting figure; ⚠️ that rounding is
load-bearing at the top end, where a 99.95% cell keeps a real (invisible)
levied residual and only an **exactly 1.0** cell collapses its base to zero.
Real-data anchors (**the shipped 2026-08-19 refresh**, 34,666 cells): citywide
institutional share of levy **4.8%**; **623 cells (1.8%) at or above the 0.25
display threshold, carrying 4.9% of city levy**; of the 714 cells above 10%,
**467 are above 99%** — the distribution is bimodal, which is why the Glass band
needs only one threshold where the hood treatment needed two. (The design was
measured on a local 2026-08-09 roll giving 624 of 34,671; ⚠️ **the set moves
with the roll**, so re-measure rather than citing these as fixed.) Flagged cells are
lower on average (median $9,261/acre vs $18,127) but heavier at the top (p90
$97,610 vs $53,673), and **18 of the city's top 100 cells by $/acre are
flagged**, the tallest at **$5.66M/acre, 100% institutional**. Consumed by the
**Glass view's uncertainty bands** (revenue cuts only). Older files lack the
column and the bands simply do not draw.

---

## 5. Zoning Bylaw Geographical Data (land-use layer, added 2026-06-29)

**Source:** Edmonton Open Data — dataset ID `fixa-tstc` ("Zoning Bylaw Geographical Data")
**Download URL:** `https://data.edmonton.ca/resource/fixa-tstc.geojson?$limit=20000`
**Download:** `scripts/download_data.py` (fetches this alongside assessment + boundaries)
**Format:** GeoJSON, ~9.2 MB
**Features:** 11,510 zoning polygons (MultiPolygon)
**CRS:** CRS84 / EPSG:4326 — reproject to EPSG:3400 before any overlay/area
**Vintage:** the **2024 Zoning Bylaw** (new codes, e.g. `RSF` = "Small Scale Flex
Residential"). Assessment is 2025 — close enough; zoning is stable. Record the
download date / `date_ext` for provenance.

**Why:** neighbourhood-level aggregation needs explicit categorization of
non-developable land (River Valley, parks, undeveloped) that parcel-level analysis
handles implicitly. Overlaid on neighbourhood boundaries → land-use composition %
per neighbourhood → drives the colour-scale set-aside. See `SPEC_revenue.md`
(Update 2026-06-29) and `FINDINGS_revenue_scale.md`.

### Columns (confirmed 2026-06-30)
| Column | Notes |
|--------|-------|
| `zoning` | zone code, e.g. `RSF`, `A`, `RM h16` — height/overlay suffixes appended; parse the **first token** for the base code |
| `description` | human-readable, e.g. "River Valley", "Small Scale Flex Residential" |
| `url` | link to the bylaw page. **The path encodes the authoritative bylaw section** — `…/part-2-…/residential-zones/…`, `…/industrial-zones/…`, `…/open-space-and-urban-services-zones/…`, `…/agricultural-zones/…`, plus `…-special-area` groups. Use as an independent **cross-check** when building the code→category dict (see quirks), NOT as the category itself (groups are mixed — see below) |
| `dc2_sub_area` | sub-area for `DC2` site-specific zones |
| `date_ext` | extract timestamp (e.g. `2026-06-29 02:07:03`) — record for provenance |
| `id`, `agreement_no` | record identifiers |
| `geometry` | polygon (Socrata source field `geometry_multipolygon`; geopandas reads it as `geometry`) |

### Known Quirks
- **Geometry needs cleaning before overlay.** Raw polygons are invalid/mixed-dimension
  → geopandas `overlay` raises `GEOSException`. Fix: `buffer(0)`, drop empty + keep
  only Polygon/MultiPolygon parts.
- **Do NOT categorize by keyword/prefix.** "Energy & Technology **Park**" is industrial,
  "Century **Park**" is a TOD redevelopment — the word "Park" ≠ green park. The `A*`
  codes are mostly River Valley special areas (Hawrelak, Muttart) but `AED` =
  Arena/Entertainment District (downtown), `ALA` = Ambleside apartments. Use an
  **explicit `code → category` dictionary** (exactly **95 base codes** confirmed
  2026-06-30; `description` + `url` make each obvious). Lives in `src/load_zoning.py`.
- **`url` cross-check (confirmed 2026-06-30).** The `url` path's bylaw section is a
  useful *verification* signal but is NOT a drop-in category — groups mix set-aside and
  developed codes. The `open-space-and-urban-services-zones` group is the clearest case:
  it contains set-aside `A`/`NA`/`PS`/`PSN` **and** developed infrastructure `PU` (Public
  Utility), `UF` (Urban Facilities), `UI` (Urban Institution), `AJ` (Alternative
  Jurisdiction). Categorize at the code level; use `url` only to catch dict errors (e.g.
  it correctly resolves the `A*` trap: `AED`→`downtown-special-area`, `ALA`/`AUVC`→
  `ambleside-special-area`, not river valley).
- **Direct Control zones (`DC`, `DC1`, `DC2`) — confirmed 2026-06-30.** ~1,081 rows are
  site-specific / special-area zones with no standard `/part-N/` bylaw section in `url`
  (`DC*`, plus named zones like Blatchford, Century Park, River Crossing). **Rule:**
  `DC`/`DC1`/`DC2` default to **developed** (stay on scale — conservative, won't wrongly
  hide land). Named-natural special-area codes (`NSRVES`, `A7` Hawrelak, etc.) are caught
  by their own explicit dict entry, not by the `DC` default.
- **`url = "legacy"` sentinel (confirmed 2026-07-07).** 44 polygons (611 ha) carry the
  literal string `legacy` in `url` instead of a bylaw-page path — pre-2024-Bylaw zones
  (mostly bare `DC`, some special-area) never migrated to the per-provision page system.
  There is **no page to scrape** for these, and the bare-`DC` ones also lack an
  `agreement_no`, so they are unclassifiable from this dataset alone (distinct from the
  ~19 unpublished provision pages that 403). The DC-use pipeline (`ANALYSIS_BACKLOG` item
  3) rolls them up as `frac_dc_unknown`; the largest single one (id `173291`, 50 ha) is
  West Edmonton Mall, geometrically coincident with the migrated `dc2-1198` polygon.
- **Set-aside categories:** never = River Valley (`A`,`NA`)/Parks (`PS`,`PSN`); not-yet
  = Future (`FD`)/rural (`AG`,`RR`)/industrial reserve (`EET*`). Institutional
  (`UI`,`UF`,`AJ`,`PU`) is a proxy for where exempt-roll understatement lives.
- **Residential split (added 2026-07-01, for the residential-only lens).** The developed
  bucket is split by each code's `description` into `res` (primary permitted use is
  housing — the `RS*`/`RM`/`RL`/`HDR`/`RMU` standard zones + special-area row-housing /
  apartment / low-density codes, e.g. `GRH`, `BLMR`, `SRH`, `CCLD`) and the
  non-residential group. `is_residential` = `frac_residential` ≥ **0.50** of *zoned*
  area (a display filter, **orthogonal to** `is_set_aside` — the two can't both be
  true since fractions sum to 1). Per-code assignments live in `src/load_zoning.py`.
- **Non-residential split (added 2026-07-03, for the use-mix view).** The old `nonres`
  bucket is split four ways: `com` (commercial/retail/entertainment, 14 codes),
  `ind` (industrial/warehousing/business employment, 7), `mix` (mixed use, 14), and
  `dc` (Direct Control — bespoke per-site bylaws, no single use claimable; 24% of
  nonres area so it can't honestly fold into another bucket). **Names mislead —
  ambiguous codes were resolved from the bylaw page's purpose statement (the `url`
  field):** `UW` "Urban Warehouse" is a downtown *mixed-use* zone, not warehousing;
  `BE` "Business Employment" sits in the bylaw's *industrial-zones* part; `HA`
  Heritage Area and `MMS` Marquis Main Street are mixed (ground-floor retail +
  res/office above); `MED`/`AED` entertainment districts are commercial. Unknown
  codes now default to `other` (on scale, claimed as no specific use, flagged
  loudly) instead of `nonres`. `frac_other` = 0 on current data (all 95 codes
  mapped). ⚠️ **There is no aggregate non-residential column.** `frac_nonres`
  (com+ind+mix+dc+other) was removed 2026-08-31 — nothing consumed it and it
  never reached the served GeoJSON, and it was the one place unclassified land
  was asserted as a non-residential use. The monthly digest reports a non-zero
  `frac_other` (`docs/RUNBOOK.md` §0) since a new bylaw code only WARNS.
- **Refresh requirement:** re-pull each pipeline cycle so developing land (rezoned
  FD/AG → residential) graduates off the set-aside list automatically.

---

## 6. Road Network (road supply layer, added 2026-07-01)

**Source:** Edmonton Open Data — dataset ID `9j8t-zm52` ("Road Network")
**Download URL:** `https://data.edmonton.ca/resource/9j8t-zm52.geojson?$limit=100000`
**Download:** `scripts/download_data.py` → `data/raw/roads.geojson` (gitignored)
**Format:** GeoJSON, ~62 MB — centreline **LineStrings**, no surface polygons
**Features:** 53,720 segments (confirmed vs `count(*)` 2026-07-01)
**CRS:** EPSG:4326 — reproject to EPSG:3400 before any length calculation

**Why:** the services lens (`docs/SPEC_services.md`) — city-maintained road
length per neighbourhood, the first cost-side metric. Consumed by
`src/load_roads.py`; the shipped metric is **collector + local metres per
boundary acre** (`road_m_per_acre`).

### Key columns
| Column | Notes |
|---|---|
| `centerline_type` | `Road` 39,515 / `Alley` 12,088 / `Railway` 2,117 — **filter to `Road`** |
| `responsible_party_description` | City of Edmonton 49,794; Province 1,164 (ring road); CN/CP rail; Private 566; neighbouring municipalities — **filter to `City of Edmonton`** |
| `functional_class_code` | closed enumeration, 15 values (4 Arterial classes, Collector/Local by adjoining land use, `Local-ParkWay`, `Local-Private`, `Alley-Residential`) — explicit dict `CLASS_GROUP` in `load_roads.py` |
| `geometry` | LineString centrelines |

### Known Quirks
- **Null `functional_class_code` = Alley + Railway exactly** (14,205 = 12,088 +
  2,117, verified 2026-07-01). After the Road + City filters every row is
  classified — a null/unknown there means upstream drift (`load_roads` warns
  loudly and defaults to `local` so the length stays in the metric).
- **41 Road-type rows are functionally classed `Alley-Residential`** (all
  City-owned, 5.7 km). Excluded per the alleys-out decision — function
  governs, not `centerline_type` (SPEC_services.md).
- **`Local-Private` ≠ privately owned:** 73 of the 376 `Local-Private` rows are
  `responsible_party = City of Edmonton` and survive the ownership filter —
  kept as `local` (responsibility governs, not the name).
- **Arterials are computed but excluded from `road_m_total`** (shared
  infrastructure — SPEC_services.md; don't re-litigate). ~0.28% of filtered
  length falls outside all neighbourhood polygons (conservation guard reports
  it every run).
- **Vintage:** live feed like the others; no year semantics of its own (the
  network changes continuously, not per roll year). Refresh weekly with the
  other inputs.

## 7. Fire Response Events (fire lens, added 2026-07-06)

**Source:** Edmonton Open Data — dataset ID `7hsn-idqi` ("Fire Response: Current and Historical")
**Download URL:** `https://data.edmonton.ca/resource/7hsn-idqi.csv?$limit=2000000`
**Download:** `scripts/download_data.py` → `data/raw/fire_response.csv` (gitignored)
**Format:** CSV via the SODA resource endpoint (snake_case API headers)
**Rows:** 948,086 dispatched events, 2011–mid-2026 (pulled 2026-07-06); ~90k/yr in the 2023–2025 window — the long-run ~65k/yr average understates current volume
**Licence:** Open Government Licence – City of Edmonton

**Why:** the fire lens (`docs/SPEC_services.md` "Fire lens") — dispatched
emergency events per neighbourhood per year, the first *demand*-side
service. Consumed by `src/load_fire.py`; the shipped metric is
**`fire_events_per_acre`** (mean annual kept events over the pinned
`FIRE_YEARS` window ÷ boundary acres).

### Key columns (headers confirmed on the first real pull, 2026-07-06; counts from the Session-12 probe)
| Column | Notes |
|---|---|
| `dispatch_datetime` | **confirmed** — resolves as the first exact candidate in `DISPATCH_COLUMN_CANDIDATES` (the resolver + substring fallback + hard error stay as drift insurance). Only 186 of 948k rows unparseable. |
| `event_close_datetime` + `event_duration_mins` | dispatch→CLOSE, i.e. incident length. **There is NO on-scene-arrival timestamp anywhere** — a true response-time metric is NOT buildable from this data (confirmed against the full column list) |
| `event_type_group` | **two-letter CODES** (MD, AL, TA, OF, CA, FR, HZ, TM…), NOT the long names the Session-12 probe showed — those live in `event_description`. ~1k rows over 15 years are code-only with a null description (DR 762, `86` 165, FP 83, HO 47, `88` 1) — kept under the bare code. |
| `event_description` | the long-name vocabulary (one-to-one with the codes): MEDICAL 57% (536k), ALARMS 144k, MOTOR VEHICLE INCIDENT 65k, OUTSIDE FIRE 48k, CITIZEN ASSIST 36k, FIRE 24k, HAZARDOUS MATERIALS 20k, OTHER 10k, RESCUE 7k, VEHICLE FIRE 5k, MESS 137, PERMIT-BURNING OR OTHER 10, + operational noise (TRAINING/MAINTENANCE 18k, COMMUNITY EVENT 2.5k, PRE-INCIDENT PLANNING 515, 31k both-null). **`load_fire` filters on this column** (bare-code fallback). |
| `response_code` | dispatch-priority letters (D 446k, AL, NF, C, B, SR, E…) — **undecoded; never filter on it** |
| `neighbourhood_name` | **pre-joined on ~99% of rows** (8,093 null over the full history) — the per-hood metric needs no spatial work |
| lat/long | present; unused by the lens (locked: no spatial fallback) |

### Known Quirks
- **The 57% MEDICAL share is the interpretive trap** — the metric is
  fire-department *demand*, mostly medical calls, not fires. Legend/blurb
  caveat by locked decision, never a filter.
- Live feed (current + historical); the metric window is pinned
  (`FIRE_YEARS` in `main.py`, last 3 FULL years) so weekly refreshes don't
  average in a partial year. Bump each January (blurb + legend years in
  `web/index.html` ride along).
- `load_fire` HARD-ERRORS if a window year has zero rows (wrong pin or
  upstream drift) and keeps-but-logs group vocabulary outside
  `KNOWN_GROUPS`. **The Session-12 probe read `event_description` values,
  not `event_type_group`** — the first real pull (2026-07-06) caught the
  original code filtering on the wrong column via exactly that unknown-
  vocabulary warning (the noise filter matched nothing, MEDICAL logged 0%).
- **Hood names lag the boundary file** — `FIRE_NAME_CORRECTIONS` in
  `src/load_fire.py` layers fire-specific fixes on top of the shared
  `NAME_CORRECTIONS`: `OLIVER → WÎHKWÊNTÔWIN` (the fire CSV still uses the
  old name; 1,476 events/yr — 5th-highest hood, displayed as 0 until the
  first production refresh caught it), plus `KESWICK/MCCONACHIE/WINDERMERE
  AREA` → their boundary hoods. Kept out of the shared dict because the
  assessment side's OLIVER straggler is deliberately unmapped (see "Name
  Matching"). Legitimately unmatched leftovers (~18 events/yr, flagged at
  the join): COREYLAND, EDMONTON MUNICIPAL AIRPORT, UNKNOWN, RURAL SOUTH
  EAST — no boundary polygon exists for them.

## 8. Fire Stations (fire lens context dots, added 2026-07-06)

**Source:** Edmonton Open Data — dataset ID `b4y7-zhnz` ("Fire Stations")
**Download URL:** `https://data.edmonton.ca/resource/b4y7-zhnz.csv?$limit=500`
**Download:** `scripts/download_data.py` → `data/raw/fire_stations.csv` (gitignored)
**Rows:** 31 — station number, address, lat/long point ONLY (no
staffing/coverage/response data; probed 2026-07-05).
Exported by `load_fire.export_fire_stations_web` to
`web/data/fire_stations.json` (committed) as `{"stations": [[lon, lat,
label], …]}` — context dots in the Services view, not a coverage claim.
Column resolution uses the same explicit-candidates rule as §7.

## 9. ETS GTFS Static Feed (transit lens, added 2026-07-11)

**Source:** Edmonton Open Data — the GTFS static feed published as FIVE
individual Socrata tables (the "zipped files" dataset `urjq-fvmq` is an
href-only landing page, no machine-readable blob; the `yiem-dcbw` "GTFS
Downloads" dataset is download-count *stats*, not the feed):

| Table | Dataset | Rows (2026-07-11) | Downloaded to |
|---|---|---|---|
| Stops | `4vt2-8zrq` | 6,882 | `data/raw/gtfs_stops.csv` |
| Routes | `d577-xky7` | 238 | `data/raw/gtfs_routes.csv` |
| Trips | `ctwr-tvrd` | 56,812 | `data/raw/gtfs_trips.csv` |
| Stop Times | `greh-g7ac` | 1,744,051 | `data/raw/gtfs_stop_times.csv` |
| Calendar Dates | `f2sy-bth7` | 9,248 | `data/raw/gtfs_calendar_dates.csv` |
| LRT Routes | `rpjw-4jft` | 4 | `data/raw/lrt_routes.geojson` |

**Download:** `scripts/download_data.py` (all gitignored). Trips and
stop_times use `$select` for only the keyed columns — trips otherwise
carries a per-trip `geometry_line` that dominates the file; stop_times
needs only `trip_id,stop_id` (31.6 MB slimmed). `$select` doesn't change
the row count, so both truncation guards still apply. LRT Routes is a
small GeoJSON (4 features), a separate 6th input feeding only the track-line
context layer — the metric runs without it.
**Why:** the transit lens (`docs/SPEC_services.md` "Transit lens") —
mean-weekday scheduled stop-events per neighbourhood. Consumed by
`src/load_transit.py`; the shipped metric is **`transit_dep_per_acre`**.

### Key columns
| Column | Notes |
|---|---|
| stops: `stop_id`, `stop_lat`/`stop_lon`, `location_type` | types: 0 stop/platform (6,673), 1 station (58 — LRT stations + transit centres, the context-dot export), 2 entrance (109), 3 node (42). **The feed includes REGIONAL stops** (Spruce Grove, St. Albert park-and-rides etc.) — they fall outside every hood polygon and land in the reported unassigned bucket (~5.8% of stop-events, 2026-07-11). |
| routes: `route_id`, `route_type_descr` | "Bus" 235 / "Tram, Streetcar, Light rail" 3 — the explicit `ROUTE_MODE` dict in `load_transit.py`; unknown values kept as `other`, logged. |
| trips: `trip_id`, `route_id`, `service_id` | plain join keys. |
| stop_times: `trip_id`, `stop_id` | one row = one scheduled stop-event; only these two columns downloaded. |
| calendar_dates: `service_id`, `date`, `exception_type` | **calendar-dates-only feed** — every active service day is an `exception_type` 1 row (no calendar.txt); type-2 removals honoured generically if they ever appear. |
| lrt_routes: `lrt_route_id`, `lrt_route_name`, `lrt_route` (multiline) | **Not part of the metric — a map context layer only.** Four route multilines: 021R Capital, 022R Metro, 023R Valley, and `HER` (High Level Bridge heritage streetcar). `export_transit_lines_web` **drops HER** (`EXCLUDED_LRT_ROUTE_IDS` — volunteer-run, not ETS LRT service, absent from the GTFS routes counted) and flattens the rest to `web/data/lrt_lines.json` (343 segments, 2026-07-11). |

### Known Quirks
- **The feed is a snapshot of the CURRENT signup only** — probed window
  2026-06-18 → 2026-08-29 (the SUMMER schedule, the seasonal low).
  Weekly refreshes will step the metric at signup boundaries. No roll-year
  semantics; provenance = download date + the window logged every load.
- **No ridership anywhere:** the portal's `sfwk-p9kr`/`77dh-qrp7` (on-time
  %) and `wh9u-ef4x` (revenue vehicle hours) are citywide-monthly only
  (probed 2026-07-11) — no stop/route/neighbourhood usage exists. The lens
  is scheduled supply and must be labelled as such.
- **On-demand transit zones are not in the GTFS** (238 fixed routes only) —
  invisible to the metric; documented limitation for the on-demand fringe.
- ~253 service_ids (~20.6k trips, 2026-07-11) are weekend/holiday-only —
  they weigh 0 in the weekday metric by construction, logged not dropped.

## 10. Building Permits (development & infill lens A, added 2026-07-12)

**Source:** Edmonton Open Data — dataset ID `24uj-dj8v` ("General Building Permits")
**Download URL:** `https://data.edmonton.ca/resource/24uj-dj8v.csv?$select=year,issue_date,work_type,building_type,units_added,neighbourhood,latitude,longitude&$limit=1000000`
*(latitude/longitude added 2026-07-15 for the 100 m detail grid —
`load_permits.export_dev_grid` → `web/data/dev_grid.json`; see the
geocoding-lag quirk below.)*
**Download:** `scripts/download_data.py` → `data/raw/building_permits.csv` (gitignored)
**Format:** CSV via the SODA resource endpoint, **slim `$select`** — only the 6
filter/join/numerator columns (the full schema is 34 cols; we skip
`construction_value`, `geometry_point`, `zoning`, `floor_area`, etc.). `$select`
does not change the row count, so both truncation guards still apply.
**Rows:** 243,371 permits, `issue_date` 2009-01-05 → present (pulled 2026-07-12)
**Licence:** Open Government Licence – City of Edmonton

**Why:** the Development & Infill lens A (`docs/SPEC_development.md`) — new
dwelling units built per neighbourhood, the project's first *change/flow* metric
(everything else describes the roll as it stands today). Consumed by
`src/load_permits.py`; the default metric is **`new_units_per_acre`** (Σ
`units_added` on new-construction ∩ residential permits over the pinned
`PERMIT_YEARS` window ÷ boundary acres). A second metric **`new_permits_per_acre`**
(permit count ÷ boundary acres, added 2026-07-13) drives the web view's
units/permits sub-metric picker — project density vs dwelling supply.
`new_dwelling_units` (window total) + `new_dwelling_permits` (count) ride into the
slim file for the tooltip.

**Window toggle (added 2026-07-13).** A second, shorter pinned window
(`PERMIT_YEARS_RECENT` in `main.py` = the last 3 full years, 2023–2025) is
aggregated by a second `load_permits` call and emits `_3yr`-suffixed twins of all
four columns (`new_units_per_acre_3yr`, `new_permits_per_acre_3yr`,
`new_dwelling_units_3yr`, `new_dwelling_permits_3yr`). The base (5yr, 2021–2025)
columns stay **unsuffixed** for backward-compat with the live geojson + web
gates. The web `#devwindow` picker switches 5yr ↔ 3yr; it's gated on the `_3yr`
columns being present (older data files show the 5yr base only). Both windows are
pinned + drift-guarded and bump together each January.

**Long "since 2009" window (added 2026-07-21).** A third window `PERMIT_YEARS_LONG`
(`main.py`) emits `_long`-suffixed twins of all four residential columns (plus
`ind_permits_per_acre_long`) — the cumulative **"density added over the era"** cut
that reproduces the inspiration lens's 2009–2023 "homes added" map. Unlike the two
sliding windows it is **anchored**: the start is fixed at `PERMIT_START_YEAR = 2009`
(the permit record's first year, DATA.md above) and only the end advances, so it is
DERIVED as `range(2009, PERMIT_YEARS[-1] + 1)` — the annual January bump of
`PERMIT_YEARS` extends it automatically, no separate pin to roll. Citywide it sums
~160k units (2009–2025) vs ~60k (5yr) / ~39k (3yr). The web `#devwindow` gains a
**"Since 2009"** button (gated on the `_long` columns) — a **first-class window**:
it drives both the hood choropleth AND its own 100 m detail grid (`export_dev_grid`
emits `units_long`/`permits_long` cells + `coverage["long"]`, added 2026-07-22).
The geocoding lag is on the NEWEST permits, not the oldest — **2009–2023 sit at
95–98% geocoded, 2025 at ~72%** — so the long window is the *best*-covered of the
three grids (84% of units on the grid, vs 79% / 71% for 5yr / 3yr). An earlier cut
made it choropleth-only on the mistaken belief that early-year geocoding was sparse;
the data disproved it (`.venv/bin/python` count by year).

### Key columns (live vocab confirmed 2026-07-12)
| Column | Notes |
|---|---|
| `units_added` | dwelling-unit numerator. A single apartment permit adds many (GRIESBACH: 2,274 units from 349 permits); a single-detached permit adds 1. Non-numeric → 0 units, kept as a permit, warned. |
| `work_type` | **new-construction filter.** `NEW_WORK_TYPES` = `(01) New` + `(01) Building - New` + `(01) New House`. Suite-adds/conversions (`(07)`/`(08)`/`(09)`) add dwellings but are INFILL densification — excluded from Lens A (they're the Lens B story). ~41k of ~78k in-window rows are null/blank `work_type` — excluded, count reported. **Verified (S48 Fable audit, 2026-07-13): all 40,956 in-window (2021–2025) null-`work_type` rows carry `units_added` = 0 (sum exactly 0), so the exclusion loses ZERO dwelling units** — they are 0-unit sub-permit-like rows (33,669 are `building_type` = Single Detached House), NOT old miscoded new-construction. (The earlier "most predate consistent coding" rationale was wrong.) |
| `building_type` | **residential-dwelling filter.** 71 distinct values with many spelling variants of each category — `Apartments (310)`/`Apartment (310)`/`Apartment Condos (315)`; `Row House (330)`/`Row Houses (330)`; `Semi Detached House` (no code); `Backyard House (110)` (a garden suite, counted). All enumerated in `RESIDENTIAL_BUILDING_TYPES`, never prefix-matched. Garages, commercial, `Mixed Use (522)` excluded. **Also `INDUSTRIAL_BUILDING_TYPES`** (400-series: Animal & Plant Services 410, Manufacturing 430, Maintenance/Hangars 450, Warehouses 460, Communication 470, Utility 480) drives the separate industrial-permit-velocity count (§ below) — enumerated by FULL STRING because codes duplicate across unrelated types (`Parkade (490)` is NOT industrial). ⚠️ **`Engineering (490)` and `Transportation Terminals (440)` were REMOVED 2026-08-18** — measured on `job_description`, 490 is **95% parkades** and 440 is **100% LRT/transit**, and they were putting a $91.2M underground-parkade spike on DOWNTOWN and flagging 7 residential hoods as industrial. They remain in `KNOWN_BUILDING_TYPES` via `NON_INDUSTRIAL_400_SERIES`. ⚠️ **Full-string enumeration did NOT prevent this** — the City files underground parkades under BOTH `Parkade (490)` and `Engineering (490)`, so excluding the obvious string left the same buildings in under the other. |
| `year` | integer permit year — drives the pinned window filter (vs parsing `issue_date`). |
| `neighbourhood` | **UPPERCASE, matches `neighbourhood_name`** — the join key. |
| `construction_value` | **added to the `$select` 2026-08-18** — the industrial detail grid's height (§ below). Documented by the City as *"Estimated value of construction work"*: a **declared estimate at permit application**, not audited spend, never reconciled. The permit fee is derived from it (an incentive to declare low) and **land is excluded**. 78% of values end in `000`, 26% in `00000` — round-number estimating, not accounting. Populated on **99.6%** of industrial new-construction rows (284/285, 5yr). ⚠️ **Nominal** — must be deflated before summing across years (§ below). ⚠️ **13 industrial permits declare exactly $0**, 32 ≤$1,000, 118 ≤$10,000; on a dollar-driven encoding those disappear unless carried by a count. |
| `floor_area` | **square footage** (per the City's field description — this resolves the m² ambiguity: median industrial permit is 3,843 sq ft ≈ 19 m square, comfortably inside a 100 m cell; p95 is 121,214 sq ft, which does span cells). ⚠️ **NOT fetched and NOT usable as an intensity measure** — populated on only **51%** of industrial new-construction permits (vs 99% residential), against `construction_value`'s 99.6%. Considered and rejected 2026-08-18; don't reach for it again without re-measuring coverage. |

### Known Quirks
- **`count(*)` aliases as `count_1`, not `count`** on this dataset (a Socrata
  inconsistency — roads returns `count`). `download_data.server_count` was
  hardened 2026-07-12 to read the sole count column by value, so the truncation
  cross-check works everywhere.
- **"Same data, different cuts":** seven other portal datasets are saved
  filters/map-views over the same two source tables (building permits + dev
  permits) — proven by identical `rowsUpdatedAt`. We pull `24uj-dj8v` and filter
  ourselves; **ignore `itki-s8y9`/`jsf3-5dv2`/`537d-t4az`/`uep4-4w4g`/`ramb-ihnk`**
  (building) and `66ut-y7w2` (dev). See `docs/SPEC_development.md` "Data".
- **Activity ≠ money path** — the name join is **warn-not-fail** (unlike the
  assessment money guard, `scripts/check_unmatched_names.py`): an unmatched
  permit hood is a blank hood, not a silent dollar loss. `CHAPPELLE AREA →
  CHAPPELLE` etc. resolve via the shared `NAME_CORRECTIONS`; the only leftover
  straggler is `GLENORA, ROSSLYN` (1 unit, immaterial).
- `load_permits` HARD-ERRORS if a window year has zero permits (stale
  `PERMIT_YEARS` pin or upstream drift), and keeps-but-warns any `work_type` /
  `building_type` value outside the `KNOWN_*` vocab (it might be a new
  residential variant to count) — same explicit-dictionary discipline as
  `load_fire`. Bump **both** `PERMIT_YEARS` and `PERMIT_YEARS_RECENT` each January.
- **`occupancy_granted_date`** exists in the full schema (a completed-builds
  variant) but is only populated for residential finalized ≥ Jan 1 2022 /
  non-residential ≥ Jan 1 2024 — useless for historical totals, not fetched.
- **Geocoding lags on the newest permits** (`latitude`/`longitude`, probed
  2026-07-14): among in-window new-construction rows, nulls are ~1–2%/yr for
  2021–2023 but 994 permits in 2024 and 3,564 in 2025 — a lag, not a
  structural hole (nearly all null-coord rows still carry `neighbourhood`, so
  hood aggregation is unaffected). The 100 m detail grid
  (`export_dev_grid`) therefore bins **geocoded permits only** — 5yr window at
  build time: 47,125 of 59,697 units (~21% not yet mapped; 3yr ~29%) — and
  writes per-window `coverage` into `dev_grid.json` so the web blurb
  discloses the live percentage. Never backfill with hood centroids. Expect
  coverage to improve as the city geocodes its backlog; the weekly regen
  picks that up automatically.

### Industrial permit velocity (SPEC_industrial.md A3, added 2026-07-18)

The same `24uj-dj8v` permits, cut for industrial construction: `load_permits`
counts new-construction (`NEW_WORK_TYPES`) ∩ `INDUSTRIAL_BUILDING_TYPES`
(400-series, above) permits per hood over the same pinned windows, emitting
**`ind_permits`** (count) → `join_and_calculate` **`ind_permits_per_acre`**
(+ the `_3yr` pair), in `SLIM_COLUMNS`. **Count only** — `units_added` is
meaningless for industrial (no dwellings), and `construction_value` is
reserved (consistent with the Lens C reservation). Aggregated separately from
the residential rollup and outer-merged, so a hood with one kind of activity
but not the other carries a true 0 in the missing column. Real data (2021–2025
window, build time): **283 new industrial permits across 117 hoods** (3yr: 189
across 85); top hoods are the industrial areas (SOUTHEAST INDUSTRIAL, MISTATIM,
CLOVER BAR, WINTERBURN, EASTGATE BUSINESS PARK); per-acre is small (p97.5 ≈
0.015/acre). Web: third `#devmetric` option "Industrial" — a Development-view
choropleth (not an Infill activity — the roll has no industrial-vs-commercial
split anyway, § 2), and **since 2026-08-18 also a 100 m detail grid**
(below). **NOTE — no
industrial-vs-commercial split exists in the assessment roll** (§ 2), so this
permit-based cut is the ONLY industrial-specific spatial signal the project
has; it is construction activity, not assessment base.

#### The industrial 100 m detail grid, and its deflator (added 2026-08-18)

`export_dev_grid` emits `ind_cv` / `ind_n` per window alongside the
residential `units` / `permits`. **Height is deflated construction value, not
permit count** — measured first: **89% of 5yr industrial cells hold exactly
one permit**, so count is a dot map, and **enlarging the cell does not fix it**
(100 m → 400 m is a 16× area increase that removes 19 of 184 cells). Dollars
spread the same cells over 164×.

⚠️ **Nominal dollars encode inflation as development.** Deflated to **constant
2025 dollars** via `data/construction_price_index.json`, built by
`scripts/fetch_construction_price_index.py` from **StatCan table
18-10-0289-01** (GEO `Edmonton, Alberta`, Type of building `Industrial
buildings [62211]`, Division `Division composite`, `Index, 2023=100`, vector
`v1617916332`). Factors: **2009 → 1.717×**, 2021 → 1.325×, 2025 → 1.000×. The
permits' own warehouse $/sqft corroborates independently (1.92× 2009→2025).
A permit year with no deflator **hard-fails**.

⚠️ **A manual, reviewed input** — mill-rates / FIR-debt pattern (§ 4, § 11).
**NOT on the weekly refresh**: a price index that moved silently would restate
every historical spike on the map at once. Re-run by hand when a year
completes, eyeball the diff, commit.

⚠️ **Two predecessor tables are ARCHIVED and must not be pinned**:
18-10-0135 stops at **2022-Q2**, 18-10-0276 at **2024-Q2**. Both still
download and still answer queries — they simply stop — so a stale pin fails
**silently**. The fetcher checks `archiveStatusEn` and warns; the successor is
findable via the WDS `getAllCubesListLite` endpoint.

⚠️ **Zero-dollar permits are carried by `ind_n`, not dropped.** 12 of 1,281
industrial permits declare exactly $0; the client floors their cells to a
visible 6 m. The floor is deliberately small — dwelling units are QUANTISED
(0% of residential cells render under 5 m) while dollars are CONTINUOUS to
zero (39–44% of industrial cells do), and a 60 m floor flattened cells worth
up to $4.6M to the same height as $0.

## 11. Alberta FIR Debt Series (debt lens D5, added 2026-07-14)

**Source:** Alberta Municipal Affairs — Municipal Financial and Statistical
Data (FIR/SIR), `https://open.alberta.ca/opendata/municipal-financial-and-statistical-data`
**Fetch:** `scripts/fetch_fir_debt.py` → committed `data/fir_debt_series.json`
(12 KB). **Manual, reviewed input** (mill-rates pattern): NOT part of the weekly
refresh — re-run when a new financial year publishes (~annually, watch for it
alongside the January year-roll), eyeball the diff, commit. openpyxl/xlrd are
dev-only deps (`requirements.txt`, not `requirements-ci.txt`); the test module
skips itself on CI.
**Format:** one XLSX workbook per financial year, every Alberta municipality.
The debt schedule ("Schedule AA", 8 identical columns 2003–2025) carries FIR
item codes `05700` Debt Limit / `05710` Total Debt / `05720` Debt Service
Limit / `05730` Total Debt Service Costs.
**Extracted:** EDMONTON (code `0098`), ST. ALBERT (`0292`), STRATHCONA COUNTY
(`0302`) — the two peers the debt-lens brief benchmarks against — for
2003–2025 (23 years; one year further than the brief expected).
**Licence:** Open Government Licence – Alberta

**Why:** debt-lens ticket D5 (`docs/fable_brief_debt_lens.md` Component 2) —
the citywide debt context annotation (trend + peer benchmark, explicitly
non-spatial). The display/chart is a separate, undecided design step; this is
the data layer only.

### Format eras (all verified 2026-07-14)
| Years | Where | Debt sheet |
|---|---|---|
| 2017–2025 | standalone `YYYY_financial_year.xlsx` on the dataset page | `AA(1)-Debt` |
| 2009–2016 | inside `2009-2016-municipal_financial-data-and-statistics.zip` | `AA(1)-Debt` |
| 2004–2008 | inside `xlsx-2003-2008.zip`, per-schedule `YYYY/YYYY-AA-Debt Info.xlsx` | `Schedule AA` |
| 2003 | same zip, legacy `2003-EA-MR/GR Debt Info.xls` (xlrd) | `GR Debt Info` |

(A `xlsx-2002-1994.zip` also exists if the series is ever extended back.)

### Known Quirks
- **STRATHCONA COUNTY 2013 is reported in $000s** in the source workbook (debt
  limit `485,926` between real-dollar neighbours 473.9M/504.2M). The fetch
  script applies a documented ×1000 correction (`KNOWN_UNIT_CORRECTIONS`),
  records `unit_corrected: 1000` on that year's JSON record, and a
  neighbour-band sanity check (factor 5 vs adjacent years) hard-fails if a new
  unit slip ever appears.
- **The FIR "Debt Limit" is the MGA regulation limit** (Debt Limit Regulation
  255/2000 — 2× revenue for most municipalities; Edmonton/Calgary have their
  own), **NOT Edmonton's internal DMFP policy limits** (≤18% tax-supported /
  ≤21% total debt servicing) that the "69% of limit" headline in the debt-lens
  brief refers to. Don't conflate the two in any display. On FIR terms,
  Edmonton 2025 total debt = 59.3% of its MGA debt limit.
- **Anchor cross-checks** pin the extraction to independently published
  figures: Edmonton 2025 total debt $4,592,150,000 (the brief's "$4.6B"
  reported to Council 2026-03-17) and Strathcona County 2022 $133,070,148 (the
  brief's audited peer datapoint). A mismatch on re-fetch means the province
  restated data → human review (`--allow-anchor-drift` to accept).
- Edmonton's series is NOT monotonic — e.g. 2017 drops to $2.91B from $3.34B
  (2016) before climbing again; real amortization, not a data error (both
  years pass the neighbour band).

## 12. Off-Site Levy Fire-Hall Catchments (debt lens D0, added 2026-07-15)
Source: **Off-Site Levy Bylaw 19340**, `edmonton.ca/business_economy/off-site-levy-bylaw`
(laptop-reachable only). The 12 fire-hall levy catchments are the Component 1
spatial join key in the debt-lens brief.
- Raw artifacts in `data/raw/offsite_levy/`: `BL19340_offsite_levy_bylaw.pdf`,
  `ScheduleA_catchment_map.jpg` (the catchment map exhibit, bylaw p.7),
  `2026_approved_rates.pdf` (cost/area/rate table).
- **No GIS vector layer exists** — data.edmonton.ca (0 Socrata hits), ArcGIS Hub
  (Calgary layers only), and the bylaw page all lack one. Boundaries are
  published **only as the Schedule A raster**. Full investigation +
  neighbourhood-union feasibility (which catchments the 407-hood grid can/can't
  reproduce, with per-catchment area validation) in
  `docs/FINDINGS_offsite_levy_catchments.md`.
- **Derived product: `data/levy_catchments.geojson`** (10 features, committed) —
  each catchment approximated as a union of neighbourhoods via
  `scripts/build_levy_catchments.py` (manual reviewed input, like
  `fetch_fir_debt.py`; NOT in the weekly refresh). The editable `CATCHMENT_HOODS`
  table maps hoods to catchments read off Schedule A. The 12 bylaw catchments
  collapse to **10 units**: EETP + Northeast EETP and Horse Hill + Northeast
  Horse Hill are each merged (the far-greenfield grid is one giant hood per
  corner). Each feature carries the brief's levy attributes + a `union_ha` /
  `area_ratio` QA field + an `approximation` label. Tests:
  `tests/test_build_levy_catchments.py`.
### Known Quirks
- **Boundaries are advisory** — the bylaw states the City "may adjust and refine"
  catchment boundaries over time; the map footnote says "subject to change." Any
  derived polygon layer must be labelled "approximated to neighbourhood
  boundaries," not presented as authoritative.
- **`EDMONTON ENERGY AND TECHNOLOGY PARK` (one 5,334 ha hood) spans BOTH the EETP
  and Northeast EETP catchments** — the neighbourhood grid is too coarse in the
  far greenfield to separate them by union (see FINDINGS §3).

## 13. City Service Unit Costs (V2 cost-per-acre, added 2026-07-15)
`data/city_unit_costs.json` — MODELED unit costs for the V2 "city service cost
per acre" composite (`SPEC_utilities` decision 3). Manual reviewed input
(mill-rates pattern; NOT auto-fetched, NOT in the weekly refresh). Sourced on
Peter's laptop (edmonton.ca unreachable from the Oracle box). **Roads + fire
only** — never label the derived metric "total city cost".
- **Roadway = $50/m/yr** (O&M + renewal). Source: edmonton.ca "Development Impact
  on Infrastructure" — neighbourhood road $600k O&M + $1.9M renewal per km,
  annualized over a 50-yr life (Peter's call 2026-07-15); 3%-of-value rule
  cross-checks (~$45). Applies to the collector+local `road_m_per_acre` metres.
- **Fire = 2026 gross operating budget $276.706M** (net $273.598M, 1,361 FTE).
  Source: City of Edmonton 2026 Approved Operating Budget PDF, Fire Rescue
  Services line. The V2 fire term divides this by the pipeline's OWN citywide
  kept-event total (don't hardcode dispatches), so the unit cost's denominator
  matches the `fire_events_per_acre` numerator.
- ⚠️ **`cost_roads_life_per_acre` (2026-09-02) is the SAME $50/m/yr roads term
  published on its own**, so a roads-only lens can show a lifecycle figure
  without the fire allocation. It is **NESTED INSIDE `svc_cost_per_acre`**
  (= this + the fire term): subtracting the two is meaningful, **adding them
  double-counts roads**. It is also the **same metres as
  `cost_roads_ops_per_acre` on the other basis** (~10.8× apart) — never sum
  those either. Three road cost numbers now ship in one file and no two of them
  combine. Computed under its own `roads is not None` guard, so it survives a
  run with no fire data (which `svc_cost_per_acre`, being all-or-nothing, does
  not). Median $1,629/acre/yr vs $151 operating; 9 hoods where roads alone
  exceed the levy, vs 1 on the operating basis.
- ⚠️ **OPEN: the two non-capital road figures do not reconcile — but the gap is
  now mostly EXPLAINED (2026-09-05).** The lifecycle O&M half ($600,000/km ÷ 50
  yr = **$12/m/yr**) and the operating maintenance rate (**$4.635/m/yr**) both
  claim to be annual non-capital spend on neighbourhood roads and sit **2.6×
  apart**. ✅ **The cause is the maintenance half:** the City's published FY2017
  `Roadway Maintenance` program (§17, $65,671,000, budgeted separately from
  snow) is **$5,970/km — 4.65× the $1,285/km** the rate is built on;
  substituting closes 2.6× to **1.29×**, and correcting the vintage to **~1.1×**
  (1.06× on a FY2025 endpoint, 1.11× on FY2026 — ⚠️ **1.29× is the figure that
  needs no escalation assumption; prefer it**).
  ⚠️ **Value UNCHANGED and not naively swappable** — $5,970 is a citywide blend
  including arterials. ⚠️ **Split treatment to resolve: §16 retired this same
  $1,285/km as ~5× too low, while it remains the maintenance half in §13.**
  Full record: `docs/FINDINGS_roadway_maintenance_rate.md`. The operating blurb
  says outright it is the low end of a range. See also `docs/SPEC_services.md`
  "Roads cost — lifecycle".
- **Consumed (2026-07-15)** by `join_and_calculate.load_unit_costs` (validates
  loudly — a malformed hand edit fails the pipeline) → the `unit_costs` arg
  computes `svc_cost_per_acre` (in `SLIM_COLUMNS`). The per-event divisor is
  the fire frame's citywide sum PRE-join (unmatched fire hoods stay in the
  denominator). Composite requires BOTH the roads and fire lenses; either
  missing → warn + skip. `main.py --skip-service-cost` / `--unit-costs-json`.
- **Displayed (2026-07-16)** two ways (`web/index.html`): the Services view's
  "Service cost (roads+fire)" checkbox (SERVICES `servicecost`, sqrt colour on
  the shared `svc-plane`) AND the Ratio view's "Per service $" denominator
  (`revenue_per_acre / svc_cost_per_acre` — dimensionless coverage, log colour,
  RATIO_DENOMS `servicecost`). Both carry the caveats below; the ratio copy also
  states it reads ≫1 because the cost side is only two services (median ≈5.8×),
  NOT "pays its way". The column ships to the live GeoJSON on the first refresh
  after the metric PR #59 — until then both controls are column-guarded off.
### The OPERATING trio (added 2026-08-03, transportation lens Stage 2)
The same file also carries `roadway_ops`, `bikeway_ops` and `transit_ets`, on a
**strictly operating basis** — maintenance + snow clearing, **no capital**.
- **Roadway ops = $4.635/m/yr** ($1,285/km maintain + $3,350/km snow).
- **Bikeway ops = $20.278/m/yr** ($178/km maintain + $20,100/km snow) — a
  bikeway metre costs **4.4× a road metre** to operate: cheap to keep up,
  expensive to clear (24-hour bare-pavement standard).
- **Transit = ETS bus+LRT gross $436.605M (2025)**; **DATS excluded** ($31.966M
  of the $468.571M total) because it is door-to-door and generates no scheduled
  stop-events. Divided by the pipeline's OWN citywide stop-event total, like fire.
- Source for the two rates: Taproot Edmonton reporting quoting City infrastructure
  field operations staff; ETS from the 2024/2025 Annual Service Plan Appendix A.
  Both **relayed**, not fetched from the Oracle box.
### Known Quirks
- **The fire term is a demand ALLOCATION of a mostly-fixed budget** — a hood with
  2× the events does not cost the City 2× (most fire cost is standing capacity).
  Carry that caveat in any UI copy. **The transit term has the identical shape.**
- ⚠️ **THIS FILE HOLDS TWO INCOMPATIBLE BASES.** `roadway_om_renewal` is
  **$50/m/yr lifecycle**; `roadway_ops` is **$4.635/m/yr operating** — the SAME
  metres, **~10.8× apart**, and both ship to the served GeoJSON. Never sum or
  compare them. The `_ops` column suffix exists solely to keep them apart; a
  test pins them distinct. See the file's own `_two_bases` field.
- **`roadway_renewal` = $38/m/yr is the RENEWAL HALF of basis (1), not a third
  basis** (added 2026-08-07). The $50 decomposes into its two published
  components over the same 50-yr life: **$12/m/yr O&M + $38/m/yr renewal**.
  ⚠️ **Never sum `roadway_renewal` with `roadway_om_renewal`** — that
  double-counts renewal; exactly one of the two may appear in any figure.
  ⚠️ **The $12 O&M half is deliberately NOT published**: it would sit beside
  `roadway_ops`' $4.635/m/yr as a *second* recurring road number, ~2.6× apart
  from it and from a different source. Renewal was chosen precisely because it
  does not collide. **Inert to the served pipeline** — `load_unit_costs` still
  returns its same 5 keys, the `bikeway_capital` pattern; only
  `tools/ward_rollup.py` reads it. ⚠️ Anything built on it is an annual
  **REQUIREMENT, not a funding gap**, and **collector+local only** (arterials
  excluded), so it understates the network. `DECISIONS.md` 2026-08-07.
- ⚠️ **$178/km/yr IS NOT A LIFECYCLE RATE**, though it was proposed as one on the
  phrasing "replace, repair, and maintain". It derives from ~$0.27M/yr over
  ~1,500 km; the same source puts snow clearing on that network at **113× it**;
  at a 50-yr life it totals **$8,900/km** for build plus all replacement; and
  against the City's own ~3%/yr set-aside rule it is **~33× low**. Full record in
  `bikeway_ops.rejected_lifecycle_reading`. **No bikeway lifecycle figure exists
  yet** — that is an open TODO item, now blocked on ONE missing input (below).
- **Bikeway CAPITAL = $452,065/km, sourced and verified 2026-08-04** on Peter's
  laptop → `bikeway_capital`. Source: **Bike Plan Implementation Guide §1.2,
  Table 3** (678 km / $306.5M; bands $365k–$790k/km by urban form),
  construction-only and explicitly excluding maintenance. Checked, not relayed:
  every row's implied $/km lands inside its own stated band and the $190.8M
  City-borne subtotal reconciles. ⚠️ **This is $/km of ASSET VALUE, not a rate —
  it is INERT**, read by nothing (`load_unit_costs` still returns its same 5
  keys; a test-equivalent assertion is that adding the block left all 560 tests
  passing).
- ⚠️ **THE ONLY THING STILL MISSING IS A SERVICE LIFE, AND EDMONTON DOES NOT
  PUBLISH ONE** for bikeways or shared pathways. Searched 2026-08-04: the
  Development Impact page (roads + fire stations only), both Bike Plan PDFs, the
  2025 Infrastructure Report, the Infrastructure State-and-Condition / Inventory
  / Tools pages, the 2023 Capital Asset Management Audit. The Bike Plan's own
  action **9.6.2(a) is to *"establish"* a bikeway asset-management program** —
  the City flagged it as not yet existing. ⚠️ **Do NOT press the sidewalk
  figure into service:** *"amortized for 20 years"* on the sidewalk-
  reconstruction page is a **local-improvement tax levy term, not an asset
  life** — the same category error as the $178/km reading.
- ⚠️ **THE 3% SET-ASIDE RULE DOES NOT TRANSFER TO BIKEWAYS** — it is tempting as
  a way around the missing life, and this project's own numbers falsify it. At
  roads' implied 3.33%/yr, $452,065/km allows **$15,069/km/yr** for all O&M plus
  renewal, but measured `bikeway_ops` is **$20,278/km/yr — 1.35× that entire
  allowance** before any capital renewal. Bikeway cost tracks a winter **service
  standard**, not asset value. (The rule is asset-specific in the source anyway:
  fire stations get *"at least 6%"*.)
- ⚠️ **A THIRD numerator/denominator mismatch, direction KNOWABLE this time.**
  Table 3 blends the **future** facility mix; `bike_m_per_acre` measures the
  **existing** stock, which is **82.2% Shared Pathway and 89.8% off-road**, with
  only **0.8% Local Street Bikeway** — the cheap on-street types the blend leans
  on. So $452,065/km most likely **understates** our network's replacement
  value. Cross-check, not a competing value: the $100M Active Transportation
  Network Expansion over 68 km is **~$1.47M/km**, but that is a whole-program
  budget (design, contingency, land) in the dearer inside-Henday contexts.
- ⚠️ **Two rate/denominator mismatches, recorded not absorbed.** The bike snow
  rate blends over a ~1,500 km network the source defines as *"bike lanes,
  multi-use paths, public pedestrian squares, bus stops, LRT platforms, and
  staircases"* — substantially **not** dedicated bikeway, while our numerator
  (~981 km) is. The road snow rate blends over ~11,000 km **including arterials**,
  which are priority-cleared and cost more per km, so the local-road term is
  likely a little high. **The 11,000 km denominator is never imported into the
  spatial pipeline** — only the per-km rate is.
- ⚠️ **Vintage mismatch, accepted:** ETS is 2025 while fire is 2026 Approved.
  They never enter the same composite (fire → `svc_cost_per_acre`, transit →
  `transport_cost_ops_per_acre`), so it is across columns, not inside a number.
- **Sidewalks are a separate, non-overlapping category** (~5,776 km, ~$5.9M/yr
  ops) and are in neither the bike metric nor the 1,500 km snow denominator.

## 14. Geographic Reference Layers (orientation, added 2026-07-27)
`web/data/reference.geojson` (**94 kB, 33 features**, committed) — the North
Saskatchewan River, the regional **highway network**, and the named regional
geography. So a first-time viewer can orient before reading the fiscal data. The
map has **no basemap tiles** (just a dark backdrop), so without these there is
no geographic context at all. Purely cartographic: no metric, no tooltip.

**Every feature carries `kind`, and boundaries carry `name` (2026-08-08).**
Before that all 13 outlines shipped as a bare `{"t":"boundary"}` and the front
end **could not tell Edmonton's own legal limit from Devon's town outline** —
they drew in one colour because nothing distinguished them. The tiers:

| `kind` | what | drawn | named |
|---|---|---|---|
| `city` | Edmonton's legal limit | lighter, wider stroke | **no** — the page title already says Edmonton, and a label at the centre sits on the choropleth |
| `region` | the four counties it abuts | faint outline | yes (**reversal** — see below) |
| `place` | 9 neighbouring municipalities | faint outline | yes |
| `zone` | Alberta's Industrial Heartland | dim warm outline | yes |
| `econ` | Nisku, Edmonton Int'l Airport | **none** | yes |

⚠️ **Regions were deliberately UNLABELLED until 2026-08-08 and that reversed**
(Peter). The original reasoning — a county is too large to label at city zoom,
and the edge, not the name, is the message — holds for an *orientation* map and
fails for a *regional* one: once the question is "who else levies here, and what
does Edmonton not tax", an unnamed edge cannot answer it. ⚠️ The old objection
survives in the ANCHOR: a county centroid sits **27–58 km** from Edmonton's
centre, so centroid labels land off the default camera entirely. Labels are
placed on the county's visible strip near the city (`_region_anchor`).

⚠️ **`econ` names have no outline on purpose.** Nisku is a *hamlet* — Alberta
publishes hamlets as points only, so no legal polygon exists to draw. The
airport has an OSM polygon, but it is a ~28 km² shape 40 km south rendered at
1 px: naming it locates it, tracing it does not, and a municipal-grey outline
would read as another jurisdiction.

⚠️ **The Industrial Heartland's identification is OURS, not the source's.**
Alberta publishes it as one unnamed 590.7 km² MultiPolygon in
`boundaries/resource_designated_industrial_zone` — **no name field at all**. It
was identified by measuring who it overlaps: Sturgeon County 171.8, Strathcona
County 134.3, **Edmonton 53.2**, Fort Saskatchewan 29.5 km², remainder ≈ Lamont
County. That is exactly the Heartland's member set, and 590.7 km² matches the
~582 km² the association publishes. The builder guards it with an area floor
(`ZONE_MIN_KM2`) because there is no name to assert against.
⚠️ **53.2 km² of it is inside Edmonton's own boundary**, so unlike the airport
and Nisku it is *not* a clean "regional infrastructure Edmonton doesn't tax"
shape. Do not narrate it as one.

⚠️ **RETRACTED 2026-08-09 — "14% of Edmonton is missing from the hood fabric"
WAS WRONG, and the error was one of CAUSE, not arithmetic.** The 2026-08-08 note
read the drawn map's **672.4 km²** against a **782.1 km²** city and concluded
that **109.6 km² (14.0%) was annexed and undeveloped land carrying no
neighbourhood**. Re-measured in `EPSG:3400` from `data/raw/neighbourhoods.geojson`:

| what | km² |
|---|---|
| raw boundary file, all 407 features | **782.11** |
| the 406 hoods that render, raw geometry | **782.00** |
| legal boundary polygon (`reference.geojson`, simplified 100 m) | **782.38** |
| shipped `neighbourhood_value_per_acre.geojson` | **672.42** |

**The raw fabric tiles the city** — 1.4 km² of legal boundary is uncovered and
1.1 km² of fabric sits outside it, both inside the 100 m simplification noise on
that outline. **The 109.6 km² is `main.py`'s `SETBACK_M = 45.0`**, the inward
buffer that opens "city block" gaps between prisms: **every one of the 406 hoods
loses area** (median **18.3%**, min 2.7%, max 65.9% — the signature of a
perimeter-proportional shrink, not of missing land), and `buffer(-45)` then
`simplify(10)` reproduces **672.42 km²** to the decimal. The only hood in the
file that truly carries no data is `LEWIS FARMS`, **0.11 km²**.
- **No metric is affected** — and this is now true for a stronger reason than
  the original note gave. Metrics are per-neighbourhood over *upstream* areas;
  `setback_m` and `simplify_tolerance_m` are documented DISPLAY-only in
  `join_and_calculate.py`. ⚠️ **For a citywide-per-acre figure there are TWO
  denominators, not three: ~782 km² total and ~771 km² land.** `672.4` is not a
  candidate at all — it is drawn geometry and has no analytical meaning. The
  retracted note listed it as one, which is the trap this entry now exists to
  close.
- ⚠️ **782.1 km² INCLUDES WATER, and that is why it will not match a published
  figure** (measured 2026-08-08). Commonly cited areas for Edmonton are ~765–768
  km², which are **land** areas. Subtracting the North Saskatchewan where it
  runs inside the city (**10.9 km²**, from this layer's own river geometry)
  gives **~771 km²**, and other water bodies close most of the remaining ~3 km².
  **So there are two denominators** — legal total ~782, legal land ~771 — and a
  citywide figure must say which. A reader checking our number against Wikipedia
  or StatCan will hit this first. (The retracted note above made this a list of
  *three* by counting the drawn 672.4; it is not a denominator.)

Built by `scripts/build_reference_layers.py`. **NOT in the weekly refresh** —
static geography, same posture as `build_levy_catchments.py`; the endpoints are
queried once at build time, never at runtime. Features carry `t`
(`"river"` | `"highway"` | `"boundary"` | `"place"`), matching
`roads.geojson`'s convention; `place` features additionally carry `name`.

⚠️ **REVISED 2026-08-03 — `t="henday"` IS GONE, replaced by `t="highway"`.**
The old layer was the Anthony Henday alone, hand-extracted from the City
centreline feed, and it **stopped at the city limit**. Peter's ask was for the
main highways to run off the edge of the frame the way the river does. See
"Why OSM" below; the retired extraction's quirks are in `TODO_archive.md`.

- **River** — Alberta `base_water_feature` MapServer **layer 72**
  (`Lake/River (20K)`), `NAME='North Saskatchewan River'` (7 polygons
  province-wide, all genuinely the river). Clipped to the city bbox + a **60 km**
  margin so it runs clean off the edge of the view rather than stopping dead —
  the city sits *on* a river that comes from and goes somewhere, and two square
  ends just inside the frame read as a lake. The margin is sized against the
  default camera: at HOME zoom 10.2 and latitude 53.5 the scale is ~79 m/px, so
  a 1440px viewport spans ~114 km flat and the 52° pitch pushes the horizon
  further; the city half-width is only ~15 km. Natively **EPSG:3400**.
  **95% of the file** and deliberately never re-simplified (settled 2026-07-27:
  Peter checked the sub-pixel islands on device — they do not read as speckle).
- **Highways** — **OpenStreetMap via Overpass** (`overpass-api.de`), classes
  **`motorway` + `trunk`**, clipped to the *same* 60 km box as the river.
  Measured 2026-08-03: 1,194 ways / 999 km raw → **871 km welded in 89 parts**,
  of which **68% lies outside the city** and the extent exceeds the city bbox on
  all four sides. Top routes: Hwy 16 (Yellowhead) 337 km, Hwy 2 (QEII) 213 km,
  Hwy 216 (Henday) 156 km, Hwy 43 131 km, then 63/28/15/16A.
- **Boundaries + places** — Alberta `urban_and_rural_municipality` MapServer.
  Seven names (`PLACES` in the build script): St. Albert, Sherwood Park, Spruce
  Grove, Fort Saskatchewan, Leduc, Beaumont, Devon. Each yields **one Polygon**
  (the largest, simplified at 100 m — 169 vertices for all seven, ~3.6 kB) and
  **one Point** at that same polygon's centroid, so a label and the shape it
  names cannot disagree. Natively **EPSG:3400**.

### Why OSM, and the trap in the obvious alternative
Two sources were tried and rejected on 2026-08-03:
- **The City centreline feed** (`data/raw/roads.geojson`) carries every main
  highway — Yellowhead, Calgary Trail, Manning, Sherwood Park Fwy, Hwy 14/15/216
  — as `Province of Alberta` rows that `load_roads` filters out. But it is a
  *City* feed: the highways **stop at the municipal boundary**, which is exactly
  the amputated look `MARGIN_M` exists to prevent for the river.
- ⚠️ **Alberta's `transportation/highways_public` MapServer RETURNS NULL
  GEOMETRY.** It has ideal attributes (510 `IN SERVICE` segments with
  `ROAD_NUMBER` over this extent) and answers **HTTP 200 with all 510 features
  and no shapes** — in `f=geojson` and `f=json`, with and without `outSR`, with
  and without an envelope, on the simplest possible `where`. Its
  `capabilities` still advertise `Query`. **A reader that trusts the feature
  count would emit an empty highway layer and log success.**

### Known Quirks
- ⚠️ **Overpass answers `406 Not Acceptable` to a raw POST body or an anonymous
  client.** The query must be **form-encoded as `data=`** with a **named
  `User-Agent`** (`OVERPASS_USER_AGENT`), as its usage policy asks.
- **OSM is ODbL**, so the credit is required *wherever the data is used*. The
  Data & Methods pod carries it in **both** builds — unlike the City
  road/fire/transit credits, which are full-only because those lenses are.
- **`primary` is deliberately NOT in `HIGHWAY_CLASSES`** — it would add ~1,591
  ways and ~1,786 km of in-city arterials, tripling the file and competing with
  the choropleth on a map that has no basemap precisely so the data reads first.
- **The highway layer is many OPEN-ENDED corridors** (89 parts), by design: they
  run off the clip edge. Anything asserting closure — as the retired Henday ring
  check did — is asserting the wrong invariant. The live assertion is that the
  network **extends past the city on all four sides**
  (`verify-reference-layer.js`), falsified by clipping it to the city limit.
- **Hwy 216 measures 156 km in OSM vs the 149 km** the retired City-feed
  extraction produced for the ring's two carriageways. Agreement within ~5% is
  what justified dropping the hand-tuned extractor; `HIGHWAY_RING_REF_KM` warns
  if that drifts past 25%.
- **At the 60 km clip the river is a MultiPolygon** (disjoint stretches up- and
  downstream), where a narrow clip yields a single Polygon. Anything asserting
  its geometry type must accept both.
- ⚠️ **`REGIONS` outlines are deliberately NOT clipped to the view extent**,
  unlike the river and the highways. Those are open shapes that would stop dead
  mid-frame without a clip; a municipality is a **closed ring**, so clipping one
  replaces its far side with a straight run along the clip box that **draws as
  if it were a real border**. Parkland County is the only one that leaves the
  extent (66.7% inside) and it simply runs off the edge.
- ⚠️ **Strathcona County is in sublayer 104 (`Specialized Municipality`,
  `SPMUN_NAME`), NOT 114** (`Municipal District and County`) with the other
  three. Alberta models specialized municipalities separately, so looking in the
  obvious county layer returns nothing. This is the `REGIONS` equivalent of the
  Sherwood Park / layer-66 trap above.
- ⚠️ **"Leduc" names two different polygons across the two lists** — the CITY of
  Leduc (`PLACES`, layer 78) sits INSIDE **Leduc County** (`REGIONS`, layer
  114). Querying one where the other is meant returns a shape of the wrong
  scale with no error.
- **`boundary` features are no longer 1:1 with `place` features** (12 vs 7).
  That used to be an asserted invariant in `verify-reference-layer.js`; it was
  retired deliberately, not broken — `REGIONS` outlines carry no name because
  these shapes are far too large to label at city zoom (Parkland County alone
  is 3.5× Edmonton).
- **Municipal outlines are drawn UNDER the data**, with the river. The seven
  places sit outside Edmonton, so no hood polygon hides them (measured: 0–0.7%
  of each outline overlaps the city fabric) — and underneath they can never cut
  across a prism the way an over-composed line would.
- **The municipality service models legal STATUS, not size, so the seven places
  need THREE sublayers** — and the obvious single-layer implementation silently
  finds nothing for two of them:
  | Sublayer | Name | Field | Places |
  |---|---|---|---|
  | **78** | City | `CITY_NAME` | St. Albert, Spruce Grove, Fort Saskatchewan, Leduc, Beaumont |
  | **56** | Town | `TOWN_NAME` | Devon |
  | **66** | Urban Service Area | `USA_NAME` | Sherwood Park |
  **Sherwood Park is the trap:** it is not a town or a city but an urban
  service area of Strathcona County, so it is in neither 78 nor 56. (Distinct
  again from **104**, `Specialized Municipality`, which holds *Strathcona
  County itself* — see the Tier 3 boundary note.) **Beaumont has been a city
  since 2019**, so it is in 78 rather than 56.
- **Sublayer 66 also holds `Sherwood Park (Bremner)`**, a separate
  future-growth polygon ~10 km east. The query matches on **equality**, not a
  prefix or `LIKE` — a pattern match would pull Bremner in and drag the label
  anchor off the real town.
- **`PLACES` is a closed hand-written list, not a radius query.** Which names
  belong on the map is a cartographic judgement (how populated should the frame
  feel?), so it is stated rather than derived: a bbox sweep would silently gain
  and lose names as the province edits boundaries, and the map's composition
  would drift with it. A name that stops resolving **raises** rather than
  quietly shipping a map with a hole in its orientation.
- **Leduc is off the bottom edge at the default camera** (projects to y≈1102 in
  a 900px viewport at HOME zoom + 52° pitch) and is culled by the label
  declutterer. That is correct behaviour, not a missing label — it appears on
  pan or zoom-out. Anything asserting "all seven visible" will fail.

## Name Matching

Neighbourhood names between the two sources may not align exactly. Normalization (strip + uppercase) and the `NAME_CORRECTIONS` dict (keyed assessment name → boundary name) are applied in `load_assessment.py`, *before* aggregation — applying corrections after aggregation could collapse two summed rows onto one boundary and duplicate it. `join_and_calculate.py` then does a normalized exact match on the already-corrected names and flags whatever remains unmatched.

**Investigation script:** `scripts/investigate_neighbourhood_names.py`

### Confirmed correction dict (assessment name → boundary name)

```python
NAME_CORRECTIONS = {
    "ANTHONY HENDAY SOUTHEAST":        "ANTHONY HENDAY SOUTH EAST",
    "CHAPPELLE AREA":                   "CHAPPELLE",
    "EDMONTON RESEARCH AND DEVEL PARK": "EDMONTON RESEARCH AND DEVELOPMENT PARK",
    "HERITAGE VALLEY TOWN CENTRE AREA": "HERITAGE VALLEY TOWN CENTRE",
    "LEWIS FARMS INDUSTRIAL":           "LEWIS FARMS BUSINESS EMPLOYMENT",
    "PLACE LA RUE":                     "PLACE LARUE",
    "RAPPERSWIL":                       "RAPPERSWILL",
    "RIVER VALLEY WINDEMERE":           "RIVER VALLEY WINDERMERE",
    "SOUTHEAST (ANNEXED) INDUSTRIAL":   "SOUTHEAST INDUSTRIAL",
    "WESTBROOK ESTATE":                 "WESTBROOK ESTATES",
}
```

### Resolved

| Assessment name | Boundary name | Resolution |
|----------------|--------------|------------|
| `OLIVER` | `WÎHKWÊNTÔWIN` (#1151) | 2024 rename. Assessment data has already migrated: 12,234 rows / $4.12B are tagged `WÎHKWÊNTÔWIN` (matches the boundary directly), with a single straggler row still tagged `OLIVER` ($500 total). The unmatched warning is real but immaterial — no correction-dict entry added, since mapping it would shift $500 onto a $4.12B neighbourhood. |
| `HERITAGE VALLEY TOWN CENTRE AREA` | `HERITAGE VALLEY TOWN CENTRE` | Resolved 2026-07-01 (data-integrity audit): spatial containment — 945 of 946 properties fall inside the HVTC boundary polygon (1 in adjacent Desrochers). Before the correction the boundary matched only a 15-row / $2.25M slice under the exact name, rendering the hood at ~1/250th of its real $572.7M — a *partial* match, so the error was invisible on the map. Correction added. See `docs/FINDINGS_data_integrity_audit.md` §1. |
| `LEWIS FARMS INDUSTRIAL` | `LEWIS FARMS BUSINESS EMPLOYMENT` | Resolved 2026-07-01 (data-integrity audit): spatial containment — 100 of 103 properties ($106.3M) fall inside the LFBE polygon (3 spill into adjacent LEWIS FARMS, boundary-edge cases). Previously LFBE had zero matched rows → dropped at export → hole in the map. Correction added. See `docs/FINDINGS_data_integrity_audit.md` §2. |

### Unresolved

*None.* The only expected unmatched warning is the `OLIVER` straggler (immaterial, deliberate — see Resolved above). Any **other** name appearing in the unmatched warning is new drift and should be investigated (spatial containment via the assessment lat/lon columns is the decisive test). **This is now enforced in CI:** `scripts/check_unmatched_names.py` asserts the live money-path unmatched set equals the committed baseline `data/expected_unmatched.json` (`{OLIVER}` assessment-side, `{LEWIS FARMS}` boundary-side) and fails the weekly build on a new assessment-side name — see RUNBOOK §2 "Check unmatched names".

---

## Per-property zoning: use the POLYGONS, not `dkk9-cj3x`'s `zoning` field (2026-08-01)

Measured while building the revenue-lens readout (`src/revenue_by_zone.py`).

`dkk9-cj3x` ("Property Info") carries a `zoning` string per account, and joining
it to the assessment roll on `account_number` is clean — 1:1, no duplicates, every
tax class matched. **It is still the wrong source here.**

| | |
|---|---|
| properties with **null** `zoning` | **35.7%** (157,030 / 439,685) |
| **revenue** with null `zoning` | **16.0%** ($433M of $2.70B) |
| **DOWNTOWN**'s revenue with null `zoning` | **42%** |

The nulls are **condo units** — Downtown is 95% unzoned by property count. A
"top 3 zones by revenue" built on this field showed *unzoned* as Downtown's
largest single entry.

**The fix, and why it is better than a workaround:** every one of those
properties has coordinates (`latitude`/`longitude`, 100% non-null in the cleaned
assessment frame), and a point-in-polygon against `data/raw/zoning.geojson`
placed **11,022 / 11,022** of Downtown's unzoned properties. Citywide the
unplaced share falls from 16.0% to **0.002%** (8 properties, $9,034). Because
those are the *same* polygons the Uses lens colours by area, revenue-by-zone and
the Uses composition become one map read two ways and cannot disagree.

**Two traps found doing this, both silent:**
- `.str.split().str[0]` on an empty string yields **NaN, not `""`** — a
  "code is present but unmatched" filter written the obvious way silently
  swallows every null-zoning row, and reported 16.04% of revenue as sitting in
  three rare zone codes. It is 0.003%.
- `gpd.sjoin` where **both** frames carry a `zoning` column suffixes them to
  `zoning_left`/`zoning_right`, and the later lookup fails or silently reads the
  wrong side. Drop the left one first.

**Coverage of the category map:** 75 of the 78 codes present resolve through
`load_zoning.ZONE_CATEGORY`; the three that do not (`CSC`, `RSL`, `US`) carry
**0.003%** of revenue and fall to `other`, flagged.

⚠️ **1,585 properties sit exactly on a zone boundary** and match two polygons.
`sjoin` emits a row per match, so they must be de-duplicated or their levy is
double-counted and the per-hood fractions stop summing to 1.

## 15. Bike Routes (transportation lens, added 2026-08-02)
`vd4b-a4iv` ("Bike Routes") — on- and off-road cycling routes as
MultiLineStrings, EPSG:4326 via Socrata GeoJSON. **10,417 segments** on first
pull (2026-08-02); 8.0 MB raw. Feed is live and City-maintained (`updatedAt`
2026-07-27). Downloaded by `scripts/download_data.py` (`bike_routes`), both
truncation guards active (`$limit=20000`, server `count(*)` cross-check).
**Consumed by `src/load_bike.py`** → `bike_m_per_acre` (SPEC_services.md
"Transportation lens"). Carries no roll-year pin — like roads and transit its
provenance is `last_checked`.

### Key columns
- `classification` — the 12-value closed enumeration that decides what counts;
  see the table below. Mapped by an EXPLICIT dict (`CLASSIFICATION_GROUP`).
- `route_coming_soon` — real bool. **651 rows are `True`**: planned, not built.
- `type` — `ON ROAD` / `OFF ROAD`. Orthogonal to `classification` (Shared
  Pathway appears as both), so it is kept only as the internal
  `bike_m_onroad` / `bike_m_offroad` split, never as the classifier.
- `network_classification`, `road_segment_type`, `construction_year`,
  `street_name_full`, `duration`, `line_weight` — unused.

### What counts, and the two traps
Measured 2026-08-02, kilometres of built (not coming-soon) route:

| classification | km | group |
|---|---|---|
| Shared Pathway | 806.4 | **dedicated** |
| Shared Trail | 74.7 | **dedicated** |
| Protected Bike Lane | 56.7 | **dedicated** |
| Painted Bike Lane | 27.9 | **dedicated** |
| Local Street Bikeway | 7.9 | **dedicated** |
| Contra-Flow Bike Lane | 7.4 | **dedicated** |
| Shared Roadway - Lower Traffic | 194.7 | shared_roadway (excluded) |
| Shared Roadway - Higher Traffic | 76.4 | shared_roadway (excluded) |
| Bus / Bike / Taxi Lane | 9.0 | shared_roadway (excluded) |
| Walkway / Breezeway | 238.7 | pedestrian (excluded) |
| Maintenance Access | 1.9 | pedestrian (excluded) |
| Unclassified | — | unclassified (excluded; 100% coming-soon) |

⚠️ **TRAP 1 — "Shared Roadway" IS A ROAD, AND IT IS ALREADY COUNTED.** Those
280 km are ordinary streets carrying a bike-route designation. They add no
asset, and `load_roads` already counts their metres in `road_m_total`, so
including them double-counts the road network against itself. This is why the
two supply columns are safe to read side by side.

⚠️ **TRAP 2 — "Walkway / Breezeway" IS 3,031 ROWS OF PEDESTRIAN PATH**, the
second-largest classification in the whole feed. A naive "sum the bike routes"
metric is ~50% not-bike by length.

### Known Quirks
- **Unmatched classifications default to EXCLUDED**, the opposite of
  `load_roads`' default-to-local. The feed is mostly *not* bike infrastructure,
  so an unrecognised value is more likely another non-asset; defaulting in would
  let upstream drift silently inflate a supply metric. Warned loudly either way.
- **981 km kept, 1.17% falls outside every neighbourhood polygon** (conservation
  guard, well under the 5% warn threshold). **335 of 407 hoods** have any
  dedicated route; the other 72 are true zeros at the join.
- ⚠️ **The metric is 82% off-road pathway, much of it river-valley and ravine
  trail** — so `bike_m_per_acre` peaks in exactly the set-aside hoods that
  generate almost no revenue (top 4: MILL CREEK RAVINE NORTH/SOUTH, RIVER VALLEY
  WALTERDALE/GLENORA, all set-aside). Same shape as the `RATIO_ROAD_FLOOR`
  denominator artifact. The UI blurb says so.
- **`web/data/bike_routes.json`** (committed, lazy-loaded, 0.24 MB, 4,049 welded
  path segments) is the map's context layer — the LRT-lines format
  (`{"lines": [...]}`), geometry only, no per-feature value.

## 16. Citywide Operating Budget Context (Data & Methods pod, added 2026-08-03)
`data/city_budget_context.json` — the four-row "how big is this against the
whole City budget" comparison in the Data & Methods popover. Manual reviewed
input (mill-rates pattern; NOT auto-fetched, NOT in the weekly refresh).
Reaches the frontend through `status.json` via
`generate_status.budget_context()`; the section hides itself if the file or the
manifest field is missing.

| line | $/yr | share of $3.8B |
|---|---|---|
| Transit (bus + LRT + DATS, gross operating) | $468.571M | 12.18% |
| Roads (maintenance + snow) | $102.521M | 2.67% |
| Bike lanes & shared pathways (maintenance + snow) | $30.420M | 0.79% |
| Sidewalks (ops) | $5.900M | 0.15% |

Total City operating budget **$3,845,555,000 (2025)** — publicly quoted as
"$3.8 billion". ✅ **Corroborated 2026-08-04** against the Open Budget portal
(§17): FY2025 **tax-supported** expenses total **$3,855,881,010**, so this value
is **99.73%** of it. Every share in the table divides by this number and it had
been relayed, so it was worth checking.

⚠️ **IT IS THE TAX-SUPPORTED BUDGET, NOT ALL FUNDS — and that is the RIGHT
denominator, not a limitation.** All-funds FY2025 is **$4,203,648,909**; the
difference is Utilities ($235.8M) and Enterprise/CRL ($112.0M). All four
numerators here are tax-supported, so an all-funds denominator would understate
every share (transit 11.15% instead of 12.18%, roads 2.44% instead of 2.67%).
**If the pod's "$3.8B operating budget" copy is ever reworded, do not let it
imply all funds.**

### Known Quirks
- ⚠️ **OPERATING ONLY, every line.** No capital anywhere: road reconstruction,
  asphalt overlay and the Neighbourhood Renewal Program on one side; new trains,
  garages and line extensions on the other. The rows are comparable **to each
  other** and none is a total cost. **Never let this read as "what
  transportation costs Edmonton."**
- ⚠️ **CITYWIDE — DO NOT WIRE TO THE SPATIAL PIPELINE.** The road figures span
  the ~11,000 km network **including arterials**; the neighbourhood lens
  excludes arterials by decision, so the two use different denominators and
  **must not share a constant**. Nothing in `src/` or `main.py` reads this file.
- ✅ **The roads-maintenance component is now PUBLISHED — and the derived figure
  it replaced was ~5× too low.** It was `$1,285/km × ~11,000 km = $14.135M`
  (a narrow unit rate multiplied across the whole network, with the
  *snow-clearing* network reused as the maintenance denominator). Now
  **$65,671,000**, the Open Budget portal's `Roadway Maintenance` program
  (FY2017) — see §17. `derived_component` is gone, so the pod's asterisk is gone.
  ⚠️ **The error was in OUR derivation, not the Taproot source** — that source's
  *totals* reconcile to 99.2% (below); only the rate×network product did not.
  The published program implies ~**$5,900/km**, not $1,285/km.
- ⚠️ **2017 IS THE ONLY YEAR WITH A ROADS-ONLY MAINTENANCE PROGRAM**, so a stale
  vintage is the price of a clean scope. The tree was re-cut in 2018 (folded into
  `Infrastructure Maintenance`, which *also* covers sidewalks, pathways and
  bridges — using it here would **double-count** against this table's own
  sidewalks and bike rows) and again in 2026 (`Mobility Infrastructure
  Services`). Peter's call 2026-08-04, documented rather than silently mixed, as
  with ETS 2025 vs fire 2026. Being 2017 dollars it is if anything a **lower
  bound**: the branch grew ~34% ($244.9M → $327.1M) by 2025.
- ✅ **THE SNOW FIGURES ARE INDEPENDENTLY CORROBORATED.** Roads snow $36.85M +
  path snow $30.15M = **$67.0M** against the portal's published `Snow and Ice
  Control` program at **$67,553,815 (FY2025) — 99.2%**. That is why the snow
  components were left untouched, and **the contrast with maintenance is what
  exposed it**: same source, one number reconciling and one not.
- ⚠️ **Transit here INCLUDES DATS ($31.966M); the per-acre transit cost column
  EXCLUDES it.** Different questions, and they are *supposed* to differ — §13's
  `transit_ets` allocates by scheduled stop-events, which DATS does not generate.
- ⚠️ **The Active Transportation Acceleration project ($4.3M) is deliberately
  NOT a row.** It is capital debt service + incremental maintenance for *new*
  build-out, while the bike line is the cost of running what exists — not
  additive. Kept in `excluded_from_the_table` so the figure is not lost.
- **Sidewalks and active transport are separate, non-overlapping categories** —
  sidewalks (~5,776 km) are not in the 1,500 km snow-clearing network, which the
  source enumerates. The two lines are safely additive.
- ⚠️ **NO SHARE OR RATIO IS EVER PUBLISHED** — the manifest carries dollars and a
  total, and the UI divides. The research this table came from shipped ratios
  that had slid one row (*"transit is roughly 15× the road ops budget"*; 15.4× is
  active transport, and sidewalks are 79.4×, not the claimed ~90×). Deriving
  makes that class of error unrepresentable. ⚠️ **The roads ratio has since moved
  on its own merits: 9.2× → 4.6×** on 2026-08-04, when the maintenance component
  was corrected. Because nothing pins a share, that was a **one-value edit** —
  which is the whole argument for the rule.

## 17. Open Budget Portal — program-level operating budgets (added 2026-08-04)
⚠️ **SAME PUBLICATION AS Socrata `da9s-v9j8` (§18), not an independent source** —
verified to the dollar 2026-08-16. Never cite the two as corroborating each
other; their agreement is a tautology.

`https://budget.edmonton.ca/api/operating_budget.csv` — the City's Open Budget
portal, **machine-readable and primary**. **7,283 rows, FY2017–FY2026**, one row
per `budget_year, fund_type, department, branch, program, category, account_type,
budget`. First fetched by hand on Peter's laptop 2026-08-04. **NOT downloaded by
`download_data.py`, NOT in the weekly refresh, NOT read by `src/` or `main.py`**
— it is a sourcing tool for the manual reviewed inputs (§13, §16), not a pipeline
input.

✅ **CORRECTED 2026-08-13 — IT IS REACHABLE FROM THE ORACLE BOX.** This line used
to add *"(edmonton.ca is unreachable from the Oracle box, §13)"* as the reason for
the laptop fetch. **`budget.edmonton.ca` is a different host from
`www.edmonton.ca`**: measured 2026-08-13 it returns `HTTP 200`, 1,037,656 bytes,
7,283 rows, while `www.edmonton.ca` fails to connect (`000`) in the same sweep.
`data.edmonton.ca`, `alberta.ca` and `open.alberta.ca` also resolve. ⚠️ **§13's
blanket "edmonton.ca is unreachable" is true only of `www.` — test the specific
host before recording a blocker from it.** (Two pieces of work were parked on the
generalised version: this fetch, and the ASSET manual on open.alberta.ca, which
turned out to be a transient 520 rather than a network policy.)

### Why it matters
It is the **only public source with sub-branch operating detail**. The Approved
Operating Budget PDF stops at branch level, where roads are bundled with parks
(`Parks and Roads Services`, FY2026 gross **$303.361M**; gross − revenue = net
cross-checks) — far too coarse to source a roads line. The portal resolves that
branch into programs: `Roadway Maintenance`, `Snow and Ice Control`,
`Parks Operations`, `Traffic Operations, Signals and Street Lighting`, and more.

### Known Quirks
- ⚠️ **THE PROGRAM TREE WAS RE-CUT TWICE AND PROGRAM NAMES DO NOT SURVIVE IT** —
  a "format eras" problem exactly like §11's FIR debt series. **2017:** roads-only
  programs (`Roadway Maintenance` **$65.671M**, `Snow and Ice Control` $63.709M).
  **2018–2025:** renamed and re-scoped to `OPS/PARS - Infrastructure Maintenance`
  ($49.7M–$56.9M), which **also covers sidewalks, pathways and bridges**.
  **2026:** re-cut again into `OPS/PARS - Mobility Infrastructure Services`
  ($76.95M). **Never build a time series by program name without checking which
  era each year is in** — a naive `groupby(program)` shows most programs
  abruptly hitting zero, which is a rename, not a cut.
- ⚠️ **`account_type` IS `Expenses` ONLY** — there is no revenue side here, so
  every figure is **gross**, never net. `fund_type` is `Tax Supported` for this
  branch.
- ⚠️ **THE PORTAL AND THE PDF DO NOT TIE EXACTLY.** Portal FY2026 Parks and Roads
  Services totals **$307,325,053** against the PDF's **$303,361,000** gross,
  **+1.31%**. Small, but they are different publications — do not present them as
  one series.
- **`category` is expense TYPE, not service** (Personnel, Fleet Services,
  Materials, External Services, Intra-municipal Charges…), and **intra-municipal
  lines are negative**, so category sums net out. Fine for totals; useless for
  splitting a program by what it maintains.
- **`/api/services.csv` does not exist** — it returns a 404 page. Only
  `operating_budget.csv` and `capital_projects.csv` were confirmed live.

### What it has already settled
- **§16's roads-maintenance component**, $14.135M (derived, ~5× low) →
  **$65.671M** published.
- **Corroborated §16's snow figures to 99.2%** — roads $36.85M + paths $30.15M =
  $67.0M vs the published `Snow and Ice Control` program $67,553,815 (FY2025).

### Cross-checks it enabled on the OTHER manual reviewed inputs
Run 2026-08-04. **None changed a committed value**; all are recorded so the
inputs are corroborated rather than merely relayed.

| repo figure | committed | portal | agreement |
|---|---|---|---|
| §16 total operating budget (2025) | $3,845,555,000 | $3,855,881,010 *(tax-supported)* | **99.7%** |
| §13 `fire_response` gross (2026) | $276,706,000 | $279,264,931 *(Fire Rescue Services branch)* | **99.1%** |
| §16 transit incl. DATS (2025) | $468,571,000 | $482,556,115 *(Edmonton Transit Service branch)* | **97.1%** |

- **Fire's 0.9% gap is the portal-vs-PDF gap**, same direction and size as the
  +1.31% seen on Parks and Roads — the repo figure is from the Approved
  Operating Budget PDF. Not an error in either.
- ⚠️ **Transit differs by ~3% and it is a SOURCE difference, not a mistake.**
  The repo takes bus+LRT **$436.605M** and DATS **$31.966M** from the ETS
  2024/2025 Annual Service Plan; the portal shows **$449.11M** and **$33.45M**
  for the same year. **Immaterial to the map**: `cost_transit_ops_per_acre`
  divides the budget by the pipeline's own citywide stop-event total, so a
  uniform ~3% scales every neighbourhood identically and moves no relative
  pattern. **Do not "fix" one source to the other** — the Annual Service Plan is
  the one that separates bus+LRT from DATS, which is what
  `transit_ets.chosen_numerator` requires.

## 18. Ranked branch operating budget — the `/full/` budget panel (added 2026-08-16)
`web/data/budget_ranked.json`, generated by `scripts/export_budget_ranked.py`
from Socrata **`da9s-v9j8`** ("Approved Operating Budget - Expenses") on
`data.edmonton.ca`.

⚠️ **`da9s-v9j8` IS §17's `budget.edmonton.ca/api/operating_budget.csv`, NOT A
SECOND SOURCE.** Verified 2026-08-16 by identity, because it arrived as a
"new dataset" suggestion and the two would otherwise be presented as
corroborating each other:

| check | §17 (portal CSV) | `da9s-v9j8` |
|---|---|---|
| columns | 8: `budget_year … budget` | identical |
| rows / years | 7,283, FY2017–FY2026 | 7,283, FY2017–FY2026 |
| FY2025 tax-supported total | $3,855,881,010 | **$3,855,881,010** |
| FY2026 Parks and Roads Services | $307,325,053 | **$307,325,053** |

Both tie **to the dollar**. Treat any agreement between them as a tautology, never
as corroboration. **What actually changes is the host:** `data.edmonton.ca` is
the one the rest of the pipeline already talks to, so this needs no new network
path — §17's hand-fetch does.

### Cadence — NOT weekly, and not "continually updated"
The dataset's own `rowsUpdatedAt` was **2026-06-05** when first pulled (~10 weeks
stale at the time), and that is normal: an *approved* budget moves when Council
approves a budget or an adjustment, roughly annually. ⚠️ **It must not ride the
weekly refresh.** The assessment roll moves weekly; letting the two share a
cadence would imply a freshness this data does not have. Manual, reviewed input
on the mill-rates pattern (§11, §16) — run the script by hand, eyeball the diff,
commit. The output carries the source's `rows_updated_at`, and the panel prints
it, so the panel dates itself from the SOURCE rather than from the run.

### The split, and why it is derived rather than a branch list
The panel ranks branches in two blocks. A branch is **"other"** iff it has zero
dollars in any of `Personnel`, `Materials, Goods and Supplies`, `External
Services`, `Fleet Services`, `Utilities & Other Charges`, `Intra-municipal
Charges` — i.e. it employs nobody and buys nothing, it only moves money.
Measured FY2026: **43 service branches, 5 other.**

⚠️ **Why the split exists at all:** `Capital Project Financing` is **$687.6M**,
the single largest line in the tax-supported budget — ahead of Police. An unsplit
ranking answers "what does Edmonton spend most on?" with *debt service*.

⚠️ **Classifying by CATEGORY instead would be wrong**, and this was measured:
`Transfer to Reserves` spans **11 branches including Police ($14.3M)**, so a
category filter strips service branches of parts of their own budget.

⚠️ **`Corporate Expenditures` is NOT financing despite the name** — it is WCB,
Risk Management, Sundry, LTD liability and incentive grants. It lands in "other"
because it delivers no service, not because it is debt. The other four are
`Capital Project Financing`, `Neighbourhood Renewal`, `Taxation Expenditures`,
`Automated Enforcement`.

The rule is applied to the data on every run and **never hardcoded as a branch
list**, because the budget tree gets re-cut (§17 records two re-cuts of the
PROGRAM tree inside Parks and Roads alone) and a name list would silently
misclassify on the first rename. The classification is written into the output
precisely so a human diff catches membership drift.

### Known Quirks
- ⚠️ **Gross, and operating only.** No capital programme, and no revenue offset,
  so **no line here is a net cost**. The revenue side is a sibling dataset,
  `m84q-ghmu` ("Approved Operating Budget - Revenues", 1,414 rows, same 8
  columns) — **not read by anything yet**. §17's *"there is no revenue side
  here"* is true of the expense feed only; the sibling closes that gap if it is
  ever wanted.
- **Branch totals are net of intra-municipal recoveries**, which are negative
  lines (`Intra-municipal Recoveries` is **-$219.8M** across 27 branches). That
  is what makes them safe to sum without double-counting internal cross-charges,
  but a branch total is therefore **not** what that branch spends in the world.
- **`Tax Supported` only** by default — the correct denominator, matching §16.
  FY2026 all-funds adds Utilities ($246.6M) and Enterprise/CRL ($127.7M).
- ⚠️ **Citywide totals with NO neighbourhood dimension.** Nothing here joins to
  the map, and nothing in `src/` or `main.py` imports it — the same boundary
  §16 states, for the same reason.

### Integrity rules (the script refuses to publish otherwise)
Branch totals must reconcile to the cent against an independently queried fund
total; every branch must classify and both blocks must be non-empty; a negative
branch total hard-fails; an unknown budget year hard-fails. `tests/test_export_budget_ranked.py`
covers each guard.

## 19. Approved Capital Budget — profile level (added 2026-08-22)
`data/capital_budget.csv`, hand-fetched from
**`https://budget.edmonton.ca/api/capital_budget.csv`** — the same Open Budget
portal host as §17, whose capital endpoints had never been probed.

⚠️ **THE OPEN DATA PORTAL HAS NO CAPITAL BUDGET.** Searched `data.edmonton.ca`
2026-08-21: approved-budget datasets are `da9s-v9j8` (operating expenses, §18)
and `m84q-ghmu` (operating revenues) — **both OPERATING** — plus `552h-hjwj`
(214 rows, the `building.edmonton.ca` app feed, 4 asset types) and a 2015 relic
(`pdmi-3qjb` / `r993-376i`). None of them is the capital budget. Do not go
looking for a Socrata capital sibling again; there isn't one.

**1,884 rows**, one per `fiscal_year, service, branch, profile_id, profile,
fund_type, fund, approved`. FY**2023–2037**, **$11,510,831,000** total.

⚠️ **THE GRAIN IS NOT ONE ROW PER PROJECT.** 1,884 rows carry only **399 distinct
`profile_id`s** — a profile repeats across fiscal years AND across funding
sources (up to **8 rows** for a single year+profile). Any per-project count or
average must `groupby("profile_id")` first; `len(df)` is a row count, not a
project count.

⚠️ **`approved` GOES NEGATIVE — 87 rows totalling −$161,302,000.** These are
funding-source reallocations, not cancellations: `15-75-0108 Mitchell Transit
Garage` carries **+$500,000 Developer / Partner Financing and −$500,000
Pay-As-You-Go** in the same year, netting to zero. **$11.51B is the NET**
(gross positive $11,672,133,000). ⚠️ **This breaks naive `fund_type` filtering** —
"how much is PAYG-funded?" is wrong unless the negatives are carried, and they
straddle fund types by construction, so a positives-only filter double-counts
the swap. 7 year+profile pairs net to exactly $0.

| | |
|---|---|
| dense window | **2023–2026 = $9,216,794,000** (the approved four-year cycle) |
| tails | carry-forwards only — 60 rows in 2027 falling to 1 in 2037 |
| top services | LRT Expansion $4.10B · Roads $1.48B · Recreation & Culture $1.02B · Yellowhead Freeway Conversion $789M · Neighbourhoods $716M |
| `fund_type` | Grants $4.60B · Tax-Supported Debt $3.50B · Reserves $1.23B · PAYG $852M · Retained Earnings $766M · CRL $290M |

A sibling `capital_projects.csv` (399 rows: `profile_id` → description, phase,
address, **lat/long**) is **NOT committed** — see the join-coverage warning in
`docs/ANALYSIS_BACKLOG.md` §11 before building anything spatial on it.

### Cadence — ⚠️ NOT annual, and there is NO freshness header
The capital budget is a **four-year cycle** moved by supplemental adjustments —
not weekly, not annual. **Manual reviewed input** (§13, §16, §18 pattern);
`download_data.py` does not fetch it and nothing in `src/` or `main.py` reads it.

⚠️ **`Last-Modified` merely ECHOES `Date`, behind `Cache-Control: no-cache`** —
there is no `rowsUpdatedAt` equivalent (§18), so **the committed file IS the
pin** and `vintage_report.check_capital_budget` compares content, not dates.
Any figure published from this must date itself from the **budget cycle**, never
from the fetch. The `⚠️ Capital budget` digest row is `docs/RUNBOOK.md` §1a.

### Known Quirks
- ⚠️ **NEW-VS-RENEWAL IS NOT A PUBLISHED FIELD.** Only two profiles are named
  outright (`Transportation: Neighbourhoods - Renewal` $69.8M,
  `Transportation: Bridges & Auxiliary Structures - Renewal` $50.7M); everything
  else would have to be inferred from words like "Reconstruction" in `profile`.
  **That is the `DATA_INTEGRITY.md` T8 hand-enumeration shape** — a value-sum
  over a name-matched set with no self-check. A keyword pass gives ~$1.02B
  renewal / ~$1.49B new across the road-ish services for 2023–26; treat it as
  **indicative only and do not publish a split sourced that way.**
  - ✅ **BUT THE SPLIT IS PUBLISHED — just not in this CSV** (added 2026-09-03).
    **Table 8, "Adopted Capital Budget by Service", pp.56–57** of the
    *2023-2026 Capital Budget* (December 2022,
    `https://www.edmonton.ca/sites/default/files/public-files/2023-2026CapitalBudget.pdf`)
    carries explicit **Growth** and **Renewal** columns per service. The
    road-relevant lines, $millions, 2023–2026:
    **Active Pathways and Roads Service — Growth 622.8 / Renewal 1,171.2 /
    Total 1,794.0**; **Yellowhead Trail Freeway Conversion — Growth 493.4**
    (booked separately as a transformational service); Grand Total
    4,997.6 / 2,194.9 / **7,192.5**. So a defensible new-vs-renewal figure can be
    **cited rather than hand-built** — use this instead of a keyword pass.
  - ⚠️ **Three methods, and they disagree mostly on the NEW side.** Renewal:
    ~$1.02B (keyword) · $1.08B (hand bucket classification, 2026-09-03) ·
    **$1.17B (Table 8)** — a ~15% spread. New: ~$1.49B (keyword) · $1.04B
    (hand) · **$1.12B (Table 8)** — a **~1.4× spread**, three times wider. The keyword pass
    overstates *new* because it sweeps in ~$326M of active-transport, pedway,
    pedestrian-bridge and streetscape profiles that are neither road
    construction nor road maintenance. **The warning above is right; Table 8 is
    the way out of it.**
  - ⚠️ **DO NOT MIX TABLE 8 WITH THIS CSV'S TOTALS — different vintages of the
    same cycle.** Table 8 is the budget **as adopted December 2022**
    (2023–26 = **$7,192.5M**); this CSV is the budget **as since adjusted**
    (2023–26 = **$9,216.8M**, +28%). Applying Table 8's *ratio* to the CSV's
    *total* silently blends the two. Table 8 is also **coarser** — its category
    is "Active Pathways **and** Roads", which bundles pathways with roadways by
    construction and cannot be decomposed.
- ⚠️ **A COMPOSITE PROFILE DOES NOT CARRY ITS PROGRAM'S SPEND** (found 2026-09-03).
  `CM-25-0000 Transportation: Neighbourhoods - Renewal` reads **$69.8M** — but the
  neighbourhood renewal program is far larger than that. The composite has been
  **decomposed into 45 standalone named profiles** (`23-40-9033` Ottewell $89.8M,
  `25-25-9506` Dunluce $89.6M, `24-40-9049` Overlanders/Homesteader $66.3M,
  `23-40-9032` McCauley $64.5M, `23-40-9031` Baturyn $45.0M, …) filed under the
  **`Neighbourhoods` service, not `Roads`** — so the composite holds only the
  unallocated remainder. Summing `CM-25-0000` alone under-counts by roughly
  **$475M**. For scale, the Dec-2022 budget book's Appendix A still showed this
  profile at **$545.7M**; individual projects graduate out of the composite as
  they are scoped.
  ⚠️ **This is nastier than the keyword-matching trap above**, because it punishes
  doing the obvious right thing: reaching for the one profile the City *names*
  after the program. **Before treating any composite total as complete, sum its
  standalone descendants and compare.** Same family as
  `check-where-the-value-can-be-wrong` — the number looks authoritative precisely
  where it cannot be checked.
- **The endpoint is byte-stable** (two fetches identical, 2026-08-21) but is
  generated per request, so the digest hashes **sorted** rows — a server-side
  reorder must not read as a budget change.
- ⚠️ **`approved` is a BUDGET, not spend.** These are approved profile amounts
  across a multi-year cycle, not cash out the door in any given year, and the
  2027+ rows are carry-forward. Never sum a `fiscal_year` slice and call it
  annual spending.
- ⚠️ **This is the CAPITAL side and §18 is the OPERATING side. Never sum them.**
  Same rule, same reason, as `city_unit_costs.json`'s `_two_bases`.

## 20. Schools + amenity distance (grid columns, added 2026-08-23)

Feeds `value_grid.json`'s `dist_lrt_m` / `dist_school_m` — road-network metres
from a cell to the nearest LRT station and catchment school. Built by
`src/load_schools.py` + `src/amenity_distance.py`; the station set comes from
`load_transit.derive_lrt_stations`. Design + the locked calls:
`docs/SPEC_development.md` "Amenity distance", `docs/DECISIONS.md` 2026-08-23.

### Sources
| dataset | id | rows | fetched |
|---|---|---|---|
| EPSB School Locations | `996c-239n` | 225 | `download_data.py --only schools_public` |
| Edmonton Catholic Schools (Current) | `gfxq-u8uu` | 97 | `--only schools_catholic` |
| LRT stations | — | 30 | derived from the GTFS already on disk (§9) |
| Road graph | `9j8t-zm52` | 39,515 walkable | the roads file the services lens uses (§7) |

Both school datasets carry `latitude`/`longitude` (zero nulls, 2026-08-23) and a
grade field, and **their schemas disagree**: EPSB has `sch_type` (`EL`/`EJ`/`JR`/
`SR`/`SP`/…) plus a free-text `grades`; ECSD has `grade_level` (`Elementary`,
`Junior`, `Senior`, `Outreach`, and comma-joined combinations) plus
`grades_offered`. `load_schools` harmonizes them; neither field is parsed as text.

### ⚠️ Coverage gap — this is NOT every school in Edmonton
The portal publishes the two public boards and nothing else. **Private, charter,
and francophone (Conseil scolaire Centre-Nord) schools are absent**, so
`dist_school_m` overstates distance for any block whose nearest school is one of
them. Never label the column "distance to the nearest school".

**⚠️ AND IT CANNOT BE CLOSED FROM DATA WE HOLD — probed three ways 2026-08-23:**

1. **The property/assessment roll cannot say what anything IS.** A parcel carries
   account number, address, `lot_size`, `Total Gross Area`, `year_built`,
   `zoning` and value — and `legal_description` is `Plan / Block / Lot` only.
   **Zero of 439,685 rows mention "school"** in any field. A private school and a
   warehouse differ only by zone code.
2. **Zoning does not substitute.** The institutional-ish zones are `PS` (751
   parcels), `PSN` (949) and `US` (**1**) — `US` being the zone schools nominally
   sit in, which is by itself proof the per-property `zoning` field is not where
   that fact reliably lives (the same lesson as the 2026-08-01 polygons-not-field
   reversal). Even clean, "institutional land" is hospitals, fire halls, places of
   worship and community leagues — not schools.
3. **The portal has no such dataset.** A catalogue search for `school` returns
   the two boards, their catchment areas, ward boundaries, building footprints
   and historical vintages — nothing private, charter or francophone. Alberta
   publishes lists that DO cover them (*Alberta's francophone regional
   authorities and schools*, *Alberta accredited international schools*) but as
   **PDFs**, not addressable rows.

**The remedy is manual, not blocked** — transcribe + geocode the provincial PDF
list; `amenity_distance` takes any point frame. ⚠️ **A hand-built list would go
STALE SILENTLY** while the two board feeds refresh weekly. Open in
`docs/ANALYSIS_BACKLOG.md` §13.

### Known Quirks
- ⚠️ **19 rows are city-wide programs, not neighbourhood schools**, and they sit
  in the same table as the catchment ones: EPSB `sch_type == 'SP'` (15 — the four
  Learning Store storefronts, Glenrose Hospital, Metro Continuing Ed., AB School
  for Deaf, Braemar, Aspen Program, L. Y. Cairns, …) and ECSD
  `grade_level == 'Outreach'` (4 — the CCAC centres). Including them would put a
  fake "school nearby" on downtown and hospital cells. Excluded by **enumerated
  category** in `load_schools`; an unknown category is KEPT and logged.
- ⚠️ **The 33 GTFS LRT "stations" include a tail track and two bus-garage
  platforms** (`Heath Sciences Tail Track`, `DL Macdonald Platform`,
  `Kathleen Andrews Platform`). They sit on the alignment and take a scheduled
  time on every trip, so trip counts do NOT separate them. What does: a passenger
  station has at least one `location_type == 2` **street entrance** child, and
  those three have none. 30 stations survive. ⚠️ **The 58 `location_type == 1`
  stops are a DIFFERENT and wrong set** — that one mixes LRT with bus transit
  centres, and it is what the `transit_stations.json` context dots draw.
- ⚠️ **Railway centrelines are excluded from the road graph on purpose.** Routing
  over them lets a walk travel *along the LRT track* to reach an LRT station.
  Dropping alleys + railways also leaves the graph better connected: 163,841
  nodes at 99.83% in one component vs 186,931 at 99.45% unfiltered.
- **`responsible_party` is NOT filtered here**, unlike `load_roads`. That filter
  exists there because the services lens measures what the City maintains; a
  provincial or private road is still walkable, and excluding it carves holes.
- **440 of 439,685 properties (0.1%) cannot reach any amenity** over the graph —
  they sit in one of the 17 disconnected fragments. They emit `null`, never a
  large sentinel a filter would read as a real "far away".
- **Points snap to the nearest graph NODE, not the nearest point on an edge.**
  Measured over 20,000 real properties: median 3.5 m of excess, p90 35 m, p99
  67 m, 0.19% over 100 m. It always ADDS distance, so the error direction
  under-claims proximity.
- ⚠️ **Road centrelines are a walk PROXY, not a walkshed.** Sidewalks, river-valley
  trails, shared-use paths and pedestrian bridges are not in the source, so a
  block whose real route is a footpath reads as further than it is.
- Distribution on the 2026-07-06 snapshot: `dist_lrt_m` median 5,346 m per cell,
  **554 cells (1.6%) within 600 m**; `dist_school_m` median 982 m, **37.8% within
  800 m**. Network/euclidean ratio to LRT: median **1.36**.

## 21. Alberta FIR Schedule MR — the filed taxable base (roll-year guard, added 2026-08-25)

**Source:** Alberta Municipal Affairs — Municipal Financial and Statistical
Data (FIR/SIR), `https://open.alberta.ca/opendata/municipal-financial-and-statistical-data`
— the **same workbooks** `scripts/fetch_fir_debt.py` already downloads for
Schedule AA (§11). That script reads one sheet of 51; this reads three more.
**Fetch:** `scripts/fetch_fir_tax_base.py` → committed `data/fir_tax_base.json`.
**Manual, reviewed input** (the mill-rates / `fir_debt_series` pattern): NOT part
of the weekly refresh. Re-run when a new financial year publishes, eyeball the
diff, commit. **Licence:** Open Government Licence – Alberta.

**What it holds** — Edmonton (FIR code `0098`), per year, from three sheets:
`MR(1)-Tax Levy`, `MR(2)-Assessment`, `MR(3)-Mill Rate`. These are what the
City **filed with the province**, so they are an external anchor on numbers the
project otherwise only models.

| year | filed residential taxable base | filed municipal levy (all classes) |
|---|---|---|
| 2023 | $131,284,317,914 | — |
| 2024 | $134,439,557,008 | — |
| 2025 | $148,128,818,480 | $2,297,399,678 |
| 2026 | $160,372,669,990 | $2,509,075,991 |

✅ **`MR(2)` is the TAXABLE base by construction, and the fetcher asserts it**
(`check_internal_consistency`): `assessment × MR(3) rate` reproduces `MR(1)`
levy to **±0.0000%** for Residential, Farmland and Non-Residential. ✅ **`MR(3)`
matches `data/mill_rates.json` exactly** (2026: Residential `7.7419`,
Non-Residential `25.2216`) — independent confirmation our rate inputs are right.

**Why it exists: the roll year is not recoverable from Socrata metadata.**
Edmonton left `Period of Coverage` reading `2025-01-01 to 2025-12-31` for the
whole 2026 roll, so `check_year_alignment.py` — which parsed that string —
reported "aligned" while the pipeline billed a 2026 roll at 2025 rates.
`scripts/check_roll_year_against_fir.py` measures the parcels instead:
residential land is barely exempt, so our residential base lands within ~1% of
the filed base for the right year and ~10% off for a neighbouring one.

### ⚠️ Known quirks
- **The buckets are NOT 1:1 with our tax classes.** `MR(2)` column [10] is
  *"Other (including annexed, vacant, total minimum tax, etc.)"*, **not** "Other
  Residential" — but Edmonton has no apartment slot in Schedule MR and files
  that sub-class there. Established from the **implied rate** (levy ÷
  assessment = `8.2872`, within 1.0% of our Other Residential `8.2064`), not
  from the label. ⚠️ **Only `residential` is safe to compare directly**, and it
  is the only column the year guard uses.
- **Machinery & Equipment is assessed and NOT levied.** 2026: $759,582,941 at a
  `0.0000` rate → $0. Edmonton levies no municipal tax on M&E and our roll has
  no such class, so it cannot enter a levy comparison — but it does make our
  assessment base look ~$760M *smaller* than the province's.
- **The newest year arrives in `YYYY_tax_rates.xlsx`**, ahead of the full
  `YYYY_financial_year.xlsx`. `discover_resources` accepts both and prefers the
  financial workbook when both exist.
- **Column positions are checked, not trusted.** `_check_header` raises if
  Schedule MR's headers stop matching the expected substrings, rather than
  reading a shifted column blind.
