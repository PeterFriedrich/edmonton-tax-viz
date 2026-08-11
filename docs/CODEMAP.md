# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~5,626-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (216 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 471–475 |  |
| `HOME` | 476–476 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 477–512 |  |
| `fmtMoney` | 513–514 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `METRICS` | 515–640 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 641–657 |  |
| `RATIO_DENOMS` | 658–719 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 720–720 |  |
| `ratioOf` | 721–721 |  |
| `ratioKept` | 722–743 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 744–754 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 755–782 |  |
| `dominantUse` | 783–816 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 817–971 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 972–1060 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |
| `DEVIATION_TITLES` | 1061–1065 |  |
| `deviationTitle` | 1066–1070 |  |
| `changeBlurb` | 1071–1090 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1091–1107 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassBlurb` | 1108–1112 |  |
| `usesBlurb` | 1113–1127 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1128–1133 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1134–1141 |  |
| `devChoroplethBlurb` | 1142–1143 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1144–1165 |  |
| `withColourClause` | 1166–1180 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `ensureGridData` | 1181–1232 |  |
| `state` | 1233–1280 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `RAMPS` | 1281–1321 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1322–1328 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1329–1334 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1335–1335 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1336–1336 |  |
| `moneyColKey` | 1337–1348 |  |
| `gridScale` | 1349–1369 |  |
| `scaleT` | 1370–1376 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1377–1388 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1389–1396 |  |
| `quantile` | 1397–1416 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1417–1449 |  |
| `moneyBlurb` | 1450–1454 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1455–1467 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1468–1517 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### base map (no basemap tiles for v1 — just a dark backdrop)

| symbol | lines | what it does |
|---|---|---|
| `topRings` | 1518–1534 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 1535–1560 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 1561–1561 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 1562–1574 |  |
| `svcT` | 1575–1579 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 1580–1581 |  |
| `fmtFire` | 1582–1582 |  |
| `fmtTransit` | 1583–1584 |  |
| `fmtBike` | 1585–1585 |  |
| `fmtWater` | 1586–1588 |  |
| `fmtSvcCost` | 1589–1593 |  |
| `fmtRoadsCost` | 1594–1595 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtTransitCost` | 1596–1597 |  |
| `fmtBikeCost` | 1598–1609 |  |
| `servicePlaneLayer` | 1610–1642 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 1643–1652 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 1653–1658 |  |
| `DEV_IND_TOTAL` | 1659–1660 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 1661–1664 | Industrial is a hood-level choropleth only — no detail grid, not infill. |
| `devGridActive` | 1665–1669 | The 100 m detail grid applies to the residential metrics only: industrial |
| `devGridOfferable` | 1670–1670 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 1671–1671 |  |
| `devCol` | 1672–1672 |  |
| `_devScale` | 1673–1673 |  |
| `devScale` | 1674–1680 |  |
| `devT` | 1681–1684 |  |
| `developmentPlaneLayer` | 1685–1701 |  |
| `fmtDev` | 1702–1717 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 1718–1721 |  |
| `devGridColKey` | 1722–1724 |  |
| `devGridScale` | 1725–1737 |  |
| `devGridLayer` | 1738–1778 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 1779–1780 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 1781–1788 |  |
| `_infillStats` | 1789–1789 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 1790–1807 |  |
| `_infillRaw` | 1808–1810 |  |
| `infillScore` | 1811–1826 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 1827–1828 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 1829–1846 |  |
| `INFILL_CENTER` | 1847–1847 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 1848–1848 |  |
| `INFILL_NEG` | 1849–1849 |  |
| `infillColorAt` | 1850–1854 |  |
| `infillPlaneLayer` | 1855–1869 |  |
| `fmtFar` | 1870–1913 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 1914–1914 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 1915–1929 |  |
| `changeFor` | 1930–1950 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 1951–1951 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 1952–1966 |  |
| `chgT` | 1967–1976 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 1977–1990 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePlaneLayer` | 1991–2029 | Flat plane — EXTRUDED IS FALSE BY DECISION, not by omission. Hoods moved |

### deviation lens: revenue per acre against the citywide average

| symbol | lines | what it does |
|---|---|---|
| `_devStats` | 2030–2030 | deviation lens: revenue per acre against the citywide average |
| `deviationStats` | 2031–2063 |  |
| `deviationOf` | 2064–2065 |  |
| `deviationT` | 2066–2076 |  |
| `fmtDeviation` | 2077–2092 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 2093–2124 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBlurb` | 2125–2141 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 2142–2142 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 2143–2163 |  |
| `ensureFireStations` | 2164–2179 |  |
| `TRANSIT_STATION_COLOR` | 2180–2180 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 2181–2198 |  |
| `ensureTransitStations` | 2199–2214 |  |
| `TRANSIT_LINE_COLOR` | 2215–2215 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 2216–2232 |  |
| `ensureLrtLines` | 2233–2249 |  |
| `BIKE_LINE_COLOR` | 2250–2250 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 2251–2267 |  |
| `ensureBikeLines` | 2268–2325 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 2326–2326 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 2327–2330 |  |
| `BOUNDARY_COLOR` | 2331–2340 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 2341–2341 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 2342–2354 |  |
| `referenceSplit` | 2355–2382 |  |
| `referenceUnderLayers` | 2383–2417 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 2418–2434 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 2435–2454 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 2455–2467 |  |
| `servicesBlurb` | 2468–2485 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 2486–2509 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 2510–2520 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 2521–2572 |  |
| `REF_TIERS` | 2573–2594 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 2595–2602 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 2603–2605 |  |
| `placeAnchors` | 2606–2629 |  |
| `labelPool` | 2630–2637 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 2638–2691 |  |
| `CHROME_IDS` | 2692–2695 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 2696–2714 |  |
| `visibleLabels` | 2715–2769 |  |
| `labelLayer` | 2770–2806 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 2807–2807 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 2808–2823 |  |
| `ratioT` | 2824–2834 |  |
| `buildLayers` | 2835–2838 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 2839–3123 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 3124–3153 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 3154–3157 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 3158–3160 |  |
| `fmtBig` | 3161–3188 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 3189–3194 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 3195–3202 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 3203–3207 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 3208–3218 |  |
| `revenueLens` | 3219–3220 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 3221–3238 |  |
| `SVC_COST_BASES` | 3239–3251 | The Services panel: this hood's revenue per acre set against what the City |
| `serviceLens` | 3252–3252 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 3253–3255 |  |
| `servicePanelFor` | 3256–3269 |  |
| `hoodPanelLens` | 3270–3273 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 3274–3291 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 3292–3323 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 3324–3329 |  |
| `sparklineSvg` | 3330–3345 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 3346–3415 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 3416–3442 |  |
| `openTemporal` | 3443–3471 |  |
| `renderRevenueMix` | 3472–3520 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 3521–3554 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 3555–3557 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 3558–3608 |  |
| `syncPinnedPanel` | 3609–3635 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 3636–3651 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 3652–3662 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 3663–3710 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 3711–3716 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 3717–3756 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 3757–3773 |  |
| `temporalClick` | 3774–3831 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 3832–3904 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 3905–4157 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 4158–4205 | The sparkline rides on every OTHER view's tooltip (Services excepted |
| `REV_CUTS` | 4206–4206 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 4207–4225 |  |
| `syncMetricButtons` | 4226–4263 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 4264–4270 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 4271–4284 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 4285–4328 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |
| `syncMillRates` | 4329–4359 | Paint the pod, gate it to the money view's revenue cuts, and place it. |
| `applyMetric` | 4360–4392 |  |
| `applyColorAdjust` | 4393–4414 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 4415–4427 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 4428–4443 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 4444–4461 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 4462–4477 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 4478–4493 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 4494–4510 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 4511–4734 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 4735–4745 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 4746–4759 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 4760–4768 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 4769–4779 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 4780–4794 | Toggle the Uses view's residential prisms (height = share of zoned |
| `syncDevControls` | 4795–4842 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 4843–4848 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 4849–4866 |  |
| `applyMoneyDetail` | 4867–4876 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `applyMoneyMode` | 4877–4885 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 4886–4904 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 4905–4915 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 4916–4922 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `setPrismOpacity` | 4923–4933 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 4934–5149 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 5150–5159 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 5160–5173 |  |
| `applySvcDriver` | 5174–5626 |  |

