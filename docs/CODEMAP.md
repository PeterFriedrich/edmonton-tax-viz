# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~7,994-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (308 indexed)

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
| `RATIO_DENOMS` | 931–963 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 964–964 |  |
| `ratioOf` | 965–965 |  |
| `ratioKept` | 966–987 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 988–998 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 999–1026 |  |
| `dominantUse` | 1027–1068 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1069–1239 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1240–1344 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1345–1349 | the Lab: a container for unfinished lenses |
| `inLab` | 1350–1351 |  |
| `DEVIATION_TITLES` | 1352–1356 |  |
| `deviationTitle` | 1357–1362 |  |
| `deviationKind` | 1363–1365 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1366–1371 |  |
| `changeBlurb` | 1372–1396 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1397–1418 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassInstBlurb` | 1419–1431 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1432–1443 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `amenityWhichPhrase` | 1444–1449 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1450–1455 |  |
| `infillAmenityBlurb` | 1456–1469 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1470–1484 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1485–1490 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1491–1498 |  |
| `devChoroplethBlurb` | 1499–1500 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1501–1549 |  |
| `withColourClause` | 1550–1567 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1568–1574 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1575–1588 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1589–1589 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1590–1604 |  |
| `fmtMB` | 1605–1615 |  |
| `showGridBusy` | 1616–1638 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1639–1655 |  |
| `loadGridData` | 1656–1709 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1710–1763 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1764–1788 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1789–1820 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1821–1821 |  |
| `gridFetches` | 1822–1846 |  |
| `RAMPS` | 1847–1887 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1888–1894 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1895–1900 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1901–1901 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1902–1908 |  |
| `AMENITY_BANDS` | 1909–1910 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1911–1913 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1914–1919 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1920–1934 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1935–1940 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1941–1959 |  |
| `gridScale` | 1960–1980 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 1981–1987 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1988–1999 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 2000–2002 |  |
| `quantile` | 2003–2017 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 2018–2050 |  |
| `moneyBlurb` | 2051–2055 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 2056–2068 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2069–2147 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2148–2148 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2149–2175 |  |
| `failLoading` | 2176–2189 |  |
| `hideLoading` | 2190–2244 |  |
| `topRings` | 2245–2261 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2262–2287 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2288–2288 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2289–2301 |  |
| `svcT` | 2302–2310 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2311–2322 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2323–2323 |  |
| `fmtFire` | 2324–2325 |  |
| `fmtTransit` | 2326–2327 |  |
| `fmtBike` | 2328–2339 |  |
| `fmtRoadM` | 2340–2350 |  |
| `fmtResShare` | 2351–2352 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2353–2358 |  |
| `fmtRoadsCost` | 2359–2363 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2364–2365 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2366–2367 |  |
| `fmtBikeCost` | 2368–2379 |  |
| `servicePlaneLayer` | 2380–2412 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2413–2422 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2423–2428 |  |
| `DEV_IND_TOTAL` | 2429–2431 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2432–2437 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2438–2442 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2443–2448 |  |
| `devGridOfferable` | 2449–2450 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2451–2451 |  |
| `devCol` | 2452–2452 |  |
| `_devScale` | 2453–2453 |  |
| `devScale` | 2454–2460 |  |
| `devT` | 2461–2464 |  |
| `developmentPlaneLayer` | 2465–2481 |  |
| `fmtDev` | 2482–2497 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2498–2503 |  |
| `DEV_GRID_IND_N` | 2504–2504 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2505–2507 |  |
| `devGridScale` | 2508–2534 |  |
| `devGridLayer` | 2535–2583 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2584–2585 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2586–2593 |  |
| `_infillStats` | 2594–2594 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2595–2612 |  |
| `_infillRaw` | 2613–2615 |  |
| `infillScore` | 2616–2631 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2632–2633 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2634–2651 |  |
| `INFILL_CENTER` | 2652–2652 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2653–2653 |  |
| `INFILL_NEG` | 2654–2654 |  |
| `infillColorAt` | 2655–2659 |  |
| `infillPlaneLayer` | 2660–2681 |  |
| `fmtFar` | 2682–2691 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `AMENITY_HIGHLIGHT_COLOR` | 2692–2692 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2693–2747 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2748–2755 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2756–2770 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2771–2791 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2792–2792 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2793–2807 |  |
| `chgT` | 2808–2817 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2818–2848 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2849–2937 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2938–2945 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2946–2946 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2947–2954 |  |
| `deviationRate` | 2955–2997 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2998–2998 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 2999–3028 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3029–3035 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3036–3047 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3048–3051 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3052–3056 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3057–3067 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3068–3083 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3084–3115 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3116–3140 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `INST_OUTLINE_COLOR` | 3141–3193 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 3194–3198 |  |
| `bandHover` | 3199–3207 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3208–3304 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3305–3312 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3313–3314 |  |
| `glassInstBandLayers` | 3315–3355 |  |
| `ratioInstBandLayers` | 3356–3383 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3384–3396 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3397–3398 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3399–3400 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3401–3401 |  |
| `deviationStats` | 3402–3446 |  |
| `deviationOf` | 3447–3448 |  |
| `deviationT` | 3449–3459 |  |
| `fmtDeviation` | 3460–3481 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3482–3525 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3526–3612 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3613–3635 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3636–3636 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3637–3657 |  |
| `ensureFireStations` | 3658–3673 |  |
| `TRANSIT_STATION_COLOR` | 3674–3674 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3675–3692 |  |
| `ensureTransitStations` | 3693–3708 |  |
| `TRANSIT_LINE_COLOR` | 3709–3709 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3710–3726 |  |
| `ensureLrtLines` | 3727–3743 |  |
| `BIKE_LINE_COLOR` | 3744–3744 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3745–3761 |  |
| `ensureBikeLines` | 3762–3819 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3820–3820 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3821–3824 |  |
| `BOUNDARY_COLOR` | 3825–3834 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3835–3835 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3836–3848 |  |
| `referenceSplit` | 3849–3876 |  |
| `referenceUnderLayers` | 3877–3911 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3912–3928 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3929–3948 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3949–3961 |  |
| `servicesBlurb` | 3962–3979 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3980–4003 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 4004–4014 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 4015–4066 |  |
| `REF_TIERS` | 4067–4088 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4089–4096 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 4097–4099 |  |
| `placeAnchors` | 4100–4123 |  |
| `labelPool` | 4124–4131 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4132–4185 |  |
| `CHROME_IDS` | 4186–4190 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4191–4209 |  |
| `visibleLabels` | 4210–4264 |  |
| `labelLayer` | 4265–4301 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 4302–4302 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4303–4318 |  |
| `ratioT` | 4319–4329 |  |
| `buildLayers` | 4330–4342 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 4343–4652 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4653–4682 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4683–4692 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4693–4695 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 4696–4727 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4728–4734 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4735–4742 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4743–4747 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4748–4758 |  |
| `revenueLens` | 4759–4760 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4761–4793 |  |
| `SVC_COST_BASES` | 4794–4811 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 4812–4820 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 4821–4836 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 4837–4839 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 4840–4846 |  |
| `svcRank` | 4847–4851 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 4852–4858 |  |
| `svcDriverReading` | 4859–4879 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 4880–4880 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4881–4884 |  |
| `servicePanelFor` | 4885–4905 |  |
| `hoodPanelLens` | 4906–4909 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4910–4927 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4928–4959 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 4960–4965 |  |
| `sparklineSvg` | 4966–4981 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 4982–5041 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5042–5047 | Development history: new supply per year |
| `devHistKey` | 5048–5057 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5058–5062 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5063–5063 |  |
| `devHistVerb` | 5064–5069 |  |
| `devHistoryFor` | 5070–5091 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5092–5111 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5112–5131 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5132–5167 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5168–5170 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5171–5234 |  |
| `syncTemporalPos` | 5235–5261 |  |
| `openTemporal` | 5262–5296 |  |
| `renderRevenueMix` | 5297–5363 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 5364–5443 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 5444–5447 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5448–5498 |  |
| `syncPinnedPanel` | 5499–5528 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5529–5544 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5545–5562 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5563–5610 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5611–5616 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5617–5663 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5664–5680 |  |
| `temporalClick` | 5681–5738 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 5739–5807 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 5808–6186 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6187–6268 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6269–6269 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6270–6288 |  |
| `syncMetricButtons` | 6289–6312 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6313–6319 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6320–6333 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6334–6375 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6376–6418 |  |
| `toggleBudgetPanel` | 6419–6444 |  |
| `syncMillRates` | 6445–6477 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 6478–6499 |  |
| `applyColorAdjust` | 6500–6521 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 6522–6534 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 6535–6550 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 6551–6568 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 6569–6585 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 6586–6607 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 6608–6624 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 6625–6864 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 6865–6875 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 6876–6889 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 6890–6898 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 6899–6909 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 6910–6921 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 6922–6935 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 6936–6956 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 6957–7004 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7005–7010 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7011–7032 |  |
| `applyMoneyDetail` | 7033–7057 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7058–7069 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7070–7077 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7078–7096 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7097–7107 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7108–7115 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7116–7132 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7133–7146 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7147–7157 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7158–7409 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7410–7419 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7420–7433 |  |
| `applySvcDriver` | 7434–7447 |  |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 7448–7994 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (942 edges)

⚠️ **A regex reference count, not a call graph** — a name in a comment or string counts, and a nested symbol is attributed to its enclosing range. Use it for *what is central* and *would this seam hold*, never as ground truth for a final module boundary.

**Most depended-on** — moving one of these touches everything below it.

| symbol | referenced by | section |
|---|---|---|
| `state` | 119 | the Lab: a container for unfinished lenses |
| `buildLayers` | 35 | geographic reference layers (all views) |
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
| services lens views (SPEC_services.md display architecture) | 2 | 50% |
| tunables | 13 | 46% |
| Development 100 m detail grid (layers-panel toggle, 2026-07-15) | 9 | 44% |
| change lens: how each hood's share of the assessment base moved | 16 | 44% |
| geographic reference layers (all views) | 87 | 41% |
| loading overlay | 56 | 36% |
| two tiers, answering two different questions | 29 | 31% |
| Money's revenue panel: where a hood's levy comes from | 34 | 26% |
| the same doubt, at 100 m | 61 | 26% |
| Development history: new supply per year | 193 | 24% |
| control appliers + the view/legend dispatchers | 210 | 20% |
| the citywide budget panel (EXPERIMENTAL, full build only) | 12 | 8% |
| services view (SPEC_services.md UI generalization, 2026-07-05) | 16 | 0% |
| the institutional uncertainty band | 2 | 0% |
| temporal lens (SPEC_temporal.md phase 3) | 4 | 0% |
| boot | 56 | 0% |

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
| `#revmix` | 5316 |
| `#svccost` | 5407 |
