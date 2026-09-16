# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~7,889-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

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
| `METRICS` | 772–902 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 903–919 |  |
| `RATIO_DENOMS` | 920–952 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 953–953 |  |
| `ratioOf` | 954–954 |  |
| `ratioKept` | 955–976 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 977–987 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 988–1015 |  |
| `dominantUse` | 1016–1057 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1058–1227 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1228–1332 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1333–1337 | the Lab: a container for unfinished lenses |
| `inLab` | 1338–1339 |  |
| `DEVIATION_TITLES` | 1340–1344 |  |
| `deviationTitle` | 1345–1350 |  |
| `deviationKind` | 1351–1353 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1354–1359 |  |
| `changeBlurb` | 1360–1384 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1385–1406 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassInstBlurb` | 1407–1419 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1420–1431 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `amenityWhichPhrase` | 1432–1437 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1438–1443 |  |
| `infillAmenityBlurb` | 1444–1457 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1458–1472 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1473–1478 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1479–1486 |  |
| `devChoroplethBlurb` | 1487–1488 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1489–1537 |  |
| `withColourClause` | 1538–1555 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1556–1562 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1563–1576 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1577–1577 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1578–1592 |  |
| `fmtMB` | 1593–1603 |  |
| `showGridBusy` | 1604–1626 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1627–1643 |  |
| `loadGridData` | 1644–1697 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1698–1751 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1752–1776 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1777–1808 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1809–1809 |  |
| `gridFetches` | 1810–1834 |  |
| `RAMPS` | 1835–1875 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1876–1882 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1883–1888 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1889–1889 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1890–1896 |  |
| `AMENITY_BANDS` | 1897–1898 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1899–1901 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1902–1907 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1908–1922 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1923–1928 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1929–1947 |  |
| `gridScale` | 1948–1968 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 1969–1975 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1976–1987 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1988–1990 |  |
| `quantile` | 1991–2005 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 2006–2038 |  |
| `moneyBlurb` | 2039–2043 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 2044–2056 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2057–2135 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2136–2136 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2137–2163 |  |
| `failLoading` | 2164–2177 |  |
| `hideLoading` | 2178–2232 |  |
| `topRings` | 2233–2249 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2250–2275 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2276–2276 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2277–2289 |  |
| `svcT` | 2290–2294 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2295–2296 |  |
| `fmtFire` | 2297–2297 |  |
| `fmtTransit` | 2298–2299 |  |
| `fmtBike` | 2300–2300 |  |
| `fmtWater` | 2301–2306 |  |
| `fmtRoadsCost` | 2307–2311 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2312–2313 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2314–2315 |  |
| `fmtBikeCost` | 2316–2327 |  |
| `servicePlaneLayer` | 2328–2360 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2361–2370 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2371–2376 |  |
| `DEV_IND_TOTAL` | 2377–2379 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2380–2385 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2386–2390 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2391–2396 |  |
| `devGridOfferable` | 2397–2398 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2399–2399 |  |
| `devCol` | 2400–2400 |  |
| `_devScale` | 2401–2401 |  |
| `devScale` | 2402–2408 |  |
| `devT` | 2409–2412 |  |
| `developmentPlaneLayer` | 2413–2429 |  |
| `fmtDev` | 2430–2445 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2446–2451 |  |
| `DEV_GRID_IND_N` | 2452–2452 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2453–2455 |  |
| `devGridScale` | 2456–2482 |  |
| `devGridLayer` | 2483–2531 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2532–2533 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2534–2541 |  |
| `_infillStats` | 2542–2542 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2543–2560 |  |
| `_infillRaw` | 2561–2563 |  |
| `infillScore` | 2564–2579 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2580–2581 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2582–2599 |  |
| `INFILL_CENTER` | 2600–2600 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2601–2601 |  |
| `INFILL_NEG` | 2602–2602 |  |
| `infillColorAt` | 2603–2607 |  |
| `infillPlaneLayer` | 2608–2622 |  |
| `fmtFar` | 2623–2632 |  |
| `AMENITY_HIGHLIGHT_COLOR` | 2633–2633 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2634–2688 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2689–2696 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2697–2711 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2712–2732 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2733–2733 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2734–2748 |  |
| `chgT` | 2749–2758 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2759–2789 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2790–2878 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2879–2886 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2887–2887 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2888–2895 |  |
| `deviationRate` | 2896–2938 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2939–2939 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 2940–2969 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 2970–2976 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 2977–2988 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 2989–2992 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 2993–2997 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 2998–3008 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3009–3024 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3025–3056 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3057–3081 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `INST_OUTLINE_COLOR` | 3082–3134 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 3135–3139 |  |
| `bandHover` | 3140–3148 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3149–3245 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3246–3253 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3254–3255 |  |
| `glassInstBandLayers` | 3256–3296 |  |
| `ratioInstBandLayers` | 3297–3324 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3325–3337 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3338–3339 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3340–3341 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3342–3342 |  |
| `deviationStats` | 3343–3387 |  |
| `deviationOf` | 3388–3389 |  |
| `deviationT` | 3390–3400 |  |
| `fmtDeviation` | 3401–3422 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3423–3466 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3467–3553 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3554–3576 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3577–3577 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3578–3598 |  |
| `ensureFireStations` | 3599–3614 |  |
| `TRANSIT_STATION_COLOR` | 3615–3615 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3616–3633 |  |
| `ensureTransitStations` | 3634–3649 |  |
| `TRANSIT_LINE_COLOR` | 3650–3650 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3651–3667 |  |
| `ensureLrtLines` | 3668–3684 |  |
| `BIKE_LINE_COLOR` | 3685–3685 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3686–3702 |  |
| `ensureBikeLines` | 3703–3760 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3761–3761 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3762–3765 |  |
| `BOUNDARY_COLOR` | 3766–3775 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3776–3776 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3777–3789 |  |
| `referenceSplit` | 3790–3817 |  |
| `referenceUnderLayers` | 3818–3852 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3853–3869 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3870–3889 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3890–3902 |  |
| `servicesBlurb` | 3903–3920 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3921–3944 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 3945–3955 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 3956–4007 |  |
| `REF_TIERS` | 4008–4029 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4030–4037 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 4038–4040 |  |
| `placeAnchors` | 4041–4064 |  |
| `labelPool` | 4065–4072 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4073–4126 |  |
| `CHROME_IDS` | 4127–4131 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4132–4150 |  |
| `visibleLabels` | 4151–4205 |  |
| `labelLayer` | 4206–4242 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 4243–4243 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4244–4259 |  |
| `ratioT` | 4260–4270 |  |
| `buildLayers` | 4271–4283 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 4284–4593 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4594–4623 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4624–4627 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4628–4630 |  |
| `fmtBig` | 4631–4658 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4659–4664 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4665–4672 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4673–4677 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4678–4688 |  |
| `revenueLens` | 4689–4690 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4691–4722 |  |
| `SVC_COST_BASES` | 4723–4738 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 4739–4747 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 4748–4763 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 4764–4766 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 4767–4773 |  |
| `svcRank` | 4774–4778 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 4779–4785 |  |
| `svcDriverReading` | 4786–4806 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 4807–4807 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4808–4811 |  |
| `servicePanelFor` | 4812–4832 |  |
| `hoodPanelLens` | 4833–4836 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4837–4854 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4855–4886 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 4887–4892 |  |
| `sparklineSvg` | 4893–4908 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 4909–4968 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 4969–4974 | Development history: new supply per year |
| `devHistKey` | 4975–4984 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 4985–4989 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 4990–4990 |  |
| `devHistVerb` | 4991–4996 |  |
| `devHistoryFor` | 4997–5018 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5019–5038 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5039–5058 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5059–5094 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5095–5097 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5098–5161 |  |
| `syncTemporalPos` | 5162–5188 |  |
| `openTemporal` | 5189–5223 |  |
| `renderRevenueMix` | 5224–5290 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 5291–5358 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 5359–5361 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5362–5412 |  |
| `syncPinnedPanel` | 5413–5442 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5443–5458 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5459–5476 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5477–5524 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5525–5530 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5531–5577 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5578–5594 |  |
| `temporalClick` | 5595–5652 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 5653–5721 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 5722–6081 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6082–6163 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6164–6164 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6165–6183 |  |
| `syncMetricButtons` | 6184–6207 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6208–6214 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6215–6228 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6229–6270 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6271–6313 |  |
| `toggleBudgetPanel` | 6314–6339 |  |
| `syncMillRates` | 6340–6372 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 6373–6394 |  |
| `applyColorAdjust` | 6395–6416 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 6417–6429 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 6430–6445 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 6446–6463 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 6464–6480 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 6481–6502 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 6503–6519 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 6520–6759 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 6760–6770 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 6771–6784 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 6785–6793 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 6794–6804 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 6805–6816 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 6817–6830 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 6831–6851 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 6852–6899 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 6900–6905 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 6906–6927 |  |
| `applyMoneyDetail` | 6928–6952 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 6953–6964 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 6965–6972 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 6973–6991 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 6992–7002 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7003–7010 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7011–7027 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7028–7041 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7042–7052 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7053–7304 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7305–7314 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7315–7328 |  |
| `applySvcDriver` | 7329–7342 |  |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 7343–7889 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (922 edges)

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
| tunables | 11 | 55% |
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
| `#revmix` | 5243 |
| `#svccost` | 5328 |
