"""Build the v002 source-verification and reviewed-event tables (22 Nov 2026).

Every decision below was made by reading the source body (article text, official
PDF page or register row) fetched on 2026-11-22; see 00_catalog/source_fetch_log_20261122.csv.
The decisions are data, kept here so they can be audited and re-run. Nothing is
inferred from model agreement. Reviewer: Claude (AI-assisted); human review pending.

Usage:  python build_reviewed_events_v002.py <male_flood_ai_data root>
"""
import csv
import sys
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(sys.argv[1])
REVIEWED_ON = "2026-11-22"
REVIEWER = "Claude (AI-assisted source check); human review pending"
TR = "AI translation (Claude), not checked by a Dhivehi speaker"
assert (ROOT / "03_reviewed/_archive_v001_20261122/flood_events.csv").exists(), "archive v001 first"

# ------------------------------------------------------------------ helpers
def w(path, rows, cols):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, cols, extrasaction="raise")
        wr.writeheader()
        for r in rows:
            wr.writerow({c: r.get(c, "") for c in cols})
    print(f"wrote {path.relative_to(ROOT)} ({len(rows)} rows)")

reg = {r["source_id"]: r for r in csv.DictReader(open(ROOT / "00_catalog/source_register.csv", encoding="utf-8-sig"))}
fetch = {}
for r in csv.DictReader(open(ROOT / "00_catalog/source_fetch_log_20261122.csv", encoding="utf-8")):
    if r["used_for_review"] == "yes":
        fetch[r["source_id"]] = r

# --------------------------------------------------- publication clock status
TZ = {
    "ras.mv": ("established UTC+5", "site clock test: latest-news stamps 20:36 on 22 Nov 2026 shown when UTC was 16:24"),
    "edition.mv": ("established UTC+5", "site clock test (20:54 shown at 16:24 UTC); JSON-LD datePublished is offset-less UTC, internal field = +5 h"),
    "plus.mv": ("explicit +05:00", "article:published_time and <time> carry +05:00"),
    "standard.mv": ("explicit +05:00", "dateModified/<time> carry +05:00"),
    "mihaaru.com": ("explicit +05:00", "article:published_time carries +05:00"),
    "mvrepublic.com": ("explicit +00:00 (UTC)", "article:published_time carries +00:00"),
    "adhadhu.com": ("established UTC+5", "page clock labelled 'Maldives time (MVT)'"),
    "psmnews.mv": ("established UTC+5", "site clock test (19:00 shown at 16:25 UTC)"),
    "archive.mv": ("established UTC+5", "site clock test (19:00 shown at 16:26 UTC)"),
}
def tz(url):
    for k, v in TZ.items():
        if k in url:
            return v
    if url.endswith(".pdf") or "ndma.gov.mv" in url or "mndf.gov.mv" in url:
        return ("not applicable (official document/page)", "event dates taken from document text")
    return ("not established", "date shown without offset; no decisive site-clock evidence")

# ------------------------------------------------ source verification records
# sid: (canonical, body, pub_as_displayed, dates_supported, male, cause, rain_t, flood_t, resp_t, rainfall,
#       excerpt_original, excerpt_lang, excerpt_en, conflicts, records, relation)
S = {}
def src(sid, canonical, body, pub, dates, male, cause, rain_t, flood_t, resp_t, rainfall, ex, lang, ex_en, conflicts, records, relation, note=""):
    S[sid] = dict(canonical_source_id=canonical, body_accessible=body, publication_as_displayed=pub, event_dates_supported=dates,
                  male_island_evidence=male, cause_stated=cause, rain_timing=rain_t, flood_timing=flood_t, response_timing=resp_t,
                  rainfall_statements=rainfall, excerpt_original=ex, excerpt_language=lang, excerpt_english=ex_en,
                  conflicts=conflicts, records=records, relation_to_records=relation, note=note)

src("SRC0001", "SRC0001", "yes", "not shown on page; bracketed by neighbouring posts 18 May 2020 20:50-22:18 (import: 22:09)", "2020-05-18 (night)",
    "explicit: many areas of Male', especially Maafannu; pumps at IGMH, STO flour warehouse, West Park", "rain, with swells also entering Male' (mixed)",
    "about 2 h of non-stop rain 'tonight'", "flooding under way at publication", "MNDF pumping under way at publication", "",
    "މާލޭގެ ބޮޑު ސަރަހައްދެއްގައި ފެންބޮޑުވެފައިވާއިރު މާލެއަށް ދަނީ އުދަވެސް އަރަމުންނެވެ.", "dv",
    "While a large area of Male' is flooded, swells are also washing into Male'.", "rain and swell reported together", "RAIN001", "supports")
src("SRC0002", "SRC0002", "yes", "12 Dec 2021 18:14", "2021-12-11; 2021-12-12", "explicit: Male'", "rain ('unusually heavy rain')",
    "rain on 11 Dec ('yesterday')", "flooding 'yesterday and today'", "", "Nasheed tweet quoted: 'Male' area witnessed 134.7mm of rain during the past 24 hours' (station and window end not stated)",
    "މާލޭގައި އިއްޔެއާއި މިއަދު ފެންބޮޑުވީ އާދަޔާ ހިލާފަށް ވާރޭ ވެހުމުންކަމަށް", "dv",
    "[...said] the flooding in Male' yesterday and today was due to unusually heavy rain", "", "RAIN002", "supports")
src("SRC0003", "SRC0003", "yes", "2022-07-17 23:31:37 (meta, no offset)", "2022-07-17", "explicit: many roads; Boduthakurufaanu Magu, Dhuvaa track area, IGMH area",
    "rain", "from this afternoon, non-stop", "many roads flooded", "MNDF pumping from 17:30 'this evening'", "",
    "މިއަދު މެންދުރުފަހުން ފެށިގެން ހުއްޓާ ނުލައި މާލެއަށް ވާރޭ ވެހުމުން ވަނީ މާލޭގެ ގިނަ މަގުތަކެއްގައި ފެންބޮޑުވެފައެވެ.", "dv",
    "Non-stop rain on Male' since this afternoon has flooded many of Male''s roads.", "", "RAIN003", "supports")
src("SRC0004", "SRC0004", "yes", "2022-11-05 12:21:39 (<time>, no offset)", "2022-11-05", "explicit: Carnival area, Male'", "coastal (tidal swells at high tide)",
    "", "this morning, during high tide", "Council crew on site", "", "The carnival area in the capital city of Male' has flooded, following tidal swells this morning.", "en", "", "", "COAST001", "supports")
src("SRC0005", "SRC0005", "yes", "Nov 05, 2022 16:32", "2022-11-05", "explicit: Alimas Carnival area and neighbouring streets", "coastal (swell waves)",
    "", "Saturday", "", "", "Swell waves hit Male' City on Saturday, flooding the Alimas Carnival area and neighboring streets.", "en", "",
    "Registered title was blank; page title is 'City Council accuses govt. of halting efforts to mitigate flooding in Carnival area'", "COAST001 (additional)", "supports")
src("SRC0006", "SRC0006", "yes", "2 April 2023 (date only)", "2023-04-01", "explicit: Male' city; Westpark area worst-hit; M. Bihuge, Haveeree Hingun (Maafannu)",
    "rain", "Saturday morning", "flooded 'within a few seconds' of the Saturday-morning rain", "MNDF came several hours after water entered houses", "",
    "The heavy rain that hit Male Saturday morning caused flooding in the entire city within a few seconds.", "en", "",
    "Time of day differs from SRC0039 ('late hours of last night')", "RAIN004", "supports")
src("SRC0007", "SRC0007", "yes (via en02.sun.mv; see.mv returned 403)", "May 04, 2023 11:50", "2023-05-04", "explicit: Majeedhee Magu, Izzuddin Magu, IGMH",
    "rain", "08:00 pm Wednesday to 08:00 am Thursday window cited", "Thursday", "", "MMS: 58 mm at Hulhule, 20:00 Wed 3 May to 08:00 Thu 4 May (12 h)",
    "Heavy rain resulted in extensive flooding in the greater Male' area on Thursday, with flood water seeping into homes and shops.", "en", "",
    "", "RAIN005", "supports")
src("SRC0008", "SRC0008", "yes", "Jul 21, 2023 13:25", "2023-07-21", "explicit: roads in the four districts of the city", "rain",
    "from midnight Thursday until late Friday morning", "Friday", "MNDF firefighters pumping", "MMS: Hulhule 71 mm between 08:00 and 11:00 Friday",
    "Torrential rain poured over Male' City from midnight Thursday until late into Friday morning, resulting in heaving flooding in the streets", "en", "", "", "RAIN006", "supports")
src("SRC0009", "SRC0009", "yes", "5 August 2023 (date only)", "2023-08-05", "explicit: surf point in Henveiru ward; Boduthakurufaanu Magu",
    "coastal (tidal surges)", "", "since 2pm Saturday", "", "", "Major waves hit the Male area Saturday afternoon, flooding parts of the surf point in Henveiru ward of Male and the Sinamale bridge highway.",
    "en", "", "", "COAST002", "supports")
src("SRC0010", "SRC0010", "yes", "Aug 06, 2023 16:29", "2023-08-05 (photo caption, bridge); 2023-08-06 (swells lashed 'the capital')",
    "5 Aug: Sinamale Bridge (not Male' island); 6 Aug: 'including the capital' - Male' island flooding not stated", "coastal (king tide, swell waves)",
    "", "peak tide hours Sunday", "police advisory from 3 PM", "", "swell waves measuring 6-8 feet lashed the shore of some of the islands in southern and central Maldives, including the capital, during peak tide hours on Sunday.",
    "en", "", "Registered title blank; page title 'People advised to avoid bridge due to tidal surges'", "COAST002 (additional)", "supports 5 Aug context; 6 Aug location unresolved")
src("SRC0011", "SRC0011", "yes (server-rendered table)", "no publication date; incident dates in table", "2023-10-01 (rainwater, M. Kandaru); 2023-07-31 (surges); 2023-08-05 (surges)",
    "explicit: island 'Male''; M. Kandaru; 'Mary Brown' area", "rainwater flooding (2023-10-01); surges (2023-07-31, 2023-08-05)", "", "", "", "",
    "Rainwater Flooding | Male' | 1 | M. Kandaru | 01.10.2023 ... Surges | Male' | 2 | Mary Brown sarahahdhah undha araathy | 31.07.2023 ... Surges | Male' | 3 | Male' | 05.08.2023",
    "en (with Dhivehi transliteration)", "Transliteration 'Mary Brown sarahahdhah undha araathy' = 'when swells reached the Mary Brown area' (" + TR + ")",
    "Table also lists 'Surges, Velaanaa International Airport, 05.08.2026' (Hulhule, not Male'; year probably a typo for 2023)", "OFF001; SP_2023-10-01; NEW_NDMA_2023-07-31; NEW_NDMA_2023-08-05", "supports")
src("SRC0012", "SRC0012", "yes", "1 January 2024 (date only)", "2023-12-31", "explicit: houses in Male and Hulhumale flooded", "rain",
    "", "Sunday", "", "MET: 179.7 mm at Hulhule from 8 am Sunday to 8 am Monday (highest ever at Hulhule)",
    "According to the MET, 179.7 millimetres of rain were recorded from 8 am Sunday to 8 am Monday.", "en", "",
    "Differs from MVRepublic (SRC0043) 179.9 mm 'within 24 hours'", "RAIN007", "supports")
src("SRC0013", "SRC0013", "yes", "11 January 2024 (date only)", "2024-01-10; context 2023-12-31", "explicit: Boduthakurufaanu Magu near Boduvalhu; Kudakudhinge Bageecha",
    "rain", "since evening (Wednesday)", "Wednesday evening", "MNDF came out Wednesday evening", "Male 118.2 'milliliters' [mm] on 31 Dec 2023 (as printed)",
    "Heavy rainfall since evening has caused flooding in parts of Male, making it difficult to walk and drive.", "en", "",
    "", "RAIN008; MFB_2024-01-10; legacy_review_2024-01-10", "supports", "Same article as the compiled record: no new evidence from RAIN008")
src("SRC0014", "SRC0014", "yes", "Jan 13, 2024 12:29", "2024-01-12", "explicit: Male' City streets; Ameenee Magu photo", "rain", "", "Friday", "NDMA: 144 homes requested help; 57 people moved",
    "MMS: heaviest 24 h total 159.3 mm in Male' City; Hulhumale' 143.4 mm; Hulhule' 105.4 mm",
    "Male' area experienced torrential rain on Friday, which flooded the city's streets and damaged homes.", "en", "",
    "Station attribution conflicts with MMS report (SRC0018): Hulhule NMC 143.4, Hulhumale AWS 105.4", "RAIN009; GS_2024-01-12", "supports")
src("SRC0015", "SRC0015", "yes", "2024-01-13 14:29 +05:00", "2024-01-12", "explicit: Male' city", "rain", "since early morning on Friday", "yesterday (Friday)",
    "NDMA tweet 12 Jan 2024: 144 households asked for help", "", "The continuous rainfall since early morning on Friday has resulted in flooded streets in Male' city.", "en", "",
    "", "RAIN009 (additional)", "supports")
