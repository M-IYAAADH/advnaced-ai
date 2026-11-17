# Road-flood data issues: Malé island proper

Logged 14 Nov 2026 from the review of `male-flood-basis/`. Full context is in `data_review.md`. Record IDs (RFxxx) refer to `derived/road_flood_inventory.csv`.

Status key: **Open** means not yet resolved. **Handled** means a workaround is already applied in the derived files; the source itself is unchanged.

## A. Source reliability

| ID | Issue | Effect | Action | Status |
|---|---|---|---|---|
| A1 | All records come from a secondary, AI-assisted compilation of news and agency reports. None of the roughly 40 linked articles has been opened or checked. | No record can be rated high confidence (60 medium, 7 low on Malé). | Top 4 landmarks checked 15 Nov 2026 (MF-12): 22 of 29 records verified from the articles (`verification/landmark_checks.csv`). 7 rely only on see.mv, which blocks automated access; open those by hand. The 17 road records remain for MF-11. | Open |
| A2 | `flood_map.html` claims "40 to 45 mm daily rain at which Malé starts to flood, per a Met Office official (Aug 2024)" with no linked source. | Risk of quoting an unverified number as a threshold. | Find the original statement or leave it out. Never use it as a trigger threshold. | Open |
| A3 | `flood_map.html` claims "16 pump stations of about 400 m³ per hour" without a source. | Unverified drainage-capacity figure. | Verify with MWSC, the council or the stormwater project documents. | Open |
| A4 | `flood_map.html` claims the NOAA GSOD rainfall "totals under half the true annual rain" and shows zero on several flood days. | If true, GSOD rainfall is unreliable for any rainfall work. | Compare GSOD annual totals with published MMS annual totals. | Open |
| A5 | The JICA 2021 survey photographs are the closest thing to a primary source, but the report has not been read. | Lost chance of higher-quality evidence. | Read the JICA report (URL in the incident file, row for 2021-12-11). | Open |

## B. Duplicates and double counting

| ID | Issue | Effect | Action | Status |
|---|---|---|---|---|
| B1 | On 20–21 Dec 2024, Majeedhee Magu appears both as the whole road and as the bounded section. The whole-road entry comes from the council repair list after the event, not from a report of flooding that day. | The source count `times_reported = 4` overstates it. It should read as 3 reported floods plus 1 designation. | Kept as `designated_flood_prone`, low confidence (RF039; the section is RF040). | Handled |
| B2 | The West Park and STO flour warehouse points are about 40 m apart and share 3 incident dates. | The same flooded spot is probably counted twice. | Checked 15 Nov 2026 (MF-12). MNDF listed them as separate sites on 10 Jan 2024, so both records stay. They share `location_group = west_park_sto` in `verification/landmark_checks.csv`; count each event once per group and keep the group in one fold. | Resolved |
| B3 | Kudakudhinge Bageecha is on Ameenee Magu, and both are reported on 3 Jan 2025. | Possibly one location counted twice. | Check in the source article. Group them for evaluation. | Open |
| B4 | Repeat counts at IGMH and West Park are partly pump-deployment reports. | Repetition may show where pumps are routinely placed, not where flooding is worst. | Checked 15 Nov 2026 (MF-12). Of 29 landmark records, 8 state flooding (incl. 1 photo caption and 2 "worst flooded area" pump sites), 13 are pumping only, 1 is a closure and 7 are unverified. Use `verified_evidence` in `verification/landmark_checks.csv` and never rank by raw count. | Handled |

## C. Contradictions

