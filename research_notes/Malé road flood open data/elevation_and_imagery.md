# High-resolution elevation, survey and aerial imagery for Malé island proper (as of 15 Nov 2026)

Scope: Malé island proper only. Hulhumalé, Villimalé and other Greater Malé islands appear only as context. "Verified" means I opened the link or service endpoint in this session. "Mentioned" means a source refers to the data, but I found no public file.

Bottom line: **I found no verified public elevation, survey or imagery source for Malé island proper that is finer than 30 m.** Every sub-30 m public dataset I verified covers Hulhumalé or other reclaimed islands, not Malé.

## Q1. Is the LAMER Group 2022 topographic survey, or "Third Additional information ... stormwater drainage system development project at Male' City" (LAMER, 2023), published online?

### Takeaway
I could not find it online. The EIA library has moved: `files.epa.gov.mv/file/<n>` URLs now return 301 redirects to `era.gov.mv/file/<n>`, and those return 404. The new ERA reports page loads its list from `/api/reports`, which also returned 404. That makes the EIA library unsearchable from here. I found no original EIA, addendum or survey figure for the Malé stormwater project.

### Cited Findings
- A search for the title on epa.gov.mv and the web found no LAMER stormwater EIA for Malé. It found an unrelated 2017 LAMER EIA, "relocation of sewer outfalls at IGMH and West park area, Male' city", in the Maldives National University repository. — [Saruna MNU item](https://saruna.mnu.edu.mv/items/1717d19a-eb70-445c-9945-bba648f17965/full)
- `https://files.epa.gov.mv/file/2007` is a LAMER report for Malé Water and Sewerage Company, according to a search snippet. It now returns a 301 to `https://era.gov.mv/file/2007`, which returns 404 (checked 15 Nov 2026). — [files.epa.gov.mv/file/2007](https://files.epa.gov.mv/file/2007)
- The EPA site has been rebranded as ERA. `https://www.era.gov.mv/reports.html` is a JavaScript shell that fetches `/api/reports`, and that endpoint returned 404 (checked 15 Nov 2026). — [ERA reports page](https://www.era.gov.mv/reports.html)
- MNU's Saruna repository holds Maldivian EIAs, including LAMER EIAs. It is the most likely place for a mirrored copy, but my searches did not surface the stormwater EIA there. — [Saruna MNU](https://saruna.mnu.edu.mv/items/1717d19a-eb70-445c-9945-bba648f17965/full)
- Context: Malé got temporary drainage systems at three sites in October 2024, overseen by the Ministry of Construction and Infrastructure, and a permanent fix was expected with Chinese government assistance. — [PSM/MV+ news](https://plus.mv/?p=104664)

### Inferences
- If the LAMER EIA and its "Third Additional Information" addendum were ever posted, they were probably on the old EPA file server. Those links are currently broken. The document could still exist offline or in ERA's internal archive.
- Maldivian EIAs often include survey drawings and spot heights as appendices. Without the document, I cannot confirm that this one has elevation maps, survey points or DEM figures.

### Gaps
- I did not verify the existence, URL, date or contents of the LAMER 2022 survey or the 2023 "Third Additional information" report. Recommended next steps: ask ERA (era.gov.mv / one.gov.mv/entities/ERA) for the file; search Saruna MNU directly; ask the Ministry of Construction and Infrastructure or the project custodian (see CLAUDE.md §5).

## Q2. Is there a public Royal HaskoningDHV (RHDHV) drainage or flood study of Malé, linked to the "DEM_interpolateRHDHV" figure?

### Takeaway
I found no public RHDHV study, DEM or report for Malé. RHDHV's public Maldives work is coastal protection, such as the Fuvahmulah revetment. The "DEM_interpolateRHDHV" label does not appear in any indexed web page, and no file in this project folder mentions RHDHV, Haskoning or LAMER.

### Cited Findings
- RHDHV's public Maldives project pages cover coastal protection, such as impact assessment, numerical modelling and design of a 2.6 km revetment on Fuvahmulah. They do not cover Malé urban drainage. — [Dutch Water Sector](https://www.dutchwatersector.com/news/maldives-ready-to-start-coastal-protection-project-for-fuvahmulah-city); [RHDHV coastal solutions](https://coastalsolutions.ireport.royalhaskoningdhv.com/infraD001)
- A web search for "DEM_interpolateRHDHV" or "RHDHV" together with Malé City Council returned only flood news. Examples are Council sandbag and drain-cleaning notices and road repairs on frequently flooded roads, with no technical study. — [Malé City Council news 477](https://malecity.gov.mv/en/news/477); [Atoll Times 10838](https://atolltimes.mv/post/news/10838)

### Inferences
- The name suggests an interpolated DEM made by or for RHDHV, possibly within the World Bank-funded stormwater master plan work (see Q3). This is an unconfirmed guess.

### Gaps
- I could not identify the Council report that contains the figure, so I could not trace the RHDHV deliverable. The student should record the report's title, date and URL so the figure's source can be followed up.

## Q3. LiDAR, UAV, photogrammetry or high-resolution DEM of Malé from open platforms, national agencies or academic work

### Takeaway
None of these open sources covers Malé island proper at better than 30 m. Hulhumalé, next door, has public web services from the Housing Development Corporation (HDC): a 0.3 m DSM, a ~10.8 m elevation surface, a point cloud and orthomosaics from 2024 to 2026. These are useful as methodological context, not Malé data. A Malé DEM was planned under the World Bank project, but the 2023 DEM/masterplan EOI was cancelled. Its terms of reference set out the need but provide no data.

### Cited Findings: verified services and catalogues
- **HDC ArcGIS Server, `https://gis.hdc.mv/server/rest/services`** (verified 15 Nov 2026). It publishes `HML_ELEVATION` (ImageServer, pixel ~10.84 m, values 0–1.94, EPSG:3857, no description or vertical datum stated) and `Hulhumale_25_dsm` (ImageServer, pixel 0.30 m, values −25.97 to 78.16, which suggests a DSM including buildings, no datum stated). The `Hosted` folder adds `Hulhumale_25_DSM_Cleaned`, `Hulhumale_Phase1_Point_Cloud` (SceneServer), `Kudagiri_Jan_2024_dsm` and dated orthomosaics, for example `IMAGERY_HMLJUN2024` to `IMAGERY_HMLJUNE2026`, plus RasMalé, Gulhifalhu, Thilafushi and Kudagiri imagery. I converted the service extents to WGS84. `HML_ELEVATION` spans about 73.532–73.552 E, 4.199–4.242 N, and the "Survey_Day" orthomosaics span 73.539–73.542 E, 4.215–4.218 N. **Both are Hulhumalé, not Malé** (Malé is roughly 73.50–73.52 E, 4.17–4.18 N). No service name or extent in any folder refers to Malé island proper. No licence or copyright text is declared (`copyrightText` is empty), and export rights are unclear. — [HDC GIS services root](https://gis.hdc.mv/server/rest/services?f=json); [HML_ELEVATION](https://gis.hdc.mv/server/rest/services/HML_ELEVATION/ImageServer?f=json); [Hulhumale_25_dsm](https://gis.hdc.mv/server/rest/services/Hulhumale_25_dsm/ImageServer?f=json); [Hosted folder](https://gis.hdc.mv/server/rest/services/Hosted?f=json)
- **OpenAerialMap**: the API query for bbox 73.495–73.525 E, 4.165–4.185 N returned `found: 0`, so there is no open imagery over Malé (checked 15 Nov 2026). — [OAM API query](https://api.openaerialmap.org/meta?bbox=73.495,4.165,73.525,4.185&limit=50)
- **OpenTopography**: the catalogue API for the Malé bbox, with federated sources included, returned `Datasets: []` (checked 15 Nov 2026). — [OpenTopography otCatalog query](https://portal.opentopography.org/API/otCatalog?productFormat=PointCloud&minx=73.49&miny=4.16&maxx=73.53&maxy=4.19&detail=false&outputFormat=json&include_federated=true)
- **Maxar Open Data**: the STAC event catalogue lists no Maldives event (checked 15 Nov 2026; nearest is "Cyclone-Ditwah-Sri-Lanka-Nov-2025"). — [Maxar Open Data catalog.json](https://maxar-opendata.s3.amazonaws.com/events/catalog.json)

### Cited Findings: mentioned only (no public file found)
- **World Bank Maldives Urban Development and Resilience Project (P163957)**: results indicators include a stormwater management master plan for Malé and Hulhumalé (target date 31 Dec 2023) and a reduction in the area of Malé flooded by a 1-in-5-year event. No DEM or survey dataset is attached. — [World Bank project page P163957](https://projects.worldbank.org/en/projects-operations/project-detail/P163957); [PID/ISDS](https://documents1.worldbank.org/curated/en/914371576902602402/pdf/Project-Information-Document-Integrated-Safeguards-Data-Sheet-Maldives-Urban-Development-and-Resilience-Project-P163957.pdf)
- **Ministry of Finance / Gazette procurement notices**: the consultancy scope covers stormwater masterplans for Malé and Hulhumalé and a **Digital Elevation Model for Malé City**, with shortlisting requiring at least 5 years of DEM experience and a 9-month completion period. A 2024 notice appears to cancel the EOI. This matches CLAUDE.md: EOI `MV-MONPI-326937-CS-QCBS` was cancelled on 12 Aug 2024. — [Gazette notice 228446](https://gazette.gov.mv/iulaan/228446); [Gazette TOR PDF 59523](https://storage.googleapis.com/gazette.gov.mv/docs/iulaan/59523.pdf) (downloaded but not text-extractable here; contents not verified)
- **National aerial survey (~2008, Government of India-assisted)**: aerial photogrammetry and DEMs for the Maldives, using 13 GPS reference stations and 41 ground control points in WGS84. I found no public download, and resolution and accuracy for Malé were not stated in the source. — [GIM International "Mapping the Maldives"](https://www.gim-international.com/content/article/mapping-the-maldives); [GIM "Aerial Survey of the Maldives"](https://www.gim-international.com/content/article/aerial-survey-of-the-maldives)
- **Maldives Land and Survey Authority (MLSA)**: base-map shapefiles are public through onemap.mv. I found no public imagery, contour or spot-height layer for Malé. Survey-tender documents require MLSA approval of topographic surveys, but these surveys are not published. — [PSM news 104759](https://psmnews.mv/en/104759); [OneMap](https://onemap.mv/)
- **Maldives Heritage Survey / OpenHeritage3D**: LiDAR and photogrammetry of heritage sites in Kaafu Atoll. These are site and building scale scans, not street terrain, and their coverage of Malé roads is unconfirmed. — [OpenHeritage3D project](https://openheritage3d.org/project/7tbq-c529)
- **WeRobotics 2016 scoping mission**: reported that drones had not yet been used systematically to make high-resolution elevation models for planning in the Maldives. — [WeRobotics blog](https://werobotics.org/blog/werobotics-scoping-mission-maldives)

### Cited Findings: academic studies (context)
- Brown et al. (2020), *Journal of Flood Risk Management*, built a **10 m DEM of Hulhumalé** from 8,706 survey points along roads and coastal defences (natural-neighbour interpolation, buildings excluded) and ran LISFLOOD-FP. This is Hulhumalé, not Malé, but the same approach could work for Malé if road spot heights were obtained. — [Wiley DOI 10.1111/jfr3.12567](https://onlinelibrary.wiley.com/doi/10.1111/jfr3.12567)
- Open UAV DEMs exist for Fuvahmulah (2017, 2019), but not for Malé. — [Zenodo 4304049](https://zenodo.org/record/4304049)
- A 2025 Huvadhoo flood-modelling paper notes the lack of a complete island DEM, which reflects how scarce island DEMs are across the Maldives. — [PMC12645334](https://pmc.ncbi.nlm.nih.gov/articles/PMC12645334/)

### Inferences
- Global satellite DEMs (Copernicus GLO-30, FABDEM, AW3D30, NASADEM) are 30 m or coarser, so they fall outside this brief. FABDEM is already in the project. TanDEM-X 12 m is distributed by DLR under restricted science-proposal access. I did not verify its terms in this session.
- Commercial very-high-resolution imagery (e.g., Maxar or Airbus via Google/Bing basemaps) is visible but cannot be downloaded for analysis without a licence.
- HDC's Hulhumalé 0.3 m DSM shows that high-resolution elevation products exist for nearby land under government corporations. A similar Malé survey would most likely sit with the Ministry or Malé City Council, not on a public portal.

### Gaps
- I could not open the Gazette TOR PDF text (no PDF text extractor was available), so I cannot quote its stated DEM resolution, accuracy or datum requirements.
- I did not verify TanDEM-X 12 m or ALOS AW3D commercial (2.5/5 m) access terms for Malé.
- HDC services declare no vertical datum, so the 0–1.94 values in `HML_ELEVATION` cannot be interpreted.

## Q4. Published spot heights or road levels for Malé streets

### Takeaway
I found no public spot-height, road-level or contour dataset for Malé island proper. The only road-level survey dataset in the region is the Hulhumalé survey used by Brown et al. (2020), and it was not published as open data in the sources I saw.

### Cited Findings
- Brown et al. (2020) used 8,706 survey points along Hulhumalé roads and defences. That shows such data exists for Hulhumalé, but the paper does not link a public dataset. — [Wiley DOI 10.1111/jfr3.12567](https://onlinelibrary.wiley.com/doi/10.1111/jfr3.12567)
- One non-peer-reviewed web story map puts Malé's highest point at about 2.3 m above sea level. It gives no datum or source, so it is indicative only and not a usable road-level source. — [ArcGIS StoryMap "Drowning Paradise"](https://storymaps.arcgis.com/stories/61711156415b4bbebfdb835e5c0a60b3)

### Inferences
- Road-level susceptibility mapping on Malé currently has no open terrain input finer than FABDEM 30 m. Getting road spot heights or the stormwater-design survey from the Ministry or the drainage-project custodian (CLAUDE.md §5, priority 3) is the main route to usable elevation data.

### Gaps
- I found no evidence that the LAMER 2022 topographic survey points, road crown levels, drain invert levels or the Council's RHDHV-labelled DEM are public.
- Not checked: the Malé City Council website document library in full, and Ministry of Construction and Infrastructure tender attachments after 2024.
