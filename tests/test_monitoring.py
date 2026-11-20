import json
from fastapi.testclient import TestClient
from app.main import app
from app import monitoring

PAYLOAD={'pickup_datetime':'2015-05-07T19:52:00Z','pickup_latitude':40.738354,
'pickup_longitude':-73.999817,'dropoff_latitude':40.723217,
'dropoff_longitude':-73.999512,'passenger_count':1}

def test_monitoring_success_and_rejection(tmp_path, monkeypatch):
    monkeypatch.setattr(monitoring, 'LOG_PATH', tmp_path/'audit.jsonl')
    with TestClient(app) as client:
        assert client.post('/predict',json=PAYLOAD).status_code == 200
        assert client.post('/predict',json={**PAYLOAD,'passenger_count':0}).status_code == 422
        data=client.get('/monitoring/summary').json()
    assert data['total_prediction_requests'] == 2
    assert data['successful_predictions'] == 1
    assert data['rejected_predictions'] == 1
    assert data['p95_latency_ms'] >= 0
    text=(tmp_path/'audit.jsonl').read_text()
    assert 'pickup_latitude' not in text and '40.738354' not in text
    assert all('model_version' in json.loads(x) for x in text.splitlines())
