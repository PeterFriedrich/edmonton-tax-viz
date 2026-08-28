# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~6,935-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (266 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 564–568 |  |
| `HOME` | 569–569 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 570–613 |  |
| `fmtMoney` | 614–615 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `METRICS` | 616–741 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 742–758 |  |
| `RATIO_DENOMS` | 759–820 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 821–821 |  |
| `ratioOf` | 822–822 |  |
| `ratioKept` | 823–844 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 845–855 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 856–883 |  |
| `dominantUse` | 884–917 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 918–1072 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1073–1177 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1178–1182 | the Lab: a container for unfinished lenses |
| `inLab` | 1183–1184 |  |
| `DEVIATION_TITLES` | 1185–1189 |  |
| `deviationTitle` | 1190–1195 |  |
| `deviationKind` | 1196–1198 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1199–1204 |  |
| `changeBlurb` | 1205–1227 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1228–1249 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassInstBlurb` | 1250–1260 | The azure cells need a sentence for the same reason the Lab's outlined |
| `amenityWhichPhrase` | 1261–1266 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1267–1272 |  |
| `infillAmenityBlurb` | 1273–1286 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1287–1301 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1302–1307 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1308–1315 |  |
| `devChoroplethBlurb` | 1316–1317 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1318–1366 |  |
| `withColourClause` | 1367–1381 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `ensureGridData` | 1382–1442 |  |
| `state` | 1443–1496 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `RAMPS` | 1497–1537 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1538–1544 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1545–1550 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1551–1551 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1552–1558 |  |
| `AMENITY_BANDS` | 1559–1560 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1561–1563 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1564–1569 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1570–1584 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1585–1590 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1591–1602 |  |
| `gridScale` | 1603–1623 |  |
| `scaleT` | 1624–1630 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1631–1642 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1643–1645 |  |
| `quantile` | 1646–1660 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1661–1693 |  |
| `moneyBlurb` | 1694–1698 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1699–1711 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1712–1790 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 1791–1791 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 1792–1818 |  |
| `failLoading` | 1819–1832 |  |
| `hideLoading` | 1833–1858 |  |
| `topRings` | 1859–1875 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 1876–1901 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 1902–1902 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 1903–1915 |  |
| `svcT` | 1916–1920 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 1921–1922 |  |
| `fmtFire` | 1923–1923 |  |
| `fmtTransit` | 1924–1925 |  |
| `fmtBike` | 1926–1926 |  |
| `fmtWater` | 1927–1929 |  |
| `fmtSvcCost` | 1930–1934 |  |
| `fmtRoadsCost` | 1935–1936 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtTransitCost` | 1937–1938 |  |
| `fmtBikeCost` | 1939–1950 |  |
| `servicePlaneLayer` | 1951–1983 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 1984–1993 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 1994–1999 |  |
| `DEV_IND_TOTAL` | 2000–2002 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2003–2008 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2009–2013 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2014–2019 |  |
| `devGridOfferable` | 2020–2021 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2022–2022 |  |
| `devCol` | 2023–2023 |  |
| `_devScale` | 2024–2024 |  |
| `devScale` | 2025–2031 |  |
| `devT` | 2032–2035 |  |
| `developmentPlaneLayer` | 2036–2052 |  |
| `fmtDev` | 2053–2068 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2069–2074 |  |
| `DEV_GRID_IND_N` | 2075–2075 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2076–2078 |  |
| `devGridScale` | 2079–2105 |  |
| `devGridLayer` | 2106–2154 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2155–2156 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2157–2164 |  |
| `_infillStats` | 2165–2165 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2166–2183 |  |
| `_infillRaw` | 2184–2186 |  |
| `infillScore` | 2187–2202 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2203–2204 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2205–2222 |  |
| `INFILL_CENTER` | 2223–2223 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2224–2224 |  |
| `INFILL_NEG` | 2225–2225 |  |
| `infillColorAt` | 2226–2230 |  |
| `infillPlaneLayer` | 2231–2245 |  |
| `fmtFar` | 2246–2255 |  |
| `AMENITY_HIGHLIGHT_COLOR` | 2256–2256 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2257–2311 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2312–2317 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2318–2332 | Hardcoded, and deliberately NOT derived from temporal.json's last year: the |
| `changeFor` | 2333–2353 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2354–2354 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2355–2369 |  |
| `chgT` | 2370–2379 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2380–2410 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2411–2499 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2500–2507 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2508–2508 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2509–2516 |  |
| `deviationRate` | 2517–2559 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2560–2560 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 2561–2590 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 2591–2597 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 2598–2609 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 2610–2613 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 2614–2618 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 2619–2629 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 2630–2645 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 2646–2672 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `INST_OUTLINE_COLOR` | 2673–2725 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 2726–2730 |  |
| `bandHover` | 2731–2739 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 2740–2836 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 2837–2844 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 2845–2846 |  |
| `glassInstBandLayers` | 2847–2875 |  |
| `deviationRateExempt` | 2876–2888 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 2889–2890 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 2891–2892 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 2893–2893 |  |
| `deviationStats` | 2894–2938 |  |
| `deviationOf` | 2939–2940 |  |
| `deviationT` | 2941–2951 |  |
| `fmtDeviation` | 2952–2973 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 2974–3017 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3018–3104 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3105–3127 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3128–3128 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3129–3149 |  |
| `ensureFireStations` | 3150–3165 |  |
| `TRANSIT_STATION_COLOR` | 3166–3166 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3167–3184 |  |
| `ensureTransitStations` | 3185–3200 |  |
| `TRANSIT_LINE_COLOR` | 3201–3201 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3202–3218 |  |
| `ensureLrtLines` | 3219–3235 |  |
| `BIKE_LINE_COLOR` | 3236–3236 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3237–3253 |  |
| `ensureBikeLines` | 3254–3311 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3312–3312 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3313–3316 |  |
| `BOUNDARY_COLOR` | 3317–3326 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3327–3327 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3328–3340 |  |
| `referenceSplit` | 3341–3368 |  |
| `referenceUnderLayers` | 3369–3403 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3404–3420 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3421–3440 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3441–3453 |  |
| `servicesBlurb` | 3454–3471 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3472–3495 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 3496–3506 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 3507–3558 |  |
| `REF_TIERS` | 3559–3580 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 3581–3588 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 3589–3591 |  |
| `placeAnchors` | 3592–3615 |  |
| `labelPool` | 3616–3623 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 3624–3677 |  |
| `CHROME_IDS` | 3678–3681 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 3682–3700 |  |
| `visibleLabels` | 3701–3755 |  |
| `labelLayer` | 3756–3792 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 3793–3793 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 3794–3809 |  |
| `ratioT` | 3810–3820 |  |
| `buildLayers` | 3821–3833 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 3834–4136 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4137–4166 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4167–4170 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4171–4173 |  |
| `fmtBig` | 4174–4201 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4202–4207 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4208–4215 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4216–4220 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4221–4231 |  |
| `revenueLens` | 4232–4233 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4234–4251 |  |
| `SVC_COST_BASES` | 4252–4264 | The Services panel: this hood's revenue per acre set against what the City |
| `serviceLens` | 4265–4265 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4266–4268 |  |
| `servicePanelFor` | 4269–4282 |  |
| `hoodPanelLens` | 4283–4286 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4287–4304 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4305–4336 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 4337–4342 |  |
| `sparklineSvg` | 4343–4358 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 4359–4428 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 4429–4455 |  |
| `openTemporal` | 4456–4484 |  |
| `renderRevenueMix` | 4485–4533 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 4534–4567 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 4568–4570 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 4571–4621 |  |
| `syncPinnedPanel` | 4622–4648 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 4649–4664 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 4665–4675 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 4676–4723 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 4724–4729 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 4730–4769 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 4770–4786 |  |
| `temporalClick` | 4787–4844 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 4845–4924 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 4925–5257 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 5258–5325 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 5326–5326 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 5327–5345 |  |
| `syncMetricButtons` | 5346–5369 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 5370–5376 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 5377–5390 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 5391–5432 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 5433–5475 |  |
| `toggleBudgetPanel` | 5476–5501 |  |
| `syncMillRates` | 5502–5532 | Paint the pod, gate it to the money view's revenue cuts, and place it. |
| `applyMetric` | 5533–5554 |  |
| `applyColorAdjust` | 5555–5576 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 5577–5589 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 5590–5605 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 5606–5623 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 5624–5640 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 5641–5656 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 5657–5673 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 5674–5913 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 5914–5924 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 5925–5938 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 5939–5947 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 5948–5958 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 5959–5970 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 5971–5984 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 5985–6005 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 6006–6053 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 6054–6059 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 6060–6077 |  |
| `applyMoneyDetail` | 6078–6087 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `applyMoneyMode` | 6088–6095 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 6096–6114 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 6115–6125 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 6126–6133 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 6134–6150 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 6151–6164 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 6165–6175 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 6176–6411 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 6412–6421 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 6422–6435 |  |
| `applySvcDriver` | 6436–6935 |  |

