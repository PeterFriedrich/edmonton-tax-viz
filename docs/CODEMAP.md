# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~6,927-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (266 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 556–560 |  |
| `HOME` | 561–561 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 562–605 |  |
| `fmtMoney` | 606–607 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `METRICS` | 608–733 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 734–750 |  |
| `RATIO_DENOMS` | 751–812 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 813–813 |  |
| `ratioOf` | 814–814 |  |
| `ratioKept` | 815–836 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 837–847 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 848–875 |  |
| `dominantUse` | 876–909 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 910–1064 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1065–1169 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1170–1174 | the Lab: a container for unfinished lenses |
| `inLab` | 1175–1176 |  |
| `DEVIATION_TITLES` | 1177–1181 |  |
| `deviationTitle` | 1182–1187 |  |
| `deviationKind` | 1188–1190 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1191–1196 |  |
| `changeBlurb` | 1197–1219 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1220–1241 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassInstBlurb` | 1242–1252 | The azure cells need a sentence for the same reason the Lab's outlined |
| `amenityWhichPhrase` | 1253–1258 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1259–1264 |  |
| `infillAmenityBlurb` | 1265–1278 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1279–1293 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1294–1299 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1300–1307 |  |
| `devChoroplethBlurb` | 1308–1309 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1310–1358 |  |
| `withColourClause` | 1359–1373 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `ensureGridData` | 1374–1434 |  |
| `state` | 1435–1488 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `RAMPS` | 1489–1529 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1530–1536 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1537–1542 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1543–1543 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1544–1550 |  |
| `AMENITY_BANDS` | 1551–1552 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1553–1555 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1556–1561 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1562–1576 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1577–1582 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1583–1594 |  |
| `gridScale` | 1595–1615 |  |
| `scaleT` | 1616–1622 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1623–1634 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1635–1637 |  |
| `quantile` | 1638–1652 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1653–1685 |  |
| `moneyBlurb` | 1686–1690 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1691–1703 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1704–1782 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 1783–1783 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 1784–1810 |  |
| `failLoading` | 1811–1824 |  |
| `hideLoading` | 1825–1850 |  |
| `topRings` | 1851–1867 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 1868–1893 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 1894–1894 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 1895–1907 |  |
| `svcT` | 1908–1912 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 1913–1914 |  |
| `fmtFire` | 1915–1915 |  |
| `fmtTransit` | 1916–1917 |  |
| `fmtBike` | 1918–1918 |  |
| `fmtWater` | 1919–1921 |  |
| `fmtSvcCost` | 1922–1926 |  |
| `fmtRoadsCost` | 1927–1928 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtTransitCost` | 1929–1930 |  |
| `fmtBikeCost` | 1931–1942 |  |
| `servicePlaneLayer` | 1943–1975 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 1976–1985 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 1986–1991 |  |
| `DEV_IND_TOTAL` | 1992–1994 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 1995–2000 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2001–2005 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2006–2011 |  |
| `devGridOfferable` | 2012–2013 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2014–2014 |  |
| `devCol` | 2015–2015 |  |
| `_devScale` | 2016–2016 |  |
| `devScale` | 2017–2023 |  |
| `devT` | 2024–2027 |  |
| `developmentPlaneLayer` | 2028–2044 |  |
| `fmtDev` | 2045–2060 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2061–2066 |  |
| `DEV_GRID_IND_N` | 2067–2067 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2068–2070 |  |
| `devGridScale` | 2071–2097 |  |
| `devGridLayer` | 2098–2146 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2147–2148 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2149–2156 |  |
| `_infillStats` | 2157–2157 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2158–2175 |  |
| `_infillRaw` | 2176–2178 |  |
| `infillScore` | 2179–2194 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2195–2196 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2197–2214 |  |
| `INFILL_CENTER` | 2215–2215 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2216–2216 |  |
| `INFILL_NEG` | 2217–2217 |  |
| `infillColorAt` | 2218–2222 |  |
| `infillPlaneLayer` | 2223–2237 |  |
| `fmtFar` | 2238–2247 |  |
| `AMENITY_HIGHLIGHT_COLOR` | 2248–2248 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2249–2303 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2304–2309 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2310–2324 | Hardcoded, and deliberately NOT derived from temporal.json's last year: the |
| `changeFor` | 2325–2345 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2346–2346 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2347–2361 |  |
| `chgT` | 2362–2371 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2372–2402 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2403–2491 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2492–2499 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2500–2500 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2501–2508 |  |
| `deviationRate` | 2509–2551 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2552–2552 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 2553–2582 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 2583–2589 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 2590–2601 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 2602–2605 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 2606–2610 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 2611–2621 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 2622–2637 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 2638–2664 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `INST_OUTLINE_COLOR` | 2665–2717 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 2718–2722 |  |
| `bandHover` | 2723–2731 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 2732–2828 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 2829–2836 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 2837–2838 |  |
| `glassInstBandLayers` | 2839–2867 |  |
| `deviationRateExempt` | 2868–2880 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 2881–2882 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 2883–2884 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 2885–2885 |  |
| `deviationStats` | 2886–2930 |  |
| `deviationOf` | 2931–2932 |  |
| `deviationT` | 2933–2943 |  |
| `fmtDeviation` | 2944–2965 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 2966–3009 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3010–3096 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3097–3119 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3120–3120 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3121–3141 |  |
| `ensureFireStations` | 3142–3157 |  |
| `TRANSIT_STATION_COLOR` | 3158–3158 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3159–3176 |  |
| `ensureTransitStations` | 3177–3192 |  |
| `TRANSIT_LINE_COLOR` | 3193–3193 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3194–3210 |  |
| `ensureLrtLines` | 3211–3227 |  |
| `BIKE_LINE_COLOR` | 3228–3228 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3229–3245 |  |
| `ensureBikeLines` | 3246–3303 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3304–3304 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3305–3308 |  |
| `BOUNDARY_COLOR` | 3309–3318 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3319–3319 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3320–3332 |  |
| `referenceSplit` | 3333–3360 |  |
| `referenceUnderLayers` | 3361–3395 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3396–3412 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3413–3432 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3433–3445 |  |
| `servicesBlurb` | 3446–3463 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3464–3487 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 3488–3498 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 3499–3550 |  |
| `REF_TIERS` | 3551–3572 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 3573–3580 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 3581–3583 |  |
| `placeAnchors` | 3584–3607 |  |
| `labelPool` | 3608–3615 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 3616–3669 |  |
| `CHROME_IDS` | 3670–3673 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 3674–3692 |  |
| `visibleLabels` | 3693–3747 |  |
| `labelLayer` | 3748–3784 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 3785–3785 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 3786–3801 |  |
| `ratioT` | 3802–3812 |  |
| `buildLayers` | 3813–3825 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 3826–4128 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4129–4158 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4159–4162 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4163–4165 |  |
| `fmtBig` | 4166–4193 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4194–4199 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4200–4207 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4208–4212 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4213–4223 |  |
| `revenueLens` | 4224–4225 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4226–4243 |  |
| `SVC_COST_BASES` | 4244–4256 | The Services panel: this hood's revenue per acre set against what the City |
| `serviceLens` | 4257–4257 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4258–4260 |  |
| `servicePanelFor` | 4261–4274 |  |
| `hoodPanelLens` | 4275–4278 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4279–4296 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4297–4328 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 4329–4334 |  |
| `sparklineSvg` | 4335–4350 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 4351–4420 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 4421–4447 |  |
| `openTemporal` | 4448–4476 |  |
| `renderRevenueMix` | 4477–4525 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 4526–4559 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 4560–4562 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 4563–4613 |  |
| `syncPinnedPanel` | 4614–4640 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 4641–4656 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 4657–4667 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 4668–4715 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 4716–4721 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 4722–4761 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 4762–4778 |  |
| `temporalClick` | 4779–4836 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 4837–4916 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 4917–5249 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 5250–5317 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 5318–5318 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 5319–5337 |  |
| `syncMetricButtons` | 5338–5361 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 5362–5368 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 5369–5382 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 5383–5424 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 5425–5467 |  |
| `toggleBudgetPanel` | 5468–5493 |  |
| `syncMillRates` | 5494–5524 | Paint the pod, gate it to the money view's revenue cuts, and place it. |
| `applyMetric` | 5525–5546 |  |
| `applyColorAdjust` | 5547–5568 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 5569–5581 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 5582–5597 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 5598–5615 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 5616–5632 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 5633–5648 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 5649–5665 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 5666–5905 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 5906–5916 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 5917–5930 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 5931–5939 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 5940–5950 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 5951–5962 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 5963–5976 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 5977–5997 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 5998–6045 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 6046–6051 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 6052–6069 |  |
| `applyMoneyDetail` | 6070–6079 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `applyMoneyMode` | 6080–6087 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 6088–6106 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 6107–6117 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 6118–6125 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 6126–6142 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 6143–6156 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 6157–6167 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 6168–6403 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 6404–6413 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 6414–6427 |  |
| `applySvcDriver` | 6428–6927 |  |