## Element ids (94) — the control surface

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
| `#peek` | 84 |
| `#peek-name` | 85 |
| `#peek-read` | 86 |
| `#peek-go` | 87 |
| `#controls` | 90 |
| `#toggle` | 103 |
| `#metric-row` | 104 |
| `#revcut` | 108 |
| `#moneymode` | 113 |
| `#views` | 120 |
| `#optpanel` | 128 |
| `#opt-fold` | 129 |
| `#opt-caret` | 129 |
| `#opt-body` | 130 |
| `#layers` | 131 |
| `#chgwindow-hd` | 132 |
| `#chgwindow` | 133 |
| `#moneydetail-hd` | 137 |
| `#moneydetail` | 138 |
| `#uses-prisms-hd` | 142 |
| `#uses-prisms` | 143 |
| `#uses-prisms-on` | 145 |
| `#devmode-hd` | 148 |
| `#devmode` | 149 |
| `#devmetric-hd` | 153 |
| `#devmetric` | 154 |
| `#devwindow-hd` | 159 |
| `#devwindow` | 160 |
| `#devdetail-hd` | 165 |
| `#devdetail` | 166 |
| `#prism-hd` | 170 |
| `#prism-row` | 171 |
| `#prism-opacity` | 173 |
| `#prism-opacity-val` | 174 |
| `#services-hd` | 176 |
| `#services` | 177 |
| `#denom-hd` | 271 |
| `#denom` | 272 |
| `#ratio-denom-hd` | 276 |
| `#ratio-denom` | 277 |
| `#hoodmode` | 288 |
| `#hoodmode-btn` | 289 |
| `#coloradj` | 301 |
| `#coloradj-btn` | 302 |
| `#a11y` | 308 |
| `#a11y-btn` | 309 |
| `#a11y-menu` | 310 |
| `#palette` | 312 |
| `#labels-on` | 319 |
| `#reference-on` | 327 |
| `#about` | 332 |
| `#about-btn` | 333 |
| `#about-menu` | 334 |
| `#about-src-services` | 343 |
| `#about-vintage` | 371 |
| `#about-modelled` | 378 |
| `#about-budget` | 388 |
| `#about-budget-lead` | 390 |
| `#about-budget-rows` | 391 |
| `#about-budget-note` | 392 |
| `#about-updated` | 403 |
| `#botleft` | 407 |
| `#compass` | 408 |
| `#rot-ccw` | 409 |
| `#tonorth` | 416 |
| `#needle` | 418 |
| `#rot-cw` | 423 |
| `#viewbtns` | 431 |
| `#center2d` | 432 |
| `#recenter` | 433 |
| `#legend` | 435 |
| `#legend-label` | 436 |
| `#legend-min` | 438 |
| `#legend-max` | 438 |
| `#legend-cats` | 440 |
| `#revmix` | 3491 |
| `#svccost` | 3535 |
