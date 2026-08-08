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
| Alberta requires a **liability code** internally | ⚠️ **LIKELY, NOT FULLY VERIFIED.** "Liability code" is a real Alberta Municipal Affairs term — **ASSET** (Assessment Shared Services Environment) is described as *"an Internet-based application and database of liability codes"*, and exempt property is reported to the province under codes in the *Recording and Reporting Information for Assessment Audit and Equalized Assessment* manual. ⚠️ The manual PDF on open.alberta.ca returned HTTP 520 on 2026-08-08, so the Table reference is from search-result text, **not read in the source**. **Confirm before sending.** |
| GIPOT figure "$15.7M, 2021-22" | ❌ **NOT USED HERE, and should not be.** Unverified; see `data/DATA.md`. It is also not an argument for this request. |

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
> **Why I believe the field already exists.** Municipalities in Alberta assign
> liability codes and report exempt property to Municipal Affairs through the
> ASSET (Assessment Shared Services Environment) system for assessment audit and
> equalized assessment purposes — exempt property is reported and then excluded
> from equalized assessment. The distinction is therefore already recorded per
> account as a matter of provincial reporting. The City of Calgary also
> discloses this status to property owners directly: its assessment notices
> carry a tax exemption status field. I am not aware of any Alberta municipality
> publishing it as open data, which is precisely why I am asking Edmonton.
>
> **A minimal version would be sufficient.** A boolean taxable/exempt column, or
> the liability code as recorded, would resolve it. Full statutory-basis detail
> (which MGA section grounds each exemption) would be valuable but is not
> necessary.
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
- If the ASSET/liability-code claim cannot be confirmed from the Municipal
  Affairs manual, cut the second half of that paragraph and ask the question
  plainly instead ("is a taxable/exempt indicator recorded per account?"). The
  request stands on its own without it.
