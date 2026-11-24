"""Per-cell attributes for the 200 m analysis grid (MF-22).

Output: derived/grid_attributes.csv, one row per cell of derived/male_grid_200m.geojson.
Run from the project root: python scripts/compute_grid_attributes.py

Method: each cell gets a 40 x 40 lattice of equal-area points (5 m spacing in EPSG:32643, same as
build_analysis_grid.py). Points inside the OneMap island outer ring are the cell's land points. A raster
value's weight is the share of land points falling in its pixel (= overlap-area weighting). Land points on
raster nodata are dropped from that layer; <layer>_valid_land_share is the share kept.
shortcut: area is sampled at 5 m, so shares are good to about 0.1-0.5 percentage points and a pixel's weight
to about 1/(land points); pixel areas inside the island are treated as equal (about 4 deg N). Use exact
polygon overlay if shapely is added.
shortcut: building coverage uses footprint outer rings only (no holes) and counts overlapping footprints once
(point is inside any); roads are clipped to the whole cell square, not to land (road_density divides by land area,
so edge cells with jetties/causeways are inflated); the coast distance uses the OneMap outer ring only.

Raster georeferencing (Pillow tags 33550 scale, 33922 tiepoint, 34735 GeoKeys key 1025):
  FABDEM RasterPixelIsPoint: tiepoint is the CENTRE of pixel (0,0); pixel i spans x0 + (i +- 0.5) * dx.
  WorldCover RasterPixelIsArea: tiepoint is the TOP-LEFT CORNER of pixel (0,0); pixel i spans x0 + i*dx .. +dx.
  Both rows run north to south. Nodata: FABDEM -9999, WorldCover 0 (tag 42113).

Columns
  cell_id, ward                      from the grid (ward = OSM ward holding most of the cell's land; unchecked against a Council map)
  land_fraction                      share of the cell square inside the OneMap polygon (recomputed, sampled)
  land_area_m2                       land_fraction * 40000, m2
  fabdem_mean_m / _min_m / _p10_m    area-weighted mean, minimum and weighted 10th percentile of FABDEM V1-2 (30 m) over land, m
                                     above EGM2008. RELATIVE RANK ONLY (island median about 5.04 m suggests residual bias; not
                                     surveyed). Licence CC BY-NC-SA 4.0. File: elevation/Male_FABDEM_30m_masked.tif
  fabdem_valid_land_share            share of land points with valid FABDEM (0-1)
  fabdem_zero_share                  weight of valid land pixels whose FABDEM value is exactly 0 m (likely the
                                     inherited water mask at the coast, not ground height); treat those cells' FABDEM with care
  worldcover_builtup_share           share of valid land points of ESA WorldCover 2021 class 50 (built-up), 0-1. NOT imperviousness.
  worldcover_tree_share              class 10; worldcover_water_share classes 80 and 90 (water, herbaceous wetland);
  worldcover_other_share             every other class (20, 30, 40, 60, 70, 95, 100). Shares sum to 1. CC BY 4.0.
  worldcover_valid_land_share        share of land points with valid WorldCover (0-1). File: mapping/male_worldcover_2021_10m.tif
  building_coverage_google075        share of land points inside any Google Open Buildings v3 footprint with confidence >= 0.75
                                     (0-1; footprint area fraction, not counts; model detections, not survey; CC BY 4.0 / ODbL).
                                     File: mapping/male_google_buildings_conf075.geojson
  road_length_m, road_density_m_per_km2        OSM road centreline length clipped to the cell square (m) and that divided by land area (m per km2). ODbL.
  road_length_vehicular_m, ..._density_...     same, fclass in primary, primary_link, secondary, tertiary, residential,
                                     service, living_street (footway, pedestrian, path, steps excluded). File: mapping/male_osm_roads.geojson
  dist_centre_to_coast_m             distance from the cell square's centre to the OneMap outer ring, m
  dist_land_centroid_to_coast_m      same from the centroid of the cell's land points (better for edge cells), m
Empty means no valid data (never 0).
"""
import json
from pathlib import Path as FilePath

import numpy as np
import pandas as pd
from matplotlib.path import Path
from PIL import Image
from pyproj import Transformer

