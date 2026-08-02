# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~4,861-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (191 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 417–421 |  |
| `HOME` | 422–422 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 423–458 |  |
| `fmtMoney` | 459–460 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `METRICS` | 461–586 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 587–603 |  |
| `RATIO_DENOMS` | 604–665 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 666–666 |  |
| `ratioOf` | 667–667 |  |
| `ratioKept` | 668–689 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 690–700 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 701–728 |  |
| `dominantUse` | 729–762 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 763–858 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 859–941 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |
| `changeBlurb` | 942–961 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 962–978 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassBlurb` | 979–983 |  |
| `usesBlurb` | 984–998 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 999–1004 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1005–1012 |  |
| `devChoroplethBlurb` | 1013–1014 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1015–1036 |  |
| `withColourClause` | 1037–1051 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `ensureGridData` | 1052–1103 |  |
| `state` | 1104–1150 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `RAMPS` | 1151–1191 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1192–1198 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1199–1204 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1205–1205 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1206–1206 |  |
| `moneyColKey` | 1207–1218 |  |
| `gridScale` | 1219–1239 |  |
| `scaleT` | 1240–1246 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1247–1258 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1259–1266 |  |
| `quantile` | 1267–1286 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1287–1319 |  |
| `moneyBlurb` | 1320–1324 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1325–1337 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1338–1387 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### base map (no basemap tiles for v1 — just a dark backdrop)

| symbol | lines | what it does |
|---|---|---|
| `topRings` | 1388–1404 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 1405–1430 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 1431–1431 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 1432–1444 |  |
| `svcT` | 1445–1449 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 1450–1451 |  |
| `fmtFire` | 1452–1452 |  |
| `fmtTransit` | 1453–1454 |  |
| `fmtBike` | 1455–1455 |  |
| `fmtWater` | 1456–1458 |  |
| `fmtSvcCost` | 1459–1470 |  |
| `servicePlaneLayer` | 1471–1503 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 1504–1513 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 1514–1519 |  |
| `DEV_IND_TOTAL` | 1520–1521 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 1522–1525 | Industrial is a hood-level choropleth only — no detail grid, not infill. |
| `devGridActive` | 1526–1530 | The 100 m detail grid applies to the residential metrics only: industrial |
| `devGridOfferable` | 1531–1531 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 1532–1532 |  |
| `devCol` | 1533–1533 |  |
| `_devScale` | 1534–1534 |  |
| `devScale` | 1535–1541 |  |
| `devT` | 1542–1545 |  |
| `developmentPlaneLayer` | 1546–1562 |  |
| `fmtDev` | 1563–1578 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 1579–1582 |  |
| `devGridColKey` | 1583–1585 |  |
| `devGridScale` | 1586–1598 |  |
| `devGridLayer` | 1599–1639 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 1640–1641 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 1642–1649 |  |
| `_infillStats` | 1650–1650 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 1651–1668 |  |
| `_infillRaw` | 1669–1671 |  |
| `infillScore` | 1672–1687 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 1688–1689 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 1690–1707 |  |
| `INFILL_CENTER` | 1708–1708 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 1709–1709 |  |
| `INFILL_NEG` | 1710–1710 |  |
| `infillColorAt` | 1711–1715 |  |
| `infillPlaneLayer` | 1716–1730 |  |
| `fmtFar` | 1731–1774 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 1775–1775 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 1776–1790 |  |
| `changeFor` | 1791–1811 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 1812–1812 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 1813–1827 |  |
| `chgT` | 1828–1837 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 1838–1843 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePlaneLayer` | 1844–1863 | Flat plane — EXTRUDED IS FALSE BY DECISION, not by omission. A prism |
| `FIRE_STATION_COLOR` | 1864–1864 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 1865–1885 |  |
| `ensureFireStations` | 1886–1901 |  |
| `TRANSIT_STATION_COLOR` | 1902–1902 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 1903–1920 |  |
| `ensureTransitStations` | 1921–1936 |  |
| `TRANSIT_LINE_COLOR` | 1937–1937 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 1938–1954 |  |
| `ensureLrtLines` | 1955–1971 |  |
| `BIKE_LINE_COLOR` | 1972–1972 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 1973–1989 |  |
| `ensureBikeLines` | 1990–2036 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 2037–2037 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HENDAY_COLOR` | 2038–2041 |  |
| `referenceSplit` | 2042–2053 |  |
| `referenceUnderLayers` | 2054–2073 | Bottom of the stack: the water, under everything the map draws. |
| `referenceOverLayers` | 2074–2093 | Top of the stack: the ring road, over the data it helps locate. |
| `ensureReference` | 2094–2106 |  |
| `servicesBlurb` | 2107–2124 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 2125–2148 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 2149–2159 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 2160–2214 |  |
| `placeSize` | 2215–2219 |  |
| `PLACE_COLOR` | 2220–2220 |  |
| `HOOD_COLOR` | 2221–2223 |  |
| `placeAnchors` | 2224–2239 |  |
| `labelPool` | 2240–2247 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 2248–2301 |  |
| `CHROME_IDS` | 2302–2305 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 2306–2324 |  |
| `visibleLabels` | 2325–2375 |  |
| `labelLayer` | 2376–2412 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 2413–2413 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 2414–2429 |  |
| `ratioT` | 2430–2440 |  |
| `buildLayers` | 2441–2444 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 2445–2720 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 2721–2746 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 2747–2750 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 2751–2753 |  |
| `fmtBig` | 2754–2781 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 2782–2787 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 2788–2795 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 2796–2800 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 2801–2811 |  |
| `revenueLens` | 2812–2813 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 2814–2818 |  |
| `temporalFor` | 2819–2836 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 2837–2868 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 2869–2874 |  |
| `sparklineSvg` | 2875–2890 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 2891–2959 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 2960–2986 |  |
| `openTemporal` | 2987–3012 |  |
| `renderRevenueMix` | 3013–3046 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderHistory` | 3047–3072 |  |
| `syncPinnedPanel` | 3073–3087 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 3088–3105 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `applyHoodMode` | 3106–3148 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 3149–3154 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 3155–3188 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 3189–3205 |  |
| `temporalClick` | 3206–3253 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 3254–3317 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 3318–3540 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 3541–3585 | The sparkline rides on EVERY view's tooltip, appended here rather than in |
| `REV_CUTS` | 3586–3586 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 3587–3605 |  |
| `syncMetricButtons` | 3606–3629 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 3630–3636 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 3637–3657 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `syncMillRates` | 3658–3688 | Paint the pod, gate it to the money view's revenue cuts, and place it. |
| `applyMetric` | 3689–3709 |  |
| `applyColorAdjust` | 3710–3731 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 3732–3744 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 3745–3760 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 3761–3778 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 3779–3794 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 3795–3810 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 3811–3827 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 3828–4015 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 4016–4026 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 4027–4040 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 4041–4049 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 4050–4060 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 4061–4075 | Toggle the Uses view's residential prisms (height = share of zoned |
| `syncDevControls` | 4076–4123 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 4124–4129 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 4130–4147 |  |
| `applyMoneyDetail` | 4148–4157 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `applyMoneyMode` | 4158–4165 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 4166–4184 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 4185–4195 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 4196–4202 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `setPrismOpacity` | 4203–4213 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 4214–4403 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 4404–4413 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 4414–4427 |  |
| `applySvcDriver` | 4428–4861 |  |

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
| `#about-vintage` | 331 |
| `#about-modelled` | 338 |
| `#about-updated` | 349 |
| `#botleft` | 353 |
| `#compass` | 354 |
| `#rot-ccw` | 355 |
| `#tonorth` | 362 |
| `#needle` | 364 |
| `#rot-cw` | 369 |
| `#viewbtns` | 377 |
| `#center2d` | 378 |
| `#recenter` | 379 |
| `#legend` | 381 |
| `#legend-label` | 382 |
| `#legend-min` | 384 |
| `#legend-max` | 384 |
| `#legend-cats` | 386 |
| `#revmix` | 3032 |
