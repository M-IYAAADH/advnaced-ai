# agent.md: working brief for the Malé area flood project

Last updated 23 Nov 2026. Read with `CLAUDE.md` (data-quality cautions), `data_review.md` (road evidence review) and `reports/combined_folder_review.md` (current state of both folders and the evidence by ward). If they conflict, the student's latest explicit instruction wins, then this file.

## 1. Topic and study area

- Module topic (student-selected): *Geospatial-Based Flood Risk Modelling and Predictive Analysis Using Artificial Intelligence*.
- **Current research question (student decision, 23 Nov 2026):** which **areas** of **Malé island proper** (for example Maafannu) are prone to flooding after rainfall?
  - Changed from roads and road sections (14 Nov 2026) because there is not enough road-level elevation or drainage data. FABDEM at about 30 m suits area units better than single streets.
  - Reporting unit: the four wards (Henveiru, Galolhu, Maafannu, Machchangolhi), from OSM (`derived/male_wards_osm.geojson`). Check the ward lines against a Council map before relying on them.
  - Analysis unit: a **200 m square grid** (decided 23 Nov 2026). It gives 71 cells touching the OneMap island polygon, about 11 of them containing a landmark report. Each cell is tagged with the ward covering most of it. Grid in a projected CRS (EPSG:32643), aligned so each cell holds 2 × 2 WorldPop 100 m pixels where possible; each cell averages about 40 FABDEM 30 m pixels. Fallback: 250 m (47 cells) if too many cells lack data. Four wards alone support description only.
  - The road inventory and matching work stay as evidence. Landmarks can now be placed in an area; whole-road reports cross ward lines and are not assigned to one ward.
- Study boundary: the official OneMap Malé polygon `Male_Flood_Data_Starter_Pack/boundary/OneMap_Male_Island.geojson`. OSM layers are clipped to a slightly different OSM island polygon, so reconcile coastline differences. Hulhumalé, Hulhulé, Villimalé and the Midhili Magu link road are **out of scope**. Their records are kept in the inventory and flagged `in_study_area = no`.
- Process: rainfall-driven urban waterlogging. Keep coastal, wave and swell flooding separate.

## 2. Susceptibility mapping, not forecasting

| | Area susceptibility mapping (current) | Future-event forecasting (not current) |
|---|---|---|
| Question | Where in Malé does flooding tend to occur? | When will the next flood happen? |
| Unit | Ward for reporting; 200 m grid cell for analysis | Day or hour |
| Labels needed | Location evidence: flooded, prone, or observed dry | Dated flood / no-flood events |
| Timestamps | **Optional** for the initial inventory | Essential |
| Evaluation | Spatial hold-out (unseen areas) | Chronological hold-out with issue and lead time |

Student clarifications (14 Nov 2026, still in force at area level):
- Timestamps are optional for the location inventory. Do not discard location evidence because it lacks a date. Keep dates where they exist, because they let us count independent events.
- A place observed flooding after rainfall is evidence that its area is flood-prone. Keep each record at its real scope (whole road, bounded section, junction, landmark, ward, city). A whole-road mention is not evidence that every part of the road flooded.
- Keep rainfall with its units and accumulation period. Record an unknown period as `unknown`. "Flooded after X mm" is an association, not a minimum threshold.
- Areas and roads absent from the records are **unknown**, not dry, unless they were observed not flooding.
- Pumping-only records show where water was removed, which partly reflects where pumps are stationed. Never rank areas by raw record counts.

Do not pivot the main project to recipe analysis, heavy-rain classification or tide regression.

## 3. Assignment requirements

Confirmed with the lecturer (reported by the student, 14 Nov 2026; closes MF-10 and issues I1–I4):
- **Deliverable:** a six-page literature review, citing at least 15 related journal articles, in IJCAI format. This replaces the older brief's 1,000–1,200-word report.
- **Template:** `COURSEWORK  SUBMISSION TEMPLATE _RESEARCH PAPER TEMPLATE .doc` in this folder is the IJCAI-format template. Use it.
- **Page rules:** references do **not** count toward the six pages. Follow the IJCAI template's rules otherwise.
- **Deadline:** 30 May 2027, **12:00 am Maldives time (UTC+5)**. This deadline covers the **whole project**. "12:00 am on 30 May" usually means midnight at the *start* of 30 May (the end of 29 May), so plan to submit by **29 May 2027**.
- **Older recipe brief:** none of its other components apply. Clustering, classification, regression and neural-network comparison, the Colab notebook and the recorded demo are **not required**.
- **Topic:** the flood topic is approved by the lecturer (reported by the student; no written copy is stored in this folder).

