# Source verification report (v002)

Prepared 22 November 2026. The study area is Malé island proper. Every decision here comes from reading the source body: the article text, an official PDF page or a register row. Each source was fetched once on 22 Nov 2026 (16:24–16:27 UTC). All fetches are logged in `00_catalog/source_fetch_log_20261122.csv`.

The reviewer is Claude (AI-assisted). Each decision still needs a human reviewer before its sprint task moves to *Done*.

No model was retrained, and nothing was pushed to GitHub.

**"Accepted" means the report was found and its date, place and cause were read and interpreted.** It does not mean measured flood extent, depth or independently observed ground truth. Every label is positive-only. A day without a report remains unlabelled.

## 1. What was checked

| Item | Count |
|---|---:|
| Registered sources | 71 |
| Sources whose body was read | 71 (SRC0027 partly: its list of pump areas did not render) |
| Fetched directly | 59 |
| Fetched via `en02.sun.mv` (see.mv returned HTTP 403) | 7 |
| Fetched via Internet Archive | 5 |
| Unique sources after URL de-duplication | 69 |
| Official documents saved locally | 7 (`01_raw/flood_evidence/official_records/`) |

The two de-duplicated pairs are SRC0046 → SRC0019 (Edition article 35325) and SRC0063 → SRC0030 (Sun article 104638). Aliases are kept in `canonical_source_id`.

News articles are not stored, because of publisher copyright. Each news source keeps its URL, access route, publication metadata and a short excerpt. For the 10 Dhivehi articles, the excerpt is in the original Thaana with an English translation. The translations are AI-made and have not been checked by a Dhivehi speaker.

Three Ras articles show no publication date. Their dates were bracketed by the neighbouring post IDs, and each bracket agrees with the imported time:

| Source | Bracketing posts |
|---|---|
| SRC0001 | 18 May 2020, 20:50–22:18 |
| SRC0022 | before 21 Dec 2024, 10:33 |
| SRC0033 | 4 Aug 2026, 17:17–19:30 |

### Publication clocks

| Clock status | Publishers | How it was established |
|---|---|---|
| Explicit +05:00 | Plus, Standard, Mihaaru | Offset printed in the page metadata |
| UTC+5 | Ras, Edition, PSM, archive.mv | The pages showed "latest" times later than the UTC fetch time, which rules out UTC |
| UTC+5 | Adhadhu | Page clock is labelled "Maldives time (MVT)" |
| UTC | MVRepublic | Explicit +00:00 |
| Not established | Sun, Atoll Times (date only), One Online, ThePress, Avas, Raajje, MMTV, MFR | No decisive evidence |

Edition's JSON-LD `datePublished` has no offset and is UTC; the time Edition displays is local. A publication time is never treated as flood onset.

## 2. Decisions

The table covers all 43 reviewed events: 41 from 2020 onward and 2 older coastal events. Full rows are in `03_reviewed/events/flood_events.csv`. Event-to-source links are in `event_source_links.csv`. The mapping from every original record is in `record_crosswalk.csv`.

| Decision (study period 2020–2026) | Events |
|---|---:|
| accepted_reported_rain_event | 30 |
| accepted_reported_coastal_event | 4 |
| mixed_or_uncertain_cause | 2 (EVT0001 18 May 2020; EVT0026 17 Dec 2024) |
| uncertain_date | 4 (30 Dec 2023; 13 Jan 2024; 14 Aug 2024; mid-Nov 2024 window) |
| uncertain_location | 1 (6 Aug 2023 coastal) |
| conflicting_evidence | 0 (every named conflict was resolved or reduced to a timing note) |
| excluded | 0 events; 13 Groundsource-only windows excluded in the crosswalk |

The 30 accepted rain events break down as follows:

- **27 single primary days.** In 5 of these, flooding continued past midnight; that is recorded as persistence, not as a new day.
- **1 event with both days explicitly reported:** 11–12 Dec 2021. The 12 Dec day rests on one source.
- **2 overnight windows**, where the event cannot be put on a single day:
  - 20–21 Dec 2024
  - 10–11 Jan 2025

  Neither day of a window may be used as a daily positive on its own.
- **29 distinct calendar days** with an accepted single-day or both-days report.
- **3 property-level official records:** OFF001, OFF003 and OFF004. Treat them separately from street or citywide reports.
- **13 events rest on a single source.** Six of these are official single-line statements: MMS on 16 Feb, 8 May and 25 May 2024, and the three NDMA property records. Check them before giving them any weight.

The 4 accepted coastal events are:

- 5 Nov 2022
- 31 Jul 2023 (NDMA "Surges"; found in this pass)
- 5 Aug 2023
- 26 Jul 2026

Two coastal events fall before the study period: the 2004 tsunami and 15 Jun 2019. Coastal events are a separate target from rain events.

### Outcome for the 30 imported records

| Imported records | Outcome |
|---|---|
| 25 records | accepted rain events |
| RAIN001 | mixed rain and swell |
| OFF005 | response-only evidence; cause not stated |
| COAST001, COAST003 | accepted coastal |
| COAST002 | 5 Aug accepted; 6 Aug location not established |

