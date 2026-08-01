# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~4,412-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

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
| `state` | 1041–1085 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `RAMPS` | 1086–1126 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1127–1133 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1134–1139 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1140–1140 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1141–1141 |  |
| `moneyColKey` | 1142–1153 |  |
| `gridScale` | 1154–1174 |  |
| `scaleT` | 1175–1181 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1182–1193 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1194–1201 |  |
| `quantile` | 1202–1221 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1222–1254 |  |
| `moneyBlurb` | 1255–1259 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1260–1272 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1273–1322 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### base map (no basemap tiles for v1 — just a dark backdrop)

| symbol | lines | what it does |
|---|---|---|
| `topRings` | 1323–1339 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 1340–1365 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 1366–1366 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 1367–1379 |  |
| `svcT` | 1380–1384 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 1385–1386 |  |
| `fmtFire` | 1387–1387 |  |
| `fmtTransit` | 1388–1389 |  |
| `fmtWater` | 1390–1392 |  |
| `fmtSvcCost` | 1393–1404 |  |
| `servicePlaneLayer` | 1405–1437 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 1438–1447 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 1448–1453 |  |
| `DEV_IND_TOTAL` | 1454–1455 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 1456–1459 | Industrial is a hood-level choropleth only — no detail grid, not infill. |
| `devGridActive` | 1460–1464 | The 100 m detail grid applies to the residential metrics only: industrial |
| `devGridOfferable` | 1465–1465 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 1466–1466 |  |
| `devCol` | 1467–1467 |  |
| `_devScale` | 1468–1468 |  |
| `devScale` | 1469–1475 |  |
| `devT` | 1476–1479 |  |
| `developmentPlaneLayer` | 1480–1496 |  |
| `fmtDev` | 1497–1512 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 1513–1516 |  |
| `devGridColKey` | 1517–1519 |  |
| `devGridScale` | 1520–1532 |  |
| `devGridLayer` | 1533–1573 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 1574–1575 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 1576–1583 |  |
| `_infillStats` | 1584–1584 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 1585–1602 |  |
| `_infillRaw` | 1603–1605 |  |
| `infillScore` | 1606–1621 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 1622–1623 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 1624–1641 |  |
| `INFILL_CENTER` | 1642–1642 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 1643–1643 |  |
| `INFILL_NEG` | 1644–1644 |  |
| `infillColorAt` | 1645–1649 |  |
| `infillPlaneLayer` | 1650–1664 |  |
| `fmtFar` | 1665–1708 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 1709–1709 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 1710–1724 |  |
| `changeFor` | 1725–1745 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 1746–1746 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 1747–1761 |  |
| `chgT` | 1762–1771 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 1772–1777 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePlaneLayer` | 1778–1797 | Flat plane — EXTRUDED IS FALSE BY DECISION, not by omission. A prism |
| `FIRE_STATION_COLOR` | 1798–1798 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 1799–1819 |  |
| `ensureFireStations` | 1820–1835 |  |
| `TRANSIT_STATION_COLOR` | 1836–1836 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 1837–1854 |  |
| `ensureTransitStations` | 1855–1870 |  |
| `TRANSIT_LINE_COLOR` | 1871–1871 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 1872–1888 |  |
| `ensureLrtLines` | 1889–1935 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 1936–1936 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HENDAY_COLOR` | 1937–1940 |  |
| `referenceSplit` | 1941–1952 |  |
| `referenceUnderLayers` | 1953–1972 | Bottom of the stack: the water, under everything the map draws. |
| `referenceOverLayers` | 1973–1992 | Top of the stack: the ring road, over the data it helps locate. |
| `ensureReference` | 1993–2005 |  |
| `servicesBlurb` | 2006–2023 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 2024–2047 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 2048–2058 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 2059–2113 |  |
| `placeSize` | 2114–2118 |  |
| `PLACE_COLOR` | 2119–2119 |  |
| `HOOD_COLOR` | 2120–2122 |  |
| `placeAnchors` | 2123–2138 |  |
| `labelPool` | 2139–2146 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 2147–2200 |  |
| `CHROME_IDS` | 2201–2203 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 2204–2222 |  |
| `visibleLabels` | 2223–2273 |  |
| `labelLayer` | 2274–2310 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 2311–2311 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 2312–2327 |  |
| `ratioT` | 2328–2338 |  |
| `buildLayers` | 2339–2342 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 2343–2616 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 2617–2642 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 2643–2646 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 2647–2649 |  |
| `fmtBig` | 2650–2655 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |
| `temporalFor` | 2656–2673 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 2674–2705 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 2706–2711 |  |
| `sparklineSvg` | 2712–2727 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 2728–2768 | The pinned chart: same geometry, plus the things only a 300px box can |
| `openTemporal` | 2769–2802 |  |
| `closeTemporal` | 2803–2817 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `applyHoodMode` | 2818–2845 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 2846–2851 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 2852–2881 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 2882–2898 |  |
| `temporalClick` | 2899–2946 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 2947–3009 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 3010–3232 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 3233–3272 | The sparkline rides on EVERY view's tooltip, appended here rather than in |
| `REV_CUTS` | 3273–3273 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 3274–3286 |  |
| `syncMetricButtons` | 3287–3299 | Paint both rows from state.metric, and hide the cut row where it has |
| `applyMetric` | 3300–3319 |  |
| `applyColorAdjust` | 3320–3341 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 3342–3354 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 3355–3370 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 3371–3388 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 3389–3404 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 3405–3420 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 3421–3437 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 3438–3616 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 3617–3627 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 3628–3641 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 3642–3650 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 3651–3661 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 3662–3676 | Toggle the Uses view's residential prisms (height = share of zoned |
| `syncDevControls` | 3677–3724 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 3725–3730 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 3731–3748 |  |
| `applyMoneyDetail` | 3749–3758 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `applyMoneyMode` | 3759–3766 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 3767–3784 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 3785–3800 | Reveal the Money lens toggle and the change window picker. Called from |
| `applyDevMode` | 3801–3807 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `setPrismOpacity` | 3808–3818 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 3819–4003 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 4004–4013 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 4014–4026 |  |
| `applySvcDriver` | 4027–4412 |  |

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