Still not in this folder: the planning files described in `CLAUDE.md` (`Project_Plan.md`, `latex/`, `ijcai26.docx`, reading matrix, 22-reference shortlist). The literature search (MF-19) does not depend on them.

## 4. Data locations

| Path | Contents | Status |
|---|---|---|
| `Male_Flood_Data_Starter_Pack/` | Boundary, OSM roads/land use, three building alternatives, WorldCover, WorldPop, FABDEM, NOAA, UHSLC, 3 city-level event leads | Raw. See its README and `CLAUDE.md` §3 |
| `Male_Flood_Data_Starter_Pack/mapping/male_osm_roads.geojson` | 571 OSM features, 65.7 km, incl. footways/service | Base road layer. 29% of features unnamed; major roads often carry only a Dhivehi `name` |
| `male-flood-basis/data/flood_incidents_greater_male_2021-2026.csv` | 18 rain-flood incidents, summaries, reported rainfall, places, URLs | Raw. Secondary, news-derived compilation |
| `male-flood-basis/data/flooded_roads_and_places_greater_male.csv` | 32 places (10 roads/sections, 16 landmarks, 6 ward/island-level), coordinates, dates, URLs | Raw. Road coordinates are midpoints, not flood points |
| `male-flood-basis/data/flood_locations_greater_male.geojson` | Compiler's road lines (traced from OSM) and points | Raw |
| `male-flood-basis/flood_map.html` | Compiler's map and write-up | Raw. Contains unverified claims (see `data_review.md`) |
| `male-flood-basis/data/*reanalysis*, hulhule_station_*, male_sea_level_*, male_forecast_*, male_daily_features_with_flood_labels.csv` | ERA5, GSOD, modelled sea level, forecast snapshot, daily table | Raw. Forecasting-oriented, not needed for the current question |
| `derived/road_flood_inventory.csv` | 73 traceable records (67 Malé) | Derived |
| `derived/road_match_review.csv` | Match status per place | Derived |
| `derived/road_flood_matched_segments.geojson` | 56 OSM segments linked to evidence (QGIS) | Derived. Not flooded/dry labels |
| `derived/road_flood_evidence_map.png` | Map | Derived |
| `derived/unnamed_segment_review.csv` | The 8 unnamed OSM segments under the compiler's lines, each marked part of the named road or not (MF-15) | Derived. Geometry-only decisions |
| `derived/landmark_position_check.csv` | Each Malé landmark point checked against its named OSM feature and the OneMap polygon (MF-16) | Derived. Not an imagery check |
| `derived/male_wards_osm.geojson`, `male_wards_map.png/.pdf` | The 4 Malé wards from OSM and a map (MF-48) | Derived. Not checked against a Council map |
| `derived/ward_evidence_summary.csv`, `ward_landmark_assignment.csv` | Landmark records placed in wards; v003 events naming each ward | Derived. Report counts, not flood frequency |
| `male_flood_ai_data/` | Organised data folder (MF-46): v003 reviewed events (`03_reviewed/events/flood_events.csv`), catalogue, aligned weather, official PDFs, status reports | Reviewed and interim data. Files already elsewhere in the repo and the Council workbook are omitted; see its `OMITTED_FILES.csv` |
| `scripts/` | `build_road_flood_inventory.py`, then `match_road_flood_records.py`, then `review_unnamed_segments.py` and `check_landmark_positions.py`; `build_ward_map.py`, then `summarise_ward_evidence.py` | Re-run from the project root (steps in `README.md`) |

## 5. Processing conventions

