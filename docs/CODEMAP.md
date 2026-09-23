# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~8,071-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

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
| `devTitle` | 1493–1500 |  |
| `devChoroplethBlurb` | 1501–1502 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1503–1551 |  |
| `withColourClause` | 1552–1569 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1570–1576 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1577–1590 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1591–1591 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1592–1606 |  |
| `fmtMB` | 1607–1617 |  |
| `showGridBusy` | 1618–1640 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1641–1657 |  |
| `loadGridData` | 1658–1711 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1712–1765 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1766–1790 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1791–1822 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1823–1823 |  |
| `gridFetches` | 1824–1848 |  |
| `RAMPS` | 1849–1889 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1890–1896 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1897–1902 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1903–1903 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1904–1910 |  |
| `AMENITY_BANDS` | 1911–1912 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1913–1915 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1916–1921 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1922–1936 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1937–1942 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1943–1961 |  |
| `gridScale` | 1962–1982 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 1983–1989 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1990–2001 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 2002–2004 |  |
| `quantile` | 2005–2019 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 2020–2052 |  |
| `moneyBlurb` | 2053–2057 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 2058–2070 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2071–2149 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2150–2150 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2151–2177 |  |
| `failLoading` | 2178–2191 |  |
| `hideLoading` | 2192–2246 |  |
| `topRings` | 2247–2263 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2264–2289 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2290–2290 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2291–2303 |  |
| `svcT` | 2304–2312 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2313–2326 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2327–2327 |  |
| `fmtFire` | 2328–2329 |  |
| `fmtTransit` | 2330–2331 |  |
| `fmtBike` | 2332–2344 |  |
| `fmtRoadM` | 2345–2358 |  |
| `fmtResShare` | 2359–2361 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2362–2367 |  |
| `fmtRoadsCost` | 2368–2372 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2373–2374 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2375–2376 |  |
| `fmtBikeCost` | 2377–2388 |  |
| `servicePlaneLayer` | 2389–2421 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2422–2431 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2432–2437 |  |
| `DEV_IND_TOTAL` | 2438–2440 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2441–2446 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2447–2451 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2452–2457 |  |
| `devGridOfferable` | 2458–2459 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2460–2460 |  |
| `devCol` | 2461–2461 |  |
| `_devScale` | 2462–2462 |  |
| `devScale` | 2463–2469 |  |
| `devT` | 2470–2473 |  |
| `developmentPlaneLayer` | 2474–2490 |  |
| `fmtDev` | 2491–2506 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2507–2512 |  |
| `DEV_GRID_IND_N` | 2513–2513 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2514–2516 |  |
| `devGridScale` | 2517–2543 |  |
| `devGridLayer` | 2544–2592 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2593–2594 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2595–2602 |  |
| `_infillStats` | 2603–2603 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2604–2621 |  |
| `_infillRaw` | 2622–2624 |  |
| `infillScore` | 2625–2640 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2641–2642 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2643–2660 |  |
| `INFILL_CENTER` | 2661–2661 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2662–2662 |  |
| `INFILL_NEG` | 2663–2663 |  |
| `infillColorAt` | 2664–2668 |  |
| `infillPlaneLayer` | 2669–2690 |  |
| `fmtFar` | 2691–2700 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `AMENITY_HIGHLIGHT_COLOR` | 2701–2701 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2702–2756 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2757–2764 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2765–2779 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2780–2800 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2801–2801 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2802–2816 |  |
| `chgT` | 2817–2826 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2827–2857 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2858–2946 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2947–2954 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2955–2955 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2956–2963 |  |
| `deviationRate` | 2964–3006 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 3007–3007 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 3008–3037 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3038–3044 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3045–3056 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3057–3060 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3061–3065 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3066–3076 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3077–3092 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3093–3124 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3125–3149 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `INST_OUTLINE_COLOR` | 3150–3202 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 3203–3207 |  |
| `bandHover` | 3208–3216 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3217–3313 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3314–3321 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3322–3323 |  |
| `glassInstBandLayers` | 3324–3364 |  |
| `ratioInstBandLayers` | 3365–3392 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3393–3405 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3406–3407 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3408–3409 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3410–3410 |  |
| `deviationStats` | 3411–3455 |  |
| `deviationOf` | 3456–3457 |  |
| `deviationT` | 3458–3468 |  |
| `fmtDeviation` | 3469–3490 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3491–3534 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3535–3621 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3622–3644 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3645–3645 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3646–3666 |  |
| `ensureFireStations` | 3667–3682 |  |
| `TRANSIT_STATION_COLOR` | 3683–3683 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3684–3701 |  |
| `ensureTransitStations` | 3702–3717 |  |
| `TRANSIT_LINE_COLOR` | 3718–3718 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3719–3735 |  |
| `ensureLrtLines` | 3736–3752 |  |
| `BIKE_LINE_COLOR` | 3753–3753 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3754–3770 |  |
| `ensureBikeLines` | 3771–3828 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3829–3829 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3830–3833 |  |
| `BOUNDARY_COLOR` | 3834–3843 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3844–3844 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3845–3857 |  |
| `referenceSplit` | 3858–3885 |  |
| `referenceUnderLayers` | 3886–3920 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3921–3937 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3938–3957 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3958–3970 |  |
| `servicesBlurb` | 3971–3988 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3989–4012 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 4013–4023 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 4024–4075 |  |
| `REF_TIERS` | 4076–4097 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4098–4105 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 4106–4108 |  |
| `placeAnchors` | 4109–4132 |  |
| `labelPool` | 4133–4140 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4141–4194 |  |
| `CHROME_IDS` | 4195–4199 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4200–4218 |  |
| `visibleLabels` | 4219–4273 |  |
| `labelLayer` | 4274–4310 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 4311–4311 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4312–4327 |  |
| `ratioT` | 4328–4350 |  |
| `zMatrix` | 4351–4355 |  |
| `buildLayers` | 4356–4379 |  |
| `flattenDuringEase` | 4380–4404 | Center 2D lowers the heights over the LAST QUARTER OF THE TILT instead |
| `buildViewLayers` | 4405–4714 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4715–4744 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4745–4754 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4755–4757 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 4758–4789 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4790–4796 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4797–4804 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4805–4809 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4810–4820 |  |
| `revenueLens` | 4821–4822 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4823–4855 |  |
| `SVC_COST_BASES` | 4856–4873 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 4874–4882 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 4883–4898 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 4899–4901 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 4902–4908 |  |
| `svcRank` | 4909–4913 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 4914–4920 |  |
| `svcDriverReading` | 4921–4941 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 4942–4942 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4943–4946 |  |
| `servicePanelFor` | 4947–4967 |  |
| `hoodPanelLens` | 4968–4971 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4972–4989 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4990–5021 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 5022–5027 |  |
| `sparklineSvg` | 5028–5043 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 5044–5103 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5104–5109 | Development history: new supply per year |
| `devHistKey` | 5110–5119 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5120–5124 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5125–5125 |  |
| `devHistVerb` | 5126–5131 |  |
| `devHistoryFor` | 5132–5153 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5154–5173 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5174–5193 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5194–5229 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5230–5232 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5233–5296 |  |
| `syncTemporalPos` | 5297–5323 |  |
| `openTemporal` | 5324–5358 |  |
| `renderRevenueMix` | 5359–5425 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 5426–5505 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 5506–5509 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5510–5560 |  |
| `syncPinnedPanel` | 5561–5590 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5591–5606 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5607–5624 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5625–5672 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5673–5678 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5679–5725 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5726–5742 |  |
| `temporalClick` | 5743–5800 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 5801–5869 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 5870–6250 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6251–6332 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6333–6333 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6334–6352 |  |
| `syncMetricButtons` | 6353–6376 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6377–6383 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6384–6397 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6398–6439 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6440–6482 |  |
| `toggleBudgetPanel` | 6483–6508 |  |
| `syncMillRates` | 6509–6541 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 6542–6563 |  |
| `applyColorAdjust` | 6564–6585 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 6586–6598 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 6599–6614 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 6615–6632 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 6633–6649 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 6650–6671 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 6672–6688 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 6689–6928 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 6929–6939 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 6940–6953 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 6954–6962 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 6963–6973 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 6974–6985 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 6986–6999 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 7000–7020 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 7021–7068 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7069–7074 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7075–7096 |  |
| `applyMoneyDetail` | 7097–7121 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7122–7133 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7134–7141 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7142–7160 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7161–7171 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7172–7179 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7180–7196 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7197–7210 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7211–7221 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7222–7473 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7474–7483 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7484–7497 |  |
| `applySvcDriver` | 7498–7511 |  |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 7512–8071 | Everything that needs the map surface: fetch the data, mount the deck.gl |

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
| `#recenter` | 595 |
| `#center2d` | 596 |
| `#legend` | 598 |
| `#legend-label` | 599 |
| `#legend-min` | 601 |
| `#legend-max` | 601 |
| `#legend-cats` | 603 |
| `#revmix` | 5378 |
| `#svccost` | 5469 |
