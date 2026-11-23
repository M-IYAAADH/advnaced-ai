# RQ5 and RQ6: raster-to-cell aggregation, data caveats, conditioning factors

Agent R3, 23 Nov 2026. Feeds MF-22 and MF-19. Budget overrun note: about 9 searches and about 19 fetch attempts, of which 9 returned content; the rest were blocked (403, bot check, connection refused). Several key papers (Hawker 2022 full text, ESA WorldCover validation report, Meadows 2024, Seoul/Guangzhou/Changsha factor studies) could NOT be opened, so they are not in the evidence table as opened sources. See "Seen only in search results" below.

## 1. Search log

| # | Query | Useful hits |
|---|---|---|
| 1 | Hawker 2022 30 m global map of elevation with forests and buildings removed FABDEM ERL | 2 (IOP page blocked; bris/EGU summaries in search result only) |
| 2 | FABDEM vertical accuracy validation urban OR island OR coastal | 3 (Santillan, Gesch opened; Meadows 2024 blocked) |
| 3 | Google Open Buildings Microsoft building footprints completeness accuracy comparison OSM | 2 (Okyere opened, abstract only) |
| 4 | urban pluvial flood susceptibility conditioning factors ML impervious building density | 1 opened later (Seleem); others snippets only |
| 5 | ESA WorldCover 2021 v200 validation overall accuracy built-up | 0 opened (PVR blocked by bot check; overall accuracy only in search text) |
| 6 | Sirko 2021 continental-scale building detection | 1 (arXiv abstract) |
| 7 | exactextractr coverage fraction zonal statistics | 1 (CRAN readme opened) |
| 8 | flat low-relief urban pluvial flood susceptibility DEM slope TWI | 1 (Seleem confirmed via agris) |

Fetches that worked: Santillan (ISPRS page), Gesch (USGS page), Okyere (arXiv abs), Sirko (arXiv abs), exactextractr (CRAN readme), Google Open Buildings site, Microsoft GlobalMLBuildingFootprints repo, Seleem (agris record).

## 2. Evidence table

