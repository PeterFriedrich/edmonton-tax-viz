# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~4,252-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (171 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 348–352 |  |
| `HOME` | 353–353 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 354–389 |  |
| `fmtMoney` | 390–391 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `METRICS` | 392–517 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 518–534 |  |
| `RATIO_DENOMS` | 535–596 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 597–597 |  |
| `ratioOf` | 598–598 |  |
| `ratioKept` | 599–620 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 621–631 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 632–659 |  |
| `dominantUse` | 660–693 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 694–772 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 773–855 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |
| `changeBlurb` | 856–875 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 876–892 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassBlurb` | 893–897 |  |
| `usesBlurb` | 898–912 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 913–918 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 919–926 |  |
| `devChoroplethBlurb` | 927–928 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 929–950 |  |
| `withColourClause` | 951–965 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `ensureGridData` | 966–1017 |  |
| `state` | 1018–1057 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `RAMPS` | 1058–1098 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1099–1105 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1106–1111 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1112–1112 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1113–1113 |  |
| `moneyColKey` | 1114–1125 |  |
| `gridScale` | 1126–1146 |  |
| `scaleT` | 1147–1153 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1154–1165 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1166–1173 |  |
| `quantile` | 1174–1193 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1194–1226 |  |
| `moneyBlurb` | 1227–1231 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1232–1244 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1245–1294 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### base map (no basemap tiles for v1 — just a dark backdrop)

| symbol | lines | what it does |
|---|---|---|
| `topRings` | 1295–1311 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 1312–1337 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 1338–1338 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 1339–1351 |  |
| `svcT` | 1352–1356 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 1357–1358 |  |
| `fmtFire` | 1359–1359 |  |
| `fmtTransit` | 1360–1361 |  |
| `fmtWater` | 1362–1364 |  |
| `fmtSvcCost` | 1365–1376 |  |
| `servicePlaneLayer` | 1377–1409 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 1410–1419 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 1420–1425 |  |
| `DEV_IND_TOTAL` | 1426–1427 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 1428–1431 | Industrial is a hood-level choropleth only — no detail grid, not infill. |
| `devGridActive` | 1432–1436 | The 100 m detail grid applies to the residential metrics only: industrial |
| `devGridOfferable` | 1437–1437 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 1438–1438 |  |
| `devCol` | 1439–1439 |  |
| `_devScale` | 1440–1440 |  |
| `devScale` | 1441–1447 |  |
| `devT` | 1448–1451 |  |
| `developmentPlaneLayer` | 1452–1468 |  |
| `fmtDev` | 1469–1484 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 1485–1488 |  |
| `devGridColKey` | 1489–1491 |  |
| `devGridScale` | 1492–1504 |  |
| `devGridLayer` | 1505–1545 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 1546–1547 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 1548–1555 |  |
| `_infillStats` | 1556–1556 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 1557–1574 |  |
| `_infillRaw` | 1575–1577 |  |
| `infillScore` | 1578–1593 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 1594–1595 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 1596–1613 |  |
| `INFILL_CENTER` | 1614–1614 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 1615–1615 |  |
| `INFILL_NEG` | 1616–1616 |  |
| `infillColorAt` | 1617–1621 |  |
| `infillPlaneLayer` | 1622–1636 |  |
| `fmtFar` | 1637–1680 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 1681–1681 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 1682–1696 |  |
| `changeFor` | 1697–1717 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 1718–1718 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 1719–1733 |  |
| `chgT` | 1734–1743 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 1744–1749 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePlaneLayer` | 1750–1769 | Flat plane — EXTRUDED IS FALSE BY DECISION, not by omission. A prism |
| `FIRE_STATION_COLOR` | 1770–1770 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 1771–1791 |  |
| `ensureFireStations` | 1792–1807 |  |
| `TRANSIT_STATION_COLOR` | 1808–1808 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 1809–1826 |  |
| `ensureTransitStations` | 1827–1842 |  |
| `TRANSIT_LINE_COLOR` | 1843–1843 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 1844–1860 |  |
| `ensureLrtLines` | 1861–1907 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 1908–1908 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HENDAY_COLOR` | 1909–1912 |  |
| `referenceSplit` | 1913–1924 |  |
| `referenceUnderLayers` | 1925–1944 | Bottom of the stack: the water, under everything the map draws. |
| `referenceOverLayers` | 1945–1964 | Top of the stack: the ring road, over the data it helps locate. |
| `ensureReference` | 1965–1977 |  |
| `servicesBlurb` | 1978–1995 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 1996–2019 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 2020–2030 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 2031–2085 |  |
| `placeSize` | 2086–2090 |  |
| `PLACE_COLOR` | 2091–2091 |  |
| `HOOD_COLOR` | 2092–2094 |  |
| `placeAnchors` | 2095–2110 |  |
| `labelPool` | 2111–2118 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 2119–2172 |  |
| `CHROME_IDS` | 2173–2175 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 2176–2194 |  |
| `visibleLabels` | 2195–2245 |  |
| `labelLayer` | 2246–2282 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 2283–2283 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 2284–2299 |  |
| `ratioT` | 2300–2310 |  |
| `buildLayers` | 2311–2314 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 2315–2588 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 2589–2614 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 2615–2618 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 2619–2621 |  |
| `fmtBig` | 2622–2627 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |
| `temporalFor` | 2628–2645 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 2646–2677 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 2678–2683 |  |
| `sparklineSvg` | 2684–2699 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 2700–2740 | The pinned chart: same geometry, plus the things only a 300px box can |
| `openTemporal` | 2741–2774 |  |
| `closeTemporal` | 2775–2786 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `applyHoodMode` | 2787–2814 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `temporalClick` | 2815–2831 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 2832–2889 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 2890–3095 | Tooltip content is per-view (closure over `state`). money: active |
| `tooltipFor` | 3096–3123 | The sparkline rides on EVERY view's tooltip, appended here rather than in |
| `REV_CUTS` | 3124–3124 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 3125–3137 |  |
| `syncMetricButtons` | 3138–3150 | Paint both rows from state.metric, and hide the cut row where it has |
| `applyMetric` | 3151–3170 |  |
| `applyColorAdjust` | 3171–3192 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 3193–3205 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 3206–3221 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 3222–3239 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 3240–3255 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 3256–3271 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 3272–3288 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 3289–3467 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 3468–3478 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 3479–3492 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 3493–3501 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 3502–3512 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 3513–3527 | Toggle the Uses view's residential prisms (height = share of zoned |
| `syncDevControls` | 3528–3575 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 3576–3581 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 3582–3599 |  |
| `applyMoneyDetail` | 3600–3609 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `applyMoneyMode` | 3610–3617 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 3618–3635 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 3636–3651 | Reveal the Money lens toggle and the change window picker. Called from |
| `applyDevMode` | 3652–3658 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `setPrismOpacity` | 3659–3669 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 3670–3854 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 3855–3864 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 3865–3877 |  |
| `applySvcDriver` | 3878–4252 |  |

## Element ids (80) — the control surface

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
| `#controls` | 47 |
| `#toggle` | 53 |
| `#metric-row` | 54 |
| `#revcut` | 58 |
| `#views` | 65 |
| `#optpanel` | 73 |
| `#opt-fold` | 74 |
| `#opt-caret` | 74 |
| `#opt-body` | 75 |
| `#layers` | 76 |
| `#moneymode-hd` | 77 |
| `#moneymode` | 78 |
| `#chgwindow-hd` | 82 |
| `#chgwindow` | 83 |
| `#moneydetail-hd` | 87 |
| `#moneydetail` | 88 |
| `#uses-prisms-hd` | 92 |
| `#uses-prisms` | 93 |
| `#uses-prisms-on` | 95 |
| `#devmode-hd` | 98 |
| `#devmode` | 99 |
| `#devmetric-hd` | 103 |
| `#devmetric` | 104 |
| `#devwindow-hd` | 109 |
| `#devwindow` | 110 |
| `#devdetail-hd` | 115 |
| `#devdetail` | 116 |
| `#prism-hd` | 120 |
| `#prism-row` | 121 |
| `#prism-opacity` | 123 |
| `#prism-opacity-val` | 124 |
| `#services-hd` | 126 |
| `#services` | 127 |
| `#denom-hd` | 177 |
| `#denom` | 178 |
| `#ratio-denom-hd` | 182 |
| `#ratio-denom` | 183 |
| `#coloradj` | 193 |
| `#coloradj-btn` | 194 |
| `#hoodmode` | 201 |
| `#hoodmode-btn` | 202 |
| `#a11y` | 208 |
| `#a11y-btn` | 209 |
| `#a11y-menu` | 210 |
| `#palette` | 212 |
| `#labels-on` | 219 |
| `#reference-on` | 227 |
| `#about` | 232 |
| `#about-btn` | 233 |
| `#about-menu` | 234 |
| `#about-src-services` | 243 |
| `#about-vintage` | 262 |
| `#about-modelled` | 269 |
| `#about-updated` | 280 |
| `#botleft` | 284 |
| `#compass` | 285 |
| `#rot-ccw` | 286 |
| `#tonorth` | 293 |
| `#needle` | 295 |
| `#rot-cw` | 300 |
| `#viewbtns` | 308 |
| `#center2d` | 309 |
| `#recenter` | 310 |
| `#legend` | 312 |
| `#legend-label` | 313 |
| `#legend-min` | 315 |
| `#legend-max` | 315 |
| `#legend-cats` | 317 |