src("SRC0016", "SRC0016", "yes", "2024-04-14 00:00:10 (displayed, UTC+5); JSON-LD 2024-04-13T19:13:26 (UTC)", "2024-04-13",
    "explicit: Male' streets; five houses relocated", "rain", "Saturday afternoon", "streets soon flooded; 'streets remain flooded' at publication", "MNDF engaged",
    "", "Saturday afternoon saw heavy rain in the Maldives, with Male' streets soon flooding.", "en", "",
    "SRC0017 says Saturday morning", "RAIN010", "supports")
src("SRC0017", "SRC0017", "yes (via en02.sun.mv; see.mv returned 403)", "Apr 14, 2024 10:41", "2024-04-13", "explicit: Male' City roads, streets and residences; 85 buildings",
    "rain", "non-stop rainfall on Saturday morning", "Saturday", "MNDF draining after Saturday's rain; 241 sand-bag barrages", "",
    "at least 85 buildings in Male' City reported sustaining various damages owing to non-stop rainfall on Saturday morning.", "en", "",
    "SRC0016 says Saturday afternoon. Registered title blank; page title '85 Male' City buildings report flooding'", "RAIN010 (additional); GS_2024-04-13", "supports")
src("SRC0018", "SRC0018", "yes (Wayback snapshot 20260218151135; current URL redirects to a script-only page)", "PDF created 2025-02-04",
    "2024-01-12; 2024-02-16; 2024-05-08; 2024-05-25; 2024-08-14 (caption); Oct 2024 (caption); Nov 2024 (undated); 2024-12-17 (dewatering); 2024-12-20",
    "explicit 'Male'' in each statement; no streets", "rain (heavy-rain episodes)", "", "see per-date statements", "dewatering 17 Dec (Fig. 48)",
    "12 Jan: 159.3 mm AWS Male', 143.4 Hulhule NMC, 105.4 Hulhumale; 25 May: 40.4 mm AWS Male'; 20 Dec: 136.5 Male', 117.4 Hulhule (24 h labelled by start day)",
    "flooding reported in N. Maalhendhoo and some areas of Male' on 8th May | Male' City reported floods on 25th May, with 40.4 mm observed at the AWS in Male' | dewatering was carried out at Male' the same day [17 Dec]",
    "en", "", "Fig. 27 caption dates Male' flood photo 14 Aug (flood day reported elsewhere as 13 Aug)",
    "OFF002; OFF005; SP_2024-01-12; NEW_MMS_2024-02-16; NEW_MMS_2024-05-25; NEW_MMS_2024-08-14; NEW_MMS_2024-11", "supports / context by date")
src("SRC0019", "SRC0019", "yes", "2024-08-13 14:29:15 (displayed, UTC+5); JSON-LD 2024-08-13T09:49:46 (UTC)", "2024-08-13", "explicit: nearly all streets of Male'; Ameenee Magu photo",
    "rain", "around 11:00 this morning", "nearly all streets flooded by publication", "Police and MNDF assisting", "",
    "Male' has been experiencing heavy rain since this morning, resulting in nearly all the streets becoming flooded.", "en", "", "",
    "RAIN011; MFB_2024-08-13; GS_2024-08-12", "supports", "Alias SRC0046 (edition.mv/bbc/35325 resolves to the same article)")
src("SRC0020", "SRC0020", "yes (65-page PDF; register pp. 58-63, assistance table pp. 56-57)", "PDF created 2024-11-07; register to 19 Oct 2024",
    "Male' rainwater flooding: 2024-01-10 (#13), 2024-01-12 (#14), 2024-01-13 (#1), 2024-04-13 (#52), 2024-08-13 (#167), 2024-09-18 (#193), 2024-10-11 (#208, #209)",
    "explicit: 'K. Male' (I)'; property names for #193, #208, #209", "rain water flooding (register category)", "", "", "",
    "assistance totals for 12-Jan, 13-Jan, 13-Apr, 13-Aug (rain water flooding); 18-Sep row is 'Fire Incidents'",
    "EMOPS-IC/2024/193 18-Sep-2024 K. Male' (I) Rain water flooding H. Dhoohimerige - Hulhangubai- Print | EMOPS-IC/2024/194 18-Sep-2024 K. Male' (I) Fire Incidents G. Sindhu Hiya",
    "en", "", "OFF003 'fire label' is case #194 at a different property, not a reclassification of #193",
    "OFF003; OFF004; GS_2024-04-13; GS_2024-08-12; GS_2024-10-11; NEW_NDMA_2024-01-13", "supports")
src("SRC0021", "SRC0021", "yes", "21 December 2024 (date only)", "2024-12-20/21 (overnight); context 2024-12-16..21",
    "explicit: West Park, IGMH, Villingili Ferry Terminal, Digicel, Jelly Pizza", "rain", "began Friday night", "flooding in several areas", "MNDF drained overnight; 16 pumps in five areas",
    "MET: Male 136.5 mm in past 24 h; Hulhule 117.4 mm",
    "The continuous rainfall, which began Friday night, led to flooding in several areas of the capital.", "en", "",
    "'Over the past five days, MNDF teams have been responding to flood-related incidents' (context for 17 Dec)", "RAIN012; GS_2024-12-20", "supports")
src("SRC0022", "SRC0022", "yes", "not shown on page; post 50798 shows 21 Dec 2024 10:33 (import: 21 Dec 08:17)", "2024-12-20/21 (overnight)",
    "explicit: Male' roads; five houses relocated", "rain", "since late last night", "roads heavily flooded", "NDMA relocated residents; 5,000 sandbags to Council",
    "MMS: highest 24 h rainfall in Male'", "ރޭ ދަންވަރުން ފެށިގެން މާލެ އަށް ކުރަމުންދާ ވިއްސާރައިގައި މަގުތަކުގައި ވަރަށް ބޮޑަށް ފެންބޮޑުވެ", "dv",
    "In the rain falling on Male' since late last night, the roads have flooded very badly", "Registered title blank; page title is about relocating five households", "RAIN012 (additional)", "supports")
src("SRC0023", "SRC0023", "yes", "3 Jan 2025 13:36", "2025-01-03", "explicit: whole of Male'; Majeedhee Magu, Ameenee Magu; Maafannu worst; Kan'baa Aisa Rani Hingun, Izzuddeen Magu",
    "rain", "since this morning", "whole of Male' flooded", "police and MNDF draining, sandbags", "",
    "މިއަދު ހެނދުނުން ފެށިގެން މެދުނުކެނޑި ވެހެމުންދާ ވާރޭގައި މުޅި މާލޭގައި ފެންބޮޑުވެ", "dv",
    "In the rain falling continuously since this morning, the whole of Male' has flooded", "rain start differs from SRC0053 (afternoon) and SRC0055 (Thursday evening)", "RAIN013", "supports")
src("SRC0024", "SRC0024", "yes", "11 January 2025 (date only)", "2025-01-10 (evening) to 2025-01-11", "explicit: Male'; eight pump areas", "rain",
    "", "since Friday evening", "13,882 t pumped as of 10 am Saturday; 46 households assisted", "Male recorded the highest rainfall in the past 24 hours (figure not extracted)",
    "Heavy rains have caused flooding in Male since Friday evening, marking the second instance of severe flooding in the city within a week.", "en", "",
    "SRC0058 places the torrential rain 'early this morning' (11 Jan)", "RAIN014", "supports")
src("SRC0025", "SRC0025", "yes", "2025-03-02 10:43 +05:00", "2025-03-01 (day and night)", "explicit: Male'; four houses, 40 people sheltered", "rain",
    "yesterday and last night", "", "NDMA temporary shelter", "",
    "އިއްޔެ އާއި ރޭ މާލެ އަށް ކުރި ވިއްސާރައިގައި ފެންބޮޑުވުމުގެ ސަބަބުން ނަޖިސް ބޭރުވުމުގެ ހާދިސާތައް ހިނގާފައިވާތީ", "dv",
    "Because sewage overflowed owing to flooding in the rain on Male' yesterday and last night", "", "RAIN015", "supports")
src("SRC0026", "SRC0026", "yes", "2025-03-11 21:04:11 published / 21:15:34 modified (no offset)", "2025-03-11", "explicit: three areas of Male'", "rain",
    "since this afternoon", "various areas flooded", "MNDF 6 pumps in 3 areas", "",
    "މިއަދު ހަވީރުން ފެށިގެން ހުއްޓާނުލާ ބޯކޮށް ވާރޭވެހުމުގެ ސަބަބުން މާލޭގެ އެކި ސަރަޙައްދުގައި ފެން ބޮޑުވެފައިވާއިރު", "dv",
    "with various areas of Male' flooded by non-stop heavy rain since this afternoon", "Import notes a reused photo; the body describes the current event", "RAIN016", "supports")
src("SRC0027", "SRC0027", "partial (area list not rendered)", "2025-04-27 23:15:05 published / 23:45 modified (no offset)", "2025-04-27", "explicit: Male'; five most flood-prone areas",
    "rain", "after sunset tonight", "Male' badly flooded", "MNDF dewatering began 'tonight 9:40'", "",
    "މިރޭ އިރުއޮއްސުނު ފަހުން މާލެއަށް ހުއްޓުމެއް ނެތި ވެހެމުންދާ ވާރޭގައި މާލޭގައި ވަނީ ވަރަށް ބޮޑަށް ފެންބޮޑުވެފައެވެ.", "dv",
    "Male' has flooded very badly in the non-stop rain since sunset tonight.", "", "RAIN017", "supports")
src("SRC0028", "SRC0028", "yes", "2025-11-26 16:04:21 (displayed, UTC+5); JSON-LD 2025-11-26T11:19:24 (UTC)", "2025-11-26", "explicit: Male' streets; seven pumps",
    "rain", "began past 1:00pm", "streets heavily flooded", "MNDF pumps", "", "Continuous rainfall in Male' began past 1:00pm, with it heavily flooding the streets.", "en", "",
    "Import calls RAIN018 a correction of 25 Nov; this source describes 26 Nov only", "RAIN018", "supports")
src("SRC0029", "SRC0029", "yes (via en02.sun.mv; see.mv returned 403)", "Nov 27, 2025 00:44", "2025-11-26 (persisting at publication)", "explicit: Male' City",
    "rain", "hours of downpour on Wednesday", "remains flooded", "pumps and sandbags", "",
    "Male' City remains flooded following hours of downpour on Wednesday.", "en", "", "Registered title blank; page title 'Male' under water; Met Office issues fresh alert'",
    "RAIN018 (additional)", "supports")
src("SRC0030", "SRC0030", "yes", "Apr 16, 2026 10:10", "2026-04-16", "explicit: roads of the capital; two locations in Maafannu", "rain", "", "April 16, 2026",
    "MNDF pumps at two Maafannu locations", "", "MNDF begins dewatering efforts in Male' as the Maldivian capital's roads were flooded due to heavy rain on April 16, 2026.", "en", "",
    "", "RAIN019; MFB_2026-04-16; legacy_review_2026-04-16", "supports", "Alias SRC0063 (see.mv/104638): identical article")
src("SRC0031", "SRC0031", "yes", "2026-07-26 22:56:02 (displayed, UTC+5); JSON-LD 2026-07-26T18:12:41 (UTC)", "2026-07-26",
    "explicit: Industrial Village, Raalhugandu, Carnival area, Boduthakurufaanu Magu", "coastal (swell waves at high tide)", "",
    "around midday", "MNDF draining", "tide: highest 0.74 m at 11:53 (datum not stated)",
    "Swell waves caused flooding and damage in several parts of Male' today, with seawater flooding roads, public areas and beachfront cafe's.", "en", "", "", "COAST003", "supports")
src("SRC0032", "SRC0032", "yes", "26 July 2026 (date only)", "2026-07-26", "explicit: Carnival area; new section of Boduthakurufaanu Magu", "coastal (tidal surges)",
    "", "early in the afternoon (Sunday)", "MNDF pumping", "", "Tidal surges began affecting parts of the city early in the afternoon, leading to water accumulating on a number of roads.",
    "en", "", "", "COAST003 (additional)", "supports")
src("SRC0033", "SRC0033", "yes", "not shown on page; bracketed by posts 4 Aug 2026 17:17-19:30 (import: 19:05)", "2026-08-04", "explicit: Male' roads", "rain (southwest monsoon)",
    "", "roads flooded at publication", "MNDF Fire and Rescue pumping", "",
    "ބޯކޮށް ވާރޭވެހި، މަގުތަކުގައި ފެންބޮޑުވުމުގެ ސަބަބުން ދަތުރުފަތުރުކުރުމަށާއި އާންމު ދިރިއުޅުމަށް ވަނީ ދަތިތަކާ ކުރިމަތިވެފައެވެ", "dv",
    "Heavy rain fell and flooding on the roads has disrupted travel and daily life", "", "RAIN020", "supports")
src("SRC0034", "SRC0034", "yes", "2026-09-12 10:13:13 (no offset)", "2026-09-12", "explicit: Male'; water entering some houses", "rain", "", "flooded at publication",
    "MNDF sandbagging", "", "މާލޭގައި ފެންބޮޑުވެފައިވާއިރު ... ބައެއް ގެތަކަށް ފެން ވަދެފައިވާތީ", "dv",
    "With Male' flooded ... because water has entered some houses", "", "RAIN021", "supports")