Records that add no new evidence: RAIN008, RAIN011 and RAIN022 cite the same article as the compiled records. RAIN019 is the same Sun article on another host.

### Legacy "uncertain" decisions that are now superseded

Seven earlier decisions are superseded. Each old decision is kept in `legacy_decision`.

| Date | Basis for the new decision |
|---|---|
| 11 Dec 2021 | Ras reports flooding "yesterday and today", independently of the JICA photos |
| 1 Apr 2023 | See RAIN004 in section 3 |
| 12 Jan 2024 | The Sun article earlier recorded as blocked is readable on `en02.sun.mv` |
| 20–21 Dec 2024 | Three accessible sources and MMS describe the overnight flooding |
| 11 Mar 2025 | ThePress reported it the same evening |
| 16 Apr 2026 | The article is readable |
| 4 May 2026 | The article is readable via the Internet Archive |

### Found during verification (not previously in any inventory)

These came from official documents:

- MMS Severe Weather Report 2024:
  - flooding in Malé on 16 Feb 2024 (accepted)
  - flooding in Malé on 25 May 2024 (accepted)
  - "August 14" photo caption (uncertain date)
  - mid-November 2024 flooding with no date given (uncertain window)
- NDMA register: 13 Jan 2024 (uncertain date).
- NDMA statistics page: coastal surges on 31 Jul 2023 (accepted) and 5 Aug 2023 (supports COAST002).

## 3. The named conflicts

### OFF003 (18 Sep 2024): resolved as separate incidents

On page 62, the NDMA register lists two cases in Malé on 18 Sep 2024:

- **#193:** "Rain water flooding", H. Dhoohimerige – Hulhangubai – Print
- **#194:** "Fire Incidents", G. Sindhu Hiya

The assistance table on page 57 has a row 69 dated 18-Sep-2024 under "Fire Incidents". That matches case #194. There is no rainwater assistance row for that date. So the "fire label" belongs to a different incident at a different property; it is not a reclassification of #193.

