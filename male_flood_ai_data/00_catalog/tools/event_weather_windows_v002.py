"""Per-event weather windows and coverage under each documented alignment (v002).

Reads the v002 reviewed events and the v002 SYNOP blocks/GSOD evidence. Nothing is
shifted in the source files; each alignment is a named column so results under
different hypotheses can be compared. No labels are created for unreported days.

Usage:  python event_weather_windows_v002.py <male_flood_ai_data root>
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(sys.argv[1])
EV = pd.read_csv(ROOT / "03_reviewed/events/flood_events.csv", dtype=str)
BL = pd.read_csv(ROOT / "02_interim/weather_aligned/noaa_synop_6h_blocks_2020-2025_v002.csv")
BL["start_local"] = pd.to_datetime(BL.block_start_local)
GS = pd.read_csv(ROOT / "03_reviewed/time_alignment/evidence/gsod_vs_synop24h_v002.csv", parse_dates=["gsod_date"]).set_index("gsod_date")
CONS = pd.read_csv(ROOT / "03_reviewed/time_alignment/evidence/synop_24h_vs_12h_consistency_v002.csv", parse_dates=["gsod_date"]).set_index("gsod_date")["class"]
ER = pd.read_csv(ROOT / "01_raw/rainfall/reanalysis/open_meteo_era5_compiled/male_reanalysis_hourly_2020-2026.csv")
ER["t"] = pd.to_datetime(ER.time_local); er = ER.set_index("t").precipitation_mm
MR = pd.read_csv(ROOT / "01_raw/sea_level/modelled/open_meteo_marine_compiled/male_sea_level_waves_hourly_2022-2026.csv")
MR["t"] = pd.to_datetime(MR.time_local); mr = MR.set_index("t").sea_level_height_msl_m
UH = pd.read_csv(ROOT / "02_interim/weather_aligned/uhslc_male_1082_hourly_2024_clean_v001.csv")
UH["t"] = pd.to_datetime(UH.time_utc, utc=True).dt.tz_localize(None) + pd.Timedelta(hours=5)  # UTC verified -> local
uh = UH.set_index("t").sea_level_mm_station_zero

def synop_day(day):
    """Local day D measured 05:00 D to 05:00 D+1 (the four UTC-aligned 6 h blocks)."""
    b = BL[(BL.start_local >= day + pd.Timedelta(hours=5)) & (BL.start_local < day + pd.Timedelta(hours=29))]
    vals = [f"{r.block_start_local[11:16]}-{r.block_end_local[11:16]} {'' if pd.isna(r.precipitation_mm) else r.precipitation_mm}{'(q2)' if r.any_suspect_qc else ''}"
            for r in b.itertuples()]
    total = b.precipitation_mm.sum() if len(b) == 4 and b.precipitation_mm.notna().all() and not b.negative_difference.any() else np.nan
    return "; ".join(vals), total, len(b) == 4 and b.precipitation_mm.notna().all()

def gsod(day):
    if day not in GS.index: return np.nan, "", ""
    r = GS.loc[day]
    return r.prcp_mm, r.flag if isinstance(r.flag, str) else "", CONS.get(day, "")

rows = []
for e in EV.itertuples():
    for day in pd.date_range(e.event_start_date, e.event_end_date):
        if day < pd.Timestamp("2020-01-01"): continue
        txt, tot, complete = synop_day(day)
        g0, f0, c0 = gsod(day); g1, f1, c1 = gsod(day + pd.Timedelta(days=1))
        lab = er.loc[day: day + pd.Timedelta(hours=23)]
        utc_hyp = er.loc[day - pd.Timedelta(hours=5): day + pd.Timedelta(hours=18)]  # if labels were UTC (rejected)
        m = mr.loc[day: day + pd.Timedelta(hours=23)].dropna()
        u = uh.loc[day: day + pd.Timedelta(hours=23)].dropna()
        rows.append(dict(event_id=e.event_id, decision=e.decision, local_date=f"{day:%Y-%m-%d}",
                         synop_blocks_local=txt, synop_local_day_0500_0500_mm=tot, synop_complete=complete,
                         gsod_shifted_date=f"{day + pd.Timedelta(days=1):%Y-%m-%d}", gsod_shifted_mm=g1, gsod_shifted_flag=f1, gsod_shifted_24h_check=c1,
                         gsod_as_labelled_mm=g0, gsod_as_labelled_flag=f0, gsod_as_labelled_24h_check=c0,
                         era5_labels_utc5_daily_mm=round(lab.sum(), 1) if len(lab) == 24 else np.nan, era5_labels_utc5_max1h_mm=lab.max() if len(lab) else np.nan,
                         era5_if_labels_utc_daily_mm_REJECTED=round(utc_hyp.sum(), 1) if len(utc_hyp) == 24 else np.nan,
                         marine_sea_level_max_m_labels_as_given=m.max() if len(m) else np.nan, marine_hours=len(m),
                         uhslc_max_mm_station_zero_local_day=u.max() if len(u) else np.nan, uhslc_hours=len(u)))
W = pd.DataFrame(rows)
W.to_csv(ROOT / "03_reviewed/time_alignment/evidence/event_weather_windows_v002.csv", index=False)

# coverage by alignment for accepted rain events in the study period
acc = W[W.decision == "accepted_reported_rain_event"]
ev_any = acc.groupby("event_id")
cov = []
def add(alignment, status, n, note=""): cov.append(dict(alignment=alignment, status=status, accepted_rain_events_covered=n, accepted_rain_events_total=ev_any.ngroups, note=note))
add("ERA5 labels = UTC+5, local day as labelled", "established by observation (pressure-tide phase)", int(ev_any.era5_labels_utc5_daily_mm.apply(lambda s: s.notna().any()).sum()))
add("ERA5 labels = UTC", "rejected", int(ev_any.era5_if_labels_utc_daily_mm_REJECTED.apply(lambda s: s.notna().any()).sum()), "shown for sensitivity only")
add("SYNOP 6 h blocks, local 05:00-05:00, complete", "clock verified (UTC); blocks derived", int(ev_any.synop_complete.apply(any).sum()), "station on Hulhule, ends 2025-08-24")
add("GSOD shifted (local day D <- GSOD D+1)", "established by observation (24 h group ending 00 UTC)", int(ev_any.gsod_shifted_mm.apply(lambda s: s.notna().any()).sum()))
n_def = int(acc[acc.gsod_shifted_24h_check == "24h_about_one_tenth_of_12h_sum"].event_id.nunique())
add("GSOD shifted, excluding days where the 24 h group is about one-tenth", "data-quality filter", int(ev_any.gsod_shifted_mm.apply(lambda s: s.notna().any()).sum()) - n_def,
    f"{n_def} events fall on a one-tenth day")
add("GSOD as labelled (local day D <- GSOD D)", "rejected", int(ev_any.gsod_as_labelled_mm.apply(lambda s: s.notna().any()).sum()), "wrong window; kept for comparison with v001")
add("Modelled sea level (labels UTC+4 or UTC+5; hypotheses unresolved)", "unresolved clock; model datum", int(ev_any.marine_hours.apply(lambda s: (s > 0).any()).sum()),
    "available from label 2022-11-23T05:00; same days under either hypothesis except edges")
add("UHSLC observed (UTC verified, station zero)", "verified", int(ev_any.uhslc_hours.apply(lambda s: (s > 0).any()).sum()), "2024 only")
pd.DataFrame(cov).to_csv(ROOT / "03_reviewed/time_alignment/evidence/coverage_by_alignment_v002.csv", index=False)
print(pd.DataFrame(cov).to_string(index=False))

# daily coverage v002 (local days); labels only from accepted reviewed events; everything else unlabelled
days = pd.date_range("2020-01-01", "2026-11-13")
lab = {}
for e in EV.itertuples():
    for dd in pd.date_range(e.event_start_date, e.event_end_date):
        lab.setdefault(dd, []).append(f"{e.event_id}:{e.decision}")
blk = BL.assign(local_day=(BL.start_local - pd.Timedelta(hours=5)).dt.normalize()).groupby("local_day").agg(
    n=("precipitation_mm", lambda s: s.notna().sum()), neg=("negative_difference", "any"))
out = pd.DataFrame(index=days)
out["era5_labels_utc5_complete"] = [len(er.loc[d: d + pd.Timedelta(hours=23)]) == 24 for d in days]
out["synop_blocks_complete"] = [(d in blk.index) and blk.loc[d, "n"] == 4 and not blk.loc[d, "neg"] for d in days]
gsd = GS.prcp_mm
out["gsod_for_local_day_available"] = [pd.notna(gsd.get(d + pd.Timedelta(days=1), np.nan)) for d in days]
out["gsod_for_local_day_24h_one_tenth"] = [CONS.get(d + pd.Timedelta(days=1), "") == "24h_about_one_tenth_of_12h_sum" for d in days]
mday = mr.dropna().groupby(mr.dropna().index.normalize()).size()
out["marine_complete_labels_as_given"] = [mday.get(d, 0) == 24 for d in days]
uday = uh.dropna().groupby(uh.dropna().index.normalize()).size()
out["uhslc_complete_local_day"] = [uday.get(d, 0) == 24 for d in days]
out["reported_events"] = [";".join(lab.get(d, [])) for d in days]
def status(v):
    if not v: return "unlabelled"
    if any(x.endswith(("accepted_reported_rain_event", "accepted_reported_coastal_event")) for x in v.split(";")): return "reported_event_day (see decision; windows are not daily positives)"
    return "uncertain_reported"
out["label_status"] = out.reported_events.map(status)
out.index.name = "local_date"
out.to_csv(ROOT / "02_interim/weather_aligned/daily_series_coverage_2020-2026_v002.csv")
print(out.label_status.value_counts().to_dict())
print(out.drop(columns=["reported_events", "label_status"]).sum().to_dict())
