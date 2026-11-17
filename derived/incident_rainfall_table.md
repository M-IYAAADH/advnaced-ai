# Rainfall for the 18 reported incidents (MF-44)

Descriptive only. Built by `scripts/build_incident_rainfall_table.py`; full table in `derived/incident_rainfall_table.csv`.
Nothing here is a flood threshold, a trigger level or a validated rainfall-response result.

## What each column is

| Column group | Meaning | Limits |
| --- | --- | --- |
| Reported (`reported_rainfall_verbatim`, `reported_male_mm`, `reported_period`) | Figures as written in the news-derived compilation, with the period only where the text states one. | Secondary, unchecked sources (A1). Only 5 of 18 incidents have a Malé figure; the other 13 have none in the compilation, which is not the same as no rain. |
| ERA5 (`era5_*`) | Reanalysis daily total and highest hourly value for the covered local date. | Modelled, not a gauge; the compilation says it underestimates peaks. Day boundary (UTC vs UTC+5) not verified. |
| Hulhulé GSOD (`hulhule_gsod_*`) | NOAA daily precipitation at the airport station on Hulhulé, converted to mm, with the flag as supplied. | Not Malé island. Series ends 24 Aug 2025, so 5 incidents have no row. GSOD days are UTC days, so a late-evening event can land on the next day. Totals may be incomplete. |

## Reported figures against the other two series

| Incident | Reported Malé (period) | ERA5 daily mm | Hulhulé GSOD mm |
| --- | --- | --- | --- |
| 30–31 Dec 2023 | 118.2 mm (period unknown for Malé; Hulhulé 179.9 mm in 24 h) | 25.0 (30th), 113.5 (31st) | 3.3 (30th), 4.3 (31st) |
| 13 Aug 2024 | 89.4 mm (8am to 8am, dates not stated; Hulhulé 63.4) | 67.1 | 51.3 |
| 20–21 Dec 2024 | 136.5 mm (8am Fri to 8am Sat, 24 h) | 25.1 (20th), 37.6 (21st) | 0.0 (20th), 93.0 (21st) |
| 2–3 Jan 2025 | 142.2 mm (period unknown; another count 162 mm by 11pm) | 66.3 (2nd), 56.2 (3rd) | 47.0 (2nd), 71.6 (3rd) |
| 21 Oct 2026 | 90 mm in 24 h | 35.0 | no station row |

## Contradictions kept, not resolved

- **30–31 Dec 2023:** Hulhulé is reported at 179.9 mm (a record), yet the GSOD station column shows 3.3 and 4.3 mm for the two days. These cannot both describe the same gauge and period. The GSOD precipitation group is likely incomplete or mis-assigned; the report is unverified. Treat both as unreliable until MMS data arrives.
- **20–21 Dec 2024:** the reported 24 h figure is 136.5 mm, GSOD puts 93.0 mm on 21 Dec and 0.0 on 20 Dec, and ERA5 is 25.1 and 37.6. The reported window (8am to 8am local) does not match either UTC day.
- **2–3 Jan 2025:** reports say 142.2 mm and 162 mm by 11pm; the single event is split over two series days.
- **ERA5 against reports:** ERA5 is lower than the reported figure on every event with one, which is consistent with its known low bias but has not been quantified here.
- **Days with no reported figure:** several have large series values (for example 12 Jan 2024: ERA5 58.2 mm, GSOD 0.0 mm; 12 Mar 2025: ERA5 98.1 mm, GSOD 65.8 mm). Others are small (1 Apr 2023: ERA5 0.9 mm for a "late-night storm", probably spilling into the next day). The series disagree with each other often, so none is a reference.

## What this table cannot support

- No minimum rainfall for flooding. A flood after X mm is an association. The "40 to 45 mm" quote on the flood map has no linked source (A2).
- No comparison with non-flood days: the compilation is positive-only, and "no report found" is not dry (`flood_reported = 0`).
- No hourly intensity. Reported figures are daily or 24 h; ERA5 hourly maxima are modelled.
- Needed: MMS hourly gauge data and station metadata for Malé (agency request, MF-23).
