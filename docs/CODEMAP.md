# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~6,748-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (262 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 546–550 |  |
| `HOME` | 551–551 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 552–595 |  |
| `fmtMoney` | 596–597 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `METRICS` | 598–723 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 724–740 |  |
| `RATIO_DENOMS` | 741–802 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 803–803 |  |
| `ratioOf` | 804–804 |  |
| `ratioKept` | 805–826 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 827–837 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 838–865 |  |
| `dominantUse` | 866–899 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 900–1054 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1055–1159 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1160–1164 | the Lab: a container for unfinished lenses |
| `inLab` | 1165–1166 |  |
| `DEVIATION_TITLES` | 1167–1171 |  |
| `deviationTitle` | 1172–1177 |  |
| `deviationKind` | 1178–1180 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1181–1186 |  |
| `changeBlurb` | 1187–1206 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1207–1228 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassInstBlurb` | 1229–1239 | The azure cells need a sentence for the same reason the Lab's outlined |
| `amenityWhichPhrase` | 1240–1245 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1246–1251 |  |
| `infillAmenityBlurb` | 1252–1265 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1266–1280 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1281–1286 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1287–1294 |  |
| `devChoroplethBlurb` | 1295–1296 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1297–1345 |  |
| `withColourClause` | 1346–1360 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `ensureGridData` | 1361–1421 |  |
| `state` | 1422–1475 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `RAMPS` | 1476–1516 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1517–1523 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1524–1529 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1530–1530 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1531–1537 |  |
| `AMENITY_BANDS` | 1538–1539 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1540–1542 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1543–1548 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1549–1563 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1564–1569 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1570–1581 |  |
| `gridScale` | 1582–1602 |  |
| `scaleT` | 1603–1609 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1610–1621 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1622–1624 |  |
| `quantile` | 1625–1639 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1640–1672 |  |
| `moneyBlurb` | 1673–1677 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1678–1690 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1691–1740 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### base map (no basemap tiles for v1 — just a dark backdrop)

| symbol | lines | what it does |
|---|---|---|
| `topRings` | 1741–1757 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 1758–1783 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 1784–1784 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 1785–1797 |  |
| `svcT` | 1798–1802 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 1803–1804 |  |
| `fmtFire` | 1805–1805 |  |
| `fmtTransit` | 1806–1807 |  |
| `fmtBike` | 1808–1808 |  |
| `fmtWater` | 1809–1811 |  |
| `fmtSvcCost` | 1812–1816 |  |
| `fmtRoadsCost` | 1817–1818 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtTransitCost` | 1819–1820 |  |
| `fmtBikeCost` | 1821–1832 |  |
| `servicePlaneLayer` | 1833–1865 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 1866–1875 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 1876–1881 |  |
| `DEV_IND_TOTAL` | 1882–1884 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 1885–1890 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 1891–1895 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 1896–1901 |  |
| `devGridOfferable` | 1902–1903 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 1904–1904 |  |
| `devCol` | 1905–1905 |  |
| `_devScale` | 1906–1906 |  |
| `devScale` | 1907–1913 |  |
| `devT` | 1914–1917 |  |
| `developmentPlaneLayer` | 1918–1934 |  |
| `fmtDev` | 1935–1950 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 1951–1956 |  |
| `DEV_GRID_IND_N` | 1957–1957 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 1958–1960 |  |
| `devGridScale` | 1961–1987 |  |
| `devGridLayer` | 1988–2036 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2037–2038 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2039–2046 |  |
| `_infillStats` | 2047–2047 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2048–2065 |  |
| `_infillRaw` | 2066–2068 |  |
| `infillScore` | 2069–2084 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2085–2086 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2087–2104 |  |
| `INFILL_CENTER` | 2105–2105 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2106–2106 |  |
| `INFILL_NEG` | 2107–2107 |  |
| `infillColorAt` | 2108–2112 |  |
| `infillPlaneLayer` | 2113–2127 |  |
| `fmtFar` | 2128–2137 |  |
| `AMENITY_HIGHLIGHT_COLOR` | 2138–2138 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2139–2193 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2194–2194 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2195–2209 |  |
| `changeFor` | 2210–2230 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2231–2231 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2232–2246 |  |
| `chgT` | 2247–2256 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2257–2270 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePlaneLayer` | 2271–2344 | Flat plane — EXTRUDED IS FALSE BY DECISION, not by omission. Hoods moved |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2345–2352 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2353–2353 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2354–2361 |  |
| `deviationRate` | 2362–2404 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2405–2405 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 2406–2435 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 2436–2442 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 2443–2454 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 2455–2458 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 2459–2463 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 2464–2474 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 2475–2490 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 2491–2517 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `INST_OUTLINE_COLOR` | 2518–2570 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 2571–2575 |  |
| `bandHover` | 2576–2584 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 2585–2681 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 2682–2689 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 2690–2691 |  |
| `glassInstBandLayers` | 2692–2720 |  |
| `deviationRateExempt` | 2721–2733 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 2734–2735 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 2736–2737 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 2738–2738 |  |
| `deviationStats` | 2739–2783 |  |
| `deviationOf` | 2784–2785 |  |
| `deviationT` | 2786–2796 |  |
| `fmtDeviation` | 2797–2818 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 2819–2862 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 2863–2949 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 2950–2972 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 2973–2973 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 2974–2994 |  |
| `ensureFireStations` | 2995–3010 |  |
| `TRANSIT_STATION_COLOR` | 3011–3011 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3012–3029 |  |
| `ensureTransitStations` | 3030–3045 |  |
| `TRANSIT_LINE_COLOR` | 3046–3046 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3047–3063 |  |
| `ensureLrtLines` | 3064–3080 |  |
| `BIKE_LINE_COLOR` | 3081–3081 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3082–3098 |  |
| `ensureBikeLines` | 3099–3156 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3157–3157 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3158–3161 |  |
| `BOUNDARY_COLOR` | 3162–3171 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3172–3172 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3173–3185 |  |
| `referenceSplit` | 3186–3213 |  |
| `referenceUnderLayers` | 3214–3248 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3249–3265 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3266–3285 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3286–3298 |  |
| `servicesBlurb` | 3299–3316 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3317–3340 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 3341–3351 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 3352–3403 |  |
| `REF_TIERS` | 3404–3425 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 3426–3433 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 3434–3436 |  |
| `placeAnchors` | 3437–3460 |  |
| `labelPool` | 3461–3468 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 3469–3522 |  |
| `CHROME_IDS` | 3523–3526 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 3527–3545 |  |
| `visibleLabels` | 3546–3600 |  |
| `labelLayer` | 3601–3637 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 3638–3638 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 3639–3654 |  |
| `ratioT` | 3655–3665 |  |
| `buildLayers` | 3666–3678 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 3679–3979 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 3980–4009 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4010–4013 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4014–4016 |  |
| `fmtBig` | 4017–4044 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4045–4050 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4051–4058 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4059–4063 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4064–4074 |  |
| `revenueLens` | 4075–4076 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4077–4094 |  |
| `SVC_COST_BASES` | 4095–4107 | The Services panel: this hood's revenue per acre set against what the City |
| `serviceLens` | 4108–4108 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4109–4111 |  |
| `servicePanelFor` | 4112–4125 |  |
| `hoodPanelLens` | 4126–4129 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4130–4147 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4148–4179 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 4180–4185 |  |
| `sparklineSvg` | 4186–4201 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 4202–4271 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 4272–4298 |  |
| `openTemporal` | 4299–4327 |  |
| `renderRevenueMix` | 4328–4376 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 4377–4410 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 4411–4413 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 4414–4464 |  |
| `syncPinnedPanel` | 4465–4491 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 4492–4507 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 4508–4518 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 4519–4566 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 4567–4572 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 4573–4612 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 4613–4629 |  |
| `temporalClick` | 4630–4687 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 4688–4767 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 4768–5100 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 5101–5155 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 5156–5156 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 5157–5175 |  |
| `syncMetricButtons` | 5176–5199 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 5200–5206 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 5207–5220 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 5221–5262 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 5263–5305 |  |
| `toggleBudgetPanel` | 5306–5331 |  |
| `syncMillRates` | 5332–5362 | Paint the pod, gate it to the money view's revenue cuts, and place it. |
| `applyMetric` | 5363–5384 |  |
| `applyColorAdjust` | 5385–5406 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 5407–5419 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 5420–5435 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 5436–5453 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 5454–5470 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 5471–5486 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 5487–5503 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 5504–5743 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 5744–5754 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 5755–5768 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 5769–5777 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 5778–5788 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 5789–5800 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 5801–5814 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 5815–5835 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 5836–5883 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 5884–5889 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 5890–5907 |  |
| `applyMoneyDetail` | 5908–5917 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `applyMoneyMode` | 5918–5925 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 5926–5944 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 5945–5955 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 5956–5963 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 5964–5980 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 5981–5994 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 5995–6005 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 6006–6241 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 6242–6251 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 6252–6265 |  |
| `applySvcDriver` | 6266–6748 |  |

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
| `#amenity-hd` | 202 |
| `#amenity` | 203 |
| `#amenity-lrt-row` | 204 |
| `#amenity-lrt-on` | 205 |
| `#amenity-school-row` | 207 |
| `#amenity-school-on` | 208 |
| `#uses-prisms-hd` | 211 |
| `#uses-prisms` | 212 |
| `#uses-prisms-on` | 214 |
| `#devmode-hd` | 217 |
| `#devmode` | 218 |
| `#devmetric-hd` | 222 |
| `#devmetric` | 223 |
| `#devwindow-hd` | 228 |
| `#devwindow` | 229 |
| `#devdetail-hd` | 234 |
| `#devdetail` | 235 |
| `#prism-hd` | 239 |
| `#prism-row` | 240 |
| `#prism-opacity` | 242 |
| `#prism-opacity-val` | 243 |
| `#services-hd` | 245 |
| `#services` | 246 |
| `#denom-hd` | 340 |
| `#denom` | 341 |
| `#ratio-denom-hd` | 345 |
| `#ratio-denom` | 346 |
| `#hoodmode` | 357 |
| `#hoodmode-btn` | 358 |
| `#coloradj` | 370 |
| `#coloradj-btn` | 371 |
| `#budget-pod` | 378 |
| `#budget-btn` | 379 |
| `#a11y` | 383 |
| `#a11y-btn` | 384 |
| `#a11y-menu` | 385 |
| `#palette` | 387 |
| `#labels-on` | 394 |
| `#reference-on` | 402 |
| `#about` | 407 |
| `#about-btn` | 408 |
| `#about-menu` | 409 |
| `#about-src-services` | 418 |
| `#about-vintage` | 446 |
| `#about-modelled` | 453 |
| `#about-budget` | 463 |
| `#about-budget-lead` | 465 |
| `#about-budget-rows` | 466 |
| `#about-budget-note` | 467 |
| `#about-updated` | 478 |
| `#botleft` | 482 |
| `#compass` | 483 |
| `#rot-ccw` | 484 |
| `#tonorth` | 491 |
| `#needle` | 493 |
| `#rot-cw` | 498 |
| `#viewbtns` | 506 |
| `#center2d` | 507 |
| `#recenter` | 508 |
| `#legend` | 510 |
| `#legend-label` | 511 |
| `#legend-min` | 513 |
| `#legend-max` | 513 |
| `#legend-cats` | 515 |
| `#revmix` | 4347 |
| `#svccost` | 4391 |
