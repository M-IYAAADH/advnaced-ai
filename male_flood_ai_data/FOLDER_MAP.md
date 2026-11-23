# Folder map

| Folder | Contents |
|---|---|
| `00_catalog/` | Dataset inventory, source register and column definitions. |
| `01_raw/rainfall/reanalysis/` | Original Open-Meteo/ERA5 downloads, including request parameters and responses. |
| `01_raw/rainfall/station/` | Original station rainfall records, including Hulhule/airport data and quality flags. |
| `01_raw/sea_level/observed/` | Measured tide-gauge records, their reference datum and quality metadata. |
| `01_raw/sea_level/modelled/` | Modelled sea levels and tide predictions, with model and datum metadata. |
| `01_raw/flood_evidence/news_english/` | English news evidence and source metadata. |
| `01_raw/flood_evidence/news_dhivehi/` | Dhivehi/Thaana news evidence in its original language. |
| `01_raw/flood_evidence/official_records/` | Original NDMA, MNDF, MMS and other official records. |
| `01_raw/flood_catalogues/groundsource/` | The unchanged groundsource_2026.parquet release and release metadata. |
| `01_raw/geospatial/male_boundary/` | Malé island boundary and its coordinate reference system. |
| `01_raw/forecast_archives/` | Historical forecasts, if obtained, retaining issue and valid times. |
| `02_interim/weather_aligned/` | Cleaned weather tables and explicit alternative time alignments. |
| `02_interim/groundsource_candidates/` | Maldives/Malé spatial screens and candidate extractions. |
| `02_interim/event_candidates/` | Unverified event leads extracted from articles and catalogues. |
| `03_reviewed/events/` | Canonical reviewed event table and links to supporting or conflicting sources. |
| `03_reviewed/storm_groups/` | Reviewed grouping of reports/dates belonging to a common storm. |
| `03_reviewed/observation_coverage/` | Evidence about monitoring coverage and observed outcomes. |
| `03_reviewed/time_alignment/` | Documented timezone and accumulation-window decisions. |
| `04_model_ready/features/` | Versioned daily feature tables and feature definitions. |
| `04_model_ready/splits/` | Reproducible chronological training, validation and test definitions. |
| `05_outputs/runs/` | A separate directory for each new experiment, with its data versions and results. |
| `05_outputs/figures/` | Exportable paper figures and tables. |
| `05_outputs/dashboard/` | Dashboard exports or data generated for the dashboard. |
| `05_outputs/legacy/daily_exploration/` | Optional copy of earlier daily_exploration outputs, kept intact. |
| `05_outputs/legacy/extended_analysis/` | Optional copy of earlier extended_analysis outputs, kept intact. |
| `05_outputs/legacy/groundsource_review/` | Optional copy of earlier groundsource_review outputs, kept intact. |
| `06_research/papers/` | Research papers, citation records and reading notes. |
| `06_research/data_requests/` | Dataset request details, correspondence and access conditions. |
| `06_research/reports/` | Case study, methodology, review decisions and final report drafts. |
