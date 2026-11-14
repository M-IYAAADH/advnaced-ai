# Road-flood data issues: Malé island proper

Logged 14 Nov 2026 from the review of `male-flood-basis/`. Full context is in `data_review.md`. Record IDs (RFxxx) refer to `derived/road_flood_inventory.csv`.

Status key: **Open** means not yet resolved. **Handled** means a workaround is already applied in the derived files; the source itself is unchanged.

## A. Source reliability

| ID | Issue | Effect | Action | Status |
|---|---|---|---|---|
| A1 | All records come from a secondary, AI-assisted compilation of news and agency reports. None of the roughly 40 linked articles has been opened or checked. | No record can be rated high confidence (59 medium, 8 low). | Check the 17 road records and the top 4 landmarks (IGMH, West Park, Villimalé Ferry Terminal, STO) against their articles. Record a quoted phrase and any junction or section detail. | Open |
| A2 | `flood_map.html` claims "40 to 45 mm daily rain at which Malé starts to flood, per a Met Office official (Aug 2024)" with no linked source. | Risk of quoting an unverified number as a threshold. | Find the original statement or leave it out. Never use it as a trigger threshold. | Open |
| A3 | `flood_map.html` claims "16 pump stations of about 400 m³ per hour" without a source. | Unverified drainage-capacity figure. | Verify with MWSC, the council or the stormwater project documents. | Open |
| A4 | `flood_map.html` claims the NOAA GSOD rainfall "totals under half the true annual rain" and shows zero on several flood days. | If true, GSOD rainfall is unreliable for any rainfall work. | Compare GSOD annual totals with published MMS annual totals. | Open |
| A5 | The JICA 2021 survey photographs are the closest thing to a primary source, but the report has not been read. | Lost chance of higher-quality evidence. | Read the JICA report (URL in the incident file, row for 2021-12-11). | Open |

## B. Duplicates and double counting

| ID | Issue | Effect | Action | Status |
|---|---|---|---|---|
| B1 | On 20–21 Dec 2024, Majeedhee Magu appears both as the whole road and as the bounded section. The whole-road entry comes from the council repair list after the event, not from a report of flooding that day. | The source count `times_reported = 4` overstates it. It should read as 3 reported floods plus 1 designation. | Kept as `designated_flood_prone`, low confidence (RF039; the section is RF040). | Handled |
| B2 | The West Park and STO flour warehouse points are about 40 m apart and share 3 incident dates. | The same flooded spot is probably counted twice. | Merge them into one group before any spatial evaluation. | Open |
| B3 | Kudakudhinge Bageecha is on Ameenee Magu, and both are reported on 3 Jan 2025. | Possibly one location counted twice. | Check in the source article. Group them for evaluation. | Open |
| B4 | Repeat counts at IGMH and West Park are partly pump-deployment reports. | Repetition may show where pumps are routinely placed, not where flooding is worst. | Report counts by evidence type. Don't rank places by raw count alone. | Open |

## C. Contradictions

| ID | Issue | Effect | Action | Status |
|---|---|---|---|---|
| C1 | The places file says Rahdhebai Magu is "not in the base map data", but the OSM layer has *Rah Dhebai Magu* (2 segments, 548 m). | The road was left off the compiler's map. | Matched as `uncertain_probable_name_match`. Confirm the location. Don't confuse it with *Rah Dhebai Hingun*. | Open |
| C2 | The places file gives Rahdhebai Magu the date 20–21 Dec 2024, but it is missing from that incident's location list. | The two source files disagree. | Kept with a note and low confidence. Check the source (atolltimes.mv/post/news/10872). | Open |
| C3 | Rainfall for 2–3 Jan 2025 is given as 142.2 mm and also as "162 mm by 11 pm in another count". | Two amounts for one event. | Both are kept in the notes; the inventory uses 142.2 mm with the period unknown. Resolve with MMS data. | Open |
| C4 | The compiler's Majeedhee section line (Dhanburuh to Nikagas Magu) is 83 m long, but the junctions are 44 m apart. The line runs about 38 m past the Nikagas junction. | The section extent is overstated. | The clipped 44 m extent is used in the derived files. | Handled |

## D. Missing values

| ID | Issue | Effect | Action | Status |
|---|---|---|---|---|
| D1 | Rahdhebai Magu has no coordinates. | It can only be placed by name match. | Recorded as `unknown`. Confirm through C1. | Open |
| D2 | Road coordinates are midpoints, not flood locations. | They can't be used as flood points. | Labelled `compiler_road_midpoint_not_flood_point`. | Handled |
| D3 | Whole-road reports have no flood extent, section or junction detail. | Can't say which segments flooded. | Labelled `whole_road_named_section_unknown`. Not every segment is labelled flooded. Look for detail during source checks (A1). | Open |
| D4 | No depth is given except "passed two feet" (about 0.6 m) on Kan'baa Aisa Rani Hingun and Izzuddeen Magu, 3 Jan 2025. No durations, and mostly no times of day. | A depth or duration target isn't possible. | None for now. | Open |
| D5 | Rainfall is missing for 13 of 18 incidents. | Little rainfall context for the events. | Recorded as `unknown`. Request MMS gauge data. | Open |
| D6 | The accumulation period is unknown for 2 of the 5 incidents that have an amount (30–31 Dec 2023, 2–3 Jan 2025). For 13 Aug 2024 the 24 h window's end date isn't stated. | Amounts can't be compared fairly. | Recorded as `unknown`. Don't assume 24 h. | Open |
| D7 | On city-wide days (13 Aug 2024 "nearly every street", 3 Jan 2025 "most of the city", 21 Oct 2026) the reports name only a few places. | Unnamed streets could be misread as dry. | Added 2 city-wide rows from the summary text. Unnamed roads are treated as unknown. | Handled |

