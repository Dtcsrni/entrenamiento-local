# Ciclo de vida de IA y MLOps

## Principio

Los modelos son componentes probabilísticos. No sustituyen contratos, catálogos ni cálculo nutricional determinista.

## Ciclos separados

### Serving

```text
input validation → preprocessing → inference → postprocessing
→ schema validation → deterministic checks → draft
```

### Evolución

```text
measured samples → curation → experiment → offline evaluation
→ integrated evaluation → manual promotion → monitoring → rollback
```

## Registro de experimentos

Cada experimento incluye:

- Objetivo e hipótesis.
- Commit de código.
- Dataset manifest y partición.
- Modelo/hash/licencia.
- Prompt y preprocesamiento.
- Hardware y runtime.
- Métricas y artefactos.
- Limitaciones y decisión.

## Datos

Clases:

- `private_raw`: fotografías originales; nunca Git.
- `private_annotated`: etiquetas personales; almacenamiento cifrado.
- `synthetic_fixture`: apto para repositorio.
- `external_dataset`: solo manifiesto/licencia, salvo permiso explícito.

Separar entrenamiento, validación y prueba por plato/receta, evitando variantes de la misma captura entre particiones.

## Baselines

Antes de un VLM complejo medir:

- Reutilización de comida personal.
- Catálogo/código de barras.
- Clasificación simple.
- Estimación por porción estándar.
- Usuario humano sin báscula.

Un modelo candidato debe superar la baseline en la métrica primaria sin degradar límites de memoria, latencia o abstención.

## Promoción

Estados:

```text
experimental → candidate → approved → deprecated → retired
```

Requisitos de promoción:

- Reporte reproducible.
- Esquema compatible.
- Golden set sin regresión crítica.
- Límites documentados.
- Modelo de amenaza revisado.
- Rollback disponible.

## Correcciones personales

Se almacenan como señales etiquetadas. No disparan entrenamiento automático. Primero alimentan memoria personal y evaluación; cualquier ajuste se promueve manualmente.

## Monitoreo

- Tasa de abstención.
- Componentes corregidos.
- Error medido cuando existe báscula.
- Desconocidos.
- Latencia y fallos.
- Cambios de distribución en comidas habituales.
- Uso de fallback.
