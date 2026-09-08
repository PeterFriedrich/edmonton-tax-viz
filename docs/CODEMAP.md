# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~7,427-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (283 indexed)

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
| `glassInstBlurb` | 1394–1404 | The azure cells need a sentence for the same reason the Lab's outlined |
| `amenityWhichPhrase` | 1405–1410 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1411–1416 |  |
| `infillAmenityBlurb` | 1417–1430 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1431–1445 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1446–1451 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1452–1459 |  |
| `devChoroplethBlurb` | 1460–1461 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1462–1510 |  |
| `withColourClause` | 1511–1528 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1529–1535 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1536–1549 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1550–1550 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1551–1565 |  |
| `fmtMB` | 1566–1576 |  |
| `showGridBusy` | 1577–1599 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1600–1616 |  |
| `loadGridData` | 1617–1670 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1671–1724 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1725–1749 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1750–1781 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1782–1782 |  |
| `gridFetches` | 1783–1806 |  |
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
| `moneyScale` | 1978–2010 |  |
| `moneyBlurb` | 2011–2015 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 2016–2028 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2029–2107 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2108–2108 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2109–2135 |  |
| `failLoading` | 2136–2149 |  |
| `hideLoading` | 2150–2204 |  |
| `topRings` | 2205–2221 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2222–2247 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2248–2248 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2249–2261 |  |
| `svcT` | 2262–2266 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2267–2268 |  |
| `fmtFire` | 2269–2269 |  |
| `fmtTransit` | 2270–2271 |  |
| `fmtBike` | 2272–2272 |  |
| `fmtWater` | 2273–2278 |  |
| `fmtRoadsCost` | 2279–2283 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2284–2285 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2286–2287 |  |
| `fmtBikeCost` | 2288–2299 |  |
| `servicePlaneLayer` | 2300–2332 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2333–2342 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2343–2348 |  |
| `DEV_IND_TOTAL` | 2349–2351 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2352–2357 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2358–2362 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2363–2368 |  |
| `devGridOfferable` | 2369–2370 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2371–2371 |  |
| `devCol` | 2372–2372 |  |
| `_devScale` | 2373–2373 |  |
| `devScale` | 2374–2380 |  |
| `devT` | 2381–2384 |  |
| `developmentPlaneLayer` | 2385–2401 |  |
| `fmtDev` | 2402–2417 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2418–2423 |  |
| `DEV_GRID_IND_N` | 2424–2424 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2425–2427 |  |
| `devGridScale` | 2428–2454 |  |
| `devGridLayer` | 2455–2503 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2504–2505 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2506–2513 |  |
| `_infillStats` | 2514–2514 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2515–2532 |  |
| `_infillRaw` | 2533–2535 |  |
| `infillScore` | 2536–2551 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2552–2553 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2554–2571 |  |
| `INFILL_CENTER` | 2572–2572 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2573–2573 |  |
| `INFILL_NEG` | 2574–2574 |  |
| `infillColorAt` | 2575–2579 |  |
| `infillPlaneLayer` | 2580–2594 |  |
| `fmtFar` | 2595–2604 |  |
| `AMENITY_HIGHLIGHT_COLOR` | 2605–2605 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2606–2660 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2661–2668 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2669–2683 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2684–2704 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2705–2705 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2706–2720 |  |
| `chgT` | 2721–2730 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2731–2761 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2762–2850 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2851–2858 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2859–2859 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2860–2867 |  |
| `deviationRate` | 2868–2910 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2911–2911 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 2912–2941 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 2942–2948 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 2949–2960 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 2961–2964 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 2965–2969 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 2970–2980 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 2981–2996 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 2997–3023 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `INST_OUTLINE_COLOR` | 3024–3076 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 3077–3081 |  |
| `bandHover` | 3082–3090 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3091–3187 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3188–3195 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3196–3197 |  |
| `glassInstBandLayers` | 3198–3226 |  |
| `deviationRateExempt` | 3227–3239 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3240–3241 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3242–3243 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3244–3244 |  |
| `deviationStats` | 3245–3289 |  |
| `deviationOf` | 3290–3291 |  |
| `deviationT` | 3292–3302 |  |
| `fmtDeviation` | 3303–3324 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3325–3368 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3369–3455 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3456–3478 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3479–3479 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3480–3500 |  |
| `ensureFireStations` | 3501–3516 |  |
| `TRANSIT_STATION_COLOR` | 3517–3517 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3518–3535 |  |
| `ensureTransitStations` | 3536–3551 |  |
| `TRANSIT_LINE_COLOR` | 3552–3552 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3553–3569 |  |
| `ensureLrtLines` | 3570–3586 |  |
| `BIKE_LINE_COLOR` | 3587–3587 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3588–3604 |  |
| `ensureBikeLines` | 3605–3662 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3663–3663 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3664–3667 |  |
| `BOUNDARY_COLOR` | 3668–3677 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3678–3678 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3679–3691 |  |
| `referenceSplit` | 3692–3719 |  |
| `referenceUnderLayers` | 3720–3754 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3755–3771 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3772–3791 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3792–3804 |  |
| `servicesBlurb` | 3805–3822 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3823–3846 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 3847–3857 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 3858–3909 |  |
| `REF_TIERS` | 3910–3931 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 3932–3939 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 3940–3942 |  |
| `placeAnchors` | 3943–3966 |  |
| `labelPool` | 3967–3974 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 3975–4028 |  |
| `CHROME_IDS` | 4029–4033 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4034–4052 |  |
| `visibleLabels` | 4053–4107 |  |
| `labelLayer` | 4108–4144 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 4145–4145 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4146–4161 |  |
| `ratioT` | 4162–4172 |  |
| `buildLayers` | 4173–4185 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 4186–4488 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4489–4518 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4519–4522 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4523–4525 |  |
| `fmtBig` | 4526–4553 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4554–4559 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4560–4567 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4568–4572 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4573–4583 |  |
| `revenueLens` | 4584–4585 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4586–4617 |  |
| `SVC_COST_BASES` | 4618–4630 | The Services panel: this hood's revenue per acre set against what the City |
| `serviceLens` | 4631–4631 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4632–4635 |  |
| `servicePanelFor` | 4636–4656 |  |
| `hoodPanelLens` | 4657–4660 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4661–4678 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4679–4710 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 4711–4716 |  |
| `sparklineSvg` | 4717–4732 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 4733–4802 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 4803–4829 |  |
| `openTemporal` | 4830–4858 |  |
| `renderRevenueMix` | 4859–4925 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 4926–4971 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 4972–4974 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 4975–5025 |  |
| `syncPinnedPanel` | 5026–5052 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5053–5068 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5069–5079 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5080–5127 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5128–5133 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5134–5173 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5174–5190 |  |
| `temporalClick` | 5191–5248 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 5249–5328 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 5329–5664 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 5665–5732 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 5733–5733 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 5734–5752 |  |
| `syncMetricButtons` | 5753–5776 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 5777–5783 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 5784–5797 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 5798–5839 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 5840–5882 |  |
| `toggleBudgetPanel` | 5883–5908 |  |
| `syncMillRates` | 5909–5941 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 5942–5963 |  |
| `applyColorAdjust` | 5964–5985 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 5986–5998 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 5999–6014 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 6015–6032 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 6033–6049 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 6050–6065 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 6066–6082 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 6083–6322 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 6323–6333 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 6334–6347 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 6348–6356 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 6357–6367 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 6368–6379 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 6380–6393 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 6394–6414 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 6415–6462 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 6463–6468 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 6469–6490 |  |
| `applyMoneyDetail` | 6491–6515 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 6516–6527 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 6528–6535 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 6536–6554 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 6555–6565 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 6566–6573 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 6574–6590 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 6591–6604 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 6605–6615 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 6616–6861 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 6862–6871 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 6872–6885 |  |
| `applySvcDriver` | 6886–6899 |  |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 6900–7427 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (869 edges)

