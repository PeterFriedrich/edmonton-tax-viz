# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~8,502-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (327 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 675–679 |  |
| `HOME` | 680–680 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 681–694 |  |
| `WINDOWS` | 695–720 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 721–730 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 731–735 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 736–811 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `money0` | 812–814 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `fmtMoney` | 815–816 |  |
| `METRICS` | 817–919 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 920–936 |  |
| `RATIO_DENOMS` | 937–970 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 971–971 |  |
| `ratioOf` | 972–972 |  |
| `ratioKept` | 973–994 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 995–1005 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 1006–1033 |  |
| `dominantUse` | 1034–1075 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1076–1226 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1227–1322 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1323–1327 | the Lab: a container for unfinished lenses |
| `inLab` | 1328–1329 |  |
| `DEVIATION_TITLES` | 1330–1334 |  |
| `deviationTitle` | 1335–1340 |  |
| `deviationKind` | 1341–1343 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1344–1351 |  |
| `changeBlurb` | 1352–1369 | Change-lens blurb (COPY_DECISIONS BC1, B8 shape). It follows the window |
| `glassLead` | 1370–1382 | Grid blurb (COPY_DECISIONS BG1, B8 shape). Names the metric (B6) and the |
| `glassInstBlurb` | 1383–1395 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1396–1404 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `ratioBlurb` | 1405–1413 | Ratio blurb (COPY_DECISIONS BR1, B8 shape): the denominator's P1, a |
| `amenityWhichPhrase` | 1414–1419 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1420–1427 |  |
| `infillAmenityBlurb` | 1428–1441 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1442–1453 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `devTitle` | 1454–1459 | Development blurb, in the COPY_DECISIONS B8 shape (BD1): what the lens |
| `devBlurb` | 1460–1518 |  |
| `setBlurb` | 1519–1531 | Blurb markup (COPY_DECISIONS B8): a blank line starts a new paragraph and |
| `currentBlurb` | 1532–1547 | The active view's blurb. Read by applyView and by the camera's 2D/3D flip |
| `withColourClause` | 1548–1565 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1566–1572 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1573–1586 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1587–1587 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1588–1602 |  |
| `fmtMB` | 1603–1613 |  |
| `showGridBusy` | 1614–1636 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1637–1653 |  |
| `loadGridData` | 1654–1707 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1708–1761 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1762–1786 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1787–1818 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1819–1819 |  |
| `gridFetches` | 1820–1845 |  |
| `RAMPS` | 1846–1886 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1887–1893 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1894–1899 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1900–1900 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1901–1907 |  |
| `AMENITY_BANDS` | 1908–1909 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1910–1912 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1913–1918 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1919–1933 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1934–1939 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1940–1958 |  |
| `gridScale` | 1959–1979 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 1980–1986 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1987–1998 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1999–2001 |  |
| `quantile` | 2002–2016 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 2017–2051 |  |
| `moneyBlurb` | 2052–2063 | The money blurb (COPY_DECISIONS BM1, B8 shape): the metric's own P1 under |
| `fillFor` | 2064–2076 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2077–2155 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2156–2156 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2157–2183 |  |
| `failLoading` | 2184–2197 |  |
| `hideLoading` | 2198–2252 |  |
| `topRings` | 2253–2269 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2270–2295 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2296–2296 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2297–2309 |  |
| `svcT` | 2310–2318 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2319–2332 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2333–2333 |  |
| `fmtFire` | 2334–2335 |  |
| `fmtTransit` | 2336–2337 |  |
| `fmtBike` | 2338–2350 |  |
| `fmtRoadM` | 2351–2364 |  |
| `fmtResShare` | 2365–2367 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2368–2373 |  |
| `fmtRoadsCost` | 2374–2378 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2379–2380 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2381–2382 |  |
| `fmtBikeCost` | 2383–2394 |  |
| `servicePlaneLayer` | 2395–2427 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2428–2437 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2438–2443 |  |
| `DEV_IND_TOTAL` | 2444–2446 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2447–2452 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2453–2457 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2458–2463 |  |
| `devGridOfferable` | 2464–2465 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2466–2466 |  |
| `devCol` | 2467–2467 |  |
| `_devScale` | 2468–2468 |  |
| `devScale` | 2469–2475 |  |
| `devT` | 2476–2479 |  |
| `developmentPlaneLayer` | 2480–2496 |  |
| `fmtDev` | 2497–2512 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2513–2518 |  |
| `DEV_GRID_IND_N` | 2519–2519 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2520–2522 |  |
| `devGridScale` | 2523–2549 |  |
| `devGridLayer` | 2550–2598 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2599–2600 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2601–2608 |  |
| `_infillStats` | 2609–2609 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2610–2627 |  |
| `_infillRaw` | 2628–2630 |  |
| `infillScore` | 2631–2646 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2647–2648 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2649–2666 |  |
| `INFILL_CENTER` | 2667–2667 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2668–2668 |  |
| `INFILL_NEG` | 2669–2669 |  |
| `infillColorAt` | 2670–2674 |  |
| `infillPlaneLayer` | 2675–2696 |  |
| `fmtFar` | 2697–2706 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `AMENITY_HIGHLIGHT_COLOR` | 2707–2707 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2708–2762 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2763–2770 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2771–2785 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2786–2806 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2807–2807 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2808–2822 |  |
| `chgT` | 2823–2832 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2833–2863 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2864–2952 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2953–2960 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2961–2961 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2962–2969 |  |
| `deviationRate` | 2970–3012 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 3013–3013 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 3014–3043 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3044–3050 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3051–3062 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3063–3066 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3067–3071 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3072–3082 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3083–3098 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3099–3130 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3131–3155 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `INST_OUTLINE_COLOR` | 3156–3208 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 3209–3213 |  |
| `bandHover` | 3214–3222 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3223–3325 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3326–3333 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3334–3335 |  |
| `glassInstBandLayers` | 3336–3376 |  |
| `ratioInstBandLayers` | 3377–3404 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3405–3417 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3418–3419 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3420–3421 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3422–3422 |  |
| `deviationStats` | 3423–3467 |  |
| `deviationOf` | 3468–3469 |  |
| `deviationT` | 3470–3480 |  |
| `fmtDeviation` | 3481–3502 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3503–3546 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3547–3633 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3634–3656 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3657–3657 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3658–3678 |  |
| `ensureFireStations` | 3679–3694 |  |
| `TRANSIT_STATION_COLOR` | 3695–3695 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3696–3713 |  |
| `ensureTransitStations` | 3714–3729 |  |
| `TRANSIT_LINE_COLOR` | 3730–3730 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3731–3747 |  |
| `ensureLrtLines` | 3748–3764 |  |
| `BIKE_LINE_COLOR` | 3765–3765 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3766–3782 |  |
| `ensureBikeLines` | 3783–3840 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3841–3841 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3842–3845 |  |
| `BOUNDARY_COLOR` | 3846–3855 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3856–3856 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3857–3869 |  |
| `referenceSplit` | 3870–3897 |  |
| `referenceUnderLayers` | 3898–3932 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3933–3949 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3950–3969 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3970–3983 |  |
| `servicesBlurb` | 3984–3995 | Services-view blurb (COPY_DECISIONS BS1, B8 shape): the colour-driving |
| `hoodHoverLayer` | 3996–4019 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 4020–4030 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 4031–4082 |  |
| `REF_TIERS` | 4083–4104 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4105–4112 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 4113–4115 |  |
| `placeAnchors` | 4116–4139 |  |
| `labelPool` | 4140–4147 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4148–4201 |  |
| `CHROME_IDS` | 4202–4206 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4207–4225 |  |
| `visibleLabels` | 4226–4280 |  |
| `labelLayer` | 4281–4317 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 4318–4318 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4319–4334 |  |
| `ratioT` | 4335–4357 |  |
| `zMatrix` | 4358–4362 |  |
| `buildLayers` | 4363–4386 |  |
| `flattenDuringEase` | 4387–4411 | Center 2D lowers the heights over the LAST QUARTER OF THE TILT instead |
| `buildViewLayers` | 4412–4721 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4722–4751 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4752–4761 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4762–4764 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 4765–4796 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4797–4803 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4804–4811 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4812–4816 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4817–4827 |  |
| `revenueLens` | 4828–4829 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4830–4862 |  |
| `SVC_COST_BASES` | 4863–4880 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 4881–4889 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 4890–4899 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 4900–4902 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 4903–4909 |  |
| `svcRank` | 4910–4914 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 4915–4921 |  |
| `svcDriverReading` | 4922–4942 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 4943–4943 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4944–4947 |  |
| `servicePanelFor` | 4948–4952 |  |
| `ratioPanelFor` | 4953–4976 | Ratio carries the cost-as-a-share-of-tax panel that Services had until |
| `hoodPanelLens` | 4977–4981 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4982–4999 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 5000–5031 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 5032–5037 |  |
| `sparklineSvg` | 5038–5053 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 5054–5113 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5114–5119 | Development history: new supply per year |
| `devHistKey` | 5120–5129 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5130–5134 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5135–5135 |  |
| `devHistVerb` | 5136–5141 |  |
| `devHistoryFor` | 5142–5177 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5178–5197 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5198–5217 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5218–5253 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5254–5256 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5257–5320 |  |
| `syncTemporalPos` | 5321–5347 |  |
| `openTemporal` | 5348–5384 |  |
| `renderRevenueMix` | 5385–5454 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderRatioCost` | 5455–5529 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `renderServiceCost` | 5530–5587 | The Services panel: what each cost IS for this hood, in dollars, and where |
| `fmtSvcRatio` | 5588–5591 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5592–5642 |  |
| `syncPinnedPanel` | 5643–5676 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5677–5692 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5693–5710 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5711–5758 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5759–5764 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5765–5812 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5813–5829 |  |
| `temporalClick` | 5830–5881 | Click a hood to pin its history; click the pinned one again to unpin. |

### neighbourhood search

| symbol | lines | what it does |
|---|---|---|
| `searchNorm` | 5882–5889 | neighbourhood search |
| `searchMatches` | 5890–5904 | Ranked: the name starts with the query, then a later WORD does (so |
| `renderSearchList` | 5905–5933 |  |
| `openSearch` | 5934–5946 |  |
| `closeSearch` | 5947–5963 |  |
| `flyToHood` | 5964–5983 | Keep the current tilt and rotation, so the camera moves TO the hood |
| `pickSearch` | 5984–6000 | A pick reads exactly like tapping or clicking the hood (temporalClick |
| `primaryRow` | 6001–6069 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 6070–6447 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6448–6537 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6538–6538 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6539–6557 |  |
| `syncMetricButtons` | 6558–6581 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6582–6588 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6589–6602 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6603–6644 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6645–6687 |  |
| `toggleBudgetPanel` | 6688–6713 |  |
| `syncMillRates` | 6714–6746 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 6747–6767 |  |
| `applyColorAdjust` | 6768–6788 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 6789–6801 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 6802–6816 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 6817–6834 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 6835–6851 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 6852–6873 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 6874–6890 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 6891–7130 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 7131–7141 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 7142–7155 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 7156–7164 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 7165–7175 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 7176–7187 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 7188–7200 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 7201–7221 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 7222–7269 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7270–7275 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7276–7297 |  |
| `applyMoneyDetail` | 7298–7322 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7323–7334 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7335–7342 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7343–7361 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7362–7372 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7373–7380 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7381–7397 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7398–7411 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7412–7422 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7423–7666 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7667–7676 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7677–7690 |  |
| `applySvcDriver` | 7691–7723 |  |

### shareable URL: the hash names the view on screen

| symbol | lines | what it does |
|---|---|---|
| `METRIC_FROM_URL` | 7724–7726 |  |
| `urlHash` | 7727–7767 |  |
| `shareLink` | 7768–7776 | Absolute on purpose: the full build carries <base href="../">, and a |
| `copyShareLink` | 7777–7788 | With no clipboard (an insecure origin, a denied permission) the link goes |
| `offered` | 7789–7795 | On screen, ignoring the Options fold: a folded panel on a phone hides |
| `applyUrlState` | 7796–7868 |  |
| `restoreFromHash` | 7869–7887 | Once, at the end of boot, after every build and data gate has run. The |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 7888–8502 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (1047 edges)

⚠️ **A regex reference count, not a call graph** — a name in a comment or string counts, and a nested symbol is attributed to its enclosing range. Use it for *what is central* and *would this seam hold*, never as ground truth for a final module boundary.

**Most depended-on** — moving one of these touches everything below it.

| symbol | referenced by | section |
|---|---|---|
| `state` | 125 | the Lab: a container for unfinished lenses |
| `buildLayers` | 39 | geographic reference layers (all views) |
| `METRICS` | 17 | tunables |
| `applyView` | 17 | control appliers + the view/legend dispatchers |
| `SERVICES` | 16 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `setBlurb` | 15 | the Lab: a container for unfinished lenses |
| `refreshLegend` | 14 | control appliers + the view/legend dispatchers |
| `CELLS` | 11 | tunables |
| `quantile` | 10 | the Lab: a container for unfinished lenses |
| `labelPool` | 10 | geographic reference layers (all views) |
| `ratioDenom` | 9 | services lens views (SPEC_services.md display architecture) |
| `ratioScale` | 9 | geographic reference layers (all views) |
| `deviationStats` | 9 | the same doubt, at 100 m |
| `esc` | 9 | money view (default): the classic metric prisms |
| `devIndustrial` | 8 | loading overlay |

**Section self-containment** — share of each section's outgoing edges that stay inside it. Low means a module cut on this banner would mostly import its neighbours.

| section | edges | self-contained |
|---|---|---|
| uses view (use-mix, 2026-07-03) | 3 | 67% |
| Infill lens (SPEC_development.md Lens B) | 27 | 67% |
| deviation lens: revenue per developed acre against peer average | 3 | 67% |
| the Lab: a container for unfinished lenses | 121 | 63% |
| tunables | 13 | 46% |
| Development 100 m detail grid (layers-panel toggle, 2026-07-15) | 9 | 44% |
| change lens: how each hood's share of the assessment base moved | 16 | 44% |
| geographic reference layers (all views) | 92 | 43% |
| loading overlay | 55 | 35% |
| two tiers, answering two different questions | 29 | 31% |
| Money's revenue panel: where a hood's levy comes from | 35 | 29% |
| Development history: new supply per year | 116 | 28% |
| the same doubt, at 100 m | 61 | 26% |
| shareable URL: the hash names the view on screen | 24 | 21% |
| services lens views (SPEC_services.md display architecture) | 5 | 20% |
| control appliers + the view/legend dispatchers | 221 | 20% |
| neighbourhood search | 114 | 11% |
| the citywide budget panel (EXPERIMENTAL, full build only) | 12 | 8% |
| services view (SPEC_services.md UI generalization, 2026-07-05) | 18 | 0% |
| the institutional uncertainty band | 2 | 0% |
| temporal lens (SPEC_temporal.md phase 3) | 4 | 0% |
| boot | 67 | 0% |

## Element ids (137) — the control surface

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
| `#title-p` | 65 |
| `#search` | 75 |
| `#search-btn` | 76 |
| `#search-box` | 79 |
| `#search-input` | 80 |
| `#search-close` | 84 |
| `#search-list` | 86 |
| `#temporal` | 93 |
| `#temporal-close` | 94 |
| `#temporal-name` | 95 |
| `#temporal-body` | 102 |
| `#temporal-chart` | 103 |
| `#temporal-read` | 104 |
| `#temporal-note` | 105 |
| `#temporal-hint` | 109 |
| `#millrates` | 125 |
| `#mill-head` | 126 |
| `#mill-rows` | 127 |
| `#mill-note` | 128 |
| `#budget` | 142 |
| `#budget-close` | 149 |
| `#budget-head` | 150 |
| `#budget-body` | 155 |
| `#budget-rows` | 156 |
| `#budget-other-hd` | 157 |
| `#budget-other` | 158 |
| `#budget-note` | 159 |
| `#peek` | 174 |
| `#peek-name` | 175 |
| `#peek-read` | 176 |
| `#peek-go` | 177 |
| `#controls` | 180 |
| `#toggle` | 193 |
| `#metric-row` | 194 |
| `#revcut` | 198 |
| `#moneymode` | 203 |
| `#views` | 209 |
| `#optpanel` | 223 |
| `#opt-fold` | 224 |
| `#opt-caret` | 224 |
| `#opt-body` | 225 |
| `#layers` | 226 |
| `#chgwindow-hd` | 227 |
| `#chgwindow` | 228 |
| `#labpick-hd` | 237 |
| `#labpick` | 238 |
| `#labcut-hd` | 239 |
| `#labcut` | 240 |
| `#moneydetail-hd` | 245 |
| `#moneydetail` | 246 |
| `#amenity-hd` | 271 |
| `#amenity` | 272 |
| `#amenity-lrt-row` | 273 |
| `#amenity-lrt-on` | 274 |
| `#amenity-school-row` | 276 |
| `#amenity-school-on` | 277 |
| `#uses-prisms-hd` | 280 |
| `#uses-prisms` | 281 |
| `#uses-prisms-on` | 283 |
| `#devmode-hd` | 286 |
| `#devmode` | 287 |
| `#devmetric-hd` | 291 |
| `#devmetric` | 292 |
| `#devwindow-hd` | 297 |
| `#devwindow` | 298 |
| `#devdetail-hd` | 303 |
| `#devdetail` | 304 |
| `#prism-hd` | 308 |
| `#prism-row` | 309 |
| `#prism-opacity` | 311 |
| `#prism-opacity-val` | 312 |
| `#services-hd` | 314 |
| `#services` | 315 |
| `#denom-hd` | 414 |
| `#denom` | 415 |
| `#ratio-denom-hd` | 419 |
| `#ratio-denom` | 420 |
| `#hoodmode` | 430 |
| `#hoodmode-btn` | 431 |
| `#coloradj` | 443 |
| `#coloradj-btn` | 444 |
| `#budget-pod` | 451 |
| `#budget-btn` | 452 |
| `#share` | 459 |
| `#share-btn` | 460 |
| `#a11y` | 463 |
| `#a11y-btn` | 464 |
| `#a11y-menu` | 465 |
| `#palette` | 467 |
| `#labels-on` | 474 |
| `#reference-on` | 482 |
| `#about` | 487 |
| `#about-btn` | 488 |
| `#about-menu` | 489 |
| `#about-src-roads` | 501 |
| `#about-src-services` | 502 |
| `#about-vintage` | 530 |
| `#about-build` | 534 |
| `#about-lot-acres` | 539 |
| `#about-modelled-roads` | 550 |
| `#about-modelled` | 572 |
| `#about-budget` | 582 |
| `#about-budget-lead` | 584 |
| `#about-budget-rows` | 585 |
| `#about-budget-note` | 586 |
| `#about-updated` | 598 |
| `#botleft` | 602 |
| `#compass` | 603 |
| `#rot-ccw` | 604 |
| `#tonorth` | 611 |
| `#needle` | 613 |
| `#rot-cw` | 618 |
| `#viewbtns` | 626 |
| `#recenter` | 628 |
| `#center2d` | 629 |
| `#legend` | 631 |
| `#legend-label` | 632 |
| `#legend-min` | 634 |
| `#legend-max` | 634 |
| `#legend-cats` | 636 |
| `#revmix` | 5404 |
| `#svccost` | 5498 |
