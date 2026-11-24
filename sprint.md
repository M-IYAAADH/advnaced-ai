# Sprint board — Malé area flood susceptibility

This file is the task source for `sprint_board.html`. Edit it, commit and push. The board re-reads it every 15 seconds when served (`http://localhost:8080/sprint_board.html`), or use **Load sprint.md** if the page is opened from disk.

## How to update

- To move a task, change its **Status** cell to `To do`, `In progress`, `Review` or `Done`. Only change your own rows unless the team agrees.
- Move a task to `Review` when its acceptance check is met. Another member reviews it before it becomes `Done`.
- Keep the table headers exactly as they are, and one row per task. Don't use the `|` character inside a cell.
- New tasks need a unique ID, a Sprint ID from the Sprints table, an Owner of `M1`, `M2` or `M3`, and whole-number Points.
- **Depends on** and **Issues** take comma-separated IDs, or `None`. Issue IDs refer to `data_issues.md`.
- **Conditional** is `Yes` for tasks that only happen if an earlier decision approves them.
- Commit message suggestion: `MF-11: In progress` or `MF-11: Done`.

## Team

| Member ID | Name | Scrum role | Focus |
| --- | --- | --- | --- |
| M1 | Iyaadh | Product Owner · Developer | Analysis and modelling: evidence checks, segment attributes, exploratory analysis, modelling decision, evaluation |
| M2 | Aslan | Developer | Data and pipelines: road segmentation, evidence joins, spatial folds, reproducible builds, maps |
| M3 | Gaanith | Scrum Master · Developer | Research and writing: source verification, literature review, data dictionary, wording checks |

Roles are a proposal; agree them at Sprint 1 planning. Sprint 0 work is recorded under Iyaadh; reassign it if teammates contributed.

## Sprints

| Sprint ID | Name | Start | End | Type | Goal |
| --- | --- | --- | --- | --- | --- |
| S0 | Sprint 0 | 2026-11-03 | 2026-11-14 | Sprint | Audit the data and build a traceable road-flood inventory. |
| S1 | Sprint 1 | 2026-11-15 | 2026-11-28 | Sprint | Verify the road-flood evidence and confirm the assignment requirements. |
| S2 | Sprint 2 | 2026-11-29 | 2026-12-12 | Sprint | Build the area-unit table (inside the 4 wards) with evidence status and attributes. |
| S3 | Sprint 3 | 2026-12-13 | 2026-12-26 | Sprint | Describe how reported areas differ from unknown areas, with the bias stated. |
| S4 | Sprint 4 | 2026-12-27 | 2027-01-09 | Sprint | Holiday-light sprint: peer reviews, rainfall table and literature review outline. |
| S5 | Sprint 5 | 2027-01-10 | 2027-01-23 | Sprint | Decide whether a positive-only ranking model is defensible, and set up spatial folds. |
| S6 | Sprint 6 | 2027-01-24 | 2027-02-06 | Sprint | Evaluate the ranking model (if approved) and draft the review's main sections. |
| S7 | Sprint 7 | 2027-02-07 | 2027-02-20 | Sprint | Complete the full literature review draft, with verified results inputs. |
| S8 | Sprint 8 | 2027-02-21 | 2027-03-06 | Sprint | Review, polish, page check and group sign-off (internal deadline 6 Mar 2027). |
| BUF | Buffer | 2027-03-07 | 2027-05-29 | Buffer | Lecturer feedback and final submission by 29 May 2027 (deadline 12:00 am on 30 May, Maldives time). |

Dates are YYYY-MM-DD. Deadline (confirmed with the lecturer): 30 May 2027, 12:00 am Maldives time, for the whole project. Plan to submit by 29 May 2027.

## Tasks

