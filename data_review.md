# Road-flood data review: Malé island proper

Reviewed 14 Nov 2026. Scope: which roads or road sections on Malé island proper are prone to rain-driven flooding. No model has been trained. Raw files are unchanged; every derived output can be regenerated with `scripts/build_road_flood_inventory.py` and then `scripts/match_road_flood_records.py`.

## 1. Summary

- The new folder `male-flood-basis/` contains the project's first **location-specific** flood evidence for Malé. It covers 18 rain-flood incidents (Dec 2021 to Oct 2026), **7 named roads, 2 bounded road sections, 15 landmarks** and 3 ward or city mentions on Malé.
- All of it is **positive-only, secondary evidence**: a compilation of news and agency reports made with AI assistance. I have not opened the roughly 40 linked articles, so no record is rated above "medium" confidence.
- All 7 roads match the OSM layer. Three matches are confident only because of Dhivehi-name aliases. Rahdhebai was uncertain until a source-article and junction check (MF-14, 17 Nov 2026) confirmed it. Landmarks are kept as points and not assigned to roads.
- The evidence supports a **documented map of reported flood-prone roads and places**, which is built, and **descriptive** comparison of road characteristics. It does **not** support a supervised flooded vs not-flooded classifier: there are no observed-dry roads, and the positives are few and concentrated on the main arterials.

## 2. Files reviewed

| File | Format | Contents | Road-flood value |
|---|---|---|---|
| `male-flood-basis/data/flood_incidents_greater_male_2021-2026.csv` | CSV, 18 rows | One row per incident: dates, summary, reported rainfall text, Malé mm, place list, source URLs | **High.** Primary table for the inventory |
| `male-flood-basis/data/flooded_roads_and_places_greater_male.csv` | CSV, 32 rows | One row per place: type, island, times reported, dates, coordinates, note, URLs | **High.** Place list and coordinates (road coordinates are midpoints) |
| `male-flood-basis/data/flood_locations_greater_male.geojson` | GeoJSON, 31 features | 9 road MultiLineStrings and 22 points, with counts | **Medium.** Compiler's road lines are traced from OSM (vertices agree to 5 decimal places). Used to cross-check matches |
| `male-flood-basis/flood_map.html` | HTML page | Compiler's map, incident log and write-up | **Low.** Same data plus unsourced claims (§4.4) |
| `male-flood-basis/README.txt` | Text | File list | Context |
| `male-flood-basis/data/male_daily_features_with_flood_labels.csv` | CSV, 2,509 days | Daily weather with `flood_reported` (22 days = 1) | Not road evidence. Forecasting-oriented; 0 means "no report found", not dry |
| `male_reanalysis_hourly/daily_2020-2026.csv`, `hulhule_station_daily_2020-2025.csv`, `male_sea_level_waves_hourly_2022-2026.csv`, `male_forecast_hourly_snapshot_2026-11-14.csv` | CSV | ERA5 (Open-Meteo), NOAA GSOD, modelled sea level and waves, one forecast run | Not road evidence. Possible context later |
| `Male_Flood_Data_Starter_Pack/flood/event_candidates.csv` (existing) | CSV, 3 rows | City-level date leads | No road detail. Dates overlap the new incidents |

## 3. Evidence counts

`derived/road_flood_inventory.csv` has one row per place named in an incident: **73 records**. Of these, **67 are on Malé** (63 inside the OneMap polygon, 3 waterfront points just outside it, 1 without coordinates) and 6 are on other islands.

Malé records only (67):

| Spatial scope | Records | Distinct places |
|---|---|---|
| Whole road named, section unknown | 14 | 7 roads |
| Bounded road section | 2 | 2 sections |
| Vague section ("central part of Majeedhee Magu") | 1 | 1 road |
| Landmark vicinity | 41 | 15 |
| Ward | 4 | 2 wards |
| City-wide, no streets | 5 | 1 |

| Evidence type | Records |
|---|---|
| Dewatering / pump deployment reported | 31 |
| News report of flooding | 23 |
| Photograph reported (news or JICA survey) | 5 |
| Council flood-prone / repair list (designation, not a dated sighting) | 4 |
| Other impact (road closed, pavement dug up) | 2 |
| Official statement, no streets named | 1 |
| Houses flooded, no roads stated | 1 |

