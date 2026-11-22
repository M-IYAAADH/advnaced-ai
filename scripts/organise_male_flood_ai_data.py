"""Copy the repository's data, evidence and outputs into the male_flood_ai_data
template, verify every copy by SHA-256, profile each dataset and write the
catalogue files and cleaned working copies.

Read-only for the repository: originals are never moved or modified. Existing
populated files in the destination are never overwritten (a differing file is
reported as a conflict instead).

Usage (Python 3.12 with pandas, pyarrow, rasterio):
    python scripts/organise_male_flood_ai_data.py --repo . --dest ../male_flood_ai_data
"""
import argparse, datetime as dt, fnmatch, hashlib, json, shutil
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

EXCLUDE_DIRS = {".git", "__pycache__", ".venv", ".ipynb_checkpoints", "node_modules"}
EXCLUDE_FILES = {".DS_Store"}
# Not data/evidence: UI app and VCS config. Recorded in file_mapping, not copied.
NOT_COPIED = {"sprint_board.html": "interactive sprint-board app UI, not data or evidence",
              ".gitignore": "version-control configuration"}

SP, MB = "Male_Flood_Data_Starter_Pack/", "male-flood-basis/"

# (glob on repo-relative path, destination folder, role, human-review note). First match wins;
# EXTRA adds secondary copies. Destination keeps the original filename.
ROUTES = [
    ("groundsource_2026.parquet", "01_raw/flood_catalogues/groundsource", "raw_source", ""),
    ("male_flood_inventory.csv", "02_interim/event_candidates", "imported_event_candidates", ""),
    (SP + "rainfall/noaa_precipitation_accumulations_*", "02_interim/weather_aligned/noaa_precipitation_accumulations", "derived_extraction", ""),
    (SP + "rainfall/noaa_*", "01_raw/rainfall/station/noaa_velana_435550_99999", "raw_source", ""),
    (SP + "rainfall/nasa_power_*.csv", "02_interim/weather_aligned/nasa_power_merra2", "derived_extraction", ""),
    (SP + "rainfall/nasa_power_*", "01_raw/rainfall/reanalysis/nasa_power_merra2", "raw_source", ""),
    (SP + "rainfall/chirpsv3_*", "01_raw/rainfall/satellite/chirps_v3", "raw_source",
     "Added subfolder: CHIRPS is satellite-gauge, not reanalysis or station; template has no satellite folder."),
    (SP + "rainfall/*", "01_raw/rainfall", "source_documentation", ""),
    (SP + "tides/*", "01_raw/sea_level/observed/uhslc_record1082", "raw_source", ""),
    (SP + "boundary/OneMap_Hulhule_Context*", "01_raw/geospatial/male_boundary", "raw_source",
     "Hulhule context polygon, not Male island proper; kept beside the boundary for station context."),
    (SP + "boundary/*", "01_raw/geospatial/male_boundary", "raw_source", ""),
    (SP + "mapping/male_osm_island_boundary.geojson", "01_raw/geospatial/male_boundary", "raw_source",
     "OSM island polygon (alternative to official OneMap boundary)."),
    (SP + "mapping/*", "01_raw/geospatial/mapping", "raw_source_clipped",
     "Added subfolder. Received as clips made by the 14 Nov 2026 research pass, not untouched provider downloads."),
    (SP + "elevation/*", "01_raw/geospatial/elevation", "raw_source",
     "Added subfolder. Male_FABDEM_30m_masked.tif is a clip of the original tile."),
    (SP + "flood/*", "02_interim/event_candidates/starter_pack_flood", "event_candidates", ""),
    (SP + "Data_Request_Specification.md", "06_research/data_requests", "research_document", ""),
    (SP + "File_Manifest.json", "00_catalog/legacy_starter_pack", "legacy_catalogue", ""),
    (SP + "Dataset_Catalogue.*", "00_catalog/legacy_starter_pack", "legacy_catalogue", ""),
    (SP + "*", "06_research/reports/starter_pack", "research_document", ""),
    (MB + "data/male_reanalysis_*", "01_raw/rainfall/reanalysis/open_meteo_era5_compiled", "raw_source_compiled",
     "Received from the 14 Nov 2026 compilation; original Open-Meteo request and timezone parameter not saved."),
    (MB + "data/hulhule_station_daily_*", "01_raw/rainfall/station/compiled_hulhule_gsod_metric", "raw_source_compiled",
     "Needs human classification: compiler-converted GSOD (metric, 99.99 blanked), not unchanged NOAA bytes. Raw NOAA GSOD 2024-2025 is in noaa_velana_435550_99999."),
    (MB + "data/male_sea_level_waves_*", "01_raw/sea_level/modelled/open_meteo_marine_compiled", "raw_source_compiled",
     "Modelled sea level, not tide-gauge observation."),
    (MB + "data/male_forecast_hourly_snapshot_*", "01_raw/forecast_archives/met_norway_snapshot_2026-11-14", "raw_source_compiled",
     "One forecast snapshot (issued about 14 Nov 2026), not a historical forecast archive."),
    (MB + "data/male_daily_features_with_flood_labels.csv", "02_interim/weather_aligned/male_flood_basis_daily_features", "derived_compiled",
     "Needs human classification: compiler-merged feature/label table, undocumented derivation; flood_reported=0 means no report found."),
    (MB + "data/*", "01_raw/flood_evidence/compiled_secondary/male_flood_basis", "news_derived_compilation",
     "Added subfolder. AI-assisted secondary compilation of news, not saved articles."),
    (MB + "README.txt", "01_raw/flood_evidence/compiled_secondary/male_flood_basis", "source_documentation", ""),
    (MB + "flood_map.html", "06_research/reports/male_flood_basis", "research_document",
     "Compiler's write-up page; contains unsourced claims logged as data_issues A2-A4."),
    ("derived/daily_exploration/*", "05_outputs/legacy/daily_exploration", "legacy_output", ""),
    ("derived/extended_analysis/*", "05_outputs/legacy/extended_analysis", "legacy_output", ""),
    ("derived/groundsource_review/*", "05_outputs/legacy/groundsource_review", "legacy_output", ""),
    ("derived/*", "05_outputs/legacy/road_evidence", "legacy_output",
     "Added subfolder for the road-evidence outputs (MF-12 to MF-17, MF-44)."),
    ("verification/*", "03_reviewed/events/legacy_landmark_checks", "legacy_review_decision",
     "Needs human classification: per-place source checks, not a canonical reviewed event table."),
    ("reports/*", "06_research/reports", "research_document", ""),
    ("research_notes/*", "06_research/reports/research_notes", "research_document", ""),
    ("requests/*", "06_research/data_requests", "research_document", ""),
    ("scripts/*", "05_outputs/legacy/scripts", "code", "Code kept with the legacy outputs it produced; working copy stays in the repo."),
    ("Male_Flood_Data_Research.pdf", "06_research/reports", "research_document",
     "Differs from the starter-pack PDF of the same name (different checksum)."),
    ("Assignment Brief*", "06_research/reports/coursework", "coursework_document",
     "Older brief; lecturer confirmed its components do not apply (CLAUDE.md, data_issues I2)."),
    ("COURSEWORK*", "06_research/reports/coursework", "coursework_document", "IJCAI-format coursework template."),
    ("*.md", "06_research/reports/project_docs", "project_document", ""),
    ("requirements.txt", "06_research/reports/project_docs", "project_document", ""),
]
EXTRA = [
    ("derived/daily_exploration/event_review.csv", "03_reviewed/events/legacy_daily_exploration", "legacy_review_decision",
     "Earlier include/uncertain decisions (18 incidents). Copied, not merged into flood_events.csv."),
    ("derived/extended_analysis/incident_storm_groups.csv", "03_reviewed/storm_groups/legacy_extended_analysis", "legacy_review_decision",
     "Storm groups S01-S17 are proxies (<=2-day gap rule), not verified storms."),
    ("derived/extended_analysis/dashboard.html", "05_outputs/dashboard", "legacy_output", ""),
    ("derived/extended_analysis/*.png", "05_outputs/figures", "legacy_output", ""),
    ("derived/extended_analysis/*.pdf", "05_outputs/figures", "legacy_output", ""),
    ("derived/road_flood_evidence_map.png", "05_outputs/figures", "legacy_output", ""),
    ("derived/groundsource_review/*.csv", "02_interim/groundsource_candidates", "groundsource_candidates",
     "Spatial-screen candidates; a polygon touching Male is not a Male flood footprint."),
]


