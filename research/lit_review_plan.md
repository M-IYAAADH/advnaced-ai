# Literature review plan (MF-41 draft)

23 Nov 2026. This is a draft. It is final only once MF-25 and MF-33 (full-text reading) confirm that each article says what we say it does.

## Brief

- Six pages in the coursework template (`COURSEWORK  SUBMISSION TEMPLATE _RESEARCH PAPER TEMPLATE .doc`), which follows the IJCAI layout. References are not counted in the six pages.
- At least 15 journal articles. We aim for 20, so a few can be dropped after full-text reading.
- Referencing: Cite Them Right Harvard. UWE says it "must be used for all new assignments in the Harvard style". The template's sample reference, `Author, A. (1970) Title. Journal 1(1): 209-238`, uses the old punctuation, so follow CTR rather than the sample. See the citation section below.
- Due 30 May 2027 at 00:00 (UTC+5). We submit by 29 May 2027.
- Review question: which areas of Malé island proper are prone to rainfall-induced flooding, and which methods can answer that honestly from positive-only, news-derived evidence and global 30 m data?

## Template format (measured 23 Nov 2026)

These settings were read from the .doc's own page and style settings in LibreOffice, then checked against a rendered PDF.

| Item | Setting |
|---|---|
| Paper | A4 (21.0 × 29.7 cm) |
| Margins | Top 3.0 cm, bottom 4.1 cm, left 1.8 cm, right 2.0 cm |
| Columns | Title and name in one full-width column. Body in **2 columns**, each about 8.3 cm wide with a 0.6 cm gap |
| Font | Times New Roman throughout |
| Title | 20 pt, bold, centred |
| Name and student number | 12 pt, bold, centred |
| Section headings | Bold capitals with numbers ("1 INTRODUCTION"). Sections 1–3 use 11 pt (Normal plus bold); section 4 and References use the `MyH1` style (12 pt bold, 18 pt before, 6 pt after). Pick one and use it for every heading. `MyH1` is the better choice |
| Body text | 11 pt, justified, single spacing, blank line between paragraphs, no first-line indent |
| Figure caption | 10 pt, bold, centred, below the figure ("Figure Example: …") |
| References | 9 pt, justified, hanging indent of 0.4 cm (`MyRef` style) |
| Abstract, page numbers | Neither is in the template |

Pitfall: the body style `MyFirstPar` is 9 pt by default. The 11 pt in the template is applied by hand on top of it. When you type or paste new text, check that it is 11 pt. You can also set `MyFirstPar` to 11 pt once.

This template is not the official IJCAI style. Official IJCAI uses US Letter, 10 pt type and narrower margins. The template's 11 pt type and large top and bottom margins fit about **750 words per page**, against roughly 900 in real IJCAI, so the budget below assumes 750.

## Structure and page budget

The template's headings (Introduction, Background research, Experimentation, Conclusions) were written for an experiment report. For a review, we keep Introduction, Background and Conclusions and replace Experimentation with the themed review.

At about 750 words per page, six pages hold about 4,500 words. Table 1 takes about half a page and the optional figure about a third, so the text budget is about 3,900 words.

| # | Heading | Subheadings | Pages | Words |
|---|---|---|---|---|
| — | Title, name and student number, Abstract | Abstract of about 150 words | 0.2 | 150 |
| 1 | Introduction | Problem: rain flooding in Malé. Research question and scope (Malé island proper, rain versus coastal flooding). Review method: databases, search terms, inclusion criteria, number screened and number included. Paper outline | 0.6 | 450 |
| 2 | Background | 2.1 Susceptibility, hazard and risk (which one we study). 2.2 Malé and atoll flooding (Wadey, Storlazzi) | 0.5 | 350 |
| 3 | Data-driven flood susceptibility methods | 3.1 Statistical and bivariate (FR, WoE). 3.2 Machine learning (SVM, RF, GARP/QUEST). 3.3 Urban and pluvial studies. 3.4 Deep learning and why it is out of scope at our data size. **Table 1: comparison of flood studies** | 1.6 (incl. table) | 800 |
| 4 | Learning from positive-only evidence | 4.1 Presence-only and PU learning (Li, Elith, Phillips). 4.2 Reporting and sampling bias (target-group background). 4.3 Minimum sample size | 0.9 | 700 |
| 5 | Validation of spatial models | 5.1 Spatial autocorrelation and block cross-validation. 5.2 Area of applicability. 5.3 Metrics without true absences (AUC criticism, Boyce, partial ROC) | 0.9 | 700 |
| 6 | Data limits on small low-lying islands | 6.1 Global DEMs on flat islands (FABDEM). 6.2 Land cover and buildings. 6.3 Missing drainage and observed-dry data | 0.5 | 350 |
| 7 | Research gaps and proposed approach | Gaps found across sections 3–6. How the Malé study responds: 200 m grid, descriptive map first, optional exploratory ranking. Optional **Figure 1: study area and wards** | 0.6 (incl. figure) | 300 |
| 8 | Conclusions | Key findings and limits of this review | 0.2 | 120 |
| — | References | Not counted | — | — |

