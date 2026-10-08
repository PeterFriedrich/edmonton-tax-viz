# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~8,661-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (332 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 703–707 |  |
| `HOME` | 708–708 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 709–722 |  |
| `WINDOWS` | 723–748 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 749–758 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 759–763 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 764–839 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `money0` | 840–842 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `fmtMoney` | 843–844 |  |
| `METRICS` | 845–947 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 948–964 |  |
| `RATIO_DENOMS` | 965–998 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 999–999 |  |
| `ratioOf` | 1000–1000 |  |
| `ratioKept` | 1001–1022 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 1023–1033 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 1034–1061 |  |
| `dominantUse` | 1062–1103 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1104–1254 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1255–1350 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1351–1355 | the Lab: a container for unfinished lenses |
| `inLab` | 1356–1357 |  |
| `DEVIATION_TITLES` | 1358–1362 |  |
| `deviationTitle` | 1363–1368 |  |
| `deviationKind` | 1369–1371 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1372–1379 |  |
| `changeBlurb` | 1380–1397 | Change-lens blurb (COPY_DECISIONS BC1, B8 shape). It follows the window |
| `glassLead` | 1398–1410 | Grid blurb (COPY_DECISIONS BG1, B8 shape). Names the metric (B6) and the |
| `glassInstBlurb` | 1411–1423 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1424–1432 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `ratioBlurb` | 1433–1441 | Ratio blurb (COPY_DECISIONS BR1, B8 shape): the denominator's P1, a |
| `amenityWhichPhrase` | 1442–1447 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1448–1455 |  |
| `infillAmenityBlurb` | 1456–1469 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1470–1481 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `devTitle` | 1482–1487 | Development blurb, in the COPY_DECISIONS B8 shape (BD1): what the lens |
| `devBlurb` | 1488–1546 |  |
| `setBlurb` | 1547–1559 | Blurb markup (COPY_DECISIONS B8): a blank line starts a new paragraph and |
| `currentBlurb` | 1560–1575 | The active view's blurb. Read by applyView and by the camera's 2D/3D flip |
| `withColourClause` | 1576–1593 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1594–1600 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1601–1614 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1615–1615 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1616–1630 |  |
| `fmtMB` | 1631–1641 |  |
| `showGridBusy` | 1642–1664 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1665–1681 |  |
| `loadGridData` | 1682–1735 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1736–1789 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1790–1814 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1815–1846 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1847–1847 |  |
| `gridFetches` | 1848–1874 |  |
| `RAMPS` | 1875–1919 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1920–1925 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `rampSetAside` | 1926–1932 | The set-aside colour beside a RAMP-coloured surface. Only where the |
| `GLASS_PLANE_COLOR` | 1933–1938 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1939–1939 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1940–1946 |  |
| `AMENITY_BANDS` | 1947–1948 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1949–1951 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1952–1957 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1958–1972 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1973–1978 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1979–1997 |  |
| `gridScale` | 1998–2018 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 2019–2025 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 2026–2037 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 2038–2040 |  |
| `quantile` | 2041–2055 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 2056–2090 |  |
| `moneyBlurb` | 2091–2102 | The money blurb (COPY_DECISIONS BM1, B8 shape): the metric's own P1 under |
| `fillFor` | 2103–2115 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2116–2194 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2195–2195 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2196–2222 |  |
| `failLoading` | 2223–2236 |  |
| `hideLoading` | 2237–2292 |  |
| `topRings` | 2293–2309 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2310–2335 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2336–2336 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2337–2349 |  |
| `svcT` | 2350–2358 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2359–2372 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2373–2373 |  |
| `fmtFire` | 2374–2375 |  |
| `fmtTransit` | 2376–2377 |  |
| `fmtBike` | 2378–2390 |  |
| `fmtRoadM` | 2391–2404 |  |
| `fmtResShare` | 2405–2407 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2408–2413 |  |
| `fmtRoadsCost` | 2414–2418 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2419–2420 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2421–2422 |  |
| `fmtBikeCost` | 2423–2434 |  |
| `servicePlaneLayer` | 2435–2467 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2468–2477 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2478–2483 |  |
| `DEV_IND_TOTAL` | 2484–2486 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2487–2492 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2493–2497 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2498–2503 |  |
| `devGridOfferable` | 2504–2505 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2506–2506 |  |
| `devCol` | 2507–2507 |  |
| `_devScale` | 2508–2508 |  |
| `devScale` | 2509–2515 |  |
| `devT` | 2516–2519 |  |
| `developmentPlaneLayer` | 2520–2536 |  |
| `fmtDev` | 2537–2552 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2553–2558 |  |
| `DEV_GRID_IND_N` | 2559–2559 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2560–2562 |  |
| `devGridScale` | 2563–2589 |  |
| `devGridLayer` | 2590–2638 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2639–2640 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2641–2648 |  |
| `_infillStats` | 2649–2649 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2650–2667 |  |
| `_infillRaw` | 2668–2670 |  |
| `infillScore` | 2671–2686 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2687–2688 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2689–2706 |  |
| `INFILL_CENTER` | 2707–2707 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2708–2708 |  |
| `INFILL_NEG` | 2709–2709 |  |
| `infillColorAt` | 2710–2714 |  |
| `infillPlaneLayer` | 2715–2736 |  |
| `fmtFar` | 2737–2746 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `AMENITY_HIGHLIGHT_COLOR` | 2747–2747 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2748–2802 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2803–2810 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2811–2825 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2826–2846 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2847–2847 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2848–2862 |  |
| `chgT` | 2863–2872 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2873–2903 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2904–2992 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2993–3000 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 3001–3001 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 3002–3009 |  |
| `deviationRate` | 3010–3052 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 3053–3053 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 3054–3083 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3084–3090 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3091–3102 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3103–3106 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3107–3111 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3112–3122 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3123–3138 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3139–3170 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3171–3195 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `INST_OUTLINE_COLOR` | 3196–3248 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 3249–3253 |  |
| `bandHover` | 3254–3262 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3263–3365 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3366–3373 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3374–3375 |  |
| `glassInstBandLayers` | 3376–3416 |  |
| `ratioInstBandLayers` | 3417–3444 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3445–3457 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3458–3459 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3460–3461 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3462–3462 |  |
| `deviationStats` | 3463–3507 |  |
| `deviationOf` | 3508–3509 |  |
| `deviationT` | 3510–3520 |  |
| `fmtDeviation` | 3521–3542 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3543–3586 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3587–3673 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3674–3696 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3697–3697 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3698–3718 |  |
| `ensureFireStations` | 3719–3734 |  |
| `TRANSIT_STATION_COLOR` | 3735–3735 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3736–3753 |  |
| `ensureTransitStations` | 3754–3769 |  |
| `TRANSIT_LINE_COLOR` | 3770–3770 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3771–3787 |  |
| `ensureLrtLines` | 3788–3804 |  |
| `BIKE_LINE_COLOR` | 3805–3805 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3806–3822 |  |
| `ensureBikeLines` | 3823–3880 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3881–3881 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3882–3885 |  |
| `BOUNDARY_COLOR` | 3886–3895 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3896–3896 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3897–3909 |  |
| `referenceSplit` | 3910–3937 |  |
| `referenceUnderLayers` | 3938–3972 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3973–3989 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3990–4009 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 4010–4023 |  |
| `servicesBlurb` | 4024–4035 | Services-view blurb (COPY_DECISIONS BS1, B8 shape): the colour-driving |
| `hoodHoverLayer` | 4036–4059 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 4060–4070 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 4071–4122 |  |
| `REF_TIERS` | 4123–4144 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4145–4152 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 4153–4155 |  |
| `placeAnchors` | 4156–4179 |  |
| `labelPool` | 4180–4187 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4188–4241 |  |
| `CHROME_IDS` | 4242–4246 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4247–4265 |  |
| `visibleLabels` | 4266–4320 |  |
| `labelLayer` | 4321–4373 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `withSelectedHood` | 4374–4414 |  |
| `_ratioScales` | 4415–4415 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4416–4431 |  |
| `ratioT` | 4432–4454 |  |
| `zMatrix` | 4455–4459 |  |
| `buildLayers` | 4460–4484 |  |
| `flattenDuringEase` | 4485–4509 | Center 2D lowers the heights over the LAST QUARTER OF THE TILT instead |
| `buildViewLayers` | 4510–4819 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4820–4849 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4850–4859 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4860–4862 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 4863–4894 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4895–4901 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4902–4909 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4910–4914 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4915–4925 |  |
| `revenueLens` | 4926–4927 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4928–4960 |  |
| `SVC_COST_BASES` | 4961–4978 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 4979–4987 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 4988–4997 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 4998–5000 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 5001–5007 |  |
| `svcRank` | 5008–5012 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 5013–5019 |  |
| `svcDriverReading` | 5020–5040 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 5041–5041 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 5042–5045 |  |
| `servicePanelFor` | 5046–5050 |  |
| `ratioPanelFor` | 5051–5074 | Ratio carries the cost-as-a-share-of-tax panel that Services had until |
| `hoodPanelLens` | 5075–5079 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 5080–5097 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 5098–5129 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 5130–5135 |  |
| `sparklineSvg` | 5136–5151 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 5152–5211 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5212–5217 | Development history: new supply per year |
| `devHistKey` | 5218–5227 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5228–5232 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5233–5233 |  |
| `devHistVerb` | 5234–5239 |  |
| `devHistoryFor` | 5240–5278 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5279–5298 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5299–5318 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5319–5354 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5355–5357 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5358–5421 |  |
| `syncTemporalPos` | 5422–5448 |  |
| `openTemporal` | 5449–5486 |  |
| `renderRevenueMix` | 5487–5556 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderRatioCost` | 5557–5631 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `renderServiceCost` | 5632–5689 | The Services panel: what each cost IS for this hood, in dollars, and where |
| `fmtSvcRatio` | 5690–5693 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5694–5744 |  |
| `syncPinnedPanel` | 5745–5778 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5779–5794 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5795–5812 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5813–5860 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5861–5866 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5867–5914 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5915–5931 |  |
| `temporalClick` | 5932–5986 | Click a hood to pin its history; click the pinned one again to unpin. |

### neighbourhood search

| symbol | lines | what it does |
|---|---|---|
| `searchNorm` | 5987–5994 | neighbourhood search |
| `searchMatches` | 5995–6009 | Ranked: the name starts with the query, then a later WORD does (so |
| `renderSearchList` | 6010–6038 |  |
| `openSearch` | 6039–6051 |  |
| `closeSearch` | 6052–6070 |  |

### how-to-read guide

| symbol | lines | what it does |
|---|---|---|
| `openGuide` | 6071–6083 |  |
| `closeGuide` | 6084–6091 |  |
| `maybeAutoGuide` | 6092–6108 |  |
| `flyToHood` | 6109–6128 | Keep the current tilt and rotation, so the camera moves TO the hood |
| `pickSearch` | 6129–6147 | A pick reads exactly like tapping or clicking the hood (temporalClick |
| `primaryRow` | 6148–6216 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 6217–6594 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6595–6684 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6685–6685 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6686–6704 |  |
| `syncMetricButtons` | 6705–6728 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6729–6735 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6736–6749 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6750–6791 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6792–6834 |  |
| `toggleBudgetPanel` | 6835–6860 |  |
| `syncMillRates` | 6861–6893 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 6894–6914 |  |
| `applyColorAdjust` | 6915–6935 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 6936–6948 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 6949–6963 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 6964–6981 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 6982–6998 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 6999–7020 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 7021–7037 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 7038–7277 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 7278–7288 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 7289–7304 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 7305–7313 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 7314–7324 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 7325–7336 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 7337–7349 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 7350–7370 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 7371–7418 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7419–7424 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7425–7446 |  |
| `applyMoneyDetail` | 7447–7471 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7472–7483 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7484–7491 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7492–7510 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7511–7521 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7522–7529 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7530–7546 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7547–7560 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7561–7571 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7572–7815 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7816–7825 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7826–7839 |  |
| `applySvcDriver` | 7840–7872 |  |

### shareable URL: the hash names the view on screen

| symbol | lines | what it does |
|---|---|---|
| `METRIC_FROM_URL` | 7873–7875 |  |
| `urlHash` | 7876–7916 |  |
| `shareLink` | 7917–7925 | Absolute on purpose: the full build carries <base href="../">, and a |
| `copyShareLink` | 7926–7937 | With no clipboard (an insecure origin, a denied permission) the link goes |
| `offered` | 7938–7944 | On screen, ignoring the Options fold: a folded panel on a phone hides |
| `applyUrlState` | 7945–8017 |  |
| `restoreFromHash` | 8018–8036 | Once, at the end of boot, after every build and data gate has run. The |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 8037–8661 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (1066 edges)

⚠️ **A regex reference count, not a call graph** — a name in a comment or string counts, and a nested symbol is attributed to its enclosing range. Use it for *what is central* and *would this seam hold*, never as ground truth for a final module boundary.

**Most depended-on** — moving one of these touches everything below it.

| symbol | referenced by | section |
|---|---|---|
| `state` | 126 | the Lab: a container for unfinished lenses |
| `buildLayers` | 42 | geographic reference layers (all views) |
| `METRICS` | 17 | tunables |
| `applyView` | 17 | control appliers + the view/legend dispatchers |
| `SERVICES` | 16 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `refreshLegend` | 15 | control appliers + the view/legend dispatchers |
| `setBlurb` | 15 | the Lab: a container for unfinished lenses |
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
| the Lab: a container for unfinished lenses | 126 | 64% |
| tunables | 13 | 46% |
| Development 100 m detail grid (layers-panel toggle, 2026-07-15) | 9 | 44% |
| change lens: how each hood's share of the assessment base moved | 16 | 44% |
| geographic reference layers (all views) | 97 | 42% |
| neighbourhood search | 11 | 36% |
| loading overlay | 56 | 34% |
| two tiers, answering two different questions | 29 | 31% |
| Development history: new supply per year | 111 | 30% |
| Money's revenue panel: where a hood's levy comes from | 35 | 29% |
| the same doubt, at 100 m | 61 | 26% |
| shareable URL: the hash names the view on screen | 24 | 21% |
| control appliers + the view/legend dispatchers | 223 | 20% |
| services lens views (SPEC_services.md display architecture) | 5 | 20% |
| the citywide budget panel (EXPERIMENTAL, full build only) | 12 | 8% |
| how-to-read guide | 112 | 8% |
| services view (SPEC_services.md UI generalization, 2026-07-05) | 18 | 0% |
| the institutional uncertainty band | 2 | 0% |
| temporal lens (SPEC_temporal.md phase 3) | 4 | 0% |
| boot | 69 | 0% |

## Element ids (143) — the control surface

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
| `#search` | 75 |
| `#search-btn` | 76 |
| `#search-box` | 79 |
| `#search-input` | 80 |
| `#search-close` | 84 |
| `#search-list` | 86 |
| `#guide-btn` | 94 |
| `#guide` | 96 |
| `#guide-close` | 97 |
| `#guide-ask` | 98 |
| `#guide-show` | 99 |
| `#guide-body` | 102 |
| `#temporal` | 121 |
| `#temporal-close` | 122 |
| `#temporal-name` | 123 |
| `#temporal-body` | 130 |
| `#temporal-chart` | 131 |
| `#temporal-read` | 132 |
| `#temporal-note` | 133 |
| `#temporal-hint` | 137 |
| `#millrates` | 153 |
| `#mill-head` | 154 |
| `#mill-rows` | 155 |
| `#mill-note` | 156 |
| `#budget` | 170 |
| `#budget-close` | 177 |
| `#budget-head` | 178 |
| `#budget-body` | 183 |
| `#budget-rows` | 184 |
| `#budget-other-hd` | 185 |
| `#budget-other` | 186 |
| `#budget-note` | 187 |
| `#peek` | 202 |
| `#peek-name` | 203 |
| `#peek-read` | 204 |
| `#peek-go` | 205 |
| `#controls` | 208 |
| `#toggle` | 221 |
| `#metric-row` | 222 |
| `#revcut` | 226 |
| `#moneymode` | 231 |
| `#views` | 237 |
| `#optpanel` | 251 |
| `#opt-fold` | 252 |
| `#opt-caret` | 252 |
| `#opt-body` | 253 |
| `#layers` | 254 |
| `#chgwindow-hd` | 255 |
| `#chgwindow` | 256 |
| `#labpick-hd` | 265 |
| `#labpick` | 266 |
| `#labcut-hd` | 267 |
| `#labcut` | 268 |
| `#moneydetail-hd` | 273 |
| `#moneydetail` | 274 |
| `#amenity-hd` | 299 |
| `#amenity` | 300 |
| `#amenity-lrt-row` | 301 |
| `#amenity-lrt-on` | 302 |
| `#amenity-school-row` | 304 |
| `#amenity-school-on` | 305 |
| `#uses-prisms-hd` | 308 |
| `#uses-prisms` | 309 |
| `#uses-prisms-on` | 311 |
| `#devmode-hd` | 314 |
| `#devmode` | 315 |
| `#devmetric-hd` | 319 |
| `#devmetric` | 320 |
| `#devwindow-hd` | 325 |
| `#devwindow` | 326 |
| `#devdetail-hd` | 331 |
| `#devdetail` | 332 |
| `#prism-hd` | 336 |
| `#prism-row` | 337 |
| `#prism-opacity` | 339 |
| `#prism-opacity-val` | 340 |
| `#services-hd` | 342 |
| `#services` | 343 |
| `#denom-hd` | 442 |
| `#denom` | 443 |
| `#ratio-denom-hd` | 447 |
| `#ratio-denom` | 448 |
| `#hoodmode` | 458 |
| `#hoodmode-btn` | 459 |
| `#coloradj` | 471 |
| `#coloradj-btn` | 472 |
| `#budget-pod` | 479 |
| `#budget-btn` | 480 |
| `#share` | 487 |
| `#share-btn` | 488 |
| `#a11y` | 491 |
| `#a11y-btn` | 492 |
| `#a11y-menu` | 493 |
| `#palette` | 495 |
| `#labels-on` | 502 |
| `#reference-on` | 510 |
| `#about` | 515 |
| `#about-btn` | 516 |
| `#about-menu` | 517 |
| `#about-src-roads` | 529 |
| `#about-src-services` | 530 |
| `#about-vintage` | 558 |
| `#about-build` | 562 |
| `#about-lot-acres` | 567 |
| `#about-modelled-roads` | 578 |
| `#about-modelled` | 600 |
| `#about-budget` | 610 |
| `#about-budget-lead` | 612 |
| `#about-budget-rows` | 613 |
| `#about-budget-note` | 614 |
| `#about-updated` | 626 |
| `#botleft` | 630 |
| `#compass` | 631 |
| `#rot-ccw` | 632 |
| `#tonorth` | 639 |
| `#needle` | 641 |
| `#rot-cw` | 646 |
| `#viewbtns` | 654 |
| `#recenter` | 656 |
| `#center2d` | 657 |
| `#legend` | 659 |
| `#legend-label` | 660 |
| `#legend-min` | 662 |
| `#legend-max` | 662 |
| `#legend-cats` | 664 |
| `#revmix` | 5506 |
| `#svccost` | 5600 |
