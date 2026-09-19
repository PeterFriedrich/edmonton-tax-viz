# Findings — Arterial Roadway Assessments: how Edmonton actually allocates arterial cost

Captured 2026-09-19 (S176). **Retrieved first-hand from `edmonton.ca`, not
relayed.** Prompted by an external precedents report
(`research/edmonton-tax-viz/road_cost/road_cost_precedents_modelling.md`) that
cited the ARA system as evidence, using nine-year-old industry-association
figures while the City publishes current ones one click from the page it cited.

**Why this matters here.** `SPEC_services.md` V1 excludes arterials from
`road_m_per_acre` on the grounds that there is no defensible way to attribute a
shared arterial to an abutting neighbourhood. **The City faces the same problem
and has a published answer: it allocates by AREA, per hectare, per catchment —
never by frontage.** That is external support for the exclusion decision's
reasoning, and it is the first per-hectare arterial cost figure this project has
seen.

⚠️ **It is NOT a drop-in arterial cost layer**, and §5 says why.

## 0. Provenance

| document | URL | retrieved |
|---|---|---|
| ARA landing page | `edmonton.ca/city_government/urban_planning_and_design/arterial-roadway-assessments` | 2026-09-19, HTTP 200, title checked (not a soft-404) |
| **2026 ARA Rates** | `/sites/default/files/public-files/documents/2026-ara-rates.pdf` | 2026-09-19, 2 pp |
| Bylaw 14380, Office Consolidation **May 2026** | `/sites/default/files/public-files/documents/bl14830.pdf` | 2026-09-19, 78 pp |
| Policy & Procedure C507 | `/sites/default/files/public-files/C507.pdf` | 2026-09-19 |
| ARA Annual Reports 2021–**2024** | `/sites/default/files/public-files/<YYYY>-Arterial-Roadway-Assessments-AnnualReport.pdf` | 2026-09-19, 9 pp each |
| ARA Audit (City Auditor) | `/sites/default/files/public-files/21491_Arterial_Roadway_Assessment_Audit.pdf` | 2026-09-19, **not yet read** |

⚠️ **`WebFetch` returns 502 on every `edmonton.ca` URL above; `curl` with
`certifi` returns 200 on all of them.** Same split already recorded for the
Development Impact page (`FINDINGS_road_figures_consolidation.md` L2a) — the page
is live and the fetch tool is the thing that is broken. **Do not record an
edmonton.ca 502 as "unreachable" without trying curl+certifi first**
(`oracle-box-stale-ca-bundle`).

⚠️ **The bylaw's filename transposes its own number** — the link text says Bylaw
**14380** and the file is `bl14830.pdf`. Both spellings resolve
(`Bylaw14380Consolidation.pdf` also returns 200, same 15.2 MB document). Cosmetic,
but it will defeat a filename-pattern guess. The document's own first page reads
*"Bylaw 14380 Office Consolidation … adopted by City Council on September 26,
2006."*

## 1. The basis, verbatim — area, not frontage

ARA Annual Report 2022, p3:

> **"The net assessment owing by a given Developer is the ARA rate in force at
> the time multiplied by the assessable area of the development."**

And the landing page:

> "Each development occurring within the catchment is required to pay an
> assessment based on a **per-hectare rate** under the provisions of a servicing
> agreement."

What the assessment buys, same report, p3:

> "Developers are required to construct or pay for the construction of the **first
> four lanes** of new Arterial Roads that are deemed to have four or six lanes in
> their ultimate design and the **first five lanes** of new Arterial Road that are
> deemed to have five or seven lanes in their ultimate design."

⚠️ **So in growth catchments, arterials are developer-funded up to four or five
lanes — the same "gifted asset" structure as local roads, one tier up.** The City
funds the widening beyond that, and all renewal. Any future statement about who
paid for a neighbourhood's roads must separate these three.

## 2. The 2026 rates, transcribed

Three separate components. **Collapsing them into one number understates the
charge by the signal and dedication rates**, which is what the external report
did.

