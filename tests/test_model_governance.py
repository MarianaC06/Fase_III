import json,joblib
from pathlib import Path
from src.pipeline import FEATURES
ROOT=Path(__file__).resolve().parents[1]
def test_model_features_and_version():
    bundle=joblib.load(ROOT/'artifacts/model.joblib')
    assert bundle['features']==FEATURES
    assert bundle['version']=='1.0.0'
def test_model_beats_baseline():
    m=json.loads((ROOT/'artifacts/metrics.json').read_text())
    assert m['mae_usd'] < m['baseline_mae_usd']
    assert m['test_rows']>1000
