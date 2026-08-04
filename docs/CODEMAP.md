# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~5,081-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (196 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 467–471 |  |
| `HOME` | 472–472 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 473–508 |  |
| `fmtMoney` | 509–510 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `METRICS` | 511–636 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 637–653 |  |
| `RATIO_DENOMS` | 654–715 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 716–716 |  |
| `ratioOf` | 717–717 |  |
| `ratioKept` | 718–739 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 740–750 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 751–778 |  |
| `dominantUse` | 779–812 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 813–967 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 968–1050 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |
| `changeBlurb` | 1051–1070 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1071–1087 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassBlurb` | 1088–1092 |  |
| `usesBlurb` | 1093–1107 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1108–1113 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1114–1121 |  |
| `devChoroplethBlurb` | 1122–1123 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1124–1145 |  |
| `withColourClause` | 1146–1160 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `ensureGridData` | 1161–1212 |  |
| `state` | 1213–1260 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `RAMPS` | 1261–1301 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1302–1308 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1309–1314 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1315–1315 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1316–1316 |  |
| `moneyColKey` | 1317–1328 |  |
| `gridScale` | 1329–1349 |  |
| `scaleT` | 1350–1356 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1357–1368 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1369–1376 |  |
| `quantile` | 1377–1396 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1397–1429 |  |
| `moneyBlurb` | 1430–1434 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1435–1447 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1448–1497 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### base map (no basemap tiles for v1 — just a dark backdrop)

| symbol | lines | what it does |
|---|---|---|
| `topRings` | 1498–1514 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 1515–1540 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 1541–1541 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 1542–1554 |  |
| `svcT` | 1555–1559 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 1560–1561 |  |
| `fmtFire` | 1562–1562 |  |
| `fmtTransit` | 1563–1564 |  |
| `fmtBike` | 1565–1565 |  |
| `fmtWater` | 1566–1568 |  |
| `fmtSvcCost` | 1569–1573 |  |
| `fmtRoadsCost` | 1574–1575 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtTransitCost` | 1576–1577 |  |
| `fmtBikeCost` | 1578–1589 |  |
| `servicePlaneLayer` | 1590–1622 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 1623–1632 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 1633–1638 |  |
| `DEV_IND_TOTAL` | 1639–1640 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 1641–1644 | Industrial is a hood-level choropleth only — no detail grid, not infill. |
| `devGridActive` | 1645–1649 | The 100 m detail grid applies to the residential metrics only: industrial |
| `devGridOfferable` | 1650–1650 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 1651–1651 |  |
| `devCol` | 1652–1652 |  |
| `_devScale` | 1653–1653 |  |
| `devScale` | 1654–1660 |  |
| `devT` | 1661–1664 |  |
| `developmentPlaneLayer` | 1665–1681 |  |
| `fmtDev` | 1682–1697 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 1698–1701 |  |
| `devGridColKey` | 1702–1704 |  |
| `devGridScale` | 1705–1717 |  |
| `devGridLayer` | 1718–1758 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 1759–1760 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 1761–1768 |  |
| `_infillStats` | 1769–1769 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 1770–1787 |  |
| `_infillRaw` | 1788–1790 |  |
| `infillScore` | 1791–1806 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 1807–1808 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 1809–1826 |  |
| `INFILL_CENTER` | 1827–1827 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 1828–1828 |  |
| `INFILL_NEG` | 1829–1829 |  |
| `infillColorAt` | 1830–1834 |  |
| `infillPlaneLayer` | 1835–1849 |  |
| `fmtFar` | 1850–1893 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 1894–1894 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 1895–1909 |  |
| `changeFor` | 1910–1930 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 1931–1931 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 1932–1946 |  |
| `chgT` | 1947–1956 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 1957–1962 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePlaneLayer` | 1963–1982 | Flat plane — EXTRUDED IS FALSE BY DECISION, not by omission. A prism |
| `FIRE_STATION_COLOR` | 1983–1983 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 1984–2004 |  |
| `ensureFireStations` | 2005–2020 |  |
| `TRANSIT_STATION_COLOR` | 2021–2021 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 2022–2039 |  |
| `ensureTransitStations` | 2040–2055 |  |
| `TRANSIT_LINE_COLOR` | 2056–2056 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 2057–2073 |  |
| `ensureLrtLines` | 2074–2090 |  |
| `BIKE_LINE_COLOR` | 2091–2091 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 2092–2108 |  |
| `ensureBikeLines` | 2109–2160 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 2161–2161 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 2162–2165 |  |
| `BOUNDARY_COLOR` | 2166–2169 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `referenceSplit` | 2170–2182 |  |
| `referenceUnderLayers` | 2183–2217 | Bottom of the stack: the water, under everything the map draws. |
| `referenceOverLayers` | 2218–2237 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 2238–2250 |  |
| `servicesBlurb` | 2251–2268 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 2269–2292 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 2293–2303 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 2304–2358 |  |
| `placeSize` | 2359–2363 |  |
| `PLACE_COLOR` | 2364–2364 |  |
| `HOOD_COLOR` | 2365–2367 |  |
| `placeAnchors` | 2368–2383 |  |
| `labelPool` | 2384–2391 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 2392–2445 |  |
| `CHROME_IDS` | 2446–2449 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 2450–2468 |  |
| `visibleLabels` | 2469–2519 |  |
| `labelLayer` | 2520–2556 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 2557–2557 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 2558–2573 |  |
| `ratioT` | 2574–2584 |  |
| `buildLayers` | 2585–2588 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 2589–2864 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 2865–2890 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 2891–2894 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 2895–2897 |  |
| `fmtBig` | 2898–2925 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 2926–2931 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 2932–2939 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 2940–2944 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 2945–2955 |  |
| `revenueLens` | 2956–2957 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 2958–2962 |  |
| `temporalFor` | 2963–2980 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 2981–3012 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 3013–3018 |  |
| `sparklineSvg` | 3019–3034 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 3035–3103 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 3104–3130 |  |
| `openTemporal` | 3131–3156 |  |
| `renderRevenueMix` | 3157–3190 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderHistory` | 3191–3216 |  |
| `syncPinnedPanel` | 3217–3231 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 3232–3249 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `applyHoodMode` | 3250–3292 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 3293–3298 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 3299–3332 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 3333–3349 |  |
| `temporalClick` | 3350–3397 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 3398–3464 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 3465–3687 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 3688–3732 | The sparkline rides on EVERY view's tooltip, appended here rather than in |
| `REV_CUTS` | 3733–3733 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 3734–3752 |  |
| `syncMetricButtons` | 3753–3776 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 3777–3783 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 3784–3797 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 3798–3841 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |
| `syncMillRates` | 3842–3872 | Paint the pod, gate it to the money view's revenue cuts, and place it. |
| `applyMetric` | 3873–3893 |  |
| `applyColorAdjust` | 3894–3915 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 3916–3928 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 3929–3944 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 3945–3962 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 3963–3978 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 3979–3994 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 3995–4011 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 4012–4223 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 4224–4234 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 4235–4248 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 4249–4257 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 4258–4268 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 4269–4283 | Toggle the Uses view's residential prisms (height = share of zoned |
| `syncDevControls` | 4284–4331 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 4332–4337 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 4338–4355 |  |
| `applyMoneyDetail` | 4356–4365 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `applyMoneyMode` | 4366–4373 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 4374–4392 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 4393–4403 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 4404–4410 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `setPrismOpacity` | 4411–4421 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 4422–4611 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 4612–4621 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 4622–4635 |  |
| `applySvcDriver` | 4636–5081 |  |