src("SRC0035", "SRC0035", "yes", "2026-10-21 22:58:44 (displayed, UTC+5); JSON-LD 2026-10-21T18:30:01 (UTC)", "2026-10-21", "explicit: entire city of Male'",
    "rain", "around sundown, non-stop", "many areas flooded", "MNDF draining; NDMA special operation", "",
    "rainfall that began in Malé around sundown has continued non-stop, leaving many areas flooded.", "en", "", "",
    "RAIN022; MFB_2026-10-21; legacy_review_2026-10-21", "supports", "Same article as the compiled record: RAIN022 adds no new evidence")
src("SRC0036", "SRC0036", "yes (112-page PDF)", "PDF created 2022-03-04", "2021-12-11", "explicit: Majeedhee Magu near Henveiru Ground; central Majeedhee Magu",
    "rain", "", "after rainfall on 11 December 2021", "", "",
    "Road condition after rainfall on December 11, 2021 (Near Henveiru Ground in Majeedhee Magu Rd., Male') | Figure2-1.2 Inland flooding in Male' City, 11 December 2021",
    "en", "", "", "MFB_2021-12-11; legacy_review_2021-12-11", "supports")
src("SRC0037", "SRC0037", "yes (no date on page)", "not shown", "undated (consistent with 2022-07-17 sources)", "explicit: roads near Ekuveni running track and IGMH",
    "rain", "", "", "FRS dewatering", "", "Firefighters of FRS have begun work of dewatering the roads near Ekuveni running track and IGMH area, flooded by heavy rain.",
    "en", "", "Page shows no date; date rests on SRC0003/SRC0038", "MFB_2022-07-17; legacy_review_2022-07-17", "context only (undated)")
src("SRC0038", "SRC0038", "yes (Wayback; en.sun.mv returned 403)", "Jul 17, 2022 22:10", "2022-07-17", "explicit: Boduthakurufaanu Magu, Maafannu Track area, IGMH area",
    "rain", "since Sunday afternoon", "streets flooded; water in some homes", "MNDF dispatched about 05:30 pm", "",
    "Rain has been pouring non-stop over Male' City since Sunday afternoon, flooding the streets.", "en", "", "", "MFB_2022-07-17", "supports")
src("SRC0039", "SRC0039", "yes", "1st April 2023 (date only)", "2023-04-01", "explicit: roads of Male' City; Maafannu worst", "rain",
    "'during the late hours of last night, 1st April 2023'", "roads un-walkable 'today'", "", "",
    "During the late hours of last night, 1st April 2023 there was a heavy storm resulting in a really bad downpour in Male' City.", "en", "",
    "Read with the displayed date (1 April), 'last night' is the night ending on the morning of 1 April; SRC0006 says Saturday morning",
    "MFB_2023-04-01; legacy_review_2023-04-01", "supports")
src("SRC0040", "SRC0040", "yes", "2023-07-22 09:10:53 (<time>, no offset)", "2023-07-21", "explicit: many roads in the four districts", "rain", "", "",
    "MNDF pumping", "MMS: highest rainfall at Hulhule' 08:00-11:00 on 21 July (no figure)", "the heavy rainfall has resulted in severe flooding, affecting many roads in the four districts of the city.",
    "en", "", "", "MFB_2023-07-21; legacy_review_2023-07-21", "supports")
src("SRC0041", "SRC0041", "yes (via en02.sun.mv; see.mv returned 403)", "Dec 31, 2023 11:57", "2023-12-31", "explicit: Ameenee Magu, Boduthakurufaanu Magu, Majeedhee Magu",
    "rain", "since dawn (Sunday)", "Sunday morning", "", "", "Male' City was completely flooded as heavy rain battered the Maldivian nation on Sunday morning.", "en", "", "",
    "MFB_2023-12-31", "supports")
src("SRC0042", "SRC0042", "yes", "31 December 2023 (date only)", "2023-12-31 (flooding); 2023-12-30 (rain start)", "explicit: Male; four houses in Henveiru; houses near West Park",
    "rain", "continuous downpour since Saturday morning", "flooding reported Sunday", "pumps in six areas", "",
    "There has been a continuous downpour in Male since Saturday morning.", "en", "", "Flooding on Saturday 30 Dec is not stated",
    "MFB_2023-12-31; legacy_review_2023-12-31; GS_2023-12-30; GS_2023-12-31", "supports")
src("SRC0043", "SRC0043", "yes", "2024-01-01T18:18:00+00:00", "2023-12-31", "explicit: Male'; over 140 homes", "rain", "", "Sunday", "NDMA sandbags; 54 people relocated",
    "Hulhule 179.9 mm 'within 24 hours' (record); Male' 118.2 mm",
    "The Met Office documented a record 179.9 millimetres of rain on Hulhule Island within 24 hours", "en", "", "179.9 conflicts with 179.7 in SRC0012 and SRC0069",
    "MFB_2023-12-31", "supports")
src("SRC0044", "SRC0044", "yes (via en02.sun.mv; s1.see.mv returned 403)", "Jan 12, 2024 13:20", "2024-01-12", "explicit: flour warehouse, IGMH, West Park, Boduthakurufaanu Magu",
    "rain", "", "streets flooded at publication", "soldiers pumping", "", "Soldiers have been deployed to drain the flooded streets of Male' City amid torrential rain.", "en", "",
    "", "MFB_2024-01-12; legacy_review_2024-01-12", "supports", "Legacy review recorded this source as blocked; it is readable on en02.sun.mv")
src("SRC0045", "SRC0045", "yes", "approved 2024-08-14T10:23:42 (no offset)", "2024-08-13", "explicit: all parts of the city; IGMH, West Park and others", "rain",
    "", "Tuesday", "MNDF at 10+ areas by Tuesday evening", "Male' 89.4 mm between 8am Tuesday and 8am Wednesday",
    "The capital, Malé City was lashed by 89.4 millimeters of rainfall between 8am Tuesday to 8am Wednesday, flooding all parts of the city", "en", "", "",
    "MFB_2024-08-13; legacy_review_2024-08-13", "supports")
src("SRC0046", "SRC0019", "yes (duplicate)", "same as SRC0019", "2024-08-13", "", "", "", "", "", "", "", "", "", "", "MFB_2024-08-13", "duplicate of SRC0019")
src("SRC0047", "SRC0047", "yes (via en02.sun.mv; s1.see.mv returned 403)", "Aug 14, 2024 14:01", "2024-08-13", "explicit: Male'", "rain", "", "Tuesday", "",
    "Male' 89.4 mm on Tuesday (AWS); Thoddoo 70.6; Hulhumale' 63.4. MMS official to PSM: Male' 'prone to flooding with just 40 or 45 millimeters'",
    "Given that Male' is prone to flooding with just 40 or 45 millimeters of rainfall, 80 millimeters of rainfall is double that", "en", "",
    "Compiled record says 'Hulhule 63.4 mm'; this source gives 63.4 mm for Hulhumale'. The 40-45 mm remark is an official's quote, not a published threshold",
    "MFB_2024-08-13", "supports")
src("SRC0048", "SRC0048", "yes", "2024-08-14T15:43:53+00:00", "2024-08-13", "explicit: Male'; 256 households flooded", "rain", "", "Tuesday", "NDMA; 23 people sheltered",
    "Male' 89.4 mm 'over the past 48 hours'", "In the capital city of Malé, 256 households were flooded.", "en", "", "48 h window conflicts with 24 h in SRC0045",
    "MFB_2024-08-13", "supports")
src("SRC0049", "SRC0049", "yes (via en02.sun.mv; see.mv returned 403)", "Dec 21, 2024 11:20", "2024-12-20/21", "explicit: West Park, IGMH, Vilimale' Ferry Terminal, Dhiraagu, Jelly pizzeria",
    "rain", "", "", "16 pumps; sandbags", "MMS: Male' City 136.5 mm, 08:00 Friday to 08:00 Saturday; Hulhumale' 117 mm",
    "the heaviest rainfall over the last 24 hours - from 08:00 am Friday to 08:00 am Saturday - was recorded in Male' City with 136.5 millimeters.", "en", "",
    "Photo caption dated December 31, 2023 (reused photo, not evidence). 117 mm attributed to Hulhumale' here, to Hulhule in SRC0018/SRC0021",
    "MFB_2024-12-20", "supports")
src("SRC0050", "SRC0050", "yes", "28 December 2024 (date only)", "context: 'last weekend' (20-21 Dec 2024)", "explicit: IGMH and STO flour warehouse areas", "rain",
    "", "last weekend", "", "", "Heavy rainfall last weekend caused significant flooding, particularly in areas near the Indira Gandhi Memorial Hospital (IGMH) and the State Trading Organization (STO) flour warehouse.",
    "en", "", "", "MFB_2024-12-20; legacy_review_2024-12-20", "context only (retrospective)")
src("SRC0051", "SRC0051", "yes", "2024-12-28 16:58:10 (displayed, UTC+5)", "context: road closure for flood repairs", "explicit: Majeedhee Magu, Dhanburu Magu to Nikagas Magu",
    "not an event report", "", "", "", "", "This is the area that floods the most during the rainy season in Malé.", "en", "", "", "MFB_2024-12-20", "context only")
src("SRC0052", "SRC0052", "yes", "04 Jan 2025 (date only)", "states 'January 4, 2025'", "explicit: Majeedhee Magu, Ameenee Magu, Kan'ba Aisa Rani Hingun", "rain", "", "",
    "NDMA 774 requests", "", "Heavy rainfall on January 4, 2025 has caused significant flooding across the Maldives", "en", "",
    "Date wording conflicts with SRC0023/SRC0053/SRC0056 (Friday 3 Jan); probably the publication date", "MFB_2025-01-03", "supports with date conflict")
src("SRC0053", "SRC0053", "yes", "2025-01-04 13:00:57 (JSON-LD, no offset)", "2025-01-03 (afternoon to late night)", "explicit: Male'; West Park, IGMH, Salman Mosque, Maafannu Ferry Terminal, Kudakudhinge Bageecha, Voice of Maldives",
    "rain", "Friday from afternoon until late night", "extensive flooding", "MNDF pumping 11:37 Fri to 08:30 Sat", "MET: Male' 142.6 mm on Friday; Hulhule 144 mm 08:00 Fri to 08:00 Sat",
    "Male' experienced heavy rainfall on Friday from afternoon until late night, causing extensive flooding across the island.", "en", "", "142.6 here vs 142.2 in SRC0056",
    "MFB_2025-01-03; legacy_review_2025-01-03; GS_2025-01-02; GS_2025-01-03", "supports")
src("SRC0054", "SRC0054", "yes (Wayback; see.mv returned 403)", "January 04, 2025 12:15", "2025-01-03 to early 2025-01-04", "explicit: Male' roads", "rain", "nonstop heavy rain on Friday",
    "flooded until early Saturday morning", "pumping 11:37 Fri to 08:30 Sat (21 h)", "", "Majority of Male' City was flooded until early Saturday morning.", "en", "", "",
    "MFB_2025-01-03", "supports")
src("SRC0055", "SRC0055", "yes", "2025-01-04T14:02:00+00:00", "2025-01-03 (rain from Thursday 2 Jan evening)", "explicit: Male'", "rain", "began on Thursday evening", "", "30,569 t pumped",
    "Male' 162 mm and Hulhumale 164 mm as of 11:00 p.m. on Friday", "Rains that began on Thursday evening inundated the capital, Malé, damaging homes and businesses.", "en", "",
    "Rain start (Thursday evening) differs from SRC0023 and SRC0053", "MFB_2025-01-03", "supports")
src("SRC0056", "SRC0056", "yes", "4 January 2025 (date only)", "2025-01-03", "explicit: Male'; 774 incidents", "rain", "", "Friday", "NDMA shelter for 226",
    "Hulhule 144 mm, Male 142.2 mm on Friday", "heavy rains that caused significant flooding across the city on Friday.", "en", "", "", "MFB_2025-01-03", "supports")
src("SRC0057", "SRC0057", "yes", "2025-01-11T05:29:03+05:00", "2025-01-10/11 (overnight)", "explicit: West Park, IGMH, Boduvalhu", "rain",
    "began in the early evening and intensified by midnight", "overnight", "MNDF through the night", "",
    "The downpour, part of the ongoing monsoon season, began in the early evening and intensified by midnight, inundating several areas of the city.", "en", "", "",
    "MFB_2025-01-11; legacy_review_2025-01-11; GS_2025-01-10", "supports")
src("SRC0058", "SRC0058", "yes", "2025-01-11T10:53:57+05:00", "2025-01-11 (early morning)", "explicit: Male'; eight areas; 58 households", "rain", "torrential rain early this morning",
    "", "23 pumps; 13,882 t pumped", "MMS: Male' 130.7 mm from 8:00 AM 10 Jan to 8:00 AM 11 Jan; Hulhumale' 79.5 mm",
    "flooding in Male' from the torrential rain early this morning", "en", "", "Differs from SRC0024 ('since Friday evening')", "MFB_2025-01-11", "supports")
src("SRC0059", "SRC0059", "yes", "01 Mar 2025 (date only)", "2025-03-01 (after sunset)", "explicit: Male' streets", "rain", "shortly after sunset, about two hours",
    "street flooding", "MNDF pumps and sandbags", "orange warning 9:45 pm 1 Mar to 2 am 2 Mar",
    "Heavy rainfall continued for approximately two hours after sunset in the Malé area, causing street flooding", "en", "", "",
    "MFB_2025-03-01; legacy_review_2025-03-01; GS_2025-02-28", "supports")
