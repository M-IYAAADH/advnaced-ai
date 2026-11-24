# MF-42: peer review of Iyaadh's attribute and exploratory code

Reviewer: Aslan (M2), 24 Nov 2026. Scope: `scripts/compute_grid_attributes.py` (MF-22) and `scripts/compare_reported_unknown.py` (MF-30). Spatial blocks (MF-26) are out of scope.

## How it was checked

- Read both scripts in full.
- Reran both on Windows 11 in a clean venv built from `requirements.txt` (Python 3.13, the pinned package versions).
- Compared the regenerated outputs with the committed ones using `git status`.
- Recomputed vehicular road length per cell, sampled at 1 m and tested against the OneMap polygon, to check the road-density shortcut.

## Result

The method matches its docstrings. After fixes R1 and R2, both scripts reproduce `derived/grid_attributes.csv`, everything in `derived/mf30/` and `reports/mf30_reported_vs_unknown.md` byte for byte, and all built-in self-checks pass. The cell counts hard-coded in the MF-30 text match the data: 57 main-set cells, 6 construction-confounded cells (5 in the main set) and 2 routine pump sites.

## Findings

| ID | Severity | File | Finding | Resolution | Status |
|---|---|---|---|---|---|
| R1 | High (blocks rerun on Windows) | both | Files were opened without `encoding=`, so Windows used cp1252. `compute_grid_attributes.py` crashed reading the OneMap GeoJSON (`UnicodeDecodeError`). `compare_reported_unknown.py` wrote "Malé" in the report as cp1252, not UTF-8. This also blocks MF-32 on Windows. | Added `encoding="utf-8"` to the 4 `read_text()` calls and to the report `open()`. Outputs unchanged. Four other scripts have the same pattern (`build_dashboard.py`, `build_ward_map.py`, `define_spatial_blocks.py`, `explore_daily_flood.py`), outside this review; `scripts/rebuild_all.py` (MF-32) sets PYTHONUTF8=1, so they run there; run directly on Windows they still need the fix. | Resolved |
| R2 | Medium | `requirements.txt` | `compute_grid_attributes.py` imports `PIL`, but Pillow was not listed. It only arrived as a matplotlib dependency, so its version was unpinned. | Added `pillow==13.0.0`. | Resolved |
| R3 | Medium (affects MF-30 numbers) | `compute_grid_attributes.py` | Road length is clipped to the cell square but divided by land area (the documented shortcut). 891 m of the 61,043 m of vehicular road lies off the OneMap polygon (harbour and jetty segments). Clipping roads to land would cut density by 40% in G334800_462000, which has the highest density in the main set and is a reported, construction-confounded cell. G334600_462000 would drop by 19% and two others by 2 to 4%. All four are reported cells. The V1 reported median would fall from 30,860 to 29,113 m per km2, against 31,268 for unknown cells. So the "reported vs unknown" road-density comparison in MF-30 is partly an edge artefact. | Fixed: roads are now sampled at 1 m or finer, and only samples inside both the cell and the OneMap ring are counted. The Liang-Barsky clip is removed. The fix also drops OSM 1528883097, the duplicate segment flagged in `reports/review_s1_aslan.md` (MF-15, issue F3). It is read from `unnamed_segment_review.csv` (`rule = duplicate_geometry`), not hard-coded. New self-check: cell sums equal the on-land total (64,753 m of 65,655 m). Only the 4 road columns of `grid_attributes.csv` changed, in 27 cells. In MF-30 (V1, main set), the reported median vehicular density fell from 30,900 to 29,100 m per km2 and the unknown median stayed at 31,300. V4 fell from 31,400 to 29,400, so it is now below unknown instead of just above it. The reported maximum fell from 43,900 to 35,100. The IQR-overlap shares are unchanged (0.64, 0.67). | Resolved |
| R4 | Low | `compare_reported_unknown.py` | Several text values are hard-coded: "57-cell main set" in the figure titles, and "6 construction-confounded cells" and "two routine pump-site cells" in the report. They are correct now but will go stale if the evidence changes. | Built from `d.main.sum()`, `conf.sum()` and `pump.sum()`. The report now says "2" and "6" in digits. | Resolved |
| R5 | Low | `compare_reported_unknown.py` | The self-check on group n covers `ATTRS[2:]` only, so the FABDEM rows (two filter variants) are not checked. Line 101 repeats the check on line 100. | The self-check now covers every attribute and every `fabdem_filter` row, and asserts exactly one row per combination. The duplicate check was removed. | Resolved |
| R6 | Nit | `compute_grid_attributes.py` | A cell with no land would divide by zero (`ok.sum() / m`). It can't happen with the current grid (minimum land fraction 0.001). `.sum(1)` raises a Pandas4Warning. | Changed to `.sum(axis=1)`. The divide-by-zero case can't occur with this grid, so it is left as is. | Resolved |

R3 to R6 were fixed by Aslan on 24 Nov 2026, at the student's request, without waiting for Iyaadh. Both scripts pass their self-checks, and `scripts/rebuild_all.py --check-only` passes. Iyaadh should confirm the R3 method change when moving MF-42 to Done. The new road-density numbers replace the old ones wherever MF-30 is quoted.
