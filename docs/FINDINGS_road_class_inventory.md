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
3. ⚠️ **A per-class expected *asset* life on exactly the population the site
   charges — ~26 years — alongside a per-class *condition* that says the network
   is being kept well past it in good shape.** See §4 and **§4a**. This is the
   most consequential thing in the document, and ⚠️ **the two halves of it point
   opposite ways**: §4 was first written from the life column alone, with the
   condition column not yet transcribed, and read as evidence against the
   50-year life the site ships. **§4a corrects that.**

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

Replacement value in millions. **Physical condition transcribed 2026-09-17
(S171)** as the table's own `A+B / C / D+F` percentage split — A+B good, C fair,
D+F poor. ⚠️ **That column was omitted from this transcription until 2026-09-17,
and §4's first reading of the table was wrong because of it.** Demand/Capacity
and Functionality (two further `A+B / C / D+F` triples) are still omitted —
neither bears on service life.

| infrastructure | quantity | unit | avg age | **expected asset life** | **physical condition A+B / C / D+F** | replacement value |
|---|---:|---|---:|---:|---|---:|
| Major Arterial | 596.2 | lane km | 30 | 22 | 78 / 20 / 2 | $711 |
| Minor Arterial | 2,927.2 | lane km | 48 | 22 | 53 / 40 / 7 | $2,914 |
| **Local Roads** | **4,830.30** | lane km | **38** | **28** | **70 / 17 / 13** | $3,461 |
| **Collector Roads** | **1,763.10** | lane km | **35** | **20** | **62 / 34 / 5** | $1,888 |
| Alleys | 1,192.7 | lane km | 30 | 28 | 20 / 16 / **64** | $501 |
| Service Roads | 56,690 | metres | 10 | 30 | 46 / 37 / 17 | $139 |
| **Roads (total)** | 61,977 | varies | **39** | **24** | 61 / 28 / 11 | **$9,614** |

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

⚠️ **"We only charge local roads, so use 28" does not hold, and the blend is not
hiding a higher number — every reweighting lands in the same 24–28 band.**
Measured from `data/raw/roads.geojson` on 2026-09-17 under `load_roads`' own
filters and `CLASS_GROUP`, the charged network is **local 2,739.6 km + collector
926.2 km** centreline, so collector is **25% of the charged length** and — at
**1.49× the replacement cost per lane-km** ($1.071M vs $0.717M) — **35% of the
replacement value**. Four weightings:

| weighting | life |
|---|---:|
| local only | 28.0 |
| City lane-km, collector+local | 25.9 |
| our own centreline-km, collector+local | 26.0 |
| **replacement-cost weighted**, Σvalue ÷ Σ(value/life) | **24.5** |

⚠️ **The cost weighting is the correct one for a $/m/yr charge** — the charge is
an annualized replacement cost, so each class must enter in proportion to the
dollars it consumes, not the metres it occupies. It is the **lowest** of the
four. Dropping to local-only raises the figure; it does not lower it.

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

## 4a. ⚠️ CORRECTED 2026-09-17 (S171) — the condition column says the opposite

**This section used to read:** *"the same table also says the maintenance is not
in fact keeping pace — local roads average 38 years old against a 28-year life,
collectors 35 against 20."* The ages are right. **The inference was wrong, and it
was wrong because §1 had dropped the column that answers it.** Age past expected
life is compatible with a renewal backlog *and* with a successfully extended
life; only condition discriminates them. Appendix A publishes condition, it was
not transcribed, and the reading went the way that happened to fit the rest of
the section.

| class | avg age | expected life | **physical condition A+B / C / D+F** |
|---|---:|---:|---|
| Local Roads | 38 | 28 | **70 / 17 / 13** |
| Collector Roads | 35 | 20 | **62 / 34 / 5** |
| *Alleys (excluded from the metric)* | 30 | 28 | 20 / 16 / **64** |

⚠️ **The collector row sums to 101%, not 100** — transcribed as printed, and the
only road row in Appendix A that does. Rounding in the source, and small enough
not to touch the reading (its D+F is 5% either way), but it is a reminder that
these are rounded published percentages, not a reconciled split. The §6
reproduction asserts 99–101 rather than 100 **because the exact-100 version of
that assert failed on this row** on first run.

