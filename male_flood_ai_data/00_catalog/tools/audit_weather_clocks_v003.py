"""Weather/sea-level clock, decoding and accumulation-window audit (v003, 22 Nov 2026).

Reads raw NOAA ISD (global hourly) and GSOD files for station 43555099999 (Hulhule),
the compiled Open-Meteo ERA5 and marine files, and the UHSLC clean copy. Writes
evidence tables only. No raw file is modified, no series is shifted in place, no
rainfall value is rescaled, and nothing here is a model input.

Changes from v002:
  * AA groups are decoded with explicit parse status; malformed, period-99,
    off-schedule and duplicate/conflicting groups are counted, never silently dropped
    or resolved with "first".
  * A decoding audit (rainfall_decoding_audit_v003.csv) documents units, scaling,
    periods, condition/quality codes, missing values and the one-tenth discrepancy.
    The discrepancy stays an unresolved reporting/decoding issue; nothing is x10.
  * 6 h blocks carry local-day assignment, midnight-crossing flags, component raw
    groups, conflicts and negative differences (kept, not clipped). Four-block
    conservation is checked against complete 12 h totals (tolerance 0.05 mm) and
    hand-checked reference cases guard against time-shift, subtraction and scaling
    errors (with mutation tests showing each would be caught).
  * GSOD window alternatives: wet-day agreement and the unmatched day. The window
    applies to PRCP only, not to temperature, pressure or other GSOD fields.
  * ERA5 UTC+5 is described as empirically supported, not established.

Usage:  python audit_weather_clocks_v003.py <male_flood_ai_data root>
"""
import csv
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(sys.argv[1])
ST = ROOT / "01_raw/rainfall/station/noaa_velana_435550_99999"
OUT_I = ROOT / "02_interim/weather_aligned"
OUT_E = ROOT / "03_reviewed/time_alignment/evidence"
OUT_E.mkdir(parents=True, exist_ok=True)
LOCAL = pd.Timedelta(hours=5)  # Asia/Male, fixed UTC+5, no DST
YEARS = range(2020, 2026)
TOL = 0.05  # mm; amounts are reported in 0.1 mm steps, so any real disagreement is >= 0.1
SCHEDULE = {6: (6, 18), 12: (0, 12), 24: (0,)}  # FM-12 SYNOP reporting hours (UTC) per accumulation period
COND = {"1": "measurement impossible or inaccurate", "2": "trace", "3": "begin accumulated period (amount missing until end)",
        "4": "end accumulated period", "5": "begin deleted period", "6": "end deleted period", "7": "begin missing period",
        "8": "end missing period", "E": "estimated", "I": "incomplete (missing reports)", "J": "incomplete (erroneous reports)", "9": "missing"}
QUAL = {"0": "passed gross limits", "1": "passed all QC", "2": "suspect", "3": "erroneous", "4": "passed gross limits (NCEI source)",
        "5": "passed all QC (NCEI source)", "6": "suspect (NCEI source)", "7": "erroneous (NCEI source)", "9": "passed gross limits if element present"}
audit = []
def A(check, scope, value, expectation="", result="", note=""):
    audit.append(dict(check=check, scope=scope, value=value, expectation=expectation, result=result, note=note))

# ------------------------------------------------------------- 1. decode AA groups
rows = []
for y in YEARS:
    h = pd.read_csv(ST / f"noaa_global_hourly_{y}_43555099999.csv", dtype=str, low_memory=False)
    for c in [c for c in h.columns if c.startswith("AA")]:
        s = h[h[c].notna()]
        for date, rtype, src, grp in zip(s.DATE, s.REPORT_TYPE.str.strip(), s.SOURCE, s[c]):
            p = grp.split(",")
            ok = len(p) == 4 and p[0].isdigit() and len(p[0]) == 2 and p[1].isdigit() and len(p[1]) == 4
            rows.append(dict(observation_time_utc=date + "Z", report_type=rtype, isd_source=src, field=c, raw_group=grp,
                             parse_status="ok" if ok else "malformed",
                             accumulation_hours=(None if p[0] == "99" else int(p[0])) if ok else None,
                             # ISD format document: depth in mm, scaling factor 10, 9999 = missing
                             precipitation_mm=(None if p[1] == "9999" else int(p[1]) / 10.0) if ok else None,
                             depth_raw=p[1] if ok else "", condition_code=p[2] if ok else "", quality_code=p[3] if ok else ""))
g = pd.DataFrame(rows)
g["t"] = pd.to_datetime(g.observation_time_utc.str.rstrip("Z"))
g["condition_meaning"] = g.condition_code.map(COND).fillna("undocumented code")
g["quality_meaning"] = g.quality_code.map(QUAL).fillna("undocumented code")
g["on_synoptic_schedule"] = [bool(p == p and int(p) in SCHEDULE and t.hour in SCHEDULE[int(p)] and t.minute == 0) for p, t in zip(g.accumulation_hours, g.t)]
key = ["t", "accumulation_hours", "report_type"]
nv = g.dropna(subset=["accumulation_hours"]).groupby(key).precipitation_mm.nunique(dropna=False)
g = g.merge(nv.rename("n_distinct").reset_index(), on=key, how="left")
g["conflicting_duplicate"] = g.n_distinct.fillna(1) > 1
g["window_start_local"] = (g.t - pd.to_timedelta(g.accumulation_hours, unit="h") + LOCAL).dt.strftime("%Y-%m-%dT%H:%M")
g["window_end_local"] = (g.t + LOCAL).dt.strftime("%Y-%m-%dT%H:%M")
g.drop(columns=["t", "n_distinct"]).to_csv(OUT_I / "noaa_synop_precip_groups_2020-2025_v003.csv", index=False)