OFF003 is accepted as a property-level rainwater record. One context note: the same property had a fire on 9 Sep (case #190). The register does not say whether the rainwater entered through fire damage.

### RAIN018 (26–27 Nov 2025) versus the compiled 25 Nov 2025 record: both stand

| Date | Source | What it says |
|---|---|---|
| 25 Nov 2025 | Adhadhu, dated 25 Nov 2025 (MVT) | "Heavy continuous rain since early morning Tuesday has caused flooding in parts of Male' city", in Maafannu and near IGMH, with no pumps running as of 07:00 |
| 26 Nov 2025 | Edition, 26 Nov 2025 at 16:04 local | Rain "began past 1:00pm" on Wednesday 26 Nov and flooded the streets; seven pumps set up |
| 27 Nov 2025 | Sun, 27 Nov 2025 at 00:44 | Malé "remains flooded following hours of downpour on Wednesday" |

The import described RAIN018 as a "correction" of 25 Nov. The sources do not support that. Both dates are accepted as separate reported days (EVT0033 and EVT0034). They form a provisional storm group (STORM0028). 27 Nov is persistence only. Both histories are kept: the legacy *include* for 25 Nov, and the import's correction wording, quoted in `conflicts`.

### RAIN004 (1 Apr 2023): accepted

- **Atoll Times** (dated 2 Apr) reports heavy rain on "Saturday morning" that flooded the city, worst in the West Park area and M. Bihuge on Haveeree Hingun.
- **MFR** (dated 1 Apr) describes "the late hours of last night, 1st April 2023". Read against its own 1 April date, "last night" is the night ending on the morning of 1 April. That removes the contradiction the legacy review saw.
- **Station record:** the Hulhulé SYNOP 6-hour group for 00–06 UTC on 1 Apr (05:00–11:00 local, Saturday) records **49.0 mm**. The earlier "GSOD 0.0 mm" was GSOD's 1 Apr value, which covers 05:00 on 31 Mar to 05:00 on 1 Apr. GSOD's 2 Apr value of 4.8 mm is one-tenth of 49 mm, which is the 24-hour group defect described in `TIME_ALIGNMENT_REPORT.md`.
- **ERA5:** shows 0.9 mm. This is reanalysis, not an observation.

The two articles still disagree on time of day ("late night" versus "morning"), and that disagreement is kept in the record.

### RAIN007 (31 Dec 2023): traced

- **Atoll Times** quotes the MET: **179.7 mm** at Hulhulé, "from 8 am Sunday to 8 am Monday" (08:00 on 31 Dec to 08:00 on 1 Jan, local time), the highest ever recorded there. The Council VLR (2025) also gives 179.7 mm.
- **179.9 mm** appears only in MVRepublic ("within 24 hours"). It is treated as an unsupported digit variant.
- The original MMS bulletin was not retrieved.
- **Station record:** the Hulhulé SYNOP 12-hour group for 00–12 UTC on 31 Dec (05:00–17:00 local) records **184.0 mm**. The following 12 hours add 5.0 mm. Rainfall is in millimetres; the ISD quality code is 1 ("passed all QC").
- **Why the earlier comparison failed:**
  - The **4.3 mm** comparison was GSOD's 31 Dec value. That is the 24 hours ending at 05:00 local on 31 Dec, which is *before* the storm.
  - The storm falls in GSOD's 1 Jan value (18.8 mm, flag G). That value comes from a 24-hour group of 18.9 mm, which is one-tenth of the roughly 189 mm in the 12-hour groups.

The reported amount is therefore consistent with the station's 12-hour record.

### RAIN010 (13 Apr 2024) and RAIN014 (10–11 Jan 2025): dates settled, intraday timing open

**RAIN010.** Edition says the rain was on Saturday afternoon; Sun says Saturday morning. Both agree on Saturday 13 Apr, and NDMA case #52 is dated 13 Apr.

- At Hulhulé, the SYNOP record shows 0 mm for 05:00–11:00 local and 86 mm for 11:00–17:00.
- The station is not on Malé island, so the article disagreement stays unresolved.
- Edition's 00:00 publication on 14 Apr ("streets remain flooded") counts as persistence, not a second day.

**RAIN014.** The date window holds; the timing does not resolve.

- Atoll Times: flooding "since Friday evening".
- Standard: rain began in the early evening and intensified by midnight.
- Plus: torrential rain "early this morning".
- MMS: Malé 130.7 mm, 08:00 Friday 10 Jan to 08:00 Saturday 11 Jan.
- At Hulhulé: 8 mm for 17:00–23:00 on 10 Jan, 62 mm for 23:00–05:00, and 31 mm for 05:00–11:00 on 11 Jan.

The event is kept as an overnight window, 10–11 Jan, with both timing descriptions recorded.

## 4. Other source findings

- **Station names conflict.** Sun attributes 143.4 mm on 12 Jan 2024 to Hulhumalé; the MMS report attributes it to the Hulhulé NMC. Sun attributes 117 mm on 20 Dec 2024 to Hulhumalé; MMS and Atoll Times give 117.4 mm for Hulhulé. The compiled "Hulhulé 63.4 mm" for 13 Aug 2024 is Hulhumalé in Sun.
- **Origin of "40–45 mm".** Sun (14 Aug 2024), quoting PSM, reports an MMS official saying Malé "is prone to flooding with just 40 or 45 millimeters". It is an official's remark, not a published threshold.
- **Reused photo.** SRC0049's photo caption is dated 31 Dec 2023. It was not used as evidence.
- **Corrected titles.** Several registered titles were blank or belonged to another story: SRC0005, SRC0010, SRC0017, SRC0022, SRC0029. The page titles are now recorded.
- **Groundsource-only windows.** Thirteen windows have no article or record, so they stay excluded. They are not evidence of "no flood". Two others now coincide with MMS statements: 18 Nov 2024 (uncertain window) and 17 Dec 2024 (response-only).

## 5. Classification of the outstanding files

| File | Inspection result | Classification |
|---|---|---|
| `hulhule_station_daily_2020-2025.csv` (compiler GSOD) | Checked against raw NOAA GSOD for 2020–2025: all 2,049 precipitation values equal PRCP × 25.4; all 57 `99.99` values are blank; flags are identical; F→C, knots→km/h and FRSHTT conversions are correct. | Derived working data with a verified conversion. It inherits GSOD's date convention and the 24-hour defect. The raw 2020–2023 GSOD files have now been added (DS0064–DS0067). |
| `male_daily_features_with_flood_labels.csv` | All columns reproduce exactly: ERA5 daily as labelled; compiled GSOD on the same date, which is the wrong window; rolling sums; marine daily maximum. Its `flood_reported` column has 22 positive days, which include days now judged uncertain and leave out accepted ones. Its 0 values mean "no report found". | Legacy derived data, superseded. Not for modelling. |
| `landmark_checks.csv` | 29 per-place source checks: 22 verified and 7 with a blocked source. Most evidence types are `dewatering_only`. | Spatial-reference and review material for road and landmark mapping. These are not flood-risk observations or labels. |
| `bobs flood.xlsx` (Downloads) | One sheet with a monthly table (Jan 2023–Jul 2026): houses affected, drains cleared, roads repaired, monthly rainfall. Created 16 Aug 2026. Its charts link to `D:\Flooding in Male' city\…`. | Imported unchanged to `01_raw/flood_evidence/compiled_secondary/bobs_flood_workbook/`. Monthly context only; it cannot verify events. It is excluded from the ZIP until permission to use it is confirmed. |

## 6. Limits of this pass

- Reviewed by AI only; human review is pending.
- The Dhivehi translations are not checked by a Dhivehi speaker.
- One reading per source; no second fetch for comparison.
- The MMS 2023 bulletin and the original MMS 2024 PDF URL were not retrieved (a 2026 Internet Archive copy was used instead).
- No search was made for new articles on the 13 Groundsource-only windows, or on dates with no report.
- Observation coverage is still unknown, so non-flood days cannot be labelled.
