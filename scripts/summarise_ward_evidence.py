"""Place Malé flood evidence into the four OSM wards.

Inputs: derived/male_wards_osm.geojson (scripts/build_ward_map.py),
        derived/road_flood_inventory.csv,
        male_flood_ai_data/03_reviewed/events/flood_events.csv (v003).
Outputs: derived/ward_landmark_assignment.csv (one row per landmark record),
         derived/ward_evidence_summary.csv (one row per ward).
Counts are reports, not flood frequency: no report means unknown, not dry.
Whole-road records are not assigned, because those roads cross ward lines.
Run from the project root: python scripts/summarise_ward_evidence.py
"""
import csv
import json
import re
from collections import defaultdict

from matplotlib.path import Path

WARDS = "derived/male_wards_osm.geojson"
INVENTORY = "derived/road_flood_inventory.csv"
EVENTS = "male_flood_ai_data/03_reviewed/events/flood_events.csv"
NAME_PATTERNS = {"Henveiru": r"henveiru", "Galolhu": r"galolhu", "Maafannu": r"maafannu", "Machchangolhi": r"mach+angolhi"}


def load_wards():
    feats = json.load(open(WARDS, encoding="utf-8"))["features"]
    return [(f["properties"]["ward"], [Path(poly[0]) for poly in f["geometry"]["coordinates"]]) for f in feats]


def ward_of(wards, lon, lat):
    hits = [name for name, polys in wards if any(p.contains_point((lon, lat)) for p in polys)]
    return hits[0] if len(hits) == 1 else ("outside_ward_polygons" if not hits else "ambiguous")


def main():
    wards = load_wards()
    names = [n for n, _ in wards]

    assigned = []
    for r in csv.DictReader(open(INVENTORY, encoding="utf-8-sig")):
        if r["in_study_area"] != "yes" or r["spatial_scope"] != "landmark_vicinity":
            continue
        try:
            lon, lat = float(r["longitude"]), float(r["latitude"])
        except ValueError:
            continue  # unknown coordinate stays unassigned, never imputed
        assigned.append({"record_id": r["record_id"], "location_description": r["location_description"],
                         "event_date_if_available": r["event_date_if_available"], "evidence_type": r["evidence_type"],
                         "confidence": r["confidence"], "ward": ward_of(wards, lon, lat)})
    with open("derived/ward_landmark_assignment.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(assigned[0]))
        w.writeheader()
        w.writerows(assigned)

    events = [e for e in csv.DictReader(open(EVENTS, encoding="utf-8-sig")) if e["decision"] == "accepted_reported_rain_event"]
    named = defaultdict(int)
    for e in events:
        text = (e["location_as_reported"] + " " + e["notes"]).lower()
        for ward, pat in NAME_PATTERNS.items():
            if re.search(pat, text):
                named[ward] += 1

    summary = []
    for ward in sorted(names):
        recs = [a for a in assigned if a["ward"] == ward]
        summary.append({"ward": ward,
                        "landmarks": len({a["location_description"] for a in recs}),
                        "landmark_records": len(recs),
                        "distinct_landmark_dates": len({a["event_date_if_available"] for a in recs if a["event_date_if_available"] not in ("", "unknown")}),
                        "v003_accepted_rain_events_naming_ward": named[ward],
                        "v003_accepted_rain_events_total": len(events)})
    with open("derived/ward_evidence_summary.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(summary[0]))
        w.writeheader()
        w.writerows(summary)

    assert sum(s["landmark_records"] for s in summary) + sum(a["ward"] not in names for a in assigned) == len(assigned)
    for s in summary:
        print(s)


if __name__ == "__main__":
    main()
