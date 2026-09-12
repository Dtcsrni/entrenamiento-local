# Entrenamiento Local

Sistema personal Android para registrar entrenamiento, alimentación y suplementos, con funcionamiento local-first, integración auxiliar con Amazfit Active e inferencia pesada privada en el equipo Tezkatli.

## Estado

**Fase:** definición y viabilidad técnica. No existe todavía una versión funcional ni se han validado en hardware las capacidades del reloj o los modelos de IA.

## Principios

- Android conserva la fuente operativa de los datos confirmados.
- Las funciones esenciales operan sin red.
- Tezkatli ejecuta trabajos pesados de forma asíncrona y privada.
- La IA produce borradores; las reglas validan y el usuario confirma.
- Todo valor se clasifica como observado, medido, calculado, estimado o confirmado.
- Las decisiones y resultados deben ser trazables y reproducibles.

## Documentación principal

- [Acta del proyecto](docs/00-governance/PROJECT_CHARTER.md)
- [Plan de desarrollo](docs/00-governance/DEVELOPMENT_PLAN.md)
- [Especificación de requisitos](docs/01-requirements/SRS.md)
- [Casos de uso](docs/01-requirements/USE_CASES.md)
- [Backlog inicial](docs/01-requirements/BACKLOG.md)
- [Arquitectura](docs/03-architecture/ARCHITECTURE.md)
- [Modelo de datos](docs/03-architecture/DATA_MODEL.md)
- [Sincronización e IA](docs/03-architecture/SYNC_AND_AI.md)
- [Estrategia de pruebas](docs/05-quality/TEST_STRATEGY.md)
- [Modelo de amenazas](docs/06-security/THREAT_MODEL.md)
- [Ciclo de vida de IA](docs/07-ai/AI_MLOPS.md)
- [Runbook operativo](docs/08-operations/RUNBOOK.md)
- [Fuentes de investigación](docs/09-research/SOURCES.md)
- [Base de evidencia y protocolo para rutinas](docs/09-research/EVIDENCE_BASE_AND_ROUTINE_PROTOCOL.md)
- [Matriz de trazabilidad](docs/00-governance/TRACEABILITY.md)
- [Registro de riesgos](docs/00-governance/RISK_REGISTER.md)
- [Decisiones arquitectónicas](docs/03-architecture/adr/README.md)

## Estructura prevista

```text
apps/android/             Aplicación Android nativa
apps/zepp/                Aplicación auxiliar Zepp OS
services/tezkatli-api/    API y workers privados
packages/contracts/       OpenAPI y JSON Schema compartidos
ai/                       Pipelines, evaluaciones y registro de modelos
data/                     Esquemas, catálogos y datos semilla no personales
docs/                     Requisitos, diseño, calidad y operación
infra/                    Configuración reproducible de Tezkatli y red
scripts/                  Validación y automatización
tests/                    Pruebas de contrato, E2E, hardware y rendimiento
```

## Validación local

```powershell
python scripts/validate_repository.py
```

## Privacidad

No se deben incorporar fotografías personales, bases reales, respaldos, pesos de modelos, tokens, claves, APK firmadas ni resultados que contengan información sensible. Consulte [SECURITY.md](SECURITY.md).
