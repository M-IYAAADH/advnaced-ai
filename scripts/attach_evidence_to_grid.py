"""Attach positive-only flood evidence to the 200 m analysis grid (MF-21).

Inputs (unchanged): derived/male_grid_200m.geojson, derived/road_flood_inventory.csv (in_study_area == yes),
  verification/landmark_checks.csv, derived/landmark_position_check.csv,
  derived/road_flood_matched_segments.geojson,
  male_flood_ai_data/03_reviewed/events/flood_events.csv (v003).
Outputs:
  derived/grid_evidence_records.csv  one row per record, except a bounded section gives one row per cell it crosses.
    record_id, location_description, spatial_scope, evidence_class (stated_flooding / pumping_only / closure_only /
    designated), verification (verified / unverified / not_checked), location_group, cell_id, assignment_method,
    not_assigned_reason, position_offshore, section_note, event_date_if_available, incident_id, v003_event_id,
    v003_decision, v003_flag, confidence
  derived/grid_evidence.csv  one row per grid cell (all 75): cell_id, ward, land_fraction, status
    (reported_flooding > pumping_only > designated > unknown), status_note, stated_only_construction_confounded
    (yes when the only stated flooding is RF071, construction confounder E5), n_records_stated, n_dates_stated,
    n_records_pumping, n_dates_pumping, n_records_designated, n_location_groups_stated, n_location_groups_pumping,
    location_groups, routine_pump_site, whole_roads_listed (listing only), ward_mentions_v003 (listing only), has_unverified
Rules: no report means unknown, never dry. Whole-road, ward and city records never give a cell a status.
  Pumping-only records stay separate from stated flooding. Counts are reports, not frequency.
Location groups: use landmark_checks.location_group when the record is checked; otherwise places are merged when
  they share an OSM feature id or lie within 50 m, and unchecked places get a slug of their first place name.
Bounded sections (RF040, RF071): the matched-segments file holds full OSM segments, not the clipped section.
  RF071 (extent approximate): all segments tagged bounded_section_uncertain. RF040: only the 44 m clip is meant
  (data_issues C4/F4), but no clipped geometry is saved, so a 44 m window centred on the nearest segment point to the
  RF040 coordinate is used (approximate; section_note says so). Vague section RF002 has no geometry: not assigned.
v003 links: inventory incident_id matches the MFB_<incident_id> token in original_record_ids. Free-text street names
  in v003 are NOT parsed into cells (limitation); ward_mentions_v003 counts accepted rain events naming the ward.
Run from the project root: python scripts/attach_evidence_to_grid.py
"""
import csv
import json
import re
from collections import defaultdict

import numpy as np
from matplotlib.path import Path
from pyproj import Transformer

GRID = "derived/male_grid_200m.geojson"
INV = "derived/road_flood_inventory.csv"
CHECKS = "verification/landmark_checks.csv"
POS = "derived/landmark_position_check.csv"
SEGS = "derived/road_flood_matched_segments.geojson"
EVENTS = "male_flood_ai_data/03_reviewed/events/flood_events.csv"
NAME_PATTERNS = {"Henveiru": r"henveiru", "Galolhu": r"galolhu", "Maafannu": r"maafannu", "Machchangolhi": r"mach+angolhi"}
STATED = {"flooding_stated", "flooding_stated_area", "flooding_stated_waterlogged", "flooding_stated_with_dewatering",
          "photo_caption_flooding", "dewatering_at_worst_flooded_area"}
ROUTINE = {"igmh", "west_park_sto"}
to_utm = Transformer.from_crs("EPSG:4326", "EPSG:32643", always_xy=True)
rd = lambda p: list(csv.DictReader(open(p, encoding="utf-8-sig")))


E5_CONFOUNDED = {"RF071"}  # data_issues.md E5


def slug(s):
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")[:30]


