# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~8,068-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (309 indexed)

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
| `VIEWS` | 1242–1337 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1338–1342 | the Lab: a container for unfinished lenses |
| `inLab` | 1343–1344 |  |
| `DEVIATION_TITLES` | 1345–1349 |  |
| `deviationTitle` | 1350–1355 |  |
| `deviationKind` | 1356–1358 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1359–1364 |  |
| `changeBlurb` | 1365–1389 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1390–1411 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassInstBlurb` | 1412–1424 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1425–1436 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `amenityWhichPhrase` | 1437–1442 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1443–1448 |  |
| `infillAmenityBlurb` | 1449–1462 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1463–1474 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `devTitle` | 1475–1480 | Development blurb, in the COPY_DECISIONS B8 shape (BD1): what the lens |
| `devBlurb` | 1481–1539 |  |
| `setBlurb` | 1540–1553 | Blurb markup (COPY_DECISIONS B8): a blank line starts a new paragraph and |
| `withColourClause` | 1554–1571 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1572–1578 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1579–1592 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1593–1593 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1594–1608 |  |
| `fmtMB` | 1609–1619 |  |
| `showGridBusy` | 1620–1642 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1643–1659 |  |
| `loadGridData` | 1660–1713 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1714–1767 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1768–1792 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1793–1824 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1825–1825 |  |
| `gridFetches` | 1826–1850 |  |
| `RAMPS` | 1851–1891 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1892–1898 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1899–1904 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1905–1905 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1906–1912 |  |
| `AMENITY_BANDS` | 1913–1914 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1915–1917 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1918–1923 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1924–1938 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1939–1944 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1945–1963 |  |
| `gridScale` | 1964–1984 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 1985–1991 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1992–2003 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 2004–2006 |  |
| `quantile` | 2007–2021 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 2022–2054 |  |
| `moneyBlurb` | 2055–2059 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 2060–2072 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2073–2151 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2152–2152 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2153–2179 |  |
| `failLoading` | 2180–2193 |  |
| `hideLoading` | 2194–2248 |  |
| `topRings` | 2249–2265 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2266–2291 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2292–2292 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2293–2305 |  |
| `svcT` | 2306–2314 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2315–2328 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2329–2329 |  |
| `fmtFire` | 2330–2331 |  |
| `fmtTransit` | 2332–2333 |  |
| `fmtBike` | 2334–2346 |  |
| `fmtRoadM` | 2347–2360 |  |
| `fmtResShare` | 2361–2363 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2364–2369 |  |
| `fmtRoadsCost` | 2370–2374 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2375–2376 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2377–2378 |  |
| `fmtBikeCost` | 2379–2390 |  |
| `servicePlaneLayer` | 2391–2423 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2424–2433 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2434–2439 |  |
| `DEV_IND_TOTAL` | 2440–2442 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2443–2448 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2449–2453 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2454–2459 |  |
| `devGridOfferable` | 2460–2461 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2462–2462 |  |
| `devCol` | 2463–2463 |  |
| `_devScale` | 2464–2464 |  |
| `devScale` | 2465–2471 |  |
| `devT` | 2472–2475 |  |
| `developmentPlaneLayer` | 2476–2492 |  |
| `fmtDev` | 2493–2508 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2509–2514 |  |
| `DEV_GRID_IND_N` | 2515–2515 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2516–2518 |  |
| `devGridScale` | 2519–2545 |  |
| `devGridLayer` | 2546–2594 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2595–2596 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2597–2604 |  |
| `_infillStats` | 2605–2605 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2606–2623 |  |
| `_infillRaw` | 2624–2626 |  |
| `infillScore` | 2627–2642 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2643–2644 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2645–2662 |  |
| `INFILL_CENTER` | 2663–2663 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2664–2664 |  |
| `INFILL_NEG` | 2665–2665 |  |
| `infillColorAt` | 2666–2670 |  |
| `infillPlaneLayer` | 2671–2692 |  |
| `fmtFar` | 2693–2702 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `AMENITY_HIGHLIGHT_COLOR` | 2703–2703 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2704–2758 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2759–2766 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2767–2781 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2782–2802 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2803–2803 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2804–2818 |  |
| `chgT` | 2819–2828 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2829–2859 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2860–2948 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2949–2956 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2957–2957 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2958–2965 |  |
| `deviationRate` | 2966–3008 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 3009–3009 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 3010–3039 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3040–3046 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3047–3058 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3059–3062 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3063–3067 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3068–3078 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3079–3094 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3095–3126 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3127–3151 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `INST_OUTLINE_COLOR` | 3152–3204 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 3205–3209 |  |
| `bandHover` | 3210–3218 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3219–3315 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3316–3323 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3324–3325 |  |
| `glassInstBandLayers` | 3326–3366 |  |
| `ratioInstBandLayers` | 3367–3394 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3395–3407 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3408–3409 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3410–3411 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3412–3412 |  |
| `deviationStats` | 3413–3457 |  |
| `deviationOf` | 3458–3459 |  |
| `deviationT` | 3460–3470 |  |
| `fmtDeviation` | 3471–3492 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3493–3536 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3537–3623 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3624–3646 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3647–3647 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3648–3668 |  |
| `ensureFireStations` | 3669–3684 |  |
| `TRANSIT_STATION_COLOR` | 3685–3685 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3686–3703 |  |
| `ensureTransitStations` | 3704–3719 |  |
| `TRANSIT_LINE_COLOR` | 3720–3720 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3721–3737 |  |
| `ensureLrtLines` | 3738–3754 |  |
| `BIKE_LINE_COLOR` | 3755–3755 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3756–3772 |  |
| `ensureBikeLines` | 3773–3830 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3831–3831 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3832–3835 |  |
| `BOUNDARY_COLOR` | 3836–3845 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3846–3846 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3847–3859 |  |
| `referenceSplit` | 3860–3887 |  |
| `referenceUnderLayers` | 3888–3922 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3923–3939 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3940–3959 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3960–3972 |  |
| `servicesBlurb` | 3973–3990 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3991–4014 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 4015–4025 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 4026–4077 |  |
| `REF_TIERS` | 4078–4099 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4100–4107 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 4108–4110 |  |
| `placeAnchors` | 4111–4134 |  |
| `labelPool` | 4135–4142 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4143–4196 |  |
| `CHROME_IDS` | 4197–4201 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4202–4220 |  |
| `visibleLabels` | 4221–4275 |  |
| `labelLayer` | 4276–4312 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 4313–4313 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4314–4329 |  |
| `ratioT` | 4330–4352 |  |
| `zMatrix` | 4353–4357 |  |
| `buildLayers` | 4358–4381 |  |
| `flattenDuringEase` | 4382–4406 | Center 2D lowers the heights over the LAST QUARTER OF THE TILT instead |
| `buildViewLayers` | 4407–4716 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4717–4746 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4747–4756 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4757–4759 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 4760–4791 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4792–4798 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4799–4806 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4807–4811 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4812–4822 |  |
| `revenueLens` | 4823–4824 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4825–4857 |  |
| `SVC_COST_BASES` | 4858–4875 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 4876–4884 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 4885–4900 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 4901–4903 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 4904–4910 |  |
| `svcRank` | 4911–4915 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 4916–4922 |  |
| `svcDriverReading` | 4923–4943 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 4944–4944 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4945–4948 |  |
| `servicePanelFor` | 4949–4969 |  |
| `hoodPanelLens` | 4970–4973 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4974–4991 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4992–5023 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 5024–5029 |  |
| `sparklineSvg` | 5030–5045 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 5046–5105 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5106–5111 | Development history: new supply per year |
| `devHistKey` | 5112–5121 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5122–5126 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5127–5127 |  |
| `devHistVerb` | 5128–5133 |  |
| `devHistoryFor` | 5134–5155 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5156–5175 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5176–5195 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5196–5231 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5232–5234 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5235–5298 |  |
| `syncTemporalPos` | 5299–5325 |  |
| `openTemporal` | 5326–5360 |  |
| `renderRevenueMix` | 5361–5427 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 5428–5507 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 5508–5511 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5512–5562 |  |
| `syncPinnedPanel` | 5563–5592 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5593–5608 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5609–5626 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5627–5674 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5675–5680 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5681–5727 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5728–5744 |  |
| `temporalClick` | 5745–5802 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 5803–5871 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 5872–6252 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6253–6334 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6335–6335 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6336–6354 |  |
| `syncMetricButtons` | 6355–6378 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6379–6385 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6386–6399 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6400–6441 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6442–6484 |  |
| `toggleBudgetPanel` | 6485–6510 |  |
| `syncMillRates` | 6511–6543 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 6544–6564 |  |
| `applyColorAdjust` | 6565–6585 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 6586–6598 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 6599–6613 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 6614–6631 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 6632–6648 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 6649–6670 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 6671–6687 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 6688–6927 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 6928–6938 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 6939–6952 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 6953–6961 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 6962–6972 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 6973–6984 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 6985–6997 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 6998–7018 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 7019–7066 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7067–7072 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7073–7094 |  |
| `applyMoneyDetail` | 7095–7119 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7120–7131 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7132–7139 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7140–7158 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7159–7169 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7170–7177 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7178–7194 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7195–7208 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7209–7219 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7220–7470 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7471–7480 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7481–7494 |  |
| `applySvcDriver` | 7495–7508 |  |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 7509–8068 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (959 edges)

⚠️ **A regex reference count, not a call graph** — a name in a comment or string counts, and a nested symbol is attributed to its enclosing range. Use it for *what is central* and *would this seam hold*, never as ground truth for a final module boundary.

**Most depended-on** — moving one of these touches everything below it.

| symbol | referenced by | section |
|---|---|---|
| `state` | 118 | the Lab: a container for unfinished lenses |
| `buildLayers` | 37 | geographic reference layers (all views) |
| `METRICS` | 16 | tunables |
| `SERVICES` | 14 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `applyView` | 14 | control appliers + the view/legend dispatchers |
| `refreshLegend` | 14 | control appliers + the view/legend dispatchers |
| `setBlurb` | 14 | the Lab: a container for unfinished lenses |
| `CELLS` | 10 | tunables |
| `quantile` | 10 | the Lab: a container for unfinished lenses |
| `ratioScale` | 9 | geographic reference layers (all views) |
| `deviationStats` | 9 | the same doubt, at 100 m |
| `ratioDenom` | 8 | services lens views (SPEC_services.md display architecture) |
| `devIndustrial` | 8 | loading overlay |
| `devCol` | 8 | loading overlay |
| `exemptFrac` | 8 | the institutional uncertainty band |

**Section self-containment** — share of each section's outgoing edges that stay inside it. Low means a module cut on this banner would mostly import its neighbours.

| section | edges | self-contained |
|---|---|---|
| uses view (use-mix, 2026-07-03) | 3 | 67% |
| Infill lens (SPEC_development.md Lens B) | 27 | 67% |
| deviation lens: revenue per developed acre against peer average | 3 | 67% |
| the Lab: a container for unfinished lenses | 103 | 64% |
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
| control appliers + the view/legend dispatchers | 224 | 19% |
| the citywide budget panel (EXPERIMENTAL, full build only) | 12 | 8% |
| services view (SPEC_services.md UI generalization, 2026-07-05) | 17 | 0% |
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
| `#revmix` | 5380 |
| `#svccost` | 5471 |