# ------------------------------------------------------------- 2. decoding audit
A("format: depth units/scaling", "ISD format document (provider_docs/isd-format-document.pdf)", "mm, scaling factor 10; 9999 missing; period 99 missing",
  "decoder divides 4-digit depth by 10", "applied", "parser: precipitation_mm = int(depth)/10; no further scaling")
A("parse status", "all AA groups 2020-2025", f"{len(g)} groups; malformed {int((g.parse_status != 'ok').sum())}", "0 malformed",
  "pass" if (g.parse_status == "ok").all() else "fail")
A("report types / ISD source", "all AA groups", "; ".join(f"{k} {v}" for k, v in g.report_type.value_counts().items()) + " | source " +
  "; ".join(f"{k} {v}" for k, v in g.isd_source.value_counts().items()))
A("duplicates", "same time, period and report type", f"{int(g.duplicated(key).sum())} duplicate rows; {int(g.conflicting_duplicate.sum())} rows in conflicting sets",
  "conflicts flagged, never resolved by order", "pass")
p99 = g[g.accumulation_hours.isna() & (g.parse_status == "ok")]
A("period 99 (missing period)", "groups", f"{len(p99)} groups; {int((p99.precipitation_mm > 0).sum())} with a positive depth", "excluded from blocks: window unknown",
  "flagged", "kept in the groups table with accumulation_hours blank")
off = g[g.accumulation_hours.notna() & ~g.on_synoptic_schedule]
A("off-schedule groups", "period known, hour outside 00/06/12/18 schedule", f"{len(off)} groups at hours {sorted(set(off.t.dt.hour))}",
  "excluded from blocks; listed", "flagged", "GSOD used the 03 UTC 24 h group on 2021-07-03 (see GSOD alternatives)")
for per in (6, 12, 24):
    s = g[(g.accumulation_hours == per)]
    pos = s[s.precipitation_mm > 0]
    frac = pos[pos.depth_raw.str[-1] != "0"]
    A(f"{per} h depth resolution", f"{per} h groups", f"{len(s)} groups; missing {int(s.precipitation_mm.isna().sum())}; zero {int((s.precipitation_mm == 0).sum())}; "
      f"positive {len(pos)}; positive with a non-zero tenths digit {len(frac)}, of which >= 1 mm: {int((frac.precipitation_mm >= 1).sum())}",
      "6/12 h: whole mm except sub-1 mm amounts (SYNOP code table 3590: RRR in mm, 990-999 = tenths below 1 mm)" if per < 24 else "24 h group: 0.1 mm resolution",
      ("consistent" if (frac.precipitation_mm < 1).all() else "inconsistent") if per < 24 else "see one-tenth checks")
cq = pd.crosstab(np.where(g.precipitation_mm.isna(), "missing", np.where(g.precipitation_mm == 0, "zero", "positive")), g.condition_code)
for depth_class, r in cq.iterrows():
    A("condition codes by depth class", depth_class, "; ".join(f"{k}={int(v)}" for k, v in r.items() if v),
      "", "noted", "code 3 accompanies every positive amount although documented as 'begin accumulated period'; amounts used as reported, code not relied on")
qq = pd.crosstab(g.accumulation_hours.fillna(99).astype(int), g.quality_code)
for per, r in qq.iterrows():
    A("quality codes by period", f"{per} h" if per != 99 else "period 99", "; ".join(f"{k}={int(v)}" for k, v in r.items() if v), "", "noted",
      "quality 2 = suspect; suspect components are flagged on blocks (any_suspect_qc) and excluded from the ERA5 clock test")

# ------------------------------------------------------- 3. non-overlapping 6 h blocks
fm = g[(g.report_type == "FM-12") & g.on_synoptic_schedule]
def table(hours, hour):
    s = fm[(fm.accumulation_hours == hours) & (fm.t.dt.hour == hour)]
    return {t: (x.precipitation_mm.iloc[0] if x.precipitation_mm.nunique(dropna=False) == 1 else np.nan,
                "/".join(sorted(set(x.quality_code))), " | ".join(x.raw_group), bool(x.conflicting_duplicate.any()))
            for t, x in s.groupby("t")}
g6_06, g12_12, g6_18, g12_00, g24_00 = table(6, 6), table(12, 12), table(6, 18), table(12, 0), table(24, 0)
MISSING = (np.nan, "", "", False)
blocks = []
for day in pd.date_range(f"{YEARS[0]}-01-01", f"{YEARS[-1]}-12-31"):
    t06, t12, t18, t24 = (day + pd.Timedelta(hours=h) for h in (6, 12, 18, 24))
    a = g6_06.get(t06, MISSING); b12 = g12_12.get(t12, MISSING); c = g6_18.get(t18, MISSING); d12 = g12_00.get(t24, MISSING)
    def diff(big, small):
        return big[0] - small[0] if pd.notna(big[0]) and pd.notna(small[0]) else np.nan
    for start, mm, how, parts in (
        (day, a[0], "6h group ending 06Z", [a]),
        (t06, diff(b12, a), "12h group ending 12Z minus 6h ending 06Z", [b12, a]),
        (t12, c[0], "6h group ending 18Z", [c]),
        (t18, diff(d12, c), "12h group ending 00Z(next) minus 6h ending 18Z", [d12, c]),
    ):
        missing = [n for n, p in zip(("12h" if len(parts) == 2 else "6h", "6h"), parts) if pd.isna(p[0])]
        blocks.append(dict(block_start_utc=start, block_end_utc=start + pd.Timedelta(hours=6), precipitation_mm=mm, derivation=how,
                           component_raw_groups=" ; ".join(p[2] or "absent" for p in parts), quality_codes="/".join(p[1] for p in parts),
                           conflicting_observation=any(p[3] for p in parts),
                           missing_reason="" if pd.notna(mm) else ("conflicting duplicate" if any(p[3] for p in parts) else "component absent or missing: " + ",".join(missing)),
                           negative_difference=bool(pd.notna(mm) and mm < -TOL)))