Rules for the writing:

- Each themed section compares studies (task, data, unit, labels, validation, limitation). Do not summarise one paper per paragraph.
- Each section ends with what the theme means for Malé.
- Use Table 1 for the comparison of flood studies. It saves about half a page of prose.
- Quote no numbers from an abstract-only reading.

## Articles mapped to sections

All 23 are journal articles. Each DOI was checked against Crossref on 23 Nov 2026: authors, title, journal, volume and pages. The ✔ column shows which ones have been read in full text. Only Ploton has been so far.

| # | Article | Journal | Section | Read in full |
|---|---|---|---|---|
| 1 | Mosavi, Ozturk and Chau (2018) Flood prediction using machine learning models: literature review | *Water* 10(11), 1536. doi:10.3390/w10111536 | 3 | |
| 2 | Tehrany, Pradhan and Jebur (2014) Flood susceptibility mapping using a novel ensemble weights-of-evidence and support vector machine models in GIS | *J. Hydrology* 512, 332–343. doi:10.1016/j.jhydrol.2014.03.008 | 3.1–3.2 | |
| 3 | Rahmati, Pourghasemi and Zeinivand (2016) Flood susceptibility mapping using frequency ratio and weights-of-evidence models in the Golastan Province, Iran | *Geocarto International* 31(1), 42–70. doi:10.1080/10106049.2015.1041559 | 3.1 | |
| 4 | Wang et al. (2015) Flood hazard risk assessment model based on random forest | *J. Hydrology* 527, 1130–1141. doi:10.1016/j.jhydrol.2015.06.008 | 3.2 | |
| 5 | Darabi et al. (2019) Urban flood risk mapping using the GARP and QUEST models | *J. Hydrology* 569, 142–154. doi:10.1016/j.jhydrol.2018.12.002 | 3.3 | |
| 6 | Seleem et al. (2022) Towards urban flood susceptibility mapping using data-driven models in Berlin | *Geomatics, Natural Hazards and Risk* 13(1), 1640–1662. doi:10.1080/19475705.2022.2097131 | 3.3, 6 | |
| 7 | Mobley et al. (2021) Quantification of continuous flood hazard using random forest classification and flood insurance claims | *NHESS* 21, 807–822. doi:10.5194/nhess-21-807-2021 | 3.3, 4.2 | |
| 8 | Bentivoglio et al. (2022) Deep learning methods for flood mapping | *HESS* 26, 4345–4378. doi:10.5194/hess-26-4345-2022 | 3.4 | |
| 9 | Li et al. (2022) A positive-unlabeled learning algorithm for urban flood susceptibility modeling | *Land* 11(11), 1971. doi:10.3390/land11111971 | 4.1 | |
| 10 | Elith et al. (2011) A statistical explanation of MaxEnt for ecologists | *Diversity and Distributions* 17(1), 43–57. doi:10.1111/j.1472-4642.2010.00725.x | 4.1 | |
| 11 | Phillips et al. (2009) Sample selection bias and presence-only distribution models | *Ecological Applications* 19(1), 181–197. doi:10.1890/07-2153.1 | 4.2 | |
| 12 | Wisz et al. (2008) Effects of sample size on the performance of species distribution models | *Diversity and Distributions* 14(5), 763–773. doi:10.1111/j.1472-4642.2008.00482.x | 4.3 | |
| 13 | van Proosdij et al. (2016) Minimum required number of specimen records | *Ecography* 39, 542–552. doi:10.1111/ecog.01509 | 4.3 | |
| 14 | Roberts et al. (2017) Cross-validation strategies for data with temporal, spatial, hierarchical or phylogenetic structure | *Ecography* 40(8), 913–929. doi:10.1111/ecog.02881 | 5.1 | |
| 15 | Ploton et al. (2020) Spatial validation reveals poor predictive performance of large-scale ecological mapping models | *Nature Communications* 11, 4540. doi:10.1038/s41467-020-18321-y | 5.1 | ✔ |
| 16 | Valavi et al. (2019) blockCV | *Methods in Ecology and Evolution* 10(2), 225–232. doi:10.1111/2041-210X.13107 | 5.1 | |
| 17 | Meyer and Pebesma (2021) Predicting into unknown space? | *Methods in Ecology and Evolution* 12(9), 1620–1633. doi:10.1111/2041-210X.13650 | 5.2 | |
| 18 | Lobo, Jiménez-Valverde and Real (2008) AUC: a misleading measure | *Global Ecology and Biogeography* 17(2), 145–151. doi:10.1111/j.1466-8238.2007.00358.x | 5.3 | |
| 19 | Hirzel et al. (2006) Evaluating the ability of habitat suitability models to predict species presences | *Ecological Modelling* 199(2), 142–152. doi:10.1016/j.ecolmodel.2006.05.017 | 5.3 | |
| 20 | Wadey et al. (2017) Coastal flooding in the Maldives: an assessment of historic events | *Natural Hazards* 89, 131–159. doi:10.1007/s11069-017-2957-5 | 2.2, 6 | |
| 21 | Storlazzi et al. (2018) Most atolls will be uninhabitable by the mid-21st century | *Science Advances* 4(4), eaap9741. doi:10.1126/sciadv.aap9741 | 2.2 | |
| 22 | Hawker et al. (2022) A 30 m global map of elevation with forests and buildings removed | *Environmental Research Letters* 17, 024016. doi:10.1088/1748-9326/ac4d4f | 6.1 | |
| 23 | Peterson, Papeş and Soberón (2008) Rethinking ROC analysis in ecological niche modeling | *Ecological Modelling* 213(1), 63–72. doi:10.1016/j.ecolmodel.2007.11.008 | 5.3 (reserve) | |

