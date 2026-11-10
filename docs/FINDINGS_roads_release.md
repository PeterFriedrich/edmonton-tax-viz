# FINDINGS — the public roads lens, before the first release

**Run:** 2026-11-10 (S242), **Fable 5.2** (`claude-fable-5-2`), from
`docs/FABLE_AUDIT_roads_release.md`. The builders and every audit since S172
were Opus; S149 and S172 were Fable 5.1.

**Scope:** the four public roads surfaces (Services → Roads, Roads cost, Roads
cost — lifecycle; Ratio on road metres), their rates, metres, copy and the
share-of-levy panel. The levy itself is taken as given
(`docs/FABLE_AUDIT_levy_as_revenue.md` owns it). Full-build layers are out.

**Every claim is tagged.** *(measured)* = computed this session, on the served
file `web/data/neighbourhood_value_per_acre.geojson` (refresh commit `2eaed4e`,
2026-11-09, 406 neighbourhoods, 48 set-aside, 358 published), on
`load_roads` re-run on `data/raw/roads.geojson` (pulled 2026-11-02), or on a
primary source re-fetched 2026-11-10. *(read)* = taken from a repo document or
from the code, not re-derived. Nothing here changes code, data or copy, and no
replacement rate is proposed.

**Headline.** No roads level is UNSOUND and **no shipped roads number was
found wrong.** Nothing on the roads lens has to block the release. Two copy
calls are worth settling first because they are cheap and public (§9, items
1–2). The largest unstated effect is the arterial exclusion on the Ratio view
(L3).

The Development appendix (§10) did find things: **one shipped Development
number is wrong** (CHAPPELLE's units since 2009 are 28 low, 0.4%, because the
City renamed a string and a name-keyed correction stopped matching), and the
grid blurb's "yet … lag geocoding" is unsupported on every state, not only the
default one.

## 0. The hinge — confirmed

*(read, `web/index.html`)* The public build shows exactly these road surfaces:

| Surface | Served column | Gate |
|---|---|---|
| Services → Roads | `road_m_per_acre` | `SERVICES.roads.pub: true` |
| Services → Roads cost | `cost_roads_ops_per_acre` | `SERVICES.roadscost.pub: true` |
| Services → Roads cost — lifecycle | `cost_roads_life_per_acre` | `SERVICES.roadslife.pub: true` |
| Ratio → road metres | `revenue_per_acre / road_m_per_acre`, client-side, floor 5 m/acre | `RATIO_DENOMS.roads`; the denominator picker is `FULL_BUILD`-only, so roads is the only public choice |

No other `SERVICES` entry carries `pub`, and the row filter is
`FULL_BUILD || SERVICES[r.svc].pub`. The Services panel shows dollars per acre
and a rank; the Ratio panel shows each road cost as a share of the
neighbourhood's city tax, with bars that fill at 100% and turn amber above it.
The brief's table is right.

## 1. Verdicts

| Level | Question | Verdict | One line |
|---|---|---|---|
| L0 | Should the roads lens be published? | **CONDITIONAL** | It holds one spatial variable, drawn three times and once inverted. It is sound as a supply map plus a magnitude, not as a ranking of what neighbourhoods cost |
| L1 | Two bases, both shipped | **CONDITIONAL** | The operating layer adds no picture and carries the least-defended level. It is honest only because the copy calls it a floor |
| L2 | The two rates | **CONDITIONAL** | Both transcriptions are right. Lifecycle is a floor on the City's own pairing. Operating is a floor under a joint condition on arterial cost that no source publishes |
| L3 | The metres | **CONDITIONAL** | Reproduce from raw. The arterial exclusion is not neutral: it lifts non-residential neighbourhoods' Ratio reading by a median 1.68×, residential by 1.22× |
| L4 | Share of levy | **SOUND** at shipped rates | No published neighbourhood is above 50%. The 100% mark fires only on set-aside land |
| L5 | Public copy | **CONDITIONAL** | Every number matches. Three sentences attribute a derived rate and an inferred unit to the City as published |
| L6 | Code (spot-check) | **SOUND** | Served cost ÷ served metres = the configured rate on all 406; metres rebuild from raw to 5×10⁻⁵ |

