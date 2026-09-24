# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~8,058-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (310 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 643–647 |  |
| `HOME` | 648–648 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 649–662 |  |
| `WINDOWS` | 663–688 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 689–698 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 699–703 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 704–779 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `money0` | 780–782 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `fmtMoney` | 783–784 |  |
| `METRICS` | 785–887 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 888–904 |  |
| `RATIO_DENOMS` | 905–938 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 939–939 |  |
| `ratioOf` | 940–940 |  |
| `ratioKept` | 941–962 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 963–973 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 974–1001 |  |
| `dominantUse` | 1002–1043 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1044–1214 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1215–1310 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1311–1315 | the Lab: a container for unfinished lenses |
| `inLab` | 1316–1317 |  |
| `DEVIATION_TITLES` | 1318–1322 |  |
| `deviationTitle` | 1323–1328 |  |
| `deviationKind` | 1329–1331 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1332–1339 |  |
| `changeBlurb` | 1340–1360 | Change-lens blurb (COPY_DECISIONS BC1, B8 shape). It follows the window |
| `GLASS_BLURBS` | 1361–1382 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassInstBlurb` | 1383–1395 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1396–1407 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `amenityWhichPhrase` | 1408–1413 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1414–1419 |  |
| `infillAmenityBlurb` | 1420–1433 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1434–1445 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `devTitle` | 1446–1451 | Development blurb, in the COPY_DECISIONS B8 shape (BD1): what the lens |
| `devBlurb` | 1452–1510 |  |
| `setBlurb` | 1511–1523 | Blurb markup (COPY_DECISIONS B8): a blank line starts a new paragraph and |
| `currentBlurb` | 1524–1539 | The active view's blurb. Read by applyView and by the camera's 2D/3D flip |
| `withColourClause` | 1540–1557 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1558–1564 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1565–1578 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1579–1579 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1580–1594 |  |
| `fmtMB` | 1595–1605 |  |
| `showGridBusy` | 1606–1628 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1629–1645 |  |
| `loadGridData` | 1646–1699 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1700–1753 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1754–1778 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1779–1810 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1811–1811 |  |
| `gridFetches` | 1812–1836 |  |
| `RAMPS` | 1837–1877 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1878–1884 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1885–1890 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1891–1891 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1892–1898 |  |
| `AMENITY_BANDS` | 1899–1900 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1901–1903 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1904–1909 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1910–1924 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1925–1930 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1931–1949 |  |
| `gridScale` | 1950–1970 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 1971–1977 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1978–1989 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1990–1992 |  |
| `quantile` | 1993–2007 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 2008–2042 |  |
| `moneyBlurb` | 2043–2054 | The money blurb (COPY_DECISIONS BM1, B8 shape): the metric's own P1 under |
| `fillFor` | 2055–2067 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2068–2146 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2147–2147 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2148–2174 |  |
| `failLoading` | 2175–2188 |  |
| `hideLoading` | 2189–2243 |  |
| `topRings` | 2244–2260 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2261–2286 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2287–2287 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2288–2300 |  |
| `svcT` | 2301–2309 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2310–2323 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2324–2324 |  |
| `fmtFire` | 2325–2326 |  |
| `fmtTransit` | 2327–2328 |  |
| `fmtBike` | 2329–2341 |  |
| `fmtRoadM` | 2342–2355 |  |
| `fmtResShare` | 2356–2358 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2359–2364 |  |
| `fmtRoadsCost` | 2365–2369 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2370–2371 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2372–2373 |  |
| `fmtBikeCost` | 2374–2385 |  |
| `servicePlaneLayer` | 2386–2418 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2419–2428 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2429–2434 |  |
| `DEV_IND_TOTAL` | 2435–2437 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2438–2443 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2444–2448 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2449–2454 |  |
| `devGridOfferable` | 2455–2456 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2457–2457 |  |
| `devCol` | 2458–2458 |  |
| `_devScale` | 2459–2459 |  |
| `devScale` | 2460–2466 |  |
| `devT` | 2467–2470 |  |
| `developmentPlaneLayer` | 2471–2487 |  |
| `fmtDev` | 2488–2503 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2504–2509 |  |
| `DEV_GRID_IND_N` | 2510–2510 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2511–2513 |  |
| `devGridScale` | 2514–2540 |  |
| `devGridLayer` | 2541–2589 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2590–2591 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2592–2599 |  |
| `_infillStats` | 2600–2600 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2601–2618 |  |
| `_infillRaw` | 2619–2621 |  |
| `infillScore` | 2622–2637 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2638–2639 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2640–2657 |  |
| `INFILL_CENTER` | 2658–2658 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2659–2659 |  |
| `INFILL_NEG` | 2660–2660 |  |
| `infillColorAt` | 2661–2665 |  |
| `infillPlaneLayer` | 2666–2687 |  |
| `fmtFar` | 2688–2697 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `AMENITY_HIGHLIGHT_COLOR` | 2698–2698 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2699–2753 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2754–2761 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2762–2776 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2777–2797 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2798–2798 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2799–2813 |  |
| `chgT` | 2814–2823 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2824–2854 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2855–2943 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2944–2951 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2952–2952 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2953–2960 |  |
| `deviationRate` | 2961–3003 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 3004–3004 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 3005–3034 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3035–3041 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3042–3053 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3054–3057 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3058–3062 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3063–3073 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3074–3089 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3090–3121 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3122–3146 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `INST_OUTLINE_COLOR` | 3147–3199 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 3200–3204 |  |
| `bandHover` | 3205–3213 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3214–3310 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3311–3318 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3319–3320 |  |
| `glassInstBandLayers` | 3321–3361 |  |
| `ratioInstBandLayers` | 3362–3389 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3390–3402 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3403–3404 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3405–3406 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3407–3407 |  |
| `deviationStats` | 3408–3452 |  |
| `deviationOf` | 3453–3454 |  |
| `deviationT` | 3455–3465 |  |
| `fmtDeviation` | 3466–3487 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3488–3531 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3532–3618 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3619–3641 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3642–3642 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3643–3663 |  |
| `ensureFireStations` | 3664–3679 |  |
| `TRANSIT_STATION_COLOR` | 3680–3680 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3681–3698 |  |
| `ensureTransitStations` | 3699–3714 |  |
| `TRANSIT_LINE_COLOR` | 3715–3715 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3716–3732 |  |
| `ensureLrtLines` | 3733–3749 |  |
| `BIKE_LINE_COLOR` | 3750–3750 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3751–3767 |  |
| `ensureBikeLines` | 3768–3825 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3826–3826 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3827–3830 |  |
| `BOUNDARY_COLOR` | 3831–3840 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3841–3841 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3842–3854 |  |
| `referenceSplit` | 3855–3882 |  |
| `referenceUnderLayers` | 3883–3917 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3918–3934 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3935–3954 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3955–3967 |  |
| `servicesBlurb` | 3968–3985 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3986–4009 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 4010–4020 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 4021–4072 |  |
| `REF_TIERS` | 4073–4094 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4095–4102 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 4103–4105 |  |
| `placeAnchors` | 4106–4129 |  |
| `labelPool` | 4130–4137 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4138–4191 |  |
| `CHROME_IDS` | 4192–4196 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4197–4215 |  |
| `visibleLabels` | 4216–4270 |  |
| `labelLayer` | 4271–4307 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 4308–4308 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4309–4324 |  |
| `ratioT` | 4325–4347 |  |
| `zMatrix` | 4348–4352 |  |
| `buildLayers` | 4353–4376 |  |
| `flattenDuringEase` | 4377–4401 | Center 2D lowers the heights over the LAST QUARTER OF THE TILT instead |
| `buildViewLayers` | 4402–4711 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4712–4741 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4742–4751 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4752–4754 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 4755–4786 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4787–4793 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4794–4801 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4802–4806 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4807–4817 |  |
| `revenueLens` | 4818–4819 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4820–4852 |  |
| `SVC_COST_BASES` | 4853–4870 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 4871–4879 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 4880–4895 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 4896–4898 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 4899–4905 |  |
| `svcRank` | 4906–4910 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 4911–4917 |  |
| `svcDriverReading` | 4918–4938 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 4939–4939 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4940–4943 |  |
| `servicePanelFor` | 4944–4964 |  |
| `hoodPanelLens` | 4965–4968 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4969–4986 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4987–5018 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 5019–5024 |  |
| `sparklineSvg` | 5025–5040 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 5041–5100 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5101–5106 | Development history: new supply per year |
| `devHistKey` | 5107–5116 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5117–5121 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5122–5122 |  |
| `devHistVerb` | 5123–5128 |  |
| `devHistoryFor` | 5129–5150 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5151–5170 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5171–5190 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5191–5226 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5227–5229 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5230–5293 |  |
| `syncTemporalPos` | 5294–5320 |  |
| `openTemporal` | 5321–5355 |  |
| `renderRevenueMix` | 5356–5422 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 5423–5502 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 5503–5506 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5507–5557 |  |
| `syncPinnedPanel` | 5558–5587 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5588–5603 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5604–5621 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5622–5669 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5670–5675 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5676–5722 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5723–5739 |  |
| `temporalClick` | 5740–5797 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 5798–5866 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 5867–6247 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6248–6329 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6330–6330 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6331–6349 |  |
| `syncMetricButtons` | 6350–6373 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6374–6380 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6381–6394 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6395–6436 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6437–6479 |  |
| `toggleBudgetPanel` | 6480–6505 |  |
| `syncMillRates` | 6506–6538 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 6539–6559 |  |
| `applyColorAdjust` | 6560–6580 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 6581–6593 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 6594–6608 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 6609–6626 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 6627–6643 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 6644–6665 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 6666–6682 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 6683–6922 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 6923–6933 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 6934–6947 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 6948–6956 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 6957–6967 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 6968–6979 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 6980–6992 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 6993–7013 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 7014–7061 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7062–7067 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7068–7089 |  |
| `applyMoneyDetail` | 7090–7114 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7115–7126 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7127–7134 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7135–7153 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7154–7164 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7165–7172 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7173–7189 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7190–7203 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7204–7214 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7215–7458 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7459–7468 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7469–7482 |  |
| `applySvcDriver` | 7483–7496 |  |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 7497–8058 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (968 edges)

⚠️ **A regex reference count, not a call graph** — a name in a comment or string counts, and a nested symbol is attributed to its enclosing range. Use it for *what is central* and *would this seam hold*, never as ground truth for a final module boundary.

**Most depended-on** — moving one of these touches everything below it.

| symbol | referenced by | section |
|---|---|---|
| `state` | 119 | the Lab: a container for unfinished lenses |
| `buildLayers` | 37 | geographic reference layers (all views) |
| `METRICS` | 16 | tunables |
| `applyView` | 15 | control appliers + the view/legend dispatchers |
| `setBlurb` | 15 | the Lab: a container for unfinished lenses |
| `SERVICES` | 14 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `refreshLegend` | 14 | control appliers + the view/legend dispatchers |
| `CELLS` | 10 | tunables |
| `quantile` | 10 | the Lab: a container for unfinished lenses |
| `ratioDenom` | 9 | services lens views (SPEC_services.md display architecture) |
| `ratioScale` | 9 | geographic reference layers (all views) |
| `deviationStats` | 9 | the same doubt, at 100 m |
| `devIndustrial` | 8 | loading overlay |
| `devCol` | 8 | loading overlay |
| `exemptFrac` | 8 | the institutional uncertainty band |

**Section self-containment** — share of each section's outgoing edges that stay inside it. Low means a module cut on this banner would mostly import its neighbours.

| section | edges | self-contained |
|---|---|---|
| uses view (use-mix, 2026-07-03) | 3 | 67% |
| Infill lens (SPEC_development.md Lens B) | 27 | 67% |
| deviation lens: revenue per developed acre against peer average | 3 | 67% |
| the Lab: a container for unfinished lenses | 118 | 64% |
| tunables | 13 | 46% |
| Development 100 m detail grid (layers-panel toggle, 2026-07-15) | 9 | 44% |
| change lens: how each hood's share of the assessment base moved | 16 | 44% |
| geographic reference layers (all views) | 92 | 43% |
| loading overlay | 55 | 35% |
| two tiers, answering two different questions | 29 | 31% |
| Money's revenue panel: where a hood's levy comes from | 34 | 26% |
| the same doubt, at 100 m | 61 | 26% |
| services lens views (SPEC_services.md display architecture) | 4 | 25% |
| Development history: new supply per year | 194 | 24% |
| control appliers + the view/legend dispatchers | 216 | 20% |
| the citywide budget panel (EXPERIMENTAL, full build only) | 12 | 8% |
| services view (SPEC_services.md UI generalization, 2026-07-05) | 17 | 0% |
| the institutional uncertainty band | 2 | 0% |
| temporal lens (SPEC_temporal.md phase 3) | 4 | 0% |
| boot | 59 | 0% |

## Element ids (128) — the control surface

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
| `#gridbusy` | 53 |
| `#gridbusy-spinner` | 54 |
| `#gridbusy-text` | 56 |
| `#gridbusy-size` | 57 |
| `#title` | 61 |
| `#title-h` | 62 |
| `#title-p` | 65 |
| `#temporal` | 75 |
| `#temporal-close` | 76 |
| `#temporal-name` | 77 |
| `#temporal-body` | 84 |
| `#temporal-chart` | 85 |
| `#temporal-read` | 86 |
| `#temporal-note` | 87 |
| `#temporal-hint` | 91 |
| `#millrates` | 107 |
| `#mill-head` | 108 |
| `#mill-rows` | 109 |
| `#mill-note` | 110 |
| `#budget` | 124 |
| `#budget-close` | 131 |
| `#budget-head` | 132 |
| `#budget-body` | 137 |
| `#budget-rows` | 138 |
| `#budget-other-hd` | 139 |
| `#budget-other` | 140 |
| `#budget-note` | 141 |
| `#peek` | 156 |
| `#peek-name` | 157 |
| `#peek-read` | 158 |
| `#peek-go` | 159 |
| `#controls` | 162 |
| `#toggle` | 175 |
| `#metric-row` | 176 |
| `#revcut` | 180 |
| `#moneymode` | 185 |
| `#views` | 191 |
| `#optpanel` | 205 |
| `#opt-fold` | 206 |
| `#opt-caret` | 206 |
| `#opt-body` | 207 |
| `#layers` | 208 |
| `#chgwindow-hd` | 209 |
| `#chgwindow` | 210 |
| `#labpick-hd` | 219 |
| `#labpick` | 220 |
| `#labcut-hd` | 221 |
| `#labcut` | 222 |
| `#moneydetail-hd` | 227 |
| `#moneydetail` | 228 |
| `#amenity-hd` | 253 |
| `#amenity` | 254 |
| `#amenity-lrt-row` | 255 |
| `#amenity-lrt-on` | 256 |
| `#amenity-school-row` | 258 |
| `#amenity-school-on` | 259 |
| `#uses-prisms-hd` | 262 |
| `#uses-prisms` | 263 |
| `#uses-prisms-on` | 265 |
| `#devmode-hd` | 268 |
| `#devmode` | 269 |
| `#devmetric-hd` | 273 |
| `#devmetric` | 274 |
| `#devwindow-hd` | 279 |
| `#devwindow` | 280 |
| `#devdetail-hd` | 285 |
| `#devdetail` | 286 |
| `#prism-hd` | 290 |
| `#prism-row` | 291 |
| `#prism-opacity` | 293 |
| `#prism-opacity-val` | 294 |
| `#services-hd` | 296 |
| `#services` | 297 |
| `#denom-hd` | 396 |
| `#denom` | 397 |
| `#ratio-denom-hd` | 401 |
| `#ratio-denom` | 402 |
| `#hoodmode` | 412 |
| `#hoodmode-btn` | 413 |
| `#coloradj` | 425 |
| `#coloradj-btn` | 426 |
| `#budget-pod` | 433 |
| `#budget-btn` | 434 |
| `#a11y` | 438 |
| `#a11y-btn` | 439 |
| `#a11y-menu` | 440 |
| `#palette` | 442 |
| `#labels-on` | 449 |
| `#reference-on` | 457 |
| `#about` | 462 |
| `#about-btn` | 463 |
| `#about-menu` | 464 |
| `#about-src-roads` | 476 |
| `#about-src-services` | 477 |
| `#about-vintage` | 505 |
| `#about-build` | 509 |
| `#about-modelled-roads` | 523 |
| `#about-modelled` | 541 |
| `#about-budget` | 551 |
| `#about-budget-lead` | 553 |
| `#about-budget-rows` | 554 |
| `#about-budget-note` | 555 |
| `#about-updated` | 566 |
| `#botleft` | 570 |
| `#compass` | 571 |
| `#rot-ccw` | 572 |
| `#tonorth` | 579 |
| `#needle` | 581 |
| `#rot-cw` | 586 |
| `#viewbtns` | 594 |
| `#recenter` | 596 |
| `#center2d` | 597 |
| `#legend` | 599 |
| `#legend-label` | 600 |
| `#legend-min` | 602 |
| `#legend-max` | 602 |
| `#legend-cats` | 604 |
| `#revmix` | 5375 |
| `#svccost` | 5466 |
