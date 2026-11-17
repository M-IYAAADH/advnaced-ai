"""Build derived/road_flood_inventory.csv from the male-flood-basis compilation.

One row = one place named in one reported rain-flood incident (or one
non-dated designation). Every row cites the source file and row it came from.
Interpretations that are not stated verbatim in the source files are written
into `notes`, never into the measured fields.

Inputs (read-only):
  male-flood-basis/data/flood_incidents_greater_male_2021-2026.csv
  male-flood-basis/data/flooded_roads_and_places_greater_male.csv
  Male_Flood_Data_Starter_Pack/boundary/OneMap_Male_Island.geojson

Run from the project root:  python3 scripts/build_road_flood_inventory.py
"""
from __future__ import annotations

import csv
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INC = ROOT / "male-flood-basis/data/flood_incidents_greater_male_2021-2026.csv"
PLACES = ROOT / "male-flood-basis/data/flooded_roads_and_places_greater_male.csv"
BOUNDARY = ROOT / "Male_Flood_Data_Starter_Pack/boundary/OneMap_Male_Island.geojson"
OUT = ROOT / "derived/road_flood_inventory.csv"

UNK = "unknown"

# ---------------------------------------------------------------------------
# Rainfall reported in the incident file, per incident. Amounts are copied from
# the `reported_rainfall` text; the accumulation period is filled only where the
# text states it. Anything else stays "unknown".
# ---------------------------------------------------------------------------
RAIN = {
    "2023-07-21": dict(mm=UNK, period=UNK, station=UNK,
        note="Source: heaviest at Hulhule 08:00-11:00; no amount published."),
    "2023-12-31": dict(mm="118.2", period=UNK, station="Male (as reported)",
        note="Source text: 'Hulhule 179.9 mm in 24 h (record), Male 118.2 mm'. The 24 h period is stated for the Hulhule figure only; Male period not stated."),
    "2024-08-13": dict(mm="89.4", period="24 h, 08:00 to 08:00 (end date not stated)", station="Male (as reported)",
        note="Hulhule 63.4 mm also reported for the same window."),
    "2024-12-20": dict(mm="136.5", period="24 h, 08:00 Fri 20 Dec to 08:00 Sat 21 Dec 2024", station="Male (as reported)",
        note="Hulhumale 117 mm also reported for the same window."),
    "2025-01-03": dict(mm="142.2", period=UNK, station="Male (as reported)",
        note="CONTRADICTION in source: '162 mm by 11pm in another count'. Hulhule 144 mm; Hulhumale 122-164 mm. Periods not stated."),
    "2025-03-01": dict(mm=UNK, period=UNK, station=UNK,
        note="Source: about two hours of rain after sunset; amount not reported."),
    "2026-10-21": dict(mm="90", period="24 h", station="Male (as reported)", note=""),
}

# ---------------------------------------------------------------------------
# Evidence classification for each (incident, place) pair, read from the
# incident `summary` text. Keys are (incident_id, place name as in the files).
# evidence_type vocabulary:
#   news_report_flooding          news text says the place flooded / was under water
#   news_report_photograph        news/survey says the place was photographed flooded
#   dewatering_reported           pumps / MNDF / firefighters drained water there
#   agency_flood_prone_list       council named the road as flood-prone / repaired it
#                                 after the event (designation, not a dated sighting)
#   official_statement_no_streets Met Office / authority statement without street names
#   building_flooding_reported    houses/buildings flooded; says nothing about roads
#   other_reported_impact         closure, digging, burials etc. linked to water
# ---------------------------------------------------------------------------
E = {}
def ev(inc, place, etype, scope, conf, note=""):
    E[(inc, place)] = (etype, scope, conf, note)

IGMH = "IGMH area (Indira Gandhi Memorial Hospital)"
KKB = "Kudakudhinge Bageecha (children's park, Ameenee Magu)"
MFT = "Maafannu (Villimalé) Ferry Terminal"
MAJ_SEC = "Majeedhee Magu, Dhanburuh Magu to Nikagas Magu"
BOD_SEC = "Boduthakurufaanu Magu, Henveiru Ferry Terminal to Izzuddin Jetty"
CITY = "Malé city-wide (streets not named)"

ev("2021-12-11", "Henveiru Ground (stadium)", "news_report_photograph", "landmark_vicinity", "medium",
   "JICA survey photograph of 'flooded road near Henveiru Ground'; which road is not stated.")
ev("2021-12-11", "Majeedhee Magu", "news_report_photograph", "road_section_vague", "medium",
   "JICA survey photograph of 'the central part of Majeedhee Magu'; section limits not stated.")
