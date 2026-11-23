# Malé flood project: data inventory and progress report

**Update, 17 November 2026:** This inventory records the earlier state. The subsequent models, documented time-alignment sensitivity, dashboard and remaining validation gaps are in [extended analysis](extended_analysis.md). Its source-metadata findings supersede the tentative timezone and GSOD assumptions below.

Inspected 17 Nov 2026 by reading the files in `male-flood-basis/` and `Male_Flood_Data_Starter_Pack/` (pandas profiling, no files modified, no synthetic data). Tags: **[V]** verified in the files by me; **[D]** stated in a file's documentation but not independently checkable; **[A]** assumption or inference; **[U]** could not inspect.

## 0. Things to know first

- **Recorded research question differs from the brief you pasted.** The project record (CLAUDE.md, agent.md, 14 Nov 2026) fixes the question as "which roads or road sections on Malé island proper are prone to flooding" (susceptibility mapping, not forecasting). The brief says "predict flood risk using historical rainfall". Section 6 recommends how to reconcile them.
- **Council statement [user-reported, not in any file]:** maintenance logs and detailed road elevation data are unavailable. I could not verify this; I treat it as given. It removes the two agency items most useful for street-level modelling.
- **Study-area scope:** the weather and sea-level series are point/grid products near Malé, not island-specific gauges. The flood-incident files cover Greater Malé; only Malé-island rows should be used.

## 1. Data inventory

### 1.1 Weather, sea level and labels (`male-flood-basis/data/`)

Provenance for this folder: an AI-assisted compilation dated 14 Nov 2026 (`male-flood-basis/README.txt`, `flood_map.html`). The README names the sources, but the individual download calls are not recorded, so how each file was obtained is **[D]**.

| File | Rows x cols | What a row is | Coverage (verified) | Resolution / time | Type |
| --- | --- | --- | --- | --- | --- |
| `male_reanalysis_hourly_2020-2026.csv` | 60,216 x 12 | one hour, one grid point (Malé) | 2020-01-01T00:00 to 2026-11-13T23:00 | hourly, column `time_local` | ERA5 reanalysis via Open-Meteo **[D]** |
| `male_reanalysis_daily_2020-2026.csv` | 2,509 x 17 | one day | 2020-01-01 to 2026-11-13 | daily | same, daily aggregates |
| `male_sea_level_waves_hourly_2022-2026.csv` | 42,672 x 4 | one hour | file 2022-01-01 to 2026-11-13; sea level valid only from 2022-11-23T05:00 | hourly, `time_local` | Open-Meteo Marine, **modelled** sea level incl. tide, waves, swell **[D]** |
| `hulhule_station_daily_2020-2025.csv` | 2,049 x 14 | one day, Velana airport station (Hulhulé) | 2020-01-01 to 2025-08-24 | daily | NOAA GSOD observations, converted to metric **[D]** |
| `male_daily_features_with_flood_labels.csv` | 2,509 x 19 | one day, merged features and label | 2020-01-01 to 2026-11-13 | daily | derived by the compiler (merge of the above) |
| `flood_incidents_greater_male_2021-2026.csv` | 18 x 7 | one incident (storm) | 11 Dec 2021 to 21 Oct 2026 | date text only | news-derived compilation |
| `flooded_roads_and_places_greater_male.csv` / `flood_locations_greater_male.geojson` | 32 rows (Malé 27, Hulhumalé 3, Hulhulé 1, Villimalé 1) | one road, landmark or area | n/a | n/a | news-derived, positive-only |
| `male_forecast_hourly_snapshot_2026-11-14.csv` | 91 x 11 | forecast hour, one model run | 2026-11-14T15:00Z to 2026-11-24T00:00Z | hourly then 6-hourly, UTC | MET Norway forecast **[D]** |

