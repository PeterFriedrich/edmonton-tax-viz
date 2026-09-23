# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~8,070-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (310 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 641–645 |  |
| `HOME` | 646–646 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 647–660 |  |
| `WINDOWS` | 661–686 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 687–696 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 697–701 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 702–777 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `money0` | 778–780 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `fmtMoney` | 781–782 |  |
| `METRICS` | 783–913 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 914–930 |  |
| `RATIO_DENOMS` | 931–964 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 965–965 |  |
| `ratioOf` | 966–966 |  |
| `ratioKept` | 967–988 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 989–999 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 1000–1027 |  |
| `dominantUse` | 1028–1069 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1070–1240 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1241–1345 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1346–1350 | the Lab: a container for unfinished lenses |
| `inLab` | 1351–1352 |  |
| `DEVIATION_TITLES` | 1353–1357 |  |
| `deviationTitle` | 1358–1363 |  |
| `deviationKind` | 1364–1366 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1367–1372 |  |
| `changeBlurb` | 1373–1397 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1398–1419 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassInstBlurb` | 1420–1432 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1433–1444 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `amenityWhichPhrase` | 1445–1450 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1451–1456 |  |
| `infillAmenityBlurb` | 1457–1470 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1471–1485 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1486–1491 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1492–1499 |  |
| `devChoroplethBlurb` | 1500–1501 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1502–1550 |  |
| `withColourClause` | 1551–1568 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1569–1575 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1576–1589 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1590–1590 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1591–1605 |  |
| `fmtMB` | 1606–1616 |  |
| `showGridBusy` | 1617–1639 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1640–1656 |  |
| `loadGridData` | 1657–1710 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1711–1764 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1765–1789 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1790–1821 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1822–1822 |  |
| `gridFetches` | 1823–1847 |  |
| `RAMPS` | 1848–1888 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1889–1895 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1896–1901 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1902–1902 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1903–1909 |  |
| `AMENITY_BANDS` | 1910–1911 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1912–1914 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1915–1920 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1921–1935 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1936–1941 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1942–1960 |  |
| `gridScale` | 1961–1981 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 1982–1988 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1989–2000 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 2001–2003 |  |
| `quantile` | 2004–2018 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 2019–2051 |  |
| `moneyBlurb` | 2052–2056 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 2057–2069 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2070–2148 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2149–2149 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2150–2176 |  |
| `failLoading` | 2177–2190 |  |
| `hideLoading` | 2191–2245 |  |
| `topRings` | 2246–2262 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2263–2288 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2289–2289 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2290–2302 |  |
| `svcT` | 2303–2311 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2312–2325 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2326–2326 |  |
| `fmtFire` | 2327–2328 |  |
| `fmtTransit` | 2329–2330 |  |
| `fmtBike` | 2331–2343 |  |
| `fmtRoadM` | 2344–2357 |  |
| `fmtResShare` | 2358–2360 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2361–2366 |  |
| `fmtRoadsCost` | 2367–2371 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2372–2373 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2374–2375 |  |
| `fmtBikeCost` | 2376–2387 |  |
| `servicePlaneLayer` | 2388–2420 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2421–2430 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2431–2436 |  |
| `DEV_IND_TOTAL` | 2437–2439 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2440–2445 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2446–2450 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2451–2456 |  |
| `devGridOfferable` | 2457–2458 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2459–2459 |  |
| `devCol` | 2460–2460 |  |
| `_devScale` | 2461–2461 |  |
| `devScale` | 2462–2468 |  |
| `devT` | 2469–2472 |  |
| `developmentPlaneLayer` | 2473–2489 |  |
| `fmtDev` | 2490–2505 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2506–2511 |  |
| `DEV_GRID_IND_N` | 2512–2512 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2513–2515 |  |
| `devGridScale` | 2516–2542 |  |
| `devGridLayer` | 2543–2591 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2592–2593 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2594–2601 |  |
| `_infillStats` | 2602–2602 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2603–2620 |  |
| `_infillRaw` | 2621–2623 |  |
| `infillScore` | 2624–2639 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2640–2641 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2642–2659 |  |
| `INFILL_CENTER` | 2660–2660 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2661–2661 |  |
| `INFILL_NEG` | 2662–2662 |  |
| `infillColorAt` | 2663–2667 |  |
| `infillPlaneLayer` | 2668–2689 |  |
| `fmtFar` | 2690–2699 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `AMENITY_HIGHLIGHT_COLOR` | 2700–2700 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2701–2755 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2756–2763 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2764–2778 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2779–2799 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2800–2800 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2801–2815 |  |
| `chgT` | 2816–2825 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2826–2856 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2857–2945 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2946–2953 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2954–2954 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2955–2962 |  |
| `deviationRate` | 2963–3005 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 3006–3006 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 3007–3036 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3037–3043 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3044–3055 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3056–3059 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3060–3064 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3065–3075 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3076–3091 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3092–3123 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3124–3148 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `INST_OUTLINE_COLOR` | 3149–3201 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 3202–3206 |  |
| `bandHover` | 3207–3215 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3216–3312 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3313–3320 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3321–3322 |  |
| `glassInstBandLayers` | 3323–3363 |  |
| `ratioInstBandLayers` | 3364–3391 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3392–3404 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3405–3406 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3407–3408 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3409–3409 |  |
| `deviationStats` | 3410–3454 |  |
| `deviationOf` | 3455–3456 |  |
| `deviationT` | 3457–3467 |  |
| `fmtDeviation` | 3468–3489 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3490–3533 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3534–3620 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3621–3643 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3644–3644 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3645–3665 |  |
| `ensureFireStations` | 3666–3681 |  |
| `TRANSIT_STATION_COLOR` | 3682–3682 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3683–3700 |  |
| `ensureTransitStations` | 3701–3716 |  |
| `TRANSIT_LINE_COLOR` | 3717–3717 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3718–3734 |  |
| `ensureLrtLines` | 3735–3751 |  |
| `BIKE_LINE_COLOR` | 3752–3752 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3753–3769 |  |
| `ensureBikeLines` | 3770–3827 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3828–3828 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3829–3832 |  |
| `BOUNDARY_COLOR` | 3833–3842 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3843–3843 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3844–3856 |  |
| `referenceSplit` | 3857–3884 |  |
| `referenceUnderLayers` | 3885–3919 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3920–3936 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3937–3956 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3957–3969 |  |
| `servicesBlurb` | 3970–3987 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3988–4011 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 4012–4022 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 4023–4074 |  |
| `REF_TIERS` | 4075–4096 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4097–4104 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 4105–4107 |  |
| `placeAnchors` | 4108–4131 |  |
| `labelPool` | 4132–4139 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4140–4193 |  |
| `CHROME_IDS` | 4194–4198 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4199–4217 |  |
| `visibleLabels` | 4218–4272 |  |
| `labelLayer` | 4273–4309 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 4310–4310 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4311–4326 |  |
| `ratioT` | 4327–4349 |  |
| `zMatrix` | 4350–4354 |  |
| `buildLayers` | 4355–4378 |  |
| `flattenDuringEase` | 4379–4403 | Center 2D lowers the heights over the LAST QUARTER OF THE TILT instead |
| `buildViewLayers` | 4404–4713 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4714–4743 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4744–4753 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4754–4756 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 4757–4788 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4789–4795 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4796–4803 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4804–4808 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4809–4819 |  |
| `revenueLens` | 4820–4821 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4822–4854 |  |
| `SVC_COST_BASES` | 4855–4872 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 4873–4881 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 4882–4897 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 4898–4900 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 4901–4907 |  |
| `svcRank` | 4908–4912 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 4913–4919 |  |
| `svcDriverReading` | 4920–4940 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 4941–4941 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4942–4945 |  |
| `servicePanelFor` | 4946–4966 |  |
| `hoodPanelLens` | 4967–4970 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4971–4988 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4989–5020 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 5021–5026 |  |
| `sparklineSvg` | 5027–5042 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 5043–5102 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5103–5108 | Development history: new supply per year |
| `devHistKey` | 5109–5118 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5119–5123 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5124–5124 |  |
| `devHistVerb` | 5125–5130 |  |
| `devHistoryFor` | 5131–5152 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5153–5172 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5173–5192 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5193–5228 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5229–5231 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5232–5295 |  |
| `syncTemporalPos` | 5296–5322 |  |
| `openTemporal` | 5323–5357 |  |
| `renderRevenueMix` | 5358–5424 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 5425–5504 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 5505–5508 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5509–5559 |  |
| `syncPinnedPanel` | 5560–5589 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5590–5605 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5606–5623 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5624–5671 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5672–5677 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5678–5724 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5725–5741 |  |
| `temporalClick` | 5742–5799 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 5800–5868 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 5869–6249 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6250–6331 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6332–6332 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6333–6351 |  |
| `syncMetricButtons` | 6352–6375 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6376–6382 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6383–6396 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6397–6438 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6439–6481 |  |
| `toggleBudgetPanel` | 6482–6507 |  |
| `syncMillRates` | 6508–6540 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 6541–6562 |  |
| `applyColorAdjust` | 6563–6584 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 6585–6597 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 6598–6613 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
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
| `applyAmenity` | 6985–6998 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 6999–7019 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 7020–7067 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7068–7073 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7074–7095 |  |
| `applyMoneyDetail` | 7096–7120 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7121–7132 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7133–7140 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7141–7159 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7160–7170 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7171–7178 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7179–7195 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7196–7209 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7210–7220 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7221–7472 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7473–7482 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7483–7496 |  |
| `applySvcDriver` | 7497–7510 |  |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 7511–8070 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (950 edges)

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
| the Lab: a container for unfinished lenses | 109 | 65% |
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
| `#center2d` | 594 |
| `#recenter` | 595 |
| `#legend` | 597 |
| `#legend-label` | 598 |
| `#legend-min` | 600 |
| `#legend-max` | 600 |
| `#legend-cats` | 602 |
| `#revmix` | 5377 |
| `#svccost` | 5468 |
