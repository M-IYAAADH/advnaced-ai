# MF-50 decision record: descriptive only, or a positive-only ranking?

**DRAFT FOR THE GROUP TO DECIDE: not a decision.**

All counts come from `derived/grid_evidence.csv`, `derived/grid_blocks.csv` and `reports/mf26_blocks_proposal.md`. Method sources are abstract-only unless stated (see section 7).

## 1. Question and why now
Should the project stay "descriptive only" (an evidence map of reported flooding in the 75-cell, 200 m grid), or also add "a positive-only ranking with spatial folds"? MF-26 (blocks) and MF-22 (attributes) depend on the answer. The fixed facts: the evidence is positive-only, there are no observed-dry cells, unknown is never dry, and any model output is a ranking, never a flooded/dry classifier or a probability.

## 2. Evidence in hand
Cells by status (75 cells): unknown 57, reported_flooding 12, pumping_only 5, designated 1.

| Version | Positive cells | Independent location groups | Note |
|---|---|---|---|
| (a) stated flooding | 12 | 7 (the other 6 cells have no group) | 2 of 12 are routine pump sites (IGMH, West Park/STO) |
| (b) stated + pumping | 17 | 12 | adds 5 pumping-only cells, 5 more groups |
| (c) stated without construction-confounded cells | 6 | 7 (6 cells; one cell holds two groups) | removes the 6 cells resting only on RF071 |

- RF071 (30 Jul 2026) is one record and one date. It is attributed to pumps not yet commissioned on a rebuilt road (issue E5). So the 6 confounded cells are one event, not 6.
- With a 0.25 land-fraction cutoff, MF-26 gives 10 / 15 / 5 positives for (a) / (b) / (c).
- Positives per proposed k = 6 block (a / b / c): A 2/2/0, B 1/1/1, C 5/6/1, D 2/3/2, E 0/2/0, F 2/3/2. Block E has no stated positive. Under (c) only 4 blocks hold any positive, and none holds more than 2.

Missing: observed-dry or complete-coverage records, Council/NDMA/MNDF logs, drainage and pump locations, and the agency responses (MF-45, not yet received). Wards are OSM lines, not checked against a Council map.

## 3. Option A: descriptive only
- **Produces:** the evidence map by cell and status, plus a reported-versus-unknown comparison of covariates (MF-30). Everything is shown with and without pumping-only records and with and without the 6 confounded cells.
- **For:** it claims only what the data show. It needs no absences. It is not hurt by the small count.
- **Against:** it ranks no unreported cell. It cannot say which unknown cells look like the reported ones.
- **Risks:** readers may still read "reported" as "most flood-prone". The map must say that unknown is not dry, that main roads and landmarks are over-reported, and that pump sites reflect where pumps stand.

## 4. Option B: positive-only ranking with spatial folds
**Method family (least fragile).** Two to four covariates, then either a strongly regularised presence-background model (linear/hinge only) or a transparent rank-sum of physically justified covariates. Avoid random forest, PU bagging, one-class SVM and neural nets at this size. Candidate covariates from `derived/grid_attributes.csv`: FABDEM mean, minimum and 10th percentile; distance to coast; building area fraction; road density; WorldCover built-up share. Not available: slope, TWI, drainage, pumps, soil. WorldPop stays out (exposure only).

**Minimum presences (abstract only).** van Proosdij et al. 2016: about 14 to 25 presences in real-data cases. Wisz et al. 2008: no algorithm consistently good under 30 records. Hernandez et al. 2006: Maxent usable at 5 to 25 for narrow-range species. These are ecology studies. None is a flood study.

**Bias handling.**
- Pumping-only records form a separate set. Run every comparison with and without them.
- Count one presence per location group per event.
- Optional background restricted to cells that could have been reported (landmark, arterial road or pump station). This is a loose analogue of Phillips 2009. Drop it if few cells qualify.
- A bias covariate goes in the background only, not in the score.
- No further thinning: one presence per 200 m cell already thins.