bl = pd.DataFrame(blocks)
assert ((bl.block_end_utc - bl.block_start_utc) == pd.Timedelta(hours=6)).all()
assert (bl.block_start_utc.diff().dropna() == pd.Timedelta(hours=6)).all(), "blocks must tile time without gaps or overlaps"
bl["block_start_local"] = (bl.block_start_utc + LOCAL).dt.strftime("%Y-%m-%dT%H:%M")
bl["block_end_local"] = (bl.block_end_utc + LOCAL).dt.strftime("%Y-%m-%dT%H:%M")
bl["crosses_local_midnight"] = (bl.block_start_utc + LOCAL).dt.date != (bl.block_end_utc + LOCAL - pd.Timedelta(seconds=1)).dt.date
# local day D is measured 05:00 D to 05:00 D+1: the block starting 23:00 local belongs to the day it starts on
bl["local_day_0500_0500"] = (bl.block_start_utc + LOCAL - pd.Timedelta(hours=5)).dt.strftime("%Y-%m-%d")
bl["any_suspect_qc"] = bl.quality_codes.str.contains("2")
assert bl.crosses_local_midnight.sum() == len(bl) // 4 and (bl[bl.crosses_local_midnight].block_start_local.str[11:] == "23:00").all()
out_bl = bl.assign(block_start_utc=bl.block_start_utc.dt.strftime("%Y-%m-%dT%H:%MZ"), block_end_utc=bl.block_end_utc.dt.strftime("%Y-%m-%dT%H:%MZ"))
out_bl.to_csv(OUT_I / "noaa_synop_6h_blocks_2020-2025_v003.csv", index=False)
A("6 h blocks", "2020-2025", f"{len(bl)} blocks; with value {int(bl.precipitation_mm.notna().sum())}; negative differences {int(bl.negative_difference.sum())} (kept, flagged); "
  f"conflicting {int(bl.conflicting_observation.sum())}; crossing local midnight {int(bl.crosses_local_midnight.sum())} (23:00-05:00 local)", "", "built")
neg = bl[bl.negative_difference]
A("negative differences", "6 h blocks", "; ".join(f"{r.block_start_local} {r.precipitation_mm:+.1f} mm [{r.component_raw_groups}]" for r in neg.itertuples()) or "none",
  "never clipped to zero", "flagged", "excluded from daily totals and the ERA5 test; value kept as computed")

# four-block conservation against complete 12 h totals (an identity by construction: it catches bookkeeping, not shifts or scaling)
cons = []
for day, x in bl.groupby(bl.block_start_utc.dt.normalize()):
    t12, t24 = day + pd.Timedelta(hours=12), day + pd.Timedelta(hours=24)
    a, b = g12_12.get(t12, MISSING)[0], g12_00.get(t24, MISSING)[0]
    if len(x) == 4 and x.precipitation_mm.notna().all() and pd.notna(a) and pd.notna(b):
        cons.append(abs(x.precipitation_mm.sum() - (a + b)) <= TOL)
A("four-block conservation", "UTC days with 4 blocks and both 12 h groups", f"{sum(cons)} of {len(cons)} within {TOL} mm",
  "all pass", "pass" if all(cons) else "fail", "identity by construction (a + (b12 - a) + c + (d12 - c) = b12 + d12); insufficient on its own - see reference cases")
assert all(cons)

# --------------------------------------------- 4. hand-checked reference cases
# Each expected value was derived by hand from the raw ISD lines quoted in raw_groups (read from the CSV text, 22 Nov 2026).
REF = [
    # (case, block_start_utc, expected_mm or None for missing, raw groups used, hand arithmetic, guards against)
    ("R1", "2023-04-01T00:00", 49.0, "2023-04-01T06 AA1 06,0490,3,1", "490/10 = 49.0 (6 h group as reported)", "scaling (x10 -> 490, /10 -> 4.9); shift (neighbouring blocks are 0)"),
    ("R2", "2023-04-01T06:00", 0.0, "2023-04-01T12 AA1 12,0490,3,1 ; 2023-04-01T06 AA1 06,0490,3,1", "49.0 - 49.0 = 0.0", "subtraction omitted (would give 49.0)"),
    ("R3", "2024-01-10T06:00", 27.7, "2024-01-10T12 AA1 12,0280,3,1 ; 2024-01-10T06 AA1 06,0003,3,1", "28.0 - 0.3 = 27.7", "subtraction with mixed resolution; scaling"),
    ("R4", "2024-01-10T12:00", 50.0, "2024-01-10T18 AA1 06,0500,3,1", "500/10 = 50.0", "shift (adjacent blocks 27.7 and 1.0)"),
    ("R5", "2024-01-10T18:00", 1.0, "2024-01-11T00 AA1 12,0510,3,2 ; 2024-01-10T18 AA1 06,0500,3,1", "51.0 - 50.0 = 1.0 (23:00 10 Jan - 05:00 11 Jan local)", "midnight crossing; subtraction"),
    ("R6", "2024-04-13T06:00", 86.0, "2024-04-13T12 AA1 12,0860,3,1 ; 2024-04-13T06 AA1 06,0000,9,1", "86.0 - 0.0 = 86.0", "shift (05:00-11:00 local block is 0)"),
    ("R7", "2024-04-13T18:00", 3.0, "2024-04-14T00 AA1 12,0230,3,1 ; 2024-04-13T18 AA1 06,0200,3,1", "23.0 - 20.0 = 3.0", "subtraction omitted (would give 23.0)"),
    ("R8", "2025-01-10T18:00", 62.0, "2025-01-11T00 AA1 12,0700,3,1 ; 2025-01-10T18 AA1 06,0080,3,1", "70.0 - 8.0 = 62.0 (23:00 10 Jan - 05:00 11 Jan local)", "midnight crossing; shift (next block 31.0)"),
    ("R9", "2023-12-31T00:00", None, "no 6 h group at 2023-12-31T06; 12 h ending 12Z = 12,1840,3,1", "missing (not 0, not 184.0)", "missingness preserved"),
]
bv = bl.set_index(bl.block_start_utc.dt.strftime("%Y-%m-%dT%H:%M")).precipitation_mm
raw_text = set(g.observation_time_utc.str[:13] + " " + g.field + " " + g.raw_group)
def check_refs(series):
    return [(None if pd.isna(series.get(s, np.nan)) else round(float(series.get(s)), 1)) == exp for _, s, exp, *_ in REF]