def sha256(p, buf=1 << 22):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while b := f.read(buf):
            h.update(b)
    return h.hexdigest()


def repo_files(repo):
    for p in sorted(repo.rglob("*")):
        rel = p.relative_to(repo)
        if p.is_file() and not (set(rel.parts) & EXCLUDE_DIRS) and p.name not in EXCLUDE_FILES:
            yield rel.as_posix()


def routes_for(rel):
    out = []
    for table, first_only in ((ROUTES, True), (EXTRA, False)):
        for pat, folder, role, note in table:
            if fnmatch.fnmatchcase(rel, pat):
                # only research_notes/ has nested folders worth keeping; everything else is flat
                sub = rel[len("research_notes/"):] if rel.startswith("research_notes/") else Path(rel).name
                out.append((f"{folder}/{sub}", role, note))
                if first_only:
                    break
    return out


# ---------------------------------------------------------------- curated metadata
# Keyed by repo-relative path glob. Facts come from the files, the starter-pack catalogue/READMEs,
# male-flood-basis/README.txt and the earlier verified reports. 'unknown' means not documented.
META = {
    "groundsource_2026.parquet": dict(
        provider="Google Research (Groundsource v1, Zenodo DOI 10.5281/zenodo.18647054)",
        source_url="https://zenodo.org/records/18647054", source_type="news_derived_catalogue (Gemini extraction)",
        time_resolution="day-level event intervals", geographic_scope="global; Male only via spatial screen",
        timestamp_timezone="unknown (dates only)", accumulation_window="not applicable", units="area_km2 = area of location polygon (not flooded area)",
        licence="CC BY 4.0 per GEE community catalogue; confirm at Zenodo before redistribution",
        nature="news_derived", downloaded="unknown (MD5 cd1b5de6508f7aad8e1d1d0dd4cecea6 matches Zenodo v1)"),
    SP + "rainfall/noaa_global_hourly_*": dict(
        provider="NOAA NCEI Global Hourly (ISD), station 435550/99999 VRMM Velana, Hulhule",
        source_url="https://noaa-global-hourly-pds.s3.amazonaws.com/{year}/43555099999.csv", source_type="measured_station_reports",
        time_resolution="irregular synoptic/METAR reports (FM-12/FM-15/FM-16)", geographic_scope="Hulhule airport, 4.192N 73.529E (not Male island)",
        timestamp_timezone="UTC (ISD DATE field)", accumulation_window="AA groups: 6, 12, 24 h and unknown-period; no 1-h group verified",
        units="encoded ISD groups (scaled integers); see ISD format", missing="9999 / 99 period codes inside groups; blank groups",
        flags="QUALITY_CONTROL, per-group quality and condition codes", licence="NOAA open data; cite NOAA",
        nature="measured", downloaded="2026-11-14"),
    SP + "rainfall/noaa_gsod_*": dict(
        provider="NOAA NCEI Global Summary of the Day, station 43555099999", source_type="measured_station_daily_summary",
        source_url="https://www.ncei.noaa.gov/data/global-summary-of-the-day/access/{year}/43555099999.csv",
        time_resolution="daily", geographic_scope="Hulhule airport, 4.192N 73.529E (not Male island)",
        timestamp_timezone="GSOD day; day boundary relative to local time not verified",
        accumulation_window="PRCP flag letter gives reporting composition; may include part of preceding day (NOAA metadata)",
        units="PRCP inches; TEMP/DEWP/MAX/MIN degF; WDSP/MXSPD/GUST knots; VISIB miles; SLP/STP hPa",
        missing="PRCP 99.99; TEMP 9999.9; SLP/STP 9999.9; WDSP/MXSPD/GUST 999.9; VISIB 999.9",
        flags="PRCP flag letter A-I; *_ATTRIBUTES = count of observations", licence="NOAA open data",
        nature="measured", downloaded="2026-11-14"),
    SP + "rainfall/noaa_precipitation_accumulations_*": dict(
        provider="Derived from NOAA Global Hourly AA groups (starter-pack research pass)", source_type="derived_extraction",
        time_resolution="per report", geographic_scope="Hulhule airport", timestamp_timezone="UTC (Z suffix)",
        accumulation_window="accumulation_hours column (6, 12, 24 or blank=unknown); overlapping windows must not be summed",
        units="precipitation_mm (tenths divided by 10)", missing="period 99 and depth 9999 set to blank", flags="condition_code, quality_code",
        licence="NOAA open data", nature="measured (derived extraction)", downloaded="2026-11-14"),
    SP + "rainfall/nasa_power_*": dict(
        provider="NASA POWER (MERRA-2 reanalysis)", source_url="see nasa_power_request_url.txt", source_type="reanalysis",
        time_resolution="hourly", geographic_scope="point 4.175N 73.510E (grid cell, not a gauge)",
        timestamp_timezone="UTC; CSV adds UTC+5 column", accumulation_window="hourly rate as delivered (PRECTOTCORR)",
        units="mm/hour", licence="NASA open data", nature="reanalysis", downloaded="2026-11-14"),
    SP + "rainfall/chirpsv3_*": dict(
        provider="Climate Hazards Center CHIRPS v3 (final, sat)", source_url="https://www.chc.ucsb.edu/data/chirps3",
        source_type="satellite_gauge_blend", time_resolution="daily (one date: 2025-01-03)", geographic_scope="3x3 cells of 0.05 deg around Male",
        timestamp_timezone="CHIRPS day (UTC-based product day)", accumulation_window="daily total", units="mm",
        licence="public domain", nature="satellite_estimate", downloaded="2026-11-14"),
    SP + "tides/UHSLC*": dict(
        provider="UHSLC / JASL research-quality hourly, Male record 1082 version B", source_type="measured_tide_gauge",
        source_url="https://uhslc.soest.hawaii.edu/erddap/tabledap/global_hourly_rqds.html", time_resolution="hourly",
        geographic_scope="Male tide gauge 4.19N 73.5267E", timestamp_timezone="UTC (units row)", accumulation_window="instantaneous hourly value",
        units="sea_level mm relative to station zero (not MSL, not flood depth)", missing="blank sea_level (125 rows)",
        flags="quality column", licence="free use and redistribution; cite DOI 10.7289/V5V40S7W", nature="measured", downloaded="2026-11-14"),
    SP + "boundary/OneMap_Male*": dict(
        provider="OneMap Maldives (island layer, service island_20240509)", source_url="https://readme.onemap.mv/", source_type="official_boundary",
        geographic_scope="Male island proper (OBJECTID 1442)", licence="public download; no explicit reuse licence found; confirm terms",
        nature="official_vector", downloaded="2026-11-14"),
    SP + "boundary/OneMap_Hulhule*": dict(
        provider="OneMap Maldives", source_url="https://readme.onemap.mv/", source_type="official_boundary",
        geographic_scope="Hulhule (context only, not study area)", licence="confirm terms", nature="official_vector", downloaded="2026-11-14"),
    SP + "mapping/male_osm_*": dict(
        provider="OpenStreetMap via Geofabrik (snapshot 2026-11-13)", source_url="https://download.geofabrik.de/asia/maldives.html",
        source_type="volunteered_vector", geographic_scope="Male, clipped to OSM island polygon", licence="ODbL 1.0", nature="mapped_vector",
        downloaded="2026-11-14"),
    SP + "mapping/male_microsoft_*": dict(
        provider="Microsoft Global ML Building Footprints", source_url="https://github.com/microsoft/GlobalMLBuildingFootprints",
        source_type="ml_detections", geographic_scope="Male, clipped to OSM island polygon", licence="CDLA Permissive 2.0",
        nature="modelled_detections", downloaded="2026-11-14"),
    SP + "mapping/male_google_*": dict(
        provider="Google Open Buildings v3 (inference May 2023)", source_url="https://sites.research.google/gr/open-buildings/",
        source_type="ml_detections", geographic_scope="Male, clipped to OSM island polygon", licence="CC BY 4.0 or ODbL 1.0 (user choice)",
        nature="modelled_detections", downloaded="2026-11-14"),
    SP + "mapping/male_worldcover_*": dict(
        provider="ESA WorldCover 2021 v200", source_url="https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v200",
        source_type="land_cover_raster", time_resolution="2021 composite", geographic_scope="Male clip", units="class codes",
        licence="CC BY 4.0", nature="modelled_classification", downloaded="2026-11-14"),
    SP + "mapping/male_worldpop_*": dict(
        provider="WorldPop Global2 R2025A", source_url="https://api.worldpop.org/v3/countries/MDV/files?year=2025",
        source_type="population_raster", time_resolution="2025", geographic_scope="Male crop", units="people per ~100 m cell",
        licence="CC BY 4.0", nature="modelled", downloaded="2026-11-14"),
    SP + "elevation/*.tif": dict(
        provider="FABDEM V1-2 (University of Bristol)", source_url="https://data.bris.ac.uk/datasets/s5hqmjcdj8yo2ibzi9b4ew3sn/",
        source_type="dem_raster", geographic_scope="tile N04E073; masked clip to OneMap Male polygon", units="m, EGM2008 vertical datum",
        licence="CC BY-NC-SA 4.0", nature="modelled (forest/building-removed DEM, not surveyed)", downloaded="2026-11-14"),
    SP + "flood/event_candidates.csv": dict(
        provider="Starter-pack research pass (NDMA, Male City Council VLR, MMS)", source_type="event_leads",
        time_resolution="date", geographic_scope="Male city-level", licence="per source", nature="official_record_leads", downloaded="2026-11-14"),
    MB + "data/male_reanalysis_*": dict(
        provider="ERA5 via Open-Meteo historical API (per compiler README)", source_url="https://open-meteo.com/en/docs/historical-weather-api",
        source_type="reanalysis", time_resolution="hourly / daily", geographic_scope="Male grid point (coordinates not recorded)",
        timestamp_timezone="time_local: undocumented compiler label (UTC+5 plausible, unverified)",
        accumulation_window="Open-Meteo hourly precipitation = preceding-hour sum (provider docs); daily = sum by nominal day",
        units="mm, degC, %, hPa, km/h, deg (in column names)", licence="Open-Meteo CC BY 4.0; ERA5 Copernicus licence",
        nature="reanalysis", downloaded="about 2026-11-14 (compiler)"),
    MB + "data/hulhule_station_daily_*": dict(
        provider="NOAA GSOD station 43555099999, converted by the compiler", source_type="measured_station_daily_summary (converted)",
        time_resolution="daily", geographic_scope="Hulhule airport (not Male island)", timestamp_timezone="GSOD day; boundary unverified",
        accumulation_window="GSOD daily; precip_flag gives composition", units="metric (degC, hPa, km, km/h, mm)",
        missing="blank (raw 99.99 converted to blank)", flags="precip_flag", licence="NOAA open data", nature="measured (converted)",
        downloaded="about 2026-11-14 (compiler)"),
    MB + "data/male_sea_level_waves_*": dict(
        provider="Open-Meteo Marine API (per compiler README)", source_url="https://open-meteo.com/en/docs/marine-weather-api",
        source_type="modelled_sea_level_and_waves", time_resolution="hourly", geographic_scope="Male grid point (coordinates not recorded)",
        timestamp_timezone="time_local: undocumented; tide correlation with UHSLC consistent with UTC+4 or UTC+5",
        accumulation_window="instantaneous", units="m (sea level relative to MSL, model datum)", missing="blank",
        licence="Open-Meteo CC BY 4.0", nature="modelled", downloaded="about 2026-11-14 (compiler)"),
    MB + "data/male_forecast_hourly_*": dict(
        provider="MET Norway Locationforecast (per compiler README)", source_url="https://api.met.no/weatherapi/locationforecast/2.0/documentation",
        source_type="forecast_snapshot", time_resolution="hourly then 6-hourly", geographic_scope="Male point",
        timestamp_timezone="UTC (Z suffix)", accumulation_window="precip_next_1h_mm / precip_next_6h_mm forward windows",
        units="degC, %, hPa, m/s, mm", licence="MET Norway CC BY 4.0 / NLOD", nature="forecast", downloaded="2026-11-14 (compiler)"),
    MB + "data/male_daily_features_*": dict(
        provider="Compiler merge of the ERA5, GSOD, sea-level and incident files", source_type="derived_feature_label_table",
        time_resolution="daily", geographic_scope="Male (ERA5 point) + Hulhule station", timestamp_timezone="nominal day (undocumented)",
        accumulation_window="same-day sums; prev3d/prev7d windows not documented", units="mm, km/h, deg, hPa, %, degC, m",
        missing="blank", licence="derived", nature="derived (flood_reported=0 means no report found)", downloaded="2026-11-14 (compiler)"),
    MB + "data/flood*": dict(
        provider="AI-assisted news compilation (male-flood-basis, 14 Nov 2026)", source_type="news_derived_compilation",
        time_resolution="date text", geographic_scope="Greater Male (Male, Hulhumale, Hulhule, Villimale)",
        licence="secondary; source articles under publisher copyright", nature="news_derived", downloaded="2026-11-14 (compiler)"),
    "male_flood_inventory.csv": dict(
        provider="Export of an earlier chat research session (record_provenance column)", source_type="news_and_official_record_candidates",
        time_resolution="date windows; some local clock times with qualifiers", geographic_scope="Male island (as asserted per row)",
        timestamp_timezone="event clocks interpreted as local per article; publication timezone unknown",
        licence="secondary; source articles under publisher copyright", nature="news_derived + official_record_leads", downloaded="2026-11-22 (export_date)"),
}


