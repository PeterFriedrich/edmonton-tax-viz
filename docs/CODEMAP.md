# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~5,032-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (195 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 456–460 |  |
| `HOME` | 461–461 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 462–497 |  |
| `fmtMoney` | 498–499 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `METRICS` | 500–625 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 626–642 |  |
| `RATIO_DENOMS` | 643–704 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 705–705 |  |
| `ratioOf` | 706–706 |  |
| `ratioKept` | 707–728 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 729–739 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 740–767 |  |
| `dominantUse` | 768–801 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 802–956 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 957–1039 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |
| `changeBlurb` | 1040–1059 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1060–1076 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassBlurb` | 1077–1081 |  |
| `usesBlurb` | 1082–1096 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1097–1102 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1103–1110 |  |
| `devChoroplethBlurb` | 1111–1112 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1113–1134 |  |
| `withColourClause` | 1135–1149 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `ensureGridData` | 1150–1201 |  |
| `state` | 1202–1249 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `RAMPS` | 1250–1290 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1291–1297 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1298–1303 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1304–1304 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1305–1305 |  |
| `moneyColKey` | 1306–1317 |  |
| `gridScale` | 1318–1338 |  |
| `scaleT` | 1339–1345 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1346–1357 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1358–1365 |  |
| `quantile` | 1366–1385 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1386–1418 |  |
| `moneyBlurb` | 1419–1423 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1424–1436 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1437–1486 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### base map (no basemap tiles for v1 — just a dark backdrop)

| symbol | lines | what it does |
|---|---|---|
| `topRings` | 1487–1503 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 1504–1529 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 1530–1530 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 1531–1543 |  |
| `svcT` | 1544–1548 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 1549–1550 |  |
| `fmtFire` | 1551–1551 |  |
| `fmtTransit` | 1552–1553 |  |
| `fmtBike` | 1554–1554 |  |
| `fmtWater` | 1555–1557 |  |
| `fmtSvcCost` | 1558–1562 |  |
| `fmtRoadsCost` | 1563–1564 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtTransitCost` | 1565–1566 |  |
| `fmtBikeCost` | 1567–1578 |  |
| `servicePlaneLayer` | 1579–1611 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 1612–1621 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 1622–1627 |  |
| `DEV_IND_TOTAL` | 1628–1629 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 1630–1633 | Industrial is a hood-level choropleth only — no detail grid, not infill. |
| `devGridActive` | 1634–1638 | The 100 m detail grid applies to the residential metrics only: industrial |
| `devGridOfferable` | 1639–1639 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 1640–1640 |  |
| `devCol` | 1641–1641 |  |
| `_devScale` | 1642–1642 |  |
| `devScale` | 1643–1649 |  |
| `devT` | 1650–1653 |  |
| `developmentPlaneLayer` | 1654–1670 |  |
| `fmtDev` | 1671–1686 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 1687–1690 |  |
| `devGridColKey` | 1691–1693 |  |
| `devGridScale` | 1694–1706 |  |
| `devGridLayer` | 1707–1747 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 1748–1749 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 1750–1757 |  |
| `_infillStats` | 1758–1758 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 1759–1776 |  |
| `_infillRaw` | 1777–1779 |  |
| `infillScore` | 1780–1795 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 1796–1797 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 1798–1815 |  |
| `INFILL_CENTER` | 1816–1816 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 1817–1817 |  |
| `INFILL_NEG` | 1818–1818 |  |
| `infillColorAt` | 1819–1823 |  |
| `infillPlaneLayer` | 1824–1838 |  |
| `fmtFar` | 1839–1882 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 1883–1883 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 1884–1898 |  |
| `changeFor` | 1899–1919 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 1920–1920 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 1921–1935 |  |
| `chgT` | 1936–1945 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 1946–1951 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePlaneLayer` | 1952–1971 | Flat plane — EXTRUDED IS FALSE BY DECISION, not by omission. A prism |
| `FIRE_STATION_COLOR` | 1972–1972 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 1973–1993 |  |
| `ensureFireStations` | 1994–2009 |  |
| `TRANSIT_STATION_COLOR` | 2010–2010 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 2011–2028 |  |
| `ensureTransitStations` | 2029–2044 |  |
| `TRANSIT_LINE_COLOR` | 2045–2045 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 2046–2062 |  |
| `ensureLrtLines` | 2063–2079 |  |
| `BIKE_LINE_COLOR` | 2080–2080 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 2081–2097 |  |
| `ensureBikeLines` | 2098–2149 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 2150–2150 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 2151–2154 |  |
| `BOUNDARY_COLOR` | 2155–2158 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `referenceSplit` | 2159–2171 |  |
| `referenceUnderLayers` | 2172–2206 | Bottom of the stack: the water, under everything the map draws. |
| `referenceOverLayers` | 2207–2226 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 2227–2239 |  |
| `servicesBlurb` | 2240–2257 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 2258–2281 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 2282–2292 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 2293–2347 |  |
| `placeSize` | 2348–2352 |  |
| `PLACE_COLOR` | 2353–2353 |  |
| `HOOD_COLOR` | 2354–2356 |  |
| `placeAnchors` | 2357–2372 |  |
| `labelPool` | 2373–2380 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 2381–2434 |  |
| `CHROME_IDS` | 2435–2438 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 2439–2457 |  |
| `visibleLabels` | 2458–2508 |  |
| `labelLayer` | 2509–2545 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 2546–2546 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 2547–2562 |  |
| `ratioT` | 2563–2573 |  |
| `buildLayers` | 2574–2577 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 2578–2853 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 2854–2879 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 2880–2883 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 2884–2886 |  |
| `fmtBig` | 2887–2914 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 2915–2920 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 2921–2928 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 2929–2933 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 2934–2944 |  |
| `revenueLens` | 2945–2946 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 2947–2951 |  |
| `temporalFor` | 2952–2969 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 2970–3001 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 3002–3007 |  |
| `sparklineSvg` | 3008–3023 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 3024–3092 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 3093–3119 |  |
| `openTemporal` | 3120–3145 |  |
| `renderRevenueMix` | 3146–3179 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderHistory` | 3180–3205 |  |
| `syncPinnedPanel` | 3206–3220 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 3221–3238 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `applyHoodMode` | 3239–3281 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 3282–3287 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 3288–3321 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 3322–3338 |  |
| `temporalClick` | 3339–3386 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 3387–3453 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 3454–3676 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 3677–3721 | The sparkline rides on EVERY view's tooltip, appended here rather than in |
| `REV_CUTS` | 3722–3722 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 3723–3741 |  |
| `syncMetricButtons` | 3742–3765 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 3766–3772 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 3773–3793 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `syncMillRates` | 3794–3824 | Paint the pod, gate it to the money view's revenue cuts, and place it. |
| `applyMetric` | 3825–3845 |  |
| `applyColorAdjust` | 3846–3867 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 3868–3880 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 3881–3896 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 3897–3914 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 3915–3930 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 3931–3946 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 3947–3963 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 3964–4175 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 4176–4186 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 4187–4200 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 4201–4209 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 4210–4220 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 4221–4235 | Toggle the Uses view's residential prisms (height = share of zoned |
| `syncDevControls` | 4236–4283 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 4284–4289 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 4290–4307 |  |
| `applyMoneyDetail` | 4308–4317 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `applyMoneyMode` | 4318–4325 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 4326–4344 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 4345–4355 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 4356–4362 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `setPrismOpacity` | 4363–4373 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 4374–4563 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 4564–4573 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 4574–4587 |  |
| `applySvcDriver` | 4588–5032 |  |

## Element ids (89) — the control surface

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
| `#about-updated` | 388 |
| `#botleft` | 392 |
| `#compass` | 393 |
| `#rot-ccw` | 394 |
| `#tonorth` | 401 |
| `#needle` | 403 |
| `#rot-cw` | 408 |
| `#viewbtns` | 416 |
| `#center2d` | 417 |
| `#recenter` | 418 |
| `#legend` | 420 |
| `#legend-label` | 421 |
| `#legend-min` | 423 |
| `#legend-max` | 423 |
| `#legend-cats` | 425 |
| `#revmix` | 3165 |
