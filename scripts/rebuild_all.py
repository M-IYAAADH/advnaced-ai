"""MF-32: rebuild every derived output from the raw inputs with one command, then check traceability.

Run from anywhere:  python scripts/rebuild_all.py
  --check-only   skip the rebuild and only run the traceability checks

Steps are the README "Reproduce" list, in order; the first failing step stops the run. Raw inputs
(Male_Flood_Data_Starter_Pack/, male-flood-basis/, male_flood_ai_data/, verification/) are never written.
The male_flood_ai_data packaging scripts (organise_/package_male_flood_ai_data, reconcile_flood_inventory,
finalise_catalog) are not steps: they were one-off builds from downloads outside the repo, and their
reviewed tables are inputs here.

Traceability checks (each failure is listed; exit code 1 if any):
  - every inventory row's "incident row N (ID)" and "places row M" point at that row of the source CSV
  - every record_id used downstream exists in the inventory; every places_file_row matches the place name
  - every cell_id, v003_event_id, incident_id and matched osm_id exists in its source table
At the end, tracked outputs that the rebuild changed are listed (git status), so drift from the committed
version is visible.
"""
import csv
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEPS = [
    "build_road_flood_inventory", "match_road_flood_records", "review_unnamed_segments",
    "check_landmark_positions", "build_incident_rainfall_table", "build_ward_map", "summarise_ward_evidence",
    "build_analysis_grid", "attach_evidence_to_grid", "compute_grid_attributes", "define_spatial_blocks",
    "compare_reported_unknown", "build_area_evidence_map", "explore_daily_flood", "extended_daily_analysis",
    "build_dashboard",
]
INCIDENTS = "male-flood-basis/data/flood_incidents_greater_male_2021-2026.csv"
PLACES = "male-flood-basis/data/flooded_roads_and_places_greater_male.csv"


