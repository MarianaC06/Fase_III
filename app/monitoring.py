"""Basic local observability. No raw coordinates, payloads, or passenger data are logged."""
import json
import os
import threading
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

LOG_PATH = Path(os.getenv('UBERFARE_AUDIT_LOG', 'runtime/audit.jsonl'))
_lock = threading.Lock()

def record(method: str, route: str, status: int, duration_ms: float, model_version: str):
    event = {'event_id': str(uuid4()), 'timestamp_utc': datetime.now(timezone.utc).isoformat(),
             'method': method, 'route': route, 'status_code': status,
             'duration_ms': round(duration_ms, 3), 'model_version': model_version}
    with _lock:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LOG_PATH.open('a', encoding='utf-8') as f:
            f.write(json.dumps(event, ensure_ascii=False) + '\n')
    return event

def summary():
    events=[]
    if LOG_PATH.exists():
        for line in LOG_PATH.read_text(encoding='utf-8').splitlines():
            try: events.append(json.loads(line))
            except json.JSONDecodeError: continue
    requests=[e for e in events if e.get('route') == '/predict']
    latencies=sorted(float(e['duration_ms']) for e in requests)
    n=len(latencies)
    return {'total_prediction_requests': n,
            'successful_predictions': sum(e.get('status_code') == 200 for e in requests),
            'rejected_predictions': sum(e.get('status_code') == 422 for e in requests),
            'server_errors': sum(e.get('status_code',0) >= 500 for e in requests),
            'p95_latency_ms': round(latencies[max(0, int((n*0.95 + 0.999999))-1)], 3) if n else None,
            'status_counts': dict(Counter(str(e['status_code']) for e in requests)),
            'note': 'Métricas de solicitudes locales. No miden drift ni precisión en producción.'}