ev("2022-07-17", "Ekuveni running track", "dewatering_reported", "landmark_vicinity", "medium",
   "Firefighters pumped out roads near the track; roads not named.")
ev("2022-07-17", IGMH, "dewatering_reported", "landmark_vicinity", "medium",
   "Firefighters pumped out roads near the IGMH area; roads not named.")
ev("2023-04-01", "Maafannu ward (streets not named)", "news_report_flooding", "ward", "medium",
   "Roads hard to walk next day; households flooded; Maafannu worst hit. Storm late on 1 Apr.")
ev("2023-07-21", CITY, "official_statement_no_streets", "city", "medium",
   "Met Office reported severe flooding on many roads in all four districts; no streets named.")
for road in ("Ameenee Magu", "Boduthakurufaanu Magu", "Majeedhee Magu"):
    ev("2023-12-31", road, "news_report_flooding", "whole_road_named_section_unknown", "medium",
       "'Heavily flooded'; no section given, so not every segment can be assumed flooded.")
for p in (IGMH, "West Park area", "Maldives Polytechnic area"):
    ev("2023-12-31", p, "dewatering_reported", "landmark_vicinity", "low",
       "Source wording 'Pumps ran at two sites near IGMH, West Park and near the Polytechnic' is ambiguous about which places had pumps.")
ev("2023-12-31", "Henveiru ward (houses flooded, streets not named)", "building_flooding_reported", "ward", "low",
   "Four houses flooded in Henveiru; no road flooding stated.")
for p in ("Hulhumalé roads (not named)", "Midhili Magu (Hulhulé to Hulhumalé highway)", "Hulhulé (airport island)"):
    ev("2023-12-31", p, "news_report_flooding", "island" if "Midhili" not in p else "whole_road_named_section_unknown",
       "medium", "Outside Male island proper study area.")
for p in ("Boduthakurufaanu Magu", KKB, "West Park area", "STO flour warehouse area"):
    ev("2024-01-10", p, "dewatering_reported", "whole_road_named_section_unknown" if p == "Boduthakurufaanu Magu" else "landmark_vicinity",
       "medium", "MNDF drained water here; no section given." if p == "Boduthakurufaanu Magu" else "MNDF drained water here.")
for p in ("STO flour warehouse area", IGMH, "West Park area", "Boduthakurufaanu Magu"):
    ev("2024-01-12", p, "dewatering_reported", "whole_road_named_section_unknown" if p == "Boduthakurufaanu Magu" else "landmark_vicinity",
       "medium", "Pumps ran here; no section given." if p == "Boduthakurufaanu Magu" else "Pumps ran here.")
ev("2024-01-12", "Ameenee Magu", "news_report_photograph", "whole_road_named_section_unknown", "medium",
   "Photographed under water; photographed section not stated.")
for p in (IGMH, "West Park area", "Pizza Buona area", "Dhiraagu head office area", "Dharubaaruge area"):
    ev("2024-08-13", p, "news_report_flooding", "landmark_vicinity", "medium",
       "Named among the worst areas; nearly all streets in Male flooded that day.")
ev("2024-08-13", "Rasfannu", "other_reported_impact", "landmark_vicinity", "low",
   "Source says Rasfannu 'was closed'; flooding at Rasfannu is implied, not stated.")
ev("2024-08-13", "Ameenee Magu", "news_report_photograph", "whole_road_named_section_unknown", "medium",
   "Photographed flooded; section not stated. Nearly all streets flooded that day.")
ev("2024-08-13", "Villimalé (streets not named)", "dewatering_reported", "island", "medium",
   "Outside Male island proper study area.")
for p in ("West Park area", IGMH, "STO flour warehouse area", MFT, "Dhiraagu head office area"):
    ev("2024-12-20", p, "news_report_flooding", "landmark_vicinity", "medium", "Flooding 'centred on' this area.")
ev("2024-12-20", MAJ_SEC, "agency_flood_prone_list", "road_section_bounded", "medium",
   "Council named this stretch as the one that floods most; closed for drainage work after the event. A designation, not a dated sighting.")
ev("2024-12-20", "Majeedhee Magu", "agency_flood_prone_list", "whole_road_named_section_unknown", "low",
   "Summary says the council repaired Majeedhee Magu after the event; it does not say the whole road flooded on 20-21 Dec. Possible double count with the bounded-section record.")
ev("2024-12-20", "Chaandhanee Magu", "agency_flood_prone_list", "whole_road_named_section_unknown", "low",
   "On council flood-prone repair list after the event; flooding on 20-21 Dec not stated directly.")
