# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~8,691-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (317 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `THEMED` | 707–707 | Colours that depend on the backdrop, one value per theme (docs/UI.md → |
| `themed` | 708–708 |  |
| `tc` | 709–714 |  |
| `CENTER` | 715–719 |  |
| `HOME` | 720–720 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 721–734 |  |
| `WINDOWS` | 735–760 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 761–770 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 771–775 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 776–851 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `money0` | 852–854 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `fmtMoney` | 855–856 |  |
| `METRICS` | 857–976 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `RATIO_DENOMS` | 977–1010 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 1011–1011 |  |
| `ratioOf` | 1012–1012 |  |
| `ratioKept` | 1013–1034 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 1035–1047 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 1048–1075 |  |
| `dominantUse` | 1076–1117 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1118–1268 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1269–1364 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1365–1369 | the Lab: a container for unfinished lenses |
| `inLab` | 1370–1371 |  |
| `DEVIATION_TITLES` | 1372–1376 |  |
| `deviationTitle` | 1377–1382 |  |
| `deviationKind` | 1383–1385 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1386–1393 |  |
| `changeBlurb` | 1394–1411 | Change-lens blurb (COPY_DECISIONS BC1, B8 shape). It follows the window |
| `glassLead` | 1412–1424 | Grid blurb (COPY_DECISIONS BG1, B8 shape). Names the metric (B6) and the |
| `glassInstBlurb` | 1425–1437 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1438–1446 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `ratioBlurb` | 1447–1455 | Ratio blurb (COPY_DECISIONS BR1, B8 shape): the denominator's P1, a |
| `amenityWhichPhrase` | 1456–1461 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1462–1469 |  |
| `infillAmenityBlurb` | 1470–1483 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1484–1495 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `devTitle` | 1496–1501 | Development blurb, in the COPY_DECISIONS B8 shape (BD1): what the lens |
| `devBlurb` | 1502–1560 |  |
| `setBlurb` | 1561–1573 | Blurb markup (COPY_DECISIONS B8): a blank line starts a new paragraph and |
| `currentBlurb` | 1574–1589 | The active view's blurb. Read by applyView and by the camera's 2D/3D flip |
| `withColourClause` | 1590–1607 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1608–1614 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1615–1628 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1629–1629 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1630–1644 |  |
| `fmtMB` | 1645–1655 |  |
| `showGridBusy` | 1656–1678 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1679–1695 |  |
| `loadGridData` | 1696–1749 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1750–1803 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1804–1828 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1829–1860 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1861–1861 |  |
| `gridFetches` | 1862–1888 |  |
| `RAMPS` | 1889–1939 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `rampSetAside` | 1940–1952 | The set-aside colour beside a RAMP-coloured surface. Only where the |
| `lotKey` | 1953–1953 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1954–1960 |  |
| `AMENITY_BANDS` | 1961–1962 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1963–1965 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1966–1971 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1972–1986 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1987–1992 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1993–2011 |  |
| `gridScale` | 2012–2032 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 2033–2039 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 2040–2051 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 2052–2054 |  |
| `quantile` | 2055–2069 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 2070–2104 |  |
| `moneyBlurb` | 2105–2116 | The money blurb (COPY_DECISIONS BM1, B8 shape): the metric's own P1 under |
| `fillFor` | 2117–2129 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2130–2208 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2209–2209 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2210–2236 |  |
| `failLoading` | 2237–2250 |  |
| `hideLoading` | 2251–2306 |  |
| `topRings` | 2307–2323 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2324–2349 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2350–2350 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2351–2363 |  |
| `svcT` | 2364–2372 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2373–2386 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2387–2387 |  |
| `fmtFire` | 2388–2389 |  |
| `fmtTransit` | 2390–2391 |  |
| `fmtBike` | 2392–2404 |  |
| `fmtRoadM` | 2405–2418 |  |
| `fmtResShare` | 2419–2421 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2422–2427 |  |
| `fmtRoadsCost` | 2428–2432 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2433–2434 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2435–2436 |  |
| `fmtBikeCost` | 2437–2448 |  |
| `servicePlaneLayer` | 2449–2481 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2482–2491 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2492–2497 |  |
| `DEV_IND_TOTAL` | 2498–2500 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2501–2506 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2507–2511 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2512–2517 |  |
| `devGridOfferable` | 2518–2519 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2520–2520 |  |
| `devCol` | 2521–2521 |  |
| `_devScale` | 2522–2522 |  |
| `devScale` | 2523–2529 |  |
| `devT` | 2530–2533 |  |
| `developmentPlaneLayer` | 2534–2550 |  |
| `fmtDev` | 2551–2566 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2567–2572 |  |
| `DEV_GRID_IND_N` | 2573–2573 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2574–2576 |  |
| `devGridScale` | 2577–2603 |  |
| `devGridLayer` | 2604–2652 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2653–2654 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2655–2662 |  |
| `_infillStats` | 2663–2663 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2664–2681 |  |
| `_infillRaw` | 2682–2684 |  |
| `infillScore` | 2685–2700 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2701–2702 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2703–2723 |  |
| `infillColorAt` | 2724–2728 |  |
| `infillPlaneLayer` | 2729–2750 |  |
| `fmtFar` | 2751–2761 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `amenityHighlightGridLayer` | 2762–2816 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2817–2824 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2825–2839 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2840–2860 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2861–2861 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2862–2876 |  |
| `chgT` | 2877–2886 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2887–2917 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2918–3006 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 3007–3014 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 3015–3015 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 3016–3023 |  |
| `deviationRate` | 3024–3067 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `exemptFrac` | 3068–3097 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3098–3104 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3105–3116 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3117–3120 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3121–3125 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3126–3136 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3137–3152 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3153–3184 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3185–3262 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `isBandLayer` | 3263–3267 |  |
| `bandHover` | 3268–3276 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3277–3379 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3380–3387 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3388–3389 |  |
| `glassInstBandLayers` | 3390–3430 |  |
| `ratioInstBandLayers` | 3431–3458 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3459–3471 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3472–3473 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3474–3475 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3476–3476 |  |
| `deviationStats` | 3477–3521 |  |
| `deviationOf` | 3522–3523 |  |
| `deviationT` | 3524–3534 |  |
| `fmtDeviation` | 3535–3556 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3557–3600 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3601–3687 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3688–3712 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `fireStationsLayer` | 3713–3733 |  |
| `ensureFireStations` | 3734–3750 |  |
| `transitStationsLayer` | 3751–3768 |  |
| `ensureTransitStations` | 3769–3785 |  |
| `lrtLinesLayer` | 3786–3802 |  |
| `ensureLrtLines` | 3803–3820 |  |
| `bikeLinesLayer` | 3821–3837 |  |
| `ensureBikeLines` | 3838–3924 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `referenceSplit` | 3925–3952 |  |
| `referenceUnderLayers` | 3953–3987 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3988–4004 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 4005–4024 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 4025–4038 |  |
| `servicesBlurb` | 4039–4050 | Services-view blurb (COPY_DECISIONS BS1, B8 shape): the colour-driving |
| `hoodHoverLayer` | 4051–4074 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 4075–4085 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 4086–4137 |  |
| `REF_TIERS` | 4138–4159 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4160–4168 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `placeAnchors` | 4169–4192 |  |
| `labelPool` | 4193–4200 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4201–4254 |  |
| `CHROME_IDS` | 4255–4259 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4260–4278 |  |
| `visibleLabels` | 4279–4333 |  |
| `labelLayer` | 4334–4388 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `withSelectedHood` | 4389–4429 |  |
| `_ratioScales` | 4430–4430 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4431–4446 |  |
| `ratioT` | 4447–4469 |  |
| `zMatrix` | 4470–4474 |  |
| `buildLayers` | 4475–4499 |  |
| `flattenDuringEase` | 4500–4524 | Center 2D lowers the heights over the LAST QUARTER OF THE TILT instead |
| `buildViewLayers` | 4525–4839 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4840–4869 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4870–4879 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4880–4882 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 4883–4914 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4915–4921 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4922–4929 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4930–4934 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4935–4945 |  |
| `revenueLens` | 4946–4947 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4948–4980 |  |
| `SVC_COST_BASES` | 4981–4998 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 4999–5007 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 5008–5017 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 5018–5020 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 5021–5027 |  |
| `svcRank` | 5028–5032 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 5033–5039 |  |
| `svcDriverReading` | 5040–5060 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 5061–5061 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 5062–5065 |  |
| `servicePanelFor` | 5066–5070 |  |
| `ratioPanelFor` | 5071–5094 | Ratio carries the cost-as-a-share-of-tax panel that Services had until |
| `hoodPanelLens` | 5095–5099 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 5100–5117 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 5118–5149 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 5150–5155 |  |
| `sparklineSvg` | 5156–5171 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 5172–5231 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5232–5237 | Development history: new supply per year |
| `devHistKey` | 5238–5247 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5248–5252 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5253–5253 |  |
| `devHistVerb` | 5254–5259 |  |
| `devHistoryFor` | 5260–5298 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5299–5318 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5319–5338 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5339–5374 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5375–5377 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5378–5441 |  |
| `syncTemporalPos` | 5442–5468 |  |
| `openTemporal` | 5469–5506 |  |
| `renderRevenueMix` | 5507–5576 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderRatioCost` | 5577–5651 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `renderServiceCost` | 5652–5709 | The Services panel: what each cost IS for this hood, in dollars, and where |
| `fmtSvcRatio` | 5710–5713 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5714–5764 |  |
| `syncPinnedPanel` | 5765–5798 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5799–5814 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5815–5832 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5833–5880 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5881–5886 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5887–5934 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5935–5951 |  |
| `temporalClick` | 5952–6006 | Click a hood to pin its history; click the pinned one again to unpin. |

### neighbourhood search

| symbol | lines | what it does |
|---|---|---|
| `searchNorm` | 6007–6014 | neighbourhood search |
| `searchMatches` | 6015–6029 | Ranked: the name starts with the query, then a later WORD does (so |
| `renderSearchList` | 6030–6058 |  |
| `openSearch` | 6059–6071 |  |
| `closeSearch` | 6072–6090 |  |

### how-to-read guide

| symbol | lines | what it does |
|---|---|---|
| `openGuide` | 6091–6103 |  |
| `closeGuide` | 6104–6111 |  |
| `maybeAutoGuide` | 6112–6128 |  |
| `flyToHood` | 6129–6148 | Keep the current tilt and rotation, so the camera moves TO the hood |
| `pickSearch` | 6149–6167 | A pick reads exactly like tapping or clicking the hood (temporalClick |
| `primaryRow` | 6168–6236 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 6237–6614 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6615–6704 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6705–6705 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6706–6724 |  |
| `syncMetricButtons` | 6725–6748 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6749–6755 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6756–6769 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6770–6811 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6812–6854 |  |
| `toggleBudgetPanel` | 6855–6880 |  |
| `syncMillRates` | 6881–6913 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 6914–6934 |  |
| `applyColorAdjust` | 6935–6955 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 6956–6968 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 6969–6983 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 6984–7001 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 7002–7018 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 7019–7040 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 7041–7057 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 7058–7297 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 7298–7310 | Legend rows for the uses view: the categories actually on screen |
| `applyTheme` | 7311–7318 | Switch theme. Every tc() colour is re-read on the rebuild, because |
| `applyPalette` | 7319–7334 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 7335–7343 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 7344–7354 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 7355–7366 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 7367–7379 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 7380–7400 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 7401–7448 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7449–7454 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7455–7476 |  |
| `applyMoneyDetail` | 7477–7501 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7502–7513 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7514–7521 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7522–7540 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7541–7551 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7552–7559 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7560–7576 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7577–7590 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7591–7601 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7602–7845 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7846–7855 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7856–7869 |  |
| `applySvcDriver` | 7870–7902 |  |

### shareable URL: the hash names the view on screen

| symbol | lines | what it does |
|---|---|---|
| `METRIC_FROM_URL` | 7903–7905 |  |
| `urlHash` | 7906–7946 |  |
| `shareLink` | 7947–7955 | Absolute on purpose: the full build carries <base href="../">, and a |
| `copyShareLink` | 7956–7967 | With no clipboard (an insecure origin, a denied permission) the link goes |
| `offered` | 7968–7974 | On screen, ignoring the Options fold: a folded panel on a phone hides |
| `applyUrlState` | 7975–8047 |  |
| `restoreFromHash` | 8048–8066 | Once, at the end of boot, after every build and data gate has run. The |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 8067–8691 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (1077 edges)

⚠️ **A regex reference count, not a call graph** — a name in a comment or string counts, and a nested symbol is attributed to its enclosing range. Use it for *what is central* and *would this seam hold*, never as ground truth for a final module boundary.

**Most depended-on** — moving one of these touches everything below it.

| symbol | referenced by | section |
|---|---|---|
| `state` | 127 | the Lab: a container for unfinished lenses |
| `buildLayers` | 42 | geographic reference layers (all views) |
| `tc` | 27 | tunables |
| `themed` | 17 | tunables |
| `METRICS` | 17 | tunables |
| `applyView` | 17 | control appliers + the view/legend dispatchers |
| `SERVICES` | 16 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `refreshLegend` | 16 | control appliers + the view/legend dispatchers |
| `setBlurb` | 15 | the Lab: a container for unfinished lenses |
| `CELLS` | 11 | tunables |
| `quantile` | 10 | the Lab: a container for unfinished lenses |
| `ratioDenom` | 9 | services lens views (SPEC_services.md display architecture) |
| `ratioScale` | 9 | geographic reference layers (all views) |
| `deviationStats` | 9 | the same doubt, at 100 m |
| `esc` | 9 | money view (default): the classic metric prisms |

**Section self-containment** — share of each section's outgoing edges that stay inside it. Low means a module cut on this banner would mostly import its neighbours.

| section | edges | self-contained |
|---|---|---|
| the Lab: a container for unfinished lenses | 125 | 62% |
| tunables | 15 | 53% |
| Infill lens (SPEC_development.md Lens B) | 27 | 52% |
| uses view (use-mix, 2026-07-03) | 4 | 50% |
| deviation lens: revenue per developed acre against peer average | 4 | 50% |
| change lens: how each hood's share of the assessment base moved | 16 | 44% |
| Development 100 m detail grid (layers-panel toggle, 2026-07-15) | 10 | 40% |
| neighbourhood search | 11 | 36% |
| geographic reference layers (all views) | 96 | 34% |
| loading overlay | 56 | 34% |
| Development history: new supply per year | 112 | 29% |
| Money's revenue panel: where a hood's levy comes from | 35 | 29% |
| two tiers, answering two different questions | 30 | 27% |
| shareable URL: the hash names the view on screen | 24 | 21% |
| control appliers + the view/legend dispatchers | 223 | 21% |
| services lens views (SPEC_services.md display architecture) | 5 | 20% |
| the same doubt, at 100 m | 66 | 18% |
| the citywide budget panel (EXPERIMENTAL, full build only) | 12 | 8% |
| how-to-read guide | 113 | 8% |
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
| `#revmix` | 5526 |
| `#svccost` | 5620 |