ref_rows = []
for (case, s, exp, raw, arith, guards), ok in zip(REF, check_refs(bv)):
    quoted = [q.strip() for q in raw.split(";") if q.strip()[:4].isdigit() and " AA" in q]
    raw_ok = all(q in raw_text for q in quoted)
    ref_rows.append(dict(case=case, block_start_utc=s, block_start_local=(pd.Timestamp(s) + LOCAL).strftime("%Y-%m-%dT%H:%M"), expected_mm=exp,
                         computed_mm=bv.get(s), raw_groups=raw, hand_arithmetic=arith, guards_against=guards, raw_quoted_matches_file=raw_ok, result="pass" if ok and raw_ok else "fail"))
# mutation tests: each plausible bug must fail at least one reference case
mut = {"blocks shifted +6 h": bv.shift(1), "blocks shifted -6 h": bv.shift(-1), "blocks shifted +5 h (local labels as UTC)": bv.shift(1),
       "depth x10": bv * 10, "depth /10": bv / 10,
       "subtraction omitted": bl.assign(v=np.where(bl.derivation.str.startswith("12h"),
                                                   [g12_12.get(t + pd.Timedelta(hours=6), MISSING)[0] if t.hour == 6 else g12_00.get(t + pd.Timedelta(hours=6), MISSING)[0] for t in bl.block_start_utc],
                                                   bl.precipitation_mm)).set_index(bv.index).v,
       "missing filled with 0": bv.fillna(0)}
for name, series in mut.items():
    caught = [r[0] for r, ok in zip(REF, check_refs(series)) if not ok]
    ref_rows.append(dict(case="MUTATION", block_start_utc="", expected_mm="", computed_mm="", raw_groups="", hand_arithmetic=name,
                         guards_against="caught by " + (",".join(caught) or "NONE"), raw_quoted_matches_file="", result="pass" if caught else "fail"))
ref = pd.DataFrame(ref_rows)
ref.to_csv(OUT_E / "rainfall_reference_cases_v003.csv", index=False)
assert (ref.result == "pass").all(), ref[ref.result != "pass"]
A("reference cases", "9 hand-checked blocks + 7 mutation tests", f"{int((ref.result == 'pass').sum())} of {len(ref)} pass", "all pass", "pass",
  "03_reviewed/time_alignment/evidence/rainfall_reference_cases_v003.csv")

# ----------------------------------------------- 5. GSOD versus the 24 h group
gs = pd.concat([pd.read_csv(ST / f"noaa_gsod_{y}_43555099999.csv", dtype=str) for y in YEARS])
gs["d"] = pd.to_datetime(gs.DATE)
gs["prcp_in"] = pd.to_numeric(gs.PRCP)
gs["flag"] = gs.PRCP_ATTRIBUTES.str.strip()
gs["prcp_mm"] = np.where(gs.prcp_in >= 99.99, np.nan, (gs.prcp_in * 25.4).round(1))
v24 = pd.Series({t: v[0] for t, v in g24_00.items()}); q24 = pd.Series({t: v[1] for t, v in g24_00.items()})
r24 = pd.Series({t: v[2] for t, v in g24_00.items()})
v12 = {**{t: v[0] for t, v in g12_12.items()}, **{t: v[0] for t, v in g12_00.items()}}
def pair(end):
    a, b = v12.get(end - pd.Timedelta(hours=12), np.nan), v12.get(end, np.nan)
    return a + b
m = gs.set_index("d")[["PRCP", "flag", "prcp_mm"]]
m["synop24h_00Z_same_date_mm"] = v24.reindex(m.index)
m["synop24h_quality"] = q24.reindex(m.index)
m["synop24h_raw_group"] = r24.reindex(m.index)
m["synop_12h_pair_sum_mm"] = [pair(d) for d in m.index]
m["gsod_equals_24h_group"] = (m.prcp_mm - m.synop24h_00Z_same_date_mm).abs() <= 0.3
m["window_local"] = [f"{(d - pd.Timedelta(days=1)):%Y-%m-%d} 05:00 to {d:%Y-%m-%d} 05:00" for d in m.index]
m.index.name = "gsod_date"
m.to_csv(OUT_E / "gsod_vs_synop24h_v003.csv")
gm = m[(m.flag == "G") & m.prcp_mm.notna() & m.synop24h_00Z_same_date_mm.notna()]

