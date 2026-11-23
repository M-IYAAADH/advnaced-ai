# Repo and data folder: combined review

Reviewed 23 Nov 2026. This compares the project repo with the organised data folder `male_flood_ai_data/` (v002/v003, 22 Nov 2026), and summarises the flood evidence by ward for the area-level question.

## 1. How the two folders relate

`male_flood_ai_data/` was built from the repo by MF-46, then extended by the v002 and v003 source and clock checks. On 23 Nov 2026 it was compared file by file (SHA-256) with the repo.

| Status | Files | Contents |
|---|---:|---|
| Byte-identical to a repo file | 152 | Starter pack, `male-flood-basis/`, earlier outputs, copies of the project docs |
| Only in the data folder, now in the repo | 106 | v003 reviewed events, catalogue and source register, aligned weather tables, NOAA 2020–2023 station files, official PDFs, status reports, archived v001/v002 tables |
| Kept out of git | 6 | Council workbook (sharing permission not confirmed), `groundsource_2026.parquet` (636 MB), an old copy of `sprint.md`, the old recipe brief, an unused email prompt |

Every omitted file is listed in `male_flood_ai_data/OMITTED_FILES.csv`, with the repo path of its copy or the reason it was left out. Duplicates were not committed twice.

## 2. Repo statements that the data folder supersedes

| Topic | Earlier repo statement | Current evidence (data folder) |
|---|---|---|
| Flood labels | 18 compiled incidents; 11 dated events retained (`reports/extended_analysis.md`) | 43 reviewed events: 30 accepted rain, 6 coastal, 7 uncertain (`03_reviewed/events/flood_events.csv`, v003) |
| Hulhulé GSOD day | One-day shift "probable, not proven" | Established: GSOD for local day L is stored on date L+1 (1,700 of 1,701 days) |
| GSOD magnitude (issue A4) | Claim that GSOD totals are under half the true rain, unverified | Explained: the SYNOP 24 h group is about one-tenth of the 12 h sums on 178 days (2020 to 1 Feb 2024), and GSOD inherits it |
| ERA5 clock | `time_local` undocumented | Established as UTC+5. Release latency and the original request are still unknown |
| Modelled sea-level clock | Undocumented | Still unresolved: UTC+4 or UTC+5 |
| Source checks (issue A1) | About 40 linked articles never opened | 71 sources fetched and read; 23 of the 43 events rest on one source |
| JICA report (issue A5) | Not read | The 2022 JICA survey PDF is now in `01_raw/flood_evidence/official_records/`. Still to be read (MF-13) |
| Data folder README | Describes an empty template | The folder holds data. Read `06_research/reports/CHATGPT_DATA_UPDATE.md` for the current state |

Consequence: the daily analysis (MF-47) used the v001 labels and needs a rerun on v003 before any of its numbers are quoted.

## 3. Evidence by ward

Ward boundaries come from OpenStreetMap (`derived/male_wards_osm.geojson`, MF-48). They have not been checked against a Council ward map. Figures are rebuilt by `scripts/summarise_ward_evidence.py` into `derived/ward_evidence_summary.csv` and `derived/ward_landmark_assignment.csv`.

| Ward | Landmarks | Landmark records | Of which pumping only | Distinct dates | v003 accepted rain events naming the ward |
|---|---:|---:|---:|---:|---:|
| Maafannu | 6 | 29 | 20 | 11 | 10 |
| Henveiru | 5 | 7 | 4 | 5 | 4 |
| Galolhu | 1 | 1 | 1 | 1 | 0 |
| Machchangolhi | 1 | 1 | 1 | 1 | 0 |

- 16 of the 30 accepted rain events name no ward. Most are city-wide ("many roads in the four districts", "nearly all streets").
- Maafannu's lead comes mostly from IGMH (10 records) and West Park (8). Both are routine pump sites (issue B4), and 20 of Maafannu's 29 records are pumping reports, not stated flooding.
- The Ekuveni track point falls in Machchangolhi, but its position still needs an imagery check (issue E6).
- Whole-road records (13) and the 2 bounded sections are not assigned to a ward, because those roads cross ward lines.

**Reading.** The records lean towards Maafannu, but this reflects where pumps are placed and where landmarks are reported as much as where water collects. Galolhu and Machchangolhi are under-reported, not shown to be dry. Four wards support a descriptive comparison only; any model or spatial hold-out needs finer units inside the wards.

## 4. What this changes

1. Recorded scope is now area level (student decision, 23 Nov 2026); `CLAUDE.md`, `agent.md` and `sprint.md` were updated.
2. Issues A1, A4 and A5 in `data_issues.md` were updated with the v002/v003 findings.
3. Analysis unit decided (23 Nov 2026): a 200 m grid (71 cells on the island, about 11 with a landmark report; fallback 250 m). Still open: checking the OSM ward lines against a Council map; rerunning MF-47 on v003.