def main():
    grid = json.load(open(GRID))["features"]
    cells = []
    for f in grid:
        p = f["properties"]
        cells.append((p["cell_id"], Path(np.column_stack(to_utm.transform(*zip(*f["geometry"]["coordinates"][0])))), p))
    ids = [c[0] for c in cells]
    key = {(round(c[2]["easting_min"]), round(c[2]["northing_min"])): c[0] for c in cells}

    def cell_at(lon, lat):
        x, y = to_utm.transform(lon, lat)
        return next((cid for cid, path, _ in cells if path.contains_point((x, y))), None)

    def cells_of_line(xy, lo=None, hi=None):
        pts = np.array(xy)
        d = np.r_[0, np.cumsum(np.hypot(*np.diff(pts, axis=0).T))]
        t = np.arange(d[0] if lo is None else lo, (d[-1] if hi is None else hi) + 1e-9, 2.0)
        x, y = np.interp(t, d, pts[:, 0]), np.interp(t, d, pts[:, 1])
        out = {key.get((int(np.floor(a / 200) * 200), int(np.floor(b / 200) * 200))) for a, b in zip(x, y)}
        return sorted(c for c in out if c)

    inv = [r for r in rd(INV) if r["in_study_area"] == "yes"]
    checks = {r["record_id"]: r for r in rd(CHECKS)}
    pos = {r["place"]: r for r in rd(POS)}

    # location groups for landmark places
    lm = sorted({r["location_description"] for r in inv if r["spatial_scope"] == "landmark_vicinity"})
    mism = [p for p in lm if p not in pos]
    parent = {p: p for p in lm}
    find = lambda a: a if parent[a] == a else find(parent[a])
    xy = {p: to_utm.transform(float(pos[p]["longitude"]), float(pos[p]["latitude"])) for p in lm if p in pos}
    for a in xy:
        for b in xy:
            same_feat = pos[a]["osm_feature_ids"] and pos[a]["osm_feature_ids"] == pos[b]["osm_feature_ids"]
            if same_feat or np.hypot(xy[a][0] - xy[b][0], xy[a][1] - xy[b][1]) < 50:
                parent[find(a)] = find(b)
    chk_group = {}
    for r in inv:
        if r["record_id"] in checks:
            chk_group.setdefault(find(r["location_description"]), checks[r["record_id"]]["location_group"])
    group_of = {p: chk_group.get(find(p), slug(find(p))) for p in lm}

    # v003 links
    events = rd(EVENTS)
    by_inc = defaultdict(list)
    for e in events:
        for t in e["original_record_ids"].split(";"):
            if t.startswith("MFB_"):
                by_inc[t[4:]].append(e)

    # section geometry
    segs = {f["properties"]["osm_id"]: f for f in json.load(open(SEGS))["features"]}
    section_cells, whole_roads = {}, defaultdict(set)
    for f in segs.values():
        p = f["properties"]
        kinds = p["evidence_kinds"]
        utm = np.column_stack(to_utm.transform(*zip(*f["geometry"]["coordinates"])))
        if "bounded_section_uncertain" in kinds:
            section_cells.setdefault("RF071", set()).update(cells_of_line(utm))
        if "bounded_section_partial" in kinds:  # RF040
            r = next(r for r in inv if r["record_id"] == "RF040")
            q = np.array(to_utm.transform(float(r["longitude"]), float(r["latitude"])))
            d = np.r_[0, np.cumsum(np.hypot(*np.diff(utm, axis=0).T))]
            t = np.arange(0, d[-1], 1.0)
            px, py = np.interp(t, d, utm[:, 0]), np.interp(t, d, utm[:, 1])
            c = t[np.argmin(np.hypot(px - q[0], py - q[1]))]
            section_cells["RF040"] = set(cells_of_line(utm, max(c - 22, 0), min(c + 22, d[-1])))
        if "road_named_section_unknown" in kinds:
            name = p["evidence_places"].split(" | ")[0].split(", ")[0]
            whole_roads[name].update(cells_of_line(utm))
    road_cells = defaultdict(set)  # cell -> road names (listing only)
    for n, cs in whole_roads.items():
        for c in cs:
            road_cells[c].add(n)

    rows = []
    for r in inv:
        rid, scope = r["record_id"], r["spatial_scope"]
        chk = checks.get(rid)
        if scope == "landmark_vicinity" and chk:
            ve = chk["verified_evidence"]
            if ve in STATED: cls, ver = "stated_flooding", "verified"
            elif ve == "dewatering_only": cls, ver = "pumping_only", "verified"
            elif ve.startswith("closure"): cls, ver = "closure_only", "verified"
            else: ve = None
        else:
            ve = None
        if ve is None:
            et = r["evidence_type"]
            if r["flood_status"] == "designated_flood_prone": cls = "designated"
            elif et == "dewatering_reported": cls = "pumping_only"
            else: cls = "stated_flooding"
            ver = "unverified" if chk else "not_checked"
        grp = group_of.get(r["location_description"], "") if scope == "landmark_vicinity" else ""
        if chk and not grp: grp = chk["location_group"]
        evs = by_inc.get(r["incident_id"], [])
        flag = "linked_only_coastal_or_uncertain" if evs and all(e["decision"] != "accepted_reported_rain_event" for e in evs) else ""
        base = dict(record_id=rid, location_description=r["location_description"], spatial_scope=scope, evidence_class=cls,
                    verification=ver, location_group=grp, cell_id="", assignment_method="", not_assigned_reason="",
                    position_offshore="no", section_note="", event_date_if_available=r["event_date_if_available"],
                    incident_id=r["incident_id"], v003_event_id=";".join(e["event_id"] for e in evs) or "unknown",
                    v003_decision=";".join(e["decision"] for e in evs) or "unknown", v003_flag=flag, confidence=r["confidence"])
        if scope == "landmark_vicinity":
            p = pos.get(r["location_description"])
            lon, lat = (float(p["longitude"]), float(p["latitude"])) if p else (None, None)
            if p and p["result"].startswith("excluded"): base["position_offshore"] = "yes"
            c = cell_at(lon, lat) if p else None
            if c: rows.append({**base, "cell_id": c, "assignment_method": "point_in_cell"})
            else: rows.append({**base, "assignment_method": "not_in_any_cell",
                               "not_assigned_reason": "landmark point falls in no grid cell" if p else "no position-check row"})
        elif rid in section_cells:
            note = "approximate extent (44 m window at nearest point to compiler coordinate; clip not saved)" if rid == "RF040" \
                else "all OSM segments tagged bounded_section_uncertain; compiler extent approximate"
            for c in sorted(section_cells[rid]):
                rows.append({**base, "cell_id": c, "assignment_method": "section_line_crosses", "section_note": note})
        else:
            m, why = {"ward": ("not_assigned_ward", "ward-level mention; not spread to cells"),
                      "city": ("not_assigned_city", "city-level mention; not spread to cells")}.get(
                scope, ("not_assigned_whole_road", "whole-road or vague-section mention; extent within road unknown"))
            rows.append({**base, "assignment_method": m, "not_assigned_reason": why})

    # per-cell
    wmen = {w: sum(1 for e in events if e["decision"] == "accepted_reported_rain_event" and
                   re.search(pat, (e["location_as_reported"] + " " + e["notes"]).lower())) for w, pat in NAME_PATTERNS.items()}
    out = []
    for cid, _, p in cells:
        rs = [r for r in rows if r["cell_id"] == cid]
        def sel(cls): return [r for r in rs if r["evidence_class"] == cls]
        dts = lambda L: len({r["event_date_if_available"] for r in L} - {"", "unknown"})
        grps = lambda L: {r["location_group"] for r in L if r["location_group"]}
        st, pu, de, cl = sel("stated_flooding"), sel("pumping_only"), sel("designated"), sel("closure_only")
        # E5: RF071 (Boduthakurufaanu section, 30 Jul 2026) was blamed on pumps not yet commissioned on a rebuilt road,
        # and its extent is approximate; flag cells whose stated flooding rests only on it.
        e5_only = "yes" if st and all(r["record_id"] in E5_CONFOUNDED for r in st) else "no"
        status = "reported_flooding" if st else "pumping_only" if pu else "designated" if de else "unknown"
        out.append(dict(cell_id=cid, ward=p["ward"], land_fraction=p["land_fraction"], status=status,
                        status_note="only closure records (flooding not stated at the place)" if cl and status == "unknown" else "",
                        n_records_stated=len(st), n_dates_stated=dts(st), n_records_pumping=len(pu), n_dates_pumping=dts(pu),
                        n_records_designated=len(de), n_location_groups_stated=len(grps(st)), n_location_groups_pumping=len(grps(pu)),
                        location_groups=";".join(sorted(grps(rs))),
                        routine_pump_site="yes" if any(r["location_group"] in ROUTINE for r in pu) else "no",
                        whole_roads_listed=";".join(sorted(road_cells.get(cid, []))),
                        ward_mentions_v003=wmen.get(p["ward"], "unknown"),
                        stated_only_construction_confounded=e5_only,
                        has_unverified="yes" if any(r["verification"] == "unverified" for r in rs) else "no"))
    for path, data in (("derived/grid_evidence_records.csv", rows), ("derived/grid_evidence.csv", out)):
        with open(path, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(data[0])); w.writeheader(); w.writerows(data)

    # self-check
    assert {r["record_id"] for r in rows} == {r["record_id"] for r in inv}
    assert all(r["cell_id"] or r["not_assigned_reason"] for r in rows)
    n_sec = sum(len(v) for v in section_cells.values())
    assert len(rows) == len(inv) - len(section_cells) + n_sec
    assert len(out) == 75 and [o["cell_id"] for o in out] == ids and len(set(ids)) == 75
    assert all(r["spatial_scope"] in ("landmark_vicinity", "road_section_bounded") for r in rows if r["cell_id"])
    assert {o["status"] for o in out} <= {"reported_flooding", "pumping_only", "designated", "unknown"}
    for o in out:
        rs = [r for r in rows if r["cell_id"] == o["cell_id"]]
        assert o["n_records_stated"] == sum(r["evidence_class"] == "stated_flooding" for r in rs)
        assert o["n_records_pumping"] == sum(r["evidence_class"] == "pumping_only" for r in rs)
        assert o["n_records_designated"] == sum(r["evidence_class"] == "designated" for r in rs)
    assert all(o["stated_only_construction_confounded"] == "no" or o["status"] == "reported_flooding" for o in out)
    print("join mismatches (inventory place not in position check):", mism)
    print("status counts:", {s: sum(o["status"] == s for o in out) for s in ("reported_flooding", "pumping_only", "designated", "unknown")})
    print("method counts:", {m: sum(r["assignment_method"] == m for r in rows) for m in sorted({r["assignment_method"] for r in rows})})
    print("section cells:", {k: sorted(v) for k, v in section_cells.items()})
    for r in [x for x in rows if x["record_id"] in ("RF004", "RF038", "RF049")]:
        i = next(x for x in inv if x["record_id"] == r["record_id"])
        print("spot", r["record_id"], pos[i["location_description"]]["longitude"], pos[i["location_description"]]["latitude"], r["cell_id"])
    print("self-check passed")


if __name__ == "__main__":
    main()
