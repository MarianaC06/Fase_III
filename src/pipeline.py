"""Reproducible Uber fare training and inference pipeline."""
import argparse,json,hashlib,platform
from pathlib import Path
import numpy as np,pandas as pd,joblib
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score
from sklearn.model_selection import train_test_split
FEATURES=['distance_km','pickup_hour','pickup_weekday','pickup_year','pickup_month','passenger_count','pickup_latitude','pickup_longitude','dropoff_latitude','dropoff_longitude']
def haversine(lat1,lon1,lat2,lon2):
    r=6371.;a=np.sin(np.radians(lat2-lat1)/2)**2+np.cos(np.radians(lat1))*np.cos(np.radians(lat2))*np.sin(np.radians(lon2-lon1)/2)**2
    return 2*r*np.arcsin(np.sqrt(np.clip(a,0,1)))
def prepare(df,training=True):
    d=df.copy();d['pickup_datetime']=pd.to_datetime(d['pickup_datetime'],utc=True,errors='coerce')
    cols=['pickup_longitude','pickup_latitude','dropoff_longitude','dropoff_latitude','passenger_count']
    for c in cols:d[c]=pd.to_numeric(d[c],errors='coerce')
    valid=d['pickup_datetime'].notna() & d[cols].notna().all(axis=1)
    valid &= d['pickup_latitude'].between(40,42)&d['dropoff_latitude'].between(40,42)&d['pickup_longitude'].between(-75,-72)&d['dropoff_longitude'].between(-75,-72)
    valid &= d['passenger_count'].between(1,6)
    if training:valid &= pd.to_numeric(d['fare_amount'],errors='coerce').between(2.5,200)
    d=d.loc[valid].copy();d['distance_km']=haversine(d.pickup_latitude,d.pickup_longitude,d.dropoff_latitude,d.dropoff_longitude)
    d=d.loc[d.distance_km.between(.1,100)].copy();t=d.pickup_datetime.dt
    d['pickup_hour']=t.hour;d['pickup_weekday']=t.dayofweek;d['pickup_year']=t.year;d['pickup_month']=t.month
    return d
def train(input_path,output_dir):
    output_dir=Path(output_dir);output_dir.mkdir(parents=True,exist_ok=True)
    raw=pd.read_csv(input_path);d=prepare(raw)
    X=d[FEATURES];y=d.fare_amount
    Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.2,random_state=42)
    model=HistGradientBoostingRegressor(max_iter=90,max_leaf_nodes=31,learning_rate=.1,l2_regularization=1,random_state=42)
    model.fit(Xtr,ytr);pred=model.predict(Xte)
    metrics={'records_original':len(raw),'records_valid':len(d),'train_rows':len(Xtr),'test_rows':len(Xte),'mae_usd':round(float(mean_absolute_error(yte,pred)),4),'rmse_usd':round(float(np.sqrt(mean_squared_error(yte,pred))),4),'r2':round(float(r2_score(yte,pred)),4),'baseline_mae_usd':round(float(mean_absolute_error(yte,np.full(len(yte),ytr.median()))),4),'model_version':'1.0.0','split_seed':42,'dataset_sha256':hashlib.sha256(Path(input_path).read_bytes()).hexdigest(),'python':platform.python_version()}
    joblib.dump({'model':model,'features':FEATURES,'version':'1.0.0'},output_dir/'model.joblib');(output_dir/'metrics.json').write_text(json.dumps(metrics,indent=2),encoding='utf8')
    pd.DataFrame({'actual':yte.to_numpy(),'predicted':pred}).head(300).to_csv(output_dir/'sample_predictions.csv',index=False)
    print(json.dumps(metrics,indent=2));return metrics
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',default='data/uber.csv');p.add_argument('--output',default='artifacts');a=p.parse_args();train(a.input,a.output)