def meta_for(rel):
    for pat, m in META.items():
        if fnmatch.fnmatchcase(rel, pat):
            return m
    if rel.startswith(("derived/", "verification/")):
        return dict(provider="Project analysis (this repository)", source_type="derived_output", nature="derived",
                    licence="project output; inherits source licences")
    return {}


# ---------------------------------------------------------------- profiling
DATE_HINTS = ("date", "time", "DATE", "anchor", "start", "end")


def read_csv(path, skiprows=None):
    return pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8-sig", low_memory=False, skiprows=skiprows)


def profile_csv(path, rel):
    skip = [1] if "UHSLC" in rel else None  # units row after header
    d = read_csv(path, skip)
    blank = (d == "").sum()
    out = dict(format="CSV", row_count=len(d), column_count=d.shape[1], variables=";".join(d.columns),
               missing_cells=int(blank.sum()), duplicate_rows=int(d.duplicated().sum()), profiling="complete")
    dates = []
    for c in d.columns:
        if any(h in c for h in DATE_HINTS):
            s = pd.to_datetime(d[c].str.slice(0, 19).replace("", None), errors="coerce", format="mixed")
            if s.notna().sum() >= max(1, 0.5 * (d[c] != "").sum()):
                dates.append((c, s))
    if dates:
        c, s = dates[0]
        out.update(coverage_start=str(s.min())[:19], coverage_end=str(s.max())[:19], time_column=c,
                   duplicate_timestamps=int(s.dropna().duplicated().sum()))
    lat = next((c for c in d.columns if c.lower() in ("latitude", "lat", "centroid_lat", "requested_latitude")), None)
    lon = next((c for c in d.columns if c.lower() in ("longitude", "lon", "centroid_lon", "requested_longitude")), None)
    if lat and lon:
        la, lo = pd.to_numeric(d[lat], errors="coerce"), pd.to_numeric(d[lon], errors="coerce")
        ok = la.between(-90, 90) & lo.between(-180, 180)
        out.update(spatial_coordinates=f"{lat}/{lon}: lat {la.min()}..{la.max()}, lon {lo.min()}..{lo.max()}",
                   invalid_coordinates=int((~ok & la.notna()).sum()), missing_coordinates=int(la.isna().sum()))
    out["_df"] = d
    out["_blank"] = blank
    return out


