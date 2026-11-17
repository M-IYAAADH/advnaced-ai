"""MF-15: review the unnamed OSM segments that the compiler's road lines cover.

The compiler's lines for Majeedhee, Ameenee and Boduthakurufaanu Magu overlap
8 OSM segments that carry no name (issue F3 in data_issues.md). This script
recomputes the geometry checks for each one and records whether it is part of
the named road, with the reason.

Output (derived/, raw inputs untouched):
  unnamed_segment_review.csv   one row per unnamed segment

Rules applied, in order (the reason column says which one decided):
  1. Duplicate geometry: a segment lying within 2 m of the named road's
     centreline for 40 m or more duplicates it. It is not a separate part of
     the road; counting it would double the named length.
  2. Pedestrian feature (footway, steps): pavement, crossing or steps, not
     the road carriageway.
  3. Perpendicular stub: shorter than 10 m, more than 60 degrees off the road's
     bearing and with one end on it. An access or crossing connector.
  Anything else would be marked for manual review (none at present).

Decisions use OSM geometry only; nothing here was checked on imagery.
Run from the project root, after match_road_flood_records.py.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

from match_road_flood_records import (DHIVEHI_ALIAS, KX, KY, LAT0, LON0, OSM, ROOT, SRC_GEO,
                                      densify, length, parts, pt_to_lines)

OUT = ROOT / "derived/unnamed_segment_review.csv"
ROADS = ["Majeedhee Magu", "Ameenee Magu", "Boduthakurufaanu Magu"]
COVER_TOL_M, COVER_FRAC = 3.0, 0.5  # same overlap test as match_road_flood_records.geom_overlap
DUP_TOL_M, DUP_MIN_M = 2.0, 40.0
STUB_MAX_M, STUB_MIN_ANGLE = 10.0, 60.0
PEDESTRIAN = {"footway", "steps", "path", "pedestrian"}


def bearing(L):
    d = L[-1] - L[0]
    return float(np.degrees(np.arctan2(d[0], d[1])) % 180)


def angle_diff(a, b):
    d = abs(a - b) % 180
    return min(d, 180 - d)


def main():
    feats = json.load(open(OSM, encoding="utf-8"))["features"]
    seg = []
    for f in feats:
        p = f["properties"]
        ls = parts(f["geometry"])
        seg.append(dict(osm_id=str(p["osm_id"]), name=p["name"] or "", fclass=p["fclass"],
                        oneway=p["oneway"], lines=ls, len_m=length(ls)))
    src = {f["properties"]["name"]: f for f in json.load(open(SRC_GEO, encoding="utf-8"))["features"]}

    rows = []
    for road in ROADS:
        osm_name = DHIVEHI_ALIAS[road.lower()]
        named = [s for s in seg if s["name"] == osm_name]
        named_lines = [L for s in named for L in s["lines"]]
        comp = parts(src[road]["geometry"])
        for s in seg:
            if s["name"]:
                continue
            # Coverage uses exactly the match script's sampling (2 m densify per line) so the
            # same segments are selected; the other checks use 1 m steps.
            cover = float((pt_to_lines(np.vstack([densify(L) for L in s["lines"]]), comp) < COVER_TOL_M).mean())
            D = np.vstack([densify(L, 1.0) for L in s["lines"]])
            if cover < COVER_FRAC:
                continue
            d_named = pt_to_lines(D, named_lines)
            on_centreline_m = float((d_named[1:] < DUP_TOL_M).sum())  # ~1 m steps
            end_gaps = [float(pt_to_lines(e[None], named_lines)[0])
                        for L in s["lines"] for e in (L[0], L[-1])]
            nearest = min(named, key=lambda n: pt_to_lines(D, n["lines"]).mean())
            ang = angle_diff(bearing(max(s["lines"], key=len)), bearing(max(nearest["lines"], key=len)))
            touching = sorted({(o["name"] or f"(unnamed {o['fclass']})") for o in seg if o["osm_id"] != s["osm_id"]
                               for L in s["lines"] for e in (L[0], L[-1])
                               if pt_to_lines(e[None], o["lines"])[0] < 2.0})
            c = np.vstack(s["lines"]).mean(0)

            if on_centreline_m >= DUP_MIN_M:
                part, rule = "no", "duplicate_geometry"
                reason = (f"{on_centreline_m:.0f} m of it lies within {DUP_TOL_M:.0f} m of the {road} centreline "
                          f"(OSM segment {nearest['osm_id']}), so it duplicates the named road there; the rest "
                          f"({s['len_m'] - on_centreline_m:.0f} m) links to {', '.join(t for t in touching if t != osm_name) or 'nothing'}. "
                          "Exclude from the segment table to avoid counting road length twice. Confirm on imagery.")
            elif s["fclass"] in PEDESTRIAN:
                part, rule = "no", "pedestrian_feature"
                reason = (f"{s['fclass']}, {s['len_m']:.1f} m, {ang:.0f} degrees to the road: a pavement, crossing "
                          "or steps feature, not the carriageway.")
            elif s["len_m"] < STUB_MAX_M and ang > STUB_MIN_ANGLE and min(end_gaps) < 1.0:
                part, rule = "no", "perpendicular_stub"
                reason = (f"{s['fclass']}, {s['len_m']:.1f} m, {ang:.0f} degrees to the road with one end on it: "
                          "an access or crossing connector.")
            else:
                part, rule, reason = "needs_manual_review", "none", "No rule applies."
            if s["fclass"] in PEDESTRIAN and s["len_m"] < STUB_MAX_M and ang > STUB_MIN_ANGLE:
                reason += " Also a short perpendicular stub."

            rows.append(dict(
                osm_id=s["osm_id"], beside_road=road, osm_road_name=osm_name, fclass=s["fclass"],
                oneway=s["oneway"], length_m=round(s["len_m"], 1),
                share_within_3m_of_compiler_line=round(cover, 2),
                length_on_named_centreline_m=round(on_centreline_m),
                angle_to_named_road_deg=round(ang),
                end_gaps_to_named_road_m=";".join(f"{g:.1f}" for g in end_gaps),
                touches=";".join(touching),
                centre_lat=round(c[1] / KY + LAT0, 6), centre_lon=round(c[0] / KX + LON0, 6),
                part_of_named_road=part, rule=rule, reason=reason,
                checked_on_imagery="no"))

    rows.sort(key=lambda r: (ROADS.index(r["beside_road"]), r["osm_id"]))
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {len(rows)} rows -> {OUT.relative_to(ROOT).as_posix()}")
    for r in rows:
        print(f"  {r['osm_id']:>11}  {r['beside_road']:<22} {r['fclass']:<12} {r['length_m']:>6} m  "
              f"{r['part_of_named_road']:<5} {r['rule']}")


if __name__ == "__main__":
    main()