### 2a. Residential catchments ($/ha)

| catchment | core rate | signal rate |
|---|---:|---:|
| Big Lake | 217,934 | 10,513 |
| Castle Downs Extension | 180,914 | 11,227 |
| Dechene, Donsdale, Jamieson, & Wedgewood | **12,953** | 0 |
| Decoteau | 236,957 | 8,621 |
| Ebbers and Gorman | 235,652 | 7,301 |
| Edgemont | 436,183 | 15,583 |
| Ellerslie | 235,196 | 18,527 |
| Goodridge Corners | 116,745 | 8,377 |
| **Heritage Valley** | **519,212** | 23,887 |
| Horse Hill | 382,343 | 9,248 |
| Lake District | 312,044 | 36,374 |
| Lewis Farms | 348,882 | 14,692 |
| Palisades | 84,113 | 59,531 |
| **Pilot Sound** | **551,757** | 33,133 |
| Riverview | 249,859 | 9,765 |
| Southeast ASP | 267,794 | 12,792 |
| Terwillegar Heights | 47,779 | 0 |
| The Grange | **Under Review** | 50,373 |
| The Meadows | 347,309 | 22,681 |
| **Windermere** | **381,678** | 12,839 |
| **City-Wide Residential Weighted Average** | **299,963** | **11,531** |

⚠️ **`The Grange` core rate is the string `Under Review`, not a number.** Anything
that parses this table must handle a non-numeric cell.

### 2b. Commercial / industrial catchments ($/ha)

| catchment | core rate | signal rate |
|---|---:|---:|
| Aurum & Clover Bar | 146,319 | 3,997 |
| Crossroads | 52,480 | 4,810 |
| Edmonton Energy & Technology Park | 128,093 | 2,551 |
| Maple Ridge & Southeast Industrial | 150,546 | 4,583 |
| Mistatim | 29,470 | 1,132 |
| Place LaRue | 79,945 | 0 |
| Poundmaker | 69,640 | 1,337 |
| Pylypow | 151,356 | 5,600 |
| Rampart | 207,279 | 3,684 |
| Sunwapta | **11,961** | **62,809** |
| Winterburn | 69,390 | 2,885 |
| **City-Wide Industrial Weighted Average** | **120,595** | **3,060** |

⚠️ **Sunwapta's signal rate is 5.3× its core rate** — the only row where signals
dominate. Palisades (residential) is the other outlier at 0.71×. Every other
catchment sits below 0.16×. Transcribed as printed; not investigated.

### 2c. Land dedication rates ($/ha, 2026)

| quadrant | rate |
|---|---:|
| SW | 775,000 |
| SE | 680,000 |
| NW / West | 680,000 |
| NE | 680,000 |
| Crossroads | 400,000 |

The PDF's own header: *"Note that these rates may change over the course of the
year as updated costs are made available to the City and/or there is a change to
the ARA Bylaw."* **This is a live, revised-in-year figure, not an annual
constant.** Contact given as `development.coordination@edmonton.ca`.

## 3. ⚠️ Policy C592 — the City rebates property tax into industrial servicing

**All eleven** industrial catchments carry an asterisk, defined on the rates PDF
p2:

> "The ARA rates in this particular Catchment have been reduced as per City Policy
> C592 i.e. the **Industrial Infrastructure Cost Sharing Program**. Under this
> Program, the City contributes a portion of its **municipal property tax revenue**
> from eligible ARA Catchment areas towards reducing the cost of development
> assessments."

⚠️ **This is a tax expenditure targeted at industrial land, and it is directly
relevant to a revenue-per-acre lens**: municipal levy collected from industrial
catchments is recycled into reducing those same catchments' servicing charges. A
revenue-per-acre figure for industrial land is therefore **gross of a rebate that
residential land does not receive**, and the published industrial weighted average
($120,595/ha) is a **post-rebate** number — the pre-rebate one is not published.

**Not quantified here.** The size of the contribution, its budget line, and
whether it is capped are all in C592, which has not been read. **This is the
single most actionable thing in this document** and it is new to the project —
`C592` appears nowhere in `docs/` or `data/`.

