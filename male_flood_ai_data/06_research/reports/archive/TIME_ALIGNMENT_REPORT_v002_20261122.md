# Time alignment report (v002)

Prepared 22 November 2026. This report audits the clocks and measurement windows of every weather and sea-level series.

All raw series are left unchanged. Each alignment is recorded as a named decision or hypothesis in `03_reviewed/time_alignment/time_alignment_decisions.csv`: TA002-01 to TA002-10, with the nine v001 rows kept as TA001-xx. The evidence tables are in `03_reviewed/time_alignment/evidence/`, and the scripts are in `00_catalog/tools/`.

No alignment was chosen because it improves agreement with flood reports. Each one was fixed from station records or provider documentation before the event comparison was run.

## 1. Summary

| Series | Clock | Measurement window | Status |
|---|---|---|---|
| ERA5 via Open-Meteo, hourly and daily (DS0051–52) | `time_local` = **UTC+5** | Documented: hour *h* is the sum over (*h*−1, *h*]. Daily total = labels 00–23 | Clock established by observation. The accumulation convention is documented by the provider but not verified for this file. The original request is still unsaved. |
| NOAA GSOD PRCP, Hulhulé (DS0019–20, DS0048, DS0064–67) | GSOD date = UTC day | Flag G = the 24 h SYNOP group reported at **00 UTC on that date**, i.e. **05:00 local D−1 to 05:00 local D** | Established by observation (1,700 of 1,701 days) and the NOAA readme |
| NOAA SYNOP AA groups (ISD, DS0017–18, DS0068–71) | UTC | 6 h groups ending 06 and 18 UTC; 12 h ending 00 and 12 UTC; 24 h ending 00 UTC | Verified. The 6 h blocks derived from them are provisional. |
| SYNOP 24 h group magnitude | — | — | **Defect:** on 178 days the value is about one-tenth of the 12 h sums (2020 to 1 Feb 2024) |
| Open-Meteo Marine sea level (DS0053) | Labels are +4.0 to +4.7 h relative to UTC | Instantaneous | **Unresolved:** UTC+4 or UTC+5 |
| UHSLC Malé gauge 2024 (DS0023, DS0057) | UTC | Instantaneous hourly; mm relative to station zero | Verified |
| MMS totals quoted in news and reports | Local | 08:00–08:00 | Documented in the sources. The label convention differs by source. |
| NASA POWER; MET Norway | UTC | As documented | Verified; not used |

## 2. ERA5 (Open-Meteo): labels behave as UTC+5

The Open-Meteo request was not saved, and a column named `time_local` does not prove its timezone. Two independent tests were run instead.

### Semidiurnal pressure tide

The mean daily anomaly of `pressure_msl` has a 12-hour harmonic (1.45 hPa) that peaks at **label hour 9.86**. The same calculation on observed Hulhulé sea-level pressure from ISD, which is timestamped in UTC, gives a peak at **04.83 UTC** (2020 to Aug 2025).

The implied offset is **label = UTC + 5.05 h**. If the labels were UTC, ERA5's peak would sit near 04:50 local time. That contradicts the observed station.

### Rain timing against the station's 6-hour blocks

The test compared log totals over 6,248 blocks:

| Hypothesis | r |
|---|---:|
| UTC labels | 0.465 |
| UTC+5, interval-starting | 0.524 |
| UTC+4, interval-ending | 0.524 |
| UTC+5, interval-ending | 0.515 |

This rejects UTC labels. It cannot separate the accumulation convention from a one-hour offset, so the provider's documented convention (interval-ending) is kept as **H_END**, and **H_START** is kept as the alternative.

### Consequences

- Read ERA5 labels as Asia/Male time.
- The daily file sums labels 00–23. Under H_END that covers (D−1 23:00, D 23:00] local. The one-hour ambiguity barely affects daily totals.
- What is still missing is the documentation itself. Re-request the data with explicit `timezone=GMT` and `timezone=Asia/Male`, and save both requests and responses.