Columns:
- Reanalysis hourly: `time_local, precipitation_mm, rain_mm, temperature_2m_degC, relative_humidity_2m_%, dew_point_2m_degC, pressure_msl_hPa, surface_pressure_hPa, cloud_cover_%, wind_speed_10m_kmh, wind_gusts_10m_kmh, wind_direction_10m_deg`. `precipitation_mm` and `rain_mm` are identical in all rows **[V]**.
- Sea level: `time_local, sea_level_height_msl_m, wave_height_m, swell_wave_height_m`.
- Station daily: `date, temp_mean_c, dewpoint_c, sea_level_pressure_hpa, visibility_km, wind_mean_kmh, wind_max_sustained_kmh, wind_gust_kmh, temp_max_c, temp_min_c, precip_mm, precip_flag, rain_observed, thunder_observed`.
- Features-with-labels: `date, flood_reported, incident_id, rain_mm_reanalysis, rain_mm_station, rain_prev3d_mm, rain_prev7d_mm, max_1h_rain_mm, max_3h_rain_mm, rain_hours, gust_max_kmh, wind_max_kmh, wind_dir_deg, pressure_min_hpa, humidity_mean_pct, cloud_mean_pct, temp_mean_c, sea_level_max_m, month`.
- Incidents: `incident_id, dates, summary, reported_rainfall, male_reported_mm, locations, source_urls`.
- Roads and places: `name, type, island, times_reported, incident_dates, latitude, longitude, note, source_urls`.

**Timezone and accumulation semantics (open issue).**
- `time_local` is not defined in any file. Correlating the sea-level column with UHSLC observed sea level (UTC) for 2024 gives r = 0.963 if `time_local` is UTC+4 and 0.959 if UTC+5, but 0.788 at +3, 0.775 at +6 and -0.25 at +0 **[V]**. So it is consistent with Maldives local time but one hour is not resolvable from tides.
- I could not check the ERA5 rainfall timezone: against the 5-day NASA POWER MERRA2 sample the hourly correlation is only about 0.06 to 0.07 at either offset **[V]**, so that test is uninformative.
- Whether `precipitation_mm` at hour t is the preceding or following hour's total is **not documented in the files [U]**. Open-Meteo documents hourly precipitation as the sum of the preceding hour **[A, from general knowledge, unchecked here]**.
- GSOD daily precipitation is a daily value dated by NOAA; the `precip_flag` letters are NOAA's accumulation flags **[D]**. Day boundaries are UTC days in GSOD **[A]**.

### 1.2 Starter pack (`Male_Flood_Data_Starter_Pack/`)

Obtained by an earlier research pass on 14 Nov 2026 from the official hosts named in each folder's metadata JSON **[D]**. READMEs and QA JSONs were read; the spatial rasters were **not** opened (see Section 7).

| File | Contents (verified unless noted) | Coverage | Licence **[D]** |
| --- | --- | --- | --- |
| `rainfall/noaa_global_hourly_2024_43555099999.csv` | 10,784 x 34 reports, station 435550/99999 (Velana, Hulhulé, 4.192 N 73.529 E) | 2024-01-01 to 2024-12-31 | NOAA, open |
| `rainfall/noaa_global_hourly_2025_43555099999.csv` | 7,198 x 34 | 2025-01-01 to 2025-08-24T21:00 | same |
| `rainfall/noaa_precipitation_accumulations_2024.csv`, `..._2025.csv` | derived: 1,666 and 1,128 precipitation groups (columns `observation_time_utc, accumulation_hours, precipitation_mm, condition_code, quality_code, raw_precipitation_group`) | 2024; 2025 to Aug | derived from NOAA |
| `rainfall/noaa_gsod_2024_43555099999.csv`, `..._2025_...csv` | 355 and 236 daily rows, PRCP in inches | 2024-01-01 to 2025-08-24 | NOAA |
| `rainfall/nasa_power_male_hourly_precipitation_20250101_20250105.csv` | 120 hourly rows, MERRA2 reanalysis, UTC and UTC+5 columns | 1-5 Jan 2025 only | NASA POWER |
| `rainfall/chirpsv3_sat_20250103_male_context.tif` | 3 x 3 cells, 3 Jan 2025; the README states 108.27 mm at the Malé pixel **[D]** | one day | CHIRPS |
| `tides/UHSLC_Male_Record1082_Hourly_2024.csv` | 8,784 hourly rows after a units row; sea level in mm relative to station zero, UTC; 8,659 valid, 125 missing per QA | 2024-01-01 to 2024-12-31 | free reuse with citation |
| `flood/event_candidates.csv` | 3 city-level date/source leads (1 Oct 2023, 31 Dec 2023, 12 Jan 2024) | n/a | n/a |
| `boundary/OneMap_Male_Island.geojson` | 1 polygon, official island boundary | n/a | OneMap |
| `mapping/male_osm_roads.geojson` | 571 LineStrings (fields `fclass, name, ref, oneway, maxspeed, bridge, tunnel`...) | n/a | ODbL |
| `mapping/male_osm_landuse.geojson` / `male_osm_buildings.geojson` | 51 / 933 polygons | n/a | ODbL |
| `mapping/male_microsoft_buildings.geojson` | 4,677 polygons (`height, confidence`) | n/a | per README |
| `mapping/male_google_buildings.geojson` (and `_conf075`) | 10,077 (5,773 at confidence >= 0.75) | n/a | per README |
| `elevation/Male_FABDEM_30m_masked.tif` (+ source tile) | FABDEM V1-2, about 30 m, 2,169 valid in-island samples; QA reports median 5.04 m and max 15.15 m | n/a | CC BY-NC-SA 4.0 |
| `mapping/male_worldcover_2021_10m.tif`, `male_worldpop_2025_100m.tif` | land cover and **modelled** population rasters | 2021; 2025 | open, per README |

