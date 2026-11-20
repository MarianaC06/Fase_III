"""Run from repository root: python -m scripts.generate_monitoring_evidence"""
import json
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app import monitoring

out=Path('evidencias/monitoreo')
out.mkdir(parents=True,exist_ok=True)
monitoring.LOG_PATH=out/'auditoria_demo.jsonl'
monitoring.LOG_PATH.unlink(missing_ok=True)
base={'pickup_datetime':'2015-05-07T19:52:00Z','pickup_latitude':40.738354,
'pickup_longitude':-73.999817,'dropoff_latitude':40.723217,
'dropoff_longitude':-73.999512,'passenger_count':1}
with TestClient(app) as client:
    responses=[client.post('/predict',json=base),
               client.post('/predict',json={**base,'passenger_count':0}),
               client.post('/predict',json={**base,'dropoff_latitude':40.7200})]
    report={'sample_http_statuses':[r.status_code for r in responses],
            'monitoring':client.get('/monitoring/summary').json()}
(out/'resumen_demo.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(report,indent=2,ensure_ascii=False))
print('Evidencias generadas en:',out)
