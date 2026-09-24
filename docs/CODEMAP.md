# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~8,023-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (310 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 643–647 |  |
| `HOME` | 648–648 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 649–662 |  |
| `WINDOWS` | 663–688 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 689–698 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 699–703 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 704–779 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `money0` | 780–782 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `fmtMoney` | 783–784 |  |
| `METRICS` | 785–887 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 888–904 |  |
| `RATIO_DENOMS` | 905–938 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 939–939 |  |
| `ratioOf` | 940–940 |  |
| `ratioKept` | 941–962 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 963–973 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 974–1001 |  |
| `dominantUse` | 1002–1043 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1044–1194 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1195–1290 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1291–1295 | the Lab: a container for unfinished lenses |
| `inLab` | 1296–1297 |  |
| `DEVIATION_TITLES` | 1298–1302 |  |
| `deviationTitle` | 1303–1308 |  |
| `deviationKind` | 1309–1311 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1312–1319 |  |
| `changeBlurb` | 1320–1337 | Change-lens blurb (COPY_DECISIONS BC1, B8 shape). It follows the window |
| `glassLead` | 1338–1350 | Grid blurb (COPY_DECISIONS BG1, B8 shape). Names the metric (B6) and the |
| `glassInstBlurb` | 1351–1363 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1364–1375 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `amenityWhichPhrase` | 1376–1381 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1382–1389 |  |
| `infillAmenityBlurb` | 1390–1403 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1404–1415 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `devTitle` | 1416–1421 | Development blurb, in the COPY_DECISIONS B8 shape (BD1): what the lens |
| `devBlurb` | 1422–1480 |  |
| `setBlurb` | 1481–1493 | Blurb markup (COPY_DECISIONS B8): a blank line starts a new paragraph and |
| `currentBlurb` | 1494–1509 | The active view's blurb. Read by applyView and by the camera's 2D/3D flip |
| `withColourClause` | 1510–1527 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1528–1534 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1535–1548 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1549–1549 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1550–1564 |  |
| `fmtMB` | 1565–1575 |  |
| `showGridBusy` | 1576–1598 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1599–1615 |  |
| `loadGridData` | 1616–1669 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1670–1723 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1724–1748 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1749–1780 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1781–1781 |  |
| `gridFetches` | 1782–1806 |  |
| `RAMPS` | 1807–1847 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1848–1854 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1855–1860 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1861–1861 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1862–1868 |  |
| `AMENITY_BANDS` | 1869–1870 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1871–1873 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1874–1879 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1880–1894 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1895–1900 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1901–1919 |  |
| `gridScale` | 1920–1940 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 1941–1947 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1948–1959 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1960–1962 |  |
| `quantile` | 1963–1977 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1978–2012 |  |
| `moneyBlurb` | 2013–2024 | The money blurb (COPY_DECISIONS BM1, B8 shape): the metric's own P1 under |
| `fillFor` | 2025–2037 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2038–2116 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2117–2117 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2118–2144 |  |
| `failLoading` | 2145–2158 |  |
| `hideLoading` | 2159–2213 |  |
| `topRings` | 2214–2230 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2231–2256 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2257–2257 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2258–2270 |  |
| `svcT` | 2271–2279 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2280–2293 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2294–2294 |  |
| `fmtFire` | 2295–2296 |  |
| `fmtTransit` | 2297–2298 |  |
| `fmtBike` | 2299–2311 |  |
| `fmtRoadM` | 2312–2325 |  |
| `fmtResShare` | 2326–2328 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2329–2334 |  |
| `fmtRoadsCost` | 2335–2339 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2340–2341 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2342–2343 |  |
| `fmtBikeCost` | 2344–2355 |  |
| `servicePlaneLayer` | 2356–2388 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2389–2398 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2399–2404 |  |
| `DEV_IND_TOTAL` | 2405–2407 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2408–2413 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2414–2418 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2419–2424 |  |
| `devGridOfferable` | 2425–2426 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2427–2427 |  |
| `devCol` | 2428–2428 |  |
| `_devScale` | 2429–2429 |  |
| `devScale` | 2430–2436 |  |
| `devT` | 2437–2440 |  |
| `developmentPlaneLayer` | 2441–2457 |  |
| `fmtDev` | 2458–2473 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2474–2479 |  |
| `DEV_GRID_IND_N` | 2480–2480 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2481–2483 |  |
| `devGridScale` | 2484–2510 |  |
| `devGridLayer` | 2511–2559 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2560–2561 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2562–2569 |  |
| `_infillStats` | 2570–2570 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2571–2588 |  |
| `_infillRaw` | 2589–2591 |  |
| `infillScore` | 2592–2607 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2608–2609 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2610–2627 |  |
| `INFILL_CENTER` | 2628–2628 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2629–2629 |  |
| `INFILL_NEG` | 2630–2630 |  |
| `infillColorAt` | 2631–2635 |  |
| `infillPlaneLayer` | 2636–2657 |  |
| `fmtFar` | 2658–2667 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `AMENITY_HIGHLIGHT_COLOR` | 2668–2668 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2669–2723 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2724–2731 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2732–2746 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2747–2767 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2768–2768 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2769–2783 |  |
| `chgT` | 2784–2793 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2794–2824 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2825–2913 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2914–2921 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2922–2922 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2923–2930 |  |
| `deviationRate` | 2931–2973 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2974–2974 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 2975–3004 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3005–3011 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3012–3023 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3024–3027 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3028–3032 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3033–3043 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3044–3059 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3060–3091 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3092–3116 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `INST_OUTLINE_COLOR` | 3117–3169 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 3170–3174 |  |
| `bandHover` | 3175–3183 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3184–3280 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3281–3288 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3289–3290 |  |
| `glassInstBandLayers` | 3291–3331 |  |
| `ratioInstBandLayers` | 3332–3359 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3360–3372 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3373–3374 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3375–3376 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3377–3377 |  |
| `deviationStats` | 3378–3422 |  |
| `deviationOf` | 3423–3424 |  |
| `deviationT` | 3425–3435 |  |
| `fmtDeviation` | 3436–3457 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3458–3501 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3502–3588 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3589–3611 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3612–3612 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3613–3633 |  |
| `ensureFireStations` | 3634–3649 |  |
| `TRANSIT_STATION_COLOR` | 3650–3650 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3651–3668 |  |
| `ensureTransitStations` | 3669–3684 |  |
| `TRANSIT_LINE_COLOR` | 3685–3685 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3686–3702 |  |
| `ensureLrtLines` | 3703–3719 |  |
| `BIKE_LINE_COLOR` | 3720–3720 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3721–3737 |  |
| `ensureBikeLines` | 3738–3795 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3796–3796 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3797–3800 |  |
| `BOUNDARY_COLOR` | 3801–3810 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3811–3811 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3812–3824 |  |
| `referenceSplit` | 3825–3852 |  |
| `referenceUnderLayers` | 3853–3887 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3888–3904 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3905–3924 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3925–3938 |  |
| `servicesBlurb` | 3939–3950 | Services-view blurb (COPY_DECISIONS BS1, B8 shape): the colour-driving |
| `hoodHoverLayer` | 3951–3974 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 3975–3985 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 3986–4037 |  |
| `REF_TIERS` | 4038–4059 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4060–4067 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 4068–4070 |  |
| `placeAnchors` | 4071–4094 |  |
| `labelPool` | 4095–4102 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4103–4156 |  |
| `CHROME_IDS` | 4157–4161 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4162–4180 |  |
| `visibleLabels` | 4181–4235 |  |
| `labelLayer` | 4236–4272 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 4273–4273 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4274–4289 |  |
| `ratioT` | 4290–4312 |  |
| `zMatrix` | 4313–4317 |  |
| `buildLayers` | 4318–4341 |  |
| `flattenDuringEase` | 4342–4366 | Center 2D lowers the heights over the LAST QUARTER OF THE TILT instead |
| `buildViewLayers` | 4367–4676 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4677–4706 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4707–4716 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4717–4719 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 4720–4751 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4752–4758 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4759–4766 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4767–4771 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4772–4782 |  |
| `revenueLens` | 4783–4784 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4785–4817 |  |
| `SVC_COST_BASES` | 4818–4835 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 4836–4844 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 4845–4860 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 4861–4863 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 4864–4870 |  |
| `svcRank` | 4871–4875 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 4876–4882 |  |
| `svcDriverReading` | 4883–4903 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 4904–4904 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4905–4908 |  |
| `servicePanelFor` | 4909–4929 |  |
| `hoodPanelLens` | 4930–4933 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4934–4951 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4952–4983 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 4984–4989 |  |
| `sparklineSvg` | 4990–5005 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 5006–5065 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5066–5071 | Development history: new supply per year |
| `devHistKey` | 5072–5081 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5082–5086 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5087–5087 |  |
| `devHistVerb` | 5088–5093 |  |
| `devHistoryFor` | 5094–5115 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5116–5135 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5136–5155 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5156–5191 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5192–5194 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5195–5258 |  |
| `syncTemporalPos` | 5259–5285 |  |
| `openTemporal` | 5286–5320 |  |
| `renderRevenueMix` | 5321–5387 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 5388–5467 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 5468–5471 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5472–5522 |  |
| `syncPinnedPanel` | 5523–5552 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5553–5568 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5569–5586 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5587–5634 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5635–5640 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5641–5687 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5688–5704 |  |
| `temporalClick` | 5705–5762 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 5763–5831 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 5832–6212 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6213–6294 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6295–6295 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6296–6314 |  |
| `syncMetricButtons` | 6315–6338 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6339–6345 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6346–6359 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6360–6401 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6402–6444 |  |
| `toggleBudgetPanel` | 6445–6470 |  |
| `syncMillRates` | 6471–6503 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 6504–6524 |  |
| `applyColorAdjust` | 6525–6545 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 6546–6558 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 6559–6573 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 6574–6591 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 6592–6608 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 6609–6630 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 6631–6647 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 6648–6887 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 6888–6898 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 6899–6912 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 6913–6921 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 6922–6932 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 6933–6944 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 6945–6957 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 6958–6978 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 6979–7026 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7027–7032 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7033–7054 |  |
| `applyMoneyDetail` | 7055–7079 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7080–7091 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7092–7099 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7100–7118 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7119–7129 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7130–7137 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7138–7154 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7155–7168 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7169–7179 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7180–7423 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7424–7433 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7434–7447 |  |
| `applySvcDriver` | 7448–7461 |  |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 7462–8023 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (968 edges)