def profile_geojson(path):
    g = json.loads(Path(path).read_text(encoding="utf-8"))
    feats = g.get("features", [])
    types, keys, xs, ys = {}, set(), [], []

    def walk(c):
        if isinstance(c, (list, tuple)) and c and isinstance(c[0], (int, float)):
            xs.append(c[0]); ys.append(c[1])
        elif isinstance(c, (list, tuple)):
            for x in c:
                walk(x)
    for f in feats:
        geom = f.get("geometry") or {}
        types[geom.get("type")] = types.get(geom.get("type"), 0) + 1
        keys |= set((f.get("properties") or {}).keys())
        walk(geom.get("coordinates", []))
    xs, ys = np.array(xs), np.array(ys)
    bad = int(((xs < -180) | (xs > 180) | (ys < -90) | (ys > 90)).sum()) if len(xs) else 0
    return dict(format="GeoJSON", row_count=len(feats), column_count=len(keys), variables=";".join(sorted(keys)),
                spatial_coordinates=(f"bbox lon {xs.min():.5f}..{xs.max():.5f}, lat {ys.min():.5f}..{ys.max():.5f}; "
                                     f"geometry {types}; CRS {g.get('crs', {}).get('properties', {}).get('name', 'not stated (GeoJSON default WGS84)')}") if len(xs) else "",
                invalid_coordinates=bad, null_geometries=types.get(None, 0), profiling="complete")