## 4. Scale, from the annual reports

| | 2022 | 2024 |
|---|---:|---:|
| ARAs collected, residential | $298,074,884 | $351,613,098 |
| ARAs collected, industrial | $4,012,392 | $1,441,942 |
| **— of which cash (residential)** | $12,920,893 | **$22,052,860** |
| — waivers (residential) | $195,187,198 | $146,605,616 |
| — offsets (residential) | $89,966,793 | $182,954,622 |
| Remaining unclaimed arterial cost, residential | **$1,289,709,505** | — |
| Remaining unclaimed arterial cost, industrial | **$752,486,954** | — |

⚠️ **Only 6.3% of 2024's residential collections was cash** ($22.1M of $351.6M);
the rest is waivers and offsets between developers. **"Collected" here does not
mean money moved.** Anyone quoting the $351.6M as City revenue would be wrong —
it is a clearing total for a cost-sharing ledger.

**~$2.04B of arterial construction remained unbuilt and unclaimed across
catchments at end-2022.** Largest: Horse Hill $399.8M, Edmonton Energy &
Technology Park $527.5M (industrial), Decoteau $248.8M.

## 5. ⚠️ Why this is NOT an arterial cost layer for the metric

Four reasons, each sufficient on its own:

1. **Growth catchments only.** ARA applies where Bylaw 14380 defines a catchment
   — new/greenfield areas. **Mature Edmonton has no ARA rate at all.** A metric
   built on it would be null for most of the city and would read as "mature
   neighbourhoods impose no arterial cost," which is false.
2. **One-time capital, not lifecycle.** The rate buys initial construction of the
   first four or five lanes. It contains no O&M, no renewal, no winter. It is not
   commensurable with `roadway_om_renewal`'s $50/m/yr, and summing them would mix
   bases exactly as `city_unit_costs.json._two_bases` forbids.
3. **Assessable area ≠ our acreage.** The denominator is the *assessable area of
   the development* inside a *catchment boundary*. Our denominator is
   neighbourhood polygon acres. The two are not the same geography and no
   crosswalk is published.
4. **Developer-paid, not City-paid.** It is a cost-share among developers, not a
   municipal expenditure. A cost-to-serve lens measuring what the *City* spends
   must not count it.

**What it is legitimately good for:** confirming the area-allocation principle
(§1), sizing the arterial capital burden of growth areas (§4), and the C592
finding (§3).

## 6. An indicative cross-read against the BILD study

`FINDINGS_growth_servicing.md` §4 holds BILD's claim of **$3.2B private upfront
capital in Heritage Valley + Windermere, ~$2.4B of it roads**, and our own
measured polygon acreages for the same two areas.

| | acres | ha | 2026 core+signal rate | implied |
|---|---:|---:|---:|---:|
| Heritage Valley | 5,536 | 2,240 | $543,099/ha | $1.22B |
| Windermere | 3,734 | 1,511 | $394,517/ha | $0.60B |
| **combined** | **9,270** | **3,751** | — | **$1.81B** |

**$1.81B of arterial alone, at 2026 rates, against BILD's $2.4B for all developer
road contributions.** Directionally consistent, and it makes BILD's figure look
plausible rather than inflated — which is worth recording because this project
holds the BILD study as an advocacy counter-case and has so far only checked its
*revenue* side.

⚠️ **INDICATIVE ONLY — do not quote this as a reconciliation.** Three mismatches,
all unquantified: catchment boundary ≠ our neighbourhood polygons; *assessable*
area ≠ gross polygon area (and is strictly smaller, so this **overstates**); and
2026 rates applied to construction spread over ~20 years of history, against a
nominal BILD total (which **also** overstates). Both known biases push the same
way, so **$1.81B is a ceiling on the comparison, not an estimate.**

## 7. What the external report got wrong

Recorded because it is the reason this retrieval happened.

