"""Build a standalone, offline research dashboard from the audited derived files."""
from pathlib import Path
import json
import pandas as pd
R=Path(__file__).resolve().parents[1]; O=R/'derived/extended_analysis'; inv=pd.read_csv(R/'derived/road_flood_inventory.csv').fillna(''); checks=pd.read_csv(R/'verification/landmark_checks.csv').fillna(''); checks=checks[(checks.check_status=='verified') & checks.verified_evidence.isin(['flooding_stated_with_dewatering','flooding_stated','flooding_stated_waterlogged','photo_caption_flooding','dewatering_at_worst_flooded_area'])]; loc=checks.merge(inv,on='record_id'); loc=loc[(loc.in_study_area=='yes') & (loc.latitude!='')];
for col in ['latitude','longitude']: loc[col]=pd.to_numeric(loc[col])
# Approximate landmark coordinates are explicitly not flooded road coordinates.
data={'boundary':json.loads((R/'Male_Flood_Data_Starter_Pack/boundary/OneMap_Male_Island.geojson').read_text()),'locations':loc[['record_id','place','event','latitude','longitude','source_checked','note']].to_dict('records'),'daily':pd.read_csv(O/'daily_data.csv').fillna('').to_dict('records'),'metrics':pd.read_csv(O/'metrics.csv').fillna('').query("alignment == 'nominal'").to_dict('records'),'scores':pd.read_csv(O/'scores.csv').fillna('').to_dict('records')}
template=(R/'scripts/dashboard_template.html').read_text(); (O/'dashboard.html').write_text(template.replace('__DATA__',json.dumps(data,ensure_ascii=False).replace('</','<\\/')))
print('Dashboard:',O/'dashboard.html','locations:',len(loc))