| Citation | DOI / URL | What it did | Finding relevant to RQ | Confidence |
|---|---|---|---|---|
| Baston D. exactextractr (R package), CRAN readme | https://cran.r-project.org/web/packages/exactextractr/readme/README.html | Zonal statistics that weight raster cells by the fraction covered by each polygon | "Unlike most zonal statistics implementations, it handles grid cells that are partially covered by a polygon." "the error introduced by incorrectly handling partial coverage is less than 1% for 88% of municipalities and reaches a maximum of 9%." Says assuming equal cell areas "is not correct for rasters in geographic coordinates"; recommends a weighting raster of cell areas. | Official documentation, opened. The error figures are the package's own example (municipalities, not 200 m cells); at 40 pixels per cell edge effects will be larger than in that example. Author name for the package taken from knowledge, not from the page; check before citing. |
| Santillan J.R. (2023) Vertical accuracy evaluation of the Forest and Buildings Removed Copernicus DEM (FABDEM) over the Philippines. Int. Arch. Photogramm. Remote Sens. Spatial Inf. Sci. XLVIII-4/W6-2022, 311-318 | https://isprs-archives.copernicus.org/articles/XLVIII-4-W6-2022/311/2023/ (page notes a corrigendum; check it) | 17,013 geodetic control points, country and island level | "some islands having RMSEs as low as 3.03 meters and as high as 5.80 m"; country RMSE averages 4.74 m; mean error -1.44 m (underestimates); most accurate below 100 m elevation and slopes below 2 degrees; "care must be taken when applying the FABDEM in an archipelagic country". | Abstract page only. Independent. Philippine islands are larger and hillier than Malé; it does not address built-up areas or atolls. Corrigendum not checked. |
| Gesch D.B. (2023) Assessing global elevation models for mapping the low elevation coastal zone. Conference paper, USGS | https://www.usgs.gov/publications/assessing-global-elevation-models-mapping-low-elevation-coastal-zone ; DOI listed there: 10.5281/zenodo.8011577 | Compared 30 m and 90 m global DEMs against US geodetic control points | Page (paraphrased): FABDEM performs best for high-confidence LECZ mapping with minimal bias and lowest error; global DEMs "are not accurate enough to show fine-scale flooding (under 1 meter) with high confidence" (paraphrase, not a verbatim quote). | Abstract page only; US coast, not atolls. Conference paper, not a journal. |
| Hawker L. et al. (2022) A 30 m global map of elevation with forests and buildings removed. Environ. Res. Lett. 17(2) 024016 | DOI 10.1088/1748-9326/ac4d4f (journal page returned 403; DOI not resolved by me) | Random-forest removal of tree and building heights from Copernicus GLO-30 | From a search-engine summary only (not read at source): mean absolute error in built-up areas fell from 1.61 m to 1.12 m. | NOT opened. Treat numbers as unverified until the paper is read. Developer-reported. |
| Okyere F., Lu M., Brunn A. (2025) Evaluating the quality of open building datasets for mapping urban inequality: a comparative analysis across 5 cities. arXiv 2508.12872 | https://arxiv.org/abs/2508.12872v1 | Google and Microsoft footprints vs OSM in Accra, Nairobi, Caracas, Berlin, Houston (IoU, positional accuracy, completeness) | "Houston and Berlin demonstrating high alignment and completeness"; "cities like Accra and Caracas may be under-represented" (dense or informal areas). No numbers in the abstract. Year of publication taken as 2025 from the arXiv id; not confirmed on the page. | Abstract only; preprint; no South Asian or island city. |
| Sirko W. et al. (2021) Continental-scale building detection from high resolution satellite imagery. arXiv 2107.12283 | https://arxiv.org/abs/2107.12283v2 | U-Net pipeline on 50 cm imagery, 100k images, 1.75M labelled buildings, 516M footprints (Africa) | Abstract reports mAP gains only (mixup +0.12, self-training +0.06) and says the pipeline "obtains good results even on a wide variety of challenging rural and urban contexts". No precision/recall figures on the page. | Abstract only. Describes the Africa model, not the later global/South Asia release that includes Maldives. |
| Google Research. Open Buildings dataset website | https://sites.research.google/gr/open-buildings/ | Dataset documentation | Maldives (MDV) is in the country list; released confidence is 0.65 to 1.0. Difficult cases named: "settlements with many contiguous buildings that lack clear boundaries", areas of small buildings, high-rise footprints shifting with view angle. Precision at 0.65/0.70/0.75 is not stated in the text. | Official page, opened. Quality for Malé specifically unknown. |
| Microsoft. GlobalMLBuildingFootprints repository | https://github.com/microsoft/GlobalMLBuildingFootprints | Dataset documentation | South Asia: precision 94.8%, recall 76.7%, IoU 63.1% (lowest of regions listed). "It is not perfect, particularly in dense urban areas but it provides good recall in rural areas." Quality "at least as good as hand digitized buildings in OpenStreetMap" (developer claim). Missing areas appear as "squares of missing data". Maldives not mentioned in text; coverage unknown. | Official page, opened. Developer-reported. |
| Seleem O., Ayzel G., de Souza A.C.T., Bronstert A., Heistermann M. (2022) Towards urban flood susceptibility mapping using data-driven models in Berlin, Germany. Geomatics, Natural Hazards and Risk 13(1) 1640-1662 | DOI 10.1080/19475705.2022.2097131 | 4,333 flooded locations, 11 predictors, CNN/ANN/RF/SVM at 30, 10, 5, 2 m | "Aspect was the most influential factor for the image-based models, and altitude was the most influential for the point-based models." RF best at every resolution, 2 m strongest; transfer outside training area was only moderate. | Record/abstract only (agris page). Berlin has a real inventory with negatives; the 11 factors are not itemised in what I read. |