| claim | report (cited as "2017 UDI figures") | City, 2026 |
|---|---|---|
| residential range | $14,111 – $263,894/ha | **$12,953 – $551,757/ha** — **9 of the 19 numeric rows sit above the report's stated maximum** |
| residential weighted average | ~$170,760/ha | **$299,963/ha** (1.76×) |
| "overall roadway levy" | ~$140,264/ha | **no such figure** in the City table |
| components | one rate | **three** (core, signal, land dedication) |

⚠️ **The pattern, not the numbers, is the lesson.** The report reached a live City
primary through a nine-year-old **developer industry association** relay — UDI,
the same advocacy side as the BILD study the report elsewhere correctly labels a
counter-case — while the current City figures sat one link from the page it cited.
Round 3's lesson was *"a dead relay is not a dead source"*
(`road_cost_rounds.md`); **this is the inverse: a live source reached only through
a stale relay.** `verify-relayed-external-advice`, eleventh instance.

## 8. Reproduction

```python
# City of Edmonton, 2026 ARA Rates (2 pp), retrieved 2026-09-19.
# Residential core rates, $/ha. 'The Grange' is the string "Under Review".
res = {
    "Big Lake": 217934, "Castle Downs Extension": 180914,
    "Dechene, Donsdale, Jamieson, & Wedgewood": 12953, "Decoteau": 236957,
    "Ebbers and Gorman": 235652, "Edgemont": 436183, "Ellerslie": 235196,
    "Goodridge Corners": 116745, "Heritage Valley": 519212, "Horse Hill": 382343,
    "Lake District": 312044, "Lewis Farms": 348882, "Palisades": 84113,
    "Pilot Sound": 551757, "Riverview": 249859, "Southeast ASP": 267794,
    "Terwillegar Heights": 47779, "The Meadows": 347309, "Windermere": 381678,
}
PUBLISHED_WA = 299963          # City-Wide Residential Weighted Average, p1
assert len(res) == 19, "20 residential rows, one ('The Grange') is non-numeric"
assert min(res.values()) == 12953 and max(res.values()) == 551757

# The published average is WEIGHTED by assessable area, which the City does NOT
# publish -- so it cannot be recomputed, only bounded. Assert the bound, and
# assert it is NOT the simple mean (a reader who assumes it is will be ~10% low).
assert min(res.values()) < PUBLISHED_WA < max(res.values())
simple = sum(res.values()) / len(res)
assert abs(simple - 271858) < 1
assert PUBLISHED_WA > simple, "big catchments carry the high rates"
assert 1.09 < PUBLISHED_WA / simple < 1.11

# S7: the external report's figures, against the City's own.
assert PUBLISHED_WA / 170760 > 1.75          # report's WA is 1.76x low
assert 263894 < max(res.values())            # report's stated max is below 9 of 19 rows
assert sum(1 for v in res.values() if v > 263894) == 9

# S6: the indicative BILD cross-read. Both known biases OVERSTATE, so this is a
# ceiling, not an estimate -- the assert pins the direction, not the value.
AC = 0.404686
hv = 5536 * AC * (519212 + 23887)            # FINDINGS_growth_servicing.md S4 acreages
wi = 3734 * AC * (381678 + 12839)
assert 1.80e9 < hv + wi < 1.82e9, (hv + wi)
assert hv + wi < 2.4e9, "must stay under BILD's all-roads total to be consistent"
print(f"ARA resid WA ${PUBLISHED_WA:,}/ha (simple mean ${simple:,.0f}); "
      f"HV+Windermere arterial ceiling ${(hv+wi)/1e9:.2f}B")
```

## 9. Follow-ups

1. **Read Policy C592** (§3). Quantify the industrial tax rebate — size, budget
   line, cap. `ANALYSIS_BACKLOG.md` row.
2. **Read the ARA Audit** (City Auditor, May 2022, retrieved but unread). A City
   Auditor report on this program may state the rate-setting method, which would
   make §2's figures reproducible rather than merely transcribed.
3. **Do not build an arterial cost column from this** without reopening
   `SPEC_services.md` V1 — §5 lists four blockers.
