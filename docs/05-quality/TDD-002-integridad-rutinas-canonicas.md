# TDD-002 — Integridad semántica de rutinas canónicas

**Estado:** `In progress`  
**Versión:** `0.1`  
**Fecha:** `2026-09-17`  
**Diseño asociado:** [SDD-001](../03-architecture/SDD-001-rutina-canonica-versionado.md)

## 1. Objetivo

Detectar automáticamente inconsistencias entre el contenido declarado y las
tres HTML canónicas, especialmente las que no detectan los checks actuales del
repositorio: tarjetas ausentes, índices discontinuos, claves incompletas y
totales falsos.

## 2. Sistema bajo prueba

| Día | Archivo | Contrato declarado |
|---|---|---|
| 1 | `data/rutinas_autocontenidas/canonicas/Rutina_Dia_1_Espalda_Biceps_V1.html` | 6 ejercicios; 20 series; `4 + 4 + 3 + 3 + 3 + 3` según el documento actual |
| 2 | `data/rutinas_autocontenidas/canonicas/Rutina_Dia_2_Pierna_Gluteo_V1.html` | 6 ejercicios; 20 series; `3 + 3 + 3 + 4 + 3 + 4` |
| 3 | `data/rutinas_autocontenidas/canonicas/Rutina_Dia_3_Pecho_Hombro_Triceps_V1.html` | 7 ejercicios; 22 series; `4 + 3 + 3 + 3 + 3 + 3 + 3` |

El contrato del Día 1 debe mantenerse explícito: si se decide volver a otra
distribución, se actualizarán SDD-001, el documento de contenido, la salida y
la matriz de trazabilidad en el mismo cambio.

## 3. Casos de prueba

### TST-CAN-001 — Conteo e índices

**Preparación:** leer cada HTML sin ejecutar scripts y localizar tarjetas con
`data-exercise`.

**Comprobaciones:**

- cantidad de tarjetas igual a `exerciseCount`;
- índices únicos y exactamente contiguos;
- ningún ejercicio declarado desaparece del DOM canónico;
- cada tarjeta tiene título, métricas y tracker.

**Resultado esperado:** Día 1 debe quedar en fallo reproducible mientras falten
las tarjetas 3 y 4; Día 2 y Día 3 deben superar este caso.

### TST-CAN-002 — Suma de series efectivas

**Preparación:** extraer `data-series-keys` por tarjeta y contar las claves.

**Comprobaciones:**

- cada conjunto tiene claves `e{index}s1..e{index}sN`;
- la suma coincide con el total declarado;
- la distribución coincide con dashboard, resumen y documento del día;
- `warmupSet` no se suma como serie efectiva.

**Resultado esperado:** ningún total depende solo de texto visible; cualquier
discrepancia produce ubicación de archivo, ejercicio y valor esperado/real.

### TST-CAN-003 — Navegación sucesiva

**Preparación:** extraer cada `nextExerciseCue`, `data-next` y etiqueta visible.

**Comprobaciones:**

- tarjeta `i` apunta a `i + 1` cuando no es la última;
- la etiqueta del botón coincide con el título de la tarjeta `i + 1`;
- la última tarjeta muestra finalización y no un siguiente inexistente;
- no se permiten índices 0, repetidos o fuera del rango.

**Resultado esperado:** el defecto de Día 3 se reporta indicando el botón cuya
etiqueta repite el ejercicio actual.

## 4. Casos negativos y de frontera

- HTML sin tarjetas.
- Dos tarjetas con el mismo `data-exercise`.
- Salto de índice, por ejemplo 2 → 4.
- `data-series-keys` vacío, duplicado o con `s0`.
- Total declarado distinto de la suma.
- Calentamiento contado como serie efectiva.
- Última tarjeta con `data-next`.
- Texto del dashboard con total correcto pero trackers incompletos.
- Atributo presente en una tarjeta y ausente en otra.

## 5. Implementación

El validador de solo lectura es
`scripts/validate_canonical_routines.py` y usa el parser HTML de la biblioteca
estándar o una estrategia equivalente estable. Debe:

1. recibir rutas explícitas o usar las tres canónicas por defecto;
2. emitir errores estructurados con archivo, ejercicio, atributo, esperado y
   observado;
3. devolver código distinto de cero ante cualquier discrepancia;
4. no modificar HTML, documentos, manifiestos ni artefactos;
5. poder ejecutarse desde PowerShell y desde una prueba Python; y
6. evitar volcar imágenes embebidas o contenido base64 en la salida.

Comando de ejecución sobre las tres salidas:

```powershell
python scripts/validate_canonical_routines.py
```

También acepta rutas explícitas para aislar un día durante el diagnóstico.

La prueba se mantiene separada del validador general hasta que la salida canónica
actual sea corregida; de ese modo el fallo se observa como evidencia explícita
y no se oculta cambiando el esperado.

## 6. Evidencia requerida

- salida del validador con versión de Python y rutas revisadas;
- prueba de que el caso falla ante una mutación sintética de cada invariante;
- salida posterior sin discrepancias tras corregir el contenido;
- `python scripts/validate_repository.py` y `git diff --check`;
- revisión visual independiente para confirmar que el DOM corregido se ve y
  navega correctamente.

La prueba automatizada demuestra estructura y aritmética; no demuestra por sí
sola técnica de ejercicio, exactitud del equipo, experiencia de usuario ni
validez científica de la prescripción.

## 7. Criterio de cierre

TDD-002 pasa a `Verified` cuando los tres días superan TST-CAN-001..003, las
mutaciones negativas son rechazadas y la evidencia queda enlazada en
`TRACEABILITY.md`. Mientras Día 1 o Día 3 conserven los defectos descritos, el
estado correcto es `Partial` o `In progress`, nunca `Verified`.