## 2. Data quality (quantified)

**Reanalysis hourly [V]:** no missing values, no duplicate timestamps, perfectly regular 1-hour step, no negative rain. Maximum 32.6 mm in one hour (2020-08-06T09:00); 25 hours are >= 10 mm. Daily file equals the hourly sums to rounding.

**Sea level [V]:** regular hourly step, no duplicates. `sea_level_height_msl_m` is blank for 8,261 of 42,672 rows: 7,824 before the series starts (2022-11-23T05:00) and 437 after, in three runs (5 h on 2022-11-23, 168 h from 2024-06-12 05:00, 264 h from 2025-01-29 05:00). Range -0.27 to 1.05 m. Waves are complete from 2022-01-01. This is **modelled**, not gauge data. The only observed record is UHSLC 2024 (8,659 of 8,784 valid).

**Station daily (Hulhulé) [V]:**
- 2,049 rows over a 2,063-day span, so 14 calendar days are absent (3 in 2021, 11 in 2024).
- `precip_mm` is blank in 57 rows (49 in 2023). No `99.99` placeholders remain: the 17 Apr 2024 raw value was converted to blank.
- Four days exceed 100 mm: 14 Apr 2024 (108.5), 8 Aug 2024 (117.3), 4 Jan 2025 (144.3), 2 Mar 2025 (173.7).
- Flags: G 1,759, I 82, E 80, F 46, H 10, B 8, A 7. Not interpreted further.
- `rain_observed` disagrees with `precip_mm`: 450 days observed = 1 with 0 mm, and 183 days > 0 mm with observed = 0. Treat `rain_observed` as unreliable.
- The 590 rows for 2024-01-01 to 2025-08-24 match the raw Starter Pack GSOD files (converted from inches) within 0.1 mm, with the same blanks.

**Missing rainfall treated as zero?** I found **no** such conversion. Where the station value is blank, `rain_mm_station` in the features file is blank (517 blanks: 57 missing, 14 absent dates, and the 446 days after 24 Aug 2025). Zero rainfall is only used where the station recorded 0.0.

**NOAA hourly [V]:** the 2,584 (2024) and 1,741 (2025) duplicate timestamps are different report types at the same time (FM-12, FM-15, FM-16), not errors. Precipitation groups are 6-, 12- and 24-hour accumulations plus unknown-period groups; no one-hour group was found **[D, QA JSON]**.

**Malé (ERA5) against Hulhulé (station), daily [V]:** 1,988 days with both. Pearson 0.358, Spearman 0.487. At the 25.4 mm level: station 48 days, ERA5 93 days, both 14. On 17 days the station shows >= 25.4 mm while ERA5 is < 10 mm. The two series are far from interchangeable, and neither is a gauge on Malé island proper.

