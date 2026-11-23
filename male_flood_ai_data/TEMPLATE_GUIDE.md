# CSV template guide

All templates contain column headers only. No data availability, observation, non-flood day or event has been invented or accepted as a label.

| File | One row represents | Important fields |
|---|---|---|
| `00_catalog/dataset_inventory.csv` | A file or clearly defined dataset | Actual path, provider, coverage, spatial scope, timezone, accumulation, units, missing values, quality flags, download date, licence and checksum. Suggested inventory statuses: `not_imported`, `imported`, `metadata_incomplete`, `reviewed`. |
| `00_catalog/source_register.csv` | One news article or official document | Stable source ID, publisher, original title, `en`/`dv`/other language, URL, publication date/time as printed, separately verified datetime and local evidence path. Unknown source timezone stays unknown. |
| `00_catalog/data_dictionary.csv` | A column in a dataset | Meaning, type, units, accepted values and what missing means. |
| `02_interim/event_candidates/event_candidates.csv` | A candidate occurrence from a source | Keep reported date wording, location, scope and proposed cause. Suggested statuses: `pending`, `needs_date_check`, `needs_scope_check`, `reviewed`. |
| `03_reviewed/events/flood_events.csv` | A reviewed flood occurrence/date window | Stable event ID; inclusive local date range; confirmed/uncertain scope; flood type; storm ID; separate optional flood-onset, rain-start and response clocks; evidence; reviewer and review date. Suggested statuses: `accepted`, `uncertain`, `excluded`. A missing storm ID does not mean independence. |
| `03_reviewed/events/event_source_links.csv` | An event-to-source relationship | Suggested relationships: `supports`, `conflicts`, `context_only`, `possible_duplicate`. Record conflicting dates and decisions without erasing the original claim. |
| `03_reviewed/storm_groups/storm_groups.csv` | A proposed or reviewed storm group | Date window, grouping basis, evidence and decision status. Do not infer independence from an arbitrary calendar gap alone. |
| `03_reviewed/observation_coverage/observation_coverage.csv` | Coverage/outcome evidence for one date and scope | Coverage method and status. Suggested methods: `systematic_observation`, `agency_record`, `media_search`, `unknown`. Suggested outcomes: `flood_observed`, `non_flood_observed`, `unlabelled`, `uncertain`. Record evidence for an observed non-flood outcome; do not derive it from absent news. |
| `03_reviewed/time_alignment/time_alignment_decisions.csv` | A documented alignment decision or hypothesis | Original timezone/accumulation window; proposed target; conversion; evidence; `unresolved`, `hypothesis_only` or `verified`. Retain alternatives for sensitivity analysis. |
| `04_model_ready/features/feature_catalog.csv` | One model feature | Sources, aggregation, lag and whether/when the feature could be available at issue time. Same-day completed rainfall cannot silently become an advance forecast input. |
| `04_model_ready/splits/splits.csv` | One experiment fold | Issue time/horizon, chronological date ranges, gap, and versions of features, labels and storm groups. Use a documented half-open or inclusive boundary convention consistently. |

## IDs and source relationships

Use IDs consistently across tables: `SRC0001`, `EVT0001`, `STORM0001`, `DS0001`. IDs identify records, not confidence or chronological ordering. Record the review decision separately.

Keep the canonical reviewed table in `03_reviewed/events/`. If exporting a versioned modelling snapshot, save that snapshot with the experiment and document its origin. Separate exported rain/coastal subsets should be reproducible views of the canonical table.

## No fixed flood count in the template

The news windows and official leads discussed in the chat still need comparison with the project inventory, date checks and storm grouping. This folder structure deliberately does not turn those counts into confirmed model labels.
