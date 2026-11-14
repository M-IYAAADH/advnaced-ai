# Male flood-project dataset catalogue

Checked:14November2026. Study area:Male island proper; proposed process:rainfall-induced urban waterlogging.

Downloaded means file bytes and content were inspected. Catalogue-only and request-only sources are explicitly labelled. This starter pack is not a joined or validated flood-training dataset.

## B1 | Official OneMap Male island polygon

- Role:Study boundary
- Access:Downloaded and inspected
- Detail:Vector island outline; EPSG:4326
- Coverage:One Male polygon, OBJECTID1442, FCODE LD0442; service island_20240509
- Source:[https://readme.onemap.mv/](https://readme.onemap.mv/)
- Included files:boundary/OneMap_Male_Island.geojson
- Main limitation:Verify current reclamation/coastline and observation-era boundary. Service date is not proof of a current survey.
- Licence/access terms:Public access/download advertised; no explicit open-reuse licence identified in layer metadata; confirm terms.

## M1 | OpenStreetMap roads and land use

- Role:Road geometry / urban context
- Access:Downloaded, clipped and geometry-checked
- Detail:571 road features;51 land-use features
- Coverage:OSM snapshot2026-11-13; Male OSM island clip
- Source:[https://download.geofabrik.de/asia/maldives.html](https://download.geofabrik.de/asia/maldives.html)
- Included files:mapping/male_osm_roads.geojson, mapping/male_osm_landuse.geojson
- Main limitation:Road centre-lines are not drain locations or capacity. Mapping completeness varies.
- Licence/access terms:ODbL 1.0

## M2 | OpenStreetMap building footprints

- Role:Building-footprint alternative
- Access:Downloaded, cleaned and geometry-checked
- Detail:933 polygons after removing2 building=no records
- Coverage:Same OSM boundary and source snapshot
- Source:[https://download.geofabrik.de/asia/maldives.html](https://download.geofabrik.de/asia/maldives.html)
- Included files:mapping/male_osm_buildings.geojson
- Main limitation:Incomplete coverage; compare visually with other alternatives. No validated height or household count.
- Licence/access terms:ODbL 1.0

## M3 | Microsoft Global ML Building Footprints

- Role:Building-footprint alternative
- Access:Downloaded, clipped and geometry-checked
- Detail:4,677 candidate footprint polygons
- Coverage:Release index2026-08-13; capture dates for local imagery not established
- Source:[https://github.com/microsoft/GlobalMLBuildingFootprints](https://github.com/microsoft/GlobalMLBuildingFootprints)
- Included files:mapping/male_microsoft_buildings.geojson
- Main limitation:Model detections, not surveyed truth. Placeholder height/confidence values must not be used as real measurements.
- Licence/access terms:CDLA Permissive 2.0 (current official repository)

## M4 | Google Open Buildings v3

- Role:Building-footprint alternative
- Access:Downloaded, clipped, filtered and geometry-checked
- Detail:5,773 detections at confidence>=0.75;10,077 in full audit file
- Coverage:InferenceMay2023; tile3b3; imagery dates not established
- Source:[https://sites.research.google/gr/open-buildings/](https://sites.research.google/gr/open-buildings/)
- Included files:mapping/male_google_buildings_conf075.geojson, mapping/male_google_buildings.geojson
- Main limitation:Chosen0.75 threshold is not a promised precision. Do not add counts across Google,Microsoft andOSM; duplicates and different segmentation.
- Licence/access terms:CC BY 4.0 or ODbL1.0 (provider offers choice)

## M5 | ESA WorldCover2021v200

- Role:Land-cover predictor
- Access:Actual pixels downloaded and masked
- Detail:Nominal10m;227x153 bounding grid;24,188 valid cells
- Coverage:Observation year2021
- Source:[https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v200](https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v200)
- Included files:mapping/male_worldcover_2021_10m.tif
- Main limitation:Built-up class is not measured imperviousness. Narrow streets are mixed pixels; date-match to events.
- Licence/access terms:CC BY4.0

## M6 | WorldPop Global2 R2025A population2025

- Role:Optional exposure layer
- Access:Actual country TIFF downloaded; Male crop supplied
- Detail:Nominal100m;23x15 bounding grid;233 valid cells
- Coverage:2025 modelled population per cell; alpha-release product
- Source:[https://api.worldpop.org/v3/countries/MDV/files?year=2025](https://api.worldpop.org/v3/countries/MDV/files?year=2025)
- Included files:mapping/male_worldpop_2025_100m.tif
- Main limitation:Use broad exposure, not household locations or flood labels. Boundary masking changes totals. Do not quote clipped sum as official census.
- Licence/access terms:CC BY4.0

## E1 | FABDEM V1-2

- Role:Coarse exploratory elevation comparator
- Access:Original tile downloaded; official-boundary clip checked
- Detail:1arcsecond(~30m);48x70 bounding crop;2,169 inside-island samples
- Coverage:N04E073; WGS84/EGM2008; original Copernicus source-era terrain
- Source:[https://data.bris.ac.uk/datasets/s5hqmjcdj8yo2ibzi9b4ew3sn/](https://data.bris.ac.uk/datasets/s5hqmjcdj8yo2ibzi9b4ew3sn/)
- Included files:elevation/Male_FABDEM_30m_masked.tif, elevation/N04E073_FABDEM_V1-2.tif
- Main limitation:Not validated against local survey. Median5.04m,max15.15m and65zeros warrant urban-bias/reclamation checks. Cannot establish street flood depth.
- Licence/access terms:CC BY-NC-SA4.0; retain official attribution and ShareAlike for adapted FABDEM.

## E2 | Copernicus GLO-30

- Role:Alternative global surface model
- Access:Catalogue verified; no second raster downloaded
- Detail:1arcsecond(~30m)DSM
- Coverage:Global product; source-era coast and surface
- Source:[https://dataspace.copernicus.eu/explore-data/data-collections/copernicus-contributing-missions/collections-description/COP-DEM](https://dataspace.copernicus.eu/explore-data/data-collections/copernicus-contributing-missions/collections-description/COP-DEM)
- Included files:None; source/request lead only
- Main limitation:Includes buildings/vegetation; global vertical specification does not establish Male accuracy.
- Licence/access terms:Copernicus DEM licence; attribution required.

## E3 | Local ground survey / DEM

- Role:Preferred elevation input
- Access:Request required; public high-resolution Male DEM not located
- Detail:Ask for actual resolution, vertical accuracy, datum and survey dates
- Coverage:Male island proper; current and historical reclamation
- Source:[https://www.gazette.gov.mv/iulaan/303525](https://www.gazette.gov.mv/iulaan/303525)
- Included files:None; source/request lead only
- Main limitation:The2023 DEM/masterplan EOI was cancelled12Aug2024. Do not infer delivery from that notice. Ask separately about survey inputs behind completed stormwater designs.
- Licence/access terms:Agency permission and dataset-specific terms.

## D1 | Completed Male stormwater designs and surveys

- Role:Drainage network / capacity / survey inputs
- Access:Completion documented; underlying files request-only
- Detail:Ask for GIS/CAD, survey points, inverts, capacities, pumps, outfalls and model inputs
- Coverage:WorldBank July2024 report says Male detailed designs/tender docs completedMay2024
- Source:[https://documents1.worldbank.org/curated/en/099110624015517827/pdf/P163957-b07c3d4e-8d19-42d6-922e-85953c240e40.pdf](https://documents1.worldbank.org/curated/en/099110624015517827/pdf/P163957-b07c3d4e-8d19-42d6-922e-85953c240e40.pdf)
- Included files:None; source/request lead only
- Main limitation:Design completion is not proof of a downloadable asset database or installed/current network. Scope and custodian access must be confirmed.
- Licence/access terms:Agency permission and consultant/client terms.

## F1 | NDMA Male rainwater incident table

- Role:Candidate event dates / source records
- Access:Public HTML inspected; complete spatial inventory not found
- Detail:Incident date and location text; no full flood footprint
- Coverage:Visible2023-10-01 Male rainwater record
- Source:[https://ndma.gov.mv/en/statistics/atoll/21/incident](https://ndma.gov.mv/en/statistics/atoll/21/incident)
- Included files:flood/event_candidates.csv
- Main limitation:Three deidentified city-level candidates supplied across sources are not street training labels; unreported is not observed dry.
- Licence/access terms:Public report use with attribution; request permission for detailed records.

## F2 | NDMA DALA statistics

- Role:Aggregate event context
- Access:Download products advertised; CSV bytes not fetched
- Detail:Monthly/island/atoll and impact aggregates
- Coverage:Dynamic public portal; actual year/product coverage to confirm
- Source:[https://stats.ndma.gov.mv/download-statistics](https://stats.ndma.gov.mv/download-statistics)
- Included files:None; source/request lead only
- Main limitation:Public API attempt returned403. Do not claim downloads verified or use aggregate counts as per-street labels.
- Licence/access terms:Confirm download terms with provider.

## F3 | Council VLR2025 and underlying disaster plan

- Role:Local hazard context / data-request lead
- Access:Official report inspected; underlying event maps request-only
- Detail:City/ward summaries; selected event dates
- Coverage:2019-2024 major surface-water summary in2025 report
- Source:[https://cdn.malecity.gov.mv/website/documents/6zqnEssfa8YfgaNZkf_I0-VLR_Male_Small%20file%20size.pdf](https://cdn.malecity.gov.mv/website/documents/6zqnEssfa8YfgaNZkf_I0-VLR_Male_Small%20file%20size.pdf)
- Included files:None; source/request lead only
- Main limitation:Ask for underlying Draft Male City Disaster Management Plan2025 event/hazard maps, deidentified observations and coverage. Do not copy entire report into data pack.
- Licence/access terms:Council report copyright; underlying-data permission required.

## R1 | MMS historical rainfall

- Role:Rainfall / weather
- Access:Request required
- Detail:Hourly offered in the request form; subhourly availability unverified.
- Coverage:Request Male island gauges and the nearest available Hulhule station; require station metadata.
- Source:[https://www.meteorology.gov.mv/climate-data](https://www.meteorology.gov.mv/climate-data)
- Included files:None; source/request lead only
- Main limitation:Primary source for short-duration local rainfall Official form indexed; no data requested or obtained; current website may redirect.
- Licence/access terms:Complementary to Maldivian nationals and qualifying research; application purpose only; no third-party redistribution without written MMS permission

## R2 | NOAA ISD Global Hourly / Velana Intl

- Role:Rainfall / weather
- Access:Open download verified
- Detail:Hourly/synoptic meteorological reports; precipitation groups in the tested years are 6-, 12- and 24-hour totals, not hourly rainfall.
- Coverage:2024 calendar year and 2025 Jan 1-Aug 24 downloaded. Station-history metadata spans 1981 Jan 1-2025 Aug 24 with possible gaps.
- Source:[https://noaa-global-hourly-pds.s3.amazonaws.com/2024/43555099999.csv](https://noaa-global-hourly-pds.s3.amazonaws.com/2024/43555099999.csv)
- Included files:rainfall/noaa_global_hourly_2024_43555099999.csv, rainfall/noaa_global_hourly_2025_43555099999.csv, rainfall/noaa_precipitation_accumulations_2024.csv, rainfall/noaa_precipitation_accumulations_2025.csv
- Main limitation:Measured nearby-station context at 6-hour/daily scale. Obtain MMS data for hourly/subhourly rainfall bursts. 2024: 10,784 meteorological rows; 1,666 nonempty AA groups, including 30 missing depths. 2025: 7,198 rows; 1,128 AA groups, including 21 missing depths. No 1-hour AA precipitation group found in either year. Quality and condition flags retained.
- Licence/access terms:Free download without login; cite NOAA and station source.

## R3 | NOAA GSOD / Velana Intl

- Role:Rainfall / weather
- Access:Open download verified
- Detail:Daily derived summaries.
- Coverage:2024: 355 dates, 354 nonmissing PRCP. 2025: 236 dates through Aug 24, all 236 with PRCP. Hulhule airport is not Male island proper.
- Source:[https://www.ncei.noaa.gov/data/global-summary-of-the-day/access/2024/43555099999.csv](https://www.ncei.noaa.gov/data/global-summary-of-the-day/access/2024/43555099999.csv)
- Included files:rainfall/noaa_gsod_2024_43555099999.csv, rainfall/noaa_gsod_2025_43555099999.csv
- Main limitation:Screen event dates and broad daily context; unsuitable for peak short-duration intensity or within-city rainfall variation. PRCP units are inches; raw attributes retained. 2024 is not complete. Missing dates and sentinel values are not zero.
- Licence/access terms:Free download without login.

## R4 | NASA GPM IMERG Final V07

- Role:Rainfall / weather
- Access:Free registration / Earthdata or PPS download route; files not downloaded
- Detail:30 minutes; 0.1 degree grid (about 11 km).
- Coverage:Official directory: Jan 1998-present, with about 3.5 months latency for Final. Global ocean/land coverage includes Male latitude; actual Male values have not been extracted here.
- Source:[https://disc.gsfc.nasa.gov/datasets/GPM_3IMERGHH_07/summary](https://disc.gsfc.nasa.gov/datasets/GPM_3IMERGHH_07/summary)
- Included files:None; source/request lead only
- Main limitation:Best gridded subdaily fallback for regional event timing. Validate against gauges; not street-scale precipitation. Convert rate (mm/hour) to half-hour depth by multiplying by 0.5. Official directory and product documentation checked.
- Licence/access terms:Free NASA data; Earthdata or PPS registration for common download routes.

## R5 | ERA5 hourly time-series single levels

- Role:Rainfall / weather
- Access:CDSaccount/licenceacceptance/APIrequired;notdownloaded
- Detail:Hourly; 0.25 degree grid (about 28 km).
- Coverage:1940-present global atmosphere. A nearby grid point is returned for an off-grid request. Male island is not resolved.
- Source:[https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels-timeseries](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels-timeseries)
- Included files:None; source/request lead only
- Main limitation:Secondary reanalysis baseline; a large marine grid cell does not measure local convective rainfall peaks. Official dataset and download form checked; data not downloaded.
- Licence/access terms:CC-BY; free CDS registration and licence acceptance required.

## R6 | ERA5-Land hourly

- Role:Rainfall / weather
- Access:CDSaccount/APIrequired;notdownloaded
- Detail:Hourly; 0.1 degree delivery grid, about 9 km native.
- Coverage:1950-present land component. Valid Male grid-cell coverage has not been verified.
- Source:[https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land)
- Included files:None; source/request lead only
- Main limitation:Do not treat global extent as proof of valid values on a tiny island. ERA5 atmosphere avoids this land-mask issue but remains coarse. Official catalogue checked; no actual Male valid-pixel test.
- Licence/access terms:CC-BY

## R7 | CHIRPS v3 daily final

- Role:Rainfall / weather
- Access:OpenHTTPGeoTIFF/COG/NetCDF
- Detail:Daily values derived from pentads; 0.05 degree grid (about 5.6 km), not subdaily.
- Coverage:Land, 60 N-60 S. At 4.175 N, 73.510 E the 2025 Jan 3 final-sat COG contains a valid estimate of 108.274635314941 mm. One pixel/date is verified, not the complete historical record.
- Source:[https://www.chc.ucsb.edu/data/chirps3](https://www.chc.ucsb.edu/data/chirps3)
- Included files:rainfall/chirpsv3_sat_20250103_male_context.tif
- Main limitation:Useful for daily/climate context, not short-duration waterlogging intensity. Daily v3 inherits pentad totals and ERA5/IMERG timing; do not use agreement with those inputs as independent validation. Official v3 description and daily README checked. Actual COG sampled using GDAL; a 3-by-3-cell context GeoTIFF is saved. CHIRPS v2 ends after Dec 2026.
- Licence/access terms:Publicdomain

## T1 | JASL/UHSLC Male record1082, versionB

- Role:Optional tide/water-level covariate
- Access:Actual CSV downloaded and inspected
- Detail:Hourly;8,784 timestamps;8,659 valid,125 missing
- Coverage:2024-01-01 to2024-12-31 UTC; station4.19N,73.5267E
- Source:[https://uhslc.soest.hawaii.edu/erddap/tabledap/global_hourly_rqds.html](https://uhslc.soest.hawaii.edu/erddap/tabledap/global_hourly_rqds.html)
- Included files:tides/UHSLC_Male_Record1082_Hourly_2024.csv
- Main limitation:Water levels are mm relative station zero, not flood depth or automatically MSL. Reconcile vertical datums before combining with elevation. Includes a units row after header.
- Licence/access terms:Free use/redistribution per ERDDAP metadata; cite DOI10.7289/V5V40S7W.

## M7 | Dynamic World V1

- Role:Optional time-matched land cover
- Access:Catalogue only; Male samples not extracted
- Detail:10m class probabilities
- Coverage:2015 onward, cloud-filtered Sentinel2
- Source:[https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_DYNAMICWORLD_V1](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_DYNAMICWORLD_V1)
- Included files:None; source/request lead only
- Main limitation:Use pre-event images. flooded_vegetation class is not urban flood ground truth.
- Licence/access terms:CC BY4.0 plus required source attribution.
