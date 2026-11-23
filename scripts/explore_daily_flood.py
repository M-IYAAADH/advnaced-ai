"""Rebuild a conservative daily reported-flood experiment; see reports/daily_exploration.md."""
from pathlib import Path
import json, pickle
import numpy as np
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import average_precision_score, confusion_matrix, precision_score, recall_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'derived/daily_exploration'
DATA = ROOT / 'male-flood-basis/data'
OUT.mkdir(exist_ok=True, parents=True)
review = pd.read_csv(OUT / 'event_review.csv').fillna('')
raw = pd.read_csv(DATA / 'flood_incidents_greater_male_2021-2026.csv')
assert len(review) == len(raw) and set(review.incident_id) == set(raw.incident_id)
assert review.loc[review.decision.eq('include'), 'positive_date'].ne('').all()
positive = dict(zip(review.loc[review.decision.eq('include'), 'positive_date'], review.loc[review.decision.eq('include'), 'incident_id']))
uncertain = {x for s in review.uncertain_dates for x in s.split(';') if x}
assert not set(positive).intersection(uncertain)

daily = pd.read_csv(DATA / 'male_reanalysis_daily_2020-2026.csv', parse_dates=['date']).set_index('date').asfreq('D')
hour = pd.read_csv(DATA / 'male_reanalysis_hourly_2020-2026.csv', parse_dates=['time_local']).set_index('time_local')
sea = pd.read_csv(DATA / 'male_sea_level_waves_hourly_2022-2026.csv', parse_dates=['time_local']).set_index('time_local')
station = pd.read_csv(DATA / 'hulhule_station_daily_2020-2025.csv', parse_dates=['date']).set_index('date')
f = pd.DataFrame(index=daily.index)
f['rain_mm'] = daily.precipitation_sum_mm
f['wet_hours'] = daily.precipitation_hours_h
f['max_hour_mm'] = hour.precipitation_mm.resample('D').max().reindex(f.index)
f['rain_prev1_mm'] = f.rain_mm.shift(1)
f['rain_prev3_mm'] = f.rain_mm.shift(1).rolling(3, min_periods=3).sum()
f['rain_prev7_mm'] = f.rain_mm.shift(1).rolling(7, min_periods=7).sum()
f['sea_msl_max_m'] = sea.sea_level_height_msl_m.resample('D').max().reindex(f.index)
f['station_rain_mm'] = station.precip_mm.reindex(f.index)
f['season_sin'] = np.sin(2*np.pi*f.index.dayofyear/365.25)
f['season_cos'] = np.cos(2*np.pi*f.index.dayofyear/365.25)
f['label'] = f.index.strftime('%Y-%m-%d').map(lambda d: 1 if d in positive else (np.nan if d in uncertain else 0))
f['event_id'] = f.index.strftime('%Y-%m-%d').map(positive).fillna('')
f.index.name = 'date'
f.to_csv(OUT / 'daily_features.csv')
assert f.loc['2024-04-17','station_rain_mm'] != f.loc['2024-04-17','station_rain_mm']
assert f.loc['2025-01-03','rain_prev1_mm'] == f.loc['2025-01-02','rain_mm']

