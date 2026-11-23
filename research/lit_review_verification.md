# Claim verification for the literature review (MF-70)

23 Nov 2026. Five Sonnet agents and the lead session checked every claim in `review/review_content.py` against the sources. They used only legitimate copies: publisher open-access pages, PubMed Central, university repositories, preprints and abstracts. Publisher sites blocked most automated access, and no paywall was bypassed.

Key to "Read": **F** = full text (or accepted manuscript or preprint); **A** = abstract only.

## Corrections made

| Source | Was | Now | Evidence |
|---|---|---|---|
| Seleem *et al.* 2022 (F, Potsdam repository) | "used 4,333 flooded locations" | 4,333 in the inventory (fire brigade, social media, customer reports). Modelled a 170 km² subset of 1,967 flooded and 1,967 non-flooded points with a random split | "4333 reported flood locations"; "1967 non-flooded locations" |
| Mobley *et al.* 2021 (F) | one-to-one random pseudo-absences; AUC 0.895 "on a random test set"; claims "record damage" | pseudo-absences drawn at random from building footprints at roughly 1:1; AUC 0.895 with test accuracy 82.2%; claims "record losses" | Results section |
| Darabi *et al.* 2019 (F, UTS accepted manuscript) | "compared" GARP and QUEST | GARP outperformed QUEST, AUC 93.5% against 89.2%, with a random 70/30 split | "randomly divided into two groups 70% … and 30%" |
| Zhang *et al.* 2025 (F, MDPI PDF) | "+24% accuracy" | 0.71 to 0.95 (24 percentage points), from changing both the sampling range and the method of choosing non-flood points | Conclusions; datasets I–IV |
| Bentivoglio *et al.* 2022 (F) | "a major challenge" | full quote: "a major challenge lies in developing deep learning models that can generalize to unseen case studies" | Abstract |
| Wang, Lyu and Zhang 2023 (A) | needs labelled units | needs a small labelled set | "labeled and unlabeled units" |
| Elith *et al.* 2011 (F) | "the most widely used presence-only method"; "cannot give calibrated probabilities" | "used extensively"; absolute probabilities are not identifiable without prevalence, but places can still be ranked | "utilized extensively"; "Prevalence cannot be exactly determined from presence-only data" |
| Al-Abadi and Pradhan 2020 (A) | a point is "defensible only at very small scales" | a flood cannot be shown as a point except at very small map scales (about 1:10,000,000) | Abstract |
| Storlazzi *et al.* 2018 (A, PMC) | aquifers only | damage to infrastructure as well as aquifers | Abstract |
| Yoo and Koo 2025 (A) | strong or moderate autocorrelation | adds that weak autocorrelation shows little bias | Abstract |
| Hirzel *et al.* 2006 (A) | presences compared with chance | based on the ratio of predicted to expected presences | Abstract |
| Section 5 | Rahmati and Mobley used random splits | Rahmati, Darabi and Seleem split randomly. Mobley's split design was not confirmed, so it is no longer named | As above |

## Added

- **Wadey *et al.* 2017 (A, UWA repository abstract).** Sea levels 1987–2015, hindcast waves 1979–2015, and the April 1987 and May 2007 events. Southern Ocean swell plus spring tides was a key cause, and wave set-up was "an essential" but poorly quantified mechanism. The full text was blocked, so check it, including whether it discusses Malé or rain flooding.
- Wisz: "No algorithm predicted consistently well with small sample size (n < 30)" (A).
- van Proosdij: 14–25 records were needed in the real African study area (A, Dryad).
- Ploton: R² 0.53 non-spatial against about 0.14 spatial (F, PMC).

## Not added

- **Fu *et al.* 2022:** only a related EGU conference abstract could be read, not the journal article. Add it after reading the paper.
- **Tehrany 2014 study details:** found only in an unofficial slide deck.

## Verified as written

| Source | Read |
|---|---|
| Rahmati 2016: random 70/30, nine factors, AUC values | A, verbatim |
| Phillips 2009 | F |
| Ploton 2020 | F |
| Hawker 2022: MAE figures, 12 countries, remaining building artefacts | F |
| Hawker 2018 | F |
| Valavi 2019: buffer, spatial and environmental blocks | F, preprint |
| Roberts 2017 | A |
| Hijmans 2012 | A |
| Lobo 2008 | A |
| Meyer and Pebesma 2021: dissimilarity index and threshold | A |
| Brown 2020 | A |
| Bersabe and Jun 2025 | A |
| Li 2022 | A |
| Songchon 2021 | A |
| Tang 2019 | A |
| Du 2016 | A |
| Mosavi 2018 | F, arXiv copy |

## Still abstract-only, so read before submission

Wadey, Brown, Bersabe, Li, Tang, Wisz, van Proosdij, Songchon, Al-Abadi, Roberts, Hijmans, Yoo, Meyer, Lobo, Hirzel and Du.

The claims taken from these are the authors' own abstract statements, so they are low risk. Reading the full papers would still let you defend them under questioning. Open-access PDFs exist for Brown (Wiley OA), Wadey (Southampton accepted manuscript), Bersabe and Li (MDPI) and Meyer (arXiv). Download them in a browser.