src("SRC0060", "SRC0060", "yes", "2025-03-02 12:30:43 (displayed, UTC+5)", "2025-03-01 (pumps used 'past two days')", "explicit: IGMH, West Park, Maafannu ferry terminal", "rain",
    "", "", "pumps at 10 locations; 1,000 t by 10 pm last night", "", "Water pumps were installed at 10 key locations, including the IGMH area, West Park, and the Maafannu ferry terminal.",
    "en", "", "", "MFB_2025-03-01", "supports")
src("SRC0061", "SRC0061", "yes", "12 Mar 2025 (date only)", "2025-03-11 (Tuesday evening onward)", "explicit: IGMH, Westpark, Maafannu Ferry Terminal", "rain",
    "since Tuesday evening", "widespread flooding", "six pumps since Tuesday afternoon", "", "Since Tuesday evening, continuous rainfall had led to widespread flooding across the city.", "en", "", "",
    "MFB_2025-03-11; legacy_review_2025-03-11", "supports")
src("SRC0062", "SRC0062", "yes", "Nov 25, 2025 (page clock labelled MVT)", "2025-11-25", "explicit: Maafannu; near IGMH; near Ameeniyya School", "rain", "since early morning Tuesday",
    "parts of Male' flooded", "no pumps as of 7:00 am", "", "Heavy continuous rain since early morning Tuesday has caused flooding in parts of Male' city.", "en", "", "",
    "MFB_2025-11-25; legacy_review_2025-11-25", "supports")
src("SRC0063", "SRC0030", "yes (duplicate; Wayback)", "same as SRC0030", "2026-04-16", "", "", "", "", "", "", "", "", "", "", "MFB_2026-04-16", "duplicate of SRC0030")
src("SRC0064", "SRC0064", "yes (Wayback; see.mv returned 403)", "May 04, 2026 10:31", "2026-05-04", "explicit: IGMH, Maafannu Ferry Terminal, Salman Mosque, Swimming Track",
    "rain", "Monday", "streets flooded", "soldiers dewatering", "", "Maldives National Defense Force (MNDF) deployed soldiers on Monday, after heavy rain flooded the streets of Male' City.", "en", "",
    "", "MFB_2026-05-04; legacy_review_2026-05-04", "supports", "Legacy review recorded this source as blocked; it is readable via Wayback")
src("SRC0065", "SRC0065", "yes", "2026-07-30 14:18 +05:00", "2026-07-30", "explicit: new section of Boduthakurufaanu Magu", "rain (permanent drainage pumps not yet commissioned)",
    "Thursday", "temporary flooding", "MNDF portable pumps", "", "Heavy rainfall on Thursday caused temporary flooding along parts of the newly developed road.", "en", "", "",
    "MFB_2026-07-30; legacy_review_2026-07-30", "supports")
src("SRC0066", "SRC0066", "yes", "approved 2026-07-30T18:07:23 (no offset)", "2026-07-30", "explicit: Boduthakurufaanu Magu new section", "rain", "Thursday", "significant flooding across the road", "", "",
    "heavy rainfall on Thursday caused significant flooding across the road.", "en", "", "", "MFB_2026-07-30", "supports")
src("SRC0067", "SRC0067", "yes", "2026-10-22 16:14:03 (displayed, UTC+5)", "2026-10-21 (night)", "explicit: Male'; 89 buildings", "rain", "last night's non-stop rainfall", "", "10,000 sand sacks",
    "Male' 90 mm in the last 24 hours", "more than 80 reports where buildings flooded during last night's non-stop rainfall in Male'.", "en", "", "", "MFB_2026-10-21", "supports")
src("SRC0068", "SRC0068", "yes", "2026-10-24 14:28:59 (displayed, UTC+5)", "Hulhumale' cemetery, 24 Oct", "not Male' island (Hulhumale')", "groundwater/rain", "", "", "", "",
    "Burials at Hulhumale' cemetery have been suspended due to flooding", "en", "", "", "MFB_2026-10-21", "context only (not Male' island)")
src("SRC0069", "SRC0069", "yes (144-page PDF)", "PDF created 2025-09-26", "2023-12-31; 2024-01-12 (hazard summary)", "explicit: Male' city", "rain (surface water flooding)", "", "",
    "", "31 Dec 2023: 179.7 mm (highest in 26 years); 12 Jan 2024: 143.4 mm; January 2024 flash floods: 110 mm within three hours",
    "31 Dec 2023: 179.7 mm rainfall (highest in 26 years) | 12 Jan 2024: 143.4 mm rainfall", "en", "", "City-scale summary; source cited as NDMA / Draft City Disaster Management Plan 2025",
    "SP_2023-12-31", "supports")
src("SRC0070", "SRC0070", "yes", "not shown", "2004-12-26", "explicit: two-thirds of the capital city", "coastal (tsunami)", "", "first hours of the day", "", "",
    "Two-thirds of the capital city was flooded during the first hours of the day.", "en", "", "Outside the 2020-2026 study period", "GS_2004-12-26", "supports")
src("SRC0071", "SRC0071", "yes", "2019-06-15 14:34 (UTC+5 by site clock test)", "2019-06-15", "explicit: Alimas Carnival, Raalhugandu, Artificial Beach, Boduthakurufaanu Magu, Industrial Village",
    "coastal (tidal swells)", "", "Saturday morning and afternoon", "", "", "Tidal swells have resulted in flooding in parts of the capital, Male' City.", "en", "",
    "'Repeatedly affected ... this weekend' (Maldivian weekend is Friday-Saturday); 16 June not supported. Outside study period", "GS_2019-06-15", "supports")
assert set(S) == set(reg), set(reg) ^ set(S)

OFFICIAL_COPY = {
    "SRC0011": "01_raw/flood_evidence/official_records/ndma_male_city_incident_statistics_page_20261122.html",
    "SRC0018": "01_raw/flood_evidence/official_records/mms_severe_weather_report_2024_wayback_20260218151135.pdf",
    "SRC0020": "01_raw/flood_evidence/official_records/ndma_annual_report_2024_vzrqjkea.pdf",
    "SRC0036": "01_raw/flood_evidence/official_records/jica_12368783_climate_disaster_survey_male_2022.pdf",
    "SRC0037": "01_raw/flood_evidence/official_records/mndf_news_article_3928_page_20261122.html",
    "SRC0069": "01_raw/flood_evidence/official_records/male_city_council_vlr_2025.pdf",
    "SRC0070": "01_raw/flood_evidence/official_records/ndma_tsunami_gallery_page_20261122.html",
}
sv = []
for sid in sorted(S):
    r = reg[sid]; f = fetch.get(sid, {}); s = S[sid]
    tzs, tzb = tz(f.get("final_url", r["url"]))
    sv.append(dict(source_id=sid, canonical_source_id=s["canonical_source_id"], publisher=r["publisher"], url_registered=r["url"],
                   url_checked=f.get("final_url", ""), access_method=f.get("attempt", ""), http_status=f.get("http_code", ""),
                   checked_at_utc=f.get("fetched_at_utc", ""), body_accessible=s["body_accessible"], language=r["language"],
                   title_registered=r["title"], publication_as_displayed=s["publication_as_displayed"],
                   publication_timezone_status=tzs, publication_timezone_basis=tzb,
                   event_dates_supported=s["event_dates_supported"], male_island_evidence=s["male_island_evidence"], cause_stated=s["cause_stated"],
                   rain_timing=s["rain_timing"], flood_timing=s["flood_timing"], response_timing=s["response_timing"],
                   rainfall_statements=s["rainfall_statements"], excerpt_original=s["excerpt_original"], excerpt_language=s["excerpt_language"],
                   excerpt_english=s["excerpt_english"] or ("(original is English)" if s["excerpt_original"] else ""),
                   translation_note=TR if s["excerpt_language"] == "dv" else "",
                   conflicts=s["conflicts"], records_supported=s["records"], relation_to_records=s["relation_to_records"],
                   local_evidence_path=OFFICIAL_COPY.get(sid, ""),
                   copy_policy="official copy saved; reuse terms to confirm before redistribution" if sid in OFFICIAL_COPY else "no copy stored (publisher copyright); URL, metadata and short excerpt only",
                   reviewer=REVIEWER, reviewed_on=REVIEWED_ON, note=s["note"]))
SV_COLS = list(sv[0].keys())
w("00_catalog/source_verification.csv", sv, SV_COLS)

# ------------------------------------------------------------------ events
E = []
def ev(eid, start, end, cert, decision, ftype, scope, loc, onset, rain, resp, tsrc, links, originals, conflicts="", rainfall="", notes="", legacy="", period="in_study_period"):
    E.append(dict(event_id=eid, event_start_date=start, event_end_date=end, date_certainty=cert, decision=decision, flood_type=ftype,
                  evidence_scope=scope, location_as_reported=loc, flood_onset_time_local=onset, rain_start_time_local=rain,
                  response_start_time_local=resp, timing_evidence_source_id=tsrc, links=links, original_record_ids=originals,
                  conflicts=conflicts, rainfall_statements=rainfall, notes=notes, legacy_decision=legacy, study_period=period))
SYN = "Hulhule SYNOP 6/12 h groups (UTC; local = +5 h): "
ev("EVT0001", "2020-05-18", "2020-05-18", "single_day", "mixed_or_uncertain_cause", "mixed_rain_and_swell", "citywide_with_landmarks",
   "Many areas of Male', especially Maafannu; pumps at IGMH, STO flour warehouse, West Park", "unknown", "evening, about 2 h before 22:09 publication (approximate)",
   "pumping under way by publication", "SRC0001", [("SRC0001", "supports", "2020-05-18", "2020-05-18", "Male' island explicit", "mixed")], "RAIN001",
   "Rain flooding and swells entering Male' reported in the same evening; mechanisms not separable from the article")
ev("EVT0002", "2021-12-11", "2021-12-12", "both_days_reported", "accepted_reported_rain_event", "rain", "street",
   "Majeedhee Magu near Henveiru Ground and central Majeedhee Magu (JICA photographs); Male'", "unknown", "11 Dec (Ras: 'yesterday')", "unknown", "SRC0002;SRC0036",
   [("SRC0036", "supports", "2021-12-11", "2021-12-11", "Male' streets named", "accepted"), ("SRC0002", "supports", "2021-12-11", "2021-12-12", "Male' explicit", "accepted")],
   "RAIN002;MFB_2021-12-11;LEGACY_REVIEW_2021-12-11", "12 Dec rests on one source (Ras)",
   "Nasheed tweet (quoted by Ras): 'Male' area' 134.7 mm in past 24 h; station and window end not stated",
   "Legacy 'uncertain' (photo date not independently established) superseded: Ras independently reports flooding on 11 Dec", "uncertain")
ev("EVT0003", "2022-07-17", "2022-07-17", "single_day", "accepted_reported_rain_event", "rain", "street",
   "Many roads; Boduthakurufaanu Magu; Dhuvaa/Maafannu track area (Ekuveni); IGMH area", "unknown", "afternoon (Sunday)", "17:30 (MNDF pumping)", "SRC0003;SRC0038",
   [("SRC0003", "supports", "2022-07-17", "2022-07-17", "Male' roads named", "accepted"), ("SRC0038", "supports", "2022-07-17", "2022-07-17", "Male' roads named", "accepted"),
    ("SRC0037", "context_only", "", "", "undated official page", "context")], "RAIN003;MFB_2022-07-17;LEGACY_REVIEW_2022-07-17", legacy="include")
ev("EVT0004", "2022-11-05", "2022-11-05", "single_day", "accepted_reported_coastal_event", "coastal_swell", "landmark",
   "Alimas Carnival area and neighbouring streets (Henveiru)", "morning, at high tide", "", "Council crew on site", "SRC0004",
   [("SRC0004", "supports", "2022-11-05", "2022-11-05", "Male' landmark named", "accepted"), ("SRC0005", "supports", "2022-11-05", "2022-11-05", "Male' landmark named", "accepted")], "COAST001")
ev("EVT0005", "2023-04-01", "2023-04-01", "single_day", "accepted_reported_rain_event", "rain", "street",
   "Male' city; West Park area worst-hit; M. Bihuge, Haveeree Hingun (Maafannu); Maafannu district", "Saturday morning (reported)",
   "late night 31 Mar / early 1 Apr (mfr) vs Saturday morning (Atoll Times): unresolved", "MNDF several hours after water entered houses", "SRC0006;SRC0039",
   [("SRC0006", "supports", "2023-04-01", "2023-04-01", "Male' places named", "accepted"), ("SRC0039", "supports", "2023-04-01", "2023-04-01", "Male' explicit", "accepted")],
   "RAIN004;MFB_2023-04-01;LEGACY_REVIEW_2023-04-01",
   "Time-of-day wording differs. Earlier 'low rainfall' conflict is resolved: GSOD 1 Apr covers 05:00 31 Mar to 05:00 1 Apr local; the Saturday-morning rain is in the 6-h group 05:00-11:00 local 1 Apr = 49.0 mm; GSOD 2 Apr (4.8 mm) is one-tenth of it (24-h group defect). ERA5 0.9 mm reflects reanalysis, not observation",
   SYN + "05:00-11:00 local 1 Apr 2023 = 49.0 mm (6-h group, q1); 24-h group ending 00 UTC 2 Apr = 4.9 mm (one-tenth)",
   "Legacy 'uncertain' (publication date vs 'last night') superseded: mfr is dated 1 April, so 'last night' is the night ending on 1 April", "uncertain")
