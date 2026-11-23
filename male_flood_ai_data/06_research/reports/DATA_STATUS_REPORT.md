# Malé flood AI: data status report

Prepared 22 November 2026, from the files themselves. This report covers the organised folder `male_flood_ai_data/` and the package `male_flood_ai_data_20261122T161053Z.zip`. Counts were recomputed in this pass rather than copied from earlier reports. Where an earlier figure is repeated, its source is named.

The study area is **Malé island proper**. No model was retrained. No record was promoted to an accepted flood label.

## 1. What was done

1. **Inventory.** Every repository file was checksummed (SHA-256), except `.git`, caches and virtual environments. This included untracked files such as `groundsource_2026.parquet` and `male_flood_inventory.csv`. All 55 data files (CSV, GeoJSON, GeoTIFF, GeoParquet) were profiled completely. For the 636 MiB Groundsource file, this used parquet metadata plus a chunked scan of its `uuid`, `start_date` and `end_date` columns; geometry was never loaded. Results are in `00_catalog/dataset_inventory.csv` (63 rows, including the cleaned and review tables), `data_quality_summary.csv` and `data_dictionary.csv`.
2. **Organisation.** Files were copied into the template, never moved. The originals and every working path in the repository are untouched. Each copy was verified against the original SHA-256: 158 copy records, 0 mismatches, 0 conflicts with pre-existing files. The archive check is in `PACKAGE_VERIFICATION.md`. Every mapping is in `00_catalog/file_mapping.csv`. No two repository files are byte-identical (`duplicate_files_by_checksum.csv` is empty). The `male_flood_inventory.csv` in Downloads is byte-identical to the repository copy and is recorded as a duplicate, not copied again.
3. **Import and reconciliation.** The new CSV is preserved unchanged at `02_interim/event_candidates/male_flood_inventory.csv`. All 30 records are reconciled in `inventory_reconciliation.csv`, alongside the 3 existing compiled incidents the import does not mention. All sources are registered in `00_catalog/source_register.csv`.
4. **Cleaning.** Four working copies were written to `02_interim/`, with input/output row counts in `02_interim/cleaning_log_v001.csv`. See section 7.

Template additions are recorded in `file_mapping.csv`: `01_raw/rainfall/satellite/`, `01_raw/geospatial/{mapping,elevation}/`, `01_raw/flood_evidence/compiled_secondary/` and `05_outputs/legacy/{road_evidence,scripts}/`. The new organising scripts are in `00_catalog/tools/`.

### Files needing human classification

| File | Placed in | Question |
|---|---|---|
| `male-flood-basis/data/hulhule_station_daily_2020-2025.csv` | `01_raw/rainfall/station/compiled_hulhule_gsod_metric/` | Compiler-converted GSOD (metric, 99.99 blanked): raw or interim? It is the only station series before 2024 and is not unchanged NOAA bytes. |
| `male-flood-basis/data/male_daily_features_with_flood_labels.csv` | `02_interim/weather_aligned/male_flood_basis_daily_features/` | The derivation is undocumented and `flood_reported = 0` means "no report found". Keep as interim, or retire? |
| `verification/landmark_checks.csv` | `03_reviewed/events/legacy_landmark_checks/` | Per-place source checks: are they reviewed evidence, or a legacy output? |

## 2. What data is present

### Present and usable (with caveats)