| ID | Issue | Effect | Action | Status |
|---|---|---|---|---|
| C1 | The places file says Rahdhebai Magu is "not in the base map data", but the OSM layer has *Rah Dhebai Magu* (2 segments, 548 m). | The road was left off the compiler's map. | Confirmed in MF-14 (17 Nov 2026) as OSM *Rah Dhebai Magu* (306840956, 649440524). edition.mv/.../38397 diverts traffic "from Chaandhanee Magu to Rah-dhebai Magu" around the closed Majeedhee section, and those two roads are the nearest Majeedhee crossings either side of it. *Rah Dhebai Hingun* does not reach Majeedhee. Not checked on imagery. | Handled |
| C2 | The places file gives Rahdhebai Magu the date 20–21 Dec 2024, but it is missing from that incident's location list. | The two source files disagree. | Checked in MF-14: atolltimes.mv/post/news/10872 (28 Dec 2024) lists Rahdhebai Magu among roads repaired after a survey of "the most flood-prone areas", with Chaandhanee and Majeedhee. The incident file's omission looks like a compiler error. RF041 stays a designation (no dated flood is stated) and is raised to medium confidence. see.mv/94000 returned HTTP 403. | Handled |
| C3 | Rainfall for 2–3 Jan 2025 is given as 142.2 mm and also as "162 mm by 11 pm in another count". | Two amounts for one event. | Both are kept in the notes; the inventory uses 142.2 mm with the period unknown. Resolve with MMS data. | Open |
| C4 | The compiler's Majeedhee section line (Dhanburuh to Nikagas Magu) is 83 m long, but the junctions are 44 m apart. The line runs about 38 m past the Nikagas junction. | The section extent is overstated. | The clipped 44 m extent is used in the derived files. | Handled |

## D. Missing values

| ID | Issue | Effect | Action | Status |
|---|---|---|---|---|
| D1 | Rahdhebai Magu has no coordinates. | It can only be placed by name match. | The inventory coordinate stays `unknown` (never imputed). The road is located through the confirmed OSM match in C1. | Handled |
| D2 | Road coordinates are midpoints, not flood locations. | They can't be used as flood points. | Labelled `compiler_road_midpoint_not_flood_point`. | Handled |
| D3 | Whole-road reports have no flood extent, section or junction detail. | Can't say which segments flooded. | Labelled `whole_road_named_section_unknown`. Not every segment is labelled flooded. Look for detail during source checks (A1). | Open |
| D4 | No depth is given except "passed two feet" (about 0.6 m) on Kan'baa Aisa Rani Hingun and Izzuddeen Magu, 3 Jan 2025. No durations, and mostly no times of day. | A depth or duration target isn't possible. | None for now. | Open |
| D5 | Rainfall is missing for 13 of 18 incidents. | Little rainfall context for the events. | Recorded as `unknown`. Request MMS gauge data. | Open |
| D6 | The accumulation period is unknown for 2 of the 5 incidents that have an amount (30–31 Dec 2023, 2–3 Jan 2025). For 13 Aug 2024 the 24 h window's end date isn't stated. | Amounts can't be compared fairly. | Recorded as `unknown`. Don't assume 24 h. Still unknown for 30-31 Dec 2023 and 2-3 Jan 2025; see `derived/incident_rainfall_table.md`. | Open |
| D7 | On city-wide days (13 Aug 2024 "nearly every street", 3 Jan 2025 "most of the city", 21 Oct 2026) the reports name only a few places. | Unnamed streets could be misread as dry. | Added 2 city-wide rows from the summary text. Unnamed roads are treated as unknown. | Handled |

## E. Uncertain interpretations

