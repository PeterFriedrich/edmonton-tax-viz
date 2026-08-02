# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~4,761-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (187 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 403–407 |  |
| `HOME` | 408–408 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 409–444 |  |
| `fmtMoney` | 445–446 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `METRICS` | 447–572 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 573–589 |  |
| `RATIO_DENOMS` | 590–651 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 652–652 |  |
| `ratioOf` | 653–653 |  |
| `ratioKept` | 654–675 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 676–686 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 687–714 |  |
| `dominantUse` | 715–748 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 749–827 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 828–910 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |
| `changeBlurb` | 911–930 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 931–947 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassBlurb` | 948–952 |  |
| `usesBlurb` | 953–967 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 968–973 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 974–981 |  |
| `devChoroplethBlurb` | 982–983 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 984–1005 |  |
| `withColourClause` | 1006–1020 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `ensureGridData` | 1021–1072 |  |
| `state` | 1073–1117 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `RAMPS` | 1118–1158 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1159–1165 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1166–1171 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1172–1172 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1173–1173 |  |
| `moneyColKey` | 1174–1185 |  |
| `gridScale` | 1186–1206 |  |
| `scaleT` | 1207–1213 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1214–1225 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1226–1233 |  |
| `quantile` | 1234–1253 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1254–1286 |  |
| `moneyBlurb` | 1287–1291 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1292–1304 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1305–1354 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### base map (no basemap tiles for v1 — just a dark backdrop)

| symbol | lines | what it does |
|---|---|---|
| `topRings` | 1355–1371 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 1372–1397 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 1398–1398 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 1399–1411 |  |
| `svcT` | 1412–1416 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 1417–1418 |  |
| `fmtFire` | 1419–1419 |  |
| `fmtTransit` | 1420–1421 |  |
| `fmtWater` | 1422–1424 |  |
| `fmtSvcCost` | 1425–1436 |  |
| `servicePlaneLayer` | 1437–1469 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 1470–1479 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 1480–1485 |  |
| `DEV_IND_TOTAL` | 1486–1487 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 1488–1491 | Industrial is a hood-level choropleth only — no detail grid, not infill. |
| `devGridActive` | 1492–1496 | The 100 m detail grid applies to the residential metrics only: industrial |
| `devGridOfferable` | 1497–1497 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 1498–1498 |  |
| `devCol` | 1499–1499 |  |
| `_devScale` | 1500–1500 |  |
| `devScale` | 1501–1507 |  |
| `devT` | 1508–1511 |  |
| `developmentPlaneLayer` | 1512–1528 |  |
| `fmtDev` | 1529–1544 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 1545–1548 |  |
| `devGridColKey` | 1549–1551 |  |
| `devGridScale` | 1552–1564 |  |
| `devGridLayer` | 1565–1605 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 1606–1607 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 1608–1615 |  |
| `_infillStats` | 1616–1616 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 1617–1634 |  |
| `_infillRaw` | 1635–1637 |  |
| `infillScore` | 1638–1653 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 1654–1655 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 1656–1673 |  |
| `INFILL_CENTER` | 1674–1674 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 1675–1675 |  |
| `INFILL_NEG` | 1676–1676 |  |
| `infillColorAt` | 1677–1681 |  |
| `infillPlaneLayer` | 1682–1696 |  |
| `fmtFar` | 1697–1740 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 1741–1741 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 1742–1756 |  |
| `changeFor` | 1757–1777 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 1778–1778 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 1779–1793 |  |
| `chgT` | 1794–1803 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 1804–1809 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePlaneLayer` | 1810–1829 | Flat plane — EXTRUDED IS FALSE BY DECISION, not by omission. A prism |
| `FIRE_STATION_COLOR` | 1830–1830 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 1831–1851 |  |
| `ensureFireStations` | 1852–1867 |  |
| `TRANSIT_STATION_COLOR` | 1868–1868 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 1869–1886 |  |
| `ensureTransitStations` | 1887–1902 |  |
| `TRANSIT_LINE_COLOR` | 1903–1903 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 1904–1920 |  |
| `ensureLrtLines` | 1921–1967 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 1968–1968 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HENDAY_COLOR` | 1969–1972 |  |
| `referenceSplit` | 1973–1984 |  |
| `referenceUnderLayers` | 1985–2004 | Bottom of the stack: the water, under everything the map draws. |
| `referenceOverLayers` | 2005–2024 | Top of the stack: the ring road, over the data it helps locate. |
| `ensureReference` | 2025–2037 |  |
| `servicesBlurb` | 2038–2055 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 2056–2079 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 2080–2090 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 2091–2145 |  |
| `placeSize` | 2146–2150 |  |
| `PLACE_COLOR` | 2151–2151 |  |
| `HOOD_COLOR` | 2152–2154 |  |
| `placeAnchors` | 2155–2170 |  |
| `labelPool` | 2171–2178 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 2179–2232 |  |
| `CHROME_IDS` | 2233–2236 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 2237–2255 |  |
| `visibleLabels` | 2256–2306 |  |
| `labelLayer` | 2307–2343 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 2344–2344 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 2345–2360 |  |
| `ratioT` | 2361–2371 |  |
| `buildLayers` | 2372–2375 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 2376–2649 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 2650–2675 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 2676–2679 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 2680–2682 |  |
| `fmtBig` | 2683–2710 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 2711–2716 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 2717–2724 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 2725–2729 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 2730–2740 |  |
| `revenueLens` | 2741–2742 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 2743–2747 |  |
| `temporalFor` | 2748–2765 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 2766–2797 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 2798–2803 |  |
| `sparklineSvg` | 2804–2819 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 2820–2888 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 2889–2915 |  |
| `openTemporal` | 2916–2941 |  |
| `renderRevenueMix` | 2942–2975 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderHistory` | 2976–3001 |  |
| `syncPinnedPanel` | 3002–3016 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 3017–3034 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `applyHoodMode` | 3035–3077 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 3078–3083 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 3084–3117 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 3118–3134 |  |
| `temporalClick` | 3135–3182 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 3183–3245 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 3246–3468 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 3469–3513 | The sparkline rides on EVERY view's tooltip, appended here rather than in |
| `REV_CUTS` | 3514–3514 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 3515–3533 |  |
| `syncMetricButtons` | 3534–3557 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 3558–3564 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 3565–3585 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `syncMillRates` | 3586–3616 | Paint the pod, gate it to the money view's revenue cuts, and place it. |
| `applyMetric` | 3617–3637 |  |
| `applyColorAdjust` | 3638–3659 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 3660–3672 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 3673–3688 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 3689–3706 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 3707–3722 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 3723–3738 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 3739–3755 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 3756–3934 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 3935–3945 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 3946–3959 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 3960–3968 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 3969–3979 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 3980–3994 | Toggle the Uses view's residential prisms (height = share of zoned |
| `syncDevControls` | 3995–4042 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 4043–4048 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 4049–4066 |  |
| `applyMoneyDetail` | 4067–4076 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `applyMoneyMode` | 4077–4084 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 4085–4103 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 4104–4114 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 4115–4121 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `setPrismOpacity` | 4122–4132 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 4133–4321 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 4322–4331 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 4332–4344 |  |
| `applySvcDriver` | 4345–4761 |  |

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
| `#denom-hd` | 226 |
| `#denom` | 227 |
| `#ratio-denom-hd` | 231 |
| `#ratio-denom` | 232 |
| `#hoodmode` | 243 |
| `#hoodmode-btn` | 244 |
| `#coloradj` | 256 |
| `#coloradj-btn` | 257 |
| `#a11y` | 263 |
| `#a11y-btn` | 264 |
| `#a11y-menu` | 265 |
| `#palette` | 267 |
| `#labels-on` | 274 |
| `#reference-on` | 282 |
| `#about` | 287 |
| `#about-btn` | 288 |
| `#about-menu` | 289 |
| `#about-src-services` | 298 |
| `#about-vintage` | 317 |
| `#about-modelled` | 324 |
| `#about-updated` | 335 |
| `#botleft` | 339 |
| `#compass` | 340 |
| `#rot-ccw` | 341 |
| `#tonorth` | 348 |
| `#needle` | 350 |
| `#rot-cw` | 355 |
| `#viewbtns` | 363 |
| `#center2d` | 364 |
| `#recenter` | 365 |
| `#legend` | 367 |
| `#legend-label` | 368 |
| `#legend-min` | 370 |
| `#legend-max` | 370 |
| `#legend-cats` | 372 |
| `#revmix` | 2961 |
