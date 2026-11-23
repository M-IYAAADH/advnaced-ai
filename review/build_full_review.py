# Builds the full review into the coursework template.
# Usage: python3 build_full_review.py <template.docx> <out.docx>
#   template.docx = the coursework .doc converted with: soffice --headless --convert-to docx <file>.doc
#   needs python-docx; reads review_content.py, refs.json and the two figures from this folder.
import sys, os, re, json
import docx
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import review_content as RC

SRC, OUT = sys.argv[1], sys.argv[2]
FIGS = {'fig1': os.path.join(HERE, '..', 'derived', 'male_wards_map.png'),
        'fig2': os.path.join(HERE, 'fig2_framework.png')}

d = docx.Document(SRC)
st = d.styles
st['MyFirstPar'].font.size = Pt(11)   # template's 11 pt was manual formatting; fix it in the style
st['MyFirstPar'].paragraph_format.space_after = Pt(6)
st['MyRef'].font.size = Pt(9)
st['MyRef'].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT  # justified URLs leave wide gaps
st['MyRef'].paragraph_format.space_after = Pt(2)

body = d.element.body
paras = d.paragraphs
def set_text(p, t):
    p.runs[0].text = t
    for r in p.runs[1:]: r.text = ''
set_text(paras[0], RC.TITLE)
set_text(paras[2], RC.AUTHOR)
for p in paras[4:]:
    body.remove(p._p)  # the final 2-column sectPr stays

def runs(p, text, size=None):
    text = text.replace('[', '(').replace(']', ')')  # citations written with [] in the content file
    for i, part in enumerate(re.split(r'\*([^*]+)\*', text)):
        if not part: continue
        r = p.add_run(part); r.italic = (i % 2 == 1)
        if size: r.font.size = Pt(size)

def caption(t):
    p = d.add_paragraph(style='FirstBody'); p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.space_after = Pt(8); runs(p, t)

def table(T):
    caption(T['caption'])
    t = d.add_table(rows=1, cols=len(T['head']))
    t.style = None
    widths = [Cm(1.8), Cm(2.5), Cm(1.6), Cm(2.3)]
    for i, h in enumerate(T['head']):
        c = t.rows[0].cells[i]; c.paragraphs[0].text = ''
        r = c.paragraphs[0].add_run(h); r.bold = True; r.font.size = Pt(8)
    for row in T['rows']:
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].paragraphs[0].text = ''; runs(cells[i].paragraphs[0], v, size=8)
    for row in t.rows:
        for i, c in enumerate(row.cells):
            c.width = widths[i]
            for p in c.paragraphs:
                p.paragraph_format.space_after = Pt(0); p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    # fixed layout + explicit grid, otherwise LibreOffice/Word ignore the cell widths
    tblPr = t._tbl.tblPr
    lay = OxmlElement('w:tblLayout'); lay.set(qn('w:type'), 'fixed'); tblPr.append(lay)
    tw = OxmlElement('w:tblW'); tw.set(qn('w:w'), str(int(sum(w.cm for w in widths) * 567))); tw.set(qn('w:type'), 'dxa'); tblPr.append(tw)
    for gc, w in zip(t._tbl.tblGrid.findall(qn('w:gridCol')), widths): gc.set(qn('w:w'), str(int(w.cm * 567)))
    # top, header and bottom rules only (booktabs look)
    b = OxmlElement('w:tblBorders')
    for edge in ('top', 'bottom', 'insideH'):
        e = OxmlElement(f'w:{edge}'); e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), '4'); e.set(qn('w:color'), '000000')
        b.append(e)
    tblPr.append(b)
    d.add_paragraph(style='MyFirstPar')

for kind, val in RC.C:
    if kind == 'H':
        d.add_paragraph(val, style='MyH1')
    elif kind == 'S':
        p = d.add_paragraph(style='MyFirstPar'); r = p.add_run(val); r.bold = True
        p.paragraph_format.space_after = Pt(2); p.paragraph_format.keep_with_next = True
    elif kind == 'P':
        runs(d.add_paragraph(style='MyFirstPar'), val)
    elif kind == 'TABLE':
        table(RC.TABLE)
    elif kind == 'FIG':
        key, cap = val
        p = d.add_paragraph(style='MyFirstPar'); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(FIGS[key], width=Cm(7.8))
        p.paragraph_format.keep_with_next = True
        caption(cap)

d.add_paragraph('REFERENCES', style='MyH1')
refs = json.load(open(os.path.join(HERE, 'refs.json')))
def initials(i): return i.upper()
def fmt_auth(a):
    if len(a) > 9: return [(f'{a[0][0]}, {initials(a[0][1])}', False), (' et al.', True)]
    names = [f'{f}, {initials(i)}' if i else f for f, i in a]
    return [(names[0] if len(names) == 1 else ', '.join(names[:-1]) + ' and ' + names[-1], False)]
for r in sorted(refs, key=lambda r: (r['auth'][0][0].lower(), r['year'])):
    p = d.add_paragraph(style='MyRef')
    for t, it in fmt_auth(r['auth']): p.add_run(t).italic = it
    p.add_run(f" ({r['year']}) '{r['title']}', ")
    p.add_run(r['journal']).italic = True
    loc = f", {r['vol']}" + (f"({r['iss']})" if r['iss'] else '')
    pg = r['page']
    if pg and '-' in pg: loc += ', pp. ' + pg.replace('-', '–')
    elif r['art'] or pg: loc += ', ' + (r['art'] or pg)
    p.add_run(loc + f". Available at: https://doi.org/{r['doi']}.")
d.save(OUT)
words = sum(len(re.sub(r'\*', '', v).split()) for k, v in RC.C if k == 'P')
print('saved', OUT, '| body words:', words, '| refs:', len(refs))