**Station day appears shifted against reported flood days [V pattern, A cause].**
- 12 Jan 2024: station 0.0 mm on the 12th, 15.5 mm on the 13th.
- 20 Dec 2024: 0.0 on the 20th, 93.0 on the 21st; the report states 136.5 mm for 8am Fri to 8am Sat.
- 11 Mar 2025: 0.0 on the 11th, 65.8 on the 12th.
- Cause is probably end-of-window or UTC dating of 24 h accumulations. Not proven.
- **31 Dec 2023:** reports say Hulhulé 179.9 mm in 24 h, yet the station column shows 3.3 (30th), 4.3 (31st) and 18.8 (1 Jan). Unresolved; the report may be wrong or the GSOD record incomplete.

**Cleaning already done (documented in files):** `99.99` to blank; inches to mm; `time_local` produced by the compiler; derived NOAA accumulation tables (period `99` and depth `9999` to blank, tenths to mm). **My recommendations, not done:** define the UTC offset for each series; align windows; keep ERA5 and station as separate predictors; do not impute station gaps.

## 3. Flood labels

**Are there flood observations?** There are **news-derived reports of flooding on 22 calendar days in 18 incidents** (11 Dec 2021 to 21 Oct 2026) **[V]**. They come from a secondary, AI-assisted compilation; the linked articles have not been opened for all records (project issue A1). They are not systematic observations.

- **Independent events:** 18 incidents. Two (10 and 12 Jan 2024) are two days apart and may be one wet spell, so the defensible range is 17 to 18. Four are two-day events labelled on both days, which is why the features file has 22 flag days.
- **Dates:** day-level only. **No onset or end times in the structured files.** The incident text carries a few phrases (for example rain "from about 11:00" on 13 Aug 2024, a "late-night storm" on 1 Apr 2023); these are not machine-usable.
- **Locations:** many incidents name no streets (for example 21 Jul 2023, 13 Aug 2024, 11 Jan 2025). Roads, landmarks and areas are in the 32-row places file, positive-only. The roads are mostly main arterials.
- **Severity:** only anecdotal (homes flooded, pumps used, "tonnes pumped"). **No flood depth or extent** anywhere **[V: searched the incident text for depth and cm/metre terms and found none]**.
- **Rain versus coastal:** the incident text has **no** mention of waves, overtopping, high tide or sea level **[V by keyword search]**, and the compilation labels all as rain-floods **[D]**. Rain and coastal flooding cannot be separated from these files independently; mechanism is asserted, not observed. The Council's 2025 VLR (outside these files) is reported to mention separate wave overtopping.
- **Non-flood periods:** **not observed.** `flood_reported = 0` means "no report found" for 2,487 of 2,509 days. The compilation is positive-only.
- **Sea level at flood days [V, modelled]:** the daily-maximum modelled sea level on flood days is not unusually high: only 3 of 20 flood days are at or above the 90th percentile (0.94 m), and the lowest is the 9th percentile. This does not prove sea level is irrelevant (daily max, modelled, no onset time).

**Do the labels support hourly or daily prediction?** Hourly: **no** (no times). Daily: only a weak, city-level, positive-unlabelled signal, with roughly 18 events. Not enough for a validated classifier or false-alarm estimates.

## 4. Dataset alignment

| Window | Dates | Independent flood events |
| --- | --- | --- |
| ERA5 rainfall (hourly) with all labels | 2020-01-01 to 2026-11-13 | 18 (22 flag days; 2,509 days) |
| ERA5 with modelled sea level | 2022-11-23 to 2026-11-13 (1,452 days; 437 hourly sea-level gaps) | 16 (20 flag days) |
| Hulhulé station daily rainfall with labels | 2020-01-01 to 2025-08-24 | 13 |
| Station and modelled sea level and labels | 2022-11-23 to 2025-08-24 | 11 |
| Observed sea level (UHSLC 2024) with labels | 2024 only | 4 (10 Jan, 12 Jan, 13 Aug, 20 Dec) |

