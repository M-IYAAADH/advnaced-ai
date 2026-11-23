"""Weather/sea-level clock and accumulation-window audit (v002, 22 Nov 2026).

Reads raw NOAA ISD (global hourly) and GSOD files for station 43555099999
(Hulhule), the compiled Open-Meteo ERA5 and marine files, and the UHSLC clean
copy. Writes evidence tables only. No raw file is modified, no series is
shifted in place and nothing here is a model input.

Usage:  python audit_weather_clocks_v002.py <male_flood_ai_data root>
"""
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

# ---------------------------------------------------------------- 1. ISD groups
rows = []
for y in YEARS:
    h = pd.read_csv(ST / f"noaa_global_hourly_{y}_43555099999.csv", dtype=str, low_memory=False)
    for c in [c for c in h.columns if c.startswith("AA")]:
        s = h[h[c].notna()]
        for date, rtype, grp in zip(s.DATE, s.REPORT_TYPE, s[c]):
            p = grp.split(",")
            if len(p) != 4:
                continue
            period = None if p[0] == "99" else int(p[0])
            mm = None if p[1] == "9999" else int(p[1]) / 10.0
            rows.append(dict(observation_time_utc=date + "Z", report_type=rtype, field=c, raw_group=grp,
                             accumulation_hours=period, precipitation_mm=mm, condition_code=p[2], quality_code=p[3]))
g = pd.DataFrame(rows)
g["t"] = pd.to_datetime(g.observation_time_utc.str.rstrip("Z"))
g["window_start_local"] = (g.t - pd.to_timedelta(g.accumulation_hours, unit="h") + LOCAL).dt.strftime("%Y-%m-%dT%H:%M")
g["window_end_local"] = (g.t + LOCAL).dt.strftime("%Y-%m-%dT%H:%M")
g["quality_meaning"] = g.quality_code.map({"0": "passed gross limits", "1": "passed all QC", "2": "suspect",
                                           "3": "erroneous", "9": "passed gross limits if present"}).fillna("see ISD doc")
g.drop(columns="t").to_csv(OUT_I / "noaa_synop_precip_groups_2020-2025_v002.csv", index=False)

# --------------------------------------------------- 2. non-overlapping 6 h blocks
fm = g[(g.report_type == "FM-12") & g.precipitation_mm.notna()]
def grp(hours, hour):
    s = fm[(fm.accumulation_hours == hours) & (fm.t.dt.hour == hour)]
    return s.groupby("t").agg(mm=("precipitation_mm", "first"), q=("quality_code", "first"))
g6_06, g12_12, g6_18, g12_00, g24_00 = grp(6, 6), grp(12, 12), grp(6, 18), grp(12, 0), grp(24, 0)
blocks = []
for day in pd.date_range(f"{YEARS[0]}-01-01", f"{YEARS[-1]}-12-31"):
    t06, t12, t18, t24 = (day + pd.Timedelta(hours=h) for h in (6, 12, 18, 24))
    def val(tab, t):
        return (tab.loc[t, "mm"], tab.loc[t, "q"]) if t in tab.index else (np.nan, "")
    a, qa = val(g6_06, t06); b12, qb = val(g12_12, t12); c, qc = val(g6_18, t18); d12, qd = val(g12_00, t24)
    for start, mm, how, q in (
        (day, a, "6h group ending 06Z", qa),
        (t06, b12 - a if pd.notna(b12) and pd.notna(a) else np.nan, "12h group ending 12Z minus 6h ending 06Z", f"{qb}/{qa}"),
        (t12, c, "6h group ending 18Z", qc),
        (t18, d12 - c if pd.notna(d12) and pd.notna(c) else np.nan, "12h group ending 00Z(next) minus 6h ending 18Z", f"{qd}/{qc}"),
    ):
        blocks.append(dict(block_start_utc=start, block_end_utc=start + pd.Timedelta(hours=6), precipitation_mm=mm,
                           derivation=how, quality_codes=q, negative_difference=bool(pd.notna(mm) and mm < 0)))
bl = pd.DataFrame(blocks)
bl["block_start_local"] = (bl.block_start_utc + LOCAL).dt.strftime("%Y-%m-%dT%H:%M")
bl["block_end_local"] = (bl.block_end_utc + LOCAL).dt.strftime("%Y-%m-%dT%H:%M")
bl["any_suspect_qc"] = bl.quality_codes.str.contains("2")
out_bl = bl.assign(block_start_utc=bl.block_start_utc.dt.strftime("%Y-%m-%dT%H:%MZ"),
                   block_end_utc=bl.block_end_utc.dt.strftime("%Y-%m-%dT%H:%MZ"))
out_bl.to_csv(OUT_I / "noaa_synop_6h_blocks_2020-2025_v002.csv", index=False)

# ----------------------------------------------- 3. GSOD versus the 24 h group
gs = pd.concat([pd.read_csv(ST / f"noaa_gsod_{y}_43555099999.csv", dtype=str) for y in YEARS])
gs["d"] = pd.to_datetime(gs.DATE)
gs["prcp_in"] = pd.to_numeric(gs.PRCP)
gs["flag"] = gs.PRCP_ATTRIBUTES.str.strip()
gs["prcp_mm"] = np.where(gs.prcp_in >= 99.99, np.nan, (gs.prcp_in * 25.4).round(1))
a24 = g24_00.copy(); a24.index = a24.index.normalize()
s12 = (g12_12.mm.rename("m12").reindex(a24.index - pd.Timedelta(hours=12)).set_axis(a24.index)
       + g12_00.mm.reindex(a24.index.map(lambda x: x)).set_axis(a24.index))
