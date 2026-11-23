"""Build the 200 m analysis grid for Malé island proper (MF-20).

Inputs (raw or earlier derived, unchanged):
  Male_Flood_Data_Starter_Pack/boundary/OneMap_Male_Island.geojson  (study boundary)
  derived/male_wards_osm.geojson                                    (scripts/build_ward_map.py)
Output:
  derived/male_grid_200m.geojson  (WGS84 polygons; cell edges are exact in EPSG:32643)

Each cell is a 200 m square in UTM zone 43N (EPSG:32643), with its lower-left corner on a
multiple of 200 m. That makes cell IDs stable: G<easting>_<northing> of the lower-left corner.
Cells touching the island are kept, with:
  land_fraction  share of the cell inside the OneMap polygon
  ward           ward holding most of the cell's land (OSM ward lines, not checked against a Council map)
  ward_share     share of the cell's land in that ward
Rasters (FABDEM, WorldCover, WorldPop) are in degrees, so they are not pixel-aligned with this
grid; MF-22 should weight raster values by overlap area.
Run from the project root: python scripts/build_analysis_grid.py
"""
import json
from collections import Counter
from pathlib import Path as FilePath

import numpy as np
from matplotlib.path import Path
from pyproj import Transformer

ISLAND = FilePath("Male_Flood_Data_Starter_Pack/boundary/OneMap_Male_Island.geojson")
WARDS = FilePath("derived/male_wards_osm.geojson")
OUT = FilePath("derived/male_grid_200m.geojson")
CELL = 200
SAMPLES = 40  # shortcut: land and ward shares come from a 40 x 40 point lattice per cell (5 m spacing, about 0.1% resolution); use exact polygon overlay if shapely is ever added

to_utm = Transformer.from_crs("EPSG:4326", "EPSG:32643", always_xy=True)
to_wgs = Transformer.from_crs("EPSG:32643", "EPSG:4326", always_xy=True)


def utm_path(ring):
    x, y = to_utm.transform(*zip(*ring))
    return Path(np.column_stack([x, y]))


def ring_area(path):
    x, y = path.vertices[:, 0], path.vertices[:, 1]
    return abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1))) / 2


def main():
    island = utm_path(json.loads(ISLAND.read_text())["features"][0]["geometry"]["coordinates"][0])
    wards = [(f["properties"]["ward"], [utm_path(poly[0]) for poly in f["geometry"]["coordinates"]])
             for f in json.loads(WARDS.read_text(encoding="utf-8"))["features"]]

    (xmin, ymin), (xmax, ymax) = island.vertices.min(0), island.vertices.max(0)
    x0, y0 = np.floor(xmin / CELL) * CELL, np.floor(ymin / CELL) * CELL
    offsets = (np.arange(SAMPLES) + 0.5) * CELL / SAMPLES
    gx, gy = np.meshgrid(offsets, offsets)
    lattice = np.column_stack([gx.ravel(), gy.ravel()])

    feats, land_m2 = [], 0.0
    for e in np.arange(x0, xmax, CELL):
        for n in np.arange(y0, ymax, CELL):
            pts = lattice + (e, n)
            on_land = island.contains_points(pts)
            if not on_land.any():
                continue
            land = pts[on_land]
            ward_of = np.full(len(land), "", dtype=object)
            for name, polys in wards:
                inside = np.zeros(len(land), bool)
                for p in polys:
                    inside |= p.contains_points(land)
                ward_of[inside & (ward_of == "")] = name
            counts = Counter(w for w in ward_of if w)
            ward, k = counts.most_common(1)[0] if counts else ("outside_ward_polygons", 0)
            frac = on_land.mean()
            land_m2 += frac * CELL * CELL
            corners = [(e, n), (e + CELL, n), (e + CELL, n + CELL), (e, n + CELL), (e, n)]
            lon, lat = to_wgs.transform(*zip(*corners))
            feats.append({
                "type": "Feature",
                "properties": {"cell_id": f"G{int(e)}_{int(n)}", "easting_min": int(e), "northing_min": int(n),
                               "land_fraction": round(float(frac), 3), "ward": ward,
                               "ward_share": round(k / len(land), 3)},
                "geometry": {"type": "Polygon", "coordinates": [[[round(a, 7), round(b, 7)] for a, b in zip(lon, lat)]]},
            })

    ids = [f["properties"]["cell_id"] for f in feats]
    assert len(ids) == len(set(ids)), "duplicate cell IDs"
    island_m2 = ring_area(island)
    assert abs(land_m2 - island_m2) / island_m2 < 0.01, (land_m2, island_m2)  # cells tile the island

    OUT.write_text(json.dumps({"type": "FeatureCollection",
                               "name": "male_grid_200m",
                               "crs_note": "coordinates WGS84 (EPSG:4326); cells are exact 200 m squares in EPSG:32643",
                               "features": feats}))
    by_ward = Counter(f["properties"]["ward"] for f in feats)
    print(f"{len(feats)} cells; island {island_m2 / 1e6:.3f} km2, cells' land {land_m2 / 1e6:.3f} km2; by ward {dict(by_ward)}")


if __name__ == "__main__":
    main()