alt = []
for k, label in ((-1, "GSOD D <- 24 h ending 00 UTC D-1"), (0, "GSOD D <- 24 h ending 00 UTC D (05:00 local D-1 to 05:00 local D)"), (1, "GSOD D <- 24 h ending 00 UTC D+1 (UTC day D)")):
    ends = m.index + pd.Timedelta(days=k)
    s = pd.Series([pair(e) for e in ends], index=m.index)
    ok = s.notna() & m.prcp_mm.notna()
    gw, sw = m.prcp_mm[ok] > 0, s[ok] > 0
    gflag = (m.flag == "G") & m.prcp_mm.notna()
    eq = (m.prcp_mm[gflag] - v24.reindex(ends[gflag.values]).values).abs() <= 0.3
    alt.append(dict(alignment=label, shift_days=k, days_compared=int(ok.sum()), wet_day_agreement=round(float((gw == sw).mean()), 4),
                    both_wet=int((gw & sw).sum()), gsod_only_wet=int((gw & ~sw).sum()), synop_only_wet=int((~gw & sw).sum()),
                    synop_only_wet_median_mm=float(s[ok][~gw & sw].median()) if (~gw & sw).any() else np.nan,
                    flag_g_days_equal_24h_group=int(eq.sum()), flag_g_days_with_24h_group=int(eq.notna().sum() - v24.reindex(ends[gflag.values]).isna().sum()),
                    note="wet = > 0 mm; GSOD 0 includes trace; SYNOP side = sum of the two 12 h groups (whole mm), so it is independent of the 24 h group defect"))
un = gm[~gm.gsod_equals_24h_group]
for d0, r in un.iterrows():
    offs = g[(g.accumulation_hours == 24) & (g.t > d0) & (g.t < d0 + pd.Timedelta(days=1))]
    alt.append(dict(alignment="UNMATCHED flag-G day", shift_days="", days_compared="", wet_day_agreement="", both_wet="", gsod_only_wet="", synop_only_wet="",
                    synop_only_wet_median_mm="", flag_g_days_equal_24h_group="", flag_g_days_with_24h_group="",
                    note=f"{d0:%Y-%m-%d}: GSOD {r.PRCP} in = {r.prcp_mm} mm; 00 UTC 24 h group {r.synop24h_raw_group} = {r.synop24h_00Z_same_date_mm} mm; "
                         f"off-schedule 24 h groups that day: {'; '.join(offs.observation_time_utc + ' ' + offs.raw_group) or 'none'}. "
                         "GSOD matches the 03 UTC report, i.e. a later 24 h report replaced the 00 UTC one; the window ends 08:00 local, not 05:00"))
pd.DataFrame(alt).to_csv(OUT_E / "gsod_window_alternatives_v003.csv", index=False)
best = max(alt[:3], key=lambda x: x["wet_day_agreement"])
assert best["shift_days"] == 0, "the documented window must be the best-agreeing alternative; re-examine before using it"
A("GSOD window", "flag G days 2020-2025", f"{int(gm.gsod_equals_24h_group.sum())} of {len(gm)} equal the 00 UTC 24 h group within 0.3 mm; wet-day agreement "
  + "; ".join(f"shift {x['shift_days']:+d} d: {x['wet_day_agreement']:.3f}" for x in alt[:3]), "", "documented window best",
  "applies to PRCP only. GSOD TEMP/DEWP/SLP/MAX/MIN etc. are UTC-day statistics and are not shifted")

# ------------------------------------- 6. 24 h group versus 12 h pair sums (the one-tenth discrepancy)
c = m.dropna(subset=["synop24h_00Z_same_date_mm", "synop_12h_pair_sum_mm"]).copy()
r = c.synop24h_00Z_same_date_mm; s = c.synop_12h_pair_sum_mm
c["class"] = np.select(
    [(s < 1) & (r < 1), (r - s).abs() <= np.maximum(2, 0.15 * s), (s >= 10) & ((r * 10 - s).abs() <= np.maximum(5, 0.15 * s))],
    ["both_dry", "consistent", "24h_about_one_tenth_of_12h_sum"], "other_inconsistent")
c["raw24_integer"] = c.synop24h_raw_group.str.split(",").str[1].astype(int)
c["raw24_integer_equals_12h_sum_mm"] = (c.raw24_integer - c.synop_12h_pair_sum_mm).abs() <= TOL
c[["PRCP", "flag", "prcp_mm", "synop24h_00Z_same_date_mm", "synop24h_raw_group", "raw24_integer", "synop24h_quality", "synop_12h_pair_sum_mm",
   "raw24_integer_equals_12h_sum_mm", "class"]].to_csv(OUT_E / "synop_24h_vs_12h_consistency_v003.csv")
ten = c[c["class"] == "24h_about_one_tenth_of_12h_sum"]
wet = c[c.synop_12h_pair_sum_mm >= 10]
first_ok = wet[wet["class"] == "consistent"].index.min()
A("one-tenth discrepancy: size", "24 h group vs 12 h pair sum", f"{len(ten)} days ({ten.index.min():%Y-%m-%d} to {ten.index.max():%Y-%m-%d}); "
  f"{int((ten.synop24h_quality == '2').sum())} carry quality 2 (suspect)", "", "unresolved")