def rebuild():
    # PYTHONUTF8: several scripts open files without encoding=, which breaks on Windows cp1252 (MF-42 R1)
    env = dict(os.environ, PYTHONUTF8="1", LOKY_MAX_CPU_COUNT="2",
               MPLCONFIGDIR=str(Path(tempfile.gettempdir()) / "male-matplotlib"))
    for i, s in enumerate(STEPS, 1):
        t = time.time()
        print(f"[{i}/{len(STEPS)}] {s} ...", flush=True)
        r = subprocess.run([sys.executable, f"scripts/{s}.py"], cwd=ROOT, env=env, capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        if r.returncode:
            sys.exit(f"FAILED at {s} (exit {r.returncode}):\n{r.stdout[-2000:]}\n{r.stderr[-4000:]}")
        print(f"    ok ({time.time() - t:.0f} s)")


def rows(path):
    with open(ROOT / path, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def ids(path, col):
    return {r[col] for r in rows(path)}


def check():
    bad = []
    inc, places = rows(INCIDENTS), rows(PLACES)
    inv = rows("derived/road_flood_inventory.csv")
    rid = [r["record_id"] for r in inv]
    if len(set(rid)) != len(rid):
        bad.append("road_flood_inventory: duplicate record_id")

    # 1. inventory row -> source rows ("row N" = CSV record N-1 after the header, as the builder counts)
    for r in inv:
        src = r["source_page_or_row"]
        m = re.search(r"incident row (\d+) \(([^)]+)\)", src)
        if not m:
            bad.append(f"{r['record_id']}: no incident row in '{src}'")
        else:
            n, iid = int(m[1]), m[2]
            if not 2 <= n <= len(inc) + 1 or inc[n - 2]["incident_id"] != iid or r["incident_id"] != iid:
                bad.append(f"{r['record_id']}: incident row {n} is not {iid}")
        for p in re.findall(r"places row (\d+)", src):
            p = int(p)
            name = places[p - 2]["name"] if 2 <= p <= len(places) + 1 else None
            if name is None or name not in (r["road_name_original"], r["location_description"]):
                bad.append(f"{r['record_id']}: places row {p} is '{name}', record names "
                           f"'{r['road_name_original']}' / '{r['location_description']}'")

    # 2. downstream record_id and places_file_row references
    inv_ids = set(rid)
    refs = {
        "derived/grid_evidence_records.csv": [r["record_id"] for r in rows("derived/grid_evidence_records.csv")],
        "derived/ward_landmark_assignment.csv": [r["record_id"] for r in rows("derived/ward_landmark_assignment.csv")],
        "verification/landmark_checks.csv": [r["record_id"] for r in rows("verification/landmark_checks.csv")],
        "derived/road_match_review.csv": [x for r in rows("derived/road_match_review.csv")
                                          for x in r["inventory_record_ids"].split(";") if x],
    }
    for f, xs in refs.items():
        bad += [f"{f}: record_id {x} not in inventory" for x in sorted(set(xs) - inv_ids)]
    if set(refs["derived/grid_evidence_records.csv"]) != inv_ids - {r["record_id"] for r in inv if r["in_study_area"] != "yes"}:
        bad.append("grid_evidence_records: record set differs from the in-study-area inventory")
    for f in ("derived/road_match_review.csv", "derived/landmark_position_check.csv"):
        for r in rows(f):
            p = int(r["places_file_row"])
            if not 2 <= p <= len(places) + 1 or places[p - 2]["name"] != r["place"]:
                bad.append(f"{f}: places_file_row {p} is not '{r['place']}'")

    # 3. other keys
    cells = {f["properties"]["cell_id"] for f in
             json.loads((ROOT / "derived/male_grid_200m.geojson").read_text(encoding="utf-8"))["features"]}
    events = ids("male_flood_ai_data/03_reviewed/events/flood_events.csv", "event_id")
    inc_ids = {r["incident_id"] for r in inc}
    for r in rows("derived/grid_evidence_records.csv"):
        if r["cell_id"] and r["cell_id"] not in cells:
            bad.append(f"grid_evidence_records {r['record_id']}: cell {r['cell_id']} not in grid")
        for e in filter(None, r["v003_event_id"].split(";")):
            if e not in events:
                bad.append(f"grid_evidence_records {r['record_id']}: event {e} not in flood_events")
    for f in ("derived/grid_evidence.csv", "derived/grid_attributes.csv", "derived/grid_blocks.csv"):
        if ids(f, "cell_id") != cells:
            bad.append(f"{f}: cell_id set differs from male_grid_200m.geojson")
    bad += [f"incident_rainfall_table: {x} not in incidents" for x in
            sorted(ids("derived/incident_rainfall_table.csv", "incident_id") - inc_ids)]
    bad += [f"road_flood_inventory: incident {x} not in incidents" for x in sorted({r["incident_id"] for r in inv} - inc_ids)]
    osm = {str(f["properties"]["osm_id"]) for f in json.loads(
        (ROOT / "Male_Flood_Data_Starter_Pack/mapping/male_osm_roads.geojson").read_text(encoding="utf-8"))["features"]}
    seg = {str(f["properties"]["osm_id"]) for f in json.loads(
        (ROOT / "derived/road_flood_matched_segments.geojson").read_text(encoding="utf-8"))["features"]}
    bad += [f"road_flood_matched_segments: osm_id {x} not in OSM roads" for x in sorted(seg - osm)]

    print(f"traceability: {len(inv)} inventory rows, {len(cells)} cells, {len(seg)} matched segments checked")
    return bad


if __name__ == "__main__":
    if "--check-only" not in sys.argv:
        rebuild()
    problems = check()
    for p in problems:
        print("  TRACE FAIL", p)
    changed = subprocess.run(["git", "status", "--porcelain", "-uno", "--","derived", "reports", "qgis"], cwd=ROOT,
                             capture_output=True, text=True).stdout.strip()
    print("tracked outputs changed by this build:\n" + changed if changed else "outputs identical to the committed version")
    sys.exit(1 if problems else 0)
