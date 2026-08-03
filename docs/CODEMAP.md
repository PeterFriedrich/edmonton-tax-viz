# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~4,895-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (192 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 426–430 |  |
| `HOME` | 431–431 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 432–467 |  |
| `fmtMoney` | 468–469 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `METRICS` | 470–595 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 596–612 |  |
| `RATIO_DENOMS` | 613–674 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 675–675 |  |
| `ratioOf` | 676–676 |  |
| `ratioKept` | 677–698 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 699–709 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 710–737 |  |
| `dominantUse` | 738–771 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 772–867 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 868–950 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |
| `changeBlurb` | 951–970 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 971–987 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassBlurb` | 988–992 |  |
| `usesBlurb` | 993–1007 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1008–1013 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1014–1021 |  |
| `devChoroplethBlurb` | 1022–1023 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1024–1045 |  |
| `withColourClause` | 1046–1060 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `ensureGridData` | 1061–1112 |  |
| `state` | 1113–1159 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `RAMPS` | 1160–1200 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1201–1207 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1208–1213 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1214–1214 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1215–1215 |  |
| `moneyColKey` | 1216–1227 |  |
| `gridScale` | 1228–1248 |  |
| `scaleT` | 1249–1255 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1256–1267 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1268–1275 |  |
| `quantile` | 1276–1295 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1296–1328 |  |
| `moneyBlurb` | 1329–1333 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1334–1346 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1347–1396 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### base map (no basemap tiles for v1 — just a dark backdrop)

| symbol | lines | what it does |
|---|---|---|
| `topRings` | 1397–1413 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 1414–1439 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 1440–1440 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 1441–1453 |  |
| `svcT` | 1454–1458 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 1459–1460 |  |
| `fmtFire` | 1461–1461 |  |
| `fmtTransit` | 1462–1463 |  |
| `fmtBike` | 1464–1464 |  |
| `fmtWater` | 1465–1467 |  |
| `fmtSvcCost` | 1468–1479 |  |
| `servicePlaneLayer` | 1480–1512 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 1513–1522 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 1523–1528 |  |
| `DEV_IND_TOTAL` | 1529–1530 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 1531–1534 | Industrial is a hood-level choropleth only — no detail grid, not infill. |
| `devGridActive` | 1535–1539 | The 100 m detail grid applies to the residential metrics only: industrial |
| `devGridOfferable` | 1540–1540 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 1541–1541 |  |
| `devCol` | 1542–1542 |  |
| `_devScale` | 1543–1543 |  |
| `devScale` | 1544–1550 |  |
| `devT` | 1551–1554 |  |
| `developmentPlaneLayer` | 1555–1571 |  |
| `fmtDev` | 1572–1587 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 1588–1591 |  |
| `devGridColKey` | 1592–1594 |  |
| `devGridScale` | 1595–1607 |  |
| `devGridLayer` | 1608–1648 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 1649–1650 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 1651–1658 |  |
| `_infillStats` | 1659–1659 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 1660–1677 |  |
| `_infillRaw` | 1678–1680 |  |
| `infillScore` | 1681–1696 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 1697–1698 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 1699–1716 |  |
| `INFILL_CENTER` | 1717–1717 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 1718–1718 |  |
| `INFILL_NEG` | 1719–1719 |  |
| `infillColorAt` | 1720–1724 |  |
| `infillPlaneLayer` | 1725–1739 |  |
| `fmtFar` | 1740–1783 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 1784–1784 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 1785–1799 |  |
| `changeFor` | 1800–1820 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 1821–1821 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 1822–1836 |  |
| `chgT` | 1837–1846 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 1847–1852 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePlaneLayer` | 1853–1872 | Flat plane — EXTRUDED IS FALSE BY DECISION, not by omission. A prism |
| `FIRE_STATION_COLOR` | 1873–1873 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 1874–1894 |  |
| `ensureFireStations` | 1895–1910 |  |
| `TRANSIT_STATION_COLOR` | 1911–1911 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 1912–1929 |  |
| `ensureTransitStations` | 1930–1945 |  |
| `TRANSIT_LINE_COLOR` | 1946–1946 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 1947–1963 |  |
| `ensureLrtLines` | 1964–1980 |  |
| `BIKE_LINE_COLOR` | 1981–1981 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 1982–1998 |  |
| `ensureBikeLines` | 1999–2050 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 2051–2051 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 2052–2055 |  |
| `BOUNDARY_COLOR` | 2056–2059 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `referenceSplit` | 2060–2072 |  |
| `referenceUnderLayers` | 2073–2107 | Bottom of the stack: the water, under everything the map draws. |
| `referenceOverLayers` | 2108–2127 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 2128–2140 |  |
| `servicesBlurb` | 2141–2158 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 2159–2182 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 2183–2193 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 2194–2248 |  |
| `placeSize` | 2249–2253 |  |
| `PLACE_COLOR` | 2254–2254 |  |
| `HOOD_COLOR` | 2255–2257 |  |
| `placeAnchors` | 2258–2273 |  |
| `labelPool` | 2274–2281 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 2282–2335 |  |
| `CHROME_IDS` | 2336–2339 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 2340–2358 |  |
| `visibleLabels` | 2359–2409 |  |
| `labelLayer` | 2410–2446 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 2447–2447 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 2448–2463 |  |
| `ratioT` | 2464–2474 |  |
| `buildLayers` | 2475–2478 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 2479–2754 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 2755–2780 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 2781–2784 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 2785–2787 |  |
| `fmtBig` | 2788–2815 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 2816–2821 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 2822–2829 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 2830–2834 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 2835–2845 |  |
| `revenueLens` | 2846–2847 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 2848–2852 |  |
| `temporalFor` | 2853–2870 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 2871–2902 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 2903–2908 |  |
| `sparklineSvg` | 2909–2924 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 2925–2993 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 2994–3020 |  |
| `openTemporal` | 3021–3046 |  |
| `renderRevenueMix` | 3047–3080 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderHistory` | 3081–3106 |  |
| `syncPinnedPanel` | 3107–3121 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 3122–3139 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `applyHoodMode` | 3140–3182 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 3183–3188 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 3189–3222 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 3223–3239 |  |
| `temporalClick` | 3240–3287 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 3288–3351 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 3352–3574 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 3575–3619 | The sparkline rides on EVERY view's tooltip, appended here rather than in |
| `REV_CUTS` | 3620–3620 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 3621–3639 |  |
| `syncMetricButtons` | 3640–3663 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 3664–3670 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 3671–3691 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `syncMillRates` | 3692–3722 | Paint the pod, gate it to the money view's revenue cuts, and place it. |
| `applyMetric` | 3723–3743 |  |
| `applyColorAdjust` | 3744–3765 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 3766–3778 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 3779–3794 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 3795–3812 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 3813–3828 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 3829–3844 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 3845–3861 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 3862–4049 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 4050–4060 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 4061–4074 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 4075–4083 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 4084–4094 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 4095–4109 | Toggle the Uses view's residential prisms (height = share of zoned |
| `syncDevControls` | 4110–4157 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 4158–4163 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 4164–4181 |  |
| `applyMoneyDetail` | 4182–4191 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `applyMoneyMode` | 4192–4199 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 4200–4218 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 4219–4229 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 4230–4236 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `setPrismOpacity` | 4237–4247 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 4248–4437 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 4438–4447 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 4448–4461 |  |
| `applySvcDriver` | 4462–4895 |  |

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
| `#denom-hd` | 240 |
| `#denom` | 241 |
| `#ratio-denom-hd` | 245 |
| `#ratio-denom` | 246 |
| `#hoodmode` | 257 |
| `#hoodmode-btn` | 258 |
| `#coloradj` | 270 |
| `#coloradj-btn` | 271 |
| `#a11y` | 277 |
| `#a11y-btn` | 278 |
| `#a11y-menu` | 279 |
| `#palette` | 281 |
| `#labels-on` | 288 |
| `#reference-on` | 296 |
| `#about` | 301 |
| `#about-btn` | 302 |
| `#about-menu` | 303 |
| `#about-src-services` | 312 |
| `#about-vintage` | 340 |
| `#about-modelled` | 347 |
| `#about-updated` | 358 |
| `#botleft` | 362 |
| `#compass` | 363 |
| `#rot-ccw` | 364 |
| `#tonorth` | 371 |
| `#needle` | 373 |
| `#rot-cw` | 378 |
| `#viewbtns` | 386 |
| `#center2d` | 387 |
| `#recenter` | 388 |
| `#legend` | 390 |
| `#legend-label` | 391 |
| `#legend-min` | 393 |
| `#legend-max` | 393 |
| `#legend-cats` | 395 |
| `#revmix` | 3066 |