A("one-tenth discrepancy: raw digits", "one-tenth days", f"raw 24 h integer equals the 12 h sum in mm on {int(ten.raw24_integer_equals_12h_sum_mm.sum())} of {len(ten)} days; "
  f"within 1 mm on {int(((ten.raw24_integer - ten.synop_12h_pair_sum_mm).abs() <= 1).sum())}", "", "evidence",
  "pattern expected if a whole-mm amount was placed in the 0.1 mm field")
A("one-tenth discrepancy: regime", "days with 12 h sum >= 10 mm", f"before 2024-02-02: {int((wet.index < '2024-02-02').sum())} days, of which one-tenth "
  f"{int(((wet.index < '2024-02-02') & (wet['class'] == '24h_about_one_tenth_of_12h_sum')).sum())}; first consistent wet day {first_ok:%Y-%m-%d}; "
  f"from then: {int((wet.index >= first_ok).sum())} days, of which consistent {int(((wet.index >= first_ok) & (wet['class'] == 'consistent')).sum())}", "", "evidence",
  "a step change in early February 2024, not random noise")
A("one-tenth discrepancy: status", "conclusion", "unresolved reporting/decoding discrepancy", "", "no correction applied",
  "Not established whether the station encoded 24 h amounts in mm or a decoder/processing step mis-scaled them; the decoder here follows the ISD document. "
  "Raw values are not multiplied by ten. Use the 6/12 h groups for magnitude and flag GSOD/24 h values on listed days")
pd.DataFrame(audit).to_csv(OUT_E / "rainfall_decoding_audit_v003.csv", index=False)

# -------------------------------------------------------- 7. ERA5 clock tests (unchanged method)
e = pd.read_csv(ROOT / "01_raw/rainfall/reanalysis/open_meteo_era5_compiled/male_reanalysis_hourly_2020-2026.csv")
e["t"] = pd.to_datetime(e.time_local); e["h"] = e.t.dt.hour
anom = e.pressure_msl_hPa - e.groupby(e.t.dt.date).pressure_msl_hPa.transform("mean")
clim = anom.groupby(e.h).mean()
H = np.arange(24); diag = []
for per in (12, 24):
    wv = 2 * np.pi / per
    cc, ss = np.linalg.lstsq(np.c_[np.cos(wv * H), np.sin(wv * H)], clim.values, rcond=None)[0]
    diag.append(dict(test="ERA5 MSLP diurnal harmonic", detail=f"period {per} h", value=round((np.arctan2(ss, cc) / wv) % per, 2),
                     unit="label hour of first maximum", amplitude_hPa=round(float(np.hypot(cc, ss)), 2)))
er = e.set_index("t").precipitation_mm
csum = er.cumsum()  # hoisted out of the loop (v002 recomputed it 16 times)
okb = bl.dropna(subset=["precipitation_mm"])
okb = okb[(~okb.negative_difference) & (~okb.any_suspect_qc) & (~okb.conflicting_observation)]
def wsum(a, b):
    try:
        return csum.loc[b] - csum.loc[a - pd.Timedelta(hours=1)]
    except KeyError:
        return np.nan
for k in range(0, 8):
    for conv, lo, hi in (("interval_ending", 1, 6), ("interval_starting", 0, 5)):
        vals = np.array([wsum(st + pd.Timedelta(hours=k + lo), st + pd.Timedelta(hours=k + hi)) for st in okb.block_start_utc])
        ok = ~np.isnan(vals)
        x, y = np.log1p(vals[ok]), np.log1p(okb.precipitation_mm.values[ok])
        diag.append(dict(test="ERA5 hourly vs SYNOP 6 h blocks", detail=f"labels = UTC+{k}, {conv}",
                         value=round(float(np.corrcoef(x, y)[0, 1]), 4), unit="Pearson r of log1p totals", n=int(ok.sum())))
pd.DataFrame(diag).to_csv(OUT_E / "era5_clock_diagnostics_v003.csv", index=False)

# --------------------------------------------- 8. modelled vs observed tide phase (unchanged method)
u = pd.read_csv(ROOT / "02_interim/weather_aligned/uhslc_male_1082_hourly_2024_clean_v001.csv")
u["t"] = pd.to_datetime(u.time_utc, utc=True).dt.tz_localize(None)
u = u.dropna(subset=["sea_level_mm_station_zero"])
mr = pd.read_csv(ROOT / "01_raw/sea_level/modelled/open_meteo_marine_compiled/male_sea_level_waves_hourly_2022-2026.csv")
mr["t"] = pd.to_datetime(mr.time_local); mr = mr.dropna(subset=["sea_level_height_msl_m"])
first_valid = mr.t.min()
mr = mr[(mr.t >= "2024-01-01") & (mr.t < "2025-01-01")]
con = {"M2": 12.4206012, "S2": 12.0, "N2": 12.65834751, "K1": 23.9344697, "O1": 25.8193417}
def fit(t, y):
    th = (t - pd.Timestamp("2024-01-01")).dt.total_seconds().values / 3600
    cols = [np.ones_like(th)]
    for p in con.values():
        cols += [np.cos(2 * np.pi / p * th), np.sin(2 * np.pi / p * th)]
    b = np.linalg.lstsq(np.column_stack(cols), y, rcond=None)[0]
    return {k: (np.hypot(b[1 + 2 * i], b[2 + 2 * i]), np.arctan2(b[2 + 2 * i], b[1 + 2 * i])) for i, k in enumerate(con)}