ev("2024-12-20", "Rahdhebai Magu", "agency_flood_prone_list", "whole_road_named_section_unknown", "low",
   "On council flood-prone repair list (places file). NOT listed in the incident file's locations for 2024-12-20.")
for road in ("Majeedhee Magu", "Ameenee Magu"):
    ev("2025-01-03", road, "news_report_flooding", "whole_road_named_section_unknown", "medium",
       "Became impassable; section not stated.")
for road in ("Kan'baa Aisa Rani Hingun", "Izzuddeen Magu"):
    ev("2025-01-03", road, "news_report_flooding", "whole_road_named_section_unknown", "medium",
       "Reported water depth passed two feet (about 0.6 m); location along the road not stated.")
for p in ("West Park area", IGMH, "King Salman Mosque area", MFT, KKB, "Voice of Maldives area"):
    ev("2025-01-03", p, "dewatering_reported", "landmark_vicinity", "medium", "Pumps ran here.")
ev("2025-01-03", "Rasfannu", "other_reported_impact", "landmark_vicinity", "medium",
   "Pavement dug up to drain water.")
ev("2025-01-03", "Hulhumalé Cemetery", "other_reported_impact", "landmark_vicinity", "medium",
   "Outside study area. Graves filled with water; burials suspended days later.")
ev("2025-01-11", CITY, "dewatering_reported", "city", "medium", "MNDF drained streets; 58 households assisted; no streets named.")
for inc in ("2025-03-01", "2025-03-11"):
    for p in (IGMH, "West Park area", MFT):
        ev(inc, p, "dewatering_reported", "landmark_vicinity", "medium", "Pumps deployed here.")
ev("2025-11-25", "Maafannu ward (streets not named)", "news_report_flooding", "ward", "medium", "Parts of Maafannu flooded.")
ev("2025-11-25", IGMH, "news_report_photograph", "landmark_vicinity", "medium", "Floodwater photographed near IGMH.")
ev("2026-04-16", "Maafannu ward (streets not named)", "dewatering_reported", "ward", "medium", "MNDF pumps at two unnamed locations in Maafannu.")
for p in (IGMH, MFT, "King Salman Mosque area", "Swimming Track area"):
    ev("2026-05-04", p, "dewatering_reported", "landmark_vicinity", "medium", "Dewatering took place here.")
ev("2026-07-30", BOD_SEC, "news_report_flooding", "road_section_bounded", "medium",
   "Rebuilt section; flooding attributed to permanent drainage pumps not yet running (construction-stage confounder). Section ends are landmarks; extent approximate.")
ev("2026-10-21", CITY, "news_report_flooding", "city", "medium", "Whole city flooded; 89 buildings; no streets named.")
ev("2026-10-21", "Hulhumalé Cemetery", "other_reported_impact", "landmark_vicinity", "low",
   "Outside study area. Graves filled with water; burials suspended on 24 Oct.")

# City-wide statements present only in incident summary text (not in the
# compiled location lists). Kept as separate rows so absence of a street from
# the inventory is not read as 'dry' on these days.
SUMMARY_ONLY = [
    ("2024-08-13", CITY, "news_report_flooding", "city", "medium",
     "From summary text 'Nearly every street flooded'; not in the compiled locations list."),
    ("2025-01-03", CITY, "news_report_flooding", "city", "medium",
     "From summary text 'flooded most of the city'; not in the compiled locations list."),
]

# Precision of the coordinates supplied in the places file
def precision(ptype: str, note: str) -> str:
    if ptype == "road":
        return "compiler_road_midpoint_not_flood_point"
    if ptype == "landmark":
        return "landmark_point_approximate" if "approximate" in note.lower() else "landmark_point"
    return "area_centroid_indicative_only"


def normalise(name: str) -> str:
    """Spelling key for matching: strip qualifiers/diacritics/apostrophes/spaces, collapse doubled letters."""
    n = name.split(",")[0]
    n = re.sub(r"\(.*?\)", "", n)
    n = unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode()
    n = re.sub(r"[^a-z ]", "", n.lower())
    n = re.sub(r"\s+", " ", n).strip()
    n = n.replace("higun", "hingun")
    n = re.sub(r"(.)\1+", r"\1", n)  # aa->a, ee->e
    return n


def point_in_poly(lon, lat, ring):
    inside = False
    for (x1, y1), (x2, y2) in zip(ring, ring[1:] + ring[:1]):
        if (y1 > lat) != (y2 > lat) and lon < x1 + (lat - y1) * (x2 - x1) / (y2 - y1):
            inside = not inside
    return inside


