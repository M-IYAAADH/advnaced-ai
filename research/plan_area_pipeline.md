# Research plan: area pipeline (MF-21, MF-22, MF-26, MF-50)

Written 23 Nov 2026 by the orchestrator (Claude) before any web search. Status: **awaiting the student's approval** ("go").

Fixed context (not reopened): the question is which areas of Malé island proper flood after rain. Results are reported by the 4 OSM wards and analysed on the 75-cell 200 m grid (EPSG:32643). Evidence is positive-only: about 11 cells hold a landmark report and none is observed dry. Pumping-only records are biased toward pump sites (B4). No report means unknown. No thresholds are stated.

## 1. Research questions

| RQ | Informs | Question | Decision it feeds |
|---|---|---|---|
| RQ1 | MF-26 | What minimum land fraction, or which coastal-cell rules (drop, merge with a neighbour, clip, weight), do grid-based urban or coastal flood-susceptibility studies use? | Land-fraction rule (sensitivity check at 0.1, 0.25 and 0.5) |
| RQ2 | MF-26 | How should spatial blocks be chosen for spatial cross-validation (block size against spatial autocorrelation range, number of folds, buffered leave-one-out) when positives are very few? Roberts et al. (2017); Valavi et al. (2019) blockCV; Ploton et al. (2020); Meyer and Pebesma. | Block layout: wards, or groups of neighbouring cells |
| RQ3 | MF-50 | Which positive-unlabelled (PU) or presence-background methods (MaxEnt, PU bagging, one-class SVM, presence-only RF) are used for flood susceptibility? What minimum number of presences do they need? How is a ranking evaluated (continuous Boyce index, recall@k, partial ROC, and why AUC against unknowns misleads)? | Option set and metrics in the MF-50 draft |
| RQ4 | MF-50, MF-21 | How do studies correct for reporting or sampling bias in presence-only data (target-group background, bias grids per Phillips et al. 2009, spatial thinning, bias covariates)? How would that apply to pump-site and landmark bias? | Bias handling in MF-50; flags and grouping kept by MF-21 |
| RQ5 | MF-22 | Method guidance for area-weighted aggregation of rasters to polygons. What is known about FABDEM accuracy in urban areas and on small islands, and about ESA WorldCover built-up accuracy? Which building-footprint source (OSM, Microsoft, Google Open Buildings) fits dense small-island cities? | Aggregation method; caveats per column; the one building source |
| RQ6 | MF-22 | Which conditioning factors do urban pluvial-flood susceptibility studies use at about 100 to 250 m resolution, and which are feasible with our data? | Attribute list for `derived/grid_attributes.csv` |

## 2. Sources and search strategy

**Sources:** Google Scholar-style queries, publisher pages (Elsevier, Springer, Wiley, MDPI, Copernicus/EGU, IOP), DOI resolution via doi.org, and official dataset documentation: FABDEM (Hawker et al. 2022, ERL; University of Bristol data page), ESA WorldCover 2021 product validation report, WorldPop methods, Microsoft GlobalMLBuildingFootprints repository, Google Open Buildings technical report.

**Query strings (starting set; agents may refine and must log what they ran):**

- RQ1: `"flood susceptibility" grid cell "land fraction" coastal`; `"urban flood susceptibility" grid "coastal cells" excluded`; `"fishnet" flood susceptibility urban cell size`; `"partial cells" OR "edge cells" zonal statistics flood mapping`
- RQ2: `Roberts 2017 "cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure"`; `blockCV Valavi 2019 spatial blocking`; `"spatial cross-validation" "block size" autocorrelation range "few presences"`; `"spatial cross-validation" flood susceptibility`; `Ploton 2020 spatial validation`
- RQ3: `"positive-unlabeled" flood susceptibility`; `"presence-only" OR MaxEnt "flood susceptibility" urban`; `"one-class" flood susceptibility`; `"continuous Boyce index" Hirzel 2006`; `"partial ROC" Peterson 2008`; `"minimum number of presences" species distribution model van Proosdij 2016`; `"AUC" presence-background misleading Lobo 2008`
- RQ4: `Phillips 2009 "sample selection bias" target-group background`; `"bias file" OR "bias grid" MaxEnt sampling effort`; `"spatial thinning" spThin Aiello-Lammens 2015`; `"reporting bias" crowdsourced OR "citizen" flood reports location`; `flood reports social media bias population roads`
- RQ5: `FABDEM accuracy urban Hawker 2022`; `FABDEM "small island" OR atoll OR coastal validation`; `"ESA WorldCover" accuracy built-up validation`; `"Google Open Buildings" OR "Microsoft building footprints" accuracy completeness small island OR "Global South"`; `"area-weighted" zonal statistics raster polygon exact extraction`
- RQ6: `"pluvial flood susceptibility" urban conditioning factors`; `"urban flood susceptibility" machine learning factors "imperviousness" "distance to drainage"`; `"flood susceptibility" "100 m" OR "250 m" grid urban`; `"waterlogging" susceptibility urban factors`

