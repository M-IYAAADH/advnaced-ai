# Male flood-data research

Checked14November2026. Four parallel source searches; actual downloaded data plus labelled access leads.

## Data found for your Male flood project

Four parallel research searches checked flood records, rainfall, elevation/drainage and mapping/exposure. Actual data files were downloaded and inspected, not just catalogued. Scope: Male island proper; primary task: rainfall-induced urban waterlogging. Checked14November2026.

### What is ready, and what still determines feasibility

You can start the GIS and data-quality work now. The main acquisition gaps are trustworthy flooded/dry observations, short-duration local rainfall, and detailed local ground/drainage data. The starter pack is not a validated flood-training dataset.

| Need | Result | Status |
| --- | --- | --- |
| Boundary | Official OneMap Male polygon and OSM clip boundary | Downloaded |
| Roads / buildings | 571 road features;3 separate building alternatives | Downloaded |
| Land cover / population | WorldCover10m2021;WorldPop100m2025 | Downloaded |
| Elevation | FABDEM30m original tile and Male clip | Downloaded; coarse/unvalidated |
| Weather | Airport2024/2025 meteorology and6/12/24h rain accumulations | Downloaded; not hourly rainfall |
| Tides | 2024 research-quality hourly nearby gauge | Downloaded;125missing values |
| Local flood labels | Public reports/event leads; no full observed street inventory verified | Request needed |
| Detailed drains / survey | Completed design-document lead; public data not located | Request needed |

### Recommended starting combination

Use the official boundary, OSM roads, a visually audited building alternative and WorldCover as spatial inputs. Use the NOAA/tide files to explore event matching, retaining their limitations. Compare FABDEM only as an exploratory elevation source until checked against survey. Prioritise Council/NDMA and MMS requests before making predictive claims.

Important correction to the earlier planning lead: the2023 Malé DEM/masterplan EOI was cancelled12August2024 [S13]. Separate stormwater detailed designs were completed byMay2024 [S14-S15]. That is a request lead, not evidence of an openly available high-resolution DEM.

## Real map layers, not a flood prediction

See Male_Data_Coverage.png in this pack.

| Layer | Verified content | Use with care |
| --- | --- | --- |
| OSM roads | 571 clipped road features | Centre-lines; no drain capacity |
| OSM buildings | 933 cleaned footprint features | Incomplete;2 building=no removed |
| Microsoft buildings | 4,677 candidate footprints | No assumed usable height |
| Google OpenBuildings | 5,773 candidates atconfidence>=.75 | Full audit file10,077; thresholdnotvalidatedprecision |
| WorldCover | 227x153 crop;24,188valid10m cells | Observation2021; mixedstreetpixels |
| WorldPop | 23x15 crop;233valid~100m cells | Modelled2025alpha estimates; broadexposure |

The three building sources have different coverage and segmentation. Keep them separate; the counts are not an estimate of the true number of Malé buildings. Compare a sample against dated imagery/local GIS before choosing a source [S2-S6,S6b].

Mapping layers use the OSM island clip; FABDEM uses the official OneMap clip. Both boundaries are supplied and need reconciliation. This distinction matters at coasts/reclaimed land. The airport/weather and tide-gauge coordinates are outside Malé island proper [S1,S7,S10].

## Rainfall and water levels: inspect the intervals

### Measured nearby weather: downloaded NOAA data [S7-S8]

Station435550/99999, VRMM, is Velana International Airport/Hulhulé at4.192N,73.529E.2024 contains10,784 meteorological rows;2025 contains7,198 and stops24August. Multiple reports and gaps mean row count is not a count of unique complete hours.

Checked precipitation groups in both years have6-,12- or24-hour accumulation periods, plus unknown-period/missing records. No1-hour rainfall group was verified. Preserve quality and condition flags; overlapping totals must not be added. The supplied readable accumulation tables keep those fields.

GSOD daily summaries contain355dates/354nonmissing precipitation values for2024, and236dates for2025. PRCP is in inches; convert units deliberately. Missing dates and sentinel values are not zero rainfall.

### Best local rainfall acquisition: MMS [S9]

