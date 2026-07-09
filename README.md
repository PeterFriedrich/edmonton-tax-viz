# Edmonton Revenue Per Acre Analysis

A public fiscal analysis comparing Edmonton's property tax revenue to the cost of servicing it, by area.

[Edmonton Tax Visualization](https://peterfriedrich.github.io/edmonton-tax-viz/)

## What This Is

Several published studies have examined the fiscal balance of suburban development in Edmonton. A Sustainable Prosperity report found that costs to the city will exceed revenues by **nearly $4 billion over 60 years** across just 17 planned new developments. A 2016 analysis of three new neighbourhoods (Decoteau, Riverview, Horse Hills) found they'll cost **$1.4 billion more** than they'll generate over 50 years.

No comprehensive, public **revenue-per-acre analysis** has been published for Edmonton — the kind of spatial fiscal analysis that presents this data at the neighbourhood level for residents and councillors.

The goal: map Edmonton's property tax revenue and estimated service costs against land area, broken out by area and development pattern — downtown mixed-use and established infill areas alongside suburban greenfield expansion — and present the per-acre figures.

## Why Now

- Edmonton recently raised property taxes by **6.9%**
- Council is actively debating development costs and suburban expansion
- Edmonton has excellent open data infrastructure (~448,000 property assessment records publicly available)
- No comparable public analysis exists for Edmonton, despite Calgary and Ottawa having attempted versions of this work

## Methodology

This project is inspired by the **revenue-per-acre** framework developed by [Urban3](https://www.urbanthree.com/) and popularized by [Strong Towns](https://www.strongtowns.org/), adapted for Edmonton's data environment. (Methodological lineage note: Urban3's denominator is parcel acres — this project's **lot-acre** mode; the **ground-acre** default is this project's own robustness-motivated addition. See `docs/FINDINGS_denominator_cardinality.md`.)

**Core calculation:**
```
Municipal levy (or assessed value) ÷ Neighbourhood area = Revenue (value) per acre
```

with a toggleable denominator: **ground acres** (boundary area — robust to record-to-parcel cardinality issues) or **parcel/lot acres** (deduplicated titled lot area — the Urban3-analogous "developable land" view, with a low-parcel-fraction guard). The revenue numerator is the per-account municipal levy computed from assessed value × the class mill rate.

The **cost side** layers service supply and modeled service cost per acre: road network supply, a bylaw-native stormwater charge model, fire-rescue service demand, and a per-connection water/sanitary model — each validated against published figures where possible (`docs/FINDINGS_utility_validation.md`). Modeled figures are labeled *modeled, not billed*.

**Data sources (all open data):**
- [Property Assessment Data](https://data.edmonton.ca/City-Administration/Property-Assessment-Data-Current-Calendar-Year-/q7d6-ambg) (~440,000 records, refreshed weekly, annual roll)
- Neighbourhood boundaries, Zoning Bylaw geometry, road centrelines, fire-rescue events & stations, and property information (lot sizes) — all from the [Edmonton Open Data Portal](https://data.edmonton.ca/)
- Published mill rates and utility tariffs (EPCOR bylaw rates, franchise fee schedules)

**Tooling:** Python only (pandas + geopandas + shapely; deck.gl in the browser) — no GIS desktop software. The full pipeline regenerates from open data in one command and runs weekly in CI.

## The Data Challenge (resolved)

Edmonton transferred parcel-level GIS *boundary* data to AltaLIS in November 2021 — it's no longer freely available. The project resolved this without AltaLIS, GEODE, or FOIP:

1. **Neighbourhood-level aggregation** on the free boundary file is the primary unit — the same resolution as Ottawa's Hemson study and the Halifax cost-of-service research.
2. **Lot areas** (not boundary geometry) turn out to be in the open [Property Information dataset](https://data.edmonton.ca/) (`dkk9-cj3x`), which — with a repeat-aware deduplication heuristic for condo/multi-unit records (`docs/FINDINGS_lot_dedupe.md`) — supports the parcel-acre denominator and a 100 m grid view at near-Urban3 detail.

Work that would genuinely need parcel *geometry* is catalogued in `docs/PARCEL_LEVEL_OPPORTUNITIES.md`.

## Comparable Work

- **Ottawa (2021):** Hemson Consulting analysis found suburban greenfield development runs a **$465/person/year deficit** while high-density infill generates a **$606/person/year surplus**. Councillor Shawn Menard requested and publicized this; it became a major input to Ottawa's growth strategy.
- **Lafayette, LA:** Urban3's parcel-by-parcel analysis found $32 billion in infrastructure obligations against $16 million in annual maintenance revenue. Apparently the most comprehensive fiscal analysis done for a North American city.
- **Halifax:** Academic cost-of-service study across 8 settlement types found road costs of $1,053/household/year at low density vs. $26 at high density — roughly a **40:1 ratio**.
- **Arlington, VA (Rosslyn–Ballston corridor):** Transit-oriented corridor occupying roughly **8% of the county's land** generates about **33% of its tax revenue**, alongside some of the lowest tax rates in Northern Virginia — a revenue-side example at scale.
- **Calgary (2022):** Revenue-only analysis without a cost side.

## Status

**Live:** interactive 3D map at **https://peterfriedrich.github.io/edmonton-tax-viz/**
— municipal tax revenue (and assessed value) per acre by neighbourhood, with a
land-use set-aside layer and a residential-only lens. The **cost side is
built** (`docs/SPEC_services.md`, `docs/SPEC_utilities.md`): a Services view
layers the city-maintained road network (road supply per acre), a **modeled
stormwater charge** per acre, **fire-rescue service demand** per acre, and a
**modeled water/sanitary charge** per acre; a Ratio view shows **revenue per
road metre** — how much municipal revenue backs each metre of neighbourhood
road. A Uses view maps the zoning bylaw's land-use categories, and a Glass
view renders the metric in **100 m grid cells** (the Urban3-style detail
level). Both the Money and Glass views toggle between ground acres and
**parcel (lot) acres** as the denominator. A weekly GitHub Action regenerates
the data and redeploys automatically (see `docs/SPEC_deployment.md`).

See [`/research`](/research) for background findings and data source inventory.

## Technical Docs

- [`CONTRIBUTING.md`](CONTRIBUTING.md) — dev pipeline, setup, coding conventions, AI-assisted workflow
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — module contracts and data flow
- [`docs/SPEC_phase1.md`](docs/SPEC_phase1.md) — Phase 1 deliverable and acceptance criteria

## Contributing / Contact

This is an independent civic project. If you work in urban planning, municipal finance, or GIS and want to collaborate — or if you have access to data that could help — get in touch.

For code contributions, see [`CONTRIBUTING.md`](CONTRIBUTING.md).

Aligned with the work of [Strong Towns YEG](https://strongtownsyeg.ca/).
