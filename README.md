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

## Methodology (Planned)

This project follows the **revenue-per-acre** framework developed by [Urban3](https://www.urbanthree.com/) and popularized by [Strong Towns](https://www.strongtowns.org/), adapted for Edmonton's data environment.

**Core calculation:**
```
Assessed Value ÷ Parcel/Neighbourhood Area = Value per Acre
```

Layering in service cost estimates (road maintenance, water/sewer, emergency services) produces a net fiscal picture per area.

**Data sources:**
- [Edmonton Property Assessment Data](https://data.edmonton.ca/City-Administration/Property-Assessment-Data-Current-Calendar-Year-/q7d6-ambg) (~448,000 records, updated annually)
- Edmonton neighbourhood boundary shapefiles
- Parcel boundary data (via AltaLIS or FOIP request — still being pursued)
- Published infrastructure cost studies for service cost allocation

**Tooling:** QGIS, Python/Pandas, open data only where possible.

## The Data Challenge

Edmonton transferred parcel-level GIS boundary data to AltaLIS (a provincial partnership) in November 2021 — it's no longer freely available. This is a real obstacle. The current plan is to:

1. Start with **neighbourhood-level aggregation** using free boundary files
2. Pursue parcel data via University of Alberta's GEODE consortium (academic access)
3. Submit a FOIP request to the City for parcel area data
4. Use manual sampling for high-contrast spotlight comparisons

The neighbourhood-level approach still supports analysis at this resolution — Ottawa's Hemson study and the Halifax infrastructure cost research both operated at similar levels of aggregation.

## Comparable Work

- **Ottawa (2021):** Hemson Consulting analysis found suburban greenfield development runs a **$465/person/year deficit** while high-density infill generates a **$606/person/year surplus**. Councillor Shawn Menard requested and publicized this; it became a major input to Ottawa's growth strategy.
- **Lafayette, LA:** Urban3's parcel-by-parcel analysis found $32 billion in infrastructure obligations against $16 million in annual maintenance revenue. Apparently the most comprehensive fiscal analysis done for a North American city.
- **Halifax:** Academic cost-of-service study across 8 settlement types found road costs of $1,053/household/year at low density vs. $26 at high density — roughly a **40:1 ratio**.
- **Arlington, VA (Rosslyn–Ballston corridor):** Transit-oriented corridor occupying roughly **8% of the county's land** generates about **33% of its tax revenue**, alongside some of the lowest tax rates in Northern Virginia — a revenue-side example at scale.
- **Calgary (2022):** Revenue-only analysis without a cost side.

## Status

**Live:** interactive 3D map at **https://peterfriedrich.github.io/edmonton-tax-viz/**
— municipal tax revenue (and assessed value) per acre by neighbourhood, with a
land-use set-aside layer and a residential-only lens. The **cost side is now
open** (`docs/SPEC_services.md`): a Roads view renders the city-maintained road
network coloured by road supply per acre, and a Ratio view shows **revenue per
road metre** — how much municipal revenue backs each metre of neighbourhood
road. A weekly GitHub Action regenerates the data and redeploys automatically
(see `docs/SPEC_deployment.md`).

See [`/research`](/research) for background findings and data source inventory.

## Technical Docs

- [`CONTRIBUTING.md`](CONTRIBUTING.md) — dev pipeline, setup, coding conventions, AI-assisted workflow
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — module contracts and data flow
- [`docs/SPEC_phase1.md`](docs/SPEC_phase1.md) — Phase 1 deliverable and acceptance criteria

## Contributing / Contact

This is an independent civic project. If you work in urban planning, municipal finance, or GIS and want to collaborate — or if you have access to data that could help — get in touch.

For code contributions, see [`CONTRIBUTING.md`](CONTRIBUTING.md).

Aligned with the work of [Strong Towns YEG](https://strongtownsyeg.ca/).