# Common dates across all candidate sources for fair comparisons. Station ends 2025-08-24.
sets = {'season':['season_sin','season_cos'], 'rain':['rain_mm','max_hour_mm'], 'antecedent':['rain_mm','max_hour_mm','rain_prev3_mm'], 'sea':['rain_mm','max_hour_mm','sea_msl_max_m'], 'station':['station_rain_mm']}
allcols = sorted(set(sum(sets.values(), [])))
rows=[]; scores=[]; coeff=[]
for exp, shift in [('retrospective',0),('next_day',1)]:
    X=f[allcols].shift(shift)
    eligible = f.label.notna() & X.notna().all(axis=1) & (f.index >= '2023-01-01')
    # Common complete-case sample ensures source comparisons use identical dates.
    for start,end in [('2024-01-01','2024-12-31'),('2025-01-01','2025-08-24')]:
        begin=pd.Timestamp(start); stop=pd.Timestamp(end)
        train=eligible & (f.index < begin-pd.Timedelta(days=8))
        test=eligible & (f.index>=begin) & (f.index<=stop)
        y=f.label.astype(float)
        if y[train].sum()<2 or y[test].sum()<1: continue
        assert not set(f.loc[train,'event_id'].replace('',np.nan).dropna()) & set(f.loc[test,'event_id'].replace('',np.nan).dropna())
        candidates=[('prevalence','season'),('threshold','rain'),('logistic','season'),('logistic','rain'),('logistic','antecedent'),('logistic','sea'),('logistic','station'),('tree','rain')]
        for model,feature in candidates:
            if exp == 'next_day' and feature == 'station':
                continue  # GSOD reporting/availability time is not established.
            cols=sets[feature]; a=X.loc[train,cols]; b=X.loc[test,cols]; yt=y[train].astype(int); yv=y[test].astype(int)
            if model=='prevalence': p=np.repeat(yt.mean(),len(b)); threshold=.5
            elif model=='threshold':
                # Training-only F1 optimization, selected among training rain quantiles.
                rain=a.rain_mm; best=(-1,None)
                for t in np.unique(rain.quantile(np.linspace(.5,.99,30))):
                    pred=rain>=t; tp=((pred)&(yt==1)).sum(); fp=((pred)&(yt==0)).sum(); fn=((~pred)&(yt==1)).sum(); val=2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0
                    if val>best[0]: best=(val,t)
                threshold=best[1]; p=(b.rain_mm>=threshold).astype(float).values
            else:
                estimator=LogisticRegression(C=0.1, class_weight='balanced',max_iter=2000,random_state=42) if model=='logistic' else HistGradientBoostingClassifier(max_iter=50,max_leaf_nodes=3,min_samples_leaf=30,l2_regularization=10,random_state=42)
                pipe=make_pipeline(SimpleImputer(strategy='median'),StandardScaler(),estimator); pipe.fit(a,yt); p=pipe.predict_proba(b)[:,1]; threshold=.5
                with open(OUT / f'{exp}_{start}_{model}_{feature}.pkl','wb') as fh: pickle.dump(pipe,fh)
                if model=='logistic':
                    for name,val in zip(cols,pipe[-1].coef_[0]): coeff.append(dict(experiment=exp,fold=start,feature_set=feature,feature=name,standardized_coefficient=val))
            pred=(p>=.5).astype(int); cm=confusion_matrix(yv,pred,labels=[0,1]).ravel()
            rows.append(dict(experiment=exp,fold=start,train_end=str((begin-pd.Timedelta(days=9)).date()),test_end=end,model=model,feature_set=feature,train_days=len(yt),train_events=int(yt.sum()),test_days=len(yv),test_events=int(yv.sum()),prevalence=float(yv.mean()),average_precision=float(average_precision_score(yv,p)),precision=float(precision_score(yv,pred,zero_division=0)),recall=float(recall_score(yv,pred,zero_division=0)),tn=int(cm[0]),fp=int(cm[1]),fn=int(cm[2]),tp=int(cm[3]),training_rain_threshold_mm=float(threshold) if model=='threshold' else None))
            scores.extend(dict(date=str(d.date()),experiment=exp,fold=start,model=model,feature_set=feature,label=int(v),score=float(s),event_id=f.loc[d,'event_id']) for d,v,s in zip(b.index,yv,p))
pd.DataFrame(rows).to_csv(OUT/'metrics.csv',index=False)
pd.DataFrame(scores).to_csv(OUT/'out_of_sample_scores.csv',index=False)
pd.DataFrame(coeff).to_csv(OUT/'coefficients.csv',index=False)
meta={'seed':42,'included_events':len(positive),'uncertain_incidents':int((review.decision=='uncertain').sum()),'uncertain_days':len(uncertain),'common_sample':'Complete cases for every compared input; 2023 onward; station ends 2025-08-24','folds':len(set((r['experiment'],r['fold']) for r in rows)),'evaluation':'Agreement with reported labels; unknown reports are not confirmed negative','versions':{}}
import sklearn
meta['versions']={'pandas':pd.__version__,'numpy':np.__version__,'scikit-learn':sklearn.__version__,'matplotlib':matplotlib.__version__}
(OUT/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
fig,ax=plt.subplots(figsize=(9,3)); ax.plot(f.index,f.rain_mm,linewidth=.45,color='#305c86'); ax.scatter(pd.to_datetime(list(positive)),f.loc[pd.to_datetime(list(positive)),'rain_mm'],color='#bb4d36',s=22,zorder=5,label='Verified reported day'); ax.set(ylabel='Reanalysis precipitation (mm/day)',xlabel='Date',title='Rainfall and verified reported flood days'); ax.legend(); fig.tight_layout(); fig.savefig(OUT/'rainfall_events.png',dpi=200); plt.close(fig)
print(json.dumps(meta,indent=2)); print(pd.DataFrame(rows).to_string(index=False))
