# Cross-read — the three pro-50 sections, by a different model

Executed **2026-09-18 (S172)** on **Fable 5.1**, at Peter's request, against the
three sections S171 flagged as wanting a reader that had not written them:
`docs/FINDINGS_road_class_inventory.md` **§4a** and **§4b**, and
`docs/FINDINGS_roadway_implied_life.md` **§5a**. S170 (Opus 5) produced three
findings cutting *against* the shipped 50-year road life; S171 (Opus 5, next day)
produced three cutting *for* it, every falsification self-administered. This is
the read that was asked for.

**Method:** the three primary sources were re-fetched from this box and the
relevant pages read directly (2020 *Infrastructure State and Condition* p5, p18,
p19, p31, p35; 2025 edition p2, p5, p20, p21, p37; the ConstructConnect article),
not taken from the transcriptions. Both documents' offline reproduction blocks
were run first (all asserts pass). What follows is what a second reader finds
that the first did not — and, where the first was right, that too.

## 0. Verdict in one paragraph

**Every transcription checks. Two of the three arguments are weaker than
written, and one of them — §4b, the one labelled "the strongest single piece of
evidence" — does not survive decomposition of the row it stands on.** §4a's
condition reading survives in a narrower form: the charged classes are *not
failing the way alleys are*, but "70% good" is a whole-class figure and says
nothing about the cohort that is actually past its expected life; its "second
route" (mean age → life ≈ 76) is not directional, it is invalid. §5a's 60-year
quote is verbatim and its structural reading (two events, not two estimates) is
sound — but it is a forward claim about a freshly reconstructed road, and the
same paragraph that files Winnipeg's "extended to 60" as support files Calgary's
"a fully reconstructed road can last up to 20 years" as mere verification.
⚠️ **The strongest argument for 50 was already in the repo before any of these
three sections were written, and none of them depends on the ISC tables:** the
Development Impact page's own $1.9M "renew and replace" exceeds its $1.5M initial
build, which fits a lifecycle containing a replacement-scale event, i.e. the
maintained 50, and annualizing that bundle over 25 charges the extension while
refusing to count it (`TODO.md`, "A NEW argument for 50 … not circular"). **The
three S171 sections add less to that than they claim; they do not subtract from
it. 50 still looks right, on the page's own arithmetic, not on the trend.**

## 1. Transcriptions — all verified against the PDFs

| claim | source page | verified |
|---|---|---|
| Local 4,830.30 lane-km / age 38 / life 28 / **70 / 17 / 13** / $3,461M | 2020 App. A p31 | ✅ |
| Collector 1,763.10 / 35 / 20 / **62 / 34 / 5** / $1,888M | p31 | ✅ (sums to 101 as printed) |
| Alleys 1,192.7 / 30 / 28 / **20 / 16 / 64** / $501M | p31 | ✅ |
| Roads 39 / 24 / 61 / 28 / 11 / $9,614M | p31 | ✅ |
| Goods & People Movement 37 / 33 | p31 + p19 | ✅ — the 33 is the portfolio, not Roads |
| Roads 2025: $10,484,313,206 / 70.8 / 16.2 / **11.2** / 1.7 not rated | 2025 App. B p37 | ✅ |
| Roads 2023: $9,747,485,291 / 72.9 / 15.2 / **11.4** | p37 | ✅ |
| *"expected to endure for 60 years … microsurfacing at 10 years and again at 40 years … overlay completed after 30 years"* | ConstructConnect 2016 | ✅ verbatim |

The reproduction blocks in both documents are honest about what they assert:
the arithmetic on the transcribed cells. They cannot check a reading, and the
three readings are where the problems are.

## 2. §4b — the "flat D+F" series is three differently-composed aggregates

§4b's claim: Roads D+F **11.0 → 11.4 → 11.2** across 2020/2023/2025 is flat, a
backlog would be rising, therefore no backlog; *"the strongest single piece of
evidence in the 25-vs-50 file."* Asserted in §6 as `max − min < 0.5`.

