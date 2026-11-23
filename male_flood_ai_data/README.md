# Malé flood AI: dataset organisation

This is an empty, ready-to-fill folder template for a Malé-island flood research project. It contains folder guidance and blank CSV registers. It does not contain the datasets, articles, reviewed labels, trained models or results discussed in the chat.

## Start here

1. Extract the ZIP beside your existing project. Open `male_flood_ai_data/`.
2. Copy original downloads into the appropriate `01_raw/` folder. Keep their original filenames and bytes. Keep request URLs/parameters, readme files, units, quality flags, licences and metadata alongside each download.
3. Add one inventory row for each file or clearly defined dataset in `00_catalog/dataset_inventory.csv`. Record the relative path. Calculate a SHA-256 checksum when practical; leave unknown facts explicitly unknown.
4. Register each article/document in `00_catalog/source_register.csv`. Use stable IDs such as SRC0001. Preserve the original Dhivehi text; label translations and keep them alongside the original.
5. Put extracted, unverified incidents into `02_interim/event_candidates/`. Review them before creating accepted labels in `03_reviewed/events/flood_events.csv`.
6. Create weather/label versions and chronological fold definitions in `04_model_ready/`. Save each experiment in its own `05_outputs/runs/` directory.

See `FOLDER_MAP.md` for every folder and `TEMPLATE_GUIDE.md` for the CSV registers.

## Where your known data belongs

| Existing material | Destination |
|---|---|
| `groundsource_2026.parquet` | `01_raw/flood_catalogues/groundsource/` |
| Original Open-Meteo/ERA5 responses and hourly weather downloads | `01_raw/rainfall/reanalysis/` |
| Airport/Hulhule station records, including GSOD | `01_raw/rainfall/station/` |
| UHSLC or other measured tide-gauge records | `01_raw/sea_level/observed/` |
| Modelled sea level or predicted tides | `01_raw/sea_level/modelled/` |
| Saved English news evidence | `01_raw/flood_evidence/news_english/` |
| Saved Dhivehi/Thaana news evidence | `01_raw/flood_evidence/news_dhivehi/` |
| Original NDMA incident reports, MMS reports and MNDF records | `01_raw/flood_evidence/official_records/` |
| Malé boundary data | `01_raw/geospatial/male_boundary/` |
| Groundsource spatial extracts and candidate CSVs | `02_interim/groundsource_candidates/` |
| Reviewed flood records and source decisions | `03_reviewed/events/` |
| Historical forecast downloads, if later obtained | `01_raw/forecast_archives/` |
| Papers and the Malé case study | `06_research/papers/` and `06_research/reports/` |
| Dataset request correspondence and access conditions | `06_research/data_requests/` |

The location of a dataset does not establish its quality or availability. For example, the forecast archive folder is a placeholder, and airport observations do not automatically represent rainfall on Malé island.

## Preserve existing work

Your existing project may refer to `derived/daily_exploration/`, `derived/extended_analysis/`, `derived/groundsource_review/` and `reports/`. This template does not move those folders or change scripts. Keep existing outputs intact. If you adopt this layout, optional copies of the complete earlier output folders can go under `05_outputs/legacy/`; update and check script/dashboard paths as a separate migration.

## Data and label rules

- **Scope:** Malé island proper. Retain broader Maldives/Greater Malé records as candidates with their actual geographic scope; do not accept them as Malé observations solely because a polygon intersects the island.
- **Raw files:** treat `01_raw/` as immutable. Put extractions, cleaning and time conversions under `02_interim/`.
- **Event type:** use `rain`, `coastal`, `mixed` or `unknown` in one canonical reviewed event table. Keep rain and coastal target definitions distinct in experiments. An empty field means unknown, not false.
- **Evidence:** one article can mention several events and several articles can describe one event. Use `event_source_links.csv` for these relationships. A source disagreement remains visible in this file.
- **Dates and clocks:** publication time belongs in the source register. Flood onset, rainfall onset and pumping/response time have separate event columns. Never substitute one for another. Do not assume the publication timezone or weather accumulation window; record the evidence for conversion.
- **Grouping:** use `storm_group_id` to link related dates; unresolved grouping stays unresolved. Multiple households/articles are not automatically independent storms.
- **Coverage:** a day without a flood report is `unlabelled` unless an observation supports a stronger conclusion. A completed news search alone is not a confirmed non-flood observation.
- **Time split:** preserve time order and storm groups when defining training/testing data. Build transformations using training data only. A forecast experiment uses only inputs available at its prediction issue time.
- **Reanalysis:** retrospective weather data and archived forecasts are different inputs; retain their provenance and availability assumptions.
- **Groundsource:** derived polygons/candidates are place-based evidence leads, not measured flood extent or depth.

## Naming and versioning

Keep original raw filenames. If a provider uses the same filename repeatedly, place each acquisition in a separate `download_YYYY-MM-DD/` subfolder and record its checksum.

Use descriptive derived filenames, for example `male_daily_features_2020-2026_v001.parquet` and `male_flood_events_v001.csv`. Date ranges describe actual content. Avoid ambiguous names such as `final_final.csv`.

Use dates `YYYY-MM-DD` and verified datetimes with an explicit offset, for example `2026-11-22T15:00:00+05:00`. Set a local timestamp to `Asia/Male` only when its interpretation is established. Record source clocks and accumulation windows before normalising them.

Use UTF-8 for text. CSV templates include a UTF-8 BOM to help Excel display Thaana. CSV columns do not enforce types, so import IDs and raw date/time text as text in Excel.

## Experiment outputs

Create one folder per new run, for example `05_outputs/runs/run_20261122_100000Z/`. Retain the exact feature/label/grouping versions, split definition, code version, configuration, fitted pipeline, held-out scores, metrics, date-sensitivity results and report. Results based on news labels measure agreement with reported outcomes.

This template does not include a model, pipeline code or synthetic example observations. Fill registers from the files and evidence you actually hold.
