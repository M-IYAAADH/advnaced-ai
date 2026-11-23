# Literature review plan (MF-41 draft)

23 Nov 2026. This is a draft. It is final only once MF-25 and MF-33 (full-text reading) confirm that each article says what we say it does.

## Brief

- Six pages in the coursework template (`COURSEWORK  SUBMISSION TEMPLATE _RESEARCH PAPER TEMPLATE .doc`), which follows the IJCAI layout. References are not counted in the six pages.
- At least 15 journal articles. We aim for 20, so a few can be dropped after full-text reading.
- Referencing: Cite Them Right Harvard (UWE's standard from Sept 2026). The template's own example, `Author, A. (1970) Title. Journal 1(1): 209-238`, is already author-date, so the two do not conflict. The lecturer still needs to confirm this (see Open questions).
- Due 30 May 2027 at 00:00 (UTC+5). We submit by 29 May 2027.
- Review question: which areas of Malé island proper are prone to rainfall-induced flooding, and which methods can answer that honestly from positive-only, news-derived evidence and global 30 m data?

## Structure and page budget

The template's headings (Introduction, Background research, Experimentation, Conclusions) were written for an experiment report. For a review, we keep Introduction, Background and Conclusions and replace Experimentation with the themed review.

A page in the IJCAI two-column layout holds about 900 words of text. The budget below is about 4,600 words plus one table and one figure.

| # | Heading | Subheadings | Pages | Words |
|---|---|---|---|---|
| — | Title, name and student number, Abstract | Abstract of about 150 words | 0.3 | 150 |
| 1 | Introduction | Problem: rain flooding in Malé. Research question and scope (Malé island proper, rain versus coastal flooding). Review method: databases, search terms, inclusion criteria, number screened and number included. Paper outline | 0.7 | 600 |
| 2 | Background | 2.1 Susceptibility, hazard and risk (which one we study). 2.2 Malé and atoll flooding (Wadey, Storlazzi) | 0.5 | 450 |
| 3 | Data-driven flood susceptibility methods | 3.1 Statistical and bivariate (FR, WoE). 3.2 Machine learning (SVM, RF, GARP/QUEST). 3.3 Urban and pluvial studies. 3.4 Deep learning and why it is out of scope at our data size. **Table 1: comparison of flood studies** | 1.4 | 1,100 |
| 4 | Learning from positive-only evidence | 4.1 Presence-only and PU learning (Li, Elith, Phillips). 4.2 Reporting and sampling bias (target-group background). 4.3 Minimum sample size | 1.0 | 900 |
| 5 | Validation of spatial models | 5.1 Spatial autocorrelation and block cross-validation. 5.2 Area of applicability. 5.3 Metrics without true absences (AUC criticism, Boyce, partial ROC) | 1.0 | 900 |
| 6 | Data limits on small low-lying islands | 6.1 Global DEMs on flat islands (FABDEM). 6.2 Land cover and buildings. 6.3 Missing drainage and observed-dry data | 0.6 | 500 |
| 7 | Research gaps and proposed approach | Gaps found across sections 3–6. How the Malé study responds: 200 m grid, descriptive map first, optional exploratory ranking. Optional **Figure 1: study area and wards** | 0.4 | 400 |
| 8 | Conclusions | Key findings and limits of this review | 0.2 | 150 |
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

In text:
- One author: (Surname, 2022). Two or three authors: (Mosavi, Ozturk and Chau, 2018). Four or more authors: (Seleem *et al.*, 2022).
- Narrative: Ploton *et al.* (2020) showed that …
- Several sources: (Tehrany, Pradhan and Jebur, 2014; Wang *et al.*, 2015). Use one order throughout, chronological or alphabetical.
- Direct quotes need a page number: (Lobo, Jiménez-Valverde and Real, 2008, p. 146). Avoid quotes in a review.

Reference list (alphabetical, not counted in the six pages):

> Surname, Initials. (Year) 'Title of article', *Journal Title*, Volume(Issue), pp. first–last. Available at: https://doi.org/xxxx.

Example:

> Seleem, O., Ayzel, G., de Souza, A.C.T., Bronstert, A. and Heistermann, M. (2022) 'Towards urban flood susceptibility mapping using data-driven models in Berlin, Germany', *Geomatics, Natural Hazards and Risk*, 13(1), pp. 1640–1662. Available at: https://doi.org/10.1080/19475705.2022.2097131.

- List up to the number of authors the UWE CTR page shows. Check whether it asks for all authors in the reference list.
- Article-number journals (*Nature Communications*, *Land*, *ERL*, *Science Advances*) use the article number in place of pages, e.g. `11, 4540`.
- If you use Zotero or Mendeley with the "Cite Them Right 12th edition – Harvard" style, check every entry by hand, as UWE advises.

## Steps and sprint links

1. MF-25 and MF-33: read the 23 in full. Fill the reading matrix (task, study area, unit, labels, model, validation, limitations, use for Malé). Confirm each section mapping above.
2. MF-40: put the title, name and student number, and the headings above into the .doc template. Check the column, font and margin settings.
3. MF-41: finalise this outline after step 1.
4. MF-53: draft sections 1–3. MF-62 then drafts sections 4–7. MF-70 assembles the full draft and checks the six-page limit.

## Open questions for the lecturer

1. Does Cite Them Right Harvard apply, or IJCAI's own reference style? The UWE notice says to follow the style in the brief when it names one.
2. Does "journal articles" include method papers from ecology, and can conference papers count toward the 15?
3. Is an Abstract expected? The template has none.
