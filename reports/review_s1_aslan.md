# Review of Aslan's Sprint 1 tasks (MF-14, MF-15, MF-16, MF-18)

Reviewed 24 Nov 2026 by Iyaadh (M1). All four tasks are moved to Done.

## How it was checked
- Fresh clone of `main` in a clean Python 3.12 venv from `requirements.txt`.
- Ran `build_road_flood_inventory.py`, `match_road_flood_records.py`, `review_unnamed_segments.py` and `check_landmark_positions.py` twice, with `PYTHONHASHSEED=0` and `123`.
- Every committed output was rebuilt with the same content, under both seeds.

## Findings
| Task | Result | Note |
| --- | --- | --- |
| MF-18 | Pass | Rebuild works from scratch and is seed-stable. One fix: `derived/unnamed_segment_review.csv` was committed with LF endings while the script writes CRLF, like every other derived CSV (Windows git converted it). The rebuilt CRLF file is committed here, so a rebuild no longer shows a diff. |
| MF-14 | Pass, with one gap | Rah Dhebai Magu match is well argued from the two articles and OSM topology. The acceptance check also asks for imagery, which was not done. Moved to MF-27. |
| MF-15 | Pass | All 8 segments have a decision and reason. Segment 1528883097 still needs the imagery check (MF-27). |
| MF-16 | Pass | 13 landmarks match an OSM feature (0 to 11 m). Rasfannu and the Swimming Track are offshore and excluded from matching. No positions were moved. |

## For Iyaadh (not Aslan's work)
MF-15 said to drop segment 1528883097 so road length is not counted twice. `scripts/compute_grid_attributes.py` (MF-22) does not exclude it, so about 57 m is double-counted in one cell's road density. Fix it in MF-22 and rerun MF-30 before quoting road density.

## Aslan's next tasks
1. **MF-27**: imagery check for the Rah Dhebai Magu match and segment 1528883097 (1 point).
2. **MF-32**: one command that rebuilds raw to derived. The README steps (lines 15 to 30) are the starting list.
3. **MF-42**: peer-review Iyaadh's attribute and exploratory code (MF-22, MF-30).
4. Review MF-21 and MF-31. Both are M2 rows that Iyaadh built, so Aslan is the right reviewer.
5. MF-51 (spatial folds) waits for the group's MF-50 decision.