ev("EVT0006", "2023-05-04", "2023-05-04", "single_day", "accepted_reported_rain_event", "rain", "street", "Majeedhee Magu, Izzuddin Magu, IGMH; homes and shops",
   "unknown", "overnight 3-4 May (rain window cited 20:00 Wed-08:00 Thu)", "", "SRC0007", [("SRC0007", "supports", "2023-05-04", "2023-05-04", "Male' streets named", "accepted")],
   "RAIN005", "Single source", "MMS via Sun: Hulhule 58 mm, 20:00 3 May to 08:00 4 May (12 h)")
ev("EVT0007", "2023-07-21", "2023-07-21", "single_day", "accepted_reported_rain_event", "rain", "citywide", "Many roads in the four districts of Male' City", "unknown",
   "from midnight Thursday into Friday morning", "MNDF pumping (time not given)", "SRC0008", [("SRC0008", "supports", "2023-07-21", "2023-07-21", "Male' districts", "accepted"),
   ("SRC0040", "supports", "2023-07-21", "2023-07-21", "Male' districts", "accepted")], "RAIN006;MFB_2023-07-21;LEGACY_REVIEW_2023-07-21", "",
   "MMS via Sun: Hulhule 71 mm between 08:00 and 11:00 Friday 21 Jul", legacy="include")
ev("EVT0008", "2023-07-31", "2023-07-31", "single_day", "accepted_reported_coastal_event", "coastal_swell", "landmark", "'Mary Brown' area, Male' (NDMA 'Surges' entry)",
   "unknown", "", "", "SRC0011", [("SRC0011", "supports", "2023-07-31", "2023-07-31", "NDMA island 'Male''", "accepted")], "NEW_NDMA_2023-07-31",
   "Single official table row; not imported before; no news source checked", notes="Found during this verification on the NDMA statistics page")
ev("EVT0009", "2023-08-05", "2023-08-05", "single_day", "accepted_reported_coastal_event", "coastal_swell", "street",
   "Henveiru surf point (Raalhugandu); Boduthakurufaanu Magu; artificial beach (bridge/highway also affected, not Male' island)", "from about 14:00", "", "police advisory from 15:00",
   "SRC0009", [("SRC0009", "supports", "2023-08-05", "2023-08-05", "Male' places named", "accepted"), ("SRC0011", "supports", "2023-08-05", "2023-08-05", "NDMA island 'Male''", "accepted"),
   ("SRC0010", "context_only", "2023-08-05", "2023-08-06", "bridge photo; capital on 6 Aug", "context")], "COAST002;GS_2023-08-05_2023-08-06;NEW_NDMA_2023-08-05")
ev("EVT0010", "2023-08-06", "2023-08-06", "single_day", "uncertain_location", "coastal_swell", "unresolved", "'the capital' (Sun); Male' island flooding not stated", "peak tide hours Sunday",
   "", "", "SRC0010", [("SRC0010", "supports", "2023-08-06", "2023-08-06", "'including the capital' only", "uncertain_location")], "COAST002;GS_2023-08-05_2023-08-06",
   "Swells 'lashed the shore of ... the capital' on Sunday; no Male' island flooding statement")
ev("EVT0011", "2023-10-01", "2023-10-01", "single_day", "accepted_reported_rain_event", "rain", "property", "M. Kandaru (Maafannu)", "unknown", "", "", "SRC0011",
   [("SRC0011", "supports", "2023-10-01", "2023-10-01", "one property", "accepted")], "OFF001;SP_2023-10-01", "Single official register row (property level)")
ev("EVT0012", "2023-12-30", "2023-12-30", "rain_reported_flood_not_dated", "uncertain_date", "rain", "unresolved", "Male' (rain since Saturday morning)", "unknown", "Saturday morning 30 Dec",
   "", "SRC0042", [("SRC0042", "supports", "2023-12-30", "2023-12-31", "rain from 30 Dec; flooding reported 31 Dec", "uncertain_date")],
   "MFB_2023-12-31;LEGACY_REVIEW_2023-12-31;GS_2023-12-30_2024-01-01", "Atoll Times reports continuous rain since Saturday but does not date any flooding to Saturday",
   SYN + "17:00 29 Dec-05:00 30 Dec 21 mm; 17:00 30 Dec-05:00 31 Dec 38 mm (q2)", legacy="uncertain (30 Dec)")
ev("EVT0013", "2023-12-31", "2023-12-31", "single_day", "accepted_reported_rain_event", "rain", "street",
   "Ameenee Magu, Boduthakurufaanu Magu, Majeedhee Magu; four houses in Henveiru; houses near West Park; pumps in six areas", "Sunday morning (Sun: since dawn)",
   "since dawn Sunday (Sun) / since Saturday morning (Atoll Times)", "pumps in six areas (time not given)", "SRC0041;SRC0042",
   [("SRC0041", "supports", "2023-12-31", "2023-12-31", "Male' roads named", "accepted"), ("SRC0042", "supports", "2023-12-31", "2023-12-31", "Male' wards named", "accepted"),
    ("SRC0043", "supports", "2023-12-31", "2023-12-31", "Male' explicit", "accepted"), ("SRC0012", "supports", "2023-12-31", "2023-12-31", "Male' houses", "accepted"),
    ("SRC0069", "supports", "2023-12-31", "2023-12-31", "city summary", "accepted"), ("SRC0013", "context_only", "2023-12-31", "2023-12-31", "retrospective mention", "context")],
   "RAIN007;MFB_2023-12-31;LEGACY_REVIEW_2023-12-31;SP_2023-12-31;GS_2023-12-30_2024-01-01;GS_2023-12-31_2024-01-01",
   "RAIN007 rainfall conflict resolved: the 4.3 mm was GSOD 31 Dec, i.e. the 24 h ending 05:00 local 31 Dec (before the storm). The storm falls in GSOD 1 Jan (18.8 mm), whose source 24-h group (18.9) is one-tenth of the 12-h groups (184.0 + 5.0)",
   "Hulhule 179.7 mm 08:00 Sun 31 Dec-08:00 Mon 1 Jan (MET via Atoll Times; Council VLR); 179.9 mm 'within 24 hours' (MVRepublic only; unsupported digit); Male' 118.2 mm (MVRepublic, Atoll Times). " + SYN + "05:00-17:00 local 31 Dec = 184.0 mm (12-h group, q1); 17:00 31 Dec-05:00 1 Jan = 5.0 mm",
   legacy="include")
ev("EVT0014", "2024-01-10", "2024-01-10", "single_day", "accepted_reported_rain_event", "rain", "street",
   "Boduthakurufaanu Magu near Boduvalhu; Kudakudhinge Bageecha; (compiled: West Park, STO flour warehouse)", "evening (Wednesday)", "since evening", "MNDF out Wednesday evening",
   "SRC0013", [("SRC0013", "supports", "2024-01-10", "2024-01-10", "Male' places named", "accepted"), ("SRC0020", "supports", "2024-01-10", "2024-01-10", "NDMA #13 Male' City", "accepted")],
   "RAIN008;MFB_2024-01-10;LEGACY_REVIEW_2024-01-10", "", SYN + "11:00-17:00 local 27.7 mm; 17:00-23:00 50.0 mm; 23:00-05:00 1.0 mm; 24-h group ending 00 UTC 11 Jan 8.0 mm (q2, one-tenth)",
   legacy="include")
ev("EVT0015", "2024-01-12", "2024-01-12", "single_day", "accepted_reported_rain_event", "rain", "street",
   "Ameenee Magu; STO flour warehouse, IGMH, West Park, Boduthakurufaanu Magu; 227 places / 144 homes requesting help", "unknown",
   "since early morning Friday (Plus)", "soldiers pumping by 13:20", "SRC0015;SRC0044",
   [("SRC0044", "supports", "2024-01-12", "2024-01-12", "Male' places named", "accepted"), ("SRC0014", "supports", "2024-01-12", "2024-01-12", "Male' streets", "accepted"),
    ("SRC0015", "supports", "2024-01-12", "2024-01-12", "Male' explicit", "accepted"), ("SRC0018", "supports", "2024-01-12", "2024-01-12", "MMS: 227 places in Male'", "accepted"),
    ("SRC0020", "supports", "2024-01-12", "2024-01-12", "NDMA #14 Male' City", "accepted"), ("SRC0069", "context_only", "2024-01-12", "2024-01-12", "city summary", "context")],
   "RAIN009;MFB_2024-01-12;LEGACY_REVIEW_2024-01-12;SP_2024-01-12;GS_2024-01-12_2024-01-12",
   "Station attribution conflict: Sun gives Hulhumale 143.4 / Hulhule 105.4; MMS report gives Hulhule NMC 143.4 / Hulhumale AWS 105.4",
   "MMS: AWS Male' 159.3 mm (24 h, labelled 12 Jan). " + SYN + "05:00 12 Jan-05:00 13 Jan local = 156 mm (12-h pairs 90 + 66); 24-h group 15.6 mm (q2 suspect, one-tenth)",
   "Legacy 'uncertain' (source blocked; possible same storm as 10 Jan) superseded: source readable; storm relation handled in storm groups", "uncertain")
ev("EVT0016", "2024-01-13", "2024-01-13", "register_date_only", "uncertain_date", "rain", "citywide", "NDMA register: 'Male' City'", "unknown", "", "", "SRC0020",
   [("SRC0020", "supports", "2024-01-13", "2024-01-13", "NDMA #1 Male' City", "uncertain_date")], "NEW_NDMA_2024-01-13",
   "No article describes new flooding on 13 Jan; the register date may be a response/assessment date for the 12 Jan event",
   SYN + "17:00 12 Jan-05:00 13 Jan 66 mm; 05:00-11:00 13 Jan 0 mm")
ev("EVT0017", "2024-02-16", "2024-02-16", "single_day", "accepted_reported_rain_event", "rain", "citywide", "Male' (MMS figure caption citing MNDF flood reports)", "unknown", "", "",
   "SRC0018", [("SRC0018", "supports", "2024-02-16", "2024-02-16", "Male' explicit", "accepted")], "NEW_MMS_2024-02-16",
   "Single official caption ('Flood reports by MNDF due to heavy rain in Male' on 16th Feb'); not imported before", notes="Found during this verification")
ev("EVT0018", "2024-04-13", "2024-04-13", "single_day_with_persistence", "accepted_reported_rain_event", "rain", "citywide", "Male' streets and residences; 85 buildings; five houses relocated",
   "Saturday (morning per Sun, afternoon per Edition)", "Saturday morning (Sun) vs Saturday afternoon (Edition): unresolved", "MNDF engaged (time not given)", "SRC0016;SRC0017",
   [("SRC0016", "supports", "2024-04-13", "2024-04-14", "Male' streets", "accepted"), ("SRC0017", "supports", "2024-04-13", "2024-04-13", "Male' streets", "accepted"),
    ("SRC0020", "supports", "2024-04-13", "2024-04-13", "NDMA #52 Male' City", "accepted")], "RAIN010;GS_2024-04-13_2024-04-14",
   "Intraday timing unresolved. Streets still flooded at Edition's 00:00 14 Apr publication: persistence, not a new flood day",
   SYN + "05:00-11:00 local 0 mm; 11:00-17:00 86 mm; 17:00-23:00 20 mm; 23:00-05:00 3 mm (Hulhule, not Male')")
ev("EVT0019", "2024-05-08", "2024-05-08", "single_day", "accepted_reported_rain_event", "rain", "unspecified_areas", "'some areas of Male'' (MMS)", "unknown", "", "", "SRC0018",
   [("SRC0018", "supports", "2024-05-08", "2024-05-08", "Male' explicit, no places", "accepted")], "OFF002", "Single official statement; no NDMA register entry for this date")
ev("EVT0020", "2024-05-25", "2024-05-25", "single_day", "accepted_reported_rain_event", "rain", "citywide", "'Male' City reported floods' (MMS)", "unknown", "", "", "SRC0018",
   [("SRC0018", "supports", "2024-05-25", "2024-05-25", "Male' City; AWS Male' 40.4 mm", "accepted")], "NEW_MMS_2024-05-25",
   "Single official statement; 'Male' City' wording", "MMS: 40.4 mm at AWS Male' on 25 May", notes="Found during this verification")
