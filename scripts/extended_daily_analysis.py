"""Independent extension; preserves the preliminary outputs. See reports/extended_analysis.md."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, precision_score, recall_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1]; D=R/'male-flood-basis/data'; O=R/'derived/extended_analysis'; O.mkdir(parents=True,exist_ok=True)
review=pd.read_csv(R/'derived/daily_exploration/event_review.csv').fillna('')
h=pd.read_csv(D/'male_reanalysis_hourly_2020-2026.csv',parse_dates=['time_local']).set_index('time_local')
s=pd.read_csv(D/'male_sea_level_waves_hourly_2022-2026.csv',parse_dates=['time_local']).set_index('time_local')
idx=pd.date_range('2020-01-01','2026-11-13',freq='D')
# Group all reviewed incident dates, including uncertain ones, at most two calendar days apart.
events=review.copy(); events['anchor']=pd.to_datetime(events.incident_id); events=events.sort_values('anchor'); events['storm']=('S'+(events.anchor.diff().dt.days.fillna(999).gt(2).cumsum()).astype(str).str.zfill(2))
events.to_csv(O/'incident_storm_groups.csv',index=False)
basepos=events[events.decision.eq('include')]; uncertain={pd.Timestamp(x) for v in events.uncertain_dates for x in v.split(';') if x}
rows=[]; scores=[]; folds=[]
for alignment in ['nominal','rain_minus_1h','rain_plus_1h','label_minus_1d','label_plus_1d']:
    hourshift={'rain_minus_1h':-1,'rain_plus_1h':1}.get(alignment,0)
    hh=h.precipitation_mm.copy(); hh.index=hh.index+pd.Timedelta(hours=hourshift)
    rain=hh.resample('D').agg(['sum','max','count']).reindex(idx); rain.loc[rain['count']!=24,['sum','max']]=np.nan
    sea=s.sea_level_height_msl_m.resample('D').agg(['max','count']).reindex(idx); sea.loc[sea['count']!=24,'max']=np.nan
    f=pd.DataFrame(index=idx); f['rain']=rain['sum']; f['max_hour']=rain['max']; f['prev3']=f.rain.shift(1).rolling(3,min_periods=3).sum(); f['sea']=sea['max']; f['sin']=np.sin(2*np.pi*idx.dayofyear/365.25); f['cos']=np.cos(2*np.pi*idx.dayofyear/365.25)
    ld={'label_minus_1d':-1,'label_plus_1d':1}.get(alignment,0)
    # Date sensitivity translates the entire reviewed date mask, not individual uncertain days into negatives.
    pos={pd.Timestamp(x)+pd.Timedelta(days=ld):st for x,st in zip(basepos.positive_date,basepos.storm)}
    mask={x+pd.Timedelta(days=ld) for x in uncertain}; mask-=set(pos)
    y=pd.Series(0.,index=idx); y.loc[y.index.isin(mask)]=np.nan; y.loc[y.index.isin(pos)]=1
    group=pd.Series('',index=idx); group.loc[group.index.isin(pos)]=[pos[d] for d in group.index[group.index.isin(pos)]]
    for exp,shift in [('retrospective',0),('lagged',1)]:
      X=f.shift(shift)
      for coverage,columns in [('rain_only',['rain','max_hour','prev3','sin','cos']),('rain_sea_common',['rain','max_hour','prev3','sea','sin','cos'])]:
       eligible=y.notna() & X[columns].notna().all(axis=1)
       for year in [2023,2024,2025,2026]:
        start=pd.Timestamp(f'{year}-01-01'); end=min(pd.Timestamp(f'{year}-12-31'),idx[-1]); train=eligible & (idx<start-pd.Timedelta(days=8)); test=eligible & (idx>=start)&(idx<=end)
        # Exclude entire storm from training if its reviewed incident envelope overlaps test.
        testgroups=set(events.loc[(events.anchor>=start-pd.Timedelta(days=2))&(events.anchor<=end+pd.Timedelta(days=2)),'storm'])
        train &= ~group.isin(testgroups)
        yt=y[train].astype(int); yv=y[test].astype(int); ngtr=group[train][yt.eq(1)].nunique(); ngte=group[test][yv.eq(1)].nunique()
        valid=ngtr>=2 and ngte>=1
        folds.append(dict(alignment=alignment,experiment=exp,coverage=coverage,fold=year,train_start=str(idx[train][0].date()) if train.any() else '',train_end=str(idx[train][-1].date()) if train.any() else '',test_start=str(start.date()),test_end=str(end.date()),train_days=len(yt),test_days=len(yv),train_positive_days=int(yt.sum()),test_positive_days=int(yv.sum()),train_storms=ngtr,test_storms=ngte,eligible=valid))
        if not valid: continue
        a=X.loc[train]; b=X.loc[test]
        for model in (['prevalence','season','rain_threshold','rain_logistic'] if coverage=='rain_only' else ['rain_logistic','rain_sea_logistic']):
         cutoff=.5; threshold=np.nan
         if model=='prevalence': p=np.repeat(yt.mean(),len(yv))
         elif model=='rain_threshold':
          best=(-1,0)
          for t in np.unique(a.rain.quantile(np.linspace(.5,.99,30))):
           pred=a.rain>=t; tp=((pred)&(yt==1)).sum(); fp=((pred)&(yt==0)).sum(); fn=((~pred)&(yt==1)).sum(); score=2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0
           if score>best[0]: best=(score,t)
          threshold=best[1]; p=(b.rain>=threshold).astype(float).values
         else:
          cols={'season':['sin','cos'],'rain_logistic':['rain','max_hour','prev3'],'rain_sea_logistic':['rain','max_hour','prev3','sea']}[model]
          pipe=make_pipeline(StandardScaler(),LogisticRegression(C=.1,class_weight='balanced',max_iter=2000,random_state=42)); pipe.fit(a[cols],yt); p=pipe.predict_proba(b[cols])[:,1]
         pred=p>=cutoff
         rows.append(dict(alignment=alignment,experiment=exp,coverage=coverage,fold=year,model=model,train_days=len(yt),train_positive_days=int(yt.sum()),train_storms=ngtr,test_days=len(yv),test_positive_days=int(yv.sum()),test_storms=ngte,prevalence=yv.mean(),average_precision=average_precision_score(yv,p),precision_agreement=precision_score(yv,pred,zero_division=0),recall_agreement=recall_score(yv,pred,zero_division=0),flagged_days=int(pred.sum()),threshold_mm=threshold))
         if alignment=='nominal': scores.extend(dict(date=str(d.date()),experiment=exp,coverage=coverage,fold=year,model=model,reported=int(v),score=float(z),storm=group.loc[d]) for d,v,z in zip(yv.index,yv,p))
    if alignment=='nominal':
     f['reported']=y; f['storm']=group; f.index.name='date'; f.to_csv(O/'daily_data.csv')
pd.DataFrame(rows).to_csv(O/'metrics.csv',index=False); pd.DataFrame(scores).to_csv(O/'scores.csv',index=False); pd.DataFrame(folds).to_csv(O/'folds.csv',index=False)
m=pd.DataFrame(rows); fig,ax=plt.subplots(figsize=(9,4)); sub=m[(m.alignment=='nominal')&(m.coverage=='rain_only')&(m.model.isin(['prevalence','season','rain_threshold','rain_logistic']))]
for model,g in sub.groupby('model'): 
 for exp,gg in g.groupby('experiment'): ax.plot(gg.fold,gg.average_precision,marker='o',label=f'{model}, {exp}')
ax.set(xlabel='Test year',ylabel='Average precision: agreement with reports',title='Held-out reported-flood agreement (small event counts)'); ax.set_xticks([2023,2024,2025,2026]); ax.legend(fontsize=7,ncol=2); fig.tight_layout(); fig.savefig(O/'agreement_by_fold.png',dpi=300); fig.savefig(O/'agreement_by_fold.pdf'); plt.close(fig)
print(pd.DataFrame(folds).query("alignment == 'nominal' and experiment == 'retrospective'").to_string(index=False)); print(m.query("alignment == 'nominal' and coverage == 'rain_only'").to_string(index=False))
# Companion paper figure from the nominal daily file.
daily_plot=pd.read_csv(O/'daily_data.csv',parse_dates=['date']); fig,ax=plt.subplots(figsize=(10,3.5)); ax.plot(daily_plot.date,daily_plot.rain,color='#31756c',lw=.5); q=daily_plot[daily_plot.reported==1]; ax.scatter(q.date,q.rain,c='#b85231',s=18,label='Retained reported day',zorder=3); ax.set(title='Malé reanalysis rainfall and retained reported days',ylabel='Nominal daily rainfall (mm)',xlabel='Date'); ax.legend(); fig.tight_layout(); fig.savefig(O/'rainfall_reported_days.png',dpi=300); fig.savefig(O/'rainfall_reported_days.pdf'); plt.close(fig)