**The "Roads" row is not the same population in the three editions**, and
Appendix B prints the decomposition that shows it:

| edition | what "Roads" contains | sub-rows (value, D+F) |
|---|---|---|
| 2020 p31 | Major/Minor Arterial, Local, Collector, **Alleys**, Service Roads | Alleys **$501M @ 64%** |
| 2023 (via 2025 p37) | Paved Roads, Unpaved Roads | Paved $9,704.5M @ **11.5%**; Unpaved $43M unrated |
| 2025 p37 | Paved Roads, Unpaved Roads, **Curbs** | Paved $8,204.2M @ **12.5%**; **Curbs $2,097.3M @ 7.0%**; Unpaved $182.8M 100% unrated |

Three consequences, each checkable from p37 alone:

1. **The 2025 figure is a curbs-diluted paved figure.** Value-weighting the
   sub-rows reproduces the printed 11.2 exactly: (8,204.2 × 12.5 + 2,097.3 ×
   7.0) ÷ 10,484.3 = **11.18**. A **$2.1B curbs line at 7% D+F appears in 2025
   and has no value in 2023**. The paved-surface row, which is the nearest thing
   to the population the metric charges, reads **11.5 → 12.5** across the two
   editions that print it — a **1.0-point rise in two years** — and §6's own
   `< 0.5` assert **fails** on that sub-row.
2. **But that rise is itself confounded**, because 2023 Paved Roads at $9.7B is
   $1.5B *larger* than 2025 Paved Roads at $8.2B while the Roads total grew 7.6%
   — i.e. curbs were almost certainly *inside* 2023's paved line and split out in
   2025. If they were, and were at ~7% then too, 2023 paved-excluding-curbs was
   ~12.5–12.7 and the paved series is flat after all. **The source does not say
   which.** So the honest statement is not "flat" and not "rising": **the
   composition changed by more than the trend being claimed**, and a 0.4-point
   range across three re-scoped aggregates is inside the re-scoping noise.
3. **2020's 11 carries ~3.3 points of alleys** ($501M × 64% ÷ $9,614M). Roads
   excluding alleys would read ~**8.1%** in 2020 (7.6–8.6 given the integer
   rounding). Whether alleys sit inside 2023/2025's "Paved Roads" is not stated.
   If they do, the like-for-like series *starts* at ~8 and *ends* at ~11–12,
   which is the opposite of flat; if they do not, 2020's 11 is not comparable
   with the later rows for the other reason. Either way the three-point series
   does not carry.

⚠️ **The assert is a band fitted around the observation.** `< 0.5` was chosen
after seeing a 0.4 range; 2020's "11" is an integer that could be 10.5–11.49, so
the true range on the printed rows alone is up to 0.9. `DECISIONS.md` already
names this failure mode (*"a band fitted around a defect"*, 2026-09-03), and it
is one of the ten instances in `check-where-the-value-can-be-wrong`.

**And even a genuinely flat D+F would not discriminate 25 from 50.** A flat poor
share says renewal spending is keeping pace with deterioration — which, with the
Neighbourhood Renewal levy at **$174.4M/yr** (`city_unit_costs.json` →
`roadway_renewal.funded_side_2026_09_08`), is what one would expect under
*either* life. What it measures is spend adequacy, not interval. The quantity
that *would* discriminate is the spend needed to hold it flat per metre — and
that comparison already exists in the repo (`roadway_renewal.citywide_scale`:
the $38/m/yr requirement, $139M/yr, sits inside the $82–174M/yr funded bracket)
and is recorded there as "order-of-magnitude plausible; nothing more". §4b
should be demoted to the same rank, and its "strongest single piece of evidence"
label removed.

## 3. §4a — the condition reading survives narrowed; the mean-age route does not

§4a's claim: local roads are 10 years past a 28-year expected life at 70/17/13,
collectors 75% past a 20-year life at 62/34/5, alleys (excluded from the metric)
are the backlog control at 64% D+F; therefore the expected life is a design life
the City is not replacing on, and the observed interval is longer.

