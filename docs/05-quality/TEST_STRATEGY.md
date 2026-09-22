# Estrategia de pruebas

## Objetivo

Demostrar comportamiento, no solo cobertura. La evidencia debe vincularse con requisitos y riesgos.

La descomposición documental vigente está en
[`docs/00-governance/TDD_SDD_SERIES.md`](../00-governance/TDD_SDD_SERIES.md).
Los casos `TST-CAN-*`, `TST-UI-*`, `TST-MED-*` y `TST-BLD-*` son la primera
extensión para las rutinas HTML canónicas; los casos `TST-TRN-*` en adelante
se conservan para la aplicación Android y los servicios previstos.

## Capas

| Capa | Ejemplos | Frecuencia |
|---|---|---|
| Unitarias | invariantes, fórmulas, state machines | Cada cambio |
| Propiedades | unidades, serialización, idempotencia | Cada cambio relevante |
| Componentes | Room, repositorios, cola, workers | CI |
| Contratos | OpenAPI, JSON Schema, compatibilidad | CI |
| Integración | Android–API–worker | CI/local |
| UI | Compose y navegación crítica | CI selectiva |
| Sistema | sesión/comida/respaldo E2E | Release candidate |
| Hardware | Realme, Amazfit, Tezkatli, red móvil | Milestone/release |
| IA | golden sets y regresión | Cambio de modelo/pipeline |
| Seguridad | SAST, dependencias, MASVS, amenazas | CI/release |

## Pruebas críticas iniciales

- **TST-TRN-001:** transiciones válidas e inválidas de sesión.
- **TST-TRN-002:** registro con unidades, límites y tipos de serie.
- **TST-TRN-003:** corrección conserva revisión.
- **TST-SYN-001:** operación completa sin red.
- **TST-SYN-002:** entrega repetida no duplica agregado.
- **TST-REL-001:** process death después de confirmar serie.
- **TST-NUT-001:** cada método de captura termina en borrador coherente.
- **TST-NUT-002:** IA no escribe una comida confirmada.
- **TST-NUT-003:** método de medición se conserva por componente.
- **TST-AI-001:** caída de Tezkatli deja trabajo recuperable.
- **TST-AI-002:** toda respuesta contiene procedencia completa.
- **TST-AI-003:** autorización de escritura rechaza actor IA.
- **TST-CON-001:** esquemas válidos aceptan ejemplos mínimos y rechazan formatos, estados y propiedades inválidas.
- **TST-GYM-001:** histéresis evita eventos repetidos.
- **TST-WEA-001:** desconexión/reenvío/deduplicación en reloj real.
- **TST-SEC-001:** servicio no es alcanzable públicamente.
- **TST-REC-001:** respaldo se restaura en almacenamiento limpio.
- **TST-PRO-006:** abrir la portada con perfil predeterminado debe navegar a `#profile`; al definir un dato, una recarga debe conservar el inicio normal; un perfil ya definido no debe cambiar la navegación ni borrar el progreso.
- **TST-PRO-007:** validar que series de hoy, actividad dentro de siete días, actividad más antigua, timestamps futuros y ausencia de registros produzcan la frase correspondiente sin inventar resultados ni modificar datos.

## Casos frontera

- Cambio de zona horaria y horario de verano.
- Reinicio del teléfono y Tezkatli.
- Hora incorrecta en reloj.
- Carga `0` válida para peso corporal vs dato desconocido.
- Imagen enorme, corrupta o no alimentaria.
- Código de barras desconocido o asociado incorrectamente.
- Respuesta de IA tardía después de una corrección.
- Migración interrumpida.
- Espacio insuficiente.
- Health Connect con múltiples orígenes.

## Rendimiento

Critical User Journeys:

1. Abrir sesión activa.
2. Completar una serie.
3. Consultar valores anteriores.
4. Capturar comida.
5. Editar y confirmar componentes.

Medir TTID, TTFD, jank, escritura, memoria, batería, temperatura, red, cola, latencia y VRAM. Los objetivos de SRS son hipótesis hasta ejecutarse en Realme GT 6.

## IA

Reportar como mínimo:

- Dataset y condiciones.
- Accuracy top-k de alimento.
- IoU/Dice de segmentación.
- MAE y MAPE de masa.
- Error absoluto de energía/macros.
- Tasa de corrección humana.
- Calibración y cobertura.
- Latencia p50/p95.
- Memoria/VRAM máxima.
- Fallos, abstenciones y desconocidos.

No mezclar conjunto de ajuste personal con conjunto de evaluación.

## Gate de release

- Pruebas P0 aprobadas.
- Migraciones desde cada versión soportada.
- Restauración probada.
- Benchmark sin regresión no aceptada.
- Revisión de permisos y MASVS.
- SBOM y escaneo de secretos.
- Evidencia física para funciones de hardware.
