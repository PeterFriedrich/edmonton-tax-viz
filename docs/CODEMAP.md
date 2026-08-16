# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~6,143-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (241 indexed)

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
| `colorFor` | 1447–1449 |  |
| `quantile` | 1450–1469 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1470–1502 |  |
| `moneyBlurb` | 1503–1507 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1508–1520 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1521–1570 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### base map (no basemap tiles for v1 — just a dark backdrop)

| symbol | lines | what it does |
|---|---|---|
| `topRings` | 1571–1587 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 1588–1613 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 1614–1614 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 1615–1627 |  |
| `svcT` | 1628–1632 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 1633–1634 |  |
| `fmtFire` | 1635–1635 |  |
| `fmtTransit` | 1636–1637 |  |
| `fmtBike` | 1638–1638 |  |
| `fmtWater` | 1639–1641 |  |
| `fmtSvcCost` | 1642–1646 |  |
| `fmtRoadsCost` | 1647–1648 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtTransitCost` | 1649–1650 |  |
| `fmtBikeCost` | 1651–1662 |  |
| `servicePlaneLayer` | 1663–1695 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 1696–1705 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 1706–1711 |  |
| `DEV_IND_TOTAL` | 1712–1713 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 1714–1717 | Industrial is a hood-level choropleth only — no detail grid, not infill. |
| `devGridActive` | 1718–1722 | The 100 m detail grid applies to the residential metrics only: industrial |
| `devGridOfferable` | 1723–1723 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 1724–1724 |  |
| `devCol` | 1725–1725 |  |
| `_devScale` | 1726–1726 |  |
| `devScale` | 1727–1733 |  |
| `devT` | 1734–1737 |  |
| `developmentPlaneLayer` | 1738–1754 |  |
| `fmtDev` | 1755–1770 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 1771–1774 |  |
| `devGridColKey` | 1775–1777 |  |
| `devGridScale` | 1778–1790 |  |
| `devGridLayer` | 1791–1831 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 1832–1833 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 1834–1841 |  |
| `_infillStats` | 1842–1842 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 1843–1860 |  |
| `_infillRaw` | 1861–1863 |  |
| `infillScore` | 1864–1879 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 1880–1881 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 1882–1899 |  |
| `INFILL_CENTER` | 1900–1900 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 1901–1901 |  |
| `INFILL_NEG` | 1902–1902 |  |
| `infillColorAt` | 1903–1907 |  |
| `infillPlaneLayer` | 1908–1922 |  |
| `fmtFar` | 1923–1966 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 1967–1967 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 1968–1982 |  |
| `changeFor` | 1983–2003 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2004–2004 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2005–2019 |  |
| `chgT` | 2020–2029 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2030–2043 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePlaneLayer` | 2044–2117 | Flat plane — EXTRUDED IS FALSE BY DECISION, not by omission. Hoods moved |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2118–2125 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2126–2126 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2127–2134 |  |
| `deviationRate` | 2135–2172 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2173–2173 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `instFrac` | 2174–2203 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 2204–2210 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 2211–2222 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 2223–2226 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 2227–2231 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 2232–2242 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 2243–2258 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 2259–2285 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `INST_OUTLINE_COLOR` | 2286–2316 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `instBandLayers` | 2317–2343 |  |
| `deviationRateExempt` | 2344–2356 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 2357–2358 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 2359–2360 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 2361–2361 |  |
| `deviationStats` | 2362–2406 |  |
| `deviationOf` | 2407–2408 |  |
| `deviationT` | 2409–2419 |  |
| `fmtDeviation` | 2420–2441 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 2442–2485 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 2486–2514 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 2515–2537 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 2538–2538 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 2539–2559 |  |
| `ensureFireStations` | 2560–2575 |  |
| `TRANSIT_STATION_COLOR` | 2576–2576 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 2577–2594 |  |
| `ensureTransitStations` | 2595–2610 |  |
| `TRANSIT_LINE_COLOR` | 2611–2611 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 2612–2628 |  |
| `ensureLrtLines` | 2629–2645 |  |
| `BIKE_LINE_COLOR` | 2646–2646 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 2647–2663 |  |
| `ensureBikeLines` | 2664–2721 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 2722–2722 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 2723–2726 |  |
| `BOUNDARY_COLOR` | 2727–2736 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 2737–2737 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 2738–2750 |  |
| `referenceSplit` | 2751–2778 |  |
| `referenceUnderLayers` | 2779–2813 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 2814–2830 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 2831–2850 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 2851–2863 |  |
| `servicesBlurb` | 2864–2881 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 2882–2905 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 2906–2916 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 2917–2968 |  |
| `REF_TIERS` | 2969–2990 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 2991–2998 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 2999–3001 |  |
| `placeAnchors` | 3002–3025 |  |
| `labelPool` | 3026–3033 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 3034–3087 |  |
| `CHROME_IDS` | 3088–3091 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 3092–3110 |  |
| `visibleLabels` | 3111–3165 |  |
| `labelLayer` | 3166–3202 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 3203–3203 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 3204–3219 |  |
| `ratioT` | 3220–3230 |  |
| `buildLayers` | 3231–3234 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 3235–3530 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 3531–3560 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 3561–3564 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 3565–3567 |  |
| `fmtBig` | 3568–3595 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 3596–3601 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 3602–3609 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 3610–3614 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 3615–3625 |  |
| `revenueLens` | 3626–3627 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 3628–3645 |  |
| `SVC_COST_BASES` | 3646–3658 | The Services panel: this hood's revenue per acre set against what the City |
| `serviceLens` | 3659–3659 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 3660–3662 |  |
| `servicePanelFor` | 3663–3676 |  |
| `hoodPanelLens` | 3677–3680 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 3681–3698 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 3699–3730 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 3731–3736 |  |
| `sparklineSvg` | 3737–3752 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 3753–3822 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 3823–3849 |  |
| `openTemporal` | 3850–3878 |  |
| `renderRevenueMix` | 3879–3927 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 3928–3961 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 3962–3964 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 3965–4015 |  |
| `syncPinnedPanel` | 4016–4042 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 4043–4058 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 4059–4069 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 4070–4117 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 4118–4123 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 4124–4163 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 4164–4180 |  |
| `temporalClick` | 4181–4238 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 4239–4318 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 4319–4647 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 4648–4695 | The sparkline rides on every OTHER view's tooltip (Services excepted |
| `REV_CUTS` | 4696–4696 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 4697–4715 |  |
| `syncMetricButtons` | 4716–4739 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 4740–4746 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 4747–4760 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 4761–4804 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |
| `syncMillRates` | 4805–4835 | Paint the pod, gate it to the money view's revenue cuts, and place it. |
| `applyMetric` | 4836–4857 |  |
| `applyColorAdjust` | 4858–4879 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 4880–4892 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 4893–4908 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 4909–4926 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 4927–4942 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 4943–4958 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 4959–4975 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 4976–5206 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 5207–5217 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 5218–5231 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 5232–5240 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 5241–5251 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 5252–5266 | Toggle the Uses view's residential prisms (height = share of zoned |
| `syncDevControls` | 5267–5314 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 5315–5320 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 5321–5338 |  |
| `applyMoneyDetail` | 5339–5348 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `applyMoneyMode` | 5349–5356 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 5357–5375 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 5376–5386 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 5387–5394 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 5395–5411 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 5412–5425 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 5426–5436 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 5437–5658 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 5659–5668 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 5669–5682 |  |
| `applySvcDriver` | 5683–6143 |  |

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
| `#revmix` | 3898 |
| `#svccost` | 3942 |