- **Join resolution:** a reliable join exists only at **daily** resolution, because the labels are daily. The ERA5 and modelled sea-level series share an hourly grid (same `time_local` convention, but the convention is undefined).
- **Usable sample:** about 1,452 to 2,509 days, but only 16 to 18 positive events; 1,452 days is not 1,452 independent examples. Rainy days are strongly autocorrelated.
- **Issues:** the offset question above; station on Hulhulé; the one-day shift of station totals; reporting delay (news appears after the event, so a flood on a day can be dated to the report day); the labels are city-level while rainfall is a single point.
- **Available before a prediction:** at issue time you could use the preceding rainfall, sea level, pressure and wind, and an NWP rainfall forecast. ERA5 is a retrospective reanalysis and the 2026 forecast file is a single snapshot; no historical forecast archive is included, so a true forecast study cannot be built from these files.
- **Leakage risks:** the features file's `rain_mm_reanalysis`, `max_1h_rain_mm` and `max_3h_rain_mm` describe the **same day as the label**, so they are only valid for a same-day classification, not a forecast; `rain_prev3d_mm` and `rain_prev7d_mm` should be checked for whether they exclude the current day **[U]**; `sea_level_max_m` is the same-day maximum; `incident_id` and any column derived from the label must be dropped; the 40 to 45 mm "Malé floods" statement is an unsourced quote and must not be used to define a label or a feature threshold.

## 5. Current project progress

**Collected and verified [V]:** the files above, with the corrections recorded in `data_review.md` and `data_issues.md`.

**Work done, supported by files:**
- Road-flood inventory (positive-only, scope-labelled): `derived/road_flood_inventory.csv`, built by `scripts/build_road_flood_inventory.py`.
- Matching to OSM roads and the evidence map: `derived/road_match_review.csv`, `derived/road_flood_matched_segments.geojson`, `derived/road_flood_evidence_map.png` (`scripts/match_road_flood_records.py`).
- Landmark position check: `derived/landmark_position_check.csv` (`scripts/check_landmark_positions.py`) and `verification/landmark_checks.csv`.
- Unnamed OSM segment review: `derived/unnamed_segment_review.csv` (`scripts/review_unnamed_segments.py`).
- Incident rainfall table: `derived/incident_rainfall_table.csv/.md` (`scripts/build_incident_rainfall_table.py`).
- Drafted agency requests: `requests/agency_data_requests.md`; open-data research: `reports/Malé road flood open data.md`.
- Sprint board: `sprint.md`, `sprint_board.html`. At last merge, MF-10, MF-12, MF-17 and MF-44 were in Review (MF-14, MF-15, MF-18 also; MF-16 in progress).

**Not done:** no trained model, no feature engineering for roads (MF-22 waits on MF-20 segmentation), no spatial blocks (MF-26), no evaluation. The six-page literature review has not been started in this folder.

**Missing essential data:**
1. Observed flooded, dry and unknown locations across independent events, with time, mechanism, verification and observation coverage (Council/NDMA).
2. Hourly or sub-hourly rainfall from a Malé gauge, with station metadata and QC (MMS).
3. Event onset and end times and any depth or extent measure.

**Optional data that would help:** surveyed elevation or spot heights (the Council reportedly has no detailed road elevation); drainage, inlet and pump records (the Council reportedly has no maintenance logs; the stormwater design consultant or the project custodian may hold design drawings); IMERG Final rainfall (30 min, 0.1 degree) as a gridded sub-daily substitute; a longer observed tide record than UHSLC 2024.

**Three most useful next actions:**
1. Send the approved requests (MF-23) and ask Council/NDMA specifically for dated, located incident records with a flooded/dry/unknown field, and MMS for Malé hourly rainfall.
2. Settle timezone and day alignment: confirm the `time_local` offset and the accumulation window for ERA5 and GSOD, then re-date the incident days.
3. Finish segmentation and attributes (MF-20, MF-22) so a descriptive road comparison of reported against unknown segments (MF-30) can start.

## 6. Feasibility (from the inspected data only)

| Target | Feasible? | Why |
| --- | --- | --- |
| Citywide hourly flood-risk prediction | **No** | No flood times; no hourly labels; no sub-hourly gauge. |
| Citywide daily flood-risk prediction | **Not as a validated model; descriptive only** | About 18 positive events, no observed negatives, city-level labels, a one-day offset risk. A model would mostly learn rainfall seasonality and reporting patterns. |
| Street-level flood prediction | **No** | Positive-only, arterial-biased locations; no elevation or drainage; FABDEM at 30 m with an implausible median of 5.04 m. |
| Heavy-rainfall prediction (fallback) | **Yes, as a supporting weather task** | 2,509 daily rows and 60,216 hourly rows give plenty of rain data. It does not demonstrate flood prediction. |

