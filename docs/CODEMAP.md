# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~4,258-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (171 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 354–358 |  |
| `HOME` | 359–359 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 360–395 |  |
| `fmtMoney` | 396–397 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `METRICS` | 398–523 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 524–540 |  |
| `RATIO_DENOMS` | 541–602 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 603–603 |  |
| `ratioOf` | 604–604 |  |
| `ratioKept` | 605–626 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 627–637 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 638–665 |  |
| `dominantUse` | 666–699 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 700–778 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 779–861 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |
| `changeBlurb` | 862–881 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 882–898 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassBlurb` | 899–903 |  |
| `usesBlurb` | 904–918 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 919–924 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 925–932 |  |
| `devChoroplethBlurb` | 933–934 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 935–956 |  |
| `withColourClause` | 957–971 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `ensureGridData` | 972–1023 |  |
| `state` | 1024–1063 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `RAMPS` | 1064–1104 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1105–1111 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1112–1117 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1118–1118 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1119–1119 |  |
| `moneyColKey` | 1120–1131 |  |
| `gridScale` | 1132–1152 |  |
| `scaleT` | 1153–1159 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1160–1171 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1172–1179 |  |
| `quantile` | 1180–1199 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1200–1232 |  |
| `moneyBlurb` | 1233–1237 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1238–1250 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1251–1300 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### base map (no basemap tiles for v1 — just a dark backdrop)

| symbol | lines | what it does |
|---|---|---|
| `topRings` | 1301–1317 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 1318–1343 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 1344–1344 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 1345–1357 |  |
| `svcT` | 1358–1362 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 1363–1364 |  |
| `fmtFire` | 1365–1365 |  |
| `fmtTransit` | 1366–1367 |  |
| `fmtWater` | 1368–1370 |  |
| `fmtSvcCost` | 1371–1382 |  |
| `servicePlaneLayer` | 1383–1415 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 1416–1425 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 1426–1431 |  |
| `DEV_IND_TOTAL` | 1432–1433 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 1434–1437 | Industrial is a hood-level choropleth only — no detail grid, not infill. |
| `devGridActive` | 1438–1442 | The 100 m detail grid applies to the residential metrics only: industrial |
| `devGridOfferable` | 1443–1443 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 1444–1444 |  |
| `devCol` | 1445–1445 |  |
| `_devScale` | 1446–1446 |  |
| `devScale` | 1447–1453 |  |
| `devT` | 1454–1457 |  |
| `developmentPlaneLayer` | 1458–1474 |  |
| `fmtDev` | 1475–1490 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 1491–1494 |  |
| `devGridColKey` | 1495–1497 |  |
| `devGridScale` | 1498–1510 |  |
| `devGridLayer` | 1511–1551 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 1552–1553 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 1554–1561 |  |
| `_infillStats` | 1562–1562 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 1563–1580 |  |
| `_infillRaw` | 1581–1583 |  |
| `infillScore` | 1584–1599 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 1600–1601 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 1602–1619 |  |
| `INFILL_CENTER` | 1620–1620 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 1621–1621 |  |
| `INFILL_NEG` | 1622–1622 |  |
| `infillColorAt` | 1623–1627 |  |
| `infillPlaneLayer` | 1628–1642 |  |
| `fmtFar` | 1643–1686 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 1687–1687 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 1688–1702 |  |
| `changeFor` | 1703–1723 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 1724–1724 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 1725–1739 |  |
| `chgT` | 1740–1749 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 1750–1755 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePlaneLayer` | 1756–1775 | Flat plane — EXTRUDED IS FALSE BY DECISION, not by omission. A prism |
| `FIRE_STATION_COLOR` | 1776–1776 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 1777–1797 |  |
| `ensureFireStations` | 1798–1813 |  |
| `TRANSIT_STATION_COLOR` | 1814–1814 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 1815–1832 |  |
| `ensureTransitStations` | 1833–1848 |  |
| `TRANSIT_LINE_COLOR` | 1849–1849 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 1850–1866 |  |
| `ensureLrtLines` | 1867–1913 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 1914–1914 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HENDAY_COLOR` | 1915–1918 |  |
| `referenceSplit` | 1919–1930 |  |
| `referenceUnderLayers` | 1931–1950 | Bottom of the stack: the water, under everything the map draws. |
| `referenceOverLayers` | 1951–1970 | Top of the stack: the ring road, over the data it helps locate. |
| `ensureReference` | 1971–1983 |  |
| `servicesBlurb` | 1984–2001 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 2002–2025 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 2026–2036 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 2037–2091 |  |
| `placeSize` | 2092–2096 |  |
| `PLACE_COLOR` | 2097–2097 |  |
| `HOOD_COLOR` | 2098–2100 |  |
| `placeAnchors` | 2101–2116 |  |
| `labelPool` | 2117–2124 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 2125–2178 |  |
| `CHROME_IDS` | 2179–2181 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 2182–2200 |  |
| `visibleLabels` | 2201–2251 |  |
| `labelLayer` | 2252–2288 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 2289–2289 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 2290–2305 |  |
| `ratioT` | 2306–2316 |  |
| `buildLayers` | 2317–2320 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 2321–2594 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 2595–2620 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 2621–2624 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 2625–2627 |  |
| `fmtBig` | 2628–2633 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |
| `temporalFor` | 2634–2651 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 2652–2683 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 2684–2689 |  |
| `sparklineSvg` | 2690–2705 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 2706–2746 | The pinned chart: same geometry, plus the things only a 300px box can |
| `openTemporal` | 2747–2780 |  |
| `closeTemporal` | 2781–2792 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `applyHoodMode` | 2793–2820 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `temporalClick` | 2821–2837 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 2838–2895 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 2896–3101 | Tooltip content is per-view (closure over `state`). money: active |
| `tooltipFor` | 3102–3129 | The sparkline rides on EVERY view's tooltip, appended here rather than in |
| `REV_CUTS` | 3130–3130 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 3131–3143 |  |
| `syncMetricButtons` | 3144–3156 | Paint both rows from state.metric, and hide the cut row where it has |
| `applyMetric` | 3157–3176 |  |
| `applyColorAdjust` | 3177–3198 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 3199–3211 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 3212–3227 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 3228–3245 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 3246–3261 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 3262–3277 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 3278–3294 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 3295–3473 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 3474–3484 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 3485–3498 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 3499–3507 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 3508–3518 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 3519–3533 | Toggle the Uses view's residential prisms (height = share of zoned |
| `syncDevControls` | 3534–3581 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 3582–3587 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 3588–3605 |  |
| `applyMoneyDetail` | 3606–3615 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `applyMoneyMode` | 3616–3623 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 3624–3641 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 3642–3657 | Reveal the Money lens toggle and the change window picker. Called from |
| `applyDevMode` | 3658–3664 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `setPrismOpacity` | 3665–3675 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 3676–3860 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 3861–3870 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 3871–3883 |  |
| `applySvcDriver` | 3884–4258 |  |

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
| `#hoodmode` | 194 |
| `#hoodmode-btn` | 195 |
| `#coloradj` | 207 |
| `#coloradj-btn` | 208 |
| `#a11y` | 214 |
| `#a11y-btn` | 215 |
| `#a11y-menu` | 216 |
| `#palette` | 218 |
| `#labels-on` | 225 |
| `#reference-on` | 233 |
| `#about` | 238 |
| `#about-btn` | 239 |
| `#about-menu` | 240 |
| `#about-src-services` | 249 |
| `#about-vintage` | 268 |
| `#about-modelled` | 275 |
| `#about-updated` | 286 |
| `#botleft` | 290 |
| `#compass` | 291 |
| `#rot-ccw` | 292 |
| `#tonorth` | 299 |
| `#needle` | 301 |
| `#rot-cw` | 306 |
| `#viewbtns` | 314 |
| `#center2d` | 315 |
| `#recenter` | 316 |
| `#legend` | 318 |
| `#legend-label` | 319 |
| `#legend-min` | 321 |
| `#legend-max` | 321 |
| `#legend-cats` | 323 |
