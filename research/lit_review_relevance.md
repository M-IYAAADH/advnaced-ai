# Relevance skim of the 39 candidate articles (MF-19 follow-up)

23 Nov 2026. This skim is a first filter. It is not the full-text appraisal that MF-25 and MF-33 require.

## How this was checked

- **Citation details:** OpenAlex and Crossref records for every DOI. None of the 39 is retracted (OpenAlex `is_retracted = false`), and all are journal articles.
- **Content:** 34 abstracts, taken from OpenAlex, Semantic Scholar and Crossref. For 6 of those 34, the only text available was a one-sentence summary. **Full text** was read for 5 open-access PDFs: Mobley 2021, Ploton 2020, Valavi 2019 (bioRxiv preprint version), Hawker 2022 and Hawker 2018. Bentivoglio 2022 was read in part.
- **Blocked:** publisher pages (Elsevier, Wiley, Springer, T&F, MDPI, Science) refused automated access. **No text at all** could be obtained for 5 papers: Wadey 2017, Fu 2022, Huang 2025, Wang 2024 and Gallien 2014. Judge these through the UWE library before relying on them.

Key to "Read": **F** = full text, **A** = abstract, **S** = one-sentence summary only, **T** = title only.

Key to "Verdict":
- **Core:** cite it.
- **Support:** cite if space allows.
- **Reserve:** keep only as a substitute.
- **Check:** relevant by title, but must be read first.

## Years and issue numbers corrected

The rule here is our choice: cite the year of the journal volume or issue, not the online-first date, and check it against the PDF. Applying it:

| Article | Was | Now | Evidence |
|---|---|---|---|
| Brown *et al.* | 2019 | **2020**, 13(S1), e12567 | Crossref: print Jan 2020, online Oct 2019 |
| Du *et al.* | 2015 | **2016**, 9(3), 252–271 | Crossref: print Mar 2016, online Apr 2015 |
| Yoo and Koo | 2024 | **2025**, 52(5), 596–609 | Crossref: print Sep 2025, online Nov 2024 |

The plan already had these years right: Rahmati 2016 (online 2015), Elith 2011 (online 2010), van Proosdij 2016 (online 2015), Valavi 2019 (online 2018), Lobo 2008 (online 2007) and Darabi 2019 (print Feb 2019).

Issue numbers to add, from Crossref and OpenAlex:
- Tehrany 512 and Darabi 569 have no issue number.
- Wisz 14(5); van Proosdij 39(6); Roberts 40(8); Hirzel 199(2); Peterson 213(1); Lobo 17(2); Phillips 19(1); Elith 17(1); Hijmans 93(3).
- Seleem 13(1); Mobley 21(2); Bentivoglio 26(16); Li 11(11); Mosavi 10(11).
- Wadey 89(1); Storlazzi 4(4); Hawker 2022 17(2); Hawker 2018 6, article 233.
- Bersabe 14(2); Zhang 17(3); Hu 121(14); Wang 2023 38(1).
- Elsevier article-number papers (Fu, Songchon, Al-Abadi, Huang, Tang, Wang 2024) have no issue number.

Number of authors (UWE: list all authors up to nine; above nine, the first author plus *et al.*):
- Roberts *et al.* 2017 (14 authors), Ploton *et al.* 2020 (13) and Storlazzi *et al.* 2018 (11) go in the reference list as first author plus *et al.*
- All other papers list every author.

## Verdict by article