## 3. GSOD and the SYNOP groups behind it

### GSOD's date convention (TA002-02)

For flag **G** ("1 report of 24-hour precipitation amount", NOAA GSOD readme), GSOD PRCP for date D equals the SYNOP 24-hour group reported at 00 UTC on D. This held on 1,700 of 1,701 flag-G days with that group, to within 0.3 mm, over 2020–2025.

So **GSOD D covers 05:00 local D−1 to 05:00 local D**, and local day L corresponds to GSOD L+1. The NOAA readme says PRCP "will usually not end with the midnight observation". The earlier "one-day offset" is therefore no longer a hypothesis for flag-G days.

Days with other flags were not resolved individually: E 80, F 46, A 7, B 8, H 10, I 82, and blank 57.

### A magnitude defect in the 24-hour group (TA002-03)

The 24-hour group was compared with the sum of the two 12-hour groups covering the same 24 hours:

| Comparison | Days |
|---|---:|
| Both dry | 1,003 |
| Consistent | 256 |
| **24 h about one-tenth of the 12 h sum** | **178** |
| Other inconsistent (mostly small amounts) | 149 |

The one-tenth days run 39–51 per year in 2020–2023, then 4 days in early 2024 (the last on 1 Feb 2024), and none after that. Of those 178 days, 118 carry ISD quality code 2, which the ISD format document defines as "Suspect".

Of the 113 days with a 12-hour sum of at least 25.4 mm, **72 are affected**. GSOD-based heavy-rain counts for 2020–2023 are therefore understated. The v001 count of 47 days at or above 25.4 mm (2024–2025) is barely affected; the 12-hour pairs give 45.

Published MMS totals agree with the 12-hour groups:

| Date | MMS | 12 h groups | 24 h group |
|---|---:|---:|---:|
| 31 Dec 2023 | 179.7 mm | 184 + 5 mm | 18.9 mm |
| 12 Jan 2024 | 159.3 mm (Malé AWS) | 156 mm | 15.6 mm |
| 20 Dec 2024 | 117.4 mm | 117 mm | 92.9 mm |

The cause is unverified; whole-millimetre amounts encoded as tenths is one hypothesis. **No correction was applied.** Use the 6- and 12-hour groups for magnitude, and flag GSOD on the listed days. Evidence: `synop_24h_vs_12h_consistency_v002.csv`.

### Six-hour blocks (TA002-04)

`02_interim/weather_aligned/noaa_synop_6h_blocks_2020-2025_v002.csv` builds non-overlapping blocks from the FM-12 groups:

| UTC block | Local block |
|---|---|
| 00–06 | 05–11 |
| 06–12 | 11–17 |
| 12–18 | 17–23 |
| 18–24 | 23–05 |

Each 6-hour group is used as it stands. The block that only a 12-hour group covers is that group minus the matching 6-hour group.

- 6,592 of 8,768 blocks have a value.
- 1,338 local days are complete.
- 5 negative differences are flagged.
- The 6- and 12-hour amounts are in whole millimetres.
- ISD condition code 3 appears on every non-zero amount, although the documentation describes it as "begin accumulated period". It was not relied on.

No hourly or sub-hourly rainfall exists in these files.

### Effect on the named conflicts

GSOD read "as labelled" put storm totals on the day after the flood. The low-rainfall puzzles on 1 Apr 2023, 31 Dec 2023, 12 Jan 2024, 13 Apr 2024, 20 Dec 2024 and 11 Mar 2025 all come from that misreading, plus the one-tenth defect. Section 3 of `SOURCE_VERIFICATION_REPORT.md` has the event-level detail.

Hulhulé is not Malé island, so station rain cannot settle article wording about time of day.

## 4. Modelled versus observed sea level

### Clock (TA002-05)

Harmonic fits for 2024, comparing the Open-Meteo labels with UHSLC in UTC, put the model labels ahead of UTC by:

| Constituent | Offset |
|---|---:|
| M2 | +4.41 h |
| S2 | +4.68 h |
| N2 | +4.35 h |
| K1 | +4.40 h |
| O1 | +3.98 h |

The lagged correlation is 0.963 at UTC+4 and 0.959 at UTC+5. A model tide phase error of about half an hour is plausible, so the two hypotheses stay open:

- **H_MARINE_UTC+5:** the same compiler produced the ERA5 file, whose clock is UTC+5. The first valid label, 05:00 on 2022-11-23, would fit a product starting at 00 UTC, but that start time is unverified.
- **H_MARINE_UTC+4:** gives the best raw correlation.

UTC labels are rejected.

### Datum (TA002-06)

- UHSLC values are millimetres relative to station zero; the 2024 mean is 2.016 m.
- The modelled `sea_level_height_msl` has a 2024 mean of 0.448 m on its own model datum. That offset from zero is unexplained.
- Absolute levels must not be compared; compare anomalies only.
- Neither series is a flood depth.
- The 0.74 m tide that Edition quoted for 26 Jul 2026 has no stated datum.

## 5. Reported totals and event clocks

**MMS totals (TA002-07).** Totals run 08:00 to 08:00 local; the 4 May 2023 figure covers 12 hours, 20:00 to 08:00. The MMS 2024 report labels a window by its **start** day: for example, it calls 08:00 20 Dec to 08:00 21 Dec "20th December". News articles describe "the last 24 hours" on the **end** day. Every quoted total in `flood_events.csv` keeps its station, window and source.

**Publication clocks (TA002-08).** Partly established; see `SOURCE_VERIFICATION_REPORT.md` section 1.

**Event clocks (TA002-09).** Flood onset, rain start and response start are kept in separate columns, with their qualifiers ("approximately", "after", "evening"). No flood onset was measured for any event. These intraday conflicts stay open:

- EVT0005: late night or morning
- EVT0018: morning or afternoon
- EVT0028: Thursday evening, Friday morning or Friday afternoon
- EVT0029: Friday evening or early Saturday

## 6. Weather coverage under each alignment

Coverage of the 30 accepted rain events in the study period (`coverage_by_alignment_v002.csv`):

| Alignment | Status | Events covered |
|---|---|---:|
| ERA5, labels = UTC+5 | Established | 30 |
| ERA5, labels = UTC | Rejected; sensitivity only | 30 |
| SYNOP 6 h blocks, complete local day (05:00–05:00) | Verified clock | 13 |
| GSOD shifted (local day L ← GSOD L+1) | Established | 21 |
| …of which not on a one-tenth day | Quality filter | 14 |
| GSOD as labelled | Rejected | 21 (wrong window) |
| Modelled sea level (UTC+4 or UTC+5) | Unresolved clock | 28 |
| UHSLC observed | Verified | 10 (2024 only) |

Across all days from 2020-01-01 to 2026-11-13 (`daily_series_coverage_2020-2026_v002.csv`, local days):

| Series | Days |
|---|---:|
| ERA5 complete | 2,509 |
| SYNOP blocks complete | 1,338 |
| GSOD available for the local day (shifted) | 1,991, of which 178 fall on one-tenth days |
| Modelled sea level complete (labels as given) | 1,431 |
| UHSLC complete | 356 |

Of those days, 37 carry an accepted reported event, including windows and coastal events; 10 are uncertain; and **2,462 are unlabelled**. No negative labels were created.

## 7. Historical availability (advance prediction)

- **ERA5.** Typically released with a delay of about five days. This was not checked for this file, and the request was not saved. Treat it as retrospective only.
- **GSOD and ISD.** Published after the day; the station record ends 24 Aug 2025 in the files fetched today, and no 2026 files exist.
- **Forecasts.** None are archived; there is a single MET Norway snapshot.
- **Same-day totals.** Totals from any of these series are not available at a morning issue time.