⚠️ **A regex reference count, not a call graph** — a name in a comment or string counts, and a nested symbol is attributed to its enclosing range. Use it for *what is central* and *would this seam hold*, never as ground truth for a final module boundary.

**Most depended-on** — moving one of these touches everything below it.

| symbol | referenced by | section |
|---|---|---|
| `state` | 119 | the Lab: a container for unfinished lenses |
| `buildLayers` | 37 | geographic reference layers (all views) |
| `METRICS` | 17 | tunables |
| `applyView` | 15 | control appliers + the view/legend dispatchers |
| `setBlurb` | 15 | the Lab: a container for unfinished lenses |
| `SERVICES` | 14 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `refreshLegend` | 14 | control appliers + the view/legend dispatchers |
| `CELLS` | 10 | tunables |
| `quantile` | 10 | the Lab: a container for unfinished lenses |
| `ratioDenom` | 9 | services lens views (SPEC_services.md display architecture) |
| `ratioScale` | 9 | geographic reference layers (all views) |
| `deviationStats` | 9 | the same doubt, at 100 m |
| `devIndustrial` | 8 | loading overlay |
| `devCol` | 8 | loading overlay |
| `exemptFrac` | 8 | the institutional uncertainty band |

**Section self-containment** — share of each section's outgoing edges that stay inside it. Low means a module cut on this banner would mostly import its neighbours.