ev("EVT0021", "2024-08-13", "2024-08-13", "single_day", "accepted_reported_rain_event", "rain", "street",
   "Nearly all streets; IGMH, West Park, Pizza Buona, Dhiraagu, Dharubaaruge; Rasfannu; Ameenee Magu; 256 households", "late morning onward", "around 11:00", "Police/MNDF by 14:29",
   "SRC0019", [("SRC0019", "supports", "2024-08-13", "2024-08-13", "Male' streets", "accepted"), ("SRC0045", "supports", "2024-08-13", "2024-08-13", "Male' places", "accepted"),
    ("SRC0047", "supports", "2024-08-13", "2024-08-13", "Male' explicit", "accepted"), ("SRC0048", "supports", "2024-08-13", "2024-08-13", "Male' households", "accepted"),
    ("SRC0020", "supports", "2024-08-13", "2024-08-13", "NDMA #167 Male' City", "accepted"), ("SRC0046", "possible_duplicate", "2024-08-13", "2024-08-13", "alias of SRC0019", "duplicate")],
   "RAIN011;MFB_2024-08-13;LEGACY_REVIEW_2024-08-13;GS_2024-08-12_2024-08-14",
   "Rainfall windows conflict: 24 h (raajje) vs 48 h (MVRepublic); compiled 'Hulhule 63.4' is Hulhumale' in Sun",
   "Male' 89.4 mm 08:00 Tue-08:00 Wed (raajje); MMS report: Male' AWS 85 mm (date not stated)", legacy="include")
ev("EVT0022", "2024-08-14", "2024-08-14", "caption_date_only", "uncertain_date", "rain", "citywide", "MMS Fig. 27: 'August 14 MNDF photo of flooding in Male''", "unknown", "", "", "SRC0018",
   [("SRC0018", "supports", "2024-08-14", "2024-08-14", "photo caption", "uncertain_date")], "NEW_MMS_2024-08-14;LEGACY_REVIEW_2024-08-13",
   "Caption date may be the posting date of a 13 Aug photo", legacy="uncertain (14 Aug)")
ev("EVT0023", "2024-09-18", "2024-09-18", "single_day", "accepted_reported_rain_event", "rain", "property", "H. Dhoohimerige - Hulhangubai - Print (Henveiru)", "unknown", "", "", "SRC0020",
   [("SRC0020", "supports", "2024-09-18", "2024-09-18", "NDMA #193, one property", "accepted")], "OFF003",
   "OFF003 conflict resolved as separate incidents: case #194 (18 Sep) is a fire at G. Sindhu Hiya; assistance row 69 ('Fire Incidents', 18-Sep-2024) matches #194; no rainwater assistance row for 18 Sep. Context: the same property had a fire on 9 Sep (#190)",
   notes="Property-level register record")
ev("EVT0024", "2024-10-11", "2024-10-11", "single_day", "accepted_reported_rain_event", "rain", "property", "M. Bihuge; M. Raindrop (Maafannu)", "unknown", "", "", "SRC0020",
   [("SRC0020", "supports", "2024-10-11", "2024-10-11", "NDMA #208, #209", "accepted"), ("SRC0018", "context_only", "2024-10-05", "2024-10-11", "Male' images 5th/11th Oct", "context")],
   "OFF004;GS_2024-10-11_2024-10-11", "Two property records on one date", notes="M. Bihuge is also the Haveeree Hingun house quoted for 1 Apr 2023")
ev("EVT0025", "2024-11-15", "2024-11-18", "window_bounds_approximate", "uncertain_date", "rain", "citywide", "'Major flooding was reported in ... Male' ... by NDMA' (MMS)", "unknown", "", "",
   "SRC0018", [("SRC0018", "supports", "2024-11-15", "2024-11-18", "Male' explicit, date not given", "uncertain_date")], "NEW_MMS_2024-11;GS_2024-11-18_2024-11-18",
   "MMS gives no date; the episode ended about 18 Nov. Bounds are approximate and must not be expanded into daily positives", notes="Found during this verification")
ev("EVT0026", "2024-12-17", "2024-12-17", "single_day", "mixed_or_uncertain_cause", "unresolved_response_only", "citywide", "MMS Fig. 48: 'dewatering was carried out at Male''", "unknown", "", "",
   "SRC0018", [("SRC0018", "supports", "2024-12-17", "2024-12-17", "dewatering at Male'", "uncertain"), ("SRC0021", "context_only", "2024-12-16", "2024-12-21", "'past five days' responses", "context")],
   "OFF005;GS_2024-12-17_2024-12-17", "Official evidence is a response (dewatering) only; flooding and its cause are not stated. Heavy rain is likely from the station record but not stated",
   SYN + "GSOD 18 Dec (24 h ending 05:00 local 18 Dec) = 54.9 mm")
ev("EVT0027", "2024-12-20", "2024-12-21", "overnight_window", "accepted_reported_rain_event", "rain", "street",
   "West Park, IGMH, Vilimale' Ferry Terminal, Dhiraagu, Jelly Pizza; 16 pumps; 32 people sheltered (MMS)", "Friday night", "began Friday night / since late last night",
   "MNDF overnight", "SRC0021;SRC0022",
   [("SRC0021", "supports", "2024-12-20", "2024-12-21", "Male' places", "accepted"), ("SRC0022", "supports", "2024-12-20", "2024-12-21", "Male' roads", "accepted"),
    ("SRC0049", "supports", "2024-12-20", "2024-12-21", "Male' places", "accepted"), ("SRC0018", "supports", "2024-12-20", "2024-12-20", "MMS 20 Dec episode", "accepted"),
    ("SRC0050", "context_only", "2024-12-20", "2024-12-21", "'last weekend'", "context"), ("SRC0051", "context_only", "", "", "repairs", "context")],
   "RAIN012;MFB_2024-12-20;LEGACY_REVIEW_2024-12-20;GS_2024-12-20_2024-12-21", "Night spans two calendar days; do not count either day alone as a confirmed daily positive",
   "Male' 136.5 mm 08:00 Fri 20-08:00 Sat 21 (MMS; report labels it 20 Dec); Hulhule 117.4 (MMS/Atoll Times) vs 'Hulhumale 117' (Sun). " + SYN + "05:00 20 Dec-05:00 21 Dec = 117 mm (12-h pairs) vs 24-h group 92.9",
   "Legacy 'uncertain' (original blocked) superseded: three accessible sources and MMS describe the overnight flooding", "uncertain")
ev("EVT0028", "2025-01-03", "2025-01-03", "single_day_with_persistence", "accepted_reported_rain_event", "rain", "street",
   "Most of the city; Majeedhee Magu, Ameenee Magu impassable; Kan'baa Aisa Rani Hingun; Izzuddeen Magu; Maafannu worst; pumps at West Park, IGMH, Salman Mosque, Maafannu Ferry Terminal, Kudakudhinge Bageecha, Voice of Maldives",
   "Friday", "Thursday evening (MVRepublic) / Friday morning (Ras) / Friday afternoon (avas): unresolved", "11:37 Friday (MNDF pumping start)", "SRC0053;SRC0054",
   [("SRC0023", "supports", "2025-01-03", "2025-01-03", "Male' roads", "accepted"), ("SRC0053", "supports", "2025-01-03", "2025-01-03", "Male' places", "accepted"),
    ("SRC0054", "supports", "2025-01-03", "2025-01-04", "flooded until early Saturday", "accepted"), ("SRC0055", "supports", "2025-01-03", "2025-01-03", "Male' explicit", "accepted"),
    ("SRC0056", "supports", "2025-01-03", "2025-01-03", "Male' explicit", "accepted"), ("SRC0052", "conflicts", "2025-01-04", "2025-01-04", "date wording 'January 4'", "date conflict noted")],
   "RAIN013;MFB_2025-01-03;LEGACY_REVIEW_2025-01-03;GS_2025-01-02_2025-01-07;GS_2025-01-03_2025-01-03",
   "Rain-start wording conflicts; flooding persisted until early 4 Jan (persistence, not a new flood day); mmtv's 'January 4' read as publication date",
   "Male' 142.2 (Atoll Times) / 142.6 (avas) on Friday; 162 mm by 23:00 Friday (MVRepublic); Hulhule 144 mm 08:00 Fri-08:00 Sat. " + SYN + "17:00 2 Jan-05:00 3 Jan 30 mm; 11:00-17:00 3 Jan 64.7 mm; 17:00-23:00 93 mm",
   legacy="include")
ev("EVT0029", "2025-01-10", "2025-01-11", "overnight_window", "accepted_reported_rain_event", "rain", "landmark",
   "Eight pump areas incl. West Park, IGMH, Boduvalhu; 46-58 households assisted", "Friday evening (Atoll Times) / early Saturday morning (Plus): unresolved",
   "early evening Friday, intensified by midnight (Standard)", "MNDF through the night", "SRC0024;SRC0057;SRC0058",
   [("SRC0024", "supports", "2025-01-10", "2025-01-11", "Male' explicit", "accepted"), ("SRC0057", "supports", "2025-01-10", "2025-01-11", "Male' places", "accepted"),
    ("SRC0058", "supports", "2025-01-11", "2025-01-11", "Male' explicit", "accepted")], "RAIN014;MFB_2025-01-11;LEGACY_REVIEW_2025-01-11;GS_2025-01-10_2025-01-11",
   "Flood-date window: 10 Jan evening flooding stated by one source; rain-timing descriptions differ. Intraday timing kept unresolved",
   "MMS via Plus: Male' 130.7 mm 08:00 Fri 10-08:00 Sat 11. " + SYN + "17:00-23:00 10 Jan 8 mm; 23:00-05:00 62 mm; 05:00-11:00 11 Jan 31 mm",
   "Legacy 'include' with 11 Jan only; 10 Jan evening now explicit in one source", "include")
ev("EVT0030", "2025-03-01", "2025-03-01", "single_day", "accepted_reported_rain_event", "rain", "landmark", "Several areas; pumps at 10 locations incl. IGMH, West Park, Maafannu ferry terminal",
   "after sunset", "shortly after sunset (about 2 h)", "pumps that night (time not given)", "SRC0059",
   [("SRC0059", "supports", "2025-03-01", "2025-03-01", "Male' streets", "accepted"), ("SRC0060", "supports", "2025-03-01", "2025-03-02", "Male' places", "accepted"),
    ("SRC0025", "supports", "2025-03-01", "2025-03-01", "Male' explicit", "accepted")], "RAIN015;MFB_2025-03-01;LEGACY_REVIEW_2025-03-01;GS_2025-02-28_2025-03-02",
   "", SYN + "17:00-23:00 1 Mar 71 mm; 23:00 1 Mar-05:00 2 Mar 88 mm", legacy="include")
ev("EVT0031", "2025-03-11", "2025-03-11", "single_day_with_persistence", "accepted_reported_rain_event", "rain", "landmark", "IGMH, West Park, Maafannu Ferry Terminal; 6 pumps",
   "Tuesday evening", "Tuesday afternoon/evening", "pumps from Tuesday afternoon (mmtv)", "SRC0026;SRC0061",
   [("SRC0026", "supports", "2025-03-11", "2025-03-11", "Male' explicit", "accepted"), ("SRC0061", "supports", "2025-03-11", "2025-03-12", "Male' places", "accepted")],
   "RAIN016;MFB_2025-03-11;LEGACY_REVIEW_2025-03-11", "Continuation into 12 Mar is persistence, not a new flood day",
   SYN + "11:00-17:00 11 Mar 15 mm; 17:00-23:00 34 mm; 23:00-05:00 4 mm",
   "Legacy 'uncertain' (date not explicit) superseded: ThePress reports the flooding on 11 Mar itself", "uncertain")
ev("EVT0032", "2025-04-27", "2025-04-27", "single_day", "accepted_reported_rain_event", "rain", "landmark", "Five most flood-prone areas of Male' (list not rendered)", "after sunset",
   "after sunset", "21:40 (MNDF dewatering start, 'tonight 9:40')", "SRC0027", [("SRC0027", "supports", "2025-04-27", "2025-04-27", "Male' explicit", "accepted")], "RAIN017", "Single source")
ev("EVT0033", "2025-11-25", "2025-11-25", "single_day", "accepted_reported_rain_event", "rain", "landmark", "Maafannu; near IGMH; near Ameeniyya School", "early morning Tuesday",
   "early morning Tuesday", "no pumps as of 07:00", "SRC0062", [("SRC0062", "supports", "2025-11-25", "2025-11-25", "Male' places", "accepted")],
   "MFB_2025-11-25;LEGACY_REVIEW_2025-11-25", "RAIN018 calls itself a correction of this date; not supported (see EVT0034)", legacy="include")
ev("EVT0034", "2025-11-26", "2025-11-26", "single_day_with_persistence", "accepted_reported_rain_event", "rain", "citywide", "Male' streets; seven pumps", "afternoon",
   "after 13:00", "pumps by 16:04", "SRC0028", [("SRC0028", "supports", "2025-11-26", "2025-11-26", "Male' streets", "accepted"),
    ("SRC0029", "supports", "2025-11-26", "2025-11-27", "remains flooded at 00:44", "accepted")], "RAIN018",
   "RAIN018 is not a correction of 25 Nov: Adhadhu (dated 25 Nov 2025, MVT) independently reports Tuesday-morning flooding. Both dates stand as separate reported days; both histories preserved")
ev("EVT0035", "2026-04-16", "2026-04-16", "single_day", "accepted_reported_rain_event", "rain", "landmark", "Two locations in Maafannu; roads of the capital", "unknown", "", "pumps (time not given)",
   "SRC0030", [("SRC0030", "supports", "2026-04-16", "2026-04-16", "Male' roads", "accepted"), ("SRC0063", "possible_duplicate", "2026-04-16", "2026-04-16", "alias of SRC0030", "duplicate")],
   "RAIN019;MFB_2026-04-16;LEGACY_REVIEW_2026-04-16", legacy="uncertain", notes="Legacy 'uncertain' (blocked source) superseded: article readable")
