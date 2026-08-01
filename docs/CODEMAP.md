# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~4,546-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (177 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 395–399 |  |
| `HOME` | 400–400 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 401–436 |  |
| `fmtMoney` | 437–438 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `METRICS` | 439–564 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 565–581 |  |
| `RATIO_DENOMS` | 582–643 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 644–644 |  |
| `ratioOf` | 645–645 |  |
| `ratioKept` | 646–667 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 668–678 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 679–706 |  |
| `dominantUse` | 707–740 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 741–819 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 820–902 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |
| `changeBlurb` | 903–922 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 923–939 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassBlurb` | 940–944 |  |
| `usesBlurb` | 945–959 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 960–965 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 966–973 |  |
| `devChoroplethBlurb` | 974–975 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 976–997 |  |
| `withColourClause` | 998–1012 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `ensureGridData` | 1013–1064 |  |
| `state` | 1065–1109 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `RAMPS` | 1110–1150 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1151–1157 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1158–1163 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1164–1164 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1165–1165 |  |
| `moneyColKey` | 1166–1177 |  |
| `gridScale` | 1178–1198 |  |
| `scaleT` | 1199–1205 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1206–1217 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1218–1225 |  |
| `quantile` | 1226–1245 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1246–1278 |  |
| `moneyBlurb` | 1279–1283 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1284–1296 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1297–1346 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### base map (no basemap tiles for v1 — just a dark backdrop)

| symbol | lines | what it does |
|---|---|---|
| `topRings` | 1347–1363 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 1364–1389 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 1390–1390 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 1391–1403 |  |
| `svcT` | 1404–1408 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 1409–1410 |  |
| `fmtFire` | 1411–1411 |  |
| `fmtTransit` | 1412–1413 |  |
| `fmtWater` | 1414–1416 |  |
| `fmtSvcCost` | 1417–1428 |  |
| `servicePlaneLayer` | 1429–1461 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 1462–1471 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 1472–1477 |  |
| `DEV_IND_TOTAL` | 1478–1479 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 1480–1483 | Industrial is a hood-level choropleth only — no detail grid, not infill. |
| `devGridActive` | 1484–1488 | The 100 m detail grid applies to the residential metrics only: industrial |
| `devGridOfferable` | 1489–1489 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 1490–1490 |  |
| `devCol` | 1491–1491 |  |
| `_devScale` | 1492–1492 |  |
| `devScale` | 1493–1499 |  |
| `devT` | 1500–1503 |  |
| `developmentPlaneLayer` | 1504–1520 |  |
| `fmtDev` | 1521–1536 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 1537–1540 |  |
| `devGridColKey` | 1541–1543 |  |
| `devGridScale` | 1544–1556 |  |
| `devGridLayer` | 1557–1597 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 1598–1599 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 1600–1607 |  |
| `_infillStats` | 1608–1608 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 1609–1626 |  |
| `_infillRaw` | 1627–1629 |  |
| `infillScore` | 1630–1645 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 1646–1647 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 1648–1665 |  |
| `INFILL_CENTER` | 1666–1666 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 1667–1667 |  |
| `INFILL_NEG` | 1668–1668 |  |
| `infillColorAt` | 1669–1673 |  |
| `infillPlaneLayer` | 1674–1688 |  |
| `fmtFar` | 1689–1732 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 1733–1733 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 1734–1748 |  |
| `changeFor` | 1749–1769 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 1770–1770 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 1771–1785 |  |
| `chgT` | 1786–1795 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 1796–1801 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePlaneLayer` | 1802–1821 | Flat plane — EXTRUDED IS FALSE BY DECISION, not by omission. A prism |
| `FIRE_STATION_COLOR` | 1822–1822 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 1823–1843 |  |
| `ensureFireStations` | 1844–1859 |  |
| `TRANSIT_STATION_COLOR` | 1860–1860 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 1861–1878 |  |
| `ensureTransitStations` | 1879–1894 |  |
| `TRANSIT_LINE_COLOR` | 1895–1895 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 1896–1912 |  |
| `ensureLrtLines` | 1913–1959 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 1960–1960 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HENDAY_COLOR` | 1961–1964 |  |
| `referenceSplit` | 1965–1976 |  |
| `referenceUnderLayers` | 1977–1996 | Bottom of the stack: the water, under everything the map draws. |
| `referenceOverLayers` | 1997–2016 | Top of the stack: the ring road, over the data it helps locate. |
| `ensureReference` | 2017–2029 |  |
| `servicesBlurb` | 2030–2047 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 2048–2071 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 2072–2082 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 2083–2137 |  |
| `placeSize` | 2138–2142 |  |
| `PLACE_COLOR` | 2143–2143 |  |
| `HOOD_COLOR` | 2144–2146 |  |
| `placeAnchors` | 2147–2162 |  |
| `labelPool` | 2163–2170 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 2171–2224 |  |
| `CHROME_IDS` | 2225–2228 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 2229–2247 |  |
| `visibleLabels` | 2248–2298 |  |
| `labelLayer` | 2299–2335 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 2336–2336 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 2337–2352 |  |
| `ratioT` | 2353–2363 |  |
| `buildLayers` | 2364–2367 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 2368–2641 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 2642–2667 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 2668–2671 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 2672–2674 |  |
| `fmtBig` | 2675–2680 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |
| `temporalFor` | 2681–2698 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 2699–2730 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 2731–2736 |  |
| `sparklineSvg` | 2737–2752 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 2753–2793 | The pinned chart: same geometry, plus the things only a 300px box can |
| `openTemporal` | 2794–2827 |  |
| `closeTemporal` | 2828–2842 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `applyHoodMode` | 2843–2880 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 2881–2886 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 2887–2916 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 2917–2933 |  |
| `temporalClick` | 2934–2981 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 2982–3044 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 3045–3267 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 3268–3307 | The sparkline rides on EVERY view's tooltip, appended here rather than in |
| `REV_CUTS` | 3308–3308 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 3309–3327 |  |
| `syncMetricButtons` | 3328–3351 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 3352–3358 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 3359–3379 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `syncMillRates` | 3380–3410 | Paint the pod, gate it to the money view's revenue cuts, and place it. |
| `applyMetric` | 3411–3430 |  |
| `applyColorAdjust` | 3431–3452 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 3453–3465 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 3466–3481 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 3482–3499 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 3500–3515 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 3516–3531 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 3532–3548 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 3549–3727 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 3728–3738 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 3739–3752 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 3753–3761 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 3762–3772 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 3773–3787 | Toggle the Uses view's residential prisms (height = share of zoned |
| `syncDevControls` | 3788–3835 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 3836–3841 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 3842–3859 |  |
| `applyMoneyDetail` | 3860–3869 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `applyMoneyMode` | 3870–3877 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 3878–3896 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 3897–3907 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 3908–3914 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `setPrismOpacity` | 3915–3925 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 3926–4113 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 4114–4123 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 4124–4136 |  |
| `applySvcDriver` | 4137–4546 |  |

## Element ids (87) — the control surface

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
| `#toggle` | 95 |
| `#metric-row` | 96 |
| `#revcut` | 100 |
| `#moneymode` | 105 |
| `#views` | 111 |
| `#optpanel` | 119 |
| `#opt-fold` | 120 |
| `#opt-caret` | 120 |
| `#opt-body` | 121 |
| `#layers` | 122 |
| `#chgwindow-hd` | 123 |
| `#chgwindow` | 124 |
| `#moneydetail-hd` | 128 |
| `#moneydetail` | 129 |
| `#uses-prisms-hd` | 133 |
| `#uses-prisms` | 134 |
| `#uses-prisms-on` | 136 |
| `#devmode-hd` | 139 |
| `#devmode` | 140 |
| `#devmetric-hd` | 144 |
| `#devmetric` | 145 |
| `#devwindow-hd` | 150 |
| `#devwindow` | 151 |
| `#devdetail-hd` | 156 |
| `#devdetail` | 157 |
| `#prism-hd` | 161 |
| `#prism-row` | 162 |
| `#prism-opacity` | 164 |
| `#prism-opacity-val` | 165 |
| `#services-hd` | 167 |
| `#services` | 168 |
| `#denom-hd` | 218 |
| `#denom` | 219 |
| `#ratio-denom-hd` | 223 |
| `#ratio-denom` | 224 |
| `#hoodmode` | 235 |
| `#hoodmode-btn` | 236 |
| `#coloradj` | 248 |
| `#coloradj-btn` | 249 |
| `#a11y` | 255 |
| `#a11y-btn` | 256 |
| `#a11y-menu` | 257 |
| `#palette` | 259 |
| `#labels-on` | 266 |
| `#reference-on` | 274 |
| `#about` | 279 |
| `#about-btn` | 280 |
| `#about-menu` | 281 |
| `#about-src-services` | 290 |
| `#about-vintage` | 309 |
| `#about-modelled` | 316 |
| `#about-updated` | 327 |
| `#botleft` | 331 |
| `#compass` | 332 |
| `#rot-ccw` | 333 |
| `#tonorth` | 340 |
| `#needle` | 342 |
| `#rot-cw` | 347 |
| `#viewbtns` | 355 |
| `#center2d` | 356 |
| `#recenter` | 357 |
| `#legend` | 359 |
| `#legend-label` | 360 |
| `#legend-min` | 362 |
| `#legend-max` | 362 |
| `#legend-cats` | 364 |
