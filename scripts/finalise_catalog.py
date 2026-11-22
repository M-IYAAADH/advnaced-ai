"""Add curated column descriptions to 00_catalog/data_dictionary.csv and inventory rows for the
tables written by reconcile_flood_inventory.py. Idempotent. Run after the reconciliation.
    python scripts/finalise_catalog.py --dest ../male_flood_ai_data
"""
import argparse, hashlib
from pathlib import Path

import pandas as pd

IMPORT = {
    "record_id": "Stable ID from the export (RAINnnn news rain window, COASTnnn coastal window, OFFnnn official lead).",
    "event_start_date": "First reported date of the window, Male local calendar date as interpreted by the exporter.",
    "event_end_date": "Last reported date (inclusive). A multi-day window does not confirm flooding on every day.",
    "record_category": "news_rain_window, news_coastal_window or official_record_lead.",
    "flood_type": "rain_associated = reported association with rain, not proven single cause; coastal_swell.",
    "geographic_scope": "Scope asserted by the exporter; not independently verified here.",
    "reported_timing": "Free-text timing summary from the source.",
    "flood_onset_time_local": "Measured flood onset; empty in all rows (unknown).",
    "rain_start_time_local": "Reported rain-start clock (local, HH:MM); read together with the qualifier.",
    "rain_start_time_qualifier": "approximately / after; must be kept with the clock.",
    "response_start_time_local": "Reported start of pumping/response; not flood onset.",
    "event_time_notes": "Exporter notes on clocks and timezone.",
    "source_name": "Publisher or agency.", "source_language": "en, dv (Dhivehi/Thaana) or dv_en.",
    "source_title": "Original title; Thaana preserved.", "source_url": "Primary source URL.",
    "source_publication_date_as_displayed": "Publication date as printed (not event date).",
    "source_publication_time_as_displayed": "Publication clock as printed; timezone unknown.",
    "source_publication_timezone": "Always 'unknown' in the export.",
    "additional_source_url": "Second source URL, if any.",
    "additional_source_publication_date_as_displayed": "As printed.", "additional_source_publication_time_as_displayed": "As printed.",
    "review_status": "Exporter's status; none are accepted labels.", "review_notes": "Exporter's review notes (conflicts, caveats).",
    "storm_group_id": "Empty in all rows: storm grouping unresolved.", "independent_storm_status": "'unresolved' in all rows.",
    "training_label_status": "'pending_review_not_final_label' in all rows.",
    "date_window_interpretation": "How the date window should be read (reported date vs combined window).",
    "record_provenance": "Export provenance statement.", "export_date": "Date of export (2026-11-22).",
}
CLEAN_EXTRA = {
    "event_start_date_valid_iso": "True if event_start_date parses as YYYY-MM-DD.", "event_end_date_valid_iso": "True if event_end_date parses as YYYY-MM-DD.",
    "window_days": "Inclusive length of the date window.", "publication_minus_event_start_days": "Primary publication date minus event start (days); blank if no date printed.",
    "end_before_start": "True if end precedes start (data error).", "multi_day_window_not_daily_truth": "True for windows longer than one day.",
    "rain_start_time_with_qualifier": "Qualifier + clock kept together, e.g. 'after 13:00'.",
}
RECON = {
    "imported_record_id": "Imported record ID; blank for existing records absent from the import.",
    "record_category": "As imported, or existing_not_in_import.", "imported_start": "Window start.", "imported_end": "Window end.",
    "window_days": "Inclusive window length.", "flood_type_as_imported": "Imported flood_type.",
    "proposed_classification": "rain / coastal / mixed / uncertain: proposal for human review, not a label.",
    "imported_source_ids": "source_register IDs for primary and additional URLs.",
    "match_type": "exact_match_with_compiled_incident, date_overlap_possible_duplicate, matches_non_compiled_lead_only, nearby_dates_possible_same_storm, no_existing_match, existing_only.",
    "matched_compiled_incidents": "male-flood-basis incidents overlapping (or same article within 3 days), with legacy decision and storm proxy.",
    "matched_starter_pack_leads": "Starter-pack flood/event_candidates.csv leads matched.",
    "matched_groundsource_windows": "Groundsource review comparison windows matched (date overlap or same article).",
    "same_article_as": "Existing records citing the same article (host family + article number), dates within 3 days.",
    "nearby_records_1_3_days": "Records 1-3 days apart: possible same storm, not merged.",
    "new_candidate_dates_vs_compiled": "Window days not covered by any compiled incident.",
    "conflicts": "Recorded contradictions that must stay visible.",
    "era5_daily_mm_context": "ERA5 daily total (nominal day, Male grid point) for window +/-1 day. Context only, not validation.",
    "hulhule_gsod_mm_context": "Hulhule GSOD daily precip mm (flag) for window +/-1 day; station not on Male; day boundary unverified.",
    "evidence_available": "Evidence already in the project.", "checks_required": "Checks before any label decision.",
    "proposed_action": "Proposed next action.", "justification": "Reason for the proposed action.",
    "training_label_status": "Copied from import; none promoted.", "imported_review_status": "Copied.", "imported_review_notes": "Copied.",
    "reported_timing": "Copied.", "rain_start_time_local": "Qualifier + clock.", "response_start_time_local": "Copied.",
    "flood_onset_time_local": "'unknown' where the import had none.",
}
KEY = {
    ("male_reanalysis_hourly", "time_local"): "Hour label written by the compiler; UTC offset undocumented.",
    ("male_reanalysis_hourly", "precipitation_mm"): "ERA5 hourly precipitation (Open-Meteo: preceding-hour sum); mm; identical to rain_mm.",
    ("male_sea_level_waves", "sea_level_height_msl_m"): "Modelled sea level incl. tide, m relative to model MSL; blank before 2022-11-23T05:00 and in 3 gaps.",
    ("noaa_gsod_", "PRCP"): "Daily precipitation, inches; 99.99 = missing.", ("noaa_gsod_", "PRCP_ATTRIBUTES"): "NOAA precipitation flag letter A-I.",
    ("noaa_gsod_", "DATE"): "GSOD date; local-day alignment unverified.",
    ("UHSLC_", "sea_level"): "Hourly sea level, mm relative to station zero; blank = missing (units row skipped).",
    ("UHSLC_", "time"): "UTC timestamp.",
    ("hulhule_station_daily", "precip_mm"): "GSOD PRCP converted to mm by the compiler; blank = missing.",
    ("male_daily_features_with_flood_labels", "flood_reported"): "1 = compiled report; 0 = no report found (NOT observed dry).",
    ("prcp_mm", "prcp_mm"): "PRCP x 25.4, rounded 0.1 mm; blank where PRCP is 99.99.",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dest", required=True)
    dest = Path(ap.parse_args().dest).resolve()
    cat = dest / "00_catalog"
    rd = lambda p: pd.read_csv(p, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    inv, dd = rd(cat / "dataset_inventory.csv"), rd(cat / "data_dictionary.csv")

    new = [("02_interim/event_candidates/inventory_reconciliation.csv", "Reconciliation of the 30 imported records with existing inventories", RECON),
           ("02_interim/event_candidates/event_candidates.csv", "Unverified candidates: 30 imported + 18 compiled + 3 starter-pack leads", {}),
           ("03_reviewed/storm_groups/storm_groups.csv", "Legacy storm proxies S01-S17 (not verified storms)", {}),
           ("03_reviewed/time_alignment/time_alignment_decisions.csv", "Timezone/accumulation register; mostly unresolved", {})]
    n = max(int(x[2:]) for x in inv.dataset_id)
    for rel, desc, cols in new:
        p = dest / rel
        d = rd(p)
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        if rel in set(inv.relative_path):
            inv.loc[inv.relative_path == rel, ["sha256", "row_count"]] = [h, str(len(d))]
            dsid = inv.loc[inv.relative_path == rel, "dataset_id"].iloc[0]
        else:
            n += 1
            dsid = f"DS{n:04d}"
            inv.loc[len(inv)] = {**{c: "" for c in inv.columns}, "dataset_id": dsid, "relative_path": rel, "original_filename": p.name,
                                 "provider": "This organisation step (scripts/reconcile_flood_inventory.py)", "source_type": "review_working_table",
                                 "variables": ";".join(d.columns), "row_count": str(len(d)), "column_count": str(d.shape[1]), "format": "CSV",
                                 "sha256": h, "size_bytes": str(p.stat().st_size), "inventory_status": "imported", "data_nature": "derived",
                                 "notes": desc, "profiling_completeness": "complete"}
        for c in d.columns:
            if not ((dd.dataset_id == dsid) & (dd.column_name == c)).any():
                dd.loc[len(dd)] = {**{k: "" for k in dd.columns}, "dataset_id": dsid, "column_name": c, "relative_path": rel,
                                   "description": cols.get(c, ""), "data_type": "text",
                                   "missing_value_meaning": f"blank in {int((d[c] == '').sum())} of {len(d)} rows"}

    path_of = dict(zip(inv.dataset_id, inv.relative_path))
    for i, r in dd.iterrows():
        path = path_of.get(r.dataset_id, "")
        desc = ""
        if path.endswith("male_flood_inventory.csv") or path.endswith("male_flood_inventory_clean_v001.csv"):
            desc = IMPORT.get(r.column_name) or CLEAN_EXTRA.get(r.column_name, "")
        elif path.endswith("inventory_reconciliation.csv"):
            desc = RECON.get(r.column_name, "")
        for (frag, col), txt in KEY.items():
            if (frag in path or frag == col) and r.column_name == col:
                desc = txt
        if desc and not r.description:
            dd.at[i, "description"] = desc
        if not dd.at[i, "description"]:
            dd.at[i, "description"] = "not documented in source; see dataset notes"
    inv.to_csv(cat / "dataset_inventory.csv", index=False, encoding="utf-8-sig")
    dd.to_csv(cat / "data_dictionary.csv", index=False, encoding="utf-8-sig")
    print("inventory rows", len(inv), "| dictionary rows", len(dd), "| curated", int((~dd.description.str.startswith("not documented")).sum()))


if __name__ == "__main__":
    main()
