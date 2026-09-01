# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~7,082-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (274 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 579–583 |  |
| `HOME` | 584–584 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 585–598 |  |
| `WINDOWS` | 599–617 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 618–627 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 628–632 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 633–683 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `fmtMoney` | 684–685 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `METRICS` | 686–811 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 812–828 |  |
| `RATIO_DENOMS` | 829–890 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 891–891 |  |
| `ratioOf` | 892–892 |  |
| `ratioKept` | 893–914 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 915–925 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 926–953 |  |
| `dominantUse` | 954–987 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 988–1142 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1143–1247 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1248–1252 | the Lab: a container for unfinished lenses |
| `inLab` | 1253–1254 |  |
| `DEVIATION_TITLES` | 1255–1259 |  |
| `deviationTitle` | 1260–1265 |  |
| `deviationKind` | 1266–1268 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1269–1274 |  |
| `changeBlurb` | 1275–1299 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1300–1321 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassInstBlurb` | 1322–1332 | The azure cells need a sentence for the same reason the Lab's outlined |
| `amenityWhichPhrase` | 1333–1338 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1339–1344 |  |
| `infillAmenityBlurb` | 1345–1358 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1359–1373 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1374–1379 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1380–1387 |  |
| `devChoroplethBlurb` | 1388–1389 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1390–1438 |  |
| `withColourClause` | 1439–1456 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1457–1466 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `ensureGridData` | 1467–1538 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `state` | 1539–1570 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1571–1571 |  |
| `gridFetches` | 1572–1595 |  |
| `RAMPS` | 1596–1636 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1637–1643 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1644–1649 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1650–1650 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1651–1657 |  |
| `AMENITY_BANDS` | 1658–1659 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1660–1662 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1663–1668 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1669–1683 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1684–1689 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1690–1708 |  |
| `gridScale` | 1709–1729 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 1730–1736 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1737–1748 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1749–1751 |  |
| `quantile` | 1752–1766 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1767–1799 |  |
| `moneyBlurb` | 1800–1804 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1805–1817 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1818–1896 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 1897–1897 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 1898–1924 |  |
| `failLoading` | 1925–1938 |  |
| `hideLoading` | 1939–1964 |  |
| `topRings` | 1965–1981 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 1982–2007 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2008–2008 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2009–2021 |  |
| `svcT` | 2022–2026 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2027–2028 |  |
| `fmtFire` | 2029–2029 |  |
| `fmtTransit` | 2030–2031 |  |
| `fmtBike` | 2032–2032 |  |
| `fmtWater` | 2033–2035 |  |
| `fmtSvcCost` | 2036–2040 |  |
| `fmtRoadsCost` | 2041–2042 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtTransitCost` | 2043–2044 |  |
| `fmtBikeCost` | 2045–2056 |  |
| `servicePlaneLayer` | 2057–2089 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2090–2099 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2100–2105 |  |
| `DEV_IND_TOTAL` | 2106–2108 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2109–2114 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2115–2119 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2120–2125 |  |
| `devGridOfferable` | 2126–2127 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2128–2128 |  |
| `devCol` | 2129–2129 |  |
| `_devScale` | 2130–2130 |  |
| `devScale` | 2131–2137 |  |
| `devT` | 2138–2141 |  |
| `developmentPlaneLayer` | 2142–2158 |  |
| `fmtDev` | 2159–2174 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2175–2180 |  |
| `DEV_GRID_IND_N` | 2181–2181 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2182–2184 |  |
| `devGridScale` | 2185–2211 |  |
| `devGridLayer` | 2212–2260 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2261–2262 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2263–2270 |  |
| `_infillStats` | 2271–2271 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2272–2289 |  |
| `_infillRaw` | 2290–2292 |  |
| `infillScore` | 2293–2308 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2309–2310 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2311–2328 |  |
| `INFILL_CENTER` | 2329–2329 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2330–2330 |  |
| `INFILL_NEG` | 2331–2331 |  |
| `infillColorAt` | 2332–2336 |  |
| `infillPlaneLayer` | 2337–2351 |  |
| `fmtFar` | 2352–2361 |  |
| `AMENITY_HIGHLIGHT_COLOR` | 2362–2362 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2363–2417 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2418–2425 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2426–2440 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2441–2461 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2462–2462 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2463–2477 |  |
| `chgT` | 2478–2487 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2488–2518 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2519–2607 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2608–2615 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2616–2616 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2617–2624 |  |
| `deviationRate` | 2625–2667 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2668–2668 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 2669–2698 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 2699–2705 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 2706–2717 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 2718–2721 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 2722–2726 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 2727–2737 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 2738–2753 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 2754–2780 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `INST_OUTLINE_COLOR` | 2781–2833 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 2834–2838 |  |
| `bandHover` | 2839–2847 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 2848–2944 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 2945–2952 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 2953–2954 |  |
| `glassInstBandLayers` | 2955–2983 |  |
| `deviationRateExempt` | 2984–2996 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 2997–2998 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 2999–3000 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3001–3001 |  |
| `deviationStats` | 3002–3046 |  |
| `deviationOf` | 3047–3048 |  |
| `deviationT` | 3049–3059 |  |
| `fmtDeviation` | 3060–3081 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3082–3125 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3126–3212 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3213–3235 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3236–3236 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3237–3257 |  |
| `ensureFireStations` | 3258–3273 |  |
| `TRANSIT_STATION_COLOR` | 3274–3274 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3275–3292 |  |
| `ensureTransitStations` | 3293–3308 |  |
| `TRANSIT_LINE_COLOR` | 3309–3309 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3310–3326 |  |
| `ensureLrtLines` | 3327–3343 |  |
| `BIKE_LINE_COLOR` | 3344–3344 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3345–3361 |  |
| `ensureBikeLines` | 3362–3419 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3420–3420 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3421–3424 |  |
| `BOUNDARY_COLOR` | 3425–3434 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3435–3435 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3436–3448 |  |
| `referenceSplit` | 3449–3476 |  |
| `referenceUnderLayers` | 3477–3511 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3512–3528 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3529–3548 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3549–3561 |  |
| `servicesBlurb` | 3562–3579 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3580–3603 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 3604–3614 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 3615–3666 |  |
| `REF_TIERS` | 3667–3688 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 3689–3696 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 3697–3699 |  |
| `placeAnchors` | 3700–3723 |  |
| `labelPool` | 3724–3731 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 3732–3785 |  |
| `CHROME_IDS` | 3786–3789 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 3790–3808 |  |
| `visibleLabels` | 3809–3863 |  |
| `labelLayer` | 3864–3900 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 3901–3901 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 3902–3917 |  |
| `ratioT` | 3918–3928 |  |
| `buildLayers` | 3929–3941 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 3942–4244 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4245–4274 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4275–4278 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4279–4281 |  |
| `fmtBig` | 4282–4309 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4310–4315 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4316–4323 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4324–4328 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4329–4339 |  |
| `revenueLens` | 4340–4341 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4342–4359 |  |
| `SVC_COST_BASES` | 4360–4372 | The Services panel: this hood's revenue per acre set against what the City |
| `serviceLens` | 4373–4373 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4374–4376 |  |
| `servicePanelFor` | 4377–4390 |  |
| `hoodPanelLens` | 4391–4394 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4395–4412 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4413–4444 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 4445–4450 |  |
| `sparklineSvg` | 4451–4466 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 4467–4536 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 4537–4563 |  |
| `openTemporal` | 4564–4592 |  |
| `renderRevenueMix` | 4593–4641 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 4642–4675 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 4676–4678 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 4679–4729 |  |
| `syncPinnedPanel` | 4730–4756 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 4757–4772 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 4773–4783 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 4784–4831 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 4832–4837 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 4838–4877 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 4878–4894 |  |
| `temporalClick` | 4895–4952 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 4953–5032 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 5033–5365 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 5366–5433 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 5434–5434 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 5435–5453 |  |
| `syncMetricButtons` | 5454–5477 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 5478–5484 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 5485–5498 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 5499–5540 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 5541–5583 |  |
| `toggleBudgetPanel` | 5584–5609 |  |
| `syncMillRates` | 5610–5640 | Paint the pod, gate it to the money view's revenue cuts, and place it. |
| `applyMetric` | 5641–5662 |  |
| `applyColorAdjust` | 5663–5684 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 5685–5697 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 5698–5713 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 5714–5731 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 5732–5748 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 5749–5764 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 5765–5781 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 5782–6021 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 6022–6032 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 6033–6046 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 6047–6055 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 6056–6066 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 6067–6078 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 6079–6092 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 6093–6113 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 6114–6161 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 6162–6167 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 6168–6189 |  |
| `applyMoneyDetail` | 6190–6214 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 6215–6226 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 6227–6234 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 6235–6253 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 6254–6264 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 6265–6272 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 6273–6289 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 6290–6303 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 6304–6314 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 6315–6558 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 6559–6568 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 6569–6582 |  |
| `applySvcDriver` | 6583–7082 |  |

## Element ids (121) — the control surface

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
| `#about-modelled` | 486 |
| `#about-budget` | 496 |
| `#about-budget-lead` | 498 |
| `#about-budget-rows` | 499 |
| `#about-budget-note` | 500 |
| `#about-updated` | 511 |
| `#botleft` | 515 |
| `#compass` | 516 |
| `#rot-ccw` | 517 |
| `#tonorth` | 524 |
| `#needle` | 526 |
| `#rot-cw` | 531 |
| `#viewbtns` | 539 |
| `#center2d` | 540 |
| `#recenter` | 541 |
| `#legend` | 543 |
| `#legend-label` | 544 |
| `#legend-min` | 546 |
| `#legend-max` | 546 |
| `#legend-cats` | 548 |
| `#revmix` | 4612 |
| `#svccost` | 4656 |
