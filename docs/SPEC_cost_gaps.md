# SPEC — cost side: what is closest, what is biggest, and what data is missing

**Status: inventory, 2026-11-16 (S248). Nothing here is built and no served
number changed.** Peter's ask: for the cost options that are closest to
finishing or take the largest share of the budget, say what data is actually
missing, and queue the answers as report prompts.

This file is in the Claude web synced set (`docs/SPEC_*.md`). §5 holds prompts
written to be pasted into a chat in that Project.

Read with: `docs/SPEC_breakeven.md` (the frame: one register entry per cost
category, operating basis first, coverage shown wherever a number is),
`docs/SPEC_services.md` (what is built), `docs/REPORT_CLAIMS.md` (what the
report may already say about roads).

## 0. How this was measured

- **Budget:** Socrata `da9s-v9j8` (Approved Operating Budget, Expenses), queried
  2026-11-16, `fund_type = 'Tax Supported'`. FY2026 total **$4,047.1M**, 145
  programs. FY2025 total $3,855.9M, 144 programs (ties to `SPEC_breakeven.md`
  §4a).
- **Shares below are of the full FY2026 tax-supported total.** The break-even
  lens's locked denominator is operating-only on FY2025 ($3,055.2M, coverage
  15.5%). It was not recomputed for FY2026 here.
- **Datasets:** shortlisted with the `edmonton-open-data-landscape` search
  tool, then each one checked live on `data.edmonton.ca` on 2026-11-16: row
  count, last update, the columns a driver needs, and whether its
  neighbourhood names join to the pipeline's 406. A search hit is a shortlist
  entry, not proof; the facts in §3 are the live checks.
- **Earlier research rounds were read**, so a question already closed is marked
  closed and not re-asked (`/home/opc/research/edmonton-tax-viz/road_cost/road_cost_rounds.md`).
- **Not checked:** anything outside `data.edmonton.ca` (the police, library,
  transit and EPCOR sites). Those appear in §4 as questions, not findings.

## 1. The budget by branch, largest first (FY2026, tax-supported)

| $M | share | branch | state in this project |
|---|---|---|---|
| 682.8 | 16.9% | Capital Project Financing (debt charges $297.0M, pay-as-you-go $230.3M, other debt) | not modelled; no driver |
| 633.1 | 15.6% | Edmonton Police Service | not modelled; no driver; an editorial decision comes first (`SPEC_breakeven.md` §4a) |
| 504.7 | 12.5% | Edmonton Transit Service (bus and LRT $467.7M, DATS $36.9M) | **built**, full build only: bus and LRT allocated by scheduled departures |
| 304.4 | 7.5% | Parks and Roads Services (parks and forestry $82.0M, snow $74.2M, mobility infrastructure $73.3M, safe mobility $34.0M, technical and regulatory $27.9M) | **roads part built** and public ($9.32/m operating); parks not modelled |
| 279.2 | 6.9% | Fire Rescue Services (operations and training $217.5M) | demand map built; cost allocation **retired by decision** 2026-09-05 |
| 174.4 | 4.3% | Neighbourhood Renewal | lifecycle roads rate built ($50/m); compared with this money once (R10, R12) |
| 168.8 | 4.2% | Corporate Expenditures | not a place-based service |
| 128.9 | 3.2% | Sport and Recreation (facility operations $115.0M) | not modelled |
| 125.5 | 3.1% | Development Services | not modelled |
| 119.0 | 2.9% | Social Development | not modelled; no spatial driver expected |
| 98.8 | 2.4% | Explore Edmonton | not a place-based service |
| 96.2 | 2.4% | Fleet and Facility Services | internal service |
| 75.5 | 1.9% | Edmonton Public Library | not modelled |
| 69.6 | 1.7% | Community Standards (enforcement $46.7M, animal care $22.9M) | not modelled |

The first twelve rows are the twelve largest branches. Library and Community
Standards are listed because a candidate driver was found for each.

Outside the tax-supported fund, so outside the coverage denominator: Waste
Services $241.5M (utility, fee-funded). Stormwater and water are EPCOR's and
are modelled from rates (`SPEC_utilities.md`).

Modelled today on the operating basis: **$473M** (transit $436.6M, roads
$16.9M, bike $19.7M).