**Local roads are ten years past their expected asset life and still 70% good,
13% poor. Collectors are 75% past theirs and only 5% poor.** That is not a
backlog. **The alley row is what a backlog looks like in this very table** — 64%
D+F at only 30 years against a 28-year life — and it is the control that makes
the roads rows legible. Alleys are already out of `road_m_per_acre` by the
alleys-out decision, so the one asset class here that *is* failing is one the
metric does not charge.

⚠️ **So the table supports the 50-year reading, not the 25-year one.** The
expected asset life is a design life the City is demonstrably not replacing on;
the observed life, in acceptable condition, is longer.

**A second route from the same two numbers.** A stock replaced at age *L* has a
mean age of about *L*/2, so a mean age of 38 implies *L* ≈ 76. Edmonton's road
network grew over the period, which skews the age distribution **young** and
therefore makes 76 a floor rather than an estimate. ⚠️ **Treat this as
directional only** — it assumes a replacement-driven steady state, and "average
age" here is age since original construction, not since the last overlay. Both
caveats push the same way: the interval actually being achieved is well above
28, and above 50.

⚠️ **This is also the mechanism behind the page's wording.** *"Usually 25,
extended to 50 with proper maintenance"* is not two estimates of one event; it is
two different events. ~25 is when the pavement structure is due for intervention;
50 is the interval to full reconstruction, bought with the resurfacing and
renewal spending in between, while the base persists. **`road_m_per_acre` charges
the whole bundle — capital + O&M + renewal — so its denominator is the interval
over which that bundle recurs, which is the reconstruction interval, not the
resurfacing interval.**

⚠️ **RECORDED AGAINST INTEREST, IN BOTH DIRECTIONS** (`measurements-that-favour-me`,
`check-where-the-value-can-be-wrong`). The original §4 was written by a model that
had just produced three figures cutting against the shipped number, and it read an
ambiguous signal as a fourth. The correction was written by a model answering
"shouldn't that even out to 25" and it lands on the shipped number being right.
**Both readings rest on the same four cells of one table.** The transcription in
§1 is verbatim from p31 and the arithmetic is asserted in §6 — check those, not
the prose. **A different model should read this section.**

**The 25-vs-50 remains Peter's call and is NOT closed here.** What changed: the
per-class figure no longer points one way. `TODO.md`'s item is updated.

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

# --- §4a: every reweighting lands in 24-28, and the cost one is the LOWEST -----
# our own charged centreline km, measured from data/raw/roads.geojson 2026-09-17
our_local, our_collector = 2739.65, 926.20
val_local, val_collector = 3461, 1888               # $M replacement value, p31

by_our_len  = (our_local * 28 + our_collector * 20) / (our_local + our_collector)
by_cost     = ((val_local + val_collector)
               / (val_local / 28 + val_collector / 20))

assert 25.5 <= by_our_len <= 26.5, by_our_len       # ~26.0, matches the City weighting
# band deliberately tight: 24.0-25.0 still passed a mutation that replaced both
# class lives with the all-roads 24, i.e. that did no per-class weighting at all
assert 24.4 <= by_cost   <= 24.7, by_cost           # 24.5, the right one for $/m/yr
# local-only RAISES the figure -- the blend is not concealing a longer life
assert by_cost < by_our_len < 28, (by_cost, by_our_len)
# collectors are a minority of length but cost ~1.5x per lane-km, so they are a
# LARGER share of value than of metres -- which is why the cost weighting is lower
assert (our_collector / (our_local + our_collector)
        < val_collector / (val_local + val_collector))
assert 1.45 <= (val_collector / collector) / (val_local / local) <= 1.55

# --- §4a: condition discriminates "extended life" from "backlog" ---------------
# physical condition A+B / C / D+F, p31, verbatim
cond = {"local": (70, 17, 13), "collector": (62, 34, 5), "alley": (20, 16, 64)}
# NB the collector row sums to 101, not 100 -- rounding in the source, see S4a note
for k, v in cond.items():
    assert 99 <= sum(v) <= 101, (k, v)
# both charged classes are past their expected life (38>28, 35>20) yet majority
# good; the EXCLUDED alley class is the backlog control that makes that legible
assert cond["local"][0] >= 70 and cond["local"][2] <= 13
assert cond["collector"][0] >= 60 and cond["collector"][2] <= 5
assert cond["alley"][2] > cond["alley"][0], "alleys are the failing class, not roads"
print(f'reweightings: cost {by_cost:.1f} < our length {by_our_len:.1f} < local-only 28')
```
