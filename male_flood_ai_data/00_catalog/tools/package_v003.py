"""Build and verify the v002 ZIP of male_flood_ai_data (22 Nov 2026).

Checks: CRC integrity; manifest vs archive SHA-256; every 01_raw file in the v001
manifest unchanged (folder and archive) and equal to the v001 ZIP member; raw copies
vs repository originals (file_mapping); new CSV/PDF/HTML readability; Thaana
preserved; record crosswalk completeness and referential integrity.

Usage: python package_v002.py <data root> <v001 zip> <repo root> <stamp>
"""
import hashlib, io, sys, zipfile
from pathlib import Path

import pandas as pd
from pypdf import PdfReader

ROOT, OLDZIP, REPO, STAMP = Path(sys.argv[1]).resolve(), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
OUT = ROOT.parent / f"male_flood_ai_data_v002_{STAMP}.zip"
assert not OUT.exists(), "choose a new stamp"
EXCLUDE_DIRS = {"bobs_flood_workbook"}  # permission to share unconfirmed
SKIP = {".DS_Store"}
THAANA = lambda s: sum("ހ" <= c <= "޿" for c in s)
sha = lambda b: hashlib.sha256(b).hexdigest()
def fsha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while b := f.read(1 << 22): h.update(b)
    return h.hexdigest()
rd = lambda p: pd.read_csv(p, dtype=str, keep_default_na=False, encoding="utf-8-sig")
cat = ROOT / "00_catalog"
(ROOT / "06_research/reports/PACKAGE_VERIFICATION.md").unlink(missing_ok=True)

files = sorted(p for p in ROOT.rglob("*") if p.is_file() and p.name not in SKIP and "__pycache__" not in p.parts and not EXCLUDE_DIRS & set(p.parts))
excluded = sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob("*") if p.is_file() and (p.name in SKIP or EXCLUDE_DIRS & set(p.parts)))
man = pd.DataFrame([dict(path=p.relative_to(ROOT).as_posix(), size_bytes=p.stat().st_size, sha256=fsha(p)) for p in files if p.name != "package_manifest.csv"])
man.to_csv(cat / "package_manifest.csv", index=False, encoding="utf-8-sig")
files = [p for p in files if p.name != "package_manifest.csv"] + [cat / "package_manifest.csv"]
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, allowZip64=True) as z:
    for p in files:
        z.write(p, "male_flood_ai_data/" + p.relative_to(ROOT).as_posix(),
                compress_type=zipfile.ZIP_STORED if p.suffix in (".parquet", ".zip", ".png", ".tif", ".pkl", ".pdf") else zipfile.ZIP_DEFLATED)

L, fails = [f"# Package verification: {OUT.name}", "", f"Archive: `{OUT}`  ", f"Built from `{ROOT}`; previous package `{OLDZIP.name}`.", ""], []
def check(name, ok, detail):
    L.append(f"- {'PASS' if ok else 'FAIL'} - {name}: {detail}")
    if not ok: fails.append(name)
