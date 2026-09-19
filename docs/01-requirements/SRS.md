# Especificación de requisitos de software

## 1. Propósito

Definir requisitos verificables para Gymratic. Este documento es la referencia funcional; las decisiones de implementación viven en arquitectura y ADR.

## 2. Convenciones

- **SHALL / deberá:** obligatorio.
- **SHOULD / debería:** recomendado, con desviación justificada.
- **MAY / podrá:** opcional.
- Prioridad: P0 imprescindible, P1 importante, P2 experimental.

## 3. Actores y sistemas externos

- `PersonalUser`: propietario y único usuario.
- `AndroidClient`: aplicación en Realme GT 6.
- `TezkatliNode`: cómputo e inferencia privada.
- `AmazfitActive`: interfaz auxiliar.
- `ZeppApp`: puente del reloj.
- `HealthConnect`: intercambio de datos de salud en Android.
- `FoodCatalog`: catálogos importados y normalizados.

## 4. Requisitos funcionales

### 4.1 Entrenamiento

- **FUN-TRN-001 · P0:** el sistema deberá iniciar, pausar, reanudar, revisar y finalizar una sesión.
  - Aceptación: cada transición se persiste y se restaura después de cerrar el proceso.
- **FUN-TRN-002 · P0:** una sesión deberá admitir cardio inicial, fuerza y cardio final, permitiendo omitir cualquiera.
  - Aceptación: la sesión final conserva fases realizadas, orden y tiempos.
- **FUN-TRN-003 · P0:** cada serie deberá registrar ejercicio, variante/máquina, repeticiones, carga, unidad, RIR o RPE, tipo y marca temporal.
  - Aceptación: se rechazan cantidades negativas y unidades incompatibles.
- **FUN-TRN-004 · P0:** la pantalla deberá mostrar valores anteriores y objetivo sin navegación adicional.
  - Aceptación: se muestra el registro anterior de la misma variante/equipo.
- **FUN-TRN-005 · P0:** el usuario deberá corregir o deshacer una serie preservando auditoría.
  - Aceptación: la corrección conserva valor previo, valor nuevo, hora y motivo opcional.
- **FUN-TRN-006 · P0:** deberá existir temporizador automático configurable por ejercicio o serie.
  - Aceptación: continúa correctamente tras background o recreación de UI.
- **FUN-TRN-007 · P1:** deberá soportar calentamiento, trabajo, drop set, fallo y series asistidas.
- **FUN-TRN-008 · P1:** deberá calcular discos por lado y calentamientos sin alterar registros.
- **FUN-TRN-009 · P1:** deberá detectar récords con fórmula y versión explícitas.

### 4.2 Rutinas y gimnasio

- **FUN-ROU-001 · P0:** el usuario deberá crear, clonar, editar, versionar y archivar rutinas.
- **FUN-ROU-002 · P1:** el sistema deberá proponer rutinas compatibles con objetivo, tiempo, historial y equipo.
- **FUN-ROU-003 · P1:** toda propuesta deberá presentar razones y alternativas.
- **FUN-ROU-004 · P1:** el usuario deberá marcar ejercicios como preferidos, menos recomendados, temporalmente no disponibles o excluidos.
- **FUN-GYM-001 · P1:** el sistema deberá detectar una posible llegada al gimnasio y solicitar confirmación antes de iniciar.
- **FUN-GYM-002 · P0:** el catálogo del gimnasio deberá ser editable, versionado y distinguir verificado de inferido.
- **FUN-GYM-003 · P1:** el estado temporal de una máquina no deberá modificar su existencia en el catálogo.

### 4.3 Nutrición

- **FUN-NUT-001 · P0:** el sistema deberá aceptar alimentos por búsqueda, texto, código de barras, OCR, fotografía y captura manual.
- **FUN-NUT-002 · P0:** una inferencia deberá producir un borrador editable y nunca una entrada confirmada automática.
- **FUN-NUT-003 · P0:** toda cantidad deberá clasificar su método como `MEASURED`, `CALCULATED`, `ESTIMATED`, `ASSUMED` o `USER_CONFIRMED`.
- **FUN-NUT-004 · P0:** un alimento deberá conservar fuente, identificador externo, versión y nivel de calidad.
- **FUN-NUT-005 · P0:** el usuario deberá ajustar, sustituir, dividir, agregar o eliminar componentes antes de confirmar.
- **FUN-NUT-006 · P1:** deberá soportar recetas con ingredientes, masa final, rendimiento y porciones.
- **FUN-NUT-007 · P1:** deberá guardar y reutilizar comidas habituales y porciones personales.
- **FUN-NUT-008 · P1:** una captura precisa deberá admitir múltiples vistas, referencia geométrica o peso visible.
- **FUN-NUT-009 · P1:** deberá advertir ingredientes visualmente ocultos probables sin inventarlos como confirmados.

### 4.4 Suplementos

- **FUN-SUP-001 · P0:** deberá registrar producto, marca, presentación, cantidad por unidad, dosis y hora.
- **FUN-SUP-002 · P0:** deberá permitir confirmar, omitir, posponer o corregir una ingesta.
- **FUN-SUP-003 · P1:** deberá mantener inventario y estimar fecha de reposición.
- **FUN-SUP-004 · P1:** deberá aceptar producto por texto, código u OCR de etiqueta.
- **FUN-SUP-005 · P0:** no deberá generar prescripciones ni modificar dosis por decisión de IA.

### 4.5 IA

