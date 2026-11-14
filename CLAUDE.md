# Malé flood AI project: working context

This file records the student's stated requirements and the verified state of the supplied files. Use it when interpreting older or conflicting material in this folder. Explicit later instructions from the student take precedence.

## 1. Current project and requirements

- Student-selected project topic: **Geospatial-Based Flood Risk Modelling and Predictive Analysis Using Artificial Intelligence**.
- Selected study area: **Malé island proper, Maldives**. Do not silently expand the scope to Hulhumalé, Vilimalé or Greater Malé.
- Proposed manageable implementation: explainable geospatial modelling of rainfall-induced urban flood susceptibility. Treat coastal/wave flooding as a distinguishable process. This is the current planning recommendation, not proof that a model is already validated.
- **Research question clarified by the student (14 Nov 2026): which roads or road sections on Malé island proper are prone to flooding?** This is road susceptibility mapping, not forecasting the date/time of the next flood. See `agent.md` for the working rules and `data_review.md` for the current evidence review.
  - Event dates/timestamps are **optional** for the initial road-flood inventory. Do not reject useful location evidence only because it lacks a timestamp. (Dates remain required for any future-event or rainfall-response claim.)
  - A report naming a whole road is road-level evidence. Do not label every segment of it as flooded; distinguish whole-road, bounded-section, junction and landmark reports.
  - Keep rainfall amounts with their units and accumulation periods (e.g. 30 mm in 1 h vs 30 mm in 24 h); record unknown periods as unknown. Flooding after X mm is an association, not a minimum triggering threshold.
  - Roads absent from the records are **unknown**, not dry, unless there is evidence they were observed not flooding.
- Current lecturer instructions reported by the student: a **six-page literature review**, using **at least 15 related journal articles**, in the supplied **IJCAI 2026 format**.
- Working submission deadline supplied by the student: **30 May 2027**. The exact submission time, whether references count within the six pages, and whether this is the review-only or whole-project deadline remain unconfirmed.
- The planning pack contains 22 screened journal references. They need full-text appraisal before detailed claims and numerical results are used.

The uploaded recipe-review assignment brief is a conflicting older/reference brief, with inconsistent dates. It is not sufficient evidence to replace the student's selected flood topic with recipe analysis. Retain the flood topic as the working scope. Do not invent written lecturer approval; none has been supplied in this folder. Flag unresolved rubric questions once without blocking literature review, data audit or exploratory GIS work.

Whether clustering, classification, regression, neural-network comparison, the 1,000–1,200-word report, Colab submission and recorded demo from the older brief apply to this project must be clarified. Do not present them as confirmed requirements for the current six-page review.

## 2. Find the project files

The two ZIP packs may have been extracted into different subfolders. Locate files by name; do not assume a fixed absolute path.

- Planning: `Project_Plan.md`, `Flood_AI_Project_Plan.pdf`, `Literature_Reading_Matrix.csv`, `Journal_Article_Shortlist.json`.
- Writing: `latex/flood_review_starter.tex`, `latex/flood_review.bib`, original `ijcai26.sty` and `named.bst`; original Word template `ijcai26.docx`.
- Data: `Dataset_Catalogue.json`, `Dataset_Catalogue.md`, `Research_Report.md`, `Male_Flood_Data_Research.pdf`, `File_Manifest.json`.
- Acquisition: `Data_Request_Specification.md`.
- Data subfolders: `boundary/`, `mapping/`, `elevation/`, `rainfall/`, `tides/`, `flood/`.
- Read folder-specific README and QA/source JSON files before processing.
- Road-flood evidence (added 14 Nov 2026): `male-flood-basis/` (news/agency-report compilation, map page and weather files). Derived, traceable outputs: `derived/road_flood_inventory.csv`, `derived/road_match_review.csv`, `derived/road_flood_matched_segments.geojson`, `derived/road_flood_evidence_map.png`, built by `scripts/build_road_flood_inventory.py` then `scripts/match_road_flood_records.py`.
- As of 14 Nov 2026 the planning and writing files listed above (`Project_Plan.md`, `latex/`, `ijcai26.docx`, reading matrix) are **not present in this folder**; the only template here is the legacy `COURSEWORK SUBMISSION TEMPLATE _RESEARCH PAPER TEMPLATE .doc`.

