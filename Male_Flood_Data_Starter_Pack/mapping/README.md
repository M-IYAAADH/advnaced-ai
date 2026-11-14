# Malé mapping and exposure data: retrieved starter layers

Retrieved 14 November 2026. These are real downloaded/cropped data, not example geometries or simulated observations. None of these datasets is a validated flood-label inventory.

All deliverable vector coordinates use EPSG:4326 (longitude, latitude). Clip boundary: the OpenStreetMap Malé island polygon, `osm_id=14391899`, selected from the Geofabrik Maldives GeoPackage. Original archive README records OSM data timestamp `2026-11-13T21:22:20Z`. This is a volunteer-mapped island boundary, not an official administrative boundary or certified coastline. Inspect recent reclamation, port edges and modelled shoreline before using it as a definitive study boundary.

## Files ready to package

| File | Verified content |
|---|---|
| male_osm_island_boundary.geojson | One polygon feature (multipart type); clip boundary, not an official survey |
| male_osm_roads.geojson | 571 clipped OSM road features; geometries may be road fragments, not one feature per whole street |
| male_osm_buildings.geojson | 933 clipped OSM building features after removing two explicitly tagged `building=no` objects |
| male_osm_landuse.geojson | 51 clipped OSM land-use features |
| male_osm_waterways.geojson | Empty collection: zero waterways mapped inside this boundary. This does **not** establish absence of storm drains |
| male_microsoft_buildings.geojson | 4,677 clipped machine-detected footprint candidates, current indexed release 13 August 2026; exact imagery dates not established |
| male_google_buildings_conf075.geojson | 5,773 clipped Google v3 footprint candidates with confidence >=0.75, inferred May 2023 |
| male_google_buildings.geojson | Optional larger audit alternative: all 10,077 clipped Google candidates (source confidence >=0.65) |
| male_worldcover_2021_10m.tif | ESA WorldCover 2021 v200 categorical raster, 227 x 153 cells, native ~10 m, clipped/masked; 24,188 non-nodata cells |
| male_worldpop_2025_100m.tif | WorldPop Global2 R2025A 2025 constrained population estimate, 23 x 15 cells, native 3 arcsec (~100 m), clipped/masked; 233 non-nodata cells |
| results.json | Dataset URLs, access verification, licences, attribution, clipping methods and numerical QA |
| worldpop_MDV_files_2025.json | Complete official API file/citation/licence metadata retrieved for MDV and 2025 |

All eight checked vector collections have zero invalid/empty geometries (apart from the intentionally empty waterways collection). TIFF metadata, dimensions and pixel values were read using GDAL 3.10.3 (`/usr/bin/python3` has `osgeo`; the default runtime Python does not).

## Licences and attribution

Keep these sources in separate layers and preserve their licence information. Do not concatenate different building providers and count the result as unique buildings.

- **OpenStreetMap**: © OpenStreetMap contributors, Open Database License 1.0 (ODbL). Source: https://download.geofabrik.de/asia/maldives.html . Actual archive: https://download.geofabrik.de/asia/maldives-latest-free.gpkg.zip . Licence/attribution: https://www.openstreetmap.org/copyright . Derived clip boundary is OSM data too.
- **Microsoft Global ML Building Footprints**: CDLA Permissive 2.0 according to the current official repository. Source: https://github.com/microsoft/GlobalMLBuildingFootprints . Exact 13 August 2026 tile-index and tile URLs are in results.json. Current global repository imagery date range is 2014-2024; the release date is not a capture date. This clip does not establish usable building heights; source sentinel values must not be interpreted as measured heights.
- **Google Open Buildings v3**: provider offers CC BY 4.0 or ODbL 1.0. Source: https://sites.research.google/gr/open-buildings/ . Maldives is explicitly in the official country list. Tile `3b3` was downloaded from https://storage.googleapis.com/open-buildings-data/v3/polygons_s2_level_4_gzip/3b3_buildings.csv.gz . May 2023 is the inference period, not a verified capture date for every feature. The chosen 0.75 threshold is illustrative; it is not a claim of 90% precision. Density/roof offsets/contiguous buildings require local appraisal.
- **ESA WorldCover 2021 v200**: CC BY 4.0. Credit: “ESA WorldCover project 2021 / Contains modified Copernicus Sentinel data (2021) processed by ESA WorldCover consortium”. Citation: Zanaga et al. (2022), https://doi.org/10.5281/zenodo.7254221 . Source catalogue: https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v200 . Direct COG tile: https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/ESA_WorldCover_10m_2021_v200_N03E072_Map.tif . The Malé window was read through HTTP ranges; the full tile was not downloaded.
- **WorldPop Global2 R2025A**: CC BY 4.0. Citation DOI: https://doi.org/10.5258/SOTON/WP00839 . Official API metadata: https://api.worldpop.org/v3/countries/MDV/files?year=2025 . Exact country raster: https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A/2025/MDV/v1/100m/constrained/mdv_pop_2025_CN_100m_R2025A_v1.tif . Complete author citation is retained in results.json and API metadata. Use modelled counts for broad exposure only; they are not household observations or official 2025 census totals.

## Reproducible clipping and limitations

Vector geometries were clipped using GDAL/OGR `ogr2ogr -clipsrc male_osm_island_boundary.geojson ... -t_srs EPSG:4326`. This actually intersects geometries with the OSM polygon rather than merely selecting bounding-box intersections. Road features near the boundary may be shortened or multipart.

Rasters were windowed using `gdal_translate -projwin` and then masked outside the polygon using inverse `gdal_rasterize`. Native source grid positions and pixel values were preserved with **no resampling**. Polygon raster masks use the default cell-centre rule, so edge-cell inclusion is uncertain. The WorldPop sum of retained cells should not be presented as an official city population estimate or assigned precisely to buildings.

WorldCover's built-up class is not a measured impervious fraction or drainage performance. Its 10 m cells mix narrow roads, roofs and ground cover. OSM and detected footprints represent different dates and coverage. No building-provider feature count has been validated against a complete local ground survey.

These layers support a pilot map and feature preparation. A credible flood model still needs independently verified flood observations, rainfall and locally suitable elevation/drainage data.

Dynamic World (`GOOGLE/DYNAMICWORLD/V1`) and GHSL GHS-BUILT-S R2023A are additional verified catalogue candidates, not downloaded Malé layers in this package. Dynamic World's `flooded_vegetation` class is not a ground-truth street-flood mask.
