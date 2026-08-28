# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~6,939-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (266 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 568–572 |  |
| `HOME` | 573–573 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 574–617 |  |
| `fmtMoney` | 618–619 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `METRICS` | 620–745 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 746–762 |  |
| `RATIO_DENOMS` | 763–824 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 825–825 |  |
| `ratioOf` | 826–826 |  |
| `ratioKept` | 827–848 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 849–859 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 860–887 |  |
| `dominantUse` | 888–921 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 922–1076 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1077–1181 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1182–1186 | the Lab: a container for unfinished lenses |
| `inLab` | 1187–1188 |  |
| `DEVIATION_TITLES` | 1189–1193 |  |
| `deviationTitle` | 1194–1199 |  |
| `deviationKind` | 1200–1202 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1203–1208 |  |
| `changeBlurb` | 1209–1231 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1232–1253 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassInstBlurb` | 1254–1264 | The azure cells need a sentence for the same reason the Lab's outlined |
| `amenityWhichPhrase` | 1265–1270 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1271–1276 |  |
| `infillAmenityBlurb` | 1277–1290 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1291–1305 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1306–1311 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1312–1319 |  |
| `devChoroplethBlurb` | 1320–1321 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1322–1370 |  |
| `withColourClause` | 1371–1385 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `ensureGridData` | 1386–1446 |  |
| `state` | 1447–1500 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `RAMPS` | 1501–1541 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1542–1548 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1549–1554 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1555–1555 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1556–1562 |  |
| `AMENITY_BANDS` | 1563–1564 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1565–1567 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1568–1573 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1574–1588 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1589–1594 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1595–1606 |  |
| `gridScale` | 1607–1627 |  |
| `scaleT` | 1628–1634 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1635–1646 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1647–1649 |  |
| `quantile` | 1650–1664 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1665–1697 |  |
| `moneyBlurb` | 1698–1702 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1703–1715 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1716–1794 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 1795–1795 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 1796–1822 |  |
| `failLoading` | 1823–1836 |  |
| `hideLoading` | 1837–1862 |  |
| `topRings` | 1863–1879 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 1880–1905 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 1906–1906 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 1907–1919 |  |
| `svcT` | 1920–1924 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 1925–1926 |  |
| `fmtFire` | 1927–1927 |  |
| `fmtTransit` | 1928–1929 |  |
| `fmtBike` | 1930–1930 |  |
| `fmtWater` | 1931–1933 |  |
| `fmtSvcCost` | 1934–1938 |  |
| `fmtRoadsCost` | 1939–1940 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtTransitCost` | 1941–1942 |  |
| `fmtBikeCost` | 1943–1954 |  |
| `servicePlaneLayer` | 1955–1987 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 1988–1997 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 1998–2003 |  |
| `DEV_IND_TOTAL` | 2004–2006 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2007–2012 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2013–2017 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2018–2023 |  |
| `devGridOfferable` | 2024–2025 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2026–2026 |  |
| `devCol` | 2027–2027 |  |
| `_devScale` | 2028–2028 |  |
| `devScale` | 2029–2035 |  |
| `devT` | 2036–2039 |  |
| `developmentPlaneLayer` | 2040–2056 |  |
| `fmtDev` | 2057–2072 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2073–2078 |  |
| `DEV_GRID_IND_N` | 2079–2079 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2080–2082 |  |
| `devGridScale` | 2083–2109 |  |
| `devGridLayer` | 2110–2158 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2159–2160 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2161–2168 |  |
| `_infillStats` | 2169–2169 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2170–2187 |  |
| `_infillRaw` | 2188–2190 |  |
| `infillScore` | 2191–2206 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2207–2208 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2209–2226 |  |
| `INFILL_CENTER` | 2227–2227 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2228–2228 |  |
| `INFILL_NEG` | 2229–2229 |  |
| `infillColorAt` | 2230–2234 |  |
| `infillPlaneLayer` | 2235–2249 |  |
| `fmtFar` | 2250–2259 |  |
| `AMENITY_HIGHLIGHT_COLOR` | 2260–2260 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2261–2315 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2316–2321 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2322–2336 | Hardcoded, and deliberately NOT derived from temporal.json's last year: the |
| `changeFor` | 2337–2357 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2358–2358 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2359–2373 |  |
| `chgT` | 2374–2383 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2384–2414 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2415–2503 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2504–2511 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2512–2512 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2513–2520 |  |
| `deviationRate` | 2521–2563 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2564–2564 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 2565–2594 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 2595–2601 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 2602–2613 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 2614–2617 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 2618–2622 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 2623–2633 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 2634–2649 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 2650–2676 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `INST_OUTLINE_COLOR` | 2677–2729 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 2730–2734 |  |
| `bandHover` | 2735–2743 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 2744–2840 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 2841–2848 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 2849–2850 |  |
| `glassInstBandLayers` | 2851–2879 |  |
| `deviationRateExempt` | 2880–2892 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 2893–2894 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 2895–2896 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 2897–2897 |  |
| `deviationStats` | 2898–2942 |  |
| `deviationOf` | 2943–2944 |  |
| `deviationT` | 2945–2955 |  |
| `fmtDeviation` | 2956–2977 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 2978–3021 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3022–3108 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3109–3131 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3132–3132 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3133–3153 |  |
| `ensureFireStations` | 3154–3169 |  |
| `TRANSIT_STATION_COLOR` | 3170–3170 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3171–3188 |  |
| `ensureTransitStations` | 3189–3204 |  |
| `TRANSIT_LINE_COLOR` | 3205–3205 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3206–3222 |  |
| `ensureLrtLines` | 3223–3239 |  |
| `BIKE_LINE_COLOR` | 3240–3240 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3241–3257 |  |
| `ensureBikeLines` | 3258–3315 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3316–3316 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3317–3320 |  |
| `BOUNDARY_COLOR` | 3321–3330 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3331–3331 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3332–3344 |  |
| `referenceSplit` | 3345–3372 |  |
| `referenceUnderLayers` | 3373–3407 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3408–3424 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3425–3444 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3445–3457 |  |
| `servicesBlurb` | 3458–3475 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3476–3499 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 3500–3510 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 3511–3562 |  |
| `REF_TIERS` | 3563–3584 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 3585–3592 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 3593–3595 |  |
| `placeAnchors` | 3596–3619 |  |
| `labelPool` | 3620–3627 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 3628–3681 |  |
| `CHROME_IDS` | 3682–3685 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 3686–3704 |  |
| `visibleLabels` | 3705–3759 |  |
| `labelLayer` | 3760–3796 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 3797–3797 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 3798–3813 |  |
| `ratioT` | 3814–3824 |  |
| `buildLayers` | 3825–3837 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 3838–4140 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4141–4170 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4171–4174 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4175–4177 |  |
| `fmtBig` | 4178–4205 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4206–4211 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4212–4219 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4220–4224 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4225–4235 |  |
| `revenueLens` | 4236–4237 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4238–4255 |  |
| `SVC_COST_BASES` | 4256–4268 | The Services panel: this hood's revenue per acre set against what the City |
| `serviceLens` | 4269–4269 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4270–4272 |  |
| `servicePanelFor` | 4273–4286 |  |
| `hoodPanelLens` | 4287–4290 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4291–4308 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4309–4340 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 4341–4346 |  |
| `sparklineSvg` | 4347–4362 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 4363–4432 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 4433–4459 |  |
| `openTemporal` | 4460–4488 |  |
| `renderRevenueMix` | 4489–4537 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 4538–4571 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 4572–4574 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 4575–4625 |  |
| `syncPinnedPanel` | 4626–4652 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 4653–4668 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 4669–4679 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 4680–4727 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 4728–4733 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 4734–4773 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 4774–4790 |  |
| `temporalClick` | 4791–4848 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 4849–4928 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 4929–5261 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 5262–5329 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 5330–5330 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 5331–5349 |  |
| `syncMetricButtons` | 5350–5373 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 5374–5380 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 5381–5394 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 5395–5436 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 5437–5479 |  |
| `toggleBudgetPanel` | 5480–5505 |  |
| `syncMillRates` | 5506–5536 | Paint the pod, gate it to the money view's revenue cuts, and place it. |
| `applyMetric` | 5537–5558 |  |
| `applyColorAdjust` | 5559–5580 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 5581–5593 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 5594–5609 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 5610–5627 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 5628–5644 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 5645–5660 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 5661–5677 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 5678–5917 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 5918–5928 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 5929–5942 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 5943–5951 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 5952–5962 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 5963–5974 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 5975–5988 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 5989–6009 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 6010–6057 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 6058–6063 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 6064–6081 |  |
| `applyMoneyDetail` | 6082–6091 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `applyMoneyMode` | 6092–6099 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 6100–6118 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 6119–6129 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 6130–6137 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 6138–6154 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 6155–6168 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 6169–6179 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 6180–6415 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 6416–6425 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 6426–6439 |  |
| `applySvcDriver` | 6440–6939 |  |

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
| `#amenity-hd` | 224 |
| `#amenity` | 225 |
| `#amenity-lrt-row` | 226 |
| `#amenity-lrt-on` | 227 |
| `#amenity-school-row` | 229 |
| `#amenity-school-on` | 230 |
| `#uses-prisms-hd` | 233 |
| `#uses-prisms` | 234 |
| `#uses-prisms-on` | 236 |
| `#devmode-hd` | 239 |
| `#devmode` | 240 |
| `#devmetric-hd` | 244 |
| `#devmetric` | 245 |
| `#devwindow-hd` | 250 |
| `#devwindow` | 251 |
| `#devdetail-hd` | 256 |
| `#devdetail` | 257 |
| `#prism-hd` | 261 |
| `#prism-row` | 262 |
| `#prism-opacity` | 264 |
| `#prism-opacity-val` | 265 |
| `#services-hd` | 267 |
| `#services` | 268 |
| `#denom-hd` | 362 |
| `#denom` | 363 |
| `#ratio-denom-hd` | 367 |
| `#ratio-denom` | 368 |
| `#hoodmode` | 379 |
| `#hoodmode-btn` | 380 |
| `#coloradj` | 392 |
| `#coloradj-btn` | 393 |
| `#budget-pod` | 400 |
| `#budget-btn` | 401 |
| `#a11y` | 405 |
| `#a11y-btn` | 406 |
| `#a11y-menu` | 407 |
| `#palette` | 409 |
| `#labels-on` | 416 |
| `#reference-on` | 424 |
| `#about` | 429 |
| `#about-btn` | 430 |
| `#about-menu` | 431 |
| `#about-src-services` | 440 |
| `#about-vintage` | 468 |
| `#about-modelled` | 475 |
| `#about-budget` | 485 |
| `#about-budget-lead` | 487 |
| `#about-budget-rows` | 488 |
| `#about-budget-note` | 489 |
| `#about-updated` | 500 |
| `#botleft` | 504 |
| `#compass` | 505 |
| `#rot-ccw` | 506 |
| `#tonorth` | 513 |
| `#needle` | 515 |
| `#rot-cw` | 520 |
| `#viewbtns` | 528 |
| `#center2d` | 529 |
| `#recenter` | 530 |
| `#legend` | 532 |
| `#legend-label` | 533 |
| `#legend-min` | 535 |
| `#legend-max` | 535 |
| `#legend-cats` | 537 |
| `#revmix` | 4508 |
| `#svccost` | 4552 |