| Dataset | Rows | Actual coverage | Nature | Key quality facts |
|---|---:|---|---|---|
| ERA5 via Open-Meteo, hourly (`male_reanalysis_hourly_2020-2026.csv`) | 60,216 | 2020-01-01T00 to 2026-11-13T23 | reanalysis, Malé grid point | No gaps, missing values or duplicates; all 2,509 days have 24 h. `time_local` offset undocumented. |
| ERA5 daily | 2,509 | 2020-01-01 to 2026-11-13 | reanalysis | Equals hourly sums by nominal day. |
| Modelled sea level and waves (Open-Meteo Marine) | 42,672 | sea level valid from 2022-11-23T05 to 2026-11-13 | **modelled** | 8,261 blank sea-level cells; 1,431 complete days. Model datum. |
| NOAA GSOD, Hulhulé station 43555099999, raw 2024 and 2025 | 355 + 236 | 2024-01-01 to 2025-08-24 | measured, **Hulhulé airport, not Malé** | PRCP in inches. One `99.99` (17 Apr 2024) is missing, not zero. 590 valid values; 338 zero days; 47 days ≥ 25.4 mm (26 in 2024, 21 in 2025) before flag filtering. 11 calendar dates absent in 2024. Flags: G 563, E 14, H 5, B 3, A 2, F 2, I 1. |
| GSOD compiled metric version 2020–2025 | 2,049 | 2020-01-01 to 2025-08-24 | measured, converted | Across 2020-01-01 to 2026-11-13: 1,308 zero days, 684 positive, 57 missing values, 460 days with no row (including every day after 24 Aug 2025). |
| NOAA Global Hourly reports 2024, 2025 | 10,784; 7,198 | 2024-01-01 to 2025-08-24T21 UTC | measured | 2,584 and 1,741 repeated timestamps are distinct report types (FM-12/15/16), not errors. AA rainfall groups are 6, 12 or 24 h; no 1 h group verified. |
| NOAA precipitation accumulations (derived) | 1,666; 1,128 | same | measured, extracted | Overlapping windows; do not sum. |
| UHSLC Malé tide gauge, record 1082 | 8,784 | 2024-01-01 to 2024-12-31 UTC | **measured** | 125 missing; no irregular steps; 1,372–2,610 mm relative to station zero. This is not mean sea level or a flood depth. 357 complete UTC days. |
| NASA POWER (MERRA-2) | 120 | 1–5 Jan 2025 | reanalysis sample | UTC, plus a derived UTC+5 column. |
| CHIRPS v3 context tile | 9 cells | 3 Jan 2025 | satellite estimate | One cell is −9999 and is not declared as nodata. |
| MET Norway forecast | 91 | 2026-11-14T15 to 2026-11-24 UTC | forecast | One snapshot, not an archive. |
| Groundsource 2026 | 2,646,302 | 2000-01-01 to 2026-02-03 | news-derived (Gemini) | No null cells, duplicate UUIDs or reversed intervals. There are no place-name, article or cause fields. The earlier screen found 43 polygons touching the OneMap Malé boundary; these are candidate leads, not footprints. |
| OneMap Malé polygon; OSM island polygon | 1; 1 | — | official / volunteered | EPSG:4326. The two boundaries differ; reconcile before joins. |
| OSM roads, land use, buildings | 571, 51, 933 | snapshot 2026-11-13 | mapped | No invalid coordinates. |
| Microsoft and Google buildings | 4,677; 10,077 (5,773 at confidence ≥ 0.75) | — | ML detections | Kept separate; not ground truth. |
| FABDEM Malé clip / tile N04E073 | 2,169 valid cells / 12,960,000 | — | modelled DEM | Clip median 5.04 m, max 15.15 m: implausible for Malé and unvalidated. |
| WorldCover 2021; WorldPop 2025 | 24,188; 233 valid cells | — | modelled | Land cover is not imperviousness. Population is modelled. |

### Flood evidence present

| Source | Records | Nature |
|---|---:|---|
| Imported `male_flood_inventory.csv` | 30 | News- and record-derived candidates from a chat export. The export says no source was re-verified when the CSV was created. |
| male-flood-basis compiled incidents | 18 incidents, 22 calendar days | AI-assisted secondary compilation |
| Compiled roads and places | 32 rows; 31 GeoJSON features | positive-only |
| Starter-pack leads | 3 | city-level official leads |
| Legacy review decisions | 18 (11 include, 7 uncertain) | earlier manual source checks |
| Landmark source checks | 29 | earlier manual checks |
| Groundsource review | 260 regional, 55 local-screen and 29 comparison windows | spatial-screen leads |

