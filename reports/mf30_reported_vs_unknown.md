# MF-30: cells with reports vs cells with no report (unknown)

**Descriptive only. No model was fitted, scored or ranked.** All numbers come from `scripts/compare_reported_unknown.py` (outputs in `derived/mf30/`).

## 1. Purpose
Describe how cells of the 200 m Malé grid that have a flood report differ in simple terrain and built-environment attributes from cells with no report. Evidence is positive-only: a cell with no report is **unknown**, not dry. Counts are reports, not flood frequency, and nothing here ranks cells or wards.

## 2. Data and cell set
Inputs: `grid_evidence.csv`, `grid_attributes.csv`, `grid_blocks.csv`, `ward_evidence_summary.csv`. Main cell set: land fraction >= 0.25 plus the MF-26 exception cell G333600_461800 = **57 of 75 cells** (sensitivity: no cutoff, all 75). FABDEM comparisons leave out cells with exact-zero pixel share > 0.1 (likely the inherited sea mask); this drops V1 1 reported / 4 unknown, V2 1 reported / 4 unknown, V3 1 reported / 4 unknown, V4 1 reported / 4 unknown cells. Results with those cells kept are in `group_summary.csv` (fabdem_filter = all_cells). The designated cell (G334400_461600, Machchangolhi) is kept out of both groups in every version.

## 3. Method
Four versions, always unknown as the comparison group:
- V1 stated flooding vs unknown.
- V2 stated + pumping-only vs unknown.
- V3 stated, excluding the 6 construction-confounded cells (RF071 only, issue E5); confounded cells left out of both groups.
- V4 V1 without the 2 routine pump-site cells (IGMH, West Park/STO).
Per group: n, median, IQR, min, max, difference in medians, and the share of reported cells whose value lies inside the unknown group's IQR. The groups are biased samples (reports cluster at arterials and landmarks), so differences describe these cells only.

## 4. Key tables (main cell set)
### Cells per group
| Version | Reported | Unknown |
|---|---|---|
| V1_stated | 11 | 40 |
| V2_stated_plus_pumping | 16 | 40 |
| V3_stated_excl_confounded | 6 | 40 |
| V4_V1_excl_routine_pump_sites | 9 | 40 |

No-cutoff sensitivity: V1 12 / 57; V2 17 / 57; V3 6 / 57; V4 10 / 57 (reported / unknown).

### Medians (reported / unknown), n after FABDEM filter
| Attribute | V1 | V3 | V4 |
|---|---|---|---|
| fabdem_mean_m | 5.46 / 5.35 (n 10/36) | 3.22 / 5.35 (n 5/36) | 5.82 / 5.35 (n 8/36) |
| fabdem_p10_m | 1.56 / 4.18 (n 10/36) | 1.26 / 4.18 (n 5/36) | 1.86 / 4.18 (n 8/36) |
| building_coverage_google075 | 0.296 / 0.314 (n 11/40) | 0.28 / 0.314 (n 6/40) | 0.296 / 0.314 (n 9/40) |
| worldcover_builtup_share | 0.574 / 0.527 (n 11/40) | 0.577 / 0.527 (n 6/40) | 0.574 / 0.527 (n 9/40) |
| road_density_vehicular_m_per_km2 | 2.91e+04 / 3.13e+04 (n 11/40) | 2.8e+04 / 3.13e+04 (n 6/40) | 2.94e+04 / 3.13e+04 (n 9/40) |
| dist_land_centroid_to_coast_m | 70.9 / 228 (n 11/40) | 75.9 / 228 (n 6/40) | 70.9 / 228 (n 9/40) |

### Overlap: share of V1 reported cells inside the unknown IQR
| Attribute | V1 | V3 | Reported range (V1) | Unknown range |
|---|---|---|---|---|
| fabdem_mean_m | 0.30 | 0.20 | 0.73 to 7.65 | 0.738 to 8.05 |
| fabdem_p10_m | 0.50 | 0.60 | 0.46 to 6.07 | 0.45 to 6.36 |
| building_coverage_google075 | 0.55 | 0.33 | 0.146 to 0.419 | 0.118 to 0.441 |
| worldcover_builtup_share | 0.73 | 0.67 | 0.292 to 0.837 | 0.297 to 0.779 |
| road_density_vehicular_m_per_km2 | 0.64 | 0.67 | 2.13e+04 to 3.51e+04 | 1.15e+04 to 4.19e+04 |
| dist_land_centroid_to_coast_m | 0.18 | 0.17 | 22.2 to 422 | 11.9 to 511 |

### Wards (main set; not a ranking)
| Ward | Cells kept | Reported | Pumping only | Designated | Unknown | V1 | V3 |
|---|---|---|---|---|---|---|---|
| Galolhu | 8 | 0 | 1 | 0 | 7 | 0 | 0 |
| Henveiru | 17 | 8 | 2 | 0 | 7 | 8 | 3 |
| Maafannu | 22 | 3 | 1 | 0 | 18 | 3 | 3 |
| Machchangolhi | 10 | 0 | 1 | 1 | 8 | 0 | 0 |

Ward medians are in `ward_table.csv`.

## 5. What the figures show
`strip_<attribute>.png` plots each cell as a dot, reported vs unknown (no report), for V1 (left) and V3 (right), with boxes for median and IQR. `scatter_elev_coast.png` plots FABDEM 10th percentile elevation against distance to coast, with marker shapes for status, rings for confounded cells and crosses for routine pump sites.
In words, for V1 the reported cells have median fabdem_mean_m 5.46 against 5.35; fabdem_p10_m 1.56 against 4.18; building_coverage_google075 0.296 against 0.314; worldcover_builtup_share 0.574 against 0.527; road_density_vehicular_m_per_km2 2.91e+04 against 3.13e+04; dist_land_centroid_to_coast_m 70.9 against 228. For V3 the reported-cell medians are fabdem_mean_m 3.22 against 5.35; fabdem_p10_m 1.26 against 4.18; building_coverage_google075 0.28 against 0.314; worldcover_builtup_share 0.577 against 0.527; road_density_vehicular_m_per_km2 2.8e+04 against 3.13e+04; dist_land_centroid_to_coast_m 75.9 against 228. Where the share inside the unknown IQR is high (table above) the groups overlap on that attribute; where it is low they separate in these cells.

## 6. Limits
- Positive-only evidence: unknown cells include cells that flooded without a report, so differences may be understated or biased.
- Reporting favours arterials and landmarks, so reported cells are not a random sample.
- Pump sites: pumping-only and routine pump-site records reflect where pumps are stationed (V2 and V4 show the effect).
- 6 cells are confounded: their only stated flooding is RF071 (30 Jul 2026, blamed on pumps not yet commissioned, E5). V3 therefore has 6 reported cells in the main set (5 with FABDEM), so medians are very unstable.
- FABDEM is relative only, not surveyed, with known bias; exact zeros are likely sea mask. WorldCover built-up share is near saturation on land, so it separates little. Building coverage is one source (Google, confidence >= 0.75).
- The four OSM wards are not checked against a Council map; ward rows describe small n and are not comparable by size.
- Differences are descriptive and not tested for any population.

## 7. For MF-50
Facts only: see the overlap table for which attributes separate or overlap between the groups, and the V3 and V4 columns for how the picture changes when confounded cells or routine pump sites are removed. Use the MF-50 draft for any modelling decision.
