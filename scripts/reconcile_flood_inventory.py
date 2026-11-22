"""Reconcile male_flood_inventory.csv against the project's existing event records and
populate the source register, candidate table, legacy storm-group proxies and
time-alignment register in the organised male_flood_ai_data folder.

No record is promoted to an accepted flood label. Run after organise_male_flood_ai_data.py.
    python scripts/reconcile_flood_inventory.py --repo . --dest ../male_flood_ai_data
"""
import argparse, re
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

MB = "male-flood-basis/data/"


def rd(p):
    return pd.read_csv(p, dtype=str, keep_default_na=False, encoding="utf-8-sig")


def days(s, e):
    s, e = date.fromisoformat(s), date.fromisoformat(e)
    return [s + timedelta(n) for n in range((e - s).days + 1)]


def url_key(u):
    """Host family + trailing article number, so slug/host variants of one article compare equal."""
    u = re.sub(r"^https?://(www\.)?", "", u.strip()).rstrip("/")
    host = u.split("/")[0]
    fam = {"see.mv": "sun", "s1.see.mv": "sun", "en02.sun.mv": "sun", "english.sun.mv": "sun", "en.sun.mv": "sun",
           "s1.sun.mv": "sun", "v1.oneonline.mv": "oneonline.mv", "ras.mv": "ras.mv"}.get(host, host)
    num = re.findall(r"/(\d{3,})(?:$|[/?])", "/" + u.split("/", 1)[-1] + "/")
    return f"{fam}#{num[-1]}" if num else u