### Three statements in the repo that this pass found stale

1. **"Alley Renewal $174.4M"** (`SPEC_breakeven.md` §4a, `TODO.md`). That is
   the publisher's FY2025 program name for the whole Neighbourhood Renewal
   branch, already recorded as `DATA_ISSUES.md` F. FY2026 splits it:
   Neighbourhood Renewal $158.1M, Alley Renewal Capital $22.3M, less
   microsurfacing $6.0M. Alleys are about 13%. The spec's point stands (it is
   per-neighbourhood renewal money on the lifecycle basis); the name misleads.
2. **"Parks is NOT its own line"** (`TODO.md`). True for FY2025. FY2026 has
   `Parks and Urban Forestry` at $82.0M. No crosswalk between the FY2025 and
   FY2026 program names is published, so which FY2025 dollars it replaces is
   not known.
3. **"The project has NO population-by-hood source"** (`TODO.md`;
   `SPEC_breakeven.md` Task 1b). The pipeline ingests none, but a dwelling
   model has shipped since (`FINDINGS_road_per_dwelling.md`) and the portal
   carries the 2021 census by neighbourhood (§3.4).

## 2. Ranked: closest to finishing, weighted by size

"Closest" means the driver is in hand or one ingest away, and the missing piece
is one named fact. The detail for each is in §3.

| rank | option | $M | what exists | the one thing missing |
|---|---|---|---|---|
| 1 | Neighbourhood renewal (roads lifecycle, compared with spend) | 174.4 | per-profile spend in `data/capital_budget.csv`; road metres; alley centrelines found | what share of a reconstruction is road, alley, sidewalk, lighting, drainage. Two council documents that may hold it are blocked to scripts and have not been opened by a person |
| 2 | Snow and ice | 74.2 | a blended $/lane-km rate in the roads figure; a priority-class route map found | what each priority class costs, and a primary source for the roads share of the programme |
| 3 | Parks and urban forestry | 82.0 | nothing built; park polygons and a tree inventory found | how the $82.0M divides between mowed parks, natural areas and trees |
| 4 | Population per neighbourhood (an input, not a cost) | — | 2021 federal census by neighbourhood found; the dwelling model | growth since 2021 |
| 5 | Transit | 467.7 | built on scheduled supply | boardings by stop or route |
| 6 | Fire | 279.2 | demand map; station points | what a station costs, and its first-due area |
| 7 | Road maintenance beyond the $9.32 floor | 73.3 | the floor; lane-km by road class (2020) | how much more an arterial lane-km costs to maintain than a local one; what is inside "Mobility Infrastructure Services" |
| 8 | Community standards enforcement | 46.7 | nothing built; complaints by neighbourhood found | cost per complaint type |
| 9 | Police | 633.1 | nothing | a decision, then calls for service by area |
| 10 | Recreation facilities and libraries | 190.5 | facility and branch points found | cost and users per facility, by where users live |
| 11 | Debt and pay-as-you-go | 682.8 | capital profiles by fund type in `capital_budget.csv` | outstanding debt by project |

Ranks 1–3 are the ones that could close. Rank 4 unblocks several others. Ranks
9–11 are the large ones, and data alone does not unblock them.

## 3. Per option: what is in hand, what was found, what is missing

### 3.1 Neighbourhood renewal — $174.4M, lifecycle basis

- **In hand.** `data/capital_budget.csv` carries per-profile renewal spend. 14
  full-reconstruction profiles covering 24 neighbourhoods run 1.65× the City's
  published $1,900/m renewal figure, 1.38× with alley work taken out
  (`REPORT_CLAIMS.md` R10; `FINDINGS_nrp_reconstruction_cross_check.md`).
- **Found, not ingested.**
  - `dtuf-twc2` Neighbourhood and Alley Renewal: 137 rows, 133 neighbourhoods,
    all 133 names join. Type (Reconstruction 57, Pavement Renewal 74, Alley
    Reconstruction 6) and construction years. ⚠️ The newest end year is
    **2023**, although the table was touched 2026-11-09. It dates past
    projects; it is not a schedule.
  - `x2x8-m84m` Alley centrelines: 11,523 segments with class and surface
    type. Last updated 2021-06-24. The pipeline excludes alleys by decision,
    so alley metres per neighbourhood have never been computed.
