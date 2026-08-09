# Task Brief: Growth Infrastructure Financing Panel ("Debt Lens")

**For:** Fable
**From:** Planning conversation w/ Claude, [date: 2026-07-14]
**Status:** Ready to scope into tickets. Full research backing: *"Edmonton Growth Infrastructure Financing — Feasibility of a Neighbourhood Debt Lens"*. ⚠️ **NOT IN THIS REPO** — it lives in the Claude project knowledge, so nothing here can check it; treat any figure traced back to it as unsourced until it is copied in.

---

## Scope decision (read this first)

Do **NOT** build a "debt per parcel/neighbourhood" map. Municipal debt is issued citywide, not tagged to parcels or subdivisions anywhere in public data — any such number would be fabricated, not sourced.

Build instead, as **two separate, clearly-labelled components**:

1. **Growth-area financing transparency panel** (spatial, parcel/catchment-joinable) — shows what new development actually pays for vs. what falls to general ratepayers/City debt. This is the real "lens."
2. **Citywide debt context annotation** (non-spatial) — trend line + peer benchmark, presented as background, not mapped to geography.

Framing for both: "growth infrastructure financing transparency," not "debt attribution." This distinction should be explicit in UI copy — it's the load-bearing methodological claim.

---

## Component 1: Growth-area financing panel

### Spatial join key: 12 fire-hall off-site levy catchments

Source: 2026 Off-Site Levy Approved Rates (edmonton.ca/business_economy/off-site-levy-bylaw). These are named, bounded catchments — the only genuinely spatial, current, parcel-relevant financing data Edmonton publishes.

| Catchment | Facility cost | Area (ha) | Levy rate ($/ha) |
|---|---|---|---|
| Wedgewood | $26,143,915 | 622 | $42,032 |
| Blatchford | $25,757,959 | 785 | $32,813 |
| Riverview | $26,143,915 | 838 | $31,198 |
| Horse Hill | $26,143,915 | 905 | $28,888 |
| Northeast Horse Hill | $26,143,915 | 963 | $27,148 |
| Mistatim Industrial | $26,143,915 | 1,102 | $23,724 |
| Southeast | $26,143,915 | 1,181 | $22,137 |
| Walker | $24,043,915 | 1,095 | $21,958 |
| Big Lake | $26,143,915 | 1,214 | $21,535 |
| EETP | $26,143,915 | 1,268 | $20,618 |
| Cumberland | $26,143,915 | 1,338 | $19,540 |
| Northeast EETP | $26,143,915 | 2,040 | $12,816 |

**Task:** Get/digitize catchment boundary polygons if available (check if the off-site levy bylaw PDF or backgrounder has a map exhibit; may need to trace from PDF figure if no GIS layer exists — flag this as a data-acquisition risk early). Join to neighbourhood boundaries for display.

**Critical framing point:** Edmonton levies developers for fire halls ONLY. No levy for trunk roads/water/sanitary/stormwater (unlike Calgary/St. Albert, which levy $170K–$270K/ha combined for those). This asymmetry is the headline finding — make it visually obvious (e.g., "1 of 5 essential services levied" or similar).

### Levy performance data (shows levy is not keeping pace)

Off-Site Levy Annual Reports (2022/2023/2024, edmonton.ca):
- 2022: $297,366.50 collected, $0 spent
- 2023: $484,024.00 collected, $0 spent
- 2024: $3,033,592 collected (Table 6.1 — note Exec Summary says $3,259,866, use the table figure, flag discrepancy in a footnote), $0 spent
- Cumulative trust balance end-2024: $3,826,162
- **Zero fire halls built/funded by the levy through end-2024** — one fire hall (Windermere) was built pre-bylaw and excluded

Task: display cumulative levy $ vs. ~$26M single-facility cost as a simple bar/ratio per catchment — makes the funding gap visually immediate.

### IIMP growth-area overlay (Decoteau / Horse Hill / Riverview)

Primary source now located in full: Report CR_2705 (2016) + Attachment 1, archived at:
- https://doniveson.ca/wp-content/uploads/2018/09/IIMP.pdf (4-page council report)
- https://doniveson.ca/wp-content/uploads/2018/09/IIMP2.pdf (20-page Attachment 1, full tables)