### Missing, or only mentioned

- **No saved article or document copies.** Every news and official source is a URL. `01_raw/flood_evidence/news_english/`, `news_dhivehi/` and `official_records/` are empty. Of the 71 registered sources, none has a `local_evidence_path`.
- Mentioned but not downloaded:
  - NDMA 2024 incident PDF
  - MMS annual report (its URL redirected earlier)
  - Council VLR 2025
  - JICA survey report
  - NDMA DALA CSVs
  - IMERG
  - direct ERA5/CDS download
  - Copernicus GLO-30
  - Dynamic World
- Not available as open data:
  - Malé gauge rainfall (MMS)
  - observed flooded/dry location records
  - observation-coverage records
  - drainage GIS, pump records, surveyed DEM
  - historical forecast archive
  - observed tide data other than 2024
  - the original Open-Meteo request parameters
- Empty template tables: `03_reviewed/events/flood_events.csv`, `event_source_links.csv` and `observation_coverage/observation_coverage.csv` are deliberately unpopulated, because nothing has passed review. `04_model_ready/` contains headers only and `05_outputs/runs/` holds no run.
- Not inspected: `bobs flood.xlsx` and a property-registration workbook in Downloads. Neither is in the repository or the supplied ZIP.

## 3. Rainfall-only coverage versus common rainfall/sea-level coverage

Counts below are nominal days, 2020-01-01 to 2026-11-13 (`02_interim/weather_aligned/daily_series_coverage_2020-2026_v001.csv`). Episodes are the 28 rain-associated proxy episodes in section 4.

| Coverage | Days | Dates | Episodes covered |
|---|---:|---|---:|
| ERA5 rainfall only | 2,509 | 2020-01-01 to 2026-11-13 | 28 of 28 |
| ERA5 + modelled sea level (both complete) | 1,431 | 2022-11-24 to 2026-11-13 | 25 |
| Hulhulé GSOD rainfall present | 1,992 | 2020-01-01 to 2025-08-24 | 20 |
| ERA5 + modelled sea level + GSOD | 924 | 2022-11-24 to 2025-08-24 | 17 |
| ERA5 + observed tide gauge (complete UTC day) | 357 | 2024 only | 8 |

Day alignment between these series is unresolved, so the joint counts depend on taking each file's own day label at face value.

## 4. Event records, reported dates and storm groups

These are counted separately because they measure different things.

| Measure | Count | Note |
|---|---:|---|
| Imported records | 30 | 22 news rain windows, 3 news coastal windows, 5 official leads. Matches the expected composition. |
| Calendar days in imported windows | 36 | 32 rain-associated, 4 coastal. Windows are not daily ground truth. |
| Imported days not covered by any compiled incident | 20 | new candidate dates relative to the 18 compiled incidents |
| Compiled incidents / days | 18 / 22 | unchanged |
| Rain-associated candidate days, import ∪ compiled | 38 | candidate dates, not labels |
| Rain-associated proxy episodes (≤ 2-day merge rule) | 28 | 26 without RAIN001 (possibly mixed) and OFF003 (classification conflict). This is a counting device, not a storm count. |
| Coastal candidate windows | 3 (4 days) | separate target type |
| Legacy storm proxies (`storm_groups.csv`) | 17 | status `legacy_proxy_not_verified` |
| **Verified independent storm groups** | **0** | No grouping has been reviewed. |
| **Accepted flood labels** | **0** | `03_reviewed/events/flood_events.csv` is empty. |

### Reconciliation outcome (30 imported records)