## 2. L0 — should the roads lens be published?

**Verdict: CONDITIONAL.** Sound if it is read as (a) where city-maintained road
is dense, and (b) a magnitude: at a floor rate, roads take roughly a tenth of
what a residential neighbourhood pays the City. Not sound as a map of which
neighbourhoods are cheap or expensive to serve.

**Sharpest argument against.** The lens has one spatial variable.

- *(measured)* The two cost maps are the same picture. Each neighbourhood's
  position on the colour scale differs between them by at most 2.6×10⁻⁶ of the
  range. Against the supply map they differ only by its clamp (a literal 53
  m/acre, where the cost maps use the 97.5th percentile, 54.99): at most 3.6%
  of the range. Three of the four public surfaces draw one picture with three
  legends.
- *(measured)* That variable is nearly flat where people live. Across the 226
  residential neighbourhoods, road metres per acre run 31.1 (p10) to 51.0
  (p90), a factor of 1.64. Across all 358 published it is unrelated to tax per
  acre (Spearman 0.065).
- *(measured)* So the Ratio map among residential neighbourhoods is mostly the
  Money map again. Of the variance in log revenue per road metre across the 223
  residential neighbourhoods above the floor, 72% is revenue and 31% is road
  (covariance near zero); Spearman with revenue per acre is 0.82.

What the lens does establish is real and is not on the Money view: road supply
per acre barely varies across residential Edmonton while tax per acre does, so
the road bill per acre is roughly constant and the share of tax it takes is
set by the tax. No public sentence says this. S142's condition for L0 ("the
constants are defensible") is met only in the sense L2 gives: stated floors.

**What would flip it.** To SOUND: unit costs that differ by road class, age or
condition, so the dollar maps carry information the supply map does not. To
UNSOUND: a rate wrong by an order of magnitude, so the magnitude itself
misleads. L2 and L4 bound the error at about 3×, which does not do that.

## 3. L1 — two bases, both shipped

**Verdict: CONDITIONAL.** Shipping both is defensible only as long as the copy
says what each one leaves out. It does: "Operating only, so a floor" and "run
and rebuild".

**Sharpest argument against.** The operating layer adds no picture (L0) and its
level is the weakest number on the public site. It adds a 2017 budget line to a
2025 one, divides both by a 2025 network length, and applies a per-lane-km
quotient to centreline metres. *(read, S149)* On one unit the two bases are
about 3.0× apart, not the 5.4× the shipped rates give; the panel's "about five
times" sentence says the lane-km denominator widens the gap, which is true, but
not by how much. A reader is given a 5.4× range and one clause to choose with.