The official request listing offers rainfall, hourly frequency and CSV, subject to availability. Request Malé-island gauges and nearby Hulhulé data, any available10/15-minute measurements, station coordinates/instrument history, original accumulation windows, QC/missing codes and timezone. No request has been sent. Follow MMS restrictions on redistribution.

### Optional tide / water-level covariate: downloaded [S10]

UHSLC record1082(versionB), station108: hourly2024 CSV has8,784timestamps,8,659valid values and125missing. Values are millimetres relative to stationzero, with a units row after the header. These are nearby coastal water levels, not street flood depths.

Convert timestamps consistently between UTC and Maldives UTC+5; keep original times. Reconcile stationzero with the survey/DEM datum before comparing heights. Tide alone does not represent wave run-up or prove that a rainwater event was coastal.

### Event-driven modelling consequence

Rainfall and tide at one station can help distinguish events over time; they do not explain which neighbouring street floods inside the same event by themselves. Spatial features and actual location-event observations remain necessary.

## Elevation and drainage: the critical local request

### FABDEM30m: real file, limited local accuracy [S11]

Downloaded the original N04E073_FABDEM_V1-2.tif from Bristol and supplied a Malé boundary-masked clip. Native1arcsecond grid, WGS84 horizontal andEGM2008 vertical. The48x70 bounding crop has2,169inside-island sample centres; all are non-NoData.

The clip ranges0-15.15m, with median5.04m and65zero-valued samples. These are source values, not surveyed ground heights. The distribution warrants checking for residual urban bias, coastline/reclamation mismatch and water-filled pixels. It cannot establish kerbs, drain inverts or street inundation depths. No interpolation was used.

FABDEM is licensedCCBY-NC-SA4.0; the original attribution/licence and derivative status are included. Copernicus GLO-30 is a surface model including buildings/vegetation and is another coarse comparator, not a substitute for accurate local ground survey [S12].

### Two different procurements: distinguish their outcomes

| Evidence | What it establishes | What it does not establish |
| --- | --- | --- |
| 2023 DEM/masterplan EOI; cancelled12Aug2024 [S13] | The specific expression-of-interest process was cancelled | That a public Malé DEM was delivered |
| WorldBank July2024MTR,p.2 [S14] | Malé stormwater designs/tenderdocs completedMay2024 | Open files, full-island survey coverage or current installed drains |
| WorldBank September2025ISR [S15] | Detailed-design consultancy final outputs delivered | That all proposed physical works were built |

### Ask for these completed-design inputs

Seek project/client permission for survey points/DEM if produced; ground/invert levels and datum; GIS/CAD existing versus proposed drains; inlets/outfalls; pump locations/capacities/operation; dated maintenance/condition; and hydraulic-model inputs/outputs. Confirm the current custodian through the relevant Council/engineering/project office.

No authoritative open detailed Malé drainage GIS was located. The OSM clip has zero mapped waterways, which does not mean zero drains. The national survey-control-point archive also had no points in the approximate Malé bounding box; it is not a Malé terrain dataset.

## Flood labels: public history is not ground truth

### Useful local records and their limits [S16-S18]

| Source | Verified public information | Next step |
| --- | --- | --- |
| NDMA Malé incident table | Dated location-text rainwater record; no complete footprint/dry coverage | Request deidentified event-location records |
| DALA downloads | Dynamic statistics page; advertised aggregate CSVs; direct API403here | Use normal public buttons or request aggregate export; still need local labels |
| Council VLR2025 | Major surface-water event summary and reference to Draft City Disaster Management Plan2025 | Request underlying event register and hazard/observation maps |

A three-row deidentified event-candidate CSV is included:1October2023,31December2023 and12January2024. These are source/date leads for checking, not an event census and not three sets of street observations. The MMS2024 report link currently redirects; retain the provenance and reconcile the12-13January event window.

### Minimum observation schema

Request event_id, island_code, stable location_id, observation timestamp/timezone, coordinates/street/grid, location precision, observed status(flooded/dry/unknown), flood mechanism, observation coverage, evidence and verification status. Add depth/duration only where measured and defined. Ask about recording changes and reporting bias.

