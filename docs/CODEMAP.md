# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~8,054-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (311 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 649–653 |  |
| `HOME` | 654–654 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 655–668 |  |
| `WINDOWS` | 669–694 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 695–704 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 705–709 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 710–785 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `money0` | 786–788 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `fmtMoney` | 789–790 |  |
| `METRICS` | 791–893 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 894–910 |  |
| `RATIO_DENOMS` | 911–944 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 945–945 |  |
| `ratioOf` | 946–946 |  |
| `ratioKept` | 947–968 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 969–979 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 980–1007 |  |
| `dominantUse` | 1008–1049 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1050–1200 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1201–1296 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1297–1301 | the Lab: a container for unfinished lenses |
| `inLab` | 1302–1303 |  |
| `DEVIATION_TITLES` | 1304–1308 |  |
| `deviationTitle` | 1309–1314 |  |
| `deviationKind` | 1315–1317 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1318–1325 |  |
| `changeBlurb` | 1326–1343 | Change-lens blurb (COPY_DECISIONS BC1, B8 shape). It follows the window |
| `glassLead` | 1344–1356 | Grid blurb (COPY_DECISIONS BG1, B8 shape). Names the metric (B6) and the |
| `glassInstBlurb` | 1357–1369 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1370–1378 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `ratioBlurb` | 1379–1387 | Ratio blurb (COPY_DECISIONS BR1, B8 shape): the denominator's P1, a |
| `amenityWhichPhrase` | 1388–1393 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1394–1401 |  |
| `infillAmenityBlurb` | 1402–1415 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1416–1427 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `devTitle` | 1428–1433 | Development blurb, in the COPY_DECISIONS B8 shape (BD1): what the lens |
| `devBlurb` | 1434–1492 |  |
| `setBlurb` | 1493–1505 | Blurb markup (COPY_DECISIONS B8): a blank line starts a new paragraph and |
| `currentBlurb` | 1506–1521 | The active view's blurb. Read by applyView and by the camera's 2D/3D flip |
| `withColourClause` | 1522–1539 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1540–1546 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1547–1560 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1561–1561 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1562–1576 |  |
| `fmtMB` | 1577–1587 |  |
| `showGridBusy` | 1588–1610 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1611–1627 |  |
| `loadGridData` | 1628–1681 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1682–1735 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1736–1760 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1761–1792 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1793–1793 |  |
| `gridFetches` | 1794–1818 |  |
| `RAMPS` | 1819–1859 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1860–1866 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1867–1872 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1873–1873 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1874–1880 |  |
| `AMENITY_BANDS` | 1881–1882 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1883–1885 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1886–1891 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1892–1906 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1907–1912 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1913–1931 |  |
| `gridScale` | 1932–1952 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 1953–1959 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1960–1971 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1972–1974 |  |
| `quantile` | 1975–1989 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1990–2024 |  |
| `moneyBlurb` | 2025–2036 | The money blurb (COPY_DECISIONS BM1, B8 shape): the metric's own P1 under |
| `fillFor` | 2037–2049 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2050–2128 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2129–2129 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2130–2156 |  |
| `failLoading` | 2157–2170 |  |
| `hideLoading` | 2171–2225 |  |
| `topRings` | 2226–2242 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2243–2268 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2269–2269 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2270–2282 |  |
| `svcT` | 2283–2291 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2292–2305 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2306–2306 |  |
| `fmtFire` | 2307–2308 |  |
| `fmtTransit` | 2309–2310 |  |
| `fmtBike` | 2311–2323 |  |
| `fmtRoadM` | 2324–2337 |  |
| `fmtResShare` | 2338–2340 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2341–2346 |  |
| `fmtRoadsCost` | 2347–2351 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2352–2353 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2354–2355 |  |
| `fmtBikeCost` | 2356–2367 |  |
| `servicePlaneLayer` | 2368–2400 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2401–2410 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2411–2416 |  |
| `DEV_IND_TOTAL` | 2417–2419 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2420–2425 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2426–2430 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2431–2436 |  |
| `devGridOfferable` | 2437–2438 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2439–2439 |  |
| `devCol` | 2440–2440 |  |
| `_devScale` | 2441–2441 |  |
| `devScale` | 2442–2448 |  |
| `devT` | 2449–2452 |  |
| `developmentPlaneLayer` | 2453–2469 |  |
| `fmtDev` | 2470–2485 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2486–2491 |  |
| `DEV_GRID_IND_N` | 2492–2492 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2493–2495 |  |
| `devGridScale` | 2496–2522 |  |
| `devGridLayer` | 2523–2571 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2572–2573 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2574–2581 |  |
| `_infillStats` | 2582–2582 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2583–2600 |  |
| `_infillRaw` | 2601–2603 |  |
| `infillScore` | 2604–2619 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2620–2621 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2622–2639 |  |
| `INFILL_CENTER` | 2640–2640 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2641–2641 |  |
| `INFILL_NEG` | 2642–2642 |  |
| `infillColorAt` | 2643–2647 |  |
| `infillPlaneLayer` | 2648–2669 |  |
| `fmtFar` | 2670–2679 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `AMENITY_HIGHLIGHT_COLOR` | 2680–2680 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2681–2735 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2736–2743 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2744–2758 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2759–2779 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2780–2780 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2781–2795 |  |
| `chgT` | 2796–2805 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2806–2836 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2837–2925 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2926–2933 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2934–2934 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2935–2942 |  |
| `deviationRate` | 2943–2985 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2986–2986 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 2987–3016 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3017–3023 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3024–3035 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3036–3039 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3040–3044 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3045–3055 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3056–3071 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3072–3103 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3104–3128 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `INST_OUTLINE_COLOR` | 3129–3181 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 3182–3186 |  |
| `bandHover` | 3187–3195 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3196–3292 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3293–3300 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3301–3302 |  |
| `glassInstBandLayers` | 3303–3343 |  |
| `ratioInstBandLayers` | 3344–3371 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3372–3384 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3385–3386 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3387–3388 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3389–3389 |  |
| `deviationStats` | 3390–3434 |  |
| `deviationOf` | 3435–3436 |  |
| `deviationT` | 3437–3447 |  |
| `fmtDeviation` | 3448–3469 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3470–3513 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3514–3600 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3601–3623 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3624–3624 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3625–3645 |  |
| `ensureFireStations` | 3646–3661 |  |
| `TRANSIT_STATION_COLOR` | 3662–3662 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3663–3680 |  |
| `ensureTransitStations` | 3681–3696 |  |
| `TRANSIT_LINE_COLOR` | 3697–3697 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3698–3714 |  |
| `ensureLrtLines` | 3715–3731 |  |
| `BIKE_LINE_COLOR` | 3732–3732 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3733–3749 |  |
| `ensureBikeLines` | 3750–3807 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3808–3808 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3809–3812 |  |
| `BOUNDARY_COLOR` | 3813–3822 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3823–3823 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3824–3836 |  |
| `referenceSplit` | 3837–3864 |  |
| `referenceUnderLayers` | 3865–3899 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3900–3916 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3917–3936 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3937–3950 |  |
| `servicesBlurb` | 3951–3962 | Services-view blurb (COPY_DECISIONS BS1, B8 shape): the colour-driving |
| `hoodHoverLayer` | 3963–3986 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 3987–3997 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 3998–4049 |  |
| `REF_TIERS` | 4050–4071 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4072–4079 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 4080–4082 |  |
| `placeAnchors` | 4083–4106 |  |
| `labelPool` | 4107–4114 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4115–4168 |  |
| `CHROME_IDS` | 4169–4173 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4174–4192 |  |
| `visibleLabels` | 4193–4247 |  |
| `labelLayer` | 4248–4284 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 4285–4285 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4286–4301 |  |
| `ratioT` | 4302–4324 |  |
| `zMatrix` | 4325–4329 |  |
| `buildLayers` | 4330–4353 |  |
| `flattenDuringEase` | 4354–4378 | Center 2D lowers the heights over the LAST QUARTER OF THE TILT instead |
| `buildViewLayers` | 4379–4688 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4689–4718 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4719–4728 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4729–4731 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 4732–4763 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4764–4770 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4771–4778 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4779–4783 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4784–4794 |  |
| `revenueLens` | 4795–4796 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4797–4829 |  |
| `SVC_COST_BASES` | 4830–4847 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 4848–4856 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 4857–4872 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 4873–4875 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 4876–4882 |  |
| `svcRank` | 4883–4887 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 4888–4894 |  |
| `svcDriverReading` | 4895–4915 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 4916–4916 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4917–4920 |  |
| `servicePanelFor` | 4921–4943 |  |
| `hoodPanelLens` | 4944–4948 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4949–4966 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4967–4998 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 4999–5004 |  |
| `sparklineSvg` | 5005–5020 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 5021–5080 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5081–5086 | Development history: new supply per year |
| `devHistKey` | 5087–5096 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5097–5101 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5102–5102 |  |
| `devHistVerb` | 5103–5108 |  |
| `devHistoryFor` | 5109–5144 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5145–5164 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5165–5184 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5185–5220 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5221–5223 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5224–5287 |  |
| `syncTemporalPos` | 5288–5314 |  |
| `openTemporal` | 5315–5349 |  |
| `renderRevenueMix` | 5350–5416 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 5417–5496 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 5497–5500 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5501–5551 |  |
| `syncPinnedPanel` | 5552–5581 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5582–5597 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5598–5615 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5616–5663 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5664–5669 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5670–5716 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5717–5733 |  |
| `temporalClick` | 5734–5791 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 5792–5860 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 5861–6238 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6239–6325 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6326–6326 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6327–6345 |  |
| `syncMetricButtons` | 6346–6369 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6370–6376 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6377–6390 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6391–6432 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6433–6475 |  |
| `toggleBudgetPanel` | 6476–6501 |  |
| `syncMillRates` | 6502–6534 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 6535–6555 |  |
| `applyColorAdjust` | 6556–6576 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 6577–6589 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 6590–6604 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 6605–6622 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 6623–6639 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 6640–6661 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 6662–6678 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 6679–6918 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 6919–6929 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 6930–6943 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 6944–6952 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 6953–6963 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 6964–6975 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 6976–6988 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 6989–7009 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 7010–7057 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7058–7063 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7064–7085 |  |
| `applyMoneyDetail` | 7086–7110 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7111–7122 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7123–7130 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7131–7149 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7150–7160 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7161–7168 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7169–7185 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7186–7199 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7200–7210 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7211–7454 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7455–7464 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7465–7478 |  |
| `applySvcDriver` | 7479–7492 |  |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 7493–8054 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (975 edges)