The supplied Word template is `.docx`, not a legacy `.doc`. The literature-review starter is an outline, not a completed six-page review. The reference list is not a substitute for critical reading. No trained flood model or completed final submission was included in the packs.

## 3. What the downloaded data actually support

### Spatial inputs

- Official OneMap Malé island polygon; an OSM island boundary is also supplied.
- 571 OSM road features and 51 OSM land-use features.
- Alternative building sources: 933 cleaned OSM footprints; 4,677 Microsoft detections; 5,773 Google detections at confidence >=0.75, with 10,077 in the full Google audit file.
- ESA WorldCover 2021, approximately 10 m land-cover raster.
- WorldPop 2025, approximately 100 m **modelled** population for optional exposure analysis.
- FABDEM V1-2, approximately 30 m, plus a Malé clip. It is not validated local bare-earth survey. Its within-island median about 5.04 m and maximum about 15.15 m warrant bias/coastline checks.

Keep building sources separate. Counts are not building ground truth, and footprints do not establish usable height or household counts. WorldCover built-up class is not measured hydraulic imperviousness. WorldPop is not an official Malé census total.

Mapping clips use the OSM island polygon; the FABDEM clip uses the official OneMap polygon. Reconcile boundaries and dates before joins. All files are horizontally WGS84/EPSG:4326; use a suitable projected CRS for distances/areas and preserve originals. Raster grids have different native spacing and alignment.

### Weather and water level

- NOAA airport/Velana station 435550/99999 (VRMM) is on nearby **Hulhulé**, not Malé island proper.
- NOAA Global Hourly contains meteorological reports for 2024 and January–24 August 2025. Checked precipitation groups contain **6-, 12- and 24-hour accumulations**; no one-hour rainfall groups were verified. Preserve QC/condition flags and do not add overlapping totals.
- GSOD contains 591 dated rows: 355 in 2024 and 236 in 2025. There are **590 nonmissing precipitation values** because `PRCP=99.99` on **17 April 2024** is missing, not extreme rain.
- Recounted illustrative threshold: **47 valid days have PRCP >=1 inch (25.4 mm)**, before any additional filtering based on accumulation completeness/quality flags. This is 26 days in 2024 and 21 in 2025. The threshold is an analytical choice, not a verified MMS flood-warning standard.
- GSOD precipitation units are inches; temperature fields are Fahrenheit. Retain raw values and attributes when converting. Document each variable's units rather than applying a blanket conversion to every field.
- UHSLC 2024 CSV contains 8,784 hourly timestamps, **8,659 valid water levels and 125 missing**. Skip the units row immediately after the header. Values are millimetres relative to station zero, not flood depths or automatically mean sea level. Reconcile vertical datums before comparing with DEM heights.
- CHIRPS v3 includes only a small **3 January 2025** sample; it is not a complete historical rainfall series. NASA POWER contains only a **1–5 January 2025, 120-hour reanalysis example**, not local gauge measurements.
- Preserve original timestamps; distinguish UTC from Maldives UTC+5 and document reporting/accumulation windows.

### Flood labels and drainage

- `flood/event_candidates.csv` contains only **three city-level date/source leads**. It is not a flooded/dry location dataset, a complete event inventory or validation evidence for a flood classifier.
- No complete open multi-event, location-specific flooded/dry inventory was verified. Assistance/sandbag requests are not automatically observed inundation. No incident report does not mean observed dry.
- No detailed open Malé drainage GIS or high-resolution surveyed ground DEM was verified. Agency-held data may exist.
- DALA aggregate downloads were advertised, but the actual CSV bytes were not obtained. Do not describe them as downloaded observations.
- Update 14 Nov 2026: `male-flood-basis/` adds a **positive-only, news-derived** compilation of 18 rain-flood incidents (Dec 2021 to Oct 2026) naming 7 Malé roads, 2 bounded road sections and 15 landmarks. It is secondary evidence from an AI-assisted compilation whose source articles have not been checked here. It contains no observed-dry locations; most mentions are landmarks or pump/dewatering sites, and named roads are mostly the main arterials (reporting bias). Its `flood_reported = 0` days in `male_daily_features_with_flood_labels.csv` mean "no report found", not dry. Its "40 to 45 mm daily rain at which Malé starts to flood" is an attributed quote without a linked source; do not treat it as a verified threshold. Details: `data_review.md`.

## 4. Keep the research task honest

Susceptibility mapping, rain-event classification, tide forecasting and flood-risk prediction are different targets.

