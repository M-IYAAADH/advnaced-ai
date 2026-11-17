"""MF-44: descriptive rainfall table for the 18 reported rain-flood incidents.

Reads only male-flood-basis/data. Reported figures are copied verbatim and kept
apart from the two gridded/station series, which are added as context columns.
No series is merged, averaged or used to define a threshold.
Run from the project root: python3 -I scripts/build_incident_rainfall_table.py
"""
import csv
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "male-flood-basis" / "data"
OUT = ROOT / "derived"

# Dates the incident text covers (calendar days, local). Range ids use the last day.
COVER = {"2023-12-31": ["2023-12-30", "2023-12-31"], "2024-12-20": ["2024-12-20", "2024-12-21"],
         "2025-01-03": ["2025-01-02", "2025-01-03"], "2025-03-11": ["2025-03-11", "2025-03-12"]}
# Stated accumulation period of the reported Malé figure, only where the source text gives one.
PERIOD = {"2023-12-31": "unknown for Malé (24 h is stated for the Hulhulé figure only)", "2024-08-13": "8am to 8am, calendar dates not stated",
          "2024-12-20": "8am Fri to 8am Sat (24 h)", "2025-01-03": "not stated (alternative count: 162 mm by 11pm)",
          "2026-10-21": "24 h (window not stated)"}

def num(x):
    return float(x) if x not in ("", None) else None

def main():
    feat = {r["date"]: r for r in csv.DictReader(open(D / "male_daily_features_with_flood_labels.csv", encoding="utf-8"))}
    stn = {r["date"]: r for r in csv.DictReader(open(D / "hulhule_station_daily_2020-2025.csv", encoding="utf-8"))}
    rows = []
    for r in csv.DictReader(open(D / "flood_incidents_greater_male_2021-2026.csv", encoding="utf-8")):
        iid = r["incident_id"]
        days = COVER.get(iid, [iid])
        def fmt(f):
            return "; ".join(f"{d}={f(d)}" for d in days)
        def era(d): return feat[d]["rain_mm_reanalysis"] if d in feat else "no row"
        def era1h(d): return feat[d]["max_1h_rain_mm"] if d in feat else "no row"
        def gs(d):
            s = stn.get(d)
            if not s: return "no row"
            return (s["precip_mm"] or "missing") + (f" (flag {s['precip_flag']})" if s["precip_flag"] else "")
        reported = r["reported_rainfall"].strip()
        rows.append({
            "incident_id": iid, "dates_text": r["dates"], "days_covered": " ".join(days),
            "reported_rainfall_verbatim": reported,
            "reported_male_mm": r["male_reported_mm"] or "",
            "reported_period": PERIOD.get(iid, "not stated" if r["male_reported_mm"] else ""),
            "reported_status": "figure_reported" if r["male_reported_mm"] else "no_figure_in_compilation",
            "era5_daily_mm_by_day": fmt(era), "era5_max_1h_mm_by_day": fmt(era1h),
            "hulhule_gsod_daily_mm_by_day": fmt(gs),
            "source_urls": r["source_urls"],
        })
    OUT.mkdir(exist_ok=True)
    with open(OUT / "incident_rainfall_table.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(len(rows), "incidents;", sum(r["reported_status"] == "figure_reported" for r in rows), "with a reported Malé figure")

if __name__ == "__main__":
    main()
