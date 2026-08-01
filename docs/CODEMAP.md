# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~4,505-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (177 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 389–393 |  |
| `HOME` | 394–394 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 395–430 |  |
| `fmtMoney` | 431–432 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `METRICS` | 433–558 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 559–575 |  |
| `RATIO_DENOMS` | 576–637 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 638–638 |  |
| `ratioOf` | 639–639 |  |
| `ratioKept` | 640–661 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 662–672 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 673–700 |  |
| `dominantUse` | 701–734 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 735–813 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 814–896 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |
| `changeBlurb` | 897–916 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 917–933 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassBlurb` | 934–938 |  |
| `usesBlurb` | 939–953 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 954–959 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 960–967 |  |
| `devChoroplethBlurb` | 968–969 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 970–991 |  |
| `withColourClause` | 992–1006 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `ensureGridData` | 1007–1058 |  |
| `state` | 1059–1103 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `RAMPS` | 1104–1144 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1145–1151 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1152–1157 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1158–1158 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1159–1159 |  |
| `moneyColKey` | 1160–1171 |  |
| `gridScale` | 1172–1192 |  |
| `scaleT` | 1193–1199 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1200–1211 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1212–1219 |  |
| `quantile` | 1220–1239 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1240–1272 |  |
| `moneyBlurb` | 1273–1277 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1278–1290 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1291–1340 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### base map (no basemap tiles for v1 — just a dark backdrop)

| symbol | lines | what it does |
|---|---|---|
| `topRings` | 1341–1357 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 1358–1383 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 1384–1384 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 1385–1397 |  |
| `svcT` | 1398–1402 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 1403–1404 |  |
| `fmtFire` | 1405–1405 |  |
| `fmtTransit` | 1406–1407 |  |
| `fmtWater` | 1408–1410 |  |
| `fmtSvcCost` | 1411–1422 |  |
| `servicePlaneLayer` | 1423–1455 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 1456–1465 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 1466–1471 |  |
| `DEV_IND_TOTAL` | 1472–1473 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 1474–1477 | Industrial is a hood-level choropleth only — no detail grid, not infill. |
| `devGridActive` | 1478–1482 | The 100 m detail grid applies to the residential metrics only: industrial |
| `devGridOfferable` | 1483–1483 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 1484–1484 |  |
| `devCol` | 1485–1485 |  |
| `_devScale` | 1486–1486 |  |
| `devScale` | 1487–1493 |  |
| `devT` | 1494–1497 |  |
| `developmentPlaneLayer` | 1498–1514 |  |
| `fmtDev` | 1515–1530 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 1531–1534 |  |
| `devGridColKey` | 1535–1537 |  |
| `devGridScale` | 1538–1550 |  |
| `devGridLayer` | 1551–1591 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 1592–1593 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 1594–1601 |  |
| `_infillStats` | 1602–1602 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 1603–1620 |  |
| `_infillRaw` | 1621–1623 |  |
| `infillScore` | 1624–1639 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 1640–1641 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 1642–1659 |  |
| `INFILL_CENTER` | 1660–1660 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 1661–1661 |  |
| `INFILL_NEG` | 1662–1662 |  |
| `infillColorAt` | 1663–1667 |  |
| `infillPlaneLayer` | 1668–1682 |  |
| `fmtFar` | 1683–1726 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 1727–1727 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 1728–1742 |  |
| `changeFor` | 1743–1763 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 1764–1764 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 1765–1779 |  |
| `chgT` | 1780–1789 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 1790–1795 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePlaneLayer` | 1796–1815 | Flat plane — EXTRUDED IS FALSE BY DECISION, not by omission. A prism |
| `FIRE_STATION_COLOR` | 1816–1816 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 1817–1837 |  |
| `ensureFireStations` | 1838–1853 |  |
| `TRANSIT_STATION_COLOR` | 1854–1854 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 1855–1872 |  |
| `ensureTransitStations` | 1873–1888 |  |
| `TRANSIT_LINE_COLOR` | 1889–1889 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 1890–1906 |  |
| `ensureLrtLines` | 1907–1953 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 1954–1954 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HENDAY_COLOR` | 1955–1958 |  |
| `referenceSplit` | 1959–1970 |  |
| `referenceUnderLayers` | 1971–1990 | Bottom of the stack: the water, under everything the map draws. |
| `referenceOverLayers` | 1991–2010 | Top of the stack: the ring road, over the data it helps locate. |
| `ensureReference` | 2011–2023 |  |
| `servicesBlurb` | 2024–2041 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 2042–2065 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 2066–2076 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 2077–2131 |  |
| `placeSize` | 2132–2136 |  |
| `PLACE_COLOR` | 2137–2137 |  |
| `HOOD_COLOR` | 2138–2140 |  |
| `placeAnchors` | 2141–2156 |  |
| `labelPool` | 2157–2164 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 2165–2218 |  |
| `CHROME_IDS` | 2219–2222 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 2223–2241 |  |
| `visibleLabels` | 2242–2292 |  |
| `labelLayer` | 2293–2329 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 2330–2330 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 2331–2346 |  |
| `ratioT` | 2347–2357 |  |
| `buildLayers` | 2358–2361 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 2362–2635 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 2636–2661 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 2662–2665 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 2666–2668 |  |
| `fmtBig` | 2669–2674 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |
| `temporalFor` | 2675–2692 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 2693–2724 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 2725–2730 |  |
| `sparklineSvg` | 2731–2746 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 2747–2787 | The pinned chart: same geometry, plus the things only a 300px box can |
| `openTemporal` | 2788–2821 |  |
| `closeTemporal` | 2822–2836 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `applyHoodMode` | 2837–2874 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 2875–2880 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 2881–2910 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 2911–2927 |  |
| `temporalClick` | 2928–2975 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 2976–3038 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 3039–3261 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 3262–3301 | The sparkline rides on EVERY view's tooltip, appended here rather than in |
| `REV_CUTS` | 3302–3302 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 3303–3315 |  |
| `syncMetricButtons` | 3316–3334 | Paint both rows from state.metric, and hide the cut row where it has |
| `MILL_CUT_CLASSES` | 3335–3341 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 3342–3352 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `syncMillRates` | 3353–3374 | Paint the pod, gate it to the money view's revenue cuts, and sit it under |
| `applyMetric` | 3375–3394 |  |
| `applyColorAdjust` | 3395–3416 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 3417–3429 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 3430–3445 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 3446–3463 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 3464–3479 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 3480–3495 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 3496–3512 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 3513–3691 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 3692–3702 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 3703–3716 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 3717–3725 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 3726–3736 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 3737–3751 | Toggle the Uses view's residential prisms (height = share of zoned |
| `syncDevControls` | 3752–3799 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 3800–3805 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 3806–3823 |  |
| `applyMoneyDetail` | 3824–3833 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `applyMoneyMode` | 3834–3841 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 3842–3859 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 3860–3875 | Reveal the Money lens toggle and the change window picker. Called from |
| `applyDevMode` | 3876–3882 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `setPrismOpacity` | 3883–3893 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 3894–4079 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 4080–4089 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 4090–4102 |  |
| `applySvcDriver` | 4103–4505 |  |

## Element ids (88) — the control surface

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
| `#temporal-chart` | 38 |
| `#temporal-read` | 39 |
| `#temporal-note` | 40 |
| `#temporal-hint` | 44 |
| `#millrates` | 59 |
| `#mill-head` | 60 |
| `#mill-rows` | 61 |
| `#mill-note` | 62 |
| `#peek` | 76 |
| `#peek-name` | 77 |
| `#peek-read` | 78 |
| `#peek-go` | 79 |
| `#controls` | 82 |
| `#toggle` | 88 |
| `#metric-row` | 89 |
| `#revcut` | 93 |
| `#views` | 100 |
| `#optpanel` | 108 |
| `#opt-fold` | 109 |
| `#opt-caret` | 109 |
| `#opt-body` | 110 |
| `#layers` | 111 |
| `#moneymode-hd` | 112 |
| `#moneymode` | 113 |
| `#chgwindow-hd` | 117 |
| `#chgwindow` | 118 |
| `#moneydetail-hd` | 122 |
| `#moneydetail` | 123 |
| `#uses-prisms-hd` | 127 |
| `#uses-prisms` | 128 |
| `#uses-prisms-on` | 130 |
| `#devmode-hd` | 133 |
| `#devmode` | 134 |
| `#devmetric-hd` | 138 |
| `#devmetric` | 139 |
| `#devwindow-hd` | 144 |
| `#devwindow` | 145 |
| `#devdetail-hd` | 150 |
| `#devdetail` | 151 |
| `#prism-hd` | 155 |
| `#prism-row` | 156 |
| `#prism-opacity` | 158 |
| `#prism-opacity-val` | 159 |
| `#services-hd` | 161 |
| `#services` | 162 |
| `#denom-hd` | 212 |
| `#denom` | 213 |
| `#ratio-denom-hd` | 217 |
| `#ratio-denom` | 218 |
| `#hoodmode` | 229 |
| `#hoodmode-btn` | 230 |
| `#coloradj` | 242 |
| `#coloradj-btn` | 243 |
| `#a11y` | 249 |
| `#a11y-btn` | 250 |
| `#a11y-menu` | 251 |
| `#palette` | 253 |
| `#labels-on` | 260 |
| `#reference-on` | 268 |
| `#about` | 273 |
| `#about-btn` | 274 |
| `#about-menu` | 275 |
| `#about-src-services` | 284 |
| `#about-vintage` | 303 |
| `#about-modelled` | 310 |
| `#about-updated` | 321 |
| `#botleft` | 325 |
| `#compass` | 326 |
| `#rot-ccw` | 327 |
| `#tonorth` | 334 |
| `#needle` | 336 |
| `#rot-cw` | 341 |
| `#viewbtns` | 349 |
| `#center2d` | 350 |
| `#recenter` | 351 |
| `#legend` | 353 |
| `#legend-label` | 354 |
| `#legend-min` | 356 |
| `#legend-max` | 356 |
| `#legend-cats` | 358 |