with zipfile.ZipFile(OUT) as z:
    bad = z.testzip()
    names = {n[len("male_flood_ai_data/"):]: n for n in z.namelist()}
    msha = {k: sha(z.read(v)) for k, v in names.items()}
    check("CRC integrity", bad is None, "testzip OK" if bad is None else f"first bad member {bad}")
    miss = set(man.path) - set(names); extra = set(names) - set(man.path) - {"00_catalog/package_manifest.csv"}
    shabad = [r.path for r in man.itertuples() if msha.get(r.path) != r.sha256]
    check("Manifest vs archive", not (miss or extra or shabad), f"{len(man)} files; missing {len(miss)}, unexpected {len(extra)}, SHA mismatches {len(shabad)}")
    # raw preservation against the v001 manifest and the v001 archive
    v1 = rd(ROOT / "03_reviewed/_archive_v001_20261122/package_manifest_v001.csv")
    v1raw = v1[v1.path.str.startswith("01_raw/")]
    changed = [r.path for r in v1raw.itertuples() if not (ROOT / r.path).exists() or fsha(ROOT / r.path) != r.sha256 or msha.get(r.path) != r.sha256]
    check("v001 raw files unchanged (folder and archive)", not changed, f"{len(v1raw) - len(changed)} of {len(v1raw)} match their v001 SHA-256")
    with zipfile.ZipFile(OLDZIP) as oz:
        oraw = {n[len("male_flood_ai_data/"):]: n for n in oz.namelist() if n.startswith("male_flood_ai_data/01_raw/") and not n.endswith("/")}
        odiff = [k for k, v in oraw.items() if msha.get(k) != sha(oz.read(v))]
    check("v001 ZIP raw members identical in v002 ZIP", not odiff, f"{len(oraw) - len(odiff)} of {len(oraw)}")
    mp = rd(cat / "file_mapping.csv"); mraw = mp[mp.destination_path.str.startswith("01_raw/")]
    rb = [r.destination_path for r in mraw.itertuples() if msha.get(r.destination_path) != r.sha256 or ((REPO / r.original_path).exists() and fsha(REPO / r.original_path) != r.sha256)]
    check("Raw copies vs repository originals (file_mapping)", not rb, f"{len(mraw) - len(rb)} of {len(mraw)} match")
    newraw = sorted(set(k for k in names if k.startswith("01_raw/")) - set(v1raw.path))
    inv = rd(cat / "dataset_inventory.csv").set_index("relative_path")
    nb = [k for k in newraw if k.endswith(("README.md",)) is False and (k not in inv.index or inv.loc[k, "sha256"] != msha[k])]
    check("New raw files match inventory SHA-256", not nb, f"{len(newraw)} new raw files ({len(newraw) - len(nb)} verified; READMEs not inventoried)" + (f"; issues: {nb}" if nb else ""))
    # readability
    csvs = [k for k in names if k.endswith(".csv")]; cb = []
    for k in csvs:
        try: pd.read_csv(io.BytesIO(z.read(names[k])), dtype=str, keep_default_na=False, encoding="utf-8-sig", low_memory=False)
        except Exception as ex: cb.append(f"{k}: {ex}")
    check("CSV members readable (UTF-8)", not cb, f"{len(csvs) - len(cb)} of {len(csvs)}")
    pdfs = [k for k in newraw if k.endswith(".pdf")]; pb = []
    for k in pdfs:
        try: n = len(PdfReader(io.BytesIO(z.read(names[k]))).pages); assert n > 0
        except Exception as ex: pb.append(f"{k}: {ex}")
    check("New PDFs open", not pb, f"{len(pdfs) - len(pb)} of {len(pdfs)}")
    htm = [k for k in newraw if k.endswith(".html")]
    hb = [k for k in htm if len(z.read(names[k]).decode("utf-8")) < 1000]
    check("New HTML snapshots decode", not hb, f"{len(htm) - len(hb)} of {len(htm)}")
    th = {k: THAANA(z.read(names[k]).decode("utf-8-sig")) for k in csvs}
    tb = [k for k, n in th.items() if n and n != THAANA((ROOT / k).read_text(encoding="utf-8-sig"))]
    sv_th = th.get("00_catalog/source_verification.csv", 0)
    check("Thaana preserved", not tb and sv_th > 0, f"{sum(1 for n in th.values() if n)} CSVs with Thaana; source_verification.csv {sv_th} Thaana characters")
    # crosswalk and referential integrity
    get = lambda k: pd.read_csv(io.BytesIO(z.read(names[k])), dtype=str, keep_default_na=False, encoding="utf-8-sig")
    cw, fe, ln, sv, sg = (get(k) for k in ("03_reviewed/events/record_crosswalk.csv", "03_reviewed/events/flood_events.csv", "03_reviewed/events/event_source_links.csv",
                                           "00_catalog/source_verification.csv", "03_reviewed/storm_groups/storm_groups.csv"))
    imp = get("02_interim/event_candidates/male_flood_inventory.csv"); comp = get("01_raw/flood_evidence/compiled_secondary/male_flood_basis/flood_incidents_greater_male_2021-2026.csv")
    leg = get("03_reviewed/events/legacy_daily_exploration/event_review.csv"); gs = get("02_interim/groundsource_candidates/inventory_comparison.csv")
    want = (set(imp.record_id) | {"MFB_" + x for x in comp.incident_id} | {"LEGACY_REVIEW_" + x for x in leg.incident_id}
            | {f"GS_{a}_{b}" for a, b in zip(gs.groundsource_start, gs.groundsource_latest_end)} | {"SP_2023-10-01", "SP_2023-12-31", "SP_2024-01-12"}
            | {f"LEGACY_S{i:02d}" for i in range(1, 18)})
    have = set(cw.original_record_id)
    nodec = cw[cw.decisions == ""].original_record_id.tolist()
    evs = {e for x in cw.event_ids for e in x.split(";") if e}
    check("Crosswalk covers every original record", want <= have and not nodec,
          f"{len(want)} originals expected (30 import, 18 compiled, 18 legacy, 3 starter, 29 Groundsource, 17 legacy storms); missing {len(want - have)}; without decision {len(nodec)}")
    check("Crosswalk events exist", evs <= set(fe.event_id), f"{len(evs)} referenced; unknown {len(evs - set(fe.event_id))}")
    nolink = set(fe.event_id) - set(ln.event_id); unk = set(ln.source_id) - set(sv.source_id)
    check("Every event linked to a verified source", not nolink and not unk, f"{len(fe)} events; unlinked {len(nolink)}; unknown sources {len(unk)}")
    check("Every event has a storm group", set(fe.storm_group_id) <= set(sg.storm_group_id) and all(fe.storm_group_id), f"{fe.storm_group_id.nunique()} groups used")
    check("Imported CSV unchanged", msha["02_interim/event_candidates/male_flood_inventory.csv"] == fsha(REPO / "male_flood_inventory.csv"), "byte-identical to repository original")
L.insert(5, f"**Result: {'PASS' if not fails else 'FAIL: ' + ', '.join(fails)}**  ")
L.insert(6, f"Archive size {OUT.stat().st_size:,} bytes; {len(names)} members (+ this report, appended afterwards).")
L.insert(7, "")
L += ["", "Excluded by design: " + (", ".join(excluded) or "none") + ". `bobs flood.xlsx` is held locally until permission to share is confirmed; OS metadata files are skipped.",
      "Previous verification report: `06_research/reports/archive/PACKAGE_VERIFICATION_v001_20261122.md`."]
txt = "\n".join(L) + "\n"
(ROOT / "06_research/reports/PACKAGE_VERIFICATION.md").write_text(txt, encoding="utf-8")
with zipfile.ZipFile(OUT, "a", zipfile.ZIP_DEFLATED, allowZip64=True) as z:
    z.writestr("male_flood_ai_data/06_research/reports/PACKAGE_VERIFICATION.md", txt)
with zipfile.ZipFile(OUT) as z:
    assert z.testzip() is None
print(txt)