ev("EVT0036", "2026-05-04", "2026-05-04", "single_day", "accepted_reported_rain_event", "rain", "landmark", "IGMH area, Maafannu Ferry Terminal, Salman Mosque, Swimming Track", "Monday", "",
   "soldiers dewatering (time not given)", "SRC0064", [("SRC0064", "supports", "2026-05-04", "2026-05-04", "Male' places", "accepted")], "MFB_2026-05-04;LEGACY_REVIEW_2026-05-04",
   legacy="uncertain", notes="Legacy 'uncertain' (blocked source) superseded: article readable via Wayback")
ev("EVT0037", "2026-07-26", "2026-07-26", "single_day", "accepted_reported_coastal_event", "coastal_swell", "street",
   "Industrial Village, Raalhugandu, Carnival area, Boduthakurufaanu Magu (new section)", "around midday / early afternoon", "", "MNDF draining", "SRC0031",
   [("SRC0031", "supports", "2026-07-26", "2026-07-26", "Male' places", "accepted"), ("SRC0032", "supports", "2026-07-26", "2026-07-26", "Male' places", "accepted")], "COAST003",
   "", "Tide quoted: highest 0.74 m at 11:53 (datum not stated)")
ev("EVT0038", "2026-07-30", "2026-07-30", "single_day", "accepted_reported_rain_event", "rain", "street_section", "Boduthakurufaanu Magu, Henveiru Ferry Terminal to Izzuddin Jetty (new section)",
   "Thursday", "", "MNDF portable pumps", "SRC0065", [("SRC0065", "supports", "2026-07-30", "2026-07-30", "bounded road section", "accepted"),
    ("SRC0066", "supports", "2026-07-30", "2026-07-30", "road section", "accepted")], "MFB_2026-07-30;LEGACY_REVIEW_2026-07-30",
   "Cause: rain while the permanent drainage pump station was not yet commissioned", legacy="include")
ev("EVT0039", "2026-08-04", "2026-08-04", "single_day", "accepted_reported_rain_event", "rain", "citywide", "Male' roads", "unknown", "", "MNDF pumping by ~19:05", "SRC0033",
   [("SRC0033", "supports", "2026-08-04", "2026-08-04", "Male' roads", "accepted")], "RAIN020", "Single source")
ev("EVT0040", "2026-09-12", "2026-09-12", "single_day", "accepted_reported_rain_event", "rain", "citywide", "Male'; water entering some houses", "unknown", "", "MNDF sandbagging", "SRC0034",
   [("SRC0034", "supports", "2026-09-12", "2026-09-12", "Male' houses", "accepted")], "RAIN021", "Single source")
ev("EVT0041", "2026-10-21", "2026-10-21", "single_day_with_persistence", "accepted_reported_rain_event", "rain", "citywide", "Entire city; 89 buildings (35 shops, 33 houses, 4 schools)",
   "evening", "around sundown", "MNDF draining (time not given)", "SRC0035", [("SRC0035", "supports", "2026-10-21", "2026-10-21", "Male' explicit", "accepted"),
    ("SRC0067", "supports", "2026-10-21", "2026-10-22", "last night's rain", "accepted"), ("SRC0068", "context_only", "2026-10-24", "2026-10-24", "Hulhumale' cemetery, not Male' island", "context")],
   "RAIN022;MFB_2026-10-21;LEGACY_REVIEW_2026-10-21", "", "Male' 90 mm in last 24 h (Edition, 22 Oct)", legacy="include")
ev("EVT0042", "2019-06-15", "2019-06-15", "single_day", "accepted_reported_coastal_event", "coastal_swell", "street", "Alimas Carnival, Raalhugandu, Artificial Beach, Boduthakurufaanu Magu, Industrial Village",
   "Saturday morning", "", "", "SRC0071", [("SRC0071", "supports", "2019-06-15", "2019-06-15", "Male' places", "accepted")], "GS_2019-06-15_2019-06-16",
   "16 Jun (Groundsource) not supported", period="before_study_period")
ev("EVT0043", "2004-12-26", "2004-12-26", "single_day", "accepted_reported_coastal_event", "coastal_tsunami", "citywide", "Two-thirds of the capital city", "first hours of the day", "", "",
   "SRC0070", [("SRC0070", "supports", "2004-12-26", "2004-12-26", "capital", "accepted")], "GS_2004-12-26_2004-12-26", "Tsunami: separate mechanism", period="before_study_period")

STATUS = {"accepted_reported_rain_event": "accepted", "accepted_reported_coastal_event": "accepted", "excluded": "excluded"}
FE_COLS = ["event_id", "event_start_date", "event_end_date", "date_certainty", "male_island_confirmation", "location_as_reported", "flood_type", "storm_group_id",
           "flood_onset_time_local", "rain_start_time_local", "response_start_time_local", "event_times_timezone", "timing_evidence_source_id", "review_status",
           "reviewed_by", "reviewed_on", "notes",
           # documented extensions (00_catalog/schema_extensions_v002.csv)
           "decision", "evidence_scope", "independent_source_count", "supporting_source_ids", "conflicting_source_ids", "conflicts", "rainfall_statements",
           "original_record_ids", "legacy_decision", "study_period", "label_use_note", "record_version"]

# ------------------------------------------------------------ storm groups
G = []
def sg(gid, start, end, members, status, ftype, basis, srcs, notes=""):
    G.append(dict(storm_group_id=gid, period_start_date=start, period_end_date=end, member_event_ids=members, grouping_status=status, flood_type=ftype,
                  grouping_basis=basis, evidence_source_ids=srcs, notes=notes))
SINGLE = "single reported episode; no other report within 7 days; independence from unreported days unknowable"
sg("STORM0001", "2020-05-18", "2020-05-18", "EVT0001", "provisional", "mixed", SINGLE, "SRC0001")
sg("STORM0002", "2021-12-11", "2021-12-12", "EVT0002", "established", "rain", "one source describes flooding 'yesterday and today' from the same unusual rain", "SRC0002;SRC0036")
sg("STORM0003", "2022-07-17", "2022-07-17", "EVT0003", "provisional", "rain", SINGLE, "SRC0003;SRC0038")
sg("STORM0004", "2022-11-05", "2022-11-05", "EVT0004", "provisional", "coastal", SINGLE, "SRC0004;SRC0005")
sg("STORM0005", "2023-04-01", "2023-04-01", "EVT0005", "provisional", "rain", SINGLE, "SRC0006;SRC0039")
sg("STORM0006", "2023-05-04", "2023-05-04", "EVT0006", "provisional", "rain", SINGLE, "SRC0007")
sg("STORM0007", "2023-07-21", "2023-07-21", "EVT0007", "provisional", "rain", SINGLE, "SRC0008;SRC0040")
sg("STORM0008", "2023-07-31", "2023-07-31", "EVT0008", "unresolved", "coastal", "5 days before STORM0009; relation to the August swell/king-tide period not established", "SRC0011")
sg("STORM0009", "2023-08-05", "2023-08-06", "EVT0009;EVT0010", "established", "coastal", "same swell episode: surges 'expected for hours' (Atoll Times); swells to continue 24 h (Sun)", "SRC0009;SRC0010")
sg("STORM0010", "2023-10-01", "2023-10-01", "EVT0011", "provisional", "rain", SINGLE, "SRC0011")
sg("STORM0011", "2023-12-30", "2023-12-31", "EVT0012;EVT0013", "established", "rain", "'continuous downpour since Saturday morning' through Sunday (Atoll Times); low-pressure area (Sun)", "SRC0041;SRC0042")
sg("STORM0012", "2024-01-10", "2024-01-13", "EVT0014;EVT0015;EVT0016", "provisional", "rain",
   "both 10 Jan and 12 Jan reports cite the same warned system (cyclonic circulation crossing the Maldives, warned on Tuesday 9 Jan); Hulhule SYNOP shows two bursts separated by ~30 h with <=2 mm. Same synoptic system; separate flood episodes",
   "SRC0013;SRC0044;SRC0018")
sg("STORM0013", "2024-02-16", "2024-02-16", "EVT0017", "provisional", "rain", SINGLE, "SRC0018")
sg("STORM0014", "2024-04-13", "2024-04-13", "EVT0018", "provisional", "rain", SINGLE, "SRC0016;SRC0017")
sg("STORM0015", "2024-05-08", "2024-05-08", "EVT0019", "provisional", "rain", "MMS: circulations from 5-6 May; single Male' report", "SRC0018")
sg("STORM0016", "2024-05-25", "2024-05-25", "EVT0020", "provisional", "rain", "MMS: Bay of Bengal system (later Cyclone Remal); single Male' report", "SRC0018")
sg("STORM0017", "2024-08-13", "2024-08-14", "EVT0021;EVT0022", "provisional", "rain", "MMS: convection enhanced 11-17 Aug; 14 Aug only a caption date", "SRC0018;SRC0019")
sg("STORM0018", "2024-09-18", "2024-09-18", "EVT0023", "provisional", "rain", SINGLE + "; property-level record", "SRC0020")
sg("STORM0019", "2024-10-11", "2024-10-11", "EVT0024", "provisional", "rain", "MMS: severe-weather episode 4-14 Oct; Male' records on 11 Oct only", "SRC0020;SRC0018")
sg("STORM0020", "2024-11-15", "2024-11-18", "EVT0025", "unresolved", "rain", "date of Male' flooding within the mid-November episode unknown", "SRC0018")
sg("STORM0021", "2024-12-17", "2024-12-17", "EVT0026", "unresolved", "unresolved", "MMS describes back-to-back circulations (16 Dec and 20 Dec); relation to STORM0022 not established", "SRC0018;SRC0021")
sg("STORM0022", "2024-12-20", "2024-12-21", "EVT0027", "established", "rain", "single overnight episode in all sources", "SRC0021;SRC0022;SRC0049")
sg("STORM0023", "2025-01-03", "2025-01-03", "EVT0028", "established", "rain", "one episode from Thursday evening to early Saturday; MNDF pumping 11:37 Fri to 08:30 Sat", "SRC0053;SRC0054;SRC0055")
sg("STORM0024", "2025-01-10", "2025-01-11", "EVT0029", "established", "rain", "single overnight episode; Atoll Times calls it the 'second instance ... within a week' (separate from STORM0023)", "SRC0024;SRC0057")
sg("STORM0025", "2025-03-01", "2025-03-01", "EVT0030", "provisional", "rain", SINGLE, "SRC0059")
sg("STORM0026", "2025-03-11", "2025-03-11", "EVT0031", "provisional", "rain", SINGLE, "SRC0026;SRC0061")
sg("STORM0027", "2025-04-27", "2025-04-27", "EVT0032", "provisional", "rain", SINGLE, "SRC0027")
sg("STORM0028", "2025-11-25", "2025-11-26", "EVT0033;EVT0034", "provisional", "rain",
   "consecutive-day reports within one multi-day alert period (Met forecast of heavy rain over the next three days on 26 Nov); not stated to be one storm", "SRC0062;SRC0028;SRC0029")
sg("STORM0029", "2026-04-16", "2026-04-16", "EVT0035", "provisional", "rain", SINGLE, "SRC0030")
sg("STORM0030", "2026-05-04", "2026-05-04", "EVT0036", "provisional", "rain", SINGLE, "SRC0064")
sg("STORM0031", "2026-07-26", "2026-07-26", "EVT0037", "provisional", "coastal", "swell episode without severe weather; different mechanism from STORM0032", "SRC0031;SRC0032")
sg("STORM0032", "2026-07-30", "2026-07-30", "EVT0038", "provisional", "rain", "single report; drainage pumps not commissioned", "SRC0065")
sg("STORM0033", "2026-08-04", "2026-08-04", "EVT0039", "provisional", "rain", "southwest-monsoon spell ('past two weeks' of bad weather); relation to late-July events not established", "SRC0033")
sg("STORM0034", "2026-09-12", "2026-09-12", "EVT0040", "provisional", "rain", SINGLE, "SRC0034")
sg("STORM0035", "2026-10-21", "2026-10-21", "EVT0041", "established", "rain", "single overnight episode ('last night's non-stop rainfall')", "SRC0035;SRC0067")
sg("STORM0036", "2019-06-15", "2019-06-15", "EVT0042", "provisional", "coastal", "single swell weekend; before study period", "SRC0071")
sg("STORM0037", "2004-12-26", "2004-12-26", "EVT0043", "established", "coastal_tsunami", "2004 Indian Ocean tsunami", "SRC0070")
gid_of = {m: g["storm_group_id"] for g in G for m in g["member_event_ids"].split(";")}

# proposed conservative validation blocks: same target, windows <= 7 days apart (a counting device, not storm identity)
def d(s): return date.fromisoformat(s)
blocks = []
for tgt in ("rain", "coastal"):
    # mixed/unresolved groups are not rain labels, but they sit among rain dates, so they block with the rain target
    gs = sorted([g for g in G if (g["flood_type"] in ("rain", "mixed", "unresolved")) == (tgt == "rain") and g["flood_type"] != "coastal_tsunami"
                 and d(g["period_start_date"]) >= date(2020, 1, 1)], key=lambda g: g["period_start_date"])
    cur = None
    for g in gs:
        if cur and d(g["period_start_date"]) - d(cur["end"]) <= timedelta(days=7):
            cur["groups"].append(g["storm_group_id"]); cur["end"] = max(cur["end"], g["period_end_date"])
        else:
            cur = dict(target=tgt, start=g["period_start_date"], end=g["period_end_date"], groups=[g["storm_group_id"]]); blocks.append(cur)
