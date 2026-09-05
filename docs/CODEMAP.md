# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~7,361-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (279 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 628–632 |  |
| `HOME` | 633–633 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 634–647 |  |
| `WINDOWS` | 648–666 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 667–676 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 677–681 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 682–749 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `fmtMoney` | 750–751 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `METRICS` | 752–877 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 878–894 |  |
| `RATIO_DENOMS` | 895–956 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 957–957 |  |
| `ratioOf` | 958–958 |  |
| `ratioKept` | 959–980 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 981–991 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 992–1019 |  |
| `dominantUse` | 1020–1061 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1062–1247 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1248–1352 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1353–1357 | the Lab: a container for unfinished lenses |
| `inLab` | 1358–1359 |  |
| `DEVIATION_TITLES` | 1360–1364 |  |
| `deviationTitle` | 1365–1370 |  |
| `deviationKind` | 1371–1373 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1374–1379 |  |
| `changeBlurb` | 1380–1404 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1405–1426 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassInstBlurb` | 1427–1437 | The azure cells need a sentence for the same reason the Lab's outlined |
| `amenityWhichPhrase` | 1438–1443 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1444–1449 |  |
| `infillAmenityBlurb` | 1450–1463 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1464–1478 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1479–1484 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1485–1492 |  |
| `devChoroplethBlurb` | 1493–1494 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1495–1543 |  |
| `withColourClause` | 1544–1561 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1562–1568 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1569–1587 | The Detail button that selects a resolution, for the busy state in |
| `loadGridData` | 1588–1641 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1642–1689 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1690–1714 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1715–1746 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1747–1747 |  |
| `gridFetches` | 1748–1771 |  |
| `RAMPS` | 1772–1812 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1813–1819 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1820–1825 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1826–1826 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1827–1833 |  |
| `AMENITY_BANDS` | 1834–1835 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1836–1838 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1839–1844 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1845–1859 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1860–1865 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1866–1884 |  |
| `gridScale` | 1885–1905 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 1906–1912 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1913–1924 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1925–1927 |  |
| `quantile` | 1928–1942 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1943–1975 |  |
| `moneyBlurb` | 1976–1980 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1981–1993 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1994–2072 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2073–2073 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2074–2100 |  |
| `failLoading` | 2101–2114 |  |
| `hideLoading` | 2115–2154 |  |
| `topRings` | 2155–2171 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2172–2197 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2198–2198 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2199–2211 |  |
| `svcT` | 2212–2216 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2217–2218 |  |
| `fmtFire` | 2219–2219 |  |
| `fmtTransit` | 2220–2221 |  |
| `fmtBike` | 2222–2222 |  |
| `fmtWater` | 2223–2225 |  |
| `fmtSvcCost` | 2226–2230 |  |
| `fmtRoadsCost` | 2231–2235 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2236–2237 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2238–2239 |  |
| `fmtBikeCost` | 2240–2251 |  |
| `servicePlaneLayer` | 2252–2284 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2285–2294 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2295–2300 |  |
| `DEV_IND_TOTAL` | 2301–2303 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2304–2309 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2310–2314 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2315–2320 |  |
| `devGridOfferable` | 2321–2322 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2323–2323 |  |
| `devCol` | 2324–2324 |  |
| `_devScale` | 2325–2325 |  |
| `devScale` | 2326–2332 |  |
| `devT` | 2333–2336 |  |
| `developmentPlaneLayer` | 2337–2353 |  |
| `fmtDev` | 2354–2369 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2370–2375 |  |
| `DEV_GRID_IND_N` | 2376–2376 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2377–2379 |  |
| `devGridScale` | 2380–2406 |  |
| `devGridLayer` | 2407–2455 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2456–2457 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2458–2465 |  |
| `_infillStats` | 2466–2466 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2467–2484 |  |
| `_infillRaw` | 2485–2487 |  |
| `infillScore` | 2488–2503 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2504–2505 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2506–2523 |  |
| `INFILL_CENTER` | 2524–2524 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2525–2525 |  |
| `INFILL_NEG` | 2526–2526 |  |
| `infillColorAt` | 2527–2531 |  |
| `infillPlaneLayer` | 2532–2546 |  |
| `fmtFar` | 2547–2556 |  |
| `AMENITY_HIGHLIGHT_COLOR` | 2557–2557 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2558–2612 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2613–2620 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2621–2635 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2636–2656 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2657–2657 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2658–2672 |  |
| `chgT` | 2673–2682 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2683–2713 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2714–2802 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2803–2810 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2811–2811 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2812–2819 |  |
| `deviationRate` | 2820–2862 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2863–2863 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 2864–2893 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 2894–2900 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 2901–2912 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 2913–2916 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 2917–2921 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 2922–2932 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 2933–2948 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 2949–2975 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `INST_OUTLINE_COLOR` | 2976–3028 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 3029–3033 |  |
| `bandHover` | 3034–3042 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3043–3139 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3140–3147 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3148–3149 |  |
| `glassInstBandLayers` | 3150–3178 |  |
| `deviationRateExempt` | 3179–3191 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3192–3193 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3194–3195 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3196–3196 |  |
| `deviationStats` | 3197–3241 |  |
| `deviationOf` | 3242–3243 |  |
| `deviationT` | 3244–3254 |  |
| `fmtDeviation` | 3255–3276 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3277–3320 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3321–3407 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3408–3430 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3431–3431 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3432–3452 |  |
| `ensureFireStations` | 3453–3468 |  |
| `TRANSIT_STATION_COLOR` | 3469–3469 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3470–3487 |  |
| `ensureTransitStations` | 3488–3503 |  |
| `TRANSIT_LINE_COLOR` | 3504–3504 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3505–3521 |  |
| `ensureLrtLines` | 3522–3538 |  |
| `BIKE_LINE_COLOR` | 3539–3539 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3540–3556 |  |
| `ensureBikeLines` | 3557–3614 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3615–3615 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3616–3619 |  |
| `BOUNDARY_COLOR` | 3620–3629 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3630–3630 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3631–3643 |  |
| `referenceSplit` | 3644–3671 |  |
| `referenceUnderLayers` | 3672–3706 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3707–3723 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3724–3743 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3744–3756 |  |
| `servicesBlurb` | 3757–3774 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3775–3798 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 3799–3809 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 3810–3861 |  |
| `REF_TIERS` | 3862–3883 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 3884–3891 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 3892–3894 |  |
| `placeAnchors` | 3895–3918 |  |
| `labelPool` | 3919–3926 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 3927–3980 |  |
| `CHROME_IDS` | 3981–3984 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 3985–4003 |  |
| `visibleLabels` | 4004–4058 |  |
| `labelLayer` | 4059–4095 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 4096–4096 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4097–4112 |  |
| `ratioT` | 4113–4123 |  |
| `buildLayers` | 4124–4136 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 4137–4439 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4440–4469 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4470–4473 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4474–4476 |  |
| `fmtBig` | 4477–4504 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4505–4510 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4511–4518 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4519–4523 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4524–4534 |  |
| `revenueLens` | 4535–4536 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4537–4561 |  |
| `SVC_COST_BASES` | 4562–4576 | The Services panel: this hood's revenue per acre set against what the City |
| `serviceLens` | 4577–4577 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4578–4581 |  |
| `servicePanelFor` | 4582–4595 |  |
| `hoodPanelLens` | 4596–4599 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4600–4617 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4618–4649 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 4650–4655 |  |
| `sparklineSvg` | 4656–4671 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 4672–4741 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 4742–4768 |  |
| `openTemporal` | 4769–4797 |  |
| `renderRevenueMix` | 4798–4846 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 4847–4893 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 4894–4896 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 4897–4947 |  |
| `syncPinnedPanel` | 4948–4974 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 4975–4990 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 4991–5001 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5002–5049 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5050–5055 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5056–5095 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5096–5112 |  |
| `temporalClick` | 5113–5170 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 5171–5251 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 5252–5589 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 5590–5657 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 5658–5658 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 5659–5677 |  |
| `syncMetricButtons` | 5678–5701 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 5702–5708 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 5709–5722 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 5723–5764 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 5765–5807 |  |
| `toggleBudgetPanel` | 5808–5833 |  |
| `syncMillRates` | 5834–5866 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 5867–5888 |  |
| `applyColorAdjust` | 5889–5910 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 5911–5923 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 5924–5939 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 5940–5957 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 5958–5974 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 5975–5990 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 5991–6007 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 6008–6255 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 6256–6266 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 6267–6280 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 6281–6289 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 6290–6300 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 6301–6312 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 6313–6326 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 6327–6347 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 6348–6395 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 6396–6401 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 6402–6423 |  |
| `applyMoneyDetail` | 6424–6448 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 6449–6460 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 6461–6468 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 6469–6487 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 6488–6498 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 6499–6506 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 6507–6523 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 6524–6537 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 6538–6548 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 6549–6792 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 6793–6802 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 6803–6816 |  |
| `applySvcDriver` | 6817–6830 |  |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 6831–7361 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (858 edges)

⚠️ **A regex reference count, not a call graph** — a name in a comment or string counts, and a nested symbol is attributed to its enclosing range. Use it for *what is central* and *would this seam hold*, never as ground truth for a final module boundary.

**Most depended-on** — moving one of these touches everything below it.

| symbol | referenced by | section |
|---|---|---|
| `state` | 111 | the Lab: a container for unfinished lenses |
| `buildLayers` | 35 | geographic reference layers (all views) |
| `METRICS` | 16 | tunables |
| `refreshLegend` | 14 | control appliers + the view/legend dispatchers |
| `applyView` | 13 | control appliers + the view/legend dispatchers |
| `SERVICES` | 12 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `CELLS` | 10 | tunables |
| `quantile` | 10 | the Lab: a container for unfinished lenses |
| `deviationStats` | 9 | the same doubt, at 100 m |
| `ratioDenom` | 8 | services lens views (SPEC_services.md display architecture) |
| `ratioScale` | 8 | geographic reference layers (all views) |
| `devIndustrial` | 8 | loading overlay |
| `devCol` | 8 | loading overlay |
| `labelPool` | 8 | geographic reference layers (all views) |
| `esc` | 8 | money view (default): the classic metric prisms |

**Section self-containment** — share of each section's outgoing edges that stay inside it. Low means a module cut on this banner would mostly import its neighbours.

| section | edges | self-contained |
|---|---|---|
| services lens views (SPEC_services.md display architecture) | 1 | 100% |
| uses view (use-mix, 2026-07-03) | 3 | 67% |
| deviation lens: revenue per developed acre against peer average | 3 | 67% |
| Infill lens (SPEC_development.md Lens B) | 26 | 65% |
| the Lab: a container for unfinished lenses | 100 | 63% |
| tunables | 10 | 60% |
| Development 100 m detail grid (layers-panel toggle, 2026-07-15) | 9 | 44% |
| change lens: how each hood's share of the assessment base moved | 16 | 44% |
| loading overlay | 45 | 42% |
| geographic reference layers (all views) | 86 | 42% |
| Money's revenue panel: where a hood's levy comes from | 186 | 38% |
| two tiers, answering two different questions | 27 | 33% |
| the same doubt, at 100 m | 53 | 30% |
| control appliers + the view/legend dispatchers | 206 | 21% |
| the citywide budget panel (EXPERIMENTAL, full build only) | 12 | 8% |
| services view (SPEC_services.md UI generalization, 2026-07-05) | 16 | 0% |
| the institutional uncertainty band | 2 | 0% |
| temporal lens (SPEC_temporal.md phase 3) | 1 | 0% |
| boot | 56 | 0% |

## Element ids (124) — the control surface

| id | line |
|---|---|
| `#map` | 18 |
| `#loading` | 22 |
| `#loading-box` | 23 |
| `#loading-title` | 34 |
| `#loading-blurb` | 35 |
| `#loading-spinner` | 36 |
| `#loading-text` | 37 |
| `#loading-retry` | 38 |
| `#banner` | 42 |
| `#title` | 44 |
| `#title-h` | 45 |
| `#title-p` | 46 |
| `#temporal` | 57 |
| `#temporal-close` | 58 |
| `#temporal-name` | 59 |
| `#temporal-body` | 66 |
| `#temporal-chart` | 67 |
| `#temporal-read` | 68 |
| `#temporal-note` | 69 |
| `#temporal-hint` | 73 |
| `#millrates` | 89 |
| `#mill-head` | 90 |
| `#mill-rows` | 91 |
| `#mill-note` | 92 |
| `#budget` | 106 |
| `#budget-close` | 113 |
| `#budget-head` | 114 |
| `#budget-body` | 119 |
| `#budget-rows` | 120 |
| `#budget-other-hd` | 121 |
| `#budget-other` | 122 |
| `#budget-note` | 123 |
| `#peek` | 138 |
| `#peek-name` | 139 |
| `#peek-read` | 140 |
| `#peek-go` | 141 |
| `#controls` | 144 |
| `#toggle` | 157 |
| `#metric-row` | 158 |
| `#revcut` | 162 |
| `#moneymode` | 167 |
| `#views` | 173 |
| `#optpanel` | 187 |
| `#opt-fold` | 188 |
| `#opt-caret` | 188 |
| `#opt-body` | 189 |
| `#layers` | 190 |
| `#chgwindow-hd` | 191 |
| `#chgwindow` | 192 |
| `#labpick-hd` | 201 |
| `#labpick` | 202 |
| `#labcut-hd` | 203 |
| `#labcut` | 204 |
| `#moneydetail-hd` | 209 |
| `#moneydetail` | 210 |
| `#amenity-hd` | 235 |
| `#amenity` | 236 |
| `#amenity-lrt-row` | 237 |
| `#amenity-lrt-on` | 238 |
| `#amenity-school-row` | 240 |
| `#amenity-school-on` | 241 |
| `#uses-prisms-hd` | 244 |
| `#uses-prisms` | 245 |
| `#uses-prisms-on` | 247 |
| `#devmode-hd` | 250 |
| `#devmode` | 251 |
| `#devmetric-hd` | 255 |
| `#devmetric` | 256 |
| `#devwindow-hd` | 261 |
| `#devwindow` | 262 |
| `#devdetail-hd` | 267 |
| `#devdetail` | 268 |
| `#prism-hd` | 272 |
| `#prism-row` | 273 |
| `#prism-opacity` | 275 |
| `#prism-opacity-val` | 276 |
| `#services-hd` | 278 |
| `#services` | 279 |
| `#denom-hd` | 386 |
| `#denom` | 387 |
| `#ratio-denom-hd` | 391 |
| `#ratio-denom` | 392 |
| `#hoodmode` | 403 |
| `#hoodmode-btn` | 404 |
| `#coloradj` | 416 |
| `#coloradj-btn` | 417 |
| `#budget-pod` | 424 |
| `#budget-btn` | 425 |
| `#a11y` | 429 |
| `#a11y-btn` | 430 |
| `#a11y-menu` | 431 |
| `#palette` | 433 |
| `#labels-on` | 440 |
| `#reference-on` | 448 |
| `#about` | 453 |
| `#about-btn` | 454 |
| `#about-menu` | 455 |
| `#about-src-roads` | 467 |
| `#about-src-services` | 468 |
| `#about-vintage` | 496 |
| `#about-build` | 500 |
| `#about-modelled-roads` | 514 |
| `#about-modelled` | 528 |
| `#about-budget` | 538 |
| `#about-budget-lead` | 540 |
| `#about-budget-rows` | 541 |
| `#about-budget-note` | 542 |
| `#about-updated` | 553 |
| `#botleft` | 557 |
| `#compass` | 558 |
| `#rot-ccw` | 559 |
| `#tonorth` | 566 |
| `#needle` | 568 |
| `#rot-cw` | 573 |
| `#viewbtns` | 581 |
| `#center2d` | 582 |
| `#recenter` | 583 |
| `#legend` | 585 |
| `#legend-label` | 586 |
| `#legend-min` | 588 |
| `#legend-max` | 588 |
| `#legend-cats` | 590 |
| `#revmix` | 4817 |
| `#svccost` | 4866 |
