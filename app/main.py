import time
from fastapi import Request
from app import monitoring
from pathlib import Path
from datetime import datetime
from typing import Annotated
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from src.pipeline import prepare, FEATURES
ROOT=Path(__file__).resolve().parents[1]
app=FastAPI(title='Uber Fare Predictor API',version='1.0.0')
@app.middleware("http")
async def audit_requests(request: Request, call_next):
    start = time.perf_counter()
    status = 500

    try:
        response = await call_next(request)
        status = response.status_code
        return response
    finally:
        if request.url.path == "/predict":
            duration_ms = (time.perf_counter() - start) * 1000

            monitoring.record(
                method=request.method,
                route=request.url.path,
                status=status,
                duration_ms=duration_ms,
                model_version=bundle["version"]
            )
bundle=joblib.load(ROOT/'artifacts'/'model.joblib')
model=bundle['model']
class Ride(BaseModel):
    pickup_datetime:datetime
    pickup_latitude:Annotated[float,Field(ge=40,le=42)]
    pickup_longitude:Annotated[float,Field(ge=-75,le=-72)]
    dropoff_latitude:Annotated[float,Field(ge=40,le=42)]
    dropoff_longitude:Annotated[float,Field(ge=-75,le=-72)]
    passenger_count:Annotated[int,Field(ge=1,le=6)]
@app.get('/')
def home():return FileResponse(ROOT/'app'/'static'/'index.html')
@app.get('/health')
def health():return {'status':'ok','model_loaded':True,'model_version':bundle['version']}
@app.post('/predict')
def predict(ride:Ride):
    d=ride.model_dump();d['pickup_datetime']=ride.pickup_datetime.isoformat()
    X=prepare(pd.DataFrame([d]),training=False)
    if X.empty:raise HTTPException(422,'Viaje fuera de los criterios de validación')
    distance=float(X.distance_km.iloc[0])
    if not .1<=distance<=100:raise HTTPException(422,'La distancia debe estar entre 0.1 y 100 km')
    fare=max(0,float(model.predict(X[FEATURES])[0]))
    return {'estimated_fare_usd':round(fare,2),'distance_km':round(distance,2),'note':'Estimación académica basada en viajes históricos; no es una tarifa actual de Uber.'}
@app.get("/monitoring/summary")
def monitoring_summary():
    return monitoring.summary()