| # | Article | Read | What the text says (only what was read) | Fit for the Malé review | Verdict |
|---|---|---|---|---|---|
| 1 | Mosavi, Ozturk and Chau 2018 | A | Reviews ML flood **prediction** models, benchmarked for robustness, accuracy and speed | Mostly about forecasting, not mapping. Useful only as broad background | Reserve |
| 2 | Tehrany, Pradhan and Jebur 2014 | S | Ensemble of weights-of-evidence and SVM for flood susceptibility | Classic method paper for section 3.1–3.2. Study details not yet seen | Support |
| 3 | Rahmati, Pourghasemi and Zeinivand 2016 | A | Golestan, Iran. 144 flood locations, **random 70/30 split**, AUC of FR 76.47% and WoE 74.74% | Typical inventory-and-AUC design. A good example to critique in section 5 (random split) | Core |
| 4 | Wang *et al.* 2015 | S | Random forest "flood hazard risk assessment" | Possibly a risk-index model rather than a location-based susceptibility model. Unclear | Reserve |
| 5 | Darabi *et al.* 2019 | A | Sari city, Iran. **113 flood points from reports and field surveys**, GARP and QUEST, AUC and Kappa, hazard combined with vulnerability (FANP) | Urban, report-based labels, close to our case. Note that it maps risk, not only susceptibility | Core |
| 6 | Seleem *et al.* 2022 | A | Berlin pluvial. 4,333 flooded locations, CNN, ANN, RF and SVM at 2–30 m, **tests transfer to areas outside training**. RF best. Kappa moderate outside the training area | Urban rain flooding, plus a spatial transfer test. Bridges sections 3.3 and 5 | Core |
| 7 | Mobley *et al.* 2021 | F | Texas. NFIP **insurance claims** as presences, random pseudo-absences matched one-to-one, **random train/test split** with k-fold, AUC 0.895, 10 m grid | Reported-impact labels (section 4.2) with non-spatial validation (section 5) | Core |
| 8 | Bentivoglio *et al.* 2022 | A + part F | Reviews 58 deep-learning papers. Convolutional models usually more accurate. "A major challenge" is generalising to unseen case studies | Supports leaving deep learning out at our data size (section 3.4) | Support |
| 9 | Li *et al.* 2022 | A | Positive-unlabelled learning (PBLC) for urban flood susceptibility. Non-flood areas may be "contaminated" by unrecorded floods | Directly matches our positive-only problem | Core |
| 10 | Elith *et al.* 2011 | A | Explains MaxEnt for presence-only data, including sample bias and unknown prevalence | Theory for section 4.1 | Core |
| 11 | Phillips *et al.* 2009 | A | Biased presence data. A **target-group background** with the same bias improves models (226 species) | Our reporting-bias argument (section 4.2) | Core |
| 12 | Wisz *et al.* 2008 | A | 12 algorithms at 100, 30 and 10 records. Accuracy falls as sample size shrinks. MaxEnt among the least sensitive | Our small sample (section 4.3) | Core |
| 13 | van Proosdij *et al.* 2016 | A | Minimum record numbers depend on prevalence. AUC on presence-only data depends on prevalence | Section 4.3 and the metric argument in section 5.3 | Core |
| 14 | Roberts *et al.* 2017 | A | Random CV seriously underestimates error on structured data. Blocking can also force extrapolation | Basis of section 5.1 | Core |
| 15 | Ploton *et al.* 2020 | F | Non-spatial CV R² ≈ 0.5, while buffered spatial CV shows "quasi-null" predictive power | Strongest evidence for spatial validation | Core |
| 16 | Valavi *et al.* 2019 | F (preprint) | Software (blockCV) for buffer, spatial and environmental blocks. Says the best strategy depends on purpose | A tool paper. Cite only if we use block CV | Support |
| 17 | Meyer and Pebesma 2021 | A | Area of applicability: a dissimilarity index in predictor space | Section 5.2. Malé cells may fall outside the training range | Support |
| 18 | Lobo, Jiménez-Valverde and Real 2008 | A | Five reasons not to use AUC, including dependence on study extent | Section 5.3 | Core |
| 19 | Hirzel *et al.* 2006 | S | Proposes the continuous Boyce index for presence-only evaluation | Our proposed metric (section 5.3) | Core |
| 20 | Wadey *et al.* 2017 | T | No text obtained | Probably the main Maldives flood-history source (coastal). **Must read** | Check |
| 21 | Storlazzi *et al.* 2018 | A | Wave-driven overwash will make most atolls uninhabitable by mid-century. About coastal and freshwater impacts | Background only (section 2.2). Wave flooding, not rain | Support |
| 22 | Hawker *et al.* 2022 | F | FABDEM: mean absolute error in built-up areas cut from 1.61 to 1.12 m. Trained on reference data from 12 countries. Some building artefacts remain | Our DEM caveat (section 6.1). A 1.1 m error is large on a low, flat island | Core |
| 23 | Peterson, Papeş and Soberón 2008 | S | AUC undervalues models that do not predict across the whole area range. Proposes partial ROC | Section 5.3 | Reserve |
| 24 | Fu *et al.* 2022 | T | No text obtained | Flood locations taken from news by NER, the closest analogue to our evidence. **Must read** | Check |
| 25 | Songchon, Wright and Beevers 2021 | S | Assessing the quality of crowdsourced social-media data lets its uncertainty be estimated | Section 4.2, on the quality of reported data | Support |
| 26 | Al-Abadi and Pradhan 2020 | A | **Discussion article**: argues floods are areal and should not be stored as points except at very small map scales | Supports our record-scope rules (section 4.2 or 6.3). It is a discussion piece, so weight it lightly | Support |
| 27 | Huang *et al.* 2025 | T | No text obtained | Non-flood sampling in urban models. **Must read** | Check |
| 28 | Zhang *et al.* 2025 | A | Zijiang **River Basin**. Non-flood samples from FR plus one-class SVM, accuracy +24%, AUC 0.95 | A river basin, not urban. Supporting point on non-flood choice | Reserve |
| 29 | Hu, Pang and Deng 2025 | S | MaxEnt plus cloud model for urban flood risk | Presence-only urban flood model. Details unknown | Check |
| 30 | Tang *et al.* 2019 | A | Guangzhou urban waterlogging. PSO-SVM. Repeated random sampling to choose negative samples | Urban rain flooding plus the negative-sample problem (section 4.1) | Core |
| 31 | Wang, Lyu and Zhang 2023 | A | Dalian. Semi-supervised graph attention network. 4 basic factors, under 1.2% of units labelled | A data-scarce urban case, but a deep model. Section 3.4 or 6 | Support |
| 32 | Wang, Lyu and Zhang 2024 | T | No text obtained | Explainable urban pluvial ML | Check |
| 33 | Bersabe and Jun 2025 | A | Seoul. Flood points 2010–2022. LR, RF and SVM. Adding **drainage variables** (sewer density, distance to drain) raised AUC by 3.8% | Shows what our missing drainage data costs (section 6.3) | Core |
| 34 | Hijmans 2012 | A | Spatial sorting bias inflates AUC. A distance-only null model beat MaxEnt for 45% of species | Section 5.1 and 5.3 | Core |
| 35 | Yoo and Koo 2025 | A | Strong autocorrelation gives optimistic random CV. Spatial CV fixes it but can be too pessimistic | Gives the balanced view for section 5.1 | Support |
| 36 | Hawker *et al.* 2018 | F | Open global DEMs have large vertical errors. Proposes stochastic DEM ensembles | Section 6.1 | Support |
| 37 | Du *et al.* 2016 | A | SRTM and ASTER accuracy over low coastal plains, checked with ICESat and RTK GPS | Older DEMs, not FABDEM | Reserve |
| 38 | Brown *et al.* 2020 | A | Hulhumalé. Overtopping likely at 0.6 ± 0.2 m sea-level rise. Maldives land about 1 m above mean sea level | Maldives context, but Hulhumalé and coastal. Not our study area | Support |
| 39 | Gallien, Sanders and Flick 2014 | T | No text obtained | Coastal versus drainage flooding | Check |

## Totals

- **Core: 20.** Rahmati, Darabi, Seleem, Mobley, Li, Elith, Phillips, Wisz, van Proosdij, Roberts, Ploton, Lobo, Hirzel, Hawker 2022, Tang, Bersabe, Hijmans, plus Wadey, Fu and Huang if reading confirms them. That clears the 15-article minimum, with flood studies in the majority.
- **Gap the skim showed:** apart from Seleem's transfer test, none of the flood studies skimmed reports a spatial validation. Rahmati and Mobley used random splits, and Darabi's split is not stated in the abstract. This is a finding to state in section 5, not a reason to keep searching.
- **Still no rain-flood study of Malé** in any source found.

## Next action

Get the 5 title-only papers (Wadey, Fu, Huang, Wang 2024, Gallien), plus the abstract-only Core papers, through the UWE library. Then do the MF-25 and MF-33 reading-matrix appraisal.
