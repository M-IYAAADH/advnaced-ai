# Handover: Malé flood AI data status (22 Nov 2026)

This handover is self-contained. Every number was recomputed from the files on 22 Nov 2026.

## Project

- University Advanced AI project: *Geospatial-Based Flood Risk Modelling and Predictive Analysis Using AI*.
- Study area: **Malé island proper**, Maldives. Not Hulhumalé, Vilimalé or Greater Malé.
- Recorded research question: *which roads or road sections on Malé are prone to rain flooding?* This is susceptibility mapping, not forecasting. A daily reported-flood experiment exists only as supporting analysis.
- Deliverables: a six-page IJCAI-format literature review (≥ 15 journal articles) plus the project. Deadline 30 May 2027, 00:00 UTC+5.

## Data present (actual files)

- **Rainfall:**
  - ERA5 via Open-Meteo for a Malé grid point: hourly 2020-01-01 to 2026-11-13, 60,216 rows, complete for all 2,509 days. The `time_local` offset is undocumented, and the request was not saved.
  - NOAA GSOD for **Hulhulé airport** (not Malé): raw 2024 (355 rows) and 2025 (236 rows, to 24 Aug). PRCP in inches. One `99.99` is missing, not zero (17 Apr 2024). 47 days ≥ 25.4 mm.
  - A compiler-converted GSOD version for 2020 to 24 Aug 2025: 1,992 days with a value, 57 missing values, 460 days with no row.
  - NOAA hourly reports for 2024 to Aug 2025 (6, 12 and 24 h accumulation groups only; no 1 h group).
  - A 5-day NASA POWER sample, one CHIRPS day, and one MET Norway forecast snapshot (not an archive).
- **Sea level:**
  - **Observed:** UHSLC Malé gauge, 2024 only. 8,784 hourly rows, 125 missing, mm relative to station zero, UTC.
  - **Modelled:** Open-Meteo Marine, valid from 2022-11-23. 1,431 complete days.
  - The two are not pooled.
- **Spatial:** OneMap and OSM island polygons; 571 OSM roads; building layers kept separate (OSM 933; Microsoft 4,677; Google 10,077, of which 5,773 have confidence ≥ 0.75); WorldCover 2021; WorldPop 2025 (modelled); FABDEM 30 m (median 5.04 m on Malé, implausible and unvalidated).
- **Groundsource 2026** (Google, news-derived): 2,646,302 polygons, 2000-01-01 to 2026-02-03. No place, cause or article fields. An earlier screen found 43 polygons touching Malé; these are leads only.
- **Missing:**
  - no saved copy of any article or official PDF (URLs only)
  - no Malé rain gauge
  - no observed dry days or observation-coverage records
  - no drainage GIS, surveyed DEM or forecast archive

## Rainfall versus sea-level coverage (nominal days)

| Coverage | Days | Proxy episodes covered (of 28) |
|---|---:|---:|
| ERA5 rainfall only | 2,509 | 28 |
| ERA5 + modelled sea level (from 2022-11-24) | 1,431 | 25 |
| Hulhulé GSOD present (to 2025-08-24) | 1,992 | 20 |
| ERA5 + modelled sea level + GSOD | 924 | 17 |
| ERA5 + observed tide gauge (2024) | 357 | 8 |

## Flood evidence and counts

- **New import** (`male_flood_inventory.csv`, a chat export): 30 records, matching the expected 22 news rain windows, 3 coastal windows and 5 official leads. The windows span 36 calendar days (32 rain-associated, 4 coastal). Every record is `pending_review_not_final_label`, with storm status unresolved and flood onset unknown.
- **Existing compilation:** 18 incidents over 22 days, December 2021 to October 2026. The legacy review included 11 and marked 7 uncertain. Storm proxies S01–S17 come from a ≤ 2-day merge rule.
- **Reconciliation, import versus existing:**
  - exact match with a compiled incident: 10
  - date overlap: 5
  - starter-pack or Groundsource lead only: 5
  - one day from a compiled incident: 1 (RAIN018)
  - no prior record: 9
  - Three imports repeat the compiled article (RAIN008, RAIN011, RAIN022).
  - 20 imported days are new relative to the compilation. Import plus compilation gives 38 rain-associated candidate days and 28 proxy episodes (26 without the two uncertain-mechanism records).
- **Verified storm groups: 0. Accepted flood labels: 0.**
- **Conflicts that must stay visible:**
  - **OFF003** (18 Sep 2024): NDMA rainwater entry versus a fire label.
  - **RAIN018** (26–27 Nov 2025) versus the compiled 25 Nov 2025 *include*.
  - **RAIN004** (1 Apr 2023): ERA5 0.9 mm and GSOD 0.0 mm that day; time-of-day disagreement.
  - **RAIN010** (13–14 Apr 2024) and **RAIN014** (10–11 Jan 2025): intraday timing.
  - **RAIN007** (31 Dec 2023): reported 179.9 mm at Hulhulé versus 4.3 mm in GSOD.
  - RAIN001 (18 May 2020) may be mixed rain and seawater.
- **Records that should prompt re-review of uncertain legacy dates:** RAIN002, RAIN004, RAIN009, RAIN012, RAIN016, RAIN019.
- **New single-source dates:** RAIN001, RAIN005, RAIN017, RAIN020, RAIN021, COAST001, COAST003.
- **Awaiting document retrieval:** OFF002 and OFF005 (MMS report).
- **Coastal:** 3 windows (5 Nov 2022, 5–6 Aug 2023, 26 Jul 2026), kept out of the rain target.

## Time and provenance

- **Verified UTC:** NOAA hourly, UHSLC, NASA POWER, MET Norway.
- **Unresolved:** ERA5 and modelled sea-level offsets (tide correlation r = 0.963 at UTC+4, 0.959 at UTC+5). Accumulation windows are also unresolved.
- **Hypothesis only:** GSOD totals land one day after reported floods on 12 Jan 2024, 14 Apr 2024, 20 Dec 2024 and 11 Mar 2025.
- In the import, publication timezones are unknown. Clocks are kept with their qualifiers: rain started "approximately 11:00" (RAIN011) and "after 13:00" (RAIN018); pumping started at 21:40 (RAIN017). These are not flood onsets.
- The imported list and the compilation are both secondary, AI-assisted research. Groundsource has no link from record to article.

## What was cleaned

- GSOD 2024–25: converted to mm, missing values kept as missing, raw values kept.
- UHSLC 2024: explicit UTC, no datum change.
- A per-day coverage table, in which every day is `unlabelled`.
- A validated copy of the import.

No timezone, accumulation or date shift was applied. No model was retrained.

## What the data can support

- A retrospective same-day comparison of reported-flood days with ERA5 rain, measuring agreement with reports. False-alarm rates are not estimable.
- A modelled sea-level comparison only from 2022-11-24.
- **No true advance forecast**, because there is no forecast archive and the alignment is unresolved.
- Road susceptibility remains descriptive, from positive-only and arterial-biased reports. The import adds no structured road names.

## Next steps

1. Save the articles and PDFs locally.
2. Resolve the six conflicts listed above.
3. Re-review the uncertain dates and write the first accepted rows to the canonical reviewed event table.
4. Group storms from the evidence.
5. Re-request ERA5 with an explicit timezone, and test the GSOD day shift against NOAA 24 h groups.
6. Build versioned features and storm-grouped chronological splits.
7. Request agency flood/dry location records and MMS gauge rainfall.
