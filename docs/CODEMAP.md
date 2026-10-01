# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~8,328-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (320 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 657–661 |  |
| `HOME` | 662–662 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 663–676 |  |
| `WINDOWS` | 677–702 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 703–712 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 713–717 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 718–793 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `money0` | 794–796 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `fmtMoney` | 797–798 |  |
| `METRICS` | 799–901 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 902–918 |  |
| `RATIO_DENOMS` | 919–952 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 953–953 |  |
| `ratioOf` | 954–954 |  |
| `ratioKept` | 955–976 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 977–987 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 988–1015 |  |
| `dominantUse` | 1016–1057 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1058–1208 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1209–1304 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1305–1309 | the Lab: a container for unfinished lenses |
| `inLab` | 1310–1311 |  |
| `DEVIATION_TITLES` | 1312–1316 |  |
| `deviationTitle` | 1317–1322 |  |
| `deviationKind` | 1323–1325 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1326–1333 |  |
| `changeBlurb` | 1334–1351 | Change-lens blurb (COPY_DECISIONS BC1, B8 shape). It follows the window |
| `glassLead` | 1352–1364 | Grid blurb (COPY_DECISIONS BG1, B8 shape). Names the metric (B6) and the |
| `glassInstBlurb` | 1365–1377 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1378–1386 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `ratioBlurb` | 1387–1395 | Ratio blurb (COPY_DECISIONS BR1, B8 shape): the denominator's P1, a |
| `amenityWhichPhrase` | 1396–1401 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1402–1409 |  |
| `infillAmenityBlurb` | 1410–1423 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1424–1435 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `devTitle` | 1436–1441 | Development blurb, in the COPY_DECISIONS B8 shape (BD1): what the lens |
| `devBlurb` | 1442–1500 |  |
| `setBlurb` | 1501–1513 | Blurb markup (COPY_DECISIONS B8): a blank line starts a new paragraph and |
| `currentBlurb` | 1514–1529 | The active view's blurb. Read by applyView and by the camera's 2D/3D flip |
| `withColourClause` | 1530–1547 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1548–1554 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1555–1568 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1569–1569 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1570–1584 |  |
| `fmtMB` | 1585–1595 |  |
| `showGridBusy` | 1596–1618 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1619–1635 |  |
| `loadGridData` | 1636–1689 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1690–1743 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1744–1768 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1769–1800 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1801–1801 |  |
| `gridFetches` | 1802–1827 |  |
| `RAMPS` | 1828–1868 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1869–1875 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1876–1881 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1882–1882 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1883–1889 |  |
| `AMENITY_BANDS` | 1890–1891 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1892–1894 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1895–1900 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1901–1915 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1916–1921 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1922–1940 |  |
| `gridScale` | 1941–1961 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 1962–1968 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1969–1980 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1981–1983 |  |
| `quantile` | 1984–1998 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1999–2033 |  |
| `moneyBlurb` | 2034–2045 | The money blurb (COPY_DECISIONS BM1, B8 shape): the metric's own P1 under |
| `fillFor` | 2046–2058 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2059–2137 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2138–2138 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2139–2165 |  |
| `failLoading` | 2166–2179 |  |
| `hideLoading` | 2180–2234 |  |
| `topRings` | 2235–2251 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2252–2277 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2278–2278 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2279–2291 |  |
| `svcT` | 2292–2300 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2301–2314 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2315–2315 |  |
| `fmtFire` | 2316–2317 |  |
| `fmtTransit` | 2318–2319 |  |
| `fmtBike` | 2320–2332 |  |
| `fmtRoadM` | 2333–2346 |  |
| `fmtResShare` | 2347–2349 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2350–2355 |  |
| `fmtRoadsCost` | 2356–2360 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2361–2362 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2363–2364 |  |
| `fmtBikeCost` | 2365–2376 |  |
| `servicePlaneLayer` | 2377–2409 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2410–2419 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2420–2425 |  |
| `DEV_IND_TOTAL` | 2426–2428 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2429–2434 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2435–2439 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2440–2445 |  |
| `devGridOfferable` | 2446–2447 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2448–2448 |  |
| `devCol` | 2449–2449 |  |
| `_devScale` | 2450–2450 |  |
| `devScale` | 2451–2457 |  |
| `devT` | 2458–2461 |  |
| `developmentPlaneLayer` | 2462–2478 |  |
| `fmtDev` | 2479–2494 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2495–2500 |  |
| `DEV_GRID_IND_N` | 2501–2501 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2502–2504 |  |
| `devGridScale` | 2505–2531 |  |
| `devGridLayer` | 2532–2580 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2581–2582 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2583–2590 |  |
| `_infillStats` | 2591–2591 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2592–2609 |  |
| `_infillRaw` | 2610–2612 |  |
| `infillScore` | 2613–2628 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2629–2630 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2631–2648 |  |
| `INFILL_CENTER` | 2649–2649 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2650–2650 |  |
| `INFILL_NEG` | 2651–2651 |  |
| `infillColorAt` | 2652–2656 |  |
| `infillPlaneLayer` | 2657–2678 |  |
| `fmtFar` | 2679–2688 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `AMENITY_HIGHLIGHT_COLOR` | 2689–2689 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2690–2744 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2745–2752 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2753–2767 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2768–2788 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2789–2789 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2790–2804 |  |
| `chgT` | 2805–2814 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2815–2845 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2846–2934 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2935–2942 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2943–2943 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2944–2951 |  |
| `deviationRate` | 2952–2994 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2995–2995 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 2996–3025 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3026–3032 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3033–3044 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3045–3048 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3049–3053 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3054–3064 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3065–3080 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3081–3112 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3113–3137 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `INST_OUTLINE_COLOR` | 3138–3190 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 3191–3195 |  |
| `bandHover` | 3196–3204 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3205–3307 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3308–3315 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3316–3317 |  |
| `glassInstBandLayers` | 3318–3358 |  |
| `ratioInstBandLayers` | 3359–3386 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3387–3399 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3400–3401 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3402–3403 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3404–3404 |  |
| `deviationStats` | 3405–3449 |  |
| `deviationOf` | 3450–3451 |  |
| `deviationT` | 3452–3462 |  |
| `fmtDeviation` | 3463–3484 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3485–3528 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3529–3615 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3616–3638 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3639–3639 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3640–3660 |  |
| `ensureFireStations` | 3661–3676 |  |
| `TRANSIT_STATION_COLOR` | 3677–3677 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3678–3695 |  |
| `ensureTransitStations` | 3696–3711 |  |
| `TRANSIT_LINE_COLOR` | 3712–3712 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3713–3729 |  |
| `ensureLrtLines` | 3730–3746 |  |
| `BIKE_LINE_COLOR` | 3747–3747 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3748–3764 |  |
| `ensureBikeLines` | 3765–3822 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3823–3823 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3824–3827 |  |
| `BOUNDARY_COLOR` | 3828–3837 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3838–3838 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3839–3851 |  |
| `referenceSplit` | 3852–3879 |  |
| `referenceUnderLayers` | 3880–3914 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3915–3931 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3932–3951 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3952–3965 |  |
| `servicesBlurb` | 3966–3977 | Services-view blurb (COPY_DECISIONS BS1, B8 shape): the colour-driving |
| `hoodHoverLayer` | 3978–4001 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 4002–4012 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 4013–4064 |  |
| `REF_TIERS` | 4065–4086 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4087–4094 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 4095–4097 |  |
| `placeAnchors` | 4098–4121 |  |
| `labelPool` | 4122–4129 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4130–4183 |  |
| `CHROME_IDS` | 4184–4188 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4189–4207 |  |
| `visibleLabels` | 4208–4262 |  |
| `labelLayer` | 4263–4299 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 4300–4300 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4301–4316 |  |
| `ratioT` | 4317–4339 |  |
| `zMatrix` | 4340–4344 |  |
| `buildLayers` | 4345–4368 |  |
| `flattenDuringEase` | 4369–4393 | Center 2D lowers the heights over the LAST QUARTER OF THE TILT instead |
| `buildViewLayers` | 4394–4703 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4704–4733 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4734–4743 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4744–4746 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 4747–4778 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4779–4785 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4786–4793 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4794–4798 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4799–4809 |  |
| `revenueLens` | 4810–4811 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4812–4844 |  |
| `SVC_COST_BASES` | 4845–4862 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 4863–4871 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 4872–4881 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 4882–4884 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 4885–4891 |  |
| `svcRank` | 4892–4896 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 4897–4903 |  |
| `svcDriverReading` | 4904–4924 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 4925–4925 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4926–4929 |  |
| `servicePanelFor` | 4930–4934 |  |
| `ratioPanelFor` | 4935–4958 | Ratio carries the cost-as-a-share-of-tax panel that Services had until |
| `hoodPanelLens` | 4959–4963 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4964–4981 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4982–5013 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 5014–5019 |  |
| `sparklineSvg` | 5020–5035 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 5036–5095 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5096–5101 | Development history: new supply per year |
| `devHistKey` | 5102–5111 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5112–5116 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5117–5117 |  |
| `devHistVerb` | 5118–5123 |  |
| `devHistoryFor` | 5124–5159 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5160–5179 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5180–5199 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5200–5235 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5236–5238 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5239–5302 |  |
| `syncTemporalPos` | 5303–5329 |  |
| `openTemporal` | 5330–5366 |  |
| `renderRevenueMix` | 5367–5436 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderRatioCost` | 5437–5511 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `renderServiceCost` | 5512–5569 | The Services panel: what each cost IS for this hood, in dollars, and where |
| `fmtSvcRatio` | 5570–5573 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5574–5624 |  |
| `syncPinnedPanel` | 5625–5658 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5659–5674 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5675–5692 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5693–5740 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5741–5746 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5747–5794 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5795–5811 |  |
| `temporalClick` | 5812–5869 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 5870–5938 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 5939–6316 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6317–6406 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6407–6407 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6408–6426 |  |
| `syncMetricButtons` | 6427–6450 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6451–6457 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6458–6471 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6472–6513 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6514–6556 |  |
| `toggleBudgetPanel` | 6557–6582 |  |
| `syncMillRates` | 6583–6615 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 6616–6636 |  |
| `applyColorAdjust` | 6637–6657 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 6658–6670 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 6671–6685 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 6686–6703 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 6704–6720 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 6721–6742 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 6743–6759 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 6760–6999 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 7000–7010 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 7011–7024 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 7025–7033 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 7034–7044 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 7045–7056 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 7057–7069 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 7070–7090 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 7091–7138 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7139–7144 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7145–7166 |  |
| `applyMoneyDetail` | 7167–7191 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7192–7203 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7204–7211 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7212–7230 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7231–7241 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7242–7249 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7250–7266 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7267–7280 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7281–7291 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7292–7535 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7536–7545 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7546–7559 |  |
| `applySvcDriver` | 7560–7592 |  |

### shareable URL: the hash names the view on screen

| symbol | lines | what it does |
|---|---|---|
| `METRIC_FROM_URL` | 7593–7595 |  |
| `urlHash` | 7596–7636 |  |
| `shareLink` | 7637–7645 | Absolute on purpose: the full build carries <base href="../">, and a |
| `copyShareLink` | 7646–7657 | With no clipboard (an insecure origin, a denied permission) the link goes |
| `offered` | 7658–7664 | On screen, ignoring the Options fold: a folded panel on a phone hides |
| `applyUrlState` | 7665–7737 |  |
| `restoreFromHash` | 7738–7756 | Once, at the end of boot, after every build and data gate has run. The |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 7757–8328 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (1028 edges)

⚠️ **A regex reference count, not a call graph** — a name in a comment or string counts, and a nested symbol is attributed to its enclosing range. Use it for *what is central* and *would this seam hold*, never as ground truth for a final module boundary.

**Most depended-on** — moving one of these touches everything below it.

| symbol | referenced by | section |
|---|---|---|
| `state` | 122 | the Lab: a container for unfinished lenses |
| `buildLayers` | 37 | geographic reference layers (all views) |
| `METRICS` | 17 | tunables |
| `applyView` | 17 | control appliers + the view/legend dispatchers |
| `SERVICES` | 16 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `setBlurb` | 15 | the Lab: a container for unfinished lenses |
| `refreshLegend` | 14 | control appliers + the view/legend dispatchers |
| `CELLS` | 11 | tunables |
| `quantile` | 10 | the Lab: a container for unfinished lenses |
| `ratioDenom` | 9 | services lens views (SPEC_services.md display architecture) |
| `ratioScale` | 9 | geographic reference layers (all views) |
| `deviationStats` | 9 | the same doubt, at 100 m |
| `esc` | 9 | money view (default): the classic metric prisms |
| `devIndustrial` | 8 | loading overlay |
| `devCol` | 8 | loading overlay |

**Section self-containment** — share of each section's outgoing edges that stay inside it. Low means a module cut on this banner would mostly import its neighbours.

| section | edges | self-contained |
|---|---|---|
| uses view (use-mix, 2026-07-03) | 3 | 67% |
| Infill lens (SPEC_development.md Lens B) | 27 | 67% |
| deviation lens: revenue per developed acre against peer average | 3 | 67% |
| the Lab: a container for unfinished lenses | 121 | 63% |
| tunables | 13 | 46% |
| Development 100 m detail grid (layers-panel toggle, 2026-07-15) | 9 | 44% |
| change lens: how each hood's share of the assessment base moved | 16 | 44% |
| geographic reference layers (all views) | 92 | 43% |
| loading overlay | 55 | 35% |
| two tiers, answering two different questions | 29 | 31% |
| Money's revenue panel: where a hood's levy comes from | 35 | 29% |
| the same doubt, at 100 m | 61 | 26% |
| Development history: new supply per year | 215 | 23% |
| shareable URL: the hash names the view on screen | 24 | 21% |
| services lens views (SPEC_services.md display architecture) | 5 | 20% |
| control appliers + the view/legend dispatchers | 221 | 20% |
| the citywide budget panel (EXPERIMENTAL, full build only) | 12 | 8% |
| services view (SPEC_services.md UI generalization, 2026-07-05) | 18 | 0% |
| the institutional uncertainty band | 2 | 0% |
| temporal lens (SPEC_temporal.md phase 3) | 4 | 0% |
| boot | 63 | 0% |

## Element ids (131) — the control surface

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
| `#share` | 441 |
| `#share-btn` | 442 |
| `#a11y` | 445 |
| `#a11y-btn` | 446 |
| `#a11y-menu` | 447 |
| `#palette` | 449 |
| `#labels-on` | 456 |
| `#reference-on` | 464 |
| `#about` | 469 |
| `#about-btn` | 470 |
| `#about-menu` | 471 |
| `#about-src-roads` | 483 |
| `#about-src-services` | 484 |
| `#about-vintage` | 512 |
| `#about-build` | 516 |
| `#about-lot-acres` | 521 |
| `#about-modelled-roads` | 532 |
| `#about-modelled` | 554 |
| `#about-budget` | 564 |
| `#about-budget-lead` | 566 |
| `#about-budget-rows` | 567 |
| `#about-budget-note` | 568 |
| `#about-updated` | 580 |
| `#botleft` | 584 |
| `#compass` | 585 |
| `#rot-ccw` | 586 |
| `#tonorth` | 593 |
| `#needle` | 595 |
| `#rot-cw` | 600 |
| `#viewbtns` | 608 |
| `#recenter` | 610 |
| `#center2d` | 611 |
| `#legend` | 613 |
| `#legend-label` | 614 |
| `#legend-min` | 616 |
| `#legend-max` | 616 |
| `#legend-cats` | 618 |
| `#revmix` | 5386 |
| `#svccost` | 5480 |