def main():
    ring = json.load(open(BOUNDARY, encoding="utf-8"))["features"][0]["geometry"]["coordinates"][0]
    with open(PLACES, encoding="utf-8-sig") as f:
        places = list(csv.DictReader(f))
    with open(INC, encoding="utf-8-sig") as f:
        incidents = list(csv.DictReader(f))
    prow = {p["name"]: (i + 2, p) for i, p in enumerate(places)}  # +2: header is line 1
    irow = {r["incident_id"]: (i + 2, r) for i, r in enumerate(incidents)}

    pairs = []
    for inc_id, (ln, r) in irow.items():
        for loc in [x.strip() for x in r["locations"].split(";") if x.strip()]:
            pairs.append((inc_id, loc, "incident_list"))
    for inc_id, loc, *_ in SUMMARY_ONLY:
        pairs.append((inc_id, loc, "summary_only"))
    # places-file dates not present in incident lists
    listed = {(a, b) for a, b, _ in pairs}
    for name, (ln, p) in prow.items():
        for d in [x.strip() for x in p["incident_dates"].split(";")]:
            inc_id = next((k for k, (_, r) in irow.items() if r["dates"] == d), None)
            if inc_id and (inc_id, name) not in listed:
                pairs.append((inc_id, name, "places_only"))

    summary_lookup = {(a, b): rest for a, b, *rest in SUMMARY_ONLY}
    rows, missing = [], []
    for k, (inc_id, loc, origin) in enumerate(sorted(pairs, key=lambda x: (x[0], x[1])), start=1):
        iln, inc = irow[inc_id]
        pln, plc = prow.get(loc, (None, None))
        cls = summary_lookup.get((inc_id, loc)) or E.get((inc_id, loc))
        if cls is None:
            missing.append((inc_id, loc)); continue
        etype, scope, conf, note = cls
        lon = plc["longitude"] if plc and plc["longitude"] else UNK
        lat = plc["latitude"] if plc and plc["latitude"] else UNK
        island = plc["island"] if plc else UNK
        if island not in ("Malé", UNK):
            in_area = "no"
        elif lon == UNK:
            in_area = "yes_no_coordinates"
        elif point_in_poly(float(lon), float(lat), ring):
            in_area = "yes"
        else:
            in_area = "yes_point_outside_onemap_polygon"  # Malé place; waterfront point falls off the polygon
        rain = RAIN.get(inc_id, dict(mm=UNK, period=UNK, station=UNK, note="Source: rainfall not reported."))
        src_files = [f"{INC.relative_to(ROOT).as_posix()}"]
        src_rows = [f"incident row {iln} ({inc_id})"]
        if plc:
            src_files.append(f"{PLACES.relative_to(ROOT).as_posix()}")
            src_rows.append(f"places row {pln}")
        if origin == "places_only":
            note = (note + " " if note else "") + "Date appears in places file but place is not in this incident's location list."
        if origin == "summary_only":
            src_rows[0] += " summary text"
        is_road = scope.startswith(("whole_road", "road_section"))
        nm = loc.split(" (")[0] if is_road else ""
        rows.append({
            "record_id": f"RF{k:03d}",
            "source_file": " | ".join(src_files),
            "source_page_or_row": " | ".join(src_rows),
            "road_name_original": loc if is_road else "",
            "road_name_normalised": normalise(nm) if is_road else "",
            "location_description": loc,
            "longitude": lon,
            "latitude": lat,
            "location_precision": precision(plc["type"], plc["note"]) if plc else ("area_centroid_indicative_only" if scope in ("city", "ward", "island") else UNK),
            "spatial_scope": scope,
            "island": island,
            "in_study_area": in_area,
            "flood_status": "designated_flood_prone" if etype == "agency_flood_prone_list" else "reported_flooded",
            "evidence_type": etype,
            "incident_id": inc_id,
            "rainfall_amount_mm": rain["mm"],
            "rainfall_accumulation_period": rain["period"],
            "rainfall_station_or_area": rain["station"],
            "event_date_if_available": inc["dates"],
            "confidence": conf,
            "notes": " ".join(x for x in [note, ("Rain: " + rain["note"]) if rain["note"] else ""] if x),
            "source_urls": inc["source_urls"],
        })
    if missing:
        raise SystemExit(f"Unclassified (incident, place) pairs: {missing}")
    OUT.parent.mkdir(exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    print(f"wrote {len(rows)} rows -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
