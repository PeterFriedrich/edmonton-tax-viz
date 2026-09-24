# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~8,048-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

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
| `changeBlurb` | 1340–1357 | Change-lens blurb (COPY_DECISIONS BC1, B8 shape). It follows the window |
| `glassLead` | 1358–1370 | Grid blurb (COPY_DECISIONS BG1, B8 shape). Names the metric (B6) and the |
| `glassInstBlurb` | 1371–1383 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1384–1395 | Ratio's azure needs the same sentence as Glass's, for the same reason |
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
| `gridFetches` | 1802–1826 |  |
| `RAMPS` | 1827–1867 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1868–1874 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1875–1880 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1881–1881 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1882–1888 |  |
| `AMENITY_BANDS` | 1889–1890 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1891–1893 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1894–1899 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1900–1914 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1915–1920 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1921–1939 |  |
| `gridScale` | 1940–1960 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 1961–1967 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1968–1979 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1980–1982 |  |
| `quantile` | 1983–1997 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1998–2032 |  |
| `moneyBlurb` | 2033–2044 | The money blurb (COPY_DECISIONS BM1, B8 shape): the metric's own P1 under |
| `fillFor` | 2045–2057 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2058–2136 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2137–2137 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2138–2164 |  |
| `failLoading` | 2165–2178 |  |
| `hideLoading` | 2179–2233 |  |
| `topRings` | 2234–2250 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2251–2276 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2277–2277 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2278–2290 |  |
| `svcT` | 2291–2299 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2300–2313 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2314–2314 |  |
| `fmtFire` | 2315–2316 |  |
| `fmtTransit` | 2317–2318 |  |
| `fmtBike` | 2319–2331 |  |
| `fmtRoadM` | 2332–2345 |  |
| `fmtResShare` | 2346–2348 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2349–2354 |  |
| `fmtRoadsCost` | 2355–2359 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2360–2361 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2362–2363 |  |
| `fmtBikeCost` | 2364–2375 |  |
| `servicePlaneLayer` | 2376–2408 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2409–2418 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2419–2424 |  |
| `DEV_IND_TOTAL` | 2425–2427 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2428–2433 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2434–2438 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2439–2444 |  |
| `devGridOfferable` | 2445–2446 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2447–2447 |  |
| `devCol` | 2448–2448 |  |
| `_devScale` | 2449–2449 |  |
| `devScale` | 2450–2456 |  |
| `devT` | 2457–2460 |  |
| `developmentPlaneLayer` | 2461–2477 |  |
| `fmtDev` | 2478–2493 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2494–2499 |  |
| `DEV_GRID_IND_N` | 2500–2500 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2501–2503 |  |
| `devGridScale` | 2504–2530 |  |
| `devGridLayer` | 2531–2579 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2580–2581 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2582–2589 |  |
| `_infillStats` | 2590–2590 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2591–2608 |  |
| `_infillRaw` | 2609–2611 |  |
| `infillScore` | 2612–2627 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2628–2629 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2630–2647 |  |
| `INFILL_CENTER` | 2648–2648 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2649–2649 |  |
| `INFILL_NEG` | 2650–2650 |  |
| `infillColorAt` | 2651–2655 |  |
| `infillPlaneLayer` | 2656–2677 |  |
| `fmtFar` | 2678–2687 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `AMENITY_HIGHLIGHT_COLOR` | 2688–2688 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2689–2743 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2744–2751 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2752–2766 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2767–2787 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2788–2788 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2789–2803 |  |
| `chgT` | 2804–2813 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2814–2844 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2845–2933 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2934–2941 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2942–2942 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2943–2950 |  |
| `deviationRate` | 2951–2993 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2994–2994 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 2995–3024 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3025–3031 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3032–3043 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3044–3047 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3048–3052 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3053–3063 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3064–3079 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3080–3111 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3112–3136 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `INST_OUTLINE_COLOR` | 3137–3189 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 3190–3194 |  |
| `bandHover` | 3195–3203 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3204–3300 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3301–3308 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3309–3310 |  |
| `glassInstBandLayers` | 3311–3351 |  |
| `ratioInstBandLayers` | 3352–3379 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3380–3392 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3393–3394 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3395–3396 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3397–3397 |  |
| `deviationStats` | 3398–3442 |  |
| `deviationOf` | 3443–3444 |  |
| `deviationT` | 3445–3455 |  |
| `fmtDeviation` | 3456–3477 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3478–3521 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3522–3608 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3609–3631 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3632–3632 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3633–3653 |  |
| `ensureFireStations` | 3654–3669 |  |
| `TRANSIT_STATION_COLOR` | 3670–3670 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3671–3688 |  |
| `ensureTransitStations` | 3689–3704 |  |
| `TRANSIT_LINE_COLOR` | 3705–3705 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3706–3722 |  |
| `ensureLrtLines` | 3723–3739 |  |
| `BIKE_LINE_COLOR` | 3740–3740 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3741–3757 |  |
| `ensureBikeLines` | 3758–3815 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3816–3816 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3817–3820 |  |
| `BOUNDARY_COLOR` | 3821–3830 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3831–3831 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3832–3844 |  |
| `referenceSplit` | 3845–3872 |  |
| `referenceUnderLayers` | 3873–3907 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3908–3924 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3925–3944 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3945–3957 |  |
| `servicesBlurb` | 3958–3975 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3976–3999 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 4000–4010 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 4011–4062 |  |
| `REF_TIERS` | 4063–4084 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4085–4092 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 4093–4095 |  |
| `placeAnchors` | 4096–4119 |  |
| `labelPool` | 4120–4127 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4128–4181 |  |
| `CHROME_IDS` | 4182–4186 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4187–4205 |  |
| `visibleLabels` | 4206–4260 |  |
| `labelLayer` | 4261–4297 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 4298–4298 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4299–4314 |  |
| `ratioT` | 4315–4337 |  |
| `zMatrix` | 4338–4342 |  |
| `buildLayers` | 4343–4366 |  |
| `flattenDuringEase` | 4367–4391 | Center 2D lowers the heights over the LAST QUARTER OF THE TILT instead |
| `buildViewLayers` | 4392–4701 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4702–4731 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4732–4741 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4742–4744 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 4745–4776 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4777–4783 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4784–4791 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4792–4796 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4797–4807 |  |
| `revenueLens` | 4808–4809 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4810–4842 |  |
| `SVC_COST_BASES` | 4843–4860 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 4861–4869 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 4870–4885 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 4886–4888 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 4889–4895 |  |
| `svcRank` | 4896–4900 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 4901–4907 |  |
| `svcDriverReading` | 4908–4928 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 4929–4929 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4930–4933 |  |
| `servicePanelFor` | 4934–4954 |  |
| `hoodPanelLens` | 4955–4958 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4959–4976 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4977–5008 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 5009–5014 |  |
| `sparklineSvg` | 5015–5030 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 5031–5090 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5091–5096 | Development history: new supply per year |
| `devHistKey` | 5097–5106 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5107–5111 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5112–5112 |  |
| `devHistVerb` | 5113–5118 |  |
| `devHistoryFor` | 5119–5140 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5141–5160 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5161–5180 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5181–5216 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5217–5219 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5220–5283 |  |
| `syncTemporalPos` | 5284–5310 |  |
| `openTemporal` | 5311–5345 |  |
| `renderRevenueMix` | 5346–5412 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 5413–5492 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 5493–5496 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5497–5547 |  |
| `syncPinnedPanel` | 5548–5577 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5578–5593 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5594–5611 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5612–5659 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5660–5665 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5666–5712 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5713–5729 |  |
| `temporalClick` | 5730–5787 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 5788–5856 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 5857–6237 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6238–6319 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6320–6320 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6321–6339 |  |
| `syncMetricButtons` | 6340–6363 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6364–6370 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6371–6384 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6385–6426 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6427–6469 |  |
| `toggleBudgetPanel` | 6470–6495 |  |
| `syncMillRates` | 6496–6528 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 6529–6549 |  |
| `applyColorAdjust` | 6550–6570 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 6571–6583 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 6584–6598 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 6599–6616 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 6617–6633 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 6634–6655 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 6656–6672 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 6673–6912 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 6913–6923 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 6924–6937 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 6938–6946 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 6947–6957 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 6958–6969 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 6970–6982 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 6983–7003 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 7004–7051 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7052–7057 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7058–7079 |  |
| `applyMoneyDetail` | 7080–7104 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7105–7116 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7117–7124 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7125–7143 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7144–7154 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7155–7162 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7163–7179 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7180–7193 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7194–7204 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7205–7448 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7449–7458 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7459–7472 |  |
| `applySvcDriver` | 7473–7486 |  |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 7487–8048 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (968 edges)

⚠️ **A regex reference count, not a call graph** — a name in a comment or string counts, and a nested symbol is attributed to its enclosing range. Use it for *what is central* and *would this seam hold*, never as ground truth for a final module boundary.

**Most depended-on** — moving one of these touches everything below it.

| symbol | referenced by | section |
|---|---|---|
| `state` | 119 | the Lab: a container for unfinished lenses |
| `buildLayers` | 37 | geographic reference layers (all views) |
| `METRICS` | 17 | tunables |
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
| `#revmix` | 5365 |
| `#svccost` | 5456 |
