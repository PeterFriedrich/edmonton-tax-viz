# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~7,134-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (275 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 583–587 |  |
| `HOME` | 588–588 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 589–602 |  |
| `WINDOWS` | 603–621 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 622–631 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 632–636 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 637–700 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `fmtMoney` | 701–702 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `METRICS` | 703–828 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 829–845 |  |
| `RATIO_DENOMS` | 846–907 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 908–908 |  |
| `ratioOf` | 909–909 |  |
| `ratioKept` | 910–931 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 932–942 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 943–970 |  |
| `dominantUse` | 971–1004 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1005–1159 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1160–1264 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1265–1269 | the Lab: a container for unfinished lenses |
| `inLab` | 1270–1271 |  |
| `DEVIATION_TITLES` | 1272–1276 |  |
| `deviationTitle` | 1277–1282 |  |
| `deviationKind` | 1283–1285 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1286–1291 |  |
| `changeBlurb` | 1292–1316 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1317–1338 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassInstBlurb` | 1339–1349 | The azure cells need a sentence for the same reason the Lab's outlined |
| `amenityWhichPhrase` | 1350–1355 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1356–1361 |  |
| `infillAmenityBlurb` | 1362–1375 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1376–1390 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1391–1396 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1397–1404 |  |
| `devChoroplethBlurb` | 1405–1406 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1407–1455 |  |
| `withColourClause` | 1456–1473 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1474–1480 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1481–1492 | The Detail button that selects a resolution, for the busy state in |
| `ensureGridData` | 1493–1590 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `state` | 1591–1622 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1623–1623 |  |
| `gridFetches` | 1624–1647 |  |
| `RAMPS` | 1648–1688 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1689–1695 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1696–1701 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1702–1702 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1703–1709 |  |
| `AMENITY_BANDS` | 1710–1711 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1712–1714 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1715–1720 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1721–1735 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1736–1741 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1742–1760 |  |
| `gridScale` | 1761–1781 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 1782–1788 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1789–1800 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1801–1803 |  |
| `quantile` | 1804–1818 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1819–1851 |  |
| `moneyBlurb` | 1852–1856 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1857–1869 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1870–1948 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 1949–1949 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 1950–1976 |  |
| `failLoading` | 1977–1990 |  |
| `hideLoading` | 1991–2016 |  |
| `topRings` | 2017–2033 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2034–2059 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2060–2060 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2061–2073 |  |
| `svcT` | 2074–2078 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2079–2080 |  |
| `fmtFire` | 2081–2081 |  |
| `fmtTransit` | 2082–2083 |  |
| `fmtBike` | 2084–2084 |  |
| `fmtWater` | 2085–2087 |  |
| `fmtSvcCost` | 2088–2092 |  |
| `fmtRoadsCost` | 2093–2094 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtTransitCost` | 2095–2096 |  |
| `fmtBikeCost` | 2097–2108 |  |
| `servicePlaneLayer` | 2109–2141 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2142–2151 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2152–2157 |  |
| `DEV_IND_TOTAL` | 2158–2160 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2161–2166 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2167–2171 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2172–2177 |  |
| `devGridOfferable` | 2178–2179 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2180–2180 |  |
| `devCol` | 2181–2181 |  |
| `_devScale` | 2182–2182 |  |
| `devScale` | 2183–2189 |  |
| `devT` | 2190–2193 |  |
| `developmentPlaneLayer` | 2194–2210 |  |
| `fmtDev` | 2211–2226 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2227–2232 |  |
| `DEV_GRID_IND_N` | 2233–2233 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2234–2236 |  |
| `devGridScale` | 2237–2263 |  |
| `devGridLayer` | 2264–2312 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2313–2314 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2315–2322 |  |
| `_infillStats` | 2323–2323 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2324–2341 |  |
| `_infillRaw` | 2342–2344 |  |
| `infillScore` | 2345–2360 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2361–2362 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2363–2380 |  |
| `INFILL_CENTER` | 2381–2381 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2382–2382 |  |
| `INFILL_NEG` | 2383–2383 |  |
| `infillColorAt` | 2384–2388 |  |
| `infillPlaneLayer` | 2389–2403 |  |
| `fmtFar` | 2404–2413 |  |
| `AMENITY_HIGHLIGHT_COLOR` | 2414–2414 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2415–2469 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2470–2477 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2478–2492 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2493–2513 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2514–2514 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2515–2529 |  |
| `chgT` | 2530–2539 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2540–2570 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2571–2659 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2660–2667 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2668–2668 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2669–2676 |  |
| `deviationRate` | 2677–2719 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2720–2720 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 2721–2750 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 2751–2757 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 2758–2769 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 2770–2773 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 2774–2778 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 2779–2789 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 2790–2805 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 2806–2832 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `INST_OUTLINE_COLOR` | 2833–2885 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 2886–2890 |  |
| `bandHover` | 2891–2899 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 2900–2996 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 2997–3004 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3005–3006 |  |
| `glassInstBandLayers` | 3007–3035 |  |
| `deviationRateExempt` | 3036–3048 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3049–3050 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3051–3052 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3053–3053 |  |
| `deviationStats` | 3054–3098 |  |
| `deviationOf` | 3099–3100 |  |
| `deviationT` | 3101–3111 |  |
| `fmtDeviation` | 3112–3133 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3134–3177 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3178–3264 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3265–3287 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3288–3288 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3289–3309 |  |
| `ensureFireStations` | 3310–3325 |  |
| `TRANSIT_STATION_COLOR` | 3326–3326 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3327–3344 |  |
| `ensureTransitStations` | 3345–3360 |  |
| `TRANSIT_LINE_COLOR` | 3361–3361 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3362–3378 |  |
| `ensureLrtLines` | 3379–3395 |  |
| `BIKE_LINE_COLOR` | 3396–3396 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3397–3413 |  |
| `ensureBikeLines` | 3414–3471 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3472–3472 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3473–3476 |  |
| `BOUNDARY_COLOR` | 3477–3486 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3487–3487 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3488–3500 |  |
| `referenceSplit` | 3501–3528 |  |
| `referenceUnderLayers` | 3529–3563 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3564–3580 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3581–3600 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3601–3613 |  |
| `servicesBlurb` | 3614–3631 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3632–3655 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 3656–3666 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 3667–3718 |  |
| `REF_TIERS` | 3719–3740 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 3741–3748 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 3749–3751 |  |
| `placeAnchors` | 3752–3775 |  |
| `labelPool` | 3776–3783 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 3784–3837 |  |
| `CHROME_IDS` | 3838–3841 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 3842–3860 |  |
| `visibleLabels` | 3861–3915 |  |
| `labelLayer` | 3916–3952 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 3953–3953 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 3954–3969 |  |
| `ratioT` | 3970–3980 |  |
| `buildLayers` | 3981–3993 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 3994–4296 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4297–4326 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4327–4330 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4331–4333 |  |
| `fmtBig` | 4334–4361 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4362–4367 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4368–4375 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4376–4380 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4381–4391 |  |
| `revenueLens` | 4392–4393 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4394–4411 |  |
| `SVC_COST_BASES` | 4412–4424 | The Services panel: this hood's revenue per acre set against what the City |
| `serviceLens` | 4425–4425 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4426–4428 |  |
| `servicePanelFor` | 4429–4442 |  |
| `hoodPanelLens` | 4443–4446 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4447–4464 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4465–4496 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 4497–4502 |  |
| `sparklineSvg` | 4503–4518 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 4519–4588 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 4589–4615 |  |
| `openTemporal` | 4616–4644 |  |
| `renderRevenueMix` | 4645–4693 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 4694–4727 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 4728–4730 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 4731–4781 |  |
| `syncPinnedPanel` | 4782–4808 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 4809–4824 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 4825–4835 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 4836–4883 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 4884–4889 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 4890–4929 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 4930–4946 |  |
| `temporalClick` | 4947–5004 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 5005–5084 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 5085–5417 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 5418–5485 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 5486–5486 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 5487–5505 |  |
| `syncMetricButtons` | 5506–5529 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 5530–5536 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 5537–5550 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 5551–5592 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 5593–5635 |  |
| `toggleBudgetPanel` | 5636–5661 |  |
| `syncMillRates` | 5662–5692 | Paint the pod, gate it to the money view's revenue cuts, and place it. |
| `applyMetric` | 5693–5714 |  |
| `applyColorAdjust` | 5715–5736 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 5737–5749 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 5750–5765 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 5766–5783 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 5784–5800 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 5801–5816 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 5817–5833 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 5834–6073 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 6074–6084 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 6085–6098 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 6099–6107 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 6108–6118 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 6119–6130 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 6131–6144 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 6145–6165 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 6166–6213 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 6214–6219 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 6220–6241 |  |
| `applyMoneyDetail` | 6242–6266 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 6267–6278 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 6279–6286 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 6287–6305 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 6306–6316 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 6317–6324 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 6325–6341 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 6342–6355 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 6356–6366 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 6367–6610 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 6611–6620 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 6621–6634 |  |
| `applySvcDriver` | 6635–7134 |  |

