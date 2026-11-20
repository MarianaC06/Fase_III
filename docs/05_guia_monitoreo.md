# Monitoreo y auditoría — UberFare AI

## Alcance
Se registra una línea JSON por solicitud a `/predict`, con hora UTC, ID de evento, estado HTTP, latencia y versión del modelo. No se guardan coordenadas, pasajeros ni cargas completas. Las métricas agregadas incluyen total, éxito, rechazos, errores del servidor y latencia p95.

## Ejecución y evidencia
Desde la raíz del proyecto, con dependencias instaladas:

```bash
python -m pytest -q
python -m scripts.generate_monitoring_evidence
```

Se generan `evidencias/monitoreo/resumen_demo.json` y `auditoria_demo.jsonl`. Para evidencias, capturar la terminal y abrir ambos archivos. Los resultados son de una **simulación local**, no de producción.

## Interpretación
Los HTTP 422 reflejan rechazos de validación; no son necesariamente fallas del sistema. La latencia p95 con tres solicitudes es ilustrativa y no representativa de carga real. Las métricas MAE, RMSE y R² en `artifacts/metrics.json` corresponden a evaluación offline, no a monitoreo de predicciones reales.

## Límites y mejoras
El endpoint `/monitoring/summary` es solo para demostración local y **debe eliminarse o protegerse con autenticación** antes de exponer la API. El registro JSONL no es una solución centralizada ni resistente a múltiples réplicas. No hay detección de drift real ni actualización automática del modelo. Como mejoras: métricas Prometheus, registros centralizados, alertas, control de acceso y evaluación periódica con etiquetas reales.