⚠️ **A regex reference count, not a call graph** — a name in a comment or string counts, and a nested symbol is attributed to its enclosing range. Use it for *what is central* and *would this seam hold*, never as ground truth for a final module boundary.

**Most depended-on** — moving one of these touches everything below it.

| symbol | referenced by | section |
|---|---|---|
| `state` | 120 | the Lab: a container for unfinished lenses |
| `buildLayers` | 37 | geographic reference layers (all views) |
| `METRICS` | 17 | tunables |
| `applyView` | 15 | control appliers + the view/legend dispatchers |
| `setBlurb` | 15 | the Lab: a container for unfinished lenses |
| `refreshLegend` | 14 | control appliers + the view/legend dispatchers |
| `SERVICES` | 13 | services view (SPEC_services.md UI generalization, 2026-07-05) |
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
| the Lab: a container for unfinished lenses | 119 | 64% |
| tunables | 13 | 46% |
| Development 100 m detail grid (layers-panel toggle, 2026-07-15) | 9 | 44% |
| change lens: how each hood's share of the assessment base moved | 16 | 44% |
| geographic reference layers (all views) | 92 | 43% |
| loading overlay | 55 | 35% |
| two tiers, answering two different questions | 29 | 31% |
| Money's revenue panel: where a hood's levy comes from | 36 | 28% |
| the same doubt, at 100 m | 61 | 26% |
| Development history: new supply per year | 196 | 25% |
| services lens views (SPEC_services.md display architecture) | 5 | 20% |
| control appliers + the view/legend dispatchers | 216 | 20% |
| the citywide budget panel (EXPERIMENTAL, full build only) | 12 | 8% |
| services view (SPEC_services.md UI generalization, 2026-07-05) | 18 | 0% |
| the institutional uncertainty band | 2 | 0% |
| temporal lens (SPEC_temporal.md phase 3) | 4 | 0% |
| boot | 59 | 0% |

## Element ids (129) — the control surface

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
| `#about-lot-acres` | 514 |
| `#about-modelled-roads` | 525 |
| `#about-modelled` | 547 |
| `#about-budget` | 557 |
| `#about-budget-lead` | 559 |
| `#about-budget-rows` | 560 |
| `#about-budget-note` | 561 |
| `#about-updated` | 572 |
| `#botleft` | 576 |
| `#compass` | 577 |
| `#rot-ccw` | 578 |
| `#tonorth` | 585 |
| `#needle` | 587 |
| `#rot-cw` | 592 |
| `#viewbtns` | 600 |
| `#recenter` | 602 |
| `#center2d` | 603 |
| `#legend` | 605 |
| `#legend-label` | 606 |
| `#legend-min` | 608 |
| `#legend-max` | 608 |
| `#legend-cats` | 610 |
| `#revmix` | 5369 |
| `#svccost` | 5460 |