def profile_tif(path):
    import rasterio
    with rasterio.open(path) as r:
        a = r.read(1, masked=True)
        v = a.compressed()
        return dict(format="GeoTIFF", row_count=int(v.size), column_count=r.count,
                    variables=f"band1 {r.dtypes[0]}; nodata={r.nodata}",
                    spatial_coordinates=f"CRS {r.crs}; {r.width}x{r.height} px; res {r.res[0]:.6f}x{r.res[1]:.6f}; bounds {tuple(round(b, 5) for b in r.bounds)}",
                    value_range=f"valid cells {v.size}; min {v.min() if v.size else ''}; median {np.median(v) if v.size else ''}; max {v.max() if v.size else ''}",
                    missing_cells=int(a.mask.sum()) if np.ndim(a.mask) else 0, profiling="complete (all pixels; row_count = valid cells)")


def profile_parquet(path):
    f = pq.ParquetFile(path)
    md = f.metadata
    nulls, mins, maxs = {}, {}, {}
    for rg in range(md.num_row_groups):
        for ci in range(md.num_columns):
            col = md.row_group(rg).column(ci)
            st = col.statistics
            name = col.path_in_schema
            if st is not None and st.has_null_count:
                nulls[name] = nulls.get(name, 0) + st.null_count
    # chunked scan of the small columns only (geometry never loaded)
    uu, smin, emax, n_bad_order, n_rows, starts_by_year = set(), None, None, 0, 0, {}
    dup_uuid = 0
    for b in f.iter_batches(batch_size=200_000, columns=["uuid", "start_date", "end_date"]):
        t = b.to_pandas()
        n_rows += len(t)
        for u in t.uuid:
            if u in uu:
                dup_uuid += 1
            else:
                uu.add(u)
        smin = min(filter(None, [smin, t.start_date.min()]))
        emax = max(filter(None, [emax, t.end_date.max()]))
        n_bad_order += int((t.end_date < t.start_date).sum())
    geo = json.loads(md.metadata.get(b"geo", b"{}") or "{}") if md.metadata else {}
    crs = geo.get("columns", {}).get("geometry", {}).get("crs", "not stated in geo metadata (WGS84 default)")
    return dict(format="GeoParquet", row_count=n_rows, column_count=md.num_columns,
                variables=";".join(f.schema_arrow.names), coverage_start=smin, coverage_end=emax,
                duplicate_rows=dup_uuid, duplicate_note=f"duplicate uuid values: {dup_uuid}; end_date<start_date rows: {n_bad_order}",
                missing_cells=sum(nulls.values()), spatial_coordinates=f"WKB polygons; CRS {crs if isinstance(crs, str) else 'PROJJSON in geo metadata'}; {md.num_row_groups} row groups",
                profiling="metadata + chunked scan of uuid/start_date/end_date (geometry not loaded)")


# ---------------------------------------------------------------- cleaning (working copies in 02_interim)
def clean_gsod(repo, dest, log):
    rows = []
    for y in (2024, 2025):
        rel = f"{SP}rainfall/noaa_gsod_{y}_43555099999.csv"
        d = read_csv(repo / rel)
        n_in = len(d)
        d.columns = [c.strip() for c in d.columns]
        raw = d["PRCP"].str.strip()
        val = pd.to_numeric(raw, errors="coerce")
        d["prcp_raw_in"] = raw
        d["prcp_flag"] = d["PRCP_ATTRIBUTES"].str.strip()  # NOAA flag letter A-I
        miss = val.eq(99.99) | val.isna()
        d["prcp_missing"] = miss.map({True: "missing", False: ""})
        d["prcp_mm"] = (val * 25.4).round(1).where(~miss)
        d["prcp_is_zero"] = (val.eq(0) & ~miss)
        d["source_file"] = rel
        rows.append(d)
        log.append(dict(step="gsod_clean", input=rel, input_rows=n_in, output_rows=len(d),
                        decision="PRCP inches->mm (x25.4, documented NOAA units); 99.99 -> missing (not zero); raw value and flag kept; date left as GSOD day (local-day alignment unresolved)"))
    out = pd.concat(rows)
    dates = pd.to_datetime(out["DATE"])
    full = pd.date_range(dates.min(), dates.max(), freq="D")
    absent = sorted(set(full.date) - set(dates.dt.date))
    p = dest / "02_interim/weather_aligned/hulhule_gsod_clean_2024-2025_v001.csv"
    p.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(p, index=False, encoding="utf-8")
    return out, absent, p


def clean_uhslc(repo, dest, log):
    rel = f"{SP}tides/UHSLC_Male_Record1082_Hourly_2024.csv"
    d = read_csv(repo / rel, skiprows=[1])
    n_in = len(d)
    d["sea_level_raw"] = d["sea_level"]
    d["sea_level_mm_station_zero"] = pd.to_numeric(d["sea_level"], errors="coerce")
    d["sea_level_missing"] = d["sea_level_mm_station_zero"].isna().map({True: "missing", False: ""})
    d["time_utc"] = pd.to_datetime(d["time"], utc=True).dt.strftime("%Y-%m-%dT%H:%M:%S+00:00")
    t = pd.to_datetime(d["time"], utc=True)
    gaps = int((t.diff().dropna() != pd.Timedelta(hours=1)).sum())
    p = dest / "02_interim/weather_aligned/uhslc_male_1082_hourly_2024_clean_v001.csv"
    d.to_csv(p, index=False, encoding="utf-8")
    log.append(dict(step="uhslc_clean", input=rel, input_rows=n_in, output_rows=len(d),
                    decision="units row removed; numeric mm relative to station zero (no datum change); blank -> missing; explicit +00:00 UTC timestamp; local-time conversion not applied"))
    return d, gaps, p