Keep rainwater, coastal and compound events distinguishable. A sandbag/assistance request is not automatically measured flooding. A place with no incident report is unknown unless it was actually observed dry. Do not generate negative labels from absence of complaints.

### Avoid unsuitable global labels

The Global Flood Database is useful regional context but effective MODIS observations are250m; actual overlapping Malé event coverage was not established [S22]. JRC river-flood hazard maps model the wrong process and exclude small basins/islands, so they should not be used as observed Malé waterlogging labels [S23].

A good first research contribution can be a carefully verified local observation inventory. Prediction should follow that evidence, rather than treating an easily downloaded global map as ground truth.

## Gridded rainfall alternatives and other candidates

| Product | Access/detail | Suitability |
| --- | --- | --- |
| IMERG FinalV07 [S19] | Catalogue verified;30min/0.1deg(~11km); common downloads use freeEarthdata/PPS account | Best subdaily gridded candidate; actual Malé series not extracted; gauge validation needed |
| CHIRPSv3 [S20] | Open;0.05deg(~5.6km)daily; actual3Jan2025 point and3x3subset obtained | Daily climatology/context; not within-hour peaks |
| ERA5 hourly [S21] | Catalogue verified;0.25deg; freeCDSaccount/API; not downloaded | Coarse atmospheric reanalysis baseline |
| ERA5-Land | Catalogue verified;~9kmnative/0.1deg delivery | Actual Malé land-mask validity not tested; do not infer fromglobal extent |
| NASA POWER | 120-hour1-5Jan2025 point example downloaded | MERRA2 reanalysis, not a local rain gauge |
| Dynamic World [S24] | 10m/2015onward; catalogue only | Cloud-filtered, date-matched land cover; flooded_vegetation is not urban flood truth |

### CHIRPS version and interpretation matter

The actual CHIRPSv3 final-sat pixel at4.175N,73.510E on3January2025 is108.274635mm. That verifies one pixel/date, not the whole archive. The3x3context subset is included. Dailyv3 partitions pentad totals usingIMERG orERA5 timing; it is not an independent daily local gauge series [S20].

The provider saysCHIRPSv2 production will end afterDecember2026; yourMay2027 project should record its chosen version and transition deliberately. Resampling0.05-degree rainfall to10m creates a denser grid, not additional rainfall information.

### Keep observational and modelled sources distinct

NOAA/MMS gauges are point observations with their own measurement windows. IMERG is a gridded satellite/gauge product. ERA5/POWER are reanalysis estimates. Each has different errors and availability latency. Retrospective final/reanalysis data are not automatically available at a real-time forecast issue time.

## How to use this pack and close the gaps

### Start the GIS work now

Open the GeoJSON/GeoTIFF files inQGIS. Check both island boundaries, then inspect roads and one building source against dated local mapping. Preserve original grids/values. Use projected coordinates for metre-based distances/areas and reconcile raster alignment before extracting features. Existing clips use different source boundaries; do not join them blindly.

### Prioritise three data requests

- Council/NDMA: deidentified observed flooded/dry/unknown location-event records and survey coverage; start with the disaster-plan sources behind the CouncilVLR.
- MMS: local hourly and any available subhourly rainfall for matching events, original accumulation windows, station metadata and quality flags.
- Project/engineering custodian: completed stormwater-design inputs, accurate survey/elevation and existing/proposed drain/pump GIS or CAD.

### Then build a defensible pilot

Construct separate location and event tables joined bystableIDs. Keep temporal inputs available only before the intended prediction time. Choose a spatial/event holdout that tests your actual claim; group repeated locations when testing geographic generalisation and hold out future events when testing temporal transfer. Report independent event/location counts, not only pixel counts.

Do not claim depth prediction without measured depth labels and adequate elevation. If access fails, narrow Malé to an observed neighbourhood or deliver a transparent exploratory mapping/data-gap study. Any synthetic or expert-weighted susceptibility output must be labelled accordingly.

### What the files contain

The ZIP contains original/derived data, source metadata and QA, a readable/machine-readable catalogue, a data-request specification and an integrity manifest. Building sources remain separate. Raster grids are native; no model has been trained and no agency has been contacted.

### Licences are dataset-specific