**Recommended research question.** Keep the project question as recorded: "Which Malé roads or road sections are repeatedly reported as flooded, and which terrain and road attributes are associated with those reports?" A descriptive, positive-unlabelled-in-spirit susceptibility ranking. If the course needs a prediction element, add as supporting analysis: "Do daily rainfall and antecedent-rain features separate days with a reported flood from days with none, among days with comparable rain?"

**Target, horizon and baseline for that supporting task.**
- Target: a city-level reported-flood day (binary), noting "no report" is not "dry".
- Horizon: **same-day (nowcast-style) classification, not a forecast**, using only the rainfall of the preceding window. A next-day forecast needs archived forecast data that are not here.
- Baselines: always-negative and climatology; a single-feature rule (daily rain above a threshold chosen inside training folds); Hulhulé station rain as a separate comparator.
- Candidate models: L1/L2 logistic regression on a handful of features (daily, 3-day and 7-day rain; max 1 h; sea-level maximum), then a shallow gradient-boosted tree or random forest. Avoid deep models: 18 events cannot support them.
- Evaluation: leave-one-event-out or blocked-by-season cross-validation, grouped by storm; report precision and recall with confidence intervals, and state that false-alarm rates are not estimable without observed dry days.

**Limitations to state.** Positive-only, secondary news evidence; point-based rainfall from a different island or a model; undefined time convention; modelled sea level; FABDEM not validated; no drainage or elevation survey; an unsourced "40 to 45 mm" threshold.

## 7. Not inspected or not verified

- **Rasters** (`Male_FABDEM_30m_masked.tif`, `N04E073_FABDEM_V1-2.tif`, WorldCover, WorldPop, CHIRPS): `rasterio` is not installed here, so I read only their QA/metadata JSON, not the pixels. FABDEM statistics come from `FABDEM_Male_QA.json`.
- **PDFs and images** (`Male_Flood_Data_Research.pdf`, `Flood_AI_Project_Plan.pdf`, `Male_Data_Coverage.png`, the assignment brief PDF): not read.
- **`flood_map.html`:** read as text only; not rendered.
- **How each file was downloaded** (exact API calls for the ERA5, sea-level and MET Norway files): not recorded in the folder.
- **Source articles:** the news links behind the incidents were not opened by me.
- **Planning and writing files** named in CLAUDE.md (`Project_Plan.md`, `latex/`, reading matrix, the 22 screened references) are not in the folder.
- **Council statement** about maintenance logs and elevation data: supplied by you, not in any file.
- **Whether `rain_prev3d_mm` and `rain_prev7d_mm` exclude the current day,** and the ERA5 hourly accumulation convention: not verified.

## PROGRESS HANDOVER (paste into another chat)

**Project:** Advanced AI module, Malé island proper only (not Hulhumalé or Vilimalé), rainwater flooding. Deadline 29 May 2027 (submit by; lecturer-confirmed deadline 30 May 2027 00:00 UTC+5). Deliverable: six-page IJCAI-format literature review (15+ journal articles) plus the project. Recorded research question: which Malé roads or sections are prone to flooding (susceptibility mapping, not forecasting). Date of this summary: 17 Nov 2026. Files are in `male-flood-basis/data/` and `Male_Flood_Data_Starter_Pack/`.

