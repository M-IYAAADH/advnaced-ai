"""Malé island ward map from OSM ward boundaries, OSM roads and the OneMap island outline.

Inputs (raw, unchanged):
  Male_Flood_Data_Starter_Pack/boundary/osm_male_wards_overpass_2026-11-23.json
    Overpass `out geom` for OSM relations 13897577-80 (admin_level 9), fetched 2026-11-23.
  Male_Flood_Data_Starter_Pack/boundary/OneMap_Male_Island.geojson
  Male_Flood_Data_Starter_Pack/mapping/male_osm_roads.geojson
Outputs:
  derived/male_wards_osm.geojson, derived/male_wards_map.png, derived/male_wards_map.pdf
Run from the project root: python scripts/build_ward_map.py
"""
import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch, Polygon
from matplotlib.path import Path as MplPath

RAW = Path("Male_Flood_Data_Starter_Pack")
WARDS_RAW = RAW / "boundary/osm_male_wards_overpass_2026-11-23.json"
ISLAND = RAW / "boundary/OneMap_Male_Island.geojson"
ROADS = RAW / "mapping/male_osm_roads.geojson"
OUT = Path("derived")

LAT0, LON0 = 4.175, 73.5  # local metre projection used across the project (agent.md §5)
KX, KY = 111320 * math.cos(math.radians(LAT0)), 110574

COLOURS = {"Henveiru": "#c9d6c3", "Galolhu": "#e6d7b5", "Machchangolhi": "#c4d0dc", "Maafannu": "#e2c4b8"}
INK, SEA, ROAD = "#2b2b2b", "#eef2f4", "#ffffff"
FONT = "Gill Sans"
# shortcut: hand-placed label nudges (metres) for the narrow, bent Machchangolhi polygon; recheck if boundaries change
LABEL_SHIFT = {"Machchangolhi": (-110, -250)}


def xy(lon, lat):
    return (lon - LON0) * KX, (lat - LAT0) * KY


def stitch(ways):
    """Join OSM outer ways (lists of (lon, lat)) end to end into closed rings."""
    ways = [list(w) for w in ways]
    rings = []
    while ways:
        ring = ways.pop(0)
        while ring[0] != ring[-1]:
            for i, w in enumerate(ways):
                if w[0] == ring[-1]:
                    ring += w[1:]
                elif w[-1] == ring[-1]:
                    ring += w[::-1][1:]
                else:
                    continue
                ways.pop(i)
                break
            else:
                raise ValueError("ward boundary ways do not close into a ring")
        rings.append(ring)
    return rings


def centroid(ring):
    a = cx = cy = 0.0
    for (x0, y0), (x1, y1) in zip(ring, ring[1:]):
        c = x0 * y1 - x1 * y0
        a, cx, cy = a + c, cx + (x0 + x1) * c, cy + (y0 + y1) * c
    return cx / (3 * a), cy / (3 * a)


def area(ring):
    return abs(sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(ring, ring[1:]))) / 2


def load_wards():
    wards = {}
    for rel in json.loads(WARDS_RAW.read_text())["elements"]:
        ways = [[(p["lon"], p["lat"]) for p in m["geometry"]] for m in rel["members"] if m["role"] == "outer"]
        wards[rel["tags"]["name:en"]] = {"rings": stitch(ways), "osm_id": rel["id"], "name_dv": rel["tags"].get("name")}
    assert set(wards) == set(COLOURS), sorted(wards)
    return wards


def write_geojson(wards):
    feats = [{
        "type": "Feature",
        "properties": {"ward": n, "name_dv": w["name_dv"], "osm_relation": w["osm_id"], "source": "OpenStreetMap contributors, ODbL", "fetched": "2026-11-23"},
        "geometry": {"type": "MultiPolygon", "coordinates": [[[list(p) for p in r]] for r in w["rings"]]},
    } for n, w in sorted(wards.items())]
    (OUT / "male_wards_osm.geojson").write_text(json.dumps({"type": "FeatureCollection", "features": feats}, ensure_ascii=False))


