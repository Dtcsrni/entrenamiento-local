# Tezkatli API

API privada y workers asíncronos. El runtime definitivo y adaptadores de modelos dependen de SPIKE-003.

## Corte actual

Existe solo un liveness server de desarrollo. Enlaza exclusivamente a
`127.0.0.1`; no implementa readiness, autenticación, persistencia, workers ni
inferencia.

```powershell
python services/tezkatli-api/src/tezkatli_api/server.py
Invoke-RestMethod http://127.0.0.1:8771/healthz
```

La exposición por red privada se decidirá después de SPIKE-002 y la capacidad
de ejecución después de SPIKE-003.