- **Missing.**
  1. The sub-asset split of a reconstruction: road, alley, sidewalk, street
     lighting, drainage. A research round closed this negative on 2026-09-17:
     the City publishes no such table. Two council attachments may hold it,
     *Completed NRP Projects 2009–2022* (escribe `DocumentId=164273`) and the
     City Auditor's Neighbourhood Renewal audit (`DocumentId=286947`). Both
     return 403 to a script (re-tested 2026-11-16) and nobody has opened them
     in a browser. Without the split the observed $/m cannot become a rate.
  2. Renewal projects after 2023, by neighbourhood and year.
  3. A current alley inventory. The 2021 file may be enough for a first cut,
     which would let the $22.3M alley line be allocated by alley metres.

### 3.2 Snow and ice — $74.2M, operating basis

- **In hand.** The snow half of the $9.32/m roads rate: $3,350 per lane-km,
  from a programme total that is corroborated and a 55% roads share that rests
  on one secondary source (R6). The rate is blended over a network that
  includes priority-cleared arterials (`ASSUMPTIONS.md` B4).
- **Found, not ingested.** `8pdx-hfxi` Snow and Ice Clearing Route Status:
  2,240 segments with line geometry, updated 2026-11-05. By priority, linear
  km: P1 386, P2 1,670, P3 286, P4 3,856, total 6,255 (one 57 km segment has
  no priority). The pipeline's collector-plus-local length was 3,654 km on
  2026-09-08, so P4 looks like the residential network. That match is not
  tested.
- **Missing.**
  1. Cost or effort by priority class. The dataset's `num_passes` and
     `serv_hrs` fields are live during events, so a winter of snapshots would
     give passes per class. A published service level per class would give a
     weight without waiting a winter.
  2. A primary source for the roads share of the programme (against sidewalks,
     pathways, bus stops).
- **What it would change.** The snow term would be allocated by the priority
  class of the roads in each neighbourhood, not by a citywide average, and B4
  would close.

### 3.3 Parks and urban forestry — $82.0M, operating basis

- **In hand.** Nothing.
- **Found, not ingested.**
  - `gdd9-eqv9` Parks: 1,197 polygons with area and class. Active parks total
    67.8 km². By class, all statuses: natural area 20.1 km², city park 18.6,
    school and community park 17.2, district activity park 5.0, urban village
    3.4, pocket park 2.4.
  - `eecg-fc54` Trees: 489,543 rows, and every one of its 389 neighbourhood
    names joins. Location type: park 185,762 trees, boulevard 163,133.
  - `9nqb-w48x` Playgrounds (661) and the sports-field tables.
- **Missing.**
  1. How the $82.0M divides: turf and horticulture, forestry, natural areas,
     playgrounds and fields. Area alone would charge a natural area like a
     mowed park.
  2. A ruling on scope. City parks and river-valley parks serve the whole city
     (`SPEC_breakeven.md` §2b, network-shared). Pocket, urban village and
     school-and-community parks are the site-bound part.
- **Risk to name.** 48 neighbourhoods are set aside, 23 of them as river
  valley, natural area or parks. A parks cost map will be highest where the
  project draws grey.

### 3.4 Population per neighbourhood — an input

- **Found.** `xgkv-ii9t` 2021 Federal Census, Households and Families: 279
  neighbourhoods, 996,485 persons in private households. 277 names join (the
  two that do not: OLIVER, HORSE HILL NEIGHBOURHOOD 1A). 225 of the pipeline's
  226 residential neighbourhoods have a row (missing: CRYSTALLINA NERA EAST).
  Also `wpfd-8bii` (age and gender) and `522q-3877` (2019 municipal census,
  dwelling status).
- **In hand.** The dwelling model: 552,113 dwellings across 351
  neighbourhoods on 2026-09-03 (`FINDINGS_road_per_dwelling.md`).
- **Missing.** Growth since 2021. Greenfield neighbourhoods are undercounted,
  and those are the ones at the top of the Development lens (D2). Comparing
  the dwelling model with the census would size the drift.