- A heavy-rain classifier can be a supporting weather experiment, but it does not demonstrate flood prediction or geospatial flood susceptibility.
- Tide/water-level regression can be a supporting baseline, but it does not predict observed street inundation depth.
- Weather or building clustering is exploratory analysis; it does not create flood truth.
- Do not pivot the main project to these targets just to fill an unconfirmed old rubric. Present alternatives and their implications before changing the project question.
- Do not invent flood labels, depths, results, data availability or literature-review findings. Synthetic/expert-derived labels must be explicitly identified and cannot be presented as observed flood validation.

For genuine future heavy-rain prediction, define the issue time and lead time; do not use the same day's final rainfall total or other observations unavailable at issue time as predictors. Use chronological evaluation and appropriate persistence/climatology baselines. Retrospective reanalysis/final satellite products may not have been available in real time.

For geographic flood-susceptibility claims, use spatially separated evaluation, grouping repeated locations. A chronological split alone does not establish performance at unseen streets. For temporal claims, hold out future events. Choose the evaluation design to match the claim and fit preprocessing within training folds.

Three selected flood dates can support a narrowly described qualitative case study only after station/date alignment. They cannot establish flood-classifier accuracy, specificity, false-alarm rate or operational skill.

## 5. Data acquisition priorities

1. Council/NDMA: deidentified event-location records with timestamps, precision, flooded/dry/unknown status, evidence/verification, flood mechanism and observation coverage across independent events.
2. MMS: local hourly and any available subhourly rainfall, station metadata, QC flags and accumulation windows matching those events.
3. Engineering/project custodian: accurate surveys/DEM if available, existing versus proposed drains, inlets/outfalls, invert levels, pump capacities/operation and dated condition/maintenance.
4. Measured flood depth/duration only if a regression task requires such a target.

The 2023 DEM/masterplan EOI `MV-MONPI-326937-CS-QCBS` was cancelled on 12 August 2024. It does not establish DEM delivery. Separate Malé stormwater detailed designs/tender documents were reported completed by May 2024; seek underlying survey/drainage files from the project custodian. The reference contract `MV-MONPI-234588-CS-CQS` is distinct. See the research report for primary-source links.

## 6. Useful work to start now

Start with an auditable data-readiness and exploratory notebook, not a purported trained flood classifier:

1. Inventory the files and verify schema, missing values, units, dates, locations, geometry/CRS and QC flags.
2. Load/clean GSOD and UHSLC without imputing unknown observations to zero. Produce coverage and missingness tables and labelled exploratory plots.
3. Map Malé roads and one building alternative. Compare sample areas across building sources and record boundary/raster alignment issues.
4. Define candidate location/event schemas and list the flood-label/elevation/drainage fields still needed. Do not populate them with invented values.
5. Continue the six-page literature review by themes, comparing task, data, resolution, validation and limitations across the journal studies.
6. Propose the core modelling experiment once labels and data support are known. Supporting weather/tide models may be explored with clear target names and evaluation, without claiming they complete the flood project.

Preserve raw inputs and source metadata. Keep derived outputs separate, retain dataset-specific attribution/licences, use paths relative to the project root and avoid hard-coded paths from the original download environment. Do not send agency requests or publish household-level data without the student's instruction and appropriate access rights.

## 7. Task tracking: update `sprint.md` and push after every completion

`sprint.md` is the single source of truth for task status. `sprint_board.html` reads it; the GitHub repo is https://github.com/M-IYAAADH/advnaced-ai (public, branch `main`).

After finishing any task listed in `sprint.md` (whether done by a team member or by Claude):

1. `git pull` first, so you edit the latest version.
2. In the task's row, set **Status** to `Review` once its acceptance check is met. Only another member moves it to `Done` after reviewing it. Use `In progress` when starting work.
3. Update `data_issues.md` statuses for any issue IDs the task resolves.
4. Commit the work and the `sprint.md` change together, with a message such as `MF-11: Review`, then `git push`.
5. If the push is rejected, `git pull` (resolve any conflict in `sprint.md` by keeping both people's row changes) and push again.

The student has authorised Claude to commit and push to this repo after each completed task. Keep the `sprint.md` table headers unchanged, don't use `|` inside cells, and edit only the rows you worked on. New work that isn't in `sprint.md` gets a new row (unique ID, Sprint, Owner `M1`/`M2`/`M3`, Points) before it starts.