- Never edit raw files. All outputs go in `derived/`, built by scripts in `scripts/` with project-relative paths.
- Every inventory row cites `source_file` and `source_page_or_row`. Interpretations go in `notes`, never in measured fields.
- Use the explicit value `unknown`. Never impute zero rain, "dry", or a coordinate.
- `flood_status` values: `reported_flooded`, `designated_flood_prone` (council list). There is no `not_flooded` value, because no such evidence exists yet.
- `spatial_scope` values: `whole_road_named_section_unknown`, `road_section_bounded`, `road_section_vague`, `landmark_vicinity`, `ward`, `city`, `island`.
- Road names: keep the original spelling, plus a spelling key (no apostrophes or spaces, doubled letters collapsed). OSM Dhivehi aliases: Majeedhee Magu = މަޖީދީ މަގު, Ameenee Magu = އަމީނީ މަގު, Boduthakurufaanu Magu = ބޮޑުތަކުރުފާނު މަގު. Each is confirmed against the compiler's geometry. Do not match Ameenee Magu to *Amenee Goalhi*, or Rahdhebai Magu to *Rah Dhebai Hingun*.
- Landmarks are never assigned to a road. Nearby roads are listed as candidates only.
- Distances use a local metre projection centred at 4.175°N 73.5°E (fine for this island). For GIS work use EPSG:32643.
- Respect licences (OSM ODbL, FABDEM CC BY-NC-SA, etc.). Don't republish household-level details.

## 6. Known limitations of the evidence

- Positive-only and secondary: news and agency reports. The v003 review (22 Nov 2026) fetched and read 71 sources, but 23 of its 43 events rest on a single source, and independence between publishers is unresolved.
- By ward (see `reports/combined_folder_review.md` §3): Maafannu has 29 of the 38 landmark records, but 20 of those are pumping reports at routine pump sites (IGMH, West Park). Galolhu and Machchangolhi are under-reported, not shown to be dry. 16 of the 30 accepted rain events name no ward.
- Reporting bias: the named roads are mostly the island's main arterials (Majeedhee, Ameenee, Boduthakurufaanu) and well-known landmarks. On city-wide days (13 Aug 2024, 3 Jan 2025, 21 Oct 2026) many unnamed streets also flooded.
- 31 of 67 Malé records are pump/dewatering deployments. These show where water was removed, which partly reflects where pumps are stationed.
- Rainfall with an amount exists for only 5 of 18 incidents, mostly daily totals. The period is unknown for two of the five, and one has contradictory figures (142.2 vs 162 mm).
- The Boduthakurufaanu section flood on 30 Jul 2026 was attributed to pumps not yet commissioned on a rebuilt road, which is a construction confounder.
- No surveyed DEM, drainage network or pump-station locations are available. FABDEM at about 30 m is too coarse for street-level susceptibility, which is why the unit moved to areas.

## 7. Next steps

1. Check the OSM ward lines against a Council ward map, and build the 200 m analysis grid (MF-20).
2. Spot-check source articles for the 17 road records and the most-cited landmarks, recording the quote and any place detail that locates the flooding within an area. Raise confidence only after checking.
3. Place every located record (landmark, bounded section, ward mention, v003 `location_as_reported`) in its area unit at its real scope.
4. Exploratory comparison of area characteristics (FABDEM elevation, distance to coast, WorldCover, building coverage, road density) between areas with reports and **unknown** areas. Treat this as descriptive only, with and without the pump-site records.
5. Request observed-dry and complete location data from the City Council, NDMA (assistance logs) and MNDF (pump deployment logs), plus pump and drain locations from MWSC. See `Male_Flood_Data_Starter_Pack/Data_Request_Specification.md`.
6. Only then choose a modelling approach: positive-unlabelled learning or a ranking model over the 200 m grid cells with spatially blocked evaluation. See `data_review.md` §6.

Tasks, owners and sprint dates for these steps are in `sprint.md` (viewable in `sprint_board.html`).

## 8. Task tracking: update `sprint.md` and push after every completion

`sprint.md` is the single source of truth for task status. Every completed task must be recorded there and pushed to GitHub (https://github.com/M-IYAAADH/advnaced-ai, branch `main`), so the whole team sees the same board.

| Step | Command / action |
|---|---|
| 1. Get the latest version | `git pull` |
| 2. Start a task | Set its **Status** to `In progress` |
| 3. Finish a task | When the acceptance check is met, set **Status** to `Review`. Another member reviews it and sets `Done` |
| 4. Update the issue log | Change the status in `data_issues.md` for any issue IDs the task resolves |
| 5. Commit and push | `git commit -am "MF-11: Review"`, then `git push` |
| 6. If the push is rejected | `git pull`, keep both people's row changes, then push again |

Rules:
- This applies to every member and to Claude. Claude is authorised to commit and push after each completed task.
- Edit only the rows you worked on. Keep the table headers unchanged and don't use `|` inside a cell; the board will show an error naming the bad row if you do.
- Work that isn't in `sprint.md` yet gets a new row (unique ID, Sprint, Owner `M1`/`M2`/`M3`, Points) before it starts.
