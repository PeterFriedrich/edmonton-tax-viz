# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~8,059-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (310 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 644–648 |  |
| `HOME` | 649–649 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 650–663 |  |
| `WINDOWS` | 664–689 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 690–699 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 700–704 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 705–780 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `money0` | 781–783 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `fmtMoney` | 784–785 |  |
| `METRICS` | 786–888 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 889–905 |  |
| `RATIO_DENOMS` | 906–939 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 940–940 |  |
| `ratioOf` | 941–941 |  |
| `ratioKept` | 942–963 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 964–974 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 975–1002 |  |
| `dominantUse` | 1003–1044 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1045–1215 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1216–1311 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1312–1316 | the Lab: a container for unfinished lenses |
| `inLab` | 1317–1318 |  |
| `DEVIATION_TITLES` | 1319–1323 |  |
| `deviationTitle` | 1324–1329 |  |
| `deviationKind` | 1330–1332 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1333–1340 |  |
| `changeBlurb` | 1341–1361 | Change-lens blurb (COPY_DECISIONS BC1, B8 shape). It follows the window |
| `GLASS_BLURBS` | 1362–1383 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassInstBlurb` | 1384–1396 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1397–1408 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `amenityWhichPhrase` | 1409–1414 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1415–1420 |  |
| `infillAmenityBlurb` | 1421–1434 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1435–1446 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `devTitle` | 1447–1452 | Development blurb, in the COPY_DECISIONS B8 shape (BD1): what the lens |
| `devBlurb` | 1453–1511 |  |
| `setBlurb` | 1512–1524 | Blurb markup (COPY_DECISIONS B8): a blank line starts a new paragraph and |
| `currentBlurb` | 1525–1540 | The active view's blurb. Read by applyView and by the camera's 2D/3D flip |
| `withColourClause` | 1541–1558 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1559–1565 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1566–1579 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1580–1580 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1581–1595 |  |
| `fmtMB` | 1596–1606 |  |
| `showGridBusy` | 1607–1629 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1630–1646 |  |
| `loadGridData` | 1647–1700 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1701–1754 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1755–1779 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1780–1811 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1812–1812 |  |
| `gridFetches` | 1813–1837 |  |
| `RAMPS` | 1838–1878 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1879–1885 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1886–1891 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1892–1892 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1893–1899 |  |
| `AMENITY_BANDS` | 1900–1901 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1902–1904 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1905–1910 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1911–1925 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1926–1931 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1932–1950 |  |
| `gridScale` | 1951–1971 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 1972–1978 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1979–1990 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1991–1993 |  |
| `quantile` | 1994–2008 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 2009–2043 |  |
| `moneyBlurb` | 2044–2055 | The money blurb (COPY_DECISIONS BM1, B8 shape): the metric's own P1 under |
| `fillFor` | 2056–2068 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2069–2147 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2148–2148 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2149–2175 |  |
| `failLoading` | 2176–2189 |  |
| `hideLoading` | 2190–2244 |  |
| `topRings` | 2245–2261 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2262–2287 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2288–2288 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2289–2301 |  |
| `svcT` | 2302–2310 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2311–2324 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2325–2325 |  |
| `fmtFire` | 2326–2327 |  |
| `fmtTransit` | 2328–2329 |  |
| `fmtBike` | 2330–2342 |  |
| `fmtRoadM` | 2343–2356 |  |
| `fmtResShare` | 2357–2359 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2360–2365 |  |
| `fmtRoadsCost` | 2366–2370 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2371–2372 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2373–2374 |  |
| `fmtBikeCost` | 2375–2386 |  |
| `servicePlaneLayer` | 2387–2419 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2420–2429 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2430–2435 |  |
| `DEV_IND_TOTAL` | 2436–2438 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2439–2444 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2445–2449 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2450–2455 |  |
| `devGridOfferable` | 2456–2457 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2458–2458 |  |
| `devCol` | 2459–2459 |  |
| `_devScale` | 2460–2460 |  |
| `devScale` | 2461–2467 |  |
| `devT` | 2468–2471 |  |
| `developmentPlaneLayer` | 2472–2488 |  |
| `fmtDev` | 2489–2504 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2505–2510 |  |
| `DEV_GRID_IND_N` | 2511–2511 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2512–2514 |  |
| `devGridScale` | 2515–2541 |  |
| `devGridLayer` | 2542–2590 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2591–2592 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2593–2600 |  |
| `_infillStats` | 2601–2601 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2602–2619 |  |
| `_infillRaw` | 2620–2622 |  |
| `infillScore` | 2623–2638 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2639–2640 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2641–2658 |  |
| `INFILL_CENTER` | 2659–2659 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2660–2660 |  |
| `INFILL_NEG` | 2661–2661 |  |
| `infillColorAt` | 2662–2666 |  |
| `infillPlaneLayer` | 2667–2688 |  |
| `fmtFar` | 2689–2698 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `AMENITY_HIGHLIGHT_COLOR` | 2699–2699 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2700–2754 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2755–2762 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2763–2777 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2778–2798 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2799–2799 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2800–2814 |  |
| `chgT` | 2815–2824 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2825–2855 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2856–2944 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2945–2952 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2953–2953 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2954–2961 |  |
| `deviationRate` | 2962–3004 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 3005–3005 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 3006–3035 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3036–3042 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3043–3054 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3055–3058 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3059–3063 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3064–3074 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3075–3090 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3091–3122 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3123–3147 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `INST_OUTLINE_COLOR` | 3148–3200 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 3201–3205 |  |
| `bandHover` | 3206–3214 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3215–3311 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3312–3319 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3320–3321 |  |
| `glassInstBandLayers` | 3322–3362 |  |
| `ratioInstBandLayers` | 3363–3390 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3391–3403 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3404–3405 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3406–3407 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3408–3408 |  |
| `deviationStats` | 3409–3453 |  |
| `deviationOf` | 3454–3455 |  |
| `deviationT` | 3456–3466 |  |
| `fmtDeviation` | 3467–3488 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3489–3532 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3533–3619 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3620–3642 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3643–3643 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3644–3664 |  |
| `ensureFireStations` | 3665–3680 |  |
| `TRANSIT_STATION_COLOR` | 3681–3681 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3682–3699 |  |
| `ensureTransitStations` | 3700–3715 |  |
| `TRANSIT_LINE_COLOR` | 3716–3716 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3717–3733 |  |
| `ensureLrtLines` | 3734–3750 |  |
| `BIKE_LINE_COLOR` | 3751–3751 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3752–3768 |  |
| `ensureBikeLines` | 3769–3826 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3827–3827 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3828–3831 |  |
| `BOUNDARY_COLOR` | 3832–3841 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3842–3842 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3843–3855 |  |
| `referenceSplit` | 3856–3883 |  |
| `referenceUnderLayers` | 3884–3918 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3919–3935 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3936–3955 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3956–3968 |  |
| `servicesBlurb` | 3969–3986 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3987–4010 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 4011–4021 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 4022–4073 |  |
| `REF_TIERS` | 4074–4095 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4096–4103 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 4104–4106 |  |
| `placeAnchors` | 4107–4130 |  |
| `labelPool` | 4131–4138 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4139–4192 |  |
| `CHROME_IDS` | 4193–4197 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4198–4216 |  |
| `visibleLabels` | 4217–4271 |  |
| `labelLayer` | 4272–4308 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 4309–4309 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4310–4325 |  |
| `ratioT` | 4326–4348 |  |
| `zMatrix` | 4349–4353 |  |
| `buildLayers` | 4354–4377 |  |
| `flattenDuringEase` | 4378–4402 | Center 2D lowers the heights over the LAST QUARTER OF THE TILT instead |
| `buildViewLayers` | 4403–4712 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4713–4742 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4743–4752 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4753–4755 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 4756–4787 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4788–4794 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4795–4802 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4803–4807 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4808–4818 |  |
| `revenueLens` | 4819–4820 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4821–4853 |  |
| `SVC_COST_BASES` | 4854–4871 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 4872–4880 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 4881–4896 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 4897–4899 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 4900–4906 |  |
| `svcRank` | 4907–4911 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 4912–4918 |  |
| `svcDriverReading` | 4919–4939 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 4940–4940 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4941–4944 |  |
| `servicePanelFor` | 4945–4965 |  |
| `hoodPanelLens` | 4966–4969 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4970–4987 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4988–5019 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 5020–5025 |  |
| `sparklineSvg` | 5026–5041 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 5042–5101 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5102–5107 | Development history: new supply per year |
| `devHistKey` | 5108–5117 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5118–5122 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5123–5123 |  |
| `devHistVerb` | 5124–5129 |  |
| `devHistoryFor` | 5130–5151 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5152–5171 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5172–5191 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5192–5227 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5228–5230 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5231–5294 |  |
| `syncTemporalPos` | 5295–5321 |  |
| `openTemporal` | 5322–5356 |  |
| `renderRevenueMix` | 5357–5423 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 5424–5503 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 5504–5507 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5508–5558 |  |
| `syncPinnedPanel` | 5559–5588 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5589–5604 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5605–5622 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5623–5670 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5671–5676 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5677–5723 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5724–5740 |  |
| `temporalClick` | 5741–5798 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 5799–5867 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 5868–6248 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6249–6330 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6331–6331 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6332–6350 |  |
| `syncMetricButtons` | 6351–6374 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6375–6381 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6382–6395 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6396–6437 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6438–6480 |  |
| `toggleBudgetPanel` | 6481–6506 |  |
| `syncMillRates` | 6507–6539 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 6540–6560 |  |
| `applyColorAdjust` | 6561–6581 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 6582–6594 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 6595–6609 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 6610–6627 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 6628–6644 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 6645–6666 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 6667–6683 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 6684–6923 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 6924–6934 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 6935–6948 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 6949–6957 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 6958–6968 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 6969–6980 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 6981–6993 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 6994–7014 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 7015–7062 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7063–7068 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7069–7090 |  |
| `applyMoneyDetail` | 7091–7115 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7116–7127 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7128–7135 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7136–7154 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7155–7165 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7166–7173 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7174–7190 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7191–7204 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7205–7215 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7216–7459 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7460–7469 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7470–7483 |  |
| `applySvcDriver` | 7484–7497 |  |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 7498–8059 | Everything that needs the map surface: fetch the data, mount the deck.gl |

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
| `#temporal` | 76 |
| `#temporal-close` | 77 |
| `#temporal-name` | 78 |
| `#temporal-body` | 85 |
| `#temporal-chart` | 86 |
| `#temporal-read` | 87 |
| `#temporal-note` | 88 |
| `#temporal-hint` | 92 |
| `#millrates` | 108 |
| `#mill-head` | 109 |
| `#mill-rows` | 110 |
| `#mill-note` | 111 |
| `#budget` | 125 |
| `#budget-close` | 132 |
| `#budget-head` | 133 |
| `#budget-body` | 138 |
| `#budget-rows` | 139 |
| `#budget-other-hd` | 140 |
| `#budget-other` | 141 |
| `#budget-note` | 142 |
| `#peek` | 157 |
| `#peek-name` | 158 |
| `#peek-read` | 159 |
| `#peek-go` | 160 |
| `#controls` | 163 |
| `#toggle` | 176 |
| `#metric-row` | 177 |
| `#revcut` | 181 |
| `#moneymode` | 186 |
| `#views` | 192 |
| `#optpanel` | 206 |
| `#opt-fold` | 207 |
| `#opt-caret` | 207 |
| `#opt-body` | 208 |
| `#layers` | 209 |
| `#chgwindow-hd` | 210 |
| `#chgwindow` | 211 |
| `#labpick-hd` | 220 |
| `#labpick` | 221 |
| `#labcut-hd` | 222 |
| `#labcut` | 223 |
| `#moneydetail-hd` | 228 |
| `#moneydetail` | 229 |
| `#amenity-hd` | 254 |
| `#amenity` | 255 |
| `#amenity-lrt-row` | 256 |
| `#amenity-lrt-on` | 257 |
| `#amenity-school-row` | 259 |
| `#amenity-school-on` | 260 |
| `#uses-prisms-hd` | 263 |
| `#uses-prisms` | 264 |
| `#uses-prisms-on` | 266 |
| `#devmode-hd` | 269 |
| `#devmode` | 270 |
| `#devmetric-hd` | 274 |
| `#devmetric` | 275 |
| `#devwindow-hd` | 280 |
| `#devwindow` | 281 |
| `#devdetail-hd` | 286 |
| `#devdetail` | 287 |
| `#prism-hd` | 291 |
| `#prism-row` | 292 |
| `#prism-opacity` | 294 |
| `#prism-opacity-val` | 295 |
| `#services-hd` | 297 |
| `#services` | 298 |
| `#denom-hd` | 397 |
| `#denom` | 398 |
| `#ratio-denom-hd` | 402 |
| `#ratio-denom` | 403 |
| `#hoodmode` | 413 |
| `#hoodmode-btn` | 414 |
| `#coloradj` | 426 |
| `#coloradj-btn` | 427 |
| `#budget-pod` | 434 |
| `#budget-btn` | 435 |
| `#a11y` | 439 |
| `#a11y-btn` | 440 |
| `#a11y-menu` | 441 |
| `#palette` | 443 |
| `#labels-on` | 450 |
| `#reference-on` | 458 |
| `#about` | 463 |
| `#about-btn` | 464 |
| `#about-menu` | 465 |
| `#about-src-roads` | 477 |
| `#about-src-services` | 478 |
| `#about-vintage` | 506 |
| `#about-build` | 510 |
| `#about-modelled-roads` | 524 |
| `#about-modelled` | 542 |
| `#about-budget` | 552 |
| `#about-budget-lead` | 554 |
| `#about-budget-rows` | 555 |
| `#about-budget-note` | 556 |
| `#about-updated` | 567 |
| `#botleft` | 571 |
| `#compass` | 572 |
| `#rot-ccw` | 573 |
| `#tonorth` | 580 |
| `#needle` | 582 |
| `#rot-cw` | 587 |
| `#viewbtns` | 595 |
| `#recenter` | 597 |
| `#center2d` | 598 |
| `#legend` | 600 |
| `#legend-label` | 601 |
| `#legend-min` | 603 |
| `#legend-max` | 603 |
| `#legend-cats` | 605 |
| `#revmix` | 5376 |
| `#svccost` | 5467 |
