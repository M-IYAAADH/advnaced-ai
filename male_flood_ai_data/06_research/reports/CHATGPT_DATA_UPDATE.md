# Handover: Malé flood AI data, v002 verification (22 Nov 2026)

This handover stands on its own and supersedes v001, which is kept at `06_research/reports/archive/CHATGPT_DATA_UPDATE_v001_20261122.md`.

The full detail is in two reports:
- `SOURCE_VERIFICATION_REPORT.md`
- `TIME_ALIGNMENT_REPORT.md`

## What this pass did

**Sources.** All 71 registered sources were read: 59 directly, 7 through an alternative Sun host and 5 through the Internet Archive. Seven official documents were saved: the NDMA 2024 annual report, the MMS Severe Weather Report 2024, the JICA 2022 survey, the Council VLR 2025, and three government web pages. News articles keep their URL, metadata and a short excerpt. Dhivehi excerpts are given in the original with an AI-made English translation.

**Reviewed tables.** Every original record was turned into reviewed events, source links, storm groups and a crosswalk. The originals are 30 imported records, 18 compiled incidents, 18 legacy decisions, 3 starter leads, 29 Groundsource windows and 17 legacy storm proxies, plus 7 new official mentions found during the checks.

**Weather clocks.** The clocks were audited using ISD synoptic groups, NOAA documentation, the pressure tide and tidal harmonics. NOAA GSOD and ISD files for 2020–2023 were added: these are public data, saved as unchanged bytes.

**Outstanding files.** Three files were classified. `bobs flood.xlsx` was inspected and imported unchanged, but it is excluded from the ZIP (see below).

**Preserved.** The v001 tables are archived in `03_reviewed/_archive_v001_20261122/`. Legacy storm proxies and the 9 v001 time-alignment rows remain inside the new files and are marked superseded. No raw file was modified, no model was retrained, and nothing was pushed to GitHub.

"Accepted" means the report was found and its interpretation checked. It is not measured extent, depth or ground truth. All labels are positive-only.

## Conflicts resolved, with the evidence used

1. **OFF003 (18 Sep 2024): separate incidents.** The NDMA register lists case #193 as "Rain water flooding" at H. Dhoohimerige and case #194 as "Fire Incidents" at G. Sindhu Hiya, both on that date. The assistance-table row for 18 Sep is the fire, matching #194. #193 is accepted as a property-level rainwater record. The same property had a fire on 9 Sep, which is noted as context.
2. **RAIN018 versus 25 Nov 2025: both dates stand.** Adhadhu (25 Nov, MVT) reports flooding in Maafannu from early on Tuesday morning. Edition (26 Nov, 16:04 local) and Sun (27 Nov, 00:44) report rain from after 13:00 on Wednesday flooding the streets. RAIN018's "correction" wording is not supported. Both histories are kept, and the two days form a provisional storm group.
3. **RAIN004 (1 Apr 2023): accepted.** MFR is dated 1 April, so its "last night" is the night ending that morning. Atoll Times says Saturday morning. The Hulhulé SYNOP shows 49.0 mm between 05:00 and 11:00 local on 1 Apr. The earlier "0.0 mm" came from reading GSOD on the wrong day. The articles' time-of-day disagreement is still recorded.
4. **RAIN007 (31 Dec 2023): traced.** The MET figure is 179.7 mm at Hulhulé, 08:00 Sunday to 08:00 Monday, as quoted by Atoll Times and the Council VLR. The 179.9 mm figure appears only in MVRepublic. The SYNOP 12-hour group for 05:00–17:00 local on 31 Dec is 184.0 mm. The "4.3 mm" in v001 was GSOD 31 Dec, which covers the 24 hours before the storm. The storm's own GSOD value (1 Jan, 18.8 mm) is one-tenth of the 12-hour total.
5. **RAIN010 (13 Apr 2024): date settled.** Two articles and NDMA case #52 all give Saturday 13 Apr. The 00:00 report on 14 Apr is persistence, not a second flood day.
6. **RAIN014 (10–11 Jan 2025): kept as an overnight window.** Flooding is reported from Friday evening in one source and overnight or early Saturday in the others. MMS reports 130.7 mm for 08:00 10 Jan to 08:00 11 Jan.
7. **Legacy "uncertain" dates now accepted, after reading the sources:**
   - 11 Dec 2021
   - 1 Apr 2023
   - 12 Jan 2024
   - 20–21 Dec 2024 (as a window)
   - 11 Mar 2025
   - 16 Apr 2026
   - 4 May 2026

## Conflicts still unresolved