for i, b in enumerate(blocks, 1):
    b["validation_block_id"] = f"VB{i:03d}"
    for gid in b["groups"]:
        next(g for g in G if g["storm_group_id"] == gid)["validation_block_id"] = b["validation_block_id"]

# ------------------------------------------------------------ write events
fe, links = [], []
for e in E:
    sup = [l[0] for l in e["links"] if l[1] == "supports"]
    canon = {S[s]["canonical_source_id"] for s in sup}
    conf = [l[0] for l in e["links"] if l[1] == "conflicts"]
    use = {"accepted_reported_rain_event": "reported rain-flood occurrence; not measured extent/depth; positive-only",
           "accepted_reported_coastal_event": "coastal target only; exclude from rain target",
           }.get(e["decision"], "not a label; keep visible as uncertain")
    if e["date_certainty"] == "overnight_window":
        use += "; window - do not convert either day into a daily positive"
    fe.append(dict(event_id=e["event_id"], event_start_date=e["event_start_date"], event_end_date=e["event_end_date"], date_certainty=e["date_certainty"],
                   male_island_confirmation={"uncertain_location": "not_established"}.get(e["decision"], "explicit_in_source"),
                   location_as_reported=e["location_as_reported"], flood_type=e["flood_type"], storm_group_id=gid_of[e["event_id"]],
                   flood_onset_time_local=e["flood_onset_time_local"], rain_start_time_local=e["rain_start_time_local"],
                   response_start_time_local=e["response_start_time_local"], event_times_timezone="Asia/Male (UTC+5) as stated or implied in source text; not measured",
                   timing_evidence_source_id=e["timing_evidence_source_id"], review_status=STATUS.get(e["decision"], "uncertain"),
                   reviewed_by=REVIEWER, reviewed_on=REVIEWED_ON, notes=e["notes"], decision=e["decision"], evidence_scope=e["evidence_scope"],
                   independent_source_count=len(canon), supporting_source_ids=";".join(sup), conflicting_source_ids=";".join(conf), conflicts=e["conflicts"],
                   rainfall_statements=e["rainfall_statements"], original_record_ids=e["original_record_ids"], legacy_decision=e["legacy_decision"],
                   study_period=e["study_period"], label_use_note=use, record_version="v002"))
    for sid, rel, cs, ce, scope, dec in e["links"]:
        links.append(dict(event_id=e["event_id"], source_id=sid, source_relationship=rel, claimed_flood_start_date=cs, claimed_flood_end_date=ce,
                          scope_assessment=scope, review_decision=dec, decision_reason=S[sid]["excerpt_english"] if S[sid]["excerpt_language"] == "dv" else S[sid]["excerpt_original"],
                          canonical_source_id=S[sid]["canonical_source_id"], source_checked_at_utc=fetch.get(sid, {}).get("fetched_at_utc", ""), record_version="v002"))
w("03_reviewed/events/flood_events.csv", fe, FE_COLS)
w("03_reviewed/events/event_source_links.csv", links, ["event_id", "source_id", "source_relationship", "claimed_flood_start_date", "claimed_flood_end_date",
  "scope_assessment", "review_decision", "decision_reason", "canonical_source_id", "source_checked_at_utc", "record_version"])

legacy_groups = list(csv.DictReader(open(ROOT / "03_reviewed/_archive_v001_20261122/storm_groups.csv", encoding="utf-8-sig")))
SG_COLS = ["storm_group_id", "period_start_date", "period_end_date", "grouping_basis", "evidence_source_ids", "review_status", "notes",
           "member_event_ids", "grouping_status", "flood_type", "validation_block_id", "superseded_by", "record_version"]
lg_map = {"LEGACY_S01": "STORM0002", "LEGACY_S02": "STORM0003", "LEGACY_S03": "STORM0005", "LEGACY_S04": "STORM0007", "LEGACY_S05": "STORM0011", "LEGACY_S06": "STORM0012",
          "LEGACY_S07": "STORM0017", "LEGACY_S08": "STORM0022", "LEGACY_S09": "STORM0023", "LEGACY_S10": "STORM0024", "LEGACY_S11": "STORM0025", "LEGACY_S12": "STORM0026",
          "LEGACY_S13": "STORM0028", "LEGACY_S14": "STORM0029", "LEGACY_S15": "STORM0030", "LEGACY_S16": "STORM0032", "LEGACY_S17": "STORM0035"}
sg_rows = [dict(r, superseded_by=lg_map[r["storm_group_id"]], record_version="v001 (preserved)") for r in legacy_groups]
sg_rows += [dict(g, review_status=g["grouping_status"], record_version="v002") for g in G]
w("03_reviewed/storm_groups/storm_groups.csv", sg_rows, SG_COLS)
w("03_reviewed/storm_groups/validation_blocks_proposed_v002.csv",
  [dict(validation_block_id=b["validation_block_id"], target=b["target"], block_start_date=b["start"], block_end_date=b["end"], storm_group_ids=";".join(b["groups"]),
        rule="merge storm groups of the same target whose windows are <= 7 days apart", status="proposal for evaluation only; not a storm identity") for b in blocks],
  ["validation_block_id", "target", "block_start_date", "block_end_date", "storm_group_ids", "rule", "status"])

# ------------------------------------------------------------ crosswalk
ev_of = {}
for e in E:
    for o in e["original_record_ids"].split(";"):
        ev_of.setdefault(o, []).append(e["event_id"])
dec_of = {e["event_id"]: e["decision"] for e in E}
cw = []
imp = list(csv.DictReader(open(ROOT / "02_interim/event_candidates/male_flood_inventory.csv", encoding="utf-8-sig")))
for r in imp:
    rid = r["record_id"]; evs = ev_of[rid]
    cw.append(dict(original_dataset="male_flood_inventory.csv (import, 30)", original_record_id=rid, original_start=r["event_start_date"], original_end=r["event_end_date"],
                   original_status=r["review_status"], event_ids=";".join(evs), decisions=";".join(dec_of[x] for x in evs)))
comp = list(csv.DictReader(open(ROOT / "01_raw/flood_evidence/compiled_secondary/male_flood_basis/flood_incidents_greater_male_2021-2026.csv", encoding="utf-8-sig")))
for r in comp:
    rid = "MFB_" + r["incident_id"]; evs = ev_of[rid]
    cw.append(dict(original_dataset="flood_incidents_greater_male_2021-2026.csv (compiled, 18)", original_record_id=rid, original_start=r["incident_id"], original_end=r["dates"],
                   original_status="compiled incident", event_ids=";".join(evs), decisions=";".join(dec_of[x] for x in evs)))
for r in csv.DictReader(open(ROOT / "03_reviewed/events/legacy_daily_exploration/event_review.csv", encoding="utf-8-sig")):
    rid = "LEGACY_REVIEW_" + r["incident_id"]; evs = ev_of[rid]
    cw.append(dict(original_dataset="legacy event_review.csv (18)", original_record_id=rid, original_start=r["positive_date"] or r["uncertain_dates"], original_end=r["uncertain_dates"],
                   original_status=r["decision"], event_ids=";".join(evs), decisions=";".join(dec_of[x] for x in evs)))
for r in csv.DictReader(open(ROOT / "02_interim/event_candidates/starter_pack_flood/event_candidates.csv", encoding="utf-8-sig")):
    rid = "SP_" + r["event_or_record_date"]; evs = ev_of[rid]
    cw.append(dict(original_dataset="starter-pack event_candidates.csv (3)", original_record_id=rid, original_start=r["event_or_record_date"], original_end=r["event_or_record_date"],
                   original_status=r["record_type"], event_ids=";".join(evs), decisions=";".join(dec_of[x] for x in evs)))
for r in csv.DictReader(open(ROOT / "02_interim/groundsource_candidates/inventory_comparison.csv", encoding="utf-8-sig")):
    rid = f"GS_{r['groundsource_start']}_{r['groundsource_latest_end']}"; evs = ev_of.get(rid, [])
    cw.append(dict(original_dataset="Groundsource inventory_comparison.csv (29 windows)", original_record_id=rid, original_start=r["groundsource_start"],
                   original_end=r["groundsource_latest_end"], original_status=r["existing_inventory_comparison"], event_ids=";".join(evs),
                   decisions=";".join(dec_of[x] for x in evs) if evs else "excluded",
                   note="" if evs else "Groundsource intersection only; no article or record located in this pass. Not evidence that no flood occurred"))
for r in legacy_groups:
    cw.append(dict(original_dataset="storm_groups.csv v001 (legacy proxies, 17)", original_record_id=r["storm_group_id"], original_start=r["period_start_date"],
                   original_end=r["period_end_date"], original_status=r["review_status"], event_ids="", decisions=f"superseded_by {lg_map[r['storm_group_id']]}"))
for rid in sorted(k for k in ev_of if k.startswith("NEW_")):
    evs = ev_of[rid]
    cw.append(dict(original_dataset="found during v002 verification", original_record_id=rid, original_start=next(e for e in E if e["event_id"] == evs[0])["event_start_date"],
                   original_end="", original_status="new official mention", event_ids=";".join(evs), decisions=";".join(dec_of[x] for x in evs)))
for c in cw:
    c.setdefault("note", ""); c["record_version"] = "v002"
w("03_reviewed/events/record_crosswalk.csv", cw, ["original_dataset", "original_record_id", "original_start", "original_end", "original_status", "event_ids", "decisions", "note", "record_version"])
assert all(c["event_ids"] or c["decisions"].startswith(("excluded", "superseded")) for c in cw)
assert len([c for c in cw if c["original_dataset"].startswith("male_flood_inventory")]) == 30

# ------------------------------------------------------------ counts
def days(e):
    a, b = d(e["event_start_date"]), d(e["event_end_date"])
    return [(a + timedelta(i)).isoformat() for i in range((b - a).days + 1)]
inp = [e for e in E if e["study_period"] == "in_study_period"]
cnt = []
def c(k, v, note=""): cnt.append(dict(measure=k, value=v, note=note))
for ds in ("male_flood_inventory.csv (import, 30)", "flood_incidents_greater_male_2021-2026.csv (compiled, 18)", "legacy event_review.csv (18)",
           "starter-pack event_candidates.csv (3)", "Groundsource inventory_comparison.csv (29 windows)", "storm_groups.csv v001 (legacy proxies, 17)", "found during v002 verification"):
    c(f"original records: {ds}", sum(x["original_dataset"] == ds for x in cw))
c("sources registered", len(S)); c("sources checked with body accessible", sum(not S[s]["body_accessible"].startswith("no") for s in S))
c("unique sources after URL de-duplication", len({S[s]["canonical_source_id"] for s in S}), "SRC0046->SRC0019; SRC0063->SRC0030")
c("reviewed events (all)", len(E)); c("reviewed events in study period (2020+)", len(inp))
for k, v in sorted(Counter(e["decision"] for e in inp).items()):
    c(f"events in study period: {k}", v)
rain_acc = [e for e in inp if e["decision"] == "accepted_reported_rain_event"]
single = [e for e in rain_acc if e["date_certainty"] != "overnight_window" and e["date_certainty"] != "both_days_reported"]
c("source-verified reported rain-flood dates (single primary day)", len(single))
c("source-verified rain-flood events with both days explicitly reported", sum(e["date_certainty"] == "both_days_reported" for e in rain_acc), "EVT0002: 11 and 12 Dec 2021")
c("source-verified rain-flood overnight windows (2 days, day unresolved)", sum(e["date_certainty"] == "overnight_window" for e in rain_acc))
c("distinct calendar days with an accepted single-day rain report", len({x for e in single for x in days(e)} | {x for e in rain_acc if e["date_certainty"] == "both_days_reported" for x in days(e)}))
c("accepted rain events, property-level only", sum(e["evidence_scope"] == "property" for e in rain_acc))
c("accepted rain events resting on a single source", sum(len({S[l[0]]['canonical_source_id'] for l in e['links'] if l[1] == 'supports'}) == 1 for e in rain_acc))
c("source-verified coastal dates (study period)", sum(e["decision"] == "accepted_reported_coastal_event" for e in inp))
c("uncertain date windows (uncertain_date)", sum(e["decision"] == "uncertain_date" for e in inp))
c("persistence into the next day noted (not counted as new days)", sum(e["date_certainty"] == "single_day_with_persistence" for e in inp))
for k, v in sorted(Counter(e["flood_type"] for e in inp).items()):
    c(f"classification (study period): {k}", v)
for k, v in sorted(Counter((g["flood_type"], g["grouping_status"]) for g in G if d(g["period_start_date"]) >= date(2020, 1, 1)).items()):
    c(f"storm groups (study period): {k[0]} / {k[1]}", v)
c("proposed validation blocks: rain", sum(b["target"] == "rain" for b in blocks)); c("proposed validation blocks: coastal", sum(b["target"] == "coastal" for b in blocks))
for x in cnt: x["record_version"] = "v002"
w("03_reviewed/events/review_counts_v002.csv", cnt, ["measure", "value", "note", "record_version"])
for x in cnt: print(f"  {x['measure']}: {x['value']}")
