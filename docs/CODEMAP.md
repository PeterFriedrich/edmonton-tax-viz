# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~7,554-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (286 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 640–644 |  |
| `HOME` | 645–645 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 646–659 |  |
| `WINDOWS` | 660–678 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 679–688 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 689–693 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 694–761 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `fmtMoney` | 762–763 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `METRICS` | 764–889 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 890–906 |  |
| `RATIO_DENOMS` | 907–939 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 940–940 |  |
| `ratioOf` | 941–941 |  |
| `ratioKept` | 942–963 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 964–974 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 975–1002 |  |
| `dominantUse` | 1003–1044 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1045–1214 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1215–1319 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1320–1324 | the Lab: a container for unfinished lenses |
| `inLab` | 1325–1326 |  |
| `DEVIATION_TITLES` | 1327–1331 |  |
| `deviationTitle` | 1332–1337 |  |
| `deviationKind` | 1338–1340 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1341–1346 |  |
| `changeBlurb` | 1347–1371 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1372–1393 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassInstBlurb` | 1394–1406 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1407–1418 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `amenityWhichPhrase` | 1419–1424 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1425–1430 |  |
| `infillAmenityBlurb` | 1431–1444 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1445–1459 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1460–1465 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1466–1473 |  |
| `devChoroplethBlurb` | 1474–1475 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1476–1524 |  |
| `withColourClause` | 1525–1542 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1543–1549 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1550–1563 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1564–1564 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1565–1579 |  |
| `fmtMB` | 1580–1590 |  |
| `showGridBusy` | 1591–1613 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1614–1630 |  |
| `loadGridData` | 1631–1684 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1685–1738 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1739–1763 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1764–1795 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1796–1796 |  |
| `gridFetches` | 1797–1820 |  |
| `RAMPS` | 1821–1861 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1862–1868 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1869–1874 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1875–1875 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1876–1882 |  |
| `AMENITY_BANDS` | 1883–1884 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1885–1887 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1888–1893 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1894–1908 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1909–1914 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1915–1933 |  |
| `gridScale` | 1934–1954 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 1955–1961 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1962–1973 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1974–1976 |  |
| `quantile` | 1977–1991 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1992–2024 |  |
| `moneyBlurb` | 2025–2029 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 2030–2042 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2043–2121 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2122–2122 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2123–2149 |  |
| `failLoading` | 2150–2163 |  |
| `hideLoading` | 2164–2218 |  |
| `topRings` | 2219–2235 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2236–2261 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2262–2262 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2263–2275 |  |
| `svcT` | 2276–2280 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2281–2282 |  |
| `fmtFire` | 2283–2283 |  |
| `fmtTransit` | 2284–2285 |  |
| `fmtBike` | 2286–2286 |  |
| `fmtWater` | 2287–2292 |  |
| `fmtRoadsCost` | 2293–2297 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2298–2299 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2300–2301 |  |
| `fmtBikeCost` | 2302–2313 |  |
| `servicePlaneLayer` | 2314–2346 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2347–2356 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2357–2362 |  |
| `DEV_IND_TOTAL` | 2363–2365 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2366–2371 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2372–2376 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2377–2382 |  |
| `devGridOfferable` | 2383–2384 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2385–2385 |  |
| `devCol` | 2386–2386 |  |
| `_devScale` | 2387–2387 |  |
| `devScale` | 2388–2394 |  |
| `devT` | 2395–2398 |  |
| `developmentPlaneLayer` | 2399–2415 |  |
| `fmtDev` | 2416–2431 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2432–2437 |  |
| `DEV_GRID_IND_N` | 2438–2438 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2439–2441 |  |
| `devGridScale` | 2442–2468 |  |
| `devGridLayer` | 2469–2517 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2518–2519 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2520–2527 |  |
| `_infillStats` | 2528–2528 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2529–2546 |  |
| `_infillRaw` | 2547–2549 |  |
| `infillScore` | 2550–2565 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2566–2567 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2568–2585 |  |
| `INFILL_CENTER` | 2586–2586 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2587–2587 |  |
| `INFILL_NEG` | 2588–2588 |  |
| `infillColorAt` | 2589–2593 |  |
| `infillPlaneLayer` | 2594–2608 |  |
| `fmtFar` | 2609–2618 |  |
| `AMENITY_HIGHLIGHT_COLOR` | 2619–2619 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2620–2674 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2675–2682 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2683–2697 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2698–2718 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2719–2719 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2720–2734 |  |
| `chgT` | 2735–2744 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2745–2775 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2776–2864 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2865–2872 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2873–2873 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2874–2881 |  |
| `deviationRate` | 2882–2924 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2925–2925 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 2926–2955 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 2956–2962 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 2963–2974 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 2975–2978 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 2979–2983 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 2984–2994 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 2995–3010 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3011–3042 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3043–3067 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `INST_OUTLINE_COLOR` | 3068–3120 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 3121–3125 |  |
| `bandHover` | 3126–3134 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3135–3231 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3232–3239 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3240–3241 |  |
| `glassInstBandLayers` | 3242–3282 |  |
| `ratioInstBandLayers` | 3283–3310 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3311–3323 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3324–3325 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3326–3327 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3328–3328 |  |
| `deviationStats` | 3329–3373 |  |
| `deviationOf` | 3374–3375 |  |
| `deviationT` | 3376–3386 |  |
| `fmtDeviation` | 3387–3408 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3409–3452 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3453–3539 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3540–3562 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3563–3563 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3564–3584 |  |
| `ensureFireStations` | 3585–3600 |  |
| `TRANSIT_STATION_COLOR` | 3601–3601 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3602–3619 |  |
| `ensureTransitStations` | 3620–3635 |  |
| `TRANSIT_LINE_COLOR` | 3636–3636 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3637–3653 |  |
| `ensureLrtLines` | 3654–3670 |  |
| `BIKE_LINE_COLOR` | 3671–3671 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3672–3688 |  |
| `ensureBikeLines` | 3689–3746 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3747–3747 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3748–3751 |  |
| `BOUNDARY_COLOR` | 3752–3761 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3762–3762 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3763–3775 |  |
| `referenceSplit` | 3776–3803 |  |
| `referenceUnderLayers` | 3804–3838 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3839–3855 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3856–3875 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3876–3888 |  |
| `servicesBlurb` | 3889–3906 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3907–3930 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 3931–3941 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 3942–3993 |  |
| `REF_TIERS` | 3994–4015 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4016–4023 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 4024–4026 |  |
| `placeAnchors` | 4027–4050 |  |
| `labelPool` | 4051–4058 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4059–4112 |  |
| `CHROME_IDS` | 4113–4117 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4118–4136 |  |
| `visibleLabels` | 4137–4191 |  |
| `labelLayer` | 4192–4228 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 4229–4229 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4230–4245 |  |
| `ratioT` | 4246–4256 |  |
| `buildLayers` | 4257–4269 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 4270–4579 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4580–4609 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4610–4613 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4614–4616 |  |
| `fmtBig` | 4617–4644 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4645–4650 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4651–4658 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4659–4663 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4664–4674 |  |
| `revenueLens` | 4675–4676 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4677–4708 |  |
| `SVC_COST_BASES` | 4709–4721 | The Services panel: this hood's revenue per acre set against what the City |
| `serviceLens` | 4722–4722 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4723–4726 |  |
| `servicePanelFor` | 4727–4747 |  |
| `hoodPanelLens` | 4748–4751 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4752–4769 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4770–4801 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 4802–4807 |  |
| `sparklineSvg` | 4808–4823 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 4824–4893 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 4894–4920 |  |
| `openTemporal` | 4921–4949 |  |
| `renderRevenueMix` | 4950–5016 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 5017–5062 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 5063–5065 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5066–5116 |  |
| `syncPinnedPanel` | 5117–5143 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5144–5159 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5160–5170 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5171–5218 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5219–5224 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5225–5264 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5265–5281 |  |
| `temporalClick` | 5282–5339 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 5340–5419 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 5420–5779 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 5780–5847 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 5848–5848 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 5849–5867 |  |
| `syncMetricButtons` | 5868–5891 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 5892–5898 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 5899–5912 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 5913–5954 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 5955–5997 |  |
| `toggleBudgetPanel` | 5998–6023 |  |
| `syncMillRates` | 6024–6056 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 6057–6078 |  |
| `applyColorAdjust` | 6079–6100 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 6101–6113 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 6114–6129 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 6130–6147 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 6148–6164 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 6165–6180 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 6181–6197 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 6198–6437 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 6438–6448 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 6449–6462 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 6463–6471 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 6472–6482 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 6483–6494 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 6495–6508 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 6509–6529 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 6530–6577 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 6578–6583 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 6584–6605 |  |
| `applyMoneyDetail` | 6606–6630 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 6631–6642 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 6643–6650 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 6651–6669 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 6670–6680 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 6681–6688 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 6689–6705 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 6706–6719 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 6720–6730 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 6731–6982 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 6983–6992 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 6993–7006 |  |
| `applySvcDriver` | 7007–7020 |  |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 7021–7554 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (885 edges)

⚠️ **A regex reference count, not a call graph** — a name in a comment or string counts, and a nested symbol is attributed to its enclosing range. Use it for *what is central* and *would this seam hold*, never as ground truth for a final module boundary.

**Most depended-on** — moving one of these touches everything below it.

| symbol | referenced by | section |
|---|---|---|
| `state` | 114 | the Lab: a container for unfinished lenses |
| `buildLayers` | 35 | geographic reference layers (all views) |
| `METRICS` | 16 | tunables |
| `refreshLegend` | 14 | control appliers + the view/legend dispatchers |
| `SERVICES` | 13 | services view (SPEC_services.md UI generalization, 2026-07-05) |
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
| Money's revenue panel: where a hood's levy comes from | 187 | 38% |
| two tiers, answering two different questions | 29 | 31% |
| the same doubt, at 100 m | 61 | 26% |
| control appliers + the view/legend dispatchers | 208 | 21% |
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
| `#revmix` | 4969 |
| `#svccost` | 5035 |