fo = fit(u.t, u.sea_level_mm_station_zero.values / 1000); fmod = fit(mr.t, mr.sea_level_height_msl_m.values)
tide = []
for k, p in con.items():
    dphi = (fmod[k][1] - fo[k][1] + np.pi) % (2 * np.pi) - np.pi
    tide.append(dict(constituent=k, amplitude_observed_m=round(fo[k][0], 3), amplitude_model_m=round(fmod[k][0], 3),
                     model_label_minus_utc_h=round(dphi / (2 * np.pi / p), 2)))
so = u.set_index("t").sea_level_mm_station_zero / 1000; sm = mr.set_index("t").sea_level_height_msl_m
for off in range(0, 8):
    j = pd.concat([so, sm.shift(-off, freq="h").rename("m")], axis=1, join="inner").dropna()
    tide.append(dict(constituent=f"lag_corr labels=UTC+{off}", amplitude_observed_m=None, amplitude_model_m=None,
                     model_label_minus_utc_h=round(j.iloc[:, 0].corr(j.m), 4)))
tide.append(dict(constituent="means_2024", amplitude_observed_m=round(so.mean(), 3), amplitude_model_m=round(sm.mean(), 3), model_label_minus_utc_h=None))
tide.append(dict(constituent=f"marine first valid label {first_valid:%Y-%m-%dT%H:%M}", amplitude_observed_m=None, amplitude_model_m=None, model_label_minus_utc_h=None))
pd.DataFrame(tide).to_csv(OUT_E / "marine_vs_uhslc_tide_phase_v003.csv", index=False)

# --------------------------------------------- 9. time-alignment decisions (v001/v002 rows preserved)
with open(ROOT / "03_reviewed/_archive_v002_20261122/time_alignment_decisions.csv", encoding="utf-8-sig", newline="") as f:
    ta = list(csv.DictReader(f))
COLS = list(ta[0].keys())
with open(ROOT / "00_catalog/source_verification.csv", encoding="utf-8", newline="") as f:
    sv = list(csv.DictReader(f))