- **Unblocks.** The per-capita residual (`SPEC_breakeven.md` §8 #4), any
  per-capita allocation of police, recreation or libraries, and a per-capita
  form of the road-per-dwelling finding (R15).

### 3.5 Transit — $467.7M (bus and LRT), built on scheduled supply

- **In hand.** Scheduled departures per stop from GTFS; the budget allocated by
  them. The model's numerator is $436.6M (2025 budget, ETS 2024/2025 Annual
  Service Plan); the portal's FY2026 line is $467.7M.
- **Missing.** Boardings by stop or by route. The portal has citywide monthly
  totals only (`wj6v-epas`, 93 rows). Without boardings the map shows where
  service is scheduled, not where it is used, and decision §8 #6 (transit is
  network-shared) stays open.

### 3.6 Fire — $279.2M

- **In hand.** Dispatched events per acre (a demand map), station points.
- **Why there is no cost map.** The roads-plus-fire cost composite was retired
  2026-09-05: the budget pays for standing capacity and does not move with
  dispatches (`FINDINGS_services_cost_lens_verdict.md` §3). Do not re-wire it.
- **Missing, if a capacity-based term is ever wanted.** Staffing or apparatus
  per station, and each station's first-due area. Neither was found on the
  portal.

### 3.7 Road maintenance beyond the floor — $73.3M mobility infrastructure

- **In hand.** $5,970 per lane-km (FY2017) applied to centreline metres,
  published as a floor (R5, R11). Lane-km by road class from the City's 2020
  inventory table (`FINDINGS_road_class_inventory.md`; R7).
- **Found.** `rxke-mcvd` streetlights: 124,003 points, 123,905 City-owned,
  with wattage. `4feb-tv8p` curbs and sidewalks: 554,557 segments (2021).
- **Missing.**
  1. The maintenance-cost ratio between an arterial lane-km and a local one.
     It is unpublished, and the floor claim turns on it (R11).
  2. What sits inside "Mobility Infrastructure Services". FY2025 had
     `Infrastructure Operations` ($128.2M) and `Infrastructure Maintenance`
     ($56.9M); FY2026 has neither name, so the portal no longer shows a line
     that reads as road maintenance.

### 3.8 Community standards enforcement — $46.7M

- **Found.** `ypje-j649` Bylaw Complaint Details (689,414 rows, by
  neighbourhood, updated 2026-11-15) and `q7ua-agfg` 311 Requests (3.5M rows).
- **Missing.** Cost per complaint type. Small, and complaint counts carry the
  same reporting-bias problem as crime data.

### 3.9 Police — $633.1M

Not a data gap first. Any spatial driver produces a policing-cost map, and the
driver choice does the arguing (`SPEC_breakeven.md` §4a; `ANALYSIS_BACKLOG.md`
§14). The city portal carries station points only. If Peter decides to reach
it, the cheapest honest form is per capita through the residual, which needs
§3.4 and nothing else.

### 3.10 Recreation facilities and libraries — $115.0M + $75.5M

- **Found.** `nz3t-vyg3` Recreation Facilities (107: 19 recreation centres, 22
  arenas, 5 outdoor pools), `jn25-zspi` Public Libraries (22 branches).
- **Missing.** Operating cost per facility, and users by home neighbourhood.
  Without the second, these are network-shared and belong in the residual.

### 3.11 Debt and pay-as-you-go — $682.8M

- **In hand.** `data/capital_budget.csv` (profiles by fund type; $3.50B of
  approved tax-supported debt across the file) and `552h-hjwj` Capital
  Projects (219 projects with a location, 216 with a neighbourhood).
- **Missing.** Outstanding debt by project. The budget says what is borrowed
  for; nothing found says what is still owed on what. Service on capital
  already built has no per-neighbourhood driver until that exists.

## 4. Data to get, in one list

Each is a single named fact or table. Status as of 2026-11-16. None is recorded
as put to the City.

