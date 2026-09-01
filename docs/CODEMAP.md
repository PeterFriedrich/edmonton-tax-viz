# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~6,993-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (269 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 573–577 |  |
| `HOME` | 578–578 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 579–592 |  |
| `WINDOWS` | 593–608 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 609–618 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `TOKENS` | 619–669 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `fmtMoney` | 670–671 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `METRICS` | 672–797 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 798–814 |  |
| `RATIO_DENOMS` | 815–876 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 877–877 |  |
| `ratioOf` | 878–878 |  |
| `ratioKept` | 879–900 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 901–911 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 912–939 |  |
| `dominantUse` | 940–973 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 974–1128 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1129–1233 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1234–1238 | the Lab: a container for unfinished lenses |
| `inLab` | 1239–1240 |  |
| `DEVIATION_TITLES` | 1241–1245 |  |
| `deviationTitle` | 1246–1251 |  |
| `deviationKind` | 1252–1254 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1255–1260 |  |
| `changeBlurb` | 1261–1283 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1284–1305 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassInstBlurb` | 1306–1316 | The azure cells need a sentence for the same reason the Lab's outlined |
| `amenityWhichPhrase` | 1317–1322 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1323–1328 |  |
| `infillAmenityBlurb` | 1329–1342 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1343–1357 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1358–1363 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1364–1371 |  |
| `devChoroplethBlurb` | 1372–1373 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1374–1422 |  |
| `withColourClause` | 1423–1437 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `ensureGridData` | 1438–1498 |  |
| `state` | 1499–1552 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `RAMPS` | 1553–1593 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1594–1600 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1601–1606 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1607–1607 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1608–1614 |  |
| `AMENITY_BANDS` | 1615–1616 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1617–1619 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1620–1625 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1626–1640 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1641–1646 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1647–1658 |  |
| `gridScale` | 1659–1679 |  |
| `scaleT` | 1680–1686 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1687–1698 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1699–1701 |  |
| `quantile` | 1702–1716 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1717–1749 |  |
| `moneyBlurb` | 1750–1754 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1755–1767 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1768–1846 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 1847–1847 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 1848–1874 |  |
| `failLoading` | 1875–1888 |  |
| `hideLoading` | 1889–1914 |  |
| `topRings` | 1915–1931 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 1932–1957 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 1958–1958 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 1959–1971 |  |
| `svcT` | 1972–1976 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 1977–1978 |  |
| `fmtFire` | 1979–1979 |  |
| `fmtTransit` | 1980–1981 |  |
| `fmtBike` | 1982–1982 |  |
| `fmtWater` | 1983–1985 |  |
| `fmtSvcCost` | 1986–1990 |  |
| `fmtRoadsCost` | 1991–1992 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtTransitCost` | 1993–1994 |  |
| `fmtBikeCost` | 1995–2006 |  |
| `servicePlaneLayer` | 2007–2039 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2040–2049 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2050–2055 |  |
| `DEV_IND_TOTAL` | 2056–2058 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2059–2064 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2065–2069 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2070–2075 |  |
| `devGridOfferable` | 2076–2077 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2078–2078 |  |
| `devCol` | 2079–2079 |  |
| `_devScale` | 2080–2080 |  |
| `devScale` | 2081–2087 |  |
| `devT` | 2088–2091 |  |
| `developmentPlaneLayer` | 2092–2108 |  |
| `fmtDev` | 2109–2124 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2125–2130 |  |
| `DEV_GRID_IND_N` | 2131–2131 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2132–2134 |  |
| `devGridScale` | 2135–2161 |  |
| `devGridLayer` | 2162–2210 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2211–2212 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2213–2220 |  |
| `_infillStats` | 2221–2221 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2222–2239 |  |
| `_infillRaw` | 2240–2242 |  |
| `infillScore` | 2243–2258 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2259–2260 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2261–2278 |  |
| `INFILL_CENTER` | 2279–2279 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2280–2280 |  |
| `INFILL_NEG` | 2281–2281 |  |
| `infillColorAt` | 2282–2286 |  |
| `infillPlaneLayer` | 2287–2301 |  |
| `fmtFar` | 2302–2311 |  |
| `AMENITY_HIGHLIGHT_COLOR` | 2312–2312 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2313–2367 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2368–2375 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2376–2390 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2391–2411 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2412–2412 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2413–2427 |  |
| `chgT` | 2428–2437 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2438–2468 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2469–2557 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2558–2565 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2566–2566 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2567–2574 |  |
| `deviationRate` | 2575–2617 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2618–2618 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 2619–2648 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 2649–2655 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 2656–2667 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 2668–2671 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 2672–2676 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 2677–2687 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 2688–2703 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 2704–2730 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `INST_OUTLINE_COLOR` | 2731–2783 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 2784–2788 |  |
| `bandHover` | 2789–2797 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 2798–2894 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 2895–2902 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 2903–2904 |  |
| `glassInstBandLayers` | 2905–2933 |  |
| `deviationRateExempt` | 2934–2946 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 2947–2948 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 2949–2950 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 2951–2951 |  |
| `deviationStats` | 2952–2996 |  |
| `deviationOf` | 2997–2998 |  |
| `deviationT` | 2999–3009 |  |
| `fmtDeviation` | 3010–3031 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3032–3075 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3076–3162 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3163–3185 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3186–3186 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3187–3207 |  |
| `ensureFireStations` | 3208–3223 |  |
| `TRANSIT_STATION_COLOR` | 3224–3224 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3225–3242 |  |
| `ensureTransitStations` | 3243–3258 |  |
| `TRANSIT_LINE_COLOR` | 3259–3259 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3260–3276 |  |
| `ensureLrtLines` | 3277–3293 |  |
| `BIKE_LINE_COLOR` | 3294–3294 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3295–3311 |  |
| `ensureBikeLines` | 3312–3369 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3370–3370 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3371–3374 |  |
| `BOUNDARY_COLOR` | 3375–3384 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3385–3385 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3386–3398 |  |
| `referenceSplit` | 3399–3426 |  |
| `referenceUnderLayers` | 3427–3461 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3462–3478 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3479–3498 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3499–3511 |  |
| `servicesBlurb` | 3512–3529 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3530–3553 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 3554–3564 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 3565–3616 |  |
| `REF_TIERS` | 3617–3638 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 3639–3646 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 3647–3649 |  |
| `placeAnchors` | 3650–3673 |  |
| `labelPool` | 3674–3681 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 3682–3735 |  |
| `CHROME_IDS` | 3736–3739 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 3740–3758 |  |
| `visibleLabels` | 3759–3813 |  |
| `labelLayer` | 3814–3850 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 3851–3851 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 3852–3867 |  |
| `ratioT` | 3868–3878 |  |
| `buildLayers` | 3879–3891 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 3892–4194 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4195–4224 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4225–4228 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4229–4231 |  |
| `fmtBig` | 4232–4259 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4260–4265 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4266–4273 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4274–4278 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4279–4289 |  |
| `revenueLens` | 4290–4291 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4292–4309 |  |
| `SVC_COST_BASES` | 4310–4322 | The Services panel: this hood's revenue per acre set against what the City |
| `serviceLens` | 4323–4323 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4324–4326 |  |
| `servicePanelFor` | 4327–4340 |  |
| `hoodPanelLens` | 4341–4344 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4345–4362 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4363–4394 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 4395–4400 |  |
| `sparklineSvg` | 4401–4416 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 4417–4486 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 4487–4513 |  |
| `openTemporal` | 4514–4542 |  |
| `renderRevenueMix` | 4543–4591 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 4592–4625 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 4626–4628 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 4629–4679 |  |
| `syncPinnedPanel` | 4680–4706 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 4707–4722 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 4723–4733 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 4734–4781 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 4782–4787 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 4788–4827 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 4828–4844 |  |
| `temporalClick` | 4845–4902 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 4903–4982 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 4983–5315 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 5316–5383 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 5384–5384 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 5385–5403 |  |
| `syncMetricButtons` | 5404–5427 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 5428–5434 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 5435–5448 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 5449–5490 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 5491–5533 |  |
| `toggleBudgetPanel` | 5534–5559 |  |
| `syncMillRates` | 5560–5590 | Paint the pod, gate it to the money view's revenue cuts, and place it. |
| `applyMetric` | 5591–5612 |  |
| `applyColorAdjust` | 5613–5634 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 5635–5647 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 5648–5663 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 5664–5681 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 5682–5698 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 5699–5714 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 5715–5731 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 5732–5971 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 5972–5982 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 5983–5996 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 5997–6005 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 6006–6016 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 6017–6028 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 6029–6042 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 6043–6063 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 6064–6111 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 6112–6117 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 6118–6135 |  |
| `applyMoneyDetail` | 6136–6145 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `applyMoneyMode` | 6146–6153 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 6154–6172 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 6173–6183 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 6184–6191 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 6192–6208 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 6209–6222 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 6223–6233 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 6234–6469 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 6470–6479 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 6480–6493 |  |
| `applySvcDriver` | 6494–6993 |  |

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
| `#amenity-hd` | 229 |
| `#amenity` | 230 |
| `#amenity-lrt-row` | 231 |
| `#amenity-lrt-on` | 232 |
| `#amenity-school-row` | 234 |
| `#amenity-school-on` | 235 |
| `#uses-prisms-hd` | 238 |
| `#uses-prisms` | 239 |
| `#uses-prisms-on` | 241 |
| `#devmode-hd` | 244 |
| `#devmode` | 245 |
| `#devmetric-hd` | 249 |
| `#devmetric` | 250 |
| `#devwindow-hd` | 255 |
| `#devwindow` | 256 |
| `#devdetail-hd` | 261 |
| `#devdetail` | 262 |
| `#prism-hd` | 266 |
| `#prism-row` | 267 |
| `#prism-opacity` | 269 |
| `#prism-opacity-val` | 270 |
| `#services-hd` | 272 |
| `#services` | 273 |
| `#denom-hd` | 367 |
| `#denom` | 368 |
| `#ratio-denom-hd` | 372 |
| `#ratio-denom` | 373 |
| `#hoodmode` | 384 |
| `#hoodmode-btn` | 385 |
| `#coloradj` | 397 |
| `#coloradj-btn` | 398 |
| `#budget-pod` | 405 |
| `#budget-btn` | 406 |
| `#a11y` | 410 |
| `#a11y-btn` | 411 |
| `#a11y-menu` | 412 |
| `#palette` | 414 |
| `#labels-on` | 421 |
| `#reference-on` | 429 |
| `#about` | 434 |
| `#about-btn` | 435 |
| `#about-menu` | 436 |
| `#about-src-services` | 445 |
| `#about-vintage` | 473 |
| `#about-modelled` | 480 |
| `#about-budget` | 490 |
| `#about-budget-lead` | 492 |
| `#about-budget-rows` | 493 |
| `#about-budget-note` | 494 |
| `#about-updated` | 505 |
| `#botleft` | 509 |
| `#compass` | 510 |
| `#rot-ccw` | 511 |
| `#tonorth` | 518 |
| `#needle` | 520 |
| `#rot-cw` | 525 |
| `#viewbtns` | 533 |
| `#center2d` | 534 |
| `#recenter` | 535 |
| `#legend` | 537 |
| `#legend-label` | 538 |
| `#legend-min` | 540 |
| `#legend-max` | 540 |
| `#legend-cats` | 542 |
| `#revmix` | 4562 |
| `#svccost` | 4606 |