**Evaluation.** Recall@k against the share of area selected. Partial ROC. Continuous Boyce index, indicative only, with the P/E curve shown. Spatial folds from MF-26 (k = 6, each location group in one block), or leave one location group out. Not allowed: AUC against unknowns, accuracy, F1, calibration or probabilities.

**Risks at this sample size.**
- Folds with zero or one positive: under (c), 2 of 6 blocks have none and 2 have one.
- Block E has no stated positive under any version; MF-26 asks whether to merge it.
- FABDEM is a relative rank only. Its zero-share is high near the coast: median 0, mean 0.069 over 71 cells with data. Treat the DEM as unreliable at the coast.
- WorldCover built-up share is near saturation, so it has little variance and is not imperviousness (cells range 0 to 1, median 0.53).
- Moran's I of the (a) indicator is 0.200 (p = 0.003). Positives cluster, which may be clustered reporting and pump placement, not only flooding.
- Fold-wise metrics will be very noisy (research estimate: folds of 2 to 4 positives at best).

## 5. Recommendation (DRAFT, for the group to accept or change)
The research's rule: if fewer than about 10 independent presence cells remain after de-duplication and after setting aside confounded cells, prefer descriptive only. This is the research agent's judgement, not a published rule. Applied to the counts:
- (a) 12 cells, but 6 come from one record and one event. It clears 10 only if the confounded cells count.
- (b) 17 cells, or 11 without the confounded cells, but 5 of those are pumping-only. These show pump deployment, not water.
- (c) 6 cells. It fails the bar.

Draft: choose **descriptive only** as the main result (Option A). Keep any ranking as an exploratory appendix at most, labelled as such, with the sensitivity runs above. Revisit when the agency responses (MF-45) arrive.

## 6. Decisions for the group, and what would change the answer
1. Descriptive only, or descriptive plus an exploratory appendix ranking?
2. Do the 6 confounded cells count as positives, or only in version (a)?
3. Do pumping-only cells enter any ranking, or only the sensitivity runs?
4. Block layout (k = 6 or k = 5) and block E (MF-26 items).
5. **Timing:** MF-50's acceptance needs the group to agree using verified evidence and agency responses (MF-45, not yet received). Do not close this before they arrive, or record it as open and revisitable.

New data that would change the answer: observed-dry or complete-coverage records from Council, NDMA or MNDF (would allow a true flooded/dry design); more independent events at distinct locations; drainage and pump locations (would add covariates and let pump bias be handled directly). Whether any agency holds these is unknown.

## 7. Sources (as given in the research files)
Files: `research/summary_area_pipeline.md`; `research/rq3_rq4_presence_only_bias.md` (3.1 to 3.3); `reports/mf26_blocks_proposal.md`; `data_issues.md` (G1, G2, G3, B4, E5).
Articles named there (abstract only except Ploton and Budic, which were read as full text via fetch summaries; read full text before quoting):
- van Proosdij et al. 2016, Ecography 39, 542-552.
- Wisz et al. 2008, Diversity and Distributions (not yet opened).
- Hernandez et al. 2006 (cited in the RQ3 file).
- Phillips et al. 2009, Ecological Applications 19(1), 181-197.
- Hirzel et al. 2006, Ecological Modelling 199(2), 142-152.
- Peterson et al. 2008, Ecological Modelling 213(1), 63-72.
- Lobo et al. 2008, Global Ecology and Biogeography 17(2), 145-151.
- Roberts et al. 2017, Ecography 40(8), 913-929.
- Ploton et al. 2020, Nature Communications 11, 4540.
- Valavi et al. 2019, Methods in Ecology and Evolution 10(2), 225-232.
- Li et al. 2022, Land 11(11), 1971 (PU learning, urban flood).
- Agostini et al. 2024; Aiello-Lammens et al. 2015; Boria et al. 2014 (as cited in the summary).