## Element ids (122) — the control surface

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
| `#title` | 44 |
| `#title-h` | 45 |
| `#title-p` | 46 |
| `#temporal` | 57 |
| `#temporal-close` | 58 |
| `#temporal-name` | 59 |
| `#temporal-body` | 66 |
| `#temporal-chart` | 67 |
| `#temporal-read` | 68 |
| `#temporal-note` | 69 |
| `#temporal-hint` | 73 |
| `#millrates` | 89 |
| `#mill-head` | 90 |
| `#mill-rows` | 91 |
| `#mill-note` | 92 |
| `#budget` | 106 |
| `#budget-close` | 113 |
| `#budget-head` | 114 |
| `#budget-body` | 119 |
| `#budget-rows` | 120 |
| `#budget-other-hd` | 121 |
| `#budget-other` | 122 |
| `#budget-note` | 123 |
| `#peek` | 138 |
| `#peek-name` | 139 |
| `#peek-read` | 140 |
| `#peek-go` | 141 |
| `#controls` | 144 |
| `#toggle` | 157 |
| `#metric-row` | 158 |
| `#revcut` | 162 |
| `#moneymode` | 167 |
| `#views` | 173 |
| `#optpanel` | 187 |
| `#opt-fold` | 188 |
| `#opt-caret` | 188 |
| `#opt-body` | 189 |
| `#layers` | 190 |
| `#chgwindow-hd` | 191 |
| `#chgwindow` | 192 |
| `#labpick-hd` | 201 |
| `#labpick` | 202 |
| `#labcut-hd` | 203 |
| `#labcut` | 204 |
| `#moneydetail-hd` | 209 |
| `#moneydetail` | 210 |
| `#amenity-hd` | 235 |
| `#amenity` | 236 |
| `#amenity-lrt-row` | 237 |
| `#amenity-lrt-on` | 238 |
| `#amenity-school-row` | 240 |
| `#amenity-school-on` | 241 |
| `#uses-prisms-hd` | 244 |
| `#uses-prisms` | 245 |
| `#uses-prisms-on` | 247 |
| `#devmode-hd` | 250 |
| `#devmode` | 251 |
| `#devmetric-hd` | 255 |
| `#devmetric` | 256 |
| `#devwindow-hd` | 261 |
| `#devwindow` | 262 |
| `#devdetail-hd` | 267 |
| `#devdetail` | 268 |
| `#prism-hd` | 272 |
| `#prism-row` | 273 |
| `#prism-opacity` | 275 |
| `#prism-opacity-val` | 276 |
| `#services-hd` | 278 |
| `#services` | 279 |
| `#denom-hd` | 373 |
| `#denom` | 374 |
| `#ratio-denom-hd` | 378 |
| `#ratio-denom` | 379 |
| `#hoodmode` | 390 |
| `#hoodmode-btn` | 391 |
| `#coloradj` | 403 |
| `#coloradj-btn` | 404 |
| `#budget-pod` | 411 |
| `#budget-btn` | 412 |
| `#a11y` | 416 |
| `#a11y-btn` | 417 |
| `#a11y-menu` | 418 |
| `#palette` | 420 |
| `#labels-on` | 427 |
| `#reference-on` | 435 |
| `#about` | 440 |
| `#about-btn` | 441 |
| `#about-menu` | 442 |
| `#about-src-services` | 451 |
| `#about-vintage` | 479 |
| `#about-build` | 483 |
| `#about-modelled` | 490 |
| `#about-budget` | 500 |
| `#about-budget-lead` | 502 |
| `#about-budget-rows` | 503 |
| `#about-budget-note` | 504 |
| `#about-updated` | 515 |
| `#botleft` | 519 |
| `#compass` | 520 |
| `#rot-ccw` | 521 |
| `#tonorth` | 528 |
| `#needle` | 530 |
| `#rot-cw` | 535 |
| `#viewbtns` | 543 |
| `#center2d` | 544 |
| `#recenter` | 545 |
| `#legend` | 547 |
| `#legend-label` | 548 |
| `#legend-min` | 550 |
| `#legend-max` | 550 |
| `#legend-cats` | 552 |
| `#revmix` | 4664 |
| `#svccost` | 4708 |