m = gs.set_index("d")[["PRCP", "flag", "prcp_mm"]].join(a24.rename(columns={"mm": "synop24h_00Z_same_date_mm", "q": "synop24h_quality"}))
m["synop_12h_pair_sum_mm"] = s12
m["gsod_equals_24h_group"] = (m.prcp_mm - m.synop24h_00Z_same_date_mm).abs() <= 0.3
m["window_local"] = [f"{(d - pd.Timedelta(days=1)):%Y-%m-%d} 05:00 to {d:%Y-%m-%d} 05:00" for d in m.index]
m.index.name = "gsod_date"
m.to_csv(OUT_E / "gsod_vs_synop24h_v002.csv")
gm = m[(m.flag == "G") & m.prcp_mm.notna() & m.synop24h_00Z_same_date_mm.notna()]

# ------------------------------------------ 4. 24 h group versus 12 h pair sums
c = m.dropna(subset=["synop24h_00Z_same_date_mm", "synop_12h_pair_sum_mm"]).copy()
r = c.synop24h_00Z_same_date_mm; s = c.synop_12h_pair_sum_mm
c["class"] = np.select(
    [(s < 1) & (r < 1), (r - s).abs() <= np.maximum(2, 0.15 * s), (s >= 10) & ((r * 10 - s).abs() <= np.maximum(5, 0.15 * s))],
    ["both_dry", "consistent", "24h_about_one_tenth_of_12h_sum"], "other_inconsistent")
c[["PRCP", "flag", "prcp_mm", "synop24h_00Z_same_date_mm", "synop24h_quality", "synop_12h_pair_sum_mm", "class"]] \
    .to_csv(OUT_E / "synop_24h_vs_12h_consistency_v002.csv")

# -------------------------------------------------------- 5. ERA5 clock tests
e = pd.read_csv(ROOT / "01_raw/rainfall/reanalysis/open_meteo_era5_compiled/male_reanalysis_hourly_2020-2026.csv")
e["t"] = pd.to_datetime(e.time_local); e["h"] = e.t.dt.hour
anom = e.pressure_msl_hPa - e.groupby(e.t.dt.date).pressure_msl_hPa.transform("mean")
clim = anom.groupby(e.h).mean()
H = np.arange(24); diag = []
for per in (12, 24):
    w = 2 * np.pi / per
    cc, ss = np.linalg.lstsq(np.c_[np.cos(w * H), np.sin(w * H)], clim.values, rcond=None)[0]
    diag.append(dict(test="ERA5 MSLP diurnal harmonic", detail=f"period {per} h", value=round((np.arctan2(ss, cc) / w) % per, 2),
                     unit="label hour of first maximum", amplitude_hPa=round(float(np.hypot(cc, ss)), 2)))
er = e.set_index("t").precipitation_mm
okb = bl.dropna(subset=["precipitation_mm"])
okb = okb[(~okb.negative_difference) & (~okb.any_suspect_qc)]
for k in range(0, 8):
    for conv, lo, hi in (("interval_ending", 1, 6), ("interval_starting", 0, 5)):
        idx = [(st + pd.Timedelta(hours=k + lo), st + pd.Timedelta(hours=k + hi)) for st in okb.block_start_utc]
        csum = er.cumsum()
        def wsum(a, b):
            try:
                return csum.loc[b] - csum.loc[a - pd.Timedelta(hours=1)]
            except KeyError:
                return np.nan
        vals = np.array([wsum(a, b) for a, b in idx])
        ok = ~np.isnan(vals)
        x, y = np.log1p(vals[ok]), np.log1p(okb.precipitation_mm.values[ok])
        diag.append(dict(test="ERA5 hourly vs SYNOP 6 h blocks", detail=f"labels = UTC+{k}, {conv}",
                         value=round(float(np.corrcoef(x, y)[0, 1]), 4), unit="Pearson r of log1p totals", n=int(ok.sum())))
pd.DataFrame(diag).to_csv(OUT_E / "era5_clock_diagnostics_v002.csv", index=False)

# -------------------------------------------- 6. modelled vs observed tide phase
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
tide.append(dict(constituent="means_2024", amplitude_observed_m=round(so.mean(), 3), amplitude_model_m=round(sm.mean(), 3),
                 model_label_minus_utc_h=None))
tide.append(dict(constituent=f"marine first valid label {first_valid:%Y-%m-%dT%H:%M}", amplitude_observed_m=None,
                 amplitude_model_m=None, model_label_minus_utc_h=None))
pd.DataFrame(tide).to_csv(OUT_E / "marine_vs_uhslc_tide_phase_v002.csv", index=False)

# ---------------------------------------------------------------- 7. summary
print(f"ISD groups parsed: {len(g)}; FM-12 with depth: {len(fm)}")
print(f"6h blocks: {len(bl)}; with value: {bl.precipitation_mm.notna().sum()}; negative differences: {bl.negative_difference.sum()}")
print(f"GSOD days: {len(m)}; flag G with 24h group: {len(gm)}; exact (<=0.3 mm): {gm.gsod_equals_24h_group.sum()}")
print("flags:", m.flag.value_counts(dropna=False).to_dict())
print("24h vs 12h:", c["class"].value_counts().to_dict())
print(c[c["class"].isin(["24h_about_one_tenth_of_12h_sum", "other_inconsistent"])]
      [["prcp_mm", "synop24h_00Z_same_date_mm", "synop24h_quality", "synop_12h_pair_sum_mm", "class"]].to_string())
print(pd.DataFrame(diag).to_string(index=False))
print(pd.DataFrame(tide).to_string(index=False))
