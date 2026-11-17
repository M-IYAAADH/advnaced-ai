# advnaced-ai

Advanced AI (UFCFUR-15-3) project: **geospatial flood susceptibility of roads on Malé island proper, Maldives**.

The research question is which roads or road sections are prone to rain-driven flooding. This is susceptibility mapping, not forecasting the next flood. No model has been trained yet.

## Start here
- `data_review.md`: review of the road-flood evidence, matching results, and what can be built
- `data_issues.md`: logged data issues with status and actions
- `agent.md`: working brief, conventions and next steps
- `CLAUDE.md`: data-quality cautions for every dataset

## Layout
| Path | Contents |
|---|---|
| `Male_Flood_Data_Starter_Pack/` | Raw spatial, elevation, rainfall and tide data (see its README) |
| `male-flood-basis/` | Raw news-derived compilation of rain-flood incidents and places (2021–2026) |
| `derived/` | Inventory, road-match review, matched segments GeoJSON, evidence map, unnamed-segment review, landmark position check |
| `scripts/` | `build_road_flood_inventory.py`, then `match_road_flood_records.py` (see *Rebuild the derived files*) |

## Rebuild the derived files
Needs Python 3.10 or newer. Run from the repository root:

```
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python scripts/build_road_flood_inventory.py
python scripts/match_road_flood_records.py
python scripts/review_unnamed_segments.py
python scripts/check_landmark_positions.py
```

This rewrites the six files in `derived/` and never touches the raw folders. The CSV and GeoJSON outputs are deterministic, so a clean rebuild should leave `git status` showing no changes to them. The PNG map can differ by a few pixels between platforms or matplotlib versions (font rendering).

## Data licences
Each dataset keeps its own terms; there is no single licence for this repository. See `Male_Flood_Data_Starter_Pack/README.md`. Key terms: OpenStreetMap © contributors (ODbL 1.0); FABDEM CC BY-NC-SA 4.0; Google Open Buildings, ESA WorldCover and WorldPop CC BY 4.0; Microsoft buildings CDLA Permissive 2.0.