There are **no** observed-dry records, **no** model outputs and **no** citizen complaints. Confidence ratings: 60 medium, 7 low, 0 high (RF041 Rahdhebai raised to medium after its source check, MF-14).

Roads and how many separate incidents name them (the dated records are mostly whole-road mentions; one is a bounded section):

| Road (original spelling) | OSM name | Incidents | Notes |
|---|---|---|---|
| Majeedhee Magu | މަޖީދީ މަގު | 4 (one is the council repair list) | Plus bounded section Dhanburuh–Nikagas Magu (council's "stretch that floods most") |
| Ameenee Magu | އަމީނީ މަގު | 4 | Two photographed under water |
| Boduthakurufaanu Magu | ބޮޑުތަކުރުފާނު މަގު | 3, plus 1 bounded section | Section flood 30 Jul 2026 blamed on pumps not yet commissioned |
| Kan'baa Aisa Rani Hingun | Kanbaa Aisa Rani Hingun | 1 | Water "passed two feet" (about 0.6 m), 3 Jan 2025 |
| Izzuddeen Magu | Izzuddeen Magu | 1 | Same as above |
| Chaandhanee Magu | Chandhanee Magu | 1 (repair list only) | |
| Rahdhebai Magu | Rah Dhebai Magu (confirmed, MF-14) | 1 (repair list only) | No source coordinates; located by the OSM match |

Most-mentioned landmarks: IGMH area (10 incidents), West Park area (8), Villimalé Ferry Terminal (5), STO flour warehouse area (3). All four are on the west side of Malé.

Rainfall comes with an amount for only **5 of 18 incidents**, all at daily scale:

| Incident | Malé amount | Accumulation period | Issue |
|---|---|---|---|
| 30–31 Dec 2023 | 118.2 mm | unknown | "24 h" is stated for the Hulhulé figure (179.9 mm) only |
| 13 Aug 2024 | 89.4 mm | 24 h, 08:00–08:00 | End date not stated |
| 20–21 Dec 2024 | 136.5 mm | 24 h, 08:00 Fri to 08:00 Sat | |
| 2–3 Jan 2025 | 142.2 mm | unknown | Contradicted by "162 mm by 11 pm in another count" |
| 21 Oct 2026 | 90 mm | 24 h | |

No hourly intensities are reported. For 1 Mar 2025 the source gives only a duration ("about two hours of rain").

## 4. Data issues

### 4.1 Duplicates and double counting
- **Majeedhee Magu on 20–21 Dec 2024** appears both as the whole road and as the bounded section. The summary only says the council *repaired* the road afterwards, so the whole-road record is a designation that the compiler counted as an incident (`times_reported = 4` should be read as 3 reported floods plus 1 designation).
- **West Park and STO flour warehouse** points are about 40 m apart and share 3 incident dates. They probably describe the same flooded spot.
- **Kudakudhinge Bageecha** is on Ameenee Magu. On 3 Jan 2025 both are reported, so this may be one location counted twice.
- Repeat counts at **IGMH and West Park** are partly pump-deployment reports. Some of that repetition may reflect where pumps are routinely placed, not how deep the flooding was.

### 4.2 Contradictions
- The places file says Rahdhebai Magu is "not in the base map data", but the OSM layer has *Rah Dhebai Magu* (2 segments, 548 m). Rahdhebai also appears with date 20–21 Dec 2024 in the places file but is **missing** from that incident's location list. The Atoll Times article (28 Dec 2024) lists it with Chaandhanee and Majeedhee among the roads repaired, so the omission looks like a compiler error (resolved in MF-14).
- 3 Jan 2025 rainfall: 142.2 mm vs 162 mm.
- The compiler's Majeedhee section line is 83 m long, but the junctions with Dhanburuh Magu and Nikagas Magu are 44 m apart. The line runs about 38 m past the Nikagas junction. The 44 m clip is used.

### 4.3 Missing values
- Rahdhebai Magu has no coordinates. Road coordinates elsewhere are **midpoints**, not flood locations.
- No flood extent, depth (except "passed two feet" on 2 roads), duration, time of day (mostly) or junction-level detail for the whole-road mentions.
- Rainfall is missing for 13 of 18 incidents. The accumulation period is unknown for 2 of the 5 that have an amount.
- On city-wide days (13 Aug 2024 "nearly every street", 3 Jan 2025 "most of the city", 21 Oct 2026) the reports name only a few places. I added 2 city-wide rows from the summary text so these days are not misread as "only the named roads flooded".

### 4.4 Uncertain interpretations and unverified claims
- "Pumps ran at two sites near IGMH, West Park and near the Polytechnic": three places are named but two sites are counted. All three are rated low confidence.
- Rasfannu on 13 Aug 2024 "was closed". Flooding there is implied, not stated.
- Henveiru ward on 30–31 Dec 2023: houses flooded, with no road flooding stated.
- Landmark positions are the compiler's. Two are marked approximate, and three Malé waterfront points fall just outside the OneMap polygon.
- The `flood_map.html` text includes claims without a linked source in the file: "40 to 45 mm daily rain at which Malé starts to flood, per a Met Office official (Aug 2024)"; "16 pump stations of about 400 m³ per hour"; "the NOAA copy … totals under half the true annual rain". Treat all three as leads to verify, **not** facts. The first one in particular is not a verified threshold.
- The JICA 2021 survey photographs are the closest thing to primary evidence. The report URL is listed but I have not read it.

## 5. Matching to the OSM road layer

Output: `derived/road_match_review.csv` (one row per place, 32 rows). The base layer has 571 features totalling 65.7 km, 29% of them unnamed.

| Status | Places | Detail |
|---|---|---|
| `confident_whole_road_name` | 7 | Majeedhee, Ameenee and Boduthakurufaanu (via Dhivehi `name`); Kan'baa Aisa Rani, Izzuddeen, Chaandhanee, Rahdhebai (spelling variants). 50 OSM segments, 11.6 km. Every name-matched segment except one of Boduthakurufaanu's overlaps the compiler's line (Rahdhebai has no compiler line). Rahdhebai → *Rah Dhebai Magu* (MF-14). There is no source geometry, but the Edition article diverts traffic "from Chaandhanee Magu to Rah-dhebai Magu" around the closed Majeedhee section, and in OSM those two roads are the nearest crossings of Majeedhee on either side of it. *Rah Dhebai Hingun* does not reach Majeedhee. |
| `confident_section_partial_segments` | 1 | Majeedhee, Dhanburuh–Nikagas Magu: 44 m inside one 0.9 km OSM segment. Split the segment before labelling. |
| `uncertain_section_extent` | 1 | Boduthakurufaanu, Henveiru Ferry Terminal to Izzuddin Jetty: 11 segments under the compiler's approximate 779 m line. The ends are landmarks. |
| `uncertain_landmark_not_assigned` | 15 | Named OSM roads within 50 m are listed as candidates only. Example: West Park → Boduthakurufaanu 10 m, Haveeree Hingun 16 m, Kanbaa Aisa Rani 22 m. |
| `unmatched_area_level` | 3 | Maafannu ward, Henveiru ward, city-wide |
| `out_of_study_area` | 5 | Midhili Magu, Hulhumalé roads and cemetery, Hulhulé, Villimalé |

Other points:
- The compiler's lines also cover **8 unnamed OSM segments** next to Majeedhee, Ameenee and Boduthakurufaanu. Reviewed in `derived/unnamed_segment_review.csv` (MF-15): none is part of the named carriageway. Six are footways or steps and one is an 8 m service stub. The eighth, a residential way (1528883097), duplicates 57 m of the Majeedhee centreline and must be dropped when segmenting the network so length is not counted twice.
- Evidence-linked segments total 11.65 km, **18% of the OSM network length**. Boduthakurufaanu (the ring road) alone is 5.1 km.
- Of the 56 linked segments, 26 are primary or secondary roads. Of the island's 35 primary or secondary features overall, 26 are linked. The evidence is therefore heavily concentrated on arterial roads.

Map: `derived/road_flood_evidence_map.png`, with the QGIS layer `derived/road_flood_matched_segments.geojson`. Grey roads are labelled **unknown**, not dry.

## 6. What the evidence can support

| Output | Supported? | Why |
|---|---|---|
| Documented map of reported flood-prone roads and places | **Yes (built)** | Every feature traces to an inventory row and source URLs. Wording must be "reported" or "named in reports", not "flood extent". |
| Exploratory analysis of road characteristics | **Yes, descriptive only** | Compare evidence roads and landmark surroundings with **unknown** roads on road class, length, junction density, coast distance, building cover (one building source), WorldCover, FABDEM (coarse). Differences describe *reported* roads, and reporting bias toward arterials will show up. |
| Supervised flooded vs not-flooded classifier | **No, not defensibly** | There are no observed-dry labels, and treating unknown roads as dry would manufacture negatives. Positives come from about 7 roads, and three arterials dominate. A classifier would mostly learn "is a main road" or "is near IGMH/West Park", and any accuracy figure would be meaningless. |
| Positive-only susceptibility ranking (exploratory) | **Possible, with caveats** | Positive-unlabelled learning or presence-background models (MaxEnt-style) can *rank* segments by similarity to reported locations. Report it as a ranking with stated bias, never as a probability of flooding. Positive-unlabelled methods also need an assumption about how reports were sampled, and that assumption is clearly violated here (arterial and landmark bias). |
| Rainfall-response or threshold analysis | **No threshold; descriptive table only** | There are 5 amounts, all from flood days, at daily scale, with mixed or unknown periods and one contradiction. There are no reported non-flood days with matching gauge data. You can state "reported floods occurred with daily totals of about 89–142 mm"; you cannot state a trigger threshold. ERA5 badly underestimates these days (per the compiler: 56 mm vs 142 mm on 3 Jan 2025), and MMS hourly gauges would be needed. |

**Evaluation, if a ranking model is attempted later:**
- Use spatial cross-validation. Keep **all segments of one road in the same fold** (a road appears in several reports and spans the island), and preferably block by area as well (the four wards, or roughly 300–500 m tiles). Never split segments of Majeedhee, Ameenee or Boduthakurufaanu across train and test.
- Treat each landmark and its candidate roads as one group. Merge near-duplicate places (West Park and STO) before splitting.
- Metrics for positive-only data: the share of held-out positive places that fall in the top *k*% of ranked network length (recall at *k*), and the continuous Boyce index. Do not report accuracy, precision or specificity against unknown roads.
- Fit all preprocessing inside each training fold. Report results with and without the arterial roads to show how much the reporting bias drives the result.

## 7. Remaining gaps

1. **Observed-dry and complete location records.** Ask the City Council and NDMA (assistance-request logs with addresses; 774 requests on 3 Jan 2025 per the compilation) and MNDF (pump deployment logs). These logs would also give junction-level detail.
2. **Primary-source checks** of the road and landmark mentions.
3. **Drainage:** pump-station and outfall locations and the stormwater network (MWSC, council, World Bank project). These are probably the strongest predictors of where water stands.
4. **Ground elevation:** a surveyed DEM or spot heights. FABDEM at about 30 m cannot separate one street from the next.
5. **Hourly rainfall** from MMS gauges for the dated incidents. This is needed only for any later rainfall-response work.
6. Assignment requirements still unconfirmed (see `agent.md` §3).

## 8. Recommended next step

1. **Verify the 17 road records and the top 4 landmarks** against their source articles. Add a quoted phrase and any junction or section detail to the inventory, and raise confidence where the article confirms it. This is the cheapest way to improve label quality.
2. Then **split the OSM network at junctions** into block-length segments and build a segment table: evidence status (reported / designated / landmark-candidate / unknown) plus descriptive attributes. Run the exploratory comparison in §6.
3. Send the data requests in §7 in parallel (with the student's approval). Choose between a ranking model and a purely descriptive map only after seeing whether any observed-dry or complete-coverage data can be obtained.