Of these, 12 are flood or island studies (1–9 and 20–22). The rest are method papers from ecology, which address our presence-only and spatial-validation problems directly. Section 4 has to explain why species-distribution methods transfer to flood reports, because a reader may otherwise question why they are cited.

Dropped from the earlier list: Budic et al. 2016 (a minor point) and Santillan 2023 (conference proceedings, not a journal article). Santillan can still be cited, but it does not count toward the 15.

Still to find: a flood study that uses spatial cross-validation, and an urban flood study that uses social-media or news reports. These would strengthen sections 4.2 and 5. Issue and page numbers for items 2, 3 and 12 come from Crossref and should be checked against the PDF.

## Citation format (Cite Them Right Harvard)

Checked on 23 Nov 2026 against the UWE pages: cite-them-right-harvard, in-text-citations (the same page) and referencing-tools.

**In text (stated by UWE):**
- One author: (Handy, 1987), or narrative: Mintzberg (1983).
- Two or three authors: name them all, joined by "and", never "&". For example (Mosavi, Ozturk and Chau, 2018).
- Four or more authors: first surname plus *et al.*, which must be in italics. For example (Seleem *et al.*, 2022), or Ploton *et al.* (2020) showed …
- Several sources: separate them with semicolons, in **chronological order, earliest first**. For example (Tehrany, Pradhan and Jebur, 2014; Wang *et al.*, 2015; Seleem *et al.*, 2022).
- Same author, same year: add 2022a and 2022b, in that order, both in the text and in the reference list.
- Quotes: give the page number, e.g. (Robinson, 2012, p. 32). Use p. for one page and pp. for a range. A page number is optional when paraphrasing. Avoid quotes in a review.
- Cite the source in full every time. Harvard does not use *ibid.*
- Secondary citing, e.g. Melack and Thompson (1971, cited in Rowley, 1991): put only the source you actually read in the reference list. UWE says to avoid secondary citing.

**Reference list:**
- UWE: list **all authors**, unless there are more than nine. Then give the first author followed by *et al.*, in italics.
- UWE: page numbers are required for journal articles.
- UWE's examples are all books. The **journal-article layout below is the usual CTR format and is not taken from UWE's pages**. Confirm it on Cite Them Right Online (citethemrightonline.com, through the UWE OpenAthens login) before the final draft. Check two things there: whether a DOI reference needs "(Accessed: date)", and how article-number journals are shown.

> Surname, Initials. (Year) 'Title of article', *Journal Title*, Volume(Issue), pp. first–last. Available at: https://doi.org/xxxx.

> Seleem, O., Ayzel, G., de Souza, A.C.T., Bronstert, A. and Heistermann, M. (2022) 'Towards urban flood susceptibility mapping using data-driven models in Berlin, Germany', *Geomatics, Natural Hazards and Risk*, 13(1), pp. 1640–1662. Available at: https://doi.org/10.1080/19475705.2022.2097131.

- Order the list alphabetically by first author's surname. Put the same author's works in chronological order.
- Article-number journals (*Nature Communications*, *Land*, *ERL*, *Science Advances*) have no page range. Show the article number, for example `11, 4540`, after confirming the form on CTR Online.
- Tools: UWE suggests Zotero or Mendeley but names no style file. It says to check every output by hand.

## Steps and sprint links

1. MF-25 and MF-33: read the 23 in full. Fill the reading matrix (task, study area, unit, labels, model, validation, limitations, use for Malé). Confirm each section mapping above.
2. MF-40: put the title, name and student number, and the headings above into the .doc template. Use the settings in the Template format section.
3. MF-41: finalise this outline after step 1.
4. MF-53: draft sections 1–3. MF-62 then drafts sections 4–7. MF-70 assembles the full draft and checks the six-page limit.

## Open questions for the lecturer

1. Confirm that Cite Them Right Harvard applies, not IJCAI's own reference style. UWE's pages make CTR the default for Harvard. Only the lecturer's email says a brief can override it.
2. Does "journal articles" include method papers from ecology, and can conference papers count toward the 15?
3. Is an Abstract expected? The template has none. Should the template's "Source code as an appendix" line be removed for a review?