## E. Uncertain interpretations

| ID | Issue | Effect | Action | Status |
|---|---|---|---|---|
| E1 | "Pumps ran at two sites near IGMH, West Park and near the Polytechnic" (30–31 Dec 2023) names three places but counts two sites. | Unclear which places had pumps. | All three rated low confidence. Check the article. | Open |
| E2 | Rasfannu on 13 Aug 2024 "was closed". Flooding there is implied, not stated. | It might not have flooded. | Rated low confidence (`other_reported_impact`). | Open |
| E3 | Henveiru ward on 30–31 Dec 2023: houses flooded, with no road flooding stated. | Not road evidence. | Labelled `building_flooding_reported`. | Handled |
| E4 | Chaandhanee Magu (RF035) and Rahdhebai Magu (RF041) come only from the council's flood-prone repair list, not from a report of flooding on a given day. | These are designations, not dated reports of flooding. | Labelled `designated_flood_prone`. | Handled |
| E5 | The Boduthakurufaanu section flood on 30 Jul 2026 was attributed to drainage pumps not yet working on a newly rebuilt road. | A construction-stage cause, not typical flooding of that road. | Noted. Consider leaving it out of susceptibility analysis or flagging it. | Open |
| E6 | Landmark positions are the compiler's estimates. Rasfannu and STO are marked approximate, and Rasfannu and the Swimming Track fall just outside the OneMap polygon. | Possible position errors. | Flagged `yes_point_outside_onemap_polygon`. Check positions on imagery. | Open |

## F. Matching to the OSM road layer

| ID | Issue | Effect | Action | Status |
|---|---|---|---|---|
| F1 | Majeedhee, Ameenee and Boduthakurufaanu exist in OSM only under their Dhivehi names. | English name matching alone finds nothing. | A documented Dhivehi alias table is used, cross-checked against the compiler's geometry. | Handled |
| F2 | Similar-looking OSM names belong to different streets (*Amenee Goalhi*, *Rah Dhebai Hingun*). | Risk of false matches. | Explicitly excluded. | Handled |
| F3 | The compiler's lines cover 8 unnamed OSM segments next to Majeedhee, Ameenee and Boduthakurufaanu. | They may be parts of the same roads. | Left unmatched pending review. | Open |
| F4 | The Majeedhee section covers only 44 m of a 0.9 km OSM segment. | Labelling the whole segment would overstate the flooded section. | Split OSM segments at junctions before labelling. | Open |
| F5 | The Boduthakurufaanu section ends are landmarks (Henveiru Ferry Terminal, Izzuddin Jetty), and the extent is approximate. | The extent is uncertain. | Matched as `uncertain_section_extent`. | Open |
| F6 | The 15 landmarks are not tied to any specific road. | They can't directly label roads. | Nearby roads within 50 m are listed as candidates only. | Handled |
| F7 | 29% of OSM road features are unnamed. | Name matching misses some segments. | Use geometry and junction-based matching. | Open |

## G. Label quality and bias (limits modelling)

| ID | Issue | Effect | Action | Status |
|---|---|---|---|---|
| G1 | The data contains reports of flooding only, with no roads observed staying dry. | A supervised flooded vs not-flooded classifier isn't defensible. | Treat roads without reports as unknown. Request records that cover both flooded and dry roads (City Council, NDMA assistance logs, MNDF pump logs). | Open |
| G2 | The reports lean toward main roads: 26 of the island's 35 primary/secondary segments are linked to evidence. | A model would mostly learn "this is a main road". | Report any results with and without main roads. Use descriptive analysis first. | Open |
| G3 | There are few independent positives: 7 roads, 15 landmarks, and three roads dominate. | Any evaluation will be unstable. | Use spatial blocks and keep all segments of one road together when splitting train and test data. | Open |
| G4 | All 5 rainfall amounts come from flood days, at daily scale. | No rainfall threshold or rainfall-response analysis is possible. | Descriptive table only. Hourly MMS data is needed for more. | Open |
| G5 | `flood_reported = 0` in `male_daily_features_with_flood_labels.csv` means "no report found". | Misreading 0 as "dry" would invent negative labels. | Don't use 0 as a label without that caveat. | Open |
| G6 | ERA5 reanalysis badly underestimates the big days (per the compiler: 56 mm vs 142 mm measured on 3 Jan 2025). | Reanalysis can't stand in for gauge intensity. | Use MMS gauges for any rainfall work. | Open |

## H. Missing data sources

| ID | Gap | Source to request |
|---|---|---|
| H1 | Records covering both flooded and dry locations, with addresses | City Council, NDMA (assistance-request logs), MNDF (pump deployment logs) |
| H2 | Drainage network, pump-station and outfall locations | MWSC, Malé City Council, stormwater project custodian |
| H3 | Surveyed ground elevation (FABDEM at about 30 m is too coarse) | Survey or planning authority |
| H4 | Hourly rainfall for the dated incidents | Maldives Meteorological Service |

## I. Project-level open questions

| ID | Issue |
|---|---|
| I1 | Exact submission time. Whether references count toward the six pages. Whether 30 May 2027 is the review-only or whole-project deadline. |
| I2 | Whether the older recipe brief's components apply (clustering, classification, regression, neural-network comparison, Colab, demo). That brief also has contradictory 2025/2027 dates. |
| I3 | No written lecturer approval of the flood topic is in the folder. |
| I4 | The planning and writing files referenced in `CLAUDE.md` (`Project_Plan.md`, `latex/`, `ijcai26.docx`, reading matrix) are not in this folder. |