**Verified data (exact files and coverage):**
- `male_reanalysis_hourly_2020-2026.csv`: ERA5 via Open-Meteo, Malé grid point, hourly, 60,216 rows, 2020-01-01T00:00 to 2026-11-13T23:00, no gaps or missing values, max 32.6 mm/h. Daily version `male_reanalysis_daily_2020-2026.csv` (2,509 days). Time column `time_local`; offset not documented (tide correlation consistent with UTC+4 or +5).
- `male_sea_level_waves_hourly_2022-2026.csv`: **modelled** sea level (valid 2022-11-23T05:00 onward, 437 hourly gaps after that), wave and swell height from 2022-01-01.
- `hulhule_station_daily_2020-2025.csv`: NOAA GSOD, Velana airport on Hulhulé (not Malé), 2,049 days to 2025-08-24, 14 dates absent, 57 blank rainfall values (not zero-filled), 4 days above 100 mm. Station and ERA5 daily rainfall correlate weakly (Pearson 0.36, Spearman 0.49, 1,988 days).
- `Male_Flood_Data_Starter_Pack/tides/UHSLC_Male_Record1082_Hourly_2024.csv`: observed hourly sea level, UTC, mm relative to station zero, 2024 only (8,659 valid of 8,784).
- NOAA hourly reports 2024 and Jan to 24 Aug 2025 (6/12/24-hour accumulations only; no 1-hour rainfall), NASA POWER (1-5 Jan 2025 only), CHIRPS (one day).
- Spatial: OneMap island polygon, 571 OSM roads, 51 land-use polygons, building layers from OSM (933), Microsoft (4,677) and Google (10,077; 5,773 at confidence >= 0.75), WorldCover 2021, WorldPop 2025 (modelled), FABDEM 30 m (not validated; median 5.04 m looks too high for Malé). Rasters were not opened; only their QA JSON was read.

**Flood labels:** `flood_incidents_greater_male_2021-2026.csv` has 18 news-derived incidents (11 Dec 2021 to 21 Oct 2026; 22 flag days; 17 to 18 independent storms). Date-level only; no onset or end times; no depth or extent; many incidents name no streets; positive-only (no observed dry days); `flood_reported = 0` means "no report found". The incident text contains no coastal or wave wording, so rain versus coastal flooding is asserted, not separated. Compiled secondarily by AI; the source articles were not all checked. Five incidents have a reported Malé rainfall figure; periods are unknown for two. Only 3 of 20 flood days (with sea-level data) had modelled sea level at or above its 90th percentile.

**Alignment:** daily is the only reliable join. 18 events with ERA5; 16 with modelled sea level (from 2022-11-23); 13 with Hulhulé station rain (to 2025-08-24); 11 with all three; 4 with observed sea level (2024). Station daily totals appear dated a day after some reported flood days (12 Jan 2024, 20 Dec 2024, 11 Mar 2025); 31 Dec 2023 reports 179.9 mm at Hulhulé but the station file shows 4.3 mm. Same-day rain features are leakage for any forecast.

**Reported by the user (not in a file):** Malé City Council says maintenance logs and detailed road elevation data are unavailable.

**Work done:** road-flood inventory and OSM matching (`derived/road_flood_inventory.csv`, `road_match_review.csv`, `road_flood_matched_segments.geojson`, `road_flood_evidence_map.png`), landmark and unnamed-segment checks, incident rainfall table (`derived/incident_rainfall_table.csv/.md`), drafted agency requests (`requests/agency_data_requests.md`), open-data research (`reports/Malé road flood open data.md`), `data_review.md`, `data_issues.md`, sprint board (`sprint.md`). **No trained model, no road features or evaluation yet; literature review not started in this folder.**

**Feasibility:** citywide hourly prediction: no. Citywide daily validated prediction: no (about 18 positives, no negatives). Street-level prediction: no. Heavy-rain classification: yes, as a supporting weather task only. Descriptive road susceptibility (reported versus unknown segments): yes.

**Recommended design:** primary = descriptive road susceptibility ranking, with unreported roads called "unknown". Optional supporting task: same-day classification of reported-flood days from rainfall and antecedent rain (not a forecast), baselines = always-negative, climatology and a training-fold rainfall threshold, models = regularised logistic regression then a shallow gradient-boosted tree or random forest, leave-one-event-out validation, and no false-alarm claims.

**Blockers:** no observed flooded/dry/unknown locations; no Malé gauge rainfall; undefined `time_local` offset and accumulation window; no depths or times; elevation and drainage unavailable; agency requests (MF-23) not yet sent; segmentation (MF-20) pending for MF-22 and MF-26.

**Next steps:** (1) send the approved requests to Council/NDMA and MMS; (2) fix the timezone and day alignment for all series; (3) finish segmentation and attributes, then compare reported and unknown segments.