# Per-record judgements. Classification and actions are proposals for human review, built only from
# evidence already in the repository; they do not change any label.
J = {
 "RAIN001": ("uncertain", "Ras (dv) article only; no other project record for 2020.",
             "Open the Ras article; decide rain vs mixed (source mentions incoming seawater); check ERA5 for 2020-05-18; no sea-level series covers 2020.",
             "keep_candidate_needs_mechanism_check", "New date with no corroboration; seawater mention means a single rain cause is not established."),
 "RAIN002": ("rain", "Ras (dv) contemporaneous article; existing compiled 11 Dec 2021 rests on JICA survey photos (decision: uncertain).",
             "Confirm from the article which flooded days it states (11 and 12 Dec); check whether it fixes the JICA photo date.",
             "link_as_supporting_source_and_rereview_existing_uncertain", "Overlaps compiled 2021-12-11 (legacy storm S01); the new source could resolve the earlier date uncertainty. 12 Dec is a new candidate day, not a new storm."),
 "RAIN003": ("rain", "One Online (dv) article; existing compiled record with official MNDF source (decision: include).",
             "None beyond routine source check.", "link_as_additional_source", "Exact date match with compiled 2022-07-17 (S02); same event, independent second source."),
 "COAST001": ("coastal", "One Online (en) plus Sun article.", "Confirm Male island location (Carnival area) and coastal mechanism; no modelled sea level before 2022-11-23 and no observed tide data for 2022.",
              "keep_in_coastal_candidates_exclude_from_rain_target", "No existing record; coastal swell is a separate target type."),
 "RAIN004": ("rain", "Atoll Times article published 2 Apr 2023 naming Saturday (= 1 Apr 2023); existing compiled record (decision: uncertain).",
             "Resolve intraday conflict (compiled: late-night storm; import: Saturday morning). ERA5 shows 0.9 mm and Hulhule GSOD 0.0 mm on 1 Apr 2023: check 31 Mar-2 Apr rainfall before accepting the date.",
             "link_and_rereview_existing_uncertain_with_conflict_visible", "Weekday supports 1 Apr, but both weather series show almost no rain that day, so the date or the rain attribution needs checking."),
 "RAIN005": ("rain", "Sun (en) morning report.", "Open article; confirm date of flooding versus overnight rain; corroborate with a second source or NDMA log.",
             "keep_candidate_new_date", "No existing record; not in Groundsource screen."),
 "RAIN006": ("rain", "Sun (en) article; existing compiled record from PSM (decision: include).", "Routine source check.",
             "link_as_additional_source", "Exact date match with compiled 2023-07-21 (S04)."),
 "COAST002": ("coastal", "Atoll Times 4910 (same URL as Groundsource review) and Sun 83962.", "Confirm 6 Aug surges affected Male island proper (article also covers other islands and the bridge).",
              "keep_in_coastal_candidates_exclude_from_rain_target", "Matches the Groundsource 2023-08-05/06 coastal candidate; 6 Aug was unverified there and the new Sun link needs checking."),
 "OFF001": ("rain", "NDMA public incident table (same URL as starter-pack lead 2023-10-01).", "Obtain incident circumstances (time, rain cause, property only vs street); look for news corroboration.",
            "keep_official_lead", "Exact match with starter-pack lead; property-level record, not street flooding."),
 "RAIN007": ("rain", "Atoll Times 7101 (published 1 Jan 2024); compiled 30-31 Dec 2023 (include 31 Dec); council VLR lead; Groundsource overlap.",
             "Keep the 179.9 mm Hulhule report vs 4.3 mm GSOD contradiction open; decide whether 30 Dec flooded.",
             "link_as_additional_source", "Same storm as compiled 2023-12-31 (S05); multi-island article with explicit Male reference."),
 "RAIN008": ("rain", "Atoll Times 7232: the same article already used by the compiled record (decision: include).", "None.",
             "duplicate_of_existing_no_new_evidence", "Exact date and URL match with compiled 2024-01-10 (S06)."),
 "RAIN009": ("rain", "Sun 87030 (published 13 Jan) and PlusMV; Groundsource review already found 87030; MMS lead describes 12-13 Jan.",
             "Re-review the masked 12 Jan decision with Sun 87030; decide storm relation to 10 Jan; NDMA 13 Jan record is not a separate storm by default.",
             "link_and_rereview_existing_uncertain", "Compiled 2024-01-12 was uncertain because its source was blocked; this accessible source supports 12 Jan."),
 "RAIN010": ("rain", "Edition 32861 and Sun 88720; NDMA incident 2024/52 (via Groundsource review).",
             "Keep morning vs afternoon timing disagreement; confirm whether 14 Apr is a flooded day or only the publication day.",
             "keep_candidate_new_date_corroborated", "Absent from the compiled 18; matches the Groundsource review's new corroborated candidate. GSOD shows 108.5 mm dated 14 Apr (possible day-shift)."),
 "OFF002": ("rain", "MMS annual-report indexed text only; URL redirected earlier.", "Retrieve the original MMS report; find a second source for 8 May 2024.",
            "keep_official_lead_needs_retrieval", "No existing record; evidence not yet retrieved."),
 "RAIN011": ("rain", "Edition 35325 (same article as compiled source edition.mv/bbc/35325); NDMA; Groundsource overlap.",
             "None for the date; 11:00 is rain onset, not flood onset.", "duplicate_of_existing_no_new_evidence",
             "Same article number as the compiled 2024-08-13 source (S07); Groundsource 12-14 Aug extra days remain unverified."),
 "OFF003": ("uncertain", "NDMA 2024 PDF p.62 case 193 lists rainwater flooding; the assistance table lists the same date as fire.",
            "Resolve rainwater vs fire classification from the original PDF; check relation to an earlier fire at the property; find any news corroboration.",
            "hold_classification_conflict", "Recorded conflict must stay visible; Groundsource review noted this NDMA entry but did not count it."),
 "OFF004": ("rain", "NDMA 2024 PDF p.63, incidents 2024/208 and 2024/209 (two properties).",
            "Treat the two properties as one candidate date; look for a news report and rainfall context.",
            "keep_official_lead_corroborated_by_groundsource_date", "Matches the Groundsource review's new 11 Oct 2024 candidate; two records are not two storms."),
 "OFF005": ("rain", "MMS report Figure 48 caption (indexed text) on Male dewatering.",
            "Retrieve the report figure; decide relation to 20-21 Dec (3 days later); compare the unverified Groundsource 17 Dec polygon.",
            "keep_official_lead_needs_retrieval", "Same date as an unverified Groundsource candidate (date match only, no source link)."),
 "RAIN012": ("rain", "Atoll Times 10805 and Ras 50794; compiled 20-21 Dec 2024 used other URLs (decision: uncertain).",
             "Re-review the masked 20-21 Dec decision with these sources; keep the GSOD 0.0 (20th) vs 93.0 mm (21st) day-shift question open.",
             "link_and_rereview_existing_uncertain", "Same storm as compiled 2024-12-20 (S08); Groundsource review also found 10805."),
 "RAIN013": ("rain", "Ras 51148 (dv); compiled 2-3 Jan 2025 (include 3 Jan); Groundsource overlap.", "Routine source check; 2 Jan remains uncertain.",
             "link_as_additional_source", "Exact match for 3 Jan with compiled 2025-01-03 (S09)."),
 "RAIN014": ("rain", "Atoll Times 10994; compiled 2025-01-11 (include) from Standard/PlusMV.",
             "Check whether flooding began on the evening of 10 Jan (compiled says early-morning rain on 11 Jan); 10:00 on 11 Jan is a response-status time.",
             "link_and_add_candidate_day", "Same storm as compiled 2025-01-11 (S10); 10 Jan is a new candidate day, and the Groundsource review left it unverified."),
 "RAIN015": ("rain", "Mihaaru 143297 (dv, published 2 Mar); compiled 2025-03-01 (include).", "None for 1 Mar; 2 Mar is not labelled by this record.",
             "link_as_additional_source", "Exact match with compiled 2025-03-01 (S11)."),
 "RAIN016": ("rain", "ThePress 159645 (dv, published 21:15 on 11 Mar); compiled 11-12 Mar 2025 (decision: uncertain).",
             "Re-review the masked 11 Mar date; article reuses an old photo; GSOD shows 0.0 (11th) and 65.8 mm (12th).",
             "link_and_rereview_existing_uncertain", "Same storm as compiled 2025-03-11 (S12); a same-evening article supports 11 Mar."),
 "RAIN017": ("rain", "One Online 105623 (dv), MNDF pumping from 21:40.", "Open the article; look for a second source; 21:40 is dewatering start, not flood onset.",
             "keep_candidate_new_date", "No existing record; inside Groundsource date range but no Groundsource candidate."),
 "RAIN018": ("rain", "Edition 46184 and Sun 101069; compiled 2025-11-25 (include) from Adhadhu says Tuesday-morning Maafannu flooding.",
             "Decide whether 25 Nov (Tue morning, Adhadhu) and 26 Nov (rain after 13:00, Edition) are one storm, two events, or a date error; open both articles.",
             "conflict_hold_for_review", "The import says it corrects an earlier 25 Nov candidate, but the compiled 25 Nov record has its own include decision. Do not overwrite either."),
 "RAIN019": ("rain", "Sun en02 104638; compiled 2026-04-16 used see.mv/104638 (same Sun article number, blocked; decision: uncertain).",
             "Confirm both URLs are the same article; decide whether 'flooding and pumping' resolves the earlier pumps-only doubt.",
             "link_and_rereview_existing_uncertain", "Exact date match with compiled 2026-04-16 (S14)."),
 "COAST003": ("coastal", "Edition 52858 and Atoll Times 16641.", "Confirm coastal areas on Male island; check relation to the 30 Jul 2026 Boduthakurufaanu section flooding (compiled, attributed to pumps not running).",
              "keep_in_coastal_candidates_exclude_from_rain_target", "No existing record; after the Groundsource release end (2026-02-03); modelled sea level available."),
 "RAIN020": ("rain", "Ras 67665 (dv).", "Open article; look for a second source.", "keep_candidate_new_date", "No existing record."),
 "RAIN021": ("rain", "Sun s1 227310 (dv).", "Open article; look for a second source.", "keep_candidate_new_date", "No existing record."),
 "RAIN022": ("rain", "Edition 55125: the same article as the compiled record (decision: include).", "None.",
             "duplicate_of_existing_no_new_evidence", "Exact date and URL match with compiled 2026-10-21 (S17)."),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--dest", required=True)
    a = ap.parse_args()
    repo, dest = Path(a.repo).resolve(), Path(a.dest).resolve()

    imp = rd(dest / "02_interim/event_candidates/male_flood_inventory.csv")  # the preserved copy
    inc = rd(repo / MB / "flood_incidents_greater_male_2021-2026.csv")
    rt = rd(repo / "derived/incident_rainfall_table.csv").set_index("incident_id")
    rev = rd(repo / "derived/extended_analysis/incident_storm_groups.csv").set_index("incident_id")
    spl = rd(repo / "Male_Flood_Data_Starter_Pack/flood/event_candidates.csv")
    gsc = rd(repo / "derived/groundsource_review/inventory_comparison.csv")
    gsr = rd(repo / "derived/groundsource_review/male_candidate_review.csv")
    era = rd(repo / MB / "male_reanalysis_daily_2020-2026.csv").set_index("date")["precipitation_sum_mm"]
    stn = rd(repo / MB / "hulhule_station_daily_2020-2025.csv").set_index("date")
    inv = rd(dest / "00_catalog/dataset_inventory.csv")
    assert len(imp) == 30 and set(J) == set(imp.record_id), "judgement table must cover every imported record"

    # ---------------- source register (one row per distinct URL)
    src, cited = {}, {}

    def reg(url, cite, **kw):
        url = url.strip()
        if not url:
            return ""
        if url not in src:
            src[url] = dict(source_id=f"SRC{len(src) + 1:04d}", url=url, **{k: v for k, v in kw.items() if v})
        else:
            for k, v in kw.items():
                if v and not src[url].get(k):
                    src[url][k] = v
        cited.setdefault(url, []).append(cite)
        return src[url]["source_id"]

    for _, r in imp.iterrows():
        reg(r.source_url, r.record_id, publisher=r.source_name, title=r.source_title, language=r.source_language,
            publication_date_as_displayed=r.source_publication_date_as_displayed,
            publication_time_as_displayed=r.source_publication_time_as_displayed, publication_timezone=r.source_publication_timezone)
        reg(r.additional_source_url, r.record_id + " (additional)",
            publication_date_as_displayed=r.additional_source_publication_date_as_displayed,
            publication_time_as_displayed=r.additional_source_publication_time_as_displayed, publication_timezone="unknown")
    for _, r in inc.iterrows():
        for u in r.source_urls.split():
            reg(u, f"MFB_{r.incident_id}")
    for iid, r in rev.iterrows():
        reg(r.checked_url, f"legacy_review_{iid}")
    for _, r in spl.iterrows():
        reg(r.source_url, f"SP_{r.event_or_record_date}", publisher=r.record_type.split()[0])
    for _, r in gsr.iterrows():
        for u in re.split(r"\s*\|\s*", r.independent_source_url):
            reg(u, f"GS_{r.start_date}", publication_date_as_displayed=r.independent_source_publication_or_record_date)

    keys = {}
    for u in src:
        keys.setdefault(url_key(u), []).append(src[u]["source_id"])
    sr = []
    for u, s in src.items():
        same = [x for x in keys[url_key(u)] if x != s["source_id"]]
        host = re.sub(r"^https?://(www\.)?", "", u).split("/")[0]
        sr.append(dict(source_id=s["source_id"], publisher=s.get("publisher", host), title=s.get("title", ""),
                       language=s.get("language", "unknown"), url=u,
                       publication_date_as_displayed=s.get("publication_date_as_displayed", ""),
                       publication_time_as_displayed=s.get("publication_time_as_displayed", ""),
                       publication_timezone=s.get("publication_timezone", "unknown"), publication_datetime_verified_iso8601="",
                       accessed_at_utc="unknown", local_evidence_path="",
                       usage_conditions="publisher copyright; cite and link; full text not stored" if "ndma" not in u and "meteorology" not in u else "official publication; cite; confirm reuse terms",
                       notes=("No local copy saved. " + (f"Possibly the same article as {';'.join(same)} (same host family and article number). " if same else "")).strip(),
                       cited_by=";".join(dict.fromkeys(cited[u])), url_match_key=url_key(u)))
    srdf = pd.DataFrame(sr)
    old = rd(dest / "00_catalog/source_register.csv")
    assert old.empty, "source_register.csv already populated: merge manually"
    srdf.to_csv(dest / "00_catalog/source_register.csv", index=False, encoding="utf-8-sig")
    sid = {u: s["source_id"] for u, s in src.items()}

    # ---------------- existing records as date windows
    existing = []
    for _, r in inc.iterrows():
        d = rt.loc[r.incident_id, "days_covered"].split()
        rv = rev.loc[r.incident_id]
        existing.append(dict(kind="compiled", id=f"MFB_{r.incident_id}", s=min(d), e=max(d), urls=r.source_urls.split(),
                             info=f"MFB_{r.incident_id} [{rv.decision}; pos={rv.positive_date or '-'}; uncertain={rv.uncertain_dates or '-'}; legacy storm {rv.storm}]",
                             storm=rv.storm))
    for _, r in spl.iterrows():
        existing.append(dict(kind="starter", id=f"SP_{r.event_or_record_date}", s=r.event_or_record_date, e=r.event_or_record_date,
                             urls=[r.source_url], info=f"SP_{r.event_or_record_date} [{r.record_type}]", storm=""))
    for _, r in gsc.iterrows():
        existing.append(dict(kind="groundsource", id=f"GS_{r.groundsource_start}_{r.groundsource_latest_end}", s=r.groundsource_start,
                             e=r.groundsource_latest_end, urls=re.split(r"\s*\|\s*", r.independent_source) if r.independent_source else [],
                             info=f"GS_{r.groundsource_start}..{r.groundsource_latest_end} ({r.records} rec) [{r.existing_inventory_comparison}]", storm=""))
    compiled_days = {d for x in existing if x["kind"] == "compiled" for d in days(x["s"], x["e"])}

    def ctx(series, dlist, fmt):
        out = []
        for d in dlist:
            k = d.isoformat()
            out.append(f"{k}={fmt(k)}")
        return "; ".join(out)

    def gsod(k):
        if k not in stn.index:
            return "no row" if k <= "2025-08-24" else "after series end"
        v = stn.at[k, "precip_mm"]
        return f"{v} ({stn.at[k, 'precip_flag']})" if v else "missing"

    rows, matched_existing, near_rev = [], set(), {}
    for _, r in imp.iterrows():
        win = days(r.event_start_date, r.event_end_date)
        ukeys = {url_key(u) for u in (r.source_url, r.additional_source_url) if u}
        hits = {"compiled": [], "starter": [], "groundsource": []}
        url_hits, near = [], []
        exact = False
        for x in existing:
            s, e = date.fromisoformat(x["s"]), date.fromisoformat(x["e"])
            ov = max(win[0], s) <= min(win[-1], e)
            sep = (max(win[0], s) - min(win[-1], e)).days
            # a shared multi-incident document (NDMA annual PDF, MMS report) is not the same event unless dates are close
            u_hit = bool(ukeys & {url_key(u) for u in x["urls"]}) and sep <= 3
            if ov or u_hit:
                hits[x["kind"]].append(x["info"])
                matched_existing.add(x["id"])
                exact |= x["kind"] == "compiled" and (x["s"], x["e"]) == (r.event_start_date, r.event_end_date) or (x["kind"] == "compiled" and ov and u_hit)
                if u_hit:
                    url_hits.append(x["id"])
            elif 1 <= sep <= 3 and x["kind"] != "groundsource":
                near.append(f"{x['id']} ({sep} d)")
                near_rev.setdefault(x["id"], []).append(f"{r.record_id} ({sep} d)")
        new_days = [d.isoformat() for d in win if d not in compiled_days]
        if exact:
            mt = "exact_match_with_compiled_incident"
        elif hits["compiled"]:
            mt = "date_overlap_possible_duplicate"
        elif hits["starter"] or hits["groundsource"]:
            mt = "matches_non_compiled_lead_only"
        elif near:
            mt = "nearby_dates_possible_same_storm"
        else:
            mt = "no_existing_match"
        conflicts = []
        if r.record_id == "OFF003":
            conflicts.append("NDMA rainwater vs fire classification conflict (recorded in import)")
        if r.record_id == "RAIN018":
            conflicts.append("Compiled MFB_2025-11-25 (include) vs imported 26-27 Nov 'correction'")
        if r.record_id == "RAIN004":
            conflicts.append("Intraday timing (late night vs Saturday morning); ERA5 0.9 mm / GSOD 0.0 mm on 1 Apr 2023")
        if r.record_id == "RAIN010":
            conflicts.append("Morning vs afternoon rain timing between sources")
        if r.record_id == "RAIN014":
            conflicts.append("Compiled: early-morning rain 11 Jan; import: flooding since evening 10 Jan")
        if r.record_id == "RAIN007":
            conflicts.append("Reported Hulhule 179.9 mm/24 h vs GSOD 3.3-4.3 mm (existing open issue)")
        cls, ev, chk, act, why = J[r.record_id]
        ctxdays = days((win[0] - timedelta(1)).isoformat(), (win[-1] + timedelta(1)).isoformat())
        rows.append(dict(
            imported_record_id=r.record_id, record_category=r.record_category, imported_start=r.event_start_date, imported_end=r.event_end_date,
            window_days=len(win), flood_type_as_imported=r.flood_type, proposed_classification=cls,
            imported_source_ids=";".join(filter(None, [sid.get(r.source_url, ""), sid.get(r.additional_source_url, "")])),
            match_type=mt, matched_compiled_incidents=" || ".join(hits["compiled"]), matched_starter_pack_leads=" || ".join(hits["starter"]),
            matched_groundsource_windows=" || ".join(hits["groundsource"]), same_article_as=";".join(url_hits), nearby_records_1_3_days=";".join(near),
            new_candidate_dates_vs_compiled=";".join(new_days), conflicts=" | ".join(conflicts),
            era5_daily_mm_context=ctx(era, ctxdays, lambda k: era.get(k, "n/a")), hulhule_gsod_mm_context=ctx(stn, ctxdays, gsod),
            evidence_available=ev, checks_required=chk, proposed_action=act, justification=why,
            training_label_status=r.training_label_status, imported_review_status=r.review_status, imported_review_notes=r.review_notes,
            reported_timing=r.reported_timing,
            rain_start_time_local=(f"{r.rain_start_time_qualifier} {r.rain_start_time_local}".strip() if r.rain_start_time_local else ""),
            response_start_time_local=r.response_start_time_local, flood_onset_time_local=r.flood_onset_time_local or "unknown"))
    for x in existing:
        if x["kind"] == "compiled" and x["id"] not in matched_existing:
            rows.append(dict(imported_record_id="", record_category="existing_not_in_import", imported_start=x["s"], imported_end=x["e"],
                             match_type="existing_only", matched_compiled_incidents=x["info"],
                             nearby_records_1_3_days=";".join(near_rev.get(x["id"], [])),
                             proposed_action="retain_existing_record_unchanged",
                             justification="Present in the compiled inventory but absent from the import; absence from the import is not evidence against it.",
                             era5_daily_mm_context=ctx(era, days(x["s"], x["e"]), lambda k: era.get(k, "n/a")),
                             hulhule_gsod_mm_context=ctx(stn, days(x["s"], x["e"]), gsod)))
    rec = pd.DataFrame(rows)
    rec.to_csv(dest / "02_interim/event_candidates/inventory_reconciliation.csv", index=False, encoding="utf-8-sig")

    # ---------------- event candidates (template table)
    status = {"keep_candidate_needs_mechanism_check": "needs_scope_check", "conflict_hold_for_review": "needs_date_check",
              "hold_classification_conflict": "pending", "link_and_rereview_existing_uncertain_with_conflict_visible": "needs_date_check"}
    ec = []
    for _, r in imp.iterrows():
        rr = rec[rec.imported_record_id == r.record_id].iloc[0]
        ec.append(dict(candidate_id=r.record_id, source_id=sid.get(r.source_url, ""), candidate_start_date=r.event_start_date,
                       candidate_end_date=r.event_end_date, date_evidence_text=r.reported_timing, geographic_scope=r.geographic_scope,
                       location_as_reported="", candidate_flood_type={"rain": "rain", "coastal": "coastal"}.get(rr.proposed_classification, "unknown"),
                       review_status=status.get(rr.proposed_action, "pending"),
                       notes=f"Imported male_flood_inventory.csv; {rr.proposed_action}; date_window_interpretation={r.date_window_interpretation}"))
    for _, r in inc.iterrows():
        d = rt.loc[r.incident_id, "days_covered"].split()
        rv = rev.loc[r.incident_id]
        ec.append(dict(candidate_id=f"MFB_{r.incident_id}", source_id=sid.get(r.source_urls.split()[0], ""), candidate_start_date=min(d),
                       candidate_end_date=max(d), date_evidence_text=r.dates, geographic_scope="Greater Male compilation; Male rows per locations",
                       location_as_reported=r.locations, candidate_flood_type="rain",
                       review_status="needs_date_check" if rv.decision == "uncertain" else "pending",
                       notes=f"male-flood-basis compiled incident; legacy decision {rv.decision} (event_review.csv), legacy storm proxy {rv.storm}"))
    for _, r in spl.iterrows():
        ec.append(dict(candidate_id=f"SP_{r.event_or_record_date}", source_id=sid.get(r.source_url, ""), candidate_start_date=r.event_or_record_date,
                       candidate_end_date=r.event_or_record_date, date_evidence_text=r.record_type, geographic_scope=r.spatial_precision,
                       location_as_reported=r.island, candidate_flood_type="rain", review_status="pending", notes=r.limitation))
    assert rd(dest / "02_interim/event_candidates/event_candidates.csv").empty
    pd.DataFrame(ec).to_csv(dest / "02_interim/event_candidates/event_candidates.csv", index=False, encoding="utf-8-sig")

    # ---------------- legacy storm proxies (not verified storms)
    sg = []
    for s, g in rev.reset_index().groupby("storm"):
        allds = [d for i in g.incident_id for d in rt.loc[i, "days_covered"].split()]
        sg.append(dict(storm_group_id=f"LEGACY_{s}", period_start_date=min(allds), period_end_date=max(allds),
                       grouping_basis="Legacy proxy: compiled incidents merged when <=2 calendar days apart (reports/extended_analysis.md)",
                       evidence_source_ids=";".join(sid.get(u, "") for u in g.checked_url),
                       review_status="legacy_proxy_not_verified", notes="members: " + ";".join(g.incident_id)))
    assert rd(dest / "03_reviewed/storm_groups/storm_groups.csv").empty
    pd.DataFrame(sg).to_csv(dest / "03_reviewed/storm_groups/storm_groups.csv", index=False, encoding="utf-8-sig")

    # ---------------- time-alignment register (documentation; nothing resolved by performance)
    def dsid(path_part):
        m = inv[inv.original_repo_path.str.contains(path_part, regex=False)]
        return ";".join(m.dataset_id)
    ta = [
        (dsid("male_reanalysis_"), "time_local label, offset undocumented", "hour t = preceding-hour sum (Open-Meteo docs, not verified for this file)", "", "Asia/Male (+05:00)",
         "None applied. Nominal timestamps used; -1/+1 h sensitivity only (legacy extended analysis)", "unresolved", "Original Open-Meteo request (timezone parameter) not saved."),
        (dsid("male_sea_level_waves"), "time_local label, offset undocumented", "instantaneous", "", "Asia/Male (+05:00)",
         "None applied. Tide correlation with UHSLC: r=0.963 at UTC+4, 0.959 at UTC+5 (cannot separate)", "unresolved", "Modelled; do not pool with UHSLC."),
        (dsid("noaa_gsod_") + ";" + dsid("hulhule_station_daily"), "GSOD day (day boundary not documented)", "daily; may include part of preceding day (NOAA metadata)", "", "Asia/Male calendar day",
         "None applied. Pattern of totals dated one day after reported floods (12 Jan 2024, 20 Dec 2024, 11 Mar 2025) noted only", "hypothesis_only", "Station is on Hulhule, not Male."),
        (dsid("noaa_global_hourly_") + ";" + dsid("noaa_precipitation_accumulations"), "UTC (ISD)", "per AA group: 6/12/24 h ending at report time", "", "Asia/Male (+05:00)",
         "UTC+5 fixed offset is deterministic (no DST); not yet applied; overlapping windows must not be summed", "verified", "Timezone verified; daily assignment of accumulations unresolved."),
        (dsid("UHSLC_"), "UTC (units row)", "instantaneous hourly", "", "Asia/Male (+05:00)",
         "Clean copy keeps explicit +00:00; local conversion is a fixed +5 h shift when needed", "verified", "Datum: station zero (not MSL)."),
        (dsid("nasa_power_"), "UTC (and derived UTC+5 column)", "hourly rate", "", "Asia/Male (+05:00)", "Already provided in derived CSV", "verified", "Five-day sample only."),
        (dsid("male_forecast_hourly"), "UTC (Z)", "forward 1 h and 6 h windows", "", "Asia/Male (+05:00)", "Single snapshot; not used", "verified", "Not a forecast archive."),
        (dsid("male_flood_inventory.csv"), "event clocks: local per article context; publication timezone unknown", "not applicable", "", "Asia/Male",
         "Clock times kept as text with qualifiers (approximately/after); no conversion", "unresolved", "Publication time is not flood onset; RAIN010 publication 00:00:10 is not a new storm."),
        (dsid("flood_incidents_greater_male"), "dates as written by compiler", "not applicable", "", "Asia/Male calendar day",
         "None; legacy review masked uncertain dates", "unresolved", "Dates derive from article text; publication vs event date checked only for some records."),
    ]
    assert rd(dest / "03_reviewed/time_alignment/time_alignment_decisions.csv").empty
    pd.DataFrame(ta, columns=["dataset_id", "source_timestamp_timezone", "source_accumulation_start", "source_accumulation_end", "target_timezone",
                              "conversion_or_alignment_rule", "resolution_status", "notes"]).assign(
        evidence_source_ids="", decision_date="2026-11-22").reindex(
        columns=["dataset_id", "source_timestamp_timezone", "source_accumulation_start", "source_accumulation_end", "target_timezone",
                 "conversion_or_alignment_rule", "evidence_source_ids", "resolution_status", "decision_date", "notes"]).to_csv(
        dest / "03_reviewed/time_alignment/time_alignment_decisions.csv", index=False, encoding="utf-8-sig")

    # ---------------- summary
    r30 = rec[rec.imported_record_id != ""]
    imp_days = {d for _, r in imp.iterrows() for d in days(r.event_start_date, r.event_end_date)}
    rain_days = {d for _, r in imp[imp.flood_type == "rain_associated"].iterrows() for d in days(r.event_start_date, r.event_end_date)}
    print("sources", len(srdf), "| reconciliation rows", len(rec), "| candidates", len(ec), "| legacy storms", len(sg))
    print(r30.match_type.value_counts().to_string())
    print(r30.proposed_action.value_counts().to_string())
    print(r30.proposed_classification.value_counts().to_string())
    print("imported calendar days", len(imp_days), "rain-associated days", len(rain_days), "compiled days", len(compiled_days),
          "union rain+compiled", len(rain_days | compiled_days), "imported days not in compiled", len(imp_days - compiled_days))
    print("existing-only compiled:", list(rec[rec.match_type == "existing_only"].matched_compiled_incidents))


if __name__ == "__main__":
    main()