| section | edges | self-contained |
|---|---|---|
| uses view (use-mix, 2026-07-03) | 3 | 67% |
| Infill lens (SPEC_development.md Lens B) | 27 | 67% |
| deviation lens: revenue per developed acre against peer average | 3 | 67% |
| the Lab: a container for unfinished lenses | 118 | 64% |
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
| control appliers + the view/legend dispatchers | 216 | 20% |
| the citywide budget panel (EXPERIMENTAL, full build only) | 12 | 8% |
| services view (SPEC_services.md UI generalization, 2026-07-05) | 17 | 0% |
| the institutional uncertainty band | 2 | 0% |
| temporal lens (SPEC_temporal.md phase 3) | 4 | 0% |
| boot | 59 | 0% |

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
| `#title-p` | 65 |
| `#temporal` | 75 |
| `#temporal-close` | 76 |
| `#temporal-name` | 77 |
| `#temporal-body` | 84 |
| `#temporal-chart` | 85 |
| `#temporal-read` | 86 |
| `#temporal-note` | 87 |
| `#temporal-hint` | 91 |
| `#millrates` | 107 |
| `#mill-head` | 108 |
| `#mill-rows` | 109 |
| `#mill-note` | 110 |
| `#budget` | 124 |
| `#budget-close` | 131 |
| `#budget-head` | 132 |
| `#budget-body` | 137 |
| `#budget-rows` | 138 |
| `#budget-other-hd` | 139 |
| `#budget-other` | 140 |
| `#budget-note` | 141 |
| `#peek` | 156 |
| `#peek-name` | 157 |
| `#peek-read` | 158 |
| `#peek-go` | 159 |
| `#controls` | 162 |
| `#toggle` | 175 |
| `#metric-row` | 176 |
| `#revcut` | 180 |
| `#moneymode` | 185 |
| `#views` | 191 |
| `#optpanel` | 205 |
| `#opt-fold` | 206 |
| `#opt-caret` | 206 |
| `#opt-body` | 207 |
| `#layers` | 208 |
| `#chgwindow-hd` | 209 |
| `#chgwindow` | 210 |
| `#labpick-hd` | 219 |
| `#labpick` | 220 |
| `#labcut-hd` | 221 |
| `#labcut` | 222 |
| `#moneydetail-hd` | 227 |
| `#moneydetail` | 228 |
| `#amenity-hd` | 253 |
| `#amenity` | 254 |
| `#amenity-lrt-row` | 255 |
| `#amenity-lrt-on` | 256 |
| `#amenity-school-row` | 258 |
| `#amenity-school-on` | 259 |
| `#uses-prisms-hd` | 262 |
| `#uses-prisms` | 263 |
| `#uses-prisms-on` | 265 |
| `#devmode-hd` | 268 |
| `#devmode` | 269 |
| `#devmetric-hd` | 273 |
| `#devmetric` | 274 |
| `#devwindow-hd` | 279 |
| `#devwindow` | 280 |
| `#devdetail-hd` | 285 |
| `#devdetail` | 286 |
| `#prism-hd` | 290 |
| `#prism-row` | 291 |
| `#prism-opacity` | 293 |
| `#prism-opacity-val` | 294 |
| `#services-hd` | 296 |
| `#services` | 297 |
| `#denom-hd` | 396 |
| `#denom` | 397 |
| `#ratio-denom-hd` | 401 |
| `#ratio-denom` | 402 |
| `#hoodmode` | 412 |
| `#hoodmode-btn` | 413 |
| `#coloradj` | 425 |
| `#coloradj-btn` | 426 |
| `#budget-pod` | 433 |
| `#budget-btn` | 434 |
| `#a11y` | 438 |
| `#a11y-btn` | 439 |
| `#a11y-menu` | 440 |
| `#palette` | 442 |
| `#labels-on` | 449 |
| `#reference-on` | 457 |
| `#about` | 462 |
| `#about-btn` | 463 |
| `#about-menu` | 464 |
| `#about-src-roads` | 476 |
| `#about-src-services` | 477 |
| `#about-vintage` | 505 |
| `#about-build` | 509 |
| `#about-modelled-roads` | 523 |
| `#about-modelled` | 541 |
| `#about-budget` | 551 |
| `#about-budget-lead` | 553 |
| `#about-budget-rows` | 554 |
| `#about-budget-note` | 555 |
| `#about-updated` | 566 |
| `#botleft` | 570 |
| `#compass` | 571 |
| `#rot-ccw` | 572 |
| `#tonorth` | 579 |
| `#needle` | 581 |
| `#rot-cw` | 586 |
| `#viewbtns` | 594 |
| `#recenter` | 596 |
| `#center2d` | 597 |
| `#legend` | 599 |
| `#legend-label` | 600 |
| `#legend-min` | 602 |
| `#legend-max` | 602 |
| `#legend-cats` | 604 |
| `#revmix` | 5340 |
| `#svccost` | 5431 |
