# Rainfall research examples for Male, Maldives

Checked 14 November 2026. This folder contains downloaded NOAA station observations, a NASA POWER reanalysis example, a CHIRPS v3 raster subset, derived precipitation-group tables, metadata and QA. No MMS request was sent.

## NOAA: hourly reports do not mean hourly rainfall

Station 435550/99999 is MALE INTL / VELANA INTL (VRMM) on Hulhule, not Male island proper. History coordinates are 4.192 N, 73.529 E. The August 2025 station-history snapshot spans 1981 Jan 1-2025 Aug 24, with possible gaps.

Both tested Global Hourly years (2024 and 2025) contain 6-, 12- and 24-hour AA precipitation accumulations, plus unknown-period groups. No 1-hour AA precipitation group was found. Do not divide these totals to manufacture hourly intensity, or sum overlapping 6/12/24-hour windows. Preserve quality and condition codes, trace markers, missing values and report types until a documented QC policy is implemented.

The derived noaa_precipitation_accumulations CSV files retain every nonempty AA group. Period 99 and depth 9999 become blank; numeric depth is divided by 10 to obtain millimetres. Raw groups and flags remain. These tables are not fully quality-controlled model inputs.

The 2024 GSOD file contains 355 dates and 354 nonmissing PRCP values. PRCP is in inches. Missing dates are not zero. The 2025 example ends on Aug 24.

Old NOAA Global Hourly paths can redirect to HTML with HTTP 200 during cloud migration. The CSV originals here were verified from the official NOAA S3 host; failed HTML responses are excluded.

## NASA POWER: a coarse reanalysis example

The point request at 4.175 N, 73.510 E for 1-5 Jan 2025 returns 120 UTC hours. The source header identifies MERRA2. This is model reanalysis, not local gauge rainfall. The derived CSV explicitly includes UTC and UTC+5 timestamps. The original JSON and request URL are saved.

## CHIRPS v3: one valid Male pixel/date verified

For 3 Jan 2025, the final-sat COG returns 108.274635314941 mm at 4.175 N, 73.510 E. A 3-by-3-cell context GeoTIFF (0.05 degree cells, about 5.6 km) and source details are saved. This verifies one pixel/date, not the full archive. It does not measure street-level rainfall or subdaily peaks. Daily CHIRPS v3 redistributes pentad totals using IMERG or ERA5 timing. CHIRPS v2 ends after Dec 2026.

## Recommended acquisition

Request MMS local gauges, preferably hourly or 10/15-minute if available, with station metadata and QC information. IMERG Final at 0.1 degree and 30 minutes is the best gridded subdaily candidate, subject to gauge validation and a free NASA download account. Use the existing NOAA accumulations as measured regional context, and the included POWER/CHIRPS examples for prototyping only.