## Element ids (121) — the control surface

| id | line |
|---|---|
| `#map` | 18 |
| `#loading` | 22 |
| `#loading-box` | 23 |
| `#loading-title` | 30 |
| `#loading-blurb` | 31 |
| `#loading-spinner` | 32 |
| `#loading-text` | 33 |
| `#loading-retry` | 34 |
| `#banner` | 38 |
| `#title` | 40 |
| `#title-h` | 41 |
| `#title-p` | 42 |
| `#temporal` | 53 |
| `#temporal-close` | 54 |
| `#temporal-name` | 55 |
| `#temporal-body` | 62 |
| `#temporal-chart` | 63 |
| `#temporal-read` | 64 |
| `#temporal-note` | 65 |
| `#temporal-hint` | 69 |
| `#millrates` | 85 |
| `#mill-head` | 86 |
| `#mill-rows` | 87 |
| `#mill-note` | 88 |
| `#budget` | 102 |
| `#budget-close` | 109 |
| `#budget-head` | 110 |
| `#budget-body` | 115 |
| `#budget-rows` | 116 |
| `#budget-other-hd` | 117 |
| `#budget-other` | 118 |
| `#budget-note` | 119 |
| `#peek` | 134 |
| `#peek-name` | 135 |
| `#peek-read` | 136 |
| `#peek-go` | 137 |
| `#controls` | 140 |
| `#toggle` | 153 |
| `#metric-row` | 154 |
| `#revcut` | 158 |
| `#moneymode` | 163 |
| `#views` | 169 |
| `#optpanel` | 183 |
| `#opt-fold` | 184 |
| `#opt-caret` | 184 |
| `#opt-body` | 185 |
| `#layers` | 186 |
| `#chgwindow-hd` | 187 |
| `#chgwindow` | 188 |
| `#labpick-hd` | 197 |
| `#labpick` | 198 |
| `#labcut-hd` | 199 |
| `#labcut` | 200 |
| `#moneydetail-hd` | 205 |
| `#moneydetail` | 206 |
| `#amenity-hd` | 220 |
| `#amenity` | 221 |
| `#amenity-lrt-row` | 222 |
| `#amenity-lrt-on` | 223 |
| `#amenity-school-row` | 225 |
| `#amenity-school-on` | 226 |
| `#uses-prisms-hd` | 229 |
| `#uses-prisms` | 230 |
| `#uses-prisms-on` | 232 |
| `#devmode-hd` | 235 |
| `#devmode` | 236 |
| `#devmetric-hd` | 240 |
| `#devmetric` | 241 |
| `#devwindow-hd` | 246 |
| `#devwindow` | 247 |
| `#devdetail-hd` | 252 |
| `#devdetail` | 253 |
| `#prism-hd` | 257 |
| `#prism-row` | 258 |
| `#prism-opacity` | 260 |
| `#prism-opacity-val` | 261 |
| `#services-hd` | 263 |
| `#services` | 264 |
| `#denom-hd` | 358 |
| `#denom` | 359 |
| `#ratio-denom-hd` | 363 |
| `#ratio-denom` | 364 |
| `#hoodmode` | 375 |
| `#hoodmode-btn` | 376 |
| `#coloradj` | 388 |
| `#coloradj-btn` | 389 |
| `#budget-pod` | 396 |
| `#budget-btn` | 397 |
| `#a11y` | 401 |
| `#a11y-btn` | 402 |
| `#a11y-menu` | 403 |
| `#palette` | 405 |
| `#labels-on` | 412 |
| `#reference-on` | 420 |
| `#about` | 425 |
| `#about-btn` | 426 |
| `#about-menu` | 427 |
| `#about-src-services` | 436 |
| `#about-vintage` | 464 |
| `#about-modelled` | 471 |
| `#about-budget` | 481 |
| `#about-budget-lead` | 483 |
| `#about-budget-rows` | 484 |
| `#about-budget-note` | 485 |
| `#about-updated` | 496 |
| `#botleft` | 500 |
| `#compass` | 501 |
| `#rot-ccw` | 502 |
| `#tonorth` | 509 |
| `#needle` | 511 |
| `#rot-cw` | 516 |
| `#viewbtns` | 524 |
| `#center2d` | 525 |
| `#recenter` | 526 |
| `#legend` | 528 |
| `#legend-label` | 529 |
| `#legend-min` | 531 |
| `#legend-max` | 531 |
| `#legend-cats` | 533 |
| `#revmix` | 4504 |
| `#svccost` | 4548 |