def daily_coverage(repo, dest, gsod, uhslc, log):
    """One row per nominal day 2020-01-01..2026-11-13: which series exist. No labels created."""
    era = read_csv(repo / f"{MB}data/male_reanalysis_hourly_2020-2026.csv")
    era["day"] = era.time_local.str.slice(0, 10)
    e = era.groupby("day").agg(era5_hours=("precipitation_mm", lambda s: int((s != "").sum())))
    era_d = read_csv(repo / f"{MB}data/male_reanalysis_daily_2020-2026.csv").set_index("date")
    sl = read_csv(repo / f"{MB}data/male_sea_level_waves_hourly_2022-2026.csv")
    sl["day"] = sl.time_local.str.slice(0, 10)
    s = sl.groupby("day").agg(modelled_sea_level_hours=("sea_level_height_msl_m", lambda x: int((x != "").sum())))
    st = read_csv(repo / f"{MB}data/hulhule_station_daily_2020-2025.csv").set_index("date")
    u = uhslc.assign(day=uhslc.time_utc.str.slice(0, 10)).groupby("day").agg(
        observed_sea_level_hours_utc_day=("sea_level_mm_station_zero", lambda x: int(x.notna().sum())))
    days = pd.date_range("2020-01-01", "2026-11-13", freq="D").strftime("%Y-%m-%d")
    c = pd.DataFrame(index=days)
    c.index.name = "date_nominal"
    c = c.join(e).join(s).join(u)
    c["era5_daily_precip_mm"] = era_d["precipitation_sum_mm"].reindex(days)
    sp = st["precip_mm"].reindex(days)
    c["hulhule_gsod_precip_mm"] = sp
    c["hulhule_gsod_status"] = np.where(~pd.Index(days).isin(st.index), "no_row",
                                np.where(sp.fillna("") == "", "missing_value", np.where(pd.to_numeric(sp, errors="coerce") == 0, "zero", "positive")))
    c[["era5_hours", "modelled_sea_level_hours", "observed_sea_level_hours_utc_day"]] = c[["era5_hours", "modelled_sea_level_hours", "observed_sea_level_hours_utc_day"]].fillna(0).astype(int)
    c["era5_complete"] = c.era5_hours.eq(24)
    c["modelled_sea_complete"] = c.modelled_sea_level_hours.eq(24)
    c["station_rain_present"] = c.hulhule_gsod_status.isin(["zero", "positive"])
    c["observed_sea_complete_utc_day"] = c.observed_sea_level_hours_utc_day.eq(24)
    c["flood_label"] = "unlabelled"  # explicit: no day is labelled by this table
    p = dest / "02_interim/weather_aligned/daily_series_coverage_2020-2026_v001.csv"
    c.to_csv(p, encoding="utf-8")
    log.append(dict(step="daily_coverage", input="ERA5 hourly/daily, modelled sea level, Hulhule GSOD (compiled), UHSLC clean",
                    input_rows=len(era), output_rows=len(c),
                    decision="nominal day of each file's own time label; days with no series value are recorded, not imputed; observed sea level grouped by UTC day; flood_label fixed to 'unlabelled'"))
    return c, p


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--dest", required=True)
    a = ap.parse_args()
    repo, dest = Path(a.repo).resolve(), Path(a.dest).resolve()
    assert (dest / "TEMPLATE_GUIDE.md").exists(), "dest must be the extracted male_flood_ai_data template"
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    cat = dest / "00_catalog"

    files = list(repo_files(repo))
    hashes = {r: sha256(repo / r) for r in files}
    by_hash = {}
    for r, h in hashes.items():
        by_hash.setdefault(h, []).append(r)

    # ---- copy + verify
    mapping = []
    for r in files:
        size = (repo / r).stat().st_size
        dup = [x for x in by_hash[hashes[r]] if x != r]
        base = dict(original_path=r, original_filename=Path(r).name, size_bytes=size, sha256=hashes[r],
                    identical_repo_files=";".join(dup))
        if Path(r).name in NOT_COPIED and "/" not in r:
            mapping.append({**base, "destination_path": "", "role": "not_copied", "copy_action": "excluded",
                            "checksum_verified": "", "needs_human_classification": "", "notes": NOT_COPIED[Path(r).name]})
            continue
        rts = routes_for(r)
        if not rts:
            mapping.append({**base, "destination_path": "", "role": "unrouted", "copy_action": "not_copied",
                            "checksum_verified": "", "needs_human_classification": "yes", "notes": "No rule matched; classify manually."})
            continue
        for dest_rel, role, note in rts:
            target = dest / dest_rel
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                action = "already_present_identical" if sha256(target) == hashes[r] else "CONFLICT_existing_differs_not_overwritten"
            else:
                shutil.copy2(repo / r, target)
                action = "copied"
            ok = sha256(target) == hashes[r] if "CONFLICT" not in action else False
            mapping.append({**base, "destination_path": dest_rel, "role": role, "copy_action": action,
                            "checksum_verified": "yes" if ok else "NO",
                            "needs_human_classification": "yes" if note.startswith("Needs human") else "",
                            "notes": note})
    # Downloads copy of the import (outside the repo): record relationship only
    dl = Path.home() / "Downloads/male_flood_inventory.csv"
    if dl.exists():
        mapping.append(dict(original_path=str(dl), original_filename=dl.name, size_bytes=dl.stat().st_size, sha256=sha256(dl),
                            identical_repo_files=";".join(by_hash.get(sha256(dl), [])), destination_path="", role="duplicate_outside_repo",
                            copy_action="not_copied_identical_duplicate", checksum_verified="", needs_human_classification="",
                            notes="Byte-identical to the repo copy that was imported."))
    mp = pd.DataFrame(mapping)
    mp.to_csv(cat / "file_mapping.csv", index=False, encoding="utf-8-sig")

    # ---- duplicates register
    dups = [dict(sha256=h, files=";".join(v), n=len(v)) for h, v in by_hash.items() if len(v) > 1]
    pd.DataFrame(dups, columns=["sha256", "files", "n"]).to_csv(cat / "duplicate_files_by_checksum.csv", index=False, encoding="utf-8-sig")

    # ---- profile datasets
    data_ext = (".csv", ".geojson", ".tif", ".parquet")
    inv, quality, dictionary = [], [], []
    primary = mp[mp.copy_action.isin(["copied", "already_present_identical"])].drop_duplicates("original_path")
    ds_n = 0
    for _, m in primary.iterrows():
        r = m.original_path
        if not r.lower().endswith(data_ext):
            continue
        ds_n += 1
        dsid = f"DS{ds_n:04d}"
        p = repo / r
        try:
            if r.endswith(".csv"):
                prof = profile_csv(p, r)
            elif r.endswith(".geojson"):
                prof = profile_geojson(p)
            elif r.endswith(".tif"):
                prof = profile_tif(p)
            else:
                prof = profile_parquet(p)
        except Exception as ex:  # keep going; record the failure
            prof = dict(format=Path(r).suffix, profiling=f"FAILED: {ex}")
        md = meta_for(r)
        df, blank = prof.pop("_df", None), prof.pop("_blank", None)
        inv.append(dict(
            dataset_id=dsid, relative_path=m.destination_path, original_filename=Path(r).name,
            provider=md.get("provider", "unknown"), source_url=md.get("source_url", "unknown").replace("{year}", "".join(c for c in Path(r).name if c.isdigit())[:4]),
            source_type=md.get("source_type", "unknown"), variables=prof.get("variables", ""),
            time_resolution=md.get("time_resolution", "not applicable" if prof.get("format") in ("GeoJSON", "GeoTIFF") else "unknown"),
            geographic_scope=md.get("geographic_scope", "unknown"),
            coverage_start=prof.get("coverage_start", ""), coverage_end=prof.get("coverage_end", ""),
            timestamp_timezone=md.get("timestamp_timezone", "unknown" if prof.get("coverage_start") else "not applicable"),
            accumulation_window=md.get("accumulation_window", "unknown" if "rain" in r.lower() or "precip" in r.lower() else "not applicable"),
            units=md.get("units", "unknown"), missing_value_codes=md.get("missing", "blank cell"), quality_flags=md.get("flags", "none documented"),
            downloaded_at_utc=md.get("downloaded", "unknown"), licence_or_access_conditions=md.get("licence", "unknown"),
            sha256=m.sha256, inventory_status="imported" if md.get("provider") else "metadata_incomplete",
            notes=m.notes, original_repo_path=r, format=prof.get("format", ""), size_bytes=m.size_bytes,
            row_count=prof.get("row_count", ""), column_count=prof.get("column_count", ""),
            spatial_coordinates=prof.get("spatial_coordinates", ""), data_nature=md.get("nature", "unknown"),
            duplicate_records=prof.get("duplicate_note", prof.get("duplicate_rows", "")),
            duplicate_timestamps=prof.get("duplicate_timestamps", ""), profiling_completeness=prof.get("profiling", ""),
            coverage_basis_column=prof.get("time_column", ""),
            identical_files=m.identical_repo_files))
        for k in ("missing_cells", "duplicate_rows", "duplicate_timestamps", "invalid_coordinates", "missing_coordinates", "null_geometries", "value_range"):
            if k in prof:
                quality.append(dict(dataset_id=dsid, relative_path=m.destination_path, check=k, result=prof[k], notes=""))
        if df is not None:
            for c in df.columns:
                s = df[c]
                num = pd.to_numeric(s.replace("", None), errors="coerce")
                kind = "numeric" if num.notna().sum() == (s != "").sum() and (s != "").any() else "text"
                dictionary.append(dict(dataset_id=dsid, column_name=c, description="", data_type=kind,
                                       units="", allowed_values=(";".join(sorted(s.unique()))[:300] if s.nunique() <= 8 else ""),
                                       missing_value_meaning=f"blank in {int(blank[c])} of {len(s)} rows",
                                       relative_path=m.destination_path,
                                       observed_range=(f"{num.min()}..{num.max()}" if kind == "numeric" else "")))
        elif prof.get("format") == "GeoJSON":
            for k in prof["variables"].split(";"):
                if k:
                    dictionary.append(dict(dataset_id=dsid, column_name=k, description="GeoJSON feature property", data_type="",
                                           units="", allowed_values="", missing_value_meaning="", relative_path=m.destination_path, observed_range=""))
    invdf = pd.DataFrame(inv)

    # ---- cleaning
    log = []
    gsod, absent, gp = clean_gsod(repo, dest, log)
    uh, uh_gaps, up = clean_uhslc(repo, dest, log)
    cov, cp = daily_coverage(repo, dest, gsod, uh, log)
    imp = read_csv(repo / "male_flood_inventory.csv")
    n_imp = len(imp)
    for c in ("event_start_date", "event_end_date"):
        imp[c + "_valid_iso"] = pd.to_datetime(imp[c], format="%Y-%m-%d", errors="coerce").notna()
    imp["window_days"] = (pd.to_datetime(imp.event_end_date) - pd.to_datetime(imp.event_start_date)).dt.days + 1
    pub = pd.to_datetime(imp.source_publication_date_as_displayed.replace("", None), format="%Y-%m-%d", errors="coerce")
    imp["publication_minus_event_start_days"] = (pub - pd.to_datetime(imp.event_start_date)).dt.days
    imp["end_before_start"] = imp.window_days < 1
    imp["multi_day_window_not_daily_truth"] = imp.window_days > 1
    imp["rain_start_time_with_qualifier"] = np.where(imp.rain_start_time_local != "",
                                                     (imp.rain_start_time_qualifier + " " + imp.rain_start_time_local).str.strip(), "")
    ip = dest / "02_interim/event_candidates/male_flood_inventory_clean_v001.csv"
    imp.to_csv(ip, index=False, encoding="utf-8-sig")
    log.append(dict(step="import_clean", input="02_interim/event_candidates/male_flood_inventory.csv", input_rows=n_imp, output_rows=len(imp),
                    decision="all original columns unchanged as text; added ISO-date validity, window length, publication lag, multi-day flag and qualifier-preserving rain-start text; no timezone conversion"))
    pd.DataFrame(log).to_csv(dest / "02_interim/cleaning_log_v001.csv", index=False, encoding="utf-8-sig")

    # cleaned outputs also get inventory rows
    for p, src, desc in ((gp, "DS(GSOD raw 2024, 2025)", "Hulhule GSOD 2024-2025, PRCP mm with raw kept"),
                         (up, "DS(UHSLC 2024)", "UHSLC 2024 hourly with explicit UTC"),
                         (cp, "ERA5/sea/GSOD/UHSLC", "Per-day availability of each series; no labels"),
                         (ip, "male_flood_inventory.csv", "Import with validation columns")):
        ds_n += 1
        d = read_csv(p)
        invdf.loc[len(invdf)] = {**{k: "" for k in invdf.columns}, "dataset_id": f"DS{ds_n:04d}",
                                 "relative_path": p.relative_to(dest).as_posix(), "original_filename": p.name,
                                 "provider": "This organisation step (scripts/organise_male_flood_ai_data.py)", "source_type": "cleaned_working_copy",
                                 "variables": ";".join(d.columns), "row_count": len(d), "column_count": d.shape[1], "format": "CSV",
                                 "sha256": sha256(p), "size_bytes": p.stat().st_size, "inventory_status": "imported",
                                 "data_nature": "derived", "notes": f"{desc}. Derived from {src}. See 02_interim/cleaning_log_v001.csv.",
                                 "profiling_completeness": "complete", "downloaded_at_utc": now}

    # ---- specific quality checks with numbers
    g24 = gsod[gsod.source_file.str.contains("2024")]
    q = [
        ("GSOD raw 2024-2025", "dated_rows", len(gsod), "355 (2024) + 236 (2025)"),
        ("GSOD raw 2024-2025", "prcp_missing_99.99", int(gsod.prcp_missing.eq("missing").sum()), ";".join(gsod.loc[gsod.prcp_missing.eq("missing"), "DATE"])),
        ("GSOD raw 2024-2025", "prcp_nonmissing", int(gsod.prcp_missing.ne("missing").sum()), ""),
        ("GSOD raw 2024-2025", "prcp_zero_days", int(gsod.prcp_is_zero.sum()), "zero kept distinct from missing"),
        ("GSOD raw 2024-2025", "prcp_ge_25.4mm_days", int((gsod.prcp_mm >= 25.4).sum()),
         f"2024: {int((g24.prcp_mm >= 25.4).sum())}; 2025: {int((gsod[gsod.source_file.str.contains('2025')].prcp_mm >= 25.4).sum())}; before flag-based filtering"),
        ("GSOD raw 2024-2025", "absent_calendar_dates", len(absent), ";".join(map(str, absent))),
        ("GSOD raw 2024-2025", "prcp_flag_counts", json.dumps(gsod.prcp_flag.value_counts().to_dict()), "NOAA flag letters"),
        ("UHSLC 2024", "hourly_rows", len(uh), ""),
        ("UHSLC 2024", "missing_sea_level", int(uh.sea_level_missing.eq("missing").sum()), ""),
        ("UHSLC 2024", "irregular_time_steps", uh_gaps, "rows where step != 1 h"),
        ("UHSLC 2024", "range_mm_station_zero", f"{uh.sea_level_mm_station_zero.min()}..{uh.sea_level_mm_station_zero.max()}", "not flood depth; datum is station zero"),
        ("Daily coverage", "days_total", len(cov), "2020-01-01..2026-11-13 nominal days"),
        ("Daily coverage", "era5_complete_days", int(cov.era5_complete.sum()), ""),
        ("Daily coverage", "modelled_sea_complete_days", int(cov.modelled_sea_complete.sum()), ""),
        ("Daily coverage", "era5_and_modelled_sea_complete_days", int((cov.era5_complete & cov.modelled_sea_complete).sum()), ""),
        ("Daily coverage", "station_rain_present_days", int(cov.station_rain_present.sum()), "zero or positive GSOD value"),
        ("Daily coverage", "station_status_counts", json.dumps(cov.hulhule_gsod_status.value_counts().to_dict()), ""),
        ("Daily coverage", "era5_station_modelled_sea_all_present_days", int((cov.era5_complete & cov.modelled_sea_complete & cov.station_rain_present).sum()), ""),
        ("Daily coverage", "observed_sea_complete_utc_days", int(cov.observed_sea_complete_utc_day.sum()), "UHSLC 2024 only"),
        ("Daily coverage", "era5_and_observed_sea_complete_days", int((cov.era5_complete & cov.observed_sea_complete_utc_day).sum()), "nominal ERA5 day vs UTC tide day: alignment unresolved"),
    ]
    for name, check, res, note in q:
        quality.append(dict(dataset_id=name, relative_path="", check=check, result=res, notes=note))

    # ---- write catalogues (template headers first, extra columns after; keep any pre-existing rows)
    def write_ext(path, df):
        old = pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8-sig") if path.exists() else pd.DataFrame()
        cols = list(old.columns) + [c for c in df.columns if c not in old.columns]
        if len(old):  # preserve populated rows exactly
            df = pd.concat([old, df], ignore_index=True)
        df.reindex(columns=cols).to_csv(path, index=False, encoding="utf-8-sig")

    write_ext(cat / "dataset_inventory.csv", invdf)
    write_ext(cat / "data_dictionary.csv", pd.DataFrame(dictionary))
    pd.DataFrame(quality).to_csv(cat / "data_quality_summary.csv", index=False, encoding="utf-8-sig")
    print(json.dumps(dict(files=len(files), mapping_rows=len(mp), copied=int(mp.copy_action.eq("copied").sum()),
                          conflicts=int(mp.copy_action.str.contains("CONFLICT").sum()), unverified=int(mp.checksum_verified.eq("NO").sum()),
                          needs_human=int(mp.needs_human_classification.eq("yes").sum()), datasets=len(invdf), dup_groups=len(dups)), indent=1))
    for name, check, res, note in q:
        print(f"{name:22s} {check:42s} {str(res)[:90]}")


if __name__ == "__main__":
    main()
