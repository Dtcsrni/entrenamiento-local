# Arquitectura del repositorio

```text
apps/
  android/             Cliente y fuente operativa
  zepp/                Interfaz auxiliar condicionada
services/
  tezkatli-api/        API, dominio, infraestructura y workers
packages/
  contracts/           Contratos de red/eventos
  schemas/             Esquemas compartidos
  test-fixtures/       Datos sintéticos
ai/
  pipelines/           Orquestación por tarea
  adapters/            Backends de modelos
  evaluation/          Métricas y golden sets
  registry/            Modelos aprobados/candidatos
  prompts/             Prompts versionados
data/
  seed/                Datos mínimos reproducibles
  catalogs/            Manifiestos de catálogos
docs/                  Documentación gobernada
infra/                 Instalación, red, respaldo y monitoreo
scripts/               Automatización reproducible
tests/                 Pruebas cruzadas y físicas
```

## Regla de creación

Las carpetas de código se materializan al comenzar su incremento. No se agregan proyectos vacíos ni dependencias sin una necesidad ejecutable.