- **Intraday timing.** For each event below, the articles disagree on the time of day. Station data from Hulhulé cannot settle wording about Malé.

  | Event | Date | Competing accounts |
  |---|---|---|
  | EVT0005 | 1 Apr 2023 | late night vs morning |
  | EVT0018 | 13 Apr 2024 | morning vs afternoon |
  | EVT0028 | 3 Jan 2025 | rain starting Thursday evening, Friday morning or Friday afternoon |
  | EVT0029 | 10–11 Jan 2025 | Friday evening vs early Saturday |

- **Which day:** 20–21 Dec 2024 and 10–11 Jan 2025 remain overnight windows.
- **Mechanism:**
  - 18 May 2020 (RAIN001): rain flooding and swell reported together.
  - 17 Dec 2024 (OFF005): only dewatering is documented; the cause is not stated.
- **Uncertain dates:**
  - 30 Dec 2023: rain is reported, but no flooding is dated to that day.
  - 13 Jan 2024: appears only in the NDMA register.
  - 14 Aug 2024: appears only in an MMS photo caption.
  - Mid-November 2024: undated MMS statement; the window is approximate.
- **Uncertain location:** 6 Aug 2023 coastal. Swells reached "the capital", but Malé island flooding is not stated.
- **Station names:** Hulhulé and Hulhumalé are swapped between Sun and MMS for 12 Jan and 20 Dec 2024.
- **Rainfall windows:** 89.4 mm on 13 Aug 2024 is given as 24 h in one source and 48 h in another.
- **Unexplained:** MMS reports Malé floods with 40.4 mm at the Malé AWS on 25 May 2024, while the Hulhulé SYNOP shows 0 mm.
- **Single-source events:** 13 accepted events rest on one source, including 6 single-line official records.

## Accepted reported-event counts (2020–2026)

| Measure | Count |
|---|---:|
| Accepted rain events | **30** |
| …single primary day | 27 (5 note persistence past midnight) |
| …both days explicitly reported | 1 (11–12 Dec 2021) |
| …overnight windows | 2 |
| Distinct calendar days with an accepted single-day or both-days rain report | **29** |
| Accepted rain events that are property-level official records | 3 |
| Accepted coastal events | **4** (5 Nov 2022, 31 Jul 2023, 5 Aug 2023, 26 Jul 2026) |
| Mixed or uncertain cause | 2 |
| Uncertain date | 4 |
| Uncertain location | 1 |
| Groundsource-only windows excluded (not evidence of no flood) | 13 |
| Storm groups (2020+): rain | 29 (6 established, 22 provisional, 1 unresolved) |
| Storm groups (2020+): coastal | 4 (1 established, 2 provisional, 1 unresolved) |
| Storm groups (2020+): mixed | 1 |
| Storm groups (2020+): unresolved type | 1 |
| Proposed validation blocks (≤ 7-day merge; not storm identities) | 28 rain, 3 coastal |
| Verified storm groups / accepted labels in v001 | 0 / 0 |

The 2-day merge rule was replaced: groups now rest on what the sources say. For example, 10, 12 and 13 Jan 2024 are one warned synoptic system but separate flood bursts, so they are provisional. Separately, 3 Jan 2025 and 10–11 Jan 2025 are explicitly "the second instance … within a week", so they are separate groups. Those two groups share a validation block.

## Weather alignment and availability

**ERA5 (Open-Meteo).** The `time_local` labels behave as **UTC+5**. ERA5's pressure tide peaks at label hour 9.86. Observed Hulhulé pressure, timestamped in UTC, peaks at 04.83 UTC, which implies an offset of +5.05 h. This is established by observation, not by documentation. The accumulation convention is the documented interval-ending one, with interval-starting kept as an alternative. Coverage: 2020-01-01 to 2026-11-13, all 30 accepted rain events.

**GSOD.** A flag-G value for date D is the 24-hour SYNOP group ending at 00 UTC on D. That covers **05:00 local D−1 to 05:00 local D**. This was established on 1,700 of 1,701 days, so local day L should use GSOD L+1.

**Defect in the SYNOP 24-hour group.** On 178 days between 2020 and 1 Feb 2024, the group is about one-tenth of the 12-hour sums; 118 of those days are flagged suspect. That affects 72 of 113 heavy-rain days. GSOD inherits the defect. Use the SYNOP 6/12-hour blocks instead, which are now built for 2020 to 24 Aug 2025 (Hulhulé, not Malé). No hourly rainfall exists.

**Coverage of the 30 accepted rain events:**

