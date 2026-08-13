# Arquitectura del sistema

## Estilo

Monolito modular distribuido entre tres ejecutables:

1. Aplicación Android local-first.
2. API/worker privado en Tezkatli.
3. Aplicación Zepp auxiliar, condicionada por PoC.

No se adoptan microservicios, CQRS completo, event sourcing completo, Kubernetes ni CRDT en la primera etapa.

## Contexto

```mermaid
flowchart LR
    U["Usuario"] --> A["Android"]
    U --> W["Amazfit Active"]
    W <--> Z["Zepp App / Side Service"]
    Z <--> T["Tezkatli privado"]
    A <--> T
    A <--> H["Health Connect"]
    T --> C["Catálogos importados"]
```

## Contenedores

```mermaid
flowchart LR
    subgraph Android
      UI["Compose UI"] --> APP["Application/domain"]
      APP --> REP["Repositories"]
      REP --> DB["Room SSOT"]
      REP --> OUT["Transactional outbox"]
      CAP["Camera/OCR/Depth"] --> APP
    end
    subgraph Tezkatli
      API["Private API"] --> JOB["Durable job queue"]
      JOB --> ORCH["Pipeline orchestrator"]
      ORCH --> MODELS["VLM/segmentation/OCR"]
      ORCH --> CAT["Normalized catalogs"]
      ORCH --> ART["Artifacts/provenance"]
    end
    OUT <--> API
```

## Propiedad de datos

| Información | Propietario operativo | Réplica/derivado |
|---|---|---|
| Entrenamientos confirmados | Room Android | Respaldo/analítica en Tezkatli |
| Alimentación confirmada | Room Android | Respaldo/analítica en Tezkatli |
| Suplementos confirmados | Room Android | Respaldo opcional |
| Trabajos de IA | Tezkatli | Estado/cache en Android |
| Artefactos de modelos | Tezkatli | Ninguna copia obligatoria en teléfono |
| Eventos del reloj no entregados | Amazfit/Side Service | Tezkatli/Android tras ACK |
| Catálogos normalizados | Tezkatli | Subconjunto cacheado en Android |

## Contextos de dominio

- Training
- Routine Planning
- Nutrition
- Supplements
- Gym Catalog
- Capture and Interpretation
- Device Integration
- Synchronization
- Analytics

## Patrones

- UDF y state holders en UI.
- Repository en fronteras de datos.
- State machine para sesión, captura y trabajos.
- Transactional Outbox para sincronización.
- Ports and Adapters para IA, catálogos y dispositivos.
- Strategy y Specification para recomendaciones.
- Composite para comidas y recetas.
- Anti-Corruption Layer para Zepp, Health Connect y catálogos.
- Proyecciones para vistas de alto rendimiento.

## Dependencias Android

```text
app → feature → data → core
integration → contracts/domain ports
core ↛ feature
```

## Decisiones pendientes

- Modelo VLM final después de benchmark.
- Runtime final de GPU en Tezkatli.
- Compatibilidad de Zepp.
- Cifrado exacto de Room según amenaza y costo medido.
- Catálogo nutricional mexicano prioritario.
