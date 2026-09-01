# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~7,075-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

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
| `moneyColKey` | 1690–1701 |  |
| `gridScale` | 1702–1722 |  |
| `scaleT` | 1723–1729 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1730–1741 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1742–1744 |  |
| `quantile` | 1745–1759 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1760–1792 |  |
| `moneyBlurb` | 1793–1797 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1798–1810 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1811–1889 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 1890–1890 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 1891–1917 |  |
| `failLoading` | 1918–1931 |  |
| `hideLoading` | 1932–1957 |  |
| `topRings` | 1958–1974 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 1975–2000 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2001–2001 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2002–2014 |  |
| `svcT` | 2015–2019 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2020–2021 |  |
| `fmtFire` | 2022–2022 |  |
| `fmtTransit` | 2023–2024 |  |
| `fmtBike` | 2025–2025 |  |
| `fmtWater` | 2026–2028 |  |
| `fmtSvcCost` | 2029–2033 |  |
| `fmtRoadsCost` | 2034–2035 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtTransitCost` | 2036–2037 |  |
| `fmtBikeCost` | 2038–2049 |  |
| `servicePlaneLayer` | 2050–2082 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2083–2092 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2093–2098 |  |
| `DEV_IND_TOTAL` | 2099–2101 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2102–2107 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2108–2112 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2113–2118 |  |
| `devGridOfferable` | 2119–2120 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2121–2121 |  |
| `devCol` | 2122–2122 |  |
| `_devScale` | 2123–2123 |  |
| `devScale` | 2124–2130 |  |
| `devT` | 2131–2134 |  |
| `developmentPlaneLayer` | 2135–2151 |  |
| `fmtDev` | 2152–2167 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2168–2173 |  |
| `DEV_GRID_IND_N` | 2174–2174 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2175–2177 |  |
| `devGridScale` | 2178–2204 |  |
| `devGridLayer` | 2205–2253 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2254–2255 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2256–2263 |  |
| `_infillStats` | 2264–2264 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2265–2282 |  |
| `_infillRaw` | 2283–2285 |  |
| `infillScore` | 2286–2301 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2302–2303 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2304–2321 |  |
| `INFILL_CENTER` | 2322–2322 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2323–2323 |  |
| `INFILL_NEG` | 2324–2324 |  |
| `infillColorAt` | 2325–2329 |  |
| `infillPlaneLayer` | 2330–2344 |  |
| `fmtFar` | 2345–2354 |  |
| `AMENITY_HIGHLIGHT_COLOR` | 2355–2355 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2356–2410 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2411–2418 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2419–2433 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2434–2454 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2455–2455 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2456–2470 |  |
| `chgT` | 2471–2480 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2481–2511 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2512–2600 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2601–2608 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2609–2609 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2610–2617 |  |
| `deviationRate` | 2618–2660 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2661–2661 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 2662–2691 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 2692–2698 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 2699–2710 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 2711–2714 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 2715–2719 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 2720–2730 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 2731–2746 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 2747–2773 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `INST_OUTLINE_COLOR` | 2774–2826 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 2827–2831 |  |
| `bandHover` | 2832–2840 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 2841–2937 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 2938–2945 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 2946–2947 |  |
| `glassInstBandLayers` | 2948–2976 |  |
| `deviationRateExempt` | 2977–2989 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 2990–2991 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 2992–2993 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 2994–2994 |  |
| `deviationStats` | 2995–3039 |  |
| `deviationOf` | 3040–3041 |  |
| `deviationT` | 3042–3052 |  |
| `fmtDeviation` | 3053–3074 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3075–3118 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3119–3205 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3206–3228 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3229–3229 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3230–3250 |  |
| `ensureFireStations` | 3251–3266 |  |
| `TRANSIT_STATION_COLOR` | 3267–3267 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3268–3285 |  |
| `ensureTransitStations` | 3286–3301 |  |
| `TRANSIT_LINE_COLOR` | 3302–3302 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3303–3319 |  |
| `ensureLrtLines` | 3320–3336 |  |
| `BIKE_LINE_COLOR` | 3337–3337 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3338–3354 |  |
| `ensureBikeLines` | 3355–3412 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3413–3413 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3414–3417 |  |
| `BOUNDARY_COLOR` | 3418–3427 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3428–3428 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3429–3441 |  |
| `referenceSplit` | 3442–3469 |  |
| `referenceUnderLayers` | 3470–3504 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3505–3521 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3522–3541 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3542–3554 |  |
| `servicesBlurb` | 3555–3572 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3573–3596 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 3597–3607 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 3608–3659 |  |
| `REF_TIERS` | 3660–3681 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 3682–3689 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 3690–3692 |  |
| `placeAnchors` | 3693–3716 |  |
| `labelPool` | 3717–3724 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 3725–3778 |  |
| `CHROME_IDS` | 3779–3782 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 3783–3801 |  |
| `visibleLabels` | 3802–3856 |  |
| `labelLayer` | 3857–3893 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 3894–3894 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 3895–3910 |  |
| `ratioT` | 3911–3921 |  |
| `buildLayers` | 3922–3934 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 3935–4237 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4238–4267 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4268–4271 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4272–4274 |  |
| `fmtBig` | 4275–4302 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4303–4308 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4309–4316 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4317–4321 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4322–4332 |  |
| `revenueLens` | 4333–4334 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4335–4352 |  |
| `SVC_COST_BASES` | 4353–4365 | The Services panel: this hood's revenue per acre set against what the City |
| `serviceLens` | 4366–4366 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4367–4369 |  |
| `servicePanelFor` | 4370–4383 |  |
| `hoodPanelLens` | 4384–4387 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4388–4405 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4406–4437 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 4438–4443 |  |
| `sparklineSvg` | 4444–4459 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 4460–4529 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 4530–4556 |  |
| `openTemporal` | 4557–4585 |  |
| `renderRevenueMix` | 4586–4634 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 4635–4668 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 4669–4671 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 4672–4722 |  |
| `syncPinnedPanel` | 4723–4749 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 4750–4765 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 4766–4776 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 4777–4824 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 4825–4830 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 4831–4870 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 4871–4887 |  |
| `temporalClick` | 4888–4945 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 4946–5025 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 5026–5358 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 5359–5426 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 5427–5427 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 5428–5446 |  |
| `syncMetricButtons` | 5447–5470 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 5471–5477 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 5478–5491 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 5492–5533 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 5534–5576 |  |
| `toggleBudgetPanel` | 5577–5602 |  |
| `syncMillRates` | 5603–5633 | Paint the pod, gate it to the money view's revenue cuts, and place it. |
| `applyMetric` | 5634–5655 |  |
| `applyColorAdjust` | 5656–5677 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 5678–5690 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 5691–5706 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 5707–5724 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 5725–5741 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 5742–5757 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 5758–5774 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 5775–6014 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 6015–6025 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 6026–6039 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 6040–6048 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 6049–6059 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 6060–6071 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 6072–6085 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 6086–6106 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 6107–6154 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 6155–6160 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 6161–6182 |  |
| `applyMoneyDetail` | 6183–6207 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 6208–6219 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 6220–6227 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 6228–6246 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 6247–6257 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 6258–6265 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 6266–6282 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 6283–6296 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 6297–6307 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 6308–6551 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 6552–6561 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 6562–6575 |  |
| `applySvcDriver` | 6576–7075 |  |

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
| `#revmix` | 4605 |
| `#svccost` | 4649 |
