"""Match road-flood places to the downloaded OSM road layer.

Outputs (derived/, raw inputs untouched):
  road_match_review.csv               one row per named place, with match status
  road_flood_matched_segments.geojson OSM segments linked to flood evidence (QGIS)
  road_flood_evidence_map.png         simple map

Matching rules
  * Road names are compared on a spelling key (no apostrophes/spaces, doubled
    letters collapsed) plus a short, documented Dhivehi alias table, because
    several Malé roads carry only a Dhivehi `name` in this OSM extract.
  * Name matches are cross-checked against the compiler's own line geometry in
    flood_locations_greater_male.geojson (which was traced from OSM).
  * A whole-road match means "this road was named in a report"; it does NOT
    label every segment as flooded.
  * Landmarks and wards are never assigned to a road. Nearby roads are listed as
    candidates only.

Distances use a local equirectangular projection centred on Malé (error well
under 1 % over the island's ~2 km extent). Run from the project root.
"""
from __future__ import annotations

import csv
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OSM = ROOT / "Male_Flood_Data_Starter_Pack/mapping/male_osm_roads.geojson"
BOUNDARY = ROOT / "Male_Flood_Data_Starter_Pack/boundary/OneMap_Male_Island.geojson"
SRC_GEO = ROOT / "male-flood-basis/data/flood_locations_greater_male.geojson"
PLACES = ROOT / "male-flood-basis/data/flooded_roads_and_places_greater_male.csv"
INV = ROOT / "derived/road_flood_inventory.csv"
OUT_CSV = ROOT / "derived/road_match_review.csv"
OUT_GEO = ROOT / "derived/road_flood_matched_segments.geojson"
OUT_PNG = ROOT / "derived/road_flood_evidence_map.png"

LAT0, LON0 = 4.175, 73.5
KX, KY = 111320 * np.cos(np.radians(LAT0)), 110574.0

# English name in reports -> OSM Dhivehi `name` (manual transliteration; each
# is also checked against the compiler's geometry below).
DHIVEHI_ALIAS = {
    "majeedhee magu": "މަޖީދީ މަގު",
    "ameenee magu": "އަމީނީ މަގު",
    "boduthakurufaanu magu": "ބޮޑުތަކުރުފާނު މަގު",
}
# Similar-looking OSM names that are different streets (do not match).
FALSE_FRIENDS = {"ameenee magu": ["Amenee Goalhi"], "rahdhebai magu": ["Rah Dhebai Hingun"]}


def key(name: str) -> str:
    n = name.split(",")[0]
    n = re.sub(r"\(.*?\)", "", n)
    n = unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode().lower()
    n = n.replace("higun", "hingun")
    n = re.sub(r"[^a-z]", "", n)
    return re.sub(r"(.)\1+", r"\1", n)


def xy(coords):
    c = np.asarray(coords, float)[:, :2]
    return np.c_[(c[:, 0] - LON0) * KX, (c[:, 1] - LAT0) * KY]


def parts(geom):
    if geom["type"] == "LineString":
        return [xy(geom["coordinates"])]
    if geom["type"] == "MultiLineString":
        return [xy(p) for p in geom["coordinates"]]
    if geom["type"] == "Point":
        return [xy([geom["coordinates"]])]
    raise ValueError(geom["type"])


def pt_to_lines(P, lines):
    d = np.full(len(P), np.inf)
    for L in lines:
        if len(L) == 1:
            d = np.minimum(d, np.hypot(*(P - L[0]).T)); continue
        for a, b in zip(L[:-1], L[1:]):
            ab = b - a
            t = np.clip(((P - a) @ ab) / max(ab @ ab, 1e-9), 0, 1)
            d = np.minimum(d, np.hypot(*(P - (a + t[:, None] * ab)).T))
    return d


def length(lines):
    return float(sum(np.hypot(*np.diff(L, axis=0).T).sum() for L in lines if len(L) > 1))