OSM isODbL;Microsoft usesCDLA Permissive2.0;Google offersCCBY4.0/ODbL;WorldCover andWorldPop useCCBY4.0;FABDEM isCCBY-NC-SA4.0 with required original attribution. OneMap reuse terms need confirmation. Follow provider terms in the source documents; the ZIP has no single blanket data licence.

## Source links | 1

Clickable primary-source links. Exact data-download URLs, request parameters, source dates and dataset-specific limitations are retained in the catalogue and provenanceJSON files. These are data/documentation sources, not substitutes for your15journal articles.

[S1 | OneMap official portal/API documentation](https://readme.onemap.mv/)

[S2 | OpenStreetMap Maldives viaGeofabrik](https://download.geofabrik.de/asia/maldives.html)

[S3 | OpenStreetMap attribution/licence](https://www.openstreetmap.org/copyright)

[S4 | Microsoft official building footprints](https://github.com/microsoft/GlobalMLBuildingFootprints)

[S5 | Google OpenBuildings official source](https://sites.research.google/gr/open-buildings/)

[S6 | ESA WorldCover2021v200 catalogue](https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v200)

[S6b | WorldPop MDV2025 API metadata](https://api.worldpop.org/v3/countries/MDV/files?year=2025)

[S7 | NOAA GlobalHourly/ISD product documentation](https://www.ncei.noaa.gov/products/land-based-station/integrated-surface-database)

[S8 | Actual NOAA2024 airport meteorological CSV](https://noaa-global-hourly-pds.s3.amazonaws.com/2024/43555099999.csv)

[S9 | MMS historical-weather request listing](https://www.meteorology.gov.mv/climate-data)

[S10 | UHSLC research-quality hourly waterlevel access](https://uhslc.soest.hawaii.edu/erddap/tabledap/global_hourly_rqds.html)

[S11 | FABDEM official archive/readme](https://data.bris.ac.uk/datasets/s5hqmjcdj8yo2ibzi9b4ew3sn/readme.txt)

[S12 | Copernicus DEM product specifications](https://dataspace.copernicus.eu/explore-data/data-collections/copernicus-contributing-missions/collections-description/COP-DEM)

## Source links | 2

Clickable primary-source links. Exact data-download URLs, request parameters, source dates and dataset-specific limitations are retained in the catalogue and provenanceJSON files. These are data/documentation sources, not substitutes for your15journal articles.

[S13 | Official cancellation12August2024](https://www.gazette.gov.mv/iulaan/303525)

[S14 | WorldBank July2024MTR: completedMalédesigns](https://documents1.worldbank.org/curated/en/099110624015517827/pdf/P163957-b07c3d4e-8d19-42d6-922e-85953c240e40.pdf)

[S15 | WorldBank September2025ISR: designoutputs delivered](https://documents1.worldbank.org/curated/en/099091525210068111/pdf/P163957-77b14dbd-a852-42ea-a7fe-e284010060fe.pdf)

[S16 | NDMA Malé incident table](https://ndma.gov.mv/en/statistics/atoll/21/incident)

[S17 | DALA statistics/download page](https://stats.ndma.gov.mv/download-statistics)

[S18 | Malé CityCouncil VLR2025](https://cdn.malecity.gov.mv/website/documents/6zqnEssfa8YfgaNZkf_I0-VLR_Male_Small%20file%20size.pdf)

[S19 | NASA IMERG FinalV07 official product](https://disc.gsfc.nasa.gov/datasets/GPM_3IMERGHH_07/summary)

[S20 | CHIRPSv3 official data and daily derivation](https://www.chc.ucsb.edu/data/chirps3)

[S21 | ERA5 hourly point time-series catalogue](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels-timeseries)

[S22 | Global Flood Database effective observation scale](https://developers.google.com/earth-engine/datasets/catalog/GLOBAL_FLOOD_DB_MODIS_EVENTS_V1)

[S23 | JRC river flood hazard coverage exclusions](https://developers.google.com/earth-engine/datasets/catalog/JRC_CEMS_GLOFAS_FloodHazard_v2_1)

[S24 | Dynamic World official catalogue](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_DYNAMICWORLD_V1)
