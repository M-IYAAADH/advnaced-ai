# MF-26: land-fraction rule and spatial blocks

**PROPOSAL FOR THE GROUP: not a decision.** All numbers come from `scripts/define_spatial_blocks.py` (output `derived/grid_blocks.csv`).

## 1. Purpose
Propose (i) a land-fraction cutoff for the 75-cell, 200 m grid and (ii) contiguous spatial blocks for spatial cross-validation and for reporting. Evidence is positive-only: unknown is never dry, and dropped cells are "not assessed", never low susceptibility.

Positive versions: **(a)** stated flooding only (status reported_flooding, 12 cells); **(b)** stated + pumping_only (17); **(c)** (a) excluding the 6 cells whose only stated flooding is RF071, a Boduthakurufaanu section flood blamed on pumps not yet commissioned (6 cells).

## 2. Evidence base
- `research/rq1_rq2_land_fraction_blocks.md` (sections 3 and 4) and `research/summary_area_pipeline.md`.
- No flood study found states a land-fraction cutoff. The only analogue is Budic et al. 2016 (down-weight partial-land cells, mask the sea), so any cutoff is a project choice.
- Roberts et al. 2017 (abstract only read): blocked CV is preferred under spatial structure. Ploton et al. 2020 (full text read): blocks slightly longer than the autocorrelation range, and even that can be too small. Valavi et al. 2019 (blockCV) is the tool reference. The fold count and block size (about 5 blocks of 600 to 800 m) are the research agent's judgement, not from a source.

## 3. Land-fraction sensitivity
| Cutoff | Cells kept (of 75) | Positives kept (a) / (b) / (c) |
|---|---|---|
| none | 75 | 12 / 17 / 6 |
| 0.10 | 63 | 11 / 16 / 6 |
| 0.25 | 56 | 10 / 15 / 5 |
| 0.50 | 52 | 9 / 14 / 5 |

Positive cells a cutoff would drop (all stated flooding):
- G335000_462000, land fraction 0.096: dropped at 0.10, 0.25, 0.50. Construction-confounded, no location group.
- G333600_461800, 0.178 (West Park STO, location group west_park_sto, pumping also reported): dropped at 0.25 and 0.50. Not confounded, so version (c) loses it.
- G334800_462000, 0.357: dropped at 0.50 only. Construction-confounded, no location group.

**Proposed default: 0.25, with a keep-by-exception for G333600_461800.** Plain 0.25 drops a reported cell with a named landmark, which the summary says should prevent the default. Lowering to 0.10 keeps it but retains 7 more coast and jetty cells whose DEM and land-cover values are unreliable (this reasoning is judgement, not sourced). The exception keeps 57 cells, keeps all non-confounded positives, and drops only G335000_462000 (0.096, which is confounded). Its attributes must then be computed over the land part only. Run 0.10 and 0.50 as sensitivity checks as planned.

## 4. Block options (all 75 cells; queen adjacency)
k-means (random_state 0) on cell centres in EPSG:32643, then repaired so each location group sits in one block and each block is one connected piece. Positives are counted over all cells before any land cutoff.

| Layout | Blocks | Cells per block | Blocks with a positive (a) / (b) | Positives per block (a/b/c) |
|---|---|---|---|---|
| k = 4 | 4 | 20, 17, 19, 19 | 3 / 4 | 7/8/3, 0/3/0, 3/4/3, 2/2/0 |
| k = 5 | 5 | 15, 14, 16, 14, 16 | 4 / 5 | 2/3/2, 4/4/0, 0/2/0, 1/1/1, 5/7/3 |
| k = 6 | 6 | 13, 13, 11, 12, 15, 11 | 5 / 6 | see section 5 |
| 4 wards | 5 pieces | 9, 22, 31, 12, 1 | 2 / 4 | 0/1/0, 9/11/3, 3/4/3, 0/1/0, 0/0/0 |

The ward layout has one extra piece, a single jetty cell outside the ward polygons. Henveiru holds 9 of 12 (a) positives, so ward folds would leave most folds without a stated positive. Block extents are 600 to 1,200 m on a side. k = 5 has one block with no (a) positive, k = 6 has one.

## 5. Proposed layout: k = 6
Chosen because it gives the most blocks holding a version (a) positive (5 of 6) and every block holds at least one version (b) positive. It is a little smaller than the 5-block suggestion (11 to 15 cells, extents 600 to 1,000 m east-west and 800 to 1,000 m north-south).

| Block | Cells | Kept at 0.25 | Positives a / b / c | Wards touched |
|---|---|---|---|---|
| A | 13 | 10 | 2 / 2 / 0 | Galolhu, Henveiru, Maafannu, Machchangolhi |
| B | 13 | 10 | 1 / 1 / 1 | Maafannu |
| C | 11 | 7 | 5 / 6 / 1 | Henveiru |
| D | 12 | 10 | 2 / 3 / 2 | Galolhu, Henveiru, outside polygons |
| E | 15 | 12 | 0 / 2 / 0 | Galolhu, Maafannu, Machchangolhi |
| F | 11 | 7 | 2 / 3 / 2 | Maafannu |

Map (rows north to south by northing, columns west to east by easting; letter = block, lower case = land fraction under 0.25, not kept by the default; blank = no cell):
```
462200    baaa     
462000   bBAAAAcc  
461800  bBBBAAACCCc
461600  BBBBAAACCCc
461400 fFBBEEEDDDC 
461200 fFFEEEEDDDD 
461000 fFFEEEEDDDd 
460800 fFFEeeed    
```
Row labels are northing_min (m); columns run from easting_min 333400 to 335600 in 200 m steps. Exact positions are in `derived/grid_blocks.csv`.

Every location group lies in one block and every block is contiguous (checked by assert). Block C holds 5 of the 12 (a) positives but only 1 under (c), because the north-east Henveiru cluster is mostly the construction-confounded cells.

## 6. Autocorrelation indication (rough)
Moran's I of the version (a) indicator on the 56 cells kept at 0.25, queen weights: I = 0.200, permutation p = 0.003 (999 permutations, seed 0). Indicative only: positive-only labels (unknown cells are not true zeros), 56 cells, and the weights do not separate real clustering from clustered reporting and pump placement. It suggests the positives cluster, but it does not give a range, so block size remains a judgement.

## 7. Limits
- Only 12 stated positive cells (6 if the confounded cells are excluded), so fold-wise metrics will be very noisy.
- Routine pump sites and pumping-only cells mark where pumps are stationed, not only where water stood.
- Six stated cells rest on RF071 alone, a construction-related explanation rather than rain-driven flooding.
- The autocorrelation range is unknown; blocks of 600 to 1,000 m may still be too small (Ploton et al. 2020).
- Wards are OSM lines, not checked against a Council map.
- K-means centres depend on the fixed seed; a different seed could give a different layout.

## 8. Decisions for the group
1. Land-fraction default: 0.25 with the G333600_461800 exception, plain 0.10, or plain 0.25 (accepting loss of that cell)?
2. Count the 6 construction-confounded cells as positives (a) or treat them as (c) only?
3. Pumping-only cells in or out of the main presence set (b versus a)?
4. Accept k = 6, or use k = 5 (closer to the research suggestion, one block with no stated positive)?
5. Whether to merge block E (no stated positive) into a neighbour for CV, at the cost of fewer folds.