PACK = FilePath("Male_Flood_Data_Starter_Pack")
GRID = FilePath("derived/male_grid_200m.geojson")
ISLAND = PACK / "boundary/OneMap_Male_Island.geojson"
FAB = PACK / "elevation/Male_FABDEM_30m_masked.tif"
WC = PACK / "mapping/male_worldcover_2021_10m.tif"
BLD = PACK / "mapping/male_google_buildings_conf075.geojson"
ROADS = PACK / "mapping/male_osm_roads.geojson"
OUT = FilePath("derived/grid_attributes.csv")
CELL, N = 200, 40
VEHICULAR = {"primary", "primary_link", "secondary", "tertiary", "residential", "service", "living_street"}

to_utm = Transformer.from_crs("EPSG:4326", "EPSG:32643", always_xy=True)
to_wgs = Transformer.from_crs("EPSG:32643", "EPSG:4326", always_xy=True)


class Raster:
    def __init__(self, path):
        im = Image.open(path)
        t = im.tag_v2
        self.w, self.h = im.size
        self.dx, self.dy = t[33550][:2]
        tx, ty = t[33922][3:5]
        keys = t[34735]
        is_point = any(keys[i] == 1025 and keys[i + 3] == 2 for i in range(4, len(keys) - 3, 4))
        # pixel (i, j) covers [x0 + i*dx, x0 + (i+1)*dx] x [y0 - (j+1)*dy, y0 - j*dy]
        self.x0 = tx - (self.dx / 2 if is_point else 0)
        self.y0 = ty + (self.dy / 2 if is_point else 0)
        self.nodata = float(t[42113])
        self.a = np.asarray(im, dtype=float)
        assert self.a.shape == (self.h, self.w)

    def lookup(self, lon, lat):
        """Return (pixel id or -1 outside extent, value, valid mask)."""
        i = np.floor((lon - self.x0) / self.dx).astype(int)
        j = np.floor((self.y0 - lat) / self.dy).astype(int)
        inside = (i >= 0) & (i < self.w) & (j >= 0) & (j < self.h)
        v = np.full(len(lon), np.nan)
        v[inside] = self.a[j[inside], i[inside]]
        valid = inside & (v != self.nodata)
        return np.where(inside, j * self.w + i, -1), v, valid


def wquant(vals, weights, q):
    """Weighted quantile (step function: first value whose cumulative weight reaches q)."""
    o = np.argsort(vals)
    c = np.cumsum(weights[o]) / weights.sum()
    return vals[o][np.searchsorted(c, q - 1e-12)]


def pixel_weights(pix):
    ids, cnt = np.unique(pix, return_counts=True)
    return ids, cnt / cnt.sum()