**What holds.** The alley contrast is real and legible, and the rubric backs the
reading in a way §4a did not cite: the City's own grade definitions (2020 p35,
2025 p5) tie condition to *expected* life — **B** = *"within mid-stage of its
expected life"*, **C** = *"later stage"*, **D** = *"approaching the end"*. A
38-year-old class rated 70% A/B against a 28-year expected life is, by the
rater's own scale, mostly "mid-life". The condition column and the expected-life
column disagree about the same asset, and only one of them is a measurement.
That is §4a's point and it is right.

**What does not hold as written.**

1. **"70% good" is the whole class, not the past-life cohort.** Local Roads
   includes every post-1990 suburb, all of it under 28 and nearly all of it A/B.
   The condition of the roads that *are* past their expected life is not
   printed, only bounded: if ~45% of local lane-km are younger than 28 and all
   A/B (a mean age of 38 does not permit much more), the ≥28 cohort is roughly
   **45% good / 31% fair / 24% poor**. That is still nothing like the alley row —
   the backlog reading is excluded — but it is not "ten years past life and
   still 70% good", which is the sentence the TODO item now carries. **The claim
   should be "the past-life cohort is not failing", not "the past-life cohort
   is in good condition."**
2. **The "second route" (mean age 38 → L ≈ 76, "a floor") is invalid, not
   directional.** It assumes a replacement-driven steady state. Edmonton's
   mature-neighbourhood stock was built 1950–1980 and was substantially *not
   replaced* until the Neighbourhood Renewal levy began in 2009 (the
   ConstructConnect piece says so: *"A municipal levy was introduced in 2009 to
   launch the program"*). A mean age of 38 in 2020 reflects a **historical
   replacement rate near zero**, not a chosen interval; the City reads its own
   table the same way (*"Roads' assets are at or over their expected asset
   life"*, p19). Whether reconstruction resets an asset's age in the inventory
   is not defined anywhere in either edition (p5 says only why age is
   collected). **`TODO.md`'s "the mean-age arithmetic puts it above 50" should
   be withdrawn.** The first route is the only one.
3. **The contrast with alleys is a contrast between funded and unfunded
   renewal, not between two lives.** Local and collector roads had eleven years
   of NRP spending behind them by 2020; alleys had none (the alley renewal
   levy is a 2019–20 addition). So the table shows *renewal spending works* —
   which is the Development Impact page's "extended to 50 with proper
   maintenance" clause, and is consistent with 50. It is not independent of it.

## 4. §5a — verbatim, structurally sound, and selectively weighed

§5a's claim: a City staffer's *"complete reconstruction … expected to endure for
60 years"* with microsurfacing at 10/40 and an overlay at 30 explains the
Development Impact sentence — 25 is when the structure is due, 50–60 is the
reconstruction interval — so the shipped 50 is the conservative end.

**What holds.** The quote is verbatim (re-fetched). The two-events reading is
the right one, and it is the only reading under which the Development Impact
page's own numbers are internally consistent (§0 above; `TODO.md`'s non-circular
argument). Winnipeg printing *"designed for 25 … extended to 60"* is a real
second instance of the same structure.

**What does not hold as written.**

1. **It is a forward claim about a road reconstructed to 2016 standards with a
   full treatment schedule, not an observed interval.** Neighbourhood Renewal
   exists *because* the 1950–1980 stock did not last 60. For a lens that
   levelizes the cost of the *existing* network (mean age 38), the relevant
   interval is the one that stock achieves, which nobody has measured; for a
   lens about the marginal cost of a *new* street — which is how the
   Development Impact page frames its $1.5M/km — 60 is the right kind of
   number. The site's metric is the former framing with the latter's unit
   costs, and §5a does not say so.
2. **Calgary is filed, not weighed.** The same paragraph that counts Winnipeg's
   "to 60" as support records Calgary's primary *"a fully reconstructed road can
   last up to 20 years"* as a verification of the research reply and moves on.
   Read in context it is almost certainly a base life (the interval to the
   next treatment, comparable to Edmonton's "usually 25"), not a
   reconstruction interval — but that reading has to be stated, because as
   written §5a treats the datum that agrees as evidence and the one that
   disagrees as bookkeeping.
3. **The 60 requires a treatment schedule the page's $1.9M may not fund.**
   Observed NRP reconstruction runs **1.66× the published $1,900/m**
   (`docs/FINDINGS_nrp_reconstruction_cross_check.md` §3, a floor). If the
   maintenance that buys the extension costs more than the bundle assumes, the
   50-year *rate* is a floor even where the 50-year *life* is right — which the
   repo already records, and which §5a's "50 is the conservative end" elides.

## 5. What this leaves for Peter's call

- **50 is still the better-supported choice**, and the reason is the one that
  predates S171: the page's $1.9M renew-and-replace only fits the maintained
  lifecycle, and charging it over 25 double-charges the extension.
- **The 25.9 expected asset life is not refuted; it is a different quantity**
  (the interval to structural intervention, the "usually 25"). S170's reading of
  it as a competing life was wrong; S171's was right.
- **§4b should stop being called the strongest evidence.** It is an aggregate
  whose composition changed in every edition, and the property it measures
  (spend keeping pace) is life-agnostic.
- **§4a's narrowed form stands; its mean-age route should be struck.**
- **The methodology-note question in the TODO is unchanged**: the decision was
  never whether 50 is defensible — it is — but whether the site says why a
  reader who has met "25 years" elsewhere sees half the annual figure here.

## 6. Reproduction

The decomposition in §2, from 2025 Appendix B p37 alone.

```python
# 2025 Infrastructure State and Condition, Appendix B p37 — the Roads row and its
# three sub-rows (replacement value $M, D+F %, not-rated %).
paved, unpaved, curbs = 8204.164788, 182.805696, 2097.342722
roads_total = 10484.313206
assert abs(paved + unpaved + curbs - roads_total) < 0.001

# the printed 11.2 is the value-weighted blend of paved 12.5 and curbs 7.0
blend = (paved * 12.5 + curbs * 7.0) / roads_total
assert 11.1 <= blend <= 11.25, blend                    # prints 11.2
assert abs(unpaved / roads_total * 100 - 1.7) < 0.1     # the 1.7% not-rated IS unpaved

# the nearest sub-row to the charged population is Paved Roads, and across the
# two editions that print it, it RISES 11.5 -> 12.5 -- S4b's own <0.5 assert fails
paved_series = [11.5, 12.5]                              # 2023, 2025
assert max(paved_series) - min(paved_series) >= 0.5, "S4b's flat assert would pass here"

# ...but curbs were almost certainly inside 2023's paved line ($9,704.5M paved
# in 2023 vs $8,204.2M in 2025 while the Roads total grew), and if they were at
# ~7% then too, the 2023 paved-ex-curbs figure was ~12.5-12.7: flat after all.
# The source cannot decide it, which is the finding: composition noise > trend.
for c in (1800, 2000, 2097):
    ex = (9704.5 * 11.5 - c * 7.0) / (9704.5 - c)
    assert 12.4 <= ex <= 12.8, ex

# 2020's 11 carries ~3.3 points of alleys (App. A p31: $501M at 64% D+F)
r20, alleys_v, alleys_df = 9614, 501, 64
assert 3.2 <= alleys_v * alleys_df / r20 <= 3.4
ex_alleys = (r20 * 11 - alleys_v * alleys_df) / (r20 - alleys_v)
assert 7.5 <= ex_alleys <= 8.7, ex_alleys                # ~8.1, given "11" is an integer
print(f'2025 blend {blend:.2f}; paved {paved_series}; 2020 ex-alleys {ex_alleys:.1f}')
```
