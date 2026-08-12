# DRAFT — Open Data request: publish taxable/exempt liability status on `q7d6-ambg`

**Status: DRAFT, NOT SENT.** Written 2026-08-08. Peter's to send, edit or discard.

⚠️ **Read the "Claims and how far each is verified" section before sending.** One
claim in the brief this was written from was **wrong** and is corrected here; one
is verified only from search-result text, not from the primary document.

---

## Why this request exists

Our model applies published mill rates to every record on the current assessment
roll. That includes 2,254 parcels on institutional and public zoning
(`AJ`/`UF`/`UI`/`PU`) carrying **$5.62B of assessed value → ~$125.4M/yr of
modelled levy, 4.6% of the citywide total**. Whether the City actually levies
those parcels is not answerable from the published data, so the figure can only
be published as a **gross modelled** number. One field would resolve it.

---

## Claims and how far each is verified

| Claim | Status |
|---|---|
| Calgary's assessment **notices** display a taxable/exempt status | ✅ **VERIFIED.** calgary.ca states verbatim: *"Tax exemption status is noted on your assessment notice."* |
| Calgary **publishes** exemption status as open data | ❌ **FALSE — do not write this.** Checked the live schema of Calgary's `4bsw-nn7w` (Current Year Property Assessments): `roll_year, roll_number, address, assessed_value, assessment_class, assessment_class_description, re_assessed_value, nr_assessed_value, fl_assessed_value, comm_code, comm_name, year_of_construction, land_use_designation, property_type, land_size_sm, land_size_sf, land_size_ac, mod_date, sub_property_use, multipolygon, cpid, unique_key`. **There is no exempt/taxable field.** Asserting otherwise to Edmonton would be checkable and wrong. |
| Alberta requires a **liability code** internally | ✅ **VERIFIED 2026-08-12, IN THE PRIMARY SOURCE — and it is STRONGER than this draft originally claimed.** The 2026-08-08 HTTP 520 was transient. Manual downloaded and read: *2025 Recording and Reporting Information for Assessment Audit and Equalized Assessment Manual*, **Ministerial Order No. MAG:016/25**, 137 pp, open.alberta.ca dataset `1718-1771`. See "What the manual actually says" below. |
| GIPOT figure "$15.7M, 2021-22" | ❌ **NOT USED HERE, and should not be.** Unverified; see `data/DATA.md`. It is also not an argument for this request. |

---

## What the manual actually says (verified 2026-08-12, quoted from the source)

**Source:** *2025 Recording and Reporting Information for Assessment Audit and
Equalized Assessment Manual*, Ministerial Order **No. MAG:016/25**, Alberta
Municipal Affairs. open.alberta.ca dataset `1718-1771`
(`ma-recording-and-reporting-information-for-assessment-audit-and-equalized-assessment-2025.pdf`).
⚠️ **Quote it by Ministerial Order number, not by URL** — the resource UUID is a
CKAN artifact and the dataset carries every edition back to 2006.

- **ASSET, defined verbatim** (§2.1(f)): *"'ASSET' is an acronym for Assessment
  Shared Services Environment, an Internet-based application and database of
  liability codes, and assessment and sales information for use by municipalities
  and the Government of Alberta"*.
- **The liability code is seven components** (§3.6.11), two of which are exactly
  the field being requested: **Tax Code** and **Tax Exemption Code**.
- **It is mandatory and universal.** *"Every assessed property must be assigned a
  liability code"* (§3.6.11), and *"municipalities are required to record the
  liability codes assigned by the assessor and report the information to the
  department."*
- **Tax Code (Table 13) already encodes taxable vs exempt directly:**
  `T` subject to municipal tax and requisitions · `S` exempt from municipal tax
  but subject to school/other requisitions (council-bylaw exemptions under MGA
  364) · `G` eligible for PILT from the Crown in right of Canada · `E`
  *"assessable but is exempt from taxation"* · `EI` exempt incremental (CRL).
- ⚠️ **THE STRONGEST FACT, AND IT IS THE ONE TO LEAD WITH: there is no coverage
  gap.** *"Every assessed property, **including taxable property**, must be
  assigned a tax exemption code"*, and *"All taxable properties must be assigned
  the 'NAA' exemption code"* — the codes are *"mandatory in ASSET"*. So this is
  not a field that exists for some accounts and would be null for the rest. Every
  account on the roll already carries one.
- **Appendix G names our exact parcels**, citing the MGA section as the code
  itself: `MGA362(1)(d)` property used in connection with educational purposes
  held by the board of governors of a university (**the U of A**);
  `MGA362(1)(e)` property used in connection with hospital purposes held by a
  hospital board receiving Crown financial assistance (**Royal Alexandra,
  Misericordia, Grey Nuns, Cross Cancer**); `MGA362(1)(a)` Crown in right of
  Alberta or Canada; `MGA361(c)` reserves and undeveloped public-utility land.

