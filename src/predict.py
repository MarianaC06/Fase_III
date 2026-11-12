import argparse,json,joblib,pandas as pd
from pipeline import prepare

def predict(model_path,rows):
    bundle=joblib.load(model_path);clean=prepare(pd.DataFrame(rows),training=False)
    if len(clean)!=len(rows):raise ValueError('Invalid input coordinates, time, passengers or distance')
    return bundle['model'].predict(clean[bundle['features']]).round(2).tolist()
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--model',default='artifacts/model.joblib');p.add_argument('--json',required=True);a=p.parse_args()
    print(json.dumps({'predictions_usd':predict(a.model,json.loads(a.json))}))
