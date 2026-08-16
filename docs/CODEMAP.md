# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~6,255-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (243 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 527–531 |  |
| `HOME` | 532–532 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 533–576 |  |
| `fmtMoney` | 577–578 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `METRICS` | 579–704 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 705–721 |  |
| `RATIO_DENOMS` | 722–783 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 784–784 |  |
| `ratioOf` | 785–785 |  |
| `ratioKept` | 786–807 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 808–818 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 819–846 |  |
| `dominantUse` | 847–880 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 881–1035 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1036–1140 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1141–1145 | the Lab: a container for unfinished lenses |
| `inLab` | 1146–1147 |  |
| `DEVIATION_TITLES` | 1148–1152 |  |
| `deviationTitle` | 1153–1158 |  |
| `deviationKind` | 1159–1161 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1162–1167 |  |
| `changeBlurb` | 1168–1187 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1188–1204 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassBlurb` | 1205–1209 |  |
| `usesBlurb` | 1210–1224 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1225–1230 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1231–1238 |  |
| `devChoroplethBlurb` | 1239–1240 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1241–1262 |  |
| `withColourClause` | 1263–1277 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `ensureGridData` | 1278–1325 |  |
| `state` | 1326–1375 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `RAMPS` | 1376–1416 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1417–1423 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1424–1429 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1430–1430 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1431–1431 |  |
| `moneyColKey` | 1432–1443 |  |
| `gridScale` | 1444–1464 |  |
| `scaleT` | 1465–1471 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1472–1483 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1484–1486 |  |
| `quantile` | 1487–1501 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1502–1534 |  |
| `moneyBlurb` | 1535–1539 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1540–1552 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1553–1602 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### base map (no basemap tiles for v1 — just a dark backdrop)

| symbol | lines | what it does |
|---|---|---|
| `topRings` | 1603–1619 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 1620–1645 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 1646–1646 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 1647–1659 |  |
| `svcT` | 1660–1664 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 1665–1666 |  |
| `fmtFire` | 1667–1667 |  |
| `fmtTransit` | 1668–1669 |  |
| `fmtBike` | 1670–1670 |  |
| `fmtWater` | 1671–1673 |  |
| `fmtSvcCost` | 1674–1678 |  |
| `fmtRoadsCost` | 1679–1680 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtTransitCost` | 1681–1682 |  |
| `fmtBikeCost` | 1683–1694 |  |
| `servicePlaneLayer` | 1695–1727 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 1728–1737 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 1738–1743 |  |
| `DEV_IND_TOTAL` | 1744–1745 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 1746–1749 | Industrial is a hood-level choropleth only — no detail grid, not infill. |
| `devGridActive` | 1750–1754 | The 100 m detail grid applies to the residential metrics only: industrial |
| `devGridOfferable` | 1755–1755 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 1756–1756 |  |
| `devCol` | 1757–1757 |  |
| `_devScale` | 1758–1758 |  |
| `devScale` | 1759–1765 |  |
| `devT` | 1766–1769 |  |
| `developmentPlaneLayer` | 1770–1786 |  |
| `fmtDev` | 1787–1802 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 1803–1806 |  |
| `devGridColKey` | 1807–1809 |  |
| `devGridScale` | 1810–1822 |  |
| `devGridLayer` | 1823–1863 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 1864–1865 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 1866–1873 |  |
| `_infillStats` | 1874–1874 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 1875–1892 |  |
| `_infillRaw` | 1893–1895 |  |
| `infillScore` | 1896–1911 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 1912–1913 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 1914–1931 |  |
| `INFILL_CENTER` | 1932–1932 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 1933–1933 |  |
| `INFILL_NEG` | 1934–1934 |  |
| `infillColorAt` | 1935–1939 |  |
| `infillPlaneLayer` | 1940–1954 |  |
| `fmtFar` | 1955–1998 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 1999–1999 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2000–2014 |  |
| `changeFor` | 2015–2035 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2036–2036 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2037–2051 |  |
| `chgT` | 2052–2061 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2062–2075 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePlaneLayer` | 2076–2149 | Flat plane — EXTRUDED IS FALSE BY DECISION, not by omission. Hoods moved |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2150–2157 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2158–2158 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2159–2166 |  |
| `deviationRate` | 2167–2204 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2205–2205 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `instFrac` | 2206–2235 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 2236–2242 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 2243–2254 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 2255–2258 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 2259–2263 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 2264–2274 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 2275–2290 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 2291–2317 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `INST_OUTLINE_COLOR` | 2318–2348 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `instBandLayers` | 2349–2375 |  |
| `deviationRateExempt` | 2376–2388 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 2389–2390 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 2391–2392 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 2393–2393 |  |
| `deviationStats` | 2394–2438 |  |
| `deviationOf` | 2439–2440 |  |
| `deviationT` | 2441–2451 |  |
| `fmtDeviation` | 2452–2473 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 2474–2517 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 2518–2546 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 2547–2569 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 2570–2570 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 2571–2591 |  |
| `ensureFireStations` | 2592–2607 |  |
| `TRANSIT_STATION_COLOR` | 2608–2608 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 2609–2626 |  |
| `ensureTransitStations` | 2627–2642 |  |
| `TRANSIT_LINE_COLOR` | 2643–2643 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 2644–2660 |  |
| `ensureLrtLines` | 2661–2677 |  |
| `BIKE_LINE_COLOR` | 2678–2678 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 2679–2695 |  |
| `ensureBikeLines` | 2696–2753 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 2754–2754 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 2755–2758 |  |
| `BOUNDARY_COLOR` | 2759–2768 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 2769–2769 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 2770–2782 |  |
| `referenceSplit` | 2783–2810 |  |
| `referenceUnderLayers` | 2811–2845 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 2846–2862 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 2863–2882 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 2883–2895 |  |
| `servicesBlurb` | 2896–2913 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 2914–2937 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 2938–2948 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 2949–3000 |  |
| `REF_TIERS` | 3001–3022 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 3023–3030 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 3031–3033 |  |
| `placeAnchors` | 3034–3057 |  |
| `labelPool` | 3058–3065 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 3066–3119 |  |
| `CHROME_IDS` | 3120–3123 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 3124–3142 |  |
| `visibleLabels` | 3143–3197 |  |
| `labelLayer` | 3198–3234 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 3235–3235 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 3236–3251 |  |
| `ratioT` | 3252–3262 |  |
| `buildLayers` | 3263–3266 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 3267–3562 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 3563–3592 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 3593–3596 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 3597–3599 |  |
| `fmtBig` | 3600–3627 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 3628–3633 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 3634–3641 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 3642–3646 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 3647–3657 |  |
| `revenueLens` | 3658–3659 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 3660–3677 |  |
| `SVC_COST_BASES` | 3678–3690 | The Services panel: this hood's revenue per acre set against what the City |
| `serviceLens` | 3691–3691 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 3692–3694 |  |
| `servicePanelFor` | 3695–3708 |  |
| `hoodPanelLens` | 3709–3712 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 3713–3730 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 3731–3762 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 3763–3768 |  |
| `sparklineSvg` | 3769–3784 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 3785–3854 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 3855–3881 |  |
| `openTemporal` | 3882–3910 |  |
| `renderRevenueMix` | 3911–3959 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 3960–3993 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 3994–3996 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 3997–4047 |  |
| `syncPinnedPanel` | 4048–4074 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 4075–4090 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 4091–4101 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 4102–4149 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 4150–4155 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 4156–4195 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 4196–4212 |  |
| `temporalClick` | 4213–4270 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 4271–4350 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 4351–4679 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 4680–4727 | The sparkline rides on every OTHER view's tooltip (Services excepted |
| `REV_CUTS` | 4728–4728 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 4729–4747 |  |
| `syncMetricButtons` | 4748–4771 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 4772–4778 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 4779–4792 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 4793–4834 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 4835–4877 |  |
| `toggleBudgetPanel` | 4878–4903 |  |
| `syncMillRates` | 4904–4934 | Paint the pod, gate it to the money view's revenue cuts, and place it. |
| `applyMetric` | 4935–4956 |  |
| `applyColorAdjust` | 4957–4978 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 4979–4991 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 4992–5007 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 5008–5025 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 5026–5041 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 5042–5057 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 5058–5074 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 5075–5305 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 5306–5316 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 5317–5330 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 5331–5339 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 5340–5350 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 5351–5365 | Toggle the Uses view's residential prisms (height = share of zoned |
| `syncDevControls` | 5366–5413 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 5414–5419 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 5420–5437 |  |
| `applyMoneyDetail` | 5438–5447 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `applyMoneyMode` | 5448–5455 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 5456–5474 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 5475–5485 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 5486–5493 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 5494–5510 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 5511–5524 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 5525–5535 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 5536–5757 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 5758–5767 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 5768–5781 |  |
| `applySvcDriver` | 5782–6255 |  |

## Element ids (108) — the control surface

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
| `#budget` | 84 |
| `#budget-close` | 91 |
| `#budget-head` | 92 |
| `#budget-body` | 97 |
| `#budget-rows` | 98 |
| `#budget-other-hd` | 99 |
| `#budget-other` | 100 |
| `#budget-note` | 101 |
| `#peek` | 116 |
| `#peek-name` | 117 |
| `#peek-read` | 118 |
| `#peek-go` | 119 |
| `#controls` | 122 |
| `#toggle` | 135 |
| `#metric-row` | 136 |
| `#revcut` | 140 |
| `#moneymode` | 145 |
| `#views` | 151 |
| `#optpanel` | 165 |
| `#opt-fold` | 166 |
| `#opt-caret` | 166 |
| `#opt-body` | 167 |
| `#layers` | 168 |
| `#chgwindow-hd` | 169 |
| `#chgwindow` | 170 |
| `#labpick-hd` | 179 |
| `#labpick` | 180 |
| `#labcut-hd` | 181 |
| `#labcut` | 182 |
| `#moneydetail-hd` | 187 |
| `#moneydetail` | 188 |
| `#uses-prisms-hd` | 192 |
| `#uses-prisms` | 193 |
| `#uses-prisms-on` | 195 |
| `#devmode-hd` | 198 |
| `#devmode` | 199 |
| `#devmetric-hd` | 203 |
| `#devmetric` | 204 |
| `#devwindow-hd` | 209 |
| `#devwindow` | 210 |
| `#devdetail-hd` | 215 |
| `#devdetail` | 216 |
| `#prism-hd` | 220 |
| `#prism-row` | 221 |
| `#prism-opacity` | 223 |
| `#prism-opacity-val` | 224 |
| `#services-hd` | 226 |
| `#services` | 227 |
| `#denom-hd` | 321 |
| `#denom` | 322 |
| `#ratio-denom-hd` | 326 |
| `#ratio-denom` | 327 |
| `#hoodmode` | 338 |
| `#hoodmode-btn` | 339 |
| `#coloradj` | 351 |
| `#coloradj-btn` | 352 |
| `#budget-pod` | 359 |
| `#budget-btn` | 360 |
| `#a11y` | 364 |
| `#a11y-btn` | 365 |
| `#a11y-menu` | 366 |
| `#palette` | 368 |
| `#labels-on` | 375 |
| `#reference-on` | 383 |
| `#about` | 388 |
| `#about-btn` | 389 |
| `#about-menu` | 390 |
| `#about-src-services` | 399 |
| `#about-vintage` | 427 |
| `#about-modelled` | 434 |
| `#about-budget` | 444 |
| `#about-budget-lead` | 446 |
| `#about-budget-rows` | 447 |
| `#about-budget-note` | 448 |
| `#about-updated` | 459 |
| `#botleft` | 463 |
| `#compass` | 464 |
| `#rot-ccw` | 465 |
| `#tonorth` | 472 |
| `#needle` | 474 |
| `#rot-cw` | 479 |
| `#viewbtns` | 487 |
| `#center2d` | 488 |
| `#recenter` | 489 |
| `#legend` | 491 |
| `#legend-label` | 492 |
| `#legend-min` | 494 |
| `#legend-max` | 494 |
| `#legend-cats` | 496 |
| `#revmix` | 3930 |
| `#svccost` | 3974 |
