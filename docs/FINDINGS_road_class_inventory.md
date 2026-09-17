# Findings — Edmonton's Road Inventory by Class, from the Primary Table

Captured 2026-09-17 (S170). **The 2020 *Infrastructure State and Condition*
Appendix A table was obtained and read.** Until today its figures reached this
project only through a blog that is now **404**, and the send-back brief's Q1(b)
declared that provenance openly: *"BOTH constants in that formula … come from ONE
secondary relay … and the blog carrying it is now 404."*

**That relay is retired. Everything below is transcribed from the City document
itself**, and three separate things that were resting on it are now primary:

1. The **lane-km-by-class split** — and the brief's two weak constants, **34.8%**
   and **1.804**, reproduce almost exactly from it.
2. The **lane-km reading of the "~11,000 km" snow inventory**, which until now
   was inferred from two City statements rather than read off a table.
3. ⚠️ **A per-class expected asset life on exactly the population the site
   charges — and it is ~26 years, not 50.** See §4. This is the most consequential
   thing in the document and it does not favour what the site ships.

## 0. Provenance, and why it is still not perfect

- **City of Edmonton, Integrated Infrastructure Services, *2020 Infrastructure
  State and Condition*** — 36 pages, 2,646,355 bytes, Appendix A on **p31**,
  portfolio narrative on **p19**.
- ⚠️ **Obtained from the Internet Archive, via a copy the blog hosted**:
  `https://web.archive.org/web/20240112150443/http://www.matthewdance.ca/s/2020-Infrastructure-Inventory-State-and-Condition.pdf`
  (snapshot **2024-01-12**). The blog post itself (`/blog/cost-of-roads`) is
  **404 live** — confirmed from this box on 2026-09-17 over both http and https,
  while the site root returns 200, so the post was removed rather than the site
  going down.
- ⚠️ **This is the City's own PDF, but it is NOT served from a City URL any
  more.** The live `edmonton.ca` Infrastructure State and Condition page does not
  carry it. **So the document is primary; the retrieval path is not.** If this
  ever has to be cited publicly, the right move is to ask the City for the 2020
  report directly — that ask already exists as the third retrieval in the
  brief's Q1(b), and it is now a *confirmation* request rather than a hunt.
- ⚠️ **`www.edmonton.ca` soft-404s with HTTP 200** — a missing page returns 200
  and a body titled *"Page Not Found"*. A status-code check alone will report a
  dead City URL as live. Check the title or body.

## 1. Appendix A, p31 — transcribed in full for the road rows

Replacement value in millions. `A+B / C / D+F` condition splits omitted.

| infrastructure | quantity | unit | avg age | **expected asset life** | replacement value |
|---|---:|---|---:|---:|---:|
| Major Arterial | 596.2 | lane km | 30 | 22 | $711 |
| Minor Arterial | 2,927.2 | lane km | 48 | 22 | $2,914 |
| **Local Roads** | **4,830.30** | lane km | **38** | **28** | $3,461 |
| **Collector Roads** | **1,763.10** | lane km | **35** | **20** | $1,888 |
| Alleys | 1,192.7 | lane km | 30 | 28 | $501 |
| Service Roads | 56,690 | metres | 10 | 30 | $139 |
| **Roads (total)** | 61,977 | varies | **39** | **24** | **$9,614** |

⚠️ **Two relay errors are now visible, and both were in the blog, not in us.**
The blog printed the local-roads replacement value as *"$3.46 million"* and the
collector value as *"$1.9 million"* — the table says **$3,461M** and **$1,888M**,
i.e. the blog was low by a factor of 1,000 on both. The lane-km counts and the
asset lives it relayed were correct. **The brief carried only the lane-km, so
nothing downstream inherited the error** — but it is the reason a single relay
was the right thing to flag.

## 2. The brief's two weak constants, recomputed from the table

Both reproduce. **The formula was right; only its footing was bad.**

| constant | brief's value | from Appendix A | agrees |
|---|---|---|---|
| arterial share of road lane-km | 35% | (596.2+2,927.2) / 10,116.8 = **34.8%** | ✅ |
| lane-km per centreline km, collector+local | 1.80 | 6,593.4 / 3,654 = **1.804** | ✅ |

- arterial (major + minor) = **3,523.4** lane-km (blog said 3,500)
- collector + local = **6,593.4** lane-km — the population `road_m_per_acre` charges
- roads excluding alleys and service roads = **10,116.8** lane-km (blog said 10,093)

