# UberFare AI — MLOps + GitOps (prototipo reproducible)

Predicción de tarifas históricas de Uber NYC con datos 2009–2015. No representa precios actuales.

## Ejecución

```bash
pip install -r requirements.txt
pytest -q
python src/pipeline.py --input data/uber.csv --output artifacts
python src/predict.py --model artifacts/model.joblib --json '[{"pickup_datetime":"2015-05-07 19:52:06 UTC","pickup_latitude":40.738354,"pickup_longitude":-73.999817,"dropoff_latitude":40.723217,"dropoff_longitude":-73.999512,"passenger_count":1}]'
```

Coloca `uber.csv` en `data/`. El entrenamiento genera modelo, métricas y predicciones de muestra. El workflow de GitHub Actions ejecuta pruebas en cada push/PR al publicar el repositorio. `gitops/deployment.yaml` documenta un estado deseado ilustrativo: **no** constituye un despliegue real ni un servicio de inferencia implementado.

## Diseño y limitaciones

- Limpieza: tarifa 2.5–200 USD, pasajeros 1–6, coordenadas aproximadas del área de NYC y distancia 0.1–100 km.
- Variables: distancia Haversine, hora, día, mes, año, pasajeros y coordenadas.
- División aleatoria 80/20 con semilla 42; evaluación retrospectiva, no validación temporal de producción.
- Modelo: HistGradientBoostingRegressor. Métricas MAE, RMSE, R² y baseline de mediana.
- No se ha realizado integración con GitHub, Kubernetes, Argo CD, DVC, MLflow ni monitoreo continuo real; se describe su diseño objetivo en los PDF.
- Para producción: añadir API autenticada, imagen Docker, escaneo de seguridad, registro de modelos, GitOps reconciliado, alertas, trazabilidad, evaluación temporal y pruebas de carga.
