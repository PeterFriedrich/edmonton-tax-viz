# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~6,587-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (251 indexed)

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
| `GLASS_BLURBS` | 1188–1209 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassInstBlurb` | 1210–1217 | The azure cells need a sentence for the same reason the Lab's outlined |
| `glassBlurb` | 1218–1223 |  |
| `usesBlurb` | 1224–1238 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1239–1244 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1245–1252 |  |
| `devChoroplethBlurb` | 1253–1254 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1255–1303 |  |
| `withColourClause` | 1304–1318 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `ensureGridData` | 1319–1372 |  |
| `state` | 1373–1422 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `RAMPS` | 1423–1463 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1464–1470 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1471–1476 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1477–1477 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1478–1478 |  |
| `moneyColKey` | 1479–1490 |  |
| `gridScale` | 1491–1511 |  |
| `scaleT` | 1512–1518 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1519–1530 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1531–1533 |  |
| `quantile` | 1534–1548 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1549–1581 |  |
| `moneyBlurb` | 1582–1586 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1587–1599 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1600–1649 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### base map (no basemap tiles for v1 — just a dark backdrop)

| symbol | lines | what it does |
|---|---|---|
| `topRings` | 1650–1666 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 1667–1692 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 1693–1693 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 1694–1706 |  |
| `svcT` | 1707–1711 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 1712–1713 |  |
| `fmtFire` | 1714–1714 |  |
| `fmtTransit` | 1715–1716 |  |
| `fmtBike` | 1717–1717 |  |
| `fmtWater` | 1718–1720 |  |
| `fmtSvcCost` | 1721–1725 |  |
| `fmtRoadsCost` | 1726–1727 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtTransitCost` | 1728–1729 |  |
| `fmtBikeCost` | 1730–1741 |  |
| `servicePlaneLayer` | 1742–1774 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 1775–1784 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 1785–1790 |  |
| `DEV_IND_TOTAL` | 1791–1793 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 1794–1799 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 1800–1804 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 1805–1810 |  |
| `devGridOfferable` | 1811–1812 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 1813–1813 |  |
| `devCol` | 1814–1814 |  |
| `_devScale` | 1815–1815 |  |
| `devScale` | 1816–1822 |  |
| `devT` | 1823–1826 |  |
| `developmentPlaneLayer` | 1827–1843 |  |
| `fmtDev` | 1844–1859 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 1860–1865 |  |
| `DEV_GRID_IND_N` | 1866–1866 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 1867–1869 |  |
| `devGridScale` | 1870–1896 |  |
| `devGridLayer` | 1897–1945 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 1946–1947 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 1948–1955 |  |
| `_infillStats` | 1956–1956 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 1957–1974 |  |
| `_infillRaw` | 1975–1977 |  |
| `infillScore` | 1978–1993 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 1994–1995 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 1996–2013 |  |
| `INFILL_CENTER` | 2014–2014 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2015–2015 |  |
| `INFILL_NEG` | 2016–2016 |  |
| `infillColorAt` | 2017–2021 |  |
| `infillPlaneLayer` | 2022–2036 |  |
| `fmtFar` | 2037–2080 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2081–2081 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2082–2096 |  |
| `changeFor` | 2097–2117 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2118–2118 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2119–2133 |  |
| `chgT` | 2134–2143 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2144–2157 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePlaneLayer` | 2158–2231 | Flat plane — EXTRUDED IS FALSE BY DECISION, not by omission. Hoods moved |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2232–2239 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2240–2240 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2241–2248 |  |
| `deviationRate` | 2249–2286 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2287–2287 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `instFrac` | 2288–2317 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 2318–2324 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 2325–2336 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 2337–2340 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 2341–2345 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 2346–2356 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 2357–2372 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 2373–2399 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `INST_OUTLINE_COLOR` | 2400–2452 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 2453–2457 |  |
| `bandHover` | 2458–2466 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 2467–2563 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 2564–2571 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 2572–2573 |  |
| `glassInstBandLayers` | 2574–2602 |  |
| `deviationRateExempt` | 2603–2615 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 2616–2617 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 2618–2619 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 2620–2620 |  |
| `deviationStats` | 2621–2665 |  |
| `deviationOf` | 2666–2667 |  |
| `deviationT` | 2668–2678 |  |
| `fmtDeviation` | 2679–2700 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 2701–2744 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 2745–2831 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 2832–2854 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 2855–2855 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 2856–2876 |  |
| `ensureFireStations` | 2877–2892 |  |
| `TRANSIT_STATION_COLOR` | 2893–2893 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 2894–2911 |  |
| `ensureTransitStations` | 2912–2927 |  |
| `TRANSIT_LINE_COLOR` | 2928–2928 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 2929–2945 |  |
| `ensureLrtLines` | 2946–2962 |  |
| `BIKE_LINE_COLOR` | 2963–2963 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 2964–2980 |  |
| `ensureBikeLines` | 2981–3038 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3039–3039 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3040–3043 |  |
| `BOUNDARY_COLOR` | 3044–3053 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3054–3054 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3055–3067 |  |
| `referenceSplit` | 3068–3095 |  |
| `referenceUnderLayers` | 3096–3130 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3131–3147 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3148–3167 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3168–3180 |  |
| `servicesBlurb` | 3181–3198 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3199–3222 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 3223–3233 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 3234–3285 |  |
| `REF_TIERS` | 3286–3307 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 3308–3315 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 3316–3318 |  |
| `placeAnchors` | 3319–3342 |  |
| `labelPool` | 3343–3350 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 3351–3404 |  |
| `CHROME_IDS` | 3405–3408 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 3409–3427 |  |
| `visibleLabels` | 3428–3482 |  |
| `labelLayer` | 3483–3519 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 3520–3520 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 3521–3536 |  |
| `ratioT` | 3537–3547 |  |
| `buildLayers` | 3548–3560 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 3561–3863 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 3864–3893 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 3894–3897 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 3898–3900 |  |
| `fmtBig` | 3901–3928 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 3929–3934 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 3935–3942 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 3943–3947 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 3948–3958 |  |
| `revenueLens` | 3959–3960 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 3961–3978 |  |
| `SVC_COST_BASES` | 3979–3991 | The Services panel: this hood's revenue per acre set against what the City |
| `serviceLens` | 3992–3992 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 3993–3995 |  |
| `servicePanelFor` | 3996–4009 |  |
| `hoodPanelLens` | 4010–4013 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4014–4031 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4032–4063 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 4064–4069 |  |
| `sparklineSvg` | 4070–4085 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 4086–4155 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 4156–4182 |  |
| `openTemporal` | 4183–4211 |  |
| `renderRevenueMix` | 4212–4260 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 4261–4294 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 4295–4297 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 4298–4348 |  |
| `syncPinnedPanel` | 4349–4375 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 4376–4391 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 4392–4402 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 4403–4450 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 4451–4456 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 4457–4496 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 4497–4513 |  |
| `temporalClick` | 4514–4571 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 4572–4651 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 4652–4984 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 4985–5039 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 5040–5040 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 5041–5059 |  |
| `syncMetricButtons` | 5060–5083 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 5084–5090 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 5091–5104 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 5105–5146 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 5147–5189 |  |
| `toggleBudgetPanel` | 5190–5215 |  |
| `syncMillRates` | 5216–5246 | Paint the pod, gate it to the money view's revenue cuts, and place it. |
| `applyMetric` | 5247–5268 |  |
| `applyColorAdjust` | 5269–5290 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 5291–5303 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 5304–5319 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 5320–5337 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 5338–5354 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 5355–5370 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 5371–5387 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 5388–5627 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 5628–5638 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 5639–5652 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 5653–5661 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 5662–5672 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 5673–5687 | Toggle the Uses view's residential prisms (height = share of zoned |
| `syncDevControls` | 5688–5735 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 5736–5741 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 5742–5759 |  |
| `applyMoneyDetail` | 5760–5769 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `applyMoneyMode` | 5770–5777 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 5778–5796 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 5797–5807 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 5808–5815 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 5816–5832 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 5833–5846 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 5847–5857 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 5858–6088 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 6089–6098 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 6099–6112 |  |
| `applySvcDriver` | 6113–6587 |  |

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
| `#revmix` | 4231 |
| `#svccost` | 4275 |