⚠️ **The k-ratio caveat is unchanged.** Appendix A gives quantities, ages, lives
and replacement values — **not operating or snow cost by class**. No value of `k`
appears here, so the published caveat (*"a floor unless arterials cost more than
~3.3× a collector or local lane-km"*) stands exactly as written. What changes is
that its two constants are no longer single-relay.

## 3. The "~11,000 km" snow inventory is lane-km, now from a table

roads excl. alleys **10,116.8** + alleys **1,192.7** = **11,309.5 lane-km**.

⚠️ **This is a stronger confirmation of the S149 finding than the argument it
replaces.** The lane-km reading was established by combining two City statements
(the Winter Roads FAQ's *"over 4,000 lane kms of residential roads"* and a 2022
official's *"1,250 to 1,300 kilometres"* of alleys). Appendix A supplies the
whole inventory in one table, in one stated unit, with the alley line itemised at
**1,192.7** — close to, and slightly below, the relayed 1,250–1,300 estimate.
**`roadway_ops`' lane-km denominator is not in question.**

## 4. ⚠️ The expected asset lives, and what they do to the 25-vs-50 call

The table publishes an **expected asset life per road class**, which is the thing
this project has been looking for since 2026-07-15 — *on the right asset class*,
unlike every other figure available:

- **Local Roads: 28 years.** Collector Roads: **20 years.**
- Lane-km weighted across the exact collector+local population the site charges:
  **25.9 years.**
- All Roads: **24 years**. Both arterial classes: 22.

⚠️ **The site ships a 50-year life. The City's own expected asset life for the
network the metric charges is ~26.** That is the 25 reading, not the 50 one,
and it is the first time the question has been answered on the right population
rather than on a citywide aggregate.

⚠️ **Read against it, honestly, because the page's other sentence still stands.**
The 2020 report's p19 narrative says roads *"can be maintained past their expected
asset life"* **with appropriate maintenance and renewal** — which is the same
structure as the Development Impact page's *"usually 25, extended to 50 with
proper maintenance"*. So the two City sources are **consistent**: ~25 is the base
life, and 50 is what maintenance buys. The choice was always which of those the
site should publish, and this does not collapse it.

⚠️ **But the same table also says the maintenance is not in fact keeping pace**:
local roads average **38 years old against a 28-year life**, collectors **35
against 20**. Both classes are already well past the base life, which is evidence
about the *condition* attached to the 50-year reading.

**Recorded against interest** (`measurements-that-favour-me`): this is the third
independent City figure this session to land below 50, and the session's only
finding that flattered the shipped number was the centreline unit. **The
25-vs-50 remains Peter's call and is NOT reopened here** — but the "why 50 still
looks right" case in `TODO.md` now has to be made against a per-class figure,
not only against citywide aggregates.

## 5. ⚠️ A claim in our own files that this puts in doubt

`TODO.md` and `docs/AUDIT_LEDGER.md` record, from S154:

> the City's *2023 Infrastructure State and Condition Report* p27 gives Roads
> **average age 43 yrs vs expected life 33 yrs**

**The 2020 report's `Roads` row is average age 39, expected life 24 — not 33.**
Its **33** appears on **p19**, attached to something else entirely:

> *"the average age of the Goods and People Movement Portfolio is 37 years with
> an expected life of 33 years"*

— and that portfolio *"consists of Roads ($9.6 Billion), Bridges ($1.8 billion),
Active mode ($2.0 billion), Light Rail Transit ($1.5 billion) and Transit Bus
System ($152 million)"*. Bridges alone carry a **57-year** life, which is what
pulls a portfolio average up to 33 from a roads figure of 24.

⚠️ **So "Roads expected life 33" has the exact shape of a portfolio number
mislabelled as a roads number** — and our note even cites a **p27**, which in the
2020 edition is the *Ancillary Infrastructure* page. **NOT ASSERTED AS WRONG:**
our figure is from the **2023** edition, which was not obtained (the live City
page no longer serves it, and this box could not locate it). The 2023 report may
genuinely say 43/33 for Roads. **This is a flag to check, not a correction** —
but the 33 should not be quoted as a roads service life until someone opens p27
of the 2023 edition and reads the row label.

## 6. Reproduction

```python
# City of Edmonton, 2020 Infrastructure State and Condition, Appendix A p31.
maj_art, min_art, local, collector, alleys = 596.2, 2927.2, 4830.30, 1763.10, 1192.7
art   = maj_art + min_art
roads = art + local + collector          # excludes alleys and service roads
cl    = local + collector                # the population road_m_per_acre charges

assert round(art, 1) == 3523.4
assert round(roads + alleys, 1) == 11309.5          # the "~11,000 km" inventory
assert 0.345 <= art / roads <= 0.350                # brief's 35% arterial share
assert 1.80 <= cl / 3654 <= 1.81                    # brief's 1.80 lane/centreline

life = (local * 28 + collector * 20) / cl           # expected asset life, lane-km weighted
assert 25.5 <= life <= 26.5, life
print(f'collector+local expected asset life: {life:.1f} years')
```
