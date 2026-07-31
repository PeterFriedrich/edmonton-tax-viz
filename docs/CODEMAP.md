# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~4,345-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (174 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 371–375 |  |
| `HOME` | 376–376 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 377–412 |  |
| `fmtMoney` | 413–414 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `METRICS` | 415–540 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 541–557 |  |
| `RATIO_DENOMS` | 558–619 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 620–620 |  |
| `ratioOf` | 621–621 |  |
| `ratioKept` | 622–643 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 644–654 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 655–682 |  |
| `dominantUse` | 683–716 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 717–795 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 796–878 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |
| `changeBlurb` | 879–898 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 899–915 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassBlurb` | 916–920 |  |
| `usesBlurb` | 921–935 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 936–941 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 942–949 |  |
| `devChoroplethBlurb` | 950–951 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 952–973 |  |
| `withColourClause` | 974–988 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `ensureGridData` | 989–1040 |  |
| `state` | 1041–1081 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `RAMPS` | 1082–1122 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1123–1129 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1130–1135 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1136–1136 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1137–1137 |  |
| `moneyColKey` | 1138–1149 |  |
| `gridScale` | 1150–1170 |  |
| `scaleT` | 1171–1177 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1178–1189 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1190–1197 |  |
| `quantile` | 1198–1217 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1218–1250 |  |
| `moneyBlurb` | 1251–1255 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1256–1268 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1269–1318 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### base map (no basemap tiles for v1 — just a dark backdrop)

| symbol | lines | what it does |
|---|---|---|
| `topRings` | 1319–1335 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 1336–1361 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 1362–1362 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 1363–1375 |  |
| `svcT` | 1376–1380 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 1381–1382 |  |
| `fmtFire` | 1383–1383 |  |
| `fmtTransit` | 1384–1385 |  |
| `fmtWater` | 1386–1388 |  |
| `fmtSvcCost` | 1389–1400 |  |
| `servicePlaneLayer` | 1401–1433 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 1434–1443 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 1444–1449 |  |
| `DEV_IND_TOTAL` | 1450–1451 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 1452–1455 | Industrial is a hood-level choropleth only — no detail grid, not infill. |
| `devGridActive` | 1456–1460 | The 100 m detail grid applies to the residential metrics only: industrial |
| `devGridOfferable` | 1461–1461 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 1462–1462 |  |
| `devCol` | 1463–1463 |  |
| `_devScale` | 1464–1464 |  |
| `devScale` | 1465–1471 |  |
| `devT` | 1472–1475 |  |
| `developmentPlaneLayer` | 1476–1492 |  |
| `fmtDev` | 1493–1508 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 1509–1512 |  |
| `devGridColKey` | 1513–1515 |  |
| `devGridScale` | 1516–1528 |  |
| `devGridLayer` | 1529–1569 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 1570–1571 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 1572–1579 |  |
| `_infillStats` | 1580–1580 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 1581–1598 |  |
| `_infillRaw` | 1599–1601 |  |
| `infillScore` | 1602–1617 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 1618–1619 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 1620–1637 |  |
| `INFILL_CENTER` | 1638–1638 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 1639–1639 |  |
| `INFILL_NEG` | 1640–1640 |  |
| `infillColorAt` | 1641–1645 |  |
| `infillPlaneLayer` | 1646–1660 |  |
| `fmtFar` | 1661–1704 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 1705–1705 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 1706–1720 |  |
| `changeFor` | 1721–1741 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 1742–1742 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 1743–1757 |  |
| `chgT` | 1758–1767 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 1768–1773 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePlaneLayer` | 1774–1793 | Flat plane — EXTRUDED IS FALSE BY DECISION, not by omission. A prism |
| `FIRE_STATION_COLOR` | 1794–1794 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 1795–1815 |  |
| `ensureFireStations` | 1816–1831 |  |
| `TRANSIT_STATION_COLOR` | 1832–1832 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 1833–1850 |  |
| `ensureTransitStations` | 1851–1866 |  |
| `TRANSIT_LINE_COLOR` | 1867–1867 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 1868–1884 |  |
| `ensureLrtLines` | 1885–1931 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 1932–1932 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HENDAY_COLOR` | 1933–1936 |  |
| `referenceSplit` | 1937–1948 |  |
| `referenceUnderLayers` | 1949–1968 | Bottom of the stack: the water, under everything the map draws. |
| `referenceOverLayers` | 1969–1988 | Top of the stack: the ring road, over the data it helps locate. |
| `ensureReference` | 1989–2001 |  |
| `servicesBlurb` | 2002–2019 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 2020–2043 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 2044–2054 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 2055–2109 |  |
| `placeSize` | 2110–2114 |  |
| `PLACE_COLOR` | 2115–2115 |  |
| `HOOD_COLOR` | 2116–2118 |  |
| `placeAnchors` | 2119–2134 |  |
| `labelPool` | 2135–2142 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 2143–2196 |  |
| `CHROME_IDS` | 2197–2199 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 2200–2218 |  |
| `visibleLabels` | 2219–2269 |  |
| `labelLayer` | 2270–2306 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 2307–2307 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 2308–2323 |  |
| `ratioT` | 2324–2334 |  |
| `buildLayers` | 2335–2338 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 2339–2612 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 2613–2638 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 2639–2642 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 2643–2645 |  |
| `fmtBig` | 2646–2651 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |
| `temporalFor` | 2652–2669 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 2670–2701 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 2702–2707 |  |
| `sparklineSvg` | 2708–2723 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 2724–2764 | The pinned chart: same geometry, plus the things only a 300px box can |
| `openTemporal` | 2765–2798 |  |
| `closeTemporal` | 2799–2810 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `applyHoodMode` | 2811–2837 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 2838–2843 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 2844–2860 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 2861–2877 |  |
| `temporalClick` | 2878–2915 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 2916–2973 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 2974–3179 | Tooltip content is per-view (closure over `state`). money: active |
| `tooltipFor` | 3180–3207 | The sparkline rides on EVERY view's tooltip, appended here rather than in |
| `REV_CUTS` | 3208–3208 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 3209–3221 |  |
| `syncMetricButtons` | 3222–3234 | Paint both rows from state.metric, and hide the cut row where it has |
| `applyMetric` | 3235–3254 |  |
| `applyColorAdjust` | 3255–3276 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 3277–3289 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 3290–3305 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 3306–3323 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 3324–3339 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 3340–3355 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 3356–3372 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 3373–3551 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 3552–3562 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 3563–3576 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 3577–3585 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 3586–3596 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 3597–3611 | Toggle the Uses view's residential prisms (height = share of zoned |
| `syncDevControls` | 3612–3659 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 3660–3665 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 3666–3683 |  |
| `applyMoneyDetail` | 3684–3693 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `applyMoneyMode` | 3694–3701 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 3702–3719 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 3720–3735 | Reveal the Money lens toggle and the change window picker. Called from |
| `applyDevMode` | 3736–3742 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `setPrismOpacity` | 3743–3753 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 3754–3938 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 3939–3948 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 3949–3961 |  |
| `applySvcDriver` | 3962–4345 |  |

## Element ids (84) — the control surface

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
| `#peek` | 58 |
| `#peek-name` | 59 |
| `#peek-read` | 60 |
| `#peek-go` | 61 |
| `#controls` | 64 |
| `#toggle` | 70 |
| `#metric-row` | 71 |
| `#revcut` | 75 |
| `#views` | 82 |
| `#optpanel` | 90 |
| `#opt-fold` | 91 |
| `#opt-caret` | 91 |
| `#opt-body` | 92 |
| `#layers` | 93 |
| `#moneymode-hd` | 94 |
| `#moneymode` | 95 |
| `#chgwindow-hd` | 99 |
| `#chgwindow` | 100 |
| `#moneydetail-hd` | 104 |
| `#moneydetail` | 105 |
| `#uses-prisms-hd` | 109 |
| `#uses-prisms` | 110 |
| `#uses-prisms-on` | 112 |
| `#devmode-hd` | 115 |
| `#devmode` | 116 |
| `#devmetric-hd` | 120 |
| `#devmetric` | 121 |
| `#devwindow-hd` | 126 |
| `#devwindow` | 127 |
| `#devdetail-hd` | 132 |
| `#devdetail` | 133 |
| `#prism-hd` | 137 |
| `#prism-row` | 138 |
| `#prism-opacity` | 140 |
| `#prism-opacity-val` | 141 |
| `#services-hd` | 143 |
| `#services` | 144 |
| `#denom-hd` | 194 |
| `#denom` | 195 |
| `#ratio-denom-hd` | 199 |
| `#ratio-denom` | 200 |
| `#hoodmode` | 211 |
| `#hoodmode-btn` | 212 |
| `#coloradj` | 224 |
| `#coloradj-btn` | 225 |
| `#a11y` | 231 |
| `#a11y-btn` | 232 |
| `#a11y-menu` | 233 |
| `#palette` | 235 |
| `#labels-on` | 242 |
| `#reference-on` | 250 |
| `#about` | 255 |
| `#about-btn` | 256 |
| `#about-menu` | 257 |
| `#about-src-services` | 266 |
| `#about-vintage` | 285 |
| `#about-modelled` | 292 |
| `#about-updated` | 303 |
| `#botleft` | 307 |
| `#compass` | 308 |
| `#rot-ccw` | 309 |
| `#tonorth` | 316 |
| `#needle` | 318 |
| `#rot-cw` | 323 |
| `#viewbtns` | 331 |
| `#center2d` | 332 |
| `#recenter` | 333 |
| `#legend` | 335 |
| `#legend-label` | 336 |
| `#legend-min` | 338 |
| `#legend-max` | 338 |
| `#legend-cats` | 340 |