| # | what | from | unblocks | status |
|---|---|---|---|---|
| A1 | Sub-asset cost split of a neighbourhood reconstruction | escribe documents 164273 and 286947, opened in a browser; then the City | §3.1 | searched 2026-09-17, not published as data; the two documents are unread |
| A2 | Maintenance-cost ratio, arterial against local lane-km | City (Parks and Roads) | §3.7, R11 | unpublished |
| A3 | Renewal projects 2024 onward, by neighbourhood | City open data (`dtuf-twc2` stops at 2023) | §3.1 | not searched |
| A4 | Snow service level or cost by priority class, and the roads share of the programme | City (Parks and Roads) | §3.2, R6 | share: one secondary source; by class: not searched |
| A5 | Parks and Urban Forestry budget by activity | City (Parks and Roads) | §3.3 | not searched |
| A6 | Boardings by stop or route | ETS | §3.5 | not on the portal; not searched elsewhere |
| A7 | Operating cost and visits per recreation facility and library branch | City, EPL | §3.10 | not searched |
| A8 | Program detail under Mobility Infrastructure Services | City open budget | §3.7 | not searched |
| A9 | Outstanding tax-supported debt by capital profile | City (Financial Services) | §3.11 | not searched |

A3–A9 may already be answered in a published report. §5's search prompts look
for that before anyone writes to the City.

## 5. Report prompts

For a chat in the claude.ai Project, after pressing Sync. Two kinds. A
**draft** prompt produces a passage the report could carry from what is
already proven. A **search** prompt looks for a missing fact in public sources.

Rules for every prompt (say "follow `SPEC_cost_gaps.md` §5 rules"):

1. Use only figures in this file, `REPORT_CLAIMS.md` and `web/verified/REPORT_FIGURES.md`.
   Give the row or section beside each figure.
2. Keep each caveat a row carries. State nothing an `X` row withdraws.
3. For a search prompt, every claim needs a primary-source URL, the document
   title and date, and the sentence quoted word for word. If the source is
   secondary, say so. "Not found" is an acceptable answer.
4. End with proposed `REPORT_CLAIMS.md` rows (status, proof pointer) and the
   brief's reply format.

### Draft prompts

- **P1. Coverage.** "Draft the report passage that answers: of what the City
  spends, how much can this project place on a map, and why not more? Use §1
  and §2. Name police, debt and transit by size. Say which parts are a data
  gap and which are a decision."
- **P2. Renewal.** "Draft the passage on neighbourhood renewal: what the City
  budgets, what the roads model requires, and why observed reconstruction
  spend reads above the published rate. Use R10, R12, X9, X10 and §3.1. State
  the one missing fact."
- **P3. Snow.** "Draft the passage on snow clearing: what is in the $9.32
  rate, which half is corroborated, and what a priority-class map would
  change. Use R5, R6, X2 and §3.2."
- **P4. What is not mapped, and why.** "Draft a short passage explaining why
  the project draws no police, fire or recreation cost map. Use §3.6, §3.9,
  §3.10 and `SPEC_breakeven.md` §2b. One paragraph each; no cost figure per
  neighbourhood."
- **P5. Data requests.** "Turn §4 into a one-page request to the City: each
  item in one sentence, what it would let the public see, and the dataset or
  page where it would naturally be published."

### Search prompts

- **P6.** "Find the City's snow and ice service levels by road priority class,
  and any published split of the snow budget between roads and active
  pathways (A4)."
- **P7.** "Find a published breakdown of Parks and Urban Forestry operating
  spending by activity: turf, horticulture, forestry, natural areas (A5)."
- **P8.** "Find any public ETS ridership data finer than citywide monthly:
  by route, station or stop (A6)."
- **P9.** "Find published operating cost or attendance per City recreation
  facility, and visits or circulation per library branch (A7)."
- **P10.** "Find neighbourhood renewal projects scheduled or completed from
  2024 on, by neighbourhood (A3)."

**Do not send a search prompt for A1.** It was asked and answered on
2026-09-17. The next step is a person opening the two escribe documents.

Replies are filed in `/home/opc/research/edmonton-tax-viz/` before anything is
taken from them (`docs/CLAUDE_WEB.md`), and each claim is checked locally.

## Cross-refs

`SPEC_breakeven.md` §2b, §4a, §8 · `SPEC_services.md` · `SPEC_utilities.md` ·
`REPORT_CLAIMS.md` R5–R15, X2, X9, X10, D2 · `ASSUMPTIONS.md` B4 ·
`ANALYSIS_BACKLOG.md` §14 · `DATA_ISSUES.md` F ·
`FINDINGS_nrp_reconstruction_cross_check.md` ·
`FINDINGS_road_class_inventory.md` · `FINDINGS_road_per_dwelling.md` ·
`FINDINGS_services_cost_lens_verdict.md` §3
