"""Sync organising tools, write a manifest, build a timestamped ZIP64 archive of male_flood_ai_data
and verify it (integrity, checksums, raw files vs originals, CSV/Thaana readability, reconciliation
coverage). The verification report is written beside the archive and appended into it.
    python scripts/package_male_flood_ai_data.py --repo . --dest ../male_flood_ai_data --stamp 20261122T161053Z
"""
import argparse, hashlib, io, shutil, zipfile
from pathlib import Path

import pandas as pd

TOOLS = ["organise_male_flood_ai_data.py", "reconcile_flood_inventory.py", "finalise_catalog.py", "package_male_flood_ai_data.py"]
SKIP = {".DS_Store"}
THAANA = lambda s: sum("ހ" <= c <= "޿" for c in s)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def fsha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while b := f.read(1 << 22):
            h.update(b)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--dest", required=True)
    ap.add_argument("--stamp", required=True)
    a = ap.parse_args()
    repo, dest = Path(a.repo).resolve(), Path(a.dest).resolve()
    out = dest.parent / f"male_flood_ai_data_{a.stamp}.zip"
    assert not out.exists(), f"{out} exists; choose a new stamp"
    cat = dest / "00_catalog"
    rd = lambda p: pd.read_csv(p, dtype=str, keep_default_na=False, encoding="utf-8-sig")

    # 1. tools: current versions in 00_catalog/tools; drop this session's stale copies from legacy/scripts
    mp = rd(cat / "file_mapping.csv")
    (cat / "tools").mkdir(exist_ok=True)
    for t in TOOLS:
        src = repo / "scripts" / t
        (dest / "05_outputs/legacy/scripts" / t).unlink(missing_ok=True)
        shutil.copy2(src, cat / "tools" / t)
        h = fsha(src)
        row = dict(original_path=f"scripts/{t}", original_filename=t, size_bytes=str(src.stat().st_size), sha256=h,
                   identical_repo_files="", destination_path=f"00_catalog/tools/{t}", role="organising_tool", copy_action="copied",
                   checksum_verified="yes" if fsha(cat / "tools" / t) == h else "NO", needs_human_classification="",
                   notes="Written in this organisation task; current version.")
        mp = pd.concat([mp[mp.original_path != f"scripts/{t}"], pd.DataFrame([row])], ignore_index=True)
    mp.to_csv(cat / "file_mapping.csv", index=False, encoding="utf-8-sig")

    # 2. re-verify every mapped copy against its current original
    problems = []
    for _, r in mp[mp.destination_path != ""].iterrows():
        d, o = dest / r.destination_path, repo / r.original_path
        if not d.exists():
            problems.append(f"missing copy {r.destination_path}")
        elif fsha(d) != r.sha256 or (o.exists() and fsha(o) != r.sha256):
            problems.append(f"checksum mismatch {r.destination_path}")

    # 3. manifest (a previous run's verification report is regenerated below, never packed twice)
    (dest / "06_research/reports/PACKAGE_VERIFICATION.md").unlink(missing_ok=True)
    files = sorted(p for p in dest.rglob("*") if p.is_file() and p.name not in SKIP and "__pycache__" not in p.parts)
    excluded = sorted(str(p.relative_to(dest)) for p in dest.rglob("*") if p.is_file() and (p.name in SKIP or "__pycache__" in p.parts))
    man = pd.DataFrame([dict(path=p.relative_to(dest).as_posix(), size_bytes=p.stat().st_size, sha256=fsha(p))
                        for p in files if p.name != "package_manifest.csv"])
    man.to_csv(cat / "package_manifest.csv", index=False, encoding="utf-8-sig")
    files = [p for p in files if p.name != "package_manifest.csv"] + [cat / "package_manifest.csv"]

    # 4. zip (ZIP64 allowed; parquet stored, it is already compressed)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, allowZip64=True) as z:
        for p in files:
            arc = "male_flood_ai_data/" + p.relative_to(dest).as_posix()
            z.write(p, arc, compress_type=zipfile.ZIP_STORED if p.suffix in (".parquet", ".zip", ".png", ".tif", ".pkl") else zipfile.ZIP_DEFLATED)

    # 5. verify
    lines = [f"# Package verification: {out.name}", "", f"Archive: `{out}`", ""]
    with zipfile.ZipFile(out) as z:
        bad = z.testzip()
        names = {n[len("male_flood_ai_data/"):]: n for n in z.namelist()}
        member_sha = {k: sha(z.read(v)) for k, v in names.items()}
        zip64 = any(i.file_size >= 0xFFFFFFFF or i.compress_size >= 0xFFFFFFFF for i in z.infolist()) or out.stat().st_size >= 0xFFFFFFFF
        missing = sorted(set(man.path) - set(names))
        extra = sorted(set(names) - set(man.path) - {"00_catalog/package_manifest.csv"})
        sha_bad = [r.path for _, r in man.iterrows() if member_sha.get(r.path) != r.sha256]
        raw = mp[mp.destination_path.str.startswith("01_raw/")]
        raw_bad = [r.destination_path for _, r in raw.iterrows() if member_sha.get(r.destination_path) != r.sha256]
        csv_bad, thaana = [], {}
        for k, v in names.items():
            if k.endswith(".csv"):
                txt = z.read(v).decode("utf-8-sig")
                try:
                    pd.read_csv(io.StringIO(txt), dtype=str, keep_default_na=False, low_memory=False)
                except Exception as ex:
                    csv_bad.append(f"{k}: {ex}")
                if THAANA(txt):
                    thaana[k] = (THAANA(txt), THAANA((dest / k).read_text(encoding="utf-8-sig")))
        imp = pd.read_csv(io.BytesIO(z.read(names["02_interim/event_candidates/male_flood_inventory.csv"])), dtype=str, keep_default_na=False, encoding="utf-8-sig")
        rec = pd.read_csv(io.BytesIO(z.read(names["02_interim/event_candidates/inventory_reconciliation.csv"])), dtype=str, keep_default_na=False, encoding="utf-8-sig")
        uncovered = sorted(set(imp.record_id) - set(rec.imported_record_id))
        imp_sha_ok = member_sha["02_interim/event_candidates/male_flood_inventory.csv"] == fsha(repo / "male_flood_inventory.csv")
    thaana_bad = [k for k, (zc, dc) in thaana.items() if zc != dc or zc == 0]
    ok = not any([bad, missing, extra, sha_bad, raw_bad, csv_bad, uncovered, thaana_bad, problems]) and imp_sha_ok
    lines += [
        f"- Result: **{'PASS' if ok else 'FAIL'}**",
        f"- Archive size: {out.stat().st_size:,} bytes; members: {len(names)} (+ this report, appended afterwards); ZIP64 needed: {zip64} (written with allowZip64=True)",
        f"- CRC integrity (`testzip`): {'OK' if bad is None else 'first bad member ' + bad}",
        f"- Manifest vs archive: missing {len(missing)}, unexpected {len(extra)}, SHA-256 mismatches {len(sha_bad)} of {len(man)}",
        f"- Raw files (01_raw) vs original repository checksums: {len(raw) - len(raw_bad)} of {len(raw)} match",
        f"- Mapped copies re-verified against current originals: {len(mp[mp.destination_path != ''])} checked, problems {len(problems)}",
        f"- Imported CSV byte-identical to the repository original: {imp_sha_ok}",
        f"- CSV members readable as UTF-8: {sum(k.endswith('.csv') for k in names) - len(csv_bad)} of {sum(k.endswith('.csv') for k in names)}",
        f"- Thaana preserved (character counts archive = folder): " + "; ".join(f"{k} {zc}" for k, (zc, dc) in sorted(thaana.items())),
        f"- Reconciliation coverage: {len(imp) - len(uncovered)} of {len(imp)} imported records present in inventory_reconciliation.csv",
        f"- Excluded from archive: {', '.join(excluded) or 'none'} (OS metadata). Not included by design: the original template ZIP (preserved unchanged in Downloads), the new archive itself, `.git`, caches, `sprint_board.html` (app UI), `.gitignore`.",
    ]
    for label, items in (("Problems", problems), ("Missing", missing), ("Unexpected", extra), ("SHA mismatch", sha_bad),
                         ("Raw mismatch", raw_bad), ("CSV errors", csv_bad), ("Uncovered records", uncovered), ("Thaana mismatch", thaana_bad)):
        if items:
            lines.append(f"- {label}: " + "; ".join(items[:20]))
    report = "\n".join(lines) + "\n"
    (out.with_suffix(".verification.md")).write_text(report, encoding="utf-8")
    (dest / "06_research/reports/PACKAGE_VERIFICATION.md").write_text(report, encoding="utf-8")
    with zipfile.ZipFile(out, "a", zipfile.ZIP_DEFLATED, allowZip64=True) as z:
        z.writestr("male_flood_ai_data/06_research/reports/PACKAGE_VERIFICATION.md", report)
    with zipfile.ZipFile(out) as z:
        assert z.testzip() is None
    print(report)


if __name__ == "__main__":
    main()
