# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~6,727-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (259 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 543–547 |  |
| `HOME` | 548–548 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 549–592 |  |
| `fmtMoney` | 593–594 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `METRICS` | 595–720 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 721–737 |  |
| `RATIO_DENOMS` | 738–799 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 800–800 |  |
| `ratioOf` | 801–801 |  |
| `ratioKept` | 802–823 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 824–834 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 835–862 |  |
| `dominantUse` | 863–896 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 897–1051 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1052–1156 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1157–1161 | the Lab: a container for unfinished lenses |
| `inLab` | 1162–1163 |  |
| `DEVIATION_TITLES` | 1164–1168 |  |
| `deviationTitle` | 1169–1174 |  |
| `deviationKind` | 1175–1177 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1178–1183 |  |
| `changeBlurb` | 1184–1203 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1204–1225 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassInstBlurb` | 1226–1237 | The azure cells need a sentence for the same reason the Lab's outlined |
| `amenityBlurb` | 1238–1257 | A greyed city needs to say why, and needs to say HOW MUCH survived |
| `glassBlurb` | 1258–1263 |  |
| `usesBlurb` | 1264–1278 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1279–1284 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1285–1292 |  |
| `devChoroplethBlurb` | 1293–1294 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1295–1343 |  |
| `withColourClause` | 1344–1358 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `ensureGridData` | 1359–1419 |  |
| `state` | 1420–1473 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `RAMPS` | 1474–1514 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1515–1521 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1522–1527 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1528–1528 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1529–1535 |  |
| `AMENITY_BANDS` | 1536–1543 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1544–1546 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1547–1552 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1553–1567 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1568–1573 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1574–1585 |  |
| `gridScale` | 1586–1606 |  |
| `scaleT` | 1607–1613 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1614–1625 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1626–1628 |  |
| `quantile` | 1629–1643 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1644–1676 |  |
| `moneyBlurb` | 1677–1681 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1682–1694 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1695–1744 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### base map (no basemap tiles for v1 — just a dark backdrop)

| symbol | lines | what it does |
|---|---|---|
| `topRings` | 1745–1761 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 1762–1787 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 1788–1788 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 1789–1801 |  |
| `svcT` | 1802–1806 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 1807–1808 |  |
| `fmtFire` | 1809–1809 |  |
| `fmtTransit` | 1810–1811 |  |
| `fmtBike` | 1812–1812 |  |
| `fmtWater` | 1813–1815 |  |
| `fmtSvcCost` | 1816–1820 |  |
| `fmtRoadsCost` | 1821–1822 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtTransitCost` | 1823–1824 |  |
| `fmtBikeCost` | 1825–1836 |  |
| `servicePlaneLayer` | 1837–1869 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 1870–1879 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 1880–1885 |  |
| `DEV_IND_TOTAL` | 1886–1888 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 1889–1894 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 1895–1899 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 1900–1905 |  |
| `devGridOfferable` | 1906–1907 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 1908–1908 |  |
| `devCol` | 1909–1909 |  |
| `_devScale` | 1910–1910 |  |
| `devScale` | 1911–1917 |  |
| `devT` | 1918–1921 |  |
| `developmentPlaneLayer` | 1922–1938 |  |
| `fmtDev` | 1939–1954 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 1955–1960 |  |
| `DEV_GRID_IND_N` | 1961–1961 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 1962–1964 |  |
| `devGridScale` | 1965–1991 |  |
| `devGridLayer` | 1992–2040 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2041–2042 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2043–2050 |  |
| `_infillStats` | 2051–2051 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2052–2069 |  |
| `_infillRaw` | 2070–2072 |  |
| `infillScore` | 2073–2088 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2089–2090 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2091–2108 |  |
| `INFILL_CENTER` | 2109–2109 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2110–2110 |  |
| `INFILL_NEG` | 2111–2111 |  |
| `infillColorAt` | 2112–2116 |  |
| `infillPlaneLayer` | 2117–2131 |  |
| `fmtFar` | 2132–2175 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2176–2176 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2177–2191 |  |
| `changeFor` | 2192–2212 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2213–2213 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2214–2228 |  |
| `chgT` | 2229–2238 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2239–2252 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePlaneLayer` | 2253–2326 | Flat plane — EXTRUDED IS FALSE BY DECISION, not by omission. Hoods moved |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2327–2334 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2335–2335 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2336–2343 |  |
| `deviationRate` | 2344–2381 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2382–2382 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `instFrac` | 2383–2412 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 2413–2419 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 2420–2431 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 2432–2435 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 2436–2440 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 2441–2451 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 2452–2467 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 2468–2494 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `INST_OUTLINE_COLOR` | 2495–2547 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 2548–2552 |  |
| `bandHover` | 2553–2561 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 2562–2658 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 2659–2666 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 2667–2668 |  |
| `glassInstBandLayers` | 2669–2697 |  |
| `deviationRateExempt` | 2698–2710 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 2711–2712 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 2713–2714 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 2715–2715 |  |
| `deviationStats` | 2716–2760 |  |
| `deviationOf` | 2761–2762 |  |
| `deviationT` | 2763–2773 |  |
| `fmtDeviation` | 2774–2795 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 2796–2839 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 2840–2926 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 2927–2949 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 2950–2950 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 2951–2971 |  |
| `ensureFireStations` | 2972–2987 |  |
| `TRANSIT_STATION_COLOR` | 2988–2988 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 2989–3006 |  |
| `ensureTransitStations` | 3007–3022 |  |
| `TRANSIT_LINE_COLOR` | 3023–3023 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3024–3040 |  |
| `ensureLrtLines` | 3041–3057 |  |
| `BIKE_LINE_COLOR` | 3058–3058 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3059–3075 |  |
| `ensureBikeLines` | 3076–3133 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3134–3134 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3135–3138 |  |
| `BOUNDARY_COLOR` | 3139–3148 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3149–3149 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3150–3162 |  |
| `referenceSplit` | 3163–3190 |  |
| `referenceUnderLayers` | 3191–3225 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3226–3242 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3243–3262 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3263–3275 |  |
| `servicesBlurb` | 3276–3293 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3294–3317 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 3318–3328 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 3329–3380 |  |
| `REF_TIERS` | 3381–3402 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 3403–3410 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 3411–3413 |  |
| `placeAnchors` | 3414–3437 |  |
| `labelPool` | 3438–3445 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 3446–3499 |  |
| `CHROME_IDS` | 3500–3503 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 3504–3522 |  |
| `visibleLabels` | 3523–3577 |  |
| `labelLayer` | 3578–3614 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 3615–3615 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 3616–3631 |  |
| `ratioT` | 3632–3642 |  |
| `buildLayers` | 3643–3655 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 3656–3960 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 3961–3990 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 3991–3994 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 3995–3997 |  |
| `fmtBig` | 3998–4025 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4026–4031 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4032–4039 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4040–4044 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4045–4055 |  |
| `revenueLens` | 4056–4057 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4058–4075 |  |
| `SVC_COST_BASES` | 4076–4088 | The Services panel: this hood's revenue per acre set against what the City |
| `serviceLens` | 4089–4089 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4090–4092 |  |
| `servicePanelFor` | 4093–4106 |  |
| `hoodPanelLens` | 4107–4110 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4111–4128 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4129–4160 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 4161–4166 |  |
| `sparklineSvg` | 4167–4182 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 4183–4252 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 4253–4279 |  |
| `openTemporal` | 4280–4308 |  |
| `renderRevenueMix` | 4309–4357 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 4358–4391 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 4392–4394 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 4395–4445 |  |
| `syncPinnedPanel` | 4446–4472 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 4473–4488 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 4489–4499 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 4500–4547 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 4548–4553 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 4554–4593 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 4594–4610 |  |
| `temporalClick` | 4611–4668 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 4669–4748 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 4749–5081 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 5082–5136 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 5137–5137 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 5138–5156 |  |
| `syncMetricButtons` | 5157–5180 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 5181–5187 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 5188–5201 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 5202–5243 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 5244–5286 |  |
| `toggleBudgetPanel` | 5287–5312 |  |
| `syncMillRates` | 5313–5343 | Paint the pod, gate it to the money view's revenue cuts, and place it. |
| `applyMetric` | 5344–5365 |  |
| `applyColorAdjust` | 5366–5387 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 5388–5400 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 5401–5416 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 5417–5434 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 5435–5451 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 5452–5467 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 5468–5484 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 5485–5724 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 5725–5735 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 5736–5749 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 5750–5758 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 5759–5769 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 5770–5781 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 5782–5793 | Toggle one amenity band. Glass-only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 5794–5814 | Show the amenity section only in Glass, and only for the rows whose |
| `syncDevControls` | 5815–5862 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 5863–5868 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 5869–5886 |  |
| `applyMoneyDetail` | 5887–5896 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `applyMoneyMode` | 5897–5904 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 5905–5923 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 5924–5934 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 5935–5942 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 5943–5959 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 5960–5973 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 5974–5984 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 5985–6220 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 6221–6230 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 6231–6244 |  |
| `applySvcDriver` | 6245–6727 |  |

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
| `#amenity-hd` | 199 |
| `#amenity` | 200 |
| `#amenity-lrt-row` | 201 |
| `#amenity-lrt-on` | 202 |
| `#amenity-school-row` | 204 |
| `#amenity-school-on` | 205 |
| `#uses-prisms-hd` | 208 |
| `#uses-prisms` | 209 |
| `#uses-prisms-on` | 211 |
| `#devmode-hd` | 214 |
| `#devmode` | 215 |
| `#devmetric-hd` | 219 |
| `#devmetric` | 220 |
| `#devwindow-hd` | 225 |
| `#devwindow` | 226 |
| `#devdetail-hd` | 231 |
| `#devdetail` | 232 |
| `#prism-hd` | 236 |
| `#prism-row` | 237 |
| `#prism-opacity` | 239 |
| `#prism-opacity-val` | 240 |
| `#services-hd` | 242 |
| `#services` | 243 |
| `#denom-hd` | 337 |
| `#denom` | 338 |
| `#ratio-denom-hd` | 342 |
| `#ratio-denom` | 343 |
| `#hoodmode` | 354 |
| `#hoodmode-btn` | 355 |
| `#coloradj` | 367 |
| `#coloradj-btn` | 368 |
| `#budget-pod` | 375 |
| `#budget-btn` | 376 |
| `#a11y` | 380 |
| `#a11y-btn` | 381 |
| `#a11y-menu` | 382 |
| `#palette` | 384 |
| `#labels-on` | 391 |
| `#reference-on` | 399 |
| `#about` | 404 |
| `#about-btn` | 405 |
| `#about-menu` | 406 |
| `#about-src-services` | 415 |
| `#about-vintage` | 443 |
| `#about-modelled` | 450 |
| `#about-budget` | 460 |
| `#about-budget-lead` | 462 |
| `#about-budget-rows` | 463 |
| `#about-budget-note` | 464 |
| `#about-updated` | 475 |
| `#botleft` | 479 |
| `#compass` | 480 |
| `#rot-ccw` | 481 |
| `#tonorth` | 488 |
| `#needle` | 490 |
| `#rot-cw` | 495 |
| `#viewbtns` | 503 |
| `#center2d` | 504 |
| `#recenter` | 505 |
| `#legend` | 507 |
| `#legend-label` | 508 |
| `#legend-min` | 510 |
| `#legend-max` | 510 |
| `#legend-cats` | 512 |
| `#revmix` | 4328 |
| `#svccost` | 4372 |