⚠️ **A regex reference count, not a call graph** — a name in a comment or string counts, and a nested symbol is attributed to its enclosing range. Use it for *what is central* and *would this seam hold*, never as ground truth for a final module boundary.

**Most depended-on** — moving one of these touches everything below it.

| symbol | referenced by | section |
|---|---|---|
| `state` | 112 | the Lab: a container for unfinished lenses |
| `buildLayers` | 35 | geographic reference layers (all views) |
| `METRICS` | 16 | tunables |
| `refreshLegend` | 14 | control appliers + the view/legend dispatchers |
| `SERVICES` | 13 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `applyView` | 13 | control appliers + the view/legend dispatchers |
| `CELLS` | 10 | tunables |
| `quantile` | 10 | the Lab: a container for unfinished lenses |
| `deviationStats` | 9 | the same doubt, at 100 m |
| `ratioDenom` | 8 | services lens views (SPEC_services.md display architecture) |
| `ratioScale` | 8 | geographic reference layers (all views) |
| `devIndustrial` | 8 | loading overlay |
| `devCol` | 8 | loading overlay |
| `labelPool` | 8 | geographic reference layers (all views) |
| `esc` | 8 | money view (default): the classic metric prisms |

**Section self-containment** — share of each section's outgoing edges that stay inside it. Low means a module cut on this banner would mostly import its neighbours.

| section | edges | self-contained |
|---|---|---|
| services lens views (SPEC_services.md display architecture) | 1 | 100% |
| uses view (use-mix, 2026-07-03) | 3 | 67% |
| deviation lens: revenue per developed acre against peer average | 3 | 67% |
| the Lab: a container for unfinished lenses | 107 | 65% |
| Infill lens (SPEC_development.md Lens B) | 26 | 65% |
| tunables | 10 | 60% |
| Development 100 m detail grid (layers-panel toggle, 2026-07-15) | 9 | 44% |
| change lens: how each hood's share of the assessment base moved | 16 | 44% |
| geographic reference layers (all views) | 86 | 42% |
| loading overlay | 49 | 39% |
| Money's revenue panel: where a hood's levy comes from | 186 | 38% |
| two tiers, answering two different questions | 27 | 33% |
| the same doubt, at 100 m | 53 | 30% |
| control appliers + the view/legend dispatchers | 206 | 21% |
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
| `#revmix` | 4878 |
| `#svccost` | 4944 |
