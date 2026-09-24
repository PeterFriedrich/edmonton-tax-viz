# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~8,076-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (310 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 642–646 |  |
| `HOME` | 647–647 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 648–661 |  |
| `WINDOWS` | 662–687 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 688–697 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 698–702 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 703–778 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `money0` | 779–781 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `fmtMoney` | 782–783 |  |
| `METRICS` | 784–914 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 915–931 |  |
| `RATIO_DENOMS` | 932–965 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 966–966 |  |
| `ratioOf` | 967–967 |  |
| `ratioKept` | 968–989 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 990–1000 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 1001–1028 |  |
| `dominantUse` | 1029–1070 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1071–1241 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1242–1337 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1338–1342 | the Lab: a container for unfinished lenses |
| `inLab` | 1343–1344 |  |
| `DEVIATION_TITLES` | 1345–1349 |  |
| `deviationTitle` | 1350–1355 |  |
| `deviationKind` | 1356–1358 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1359–1366 |  |
| `changeBlurb` | 1367–1387 | Change-lens blurb (COPY_DECISIONS BC1, B8 shape). It follows the window |
| `GLASS_BLURBS` | 1388–1409 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassInstBlurb` | 1410–1422 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1423–1434 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `amenityWhichPhrase` | 1435–1440 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1441–1446 |  |
| `infillAmenityBlurb` | 1447–1460 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1461–1472 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `devTitle` | 1473–1478 | Development blurb, in the COPY_DECISIONS B8 shape (BD1): what the lens |
| `devBlurb` | 1479–1537 |  |
| `setBlurb` | 1538–1550 | Blurb markup (COPY_DECISIONS B8): a blank line starts a new paragraph and |
| `currentBlurb` | 1551–1566 | The active view's blurb. Read by applyView and by the camera's 2D/3D flip |
| `withColourClause` | 1567–1584 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1585–1591 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1592–1605 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1606–1606 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1607–1621 |  |
| `fmtMB` | 1622–1632 |  |
| `showGridBusy` | 1633–1655 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1656–1672 |  |
| `loadGridData` | 1673–1726 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1727–1780 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1781–1805 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1806–1837 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1838–1838 |  |
| `gridFetches` | 1839–1863 |  |
| `RAMPS` | 1864–1904 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1905–1911 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1912–1917 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1918–1918 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1919–1925 |  |
| `AMENITY_BANDS` | 1926–1927 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1928–1930 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1931–1936 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1937–1951 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1952–1957 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1958–1976 |  |
| `gridScale` | 1977–1997 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 1998–2004 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 2005–2016 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 2017–2019 |  |
| `quantile` | 2020–2034 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 2035–2067 |  |
| `moneyBlurb` | 2068–2072 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 2073–2085 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2086–2164 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2165–2165 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2166–2192 |  |
| `failLoading` | 2193–2206 |  |
| `hideLoading` | 2207–2261 |  |
| `topRings` | 2262–2278 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2279–2304 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2305–2305 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2306–2318 |  |
| `svcT` | 2319–2327 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2328–2341 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2342–2342 |  |
| `fmtFire` | 2343–2344 |  |
| `fmtTransit` | 2345–2346 |  |
| `fmtBike` | 2347–2359 |  |
| `fmtRoadM` | 2360–2373 |  |
| `fmtResShare` | 2374–2376 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2377–2382 |  |
| `fmtRoadsCost` | 2383–2387 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2388–2389 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2390–2391 |  |
| `fmtBikeCost` | 2392–2403 |  |
| `servicePlaneLayer` | 2404–2436 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2437–2446 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2447–2452 |  |
| `DEV_IND_TOTAL` | 2453–2455 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2456–2461 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2462–2466 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2467–2472 |  |
| `devGridOfferable` | 2473–2474 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2475–2475 |  |
| `devCol` | 2476–2476 |  |
| `_devScale` | 2477–2477 |  |
| `devScale` | 2478–2484 |  |
| `devT` | 2485–2488 |  |
| `developmentPlaneLayer` | 2489–2505 |  |
| `fmtDev` | 2506–2521 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2522–2527 |  |
| `DEV_GRID_IND_N` | 2528–2528 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2529–2531 |  |
| `devGridScale` | 2532–2558 |  |
| `devGridLayer` | 2559–2607 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2608–2609 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2610–2617 |  |
| `_infillStats` | 2618–2618 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2619–2636 |  |
| `_infillRaw` | 2637–2639 |  |
| `infillScore` | 2640–2655 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2656–2657 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2658–2675 |  |
| `INFILL_CENTER` | 2676–2676 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2677–2677 |  |
| `INFILL_NEG` | 2678–2678 |  |
| `infillColorAt` | 2679–2683 |  |
| `infillPlaneLayer` | 2684–2705 |  |
| `fmtFar` | 2706–2715 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `AMENITY_HIGHLIGHT_COLOR` | 2716–2716 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2717–2771 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2772–2779 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2780–2794 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2795–2815 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2816–2816 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2817–2831 |  |
| `chgT` | 2832–2841 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2842–2872 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2873–2961 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2962–2969 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2970–2970 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2971–2978 |  |
| `deviationRate` | 2979–3021 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 3022–3022 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 3023–3052 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3053–3059 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3060–3071 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3072–3075 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3076–3080 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3081–3091 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3092–3107 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3108–3139 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3140–3164 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `INST_OUTLINE_COLOR` | 3165–3217 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 3218–3222 |  |
| `bandHover` | 3223–3231 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3232–3328 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3329–3336 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3337–3338 |  |
| `glassInstBandLayers` | 3339–3379 |  |
| `ratioInstBandLayers` | 3380–3407 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3408–3420 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3421–3422 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3423–3424 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3425–3425 |  |
| `deviationStats` | 3426–3470 |  |
| `deviationOf` | 3471–3472 |  |
| `deviationT` | 3473–3483 |  |
| `fmtDeviation` | 3484–3505 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3506–3549 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3550–3636 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3637–3659 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3660–3660 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3661–3681 |  |
| `ensureFireStations` | 3682–3697 |  |
| `TRANSIT_STATION_COLOR` | 3698–3698 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3699–3716 |  |
| `ensureTransitStations` | 3717–3732 |  |
| `TRANSIT_LINE_COLOR` | 3733–3733 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3734–3750 |  |
| `ensureLrtLines` | 3751–3767 |  |
| `BIKE_LINE_COLOR` | 3768–3768 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3769–3785 |  |
| `ensureBikeLines` | 3786–3843 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3844–3844 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3845–3848 |  |
| `BOUNDARY_COLOR` | 3849–3858 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3859–3859 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3860–3872 |  |
| `referenceSplit` | 3873–3900 |  |
| `referenceUnderLayers` | 3901–3935 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3936–3952 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3953–3972 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3973–3985 |  |
| `servicesBlurb` | 3986–4003 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 4004–4027 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 4028–4038 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 4039–4090 |  |
| `REF_TIERS` | 4091–4112 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4113–4120 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 4121–4123 |  |
| `placeAnchors` | 4124–4147 |  |
| `labelPool` | 4148–4155 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4156–4209 |  |
| `CHROME_IDS` | 4210–4214 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4215–4233 |  |
| `visibleLabels` | 4234–4288 |  |
| `labelLayer` | 4289–4325 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 4326–4326 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4327–4342 |  |
| `ratioT` | 4343–4365 |  |
| `zMatrix` | 4366–4370 |  |
| `buildLayers` | 4371–4394 |  |
| `flattenDuringEase` | 4395–4419 | Center 2D lowers the heights over the LAST QUARTER OF THE TILT instead |
| `buildViewLayers` | 4420–4729 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4730–4759 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4760–4769 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4770–4772 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 4773–4804 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4805–4811 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4812–4819 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4820–4824 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4825–4835 |  |
| `revenueLens` | 4836–4837 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4838–4870 |  |
| `SVC_COST_BASES` | 4871–4888 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 4889–4897 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 4898–4913 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 4914–4916 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 4917–4923 |  |
| `svcRank` | 4924–4928 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 4929–4935 |  |
| `svcDriverReading` | 4936–4956 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 4957–4957 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4958–4961 |  |
| `servicePanelFor` | 4962–4982 |  |
| `hoodPanelLens` | 4983–4986 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4987–5004 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 5005–5036 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 5037–5042 |  |
| `sparklineSvg` | 5043–5058 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 5059–5118 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5119–5124 | Development history: new supply per year |
| `devHistKey` | 5125–5134 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5135–5139 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5140–5140 |  |
| `devHistVerb` | 5141–5146 |  |
| `devHistoryFor` | 5147–5168 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5169–5188 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5189–5208 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5209–5244 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5245–5247 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5248–5311 |  |
| `syncTemporalPos` | 5312–5338 |  |
| `openTemporal` | 5339–5373 |  |
| `renderRevenueMix` | 5374–5440 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 5441–5520 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 5521–5524 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5525–5575 |  |
| `syncPinnedPanel` | 5576–5605 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5606–5621 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5622–5639 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5640–5687 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5688–5693 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5694–5740 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5741–5757 |  |
| `temporalClick` | 5758–5815 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 5816–5884 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 5885–6265 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6266–6347 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6348–6348 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6349–6367 |  |
| `syncMetricButtons` | 6368–6391 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6392–6398 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6399–6412 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6413–6454 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6455–6497 |  |
| `toggleBudgetPanel` | 6498–6523 |  |
| `syncMillRates` | 6524–6556 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 6557–6577 |  |
| `applyColorAdjust` | 6578–6598 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 6599–6611 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 6612–6626 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 6627–6644 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 6645–6661 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 6662–6683 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 6684–6700 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 6701–6940 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 6941–6951 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 6952–6965 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 6966–6974 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 6975–6985 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 6986–6997 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 6998–7010 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 7011–7031 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 7032–7079 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7080–7085 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7086–7107 |  |
| `applyMoneyDetail` | 7108–7132 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7133–7144 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7145–7152 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7153–7171 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7172–7182 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7183–7190 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7191–7207 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7208–7221 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7222–7232 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7233–7476 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7477–7486 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7487–7500 |  |
| `applySvcDriver` | 7501–7514 |  |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 7515–8076 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (966 edges)

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
| the Lab: a container for unfinished lenses | 116 | 64% |
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
| `#title-p` | 63 |
| `#temporal` | 74 |
| `#temporal-close` | 75 |
| `#temporal-name` | 76 |
| `#temporal-body` | 83 |
| `#temporal-chart` | 84 |
| `#temporal-read` | 85 |
| `#temporal-note` | 86 |
| `#temporal-hint` | 90 |
| `#millrates` | 106 |
| `#mill-head` | 107 |
| `#mill-rows` | 108 |
| `#mill-note` | 109 |
| `#budget` | 123 |
| `#budget-close` | 130 |
| `#budget-head` | 131 |
| `#budget-body` | 136 |
| `#budget-rows` | 137 |
| `#budget-other-hd` | 138 |
| `#budget-other` | 139 |
| `#budget-note` | 140 |
| `#peek` | 155 |
| `#peek-name` | 156 |
| `#peek-read` | 157 |
| `#peek-go` | 158 |
| `#controls` | 161 |
| `#toggle` | 174 |
| `#metric-row` | 175 |
| `#revcut` | 179 |
| `#moneymode` | 184 |
| `#views` | 190 |
| `#optpanel` | 204 |
| `#opt-fold` | 205 |
| `#opt-caret` | 205 |
| `#opt-body` | 206 |
| `#layers` | 207 |
| `#chgwindow-hd` | 208 |
| `#chgwindow` | 209 |
| `#labpick-hd` | 218 |
| `#labpick` | 219 |
| `#labcut-hd` | 220 |
| `#labcut` | 221 |
| `#moneydetail-hd` | 226 |
| `#moneydetail` | 227 |
| `#amenity-hd` | 252 |
| `#amenity` | 253 |
| `#amenity-lrt-row` | 254 |
| `#amenity-lrt-on` | 255 |
| `#amenity-school-row` | 257 |
| `#amenity-school-on` | 258 |
| `#uses-prisms-hd` | 261 |
| `#uses-prisms` | 262 |
| `#uses-prisms-on` | 264 |
| `#devmode-hd` | 267 |
| `#devmode` | 268 |
| `#devmetric-hd` | 272 |
| `#devmetric` | 273 |
| `#devwindow-hd` | 278 |
| `#devwindow` | 279 |
| `#devdetail-hd` | 284 |
| `#devdetail` | 285 |
| `#prism-hd` | 289 |
| `#prism-row` | 290 |
| `#prism-opacity` | 292 |
| `#prism-opacity-val` | 293 |
| `#services-hd` | 295 |
| `#services` | 296 |
| `#denom-hd` | 395 |
| `#denom` | 396 |
| `#ratio-denom-hd` | 400 |
| `#ratio-denom` | 401 |
| `#hoodmode` | 411 |
| `#hoodmode-btn` | 412 |
| `#coloradj` | 424 |
| `#coloradj-btn` | 425 |
| `#budget-pod` | 432 |
| `#budget-btn` | 433 |
| `#a11y` | 437 |
| `#a11y-btn` | 438 |
| `#a11y-menu` | 439 |
| `#palette` | 441 |
| `#labels-on` | 448 |
| `#reference-on` | 456 |
| `#about` | 461 |
| `#about-btn` | 462 |
| `#about-menu` | 463 |
| `#about-src-roads` | 475 |
| `#about-src-services` | 476 |
| `#about-vintage` | 504 |
| `#about-build` | 508 |
| `#about-modelled-roads` | 522 |
| `#about-modelled` | 540 |
| `#about-budget` | 550 |
| `#about-budget-lead` | 552 |
| `#about-budget-rows` | 553 |
| `#about-budget-note` | 554 |
| `#about-updated` | 565 |
| `#botleft` | 569 |
| `#compass` | 570 |
| `#rot-ccw` | 571 |
| `#tonorth` | 578 |
| `#needle` | 580 |
| `#rot-cw` | 585 |
| `#viewbtns` | 593 |
| `#recenter` | 595 |
| `#center2d` | 596 |
| `#legend` | 598 |
| `#legend-label` | 599 |
| `#legend-min` | 601 |
| `#legend-max` | 601 |
| `#legend-cats` | 603 |
| `#revmix` | 5393 |
| `#svccost` | 5484 |