| Match type | Records |
|---|---|
| Exact match with a compiled incident (10) | RAIN003, RAIN004, RAIN006, RAIN008, RAIN009, RAIN011, RAIN012, RAIN015, RAIN019, RAIN022 |
| Date overlap, possible duplicate (5) | RAIN002, RAIN007, RAIN013, RAIN014, RAIN016 |
| Matches only a starter-pack or Groundsource lead (5) | COAST002, OFF001, RAIN010, OFF004, OFF005 |
| Nearby date, possible same storm (1) | RAIN018, one day after compiled 25 Nov 2025 |
| No existing match (9) | RAIN001, COAST001, RAIN005, OFF002, OFF003, RAIN017, COAST003, RAIN020, RAIN021 |

RAIN008, RAIN011 and RAIN022 cite the same article as the compiled record, so they add no new evidence. RAIN019 cites the same Sun article number on a different host. Three compiled incidents are absent from the import: 25 Nov 2025, 4 May 2026 and 30 Jul 2026. Absence from the import is not evidence against them.

### Usable, uncertain, conflicting or awaiting verification

All 30 imported records remain candidates. The status below is a recommendation for review only.

- **Supporting evidence for existing incidents (11).** Five add an independent source to an incident already included in the legacy review: RAIN003, RAIN006, RAIN007, RAIN013 and RAIN015. Three duplicate an existing article: RAIN008, RAIN011 and RAIN022. Three link to existing incidents that the review left uncertain and should prompt a re-review:
  - RAIN009 (12 Jan 2024: an accessible Sun source replaces a blocked one)
  - RAIN012 (20–21 Dec 2024)
  - RAIN016 (11 Mar 2025)

  RAIN002 and RAIN019 also bear on uncertain records (11 Dec 2021, 16 Apr 2026).
- **Conflicting (must stay visible):**
  - **OFF003**: NDMA rainwater entry versus a fire label in the assistance table.
  - **RAIN018 versus compiled 25 Nov 2025**: the import calls itself a correction, but the compiled record has its own *include* decision. Neither was overwritten.
  - **RAIN004**: the weekday confirms 1 Apr 2023, but ERA5 shows 0.9 mm and GSOD 0.0 mm that day, and the sources disagree on time of day.
  - **RAIN010 and RAIN014**: intraday timing disagreements.
  - **RAIN007**: reported 179.9 mm at Hulhulé versus 3.3–4.3 mm in GSOD.
- **Uncertain mechanism:** RAIN001 (its source mentions incoming seawater) and OFF003.
- **Awaiting verification, new dates with a single source:** RAIN001, RAIN005, RAIN017, RAIN020 and RAIN021; COAST001 and COAST003; RAIN010 (corroborated by NDMA, new to the compiled set); COAST002 (5 Aug matches the Groundsource coastal candidate, 6 Aug is still unverified).
- **Awaiting retrieval:** OFF002 and OFF005 (MMS report). OFF001 and OFF004 are property-level NDMA records.

## 5. What could support retrospective analysis or advance prediction

- **Retrospective (same-day) analysis:** ERA5 rainfall is the only series covering all 28 episodes. The modelled sea-level comparison is limited to 2022-11-24 onward (25 episodes). Station rainfall ends on 2025-08-24 and is on Hulhulé. With no observed non-flood days, results measure agreement with reported outcomes; false-alarm rates cannot be estimated.
- **Advance prediction:** not supported as a true forecast. There is no historical forecast archive, only one MET Norway snapshot. ERA5's real-time availability is not established, and timezone and day alignment are unresolved. The most these files can support is a lagged-observation experiment, labelled as such.
- **Road susceptibility (the recorded project question):** the inputs are still the positive-only, arterial-biased road and landmark evidence and OSM roads. The new import adds no road names: its location fields are empty and its locations appear only in free text.

## 6. Timezone, coverage and provenance issues still open

