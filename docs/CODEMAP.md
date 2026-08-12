# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~5,910-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

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
| `deviationRate` | 2140–2168 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2169–2169 |  |
| `instFrac` | 2170–2170 |  |
| `isUncertain` | 2171–2172 |  |
| `deviationRateExempt` | 2173–2185 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 2186–2191 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 2192–2193 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 2194–2194 |  |
| `deviationStats` | 2195–2241 |  |
| `deviationOf` | 2242–2243 |  |
| `deviationT` | 2244–2254 |  |
| `fmtDeviation` | 2255–2276 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 2277–2316 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 2317–2345 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 2346–2367 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 2368–2368 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 2369–2389 |  |
| `ensureFireStations` | 2390–2405 |  |
| `TRANSIT_STATION_COLOR` | 2406–2406 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 2407–2424 |  |
| `ensureTransitStations` | 2425–2440 |  |
| `TRANSIT_LINE_COLOR` | 2441–2441 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 2442–2458 |  |
| `ensureLrtLines` | 2459–2475 |  |
| `BIKE_LINE_COLOR` | 2476–2476 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 2477–2493 |  |
| `ensureBikeLines` | 2494–2551 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 2552–2552 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 2553–2556 |  |
| `BOUNDARY_COLOR` | 2557–2566 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 2567–2567 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 2568–2580 |  |
| `referenceSplit` | 2581–2608 |  |
| `referenceUnderLayers` | 2609–2643 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 2644–2660 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 2661–2680 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 2681–2693 |  |
| `servicesBlurb` | 2694–2711 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 2712–2735 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 2736–2746 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 2747–2798 |  |
| `REF_TIERS` | 2799–2820 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 2821–2828 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 2829–2831 |  |
| `placeAnchors` | 2832–2855 |  |
| `labelPool` | 2856–2863 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 2864–2917 |  |
| `CHROME_IDS` | 2918–2921 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 2922–2940 |  |
| `visibleLabels` | 2941–2995 |  |
| `labelLayer` | 2996–3032 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 3033–3033 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 3034–3049 |  |
| `ratioT` | 3050–3060 |  |
| `buildLayers` | 3061–3064 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 3065–3351 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 3352–3381 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 3382–3385 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 3386–3388 |  |
| `fmtBig` | 3389–3416 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 3417–3422 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 3423–3430 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 3431–3435 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 3436–3446 |  |
| `revenueLens` | 3447–3448 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 3449–3466 |  |
| `SVC_COST_BASES` | 3467–3479 | The Services panel: this hood's revenue per acre set against what the City |
| `serviceLens` | 3480–3480 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 3481–3483 |  |
| `servicePanelFor` | 3484–3497 |  |
| `hoodPanelLens` | 3498–3501 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 3502–3519 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 3520–3551 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 3552–3557 |  |
| `sparklineSvg` | 3558–3573 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 3574–3643 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 3644–3670 |  |
| `openTemporal` | 3671–3699 |  |
| `renderRevenueMix` | 3700–3748 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 3749–3782 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 3783–3785 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 3786–3836 |  |
| `syncPinnedPanel` | 3837–3863 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 3864–3879 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 3880–3890 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 3891–3938 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 3939–3944 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 3945–3984 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 3985–4001 |  |
| `temporalClick` | 4002–4059 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 4060–4136 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 4137–4414 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 4415–4462 | The sparkline rides on every OTHER view's tooltip (Services excepted |
| `REV_CUTS` | 4463–4463 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 4464–4482 |  |
| `syncMetricButtons` | 4483–4506 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 4507–4513 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 4514–4527 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 4528–4571 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |
| `syncMillRates` | 4572–4602 | Paint the pod, gate it to the money view's revenue cuts, and place it. |
| `applyMetric` | 4603–4624 |  |
| `applyColorAdjust` | 4625–4646 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 4647–4659 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 4660–4675 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 4676–4693 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 4694–4709 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 4710–4725 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 4726–4742 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 4743–4973 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 4974–4984 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 4985–4998 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 4999–5007 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 5008–5018 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 5019–5033 | Toggle the Uses view's residential prisms (height = share of zoned |
| `syncDevControls` | 5034–5081 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 5082–5087 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 5088–5105 |  |
| `applyMoneyDetail` | 5106–5115 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `applyMoneyMode` | 5116–5123 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 5124–5142 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 5143–5153 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 5154–5161 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 5162–5178 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 5179–5192 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 5193–5203 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 5204–5425 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 5426–5435 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 5436–5449 |  |
| `applySvcDriver` | 5450–5910 |  |

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
| `#revmix` | 3719 |
| `#svccost` | 3763 |
