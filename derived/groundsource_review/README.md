# Groundsource review for Malé island

Reviewed 17 November 2026. The original `groundsource_2026.parquet` was read only; no project labels were changed and no model was retrained. This review is preliminary and separate from the existing inventory. **Two previously absent Malé rain-flood event dates, 13 April and 11 October 2024, are independently corroborated and suitable for a later manual label review.** They are not yet incorporated into any model. The file does not identify the original article for either Groundsource row, so the match to the independent evidence is by date and geography, not verified provenance.

## Source, documentation and identity

The file was found at the project root and another file with the same name was found in Downloads; the Downloads copy was not inspected. The project-root file is 667,122,400 bytes (636 MiB). Its MD5, `cd1b5de6508f7aad8e1d1d0dd4cecea6`, matches the checksum for the [Zenodo v1 release, DOI 10.5281/zenodo.18647054](https://zenodo.org/records/18647054). The accompanying authoritative methods are in the [Google Research authors’ unreviewed preprint](https://eartharxiv.org/repository/object/12083/download/21690/) and the [Google Research explanation](https://research.google/blog/introducing-groundsource-turning-news-reports-into-data-with-gemini/). The [Earth Engine community catalogue](https://gee-community-catalog.org/projects/groundsource/) describes the dataset licence as CC BY 4.0; the Zenodo page's license value was not exposed in the accessible rendering, so the exact original release licence should be confirmed at Zenodo before redistribution. The preprint itself is [CC BY 4.0](https://eartharxiv.org/repository/view/12083/); that is a separate licence statement from the dataset.

The authors say Gemini extracts information from news articles and other web reports. The pipeline groups mentions of the same geographic entity on the same or consecutive dates, then emits a location-based event interval. One real storm can generate multiple rows for different geographic entities; multiple articles can be combined in a single row. The polygons are geocoded **location boundaries**, including administrative areas or buffered points, not observed inundation outlines. The reported `area_km2` is the area of that location geometry, not a measured flooded area. This is an automatically extracted, news-derived event catalogue; it is not a sensor-observation series, a flood-depth product or a forecast-model output. Individual claims have not been manually verified by this review merely because they appear in the dataset.

The authors report their global manual sample was 60% exact on location and date, with another 22% approximate or partial and 18% wrong. Those figures do not establish accuracy for Malé. Their preprint identifies wrong-place matches, imputed dates and publication/update-date errors as possible failure modes. Original event-source URLs and text are not in this release, so the pipeline’s verification cannot be repeated for a particular row without finding the source independently.

## File overview: inspected metadata first, then batches

GeoParquet contains 2,646,302 rows in three row groups. The six physical fields and their file-wide null counts are:

| Field | Arrow type | Nulls | Meaning |
|---|---|---:|---|
| `uuid` | string | 0 | record identifier |
| `area_km2` | double | 0 | area of location polygon |
| `geometry` | binary | 0 | WKB Polygon or MultiPolygon, WGS84 / EPSG:4326 |
| `start_date` | string | 0 | extracted initial date, day resolution |
| `end_date` | string | 0 | extracted final consecutive date, day resolution |
| `__index_level_0__` | int64 | 0 | serialized pandas index, not an event attribute |

The date range in this file is 2000-01-01 to 2026-02-03. Zero nulls do not imply accuracy. Coordinates are encoded in polygon WKB, not point latitude/longitude columns. There are **no fields at all** for country, place names, article URLs, article publication dates, supporting text, flood onset time, cause, depth, severity, or observation coverage. Consequently their absence cannot be summarized as ordinary null counts. Source article publication dates and onset times in the review table come only from independently found material, not from the Parquet.

## Geographic screen and limits

The source schema makes country-field and place-name searches impossible: neither field exists. Searching the string “Male” is not an alternative because the file contains no location strings. We screened every polygon in 16,000-row PyArrow batches against a generous geographic rectangle 72.3–74.1°E, 1°S–7.5°N, and then intersected the existing OneMap Malé island polygon. This is a **regional bounding-box candidate screen**, not a complete country-boundary join; the 260 candidates from 26 December 2004 to 28 December 2025 are not 260 verified Maldives events. The broad box and polygon intersection can admit large areas, false geocodes, or non-Maldives polygons; it also cannot recover a Maldives event erroneously geocoded outside the rectangle. Country and place attribution needs source tracing and a complete national island boundary.

Of those 260, 55 intersect a small Greater Malé screening box; 43 intersect the OneMap Malé boundary. The per-record [Malé review](male_candidate_review.csv) classifies these 55 as follows:

- 16 local polygons within or overlapping Malé: spatially relevant, but their event, cause, dates and exact reported place require source verification.
- 27 ambiguous city/multi-island or atoll geometries: 24 repeated multi-island geometries and three atoll-scale geometries. Intersection does not prove flooding on Malé.
- 11 polygons geographically consistent with other islands: five Vilimalé, three Hulhulé and three Hulhumalé; these island names are spatial inferences, not source attributes. One other local polygon is geographically ambiguous.
- Unrelated name matches: no text search is possible, and no specific candidate was conclusively identified as an unrelated geocoding error. This is **unknown**, not proof that none exist.

The 43 Malé-intersecting records have 29 distinct start dates and cover 49 distinct calendar dates if all extracted inclusive intervals are expanded and unioned. These are **candidate dates**, not 49 verified reported flood days. They are not 43 storms: repeated geometries and overlapping intervals commonly represent the same episode, and broad geometries add further uncertainty. Independent storm count cannot be established from these records. `maldives_spatial_candidates.csv` retains WKT and coordinates for the 260 spatial candidates; `candidate_summary.csv` omits WKT. The CSV centroids, bounds and inferred island names are analytical derivatives, not source fields.

## Event review and comparison

The comparison in [inventory_comparison.csv](inventory_comparison.csv) covers every intersecting candidate date; [male_candidate_review.csv](male_candidate_review.csv) records all 55 local-screen candidates, including excluded other-island records. Evidence links in those files are **independently located**, not claimed to be the original article used by Groundsource.

1. **13 April 2024 — new rain-flood candidate.** [NDMA's 2024 incident log](https://ndma.gov.mv/storage/uploads/50wNdLqA/vzrqjkea.pdf) lists a Malé rainwater flooding incident on 13 April (incident 2024/52). A [Sun report published 14 April](https://see.mv/88720) reports Saturday morning rain, flooded Malé roads and homes, and 85 buildings reporting damage. This supports a 13 April Malé event, without a precise flood-onset time or confirmation that flooding persisted on 14 April. Groundsource's city geometry includes multiple islands. The evidence supports a new event for further manual review, not every location in that polygon.
2. **11 October 2024 — new rain-flood candidate.** The same [NDMA incident log](https://ndma.gov.mv/storage/uploads/50wNdLqA/vzrqjkea.pdf) lists two Malé rainwater incidents dated 11 October (2024/208 and 209). They are incident records and could be related to the same storm. They support a Malé reported day but do not prove that either corresponds to the small Groundsource polygon. Do not treat the two records as two independent storms.
3. **12 January 2024 — existing uncertain event now independently corroborated.** A [Sun article published 13 January](https://en02.sun.mv/87030) explicitly reports Friday rain flooding Malé streets and homes. This supports 12 January as a reported day, although whether it was independent of the 10 January event remains unresolved. The existing masked label was not changed.
4. **13 August 2024 — existing event.** [The Edition](https://edition.mv/katy_perry/35325), published 13 August, reports Malé streets flooded by rain starting around 11:00; it does not establish flood onset at 11:00. NDMA also records 13 August. Groundsource intervals starting 12 August or ending 14 August should not automatically label those additional days.
5. **20–21 December 2024 — existing uncertain event.** A separately located [21 December article](https://atolltimes.mv/post/news/10805) reports rain beginning Friday night and flooding/drainage overnight. This is stronger contemporaneous evidence than the source used in the earlier review, but does not fix a precise flood onset or establish that both dates were flood days. This may warrant revisiting the existing masked label; no change was made.
6. **31 December 2023, 3 and 11 January and 1 March 2025** overlap events already in the inventory. The common date ranges and multiple locations indicate possible duplication, not independent new storms. Groundsource's 2–7 January 2025 city interval is much longer than the single retained 3 January day; its extra days are not independently established here.
7. **15 June 2019 and 5 August 2023** coincide with independent reports of [tidal swell flooding](https://archive.mv/en/articles/6vnVL) and [wave flooding](https://atolltimes.mv/post/news/4910), respectively. They are coastal rather than rain-flood labels. The 26 December 2004 candidate coincides with the [tsunami](https://ndma.gov.mv/en/galleries/tsunami); estimates of Malé impact differ across published accounts, so do not infer exact extent from the polygon. None should be added to a rain-only target.
8. The remaining dates lack a checked source tied to the individual row; their geography, mechanism, exact date and relationship to other events remain unresolved. A separate NDMA entry for 18 September 2024 in the same log may be useful for future inventory review, but it was not matched to a Groundsource candidate and is not counted here.

## Does it fix project limitations?

- **New dates:** two independently corroborated candidate events, not yet incorporated. They add potential positives but do not transform the small, selective inventory or prove storm independence.
- **Onset and days:** Groundsource gives day-level intervals only; no publication date or time. The independent reports sometimes clarify timing but do not confirm every Groundsource interval day.
- **Roads and severity:** small polygons can point to places to investigate, but without names and source text they cannot establish flooded road segments, depths, flood extent or severity. Their area is geographic area, not water extent.
- **Dry observations:** none; no observation frame or surveillance completeness is documented. Absence is unknown, never evidence of no flooding.
- **Modelling:** valuable leads for manual verification; insufficient by itself to validate daily modelling or support street-level risk mapping. Geocoding and extraction errors, reporting bias and date uncertainty remain.

## Next actions

1. Independently verify and document the 13 April and 11 October reports, group any related reports into conservative events, and review the previously masked 12 January and 20–21 December dates. Obtain source dates and observation context before altering labels.
2. Obtain Groundsource record-to-article provenance or conduct date- and location-specific archive searches, prioritising post-2020 local polygons and multi-day intervals; distinguish surge and tsunami from rain. Review the separate NDMA 18 September lead.
3. Request systematic event-location and observed-dry/coverage records plus local rainfall and timing metadata from relevant agencies; only then reassess evaluation. Do not retrain until the candidate review is complete.

## Reproduce the spatial screen

With Python 3.12, `pyarrow`, `shapely`, and `pandas` installed in an environment, run `python derived/groundsource_review/inspect_groundsource.py` from the project root. This reads but does not write the Parquet; it rewrites the screening CSVs and overview JSON. The manually curated review and comparison CSVs are not automatically regenerated by the screening script. No full in-memory Parquet load was used.
