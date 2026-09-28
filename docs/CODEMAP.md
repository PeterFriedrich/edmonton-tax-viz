# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~8,296-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (319 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 650–654 |  |
| `HOME` | 655–655 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 656–669 |  |
| `WINDOWS` | 670–695 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 696–705 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 706–710 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 711–786 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `money0` | 787–789 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `fmtMoney` | 790–791 |  |
| `METRICS` | 792–894 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 895–911 |  |
| `RATIO_DENOMS` | 912–945 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 946–946 |  |
| `ratioOf` | 947–947 |  |
| `ratioKept` | 948–969 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 970–980 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 981–1008 |  |
| `dominantUse` | 1009–1050 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1051–1201 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1202–1297 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1298–1302 | the Lab: a container for unfinished lenses |
| `inLab` | 1303–1304 |  |
| `DEVIATION_TITLES` | 1305–1309 |  |
| `deviationTitle` | 1310–1315 |  |
| `deviationKind` | 1316–1318 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1319–1326 |  |
| `changeBlurb` | 1327–1344 | Change-lens blurb (COPY_DECISIONS BC1, B8 shape). It follows the window |
| `glassLead` | 1345–1357 | Grid blurb (COPY_DECISIONS BG1, B8 shape). Names the metric (B6) and the |
| `glassInstBlurb` | 1358–1370 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1371–1379 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `ratioBlurb` | 1380–1388 | Ratio blurb (COPY_DECISIONS BR1, B8 shape): the denominator's P1, a |
| `amenityWhichPhrase` | 1389–1394 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1395–1402 |  |
| `infillAmenityBlurb` | 1403–1416 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1417–1428 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `devTitle` | 1429–1434 | Development blurb, in the COPY_DECISIONS B8 shape (BD1): what the lens |
| `devBlurb` | 1435–1493 |  |
| `setBlurb` | 1494–1506 | Blurb markup (COPY_DECISIONS B8): a blank line starts a new paragraph and |
| `currentBlurb` | 1507–1522 | The active view's blurb. Read by applyView and by the camera's 2D/3D flip |
| `withColourClause` | 1523–1540 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1541–1547 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1548–1561 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1562–1562 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1563–1577 |  |
| `fmtMB` | 1578–1588 |  |
| `showGridBusy` | 1589–1611 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1612–1628 |  |
| `loadGridData` | 1629–1682 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1683–1736 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1737–1761 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1762–1793 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1794–1794 |  |
| `gridFetches` | 1795–1820 |  |
| `RAMPS` | 1821–1861 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1862–1868 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1869–1874 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1875–1875 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1876–1882 |  |
| `AMENITY_BANDS` | 1883–1884 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1885–1887 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1888–1893 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1894–1908 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1909–1914 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1915–1933 |  |
| `gridScale` | 1934–1954 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 1955–1961 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1962–1973 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1974–1976 |  |
| `quantile` | 1977–1991 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1992–2026 |  |
| `moneyBlurb` | 2027–2038 | The money blurb (COPY_DECISIONS BM1, B8 shape): the metric's own P1 under |
| `fillFor` | 2039–2051 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2052–2130 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2131–2131 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2132–2158 |  |
| `failLoading` | 2159–2172 |  |
| `hideLoading` | 2173–2227 |  |
| `topRings` | 2228–2244 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2245–2270 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2271–2271 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2272–2284 |  |
| `svcT` | 2285–2293 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2294–2307 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2308–2308 |  |
| `fmtFire` | 2309–2310 |  |
| `fmtTransit` | 2311–2312 |  |
| `fmtBike` | 2313–2325 |  |
| `fmtRoadM` | 2326–2339 |  |
| `fmtResShare` | 2340–2342 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2343–2348 |  |
| `fmtRoadsCost` | 2349–2353 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2354–2355 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2356–2357 |  |
| `fmtBikeCost` | 2358–2369 |  |
| `servicePlaneLayer` | 2370–2402 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2403–2412 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2413–2418 |  |
| `DEV_IND_TOTAL` | 2419–2421 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2422–2427 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2428–2432 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2433–2438 |  |
| `devGridOfferable` | 2439–2440 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2441–2441 |  |
| `devCol` | 2442–2442 |  |
| `_devScale` | 2443–2443 |  |
| `devScale` | 2444–2450 |  |
| `devT` | 2451–2454 |  |
| `developmentPlaneLayer` | 2455–2471 |  |
| `fmtDev` | 2472–2487 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2488–2493 |  |
| `DEV_GRID_IND_N` | 2494–2494 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2495–2497 |  |
| `devGridScale` | 2498–2524 |  |
| `devGridLayer` | 2525–2573 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2574–2575 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2576–2583 |  |
| `_infillStats` | 2584–2584 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2585–2602 |  |
| `_infillRaw` | 2603–2605 |  |
| `infillScore` | 2606–2621 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2622–2623 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2624–2641 |  |
| `INFILL_CENTER` | 2642–2642 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2643–2643 |  |
| `INFILL_NEG` | 2644–2644 |  |
| `infillColorAt` | 2645–2649 |  |
| `infillPlaneLayer` | 2650–2671 |  |
| `fmtFar` | 2672–2681 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `AMENITY_HIGHLIGHT_COLOR` | 2682–2682 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2683–2737 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2738–2745 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2746–2760 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2761–2781 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2782–2782 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2783–2797 |  |
| `chgT` | 2798–2807 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2808–2838 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2839–2927 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2928–2935 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2936–2936 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2937–2944 |  |
| `deviationRate` | 2945–2987 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2988–2988 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 2989–3018 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3019–3025 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3026–3037 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3038–3041 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3042–3046 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3047–3057 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3058–3073 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3074–3105 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3106–3130 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `INST_OUTLINE_COLOR` | 3131–3183 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 3184–3188 |  |
| `bandHover` | 3189–3197 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3198–3300 |  |

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
| `ensureReference` | 3945–3958 |  |
| `servicesBlurb` | 3959–3970 | Services-view blurb (COPY_DECISIONS BS1, B8 shape): the colour-driving |
| `hoodHoverLayer` | 3971–3994 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 3995–4005 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 4006–4057 |  |
| `REF_TIERS` | 4058–4079 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4080–4087 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 4088–4090 |  |
| `placeAnchors` | 4091–4114 |  |
| `labelPool` | 4115–4122 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4123–4176 |  |
| `CHROME_IDS` | 4177–4181 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4182–4200 |  |
| `visibleLabels` | 4201–4255 |  |
| `labelLayer` | 4256–4292 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 4293–4293 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4294–4309 |  |
| `ratioT` | 4310–4332 |  |
| `zMatrix` | 4333–4337 |  |
| `buildLayers` | 4338–4361 |  |
| `flattenDuringEase` | 4362–4386 | Center 2D lowers the heights over the LAST QUARTER OF THE TILT instead |
| `buildViewLayers` | 4387–4696 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4697–4726 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4727–4736 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4737–4739 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 4740–4771 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4772–4778 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4779–4786 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4787–4791 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4792–4802 |  |
| `revenueLens` | 4803–4804 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4805–4837 |  |
| `SVC_COST_BASES` | 4838–4855 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 4856–4864 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 4865–4874 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 4875–4877 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 4878–4884 |  |
| `svcRank` | 4885–4889 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 4890–4896 |  |
| `svcDriverReading` | 4897–4917 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 4918–4918 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4919–4922 |  |
| `servicePanelFor` | 4923–4927 |  |
| `ratioPanelFor` | 4928–4951 | Ratio carries the cost-as-a-share-of-tax panel that Services had until |
| `hoodPanelLens` | 4952–4956 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4957–4974 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4975–5006 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 5007–5012 |  |
| `sparklineSvg` | 5013–5028 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 5029–5088 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5089–5094 | Development history: new supply per year |
| `devHistKey` | 5095–5104 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5105–5109 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5110–5110 |  |
| `devHistVerb` | 5111–5116 |  |
| `devHistoryFor` | 5117–5152 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5153–5172 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5173–5192 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5193–5228 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5229–5231 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5232–5295 |  |
| `syncTemporalPos` | 5296–5322 |  |
| `openTemporal` | 5323–5359 |  |
| `renderRevenueMix` | 5360–5429 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderRatioCost` | 5430–5504 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `renderServiceCost` | 5505–5562 | The Services panel: what each cost IS for this hood, in dollars, and where |
| `fmtSvcRatio` | 5563–5566 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5567–5617 |  |
| `syncPinnedPanel` | 5618–5651 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5652–5667 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5668–5685 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5686–5733 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5734–5739 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5740–5787 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5788–5804 |  |
| `temporalClick` | 5805–5862 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 5863–5931 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 5932–6309 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6310–6399 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6400–6400 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6401–6419 |  |
| `syncMetricButtons` | 6420–6443 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6444–6450 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6451–6464 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6465–6506 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6507–6549 |  |
| `toggleBudgetPanel` | 6550–6575 |  |
| `syncMillRates` | 6576–6608 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 6609–6629 |  |
| `applyColorAdjust` | 6630–6650 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 6651–6663 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 6664–6678 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 6679–6696 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 6697–6713 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 6714–6735 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 6736–6752 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 6753–6992 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 6993–7003 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 7004–7017 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 7018–7026 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 7027–7037 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 7038–7049 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 7050–7062 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 7063–7083 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 7084–7131 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7132–7137 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7138–7159 |  |
| `applyMoneyDetail` | 7160–7184 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7185–7196 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7197–7204 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7205–7223 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7224–7234 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7235–7242 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7243–7259 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7260–7273 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7274–7284 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7285–7528 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7529–7538 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7539–7552 |  |
| `applySvcDriver` | 7553–7577 |  |

### shareable URL: the hash names the view on screen

| symbol | lines | what it does |
|---|---|---|
| `METRIC_FROM_URL` | 7578–7580 |  |
| `urlHash` | 7581–7621 |  |
| `writeUrlHash` | 7622–7630 | Absolute on purpose: the full build carries <base href="../">, and a |
| `offered` | 7631–7637 | On screen, ignoring the Options fold: a folded panel on a phone hides |
| `applyUrlState` | 7638–7710 |  |
| `restoreFromHash` | 7711–7722 | Once, at the end of boot, after every build and data gate has run. The |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 7723–8296 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (1022 edges)

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
| shareable URL: the hash names the view on screen | 23 | 22% |
| control appliers + the view/legend dispatchers | 218 | 20% |
| services lens views (SPEC_services.md display architecture) | 5 | 20% |
| the citywide budget panel (EXPERIMENTAL, full build only) | 12 | 8% |
| services view (SPEC_services.md UI generalization, 2026-07-05) | 18 | 0% |
| the institutional uncertainty band | 2 | 0% |
| temporal lens (SPEC_temporal.md phase 3) | 4 | 0% |
| boot | 61 | 0% |

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
| `#about-updated` | 573 |
| `#botleft` | 577 |
| `#compass` | 578 |
| `#rot-ccw` | 579 |
| `#tonorth` | 586 |
| `#needle` | 588 |
| `#rot-cw` | 593 |
| `#viewbtns` | 601 |
| `#recenter` | 603 |
| `#center2d` | 604 |
| `#legend` | 606 |
| `#legend-label` | 607 |
| `#legend-min` | 609 |
| `#legend-max` | 609 |
| `#legend-cats` | 611 |
| `#revmix` | 5379 |
| `#svccost` | 5473 |
