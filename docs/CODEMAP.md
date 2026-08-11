# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~5,694-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (220 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 489–493 |  |
| `HOME` | 494–494 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 495–535 |  |
| `fmtMoney` | 536–537 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `METRICS` | 538–663 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 664–680 |  |
| `RATIO_DENOMS` | 681–742 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 743–743 |  |
| `ratioOf` | 744–744 |  |
| `ratioKept` | 745–766 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 767–777 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 778–805 |  |
| `dominantUse` | 806–839 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 840–994 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 995–1099 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1100–1104 | the Lab: a container for unfinished lenses |
| `inLab` | 1105–1106 |  |
| `DEVIATION_TITLES` | 1107–1111 |  |
| `deviationTitle` | 1112–1116 |  |
| `changeBlurb` | 1117–1136 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1137–1153 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassBlurb` | 1154–1158 |  |
| `usesBlurb` | 1159–1173 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1174–1179 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1180–1187 |  |
| `devChoroplethBlurb` | 1188–1189 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1190–1211 |  |
| `withColourClause` | 1212–1226 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `ensureGridData` | 1227–1278 |  |
| `state` | 1279–1328 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `RAMPS` | 1329–1369 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1370–1376 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1377–1382 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1383–1383 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1384–1384 |  |
| `moneyColKey` | 1385–1396 |  |
| `gridScale` | 1397–1417 |  |
| `scaleT` | 1418–1424 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1425–1436 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1437–1444 |  |
| `quantile` | 1445–1464 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1465–1497 |  |
| `moneyBlurb` | 1498–1502 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1503–1515 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1516–1565 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### base map (no basemap tiles for v1 — just a dark backdrop)

| symbol | lines | what it does |
|---|---|---|
| `topRings` | 1566–1582 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 1583–1608 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 1609–1609 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 1610–1622 |  |
| `svcT` | 1623–1627 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 1628–1629 |  |
| `fmtFire` | 1630–1630 |  |
| `fmtTransit` | 1631–1632 |  |
| `fmtBike` | 1633–1633 |  |
| `fmtWater` | 1634–1636 |  |
| `fmtSvcCost` | 1637–1641 |  |
| `fmtRoadsCost` | 1642–1643 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtTransitCost` | 1644–1645 |  |
| `fmtBikeCost` | 1646–1657 |  |
| `servicePlaneLayer` | 1658–1690 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 1691–1700 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 1701–1706 |  |
| `DEV_IND_TOTAL` | 1707–1708 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 1709–1712 | Industrial is a hood-level choropleth only — no detail grid, not infill. |
| `devGridActive` | 1713–1717 | The 100 m detail grid applies to the residential metrics only: industrial |
| `devGridOfferable` | 1718–1718 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 1719–1719 |  |
| `devCol` | 1720–1720 |  |
| `_devScale` | 1721–1721 |  |
| `devScale` | 1722–1728 |  |
| `devT` | 1729–1732 |  |
| `developmentPlaneLayer` | 1733–1749 |  |
| `fmtDev` | 1750–1765 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 1766–1769 |  |
| `devGridColKey` | 1770–1772 |  |
| `devGridScale` | 1773–1785 |  |
| `devGridLayer` | 1786–1826 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 1827–1828 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 1829–1836 |  |
| `_infillStats` | 1837–1837 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 1838–1855 |  |
| `_infillRaw` | 1856–1858 |  |
| `infillScore` | 1859–1874 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 1875–1876 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 1877–1894 |  |
| `INFILL_CENTER` | 1895–1895 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 1896–1896 |  |
| `INFILL_NEG` | 1897–1897 |  |
| `infillColorAt` | 1898–1902 |  |
| `infillPlaneLayer` | 1903–1917 |  |
| `fmtFar` | 1918–1961 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 1962–1962 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 1963–1977 |  |
| `changeFor` | 1978–1998 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 1999–1999 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2000–2014 |  |
| `chgT` | 2015–2024 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2025–2038 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePlaneLayer` | 2039–2077 | Flat plane — EXTRUDED IS FALSE BY DECISION, not by omission. Hoods moved |

### deviation lens: revenue per acre against the citywide average

| symbol | lines | what it does |
|---|---|---|
| `_devStats` | 2078–2078 | deviation lens: revenue per acre against the citywide average |
| `deviationStats` | 2079–2111 |  |
| `deviationOf` | 2112–2113 |  |
| `deviationT` | 2114–2124 |  |
| `fmtDeviation` | 2125–2140 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 2141–2172 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBlurb` | 2173–2189 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 2190–2190 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 2191–2211 |  |
| `ensureFireStations` | 2212–2227 |  |
| `TRANSIT_STATION_COLOR` | 2228–2228 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 2229–2246 |  |
| `ensureTransitStations` | 2247–2262 |  |
| `TRANSIT_LINE_COLOR` | 2263–2263 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 2264–2280 |  |
| `ensureLrtLines` | 2281–2297 |  |
| `BIKE_LINE_COLOR` | 2298–2298 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 2299–2315 |  |
| `ensureBikeLines` | 2316–2373 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 2374–2374 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 2375–2378 |  |
| `BOUNDARY_COLOR` | 2379–2388 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 2389–2389 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 2390–2402 |  |
| `referenceSplit` | 2403–2430 |  |
| `referenceUnderLayers` | 2431–2465 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 2466–2482 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 2483–2502 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 2503–2515 |  |
| `servicesBlurb` | 2516–2533 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 2534–2557 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 2558–2568 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 2569–2620 |  |
| `REF_TIERS` | 2621–2642 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 2643–2650 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 2651–2653 |  |
| `placeAnchors` | 2654–2677 |  |
| `labelPool` | 2678–2685 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 2686–2739 |  |
| `CHROME_IDS` | 2740–2743 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 2744–2762 |  |
| `visibleLabels` | 2763–2817 |  |
| `labelLayer` | 2818–2854 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 2855–2855 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 2856–2871 |  |
| `ratioT` | 2872–2882 |  |
| `buildLayers` | 2883–2886 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 2887–3171 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 3172–3201 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 3202–3205 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 3206–3208 |  |
| `fmtBig` | 3209–3236 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 3237–3242 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 3243–3250 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 3251–3255 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 3256–3266 |  |
| `revenueLens` | 3267–3268 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 3269–3286 |  |
| `SVC_COST_BASES` | 3287–3299 | The Services panel: this hood's revenue per acre set against what the City |
| `serviceLens` | 3300–3300 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 3301–3303 |  |
| `servicePanelFor` | 3304–3317 |  |
| `hoodPanelLens` | 3318–3321 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 3322–3339 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 3340–3371 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 3372–3377 |  |
| `sparklineSvg` | 3378–3393 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 3394–3463 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 3464–3490 |  |
| `openTemporal` | 3491–3519 |  |
| `renderRevenueMix` | 3520–3568 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 3569–3602 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 3603–3605 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 3606–3656 |  |
| `syncPinnedPanel` | 3657–3683 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 3684–3699 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 3700–3710 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 3711–3758 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 3759–3764 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 3765–3804 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 3805–3821 |  |
| `temporalClick` | 3822–3879 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 3880–3952 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 3953–4205 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 4206–4253 | The sparkline rides on every OTHER view's tooltip (Services excepted |
| `REV_CUTS` | 4254–4254 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 4255–4273 |  |
| `syncMetricButtons` | 4274–4297 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 4298–4304 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 4305–4318 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 4319–4362 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |
| `syncMillRates` | 4363–4393 | Paint the pod, gate it to the money view's revenue cuts, and place it. |
| `applyMetric` | 4394–4415 |  |
| `applyColorAdjust` | 4416–4437 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 4438–4450 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 4451–4466 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 4467–4484 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 4485–4500 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 4501–4516 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 4517–4533 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 4534–4757 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 4758–4768 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 4769–4782 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 4783–4791 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 4792–4802 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 4803–4817 | Toggle the Uses view's residential prisms (height = share of zoned |
| `syncDevControls` | 4818–4865 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 4866–4871 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 4872–4889 |  |
| `applyMoneyDetail` | 4890–4899 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `applyMoneyMode` | 4900–4907 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 4908–4926 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 4927–4937 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 4938–4945 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 4946–4962 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 4963–4976 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 4977–4987 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 4988–5209 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 5210–5219 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 5220–5233 |  |
| `applySvcDriver` | 5234–5694 |  |

