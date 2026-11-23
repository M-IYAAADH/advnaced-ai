"""Read-only batched screening of Groundsource; pip install pyarrow shapely pandas."""
from pathlib import Path
import json, hashlib
import numpy as np
import pandas as pd
import pyarrow.parquet as pq
import shapely
from shapely.geometry import shape,box,mapping
R=Path(__file__).resolve().parents[2]; P=R/'groundsource_2026.parquet'; O=Path(__file__).parent
pf=pq.ParquetFile(P); boundary=shape(json.loads((R/'Male_Flood_Data_Starter_Pack/boundary/OneMap_Male_Island.geojson').read_text())['features'][0]['geometry'])
# Deliberately broad Maldives bounding box; candidate, not verified national boundary.
region=box(72.3,-1,74.1,7.5); metro=box(73.43,4.08,73.62,4.30)
nulls={name:0 for name in pf.schema_arrow.names}; mins=[]; maxs=[]; out=[]; total=0
for batch in pf.iter_batches(batch_size=16000):
 total+=batch.num_rows
 for c in batch.schema.names: nulls[c]+=batch.column(c).null_count
 dates=batch.column('start_date').to_pylist(); ends=batch.column('end_date').to_pylist(); mins.extend([min((x for x in dates if x),default='9999')]); maxs.extend([max((x for x in ends if x),default='')])
 g=shapely.from_wkb(batch.column('geometry').to_numpy(zero_copy_only=False),on_invalid='ignore'); ix=np.flatnonzero(shapely.intersects(g,region))
 if len(ix):
  d=batch.to_pydict()
  for i in ix:
   geom=g[i]; b=geom.bounds; cent=geom.centroid
   out.append({'uuid':d['uuid'][i],'source_index':d['__index_level_0__'][i],'start_date':d['start_date'][i],'end_date':d['end_date'][i],'area_km2':d['area_km2'][i],'geometry_type':geom.geom_type,'min_lon':b[0],'min_lat':b[1],'max_lon':b[2],'max_lat':b[3],'centroid_lon':cent.x,'centroid_lat':cent.y,'intersects_male_island':bool(geom.intersects(boundary)),'intersects_greater_male_box':bool(geom.intersects(metro)),'geometry_wkt':geom.wkt})
print('scanned',total,'regional candidates',len(out),'nulls',nulls,'date',min(mins),max(maxs)); f=pd.DataFrame(out); f.sort_values(['start_date','uuid']).to_csv(O/'maldives_spatial_candidates.csv',index=False); f.drop(columns='geometry_wkt').to_csv(O/'candidate_summary.csv',index=False)
(O/'overview.json').write_text(json.dumps({'size_bytes':P.stat().st_size,'row_count':total,'schema':str(pf.schema_arrow.remove_metadata()),'row_groups':pf.num_row_groups,'null_counts':nulls,'min_start_date':min(mins),'max_end_date':max(maxs),'screening_box':[72.3,-1,74.1,7.5],'regional_candidates':len(f),'male_boundary_intersections':int(f.intersects_male_island.sum()),'greater_male_box_intersections':int(f.intersects_greater_male_box.sum())},indent=2))
print(f.drop(columns='geometry_wkt').to_string(index=False))
