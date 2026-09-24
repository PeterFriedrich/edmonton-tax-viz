# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~8,024-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

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
| `SERVICES` | 1044–1195 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1196–1291 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1292–1296 | the Lab: a container for unfinished lenses |
| `inLab` | 1297–1298 |  |
| `DEVIATION_TITLES` | 1299–1303 |  |
| `deviationTitle` | 1304–1309 |  |
| `deviationKind` | 1310–1312 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1313–1320 |  |
| `changeBlurb` | 1321–1338 | Change-lens blurb (COPY_DECISIONS BC1, B8 shape). It follows the window |
| `glassLead` | 1339–1351 | Grid blurb (COPY_DECISIONS BG1, B8 shape). Names the metric (B6) and the |
| `glassInstBlurb` | 1352–1364 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1365–1376 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `amenityWhichPhrase` | 1377–1382 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1383–1390 |  |
| `infillAmenityBlurb` | 1391–1404 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1405–1416 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `devTitle` | 1417–1422 | Development blurb, in the COPY_DECISIONS B8 shape (BD1): what the lens |
| `devBlurb` | 1423–1481 |  |
| `setBlurb` | 1482–1494 | Blurb markup (COPY_DECISIONS B8): a blank line starts a new paragraph and |
| `currentBlurb` | 1495–1510 | The active view's blurb. Read by applyView and by the camera's 2D/3D flip |
| `withColourClause` | 1511–1528 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1529–1535 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1536–1549 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1550–1550 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1551–1565 |  |
| `fmtMB` | 1566–1576 |  |
| `showGridBusy` | 1577–1599 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1600–1616 |  |
| `loadGridData` | 1617–1670 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1671–1724 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1725–1749 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1750–1781 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1782–1782 |  |
| `gridFetches` | 1783–1807 |  |
| `RAMPS` | 1808–1848 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1849–1855 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1856–1861 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1862–1862 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1863–1869 |  |
| `AMENITY_BANDS` | 1870–1871 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1872–1874 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1875–1880 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1881–1895 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1896–1901 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1902–1920 |  |
| `gridScale` | 1921–1941 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 1942–1948 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1949–1960 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1961–1963 |  |
| `quantile` | 1964–1978 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1979–2013 |  |
| `moneyBlurb` | 2014–2025 | The money blurb (COPY_DECISIONS BM1, B8 shape): the metric's own P1 under |
| `fillFor` | 2026–2038 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2039–2117 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2118–2118 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2119–2145 |  |
| `failLoading` | 2146–2159 |  |
| `hideLoading` | 2160–2214 |  |
| `topRings` | 2215–2231 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2232–2257 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2258–2258 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2259–2271 |  |
| `svcT` | 2272–2280 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2281–2294 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2295–2295 |  |
| `fmtFire` | 2296–2297 |  |
| `fmtTransit` | 2298–2299 |  |
| `fmtBike` | 2300–2312 |  |
| `fmtRoadM` | 2313–2326 |  |
| `fmtResShare` | 2327–2329 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2330–2335 |  |
| `fmtRoadsCost` | 2336–2340 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2341–2342 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2343–2344 |  |
| `fmtBikeCost` | 2345–2356 |  |
| `servicePlaneLayer` | 2357–2389 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2390–2399 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2400–2405 |  |
| `DEV_IND_TOTAL` | 2406–2408 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2409–2414 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2415–2419 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2420–2425 |  |
| `devGridOfferable` | 2426–2427 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2428–2428 |  |
| `devCol` | 2429–2429 |  |
| `_devScale` | 2430–2430 |  |
| `devScale` | 2431–2437 |  |
| `devT` | 2438–2441 |  |
| `developmentPlaneLayer` | 2442–2458 |  |
| `fmtDev` | 2459–2474 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2475–2480 |  |
| `DEV_GRID_IND_N` | 2481–2481 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2482–2484 |  |
| `devGridScale` | 2485–2511 |  |
| `devGridLayer` | 2512–2560 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2561–2562 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2563–2570 |  |
| `_infillStats` | 2571–2571 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2572–2589 |  |
| `_infillRaw` | 2590–2592 |  |
| `infillScore` | 2593–2608 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2609–2610 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2611–2628 |  |
| `INFILL_CENTER` | 2629–2629 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2630–2630 |  |
| `INFILL_NEG` | 2631–2631 |  |
| `infillColorAt` | 2632–2636 |  |
| `infillPlaneLayer` | 2637–2658 |  |
| `fmtFar` | 2659–2668 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `AMENITY_HIGHLIGHT_COLOR` | 2669–2669 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2670–2724 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2725–2732 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2733–2747 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2748–2768 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2769–2769 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2770–2784 |  |
| `chgT` | 2785–2794 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2795–2825 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2826–2914 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2915–2922 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2923–2923 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2924–2931 |  |
| `deviationRate` | 2932–2974 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2975–2975 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 2976–3005 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3006–3012 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3013–3024 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3025–3028 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3029–3033 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3034–3044 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3045–3060 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3061–3092 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3093–3117 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `INST_OUTLINE_COLOR` | 3118–3170 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 3171–3175 |  |
| `bandHover` | 3176–3184 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3185–3281 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3282–3289 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3290–3291 |  |
| `glassInstBandLayers` | 3292–3332 |  |
| `ratioInstBandLayers` | 3333–3360 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3361–3373 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3374–3375 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3376–3377 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3378–3378 |  |
| `deviationStats` | 3379–3423 |  |
| `deviationOf` | 3424–3425 |  |
| `deviationT` | 3426–3436 |  |
| `fmtDeviation` | 3437–3458 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3459–3502 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3503–3589 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3590–3612 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3613–3613 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3614–3634 |  |
| `ensureFireStations` | 3635–3650 |  |
| `TRANSIT_STATION_COLOR` | 3651–3651 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3652–3669 |  |
| `ensureTransitStations` | 3670–3685 |  |
| `TRANSIT_LINE_COLOR` | 3686–3686 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3687–3703 |  |
| `ensureLrtLines` | 3704–3720 |  |
| `BIKE_LINE_COLOR` | 3721–3721 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3722–3738 |  |
| `ensureBikeLines` | 3739–3796 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3797–3797 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3798–3801 |  |
| `BOUNDARY_COLOR` | 3802–3811 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3812–3812 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3813–3825 |  |
| `referenceSplit` | 3826–3853 |  |
| `referenceUnderLayers` | 3854–3888 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3889–3905 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3906–3925 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3926–3939 |  |
| `servicesBlurb` | 3940–3951 | Services-view blurb (COPY_DECISIONS BS1, B8 shape): the colour-driving |
| `hoodHoverLayer` | 3952–3975 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 3976–3986 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 3987–4038 |  |
| `REF_TIERS` | 4039–4060 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4061–4068 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 4069–4071 |  |
| `placeAnchors` | 4072–4095 |  |
| `labelPool` | 4096–4103 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4104–4157 |  |
| `CHROME_IDS` | 4158–4162 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4163–4181 |  |
| `visibleLabels` | 4182–4236 |  |
| `labelLayer` | 4237–4273 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 4274–4274 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4275–4290 |  |
| `ratioT` | 4291–4313 |  |
| `zMatrix` | 4314–4318 |  |
| `buildLayers` | 4319–4342 |  |
| `flattenDuringEase` | 4343–4367 | Center 2D lowers the heights over the LAST QUARTER OF THE TILT instead |
| `buildViewLayers` | 4368–4677 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4678–4707 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4708–4717 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4718–4720 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 4721–4752 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4753–4759 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4760–4767 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4768–4772 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4773–4783 |  |
| `revenueLens` | 4784–4785 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4786–4818 |  |
| `SVC_COST_BASES` | 4819–4836 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 4837–4845 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 4846–4861 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 4862–4864 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 4865–4871 |  |
| `svcRank` | 4872–4876 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 4877–4883 |  |
| `svcDriverReading` | 4884–4904 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 4905–4905 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4906–4909 |  |
| `servicePanelFor` | 4910–4930 |  |
| `hoodPanelLens` | 4931–4934 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4935–4952 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4953–4984 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 4985–4990 |  |
| `sparklineSvg` | 4991–5006 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 5007–5066 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5067–5072 | Development history: new supply per year |
| `devHistKey` | 5073–5082 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5083–5087 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5088–5088 |  |
| `devHistVerb` | 5089–5094 |  |
| `devHistoryFor` | 5095–5116 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5117–5136 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5137–5156 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5157–5192 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5193–5195 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5196–5259 |  |
| `syncTemporalPos` | 5260–5286 |  |
| `openTemporal` | 5287–5321 |  |
| `renderRevenueMix` | 5322–5388 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 5389–5468 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 5469–5472 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5473–5523 |  |
| `syncPinnedPanel` | 5524–5553 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5554–5569 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5570–5587 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5588–5635 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5636–5641 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5642–5688 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5689–5705 |  |
| `temporalClick` | 5706–5763 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 5764–5832 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 5833–6213 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6214–6295 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6296–6296 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6297–6315 |  |
| `syncMetricButtons` | 6316–6339 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6340–6346 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6347–6360 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6361–6402 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6403–6445 |  |
| `toggleBudgetPanel` | 6446–6471 |  |
| `syncMillRates` | 6472–6504 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 6505–6525 |  |
| `applyColorAdjust` | 6526–6546 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 6547–6559 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 6560–6574 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 6575–6592 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 6593–6609 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 6610–6631 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 6632–6648 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 6649–6888 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 6889–6899 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 6900–6913 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 6914–6922 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 6923–6933 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 6934–6945 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 6946–6958 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 6959–6979 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 6980–7027 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7028–7033 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7034–7055 |  |
| `applyMoneyDetail` | 7056–7080 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7081–7092 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7093–7100 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7101–7119 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7120–7130 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7131–7138 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7139–7155 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7156–7169 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7170–7180 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7181–7424 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7425–7434 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7435–7448 |  |
| `applySvcDriver` | 7449–7462 |  |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 7463–8024 | Everything that needs the map surface: fetch the data, mount the deck.gl |

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
| `#revmix` | 5341 |
| `#svccost` | 5432 |
