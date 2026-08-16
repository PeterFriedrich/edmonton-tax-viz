# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~6,238-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (243 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 514–518 |  |
| `HOME` | 519–519 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 520–563 |  |
| `fmtMoney` | 564–565 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `METRICS` | 566–691 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 692–708 |  |
| `RATIO_DENOMS` | 709–770 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 771–771 |  |
| `ratioOf` | 772–772 |  |
| `ratioKept` | 773–794 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 795–805 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 806–833 |  |
| `dominantUse` | 834–867 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 868–1022 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1023–1127 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1128–1132 | the Lab: a container for unfinished lenses |
| `inLab` | 1133–1134 |  |
| `DEVIATION_TITLES` | 1135–1139 |  |
| `deviationTitle` | 1140–1145 |  |
| `deviationKind` | 1146–1148 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1149–1154 |  |
| `changeBlurb` | 1155–1174 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1175–1191 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassBlurb` | 1192–1196 |  |
| `usesBlurb` | 1197–1211 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1212–1217 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1218–1225 |  |
| `devChoroplethBlurb` | 1226–1227 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1228–1249 |  |
| `withColourClause` | 1250–1264 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `ensureGridData` | 1265–1312 |  |
| `state` | 1313–1362 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `RAMPS` | 1363–1403 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1404–1410 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1411–1416 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1417–1417 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1418–1418 |  |
| `moneyColKey` | 1419–1430 |  |
| `gridScale` | 1431–1451 |  |
| `scaleT` | 1452–1458 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1459–1470 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1471–1473 |  |
| `quantile` | 1474–1488 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1489–1521 |  |
| `moneyBlurb` | 1522–1526 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1527–1539 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1540–1589 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### base map (no basemap tiles for v1 — just a dark backdrop)

| symbol | lines | what it does |
|---|---|---|
| `topRings` | 1590–1606 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 1607–1632 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 1633–1633 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 1634–1646 |  |
| `svcT` | 1647–1651 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 1652–1653 |  |
| `fmtFire` | 1654–1654 |  |
| `fmtTransit` | 1655–1656 |  |
| `fmtBike` | 1657–1657 |  |
| `fmtWater` | 1658–1660 |  |
| `fmtSvcCost` | 1661–1665 |  |
| `fmtRoadsCost` | 1666–1667 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtTransitCost` | 1668–1669 |  |
| `fmtBikeCost` | 1670–1681 |  |
| `servicePlaneLayer` | 1682–1714 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 1715–1724 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 1725–1730 |  |
| `DEV_IND_TOTAL` | 1731–1732 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 1733–1736 | Industrial is a hood-level choropleth only — no detail grid, not infill. |
| `devGridActive` | 1737–1741 | The 100 m detail grid applies to the residential metrics only: industrial |
| `devGridOfferable` | 1742–1742 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 1743–1743 |  |
| `devCol` | 1744–1744 |  |
| `_devScale` | 1745–1745 |  |
| `devScale` | 1746–1752 |  |
| `devT` | 1753–1756 |  |
| `developmentPlaneLayer` | 1757–1773 |  |
| `fmtDev` | 1774–1789 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 1790–1793 |  |
| `devGridColKey` | 1794–1796 |  |
| `devGridScale` | 1797–1809 |  |
| `devGridLayer` | 1810–1850 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 1851–1852 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 1853–1860 |  |
| `_infillStats` | 1861–1861 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 1862–1879 |  |
| `_infillRaw` | 1880–1882 |  |
| `infillScore` | 1883–1898 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 1899–1900 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 1901–1918 |  |
| `INFILL_CENTER` | 1919–1919 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 1920–1920 |  |
| `INFILL_NEG` | 1921–1921 |  |
| `infillColorAt` | 1922–1926 |  |
| `infillPlaneLayer` | 1927–1941 |  |
| `fmtFar` | 1942–1985 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 1986–1986 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 1987–2001 |  |
| `changeFor` | 2002–2022 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2023–2023 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2024–2038 |  |
| `chgT` | 2039–2048 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2049–2062 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePlaneLayer` | 2063–2136 | Flat plane — EXTRUDED IS FALSE BY DECISION, not by omission. Hoods moved |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2137–2144 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2145–2145 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2146–2153 |  |
| `deviationRate` | 2154–2191 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2192–2192 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `instFrac` | 2193–2222 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 2223–2229 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 2230–2241 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 2242–2245 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 2246–2250 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 2251–2261 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 2262–2277 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 2278–2304 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `INST_OUTLINE_COLOR` | 2305–2335 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `instBandLayers` | 2336–2362 |  |
| `deviationRateExempt` | 2363–2375 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 2376–2377 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 2378–2379 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 2380–2380 |  |
| `deviationStats` | 2381–2425 |  |
| `deviationOf` | 2426–2427 |  |
| `deviationT` | 2428–2438 |  |
| `fmtDeviation` | 2439–2460 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 2461–2504 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 2505–2533 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 2534–2556 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 2557–2557 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 2558–2578 |  |
| `ensureFireStations` | 2579–2594 |  |
| `TRANSIT_STATION_COLOR` | 2595–2595 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 2596–2613 |  |
| `ensureTransitStations` | 2614–2629 |  |
| `TRANSIT_LINE_COLOR` | 2630–2630 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 2631–2647 |  |
| `ensureLrtLines` | 2648–2664 |  |
| `BIKE_LINE_COLOR` | 2665–2665 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 2666–2682 |  |
| `ensureBikeLines` | 2683–2740 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 2741–2741 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 2742–2745 |  |
| `BOUNDARY_COLOR` | 2746–2755 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 2756–2756 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 2757–2769 |  |
| `referenceSplit` | 2770–2797 |  |
| `referenceUnderLayers` | 2798–2832 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 2833–2849 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 2850–2869 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 2870–2882 |  |
| `servicesBlurb` | 2883–2900 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 2901–2924 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 2925–2935 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 2936–2987 |  |
| `REF_TIERS` | 2988–3009 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 3010–3017 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 3018–3020 |  |
| `placeAnchors` | 3021–3044 |  |
| `labelPool` | 3045–3052 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 3053–3106 |  |
| `CHROME_IDS` | 3107–3110 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 3111–3129 |  |
| `visibleLabels` | 3130–3184 |  |
| `labelLayer` | 3185–3221 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 3222–3222 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 3223–3238 |  |
| `ratioT` | 3239–3249 |  |
| `buildLayers` | 3250–3253 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 3254–3549 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 3550–3579 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 3580–3583 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 3584–3586 |  |
| `fmtBig` | 3587–3614 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 3615–3620 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 3621–3628 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 3629–3633 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 3634–3644 |  |
| `revenueLens` | 3645–3646 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 3647–3664 |  |
| `SVC_COST_BASES` | 3665–3677 | The Services panel: this hood's revenue per acre set against what the City |
| `serviceLens` | 3678–3678 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 3679–3681 |  |
| `servicePanelFor` | 3682–3695 |  |
| `hoodPanelLens` | 3696–3699 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 3700–3717 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 3718–3749 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 3750–3755 |  |
| `sparklineSvg` | 3756–3771 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 3772–3841 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 3842–3868 |  |
| `openTemporal` | 3869–3897 |  |
| `renderRevenueMix` | 3898–3946 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 3947–3980 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 3981–3983 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 3984–4034 |  |
| `syncPinnedPanel` | 4035–4061 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 4062–4077 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 4078–4088 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 4089–4136 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 4137–4142 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 4143–4182 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 4183–4199 |  |
| `temporalClick` | 4200–4257 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 4258–4337 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 4338–4666 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 4667–4714 | The sparkline rides on every OTHER view's tooltip (Services excepted |
| `REV_CUTS` | 4715–4715 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 4716–4734 |  |
| `syncMetricButtons` | 4735–4758 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 4759–4765 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 4766–4779 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 4780–4821 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 4822–4864 |  |
| `toggleBudgetPanel` | 4865–4890 |  |
| `syncMillRates` | 4891–4921 | Paint the pod, gate it to the money view's revenue cuts, and place it. |
| `applyMetric` | 4922–4943 |  |
| `applyColorAdjust` | 4944–4965 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 4966–4978 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 4979–4994 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 4995–5012 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 5013–5028 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 5029–5044 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 5045–5061 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 5062–5292 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 5293–5303 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 5304–5317 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 5318–5326 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 5327–5337 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 5338–5352 | Toggle the Uses view's residential prisms (height = share of zoned |
| `syncDevControls` | 5353–5400 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 5401–5406 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 5407–5424 |  |
| `applyMoneyDetail` | 5425–5434 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `applyMoneyMode` | 5435–5442 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 5443–5461 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 5462–5472 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 5473–5480 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 5481–5497 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 5498–5511 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 5512–5522 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 5523–5744 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 5745–5754 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 5755–5768 |  |
| `applySvcDriver` | 5769–6238 |  |

## Element ids (106) — the control surface

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
| `#budget-head` | 85 |
| `#budget-rows` | 86 |
| `#budget-other-hd` | 87 |
| `#budget-other` | 88 |
| `#budget-note` | 89 |
| `#peek` | 103 |
| `#peek-name` | 104 |
| `#peek-read` | 105 |
| `#peek-go` | 106 |
| `#controls` | 109 |
| `#toggle` | 122 |
| `#metric-row` | 123 |
| `#revcut` | 127 |
| `#moneymode` | 132 |
| `#views` | 138 |
| `#optpanel` | 152 |
| `#opt-fold` | 153 |
| `#opt-caret` | 153 |
| `#opt-body` | 154 |
| `#layers` | 155 |
| `#chgwindow-hd` | 156 |
| `#chgwindow` | 157 |
| `#labpick-hd` | 166 |
| `#labpick` | 167 |
| `#labcut-hd` | 168 |
| `#labcut` | 169 |
| `#moneydetail-hd` | 174 |
| `#moneydetail` | 175 |
| `#uses-prisms-hd` | 179 |
| `#uses-prisms` | 180 |
| `#uses-prisms-on` | 182 |
| `#devmode-hd` | 185 |
| `#devmode` | 186 |
| `#devmetric-hd` | 190 |
| `#devmetric` | 191 |
| `#devwindow-hd` | 196 |
| `#devwindow` | 197 |
| `#devdetail-hd` | 202 |
| `#devdetail` | 203 |
| `#prism-hd` | 207 |
| `#prism-row` | 208 |
| `#prism-opacity` | 210 |
| `#prism-opacity-val` | 211 |
| `#services-hd` | 213 |
| `#services` | 214 |
| `#denom-hd` | 308 |
| `#denom` | 309 |
| `#ratio-denom-hd` | 313 |
| `#ratio-denom` | 314 |
| `#hoodmode` | 325 |
| `#hoodmode-btn` | 326 |
| `#coloradj` | 338 |
| `#coloradj-btn` | 339 |
| `#budget-pod` | 346 |
| `#budget-btn` | 347 |
| `#a11y` | 351 |
| `#a11y-btn` | 352 |
| `#a11y-menu` | 353 |
| `#palette` | 355 |
| `#labels-on` | 362 |
| `#reference-on` | 370 |
| `#about` | 375 |
| `#about-btn` | 376 |
| `#about-menu` | 377 |
| `#about-src-services` | 386 |
| `#about-vintage` | 414 |
| `#about-modelled` | 421 |
| `#about-budget` | 431 |
| `#about-budget-lead` | 433 |
| `#about-budget-rows` | 434 |
| `#about-budget-note` | 435 |
| `#about-updated` | 446 |
| `#botleft` | 450 |
| `#compass` | 451 |
| `#rot-ccw` | 452 |
| `#tonorth` | 459 |
| `#needle` | 461 |
| `#rot-cw` | 466 |
| `#viewbtns` | 474 |
| `#center2d` | 475 |
| `#recenter` | 476 |
| `#legend` | 478 |
| `#legend-label` | 479 |
| `#legend-min` | 481 |
| `#legend-max` | 481 |
| `#legend-cats` | 483 |
| `#revmix` | 3917 |
| `#svccost` | 3961 |
