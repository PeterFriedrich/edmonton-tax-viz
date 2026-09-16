# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~7,884-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (304 indexed)

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
| `TOKENS` | 702–769 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `fmtMoney` | 770–771 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `METRICS` | 772–897 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 898–914 |  |
| `RATIO_DENOMS` | 915–947 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 948–948 |  |
| `ratioOf` | 949–949 |  |
| `ratioKept` | 950–971 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 972–982 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 983–1010 |  |
| `dominantUse` | 1011–1052 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1053–1222 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1223–1327 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1328–1332 | the Lab: a container for unfinished lenses |
| `inLab` | 1333–1334 |  |
| `DEVIATION_TITLES` | 1335–1339 |  |
| `deviationTitle` | 1340–1345 |  |
| `deviationKind` | 1346–1348 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1349–1354 |  |
| `changeBlurb` | 1355–1379 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1380–1401 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassInstBlurb` | 1402–1414 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1415–1426 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `amenityWhichPhrase` | 1427–1432 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1433–1438 |  |
| `infillAmenityBlurb` | 1439–1452 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1453–1467 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1468–1473 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1474–1481 |  |
| `devChoroplethBlurb` | 1482–1483 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1484–1532 |  |
| `withColourClause` | 1533–1550 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1551–1557 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1558–1571 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1572–1572 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1573–1587 |  |
| `fmtMB` | 1588–1598 |  |
| `showGridBusy` | 1599–1621 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1622–1638 |  |
| `loadGridData` | 1639–1692 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1693–1746 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1747–1771 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1772–1803 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1804–1804 |  |
| `gridFetches` | 1805–1829 |  |
| `RAMPS` | 1830–1870 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1871–1877 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1878–1883 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1884–1884 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1885–1891 |  |
| `AMENITY_BANDS` | 1892–1893 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1894–1896 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1897–1902 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1903–1917 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1918–1923 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1924–1942 |  |
| `gridScale` | 1943–1963 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 1964–1970 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1971–1982 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1983–1985 |  |
| `quantile` | 1986–2000 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 2001–2033 |  |
| `moneyBlurb` | 2034–2038 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 2039–2051 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2052–2130 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2131–2131 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2132–2158 |  |
| `failLoading` | 2159–2172 |  |
| `hideLoading` | 2173–2227 |  |
| `topRings` | 2228–2244 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2245–2270 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2271–2271 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2272–2284 |  |
| `svcT` | 2285–2289 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2290–2291 |  |
| `fmtFire` | 2292–2292 |  |
| `fmtTransit` | 2293–2294 |  |
| `fmtBike` | 2295–2295 |  |
| `fmtWater` | 2296–2301 |  |
| `fmtRoadsCost` | 2302–2306 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2307–2308 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2309–2310 |  |
| `fmtBikeCost` | 2311–2322 |  |
| `servicePlaneLayer` | 2323–2355 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2356–2365 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2366–2371 |  |
| `DEV_IND_TOTAL` | 2372–2374 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2375–2380 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2381–2385 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2386–2391 |  |
| `devGridOfferable` | 2392–2393 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2394–2394 |  |
| `devCol` | 2395–2395 |  |
| `_devScale` | 2396–2396 |  |
| `devScale` | 2397–2403 |  |
| `devT` | 2404–2407 |  |
| `developmentPlaneLayer` | 2408–2424 |  |
| `fmtDev` | 2425–2440 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2441–2446 |  |
| `DEV_GRID_IND_N` | 2447–2447 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2448–2450 |  |
| `devGridScale` | 2451–2477 |  |
| `devGridLayer` | 2478–2526 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2527–2528 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2529–2536 |  |
| `_infillStats` | 2537–2537 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2538–2555 |  |
| `_infillRaw` | 2556–2558 |  |
| `infillScore` | 2559–2574 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2575–2576 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2577–2594 |  |
| `INFILL_CENTER` | 2595–2595 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2596–2596 |  |
| `INFILL_NEG` | 2597–2597 |  |
| `infillColorAt` | 2598–2602 |  |
| `infillPlaneLayer` | 2603–2617 |  |
| `fmtFar` | 2618–2627 |  |
| `AMENITY_HIGHLIGHT_COLOR` | 2628–2628 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2629–2683 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2684–2691 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2692–2706 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2707–2727 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2728–2728 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2729–2743 |  |
| `chgT` | 2744–2753 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2754–2784 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2785–2873 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2874–2881 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2882–2882 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2883–2890 |  |
| `deviationRate` | 2891–2933 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2934–2934 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 2935–2964 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 2965–2971 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 2972–2983 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 2984–2987 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 2988–2992 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 2993–3003 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3004–3019 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3020–3051 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3052–3076 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `INST_OUTLINE_COLOR` | 3077–3129 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 3130–3134 |  |
| `bandHover` | 3135–3143 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3144–3240 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3241–3248 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3249–3250 |  |
| `glassInstBandLayers` | 3251–3291 |  |
| `ratioInstBandLayers` | 3292–3319 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3320–3332 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3333–3334 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3335–3336 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3337–3337 |  |
| `deviationStats` | 3338–3382 |  |
| `deviationOf` | 3383–3384 |  |
| `deviationT` | 3385–3395 |  |
| `fmtDeviation` | 3396–3417 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3418–3461 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3462–3548 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3549–3571 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3572–3572 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3573–3593 |  |
| `ensureFireStations` | 3594–3609 |  |
| `TRANSIT_STATION_COLOR` | 3610–3610 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3611–3628 |  |
| `ensureTransitStations` | 3629–3644 |  |
| `TRANSIT_LINE_COLOR` | 3645–3645 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3646–3662 |  |
| `ensureLrtLines` | 3663–3679 |  |
| `BIKE_LINE_COLOR` | 3680–3680 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3681–3697 |  |
| `ensureBikeLines` | 3698–3755 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3756–3756 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3757–3760 |  |
| `BOUNDARY_COLOR` | 3761–3770 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3771–3771 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3772–3784 |  |
| `referenceSplit` | 3785–3812 |  |
| `referenceUnderLayers` | 3813–3847 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3848–3864 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3865–3884 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3885–3897 |  |
| `servicesBlurb` | 3898–3915 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3916–3939 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 3940–3950 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 3951–4002 |  |
| `REF_TIERS` | 4003–4024 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4025–4032 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 4033–4035 |  |
| `placeAnchors` | 4036–4059 |  |
| `labelPool` | 4060–4067 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4068–4121 |  |
| `CHROME_IDS` | 4122–4126 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4127–4145 |  |
| `visibleLabels` | 4146–4200 |  |
| `labelLayer` | 4201–4237 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 4238–4238 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4239–4254 |  |
| `ratioT` | 4255–4265 |  |
| `buildLayers` | 4266–4278 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 4279–4588 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4589–4618 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4619–4622 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4623–4625 |  |
| `fmtBig` | 4626–4653 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4654–4659 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4660–4667 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4668–4672 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4673–4683 |  |
| `revenueLens` | 4684–4685 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4686–4717 |  |
| `SVC_COST_BASES` | 4718–4733 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 4734–4742 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 4743–4758 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 4759–4761 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 4762–4768 |  |
| `svcRank` | 4769–4773 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 4774–4780 |  |
| `svcDriverReading` | 4781–4801 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 4802–4802 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4803–4806 |  |
| `servicePanelFor` | 4807–4827 |  |
| `hoodPanelLens` | 4828–4831 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4832–4849 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4850–4881 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 4882–4887 |  |
| `sparklineSvg` | 4888–4903 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 4904–4963 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 4964–4969 | Development history: new supply per year |
| `devHistKey` | 4970–4979 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 4980–4984 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 4985–4985 |  |
| `devHistVerb` | 4986–4991 |  |
| `devHistoryFor` | 4992–5013 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5014–5033 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5034–5053 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5054–5089 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5090–5092 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5093–5156 |  |
| `syncTemporalPos` | 5157–5183 |  |
| `openTemporal` | 5184–5218 |  |
| `renderRevenueMix` | 5219–5285 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 5286–5353 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 5354–5356 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5357–5407 |  |
| `syncPinnedPanel` | 5408–5437 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5438–5453 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5454–5471 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5472–5519 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5520–5525 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5526–5572 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5573–5589 |  |
| `temporalClick` | 5590–5647 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 5648–5716 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 5717–6076 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6077–6158 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6159–6159 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6160–6178 |  |
| `syncMetricButtons` | 6179–6202 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6203–6209 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6210–6223 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6224–6265 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6266–6308 |  |
| `toggleBudgetPanel` | 6309–6334 |  |
| `syncMillRates` | 6335–6367 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 6368–6389 |  |
| `applyColorAdjust` | 6390–6411 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 6412–6424 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 6425–6440 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 6441–6458 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 6459–6475 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 6476–6497 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 6498–6514 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 6515–6754 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 6755–6765 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 6766–6779 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 6780–6788 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 6789–6799 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 6800–6811 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 6812–6825 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 6826–6846 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 6847–6894 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 6895–6900 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 6901–6922 |  |
| `applyMoneyDetail` | 6923–6947 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 6948–6959 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 6960–6967 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 6968–6986 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 6987–6997 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 6998–7005 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7006–7022 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7023–7036 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7037–7047 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7048–7299 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7300–7309 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7310–7323 |  |
| `applySvcDriver` | 7324–7337 |  |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 7338–7884 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (921 edges)

⚠️ **A regex reference count, not a call graph** — a name in a comment or string counts, and a nested symbol is attributed to its enclosing range. Use it for *what is central* and *would this seam hold*, never as ground truth for a final module boundary.

**Most depended-on** — moving one of these touches everything below it.

| symbol | referenced by | section |
|---|---|---|
| `state` | 119 | the Lab: a container for unfinished lenses |
| `buildLayers` | 35 | geographic reference layers (all views) |
| `METRICS` | 16 | tunables |
| `SERVICES` | 14 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `refreshLegend` | 14 | control appliers + the view/legend dispatchers |
| `applyView` | 13 | control appliers + the view/legend dispatchers |
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
| services lens views (SPEC_services.md display architecture) | 1 | 100% |
| uses view (use-mix, 2026-07-03) | 3 | 67% |
| deviation lens: revenue per developed acre against peer average | 3 | 67% |
| Infill lens (SPEC_development.md Lens B) | 26 | 65% |
| the Lab: a container for unfinished lenses | 109 | 65% |
| tunables | 10 | 60% |
| Development 100 m detail grid (layers-panel toggle, 2026-07-15) | 9 | 44% |
| change lens: how each hood's share of the assessment base moved | 16 | 44% |
| geographic reference layers (all views) | 87 | 41% |
| loading overlay | 49 | 39% |
| two tiers, answering two different questions | 29 | 31% |
| Money's revenue panel: where a hood's levy comes from | 33 | 27% |
| the same doubt, at 100 m | 61 | 26% |
| Development history: new supply per year | 188 | 25% |
| control appliers + the view/legend dispatchers | 210 | 20% |
| the citywide budget panel (EXPERIMENTAL, full build only) | 12 | 8% |
| services view (SPEC_services.md UI generalization, 2026-07-05) | 16 | 0% |
| the institutional uncertainty band | 2 | 0% |
| temporal lens (SPEC_temporal.md phase 3) | 1 | 0% |
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
| `#revmix` | 5238 |
| `#svccost` | 5323 |
