# Sincronización y procesamiento de IA

## Escritura local-first

En una sola transacción Room:

1. Validar comando.
2. Guardar agregado o revisión.
3. Insertar evento en outbox.
4. Confirmar transacción.
5. Actualizar UI desde `Flow`.

WorkManager drena la cola con backoff. Tezkatli almacena la clave de idempotencia y la respuesta asociada.

## Estado de outbox

```text
PENDING → SENDING → ACKNOWLEDGED
                 ↘ RETRY_WAIT
                 ↘ FAILED_PERMANENT
```

## Política de conflictos

- Android domina sobre entradas confirmadas.
- Una respuesta tardía de IA no sobrescribe una revisión posterior.
- El reloj aporta eventos, no estado definitivo.
- Los borrados usan tombstone hasta ACK.
- Se compara `aggregateId + revision`.

## API de trabajos

```http
POST /v1/food-analyses
Idempotency-Key: <uuid>

202 Accepted
Location: /v1/food-analyses/{jobId}
```

Estados:

```text
QUEUED → RUNNING → SUCCEEDED
                 ↘ FAILED_RETRYABLE
                 ↘ FAILED_PERMANENT
                 ↘ CANCELLED
```

## Pipeline alimentario

```text
quality gate
 → capture routing
 → segmentation
 → identification/OCR
 → geometry/depth
 → volume and density assumptions
 → catalog normalization
 → deterministic nutrient calculation
 → schema validation
 → editable draft
```

## Routing eficiente

```text
barcode → catalog
known personal meal → reuse and review
label/package → OCR
explicit text → local parser
complex photo + Tezkatli → heavy pipeline
no Tezkatli → queued/local manual draft
```

## Seguridad de inferencia

- Sin herramientas de shell o archivos para el LLM.
- Prompts fijos y versionados.
- OCR y texto visual tratados como datos.
- JSON Schema obligatorio.
- Límites de tamaño, tiempo, tokens, memoria y concurrencia.
- Un semáforo GPU inicial.
- Reintentar solo errores transitorios.
