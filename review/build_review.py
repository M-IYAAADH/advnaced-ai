import sys,json,copy
sys.path.insert(0,'pylib')
import docx
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
# Usage: python3 build_review.py <template.docx from soffice --convert-to docx> <out.docx> refs.json  (needs python-docx)
SRC,OUT,REFS=sys.argv[1],sys.argv[2],sys.argv[3]
d=docx.Document(SRC)
st=d.styles
st['MyFirstPar'].font.size=Pt(11)   # template's 11 pt was manual; make the style itself 11 pt
st['MyRef'].font.size=Pt(9)
st['MyRef'].paragraph_format.alignment=WD_ALIGN_PARAGRAPH.LEFT  # justified URLs leave wide gaps
body=d.element.body
paras=d.paragraphs
paras[0].runs[0].text='Geospatial-Based Flood Risk Modelling and Predictive Analysis Using Artificial Intelligence: A Review for Malé, Maldives'
for r in paras[0].runs[1:]: r.text=''
paras[2].runs[0].text='[Name] & [student no.]'
for r in paras[2].runs[1:]: r.text=''
for p in paras[4:]: body.remove(p._p)   # final body sectPr (2 columns) stays
def H(t): d.add_paragraph(t,style='MyH1')
def SH(t):
    p=d.add_paragraph(style='MyFirstPar'); r=p.add_run(t); r.bold=True
def N(t):
    p=d.add_paragraph(style='MyFirstPar'); r=p.add_run(t); r.italic=True
