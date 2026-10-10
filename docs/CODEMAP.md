# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~8,850-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (323 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `THEMED` | 734–736 | Colours that depend on the backdrop, one value per theme (docs/UI.md → |
| `themed` | 737–741 | Throws on a missing or mis-sized light value: deck draws `undefined` |
| `tc` | 742–747 |  |
| `CENTER` | 748–752 |  |
| `HOME` | 753–753 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 754–767 |  |
| `WINDOWS` | 768–793 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 794–803 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 804–808 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 809–884 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `money0` | 885–887 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `fmtMoney` | 888–889 |  |
| `METRICS` | 890–1009 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `RATIO_DENOMS` | 1010–1043 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 1044–1044 |  |
| `ratioOf` | 1045–1045 |  |
| `ratioKept` | 1046–1067 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 1068–1080 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 1081–1108 |  |
| `dominantUse` | 1109–1150 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1151–1301 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1302–1397 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1398–1402 | the Lab: a container for unfinished lenses |
| `inLab` | 1403–1404 |  |
| `DEVIATION_TITLES` | 1405–1409 |  |
| `deviationTitle` | 1410–1415 |  |
| `deviationKind` | 1416–1418 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1419–1426 |  |
| `changeBlurb` | 1427–1444 | Change-lens blurb (COPY_DECISIONS BC1, B8 shape). It follows the window |
| `glassLead` | 1445–1457 | Grid blurb (COPY_DECISIONS BG1, B8 shape). Names the metric (B6) and the |
| `glassInstBlurb` | 1458–1470 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1471–1479 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `ratioBlurb` | 1480–1488 | Ratio blurb (COPY_DECISIONS BR1, B8 shape): the denominator's P1, a |
| `amenityWhichPhrase` | 1489–1494 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1495–1502 |  |
| `infillAmenityBlurb` | 1503–1516 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1517–1528 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `devTitle` | 1529–1534 | Development blurb, in the COPY_DECISIONS B8 shape (BD1): what the lens |
| `devBlurb` | 1535–1596 |  |
| `setBlurb` | 1597–1611 | Blurb markup (COPY_DECISIONS B8): a blank line starts a new paragraph and |
| `currentBlurb` | 1612–1627 | The active view's blurb. Read by applyView and by the camera's 2D/3D flip |
| `withColourClause` | 1628–1645 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1646–1652 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1653–1666 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1667–1667 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1668–1682 |  |
| `fmtMB` | 1683–1693 |  |
| `showGridBusy` | 1694–1716 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1717–1733 |  |
| `loadGridData` | 1734–1787 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1788–1841 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1842–1866 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1867–1899 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1900–1900 |  |
| `gridFetches` | 1901–1927 |  |
| `RAMPS` | 1928–1980 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `THEME_RAMPS` | 1981–2015 | The ramps for a light backdrop, per theme (docs/UI.md → Light mode, phase |
| `activeRamp` | 2016–2029 | The ramp actually drawn: the palette choice under the current theme. |
| `rampSetAside` | 2030–2042 | The set-aside colour beside a RAMP-coloured surface. Only where the |
| `lotKey` | 2043–2043 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 2044–2050 |  |
| `AMENITY_BANDS` | 2051–2052 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 2053–2055 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 2056–2061 | Whether any band is actually filtering right now. |
| `amenityInBand` | 2062–2076 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 2077–2082 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 2083–2101 |  |
| `gridScale` | 2102–2122 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 2123–2129 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 2130–2141 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 2142–2144 |  |
| `quantile` | 2145–2159 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 2160–2194 |  |
| `moneyBlurb` | 2195–2206 | The money blurb (COPY_DECISIONS BM1, B8 shape): the metric's own P1 under |
| `fillFor` | 2207–2219 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2220–2273 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### base map (no basemap tiles for v1 — just a dark backdrop)

| symbol | lines | what it does |
|---|---|---|
| `GRID_INK` | 2274–2274 |  |
| `gridName` | 2275–2288 |  |
| `paintBackdrop` | 2289–2327 | The backdrop's three MapLibre layers, after a theme or ramp change. |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2328–2328 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2329–2355 |  |
| `failLoading` | 2356–2369 |  |
| `hideLoading` | 2370–2425 |  |
| `topRings` | 2426–2442 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2443–2468 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2469–2469 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2470–2482 |  |
| `svcT` | 2483–2491 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2492–2505 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2506–2506 |  |
| `fmtFire` | 2507–2508 |  |
| `fmtTransit` | 2509–2510 |  |
| `fmtBike` | 2511–2523 |  |
| `fmtRoadM` | 2524–2537 |  |
| `fmtResShare` | 2538–2540 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2541–2546 |  |
| `fmtRoadsCost` | 2547–2551 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2552–2553 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2554–2555 |  |
| `fmtBikeCost` | 2556–2567 |  |
| `servicePlaneLayer` | 2568–2600 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2601–2610 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2611–2616 |  |
| `DEV_IND_TOTAL` | 2617–2619 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2620–2625 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2626–2630 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2631–2636 |  |
| `devGridOfferable` | 2637–2638 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2639–2639 |  |
| `devCol` | 2640–2640 |  |
| `_devScale` | 2641–2641 |  |
| `devScale` | 2642–2648 |  |
| `devT` | 2649–2652 |  |
| `developmentPlaneLayer` | 2653–2669 |  |
| `fmtDev` | 2670–2685 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2686–2691 |  |
| `DEV_GRID_IND_N` | 2692–2692 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2693–2695 |  |
| `devGridScale` | 2696–2722 |  |
| `devGridLayer` | 2723–2771 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2772–2773 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2774–2781 |  |
| `_infillStats` | 2782–2782 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2783–2800 |  |
| `_infillRaw` | 2801–2803 |  |
| `infillScore` | 2804–2819 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2820–2821 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2822–2842 |  |
| `infillColorAt` | 2843–2847 |  |
| `infillPlaneLayer` | 2848–2869 |  |
| `fmtFar` | 2870–2880 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `amenityHighlightGridLayer` | 2881–2935 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2936–2943 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2944–2958 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2959–2979 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2980–2980 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2981–2995 |  |
| `chgT` | 2996–3005 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 3006–3036 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 3037–3125 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 3126–3133 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 3134–3134 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 3135–3142 |  |
| `deviationRate` | 3143–3186 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `exemptFrac` | 3187–3216 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3217–3223 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3224–3235 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3236–3239 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3240–3244 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3245–3255 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3256–3271 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3272–3303 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3304–3381 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `isBandLayer` | 3382–3386 |  |
| `bandHover` | 3387–3395 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3396–3498 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3499–3506 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3507–3508 |  |
| `glassInstBandLayers` | 3509–3549 |  |
| `ratioInstBandLayers` | 3550–3577 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3578–3590 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3591–3592 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3593–3594 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3595–3595 |  |
| `deviationStats` | 3596–3640 |  |
| `deviationOf` | 3641–3642 |  |
| `deviationT` | 3643–3653 |  |
| `fmtDeviation` | 3654–3675 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3676–3719 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3720–3806 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3807–3831 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `fireStationsLayer` | 3832–3852 |  |
| `ensureFireStations` | 3853–3869 |  |
| `transitStationsLayer` | 3870–3887 |  |
| `ensureTransitStations` | 3888–3904 |  |
| `lrtLinesLayer` | 3905–3921 |  |
| `ensureLrtLines` | 3922–3939 |  |
| `bikeLinesLayer` | 3940–3956 |  |
| `ensureBikeLines` | 3957–4043 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `referenceSplit` | 4044–4071 |  |
| `referenceUnderLayers` | 4072–4106 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 4107–4123 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 4124–4143 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 4144–4158 |  |
| `servicesBlurb` | 4159–4170 | Services-view blurb (COPY_DECISIONS BS1, B8 shape): the colour-driving |
| `hoodHoverLayer` | 4171–4194 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 4195–4205 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 4206–4257 |  |
| `REF_TIERS` | 4258–4279 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4280–4288 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `placeAnchors` | 4289–4312 |  |
| `labelPool` | 4313–4320 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4321–4374 |  |
| `CHROME_IDS` | 4375–4379 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4380–4398 |  |
| `visibleLabels` | 4399–4453 |  |
| `labelLayer` | 4454–4508 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `withSelectedHood` | 4509–4549 |  |
| `_ratioScales` | 4550–4550 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4551–4566 |  |
| `ratioT` | 4567–4589 |  |
| `zMatrix` | 4590–4594 |  |
| `buildLayers` | 4595–4619 |  |
| `flattenDuringEase` | 4620–4644 | Center 2D lowers the heights over the LAST QUARTER OF THE TILT instead |
| `buildViewLayers` | 4645–4959 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4960–4989 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4990–4999 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 5000–5002 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 5003–5034 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 5035–5041 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 5042–5049 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 5050–5054 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 5055–5065 |  |
| `revenueLens` | 5066–5067 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 5068–5100 |  |
| `SVC_COST_BASES` | 5101–5118 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 5119–5127 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 5128–5137 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 5138–5140 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 5141–5147 |  |
| `svcRank` | 5148–5152 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 5153–5159 |  |
| `svcDriverReading` | 5160–5180 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 5181–5181 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 5182–5185 |  |
| `servicePanelFor` | 5186–5190 |  |
| `ratioPanelFor` | 5191–5214 | Ratio carries the cost-as-a-share-of-tax panel that Services had until |
| `hoodPanelLens` | 5215–5219 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 5220–5237 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 5238–5269 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 5270–5275 |  |
| `sparklineSvg` | 5276–5291 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 5292–5351 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5352–5357 | Development history: new supply per year |
| `devHistKey` | 5358–5367 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5368–5372 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5373–5373 |  |
| `devHistVerb` | 5374–5379 |  |
| `devHistoryFor` | 5380–5418 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5419–5438 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5439–5458 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5459–5494 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5495–5497 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5498–5561 |  |
| `syncTemporalPos` | 5562–5588 |  |
| `openTemporal` | 5589–5626 |  |
| `renderRevenueMix` | 5627–5696 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderRatioCost` | 5697–5771 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `renderServiceCost` | 5772–5829 | The Services panel: what each cost IS for this hood, in dollars, and where |
| `fmtSvcRatio` | 5830–5833 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5834–5884 |  |
| `syncPinnedPanel` | 5885–5918 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5919–5934 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5935–5952 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5953–6000 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 6001–6006 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 6007–6054 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 6055–6071 |  |
| `temporalClick` | 6072–6126 | Click a hood to pin its history; click the pinned one again to unpin. |

### neighbourhood search

| symbol | lines | what it does |
|---|---|---|
| `searchNorm` | 6127–6134 | neighbourhood search |
| `searchMatches` | 6135–6149 | Ranked: the name starts with the query, then a later WORD does (so |
| `renderSearchList` | 6150–6178 |  |
| `openSearch` | 6179–6191 |  |
| `closeSearch` | 6192–6210 |  |

### how-to-read guide

| symbol | lines | what it does |
|---|---|---|
| `openGuide` | 6211–6223 |  |
| `closeGuide` | 6224–6231 |  |
| `maybeAutoGuide` | 6232–6248 |  |
| `flyToHood` | 6249–6268 | Keep the current tilt and rotation, so the camera moves TO the hood |
| `pickSearch` | 6269–6287 | A pick reads exactly like tapping or clicking the hood (temporalClick |
| `primaryRow` | 6288–6356 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 6357–6734 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6735–6824 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6825–6825 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6826–6844 |  |
| `syncMetricButtons` | 6845–6868 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6869–6875 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6876–6889 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6890–6931 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6932–6974 |  |
| `toggleBudgetPanel` | 6975–7000 |  |
| `syncMillRates` | 7001–7033 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 7034–7054 |  |
| `applyColorAdjust` | 7055–7075 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 7076–7088 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 7089–7103 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 7104–7121 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 7122–7138 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 7139–7160 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 7161–7177 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 7178–7417 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 7418–7430 | Legend rows for the uses view: the categories actually on screen |
| `applyTheme` | 7431–7447 | Switch theme. Every tc() colour and the ramp (activeRamp) are re-read on |
| `syncThemeChrome` | 7448–7458 | The theme's wording and buttons outside the map. Also run once at boot, |
| `applyPalette` | 7459–7473 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 7474–7482 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 7483–7493 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 7494–7505 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 7506–7518 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 7519–7539 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 7540–7587 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7588–7593 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7594–7615 |  |
| `applyMoneyDetail` | 7616–7640 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7641–7652 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7653–7660 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7661–7679 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7680–7690 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7691–7698 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7699–7715 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7716–7729 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7730–7740 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7741–7985 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7986–7995 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7996–8009 |  |
| `applySvcDriver` | 8010–8042 |  |

### shareable URL: the hash names the view on screen

| symbol | lines | what it does |
|---|---|---|
| `METRIC_FROM_URL` | 8043–8045 |  |
| `urlHash` | 8046–8086 |  |
| `shareLink` | 8087–8095 | Absolute on purpose: the full build carries <base href="../">, and a |
| `copyShareLink` | 8096–8107 | With no clipboard (an insecure origin, a denied permission) the link goes |
| `offered` | 8108–8114 | On screen, ignoring the Options fold: a folded panel on a phone hides |
| `applyUrlState` | 8115–8187 |  |
| `restoreFromHash` | 8188–8206 | Once, at the end of boot, after every build and data gate has run. The |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 8207–8850 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (1097 edges)

⚠️ **A regex reference count, not a call graph** — a name in a comment or string counts, and a nested symbol is attributed to its enclosing range. Use it for *what is central* and *would this seam hold*, never as ground truth for a final module boundary.

**Most depended-on** — moving one of these touches everything below it.

| symbol | referenced by | section |
|---|---|---|
| `state` | 129 | the Lab: a container for unfinished lenses |
| `buildLayers` | 42 | geographic reference layers (all views) |
| `tc` | 27 | tunables |
| `themed` | 17 | tunables |
| `METRICS` | 17 | tunables |
| `applyView` | 17 | control appliers + the view/legend dispatchers |
| `SERVICES` | 16 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `refreshLegend` | 16 | control appliers + the view/legend dispatchers |
| `setBlurb` | 16 | the Lab: a container for unfinished lenses |
| `CELLS` | 11 | tunables |
| `quantile` | 10 | the Lab: a container for unfinished lenses |
| `ratioDenom` | 9 | services lens views (SPEC_services.md display architecture) |
| `ratioScale` | 9 | geographic reference layers (all views) |
| `deviationStats` | 9 | the same doubt, at 100 m |
| `esc` | 9 | money view (default): the classic metric prisms |

**Section self-containment** — share of each section's outgoing edges that stay inside it. Low means a module cut on this banner would mostly import its neighbours.

| section | edges | self-contained |
|---|---|---|
| the Lab: a container for unfinished lenses | 127 | 64% |
| tunables | 16 | 56% |
| Infill lens (SPEC_development.md Lens B) | 27 | 52% |
| uses view (use-mix, 2026-07-03) | 4 | 50% |
| deviation lens: revenue per developed acre against peer average | 4 | 50% |
| change lens: how each hood's share of the assessment base moved | 16 | 44% |
| base map (no basemap tiles for v1 — just a dark backdrop) | 5 | 40% |
| Development 100 m detail grid (layers-panel toggle, 2026-07-15) | 10 | 40% |
| neighbourhood search | 11 | 36% |
| geographic reference layers (all views) | 97 | 35% |
| loading overlay | 56 | 34% |
| Development history: new supply per year | 112 | 29% |
| Money's revenue panel: where a hood's levy comes from | 35 | 29% |
| two tiers, answering two different questions | 30 | 27% |
| shareable URL: the hash names the view on screen | 24 | 21% |
| control appliers + the view/legend dispatchers | 232 | 20% |
| services lens views (SPEC_services.md display architecture) | 5 | 20% |
| the same doubt, at 100 m | 66 | 18% |
| the citywide budget panel (EXPERIMENTAL, full build only) | 12 | 8% |
| how-to-read guide | 113 | 8% |
| services view (SPEC_services.md UI generalization, 2026-07-05) | 18 | 0% |
| the institutional uncertainty band | 2 | 0% |
| temporal lens (SPEC_temporal.md phase 3) | 4 | 0% |
| boot | 71 | 0% |

## Element ids (144) — the control surface

| id | line |
|---|---|
| `#map` | 39 |
| `#loading` | 43 |
| `#loading-box` | 44 |
| `#loading-title` | 55 |
| `#loading-blurb` | 56 |
| `#loading-spinner` | 57 |
| `#loading-text` | 58 |
| `#loading-retry` | 59 |
| `#banner` | 63 |
| `#gridbusy` | 74 |
| `#gridbusy-spinner` | 75 |
| `#gridbusy-text` | 77 |
| `#gridbusy-size` | 78 |
| `#title` | 82 |
| `#title-h` | 83 |
| `#title-p` | 87 |
| `#search` | 97 |
| `#search-btn` | 98 |
| `#search-box` | 101 |
| `#search-input` | 102 |
| `#search-close` | 106 |
| `#search-list` | 108 |
| `#guide-btn` | 116 |
| `#guide` | 118 |
| `#guide-close` | 119 |
| `#guide-ask` | 120 |
| `#guide-show` | 121 |
| `#guide-body` | 124 |
| `#temporal` | 143 |
| `#temporal-close` | 144 |
| `#temporal-name` | 145 |
| `#temporal-body` | 152 |
| `#temporal-chart` | 153 |
| `#temporal-read` | 154 |
| `#temporal-note` | 155 |
| `#temporal-hint` | 159 |
| `#millrates` | 175 |
| `#mill-head` | 176 |
| `#mill-rows` | 177 |
| `#mill-note` | 178 |
| `#budget` | 192 |
| `#budget-close` | 199 |
| `#budget-head` | 200 |
| `#budget-body` | 205 |
| `#budget-rows` | 206 |
| `#budget-other-hd` | 207 |
| `#budget-other` | 208 |
| `#budget-note` | 209 |
| `#peek` | 224 |
| `#peek-name` | 225 |
| `#peek-read` | 226 |
| `#peek-go` | 227 |
| `#controls` | 230 |
| `#toggle` | 243 |
| `#metric-row` | 244 |
| `#revcut` | 248 |
| `#moneymode` | 253 |
| `#views` | 259 |
| `#optpanel` | 273 |
| `#opt-fold` | 274 |
| `#opt-caret` | 274 |
| `#opt-body` | 275 |
| `#layers` | 276 |
| `#chgwindow-hd` | 277 |
| `#chgwindow` | 278 |
| `#labpick-hd` | 287 |
| `#labpick` | 288 |
| `#labcut-hd` | 289 |
| `#labcut` | 290 |
| `#moneydetail-hd` | 295 |
| `#moneydetail` | 296 |
| `#amenity-hd` | 321 |
| `#amenity` | 322 |
| `#amenity-lrt-row` | 323 |
| `#amenity-lrt-on` | 324 |
| `#amenity-school-row` | 326 |
| `#amenity-school-on` | 327 |
| `#uses-prisms-hd` | 330 |
| `#uses-prisms` | 331 |
| `#uses-prisms-on` | 333 |
| `#devmode-hd` | 336 |
| `#devmode` | 337 |
| `#devmetric-hd` | 341 |
| `#devmetric` | 342 |
| `#devwindow-hd` | 347 |
| `#devwindow` | 348 |
| `#devdetail-hd` | 353 |
| `#devdetail` | 354 |
| `#prism-hd` | 358 |
| `#prism-row` | 359 |
| `#prism-opacity` | 361 |
| `#prism-opacity-val` | 362 |
| `#services-hd` | 364 |
| `#services` | 365 |
| `#denom-hd` | 464 |
| `#denom` | 465 |
| `#ratio-denom-hd` | 469 |
| `#ratio-denom` | 470 |
| `#hoodmode` | 480 |
| `#hoodmode-btn` | 481 |
| `#coloradj` | 493 |
| `#coloradj-btn` | 494 |
| `#budget-pod` | 501 |
| `#budget-btn` | 502 |
| `#share` | 509 |
| `#share-btn` | 510 |
| `#a11y` | 513 |
| `#a11y-btn` | 514 |
| `#a11y-menu` | 515 |
| `#theme` | 517 |
| `#palette` | 522 |
| `#labels-on` | 529 |
| `#reference-on` | 537 |
| `#about` | 542 |
| `#about-btn` | 543 |
| `#about-menu` | 544 |
| `#about-src-roads` | 556 |
| `#about-src-services` | 557 |
| `#about-vintage` | 585 |
| `#about-build` | 589 |
| `#about-lot-acres` | 594 |
| `#about-modelled-roads` | 605 |
| `#about-modelled` | 627 |
| `#about-budget` | 637 |
| `#about-budget-lead` | 639 |
| `#about-budget-rows` | 640 |
| `#about-budget-note` | 641 |
| `#about-updated` | 653 |
| `#botleft` | 657 |
| `#compass` | 658 |
| `#rot-ccw` | 659 |
| `#tonorth` | 666 |
| `#needle` | 668 |
| `#rot-cw` | 673 |
| `#viewbtns` | 681 |
| `#recenter` | 683 |
| `#center2d` | 684 |
| `#legend` | 686 |
| `#legend-label` | 687 |
| `#legend-min` | 689 |
| `#legend-max` | 689 |
| `#legend-cats` | 691 |
| `#revmix` | 5646 |
| `#svccost` | 5740 |
