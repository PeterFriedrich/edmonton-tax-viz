# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~5,957-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (233 indexed)

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
| `deviationTitle` | 1112–1117 |  |
| `deviationKind` | 1118–1120 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1121–1126 |  |
| `changeBlurb` | 1127–1146 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1147–1163 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassBlurb` | 1164–1168 |  |
| `usesBlurb` | 1169–1183 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1184–1189 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1190–1197 |  |
| `devChoroplethBlurb` | 1198–1199 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1200–1221 |  |
| `withColourClause` | 1222–1236 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `ensureGridData` | 1237–1288 |  |
| `state` | 1289–1338 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `RAMPS` | 1339–1379 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1380–1386 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1387–1392 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1393–1393 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1394–1394 |  |
| `moneyColKey` | 1395–1406 |  |
| `gridScale` | 1407–1427 |  |
| `scaleT` | 1428–1434 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1435–1446 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1447–1454 |  |
| `quantile` | 1455–1474 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1475–1507 |  |
| `moneyBlurb` | 1508–1512 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1513–1525 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1526–1575 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### base map (no basemap tiles for v1 — just a dark backdrop)

| symbol | lines | what it does |
|---|---|---|
| `topRings` | 1576–1592 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 1593–1618 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 1619–1619 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 1620–1632 |  |
| `svcT` | 1633–1637 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 1638–1639 |  |
| `fmtFire` | 1640–1640 |  |
| `fmtTransit` | 1641–1642 |  |
| `fmtBike` | 1643–1643 |  |
| `fmtWater` | 1644–1646 |  |
| `fmtSvcCost` | 1647–1651 |  |
| `fmtRoadsCost` | 1652–1653 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtTransitCost` | 1654–1655 |  |
| `fmtBikeCost` | 1656–1667 |  |
| `servicePlaneLayer` | 1668–1700 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 1701–1710 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 1711–1716 |  |
| `DEV_IND_TOTAL` | 1717–1718 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 1719–1722 | Industrial is a hood-level choropleth only — no detail grid, not infill. |
| `devGridActive` | 1723–1727 | The 100 m detail grid applies to the residential metrics only: industrial |
| `devGridOfferable` | 1728–1728 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 1729–1729 |  |
| `devCol` | 1730–1730 |  |
| `_devScale` | 1731–1731 |  |
| `devScale` | 1732–1738 |  |
| `devT` | 1739–1742 |  |
| `developmentPlaneLayer` | 1743–1759 |  |
| `fmtDev` | 1760–1775 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 1776–1779 |  |
| `devGridColKey` | 1780–1782 |  |
| `devGridScale` | 1783–1795 |  |
| `devGridLayer` | 1796–1836 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 1837–1838 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 1839–1846 |  |
| `_infillStats` | 1847–1847 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 1848–1865 |  |
| `_infillRaw` | 1866–1868 |  |
| `infillScore` | 1869–1884 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 1885–1886 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 1887–1904 |  |
| `INFILL_CENTER` | 1905–1905 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 1906–1906 |  |
| `INFILL_NEG` | 1907–1907 |  |
| `infillColorAt` | 1908–1912 |  |
| `infillPlaneLayer` | 1913–1927 |  |
| `fmtFar` | 1928–1971 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 1972–1972 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 1973–1987 |  |
| `changeFor` | 1988–2008 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2009–2009 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2010–2024 |  |
| `chgT` | 2025–2034 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2035–2048 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePlaneLayer` | 2049–2122 | Flat plane — EXTRUDED IS FALSE BY DECISION, not by omission. Hoods moved |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2123–2130 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2131–2131 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2132–2139 |  |
| `deviationRate` | 2140–2177 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2178–2178 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `instFrac` | 2179–2179 |  |
| `isUncertain` | 2180–2181 |  |
| `deviationRateExempt` | 2182–2194 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 2195–2200 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 2201–2202 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 2203–2203 |  |
| `deviationStats` | 2204–2250 |  |
| `deviationOf` | 2251–2252 |  |
| `deviationT` | 2253–2263 |  |
| `fmtDeviation` | 2264–2285 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 2286–2329 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 2330–2358 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 2359–2380 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 2381–2381 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 2382–2402 |  |
| `ensureFireStations` | 2403–2418 |  |
| `TRANSIT_STATION_COLOR` | 2419–2419 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 2420–2437 |  |
| `ensureTransitStations` | 2438–2453 |  |
| `TRANSIT_LINE_COLOR` | 2454–2454 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 2455–2471 |  |
| `ensureLrtLines` | 2472–2488 |  |
| `BIKE_LINE_COLOR` | 2489–2489 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 2490–2506 |  |
| `ensureBikeLines` | 2507–2564 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 2565–2565 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 2566–2569 |  |
| `BOUNDARY_COLOR` | 2570–2579 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 2580–2580 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 2581–2593 |  |
| `referenceSplit` | 2594–2621 |  |
| `referenceUnderLayers` | 2622–2656 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 2657–2673 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 2674–2693 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 2694–2706 |  |
| `servicesBlurb` | 2707–2724 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 2725–2748 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 2749–2759 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 2760–2811 |  |
| `REF_TIERS` | 2812–2833 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 2834–2841 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 2842–2844 |  |
| `placeAnchors` | 2845–2868 |  |
| `labelPool` | 2869–2876 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 2877–2930 |  |
| `CHROME_IDS` | 2931–2934 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 2935–2953 |  |
| `visibleLabels` | 2954–3008 |  |
| `labelLayer` | 3009–3045 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 3046–3046 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 3047–3062 |  |
| `ratioT` | 3063–3073 |  |
| `buildLayers` | 3074–3077 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 3078–3364 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 3365–3394 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 3395–3398 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 3399–3401 |  |
| `fmtBig` | 3402–3429 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 3430–3435 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 3436–3443 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 3444–3448 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 3449–3459 |  |
| `revenueLens` | 3460–3461 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 3462–3479 |  |
| `SVC_COST_BASES` | 3480–3492 | The Services panel: this hood's revenue per acre set against what the City |
| `serviceLens` | 3493–3493 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 3494–3496 |  |
| `servicePanelFor` | 3497–3510 |  |
| `hoodPanelLens` | 3511–3514 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 3515–3532 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 3533–3564 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 3565–3570 |  |
| `sparklineSvg` | 3571–3586 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 3587–3656 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 3657–3683 |  |
| `openTemporal` | 3684–3712 |  |
| `renderRevenueMix` | 3713–3761 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 3762–3795 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 3796–3798 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 3799–3849 |  |
| `syncPinnedPanel` | 3850–3876 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 3877–3892 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 3893–3903 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 3904–3951 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 3952–3957 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 3958–3997 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 3998–4014 |  |
| `temporalClick` | 4015–4072 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 4073–4152 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 4153–4461 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 4462–4509 | The sparkline rides on every OTHER view's tooltip (Services excepted |
| `REV_CUTS` | 4510–4510 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 4511–4529 |  |
| `syncMetricButtons` | 4530–4553 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 4554–4560 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 4561–4574 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 4575–4618 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |
| `syncMillRates` | 4619–4649 | Paint the pod, gate it to the money view's revenue cuts, and place it. |
| `applyMetric` | 4650–4671 |  |
| `applyColorAdjust` | 4672–4693 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 4694–4706 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 4707–4722 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 4723–4740 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 4741–4756 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 4757–4772 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 4773–4789 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 4790–5020 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 5021–5031 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 5032–5045 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 5046–5054 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 5055–5065 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 5066–5080 | Toggle the Uses view's residential prisms (height = share of zoned |
| `syncDevControls` | 5081–5128 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 5129–5134 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 5135–5152 |  |
| `applyMoneyDetail` | 5153–5162 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `applyMoneyMode` | 5163–5170 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 5171–5189 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 5190–5200 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 5201–5208 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 5209–5225 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 5226–5239 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 5240–5250 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 5251–5472 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 5473–5482 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 5483–5496 |  |
| `applySvcDriver` | 5497–5957 |  |

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
| `#revmix` | 3732 |
| `#svccost` | 3776 |