def clip_len(p, q, x0, y0, x1, y1):
    """Liang-Barsky: length of segment p->q inside the rectangle."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    t0, t1 = 0.0, 1.0
    for pk, qk in ((-dx, p[0] - x0), (dx, x1 - p[0]), (-dy, p[1] - y0), (dy, y1 - p[1])):
        if pk == 0:
            if qk < 0:
                return 0.0
        else:
            r = qk / pk
            if pk < 0:
                t0 = max(t0, r)
            else:
                t1 = min(t1, r)
            if t0 > t1:
                return 0.0
    return (t1 - t0) * np.hypot(dx, dy)


def dist_to_ring(pt, ring):
    a, b = ring[:-1], ring[1:]
    ab = b - a
    t = np.clip(((pt - a) * ab).sum(1) / (ab ** 2).sum(1), 0, 1)
    return float(np.hypot(*(a + t[:, None] * ab - pt).T).min())


def utm_xy(coords):
    x, y = to_utm.transform(*zip(*[c[:2] for c in coords]))
    return np.column_stack([x, y])


def main():
    ring = utm_xy(json.loads(ISLAND.read_text(encoding="utf-8"))["features"][0]["geometry"]["coordinates"][0])
    island = Path(ring)
    grid = json.loads(GRID.read_text(encoding="utf-8"))["features"]
    fab, wc = Raster(FAB), Raster(WC)

    # extent check: rasters must cover the island bbox
    lo, la = to_wgs.transform(*ring.min(0)), to_wgs.transform(*ring.max(0))
    for r, n in ((fab, "FABDEM"), (wc, "WorldCover")):
        tol = 1e-4  # about 10 m: WorldCover stops a few metres short of the island's east tip; those points count as invalid
        assert r.x0 <= lo[0] + tol and r.x0 + r.w * r.dx >= la[0] - tol and r.y0 - r.h * r.dy <= lo[1] + tol and r.y0 >= la[1] - tol, n

    polys = []  # Google footprints: outer rings in UTM with bbox
    for f in json.loads(BLD.read_text(encoding="utf-8"))["features"]:
        g = f["geometry"]
        for poly in (g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]):
            xy = utm_xy(poly[0])
            polys.append((xy.min(0), xy.max(0), Path(xy)))
    bmin = np.array([p[0] for p in polys]); bmax = np.array([p[1] for p in polys])

    roads = []  # (is_vehicular, xy)
    for f in json.loads(ROADS.read_text(encoding="utf-8"))["features"]:
        g = f["geometry"]
        for line in (g["coordinates"] if g["type"] == "MultiLineString" else [g["coordinates"]]):
            roads.append((f["properties"].get("fclass") in VEHICULAR, utm_xy(line)))
    road_total = sum(np.hypot(*np.diff(xy, axis=0).T).sum() for _, xy in roads)

    off = (np.arange(N) + 0.5) * CELL / N
    gx, gy = np.meshgrid(off, off)
    lattice = np.column_stack([gx.ravel(), gy.ravel()])

    rows, spot = [], {}
    wsum = {}
    for f in grid:
        p = f["properties"]
        e, n = p["easting_min"], p["northing_min"]
        pts = lattice + (e, n)
        land = pts[island.contains_points(pts)]
        m = len(land)
        row = {"cell_id": p["cell_id"], "ward": p["ward"], "land_fraction": m / N ** 2, "land_area_m2": m / N ** 2 * CELL ** 2}
        lon, lat = to_wgs.transform(land[:, 0], land[:, 1])

        # FABDEM
        pix, v, ok = fab.lookup(lon, lat)
        row["fabdem_valid_land_share"] = ok.sum() / m
        if ok.any():
            ids, w = pixel_weights(pix[ok])
            wsum[(p["cell_id"], "fab")] = w.sum()
            vals = np.array([fab.a[i // fab.w, i % fab.w] for i in ids])
            row["fabdem_mean_m"], row["fabdem_min_m"] = float((vals * w).sum()), float(vals.min())
            row["fabdem_p10_m"] = float(wquant(vals, w, 0.10))
            # FABDEM inherits the Copernicus DEM water mask (sea flattened to 0 m), so exact zeros on land are
            # probably masked water edges, not ground at 0 m; kept as values but reported so they can be excluded.
            row["fabdem_zero_share"] = float(w[vals == 0].sum())
            spot[p["cell_id"]] = {"land_pts": m, "fab_pixels": len(ids), "fab_w": np.round(w, 3).tolist()}
        # WorldCover
        pix, v, ok = wc.lookup(lon, lat)
        row["worldcover_valid_land_share"] = ok.sum() / m
        if ok.any():
            ids, w = pixel_weights(pix[ok])
            wsum[(p["cell_id"], "wc")] = w.sum()
            k = v[ok]
            row["worldcover_builtup_share"] = float((k == 50).mean())
            row["worldcover_tree_share"] = float((k == 10).mean())
            row["worldcover_water_share"] = float(np.isin(k, (80, 90)).mean())
            row["worldcover_other_share"] = max(0.0, 1 - row["worldcover_builtup_share"] - row["worldcover_tree_share"] - row["worldcover_water_share"])
        # buildings
        inb = np.zeros(m, bool)
        cand = np.where((bmax[:, 0] >= e) & (bmin[:, 0] <= e + CELL) & (bmax[:, 1] >= n) & (bmin[:, 1] <= n + CELL))[0]
        for i in cand:
            inb |= polys[i][2].contains_points(land)
        row["building_coverage_google075"] = inb.mean()
        # roads
        tot = veh = 0.0
        for isv, xy in roads:
            if xy[:, 0].max() < e or xy[:, 0].min() > e + CELL or xy[:, 1].max() < n or xy[:, 1].min() > n + CELL:
                continue
            L = sum(clip_len(a, b, e, n, e + CELL, n + CELL) for a, b in zip(xy[:-1], xy[1:]))
            tot += L
            veh += L * isv
        km2 = row["land_area_m2"] / 1e6
        row.update(road_length_m=tot, road_density_m_per_km2=tot / km2, road_length_vehicular_m=veh,
                   road_density_vehicular_m_per_km2=veh / km2)
        row["dist_centre_to_coast_m"] = dist_to_ring(np.array([e + CELL / 2, n + CELL / 2]), ring)
        row["dist_land_centroid_to_coast_m"] = dist_to_ring(land.mean(0), ring)
        rows.append(row)
        spot.setdefault(p["cell_id"], {})["bld"] = row["building_coverage_google075"]

    cols = ["cell_id", "ward", "land_fraction", "land_area_m2", "fabdem_mean_m", "fabdem_min_m", "fabdem_p10_m",
            "fabdem_valid_land_share", "fabdem_zero_share", "worldcover_builtup_share", "worldcover_tree_share", "worldcover_water_share",
            "worldcover_other_share", "worldcover_valid_land_share", "building_coverage_google075", "road_length_m",
            "road_density_m_per_km2", "road_length_vehicular_m", "road_density_vehicular_m_per_km2",
            "dist_centre_to_coast_m", "dist_land_centroid_to_coast_m"]
    df = pd.DataFrame(rows)[cols]
    df.to_csv(OUT, index=False, float_format="%.6g")

    # ---- self-checks
    assert len(df) == 75 and df.cell_id.is_unique and list(df.cell_id) == [f["properties"]["cell_id"] for f in grid]
    assert all(abs(w - 1) < 1e-9 for w in wsum.values())
    isl = abs(np.dot(ring[:, 0], np.roll(ring[:, 1], -1)) - np.dot(ring[:, 1], np.roll(ring[:, 0], -1))) / 2
    assert abs(df.land_area_m2.sum() - isl) / isl < 0.01, (df.land_area_m2.sum(), isl)
    gl = np.array([f["properties"]["land_fraction"] for f in grid])
    assert np.abs(df.land_fraction.values - gl).max() < 0.02
    shares = [c for c in cols if c.endswith("_share") or c in ("land_fraction", "building_coverage_google075")]
    assert ((df[shares].fillna(0) >= 0) & (df[shares].fillna(0) <= 1 + 1e-9)).all().all()
    s = df[["worldcover_builtup_share", "worldcover_tree_share", "worldcover_water_share", "worldcover_other_share"]].dropna().sum(1)
    assert (abs(s - 1) < 1e-6).all()
    d = df.dropna(subset=["fabdem_min_m"])
    assert (d.fabdem_min_m <= d.fabdem_p10_m + 1e-9).all()
    xmin, ymin = ring.min(0); xmax, ymax = ring.max(0)
    ex = [f["properties"] for f in grid]
    gx0, gx1 = min(q["easting_min"] for q in ex), max(q["easting_min"] for q in ex) + CELL
    gy0, gy1 = min(q["northing_min"] for q in ex), max(q["northing_min"] for q in ex) + CELL
    indep = sum(np.hypot(*np.diff(np.clip(xy, [gx0, gy0], [gx1, gy1]), axis=0).T).sum() for _, xy in roads)  # clip-by-clamp: approx
    print(f"road total {df.road_length_m.sum():.0f} m vs all OSM {road_total:.0f} m vs clamp-in-extent {indep:.0f} m")
    assert abs(df.road_length_m.sum() - road_total) / road_total < 0.02 or abs(df.road_length_m.sum() - indep) / indep < 0.02

    # ---- reports
    print("grid extent roads outside grid (m):", round(road_total - df.road_length_m.sum()))
    land_w = df.land_area_m2
    print("island FABDEM land-weighted mean of cell means: %.2f m (QA median 5.04); built-up share over land: %.3f; google bldg cov: %.3f" % (
        np.average(d.fabdem_mean_m, weights=d.land_area_m2), np.average(df.worldcover_builtup_share.dropna(), weights=land_w[df.worldcover_builtup_share.notna()]),
        np.average(df.building_coverage_google075, weights=land_w)))
    cells = [df.sort_values("building_coverage_google075").iloc[-1].cell_id,
             df[df.land_fraction < 0.25].iloc[0].cell_id,
             df[(df.land_fraction > 0.99)].iloc[len(df[df.land_fraction > 0.99]) // 2].cell_id]
    for c in cells:
        r = df[df.cell_id == c].iloc[0]
        print("spot", c, "land_frac", round(r.land_fraction, 3), "bld", round(r.building_coverage_google075, 3), spot.get(c, "no valid fabdem"))
    print(df.describe().loc[["min", "max"]].T.round(3).to_string())
    print("cells with any missing:", df[df.isna().any(axis=1)][["cell_id", "land_fraction", "fabdem_valid_land_share", "worldcover_valid_land_share"]].to_string())


if __name__ == "__main__":
    main()