## Element ids (93) — the control surface

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
| `#views` | 119 |
| `#optpanel` | 127 |
| `#opt-fold` | 128 |
| `#opt-caret` | 128 |
| `#opt-body` | 129 |
| `#layers` | 130 |
| `#chgwindow-hd` | 131 |
| `#chgwindow` | 132 |
| `#moneydetail-hd` | 136 |
| `#moneydetail` | 137 |
| `#uses-prisms-hd` | 141 |
| `#uses-prisms` | 142 |
| `#uses-prisms-on` | 144 |
| `#devmode-hd` | 147 |
| `#devmode` | 148 |
| `#devmetric-hd` | 152 |
| `#devmetric` | 153 |
| `#devwindow-hd` | 158 |
| `#devwindow` | 159 |
| `#devdetail-hd` | 164 |
| `#devdetail` | 165 |
| `#prism-hd` | 169 |
| `#prism-row` | 170 |
| `#prism-opacity` | 172 |
| `#prism-opacity-val` | 173 |
| `#services-hd` | 175 |
| `#services` | 176 |
| `#denom-hd` | 270 |
| `#denom` | 271 |
| `#ratio-denom-hd` | 275 |
| `#ratio-denom` | 276 |
| `#hoodmode` | 287 |
| `#hoodmode-btn` | 288 |
| `#coloradj` | 300 |
| `#coloradj-btn` | 301 |
| `#a11y` | 307 |
| `#a11y-btn` | 308 |
| `#a11y-menu` | 309 |
| `#palette` | 311 |
| `#labels-on` | 318 |
| `#reference-on` | 326 |
| `#about` | 331 |
| `#about-btn` | 332 |
| `#about-menu` | 333 |
| `#about-src-services` | 342 |
| `#about-vintage` | 370 |
| `#about-modelled` | 377 |
| `#about-budget` | 387 |
| `#about-budget-lead` | 389 |
| `#about-budget-rows` | 390 |
| `#about-budget-note` | 391 |
| `#about-updated` | 399 |
| `#botleft` | 403 |
| `#compass` | 404 |
| `#rot-ccw` | 405 |
| `#tonorth` | 412 |
| `#needle` | 414 |
| `#rot-cw` | 419 |
| `#viewbtns` | 427 |
| `#center2d` | 428 |
| `#recenter` | 429 |
| `#legend` | 431 |
| `#legend-label` | 432 |
| `#legend-min` | 434 |
| `#legend-max` | 434 |
| `#legend-cats` | 436 |
| `#revmix` | 3176 |