| ID | Sprint | Owner | Points | Status | Task | Depends on | Issues | Conditional | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MF-01 | S0 | M1 | 3 | Done | Catalogue the Malé starter data pack | None | None | No | Boundary, OSM, buildings, rasters, rainfall and tide data catalogued with licences and QA notes. |
| MF-02 | S0 | M1 | 3 | Done | Collect news-derived road-flood evidence | None | None | No | male-flood-basis/ compilation: 18 incidents, 32 places, source URLs. |
| MF-03 | S0 | M1 | 5 | Done | Build traceable road-flood inventory | MF-02 | None | No | derived/road_flood_inventory.csv: 73 records, each citing source file and row. |
| MF-04 | S0 | M1 | 5 | Done | Match records to OSM roads and draw evidence map | MF-03 | F1, F2, F6 | No | road_match_review.csv, matched segments GeoJSON and evidence map; Dhivehi aliases documented. |
| MF-05 | S0 | M1 | 3 | Done | Write data review and issue log | MF-04 | None | No | data_review.md and data_issues.md (43 issues with status). |
| MF-06 | S0 | M1 | 1 | Done | Record scope rules and publish repository | None | None | No | agent.md and CLAUDE.md updated; project pushed to GitHub. |
| MF-10 | S1 | M1 | 1 | Review | Confirm requirements with the lecturer | None | I1, I2, I3 | No | Submission time, page rules (do references count?) and whether the recipe-brief components apply are recorded in agent.md §3. |
| MF-11 | S1 | M3 | 5 | To do | Verify the 17 road records against source articles | None | A1, D3 | No | Each road record gets a quoted phrase and any section or junction detail; confidence raised only where the article confirms it. |
| MF-12 | S1 | M1 | 3 | Review | Verify the top 4 landmarks and settle duplicates | None | A1, B2, E1, E2 | No | IGMH, West Park, Villimalé Ferry Terminal, STO checked; pump wording (E1) and Rasfannu (E2) resolved; West Park/STO merge decided. |
| MF-13 | S1 | M3 | 2 | To do | Read the JICA 2021 survey report | None | A5 | No | Notes on flood photos, drainage and elevation findings, with page numbers. |
| MF-14 | S1 | M2 | 2 | Done | Resolve the Rahdhebai Magu match | None | C1, C2, D1 | No | Match confirmed or rejected using the source article and imagery; match review updated. |
| MF-15 | S1 | M2 | 2 | Done | Review 8 unnamed OSM segments beside matched roads | None | F3 | No | Each segment marked as part of the named road or not, with the reason. |
| MF-16 | S1 | M2 | 2 | Done | Check landmark positions on imagery | None | E6 | No | Approximate and off-polygon points confirmed or moved, with the change logged. |
| MF-17 | S1 | M1 | 3 | Review | Draft agency data requests | None | H1, H2, H3, H4 | No | Drafts to Council/NDMA, MNDF, MWSC and MMS approved by the group. Nothing is sent without approval. |
| MF-18 | S1 | M2 | 2 | Done | Pin the Python environment and rerun steps | None | None | No | requirements.txt plus README steps; a teammate rebuilds derived/ from scratch. |
| MF-46 | S1 | M1 | 3 | Review | Organise data into male_flood_ai_data and reconcile the new flood inventory CSV | None | A1, G1, G5 | No | All files mapped and checksum-verified; 30 imported records reconciled, none promoted to labels; DATA_STATUS_REPORT written; archive verified. |
| MF-47 | S1 | M1 | 5 | Review | Exploratory daily reported-flood analysis and dashboard (supporting work, not the main question) | None | G1, G4, G5, G6 | No | reports/daily_exploration.md and reports/extended_analysis.md with fold results, time-alignment sensitivity and a dashboard; zero means no report, not dry. Uses v001 labels and needs a rerun on v003. |
| MF-48 | S1 | M1 | 2 | Review | Malé ward boundary map from OSM | None | None | No | derived/male_wards_osm.geojson (4 wards) and male_wards_map.png/pdf rebuilt by scripts/build_ward_map.py; OSM credit shown. Ward lines not yet checked against a Council map. |
| MF-49 | S1 | M1 | 2 | Review | Combined repo and data-folder review; switch recorded scope from roads to areas | MF-46, MF-48 | A1, A4, A5 | No | reports/combined_folder_review.md and ward evidence CSVs (scripts/summarise_ward_evidence.py); CLAUDE.md, agent.md, sprint.md and data_issues.md updated for the area scope. |
| MF-19 | S1 | M3 | 3 | Review | Literature search: 20+ candidate journal articles | None | None | No | Shortlist covering urban/road flood susceptibility, positive-only learning and spatial validation, with full references. |
| MF-20 | S2 | M1 | 5 | Review | Build the 200 m analysis grid inside the OSM wards | MF-48 | None | No | derived/male_grid_200m.geojson from scripts/build_analysis_grid.py: 75 cells in EPSG:32643 with stable IDs, land fraction, majority ward and ward share; cells' land equals the island area (self-check). Rasters are in degrees, so MF-22 weights them by overlap. |
| MF-21 | S2 | M2 | 3 | Review | Attach evidence to area units at the right scope | MF-20, MF-11, MF-12, MF-14 | B1, B4, D3, F6 | No | Each unit is reported, pumping-only, designated or unknown, with record scope kept. Whole-road and ward mentions are not spread to every unit as 'flooded'. |
| MF-22 | S2 | M1 | 5 | Review | Compute area-unit attributes | MF-20 | None | No | FABDEM elevation, WorldCover, building coverage (one source only), coast distance and road density per unit. |
| MF-23 | S2 | M1 | 1 | To do | Send approved data requests and log responses | MF-17 | G1 | No | Sent date and contact recorded in a response log. |
| MF-24 | S2 | M3 | 2 | To do | Data dictionary for the area-unit table | MF-21, MF-22 | None | No | Every column has units, source, licence and a known-limitations note. |
| MF-25 | S2 | M3 | 5 | To do | Reading matrix: appraise the first 8 articles | MF-19 | None | No | Task, data, resolution, labels, validation and limitations recorded for each article. |
| MF-26 | S2 | M1 | 2 | Review | Define spatial blocks and grouping rules | MF-20 | G3 | No | Blocks of neighbouring area units chosen (wards or groups of tiles); records at one landmark kept in one block. |
| MF-27 | S2 | M2 | 1 | To do | Imagery check: Rah Dhebai Magu match and OSM segment 1528883097 | MF-14, MF-15 | C1, F3 | No | Both checked on imagery; checked_on_imagery set in road_match_review.csv and unnamed_segment_review.csv. Follow-up from the MF-14/MF-15 review. |
| MF-30 | S3 | M1 | 5 | Review | Compare reported vs unknown areas | MF-21, MF-22 | G2 | No | Tables and plots by ward and by area unit, with and without pump-site records; written as descriptive, not causal. |
| MF-31 | S3 | M2 | 3 | Review | Area evidence map and QGIS project | MF-21 | None | No | Map and .qgz file; areas without reports labelled unknown, not dry. |
| MF-32 | S3 | M2 | 3 | Review | One-command rebuild from raw to derived | MF-21 | None | No | A single script rebuilds all outputs and checks every record still traces to its source row. |
| MF-33 | S3 | M3 | 5 | To do | Reading matrix: appraise the remaining articles | MF-25 | None | No | At least 15 journal articles fully appraised. |
| MF-34 | S3 | M3 | 1 | To do | Wording check on exploratory outputs | MF-30 | G1, G4 | No | Says 'reported', treats unknown as unknown, and states no rainfall thresholds. |
| MF-40 | S4 | M3 | 2 | Review | Set up the review in the coursework IJCAI template | None | I4 | No | The coursework .doc template opens with the title, authors and section skeleton in place. |
| MF-41 | S4 | M3 | 3 | In progress | Literature review outline by theme | MF-33 | None | No | Themes, article-to-section mapping and a page budget. |
| MF-42 | S4 | M2 | 2 | In progress | Peer-review Iyaadh's attribute and exploratory code | MF-30 | None | No | Findings logged and resolved. |
| MF-43 | S4 | M1 | 2 | To do | Peer-review Aslan's area units and evidence join | MF-21, MF-32 | None | No | Findings logged and resolved. |
| MF-44 | S4 | M1 | 2 | Review | Descriptive rainfall table for reported incidents | None | C3, D6, G4 | No | Units, accumulation periods and contradictions kept; no threshold claims. |
| MF-45 | S4 | M2 | 3 | To do | Follow up agency requests and load any data received | MF-23 | H1, H2, H3, H4 | No | Response log updated; received data stored raw with provenance. |
| MF-50 | S5 | M1 | 2 | Review | Decision record: descriptive only, or ranking model | MF-30, MF-45 | G1, G2, G3 | No | The group agrees, using the verified evidence and agency responses. No flooded/dry classifier without observed-dry data. |
| MF-51 | S5 | M2 | 3 | To do | Implement spatial folds | MF-26, MF-50 | B2, B3, G3 | No | Block-based folds over area units; near-duplicate places merged before splitting. |
| MF-52 | S5 | M1 | 5 | To do | Prototype positive-only ranking model | MF-50, MF-51 | G1 | Yes | Only if MF-50 approves it. Positive-unlabelled or presence-background model, presented as a ranking, not a probability. |
| MF-53 | S5 | M3 | 5 | To do | Draft review sections: background and methods | MF-41 | None | No | Drafted from the reading matrix, with citations. |
| MF-54 | S5 | M2 | 2 | To do | Leakage checks | MF-51 | None | No | All preprocessing is fitted inside training folds; a test confirms it. |
| MF-60 | S6 | M1 | 5 | To do | Evaluate ranking: recall@k and Boyce index | MF-52 | G2, G3 | Yes | Results with and without pump-site records; no accuracy scored against unknown areas. |
| MF-61 | S6 | M2 | 2 | To do | Peer-review model and evaluation | MF-60 | None | Yes | Folds, leakage and metrics checked; findings resolved. |
| MF-62 | S6 | M3 | 5 | To do | Draft review sections: labels, validation, research gap | MF-53 | None | No | Drafted with citations, and linked to this project's evidence limits. |
| MF-63 | S6 | M2 | 3 | To do | Report-ready figures pipeline | MF-31 | None | No | Map, exploratory and evaluation figures exported at print resolution by script. |
| MF-70 | S7 | M3 | 5 | In progress | Complete the full review draft in IJCAI format | MF-62, MF-40 | None | No | Six pages excluding references, with at least 15 journal articles cited. |
| MF-71 | S7 | M1 | 3 | To do | Results and limitations input | MF-30 | None | No | Verified numbers, figures and limitations handed to Gaanith. |
| MF-72 | S7 | M2 | 3 | To do | Methods input: data, processing, reproducibility | MF-32 | None | No | Short verified notes on sources, licences and the build pipeline. |
| MF-73 | S7 | M1 | 2 | To do | Check every number in the draft | MF-70 | None | No | Each figure in the text traced to a derived output or a cited source. |
| MF-80 | S8 | M3 | 3 | To do | Citation, reference and page-count check | MF-70 | I1 | No | References complete; body is six pages or fewer, excluding references. |
| MF-81 | S8 | M1 | 2 | To do | Group review of the full draft | MF-73 | None | No | All three members have commented and every comment is resolved. |
| MF-82 | S8 | M2 | 2 | To do | Final repository tidy | MF-32 | None | No | README, run steps, licences and attribution are complete; data_issues.md statuses are current. |
| MF-83 | S8 | M1 | 1 | To do | Group sign-off (internal deadline 6 Mar 2027) | MF-80, MF-81, MF-82 | None | No | All three members approve the submission package. |

## Backlog

Not yet in a sprint. The lecturer confirmed on 14 Nov 2026 (MF-10) that the older recipe brief's components don't apply. The former PB-01 to PB-04 (Colab notebook, recorded demo, 1,000–1,200-word report and model comparison) were removed; the report is replaced by the six-page review (MF-70).

| ID | Owner | Item | Pending confirmation | Note |
| --- | --- | --- | --- | --- |
| PB-05 | M2 | Integrate observed-dry or complete-coverage data from agencies | No | Only if agencies supply it (MF-45). This would unlock a supervised classifier. |
| PB-06 | M1 | Rainfall-response analysis with MMS hourly gauges | No | Only if MMS supplies hourly data (H4). Out of the current scope. |
| PB-07 | M3 | Verify the unsourced map-page claims (40–45 mm, pump capacity, GSOD completeness) | No | Issues A2, A3, A4. Low priority unless the review cites them. |