N0='[Writing notes, delete before submission. (F) = checked in full text, (A) = abstract only, (T) = not yet read. Confirm every (A)/(T) point in the full text before writing it as a finding.]'
H('ABSTRACT'); N(N0); N('About 150 words, written last. Problem, question, the four themes, main gaps, what the Malé study will do.')
H('1 INTRODUCTION')
N('~450 words. Rain flooding in Malé island proper. Research question: which areas of Malé island proper are prone to rainfall-induced flooding? This is area susceptibility mapping, not forecasting when the next flood will happen.')
N('Scope: Malé island proper only (not Hulhumalé or Vilimalé). Rain flooding is the focus. Coastal and wave flooding is treated as a separate process.')
N('Review method: databases searched (e.g. Scopus, Web of Science, Google Scholar, UWE Library), search terms, inclusion criteria (journal articles; flood susceptibility, presence-only data, spatial validation, island data), number screened and number included. State the numbers honestly.')
N('Last paragraph: outline of sections 2 to 8.')
H('2 BACKGROUND')
SH('2.1 Susceptibility, hazard and risk')
N('Define each term. Susceptibility is where flooding is likely to occur. Hazard adds magnitude or probability. Risk adds exposure and vulnerability. Darabi et al. (2019) combine hazard and vulnerability into a risk map (A). Our study maps susceptibility only.')
SH('2.2 Flooding on atolls and in the Maldives')
N('Storlazzi et al. (2018): wave-driven overwash is projected to make most atoll islands uninhabitable by the mid-21st century (A). This is coastal flooding, not rain flooding.')
N('Brown et al. (2020): Maldives land is about 1 m above mean sea level. On Hulhumalé, overtopping is likely at 0.6 ± 0.2 m of sea-level rise (A). It is context only, because Hulhumalé is not our study area.')
N('Wadey et al. (2017): history of coastal flood events in the Maldives (T). Read it before using it.')
N('Point to make: the published Maldives work is coastal. No peer-reviewed study of rain flooding in Malé was found. That is the gap this review frames.')
H('3 DATA-DRIVEN FLOOD SUSCEPTIBILITY METHODS')
SH('3.1 Statistical methods')
N('Rahmati, Pourghasemi and Zeinivand (2016): frequency ratio and weights-of-evidence, 144 flood locations, a random 70/30 split, AUC of about 75% (A). Tehrany, Pradhan and Jebur (2014): an ensemble of weights-of-evidence and SVM (A). Compare: inputs are mostly river and terrain factors (slope, TWI, distance to river). These mean little on a flat, fully built atoll island.')
SH('3.2 Urban and pluvial machine learning')
N('Compare in Table 1 (study, area, flood type, label source and count, unit, model, validation, limitation):')
N('Darabi et al. (2019): Sari, 113 flood points from reports and field surveys, GARP and QUEST (A). Tang et al. (2019): Guangzhou waterlogging, PSO-SVM, repeated random choice of negative samples (A). Seleem et al. (2022): Berlin, 4,333 flooded locations, RF best, moderate Kappa outside the training area (A). Mobley et al. (2021): Texas insurance claims, random pseudo-absences, random train/test split, AUC 0.895 (F). Bersabe and Jun (2025): Seoul, adding drainage variables raised AUC by 3.8% (A).')
N('Point to make: most studies report a high AUC from random splits and need many flood points plus drainage or terrain data. Malé has few independent reports and no open drainage data.')
SH('3.3 Deep learning')
N('Bentivoglio et al. (2022) reviewed 58 studies. Convolutional models are usually more accurate, but "a major challenge" is generalising to unseen case studies (A). Wang, Lyu and Zhang (2023) used a semi-supervised graph network with under 1.2% of units labelled (A). Conclude that deep models do not suit a dataset of our size.')
N('[Table 1 here: about half a page.]')
H('4 LEARNING FROM POSITIVE-ONLY EVIDENCE')
SH('4.1 Presence-only and positive-unlabelled learning')
N('Explain why species-distribution methods transfer: flood reports, like species records, are presences with no confirmed absences. Elith et al. (2011): MaxEnt and the problems of sample bias and unknown prevalence (A). Li et al. (2022): positive-unlabelled learning for urban floods, because "non-flood" samples may contain unrecorded floods (A). Huang et al. (2025) on non-flood sampling (T).')
SH('4.2 Reporting bias')
N('Phillips et al. (2009): a background drawn with the same bias as the presences (target group) improved models across 226 species (A). Link this to Malé: news reports and pump sites cluster on main roads. Fu et al. (2022) take flood locations from news text (T). Songchon, Wright and Beevers (2021) assess crowdsourced data quality (A). Al-Abadi and Pradhan (2020), a discussion article: floods are areas, not points (A). This supports keeping each record at its real scope.')
SH('4.3 Sample size')
N('Wisz et al. (2008): 10, 30 and 100 records. Accuracy falls with fewer records, and MaxEnt is among the least sensitive (A). van Proosdij et al. (2016): the minimum number of records depends on prevalence (A). Give the exact minimum numbers only after reading the full text.')
H('5 VALIDATION OF SPATIAL MODELS')
SH('5.1 Spatial autocorrelation and block cross-validation')
N('Roberts et al. (2017): random CV seriously underestimates error on structured data. Blocking can force extrapolation (A). Ploton et al. (2020): non-spatial CV gives R² of about 0.5, while buffered spatial CV shows "quasi-null" predictive power (F). Hijmans (2012): spatial sorting bias inflates AUC. A distance-only null model beat MaxEnt for 45% of species (A). Yoo and Koo (2025): spatial CV can also be too pessimistic (A). Valavi et al. (2019): blockCV tool (F, preprint).')
N('Point to make: of the flood studies in section 3, only Seleem et al. (2022) test a model outside the training area.')
SH('5.2 Area of applicability')
N('Meyer and Pebesma (2021): predictions are reliable only where predictors resemble the training data (A).')
SH('5.3 Metrics without true absences')
N('Lobo, Jiménez-Valverde and Real (2008): five reasons not to use AUC (A). Hirzel et al. (2006): the continuous Boyce index for presence-only data (A). AUC on presence-only data depends on prevalence (van Proosdij et al., 2016) (A).')
H('6 DATA LIMITS ON SMALL LOW-LYING ISLANDS')
SH('6.1 Elevation data')
N('Hawker et al. (2022): FABDEM cuts mean absolute vertical error in built-up areas from 1.61 m to 1.12 m. Some building artefacts remain (F). Hawker et al. (2018): open global DEMs have large vertical errors; stochastic DEM ensembles (F). Point to make: a 1 m error is a large share of the height range of an island about 1 m above sea level. Use the DEM as a relative rank only.')
SH('6.2 Land cover, buildings and drainage')
N('Note the missing drainage and observed-dry data, and contrast with Bersabe and Jun (2025), where drainage variables improved the model (A). Built-up land cover is close to 100% on Malé, so it barely varies between areas. These are project observations: present them as ours, not as literature.')
H('7 RESEARCH GAPS AND PROPOSED APPROACH')
N('~300 words. Gaps: (1) no rain-flood study of Malé; (2) flood studies seldom use spatial validation; (3) little guidance for very small presence-only samples in cities; (4) global DEMs are weak on atolls. Response: a 200 m grid, a descriptive evidence map first, and an optional exploratory ranking evaluated by spatial blocks with presence-only metrics. [Optional Figure 1: study area and wards.]')
H('8 CONCLUSIONS')
N('~120 words. Main findings and the limits of this review (search scope; some sources read as abstracts).')
H('REFERENCES')
refs=json.load(open(REFS))
def fmt_auth(a):
    if len(a)>9: return [(f'{a[0][0]}, {a[0][1]}',False),(' et al.',True)]
    names=[f'{f}, {i}' if i else f for f,i in a]
    s=names[0] if len(names)==1 else ', '.join(names[:-1])+' and '+names[-1]
    return [(s,False)]
for r in sorted(refs,key=lambda r:(r['auth'][0][0].lower(),r['year'])):
    p=d.add_paragraph(style='MyRef')
    for t,it in fmt_auth(r['auth']): p.add_run(t).italic=it
    p.add_run(f" ({r['year']}) '{r['title']}', ")
    p.add_run(r['journal']).italic=True
    loc=f", {r['vol']}" + (f"({r['iss']})" if r['iss'] else '')
    pg=r['page']
    if pg and '-' in pg: loc+=', pp. '+pg.replace('-','–')
    elif r['art'] or pg: loc+=', '+(r['art'] or pg)
    p.add_run(loc+f". Available at: https://doi.org/{r['doi']}.")
d.save(OUT)
print('saved',OUT,len(refs),'refs')
