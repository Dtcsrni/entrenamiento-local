# Modelo de datos conceptual

## Agregados

### WorkoutSession

```text
WorkoutSession
├─ sessionId
├─ lifecycleState
├─ startedAt / endedAt
├─ phases[]
│  ├─ CardioSegment
│  └─ ExerciseBlock
│     └─ PerformedSet[]
├─ source
└─ revision
```

Invariantes:

- Carga, duración y repeticiones no negativas.
- Una serie pertenece a una sola sesión.
- Una corrección conserva revisión previa.
- El cierre no elimina trabajos de sincronización pendientes.

### RoutinePlan

Contiene versión, objetivo, restricciones, bloques, alternativas y perfil de equipamiento. Una sesión captura la versión usada para preservar historia.

### MealEntry

```text
MealEntry
├─ mealId
├─ capturedAt
├─ status
├─ components[]
│  ├─ canonicalFoodId
│  ├─ amount
│  ├─ measurementMethod
│  ├─ source
│  ├─ confidenceEvidence
│  └─ nutrients
├─ analysisJobId?
└─ revision
```

### SupplementIntake

Separa producto, programa e ingesta real. La omisión no se representa como dosis cero.

### AnalysisJob

Incluye estado, claves de idempotencia, hashes, versiones, resultado estructurado, advertencias y errores saneados.

## Representación numérica

- Masa: miligramos enteros o decimal fijo.
- Energía: unidad canónica documentada, con conversión a kcal para UI.
- Tiempo: `Instant`; zona separada donde aporte significado.
- Intensidad: tipo explícito, no número sin unidad.
- Valores desconocidos: `null`/ausencia, nunca cero implícito.

## Procedencia

```text
OBSERVED       sensor o hecho visible
MEASURED       instrumento o etiqueta
CALCULATED     fórmula determinista
ESTIMATED      modelo o aproximación
ASSUMED        valor por defecto explícito
USER_CONFIRMED aceptado/corregido por usuario
```

## Auditoría selectiva

No se implementará event sourcing completo. Se conservarán revisiones para correcciones relevantes, confirmaciones de IA, cambios de rutina y versiones de algoritmos.
