"""MF-16 (part): cross-check the compiler's landmark points against named OSM features.

For each Malé landmark in the places file, this finds the OSM building or
land-use feature with the same identity (a short manual table, below), measures
the distance from the compiler's point to that feature's footprint (0 if the
point is inside it), and flags points outside the OneMap Malé polygon.

This is NOT the imagery check the task asks for. It confirms points that sit on
or next to the named OSM feature, and lists the points that still need imagery
because OSM has no matching feature. No coordinate is moved here.

Output (derived/, raw inputs untouched):
  landmark_position_check.csv   one row per Malé landmark

Run from the project root.
"""
from __future__ import annotations

import csv
import json

import numpy as np

from match_road_flood_records import EXCLUDED_LANDMARKS, POSITION_OVERRIDES, apply_position_overrides, BOUNDARY, KX, KY, LAT0, LON0, PLACES, ROOT, pt_to_lines, xy

BUILDINGS = ROOT / "Male_Flood_Data_Starter_Pack/mapping/male_osm_buildings.geojson"
LANDUSE = ROOT / "Male_Flood_Data_Starter_Pack/mapping/male_osm_landuse.geojson"
OUT = ROOT / "derived/landmark_position_check.csv"
NEAR_M = 30.0  # point within this distance of the footprint counts as consistent

# Landmark (places-file name) -> OSM feature id(s) judged to be the same place, with the reason.
# Only unambiguous identities are listed; anything else goes to the imagery list.
OSM_IDENTITY = {
    "IGMH area (Indira Gandhi Memorial Hospital)": (["151403710"], "OSM building 'Indira Gandhi Memorial Hospital'"),
    "West Park area": (["61881622"], "OSM park 'West Park'"),
    "Maafannu (Villimalé) Ferry Terminal": (["108758609"], "OSM building 'MTCC Vilingilli Ferry Terminal' (Villimalé = Vilingili)"),
    "King Salman Mosque area": (["959150179"], "OSM mosque named in Dhivehi 'Salman Rasgefaanuge Miskiy' (King Salman Mosque)"),
    "Kudakudhinge Bageecha (children's park, Ameenee Magu)": (["91986115"], "OSM park 'Kudakudhinge Bageecha'"),
    "Dhiraagu head office area": (["795286458"], "OSM building 'Dhiraagu Head Office'"),
    "Voice of Maldives area": (["1211931510"], "OSM building 'Voice of Maldives'"),
    "Dharubaaruge area": (["108762208"], "OSM building 'Dharubaaruge'"),
    # Compiler point kept (MF-16 move reverted 23 Nov 2026, see POSITION_OVERRIDES). OSM names this building only 'STO';
    # that it is the flour warehouse rests on the reports pairing it with West Park and IGMH, so it stays approximate.
    "STO flour warehouse area": (["522153523"], "OSM building 'STO' by West Park (flour warehouse identification not confirmed in OSM)"),
}
# MF-16 (17 Nov 2026): places missing from the clipped starter-pack layers, checked against
# the full OSM database via Nominatim search. Google Maps could not be read by script
# (it needs a JavaScript browser). Values: (OSM object, OSM name and tag, lat, lon).
OSM_FULL_CHECK = {
    "Ekuveni running track": ("node 1247058236", "Ekuveni (leisure=sports_centre)", 4.1700889, 73.5071790),
    "Henveiru Ground (stadium)": ("way 108650593", "Henveiru Stadium (leisure=pitch), centroid", 4.1749828, 73.5169041),
    "Pizza Buona area": ("node 11449179169", "Pizza Buona (amenity=restaurant), Majeedhee Magu", 4.1745909, 73.5148509),
    "Maldives Polytechnic area": ("node 5599539381", "Maldives Polytechnic (amenity=college)", 4.1704908, 73.5103677),
}

NOT_SAME = {}


def rings(geom):
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    return [xy(p[0]) for p in polys]


def inside(P, ring):
    x, y = P
    xs, ys = ring[:, 0], ring[:, 1]
    c = False
    for i in range(len(ring) - 1):
        if (ys[i] > y) != (ys[i + 1] > y) and x < (xs[i + 1] - xs[i]) * (y - ys[i]) / (ys[i + 1] - ys[i]) + xs[i]:
            c = not c
    return c


