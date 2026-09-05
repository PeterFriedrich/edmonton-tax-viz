# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~7,354-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (279 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 621–625 |  |
| `HOME` | 626–626 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 627–640 |  |
| `WINDOWS` | 641–659 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 660–669 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 670–674 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 675–742 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `fmtMoney` | 743–744 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `METRICS` | 745–870 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 871–887 |  |
| `RATIO_DENOMS` | 888–949 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 950–950 |  |
| `ratioOf` | 951–951 |  |
| `ratioKept` | 952–973 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 974–984 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 985–1012 |  |
| `dominantUse` | 1013–1054 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1055–1240 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1241–1345 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1346–1350 | the Lab: a container for unfinished lenses |
| `inLab` | 1351–1352 |  |
| `DEVIATION_TITLES` | 1353–1357 |  |
| `deviationTitle` | 1358–1363 |  |
| `deviationKind` | 1364–1366 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1367–1372 |  |
| `changeBlurb` | 1373–1397 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1398–1419 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassInstBlurb` | 1420–1430 | The azure cells need a sentence for the same reason the Lab's outlined |
| `amenityWhichPhrase` | 1431–1436 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1437–1442 |  |
| `infillAmenityBlurb` | 1443–1456 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1457–1471 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1472–1477 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1478–1485 |  |
| `devChoroplethBlurb` | 1486–1487 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1488–1536 |  |
| `withColourClause` | 1537–1554 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1555–1561 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1562–1580 | The Detail button that selects a resolution, for the busy state in |
| `loadGridData` | 1581–1634 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1635–1682 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1683–1707 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1708–1739 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1740–1740 |  |
| `gridFetches` | 1741–1764 |  |
| `RAMPS` | 1765–1805 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1806–1812 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1813–1818 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1819–1819 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1820–1826 |  |
| `AMENITY_BANDS` | 1827–1828 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1829–1831 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1832–1837 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1838–1852 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1853–1858 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1859–1877 |  |
| `gridScale` | 1878–1898 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 1899–1905 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1906–1917 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1918–1920 |  |
| `quantile` | 1921–1935 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1936–1968 |  |
| `moneyBlurb` | 1969–1973 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1974–1986 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1987–2065 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2066–2066 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2067–2093 |  |
| `failLoading` | 2094–2107 |  |
| `hideLoading` | 2108–2147 |  |
| `topRings` | 2148–2164 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2165–2190 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2191–2191 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2192–2204 |  |
| `svcT` | 2205–2209 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2210–2211 |  |
| `fmtFire` | 2212–2212 |  |
| `fmtTransit` | 2213–2214 |  |
| `fmtBike` | 2215–2215 |  |
| `fmtWater` | 2216–2218 |  |
| `fmtSvcCost` | 2219–2223 |  |
| `fmtRoadsCost` | 2224–2228 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2229–2230 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2231–2232 |  |
| `fmtBikeCost` | 2233–2244 |  |
| `servicePlaneLayer` | 2245–2277 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2278–2287 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2288–2293 |  |
| `DEV_IND_TOTAL` | 2294–2296 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2297–2302 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2303–2307 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2308–2313 |  |
| `devGridOfferable` | 2314–2315 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2316–2316 |  |
| `devCol` | 2317–2317 |  |
| `_devScale` | 2318–2318 |  |
| `devScale` | 2319–2325 |  |
| `devT` | 2326–2329 |  |
| `developmentPlaneLayer` | 2330–2346 |  |
| `fmtDev` | 2347–2362 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2363–2368 |  |
| `DEV_GRID_IND_N` | 2369–2369 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2370–2372 |  |
| `devGridScale` | 2373–2399 |  |
| `devGridLayer` | 2400–2448 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2449–2450 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2451–2458 |  |
| `_infillStats` | 2459–2459 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2460–2477 |  |
| `_infillRaw` | 2478–2480 |  |
| `infillScore` | 2481–2496 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2497–2498 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2499–2516 |  |
| `INFILL_CENTER` | 2517–2517 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2518–2518 |  |
| `INFILL_NEG` | 2519–2519 |  |
| `infillColorAt` | 2520–2524 |  |
| `infillPlaneLayer` | 2525–2539 |  |
| `fmtFar` | 2540–2549 |  |
| `AMENITY_HIGHLIGHT_COLOR` | 2550–2550 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2551–2605 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2606–2613 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2614–2628 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2629–2649 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2650–2650 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2651–2665 |  |
| `chgT` | 2666–2675 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2676–2706 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2707–2795 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2796–2803 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2804–2804 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2805–2812 |  |
| `deviationRate` | 2813–2855 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2856–2856 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 2857–2886 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 2887–2893 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 2894–2905 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 2906–2909 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 2910–2914 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 2915–2925 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 2926–2941 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 2942–2968 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `INST_OUTLINE_COLOR` | 2969–3021 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 3022–3026 |  |
| `bandHover` | 3027–3035 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3036–3132 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3133–3140 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3141–3142 |  |
| `glassInstBandLayers` | 3143–3171 |  |
| `deviationRateExempt` | 3172–3184 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3185–3186 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3187–3188 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3189–3189 |  |
| `deviationStats` | 3190–3234 |  |
| `deviationOf` | 3235–3236 |  |
| `deviationT` | 3237–3247 |  |
| `fmtDeviation` | 3248–3269 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3270–3313 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3314–3400 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3401–3423 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3424–3424 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3425–3445 |  |
| `ensureFireStations` | 3446–3461 |  |
| `TRANSIT_STATION_COLOR` | 3462–3462 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3463–3480 |  |
| `ensureTransitStations` | 3481–3496 |  |
| `TRANSIT_LINE_COLOR` | 3497–3497 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3498–3514 |  |
| `ensureLrtLines` | 3515–3531 |  |
| `BIKE_LINE_COLOR` | 3532–3532 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3533–3549 |  |
| `ensureBikeLines` | 3550–3607 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3608–3608 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3609–3612 |  |
| `BOUNDARY_COLOR` | 3613–3622 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3623–3623 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3624–3636 |  |
| `referenceSplit` | 3637–3664 |  |
| `referenceUnderLayers` | 3665–3699 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3700–3716 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3717–3736 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3737–3749 |  |
| `servicesBlurb` | 3750–3767 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3768–3791 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 3792–3802 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 3803–3854 |  |
| `REF_TIERS` | 3855–3876 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 3877–3884 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 3885–3887 |  |
| `placeAnchors` | 3888–3911 |  |
| `labelPool` | 3912–3919 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 3920–3973 |  |
| `CHROME_IDS` | 3974–3977 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 3978–3996 |  |
| `visibleLabels` | 3997–4051 |  |
| `labelLayer` | 4052–4088 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 4089–4089 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4090–4105 |  |
| `ratioT` | 4106–4116 |  |
| `buildLayers` | 4117–4129 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 4130–4432 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4433–4462 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4463–4466 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4467–4469 |  |
| `fmtBig` | 4470–4497 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4498–4503 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4504–4511 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4512–4516 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4517–4527 |  |
| `revenueLens` | 4528–4529 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4530–4554 |  |
| `SVC_COST_BASES` | 4555–4569 | The Services panel: this hood's revenue per acre set against what the City |
| `serviceLens` | 4570–4570 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4571–4574 |  |
| `servicePanelFor` | 4575–4588 |  |
| `hoodPanelLens` | 4589–4592 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4593–4610 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4611–4642 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 4643–4648 |  |
| `sparklineSvg` | 4649–4664 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 4665–4734 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 4735–4761 |  |
| `openTemporal` | 4762–4790 |  |
| `renderRevenueMix` | 4791–4839 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 4840–4886 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 4887–4889 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 4890–4940 |  |
| `syncPinnedPanel` | 4941–4967 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 4968–4983 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 4984–4994 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 4995–5042 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5043–5048 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5049–5088 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5089–5105 |  |
| `temporalClick` | 5106–5163 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 5164–5244 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 5245–5582 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 5583–5650 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 5651–5651 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 5652–5670 |  |
| `syncMetricButtons` | 5671–5694 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 5695–5701 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 5702–5715 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 5716–5757 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 5758–5800 |  |
| `toggleBudgetPanel` | 5801–5826 |  |
| `syncMillRates` | 5827–5859 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 5860–5881 |  |
| `applyColorAdjust` | 5882–5903 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 5904–5916 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 5917–5932 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 5933–5950 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 5951–5967 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 5968–5983 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 5984–6000 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 6001–6248 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 6249–6259 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 6260–6273 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 6274–6282 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 6283–6293 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 6294–6305 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 6306–6319 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 6320–6340 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 6341–6388 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 6389–6394 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 6395–6416 |  |
| `applyMoneyDetail` | 6417–6441 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 6442–6453 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 6454–6461 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 6462–6480 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 6481–6491 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 6492–6499 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 6500–6516 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 6517–6530 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 6531–6541 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 6542–6785 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 6786–6795 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 6796–6809 |  |
| `applySvcDriver` | 6810–6823 |  |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 6824–7354 | Everything that needs the map surface: fetch the data, mount the deck.gl |

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
| `#revmix` | 4810 |
| `#svccost` | 4859 |