⚠️ **This upgrades the request from "I believe this exists" to "this is recorded
per account under a Ministerial Order."** It also means the draft's *"full
statutory-basis detail would be valuable but is not necessary"* concession is
**too weak** — the statutory basis IS the code (`MGA362(1)(e)`), so asking for
the exemption reason code is not asking for more than asking for a boolean.

⚠️ **What this still does NOT tell us:** what Edmonton has actually coded for any
specific parcel. The manual establishes that the field exists, is mandatory and
is reported to the province — **not** what it says. Our $125.4M question stays
open, with **direction unknown**, until the City publishes or discloses it.

---

## Draft message

> **To:** City of Edmonton Open Data / Assessment & Taxation Branch
> **Subject:** Dataset request — taxable/exempt liability status on Property Assessment Data (`q7d6-ambg`)
>
> Hello,
>
> I am working with the City's open assessment data (Property Assessment Data
> (Current Calendar Year), resource `q7d6-ambg`) and would like to request an
> additional field.
>
> **The request:** publish the taxable/exempt liability status already held for
> each account — the internal liability code, or a simplified taxable/exempt
> indicator derived from it — as a column on `q7d6-ambg`.
>
> **Why it matters for users of the data.** The dataset publishes an assessed
> value and a `Tax Class` for every account, but nothing that distinguishes an
> assessed property that is levied from an assessed property that is exempt.
> Applying the published mill rates to the published roll is the natural way to
> use these two datasets together, and it silently treats exempt property as
> taxable. On institutional and public zoning alone this affects roughly 2,250
> parcels and several billion dollars of assessed value, which is large enough
> to change conclusions rather than merely blur them. Anyone doing this
> calculation gets a number that looks authoritative and may be materially
> wrong, with no signal in the data that anything is missing.
>
> **Why I believe the field already exists.** The *2025 Recording and Reporting
> Information for Assessment Audit and Equalized Assessment Manual* (Ministerial
> Order No. MAG:016/25) requires every assessed property to be assigned a
> liability code, two components of which are a **Tax Code** — `T` subject to
> municipal tax, `E` assessable but exempt from taxation, `S` exempt from
> municipal tax but subject to requisitions, `G` eligible for payment in lieu —
> and a **Tax Exemption Code** citing the MGA section that grounds the
> exemption. The manual is explicit that coverage is complete: every assessed
> property *including taxable property* must carry a tax exemption code, with
> taxable property assigned `NAA`. Municipalities are required to record these
> codes and report them to Municipal Affairs through ASSET. The distinction is
> therefore already held per account, for every account, as a matter of
> provincial reporting — this is a request to surface an existing field rather
> than to create one.
>
> The City of Calgary discloses this status to property owners directly: its
> assessment notices carry a tax exemption status field. I am not aware of any
> Alberta municipality publishing it as open data, which is precisely why I am
> asking Edmonton.
>
> **A minimal version would be sufficient.** A boolean taxable/exempt column, or
> the tax code as recorded, would resolve it. The exemption reason code
> (e.g. `MGA362(1)(e)` for hospital property) would be more useful still, and I
> understand it to be recorded in the same place.
>
> I appreciate that exemption status may raise questions I am not seeing from
> outside — if there is a reason this cannot be published, or a different
> existing source I have missed, I would be glad to hear it.
>
> Thank you for the work that goes into maintaining these datasets.
>
> [name / contact]

---

## Notes for whoever sends this

- **Keep it separate from the `qi6a-xuwt` bug report.** That one reports a
  defect (accounts missing from the historical roll). This one requests a new
  field and asserts no defect. Filing them together muddles both.
- **Do not include the $125.4M figure in the message.** It is a modelled number
  that depends on the very question being asked, and leading with it invites a
  correction rather than a field.
- **Cite resource IDs, not prose** — `q7d6-ambg` is named above for that reason.
- ~~If the ASSET/liability-code claim cannot be confirmed from the Municipal
  Affairs manual, cut the second half of that paragraph and ask the question
  plainly instead.~~ **No longer needed — confirmed in the source 2026-08-12**
  (see "What the manual actually says"). The fallback is retired; the paragraph
  now cites the Ministerial Order.
- ⚠️ **THE ONE THING STILL UNRESOLVED IS WHERE TO SEND IT.** No submission
  channel is recorded anywhere in this repo, and `edmonton.ca` is **unreachable
  from the Oracle box** (`000`/connection failure on 2026-08-12, while
  `data.edmonton.ca`, `alberta.ca` and `open.alberta.ca` all resolve). Finding
  the right intake — Open Data portal contact form vs. the Assessment & Taxation
  Branch vs. 311 — needs a machine that can reach it.
