# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~7,099-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (274 indexed)

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
| `GRID_URLS` | 1474–1483 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `ensureGridData` | 1484–1555 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `state` | 1556–1587 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1588–1588 |  |
| `gridFetches` | 1589–1612 |  |
| `RAMPS` | 1613–1653 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1654–1660 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1661–1666 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1667–1667 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1668–1674 |  |
| `AMENITY_BANDS` | 1675–1676 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1677–1679 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1680–1685 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1686–1700 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1701–1706 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1707–1725 |  |
| `gridScale` | 1726–1746 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 1747–1753 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1754–1765 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1766–1768 |  |
| `quantile` | 1769–1783 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1784–1816 |  |
| `moneyBlurb` | 1817–1821 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1822–1834 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1835–1913 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 1914–1914 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 1915–1941 |  |
| `failLoading` | 1942–1955 |  |
| `hideLoading` | 1956–1981 |  |
| `topRings` | 1982–1998 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 1999–2024 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2025–2025 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2026–2038 |  |
| `svcT` | 2039–2043 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2044–2045 |  |
| `fmtFire` | 2046–2046 |  |
| `fmtTransit` | 2047–2048 |  |
| `fmtBike` | 2049–2049 |  |
| `fmtWater` | 2050–2052 |  |
| `fmtSvcCost` | 2053–2057 |  |
| `fmtRoadsCost` | 2058–2059 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtTransitCost` | 2060–2061 |  |
| `fmtBikeCost` | 2062–2073 |  |
| `servicePlaneLayer` | 2074–2106 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2107–2116 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2117–2122 |  |
| `DEV_IND_TOTAL` | 2123–2125 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2126–2131 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2132–2136 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2137–2142 |  |
| `devGridOfferable` | 2143–2144 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2145–2145 |  |
| `devCol` | 2146–2146 |  |
| `_devScale` | 2147–2147 |  |
| `devScale` | 2148–2154 |  |
| `devT` | 2155–2158 |  |
| `developmentPlaneLayer` | 2159–2175 |  |
| `fmtDev` | 2176–2191 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2192–2197 |  |
| `DEV_GRID_IND_N` | 2198–2198 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2199–2201 |  |
| `devGridScale` | 2202–2228 |  |
| `devGridLayer` | 2229–2277 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2278–2279 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2280–2287 |  |
| `_infillStats` | 2288–2288 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2289–2306 |  |
| `_infillRaw` | 2307–2309 |  |
| `infillScore` | 2310–2325 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2326–2327 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2328–2345 |  |
| `INFILL_CENTER` | 2346–2346 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2347–2347 |  |
| `INFILL_NEG` | 2348–2348 |  |
| `infillColorAt` | 2349–2353 |  |
| `infillPlaneLayer` | 2354–2368 |  |
| `fmtFar` | 2369–2378 |  |
| `AMENITY_HIGHLIGHT_COLOR` | 2379–2379 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2380–2434 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2435–2442 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2443–2457 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2458–2478 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2479–2479 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2480–2494 |  |
| `chgT` | 2495–2504 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2505–2535 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2536–2624 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2625–2632 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2633–2633 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2634–2641 |  |
| `deviationRate` | 2642–2684 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2685–2685 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 2686–2715 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 2716–2722 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 2723–2734 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 2735–2738 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 2739–2743 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 2744–2754 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 2755–2770 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 2771–2797 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `INST_OUTLINE_COLOR` | 2798–2850 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 2851–2855 |  |
| `bandHover` | 2856–2864 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 2865–2961 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 2962–2969 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 2970–2971 |  |
| `glassInstBandLayers` | 2972–3000 |  |
| `deviationRateExempt` | 3001–3013 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3014–3015 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3016–3017 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3018–3018 |  |
| `deviationStats` | 3019–3063 |  |
| `deviationOf` | 3064–3065 |  |
| `deviationT` | 3066–3076 |  |
| `fmtDeviation` | 3077–3098 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3099–3142 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3143–3229 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3230–3252 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3253–3253 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3254–3274 |  |
| `ensureFireStations` | 3275–3290 |  |
| `TRANSIT_STATION_COLOR` | 3291–3291 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3292–3309 |  |
| `ensureTransitStations` | 3310–3325 |  |
| `TRANSIT_LINE_COLOR` | 3326–3326 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3327–3343 |  |
| `ensureLrtLines` | 3344–3360 |  |
| `BIKE_LINE_COLOR` | 3361–3361 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3362–3378 |  |
| `ensureBikeLines` | 3379–3436 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3437–3437 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3438–3441 |  |
| `BOUNDARY_COLOR` | 3442–3451 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3452–3452 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3453–3465 |  |
| `referenceSplit` | 3466–3493 |  |
| `referenceUnderLayers` | 3494–3528 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3529–3545 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3546–3565 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3566–3578 |  |
| `servicesBlurb` | 3579–3596 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3597–3620 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 3621–3631 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 3632–3683 |  |
| `REF_TIERS` | 3684–3705 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 3706–3713 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 3714–3716 |  |
| `placeAnchors` | 3717–3740 |  |
| `labelPool` | 3741–3748 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 3749–3802 |  |
| `CHROME_IDS` | 3803–3806 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 3807–3825 |  |
| `visibleLabels` | 3826–3880 |  |
| `labelLayer` | 3881–3917 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 3918–3918 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 3919–3934 |  |
| `ratioT` | 3935–3945 |  |
| `buildLayers` | 3946–3958 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 3959–4261 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4262–4291 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4292–4295 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4296–4298 |  |
| `fmtBig` | 4299–4326 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4327–4332 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4333–4340 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4341–4345 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4346–4356 |  |
| `revenueLens` | 4357–4358 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4359–4376 |  |
| `SVC_COST_BASES` | 4377–4389 | The Services panel: this hood's revenue per acre set against what the City |
| `serviceLens` | 4390–4390 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4391–4393 |  |
| `servicePanelFor` | 4394–4407 |  |
| `hoodPanelLens` | 4408–4411 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4412–4429 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4430–4461 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 4462–4467 |  |
| `sparklineSvg` | 4468–4483 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 4484–4553 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 4554–4580 |  |
| `openTemporal` | 4581–4609 |  |
| `renderRevenueMix` | 4610–4658 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 4659–4692 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 4693–4695 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 4696–4746 |  |
| `syncPinnedPanel` | 4747–4773 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 4774–4789 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 4790–4800 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 4801–4848 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 4849–4854 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 4855–4894 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 4895–4911 |  |
| `temporalClick` | 4912–4969 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 4970–5049 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 5050–5382 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 5383–5450 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 5451–5451 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 5452–5470 |  |
| `syncMetricButtons` | 5471–5494 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 5495–5501 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 5502–5515 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 5516–5557 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 5558–5600 |  |
| `toggleBudgetPanel` | 5601–5626 |  |
| `syncMillRates` | 5627–5657 | Paint the pod, gate it to the money view's revenue cuts, and place it. |
| `applyMetric` | 5658–5679 |  |
| `applyColorAdjust` | 5680–5701 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 5702–5714 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 5715–5730 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 5731–5748 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 5749–5765 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 5766–5781 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 5782–5798 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 5799–6038 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 6039–6049 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 6050–6063 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 6064–6072 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 6073–6083 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 6084–6095 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 6096–6109 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 6110–6130 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 6131–6178 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 6179–6184 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 6185–6206 |  |
| `applyMoneyDetail` | 6207–6231 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 6232–6243 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 6244–6251 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 6252–6270 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 6271–6281 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 6282–6289 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 6290–6306 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 6307–6320 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 6321–6331 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 6332–6575 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 6576–6585 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 6586–6599 |  |
| `applySvcDriver` | 6600–7099 |  |

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
| `#revmix` | 4629 |
| `#svccost` | 4673 |
