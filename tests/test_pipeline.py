import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import pandas as pd
from pipeline import haversine,prepare,FEATURES

def test_distance_zero():assert haversine(40.7,-73.9,40.7,-73.9)==0

def test_clean_and_features():
    df=pd.DataFrame([{'pickup_datetime':'2015-01-01 10:00:00 UTC','pickup_latitude':40.75,'pickup_longitude':-73.99,'dropoff_latitude':40.77,'dropoff_longitude':-73.95,'passenger_count':1,'fare_amount':12}, {'pickup_datetime':'2015-01-01 10:00:00 UTC','pickup_latitude':0,'pickup_longitude':0,'dropoff_latitude':0,'dropoff_longitude':0,'passenger_count':0,'fare_amount':-5}])
    clean=prepare(df);assert len(clean)==1;assert set(FEATURES).issubset(clean.columns)