### Seen only in search results (not opened, do not cite until read)
- ESA WorldCover 2021 v200: overall accuracy 76.7 percent (search text); Product Validation Report V2.0 at https://pure.iiasa.ac.at/18981/1/WorldCover_PVR_V2.0.pdf was blocked. Built-up user's/producer's accuracy: no source found by me.
- Meadows et al. 2024, Int. J. Digital Earth, FABDEM ranked first vs Copernicus, NASADEM, AW3D30, SRTM in flood-prone sites (https://www.tandfonline.com/doi/full/10.1080/17538947.2024.2308734, blocked).
- Guangzhou (ISPRS IJGI), Changsha (Sustainability 2025), Ordos, Seoul (IJGI 2025) susceptibility studies reporting impervious surface density as the dominant factor, with conflicting thresholds (0.2, 0.35, 0.80). Snippets only; the factor lists and resolutions are unverified.
- Berlin FSM vs TWI (Water 2021): snippet says fill-spill-merge outperformed TWI. Unverified.
- Chamberlain et al. 2024 (pairwise Jaccard 0.40 to 0.60 among Google/Microsoft/OSM/Ecopia in Africa); Minghini et al. ISPRS 2024 (OSM completeness rises with urbanisation); Fonte et al. ISPRS 2026 (hybrid OSM + Microsoft). Snippets only.

## 3. Recommendations

### RQ5a Aggregation method
Use fractional-coverage (exact) zonal statistics, not centroid sampling. Documented support: exactextractr treats partially covered pixels by coverage fraction (readme above). Concrete plan:
1. Reproject the grid to EPSG:4326 (or the raster to EPSG:32643 with bilinear/nearest resampling, but prefer not to resample the DEM) and extract in the raster's native grid; keep rasters in degrees.
2. Weight each pixel by coverage fraction times true pixel area (readme recommends an area-weighting raster for lat/long data; at 4 degrees N the cos(lat) variation across 1.9 km is negligible, so equal areas within the island are an acceptable shortcut, but state it).
3. For continuous layers (FABDEM) report weighted mean, min, max, weighted std. For categorical layers (WorldCover) report the area fraction per class, not a majority class.
4. For cells under a quarter land (19 of 75), compute statistics over land pixels only (mask by the OneMap polygon) and also output land fraction; decide the inclusion rule in MF-22.
5. Python equivalent: the `exactextract` library (same author) or rasterstats with `all_touched=False` plus manual weights. I did not open documentation for these; check before use.
Limit: a 200 m cell holds about 40 FABDEM pixels, but edge cells hold far fewer land pixels, so their statistics are noisy.

### RQ5b FABDEM
Evidence on small islands/atolls: none found. Independent studies show RMSE of 3 to 6 m on Philippine islands (Santillan) and that global DEMs cannot resolve sub-metre flooding (Gesch). A within-island median of about 5.04 m and max of about 15.15 m, when Malé is known to be only about 1 to 2 m above sea level (from background knowledge, not from a source I opened), strongly indicates residual building/vegetation bias or vertical datum offset. Treat absolute FABDEM elevation as unreliable here; only relative within-island ordering might carry weak information, and even that is unproven.

### RQ5c WorldCover built-up
No built-up class accuracy was obtained. Overall global accuracy 76.7 percent is search-result text only. On a 1.9 km² island that is almost fully built, the built-up fraction will be near 1 everywhere and will have almost no variance. Do not use as a discriminating predictor.

### RQ5d Building source
Recommendation: **Google Open Buildings (confidence >= 0.75)** as the single building source, with caveats, because (i) it is confirmed to cover Maldives (MDV listed), unlike Microsoft where I could not confirm coverage; (ii) OSM has only 933 cleaned footprints against 5,773 Google and 4,677 Microsoft, so OSM is likely very incomplete; (iii) Microsoft's South Asia IoU is 63.1 percent and both vendors state weakness in dense urban areas. No source found comparing the three for Malé or any dense small-island city, so the choice is by coverage and count, not demonstrated accuracy. Mitigation: use building footprint area fraction per cell (robust to a few merged/missed buildings) rather than building counts, and run a sensitivity check with Microsoft and OSM in MF-22. Do a manual spot check of 3 to 5 cells against imagery.

### RQ6 Conditioning factors
Evidence I could verify is thin: Seleem 2022 (Berlin) used 11 factors with a real inventory and found altitude/aspect most influential, at 2 to 30 m resolution. Snippet-level evidence (unverified) points to impervious surface density, vegetation index, road density, elevation, and drainage variables (sewer density, distance to storm drain) as common. No source was found on conditioning factors specifically at 100 to 250 m or on flat atolls, so the lists below are judgement.

**Compute now**
- Cell land fraction and majority ward.
- Building footprint area fraction (Google >= 0.75).
- Road length density and road area proxy from OSM (571 features; note OSM completeness unknown).
- Distance from cell centre or land to coastline (OneMap polygon).
- WorldPop 2025 population per cell (exposure, not a hazard driver; keep out of the susceptibility model).

**Compute with caveat**
- FABDEM weighted mean, min, max and within-cell range: bias (median about 5 m on a low island), datum unknown, 30 m DSM-like artefacts; use only as relative rank, never as height above sea level, and do not interpret as flood depth.
- Relative elevation (cell mean minus island mean) or local low-point indicator: same caveat; vertical RMSE of global DEMs (3 to 6 m in Philippines) exceeds the plausible within-island relief.
- WorldCover class fractions: built-up fraction near saturation; vegetation or bare fractions may be informative, but 10 m classes mix roofs and trees.
- Building footprint count: depends on source and merging; prefer area fraction.

**Not meaningful or not available here**
- Slope, aspect, curvature, TWI, flow accumulation from FABDEM: a 30 m DSM-like surface on a flat, fully built 1.9 km² island has relief below the DEM error; derivatives would be noise. (Judgement; the Berlin study used 2 m or better LiDAR-type data and still found aspect/altitude dominant, which does not transfer.)
- Distance to drainage/sewer inlets, drain density, pump proximity: no drainage or pump data.
- Soil type, infiltration, geology: no data; Malé is nearly fully sealed so infiltration variation is minimal (background knowledge).
- Measured imperviousness: WorldCover built-up is not hydraulic imperviousness.
- Distance to river/stream: none exist on the island.
- Rainfall as a cell attribute: one station on Hulhulé, no spatial variation at 200 m.
- Any label-derived "importance" ranking: positive-only evidence cannot support supervised factor weighting; use attributes for description or a simple expert-weighted index, flagged as such.

### Caveats to print next to attribute columns
- FABDEM columns: "FABDEM V1-2, about 30 m, bare-earth estimate derived from a surface model. Island median about 5 m suggests residual building/vegetation bias. Vertical error of global DEMs is of the order of metres; values are relative and unvalidated for Malé."
- WorldCover built-up: "ESA WorldCover 2021, 10 m land cover; built-up is not measured imperviousness. Class accuracy for Malé unknown; near-saturated on this island."
- Buildings: "Google Open Buildings, confidence >= 0.75; model detections, not a survey. Dense-area omissions and merged buildings likely; no height or household information."

## 4. Candidates for MF-19 (only items I opened)
1. Seleem, O., Ayzel, G., de Souza, A. C. T., Bronstert, A., Heistermann, M. (2022). Towards urban flood susceptibility mapping using data-driven models in Berlin, Germany. Geomatics, Natural Hazards and Risk, 13(1), 1640-1662. doi:10.1080/19475705.2022.2097131. (Abstract read only; verify full text.)
2. Santillan, J. R. (2023). Vertical accuracy evaluation of the Forest and Buildings Removed Copernicus DEM (FABDEM) over the Philippines. Int. Arch. Photogramm. Remote Sens. Spatial Inf. Sci., XLVIII-4/W6-2022, 311-318. (Conference-series archive, not a journal; check the corrigendum.)
3. Sirko, W., et al. (2021). Continental-scale building detection from high resolution satellite imagery. arXiv:2107.12283. (Preprint.) Full author list not read.
4. Okyere, F., Lu, M., Brunn, A. Evaluating the quality of open building datasets for mapping urban inequality: a comparative analysis across 5 cities. arXiv:2508.12872. (Preprint.)

Journal articles that should be found and read in full before use (not opened here): Hawker et al. 2022 ERL (doi 10.1088/1748-9326/ac4d4f); Meadows et al. 2024 IJDE (doi 10.1080/17538947.2024.2308734); the Guangzhou, Changsha, Ordos and Seoul susceptibility studies listed above.
