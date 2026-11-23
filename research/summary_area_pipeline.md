# Research summary: area pipeline (MF-21, MF-22, MF-26, MF-50)

23 Nov 2026. Draws on the three agent reports (`rq1_rq2_land_fraction_blocks.md`, `rq3_rq4_presence_only_bias.md`, `rq5_rq6_attributes.md`) and the plan (`plan_area_pipeline.md`).

## How far to trust this

- **Mostly abstracts.** Publisher pages often returned 403. Of about 33 sources cited, only Ploton et al. 2020, Budic et al. 2016 and one ANN flood paper were read as full text (through fetch summaries), along with some documentation pages. Everything else is abstract or documentation only. Read the full text before quoting anything in the review beyond the abstract.
- **DOIs check out.** 14 DOIs resolved at doi.org, and 6 had their title, journal, volume and pages confirmed against Crossref (Budic, van Proosdij, Phillips 2009, Seleem, Li 2022, Ploton). One correction: Budic et al. is *Ecology and Evolution* 6: 202–211.
- **Not verified:** the Hawker et al. 2022 FABDEM accuracy figures and the ESA WorldCover accuracy figures were seen only in search results. Neither is quoted below.
- **Judgement, not sources:** where no source gives a number (land-fraction cutoff, fold count, minimum presences for this setting), the recommendation below is our judgement and is labelled as such.

## Recommendations

| Topic | Recommendation | Basis | Feeds |
|---|---|---|---|
| Land fraction (RQ1) | No flood study states a cutoff. Compute attributes over the land part of each cell only. Run 0.10, 0.25 and 0.50 as a sensitivity check, plus a land-fraction-weighted variant. Report the cells and positive cells kept at each. Dropped cells are "not assessed", never low susceptibility. Proposed default 0.25 (judgement), unless it drops a cell with a report. | Analogue only: Budic et al. 2016 down-weight partial-land cells and mask the sea | MF-26 (B3), group decision |
| Spatial blocks (RQ2) | Blocks of neighbouring cells, not the 4 wards (one ward holds most of the evidence). About 5 contiguous blocks (each about 600–800 m), each holding at least one positive cell, with every `location_group` kept in one block. Estimate an autocorrelation range only as a rough indication. | Roberts et al. 2017 (block CV preferred, abstract); Ploton et al. 2020 (blocks slightly larger than the autocorrelation range, full text); Valavi et al. 2019 (blockCV). The fold count is judgement | MF-26 (B3), MF-51, group decision |
| Model choice (RQ3) | The descriptive evidence map is the main result. A positive-only ranking is at most an exploratory secondary output. Use only a few covariates (2 to 4), a strongly regularised presence-background model or a transparent rank-sum. Avoid RF, PU bagging, one-class SVM and neural nets at this sample size. If fewer than about 10 independent presence cells remain after de-duplication, choose descriptive only (judgement). | van Proosdij et al. 2016 (real-data minimum of 14–25 presences); Wisz et al. 2008 (no algorithm consistently good under 30); Hernandez et al. 2006 (Maxent usable at 5–25 for narrow-range species); Li et al. 2022 (PU for urban flood) | MF-50 (B4), group decision |
| Metrics (RQ3) | Use recall@k against area share, partial ROC, and the continuous Boyce index (indicative only, show the P/E curve). Evaluate by spatial block or leave one location group out. Never use AUC against unknowns, accuracy, F1, or calibration or probability claims. | Hirzel et al. 2006; Peterson et al. 2008; Lobo et al. 2008; van Proosdij et al. 2016 | MF-50, MF-60 |
| Reporting bias (RQ4) | Keep pumping-only records as a separate presence set, and run everything with and without them. Count one presence per location group per event. An optional background restricted to "reportable" cells is a loose analogue of the target-group method. A bias covariate goes in the background only. Don't thin further, since one presence per 200 m cell already thins. | Phillips et al. 2009 (target-group background); Aiello-Lammens et al. 2015 and Boria et al. 2014 (thinning, mixed evidence); Agostini et al. 2024 (unreported cannot be told apart from non-events) | MF-21 (flags), MF-50 |
| Aggregation (RQ5a) | Use fractional-coverage zonal statistics: each pixel weighted by the share of it inside the cell's land. Report continuous layers as weighted mean, minimum and 10th percentile, and categorical layers as class area fractions. At 4°N, treating pixel areas within the island as equal is an acceptable shortcut, but say so. | exactextractr documentation | MF-22 (B2) |
| Building source (RQ5d) | Google Open Buildings at confidence ≥ 0.75, as footprint **area fraction**, not counts. It is the only source confirmed to list Maldives. OSM has 933 footprints, against 5,773 from Google, so OSM is likely incomplete. Microsoft and OSM go in a later sensitivity check. | Google Open Buildings site; Microsoft repo (South Asia IoU 63.1%) | MF-22 (B2) |
| FABDEM and WorldCover (RQ5b, c) | FABDEM is a relative rank only, never height above sea level or a flood depth. Independent island RMSE is 3–6 m in the Philippines (Santillan 2023), and no atoll validation was found. WorldCover built-up is near saturation on Malé, so it has little variance and is not imperviousness. | Santillan 2023; Gesch 2023 (abstract pages) | MF-22 column caveats |
| Attributes (RQ6) | **Compute now:** land fraction, building area fraction, OSM road length density, centroid distance to the coast, FABDEM weighted mean, minimum and 10th percentile (with caveat), WorldCover built-up share (with caveat). **Not meaningful or not available:** slope, TWI, flow accumulation, drainage, pump and soil data. WorldPop is exposure only and stays out of susceptibility. | Seleem et al. 2022 (abstract); the rest is judgement | MF-22 (B2) |