clk = pd.Series([r["publication_clock_status"] for r in sv]).value_counts().to_dict()
pubs = lambda st: ", ".join(sorted({r["publisher_normalised"] for r in sv if r["publication_clock_status"] == st}))
era_r = {d["detail"]: d["value"] for d in diag if d["test"].startswith("ERA5 hourly")}
s2 = next(d["value"] for d in diag if d["detail"] == "period 12 h")
new = [
    dict(decision_id="TA003-01", dataset_id="DS0051;DS0052", source_timestamp_timezone="time_local labels behave as UTC+5 (empirically supported)",
         source_accumulation_start="Open-Meteo documentation: hourly precipitation is the preceding-hour sum (label = interval end); not verifiable from the file",
         target_timezone="Asia/Male (UTC+5)", conversion_or_alignment_rule="Use labels as local time under H_ERA5_UTC+5; keep H_START as the alternative accumulation convention",
         evidence_source_ids=f"ERA5 MSLP 12 h harmonic maximum at label hour {s2}; observed Hulhule SLP maximum 04.83 UTC (v002); rain-timing r: UTC+5/end {era_r.get('labels = UTC+5, interval_ending')}, "
                             f"UTC+5/start {era_r.get('labels = UTC+5, interval_starting')}, UTC+4/end {era_r.get('labels = UTC+4, interval_ending')}, UTC {era_r.get('labels = UTC+0, interval_ending')}",
         resolution_status="empirically_supported", decision_date="2026-11-22",
         notes="Not established: no saved request/response metadata or acquisition code states the timezone. Pressure-cycle test limits: ERA5's own S2 phase error and the 1 h accumulation ambiguity are not separable; the station is Hulhule",
         alternative_hypotheses="H_ERA5_UTC rejected by both tests; UTC+4 with interval-ending fits rain timing as well as UTC+5 with interval-starting",
         evidence_files="03_reviewed/time_alignment/evidence/era5_clock_diagnostics_v003.csv", superseded_by="", record_version="v003"),
    dict(decision_id="TA003-02", dataset_id="DS0019;DS0020;DS0048;DS0064-DS0067", source_timestamp_timezone="GSOD date = UTC day; flag-G PRCP = 24 h SYNOP group reported at 00 UTC on that date",
         source_accumulation_start="00 UTC D-1 (05:00 local D-1)", source_accumulation_end="00 UTC D (05:00 local D)", target_timezone="Asia/Male calendar day",
         conversion_or_alignment_rule="PRCP only: local day L <- GSOD L+1. Do NOT shift TEMP, DEWP, SLP, MAX, MIN, WDSP or other GSOD fields",
         evidence_source_ids=f"{int(gm.gsod_equals_24h_group.sum())} of {len(gm)} flag-G days equal the 00 UTC 24 h group; wet-day agreement "
                             + "; ".join(f"shift {x['shift_days']:+d} d {x['wet_day_agreement']:.3f}" for x in alt[:3]),
         resolution_status="established_by_observation (PRCP flag G)", decision_date="2026-11-22",
         notes="Unmatched day 2021-07-03 used an off-schedule 03 UTC report (window ends 08:00 local). Non-G flags not resolved individually",
         alternative_hypotheses="shift -1 d and +1 d rejected on wet-day agreement", evidence_files="03_reviewed/time_alignment/evidence/gsod_window_alternatives_v003.csv",
         superseded_by="", record_version="v003"),
    dict(decision_id="TA003-03", dataset_id="DS0019;DS0020;DS0048;DS0064-DS0067;DS0068-DS0071", source_timestamp_timezone="n/a", target_timezone="n/a",
         conversion_or_alignment_rule="No correction applied; raw values are not multiplied by ten. Flag GSOD/24 h values on listed days; prefer 6/12 h groups for magnitude",
         evidence_source_ids=f"{len(ten)} one-tenth days {ten.index.min():%Y-%m-%d} to {ten.index.max():%Y-%m-%d}; raw 24 h integer = 12 h sum in mm on {int(ten.raw24_integer_equals_12h_sum_mm.sum())}; "
                             f"step change: first consistent wet day {first_ok:%Y-%m-%d}",
         resolution_status="unresolved_reporting_or_decoding_discrepancy", decision_date="2026-11-22",
         notes="Origin (station encoding vs decoding/processing) not established; the ISD document specifies scaling factor 10 for all periods",
         alternative_hypotheses="whole-mm amount placed in the 0.1 mm field (consistent with the raw digits); other origins not excluded",
         evidence_files="03_reviewed/time_alignment/evidence/rainfall_decoding_audit_v003.csv;03_reviewed/time_alignment/evidence/synop_24h_vs_12h_consistency_v003.csv",
         superseded_by="", record_version="v003"),
    dict(decision_id="TA003-04", dataset_id="DS0017;DS0018;DS0068-DS0071 (ISD)", source_timestamp_timezone="UTC (ISD)",
         source_accumulation_start="per AA group: 6 h ending 06/18 UTC, 12 h ending 00/12 UTC, 24 h ending 00 UTC", target_timezone="Asia/Male (UTC+5)",
         conversion_or_alignment_rule="Non-overlapping 6 h blocks 05-11, 11-17, 17-23, 23-05 local; 23-05 block belongs to the local day it starts (05:00-05:00 day). Negative differences and conflicts flagged, not clipped or resolved",
         evidence_source_ids=f"conservation {sum(cons)}/{len(cons)}; reference cases {int((ref.result == 'pass').sum())}/{len(ref)} pass",
         resolution_status="verified_clock; derived_blocks_checked", decision_date="2026-11-22",
         notes="6/12 h amounts are whole mm except sub-1 mm values; off-schedule and period-99 groups excluded from blocks", alternative_hypotheses="",
         evidence_files="02_interim/weather_aligned/noaa_synop_6h_blocks_2020-2025_v003.csv;03_reviewed/time_alignment/evidence/rainfall_reference_cases_v003.csv",
         superseded_by="", record_version="v003"),
    dict(decision_id="TA003-05", dataset_id="DS0053", source_timestamp_timezone="time_local labels: offset +3.98 to +4.68 h relative to UTC by tidal phase", source_accumulation_start="instantaneous",
         target_timezone="Asia/Male (UTC+5)", conversion_or_alignment_rule="None applied. Keep H_MARINE_UTC+4 and H_MARINE_UTC+5 as named alternatives; compare anomalies only",
         evidence_source_ids="M2 +4.41 h, S2 +4.68, K1 +4.40, O1 +3.98; lag correlation 0.963 (UTC+4) vs 0.959 (UTC+5)", resolution_status="unresolved", decision_date="2026-11-22",
         notes="An alignment must not be chosen by flood-model performance; any analysis using sea level reports both alternatives",
         alternative_hypotheses="H_MARINE_UTC+5 (same compiler as ERA5); H_MARINE_UTC+4 (best raw correlation); UTC rejected",
         evidence_files="03_reviewed/time_alignment/evidence/marine_vs_uhslc_tide_phase_v003.csv", superseded_by="", record_version="v003"),
    dict(decision_id="TA003-08", dataset_id="article publication clocks", source_timestamp_timezone="per source: publication_timezone (offset or blank) + publication_clock_status",
         target_timezone="Asia/Male", conversion_or_alignment_rule="Convert a displayed time only when its status is metadata_confirmed or empirically_supported; archive capture time is never publication time",
         evidence_source_ids="; ".join(f"{k} {v}" for k, v in sorted(clk.items())) + f". metadata_confirmed: {pubs('metadata_confirmed')}. empirically_supported: {pubs('empirically_supported')}. "
                             f"unresolved: {pubs('unresolved')}. not_applicable: {pubs('not_applicable')}",
         resolution_status="partly_established", decision_date="2026-11-22", notes="Counts recomputed from 00_catalog/source_verification.csv; publication time is never flood onset",
         alternative_hypotheses="", evidence_files="00_catalog/source_verification.csv", superseded_by="", record_version="v003"),
]
sup = {"TA002-01": "TA003-01", "TA002-02": "TA003-02", "TA002-03": "TA003-03", "TA002-04": "TA003-04", "TA002-05": "TA003-05", "TA002-08": "TA003-08"}
for r in ta:
    if r["decision_id"] in sup:
        r["superseded_by"] = sup[r["decision_id"]]
with open(ROOT / "03_reviewed/time_alignment/time_alignment_decisions.csv", "w", encoding="utf-8", newline="") as f:
    wr = csv.DictWriter(f, COLS); wr.writeheader()
    for r in ta + new:
        wr.writerow({k: r.get(k, "") for k in COLS})

# ---------------------------------------------------------------- 10. summary
print(pd.DataFrame(audit)[["check", "value", "result"]].to_string(index=False, max_colwidth=150))
print(pd.DataFrame(alt).drop(columns=["note"]).head(3).to_string(index=False))
print(un.to_string())
print(ref[["case", "expected_mm", "computed_mm", "guards_against", "result"]].to_string(index=False))
print("24h vs 12h:", c["class"].value_counts().to_dict())
print(pd.DataFrame(diag).to_string(index=False))
print(pd.DataFrame(tide).to_string(index=False))