Per-area figures (50-year horizon, dated 2016 — label as projection, not actual):
- Developer-funded infrastructure: **$3.806B** total (Drainage $2.351B, Transportation $1.455B)
- City/Province-funded infrastructure: **$1.362B** total (rec centres $347M, libraries $36M, police $47M, fire $65M, parks $95M, transit $148M, roads/interchanges $519M, waste collection $105M)
- Net projected 50-year shortfall: **~$1.4B** across all three areas
- Area boundaries/stats for joining: Decoteau 1,960 ha / pop 74,565 / 39-yr build-out; Horse Hill 2,793 ha / pop 70,038 / 36-yr; Riverview 1,435 ha / pop 50,422 / 30-yr

Task: overlay these 3 growth-area boundaries (already used for the existing IIMP sidebar annotation on Decoteau/Horse Hill/Riverview) with the new developer-vs-City split numbers. This slots into the existing IIMP click-through sidebar — extend it, don't build a new UI pattern.

### Sanitary trunk financing note (text annotation, not mapped)

SSTC/Expansion Assessment charges paused May 13, 2024 (SSSF Oversight Committee). 2024 residential SSTC rate: $1,764/dwelling. As of end-2024: ~$361M spent cumulative on trunk construction; only $4.9M spent and $17.3M collected in 2024; SSSF fund balance $115.8M. Net: trunk sanitary for new growth is currently funded from the accumulated ratepayer reserve, not from active growth charges.

Task: one-line callout in the sidebar, no separate spatial layer needed (no clean geographic basin boundaries confirmed yet — treat as citywide-program text, not mapped).

### Blatchford contrast case study

Use as a parallel infill example alongside the 3 greenfield IIMP areas — same sidebar UI pattern, 4th entry.
- Self-liquidating "debt for land redevelopment / debt recoverable" financing structure
- District Energy Sharing System (DESS): 570 boreholes, Energy Centre One 4.25MW heating/4MW cooling, financed via self-supporting tax-guaranteed debt under Policy C597A
- $23.7M federal SREPs grant (July 2024) toward $79.2M DESS expansion
- Has its own fire-hall off-site levy catchment: $32,813/ha (already in Component 1 table above)

---

## Component 2: Citywide debt context annotation (non-spatial)

Purpose: background trend + peer comparison, NOT a map layer. Present as a separate panel/chart, clearly labelled "citywide, not neighbourhood-specific."

### Data source: Alberta Municipal Financial and Statistical Data (FIR/SIR)

- URL: https://open.alberta.ca/opendata/municipal-financial-and-statistical-data
- Format: **structured XLSX**, one file per financial year, back to 2003 (plus a 2003–2008 ZIP)
- Fields include: assets, liabilities, long-term debt, revenue, expenses, property taxes — for every Alberta municipality
- Task: pull Edmonton's long-term debt time series 2003–2024, plus **St. Albert and Strathcona County** (already-tracked peers) for benchmarking

### Headline citywide figures (2025 year-end, reported to Council Mar 17 2026)
- Total outstanding debt: **$4.6 billion**
- Using **69%** of the tax-supported debt-servicing limit
- DMFP limits: tax-supported debt servicing ≤18.0% of tax-supported net expenditures; total debt servicing ≤21.0% of City revenue (26% emergency ceiling)

### Peer datapoint
Strathcona County (2022 audited): $133.07M total debt against $589.9M limit (22.56% used) — useful comparator once FIR series is pulled for multiple years.

---

## Explicitly out of scope for this phase

- Any spatial allocation of the $4.6B citywide debt total to neighbourhoods/parcels — not defensible, don't build it.
- S&P credit rating detail, CCBF/MSI/LGFF allocations — citywide context only if used at all, not spatial, low priority.
- Local Improvement levies — genuinely parcel-level and debt-financed, but not published as consolidated open data (would need FOIP or per-bylaw scraping). Flag as a possible future phase, not this one.

---

## Open data-acquisition risks to flag before building

1. Fire-hall catchment boundary polygons — existence/format unconfirmed, may require manual digitization from a PDF map exhibit.
2. Updated "Fiscal Impacts of Growth" IIMP refresh — not yet publicly located; current numbers are 2016 projections. Check periodically for a refreshed dataset and swap in when available.
3. 2024 Off-Site Levy Annual Report has an internal inconsistency ($3,033,592 table vs. $3,259,866 exec summary, and "three catchments" text vs. seven in the table) — use the itemized table figure, footnote the discrepancy.