- **FUN-AI-001 · P0:** la inferencia deberá ejecutarse solo en el teléfono o Tezkatli.
- **FUN-AI-002 · P0:** todo resultado deberá guardar hash de entrada, modelo, pesos, prompt, preprocesamiento, esquema y tiempos.
- **FUN-AI-003 · P0:** la salida deberá validarse contra un esquema estructurado antes de mostrarse.
- **FUN-AI-004 · P0:** si Tezkatli está ausente, el trabajo deberá permanecer en cola y existir entrada manual.
- **FUN-AI-005 · P1:** el sistema deberá reutilizar correcciones personales antes de ejecutar inferencia pesada cuando exista coincidencia suficiente.
- **FUN-AI-006 · P1:** ningún modelo nuevo deberá promoverse sin evaluación contra baseline y aprobación manual.

### 4.6 Amazfit y Health Connect

- **FUN-WEA-001 · P1:** el reloj deberá mostrar ejercicio/serie actual y permitir confirmar acciones rápidas si la PoC resulta viable.
- **FUN-WEA-002 · P1:** deberá almacenar eventos hasta confirmar recepción.
- **FUN-WEA-003 · P1:** los eventos deberán incluir ID, origen, secuencia, hora y versión.
- **FUN-WEA-004 · P0:** el reloj no será fuente definitiva para repeticiones detectadas automáticamente.
- **FUN-HC-001 · P1:** deberá importar registros autorizados conservando `DataOrigin` y método de grabación.
- **FUN-HC-002 · P1:** deberá exportar sesiones terminadas mediante trabajo puntual.

### 4.7 Sincronización, exportación y recuperación

- **FUN-SYN-001 · P0:** entrenamiento, nutrición manual y suplementos deberán operar offline.
- **FUN-SYN-002 · P0:** toda mutación sincronizada deberá ser idempotente y tolerar reordenamiento y duplicación.
- **FUN-SYN-003 · P0:** Android deberá mostrar trabajos pendientes y fallos recuperables.
- **FUN-SYN-004 · P1:** los borrados sincronizados deberán usar tombstones hasta ser reconocidos.
- **FUN-EXP-001 · P0:** deberá exportar datos y metadatos en un formato documentado.
- **FUN-EXP-002 · P0:** deberá restaurar un respaldo compatible sin pérdida silenciosa.

## 5. Requisitos no funcionales

### Fiabilidad y disponibilidad

- **NFR-REL-001 · P0:** ninguna serie confirmada deberá perderse por cierre inesperado.
- **NFR-REL-002 · P0:** reintentar la misma operación no deberá duplicar datos.
- **NFR-AVA-001 · P0:** funciones esenciales no dependerán de Tezkatli ni Internet.
- **NFR-REC-001 · P0:** deberá probarse restauración completa antes de considerar confiable el respaldo.

### Rendimiento y eficiencia

- **NFR-PER-001 · P0:** objetivo inicial de mediana menor a 100 ms para persistir una serie en Realme GT 6.
- **NFR-PER-002 · P0:** objetivo inicial de TTFD menor a 500 ms para la sesión activa.
- **NFR-PER-003 · P1:** la UI no deberá bloquearse durante inferencia o sincronización.
- **NFR-EFF-001 · P1:** ubicación y sincronización deberán respetar restricciones de batería y conectividad.

### Seguridad y privacidad

- **NFR-SEC-001 · P0:** Tezkatli no deberá exponerse directamente a Internet público.
- **NFR-SEC-002 · P0:** secretos no deberán existir en código, APK, repositorio o logs.
- **NFR-SEC-003 · P0:** las entradas de imagen/texto deberán validarse y tratarse como no confiables.
- **NFR-PRI-001 · P0:** el usuario deberá controlar retención y eliminación de imágenes.
- **NFR-PRI-002 · P0:** logs y métricas deberán excluir contenido personal por defecto.

### Usabilidad, mantenibilidad y compatibilidad

- **NFR-USA-001 · P0:** completar una serie normal requerirá como máximo dos acciones deliberadas.
- **NFR-USA-002 · P0:** la UI deberá distinguir pendiente, estimado y confirmado sin depender solo del color.
- **NFR-MAI-001 · P0:** no se permitirán ciclos entre módulos Gradle.
- **NFR-MAI-002 · P0:** cambios arquitectónicos deberán documentarse mediante ADR.
- **NFR-COM-001 · P0:** contratos persistentes o de red incompatibles deberán aumentar versión o incluir migración.

### IA

- **NFR-AI-001 · P0:** la IA no deberá confirmar ni sobrescribir datos del dominio.
- **NFR-AI-002 · P0:** métricas de IA deberán reportar dataset, tamaño, condiciones y versión.
- **NFR-AI-003 · P1:** la interfaz deberá mostrar incertidumbre o limitación útil, no “confianza” autodeclarada por el LLM.

## 6. Restricciones de datos

- Masa persistida en unidad base entera o decimal de escala fija.
- Tiempo persistido como `Instant` más zona cuando sea relevante.
- Identificadores globalmente únicos para eventos sincronizables.
- Ningún valor derivado sustituye el dato fuente.
- Toda métrica derivada conserva `algorithmVersion`.

## 7. Supuestos abiertos

- Capacidad exacta y software final de Tezkatli.
- API level y compatibilidad real del Amazfit Active.
- Inventario físico del gimnasio.
- Umbral personal aceptable de error en porciones.
- Frecuencia y política final de respaldos.
