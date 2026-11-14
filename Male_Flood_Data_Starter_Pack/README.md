# Male flood-data starter pack

Read Dataset_Catalogue.md and Male_Flood_Data_Research.pdf first. Checked14November2026. Contains actual downloaded data and carefully labelled source/request leads. No models have been trained and no new flood predictions are included.

## Start in QGIS

Open boundary/OneMap_Male_Island.geojson, mapping/male_osm_roads.geojson and one building alternative. Add WorldCover, WorldPop and the FABDEM clip as separate rasters. Vectors/raster horizontal CRS is WGS84/EPSG4326. Use an appropriate projected CRS (e.g. WGS84/UTM43N, EPSG32643) for metre-based lengths/areas; preserve originals and inspect datum/accuracy.

Mapping layers were clipped by an OSM island polygon; FABDEM was masked with the official OneMap polygon. Both boundaries are included. Reconcile coastline differences before joining layers. Current geometry may postdate historical floods. Raster grids intentionally remain at native spacing and do not align automatically.

## Key interpretation rules

- Building datasets are alternatives: do not concatenate counts. Google0.75 confidence is illustrative, not a precision guarantee. Footprints do not establish heights, household counts or complete paved cover.
- NOAA GlobalHourly files are airport meteorological reports. Checked AA precipitation groups are6/12/24-hour accumulations, not1-hour rainfall. Keep quality/condition flags and missing values; do not add overlapping totals. Read rainfall/README_RAINFALL.md.
- UHSLC2024 is hourly research-quality water level at a nearby Hulhule gauge:8,784 timestamps,8,659 valid and125missing. Its CSV has a units row after the header. Values are mm relative stationzero, not flood depth; do not compare directly to DEM heights without datum reconciliation.
- FABDEM30m is not a surveyed street DEM. Its Male median5.04m/max15.15m are unvalidated estimates, with possible residual urban/coast bias.
- WorldPop is a modelled population estimate/alpha release for broad exposure, not an official Male census total. WorldCover is2021 land cover, not a hydraulic imperviousness measurement.
- flood/event_candidates.csv contains only three city-level source/date leads, not flooded/dry location labels. DALA download bytes were not obtained.
- No open, complete street-level multi-event flood/dry inventory, detailed drainage GIS or high-resolution bare-earth Male DEM was verified. Agency access remains important.

## Provenance and licences

Dataset_Catalogue.json, source results/QA JSONs and File_Manifest.json record origins and modifications. Preserve dataset-specific terms; there is no single licence for the collection.

- OSM derivatives:©OpenStreetMap contributors, ODbL1.0, https://www.openstreetmap.org/copyright
- Microsoft:CDLA Permissive2.0; https://github.com/microsoft/GlobalMLBuildingFootprints
- Google OpenBuildings:CCBY4.0 chosen from provider's dual options; source https://sites.research.google/gr/open-buildings/ ; clipped/filtered derivatives identified in metadata.
- ESAWorldCover:CCBY4.0; Zanaga etal.2022, https://doi.org/10.5281/zenodo.7254221
- WorldPop:CCBY4.0; Bondarenko etal.2025, https://doi.org/10.5258/SOTON/WP00839
- FABDEM and its clipped derivative:CCBY-NC-SA4.0. Attribution and full licence are in elevation/FABDEM_readme.txt and FABDEM_license.txt. The derivative is licensed under the same terms. Noncommercial/sharealike terms apply to that data, not automatically every unrelated file.
- UHSLC:free use/redistribution per metadata; cite https://doi.org/10.7289/V5V40S7W
- NOAA/CHIRPS:retain provider attribution and source/QC metadata.
- OneMap:public access/download advertised; explicit reuse licence not identified in layer metadata. Confirm reuse terms before republishing.

No agency requests have been sent. The public reports are linked and summarised; their original full copyrighted PDFs are not included.
