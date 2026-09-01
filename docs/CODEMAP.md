# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~7,202-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (277 indexed)

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
| `gridDetailButton` | 1481–1499 | The Detail button that selects a resolution, for the busy state in |
| `loadGridData` | 1500–1553 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1554–1601 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1602–1626 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1627–1658 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1659–1659 |  |
| `gridFetches` | 1660–1683 |  |
| `RAMPS` | 1684–1724 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1725–1731 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1732–1737 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1738–1738 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1739–1745 |  |
| `AMENITY_BANDS` | 1746–1747 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1748–1750 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1751–1756 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1757–1771 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1772–1777 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1778–1796 |  |
| `gridScale` | 1797–1817 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 1818–1824 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1825–1836 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1837–1839 |  |
| `quantile` | 1840–1854 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1855–1887 |  |
| `moneyBlurb` | 1888–1892 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1893–1905 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1906–1984 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 1985–1985 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 1986–2012 |  |
| `failLoading` | 2013–2026 |  |
| `hideLoading` | 2027–2066 |  |
| `topRings` | 2067–2083 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2084–2109 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2110–2110 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2111–2123 |  |
| `svcT` | 2124–2128 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2129–2130 |  |
| `fmtFire` | 2131–2131 |  |
| `fmtTransit` | 2132–2133 |  |
| `fmtBike` | 2134–2134 |  |
| `fmtWater` | 2135–2137 |  |
| `fmtSvcCost` | 2138–2142 |  |
| `fmtRoadsCost` | 2143–2144 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtTransitCost` | 2145–2146 |  |
| `fmtBikeCost` | 2147–2158 |  |
| `servicePlaneLayer` | 2159–2191 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2192–2201 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2202–2207 |  |
| `DEV_IND_TOTAL` | 2208–2210 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2211–2216 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2217–2221 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2222–2227 |  |
| `devGridOfferable` | 2228–2229 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2230–2230 |  |
| `devCol` | 2231–2231 |  |
| `_devScale` | 2232–2232 |  |
| `devScale` | 2233–2239 |  |
| `devT` | 2240–2243 |  |
| `developmentPlaneLayer` | 2244–2260 |  |
| `fmtDev` | 2261–2276 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2277–2282 |  |
| `DEV_GRID_IND_N` | 2283–2283 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2284–2286 |  |
| `devGridScale` | 2287–2313 |  |
| `devGridLayer` | 2314–2362 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2363–2364 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2365–2372 |  |
| `_infillStats` | 2373–2373 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2374–2391 |  |
| `_infillRaw` | 2392–2394 |  |
| `infillScore` | 2395–2410 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2411–2412 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2413–2430 |  |
| `INFILL_CENTER` | 2431–2431 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2432–2432 |  |
| `INFILL_NEG` | 2433–2433 |  |
| `infillColorAt` | 2434–2438 |  |
| `infillPlaneLayer` | 2439–2453 |  |
| `fmtFar` | 2454–2463 |  |
| `AMENITY_HIGHLIGHT_COLOR` | 2464–2464 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2465–2519 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2520–2527 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2528–2542 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2543–2563 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2564–2564 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2565–2579 |  |
| `chgT` | 2580–2589 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2590–2620 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2621–2709 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2710–2717 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2718–2718 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2719–2726 |  |
| `deviationRate` | 2727–2769 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2770–2770 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 2771–2800 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 2801–2807 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 2808–2819 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 2820–2823 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 2824–2828 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 2829–2839 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 2840–2855 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 2856–2882 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `INST_OUTLINE_COLOR` | 2883–2935 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 2936–2940 |  |
| `bandHover` | 2941–2949 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 2950–3046 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3047–3054 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3055–3056 |  |
| `glassInstBandLayers` | 3057–3085 |  |
| `deviationRateExempt` | 3086–3098 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3099–3100 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3101–3102 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3103–3103 |  |
| `deviationStats` | 3104–3148 |  |
| `deviationOf` | 3149–3150 |  |
| `deviationT` | 3151–3161 |  |
| `fmtDeviation` | 3162–3183 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3184–3227 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3228–3314 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3315–3337 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3338–3338 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3339–3359 |  |
| `ensureFireStations` | 3360–3375 |  |
| `TRANSIT_STATION_COLOR` | 3376–3376 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3377–3394 |  |
| `ensureTransitStations` | 3395–3410 |  |
| `TRANSIT_LINE_COLOR` | 3411–3411 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3412–3428 |  |
| `ensureLrtLines` | 3429–3445 |  |
| `BIKE_LINE_COLOR` | 3446–3446 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3447–3463 |  |
| `ensureBikeLines` | 3464–3521 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3522–3522 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3523–3526 |  |
| `BOUNDARY_COLOR` | 3527–3536 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3537–3537 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3538–3550 |  |
| `referenceSplit` | 3551–3578 |  |
| `referenceUnderLayers` | 3579–3613 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3614–3630 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3631–3650 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3651–3663 |  |
| `servicesBlurb` | 3664–3681 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3682–3705 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 3706–3716 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 3717–3768 |  |
| `REF_TIERS` | 3769–3790 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 3791–3798 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 3799–3801 |  |
| `placeAnchors` | 3802–3825 |  |
| `labelPool` | 3826–3833 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 3834–3887 |  |
| `CHROME_IDS` | 3888–3891 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 3892–3910 |  |
| `visibleLabels` | 3911–3965 |  |
| `labelLayer` | 3966–4002 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 4003–4003 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4004–4019 |  |
| `ratioT` | 4020–4030 |  |
| `buildLayers` | 4031–4043 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 4044–4346 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4347–4376 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4377–4380 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4381–4383 |  |
| `fmtBig` | 4384–4411 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4412–4417 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4418–4425 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4426–4430 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4431–4441 |  |
| `revenueLens` | 4442–4443 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4444–4461 |  |
| `SVC_COST_BASES` | 4462–4474 | The Services panel: this hood's revenue per acre set against what the City |
| `serviceLens` | 4475–4475 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4476–4478 |  |
| `servicePanelFor` | 4479–4492 |  |
| `hoodPanelLens` | 4493–4496 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4497–4514 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4515–4546 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 4547–4552 |  |
| `sparklineSvg` | 4553–4568 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 4569–4638 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 4639–4665 |  |
| `openTemporal` | 4666–4694 |  |
| `renderRevenueMix` | 4695–4743 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 4744–4777 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 4778–4780 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 4781–4831 |  |
| `syncPinnedPanel` | 4832–4858 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 4859–4874 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 4875–4885 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 4886–4933 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 4934–4939 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 4940–4979 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 4980–4996 |  |
| `temporalClick` | 4997–5054 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 5055–5134 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 5135–5467 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 5468–5535 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 5536–5536 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 5537–5555 |  |
| `syncMetricButtons` | 5556–5579 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 5580–5586 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 5587–5600 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 5601–5642 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 5643–5685 |  |
| `toggleBudgetPanel` | 5686–5711 |  |
| `syncMillRates` | 5712–5742 | Paint the pod, gate it to the money view's revenue cuts, and place it. |
| `applyMetric` | 5743–5764 |  |
| `applyColorAdjust` | 5765–5786 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 5787–5799 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 5800–5815 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 5816–5833 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 5834–5850 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 5851–5866 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 5867–5883 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 5884–6123 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 6124–6134 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 6135–6148 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 6149–6157 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 6158–6168 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 6169–6180 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 6181–6194 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 6195–6215 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 6216–6263 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 6264–6269 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 6270–6291 |  |
| `applyMoneyDetail` | 6292–6316 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 6317–6328 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 6329–6336 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 6337–6355 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 6356–6366 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 6367–6374 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 6375–6391 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 6392–6405 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 6406–6416 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 6417–6660 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 6661–6670 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 6671–6684 |  |
| `applySvcDriver` | 6685–7202 |  |

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
| `#revmix` | 4714 |
| `#svccost` | 4758 |