**What would flip it.** To SOUND: a City-published operating cost per
centreline km or per class. To UNSOUND: evidence that the operating rate is
not a floor (L2b's condition failing).

## 4. L2 — the two rates

**Verdict: CONDITIONAL.** No transcription error. Neither rate is wrong; both
are contestable in a known direction, and the copy states the direction.

### L2a — lifecycle, $50 per metre per year

*(measured — Development Impact page re-fetched 2026-11-10, read directly)*
The page says, of "1 kilometre of a typical Edmonton neighbourhood road":
initial cost "about $1.5 million"; "will usually last 25 years, but proper
maintenance and renewal could extend its life to 50 years"; "approximately
$600,000 to operate and maintain and another $1.9 million to renew and
replace"; total "about $4 million", "about 2.5 times the initial capital
investment"; "we need to set aside, on average, 3% of the infrastructure's
value". The words "lane" and "centreline" do not appear.
($600,000 + $1,900,000) ÷ 50 ÷ 1,000 = $50. The transcription is right.

- **The 50-year life is the page's own pairing, not a choice between two
  published lives.** *(measured, arithmetic on the page's figures)* 3% of $1.5M
  is $45,000 per km per year. The page's $2.5M over 50 years is 3.3% of $1.5M
  a year; over 25 years it would be 6.7%. The same page's fire station
  ($13M to build, $16M + $27M over 40–50 years, "at least 6%") is 6.6% at 50
  years. The City's own annualisation fits the long life in both examples. This
  agrees with S172 and is not independent of it (same page), but it is a
  second line of arithmetic S172 did not use.
- **It is an illustration, not a schedule.** The page hedges every figure
  ("about", "approximately", "typical") and dates none of them. The project
  generalises one worked example to 3,658 km.
- **Direction: a floor.** *(read, S172)* Observed neighbourhood-renewal
  reconstruction runs 1.66× the page's $1,900 per metre. "Neighbourhood road"
  reads as a local; *(measured)* collectors are 25% of the charged length
  (927 of 3,658 km) and are wider.
- **By how much it could be off:** up to 2× on the life (25 years, which the
  Data & Methods text already states), and about 1.5× on the observed renewal
  cost. Stacked, about 3×.

### L2b — operating, $9.32 per metre per year

*(measured — open-data operating budget CSV and the Taproot article, both
re-fetched 2026-11-10)* FY2017 program `Roadway Maintenance` nets to
**$65,671,000** (it exists under that name only in 2017). Taproot (29 Aug 2025):
snow and ice budget $67 million, "about 55%, or $36.85 million" on roads,
"11,000 linear kilometres of roads". $65.671M ÷ 11,000 = $5,970;
$36.85M ÷ 11,000 = $3,350. The transcription is right.

- **Unit.** *(read, S149 and its S154 correction)* 11,000 is lane-km by
  magnitude (City road plus alley centreline is 6,340 km) and by the City
  snow report's own definition; the article itself prints "linear". Applied to
  centreline metres, the shipped rate is low by about 1.8× (best estimate) to
  2.19× (upper bound). Decided 2026-09-08: state it, do not convert. Not
  re-litigated here.
- **The 55% road share** rests on the one article *(read, S187)*. Each 5 points
  is $0.31 per metre, 3.3% of the rate.
- **Vintage.** One half is 2017 dollars, the other 2025, both over a 2025
  length that grew by about 1,300 km of alleys in 2021. The 2017 half is 64% of
  the rate and is unescalated.
- **Is "a floor" true?** As a floor on *total* road cost, yes, robustly: it
  excludes all capital. As a floor on the *operating* cost of collector and
  local road it is conditional. *(measured, arithmetic on S149's 1.8× and its
  35% arterial lane share, both carried)* If arterial lane-km cost k times
  local ones, the blended rate overstates the local rate by 0.65 + 0.35k.
  Splitting the two halves: the floor holds for any snow k as long as
  maintenance k ≤ 1.4; it holds for maintenance k = 2 up to snow k ≈ 10.7; it
  fails when both exceed 3.3. *(measured, the article)* The source's own
  service levels make a large snow k plausible: arterials "to bare pavement
  within one day", residential roads "to a five-centimetre snowpack within 14
  days". No source publishes k for either half.
- **`$5,970` is this project's quotient.** The City published the budget line.
  It did not publish a rate per lane-km. See L5.

**What would flip L2.** To SOUND: a City unit-cost schedule by class. To
UNSOUND: a published k above 3.3 on both halves, or evidence the page's $600k
and $1.9M are per lane.

## 5. L3 — the metres

**Verdict: CONDITIONAL.** The length is right. What is counted is a choice
with an effect the reader is not shown.

- *(measured)* `load_roads` on the 2026-11-02 raw rebuilds the served
  `road_m_per_acre` on every neighbourhood to within 5×10⁻⁵ m/acre. Charged
  length: 3,658 km citywide (collector 927, local 2,732), 3,549 km in published
  neighbourhoods. Arterials: 1,358 km, 27.1% of classified length (the quantity A9
  sizes).

**Sharpest argument against: the arterial exclusion is not neutral across
neighbourhood types.** ASSUMPTIONS A9 sizes it citywide only.

- *(measured)* Arterial share of a neighbourhood's own classified road:
  median 18% in residential neighbourhoods (p90 31%); above 50% in 49
  published neighbourhoods, 44 of them non-residential. Downtown is 64%.
- *(measured)* Counting arterials would raise road metres by more than 25% in
  195 of the 340 neighbourhoods on the Ratio map, more than 50% in 92, and
  more than double them in 36. Rank order mostly survives (Spearman 0.88 on
  metres, 0.94 on the Ratio), but 87 of 358 move more than 50 places on
  metres.
- *(measured)* On the Ratio view the exclusion lifts the reading of
  non-residential neighbourhoods by a median 1.68× (p90 2.52×) and residential
  ones by 1.22× (p90 1.43×). Downtown reads $13,960 per road metre; with its
  arterials counted, $5,010. CALGARY TRAIL SOUTH falls from 4th to 20th,
  ARMSTRONG INDUSTRIAL from 10th to 34th, EDMISTON INDUSTRIAL from 17th to
  47th. Fifteen of the top 20 stay in the top 20. All 20 of today's top 20 are
  non-residential.
- The stated rationale ("every kind of development shares them") fits a
  suburb, where the arterial has no frontage. It fits least where the map is
  brightest: downtown and the commercial strips, where the arterial *is* the
  street the buildings front. This is not a proposal to count them. It is that
  the Ratio map's top end is partly a product of the exclusion, and no public
  sentence says the exclusion matters most there.

**Other choices, carried.**

- *(read, S202)* Equal split of boundary road: 24 published neighbourhoods
  moved more than 5%. The open call (22.9 km halved into set-aside
  neighbourhoods; the River Valley variant moves 5 published neighbourhoods
  more than 5%, ARGYLL +9.2%) is still Peter's. It does not block.
- *(measured)* The 5 m/acre Ratio floor greys 18 published neighbourhoods.
  Three published neighbourhoods read 0 m: KENDAL, RIVER VALLEY KENDAL and
  WESTVIEW VILLAGE (private roads). True as "city-maintained".
- *(measured)* The panel's rank is out of all 406, set-aside included. No
  set-aside neighbourhood is above the published median for road metres, so
  the top of the ranking is unaffected.

**What would flip it.** To SOUND: a sentence where the Ratio reader is, or a
measured frontage split of arterials. To UNSOUND: nothing found; the ordering
is stable under the alternative.

## 6. L4 — share of levy

**Verdict: SOUND at shipped rates.** The lock is "magnitude, not break-even".
The numbers behave as a magnitude.

*(measured, 358 published neighbourhoods)*

| | Lifecycle | Operating |
|---|---|---|
| Median share of city tax | 8.2% | 1.5% |
| p10 – p90 | 2.2% – 14.3% | 0.4% – 2.7% |
| Residential median (226) | 10.8% (max 21.7%) | — |
| Non-residential median | 3.3% | — |
| Published above 100% / 50% / 25% / 20% | 0 / 0 / 2 / 8 | 0 / 0 / 0 / 0 |
| Citywide, all modelled road cost ÷ modelled levy | $182.9M ÷ $2.791B = 6.6% | $34.1M = 1.2% |

- The two published neighbourhoods above 25% are RIVER VALLEY CAMERON (45.5%)
  and RIVER VALLEY GOLD BAR (30.4%). The highest developed ones are ELMWOOD
  PARK (21.7%), WELLINGTON (21.5%) and DELWOOD (21.2%).
- **Stress.** At 2× (a 25-year life) the median is about 16.5% and Elmwood Park
  43%. At 3× (25 years and the observed renewal cost) Elmwood Park is about
  65%. No developed neighbourhood crosses 100% under either. One published
  neighbourhood does at 3×: RIVER VALLEY CAMERON (136%), a river-valley
  neighbourhood with 3.1 m/acre and $339 of tax per acre that is not
  set-aside.
- **The map and the panel are one number.** Lifecycle share = $50 ÷ revenue per
  road metre. The lowest Ratio reading on the map is $164.53 per metre, so a
  reader who divides finds no neighbourhood on the map past break-even at
  $50, $100 or $150. The lens does not show a deficit anywhere, and that is what a magnitude
  reading needs.
- Docs written on earlier vintages quote 9.0% and 1.68%/1.7% medians and "9
  lifecycle above 100%". Today's figures are 8.2%, 1.5% and 8. None of these is
  on a public surface.

**Sharpest argument against.** The panel still has break-even chrome: the bar
fills at 100% and turns amber beyond it (recorded as deliberate, DECISIONS
2026-09-07). *(measured)* It fires on 8 neighbourhoods for lifecycle and 2 for
operating, **all set-aside**: MILL WOODS GOLF COURSE reads 5,420%, RIVER VALLEY
LAURIER 980%. *(read, code; not rendered this session)* `ratioPanelFor` opens
for any neighbourhood with a revenue figure, so a grey neighbourhood can show
it. The only place the product ever says "over" is on land it otherwise tells
the reader not to read.

**What would flip it.** A rate change of 3× or more, at which point the amber
would start making a break-even statement about published neighbourhoods.

## 7. L5 — the public copy

**Verdict: CONDITIONAL.** `scripts/check_cost_copy.py` passes (10 of 10 quoted
rates match `data/city_unit_costs.json`) *(measured)*. The numbers are right.
Sentence by sentence *(read against the measurements above)*:

| Sentence (surface) | Verdict |
|---|---|
| "how much city-maintained collector and local road each neighbourhood has per acre" (Roads blurb) | True |
| "Arterials show neutral grey: every kind of development shares them, so they are left out" (Roads blurb) | True as a rule. The reason fits least where arterials are the frontage (L3) |
| "$5,970 per lane-km of maintenance (the City's 2017 roads-maintenance budget) plus $3,350 of snow and ice" (Roads cost blurb) | Number right. **Reads as a City-published rate.** The City published $65.671M; the division by ~11,000 (a 2025 figure from an article that prints "linear") is this project's |
| "Operating only, so a floor: rebuilding is the lifecycle layer, and one lane is charged per street" (Roads cost note) | Fair. "A floor" is robust on total cost, conditional on operating cost (L2b) |
| "$50 per metre per year: the City's $600,000 upkeep plus $1,900,000 renewal per km over a 50-year life" (Lifecycle blurb) | True to the page |
| "One citywide rate: not what the City spends here, nor a funding gap" (Lifecycle note) | True, and L4 supports it |
| "about five times more at the lifecycle rate than to operate, a gap the operating rate's lane-kilometre denominator widens" (both panels) | True (5.36×). Does not say the like-for-like gap is about 3× |
| "one published citywide cost per kilometre applied to every neighbourhood's road length" (Data & Methods) | True of lifecycle. **The operating rate is derived, not published** |
| "the operating figures are published per lane-kilometre" (Data & Methods) | **An inference stated as a fact of publication.** No source prints either figure per lane-km; the lane-km reading is S149's, on magnitude and one City definition |
| "The 50-year life is the City's figure for a well-maintained road; it also publishes 25 years, which would double the lifecycle number" (Data & Methods) | True and fair. The page's own 3% supports 50 (L2a) |
| "the last roads-only budget the City published, unadjusted for inflation, so it understates; pushing the other way, its averages include arterials" (Data & Methods) | True. Both directions stated |
| "City tax per road metre: what each neighbourhood pays the City, divided by its metres of collector and local road" (Ratio blurb) | True. Does not say the exclusion moves the top end most (L3) |

**Sharpest argument against.** The three rows with bold text. All sit on the layer whose
level is weakest, and all lend it the City's authority for a step the City
did not take. They are wording, not numbers.

**What would flip it.** Rewording those sentences so the City is credited
with the budget and the project with the division. Wording is Peter's call
(`docs/COPY_DECISIONS.md`).

## 8. L6 — code, spot-check only

**Verdict: SOUND.** *(measured)* Served lifecycle cost ÷ served metres is
within 49.99976–50.00024 on every neighbourhood with road; operating within
9.31993–9.32006. Metres rebuild from raw (L3). The copy guard passes. S202's
reproduction and mutation runs were not redone, as the brief asks.

## 9. What this leaves for Peter

No roads item below is a wrong number; the one wrong number found is in §10 (D2). "Before release" means cheap and public, so
worth a decision first; it is still a call, not a defect.

| # | Call | When | What it is worth |
|---|---|---|---|
| 1 | Reword the three sentences that credit the City with the operating *rate* and its *unit* (Roads cost blurb; two in Data & Methods), or accept them | Before release | No number or neighbourhood moves. It is the only place the public copy attributes a derived figure to the City |
| 2 | The 100% bar and amber in the Ratio panel fire only on set-aside neighbourhoods (8 lifecycle, 2 operating; up to 5,420%). Keep, or stop showing the share where the map is grey. Confirm in a browser first; read from code only | Before release | 8 neighbourhoods' panels. No published neighbourhood is affected at shipped rates |
| 3 | Say on the Ratio surface or in Data & Methods that leaving out arterials raises the reading most downtown and on commercial and industrial land, or accept | Does not block | Median 1.68× on 117 non-residential neighbourhoods against 1.22× on 223 residential; Downtown 2.8×; 5 of the top 20 change. No served number moves |
| 4 | Close "50 or 25 years" as **keep 50** | Does not block | The page's own 3% and 6% figures fit only the long life. 25 would double every lifecycle dollar ($182.9M → $365.8M citywide); already stated in Data & Methods |
| 5 | Three Services maps are one picture. Accept, or say so in one clause | Does not block | 0 neighbourhoods move. Saves a reader comparing two identical maps |
| 6 | The S202 set-aside boundary split | Does not block (carried) | 5 published neighbourhoods above 5%, ARGYLL +9.2% |
| 7 | Size ASSUMPTIONS A9 per neighbourhood, not only citywide | Does not block | A weekly row in `notebooks/verified/03_assumptions.py`; a code change, so propose first |
| 8 | Refresh the share-of-levy figures quoted in older docs (9.0% → 8.2%; 1.68% → 1.5%; 9 → 8 above 100%) where a live doc still cites them | Does not block | Docs only |

From the Development appendix (§10):

| # | Call | When | What it is worth |
|---|---|---|---|
| 9 | ⚠️ Add the City's new spelling `CHAPPELLE, HERITAGE VALLEY AREA` to `PERMIT_NAME_CORRECTIONS` (a `src/` change, so a PR for Peter), and decide whether a guard should fail when a correction key stops matching | Does not block at this size; it is a wrong shipped number | CHAPPELLE units since 2009: 6,848 → 6,876 (+28, 0.4%). One neighbourhood |
| 10 | The grid blurb's "aren't on the grid yet (the newest permits lag geocoding)". Drop "yet" and the lag claim, or accept. The F4 draft wording does not fix it | Before release (default state) | No number moves. False as to cause on the default state (51.6% of the gap is 2009–20); "yet" unsupported on all six |
| 11 | HOLLICK-KENYON: place the one 60-unit 2012 permit, or accept | Does not block | 582 → 642 units since 2009 (+10.3%). One neighbourhood, default window only |
| 12 | The 387 units that cannot be placed between RUTHERFORD / HERITAGE VALLEY TOWN CENTRE and THE HAMPTONS / GRANVILLE: leave out (as now, and say so), or split by a stated rule | Does not block | Four neighbourhoods, each possibly 5–18% low on the default window; 2009–12 permits |
| 13 | Tell the City that coordinates stopped arriving for most permits issued since early 2025 (a `docs/DATA_ISSUES.md` row and a report), and correct `data/DATA.md`'s "expect coverage to improve" | Does not block | 30% of 3-year units are off the grid and the share is not shrinking |

**Not verified this session:** that a set-aside neighbourhood's Ratio panel
opens in a real browser (item 2); the City snow report's page-16 lane-km
definition (carried from S154); the 35% arterial lane share (carried from
S149, whose source is a relay now offline).

## 10. Development appendix (D1, D2)

Run on a fresh pull of `24uj-dj8v` (2026-11-10, the pipeline's own `$select`,
248,736 rows), through `src/load_permits.py`'s own vocabulary sets and
`load_permits` itself. *(measured)* `load_permits` on that pull rebuilds the
served `new_dwelling_units_long` exactly on all 406 neighbourhoods, and the
grid's served `coverage` block matches to the unit on every window. The
industrial metric is hidden in the public build *(read)*, so the public
Development grid has six states: units or permits × 3 windows.

### D1 — F4, the "(the newest permits lag geocoding)" clause

**F4's numbers reproduce.** *(measured)* On the default state (units, since
2009), 26,252 of 162,360 units are off the grid (16.2%); **13,557 of them
(51.6%) come from 2009–2020 permits.** Those permits average 7.34 units against
1.75 for geocoded ones; apartment units of 2009–20 are 76.6% geocoded, other
types 91.2%. F4 said 13,557 of 26,286 (52%), 7.3 against 1.75, and 77% / 91%.

Share of the off-grid gap by permit year, all six public states *(measured)*:

| State | Off grid | from 2009–20 | from 2021–23 | from 2024–25 |
|---|---|---|---|---|
| Units, since 2009 (default) | 16.2% | **51.6%** | 7.4% | 40.9% |
| Permits, since 2009 | 8.4% | 28.1% | 4.7% | 67.2% |
| Units, 5 yr | 21.3% | — | 15.3% | 84.7% |
| Permits, 5 yr | 18.8% | — | 6.5% | 93.5% |
| Units, 3 yr | 29.8% | — | 7.8% | 92.2% |
| Permits, 3 yr | 30.7% | — | 2.1% | 97.9% |

**The §4 draft wording** ("most are recent permits not yet geocoded; some older
apartment permits never were") **is not true on every state.**

- "Most are recent" is true on five states and **false on the default one**,
  where 2024–25 is 40.9% of the gap and 2009–20 is the majority. "Some older
  apartment permits never were" also understates that state: apartments are
  53.5% of the 2009–20 off-grid units, so nearly half of the old gap is not
  apartments.
- **"Not yet" is unsupported on all six.** This is new; F4 did not test it.
  *(measured)* Between the raw pull of 2026-09-03 and today (68 days), the
  number of un-geocoded new-residential permits did not change in any year
  from 2009 to 2024 (2024: 936 and 936), and 2025 went from 3,491 to 3,485
  while 12 permits left the year. *(read, `data/DATA.md`, probe of
  2026-07-14)* Among new-construction rows, 994 were un-geocoded for 2024 and
  3,564 for 2025; today 998 and 3,558 *(measured)*. In 119 days the backlog
  moved by −2 permits. *(measured, served history)* The 5-year grid held
  47,125 of 59,697 units on 2026-07-15 and holds 46,933 of 59,628 today.
- *(measured)* By issue month, new-construction permits are 95–99% geocoded
  through March 2024, 76–89% for April–November 2024, 66% for December, 51%
  for January 2025, and 21–44% for every month from February 2025 to October
  2026. Inside that last stretch there is no age gradient: permits issued 21
  months ago (39%) are geocoded at about the rate of last month's (31%). A
  rolling lag would show older months filling in, and none did in four months.
  Either the City's process changed around the turn of 2025, or coordinates
  arrive in a batch that has not run since July. The data cannot say which.
- So "yet", "lag" and `data/DATA.md`'s "expect coverage to improve as the city
  geocodes its backlog" are forecasts with four months of evidence against
  them. A wording that is true on all six states says only that these permits
  have no coordinates in the City's data, without "yet".

### D2 — the unattributed comma-name units

**The count has moved, and one fix has silently come undone.** *(measured)*
On today's pull, **565 units under 11 comma-joined names** have no boundary
match (new residential, 2009–2025). On the 2026-09-03 pull the same filter
gives 537 under 10. The docs' "14 names" does not reproduce under this filter.

- ⚠️ **A shipped number is wrong.** The City renamed a string between the two
  pulls: `CHAPPELLE AREA, HERITAGE VALLEY AREA` (16 rows) is now
  `CHAPPELLE, HERITAGE VALLEY AREA` on 15 of them. `PERMIT_NAME_CORRECTIONS`
  is keyed on the old string, so the S216 placement no longer matches. The
  served CHAPPELLE figure for units since 2009 is 6,848; with the decided
  placement it is 6,876. **28 units, 8 permits, 0.4% low.** It is the only new
  string since 09-03, and every other permit-only key still matches its rows.
  The pipeline's warning for this goes to the build log; nothing with a reader
  reported it, and the S216 test passes because its fixture carries the old
  string.

**Per neighbourhood, placed by geocode.** Only 12 of the 55 permits (146 of 565
units) have coordinates. All affect the since-2009 window only; the 5-year and
3-year windows move by at most 0.3% (GLENORA, 1 unit).

| Neighbourhood | Served units since 2009 | Placed by geocode | Change |
|---|---|---|---|
| HOLLICK-KENYON | 582 | +60 (one 2012 permit named `HOLLICK-KENYON, BRINTNELL, MILLER, BRINTNELL`) | **+10.3%** |
| RUTHERFORD | 1,774 | +59 (of `RUTHERFORD, HERITAGE VALLEY TOWN CENTRE`) | +3.3% |
| CHAPPELLE | 6,848 | +18 (of the renamed string; +28 by the S216 decision) | +0.3% / +0.4% |
| THE UPLANDS | 1,973 | +4 | +0.2% |
| GLENORA | 637 | +1 | +0.2% |
| SUMMERSIDE | 3,848 | +3 | +0.1% |
| ANTHONY HENDAY HORSE HILL (set-aside) | 0 | +1 | grey either way |

**What geocode cannot place** (419 units, no coordinates), with the bound if
the whole remainder went to one named neighbourhood:

| Name | Un-geocoded | Bound |
|---|---|---|
| `RUTHERFORD, HERITAGE VALLEY TOWN CENTRE` | 268 units, 4 permits, 2011–12 | RUTHERFORD +15.1% (on top of +3.3%), or HERITAGE VALLEY TOWN CENTRE +16.7% |
| `THE HAMPTONS, GRANVILLE` | 119 units, 17 permits, 2009–12 | THE HAMPTONS +5.6%, or GRANVILLE +10.9% |
| `ALLARD, HERITAGE VALLEY AREA` | 18 units, 2010 | ALLARD +0.5% |
| `CHAPPELLE, HERITAGE VALLEY AREA` | 10 units | CHAPPELLE +0.1% |
| `CENTRAL MCDOUGALL, QUEEN MARY PARK` | 4 units, 2016 | CENTRAL MCDOUGALL +3.0%, or QUEEN MARY PARK +0.3% |

**Release items by the brief's rule (above ~5%, or a false "no permits").**

- **HOLLICK-KENYON is 10.3% low** on the default window, by geocode.
- RUTHERFORD, HERITAGE VALLEY TOWN CENTRE, THE HAMPTONS and GRANVILLE each
  could be 5–18% low; the data cannot say which of each pair.
- **No false "no permits" is established.** 88 published neighbourhoods show
  0 units since 2009. Two are named in a comma list: EKOTA (its one unit
  geocodes to SUMMERSIDE) and HERITAGE VALLEY AREA (28 + 18 units named with
  it; every geocoded row falls in CHAPPELLE, and the ALLARD rows have no
  coordinates). Neither receives a unit by geocode.