| ID | Issue | Effect | Action | Status |
|---|---|---|---|---|
| E1 | "Pumps ran at two sites near IGMH, West Park and near the Polytechnic" (30–31 Dec 2023) names three places but counts two sites. | Unclear which places had pumps. | Resolved 15 Nov 2026 from Atoll Times 7094: MNDF listed pump sites as two areas near IGMH, West Park area, a Main Pump Station area and near Polytechnic. All three places had pumps; only West Park also has a flooding statement (houses near it). The unlocated Main Pump Station site is not added. | Resolved |
| E2 | Rasfannu on 13 Aug 2024 "was closed". Flooding there is implied, not stated. | It might not have flooded. | Resolved 15 Nov 2026. 13 Aug 2024 (Raajje): closed "due to heavy rains and floods"; flooding at Rasfannu itself still not stated, kept low. 3 Jan 2025 (MMTV): "waterlogged pavements excavated", so standing water is stated for that date. | Resolved |
| E3 | Henveiru ward on 30–31 Dec 2023: houses flooded, with no road flooding stated. | Not road evidence. | Labelled `building_flooding_reported`. | Handled |
| E4 | Chaandhanee Magu (RF035) and Rahdhebai Magu (RF041) come only from the council's flood-prone repair list, not from a report of flooding on a given day. | These are designations, not dated reports of flooding. | Labelled `designated_flood_prone`. | Handled |
| E5 | The Boduthakurufaanu section flood on 30 Jul 2026 was attributed to drainage pumps not yet working on a newly rebuilt road. | A construction-stage cause, not typical flooding of that road. | Noted. Consider leaving it out of susceptibility analysis or flagging it. | Open |
| E6 | Landmark positions are the compiler's estimates. Rasfannu and STO are marked approximate, and Rasfannu and the Swimming Track fall just outside the OneMap polygon. | Possible position errors. | Flagged `yes_point_outside_onemap_polygon`. IGMH, the Villimalé ferry terminal, STO and West Park positions match named OSM features (within about 5 m). OSM cross-check (MF-16, `derived/landmark_position_check.csv`): 8 of the 15 Malé landmarks lie inside their named OSM footprint, so they agree with OSM (the compiler probably took them from it). Update 17 Nov 2026 (MF-16): Rasfannu (a beach, 48 m offshore) and the Swimming Track (a sea swimming track, 21 m offshore) are not road locations; they are excluded from road matching and the evidence map (`EXCLUDED_LANDMARKS` in `scripts/match_road_flood_records.py`), and their inventory records are kept. Ekuveni, Henveiru Stadium, Pizza Buona and Maldives Polytechnic were checked against the full OSM database (Nominatim): all within 0.2 to 11.4 m of the named OSM object, so confirmed with OSM; Google Maps could not be read by script, so no Google check was done. No point has been moved. Remaining: STO flour warehouse (compiler marks it approximate; no OSM reference). | Open |

## F. Matching to the OSM road layer

| ID | Issue | Effect | Action | Status |
|---|---|---|---|---|
| F1 | Majeedhee, Ameenee and Boduthakurufaanu exist in OSM only under their Dhivehi names. | English name matching alone finds nothing. | A documented Dhivehi alias table is used, cross-checked against the compiler's geometry. | Handled |
| F2 | Similar-looking OSM names belong to different streets (*Amenee Goalhi*, *Rah Dhebai Hingun*). | Risk of false matches. | Explicitly excluded. | Handled |
| F3 | The compiler's lines cover 8 unnamed OSM segments next to Majeedhee, Ameenee and Boduthakurufaanu. | They may be parts of the same roads. | Reviewed in `derived/unnamed_segment_review.csv` (MF-15). None is part of the named carriageway: 6 footways or steps, 1 short service stub, and 1 residential way (1528883097) whose 57 m beside Majeedhee duplicates the named centreline. Exclude that one from the segment table (MF-20). Decided from OSM geometry only; 1528883097 should be confirmed on imagery. | Handled |
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
| G4 | All 5 rainfall amounts come from flood days, at daily scale. | No rainfall threshold or rainfall-response analysis is possible. | Descriptive table only. Hourly MMS data is needed for more. Table built: `derived/incident_rainfall_table.md` (MF-44). | Open |
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

Resolved 14 Nov 2026 with the lecturer's answers, reported by the student (MF-10). Details in `agent.md` §3.

| ID | Issue | Status |
|---|---|---|
| I1 | Exact submission time. Whether references count toward the six pages. Whether 30 May 2027 is the review-only or whole-project deadline. | Resolved: 12:00 am Maldives time on 30 May 2027 (submit by 29 May); references don't count; the deadline covers the whole project. |
| I2 | Whether the older recipe brief's components apply (clustering, classification, regression, neural-network comparison, Colab, demo). That brief also has contradictory 2025/2027 dates. | Resolved: none apply. The 1,000–1,200-word report is replaced by the six-page review. |
| I3 | No written lecturer approval of the flood topic is in the folder. | Resolved: the lecturer approved the topic (reported by the student). |
| I4 | The planning and writing files referenced in `CLAUDE.md` (`Project_Plan.md`, `latex/`, `ijcai26.docx`, reading matrix) are not in this folder. | Resolved for the template: the coursework `.doc` is the IJCAI-format template. The planning files are still missing but not needed. |