| Series | Events covered |
|---|---:|
| ERA5 | 30 |
| Complete SYNOP local day | 13 |
| GSOD, shifted alignment | 21 (14 after excluding one-tenth days) |
| Modelled sea level | 28 |
| UHSLC tide gauge (2024 only) | 10 |

**Modelled sea level.** The clock is unresolved: UTC+4 or UTC+5 (M2 phase +4.41 h; correlation 0.963 vs 0.959). It uses a model datum, so compare anomalies only. UHSLC is in UTC, millimetres relative to station zero.

**Publication clocks.**
- Established as UTC+5: Ras, Edition, Plus, Standard, Mihaaru, PSM, Adhadhu.
- UTC: MVRepublic.
- Not established: Sun, Atoll Times and others.

**MMS totals** run 08:00–08:00 local. The MMS report labels them by the start day; news articles label them by the end day.

## Can retrospective modelling proceed?

**Partly, as a descriptive experiment on reported events.** No model was trained in this pass.

What is ready:
- 30 accepted rain events (29 single or both-days dates, plus 2 windows), positive-only.
- ERA5 on a now-established clock.
- Station blocks with known windows for about 13–21 of the events.
- Event-level groups and proposed blocks for evaluation.

What it can support:
- Agreement and ranking studies: for example, how ERA5 or station rain on reported days compares with all other days.
- Reports, explicitly labelled as such.

What it cannot support:
- False-alarm rates or specificity. There are no observed non-flood days, so every day without a report is unlabelled.
- Clean binary classification. The windows, the property-level records and the 13 single-source events need a declared policy first (for example, a sensitivity analysis with and without them).

Road susceptibility, the recorded project question, still rests on positive-only, landmark-heavy evidence. These events add place names (see `location_as_reported`) but no observed dry roads.

## What specifically remains missing for advance prediction

1. **Labels with denominators.** Council or NDMA records of flooded, dry and not-observed outcomes, with observation coverage, so that non-flood days can be labelled.
2. **Local rainfall at issue time.** MMS gauge data from Malé AWS and Hulhulé, hourly or finer, with QC flags and data-availability (latency) timestamps. SYNOP ends 24 Aug 2025 in public files and has no hourly rain.
3. **A forecast archive.** Historical NWP or MMS forecasts as issued (for example GFS/ECMWF archives, or MMS WRF runs). One MET Norway snapshot is not an archive.
4. **ERA5 provenance.** Saved Open-Meteo requests, with explicit `timezone`, plus documented release latency. Without those, ERA5 is retrospective only.
5. **Observed sea level after 2024.** UHSLC for 2022–2026, or MMS tide data. Also documentation of the marine model's timezone and datum.
6. **Event clocks.** Flood-onset times from agency logs (MNDF pumping logs, NDMA call times), rather than article wording.
7. **Problem definition.** A fixed issue time and lead time, chronological and storm-blocked evaluation, and persistence and climatology baselines, all before any model is fitted.

## Files

**New or updated:**
- `00_catalog/source_verification.csv`
- `00_catalog/source_fetch_log_20261122.csv`
- `00_catalog/schema_extensions_v002.csv`
- `00_catalog/source_register.csv` (with access times and local paths)
- `00_catalog/dataset_inventory.csv` (DS0064–DS0091; DS0048, DS0049 and DS0055 reclassified)
- `03_reviewed/events/{flood_events, event_source_links, record_crosswalk, review_counts_v002}.csv`
- `03_reviewed/storm_groups/{storm_groups, validation_blocks_proposed_v002}.csv`
- `03_reviewed/time_alignment/time_alignment_decisions.csv` and `evidence/*_v002.csv`
- `02_interim/weather_aligned/{noaa_synop_precip_groups_2020-2025, noaa_synop_6h_blocks_2020-2025, daily_series_coverage_2020-2026}_v002.csv`
- `01_raw/flood_evidence/official_records/` (7 files)
- `01_raw/rainfall/station/noaa_velana_435550_99999/` (2020–2023 GSOD and ISD; `provider_docs/`)

**Scripts:** `00_catalog/tools/{audit_weather_clocks, build_reviewed_events, event_weather_windows}_v002.py`.

**Not in the ZIP:** `01_raw/flood_evidence/compiled_secondary/bobs_flood_workbook/bobs flood.xlsx`. It is a monthly table of houses affected, drains cleared, roads repaired and rainfall, from Jan 2023 to Jul 2026. Its geography is implied as Malé City. It may be internal Council data, so permission is needed before it is shared. It holds context only; it cannot verify events.

**Review status:** the reviewer was AI-assisted. A human reviewer should check the decisions and the Dhivehi translations.