- ERA5 and modelled-sea-level `time_local` offsets are undocumented. For sea level, tide correlation cannot separate UTC+4 (r = 0.963) from UTC+5 (r = 0.959); this is an earlier finding. The Open-Meteo request was not saved.
- The GSOD day boundary and accumulation window are unverified. Totals land one day after the reported flood on 12 Jan 2024, 20 Dec 2024, 11 Mar 2025 and 14 Apr 2024 (RAIN010); this is recorded as a hypothesis only.
- Publication timezones in the import are unknown. Event clocks are kept as text with their qualifiers: "approximately 11:00" and "after 13:00" (rain start), and 21:40 (pumping start). No flood-onset time exists for any record.
- No observation-coverage evidence exists, so every day without a report is **unlabelled**.
- Provenance:
  - the compilation and the import are both secondary and AI-assisted
  - Groundsource has no record-to-article link
  - no article is saved locally
  - the Groundsource licence still needs confirming at Zenodo before redistribution
  - FABDEM is CC BY-NC-SA
  - MMS data, if received, may not be redistributed

The register is `03_reviewed/time_alignment/time_alignment_decisions.csv`. Its 9 rows: 4 unresolved (ERA5, modelled sea level, the import's clocks, the compiled incident dates), 1 hypothesis-only (GSOD day shift), and 4 verified as UTC (NOAA hourly, UHSLC, NASA POWER, MET Norway).

## 7. What was cleaned, and what was left unresolved

| Output | Input → output rows | Changes | Left alone |
|---|---|---|---|
| `hulhule_gsod_clean_2024-2025_v001.csv` | 591 → 591 | PRCP inches → mm (documented NOAA units). `99.99` → missing. Raw value and flag kept. Zero kept distinct from missing. | GSOD day versus local day; flag-based filtering. Temperature and wind units not converted. |
| `uhslc_male_1082_hourly_2024_clean_v001.csv` | 8,784 → 8,784 | Units row removed. Numeric mm. Explicit `+00:00`. | No datum change; no conversion to local time. |
| `daily_series_coverage_2020-2026_v001.csv` | 2,509 days | Per-day availability of each series. | `flood_label` is fixed to `unlabelled`. |
| `male_flood_inventory_clean_v001.csv` | 30 → 30 | ISO-date validity (all valid), window length, publication lag, multi-day flag, qualifier kept with its clock. | No timezone conversion; Thaana titles kept as UTF-8. |

Unresolved, deliberately: timezone offsets, accumulation windows, event-date shifts, storm grouping, and rain versus mixed classification. None was chosen on the basis of model performance.

## 8. Next concrete steps

1. **Save the evidence.** Download the NDMA 2024 PDF, the MMS annual report and each cited article into `01_raw/flood_evidence/`, and fill `local_evidence_path` and `accessed_at_utc` in the source register.
2. **Resolve the five conflicts** in section 4: OFF003, RAIN018 versus 25 Nov 2025, RAIN004, RAIN010/RAIN014 timing, and RAIN007 rainfall.
3. **Re-review the uncertain legacy decisions** using the new sources: 11 Dec 2021, 1 Apr 2023, 12 Jan 2024, 20–21 Dec 2024, 11 Mar 2025 and 16 Apr 2026. Then write the first accepted rows to `flood_events.csv` and `event_source_links.csv`, with a reviewer and a date.
4. **Group storms by reviewed evidence** in `storm_groups.csv`, not by the ≤ 2-day rule alone.
5. **Settle the time alignment:**
   - re-request ERA5 from Open-Meteo with an explicit `timezone=Asia/Male` (or UTC) and save the request
   - test the GSOD day shift against the NOAA hourly 24 h groups ending at 03 UTC (08:00 local)
6. **Then build `04_model_ready/`.** Write a versioned daily feature table from ERA5, with lags fixed at issue time, plus chronological storm-grouped splits. Keep modelled sea level as a separate feature set on its 2022-11-24 coverage.
7. **Send the agency requests** (MF-23 and MF-45): Council/NDMA flooded, dry and unknown location records with observation coverage, and MMS gauge rainfall.
