# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~6,771-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (263 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 545–549 |  |
| `HOME` | 550–550 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 551–594 |  |
| `fmtMoney` | 595–596 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `METRICS` | 597–722 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 723–739 |  |
| `RATIO_DENOMS` | 740–801 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 802–802 |  |
| `ratioOf` | 803–803 |  |
| `ratioKept` | 804–825 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 826–836 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 837–864 |  |
| `dominantUse` | 865–898 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 899–1053 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1054–1158 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1159–1163 | the Lab: a container for unfinished lenses |
| `inLab` | 1164–1165 |  |
| `DEVIATION_TITLES` | 1166–1170 |  |
| `deviationTitle` | 1171–1176 |  |
| `deviationKind` | 1177–1179 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1180–1185 |  |
| `changeBlurb` | 1186–1205 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1206–1227 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassInstBlurb` | 1228–1238 | The azure cells need a sentence for the same reason the Lab's outlined |
| `amenityWhichPhrase` | 1239–1248 | Phrase it as what KEEPS colour/highlight. The negative form does not |
| `amenityBlurb` | 1249–1259 | A greyed city needs to say why, and needs to say HOW MUCH survived |
| `glassBlurb` | 1260–1265 |  |
| `infillAmenityBlurb` | 1266–1279 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1280–1294 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1295–1300 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1301–1308 |  |
| `devChoroplethBlurb` | 1309–1310 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1311–1359 |  |
| `withColourClause` | 1360–1374 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `ensureGridData` | 1375–1435 |  |
| `state` | 1436–1489 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `RAMPS` | 1490–1530 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1531–1537 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1538–1543 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1544–1544 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1545–1551 |  |
| `AMENITY_BANDS` | 1552–1559 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1560–1562 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1563–1568 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1569–1583 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1584–1589 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1590–1601 |  |
| `gridScale` | 1602–1622 |  |
| `scaleT` | 1623–1629 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1630–1641 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1642–1644 |  |
| `quantile` | 1645–1659 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1660–1692 |  |
| `moneyBlurb` | 1693–1697 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1698–1710 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1711–1760 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### base map (no basemap tiles for v1 — just a dark backdrop)

| symbol | lines | what it does |
|---|---|---|
| `topRings` | 1761–1777 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 1778–1803 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 1804–1804 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 1805–1817 |  |
| `svcT` | 1818–1822 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 1823–1824 |  |
| `fmtFire` | 1825–1825 |  |
| `fmtTransit` | 1826–1827 |  |
| `fmtBike` | 1828–1828 |  |
| `fmtWater` | 1829–1831 |  |
| `fmtSvcCost` | 1832–1836 |  |
| `fmtRoadsCost` | 1837–1838 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtTransitCost` | 1839–1840 |  |
| `fmtBikeCost` | 1841–1852 |  |
| `servicePlaneLayer` | 1853–1885 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 1886–1895 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 1896–1901 |  |
| `DEV_IND_TOTAL` | 1902–1904 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 1905–1910 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 1911–1915 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 1916–1921 |  |
| `devGridOfferable` | 1922–1923 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 1924–1924 |  |
| `devCol` | 1925–1925 |  |
| `_devScale` | 1926–1926 |  |
| `devScale` | 1927–1933 |  |
| `devT` | 1934–1937 |  |
| `developmentPlaneLayer` | 1938–1954 |  |
| `fmtDev` | 1955–1970 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 1971–1976 |  |
| `DEV_GRID_IND_N` | 1977–1977 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 1978–1980 |  |
| `devGridScale` | 1981–2007 |  |
| `devGridLayer` | 2008–2056 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2057–2058 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2059–2066 |  |
| `_infillStats` | 2067–2067 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2068–2085 |  |
| `_infillRaw` | 2086–2088 |  |
| `infillScore` | 2089–2104 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2105–2106 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2107–2124 |  |
| `INFILL_CENTER` | 2125–2125 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2126–2126 |  |
| `INFILL_NEG` | 2127–2127 |  |
| `infillColorAt` | 2128–2132 |  |
| `infillPlaneLayer` | 2133–2147 |  |
| `fmtFar` | 2148–2157 |  |
| `AMENITY_HIGHLIGHT_COLOR` | 2158–2158 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2159–2213 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2214–2214 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2215–2229 |  |
| `changeFor` | 2230–2250 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2251–2251 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2252–2266 |  |
| `chgT` | 2267–2276 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2277–2290 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePlaneLayer` | 2291–2364 | Flat plane — EXTRUDED IS FALSE BY DECISION, not by omission. Hoods moved |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2365–2372 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2373–2373 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2374–2381 |  |
| `deviationRate` | 2382–2419 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2420–2420 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `instFrac` | 2421–2450 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 2451–2457 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 2458–2469 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 2470–2473 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 2474–2478 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 2479–2489 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 2490–2505 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 2506–2532 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `INST_OUTLINE_COLOR` | 2533–2585 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 2586–2590 |  |
| `bandHover` | 2591–2599 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 2600–2696 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 2697–2704 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 2705–2706 |  |
| `glassInstBandLayers` | 2707–2735 |  |
| `deviationRateExempt` | 2736–2748 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 2749–2750 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 2751–2752 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 2753–2753 |  |
| `deviationStats` | 2754–2798 |  |
| `deviationOf` | 2799–2800 |  |
| `deviationT` | 2801–2811 |  |
| `fmtDeviation` | 2812–2833 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 2834–2877 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 2878–2964 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 2965–2987 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 2988–2988 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 2989–3009 |  |
| `ensureFireStations` | 3010–3025 |  |
| `TRANSIT_STATION_COLOR` | 3026–3026 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3027–3044 |  |
| `ensureTransitStations` | 3045–3060 |  |
| `TRANSIT_LINE_COLOR` | 3061–3061 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3062–3078 |  |
| `ensureLrtLines` | 3079–3095 |  |
| `BIKE_LINE_COLOR` | 3096–3096 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3097–3113 |  |
| `ensureBikeLines` | 3114–3171 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3172–3172 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3173–3176 |  |
| `BOUNDARY_COLOR` | 3177–3186 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3187–3187 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3188–3200 |  |
| `referenceSplit` | 3201–3228 |  |
| `referenceUnderLayers` | 3229–3263 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3264–3280 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3281–3300 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3301–3313 |  |
| `servicesBlurb` | 3314–3331 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3332–3355 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 3356–3366 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 3367–3418 |  |
| `REF_TIERS` | 3419–3440 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 3441–3448 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 3449–3451 |  |
| `placeAnchors` | 3452–3475 |  |
| `labelPool` | 3476–3483 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 3484–3537 |  |
| `CHROME_IDS` | 3538–3541 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 3542–3560 |  |
| `visibleLabels` | 3561–3615 |  |
| `labelLayer` | 3616–3652 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 3653–3653 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 3654–3669 |  |
| `ratioT` | 3670–3680 |  |
| `buildLayers` | 3681–3693 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 3694–4002 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4003–4032 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4033–4036 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4037–4039 |  |
| `fmtBig` | 4040–4067 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4068–4073 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4074–4081 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4082–4086 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4087–4097 |  |
| `revenueLens` | 4098–4099 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4100–4117 |  |
| `SVC_COST_BASES` | 4118–4130 | The Services panel: this hood's revenue per acre set against what the City |
| `serviceLens` | 4131–4131 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4132–4134 |  |
| `servicePanelFor` | 4135–4148 |  |
| `hoodPanelLens` | 4149–4152 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4153–4170 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4171–4202 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 4203–4208 |  |
| `sparklineSvg` | 4209–4224 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 4225–4294 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 4295–4321 |  |
| `openTemporal` | 4322–4350 |  |
| `renderRevenueMix` | 4351–4399 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 4400–4433 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 4434–4436 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 4437–4487 |  |
| `syncPinnedPanel` | 4488–4514 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 4515–4530 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 4531–4541 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 4542–4589 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 4590–4595 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 4596–4635 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 4636–4652 |  |
| `temporalClick` | 4653–4710 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 4711–4790 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 4791–5123 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 5124–5178 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 5179–5179 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 5180–5198 |  |
| `syncMetricButtons` | 5199–5222 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 5223–5229 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 5230–5243 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 5244–5285 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 5286–5328 |  |
| `toggleBudgetPanel` | 5329–5354 |  |
| `syncMillRates` | 5355–5385 | Paint the pod, gate it to the money view's revenue cuts, and place it. |
| `applyMetric` | 5386–5407 |  |
| `applyColorAdjust` | 5408–5429 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 5430–5442 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 5443–5458 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 5459–5476 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 5477–5493 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 5494–5509 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 5510–5526 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 5527–5766 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 5767–5777 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 5778–5791 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 5792–5800 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 5801–5811 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 5812–5823 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 5824–5837 | Toggle one amenity band. Glass and Infill — the rows are hidden elsewhere |
| `syncAmenityControls` | 5838–5858 | Show the amenity section in Glass and Infill (the amenity distances ride |
| `syncDevControls` | 5859–5906 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 5907–5912 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 5913–5930 |  |
| `applyMoneyDetail` | 5931–5940 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `applyMoneyMode` | 5941–5948 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 5949–5967 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 5968–5978 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 5979–5986 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 5987–6003 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 6004–6017 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 6018–6028 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 6029–6264 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 6265–6274 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 6275–6288 |  |
| `applySvcDriver` | 6289–6771 |  |

## Element ids (114) — the control surface

| id | line |
|---|---|
| `#map` | 18 |
| `#banner` | 20 |
| `#title` | 22 |
| `#title-h` | 23 |
| `#title-p` | 24 |
| `#temporal` | 35 |
| `#temporal-close` | 36 |
| `#temporal-name` | 37 |
| `#temporal-body` | 44 |
| `#temporal-chart` | 45 |
| `#temporal-read` | 46 |
| `#temporal-note` | 47 |
| `#temporal-hint` | 51 |
| `#millrates` | 67 |
| `#mill-head` | 68 |
| `#mill-rows` | 69 |
| `#mill-note` | 70 |
| `#budget` | 84 |
| `#budget-close` | 91 |
| `#budget-head` | 92 |
| `#budget-body` | 97 |
| `#budget-rows` | 98 |
| `#budget-other-hd` | 99 |
| `#budget-other` | 100 |
| `#budget-note` | 101 |
| `#peek` | 116 |
| `#peek-name` | 117 |
| `#peek-read` | 118 |
| `#peek-go` | 119 |
| `#controls` | 122 |
| `#toggle` | 135 |
| `#metric-row` | 136 |
| `#revcut` | 140 |
| `#moneymode` | 145 |
| `#views` | 151 |
| `#optpanel` | 165 |
| `#opt-fold` | 166 |
| `#opt-caret` | 166 |
| `#opt-body` | 167 |
| `#layers` | 168 |
| `#chgwindow-hd` | 169 |
| `#chgwindow` | 170 |
| `#labpick-hd` | 179 |
| `#labpick` | 180 |
| `#labcut-hd` | 181 |
| `#labcut` | 182 |
| `#moneydetail-hd` | 187 |
| `#moneydetail` | 188 |
| `#amenity-hd` | 201 |
| `#amenity` | 202 |
| `#amenity-lrt-row` | 203 |
| `#amenity-lrt-on` | 204 |
| `#amenity-school-row` | 206 |
| `#amenity-school-on` | 207 |
| `#uses-prisms-hd` | 210 |
| `#uses-prisms` | 211 |
| `#uses-prisms-on` | 213 |
| `#devmode-hd` | 216 |
| `#devmode` | 217 |
| `#devmetric-hd` | 221 |
| `#devmetric` | 222 |
| `#devwindow-hd` | 227 |
| `#devwindow` | 228 |
| `#devdetail-hd` | 233 |
| `#devdetail` | 234 |
| `#prism-hd` | 238 |
| `#prism-row` | 239 |
| `#prism-opacity` | 241 |
| `#prism-opacity-val` | 242 |
| `#services-hd` | 244 |
| `#services` | 245 |
| `#denom-hd` | 339 |
| `#denom` | 340 |
| `#ratio-denom-hd` | 344 |
| `#ratio-denom` | 345 |
| `#hoodmode` | 356 |
| `#hoodmode-btn` | 357 |
| `#coloradj` | 369 |
| `#coloradj-btn` | 370 |
| `#budget-pod` | 377 |
| `#budget-btn` | 378 |
| `#a11y` | 382 |
| `#a11y-btn` | 383 |
| `#a11y-menu` | 384 |
| `#palette` | 386 |
| `#labels-on` | 393 |
| `#reference-on` | 401 |
| `#about` | 406 |
| `#about-btn` | 407 |
| `#about-menu` | 408 |
| `#about-src-services` | 417 |
| `#about-vintage` | 445 |
| `#about-modelled` | 452 |
| `#about-budget` | 462 |
| `#about-budget-lead` | 464 |
| `#about-budget-rows` | 465 |
| `#about-budget-note` | 466 |
| `#about-updated` | 477 |
| `#botleft` | 481 |
| `#compass` | 482 |
| `#rot-ccw` | 483 |
| `#tonorth` | 490 |
| `#needle` | 492 |
| `#rot-cw` | 497 |
| `#viewbtns` | 505 |
| `#center2d` | 506 |
| `#recenter` | 507 |
| `#legend` | 509 |
| `#legend-label` | 510 |
| `#legend-min` | 512 |
| `#legend-max` | 512 |
| `#legend-cats` | 514 |
| `#revmix` | 4370 |
| `#svccost` | 4414 |