**Inclusion:** peer-reviewed journal articles first, then official dataset documentation. Published 2010 or later, unless a method is foundational (e.g. Hirzel et al. 2006, Phillips et al. 2009, Lobo et al. 2008). Prefer studies of urban, coastal or island settings, and studies with stated validation designs.

**Exclusion:** blogs, AI-generated summaries, Q&A sites, unsourced claims, predatory or unindexed venues, and preprints when a peer-reviewed version exists. A conference paper only if it is the canonical source of a method.

## 3. Agent split and budget

| Agent | Model | RQs | Output file | Budget |
|---|---|---|---|---|
| R1 | Sonnet | RQ1, RQ2 | `research/rq1_rq2_land_fraction_blocks.md` | about 25 searches and 15 source opens; target 6 to 10 cited sources |
| R2 | Sonnet | RQ3, RQ4 | `research/rq3_rq4_presence_only_bias.md` | about 25 searches and 15 source opens; target 8 to 12 cited sources |
| R3 | Sonnet | RQ5, RQ6 | `research/rq5_rq6_attributes.md` | about 25 searches and 15 source opens; target 8 to 12 cited sources, dataset documentation included |

Agents run in parallel, write only their own file, and do not edit `sprint.md`, `data_issues.md` or anything outside `research/`. They do not touch git.

## 4. Output format (every agent)

1. **Search log:** the queries run and the number of useful hits for each.
2. **Evidence table**, one row per source, with these columns: citation (authors, year, title, journal), DOI or URL, what the study did (task, data, resolution, labels, validation), finding relevant to the RQ, and confidence note. The confidence note says `full text` or `abstract only`, plus any caveat (setting differs from Malé, sample size, etc.).
3. **Recommendation for this project**, per RQ, with its limits. Where sources disagree or nothing applies, say so. Write `unknown` rather than guess.
4. **Candidates for MF-19:** journal articles worth using in the literature review.

Rules: open each source before citing it. Never cite from memory. If a DOI does not resolve or the page is not readable, say so. Quote the key sentence for any numeric claim (a block size, a minimum presence count, an accuracy figure).

## 5. How the findings feed decisions

| Finding | Goes into | Who decides |
|---|---|---|
| RQ1 land-fraction rule | `scripts/define_spatial_blocks.py` and `reports/mf26_blocks_proposal.md` (B3), with the sensitivity check at 0.1, 0.25 and 0.5 | **Group decision** (MF-26 stays a proposal) |
| RQ2 block layout and fold count | B3 block proposal; later MF-51 | **Group decision** |
| RQ3 method options, minimum presences, metrics | `reports/mf50_decision_record.md` (B4) | **Group decision** (MF-50) |
| RQ4 bias handling | B4 decision record; B1 keeps `pumping_only` flags and `location_group` so either choice remains possible | Bias method: **group decision**. Flags: built now |
| RQ5 aggregation method, building source, raster caveats | `scripts/compute_grid_attributes.py` (B2) and its docstring | Orchestrator picks the building source from RQ5 and states it. The group can change it |
| RQ6 attribute list | B2 column list. Infeasible factors (drainage, surveyed DEM) are listed as missing, never proxied silently | Orchestrator, within the MF-22 acceptance |

The research summary (`research/summary_area_pipeline.md`) collects the recommendations, the open group decisions, and the "Candidates for MF-19" list.

## 6. Pending before the build (Phase C)

- **MF-16 on `origin/Aslan-work`:** the student decides whether to merge it before MF-21. It excludes Rasfannu and the Swimming Track, moves the STO point about 790 m to the north-harbour STO site, and reopens B2 (the `west_park_sto` location group no longer holds).