def main():
    wards = load_wards()
    write_geojson(wards)
    island = [xy(*p) for p in json.loads(ISLAND.read_text())["features"][0]["geometry"]["coordinates"][0]]
    roads = json.loads(ROADS.read_text())["features"]

    plt.rcParams["font.family"] = FONT
    fig, ax = plt.subplots(figsize=(10, 6.4), dpi=300)
    fig.patch.set_facecolor(SEA)
    ax.set_facecolor(SEA)
    ax.set_aspect("equal")
    ax.axis("off")

    clip = Polygon(island, closed=True, transform=ax.transData)
    ax.add_patch(Polygon(island, closed=True, fc="#f3f1ec", ec="none"))
    for name, w in wards.items():
        for ring in w["rings"]:
            p = ax.add_patch(Polygon([xy(*q) for q in ring], closed=True, fc=COLOURS[name], ec="none"))
            p.set_clip_path(clip)

    widths = {"primary": 1.6, "primary_link": 1.2, "secondary": 1.2, "tertiary": 0.9}
    for f in roads:
        cls = f["properties"]["fclass"]
        if cls in {"footway", "path", "steps"} or f["geometry"]["type"] != "LineString":
            continue
        pts = [xy(*c) for c in f["geometry"]["coordinates"]]
        line = ax.add_patch(PathPatch(MplPath(pts), fc="none", ec=ROAD, lw=widths.get(cls, 0.45), capstyle="round", joinstyle="round"))
        line.set_clip_path(clip)

    # ward edges drawn on top of roads, then the coastline
    for name, w in wards.items():
        for ring in w["rings"]:
            e = ax.add_patch(Polygon([xy(*q) for q in ring], closed=True, fc="none", ec="#8a8a8a", lw=0.7))
            e.set_clip_path(clip)
    ax.add_patch(Polygon(island, closed=True, fc="none", ec=INK, lw=0.9))

    for name, w in wards.items():
        biggest = max(w["rings"], key=lambda r: area([xy(*q) for q in r]))
        cx, cy = centroid([xy(*q) for q in biggest])
        dx, dy = LABEL_SHIFT.get(name, (0, 0))
        ax.text(cx + dx, cy + dy, name.upper(), ha="center", va="center", fontsize=10, color=INK)

    xs, ys = zip(*island)
    pad = 160
    ax.set_xlim(min(xs) - pad, max(xs) + pad)
    ax.set_ylim(min(ys) - pad * 1.6, max(ys) + pad * 1.2)
    x0, y0 = min(xs) - pad + 40, min(ys) - pad * 1.6 + 60

    # scale bar 500 m in two halves
    for i, fc in enumerate((INK, "white")):
        ax.add_patch(Polygon([(x0 + i * 250, y0), (x0 + (i + 1) * 250, y0), (x0 + (i + 1) * 250, y0 + 14), (x0 + i * 250, y0 + 14)], fc=fc, ec=INK, lw=0.6))
    for d in (0, 250, 500):
        ax.text(x0 + d, y0 + 30, f"{d}" if d < 500 else "500 m", ha="center", va="bottom", fontsize=7.5, color=INK)

    nx, ny = max(xs) + pad - 60, max(ys) + pad * 1.2 - 260
    ax.annotate("", xy=(nx, ny + 90), xytext=(nx, ny), arrowprops=dict(arrowstyle="-|>", color=INK, lw=0.9, mutation_scale=10))
    ax.text(nx, ny + 100, "N", ha="center", va="bottom", fontsize=9, color=INK)

    ax.text(min(xs) - pad + 40, max(ys) + pad * 1.2 - 60, "Malé", fontsize=20, color=INK, va="top")
    ax.text(min(xs) - pad + 40, max(ys) + pad * 1.2 - 175, "Wards", fontsize=10, color="#5a5a5a", va="top")
    ax.text(max(xs) + pad - 40, y0, "Ward boundaries and roads: © OpenStreetMap contributors.   Island outline: OneMap.",
            ha="right", va="bottom", fontsize=6, color="#6a6a6a")

    fig.savefig(OUT / "male_wards_map.png", bbox_inches="tight", pad_inches=0, facecolor=SEA)
    fig.savefig(OUT / "male_wards_map.pdf", bbox_inches="tight", pad_inches=0, facecolor=SEA)


if __name__ == "__main__":
    main()
