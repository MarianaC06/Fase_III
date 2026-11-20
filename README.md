# UberFare AI | Fase III integrada

Integra la **API e interfaz web de fase II** con el **modelo, métricas y pipeline de fase III**. El modelo canónico es `artifacts/model.joblib` (HistGradientBoostingRegressor); no se mezclan predicciones de modelos distintos.

## Ejecutar
```bash
python -m venv .venv
# activar el entorno virtual
pip install -r requirements.txt
pytest -q
uvicorn app.main:app --reload
```
Abrir http://127.0.0.1:8000 y http://127.0.0.1:8000/docs.

## Entrenar de nuevo
`python -m src.pipeline --input data/uber.csv --output artifacts`

## Contenedor
`docker compose up --build` (requiere Docker instalado; no se afirma que haya sido ejecutado).

## Evidencias
`evidencias/` contiene salida de pruebas, métricas y verificaciones locales. Las capturas originales de fase II se preservan en `docs/FaseII_Pruebas_Uber.pdf`. GitHub Actions y Kubernetes son configuraciones; deben ejecutarse en infraestructura real para obtener evidencia de despliegue.

## Limitaciones
Datos de 2009-2015; no predice tarifas dinámicas actuales. Los errores son de evaluación histórica. El modelo de fase II se conserva únicamente como antecedente documental.