def main():
    feats = {}
    for path in (BUILDINGS, LANDUSE):
        for f in json.load(open(path, encoding="utf-8"))["features"]:
            feats[str(f["properties"]["osm_id"])] = f
    onemap = rings(json.load(open(BOUNDARY, encoding="utf-8"))["features"][0]["geometry"])

    with open(PLACES, encoding="utf-8-sig") as fh:
        places = [(i, r) for i, r in enumerate(apply_position_overrides(list(csv.DictReader(fh))), start=2)
                  if r["type"] == "landmark" and r["island"] == "Malé"]

    rows = []
    for i, p in places:
        P = xy([[float(p["longitude"]), float(p["latitude"])]])[0]
        in_onemap = any(inside(P, R) for R in onemap)
        coast_m = min(float(pt_to_lines(P[None], [R])[0]) for R in onemap)
        approx = "approximate" in p["note"].lower()
        row = dict(place=p["name"], places_file_row=i, latitude=p["latitude"], longitude=p["longitude"],
                   compiler_marked_approximate="yes" if approx else "no",
                   inside_onemap_polygon="yes" if in_onemap else "no",
                   distance_to_onemap_coastline_m=round(coast_m, 1),
                   osm_feature_ids="", osm_feature="", distance_to_osm_footprint_m="",
                   result="", action_needed="", position_changed="no",
                   compiler_latitude=p.get("orig_latitude", p["latitude"]), compiler_longitude=p.get("orig_longitude", p["longitude"]),
                   position_change_source="", position_change_reason="")
        if p["name"] in POSITION_OVERRIDES:
            _, _, src, why = POSITION_OVERRIDES[p["name"]]
            row.update(position_changed="yes", position_change_source=src, position_change_reason=why)
        if p["name"] in OSM_IDENTITY:
            ids, why = OSM_IDENTITY[p["name"]]
            d = []
            for oid in ids:
                R = rings(feats[oid]["geometry"])
                d.append(0.0 if any(inside(P, r) for r in R) else min(float(pt_to_lines(P[None], [r])[0]) for r in R))
            dist = min(d)
            row.update(osm_feature_ids=";".join(ids), osm_feature=why, distance_to_osm_footprint_m=round(dist, 1))
            if dist <= NEAR_M:
                row.update(result="consistent_with_osm_feature",
                           action_needed="none" if in_onemap else "imagery: point is off the OneMap polygon")
            else:
                row.update(result="far_from_osm_feature", action_needed=f"imagery: point is {dist:.0f} m from the named OSM feature")
        elif p["name"] in OSM_FULL_CHECK:
            oid, why, la, lo = OSM_FULL_CHECK[p["name"]]
            dist = float(np.hypot(*(P - xy([[lo, la]])[0])))
            row.update(osm_feature_ids=oid, osm_feature=why + " [full OSM, Nominatim]",
                       distance_to_osm_footprint_m=round(dist, 1))
            row.update(result="consistent_with_osm_feature", action_needed="none") if dist <= NEAR_M else                 row.update(result="far_from_osm_feature", action_needed=f"imagery: point is {dist:.0f} m from the OSM object")
        elif p["name"] in EXCLUDED_LANDMARKS:
            row.update(result="excluded_not_road_location", osm_feature=EXCLUDED_LANDMARKS[p["name"]],
                       action_needed="none: removed from matching and map (MF-16)")
        else:
            row.update(result="no_osm_feature",
                       osm_feature=NOT_SAME.get(p["name"], "No OSM building or land-use feature with this name."),
                       action_needed="imagery: no OSM reference to check against")
        if approx and row["action_needed"] == "none" and row["result"] != "consistent_with_osm_feature":
            row["action_needed"] = "imagery: compiler marks the position approximate"
        rows.append(row)

    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {len(rows)} rows -> {OUT.relative_to(ROOT).as_posix()}")
    for r in rows:
        print(f"  {r['place'][:38]:<38} approx={r['compiler_marked_approximate']:<3} onemap={r['inside_onemap_polygon']:<3} "
              f"osm_d={str(r['distance_to_osm_footprint_m']):>5}  {r['result']:<28} {r['action_needed']}")


if __name__ == "__main__":
    main()
