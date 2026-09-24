# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~8,080-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (310 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 642–646 |  |
| `HOME` | 647–647 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 648–661 |  |
| `WINDOWS` | 662–687 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 688–697 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 698–702 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 703–778 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `money0` | 779–781 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `fmtMoney` | 782–783 |  |
| `METRICS` | 784–914 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 915–931 |  |
| `RATIO_DENOMS` | 932–965 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 966–966 |  |
| `ratioOf` | 967–967 |  |
| `ratioKept` | 968–989 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 990–1000 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 1001–1028 |  |
| `dominantUse` | 1029–1070 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1071–1241 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1242–1346 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1347–1351 | the Lab: a container for unfinished lenses |
| `inLab` | 1352–1353 |  |
| `DEVIATION_TITLES` | 1354–1358 |  |
| `deviationTitle` | 1359–1364 |  |
| `deviationKind` | 1365–1367 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1368–1373 |  |
| `changeBlurb` | 1374–1398 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1399–1420 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassInstBlurb` | 1421–1433 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1434–1445 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `amenityWhichPhrase` | 1446–1451 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1452–1457 |  |
| `infillAmenityBlurb` | 1458–1471 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1472–1486 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1487–1492 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1493–1501 |  |
| `devChoroplethBlurb` | 1502–1511 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1512–1560 |  |
| `withColourClause` | 1561–1578 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1579–1585 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1586–1599 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1600–1600 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1601–1615 |  |
| `fmtMB` | 1616–1626 |  |
| `showGridBusy` | 1627–1649 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1650–1666 |  |
| `loadGridData` | 1667–1720 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1721–1774 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1775–1799 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1800–1831 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1832–1832 |  |
| `gridFetches` | 1833–1857 |  |
| `RAMPS` | 1858–1898 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1899–1905 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1906–1911 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1912–1912 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1913–1919 |  |
| `AMENITY_BANDS` | 1920–1921 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1922–1924 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1925–1930 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1931–1945 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1946–1951 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1952–1970 |  |
| `gridScale` | 1971–1991 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 1992–1998 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1999–2010 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 2011–2013 |  |
| `quantile` | 2014–2028 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 2029–2061 |  |
| `moneyBlurb` | 2062–2066 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 2067–2079 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2080–2158 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2159–2159 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2160–2186 |  |
| `failLoading` | 2187–2200 |  |
| `hideLoading` | 2201–2255 |  |
| `topRings` | 2256–2272 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2273–2298 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2299–2299 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2300–2312 |  |
| `svcT` | 2313–2321 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2322–2335 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2336–2336 |  |
| `fmtFire` | 2337–2338 |  |
| `fmtTransit` | 2339–2340 |  |
| `fmtBike` | 2341–2353 |  |
| `fmtRoadM` | 2354–2367 |  |
| `fmtResShare` | 2368–2370 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2371–2376 |  |
| `fmtRoadsCost` | 2377–2381 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2382–2383 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2384–2385 |  |
| `fmtBikeCost` | 2386–2397 |  |
| `servicePlaneLayer` | 2398–2430 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2431–2440 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2441–2446 |  |
| `DEV_IND_TOTAL` | 2447–2449 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2450–2455 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2456–2460 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2461–2466 |  |
| `devGridOfferable` | 2467–2468 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2469–2469 |  |
| `devCol` | 2470–2470 |  |
| `_devScale` | 2471–2471 |  |
| `devScale` | 2472–2478 |  |
| `devT` | 2479–2482 |  |
| `developmentPlaneLayer` | 2483–2499 |  |
| `fmtDev` | 2500–2515 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2516–2521 |  |
| `DEV_GRID_IND_N` | 2522–2522 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2523–2525 |  |
| `devGridScale` | 2526–2552 |  |
| `devGridLayer` | 2553–2601 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2602–2603 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2604–2611 |  |
| `_infillStats` | 2612–2612 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2613–2630 |  |
| `_infillRaw` | 2631–2633 |  |
| `infillScore` | 2634–2649 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2650–2651 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2652–2669 |  |
| `INFILL_CENTER` | 2670–2670 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2671–2671 |  |
| `INFILL_NEG` | 2672–2672 |  |
| `infillColorAt` | 2673–2677 |  |
| `infillPlaneLayer` | 2678–2699 |  |
| `fmtFar` | 2700–2709 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `AMENITY_HIGHLIGHT_COLOR` | 2710–2710 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2711–2765 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2766–2773 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2774–2788 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2789–2809 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2810–2810 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2811–2825 |  |
| `chgT` | 2826–2835 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2836–2866 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2867–2955 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2956–2963 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2964–2964 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2965–2972 |  |
| `deviationRate` | 2973–3015 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 3016–3016 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 3017–3046 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3047–3053 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3054–3065 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3066–3069 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3070–3074 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3075–3085 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3086–3101 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3102–3133 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3134–3158 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `INST_OUTLINE_COLOR` | 3159–3211 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 3212–3216 |  |
| `bandHover` | 3217–3225 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3226–3322 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3323–3330 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3331–3332 |  |
| `glassInstBandLayers` | 3333–3373 |  |
| `ratioInstBandLayers` | 3374–3401 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3402–3414 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3415–3416 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3417–3418 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3419–3419 |  |
| `deviationStats` | 3420–3464 |  |
| `deviationOf` | 3465–3466 |  |
| `deviationT` | 3467–3477 |  |
| `fmtDeviation` | 3478–3499 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3500–3543 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3544–3630 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3631–3653 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3654–3654 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3655–3675 |  |
| `ensureFireStations` | 3676–3691 |  |
| `TRANSIT_STATION_COLOR` | 3692–3692 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3693–3710 |  |
| `ensureTransitStations` | 3711–3726 |  |
| `TRANSIT_LINE_COLOR` | 3727–3727 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3728–3744 |  |
| `ensureLrtLines` | 3745–3761 |  |
| `BIKE_LINE_COLOR` | 3762–3762 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3763–3779 |  |
| `ensureBikeLines` | 3780–3837 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3838–3838 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3839–3842 |  |
| `BOUNDARY_COLOR` | 3843–3852 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3853–3853 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3854–3866 |  |
| `referenceSplit` | 3867–3894 |  |
| `referenceUnderLayers` | 3895–3929 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3930–3946 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3947–3966 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3967–3979 |  |
| `servicesBlurb` | 3980–3997 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3998–4021 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 4022–4032 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 4033–4084 |  |
| `REF_TIERS` | 4085–4106 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4107–4114 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 4115–4117 |  |
| `placeAnchors` | 4118–4141 |  |
| `labelPool` | 4142–4149 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4150–4203 |  |
| `CHROME_IDS` | 4204–4208 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4209–4227 |  |
| `visibleLabels` | 4228–4282 |  |
| `labelLayer` | 4283–4319 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 4320–4320 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4321–4336 |  |
| `ratioT` | 4337–4359 |  |
| `zMatrix` | 4360–4364 |  |
| `buildLayers` | 4365–4388 |  |
| `flattenDuringEase` | 4389–4413 | Center 2D lowers the heights over the LAST QUARTER OF THE TILT instead |
| `buildViewLayers` | 4414–4723 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4724–4753 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4754–4763 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4764–4766 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 4767–4798 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4799–4805 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4806–4813 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4814–4818 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4819–4829 |  |
| `revenueLens` | 4830–4831 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4832–4864 |  |
| `SVC_COST_BASES` | 4865–4882 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 4883–4891 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 4892–4907 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 4908–4910 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 4911–4917 |  |
| `svcRank` | 4918–4922 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 4923–4929 |  |
| `svcDriverReading` | 4930–4950 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 4951–4951 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4952–4955 |  |
| `servicePanelFor` | 4956–4976 |  |
| `hoodPanelLens` | 4977–4980 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4981–4998 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4999–5030 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 5031–5036 |  |
| `sparklineSvg` | 5037–5052 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 5053–5112 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5113–5118 | Development history: new supply per year |
| `devHistKey` | 5119–5128 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5129–5133 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5134–5134 |  |
| `devHistVerb` | 5135–5140 |  |
| `devHistoryFor` | 5141–5162 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5163–5182 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5183–5202 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5203–5238 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5239–5241 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5242–5305 |  |
| `syncTemporalPos` | 5306–5332 |  |
| `openTemporal` | 5333–5367 |  |
| `renderRevenueMix` | 5368–5434 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 5435–5514 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 5515–5518 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5519–5569 |  |
| `syncPinnedPanel` | 5570–5599 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5600–5615 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5616–5633 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5634–5681 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5682–5687 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5688–5734 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5735–5751 |  |
| `temporalClick` | 5752–5809 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 5810–5878 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 5879–6259 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6260–6341 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6342–6342 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6343–6361 |  |
| `syncMetricButtons` | 6362–6385 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6386–6392 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6393–6406 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6407–6448 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6449–6491 |  |
| `toggleBudgetPanel` | 6492–6517 |  |
| `syncMillRates` | 6518–6550 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 6551–6572 |  |
| `applyColorAdjust` | 6573–6594 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 6595–6607 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 6608–6623 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 6624–6641 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 6642–6658 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 6659–6680 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 6681–6697 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 6698–6937 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 6938–6948 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 6949–6962 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 6963–6971 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 6972–6982 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 6983–6994 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 6995–7008 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 7009–7029 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 7030–7077 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7078–7083 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7084–7105 |  |
| `applyMoneyDetail` | 7106–7130 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7131–7142 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7143–7150 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7151–7169 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7170–7180 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7181–7188 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7189–7205 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7206–7219 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7220–7230 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7231–7482 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7483–7492 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7493–7506 |  |
| `applySvcDriver` | 7507–7520 |  |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 7521–8080 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (951 edges)

⚠️ **A regex reference count, not a call graph** — a name in a comment or string counts, and a nested symbol is attributed to its enclosing range. Use it for *what is central* and *would this seam hold*, never as ground truth for a final module boundary.

**Most depended-on** — moving one of these touches everything below it.

| symbol | referenced by | section |
|---|---|---|
| `state` | 119 | the Lab: a container for unfinished lenses |
| `buildLayers` | 37 | geographic reference layers (all views) |
| `METRICS` | 16 | tunables |
| `SERVICES` | 14 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `applyView` | 14 | control appliers + the view/legend dispatchers |
| `refreshLegend` | 14 | control appliers + the view/legend dispatchers |
| `CELLS` | 10 | tunables |
| `quantile` | 10 | the Lab: a container for unfinished lenses |
| `ratioScale` | 9 | geographic reference layers (all views) |
| `deviationStats` | 9 | the same doubt, at 100 m |
| `ratioDenom` | 8 | services lens views (SPEC_services.md display architecture) |
| `devIndustrial` | 8 | loading overlay |
| `devCol` | 8 | loading overlay |
| `exemptFrac` | 8 | the institutional uncertainty band |
| `labelPool` | 8 | geographic reference layers (all views) |

**Section self-containment** — share of each section's outgoing edges that stay inside it. Low means a module cut on this banner would mostly import its neighbours.

| section | edges | self-contained |
|---|---|---|
| uses view (use-mix, 2026-07-03) | 3 | 67% |
| Infill lens (SPEC_development.md Lens B) | 27 | 67% |
| deviation lens: revenue per developed acre against peer average | 3 | 67% |
| the Lab: a container for unfinished lenses | 110 | 65% |
| tunables | 13 | 46% |
| Development 100 m detail grid (layers-panel toggle, 2026-07-15) | 9 | 44% |
| change lens: how each hood's share of the assessment base moved | 16 | 44% |
| geographic reference layers (all views) | 92 | 43% |
| loading overlay | 55 | 35% |
| two tiers, answering two different questions | 29 | 31% |
| Money's revenue panel: where a hood's levy comes from | 34 | 26% |
| the same doubt, at 100 m | 61 | 26% |
| services lens views (SPEC_services.md display architecture) | 4 | 25% |
| Development history: new supply per year | 194 | 24% |
| control appliers + the view/legend dispatchers | 210 | 20% |
| the citywide budget panel (EXPERIMENTAL, full build only) | 12 | 8% |
| services view (SPEC_services.md UI generalization, 2026-07-05) | 16 | 0% |
| the institutional uncertainty band | 2 | 0% |
| temporal lens (SPEC_temporal.md phase 3) | 4 | 0% |
| boot | 57 | 0% |

## Element ids (128) — the control surface

| id | line |
|---|---|
| `#map` | 18 |
| `#loading` | 22 |
| `#loading-box` | 23 |
| `#loading-title` | 34 |
| `#loading-blurb` | 35 |
| `#loading-spinner` | 36 |
| `#loading-text` | 37 |
| `#loading-retry` | 38 |
| `#banner` | 42 |
| `#gridbusy` | 53 |
| `#gridbusy-spinner` | 54 |
| `#gridbusy-text` | 56 |
| `#gridbusy-size` | 57 |
| `#title` | 61 |
| `#title-h` | 62 |
| `#title-p` | 63 |
| `#temporal` | 74 |
| `#temporal-close` | 75 |
| `#temporal-name` | 76 |
| `#temporal-body` | 83 |
| `#temporal-chart` | 84 |
| `#temporal-read` | 85 |
| `#temporal-note` | 86 |
| `#temporal-hint` | 90 |
| `#millrates` | 106 |
| `#mill-head` | 107 |
| `#mill-rows` | 108 |
| `#mill-note` | 109 |
| `#budget` | 123 |
| `#budget-close` | 130 |
| `#budget-head` | 131 |
| `#budget-body` | 136 |
| `#budget-rows` | 137 |
| `#budget-other-hd` | 138 |
| `#budget-other` | 139 |
| `#budget-note` | 140 |
| `#peek` | 155 |
| `#peek-name` | 156 |
| `#peek-read` | 157 |
| `#peek-go` | 158 |
| `#controls` | 161 |
| `#toggle` | 174 |
| `#metric-row` | 175 |
| `#revcut` | 179 |
| `#moneymode` | 184 |
| `#views` | 190 |
| `#optpanel` | 204 |
| `#opt-fold` | 205 |
| `#opt-caret` | 205 |
| `#opt-body` | 206 |
| `#layers` | 207 |
| `#chgwindow-hd` | 208 |
| `#chgwindow` | 209 |
| `#labpick-hd` | 218 |
| `#labpick` | 219 |
| `#labcut-hd` | 220 |
| `#labcut` | 221 |
| `#moneydetail-hd` | 226 |
| `#moneydetail` | 227 |
| `#amenity-hd` | 252 |
| `#amenity` | 253 |
| `#amenity-lrt-row` | 254 |
| `#amenity-lrt-on` | 255 |
| `#amenity-school-row` | 257 |
| `#amenity-school-on` | 258 |
| `#uses-prisms-hd` | 261 |
| `#uses-prisms` | 262 |
| `#uses-prisms-on` | 264 |
| `#devmode-hd` | 267 |
| `#devmode` | 268 |
| `#devmetric-hd` | 272 |
| `#devmetric` | 273 |
| `#devwindow-hd` | 278 |
| `#devwindow` | 279 |
| `#devdetail-hd` | 284 |
| `#devdetail` | 285 |
| `#prism-hd` | 289 |
| `#prism-row` | 290 |
| `#prism-opacity` | 292 |
| `#prism-opacity-val` | 293 |
| `#services-hd` | 295 |
| `#services` | 296 |
| `#denom-hd` | 395 |
| `#denom` | 396 |
| `#ratio-denom-hd` | 400 |
| `#ratio-denom` | 401 |
| `#hoodmode` | 411 |
| `#hoodmode-btn` | 412 |
| `#coloradj` | 424 |
| `#coloradj-btn` | 425 |
| `#budget-pod` | 432 |
| `#budget-btn` | 433 |
| `#a11y` | 437 |
| `#a11y-btn` | 438 |
| `#a11y-menu` | 439 |
| `#palette` | 441 |
| `#labels-on` | 448 |
| `#reference-on` | 456 |
| `#about` | 461 |
| `#about-btn` | 462 |
| `#about-menu` | 463 |
| `#about-src-roads` | 475 |
| `#about-src-services` | 476 |
| `#about-vintage` | 504 |
| `#about-build` | 508 |
| `#about-modelled-roads` | 522 |
| `#about-modelled` | 540 |
| `#about-budget` | 550 |
| `#about-budget-lead` | 552 |
| `#about-budget-rows` | 553 |
| `#about-budget-note` | 554 |
| `#about-updated` | 565 |
| `#botleft` | 569 |
| `#compass` | 570 |
| `#rot-ccw` | 571 |
| `#tonorth` | 578 |
| `#needle` | 580 |
| `#rot-cw` | 585 |
| `#viewbtns` | 593 |
| `#recenter` | 595 |
| `#center2d` | 596 |
| `#legend` | 598 |
| `#legend-label` | 599 |
| `#legend-min` | 601 |
| `#legend-max` | 601 |
| `#legend-cats` | 603 |
| `#revmix` | 5387 |
| `#svccost` | 5478 |