## Element ids (119) — the control surface

| id | line |
|---|---|
| `#map` | 18 |
| `#loading` | 22 |
| `#loading-box` | 23 |
| `#loading-spinner` | 24 |
| `#loading-text` | 25 |
| `#loading-retry` | 26 |
| `#banner` | 30 |
| `#title` | 32 |
| `#title-h` | 33 |
| `#title-p` | 34 |
| `#temporal` | 45 |
| `#temporal-close` | 46 |
| `#temporal-name` | 47 |
| `#temporal-body` | 54 |
| `#temporal-chart` | 55 |
| `#temporal-read` | 56 |
| `#temporal-note` | 57 |
| `#temporal-hint` | 61 |
| `#millrates` | 77 |
| `#mill-head` | 78 |
| `#mill-rows` | 79 |
| `#mill-note` | 80 |
| `#budget` | 94 |
| `#budget-close` | 101 |
| `#budget-head` | 102 |
| `#budget-body` | 107 |
| `#budget-rows` | 108 |
| `#budget-other-hd` | 109 |
| `#budget-other` | 110 |
| `#budget-note` | 111 |
| `#peek` | 126 |
| `#peek-name` | 127 |
| `#peek-read` | 128 |
| `#peek-go` | 129 |
| `#controls` | 132 |
| `#toggle` | 145 |
| `#metric-row` | 146 |
| `#revcut` | 150 |
| `#moneymode` | 155 |
| `#views` | 161 |
| `#optpanel` | 175 |
| `#opt-fold` | 176 |
| `#opt-caret` | 176 |
| `#opt-body` | 177 |
| `#layers` | 178 |
| `#chgwindow-hd` | 179 |
| `#chgwindow` | 180 |
| `#labpick-hd` | 189 |
| `#labpick` | 190 |
| `#labcut-hd` | 191 |
| `#labcut` | 192 |
| `#moneydetail-hd` | 197 |
| `#moneydetail` | 198 |
| `#amenity-hd` | 212 |
| `#amenity` | 213 |
| `#amenity-lrt-row` | 214 |
| `#amenity-lrt-on` | 215 |
| `#amenity-school-row` | 217 |
| `#amenity-school-on` | 218 |
| `#uses-prisms-hd` | 221 |
| `#uses-prisms` | 222 |
| `#uses-prisms-on` | 224 |
| `#devmode-hd` | 227 |
| `#devmode` | 228 |
| `#devmetric-hd` | 232 |
| `#devmetric` | 233 |
| `#devwindow-hd` | 238 |
| `#devwindow` | 239 |
| `#devdetail-hd` | 244 |
| `#devdetail` | 245 |
| `#prism-hd` | 249 |
| `#prism-row` | 250 |
| `#prism-opacity` | 252 |
| `#prism-opacity-val` | 253 |
| `#services-hd` | 255 |
| `#services` | 256 |
| `#denom-hd` | 350 |
| `#denom` | 351 |
| `#ratio-denom-hd` | 355 |
| `#ratio-denom` | 356 |
| `#hoodmode` | 367 |
| `#hoodmode-btn` | 368 |
| `#coloradj` | 380 |
| `#coloradj-btn` | 381 |
| `#budget-pod` | 388 |
| `#budget-btn` | 389 |
| `#a11y` | 393 |
| `#a11y-btn` | 394 |
| `#a11y-menu` | 395 |
| `#palette` | 397 |
| `#labels-on` | 404 |
| `#reference-on` | 412 |
| `#about` | 417 |
| `#about-btn` | 418 |
| `#about-menu` | 419 |
| `#about-src-services` | 428 |
| `#about-vintage` | 456 |
| `#about-modelled` | 463 |
| `#about-budget` | 473 |
| `#about-budget-lead` | 475 |
| `#about-budget-rows` | 476 |
| `#about-budget-note` | 477 |
| `#about-updated` | 488 |
| `#botleft` | 492 |
| `#compass` | 493 |
| `#rot-ccw` | 494 |
| `#tonorth` | 501 |
| `#needle` | 503 |
| `#rot-cw` | 508 |
| `#viewbtns` | 516 |
| `#center2d` | 517 |
| `#recenter` | 518 |
| `#legend` | 520 |
| `#legend-label` | 521 |
| `#legend-min` | 523 |
| `#legend-max` | 523 |
| `#legend-cats` | 525 |
| `#revmix` | 4496 |
| `#svccost` | 4540 |
