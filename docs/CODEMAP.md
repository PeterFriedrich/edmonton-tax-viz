# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~5,167-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (198 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 470–474 |  |
| `HOME` | 475–475 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 476–511 |  |
| `fmtMoney` | 512–513 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `METRICS` | 514–639 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 640–656 |  |
| `RATIO_DENOMS` | 657–718 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 719–719 |  |
| `ratioOf` | 720–720 |  |
| `ratioKept` | 721–742 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 743–753 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 754–781 |  |
| `dominantUse` | 782–815 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 816–970 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 971–1053 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |
| `changeBlurb` | 1054–1073 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1074–1090 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassBlurb` | 1091–1095 |  |
| `usesBlurb` | 1096–1110 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1111–1116 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1117–1124 |  |
| `devChoroplethBlurb` | 1125–1126 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1127–1148 |  |
| `withColourClause` | 1149–1163 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `ensureGridData` | 1164–1215 |  |
| `state` | 1216–1263 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `RAMPS` | 1264–1304 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1305–1311 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1312–1317 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1318–1318 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1319–1319 |  |
| `moneyColKey` | 1320–1331 |  |
| `gridScale` | 1332–1352 |  |
| `scaleT` | 1353–1359 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1360–1371 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1372–1379 |  |
| `quantile` | 1380–1399 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1400–1432 |  |
| `moneyBlurb` | 1433–1437 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1438–1450 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1451–1500 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### base map (no basemap tiles for v1 — just a dark backdrop)

| symbol | lines | what it does |
|---|---|---|
| `topRings` | 1501–1517 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 1518–1543 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 1544–1544 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 1545–1557 |  |
| `svcT` | 1558–1562 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 1563–1564 |  |
| `fmtFire` | 1565–1565 |  |
| `fmtTransit` | 1566–1567 |  |
| `fmtBike` | 1568–1568 |  |
| `fmtWater` | 1569–1571 |  |
| `fmtSvcCost` | 1572–1576 |  |
| `fmtRoadsCost` | 1577–1578 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtTransitCost` | 1579–1580 |  |
| `fmtBikeCost` | 1581–1592 |  |
| `servicePlaneLayer` | 1593–1625 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 1626–1635 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 1636–1641 |  |
| `DEV_IND_TOTAL` | 1642–1643 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 1644–1647 | Industrial is a hood-level choropleth only — no detail grid, not infill. |
| `devGridActive` | 1648–1652 | The 100 m detail grid applies to the residential metrics only: industrial |
| `devGridOfferable` | 1653–1653 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 1654–1654 |  |
| `devCol` | 1655–1655 |  |
| `_devScale` | 1656–1656 |  |
| `devScale` | 1657–1663 |  |
| `devT` | 1664–1667 |  |
| `developmentPlaneLayer` | 1668–1684 |  |
| `fmtDev` | 1685–1700 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 1701–1704 |  |
| `devGridColKey` | 1705–1707 |  |
| `devGridScale` | 1708–1720 |  |
| `devGridLayer` | 1721–1761 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 1762–1763 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 1764–1771 |  |
| `_infillStats` | 1772–1772 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 1773–1790 |  |
| `_infillRaw` | 1791–1793 |  |
| `infillScore` | 1794–1809 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 1810–1811 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 1812–1829 |  |
| `INFILL_CENTER` | 1830–1830 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 1831–1831 |  |
| `INFILL_NEG` | 1832–1832 |  |
| `infillColorAt` | 1833–1837 |  |
| `infillPlaneLayer` | 1838–1852 |  |
| `fmtFar` | 1853–1896 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 1897–1897 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 1898–1912 |  |
| `changeFor` | 1913–1933 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 1934–1934 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 1935–1949 |  |
| `chgT` | 1950–1959 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 1960–1965 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePlaneLayer` | 1966–1985 | Flat plane — EXTRUDED IS FALSE BY DECISION, not by omission. A prism |
| `FIRE_STATION_COLOR` | 1986–1986 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 1987–2007 |  |
| `ensureFireStations` | 2008–2023 |  |
| `TRANSIT_STATION_COLOR` | 2024–2024 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 2025–2042 |  |
| `ensureTransitStations` | 2043–2058 |  |
| `TRANSIT_LINE_COLOR` | 2059–2059 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 2060–2076 |  |
| `ensureLrtLines` | 2077–2093 |  |
| `BIKE_LINE_COLOR` | 2094–2094 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 2095–2111 |  |
| `ensureBikeLines` | 2112–2163 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 2164–2164 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 2165–2168 |  |
| `BOUNDARY_COLOR` | 2169–2172 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `referenceSplit` | 2173–2185 |  |
| `referenceUnderLayers` | 2186–2220 | Bottom of the stack: the water, under everything the map draws. |
| `referenceOverLayers` | 2221–2240 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 2241–2253 |  |
| `servicesBlurb` | 2254–2271 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 2272–2295 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 2296–2306 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 2307–2361 |  |
| `placeSize` | 2362–2366 |  |
| `PLACE_COLOR` | 2367–2367 |  |
| `HOOD_COLOR` | 2368–2370 |  |
| `placeAnchors` | 2371–2386 |  |
| `labelPool` | 2387–2394 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 2395–2448 |  |
| `CHROME_IDS` | 2449–2452 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 2453–2471 |  |
| `visibleLabels` | 2472–2522 |  |
| `labelLayer` | 2523–2559 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 2560–2560 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 2561–2576 |  |
| `ratioT` | 2577–2587 |  |
| `buildLayers` | 2588–2591 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 2592–2867 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 2868–2893 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 2894–2897 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 2898–2900 |  |
| `fmtBig` | 2901–2928 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 2929–2934 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 2935–2942 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 2943–2947 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 2948–2958 |  |
| `revenueLens` | 2959–2960 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 2961–2973 |  |
| `hoodPanelLens` | 2974–2977 | Whether the pinned-hood PANEL (assessment history / revenue mix) applies |
| `temporalFor` | 2978–2995 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 2996–3027 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 3028–3033 |  |
| `sparklineSvg` | 3034–3049 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 3050–3118 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 3119–3145 |  |
| `openTemporal` | 3146–3171 |  |
| `renderRevenueMix` | 3172–3205 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderHistory` | 3206–3231 |  |
| `syncPinnedPanel` | 3232–3255 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 3256–3271 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 3272–3282 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 3283–3330 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 3331–3336 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 3337–3375 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 3376–3392 |  |
| `temporalClick` | 3393–3450 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 3451–3517 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 3518–3753 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 3754–3801 | The sparkline rides on every OTHER view's tooltip (Services excepted |
| `REV_CUTS` | 3802–3802 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 3803–3821 |  |
| `syncMetricButtons` | 3822–3845 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 3846–3852 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 3853–3866 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 3867–3910 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |
| `syncMillRates` | 3911–3941 | Paint the pod, gate it to the money view's revenue cuts, and place it. |
| `applyMetric` | 3942–3963 |  |
| `applyColorAdjust` | 3964–3985 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 3986–3998 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 3999–4014 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 4015–4032 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 4033–4048 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 4049–4064 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 4065–4081 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 4082–4293 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 4294–4304 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 4305–4318 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 4319–4327 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 4328–4338 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 4339–4353 | Toggle the Uses view's residential prisms (height = share of zoned |
| `syncDevControls` | 4354–4401 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 4402–4407 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 4408–4425 |  |
| `applyMoneyDetail` | 4426–4435 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `applyMoneyMode` | 4436–4443 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 4444–4462 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 4463–4473 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 4474–4480 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `setPrismOpacity` | 4481–4491 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 4492–4693 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 4694–4703 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 4704–4717 |  |
| `applySvcDriver` | 4718–5167 |  |

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
| `#about-updated` | 402 |
| `#botleft` | 406 |
| `#compass` | 407 |
| `#rot-ccw` | 408 |
| `#tonorth` | 415 |
| `#needle` | 417 |
| `#rot-cw` | 422 |
| `#viewbtns` | 430 |
| `#center2d` | 431 |
| `#recenter` | 432 |
| `#legend` | 434 |
| `#legend-label` | 435 |
| `#legend-min` | 437 |
| `#legend-max` | 437 |
| `#legend-cats` | 439 |
| `#revmix` | 3191 |