## What MF-21 records now, so either MF-50 option stays open

For each record: record ID, date as reported, evidence class (stated flooding, pumping only, designated, unverified), scope, `location_group`, cell ID or the reason it has none, assignment method, and whether the site is a routine pump site. Whole-road and ward mentions are listed per cell but never set a cell's status. No `observed_dry` value is created.

## Open decisions for the group

1. The land-fraction rule, from the MF-26 proposal.
2. The block layout and fold count, from the MF-26 proposal.
3. MF-50: descriptive only, or an exploratory positive-only ranking. Also whether the de-duplicated presence count clears the roughly-10 bar (our judgement).
4. Whether pumping-only records enter any model, or stay only in the sensitivity runs.
5. The building source, if the group prefers Microsoft or OSM after the sensitivity check.

## Candidates for MF-19 (literature review)

All are journal articles with checked DOIs. Read the full text before citing details.

1. Li, W., Liu, Y., Liu, Z., Huang, H., Huang, W., Gao, Z. (2022). A positive-unlabeled learning algorithm for urban flood susceptibility modeling. *Land* 11(11), 1971. doi:10.3390/land11111971
2. Seleem, O., Ayzel, G., de Souza, A. C. T., Bronstert, A., Heistermann, M. (2022). Towards urban flood susceptibility mapping using data-driven models in Berlin, Germany. *Geomatics, Natural Hazards and Risk* 13(1), 1640–1662. doi:10.1080/19475705.2022.2097131
3. Roberts, D. R., et al. (2017). Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. *Ecography* 40(8), 913–929. doi:10.1111/ecog.02881
4. Ploton, P., et al. (2020). Spatial validation reveals poor predictive performance of large-scale ecological mapping models. *Nature Communications* 11, 4540. doi:10.1038/s41467-020-18321-y
5. Valavi, R., Elith, J., Lahoz-Monfort, J. J., Guillera-Arroita, G. (2019). blockCV: an R package for generating spatially or environmentally separated folds for k-fold cross-validation of species distribution models. *Methods in Ecology and Evolution* 10(2), 225–232. doi:10.1111/2041-210X.13107
6. Meyer, H., Pebesma, E. (2021). Predicting into unknown space? Estimating the area of applicability of spatial prediction models. *Methods in Ecology and Evolution* 12(9), 1620–1633. doi:10.1111/2041-210X.13650
7. Phillips, S. J., et al. (2009). Sample selection bias and presence-only distribution models: implications for background and pseudo-absence data. *Ecological Applications* 19(1), 181–197. doi:10.1890/07-2153.1
8. van Proosdij, A. S. J., Sosef, M. S. M., Wieringa, J. J., Raes, N. (2016). Minimum required number of specimen records to develop accurate species distribution models. *Ecography* 39, 542–552. doi:10.1111/ecog.01509
9. Hirzel, A. H., Le Lay, G., Helfer, V., Randin, C., Guisan, A. (2006). Evaluating the ability of habitat suitability models to predict species presences. *Ecological Modelling* 199(2), 142–152.
10. Lobo, J. M., Jiménez-Valverde, A., Real, R. (2008). AUC: a misleading measure of the performance of predictive distribution models. *Global Ecology and Biogeography* 17(2), 145–151. doi:10.1111/j.1466-8238.2007.00358.x
11. Peterson, A. T., Papeş, M., Soberón, J. (2008). Rethinking receiver operating characteristic analysis applications in ecological niche modeling. *Ecological Modelling* 213(1), 63–72. doi:10.1016/j.ecolmodel.2007.11.008
12. Budic, L., Didenko, G., Dormann, C. F. (2016). Squares of different sizes: effect of geographical projection on model parameter estimates in species distribution modeling. *Ecology and Evolution* 6, 202–211. doi:10.1002/ece3.1838

Still to find and read (not opened in this pass): Hawker et al. 2022 *Environmental Research Letters* (FABDEM, doi:10.1088/1748-9326/ac4d4f); Meadows et al. 2024 *International Journal of Digital Earth*; Wisz et al. 2008 *Diversity and Distributions*; a peer-reviewed flood study that uses spatial cross-validation.