## Element ids (98) — the control surface

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
| `#optpanel` | 133 |
| `#opt-fold` | 134 |
| `#opt-caret` | 134 |
| `#opt-body` | 135 |
| `#layers` | 136 |
| `#chgwindow-hd` | 137 |
| `#chgwindow` | 138 |
| `#labpick-hd` | 147 |
| `#labpick` | 148 |
| `#labcut-hd` | 149 |
| `#labcut` | 150 |
| `#moneydetail-hd` | 155 |
| `#moneydetail` | 156 |
| `#uses-prisms-hd` | 160 |
| `#uses-prisms` | 161 |
| `#uses-prisms-on` | 163 |
| `#devmode-hd` | 166 |
| `#devmode` | 167 |
| `#devmetric-hd` | 171 |
| `#devmetric` | 172 |
| `#devwindow-hd` | 177 |
| `#devwindow` | 178 |
| `#devdetail-hd` | 183 |
| `#devdetail` | 184 |
| `#prism-hd` | 188 |
| `#prism-row` | 189 |
| `#prism-opacity` | 191 |
| `#prism-opacity-val` | 192 |
| `#services-hd` | 194 |
| `#services` | 195 |
| `#denom-hd` | 289 |
| `#denom` | 290 |
| `#ratio-denom-hd` | 294 |
| `#ratio-denom` | 295 |
| `#hoodmode` | 306 |
| `#hoodmode-btn` | 307 |
| `#coloradj` | 319 |
| `#coloradj-btn` | 320 |
| `#a11y` | 326 |
| `#a11y-btn` | 327 |
| `#a11y-menu` | 328 |
| `#palette` | 330 |
| `#labels-on` | 337 |
| `#reference-on` | 345 |
| `#about` | 350 |
| `#about-btn` | 351 |
| `#about-menu` | 352 |
| `#about-src-services` | 361 |
| `#about-vintage` | 389 |
| `#about-modelled` | 396 |
| `#about-budget` | 406 |
| `#about-budget-lead` | 408 |
| `#about-budget-rows` | 409 |
| `#about-budget-note` | 410 |
| `#about-updated` | 421 |
| `#botleft` | 425 |
| `#compass` | 426 |
| `#rot-ccw` | 427 |
| `#tonorth` | 434 |
| `#needle` | 436 |
| `#rot-cw` | 441 |
| `#viewbtns` | 449 |
| `#center2d` | 450 |
| `#recenter` | 451 |
| `#legend` | 453 |
| `#legend-label` | 454 |
| `#legend-min` | 456 |
| `#legend-max` | 456 |
| `#legend-cats` | 458 |
| `#revmix` | 3539 |
| `#svccost` | 3583 |