def densify(L, step=2.0):
    out = [L[0]]
    for a, b in zip(L[:-1], L[1:]):
        n = max(int(np.hypot(*(b - a)) // step), 1)
        out += [a + (b - a) * k / n for k in range(1, n + 1)]
    return np.array(out)


def main():
    osm = json.load(open(OSM, encoding="utf-8"))["features"]
    seg = []
    for f in osm:
        p = f["properties"]
        ls = parts(f["geometry"])
        seg.append(dict(osm_id=str(p["osm_id"]), name=p["name"] or "", fclass=p["fclass"],
                        lines=ls, dense=np.vstack([densify(L) for L in ls]), len_m=length(ls), feat=f))
    total_len = sum(s["len_m"] for s in seg)
    by_key = defaultdict(list)
    for s in seg:
        if s["name"]:
            by_key[key(s["name"])].append(s)
            by_key[s["name"]].append(s)  # exact (Dhivehi) lookup

    src = {f["properties"]["name"]: f for f in json.load(open(SRC_GEO, encoding="utf-8"))["features"]}
    with open(PLACES, encoding="utf-8-sig") as fh:
        places = list(csv.DictReader(fh))
    with open(INV, encoding="utf-8") as fh:
        inv = list(csv.DictReader(fh))
    recs = defaultdict(list)
    for r in inv:
        recs[r["location_description"]].append(r)

    def geom_overlap(name, tol=3.0, frac=0.5):
        """OSM segments with >= frac of densified length within tol m of the compiler's line."""
        f = src.get(name)
        if not f or f["geometry"]["type"] == "Point":
            return set()
        ls = parts(f["geometry"])
        return {s["osm_id"] for s in seg if (pt_to_lines(s["dense"], ls) < tol).mean() >= frac}

    alias = {key(k): v for k, v in DHIVEHI_ALIAS.items()}
    false_friends = {key(k): v for k, v in FALSE_FRIENDS.items()}

    def named(rname):
        k = key(rname)
        hits = list(by_key.get(k, []))
        if k in alias:
            hits += by_key.get(alias[k], [])
        return {s["osm_id"]: s for s in hits}

    segid = {s["osm_id"]: s for s in seg}
    seg_evidence = defaultdict(list)  # osm_id -> list of (place, status, part)
    rows = []

    for i, p in enumerate(places, start=2):
        name, ptype, island = p["name"], p["type"], p["island"]
        rids = [r["record_id"] for r in recs.get(name, [])]
        n_inc = len({r["incident_id"] for r in recs.get(name, [])})
        row = dict(place=name, place_type=ptype, island=island, places_file_row=i,
                   inventory_record_ids=";".join(rids), n_incidents_in_inventory=n_inc,
                   match_status="", osm_ids="", osm_names="", n_osm_segments=0,
                   matched_length_m="", compiler_geometry_agreement="", candidate_nearby_roads="",
                   match_method="", notes="")
        base = name.split(",")[0]
        if island != "Malé":
            row.update(match_status="out_of_study_area", match_method="island field",
                       notes="Not on Malé island proper; OSM extract is clipped to Malé.")
        elif ptype == "road" and "," not in name:
            hits = named(base)
            geo = geom_overlap(name)
            row["osm_ids"] = ";".join(sorted(hits))
            row["osm_names"] = ";".join(sorted({h["name"] for h in hits.values()}))
            row["n_osm_segments"] = len(hits)
            row["matched_length_m"] = round(sum(h["len_m"] for h in hits.values()))
            only_geo = geo - set(hits)
            row["compiler_geometry_agreement"] = (
                "no compiler geometry" if not src.get(name) else
                f"{len(set(hits) & geo)}/{len(hits)} name-matched segments overlap compiler line; "
                f"{len(only_geo)} extra overlapping OSM segments "
                f"({', '.join(sorted({segid[g]['name'] or '(unnamed)' for g in only_geo})) or 'none'})")
            ff = [x for x in false_friends.get(key(base), []) if by_key.get(x)]
            method = "spelling key" + (" + Dhivehi alias" if key(base) in alias else "")
            if not hits:
                row.update(match_status="unmatched", match_method=method)
            elif base == "Rahdhebai Magu":
                row.update(match_status="uncertain_probable_name_match", match_method=method + " (spacing variant 'Rah Dhebai')",
                           notes="Places file says the road is 'not in the base map data', but this OSM extract has 'Rah Dhebai Magu'. "
                                 "No source coordinates to confirm. Different street 'Rah Dhebai Hingun' also exists.")
            else:
                row.update(match_status="confident_whole_road_name", match_method=method,
                           notes="Report names the road without a section: road-level evidence only; do not label every segment flooded.")
            if ff:
                row["notes"] += f" Not matched to similarly spelled different street(s): {', '.join(ff)}."
            if only_geo:
                row["notes"] += " Compiler line also covers unnamed OSM segments; reviewed in unnamed_segment_review.csv (MF-15): none is part of the named carriageway, so they stay unmatched."
            for h in hits:
                seg_evidence[h].append((base, "road_named_section_unknown" if row["match_status"].startswith("confident") else "road_named_uncertain_match"))
        elif ptype == "road":  # bounded sections
            if base == "Majeedhee Magu":
                maj = named("Majeedhee Magu")
                ends = []
                for cross in ("Dhanburuh Magu", "Nikagas Magu"):
                    cs = named(cross)
                    best = None
                    for c in cs.values():
                        for m in maj.values():
                            d = pt_to_lines(c["dense"], m["lines"])
                            j = int(np.argmin(d))
                            if best is None or d[j] < best[0]:
                                best = (d[j], c["dense"][j], cross)
                    ends.append(best)
                xs = sorted(e[1][0] for e in ends)
                SECTION_XRANGE[:] = xs
                sec_len, sec_ids = 0.0, []
                for oid, m in maj.items():
                    for L in m["lines"]:
                        D = densify(L, 0.5)
                        inside = (D[:, 0] >= xs[0]) & (D[:, 0] <= xs[1])
                        if inside.any():
                            sec_len += np.hypot(*np.diff(D, axis=0).T)[inside[1:] & inside[:-1]].sum()
                            sec_ids.append(oid)
                sec_ids = sorted(set(sec_ids))
                comp = length(parts(src[name]["geometry"])) if name in src else None
                row.update(match_status="confident_section_partial_segments",
                           osm_ids=";".join(sec_ids), osm_names="މަޖީދީ މަގު", n_osm_segments=len(sec_ids),
                           matched_length_m=round(sec_len),
                           compiler_geometry_agreement=f"compiler section length {comp:.0f} m vs clipped {sec_len:.0f} m" if comp else "",
                           match_method="Dhivehi alias + clip between nearest points to Dhanburuh Magu and Nikagas Magu "
                                        f"(gaps {ends[0][0]:.1f} m, {ends[1][0]:.1f} m)",
                           notes="One block between the two junctions; only part of the listed OSM segment lies in it, so split before labelling. "
                                 "The compiler's line runs on to the next OSM node west of the Nikagas Magu junction, beyond the stated section; the clipped extent is used here.")
                for o in sec_ids:
                    seg_evidence[o].append((name, "bounded_section_partial"))
            else:  # Boduthakurufaanu section with landmark ends
                geo = geom_overlap(name, tol=3.0, frac=0.3)
                comp = length(parts(src[name]["geometry"])) if name in src else None
                row.update(match_status="uncertain_section_extent",
                           osm_ids=";".join(sorted(geo)),
                           osm_names=";".join(sorted({segid[g]['name'] or '(unnamed)' for g in geo})),
                           n_osm_segments=len(geo),
                           compiler_geometry_agreement=f"compiler section length {comp:.0f} m" if comp else "",
                           match_method="overlap with compiler's approximate section line (>=30% within 3 m)",
                           notes="Section ends are landmarks (ferry terminal, jetty); compiler marks extent approximate. "
                                 "Flooding attributed to pumps not yet commissioned on a rebuilt road.")
                for o in sorted(geo):
                    seg_evidence[o].append((name, "bounded_section_uncertain"))
        else:  # landmark / ward / city
            if p["longitude"] and ptype == "landmark":
                P = xy([[float(p["longitude"]), float(p["latitude"])]])
                cands = []
                for s in seg:
                    if not s["name"]:
                        continue
                    d = float(pt_to_lines(P, s["lines"])[0])
                    if d <= 50:
                        cands.append((d, s["name"]))
                best = {}
                for d, n in sorted(cands):
                    best.setdefault(n, d)
                row["candidate_nearby_roads"] = "; ".join(f"{n} ({d:.0f} m)" for n, d in list(best.items())[:5])
            if ptype == "landmark":
                row.update(match_status="uncertain_landmark_not_assigned",
                           match_method="named OSM roads within 50 m of landmark point (candidates only)",
                           notes="Report names a landmark, not a road. Candidate roads are not labelled flooded.")
            else:
                row.update(match_status="unmatched_area_level", match_method="none",
                           notes="Ward/city-level report; no street can be identified.")
        rows.append(row)

    OUT_CSV.parent.mkdir(exist_ok=True)
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)

    feats = []
    for oid, ev in seg_evidence.items():
        s = segid[oid]
        props = dict(osm_id=oid, osm_name=s["name"], fclass=s["fclass"], length_m=round(s["len_m"], 1),
                     evidence_places=" | ".join(sorted({e[0] for e in ev})),
                     evidence_kinds=" | ".join(sorted({e[1] for e in ev})),
                     label_note="Road named in flood report(s); flooded extent within this segment unknown. Not a flooded/dry label.")
        feats.append(dict(type="Feature", properties=props, geometry=s["feat"]["geometry"]))
    json.dump(dict(type="FeatureCollection", features=feats), open(OUT_GEO, "w", encoding="utf-8"), ensure_ascii=False)

    # --- summary for the report
    named_len = sum(segid[o]["len_m"] for o in seg_evidence)
    print(f"OSM network: {len(seg)} features, {total_len/1000:.1f} km; "
          f"linked to evidence: {len(seg_evidence)} features, {named_len/1000:.2f} km ({100*named_len/total_len:.0f}%)")
    for r in rows:
        print(f"{r['match_status']:36s} {r['n_osm_segments']:>3} {str(r['matched_length_m']):>6}  {r['place'][:60]}")
    draw(seg, seg_evidence, places, rows)


def draw(seg, seg_evidence, places, rows):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ring = xy(json.load(open(BOUNDARY, encoding="utf-8"))["features"][0]["geometry"]["coordinates"][0])
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=150)
    ax.fill(*ring.T, color="#f3f1ec", zorder=0)
    ax.plot(*ring.T, color="#9a968c", lw=0.8, zorder=1)
    for s in seg:
        for L in s["lines"]:
            ax.plot(*L.T, color="#c9c5bb", lw=0.6, zorder=2)
    style = {
        "road_named_section_unknown": dict(color="#2b6cb0", lw=2.2, label="Road named in report(s), section unknown"),
        "road_named_uncertain_match": dict(color="#2b6cb0", lw=2.2, ls=(0, (2, 1.5)), label="Road named, uncertain OSM match (Rah Dhebai Magu)"),
        "bounded_section_partial": dict(color="#c0392b", lw=4.0, label="Bounded section (council-named stretch)"),
        "bounded_section_uncertain": dict(color="#e67e22", lw=4.0, label="Bounded section, approximate extent"),
    }
    seen = set()
    # draw whole roads first, sections on top
    order = ["road_named_section_unknown", "road_named_uncertain_match", "bounded_section_uncertain", "bounded_section_partial"]
    maj_sec = next(r for r in rows if r["place"].startswith("Majeedhee Magu,"))
    for kind in order:
        for oid, ev in seg_evidence.items():
            if kind not in {e[1] for e in ev}:
                continue
            st = dict(style[kind]); lab = st.pop("label")
            for L in segid_lookup(seg)[oid]["lines"]:
                if kind == "bounded_section_partial":
                    L = clip_x(L, maj_sec)
                    if L is None:
                        continue
                ax.plot(*L.T, zorder=4, solid_capstyle="round", label=None if kind in seen else lab, **st)
                seen.add(kind)
    first = {"landmark": True, "area": True}
    for p in places:
        if p["island"] != "Malé" or not p["longitude"] or p["type"] == "road":
            continue
        P = xy([[float(p["longitude"]), float(p["latitude"])]])[0]
        n = int(p["times_reported"])
        if p["type"] == "landmark":
            ax.scatter(*P, s=25 + 18 * n, facecolor="#6b46c1", edgecolor="white", lw=0.8, zorder=5,
                       label="Landmark named in report(s) (size = incidents)" if first["landmark"] else None)
            first["landmark"] = False
            label = "Villimalé Ferry Terminal" if "Ferry Terminal" in p["name"] else p["name"].split(" (")[0].replace(" area", "")
            ax.annotate(label, P, xytext=(4, 4), textcoords="offset points", fontsize=6.5, color="#3b2a6b", zorder=6)
        else:
            ax.scatter(*P, s=60, marker="s", facecolor="none", edgecolor="#555", lw=1, zorder=5,
                       label="Ward/city report, street unknown (indicative point)" if first["area"] else None)
            first["area"] = False
    ax.set_aspect("equal"); ax.set_axis_off()
    ax.set_title("Malé island: roads and places named in rain-flood reports, Dec 2021 to Oct 2026\n"
                 "Evidence of reported flooding only. Grey roads are UNKNOWN, not dry.", fontsize=10, loc="left")
    ax.legend(loc="lower left", fontsize=7, frameon=True, bbox_to_anchor=(0, -0.02))
    ax.text(1, -0.02, "Sources: male-flood-basis compilation of news/agency reports (unverified); OSM roads © OpenStreetMap contributors (ODbL); OneMap boundary.\n"
                      "Local metre projection centred on 4.175°N 73.5°E.", transform=ax.transAxes, ha="right", va="top", fontsize=6, color="#555")
    fig.tight_layout(); fig.savefig(OUT_PNG); plt.close(fig)


_SEGID = {}
def segid_lookup(seg):
    if not _SEGID:
        _SEGID.update({s["osm_id"]: s for s in seg})
    return _SEGID


SECTION_XRANGE: list[float] = []


def clip_x(L, row):
    """Keep the part of a Majeedhee polyline between the two cross streets (x-range set in main)."""
    if not SECTION_XRANGE:
        return L
    rng = SECTION_XRANGE
    D = densify(L, 0.5)
    keep = (D[:, 0] >= rng[0]) & (D[:, 0] <= rng[1])
    return D[keep] if keep.sum() > 1 else None


if __name__ == "__main__":
    main()
