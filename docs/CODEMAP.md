# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~6,469-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (247 indexed)

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
| `devBlurb` | 1241–1289 |  |
| `withColourClause` | 1290–1304 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `ensureGridData` | 1305–1352 |  |
| `state` | 1353–1402 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `RAMPS` | 1403–1443 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1444–1450 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1451–1456 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1457–1457 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1458–1458 |  |
| `moneyColKey` | 1459–1470 |  |
| `gridScale` | 1471–1491 |  |
| `scaleT` | 1492–1498 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1499–1510 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1511–1513 |  |
| `quantile` | 1514–1528 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1529–1561 |  |
| `moneyBlurb` | 1562–1566 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1567–1579 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1580–1629 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### base map (no basemap tiles for v1 — just a dark backdrop)

| symbol | lines | what it does |
|---|---|---|
| `topRings` | 1630–1646 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 1647–1672 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 1673–1673 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 1674–1686 |  |
| `svcT` | 1687–1691 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 1692–1693 |  |
| `fmtFire` | 1694–1694 |  |
| `fmtTransit` | 1695–1696 |  |
| `fmtBike` | 1697–1697 |  |
| `fmtWater` | 1698–1700 |  |
| `fmtSvcCost` | 1701–1705 |  |
| `fmtRoadsCost` | 1706–1707 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtTransitCost` | 1708–1709 |  |
| `fmtBikeCost` | 1710–1721 |  |
| `servicePlaneLayer` | 1722–1754 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 1755–1764 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 1765–1770 |  |
| `DEV_IND_TOTAL` | 1771–1773 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 1774–1779 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 1780–1784 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 1785–1790 |  |
| `devGridOfferable` | 1791–1792 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 1793–1793 |  |
| `devCol` | 1794–1794 |  |
| `_devScale` | 1795–1795 |  |
| `devScale` | 1796–1802 |  |
| `devT` | 1803–1806 |  |
| `developmentPlaneLayer` | 1807–1823 |  |
| `fmtDev` | 1824–1839 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 1840–1845 |  |
| `DEV_GRID_IND_N` | 1846–1846 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 1847–1849 |  |
| `devGridScale` | 1850–1876 |  |
| `devGridLayer` | 1877–1925 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 1926–1927 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 1928–1935 |  |
| `_infillStats` | 1936–1936 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 1937–1954 |  |
| `_infillRaw` | 1955–1957 |  |
| `infillScore` | 1958–1973 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 1974–1975 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 1976–1993 |  |
| `INFILL_CENTER` | 1994–1994 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 1995–1995 |  |
| `INFILL_NEG` | 1996–1996 |  |
| `infillColorAt` | 1997–2001 |  |
| `infillPlaneLayer` | 2002–2016 |  |
| `fmtFar` | 2017–2060 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2061–2061 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2062–2076 |  |
| `changeFor` | 2077–2097 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2098–2098 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2099–2113 |  |
| `chgT` | 2114–2123 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2124–2137 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePlaneLayer` | 2138–2211 | Flat plane — EXTRUDED IS FALSE BY DECISION, not by omission. Hoods moved |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2212–2219 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2220–2220 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2221–2228 |  |
| `deviationRate` | 2229–2266 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2267–2267 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `instFrac` | 2268–2297 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 2298–2304 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 2305–2316 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 2317–2320 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 2321–2325 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 2326–2336 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 2337–2352 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 2353–2379 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `INST_OUTLINE_COLOR` | 2380–2432 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 2433–2437 |  |
| `bandHover` | 2438–2446 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 2447–2491 |  |
| `deviationRateExempt` | 2492–2504 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 2505–2506 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 2507–2508 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 2509–2509 |  |
| `deviationStats` | 2510–2554 |  |
| `deviationOf` | 2555–2556 |  |
| `deviationT` | 2557–2567 |  |
| `fmtDeviation` | 2568–2589 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 2590–2633 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 2634–2720 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 2721–2743 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 2744–2744 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 2745–2765 |  |
| `ensureFireStations` | 2766–2781 |  |
| `TRANSIT_STATION_COLOR` | 2782–2782 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 2783–2800 |  |
| `ensureTransitStations` | 2801–2816 |  |
| `TRANSIT_LINE_COLOR` | 2817–2817 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 2818–2834 |  |
| `ensureLrtLines` | 2835–2851 |  |
| `BIKE_LINE_COLOR` | 2852–2852 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 2853–2869 |  |
| `ensureBikeLines` | 2870–2927 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 2928–2928 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 2929–2932 |  |
| `BOUNDARY_COLOR` | 2933–2942 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 2943–2943 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 2944–2956 |  |
| `referenceSplit` | 2957–2984 |  |
| `referenceUnderLayers` | 2985–3019 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3020–3036 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3037–3056 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3057–3069 |  |
| `servicesBlurb` | 3070–3087 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3088–3111 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 3112–3122 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 3123–3174 |  |
| `REF_TIERS` | 3175–3196 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 3197–3204 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 3205–3207 |  |
| `placeAnchors` | 3208–3231 |  |
| `labelPool` | 3232–3239 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 3240–3293 |  |
| `CHROME_IDS` | 3294–3297 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 3298–3316 |  |
| `visibleLabels` | 3317–3371 |  |
| `labelLayer` | 3372–3408 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 3409–3409 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 3410–3425 |  |
| `ratioT` | 3426–3436 |  |
| `buildLayers` | 3437–3449 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 3450–3745 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 3746–3775 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 3776–3779 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 3780–3782 |  |
| `fmtBig` | 3783–3810 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 3811–3816 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 3817–3824 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 3825–3829 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 3830–3840 |  |
| `revenueLens` | 3841–3842 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 3843–3860 |  |
| `SVC_COST_BASES` | 3861–3873 | The Services panel: this hood's revenue per acre set against what the City |
| `serviceLens` | 3874–3874 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 3875–3877 |  |
| `servicePanelFor` | 3878–3891 |  |
| `hoodPanelLens` | 3892–3895 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 3896–3913 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 3914–3945 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 3946–3951 |  |
| `sparklineSvg` | 3952–3967 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 3968–4037 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 4038–4064 |  |
| `openTemporal` | 4065–4093 |  |
| `renderRevenueMix` | 4094–4142 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 4143–4176 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 4177–4179 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 4180–4230 |  |
| `syncPinnedPanel` | 4231–4257 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 4258–4273 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 4274–4284 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 4285–4332 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 4333–4338 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 4339–4378 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 4379–4395 |  |
| `temporalClick` | 4396–4453 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 4454–4533 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 4534–4866 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 4867–4921 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 4922–4922 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 4923–4941 |  |
| `syncMetricButtons` | 4942–4965 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 4966–4972 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 4973–4986 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 4987–5028 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 5029–5071 |  |
| `toggleBudgetPanel` | 5072–5097 |  |
| `syncMillRates` | 5098–5128 | Paint the pod, gate it to the money view's revenue cuts, and place it. |
| `applyMetric` | 5129–5150 |  |
| `applyColorAdjust` | 5151–5172 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 5173–5185 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 5186–5201 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 5202–5219 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 5220–5236 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 5237–5252 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 5253–5269 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 5270–5509 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 5510–5520 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 5521–5534 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 5535–5543 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 5544–5554 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 5555–5569 | Toggle the Uses view's residential prisms (height = share of zoned |
| `syncDevControls` | 5570–5617 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 5618–5623 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 5624–5641 |  |
| `applyMoneyDetail` | 5642–5651 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `applyMoneyMode` | 5652–5659 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 5660–5678 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 5679–5689 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 5690–5697 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 5698–5714 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 5715–5728 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 5729–5739 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 5740–5970 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 5971–5980 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 5981–5994 |  |
| `applySvcDriver` | 5995–6469 |  |

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
| `#revmix` | 4113 |
| `#svccost` | 4157 |
